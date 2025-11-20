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
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import unquote

reviews_bp = Blueprint('reviews', __name__)

# Reviews API 相关功能实现


def _normalize_file_identifier(file_id):
    """标准化文件标识符，处理URL编码等"""
    if not file_id:
        return ""
    
    # URL解码
    decoded_id = unquote(file_id)
    
    # 移除可能的前缀
    if decoded_id.startswith('urn:'):
        return decoded_id
    
    return decoded_id


def _analyze_reviewer_types(claimed_by, candidates):
    """
    分析审阅者类型，区分主要审阅者和可选审阅者
    
    Args:
        claimed_by: 已认领的用户列表
        candidates: 候选者字典，包含 users, roles, companies
    
    Returns:
        dict: 包含主要审阅者和可选审阅者信息的字典
    """
    # 提取候选用户、角色和公司
    candidate_users = candidates.get("users", []) if candidates else []
    candidate_roles = candidates.get("roles", []) if candidates else []
    candidate_companies = candidates.get("companies", []) if candidates else []
    
    # 主要审阅者 = 已认领的用户
    primary_reviewers = claimed_by or []
    
    # 可选审阅者 = 尚未认领的候选者
    optional_reviewers = {
        "users": candidate_users,
        "roles": candidate_roles, 
        "companies": candidate_companies
    }
    
    # 计算总数
    total_primary = len(primary_reviewers)
    total_optional = len(candidate_users) + len(candidate_roles) + len(candidate_companies)
    
    # 判断审阅模式
    if total_primary > 0 and total_optional > 0:
        review_mode = "mixed"  # 混合模式：既有主要审阅者，也有可选审阅者
    elif total_primary > 0:
        review_mode = "primary_only"  # 仅主要审阅者
    elif total_optional > 0:
        review_mode = "optional_only"  # 仅可选审阅者
    else:
        review_mode = "none"  # 无审阅者
    
    return {
        "primary_reviewers": primary_reviewers,
        "optional_reviewers": optional_reviewers,
        "counts": {
            "primary_total": total_primary,
            "optional_users": len(candidate_users),
            "optional_roles": len(candidate_roles),
            "optional_companies": len(candidate_companies),
            "optional_total": total_optional,
            "total_reviewers": total_primary + total_optional
        },
        "review_mode": review_mode,
        "has_primary_reviewers": total_primary > 0,
        "has_optional_reviewers": total_optional > 0,
        "is_multi_reviewer": (total_primary + total_optional) > 1,
        "assignment_details": {
            "has_direct_users": len(candidate_users) > 0,
            "has_roles": len(candidate_roles) > 0,
            "has_companies": len(candidate_companies) > 0,
            "role_names": [r.get("name", "Unknown Role") for r in candidate_roles],
            "company_names": [c.get("name", "Unknown Company") for c in candidate_companies]
        }
    }


def _analyze_group_review_config(group_review_config):
    """
    分析工作流步骤的组审阅配置
    
    Args:
        group_review_config: 组审阅配置字典
    
    Returns:
        dict: 包含组审阅配置分析的字典
    """
    if not group_review_config:
        return {
            "enabled": False,
            "type": "single",
            "description": "Single reviewer mode",
            "min_reviewers": 1,
            "is_multi_reviewer_step": False
        }
    
    enabled = group_review_config.get("enabled", False)
    review_type = group_review_config.get("type", "ALL")
    min_reviewers = group_review_config.get("min", 1)
    
    # 根据类型生成描述
    type_descriptions = {
        "ALL": "All reviewers must review",
        "ANY": "Any reviewer can approve",
        "MAJORITY": "Majority of reviewers must approve"
    }
    
    description = type_descriptions.get(review_type, f"Unknown review type: {review_type}")
    
    # 如果启用了组审阅但类型是ALL，且最小数量大于1，则是多审阅者必须模式
    if enabled and review_type == "ALL" and min_reviewers > 1:
        description = f"At least {min_reviewers} reviewers must all agree"
    elif enabled and review_type == "ANY":
        description = f"At least any one of {min_reviewers} reviewers must agree"
    elif enabled and review_type == "MAJORITY":
        description = f"Majority of reviewers must agree (minimum {min_reviewers})"
    
    return {
        "enabled": enabled,
        "type": review_type,
        "description": description,
        "min_reviewers": min_reviewers,
        "is_multi_reviewer_step": enabled and min_reviewers > 1,
        "review_strategy": {
            "requires_all": review_type == "ALL",
            "requires_any": review_type == "ANY", 
            "requires_majority": review_type == "MAJORITY"
        }
    }


def _analyze_workflow_step_reviewer_types(step):
    """
    分析工作流步骤的审阅者类型（基于工作流定义，不展开具体用户）
    
    Args:
        step: 工作流步骤数据
    
    Returns:
        dict: 包含审阅者类型分析的字典
    """
    if not step:
        return {
            "has_reviewers": False,
            "reviewer_types": [],
            "total_potential_reviewers": 0,
            "is_multi_reviewer": False,
            "assignment_mode": "none"
        }
    
    candidates = step.get("candidates", {})
    users = candidates.get("users", [])
    roles = candidates.get("roles", [])
    companies = candidates.get("companies", [])
    
    # 分析审阅者类型
    reviewer_types = []
    if users:
        reviewer_types.append({
            "type": "direct_users",
            "count": len(users),
            "items": [{"id": u.get("id"), "name": u.get("name", "Unknown User")} for u in users]
        })
    
    if roles:
        reviewer_types.append({
            "type": "roles",
            "count": len(roles),
            "items": [{"id": r.get("id"), "name": r.get("name", "Unknown Role")} for r in roles]
        })
    
    if companies:
        reviewer_types.append({
            "type": "companies", 
            "count": len(companies),
            "items": [{"id": c.get("id"), "name": c.get("name", "Unknown Company")} for c in companies]
        })
    
    # 计算潜在审阅者总数（注意：角色和公司可能包含多个用户）
    total_potential = len(users)  # 直接用户数量确定
    if roles:
        total_potential += len(roles)  # 角色数量（每个角色可能有多个用户）
    if companies:
        total_potential += len(companies)  # 公司数量（每个公司可能有多个用户）
    
    # 判断分配模式
    if len(reviewer_types) == 0:
        assignment_mode = "none"
    elif len(reviewer_types) == 1 and reviewer_types[0]["type"] == "direct_users" and reviewer_types[0]["count"] == 1:
        assignment_mode = "single_user"
    elif len(reviewer_types) == 1 and reviewer_types[0]["type"] == "direct_users":
        assignment_mode = "multiple_users"
    elif any(rt["type"] in ["roles", "companies"] for rt in reviewer_types):
        assignment_mode = "role_or_company_based"
    else:
        assignment_mode = "mixed"
    
    # 检查组审阅配置
    group_review = step.get("groupReview", {})
    is_group_review = group_review.get("enabled", False)
    
    return {
        "has_reviewers": total_potential > 0,
        "reviewer_types": reviewer_types,
        "total_potential_reviewers": total_potential,
        "is_multi_reviewer": total_potential > 1 or is_group_review,
        "assignment_mode": assignment_mode,
        "group_review_enabled": is_group_review,
        "step_type": step.get("type", "UNKNOWN"),
        "summary": {
            "direct_users": len(users),
            "roles": len(roles),
            "companies": len(companies),
            "needs_role_expansion": len(roles) > 0,
            "needs_company_expansion": len(companies) > 0
        }
    }




