# -*- coding: utf-8 -*-
"""
Enhanced CDE Document Approval Workflow API
Optimized version with comprehensive permissions, error handling, and logging

重要概念说明：
1. review_step_candidates: 从 workflow 定义创建，存储每个步骤的候选审批人配置（静态配置）
2. review_progress: 记录用户实际执行步骤的历史记录（动态记录，每次审批动作都会更新）

数据流程：
workflow.steps -> review_step_candidates (创建时配置) -> review_progress (执行时记录)
"""

import json
import psycopg2
import psycopg2.extras
from psycopg2.extras import Json
from flask import Blueprint, request, jsonify
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timezone
import sys
import os
import logging
import traceback
from functools import wraps

# Add database access path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../database_sql'))

try:
    from review_data_access_enhanced import EnhancedReviewDataAccess
except ImportError:
    try:
        from neon_config import NeonConfig
    except ImportError:
        from database_access import DatabaseAccess as EnhancedReviewDataAccess

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
approval_bp = Blueprint('approval_workflow_enhanced', __name__)

def handle_exceptions(f):
    """Decorator for comprehensive exception handling"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except psycopg2.Error as e:
            logger.error(f"Database error in {f.__name__}: {str(e)}")
            return {
                'success': False,
                'error': f'Database operation failed: {str(e)}',
                'error_type': 'database_error',
                'data': None
            }
        except ValueError as e:
            logger.error(f"Validation error in {f.__name__}: {str(e)}")
            return {
                'success': False,
                'error': f'Invalid input: {str(e)}',
                'error_type': 'validation_error',
                'data': None
            }
        except Exception as e:
            logger.error(f"Unexpected error in {f.__name__}: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return {
                'success': False,
                'error': f'Internal server error: {str(e)}',
                'error_type': 'internal_error',
                'data': None
            }
    return decorated_function

class EnhancedApprovalWorkflowManager:
    """Enhanced approval workflow manager with comprehensive features"""
    
    def __init__(self):
        try:
            self.da = EnhancedReviewDataAccess()
        except:
            # Fallback to NeonConfig if available
            try:
                from neon_config import NeonConfig
                self.neon_config = NeonConfig()
            except ImportError:
                logger.warning("No database configuration found, using environment variables")
                self.neon_config = None
    
    def get_connection(self):
        """Get database connection with fallback options"""
        try:
            if hasattr(self, 'da'):
                return self.da.get_connection()
            elif hasattr(self, 'neon_config') and self.neon_config:
                return psycopg2.connect(**self.neon_config.get_db_params())
            else:
                # Environment variable fallback
                return psycopg2.connect(
                    host=os.getenv('DB_HOST', 'localhost'),
                    port=os.getenv('DB_PORT', 5432),
                    database=os.getenv('DB_NAME', 'neondb'),
                    user=os.getenv('DB_USER', 'neondb_owner'),
                    password=os.getenv('DB_PASSWORD', ''),
                    sslmode=os.getenv('DB_SSL', 'require')
                )
        except Exception as e:
            logger.error(f"Failed to get database connection: {str(e)}")
            raise
    
    # ========================================================================
    # Enhanced Permission System
    # ========================================================================
    
    def _check_comprehensive_permissions(self, user_id: str, candidates: Dict, 
                                       project_id: str = None) -> Tuple[bool, str]:
        """
        Enhanced permission checking including users, roles, and companies
        
        Args:
            user_id: User ID (autodeskId)
            candidates: Candidates configuration
            project_id: Project ID for additional validation
            
        Returns:
            Tuple of (has_permission, reason)
        """
        if not candidates or not isinstance(candidates, dict):
            return False, "No candidates configuration found"
        
        # Check direct user assignment
        users = candidates.get('users', [])
        for user in users:
            if isinstance(user, dict) and user.get('autodeskId') == user_id:
                return True, "Direct user assignment"
        
        # Check role-based permissions
        roles = candidates.get('roles', [])
        if roles and project_id:
            user_roles = self._get_user_roles(user_id, project_id)
            for role in roles:
                role_id = role.get('id') if isinstance(role, dict) else role
                if role_id in user_roles:
                    return True, f"Role-based permission: {role_id}"
        
        # Check company-based permissions
        companies = candidates.get('companies', [])
        if companies and project_id:
            user_company = self._get_user_company(user_id, project_id)
            for company in companies:
                company_id = company.get('autodeskId') if isinstance(company, dict) else company
                if company_id == user_company:
                    return True, f"Company-based permission: {company_id}"
        
        return False, "User not found in any candidate list (users, roles, or companies)"
    
    def _get_user_roles(self, user_id: str, project_id: str) -> List[str]:
        """Get user roles in project"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT DISTINCT role_id 
                FROM project_user_roles 
                WHERE user_id = %s AND project_id = %s
            """, [user_id, project_id])
            
            roles = [row[0] for row in cursor.fetchall()]
            cursor.close()
            conn.close()
            return roles
            
        except Exception as e:
            logger.warning(f"Could not fetch user roles: {str(e)}")
            return []
    
    def _get_user_company(self, user_id: str, project_id: str) -> Optional[str]:
        """Get user company in project"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT company_id 
                FROM project_users 
                WHERE user_id = %s AND project_id = %s
                LIMIT 1
            """, [user_id, project_id])
            
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result[0] if result else None
            
        except Exception as e:
            logger.warning(f"Could not fetch user company: {str(e)}")
            return None
    
    # ========================================================================
    # Enhanced Core Approval Functions
    # ========================================================================
    
    @handle_exceptions
    def get_pending_approvals(self, user_id: str, project_id: str = None, 
                            filters: Dict = None) -> Dict[str, Any]:
        """
        Enhanced method to get user's pending approvals with filtering
        
        Args:
            user_id: User ID (autodeskId)
            project_id: Project ID (optional)
            filters: Additional filters (priority, department, etc.)
            
        Returns:
            Pending approvals with enhanced metadata
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # Build dynamic query with filters
            base_query = """
                SELECT 
                    r.id as review_id,
                    r.name as review_name,
                    r.status as review_status,
                    r.current_step_id,
                    r.current_step_name,
                    r.current_step_due_date,
                    r.created_at as review_created_at,
                    r.project_id,
                    r.priority,
                    r.department,
                    r.category,
                    
                    -- Current step information
                    rp.step_name,
                    rp.step_type,
                    rp.step_order,
                    rp.status as step_status,
                    rp.due_date as step_due_date,
                    
                    -- Candidates configuration
                    rsc.candidates,
                    rsc.source as candidates_source,
                    
                    -- File statistics
                    COUNT(rfv.id) as total_files,
                    COUNT(CASE WHEN rfv.approval_status = 'PENDING' THEN 1 END) as pending_files,
                    COUNT(CASE WHEN rfv.approval_status = 'APPROVED' THEN 1 END) as approved_files,
                    COUNT(CASE WHEN rfv.approval_status = 'REJECTED' THEN 1 END) as rejected_files,
                    
                    -- Urgency calculation
                    CASE 
                        WHEN r.current_step_due_date < CURRENT_TIMESTAMP THEN 'overdue'
                        WHEN r.current_step_due_date < CURRENT_TIMESTAMP + INTERVAL '1 day' THEN 'urgent'
                        WHEN r.current_step_due_date < CURRENT_TIMESTAMP + INTERVAL '3 days' THEN 'soon'
                        ELSE 'normal'
                    END as urgency_level
                    
                FROM reviews r
                JOIN review_progress rp ON r.id = rp.review_id AND r.current_step_id = rp.step_id
                JOIN review_step_candidates rsc ON r.id = rsc.review_id AND r.current_step_id = rsc.step_id
                LEFT JOIN review_file_versions rfv ON r.id = rfv.review_id
                
                WHERE r.status IN ('OPEN')
                AND rp.status IN ('PENDING', 'CLAIMED')
                AND rsc.is_active = true
            """
            
            params = []
            
            # Add user permission check
            base_query += """
                AND (
                    rsc.candidates::jsonb -> 'users' @> %s::jsonb
                    OR EXISTS (
                        SELECT 1 FROM jsonb_array_elements(rsc.candidates::jsonb -> 'users') as user_obj
                        WHERE user_obj ->> 'autodeskId' = %s
                    )
                )
            """
            params.extend([json.dumps([{"autodeskId": user_id}]), user_id])
            
            # Add project filter
            if project_id:
                base_query += " AND r.project_id = %s"
                params.append(project_id)
            
            # Add additional filters
            if filters:
                if filters.get('priority'):
                    base_query += " AND r.priority = %s"
                    params.append(filters['priority'])
                
                if filters.get('department'):
                    base_query += " AND r.department = %s"
                    params.append(filters['department'])
                
                if filters.get('urgency_level'):
                    urgency_filter = filters['urgency_level']
                    if urgency_filter == 'overdue':
                        base_query += " AND r.current_step_due_date < CURRENT_TIMESTAMP"
                    elif urgency_filter == 'urgent':
                        base_query += " AND r.current_step_due_date < CURRENT_TIMESTAMP + INTERVAL '1 day'"
            
            # Add grouping and ordering
            base_query += """
                GROUP BY r.id, r.name, r.status, r.current_step_id, r.current_step_name, 
                         r.current_step_due_date, r.created_at, r.project_id, r.priority,
                         r.department, r.category, rp.step_name, rp.step_type, rp.step_order, 
                         rp.status, rp.due_date, rsc.candidates, rsc.source
                ORDER BY 
                    CASE 
                        WHEN r.current_step_due_date < CURRENT_TIMESTAMP THEN 0
                        ELSE 1 
                    END,
                    r.priority ASC,
                    r.current_step_due_date ASC NULLS LAST,
                    r.created_at DESC
            """
            
            cursor.execute(base_query, params)
            results = cursor.fetchall()
            
            pending_reviews = []
            for result in results:
                # Verify permissions for each review
                has_permission, permission_reason = self._check_comprehensive_permissions(
                    user_id, result['candidates'], result['project_id']
                )
                
                if has_permission:
                    pending_reviews.append({
                        'review_id': result['review_id'],
                        'review_name': result['review_name'],
                        'review_status': result['review_status'],
                        'project_id': result['project_id'],
                        'priority': result['priority'],
                        'department': result['department'],
                        'category': result['category'],
                        'urgency_level': result['urgency_level'],
                        'permission_reason': permission_reason,
                        'current_step': {
                            'step_id': result['current_step_id'],
                            'step_name': result['step_name'],
                            'step_type': result['step_type'],
                            'step_order': result['step_order'],
                            'status': result['step_status'],
                            'due_date': result['step_due_date'].isoformat() if result['step_due_date'] else None
                        },
                        'files_summary': {
                            'total': result['total_files'],
                            'pending': result['pending_files'],
                            'approved': result['approved_files'],
                            'rejected': result['rejected_files'],
                            'completion_rate': round(
                                (result['approved_files'] + result['rejected_files']) / max(result['total_files'], 1) * 100, 1
                            )
                        },
                        'candidates_source': result['candidates_source'],
                        'created_at': result['review_created_at'].isoformat() if result['review_created_at'] else None
                    })
            
            # Calculate summary statistics
            total_pending = len(pending_reviews)
            overdue_count = sum(1 for r in pending_reviews if r['urgency_level'] == 'overdue')
            urgent_count = sum(1 for r in pending_reviews if r['urgency_level'] == 'urgent')
            
            return {
                'success': True,
                'data': {
                    'user_id': user_id,
                    'project_id': project_id,
                    'filters_applied': filters or {},
                    'summary': {
                        'total_pending': total_pending,
                        'overdue': overdue_count,
                        'urgent': urgent_count,
                        'normal': total_pending - overdue_count - urgent_count
                    },
                    'reviews': pending_reviews
                },
                'metadata': {
                    'query_timestamp': datetime.now(timezone.utc).isoformat(),
                    'permission_check': 'comprehensive'
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting pending approvals: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    
    @handle_exceptions
    def get_review_details_for_approval(self, review_id: int, user_id: str) -> Dict[str, Any]:
        """
        Enhanced method to get review details with comprehensive permission checking
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # Get review basic information
            cursor.execute("""
                SELECT 
                    r.*,
                    w.name as workflow_name,
                    w.steps as workflow_steps
                FROM reviews r
                LEFT JOIN workflows w ON r.workflow_id = w.id
                WHERE r.id = %s
            """, [review_id])
            
            review = cursor.fetchone()
            if not review:
                return {
                    'success': False,
                    'error': 'Review not found',
                    'error_type': 'not_found',
                    'data': None
                }
            
            # Get current step information with candidates
            # 方案2實現：使用 template_step_id 匹配，fallback 使用 step_order
            cursor.execute("""
                SELECT
                    rsc.step_id,
                    rsc.step_name,
                    rsc.step_type,
                    rsc.step_order,
                    COALESCE(rp.status, 'PENDING') as status,
                    rp.assigned_to,
                    rp.claimed_by,
                    rp.completed_by,
                    rp.started_at,
                    rp.completed_at,
                    rp.due_date,
                    rp.decision,
                    rp.comments,
                    rsc.candidates,
                    rsc.source as candidates_source
                FROM review_step_candidates rsc
                LEFT JOIN review_progress rp
                    ON rp.review_id = rsc.review_id
                    AND (
                        rp.template_step_id = rsc.step_id  -- ✅ 優先使用 template_step_id
                        OR rp.step_order = rsc.step_order   -- ✅ Fallback 使用 step_order
                    )
                WHERE rsc.review_id = %s AND rsc.step_order = %s AND rsc.is_active = true
            """, [review_id, review['current_step_number']])

            current_step = cursor.fetchone()

            # Enhanced permission verification
            can_approve = False
            permission_details = {}

            if current_step:
                can_approve, permission_reason = self._check_comprehensive_permissions(
                    user_id, current_step['candidates'], review['project_id']
                )
                permission_details = {
                    'can_approve': can_approve,
                    'reason': permission_reason,
                    'candidates': current_step['candidates']
                }
            
            # Get files with enhanced metadata
            cursor.execute("""
                SELECT 
                    rfv.id, 
                    rfv.file_version_urn,
                    rfv.approval_status, 
                    rfv.approval_comments,
                    rfv.created_at, 
                    rfv.updated_at, 
                    rfv.approved_at,
                    rfv.local_file_path, 
                    rfv.thumbnail_url,
                    -- Get file details from file_versions table
                    fv.file_size,
                    fv.mime_type as file_extension,
                    fv.version_number,
                    -- Extract file name from file_id or use a default
                    COALESCE(f.name, 'Unknown File') as file_name
                FROM review_file_versions rfv
                LEFT JOIN file_versions fv ON rfv.file_version_urn = fv.urn
                LEFT JOIN files f ON fv.file_id = f.id
                WHERE rfv.review_id = %s
                ORDER BY file_name, version_number DESC
            """, [review_id])
            
            files = cursor.fetchall()
            
            # Get approval history with enhanced details
            cursor.execute("""
                SELECT 
                    step_id, step_name, step_type, step_order, status,
                    assigned_to, claimed_by, completed_by, action_by,
                    decision, comments, notes,
                    started_at, completed_at, end_time,
                    due_date,
                    CASE 
                        WHEN completed_at IS NOT NULL AND due_date IS NOT NULL THEN
                            EXTRACT(EPOCH FROM (completed_at - due_date)) / 3600
                        ELSE NULL
                    END as hours_vs_deadline
                FROM review_progress
                WHERE review_id = %s
                ORDER BY step_order ASC
            """, [review_id])
            
            approval_history = cursor.fetchall()
            
            # Get comments for current step
            cursor.execute("""
                SELECT local_comments
                FROM review_progress
                WHERE review_id = %s AND step_id = %s
            """, [review_id, review['current_step_id']])
            
            comments_result = cursor.fetchone()
            step_comments = []
            if comments_result and comments_result['local_comments']:
                try:
                    step_comments = json.loads(comments_result['local_comments'])
                except:
                    step_comments = []

            # Get workflow's approval_status_options
            approval_status_options = self._get_workflow_approval_status_options(review['workflow_id'], cursor)

            # Parse workflow steps for due date calculation
            workflow_steps = []
            if review.get('workflow_steps'):
                try:
                    workflow_steps = json.loads(review['workflow_steps']) if isinstance(review['workflow_steps'], str) else review['workflow_steps']
                except:
                    workflow_steps = []

            return {
                'success': True,
                'data': {
                    'review': {
                        'id': review['id'],
                        'name': review['name'],
                        'description': review['description'],
                        'status': review['status'],
                        'project_id': review['project_id'],
                        'workflow_id': review['workflow_id'],
                        'workflow_name': review['workflow_name'],
                        'priority': review['priority'],
                        'department': review['department'],
                        'category': review['category'],
                        'created_at': review['created_at'].isoformat() if review['created_at'] else None,
                        'current_step_id': review['current_step_id'],
                        'current_step_name': review['current_step_name'],
                        'current_step_due_date': review['current_step_due_date'].isoformat() if review['current_step_due_date'] else None,
                        'progress_percentage': float(review['progress_percentage']) if review['progress_percentage'] else 0.0
                    },
                    'workflow': {
                        'id': review['workflow_id'],
                        'name': review['workflow_name'],
                        'steps': workflow_steps
                    },
                    'current_step': dict(current_step) if current_step else None,
                    'permission_details': permission_details,
                    'files': [dict(file) for file in files],
                    'approval_history': [dict(step) for step in approval_history],
                    'step_comments': step_comments,
                    'approval_status_options': approval_status_options
                },
                'metadata': {
                    'user_id': user_id,
                    'access_timestamp': datetime.now(timezone.utc).isoformat(),
                    'permission_check': 'comprehensive'
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting review details: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    
    @handle_exceptions
    def submit_approval_decision(self, review_id: int, step_id: str, user_id: str,
                               decision: str = None, comments: str = None,
                               file_decisions: List[Dict] = None,
                               conditions: str = None) -> Dict[str, Any]:
        """
        Enhanced approval decision submission with comprehensive validation

        注意事项：
        - 只有状态为 DRAFT、IN_PROGRESS 或 PENDING 的 review 可以修改
        - CLOSED、CANCELLED、ARCHIVED 状态的 review 为只读
        - decision 参数已改为可选，提交审阅只需要 comments
        - file_decisions 仅在最终审批步骤使用
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # ✅ 检查 review 是否可修改
            can_modify, modify_error = self._check_review_is_modifiable(review_id, cursor)
            if not can_modify:
                return {
                    'success': False,
                    'error': modify_error,
                    'error_type': 'invalid_state',
                    'data': None
                }

            # 获取 workflow_id 用于验证决策（如果提供了 decision）
            cursor.execute("SELECT workflow_id FROM reviews WHERE id = %s", [review_id])
            review_info = cursor.fetchone()
            if not review_info:
                return {
                    'success': False,
                    'error': 'Review not found',
                    'error_type': 'not_found',
                    'data': None
                }

            workflow_id = review_info['workflow_id']

            # ✅ 验证决策值（仅在提供了 decision 时验证）
            if decision:
                is_valid, validation_error, valid_options = self._validate_approval_decision(
                    decision.upper(), workflow_id, cursor
                )
                if not is_valid:
                    return {
                        'success': False,
                        'error': validation_error,
                        'error_type': 'validation_error',
                        'data': None
                    }

            # ✅ 验证 file_decisions 中的每个决策（仅在提供了 file_decisions 时）
            if file_decisions:
                for file_dec in file_decisions:
                    file_decision = file_dec.get('decision', '').upper()
                    is_valid, validation_error, _ = self._validate_approval_decision(
                        file_decision, workflow_id, cursor
                    )
                    if not is_valid:
                        return {
                            'success': False,
                            'error': f"Invalid file decision: {validation_error}",
                            'error_type': 'validation_error',
                            'data': None
                        }
            
            # Get current step and verify permissions (use LATERAL to get latest record)
            cursor.execute("""
                SELECT rsc.candidates, COALESCE(rp.status, 'PENDING') as status, r.project_id, r.name as review_name
                FROM review_step_candidates rsc
                LEFT JOIN LATERAL (
                    SELECT *
                    FROM review_progress
                    WHERE review_id = rsc.review_id AND step_id = rsc.step_id
                    ORDER BY created_at DESC
                    LIMIT 1
                ) rp ON true
                JOIN reviews r ON rsc.review_id = r.id
                WHERE rsc.review_id = %s AND rsc.step_id = %s AND rsc.is_active = true
            """, [review_id, step_id])
            
            step_info = cursor.fetchone()
            if not step_info:
                return {
                    'success': False,
                    'error': 'Step not found or inactive',
                    'error_type': 'not_found',
                    'data': None
                }
            
            # Verify step status
            if step_info['status'] not in ['PENDING', 'CLAIMED']:
                return {
                    'success': False,
                    'error': f'Step cannot be approved in current status: {step_info["status"]}',
                    'error_type': 'invalid_state',
                    'data': None
                }
            
            # Enhanced permission check
            can_approve, permission_reason = self._check_comprehensive_permissions(
                user_id, step_info['candidates'], step_info['project_id']
            )
            
            if not can_approve:
                return {
                    'success': False,
                    'error': f'Permission denied: {permission_reason}',
                    'error_type': 'permission_denied',
                    'data': None
                }
            
            # Get user information for audit trail
            user_info = self._get_user_info(user_id, step_info['project_id'])

            now = datetime.now(timezone.utc)

            # Update step status with enhanced information
            # 步骤提交后状态设为 COMPLETED
            # Only update the latest record for this step
            new_status = 'COMPLETED'
            cursor.execute("""
                UPDATE review_progress
                SET
                    status = %s,
                    decision = %s,
                    comments = %s,
                    conditions = %s,
                    action_by = %s,
                    completed_by = %s,
                    completed_at = %s,
                    end_time = %s,
                    updated_at = %s
                WHERE review_id = %s AND step_id = %s
                  AND id = (
                      SELECT id FROM review_progress
                      WHERE review_id = %s AND step_id = %s
                      ORDER BY created_at DESC
                      LIMIT 1
                  )
                RETURNING id
            """, [
                new_status,
                decision,  # decision 可能为 None
                comments,
                conditions,
                json.dumps(user_info),
                json.dumps(user_info),
                now,
                now,
                now,
                review_id,
                step_id,
                review_id,
                step_id
            ])
            
            step_updated = cursor.fetchone()
            if not step_updated:
                raise Exception('Failed to update step status')
            
            # Process file decisions with enhanced validation
            files_processed = 0
            file_errors = []
            
            if file_decisions:
                for file_decision in file_decisions:
                    file_id = file_decision.get('file_id')
                    # Frontend sends 'decision' field, not 'status'
                    file_status = file_decision.get('decision', decision)
                    file_comments = file_decision.get('comments', '')

                    if not file_id:
                        error_msg = "Missing file_id in file decision"
                        logger.error(f"[submit_approval_decision] {error_msg}")
                        raise ValueError(error_msg)

                    logger.info(f"[submit_approval_decision] Processing file decision: file_id={file_id}, decision={file_status}")

                    cursor.execute("""
                        UPDATE review_file_versions
                        SET
                            approval_status = %s,
                            approval_comments = %s,
                            approved_at = %s,
                            updated_at = %s
                        WHERE id = %s AND review_id = %s
                        RETURNING id, file_version_urn
                    """, [
                        file_status,
                        file_comments,
                        now if file_status in ['APPROVED', 'REJECTED'] else None,
                        now,
                        file_id,
                        review_id
                    ])

                    file_result = cursor.fetchone()
                    if file_result:
                        files_processed += 1
                        logger.info(f"[submit_approval_decision] File {file_id} (URN: {file_result['file_version_urn']}) updated to {file_status}")
                    else:
                        error_msg = f"File {file_id} not found in review {review_id}"
                        logger.error(f"[submit_approval_decision] {error_msg}")
                        raise ValueError(error_msg)
            
            # Handle workflow progression
            workflow_result = self._handle_workflow_progression(
                cursor, review_id, step_id, decision, now
            )

            logger.info(f"Workflow progression result: {workflow_result}")

            conn.commit()
            
            # Log the approval action
            logger.info(f"Review step submitted: Review {review_id}, Step {step_id}, "
                       f"User {user_id}, Files processed: {files_processed}")

            return {
                'success': True,
                'message': 'Review step submitted successfully',
                'data': {
                    'review_id': review_id,
                    'step_id': step_id,
                    'decision': decision,  # 可能为 None
                    'user_info': user_info,
                    'permission_reason': permission_reason,
                    'files_processed': files_processed,
                    'file_errors': file_errors,
                    'workflow_progression': workflow_result,
                    'completed_at': now.isoformat()
                },
                'metadata': {
                    'submission_timestamp': now.isoformat(),
                    'review_name': step_info['review_name']
                }
            }
            
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error submitting approval decision: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    
    # ========================================================================
    # Enhanced Helper Methods
    # ========================================================================
    
    def _initialize_review_step_candidates_from_workflow(self, review_id: int, 
                                                         workflow_id: int) -> bool:
        """
        从 workflow 定义初始化 review_step_candidates
        这应该在创建 review 时调用，为每个步骤配置候选审批人
        
        Args:
            review_id: Review ID
            workflow_id: Workflow ID
            
        Returns:
            是否成功初始化
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # 获取 workflow 的步骤定义
            cursor.execute("""
                SELECT steps FROM workflows WHERE id = %s
            """, [workflow_id])
            
            workflow = cursor.fetchone()
            if not workflow or not workflow['steps']:
                logger.warning(f"Workflow {workflow_id} not found or has no steps")
                return False
            
            workflow_steps = workflow['steps']
            if isinstance(workflow_steps, str):
                workflow_steps = json.loads(workflow_steps)
            
            # 为每个步骤创建候选人配置
            now = datetime.now(timezone.utc)
            for step in workflow_steps:
                step_id = step.get('id')
                step_name = step.get('name', '')
                step_type = step.get('type', 'REVIEWER')
                step_order = step.get('order', 0)
                
                # 从 workflow 步骤定义中获取候选人配置
                candidates = {
                    'users': step.get('users', []),
                    'roles': step.get('roles', []),
                    'companies': step.get('companies', [])
                }
                
                cursor.execute("""
                    INSERT INTO review_step_candidates (
                        review_id, step_id, step_name, step_type, step_order,
                        candidates, source, is_active, created_at, updated_at
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (review_id, step_id)
                    WHERE status NOT IN ('SENT_BACK', 'COMPLETED')
                    DO UPDATE SET
                        step_name = EXCLUDED.step_name,
                        step_type = EXCLUDED.step_type,
                        step_order = EXCLUDED.step_order,
                        candidates = EXCLUDED.candidates,
                        updated_at = EXCLUDED.updated_at
                """, [
                    review_id, step_id, step_name, step_type, step_order,
                    json.dumps(candidates), 'workflow_template', True, now, now
                ])
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"Initialized {len(workflow_steps)} step candidates for review {review_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize review step candidates: {str(e)}")
            return False
    
    def _initialize_review_progress_from_workflow(self, review_id: int, 
                                                  workflow_id: int,
                                                  initial_step_id: str = None) -> bool:
        """
        从 workflow 定义初始化 review_progress
        这应该在创建 review 时调用，为每个步骤创建初始进度记录
        
        注意：review_progress 记录的是实际执行历史
        - 初始时所有步骤都设为 PENDING 状态
        - 第一个步骤会设置 started_at，其他步骤的 started_at 为 null
        - 当步骤被实际执行时，会更新状态为 COMPLETED/REJECTED 等
        
        Args:
            review_id: Review ID
            workflow_id: Workflow ID
            initial_step_id: 初始步骤ID（第一个步骤会设置 started_at）
            
        Returns:
            是否成功初始化
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # 获取 workflow 的步骤定义
            cursor.execute("""
                SELECT steps FROM workflows WHERE id = %s
            """, [workflow_id])
            
            workflow = cursor.fetchone()
            if not workflow or not workflow['steps']:
                logger.warning(f"Workflow {workflow_id} not found or has no steps")
                return False
            
            workflow_steps = workflow['steps']
            if isinstance(workflow_steps, str):
                workflow_steps = json.loads(workflow_steps)
            
            # 如果没有指定初始步骤，使用第一个步骤
            if not initial_step_id and workflow_steps:
                initial_step_id = workflow_steps[0].get('id')
            
            # 为每个步骤创建初始进度记录
            now = datetime.now(timezone.utc)
            for step in workflow_steps:
                step_id = step.get('id')
                step_name = step.get('name', '')
                step_type = step.get('type', 'REVIEWER')
                step_order = step.get('order', 0)
                
                # 第一个步骤设为 PENDING 并开始，其他也设为 PENDING 但不开始
                # 注意：数据库约束不接受 NOT_STARTED，所以都用 PENDING
                status = 'PENDING'
                started_at = now if step_id == initial_step_id else None
                
                cursor.execute("""
                    INSERT INTO review_progress (
                        review_id, step_id, step_name, step_type, step_order,
                        status, started_at, created_at, updated_at
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (review_id, step_id)
                    WHERE status NOT IN ('SENT_BACK', 'COMPLETED')
                    DO UPDATE SET
                        step_name = EXCLUDED.step_name,
                        step_type = EXCLUDED.step_type,
                        step_order = EXCLUDED.step_order,
                        status = EXCLUDED.status,
                        started_at = EXCLUDED.started_at,
                        updated_at = EXCLUDED.updated_at
                """, [
                    review_id, step_id, step_name, step_type, step_order,
                    status, started_at, now, now
                ])
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"Initialized {len(workflow_steps)} progress records for review {review_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize review progress: {str(e)}")
            return False
    
    def _check_review_is_modifiable(self, review_id: int, cursor) -> Tuple[bool, str]:
        """
        检查 review 是否可以修改
        
        Args:
            review_id: Review ID
            cursor: 数据库游标
            
        Returns:
            (是否可修改, 错误消息)
        """
        cursor.execute("""
            SELECT status FROM reviews WHERE id = %s
        """, [review_id])
        
        review = cursor.fetchone()
        if not review:
            return False, f"Review {review_id} not found"
        
        # 只有以下状态的 review 可以修改
        # OPEN 状态表示审阅已启动，应该允许继续进行审阅操作
        modifiable_statuses = ['DRAFT', 'IN_PROGRESS', 'PENDING', 'OPEN']

        if review['status'] not in modifiable_statuses:
            return False, f"Review is {review['status']} and cannot be modified. Only DRAFT, IN_PROGRESS, PENDING, or OPEN reviews can be modified."

        return True, ""
    
    def _get_workflow_approval_status_options(self, workflow_id: int, cursor) -> List[Dict]:
        """
        获取 workflow 配置的自定义审批状态选项
        
        Args:
            workflow_id: Workflow ID
            cursor: 数据库游标
            
        Returns:
            审批状态选项列表，格式：
            [
                {
                    "id": "f44e623d-f04f-47fe-8195-efc43d1d985b",
                    "label": "已批准",
                    "value": "APPROVED",
                    "builtIn": true
                },
                ...
            ]
        """
        cursor.execute("""
            SELECT approval_status_options FROM workflows WHERE id = %s
        """, [workflow_id])
        
        workflow = cursor.fetchone()
        if not workflow:
            return []
        
        options = workflow.get('approval_status_options')
        if not options:
            return []
        
        # 如果是字符串，解析为 JSON
        if isinstance(options, str):
            try:
                options = json.loads(options)
            except:
                return []
        
        return options if isinstance(options, list) else []
    
    def _validate_approval_decision(self, decision: str, workflow_id: int, cursor) -> Tuple[bool, str, List[str]]:
        """
        验证审批决策是否有效
        
        核心概念：
        - 所有审批状态的 value 最终只有两个：APPROVED 或 REJECTED
        - workflow 的 approval_status_options 配置了多个选项（如"已批准"、"已批准且带注释"），
          但它们的 value 都是 APPROVED 或 REJECTED
        - 前端应该：
          1. 从 workflow.approval_status_options 读取配置
          2. 显示 label 给用户选择（如"已批准"、"已拒绝"、"已批准且带注释"）
          3. 提交时使用对应的 value（APPROVED 或 REJECTED）
        - 后端只验证 value 是否为 APPROVED 或 REJECTED
        
        Args:
            decision: 决策值（必须是 APPROVED 或 REJECTED）
            workflow_id: Workflow ID
            cursor: 数据库游标
            
        Returns:
            (是否有效, 错误消息, 有效决策列表)
        """
        # 核心决策值（所有 approval_status_options 的 value 都映射到这两个）
        valid_core_decisions = ['APPROVED', 'REJECTED']
        
        if decision not in valid_core_decisions:
            # 获取自定义选项以提供更友好的错误消息
            custom_options = self._get_workflow_approval_status_options(workflow_id, cursor)
            if custom_options:
                available_options = [f"{opt.get('label')} (value: {opt.get('value')})" for opt in custom_options]
                error_msg = f"Invalid decision '{decision}'. Available options: {', '.join(available_options)}. Note: Use the 'value' field (APPROVED/REJECTED), not the label."
            else:
                error_msg = f"Invalid decision '{decision}'. Valid values: APPROVED, REJECTED"
            
            return False, error_msg, valid_core_decisions
        
        return True, "", valid_core_decisions
    
    def _get_user_info(self, user_id: str, project_id: str) -> Dict[str, Any]:
        """
        Get comprehensive user information by joining users and project_users tables.

        注意：user_id 参数可能是：
        - project_users.autodesk_id (前端传递的 Autodesk ID)
        - users.user_id (用户表的主键)

        我们需要通过 project_users.autodesk_id 来查找用户信息
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # 通过 autodesk_id 联合查询 project_users 和 users 表
            cursor.execute("""
                SELECT
                    u.name as user_name,
                    u.email,
                    pu.project_company_name as company_name,
                    pu.autodesk_id
                FROM project_users pu
                JOIN users u ON pu.user_id = u.user_id
                WHERE pu.autodesk_id = %s AND pu.project_id = %s
                LIMIT 1
            """, [user_id, project_id])

            result = cursor.fetchone()

            if not result:
                # 如果通过 autodesk_id 找不到，尝试直接用 user_id 查询
                cursor.execute("""
                    SELECT
                        u.name as user_name,
                        u.email,
                        pu.project_company_name as company_name
                    FROM users u
                    LEFT JOIN project_users pu ON u.user_id = pu.user_id AND pu.project_id = %s
                    WHERE u.user_id = %s
                    LIMIT 1
                """, [project_id, user_id])
                result = cursor.fetchone()

            cursor.close()
            conn.close()

            if result:
                return {
                    'autodeskId': user_id,
                    'name': result['user_name'] or 'Unknown User',
                    'email': result['email'],
                    'company': result['company_name']
                }
            else:
                # 记录警告：找不到用户
                logger.warning(f"User not found: autodesk_id/user_id={user_id}, project_id={project_id}")
                return {
                    'autodeskId': user_id,
                    'name': 'Unknown User',
                    'email': None,
                    'company': None
                }

        except Exception as e:
            logger.warning(f"Could not fetch user info: {str(e)}, user_id={user_id}, project_id={project_id}")
            return {
                'autodeskId': user_id,
                'name': 'Unknown User',
                'email': None,
                'company': None
            }
    
    def _determine_step_status(self, decision: str) -> str:
        """Determine step status based on decision"""
        status_mapping = {
            'APPROVED': 'COMPLETED',
            'REJECTED': 'REJECTED',
            'REQUEST_CHANGES': 'REQUEST_CHANGES',
            'CONDITIONAL_APPROVAL': 'CONDITIONAL'
        }
        return status_mapping.get(decision, 'COMPLETED')
    
    def _handle_workflow_progression(self, cursor, review_id: int,
                                   current_step_id: str, decision: str,
                                   timestamp: datetime) -> Dict[str, Any]:
        """Handle workflow progression logic"""
        try:
            # 步骤提交后自动进入下一步（无论是否有 decision）
            if decision == 'APPROVED' or decision is None:
                # Get next step
                next_step_info = self._get_next_step(cursor, review_id, current_step_id)
                
                if next_step_info:
                    # Move to next step
                    cursor.execute("""
                        UPDATE reviews
                        SET 
                            current_step_id = %s,
                            current_step_name = %s,
                            current_step_number = %s,
                            progress_percentage = %s,
                            updated_at = %s
                        WHERE id = %s
                    """, [
                        next_step_info['step_id'],
                        next_step_info['step_name'],
                        next_step_info['step_order'],
                        (next_step_info['step_order'] / next_step_info['total_steps']) * 100,
                        timestamp,
                        review_id
                    ])

                    # Activate next step - Use UPSERT to support both ACC synced and locally created reviews
                    # First, get step configuration from review_step_candidates
                    cursor.execute("""
                        SELECT step_id, step_name, step_type, step_order, candidates
                        FROM review_step_candidates
                        WHERE review_id = %s AND step_id = %s
                    """, [review_id, next_step_info['step_id']])

                    next_step_config = cursor.fetchone()
                    if not next_step_config:
                        logger.error(f"Next step configuration not found: review_id={review_id}, step_id={next_step_info['step_id']}")
                        raise Exception(f"Step configuration not found for step {next_step_info['step_id']}")

                    # UPSERT: Insert if not exists, update if exists
                    # This handles both ACC synced reviews (all steps pre-exist) and local reviews (steps created on demand)
                    cursor.execute("""
                        INSERT INTO review_progress (
                            review_id, step_id, step_name, step_type, step_order,
                            status, started_at, candidates, created_at, updated_at
                        ) VALUES (
                            %s, %s, %s, %s, %s, 'PENDING', %s, %s, %s, %s
                        )
                        ON CONFLICT (review_id, step_id)
                    WHERE status NOT IN ('SENT_BACK', 'COMPLETED')
                    DO UPDATE SET
                            status = 'PENDING',
                            started_at = EXCLUDED.started_at,
                            updated_at = EXCLUDED.updated_at
                    """, [
                        review_id,
                        next_step_config['step_id'],
                        next_step_config['step_name'],
                        next_step_config['step_type'],
                        next_step_config['step_order'],
                        timestamp,
                        Json(next_step_config['candidates']) if next_step_config['candidates'] else Json({}),
                        timestamp,
                        timestamp
                    ])

                    logger.info(f"Activated next step: review_id={review_id}, step_id={next_step_info['step_id']}, step_name={next_step_config['step_name']}")

                    return {
                        'action': 'moved_to_next_step',
                        'next_step': next_step_info,
                        'review_status': 'OPEN'
                    }
                else:
                    # Complete review
                    cursor.execute("""
                        UPDATE reviews
                        SET 
                            status = 'CLOSED',
                            finished_at = %s,
                            progress_percentage = 100.0,
                            updated_at = %s
                        WHERE id = %s
                    """, [timestamp, timestamp, review_id])
                    
                    return {
                        'action': 'review_completed',
                        'next_step': None,
                        'review_status': 'CLOSED'
                    }
            
            elif decision in ['REJECTED', 'REQUEST_CHANGES']:
                # Handle rejection or change request
                cursor.execute("""
                    UPDATE reviews
                    SET 
                        status = 'VOID' if %s = 'REJECTED' else 'OPEN',
                        updated_at = %s
                    WHERE id = %s
                """, [decision, timestamp, review_id])
                
                return {
                    'action': 'review_rejected' if decision == 'REJECTED' else 'changes_requested',
                    'next_step': None,
                    'review_status': 'VOID' if decision == 'REJECTED' else 'OPEN'
                }
            
            return {
                'action': 'no_progression',
                'next_step': None,
                'review_status': 'unchanged'
            }
            
        except Exception as e:
            logger.error(f"Error in workflow progression: {str(e)}")
            raise
    
    def _get_next_step(self, cursor, review_id: int, current_step_id: str) -> Optional[Dict]:
        """
        Get next step information with total steps count.

        注意：查询 review_step_candidates 而不是 review_progress，
        因为 review_progress 只记录已执行的步骤，而 review_step_candidates 包含所有步骤配置
        """
        try:
            # Get current step order from review_step_candidates
            cursor.execute("""
                SELECT step_order
                FROM review_step_candidates
                WHERE review_id = %s AND step_id = %s
            """, [review_id, current_step_id])

            current_info = cursor.fetchone()
            if not current_info:
                logger.warning(f"Current step not found: review_id={review_id}, step_id={current_step_id}")
                return None

            current_order = current_info['step_order']

            # Get next step from review_step_candidates
            cursor.execute("""
                SELECT step_id, step_name, step_type, step_order,
                       (SELECT COUNT(*) FROM review_step_candidates WHERE review_id = %s) as total_steps
                FROM review_step_candidates
                WHERE review_id = %s AND step_order > %s AND is_active = true
                ORDER BY step_order ASC
                LIMIT 1
            """, [review_id, review_id, current_order])

            next_step = cursor.fetchone()
            if next_step:
                return {
                    'step_id': next_step['step_id'],
                    'step_name': next_step['step_name'],
                    'step_type': next_step['step_type'],
                    'step_order': next_step['step_order'],
                    'total_steps': next_step['total_steps']
                }

            logger.info(f"No next step found after step_order={current_order} for review_id={review_id}")
            return None

        except Exception as e:
            logger.error(f"Error getting next step: {str(e)}")
            return None


# ============================================================================
# Enhanced API Endpoints
# ============================================================================

# Create enhanced manager instance
enhanced_approval_manager = EnhancedApprovalWorkflowManager()

@approval_bp.route('/api/approval/users/<user_id>/pending', methods=['GET'])
def get_pending_approvals_enhanced(user_id):
    """Enhanced endpoint for getting user's pending approvals"""
    try:
        project_id = request.args.get('project_id')
        
        # Parse filters from query parameters
        filters = {}
        if request.args.get('priority'):
            filters['priority'] = int(request.args.get('priority'))
        if request.args.get('department'):
            filters['department'] = request.args.get('department')
        if request.args.get('urgency_level'):
            filters['urgency_level'] = request.args.get('urgency_level')
        
        result = enhanced_approval_manager.get_pending_approvals(
            user_id, project_id, filters if filters else None
        )
        
        status_code = 200 if result['success'] else 500
        if result.get('error_type') == 'not_found':
            status_code = 404
        elif result.get('error_type') == 'validation_error':
            status_code = 400
        
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Unexpected error in get_pending_approvals_enhanced: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}',
            'error_type': 'internal_error'
        }), 500

