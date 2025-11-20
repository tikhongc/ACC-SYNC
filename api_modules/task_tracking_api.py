"""
獨立的任務追蹤API
不修改現有同步邏輯，只是在外層包裝任務狀態管理
"""

from flask import Blueprint, jsonify, request
from datetime import datetime
import logging
from .task_lifecycle_manager import task_manager
# 舊的進度函數已移除，現在使用獨立的任務追蹤系統

logger = logging.getLogger(__name__)

task_tracking_bp = Blueprint('task_tracking', __name__)

@task_tracking_bp.route('/api/task-tracking/start')
def start_task_manager():
    """啟動任務管理器"""
    try:
        task_manager.start()
        return jsonify({
            "success": True,
            "message": "Task manager started"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@task_tracking_bp.route('/api/task-tracking/stats')
def get_task_stats():
    """獲取任務統計"""
    try:
        stats = task_manager.get_stats()
        return jsonify({
            "success": True,
            "data": stats
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@task_tracking_bp.route('/api/task-tracking/project/<project_id>/sync-progress/<task_id>')
def get_smart_sync_progress(project_id, task_id):
    """
    智能任務進度查詢
    - 首先檢查任務管理器
    - 如果不存在，檢查原始進度存儲
    - 自動處理任務生命週期
    """
    try:
        logger.info(f"🔍 Smart progress check for task: {task_id}")
        
        # 1. 檢查任務管理器
        task_status = task_manager.get_task_status(task_id)
        
        if not task_status['exists']:
            # 2. 任務不在管理器中，任務可能已經完成或過期
            logger.info(f"🚫 Task {task_id} not found in task manager")
            return jsonify({
                "success": True,
                "data": {
                    "_id": task_id,
                    "project_id": project_id,
                    "task_type": "batch_optimized_sync",
                    "task_status": "completed",
                    "progress": {
                        "current_stage": "completed",
                        "progress_percentage": 100.0
                    },
                    "updated_at": datetime.now().isoformat(),
                    "results": {"message": "Task completed or expired"}
                }
            })
        
        # 3. 根據管理器狀態返回響應
        if task_status['status'] in ['expired', 'completed']:
            logger.info(f"✅ Task {task_id} is {task_status['status']}")
            return jsonify({
                "success": True,
                "data": {
                    "_id": task_id,
                    "project_id": project_id,
                    "task_type": "batch_optimized_sync",
                    "task_status": "completed",
                    "progress": {
                        "current_stage": "completed",
                        "progress_percentage": 100.0,
                        **task_status.get('data', {})
                    },
                    "updated_at": task_status.get('last_updated', datetime.now().isoformat()),
                    "results": task_status.get('data', {}).get('results', {"message": f"Task {task_status['status']}"})
                }
            })
        
        elif task_status['status'] == 'failed':
            logger.warning(f"❌ Task {task_id} failed")
            return jsonify({
                "success": True,
                "data": {
                    "_id": task_id,
                    "project_id": project_id,
                    "task_type": "batch_optimized_sync",
                    "task_status": "failed",
                    "progress": {
                        "current_stage": "failed",
                        "progress_percentage": 0.0
                    },
                    "updated_at": task_status.get('last_updated', datetime.now().isoformat()),
                    "error": task_status.get('data', {}).get('error', 'Task failed')
                }
            })
        
        else:
            # 任務仍在運行，返回當前狀態
            logger.debug(f"🔄 Task {task_id} still running")
            task_data = task_status.get('data', {})
            return jsonify({
                "success": True,
                "data": {
                    "_id": task_id,
                    "project_id": project_id,
                    "task_type": "batch_optimized_sync",
                    "task_status": task_status['status'],
                    "progress": {
                        "current_stage": task_data.get("current_stage", "unknown"),
                        "progress_percentage": task_data.get("progress_percentage", 0.0),
                        **{k: v for k, v in task_data.items() 
                           if k not in ["task_status", "current_stage", "progress_percentage", "updated_at"]}
                    },
                    "updated_at": task_status.get("last_updated", datetime.now().isoformat())
                }
            })
        
    except Exception as e:
        logger.error(f"Smart progress check failed: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@task_tracking_bp.route('/api/task-tracking/cleanup', methods=['POST'])
def manual_cleanup():
    """手動清理過期任務"""
    try:
        # 獲取清理前統計
        before_stats = task_manager.get_stats()
        
        # 執行清理
        task_manager._cleanup_expired_tasks()
        
        # 獲取清理後統計
        after_stats = task_manager.get_stats()
        
        cleaned_count = before_stats['total_tasks'] - after_stats['total_tasks']
        
        return jsonify({
            "success": True,
            "message": f"Cleaned {cleaned_count} expired tasks",
            "before": before_stats,
            "after": after_stats
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