def _is_file_match(version, file_id):
    """改进的文件匹配逻辑，使用精确匹配"""
    if not version or not file_id:
        return False
    
    # 标准化文件ID
    normalized_file_id = _normalize_file_identifier(file_id)
    
    # 获取版本信息
    version_urn = version.get("urn", "")
    version_item_urn = version.get("itemUrn", "")
    version_name = version.get("name", "")
    
    # 精确匹配策略
    matches = [
        # 1. 精确URN匹配
        version_urn == normalized_file_id,
        version_urn == file_id,
        
        # 2. ItemURN匹配
        version_item_urn == normalized_file_id,
        version_item_urn == file_id,
        
        # 3. 文件名精确匹配
        version_name == normalized_file_id,
        version_name == file_id,
        
        # 4. 如果文件ID看起来像文件名，进行文件名匹配
        version_name and not file_id.startswith('urn:') and version_name.lower() == file_id.lower()
    ]
    
    return any(matches)


def _check_review_for_file(review, file_id, project_id, headers):
    """检查单个评审是否包含指定文件，并返回匹配的文件版本信息"""
    try:
        review_id = review.get('id')
        if not review_id:
            return None
        
        # 获取评审的文件版本
        versions_url = f"{config.AUTODESK_API_BASE}/construction/reviews/v1/projects/{project_id}/reviews/{review_id}/versions"
        versions_response = requests.get(versions_url, headers=headers, timeout=10)
        
        if versions_response.status_code != 200:
            print(f"⚠️ 无法获取评审 {review_id} 的文件版本: {versions_response.status_code}")
            return None
        
        versions_data = versions_response.json()
        versions = versions_data.get("results", [])
        
        # 使用改进的匹配逻辑，同时返回匹配的文件版本信息
        for version in versions:
            if _is_file_match(version, file_id):
                print(f"✅ 在评审 {review_id} 中找到匹配文件: {version.get('name', 'Unknown')}")
                # 返回review和匹配的版本信息，避免重复API调用
                return {
                    'review': review,
                    'matched_version': version,
                    'all_versions': versions
                }
        
        return None
        
    except Exception as e:
        print(f"❌ 检查评审 {review.get('id', 'unknown')} 时出错: {str(e)}")
        return None


def _check_review_contains_file(review, filter_file_urn, filter_file_name, project_id, headers):
    """检查评审是否包含指定的文件（用于过滤）"""
    try:
        review_id = review.get('id')
        if not review_id:
            return False
        
        # 获取评审的文件版本
        versions_url = f"{config.AUTODESK_API_BASE}/construction/reviews/v1/projects/{project_id}/reviews/{review_id}/versions"
        versions_response = requests.get(versions_url, headers=headers, timeout=10)
        
        if versions_response.status_code != 200:
            return False
        
        versions_data = versions_response.json()
        versions = versions_data.get("results", [])
        
        # 检查是否有匹配的文件
        for version in versions:
            if not version:
                continue
            
            # 文件URN匹配
            if filter_file_urn and _is_file_match(version, filter_file_urn):
                return True
            
            # 文件名匹配
            if filter_file_name:
                version_name = version.get("name", "")
                if version_name and filter_file_name.lower() in version_name.lower():
                    return True
        
        return False
        
    except Exception as e:
        print(f"❌ 检查评审 {review.get('id', 'unknown')} 文件时出错: {str(e)}")
        return False