@approval_bp.route('/api/approval/reviews/<int:review_id>', methods=['GET'])
def get_review_for_approval_enhanced(review_id):
    """Enhanced endpoint for getting review details for approval"""
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'Missing required parameter: user_id',
                'error_type': 'validation_error'
            }), 400
        
        result = enhanced_approval_manager.get_review_details_for_approval(review_id, user_id)
        
        status_code = 200 if result['success'] else 500
        if result.get('error_type') == 'not_found':
            status_code = 404
        elif result.get('error_type') == 'validation_error':
            status_code = 400
        
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Unexpected error in get_review_for_approval_enhanced: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}',
            'error_type': 'internal_error'
        }), 500

@approval_bp.route('/api/approval/reviews/<int:review_id>/steps/<step_id>/decide', methods=['POST'])
def submit_approval_decision_enhanced(review_id, step_id):
    """Enhanced endpoint for submitting approval decisions"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body must contain JSON data',
                'error_type': 'validation_error'
            }), 400
        
        # Validate required fields (decision 已改为可选，只需要 user_id)
        required_fields = ['user_id']
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}',
                'error_type': 'validation_error'
            }), 400

        result = enhanced_approval_manager.submit_approval_decision(
            review_id=review_id,
            step_id=step_id,
            user_id=data['user_id'],
            decision=data.get('decision'),  # 可选参数
            comments=data.get('comments', ''),
            file_decisions=data.get('file_decisions', []),
            conditions=data.get('conditions', '')
        )
        
        status_code = 200 if result['success'] else 400
        if result.get('error_type') == 'not_found':
            status_code = 404
        elif result.get('error_type') == 'permission_denied':
            status_code = 403
        elif result.get('error_type') == 'validation_error':
            status_code = 400
        
        return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Unexpected error in submit_approval_decision_enhanced: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}',
            'error_type': 'internal_error'
        }), 500

@approval_bp.route('/api/approval/reviews', methods=['POST'])
def create_review_with_workflow():
    """
    创建新的 review 并自动初始化 step_candidates 和 progress
    
    这个端点会：
    1. 创建 review 记录
    2. 从 workflow 定义初始化 review_step_candidates（静态配置）
    3. 从 workflow 定义初始化 review_progress（动态记录）
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body must contain JSON data',
                'error_type': 'validation_error'
            }), 400
        
        # 验证必需字段
        required_fields = ['project_id', 'workflow_id', 'name', 'created_by']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}',
                'error_type': 'validation_error'
            }), 400
        
        conn = None
        try:
            conn = enhanced_approval_manager.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # 生成 review UUID
            import uuid
            review_uuid = str(uuid.uuid4())
            now = datetime.now(timezone.utc)
            
            # 获取 workflow 信息
            cursor.execute("""
                SELECT id, steps FROM workflows WHERE id = %s
            """, [data['workflow_id']])
            
            workflow = cursor.fetchone()
            if not workflow:
                return jsonify({
                    'success': False,
                    'error': f'Workflow {data["workflow_id"]} not found',
                    'error_type': 'not_found'
                }), 404
            
            workflow_steps = workflow['steps']
            if isinstance(workflow_steps, str):
                workflow_steps = json.loads(workflow_steps)
            
            if not workflow_steps:
                return jsonify({
                    'success': False,
                    'error': 'Workflow has no steps defined',
                    'error_type': 'validation_error'
                }), 400
            
            # 获取第一个步骤作为初始步骤
            first_step = workflow_steps[0]
            first_step_id = first_step.get('id')
            first_step_name = first_step.get('name', '')
            
            # 创建 review 记录
            cursor.execute("""
                INSERT INTO reviews (
                    review_uuid, project_id, workflow_id, data_source,
                    name, description, status, created_by, priority,
                    department, category, total_steps, current_step_number,
                    current_step_id, current_step_name,
                    progress_percentage, created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                RETURNING id
            """, [
                review_uuid,
                data['project_id'],
                data['workflow_id'],
                'local_system',
                data['name'],
                data.get('description', ''),
                'DRAFT',  # 初始状态为 DRAFT
                json.dumps(data['created_by']),
                data.get('priority', 2),
                data.get('department', ''),
                data.get('category', ''),
                len(workflow_steps),
                1,  # 从第一步开始
                first_step_id,
                first_step_name,
                0.0,  # 初始进度为 0
                now,
                now
            ])
            
            review_id = cursor.fetchone()['id']
            
            # 直接在当前事务中初始化步骤（避免事务隔离问题）
            # 为每个步骤创建候选人配置和进度记录
            for step in workflow_steps:
                step_id = step.get('id')
                step_name = step.get('name', '')
                step_type = step.get('type', 'REVIEWER')
                step_order = step.get('order', 0)

                # 创建 review_step_candidates
                candidates = {
                    'users': step.get('users', []),
                    'roles': step.get('roles', []),
                    'companies': step.get('companies', [])
                }

                cursor.execute("""
                    INSERT INTO review_step_candidates (
                        review_id, step_id, step_name, step_type, step_order,
                        candidates, source, is_active, created_at, updated_at
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """, [
                    review_id, step_id, step_name, step_type, step_order,
                    json.dumps(candidates), 'workflow_template', True, now, now
                ])

                # 创建 review_progress
                status = 'PENDING'
                started_at = now if step_id == first_step_id else None

                cursor.execute("""
                    INSERT INTO review_progress (
                        review_id, step_id, step_name, step_type, step_order,
                        status, started_at, created_at, updated_at
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """, [
                    review_id, step_id, step_name, step_type, step_order,
                    status, started_at, now, now
                ])

            conn.commit()
            cursor.close()
            
            return jsonify({
                'success': True,
                'message': 'Review created successfully with workflow configuration',
                'data': {
                    'review_id': review_id,
                    'review_uuid': review_uuid,
                    'workflow_id': data['workflow_id'],
                    'total_steps': len(workflow_steps),
                    'current_step_id': first_step_id,
                    'current_step_name': first_step_name,
                    'steps_initialized': len(workflow_steps)
                },
                'metadata': {
                    'created_at': now.isoformat()
                }
            }), 201
            
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error creating review: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
        
    except Exception as e:
        logger.error(f"Unexpected error in create_review_with_workflow: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}',
            'error_type': 'internal_error'
        }), 500

