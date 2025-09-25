# -*- coding: utf-8 -*-
"""
Reviews API 相关模块
处理 ACC Reviews API 的所有功能，包括审批工作流和评审数据
"""

import requests
import json
from flask import Blueprint, jsonify, request
from datetime import datetime
import config
import utils

reviews_bp = Blueprint('reviews', __name__)


@reviews_bp.route('/api/reviews/<project_id>')
def get_project_reviews(project_id):
    """获取指定项目的评审列表"""
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
    
    # 过滤参数
    filter_workflow_id = request.args.get('filter[workflowId]', '')
    filter_status = request.args.get('filter[status]', '')
    filter_current_step_due_date = request.args.get('filter[currentStepDueDate]', '')
    filter_created_at = request.args.get('filter[createdAt]', '')
    filter_updated_at = request.args.get('filter[updatedAt]', '')
    filter_finished_at = request.args.get('filter[finishedAt]', '')
    filter_next_action_by_user = request.args.get('filter[nextActionByUser]', '')
    filter_next_action_by_role = request.args.get('filter[nextActionByRole]', '')
    filter_next_action_by_company = request.args.get('filter[nextActionByCompany]', '')
    filter_name = request.args.get('filter[name]', '')
    filter_sequence_id = request.args.get('filter[sequenceId]', '')
    filter_archived = request.args.get('filter[archived]', '')
    filter_archived_by = request.args.get('filter[archivedBy]', '')
    filter_archived_at = request.args.get('filter[archivedAt]', '')
    
    # 构建查询参数
    params = {
        'limit': min(limit, 50),  # 最大50
        'offset': offset
    }
    
    if sort:
        params['sort'] = sort
    if filter_workflow_id:
        params['filter[workflowId]'] = filter_workflow_id
    if filter_status:
        params['filter[status]'] = filter_status
    if filter_current_step_due_date:
        params['filter[currentStepDueDate]'] = filter_current_step_due_date
    if filter_created_at:
        params['filter[createdAt]'] = filter_created_at
    if filter_updated_at:
        params['filter[updatedAt]'] = filter_updated_at
    if filter_finished_at:
        params['filter[finishedAt]'] = filter_finished_at
    if filter_next_action_by_user:
        params['filter[nextActionByUser]'] = filter_next_action_by_user
    if filter_next_action_by_role:
        params['filter[nextActionByRole]'] = filter_next_action_by_role
    if filter_next_action_by_company:
        params['filter[nextActionByCompany]'] = filter_next_action_by_company
    if filter_name:
        params['filter[name]'] = filter_name
    if filter_sequence_id:
        params['filter[sequenceId]'] = filter_sequence_id
    if filter_archived:
        params['filter[archived]'] = filter_archived.lower() == 'true'
    if filter_archived_by:
        params['filter[archivedBy]'] = filter_archived_by
    if filter_archived_at:
        params['filter[archivedAt]'] = filter_archived_at
    
    try:
        # 调用 Autodesk Construction Cloud Reviews API
        reviews_url = f"{config.AUTODESK_API_BASE}/construction/reviews/v1/projects/{project_id}/reviews"
        reviews_resp = requests.get(reviews_url, headers=headers, params=params)
        
        print(f"API请求URL: {reviews_url}")
        print(f"API请求参数: {params}")
        print(f"API响应状态码: {reviews_resp.status_code}")
        
        if reviews_resp.status_code != 200:
            error_text = reviews_resp.text
            print(f"API错误响应: {error_text}")
            raise Exception(f"获取评审列表失败: {reviews_resp.status_code} - {error_text}")
        
        try:
            reviews_data = reviews_resp.json()
            print(f"API响应数据: {reviews_data}")  # 调试信息
            
            # 详细调试前几个评审的ID信息
            if reviews_data and reviews_data.get("results"):
                print(f"总共获取到 {len(reviews_data['results'])} 个评审")
                for i, review in enumerate(reviews_data["results"][:5]):  # 只打印前5个
                    if review:
                        print(f"评审 {i+1}: ID={review.get('id')}, sequenceId={review.get('sequenceId')}, name={review.get('name', '')[:50]}")
                        
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            raise Exception(f"API响应数据格式错误: {str(e)}")
        
        if not reviews_data:
            print("API返回空数据")
            reviews_data = {"results": [], "pagination": {}}
            
        reviews_list = reviews_data.get("results", [])
        pagination = reviews_data.get("pagination", {})
        
        # 使用sequenceId作为主要去重标识，因为id可能不唯一
        seen_ids = set()
        unique_reviews = []
        duplicate_count = 0
        
        for review in reviews_list:
            if not review:
                continue
                
            # 优先使用sequenceId，如果没有则使用id
            review_unique_id = review.get("sequenceId") or review.get("id", "")
            if not review_unique_id:
                continue  # 跳过没有唯一标识的评审
                
            if review_unique_id in seen_ids:
                duplicate_count += 1
                print(f"发现重复评审: sequenceId={review.get('sequenceId')}, id={review.get('id')}, name={review.get('name', '')[:50]}")
                continue  # 跳过重复的评审
            
            seen_ids.add(review_unique_id)
            unique_reviews.append(review)
        
        original_count = len(reviews_list)
        reviews_list = unique_reviews
        
        if duplicate_count > 0:
            print(f"去重完成: 原始 {original_count} -> 去重后 {len(reviews_list)} (移除 {duplicate_count} 个重复)")
            
        # 调试去重后的评审ID
        print("去重后的评审ID列表:")
        for i, review in enumerate(reviews_list[:5]):  # 只打印前5个
            if review:
                print(f"去重后评审 {i+1}: ID={review.get('id')}, sequenceId={review.get('sequenceId')}, name={review.get('name', '')[:50]}")
        
        # 生成评审分析数据
        reviews_analysis = []
        for review in reviews_list:
            if not review:  # 跳过空的review对象
                continue
                
            # 安全获取nextActionBy数据
            next_action_by = review.get("nextActionBy") or {}
            claimed_by = next_action_by.get("claimedBy") or []
            candidates = next_action_by.get("candidates") or {}
            
            analysis = {
                "id": review.get("id", ""),
                "sequence_id": review.get("sequenceId", 0),
                "name": review.get("name", ""),
                "status": review.get("status", ""),
                "current_step_id": review.get("currentStepId", ""),
                "current_step_due_date": utils.format_timestamp(review.get("currentStepDueDate", "")),
                "created_by": review.get("createdBy") or {},
                "created_at": utils.format_timestamp(review.get("createdAt", "")),
                "updated_at": utils.format_timestamp(review.get("updatedAt", "")),
                "finished_at": utils.format_timestamp(review.get("finishedAt", "")),
                "archived": review.get("archived", False),
                "archived_by": review.get("archivedBy") or {},
                "archived_at": utils.format_timestamp(review.get("archivedAt", "")),
                "workflow_id": review.get("workflowId", ""),
                "next_action_by": next_action_by,
                "has_claimed_users": len(claimed_by) > 0,
                "candidates_count": {
                    "roles": len(candidates.get("roles") or []),
                    "users": len(candidates.get("users") or []),
                    "companies": len(candidates.get("companies") or [])
                }
            }
            reviews_analysis.append(analysis)
        
        # 生成详细的评审分析（使用去重后的评审列表）
        detailed_analysis = []
        for i, review in enumerate(reviews_list):
            if not review:  # 跳过空的review对象
                continue
                
            # 安全获取nextActionBy数据
            next_action_by = review.get('nextActionBy') or {}
            claimed_by = next_action_by.get('claimedBy') or []
            candidates = next_action_by.get('candidates') or {}
            
            review_analysis = {
                "review_number": i + 1,
                "basic_info": {
                    "id": review.get('id', 'N/A'),
                    "sequence_id": review.get('sequenceId', 'N/A'),
                    "name": review.get('name', 'N/A'),
                    "status": review.get('status', 'N/A'),
                    "workflow_id": review.get('workflowId', 'N/A'),
                    "created_at": utils.format_timestamp(review.get('createdAt', '')),
                    "updated_at": utils.format_timestamp(review.get('updatedAt', '')),
                    "finished_at": utils.format_timestamp(review.get('finishedAt', ''))
                },
                "review_summary": {
                    "current_step_id": review.get('currentStepId', 'N/A'),
                    "current_step_due_date": utils.format_timestamp(review.get('currentStepDueDate', '')),
                    "archived": review.get('archived', False),
                    "has_claimed_users": len(claimed_by) > 0,
                    "total_candidates": (
                        len(candidates.get('roles') or []) +
                        len(candidates.get('users') or []) +
                        len(candidates.get('companies') or [])
                    )
                },
                "participants": {
                    "created_by": review.get('createdBy') or {},
                    "archived_by": review.get('archivedBy') or {},
                    "claimed_by": claimed_by,
                    "candidates": candidates
                }
            }
            detailed_analysis.append(review_analysis)
        
        # 生成统计信息
        total_reviews = pagination.get('totalResults', len(reviews_list))
        status_counts = {}
        for review in reviews_list:
            if review:  # 确保review不为空
                status = review.get('status', 'UNKNOWN')
                status_counts[status] = status_counts.get(status, 0) + 1
        
        archived_count = len([r for r in reviews_list if r and r.get('archived', False)])
        
        # 安全计算有认领用户的评审数量
        with_claimed_users = 0
        total_candidates = 0
        
        for r in reviews_list:
            if r:  # 确保review不为空
                next_action_by = r.get('nextActionBy') or {}
                claimed_by = next_action_by.get('claimedBy') or []
                if len(claimed_by) > 0:
                    with_claimed_users += 1
                
                # 计算候选者总数
                candidates = next_action_by.get('candidates') or {}
                total_candidates += (
                    len(candidates.get('users') or []) + 
                    len(candidates.get('roles') or []) + 
                    len(candidates.get('companies') or [])
                )
        
        stats = {
            "total_reviews": total_reviews,
            "current_page_count": len(reviews_list),
            "original_count": original_count,
            "duplicate_count": duplicate_count,
            "unique_count": len(reviews_list),
            "status_counts": status_counts,
            "archived_count": archived_count,
            "active_count": len(reviews_list) - archived_count,
            "with_claimed_users": with_claimed_users,
            "avg_candidates_per_review": round(total_candidates / len(reviews_list), 1) if reviews_list else 0
        }
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "query_params": params,
            "stats": stats,
            "reviews": reviews_analysis,
            "detailed_analysis": detailed_analysis,
            "pagination": pagination,
            "raw_data": reviews_list,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"获取评审数据时出错: {str(e)}")
        return jsonify({
            "error": f"获取评审数据失败: {str(e)}",
            "status": "error"
        }), 500


