# -*- coding: utf-8 -*-
"""
步骤进度管理API模块
实现步骤进度管理，包括状态转换和候选人操作
"""

import json
from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from typing import Dict, List, Optional, Any
import utils

# 添加数据库访问
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../database_sql'))
from neon_config import NeonConfig
import psycopg2
import psycopg2.extras

step_progress_bp = Blueprint('step_progress', __name__)

class StepProgressManager:
    """步骤进度管理器"""
    
    def __init__(self):
        """初始化步骤进度管理器"""
        self.neon_config = NeonConfig()
        self.db_params = self.neon_config.get_db_params()
    
    def get_connection(self):
        """获取数据库连接"""
        return psycopg2.connect(**self.db_params)
    
    def claim_step(self, review_id: int, step_id: str, user_info: Dict[str, Any]) -> bool:
        """
        认领步骤
        
        Args:
            review_id: 评审ID
            step_id: 步骤ID
            user_info: 用户信息 {"autodeskId": "xxx", "name": "xxx"}
            
        Returns:
            是否成功
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 检查步骤状态
            cursor.execute("""
                SELECT status, step_order FROM review_progress 
                WHERE review_id = %s AND step_id = %s
            """, [review_id, step_id])
            
            result = cursor.fetchone()
            if not result:
                raise ValueError("步骤不存在")
            
            status, step_order = result
            
            if status not in ['PENDING', 'UNCLAIMED']:
                raise ValueError(f"步骤状态不允许认领: {status}")
            
            # 更新步骤状态
            now = datetime.now(timezone.utc)
            cursor.execute("""
                UPDATE review_progress 
                SET status = 'CLAIMED',
                    claimed_by = %s,
                    started_at = %s,
                    updated_at = %s
                WHERE review_id = %s AND step_id = %s
            """, [
                json.dumps(user_info),
                now,
                now,
                review_id,
                step_id
            ])
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"✗ 认领步骤失败: {str(e)}")
            return False
            
        finally:
            if conn:
                conn.close()
    
    def submit_step(
        self, 
        review_id: int, 
        step_id: str, 
        submission_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        提交步骤
        
        Args:
            review_id: 评审ID
            step_id: 步骤ID
            submission_data: 提交数据
            {
                "decision": "APPROVED" | "REJECTED",
                "comments": "评论",
                "conditions": "条件",
                "user_info": {"autodeskId": "xxx", "name": "xxx"},
                "file_approvals": [
                    {
                        "file_version_id": 123,
                        "approval_status": "APPROVED",
                        "comments": "文件评论"
                    }
                ]
            }
            
        Returns:
            提交结果
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 检查步骤状态
            cursor.execute("""
                SELECT status, step_order, step_type FROM review_progress 
                WHERE review_id = %s AND step_id = %s
            """, [review_id, step_id])
            
            result = cursor.fetchone()
            if not result:
                raise ValueError("步骤不存在")
            
            status, step_order, step_type = result
            
            if status not in ['CLAIMED']:
                raise ValueError(f"步骤状态不允许提交: {status}")
            
            decision = submission_data.get('decision')
            user_info = submission_data.get('user_info', {})
            now = datetime.now(timezone.utc)
            
            # 更新步骤状态
            cursor.execute("""
                UPDATE review_progress 
                SET status = 'SUBMITTED',
                    decision = %s,
                    comments = %s,
                    conditions = %s,
                    completed_by = %s,
                    completed_at = %s,
                    updated_at = %s
                WHERE review_id = %s AND step_id = %s
            """, [
                decision,
                submission_data.get('comments'),
                submission_data.get('conditions'),
                json.dumps(user_info),
                now,
                now,
                review_id,
                step_id
            ])
            
            # 处理文件审批
            file_approvals = submission_data.get('file_approvals', [])
            files_processed = 0
            
            for file_approval in file_approvals:
                self._update_file_approval(
                    cursor, 
                    file_approval['file_version_id'],
                    file_approval.get('approval_status', decision),
                    file_approval.get('comments'),
                    user_info
                )
                files_processed += 1
            
            # 创建审批决策记录
            self._create_approval_decision(
                cursor, review_id, step_id, submission_data
            )
            
            # 检查是否需要进入下一步骤
            next_step_activated = self._check_and_activate_next_step(
                cursor, review_id, step_order, decision
            )
            
            conn.commit()
            
            return {
                'step_submitted': True,
                'files_processed': files_processed,
                'next_step_activated': next_step_activated,
                'decision': decision
            }
            
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"✗ 提交步骤失败: {str(e)}")
            raise
            
        finally:
            if conn:
                conn.close()
    
    def _update_file_approval(
        self, 
        cursor, 
        file_version_id: int, 
        approval_status: str,
        comments: str,
        user_info: Dict
    ):
        """更新文件审批状态"""
        cursor.execute("""
            UPDATE review_file_versions 
            SET approval_status = %s,
                approval_comments = %s,
                approved_at = %s,
                updated_at = %s
            WHERE id = %s
        """, [
            approval_status,
            comments,
            datetime.now(timezone.utc) if approval_status in ['APPROVED', 'REJECTED'] else None,
            datetime.now(timezone.utc),
            file_version_id
        ])
    
    def _create_approval_decision(
        self, 
        cursor, 
        review_id: int, 
        step_id: str, 
        submission_data: Dict
    ):
        """创建审批决策记录"""
        cursor.execute("""
            INSERT INTO approval_decisions (
                review_id, step_id, decision, decision_reason,
                conditions, recommendations, decided_by,
                comments, decided_at, created_at, updated_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """, [
            review_id,
            step_id,
            submission_data.get('decision'),
            submission_data.get('decision_reason'),
            submission_data.get('conditions'),
            submission_data.get('recommendations'),
            json.dumps(submission_data.get('user_info', {})),
            submission_data.get('comments'),
            datetime.now(timezone.utc),
            datetime.now(timezone.utc),
            datetime.now(timezone.utc)
        ])
    
    def _check_and_activate_next_step(
        self, 
        cursor, 
        review_id: int, 
        current_step_order: int,
        decision: str
    ) -> bool:
        """检查并激活下一步骤"""
        # 如果当前步骤被拒绝，评审可能需要回到发起人
        if decision == 'REJECTED':
            # 检查是否启用了"sent back to initiator"
            # 这里简化处理，直接结束评审
            cursor.execute("""
                UPDATE reviews 
                SET status = 'CLOSED', 
                    finished_at = %s,
                    updated_at = %s
                WHERE id = %s
            """, [datetime.now(timezone.utc), datetime.now(timezone.utc), review_id])
            return False
        
        # 查找下一个步骤
        cursor.execute("""
            SELECT step_id FROM review_progress 
            WHERE review_id = %s AND step_order = %s
        """, [review_id, current_step_order + 1])
        
        next_step = cursor.fetchone()
        
        if next_step:
            # 激活下一步骤
            cursor.execute("""
                UPDATE review_progress 
                SET status = 'CLAIMED',
                    started_at = %s,
                    updated_at = %s
                WHERE review_id = %s AND step_id = %s
            """, [
                datetime.now(timezone.utc),
                datetime.now(timezone.utc),
                review_id,
                next_step[0]
            ])
            
            # 更新评审当前步骤
            cursor.execute("""
                UPDATE reviews 
                SET current_step_id = %s,
                    current_step_number = %s,
                    updated_at = %s
                WHERE id = %s
            """, [
                next_step[0],
                current_step_order + 1,
                datetime.now(timezone.utc),
                review_id
            ])
            
            return True
        else:
            # 没有下一步骤，完成评审
            cursor.execute("""
                UPDATE reviews 
                SET status = 'CLOSED',
                    finished_at = %s,
                    progress_percentage = 100.0,
                    updated_at = %s
                WHERE id = %s
            """, [
                datetime.now(timezone.utc),
                datetime.now(timezone.utc),
                review_id
            ])
            
            return False
    
    def delegate_step(
        self,
        review_id: int,
        step_id: str,
        delegate_to_user_id: str,
        delegator_info: Dict[str, Any],
        delegation_reason: str = ""
    ) -> Dict[str, Any]:
        """
        委派審閱步驟

        將當前已認領的步驟委派給候選人列表中的其他用戶

        Args:
            review_id: 評審ID
            step_id: 步驟ID
            delegate_to_user_id: 被委派用戶的autodeskId
            delegator_info: 委派人信息
            delegation_reason: 委派原因

        Returns:
            委派結果
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            now = datetime.now(timezone.utc)

            # 1. 驗證當前步驟狀態和委派人權限
            cursor.execute("""
                SELECT rp.status, rp.claimed_by, rp.step_name
                FROM review_progress rp
                WHERE rp.review_id = %s AND rp.step_id = %s
                ORDER BY rp.created_at DESC LIMIT 1
            """, [review_id, step_id])

            current_step = cursor.fetchone()
            if not current_step:
                return {"success": False, "error": "步驟不存在"}

            if current_step['status'] != 'CLAIMED':
                return {"success": False, "error": f"只有已認領的步驟才能委派，當前狀態: {current_step['status']}"}

            # 驗證委派人是否為當前認領人
            claimed_by = current_step['claimed_by']
            if isinstance(claimed_by, str):
                claimed_by = json.loads(claimed_by)

            if claimed_by.get('autodeskId') != delegator_info.get('autodeskId'):
                return {"success": False, "error": "只有當前認領人才能委派此步驟"}

            # 2. 驗證被委派用戶是否在候選人列表中
            cursor.execute("""
                SELECT rsc.candidates
                FROM review_step_candidates rsc
                WHERE rsc.review_id = %s AND rsc.step_id = %s AND rsc.is_active = true
            """, [review_id, step_id])

            candidates_result = cursor.fetchone()
            if not candidates_result:
                return {"success": False, "error": "找不到此步驟的候選人配置"}

            candidates = candidates_result['candidates']
            if isinstance(candidates, str):
                candidates = json.loads(candidates)

            # 檢查被委派用戶是否在候選人列表中
            user_in_candidates = False
            candidate_users = candidates.get('users', [])
            for user in candidate_users:
                if user.get('autodeskId') == delegate_to_user_id:
                    user_in_candidates = True
                    delegate_to_user_info = user
                    break

            if not user_in_candidates:
                return {"success": False, "error": "被委派用戶不在此步驟的候選人列表中"}

            # 3. 重置步驟狀態為PENDING，清空claimed_by
            delegation_note = f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] 委派: {delegator_info.get('name')} → {delegate_to_user_info.get('name')}"
            if delegation_reason:
                delegation_note += f", 原因: {delegation_reason}"

            cursor.execute("""
                UPDATE review_progress
                SET
                    status = 'PENDING',
                    claimed_by = NULL,
                    notes = COALESCE(notes, '') || %s,
                    updated_at = %s
                WHERE review_id = %s AND step_id = %s
            """, [
                f"\\n{delegation_note}",
                now,
                review_id,
                step_id
            ])

            # 4. 記錄委派歷史到review_notifications表
            cursor.execute("""
                INSERT INTO review_notifications (
                    review_id, user_id, message, notification_type,
                    is_read, created_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s
                )
                RETURNING id
            """, [
                review_id,
                delegate_to_user_id,
                f"您被委派處理評審步驟: {current_step['step_name']}. 委派人: {delegator_info.get('name')}. {delegation_reason if delegation_reason else ''}",
                'step_delegated',
                False,
                now
            ])

            notification_id = cursor.fetchone()['id']

            conn.commit()

            return {
                "success": True,
                "message": f"步驟已成功委派給 {delegate_to_user_info.get('name')}",
                "data": {
                    "review_id": review_id,
                    "step_id": step_id,
                    "step_name": current_step['step_name'],
                    "delegator": delegator_info,
                    "delegate_to": delegate_to_user_info,
                    "delegation_reason": delegation_reason,
                    "delegation_time": now.isoformat(),
                    "notification_id": notification_id,
                    "new_status": "PENDING"
                }
            }

        except Exception as e:
            if conn:
                conn.rollback()
            print(f"✗ 委派步驟失敗: {str(e)}")
            return {
                "success": False,
                "error": f"委派步驟失敗: {str(e)}"
            }

        finally:
            if conn:
                conn.close()

    def send_back_to_previous_step(
        self,
        review_id: int,
        current_step_id: str,
        reason: str,
        user_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        返回到上一個步驟 - 支持INSERT新記錄邏輯

        這個功能實現您要求的核心邏輯：
        - 當"初始審閱2"返回到"初始審閱1"時
        - 為"初始審閱1"插入新的記錄（而不是UPDATE現有記錄）
        - 保留返回操作的完整歷史記錄

        Args:
            review_id: 評審ID
            current_step_id: 當前步驟ID
            reason: 返回原因
            user_info: 操作用戶信息

        Returns:
            操作結果包含上一步驟信息
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            now = datetime.now(timezone.utc)

            # 1. 獲取當前步驟信息
            cursor.execute("""
                SELECT step_order, step_name, step_type, status
                FROM review_progress
                WHERE review_id = %s AND step_id = %s
                ORDER BY created_at DESC LIMIT 1
            """, [review_id, current_step_id])

            current_step = cursor.fetchone()
            if not current_step:
                return {"success": False, "error": "當前步驟不存在"}

            current_order = current_step['step_order']

            # 2. 獲取上一個步驟信息（從workflow定義中）
            cursor.execute("""
                SELECT DISTINCT step_id, step_name, step_type, step_order
                FROM review_progress
                WHERE review_id = %s AND step_order < %s
                ORDER BY step_order DESC
                LIMIT 1
            """, [review_id, current_order])

            previous_step = cursor.fetchone()
            if not previous_step:
                return {"success": False, "error": "已經是第一步，無法返回"}

            # 3. 標記當前步驟為返回狀態 (UPDATE最新記錄)
            cursor.execute("""
                UPDATE review_progress
                SET
                    status = 'SENT_BACK',
                    notes = COALESCE(notes, '') || %s,
                    completed_by = %s,
                    completed_at = %s,
                    updated_at = %s
                WHERE review_id = %s AND step_id = %s
                  AND id = (
                      SELECT id FROM review_progress
                      WHERE review_id = %s AND step_id = %s
                      ORDER BY created_at DESC
                      LIMIT 1
                  )
            """, [
                f"\\n[{now.strftime('%Y-%m-%d %H:%M:%S')}] 返回原因: {reason}",
                json.dumps(user_info),
                now,
                now,
                review_id,
                current_step_id,
                review_id,
                current_step_id
            ])

            # 4. 關鍵：為上一個步驟 INSERT 新記錄（不是UPDATE）
            cursor.execute("""
                INSERT INTO review_progress (
                    review_id, step_id, step_name, step_type, step_order,
                    status, notes, created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                RETURNING id
            """, [
                review_id,
                previous_step['step_id'],
                previous_step['step_name'],
                previous_step['step_type'],
                previous_step['step_order'],
                'PENDING',  # 重新開始，狀態為PENDING
                f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] 從步驟 {current_step['step_name']} 返回，原因: {reason}",
                now,
                now
            ])

            new_record_id = cursor.fetchone()['id']

            # 5. 更新review表的當前步驟指向上一步
            cursor.execute("""
                UPDATE reviews
                SET
                    current_step_id = %s,
                    current_step_name = %s,
                    current_step_number = %s,
                    status = 'OPEN',
                    updated_at = %s,
                    notes = COALESCE(notes, '') || %s
                WHERE id = %s
            """, [
                previous_step['step_id'],
                previous_step['step_name'],
                previous_step['step_order'],
                now,
                f"\\n[{now.strftime('%Y-%m-%d %H:%M:%S')}] 返回到步驟: {previous_step['step_name']}",
                review_id
            ])

            conn.commit()

            return {
                "success": True,
                "message": f"成功返回到步驟: {previous_step['step_name']}",
                "data": {
                    "previous_step": {
                        "step_id": previous_step['step_id'],
                        "step_name": previous_step['step_name'],
                        "step_order": previous_step['step_order'],
                        "new_record_id": new_record_id
                    },
                    "current_step": {
                        "step_id": current_step_id,
                        "step_name": current_step['step_name'],
                        "status": "SENT_BACK"
                    },
                    "reason": reason,
                    "returned_at": now.isoformat(),
                    "returned_by": user_info
                }
            }

        except Exception as e:
            if conn:
                conn.rollback()
            print(f"✗ 返回上一步失敗: {str(e)}")
            return {
                "success": False,
                "error": f"返回上一步失敗: {str(e)}"
            }

        finally:
            if conn:
                conn.close()

    def send_back_to_initiator(
        self, 
        review_id: int, 
        step_id: str, 
        reason: str,
        user_info: Dict[str, Any]
    ) -> bool:
        """
        发送回发起人
        
        Args:
            review_id: 评审ID
            step_id: 步骤ID
            reason: 发送回的原因
            user_info: 操作用户信息
            
        Returns:
            是否成功
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            now = datetime.now(timezone.utc)
            
            # 更新当前步骤状态
            cursor.execute("""
                UPDATE review_progress 
                SET status = 'SENT_BACK',
                    comments = %s,
                    completed_by = %s,
                    completed_at = %s,
                    updated_at = %s
                WHERE review_id = %s AND step_id = %s
            """, [
                f"发送回发起人: {reason}",
                json.dumps(user_info),
                now,
                now,
                review_id,
                step_id
            ])
            
            # 更新评审状态
            cursor.execute("""
                UPDATE reviews 
                SET status = 'VOID',
                    notes = COALESCE(notes, '') || %s,
                    updated_at = %s
                WHERE id = %s
            """, [
                f"\n[{now.strftime('%Y-%m-%d %H:%M:%S')}] 发送回发起人: {reason}",
                now,
                review_id
            ])
            
            conn.commit()
            return True
            
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"✗ 发送回发起人失败: {str(e)}")
            return False
            
        finally:
            if conn:
                conn.close()
    
    def get_step_progress(self, review_id: int) -> List[Dict]:
        """
        获取评审步骤进度
        
        Args:
            review_id: 评审ID
            
        Returns:
            步骤进度列表
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            cursor.execute("""
                -- Get all executed steps from review_progress
                -- Modified to support ACC synced reviews with different step_ids
                -- Match by step_order (primary) and step_id (fallback for local reviews)
                SELECT
                    rp.id,
                    rsc.review_id,
                    rsc.step_id,
                    rsc.step_name,
                    rsc.step_type,
                    rsc.step_order,
                    COALESCE(rp.status, 'PENDING') as status,
                    rp.assigned_to,
                    rp.claimed_by,
                    rp.completed_by,
                    rp.action_by,
                    rp.decision,
                    rp.comments,
                    rp.notes,
                    rp.started_at,
                    rp.completed_at,
                    rp.end_time,
                    rp.due_date,
                    rp.local_comments,
                    rp.created_at,
                    rp.updated_at,
                    rsc.candidates,
                    CASE
                        WHEN rsc.candidates IS NOT NULL THEN
                            COALESCE(
                                jsonb_array_length(rsc.candidates->'users'), 0
                            ) + COALESCE(
                                jsonb_array_length(rsc.candidates->'roles'), 0
                            ) + COALESCE(
                                jsonb_array_length(rsc.candidates->'companies'), 0
                            )
                        ELSE 0
                    END as candidate_count,
                    0 as key_reviewer_count
                FROM review_step_candidates rsc
                LEFT JOIN review_progress rp
                    ON rp.review_id = rsc.review_id
                    AND (
                        rp.template_step_id = rsc.step_id  -- ✅ 優先使用 template_step_id
                        OR rp.step_order = rsc.step_order   -- ✅ Fallback 使用 step_order
                    )
                WHERE rsc.review_id = %s
                ORDER BY rsc.step_order, rp.id
            """, [review_id])
            
            steps = []
            for step in cursor.fetchall():
                step_dict = dict(step)

                # 解析JSON字段 (从review_progress表来的字段)
                json_fields = ['assigned_to', 'claimed_by', 'completed_by', 'action_by', 'local_comments']
                for field in json_fields:
                    if step_dict.get(field):
                        try:
                            if isinstance(step_dict[field], str):
                                step_dict[field] = json.loads(step_dict[field])
                        except:
                            step_dict[field] = {} if field != 'local_comments' else []

                # candidates 已经是 JSONB 类型，不需要解析
                # 如果 candidates 为 None，设置为空对象
                if step_dict.get('candidates') is None:
                    step_dict['candidates'] = {}

                steps.append(step_dict)
            
            return steps
            
        except Exception as e:
            print(f"✗ 获取步骤进度失败: {str(e)}")
            return []
            
        finally:
            if conn:
                conn.close()
    
    def get_user_pending_tasks(self, user_acc_id: str, project_id: str = None) -> List[Dict]:
        """
        获取用户待处理任务
        
        Args:
            user_acc_id: 用户ACC ID
            project_id: 项目ID（可选）
            
        Returns:
            待处理任务列表
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # 构建查询条件
            where_conditions = [
                "rp.status IN ('PENDING', 'CLAIMED')",
                "rc.candidate_acc_id = %s"
            ]
            params = [user_acc_id]
            
            if project_id:
                where_conditions.append("r.project_id = %s")
                params.append(project_id)
            
            cursor.execute(f"""
                SELECT DISTINCT
                    r.id as review_id,
                    r.name as review_name,
                    r.priority,
                    r.status as review_status,
                    rp.step_id,
                    rp.step_name,
                    rp.status as step_status,
                    rp.due_date,
                    false as is_key_reviewer,
                    'user' as candidate_type,
                    CASE 
                        WHEN rp.due_date < CURRENT_TIMESTAMP THEN true
                        ELSE false
                    END as is_overdue
                FROM reviews r
                JOIN review_progress rp ON r.id = rp.review_id
                LEFT JOIN review_step_candidates rsc ON rp.review_id = rsc.review_id AND rp.step_id = rsc.step_id
                WHERE {' AND '.join(where_conditions)}
                ORDER BY 
                    CASE WHEN rp.due_date < CURRENT_TIMESTAMP THEN 0 ELSE 1 END,
                    r.priority ASC,
                    rp.due_date ASC NULLS LAST
            """, params)
            
            tasks = [dict(task) for task in cursor.fetchall()]
            return tasks
            
        except Exception as e:
            print(f"✗ 获取用户待处理任务失败: {str(e)}")
            return []
            
        finally:
            if conn:
                conn.close()

# 创建全局实例
step_progress_manager = StepProgressManager()

@step_progress_bp.route('/api/step-progress/reviews/<int:review_id>/steps/<step_id>/claim', methods=['POST'])
def claim_step(review_id, step_id):
    """
    认领步骤
    """
    try:
        data = request.get_json()
        user_info = data.get('user_info')
        
        if not user_info:
            return jsonify({
                "error": "缺少用户信息",
                "status": "bad_request"
            }), 400
        
        success = step_progress_manager.claim_step(review_id, step_id, user_info)
        
        if success:
            return jsonify({
                "status": "success",
                "message": "步骤认领成功"
            })
        else:
            return jsonify({
                "error": "步骤认领失败",
                "status": "error"
            }), 400
        
    except Exception as e:
        print(f"✗ 认领步骤失败: {str(e)}")
        return jsonify({
            "error": f"认领步骤失败: {str(e)}",
            "status": "error"
        }), 500

@step_progress_bp.route('/api/step-progress/reviews/<int:review_id>/steps/<step_id>/submit', methods=['POST'])
def submit_step(review_id, step_id):
    """
    提交步骤
    """
    try:
        data = request.get_json()
        
        # 验证必需字段
        if not data.get('decision'):
            return jsonify({
                "error": "缺少决策信息",
                "status": "bad_request"
            }), 400
        
        if not data.get('user_info'):
            return jsonify({
                "error": "缺少用户信息",
                "status": "bad_request"
            }), 400
        
        result = step_progress_manager.submit_step(review_id, step_id, data)
        
        return jsonify({
            "status": "success",
            "message": "步骤提交成功",
            "data": result
        })
        
    except Exception as e:
        print(f"✗ 提交步骤失败: {str(e)}")
        return jsonify({
            "error": f"提交步骤失败: {str(e)}",
            "status": "error"
        }), 500

@step_progress_bp.route('/api/step-progress/reviews/<int:review_id>/steps/<step_id>/delegate', methods=['POST'])
def delegate_step_endpoint(review_id, step_id):
    """
    委派審閱步驟

    Request Body:
    {
        "delegate_to_user_id": "被委派用戶的autodeskId",
        "delegator_info": {"autodeskId": "xxx", "name": "xxx"},
        "delegation_reason": "委派原因（可選）"
    }
    """
    try:
        data = request.get_json()

        delegate_to_user_id = data.get('delegate_to_user_id')
        delegator_info = data.get('delegator_info')
        delegation_reason = data.get('delegation_reason', '')

        if not delegate_to_user_id:
            return jsonify({
                "success": False,
                "error": "缺少被委派用戶ID",
                "status": "bad_request"
            }), 400

        if not delegator_info:
            return jsonify({
                "success": False,
                "error": "缺少委派人信息",
                "status": "bad_request"
            }), 400

        result = step_progress_manager.delegate_step(
            review_id, step_id, delegate_to_user_id, delegator_info, delegation_reason
        )

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        print(f"✗ 委派步驟失敗: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"委派步驟失敗: {str(e)}",
            "status": "error"
        }), 500

@step_progress_bp.route('/api/step-progress/reviews/<int:review_id>/steps/<step_id>/send-back-to-previous', methods=['POST'])
def send_back_to_previous_step_endpoint(review_id, step_id):
    """
    返回到上一個步驟 - 支持INSERT新記錄邏輯

    Request Body:
    {
        "reason": "返回原因",
        "user_info": {"autodeskId": "xxx", "name": "xxx"}
    }
    """
    try:
        data = request.get_json()

        reason = data.get('reason', '需要返回修改')
        user_info = data.get('user_info')

        if not user_info:
            return jsonify({
                "success": False,
                "error": "缺少用戶信息",
                "status": "bad_request"
            }), 400

        result = step_progress_manager.send_back_to_previous_step(
            review_id, step_id, reason, user_info
        )

        if result["success"]:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        print(f"✗ 返回上一步失敗: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"返回上一步失敗: {str(e)}",
            "status": "error"
        }), 500

@step_progress_bp.route('/api/step-progress/reviews/<int:review_id>/steps/<step_id>/send-back', methods=['POST'])
def send_back_step(review_id, step_id):
    """
    发送回发起人
    """
    try:
        data = request.get_json()
        
        reason = data.get('reason', '需要修改')
        user_info = data.get('user_info')
        
        if not user_info:
            return jsonify({
                "error": "缺少用户信息",
                "status": "bad_request"
            }), 400
        
        success = step_progress_manager.send_back_to_initiator(
            review_id, step_id, reason, user_info
        )
        
        if success:
            return jsonify({
                "status": "success",
                "message": "已发送回发起人"
            })
        else:
            return jsonify({
                "error": "发送回发起人失败",
                "status": "error"
            }), 400
        
    except Exception as e:
        print(f"✗ 发送回发起人失败: {str(e)}")
        return jsonify({
            "error": f"发送回发起人失败: {str(e)}",
            "status": "error"
        }), 500

@step_progress_bp.route('/api/step-progress/reviews/<int:review_id>/progress')
def get_review_progress(review_id):
    """
    获取评审步骤进度
    """
    try:
        steps = step_progress_manager.get_step_progress(review_id)
        
        return jsonify({
            "status": "success",
            "data": {
                "review_id": review_id,
                "steps": steps,
                "total_steps": len(steps)
            }
        })
        
    except Exception as e:
        print(f"✗ 获取步骤进度失败: {str(e)}")
        return jsonify({
            "error": f"获取步骤进度失败: {str(e)}",
            "status": "error"
        }), 500

@step_progress_bp.route('/api/step-progress/users/<user_acc_id>/tasks')
def get_user_tasks(user_acc_id):
    """
    获取用户待处理任务
    """
    try:
        project_id = request.args.get('project_id')
        
        tasks = step_progress_manager.get_user_pending_tasks(user_acc_id, project_id)
        
        return jsonify({
            "status": "success",
            "data": {
                "user_acc_id": user_acc_id,
                "project_id": project_id,
                "tasks": tasks,
                "total_tasks": len(tasks),
                "overdue_tasks": len([t for t in tasks if t.get('is_overdue')])
            }
        })
        
    except Exception as e:
        print(f"✗ 获取用户任务失败: {str(e)}")
        return jsonify({
            "error": f"获取用户任务失败: {str(e)}",
            "status": "error"
        }), 500