@approval_bp.route('/api/approval/reviews/<int:review_id>/steps/<step_id>/start', methods=['POST'])
def start_step(review_id, step_id):
    """
    启动审批步骤（claim step）

    这个端点会：
    1. 验证用户权限
    2. 将步骤状态从 PENDING 更新为 CLAIMED
    3. 记录 claimed_by 和 started_at

    Request Body:
    {
        "user_id": "string",  # 必需：用户ID
        "notes": "string"     # 可选：启动备注
    }
    """
    try:
        data = request.get_json()
        if not data or not data.get('user_id'):
            return jsonify({
                'success': False,
                'error': 'Missing required field: user_id',
                'error_type': 'validation_error'
            }), 400

        user_id = data['user_id']
        notes = data.get('notes', '')
        
        conn = None
        try:
            conn = enhanced_approval_manager.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # ✅ 检查 review 是否可修改
            can_modify, modify_error = enhanced_approval_manager._check_review_is_modifiable(review_id, cursor)
            if not can_modify:
                return jsonify({
                    'success': False,
                    'error': modify_error,
                    'error_type': 'invalid_state'
                }), 400
            
            # 获取步骤信息和权限验证
            # Use LEFT JOIN LATERAL to get only the latest review_progress record
            cursor.execute("""
                SELECT
                    rsc.candidates,
                    COALESCE(rp.status, 'PENDING') as status,
                    rp.claimed_by,
                    r.project_id,
                    r.name as review_name,
                    r.current_step_id
                FROM review_step_candidates rsc
                LEFT JOIN LATERAL (
                    SELECT *
                    FROM review_progress
                    WHERE review_id = rsc.review_id AND step_id = rsc.step_id
                    ORDER BY created_at DESC
                    LIMIT 1
                ) rp ON true
                JOIN reviews r ON rsc.review_id = r.id
                WHERE rsc.review_id = %s AND rsc.step_id = %s AND rsc.is_active = true
            """, [review_id, step_id])

            step_info = cursor.fetchone()
            if not step_info:
                return jsonify({
                    'success': False,
                    'error': 'Step not found or inactive',
                    'error_type': 'not_found'
                }), 404

            # 验证步骤状态
            if step_info['status'] not in ['PENDING']:
                return jsonify({
                    'success': False,
                    'error': f'Step cannot be started in current status: {step_info["status"]}',
                    'error_type': 'invalid_state',
                    'data': {
                        'current_status': step_info['status'],
                        'claimed_by': step_info.get('claimed_by')
                    }
                }), 400
            
            # 验证这是当前活动步骤
            if step_info['current_step_id'] != step_id:
                return jsonify({
                    'success': False,
                    'error': f'This is not the current active step. Current step: {step_info["current_step_id"]}',
                    'error_type': 'invalid_state'
                }), 400
            
            # 权限验证
            can_start, permission_reason = enhanced_approval_manager._check_comprehensive_permissions(
                user_id, step_info['candidates'], step_info['project_id']
            )
            
            if not can_start:
                return jsonify({
                    'success': False,
                    'error': f'Permission denied: {permission_reason}',
                    'error_type': 'permission_denied'
                }), 403

            # 获取用户信息
            user_info = enhanced_approval_manager._get_user_info(user_id, step_info['project_id'])

            now = datetime.now(timezone.utc)

            # 获取步骤的详细信息（从 review_step_candidates）
            cursor.execute("""
                SELECT step_name, step_type, step_order
                FROM review_step_candidates
                WHERE review_id = %s AND step_id = %s
            """, [review_id, step_id])
            step_details = cursor.fetchone()

            # Update the latest review_progress record to CLAIMED status
            # First, try to update existing PENDING record
            cursor.execute("""
                UPDATE review_progress
                SET
                    status = 'CLAIMED',
                    claimed_by = %s,
                    started_at = %s,
                    notes = %s,
                    updated_at = %s
                WHERE review_id = %s AND step_id = %s
                  AND id = (
                      SELECT id FROM review_progress
                      WHERE review_id = %s AND step_id = %s
                      ORDER BY created_at DESC
                      LIMIT 1
                  )
                RETURNING id
            """, [
                json.dumps(user_info),
                now,
                notes,
                now,
                review_id,
                step_id,
                review_id,
                step_id
            ])

            step_updated = cursor.fetchone()

            # If no record exists (shouldn't happen, but handle it), create one
            if not step_updated:
                cursor.execute("""
                    INSERT INTO review_progress (
                        review_id, step_id, step_name, step_type, step_order,
                        status, claimed_by, started_at, notes,
                        created_at, updated_at
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    RETURNING id
                """, [
                    review_id,
                    step_id,
                    step_details['step_name'] if step_details else '',
                    step_details['step_type'] if step_details else 'REVIEWER',
                    step_details['step_order'] if step_details else 0,
                    'CLAIMED',
                    json.dumps(user_info),
                    now,
                    notes,
                    now,
                    now
                ])
                step_updated = cursor.fetchone()

            if not step_updated:
                raise Exception('Failed to start step')
            
            conn.commit()
            cursor.close()
            
            logger.info(f"Step started: Review {review_id}, Step {step_id}, User {user_id}")
            
            return jsonify({
                'success': True,
                'message': 'Step started successfully',
                'data': {
                    'review_id': review_id,
                    'step_id': step_id,
                    'status': 'CLAIMED',
                    'claimed_by': user_info,
                    'started_at': now.isoformat(),
                    'notes': notes
                },
                'metadata': {
                    'review_name': step_info['review_name'],
                    'timestamp': now.isoformat()
                }
            }), 200
            
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error starting step: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
        
    except Exception as e:
        logger.error(f"Unexpected error in start_step: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}',
            'error_type': 'internal_error'
        }), 500

