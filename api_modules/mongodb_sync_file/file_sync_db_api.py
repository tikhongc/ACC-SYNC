# -*- coding: utf-8 -*-
"""
文件同步数据库API模块
专门处理文件数据的数据库同步功能，支持全量同步和增量同步
"""

import time
import logging
from datetime import datetime, timezone, timedelta
import pytz
from flask import Blueprint, jsonify, request
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict, deque
from typing import Dict, List, Tuple, Any

import config
import utils
from database.data_access_layer import DataAccessLayer
from database.incremental_sync import IncrementalSyncManager
from database.data_sync_strategy import DataTransformer

# 統一的中國時區定義
CHINA_TZ = pytz.timezone('Asia/Shanghai')

# ============================================================================
# 統一時間處理工具函數
# ============================================================================

def get_china_time():
    """獲取當前中國時間"""
    return datetime.now(CHINA_TZ)

def parse_api_datetime(datetime_str):
    """解析API返回的日期時間字符串，統一轉換為中國時區"""
    if not datetime_str:
        return None
    
    try:
        # ACC API通常返回ISO格式的時間戳
        if datetime_str.endswith('Z'):
            # UTC時間戳，轉換為中國時區
            dt = datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
            return dt.astimezone(CHINA_TZ)
        else:
            # 嘗試直接解析
            dt = datetime.fromisoformat(datetime_str)
            # 如果沒有時區信息，假設為UTC並轉換為中國時區
            if dt.tzinfo is None:
                dt = pytz.utc.localize(dt)
            return dt.astimezone(CHINA_TZ)
    except Exception as e:
        logger.warning(f"解析日期時間失敗: {datetime_str}, {str(e)}")
        return None

def normalize_db_datetime(dt):
    """標準化數據庫中的日期時間，統一轉換為中國時區"""
    if not dt:
        return None
    
    try:
        # 使用timestamp進行轉換，避免時區比較問題
        if hasattr(dt, 'timestamp'):
            # 如果有timestamp方法，使用它
            timestamp = dt.timestamp()
        elif hasattr(dt, 'tzinfo') and dt.tzinfo is not None:
            # 有時區信息的datetime
            timestamp = dt.timestamp()
        else:
            # 沒有時區信息，假設為UTC
            utc_dt = pytz.utc.localize(dt)
            timestamp = utc_dt.timestamp()
        
        # 從timestamp創建中國時區的datetime
        return datetime.fromtimestamp(timestamp, CHINA_TZ)
        
    except Exception as e:
        logger.warning(f"標準化日期時間失敗: {dt}, 類型: {type(dt)}, 錯誤: {str(e)}")
        try:
            # 嘗試替代方案：直接使用pytz轉換
            if hasattr(dt, 'tzinfo'):
                if dt.tzinfo is None:
                    return pytz.utc.localize(dt).astimezone(CHINA_TZ)
                else:
                    return dt.astimezone(CHINA_TZ)
            else:
                # MongoDB datetime對象
                return pytz.utc.localize(dt).astimezone(CHINA_TZ)
        except Exception as e2:
            logger.error(f"所有時間轉換方法都失敗: {dt}, 錯誤1: {str(e)}, 錯誤2: {str(e2)}")
            # 最後的fallback：返回當前中國時間
            return get_china_time()

def format_china_time(dt):
    """格式化中國時間顯示"""
    if not dt:
        return None
    
    # 確保是中國時區
    if hasattr(dt, 'tzinfo') and dt.tzinfo != CHINA_TZ:
        dt = dt.astimezone(CHINA_TZ)
    
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def debug_datetime_object(dt, name="datetime"):
    """調試日期時間對象的詳細信息"""
    if dt is None:
        logger.debug(f"🔍 {name}: None")
        return
    
    logger.debug(f"🔍 {name} 詳細信息:")
    logger.debug(f"   類型: {type(dt)}")
    logger.debug(f"   值: {dt}")
    logger.debug(f"   字符串表示: {str(dt)}")
    logger.debug(f"   repr: {repr(dt)}")
    
    if hasattr(dt, 'tzinfo'):
        logger.debug(f"   tzinfo: {dt.tzinfo}")
        logger.debug(f"   tzinfo類型: {type(dt.tzinfo)}")
        if dt.tzinfo:
            logger.debug(f"   tzinfo名稱: {getattr(dt.tzinfo, 'zone', 'Unknown')}")
    else:
        logger.debug(f"   沒有tzinfo屬性")
    
    if hasattr(dt, 'timestamp'):
        try:
            logger.debug(f"   timestamp: {dt.timestamp()}")
        except Exception as e:
            logger.debug(f"   timestamp錯誤: {e}")
    
    # 嘗試轉換為不同格式
    try:
        logger.debug(f"   isoformat: {dt.isoformat()}")
    except Exception as e:
        logger.debug(f"   isoformat錯誤: {e}")
        
    logger.debug(f"   ---")

from .file_sync_api import (
    get_project_top_folders, 
    get_folder_contents, 
    get_item_versions,
    batch_get_files_custom_attributes,
    get_folder_custom_attribute_definitions
)