def get_workflow_step_info(project_id, workflow_id, current_step_id, access_token, review_status=None):
    """获取工作流步骤信息，计算当前步骤进度"""
    if not workflow_id:
        return {
            "current_step_number": 0,
            "total_steps": 0,
            "current_step_name": "",
            "progress_percentage": 0,
            "step_progress_text": "No workflow",
            "final_status": "unknown",
            "is_completed": False,
            "is_rejected": False
        }
    
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # 转换项目ID格式（移除 'b.' 前缀）
        from api_modules.submittal_api import convert_project_id
        clean_project_id = convert_project_id(project_id)
        
        # 获取工作流详细信息
        workflow_url = f"{config.AUTODESK_API_BASE}/construction/reviews/v1/projects/{clean_project_id}/workflows/{workflow_id}"
        workflow_resp = requests.get(workflow_url, headers=headers)
        
        if workflow_resp.status_code != 200:
            print(f"Failed to get workflow details: {workflow_resp.status_code}")
            return {
                "current_step_number": 0,
                "total_steps": 0,
                "current_step_name": "",
                "progress_percentage": 0,
                "step_progress_text": "Cannot get workflow info",
                "final_status": "error",
                "is_completed": False,
                "is_rejected": False
            }
        
        workflow_data = workflow_resp.json()
        
        # 处理工作流数据
        steps = workflow_data.get("steps", [])
        total_steps = len(steps)
        
        if total_steps == 0:
            return {
                "current_step_number": 0,
                "total_steps": 0,
                "current_step_name": "",
                "progress_percentage": 0,
                "step_progress_text": "Workflow has no steps",
                "final_status": "empty",
                "is_completed": False,
                "is_rejected": False
            }
        
        # 分析评审状态和最终状态
        is_completed = review_status in ['CLOSED', 'VOID']
        is_rejected = review_status == 'VOID'
        is_approved = review_status == 'CLOSED'
        
        # 查找当前步骤
        current_step_number = 0
        current_step_name = ""
        
        for i, step in enumerate(steps):
            if step and step.get("id") == current_step_id:
                current_step_number = i + 1
                current_step_name = step.get("name", f"Step {i + 1}")
                break
        
        # 如果没有找到匹配的步骤ID，可能是已完成或其他状态
        if current_step_number == 0:
            if is_completed:
                # 根据评审状态确定最终状态
                if is_rejected:
                    final_status = "rejected"
                    progress_text = f"Rejected ({total_steps}/{total_steps})"
                    current_step_name = "Rejected"
                elif is_approved:
                    final_status = "approved"
                    progress_text = f"Approved ({total_steps}/{total_steps})"
                    current_step_name = "Approved"
                else:
                    final_status = "completed"
                    progress_text = f"Completed ({total_steps}/{total_steps})"
                    current_step_name = "Completed"
                
                return {
                    "current_step_number": total_steps,
                    "total_steps": total_steps,
                    "current_step_name": current_step_name,
                    "progress_percentage": 100,
                    "step_progress_text": progress_text,
                    "final_status": final_status,
                    "is_completed": True,
                    "is_rejected": is_rejected
                }
            else:
                # 未找到当前步骤，可能是数据问题
                return {
                    "current_step_number": 0,
                    "total_steps": total_steps,
                    "current_step_name": "Unknown",
                    "progress_percentage": 0,
                    "step_progress_text": "Unknown progress",
                    "final_status": "unknown",
                    "is_completed": False,
                    "is_rejected": False
                }
        
        # 计算进度百分比
        if is_completed:
            progress_percentage = 100
            if is_rejected:
                final_status = "rejected"
                progress_text = f"Rejected ({total_steps}/{total_steps})"
            elif is_approved:
                final_status = "approved"
                progress_text = f"Approved ({total_steps}/{total_steps})"
            else:
                final_status = "completed"
                progress_text = f"Completed ({total_steps}/{total_steps})"
        else:
            progress_percentage = round((current_step_number / total_steps) * 100, 1)
            final_status = "in_progress"
            progress_text = f"Step {current_step_number} / {total_steps} ({progress_percentage}%)"
        
        return {
            "current_step_number": current_step_number,
            "total_steps": total_steps,
            "current_step_name": current_step_name,
            "progress_percentage": progress_percentage,
            "step_progress_text": progress_text,
            "workflow_name": workflow_data.get("name", ""),
            "workflow_description": workflow_data.get("description", ""),
            "final_status": final_status,
            "is_completed": is_completed,
            "is_rejected": is_rejected
        }
        
    except Exception as e:
        print(f"Error getting workflow step info: {str(e)}")
        return {
            "current_step_number": 0,
            "total_steps": 0,
            "current_step_name": "",
            "progress_percentage": 0,
            "step_progress_text": f"Failed to get progress: {str(e)}",
            "final_status": "error",
            "is_completed": False,
            "is_rejected": False
        }




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
    
    # 转换项目ID格式（移除 'b.' 前缀）
    from api_modules.submittal_api import convert_project_id
    clean_project_id = convert_project_id(project_id)
    print(f"🔧 Reviews API: 原始项目ID: {project_id}, 转换后: {clean_project_id}")
    
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
    
    # 新增：文件URN过滤参数（自定义实现）
    filter_file_urn = request.args.get('filter[fileUrn]', '')
    filter_file_name = request.args.get('filter[fileName]', '')
    
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
        reviews_url = f"{config.AUTODESK_API_BASE}/construction/reviews/v1/projects/{clean_project_id}/reviews"
        reviews_resp = requests.get(reviews_url, headers=headers, params=params)
        
        print(f"API请求URL: {reviews_url}")
        print(f"API请求参数: {params}")
        print(f"API响应状态码: {reviews_resp.status_code}")
        
        if reviews_resp.status_code != 200:
            error_text = reviews_resp.text
            print(f"API错误响应: {error_text}")
            raise Exception(f"Failed to get review list: {reviews_resp.status_code} - {error_text}")
        
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
            raise Exception(f"API response data format error: {str(e)}")
        
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
        
        # 新增：文件过滤逻辑
        if filter_file_urn or filter_file_name:
            print(f"🔍 应用文件过滤: URN={filter_file_urn}, Name={filter_file_name}")
            filtered_reviews = []
            file_filter_start_time = time.time()
            
            # 使用并行处理来加速文件过滤
            max_workers = min(8, len(reviews_list))
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # 为每个评审提交文件检查任务
                future_to_review = {}
                for review in reviews_list:
                    if review and review.get('id'):
                        future = executor.submit(_check_review_contains_file, 
                                               review, filter_file_urn, filter_file_name, 
                                               project_id, headers)
                        future_to_review[future] = review
                
                # 收集过滤结果
                for future in as_completed(future_to_review):
                    try:
                        contains_file = future.result(timeout=10)
                        if contains_file:
                            review = future_to_review[future]
                            filtered_reviews.append(review)
                            print(f"✅ 评审 {review.get('id')} 包含目标文件")
                    except Exception as e:
                        print(f"❌ 文件过滤检查出错: {str(e)}")
                        continue
            
            file_filter_time = round(time.time() - file_filter_start_time, 2)
            print(f"🎯 文件过滤完成: {len(reviews_list)} -> {len(filtered_reviews)} 个评审，耗时 {file_filter_time} 秒")
            
            reviews_list = filtered_reviews
        
        # 生成评审分析数据
        reviews_analysis = []
        
        for review in reviews_list:
            if not review:  # 跳过空的review对象
                continue
                
            # 安全获取nextActionBy数据
            next_action_by = review.get("nextActionBy") or {}
            claimed_by = next_action_by.get("claimedBy") or []
            candidates = next_action_by.get("candidates") or {}
            
            # 获取工作流步骤进度信息
            workflow_id = review.get("workflowId", "")
            current_step_id = review.get("currentStepId", "")
            review_status = review.get("status", "")
            step_progress = get_workflow_step_info(project_id, workflow_id, current_step_id, access_token, review_status)
            
            # 分析审阅者类型（主要 vs 可选）
            reviewer_analysis = _analyze_reviewer_types(claimed_by, candidates)
            
            # 提取详细的候选人信息
            candidate_details = {
                "users": [],
                "roles": [],
                "companies": [],
                "claimed_users": []
            }
            
            # 处理已认领用户
            for user in claimed_by:
                if user:
                    candidate_details["claimed_users"].append({
                        "id": user.get("id", ""),
                        "name": user.get("name", ""),
                        "email": user.get("email", ""),
                        "autodeskId": user.get("autodeskId", "")
                    })
            
            # 处理候选用户
            for user in candidates.get("users", []):
                if user:
                    candidate_details["users"].append({
                        "id": user.get("id", ""),
                        "name": user.get("name", ""),
                        "email": user.get("email", ""),
                        "autodeskId": user.get("autodeskId", "")
                    })
            
            # 处理候选角色
            for role in candidates.get("roles", []):
                if role:
                    candidate_details["roles"].append({
                        "id": role.get("id", ""),
                        "name": role.get("name", ""),
                        "description": role.get("description", "")
                    })
            
            # 处理候选公司
            for company in candidates.get("companies", []):
                if company:
                    candidate_details["companies"].append({
                        "id": company.get("id", ""),
                        "name": company.get("name", ""),
                        "trade": company.get("trade", "")
                    })

            analysis = {
                "id": review.get("id", ""),
                "sequence_id": review.get("sequenceId", 0),
                "name": review.get("name", ""),
                "status": review.get("status", ""),
                "current_step_id": current_step_id,
                "current_step_due_date": utils.format_timestamp(review.get("currentStepDueDate", "")),
                "created_by": review.get("createdBy") or {},
                "created_at": utils.format_timestamp(review.get("createdAt", "")),
                "updated_at": utils.format_timestamp(review.get("updatedAt", "")),
                "finished_at": utils.format_timestamp(review.get("finishedAt", "")),
                "archived": review.get("archived", False),
                "archived_by": review.get("archivedBy") or {},
                "archived_at": utils.format_timestamp(review.get("archivedAt", "")),
                "workflow_id": workflow_id,
                "next_action_by": next_action_by,
                "has_claimed_users": len(claimed_by) > 0,
                "candidates_count": {
                    "roles": len(candidates.get("roles") or []),
                    "users": len(candidates.get("users") or []),
                    "companies": len(candidates.get("companies") or [])
                },
                # 新增：详细的候选人信息
                "candidate_details": candidate_details,
                # 新增：审阅者类型分析
                "reviewer_analysis": reviewer_analysis,
                # 新增：工作流步骤进度信息
                "workflow_progress": step_progress
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
            
            # 获取工作流步骤进度信息
            workflow_id = review.get('workflowId', '')
            current_step_id = review.get('currentStepId', '')
            review_status = review.get('status', '')
            step_progress = get_workflow_step_info(project_id, workflow_id, current_step_id, access_token, review_status)
            
            # 分析审阅者类型（主要 vs 可选）
            reviewer_analysis = _analyze_reviewer_types(claimed_by, candidates)
            
            review_analysis = {
                "review_number": i + 1,
                "basic_info": {
                    "id": review.get('id', 'N/A'),
                    "sequence_id": review.get('sequenceId', 'N/A'),
                    "name": review.get('name', 'N/A'),
                    "status": review.get('status', 'N/A'),
                    "workflow_id": workflow_id,
                    "created_at": utils.format_timestamp(review.get('createdAt', '')),
                    "updated_at": utils.format_timestamp(review.get('updatedAt', '')),
                    "finished_at": utils.format_timestamp(review.get('finishedAt', ''))
                },
                "review_summary": {
                    "current_step_id": current_step_id,
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
                },
                # 新增：审阅者类型分析
                "reviewer_analysis": reviewer_analysis,
                # 新增：工作流步骤进度信息
                "workflow_progress": step_progress
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
        project_id = config.DEFAULT_PROJECT_ID
    
    return get_project_reviews(project_id)


@reviews_bp.route('/api/reviews/jarvis')
def get_jarvis_reviews_simple():
    """
    获取项目的评审数据 - 支持动态项目ID和文件过滤
    
    支持的查询参数：
    - projectId: 项目ID（必需）
    - filter[fileUrn]: 按文件URN过滤评审
    - filter[fileName]: 按文件名过滤评审
    - 其他标准过滤参数...
    
    示例：
    - 获取所有评审: /api/reviews/jarvis?projectId=xxx
    - 按文件URN过滤: /api/reviews/jarvis?projectId=xxx&filter[fileUrn]=urn:adsk.wipprod:fs.file:vf.xxx
    - 按文件名过滤: /api/reviews/jarvis?projectId=xxx&filter[fileName]=UserGuide.pdf
    """
    # 获取项目ID - 必须通过参数提供
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 参数",
            "message": "请在请求中提供 projectId 参数，例如: ?projectId=your-project-id",
            "status": "error",
            "suggestion": "请先选择一个项目，然后重试"
        }), 400
    
    print(f"🚀 Reviews API: 使用项目ID: {project_id}")
    
    # 检查是否有文件过滤参数
    filter_file_urn = request.args.get('filter[fileUrn]', '')
    filter_file_name = request.args.get('filter[fileName]', '')
    
    if filter_file_urn or filter_file_name:
        print(f"🔍 应用文件过滤: URN={filter_file_urn}, Name={filter_file_name}")
    
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
    
    # 转换项目ID格式（移除 'b.' 前缀）
    from api_modules.submittal_api import convert_project_id
    clean_project_id = convert_project_id(project_id)
    print(f"🔧 Reviews API: 原始项目ID: {project_id}, 转换后: {clean_project_id}")
    
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
        workflows_url = f"{config.AUTODESK_API_BASE}/construction/reviews/v1/projects/{clean_project_id}/workflows"
        workflows_resp = requests.get(workflows_url, headers=headers, params=params)
        
        if workflows_resp.status_code != 200:
            raise Exception(f"Failed to get workflow list: {workflows_resp.status_code} - {workflows_resp.text}")
        
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
                        "group_review_analysis": _analyze_group_review_config(step.get('groupReview', {})),
                        "candidates": {
                            "roles_count": len(step.get('candidates', {}).get('roles', [])),
                            "users_count": len(step.get('candidates', {}).get('users', [])),
                            "companies_count": len(step.get('candidates', {}).get('companies', [])),
                            "roles": step.get('candidates', {}).get('roles', []),
                            "users": step.get('candidates', {}).get('users', []),
                            "companies": step.get('candidates', {}).get('companies', [])
                        },
                        # 添加审阅者类型分析（基于工作流定义）
                        "reviewer_type_analysis": _analyze_workflow_step_reviewer_types(step)
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
        project_id = config.DEFAULT_PROJECT_ID
    
    return get_project_workflows(project_id)


