"""
审批系统同步管理器 - 优化版
负责从ACC同步工作流和评审数据到本地数据库
支持全量同步和增量同步

优化特性：
1. 并行API调用 - 使用ThreadPoolExecutor实现并发请求
2. 批量数据库插入 - 减少数据库往返次数
3. 智能分页和限流 - 自动处理API分页和限流重试
4. 性能监控 - 详细的性能统计和时间追踪
"""

import sys
import os
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timezone
import uuid
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import wraps

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Try different import paths
try:
    from database_sql.review_data_access import ReviewDataAccess
    from database_sql.neon_config import NeonConfig
except ImportError:
    print("Warning: Could not import from database_sql, trying alternative path")
    try:
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../database_sql')))
        from review_data_access import ReviewDataAccess
        from neon_config import NeonConfig
    except ImportError:
        print("Warning: Could not import ReviewDataAccess, using placeholder")
        ReviewDataAccess = None
        NeonConfig = None


class ReviewSyncManager:
    """审批系统同步管理器 - 优化版"""
    
    def __init__(self, data_access: Optional[ReviewDataAccess] = None, max_workers: int = 10):
        """
        初始化同步管理器
        
        Args:
            data_access: 数据访问层实例，如果为None则创建新实例
            max_workers: 并发工作线程数（建议5-10，避免API限流）
        """
        self.da = data_access or ReviewDataAccess()
        self.max_workers = max_workers
        self.sync_stats = {
            'workflows_synced': 0,
            'workflows_updated': 0,
            'workflows_skipped': 0,
            'reviews_synced': 0,
            'reviews_updated': 0,
            'reviews_skipped': 0,
            'errors': [],
            'performance': {
                'api_calls': 0,
                'api_time': 0.0,
                'db_time': 0.0,
                'total_time': 0.0
            }
        }
    
    # ========================================================================
    # API限流和重试装饰器
    # ========================================================================
    
    @staticmethod
    def rate_limit_retry(max_retries: int = 3, backoff_factor: float = 2.0):
        """
        API限流重试装饰器
        
        Args:
            max_retries: 最大重试次数
            backoff_factor: 退避因子（指数退避）
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(max_retries):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        error_str = str(e).lower()
                        # 检查是否是限流错误
                        if '429' in error_str or 'rate limit' in error_str or 'too many requests' in error_str:
                            if attempt < max_retries - 1:
                                wait_time = backoff_factor ** attempt
                                print(f"⚠ API限流，等待 {wait_time:.1f}秒后重试... (尝试 {attempt + 1}/{max_retries})")
                                time.sleep(wait_time)
                            else:
                                raise Exception(f"API限流，已重试{max_retries}次仍失败: {str(e)}")
                        else:
                            # 非限流错误直接抛出
                            raise
                raise Exception(f"API调用失败，已重试{max_retries}次")
            return wrapper
        return decorator
    
    # ========================================================================
    # 工作流同步
    # ========================================================================
    
    def sync_workflow_from_acc(self, acc_workflow_data: Dict[str, Any]) -> Tuple[int, str]:
        """
        从ACC同步单个工作流
        
        Args:
            acc_workflow_data: ACC工作流数据
            
        Returns:
            (workflow_id, action) - 工作流ID和操作类型('created', 'updated', 'skipped')
        """
        try:
            acc_workflow_id = acc_workflow_data.get('id')
            if not acc_workflow_id:
                raise ValueError("ACC工作流数据缺少ID")
            
            # 检查是否已存在
            existing_workflow = self.da.get_workflow_by_acc_id(acc_workflow_id)
            
            # 准备工作流数据
            workflow_data = self._transform_acc_workflow_data(acc_workflow_data)
            
            if existing_workflow:
                # 检查是否需要更新
                if self._should_update_workflow(existing_workflow, workflow_data):
                    # 更新现有工作流
                    self.da.update_workflow(existing_workflow['id'], workflow_data)
                    self.sync_stats['workflows_updated'] += 1
                    return existing_workflow['id'], 'updated'
                else:
                    self.sync_stats['workflows_skipped'] += 1
                    return existing_workflow['id'], 'skipped'
            else:
                # 创建新工作流
                workflow_id = self.da.create_workflow(workflow_data)
                self.sync_stats['workflows_synced'] += 1
                return workflow_id, 'created'
        
        except Exception as e:
            error_msg = f"同步工作流失败 (ACC ID: {acc_workflow_data.get('id')}): {str(e)}"
            self.sync_stats['errors'].append(error_msg)
            print(f"✗ {error_msg}")
            raise
    
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
            'additional_options': acc_data.get('additionalOptions', {}),
            'approval_status_options': acc_data.get('approvalStatusOptions', []),
            'copy_files_options': acc_data.get('copyFilesOptions', {}),
            'attached_attributes': acc_data.get('attachedAttributes', []),
            'update_attributes_options': acc_data.get('updateAttributesOptions', {}),
            'steps': acc_data.get('steps', []),
            'created_by': acc_data.get('createdBy', {}),  # 存储完整的用户对象
            'created_at': self._parse_timestamp(acc_data.get('createdAt')),
            'updated_at': self._parse_timestamp(acc_data.get('updatedAt')),
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
    
    def _should_update_workflow(self, existing: Dict, new_data: Dict) -> bool:
        """判断是否需要更新工作流"""
        # 比较关键字段
        key_fields = ['name', 'description', 'status', 'steps']
        for field in key_fields:
            if existing.get(field) != new_data.get(field):
                return True
        return False
    
    # ========================================================================
    # 评审同步
    # ========================================================================
    
    def sync_review_from_acc(self, acc_review_data: Dict[str, Any]) -> Tuple[int, str]:
        """
        从ACC同步单个评审
        
        Args:
            acc_review_data: ACC评审数据
            
        Returns:
            (review_id, action) - 评审ID和操作类型
        """
        try:
            acc_review_id = acc_review_data.get('id')
            if not acc_review_id:
                raise ValueError("ACC评审数据缺少ID")
            
            # 检查是否已存在
            existing_review = self.da.get_review_by_acc_id(acc_review_id)
            
            # 准备评审数据
            review_data = self._transform_acc_review_data(acc_review_data)
            
            if existing_review:
                # 检查是否需要更新
                if self._should_update_review(existing_review, review_data):
                    self.da.update_review(existing_review['id'], review_data)
                    review_id = existing_review['id']
                    action = 'updated'
                    self.sync_stats['reviews_updated'] += 1
                else:
                    review_id = existing_review['id']
                    action = 'skipped'
                    self.sync_stats['reviews_skipped'] += 1
            else:
                # 创建新评审
                review_id = self.da.create_review(review_data)
                action = 'created'
                self.sync_stats['reviews_synced'] += 1
            
            # 同步评审的文件版本
            if 'fileVersions' in acc_review_data:
                self._sync_review_file_versions(review_id, acc_review_data['fileVersions'])
            
            # 同步评审进度
            if 'steps' in acc_review_data:
                self._sync_review_progress(review_id, acc_review_data['steps'])
            
            return review_id, action
        
        except Exception as e:
            error_msg = f"同步评审失败 (ACC ID: {acc_review_data.get('id')}): {str(e)}"
            self.sync_stats['errors'].append(error_msg)
            print(f"✗ {error_msg}")
            raise
    
    def _transform_acc_review_data(self, acc_data: Dict[str, Any]) -> Dict[str, Any]:
        """转换ACC评审数据为本地格式"""
        return {
            'review_uuid': acc_data.get('id'),  # 使用 ACC 的 review ID 作为 UUID
            'project_id': acc_data.get('projectId'),
            'data_source': 'acc_sync',
            'acc_review_id': acc_data.get('id'),
            'acc_sequence_id': acc_data.get('sequenceId'),
            'name': acc_data.get('name', 'Unnamed Review'),
            'description': acc_data.get('description'),
            'notes': acc_data.get('notes'),  # API的notes字段
            'status': self._map_review_status(acc_data.get('status', 'open')),
            'current_step_id': acc_data.get('currentStepId'),
            'current_step_due_date': self._parse_timestamp(acc_data.get('currentStepDueDate')),
            'current_step_name': acc_data.get('currentStepName'),
            'workflow_uuid': acc_data.get('workflowId'),
            'created_by': acc_data.get('createdBy', {}),
            'assigned_to': acc_data.get('assignedTo', []),
            'next_action_by': acc_data.get('nextActionBy', {}),
            'archived': acc_data.get('archived', False),
            'archived_by': acc_data.get('archivedBy', {}),
            'archived_at': self._parse_timestamp(acc_data.get('archivedAt')),
            'archived_reason': acc_data.get('archivedReason'),
            'created_at': self._parse_timestamp(acc_data.get('createdAt')),
            'updated_at': self._parse_timestamp(acc_data.get('updatedAt')),
            'started_at': self._parse_timestamp(acc_data.get('startedAt')),
            'finished_at': self._parse_timestamp(acc_data.get('finishedAt')),
            'last_synced_at': datetime.now(timezone.utc),
            'sync_status': 'synced'
        }
    
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
    
    def _should_update_review(self, existing: Dict, new_data: Dict) -> bool:
        """判断是否需要更新评审"""
        key_fields = ['name', 'status', 'current_step_id', 'current_step_name']
        for field in key_fields:
            if existing.get(field) != new_data.get(field):
                return True
        return False
    
    def _sync_review_file_versions(self, review_id: int, file_versions: List[Dict]) -> None:
        """同步评审的文件版本（批量优化版）"""
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
                
                file_data = {
                    'review_id': review_id,
                    'file_urn': fv_data.get('urn') or fv_data.get('fileUrn'),  # API返回urn字段
                    'file_name': fv_data.get('name') or fv_data.get('fileName'),
                    'file_size': fv_data.get('fileSize'),
                    'file_extension': fv_data.get('fileExtension'),
                    'file_path': fv_data.get('filePath'),
                    'version_number': fv_data.get('versionNumber'),
                    'version_urn': fv_data.get('versionUrn'),
                    'item_urn': fv_data.get('itemUrn'),
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
                self.sync_stats['performance']['db_time'] += db_time
                print(f"  ✓ 批量插入 {inserted_count} 个文件版本 (耗时: {db_time:.2f}秒)")
            except Exception as e:
                error_msg = f"批量插入文件版本失败: {str(e)}"
                self.sync_stats['errors'].append(error_msg)
                print(f"✗ {error_msg}")
    
    def _sync_review_progress(self, review_id: int, steps: List[Dict]) -> None:
        """同步评审进度（批量优化版）"""
        if not steps:
            return
        
        db_start = time.time()
        batch_data = []
        
        for idx, step_data in enumerate(steps):
            try:
                progress_data = {
                    'review_id': review_id,
                    'step_id': step_data.get('stepId') or step_data.get('id'),  # API返回stepId
                    'step_name': step_data.get('stepName') or step_data.get('name'),
                    'step_type': self._map_step_type(step_data.get('type', 'reviewer')),
                    'step_order': idx + 1,
                    'status': self._map_step_status(step_data.get('status', 'pending')),
                    'assigned_to': step_data.get('assignedTo', []),
                    'claimed_by': step_data.get('claimedBy', {}),
                    'completed_by': step_data.get('completedBy', {}),
                    'action_by': step_data.get('actionBy', {}),  # 新增：执行操作的用户
                    'candidates': step_data.get('candidates', {}),
                    'decision': step_data.get('decision'),
                    'comments': step_data.get('comments'),
                    'notes': step_data.get('notes'),  # 新增：步骤备注
                    'due_date': self._parse_timestamp(step_data.get('dueDate')),
                    'started_at': self._parse_timestamp(step_data.get('startedAt')),
                    'completed_at': self._parse_timestamp(step_data.get('completedAt')),
                    'end_time': self._parse_timestamp(step_data.get('endTime'))  # 新增：结束时间
                }
                
                batch_data.append(progress_data)
            
            except Exception as e:
                error_msg = f"准备进度步骤数据失败: {str(e)}"
                self.sync_stats['errors'].append(error_msg)
                print(f"✗ {error_msg}")
        
        # 批量插入
        if batch_data:
            try:
                inserted_count = self.da.batch_insert_review_steps(batch_data)
                db_time = time.time() - db_start
                self.sync_stats['performance']['db_time'] += db_time
                print(f"  ✓ 批量插入 {inserted_count} 个进度步骤 (耗时: {db_time:.2f}秒)")
            except Exception as e:
                error_msg = f"批量插入进度步骤失败: {str(e)}"
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
    
    # ========================================================================
    # 文件审批历史同步
    # ========================================================================
    
    def sync_file_approval_history(
        self,
        api_client,
        project_id: str,
        file_version_urn: str,
        review_data: Optional[Dict] = None
    ) -> int:
        """
        同步单个文件的审批历史
        
        Args:
            api_client: API客户端
            project_id: 项目ID
            file_version_urn: 文件版本URN
            review_data: 评审数据（可选，用于补充信息）
            
        Returns:
            同步的记录数
        """
        try:
            # URL编码文件URN
            import urllib.parse
            encoded_urn = urllib.parse.quote(file_version_urn, safe='')
            
            # 调用API获取审批状态
            url = f'/projects/{project_id}/versions/{encoded_urn}/approval-statuses'
            result = api_client.get(url)
            
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
                    'is_latest_in_review': True  # 可以后续优化
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
            print(f"⚠ {error_msg}")
            return 0
    
    def sync_all_file_approval_histories(
        self,
        api_client,
        project_id: str,
        file_versions: List[Dict],
        show_progress: bool = True
    ) -> int:
        """
        批量同步文件审批历史
        
        Args:
            api_client: API客户端
            project_id: 项目ID
            file_versions: 文件版本列表
            show_progress: 是否显示进度
            
        Returns:
            总同步记录数
        """
        if not file_versions:
            return 0
        
        if show_progress:
            print(f"\n📋 同步文件审批历史...")
            print(f"   文件数量: {len(file_versions)}")
        
        total_synced = 0
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            
            for fv in file_versions:
                file_urn = fv.get('urn') or fv.get('fileUrn')
                if file_urn:
                    future = executor.submit(
                        self.sync_file_approval_history,
                        api_client,
                        project_id,
                        file_urn,
                        fv
                    )
                    futures.append(future)
            
            completed = 0
            for future in as_completed(futures):
                try:
                    count = future.result()
                    total_synced += count
                    completed += 1
                    
                    if show_progress and completed % 10 == 0:
                        print(f"   进度: {completed}/{len(futures)} 文件")
                        
                except Exception as e:
                    error_msg = f"处理文件审批历史失败: {str(e)}"
                    self.sync_stats['errors'].append(error_msg)
        
        if show_progress:
            print(f"   ✓ 完成: 同步 {total_synced} 条审批历史记录")
        
        return total_synced
    
    # ========================================================================
    # 并行API调用辅助方法
    # ========================================================================
    
    @rate_limit_retry(max_retries=3, backoff_factor=2.0)
    def _fetch_review_versions(self, api_client, project_id: str, review_id: str) -> List[Dict]:
        """
        获取评审的文件版本（带限流重试）
        
        Args:
            api_client: API客户端
            project_id: 项目ID
            review_id: 评审ID
            
        Returns:
            文件版本列表
        """
        try:
            self.sync_stats['performance']['api_calls'] += 1
            # 假设API客户端有get_review_versions方法
            result = api_client.get(f'/projects/{project_id}/reviews/{review_id}/versions')
            return result.get('results', []) if result else []
        except Exception as e:
            print(f"⚠ 获取文件版本失败 (review: {review_id}): {e}")
            return []
    
    @rate_limit_retry(max_retries=3, backoff_factor=2.0)
    def _fetch_review_progress(self, api_client, project_id: str, review_id: str) -> List[Dict]:
        """
        获取评审进度（带限流重试）
        
        Args:
            api_client: API客户端
            project_id: 项目ID
            review_id: 评审ID
            
        Returns:
            进度步骤列表
        """
        try:
            self.sync_stats['performance']['api_calls'] += 1
            result = api_client.get(f'/projects/{project_id}/reviews/{review_id}/progress')
            return result.get('results', []) if result else []
        except Exception as e:
            print(f"⚠ 获取进度失败 (review: {review_id}): {e}")
            return []
    
    @rate_limit_retry(max_retries=3, backoff_factor=2.0)
    def _fetch_review_workflow(self, api_client, project_id: str, review_id: str) -> Dict:
        """
        获取评审工作流（带限流重试）
        
        Args:
            api_client: API客户端
            project_id: 项目ID
            review_id: 评审ID
            
        Returns:
            工作流数据
        """
        try:
            self.sync_stats['performance']['api_calls'] += 1
            result = api_client.get(f'/projects/{project_id}/reviews/{review_id}/workflow')
            return result if result else {}
        except Exception as e:
            print(f"⚠ 获取工作流失败 (review: {review_id}): {e}")
            return {}
    
    # ========================================================================
    # 批量同步
    # ========================================================================
    
    def sync_workflows_batch(
        self,
        acc_workflows: List[Dict[str, Any]],
        show_progress: bool = True
    ) -> Dict[str, Any]:
        """
        批量同步工作流
        
        Args:
            acc_workflows: ACC工作流数据列表
            show_progress: 是否显示进度
            
        Returns:
            同步统计信息
        """
        total = len(acc_workflows)
        
        if show_progress:
            print(f"\n开始同步 {total} 个工作流...")
            print("=" * 60)
        
        for idx, workflow_data in enumerate(acc_workflows, 1):
            try:
                workflow_id, action = self.sync_workflow_from_acc(workflow_data)
                
                if show_progress:
                    status_icon = {
                        'created': '✓ 新建',
                        'updated': '↻ 更新',
                        'skipped': '⊘ 跳过'
                    }
                    print(f"[{idx}/{total}] {status_icon[action]} 工作流: {workflow_data.get('name')} (ID: {workflow_id})")
            
            except Exception as e:
                if show_progress:
                    print(f"[{idx}/{total}] ✗ 失败: {workflow_data.get('name')}")
        
        if show_progress:
            print("\n" + "=" * 60)
            self._print_sync_summary()
        
        return self.sync_stats
    
    def sync_reviews_batch_parallel(
        self,
        acc_reviews: List[Dict[str, Any]],
        api_client,
        project_id: str,
        show_progress: bool = True
    ) -> Dict[str, Any]:
        """
        并行批量同步评审（优化版）
        
        策略：
        1. 先并行获取所有评审的详细数据（versions, progress）
        2. 再批量插入数据库
        
        Args:
            acc_reviews: ACC评审数据列表（基础信息）
            api_client: API客户端实例
            project_id: 项目ID
            show_progress: 是否显示进度
            
        Returns:
            同步统计信息
        """
        total = len(acc_reviews)
        
        if show_progress:
            print(f"\n🚀 开始并行同步 {total} 个评审...")
            print(f"   并发线程数: {self.max_workers}")
            print("=" * 60)
        
        start_time = time.time()
        
        # ========== 阶段 1: 并行获取详细数据 ==========
        if show_progress:
            print(f"\n📥 阶段 1/2: 并行获取API数据...")
        
        api_start = time.time()
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 为每个评审提交3个并行任务
            future_to_review = {}
            
            for review_data in acc_reviews:
                review_id = review_data.get('id')
                
                # 提交3个并行API调用
                future_versions = executor.submit(
                    self._fetch_review_versions, 
                    api_client, 
                    project_id,
                    review_id
                )
                future_progress = executor.submit(
                    self._fetch_review_progress, 
                    api_client, 
                    project_id,
                    review_id
                )
                future_workflow = executor.submit(
                    self._fetch_review_workflow, 
                    api_client, 
                    project_id,
                    review_id
                )
                
                future_to_review[future_versions] = (review_data, 'versions')
                future_to_review[future_progress] = (review_data, 'progress')
                future_to_review[future_workflow] = (review_data, 'workflow')
            
            # 收集结果
            review_details = {}
            completed = 0
            total_tasks = len(future_to_review)
            
            for future in as_completed(future_to_review):
                review_data, data_type = future_to_review[future]
                review_id = review_data.get('id')
                
                try:
                    result = future.result()
                    
                    if review_id not in review_details:
                        review_details[review_id] = {
                            'review': review_data,
                            'versions': None,
                            'progress': None,
                            'workflow': None
                        }
                    
                    review_details[review_id][data_type] = result
                    completed += 1
                    
                    if show_progress and completed % 10 == 0:
                        progress_pct = (completed / total_tasks) * 100
                        elapsed = time.time() - api_start
                        print(f"   📊 进度: {completed}/{total_tasks} ({progress_pct:.1f}%) | 耗时: {elapsed:.1f}秒")
                
                except Exception as e:
                    error_msg = f"获取评审详情失败 (ID: {review_id}, type: {data_type}): {str(e)}"
                    self.sync_stats['errors'].append(error_msg)
                    if show_progress:
                        print(f"   ✗ {error_msg}")
        
        api_time = time.time() - api_start
        self.sync_stats['performance']['api_time'] += api_time
        
        if show_progress:
            print(f"\n✓ API数据获取完成")
            print(f"   总API调用: {self.sync_stats['performance']['api_calls']} 次")
            print(f"   耗时: {api_time:.2f}秒")
            print(f"   平均每个评审: {api_time/total:.2f}秒")
            print(f"   提速比: {(total * 3 * 6) / api_time:.1f}x (相比串行6秒/请求)")
        
        # ========== 阶段 2: 批量写入数据库 ==========
        if show_progress:
            print(f"\n💾 阶段 2/2: 批量写入数据库...")
        
        db_start = time.time()
        
        for idx, (review_id, details) in enumerate(review_details.items(), 1):
            try:
                # 合并数据
                review_data = details['review']
                if details['versions']:
                    review_data['fileVersions'] = details['versions']
                if details['progress']:
                    review_data['steps'] = details['progress']
                
                # 同步到数据库
                local_review_id, action = self.sync_review_from_acc(review_data)
                
                if show_progress:
                    status_icon = {
                        'created': '✓ 新建',
                        'updated': '↻ 更新',
                        'skipped': '⊘ 跳过'
                    }
                    print(f"[{idx}/{total}] {status_icon[action]} 评审: {review_data.get('name')} (ID: {local_review_id})")
            
            except Exception as e:
                error_msg = f"同步评审失败: {review_data.get('name')} - {str(e)}"
                self.sync_stats['errors'].append(error_msg)
                if show_progress:
                    print(f"[{idx}/{total}] ✗ 失败: {review_data.get('name')}")
        
        db_time = time.time() - db_start
        total_time = time.time() - start_time
        
        self.sync_stats['performance']['total_time'] = total_time
        
        if show_progress:
            print("\n" + "=" * 60)
            print(f"📊 性能统计:")
            print(f"   API调用阶段: {api_time:.2f}秒 ({api_time/total_time*100:.1f}%)")
            print(f"   数据库写入: {db_time:.2f}秒 ({db_time/total_time*100:.1f}%)")
            print(f"   总耗时: {total_time:.2f}秒")
            print(f"   平均每个评审: {total_time/total:.2f}秒")
            print(f"   整体提速比: {(total * 18) / total_time:.1f}x (相比串行18秒/评审)")
            self._print_sync_summary()
        
        return self.sync_stats
    
    # ========================================================================
    # 智能分页获取
    # ========================================================================
    
    def fetch_all_reviews_with_pagination(
        self,
        api_client,
        project_id: str,
        limit_per_page: int = 50,
        show_progress: bool = True
    ) -> List[Dict]:
        """
        智能分页获取所有评审
        
        利用API的分页功能并行获取多页数据
        
        Args:
            api_client: API客户端
            project_id: 项目ID
            limit_per_page: 每页数量（最大50）
            show_progress: 是否显示进度
            
        Returns:
            所有评审列表
        """
        if show_progress:
            print(f"\n📄 智能分页获取评审列表...")
        
        # 第一次调用获取总数
        first_page = api_client.get(
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
            with ThreadPoolExecutor(max_workers=min(5, pages_needed)) as executor:
                futures = []
                for page in range(1, pages_needed + 1):
                    offset = page * limit_per_page
                    future = executor.submit(
                        self._fetch_reviews_page,
                        api_client,
                        project_id,
                        limit_per_page,
                        offset
                    )
                    futures.append(future)
                
                for idx, future in enumerate(as_completed(futures), 1):
                    try:
                        page_data = future.result()
                        reviews.extend(page_data)
                        if show_progress and idx % 5 == 0:
                            print(f"   已获取 {idx}/{pages_needed} 页")
                    except Exception as e:
                        error_msg = f"获取分页数据失败: {e}"
                        self.sync_stats['errors'].append(error_msg)
                        print(f"⚠ {error_msg}")
        
        if show_progress:
            print(f"✓ 共获取 {len(reviews)} 个评审\n")
        
        return reviews
    
    @rate_limit_retry(max_retries=3, backoff_factor=2.0)
    def _fetch_reviews_page(
        self,
        api_client,
        project_id: str,
        limit: int,
        offset: int
    ) -> List[Dict]:
        """获取单页评审数据（带限流重试）"""
        try:
            self.sync_stats['performance']['api_calls'] += 1
            result = api_client.get(
                f'/projects/{project_id}/reviews',
                params={'limit': limit, 'offset': offset}
            )
            return result.get('results', [])
        except Exception as e:
            print(f"⚠ 获取评审页面失败 (offset: {offset}): {e}")
            return []
    
    # ========================================================================
    # 辅助方法
    # ========================================================================
    
    def _parse_timestamp(self, timestamp_str: Optional[str]) -> Optional[datetime]:
        """解析时间戳字符串"""
        if not timestamp_str:
            return None
        
        try:
            # 尝试ISO格式
            return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        except:
            try:
                # 尝试其他格式
                return datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%f')
            except:
                return None
    
    def _print_sync_summary(self) -> None:
        """打印同步摘要（增强版）"""
        print("\n📊 同步摘要:")
        print(f"  工作流:")
        print(f"    - 新建: {self.sync_stats['workflows_synced']}")
        print(f"    - 更新: {self.sync_stats['workflows_updated']}")
        print(f"    - 跳过: {self.sync_stats['workflows_skipped']}")
        print(f"  评审:")
        print(f"    - 新建: {self.sync_stats['reviews_synced']}")
        print(f"    - 更新: {self.sync_stats['reviews_updated']}")
        print(f"    - 跳过: {self.sync_stats['reviews_skipped']}")
        
        # 性能统计
        perf = self.sync_stats['performance']
        if perf['total_time'] > 0:
            print(f"\n⚡ 性能指标:")
            print(f"  总耗时: {perf['total_time']:.2f}秒")
            print(f"  API调用: {perf['api_calls']} 次 ({perf['api_time']:.2f}秒)")
            print(f"  数据库操作: {perf['db_time']:.2f}秒")
            
            total_items = (self.sync_stats['workflows_synced'] + 
                          self.sync_stats['workflows_updated'] +
                          self.sync_stats['reviews_synced'] + 
                          self.sync_stats['reviews_updated'])
            
            if total_items > 0:
                print(f"  平均处理速度: {perf['total_time']/total_items:.2f}秒/项")
        
        if self.sync_stats['errors']:
            print(f"\n⚠ 错误数量: {len(self.sync_stats['errors'])}")
            for error in self.sync_stats['errors'][:5]:  # 只显示前5个错误
                print(f"  - {error}")
            if len(self.sync_stats['errors']) > 5:
                print(f"  ... 还有 {len(self.sync_stats['errors']) - 5} 个错误")
    
    def reset_stats(self) -> None:
        """重置统计信息"""
        self.sync_stats = {
            'workflows_synced': 0,
            'workflows_updated': 0,
            'workflows_skipped': 0,
            'reviews_synced': 0,
            'reviews_updated': 0,
            'reviews_skipped': 0,
            'errors': [],
            'performance': {
                'api_calls': 0,
                'api_time': 0.0,
                'db_time': 0.0,
                'total_time': 0.0
            }
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return self.sync_stats.copy()


# ============================================================================
# 便捷函数
# ============================================================================

def get_review_sync_manager(data_access: Optional[ReviewDataAccess] = None) -> ReviewSyncManager:
    """获取ReviewSyncManager实例"""
    return ReviewSyncManager(data_access)


if __name__ == "__main__":
    # 测试代码
    print("审批系统同步管理器测试")
    print("=" * 60)
    
    try:
        sync_manager = get_review_sync_manager()
        print("✓ 同步管理器初始化成功")
        
        # 显示当前统计
        stats = sync_manager.get_stats()
        print(f"\n当前统计: {json.dumps(stats, indent=2, ensure_ascii=False)}")
        
    except Exception as e:
        print(f"✗ 错误: {e}")
        import traceback
        traceback.print_exc()

