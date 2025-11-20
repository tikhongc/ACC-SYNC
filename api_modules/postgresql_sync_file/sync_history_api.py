# -*- coding: utf-8 -*-
"""
统一同步历史API - 支持多模块同步历史查看
提供统一的界面查看所有同步任务历史，包括未来的review等模块
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from flask import Blueprint, request, jsonify

from database_sql.optimized_data_access import get_optimized_postgresql_dal

logger = logging.getLogger(__name__)

# 创建蓝图
sync_history_bp = Blueprint('sync_history', __name__)

# ============================================================================
# 统一同步历史API
# ============================================================================

@sync_history_bp.route('/api/sync-history/project/<project_id>', methods=['GET'])
def get_project_sync_history(project_id):
    """
    获取项目的同步历史
    
    GET /api/sync-history/project/{project_id}
    
    查询参数:
    - limit: 返回记录数量限制 (默认: 20, 最大: 100)
    - offset: 偏移量 (默认: 0)
    - module_type: 模块类型过滤 ('file_management', 'review', 'permission', 'custom_attributes')
    - task_type: 任务类型过滤 ('full_sync', 'incremental_sync', 等)
    - status: 状态过滤 ('completed', 'failed', 'running', 等)
    - start_date: 开始日期过滤 (ISO格式)
    - end_date: 结束日期过滤 (ISO格式)
    """
    try:
        # 获取查询参数
        limit = min(int(request.args.get('limit', 20)), 100)
        offset = int(request.args.get('offset', 0))
        module_type = request.args.get('module_type')
        task_type = request.args.get('task_type')
        status = request.args.get('status')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # 构建查询条件
        conditions = ["project_id = $1"]
        params = [project_id]
        param_count = 1
        
        if module_type:
            param_count += 1
            conditions.append(f"module_type = ${param_count}")
            params.append(module_type)
        
        if task_type:
            param_count += 1
            conditions.append(f"task_type = ${param_count}")
            params.append(task_type)
        
        if status:
            param_count += 1
            conditions.append(f"task_status = ${param_count}")
            params.append(status)
        
        if start_date:
            param_count += 1
            conditions.append(f"start_time >= ${param_count}")
            params.append(datetime.fromisoformat(start_date.replace('Z', '+00:00')))
        
        if end_date:
            param_count += 1
            conditions.append(f"start_time <= ${param_count}")
            params.append(datetime.fromisoformat(end_date.replace('Z', '+00:00')))
        
        # 执行查询
        def run_query():
            import asyncio
            return asyncio.run(_get_sync_history_data(conditions, params, limit, offset))
        
        result = run_query()
        
        return jsonify({
            "success": True,
            "data": {
                "sync_history": result['history'],
                "total_count": result['total_count'],
                "limit": limit,
                "offset": offset,
                "project_id": project_id
            },
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"获取项目同步历史失败: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "error_code": "SYNC_HISTORY_ERROR"
        }), 500

@sync_history_bp.route('/api/sync-history/project/<project_id>/summary', methods=['GET'])
def get_project_sync_summary(project_id):
    """
    获取项目同步摘要统计
    
    GET /api/sync-history/project/{project_id}/summary
    """
    try:
        def run_query():
            import asyncio
            return asyncio.run(_get_project_sync_summary(project_id))
        
        summary = run_query()
        
        return jsonify({
            "success": True,
            "data": summary,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"获取项目同步摘要失败: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "error_code": "SYNC_SUMMARY_ERROR"
        }), 500

@sync_history_bp.route('/api/sync-history/all-projects/summary', methods=['GET'])
def get_all_projects_sync_summary():
    """
    获取所有项目的同步摘要
    
    GET /api/sync-history/all-projects/summary
    
    查询参数:
    - days: 统计天数 (默认: 7)
    """
    try:
        days = int(request.args.get('days', 7))
        
        def run_query():
            import asyncio
            return asyncio.run(_get_all_projects_summary(days))
        
        summary = run_query()
        
        return jsonify({
            "success": True,
            "data": summary,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"获取所有项目同步摘要失败: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "error_code": "ALL_PROJECTS_SUMMARY_ERROR"
        }), 500

@sync_history_bp.route('/api/sync-history/task/<task_uuid>', methods=['GET'])
def get_sync_task_details(task_uuid):
    """
    获取特定同步任务的详细信息
    
    GET /api/sync-history/task/{task_uuid}
    """
    try:
        def run_query():
            import asyncio
            return asyncio.run(_get_task_details(task_uuid))
        
        task_details = run_query()
        
        if not task_details:
            return jsonify({
                "success": False,
                "error": f"任务 {task_uuid} 不存在",
                "error_code": "TASK_NOT_FOUND"
            }), 404
        
        return jsonify({
            "success": True,
            "data": task_details,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"获取任务详情失败: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "error_code": "TASK_DETAILS_ERROR"
        }), 500

# ============================================================================
# 数据查询函数
# ============================================================================

async def _get_sync_history_data(conditions: List[str], params: List[Any], 
                                limit: int, offset: int) -> Dict[str, Any]:
    """获取同步历史数据"""
    dal = await get_optimized_postgresql_dal()
    
    async with dal.get_connection() as conn:
        # 构建查询语句
        where_clause = " AND ".join(conditions)
        
        # 获取总数
        count_query = f"""
        SELECT COUNT(*) as total_count
        FROM sync_tasks
        WHERE {where_clause}
        """
        
        count_result = await conn.fetchrow(count_query, *params)
        total_count = count_result['total_count']
        
        # 获取历史数据
        history_query = f"""
        SELECT 
            task_uuid,
            project_id,
            task_type,
            module_type,
            task_status,
            performance_mode,
            
            -- 同步内容标记
            synced_file_tree,
            synced_versions,
            synced_custom_attributes_definitions,
            synced_custom_attributes_values,
            synced_permissions,
            synced_reviews,
            
            -- 统计信息
            folders_synced,
            files_synced,
            versions_synced,
            custom_attrs_synced,
            permissions_synced,
            reviews_synced,
            
            -- 时间信息
            start_time,
            end_time,
            duration_seconds,
            
            -- 用户信息
            started_by_user_name,
            
            -- 错误信息
            error_message,
            
            created_at
        FROM sync_tasks
        WHERE {where_clause}
        ORDER BY start_time DESC
        LIMIT ${len(params) + 1} OFFSET ${len(params) + 2}
        """
        
        params.extend([limit, offset])
        rows = await conn.fetch(history_query, *params)
        
        # 转换为字典列表
        history = []
        for row in rows:
            task_data = dict(row)
            
            # 生成同步内容摘要
            sync_content = []
            if task_data['synced_file_tree']:
                sync_content.append('文件树')
            if task_data['synced_versions']:
                sync_content.append('版本')
            if task_data['synced_custom_attributes_definitions'] or task_data['synced_custom_attributes_values']:
                sync_content.append('自定义属性')
            if task_data['synced_permissions']:
                sync_content.append('权限')
            if task_data['synced_reviews']:
                sync_content.append('评审')
            
            task_data['sync_content_summary'] = '+'.join(sync_content) if sync_content else '无'
            
            # 格式化时间
            if task_data['start_time']:
                task_data['start_time'] = task_data['start_time'].isoformat()
            if task_data['end_time']:
                task_data['end_time'] = task_data['end_time'].isoformat()
            if task_data['created_at']:
                task_data['created_at'] = task_data['created_at'].isoformat()
            
            history.append(task_data)
        
        return {
            'history': history,
            'total_count': total_count
        }

async def _get_project_sync_summary(project_id: str) -> Dict[str, Any]:
    """获取项目同步摘要"""
    dal = await get_optimized_postgresql_dal()
    
    async with dal.get_connection() as conn:
        query = """
        SELECT 
            COUNT(*) as total_syncs,
            COUNT(CASE WHEN task_status = 'completed' THEN 1 END) as successful_syncs,
            COUNT(CASE WHEN task_status = 'failed' THEN 1 END) as failed_syncs,
            COUNT(CASE WHEN task_status = 'running' THEN 1 END) as running_syncs,
            COUNT(CASE WHEN task_type = 'full_sync' THEN 1 END) as full_syncs,
            COUNT(CASE WHEN task_type LIKE '%incremental%' THEN 1 END) as incremental_syncs,
            MAX(start_time) as last_sync_time,
            MAX(CASE WHEN task_status = 'completed' THEN start_time END) as last_successful_sync,
            AVG(CASE WHEN task_status = 'completed' THEN duration_seconds END) as avg_duration_seconds,
            SUM(folders_synced) as total_folders_synced,
            SUM(files_synced) as total_files_synced,
            SUM(versions_synced) as total_versions_synced,
            SUM(custom_attrs_synced) as total_custom_attrs_synced,
            
            -- 按模块统计
            COUNT(CASE WHEN module_type = 'file_management' THEN 1 END) as file_management_syncs,
            COUNT(CASE WHEN module_type = 'review' THEN 1 END) as review_syncs,
            COUNT(CASE WHEN module_type = 'permission' THEN 1 END) as permission_syncs,
            COUNT(CASE WHEN module_type = 'custom_attributes' THEN 1 END) as custom_attributes_syncs
        FROM sync_tasks
        WHERE project_id = $1
        """
        
        row = await conn.fetchrow(query, project_id)
        
        if not row:
            return {}
        
        summary = dict(row)
        
        # 格式化时间
        if summary['last_sync_time']:
            summary['last_sync_time'] = summary['last_sync_time'].isoformat()
        if summary['last_successful_sync']:
            summary['last_successful_sync'] = summary['last_successful_sync'].isoformat()
        
        # 计算成功率
        if summary['total_syncs'] > 0:
            summary['success_rate'] = round((summary['successful_syncs'] / summary['total_syncs']) * 100, 2)
        else:
            summary['success_rate'] = 0
        
        return summary

async def _get_all_projects_summary(days: int) -> Dict[str, Any]:
    """获取所有项目的同步摘要"""
    dal = await get_optimized_postgresql_dal()
    
    async with dal.get_connection() as conn:
        # 计算开始时间
        start_time = datetime.utcnow() - timedelta(days=days)
        
        query = """
        SELECT 
            project_id,
            COUNT(*) as total_syncs,
            COUNT(CASE WHEN task_status = 'completed' THEN 1 END) as successful_syncs,
            COUNT(CASE WHEN task_status = 'failed' THEN 1 END) as failed_syncs,
            MAX(start_time) as last_sync_time,
            AVG(CASE WHEN task_status = 'completed' THEN duration_seconds END) as avg_duration_seconds
        FROM sync_tasks
        WHERE start_time >= $1
        GROUP BY project_id
        ORDER BY last_sync_time DESC
        """
        
        rows = await conn.fetch(query, start_time)
        
        projects = []
        total_syncs = 0
        total_successful = 0
        total_failed = 0
        
        for row in rows:
            project_data = dict(row)
            
            # 格式化时间
            if project_data['last_sync_time']:
                project_data['last_sync_time'] = project_data['last_sync_time'].isoformat()
            
            # 计算成功率
            if project_data['total_syncs'] > 0:
                project_data['success_rate'] = round((project_data['successful_syncs'] / project_data['total_syncs']) * 100, 2)
            else:
                project_data['success_rate'] = 0
            
            projects.append(project_data)
            
            # 累计统计
            total_syncs += project_data['total_syncs']
            total_successful += project_data['successful_syncs']
            total_failed += project_data['failed_syncs']
        
        # 总体统计
        overall_success_rate = round((total_successful / total_syncs) * 100, 2) if total_syncs > 0 else 0
        
        return {
            'period_days': days,
            'total_projects': len(projects),
            'overall_stats': {
                'total_syncs': total_syncs,
                'successful_syncs': total_successful,
                'failed_syncs': total_failed,
                'success_rate': overall_success_rate
            },
            'projects': projects
        }

async def _get_task_details(task_uuid: str) -> Optional[Dict[str, Any]]:
    """获取任务详细信息"""
    dal = await get_optimized_postgresql_dal()
    
    async with dal.get_connection() as conn:
        query = """
        SELECT *
        FROM sync_tasks
        WHERE task_uuid = $1
        """
        
        row = await conn.fetchrow(query, task_uuid)
        
        if not row:
            return None
        
        task_details = dict(row)
        
        # 格式化时间
        time_fields = ['start_time', 'end_time', 'created_at', 'updated_at']
        for field in time_fields:
            if task_details.get(field):
                task_details[field] = task_details[field].isoformat()
        
        return task_details

# ============================================================================
# 工具函数
# ============================================================================

def format_duration(seconds: float) -> str:
    """格式化持续时间"""
    if not seconds:
        return "0秒"
    
    if seconds < 60:
        return f"{seconds:.1f}秒"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}分钟"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}小时"

def get_sync_status_display(status: str) -> Dict[str, str]:
    """获取同步状态的显示信息"""
    status_map = {
        'pending': {'text': '等待中', 'color': 'orange'},
        'running': {'text': '运行中', 'color': 'blue'},
        'completed': {'text': '已完成', 'color': 'green'},
        'failed': {'text': '失败', 'color': 'red'},
        'cancelled': {'text': '已取消', 'color': 'gray'}
    }
    
    return status_map.get(status, {'text': status, 'color': 'gray'})
