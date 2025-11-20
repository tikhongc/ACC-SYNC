# -*- coding: utf-8 -*-
"""
评审CRUD API模块
实现评审的完整CRUD操作，包括状态管理和文件关联
"""

import json
import time
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

review_crud_bp = Blueprint('review_crud', __name__)

class ReviewCRUDManager:
    """评审CRUD管理器"""
    
    def __init__(self):
        """初始化评审CRUD管理器"""
        self.neon_config = NeonConfig()
        self.db_params = self.neon_config.get_db_params()
    
    def get_connection(self):
        """获取数据库连接"""
        return psycopg2.connect(**self.db_params)
    
    def create_review(self, review_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建新评审
        
        Args:
            review_data: 评审数据
            {
                "name": "评审名称",
                "description": "评审描述",
                "notes": "评审备注",
                "project_id": "项目ID",
                "workflow_id": 工作流ID,
                "created_by": {"autodeskId": "xxx", "name": "xxx"},
                "file_versions": [
                    {
                        "file_urn": "文件URN",
                        "file_name": "文件名",
                        "version_number": 1
                    }
                ],
                "priority": 3,
                "department": "部门",
                "category": "分类"
            }
            
        Returns:
            创建结果
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 生成UUID
            import uuid
            review_uuid = str(uuid.uuid4())
            
            now = datetime.now(timezone.utc)
            
            # 获取工作流信息
            workflow_info = self._get_workflow_info(cursor, review_data.get('workflow_id'))
            if not workflow_info:
                raise ValueError("指定的工作流不存在")
            
            # 插入评审记录
            insert_sql = """
                INSERT INTO reviews (
                    review_uuid, project_id, workflow_id, data_source,
                    name, description, notes, status,
                    workflow_uuid, created_by, priority, department, category,
                    total_steps, current_step_number, progress_percentage,
                    created_at, updated_at, started_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                RETURNING id
            """
            
            cursor.execute(insert_sql, [
                review_uuid,
                review_data.get('project_id'),
                review_data.get('workflow_id'),
                'local_system',
                review_data.get('name'),
                review_data.get('description'),
                review_data.get('notes'),
                'OPEN',  # 创建时状态为 OPEN（第一步已自动完成）
                workflow_info['workflow_uuid'],
                json.dumps(review_data.get('created_by', {})),
                review_data.get('priority', 3),
                review_data.get('department'),
                review_data.get('category'),
                len(workflow_info.get('steps', [])),
                1,
                0.0,
                now,
                now,
                now
            ])
            
            review_id = cursor.fetchone()[0]

            # 创建评审进度步骤
            self._create_review_progress_steps(cursor, review_id, workflow_info)

            # 添加文件版本
            file_versions = review_data.get('file_versions', [])
            if file_versions:
                self._add_review_file_versions(cursor, review_id, file_versions)

            # 自动完成第一步（发起者步骤）
            steps = workflow_info.get('steps', [])
            if steps and len(steps) > 0:
                first_step = steps[0]
                self._auto_complete_initiator_step(
                    cursor,
                    review_id,
                    first_step.get('id', 'step_1'),
                    review_data.get('created_by', {}),
                    steps  # 传入所有步骤信息
                )

            # 临时修复：将创建者添加到所有步骤的 candidates 中（除了第一步发起者）
            conn.commit()
            
            return {
                'review_id': review_id,
                'review_uuid': review_uuid,
                'status': 'created',
                'file_versions_added': len(file_versions)
            }
            
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"[ERROR] Create review failed: {str(e)}")
            raise
            
        finally:
            if conn:
                conn.close()
    
    def _get_workflow_info(self, cursor, workflow_id: int) -> Optional[Dict]:
        """获取工作流信息"""
        cursor.execute("""
            SELECT workflow_uuid, steps, name 
            FROM workflows 
            WHERE id = %s
        """, [workflow_id])
        
        result = cursor.fetchone()
        if not result:
            return None
        
        workflow_uuid, steps_json, name = result
        # Handle both JSON string and already parsed list from JSONB column
        if isinstance(steps_json, str):
            steps = json.loads(steps_json) if steps_json else []
        elif isinstance(steps_json, list):
            steps = steps_json
        else:
            steps = []
        
        return {
            'workflow_uuid': workflow_uuid,
            'steps': steps,
            'name': name
        }
    
    def _create_review_progress_steps(self, cursor, review_id: int, workflow_info: Dict):
        """创建评审进度步骤 - 同时创建 review_step_candidates 和 review_progress"""
        steps = workflow_info.get('steps', [])
        now = datetime.now(timezone.utc)

        for idx, step in enumerate(steps):
            step_id = step.get('id', f'step_{idx + 1}')
            step_name = step.get('name', f'Step {idx + 1}')
            step_type = step.get('type', 'REVIEWER')
            step_order = idx + 1

            # 从 workflow step 中获取 candidates 配置，如果没有则使用空配置
            step_candidates = step.get('candidates', {"users": [], "roles": [], "companies": []})

            # 确保 candidates 是字典格式
            if not isinstance(step_candidates, dict):
                step_candidates = {"users": [], "roles": [], "companies": []}

            # 1. 创建 review_step_candidates 记录（配置信息）
            cursor.execute("""
                INSERT INTO review_step_candidates (
                    review_id, step_id, step_name, step_type, step_order,
                    candidates, created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, [
                review_id,
                step_id,
                step_name,
                step_type,
                step_order,
                json.dumps(step_candidates),  # 使用 workflow 中的 candidates 配置
                now,
                now
            ])

            # 2. 不创建 review_progress 记录
            # review_progress 只在步骤被实际执行时才创建记录
    
    def _add_review_file_versions(self, cursor, review_id: int, file_versions: List[Dict]):
        """Add review file versions"""
        for file_version in file_versions:
            # Skip if file_urn is missing
            file_urn = file_version.get('file_urn') or file_version.get('file_version_urn')
            if not file_urn:
                print(f"⚠️  Skipping file version with missing URN: {file_version}")
                continue

            cursor.execute("""
                INSERT INTO review_file_versions (
                    review_id, file_version_urn, approval_status, created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s
                )
            """, [
                review_id,
                file_urn,
                'PENDING',
                datetime.now(timezone.utc),
                datetime.now(timezone.utc)
            ])

    def _add_creator_to_candidates(self, cursor, review_id: int, created_by: Dict, steps: List):
        """将创建者添加到所有步骤的 candidates 中（临时修复）"""
        # 准备用户信息
        user_candidate = {
            "autodeskId": created_by.get('autodeskId', ''),
            "name": created_by.get('name', ''),
            "email": created_by.get('email', '')
        }

        # 跳过第一步（发起者步骤），从第二步开始
        for idx, step in enumerate(steps[1:], start=2):
            step_id = step.get('id', f'step_{idx}')

            # 更新 candidates，添加创建者到 users 列表
            cursor.execute("""
                UPDATE review_step_candidates
                SET candidates = jsonb_set(
                    candidates,
                    '{users}',
                    COALESCE(candidates->'users', '[]'::jsonb) || %s::jsonb
                ),
                updated_at = %s
                WHERE review_id = %s AND step_id = %s
            """, [
                json.dumps([user_candidate]),
                datetime.now(timezone.utc),
                review_id,
                step_id
            ])

    def _auto_complete_initiator_step(self, cursor, review_id: int, step_id: str, created_by: Dict, all_steps: List):
        """自动完成发起者步骤（第一步），并将 current_step 更新为第二步"""
        now = datetime.now(timezone.utc)

        # 创建 review_progress 记录，标记为 SUBMITTED
        cursor.execute("""
            INSERT INTO review_progress (
                review_id, step_id, step_name, step_type, step_order,
                status, claimed_by, completed_by, action_by,
                started_at, completed_at, end_time,
                decision, comments, notes,
                created_at, updated_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """, [
            review_id,
            step_id,
            '发起者',  # 第一步通常是发起者步骤
            'INITIATOR',
            1,
            'SUBMITTED',
            json.dumps(created_by),  # 发起者认领
            json.dumps(created_by),  # 发起者完成
            json.dumps(created_by),  # 发起者操作
            now,  # 开始时间
            now,  # 完成时间
            now,  # 结束时间
            'APPROVED',  # 自动批准
            '自动提交 - Review created by initiator',
            'Auto-completed initiator step',
            now,
            now
        ])

        # 更新 review 的 current_step 为第二步（如果存在）
        if len(all_steps) > 1:
            second_step = all_steps[1]
            cursor.execute("""
                UPDATE reviews
                SET
                    current_step_id = %s,
                    current_step_name = %s,
                    current_step_number = %s,
                    updated_at = %s
                WHERE id = %s
            """, [
                second_step.get('id'),
                second_step.get('name'),
                2,  # 第二步的 order
                now,
                review_id
            ])

    def get_review(self, review_id: int) -> Optional[Dict]:
        """
        获取评审详细信息
        
        Args:
            review_id: 评审ID
            
        Returns:
            评审信息
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # 获取评审基本信息
            cursor.execute("""
                SELECT r.*, w.name as workflow_name
                FROM reviews r
                LEFT JOIN workflows w ON r.workflow_id = w.id
                WHERE r.id = %s
            """, [review_id])
            
            review = cursor.fetchone()
            if not review:
                return None
            
            review_dict = dict(review)
            
            # 解析JSON字段
            json_fields = ['assigned_to', 'next_action_by', 'archived_by', 'tags', 'custom_fields']
            for field in json_fields:
                if review_dict.get(field):
                    try:
                        if isinstance(review_dict[field], str):
                            review_dict[field] = json.loads(review_dict[field])
                    except:
                        review_dict[field] = {}

            # Remove created_by / updated_by from response
            review_dict.pop('created_by', None)
            review_dict.pop('updated_by', None)
            
            # 获取文件版本
            cursor.execute("""
                SELECT * FROM review_file_versions 
                WHERE review_id = %s 
                ORDER BY created_at
            """, [review_id])
            
            file_versions = [dict(fv) for fv in cursor.fetchall()]
            review_dict['file_versions'] = file_versions
            
            # 获取进度步骤
            cursor.execute("""
                SELECT * FROM review_progress 
                WHERE review_id = %s 
                ORDER BY step_order
            """, [review_id])
            
            progress_steps = []
            for step in cursor.fetchall():
                step_dict = dict(step)
                # 解析JSON字段
                json_fields = ['assigned_to', 'claimed_by', 'completed_by', 'action_by', 'candidates', 'local_comments']
                for field in json_fields:
                    if step_dict.get(field):
                        try:
                            if isinstance(step_dict[field], str):
                                step_dict[field] = json.loads(step_dict[field])
                        except:
                            step_dict[field] = {} if field != 'local_comments' else []
                progress_steps.append(step_dict)
            
            review_dict['progress_steps'] = progress_steps
            
            # 获取候选人配置
            cursor.execute("""
                SELECT 
                    rsc.id,
                    rsc.review_id,
                    rsc.step_id,
                    rsc.step_name,
                    rsc.step_order,
                    rsc.candidates,
                    rsc.source
                FROM review_step_candidates rsc
                WHERE rsc.review_id = %s AND rsc.is_active = true
                ORDER BY rsc.step_order
            """, [review_id])
            
            candidates = [dict(c) for c in cursor.fetchall()]
            review_dict['candidates'] = candidates
            
            return review_dict
            
        except Exception as e:
            print(f"[ERROR] Get review failed: {str(e)}")
            return None
            
        finally:
            if conn:
                conn.close()
    
    def update_review(self, review_id: int, updates: Dict[str, Any]) -> bool:
        """
        更新评审
        
        Args:
            review_id: 评审ID
            updates: 更新数据
            
        Returns:
            是否成功
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 构建更新SQL
            update_fields = []
            params = []
            
            allowed_fields = [
                'name', 'description', 'notes', 'status', 'priority', 
                'department', 'category', 'archived', 'archived_reason',
                'current_step_id', 'current_step_name', 'current_step_due_date'
            ]
            
            for field in allowed_fields:
                if field in updates:
                    update_fields.append(f"{field} = %s")
                    params.append(updates[field])
            
            if not update_fields:
                return True
            
            update_fields.append("updated_at = %s")
            params.append(datetime.now(timezone.utc))
            params.append(review_id)
            
            sql = f"""
                UPDATE reviews 
                SET {', '.join(update_fields)}
                WHERE id = %s
            """
            
            cursor.execute(sql, params)
            conn.commit()
            
            return cursor.rowcount > 0
            
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"[ERROR] 更新评审失败: {str(e)}")
            return False
            
        finally:
            if conn:
                conn.close()
    
    def delete_review(self, review_id: int) -> bool:
        """
        删除评审
        
        Args:
            review_id: 评审ID
            
        Returns:
            是否成功
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 检查评审状态
            cursor.execute("""
                SELECT status FROM reviews WHERE id = %s
            """, [review_id])
            
            result = cursor.fetchone()
            if not result:
                return False
            
            status = result[0]
            
            # 只允许删除草稿状态的评审
            if status not in ['DRAFT', 'CANCELLED']:
                raise ValueError("只能删除草稿或已取消状态的评审")
            
            # 删除评审（级联删除相关数据）
            cursor.execute("""
                DELETE FROM reviews WHERE id = %s
            """, [review_id])
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"[ERROR] 删除评审失败: {str(e)}")
            return False
            
        finally:
            if conn:
                conn.close()
    
    def list_reviews(self, filters: Dict = None, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """
        获取评审列表
        
        Args:
            filters: 过滤条件
            page: 页码
            page_size: 每页大小
            
        Returns:
            评审列表和分页信息
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # 构建查询条件
            where_conditions = []
            params = []
            
            if filters:
                if filters.get('project_id'):
                    where_conditions.append("r.project_id = %s")
                    params.append(filters['project_id'])
                
                if filters.get('status'):
                    where_conditions.append("r.status = %s")
                    params.append(filters['status'])
                
                if filters.get('workflow_id'):
                    where_conditions.append("r.workflow_id = %s")
                    params.append(filters['workflow_id'])
                
                if filters.get('priority'):
                    where_conditions.append("r.priority = %s")
                    params.append(filters['priority'])
                
                if filters.get('department'):
                    where_conditions.append("r.department = %s")
                    params.append(filters['department'])
                
                if filters.get('search'):
                    search_term = f"%{filters['search']}%"
                    where_conditions.append("(r.name ILIKE %s OR r.description ILIKE %s)")
                    params.extend([search_term, search_term])
            
            where_clause = f"WHERE {' AND '.join(where_conditions)}" if where_conditions else ""
            
            # 获取总数
            count_sql = f"""
                SELECT COUNT(*) FROM reviews r {where_clause}
            """
            cursor.execute(count_sql, params)
            count_result = cursor.fetchone()
            # RealDictCursor returns RealDictRow, access by key 'count' instead of index [0]
            total_count = count_result['count'] if count_result else 0
            print(f"[DEBUG] total_count from DB: {total_count}")

            # 获取分页数据
            offset = (page - 1) * page_size
            list_sql = f"""
                SELECT
                    r.*,
                    w.name as workflow_name,
                    COUNT(rfv.id) as file_count
                FROM reviews r
                LEFT JOIN workflows w ON r.workflow_id = w.id
                LEFT JOIN review_file_versions rfv ON r.id = rfv.review_id
                {where_clause}
                GROUP BY r.id, w.name
                ORDER BY r.created_at DESC
                LIMIT %s OFFSET %s
            """

            params.extend([page_size, offset])
            print(f"[DEBUG] list_sql: {list_sql}")
            print(f"[DEBUG] params with pagination: {params}")
            cursor.execute(list_sql, params)
            
            reviews = []
            for review in cursor.fetchall():
                review_dict = dict(review)
                
                # 解析JSON字段
                json_fields = ['assigned_to', 'next_action_by', 'tags']
                for field in json_fields:
                    if review_dict.get(field):
                        try:
                            if isinstance(review_dict[field], str):
                                review_dict[field] = json.loads(review_dict[field])
                        except:
                            review_dict[field] = {}

                # Remove created_by / updated_by from response
                review_dict.pop('created_by', None)
                review_dict.pop('updated_by', None)
                
                reviews.append(review_dict)
            
            # 计算分页信息
            total_pages = (total_count + page_size - 1) // page_size
            
            return {
                'reviews': reviews,
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total_count': total_count,
                    'total_pages': total_pages,
                    'has_next': page < total_pages,
                    'has_prev': page > 1
                },
                'filters_applied': filters or {}
            }
            
        except Exception as e:
            print(f"[ERROR] 获取评审列表失败: {str(e)}")
            return {
                'reviews': [],
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total_count': 0,
                    'total_pages': 0,
                    'has_next': False,
                    'has_prev': False
                },
                'filters_applied': filters or {}
            }
            
        finally:
            if conn:
                conn.close()
    
    def start_review(self, review_id: int) -> bool:
        """
        启动评审
        
        Args:
            review_id: 评审ID
            
        Returns:
            是否成功
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 更新评审状态
            cursor.execute("""
                UPDATE reviews 
                SET status = 'OPEN', started_at = %s, updated_at = %s
                WHERE id = %s AND status = 'DRAFT'
            """, [datetime.now(timezone.utc), datetime.now(timezone.utc), review_id])
            
            if cursor.rowcount == 0:
                return False
            
            # 更新第一个步骤状态
            cursor.execute("""
                UPDATE review_progress 
                SET status = 'PENDING', started_at = %s, updated_at = %s
                WHERE review_id = %s AND step_order = 1
            """, [datetime.now(timezone.utc), datetime.now(timezone.utc), review_id])
            
            conn.commit()
            return True
            
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"[ERROR] 启动评审失败: {str(e)}")
            return False
            
        finally:
            if conn:
                conn.close()

# 创建全局实例
review_crud_manager = ReviewCRUDManager()

@review_crud_bp.route('/api/reviews', methods=['POST'])
def create_review():
    """
    创建新评审
    """
    try:
        data = request.get_json()
        
        # 验证必需字段
        required_fields = ['name', 'project_id', 'workflow_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    "error": f"缺少必需字段: {field}",
                    "status": "bad_request"
                }), 400
        
        print(f"📝 创建评审: {data.get('name')}")
        
        # 创建评审
        result = review_crud_manager.create_review(data)
        
        return jsonify({
            "status": "success",
            "message": "评审创建成功",
            "data": result
        }), 201
        
    except Exception as e:
        print(f"[ERROR] 创建评审失败: {str(e)}")
        return jsonify({
            "error": f"创建评审失败: {str(e)}",
            "status": "error"
        }), 500

