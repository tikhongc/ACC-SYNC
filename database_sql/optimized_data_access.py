# -*- coding: utf-8 -*-
"""
优化的PostgreSQL数据访问层
基于同步优化方案，支持批量操作和智能跳过
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Tuple
from contextlib import asynccontextmanager

import asyncpg
from database_sql.neon_config import neon_postgresql_config

logger = logging.getLogger(__name__)

class OptimizedPostgreSQLDataAccess:
    """优化的PostgreSQL数据访问层"""
    
    def __init__(self):
        self.config = neon_postgresql_config
        self._pool: Optional[asyncpg.Pool] = None
    
    async def connect(self):
        """连接数据库"""
        if self._pool is None:
            self._pool = await self.config.create_pool()
        return self
    
    async def close(self):
        """关闭数据库连接"""
        if self._pool:
            await self._pool.close()
            self._pool = None
    
    @asynccontextmanager
    async def get_connection(self):
        """获取数据库连接"""
        if self._pool is None:
            await self.connect()
        
        async with self._pool.acquire() as conn:
            yield conn
    
    # ============================================================================
    # 🚀 Layer 1: 智能分支跳过优化
    # ============================================================================
    
    async def get_folders_for_smart_skip_check(self, project_id: str, last_sync_time: datetime) -> List[Dict[str, Any]]:
        """获取需要智能跳过检查的文件夹"""
        try:
            async with self.get_connection() as conn:
                # 🔑 核心优化：使用 rollup 时间进行智能分支跳过
                query = """
                WITH changed_folders AS (
                    SELECT 
                        f.id,
                        f.name,
                        f.path,
                        f.depth,
                        f.last_modified_time,
                        f.last_modified_time_rollup,
                        f.parent_id,
                        f.object_count
                    FROM folders f
                    WHERE f.project_id = $1
                      AND (f.last_modified_time_rollup > $2 OR f.last_modified_time_rollup IS NULL)
                )
                SELECT 
                    cf.*,
                    COUNT(sub.id) as subfolder_count
                FROM changed_folders cf
                LEFT JOIN folders sub ON sub.parent_id = cf.id
                GROUP BY cf.id, cf.name, cf.path, cf.depth, cf.last_modified_time, 
                         cf.last_modified_time_rollup, cf.parent_id, cf.object_count
                ORDER BY cf.depth, cf.path;
                """
                
                rows = await conn.fetch(query, project_id, last_sync_time)
                return [self._row_to_dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"获取智能跳过文件夹失败: {e}")
            return []
    
    async def get_changed_files_since_last_sync(self, project_id: str, last_sync_time: datetime, 
                                              folder_ids: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """获取自上次同步以来变化的文件"""
        try:
            async with self.get_connection() as conn:
                # 构建查询条件
                conditions = ["f.project_id = $1", "f.last_modified_time > $2"]
                params = [project_id, last_sync_time]
                
                if folder_ids:
                    conditions.append(f"f.parent_folder_id = ANY($3)")
                    params.append(folder_ids)
                
                query = f"""
                SELECT 
                    f.id,
                    f.name,
                    f.display_name,
                    f.parent_folder_id,
                    f.folder_path,
                    f.file_type,
                    f.last_modified_time,
                    f.current_version_id,
                    f.version_number,
                    f.file_size,
                    fo.name as folder_name,
                    fo.path as folder_path_full
                FROM files f
                LEFT JOIN folders fo ON f.parent_folder_id = fo.id
                WHERE {' AND '.join(conditions)}
                ORDER BY f.last_modified_time DESC;
                """
                
                rows = await conn.fetch(query, *params)
                return [self._row_to_dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"获取变化文件失败: {e}")
            return []
    
    # ============================================================================
    # 🚀 Layer 2: 批量操作优化
    # ============================================================================
    
    async def batch_upsert_folders(self, folders_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量插入/更新文件夹"""
        if not folders_data:
            return {'upserted': 0, 'errors': []}
        
        try:
            async with self.get_connection() as conn:
                async with conn.transaction():
                    upsert_query = """
                    INSERT INTO folders (
                        id, project_id, name, display_name, parent_id, path, path_segments, depth,
                        create_time, create_user_id, create_user_name,
                        last_modified_time, last_modified_user_id, last_modified_user_name,
                        last_modified_time_rollup, object_count, total_file_size, hidden,
                        metadata, folder_permissions, folder_settings, sync_info, updated_at
                    ) VALUES (
                        $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23
                    )
                    ON CONFLICT (id) 
                    DO UPDATE SET
                        name = EXCLUDED.name,
                        display_name = EXCLUDED.display_name,
                        parent_id = EXCLUDED.parent_id,
                        path = EXCLUDED.path,
                        path_segments = EXCLUDED.path_segments,
                        depth = EXCLUDED.depth,
                        last_modified_time = EXCLUDED.last_modified_time,
                        last_modified_user_id = EXCLUDED.last_modified_user_id,
                        last_modified_user_name = EXCLUDED.last_modified_user_name,
                        last_modified_time_rollup = EXCLUDED.last_modified_time_rollup,
                        object_count = EXCLUDED.object_count,
                        total_file_size = EXCLUDED.total_file_size,
                        hidden = EXCLUDED.hidden,
                        metadata = EXCLUDED.metadata,
                        folder_permissions = EXCLUDED.folder_permissions,
                        folder_settings = EXCLUDED.folder_settings,
                        sync_info = EXCLUDED.sync_info,
                        updated_at = EXCLUDED.updated_at
                    WHERE folders.last_modified_time < EXCLUDED.last_modified_time
                       OR folders.last_modified_time_rollup < EXCLUDED.last_modified_time_rollup;
                    """
                    
                    upsert_count = 0
                    errors = []
                    
                    for folder_data in folders_data:
                        try:
                            folder_record = self._prepare_folder_record(folder_data)
                            await conn.execute(upsert_query, *folder_record)
                            upsert_count += 1
                        except Exception as e:
                            errors.append(f"Folder {folder_data.get('id')}: {str(e)}")
                    
                    return {'upserted': upsert_count, 'errors': errors}
                    
        except Exception as e:
            logger.error(f"批量文件夹操作失败: {e}")
            return {'upserted': 0, 'errors': [str(e)]}
    
    async def batch_upsert_files(self, files_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量插入/更新文件"""
        if not files_data:
            return {'upserted': 0, 'errors': []}
        
        try:
            async with self.get_connection() as conn:
                async with conn.transaction():
                    upsert_query = """
                    INSERT INTO files (
                        id, project_id, name, display_name, parent_folder_id, folder_path, full_path,
                        path_segments, depth, create_time, create_user_id, create_user_name,
                        last_modified_time, last_modified_user_id, last_modified_user_name,
                        file_type, mime_type, reserved, hidden, metadata, 
                        file_permissions, file_settings, review_info, sync_info, updated_at
                    ) VALUES (
                        $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20,
                        $21, $22, $23, $24, $25
                    )
                    ON CONFLICT (id) 
                    DO UPDATE SET
                        name = EXCLUDED.name,
                        display_name = EXCLUDED.display_name,
                        parent_folder_id = EXCLUDED.parent_folder_id,
                        folder_path = EXCLUDED.folder_path,
                        full_path = EXCLUDED.full_path,
                        path_segments = EXCLUDED.path_segments,
                        depth = EXCLUDED.depth,
                        last_modified_time = EXCLUDED.last_modified_time,
                        last_modified_user_id = EXCLUDED.last_modified_user_id,
                        last_modified_user_name = EXCLUDED.last_modified_user_name,
                        file_type = EXCLUDED.file_type,
                        mime_type = EXCLUDED.mime_type,
                        reserved = EXCLUDED.reserved,
                        hidden = EXCLUDED.hidden,
                        metadata = EXCLUDED.metadata,
                        file_permissions = EXCLUDED.file_permissions,
                        file_settings = EXCLUDED.file_settings,
                        review_info = EXCLUDED.review_info,
                        sync_info = EXCLUDED.sync_info,
                        updated_at = EXCLUDED.updated_at
                    WHERE files.last_modified_time IS NULL OR files.last_modified_time < EXCLUDED.last_modified_time;
                    """
                    
                    upsert_count = 0
                    errors = []
                    
                    for file_data in files_data:
                        try:
                            file_record = self._prepare_file_record(file_data)
                            await conn.execute(upsert_query, *file_record)
                            upsert_count += 1
                        except Exception as e:
                            errors.append(f"File {file_data.get('id')}: {str(e)}")
                    
                    return {'upserted': upsert_count, 'errors': errors}
                    
        except Exception as e:
            logger.error(f"批量文件操作失败: {e}")
            return {'upserted': 0, 'errors': [str(e)]}
    
    # ============================================================================
    # 🚀 Layer 3: 自定义属性分离表优化
    # ============================================================================
    
    async def batch_upsert_custom_attribute_definitions(self, definitions_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量插入/更新自定义属性定义"""
        if not definitions_data:
            return {'upserted': 0, 'errors': []}
        
        try:
            async with self.get_connection() as conn:
                async with conn.transaction():
                    upsert_query = """
                    INSERT INTO custom_attribute_definitions (
                        attr_id, project_id, scope_type, scope_folder_id, inherit_to_subfolders,
                        name, type, array_values, description, is_required, default_value,
                        validation_rules, sync_info, updated_at
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
                    ON CONFLICT (attr_id, project_id, COALESCE(scope_folder_id, ''))
                    DO UPDATE SET
                        scope_type = EXCLUDED.scope_type,
                        inherit_to_subfolders = EXCLUDED.inherit_to_subfolders,
                        name = EXCLUDED.name,
                        type = EXCLUDED.type,
                        array_values = EXCLUDED.array_values,
                        description = EXCLUDED.description,
                        is_required = EXCLUDED.is_required,
                        default_value = EXCLUDED.default_value,
                        validation_rules = EXCLUDED.validation_rules,
                        sync_info = EXCLUDED.sync_info,
                        updated_at = EXCLUDED.updated_at;
                    """
                    
                    upsert_count = 0
                    errors = []
                    
                    for def_data in definitions_data:
                        try:
                            def_record = self._prepare_custom_attr_definition_record(def_data)
                            await conn.execute(upsert_query, *def_record)
                            upsert_count += 1
                        except Exception as e:
                            errors.append(f"Definition {def_data.get('attr_id')}: {str(e)}")
                    
                    return {'upserted': upsert_count, 'errors': errors}
                    
        except Exception as e:
            logger.error(f"批量属性定义操作失败: {e}")
            return {'upserted': 0, 'errors': [str(e)]}
    
    async def batch_upsert_custom_attribute_values(self, values_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量插入/更新自定义属性值"""
        if not values_data:
            return {'upserted': 0, 'errors': []}
        
        try:
            async with self.get_connection() as conn:
                async with conn.transaction():
                    upsert_query = """
                    INSERT INTO custom_attribute_values (
                        file_id, attr_definition_id, project_id, value, value_date, value_number, 
                        value_boolean, value_array, updated_at, updated_by_user_id, updated_by_user_name,
                        validation_status, validation_errors, sync_info
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
                    ON CONFLICT (file_id, attr_definition_id)
                    DO UPDATE SET
                        value = EXCLUDED.value,
                        value_date = EXCLUDED.value_date,
                        value_number = EXCLUDED.value_number,
                        value_boolean = EXCLUDED.value_boolean,
                        value_array = EXCLUDED.value_array,
                        updated_at = EXCLUDED.updated_at,
                        updated_by_user_id = EXCLUDED.updated_by_user_id,
                        updated_by_user_name = EXCLUDED.updated_by_user_name,
                        validation_status = EXCLUDED.validation_status,
                        validation_errors = EXCLUDED.validation_errors,
                        sync_info = EXCLUDED.sync_info;
                    """
                    
                    upsert_count = 0
                    errors = []
                    
                    for value_data in values_data:
                        try:
                            value_record = self._prepare_custom_attr_value_record(value_data)
                            await conn.execute(upsert_query, *value_record)
                            upsert_count += 1
                        except Exception as e:
                            errors.append(f"Value {value_data.get('file_id')}-{value_data.get('attr_id')}: {str(e)}")
                    
                    return {'upserted': upsert_count, 'errors': errors}
                    
        except Exception as e:
            logger.error(f"批量属性值操作失败: {e}")
            return {'upserted': 0, 'errors': [str(e)]}
    
    async def get_files_with_custom_attributes(self, project_id: str, file_ids: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """获取文件及其自定义属性（优化查询）"""
        try:
            async with self.get_connection() as conn:
                # 构建查询条件
                conditions = ["f.project_id = $1"]
                params = [project_id]
                
                if file_ids:
                    conditions.append("f.id = ANY($2)")
                    params.append(file_ids)
                
                # 🔑 使用JSONB聚合优化查询
                query = f"""
                SELECT 
                    f.*,
                    COALESCE(
                        JSONB_AGG(
                            JSONB_BUILD_OBJECT(
                                'attr_id', cav.attr_id,
                                'name', cad.name,
                                'type', cad.type,
                                'value', cav.value,
                                'value_date', cav.value_date,
                                'value_number', cav.value_number,
                                'value_boolean', cav.value_boolean,
                                'array_values', cad.array_values,
                                'updated_at', cav.updated_at
                            ) ORDER BY cad.name
                        ) FILTER (WHERE cav.attr_id IS NOT NULL),
                        '[]'::jsonb
                    ) as custom_attributes
                FROM files f
                LEFT JOIN custom_attribute_values cav ON cav.file_id = f.id
                LEFT JOIN custom_attribute_definitions cad ON cad.attr_id = cav.attr_id 
                    AND cad.project_id = cav.project_id
                WHERE {' AND '.join(conditions)}
                GROUP BY f.id
                ORDER BY f.name;
                """
                
                rows = await conn.fetch(query, *params)
                return [self._row_to_dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"获取文件自定义属性失败: {e}")
            return []
    
    # ============================================================================
    # 🚀 Layer 4: 同步任务管理优化
    # ============================================================================
    
    async def create_sync_task(self, task_data: Dict[str, Any]) -> str:
        """创建同步任务"""
        try:
            async with self.get_connection() as conn:
                query = """
                INSERT INTO sync_tasks (
                    task_uuid, project_id, task_type, task_status, performance_mode,
                    parameters, progress, performance_stats, sync_results, 
                    start_time, created_at, updated_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
                RETURNING task_uuid;
                """
                
                task_uuid = task_data.get('task_uuid')
                result = await conn.fetchrow(
                    query,
                    task_uuid,
                    task_data.get('project_id'),
                    task_data.get('task_type'),
                    task_data.get('task_status', 'pending'),
                    task_data.get('performance_mode', 'standard'),
                    json.dumps(task_data.get('parameters', {})),
                    json.dumps(task_data.get('progress', {})),
                    json.dumps(task_data.get('performance_stats', {})),
                    json.dumps(task_data.get('results', {})),
                    task_data.get('start_time'),
                    datetime.now(),
                    datetime.now()
                )
                
                return result['task_uuid']
                
        except Exception as e:
            logger.error(f"创建同步任务失败: {e}")
            return None
    
    async def update_sync_task_progress(self, task_uuid: str, progress_data: Dict[str, Any]) -> bool:
        """更新同步任务进度"""
        try:
            async with self.get_connection() as conn:
                query = """
                UPDATE sync_tasks 
                SET progress = $2, 
                    performance_stats = $3,
                    task_status = $4,
                    updated_at = $5
                WHERE task_uuid = $1;
                """
                
                result = await conn.execute(
                    query,
                    task_uuid,
                    json.dumps(progress_data.get('progress', {})),
                    json.dumps(progress_data.get('performance_stats', {})),
                    progress_data.get('task_status', 'running'),
                    datetime.now()
                )
                
                return "UPDATE 1" in result
                
        except Exception as e:
            logger.error(f"更新同步任务进度失败: {e}")
            return False
    
    async def complete_sync_task(self, task_uuid: str, results: Dict[str, Any]) -> bool:
        """Complete sync task with enhanced schema support"""
        try:
            async with self.get_connection() as conn:
                # Determine task status
                task_status = 'completed' if results.get('status') == 'success' else 'failed'
                
                query = """
                UPDATE sync_tasks 
                SET task_status = $2,
                    sync_results = $3,
                    synced_file_tree = $4,
                    synced_versions = $5,
                    synced_custom_attributes_definitions = $6,
                    synced_custom_attributes_values = $7,
                    synced_permissions = $8,
                    folders_synced = $9,
                    files_synced = $10,
                    versions_synced = $11,
                    custom_attrs_synced = $12,
                    performance_stats = $13,
                    error_message = $14,
                    error_details = $15,
                    end_time = $16,
                    duration_seconds = EXTRACT(EPOCH FROM ($16 - start_time)),
                    updated_at = $17
                WHERE task_uuid = $1;
                """
                
                end_time = datetime.now()
                result = await conn.execute(
                    query,
                    task_uuid,
                    task_status,
                    json.dumps(results),
                    results.get('synced_file_tree', False),
                    results.get('synced_versions', False),
                    results.get('synced_custom_attributes_definitions', False),
                    results.get('synced_custom_attributes_values', False),
                    results.get('synced_permissions', False),
                    results.get('folders_synced', 0),
                    results.get('files_synced', 0),
                    results.get('versions_synced', 0),
                    results.get('custom_attrs_synced', 0),
                    json.dumps(results.get('performance_stats', {})),
                    results.get('error', None),
                    json.dumps(results.get('error_details', {})),
                    end_time,
                    datetime.now()
                )
                
                return "UPDATE 1" in result
                
        except Exception as e:
            logger.error(f"Failed to complete sync task: {e}")
            return False
    
    async def get_project_last_sync_time(self, project_id: str) -> Optional[datetime]:
        """获取项目最后同步时间"""
        try:
            async with self.get_connection() as conn:
                query = """
                SELECT last_sync_time 
                FROM projects 
                WHERE id = $1;
                """
                
                result = await conn.fetchrow(query, project_id)
                return result['last_sync_time'] if result else None
                
        except Exception as e:
            logger.error(f"获取项目同步时间失败: {e}")
            return None
    

    async def batch_upsert_file_versions(self, versions_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量插入或更新文件版本"""
        try:
            async with self.get_connection() as conn:
                if not versions_data:
                    return {'upserted': 0, 'errors': []}
                
                # 准备插入数据 - V2架构
                insert_query = """
                INSERT INTO file_versions (
                    id, file_id, project_id, version_number, urn, item_urn, storage_urn, lineage_urn,
                    create_time, create_user_id, create_user_name, last_modified_time, last_modified_user_id, last_modified_user_name,
                    file_size, storage_size, mime_type, process_state, is_current_version, version_status,
                    metadata, review_info, extension, download_info, download_url, sync_info
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26)
                ON CONFLICT (id) DO UPDATE SET
                    version_number = EXCLUDED.version_number,
                    urn = EXCLUDED.urn,
                    item_urn = EXCLUDED.item_urn,
                    storage_urn = EXCLUDED.storage_urn,
                    lineage_urn = EXCLUDED.lineage_urn,
                    last_modified_time = EXCLUDED.last_modified_time,
                    last_modified_user_id = EXCLUDED.last_modified_user_id,
                    last_modified_user_name = EXCLUDED.last_modified_user_name,
                    file_size = EXCLUDED.file_size,
                    storage_size = EXCLUDED.storage_size,
                    mime_type = EXCLUDED.mime_type,
                    process_state = EXCLUDED.process_state,
                    is_current_version = EXCLUDED.is_current_version,
                    version_status = EXCLUDED.version_status,
                    metadata = EXCLUDED.metadata,
                    review_info = EXCLUDED.review_info,
                    extension = EXCLUDED.extension,
                    download_info = EXCLUDED.download_info,
                    download_url = EXCLUDED.download_url,
                    sync_info = EXCLUDED.sync_info,
                    updated_at = CURRENT_TIMESTAMP;
                """
                
                upserted_count = 0
                errors = []
                
                for version_data in versions_data:
                    try:
                        await conn.execute(
                            insert_query,
                            version_data.get('id'),
                            version_data.get('file_id'),
                            version_data.get('project_id'),
                            version_data.get('version_number', 1),
                            version_data.get('urn', version_data.get('id')),  # Use id as urn if not provided
                            version_data.get('item_urn'),
                            version_data.get('storage_urn'),
                            version_data.get('lineage_urn'),
                            self._parse_datetime(version_data.get('create_time')),
                            version_data.get('create_user_id'),
                            version_data.get('create_user_name'),
                            self._parse_datetime(version_data.get('last_modified_time')),
                            version_data.get('last_modified_user_id'),
                            version_data.get('last_modified_user_name'),
                            version_data.get('file_size', 0),
                            version_data.get('storage_size', 0),
                            version_data.get('mime_type'),
                            version_data.get('process_state'),
                            version_data.get('is_current_version', False),
                            version_data.get('version_status', 'active'),
                            json.dumps(version_data.get('metadata', {})),
                            json.dumps(version_data.get('review_info', {})),
                            json.dumps(version_data.get('extension', {})),
                            json.dumps(version_data.get('download_info', {})),
                            version_data.get('download_url'),
                            json.dumps(version_data.get('sync_info', {}))
                        )
                        upserted_count += 1
                    except Exception as e:
                        errors.append(f"Version {version_data.get('id', 'unknown')}: {str(e)}")
                
                return {
                    'upserted': upserted_count,
                    'errors': errors
                }
                
        except Exception as e:
            logger.error(f"批量文件版本操作失败: {e}")
            return {'upserted': 0, 'errors': [str(e)]}

    async def update_project_sync_info(self, project_id: str, sync_info: Dict[str, Any]) -> bool:
        """更新项目同步信息"""
        try:
            async with self.get_connection() as conn:
                query = """
                UPDATE projects 
                SET last_sync_time = $2,
                    sync_status = $3,
                    sync_stats = $4,
                    updated_at = $5
                WHERE id = $1;
                """
                
                result = await conn.execute(
                    query,
                    project_id,
                    sync_info.get('last_sync_time'),
                    sync_info.get('sync_status', 'completed'),
                    json.dumps(sync_info.get('sync_stats', {})),
                    datetime.now()
                )
                
                return "UPDATE 1" in result
                
        except Exception as e:
            logger.error(f"更新项目同步信息失败: {e}")
            return False
    
    # ============================================================================
    # 辅助方法
    # ============================================================================
    
    def _prepare_folder_record(self, folder_data: Dict[str, Any]) -> Tuple:
        """准备文件夹记录 - V2架构"""
        return (
            folder_data.get('id'),
            folder_data.get('project_id'),
            folder_data.get('name'),
            folder_data.get('display_name'),
            folder_data.get('parent_id'),
            folder_data.get('path'),
            folder_data.get('path_segments', []),
            folder_data.get('depth', 0),
            self._parse_datetime(folder_data.get('create_time')),
            folder_data.get('create_user_id'),
            folder_data.get('create_user_name'),
            self._parse_datetime(folder_data.get('last_modified_time')),
            folder_data.get('last_modified_user_id'),
            folder_data.get('last_modified_user_name'),
            self._parse_datetime(folder_data.get('last_modified_time_rollup')),
            folder_data.get('object_count', 0),
            folder_data.get('total_size', 0),  # Will map to total_file_size
            folder_data.get('hidden', False),
            json.dumps(folder_data.get('metadata', {})),
            json.dumps(folder_data.get('folder_permissions', {})),  # V2 field
            json.dumps(folder_data.get('folder_settings', {})),     # V2 field
            json.dumps(folder_data.get('sync_info', {})),
            datetime.now()
        )
    
    def _prepare_file_record(self, file_data: Dict[str, Any]) -> Tuple:
        """准备文件记录 - V2架构"""
        return (
            file_data.get('id'),
            file_data.get('project_id'),
            file_data.get('name'),
            file_data.get('display_name'),
            file_data.get('parent_folder_id'),
            file_data.get('folder_path', ''),
            file_data.get('full_path'),
            file_data.get('path_segments', []),
            file_data.get('depth', 0),
            self._parse_datetime(file_data.get('create_time')),
            file_data.get('create_user_id'),
            file_data.get('create_user_name'),
            self._parse_datetime(file_data.get('last_modified_time')),
            file_data.get('last_modified_user_id'),
            file_data.get('last_modified_user_name'),
            file_data.get('file_type'),
            file_data.get('mime_type'),
            file_data.get('reserved', False),
            file_data.get('hidden', False),
            json.dumps(file_data.get('metadata', {})),
            json.dumps(file_data.get('file_permissions', {})),
            json.dumps(file_data.get('file_settings', {})),
            json.dumps(file_data.get('review_info', {})),
            json.dumps(file_data.get('sync_info', {})),
            datetime.now()
        )
    
    def _prepare_custom_attr_definition_record(self, def_data: Dict[str, Any]) -> Tuple:
        """准备自定义属性定义记录 - V2架构"""
        return (
            def_data.get('attr_id'),
            def_data.get('project_id'),
            def_data.get('scope_type', 'project'),  # V2 field
            def_data.get('scope_folder_id'),        # V2 field (renamed from folder_id)
            def_data.get('inherit_to_subfolders', True),  # V2 field
            def_data.get('name'),
            def_data.get('type'),
            json.dumps(def_data.get('array_values')) if def_data.get('array_values') else None,
            def_data.get('description'),
            def_data.get('is_required', False),
            def_data.get('default_value'),
            json.dumps(def_data.get('validation_rules', {})),  # V2 field
            json.dumps(def_data.get('sync_info', {})),
            datetime.now()
        )
    
    def _prepare_custom_attr_value_record(self, value_data: Dict[str, Any]) -> Tuple:
        """准备自定义属性值记录 - V2架构"""
        return (
            value_data.get('file_id'),
            value_data.get('attr_definition_id'),  # V2 field (renamed from attr_id)
            value_data.get('project_id'),
            value_data.get('value'),
            self._parse_datetime(value_data.get('value_date')),
            value_data.get('value_number'),
            value_data.get('value_boolean'),
            json.dumps(value_data.get('value_array')) if value_data.get('value_array') else None,  # V2 field
            datetime.now(),
            value_data.get('updated_by_user_id'),
            value_data.get('updated_by_user_name'),
            value_data.get('validation_status', 'valid'),  # V2 field
            json.dumps(value_data.get('validation_errors', [])),  # V2 field
            json.dumps(value_data.get('sync_info', {}))
        )
    
    def _parse_datetime(self, datetime_str) -> Optional[datetime]:
        """Parse datetime string or datetime object - preserves timezone info"""
        if not datetime_str:
            return None
        
        # If already a datetime object, return as is (preserves timezone)
        if isinstance(datetime_str, datetime):
            return datetime_str
        
        # If not a string, return None
        if not isinstance(datetime_str, str):
            return None
        
        try:
            # Handle ACC API special format: 2025-10-20T02:32:52.0000000Z
            if 'T' in datetime_str:
                # Handle UTC time ending with Z
                if datetime_str.endswith('Z'):
                    # Handle more than 6 decimal places (Python's %f only supports 6)
                    if '.' in datetime_str:
                        date_part, time_part = datetime_str.split('T')
                        if '.' in time_part:
                            time_base, microseconds_z = time_part.split('.')
                            microseconds = microseconds_z.rstrip('Z')
                            # Truncate or pad to 6 digits
                            if len(microseconds) > 6:
                                microseconds = microseconds[:6]
                            else:
                                microseconds = microseconds.ljust(6, '0')
                            datetime_str = f"{date_part}T{time_base}.{microseconds}Z"
                    
                    # Use fromisoformat for processing
                    return datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
                else:
                    return datetime.fromisoformat(datetime_str)
            
            # Try other formats
            formats = [
                "%Y-%m-%dT%H:%M:%S.%fZ",
                "%Y-%m-%dT%H:%M:%SZ", 
                "%Y-%m-%dT%H:%M:%S.%f",
                "%Y-%m-%dT%H:%M:%S"
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(datetime_str, fmt)
                except ValueError:
                    continue
            
            logger.warning(f"Cannot parse datetime: {datetime_str}")
            return None
            
        except Exception as e:
            logger.warning(f"Datetime parsing error: {e}")
            return None
    
    def _row_to_dict(self, row) -> Dict[str, Any]:
        """将数据库行转换为字典"""
        if row is None:
            return {}
        
        result = dict(row)
        
        # 将JSON字段解析回Python对象
        json_fields = ['metadata', 'extension', 'file_info', 'current_version', 
                      'versions_summary', 'children_stats', 'sync_info', 'parameters', 
                      'progress', 'performance_stats', 'results', 'custom_attributes',
                      'array_values', 'relation_metadata']
        
        for field in json_fields:
            if field in result and result[field]:
                try:
                    if isinstance(result[field], str):
                        result[field] = json.loads(result[field])
                except (json.JSONDecodeError, TypeError):
                    logger.warning(f"无法解析JSON字段 {field}: {result[field]}")
                    result[field] = {}
        
        # 兼容MongoDB的_id字段
        if 'id' in result:
            result['_id'] = result['id']
        
        return result

# 全局优化数据访问实例
optimized_postgresql_dal = OptimizedPostgreSQLDataAccess()

# 便捷函数
async def get_optimized_postgresql_dal():
    """获取优化的PostgreSQL数据访问层实例"""
    await optimized_postgresql_dal.connect()
    return optimized_postgresql_dal

async def close_optimized_postgresql_dal():
    """关闭优化的PostgreSQL数据访问层"""
    await optimized_postgresql_dal.close()