# 创建Blueprint
file_sync_db_bp = Blueprint('file_sync_db', __name__)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileSyncDatabaseManager:
    """文件同步数据库管理器"""
    
    def __init__(self):
        self.dal = DataAccessLayer()
        self.sync_manager = IncrementalSyncManager(self.dal)
        self.converter = DataTransformer()
        
    def full_sync_project(self, project_id: str, max_depth: int = 10, 
                         include_custom_attributes: bool = True) -> dict:
        """
        项目全量同步到数据库
        
        Args:
            project_id: 项目ID
            max_depth: 最大遍历深度
            include_custom_attributes: 是否包含自定义属性
            
        Returns:
            同步结果字典
        """
        start_time = time.time()
        
        try:
            # 1. 创建同步任务记录
            task_id = self._create_sync_task(project_id, "full_sync", {
                "max_depth": max_depth,
                "include_custom_attributes": include_custom_attributes
            })
            
            # 2. 🧹 清除項目現有數據（全量同步的關鍵步驟）
            logger.info(f"🧹 全量同步第一步：清除項目 {project_id} 的現有數據")
            clear_stats = self.dal.clear_project_data(project_id)
            logger.info(f"數據清理完成: {clear_stats}")
            
            # 3. 获取API访问令牌
            access_token = utils.get_access_token()
            if not access_token:
                raise Exception("无法获取访问令牌")
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # 4. 获取项目顶级文件夹（带重试机制）
            logger.info(f"開始重新同步項目: {project_id}")
            
            # 增强的重试机制
            max_retries = 5
            retry_delay = 3
            top_folders_data = None
            
            for attempt in range(max_retries):
                try:
                    logger.info(f"尝试获取顶级文件夹 (第 {attempt + 1}/{max_retries} 次)")
                    top_folders_data = get_project_top_folders(project_id, headers)
                    
                    if top_folders_data and top_folders_data.get('data'):
                        logger.info(f"✅ 成功获取顶级文件夹 (尝试 {attempt + 1})")
                        break
                    else:
                        logger.warning(f"⚠️ 获取到空的顶级文件夹数据 (尝试 {attempt + 1})")
                        if attempt < max_retries - 1:
                            logger.info(f"等待 {retry_delay} 秒后重试...")
                            time.sleep(retry_delay)
                            retry_delay *= 1.5  # 递增延迟
                            continue
                        
                except Exception as e:
                    logger.error(f"❌ 获取顶级文件夹失败 (尝试 {attempt + 1}): {str(e)}")
                    if attempt < max_retries - 1:
                        logger.info(f"等待 {retry_delay} 秒后重试...")
                        time.sleep(retry_delay)
                        retry_delay *= 1.5
                        continue
                    else:
                        raise Exception(f"经过 {max_retries} 次重试后仍无法获取项目顶级文件夹: {str(e)}")
            
            if not top_folders_data or not top_folders_data.get('data'):
                raise Exception(f"经过 {max_retries} 次重试后仍无法获取有效的项目顶级文件夹数据")
            
            # 5. 初始化项目记录
            project_data = DataTransformer.transform_project_data({
                "id": project_id,
                "attributes": {
                    "name": f"Project {project_id}"
                }
            })
            
            self.dal.create_or_update_project(project_data)
            
            # 6. 递归同步所有文件夹和文件
            sync_results = {
                "folders_synced": 0,
                "files_synced": 0,
                "versions_synced": 0,
                "errors": [],
                "total_size": 0
            }
            
            for top_folder in top_folders_data.get('data', []):
                folder_result = self._sync_folder_recursive(
                    project_id, top_folder, headers, 
                    max_depth, 0, include_custom_attributes, None
                )
                
                sync_results["folders_synced"] += folder_result["folders_synced"]
                sync_results["files_synced"] += folder_result["files_synced"]
                sync_results["versions_synced"] += folder_result["versions_synced"]
                sync_results["total_size"] += folder_result["total_size"]
                sync_results["errors"].extend(folder_result["errors"])
            
            # 7. 更新项目统计信息
            duration = time.time() - start_time
            self._update_project_statistics(project_id, sync_results, duration)
            
            # 8. 完成同步任务
            self._complete_sync_task(task_id, sync_results, duration)
            
            logger.info(f"全量同步完成: {sync_results}")
            return {
                "success": True,
                "task_id": task_id,
                "duration_seconds": duration,
                "results": sync_results
            }
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"全量同步失败: {str(e)}")
            
            # 更新失败状态
            if 'task_id' in locals():
                self._fail_sync_task(task_id, str(e), duration)
            
            return {
                "success": False,
                "error": str(e),
                "duration_seconds": duration
            }
    
    def incremental_sync_project(self, project_id: str) -> dict:
        """
        项目增量同步到数据库
        
        Args:
            project_id: 项目ID
            
        Returns:
            同步结果字典
        """
        start_time = time.time()
        
        try:
            # 1. 获取上次同步时间
            last_sync_time = self.sync_manager.get_last_sync_time(project_id)
            logger.info(f"开始增量同步项目: {project_id}, 上次同步: {last_sync_time}")
            
            # 2. 检测变更
            changes = self.sync_manager.detect_changes(project_id, last_sync_time)
            
            if not any(changes.values()):
                logger.info("没有检测到变更，跳过同步")
                return {
                    "success": True,
                    "message": "没有变更需要同步",
                    "changes": changes
                }
            
            # 3. 创建增量同步任务
            task_id = self._create_sync_task(project_id, "incremental_sync", {
                "since": last_sync_time.isoformat(),
                "detected_changes": changes
            })
            
            # 4. 执行增量同步
            access_token = utils.get_access_token()
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            sync_results = self.sync_manager.incremental_sync_folders(
                project_id, changes["new_folders"] + changes["updated_folders"], headers
            )
            
            file_results = self.sync_manager.incremental_sync_files(
                project_id, changes["new_files"] + changes["updated_files"], headers
            )
            
            # 5. 合并结果
            total_results = {
                "folders_synced": sync_results.get("new", 0) + sync_results.get("updated", 0),
                "files_synced": file_results.get("new", 0) + file_results.get("updated", 0), 
                "versions_synced": 0,  # 增量同步暂不支持版本同步
                "errors": []  # 简化错误处理
            }
            
            # 6. 完成任务
            duration = time.time() - start_time
            self._complete_sync_task(task_id, total_results, duration)
            
            logger.info(f"增量同步完成: {total_results}")
            return {
                "success": True,
                "task_id": task_id,
                "duration_seconds": duration,
                "changes": changes,
                "results": total_results
            }
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"增量同步失败: {str(e)}")
            
            if 'task_id' in locals():
                self._fail_sync_task(task_id, str(e), duration)
            
            return {
                "success": False,
                "error": str(e),
                "duration_seconds": duration
            }
    
    def _sync_folder_recursive(self, project_id: str, folder_data: dict, headers: dict,
                              max_depth: int, current_depth: int, 
                              include_custom_attributes: bool, parent_path: str) -> dict:
        """递归同步文件夹"""
        
        if current_depth >= max_depth:
            return {"folders_synced": 0, "files_synced": 0, "versions_synced": 0, "errors": [], "total_size": 0}
        
        try:
            folder_id = folder_data.get('id')
            folder_attributes = folder_data.get('attributes', {})
            
            # 构建路径信息
            folder_name = folder_attributes.get('displayName', folder_attributes.get('name', 'Unknown'))
            current_path = f"{parent_path}/{folder_name}" if parent_path else folder_name
            
            logger.info(f"同步文件夹: {folder_name} (深度: {current_depth})")
            
            # 转换文件夹数据
            # 正确的参数: api_data, project_id, parent_id=None, path="", depth=0
            parent_folder_id = folder_data.get('relationships', {}).get('parent', {}).get('data', {}).get('id') if parent_path else None
            folder_doc = DataTransformer.transform_folder_data(
                folder_data, project_id, parent_folder_id, parent_path or "", current_depth
            )
            
            # 获取自定义属性定义（带错误处理）
            if include_custom_attributes:
                try:
                    custom_attrs = get_folder_custom_attribute_definitions(project_id, folder_id)
                    if custom_attrs:
                        folder_doc["custom_attribute_definitions"] = custom_attrs
                except Exception as e:
                    logger.warning(f"获取文件夹自定义属性失败 {folder_name}: {str(e)}")
            
            # 保存文件夹到数据库
            self.dal.create_or_update_folder(folder_doc)
            
            results = {"folders_synced": 1, "files_synced": 0, "versions_synced": 0, "errors": [], "total_size": 0}
            
            # 获取文件夹内容（带重试机制）
            max_retries = 3
            contents_data = None
            
            for attempt in range(max_retries):
                try:
                    contents_data = get_folder_contents(project_id, folder_id, headers)
                    if contents_data:
                        break
                except Exception as e:
                    logger.warning(f"获取文件夹内容失败 {folder_name} (尝试 {attempt + 1}): {str(e)}")
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)  # 指数退避
                        continue
                    else:
                        logger.error(f"获取文件夹内容最终失败 {folder_name}: {str(e)}")
                        results["errors"].append({
                            "folder_id": folder_id,
                            "error": f"无法获取文件夹内容: {str(e)}"
                        })
                        return results
            
            if not contents_data:
                logger.warning(f"文件夹内容为空: {folder_name}")
                return results
            
            # 分离文件夹和文件
            subfolders = []
            files = []
            
            for item in contents_data.get('data', []):
                if item.get('type') == 'folders':
                    subfolders.append(item)
                else:
                    files.append(item)
            
            # 递归处理子文件夹
            for subfolder in subfolders:
                subfolder_result = self._sync_folder_recursive(
                    project_id, subfolder, headers, max_depth, 
                    current_depth + 1, include_custom_attributes, current_path
                )
                
                results["folders_synced"] += subfolder_result["folders_synced"]
                results["files_synced"] += subfolder_result["files_synced"]
                results["versions_synced"] += subfolder_result["versions_synced"]
                results["total_size"] += subfolder_result["total_size"]
                results["errors"].extend(subfolder_result["errors"])
            
            # 批量处理文件
            if files:
                file_result = self._sync_files_batch(
                    project_id, files, headers, folder_id, current_path, include_custom_attributes, current_depth
                )
                
                results["files_synced"] += file_result["files_synced"]
                results["versions_synced"] += file_result["versions_synced"]
                results["total_size"] += file_result["total_size"]
                results["errors"].extend(file_result["errors"])
            
            return results
            
        except Exception as e:
            logger.error(f"同步文件夹失败 {folder_data.get('id', 'unknown')}: {str(e)}")
            return {
                "folders_synced": 0, "files_synced": 0, "versions_synced": 0, 
                "errors": [{"folder_id": folder_data.get('id'), "error": str(e)}],
                "total_size": 0
            }
    
    def _sync_files_batch(self, project_id: str, files: list, headers: dict,
                         parent_folder_id: str, folder_path: str, 
                         include_custom_attributes: bool, current_depth: int = 0) -> dict:
        """批量同步文件"""
        
        results = {"files_synced": 0, "versions_synced": 0, "total_size": 0, "errors": []}
        
        try:
            # 批量获取文件版本
            file_ids = [f.get('id') for f in files if f.get('id')]
            
            # 并行获取版本信息
            versions_data = {}
            with ThreadPoolExecutor(max_workers=5) as executor:
                future_to_file = {
                    executor.submit(get_item_versions, project_id, file_id, headers): file_id
                    for file_id in file_ids
                }
                
                for future in as_completed(future_to_file):
                    file_id = future_to_file[future]
                    try:
                        versions = future.result()
                        versions_data[file_id] = versions
                    except Exception as e:
                        logger.error(f"获取文件版本失败 {file_id}: {str(e)}")
                        results["errors"].append({"file_id": file_id, "error": str(e)})
            
            # 批量获取自定义属性
            custom_attributes_data = {}
            if include_custom_attributes:
                # 创建临时文件节点用于自定义属性获取
                temp_file_nodes = []
                for file_data in files:
                    file_id = file_data.get('id')
                    if file_id in versions_data:
                        temp_node = type('FileNode', (), {
                            'versions': versions_data[file_id],
                            'name': file_data.get('attributes', {}).get('displayName', 'Unknown')
                        })()
                        temp_file_nodes.append(temp_node)
                
                if temp_file_nodes:
                    custom_attributes_data = batch_get_files_custom_attributes(project_id, temp_file_nodes)
            
            # 处理每个文件
            for file_data in files:
                try:
                    file_id = file_data.get('id')
                    versions = versions_data.get(file_id, [])
                    
                    # 转换文件数据
                    # 正确的参数: api_data, project_id, parent_folder_id, folder_path, depth=0
                    file_doc = DataTransformer.transform_file_data(
                        file_data, project_id, parent_folder_id, folder_path, current_depth
                    )
                    
                    # 添加自定义属性
                    if include_custom_attributes and versions:
                        latest_version = versions[0]
                        version_id = latest_version.get('id')
                        if version_id in custom_attributes_data:
                            file_doc["custom_attributes"] = custom_attributes_data[version_id]
                    
                    # 保存文件到数据库
                    self.dal.create_or_update_file(file_doc)
                    results["files_synced"] += 1
                    
                    # 保存文件版本
                    for version in versions:
                        version_doc = {
                            "_id": version.get("id"),
                            "file_id": file_id,
                            "project_id": project_id,
                            "urn": version.get("id"),
                            "version_number": version.get("attributes", {}).get("versionNumber", 1),
                            "display_name": version.get("attributes", {}).get("displayName", ""),
                            "file_size": version.get("attributes", {}).get("storageSize", 0),
                            "created_at": datetime.now(),
                            "updated_at": datetime.now()
                        }
                        self.dal.create_or_update_file_version(version_doc)
                        results["versions_synced"] += 1
                    
                    # 累计文件大小 - 修复total_size计算问题
                    if versions:
                        latest_version = versions[0]
                        # 从版本数据的attributes.storageSize获取文件大小
                        file_size = (
                            latest_version.get('attributes', {}).get('storageSize', 0) or
                            latest_version.get('attributes', {}).get('fileSize', 0) or
                            0
                        )
                        if file_size and file_size > 0:
                            results["total_size"] += file_size
                            logger.debug(f"文件 {file_data.get('id')} 大小: {file_size} bytes")
                    
                except Exception as e:
                    logger.error(f"同步文件失败 {file_data.get('id', 'unknown')}: {str(e)}")
                    results["errors"].append({
                        "file_id": file_data.get('id'),
                        "error": str(e)
                    })
            
            return results
            
        except Exception as e:
            logger.error(f"批量同步文件失败: {str(e)}")
            return {
                "files_synced": 0, "versions_synced": 0, "total_size": 0,
                "errors": [{"error": f"批量同步失败: {str(e)}"}]
            }
    
    def _create_sync_task(self, project_id: str, task_type: str, parameters: dict) -> str:
        """创建同步任务记录"""
        task_data = {
            "project_id": project_id,
            "task_type": task_type,
            "task_status": "running",
            "parameters": parameters,
            "progress": {
                "total_items": 0,
                "processed_items": 0,
                "success_count": 0,
                "error_count": 0,
                "current_stage": "initializing",
                "progress_percentage": 0.0
            },
            "start_time": datetime.now()
        }
        
        return self.dal.create_sync_task(task_data)
    
    def _complete_sync_task(self, task_id: str, results: dict, duration: float):
        """完成同步任务"""
        self.dal.update_sync_task_status(task_id, "completed", results, duration)
    
    def _record_successful_sync(self, project_id: str, sync_type: str, results: dict, duration: float):
        """记录成功的同步到简化的历史记录"""
        try:
            # 添加持续时间到结果中
            results_with_duration = results.copy()
            results_with_duration["duration_seconds"] = duration
            
            # 创建简化的同步历史记录
            success = self.dal.create_sync_history_record(project_id, sync_type, results_with_duration)
            if success:
                logger.info(f"成功记录同步历史: {project_id} - {sync_type}")
            else:
                logger.warning(f"记录同步历史失败: {project_id} - {sync_type}")
                
        except Exception as e:
            logger.error(f"记录同步历史时出错: {str(e)}")
    
    def _fail_sync_task(self, task_id: str, error: str, duration: float):
        """标记同步任务失败"""
        results = {"error": error}
        self.dal.update_sync_task_status(task_id, "failed", results, duration)
    
    def _update_project_statistics(self, project_id: str, sync_results: dict, duration: float):
        """更新项目统计信息"""
        stats = {
            "total_folders": sync_results["folders_synced"],
            "total_files": sync_results["files_synced"],
            "total_size_bytes": sync_results["total_size"],
            "last_calculated": datetime.now()
        }
        
        self.dal.update_project_sync_status(project_id, "success", duration)
        self.dal.update_project_statistics(project_id, stats)


