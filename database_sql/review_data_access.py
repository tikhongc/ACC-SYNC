"""
统一审批系统数据访问层
提供完整的CRUD操作和业务逻辑
支持ACC同步数据和本地数据的统一管理
"""

import psycopg2
from psycopg2.extras import RealDictCursor, Json
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime, timezone
import uuid
import json
from contextlib import contextmanager

# Database connection configuration
def get_connection(connection_params: Optional[Dict] = None):
    """
    Get database connection using psycopg2
    
    Args:
        connection_params: Optional connection parameters
        
    Returns:
        psycopg2 connection object
    """
    if connection_params:
        return psycopg2.connect(**connection_params)
    
    # Default connection using neon_config settings
    try:
        from neon_config import neon_postgresql_config
        config = neon_postgresql_config
        
        conn_params = {
            'host': config.host,
            'port': config.port,
            'database': config.database,
            'user': config.user,
            'password': config.password,
            'sslmode': config.ssl
        }
        return psycopg2.connect(**conn_params)
    except Exception as e:
        # Fallback to environment variables or default
        import os
        return psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', 5432),
            database=os.getenv('DB_NAME', 'neondb'),
            user=os.getenv('DB_USER', 'neondb_owner'),
            password=os.getenv('DB_PASSWORD', ''),
            sslmode=os.getenv('DB_SSL', 'require')
        )