@reviews_bp.route('/api/reviews/workflows/jarvis')
def get_jarvis_workflows_simple():
    """获取项目的审批工作流数据 - 支持动态项目ID"""
    # 获取项目ID - 必须通过参数提供
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 参数",
            "message": "请在请求中提供 projectId 参数，例如: ?projectId=your-project-id",
            "status": "error",
            "suggestion": "请先选择一个项目，然后重试"
        }), 400
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
            raise Exception(f"Failed to get review workflow: {workflow_resp.status_code} - {error_text}")
        
        try:
            workflow_data = workflow_resp.json()
            print(f"API响应数据: {workflow_data}")
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            raise Exception(f"API response data format error: {str(e)}")
        
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
                "group_review_analysis": _analyze_group_review_config(step.get("groupReview") or {}),
                "candidates": {
                    "roles": candidates.get("roles") or [],
                    "users": candidates.get("users") or [],
                    "companies": candidates.get("companies") or [],
                    "roles_count": len(candidates.get("roles") or []),
                    "users_count": len(candidates.get("users") or []),
                    "companies_count": len(candidates.get("companies") or [])
                },
                # 添加审阅者类型分析（基于工作流定义）
                "reviewer_type_analysis": _analyze_workflow_step_reviewer_types(step)
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
    """获取指定项目中指定评审的工作流"""
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 参数",
            "message": "请在请求中提供 projectId 参数",
            "status": "error"
        }), 400
    
    return get_review_workflow(project_id, review_id)


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
            raise Exception(f"Failed to get review file versions: {versions_resp.status_code} - {error_text}")
        
        try:
            versions_data = versions_resp.json()
            print(f"API响应数据: {versions_data}")
            
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            raise Exception(f"API response data format error: {str(e)}")
        
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
            
            # 处理审批状态 - 只有当审批状态有有效数据时才创建对象
            processed_approve_status = None
            if approve_status and (approve_status.get("id") or approve_status.get("label") or approve_status.get("value")):
                processed_approve_status = {
                    "id": approve_status.get("id", ""),
                    "label": approve_status.get("label", ""),
                    "value": approve_status.get("value", ""),
                    "status_type": get_approve_status_type(approve_status.get("value", ""))
                }
            
            analysis = {
                "urn": version.get("urn", ""),
                "item_urn": version.get("itemUrn", ""),
                "name": version.get("name", ""),
                "version_number": version_number,
                "file_size": file_size,
                "created_date": utils.format_timestamp(created_date) if created_date else "",
                "modified_date": utils.format_timestamp(modified_date) if modified_date else "",
                "approve_status": processed_approve_status,
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
            if version["approve_status"]:
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
    """获取指定项目中指定评审的文件版本"""
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 参数",
            "message": "请在请求中提供 projectId 参数",
            "status": "error"
        }), 400
    
    return get_review_versions(project_id, review_id)


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
            raise Exception(f"Failed to get file approval history: {approval_resp.status_code} - {error_text}")
        
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
            raise Exception(f"API response data format error: {str(e)}")
        
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
                    "name": review_info.get("name", ""),
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
    """获取指定项目中指定文件版本的审批历史"""
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 参数",
            "message": "请在请求中提供 projectId 参数",
            "status": "error"
        }), 400
    
    return get_version_approval_statuses(project_id, version_id)