# 全局管理器实例
sync_manager = FileSyncDatabaseManager()


# ============================================================================
# 批量优化同步管理器
# ============================================================================

class BatchOptimizedSyncManager:
    """批量优化的同步管理器 - 专注于metadata同步性能优化"""
    
    def __init__(self, batch_size: int = 100, api_delay: float = 0.2):
        self.dal = DataAccessLayer()
        self.batch_size = batch_size
        self.api_delay = api_delay  # API调用间隔，避免速率限制
        self.converter = DataTransformer()
        
    def batch_sync_project(self, project_id: str, max_depth: int = 10, 
                          include_custom_attributes: bool = True, task_id: str = None,
                          is_full_sync: bool = False) -> dict:
        """
        批量优化的项目同步
        
        核心优化策略：
        1. 广度优先遍历，避免深度递归
        2. 批量API调用，减少网络开销
        3. 批量数据库操作，提升写入性能
        4. 智能API节流，避免速率限制
        
        Args:
            project_id: 項目ID
            max_depth: 最大遍歷深度
            include_custom_attributes: 是否包含自定義屬性
            task_id: 任務ID
            is_full_sync: 是否為全量同步（會先清除現有數據）
        """
        start_time = time.time()
        
        try:
            # 1. 创建或使用现有同步任务记录
            if task_id is None:
                sync_type = "full_sync" if is_full_sync else "batch_optimized_sync"
                task_id = self._create_sync_task(project_id, sync_type, {
                    "max_depth": max_depth,
                    "include_custom_attributes": include_custom_attributes,
                    "batch_size": self.batch_size,
                    "is_full_sync": is_full_sync
                })
            
            # 2. 🧹 如果是全量同步，先清除項目現有數據
            if is_full_sync:
                logger.info(f"🧹 全量同步模式：清除項目 {project_id} 的現有數據")
                clear_stats = self.dal.clear_project_data(project_id)
                logger.info(f"數據清理完成: {clear_stats}")
            
            # 3. 获取API访问令牌
            access_token = utils.get_access_token()
            if not access_token:
                raise Exception("无法获取访问令牌")
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # 3. 获取顶级文件夹
            logger.info(f"开始批量优化同步项目: {project_id}")
            top_folders_data = self._get_top_folders_with_retry(project_id, headers)
            
            # 4. 批量收集所有项目metadata
            self._update_sync_task_progress(task_id, {
                "current_stage": "collecting",
                "progress_percentage": 50.0,  # 收集阶段内部进度
                "processed_items": 0,
                "total_items": 0
            })
            
            all_folders, all_files = self._collect_all_items_bfs(
                project_id, top_folders_data['data'], headers, max_depth, task_id
            )
            
            # 更新收集完成，开始文件夹处理
            self._update_sync_task_progress(task_id, {
                "current_stage": "processing_folders",
                "progress_percentage": 0.0,  # 文件夹处理阶段开始
                "processed_items": 0,
                "total_items": len(all_folders) + len(all_files),
                "total_folders": len(all_folders),
                "total_files": len(all_files)
            })
            
            # 5. 批量处理文件夹（按层级顺序）
            folder_results = self._batch_process_folders(
                all_folders, project_id, include_custom_attributes, headers, task_id
            )
            
            # 6. 批量处理文件
            self._update_sync_task_progress(task_id, {
                "current_stage": "processing_files",
                "progress_percentage": 0.0,  # 文件处理阶段开始
                "folders_processed": folder_results["success_count"],
                "files_processed": 0,
                "total_items": len(all_folders) + len(all_files)
            })
            
            file_results = self._batch_process_files(
                all_files, project_id, include_custom_attributes, headers, task_id
            )
            
            # 7. 合并结果
            sync_results = {
                "folders_synced": folder_results["success_count"],
                "files_synced": file_results["files_synced"],
                "versions_synced": file_results["versions_synced"],
                "total_size": file_results["total_size"],
                "errors": folder_results["errors"] + file_results["errors"]
            }
            
            # 8. 完成同步
            self._update_sync_task_progress(task_id, {
                "current_stage": "finalizing",
                "progress_percentage": 100.0,  # 最终化阶段完成
                "folders_processed": folder_results["success_count"],
                "files_processed": file_results["files_synced"],
                "versions_processed": file_results["versions_synced"],
                "total_items": len(all_folders) + len(all_files)
            })
            
            duration = time.time() - start_time
            self._update_project_statistics(project_id, sync_results, duration)
            self._complete_sync_task(task_id, sync_results, duration)
            
            # 通知任務追蹤系統任務完成
            try:
                from api_modules.task_lifecycle_manager import task_manager
                task_manager.complete_task(task_id, sync_results)
            except ImportError:
                logger.warning("Task tracking system not available")
            
            logger.info(f"批量优化同步完成: {sync_results}")
            return {
                "success": True,
                "task_id": task_id,
                "duration_seconds": duration,
                "results": sync_results
            }
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"批量优化同步失败: {str(e)}")
            
            if 'task_id' in locals():
                self._fail_sync_task(task_id, str(e), duration)
                # 通知任務追蹤系統任務失敗
                try:
                    from api_modules.task_lifecycle_manager import task_manager
                    task_manager.fail_task(task_id, str(e))
                except ImportError:
                    logger.warning("Task tracking system not available")
            
            return {
                "success": False,
                "error": str(e),
                "duration_seconds": duration
            }
    
    def _collect_all_items_bfs(self, project_id: str, top_folders: List[dict], 
                              headers: dict, max_depth: int, task_id: str = None) -> Tuple[List, List]:
        """
        广度优先收集所有项目metadata
        
        优势：
        - 避免递归调用栈问题
        - 可以预先知道总量，便于进度追踪
        - 减少API调用的嵌套复杂度
        """
        all_folders = []
        all_files = []
        
        # 使用队列进行广度优先遍历
        # 队列元素: (folder_data, depth, parent_path)
        folder_queue = deque()
        
        # 初始化队列
        for folder in top_folders:
            folder_queue.append((folder, 0, ""))
        
        processed_folders = 0
        total_api_calls = 0
        
        while folder_queue:
            folder_data, depth, parent_path = folder_queue.popleft()
            
            if depth >= max_depth:
                continue
            
            folder_id = folder_data.get('id')
            folder_name = folder_data.get('attributes', {}).get('displayName', 'Unknown')
            current_path = f"{parent_path}/{folder_name}" if parent_path else folder_name
            
            # 添加到文件夹列表（带层级信息）
            all_folders.append((folder_data, depth, parent_path))
            
            # API节流 - 关键优化点
            if total_api_calls > 0 and total_api_calls % 10 == 0:
                logger.info(f"API节流暂停 {self.api_delay} 秒 (已调用 {total_api_calls} 次)")
                time.sleep(self.api_delay)
            
            try:
                # 获取文件夹内容
                logger.info(f"收集文件夹内容: {folder_name} (深度: {depth})")
                contents_data = get_folder_contents(project_id, folder_id, headers)
                total_api_calls += 1
                
                if not contents_data or not contents_data.get('data'):
                    continue
                
                # 分离文件夹和文件
                for item in contents_data['data']:
                    item_type = item.get('type')
                    
                    if item_type == 'folders':
                        # 添加子文件夹到队列
                        folder_queue.append((item, depth + 1, current_path))
                    else:
                        # 添加文件到列表（带上下文信息）
                        all_files.append((item, folder_id, current_path, depth))
                
                processed_folders += 1
                
                # 进度日志和数据库更新
                if processed_folders % 10 == 0:
                    logger.info(f"已收集 {processed_folders} 个文件夹, {len(all_files)} 个文件")
                    
                    # 更新收集进度到数据库
                    if task_id:
                        # 估算收集进度（基于已处理的文件夹数量）
                        estimated_total = max(len(top_folders) * 5, processed_folders + len(folder_queue))
                        collect_progress = min((processed_folders / estimated_total) * 100, 90)
                        
                        self._update_sync_task_progress(task_id, {
                            "current_stage": "collecting",
                            "progress_percentage": collect_progress,
                            "processed_folders": processed_folders,
                            "collected_files": len(all_files),
                            "queue_remaining": len(folder_queue)
                        })
                
            except Exception as e:
                logger.error(f"收集文件夹内容失败 {folder_name}: {str(e)}")
                continue
        
        # 收集完成，更新最终进度
        if task_id:
            self._update_sync_task_progress(task_id, {
                "current_stage": "collecting",
                "progress_percentage": 100.0,
                "processed_folders": processed_folders,
                "collected_files": len(all_files),
                "total_folders_found": len(all_folders),
                "total_files_found": len(all_files)
            })
        
        logger.info(f"收集完成: {len(all_folders)} 个文件夹, {len(all_files)} 个文件, {total_api_calls} 次API调用")
        return all_folders, all_files
    
    def _batch_process_folders(self, folders_with_context: List[Tuple], project_id: str,
                              include_custom_attributes: bool, headers: dict, task_id: str) -> dict:
        """
        批量处理文件夹metadata
        
        关键优化：
        1. 按深度排序，确保父文件夹先处理
        2. 批量数据库操作
        3. 可选的自定义属性批量获取
        """
        results = {"success_count": 0, "errors": []}
        
        # 按深度排序，确保依赖关系正确
        folders_with_context.sort(key=lambda x: x[1])  # 按depth排序
        
        batch_docs = []
        processed_count = 0
        
        for folder_data, depth, parent_path in folders_with_context:
            try:
                # 转换文件夹数据
                parent_folder_id = folder_data.get('relationships', {}).get('parent', {}).get('data', {}).get('id') if parent_path else None
                folder_doc = DataTransformer.transform_folder_data(
                    folder_data, project_id, parent_folder_id, parent_path, depth
                )
                
                # 获取自定义属性（如果需要）
                if include_custom_attributes:
                    try:
                        folder_id = folder_data.get('id')
                        custom_attrs = get_folder_custom_attribute_definitions(project_id, folder_id)
                        if custom_attrs:
                            folder_doc["custom_attribute_definitions"] = custom_attrs
                        
                        # API节流
                        time.sleep(self.api_delay * 0.5)  # 自定义属性调用频率更低
                        
                    except Exception as e:
                        logger.warning(f"获取文件夹自定义属性失败: {str(e)}")
                
                batch_docs.append(folder_doc)
                processed_count += 1
                
                # 批量处理
                if len(batch_docs) >= self.batch_size:
                    batch_result = self._batch_upsert_folders(batch_docs)
                    results["success_count"] += batch_result["success_count"]
                    results["errors"].extend(batch_result["errors"])
                    batch_docs = []
                    
                    # 更新任务进度
                    folder_progress = (processed_count / len(folders_with_context)) * 100
                    self._update_sync_task_progress(task_id, {
                        "folders_processed": processed_count,
                        "current_stage": "processing_folders",
                        "progress_percentage": folder_progress,
                        "total_folders": len(folders_with_context)
                    })
                
            except Exception as e:
                logger.error(f"处理文件夹失败: {str(e)}")
                results["errors"].append({
                    "folder_id": folder_data.get('id'),
                    "error": str(e)
                })
        
        # 处理剩余的文件夹
        if batch_docs:
            batch_result = self._batch_upsert_folders(batch_docs)
            results["success_count"] += batch_result["success_count"]
            results["errors"].extend(batch_result["errors"])
        
        logger.info(f"文件夹批量处理完成: 成功 {results['success_count']}, 错误 {len(results['errors'])}")
        return results
    
    def _batch_process_files(self, files_with_context: List[Tuple], project_id: str,
                            include_custom_attributes: bool, headers: dict, task_id: str) -> dict:
        """
        批量处理文件metadata
        
        关键优化：
        1. 按文件夹分组，批量获取自定义属性
        2. 批量数据库操作
        3. 版本信息一并处理
        """
        results = {
            "files_synced": 0, "versions_synced": 0, 
            "total_size": 0, "errors": []
        }
        
        # 按文件夹分组，便于批量处理
        files_by_folder = defaultdict(list)
        for file_data, folder_id, folder_path, depth in files_with_context:
            files_by_folder[folder_id].append((file_data, folder_path, depth))
        
        processed_folders = 0
        total_folders = len(files_by_folder)
        
        for folder_id, files_in_folder in files_by_folder.items():
            try:
                # 批量获取自定义属性
                custom_attrs_data = {}
                if include_custom_attributes and files_in_folder:
                    version_ids = [f[0].get('id') for f in files_in_folder if f[0].get('id')]
                    
                    if version_ids:
                        # 分批获取，避免URL过长
                        total_batches = (len(version_ids) + 19) // 20  # 向上取整
                        for i in range(0, len(version_ids), 20):
                            batch_ids = version_ids[i:i + 20]
                            current_batch = i // 20 + 1
                            
                            try:
                                # 报告自定义属性处理进度
                                attrs_progress = (current_batch / total_batches) * 100
                                self._update_sync_task_progress(task_id, {
                                    "current_stage": "processing_attributes",
                                    "progress_percentage": attrs_progress,
                                    "processed_attribute_batches": current_batch,
                                    "total_attribute_batches": total_batches,
                                    "current_folder": folder_id
                                })
                                
                                # 使用自定义属性API直接调用
                                from .custom_attributes_api import CustomAttributesAPI
                                custom_attrs_api = CustomAttributesAPI()
                                attrs_result = custom_attrs_api.get_file_custom_attributes(project_id, batch_ids)
                                
                                if attrs_result and attrs_result.get('results'):
                                    custom_attrs_data.update(attrs_result['results'])
                                
                                # API节流
                                time.sleep(self.api_delay)
                                
                            except Exception as e:
                                logger.warning(f"批量获取自定义属性失败: {str(e)}")
                
                # 批量转换文件数据
                file_docs = []
                version_docs = []
                
                for file_data, folder_path, depth in files_in_folder:
                    try:
                        # 转换文件数据
                        file_doc = DataTransformer.transform_file_data(
                            file_data, project_id, folder_id, folder_path, depth
                        )
                        
                        # 添加自定义属性
                        version_id = file_data.get('id')
                        if version_id in custom_attrs_data:
                            file_doc['custom_attributes'] = custom_attrs_data[version_id].get('customAttributes', {})
                            file_doc['has_custom_attributes'] = custom_attrs_data[version_id].get('hasCustomAttributes', False)
                        
                        file_docs.append(file_doc)
                        
                        # 转换版本数据
                        version_doc = DataTransformer.transform_version_data(
                            file_data, file_doc['_id'], project_id
                        )
                        version_docs.append(version_doc)
                        
                        # 累计文件大小 - 修复total_size计算问题
                        # 文件大小信息在version_doc的metadata中
                        storage_size = version_doc.get('metadata', {}).get('file_size', 0)
                        
                        if storage_size and storage_size > 0:
                            results["total_size"] += storage_size
                            logger.debug(f"文件 {file_data.get('id')} 大小: {storage_size} bytes")
                        else:
                            logger.debug(f"文件 {file_data.get('id')} 大小为0或未找到")
                        
                    except Exception as e:
                        logger.error(f"转换文件数据失败: {str(e)}")
                        results["errors"].append({
                            "file_id": file_data.get('id'),
                            "error": str(e)
                        })
                
                # 批量数据库操作
                if file_docs:
                    # 批量插入文件
                    file_batch_result = self.dal.batch_upsert_files(file_docs)
                    results["files_synced"] += file_batch_result["inserted"] + file_batch_result["updated"]
                    
                    # 批量插入版本
                    version_batch_result = self._batch_upsert_versions(version_docs)
                    results["versions_synced"] += version_batch_result["success_count"]
                    results["errors"].extend(version_batch_result["errors"])
                
                processed_folders += 1
                
                # 更新进度
                if processed_folders % 5 == 0 or processed_folders == total_folders:
                    progress_percentage = (processed_folders / total_folders) * 100
                    logger.info(f"文件处理进度: {processed_folders}/{total_folders} ({progress_percentage:.1f}%)")
                    
                    self._update_sync_task_progress(task_id, {
                        "files_processed": results["files_synced"],
                        "current_stage": "processing_files",
                        "progress_percentage": progress_percentage,
                        "total_file_folders": total_folders,
                        "processed_file_folders": processed_folders
                    })
                
            except Exception as e:
                logger.error(f"批量处理文件夹 {folder_id} 失败: {str(e)}")
                results["errors"].append({
                    "folder_id": folder_id,
                    "error": str(e)
                })
        
        logger.info(f"文件批量处理完成: 文件 {results['files_synced']}, 版本 {results['versions_synced']}, 大小 {results['total_size']} bytes")
        return results
    
    def _batch_upsert_folders(self, folder_docs: List[Dict]) -> dict:
        """批量插入文件夹"""
        results = {"success_count": 0, "errors": []}
        
        try:
            for folder_doc in folder_docs:
                if self.dal.create_or_update_folder(folder_doc):
                    results["success_count"] += 1
                else:
                    results["errors"].append({
                        "folder_id": folder_doc.get('_id'),
                        "error": "数据库操作失败"
                    })
        except Exception as e:
            logger.error(f"批量文件夹操作失败: {str(e)}")
            results["errors"].append({"error": str(e)})
        
        return results
    
    def _batch_upsert_versions(self, version_docs: List[Dict]) -> dict:
        """批量插入版本"""
        results = {"success_count": 0, "errors": []}
        
        try:
            for version_doc in version_docs:
                if self.dal.create_or_update_file_version(version_doc):
                    results["success_count"] += 1
                else:
                    results["errors"].append({
                        "version_id": version_doc.get('_id'),
                        "error": "数据库操作失败"
                    })
        except Exception as e:
            logger.error(f"批量版本操作失败: {str(e)}")
            results["errors"].append({"error": str(e)})
        
        return results
    
    # 复用现有的辅助方法
    def _create_sync_task(self, project_id: str, task_type: str, parameters: dict) -> str:
        """创建同步任务记录"""
        return sync_manager._create_sync_task(project_id, task_type, parameters)
    
    def _get_top_folders_with_retry(self, project_id: str, headers: dict):
        """获取顶级文件夹（带重试）"""
        # 增强的重试机制
        max_retries = 5
        retry_delay = 3
        top_folders_data = None
        
        for attempt in range(max_retries):
            try:
                logger.info(f"尝试获取顶级文件夹 (第 {attempt + 1}/{max_retries} 次)")
                top_folders_data = get_project_top_folders(project_id, headers)
                if top_folders_data and top_folders_data.get('data'):
                    logger.info(f"✅ 成功获取顶级文件夹 (尝试 {attempt + 1})")
                    break
                else:
                    logger.warning(f"⚠️ 获取到空的顶级文件夹数据 (尝试 {attempt + 1})")
                    if attempt < max_retries - 1:
                        logger.info(f"等待 {retry_delay} 秒后重试...")
                        time.sleep(retry_delay)
                        retry_delay *= 1.5
                        continue
            except Exception as e:
                logger.error(f"❌ 获取顶级文件夹失败 (尝试 {attempt + 1}): {str(e)}")
                if attempt < max_retries - 1:
                    logger.info(f"等待 {retry_delay} 秒后重试...")
                    time.sleep(retry_delay)
                    retry_delay *= 1.5
                    continue
                else:
                    raise Exception(f"经过 {max_retries} 次重试后仍无法获取项目顶级文件夹: {str(e)}")
        
        if not top_folders_data or not top_folders_data.get('data'):
            raise Exception(f"经过 {max_retries} 次重试后仍无法获取有效的项目顶级文件夹数据")
        
        return top_folders_data
    
    def _update_project_statistics(self, project_id: str, sync_results: dict, duration: float):
        """更新项目统计"""
        return sync_manager._update_project_statistics(project_id, sync_results, duration)
    
    def _complete_sync_task(self, task_id: str, results: dict, duration: float):
        """完成同步任务"""
        return sync_manager._complete_sync_task(task_id, results, duration)
    
    def _fail_sync_task(self, task_id: str, error: str, duration: float):
        """标记任务失败"""
        return sync_manager._fail_sync_task(task_id, error, duration)
    
    def _update_sync_task_progress(self, task_id: str, progress_data: dict):
        """更新同步任务进度（使用獨立任務追蹤系統）"""
        try:
            from api_modules.task_lifecycle_manager import task_manager
            task_manager.update_task(task_id, progress_data)
        except ImportError:
            logger.warning("Task tracking system not available")
        except Exception as e:
            logger.warning(f"更新任务进度失败: {str(e)}")

