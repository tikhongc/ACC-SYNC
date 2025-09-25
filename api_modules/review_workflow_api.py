# -*- coding: utf-8 -*-
"""
Approval Workflows API 相关模块
处理 ACC Reviews API 中的审批工作流功能
"""

import requests
import json
from flask import Blueprint, jsonify, request
from datetime import datetime
import config
import utils

workflows_bp = Blueprint('workflows', __name__)


@workflows_bp.route('/api/workflows/<project_id>')
def get_project_workflows(project_id):
    """获取指定项目的审批工作流列表"""
    access_token = utils.get_access_token()
    if not access_token:
        return jsonify({
            "error": "未找到 Access Token，请先进行认证",
            "status": "unauthorized"
        }), 401
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # 获取查询参数
    limit = request.args.get('limit', 50, type=int)
    offset = request.args.get('offset', 0, type=int)
    sort = request.args.get('sort', '')
    filter_initiator = request.args.get('filter[initiator]', '')
    filter_status = request.args.get('filter[status]', 'ACTIVE')
    
    # 构建查询参数
    params = {
        'limit': min(limit, 50),  # 最大50
        'offset': offset
    }
    
    if sort:
        params['sort'] = sort
    if filter_initiator:
        params['filter[initiator]'] = filter_initiator.lower() == 'true'
    if filter_status:
        params['filter[status]'] = filter_status
    
    try:
        # 调用 Autodesk Construction Cloud Reviews API
        workflows_url = f"{config.AUTODESK_API_BASE}/construction/reviews/v1/projects/{project_id}/workflows"
        workflows_resp = requests.get(workflows_url, headers=headers, params=params)
        
        if workflows_resp.status_code != 200:
            raise Exception(f"获取工作流列表失败: {workflows_resp.status_code} - {workflows_resp.text}")
        
        workflows_data = workflows_resp.json()
        workflows_list = workflows_data.get("results", [])
        pagination = workflows_data.get("pagination", {})
        
        # 生成工作流分析数据
        workflows_analysis = []
        for workflow in workflows_list:
            analysis = {
                "id": workflow.get("id"),
                "name": workflow.get("name"),
                "description": workflow.get("description", ""),
                "notes": workflow.get("notes", ""),
                "status": workflow.get("status"),
                "created_at": utils.format_timestamp(workflow.get("createdAt", "")),
                "updated_at": utils.format_timestamp(workflow.get("updatedAt", "")),
                "steps_count": len(workflow.get("steps", [])),
                "approval_options_count": len(workflow.get("approvalStatusOptions", [])),
                "has_copy_files": workflow.get("copyFilesOptions", {}).get("enabled", False),
                "has_attached_attributes": len(workflow.get("attachedAttributes", [])) > 0,
                "additional_options": workflow.get("additionalOptions", {}),
                "steps": workflow.get("steps", []),
                "approval_status_options": workflow.get("approvalStatusOptions", []),
                "copy_files_options": workflow.get("copyFilesOptions", {}),
                "attached_attributes": workflow.get("attachedAttributes", []),
                "update_attributes_options": workflow.get("updateAttributesOptions", {})
            }
            workflows_analysis.append(analysis)
        
        # 生成详细的工作流步骤分析
        detailed_analysis = []
        for i, workflow in enumerate(workflows_list):
            workflow_analysis = {
                "workflow_number": i + 1,
                "basic_info": {
                    "id": workflow.get('id', 'N/A'),
                    "name": workflow.get('name', 'N/A'),
                    "description": workflow.get('description', 'N/A'),
                    "status": workflow.get('status', 'N/A'),
                    "created_at": utils.format_timestamp(workflow.get('createdAt', '')),
                    "updated_at": utils.format_timestamp(workflow.get('updatedAt', '')),
                    "notes": workflow.get('notes', 'N/A')
                },
                "workflow_summary": {
                    "steps_count": len(workflow.get('steps', [])),
                    "approval_options_count": len(workflow.get('approvalStatusOptions', [])),
                    "has_copy_files": workflow.get('copyFilesOptions', {}).get('enabled', False),
                    "has_attached_attributes": len(workflow.get('attachedAttributes', [])) > 0,
                    "allow_initiator_edit": workflow.get('additionalOptions', {}).get('allowInitiatorToEdit', False)
                },
                "detailed_steps": []
            }
            
            # 分析工作流步骤
            steps = workflow.get("steps", [])
            if steps:
                for step_idx, step in enumerate(steps):
                    step_detail = {
                        "step_number": step_idx + 1,
                        "name": step.get('name', 'N/A'),
                        "type": step.get('type', 'N/A'),
                        "duration": step.get('duration', 0),
                        "due_date_type": step.get('dueDateType', 'N/A'),
                        "group_review": step.get('groupReview', {}),
                        "candidates": {
                            "roles_count": len(step.get('candidates', {}).get('roles', [])),
                            "users_count": len(step.get('candidates', {}).get('users', [])),
                            "companies_count": len(step.get('candidates', {}).get('companies', [])),
                            "roles": step.get('candidates', {}).get('roles', []),
                            "users": step.get('candidates', {}).get('users', []),
                            "companies": step.get('candidates', {}).get('companies', [])
                        }
                    }
                    workflow_analysis["detailed_steps"].append(step_detail)
            
            detailed_analysis.append(workflow_analysis)
        
        # 生成统计信息
        total_workflows = pagination.get('totalResults', len(workflows_list))
        active_workflows = len([w for w in workflows_list if w.get('status') == 'ACTIVE'])
        inactive_workflows = len([w for w in workflows_list if w.get('status') == 'INACTIVE'])
        
        stats = {
            "total_workflows": total_workflows,
            "current_page_count": len(workflows_list),
            "active_workflows": active_workflows,
            "inactive_workflows": inactive_workflows,
            "avg_steps_per_workflow": round(sum(len(w.get('steps', [])) for w in workflows_list) / len(workflows_list), 1) if workflows_list else 0,
            "workflows_with_copy_files": len([w for w in workflows_list if w.get('copyFilesOptions', {}).get('enabled', False)]),
            "workflows_with_attributes": len([w for w in workflows_list if w.get('attachedAttributes')])
        }
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "query_params": params,
            "stats": stats,
            "workflows": workflows_analysis,
            "detailed_analysis": detailed_analysis,
            "pagination": pagination,
            "raw_data": workflows_list,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"获取工作流数据时出错: {str(e)}")
        return jsonify({
            "error": f"获取工作流数据失败: {str(e)}",
            "status": "error"
        }), 500


@workflows_bp.route('/api/workflows/<project_id>/jarvis')
def get_jarvis_workflows(project_id=None):
    """获取 isBIM JARVIS 2025 Dev 项目的审批工作流数据"""
    # 如果没有提供project_id，使用默认的JARVIS项目ID
    if not project_id:
        project_id = config.JARVIS_PROJECT_ID
    
    return get_project_workflows(project_id)


@workflows_bp.route('/api/workflows/jarvis')
def get_jarvis_workflows_simple():
    """获取 JARVIS 项目的审批工作流数据（简化路由）"""
    return get_project_workflows(config.JARVIS_PROJECT_ID)
