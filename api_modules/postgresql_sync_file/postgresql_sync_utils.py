# -*- coding: utf-8 -*-
"""
PostgreSQL同步系統的共同工具函數
提取重複代碼，提高可維護性和可測試性
"""

import asyncio
import uuid
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

try:
    from .postgresql_sync_manager import OptimizedPostgreSQLSyncManager
except ImportError:
    from postgresql_sync_manager import OptimizedPostgreSQLSyncManager
from database_sql.optimized_data_access import get_optimized_postgresql_dal

# 嘗試導入認證管理器，如果不存在則使用utils中的認證
try:
    from .auth_manager import get_auth_headers
except ImportError:
    try:
        from auth_manager import get_auth_headers
    except ImportError:
        def get_auth_headers():
            """使用utils中的認證邏輯"""
            try:
                import sys
                import os
                # 添加項目根目錄到路徑
                project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                if project_root not in sys.path:
                    sys.path.append(project_root)
                
                import utils
                access_token = utils.get_access_token()
                if access_token:
                    return {
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                    }
                else:
                    logger.error("No access token available")
                    return None
            except Exception as e:
                logger.error(f"Failed to get auth headers: {e}")
                return None

logger = logging.getLogger(__name__)

# ============================================================================
# 🔧 同步管理器配置工具
# ============================================================================

class SyncManagerFactory:
    """同步管理器工廠類"""
    
    PERFORMANCE_CONFIGS = {
        'standard': {
            'batch_size': 100,
            'api_delay': 0.02,
            'max_workers': 8,
            'memory_threshold_mb': 1024
        },
        'high_performance': {
            'batch_size': 200,
            'api_delay': 0.01,
            'max_workers': 16,
            'memory_threshold_mb': 2048
        },
        'memory_optimized': {
            'batch_size': 50,
            'api_delay': 0.05,
            'max_workers': 4,
            'memory_threshold_mb': 512
        }
    }
    
    @classmethod
    def create_sync_manager(cls, performance_mode: str = 'standard') -> OptimizedPostgreSQLSyncManager:
        """創建同步管理器實例"""
        if performance_mode not in cls.PERFORMANCE_CONFIGS:
            raise ValueError(f"Invalid performance mode: {performance_mode}")
        
        config = cls.PERFORMANCE_CONFIGS[performance_mode]
        return OptimizedPostgreSQLSyncManager(**config)
    
    @classmethod
    def get_available_modes(cls) -> List[str]:
        """獲取可用的性能模式"""
        return list(cls.PERFORMANCE_CONFIGS.keys())
    
    @classmethod
    def adjust_sync_manager(cls, sync_manager: OptimizedPostgreSQLSyncManager, 
                          performance_mode: str) -> None:
        """調整現有同步管理器的參數"""
        if performance_mode not in cls.PERFORMANCE_CONFIGS:
            logger.warning(f"Unknown performance mode: {performance_mode}, using standard")
            performance_mode = 'standard'
        
        config = cls.PERFORMANCE_CONFIGS[performance_mode]
        sync_manager.batch_size = config['batch_size']
        sync_manager.api_delay = config['api_delay']
        sync_manager.max_workers = config['max_workers']
        sync_manager.memory_threshold_mb = config['memory_threshold_mb']
        
        logger.info(f"同步管理器已調整為 {performance_mode} 模式")

# ============================================================================
# 🔧 任務管理工具
# ============================================================================