@reviews_bp.route('/api/reviews/file-workflows/<project_id>/<path:file_id>', methods=['GET'])
def get_file_workflows(project_id, file_id):
    """获取文件关联的工作流（优化版本）"""
    start_time = time.time()
    print(f"🔍 get_file_workflows - 开始处理请求")
    print(f"📋 接收参数: project_id={project_id}, file_id={file_id}")
    
    try:
        access_token = utils.get_access_token()
        if not access_token:
            print("❌ 未找到访问令牌")
            return jsonify({
                "success": False,
                "error": "Failed to get access token"
            }), 401
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # 转换项目ID格式（移除 'b.' 前缀）
        from api_modules.submittal_api import convert_project_id
        clean_project_id = convert_project_id(project_id)
        print(f"🔧 File Workflows API: 原始项目ID: {project_id}, 转换后: {clean_project_id}")
        
        # 直接从API获取评审数据（移除缓存以避免跨文件查询污染）
        reviews_url = f"{config.AUTODESK_API_BASE}/construction/reviews/v1/projects/{clean_project_id}/reviews"
        print(f"📡 从API获取项目评审: {reviews_url}")
        
        # 添加分页参数以获取更多数据
        params = {
            'limit': 50,  # 每页最大数量
            'offset': 0
        }
        
        response = requests.get(reviews_url, headers=headers, params=params, timeout=30)
        
        if response.status_code != 200:
            error_msg = f"Failed to get project reviews: {response.status_code}"
            if response.text:
                try:
                    error_data = response.json()
                    error_msg += f" - {error_data.get('detail', response.text)}"
                except:
                    error_msg += f" - {response.text}"
            
            return jsonify({
                "success": False,
                "error": error_msg
            }), response.status_code
        
        reviews_data = response.json()
        
        all_reviews = reviews_data.get("results", [])
        print(f"📊 总评审数量: {len(all_reviews)}")
        
        if not all_reviews:
            return jsonify({
                "success": True,
                "workflows": [],
                "total_count": 0,
                "message": "No reviews found in project",
                "processing_time": round(time.time() - start_time, 2)
            })
        
        # 优化：使用更保守的并发策略以避免API限制
        file_workflows = []
        max_workers = min(5, len(all_reviews))  # 减少并发数以提高稳定性
        
        print(f"🚀 使用 {max_workers} 个线程并行检查评审（优化版本）")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任务
            future_to_review = {
                executor.submit(_check_review_for_file, review, file_id, project_id, headers): review
                for review in all_reviews
            }
            
            # 收集结果
            for future in as_completed(future_to_review):
                try:
                    result = future.result(timeout=15)  # 15秒超时
                    if result:
                        matching_review = result['review']
                        matched_version = result['matched_version']
                        
                        # 移除工作流进度查询以优化性能
                        # 工作流进度信息可以在需要时单独获取
                        workflow_progress = None
                        
                        # 直接从已获取的版本信息中提取文件审阅状态，避免重复API调用
                        file_approval_status = None
                        try:
                            approve_status = matched_version.get("approveStatus")
                            if approve_status:
                                file_approval_status = {
                                    "id": approve_status.get("id"),
                                    "label": approve_status.get("label"),
                                    "value": approve_status.get("value")
                                }
                        except Exception as e:
                            print(f"⚠️ 提取文件审阅状态失败: {str(e)}")
                        
                        # 构建工作流信息
                        workflow_info = {
                            "id": matching_review["id"],
                            "name": matching_review["name"],
                            "sequenceId": matching_review["sequenceId"],
                            "status": matching_review["status"],
                            "workflowId": matching_review.get("workflowId"),
                            "currentStepId": matching_review.get("currentStepId"),
                            "currentStepDueDate": matching_review.get("currentStepDueDate"),
                            "createdAt": matching_review.get("createdAt"),
                            "updatedAt": matching_review.get("updatedAt"),
                            "finishedAt": matching_review.get("finishedAt"),
                            "createdBy": matching_review.get("createdBy"),
                            "nextActionBy": matching_review.get("nextActionBy"),
                            "workflowProgress": workflow_progress,
                            "archived": matching_review.get("archived", False),
                            "archivedAt": matching_review.get("archivedAt"),
                            "archivedBy": matching_review.get("archivedBy"),
                            "fileApprovalStatus": file_approval_status  # 新增：文件审阅状态
                        }
                        
                        file_workflows.append(workflow_info)
                        print(f"✅ 找到工作流: {matching_review['name']} (ID: {matching_review['id']})")
                
                except Exception as e:
                    print(f"❌ 处理评审时出错: {str(e)}")
                    continue
        
        processing_time = round(time.time() - start_time, 2)
        print(f"🎯 找到 {len(file_workflows)} 个工作流，耗时 {processing_time} 秒")
        
        response = jsonify({
            "success": True,
            "workflows": file_workflows,
            "total_count": len(file_workflows),
            "total_reviews_checked": len(all_reviews),
            "processing_time": processing_time,
            "message": f"Successfully found {len(file_workflows)} workflows for file"
        })
        
        # 添加防缓存头
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        
        return response
        
    except Exception as e:
        processing_time = round(time.time() - start_time, 2)
        print(f"❌ get_file_workflows 出错: {str(e)}")
        response = jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}",
            "processing_time": processing_time
        })
        
        # 添加防缓存头
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        
        return response, 500