@review_crud_bp.route('/api/reviews/<int:review_id>')
def get_review(review_id):
    """
    获取评审详细信息
    """
    try:
        review = review_crud_manager.get_review(review_id)
        
        if not review:
            return jsonify({
                "error": "评审不存在",
                "status": "not_found"
            }), 404
        
        return jsonify({
            "status": "success",
            "data": review
        })
        
    except Exception as e:
        print(f"[ERROR] 获取评审失败: {str(e)}")
        return jsonify({
            "error": f"获取评审失败: {str(e)}",
            "status": "error"
        }), 500

@review_crud_bp.route('/api/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    """
    更新评审
    """
    try:
        data = request.get_json()
        
        success = review_crud_manager.update_review(review_id, data)
        
        if success:
            return jsonify({
                "status": "success",
                "message": "评审更新成功"
            })
        else:
            return jsonify({
                "error": "评审更新失败",
                "status": "error"
            }), 400
        
    except Exception as e:
        print(f"[ERROR] 更新评审失败: {str(e)}")
        return jsonify({
            "error": f"更新评审失败: {str(e)}",
            "status": "error"
        }), 500

@review_crud_bp.route('/api/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    """
    删除评审
    """
    try:
        success = review_crud_manager.delete_review(review_id)
        
        if success:
            return jsonify({
                "status": "success",
                "message": "评审删除成功"
            })
        else:
            return jsonify({
                "error": "评审删除失败",
                "status": "error"
            }), 400
        
    except Exception as e:
        print(f"[ERROR] 删除评审失败: {str(e)}")
        return jsonify({
            "error": f"删除评审失败: {str(e)}",
            "status": "error"
        }), 500

@review_crud_bp.route('/api/reviews')
def list_reviews():
    """
    获取评审列表
    """
    try:
        # 获取查询参数
        filters = {}
        if request.args.get('project_id'):
            filters['project_id'] = request.args.get('project_id')
        if request.args.get('status'):
            filters['status'] = request.args.get('status')
        if request.args.get('workflow_id'):
            filters['workflow_id'] = int(request.args.get('workflow_id'))
        if request.args.get('priority'):
            filters['priority'] = int(request.args.get('priority'))
        if request.args.get('department'):
            filters['department'] = request.args.get('department')
        if request.args.get('search'):
            filters['search'] = request.args.get('search')

        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))

        print(f"[DEBUG] list_reviews called with filters: {filters}, page: {page}, page_size: {page_size}")

        # 获取评审列表
        result = review_crud_manager.list_reviews(filters, page, page_size)

        print(f"[DEBUG] list_reviews result: reviews count = {len(result.get('reviews', []))}, total_count = {result.get('pagination', {}).get('total_count', 0)}")

        return jsonify({
            "status": "success",
            "data": result
        })
        
    except Exception as e:
        print(f"[ERROR] 获取评审列表失败: {str(e)}")
        return jsonify({
            "error": f"获取评审列表失败: {str(e)}",
            "status": "error"
        }), 500

@review_crud_bp.route('/api/reviews/<int:review_id>/start', methods=['POST'])
def start_review(review_id):
    """
    启动评审
    """
    try:
        success = review_crud_manager.start_review(review_id)
        
        if success:
            return jsonify({
                "status": "success",
                "message": "评审启动成功"
            })
        else:
            return jsonify({
                "error": "评审启动失败",
                "status": "error"
            }), 400
        
    except Exception as e:
        print(f"[ERROR] 启动评审失败: {str(e)}")
        return jsonify({
            "error": f"启动评审失败: {str(e)}",
            "status": "error"
        }), 500