class TaskManager:
    """任務管理工具類"""
    
    @staticmethod
    def generate_task_uuid() -> str:
        """生成任務UUID"""
        return str(uuid.uuid4())
    
    @staticmethod
    async def create_sync_task_record(project_id: str, task_uuid: str, task_type: str,
                                    performance_mode: str, parameters: Dict[str, Any]) -> bool:
        """創建同步任務記錄"""
        try:
            dal = await get_optimized_postgresql_dal()
            task_data = {
                'task_uuid': task_uuid,
                'project_id': project_id,
                'task_type': task_type,
                'task_status': 'running',
                'performance_mode': performance_mode,
                'parameters': parameters,
                'start_time': datetime.utcnow()
            }
            
            await dal.create_sync_task(task_data)
            return True
        except Exception as e:
            logger.error(f"Failed to create task record: {e}")
            return False
    
    @staticmethod
    async def complete_sync_task_record(task_uuid: str, results: Dict[str, Any], 
                                      sync_stats: Dict[str, Any] = None) -> bool:
        """Complete sync task record"""
        try:
            dal = await get_optimized_postgresql_dal()
            
            # Prepare complete results data
            complete_results = {
                'status': results.get('status', 'success'),
                'message': results.get('message', ''),
                'folders_synced': results.get('folders_synced', 0),
                'files_synced': results.get('files_synced', 0),
                'custom_attrs_synced': results.get('custom_attrs_synced', 0),
                'versions_synced': results.get('versions_synced', 0),
                'duration_seconds': results.get('duration_seconds', 0),
                'optimization_efficiency': results.get('optimization_efficiency', {}),
                'architecture_version': results.get('architecture_version', 'v2'),
                'sync_type': results.get('sync_type', 'unknown'),
                'synced_file_tree': True,  # Whether file tree was synced
                'synced_versions': results.get('versions_synced', 0) > 0,  # Whether versions were synced
                'synced_custom_attributes_definitions': results.get('custom_attrs_definitions_synced', 0) > 0,
                'synced_custom_attributes_values': results.get('custom_attrs_synced', 0) > 0,
                'synced_permissions': results.get('permissions_synced', False),  # Set to False for now, future expansion
                'performance_stats': sync_stats or results.get('performance_stats', {})
            }
            
            success = await dal.complete_sync_task(task_uuid, complete_results)
            if success:
                logger.info(f"Sync task record completed: {task_uuid}")
            else:
                logger.warning(f"Failed to complete sync task record: {task_uuid}")
            
            return success
        except Exception as e:
            logger.error(f"Failed to complete task record: {e}")
            return False
    
    @staticmethod
    async def fail_sync_task_record(task_uuid: str, error_message: str, 
                                  error_details: Dict[str, Any] = None) -> bool:
        """Mark sync task as failed"""
        try:
            dal = await get_optimized_postgresql_dal()
            
            # Prepare failure results data
            failure_results = {
                'status': 'failed',
                'error': error_message,
                'error_details': error_details or {},
                'folders_synced': 0,
                'files_synced': 0,
                'custom_attrs_synced': 0,
                'versions_synced': 0
            }
            
            success = await dal.complete_sync_task(task_uuid, failure_results)
            if success:
                logger.info(f"Sync task record marked as failed: {task_uuid}")
            
            return success
        except Exception as e:
            logger.error(f"Failed to mark task as failed: {e}")
            return False

# ============================================================================
# 🔧 認證和驗證工具
# ============================================================================