# ============================================================================
# 增量同步管理器
# ============================================================================

class IncrementalSyncManager:
    """真正的增量同步管理器 - 基於ACC API的lastModifiedTime對比"""
    
    def __init__(self, batch_size: int = 100, api_delay: float = 0.2):
        self.dal = DataAccessLayer()
        self.batch_size = batch_size
        self.api_delay = api_delay
        self.converter = DataTransformer()
    
    def incremental_sync_project(self, project_id: str, max_depth: int = 10, 
                                include_custom_attributes: bool = True, task_id: str = None) -> dict:
        """
        執行真正的增量同步
        
        核心邏輯：
        1. 獲取上次同步時間
        2. 遍歷ACC API獲取所有項目
        3. 對比每個項目的lastModifiedTime與上次同步時間
        4. 只同步有變更的項目
        """
        start_time = time.time()
        
        try:
            # 1. 獲取上次同步時間
            last_sync_time = self._get_last_sync_time(project_id)
            logger.info(f"🔄 開始增量同步項目: {project_id}, 上次同步時間: {last_sync_time}")
            
            # 2. 獲取API訪問令牌
            access_token = utils.get_access_token()
            if not access_token:
                raise Exception("无法获取访问令牌")
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # 3. 獲取項目頂級文件夾
            top_folders_data = self._get_top_folders_with_retry(project_id, headers)
            
            # 4. 收集所有項目並檢查變更
            self._update_sync_task_progress(task_id, {
                "current_stage": "checking_changes",
                "progress_percentage": 10.0,
                "message": "檢查項目變更..."
            })
            
            changed_folders, changed_files = self._collect_changed_items(
                project_id, top_folders_data['data'], headers, max_depth, last_sync_time, task_id
            )
            
            # 5. 如果沒有變更，直接返回
            if not changed_folders and not changed_files:
                logger.info("📋 沒有檢測到變更，跳過同步")
                return {
                    "success": True,
                    "message": "沒有變更需要同步",
                    "results": {
                        "folders_synced": 0,
                        "files_synced": 0,
                        "versions_synced": 0,
                        "total_size": 0,
                        "errors": []
                    }
                }
            
            logger.info(f"📊 檢測到變更: {len(changed_folders)} 個文件夾, {len(changed_files)} 個文件")
            
            # 6. 同步變更的項目
            self._update_sync_task_progress(task_id, {
                "current_stage": "syncing_changes",
                "progress_percentage": 30.0,
                "changed_folders": len(changed_folders),
                "changed_files": len(changed_files)
            })
            
            sync_results = self._sync_changed_items(
                project_id, changed_folders, changed_files, headers, include_custom_attributes, task_id
            )
            
            # 7. 更新項目同步時間
            duration = time.time() - start_time
            self._update_project_sync_time(project_id, duration)
            
            logger.info(f"✅ 增量同步完成: {sync_results}")
            return {
                "success": True,
                "duration_seconds": duration,
                "results": sync_results
            }
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"❌ 增量同步失敗: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "duration_seconds": duration
            }
    
    def _get_last_sync_time(self, project_id: str):
        """獲取上次同步時間，統一使用中國時區"""
        try:
            db = self.dal.connect()
            project = db.projects.find_one({"_id": project_id})
            
            if project and project.get("sync_info") and project["sync_info"].get("last_sync_time"):
                last_sync = project["sync_info"]["last_sync_time"]
                # 使用統一的時間標準化函數
                return normalize_db_datetime(last_sync)
            
            # 如果沒有記錄，返回7天前（中國時區）
            return get_china_time() - timedelta(days=7)
            
        except Exception as e:
            logger.error(f"獲取上次同步時間失敗: {str(e)}")
            return get_china_time() - timedelta(days=7)
    
    def _get_top_folders_with_retry(self, project_id: str, headers: dict):
        """獲取頂級文件夾（帶重試）"""
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                from .file_sync_api import get_project_top_folders
                top_folders_data = get_project_top_folders(project_id, headers)
                
                if top_folders_data and top_folders_data.get('data'):
                    return top_folders_data
                    
            except Exception as e:
                logger.warning(f"獲取頂級文件夾失敗 (嘗試 {attempt + 1}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                else:
                    raise Exception(f"經過 {max_retries} 次重試後仍無法獲取項目頂級文件夾")
        
        raise Exception("無法獲取有效的項目頂級文件夾數據")
    
    def _collect_changed_items(self, project_id: str, top_folders: List[dict], 
                              headers: dict, max_depth: int, last_sync_time, task_id: str = None):
        """收集有變更的項目"""
        from collections import deque
        
        # 強制轉換基準時間為中國時區，避免時區比較問題
        try:
            if last_sync_time:
                # 使用timestamp方式確保時區統一
                if hasattr(last_sync_time, 'timestamp'):
                    timestamp = last_sync_time.timestamp()
                    last_sync_time = datetime.fromtimestamp(timestamp, CHINA_TZ)
                else:
                    # 如果沒有timestamp方法，嘗試其他方式
                    last_sync_time = normalize_db_datetime(last_sync_time)
                
                logger.info(f"🕐 增量同步基準時間（中國時區）: {format_china_time(last_sync_time)}")
            else:
                logger.warning("⚠️ 沒有基準時間，使用7天前")
                last_sync_time = get_china_time() - timedelta(days=7)
                
        except Exception as e:
            logger.error(f"❌ 基準時間轉換失敗: {str(e)}")
            logger.error(f"   原始時間: {last_sync_time}, 類型: {type(last_sync_time)}")
            # 使用fallback時間
            last_sync_time = get_china_time() - timedelta(days=7)
            logger.info(f"🕐 使用fallback基準時間: {format_china_time(last_sync_time)}")
        
        changed_folders = []
        changed_files = []
        
        # 使用隊列進行廣度優先遍歷
        folder_queue = deque()
        
        # 初始化隊列
        for folder in top_folders:
            folder_queue.append((folder, 0, ""))
        
        processed_folders = 0
        total_api_calls = 0
        
        while folder_queue:
            folder_data, depth, parent_path = folder_queue.popleft()
            
            if depth >= max_depth:
                continue
            
            folder_id = folder_data.get('id')
            folder_name = folder_data.get('attributes', {}).get('displayName', 'Unknown')
            current_path = f"{parent_path}/{folder_name}" if parent_path else folder_name
            
            # 檢查文件夾是否有變更
            folder_last_modified = self._parse_datetime(folder_data.get('attributes', {}).get('lastModifiedTime'))
            
            if folder_last_modified and last_sync_time:
                try:
                    # 使用timestamp進行數值比較，完全避免時區問題
                    api_timestamp = self._get_timestamp(folder_last_modified)
                    base_timestamp = self._get_timestamp(last_sync_time)
                    
                    if api_timestamp and base_timestamp and api_timestamp > base_timestamp:
                        changed_folders.append((folder_data, depth, parent_path))
                        logger.info(f"📁 文件夾有變更: {folder_name} (API:{api_timestamp} > 基準:{base_timestamp})")
                        
                except Exception as e:
                    logger.error(f"❌ 時間戳比較失敗: {folder_name}, {str(e)}")
                    # 如果時間戳比較失敗，假設有變更（保守策略）
                    changed_folders.append((folder_data, depth, parent_path))
                    logger.warning(f"⚠️ 時間戳比較失敗，假設文件夾有變更: {folder_name}")
            
            # API節流
            if total_api_calls > 0 and total_api_calls % 10 == 0:
                time.sleep(self.api_delay)
            
            try:
                # 獲取文件夾內容
                from .file_sync_api import get_folder_contents
                contents_data = get_folder_contents(project_id, folder_id, headers)
                total_api_calls += 1
                
                if not contents_data or not contents_data.get('data'):
                    continue
                
                # 分離文件夾和文件
                for item in contents_data['data']:
                    item_type = item.get('type')
                    item_last_modified = self._parse_datetime(item.get('attributes', {}).get('lastModifiedTime'))
                    
                    if item_type == 'folders':
                        # 添加子文件夾到隊列
                        folder_queue.append((item, depth + 1, current_path))
                    else:
                        # 檢查文件是否有變更
                        if item_last_modified and last_sync_time:
                            try:
                                # 使用timestamp進行數值比較
                                file_timestamp = self._get_timestamp(item_last_modified)
                                base_timestamp = self._get_timestamp(last_sync_time)
                                
                                if file_timestamp and base_timestamp and file_timestamp > base_timestamp:
                                    changed_files.append((item, folder_id, current_path, depth))
                                    logger.debug(f"📄 文件有變更: {item.get('attributes', {}).get('displayName', 'Unknown')} (時間戳:{file_timestamp} > {base_timestamp})")
                            except Exception as e:
                                logger.error(f"❌ 文件時間戳比較失敗: {item.get('attributes', {}).get('displayName', 'Unknown')}, {str(e)}")
                                # 保守策略：假設有變更
                                changed_files.append((item, folder_id, current_path, depth))
                
                processed_folders += 1
                
                # 更新進度
                if processed_folders % 10 == 0 and task_id:
                    self._update_sync_task_progress(task_id, {
                        "current_stage": "checking_changes",
                        "progress_percentage": min(10 + (processed_folders / max(len(top_folders) * 5, 1)) * 20, 30),
                        "processed_folders": processed_folders,
                        "changed_folders": len(changed_folders),
                        "changed_files": len(changed_files)
                    })
                
            except Exception as e:
                logger.error(f"檢查文件夾內容失敗 {folder_name}: {str(e)}")
                continue
        
        return changed_folders, changed_files
    
    def _parse_datetime(self, datetime_str):
        """解析日期時間字符串，統一轉換為中國時區"""
        return parse_api_datetime(datetime_str)
    
    def _get_timestamp(self, dt):
        """獲取datetime對象的timestamp，避免時區比較問題"""
        if not dt:
            return None
        
        try:
            # 如果有timestamp方法，直接使用
            if hasattr(dt, 'timestamp'):
                return dt.timestamp()
            
            # 如果沒有時區信息，假設為UTC
            if hasattr(dt, 'tzinfo') and dt.tzinfo is None:
                utc_dt = pytz.utc.localize(dt)
                return utc_dt.timestamp()
            
            # 如果有時區信息，轉換為UTC後獲取timestamp
            if hasattr(dt, 'tzinfo') and dt.tzinfo is not None:
                return dt.timestamp()
            
            # MongoDB datetime對象處理
            utc_dt = pytz.utc.localize(dt)
            return utc_dt.timestamp()
            
        except Exception as e:
            logger.warning(f"獲取timestamp失敗: {dt}, 錯誤: {str(e)}")
            return None
    
    def _sync_changed_items(self, project_id: str, changed_folders: List, changed_files: List, 
                           headers: dict, include_custom_attributes: bool, task_id: str = None):
        """同步有變更的項目"""
        sync_results = {
            "folders_synced": 0,
            "files_synced": 0,
            "versions_synced": 0,
            "total_size": 0,
            "errors": []
        }
        
        # 同步文件夾
        for i, (folder_data, depth, parent_path) in enumerate(changed_folders):
            try:
                folder_db_data = self.converter.transform_folder_data(
                    folder_data, project_id, parent_path
                )
                
                if self.dal.create_or_update_folder(folder_db_data):
                    sync_results["folders_synced"] += 1
                
                # 更新進度
                if task_id and i % 5 == 0:
                    progress = 30 + (i / len(changed_folders)) * 30
                    self._update_sync_task_progress(task_id, {
                        "current_stage": "syncing_folders",
                        "progress_percentage": progress,
                        "folders_processed": i + 1
                    })
                    
            except Exception as e:
                error_msg = f"同步文件夾失敗: {folder_data.get('attributes', {}).get('displayName', 'Unknown')}: {str(e)}"
                logger.error(error_msg)
                sync_results["errors"].append(error_msg)
        
        # 同步文件
        for i, (file_data, parent_folder_id, folder_path, depth) in enumerate(changed_files):
            try:
                file_db_data = self.converter.transform_file_data(
                    file_data, project_id, parent_folder_id, folder_path
                )
                
                if self.dal.create_or_update_file(file_db_data):
                    sync_results["files_synced"] += 1
                
                # 獲取文件版本
                try:
                    from .file_sync_api import get_item_versions
                    versions = get_item_versions(project_id, file_data.get('id'), headers)
                    
                    for version in versions:
                        version_db_data = self.converter.transform_version_data(
                            version, file_data.get('id'), project_id
                        )
                        
                        if self.dal.create_or_update_file_version(version_db_data):
                            sync_results["versions_synced"] += 1
                            sync_results["total_size"] += version_db_data.get("file_info", {}).get("size", 0)
                            
                except Exception as ve:
                    logger.warning(f"獲取文件版本失敗: {str(ve)}")
                
                # 更新進度
                if task_id and i % 5 == 0:
                    progress = 60 + (i / len(changed_files)) * 30
                    self._update_sync_task_progress(task_id, {
                        "current_stage": "syncing_files",
                        "progress_percentage": progress,
                        "files_processed": i + 1
                    })
                    
            except Exception as e:
                error_msg = f"同步文件失敗: {file_data.get('attributes', {}).get('displayName', 'Unknown')}: {str(e)}"
                logger.error(error_msg)
                sync_results["errors"].append(error_msg)
        
        return sync_results
    
    def _update_project_sync_time(self, project_id: str, duration: float):
        """更新項目同步時間"""
        try:
            from datetime import datetime
            self.dal.update_project_sync_status(
                project_id, 
                "completed", 
                duration=duration
            )
        except Exception as e:
            logger.error(f"更新項目同步時間失敗: {str(e)}")
    
    def _update_sync_task_progress(self, task_id: str, progress_data: dict):
        """更新同步任務進度"""
        if not task_id:
            return
            
        try:
            # 更新任務追蹤系統
            from api_modules.task_lifecycle_manager import task_manager
            task_manager.update_task(task_id, progress_data)
        except ImportError:
            logger.warning("Task tracking system not available")
        except Exception as e:
            logger.warning(f"更新任務進度失敗: {str(e)}")

# 创建管理器实例
batch_sync_manager = BatchOptimizedSyncManager(batch_size=100, api_delay=0.2)
incremental_sync_manager = IncrementalSyncManager(batch_size=100, api_delay=0.2)


def _force_cleanup_running_tasks(project_id: str) -> dict:
    """
    强制清理项目的所有运行中任务
    """
    try:
        from datetime import datetime
        
        db = batch_sync_manager.dal.connect()
        
        # 直接取消所有running状态的任务
        result = db.sync_tasks.update_many(
            {
                'task_status': 'running',
                'project_id': project_id
            },
            {
                '$set': {
                    'task_status': 'cancelled',
                    'end_time': datetime.now(),
                    'updated_at': datetime.now(),
                    'results': {'error': '新同步启动，强制清理'}
                }
            }
        )
        
        return {
            "cancelled_count": result.modified_count,
            "message": f"强制取消了 {result.modified_count} 个运行中的任务"
        }
        
    except Exception as e:
        logger.error(f"强制清理任务失败: {str(e)}")
        return {
            "cancelled_count": 0,
            "message": f"清理失败: {str(e)}"
        }


# 舊的內存進度存儲已移除，現在使用獨立的任務追蹤系統


def _complete_task(task_id: str, results: dict):
    """完成任务并记录到简化的同步历史"""
    try:
        from datetime import datetime
        from database.data_access_layer import DataAccessLayer
        
        # 使用简化的同步记录
        dal = DataAccessLayer()
        project_id = results.get("project_id")
        duration = results.get("duration_seconds", 0)
        
        # 准备同步结果数据
        sync_results = {
            "folders_synced": results.get("folders_synced", 0),
            "files_synced": results.get("files_synced", 0),
            "versions_synced": results.get("versions_synced", 0),
            "total_size": results.get("total_size", 0),  # 修复total_size问题
            "duration_seconds": duration
        }
        
        # 只记录成功的同步到简化的历史记录
        success = dal.create_sync_history_record(project_id, "batch_sync", sync_results)
        
        if success:
            logger.info(f"✅ 成功记录批量同步历史: {project_id}")
        else:
            logger.warning(f"⚠️ 记录同步历史失败，但同步本身成功: {project_id}")
        
        # 任務完成邏輯已移至獨立的任務追蹤系統
            
        return success
        
    except Exception as e:
        logger.error(f"保存同步记录失败: {str(e)}")
        return False


def _fail_task(task_id: str, error_message: str):
    """標記任務失敗"""
    try:
        logger.error(f"❌ 任務失敗 {task_id}: {error_message}")
        # 任務失敗邏輯已移至獨立的任務追蹤系統
        return True
        
    except Exception as e:
        logger.error(f"標記任務失敗時出錯: {str(e)}")
        return False


def _auto_cleanup_old_tasks(project_id: str) -> dict:
    """
    自动清理项目的旧同步任务
    
    清理策略:
    1. 取消所有running状态但超过10分钟未更新的任务
    2. 取消所有running状态的重复任务（只保留最新的一个）
    3. 删除超过24小时的已完成/失败/取消任务
    
    Returns:
        dict: 清理结果统计
    """
    try:
        from datetime import datetime, timedelta
        
        db = batch_sync_manager.dal.connect()
        cleanup_stats = {
            "stuck_tasks_cancelled": 0,
            "duplicate_tasks_cancelled": 0, 
            "old_tasks_deleted": 0,
            "errors": []
        }
        
        # 1. 取消卡住的任务（超过10分钟未更新）
        cutoff_time = datetime.now() - timedelta(minutes=10)
        stuck_tasks = list(db.sync_tasks.find({
            'task_status': 'running',
            'project_id': project_id,
            'updated_at': {'$lt': cutoff_time}
        }))
        
        for task in stuck_tasks:
            try:
                updated_task = task.copy()
                updated_task['task_status'] = 'cancelled'
                updated_task['end_time'] = datetime.now()
                updated_task['updated_at'] = datetime.now()
                updated_task['results'] = {'error': '任务超时，自动清理'}
                
                result = db.sync_tasks.replace_one({'_id': task['_id']}, updated_task)
                if result.modified_count > 0:
                    cleanup_stats["stuck_tasks_cancelled"] += 1
                    logger.info(f"取消卡住任务: {task['_id']}")
            except Exception as e:
                cleanup_stats["errors"].append(f"取消卡住任务失败 {task['_id']}: {str(e)}")
        
        # 2. 处理重复的running任务（只保留最新的）
        running_tasks = list(db.sync_tasks.find({
            'task_status': 'running',
            'project_id': project_id
        }).sort('created_at', -1))
        
        if len(running_tasks) > 1:
            # 保留最新的，取消其他的
            for task in running_tasks[1:]:
                try:
                    updated_task = task.copy()
                    updated_task['task_status'] = 'cancelled'
                    updated_task['end_time'] = datetime.now()
                    updated_task['updated_at'] = datetime.now()
                    updated_task['results'] = {'error': '重复任务，自动清理'}
                    
                    result = db.sync_tasks.replace_one({'_id': task['_id']}, updated_task)
                    if result.modified_count > 0:
                        cleanup_stats["duplicate_tasks_cancelled"] += 1
                        logger.info(f"取消重复任务: {task['_id']}")
                except Exception as e:
                    cleanup_stats["errors"].append(f"取消重复任务失败 {task['_id']}: {str(e)}")
        
        # 3. 删除超过24小时的旧任务
        old_task_cutoff = datetime.now() - timedelta(hours=24)
        old_tasks_result = db.sync_tasks.delete_many({
            'project_id': project_id,
            'task_status': {'$in': ['completed', 'failed', 'cancelled']},
            'updated_at': {'$lt': old_task_cutoff}
        })
        cleanup_stats["old_tasks_deleted"] = old_tasks_result.deleted_count
        
        if cleanup_stats["old_tasks_deleted"] > 0:
            logger.info(f"删除 {cleanup_stats['old_tasks_deleted']} 个超过24小时的旧任务")
        
        return cleanup_stats
        
    except Exception as e:
        logger.error(f"自动清理任务失败: {str(e)}")
        return {
            "stuck_tasks_cancelled": 0,
            "duplicate_tasks_cancelled": 0,
            "old_tasks_deleted": 0,
            "errors": [f"清理失败: {str(e)}"]
        }


# ============================================================================
# API 端点
# ============================================================================

@file_sync_db_bp.route('/api/file-sync-db/project/<project_id>/sync', methods=['POST'])
def unified_sync_project_api(project_id):
    """
    統一的項目同步API
    
    POST /api/file-sync-db/project/{project_id}/sync
    
    参数:
    - syncType: 同步類型 ("full_sync" | "incremental_sync") (默认: "incremental_sync")
    - maxDepth: 最大遍历深度 (默认: 10)
    - includeCustomAttributes: 是否包含自定义属性 (默认: true)
    - batchSize: 批量处理大小 (默认: 100)
    - apiDelay: API调用间隔秒数 (默认: 0.2)
    """
    try:
        # 获取参数
        request_data = request.json or {}
        sync_type = request_data.get('syncType', 'incremental_sync')
        max_depth = request_data.get('maxDepth', 10)
        include_custom_attributes = request_data.get('includeCustomAttributes', True)
        batch_size = request_data.get('batchSize', 100)
        api_delay = request_data.get('apiDelay', 0.2)
        
        # 驗證同步類型
        if sync_type not in ['full_sync', 'incremental_sync']:
            return jsonify({
                "success": False,
                "error": f"無效的同步類型: {sync_type}，必須是 'full_sync' 或 'incremental_sync'"
            }), 400
        
        logger.info(f"開始{sync_type}項目 {project_id}: maxDepth={max_depth}, batchSize={batch_size}")
        
        # 🧹 强制清理该项目的所有运行中任务
        cleanup_result = _force_cleanup_running_tasks(project_id)
        logger.info(f"强制清理运行中任务: {cleanup_result}")
        
        # 生成任务ID
        import uuid
        task_id = str(uuid.uuid4())
        
        # 根據同步類型選擇執行方式
        if sync_type == 'full_sync':
            return _execute_full_sync(project_id, task_id, max_depth, include_custom_attributes, batch_size, api_delay)
        else:
            return _execute_incremental_sync(project_id, task_id, max_depth, include_custom_attributes, batch_size, api_delay)
            
    except Exception as e:
        logger.error(f"統一同步API失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"同步失败: {str(e)}"
        }), 500

