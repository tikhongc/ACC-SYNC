"""
獨立的任務生命週期管理器
完全獨立於同步邏輯，專門處理任務狀態追蹤和清理
"""

import threading
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)

class TaskLifecycleManager:
    """
    任務生命週期管理器
    - 獨立於業務邏輯
    - 自動清理過期任務
    - 提供統一的任務狀態查詢接口
    """
    
    def __init__(self):
        self._tasks: Dict[str, Dict[str, Any]] = {}
        self._cleanup_thread = None
        self._cleanup_interval = 300  # 5分鐘清理一次
        self._task_ttl = 1800  # 任務30分鐘後過期
        self._running = False
        self._lock = threading.RLock()
    
    def start(self):
        """啟動管理器"""
        if self._running:
            return
            
        self._running = True
        self._cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self._cleanup_thread.start()
        logger.info("🚀 Task Lifecycle Manager started")
    
    def stop(self):
        """停止管理器"""
        self._running = False
        if self._cleanup_thread:
            self._cleanup_thread.join(timeout=5)
        logger.info("🛑 Task Lifecycle Manager stopped")
    
    def register_task(self, task_id: str, initial_data: Dict[str, Any] = None) -> None:
        """註冊新任務"""
        with self._lock:
            self._tasks[task_id] = {
                'created_at': datetime.now(),
                'last_updated': datetime.now(),
                'status': 'running',
                'data': initial_data or {},
                'access_count': 0
            }
            logger.debug(f"📝 Task registered: {task_id}")
    
    def update_task(self, task_id: str, data: Dict[str, Any]) -> None:
        """更新任務數據"""
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id]['data'].update(data)
                self._tasks[task_id]['last_updated'] = datetime.now()
                
                # 自動檢測完成狀態
                if data.get('current_stage') == 'completed' or data.get('task_status') == 'completed':
                    self._tasks[task_id]['status'] = 'completed'
                    logger.debug(f"✅ Task marked as completed: {task_id}")
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """獲取任務狀態（用於API響應）"""
        with self._lock:
            if task_id not in self._tasks:
                return {
                    'exists': False,
                    'status': 'not_found',
                    'message': 'Task not found or expired'
                }
            
            task = self._tasks[task_id]
            task['access_count'] += 1
            
            # 檢查是否過期
            if self._is_task_expired(task):
                return {
                    'exists': True,
                    'status': 'expired',
                    'message': 'Task has expired',
                    'data': task['data']
                }
            
            return {
                'exists': True,
                'status': task['status'],
                'data': task['data'],
                'created_at': task['created_at'].isoformat(),
                'last_updated': task['last_updated'].isoformat()
            }
    
    def complete_task(self, task_id: str, results: Dict[str, Any] = None) -> None:
        """標記任務為完成"""
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id]['status'] = 'completed'
                self._tasks[task_id]['last_updated'] = datetime.now()
                if results:
                    self._tasks[task_id]['data']['results'] = results
                logger.info(f"🎉 Task completed: {task_id}")
    
    def fail_task(self, task_id: str, error: str) -> None:
        """標記任務為失敗"""
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id]['status'] = 'failed'
                self._tasks[task_id]['last_updated'] = datetime.now()
                self._tasks[task_id]['data']['error'] = error
                logger.warning(f"❌ Task failed: {task_id} - {error}")
    
    def _is_task_expired(self, task: Dict[str, Any]) -> bool:
        """檢查任務是否過期"""
        if task['status'] in ['completed', 'failed']:
            # 完成或失敗的任務，5分鐘後過期
            return datetime.now() - task['last_updated'] > timedelta(minutes=5)
        else:
            # 運行中的任務，30分鐘後過期
            return datetime.now() - task['last_updated'] > timedelta(seconds=self._task_ttl)
    
    def _cleanup_loop(self):
        """清理循環"""
        while self._running:
            try:
                self._cleanup_expired_tasks()
                time.sleep(self._cleanup_interval)
            except Exception as e:
                logger.error(f"Cleanup error: {e}")
    
    def _cleanup_expired_tasks(self):
        """清理過期任務"""
        with self._lock:
            expired_tasks = []
            for task_id, task in self._tasks.items():
                if self._is_task_expired(task):
                    expired_tasks.append(task_id)
            
            for task_id in expired_tasks:
                del self._tasks[task_id]
                logger.debug(f"🧹 Expired task cleaned: {task_id}")
            
            if expired_tasks:
                logger.info(f"🧹 Cleaned {len(expired_tasks)} expired tasks")
    
    def get_stats(self) -> Dict[str, Any]:
        """獲取統計信息"""
        with self._lock:
            total = len(self._tasks)
            running = sum(1 for t in self._tasks.values() if t['status'] == 'running')
            completed = sum(1 for t in self._tasks.values() if t['status'] == 'completed')
            failed = sum(1 for t in self._tasks.values() if t['status'] == 'failed')
            
            return {
                'total_tasks': total,
                'running_tasks': running,
                'completed_tasks': completed,
                'failed_tasks': failed,
                'cleanup_interval': self._cleanup_interval,
                'task_ttl': self._task_ttl
            }

# 全局實例
task_manager = TaskLifecycleManager()
