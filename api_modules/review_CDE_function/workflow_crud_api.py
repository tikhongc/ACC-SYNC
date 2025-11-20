# -*- coding: utf-8 -*-
"""
工作流CRUD API模块
实现工作流的完整CRUD操作
"""

import json
import uuid
from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from typing import Dict, List, Optional, Any
import sys
import os

# 添加数据库访问路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../database_sql'))
from neon_config import NeonConfig
import psycopg2
import psycopg2.extras

workflow_crud_bp = Blueprint('workflow_crud', __name__)

class WorkflowCRUDManager:
    """工作流CRUD管理器"""

    def __init__(self):
        """初始化工作流CRUD管理器"""
        self.neon_config = NeonConfig()
        self.db_params = self.neon_config.get_db_params()

    def get_connection(self):
        """获取数据库连接"""
        return psycopg2.connect(**self.db_params)

    def create_workflow(self, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建新工作流

        Args:
            workflow_data: 工作流数据
            {
                "name": "工作流名称",
                "description": "描述",
                "notes": "备注",
                "project_id": "项目ID",
                "template_type": "模板类型 (one_step, two_step, three_step, custom)",
                "created_by": {"autodeskId": "xxx", "name": "xxx"}
            }

        Returns:
            创建结果
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            workflow_uuid = str(uuid.uuid4())
            now = datetime.now(timezone.utc)

            # 根据模板类型生成步骤配置
            steps = self._generate_steps_from_template(workflow_data.get('template_type', 'two_step'))

            # 插入工作流记录
            insert_sql = """
                INSERT INTO workflows (
                    workflow_uuid, project_id, data_source,
                    name, description, notes, status,
                    steps, created_by, created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                RETURNING id, workflow_uuid
            """

            cursor.execute(insert_sql, [
                workflow_uuid,
                workflow_data.get('project_id'),
                'local_system',
                workflow_data.get('name'),
                workflow_data.get('description'),
                workflow_data.get('notes'),
                'ACTIVE',
                json.dumps(steps),
                json.dumps(workflow_data.get('created_by', {})),
                now,
                now
            ])

            result = cursor.fetchone()
            conn.commit()

            return {
                'success': True,
                'data': {
                    'id': result['id'],
                    'workflow_uuid': result['workflow_uuid'],
                    'message': 'Workflow created successfully'
                }
            }

        except Exception as e:
            if conn:
                conn.rollback()
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            if conn:
                cursor.close()
                conn.close()

    def _generate_steps_from_template(self, template_type: str) -> List[Dict]:
        """根据模板类型生成步骤配置"""
        templates = {
            'one_step': [
                {
                    'id': 'step_1',
                    'name': 'Approval',
                    'type': 'APPROVER',
                    'order': 1,
                    'reviewer_type': 'SINGLE_REVIEWER',
                    'time_allowed': 3,
                    'time_unit': 'CALENDAR_DAYS'
                }
            ],
            'two_step': [
                {
                    'id': 'step_1',
                    'name': 'Initial Review',
                    'type': 'REVIEWER',
                    'order': 1,
                    'reviewer_type': 'SINGLE_REVIEWER',
                    'time_allowed': 3,
                    'time_unit': 'CALENDAR_DAYS'
                },
                {
                    'id': 'step_2',
                    'name': 'Final Approval',
                    'type': 'APPROVER',
                    'order': 2,
                    'reviewer_type': 'SINGLE_REVIEWER',
                    'time_allowed': 2,
                    'time_unit': 'CALENDAR_DAYS'
                }
            ],
            'three_step': [
                {
                    'id': 'step_1',
                    'name': 'Initial Review',
                    'type': 'REVIEWER',
                    'order': 1,
                    'reviewer_type': 'SINGLE_REVIEWER',
                    'time_allowed': 3,
                    'time_unit': 'CALENDAR_DAYS'
                },
                {
                    'id': 'step_2',
                    'name': 'Secondary Review',
                    'type': 'REVIEWER',
                    'order': 2,
                    'reviewer_type': 'SINGLE_REVIEWER',
                    'time_allowed': 3,
                    'time_unit': 'CALENDAR_DAYS'
                },
                {
                    'id': 'step_3',
                    'name': 'Final Approval',
                    'type': 'APPROVER',
                    'order': 3,
                    'reviewer_type': 'SINGLE_REVIEWER',
                    'time_allowed': 2,
                    'time_unit': 'CALENDAR_DAYS'
                }
            ],
            'custom': [
                {
                    'id': 'step_1',
                    'name': 'Review',
                    'type': 'REVIEWER',
                    'order': 1,
                    'reviewer_type': 'SINGLE_REVIEWER',
                    'time_allowed': 5,
                    'time_unit': 'CALENDAR_DAYS'
                }
            ]
        }

        return templates.get(template_type, templates['two_step'])

    def get_workflow(self, workflow_id: int) -> Dict[str, Any]:
        """获取工作流详情"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cursor.execute("""
                SELECT * FROM workflows
                WHERE id = %s
            """, [workflow_id])

            workflow = cursor.fetchone()

            if not workflow:
                return {
                    'success': False,
                    'error': 'Workflow not found'
                }

            return {
                'success': True,
                'data': dict(workflow)
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            if conn:
                cursor.close()
                conn.close()

    def list_workflows(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """获取工作流列表"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # 构建查询条件
            where_clauses = []
            params = []

            if 'project_id' in filters:
                where_clauses.append("project_id = %s")
                params.append(filters['project_id'])

            if 'status' in filters:
                where_clauses.append("status = %s")
                params.append(filters['status'])

            where_sql = ""
            if where_clauses:
                where_sql = "WHERE " + " AND ".join(where_clauses)

            # 执行查询
            query = f"""
                SELECT
                    id, workflow_uuid, project_id, data_source,
                    name, description, notes, status,
                    steps, steps_count, total_reviews, active_reviews,
                    created_by, created_at, updated_at
                FROM workflows
                {where_sql}
                ORDER BY created_at DESC
            """

            cursor.execute(query, params)
            workflows = cursor.fetchall()

            return {
                'success': True,
                'data': [dict(w) for w in workflows],
                'count': len(workflows)
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'data': []
            }
        finally:
            if conn:
                cursor.close()
                conn.close()

    def update_workflow(self, workflow_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新工作流"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # 构建更新字段
            update_fields = []
            params = []

            if 'name' in update_data:
                update_fields.append("name = %s")
                params.append(update_data['name'])

            if 'description' in update_data:
                update_fields.append("description = %s")
                params.append(update_data['description'])

            if 'notes' in update_data:
                update_fields.append("notes = %s")
                params.append(update_data['notes'])

            if 'status' in update_data:
                update_fields.append("status = %s")
                params.append(update_data['status'])

            if 'steps' in update_data:
                update_fields.append("steps = %s")
                params.append(json.dumps(update_data['steps']))

            if not update_fields:
                return {
                    'success': False,
                    'error': 'No fields to update'
                }

            # 添加 updated_at
            update_fields.append("updated_at = %s")
            params.append(datetime.now(timezone.utc))

            # 添加 workflow_id
            params.append(workflow_id)

            # 执行更新
            update_sql = f"""
                UPDATE workflows
                SET {', '.join(update_fields)}
                WHERE id = %s
            """

            cursor.execute(update_sql, params)
            conn.commit()

            if cursor.rowcount == 0:
                return {
                    'success': False,
                    'error': 'Workflow not found'
                }

            return {
                'success': True,
                'message': 'Workflow updated successfully'
            }

        except Exception as e:
            if conn:
                conn.rollback()
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            if conn:
                cursor.close()
                conn.close()

    def delete_workflow(self, workflow_id: int) -> Dict[str, Any]:
        """删除工作流"""
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # 检查是否有关联的评审
            cursor.execute("""
                SELECT COUNT(*) FROM reviews
                WHERE workflow_id = %s
            """, [workflow_id])

            review_count = cursor.fetchone()[0]

            if review_count > 0:
                return {
                    'success': False,
                    'error': f'Cannot delete workflow: {review_count} review(s) are using this workflow'
                }

            # 删除工作流
            cursor.execute("""
                DELETE FROM workflows
                WHERE id = %s
            """, [workflow_id])

            conn.commit()

            if cursor.rowcount == 0:
                return {
                    'success': False,
                    'error': 'Workflow not found'
                }

            return {
                'success': True,
                'message': 'Workflow deleted successfully'
            }

        except Exception as e:
            if conn:
                conn.rollback()
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            if conn:
                cursor.close()
                conn.close()

# 初始化管理器
workflow_manager = WorkflowCRUDManager()

# ============================================================================
# API 路由
# ============================================================================

@workflow_crud_bp.route('/api/workflows', methods=['POST'])
def create_workflow():
    """创建工作流"""
    try:
        data = request.get_json()
        result = workflow_manager.create_workflow(data)
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@workflow_crud_bp.route('/api/workflows/<int:workflow_id>')
def get_workflow(workflow_id):
    """获取工作流详情"""
    try:
        result = workflow_manager.get_workflow(workflow_id)
        status_code = 200 if result['success'] else 404
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@workflow_crud_bp.route('/api/workflows')
def list_workflows():
    """获取工作流列表"""
    try:
        filters = {
            'project_id': request.args.get('project_id'),
            'status': request.args.get('status')
        }
        # 移除 None 值
        filters = {k: v for k, v in filters.items() if v is not None}

        result = workflow_manager.list_workflows(filters)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'data': []
        }), 500

@workflow_crud_bp.route('/api/workflows/<int:workflow_id>', methods=['PUT'])
def update_workflow(workflow_id):
    """更新工作流"""
    try:
        data = request.get_json()
        result = workflow_manager.update_workflow(workflow_id, data)
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@workflow_crud_bp.route('/api/workflows/<int:workflow_id>', methods=['DELETE'])
def delete_workflow(workflow_id):
    """删除工作流"""
    try:
        result = workflow_manager.delete_workflow(workflow_id)
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@workflow_crud_bp.route('/api/workflow-templates')
def get_workflow_templates():
    """获取工作流模板列表"""
    templates = [
        {
            'template_type': 'one_step',
            'name': 'One Step Approval',
            'description': 'Single approval step workflow'
        },
        {
            'template_type': 'two_step',
            'name': 'Two Step Approval',
            'description': 'Two-step approval workflow'
        },
        {
            'template_type': 'three_step',
            'name': 'Three Step Approval',
            'description': 'Three-step approval workflow'
        },
        {
            'template_type': 'custom',
            'name': 'Custom Workflow',
            'description': 'Custom workflow configuration'
        }
    ]

    return jsonify({
        'success': True,
        'data': templates
    }), 200
