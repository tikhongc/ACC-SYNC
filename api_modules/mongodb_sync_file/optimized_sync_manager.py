# -*- coding: utf-8 -*-
"""
優化的同步管理器
實現高性能的全量同步和增量同步功能

核心優化策略：
1. 分層並發BFS遍歷
2. 批量API調用
3. 自適應API節流
4. 智能並發處理
5. 批量數據庫操作
"""

import time
import logging
from datetime import datetime, timedelta
from collections import deque, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Tuple, Any, Optional
import threading
import requests

# 導入現有模組
from database.data_access_layer import DataAccessLayer
from database.simplified_sync_schema import (
    CHINA_TZ, get_china_time, format_china_time
)
from .file_sync_api import (
    get_folder_contents, get_item_versions, 
    get_multiple_folder_contents_batch, get_versions_parallel
)
# 從 file_sync_db_api 導入時間處理函數
from .file_sync_db_api import normalize_db_datetime, parse_api_datetime
from database.data_sync_strategy import DataTransformer
import utils

logger = logging.getLogger(__name__)

class OptimizedSyncManager:
    """
    優化的同步管理器
    
    主要改進：
    - 分層並發BFS遍歷，避免單線程瓶頸
    - 批量API調用，減少網絡開銷
    - 自適應API節流，動態調整延遲
    - 智能並發處理，最大化資源利用
    """
    
    def __init__(self, batch_size: int = 100, api_delay: float = 0.02, max_workers: int = 6):
        self.dal = DataAccessLayer()
        self.batch_size = batch_size
        self.api_delay = api_delay
        self.max_workers = max_workers
        self.converter = DataTransformer()
        
        # 自適應節流相關
        self.adaptive_delay = True
        self.api_response_times = []
        self.max_response_history = 20
        
        # 性能統計
        self.stats = {
            'api_calls': 0,
            'concurrent_operations': 0,
            'batch_operations': 0,
            'total_throttle_time': 0
        }
    
    # ============================================================================
    # 優化的全量同步
    # ============================================================================
    
    def optimized_full_sync(self, project_id: str, max_depth: int = 10, 
                           include_custom_attributes: bool = True, task_id: str = None) -> dict:
        """
        優化的全量同步
        
        核心改進：
        1. 分層並發BFS收集
        2. 批量API調用
        3. 自適應節流
        4. 並發數據處理
        """
        start_time = time.time()
        
        try:
            logger.info(f"🚀 開始優化全量同步: {project_id}")
            
            # 1. 獲取API訪問令牌
            access_token = utils.get_access_token()
            if not access_token:
                raise Exception("無法獲取訪問令牌")
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # 2. 清除現有數據（全量同步）
            if task_id:
                self._update_sync_task_progress(task_id, {
                    "current_stage": "clearing_data",
                    "progress_percentage": 5.0,
                    "message": "清除現有數據..."
                })
            
            self.dal.clear_project_data(project_id)
            logger.info(f"✅ 已清除項目數據: {project_id}")
            
            # 3. 獲取項目頂級文件夾
            top_folders_data = self._get_top_folders_with_retry(project_id, headers)
            
            # 4. 優化的BFS收集所有項目
            if task_id:
                self._update_sync_task_progress(task_id, {
                    "current_stage": "collecting",
                    "progress_percentage": 10.0,
                    "message": "收集項目結構..."
                })
            
            all_folders, all_files = self._collect_all_items_concurrent_bfs(
                project_id, top_folders_data['data'], headers, max_depth, task_id
            )
            
            logger.info(f"📊 收集完成: {len(all_folders)} 個文件夾, {len(all_files)} 個文件")
            
            # 5. 並發處理文件夾
            if task_id:
                self._update_sync_task_progress(task_id, {
                    "current_stage": "processing_folders",
                    "progress_percentage": 60.0,
                    "message": "處理文件夾..."
                })
            
            folder_results = self._enhanced_batch_process_folders(
                all_folders, project_id, include_custom_attributes, headers, task_id
            )
            
            # 6. 並發處理文件
            if task_id:
                self._update_sync_task_progress(task_id, {
                    "current_stage": "processing_files",
                    "progress_percentage": 80.0,
                    "message": "處理文件..."
                })
            
            file_results = self._enhanced_batch_process_files(
                all_files, project_id, include_custom_attributes, headers, task_id
            )
            
            # 7. 更新項目同步時間
            self.dal.update_project_sync_status(project_id, "completed", get_china_time())
            
            # 8. 計算結果
            duration = time.time() - start_time
            
            results = {
                "folders_synced": folder_results.get("folders_synced", 0),
                "files_synced": file_results.get("files_synced", 0),
                "versions_synced": file_results.get("versions_synced", 0),
                "total_size": file_results.get("total_size", 0),
                "errors": folder_results.get("errors", []) + file_results.get("errors", [])
            }
            
            # 性能統計
            performance_stats = {
                "duration_seconds": duration,
                "api_calls": self.stats['api_calls'],
                "concurrent_operations": self.stats['concurrent_operations'],
                "batch_operations": self.stats['batch_operations'],
                "avg_api_response_time": sum(self.api_response_times) / len(self.api_response_times) if self.api_response_times else 0,
                "throttle_time": self.stats['total_throttle_time']
            }
            
            logger.info(f"✅ 優化全量同步完成: {duration:.2f}秒, API調用: {self.stats['api_calls']}")
            
            return {
                "success": True,
                "results": results,
                "performance": performance_stats,
                "optimization_info": {
                    "max_workers": self.max_workers,
                    "batch_size": self.batch_size,
                    "api_delay": self.api_delay,
                    "adaptive_delay": self.adaptive_delay
                }
            }
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"❌ 優化全量同步失敗: {str(e)}")
            
            return {
                "success": False,
                "error": str(e),
                "duration_seconds": duration
            }
    
    # ============================================================================
    # 優化的增量同步
    # ============================================================================
    
    def optimized_incremental_sync(self, project_id: str, max_depth: int = 10, 
                                  include_custom_attributes: bool = True, task_id: str = None) -> dict:
        """
        優化的增量同步
        
        核心改進：
        1. 分層並發變更檢測
        2. 智能時間戳比較
        3. 批量變更處理
        4. 並發API調用
        """
        start_time = time.time()
        
        try:
            logger.info(f"🔄 開始優化增量同步: {project_id}")
            
            # 1. 獲取上次同步時間
            last_sync_time = self._get_last_sync_time(project_id)
            logger.info(f"📅 上次同步時間: {format_china_time(last_sync_time) if last_sync_time else 'None'}")
            
            # 2. 獲取API訪問令牌
            access_token = utils.get_access_token()
            if not access_token:
                raise Exception("無法獲取訪問令牌")
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # 3. 獲取項目頂級文件夾
            top_folders_data = self._get_top_folders_with_retry(project_id, headers)
            
            # 4. 檢查是否有基準時間
            if not last_sync_time:
                logger.warning("⚠️ 沒有上次同步時間，無法執行增量同步")
                return {
                    "success": False,
                    "error": "沒有上次同步時間記錄，請先執行全量同步",
                    "message": "需要先執行全量同步來建立基準時間",
                    "duration_seconds": time.time() - start_time
                }
            
            # 5. 優化的變更檢測
            if task_id:
                self._update_sync_task_progress(task_id, {
                    "current_stage": "checking_changes",
                    "progress_percentage": 10.0,
                    "message": "檢查變更..."
                })
            
            changed_folders, changed_files = self._collect_changed_items_concurrent(
                project_id, top_folders_data['data'], headers, max_depth, last_sync_time, task_id
            )
            
            # 6. 如果沒有變更，直接返回
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
                    },
                    "performance": {
                        "duration_seconds": time.time() - start_time,
                        "api_calls": self.stats['api_calls']
                    }
                }
            
            logger.info(f"📊 檢測到變更: {len(changed_folders)} 個文件夾, {len(changed_files)} 個文件")
            
            # 6. 並發同步變更的項目
            if task_id:
                self._update_sync_task_progress(task_id, {
                    "current_stage": "syncing_changes",
                    "progress_percentage": 50.0,
                    "message": "同步變更..."
                })
            
            sync_results = self._sync_changed_items_concurrent(
                project_id, changed_folders, changed_files, headers, include_custom_attributes, task_id
            )
            
            # 7. 更新項目同步時間
            self.dal.update_project_sync_status(project_id, "completed", get_china_time())
            
            # 8. 計算結果
            duration = time.time() - start_time
            
            performance_stats = {
                "duration_seconds": duration,
                "api_calls": self.stats['api_calls'],
                "concurrent_operations": self.stats['concurrent_operations'],
                "changes_detected": len(changed_folders) + len(changed_files),
                "smart_skips": self.stats.get('smart_skips', 0),
                "avg_api_response_time": sum(self.api_response_times) / len(self.api_response_times) if self.api_response_times else 0,
                "optimization_efficiency": self._calculate_optimization_efficiency()
            }
            
            logger.info(f"✅ 優化增量同步完成: {duration:.2f}秒, 變更: {len(changed_folders) + len(changed_files)}, 智能跳過: {self.stats.get('smart_skips', 0)}, 優化效率: {performance_stats['optimization_efficiency']}%")
            
            return {
                "success": True,
                "results": sync_results,
                "performance": performance_stats,
                "optimization_info": {
                    "max_workers": self.max_workers,
                    "changes_detected": len(changed_folders) + len(changed_files)
                }
            }
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"❌ 優化增量同步失敗: {str(e)}")
            
            return {
                "success": False,
                "error": str(e),
                "duration_seconds": duration
            }
    
    # ============================================================================
    # 分層並發BFS收集
    # ============================================================================
    
    def _collect_all_items_concurrent_bfs(self, project_id: str, top_folders: List[dict], 
                                         headers: dict, max_depth: int, task_id: str = None) -> Tuple[List, List]:
        """
        分層並發的BFS收集所有項目
        
        優化策略：
        1. 按層級處理，每層內部並發
        2. 批量獲取文件夾內容
        3. 自適應API節流
        """
        all_folders = []
        all_files = []
        
        # 按層級處理
        current_level = [(folder, 0, "") for folder in top_folders]
        processed_levels = 0
        
        while current_level and processed_levels < max_depth:
            logger.info(f"🔄 處理第 {processed_levels + 1} 層，共 {len(current_level)} 個文件夾")
            
            next_level = []
            
            # 當前層級並發處理
            level_folders, level_files, level_subfolders = self._process_level_concurrent(
                project_id, current_level, headers, processed_levels
            )
            
            all_folders.extend(level_folders)
            all_files.extend(level_files)
            next_level.extend(level_subfolders)
            
            # 更新進度
            if task_id:
                progress = min(10 + (processed_levels / max_depth) * 40, 50)
                self._update_sync_task_progress(task_id, {
                    "current_stage": "collecting",
                    "progress_percentage": progress,
                    "processed_levels": processed_levels + 1,
                    "collected_folders": len(all_folders),
                    "collected_files": len(all_files)
                })
            
            current_level = next_level
            processed_levels += 1
        
        logger.info(f"📊 BFS收集完成: {len(all_folders)} 個文件夾, {len(all_files)} 個文件")
        return all_folders, all_files
    
    def _process_level_concurrent(self, project_id: str, level_folders: List[Tuple], 
                                 headers: dict, depth: int) -> Tuple[List, List, List]:
        """並發處理單個層級的所有文件夾"""
        level_folder_results = []
        level_file_results = []
        level_subfolder_results = []
        
        # 提取文件夾ID進行批量處理
        folder_ids = [folder_info[0].get('id') for folder_info in level_folders]
        
        # 批量獲取文件夾內容
        start_time = time.time()
        contents_batch = get_multiple_folder_contents_batch(project_id, folder_ids, headers)
        api_time = time.time() - start_time
        
        self.stats['api_calls'] += len(folder_ids)
        self.stats['batch_operations'] += 1
        self._record_api_response_time(api_time)
        
        # 並發處理結果
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._process_single_folder_content, folder_info, contents_batch, depth): folder_info
                for folder_info in level_folders
            }
            
            for future in as_completed(futures):
                try:
                    folder_data, file_data, subfolder_data = future.result()
                    level_folder_results.extend(folder_data)
                    level_file_results.extend(file_data)
                    level_subfolder_results.extend(subfolder_data)
                    self.stats['concurrent_operations'] += 1
                except Exception as e:
                    logger.error(f"處理文件夾內容失敗: {e}")
        
        # 自適應節流
        self._adaptive_api_throttle()
        
        return level_folder_results, level_file_results, level_subfolder_results
    
    def _process_single_folder_content(self, folder_info: Tuple, contents_batch: dict, 
                                      depth: int) -> Tuple[List, List, List]:
        """處理單個文件夾的內容"""
        folder_data, current_depth, parent_path = folder_info
        folder_id = folder_data.get('id')
        folder_name = folder_data.get('attributes', {}).get('displayName', 'Unknown')
        current_path = f"{parent_path}/{folder_name}" if parent_path else folder_name
        
        folder_results = [(folder_data, current_depth, parent_path)]
        file_results = []
        subfolder_results = []
        
        # 獲取該文件夾的內容
        contents_data = contents_batch.get(folder_id, {})
        if contents_data and contents_data.get('data'):
            for item in contents_data['data']:
                item_type = item.get('type')
                if item_type == 'folders':
                    subfolder_results.append((item, current_depth + 1, current_path))
                else:
                    file_results.append((item, folder_id, current_path, current_depth))
        
        return folder_results, file_results, subfolder_results
    
    # ============================================================================
    # 優化的增量變更檢測
    # ============================================================================
    
    def _collect_changed_items_concurrent(self, project_id: str, top_folders: List[dict], 
                                         headers: dict, max_depth: int, last_sync_time, 
                                         task_id: str = None) -> Tuple[List, List]:
        """
        並發檢測變更項目
        
        優化策略：
        1. 分層並發檢測
        2. 智能時間戳比較
        3. 批量API調用
        """
        # 標準化基準時間
        logger.info(f"🔍 原始 last_sync_time: {last_sync_time}, 類型: {type(last_sync_time)}")
        last_sync_time = self._normalize_sync_time(last_sync_time)
        logger.info(f"🔍 標準化後 last_sync_time: {last_sync_time}, 類型: {type(last_sync_time)}")
        
        if last_sync_time:
            logger.info(f"🔍 基準時間戳: {self._get_timestamp(last_sync_time)}")
        else:
            logger.warning("⚠️ 基準時間為空，將使用7天前")
        
        changed_folders = []
        changed_files = []
        
        # 按層級檢測變更
        current_level = [(folder, 0, "") for folder in top_folders]
        processed_levels = 0
        
        while current_level and processed_levels < max_depth:
            logger.info(f"🔍 檢測第 {processed_levels + 1} 層變更，共 {len(current_level)} 個文件夾")
            
            next_level = []
            
            # 當前層級並發檢測
            level_changed_folders, level_changed_files, level_subfolders = self._detect_level_changes_concurrent(
                project_id, current_level, headers, last_sync_time, processed_levels
            )
            
            changed_folders.extend(level_changed_folders)
            changed_files.extend(level_changed_files)
            next_level.extend(level_subfolders)
            
            # 更新進度
            if task_id:
                progress = min(10 + (processed_levels / max_depth) * 20, 30)
                self._update_sync_task_progress(task_id, {
                    "current_stage": "checking_changes",
                    "progress_percentage": progress,
                    "processed_levels": processed_levels + 1,
                    "changed_folders": len(changed_folders),
                    "changed_files": len(changed_files)
                })
            
            current_level = next_level
            processed_levels += 1
        
        logger.info(f"🔍 變更檢測完成: {len(changed_folders)} 個文件夾, {len(changed_files)} 個文件")
        return changed_folders, changed_files
    
    def _detect_level_changes_concurrent(self, project_id: str, level_folders: List[Tuple], 
                                        headers: dict, last_sync_time, depth: int) -> Tuple[List, List, List]:
        """並發檢測單個層級的變更"""
        level_changed_folders = []
        level_changed_files = []
        level_subfolders = []
        
        # 批量獲取文件夾內容
        folder_ids = [folder_info[0].get('id') for folder_info in level_folders]
        contents_batch = get_multiple_folder_contents_batch(project_id, folder_ids, headers)
        
        self.stats['api_calls'] += len(folder_ids)
        self.stats['batch_operations'] += 1
        
        # 並發檢測變更
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._detect_folder_changes, folder_info, contents_batch, last_sync_time, depth): folder_info
                for folder_info in level_folders
            }
            
            for future in as_completed(futures):
                try:
                    folder_changes, file_changes, subfolders = future.result()
                    level_changed_folders.extend(folder_changes)
                    level_changed_files.extend(file_changes)
                    level_subfolders.extend(subfolders)
                    self.stats['concurrent_operations'] += 1
                except Exception as e:
                    logger.error(f"檢測文件夾變更失敗: {e}")
        
        return level_changed_folders, level_changed_files, level_subfolders
    
    def _detect_folder_changes(self, folder_info: Tuple, contents_batch: dict, 
                              last_sync_time, depth: int) -> Tuple[List, List, List]:
        """檢測單個文件夾的變更 - 優化版本，使用 last_modified_time_rollup 智能跳過"""
        folder_data, current_depth, parent_path = folder_info
        folder_id = folder_data.get('id')
        folder_name = folder_data.get('attributes', {}).get('displayName', 'Unknown')
        current_path = f"{parent_path}/{folder_name}" if parent_path else folder_name
        
        changed_folders = []
        changed_files = []
        subfolders = []
        
        # 🚀 核心優化：使用 last_modified_time_rollup 進行智能分支跳過
        folder_rollup_time = self._parse_datetime(folder_data.get('attributes', {}).get('lastModifiedTimeRollup'))
        
        # If entire branch (including all sub-items) has no changes, skip directly
        if folder_rollup_time and not self._is_changed(folder_rollup_time, last_sync_time):
            logger.debug(f"Smart skip branch: {folder_name} (rollup time: {folder_rollup_time} <= base time: {last_sync_time})")
            self.stats.setdefault('smart_skips', 0)
            self.stats['smart_skips'] += 1
            return changed_folders, changed_files, subfolders
        
        logger.debug(f"Branch has changes, continue checking: {folder_name} (rollup time: {folder_rollup_time} > base time: {last_sync_time})")
        
        # Check if folder itself has changes
        folder_last_modified = self._parse_datetime(folder_data.get('attributes', {}).get('lastModifiedTime'))
        if self._is_changed(folder_last_modified, last_sync_time):
            changed_folders.append((folder_data, current_depth, parent_path))
            logger.debug(f"Folder has changes: {folder_name}")
        
        # 檢查文件夾內容
        contents_data = contents_batch.get(folder_id, {})
        if contents_data and contents_data.get('data'):
            for item in contents_data['data']:
                item_type = item.get('type')
                
                if item_type == 'folders':
                    # Check subfolder rollup time for smart skipping
                    subfolder_rollup_time = self._parse_datetime(item.get('attributes', {}).get('lastModifiedTimeRollup'))
                    if subfolder_rollup_time and self._is_changed(subfolder_rollup_time, last_sync_time):
                    subfolders.append((item, current_depth + 1, current_path))
                        logger.debug(f"Subfolder has changes: {item.get('attributes', {}).get('displayName', 'Unknown')}")
                else:
                        logger.debug(f"Skipping subfolder branch: {item.get('attributes', {}).get('displayName', 'Unknown')}")
                        self.stats.setdefault('smart_skips', 0)
                        self.stats['smart_skips'] += 1
                else:
                    # Check if file has changes
                    item_last_modified = self._parse_datetime(item.get('attributes', {}).get('lastModifiedTime'))
                    if self._is_changed(item_last_modified, last_sync_time):
                        changed_files.append((item, folder_id, current_path, current_depth))
                        logger.debug(f"File has changes: {item.get('attributes', {}).get('displayName', 'Unknown')}")
        
        return changed_folders, changed_files, subfolders
    
    # ============================================================================
    # 增強的並發處理
    # ============================================================================
    
    def _enhanced_batch_process_folders(self, folders_with_context: List[Tuple], project_id: str,
                                       include_custom_attributes: bool, headers: dict, task_id: str) -> dict:
        """增強的文件夾批量處理"""
        results = {"folders_synced": 0, "errors": []}
        
        if not folders_with_context:
            return results
        
        # 分批處理，避免過大的並發
        batch_size = min(self.batch_size, len(folders_with_context))
        batches = [folders_with_context[i:i+batch_size] for i in range(0, len(folders_with_context), batch_size)]
        
        for batch_idx, batch in enumerate(batches):
            logger.info(f"🔄 處理文件夾批次 {batch_idx + 1}/{len(batches)}, 大小: {len(batch)}")
            
            # 並發處理當前批次
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {
                    executor.submit(self._process_single_folder, folder_info, project_id, headers): folder_info
                    for folder_info in batch
                }
                
                for future in as_completed(futures):
                    try:
                        folder_result = future.result()
                        if folder_result.get('success'):
                            results["folders_synced"] += 1
                        else:
                            results["errors"].append(folder_result.get('error'))
                        self.stats['concurrent_operations'] += 1
                    except Exception as e:
                        logger.error(f"處理文件夾失敗: {e}")
                        results["errors"].append(str(e))
            
            # 批量數據庫操作
            self.stats['batch_operations'] += 1
            
            # 更新進度
            if task_id:
                progress = 60 + (batch_idx + 1) / len(batches) * 15
                self._update_sync_task_progress(task_id, {
                    "current_stage": "processing_folders",
                    "progress_percentage": progress,
                    "processed_batches": batch_idx + 1,
                    "total_batches": len(batches)
                })
        
        logger.info(f"✅ 文件夾處理完成: {results['folders_synced']} 個成功, {len(results['errors'])} 個錯誤")
        return results
    
    def _enhanced_batch_process_files(self, files_with_context: List[Tuple], project_id: str,
                                     include_custom_attributes: bool, headers: dict, task_id: str) -> dict:
        """增強的文件批量處理"""
        results = {"files_synced": 0, "versions_synced": 0, "total_size": 0, "errors": []}
        
        if not files_with_context:
            return results
        
        # 按文件夾分組，便於批量處理
        files_by_folder = defaultdict(list)
        for file_data, folder_id, folder_path, depth in files_with_context:
            files_by_folder[folder_id].append((file_data, folder_path, depth))
        
        # 並發處理多個文件夾
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._process_folder_files, project_id, folder_id, files, headers, include_custom_attributes): folder_id
                for folder_id, files in files_by_folder.items()
            }
            
            processed_folders = 0
            total_folders = len(files_by_folder)
            
            for future in as_completed(futures):
                try:
                    folder_results = future.result()
                    results["files_synced"] += folder_results["files_synced"]
                    results["versions_synced"] += folder_results["versions_synced"]
                    results["total_size"] += folder_results["total_size"]
                    results["errors"].extend(folder_results["errors"])
                    
                    processed_folders += 1
                    self.stats['concurrent_operations'] += 1
                    
                    # 更新進度
                    if task_id:
                        progress = 80 + (processed_folders / total_folders) * 15
                        self._update_sync_task_progress(task_id, {
                            "current_stage": "processing_files",
                            "progress_percentage": progress,
                            "processed_folders": processed_folders,
                            "total_folders": total_folders
                        })
                        
                except Exception as e:
                    logger.error(f"處理文件夾文件失敗: {e}")
                    results["errors"].append(str(e))
        
        logger.info(f"✅ 文件處理完成: {results['files_synced']} 個文件, {results['versions_synced']} 個版本")
        return results
    
    def _process_folder_files(self, project_id: str, folder_id: str, files: List[Tuple], 
                             headers: dict, include_custom_attributes: bool) -> dict:
        """處理單個文件夾內的所有文件"""
        results = {"files_synced": 0, "versions_synced": 0, "total_size": 0, "errors": []}
        
        try:
            # 提取文件ID
            file_ids = [file_data.get('id') for file_data, _, _ in files if file_data.get('id')]
            
            # 批量獲取版本信息
            versions_data = get_versions_parallel(project_id, file_ids, headers)
            self.stats['api_calls'] += len(file_ids)
            self.stats['batch_operations'] += 1
            
            # 處理每個文件
            for file_data, folder_path, depth in files:
                file_id = file_data.get('id')
                if file_id in versions_data:
                    # 轉換並保存文件數據
                    converted_file = self.converter.transform_file_data(
                        file_data, project_id, folder_id, folder_path, depth
                    )
                    
                    # 保存到數據庫
                    self.dal.create_or_update_file(converted_file)
                    results["files_synced"] += 1
                    
                    # 保存文件版本 - 關鍵修復！
                    versions = versions_data[file_id]  # get_item_versions已經返回data列表
                    for version in versions:
                        try:
                            version_doc = self.converter.transform_version_data(
                                version, file_id, project_id
                            )
                            
                            if self.dal.create_or_update_file_version(version_doc):
                                results["versions_synced"] += 1
                                
                            # 計算文件大小
                            size = version.get('attributes', {}).get('storageSize', 0)
                            if size:
                                results["total_size"] += size
                                
                        except Exception as ve:
                            logger.error(f"保存版本失敗 {file_id}: {str(ve)}")
                            results["errors"].append(f"版本保存失敗: {str(ve)}")
            
        except Exception as e:
            logger.error(f"處理文件夾文件失敗 {folder_id}: {e}")
            results["errors"].append(str(e))
        
        return results
    
    # ============================================================================
    # 輔助方法
    # ============================================================================
    
    def _normalize_sync_time(self, last_sync_time):
        """標準化同步時間"""
        try:
            if last_sync_time:
                # 如果已經是datetime對象且有時區信息，直接返回
                if isinstance(last_sync_time, datetime):
                    if last_sync_time.tzinfo:
                        return last_sync_time.astimezone(CHINA_TZ)
                    else:
                        # 假設為UTC時間
                        return pytz.utc.localize(last_sync_time).astimezone(CHINA_TZ)
                elif hasattr(last_sync_time, 'timestamp'):
                    timestamp = last_sync_time.timestamp()
                    return datetime.fromtimestamp(timestamp, CHINA_TZ)
                else:
                    # 字符串格式，嘗試解析
                    parsed = self._parse_datetime(last_sync_time)
                    if parsed:
                        return parsed
                    else:
                        return normalize_db_datetime(last_sync_time)
            else:
                # 如果沒有基準時間，返回None而不是7天前
                logger.warning("⚠️ 沒有基準時間，增量同步將跳過")
                return None
        except Exception as e:
            logger.error(f"時間標準化失敗: {e}")
            # 返回None而不是7天前
            return None
    
    def _is_changed(self, item_time, base_time):
        """檢查項目是否有變更"""
        if not item_time or not base_time:
            return False
        
        try:
            item_timestamp = self._get_timestamp(item_time)
            base_timestamp = self._get_timestamp(base_time)
            
            return item_timestamp and base_timestamp and item_timestamp > base_timestamp
        except Exception as e:
            logger.error(f"時間比較失敗: {e}")
            return False
    
    def _get_timestamp(self, dt):
        """獲取datetime對象的timestamp"""
        if not dt:
            return None
        
        try:
            if hasattr(dt, 'timestamp'):
                return dt.timestamp()
            
            if hasattr(dt, 'tzinfo') and dt.tzinfo is None:
                import pytz
                utc_dt = pytz.utc.localize(dt)
                return utc_dt.timestamp()
            
            if hasattr(dt, 'tzinfo') and dt.tzinfo is not None:
                return dt.timestamp()
            
            # MongoDB datetime對象處理
            import pytz
            utc_dt = pytz.utc.localize(dt)
            return utc_dt.timestamp()
            
        except Exception as e:
            logger.warning(f"獲取timestamp失敗: {dt}, 錯誤: {str(e)}")
            return None
    
    def _parse_datetime(self, datetime_str):
        """解析日期時間字符串，支持多種格式"""
        if not datetime_str:
            return None
        
        try:
            # 首先嘗試使用原有的API解析函數
            result = parse_api_datetime(datetime_str)
            if result:
                return result
        except:
            pass
        
        try:
            # 嘗試解析RFC 2822格式（如：Wed, 05 Nov 2025 09:47:55 GMT）
            from email.utils import parsedate_to_datetime
            dt = parsedate_to_datetime(datetime_str)
            return dt.astimezone(CHINA_TZ)
        except:
            pass
        
        try:
            # 嘗試其他常見格式
            import dateutil.parser
            dt = dateutil.parser.parse(datetime_str)
            if dt.tzinfo is None:
                dt = pytz.utc.localize(dt)
            return dt.astimezone(CHINA_TZ)
        except:
            pass
        
        logger.warning(f"無法解析日期時間: {datetime_str}")
        return None
    
    def _adaptive_api_throttle(self):
        """自適應API節流"""
        if not self.adaptive_delay:
            return
        
        if len(self.api_response_times) > 5:
            avg_response_time = sum(self.api_response_times[-5:]) / 5
            
            if avg_response_time > 2.0:
                # API響應慢，增加延遲
                delay = 0.1
            elif avg_response_time > 1.0:
                delay = 0.05
            elif avg_response_time < 0.3:
                # API響應快，減少延遲
                delay = 0.01
            else:
                delay = self.api_delay
            
            if delay > 0:
                time.sleep(delay)
                self.stats['total_throttle_time'] += delay
    
    def _record_api_response_time(self, response_time):
        """記錄API響應時間"""
        self.api_response_times.append(response_time)
        if len(self.api_response_times) > self.max_response_history:
            self.api_response_times.pop(0)
    
    def _get_top_folders_with_retry(self, project_id: str, headers: dict):
        """帶重試的頂級文件夾獲取"""
        from .file_sync_api import get_project_top_folders
        
        for attempt in range(3):
            try:
                result = get_project_top_folders(project_id, headers)
                if result and result.get('data'):
                    return result
            except Exception as e:
                logger.warning(f"獲取頂級文件夾失敗 (嘗試 {attempt + 1}/3): {e}")
                if attempt < 2:
                    time.sleep(1)
        
        raise Exception("無法獲取項目頂級文件夾")
    
    def _get_last_sync_time(self, project_id: str):
        """獲取上次同步時間，統一使用中國時區"""
        try:
            db = self.dal.connect()
            project = db.projects.find_one({"_id": project_id})
            
            if project and project.get("sync_info") and project["sync_info"].get("last_sync_time"):
                last_sync = project["sync_info"]["last_sync_time"]
                # 使用統一的時間標準化函數
                from api_modules.file_sync_db_api import normalize_db_datetime
                normalized_time = normalize_db_datetime(last_sync)
                logger.info(f"獲取上次同步時間: {last_sync} -> {normalized_time}")
                return normalized_time
            else:
                logger.info("項目沒有上次同步時間記錄")
                return None
        except Exception as e:
            logger.error(f"獲取上次同步時間失敗: {e}")
            return None
    
    def _process_single_folder(self, folder_info: Tuple, project_id: str, headers: dict) -> dict:
        """處理單個文件夾"""
        try:
            folder_data, depth, parent_path = folder_info
            
            # 轉換文件夾數據
            converted_folder = self.converter.transform_folder_data(folder_data, project_id, None, parent_path, depth)
            
            # 保存到數據庫
            self.dal.create_or_update_folder(converted_folder)
            
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _sync_changed_items_concurrent(self, project_id: str, changed_folders: List, 
                                      changed_files: List, headers: dict, 
                                      include_custom_attributes: bool, task_id: str) -> dict:
        """並發同步變更的項目"""
        results = {
            "folders_synced": 0,
            "files_synced": 0,
            "versions_synced": 0,
            "total_size": 0,
            "errors": []
        }
        
        # 並發處理文件夾
        if changed_folders:
            folder_results = self._enhanced_batch_process_folders(
                changed_folders, project_id, include_custom_attributes, headers, task_id
            )
            results["folders_synced"] = folder_results["folders_synced"]
            results["errors"].extend(folder_results["errors"])
        
        # 並發處理文件
        if changed_files:
            file_results = self._enhanced_batch_process_files(
                changed_files, project_id, include_custom_attributes, headers, task_id
            )
            results["files_synced"] = file_results["files_synced"]
            results["versions_synced"] = file_results["versions_synced"]
            results["total_size"] = file_results["total_size"]
            results["errors"].extend(file_results["errors"])
        
        return results
    
    def _update_sync_task_progress(self, task_id: str, progress_data: dict):
        """更新同步任務進度"""
        try:
            from api_modules.task_lifecycle_manager import task_manager
            task_manager.update_task(task_id, {"progress": progress_data})
        except Exception as e:
            logger.warning(f"更新任務進度失敗: {str(e)}")
    
    def _calculate_optimization_efficiency(self) -> float:
        """
        計算優化效率
        
        Returns:
            float: 優化效率百分比 (0-100)
        """
        try:
            total_operations = self.stats.get('concurrent_operations', 0) + self.stats.get('smart_skips', 0)
            smart_skips = self.stats.get('smart_skips', 0)
            
            if total_operations == 0:
                return 0.0
            
            # 計算跳過的比例作為優化效率
            efficiency = (smart_skips / total_operations) * 100
            return round(efficiency, 2)
            
        except Exception as e:
            logger.warning(f"計算優化效率失敗: {str(e)}")
            return 0.0


# ============================================================================
# 優化同步管理器實例
# ============================================================================

# 創建全局優化同步管理器實例
optimized_sync_manager = OptimizedSyncManager(
    batch_size=100,
    api_delay=0.02,  # 更小的延遲
    max_workers=6    # 更多的並發線程
)

# 高性能配置的實例
high_performance_sync_manager = OptimizedSyncManager(
    batch_size=150,
    api_delay=0.01,  # 最小延遲
    max_workers=8    # 最大並發
)

# 保守配置的實例（適用於API限制較嚴格的環境）
conservative_sync_manager = OptimizedSyncManager(
    batch_size=50,
    api_delay=0.05,
    max_workers=3
)