@approval_bp.route('/api/approval/reviews/<int:review_id>/steps/<step_id>/submit', methods=['POST'])
def submit_step(review_id, step_id):
    """
    提交审批决策（支持文件级决策）
    
    这个端点会：
    1. 验证用户权限
    2. 更新步骤状态
    3. 支持整体决策或文件级决策
    4. 处理工作流流转
    
    Request Body:
    {
        "user_id": "string",              # 必需：用户ID
        "decision": "string",             # 必需：整体决策 (APPROVED/REJECTED/REQUEST_CHANGES)
        "comments": "string",             # 可选：整体评论
        "conditions": "string",           # 可选：条件说明
        "file_decisions": [               # 可选：文件级决策
            {
                "file_id": 123,           # 文件ID
                "file_version_urn": "urn:...",  # 或使用 URN
                "decision": "APPROVED",   # 文件决策
                "comments": "string"      # 文件评论
            }
        ]
    }
    """
    try:
        data = request.get_json()
        if not data or not data.get('user_id') or not data.get('decision'):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: user_id and decision',
                'error_type': 'validation_error'
            }), 400
        
        user_id = data['user_id']
        decision = data['decision'].upper()
        comments = data.get('comments', '')
        conditions = data.get('conditions', '')
        file_decisions = data.get('file_decisions', [])
        
        # 调用 manager 的 submit_approval_decision 方法（内部会进行完整验证）
        result = enhanced_approval_manager.submit_approval_decision(
            review_id=review_id,
            step_id=step_id,
            user_id=user_id,
            decision=decision,
            comments=comments,
            file_decisions=file_decisions,
            conditions=conditions
        )
        
        if result['success']:
            return jsonify(result), 200
        else:
            status_code = 403 if result.get('error_type') == 'permission_denied' else 400
            return jsonify(result), status_code
        
    except Exception as e:
        logger.error(f"Unexpected error in submit_step: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}',
            'error_type': 'internal_error'
        }), 500