@reviews_bp.route('/api/reviews/<project_id>/jarvis')
def get_jarvis_reviews(project_id=None):
    """获取 isBIM JARVIS 2025 Dev 项目的评审数据"""
    # 如果没有提供project_id，使用默认的JARVIS项目ID
    if not project_id:
        project_id = config.JARVIS_PROJECT_ID
    
    return get_project_reviews(project_id)


@reviews_bp.route('/api/reviews/jarvis')
def get_jarvis_reviews_simple():
    """获取项目的评审数据 - 支持动态项目ID"""
    # 获取项目ID - 优先使用请求参数，否则使用默认项目ID
    project_id = request.args.get('projectId', config.JARVIS_PROJECT_ID)
    print(f"🚀 Reviews API: 使用项目ID: {project_id}")
    
    return get_project_reviews(project_id)


# ==================== 工作流相关接口 ====================

@reviews_bp.route('/api/reviews/workflows/<project_id>')
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


@reviews_bp.route('/api/reviews/workflows/<project_id>/jarvis')
def get_jarvis_workflows(project_id=None):
    """获取 isBIM JARVIS 2025 Dev 项目的审批工作流数据"""
    # 如果没有提供project_id，使用默认的JARVIS项目ID
    if not project_id:
        project_id = config.JARVIS_PROJECT_ID
    
    return get_project_workflows(project_id)


