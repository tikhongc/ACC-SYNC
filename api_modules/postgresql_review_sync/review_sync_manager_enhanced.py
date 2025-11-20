"""
审批系统同步管理器 - 增强优化版
负责从ACC同步工作流、模板和评审数据到本地数据库

增强优化特性：
1. ✅ 批量UPSERT优化 - 使用PostgreSQL的ON CONFLICT语法
2. ✅ 增强性能监控 - 详细的性能追踪和瓶颈分析
3. ✅ 异步并行同步 (asyncio) - 比ThreadPoolExecutor更高效
4. ✅ 内存缓存层 (cachetools) - 减少重复API调用
5. ✅ 智能重试机制 - 指数退避和断路器模式
6. ✅ 内存优化 - 流式处理大数据集
7. ✅ 工作流模板同步 - 支持基础模板和详细API调用
8. ✅ 智能模板分析 - 自动识别模板类型和特征

注意：账户数据同步功能已移除，现在使用独立的 database_sql/account_sync.py
"""

import sys
import os
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timezone, timedelta
import uuid
import json
import time
import asyncio
import aiohttp
import threading
from functools import wraps, partial
from dataclasses import dataclass, asdict
from collections import defaultdict
import hashlib

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Override print to always flush output (fixes Windows console buffering)
print = partial(print, flush=True)

# Try different import paths
try:
    from database_sql.review_data_access import ReviewDataAccess
    from database_sql.neon_config import NeonConfig
    import psycopg2
    import psycopg2.extras
except ImportError:
    print("Warning: Could not import from database_sql, trying alternative path")
    try:
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../database_sql')))
        from review_data_access import ReviewDataAccess
        from neon_config import NeonConfig
        import psycopg2
        import psycopg2.extras
    except ImportError:
        print("Warning: Could not import dependencies, using placeholders")
        ReviewDataAccess = None
        NeonConfig = None
        psycopg2 = None

# cachetools 缓存
try:
    from cachetools import TTLCache
    CACHETOOLS_AVAILABLE = True
except ImportError:
    CACHETOOLS_AVAILABLE = False
    print("Warning: cachetools not available, caching disabled. Install with: pip install cachetools")


# ============================================================================
# 性能监控数据结构
# ============================================================================

@dataclass
class PerformanceMetrics:
    """性能指标数据类"""
    api_calls: int = 0
    api_time: float = 0.0
    api_errors: int = 0
    db_queries: int = 0
    db_time: float = 0.0
    db_errors: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    cache_time: float = 0.0
    total_time: float = 0.0
    memory_usage_mb: float = 0.0
    
    # 详细计时
    timing_breakdown: Dict[str, float] = None
    
    def __post_init__(self):
        if self.timing_breakdown is None:
            self.timing_breakdown = defaultdict(float)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        result = asdict(self)
        result['timing_breakdown'] = dict(result['timing_breakdown'])
        return result
    
    def get_cache_hit_rate(self) -> float:
        """计算缓存命中率"""
        total = self.cache_hits + self.cache_misses
        return (self.cache_hits / total * 100) if total > 0 else 0.0
    
    def get_api_success_rate(self) -> float:
        """计算API成功率"""
        total = self.api_calls + self.api_errors
        return (self.api_calls / total * 100) if total > 0 else 0.0


# ============================================================================
# Cachetools 缓存管理器（替代 Redis）
# ============================================================================

