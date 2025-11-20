"""
审批系统同步管理器
负责从ACC同步工作流和评审数据到本地数据库
支持全量同步和增量同步
"""

import sys
import os
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timezone
import uuid
import json

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from review_data_access import ReviewDataAccess
from neon_config import get_connection


class ReviewSyncManager:
    """审批系统同步管理器"""
    
    def __init__(self, data_access: Optional[ReviewDataAccess] = None):
        """
        初始化同步管理器
        
        Args:
            data_access: 数据访问层实例，如果为None则创建新实例
        """
        self.da = data_access or ReviewDataAccess()
        self.sync_stats = {
            'workflows_synced': 0,
            'workflows_updated': 0,
            'workflows_skipped': 0,
            'reviews_synced': 0,
            'reviews_updated': 0,
            'reviews_skipped': 0,
            'comments_synced': 0,
            'errors': []
        }
    
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
            'workflow_uuid': str(uuid.uuid4()),
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
            'review_uuid': str(uuid.uuid4()),
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
        """同步评审的文件版本"""
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
                
                # 检查是否已存在
                existing_files = self.da.get_review_files(review_id)
                existing_file = next(
                    (f for f in existing_files if f['file_urn'] == file_data['file_urn']),
                    None
                )
                
                if not existing_file:
                    self.da.add_file_to_review(file_data)
            
            except Exception as e:
                print(f"✗ 同步文件版本失败: {str(e)}")
    
    def _sync_review_progress(self, review_id: int, steps: List[Dict]) -> None:
        """同步评审进度"""
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
                
                # 检查是否已存在
                existing_progress = self.da.get_review_progress(review_id)
                existing_step = next(
                    (s for s in existing_progress if s['step_id'] == progress_data['step_id']),
                    None
                )
                
                if not existing_step:
                    self.da.add_review_step(progress_data)
            
            except Exception as e:
                print(f"✗ 同步进度步骤失败: {str(e)}")
    
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
    # 评论同步
    # ========================================================================
    
    def sync_comments_from_acc(
        self,
        review_id: int,
        acc_comments: List[Dict[str, Any]]
    ) -> int:
        """
        同步评审评论
        
        Args:
            review_id: 本地评审ID
            acc_comments: ACC评论数据列表
            
        Returns:
            同步的评论数量
        """
        synced_count = 0
        
        for comment_data in acc_comments:
            try:
                comment = {
                    'review_id': review_id,
                    'content': comment_data.get('content', ''),
                    'comment_type': comment_data.get('type', 'general'),
                    'author': comment_data.get('author', {}),
                    'status': comment_data.get('status', 'active'),
                    'is_private': comment_data.get('isPrivate', False),
                    'markup_data': comment_data.get('markupData', {}),
                    'page_number': comment_data.get('pageNumber'),
                    'coordinates': comment_data.get('coordinates', {}),
                    'attachments': comment_data.get('attachments', []),
                    'created_at': self._parse_timestamp(comment_data.get('createdAt')),
                    'updated_at': self._parse_timestamp(comment_data.get('updatedAt'))
                }
                
                self.da.add_comment(comment)
                synced_count += 1
                self.sync_stats['comments_synced'] += 1
            
            except Exception as e:
                print(f"✗ 同步评论失败: {str(e)}")
        
        return synced_count
    
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
    
    def sync_reviews_batch(
        self,
        acc_reviews: List[Dict[str, Any]],
        show_progress: bool = True
    ) -> Dict[str, Any]:
        """
        批量同步评审
        
        Args:
            acc_reviews: ACC评审数据列表
            show_progress: 是否显示进度
            
        Returns:
            同步统计信息
        """
        total = len(acc_reviews)
        
        if show_progress:
            print(f"\n开始同步 {total} 个评审...")
            print("=" * 60)
        
        for idx, review_data in enumerate(acc_reviews, 1):
            try:
                review_id, action = self.sync_review_from_acc(review_data)
                
                if show_progress:
                    status_icon = {
                        'created': '✓ 新建',
                        'updated': '↻ 更新',
                        'skipped': '⊘ 跳过'
                    }
                    print(f"[{idx}/{total}] {status_icon[action]} 评审: {review_data.get('name')} (ID: {review_id})")
            
            except Exception as e:
                if show_progress:
                    print(f"[{idx}/{total}] ✗ 失败: {review_data.get('name')}")
        
        if show_progress:
            print("\n" + "=" * 60)
            self._print_sync_summary()
        
        return self.sync_stats
    
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
        """打印同步摘要"""
        print("\n📊 同步摘要:")
        print(f"  工作流:")
        print(f"    - 新建: {self.sync_stats['workflows_synced']}")
        print(f"    - 更新: {self.sync_stats['workflows_updated']}")
        print(f"    - 跳过: {self.sync_stats['workflows_skipped']}")
        print(f"  评审:")
        print(f"    - 新建: {self.sync_stats['reviews_synced']}")
        print(f"    - 更新: {self.sync_stats['reviews_updated']}")
        print(f"    - 跳过: {self.sync_stats['reviews_skipped']}")
        print(f"  评论: {self.sync_stats['comments_synced']}")
        
        if self.sync_stats['errors']:
            print(f"\n⚠ 错误数量: {len(self.sync_stats['errors'])}")
            for error in self.sync_stats['errors'][:5]:  # 只显示前5个错误
                print(f"  - {error}")
    
    def reset_stats(self) -> None:
        """重置统计信息"""
        self.sync_stats = {
            'workflows_synced': 0,
            'workflows_updated': 0,
            'workflows_skipped': 0,
            'reviews_synced': 0,
            'reviews_updated': 0,
            'reviews_skipped': 0,
            'comments_synced': 0,
            'errors': []
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