class ReviewDataAccess:
    """审批系统数据访问类"""
    
    def __init__(self, connection_params: Optional[Dict] = None):
        """
        初始化数据访问层
        
        Args:
            connection_params: 数据库连接参数，如果为None则使用默认配置
        """
        self.connection_params = connection_params
    
    def get_connection(self):
        """
        Get database connection
        
        Returns:
            psycopg2 connection object
        """
        return get_connection(self.connection_params)
    
    @contextmanager
    def get_cursor(self):
        """获取数据库游标的上下文管理器"""
        conn = get_connection(self.connection_params)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    # ========================================================================
    # 工作流管理
    # ========================================================================
    
    def create_workflow(self, workflow_data: Dict[str, Any]) -> int:
        """
        创建新工作流
        
        Args:
            workflow_data: 工作流数据字典
            
        Returns:
            创建的工作流ID
        """
        with self.get_cursor() as cursor:
            # 生成UUID
            if 'workflow_uuid' not in workflow_data:
                workflow_data['workflow_uuid'] = str(uuid.uuid4())
            
            # 设置默认值
            workflow_data.setdefault('data_source', 'local_system')
            workflow_data.setdefault('status', 'ACTIVE')
            workflow_data.setdefault('steps', [])
            workflow_data.setdefault('tags', [])
            workflow_data.setdefault('custom_fields', {})
            workflow_data.setdefault('created_by', {})
            
            # 构建插入语句
            columns = ', '.join(workflow_data.keys())
            placeholders = ', '.join(['%s'] * len(workflow_data))
            values = [Json(v) if isinstance(v, (dict, list)) else v 
                     for v in workflow_data.values()]
            
            query = f"""
                INSERT INTO workflows ({columns})
                VALUES ({placeholders})
                RETURNING id
            """
            
            cursor.execute(query, values)
            result = cursor.fetchone()
            return result['id']
    
    def get_workflow(self, workflow_id: int) -> Optional[Dict[str, Any]]:
        """获取工作流详情"""
        with self.get_cursor() as cursor:
            cursor.execute("""
                SELECT * FROM workflows WHERE id = %s
            """, (workflow_id,))
            return dict(cursor.fetchone()) if cursor.rowcount > 0 else None
    
    def get_workflow_by_uuid(self, workflow_uuid: str) -> Optional[Dict[str, Any]]:
        """通过UUID获取工作流"""
        with self.get_cursor() as cursor:
            cursor.execute("""
                SELECT * FROM workflows WHERE workflow_uuid = %s
            """, (workflow_uuid,))
            return dict(cursor.fetchone()) if cursor.rowcount > 0 else None
    
    def get_workflow_by_acc_id(self, acc_workflow_id: str) -> Optional[Dict[str, Any]]:
        """通过ACC工作流ID获取工作流"""
        with self.get_cursor() as cursor:
            cursor.execute("""
                SELECT * FROM workflows WHERE acc_workflow_id = %s
            """, (acc_workflow_id,))
            return dict(cursor.fetchone()) if cursor.rowcount > 0 else None
    
    def update_workflow(self, workflow_id: int, update_data: Dict[str, Any]) -> bool:
        """
        更新工作流
        
        Args:
            workflow_id: 工作流ID
            update_data: 要更新的数据
            
        Returns:
            是否更新成功
        """
        with self.get_cursor() as cursor:
            # 构建更新语句
            set_clause = ', '.join([f"{k} = %s" for k in update_data.keys()])
            values = [Json(v) if isinstance(v, (dict, list)) else v 
                     for v in update_data.values()]
            values.append(workflow_id)
            
            query = f"""
                UPDATE workflows 
                SET {set_clause}
                WHERE id = %s
            """
            
            cursor.execute(query, values)
            return cursor.rowcount > 0
    
    def list_workflows(
        self,
        project_id: Optional[str] = None,
        status: Optional[str] = None,
        data_source: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        列出工作流
        
        Args:
            project_id: 项目ID过滤
            status: 状态过滤
            data_source: 数据源过滤
            limit: 返回数量限制
            offset: 偏移量
            
        Returns:
            工作流列表
        """
        with self.get_cursor() as cursor:
            conditions = []
            params = []
            
            if project_id:
                conditions.append("project_id = %s")
                params.append(project_id)
            
            if status:
                conditions.append("status = %s")
                params.append(status)
            
            if data_source:
                conditions.append("data_source = %s")
                params.append(data_source)
            
            where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
            params.extend([limit, offset])
            
            query = f"""
                SELECT * FROM workflows
                {where_clause}
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s
            """
            
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def delete_workflow(self, workflow_id: int) -> bool:
        """删除工作流"""
        with self.get_cursor() as cursor:
            cursor.execute("DELETE FROM workflows WHERE id = %s", (workflow_id,))
            return cursor.rowcount > 0
    
    # ========================================================================
    # 评审管理
    # ========================================================================
    
    def create_review(self, review_data: Dict[str, Any]) -> int:
        """创建新评审"""
        with self.get_cursor() as cursor:
            # 生成UUID
            if 'review_uuid' not in review_data:
                review_data['review_uuid'] = str(uuid.uuid4())
            
            # 设置默认值
            review_data.setdefault('data_source', 'local_system')
            review_data.setdefault('status', 'DRAFT')
            review_data.setdefault('priority', 3)
            review_data.setdefault('tags', [])
            review_data.setdefault('custom_fields', {})
            review_data.setdefault('created_by', {})
            review_data.setdefault('assigned_to', [])
            review_data.setdefault('notes', None)
            
            # 构建插入语句
            columns = ', '.join(review_data.keys())
            placeholders = ', '.join(['%s'] * len(review_data))
            values = [Json(v) if isinstance(v, (dict, list)) else v 
                     for v in review_data.values()]
            
            query = f"""
                INSERT INTO reviews ({columns})
                VALUES ({placeholders})
                RETURNING id
            """
            
            cursor.execute(query, values)
            result = cursor.fetchone()
            return result['id']
    
    def create_review_from_workflow(
        self,
        workflow_id: int,
        review_name: str,
        created_by_user_id: str,
        created_by_user_name: str
    ) -> int:
        """从工作流创建评审（使用数据库函数）"""
        with self.get_cursor() as cursor:
            cursor.execute("""
                SELECT create_review_from_workflow(%s, %s, %s, %s)
            """, (workflow_id, review_name, created_by_user_id, created_by_user_name))
            result = cursor.fetchone()
            return result['create_review_from_workflow']
    
    def get_review(self, review_id: int) -> Optional[Dict[str, Any]]:
        """获取评审详情"""
        with self.get_cursor() as cursor:
            cursor.execute("""
                SELECT * FROM reviews WHERE id = %s
            """, (review_id,))
            return dict(cursor.fetchone()) if cursor.rowcount > 0 else None
    
    def get_review_by_uuid(self, review_uuid: str) -> Optional[Dict[str, Any]]:
        """通过UUID获取评审"""
        with self.get_cursor() as cursor:
            cursor.execute("""
                SELECT * FROM reviews WHERE review_uuid = %s
            """, (review_uuid,))
            return dict(cursor.fetchone()) if cursor.rowcount > 0 else None
    
    def get_review_by_acc_id(self, acc_review_id: str) -> Optional[Dict[str, Any]]:
        """通过ACC评审ID获取评审"""
        with self.get_cursor() as cursor:
            cursor.execute("""
                SELECT * FROM reviews WHERE acc_review_id = %s
            """, (acc_review_id,))
            return dict(cursor.fetchone()) if cursor.rowcount > 0 else None
    
    def update_review(self, review_id: int, update_data: Dict[str, Any]) -> bool:
        """更新评审"""
        with self.get_cursor() as cursor:
            set_clause = ', '.join([f"{k} = %s" for k in update_data.keys()])
            values = [Json(v) if isinstance(v, (dict, list)) else v 
                     for v in update_data.values()]
            values.append(review_id)
            
            query = f"""
                UPDATE reviews 
                SET {set_clause}
                WHERE id = %s
            """
            
            cursor.execute(query, values)
            return cursor.rowcount > 0
    
    def list_reviews(
        self,
        project_id: Optional[str] = None,
        workflow_id: Optional[int] = None,
        status: Optional[str] = None,
        priority: Optional[int] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """列出评审"""
        with self.get_cursor() as cursor:
            conditions = []
            params = []
            
            if project_id:
                conditions.append("project_id = %s")
                params.append(project_id)
            
            if workflow_id:
                conditions.append("workflow_id = %s")
                params.append(workflow_id)
            
            if status:
                conditions.append("status = %s")
                params.append(status)
            
            if priority:
                conditions.append("priority = %s")
                params.append(priority)
            
            where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
            params.extend([limit, offset])
            
            query = f"""
                SELECT * FROM reviews_overview
                {where_clause}
                ORDER BY priority, created_at DESC
                LIMIT %s OFFSET %s
            """
            
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def delete_review(self, review_id: int) -> bool:
        """删除评审"""
        with self.get_cursor() as cursor:
            cursor.execute("DELETE FROM reviews WHERE id = %s", (review_id,))
            return cursor.rowcount > 0
    
    # ========================================================================
    # 文件版本管理
    # ========================================================================
    
    def add_file_to_review(self, file_data: Dict[str, Any]) -> int:
        """添加文件到评审"""
        with self.get_cursor() as cursor:
            file_data.setdefault('approval_status', 'PENDING')
            file_data.setdefault('tags', [])
            file_data.setdefault('custom_attributes', [])
            file_data.setdefault('approval_history', [])
            
            columns = ', '.join(file_data.keys())
            placeholders = ', '.join(['%s'] * len(file_data))
            values = [Json(v) if isinstance(v, (dict, list)) else v 
                     for v in file_data.values()]
            
            query = f"""
                INSERT INTO review_file_versions ({columns})
                VALUES ({placeholders})
                RETURNING id
            """
            
            cursor.execute(query, values)
            result = cursor.fetchone()
            return result['id']
    
    def update_file_approval_status(
        self,
        file_version_id: int,
        approval_status: str,
        approval_comments: Optional[str] = None,
        approval_status_id: Optional[str] = None,
        approval_status_value: Optional[str] = None,
        approval_label: Optional[str] = None
    ) -> bool:
        """更新文件审批状态"""
        with self.get_cursor() as cursor:
            cursor.execute("""
                UPDATE review_file_versions
                SET approval_status = %s,
                    approval_comments = %s,
                    approval_status_id = %s,
                    approval_status_value = %s,
                    approval_label = %s,
                    approved_at = CASE WHEN %s = 'APPROVED' THEN CURRENT_TIMESTAMP ELSE approved_at END
                WHERE id = %s
            """, (approval_status, approval_comments, approval_status_id, 
                  approval_status_value, approval_label, approval_status, file_version_id))
            return cursor.rowcount > 0
    
    def get_review_files(self, review_id: int) -> List[Dict[str, Any]]:
        """获取评审的所有文件"""
        with self.get_cursor() as cursor:
            cursor.execute("""
                SELECT * FROM review_file_versions
                WHERE review_id = %s
                ORDER BY created_at DESC
            """, (review_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def batch_insert_review_files(self, files_data: List[Dict[str, Any]]) -> int:
        """
        批量插入评审文件版本
        
        Args:
            files_data: 文件数据列表
            
        Returns:
            插入的记录数
        """
        if not files_data:
            return 0
        
        with self.get_cursor() as cursor:
            # 设置默认值
            for file_data in files_data:
                file_data.setdefault('approval_status', 'PENDING')
                file_data.setdefault('tags', [])
                file_data.setdefault('custom_attributes', [])
                file_data.setdefault('approval_history', [])
            
            # 获取所有字段名（使用第一条记录的字段）
            columns = list(files_data[0].keys())
            columns_str = ', '.join(columns)
            
            # 构建批量插入语句
            placeholders = ', '.join(['%s'] * len(columns))
            values_template = f"({placeholders})"
            
            # 准备所有值
            all_values = []
            for file_data in files_data:
                row_values = [
                    Json(file_data[col]) if isinstance(file_data[col], (dict, list)) else file_data[col]
                    for col in columns
                ]
                all_values.extend(row_values)
            
            # 构建完整的INSERT语句
            values_clause = ', '.join([values_template] * len(files_data))
            query = f"""
                INSERT INTO review_file_versions ({columns_str})
                VALUES {values_clause}
                ON CONFLICT (review_id, file_version_urn) DO NOTHING
            """
            
            cursor.execute(query, all_values)
            return cursor.rowcount
    
    # ========================================================================
    # 进度管理
    # ========================================================================
    
    def add_review_step(self, step_data: Dict[str, Any]) -> int:
        """添加评审步骤"""
        with self.get_cursor() as cursor:
            step_data.setdefault('status', 'PENDING')
            step_data.setdefault('assigned_to', [])
            step_data.setdefault('attachments', [])
            step_data.setdefault('action_by', {})
            step_data.setdefault('notes', None)
            
            columns = ', '.join(step_data.keys())
            placeholders = ', '.join(['%s'] * len(step_data))
            values = [Json(v) if isinstance(v, (dict, list)) else v 
                     for v in step_data.values()]
            
            query = f"""
                INSERT INTO review_progress ({columns})
                VALUES ({placeholders})
                RETURNING id
            """
            
            cursor.execute(query, values)
            result = cursor.fetchone()
            return result['id']
    
    def update_step_status(
        self,
        step_id: int,
        status: str,
        decision: Optional[str] = None,
        comments: Optional[str] = None,
        completed_by: Optional[Dict] = None,
        action_by: Optional[Dict] = None,
        end_time: Optional[datetime] = None
    ) -> bool:
        """更新步骤状态"""
        with self.get_cursor() as cursor:
            cursor.execute("""
                UPDATE review_progress
                SET status = %s,
                    decision = %s,
                    comments = %s,
                    completed_by = %s,
                    action_by = %s,
                    end_time = %s,
                    completed_at = CASE WHEN %s IN ('APPROVED', 'REJECTED', 'SUBMITTED') 
                                   THEN CURRENT_TIMESTAMP ELSE completed_at END
                WHERE id = %s
            """, (status, decision, comments, 
                  Json(completed_by) if completed_by else None,
                  Json(action_by) if action_by else None,
                  end_time,
                  status, step_id))
            return cursor.rowcount > 0
    
    def get_review_progress(self, review_id: int) -> List[Dict[str, Any]]:
        """获取评审进度"""
        with self.get_cursor() as cursor:
            cursor.execute("""
                SELECT * FROM review_progress
                WHERE review_id = %s
                ORDER BY step_order
            """, (review_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def batch_insert_review_steps(self, steps_data: List[Dict[str, Any]]) -> int:
        """
        批量插入评审步骤

        Args:
            steps_data: 步骤数据列表

        Returns:
            插入的记录数
        """
        print(f"[DEBUG] ReviewDataAccess.batch_insert_review_steps called with {len(steps_data)} steps")
        if not steps_data:
            return 0

        with self.get_cursor() as cursor:
            # 设置默认值
            for step_data in steps_data:
                step_data.setdefault('status', 'PENDING')
                step_data.setdefault('assigned_to', [])
                step_data.setdefault('attachments', [])
                step_data.setdefault('action_by', {})
                step_data.setdefault('notes', None)
            
            # 获取所有字段名
            columns = list(steps_data[0].keys())
            columns_str = ', '.join(columns)
            
            # 构建批量插入语句
            placeholders = ', '.join(['%s'] * len(columns))
            values_template = f"({placeholders})"
            
            # 准备所有值
            all_values = []
            for step_data in steps_data:
                row_values = [
                    Json(step_data[col]) if isinstance(step_data[col], (dict, list)) else step_data[col]
                    for col in columns
                ]
                all_values.extend(row_values)
            
            # 构建完整的INSERT语句
            values_clause = ', '.join([values_template] * len(steps_data))
            query = f"""
                INSERT INTO review_progress ({columns_str})
                VALUES {values_clause}
                ON CONFLICT (review_id, step_id)
                WHERE status NOT IN ('SENT_BACK', 'COMPLETED')
                DO NOTHING
            """

            # DEBUG: Print SQL and first step data
            print(f"[DEBUG] SQL (first 300 chars): {query[:300]}...")
            if steps_data:
                first_step = steps_data[0]
                print(f"[DEBUG] First step data: review_id={first_step.get('review_id')}, step_id={first_step.get('step_id')}, status={first_step.get('status')}")

            cursor.execute(query, all_values)
            inserted_count = cursor.rowcount
            print(f"[DEBUG] Inserted {inserted_count} rows")
            return inserted_count
    
    def batch_insert_file_approval_history(self, approval_data: List[Dict[str, Any]]) -> int:
        """
        批量插入文件审批历史
        
        Args:
            approval_data: 审批历史数据列表
            
        Returns:
            插入的记录数
        """
        if not approval_data:
            return 0
        
        with self.get_cursor() as cursor:
            # 设置默认值
            for record in approval_data:
                record.setdefault('approved_by', {})
                record.setdefault('is_current', False)
                record.setdefault('is_latest_in_review', False)
            
            # 获取所有字段名
            columns = list(approval_data[0].keys())
            columns_str = ', '.join(columns)
            
            # 构建批量插入语句
            placeholders = ', '.join(['%s'] * len(columns))
            values_template = f"({placeholders})"
            
            # 准备所有值
            all_values = []
            for record in approval_data:
                row_values = [
                    Json(record[col]) if isinstance(record[col], (dict, list)) else record[col]
                    for col in columns
                ]
                all_values.extend(row_values)
            
            # 构建完整的INSERT语句
            values_clause = ', '.join([values_template] * len(approval_data))
            query = f"""
                INSERT INTO file_approval_history ({columns_str})
                VALUES {values_clause}
                ON CONFLICT (file_version_urn, review_acc_id, approval_status_id) 
                DO UPDATE SET
                    review_status = EXCLUDED.review_status,
                    is_current = EXCLUDED.is_current,
                    synced_at = CURRENT_TIMESTAMP
            """
            
            cursor.execute(query, all_values)
            return cursor.rowcount
    
    def get_user_pending_tasks(self, user_id: str) -> List[Dict[str, Any]]:
        """获取用户待处理任务"""
        with self.get_cursor() as cursor:
            cursor.execute("""
                SELECT * FROM get_user_pending_tasks(%s)
            """, (user_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    # ========================================================================
    # 评论管理
    # ========================================================================
    
    def add_comment(self, comment_data: Dict[str, Any]) -> int:
        """添加评论"""
        with self.get_cursor() as cursor:
            comment_data.setdefault('comment_type', 'general')
            comment_data.setdefault('status', 'active')
            comment_data.setdefault('is_private', False)
            comment_data.setdefault('tags', [])
            comment_data.setdefault('attachments', [])
            
            columns = ', '.join(comment_data.keys())
            placeholders = ', '.join(['%s'] * len(comment_data))
            values = [Json(v) if isinstance(v, (dict, list)) else v 
                     for v in comment_data.values()]
            
            query = f"""
                INSERT INTO review_comments ({columns})
                VALUES ({placeholders})
                RETURNING id
            """
            
            cursor.execute(query, values)
            result = cursor.fetchone()
            return result['id']
    
    def get_review_comments(
        self,
        review_id: int,
        file_version_id: Optional[int] = None,
        include_resolved: bool = True
    ) -> List[Dict[str, Any]]:
        """获取评审评论"""
        with self.get_cursor() as cursor:
            conditions = ["review_id = %s"]
            params = [review_id]
            
            if file_version_id:
                conditions.append("file_version_id = %s")
                params.append(file_version_id)
            
            if not include_resolved:
                conditions.append("status != 'resolved'")
            
            where_clause = ' AND '.join(conditions)
            
            cursor.execute(f"""
                SELECT * FROM review_comments
                WHERE {where_clause}
                ORDER BY created_at DESC
            """, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def resolve_comment(self, comment_id: int, resolved_by: Dict[str, Any]) -> bool:
        """解决评论"""
        with self.get_cursor() as cursor:
            cursor.execute("""
                UPDATE review_comments
                SET status = 'resolved',
                    resolved_at = CURRENT_TIMESTAMP,
                    resolved_by = %s
                WHERE id = %s
            """, (Json(resolved_by), comment_id))
            return cursor.rowcount > 0
    
    # ========================================================================
    # 决策管理
    # ========================================================================
    
    def add_approval_decision(self, decision_data: Dict[str, Any]) -> int:
        """添加审批决策"""
        with self.get_cursor() as cursor:
            decision_data.setdefault('attachments', [])
            decision_data.setdefault('custom_fields', {})
            
            columns = ', '.join(decision_data.keys())
            placeholders = ', '.join(['%s'] * len(decision_data))
            values = [Json(v) if isinstance(v, (dict, list)) else v 
                     for v in decision_data.values()]
            
            query = f"""
                INSERT INTO approval_decisions ({columns})
                VALUES ({placeholders})
                RETURNING id
            """
            
            cursor.execute(query, values)
            result = cursor.fetchone()
            return result['id']
    
    def get_review_decisions(self, review_id: int) -> List[Dict[str, Any]]:
        """获取评审决策"""
        with self.get_cursor() as cursor:
            cursor.execute("""
                SELECT * FROM approval_decisions
                WHERE review_id = %s
                ORDER BY decided_at DESC
            """, (review_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    # ========================================================================
    # 通知管理
    # ========================================================================
    
    def create_notification(self, notification_data: Dict[str, Any]) -> int:
        """创建通知"""
        with self.get_cursor() as cursor:
            notification_data.setdefault('is_read', False)
            notification_data.setdefault('is_sent', False)
            notification_data.setdefault('delivery_method', 'system')
            notification_data.setdefault('priority', 3)
            
            columns = ', '.join(notification_data.keys())
            placeholders = ', '.join(['%s'] * len(notification_data))
            values = [Json(v) if isinstance(v, (dict, list)) else v 
                     for v in notification_data.values()]
            
            query = f"""
                INSERT INTO review_notifications ({columns})
                VALUES ({placeholders})
                RETURNING id
            """
            
            cursor.execute(query, values)
            result = cursor.fetchone()
            return result['id']
    
    def get_user_notifications(
        self,
        user_id: str,
        unread_only: bool = False,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """获取用户通知"""
        with self.get_cursor() as cursor:
            unread_filter = "AND is_read = FALSE" if unread_only else ""
            
            cursor.execute(f"""
                SELECT * FROM review_notifications
                WHERE recipient->>'user_id' = %s
                {unread_filter}
                ORDER BY created_at DESC
                LIMIT %s
            """, (user_id, limit))
            return [dict(row) for row in cursor.fetchall()]
    
    def mark_notification_read(self, notification_id: int) -> bool:
        """标记通知为已读"""
        with self.get_cursor() as cursor:
            cursor.execute("""
                UPDATE review_notifications
                SET is_read = TRUE,
                    read_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (notification_id,))
            return cursor.rowcount > 0
    
    # ========================================================================
    # 模板管理
    # ========================================================================
    
    def create_workflow_template(self, template_data: Dict[str, Any]) -> int:
        """创建工作流模板"""
        with self.get_cursor() as cursor:
            if 'template_uuid' not in template_data:
                template_data['template_uuid'] = str(uuid.uuid4())
            
            template_data.setdefault('is_active', True)
            template_data.setdefault('is_public', False)
            template_data.setdefault('usage_count', 0)
            
            columns = ', '.join(template_data.keys())
            placeholders = ', '.join(['%s'] * len(template_data))
            values = [Json(v) if isinstance(v, (dict, list)) else v 
                     for v in template_data.values()]
            
            query = f"""
                INSERT INTO workflow_templates ({columns})
                VALUES ({placeholders})
                RETURNING id
            """
            
            cursor.execute(query, values)
            result = cursor.fetchone()
            return result['id']
    
    def get_workflow_templates(
        self,
        category: Optional[str] = None,
        active_only: bool = True
    ) -> List[Dict[str, Any]]:
        """获取工作流模板列表"""
        with self.get_cursor() as cursor:
            conditions = []
            params = []
            
            if category:
                conditions.append("category = %s")
                params.append(category)
            
            if active_only:
                conditions.append("is_active = TRUE")
            
            where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
            
            cursor.execute(f"""
                SELECT * FROM workflow_templates
                {where_clause}
                ORDER BY usage_count DESC, created_at DESC
            """, params)
            return [dict(row) for row in cursor.fetchall()]
    
    # ========================================================================
    # 统计和报表
    # ========================================================================
    
    def get_workflow_statistics(self, workflow_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """获取工作流统计"""
        with self.get_cursor() as cursor:
            where_clause = "WHERE id = %s" if workflow_id else ""
            params = [workflow_id] if workflow_id else []
            
            cursor.execute(f"""
                SELECT * FROM workflow_statistics
                {where_clause}
            """, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_review_activity_stats(self, review_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """获取评审活动统计"""
        with self.get_cursor() as cursor:
            where_clause = "WHERE review_id = %s" if review_id else ""
            params = [review_id] if review_id else []
            
            cursor.execute(f"""
                SELECT * FROM review_activity_stats
                {where_clause}
            """, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_pending_tasks_summary(self) -> Dict[str, Any]:
        """获取待处理任务摘要"""
        with self.get_cursor() as cursor:
            cursor.execute("""
                SELECT
                    COUNT(*) as total_tasks,
                    COUNT(*) FILTER (WHERE is_overdue) as overdue_tasks,
                    COUNT(*) FILTER (WHERE urgency_level = '紧急') as urgent_tasks,
                    COUNT(*) FILTER (WHERE urgency_level = '即将到期') as due_soon_tasks
                FROM pending_tasks_view
            """)
            return dict(cursor.fetchone())

    def get_review_progress_by_template_step(self, review_id: int, template_step_id: str) -> Dict[str, Any]:
        """
        根據 review_id 和 template_step_id 查詢 progress 記錄

        Args:
            review_id: 評審ID
            template_step_id: 模板步驟ID

        Returns:
            進度記錄字典，如果不存在則返回 None
        """
        with self.get_cursor() as cursor:
            cursor.execute("""
                SELECT *
                FROM review_progress
                WHERE review_id = %s AND template_step_id = %s
                LIMIT 1
            """, (review_id, template_step_id))

            result = cursor.fetchone()
            return dict(result) if result else None


# ============================================================================
# 便捷函数
# ============================================================================

def get_review_data_access(connection_params: Optional[Dict] = None) -> ReviewDataAccess:
    """获取ReviewDataAccess实例"""
    return ReviewDataAccess(connection_params)


if __name__ == "__main__":
    # 测试代码
    print("审批系统数据访问层测试")
    print("=" * 60)
    
    try:
        da = get_review_data_access()
        
        # 测试连接
        with da.get_cursor() as cursor:
            cursor.execute("SELECT version()")
            version = cursor.fetchone()
            print(f"✓ 数据库连接成功")
            print(f"  版本: {version['version']}")
        
        print("\n数据访问层初始化成功！")
        
    except Exception as e:
        print(f"✗ 错误: {e}")
        import traceback
        traceback.print_exc()