@reviews_bp.route('/api/reviews/workflows/jarvis')
def get_jarvis_workflows_simple():
    """获取项目的审批工作流数据 - 支持动态项目ID"""
    # 获取项目ID - 优先使用请求参数，否则使用默认项目ID
    project_id = request.args.get('projectId', config.JARVIS_PROJECT_ID)
    print(f"🚀 Workflows API: 使用项目ID: {project_id}")
    
    return get_project_workflows(project_id)


# ==================== 单个评审工作流接口 ====================

@reviews_bp.route('/api/reviews/<project_id>/<review_id>/workflow')
def get_review_workflow(project_id, review_id):
    """获取指定评审的关联工作流"""
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
    
    try:
        # 调用 Autodesk Construction Cloud Reviews API
        workflow_url = f"{config.AUTODESK_API_BASE}/construction/reviews/v1/projects/{project_id}/reviews/{review_id}/workflow"
        
        print(f"API请求URL: {workflow_url}")
        print(f"API请求头: {headers}")
        
        workflow_resp = requests.get(workflow_url, headers=headers)
        
        print(f"API响应状态码: {workflow_resp.status_code}")
        
        if workflow_resp.status_code != 200:
            error_text = workflow_resp.text
            print(f"API错误响应: {error_text}")
            raise Exception(f"获取评审工作流失败: {workflow_resp.status_code} - {error_text}")
        
        try:
            workflow_data = workflow_resp.json()
            print(f"API响应数据: {workflow_data}")
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            raise Exception(f"API响应数据格式错误: {str(e)}")
        
        if not workflow_data:
            print("API返回空工作流数据")
            workflow_data = {}
        
        # 生成工作流分析数据
        workflow_analysis = {
            "id": workflow_data.get("id", ""),
            "name": workflow_data.get("name", ""),
            "description": workflow_data.get("description", ""),
            "notes": workflow_data.get("notes", ""),
            "additional_options": workflow_data.get("additionalOptions") or {},
            "steps": workflow_data.get("steps") or [],
            "approval_status_options": workflow_data.get("approvalStatusOptions") or [],
            "copy_files_options": workflow_data.get("copyFilesOptions") or {},
            "attached_attributes": workflow_data.get("attachedAttributes") or [],
            "update_attributes_options": workflow_data.get("updateAttributesOptions") or {},
            # 计算统计信息
            "steps_count": len(workflow_data.get("steps", [])),
            "approval_options_count": len(workflow_data.get("approvalStatusOptions", [])),
            "has_copy_files": workflow_data.get("copyFilesOptions", {}).get("enabled", False),
            "has_attached_attributes": len(workflow_data.get("attachedAttributes", [])) > 0,
            "allow_initiator_edit": workflow_data.get("additionalOptions", {}).get("allowInitiatorToEdit", False)
        }
        
        # 生成详细的步骤分析
        detailed_steps = []
        steps = workflow_data.get("steps", [])
        for step_idx, step in enumerate(steps):
            if not step:
                continue
                
            candidates = step.get("candidates") or {}
            step_detail = {
                "step_number": step_idx + 1,
                "id": step.get("id", ""),
                "name": step.get("name", ""),
                "type": step.get("type", ""),
                "duration": step.get("duration", 0),
                "due_date_type": step.get("dueDateType", ""),
                "group_review": step.get("groupReview") or {},
                "candidates": {
                    "roles": candidates.get("roles") or [],
                    "users": candidates.get("users") or [],
                    "companies": candidates.get("companies") or [],
                    "roles_count": len(candidates.get("roles") or []),
                    "users_count": len(candidates.get("users") or []),
                    "companies_count": len(candidates.get("companies") or [])
                }
            }
            detailed_steps.append(step_detail)
        
        # 生成审批状态选项分析
        approval_options_analysis = []
        for option in workflow_data.get("approvalStatusOptions", []):
            if not option:
                continue
            option_analysis = {
                "id": option.get("id", ""),
                "label": option.get("label", ""),
                "value": option.get("value", ""),
                "built_in": option.get("builtIn", False)
            }
            approval_options_analysis.append(option_analysis)
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "review_id": review_id,
            "workflow": workflow_analysis,
            "detailed_steps": detailed_steps,
            "approval_options": approval_options_analysis,
            "raw_data": workflow_data,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"获取评审工作流时出错: {str(e)}")
        return jsonify({
            "error": f"获取评审工作流失败: {str(e)}",
            "status": "error"
        }), 500


