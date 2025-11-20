# -*- coding: utf-8 -*-
"""
PostgreSQL同步服務 - 業務邏輯層
提供統一的同步接口，支持全量和增量同步
重構後使用共同工具模組，提高可維護性
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

from .postgresql_sync_manager import OptimizedPostgreSQLSyncManager
from database_sql.optimized_data_access import get_optimized_postgresql_dal
from .postgresql_sync_utils import (
    SyncManagerFactory, TaskManager, AuthUtils, 
    RollupCheckUtils, PerformanceUtils, SyncExecutionUtils
)

logger = logging.getLogger(__name__)

class PostgreSQLSyncService:
    """PostgreSQL同步服務 - 重構後的業務邏輯層"""
    
    def __init__(self, performance_mode: str = 'standard'):
        self.sync_manager = SyncManagerFactory.create_sync_manager(performance_mode)
        self.current_performance_mode = performance_mode
    
    async def start_full_sync(self, project_id: str, max_depth: int = 10, 
                            include_custom_attributes: bool = True, 
                            performance_mode: str = None) -> Dict[str, Any]:
        """
        啟動全量同步 - 重構版本
        
        Args:
            project_id: 項目ID
            max_depth: 最大深度
            include_custom_attributes: 是否包含自定義屬性
            performance_mode: 性能模式，如果為None則使用當前模式
        
        Returns:
            同步結果
        """
        
        # 使用指定的性能模式或當前模式
        if performance_mode is None:
            performance_mode = self.current_performance_mode
        
        logger.info(f"🚀 啟動全量同步: 項目 {project_id}, 性能模式: {performance_mode}")
        
        try:
            # 驗證參數
            validation = AuthUtils.validate_sync_parameters(
                'full_sync', performance_mode, max_depth, include_custom_attributes
            )
            if not validation['valid']:
                return {
                    'status': 'error',
                    'error': f"參數驗證失敗: {', '.join(validation['errors'])}"
                }
            
            # 生成任務UUID
            task_uuid = TaskManager.generate_task_uuid()
            
            # 獲取認證頭
            headers = AuthUtils.get_auth_headers_safe()
            if not headers:
                return {
                    'status': 'error',
                    'error': '無法獲取認證信息',
                    'task_uuid': task_uuid
                }
            
            # 調整同步管理器參數
            if performance_mode != self.current_performance_mode:
                SyncManagerFactory.adjust_sync_manager(self.sync_manager, performance_mode)
                self.current_performance_mode = performance_mode
            
            # 創建同步任務記錄
            parameters = {
                    'max_depth': max_depth,
                    'include_custom_attributes': include_custom_attributes
            }
            
            task_created = await TaskManager.create_sync_task_record(
                project_id, task_uuid, 'full_sync', performance_mode, parameters
            )
            
            if not task_created:
                logger.warning(f"任務記錄創建失敗，但繼續執行同步: {task_uuid}")
            
            # 執行全量同步
            result = await SyncExecutionUtils.execute_sync(
                self.sync_manager, 'full_sync', project_id, 
                max_depth, include_custom_attributes, task_uuid
            )
            
            # 添加額外信息
            result['task_uuid'] = task_uuid
            result['performance_mode'] = performance_mode
            result['sync_type'] = 'full_sync'
            
            # 完成同步任務記錄
            if result.get('status') == 'success':
                await TaskManager.complete_sync_task_record(
                    task_uuid, result, self.sync_manager._get_performance_stats()
                )
            elif result.get('status') == 'error':
                await TaskManager.fail_sync_task_record(
                    task_uuid, result.get('error', 'Unknown error'), 
                    {'sync_type': 'full_sync', 'project_id': project_id}
                )
            
            logger.info(f"✅ 全量同步完成: {result.get('status', 'unknown')}")
            return result
            
        except Exception as e:
            logger.error(f"❌ 全量同步失敗: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'task_uuid': task_uuid if 'task_uuid' in locals() else None
            }
    
    async def start_incremental_sync(self, project_id: str, max_depth: int = 10, 
                                   include_custom_attributes: bool = True, 
                                   performance_mode: str = None,
                                   enable_top_level_rollup_check: bool = True) -> Dict[str, Any]:
        """
        啟動增量同步 - 重構版本，包含頂層rollup檢查優化
        
        Args:
            project_id: 項目ID
            max_depth: 最大深度
            include_custom_attributes: 是否包含自定義屬性
            performance_mode: 性能模式，如果為None則使用當前模式
            enable_top_level_rollup_check: 是否啟用頂層rollup檢查
        
        Returns:
            同步結果
        """
        
        # 使用指定的性能模式或當前模式
        if performance_mode is None:
            performance_mode = self.current_performance_mode
        
        logger.info(f"🔄 啟動增量同步: 項目 {project_id}, 性能模式: {performance_mode}")
        
        try:
            # 驗證參數
            validation = AuthUtils.validate_sync_parameters(
                'incremental_sync', performance_mode, max_depth, include_custom_attributes
            )
            if not validation['valid']:
                return {
                    'status': 'error',
                    'error': f"參數驗證失敗: {', '.join(validation['errors'])}"
                }
            
            # 生成任務UUID
            task_uuid = TaskManager.generate_task_uuid()
            
            # 🔑 關鍵優化：頂層rollup時間檢查
            if enable_top_level_rollup_check:
                rollup_check_result = await RollupCheckUtils.check_project_top_level_rollup(
                    project_id, self.sync_manager
                )
                
                if rollup_check_result.get('can_skip_entire_project'):
                    logger.info(f"🚀 頂層rollup優化: 整個項目 {project_id} 可以跳過")
                    return {
                        'status': 'no_changes',
                        'message': 'Entire project skipped due to top-level rollup optimization',
                        'task_uuid': task_uuid,
                        'performance_mode': performance_mode,
                        'folders_synced': 0,
                        'files_synced': 0,
                        'custom_attrs_synced': 0,
                        'optimization_efficiency': 100.0,
                        'top_level_rollup_optimization': True,
                        'rollup_check_details': rollup_check_result
                    }
            
            # 獲取認證頭
            headers = AuthUtils.get_auth_headers_safe()
            if not headers:
                return {
                    'status': 'error',
                    'error': '無法獲取認證信息',
                    'task_uuid': task_uuid
                }
            
            # 調整同步管理器參數
            if performance_mode != self.current_performance_mode:
                SyncManagerFactory.adjust_sync_manager(self.sync_manager, performance_mode)
                self.current_performance_mode = performance_mode
            
            # 創建同步任務記錄
            parameters = {
                    'max_depth': max_depth,
                'include_custom_attributes': include_custom_attributes,
                'enable_top_level_rollup_check': enable_top_level_rollup_check
            }
            
            task_created = await TaskManager.create_sync_task_record(
                project_id, task_uuid, 'incremental_sync', performance_mode, parameters
            )
            
            if not task_created:
                logger.warning(f"任務記錄創建失敗，但繼續執行同步: {task_uuid}")
            
            # 執行增量同步
            result = await SyncExecutionUtils.execute_sync(
                self.sync_manager, 'incremental_sync', project_id, 
                max_depth, include_custom_attributes, task_uuid
            )
            
            # 添加額外信息
            result['task_uuid'] = task_uuid
            result['performance_mode'] = performance_mode
            result['sync_type'] = 'incremental_sync'
            result['top_level_rollup_check'] = enable_top_level_rollup_check
            
            # 完成同步任務記錄
            if result.get('status') == 'success':
                await TaskManager.complete_sync_task_record(
                    task_uuid, result, self.sync_manager._get_performance_stats()
                )
            elif result.get('status') == 'error':
                await TaskManager.fail_sync_task_record(
                    task_uuid, result.get('error', 'Unknown error'), 
                    {'sync_type': 'incremental_sync', 'project_id': project_id}
                )
            
            logger.info(f"✅ 增量同步完成: {result.get('status', 'unknown')}")
            return result
            
        except Exception as e:
            logger.error(f"❌ 增量同步失敗: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'task_uuid': task_uuid if 'task_uuid' in locals() else None
            }
    
    async def get_sync_status(self, task_uuid: str) -> Dict[str, Any]:
        """
        获取同步任务状态
        
        Args:
            task_uuid: 任务UUID
        
        Returns:
            任务状态信息
        """
        
        try:
            dal = await get_optimized_postgresql_dal()
            
            async with dal.get_connection() as conn:
                query = """
                SELECT 
                    task_uuid,
                    project_id,
                    task_type,
                    task_status,
                    performance_mode,
                    parameters,
                    progress,
                    performance_stats,
                    results,
                    start_time,
                    end_time,
                    duration_seconds,
                    created_at,
                    updated_at
                FROM sync_tasks 
                WHERE task_uuid = $1;
                """
                
                row = await conn.fetchrow(query, task_uuid)
                
                if not row:
                    return {
                        'status': 'error',
                        'error': f'任务 {task_uuid} 不存在'
                    }
                
                return dal._row_to_dict(row)
                
        except Exception as e:
            logger.error(f"获取同步状态失败: {e}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    async def get_project_sync_history(self, project_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取项目同步历史
        
        Args:
            project_id: 项目ID
            limit: 返回记录数限制
        
        Returns:
            同步历史记录列表
        """
        
        try:
            dal = await get_optimized_postgresql_dal()
            
            async with dal.get_connection() as conn:
                query = """
                SELECT 
                    task_uuid,
                    task_type,
                    task_status,
                    performance_mode,
                    start_time,
                    end_time,
                    duration_seconds,
                    results
                FROM sync_tasks 
                WHERE project_id = $1
                ORDER BY start_time DESC
                LIMIT $2;
                """
                
                rows = await conn.fetch(query, project_id, limit)
                return [dal._row_to_dict(row) for row in rows]
                
        except Exception as e:
            logger.error(f"获取同步历史失败: {e}")
            return []
    
    async def get_sync_performance_stats(self, project_id: str, 
                                       start_date: Optional[datetime] = None,
                                       end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        获取同步性能统计
        
        Args:
            project_id: 项目ID
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            性能统计信息
        """
        
        try:
            dal = await get_optimized_postgresql_dal()
            
            async with dal.get_connection() as conn:
                # 构建查询条件
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
                    COUNT(*) as total_syncs,
                    AVG(duration_seconds) as avg_duration,
                    MIN(duration_seconds) as min_duration,
                    MAX(duration_seconds) as max_duration,
                    SUM(CAST(results->>'folders_synced' AS INTEGER)) as total_folders_synced,
                    SUM(CAST(results->>'files_synced' AS INTEGER)) as total_files_synced,
                    SUM(CAST(results->>'custom_attrs_synced' AS INTEGER)) as total_custom_attrs_synced,
                    AVG(CAST(performance_stats->>'optimization_efficiency' AS FLOAT)) as avg_optimization_efficiency
                FROM sync_tasks 
                WHERE {' AND '.join(conditions)};
                """
                
                row = await conn.fetchrow(query, *params)
                
                if row:
                    stats = dal._row_to_dict(row)
                    
                    # 计算额外统计信息
                    stats['performance_grade'] = self._calculate_performance_grade(stats)
                    stats['efficiency_trend'] = await self._get_efficiency_trend(dal, project_id, start_date, end_date)
                    
                    return stats
                else:
                    return {'message': '没有找到同步记录'}
                
        except Exception as e:
            logger.error(f"获取性能统计失败: {e}")
            return {'error': str(e)}
    
    def _adjust_sync_manager_for_performance_mode(self, performance_mode: str):
        """根据性能模式调整同步管理器参数"""
        
        if performance_mode == 'high_performance':
            # 高性能模式：更大的批量大小，更多的并发
            self.sync_manager.batch_size = 200
            self.sync_manager.max_workers = 16
            self.sync_manager.api_delay = 0.01
            self.sync_manager.memory_threshold_mb = 2048
            
        elif performance_mode == 'memory_optimized':
            # 内存优化模式：较小的批量大小，较少的并发
            self.sync_manager.batch_size = 50
            self.sync_manager.max_workers = 4
            self.sync_manager.api_delay = 0.05
            self.sync_manager.memory_threshold_mb = 512
            
        else:  # standard
            # 标准模式：平衡的参数
            self.sync_manager.batch_size = 100
            self.sync_manager.max_workers = 8
            self.sync_manager.api_delay = 0.02
            self.sync_manager.memory_threshold_mb = 1024
        
        logger.info(f"同步管理器已调整为 {performance_mode} 模式")
    
    def _calculate_performance_grade(self, stats: Dict[str, Any]) -> str:
        """计算性能等级"""
        
        avg_duration = stats.get('avg_duration', 0)
        avg_efficiency = stats.get('avg_optimization_efficiency', 0)
        
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
    
    async def _get_efficiency_trend(self, dal, project_id: str, 
                                  start_date: Optional[datetime], 
                                  end_date: Optional[datetime]) -> str:
        """获取效率趋势"""
        
        try:
            async with dal.get_connection() as conn:
                # 获取最近的同步记录，按时间排序
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
                
                # 计算趋势
                recent_avg = sum(efficiencies[:3]) / min(3, len(efficiencies))
                older_avg = sum(efficiencies[-3:]) / min(3, len(efficiencies[-3:]))
                
                if recent_avg > older_avg + 5:
                    return 'improving'
                elif recent_avg < older_avg - 5:
                    return 'declining'
                else:
                    return 'stable'
                    
        except Exception as e:
            logger.warning(f"获取效率趋势失败: {e}")
            return 'unknown'

# ============================================================================
# 🚀 全局服務實例和便捷函數
# ============================================================================

# 全局PostgreSQL同步服務實例
postgresql_sync_service = PostgreSQLSyncService()

# 便捷函數 - 重構版本
async def start_full_sync(project_id: str, **kwargs) -> Dict[str, Any]:
    """啟動全量同步的便捷函數"""
    return await postgresql_sync_service.start_full_sync(project_id, **kwargs)

async def start_incremental_sync(project_id: str, **kwargs) -> Dict[str, Any]:
    """啟動增量同步的便捷函數"""
    return await postgresql_sync_service.start_incremental_sync(project_id, **kwargs)

async def get_sync_status(task_uuid: str) -> Dict[str, Any]:
    """獲取同步狀態的便捷函數"""
    return await postgresql_sync_service.get_sync_status(task_uuid)

async def get_project_sync_history(project_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """獲取項目同步歷史的便捷函數"""
    return await postgresql_sync_service.get_project_sync_history(project_id, limit)

async def get_sync_performance_stats(project_id: str, **kwargs) -> Dict[str, Any]:
    """獲取同步性能統計的便捷函數"""
    return await postgresql_sync_service.get_sync_performance_stats(project_id, **kwargs)

# 工廠函數
def create_sync_service(performance_mode: str = 'standard') -> PostgreSQLSyncService:
    """創建新的同步服務實例"""
    return PostgreSQLSyncService(performance_mode)

def get_available_performance_modes() -> List[str]:
    """獲取可用的性能模式"""
    return SyncManagerFactory.get_available_modes()