def _execute_full_sync(project_id, task_id, max_depth, include_custom_attributes, batch_size, api_delay):
    """執行全量同步"""
    import threading
    
    def run_full_sync():
        try:
            from datetime import datetime
            start_time = datetime.now()
            
            # 註冊任務到追蹤系統
            try:
                from api_modules.task_lifecycle_manager import task_manager
                task_manager.register_task(task_id, {
                    "current_stage": "initializing",
                    "progress_percentage": 0.0,
                    "project_id": project_id,
                    "task_type": "full_sync"
                })
            except ImportError:
                logger.warning("Task tracking system not available")
            
            # 创建批量同步管理器並執行全量同步
            batch_manager = BatchOptimizedSyncManager(batch_size=batch_size, api_delay=api_delay)
            result = batch_manager.batch_sync_project(
                project_id, 
                max_depth=max_depth,
                include_custom_attributes=include_custom_attributes,
                task_id=task_id,
                is_full_sync=True  # 關鍵：啟用數據清理
            )
            
            # 计算耗时
            duration = (datetime.now() - start_time).total_seconds()
            
            # 完成任务并记录到数据库
            if result.get("success"):
                _complete_task(task_id, result.get("results", {}))
                # 通知任務追蹤系統任務完成
                try:
                    from api_modules.task_lifecycle_manager import task_manager
                    task_manager.complete_task(task_id, result.get("results", {}))
                except ImportError:
                    pass
            else:
                _fail_task(task_id, result.get("error", "Unknown error"))
                # 通知任務追蹤系統任務失敗
                try:
                    from api_modules.task_lifecycle_manager import task_manager
                    task_manager.fail_task(task_id, result.get("error", "Unknown error"))
                except ImportError:
                    pass
                    
        except Exception as e:
            logger.error(f"全量同步執行失敗: {str(e)}")
            _fail_task(task_id, str(e))
            try:
                from api_modules.task_lifecycle_manager import task_manager
                task_manager.fail_task(task_id, str(e))
            except ImportError:
                pass
    
    # 启动后台线程
    sync_thread = threading.Thread(target=run_full_sync)
    sync_thread.daemon = True
    sync_thread.start()
    
    return jsonify({
        "success": True,
        "message": "全量同步已启动",
        "data": {
            "task_id": task_id,
            "status": "running",
            "sync_type": "full_sync",
            "optimization_info": {
                "batch_size": batch_size,
                "api_delay": api_delay
            }
        }
    })