@reviews_bp.route('/api/reviews/jarvis/<review_id>/workflow')
def get_jarvis_review_workflow(review_id):
    """获取 JARVIS 项目中指定评审的工作流"""
    return get_review_workflow(config.JARVIS_PROJECT_ID, review_id)


# ==================== 评审文件版本接口 ====================

@reviews_bp.route('/api/reviews/<project_id>/<review_id>/versions')
def get_review_versions(project_id, review_id):
    """获取指定评审的文件版本列表"""
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
    filter_approve_status = request.args.getlist('filter[approveStatus]')
    
    # 构建查询参数
    params = {
        'limit': min(limit, 50),  # 最大50
        'offset': offset
    }
    
    # 添加审批状态过滤器
    for status in filter_approve_status:
        if status:
            params.setdefault('filter[approveStatus]', []).append(status)
    
    try:
        # 调用 Autodesk Construction Cloud Reviews API
        versions_url = f"{config.AUTODESK_API_BASE}/construction/reviews/v1/projects/{project_id}/reviews/{review_id}/versions"
        
        print(f"API请求URL: {versions_url}")
        print(f"API请求参数: {params}")
        
        versions_resp = requests.get(versions_url, headers=headers, params=params)
        
        print(f"API响应状态码: {versions_resp.status_code}")
        
        if versions_resp.status_code != 200:
            error_text = versions_resp.text
            print(f"API错误响应: {error_text}")
            raise Exception(f"获取评审文件版本失败: {versions_resp.status_code} - {error_text}")
        
        try:
            versions_data = versions_resp.json()
            print(f"API响应数据: {versions_data}")
            
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            raise Exception(f"API响应数据格式错误: {str(e)}")
        
        if not versions_data:
            print("API返回空文件版本数据")
            versions_data = {"results": [], "pagination": {}}
        
        versions_list = versions_data.get("results", [])
        pagination = versions_data.get("pagination", {})
        
        # 对文件版本进行去重处理
        seen_urns = set()
        unique_versions = []
        duplicate_versions_count = 0
        
        for version in versions_list:
            if not version:
                continue
                
            version_urn = version.get("urn", "")
            if not version_urn:
                continue  # 跳过没有URN的版本
                
            if version_urn in seen_urns:
                duplicate_versions_count += 1
                continue  # 跳过重复的文件版本
            
            seen_urns.add(version_urn)
            unique_versions.append(version)
        
        original_versions_count = len(versions_list)
        versions_list = unique_versions
        
        if duplicate_versions_count > 0:
            print(f"文件版本去重: 原始 {original_versions_count} -> 去重后 {len(versions_list)} (移除 {duplicate_versions_count} 个重复)")
        
        # 生成文件版本分析数据
        versions_analysis = []
        for version in versions_list:
            if not version:
                continue
            
            approve_status = version.get("approveStatus") or {}
            review_content = version.get("reviewContent") or {}
            custom_attributes = review_content.get("customAttributes") or []
            
            # 提取更多标识符来区分文件
            version_number = extract_version_number(version.get("urn", ""))
            file_size = version.get("size", 0)
            created_date = version.get("createdDate", "")
            modified_date = version.get("modifiedDate", "")
            
            analysis = {
                "urn": version.get("urn", ""),
                "item_urn": version.get("itemUrn", ""),
                "name": version.get("name", ""),
                "version_number": version_number,
                "file_size": file_size,
                "created_date": utils.format_timestamp(created_date) if created_date else "",
                "modified_date": utils.format_timestamp(modified_date) if modified_date else "",
                "approve_status": {
                    "id": approve_status.get("id", ""),
                    "label": approve_status.get("label", ""),
                    "value": approve_status.get("value", ""),
                    "status_type": get_approve_status_type(approve_status.get("value", ""))
                },
                "review_content": {
                    "name": review_content.get("name", ""),
                    "custom_attributes": custom_attributes,
                    "custom_attributes_count": len(custom_attributes)
                },
                "copied_file_version_urn": version.get("copiedFileVersionUrn", ""),
                "has_copied_version": bool(version.get("copiedFileVersionUrn")),
                "file_extension": get_file_extension(version.get("name", "")),
                "is_pdf": version.get("name", "").lower().endswith('.pdf'),
                "unique_identifier": f"{version.get('itemUrn', '')}-{version_number}",
                "display_name": f"{version.get('name', '')} (v{version_number})" if version_number else version.get('name', ''),
                # 保留原始数据用于调试
                "raw_version_data": version
            }
            versions_analysis.append(analysis)
        
        # 生成统计信息
        total_versions = pagination.get('totalResults', len(versions_list))
        status_counts = {}
        file_type_counts = {}
        
        for version in versions_analysis:
            # 统计审批状态
            status_label = version["approve_status"]["label"]
            if status_label:
                status_counts[status_label] = status_counts.get(status_label, 0) + 1
            
            # 统计文件类型
            file_ext = version["file_extension"]
            if file_ext:
                file_type_counts[file_ext] = file_type_counts.get(file_ext, 0) + 1
        
        copied_versions_count = len([v for v in versions_analysis if v["has_copied_version"]])
        with_custom_attributes = len([v for v in versions_analysis if v["review_content"]["custom_attributes_count"] > 0])
        
        stats = {
            "total_versions": total_versions,
            "current_page_count": len(versions_list),
            "original_versions_count": original_versions_count,
            "duplicate_versions_count": duplicate_versions_count,
            "unique_versions_count": len(versions_list),
            "status_counts": status_counts,
            "file_type_counts": file_type_counts,
            "copied_versions_count": copied_versions_count,
            "with_custom_attributes": with_custom_attributes,
            "pdf_files_count": len([v for v in versions_analysis if v["is_pdf"]])
        }
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "review_id": review_id,
            "query_params": params,
            "stats": stats,
            "versions": versions_analysis,
            "pagination": pagination,
            "raw_data": versions_list,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"获取评审文件版本时出错: {str(e)}")
        return jsonify({
            "error": f"获取评审文件版本失败: {str(e)}",
            "status": "error"
        }), 500


