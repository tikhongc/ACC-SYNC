# -*- coding: utf-8 -*-
"""
PostgreSQL同步路由 - HTTP API層
提供RESTful API接口，使用重構後的服務層
專注於HTTP請求處理和響應格式化
"""

import asyncio
import logging
from datetime import datetime
from flask import Blueprint, jsonify, request
from typing import Dict, List, Any, Optional

from .postgresql_sync_service import postgresql_sync_service, create_sync_service
from .postgresql_sync_utils import (
    SyncManagerFactory, AuthUtils, RollupCheckUtils, 
    ResponseUtils, PerformanceUtils
)
from database_sql.optimized_data_access import get_optimized_postgresql_dal

logger = logging.getLogger(__name__)

# 創建藍圖
postgresql_sync_bp = Blueprint('postgresql_sync', __name__)

# ============================================================================
# 🚀 核心同步API端点
# ============================================================================

@postgresql_sync_bp.route('/api/postgresql-sync/project/<project_id>/sync', methods=['POST'])
def unified_sync_api(project_id):
    """
    統一的PostgreSQL項目同步API - 重構版本
    
    POST /api/postgresql-sync/project/{project_id}/sync
    
    參數:
    - syncType: 同步類型 ("full_sync" | "incremental_sync") (默認: "incremental_sync")
    - performanceMode: 性能模式 ("standard" | "high_performance" | "memory_optimized") (默認: "standard")
    - maxDepth: 最大遍歷深度 (默認: 10)
    - includeCustomAttributes: 是否包含自定義屬性 (默認: true)
    - enableTopLevelRollupCheck: 是否啟用頂層rollup檢查 (默認: true)
    """
    try:
        # 獲取和驗證參數
        request_data = request.json or {}
        sync_type = request_data.get('syncType', 'incremental_sync')
        performance_mode = request_data.get('performanceMode', 'standard')
        max_depth = request_data.get('maxDepth', 10)
        include_custom_attributes = request_data.get('includeCustomAttributes', True)
        enable_top_level_rollup_check = request_data.get('enableTopLevelRollupCheck', True)
        
        # 使用工具類驗證參數
        validation = AuthUtils.validate_sync_parameters(
            sync_type, performance_mode, max_depth, include_custom_attributes
        )
        
        if not validation['valid']:
            return jsonify(ResponseUtils.create_error_response(
                f"參數驗證失敗: {', '.join(validation['errors'])}", 
                "INVALID_PARAMETERS"
            )), 400
        
        logger.info(f"Starting {sync_type} for project {project_id} with {performance_mode} mode")
        
        # 執行同步 - 使用服務層
        def run_sync():
            if sync_type == 'full_sync':
                return asyncio.run(postgresql_sync_service.start_full_sync(
                    project_id=project_id,
                    max_depth=max_depth,
                    include_custom_attributes=include_custom_attributes,
                    performance_mode=performance_mode
                ))
            else:  # incremental_sync
                return asyncio.run(postgresql_sync_service.start_incremental_sync(
                    project_id=project_id,
                    max_depth=max_depth,
                    include_custom_attributes=include_custom_attributes,
                    performance_mode=performance_mode,
                    enable_top_level_rollup_check=enable_top_level_rollup_check
                ))
        
        # 在後台執行同步
        import threading
        
        def background_sync():
            try:
                result = run_sync()
                logger.info(f"Sync completed: {result.get('status', 'unknown')}")
            except Exception as e:
                logger.error(f"Background sync failed: {e}")
        
        # 立即執行以獲取任務ID和初始狀態
        result = run_sync()
        
        # 如果是no_changes狀態，直接返回
        if result.get('status') == 'no_changes':
            return jsonify(ResponseUtils.create_success_response(
                result, "Project skipped due to optimization"
            )), 200
        
        # 如果有錯誤，直接返回
        if result.get('status') == 'error':
            return jsonify(ResponseUtils.create_error_response(
                result.get('error', 'Unknown error'), "SYNC_ERROR"
            )), 500
        
        # 返回成功響應
        response_data = ResponseUtils.create_sync_response(
            task_id=result.get('task_uuid', 'unknown'),
            sync_type=sync_type,
            performance_mode=performance_mode,
            status="started",
            message=f"PostgreSQL {sync_type} started successfully",
            top_level_rollup_check=enable_top_level_rollup_check
        )
        
        return jsonify(response_data), 202
        
    except Exception as e:
        logger.error(f"PostgreSQL sync API error: {e}")
        return jsonify(ResponseUtils.create_error_response(
            str(e), "API_ERROR"
        )), 500