# ==================== 便捷的文件工作流查询接口 ====================

# ==================== 单个工作流查询接口 ====================

@reviews_bp.route('/api/workflows/<project_id>/<workflow_id>')
def get_single_workflow(project_id, workflow_id):
    """获取指定项目中的单个工作流详情"""
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
    
    # 转换项目ID格式（移除 'b.' 前缀）
    from api_modules.submittal_api import convert_project_id
    clean_project_id = convert_project_id(project_id)
    print(f"🔧 Single Workflow API: 原始项目ID: {project_id}, 转换后: {clean_project_id}")
    
    try:
        # 调用 Autodesk Construction Cloud Reviews API
        workflow_url = f"{config.AUTODESK_API_BASE}/construction/reviews/v1/projects/{clean_project_id}/workflows/{workflow_id}"
        
        print(f"API请求URL: {workflow_url}")
        
        workflow_resp = requests.get(workflow_url, headers=headers, timeout=30)
        
        print(f"API响应状态码: {workflow_resp.status_code}")
        
        if workflow_resp.status_code != 200:
            error_text = workflow_resp.text
            print(f"API错误响应: {error_text}")
            raise Exception(f"Failed to get workflow details: {workflow_resp.status_code} - {error_text}")
        
        try:
            workflow_data = workflow_resp.json()
            print(f"API响应数据: {workflow_data}")
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            raise Exception(f"API response data format error: {str(e)}")
        
        if not workflow_data:
            print("API返回空工作流数据")
            workflow_data = {}
        
        # 生成工作流分析数据
        workflow_analysis = {
            "id": workflow_data.get("id", ""),
            "name": workflow_data.get("name", ""),
            "description": workflow_data.get("description", ""),
            "notes": workflow_data.get("notes", ""),
            "status": workflow_data.get("status", ""),
            "created_at": utils.format_timestamp(workflow_data.get("createdAt", "")),
            "updated_at": utils.format_timestamp(workflow_data.get("updatedAt", "")),
            "steps_count": len(workflow_data.get("steps", [])),
            "approval_options_count": len(workflow_data.get("approvalStatusOptions", [])),
            "has_copy_files": workflow_data.get("copyFilesOptions", {}).get("enabled", False),
            "has_attached_attributes": len(workflow_data.get("attachedAttributes", [])) > 0,
            "additional_options": workflow_data.get("additionalOptions", {}),
            "steps": workflow_data.get("steps", []),
            "approval_status_options": workflow_data.get("approvalStatusOptions", []),
            "copy_files_options": workflow_data.get("copyFilesOptions", {}),
            "attached_attributes": workflow_data.get("attachedAttributes", []),
            "update_attributes_options": workflow_data.get("updateAttributesOptions", {})
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
                "group_review_analysis": _analyze_group_review_config(step.get("groupReview") or {}),
                "candidates": {
                    "roles": candidates.get("roles") or [],
                    "users": candidates.get("users") or [],
                    "companies": candidates.get("companies") or [],
                    "roles_count": len(candidates.get("roles") or []),
                    "users_count": len(candidates.get("users") or []),
                    "companies_count": len(candidates.get("companies") or [])
                },
                # 添加审阅者类型分析（基于工作流定义）
                "reviewer_type_analysis": _analyze_workflow_step_reviewer_types(step)
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
            "workflow_id": workflow_id,
            "workflow": workflow_analysis,
            "detailed_steps": detailed_steps,
            "approval_options": approval_options_analysis,
            "raw_data": workflow_data,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"获取单个工作流时出错: {str(e)}")
        return jsonify({
            "error": f"获取工作流详情失败: {str(e)}",
            "status": "error"
        }), 500


@reviews_bp.route('/api/workflows/jarvis/<workflow_id>')
def get_jarvis_single_workflow(workflow_id):
    """获取指定项目中的单个工作流详情（简化路由）"""
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 参数",
            "message": "请在请求中提供 projectId 参数",
            "status": "error"
        }), 400
    
    return get_single_workflow(project_id, workflow_id)