def get_approve_status_type(status_value):
    """获取审批状态的类型用于UI显示"""
    status_map = {
        'APPROVED': 'success',
        'REJECTED': 'danger',
        'PENDING': 'warning',
        'VOID': 'info'
    }
    return status_map.get(status_value, 'info')


def get_file_extension(filename):
    """获取文件扩展名"""
    if not filename:
        return ""
    return filename.split('.')[-1].upper() if '.' in filename else ""


def extract_version_number(urn):
    """从URN中提取版本号"""
    if not urn:
        return ""
    
    # URN格式通常是: urn:adsk.wipprod:fs.file:vf.xxxxx?version=N
    import re
    version_match = re.search(r'version=(\d+)', urn)
    if version_match:
        return version_match.group(1)
    
    # 也可能在URN的其他部分
    version_match = re.search(r'v(\d+)', urn)
    if version_match:
        return version_match.group(1)
    
    return "1"  # 默认版本号


@reviews_bp.route('/api/reviews/jarvis/<review_id>/versions')
def get_jarvis_review_versions(review_id):
    """获取 JARVIS 项目中指定评审的文件版本"""
    return get_review_versions(config.JARVIS_PROJECT_ID, review_id)


# ==================== 文件版本审批历史接口 ====================

@reviews_bp.route('/api/versions/<project_id>/<path:version_id>/approval-statuses')
def get_version_approval_statuses(project_id, version_id):
    """获取指定文件版本的审批历史和评审记录"""
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
    
    # 构建查询参数
    params = {
        'limit': min(limit, 50),  # 最大50
        'offset': offset
    }
    
    try:
        # URL编码版本ID（通常是URN）
        from urllib.parse import quote
        encoded_version_id = quote(version_id, safe='')
        
        # 调用 Autodesk Construction Cloud Reviews API
        approval_url = f"{config.AUTODESK_API_BASE}/construction/reviews/v1/projects/{project_id}/versions/{encoded_version_id}/approval-statuses"
        
        print(f"API请求URL: {approval_url}")
        print(f"API请求参数: {params}")
        print(f"原始版本ID: {version_id}")
        print(f"编码版本ID: {encoded_version_id}")
        
        approval_resp = requests.get(approval_url, headers=headers, params=params)
        
        print(f"API响应状态码: {approval_resp.status_code}")
        
        if approval_resp.status_code != 200:
            error_text = approval_resp.text
            print(f"API错误响应: {error_text}")
            raise Exception(f"获取文件审批历史失败: {approval_resp.status_code} - {error_text}")
        
        try:
            approval_data = approval_resp.json()
            print(f"API响应数据: {approval_data}")
            
            # 详细记录第一个审批记录的结构，以便了解可用字段
            if approval_data and approval_data.get("results") and len(approval_data["results"]) > 0:
                first_approval = approval_data["results"][0]
                print(f"第一个审批记录的完整结构: {json.dumps(first_approval, indent=2, ensure_ascii=False)}")
                print(f"第一个审批记录的所有字段: {list(first_approval.keys())}")
                
                # 检查嵌套结构
                if "approvalStatus" in first_approval:
                    print(f"approvalStatus字段: {list(first_approval['approvalStatus'].keys())}")
                if "review" in first_approval:
                    print(f"review字段: {list(first_approval['review'].keys())}")
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            raise Exception(f"API响应数据格式错误: {str(e)}")
        
        if not approval_data:
            print("API返回空审批历史数据")
            approval_data = {"results": [], "pagination": {}}
        
        approval_list = approval_data.get("results", [])
        pagination = approval_data.get("pagination", {})
        
        # 生成审批历史分析数据
        approval_analysis = []
        for approval in approval_list:
            if not approval:
                continue
            
            approval_status = approval.get("approvalStatus") or {}
            review_info = approval.get("review") or {}
            
            # 提取用户信息 - 检查所有可能的用户字段
            user_info = {}
            
            # 检查审批状态中的用户信息
            if "approvedBy" in approval:
                user_info["approved_by"] = approval.get("approvedBy") or {}
            if "reviewedBy" in approval:
                user_info["reviewed_by"] = approval.get("reviewedBy") or {}
            if "createdBy" in approval:
                user_info["created_by"] = approval.get("createdBy") or {}
            if "updatedBy" in approval:
                user_info["updated_by"] = approval.get("updatedBy") or {}
            if "assignedTo" in approval:
                user_info["assigned_to"] = approval.get("assignedTo") or {}
            
            # 检查时间戳信息
            timestamps = {}
            if "approvedAt" in approval:
                timestamps["approved_at"] = utils.format_timestamp(approval.get("approvedAt", ""))
            if "reviewedAt" in approval:
                timestamps["reviewed_at"] = utils.format_timestamp(approval.get("reviewedAt", ""))
            if "createdAt" in approval:
                timestamps["created_at"] = utils.format_timestamp(approval.get("createdAt", ""))
            if "updatedAt" in approval:
                timestamps["updated_at"] = utils.format_timestamp(approval.get("updatedAt", ""))
            
            # 检查审批状态中的用户信息
            if isinstance(approval_status, dict):
                if "approvedBy" in approval_status:
                    user_info["status_approved_by"] = approval_status.get("approvedBy") or {}
                if "assignedTo" in approval_status:
                    user_info["status_assigned_to"] = approval_status.get("assignedTo") or {}
            
            # 检查评审信息中的用户信息
            if isinstance(review_info, dict):
                if "createdBy" in review_info:
                    user_info["review_created_by"] = review_info.get("createdBy") or {}
                if "assignedTo" in review_info:
                    user_info["review_assigned_to"] = review_info.get("assignedTo") or {}
                if "currentAssignee" in review_info:
                    user_info["current_assignee"] = review_info.get("currentAssignee") or {}
            
            analysis = {
                "approval_status": {
                    "id": approval_status.get("id", ""),
                    "label": approval_status.get("label", ""),
                    "value": approval_status.get("value", ""),
                    "status_type": get_approve_status_type(approval_status.get("value", ""))
                },
                "review": {
                    "id": review_info.get("id", ""),
                    "sequence_id": review_info.get("sequenceId", 0),
                    "status": review_info.get("status", ""),
                    "status_type": get_review_status_type(review_info.get("status", ""))
                },
                "user_info": user_info,
                "timestamps": timestamps,
                "has_user_info": len(user_info) > 0,
                "has_timestamps": len(timestamps) > 0,
                "is_in_review": review_info.get("status") == "OPEN",
                "is_finished": review_info.get("status") in ["CLOSED", "VOID"],
                "sequence_display": f"#{review_info.get('sequenceId', 0)}"
            }
            approval_analysis.append(analysis)
        
        # 生成统计信息
        total_approvals = pagination.get('totalResults', len(approval_list))
        
        # 按状态分组统计
        approval_status_counts = {}
        review_status_counts = {}
        in_review_count = 0
        finished_count = 0
        
        for approval in approval_analysis:
            # 统计审批状态
            approval_label = approval["approval_status"]["label"]
            if approval_label:
                approval_status_counts[approval_label] = approval_status_counts.get(approval_label, 0) + 1
            
            # 统计评审状态
            review_status = approval["review"]["status"]
            if review_status:
                review_status_counts[review_status] = review_status_counts.get(review_status, 0) + 1
            
            # 统计进行中和已完成
            if approval["is_in_review"]:
                in_review_count += 1
            elif approval["is_finished"]:
                finished_count += 1
        
        # 按序列ID排序（倒序）
        approval_analysis.sort(key=lambda x: x["review"]["sequence_id"], reverse=True)
        
        # 分组数据
        in_review_approvals = [a for a in approval_analysis if a["is_in_review"]]
        finished_approvals = [a for a in approval_analysis if a["is_finished"]]
        
        stats = {
            "total_approvals": total_approvals,
            "current_page_count": len(approval_list),
            "approval_status_counts": approval_status_counts,
            "review_status_counts": review_status_counts,
            "in_review_count": in_review_count,
            "finished_count": finished_count,
            "latest_sequence_id": max([a["review"]["sequence_id"] for a in approval_analysis], default=0)
        }
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "version_id": version_id,
            "encoded_version_id": encoded_version_id,
            "query_params": params,
            "stats": stats,
            "approval_history": approval_analysis,
            "in_review_approvals": in_review_approvals,
            "finished_approvals": finished_approvals,
            "pagination": pagination,
            "raw_data": approval_list,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"获取文件审批历史时出错: {str(e)}")
        return jsonify({
            "error": f"获取文件审批历史失败: {str(e)}",
            "status": "error"
        }), 500


def get_review_status_type(status_value):
    """获取评审状态的类型用于UI显示"""
    status_map = {
        'OPEN': 'success',
        'CLOSED': 'info',
        'VOID': 'warning'
    }
    return status_map.get(status_value, 'info')


@reviews_bp.route('/api/versions/jarvis/<path:version_id>/approval-statuses')
def get_jarvis_version_approval_statuses(version_id):
    """获取 JARVIS 项目中指定文件版本的审批历史"""
    return get_version_approval_statuses(config.JARVIS_PROJECT_ID, version_id)