def _execute_incremental_sync(project_id, task_id, max_depth, include_custom_attributes, batch_size, api_delay):
    """執行增量同步"""
    import threading
    
    def run_incremental_sync():
        try:
            from datetime import datetime
            start_time = datetime.now()
            
            # 註冊任務到追蹤系統
            try:
                from api_modules.task_lifecycle_manager import task_manager
                task_manager.register_task(task_id, {
                    "current_stage": "initializing",
                    "progress_percentage": 0.0,
                    "project_id": project_id,
                    "task_type": "incremental_sync"
                })
            except ImportError:
                logger.warning("Task tracking system not available")
            
            # 創建增量同步管理器並執行真正的增量同步
            incremental_manager = IncrementalSyncManager(batch_size=batch_size, api_delay=api_delay)
            result = incremental_manager.incremental_sync_project(
                project_id, 
                max_depth=max_depth,
                include_custom_attributes=include_custom_attributes,
                task_id=task_id
            )
            
            # 计算耗时
            duration = (datetime.now() - start_time).total_seconds()
            
            # 完成任务并记录到数据库
            if result.get("success"):
                _complete_task(task_id, result.get("results", {}))
                try:
                    from api_modules.task_lifecycle_manager import task_manager
                    task_manager.complete_task(task_id, result.get("results", {}))
                except ImportError:
                    pass
            else:
                _fail_task(task_id, result.get("error", "Unknown error"))
                try:
                    from api_modules.task_lifecycle_manager import task_manager
                    task_manager.fail_task(task_id, result.get("error", "Unknown error"))
                except ImportError:
                    pass
                    
        except Exception as e:
            logger.error(f"增量同步執行失敗: {str(e)}")
            _fail_task(task_id, str(e))
            try:
                from api_modules.task_lifecycle_manager import task_manager
                task_manager.fail_task(task_id, str(e))
            except ImportError:
                pass
    
    # 启动后台线程
    sync_thread = threading.Thread(target=run_incremental_sync)
    sync_thread.daemon = True
    sync_thread.start()
    
    return jsonify({
        "success": True,
        "message": "增量同步已启动",
        "data": {
            "task_id": task_id,
            "status": "running",
            "sync_type": "incremental_sync",
            "optimization_info": {
                "batch_size": batch_size,
                "api_delay": api_delay
            }
        }
    })