# ==================== 单个评审查询接口 ====================

@reviews_bp.route('/api/review/<project_id>/<review_id>')
def get_single_review(project_id, review_id):
    """获取指定项目中的单个评审详情"""
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
        review_url = f"{config.AUTODESK_API_BASE}/construction/reviews/v1/projects/{project_id}/reviews/{review_id}"
        
        print(f"API请求URL: {review_url}")
        
        review_resp = requests.get(review_url, headers=headers, timeout=30)
        
        print(f"API响应状态码: {review_resp.status_code}")
        
        if review_resp.status_code != 200:
            error_text = review_resp.text
            print(f"API错误响应: {error_text}")
            raise Exception(f"Failed to get review details: {review_resp.status_code} - {error_text}")
        
        try:
            review_data = review_resp.json()
            print(f"API响应数据: {review_data}")
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            raise Exception(f"API response data format error: {str(e)}")
        
        if not review_data:
            print("API返回空评审数据")
            review_data = {}
        
        # 安全获取nextActionBy数据
        next_action_by = review_data.get("nextActionBy") or {}
        claimed_by = next_action_by.get("claimedBy") or []
        candidates = next_action_by.get("candidates") or {}
        
        # 获取工作流步骤进度信息
        workflow_id = review_data.get("workflowId", "")
        current_step_id = review_data.get("currentStepId", "")
        review_status = review_data.get("status", "")
        step_progress = get_workflow_step_info(project_id, workflow_id, current_step_id, access_token, review_status)
        
        # 分析审阅者类型（主要 vs 可选）
        reviewer_analysis = _analyze_reviewer_types(claimed_by, candidates)
        
        # 生成评审分析数据
        review_analysis = {
            "id": review_data.get("id", ""),
            "sequence_id": review_data.get("sequenceId", 0),
            "name": review_data.get("name", ""),
            "status": review_data.get("status", ""),
            "current_step_id": current_step_id,
            "current_step_due_date": utils.format_timestamp(review_data.get("currentStepDueDate", "")),
            "created_by": review_data.get("createdBy") or {},
            "created_at": utils.format_timestamp(review_data.get("createdAt", "")),
            "updated_at": utils.format_timestamp(review_data.get("updatedAt", "")),
            "finished_at": utils.format_timestamp(review_data.get("finishedAt", "")),
            "archived": review_data.get("archived", False),
            "archived_by": review_data.get("archivedBy") or {},
            "archived_at": utils.format_timestamp(review_data.get("archivedAt", "")),
            "workflow_id": workflow_id,
            "next_action_by": next_action_by,
            "has_claimed_users": len(claimed_by) > 0,
            "candidates_count": {
                "roles": len(candidates.get("roles") or []),
                "users": len(candidates.get("users") or []),
                "companies": len(candidates.get("companies") or [])
            },
            # 审阅者类型分析
            "reviewer_analysis": reviewer_analysis,
            # 工作流步骤进度信息
            "workflow_progress": step_progress
        }
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "review_id": review_id,
            "review": review_analysis,
            "raw_data": review_data,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"获取单个评审时出错: {str(e)}")
        return jsonify({
            "error": f"获取评审详情失败: {str(e)}",
            "status": "error"
        }), 500


@reviews_bp.route('/api/review/jarvis/<review_id>')
def get_jarvis_single_review(review_id):
    """获取指定项目中的单个评审详情（简化路由）"""
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 参数",
            "message": "请在请求中提供 projectId 参数",
            "status": "error"
        }), 400
    
    return get_single_review(project_id, review_id)


# ==================== 评审进度历史接口 ====================

@reviews_bp.route('/api/reviews/<project_id>/<review_id>/progress')
def get_review_progress(project_id, review_id):
    """获取指定评审的进度历史记录"""
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
        # 调用 Autodesk Construction Cloud Reviews API
        progress_url = f"{config.AUTODESK_API_BASE}/construction/reviews/v1/projects/{project_id}/reviews/{review_id}/progress"
        
        print(f"API请求URL: {progress_url}")
        print(f"API请求参数: {params}")
        
        progress_resp = requests.get(progress_url, headers=headers, params=params, timeout=30)
        
        print(f"API响应状态码: {progress_resp.status_code}")
        
        if progress_resp.status_code != 200:
            error_text = progress_resp.text
            print(f"API错误响应: {error_text}")
            raise Exception(f"Failed to get review progress: {progress_resp.status_code} - {error_text}")
        
        try:
            progress_data = progress_resp.json()
            print(f"API响应数据: {progress_data}")
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            raise Exception(f"API response data format error: {str(e)}")
        
        if not progress_data:
            print("API返回空进度数据")
            progress_data = {"results": [], "pagination": {}}
        
        progress_list = progress_data.get("results", [])
        pagination = progress_data.get("pagination", {})
        
        # 生成进度分析数据
        progress_analysis = []
        for progress in progress_list:
            if not progress:
                continue
            
            candidates = progress.get("candidates") or {}
            claimed_by = progress.get("claimedBy") or {}
            action_by = progress.get("actionBy") or {}
            
            analysis = {
                "step_id": progress.get("stepId", ""),
                "step_name": progress.get("stepName", ""),
                "status": progress.get("status", ""),
                "claimed_by": claimed_by,
                "action_by": action_by,
                "candidates": {
                    "roles": candidates.get("roles") or [],
                    "users": candidates.get("users") or [],
                    "companies": candidates.get("companies") or [],
                    "roles_count": len(candidates.get("roles") or []),
                    "users_count": len(candidates.get("users") or []),
                    "companies_count": len(candidates.get("companies") or [])
                },
                "end_time": utils.format_timestamp(progress.get("endTime", "")),
                "notes": progress.get("notes", ""),
                "has_claimed_user": bool(claimed_by),
                "has_action_user": bool(action_by),
                "is_completed": progress.get("status") in ["SUBMITTED", "APPROVED", "REJECTED"],
                "is_claimed": progress.get("status") == "CLAIMED",
                "is_pending": progress.get("status") == "PENDING",
                "step_type": get_step_type_from_candidates(candidates),
                "action_summary": get_action_summary(progress.get("status"), claimed_by, action_by)
            }
            progress_analysis.append(analysis)
        
        # 生成统计信息
        total_progress = pagination.get('totalResults', len(progress_list))
        status_counts = {}
        for progress in progress_analysis:
            status = progress["status"]
            if status:
                status_counts[status] = status_counts.get(status, 0) + 1
        
        completed_count = len([p for p in progress_analysis if p["is_completed"]])
        claimed_count = len([p for p in progress_analysis if p["is_claimed"]])
        pending_count = len([p for p in progress_analysis if p["is_pending"]])
        
        stats = {
            "total_progress": total_progress,
            "current_page_count": len(progress_list),
            "status_counts": status_counts,
            "completed_count": completed_count,
            "claimed_count": claimed_count,
            "pending_count": pending_count,
            "progress_completion_rate": round((completed_count / len(progress_analysis)) * 100, 1) if progress_analysis else 0
        }
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "review_id": review_id,
            "query_params": params,
            "stats": stats,
            "progress": progress_analysis,
            "pagination": pagination,
            "raw_data": progress_list,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"获取评审进度时出错: {str(e)}")
        return jsonify({
            "error": f"获取评审进度失败: {str(e)}",
            "status": "error"
        }), 500


