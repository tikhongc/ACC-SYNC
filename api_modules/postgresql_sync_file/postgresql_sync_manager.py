# -*- coding: utf-8 -*-
"""
优化的PostgreSQL同步管理器
基于五层优化策略，支持智能跳过、批量操作、并发处理
"""

import asyncio
import time
import uuid
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import gc
import pytz

from database_sql.optimized_data_access import get_optimized_postgresql_dal
from database.data_sync_strategy import DataTransformer

logger = logging.getLogger(__name__)

# 中国时区常量
CHINA_TZ = pytz.timezone('Asia/Shanghai')

class OptimizedPostgreSQLSyncManager:
    """优化的PostgreSQL同步管理器"""
    
    def __init__(self, batch_size: int = 100, api_delay: float = 0.02, max_workers: int = 8, memory_threshold_mb: int = 1024):
        self.batch_size = batch_size
        self.api_delay = api_delay
        self.max_workers = max_workers
        self.memory_threshold_mb = memory_threshold_mb
        
        # 性能统计
        self.stats = {
            'api_calls': 0,
            'api_calls_saved': 0,
            'smart_skips': 0,
            'batch_operations': 0,
            'concurrent_operations': 0,
            'memory_peak_mb': 0,
            'processing_time': 0
        }
        
        # 数据转换器
        self.converter = DataTransformer()
        
        # 内存管理 (已在__init__中設置)
        
        # 并发控制
        self.api_semaphore = asyncio.Semaphore(8)
        self.db_semaphore = asyncio.Semaphore(15)
        
        # 统一使用V2架构
        pass
    
    # ============================================================================
    # 🌏 时区转换工具函数
    # ============================================================================
    
    def _convert_to_china_timezone(self, dt: datetime) -> datetime:
        """
        将datetime转换为中国时区
        
        Args:
            dt: 输入的datetime对象
            
        Returns:
            转换为中国时区的datetime对象
        """
        if not dt:
            return dt
            
        try:
            # 如果是naive datetime，假设为UTC
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            
            # 转换为中国时区
            china_dt = dt.astimezone(CHINA_TZ)
            return china_dt
            
        except Exception as e:
            logger.warning(f"时区转换失败: {dt}, 错误: {e}")
            return dt
    
    def _parse_datetime_to_china(self, datetime_str) -> Optional[datetime]:
        """
        解析datetime字符串并转换为中国时区
        
        Args:
            datetime_str: 时间字符串或datetime对象
            
        Returns:
            转换为中国时区的datetime对象
        """
        # 先使用原有的解析方法
        parsed_dt = self._parse_datetime(datetime_str)
        
        if parsed_dt:
            # 转换为中国时区
            return self._convert_to_china_timezone(parsed_dt)
        
        return None
    
    def _batch_convert_timestamps_to_china(self, data_dict: Dict[str, Any], 
                                         timestamp_fields: List[str]) -> Dict[str, Any]:
        """
        批量转换数据字典中的时间戳字段为中国时区
        
        Args:
            data_dict: 包含时间戳的数据字典
            timestamp_fields: 需要转换的时间戳字段列表
            
        Returns:
            转换后的数据字典
        """
        converted_dict = data_dict.copy()
        
        for field in timestamp_fields:
            if field in converted_dict and converted_dict[field]:
                # 如果是字符串，先解析再转换
                if isinstance(converted_dict[field], str):
                    converted_dict[field] = self._parse_datetime_to_china(converted_dict[field])
                # 如果是datetime对象，直接转换
                elif isinstance(converted_dict[field], datetime):
                    converted_dict[field] = self._convert_to_china_timezone(converted_dict[field])
        
        return converted_dict
        
    # ============================================================================
    # 🚀 Layer 1: 智能分支跳过优化
    # ============================================================================
    
    async def _smart_branch_filtering(self, project_id: str, last_sync_time: datetime, 
                                    headers: dict) -> List[Dict[str, Any]]:
        """智能分支过滤 - 核心优化，包含顶层rollup检查"""
        
        logger.info("🔍 开始智能分支过滤...")
        start_time = time.time()
        
        try:
            dal = await get_optimized_postgresql_dal()
            
            # 🚀 CRITICAL OPTIMIZATION: 顶层rollup时间检查
            # 这是最重要的优化 - 可以跳过整个项目
            top_level_check = await self._check_project_top_level_rollup(project_id, last_sync_time, dal)
            
            if top_level_check.get('can_skip_entire_project'):
                logger.info("🚀 TOP-LEVEL ROLLUP OPTIMIZATION: Entire project can be skipped!")
                logger.info(f"   Max rollup time: {top_level_check.get('max_rollup_time')}")
                logger.info(f"   Last sync time: {top_level_check.get('last_sync_time')}")
                logger.info(f"   Skip efficiency: {top_level_check.get('skip_efficiency_percentage', 0):.1f}%")
                
                self.stats['smart_skips'] += top_level_check.get('total_top_level_folders', 1)
                self.stats['api_calls_saved'] += top_level_check.get('total_top_level_folders', 1) * 10  # 估算节省的API调用
                self.stats['top_level_rollup_skips'] = 1
                
                return []  # 整个项目都可以跳过
            
            logger.info(f"🔍 Top-level check: {top_level_check.get('folders_with_changes', 0)} folders need checking")
            
            # 🔑 第二步：获取可能有变化的文件夹（现在只检查有变化的顶层文件夹）
            changed_folders = await dal.get_folders_for_smart_skip_check(project_id, last_sync_time)
            
            if not changed_folders:
                logger.info("✅ 智能跳过：没有发现变化的文件夹")
                self.stats['smart_skips'] += 1
                return []
            
            # 🔑 第三步：递归检查文件夹树，应用rollup时间优化
            filtered_items = []
            
            for folder in changed_folders:
                # 检查rollup时间
                rollup_time = self._parse_datetime(folder.get('last_modified_time_rollup'))
                
                if rollup_time and rollup_time <= last_sync_time:
                    # 🚀 智能跳过：整个分支无变化
                    logger.debug(f"智能跳过分支: {folder.get('name')} (rollup: {rollup_time} <= sync: {last_sync_time})")
                    self.stats['smart_skips'] += 1
                    self.stats['api_calls_saved'] += folder.get('object_count', 1) * 2  # 估算节省的API调用
                    continue
                
                # 需要进一步检查的文件夹
                filtered_items.append(folder)
                logger.debug(f"分支有变化，继续检查: {folder.get('name')} (rollup: {rollup_time} > sync: {last_sync_time})")
            
            processing_time = time.time() - start_time
            self.stats['processing_time'] += processing_time
            
            skip_efficiency = (self.stats['smart_skips'] / max(len(changed_folders), 1)) * 100
            logger.info(f"🎯 智能分支过滤完成: {len(filtered_items)}/{len(changed_folders)} 需要处理, 跳过效率: {skip_efficiency:.1f}%")
            
            return filtered_items
            
        except Exception as e:
            logger.error(f"智能分支过滤失败: {e}")
            return []
    
    async def _check_project_top_level_rollup(self, project_id: str, last_sync_time: datetime, 
                                         dal) -> Dict[str, Any]:
        """
        🚀 CRITICAL OPTIMIZATION: 检查项目顶层rollup时间
        这是最重要的优化 - 可以在不调用任何API的情况下判断整个项目是否需要同步
        """
        try:
            async with dal.get_connection() as conn:
                query = """
                SELECT 
                    MAX(last_modified_time_rollup) as max_rollup_time,
                    COUNT(*) as total_top_level_folders,
                    COUNT(CASE WHEN last_modified_time_rollup > $2 THEN 1 END) as folders_with_changes,
                    AVG(object_count) as avg_objects_per_folder
                FROM folders 
                WHERE project_id = $1 
                  AND depth = 0
                  AND last_modified_time_rollup IS NOT NULL
                """
                
                result = await conn.fetchrow(query, project_id, last_sync_time)
                
                if not result or not result['max_rollup_time']:
                    return {
                        'can_skip_entire_project': False,
                        'reason': 'No top-level folders found or no rollup time available',
                        'recommendation': 'Perform incremental sync with folder-level checks'
                    }
                
                max_rollup_time = result['max_rollup_time']
                total_folders = result['total_top_level_folders']
                folders_with_changes = result['folders_with_changes']
                avg_objects = result['avg_objects_per_folder'] or 0
                
                # 🎯 关键判断：如果最大rollup时间 <= 上次同步时间，整个项目都可以跳过
                can_skip_entire_project = max_rollup_time <= last_sync_time
                
                skip_efficiency = 0.0
                if total_folders > 0:
                    skip_efficiency = ((total_folders - folders_with_changes) / total_folders) * 100
                
                # 估算节省的API调用次数
                estimated_api_calls_saved = 0
                if can_skip_entire_project:
                    # 每个文件夹至少节省2个API调用（获取内容 + 获取自定义属性）
                    estimated_api_calls_saved = int(total_folders * avg_objects * 2)
                
                return {
                    'can_skip_entire_project': can_skip_entire_project,
                    'max_rollup_time': max_rollup_time.isoformat(),
                    'last_sync_time': last_sync_time.isoformat(),
                    'total_top_level_folders': total_folders,
                    'folders_with_changes': folders_with_changes,
                    'skip_efficiency_percentage': skip_efficiency,
                    'estimated_api_calls_saved': estimated_api_calls_saved,
                    'recommendation': 'Skip entire project' if can_skip_entire_project else 'Perform incremental sync',
                    'optimization_level': 'project_level' if can_skip_entire_project else 'folder_level'
                }
                
        except Exception as e:
            logger.error(f"Top-level rollup check failed: {e}")
            return {
                'can_skip_entire_project': False,
                'reason': f'Check failed: {str(e)}',
                'recommendation': 'Perform incremental sync with error handling'
            }
    
    # ============================================================================
    # 🚀 Layer 2.5: 文件级Timestamp比对优化
    # ============================================================================
    
    async def _identify_files_needing_updates(self, changed_files: List[Dict], project_id: str, 
                                            last_sync_time: datetime, dal) -> List[Dict]:
        """
        🎯 关键优化：文件级timestamp比对
        识别需要更新自定义属性和版本的文件，记录文件ID用于批量API调用
        """
        try:
            files_needing_updates = []
            
            logger.info(f"🔍 开始文件级timestamp比对: {len(changed_files)} 个文件")
            
            for file_data in changed_files:
                file_id = file_data.get('id')
                if not file_id:
                    continue
                
                # 获取文件的lastModifiedTime
                attributes = file_data.get('attributes', {})
                file_modified_time_str = attributes.get('lastModifiedTime')
                
                if not file_modified_time_str:
                    # 没有修改时间，保守策略：需要更新
                    files_needing_updates.append({
                        'file_id': file_id,
                        'file_data': file_data,
                        'reason': 'no_modified_time',
                        'needs_custom_attributes': True,
                        'needs_version_update': True
                    })
                    continue
                
                # 解析文件修改时间
                file_modified_time = self._parse_datetime(file_modified_time_str)
                
                if not file_modified_time:
                    # 解析失败，保守策略：需要更新
                    files_needing_updates.append({
                        'file_id': file_id,
                        'file_data': file_data,
                        'reason': 'parse_time_failed',
                        'needs_custom_attributes': True,
                        'needs_version_update': True
                    })
                    continue
                
                # 🎯 关键比较：文件修改时间 vs 上次同步时间
                if self._is_file_modified_since_sync(file_modified_time, last_sync_time):
                    # 文件有更新，需要检查自定义属性和版本
                    files_needing_updates.append({
                        'file_id': file_id,
                        'file_data': file_data,
                        'reason': 'file_modified',
                        'file_modified_time': file_modified_time.isoformat(),
                        'last_sync_time': last_sync_time.isoformat(),
                        'needs_custom_attributes': True,
                        'needs_version_update': True
                    })
                    
                    logger.debug(f"📄 文件需要更新: {attributes.get('displayName', file_id)} "
                               f"(修改时间: {file_modified_time} > 同步时间: {last_sync_time})")
                else:
                    # 文件无变化，跳过
                    logger.debug(f"⏭️ 文件跳过: {attributes.get('displayName', file_id)} "
                               f"(修改时间: {file_modified_time} <= 同步时间: {last_sync_time})")
            
            # 统计
            self.stats['files_analyzed'] = len(changed_files)
            self.stats['files_needing_updates'] = len(files_needing_updates)
            self.stats['files_skipped'] = len(changed_files) - len(files_needing_updates)
            
            skip_efficiency = (self.stats['files_skipped'] / max(len(changed_files), 1)) * 100
            
            logger.info(f"🎯 文件级比对完成: {len(files_needing_updates)}/{len(changed_files)} 需要更新, "
                       f"跳过效率: {skip_efficiency:.1f}%")
            
            return files_needing_updates
            
        except Exception as e:
            logger.error(f"文件级timestamp比对失败: {e}")
            # 失败时返回所有文件（保守策略）
            return [{'file_id': f.get('id'), 'file_data': f, 'reason': 'comparison_failed', 
                    'needs_custom_attributes': True, 'needs_version_update': True} 
                   for f in changed_files if f.get('id')]
    
    def _is_file_modified_since_sync(self, file_modified_time: datetime, last_sync_time: datetime) -> bool:
        """检查文件是否在上次同步后被修改"""
        try:
            if not file_modified_time or not last_sync_time:
                return True  # 保守策略
            
            # 处理时区问题
            if file_modified_time.tzinfo is None:
                file_modified_time = file_modified_time.replace(tzinfo=timezone.utc)
            if last_sync_time.tzinfo is None:
                last_sync_time = last_sync_time.replace(tzinfo=timezone.utc)
            
            return file_modified_time > last_sync_time
            
        except Exception as e:
            logger.warning(f"文件时间比较失败: {e}")
            return True  # 保守策略
    
    def _parse_datetime(self, datetime_str):
        """解析datetime字符串，支持多种格式"""
        if not datetime_str:
            return None
        
        # 如果已经是datetime对象，直接返回
        if isinstance(datetime_str, datetime):
            return datetime_str
        
        try:
            # 只处理字符串类型
            if not isinstance(datetime_str, str):
                logger.warning(f"Expected string for datetime parsing, got {type(datetime_str)}: {datetime_str}")
                return None
            
            # 处理ACC API返回的特殊格式：2025-10-20T02:32:52.0000000Z
            if 'T' in datetime_str:
                # 处理Z结尾的UTC时间
                if datetime_str.endswith('Z'):
                    # 处理超过6位的小数秒（Python的%f只支持6位）
                    if '.' in datetime_str:
                        date_part, time_part = datetime_str.split('T')
                        if '.' in time_part:
                            time_base, microseconds_z = time_part.split('.')
                            microseconds = microseconds_z.rstrip('Z')
                            # 截断或填充到6位
                            if len(microseconds) > 6:
                                microseconds = microseconds[:6]
                            else:
                                microseconds = microseconds.ljust(6, '0')
                            datetime_str = f"{date_part}T{time_base}.{microseconds}Z"
                    
                    # 使用fromisoformat处理
                    return datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
                else:
                    return datetime.fromisoformat(datetime_str)
            
            # 尝试其他格式
            formats = [
                '%Y-%m-%dT%H:%M:%S.%fZ',
                '%Y-%m-%dT%H:%M:%SZ',
                '%Y-%m-%dT%H:%M:%S.%f',
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d'
            ]
            
            for fmt in formats:
                try:
                    dt = datetime.strptime(datetime_str, fmt)
                    if 'Z' in fmt or 'T' in fmt:
                        dt = dt.replace(tzinfo=timezone.utc)
                    return dt
                except ValueError:
                    continue
            
            logger.warning(f"Cannot parse datetime: {datetime_str}")
            return None
            
        except Exception as e:
            logger.warning(f"Datetime parsing failed: {datetime_str}, error: {e}")
            return None

    # ============================================================================
    # 🚀 Layer 2: 批量API调用优化
    # ============================================================================
    
    async def _batch_api_operations(self, project_id: str, folders_to_check: List[Dict[str, Any]], 
                                  headers: dict) -> Tuple[List[Dict], List[Dict]]:
        """批量API操作优化"""
        
        logger.info(f"📡 开始批量API操作: {len(folders_to_check)} 个文件夹")
        start_time = time.time()
        
        try:
            dal = await get_optimized_postgresql_dal()
            last_sync_time = await dal.get_project_last_sync_time(project_id)
            
            # 🔑 批量获取文件夹内容
            folder_ids = [folder['id'] for folder in folders_to_check]
            
            # 分批处理，避免API限制
            batch_size = min(20, len(folder_ids))  # API批量限制
            contents_batches = []
            
            # 使用現有的異步方法逐個獲取文件夾內容
            try:
                import aiohttp
                
                async with aiohttp.ClientSession() as session:
                    contents_batches = []
                    
                    # 分批處理以避免過多並發
                    for i in range(0, len(folder_ids), batch_size):
                        batch_ids = folder_ids[i:i + batch_size]
                        
                        # 並發獲取當前批次的文件夾內容
                        tasks = []
                        for folder_id in batch_ids:
                            task = self._get_folder_contents_async(session, project_id, folder_id, headers)
                            tasks.append((folder_id, task))
                        
                        # 等待當前批次完成
                        batch_results = {}
                        for folder_id, task in tasks:
                            try:
                                content = await task
                                batch_results[folder_id] = content
                            except Exception as e:
                                logger.warning(f"Failed to get contents for folder {folder_id}: {e}")
                                batch_results[folder_id] = {}
                        
                        contents_batches.append(batch_results)
                        
                        # API節流
                        if i + batch_size < len(folder_ids):
                            await asyncio.sleep(self.api_delay)
                            
            except ImportError:
                logger.warning("aiohttp not available, skipping batch processing")
                contents_batches = []
            
            # 🔑 解析批量结果，提取变化的文件和文件夹
            changed_folders = []
            changed_files = []
            
            for batch_contents in contents_batches:
                for folder_id, contents_data in batch_contents.items():
                    if not contents_data or not contents_data.get('data'):
                        continue
                    
                    # 找到对应的文件夹信息
                    folder_info = next((f for f in folders_to_check if f['id'] == folder_id), None)
                    if not folder_info:
                        continue
                    
                    # 处理文件夹内容
                    for item in contents_data['data']:
                        item_type = item.get('type')
                        
                        if item_type == 'folders':
                            # 子文件夹 - 检查rollup时间
                            subfolder_rollup = self._parse_datetime(
                                item.get('attributes', {}).get('lastModifiedTimeRollup')
                            )
                            if not subfolder_rollup or (last_sync_time and subfolder_rollup > last_sync_time):
                                changed_folders.append(item)
                            else:
                                self.stats['smart_skips'] += 1
                        
                        elif item_type in ['items', 'files']:
                            # 文件 - 检查修改时间
                            file_modified = self._parse_datetime(
                                item.get('attributes', {}).get('lastModifiedTime')
                            )
                            if file_modified and last_sync_time and file_modified > last_sync_time:
                                changed_files.append(item)
            
            api_time = time.time() - start_time
            self.stats['processing_time'] += api_time
            
            logger.info(f"✅ 批量API操作完成: {len(changed_folders)} 文件夹, {len(changed_files)} 文件, 耗时: {api_time:.2f}s")
            
            return changed_folders, changed_files
            
        except Exception as e:
            logger.error(f"批量API操作失败: {e}")
            return [], []
    
    async def _batch_get_file_versions_and_custom_attrs(self, project_id: str, 
                                                      changed_files: List[Dict[str, Any]], 
                                                      headers: dict) -> List[Dict[str, Any]]:
        """批量获取文件版本和自定义属性"""
        
        if not changed_files:
            return []
        
        logger.info(f"Batch retrieving file details: {len(changed_files)} files")
        
        try:
            # 🔑 批量获取文件版本详细信息（参考MongoDB实现）
            file_ids = [file_data['id'] for file_data in changed_files]
            
            # 分批处理版本信息获取
            batch_size = 10  # 版本API并发限制更严格
            all_file_metadata = []
            
            # 并发获取版本信息
            try:
                import aiohttp
                
                async with aiohttp.ClientSession() as session:
                    # 分批处理文件
                    for i in range(0, len(changed_files), batch_size):
                        batch_files = changed_files[i:i + batch_size]
                        
                        # 并发获取当前批次的版本信息
                        tasks = []
                        for file_data in batch_files:
                            file_id = file_data.get('id')
                            if file_id:
                                task = self._get_file_versions_async(session, project_id, file_id, headers)
                                tasks.append((file_data, task))
                        
                        # 等待当前批次完成
                        for file_data, task in tasks:
                            try:
                                versions_info = await task
                                # 将版本信息合并到文件数据中
                                file_data['versions_info'] = versions_info
                                all_file_metadata.append(file_data)
                                
                                self.stats['api_calls'] += 1
                            except Exception as e:
                                logger.warning(f"获取文件版本失败 {file_data.get('id')}: {e}")
                                # 即使版本获取失败，也保留基本文件信息
                                file_data['versions_info'] = []
                                all_file_metadata.append(file_data)
                        
                        # API节流
                        if i + batch_size < len(changed_files):
                            await asyncio.sleep(self.api_delay)
                        
                        self.stats['batch_operations'] += 1
                        
            except ImportError:
                logger.warning("aiohttp not available, using basic file metadata")
                all_file_metadata = changed_files
            
            # 🔑 批量获取自定义属性和存储信息 (Custom Attributes API)
            version_urns = []
            file_to_version_map = {}
            
            for file_metadata in all_file_metadata:
                # 从versions_info中获取版本URN
                versions_info = file_metadata.get('versions_info', [])
                if versions_info:
                    version_urn = versions_info[0].get('id')  # 使用最新版本
                    if version_urn:
                        version_urns.append(version_urn)
                        file_to_version_map[version_urn] = file_metadata.get('id')
            
            custom_attributes_data = []
            if version_urns:
                # 分批获取自定义属性 (API限制50个)
                for i in range(0, len(version_urns), batch_size):
                    batch_urns = version_urns[i:i + batch_size]
                    
                    async with self.api_semaphore:
                        # 调用实际的Custom Attributes API
                        custom_attrs_batch = await self._call_custom_attributes_api(project_id, batch_urns, headers)
                        
                        custom_attributes_data.extend(custom_attrs_batch)
                        self.stats['api_calls'] += 1
                        self.stats['batch_operations'] += 1
            
            # 合并文件元数据、版本信息和自定义属性
            enriched_files = []
            for file_metadata in all_file_metadata:
                # 查找对应的自定义属性和存储信息
                file_id = file_metadata.get('id')
                versions_info = file_metadata.get('versions_info', [])
                
                # 从自定义属性API获取额外信息
                custom_attrs_info = None
                if versions_info:
                    version_urn = versions_info[0].get('id')
                    custom_attrs_info = next(
                        (attr for attr in custom_attributes_data if attr.get('urn') == version_urn),
                        None
                    )
                
                # 更新版本信息中的storageUrn
                if custom_attrs_info and versions_info:
                    storage_urn = custom_attrs_info.get('storageUrn')
                    if storage_urn:
                        versions_info[0]['detailed_attributes']['storageUrn'] = storage_urn
                
                # 添加自定义属性
                file_metadata['custom_attributes'] = custom_attrs_info.get('customAttributes', []) if custom_attrs_info else []
                enriched_files.append(file_metadata)
            
            logger.info(f"✅ 文件详细信息获取完成: {len(enriched_files)} 个文件")
            return enriched_files
            
        except Exception as e:
            logger.error(f"批量获取文件信息失败: {e}")
            return changed_files  # 返回基本信息
    
    # ============================================================================
    # 🚀 Layer 3: 数据库批量操作优化
    # ============================================================================
    
    async def _batch_database_operations(self, project_id: str, 
                                       changed_folders: List[Dict[str, Any]], 
                                       changed_files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量数据库操作优化"""
        
        logger.info(f"💾 开始批量数据库操作: {len(changed_folders)} 文件夹, {len(changed_files)} 文件")
        start_time = time.time()
        
        try:
            dal = await get_optimized_postgresql_dal()
            results = {
                'folders_synced': 0,
                'files_synced': 0,
                'custom_attrs_synced': 0,
                'errors': []
            }
            
            # 🔑 第一阶段：批量处理文件夹
            if changed_folders:
                async with self.db_semaphore:
                    folders_data = []
                    for folder in changed_folders:
                        folder_record = self.converter.transform_folder_data(
                            folder, project_id, None, "", 0
                        )
                        folders_data.append(folder_record)
                    
                    folder_result = await dal.batch_upsert_folders(folders_data)
                    results['folders_synced'] = folder_result.get('upserted', 0)
                    results['errors'].extend(folder_result.get('errors', []))
                    
                    self.stats['batch_operations'] += 1
            
            # 🔑 第二阶段：批量处理文件
            if changed_files:
                async with self.db_semaphore:
                    files_data = []
                    versions_data = []
                    custom_attrs_definitions = []
                    custom_attrs_values = []
                    
                    for file_data in changed_files:
                        # 转换文件数据
                        file_record = self.converter.transform_file_data(
                            file_data, project_id, None, "", 0
                        )
                        files_data.append(file_record)
                        
                        # 🔑 处理文件版本信息
                        tip_version_urn = file_record.get('tip_version_urn')
                        logger.info(f"DEBUG: File {file_record.get('name')} tip_version_urn: {tip_version_urn}")
                        if tip_version_urn:
                            logger.info(f"DEBUG: Creating version record for {file_record.get('name')}")
                            version_record = {
                                'id': tip_version_urn,
                                'project_id': project_id,
                                'file_id': file_record['id'],
                                'version_number': 1,  # 默认为1，实际应从API获取
                                'version_type': 'tip',
                                'create_time': file_record.get('create_time'),
                                'create_user_id': file_record.get('create_user_id'),
                                'create_user_name': file_record.get('create_user_name'),
                                'file_size': file_record.get('file_size', 0),
                                'storage_urn': file_record.get('storage_location'),
                                'mime_type': file_record.get('mime_type'),
                                'metadata': {
                                    'is_tip_version': True,
                                    'original_file_data': file_data
                                }
                            }
                            versions_data.append(version_record)
                            logger.info(f"DEBUG: Added version record, total versions_data: {len(versions_data)}")
                        else:
                            logger.info(f"DEBUG: No tip_version_urn for file {file_record.get('name')}")
                        
                        # 🔑 提取自定义属性 (分离表设计)
                        custom_attrs = file_data.get('custom_attributes', [])
                        for attr in custom_attrs:
                            # 属性定义
                            attr_def = {
                                'attr_id': attr.get('id'),
                                'project_id': project_id,
                                'name': attr.get('name'),
                                'type': attr.get('type'),
                                'array_values': attr.get('arrayValues', [])
                            }
                            custom_attrs_definitions.append(attr_def)
                            
                            # 属性值
                            attr_value = {
                                'file_id': file_data.get('id'),
                                'attr_id': attr.get('id'),
                                'project_id': project_id,
                                'value': attr.get('value'),
                                'value_date': self._parse_date_value(attr) if attr.get('type') == 'date' else None,
                                'value_number': self._parse_number_value(attr) if attr.get('type') == 'number' else None,
                                'value_boolean': self._parse_boolean_value(attr) if attr.get('type') == 'boolean' else None
                            }
                            custom_attrs_values.append(attr_value)
                    
                    # 批量插入文件
                    file_result = await dal.batch_upsert_files(files_data)
                    results['files_synced'] = file_result.get('upserted', 0)
                    results['errors'].extend(file_result.get('errors', []))
                    
                    # 🔑 批量插入文件版本
                    logger.info(f"DEBUG: versions_data length: {len(versions_data)}")
                    if versions_data:
                        try:
                            logger.info(f"DEBUG: Creating {len(versions_data)} file versions...")
                            versions_result = await dal.batch_upsert_file_versions(versions_data)
                            logger.info(f"✅ 文件版本同步完成: {versions_result.get('upserted', 0)} 个版本")
                        except Exception as e:
                            logger.error(f"文件版本同步失败: {e}")
                            results['errors'].append(f"File versions sync failed: {e}")
                    else:
                        logger.info("DEBUG: No versions_data to process")
                    
                    # 🔑 第三阶段：批量处理自定义属性 (分离表)
                    if custom_attrs_definitions:
                        # 去重属性定义
                        unique_definitions = self._deduplicate_definitions(custom_attrs_definitions)
                        def_result = await dal.batch_upsert_custom_attribute_definitions(unique_definitions)
                        
                        # 批量插入属性值
                        if custom_attrs_values:
                            value_result = await dal.batch_upsert_custom_attribute_values(custom_attrs_values)
                            results['custom_attrs_synced'] = value_result.get('upserted', 0)
                            results['errors'].extend(value_result.get('errors', []))
                    
                    self.stats['batch_operations'] += 2  # 文件 + 自定义属性
            
            db_time = time.time() - start_time
            self.stats['processing_time'] += db_time
            
            logger.info(f"✅ 批量数据库操作完成: 耗时 {db_time:.2f}s")
            logger.info(f"   - 文件夹: {results['folders_synced']}")
            logger.info(f"   - 文件: {results['files_synced']}")
            logger.info(f"   - 自定义属性: {results['custom_attrs_synced']}")
            
            return results
            
        except Exception as e:
            logger.error(f"批量数据库操作失败: {e}")
            return {'folders_synced': 0, 'files_synced': 0, 'custom_attrs_synced': 0, 'errors': [str(e)]}
    
    # ============================================================================
    # 🚀 Layer 4: 并发处理优化
    # ============================================================================
    
    async def _concurrent_processing_with_memory_management(self, project_id: str, 
                                                          sync_items: List[Dict[str, Any]], 
                                                          headers: dict) -> Dict[str, Any]:
        """并发处理与内存管理"""
        
        logger.info(f"⚡ 开始并发处理: {len(sync_items)} 个项目")
        start_time = time.time()
        
        try:
            # 🔑 智能任务分组
            task_groups = self._create_intelligent_task_groups(sync_items)
            
            results = {
                'high_priority': {'count': 0, 'errors': []},
                'medium_priority': {'count': 0, 'errors': []},
                'low_priority': {'count': 0, 'errors': []},
                'total_processed': 0
            }
            
            # 🔑 分阶段并发执行
            # 阶段1：高优先级任务（最大并发）
            if task_groups['high_priority']:
                logger.info(f"🔥 处理高优先级任务: {len(task_groups['high_priority'])} 个")
                high_results = await self._process_priority_group(
                    project_id, task_groups['high_priority'], headers, max_concurrency=self.max_workers
                )
                results['high_priority'] = high_results
                results['total_processed'] += high_results['count']
                
                # 内存清理
                await self._memory_cleanup()
            
            # 阶段2：中优先级任务（中等并发）
            if task_groups['medium_priority']:
                logger.info(f"🔶 处理中优先级任务: {len(task_groups['medium_priority'])} 个")
                medium_results = await self._process_priority_group(
                    project_id, task_groups['medium_priority'], headers, max_concurrency=self.max_workers // 2
                )
                results['medium_priority'] = medium_results
                results['total_processed'] += medium_results['count']
                
                # 内存清理
                await self._memory_cleanup()
            
            # 阶段3：低优先级任务（低并发）
            if task_groups['low_priority']:
                logger.info(f"🔷 处理低优先级任务: {len(task_groups['low_priority'])} 个")
                low_results = await self._process_priority_group(
                    project_id, task_groups['low_priority'], headers, max_concurrency=self.max_workers // 4
                )
                results['low_priority'] = low_results
                results['total_processed'] += low_results['count']
            
            concurrent_time = time.time() - start_time
            self.stats['processing_time'] += concurrent_time
            
            logger.info(f"✅ 并发处理完成: {results['total_processed']} 个项目, 耗时: {concurrent_time:.2f}s")
            
            return results
            
        except Exception as e:
            logger.error(f"并发处理失败: {e}")
            return {'total_processed': 0, 'errors': [str(e)]}
    
    def _create_intelligent_task_groups(self, items: List[Dict[str, Any]]) -> Dict[str, List]:
        """智能任务分组"""
        
        groups = {
            'high_priority': [],    # 高优先级：小文件、重要文件夹
            'medium_priority': [],  # 中优先级：普通文件
            'low_priority': []      # 低优先级：大文件、复杂属性
        }
        
        for item in items:
            priority = self._calculate_item_priority(item)
            groups[priority].append(item)
        
        logger.info(f"📊 任务分组完成: 高优先级 {len(groups['high_priority'])}, "
                   f"中优先级 {len(groups['medium_priority'])}, 低优先级 {len(groups['low_priority'])}")
        
        return groups
    
    def _calculate_item_priority(self, item: Dict[str, Any]) -> str:
        """计算项目优先级"""
        
        # 基础优先级
        if item.get('type') == 'folders':
            base_priority = 'high_priority'
        else:
            base_priority = 'medium_priority'
        
        # 根据文件大小调整
        file_size = item.get('attributes', {}).get('fileSize', 0)
        if file_size > 50 * 1024 * 1024:  # 50MB以上
            return 'low_priority'
        
        # 根据自定义属性数量调整
        custom_attrs_count = len(item.get('custom_attributes', []))
        if custom_attrs_count > 10:
            return 'low_priority'
        
        # 根据修改时间调整（最近修改的优先）
        last_modified = item.get('attributes', {}).get('lastModifiedTime')
        if last_modified:
            modified_time = self._parse_datetime(last_modified)
            if modified_time and (datetime.utcnow() - modified_time).days < 1:
                return 'high_priority'
        
        return base_priority
    
    async def _process_priority_group(self, project_id: str, items: List[Dict[str, Any]], 
                                    headers: dict, max_concurrency: int) -> Dict[str, Any]:
        """处理优先级组"""
        
        semaphore = asyncio.Semaphore(max_concurrency)
        
        async def process_item_with_semaphore(item):
            async with semaphore:
                return await self._process_single_item_optimized(project_id, item, headers)
        
        # 创建并发任务
        tasks = [process_item_with_semaphore(item) for item in items]
        
        # 执行并收集结果
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 统计结果
        success_count = 0
        errors = []
        
        for result in results:
            if isinstance(result, Exception):
                errors.append(str(result))
            else:
                success_count += 1
        
        self.stats['concurrent_operations'] += len(tasks)
        
        return {'count': success_count, 'errors': errors}
    
    async def _process_single_item_optimized(self, project_id: str, item: Dict[str, Any], 
                                           headers: dict) -> bool:
        """优化的单项目处理"""
        
        try:
            # 这里可以添加单项目的具体处理逻辑
            # 例如：获取详细信息、转换数据、存储到数据库等
            
            # 模拟处理时间
            await asyncio.sleep(0.01)
            
            return True
            
        except Exception as e:
            logger.error(f"单项目处理失败: {e}")
            raise
    
    # ============================================================================
    # 🚀 Layer 5: 内存管理与性能监控
    # ============================================================================
    
    async def _memory_cleanup(self):
        """内存清理"""
        
        current_memory = self._get_memory_usage_mb()
        
        if current_memory > self.memory_threshold_mb * 0.8:
            logger.warning(f"内存使用过高: {current_memory}MB, 执行清理")
            
            # 强制垃圾回收
            gc.collect()
            
            # 等待内存释放
            await asyncio.sleep(0.1)
            
            new_memory = self._get_memory_usage_mb()
            logger.info(f"内存清理完成: {current_memory}MB -> {new_memory}MB")
        
        # 更新峰值内存使用
        self.stats['memory_peak_mb'] = max(self.stats['memory_peak_mb'], current_memory)
    
    def _get_memory_usage_mb(self) -> float:
        """获取当前内存使用量(MB)"""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024
        except ImportError:
            return 0.0
    
    def _calculate_optimization_efficiency(self) -> float:
        """计算优化效率"""
        try:
            total_operations = self.stats.get('concurrent_operations', 0) + self.stats.get('smart_skips', 0)
            smart_skips = self.stats.get('smart_skips', 0)
            
            if total_operations == 0:
                return 0.0
            
            # 计算跳过的比例作为优化效率
            efficiency = (smart_skips / total_operations) * 100
            return round(efficiency, 2)
            
        except Exception as e:
            logger.warning(f"计算优化效率失败: {str(e)}")
            return 0.0
    
    # ============================================================================
    # 🚀 主要同步方法
    # ============================================================================
    
    async def optimized_incremental_sync(self, project_id: str, max_depth: int = 10, 
                                       include_custom_attributes: bool = True, 
                                       task_uuid: str = None, headers: dict = None) -> Dict[str, Any]:
        """优化的增量同步 - 统一使用V2架构"""
        
        logger.info(f"🚀 开始优化增量同步: 项目 {project_id}")
        
        # 直接使用V2架构的增量同步
        return await self._optimized_incremental_sync_v2(project_id, max_depth, include_custom_attributes, task_uuid, headers)
            
    async def optimized_full_sync(self, project_id: str, max_depth: int = 10, 
                                include_custom_attributes: bool = True, 
                                task_uuid: str = None, headers: dict = None) -> Dict[str, Any]:
        """优化的全量同步 - 统一使用V2架构"""
        
        logger.info(f"🚀 开始优化全量同步: 项目 {project_id}")
            
        # 直接使用V2架构的全量同步
        return await self._optimized_full_sync_v2(project_id, max_depth, include_custom_attributes, task_uuid, headers)
    
    # ============================================================================
    # 辅助方法 - 异步API调用
    # ============================================================================
    
    async def _get_top_folders_async(self, project_id: str, headers: dict) -> dict:
        """异步获取项目顶级文件夹 - 使用正确的Hub-based API"""
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                # Step 1: Get hubs to find the hub containing this project
                hubs_url = "https://developer.api.autodesk.com/project/v1/hubs"
                
                async with session.get(hubs_url, headers=headers) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"Failed to get hubs: {response.status} - {error_text}")
                    
                    hubs_data = await response.json()
                    self.stats['api_calls'] += 1
                
                # Step 2: Find the hub containing our project
                hub_id = None
                for hub in hubs_data.get('data', []):
                    hub_id_candidate = hub.get('id')
                    
                    # Check if project exists in this hub
                    projects_url = f"https://developer.api.autodesk.com/project/v1/hubs/{hub_id_candidate}/projects"
                    async with session.get(projects_url, headers=headers) as proj_response:
                        if proj_response.status == 200:
                            projects_data = await proj_response.json()
                            self.stats['api_calls'] += 1
                            
                            for project in projects_data.get('data', []):
                                if project.get('id') == project_id:
                                    hub_id = hub_id_candidate
                                    break
                    
                    if hub_id:
                        break
                
                if not hub_id:
                    raise Exception(f"Project {project_id} not found in any accessible hub")
                
                # Step 3: Get top folders for the project
                top_folders_url = f"https://developer.api.autodesk.com/project/v1/hubs/{hub_id}/projects/{project_id}/topFolders"
                
                async with session.get(top_folders_url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.stats['api_calls'] += 1
                        return data
                    else:
                        error_text = await response.text()
                        raise Exception(f"Failed to get top folders: {response.status} - {error_text}")
                        
        except ImportError:
            # Fallback to synchronous requests if aiohttp not available
            import requests
            
            # Step 1: Get hubs
            hubs_url = "https://developer.api.autodesk.com/project/v1/hubs"
            response = requests.get(hubs_url, headers=headers)
            
            if response.status_code != 200:
                raise Exception(f"Failed to get hubs: {response.status_code} - {response.text}")
            
            hubs_data = response.json()
            self.stats['api_calls'] += 1
            
            # Step 2: Find hub containing project
            hub_id = None
            for hub in hubs_data.get('data', []):
                hub_id_candidate = hub.get('id')
                
                projects_url = f"https://developer.api.autodesk.com/project/v1/hubs/{hub_id_candidate}/projects"
                proj_response = requests.get(projects_url, headers=headers)
                
                if proj_response.status_code == 200:
                    projects_data = proj_response.json()
                    self.stats['api_calls'] += 1
                    
                    for project in projects_data.get('data', []):
                        if project.get('id') == project_id:
                            hub_id = hub_id_candidate
                            break
                
                if hub_id:
                    break
            
            if not hub_id:
                raise Exception(f"Project {project_id} not found in any accessible hub")
            
            # Step 3: Get top folders
            top_folders_url = f"https://developer.api.autodesk.com/project/v1/hubs/{hub_id}/projects/{project_id}/topFolders"
            response = requests.get(top_folders_url, headers=headers)
            
            if response.status_code == 200:
                self.stats['api_calls'] += 1
                return response.json()
            else:
                raise Exception(f"Failed to get top folders: {response.status_code} - {response.text}")
    
    async def _collect_all_items_recursive_async(self, project_id: str, top_folders: list,
                                               headers: dict, max_depth: int) -> Tuple[List, List]:
        """异步递归收集所有文件夹和文件"""
        all_folders = []
        all_files = []
        
        # BFS queue: (folder_data, depth, parent_path)
        queue = [(folder, 0, "") for folder in top_folders]
        
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                while queue and len(queue) > 0:
                    current_batch = queue[:self.batch_size]
                    queue = queue[self.batch_size:]
                    
                    # 并发获取当前批次的文件夹内容
                    tasks = []
                    for folder_data, depth, parent_path in current_batch:
                        if depth >= max_depth:
                            continue
                            
                        folder_id = folder_data.get('id')
                        if folder_id:
                            task = self._get_folder_contents_async(session, project_id, folder_id, headers)
                            tasks.append((folder_data, depth, parent_path, task))
                
                    # 处理当前批次的结果
                    for folder_data, depth, parent_path, task in tasks:
                        try:
                            contents = await task
                            all_folders.append(folder_data)
                            
                            # 处理文件夹内容
                            for item in contents.get('data', []):
                                item_type = item.get('type')
                                
                                if item_type == 'folders':
                                    # 子文件夹加入队列
                                    new_path = f"{parent_path}/{folder_data.get('attributes', {}).get('name', '')}"
                                    queue.append((item, depth + 1, new_path))
                                elif item_type in ['items', 'files']:
                                    # 文件直接添加
                                    all_files.append(item)
                                    
                        except Exception as e:
                            logger.warning(f"获取文件夹内容失败 {folder_data.get('id')}: {e}")
                    
                    # API节流
                    if queue:
                        await asyncio.sleep(self.api_delay)
                        
        except ImportError:
            logger.warning("aiohttp not available, using basic collection")
            # 简单的同步收集
            for folder in top_folders:
                all_folders.append(folder)
        
        logger.info(f"BFS收集完成: {len(all_folders)} 文件夹, {len(all_files)} 文件")
        return all_folders, all_files
    
    async def _get_folder_contents_async(self, session, project_id: str, folder_id: str, headers: dict) -> dict:
        """异步获取文件夹内容"""
        url = f"https://developer.api.autodesk.com/data/v1/projects/{project_id}/folders/{folder_id}/contents"
        
        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    self.stats['api_calls'] += 1
                    return data
                else:
                    logger.warning(f"Failed to get folder contents: {response.status}")
                    return {}
        except Exception as e:
            logger.error(f"Error getting folder contents: {e}")
            return {}
    
    async def _get_file_versions_async(self, session, project_id: str, item_id: str, headers: dict) -> List[Dict]:
        """异步获取文件版本信息"""
        url = f"https://developer.api.autodesk.com/data/v1/projects/{project_id}/items/{item_id}/versions"
        
        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    self.stats['api_calls'] += 1
                    return data.get('data', [])
                else:
                    logger.warning(f"Failed to get file versions: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error getting file versions: {e}")
            return []
    
    # ============================================================================
    # 辅助方法 - 异步API调用
    # ============================================================================
    
    async def _get_top_folders_async(self, project_id: str, headers: dict) -> dict:
        """异步获取项目顶级文件夹 - 使用正确的Hub-based API"""
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                # Step 1: Get hubs to find the hub containing this project
                hubs_url = "https://developer.api.autodesk.com/project/v1/hubs"
                
                async with session.get(hubs_url, headers=headers) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"Failed to get hubs: {response.status} - {error_text}")
                    
                    hubs_data = await response.json()
                    self.stats['api_calls'] += 1
                
                # Step 2: Find the hub containing our project
                hub_id = None
                for hub in hubs_data.get('data', []):
                    hub_id_candidate = hub.get('id')
                    
                    # Check if project exists in this hub
                    projects_url = f"https://developer.api.autodesk.com/project/v1/hubs/{hub_id_candidate}/projects"
                    async with session.get(projects_url, headers=headers) as proj_response:
                        if proj_response.status == 200:
                            projects_data = await proj_response.json()
                            self.stats['api_calls'] += 1
                            
                            for project in projects_data.get('data', []):
                                if project.get('id') == project_id:
                                    hub_id = hub_id_candidate
                                    break
                    
                    if hub_id:
                        break
                
                if not hub_id:
                    raise Exception(f"Project {project_id} not found in any accessible hub")
                
                # Step 3: Get top folders for the project
                top_folders_url = f"https://developer.api.autodesk.com/project/v1/hubs/{hub_id}/projects/{project_id}/topFolders"
                
                async with session.get(top_folders_url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.stats['api_calls'] += 1
                        return data
                    else:
                        error_text = await response.text()
                        raise Exception(f"Failed to get top folders: {response.status} - {error_text}")
                        
        except ImportError:
            # Fallback to synchronous requests if aiohttp not available
            import requests
            
            # Step 1: Get hubs
            hubs_url = "https://developer.api.autodesk.com/project/v1/hubs"
            response = requests.get(hubs_url, headers=headers)
            
            if response.status_code != 200:
                raise Exception(f"Failed to get hubs: {response.status_code} - {response.text}")
            
            hubs_data = response.json()
            self.stats['api_calls'] += 1
            
            # Step 2: Find hub containing project
            hub_id = None
            for hub in hubs_data.get('data', []):
                hub_id_candidate = hub.get('id')
                
                projects_url = f"https://developer.api.autodesk.com/project/v1/hubs/{hub_id_candidate}/projects"
                proj_response = requests.get(projects_url, headers=headers)
                
                if proj_response.status_code == 200:
                    projects_data = proj_response.json()
                    self.stats['api_calls'] += 1
                    
                    for project in projects_data.get('data', []):
                        if project.get('id') == project_id:
                            hub_id = hub_id_candidate
                            break
                
                if hub_id:
                    break
            
            if not hub_id:
                raise Exception(f"Project {project_id} not found in any accessible hub")
            
            # Step 3: Get top folders
            top_folders_url = f"https://developer.api.autodesk.com/project/v1/hubs/{hub_id}/projects/{project_id}/topFolders"
            response = requests.get(top_folders_url, headers=headers)
            
            if response.status_code == 200:
                self.stats['api_calls'] += 1
                return response.json()
            else:
                raise Exception(f"Failed to get top folders: {response.status_code} - {response.text}")
    
    async def _collect_all_items_recursive_async(self, project_id: str, top_folders: list, 
                                               headers: dict, max_depth: int) -> Tuple[List, List]:
        """异步递归收集所有文件夹和文件"""
        all_folders = []
        all_files = []
        
        # BFS queue: (folder_data, depth, parent_path)
        queue = [(folder, 0, "") for folder in top_folders]
        
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                while queue:
                    current_batch = queue[:self.batch_size]  # Process in batches
                    queue = queue[self.batch_size:]
                    
                    # Process batch of folders concurrently
                    tasks = []
                    for folder_data, depth, parent_path in current_batch:
                        if depth >= max_depth:
                            continue
                            
                        all_folders.append(folder_data)
                        folder_id = folder_data['id']
                        
                        # Create task for getting folder contents
                        task = self._get_folder_contents_async(session, project_id, folder_id, headers)
                        tasks.append((task, folder_data, depth, parent_path))
                    
                    # Wait for all tasks in batch to complete
                    for task, folder_data, depth, parent_path in tasks:
                        try:
                            contents = await task
                            
                            if contents and contents.get('data'):
                                for item in contents['data']:
                                    if item['type'] == 'folders':
                                        # Add subfolder to queue
                                        queue.append((item, depth + 1, parent_path))
                                    elif item['type'] == 'items':
                                        # Add file to collection
                                        all_files.append(item)
                                        
                        except Exception as e:
                            logger.warning(f"Failed to get contents for folder {folder_data.get('id')}: {e}")
                            continue
                    
                    # Add small delay to avoid rate limiting
                    if queue:  # Only delay if there are more items to process
                        await asyncio.sleep(self.api_delay)
                        
        except ImportError:
            # Fallback to synchronous processing
            logger.warning("aiohttp not available, using synchronous processing")
            return await self._collect_all_items_sync_fallback(project_id, top_folders, headers, max_depth)
        
        return all_folders, all_files
    
    async def _get_folder_contents_async(self, session, project_id: str, folder_id: str, headers: dict) -> dict:
        """异步获取文件夹内容"""
        url = f"https://developer.api.autodesk.com/data/v1/projects/{project_id}/folders/{folder_id}/contents"
        
        try:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    self.stats['api_calls'] += 1
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to get folder contents: {response.status} - {error_text}")
        except Exception as e:
            logger.warning(f"Error getting folder contents for {folder_id}: {e}")
            return {}
    
    async def _get_file_versions_async(self, session, project_id: str, item_id: str, headers: dict) -> List[Dict]:
        """获取文件的所有版本信息（参考MongoDB实现）"""
        try:
            url = f"https://developer.api.autodesk.com/data/v1/projects/{project_id}/items/{item_id}/versions"
            
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    versions = data.get('data', [])
                    
                    # 直接使用版本API返回的信息，不需要额外的详情API
                    detailed_versions = []
                    for version in versions:
                        # 从版本API响应中提取详细信息
                        version_attrs = version.get('attributes', {})
                        extension_data = version_attrs.get('extension', {}).get('data', {})
                        
                        # 添加详细属性到版本对象
                        version['detailed_attributes'] = {
                            'storageSize': version_attrs.get('storageSize', 0),
                            'mimeType': version_attrs.get('fileType'),  # 使用fileType作为mimeType
                            'processState': extension_data.get('processState'),
                            'downloadUrl': None,  # 需要从其他API获取
                            'storageUrn': None  # 将从自定义属性API获取
                        }
                        detailed_versions.append(version)
                    
                    return detailed_versions
                else:
                    logger.warning(f"获取文件版本失败: {response.status} - {await response.text()}")
                    return []
                    
        except Exception as e:
            logger.error(f"获取文件版本异常 {item_id}: {e}")
            return []
    
    async def _get_version_detail_async(self, session, project_id: str, version_id: str, headers: dict) -> Dict:
        """获取版本详细信息（包括文件大小、MIME类型等）"""
        try:
            url = f"https://developer.api.autodesk.com/data/v1/projects/{project_id}/versions/{version_id}"
            
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    version_data = data.get('data', {})
                    attributes = version_data.get('attributes', {})
                    relationships = version_data.get('relationships', {})
                    
                    # 提取关键信息（参考MongoDB的做法）
                    return {
                        'detailed_attributes': {
                            'storageSize': attributes.get('storageSize', 0),
                            'mimeType': attributes.get('mimeType'),
                            'processState': attributes.get('processState'),
                            'downloadUrl': relationships.get('downloadFormats', {}).get('links', {}).get('related'),
                            'storageUrn': relationships.get('storage', {}).get('data', {}).get('id')
                        }
                    }
                else:
                    logger.debug(f"获取版本详情失败: {response.status}")
                    return {}
                    
        except Exception as e:
            logger.debug(f"获取版本详情异常 {version_id}: {e}")
            return {}

    async def _call_custom_attributes_api(self, project_id: str, version_urns: List[str], headers: dict) -> List[Dict]:
        """調用ACC自定義屬性API"""
        try:
            import aiohttp
            
            # 移除 'b.' 前綴以用於BIM360 API
            bim360_project_id = project_id.replace('b.', '') if project_id.startswith('b.') else project_id
            
            url = f"https://developer.api.autodesk.com/bim360/docs/v1/projects/{bim360_project_id}/versions:batch-get"
            
            payload = {
                "urns": version_urns
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('results', [])
                    elif response.status == 404:
                        # 項目可能不支持自定義屬性
                        logger.info(f"Custom attributes not available for project {project_id}")
                        return []
                    else:
                        error_text = await response.text()
                        logger.warning(f"Custom attributes API failed: {response.status} - {error_text}")
                        return []
                        
        except ImportError:
            # Fallback to synchronous requests
            import requests
            
            bim360_project_id = project_id.replace('b.', '') if project_id.startswith('b.') else project_id
            url = f"https://developer.api.autodesk.com/bim360/docs/v1/projects/{bim360_project_id}/versions:batch-get"
            
            payload = {
                "urns": version_urns
            }
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('results', [])
            elif response.status_code == 404:
                logger.info(f"Custom attributes not available for project {project_id}")
                return []
            else:
                logger.warning(f"Custom attributes API failed: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            logger.error(f"Custom attributes API call failed: {e}")
            return []
    
    async def _collect_all_items_sync_fallback(self, project_id: str, top_folders: list, 
                                             headers: dict, max_depth: int) -> Tuple[List, List]:
        """同步方式收集数据的后备方案"""
        import requests
        
        all_folders = []
        all_files = []
        
        queue = [(folder, 0, "") for folder in top_folders]
        
        while queue:
            folder_data, depth, parent_path = queue.pop(0)
            
            if depth >= max_depth:
                continue
                
            all_folders.append(folder_data)
            folder_id = folder_data['id']
            
            try:
                url = f"https://developer.api.autodesk.com/data/v1/projects/{project_id}/folders/{folder_id}/contents"
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    self.stats['api_calls'] += 1
                    contents = response.json()
                    
                    if contents and contents.get('data'):
                        for item in contents['data']:
                            if item['type'] == 'folders':
                                queue.append((item, depth + 1, parent_path))
                            elif item['type'] == 'items':
                                all_files.append(item)
                else:
                    logger.warning(f"Failed to get contents for folder {folder_id}: {response.status_code}")
                    
            except Exception as e:
                logger.warning(f"Error processing folder {folder_id}: {e}")
                continue
            
            # Rate limiting
            time.sleep(self.api_delay)
        
        return all_folders, all_files
    
    async def _sync_folder_custom_attribute_definitions(self, project_id: str, folder_id: str, headers: dict) -> List[Dict[str, Any]]:
        """同步文件夾的自定義屬性定義"""
        try:
            import aiohttp
            import urllib.parse
            
            # Remove 'b.' prefix for BIM360 API
            bim360_project_id = project_id.replace('b.', '') if project_id.startswith('b.') else project_id
            
            # URL encode folder ID
            encoded_folder_id = urllib.parse.quote(folder_id, safe='')
            
            url = f"https://developer.api.autodesk.com/bim360/docs/v1/projects/{bim360_project_id}/folders/{encoded_folder_id}/custom-attribute-definitions"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        definitions = data.get('results', [])
                        
                        logger.info(f"Found {len(definitions)} custom attribute definitions for folder {folder_id}")
                        
                        # Transform to our format
                        folder_definitions = []
                        for definition in definitions:
                            attr_def = {
                                'attr_id': definition.get('id'),
                                'project_id': project_id,
                                'scope_type': 'folder',  # 设置作用域类型为文件夹
                                'scope_folder_id': folder_id,  # 关联到具体文件夹
                                'name': definition.get('name'),
                                'type': definition.get('type'),
                                'array_values': definition.get('arrayValues', []),
                                'description': None,  # Not provided by API
                                'is_required': False,  # Default
                                'default_value': None,  # Not provided by API
                                'inherit_to_subfolders': False  # 不继承到子文件夹，每个文件夹独立设置
                            }
                            folder_definitions.append(attr_def)
                        
                        return folder_definitions
                        
                    elif response.status == 404:
                        # Folder may not have custom attributes defined
                        logger.debug(f"No custom attributes defined for folder {folder_id}")
                        return []
                    else:
                        error_text = await response.text()
                        logger.warning(f"Failed to get folder custom attributes: {response.status} - {error_text}")
                        return []
                        
        except ImportError:
            # Fallback to synchronous requests
            import requests
            import urllib.parse
            
            bim360_project_id = project_id.replace('b.', '') if project_id.startswith('b.') else project_id
            encoded_folder_id = urllib.parse.quote(folder_id, safe='')
            
            url = f"https://developer.api.autodesk.com/bim360/docs/v1/projects/{bim360_project_id}/folders/{encoded_folder_id}/custom-attribute-definitions"
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                definitions = data.get('results', [])

                folder_definitions = []
                for definition in definitions:
                    attr_def = {
                        'attr_id': definition.get('id'),
                        'project_id': project_id,
                        'scope_type': 'folder',  # 设置作用域类型为文件夹
                        'scope_folder_id': folder_id,  # 关联到具体文件夹
                        'name': definition.get('name'),
                        'type': definition.get('type'),
                        'array_values': definition.get('arrayValues', []),
                        'description': None,
                        'is_required': False,
                        'default_value': None,
                        'inherit_to_subfolders': False  # 不继承到子文件夹
                    }
                    folder_definitions.append(attr_def)

                return folder_definitions
            else:
                logger.debug(f"No custom attributes for folder {folder_id}: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting folder custom attributes for {folder_id}: {e}")
            return []

    async def _batch_process_folders_async(self, folders: List, project_id: str, headers: dict = None, include_custom_attributes: bool = False) -> Dict[str, Any]:
        """异步批量处理文件夹"""
        try:
            from database.data_sync_strategy import DataTransformer
            
            dal = await get_optimized_postgresql_dal()
            transformer = DataTransformer()
            
            # Transform folder data
            folders_data = []
            all_folder_definitions = []
            
            for folder_api_data in folders:
                try:
                    folder_record = transformer.transform_folder_data(
                        folder_api_data, project_id, None, "", 0
                    )
                    folders_data.append(folder_record)
                    
                    # 🔑 Get folder custom attribute definitions if requested
                    if include_custom_attributes and headers:
                        folder_id = folder_api_data.get('id')
                        if folder_id:
                            try:
                                folder_definitions = await self._sync_folder_custom_attribute_definitions(
                                    project_id, folder_id, headers
                                )
                                all_folder_definitions.extend(folder_definitions)
                                
                                if folder_definitions:
                                    logger.info(f"Found {len(folder_definitions)} custom attribute definitions for folder {folder_record.get('name')}")
                                    
                            except Exception as e:
                                logger.warning(f"Failed to get custom attributes for folder {folder_id}: {e}")
                    
                except Exception as e:
                    logger.warning(f"Failed to transform folder data: {e}")
                    continue
            
            # Batch insert folders to database
            folders_synced = 0
            if folders_data:
                result = await dal.batch_upsert_folders(folders_data)
                folders_synced = result.get('upserted', 0)
                self.stats['batch_operations'] += 1
            
            # 🔑 Batch insert folder custom attribute definitions
            folder_definitions_synced = 0
            if all_folder_definitions:
                logger.info(f"Processing {len(all_folder_definitions)} folder custom attribute definitions...")
                try:
                    # Remove duplicates
                    unique_definitions = self._deduplicate_definitions(all_folder_definitions)
                    def_result = await dal.batch_upsert_custom_attribute_definitions(unique_definitions)
                    folder_definitions_synced = def_result.get('upserted', 0)
                    logger.info(f"✅ Folder custom attribute definitions synced: {folder_definitions_synced}")
                    
                except Exception as e:
                    logger.error(f"Failed to sync folder custom attribute definitions: {e}")
            
            return {
                'synced': folders_synced,
                'folder_custom_attrs_synced': folder_definitions_synced
            }
            
        except Exception as e:
            logger.error(f"Error in batch folder processing: {e}")
            return {'synced': 0}
    
    async def _batch_process_files_async(self, files: List, project_id: str) -> Dict[str, Any]:
        """异步批量处理文件"""
        try:
            from database.data_sync_strategy import DataTransformer
            
            dal = await get_optimized_postgresql_dal()
            transformer = DataTransformer()
            
            # Transform file data
            files_data = []
            versions_data = []
            custom_attrs_definitions = []
            custom_attrs_values = []
            
            for file_api_data in files:
                try:
                    file_record = transformer.transform_file_data(
                        file_api_data, project_id, None, "", 0
                    )
                    files_data.append(file_record)
                    
                    # 🔑 Process custom attributes from enriched file data
                    custom_attrs = file_api_data.get('custom_attributes', [])
                    if custom_attrs:
                        logger.info(f"DEBUG: Processing {len(custom_attrs)} custom attributes for {file_record.get('name')}")
                        
                        for attr in custom_attrs:
                            # Attribute definition
                            attr_def = {
                                'attr_id': attr.get('id'),
                                'project_id': project_id,
                                'name': attr.get('name'),
                                'type': attr.get('type'),
                                'array_values': attr.get('arrayValues', [])
                            }
                            custom_attrs_definitions.append(attr_def)
                            
                            # Attribute value
                            attr_value = {
                                'file_id': file_record['id'],
                                'attr_id': attr.get('id'),
                                'project_id': project_id,
                                'value': attr.get('value'),
                                'value_date': self._parse_date_value(attr) if attr.get('type') == 'date' else None,
                                'value_number': self._parse_number_value(attr) if attr.get('type') == 'number' else None,
                                'value_boolean': self._parse_boolean_value(attr) if attr.get('type') == 'boolean' else None
                            }
                            custom_attrs_values.append(attr_value)
                    
                    # 🔑 Create file version records from detailed version info
                    versions_info = file_api_data.get('versions_info', [])
                    if versions_info:
                        logger.info(f"DEBUG: Creating {len(versions_info)} versions for {file_record.get('name')}")
                        
                        for version in versions_info:
                            version_id = version.get('id')
                            if version_id:
                                # 获取详细属性（参考MongoDB实现）
                                version_attrs = version.get('attributes', {})
                                detailed_attrs = version.get('detailed_attributes', {})
                                
                                # 优先使用详细信息，回退到基本信息
                                file_size = (
                                    detailed_attrs.get('storageSize', 0) or
                                    version_attrs.get('storageSize', 0) or
                                    0
                                )
                                
                                mime_type = (
                                    detailed_attrs.get('mimeType') or
                                    version_attrs.get('mimeType')
                                )
                                
                                storage_urn = (
                                    detailed_attrs.get('storageUrn') or
                                    version_attrs.get('storageUrn')
                                )
                                
                                version_record = {
                                    'id': version_id,
                                    'project_id': project_id,
                                    'file_id': file_record['id'],
                                    'version_number': version_attrs.get('versionNumber', 1),
                                    'version_type': 'tip' if version == versions_info[0] else 'historical',
                                    'create_time': self._parse_datetime(version_attrs.get('createTime')),
                                    'create_user_id': version_attrs.get('createUserId'),
                                    'create_user_name': version_attrs.get('createUserName'),
                                    'file_size': file_size,
                                    'storage_urn': storage_urn,
                                    'mime_type': mime_type,
                                    'metadata': {
                                        'process_state': detailed_attrs.get('processState'),
                                        'download_url': detailed_attrs.get('downloadUrl'),
                                        'enhanced_version': True
                                    }
                                }
                                versions_data.append(version_record)
                                
                                # 更新文件记录的信息（使用最新版本的信息）
                                if version == versions_info[0]:  # 最新版本
                                    file_record.update({
                                        'file_size': file_size,
                                        'mime_type': mime_type,
                                        'storage_urn': storage_urn,
                                        'process_state': detailed_attrs.get('processState'),
                                        'download_url': detailed_attrs.get('downloadUrl')
                                    })
                    else:
                        # 回退到原有逻辑（如果没有详细版本信息）
                        tip_version_urn = file_record.get('tip_version_urn')
                        if tip_version_urn:
                            logger.info(f"DEBUG: Creating fallback version for {file_record.get('name')}")
                            version_record = {
                                'id': tip_version_urn,
                                'project_id': project_id,
                                'file_id': file_record['id'],
                                'version_number': 1,
                                'version_type': 'tip',
                                'create_time': file_record.get('create_time'),
                                'create_user_id': file_record.get('create_user_id'),
                                'create_user_name': file_record.get('create_user_name'),
                                'file_size': file_record.get('file_size', 0),
                                'storage_urn': file_record.get('storage_location'),
                                'mime_type': file_record.get('mime_type'),
                                'metadata': {
                                    'is_tip_version': True,
                                    'fallback_version': True
                                }
                            }
                            versions_data.append(version_record)
                    
                except Exception as e:
                    logger.warning(f"Failed to transform file data: {e}")
                    continue
            
            # Batch insert files to database
            if files_data:
                result = await dal.batch_upsert_files(files_data)
                self.stats['batch_operations'] += 1
                
                # 🔑 Batch insert file versions
                if versions_data:
                    logger.info(f"DEBUG: Creating {len(versions_data)} file versions...")
                    try:
                        versions_result = await dal.batch_upsert_file_versions(versions_data)
                        logger.info(f"✅ File versions created: {versions_result.get('upserted', 0)}")
                    except Exception as e:
                        logger.error(f"Failed to create file versions: {e}")
                
                # 🔑 Batch insert custom attributes
                custom_attrs_synced = 0
                if custom_attrs_definitions:
                    logger.info(f"DEBUG: Processing {len(custom_attrs_definitions)} custom attribute definitions...")
                    try:
                        # Remove duplicates from definitions
                        unique_definitions = self._deduplicate_definitions(custom_attrs_definitions)
                        def_result = await dal.batch_upsert_custom_attribute_definitions(unique_definitions)
                        logger.info(f"✅ Custom attribute definitions created: {def_result.get('upserted', 0)}")
                        
                        # Insert attribute values
                        if custom_attrs_values:
                            logger.info(f"DEBUG: Creating {len(custom_attrs_values)} custom attribute values...")
                            value_result = await dal.batch_upsert_custom_attribute_values(custom_attrs_values)
                            custom_attrs_synced = value_result.get('upserted', 0)
                            logger.info(f"✅ Custom attribute values created: {custom_attrs_synced}")
                        
                    except Exception as e:
                        logger.error(f"Failed to create custom attributes: {e}")
                
                return {
                    'synced': result.get('upserted', 0),
                    'custom_attrs_synced': custom_attrs_synced
                }
            
            return {'synced': 0}
            
        except Exception as e:
            logger.error(f"Error in batch file processing: {e}")
            return {'synced': 0}
    
    async def _batch_process_custom_attributes_async(self, files: List, project_id: str, headers: dict) -> Dict[str, Any]:
        """异步批量处理自定义属性"""
        try:
            # For now, return 0 as custom attributes require additional API setup
            # In a full implementation, this would:
            # 1. Extract file IDs from the files list
            # 2. Call Custom Attributes API in batches
            # 3. Transform and store the attributes
            logger.info("Custom attributes processing skipped (requires additional API setup)")
            return {'synced': 0}
            
        except Exception as e:
            logger.error(f"Error in custom attributes processing: {e}")
            return {'synced': 0}
    
    def _parse_datetime(self, datetime_str):
        """解析API返回的日期时间字符串"""
        if not datetime_str:
            return None
        
        try:
            from datetime import datetime
            # ACC API通常返回ISO格式的时间戳
            if datetime_str.endswith('Z'):
                # UTC时间戳
                return datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
            else:
                # 尝试直接解析
                return datetime.fromisoformat(datetime_str)
        except Exception as e:
            logger.warning(f"解析日期时间失败: {datetime_str}, {str(e)}")
            return None

    def _calculate_optimization_efficiency(self, folders_count: int, files_count: int, duration: float) -> float:
        """计算优化效率"""
        try:
            # Simple efficiency calculation based on items per second
            total_items = folders_count + files_count
            if total_items == 0 or duration == 0:
                return 100.0
            
            items_per_second = total_items / duration
            
            # Efficiency scale: 
            # > 10 items/sec = 95%+
            # > 5 items/sec = 85%+  
            # > 1 item/sec = 70%+
            # < 1 item/sec = lower
            
            if items_per_second >= 10:
                return min(95.0 + (items_per_second - 10) * 0.5, 100.0)
            elif items_per_second >= 5:
                return 85.0 + (items_per_second - 5) * 2.0
            elif items_per_second >= 1:
                return 70.0 + (items_per_second - 1) * 3.75
            else:
                return max(50.0, 70.0 * items_per_second)
                
        except Exception:
            return 75.0  # Default efficiency
    
    # ============================================================================
    # 辅助方法 - 其他
    # ============================================================================
    
    def _get_performance_stats(self) -> Dict[str, Any]:
        """获取性能统计"""
        return {
            'api_calls': self.stats['api_calls'],
            'api_calls_saved': self.stats['api_calls_saved'],
            'smart_skips': self.stats['smart_skips'],
            'batch_operations': self.stats['batch_operations'],
            'concurrent_operations': self.stats['concurrent_operations'],
            'memory_peak_mb': self.stats['memory_peak_mb'],
            'processing_time_seconds': round(self.stats['processing_time'], 2)
        }
    
    
    def _get_last_sync_time(self, project_id: str) -> datetime:
        """获取上次同步时间（同步方法）"""
        # 这里应该从数据库获取，暂时返回一个默认值
        return datetime.utcnow() - timedelta(hours=1)
    
    def _deduplicate_definitions(self, definitions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """去重属性定义"""
        seen = set()
        unique_definitions = []

        for definition in definitions:
            # Use attr_id, project_id, and scope_folder_id for deduplication
            # scope_folder_id can be None for project-level attributes
            key = (
                definition.get('attr_id'),
                definition.get('project_id'),
                definition.get('scope_folder_id')  # 包含文件夹ID以区分不同文件夹的属性定义
            )
            if key not in seen:
                seen.add(key)
                unique_definitions.append(definition)

        return unique_definitions
    
    async def _get_attr_definition_id_mapping(self, definitions: List[Dict], dal) -> Dict[int, int]:
        """获取ACC API属性ID到数据库定义ID的映射"""
        mapping = {}
        
        try:
            async with dal.get_connection() as conn:
                for definition in definitions:
                    acc_attr_id = definition.get('attr_id')
                    project_id = definition.get('project_id')
                    
                    if acc_attr_id and project_id:
                        # 查询数据库中对应的定义ID
                        result = await conn.fetchrow("""
                            SELECT id FROM custom_attribute_definitions 
                            WHERE attr_id = $1 AND project_id = $2
                            LIMIT 1
                        """, acc_attr_id, project_id)
                        
                        if result:
                            mapping[acc_attr_id] = result['id']
                            
        except Exception as e:
            logger.error(f"Failed to get attribute definition ID mapping: {e}")
            
        return mapping
    
    # ============================================================================
    # 🚀 V2架构专用同步方法
    # ============================================================================
    
    async def _optimized_incremental_sync_v2(self, project_id: str, max_depth: int = 10, 
                                           include_custom_attributes: bool = True, 
                                           task_uuid: str = None, headers: dict = None) -> Dict[str, Any]:
        """V2架构的优化增量同步"""
        
        logger.info(f"🚀 开始优化增量同步 V2: 项目 {project_id}")
        start_time = time.time()
        
        try:
            # 重置统计
            self.stats = {key: 0 for key in self.stats}
            
            dal = await get_optimized_postgresql_dal()
            
            # 🔑 获取上次同步时间
            last_sync_time = await dal.get_project_last_sync_time(project_id)
            if not last_sync_time:
                logger.info("未找到上次同步时间，执行全量同步")
                return await self._optimized_full_sync_v2(project_id, max_depth, include_custom_attributes, task_uuid, headers)
            
            logger.info(f"上次同步时间: {last_sync_time}")
            
            # 🚀 Layer 1: 智能分支跳过 (V2版本)
            folders_to_check = await self._smart_branch_filtering_v2(project_id, last_sync_time, headers)
            
            if not folders_to_check:
                logger.info("✅ 智能跳过：项目无变化")
                return {
                    'status': 'no_changes',
                    'folders_synced': 0,
                    'files_synced': 0,
                    'custom_attrs_synced': 0,
                    'performance_stats': self._get_performance_stats(),
                    'optimization_efficiency': 100.0,
                    'architecture_version': 'v2'
                }
            
            # 🚀 Layer 2: 批量API调用 (V2版本)
            changed_folders, changed_files = await self._batch_api_operations_v2(project_id, folders_to_check, headers)
            
            logger.info(f"📊 API批量操作完成: {len(changed_folders)} 文件夹, {len(changed_files)} 文件")
            
            # 🚀 Layer 3: 文件级timestamp比对和批量标记 (V2版本)
            files_needing_updates = await self._identify_files_needing_updates_v2(
                changed_files, project_id, last_sync_time, dal
            )
            
            logger.info(f"🎯 文件更新分析: {len(files_needing_updates)} 个文件需要更新")
            
            # 获取文件详细信息（包括自定义属性）- V2版本
            # 只处理需要更新的文件
            files_to_process = []
            if files_needing_updates:
                # 从需要更新的文件中提取文件数据
                files_to_process = [item['file_data'] for item in files_needing_updates if 'file_data' in item]
                
                if include_custom_attributes and files_to_process:
                    files_to_process = await self._batch_get_file_versions_and_custom_attrs_v2(project_id, files_to_process, headers)
            
            # 🚀 Layer 4: 批量数据库操作 (V2版本)
            folders_synced = 0
            files_synced = 0
            custom_attrs_synced = 0
            
            if changed_folders:
                folders_synced = await self._batch_insert_folders_v2(changed_folders, dal)
            
            if files_to_process:
                # 转换文件数据为V2格式
                v2_files_data = []
                for file_data in files_to_process:
                    custom_attrs = file_data.get('custom_attributes', {})
                    v2_file = {
                        'id': file_data.get('id'),
                        'project_id': file_data.get('project_id'),
                        'name': file_data.get('name') or custom_attrs.get('name'),
                        'display_name': file_data.get('display_name') or custom_attrs.get('title'),
                        'parent_folder_id': file_data.get('parent_folder_id'),
                        'folder_path': file_data.get('folder_path', ''),
                        'full_path': file_data.get('full_path', ''),
                        'path_segments': file_data.get('path_segments', []),
                        'depth': file_data.get('depth', 0),
                        'create_time': custom_attrs.get('createTime'),
                        'create_user_id': custom_attrs.get('createUserId'),
                        'create_user_name': custom_attrs.get('createUserName'),
                        'last_modified_time': custom_attrs.get('lastModifiedTime'),
                        'last_modified_user_id': custom_attrs.get('lastModifiedUserId'),
                        'last_modified_user_name': custom_attrs.get('lastModifiedUserName'),
                        'file_type': custom_attrs.get('name', '').split('.')[-1] if custom_attrs.get('name') else '',
                        'mime_type': '',
                        'reserved': False,
                        'hidden': False,
                        'metadata': {},
                        'file_permissions': {},
                        'file_settings': {},
                        'review_info': {},
                        'sync_info': {'synced_at': datetime.now().isoformat()}
                    }
                    
                    # 转换时间戳字段为中国时区
                    timestamp_fields = ['create_time', 'last_modified_time']
                    v2_file = self._batch_convert_timestamps_to_china(v2_file, timestamp_fields)
                    v2_files_data.append(v2_file)
                
                files_synced = await self._batch_insert_files_v2(v2_files_data, dal)
                
                # 插入文件版本 (V2架构)
                await self._batch_insert_file_versions_v2(files_to_process, dal)
            
            if include_custom_attributes and files_to_process:
                custom_attrs_synced = await self._batch_insert_custom_attributes_v2(files_to_process, dal)
            
            # 只有在实际同步了内容时才更新同步状态
            if folders_synced > 0 or files_synced > 0 or custom_attrs_synced > 0:
                await self._update_project_sync_status(project_id, dal)
            
            # 计算结果
            duration = time.time() - start_time
            optimization_efficiency = self._calculate_optimization_efficiency(folders_synced, files_synced, duration)
            
            result = {
                'status': 'success',
                'message': 'V2 Incremental sync completed successfully',
                'folders_synced': folders_synced,
                'files_synced': files_synced,
                'custom_attrs_synced': custom_attrs_synced,
                'files_needing_updates': len(files_needing_updates),
                'duration_seconds': round(duration, 2),
                'optimization_efficiency': optimization_efficiency,
                'performance_stats': self._get_performance_stats(),
                'architecture_version': 'v2'
            }
            
            logger.info(f"✅ V2增量同步完成: {result}")
            return result
            
        except Exception as e:
            logger.error(f"❌ V2增量同步失败: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'duration_seconds': time.time() - start_time,
                'architecture_version': 'v2'
            }
    
    async def _smart_branch_filtering_v2(self, project_id: str, last_sync_time: datetime, 
                                       headers: dict) -> List[Dict[str, Any]]:
        """V2架构的智能分支过滤"""
        return await self._smart_branch_filtering(project_id, last_sync_time, headers)
    
    async def _batch_api_operations_v2(self, project_id: str, folders_to_check: List[Dict], 
                                     headers: dict) -> tuple:
        """V2架构的批量API操作"""
        return await self._batch_api_operations(project_id, folders_to_check, headers)
    
    async def _identify_files_needing_updates_v2(self, changed_files: List[Dict], 
                                               project_id: str, last_sync_time: datetime, 
                                               dal) -> List[Dict]:
        """V2架构的文件更新识别"""
        return await self._identify_files_needing_updates(changed_files, project_id, last_sync_time, dal)
    
    async def _optimized_full_sync_v2(self, project_id: str, max_depth: int = 10, 
                                    include_custom_attributes: bool = True, 
                                    task_uuid: str = None, headers: dict = None) -> Dict[str, Any]:
        """V2架构的优化全量同步"""
        
        logger.info(f"🚀 开始优化全量同步 V2: 项目 {project_id}")
        start_time = time.time()
        
        try:
            # 1. 清除现有项目数据
            dal = await get_optimized_postgresql_dal()
            
            async with dal.get_connection() as conn:
                # Clear existing project data - first count, then delete
                deleted_attrs = await conn.fetchval("SELECT COUNT(*) FROM custom_attribute_values WHERE project_id = $1", project_id) or 0
                await conn.execute("DELETE FROM custom_attribute_values WHERE project_id = $1", project_id)
                
                deleted_defs = await conn.fetchval("SELECT COUNT(*) FROM custom_attribute_definitions WHERE project_id = $1", project_id) or 0
                await conn.execute("DELETE FROM custom_attribute_definitions WHERE project_id = $1", project_id)
                
                deleted_versions = await conn.fetchval("SELECT COUNT(*) FROM file_versions WHERE project_id = $1", project_id) or 0
                await conn.execute("DELETE FROM file_versions WHERE project_id = $1", project_id)
                
                deleted_files = await conn.fetchval("SELECT COUNT(*) FROM files WHERE project_id = $1", project_id) or 0
                await conn.execute("DELETE FROM files WHERE project_id = $1", project_id)
                
                deleted_folders = await conn.fetchval("SELECT COUNT(*) FROM folders WHERE project_id = $1", project_id) or 0
                await conn.execute("DELETE FROM folders WHERE project_id = $1", project_id)
                
            logger.info(f"🧹 数据清理完成: 文件夹({deleted_folders}), 文件({deleted_files}), 版本({deleted_versions}), 属性定义({deleted_defs}), 属性值({deleted_attrs})")
            
            # 2. 检查认证头
            if not headers:
                logger.error("Missing authentication headers")
                return {
                    'status': 'error',
                    'error': 'Missing authentication headers'
                }
            
            # 3. 获取项目顶级文件夹
            logger.info(f"📁 获取项目顶级文件夹...")
            
            try:
                # Call real ACC API to get top-level folders
                top_folders_data = await self._get_top_folders_async(project_id, headers)
                if not top_folders_data or not top_folders_data.get('data'):
                    logger.warning(f"No top-level folders found for project {project_id}")
                    return {
                        'status': 'success',
                        'message': 'No folders found in project',
                        'folders_synced': 0,
                        'files_synced': 0,
                        'custom_attrs_synced': 0,
                        'performance_stats': self.stats
                    }
                
                top_folders = top_folders_data.get('data', [])
                logger.info(f"📂 找到 {len(top_folders)} 个顶级文件夹")
                
                # 4. BFS递归收集所有数据
                logger.info("🔄 开始BFS递归收集数据...")
                all_folders, all_files, all_custom_attrs = await self._bfs_collect_all_data_v2(
                    project_id, top_folders, max_depth, include_custom_attributes, headers
                )
                
                # 5. 获取文件版本和自定义属性详细信息
                if all_files:
                    logger.info("Getting file versions and custom attributes...")
                    enriched_files = await self._batch_get_file_versions_and_custom_attrs_v2(
                        project_id, all_files, headers
                    )
                    all_files = enriched_files
                
                # 5. 批量插入数据 - 使用V2架构
                logger.info("💾 开始批量数据库操作...")
                
                # 5.1 插入文件夹
                folders_synced = await self._batch_insert_folders_v2(all_folders, dal)
                
                # 5.2 插入文件 (使用V2字段)
                # 转换文件数据为V2格式
                v2_files_data = []
                for file_data in all_files:
                    # 使用自定义属性中的信息来填充V2字段
                    custom_attrs = file_data.get('custom_attributes', {})
                    
                    v2_file = {
                        'id': file_data.get('id'),
                        'project_id': file_data.get('project_id'),
                        'name': file_data.get('name') or custom_attrs.get('name'),
                        'display_name': file_data.get('display_name') or custom_attrs.get('title'),
                        'parent_folder_id': file_data.get('parent_folder_id'),
                        'folder_path': file_data.get('folder_path', ''),
                        'full_path': file_data.get('full_path', ''),
                        'path_segments': file_data.get('path_segments', []),
                        'depth': file_data.get('depth', 0),
                        'create_time': custom_attrs.get('createTime'),
                        'create_user_id': custom_attrs.get('createUserId'),
                        'create_user_name': custom_attrs.get('createUserName'),
                        'last_modified_time': custom_attrs.get('lastModifiedTime'),
                        'last_modified_user_id': custom_attrs.get('lastModifiedUserId'),
                        'last_modified_user_name': custom_attrs.get('lastModifiedUserName'),
                        'file_type': custom_attrs.get('name', '').split('.')[-1] if custom_attrs.get('name') else '',
                        'mime_type': '',
                        'reserved': False,
                        'hidden': False,
                        'metadata': {},
                        'file_permissions': {},
                        'file_settings': {},
                        'review_info': {},
                        'sync_info': {'synced_at': datetime.now().isoformat()}
                    }
                    
                    # 转换时间戳字段为中国时区
                    timestamp_fields = ['create_time', 'last_modified_time']
                    v2_file = self._batch_convert_timestamps_to_china(v2_file, timestamp_fields)
                    v2_files_data.append(v2_file)
                
                files_synced = await self._batch_insert_files_v2(v2_files_data, dal)
                
                # 5.3 插入文件版本 (集中管理版本信息)
                versions_synced = await self._batch_insert_file_versions_v2(all_files, dal)
                
                # 5.4 插入自定义属性 (使用V2关联设计)
                custom_attrs_synced = 0
                if include_custom_attributes and all_files:
                    custom_attrs_synced = await self._batch_insert_custom_attributes_v2(all_files, dal)

                # 5.5 插入文件夹自定义属性定义
                folder_attr_defs_synced = 0
                logger.info(f"📋 Total folder custom attribute definitions collected: {len(all_custom_attrs.get('definitions', []))}")
                if include_custom_attributes and all_custom_attrs.get('definitions'):
                    try:
                        definitions = all_custom_attrs['definitions']
                        logger.info(f"📋 Processing {len(definitions)} folder custom attribute definitions...")
                        # 去重
                        unique_definitions = self._deduplicate_definitions(definitions)
                        logger.info(f"📋 After deduplication: {len(unique_definitions)} unique definitions")
                        if unique_definitions:
                            result = await dal.batch_upsert_custom_attribute_definitions(unique_definitions)
                            folder_attr_defs_synced = result.get('upserted', 0)
                            logger.info(f"✅ Folder custom attribute definitions synced: {folder_attr_defs_synced}")
                    except Exception as e:
                        logger.error(f"Failed to sync folder custom attribute definitions: {e}")
                        import traceback
                        logger.error(traceback.format_exc())

                # 6. 更新项目同步状态
                await self._update_project_sync_status(project_id, dal)
                
                end_time = time.time()
                duration = end_time - start_time
                
                # 7. 生成结果报告
                result = {
                    'status': 'success',
                    'folders_synced': folders_synced,
                    'files_synced': files_synced,
                    'versions_synced': versions_synced,
                    'custom_attrs_synced': custom_attrs_synced,
                    'total_time_seconds': round(duration, 2),
                    'performance_stats': self.stats,
                    'architecture_version': 'v2'
                }
                
                logger.info(f"✅ V2全量同步完成: {result}")
                return result
                
            except Exception as e:
                logger.error(f"V2同步过程中出错: {e}")
                return {
                    'status': 'error',
                    'error': str(e),
                    'folders_synced': 0,
                    'files_synced': 0,
                    'custom_attrs_synced': 0,
                    'architecture_version': 'v2'
                }
                
        except Exception as e:
            logger.error(f"❌ V2全量同步失败: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'folders_synced': 0,
                'files_synced': 0,
                'custom_attrs_synced': 0,
                'architecture_version': 'v2'
            }
    
    async def _bfs_collect_all_data_v2(self, project_id: str, top_folders: List[Dict], 
                                     max_depth: int, include_custom_attributes: bool, 
                                     headers: dict) -> Tuple[List[Dict], List[Dict], Dict]:
        """BFS收集所有数据 - V2优化版本"""
        
        all_folders = []
        all_files = []
        all_custom_attrs = {'definitions': [], 'values': []}
        
        try:
            import aiohttp
            
            async with aiohttp.ClientSession() as session:
                # BFS队列：(folder_data, depth, parent_path)
                queue = [(folder, 0, "") for folder in top_folders]
                
                while queue and len(queue) > 0:
                    current_folder, depth, parent_path = queue.pop(0)
                    
                    if depth >= max_depth:
                        continue
                    
                    folder_id = current_folder.get('id')
                    folder_name = current_folder.get('attributes', {}).get('name', 'Unknown')
                    current_path = f"{parent_path}/{folder_name}".strip('/')
                    
                    # 转换文件夹数据为V2格式
                    folder_data = self._transform_folder_data_v2(current_folder, project_id, parent_path, depth)
                    all_folders.append(folder_data)

                    # 🔑 收集文件夹自定义属性定义
                    if include_custom_attributes:
                        try:
                            folder_defs = await self._get_folder_custom_attr_definitions_v2(
                                project_id, folder_id, headers, session
                            )
                            if folder_defs:
                                all_custom_attrs['definitions'].extend(folder_defs)
                                logger.info(f"📋 Found {len(folder_defs)} custom attribute definitions for folder {folder_name}")
                        except Exception as e:
                            logger.warning(f"Failed to get custom attributes for folder {folder_id}: {e}")
                    
                    # 获取文件夹内容
                    contents_url = f"https://developer.api.autodesk.com/data/v1/projects/{project_id}/folders/{folder_id}/contents"
                    
                    try:
                        async with session.get(contents_url, headers=headers) as response:
                            if response.status == 200:
                                contents_data = await response.json()
                                self.stats['api_calls'] += 1
                                
                                for item in contents_data.get('data', []):
                                    item_type = item.get('type')
                                    
                                    if item_type == 'folders':
                                        # 添加子文件夹到队列
                                        queue.append((item, depth + 1, current_path))
                                    
                                    elif item_type == 'items':
                                        # 转换文件数据为V2格式
                                        file_data = self._transform_file_data_v2(item, project_id, current_path, depth + 1)
                                        all_files.append(file_data)
                            
                            else:
                                logger.warning(f"Failed to get folder contents: {response.status}")
                                
                    except Exception as e:
                        logger.error(f"Error getting folder contents for {folder_name}: {e}")
                        continue
                
                # 文件夹自定义属性已在BFS遍历中收集到all_custom_attrs['definitions']
                logger.info(f"📊 BFS收集完成: {len(all_folders)} 文件夹, {len(all_files)} 文件, {len(all_custom_attrs.get('definitions', []))} 文件夹属性定义")
                
                return all_folders, all_files, all_custom_attrs
                
        except ImportError:
            logger.error("aiohttp not available, cannot make API calls")
            return [], [], {}
        except Exception as e:
            logger.error(f"BFS数据收集失败: {e}")
            return [], [], {}
    
    def _transform_folder_data_v2(self, folder_data: Dict, project_id: str, parent_path: str, depth: int) -> Dict:
        """转换文件夹数据为V2格式，并转换时区为中国时区"""
        attributes = folder_data.get('attributes', {})
        
        # 基础数据
        folder_record = {
            'id': folder_data.get('id'),
            'project_id': project_id,
            'name': attributes.get('name'),
            'display_name': attributes.get('displayName'),
            'parent_id': folder_data.get('relationships', {}).get('parent', {}).get('data', {}).get('id'),
            'path': f"{parent_path}/{attributes.get('name')}".strip('/'),
            'path_segments': f"{parent_path}/{attributes.get('name')}".strip('/').split('/'),
            'depth': depth,
            'create_time': attributes.get('createTime'),
            'create_user_id': attributes.get('createUserId'),
            'create_user_name': attributes.get('createUserName'),
            'last_modified_time': attributes.get('lastModifiedTime'),
            'last_modified_user_id': attributes.get('lastModifiedUserId'),
            'last_modified_user_name': attributes.get('lastModifiedUserName'),
            'last_modified_time_rollup': attributes.get('lastModifiedTime'),  # 初始设为相同值
            'object_count': attributes.get('objectCount', 0),
            'total_size': 0,
            'hidden': attributes.get('hidden', False),
            'metadata': attributes.get('extension', {}),
            'extension': attributes.get('extension', {}),
            'children_stats': {},
            'sync_info': {'synced_at': datetime.now().isoformat()}
        }
        
        # 批量转换时间戳字段为中国时区
        timestamp_fields = ['create_time', 'last_modified_time', 'last_modified_time_rollup']
        return self._batch_convert_timestamps_to_china(folder_record, timestamp_fields)
    
    def _transform_file_data_v2(self, file_data: Dict, project_id: str, folder_path: str, depth: int) -> Dict:
        """转换文件数据为V2格式，并转换时区为中国时区"""
        attributes = file_data.get('attributes', {})
        
        # 基础数据
        file_record = {
            'id': file_data.get('id'),
            'project_id': project_id,
            'name': attributes.get('name'),
            'display_name': attributes.get('displayName'),
            'parent_folder_id': file_data.get('relationships', {}).get('parent', {}).get('data', {}).get('id'),
            'folder_path': folder_path,
            'full_path': f"{folder_path}/{attributes.get('name')}".strip('/'),
            'path_segments': f"{folder_path}/{attributes.get('name')}".strip('/').split('/'),
            'depth': depth,
            'create_time': attributes.get('createTime'),
            'create_user_id': attributes.get('createUserId'),
            'create_user_name': attributes.get('createUserName'),
            'last_modified_time': attributes.get('lastModifiedTime'),
            'last_modified_user_id': attributes.get('lastModifiedUserId'),
            'last_modified_user_name': attributes.get('lastModifiedUserName'),
            'file_type': attributes.get('extension'),
            'mime_type': attributes.get('mimeType'),
            'reserved': attributes.get('reserved', False),
            'hidden': attributes.get('hidden', False),
            'metadata': attributes.get('extension', {}),
            'file_permissions': {},  # V2新字段
            'file_settings': {},     # V2新字段
            'review_info': {},       # V2新字段
            'sync_info': {'synced_at': datetime.now().isoformat()}
        }
        
        # 批量转换时间戳字段为中国时区
        timestamp_fields = ['create_time', 'last_modified_time']
        return self._batch_convert_timestamps_to_china(file_record, timestamp_fields)
    
    async def _batch_insert_folders_v2(self, folders_data: List[Dict], dal) -> int:
        """批量插入文件夹 - V2架构"""
        if not folders_data:
            return 0
        
        try:
            result = await dal.batch_upsert_folders(folders_data)
            return result.get('upserted', 0)
        except Exception as e:
            logger.error(f"V2 folder batch insert failed: {e}")
            return 0
    
    async def _batch_insert_files_v2(self, files_data: List[Dict], dal) -> int:
        """批量插入文件 - V2架构"""
        if not files_data:
            return 0
        
        try:
            result = await dal.batch_upsert_files(files_data)
            return result.get('upserted', 0)
        except Exception as e:
            logger.error(f"V2 file batch insert failed: {e}")
            return 0
    
    async def _batch_insert_file_versions_v2(self, files_data: List[Dict], dal) -> int:
        """批量插入文件版本 - V2架构"""
        if not files_data:
            return 0
        
        try:
            # 为每个文件创建版本记录
            versions_data = []
            for file_data in files_data:
                versions_info = file_data.get('versions_info', [])
                
                # 处理文件版本信息
                
                if versions_info:
                    # 处理从API获取的真实版本信息
                    for i, version in enumerate(versions_info):
                        version_attrs = version.get('attributes', {})
                        detailed_attrs = version.get('detailed_attributes', {})
                        
                        # 基础版本数据
                        version_data = {
                            'id': version.get('id'),
                            'file_id': file_data.get('id'),
                            'project_id': file_data.get('project_id'),
                            'version_number': version_attrs.get('versionNumber', i + 1),
                            'urn': version.get('id'),
                            'item_urn': version.get('relationships', {}).get('item', {}).get('data', {}).get('id'),
                            'storage_urn': detailed_attrs.get('storageUrn'),
                            'lineage_urn': version_attrs.get('lineageUrn'),
                            'create_time': version_attrs.get('createTime'),
                            'create_user_id': version_attrs.get('createUserId'),
                            'create_user_name': version_attrs.get('createUserName'),
                            'last_modified_time': version_attrs.get('lastModifiedTime'),
                            'last_modified_user_id': version_attrs.get('lastModifiedUserId'),
                            'last_modified_user_name': version_attrs.get('lastModifiedUserName'),
                            'file_size': version_attrs.get('storageSize', 0),
                            'storage_size': detailed_attrs.get('storageSize', 0),
                            'mime_type': detailed_attrs.get('mimeType') or version_attrs.get('fileType'),
                            'process_state': detailed_attrs.get('processState'),
                            'download_url': detailed_attrs.get('downloadUrl'),
                            'is_current_version': i == 0,  # 第一个版本是最新版本
                            'version_status': 'active',
                            'metadata': version_attrs.get('extension', {}),
                            'review_info': {},
                            'extension': version_attrs.get('extension', {}),
                            'download_info': {'downloadUrl': detailed_attrs.get('downloadUrl')},
                            'sync_info': {'synced_at': datetime.now().isoformat()}
                        }
                        
                        # 转换时间戳字段为中国时区
                        timestamp_fields = ['create_time', 'last_modified_time']
                        version_data = self._batch_convert_timestamps_to_china(version_data, timestamp_fields)
                        versions_data.append(version_data)
                else:
                    # 如果没有版本信息，创建默认版本
                    version_data = {
                        'id': f"{file_data.get('id')}_v1",
                        'file_id': file_data.get('id'),
                        'project_id': file_data.get('project_id'),
                        'version_number': 1,
                        'urn': f"{file_data.get('id')}_v1",
                        'create_time': file_data.get('create_time'),
                        'create_user_id': file_data.get('create_user_id'),
                        'create_user_name': file_data.get('create_user_name'),
                        'last_modified_time': file_data.get('last_modified_time'),
                        'last_modified_user_id': file_data.get('last_modified_user_id'),
                        'last_modified_user_name': file_data.get('last_modified_user_name'),
                        'mime_type': file_data.get('mime_type'),
                        'is_current_version': True,
                        'version_status': 'active',
                        'metadata': file_data.get('metadata', {}),
                        'review_info': file_data.get('review_info', {}),
                        'sync_info': file_data.get('sync_info', {})
                    }
                    
                    # 转换时间戳字段为中国时区
                    timestamp_fields = ['create_time', 'last_modified_time']
                    version_data = self._batch_convert_timestamps_to_china(version_data, timestamp_fields)
                    versions_data.append(version_data)
            
            if versions_data:
                result = await dal.batch_upsert_file_versions(versions_data)
                logger.info(f"File versions sync completed: {result.get('upserted', 0)} versions")
                return result.get('upserted', 0)
            else:
                return 0
        except Exception as e:
            logger.error(f"V2 file versions batch insert failed: {e}")
            return 0
    
    async def _batch_insert_custom_attributes_v2(self, files_data: List[Dict], dal) -> int:
        """批量插入自定义属性 - V2架构"""
        if not files_data:
            return 0
        
        try:
            custom_attrs_definitions = []
            custom_attrs_values = []
            
            # 从文件数据中提取自定义属性
            for file_data in files_data:
                custom_attrs_info = file_data.get('custom_attributes')
                
                # 处理自定义属性信息
                
                if custom_attrs_info and custom_attrs_info.get('customAttributes'):
                    custom_attrs = custom_attrs_info.get('customAttributes', [])
                    
                    for attr in custom_attrs:
                        # 属性定义 - 清理编码问题并添加V2字段
                        attr_def = {
                            'attr_id': attr.get('id'),
                            'project_id': file_data.get('project_id'),
                            'name': str(attr.get('name', '')).encode('ascii', errors='ignore').decode('ascii') if attr.get('name') else '',
                            'type': attr.get('type'),
                            'array_values': attr.get('arrayValues', []),
                            'description': str(attr.get('description', '')).encode('ascii', errors='ignore').decode('ascii') if attr.get('description') else None,
                            'is_required': attr.get('isRequired', False),
                            'default_value': str(attr.get('defaultValue', '')).encode('ascii', errors='ignore').decode('ascii') if attr.get('defaultValue') else None,
                            'scope_type': 'project',  # V2 field
                            'scope_folder_id': None,  # V2 field
                            'inherit_to_subfolders': True,  # V2 field
                            'validation_rules': {},  # V2 field
                            'sync_info': {'synced_at': datetime.now().isoformat()}
                        }
                        custom_attrs_definitions.append(attr_def)
                        
                        # 属性值 - 使用V2字段映射
                        attr_value = {
                            'file_id': file_data.get('id'),
                            'attr_definition_id': attr.get('id'),  # V2 field (renamed from attr_id)
                            'project_id': file_data.get('project_id'),
                            'value': str(attr.get('value', '')).encode('ascii', errors='ignore').decode('ascii') if attr.get('value') else None,
                            'value_date': self._parse_date_value(attr) if attr.get('type') == 'date' else None,
                            'value_number': self._parse_number_value(attr) if attr.get('type') == 'number' else None,
                            'value_boolean': self._parse_boolean_value(attr) if attr.get('type') == 'boolean' else None,
                            'value_array': attr.get('arrayValues') if attr.get('type') == 'array' else None,  # V2 field
                            'validation_status': 'valid',  # V2 field
                            'validation_errors': [],  # V2 field
                            'updated_at': datetime.now(),
                            'sync_info': {'synced_at': datetime.now().isoformat()}
                        }
                        custom_attrs_values.append(attr_value)
            
            total_synced = 0
            
            logger.info(f"Found {len(custom_attrs_definitions)} attribute definitions and {len(custom_attrs_values)} attribute values")
            
            # 插入属性定义并获取ID映射
            attr_id_mapping = {}  # ACC API attr_id -> database definition id
            if custom_attrs_definitions:
                # 去重属性定义
                unique_definitions = self._deduplicate_definitions(custom_attrs_definitions)
                def_result = await dal.batch_upsert_custom_attribute_definitions(unique_definitions)
                logger.info(f"Custom attribute definitions sync completed: {def_result.get('upserted', 0)} definitions")
                
                # 获取属性定义的ID映射
                attr_id_mapping = await self._get_attr_definition_id_mapping(unique_definitions, dal)
                logger.info(f"Retrieved {len(attr_id_mapping)} attribute ID mappings")
            
            # 更新属性值中的attr_definition_id并插入
            if custom_attrs_values and attr_id_mapping:
                # 更新属性值中的attr_definition_id
                for attr_value in custom_attrs_values:
                    acc_attr_id = attr_value.get('attr_definition_id')  # 这是ACC API的ID
                    db_definition_id = attr_id_mapping.get(acc_attr_id)
                    if db_definition_id:
                        attr_value['attr_definition_id'] = db_definition_id
                    else:
                        logger.warning(f"No database ID found for ACC attribute ID: {acc_attr_id}")
                
                # 过滤掉没有有效attr_definition_id的值
                valid_values = [v for v in custom_attrs_values if v.get('attr_definition_id')]
                logger.info(f"Processing {len(valid_values)} valid attribute values out of {len(custom_attrs_values)}")
                
                if valid_values:
                    value_result = await dal.batch_upsert_custom_attribute_values(valid_values)
                    total_synced = value_result.get('upserted', 0)
                    logger.info(f"Custom attribute values sync completed: {total_synced} values")
            elif custom_attrs_values and not attr_id_mapping:
                logger.warning(f"Found {len(custom_attrs_values)} attribute values but no ID mappings available")
            
            return total_synced
            
        except Exception as e:
            logger.error(f"V2 custom attributes batch insert failed: {str(e).encode('ascii', errors='ignore').decode('ascii')}")
            return 0
    
    async def _batch_get_file_versions_and_custom_attrs_v2(self, project_id: str, 
                                                         changed_files: List[Dict[str, Any]], 
                                                         headers: dict) -> List[Dict[str, Any]]:
        """批量获取文件版本和自定义属性 - V2版本"""
        
        if not changed_files:
            return []
        
        logger.info(f"Batch retrieving file details: {len(changed_files)} files")
        
        try:
            # 🔑 批量获取文件版本详细信息（参考V1实现）
            file_ids = [file_data['id'] for file_data in changed_files]
            
            # 分批处理版本信息获取
            batch_size = 10  # 版本API并发限制更严格
            all_file_metadata = []
            
            # 并发获取版本信息
            try:
                import aiohttp
                
                async with aiohttp.ClientSession() as session:
                    # 分批处理文件
                    for i in range(0, len(changed_files), batch_size):
                        batch_files = changed_files[i:i + batch_size]
                        
                        # 并发获取当前批次的版本信息
                        tasks = []
                        for file_data in batch_files:
                            file_id = file_data.get('id')
                            if file_id:
                                task = self._get_file_versions_async(session, project_id, file_id, headers)
                                tasks.append((file_data, task))
                        
                        # 等待当前批次完成
                        for file_data, task in tasks:
                            try:
                                versions_info = await task
                                # 将版本信息合并到文件数据中
                                file_data['versions_info'] = versions_info
                                all_file_metadata.append(file_data)
                                
                                self.stats['api_calls'] += 1
                            except Exception as e:
                                logger.warning(f"获取文件版本失败 {file_data.get('id')}: {e}")
                                # 即使版本获取失败，也保留基本文件信息
                                file_data['versions_info'] = []
                                all_file_metadata.append(file_data)
                        
                        # API节流
                        if i + batch_size < len(changed_files):
                            await asyncio.sleep(self.api_delay)
                        
                        self.stats['batch_operations'] += 1
                        
            except ImportError:
                logger.warning("aiohttp not available, using basic file metadata")
                all_file_metadata = changed_files
            
            # 🔑 批量获取自定义属性
            version_urns = []
            file_to_version_map = {}
            
            for file_metadata in all_file_metadata:
                # 从versions_info中获取版本URN
                versions_info = file_metadata.get('versions_info', [])
                if versions_info:
                    version_urn = versions_info[0].get('id')  # 使用最新版本
                    if version_urn:
                        version_urns.append(version_urn)
                        file_to_version_map[version_urn] = file_metadata.get('id')
            
            custom_attributes_data = []
            if version_urns:
                # 分批获取自定义属性 (API限制50个)
                for i in range(0, len(version_urns), batch_size):
                    batch_urns = version_urns[i:i + batch_size]
                    
                    async with self.api_semaphore:
                        # 调用实际的Custom Attributes API
                        custom_attrs_batch = await self._call_custom_attributes_api(project_id, batch_urns, headers)
                        
                        custom_attributes_data.extend(custom_attrs_batch)
                        self.stats['api_calls'] += 1
                        self.stats['batch_operations'] += 1
            
            # 合并文件元数据、版本信息和自定义属性
            enriched_files = []
            for file_metadata in all_file_metadata:
                # 查找对应的自定义属性
                file_id = file_metadata.get('id')
                versions_info = file_metadata.get('versions_info', [])
                
                # 从自定义属性API获取额外信息
                custom_attrs_info = None
                if versions_info:
                    version_urn = versions_info[0].get('id')
                    custom_attrs_info = next(
                        (attr for attr in custom_attributes_data if attr.get('urn') == version_urn),
                        None
                    )
                
                # 合并所有信息到文件数据中
                enriched_file = file_metadata.copy()
                enriched_file['custom_attributes'] = custom_attrs_info
                
                # 如果文件名为空，尝试从自定义属性中获取
                if not enriched_file.get('name') and custom_attrs_info:
                    enriched_file['name'] = custom_attrs_info.get('name') or custom_attrs_info.get('title')
                
                enriched_files.append(enriched_file)
            
            logger.info(f"File details retrieval completed: {len(enriched_files)} files")
            return enriched_files
            
        except Exception as e:
            logger.error(f"Batch file details retrieval failed: {e}")
            return changed_files  # 返回基本信息
    
    async def _get_folder_custom_attr_definitions_v2(self, project_id: str, folder_id: str,
                                                     headers: dict, session) -> List[Dict]:
        """获取单个文件夹的自定义属性定义 - V2版本"""
        import urllib.parse

        definitions = []

        try:
            # Remove 'b.' prefix for BIM360 API
            bim360_project_id = project_id.replace('b.', '') if project_id.startswith('b.') else project_id

            # URL encode folder ID
            encoded_folder_id = urllib.parse.quote(folder_id, safe='')

            url = f"https://developer.api.autodesk.com/bim360/docs/v1/projects/{bim360_project_id}/folders/{encoded_folder_id}/custom-attribute-definitions"

            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    self.stats['api_calls'] += 1

                    results = data.get('results', [])
                    for definition in results:
                        attr_def = {
                            'attr_id': definition.get('id'),
                            'project_id': project_id,
                            'scope_type': 'folder',
                            'scope_folder_id': folder_id,
                            'name': definition.get('name'),
                            'type': definition.get('type'),
                            'array_values': definition.get('arrayValues', []),
                            'description': None,
                            'is_required': False,
                            'default_value': None,
                            'inherit_to_subfolders': False
                        }
                        definitions.append(attr_def)

                elif response.status == 404:
                    # 文件夹没有自定义属性定义是正常的
                    pass
                else:
                    logger.debug(f"Failed to get custom attr definitions for folder {folder_id}: {response.status}")

        except Exception as e:
            logger.warning(f"Error getting custom attr definitions for folder {folder_id}: {e}")

        return definitions

    async def _collect_custom_attributes_v2(self, project_id: str, headers: dict, session) -> Dict:
        """收集自定义属性 - V2版本"""
        # 文件夹自定义属性已在BFS遍历中收集
        # 这里可以收集其他类型的自定义属性（如项目级别的）
        return {'definitions': [], 'values': []}
    
    async def _update_project_sync_status(self, project_id: str, dal):
        """更新项目同步状态"""
        try:
            async with dal.get_connection() as conn:
                await conn.execute("""
                    INSERT INTO projects (id, name, last_sync_time, last_full_sync_time, sync_status)
                    VALUES ($1, $2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'completed')
                    ON CONFLICT (id) DO UPDATE SET
                        last_sync_time = CURRENT_TIMESTAMP,
                        last_full_sync_time = CURRENT_TIMESTAMP,
                        sync_status = 'completed',
                        updated_at = CURRENT_TIMESTAMP
                """, project_id, f"Project {project_id}")
        except Exception as e:
            logger.error(f"更新项目同步状态失败: {e}")
    
    def _parse_date_value(self, attr: Dict[str, Any]) -> Optional[datetime]:
        """解析日期类型属性值"""
        if attr.get('type') == 'date' and attr.get('value'):
            return self._parse_datetime(attr['value'])
        return None
    
    def _parse_number_value(self, attr: Dict[str, Any]) -> Optional[float]:
        """解析数值类型属性值"""
        if attr.get('type') == 'number' and attr.get('value') is not None:
            try:
                return float(attr['value'])
            except (ValueError, TypeError):
                return None
        return None
    
    def _parse_boolean_value(self, attr: Dict[str, Any]) -> Optional[bool]:
        """解析布尔类型属性值"""
        if attr.get('type') == 'boolean' and attr.get('value') is not None:
            value = attr['value']
            if isinstance(value, bool):
                return value
            elif isinstance(value, str):
                return value.lower() in ('true', '1', 'yes', 'on')
            elif isinstance(value, (int, float)):
                return bool(value)
        return None

# 全局优化同步管理器实例
optimized_postgresql_sync_manager = OptimizedPostgreSQLSyncManager(
    batch_size=100,
    api_delay=0.02,
    max_workers=8
)