@approval_bp.route('/api/approval/reviews/<int:review_id>/notify', methods=['POST'])
def send_review_notification(review_id):
    """
    發送review相關通知

    創建review後或步驟完成後發送通知給相關用戶

    Request Body:
    {
        "user_ids": ["user1_autodeskId", "user2_autodeskId"],
        "message": "通知消息內容",
        "notification_type": "review_created|step_completed|review_completed",
        "sender_info": {"autodeskId": "xxx", "name": "xxx"}
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body must contain JSON data',
                'error_type': 'validation_error'
            }), 400

        # 驗證必需字段
        required_fields = ['user_ids', 'message', 'sender_info']
        missing_fields = [field for field in required_fields if not data.get(field)]

        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}',
                'error_type': 'validation_error'
            }), 400

        user_ids = data['user_ids']
        message = data['message']
        notification_type = data.get('notification_type', 'review_created')
        sender_info = data['sender_info']

        conn = None
        try:
            conn = enhanced_approval_manager.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # 驗證review存在
            cursor.execute("""
                SELECT id, name, project_id FROM reviews WHERE id = %s
            """, [review_id])

            review = cursor.fetchone()
            if not review:
                return jsonify({
                    'success': False,
                    'error': f'Review {review_id} not found',
                    'error_type': 'not_found'
                }), 404

            now = datetime.now(timezone.utc)
            notifications_created = []

            # 為每個用戶創建通知記錄
            for user_id in user_ids:
                cursor.execute("""
                    INSERT INTO review_notifications (
                        review_id, user_id, message, notification_type,
                        sent_by, sent_at, is_read, created_at
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    RETURNING id
                """, [
                    review_id,
                    user_id,
                    message,
                    notification_type,
                    json.dumps(sender_info),
                    now,
                    False,
                    now
                ])

                notification_id = cursor.fetchone()['id']
                notifications_created.append({
                    'notification_id': notification_id,
                    'user_id': user_id,
                    'message': message,
                    'sent_at': now.isoformat()
                })

            conn.commit()

            return jsonify({
                'success': True,
                'message': f'Successfully sent notifications to {len(user_ids)} users',
                'data': {
                    'review_id': review_id,
                    'review_name': review['name'],
                    'notification_type': notification_type,
                    'sender': sender_info,
                    'recipients_count': len(user_ids),
                    'notifications': notifications_created
                },
                'metadata': {
                    'sent_at': now.isoformat()
                }
            }), 201

        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error sending review notification: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()

    except Exception as e:
        logger.error(f"Unexpected error in send_review_notification: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}',
            'error_type': 'internal_error'
        }), 500

@approval_bp.route('/api/approval/reviews/<int:review_id>/notifications', methods=['GET'])
def get_review_notifications(review_id):
    """
    獲取review的通知歷史

    Query Parameters:
    - user_id: 過濾特定用戶的通知
    - is_read: 過濾已讀/未讀通知 (true/false)
    - notification_type: 過濾通知類型
    """
    try:
        user_id = request.args.get('user_id')
        is_read = request.args.get('is_read')
        notification_type = request.args.get('notification_type')

        conn = None
        try:
            conn = enhanced_approval_manager.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # 構建查詢條件
            where_conditions = ["review_id = %s"]
            params = [review_id]

            if user_id:
                where_conditions.append("user_id = %s")
                params.append(user_id)

            if is_read is not None:
                where_conditions.append("is_read = %s")
                params.append(is_read.lower() == 'true')

            if notification_type:
                where_conditions.append("notification_type = %s")
                params.append(notification_type)

            where_clause = " AND ".join(where_conditions)

            cursor.execute(f"""
                SELECT
                    id, review_id, user_id, message, notification_type,
                    sent_by, sent_at, read_at, is_read, created_at
                FROM review_notifications
                WHERE {where_clause}
                ORDER BY created_at DESC
            """, params)

            notifications = []
            for row in cursor.fetchall():
                notification = dict(row)

                # 解析sent_by JSON字段
                if notification.get('sent_by'):
                    try:
                        notification['sent_by'] = json.loads(notification['sent_by'])
                    except:
                        notification['sent_by'] = {}

                notifications.append(notification)

            return jsonify({
                'success': True,
                'data': {
                    'review_id': review_id,
                    'total_notifications': len(notifications),
                    'notifications': notifications
                }
            }), 200

        except Exception as e:
            logger.error(f"Error getting review notifications: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()

    except Exception as e:
        logger.error(f"Unexpected error in get_review_notifications: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}',
            'error_type': 'internal_error'
        }), 500

@approval_bp.route('/api/approval/reviews/<int:review_id>/files/batch-approve', methods=['POST'])
def batch_approve_files(review_id):
    """
    批量审批文件
    
    这个端点允许一次性审批多个文件，每个文件可以有独立的决策和评论。
    适用于需要快速处理大量文件的场景。
    
    Request Body:
    {
        "user_id": "string",              # 必需：用户ID
        "files": [                        # 必需：文件审批列表
            {
                "file_id": 123,           # 文件ID（二选一）
                "file_version_urn": "urn:...",  # 或使用 URN（二选一）
                "decision": "APPROVED",   # 必需：文件决策
                "comments": "string"      # 可选：文件评论
            }
        ],
        "overall_comments": "string"      # 可选：整体评论
    }
    
    Response:
    {
        "success": true,
        "message": "Batch approval completed",
        "data": {
            "review_id": 123,
            "total_files": 10,
            "processed": 10,
            "successful": 9,
            "failed": 1,
            "results": [...]
        }
    }
    """
    try:
        data = request.get_json()
        if not data or not data.get('user_id') or not data.get('files'):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: user_id and files',
                'error_type': 'validation_error'
            }), 400
        
        user_id = data['user_id']
        files = data['files']
        overall_comments = data.get('overall_comments', '')
        
        if not isinstance(files, list) or len(files) == 0:
            return jsonify({
                'success': False,
                'error': 'files must be a non-empty array',
                'error_type': 'validation_error'
            }), 400
        
        conn = None
        try:
            conn = enhanced_approval_manager.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # ✅ 检查 review 是否可修改
            can_modify, modify_error = enhanced_approval_manager._check_review_is_modifiable(review_id, cursor)
            if not can_modify:
                return jsonify({
                    'success': False,
                    'error': modify_error,
                    'error_type': 'invalid_state'
                }), 400
            
            # 验证 review 存在并获取基本信息
            cursor.execute("""
                SELECT id, name, status, project_id, current_step_id, workflow_id
                FROM reviews
                WHERE id = %s
            """, [review_id])
            
            review = cursor.fetchone()
            if not review:
                return jsonify({
                    'success': False,
                    'error': f'Review {review_id} not found',
                    'error_type': 'not_found'
                }), 404
            
            workflow_id = review['workflow_id']
            
            # 验证用户对当前步骤的权限
            if review['current_step_id']:
                cursor.execute("""
                    SELECT candidates FROM review_step_candidates
                    WHERE review_id = %s AND step_id = %s AND is_active = true
                """, [review_id, review['current_step_id']])
                
                step_candidate = cursor.fetchone()
                if step_candidate:
                    can_approve, permission_reason = enhanced_approval_manager._check_comprehensive_permissions(
                        user_id, step_candidate['candidates'], review['project_id']
                    )
                    
                    if not can_approve:
                        return jsonify({
                            'success': False,
                            'error': f'Permission denied: {permission_reason}',
                            'error_type': 'permission_denied'
                        }), 403
            
            # 获取用户信息
            user_info = enhanced_approval_manager._get_user_info(user_id, review['project_id'])
            
            now = datetime.now(timezone.utc)
            
            # 批量处理文件审批
            results = []
            successful_count = 0
            failed_count = 0
            
            for file_data in files:
                file_result = {
                    'file_id': file_data.get('file_id'),
                    'file_version_urn': file_data.get('file_version_urn'),
                    'success': False,
                    'error': None
                }
                
                try:
                    # 验证必需字段
                    if not file_data.get('decision'):
                        file_result['error'] = 'Missing decision field'
                        failed_count += 1
                        results.append(file_result)
                        continue
                    
                    decision = file_data['decision'].upper()
                    
                    # ✅ 验证决策值（使用简化的核心值验证）
                    is_valid, validation_error, valid_decisions = enhanced_approval_manager._validate_approval_decision(
                        decision, workflow_id, cursor
                    )
                    
                    if not is_valid:
                        file_result['error'] = validation_error
                        failed_count += 1
                        results.append(file_result)
                        continue
                    
                    # 根据提供的标识符更新文件
                    if file_data.get('file_id'):
                        # 使用 file_id
                        cursor.execute("""
                            UPDATE review_file_versions
                            SET 
                                approval_status = %s,
                                approval_comments = %s,
                                approved_at = %s,
                                updated_at = %s
                            WHERE id = %s AND review_id = %s
                            RETURNING id, file_version_urn, approval_status
                        """, [
                            decision,
                            file_data.get('comments', ''),
                            now if decision in ['APPROVED', 'REJECTED'] else None,
                            now,
                            file_data['file_id'],
                            review_id
                        ])
                    elif file_data.get('file_version_urn'):
                        # 使用 file_version_urn
                        cursor.execute("""
                            UPDATE review_file_versions
                            SET 
                                approval_status = %s,
                                approval_comments = %s,
                                approved_at = %s,
                                updated_at = %s
                            WHERE file_version_urn = %s AND review_id = %s
                            RETURNING id, file_version_urn, approval_status
                        """, [
                            decision,
                            file_data.get('comments', ''),
                            now if decision in ['APPROVED', 'REJECTED'] else None,
                            now,
                            file_data['file_version_urn'],
                            review_id
                        ])
                    else:
                        file_result['error'] = 'Must provide either file_id or file_version_urn'
                        failed_count += 1
                        results.append(file_result)
                        continue
                    
                    updated_file = cursor.fetchone()
                    
                    if updated_file:
                        file_result['success'] = True
                        file_result['file_id'] = updated_file['id']
                        file_result['file_version_urn'] = updated_file['file_version_urn']
                        file_result['approval_status'] = updated_file['approval_status']
                        successful_count += 1
                    else:
                        file_result['error'] = 'File not found in this review'
                        failed_count += 1
                    
                except Exception as e:
                    file_result['error'] = str(e)
                    failed_count += 1
                
                results.append(file_result)
            
            # 如果提供了整体评论，更新到 review
            if overall_comments:
                cursor.execute("""
                    UPDATE reviews
                    SET notes = %s, updated_at = %s
                    WHERE id = %s
                """, [overall_comments, now, review_id])
            
            conn.commit()
            cursor.close()
            
            logger.info(f"Batch file approval: Review {review_id}, User {user_id}, "
                       f"Processed: {len(files)}, Success: {successful_count}, Failed: {failed_count}")
            
            return jsonify({
                'success': True,
                'message': f'Batch approval completed: {successful_count} successful, {failed_count} failed',
                'data': {
                    'review_id': review_id,
                    'review_name': review['name'],
                    'total_files': len(files),
                    'processed': len(results),
                    'successful': successful_count,
                    'failed': failed_count,
                    'results': results,
                    'user_info': user_info,
                    'overall_comments': overall_comments
                },
                'metadata': {
                    'timestamp': now.isoformat()
                }
            }), 200
            
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error in batch file approval: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
        
    except Exception as e:
        logger.error(f"Unexpected error in batch_approve_files: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}',
            'error_type': 'internal_error'
        }), 500

# Health check endpoint
@approval_bp.route('/api/approval/health', methods=['GET'])
def health_check():
    """Health check endpoint for the enhanced approval workflow"""
    try:
        # Test database connection
        conn = enhanced_approval_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'status': 'healthy',
            'service': 'Enhanced CDE Approval Workflow',
            'version': '2.0.0',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'features': [
                'comprehensive_permissions',
                'enhanced_error_handling',
                'detailed_logging',
                'workflow_progression',
                'file_level_decisions',
                'batch_file_approval',
                'urgency_tracking',
                'start_step_api',
                'submit_step_api'
            ]
        }), 200
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }), 500

if __name__ == '__main__':
    print("Enhanced CDE Approval Workflow API Module")
    logger.info("Enhanced approval workflow API initialized")
