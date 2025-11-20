#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件树构建器 - 核心业务逻辑

功能：
1. 从数据库查询文件夹和文件数据
2. 构建树形结构
3. 格式化为前端需要的格式
4. 存储到缓存表
"""

import json
import time
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timezone
import psycopg2
import psycopg2.extras
import logging

logger = logging.getLogger(__name__)


class FileTreeBuilder:
    """文件树构建器"""

    def __init__(self, db_params: Dict[str, str]):
        """
        初始化构建器

        Args:
            db_params: 数据库连接参数 {host, port, database, user, password, sslmode}
        """
        self.db_params = db_params
        self.conn = None
        self.cur = None

    def connect(self) -> bool:
        """连接数据库"""
        try:
            self.conn = psycopg2.connect(**self.db_params)
            self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            logger.info("数据库连接成功")
            return True
        except Exception as e:
            logger.error(f"数据库连接失败: {str(e)}")
            return False

    def disconnect(self):
        """断开数据库连接"""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        logger.info("数据库连接已关闭")

    def query_folders(self, project_id: str) -> List[Dict[str, Any]]:
        """
        查询项目下的所有文件夹

        Returns:
            文件夹列表，包含: id, project_id, name, display_name, parent_id, path,
                           depth, create_time, create_user_name, last_modified_time, hidden
        """
        sql = """
        SELECT
            id,
            project_id,
            name,
            COALESCE(display_name, name) as display_name,
            parent_id,
            path,
            depth,
            create_time,
            create_user_name,
            last_modified_time,
            last_modified_user_name,
            hidden
        FROM folders
        WHERE project_id = %s
        ORDER BY path ASC;
        """

        try:
            self.cur.execute(sql, (project_id,))
            folders = self.cur.fetchall()
            logger.info(f"查询到 {len(folders)} 个文件夹")
            return [dict(row) for row in folders]
        except Exception as e:
            logger.error(f"查询文件夹失败: {str(e)}")
            return []

    def query_files(self, project_id: str) -> List[Dict[str, Any]]:
        """
        查询项目下的所有文件（使用最新版本的数据）

        Returns:
            文件列表，包含: id, name, folder_path, file_type, create_time,
                           create_user_name, last_modified_user_name, last_modified_time,
                           version_number, size (file_size), urn, reviewState
        """
        sql = """
        SELECT
            f.id,
            f.name,
            COALESCE(f.folder_path, '') as folder_path,
            f.file_type,
            f.create_time,
            f.create_user_name,
            COALESCE(fv.create_user_name, f.last_modified_user_name) as last_modified_user_name,
            COALESCE(fv.create_time, f.last_modified_time) as last_modified_time,
            fv.version_number,
            fv.file_size as size,
            fv.urn,
            fv.review_state AS "reviewState"
        FROM files f
        LEFT JOIN file_versions fv ON f.id = fv.file_id AND fv.is_current_version = true
        WHERE f.project_id = %s
        ORDER BY f.name ASC;
        """

        try:
            self.cur.execute(sql, (project_id,))
            files = self.cur.fetchall()
            logger.info(f"查询到 {len(files)} 个文件")
            return [dict(row) for row in files]
        except Exception as e:
            logger.error(f"查询文件失败: {str(e)}")
            return []

    def query_custom_attributes(self, project_id: str) -> Dict[str, List[Dict]]:
        """
        查询文件的自定义属性值

        Returns:
            字典，key为file_id，value为属性列表
        """
        sql = """
        SELECT
            cav.file_id,
            cad.name as attr_name,
            cad.type as attr_type,
            cav.value,
            cav.value_date,
            cav.value_number,
            cav.value_boolean,
            cav.value_array
        FROM custom_attribute_values cav
        JOIN custom_attribute_definitions cad ON cav.attr_definition_id = cad.id
        WHERE cav.project_id = %s;
        """

        try:
            self.cur.execute(sql, (project_id,))
            rows = self.cur.fetchall()

            # 按file_id分组
            attrs_by_file = {}
            for row in rows:
                file_id = row['file_id']
                if file_id not in attrs_by_file:
                    attrs_by_file[file_id] = []

                # 获取实际的值（取决于类型）
                value = (
                    row['value'] or
                    row['value_date'] or
                    row['value_number'] or
                    row['value_boolean'] or
                    row['value_array']
                )

                attrs_by_file[file_id].append({
                    'name': row['attr_name'],
                    'type': row['attr_type'],
                    'value': value
                })

            logger.info(f"查询到 {len(attrs_by_file)} 个文件的自定义属性")
            return attrs_by_file
        except Exception as e:
            logger.error(f"查询自定义属性失败: {str(e)}")
            return {}

    def query_folder_custom_attributes(self, project_id: str) -> Dict[str, List[Dict]]:
        """
        查询文件夹的自定义属性设置（scope_type='folder'）

        Returns:
            字典，key为folder_id，value为属性定义列表
        """
        sql = """
        SELECT
            scope_folder_id,
            attr_id,
            name,
            type,
            array_values,
            description,
            is_required,
            default_value,
            inherit_to_subfolders
        FROM custom_attribute_definitions
        WHERE project_id = %s AND scope_type = 'folder' AND scope_folder_id IS NOT NULL;
        """

        try:
            self.cur.execute(sql, (project_id,))
            rows = self.cur.fetchall()

            # 按folder_id分组
            attrs_by_folder = {}
            for row in rows:
                folder_id = row['scope_folder_id']
                if folder_id not in attrs_by_folder:
                    attrs_by_folder[folder_id] = []

                attrs_by_folder[folder_id].append({
                    'attr_id': row['attr_id'],
                    'name': row['name'],
                    'type': row['type'],
                    'array_values': row['array_values'],
                    'description': row['description'],
                    'is_required': row['is_required'],
                    'default_value': row['default_value'],
                    'inherit_to_subfolders': row['inherit_to_subfolders']
                })

            logger.info(f"查询到 {len(attrs_by_folder)} 个文件夹的自定义属性设置")
            return attrs_by_folder
        except Exception as e:
            logger.error(f"查询文件夹自定义属性失败: {str(e)}")
            return {}

    def build_tree_from_paths(self, folders: List[Dict], files: List[Dict],
                               folder_attrs: Dict[str, List[Dict]] = None,
                               file_attrs: Dict[str, List[Dict]] = None) -> Dict:
        """
        将扁平的文件夹和文件列表构建成树形结构

        Args:
            folders: 文件夹列表
            files: 文件列表
            folder_attrs: 文件夹自定义属性设置，key为folder_id
            file_attrs: 文件自定义属性值，key为file_id

        Returns:
            树形结构字典
        """
        logger.info("开始构建树形结构...")

        # 初始化默认值
        if folder_attrs is None:
            folder_attrs = {}
        if file_attrs is None:
            file_attrs = {}

        # 步骤1: 创建文件夹树的"骨架"
        folder_tree = {}  # key: folder_id, value: folder_info

        for folder in folders:
            folder_id = folder['id']
            folder_tree[folder_id] = {
                'type': 'folder',
                'id': folder_id,
                'name': folder['display_name'],
                'path': folder['path'],
                'create_time': folder['create_time'].isoformat() if folder['create_time'] else None,
                'create_user_name': folder['create_user_name'],
                'last_modified_time': folder['last_modified_time'].isoformat() if folder['last_modified_time'] else None,
                'hidden': folder['hidden'],
                'last_modified_user_name': folder.get('last_modified_user_name'),
                'customAttributes': folder_attrs.get(folder_id, []),  # 添加文件夹的自定义属性设置
                'children': []  # 先设置为空数组，后面添加子项
            }

        # 步骤2: 构建树的层级关系
        root_folders = []  # 根文件夹

        for folder in folders:
            folder_id = folder['id']
            parent_id = folder['parent_id']

            if parent_id is None:
                # 根文件夹
                root_folders.append(folder_tree[folder_id])
            else:
                # 有父文件夹
                if parent_id in folder_tree:
                    parent = folder_tree[parent_id]
                    if 'children' not in parent:
                        parent['children'] = []
                    parent['children'].append(folder_tree[folder_id])
                else:
                    logger.warning(f"文件夹 {folder_id} 的父文件夹 {parent_id} 不存在")
                    root_folders.append(folder_tree[folder_id])  # 当父文件夹缺失时，将其视为根文件夹

        # 步骤3: 添加文件到对应的文件夹
        for file_info in files:
            file_id = file_info['id']
            file_dict = {
                'type': 'file',
                'id': file_id,
                'name': file_info['name'],
                'folder_path': file_info['folder_path'],
                'file_type': file_info['file_type'],
                'create_time': file_info['create_time'].isoformat() if file_info['create_time'] else None,
                'create_user_name': file_info['create_user_name'],
                'last_modified_user_name': file_info['last_modified_user_name'],
                'last_modified_time': file_info['last_modified_time'].isoformat() if file_info['last_modified_time'] else None,
                'version_number': file_info['version_number'],
                'size': file_info['size'],
                'urn': file_info['urn'],
                'reviewState': file_info.get('reviewState', 'NotInReview'),  # 使用 get 方法，如果不存在则默认为 NotInReview
                'customAttributeValues': file_attrs.get(file_id, [])  # 添加文件的自定义属性值
            }

            # 找到文件所在的文件夹
            parent_folder_id = None
            for folder_id, folder_node in folder_tree.items():
                if folder_node['path'] == file_info['folder_path']:
                    parent_folder_id = folder_id
                    break

            if parent_folder_id and parent_folder_id in folder_tree:
                if 'children' not in folder_tree[parent_folder_id]:
                    folder_tree[parent_folder_id]['children'] = []
                folder_tree[parent_folder_id]['children'].append(file_dict)
            else:
                # 如果找不到父文件夹，添加到根文件夹
                logger.warning(f"文件 {file_info['id']} 的父文件夹不存在，添加到根文件夹")
                root_folders.append(file_dict)

        # 返回树结构（以根文件夹数组的形式）
        tree = {
            'root': root_folders,
            'metadata': {
                'total_folders': len(folder_tree),
                'total_files': len(files),
                'built_at': datetime.now(timezone.utc).isoformat()
            }
        }

        logger.info(f"树形结构构建完成: {len(folder_tree)} 文件夹, {len(files)} 文件")
        return tree

    def save_to_cache(self, project_id: str, tree: Dict, build_time_ms: float) -> bool:
        """
        保存树结构到缓存表

        Args:
            project_id: 项目ID
            tree: 树结构字典
            build_time_ms: 构建耗时（毫秒）

        Returns:
            是否成功保存
        """
        try:
            tree_json = json.dumps(tree, ensure_ascii=False)
            tree_size = len(tree_json.encode('utf-8'))

            sql = """
            INSERT INTO file_tree_cache (
                project_id, cached_tree, last_updated, cache_version,
                tree_size_bytes, total_folders, total_files, last_build_time_ms
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (project_id) DO UPDATE SET
                cached_tree = EXCLUDED.cached_tree,
                last_updated = EXCLUDED.last_updated,
                cache_version = file_tree_cache.cache_version + 1,
                tree_size_bytes = EXCLUDED.tree_size_bytes,
                total_folders = EXCLUDED.total_folders,
                total_files = EXCLUDED.total_files,
                last_build_time_ms = EXCLUDED.last_build_time_ms
            """

            self.cur.execute(sql, (
                project_id,
                tree_json,
                datetime.now(timezone.utc),
                1,
                tree_size,
                tree['metadata']['total_folders'],
                tree['metadata']['total_files'],
                build_time_ms
            ))

            self.conn.commit()
            logger.info(f"树结构已保存到缓存 (大小: {tree_size} 字节)")
            return True
        except Exception as e:
            self.conn.rollback()
            logger.error(f"保存缓存失败: {str(e)}")
            return False

    def get_cached_tree(self, project_id: str) -> Optional[Dict]:
        """
        从缓存表获取树结构

        Args:
            project_id: 项目ID

        Returns:
            树结构字典，如果缓存不存在或为空则返回 None
        """
        try:
            sql = "SELECT cached_tree FROM file_tree_cache WHERE project_id = %s"
            self.cur.execute(sql, (project_id,))
            result = self.cur.fetchone()

            if result and result['cached_tree']:
                logger.info("从缓存读取树结构成功")
                # cached_tree 可能已经是字典（如果由 psycopg2 自动转换）或字符串（JSON）
                cached_tree = result['cached_tree']
                if isinstance(cached_tree, dict):
                    return cached_tree
                else:
                    return json.loads(cached_tree)
            else:
                logger.info("缓存不存在或为空")
                return None
        except Exception as e:
            logger.error(f"读取缓存失败: {str(e)}")
            return None

    def invalidate_cache(self, project_id: str) -> bool:
        """
        清空缓存（写入时失效）

        Args:
            project_id: 项目ID

        Returns:
            是否成功清空
        """
        try:
            sql = """
            UPDATE file_tree_cache
            SET cached_tree = NULL, updated_at = %s
            WHERE project_id = %s
            """
            self.cur.execute(sql, (datetime.now(timezone.utc), project_id))
            self.conn.commit()
            logger.info(f"缓存已清空 (project_id: {project_id})")
            return True
        except Exception as e:
            self.conn.rollback()
            logger.error(f"清空缓存失败: {str(e)}")
            return False

    def build_and_cache_tree(self, project_id: str) -> Optional[Dict]:
        """
        构建树结构并保存到缓存（昂贵操作）

        Args:
            project_id: 项目ID

        Returns:
            构建好的树结构
        """
        logger.info(f"开始构建文件树 (project_id: {project_id})")
        start_time = time.time()

        try:
            # 1. 查询数据
            folders = self.query_folders(project_id)
            files = self.query_files(project_id)

            # 2. 查询自定义属性
            folder_attrs = self.query_folder_custom_attributes(project_id)
            file_attrs = self.query_custom_attributes(project_id)

            # 3. 构建树（包含自定义属性）
            tree = self.build_tree_from_paths(folders, files, folder_attrs, file_attrs)

            # 4. 保存到缓存
            build_time_ms = (time.time() - start_time) * 1000
            self.save_to_cache(project_id, tree, build_time_ms)

            logger.info(f"文件树构建完成 (耗时: {build_time_ms:.2f}ms)")
            return tree
        except Exception as e:
            logger.error(f"构建文件树失败: {str(e)}")
            return None


# ============================================================================
# 导出函数 - 供Flask API使用
# ============================================================================

def get_file_tree(project_id: str, db_params: Dict[str, str], force_refresh: bool = False) -> Tuple[Optional[Dict], bool]:
    """
    获取文件树（优先使用缓存）

    Args:
        project_id: 项目ID
        db_params: 数据库连接参数
        force_refresh: 是否强制刷新缓存

    Returns:
        (tree_dict, from_cache) - 树结构和是否来自缓存
    """
    builder = FileTreeBuilder(db_params)

    if not builder.connect():
        return None, False

    try:
        # 如果不强制刷新，先检查缓存
        if not force_refresh:
            cached_tree = builder.get_cached_tree(project_id)
            if cached_tree is not None:
                logger.info("缓存命中")
                return cached_tree, True

        # 缓存未命中，构建新的树
        logger.info("缓存未命中，开始构建新树")
        tree = builder.build_and_cache_tree(project_id)
        return tree, False
    finally:
        builder.disconnect()


def invalidate_file_tree_cache(project_id: str, db_params: Dict[str, str]) -> bool:
    """
    清空文件树缓存

    Args:
        project_id: 项目ID
        db_params: 数据库连接参数

    Returns:
        是否成功清空
    """
    builder = FileTreeBuilder(db_params)

    if not builder.connect():
        return False

    try:
        return builder.invalidate_cache(project_id)
    finally:
        builder.disconnect()