# ============================================================================
# 舊的API端點（保留以便向後兼容，但標記為已棄用）
# ============================================================================

@file_sync_db_bp.route('/api/file-sync-db/project/<project_id>/full-sync', methods=['POST'])
def full_sync_project_api(project_id):
    """
    项目全量同步API (已棄用)
    
    ⚠️ DEPRECATED: 請使用 POST /api/file-sync-db/project/{project_id}/sync 
    並設置 syncType: "full_sync"
    
    POST /api/file-sync-db/project/{project_id}/full-sync
    
    参数:
    - maxDepth: 最大遍历深度 (默认: 10)
    - includeCustomAttributes: 是否包含自定义属性 (默认: true)
    """
    try:
        # 获取参数
        max_depth = request.json.get('maxDepth', 10) if request.json else request.args.get('maxDepth', 10, type=int)
        include_custom_attributes = request.json.get('includeCustomAttributes', True) if request.json else request.args.get('includeCustomAttributes', 'true').lower() == 'true'
        
        logger.info(f"开始全量同步项目 {project_id}: maxDepth={max_depth}, includeCustomAttributes={include_custom_attributes}")
        
        # 执行同步
        result = sync_manager.full_sync_project(
            project_id, 
            max_depth=max_depth,
            include_custom_attributes=include_custom_attributes
        )
        
        if result["success"]:
            return jsonify({
                "success": True,
                "message": f"项目全量同步完成",
                "data": result
            })
        else:
            return jsonify({
                "success": False,
                "error": result["error"],
                "duration_seconds": result["duration_seconds"]
            }), 500
            
    except Exception as e:
        logger.error(f"全量同步API失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"全量同步失败: {str(e)}"
        }), 500


@file_sync_db_bp.route('/api/file-sync-db/project/<project_id>/incremental-sync', methods=['POST'])
def incremental_sync_project_api(project_id):
    """
    项目增量同步API (已棄用)
    
    ⚠️ DEPRECATED: 請使用 POST /api/file-sync-db/project/{project_id}/sync 
    並設置 syncType: "incremental_sync"
    """
    """
    项目增量同步API
    
    POST /api/file-sync-db/project/{project_id}/incremental-sync
    """
    try:
        logger.info(f"开始增量同步项目 {project_id}")
        
        # 执行增量同步
        result = sync_manager.incremental_sync_project(project_id)
        
        if result["success"]:
            return jsonify({
                "success": True,
                "message": "项目增量同步完成",
                "data": result
            })
        else:
            return jsonify({
                "success": False,
                "error": result["error"],
                "duration_seconds": result["duration_seconds"]
            }), 500
            
    except Exception as e:
        logger.error(f"增量同步API失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"增量同步失败: {str(e)}"
        }), 500


