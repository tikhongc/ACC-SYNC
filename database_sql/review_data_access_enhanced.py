"""
增强的审批系统数据访问层
扩展原有的ReviewDataAccess，添加批量UPSERT支持
"""

from typing import List, Dict, Any, Tuple
from psycopg2.extras import Json
from review_data_access import ReviewDataAccess


class EnhancedReviewDataAccess(ReviewDataAccess):
    """增强的审批系统数据访问类 - 支持批量UPSERT"""
    
    def batch_upsert_workflows(self, workflows_data: List[Dict[str, Any]]) -> Tuple[int, int]:
        """
        批量UPSERT工作流（使用PostgreSQL的ON CONFLICT）
        
        Args:
            workflows_data: 工作流数据列表
            
        Returns:
            (插入数量, 更新数量)
        """
        if not workflows_data:
            return 0, 0
        
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                inserted = 0
                updated = 0
                
                for workflow_data in workflows_data:
                    # 设置默认值
                    workflow_data.setdefault('additional_options', {})
                    workflow_data.setdefault('approval_status_options', [])
                    workflow_data.setdefault('copy_files_options', {})
                    workflow_data.setdefault('attached_attributes', [])
                    workflow_data.setdefault('update_attributes_options', {})
                    workflow_data.setdefault('steps', [])
                    workflow_data.setdefault('created_by', {})
                    
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
                    
                    # 转换JSON字段
                    params = workflow_data.copy()
                    for json_field in ['additional_options', 'approval_status_options', 'copy_files_options',
                                      'attached_attributes', 'update_attributes_options', 'steps', 'created_by']:
                        if json_field in params and isinstance(params[json_field], (dict, list)):
                            params[json_field] = Json(params[json_field])
                    
                    cursor.execute(sql, params)
                    result = cursor.fetchone()
                    
                    if result:
                        if result[1]:  # inserted
                            inserted += 1
                        else:
                            updated += 1
                
                conn.commit()
                return inserted, updated
    
    def batch_upsert_reviews(self, reviews_data: List[Dict[str, Any]]) -> Tuple[int, int]:
        """
        批量UPSERT评审
        
        Args:
            reviews_data: 评审数据列表
            
        Returns:
            (插入数量, 更新数量)
        """
        if not reviews_data:
            return 0, 0
        
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                inserted = 0
                updated = 0
                
                for review_data in reviews_data:
                    # 设置默认值
                    review_data.setdefault('created_by', {})
                    review_data.setdefault('assigned_to', [])
                    review_data.setdefault('next_action_by', {})
                    review_data.setdefault('archived', False)
                    review_data.setdefault('archived_by', {})
                    
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
                        ON CONFLICT (acc_review_id)
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
                    
                    # 转换JSON字段
                    params = review_data.copy()
                    for json_field in ['created_by', 'assigned_to', 'next_action_by', 'archived_by']:
                        if json_field in params and isinstance(params[json_field], (dict, list)):
                            params[json_field] = Json(params[json_field])
                    
                    cursor.execute(sql, params)
                    result = cursor.fetchone()
                    
                    if result:
                        if result[1]:  # inserted
                            inserted += 1
                        else:
                            updated += 1
                
                conn.commit()
                return inserted, updated
    
    def batch_upsert_review_files(self, files_data: List[Dict[str, Any]]) -> Tuple[int, int]:
        """
        批量UPSERT评审文件版本
        
        Args:
            files_data: 文件数据列表
            
        Returns:
            (插入数量, 更新数量)
        """
        if not files_data:
            return 0, 0
        
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                inserted = 0
                updated = 0
                
                for file_data in files_data:
                    # 设置默认值
                    file_data.setdefault('approval_status', 'PENDING')
                    file_data.setdefault('tags', [])
                    file_data.setdefault('custom_attributes', [])
                    file_data.setdefault('approval_history', [])
                    file_data.setdefault('review_content', {})
                    
                    sql = """
                        INSERT INTO review_file_versions (
                            review_id, file_urn, file_name, file_size, file_extension, file_path,
                            version_number, version_urn, item_urn, approval_status, approval_status_id,
                            approval_status_value, approval_label, approval_comments, review_content,
                            custom_attributes, copied_file_version_urn, tags, approval_history
                        )
                        VALUES (
                            %(review_id)s, %(file_urn)s, %(file_name)s, %(file_size)s, %(file_extension)s, %(file_path)s,
                            %(version_number)s, %(version_urn)s, %(item_urn)s, %(approval_status)s, %(approval_status_id)s,
                            %(approval_status_value)s, %(approval_label)s, %(approval_comments)s, %(review_content)s,
                            %(custom_attributes)s, %(copied_file_version_urn)s, %(tags)s, %(approval_history)s
                        )
                        ON CONFLICT (review_id, file_urn)
                        DO UPDATE SET
                            file_name = EXCLUDED.file_name,
                            file_size = EXCLUDED.file_size,
                            file_extension = EXCLUDED.file_extension,
                            file_path = EXCLUDED.file_path,
                            version_number = EXCLUDED.version_number,
                            version_urn = EXCLUDED.version_urn,
                            item_urn = EXCLUDED.item_urn,
                            approval_status = EXCLUDED.approval_status,
                            approval_status_id = EXCLUDED.approval_status_id,
                            approval_status_value = EXCLUDED.approval_status_value,
                            approval_label = EXCLUDED.approval_label,
                            approval_comments = EXCLUDED.approval_comments,
                            review_content = EXCLUDED.review_content,
                            custom_attributes = EXCLUDED.custom_attributes,
                            copied_file_version_urn = EXCLUDED.copied_file_version_urn,
                            tags = EXCLUDED.tags,
                            approval_history = EXCLUDED.approval_history,
                            updated_at = CURRENT_TIMESTAMP
                        RETURNING id, (xmax = 0) AS inserted
                    """
                    
                    # 转换JSON字段
                    params = file_data.copy()
                    for json_field in ['tags', 'custom_attributes', 'approval_history', 'review_content']:
                        if json_field in params and isinstance(params[json_field], (dict, list)):
                            params[json_field] = Json(params[json_field])
                    
                    cursor.execute(sql, params)
                    result = cursor.fetchone()
                    
                    if result:
                        if result[1]:  # inserted
                            inserted += 1
                        else:
                            updated += 1
                
                conn.commit()
                return inserted, updated
    
    def batch_upsert_review_steps(self, steps_data: List[Dict[str, Any]]) -> Tuple[int, int]:
        """
        批量UPSERT评审进度步骤
        
        Args:
            steps_data: 步骤数据列表
            
        Returns:
            (插入数量, 更新数量)
        """
        if not steps_data:
            return 0, 0
        
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                inserted = 0
                updated = 0
                
                for step_data in steps_data:
                    # 设置默认值
                    step_data.setdefault('assigned_to', [])
                    step_data.setdefault('claimed_by', {})
                    step_data.setdefault('completed_by', {})
                    step_data.setdefault('action_by', {})
                    step_data.setdefault('candidates', {})
                    
                    sql = """
                        INSERT INTO review_progress (
                            review_id, step_id, template_step_id, step_name, step_type, step_order, status,
                            assigned_to, claimed_by, completed_by, action_by, candidates,
                            decision, comments, notes, due_date, started_at, completed_at, end_time
                        )
                        VALUES (
                            %(review_id)s, %(step_id)s, %(template_step_id)s, %(step_name)s, %(step_type)s, %(step_order)s, %(status)s,
                            %(assigned_to)s, %(claimed_by)s, %(completed_by)s, %(action_by)s, %(candidates)s,
                            %(decision)s, %(comments)s, %(notes)s, %(due_date)s, %(started_at)s, %(completed_at)s, %(end_time)s
                        )
                        ON CONFLICT (review_id, step_id)
                        WHERE status NOT IN ('SENT_BACK', 'COMPLETED')
                        DO UPDATE SET
                            template_step_id = EXCLUDED.template_step_id,
                            step_name = EXCLUDED.step_name,
                            step_type = EXCLUDED.step_type,
                            step_order = EXCLUDED.step_order,
                            status = EXCLUDED.status,
                            assigned_to = EXCLUDED.assigned_to,
                            claimed_by = EXCLUDED.claimed_by,
                            completed_by = EXCLUDED.completed_by,
                            action_by = EXCLUDED.action_by,
                            candidates = EXCLUDED.candidates,
                            decision = EXCLUDED.decision,
                            comments = EXCLUDED.comments,
                            notes = EXCLUDED.notes,
                            due_date = EXCLUDED.due_date,
                            started_at = EXCLUDED.started_at,
                            completed_at = EXCLUDED.completed_at,
                            end_time = EXCLUDED.end_time,
                            updated_at = CURRENT_TIMESTAMP
                        RETURNING id, (xmax = 0) AS inserted
                    """
                    
                    # 转换JSON字段
                    params = step_data.copy()
                    for json_field in ['assigned_to', 'claimed_by', 'completed_by', 'action_by', 'candidates']:
                        if json_field in params and isinstance(params[json_field], (dict, list)):
                            params[json_field] = Json(params[json_field])

                    # DEBUG: Print SQL and params for first step
                    if inserted + updated == 0:
                        print(f"[DEBUG] First step SQL: {sql[:200]}...")
                        print(f"[DEBUG] Step data: review_id={params.get('review_id')}, step_id={params.get('step_id')}, status={params.get('status')}")

                    cursor.execute(sql, params)
                    result = cursor.fetchone()
                    
                    if result:
                        if result[1]:  # inserted
                            inserted += 1
                        else:
                            updated += 1
                
                conn.commit()
                return inserted, updated

    def get_review_progress_by_template_step(self, review_id: int, template_step_id: str) -> Dict[str, Any]:
        """
        根據 review_id 和 template_step_id 查詢 progress 記錄

        Args:
            review_id: 評審ID
            template_step_id: 模板步驟ID

        Returns:
            進度記錄字典，如果不存在則返回 None
        """
        sql = """
            SELECT *
            FROM review_progress
            WHERE review_id = %s AND template_step_id = %s
            LIMIT 1
        """

        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql, (review_id, template_step_id))
                result = cursor.fetchone()

                if result:
                    columns = [desc[0] for desc in cursor.description]
                    return dict(zip(columns, result))

                return None


# 便捷函数
def get_enhanced_data_access(connection_params=None) -> EnhancedReviewDataAccess:
    """获取增强的数据访问实例"""
    return EnhancedReviewDataAccess(connection_params)