class CacheToolsManager:
    """基于 cachetools 的缓存管理器（Redis 替代方案）"""
    
    def __init__(self, ttl: int = 3600, max_size: int = 1000, enabled: bool = True):
        """
        初始化缓存
        
        Args:
            ttl: 缓存过期时间（秒）
            max_size: 最大缓存条目数
            enabled: 是否启用缓存
        """
        self.enabled = enabled and CACHETOOLS_AVAILABLE
        self.ttl = ttl
        self.max_size = max_size
        
        if self.enabled:
            try:
                # TTLCache: 自动过期的缓存，线程安全
                self.cache = TTLCache(maxsize=max_size, ttl=ttl)
                self.lock = threading.RLock()  # 可重入锁，支持嵌套调用
                print(f"[Cache] Memory cache enabled (TTL: {ttl}s, Max: {max_size} entries)")
            except Exception as e:
                print(f"[Cache] Initialization failed, cache disabled: {e}")
                self.enabled = False
                self.cache = None
                self.lock = None
        else:
            self.cache = None
            self.lock = None
            if not CACHETOOLS_AVAILABLE:
                print("[Cache] cachetools not installed. Install with: pip install cachetools")
    
    def _make_key(self, prefix: str, *args) -> str:
        """生成缓存键"""
        key_parts = [prefix] + [str(arg) for arg in args]
        return ':'.join(key_parts)
    
    def get(self, prefix: str, *args) -> Optional[Any]:
        """获取缓存"""
        if not self.enabled:
            return None
        
        try:
            key = self._make_key(prefix, *args)
            with self.lock:
                return self.cache.get(key)
        except Exception as e:
            print(f"[Cache] GET failed: {e}")
            return None
    
    def set(self, prefix: str, *args, value: Any) -> bool:
        """设置缓存"""
        if not self.enabled:
            return False
        
        try:
            key = self._make_key(prefix, *args)
            with self.lock:
                self.cache[key] = value
            return True
        except Exception as e:
            print(f"[Cache] SET failed: {e}")
            return False
    
    def delete(self, prefix: str, *args) -> bool:
        """删除缓存"""
        if not self.enabled:
            return False
        
        try:
            key = self._make_key(prefix, *args)
            with self.lock:
                if key in self.cache:
                    del self.cache[key]
                    return True
            return False
        except Exception as e:
            print(f"[Cache] DELETE failed: {e}")
            return False
    
    def clear_pattern(self, pattern: str) -> int:
        """清除匹配模式的缓存"""
        if not self.enabled:
            return 0
        
        try:
            with self.lock:
                keys_to_delete = [k for k in list(self.cache.keys()) if pattern in k]
                for key in keys_to_delete:
                    del self.cache[key]
                return len(keys_to_delete)
        except Exception as e:
            print(f"[Cache] CLEAR failed: {e}")
            return 0
    
    def clear_all(self) -> bool:
        """清空所有缓存"""
        if not self.enabled:
            return False
        
        try:
            with self.lock:
                self.cache.clear()
            return True
        except Exception as e:
            print(f"[Cache] CLEAR ALL failed: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        if not self.enabled:
            return {'enabled': False}
        
        try:
            with self.lock:
                current_size = len(self.cache)
                return {
                    'enabled': True,
                    'current_size': current_size,
                    'max_size': self.max_size,
                    'ttl': self.ttl,
                    'usage_percent': round(current_size / self.max_size * 100, 2) if self.max_size > 0 else 0
                }
        except Exception as e:
            print(f"[Cache] GET STATS failed: {e}")
            return {'enabled': True, 'error': str(e)}


# ============================================================================
# 增强的同步管理器
# ============================================================================

class EnhancedReviewSyncManager:
    """增强的审批系统同步管理器"""
    
    def __init__(
        self, 
        data_access: Optional[ReviewDataAccess] = None,
        max_concurrent: int = 10,
        enable_cache: bool = True,
        cache_ttl: int = 3600,
        cache_max_size: int = 1000,
        batch_size: int = 100
    ):
        """
        初始化增强同步管理器
        
        Args:
            data_access: 数据访问层实例
            max_concurrent: 最大并发数
            enable_cache: 是否启用内存缓存
            cache_ttl: 缓存过期时间（秒）
            cache_max_size: 缓存最大条目数（推荐：1000-10000）
            batch_size: 批量操作大小
        """
        self.da = data_access or ReviewDataAccess()
        self.max_concurrent = max_concurrent
        self.batch_size = batch_size
        
        # 账户同步功能已移除，现在使用独立的 account_sync.py
        
        # 初始化 cachetools 缓存（替代 Redis）
        self.cache = CacheToolsManager(
            ttl=cache_ttl,
            max_size=cache_max_size,
            enabled=enable_cache
        )
        
        # 性能指标
        self.metrics = PerformanceMetrics()
        
        # 同步统计
        self.sync_stats = {
            'workflows_synced': 0,
            'workflows_updated': 0,
            'workflows_skipped': 0,
            'templates_synced': 0,
            'templates_updated': 0,
            'templates_skipped': 0,
            'reviews_synced': 0,
            'reviews_updated': 0,
            'reviews_skipped': 0,
            'file_versions_synced': 0,
            'file_versions_total': 0,
            'progress_steps_synced': 0,
            'progress_steps_total': 0,
            'errors': []
        }
        
        # 断路器状态
        self.circuit_breaker = {
            'failures': 0,
            'last_failure_time': None,
            'state': 'closed',  # closed, open, half-open
            'threshold': 5,
            'timeout': 60
        }
    
    # ========================================================================
    # 性能监控装饰器
    # ========================================================================
    
    @staticmethod
    def track_performance(operation: str):
        """性能追踪装饰器（静态方法版本）"""
        def decorator(func):
            @wraps(func)
            async def async_wrapper(self, *args, **kwargs):
                start_time = time.time()
                try:
                    result = await func(self, *args, **kwargs)
                    elapsed = time.time() - start_time
                    self.metrics.timing_breakdown[operation] += elapsed
                    return result
                except Exception as e:
                    elapsed = time.time() - start_time
                    self.metrics.timing_breakdown[f"{operation}_error"] += elapsed
                    raise
            
            @wraps(func)
            def sync_wrapper(self, *args, **kwargs):
                start_time = time.time()
                try:
                    result = func(self, *args, **kwargs)
                    elapsed = time.time() - start_time
                    self.metrics.timing_breakdown[operation] += elapsed
                    return result
                except Exception as e:
                    elapsed = time.time() - start_time
                    self.metrics.timing_breakdown[f"{operation}_error"] += elapsed
                    raise
            
            return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
        return decorator
    
    # ========================================================================
    # 断路器模式
    # ========================================================================
    
    def check_circuit_breaker(self) -> bool:
        """检查断路器状态"""
        cb = self.circuit_breaker
        
        if cb['state'] == 'open':
            # 检查是否可以尝试恢复
            if cb['last_failure_time']:
                elapsed = time.time() - cb['last_failure_time']
                if elapsed > cb['timeout']:
                    cb['state'] = 'half-open'
                    print(f"[CIRCUIT] Circuit breaker entering half-open state, attempting recovery...")
                    return True
                else:
                    return False
            return False
        
        return True
    
    def record_success(self):
        """记录成功"""
        cb = self.circuit_breaker
        if cb['state'] == 'half-open':
            cb['state'] = 'closed'
            cb['failures'] = 0
            # Circuit breaker closed, service restored
    
    def record_failure(self):
        """记录失败"""
        cb = self.circuit_breaker
        cb['failures'] += 1
        cb['last_failure_time'] = time.time()
        
        if cb['failures'] >= cb['threshold']:
            cb['state'] = 'open'
            # Circuit breaker opened, API calls paused
    
    # ========================================================================
    # 异步API调用（使用aiohttp）
    # ========================================================================
    
    @track_performance('api_call')
    async def _async_api_call(
        self, 
        session: aiohttp.ClientSession,
        method: str,
        url: str,
        headers: Optional[Dict] = None,
        **kwargs
    ) -> Optional[Dict]:
        """
        异步API调用
        
        Args:
            session: aiohttp会话
            method: HTTP方法
            url: URL
            **kwargs: 其他参数
            
        Returns:
            API响应数据
        """
        # 检查断路器
        if not self.check_circuit_breaker():
            raise Exception("断路器已打开，API调用被阻止")
        
        # 检查缓存
        cache_key = f"{method}:{url}"
        cached = self.cache.get('api', cache_key)
        if cached:
            self.metrics.cache_hits += 1
            return cached
        
        self.metrics.cache_misses += 1
        
        # 执行API调用
        start_time = time.time()
        try:
            # 如果提供了 headers，使用提供的，否则需要从外部获取
            request_headers = headers or kwargs.pop('headers', {})
            
            # 确保 URL 是完整的
            if not url.startswith('http'):
                import config
                url = f"{config.AUTODESK_API_BASE}/construction/reviews/v1{url}"
            
            async with session.request(method, url, headers=request_headers, **kwargs) as response:
                response.raise_for_status()
                data = await response.json()
                
                elapsed = time.time() - start_time
                self.metrics.api_calls += 1
                self.metrics.api_time += elapsed
                
                # 缓存结果
                self.cache.set('api', cache_key, value=data)
                
                # 记录成功
                self.record_success()
                
                return data
                
        except Exception as e:
            elapsed = time.time() - start_time
            self.metrics.api_errors += 1
            self.metrics.api_time += elapsed
            
            # 记录失败
            self.record_failure()
            
            print(f"[WARNING] API call failed ({url}): {e}")
            raise
    
    # ========================================================================
    # 批量UPSERT优化
    # ========================================================================
    
    @track_performance('batch_upsert_workflows')
    def batch_upsert_workflows(self, workflows: List[Dict[str, Any]]) -> Tuple[int, int]:
        """
        批量UPSERT工作流（使用PostgreSQL的ON CONFLICT）
        
        Args:
            workflows: 工作流数据列表
            
        Returns:
            (插入数量, 更新数量)
        """
        if not workflows:
            return 0, 0
        
        start_time = time.time()
        
        try:
            # 准备批量数据
            batch_data = []
            for wf in workflows:
                wf_data = self._transform_acc_workflow_data(wf)
                batch_data.append(wf_data)
            
            # 执行批量UPSERT
            sql = """
                INSERT INTO workflows (
                    workflow_uuid, project_id, data_source, acc_workflow_id,
                    name, description, notes, status, additional_options,
                    approval_status_options, copy_files_options, attached_attributes,
                    update_attributes_options, steps, created_by,
                    created_at, updated_at, last_synced_at, sync_status
                )
                VALUES (
                    %(workflow_uuid)s, %(project_id)s, %(data_source)s, %(acc_workflow_id)s,
                    %(name)s, %(description)s, %(notes)s, %(status)s, %(additional_options)s,
                    %(approval_status_options)s, %(copy_files_options)s, %(attached_attributes)s,
                    %(update_attributes_options)s, %(steps)s, %(created_by)s,
                    %(created_at)s, %(updated_at)s, %(last_synced_at)s, %(sync_status)s
                )
                ON CONFLICT (acc_workflow_id) 
                DO UPDATE SET
                    name = EXCLUDED.name,
                    description = EXCLUDED.description,
                    notes = EXCLUDED.notes,
                    status = EXCLUDED.status,
                    additional_options = EXCLUDED.additional_options,
                    approval_status_options = EXCLUDED.approval_status_options,
                    copy_files_options = EXCLUDED.copy_files_options,
                    attached_attributes = EXCLUDED.attached_attributes,
                    update_attributes_options = EXCLUDED.update_attributes_options,
                    steps = EXCLUDED.steps,
                    updated_at = EXCLUDED.updated_at,
                    last_synced_at = EXCLUDED.last_synced_at,
                    sync_status = EXCLUDED.sync_status
                RETURNING id, (xmax = 0) AS inserted
            """
            
            # 执行批量操作
            with self.da.get_connection() as conn:
                with conn.cursor() as cur:
                    results = []
                    for data in batch_data:
                        cur.execute(sql, data)
                        results.append(cur.fetchone())
                    conn.commit()
            
            # 统计结果
            inserted = sum(1 for _, is_insert in results if is_insert)
            updated = len(results) - inserted
            
            elapsed = time.time() - start_time
            self.metrics.db_queries += 1
            self.metrics.db_time += elapsed
            
            print(f"  SUCCESS: Batch UPSERT workflows: {inserted} new, {updated} updated (duration: {elapsed:.2f}s)")
            
            return inserted, updated
            
        except Exception as e:
            elapsed = time.time() - start_time
            self.metrics.db_errors += 1
            self.metrics.db_time += elapsed
            error_msg = f"批量UPSERT工作流失败: {str(e)}"
            self.sync_stats['errors'].append(error_msg)
            print(f"✗ {error_msg}")
            raise
    
    @track_performance('batch_upsert_reviews')
    def batch_upsert_reviews(self, reviews: List[Dict[str, Any]]) -> Tuple[int, int]:
        """
        批量UPSERT评审
        
        Args:
            reviews: 评审数据列表
            
        Returns:
            (插入数量, 更新数量)
        """
        if not reviews:
            return 0, 0
        
        start_time = time.time()
        
        try:
            # 准备批量数据
            batch_data = []
            for review in reviews:
                review_data = self._transform_acc_review_data(review, project_id=getattr(self, '_current_project_id', None))
                batch_data.append(review_data)
            
            # 执行批量UPSERT
            sql = """
                INSERT INTO reviews (
                    review_uuid, project_id, data_source, acc_review_id, acc_sequence_id,
                    name, description, notes, status, current_step_id, current_step_due_date,
                    current_step_name, workflow_uuid, created_by, assigned_to, next_action_by,
                    archived, archived_by, archived_at, archived_reason,
                    created_at, updated_at, started_at, finished_at,
                    last_synced_at, sync_status
                )
                VALUES (
                    %(review_uuid)s, %(project_id)s, %(data_source)s, %(acc_review_id)s, %(acc_sequence_id)s,
                    %(name)s, %(description)s, %(notes)s, %(status)s, %(current_step_id)s, %(current_step_due_date)s,
                    %(current_step_name)s, %(workflow_uuid)s, %(created_by)s, %(assigned_to)s, %(next_action_by)s,
                    %(archived)s, %(archived_by)s, %(archived_at)s, %(archived_reason)s,
                    %(created_at)s, %(updated_at)s, %(started_at)s, %(finished_at)s,
                    %(last_synced_at)s, %(sync_status)s
                )
                ON CONFLICT (review_uuid)
                DO UPDATE SET
                    name = EXCLUDED.name,
                    description = EXCLUDED.description,
                    notes = EXCLUDED.notes,
                    status = EXCLUDED.status,
                    current_step_id = EXCLUDED.current_step_id,
                    current_step_due_date = EXCLUDED.current_step_due_date,
                    current_step_name = EXCLUDED.current_step_name,
                    assigned_to = EXCLUDED.assigned_to,
                    next_action_by = EXCLUDED.next_action_by,
                    archived = EXCLUDED.archived,
                    archived_by = EXCLUDED.archived_by,
                    archived_at = EXCLUDED.archived_at,
                    archived_reason = EXCLUDED.archived_reason,
                    updated_at = EXCLUDED.updated_at,
                    finished_at = EXCLUDED.finished_at,
                    last_synced_at = EXCLUDED.last_synced_at,
                    sync_status = EXCLUDED.sync_status
                RETURNING id, (xmax = 0) AS inserted
            """
            
            # 执行批量操作
            with self.da.get_connection() as conn:
                with conn.cursor() as cur:
                    results = []
                    for data in batch_data:
                        cur.execute(sql, data)
                        results.append(cur.fetchone())
                    conn.commit()
            
            # 统计结果
            inserted = sum(1 for _, is_insert in results if is_insert)
            updated = len(results) - inserted
            
            elapsed = time.time() - start_time
            self.metrics.db_queries += 1
            self.metrics.db_time += elapsed
            
            print(f"  SUCCESS: Batch UPSERT reviews: {inserted} new, {updated} updated (duration: {elapsed:.2f}s)")
            
            return inserted, updated
            
        except Exception as e:
            elapsed = time.time() - start_time
            self.metrics.db_errors += 1
            self.metrics.db_time += elapsed
            error_msg = f"Batch UPSERT reviews failed: {str(e)}"
            self.sync_stats['errors'].append(error_msg)
            print(f"✗ {error_msg}")
            raise
    
    # ========================================================================
    # 异步并行同步（使用asyncio）
    # ========================================================================
    
    async def fetch_all_workflows(
        self,
        session: aiohttp.ClientSession,
        project_id: str,
        show_progress: bool = True
    ) -> List[Dict[str, Any]]:
        """
        获取所有工作流（用于缓存）
        
        Args:
            session: aiohttp会话
            project_id: 项目ID
            show_progress: 是否显示进度
            
        Returns:
            所有工作流列表
        """
        if show_progress:
            print(f"\n[FETCH] Getting all workflows for caching...")
        
        try:
            # 获取工作流列表
            headers = getattr(self, '_temp_headers', {})
            result = await self._async_api_call(
                session,
                'GET',
                f'/projects/{project_id}/workflows',
                headers=headers,
                params={'limit': 50, 'offset': 0}
            )
            
            workflows = result.get('results', [])
            total_results = result.get('pagination', {}).get('totalResults', len(workflows))
            
            if show_progress:
                print(f"   SUCCESS: Retrieved {len(workflows)} workflows")
            
            # 如果有更多页面，继续获取
            if total_results > len(workflows):
                remaining_pages = (total_results - len(workflows) + 49) // 50
                if show_progress:
                    print(f"   需要额外获取 {remaining_pages} 页...")
                
                tasks = []
                for page in range(1, remaining_pages + 1):
                    offset = page * 50
                    task = self._async_api_call(
                        session,
                        'GET',
                        f'/projects/{project_id}/workflows',
                        headers=headers,
                        params={'limit': 50, 'offset': offset}
                    )
                    tasks.append(task)
                
                page_results = await asyncio.gather(*tasks, return_exceptions=True)
                
                for result in page_results:
                    if not isinstance(result, Exception):
                        workflows.extend(result.get('results', []))
            
            if show_progress:
                print(f"   [OK] Retrieved {len(workflows)} workflows total")
            
            return workflows
            
        except Exception as e:
            error_msg = f"获取工作流失败: {str(e)}"
            self.sync_stats['errors'].append(error_msg)
            print(f"   [ERROR] {error_msg}")
            return []
    
    async def async_sync_reviews_parallel(
        self,
        api_client,
        project_id: str,
        reviews: List[Dict[str, Any]],
        show_progress: bool = True
    ) -> Dict[str, Any]:
        """
        异步并行同步评审（使用asyncio）
        
        Args:
            api_client: API客户端
            project_id: 项目ID
            reviews: 评审列表
            show_progress: 是否显示进度
            
        Returns:
            同步统计信息
        """
        total = len(reviews)
        
        if show_progress:
            print(f"\n[ASYNC] Starting parallel async sync for {total} reviews...")
            print(f"   Max concurrent: {self.max_concurrent}")
            print("=" * 60)
        
        start_time = time.time()
        
        # 设置当前项目ID供其他方法使用
        self._current_project_id = project_id
        
        # 创建异步HTTP会话
        async with aiohttp.ClientSession() as session:
            # Step 1: Pre-fetch all workflows and build cache
            if show_progress:
                print(f"\n[OPTIMIZE] Pre-fetching workflow cache...")
            
            all_workflows = await self.fetch_all_workflows(session, project_id, show_progress)
            workflow_cache = {wf['id']: wf for wf in all_workflows}
            
            if show_progress:
                print(f"   [OK] Workflow cache built: {len(workflow_cache)} workflows")
                
                # 分析 review 的 workflow 分布
                workflow_usage = {}
                for review in reviews:
                    wf_id = review.get('workflowId')
                    if wf_id:
                        workflow_usage[wf_id] = workflow_usage.get(wf_id, 0) + 1
                
                print(f"   [STATS] Workflow usage analysis:")
                for wf_id, count in workflow_usage.items():
                    wf_name = workflow_cache.get(wf_id, {}).get('name', 'Unknown')
                    print(f"      - {wf_name}: {count} reviews")
                
                # 计算预期的缓存节省
                total_workflow_calls = sum(workflow_usage.values())
                unique_workflows = len(workflow_usage)
                saved_calls = total_workflow_calls - unique_workflows
                if saved_calls > 0:
                    print(f"   [OPTIMIZE] Expected to save {saved_calls} workflow API calls (savings: {saved_calls/total_workflow_calls*100:.1f}%)")
            
            # 创建信号量限制并发
            semaphore = asyncio.Semaphore(self.max_concurrent)
            
            # 创建所有任务（传入 workflow_cache）
            tasks = []
            for review in reviews:
                task = self._async_fetch_review_details(
                    session,
                    api_client,
                    project_id,
                    review,
                    semaphore,
                    workflow_cache  # Pass workflow cache
                )
                tasks.append(task)
            
            # 并行执行所有任务
            if show_progress:
                print(f"\n[PHASE 1/2] Async API data fetching...")
            
            review_details = await asyncio.gather(*tasks, return_exceptions=True)
            
            # 处理结果
            successful_reviews = []
            for idx, result in enumerate(review_details):
                if isinstance(result, Exception):
                    error_msg = f"获取评审详情失败: {str(result)}"
                    self.sync_stats['errors'].append(error_msg)
                    if show_progress:
                        print(f"   ✗ {error_msg}")
                else:
                    successful_reviews.append(result)
        
        api_time = time.time() - start_time
        self.metrics.api_time += api_time
        
        if show_progress:
            print(f"\nSUCCESS: API data fetching completed")
            print(f"   Total API calls: {self.metrics.api_calls} times")
            print(f"   Duration: {api_time:.2f}s")
            print(f"   Success: {len(successful_reviews)}/{total}")
        
        # Phase 2: Batch database writing
        if show_progress:
            print(f"\n[PHASE 2/2] Batch database writing...")
        
        db_start = time.time()
        
        # Batch UPSERT reviews
        inserted, updated = self.batch_upsert_reviews(successful_reviews)
        self.sync_stats['reviews_synced'] += inserted
        self.sync_stats['reviews_updated'] += updated
        
        # 🔧 修复：同步 file versions 和 progress steps
        total_file_versions = 0
        total_progress_steps = 0
        
        for review in successful_reviews:
            review_id = review.get('id')
            if not review_id:
                continue
                
            # 获取数据库中的 review ID
            db_review = self.da.get_review_by_acc_id(review_id)
            if not db_review:
                continue
                
            local_review_id = db_review['id']
            
            # 同步文件版本
            file_versions = review.get('fileVersions', [])
            if file_versions:
                self._sync_review_file_versions(local_review_id, file_versions)
                total_file_versions += len(file_versions)
                self.sync_stats['file_versions_synced'] += len(file_versions)
                
            # 同步进度步骤
            progress_steps = review.get('steps', [])
            if progress_steps:
                self._sync_review_progress(local_review_id, progress_steps)
                total_progress_steps += len(progress_steps)
                self.sync_stats['progress_steps_synced'] += len(progress_steps)
        
        self.sync_stats['file_versions_total'] = total_file_versions
        self.sync_stats['progress_steps_total'] = total_progress_steps
        
        if show_progress and (total_file_versions > 0 or total_progress_steps > 0):
            print(f"  SUCCESS: 同步文件版本: {total_file_versions} 个")
            print(f"  SUCCESS: 同步进度步骤: {total_progress_steps} 个")
        
        db_time = time.time() - db_start
        total_time = time.time() - start_time
        
        self.metrics.total_time = total_time
        
        if show_progress:
            print("\n" + "=" * 60)
            print(f"[STATS] Performance statistics:")
            print(f"   API调用阶段: {api_time:.2f}秒 ({api_time/total_time*100:.1f}%)")
            print(f"   数据库写入: {db_time:.2f}秒 ({db_time/total_time*100:.1f}%)")
            print(f"   总耗时: {total_time:.2f}秒")
            print(f"   平均每个评审: {total_time/total:.2f}秒")
        
        return self.sync_stats
    
    async def _async_fetch_review_details(
        self,
        session: aiohttp.ClientSession,
        api_client,
        project_id: str,
        review: Dict[str, Any],
        semaphore: asyncio.Semaphore,
        workflow_cache: Optional[Dict[str, Dict]] = None
    ) -> Dict[str, Any]:
        """
        异步获取评审详情
        
        Args:
            session: aiohttp会话
            api_client: API客户端
            project_id: 项目ID
            review: 评审基础信息
            semaphore: 并发控制信号量
            workflow_cache: 工作流缓存（可选）
            
        Returns:
            完整的评审数据
        """
        async with semaphore:
            review_id = review.get('id')
            
            # Optimization: Use workflow cache instead of API calls
            workflow_id = review.get('workflowId')
            workflow = None
            
            if workflow_cache and workflow_id and workflow_id in workflow_cache:
                # Cache hit: Get workflow from cache
                workflow = workflow_cache[workflow_id]
                self.metrics.cache_hits += 1
                
                # 只需要获取2个API端点（versions 和 progress）
                headers = getattr(self, '_temp_headers', {})
                tasks = [
                    self._async_api_call(
                        session,
                        'GET',
                        f'/projects/{project_id}/reviews/{review_id}/versions',
                        headers=headers
                    ),
                    self._async_api_call(
                        session,
                        'GET',
                        f'/projects/{project_id}/reviews/{review_id}/progress',
                        headers=headers
                    )
                ]
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # 合并结果
                versions = results[0] if not isinstance(results[0], Exception) else []
                progress = results[1] if not isinstance(results[1], Exception) else []
                
            else:
                # 🔄 缓存未命中，需要调用 workflow API
                if workflow_cache is not None:
                    self.metrics.cache_misses += 1
                
                # 并行获取3个API端点（包括 workflow）
                headers = getattr(self, '_temp_headers', {})
                tasks = [
                    self._async_api_call(
                        session,
                        'GET',
                        f'/projects/{project_id}/reviews/{review_id}/versions',
                        headers=headers
                    ),
                    self._async_api_call(
                        session,
                        'GET',
                        f'/projects/{project_id}/reviews/{review_id}/progress',
                        headers=headers
                    ),
                    self._async_api_call(
                        session,
                        'GET',
                        f'/projects/{project_id}/reviews/{review_id}/workflow',
                        headers=headers
                    )
                ]
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # 合并结果
                versions = results[0] if not isinstance(results[0], Exception) else []
                progress = results[1] if not isinstance(results[1], Exception) else []
                workflow = results[2] if not isinstance(results[2], Exception) else {}
            
            # 添加到评审数据
            review['fileVersions'] = versions.get('results', []) if isinstance(versions, dict) else []
            review['steps'] = progress.get('results', []) if isinstance(progress, dict) else []
            review['workflow'] = workflow or {}
            
            return review
    
    # ========================================================================
    # 数据转换方法（复用原有逻辑）
    # ========================================================================
    
    def _transform_acc_workflow_data(self, acc_data: Dict[str, Any]) -> Dict[str, Any]:
        """转换ACC工作流数据为本地格式"""
        return {
            'workflow_uuid': acc_data.get('id'),  # 使用 ACC 的 workflow ID 作为 UUID
            'project_id': acc_data.get('projectId'),
            'data_source': 'acc_sync',
            'acc_workflow_id': acc_data.get('id'),
            'name': acc_data.get('name', 'Unnamed Workflow'),
            'description': acc_data.get('description'),
            'notes': acc_data.get('notes'),
            'status': self._map_workflow_status(acc_data.get('status', 'active')),
            'additional_options': json.dumps(acc_data.get('additionalOptions', {})),
            'approval_status_options': json.dumps(acc_data.get('approvalStatusOptions', [])),
            'copy_files_options': json.dumps(acc_data.get('copyFilesOptions', {})),
            'attached_attributes': json.dumps(acc_data.get('attachedAttributes', [])),
            'update_attributes_options': json.dumps(acc_data.get('updateAttributesOptions', {})),
            'steps': json.dumps(acc_data.get('steps', [])),
            'created_by': json.dumps(acc_data.get('createdBy', {})),
            'created_at': self._parse_timestamp(acc_data.get('createdAt')),
            'updated_at': self._parse_timestamp(acc_data.get('updatedAt')),
            'last_synced_at': datetime.now(timezone.utc),
            'sync_status': 'synced'
        }
    
    def _transform_acc_review_data(self, acc_data: Dict[str, Any], project_id: Optional[str] = None) -> Dict[str, Any]:
        """
        转换ACC评审数据为本地格式
        
        注意：workflow_id 会由数据库触发器自动设置，无需手动查找
        """
        workflow_uuid = acc_data.get('workflowId')
        
        return {
            'review_uuid': acc_data.get('id'),  # 使用 ACC 的 review ID 作为 UUID
            'project_id': project_id or acc_data.get('projectId'),
            'data_source': 'acc_sync',
            'acc_review_id': acc_data.get('id'),
            'acc_sequence_id': acc_data.get('sequenceId'),
            'name': acc_data.get('name', 'Unnamed Review'),
            'description': acc_data.get('description'),
            'notes': acc_data.get('notes'),
            'status': self._map_review_status(acc_data.get('status', 'open')),
            'current_step_id': acc_data.get('currentStepId'),
            'current_step_due_date': self._parse_timestamp(acc_data.get('currentStepDueDate')),
            'current_step_name': acc_data.get('currentStepName'),
            # workflow_id 由数据库触发器自动设置，只需提供 workflow_uuid
            'workflow_uuid': workflow_uuid,
            'created_by': json.dumps(acc_data.get('createdBy', {})),
            'assigned_to': json.dumps(acc_data.get('assignedTo', [])),
            'next_action_by': json.dumps(acc_data.get('nextActionBy', {})),
            'archived': acc_data.get('archived', False),
            'archived_by': json.dumps(acc_data.get('archivedBy', {})),
            'archived_at': self._parse_timestamp(acc_data.get('archivedAt')),
            'archived_reason': acc_data.get('archivedReason'),
            'created_at': self._parse_timestamp(acc_data.get('createdAt')),
            'updated_at': self._parse_timestamp(acc_data.get('updatedAt')),
            'started_at': self._parse_timestamp(acc_data.get('startedAt')),
            'finished_at': self._parse_timestamp(acc_data.get('finishedAt')),
            'last_synced_at': datetime.now(timezone.utc),
            'sync_status': 'synced'
        }
    
    def _map_workflow_status(self, acc_status: str) -> str:
        """映射ACC工作流状态到本地状态"""
        status_map = {
            'active': 'ACTIVE',
            'inactive': 'INACTIVE',
            'draft': 'DRAFT',
            'archived': 'ARCHIVED'
        }
        return status_map.get(acc_status.lower(), 'ACTIVE')
    
    def _map_review_status(self, acc_status: str) -> str:
        """映射ACC评审状态到本地状态"""
        status_map = {
            'open': 'OPEN',
            'closed': 'CLOSED',
            'void': 'VOID',
            'failed': 'FAILED',
            'draft': 'DRAFT',
            'cancelled': 'CANCELLED'
        }
        return status_map.get(acc_status.lower(), 'OPEN')
    
    def _parse_timestamp(self, timestamp_str: Optional[str]) -> Optional[datetime]:
        """解析时间戳字符串"""
        if not timestamp_str:
            return None
        
        try:
            return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        except:
            try:
                return datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%f')
            except:
                return None
    
    # _get_workflow_id_by_uuid 方法已删除
    # workflow_id 现在由数据库触发器自动设置，无需手动查找
    
    # ========================================================================
    # 文件版本和进度同步（批量优化）
    # ========================================================================
    
    @track_performance('sync_review_file_versions')
    def _sync_review_file_versions(self, review_id: int, file_versions: List[Dict]) -> None:
        """
        同步评审的文件版本（批量优化版）
        
        注意：此方法只同步审批状态，不存储文件信息
        文件信息应该已经在 file_versions 表中（由 postgresql_sync_manager 同步）
        """
        if not file_versions:
            return
        
        db_start = time.time()
        batch_data = []
        
        for fv_data in file_versions:
            try:
                # 处理审批状态对象
                approve_status = fv_data.get('approveStatus', {})
                if isinstance(approve_status, dict):
                    approval_status_id = approve_status.get('id')
                    approval_status_value = approve_status.get('value', 'PENDING')
                    approval_label = approve_status.get('label')
                    approval_status = self._map_approval_status(approval_status_value)
                else:
                    # 兼容旧格式
                    approval_status = self._map_approval_status(fv_data.get('approvalStatus', 'pending'))
                    approval_status_id = None
                    approval_status_value = None
                    approval_label = fv_data.get('approvalLabel')
                
                # 🔑 关键改变：只存储 file_version_urn 和审批状态
                # 文件信息从 file_versions 表获取
                file_version_urn = fv_data.get('urn') or fv_data.get('versionUrn')
                
                if not file_version_urn:
                    print(f"  [WARNING] Missing file_version_urn, skipping file")
                    continue
                
                file_data = {
                    'review_id': review_id,
                    'file_version_urn': file_version_urn,  # 🔑 引用 file_versions.urn
                    
                    # 只存储审批相关信息
                    'approval_status': approval_status,
                    'approval_status_id': approval_status_id,
                    'approval_status_value': approval_status_value,
                    'approval_label': approval_label,
                    'approval_comments': fv_data.get('approvalComments'),
                    'review_content': fv_data.get('reviewContent', {}),
                    'custom_attributes': fv_data.get('customAttributes', []),
                    'copied_file_version_urn': fv_data.get('copiedFileVersionUrn')
                }
                
                batch_data.append(file_data)
            
            except Exception as e:
                error_msg = f"准备文件版本数据失败: {str(e)}"
                self.sync_stats['errors'].append(error_msg)
                print(f"✗ {error_msg}")
        
        # 批量插入
        if batch_data:
            try:
                inserted_count = self.da.batch_insert_review_files(batch_data)
                db_time = time.time() - db_start
                self.metrics.db_time += db_time
                self.metrics.db_queries += 1
                print(f"  SUCCESS: Batch insert {inserted_count} file versions (duration: {db_time:.2f}s)")
            except Exception as e:
                error_msg = f"批量插入文件版本失败: {str(e)}"
                self.sync_stats['errors'].append(error_msg)
                self.metrics.db_errors += 1
                print(f"✗ {error_msg}")
    
    @track_performance('sync_review_progress')
    def _sync_review_progress(self, review_id: int, steps: List[Dict]) -> None:
        """
        同步评审进度（批量优化版）
        
        重要概念说明：
        1. review_step_candidates: 从 workflow 模板创建，存储候选审批人配置（静态配置）
           - 只包含 workflow 定义的步骤（不包含"返回"产生的重复步骤）
           - 用于权限验证："谁可以审批这个步骤"
        
        2. review_progress: 记录实际执行历史和状态（动态记录）
           - 包含所有实际执行的步骤（包括"返回"产生的重复步骤）
           - 记录历史："谁在什么时候审批了，结果如何"
           - 数量可能大于 workflow 步骤数（因为"返回"功能）
        
        方案2實現：
        - 步驟1: 從 workflow template 創建完整的 review_step_candidates（所有步驟）
        - 步驟2: 同步 review_progress（只有已執行的步驟，自動關聯 template_step_id）
        """
        if not steps:
            return

        # 步驟 1: 獲取 workflow template 配置
        workflow_steps_config = self._get_workflow_steps_for_review(review_id)
        if not workflow_steps_config:
            print(f"  [WARNING] No workflow template found for review {review_id}, skipping sync")
            return

        # 步驟 2: 從 workflow template 創建完整的 step_candidates（所有步驟，包括未執行的）
        # ✅ 使用 template step_id，確保配置完整性
        try:
            self._create_candidates_from_template(review_id, workflow_steps_config)
        except Exception as e:
            error_msg = f"從模板創建候選人配置失敗: {str(e)}"
            self.sync_stats['errors'].append(error_msg)
            print(f"✗ {error_msg}")

        # 步驟 3: 同步 review_progress（只有已執行的步驟）
        # ✅ 自動關聯到 template_step_id（通過 step_order 匹配）
        try:
            self._sync_progress_with_template_mapping(review_id, steps, workflow_steps_config)
        except Exception as e:
            error_msg = f"同步進度並關聯模板失敗: {str(e)}"
            self.sync_stats['errors'].append(error_msg)
            print(f"✗ {error_msg}")
    
    def _map_approval_status(self, acc_status: str) -> str:
        """映射审批状态"""
        status_map = {
            'pending': 'PENDING',
            'approved': 'APPROVED',
            'rejected': 'REJECTED',
            'in_review': 'IN_REVIEW'
        }
        return status_map.get(acc_status.lower(), 'PENDING')
    
    def _map_step_type(self, acc_type: str) -> str:
        """映射步骤类型"""
        type_map = {
            'reviewer': 'REVIEWER',
            'approver': 'APPROVER',
            'initiator': 'INITIATOR',
            'final': 'FINAL'
        }
        return type_map.get(acc_type.lower(), 'REVIEWER')
    
    def _map_step_status(self, acc_status: str) -> str:
        """映射步骤状态"""
        status_map = {
            'pending': 'PENDING',
            'claimed': 'CLAIMED',
            'in_progress': 'OPEN',
            'submitted': 'SUBMITTED',
            'approved': 'APPROVED',
            'rejected': 'REJECTED',
            'skipped': 'SKIPPED'
        }
        return status_map.get(acc_status.lower(), 'PENDING')
    
    def _get_workflow_steps_for_review(self, review_id: int) -> List[Dict]:
        """获取评审关联的工作流步骤配置"""
        try:
            with self.da.get_connection() as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    # 尝试通过 workflow_id 关联
                    cur.execute("""
                        SELECT w.steps, w.workflow_uuid, w.name as workflow_name
                        FROM reviews r
                        JOIN workflows w ON r.workflow_id = w.id
                        WHERE r.id = %s AND r.workflow_id IS NOT NULL
                    """, (review_id,))
                    
                    result = cur.fetchone()
                    if result and result['steps']:
                        steps = json.loads(result['steps']) if isinstance(result['steps'], str) else result['steps']
                        if isinstance(steps, list) and len(steps) > 0:
                            print(f"  [WORKFLOW] Found workflow via workflow_id: {result['workflow_name']} ({len(steps)} steps)")
                            return steps
                    
                    # 如果通过 workflow_id 没找到，尝试通过 workflow_uuid 关联
                    cur.execute("""
                        SELECT w.steps, w.workflow_uuid, w.name as workflow_name, r.workflow_uuid as review_workflow_uuid
                        FROM reviews r
                        JOIN workflows w ON r.workflow_uuid = w.workflow_uuid
                        WHERE r.id = %s AND r.workflow_uuid IS NOT NULL
                    """, (review_id,))
                    
                    result = cur.fetchone()
                    if result and result['steps']:
                        steps = json.loads(result['steps']) if isinstance(result['steps'], str) else result['steps']
                        if isinstance(steps, list) and len(steps) > 0:
                            print(f"  [WORKFLOW] Found workflow via workflow_uuid: {result['workflow_name']} ({len(steps)} steps)")
                            return steps
                    
                    # 如果都没找到，记录调试信息
                    cur.execute("""
                        SELECT workflow_id, workflow_uuid, name
                        FROM reviews 
                        WHERE id = %s
                    """, (review_id,))
                    
                    review_info = cur.fetchone()
                    if review_info:
                        print(f"  [WARNING] No workflow found for review {review_id}")
                        print(f"            Review workflow_id: {review_info['workflow_id']}")
                        print(f"            Review workflow_uuid: {review_info['workflow_uuid']}")
                    
                    return []
        except Exception as e:
            print(f"[WARNING] Failed to get workflow steps config: {e}")
            return []
    
    def _get_candidates_from_workflow_config(self, workflow_steps: List[Dict], step_id: str) -> Dict:
        """从工作流配置中获取指定步骤的候选人信息"""
        try:
            for step in workflow_steps:
                if step.get('id') == step_id:
                    candidates = step.get('candidates', {})
                    if candidates and isinstance(candidates, dict):
                        # 确保候选人数据格式正确
                        formatted_candidates = {
                            'users': candidates.get('users', []),
                            'roles': candidates.get('roles', []),
                            'companies': candidates.get('companies', [])
                        }
                        # 只返回非空的候选人信息
                        if any(formatted_candidates.values()):
                            return formatted_candidates
            return {}
        except Exception as e:
            print(f"[WARNING] Failed to parse workflow candidates config: {e}")
            return {}
    
    # ========================================================================
    # 文件审批历史同步（异步版本）
    # ========================================================================
    
    async def async_sync_file_approval_history(
        self,
        session: aiohttp.ClientSession,
        api_client,
        project_id: str,
        file_version_urn: str,
        review_data: Optional[Dict] = None
    ) -> int:
        """
        异步同步单个文件的审批历史
        
        Args:
            session: aiohttp会话
            api_client: API客户端
            project_id: 项目ID
            file_version_urn: 文件版本URN
            review_data: 评审数据（可选）
            
        Returns:
            同步的记录数
        """
        try:
            # URL编码文件URN
            import urllib.parse
            encoded_urn = urllib.parse.quote(file_version_urn, safe='')
            
            # 调用API获取审批状态
            url = f'/projects/{project_id}/versions/{encoded_urn}/approval-statuses'
            result = await self._async_api_call(session, 'GET', url)
            
            if not result or 'results' not in result:
                return 0
            
            approval_records = []
            for item in result.get('results', []):
                approval_status = item.get('approvalStatus', {})
                review = item.get('review', {})
                
                record = {
                    'file_version_urn': file_version_urn,
                    'file_item_urn': review_data.get('itemUrn') if review_data else None,
                    'file_name': review_data.get('name') if review_data else None,
                    'review_acc_id': review.get('id'),
                    'review_sequence_id': review.get('sequenceId'),
                    'review_status': review.get('status'),
                    'review_name': review_data.get('name') if review_data else None,
                    'approval_status_id': approval_status.get('id'),
                    'approval_status_label': approval_status.get('label'),
                    'approval_status_value': approval_status.get('value'),
                    'approval_status_type': approval_status.get('type'),
                    'is_current': review.get('status') == 'OPEN',
                    'is_latest_in_review': True
                }
                
                approval_records.append(record)
            
            # 批量插入
            if approval_records:
                inserted_count = self.da.batch_insert_file_approval_history(approval_records)
                return inserted_count
            
            return 0
            
        except Exception as e:
            error_msg = f"同步文件审批历史失败 (URN: {file_version_urn}): {str(e)}"
            self.sync_stats['errors'].append(error_msg)
            print(f"[WARNING] {error_msg}")
            return 0
    
    # ========================================================================
    # 智能分页获取（异步版本）
    # ========================================================================
    
    async def async_fetch_all_reviews_with_pagination(
        self,
        session: aiohttp.ClientSession,
        api_client,
        project_id: str,
        limit_per_page: int = 50,
        show_progress: bool = True
    ) -> List[Dict]:
        """
        异步智能分页获取所有评审
        
        Args:
            session: aiohttp会话
            api_client: API客户端
            project_id: 项目ID
            limit_per_page: 每页数量
            show_progress: 是否显示进度
            
        Returns:
            所有评审列表
        """
        if show_progress:
            print(f"\n[FETCH] Async smart pagination for review list...")
        
        # 第一次调用获取总数
        first_page = await self._async_api_call(
            session,
            'GET',
            f'/projects/{project_id}/reviews',
            params={'limit': limit_per_page, 'offset': 0}
        )
        
        total_results = first_page.get('pagination', {}).get('totalResults', 0)
        reviews = first_page.get('results', [])
        
        if show_progress:
            print(f"   总评审数: {total_results}")
            print(f"   第一页: {len(reviews)} 个")
        
        # 计算需要的页数
        pages_needed = (total_results - limit_per_page + limit_per_page - 1) // limit_per_page
        
        if pages_needed > 0:
            if show_progress:
                print(f"   需要额外获取 {pages_needed} 页...")
            
            # 并行获取剩余页面
            semaphore = asyncio.Semaphore(min(5, pages_needed))
            tasks = []
            
            for page in range(1, pages_needed + 1):
                offset = page * limit_per_page
                task = self._async_fetch_reviews_page(
                    session,
                    api_client,
                    project_id,
                    limit_per_page,
                    offset,
                    semaphore
                )
                tasks.append(task)
            
            page_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for idx, result in enumerate(page_results, 1):
                if isinstance(result, Exception):
                    error_msg = f"获取分页数据失败: {result}"
                    self.sync_stats['errors'].append(error_msg)
                    print(f"[WARNING] {error_msg}")
                else:
                    reviews.extend(result)
                    if show_progress and idx % 5 == 0:
                        print(f"   Retrieved {idx}/{pages_needed} pages")
        
        if show_progress:
            print(f"SUCCESS: Retrieved {len(reviews)} reviews total\n")
        
        return reviews
    
    async def _async_fetch_reviews_page(
        self,
        session: aiohttp.ClientSession,
        api_client,
        project_id: str,
        limit: int,
        offset: int,
        semaphore: asyncio.Semaphore
    ) -> List[Dict]:
        """异步获取单页评审数据"""
        async with semaphore:
            try:
                result = await self._async_api_call(
                    session,
                    'GET',
                    f'/projects/{project_id}/reviews',
                    params={'limit': limit, 'offset': offset}
                )
                return result.get('results', [])
            except Exception as e:
                print(f"[WARNING] Failed to fetch review page (offset: {offset}): {e}")
                return []
    
    # ========================================================================
    # 性能报告
    # ========================================================================
    
    def get_performance_report(self) -> Dict[str, Any]:
        """获取详细的性能报告"""
        metrics_dict = self.metrics.to_dict()
        
        return {
            'summary': {
                'total_time': self.metrics.total_time,
                'api_calls': self.metrics.api_calls,
                'api_success_rate': self.metrics.get_api_success_rate(),
                'cache_hit_rate': self.metrics.get_cache_hit_rate(),
                'db_queries': self.metrics.db_queries,
                'memory_usage_mb': self.metrics.memory_usage_mb
            },
            'detailed_metrics': metrics_dict,
            'sync_stats': self.sync_stats,
            'circuit_breaker': self.circuit_breaker,
            'bottlenecks': self._identify_bottlenecks()
        }
    
    def _identify_bottlenecks(self) -> List[Dict[str, Any]]:
        """识别性能瓶颈"""
        bottlenecks = []
        
        # API时间占比过高
        if self.metrics.total_time > 0:
            api_ratio = self.metrics.api_time / self.metrics.total_time
            if api_ratio > 0.7:
                bottlenecks.append({
                    'type': 'api',
                    'severity': 'high',
                    'message': f'API calls consume {api_ratio*100:.1f}% of total time',
                    'suggestion': 'Consider increasing concurrency or using more caching'
                })
        
        # 缓存命中率过低
        cache_hit_rate = self.metrics.get_cache_hit_rate()
        if cache_hit_rate < 30 and self.cache.enabled:
            bottlenecks.append({
                'type': 'cache',
                'severity': 'medium',
                'message': f'Cache hit rate is only {cache_hit_rate:.1f}%',
                'suggestion': 'Consider increasing cache TTL or warming up cache'
            })
        
        # 数据库时间占比过高
        if self.metrics.total_time > 0:
            db_ratio = self.metrics.db_time / self.metrics.total_time
            if db_ratio > 0.5:
                bottlenecks.append({
                    'type': 'database',
                    'severity': 'high',
                    'message': f'Database operations consume {db_ratio*100:.1f}% of total time',
                    'suggestion': 'Consider increasing batch size or optimizing SQL'
                })
        
        return bottlenecks
    
    def print_performance_report(self):
        """打印性能报告"""
        report = self.get_performance_report()
        
        print("\n" + "=" * 80)
        print("[PERFORMANCE ANALYSIS REPORT]")
        print("=" * 80)
        
        summary = report['summary']
        print(f"\nSummary:")
        print(f"  Total Time: {summary['total_time']:.2f}s")
        print(f"  API Calls: {summary['api_calls']} times (Success Rate: {summary['api_success_rate']:.1f}%)")
        print(f"  Cache Hit Rate: {summary['cache_hit_rate']:.1f}%")
        print(f"  DB Queries: {summary['db_queries']} times")
        print(f"  Memory Usage: {summary['memory_usage_mb']:.2f}MB")
        
        # 时间分解
        print(f"\nTiming Breakdown:")
        timing = self.metrics.timing_breakdown
        for operation, duration in sorted(timing.items(), key=lambda x: x[1], reverse=True)[:10]:
            percentage = (duration / summary['total_time'] * 100) if summary['total_time'] > 0 else 0
            print(f"  {operation:.<40} {duration:>8.2f}s ({percentage:>5.1f}%)")
        
        # 瓶颈分析
        bottlenecks = report['bottlenecks']
        if bottlenecks:
            print(f"\n[WARNING] Performance Bottlenecks:")
            for bn in bottlenecks:
                severity_label = {'high': '[HIGH]', 'medium': '[MEDIUM]', 'low': '[LOW]'}
                print(f"  {severity_label.get(bn['severity'], '[INFO]')} [{bn['type'].upper()}] {bn['message']}")
                print(f"     [TIP] {bn['suggestion']}")
        else:
            print(f"\n[OK] No significant bottlenecks detected")
        
        print("\n" + "=" * 80)
    
    # ========================================================================
    # 工作流模板同步功能（整合自 template_sync_api.py）
    # ========================================================================
    
    async def sync_workflow_templates_enhanced(
        self,
        session: aiohttp.ClientSession,
        project_id: str,
        access_token: str,
        fetch_detailed_data: bool = True,
        show_progress: bool = True
    ) -> Dict[str, Any]:
        """
        增强的工作流模板同步 - 支持详细数据获取
        
        Args:
            session: aiohttp会话
            project_id: 项目ID
            access_token: 访问令牌
            fetch_detailed_data: 是否获取详细数据（调用单个workflow API）
            show_progress: 是否显示进度
            
        Returns:
            同步结果统计
        """
        if show_progress:
            print(f"\nTARGET: 开始同步工作流模板: {project_id}")
            print(f"   详细数据获取: {'启用' if fetch_detailed_data else '禁用'}")
        
        start_time = time.time()
        
        # 设置临时headers
        self._temp_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            # 清理项目ID前缀
            clean_project_id = project_id.replace('b.', '') if project_id.startswith('b.') else project_id
            
            # 第一步：获取所有工作流（作为模板）
            all_workflows = await self._fetch_all_workflows_for_templates(
                session, clean_project_id, show_progress
            )
            
            if not all_workflows:
                return {
                    'project_id': project_id,
                    'total_templates_fetched': 0,
                    'templates_inserted': 0,
                    'templates_updated': 0,
                    'templates_skipped': 0,
                    'errors': [],
                    'sync_time': datetime.now(timezone.utc).isoformat()
                }
            
            # 第二步：如果启用详细数据获取，并行获取每个工作流的详细信息
            if fetch_detailed_data:
                detailed_workflows = await self._fetch_workflows_details_parallel_for_templates(
                    session, clean_project_id, all_workflows, show_progress
                )
            else:
                detailed_workflows = all_workflows
            
            # 第三步：分析工作流并分类为模板
            template_analysis = self._analyze_workflows_for_templates(detailed_workflows, show_progress)
            
            # 第四步：批量同步到数据库
            sync_stats = await self._batch_upsert_workflow_templates(
                project_id, template_analysis['suitable_templates'], show_progress
            )
            
            elapsed_time = time.time() - start_time
            
            result = {
                'project_id': project_id,
                'total_workflows_fetched': len(all_workflows),
                'detailed_workflows_fetched': len(detailed_workflows) if fetch_detailed_data else 0,
                'suitable_templates_found': len(template_analysis['suitable_templates']),
                'templates_inserted': sync_stats['inserted'],
                'templates_updated': sync_stats['updated'],
                'templates_skipped': sync_stats['skipped'],
                'template_analysis': template_analysis['summary'],
                'errors': sync_stats['errors'],
                'elapsed_time': f"{elapsed_time:.2f}秒",
                'sync_time': datetime.now(timezone.utc).isoformat()
            }
            
            if show_progress:
                print(f"\n✅ 模板同步完成，耗时: {elapsed_time:.2f}秒")
                print(f"   发现 {len(template_analysis['suitable_templates'])} 个适合的模板")
                print(f"   新增: {sync_stats['inserted']}, 更新: {sync_stats['updated']}")
            
            return result
            
        except Exception as e:
            error_msg = f"模板同步失败: {str(e)}"
            self.sync_stats['errors'].append(error_msg)
            if show_progress:
                print(f"❌ {error_msg}")
            raise
        
        finally:
            # 清理临时headers
            if hasattr(self, '_temp_headers'):
                delattr(self, '_temp_headers')
    
    async def _fetch_all_workflows_for_templates(
        self,
        session: aiohttp.ClientSession,
        project_id: str,
        show_progress: bool = True
    ) -> List[Dict[str, Any]]:
        """
        获取所有工作流用于模板分析
        """
        if show_progress:
            print(f"INFO: 获取工作流列表...")
        
        all_workflows = []
        offset = 0
        limit = 50
        
        while True:
            try:
                result = await self._async_api_call(
                    session,
                    'GET',
                    f'/projects/{project_id}/workflows',
                    headers=self._temp_headers,
                    params={
                        'limit': limit,
                        'offset': offset,
                        'sort': 'name'
                    }
                )
                
                workflows = result.get('results', [])
                all_workflows.extend(workflows)
                
                # 检查是否还有更多数据
                pagination = result.get('pagination', {})
                total_results = pagination.get('totalResults', len(workflows))
                
                if show_progress:
                    print(f"   获取到 {len(workflows)} 个工作流，总计 {len(all_workflows)}/{total_results}")
                
                if offset + len(workflows) >= total_results:
                    break
                
                offset += limit
                
            except Exception as e:
                error_msg = f"获取工作流列表失败 (offset: {offset}): {str(e)}"
                self.sync_stats['errors'].append(error_msg)
                print(f"[WARNING] {error_msg}")
                break
        
        if show_progress:
            print(f"✅ 共获取 {len(all_workflows)} 个工作流")
        
        return all_workflows
    
    async def _fetch_workflows_details_parallel_for_templates(
        self,
        session: aiohttp.ClientSession,
        project_id: str,
        workflows: List[Dict],
        show_progress: bool = True
    ) -> List[Dict]:
        """
        并行获取工作流详细信息用于模板分析
        """
        if show_progress:
            print(f"🔍 并行获取 {len(workflows)} 个工作流的详细信息...")
        
        # 创建信号量限制并发
        semaphore = asyncio.Semaphore(min(self.max_concurrent, 10))
        
        # 创建所有任务
        tasks = []
        for workflow in workflows:
            workflow_id = workflow.get('id')
            if workflow_id:
                task = self._fetch_single_workflow_detail_for_template(
                    session, project_id, workflow_id, workflow, semaphore
                )
                tasks.append(task)
        
        # 并行执行所有任务
        detailed_workflows = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 过滤成功的结果
        successful_workflows = []
        for result in detailed_workflows:
            if isinstance(result, Exception):
                error_msg = f"获取工作流详情失败: {str(result)}"
                self.sync_stats['errors'].append(error_msg)
                if show_progress:
                    print(f"   ⚠ {error_msg}")
            else:
                successful_workflows.append(result)
        
        if show_progress:
            print(f"✅ 成功获取 {len(successful_workflows)}/{len(workflows)} 个详细工作流")
        
        return successful_workflows
    
    async def _fetch_single_workflow_detail_for_template(
        self,
        session: aiohttp.ClientSession,
        project_id: str,
        workflow_id: str,
        base_workflow: Dict,
        semaphore: asyncio.Semaphore
    ) -> Dict:
        """
        获取单个工作流的详细信息
        """
        async with semaphore:
            try:
                # 调用详细API
                detailed_data = await self._async_api_call(
                    session,
                    'GET',
                    f'/projects/{project_id}/workflows/{workflow_id}',
                    headers=self._temp_headers
                )
                
                # 合并基础数据和详细数据
                if detailed_data:
                    # 使用详细数据，但保留一些基础字段
                    detailed_data['projectId'] = project_id
                    return detailed_data
                else:
                    return base_workflow
                    
            except Exception as e:
                # 如果详细API失败，返回基础数据
                print(f"⚠ 获取工作流详情失败 {workflow_id}: {e}")
                return base_workflow
    
    def _analyze_workflows_for_templates(
        self,
        workflows: List[Dict],
        show_progress: bool = True
    ) -> Dict[str, Any]:
        """
        分析工作流并识别适合作为模板的工作流
        """
        if show_progress:
            print(f"🔍 分析 {len(workflows)} 个工作流...")
        
        suitable_templates = []
        analysis_summary = {
            'total_analyzed': len(workflows),
            'suitable_for_template': 0,
            'has_group_review': 0,
            'template_types': {},
            'complexity_distribution': {'simple': 0, 'moderate': 0, 'complex': 0}
        }
        
        for workflow in workflows:
            analysis = self._analyze_single_workflow_for_template(workflow)
            
            # 判断是否适合作为模板
            if analysis['is_template_worthy']:
                # 添加分析结果到工作流数据
                workflow['template_analysis'] = analysis
                suitable_templates.append(workflow)
                analysis_summary['suitable_for_template'] += 1
                
                # 统计模板类型
                template_type = analysis['template_type']
                analysis_summary['template_types'][template_type] = \
                    analysis_summary['template_types'].get(template_type, 0) + 1
                
                # 统计复杂度
                complexity = analysis['complexity_level']
                analysis_summary['complexity_distribution'][complexity] += 1
                
                if analysis['has_group_review']:
                    analysis_summary['has_group_review'] += 1
        
        if show_progress:
            print(f"   适合作为模板: {analysis_summary['suitable_for_template']} 个")
            print(f"   包含组审核: {analysis_summary['has_group_review']} 个")
            if analysis_summary['template_types']:
                print(f"   模板类型分布: {analysis_summary['template_types']}")
        
        return {
            'suitable_templates': suitable_templates,
            'summary': analysis_summary
        }
    
    def _analyze_single_workflow_for_template(self, workflow: Dict) -> Dict:
        """
        分析单个工作流的模板特征
        """
        steps = workflow.get('steps', [])
        
        analysis = {
            'steps_count': len(steps),
            'has_group_review': False,
            'has_specific_users': False,
            'has_specific_companies': False,
            'has_role_assignments': False,
            'complexity_score': 0,
            'is_template_worthy': False,
            'template_type': 'custom',
            'complexity_level': 'simple',
            'base_template_match': None
        }
        
        # 分析步骤特征
        for step in steps:
            # 检查组审核
            group_review = step.get('groupReview', {})
            if group_review.get('enabled', False):
                analysis['has_group_review'] = True
                analysis['complexity_score'] += 2
            
            # 检查候选人配置
            candidates = step.get('candidates', {})
            
            if candidates.get('users'):
                analysis['has_specific_users'] = True
                analysis['complexity_score'] += 3  # 具体用户降低模板价值
            
            if candidates.get('companies'):
                analysis['has_specific_companies'] = True
                analysis['complexity_score'] += 2
            
            if candidates.get('roles'):
                analysis['has_role_assignments'] = True
                analysis['complexity_score'] += 1  # 角色分配增加模板价值
        
        # 判断是否适合作为模板
        # 优先考虑没有具体用户分配的工作流
        analysis['is_template_worthy'] = (
            not analysis['has_specific_users'] and  # 没有具体用户
            analysis['steps_count'] > 0 and         # 有步骤
            analysis['complexity_score'] <= 5       # 复杂度不太高
        )
        
        # 确定模板类型
        analysis['template_type'] = self._determine_enhanced_template_type(analysis)
        
        # 确定复杂度级别
        if analysis['complexity_score'] <= 2:
            analysis['complexity_level'] = 'simple'
        elif analysis['complexity_score'] <= 4:
            analysis['complexity_level'] = 'moderate'
        else:
            analysis['complexity_level'] = 'complex'
        
        # 尝试匹配基础模板
        analysis['base_template_match'] = self._match_base_template(analysis)
        
        return analysis
    
    def _determine_enhanced_template_type(self, analysis: Dict) -> str:
        """
        增强的模板类型确定
        """
        steps_count = analysis['steps_count']
        has_group = analysis['has_group_review']
        
        if has_group:
            if steps_count == 2:
                return 'two_step_group'
            elif steps_count == 3:
                return 'three_step_group'
            elif steps_count == 4:
                return 'four_step_group'
            elif steps_count == 5:
                return 'five_step_group'
            else:
                return 'custom_group'
        else:
            if steps_count == 1:
                return 'one_step'
            elif steps_count == 2:
                return 'two_step'
            elif steps_count == 3:
                return 'three_step'
            elif steps_count == 4:
                return 'four_step'
            elif steps_count == 5:
                return 'five_step'
            else:
                return 'custom'
    
    def _match_base_template(self, analysis: Dict) -> Optional[str]:
        """
        匹配基础模板
        """
        steps_count = analysis['steps_count']
        has_group = analysis['has_group_review']
        
        # 基础模板匹配规则
        if has_group:
            template_map = {
                2: 'two_step_group',
                3: 'three_step_group',
                4: 'four_step_group'
            }
        else:
            template_map = {
                1: 'one_step',
                2: 'two_step',
                3: 'three_step',
                4: 'four_step',
                5: 'five_step'
            }
        
        return template_map.get(steps_count)
    
    async def _batch_upsert_workflow_templates(
        self,
        project_id: str,
        workflows: List[Dict],
        show_progress: bool = True
    ) -> Dict[str, Any]:
        """
        批量UPSERT工作流模板到workflow_templates表
        """
        stats = {
            'inserted': 0,
            'updated': 0,
            'skipped': 0,
            'errors': []
        }
        
        if not workflows:
            return stats
        
        if show_progress:
            print(f"💾 批量同步 {len(workflows)} 个模板到数据库...")
        
        start_time = time.time()
        
        try:
            # 准备批量数据
            batch_data = []
            for workflow in workflows:
                template_data = self._transform_workflow_to_template(project_id, workflow)
                batch_data.append(template_data)
            
            # 执行批量UPSERT
            upsert_sql = """
                INSERT INTO workflow_templates (
                    template_uuid, name, description, category, industry,
                    acc_template_id, data_source, template_type, steps_count,
                    steps_config, template_config, default_settings,
                    additional_options, approval_status_options, copy_files_options,
                    attached_attributes, update_attributes_options,
                    created_by, is_active, is_public, is_template,
                    base_template_key, template_characteristics,
                    last_synced_at, sync_status, created_at, updated_at
                ) VALUES (
                    %(template_uuid)s, %(name)s, %(description)s, %(category)s, %(industry)s,
                    %(acc_template_id)s, %(data_source)s, %(template_type)s, %(steps_count)s,
                    %(steps_config)s, %(template_config)s, %(default_settings)s,
                    %(additional_options)s, %(approval_status_options)s, %(copy_files_options)s,
                    %(attached_attributes)s, %(update_attributes_options)s,
                    %(created_by)s, %(is_active)s, %(is_public)s, %(is_template)s,
                    %(base_template_key)s, %(template_characteristics)s,
                    %(last_synced_at)s, %(sync_status)s, %(created_at)s, %(updated_at)s
                )
                ON CONFLICT (acc_template_id)
                DO UPDATE SET
                    name = EXCLUDED.name,
                    description = EXCLUDED.description,
                    steps_count = EXCLUDED.steps_count,
                    steps_config = EXCLUDED.steps_config,
                    template_config = EXCLUDED.template_config,
                    additional_options = EXCLUDED.additional_options,
                    approval_status_options = EXCLUDED.approval_status_options,
                    copy_files_options = EXCLUDED.copy_files_options,
                    attached_attributes = EXCLUDED.attached_attributes,
                    update_attributes_options = EXCLUDED.update_attributes_options,
                    is_active = EXCLUDED.is_active,
                    base_template_key = EXCLUDED.base_template_key,
                    template_characteristics = EXCLUDED.template_characteristics,
                    last_synced_at = EXCLUDED.last_synced_at,
                    sync_status = EXCLUDED.sync_status,
                    updated_at = EXCLUDED.updated_at
                RETURNING id, (xmax = 0) AS inserted
            """
            
            # 执行批量操作
            with self.da.get_connection() as conn:
                with conn.cursor() as cur:
                    results = []
                    for data in batch_data:
                        try:
                            cur.execute(upsert_sql, data)
                            result = cur.fetchone()
                            if result:
                                results.append(result)
                        except Exception as e:
                            error_msg = f"处理模板失败 {data.get('name', 'unknown')}: {str(e)}"
                            stats['errors'].append(error_msg)
                            if show_progress:
                                print(f"   ⚠ {error_msg}")
                    
                    conn.commit()
            
            # 统计结果
            inserted = sum(1 for _, is_insert in results if is_insert)
            updated = len(results) - inserted
            
            stats['inserted'] = inserted
            stats['updated'] = updated
            
            elapsed = time.time() - start_time
            self.metrics.db_queries += 1
            self.metrics.db_time += elapsed
            
            if show_progress:
                print(f"✅ 批量UPSERT模板完成: {inserted}个新建, {updated}个更新 (耗时: {elapsed:.2f}秒)")
            
            return stats
            
        except Exception as e:
            error_msg = f"批量同步模板失败: {str(e)}"
            stats['errors'].append(error_msg)
            self.sync_stats['errors'].append(error_msg)
            if show_progress:
                print(f"❌ {error_msg}")
            raise
    
    def _transform_workflow_to_template(self, project_id: str, workflow: Dict) -> Dict:
        """
        转换ACC工作流数据为模板格式
        """
        now = datetime.now(timezone.utc)
        
        # 获取分析结果
        analysis = workflow.get('template_analysis', {})
        
        # 解析步骤配置
        steps = workflow.get('steps', [])
        steps_count = len(steps)
        
        # 转换步骤配置
        steps_config = self._transform_steps_config_for_template(steps)
        
        # 解析时间戳
        created_at = self._parse_timestamp(workflow.get('createdAt'))
        updated_at = self._parse_timestamp(workflow.get('updatedAt'))
        
        return {
            'template_uuid': workflow.get('id'),  # 使用ACC workflow ID作为UUID
            'name': workflow.get('name', 'Unnamed Template'),
            'description': workflow.get('description'),
            'category': 'acc_synced',
            'industry': 'construction',
            'acc_template_id': workflow.get('id'),
            'data_source': 'acc_sync',
            'template_type': analysis.get('template_type', 'custom'),
            'steps_count': steps_count,
            'steps_config': json.dumps(steps_config),
            'template_config': json.dumps(workflow),  # 保存完整的原始数据
            'default_settings': json.dumps({}),
            'additional_options': json.dumps(workflow.get('additionalOptions', {})),
            'approval_status_options': json.dumps(workflow.get('approvalStatusOptions', [])),
            'copy_files_options': json.dumps(workflow.get('copyFilesOptions', {})),
            'attached_attributes': json.dumps(workflow.get('attachedAttributes', [])),
            'update_attributes_options': json.dumps(workflow.get('updateAttributesOptions', {})),
            'created_by': json.dumps(workflow.get('createdBy', {})),
            'is_active': workflow.get('status', 'ACTIVE') == 'ACTIVE',
            'is_public': True,  # ACC模板默认为公共
            'is_template': True,
            'base_template_key': analysis.get('base_template_match'),
            'template_characteristics': json.dumps({
                'complexity_level': analysis.get('complexity_level', 'simple'),
                'has_group_review': analysis.get('has_group_review', False),
                'has_role_assignments': analysis.get('has_role_assignments', False),
                'complexity_score': analysis.get('complexity_score', 0),
                'analysis_version': '1.0'
            }),
            'last_synced_at': now,
            'sync_status': 'synced',
            'created_at': created_at or now,
            'updated_at': updated_at or now
        }
    
    def _transform_steps_config_for_template(self, steps: List[Dict]) -> List[Dict]:
        """
        转换步骤配置为模板格式
        """
        transformed_steps = []
        
        for idx, step in enumerate(steps):
            # 解析组审核配置
            group_review = step.get('groupReview', {})
            
            # 确定审核者类型
            reviewer_type = 'SINGLE_REVIEWER'
            if group_review.get('enabled'):
                reviewer_type = 'GROUP_APPROVAL'
            elif len(step.get('candidates', {}).get('users', [])) > 1:
                reviewer_type = 'MULTIPLE_REVIEWERS'
            
            # 转换步骤配置
            step_config = {
                'id': step.get('id', f'step_{idx + 1}'),
                'name': step.get('name', f'Step {idx + 1}'),
                'type': step.get('type', 'REVIEWER'),
                'order': idx + 1,
                'reviewer_type': reviewer_type,
                'time_allowed': step.get('duration', 3),
                'time_unit': step.get('dueDateType', 'CALENDAR_DAY'),
                'enable_sent_back': True,  # 默认启用
                'group_review': {
                    'enabled': group_review.get('enabled', False),
                    'type': group_review.get('type', 'MINIMUM'),
                    'min': group_review.get('min', 1)
                },
                'candidates': step.get('candidates', {
                    'users': [],
                    'roles': [],
                    'companies': []
                }),
                'original_step_data': step  # 保存原始数据
            }
            
            transformed_steps.append(step_config)
        
        return transformed_steps
    
    # ========================================================================
    # 基础模板管理
    # ========================================================================
    
    def get_base_templates(self, category: Optional[str] = None) -> List[Dict]:
        """
        获取基础模板列表
        
        Args:
            category: 模板分类过滤
            
        Returns:
            基础模板列表
        """
        try:
            with self.da.get_connection() as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                    if category:
                        cur.execute(
                            "SELECT * FROM base_templates WHERE category = %s AND is_active = true ORDER BY display_order",
                            (category,)
                        )
                    else:
                        cur.execute(
                            "SELECT * FROM base_templates WHERE is_active = true ORDER BY display_order"
                        )
                    
                    templates = cur.fetchall()
                    
                    # 转换为字典列表并解析JSON字段
                    result = []
                    for template in templates:
                        template_dict = dict(template)
                        
                        # 解析JSON字段
                        if template_dict.get('base_steps_config'):
                            try:
                                template_dict['base_steps_config'] = json.loads(template_dict['base_steps_config'])
                            except:
                                template_dict['base_steps_config'] = []
                        
                        result.append(template_dict)
                    
                    return result
                    
        except Exception as e:
            error_msg = f"获取基础模板失败: {str(e)}"
            print(f"❌ {error_msg}")
            return []
    
    def create_workflow_from_base_template(
        self,
        base_template_key: str,
        workflow_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        基于基础模板创建工作流
        
        Args:
            base_template_key: 基础模板键值
            workflow_data: 工作流配置数据
            
        Returns:
            创建结果
        """
        try:
            # 获取基础模板
            base_templates = self.get_base_templates()
            base_template = next(
                (t for t in base_templates if t['template_key'] == base_template_key), 
                None
            )
            
            if not base_template:
                raise ValueError(f"基础模板不存在: {base_template_key}")
            
            # 合并基础模板和用户配置
            merged_config = {
                'name': workflow_data.get('name', base_template['name']),
                'description': workflow_data.get('description', base_template['description']),
                'steps': base_template['base_steps_config'].copy(),
                'base_template_key': base_template_key,
                'template_type': base_template['template_key'],
                'steps_count': base_template['steps_count'],
                'has_group_review': base_template['has_group_review']
            }
            
            # 应用用户自定义配置
            if 'steps_config' in workflow_data:
                # 用户提供了步骤配置，合并到基础步骤中
                user_steps = workflow_data['steps_config']
                for i, user_step in enumerate(user_steps):
                    if i < len(merged_config['steps']):
                        # 更新现有步骤
                        merged_config['steps'][i].update(user_step)
            
            return {
                'status': 'success',
                'workflow_config': merged_config,
                'base_template': base_template
            }
            
        except Exception as e:
            error_msg = f"基于基础模板创建工作流失败: {str(e)}"
            print(f"❌ {error_msg}")
            return {'status': 'error', 'error': error_msg}
    
    # ========================================================================
    # 注意：账户数据同步功能已移除
    # 现在使用独立的 database_sql/account_sync.py 来处理账户、用户、公司、角色同步
    # ========================================================================
    
    async def full_project_sync_with_templates(
        self,
        project_id: str,
        access_token: str,
        sync_templates: bool = True,
        fetch_detailed_template_data: bool = True,
        show_progress: bool = True
    ) -> Dict[str, Any]:
        """
        完整的项目同步（包含模板和评审数据）
        注意：账户数据同步已移除，请使用独立的 account_sync.py
        
        Args:
            project_id: 项目ID
            access_token: 访问令牌
            sync_templates: 是否同步工作流模板
            fetch_detailed_template_data: 是否获取详细模板数据
            show_progress: 是否显示进度
            
        Returns:
            完整的同步结果
        """
        if show_progress:
            print(f"\n[START] Starting project sync (templates + reviews)")
            print(f"   项目ID: {project_id}")
            print(f"   包含工作流模板: {sync_templates}")
            print(f"   详细模板数据: {fetch_detailed_template_data}")
            print("   注意: 账户数据同步请使用独立的 account_sync.py")
            print("=" * 80)
        
        start_time = time.time()
        results = {}
        
        # 设置临时headers供API调用使用
        self._temp_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        try:
            # 创建异步HTTP会话
            async with aiohttp.ClientSession() as session:
                
                # 阶段1: 同步工作流模板（如果启用）
                if sync_templates:
                    if show_progress:
                        print(f"\nTARGET: 开始同步工作流模板...")
                    
                    template_result = await self.sync_workflow_templates_enhanced(
                        session, project_id, access_token, 
                        fetch_detailed_template_data, show_progress
                    )
                    results['template_sync'] = template_result
                    
                    # 更新统计
                    self.sync_stats['templates_synced'] += template_result.get('templates_inserted', 0)
                    self.sync_stats['templates_updated'] += template_result.get('templates_updated', 0)
                
                # 阶段2: 同步评审数据
                if show_progress:
                    print(f"\nINFO: 开始同步评审数据...")
                
                # 获取评审列表
                reviews = await self.async_fetch_all_reviews_with_pagination(
                    session, None, project_id, show_progress=show_progress
                )
                
                if reviews:
                    # 异步并行同步评审
                    review_result = await self.async_sync_reviews_parallel(
                        None, project_id, reviews, show_progress
                    )
                    results['review_sync'] = review_result
                else:
                    results['review_sync'] = {
                        'status': 'no_reviews',
                        'message': '项目中没有找到评审数据'
                    }
            
            total_time = time.time() - start_time
            
            # 生成综合报告
            final_result = {
                'project_id': project_id,
                'sync_components': {
                    'workflow_templates': sync_templates,
                    'review_data': True,
                    'account_data': False  # 账户数据同步已移除
                },
                'results': results,
                'sync_statistics': self.sync_stats,
                'performance_metrics': self.get_performance_report(),
                'execution_time': f"{total_time:.2f}秒",
                'sync_time': datetime.now(timezone.utc).isoformat()
            }
            
            if show_progress:
                print(f"\n✅ 完整项目同步完成，总耗时: {total_time:.2f}秒")
                print(f"📊 同步统计:")
                if sync_templates:
                    print(f"   模板: {self.sync_stats['templates_synced']} 新增, {self.sync_stats['templates_updated']} 更新")
                print(f"   工作流: {self.sync_stats['workflows_synced']} 新增, {self.sync_stats['workflows_updated']} 更新")
                print(f"   评审: {self.sync_stats['reviews_synced']} 新增, {self.sync_stats['reviews_updated']} 更新")
            
            return final_result
            
        except Exception as e:
            error_msg = f"项目同步失败: {str(e)}"
            print(f"✗ {error_msg}")
            return {
                'error': error_msg,
                'project_id': project_id,
                'results': results,
                'sync_statistics': self.sync_stats
            }
        
        finally:
            # 清理临时headers
            if hasattr(self, '_temp_headers'):
                delattr(self, '_temp_headers')


    def _create_review_step_candidates_from_workflow_template(self, review_id: int, workflow_steps_config: List[Dict]) -> None:
        """
        基于工作流模板为评审创建步骤候选人配置（正确的逻辑）
        
        Args:
            review_id: 评审ID
            workflow_steps_config: 工作流模板的步骤配置
        """
        try:
            if not workflow_steps_config:
                print(f"  [CANDIDATES] No workflow template found for review {review_id}")
                return
            
            candidates_batch = []
            
            for step_order, step_config in enumerate(workflow_steps_config, 1):
                step_id = step_config.get('id')
                if not step_id:
                    print(f"  [WARNING] Step {step_order} has no ID, skipping")
                    continue
                
                step_name = step_config.get('name', 'Unknown Step')
                step_type = step_config.get('type', 'REVIEWER')
                step_candidates = step_config.get('candidates', {})
                
                # 标准化候选人数据格式
                if isinstance(step_candidates, dict):
                    standardized_candidates = {
                        'users': step_candidates.get('users', []),
                        'roles': step_candidates.get('roles', []),
                        'companies': step_candidates.get('companies', [])
                    }
                else:
                    standardized_candidates = {'users': [], 'roles': [], 'companies': []}
                
                candidate_config = {
                    'review_id': review_id,
                    'step_id': step_id,
                    'step_name': step_name,
                    'step_type': step_type,
                    'step_order': step_order,
                    'candidates': standardized_candidates,
                    'source': 'workflow_template'  # 来源是工作流模板
                }
                
                candidates_batch.append(candidate_config)
            
            # 批量插入候选人配置
            if candidates_batch:
                self._batch_upsert_review_step_candidates(candidates_batch)
                print(f"  [CANDIDATES] Created {len(candidates_batch)} step candidate configurations from workflow template")
            else:
                print(f"  [CANDIDATES] No valid steps found in workflow template for review {review_id}")
                
        except Exception as e:
            print(f"[ERROR] Failed to create review step candidates from workflow template: {e}")

    def _create_review_step_candidates_from_progress(self, review_id: int, steps: List[Dict], workflow_steps_config: List[Dict]) -> None:
        """
        从 review_progress 创建步骤候选人配置（使用 ACC step_id）

        这是根本性修复：使用 ACC API 返回的 step_id 而不是 workflow template step_id
        这样 review_step_candidates.step_id 会匹配 review_progress.step_id

        Args:
            review_id: 评审ID
            steps: ACC API 返回的步骤数据（包含 ACC step_id）
            workflow_steps_config: 工作流步骤配置（用于 candidates fallback）
        """
        try:
            candidates_batch = []
            processed_steps = set()  # 跟踪已处理的步骤，避免重复

            print(f"  [CANDIDATES] Creating step candidates from ACC progress data (review_id={review_id})")

            for step_data in steps:
                # 关键：使用 ACC API 的 step_id，不是 workflow template 的 step_id
                step_id = step_data.get('stepId') or step_data.get('id')
                if not step_id:
                    print(f"  [WARNING] Step has no step_id, skipping")
                    continue

                # 检查是否已处理过这个步骤（避免重复，因为 send-back 可能产生重复 step_id）
                step_key = (review_id, step_id)
                if step_key in processed_steps:
                    print(f"  [SKIP] Step {step_id} already processed")
                    continue
                processed_steps.add(step_key)

                # 候选人优先级：
                # 1. nextActionBy.candidates (当前活跃步骤)
                # 2. step.candidates (步骤本身的候选人)
                # 3. workflow_steps_config (从 workflow template fallback)
                candidates = {}
                source = 'acc_sync'

                # 优先级1: nextActionBy (当前活跃步骤的候选人)
                if step_data.get('status') in ['PENDING', 'CLAIMED', 'pending', 'claimed']:
                    next_action_by = step_data.get('nextActionBy', {})
                    if next_action_by and next_action_by.get('candidates'):
                        candidates = next_action_by.get('candidates', {})
                        source = 'acc_sync'
                        print(f"  [CANDIDATES] Step {step_id}: Using nextActionBy candidates")

                # 优先级2: 步骤本身的 candidates
                if not candidates or (isinstance(candidates, dict) and not any(candidates.values())):
                    candidates = step_data.get('candidates', {})
                    if candidates and any(candidates.values()):
                        source = 'acc_sync'
                        print(f"  [CANDIDATES] Step {step_id}: Using step.candidates")

                # 优先级3: 从 workflow 配置 fallback（通过 step_order 匹配）
                if not candidates or (isinstance(candidates, dict) and not any(candidates.values())):
                    step_order = step_data.get('stepOrder') or step_data.get('order', 0)
                    # 通过 step_order 在 workflow template 中查找候选人
                    if workflow_steps_config and step_order > 0 and step_order <= len(workflow_steps_config):
                        template_step = workflow_steps_config[step_order - 1]
                        template_candidates = template_step.get('candidates', {})
                        if template_candidates and any(template_candidates.values()):
                            candidates = template_candidates
                            source = 'workflow_template'
                            print(f"  [CANDIDATES] Step {step_id}: Fallback to workflow template candidates")

                # 如果还是没有候选人，设置空结构
                if not candidates or (isinstance(candidates, dict) and not any(candidates.values())):
                    candidates = {'users': [], 'roles': [], 'companies': []}
                    source = 'acc_sync'
                    print(f"  [CANDIDATES] Step {step_id}: No candidates found, using empty structure")

                # 标准化候选人数据格式
                if isinstance(candidates, dict):
                    standardized_candidates = {
                        'users': candidates.get('users', []),
                        'roles': candidates.get('roles', []),
                        'companies': candidates.get('companies', [])
                    }
                else:
                    standardized_candidates = {'users': [], 'roles': [], 'companies': []}

                # 构建候选人配置
                candidate_config = {
                    'review_id': review_id,
                    'step_id': step_id,  # ✅ 使用 ACC step_id（关键修复）
                    'step_name': step_data.get('stepName') or step_data.get('name', 'Unknown Step'),
                    'step_type': step_data.get('stepType') or step_data.get('type', 'REVIEWER'),
                    'step_order': step_data.get('stepOrder') or step_data.get('order', 0),
                    'candidates': standardized_candidates,
                    'source': source
                }

                candidates_batch.append(candidate_config)

            # 批量 UPSERT 候选人配置
            if candidates_batch:
                self._batch_upsert_review_step_candidates(candidates_batch)
                print(f"  [CANDIDATES] ✓ Created {len(candidates_batch)} step candidate configurations using ACC step_ids")
            else:
                print(f"  [CANDIDATES] No valid steps to create candidate configurations")

        except Exception as e:
            print(f"✗ [ERROR] Failed to create review step candidates from progress: {e}")
            import traceback
            traceback.print_exc()

    def _create_candidates_from_template(self, review_id: int, workflow_steps_config: List[Dict]) -> None:
        """
        從 workflow template 創建完整的步驟候選人配置

        這是方案2的核心方法：
        - 為所有 template 步驟創建 candidates（即使未執行）
        - 使用 template step_id（不是 ACC step_id）
        - 確保配置完整性

        Args:
            review_id: 評審ID
            workflow_steps_config: 工作流步驟配置（完整的模板步驟）
        """
        try:
            if not workflow_steps_config:
                print(f"  [CANDIDATES] No workflow steps config provided, skipping candidate creation")
                return

            candidates_batch = []

            print(f"  [CANDIDATES] Creating candidates from workflow template (review_id={review_id}, {len(workflow_steps_config)} steps)")

            for idx, template_step in enumerate(workflow_steps_config):
                # ✅ 使用 template step_id（關鍵！）
                template_step_id = template_step.get('id')
                if not template_step_id:
                    print(f"  [WARNING] Template step missing 'id' field, skipping")
                    continue

                # 獲取步驟配置
                step_name = template_step.get('name', 'Unknown Step')
                step_type = template_step.get('type', 'REVIEWER')
                # ✅ 使用索引 + 1 作為 step_order（因為 order 從 1 開始）
                step_order = template_step.get('order', idx + 1)

                # 獲取 candidates 配置
                candidates = template_step.get('candidates', {})
                if isinstance(candidates, dict):
                    standardized_candidates = {
                        'users': candidates.get('users', []),
                        'roles': candidates.get('roles', []),
                        'companies': candidates.get('companies', [])
                    }
                else:
                    standardized_candidates = {'users': [], 'roles': [], 'companies': []}

                candidate_config = {
                    'review_id': review_id,
                    'step_id': template_step_id,  # ✅ 使用 template step_id
                    'step_name': step_name,
                    'step_type': step_type,
                    'step_order': step_order,
                    'candidates': standardized_candidates,
                    'source': 'workflow_template'
                }

                candidates_batch.append(candidate_config)
                print(f"  [CANDIDATES]   Step {step_order}: {step_name} (template_id={template_step_id})")

            # 批量 UPSERT 候選人配置
            if candidates_batch:
                self._batch_upsert_review_step_candidates(candidates_batch)
                print(f"  [CANDIDATES] ✓ Created {len(candidates_batch)} complete step candidate configurations from template")
            else:
                print(f"  [CANDIDATES] No valid steps to create candidate configurations")

        except Exception as e:
            print(f"✗ [ERROR] Failed to create candidates from template: {e}")
            import traceback
            traceback.print_exc()

    def _sync_progress_with_template_mapping(self, review_id: int, steps: List[Dict], workflow_steps_config: List[Dict]) -> None:
        """
        同步 progress，並自動關聯到 template step_id

        這是方案2的核心方法：
        - 同步 ACC API 的執行記錄
        - 通過 step_order 自動關聯到 template_step_id
        - 保留 ACC step_id 用於歷史追蹤

        Args:
            review_id: 評審ID
            steps: ACC API 返回的步驟執行數據
            workflow_steps_config: 工作流步驟配置（用於查找 template_step_id）
        """
        try:
            batch_data = []

            print(f"  [PROGRESS] Syncing progress with template mapping (review_id={review_id}, {len(steps)} progress records)")

            for idx, step_data in enumerate(steps):
                # ACC step_id（執行時的ID）
                acc_step_id = step_data.get('stepId') or step_data.get('id')
                if not acc_step_id:
                    print(f"  [WARNING] Progress step missing 'stepId', skipping")
                    continue

                # 步驟順序（用於匹配 template）
                # ✅ 使用 API 的 stepOrder，如果不存在則使用索引 + 1
                step_order = step_data.get('stepOrder') or step_data.get('order') or (idx + 1)

                # ✅ 通過 step_order 查找對應的 template step_id
                template_step_id = None
                if workflow_steps_config and 0 < step_order <= len(workflow_steps_config):
                    template_step = workflow_steps_config[step_order - 1]  # order 從 1 開始
                    template_step_id = template_step.get('id')
                    print(f"  [PROGRESS]   Step {step_order}: ACC_id={acc_step_id} → template_id={template_step_id}")
                else:
                    print(f"  [WARNING] Cannot find template step for order {step_order} (total: {len(workflow_steps_config)})")

                # 從 ACC API 獲取 candidates（用於歷史記錄）
                candidates = step_data.get('candidates', {})
                if not candidates or (isinstance(candidates, dict) and not any(candidates.values())):
                    # 從工作流配置補充 candidates
                    if template_step_id and workflow_steps_config:
                        workflow_candidates = self._get_candidates_from_workflow_config(
                            workflow_steps_config, template_step_id
                        )
                        if workflow_candidates:
                            candidates = workflow_candidates

                progress_data = {
                    'review_id': review_id,
                    'step_id': acc_step_id,  # ACC step_id（保留用於歷史記錄）
                    'template_step_id': template_step_id,  # ✅ 新增：關聯到 template
                    'step_name': step_data.get('stepName') or step_data.get('name'),
                    'step_type': self._map_step_type(step_data.get('type', 'reviewer')),
                    'step_order': step_order,
                    'status': self._map_step_status(step_data.get('status', 'pending')),
                    'assigned_to': step_data.get('assignedTo', []),
                    'claimed_by': step_data.get('claimedBy', {}),
                    'completed_by': step_data.get('completedBy', {}),
                    'action_by': step_data.get('actionBy', {}),
                    'candidates': candidates,
                    'decision': step_data.get('decision'),
                    'comments': step_data.get('comments'),
                    'notes': step_data.get('notes'),
                    'due_date': self._parse_timestamp(step_data.get('dueDate')),
                    'started_at': self._parse_timestamp(step_data.get('startedAt')),
                    'completed_at': self._parse_timestamp(step_data.get('completedAt')),
                    'end_time': self._parse_timestamp(step_data.get('endTime'))
                }

                batch_data.append(progress_data)

            # 批量UPSERT
            if batch_data:
                try:
                    # 檢查是否有增強版的 batch_upsert_review_steps 方法
                    if hasattr(self.da, 'batch_upsert_review_steps'):
                        inserted, updated = self.da.batch_upsert_review_steps(batch_data)
                        print(f"  [PROGRESS] ✓ Batch UPSERT: {inserted} inserted, {updated} updated")
                    else:
                        # 回退到普通插入
                        inserted_count = self.da.batch_insert_review_steps(batch_data)
                        print(f"  [PROGRESS] ✓ Batch INSERT: {inserted_count} records")
                except Exception as e:
                    print(f"✗ [ERROR] Failed to batch upsert progress: {e}")
                    raise

            # ✅ 新增：為當前活躍步驟創建 progress 記錄
            # ACC API 只返回已完成的步驟，需要為當前待處理步驟創建記錄
            self._create_current_step_progress(review_id, steps, workflow_steps_config)

        except Exception as e:
            print(f"✗ [ERROR] Failed to sync progress with template mapping: {e}")
            import traceback
            traceback.print_exc()

    def _create_current_step_progress(self, review_id: int, executed_steps: List[Dict], workflow_steps_config: List[Dict]) -> None:
        """
        為當前活躍步驟創建 progress 記錄

        ACC API 只返回已完成的步驟，不返回當前待處理步驟。
        這個方法檢測並創建當前步驟的 progress 記錄。

        邏輯：
        1. 找出已執行步驟的最大 step_order
        2. 當前步驟應該是 max_order + 1
        3. 如果該步驟在 workflow template 中存在，且沒有 progress 記錄，則創建

        Args:
            review_id: 評審ID
            executed_steps: ACC API 返回的已執行步驟
            workflow_steps_config: 工作流步驟配置
        """
        try:
            # ✅ 診斷日誌：確認方法被調用
            print(f"  [CURRENT_STEP] Processing review_id={review_id}, executed_steps={len(executed_steps)}, workflow_steps={len(workflow_steps_config) if workflow_steps_config else 0}")

            if not workflow_steps_config:
                print(f"  [CURRENT_STEP] Skipped - no workflow config for review {review_id}")
                return

            # 1. 找出已執行步驟的最大 step_order
            # ✅ 從數據庫查詢已插入的 review_progress，找出實際的最大 step_order
            # 這比依賴 API 返回的數據更可靠
            max_executed_order = 0
            try:
                with self.da.get_cursor() as cursor:
                    cursor.execute("""
                        SELECT COALESCE(MAX(step_order), 0) as max_order
                        FROM review_progress
                        WHERE review_id = %s
                    """, (review_id,))
                    result = cursor.fetchone()
                    if result:
                        max_executed_order = result['max_order'] if isinstance(result, dict) else result[0]
            except Exception as e:
                print(f"  [CURRENT_STEP] Error querying max step_order: {e}")
                # Fallback: 從 API 數據計算
                for step_data in executed_steps:
                    step_order = step_data.get('stepOrder') or step_data.get('order', 0)
                    if step_order > max_executed_order:
                        max_executed_order = step_order

            # 2. 當前活躍步驟應該是下一個
            current_step_order = max_executed_order + 1

            # ✅ 診斷日誌：顯示計算結果
            print(f"  [CURRENT_STEP] max_executed_order={max_executed_order}, current_step_order={current_step_order}")

            # 3. 檢查該步驟是否在 workflow 中存在
            if current_step_order > len(workflow_steps_config):
                # 已經完成所有步驟
                print(f"  [CURRENT_STEP] All steps completed (max_order={max_executed_order}, total={len(workflow_steps_config)})")
                return

            # 4. 獲取該步驟的 template 配置
            template_step = workflow_steps_config[current_step_order - 1]
            template_step_id = template_step.get('id')

            if not template_step_id:
                print(f"  [WARNING] Cannot find template step_id for order {current_step_order}")
                return

            # 5. 檢查是否已經有該步驟的 progress 記錄
            existing_progress = self.da.get_review_progress_by_template_step(review_id, template_step_id)
            if existing_progress:
                print(f"  [CURRENT_STEP] Progress already exists for step {current_step_order} (template_id={template_step_id})")
                return

            # 6. 創建當前步驟的 progress 記錄
            print(f"  [CURRENT_STEP] Creating progress for current step {current_step_order}: {template_step.get('name')} (template_id={template_step_id})")

            # 從 template 獲取 candidates
            candidates = template_step.get('candidates', {})
            standardized_candidates = {
                'users': candidates.get('users', []) if isinstance(candidates.get('users'), list) else [],
                'roles': candidates.get('roles', []) if isinstance(candidates.get('roles'), list) else [],
                'companies': candidates.get('companies', []) if isinstance(candidates.get('companies'), list) else []
            }

            progress_data = {
                'review_id': review_id,
                'step_id': template_step_id,  # 使用 template step_id（因為 ACC 沒有給 runtime ID）
                'template_step_id': template_step_id,
                'step_name': template_step.get('name', 'Unknown Step'),
                'step_type': self._map_step_type(template_step.get('type', 'REVIEWER')),
                'step_order': current_step_order,
                'status': 'PENDING',  # 當前步驟狀態為 PENDING
                'assigned_to': [],
                'claimed_by': {},
                'completed_by': {},
                'action_by': {},
                'candidates': standardized_candidates,
                'decision': None,
                'comments': None,
                'notes': '',
                'due_date': None,
                'started_at': None,
                'completed_at': None,
                'end_time': None
            }

            # 插入記錄
            try:
                if hasattr(self.da, 'batch_upsert_review_steps'):
                    inserted, updated = self.da.batch_upsert_review_steps([progress_data])
                    print(f"  [CURRENT_STEP] ✓ Created current step progress (inserted={inserted}, updated={updated})")
                else:
                    inserted_count = self.da.batch_insert_review_steps([progress_data])
                    print(f"  [CURRENT_STEP] ✓ Created current step progress (inserted={inserted_count})")
            except Exception as e:
                print(f"✗ [ERROR] Failed to create current step progress: {e}")
                raise

        except Exception as e:
            print(f"✗ [ERROR] Failed in _create_current_step_progress: {e}")
            import traceback
            traceback.print_exc()

    def _create_review_step_candidates_from_cache(self, review_id: int, steps: List[Dict], workflow_steps_config: List[Dict]) -> None:
        """
        从缓存的工作流数据为评审创建步骤候选人配置
        
        Args:
            review_id: 评审ID
            steps: ACC API 返回的步骤数据
            workflow_steps_config: 缓存的工作流步骤配置
        """
        try:
            candidates_batch = []
            processed_steps = set()  # 跟踪已处理的步骤，避免重复
            
            for step_data in steps:
                step_id = step_data.get('stepId') or step_data.get('id')
                if not step_id:
                    continue
                
                # 检查是否已处理过这个步骤（避免重复）
                step_key = (review_id, step_id)
                if step_key in processed_steps:
                    continue
                processed_steps.add(step_key)
                
                # 优先级1: nextActionBy (当前活跃步骤)
                candidates = {}
                source = 'acc_sync'  # 默认为 acc_sync，符合约束
                
                if step_data.get('status') in ['PENDING', 'CLAIMED']:
                    # 这是当前活跃步骤，尝试从 nextActionBy 获取
                    next_action_by = step_data.get('nextActionBy', {})
                    if next_action_by and next_action_by.get('candidates'):
                        candidates = next_action_by.get('candidates', {})
                        source = 'acc_sync'  # nextActionBy 来源也标记为 acc_sync
                    else:
                        # 优先级2: 步骤本身的 candidates
                        candidates = step_data.get('candidates', {})
                        source = 'acc_sync' if candidates else 'acc_sync'
                else:
                    # 优先级2: 步骤本身的 candidates
                    candidates = step_data.get('candidates', {})
                    source = 'acc_sync' if candidates else 'acc_sync'
                
                # 优先级3: 从工作流配置获取
                if not candidates or (isinstance(candidates, dict) and not any(candidates.values())):
                    workflow_candidates = self._get_candidates_from_workflow_config(
                        workflow_steps_config, step_id
                    )
                    if workflow_candidates:
                        candidates = workflow_candidates
                        source = 'workflow_template'  # 从工作流配置获取的标记为 workflow_template
                    else:
                        # 设置空的候选人结构
                        candidates = {'users': [], 'roles': [], 'companies': []}
                        source = 'acc_sync'  # 空的也标记为 acc_sync
                
                # 标准化候选人数据格式
                if isinstance(candidates, dict):
                    standardized_candidates = {
                        'users': candidates.get('users', []),
                        'roles': candidates.get('roles', []),
                        'companies': candidates.get('companies', [])
                    }
                else:
                    standardized_candidates = {'users': [], 'roles': [], 'companies': []}
                
                candidate_config = {
                    'review_id': review_id,
                    'step_id': step_id,
                    'step_name': step_data.get('stepName') or step_data.get('name'),
                    'step_type': step_data.get('stepType') or step_data.get('type'),
                    'step_order': step_data.get('stepOrder') or step_data.get('order', 0),
                    'candidates': standardized_candidates,
                    'source': source
                }
                
                candidates_batch.append(candidate_config)
            
            # 批量插入候选人配置
            if candidates_batch:
                self._batch_upsert_review_step_candidates(candidates_batch)
                print(f"  [CANDIDATES] Created {len(candidates_batch)} step candidate configurations")
                
        except Exception as e:
            print(f"[ERROR] Failed to create review step candidates: {e}")
    
    def _batch_upsert_review_step_candidates(self, candidates_data: List[Dict]) -> None:
        """
        批量UPSERT评审步骤候选人配置
        
        Args:
            candidates_data: 候选人配置数据列表
        """
        if not candidates_data:
            return
        
        try:
            with self.da.get_connection() as conn:
                with conn.cursor() as cursor:
                    # 构建批量UPSERT SQL
                    upsert_sql = """
                        INSERT INTO review_step_candidates (
                            review_id, step_id, step_name, step_type, step_order,
                            candidates, source
                        ) VALUES %s
                        ON CONFLICT (review_id, step_id) 
                        DO UPDATE SET
                            step_name = EXCLUDED.step_name,
                            step_type = EXCLUDED.step_type,
                            step_order = EXCLUDED.step_order,
                            candidates = EXCLUDED.candidates,
                            source = EXCLUDED.source,
                            updated_at = CURRENT_TIMESTAMP
                    """
                    
                    # 准备数据
                    values_list = []
                    for config in candidates_data:
                        values_list.append((
                            config['review_id'],
                            config['step_id'],
                            config['step_name'],
                            config['step_type'],
                            config['step_order'],
                            psycopg2.extras.Json(config['candidates']),
                            config['source']
                        ))
                    
                    # 执行批量UPSERT
                    psycopg2.extras.execute_values(
                        cursor, upsert_sql, values_list,
                        template=None, page_size=100
                    )
                    
                    conn.commit()
                    
        except Exception as e:
            print(f"[ERROR] Failed to batch upsert review step candidates: {e}")
            raise


# ============================================================================
# 便捷函数
# ============================================================================

def get_enhanced_sync_manager(
    data_access: Optional[ReviewDataAccess] = None,
    **kwargs
) -> EnhancedReviewSyncManager:
    """获取增强的同步管理器实例"""
    return EnhancedReviewSyncManager(data_access, **kwargs)


if __name__ == "__main__":
    # 测试代码
    print("增强的审批系统同步管理器测试")
    print("=" * 60)
    
    try:
        sync_manager = get_enhanced_sync_manager(
            max_concurrent=10,
            enable_cache=True,
            cache_ttl=3600,
            cache_max_size=5000,
            batch_size=100
        )
        print("SUCCESS: 增强同步管理器初始化成功")
        
        # 显示缓存统计
        cache_stats = sync_manager.cache.get_stats()
        print(f"\n缓存统计:")
        print(json.dumps(cache_stats, indent=2, ensure_ascii=False))
        
        # 显示性能报告
        report = sync_manager.get_performance_report()
        print(f"\n当前性能指标:")
        print(json.dumps(report, indent=2, ensure_ascii=False, default=str))
        
    except Exception as e:
        print(f"✗ 错误: {e}")
        import traceback
        traceback.print_exc()