@file_sync_db_bp.route('/api/file-sync-db/project/<project_id>/batch-sync', methods=['POST'])
def batch_sync_project_api(project_id):
    """
    批量优化的项目同步API (已棄用)
    
    ⚠️ DEPRECATED: 請使用 POST /api/file-sync-db/project/{project_id}/sync 
    並設置 syncType: "full_sync" 或 "incremental_sync"
    
    POST /api/file-sync-db/project/{project_id}/batch-sync
    
    参数:
    - maxDepth: 最大遍历深度 (默认: 10)
    - includeCustomAttributes: 是否包含自定义属性 (默认: true)
    - batchSize: 批量处理大小 (默认: 100)
    - apiDelay: API调用间隔秒数 (默认: 0.2)
    - isFullSync: 是否為全量同步，會先清除現有數據 (默认: false)
    """
    try:
        # 获取参数
        request_data = request.json or {}
        max_depth = request_data.get('maxDepth', 10)
        include_custom_attributes = request_data.get('includeCustomAttributes', True)
        batch_size = request_data.get('batchSize', 100)
        api_delay = request_data.get('apiDelay', 0.2)
        is_full_sync = request_data.get('isFullSync', False)
        
        sync_mode = "全量同步" if is_full_sync else "增量同步"
        logger.info(f"开始批量优化{sync_mode}项目 {project_id}: maxDepth={max_depth}, batchSize={batch_size}, isFullSync={is_full_sync}")
        
        # 🧹 强制清理该项目的所有运行中任务
        cleanup_result = _force_cleanup_running_tasks(project_id)
        logger.info(f"强制清理运行中任务: {cleanup_result}")
        
        # 生成简单的任务ID（不存储到数据库）
        import uuid
        task_id = str(uuid.uuid4())
        
        # 立即返回任务ID，同步在后台执行
        import threading
        
        def run_batch_sync():
            try:
                from datetime import datetime
                start_time = datetime.now()
                
                # 註冊任務到追蹤系統
                try:
                    from api_modules.task_lifecycle_manager import task_manager
                    task_type = "full_sync" if is_full_sync else "batch_optimized_sync"
                    task_manager.register_task(task_id, {
                    "current_stage": "initializing",
                    "progress_percentage": 0.0,
                        "project_id": project_id,
                        "task_type": task_type,
                        "is_full_sync": is_full_sync
                })
                    logger.info(f"任务 {task_id} 已注册到任务追踪系统 (類型: {task_type})")
                except ImportError:
                    logger.warning("Task tracking system not available")
                
                # 创建批量同步管理器
                batch_manager = BatchOptimizedSyncManager(batch_size=batch_size, api_delay=api_delay)
                
                # 执行批量同步（使用内存进度）
                result = batch_manager.batch_sync_project(
                    project_id, 
                    max_depth=max_depth,
                    include_custom_attributes=include_custom_attributes,
                    task_id=task_id,
                    is_full_sync=is_full_sync
                )
                
                # 计算耗时
                duration = (datetime.now() - start_time).total_seconds()
                
                # 完成任务并记录到数据库
                if result.get("success", False):
                    _complete_task(task_id, {
                        "project_id": project_id,
                        "start_time": start_time,
                        "duration_seconds": duration,
                        **result.get("results", {})
                    })
                else:
                    # 失败的任务通知追蹤系統
                    try:
                        from api_modules.task_lifecycle_manager import task_manager
                        task_manager.fail_task(task_id, result.get("error", "Unknown error"))
                    except ImportError:
                        logger.warning("Task tracking system not available")
                    
            except Exception as e:
                logger.error(f"后台批量同步失败: {str(e)}")
                try:
                    from api_modules.task_lifecycle_manager import task_manager
                    task_manager.fail_task(task_id, str(e))
                except ImportError:
                    logger.warning("Task tracking system not available")
        
        # 启动后台线程
        sync_thread = threading.Thread(target=run_batch_sync)
        sync_thread.daemon = True
        sync_thread.start()
        
        # 立即返回任务信息
        return jsonify({
            "success": True,
            "message": f"批量优化{sync_mode}已启动",
            "data": {
                "task_id": task_id,
                "status": "running",
                "optimization_info": {
                    "batch_size": batch_size,
                    "api_delay": api_delay,
                    "sync_type": "full_sync" if is_full_sync else "batch_optimized",
                    "is_full_sync": is_full_sync
                }
            }
        })
            
    except Exception as e:
        logger.error(f"批量优化同步API失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"批量优化同步失败: {str(e)}"
        }), 500


# 舊的進度查詢API已移除，現在使用 /api/task-tracking/project/<project_id>/sync-progress/<task_id>


@file_sync_db_bp.route('/api/file-sync-db/project/<project_id>/sync-status')
def get_sync_status(project_id):
    """
    获取项目同步状态
    
    GET /api/file-sync-db/project/{project_id}/sync-status
    """
    try:
        # 获取项目信息
        project = sync_manager.dal.get_project(project_id)
        if not project:
            return jsonify({
                "success": False,
                "error": "项目不存在"
            }), 404
        
        # 获取最近的同步任务
        recent_tasks = sync_manager.dal.get_recent_sync_tasks(project_id, limit=5)
        
        return jsonify({
            "success": True,
            "data": {
                "project": {
                    "id": project_id,
                    "sync_info": project.get("sync_info", {}),
                    "statistics": project.get("statistics", {})
                },
                "recent_tasks": recent_tasks
            }
        })
        
    except Exception as e:
        logger.error(f"获取同步状态失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"获取同步状态失败: {str(e)}"
        }), 500


@file_sync_db_bp.route('/api/file-sync-db/project/<project_id>/folders')
def get_project_folders_from_db(project_id):
    """
    从数据库获取项目文件夹列表
    
    GET /api/file-sync-db/project/{project_id}/folders
    
    参数:
    - depth: 指定层级 (可选)
    - parent_id: 父文件夹ID (可选)
    - limit: 限制数量 (默认: 100)
    """
    try:
        depth = request.args.get('depth', type=int)
        parent_id = request.args.get('parent_id')
        limit = request.args.get('limit', 100, type=int)
        
        folders = sync_manager.dal.get_project_folders(
            project_id, 
            depth=depth, 
            parent_id=parent_id, 
            limit=limit
        )
        
        return jsonify({
            "success": True,
            "data": {
                "folders": folders,
                "total_count": len(folders)
            }
        })
        
    except Exception as e:
        logger.error(f"获取文件夹列表失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"获取文件夹列表失败: {str(e)}"
        }), 500


@file_sync_db_bp.route('/api/file-sync-db/project/<project_id>/files')
def get_project_files_from_db(project_id):
    """
    从数据库获取项目文件列表
    
    GET /api/file-sync-db/project/{project_id}/files
    
    参数:
    - folder_id: 文件夹ID (可选)
    - file_type: 文件类型 (可选)
    - limit: 限制数量 (默认: 100)
    """
    try:
        folder_id = request.args.get('folder_id')
        file_type = request.args.get('file_type')
        limit = request.args.get('limit', 100, type=int)
        
        files = sync_manager.dal.get_project_files(
            project_id,
            folder_id=folder_id,
            file_type=file_type,
            limit=limit
        )
        
        return jsonify({
            "success": True,
            "data": {
                "files": files,
                "total_count": len(files)
            }
        })
        
    except Exception as e:
        logger.error(f"获取文件列表失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"获取文件列表失败: {str(e)}"
        }), 500


@file_sync_db_bp.route('/api/file-sync-db/search')
def search_files_and_folders():
    """
    搜索文件和文件夹
    
    GET /api/file-sync-db/search
    
    参数:
    - q: 搜索关键词 (必需)
    - project_id: 项目ID (必需)
    - type: 搜索类型 files/folders/both (默认: both)
    - limit: 限制数量 (默认: 50)
    """
    try:
        query = request.args.get('q')
        project_id = request.args.get('project_id')
        search_type = request.args.get('type', 'both')
        limit = request.args.get('limit', 50, type=int)
        
        if not query or not project_id:
            return jsonify({
                "success": False,
                "error": "缺少必需参数: q 和 project_id"
            }), 400
        
        results = {}
        
        if search_type in ['files', 'both']:
            files = sync_manager.dal.search_files(project_id, query, limit)
            results['files'] = files
        
        if search_type in ['folders', 'both']:
            folders = sync_manager.dal.search_folders(project_id, query, limit)
            results['folders'] = folders
        
        return jsonify({
            "success": True,
            "data": results
        })
        
    except Exception as e:
        logger.error(f"搜索失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"搜索失败: {str(e)}"
        }), 500


@file_sync_db_bp.route('/api/file-sync-db/health')
def health_check():
    """健康检查API"""
    try:
        # 测试数据库连接
        db = sync_manager.dal.connect()
        
        # 获取基本统计信息
        stats = {
            "database_connected": True,
            "collections": {
                "projects": db.projects.count_documents({}),
                "folders": db.folders.count_documents({}),
                "files": db.files.count_documents({}),
                "file_versions": db.file_versions.count_documents({}),
                "sync_tasks": db.sync_tasks.count_documents({})
            }
        }
        
        return jsonify({
            "success": True,
            "status": "healthy",
            "data": stats
        })
        
    except Exception as e:
        logger.error(f"健康检查失败: {str(e)}")
        return jsonify({
            "success": False,
            "status": "unhealthy",
            "error": str(e)
        }), 500


@file_sync_db_bp.route('/api/file-sync-db/project/<project_id>/sync-history')
def get_sync_history(project_id):
    """
    Get simplified sync history for a project (only successful syncs)
    
    GET /api/file-sync-db/project/{project_id}/sync-history
    
    Parameters:
    - limit: Number of records to return (default: 20)
    - offset: Number of records to skip (default: 0)
    - sync_type: Filter by sync type (optional: full_sync, batch_sync)
    """
    try:
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)
        sync_type = request.args.get('sync_type')
        
        # 使用简化的同步历史记录
        records = sync_manager.dal.get_sync_history(
            project_id, 
            limit=limit, 
            offset=offset, 
            sync_type=sync_type
        )
        
        # 获取总数
        total_count = sync_manager.dal.get_sync_history_count(project_id, sync_type)
        
        return jsonify({
            "success": True,
            "data": {
                "tasks": records,  # 保持兼容性，仍然叫tasks
                "pagination": {
                    "total": total_count,
                    "limit": limit,
                    "offset": offset,
                    "has_more": (offset + limit) < total_count
                }
            }
        })
        
    except Exception as e:
        logger.error(f"获取同步历史失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"获取同步历史失败: {str(e)}"
        }), 500


# 調試API已移至獨立的任務追蹤系統 /api/task-tracking/stats 和 /api/task-tracking/cleanup


@file_sync_db_bp.route('/api/file-sync-db/project/<project_id>/cleanup-tasks', methods=['POST'])
def cleanup_stuck_tasks(project_id):
    """清理卡住的同步任务"""
    try:
        from datetime import datetime, timedelta
        from bson import ObjectId
        
        db = batch_sync_manager.dal.connect()
        
        # 获取所有running状态的任务
        running_tasks = list(db.sync_tasks.find({
            'task_status': 'running',
            'project_id': project_id
        }).sort('created_at', -1))
        
        if len(running_tasks) <= 1:
            return jsonify({
                "success": True,
                "message": f"无需清理，只有 {len(running_tasks)} 个运行中的任务"
            })
        
        # 保留最新的，其他的标记为取消
        latest_task = running_tasks[0]
        cancelled_count = 0
        
        for task in running_tasks[1:]:
            task_id = task['_id']
            
            # 使用replace_one来替换整个文档
            updated_task = task.copy()
            updated_task['task_status'] = 'cancelled'
            updated_task['end_time'] = datetime.now()
            updated_task['updated_at'] = datetime.now()
            updated_task['results'] = {'error': '重复任务，已清理'}
            
            result = db.sync_tasks.replace_one({'_id': task_id}, updated_task)
            if result.modified_count > 0:
                cancelled_count += 1
        
        return jsonify({
            "success": True,
            "message": f"清理完成，保留任务 {latest_task['_id']}，取消了 {cancelled_count} 个重复任务"
        })
        
    except Exception as e:
        logger.error(f"清理任务失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"清理任务失败: {str(e)}"
        }), 500