@postgresql_sync_bp.route('/api/postgresql-sync/project/<project_id>/status/<task_id>', methods=['GET'])
def get_sync_status(project_id, task_id):
    """獲取PostgreSQL同步任務狀態 - 重構版本"""
    try:
        # 使用服務層獲取狀態
        def get_status():
            return asyncio.run(postgresql_sync_service.get_sync_status(task_id))
        
        result = get_status()
        
        if result.get('status') == 'error':
            return jsonify(ResponseUtils.create_error_response(
                result.get('error', 'Task not found'), "TASK_NOT_FOUND"
            )), 404
        
        return jsonify(ResponseUtils.create_success_response(
            result, "Task status retrieved successfully"
        )), 200
        
    except Exception as e:
        logger.error(f"Get sync status error: {e}")
        return jsonify(ResponseUtils.create_error_response(
            str(e), "STATUS_ERROR"
        )), 500

@postgresql_sync_bp.route('/api/postgresql-sync/project/<project_id>/rollup-check', methods=['GET'])
def check_rollup_status(project_id):
    """
    🚀 新增：检查项目顶层rollup状态
    这是关键的优化端点，可以在同步前快速判断是否需要同步
    """
    try:
        # 获取查询参数
        last_sync_time_str = request.args.get('lastSyncTime')
        
        if not last_sync_time_str:
            return jsonify({
                "success": False,
                "error": "lastSyncTime parameter is required"
            }), 400
        
        # 解析时间
        try:
            last_sync_time = datetime.fromisoformat(last_sync_time_str.replace('Z', '+00:00'))
        except ValueError:
            return jsonify({
                "success": False,
                "error": "Invalid lastSyncTime format. Use ISO format."
            }), 400
        
        # 执行顶层rollup检查
        def check_rollup():
            sync_manager = sync_managers['standard']
            return asyncio.run(_check_project_top_level_rollup(project_id, sync_manager, last_sync_time))
        
        rollup_result = check_rollup()
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "last_sync_time": last_sync_time_str,
            "rollup_check_result": rollup_result
        }), 200
        
    except Exception as e:
        logger.error(f"Rollup check error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ============================================================================
# 🚀 性能监控和统计API
# ============================================================================

@optimized_postgresql_sync_bp.route('/api/optimized-postgresql-sync/project/<project_id>/performance-stats', methods=['GET'])
def get_postgresql_performance_stats(project_id):
    """获取PostgreSQL同步性能统计"""
    try:
        def get_stats():
            return asyncio.run(_get_postgresql_performance_stats(project_id))
        
        stats = get_stats()
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "performance_stats": stats
        }), 200
        
    except Exception as e:
        logger.error(f"Get performance stats error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@optimized_postgresql_sync_bp.route('/api/optimized-postgresql-sync/project/<project_id>/optimization-report', methods=['GET'])
def get_optimization_report(project_id):
    """获取优化报告"""
    try:
        def get_report():
            return asyncio.run(_generate_optimization_report(project_id))
        
        report = get_report()
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "optimization_report": report
        }), 200
        
    except Exception as e:
        logger.error(f"Get optimization report error: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ============================================================================
# 🚀 辅助函数
# ============================================================================

async def _check_project_top_level_rollup(project_id: str, sync_manager: OptimizedPostgreSQLSyncManager, 
                                        last_sync_time: Optional[datetime] = None) -> Dict[str, Any]:
    """
    🔑 关键优化：检查项目顶层rollup时间
    这是最重要的优化 - 可以在不调用任何API的情况下判断整个项目是否需要同步
    """
    try:
        dal = await get_optimized_postgresql_dal()
        
        # 如果没有提供last_sync_time，从数据库获取
        if not last_sync_time:
            last_sync_time = await dal.get_project_last_sync_time(project_id)
            
        if not last_sync_time:
            return {
                'can_skip_entire_project': False,
                'reason': 'No previous sync time found',
                'recommendation': 'Perform full sync'
            }
        
        # 🚀 核心优化：获取项目顶层文件夹的最大rollup时间
        async with dal.get_connection() as conn:
            query = """
            SELECT 
                MAX(last_modified_time_rollup) as max_rollup_time,
                COUNT(*) as total_top_level_folders,
                COUNT(CASE WHEN last_modified_time_rollup > $2 THEN 1 END) as folders_with_changes
            FROM folders 
            WHERE project_id = $1 
              AND (parent_id IS NULL OR parent_id = '')
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
            
            # 🎯 关键判断：如果最大rollup时间 <= 上次同步时间，整个项目都可以跳过
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

async def _execute_postgresql_sync(sync_manager: OptimizedPostgreSQLSyncManager, sync_type: str, 
                                 project_id: str, max_depth: int, include_custom_attributes: bool, 
                                 task_id: str) -> Dict[str, Any]:
    """执行PostgreSQL同步"""
    try:
        headers = get_auth_headers()
        
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
        logger.error(f"PostgreSQL sync execution failed: {e}")
        return {
            'status': 'error',
            'error': str(e),
            'task_id': task_id
        }

async def _get_postgresql_performance_stats(project_id: str) -> Dict[str, Any]:
    """获取PostgreSQL性能统计"""
    try:
        dal = await get_optimized_postgresql_dal()
        
        async with dal.get_connection() as conn:
            # 获取项目统计信息
            stats_query = """
            SELECT 
                COUNT(DISTINCT f.id) as total_folders,
                COUNT(DISTINCT fi.id) as total_files,
                COUNT(DISTINCT cav.id) as total_custom_attributes,
                MAX(f.last_modified_time_rollup) as latest_rollup_time,
                MAX(f.updated_at) as latest_sync_time
            FROM folders f
            LEFT JOIN files fi ON fi.project_id = f.project_id
            LEFT JOIN custom_attribute_values cav ON cav.project_id = f.project_id
            WHERE f.project_id = $1
            """
            
            stats = await conn.fetchrow(stats_query, project_id)
            
            return {
                'project_id': project_id,
                'total_folders': stats['total_folders'] or 0,
                'total_files': stats['total_files'] or 0,
                'total_custom_attributes': stats['total_custom_attributes'] or 0,
                'latest_rollup_time': stats['latest_rollup_time'].isoformat() if stats['latest_rollup_time'] else None,
                'latest_sync_time': stats['latest_sync_time'].isoformat() if stats['latest_sync_time'] else None,
                'database_type': 'PostgreSQL',
                'optimization_features': [
                    'separated_custom_attributes',
                    'batch_upsert_operations',
                    'smart_branch_skipping',
                    'top_level_rollup_optimization',
                    'concurrent_processing'
                ]
            }
            
    except Exception as e:
        logger.error(f"Get PostgreSQL performance stats failed: {e}")
        return {
            'error': str(e),
            'project_id': project_id
        }

async def _generate_optimization_report(project_id: str) -> Dict[str, Any]:
    """生成优化报告"""
    try:
        dal = await get_optimized_postgresql_dal()
        
        # 获取最近的同步任务统计
        async with dal.get_connection() as conn:
            recent_tasks_query = """
            SELECT 
                task_type,
                performance_mode,
                results,
                performance_stats,
                duration_seconds,
                created_at
            FROM sync_tasks 
            WHERE project_id = $1 
              AND task_status = 'completed'
            ORDER BY created_at DESC 
            LIMIT 10
            """
            
            recent_tasks = await conn.fetch(recent_tasks_query, project_id)
            
            # 计算优化效果
            total_tasks = len(recent_tasks)
            if total_tasks == 0:
                return {
                    'project_id': project_id,
                    'message': 'No completed sync tasks found',
                    'recommendation': 'Run a sync to generate optimization report'
                }
            
            # 分析性能趋势
            avg_duration = sum(task['duration_seconds'] or 0 for task in recent_tasks) / total_tasks
            
            # 分析优化效率
            optimization_efficiencies = []
            for task in recent_tasks:
                perf_stats = task.get('performance_stats', {})
                if isinstance(perf_stats, dict):
                    efficiency = perf_stats.get('optimization_efficiency', 0)
                    if efficiency > 0:
                        optimization_efficiencies.append(efficiency)
            
            avg_optimization_efficiency = sum(optimization_efficiencies) / len(optimization_efficiencies) if optimization_efficiencies else 0
            
            return {
                'project_id': project_id,
                'analysis_period': f'Last {total_tasks} completed syncs',
                'performance_summary': {
                    'average_sync_duration_seconds': round(avg_duration, 2),
                    'average_optimization_efficiency': round(avg_optimization_efficiency, 1),
                    'total_completed_syncs': total_tasks
                },
                'optimization_features_active': [
                    'Top-level rollup time checking',
                    'Smart branch skipping',
                    'Batch API operations',
                    'Separated custom attributes tables',
                    'Concurrent processing with priority scheduling',
                    'Memory management and monitoring'
                ],
                'recommendations': [
                    'Enable top-level rollup checking for maximum efficiency',
                    'Use high_performance mode for large projects',
                    'Monitor optimization efficiency trends',
                    'Consider full sync if efficiency drops below 50%'
                ],
                'database_optimization_status': 'PostgreSQL with separated tables - Optimal'
            }
            
    except Exception as e:
        logger.error(f"Generate optimization report failed: {e}")
        return {
            'project_id': project_id,
            'error': str(e)
        }

# ============================================================================
# 🚀 額外的便捷端點
# ============================================================================

@postgresql_sync_bp.route('/api/postgresql-sync/performance-modes', methods=['GET'])
def get_performance_modes():
    """獲取可用的性能模式"""
    try:
        modes = SyncManagerFactory.get_available_modes()
        configs = {mode: SyncManagerFactory.PERFORMANCE_CONFIGS[mode] for mode in modes}
        
        return jsonify(ResponseUtils.create_success_response({
            'available_modes': modes,
            'configurations': configs
        }, "Performance modes retrieved successfully")), 200
        
    except Exception as e:
        logger.error(f"Get performance modes error: {e}")
        return jsonify(ResponseUtils.create_error_response(
            str(e), "MODES_ERROR"
        )), 500

@postgresql_sync_bp.route('/api/postgresql-sync/project/<project_id>/performance-stats', methods=['GET'])
def get_performance_stats(project_id):
    """獲取項目性能統計"""
    try:
        def get_stats():
            return asyncio.run(postgresql_sync_service.get_sync_performance_stats(project_id))
        
        result = get_stats()
        
        return jsonify(ResponseUtils.create_success_response(
            result, "Performance stats retrieved successfully"
        )), 200
        
    except Exception as e:
        logger.error(f"Get performance stats error: {e}")
        return jsonify(ResponseUtils.create_error_response(
            str(e), "STATS_ERROR"
        )), 500

# ============================================================================
# 🚀 導出藍圖
# ============================================================================

def register_postgresql_sync_routes(app):
    """註冊PostgreSQL同步路由 - 重構版本"""
    app.register_blueprint(postgresql_sync_bp)
    logger.info("PostgreSQL sync routes registered successfully")

# 向後兼容的函數名
def register_optimized_postgresql_sync_routes(app):
    """向後兼容的註冊函數"""
    register_postgresql_sync_routes(app)
    logger.warning("Using deprecated function name. Please use register_postgresql_sync_routes instead.")