@reviews_bp.route('/api/reviews/jarvis/<review_id>/progress')
def get_jarvis_review_progress(review_id):
    """获取指定项目中指定评审的进度历史（简化路由）"""
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 参数",
            "message": "请在请求中提供 projectId 参数",
            "status": "error"
        }), 400
    
    return get_review_progress(project_id, review_id)


# 辅助函数
def get_step_type_from_candidates(candidates):
    """根据候选者信息推断步骤类型"""
    if not candidates:
        return "unknown"
    
    users = candidates.get("users", [])
    roles = candidates.get("roles", [])
    companies = candidates.get("companies", [])
    
    if users and not roles and not companies:
        return "direct_assignment"
    elif roles and not users and not companies:
        return "role_based"
    elif companies and not users and not roles:
        return "company_based"
    elif users or roles or companies:
        return "mixed_assignment"
    else:
        return "no_assignment"


def get_action_summary(status, claimed_by, action_by):
    """生成操作摘要"""
    if not status:
        return "No status information"
    
    if status == "PENDING":
        return "Waiting to be claimed"
    elif status == "CLAIMED":
        if claimed_by:
            return f"Claimed by {claimed_by.get('name', 'Unknown user')}"
        return "Claimed"
    elif status == "SUBMITTED":
        if action_by:
            return f"Submitted by {action_by.get('name', 'Unknown user')}"
        return "Submitted"
    elif status == "APPROVED":
        if action_by:
            return f"Approved by {action_by.get('name', 'Unknown user')}"
        return "Approved"
    elif status == "REJECTED":
        if action_by:
            return f"Rejected by {action_by.get('name', 'Unknown user')}"
        return "Rejected"
    else:
        return f"Status: {status}"


@reviews_bp.route('/api/reviews/by-file/<project_id>/<path:file_id>')
def get_reviews_by_file(project_id, file_id):
    """
    通过文件ID获取相关的评审工作流（新的便捷接口）
    
    这个接口结合了优化的文件匹配和Reviews API的文件过滤功能
    提供更好的性能和准确性
    
    参数：
    - project_id: 项目ID
    - file_id: 文件ID/URN
    
    返回：包含工作流信息的评审列表
    """
    start_time = time.time()
    print(f"🔍 get_reviews_by_file - 开始处理请求")
    print(f"📋 接收参数: project_id={project_id}, file_id={file_id}")
    
    try:
        access_token = utils.get_access_token()
        if not access_token:
            return jsonify({
                "success": False,
                "error": "Failed to get access token"
            }), 401
        
        # 使用扩展的Reviews API进行文件过滤查询
        # 构建查询参数，使用文件URN过滤
        from flask import request as flask_request
        
        # 临时修改request.args来传递过滤参数
        original_args = flask_request.args
        
        # 创建新的查询参数
        new_args = dict(original_args)
        new_args['filter[fileUrn]'] = file_id
        new_args['limit'] = '50'  # 增加限制以获取更多结果
        
        # 临时替换request.args
        flask_request.args = type(original_args)(new_args)
        
        try:
            # 调用优化的评审查询函数
            result = get_project_reviews(project_id)
            
            # 从结果中提取评审数据
            if hasattr(result, 'get_json'):
                result_data = result.get_json()
            else:
                result_data = result
            
            if result_data and result_data.get('success'):
                reviews = result_data.get('reviews', [])
                
                # 转换为工作流格式
                workflows = []
                for review in reviews:
                    workflow_info = {
                        "id": review.get("id"),
                        "name": review.get("name"),
                        "sequenceId": review.get("sequence_id"),
                        "status": review.get("status"),
                        "workflowId": review.get("workflow_id"),
                        "currentStepId": review.get("current_step_id"),
                        "currentStepDueDate": review.get("current_step_due_date"),
                        "createdAt": review.get("created_at"),
                        "updatedAt": review.get("updated_at"),
                        "finishedAt": review.get("finished_at"),
                        "createdBy": review.get("created_by"),
                        "nextActionBy": review.get("next_action_by"),
                        "workflowProgress": review.get("workflow_progress"),
                        "archived": review.get("archived", False),
                        "archivedAt": review.get("archived_at"),
                        "archivedBy": review.get("archived_by")
                    }
                    workflows.append(workflow_info)
                
                processing_time = round(time.time() - start_time, 2)
                
                response = jsonify({
                    "success": True,
                    "workflows": workflows,
                    "total_count": len(workflows),
                    "processing_time": processing_time,
                    "method": "enhanced_reviews_api_filtering",
                    "message": f"Successfully found {len(workflows)} workflows using enhanced API filtering"
                })
                
                # 添加防缓存头
                response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                response.headers['Pragma'] = 'no-cache'
                response.headers['Expires'] = '0'
                
                return response
            else:
                # 如果API过滤失败，回退到原始方法
                print("⚠️ API过滤失败，回退到原始文件工作流查询方法")
                return get_file_workflows(project_id, file_id)
                
        finally:
            # 恢复原始的request.args
            flask_request.args = original_args
        
    except Exception as e:
        processing_time = round(time.time() - start_time, 2)
        print(f"❌ get_reviews_by_file 出错: {str(e)}")
        
        # 出错时回退到原始方法
        print("⚠️ 出错，回退到原始文件工作流查询方法")
        return get_file_workflows(project_id, file_id)