class AuthUtils:
    """認證和驗證工具類"""
    
    @staticmethod
    def get_auth_headers_safe() -> Optional[Dict[str, str]]:
        """安全地獲取認證頭"""
        try:
            return get_auth_headers()
        except Exception as e:
            logger.error(f"獲取認證頭失敗: {e}")
            return None
    
    @staticmethod
    def validate_sync_parameters(sync_type: str, performance_mode: str, 
                               max_depth: int, include_custom_attributes: bool) -> Dict[str, Any]:
        """驗證同步參數"""
        errors = []
        
        # 驗證同步類型
        if sync_type not in ['full_sync', 'incremental_sync']:
            errors.append(f"Invalid sync type: {sync_type}")
        
        # 驗證性能模式
        if performance_mode not in SyncManagerFactory.get_available_modes():
            errors.append(f"Invalid performance mode: {performance_mode}")
        
        # 驗證深度
        if not isinstance(max_depth, int) or max_depth < 1 or max_depth > 50:
            errors.append(f"Invalid max_depth: {max_depth}. Must be between 1 and 50")
        
        # 驗證自定義屬性參數
        if not isinstance(include_custom_attributes, bool):
            errors.append(f"Invalid include_custom_attributes: {include_custom_attributes}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }

# ============================================================================
# 🔧 頂層Rollup檢查工具
# ============================================================================

class RollupCheckUtils:
    """Rollup檢查工具類"""
    
    @staticmethod
    async def check_project_top_level_rollup(project_id: str, 
                                           sync_manager: OptimizedPostgreSQLSyncManager,
                                           last_sync_time: Optional[datetime] = None) -> Dict[str, Any]:
        """
        🔑 關鍵優化：檢查項目頂層rollup時間
        這是最重要的優化 - 可以在不調用任何API的情況下判斷整個項目是否需要同步
        """
        try:
            dal = await get_optimized_postgresql_dal()
            
            # 如果沒有提供last_sync_time，從數據庫獲取
            if not last_sync_time:
                last_sync_time = await dal.get_project_last_sync_time(project_id)
                
            if not last_sync_time:
                return {
                    'can_skip_entire_project': False,
                    'reason': 'No previous sync time found',
                    'recommendation': 'Perform full sync'
                }
            
            # 🚀 核心優化：獲取項目頂層文件夾的最大rollup時間
            async with dal.get_connection() as conn:
                query = """
                SELECT 
                    MAX(last_modified_time_rollup) as max_rollup_time,
                    COUNT(*) as total_top_level_folders,
                    COUNT(CASE WHEN last_modified_time_rollup > $2 THEN 1 END) as folders_with_changes
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
                
                # 🎯 關鍵判斷：如果最大rollup時間 <= 上次同步時間，整個項目都可以跳過
                can_skip_entire_project = max_rollup_time <= last_sync_time
                
                skip_efficiency = 0.0
                if total_folders > 0:
                    skip_efficiency = ((total_folders - folders_with_changes) / total_folders) * 100
                
                return {
                    'can_skip_entire_project': can_skip_entire_project,
                    'max_rollup_time': max_rollup_time.isoformat(),
                    'last_sync_time': last_sync_time.isoformat(),
                    'total_top_level_folders': total_folders,
                    'folders_with_changes': folders_with_changes,
                    'skip_efficiency_percentage': skip_efficiency,
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
# 🔧 性能統計工具
# ============================================================================

class PerformanceUtils:
    """性能統計工具類"""
    
    @staticmethod
    def calculate_performance_grade(avg_duration: float, avg_efficiency: float) -> str:
        """計算性能等級"""
        if avg_duration < 30 and avg_efficiency > 80:
            return 'A+'
        elif avg_duration < 60 and avg_efficiency > 70:
            return 'A'
        elif avg_duration < 120 and avg_efficiency > 60:
            return 'B'
        elif avg_duration < 300 and avg_efficiency > 50:
            return 'C'
        else:
            return 'D'
    
    @staticmethod
    async def get_efficiency_trend(project_id: str, 
                                 start_date: Optional[datetime] = None,
                                 end_date: Optional[datetime] = None) -> str:
        """獲取效率趨勢"""
        try:
            dal = await get_optimized_postgresql_dal()
            
            async with dal.get_connection() as conn:
                # 獲取最近的同步記錄，按時間排序
                conditions = ["project_id = $1", "task_status = 'completed'"]
                params = [project_id]
                
                if start_date:
                    conditions.append("start_time >= $2")
                    params.append(start_date)
                
                if end_date:
                    conditions.append("start_time <= $3")
                    params.append(end_date)
                
                query = f"""
                SELECT 
                    CAST(performance_stats->>'optimization_efficiency' AS FLOAT) as efficiency
                FROM sync_tasks 
                WHERE {' AND '.join(conditions)}
                ORDER BY start_time DESC
                LIMIT 10;
                """
                
                rows = await conn.fetch(query, *params)
                
                if len(rows) < 2:
                    return 'insufficient_data'
                
                efficiencies = [row['efficiency'] for row in rows if row['efficiency'] is not None]
                
                if len(efficiencies) < 2:
                    return 'insufficient_data'
                
                # 計算趨勢
                recent_avg = sum(efficiencies[:3]) / min(3, len(efficiencies))
                older_avg = sum(efficiencies[-3:]) / min(3, len(efficiencies[-3:]))
                
                if recent_avg > older_avg + 5:
                    return 'improving'
                elif recent_avg < older_avg - 5:
                    return 'declining'
                else:
                    return 'stable'
                    
        except Exception as e:
            logger.warning(f"獲取效率趨勢失敗: {e}")
            return 'unknown'

# ============================================================================
# 🔧 響應格式化工具
# ============================================================================

class ResponseUtils:
    """響應格式化工具類"""
    
    @staticmethod
    def create_success_response(data: Dict[str, Any], message: str = "Success") -> Dict[str, Any]:
        """創建成功響應"""
        return {
            "success": True,
            "message": message,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def create_error_response(error: str, error_code: str = "UNKNOWN_ERROR") -> Dict[str, Any]:
        """創建錯誤響應"""
        return {
            "success": False,
            "error": error,
            "error_code": error_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def create_sync_response(task_id: str, sync_type: str, performance_mode: str, 
                           status: str, **kwargs) -> Dict[str, Any]:
        """創建同步響應"""
        response = {
            "success": True,
            "task_id": task_id,
            "sync_type": sync_type,
            "performance_mode": performance_mode,
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }
        response.update(kwargs)
        return response

# ============================================================================
# 🔧 同步執行工具
# ============================================================================

class SyncExecutionUtils:
    """同步執行工具類"""
    
    @staticmethod
    async def execute_sync(sync_manager: OptimizedPostgreSQLSyncManager, 
                         sync_type: str, project_id: str, max_depth: int, 
                         include_custom_attributes: bool, task_id: str) -> Dict[str, Any]:
        """執行同步操作"""
        try:
            headers = AuthUtils.get_auth_headers_safe()
            if not headers:
                return {
                    'status': 'error',
                    'error': '無法獲取認證信息',
                    'task_id': task_id
                }
            
            if sync_type == 'full_sync':
                result = await sync_manager.optimized_full_sync(
                    project_id=project_id,
                    max_depth=max_depth,
                    include_custom_attributes=include_custom_attributes,
                    task_uuid=task_id,
                    headers=headers
                )
            else:  # incremental_sync
                result = await sync_manager.optimized_incremental_sync(
                    project_id=project_id,
                    max_depth=max_depth,
                    include_custom_attributes=include_custom_attributes,
                    task_uuid=task_id,
                    headers=headers
                )
            
            return result
            
        except Exception as e:
            logger.error(f"同步執行失敗: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'task_id': task_id
            }
