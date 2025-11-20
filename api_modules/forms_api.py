# -*- coding: utf-8 -*-
"""
Forms API 相关模块
处理 ACC Forms API 的所有功能
"""

import requests
import json
from flask import Blueprint, jsonify, Response
from datetime import datetime
import config
import utils

forms_bp = Blueprint('forms', __name__)


@forms_bp.route('/api/forms/jarvis')
def get_jarvis_forms():
    """获取项目的表单数据 - 支持动态项目ID"""
    from flask import request
    
    access_token = utils.get_access_token()
    if not access_token:
        return jsonify({
            "error": "未找到 Access Token，请先进行认证",
            "status": "unauthorized"
        }), 401
    
    # 获取项目ID - 必须通过参数提供
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 参数",
            "message": "请在请求中提供 projectId 参数，例如: ?projectId=your-project-id",
            "status": "error",
            "suggestion": "请先选择一个项目，然后重试"
        }), 400
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        print(f"🚀 Forms API: 使用项目ID: {project_id}")
        
        # 获取表单列表
        forms_url = f"{config.AUTODESK_API_BASE}/construction/forms/v1/projects/{project_id}/forms"
        forms_resp = requests.get(forms_url, headers=headers)
        
        if forms_resp.status_code != 200:
            raise Exception(f"获取表单列表失败: {forms_resp.status_code} - {forms_resp.text}")
        
        forms_data = forms_resp.json()
        forms_list = forms_data.get("data", [])
        
        # 生成表单分析
        forms_analysis = []
        for form in forms_list:
            analysis = {
                "id": form.get("id"),
                "name": form.get("name"),
                "status": form.get("status"),
                "created_at": utils.format_timestamp(form.get("createdAt", "")),
                "updated_at": utils.format_timestamp(form.get("updatedAt", "")),
                "created_by": form.get("createdBy"),
                "form_date": form.get("formDate"),
                "work_records": {
                    "worklog_entries": utils.safe_get_length(form.get("tabularValues", {}).get("worklogEntries")),
                    "materials_entries": utils.safe_get_length(form.get("tabularValues", {}).get("materialsEntries")),
                    "equipment_entries": utils.safe_get_length(form.get("tabularValues", {}).get("equipmentEntries"))
                },
                "custom_fields": utils.safe_get_length(form.get("customValues")),
                "has_pdf": bool(form.get("pdfUrl")),
                "description": form.get("description", ""),
                "notes": form.get("notes", "")
            }
            forms_analysis.append(analysis)
        
        # 生成详细的工作记录分析 (移除HTML，改为结构化数据)
        detailed_analysis = []
        for i, form in enumerate(forms_list):
            form_analysis = {
                "form_number": i + 1,
                "basic_info": {
                    "id": form.get('id', 'N/A'),
                    "name": form.get('name', 'N/A'),
                    "status": form.get('status', 'N/A'),
                    "form_date": form.get('formDate', 'N/A'),
                    "created_at": utils.format_timestamp(form.get('createdAt', '')),
                    "updated_at": utils.format_timestamp(form.get('updatedAt', '')),
                    "created_by": form.get('createdBy', 'N/A')
                },
                "work_records_summary": {
                    "worklog_entries": utils.safe_get_length(form.get('tabularValues', {}).get('worklogEntries')),
                    "materials_entries": utils.safe_get_length(form.get('tabularValues', {}).get('materialsEntries')),
                    "equipment_entries": utils.safe_get_length(form.get('tabularValues', {}).get('equipmentEntries')),
                    "custom_fields": utils.safe_get_length(form.get('customValues'))
                },
                "detailed_records": {}
            }
            
            # 显示具体的工作记录内容
            tabular_values = form.get("tabularValues", {})
            if tabular_values:
                if tabular_values.get("worklogEntries"):
                    worklog_details = []
                    for entry in tabular_values["worklogEntries"]:
                        hours = entry.get('timespan', 0) / 3600000  # 转换为小时
                        worklog_details.append({
                            "trade": entry.get('trade', 'N/A'),
                            "headcount": entry.get('headcount', 0),
                            "hours": round(hours, 1),
                            "description": entry.get('description', '')
                        })
                    form_analysis["detailed_records"]["worklog_entries"] = worklog_details
                
                if tabular_values.get("materialsEntries"):
                    materials_details = []
                    for entry in tabular_values["materialsEntries"]:
                        materials_details.append({
                            "item": entry.get('item', 'N/A'),
                            "quantity": entry.get('quantity', 0),
                            "unit": entry.get('unit', ''),
                            "description": entry.get('description', '')
                        })
                    form_analysis["detailed_records"]["materials_entries"] = materials_details
                
                if tabular_values.get("equipmentEntries"):
                    equipment_details = []
                    for entry in tabular_values["equipmentEntries"]:
                        hours = entry.get('timespan', 0) / 3600000
                        equipment_details.append({
                            "item": entry.get('item', 'N/A'),
                            "quantity": entry.get('quantity', 0),
                            "hours": round(hours, 1),
                            "description": entry.get('description', '')
                        })
                    form_analysis["detailed_records"]["equipment_entries"] = equipment_details
            
            detailed_analysis.append(form_analysis)
        
        # 返回JSON格式的数据
        result = {
            "status": "success",
            "project_id": project_id,
            "forms_count": len(forms_list),
            "forms": forms_list,
            "analysis": forms_analysis,
            "detailed_analysis": detailed_analysis,
            "raw_data": forms_data
        }
        
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ Forms API错误: {str(e)}")
        return jsonify({
            "error": f"获取表单数据时发生错误: {str(e)}",
            "status": "error",
            "project_id": project_id
        }), 500


@forms_bp.route('/api/forms/export-json')
def export_forms_json():
    """导出表单数据为 JSON 文件"""
    access_token = utils.get_access_token()
    if not access_token:
        return {"error": "No access token found"}, 401
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        # 获取项目ID - 必须通过参数提供
        from flask import request
        project_id = request.args.get('projectId')
        
        if not project_id:
            return jsonify({
                "error": "缺少必需的 projectId 参数",
                "message": "请在请求中提供 projectId 参数",
                "status": "error"
            }), 400
        
        print(f"🚀 Export Forms API: 使用项目ID: {project_id}")
        
        forms_url = f"{config.AUTODESK_API_BASE}/construction/forms/v1/projects/{project_id}/forms"
        forms_resp = requests.get(forms_url, headers=headers)
        
        if forms_resp.status_code != 200:
            return {"error": f"Failed to fetch forms: {forms_resp.status_code}"}, 400
        
        forms_data = forms_resp.json()
        
        # 生成导出数据
        export_data = {
            "export_info": {
                "timestamp": datetime.now().isoformat(),
                "project_id": project_id,
                "total_forms": len(forms_data.get("data", [])),
                "export_type": "Forms API"
            },
            "forms_summary": [],
            "raw_data": forms_data
        }
        
        # 生成表单摘要
        for form in forms_data.get("data", []):
            summary = {
                "id": form.get("id"),
                "name": form.get("name"),
                "status": form.get("status"),
                "created_at": form.get("createdAt"),
                "updated_at": form.get("updatedAt"),
                "created_by": form.get("createdBy"),
                "form_date": form.get("formDate"),
                "work_records": {
                    "worklog_entries": utils.safe_get_length(form.get("tabularValues", {}).get("worklogEntries")),
                    "materials_entries": utils.safe_get_length(form.get("tabularValues", {}).get("materialsEntries")),
                    "equipment_entries": utils.safe_get_length(form.get("tabularValues", {}).get("equipmentEntries"))
                },
                "custom_fields": utils.safe_get_length(form.get("customValues")),
                "has_pdf": bool(form.get("pdfUrl")),
                "workflow_timeline": {
                    "created": form.get("createdAt"),
                    "last_updated": form.get("updatedAt"),
                    "status": form.get("status")
                }
            }
            export_data["forms_summary"].append(summary)
        
        # 生成 JSON 响应
        json_str = json.dumps(export_data, indent=2, ensure_ascii=False)
        response = Response(
            json_str,
            status=200,
            mimetype='application/json'
        )
        response.headers['Content-Disposition'] = f'attachment; filename=jarvis_forms_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        return response
        
    except Exception as e:
        return {"error": str(e)}, 500


@forms_bp.route('/api/test/forms')
def test_forms_api():
    """测试各种 Forms API 端点"""
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
        # 获取真实的 Account ID
        projects_resp = requests.get(f"{config.AUTODESK_API_BASE}/project/v1/hubs", headers=headers)
        
        if projects_resp.status_code != 200:
            raise Exception(f"无法获取项目信息: {projects_resp.status_code}")
        
        projects_data = projects_resp.json()
        hub_id, real_account_id, hub_name = utils.get_real_account_id(projects_data)
        
        if not hub_id:
            raise Exception("没有找到可用的项目")
        
        # 获取项目列表
        projects_url = f"{config.AUTODESK_API_BASE}/project/v1/hubs/{hub_id}/projects"
        projects_list_resp = requests.get(projects_url, headers=headers)
        
        projects_info = []
        project_ids = []
        
        if projects_list_resp.status_code == 200:
            projects_list_data = projects_list_resp.json()
            if "data" in projects_list_data:
                for project in projects_list_data["data"]:
                    project_id = project["id"]
                    project_name = project["attributes"]["name"]
                    projects_info.append({
                        "id": project_id,
                        "name": project_name
                    })
                    project_ids.append(project_id)
        
        # 测试各种 Forms API 端点
        forms_endpoints = []
        
        # 使用真实的 account ID
        forms_endpoints.extend([
            f"{config.AUTODESK_API_BASE}/construction/forms/v1/accounts/{real_account_id}/forms",
            f"{config.AUTODESK_API_BASE}/construction/forms/v2/accounts/{real_account_id}/forms",
        ])
        
        # 对每个项目尝试 Forms API
        for project_id in project_ids[:3]:  # 只测试前3个项目
            forms_endpoints.extend([
                f"{config.AUTODESK_API_BASE}/construction/forms/v1/projects/{project_id}/forms",
                f"{config.AUTODESK_API_BASE}/construction/forms/v2/projects/{project_id}/forms",
            ])
        
        forms_results = []
        
        for endpoint in forms_endpoints:
            try:
                resp = requests.get(endpoint, headers=headers)
                result = {
                    "endpoint": endpoint,
                    "status_code": resp.status_code,
                    "response_preview": resp.text[:300] + "..." if len(resp.text) > 300 else resp.text,
                    "success": resp.status_code == 200
                }
                
                if resp.status_code == 200:
                    try:
                        data = resp.json()
                        result["data_summary"] = {
                            "type": str(type(data)),
                            "keys": list(data.keys()) if isinstance(data, dict) else None,
                            "count": len(data.get("data", [])) if isinstance(data, dict) and "data" in data else len(data) if isinstance(data, list) else None
                        }
                    except:
                        pass
                        
            except Exception as e:
                result = {
                    "endpoint": endpoint,
                    "error": str(e),
                    "success": False
                }
            
            forms_results.append(result)
        
        successful_forms = [r for r in forms_results if r.get("success")]
        
        # 返回JSON格式的测试结果
        result = {
            "status": "success",
            "test_type": "Forms API 专项测试",
            "basic_info": {
                "hub_id": hub_id,
                "hub_name": hub_name,
                "real_account_id": real_account_id,
                "projects_count": len(project_ids)
            },
            "projects": projects_info,
            "forms_api_test_results": {
                "successful_endpoints": len(successful_forms),
                "total_endpoints": len(forms_endpoints),
                "success_rate": len(successful_forms) / len(forms_endpoints) if forms_endpoints else 0
            },
            "successful_endpoints": [r["endpoint"] for r in successful_forms],
            "detailed_results": forms_results,
            "has_available_apis": len(successful_forms) > 0
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "error": f"Forms API 测试失败: {str(e)}",
            "status": "error"
        }), 500


@forms_bp.route('/api/forms/templates')
def get_form_templates():
    """获取表单模板信息，支持分页和筛选参数"""
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
        # 获取查询参数
        from flask import request
        project_id = request.args.get('projectId')
        
        if not project_id:
            return jsonify({
                "error": "缺少必需的 projectId 参数",
                "message": "请在请求中提供 projectId 参数",
                "status": "error"
            }), 400
        
        print(f"🚀 Templates API: 使用项目ID: {project_id}")
        
        offset = request.args.get('offset', 0, type=int)
        limit = request.args.get('limit', 50, type=int)
        sort_order = request.args.get('sortOrder', 'desc')
        updated_after = request.args.get('updatedAfter')
        updated_before = request.args.get('updatedBefore')
        
        # 限制 limit 在 1-50 之间
        limit = max(1, min(50, limit))
        
        # 构建查询参数
        params = {
            'offset': offset,
            'limit': limit,
            'sortOrder': sort_order
        }
        
        # 添加时间筛选参数
        if updated_after:
            params['updatedAfter'] = updated_after
        if updated_before:
            params['updatedBefore'] = updated_before
        
        # 获取表单模板列表
        templates_url = f"{config.AUTODESK_API_BASE}/construction/forms/v1/projects/{project_id}/form-templates"
        templates_resp = requests.get(templates_url, headers=headers, params=params)
        
        if templates_resp.status_code != 200:
            raise Exception(f"获取表单模板失败: {templates_resp.status_code} - {templates_resp.text}")
        
        templates_data = templates_resp.json()
        templates_list = templates_data.get("data", [])
        pagination_info = templates_data.get("pagination", {})
        
        # 记录分页信息
        print(f"获取到 {len(templates_list)} 个模板，分页信息: {pagination_info}")
        
        # 分析每个模板的详细信息
        template_analysis = []
        workflow_architecture = []
        
        for template in templates_list:
            template_id = template.get("id")
            
            # 获取模板详细信息
            template_detail_url = f"{config.AUTODESK_API_BASE}/construction/forms/v1/projects/{project_id}/form-templates/{template_id}"
            detail_resp = requests.get(template_detail_url, headers=headers)
            
            analysis = {
                "id": template_id,
                "name": template.get("name"),
                "created_at": utils.format_timestamp(template.get("createdAt", "")),
                "updated_at": utils.format_timestamp(template.get("updatedAt", "")),
                "created_by": template.get("createdBy"),
                "status": template.get("status"),
                "detail_available": detail_resp.status_code == 200
            }
            
            # 深度分析模板JSON结构
            architecture_info = {
                "template_id": template_id,
                "template_name": template.get("name"),
                "roles_and_permissions": {},
                "statuses": [],
                "workflow_rules": {},
                "participants": [],
                "template_structure": {},
                "form_fields": [],
                "approval_settings": {},
                "all_keys": []
            }
            
            if detail_resp.status_code == 200:
                detail_data = detail_resp.json()
                analysis["detail_data"] = detail_data
                
                # 递归分析所有键值对
                def extract_all_keys(data, prefix=""):
                    keys = []
                    if isinstance(data, dict):
                        for key, value in data.items():
                            full_key = f"{prefix}.{key}" if prefix else key
                            keys.append(full_key)
                            if isinstance(value, (dict, list)):
                                keys.extend(extract_all_keys(value, full_key))
                    elif isinstance(data, list) and data:
                        for i, item in enumerate(data):
                            if isinstance(item, (dict, list)):
                                keys.extend(extract_all_keys(item, f"{prefix}[{i}]"))
                    return keys
                
                architecture_info["all_keys"] = extract_all_keys(detail_data)
                
                # 分析模板结构
                architecture_info["template_structure"] = {
                    "total_keys": len(architecture_info["all_keys"]),
                    "top_level_keys": list(detail_data.keys()) if isinstance(detail_data, dict) else [],
                    "has_form_definition": "formDefinition" in detail_data,
                    "has_workflow": "workflow" in detail_data,
                    "has_settings": "settings" in detail_data,
                    "has_permissions": "permissions" in detail_data
                }
                
                # 查找表单字段
                if "formDefinition" in detail_data:
                    form_def = detail_data["formDefinition"]
                    if "sections" in form_def:
                        for section in form_def["sections"]:
                            if "fields" in section:
                                for field in section["fields"]:
                                    field_info = {
                                        "id": field.get("id"),
                                        "name": field.get("name"),
                                        "type": field.get("type"),
                                        "required": field.get("required", False),
                                        "label": field.get("label")
                                    }
                                    architecture_info["form_fields"].append(field_info)
                
                # 查找审批设置
                approval_related_keys = ["approval", "review", "signature", "status", "workflow", "assignee", "reviewer"]
                for key in approval_related_keys:
                    if key in detail_data:
                        architecture_info["approval_settings"][key] = detail_data[key]
                
                # 深度搜索可能的参与者信息
                def find_participants(data, path=""):
                    participants = []
                    if isinstance(data, dict):
                        # 检查常见的参与者字段名
                        participant_keys = ["participants", "assignees", "reviewers", "approvers", "users", "members"]
                        for key in participant_keys:
                            if key in data and isinstance(data[key], list):
                                for participant in data[key]:
                                    if isinstance(participant, dict):
                                        participants.append({
                                            "source_path": f"{path}.{key}",
                                            "data": participant
                                        })
                        
                        # 递归搜索
                        for key, value in data.items():
                            if isinstance(value, (dict, list)):
                                participants.extend(find_participants(value, f"{path}.{key}" if path else key))
                    elif isinstance(data, list):
                        for i, item in enumerate(data):
                            if isinstance(item, (dict, list)):
                                participants.extend(find_participants(item, f"{path}[{i}]"))
                    return participants
                
                found_participants = find_participants(detail_data)
                architecture_info["participants"] = found_participants
                
                # 深度搜索状态和工作流信息
                def find_workflow_info(data, path=""):
                    workflow_info = {}
                    if isinstance(data, dict):
                        # 检查工作流相关字段
                        workflow_keys = ["workflow", "states", "statuses", "transitions", "flow", "process"]
                        for key in workflow_keys:
                            if key in data:
                                workflow_info[f"{path}.{key}" if path else key] = data[key]
                        
                        # 递归搜索
                        for key, value in data.items():
                            if isinstance(value, dict):
                                workflow_info.update(find_workflow_info(value, f"{path}.{key}" if path else key))
                    return workflow_info
                
                workflow_info = find_workflow_info(detail_data)
                if workflow_info:
                    architecture_info["workflow_rules"] = workflow_info
                
                # 传统方式查找（保持兼容性）
                if "participants" in detail_data:
                    participants = detail_data["participants"]
                    if participants and len(participants) > 0:
                        architecture_info["participants"].extend([{"source_path": "root.participants", "data": p} for p in participants])
            
            # 从模板列表响应中提取权限信息（这里包含了重要的审批架构信息！）
            # 提取用户权限
            user_permissions = template.get("userPermissions", [])
            group_permissions = template.get("groupPermissions", [])
            
            # 分析角色和权限
            roles = {}
            
            # 处理用户权限
            for user_perm in user_permissions:
                user_id = user_perm.get("userId", "unknown")
                permissions = user_perm.get("permissions", [])
                roles[f"user_{user_id}"] = {
                    "type": "user",
                    "permissions": permissions,
                    "count": 1
                }
            
            # 处理组权限（角色权限）
            for group_perm in group_permissions:
                role_key = group_perm.get("roleKey", "unknown")
                role_name = group_perm.get("roleName", role_key)
                permissions = group_perm.get("permissions", [])
                roles[role_name] = {
                    "type": "role",
                    "role_key": role_key,
                    "permissions": permissions,
                    "count": 1  # 这表示这个角色在模板中被定义
                }
            
            architecture_info["roles_and_permissions"] = roles
            
            # 从模板basicInfo中提取其他有用信息
            architecture_info["template_metadata"] = {
                "template_type": template.get("templateType", "unknown"),
                "is_pdf": template.get("isPdf", False),
                "has_pdf_url": bool(template.get("pdfUrl")),
                "created_by": template.get("createdBy", "unknown"),
                "updated_at": template.get("updatedAt", ""),
                "forms_url": template.get("forms", {}).get("url", "")
            }
            
            # 查找状态信息（在详细数据中）
            if detail_resp.status_code == 200:
                detail_data = detail_resp.json()
                if "workflow" in detail_data:
                    workflow = detail_data["workflow"]
                    if "states" in workflow:
                        architecture_info["statuses"] = workflow["states"]
                    if "transitions" in workflow:
                        if not architecture_info["workflow_rules"]:
                            architecture_info["workflow_rules"] = {}
                        architecture_info["workflow_rules"]["transitions"] = workflow["transitions"]
                elif "statuses" in detail_data:
                    architecture_info["statuses"] = detail_data["statuses"]
            
            template_analysis.append(analysis)
            workflow_architecture.append(architecture_info)
        
        # 移除HTML内容，直接使用结构化数据
        
        # 总结可获取的表单模板信息
        architecture_summary = {
            "total_templates": len(templates_list),
            "templates_with_roles": len([a for a in workflow_architecture if a.get("roles_and_permissions")]),
            "templates_with_form_definition": len([a for a in workflow_architecture if a.get("template_structure", {}).get("has_form_definition")]),
            "templates_with_workflow": len([a for a in workflow_architecture if a.get("template_structure", {}).get("has_workflow")]),
            "templates_with_participants": len([a for a in workflow_architecture if a.get("participants")]),
            "templates_with_workflow_rules": len([a for a in workflow_architecture if a.get("workflow_rules")]),
            "templates_with_form_fields": len([a for a in workflow_architecture if a.get("form_fields")]),
            "templates_with_approval_settings": len([a for a in workflow_architecture if a.get("approval_settings")]),
            "total_roles_found": sum([len(a.get("roles_and_permissions", {})) for a in workflow_architecture]),
            "total_form_fields": sum([len(a.get("form_fields", [])) for a in workflow_architecture]),
            "avg_keys_per_template": sum([len(a.get("all_keys", [])) for a in workflow_architecture]) / len(workflow_architecture) if workflow_architecture else 0,
            "template_types": list(set([a.get("template_metadata", {}).get("template_type", "unknown") for a in workflow_architecture])),
            "pdf_templates": len([a for a in workflow_architecture if a.get("template_metadata", {}).get("is_pdf")])
        }
        
        
        return jsonify({
            "status": "success",
            "data": templates_list,  # 直接返回模板列表，符合Autodesk API格式
            "pagination": pagination_info,
            "query_parameters": {
                "offset": offset,
                "limit": limit,
                "sort_order": sort_order,
                "updated_after": updated_after,
                "updated_before": updated_before,
                "total_requested": len(templates_list)
            },
            "templates": templates_data,  # 保留原始完整数据
            "template_analysis": template_analysis,
            "workflow_architecture": workflow_architecture,
            "architecture_summary": architecture_summary,
            "summary": {
                "total_templates": len(templates_list),
                "analysis_timestamp": datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        return jsonify({
            "error": f"获取模板数据时发生错误: {str(e)}",
            "status": "error"
        }), 500


@forms_bp.route('/api/forms/templates/export-json')
def export_templates_json():
    """导出表单模板架构数据为 JSON 文件"""
    access_token = utils.get_access_token()
    if not access_token:
        return {"error": "No access token found"}, 401
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        # 获取项目ID - 必须通过参数提供
        from flask import request
        project_id = request.args.get('projectId')
        
        if not project_id:
            return jsonify({
                "error": "缺少必需的 projectId 参数",
                "message": "请在请求中提供 projectId 参数",
                "status": "error"
            }), 400
        
        print(f"🚀 Export Templates API: 使用项目ID: {project_id}")
        
        # 获取表单模板列表 (使用默认参数获取所有模板)
        templates_url = f"{config.AUTODESK_API_BASE}/construction/forms/v1/projects/{project_id}/form-templates"
        params = {'limit': 50, 'sortOrder': 'desc'}  # 获取最新的50个模板
        templates_resp = requests.get(templates_url, headers=headers, params=params)
        
        if templates_resp.status_code != 200:
            return {"error": f"Failed to fetch templates: {templates_resp.status_code}"}, 400
        
        templates_data = templates_resp.json()
        templates_list = templates_data.get("data", [])
        
        # 获取每个模板的详细信息
        detailed_templates = []
        for template in templates_list:
            template_id = template.get("id")
            template_detail_url = f"{config.AUTODESK_API_BASE}/construction/forms/v1/projects/{project_id}/form-templates/{template_id}"
            detail_resp = requests.get(template_detail_url, headers=headers)
            
            template_info = {
                "basic_info": template,
                "detail_available": detail_resp.status_code == 200,
                "detail_data": detail_resp.json() if detail_resp.status_code == 200 else None
            }
            detailed_templates.append(template_info)
        
        # 生成导出数据
        export_data = {
            "export_info": {
                "timestamp": datetime.now().isoformat(),
                "project_id": project_id,
                "total_templates": len(templates_list),
                "export_type": "Forms Templates API - Approval Architecture"
            },
            "architecture_analysis": {
                "blueprint_components": {
                    "roles_and_permissions": "Roles and permissions definition",
                    "statuses": "Status workflow definition",
                    "workflow_rules": "Workflow rules configuration",
                    "participants": "Participant information"
                },
                "data_availability": "Check availability of form template information in each template"
            },
            "templates_data": detailed_templates,
            "raw_response": templates_data
        }
        
        # 生成 JSON 响应
        json_str = json.dumps(export_data, indent=2, ensure_ascii=False)
        response = Response(
            json_str,
            status=200,
            mimetype='application/json'
        )
        response.headers['Content-Disposition'] = f'attachment; filename=forms_templates_architecture_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        return response
        
    except Exception as e:
        return {"error": str(e)}, 500


@forms_bp.route('/api/forms/templates/recent')
def get_recent_form_templates():
    """获取最近更新的表单模板（演示查询参数使用）"""
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
        from datetime import datetime, timedelta
        from flask import request
        
        # 获取项目ID - 必须通过参数提供
        project_id = request.args.get('projectId')
        
        if not project_id:
            return jsonify({
                "error": "缺少必需的 projectId 参数",
                "message": "请在请求中提供 projectId 参数",
                "status": "error"
            }), 400
        
        print(f"🚀 Recent Templates API: 使用项目ID: {project_id}")
        
        # 获取最近30天更新的模板
        thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
        
        params = {
            'limit': 10,  # 只获取前10个
            'sortOrder': 'desc',  # 按更新时间降序
            'updatedAfter': thirty_days_ago  # 最近30天
        }
        
        templates_url = f"{config.AUTODESK_API_BASE}/construction/forms/v1/projects/{project_id}/form-templates"
        response = requests.get(templates_url, headers=headers, params=params)
        
        if response.status_code != 200:
            raise Exception(f"获取模板失败: {response.status_code} - {response.text}")
        
        data = response.json()
        templates = data.get("data", [])
        pagination = data.get("pagination", {})
        
        return jsonify({
            "status": "success",
            "message": "Successfully retrieved recently updated form templates",
            "query_info": {
                "description": "获取最近30天更新的前10个表单模板",
                "parameters_used": params,
                "api_endpoint": templates_url
            },
            "pagination": pagination,
            "results": {
                "total_found": len(templates),
                "templates": templates
            },
            "usage_examples": {
                "get_first_20": "/api/forms/templates?limit=20&offset=0",
                "get_next_20": "/api/forms/templates?limit=20&offset=20", 
                "get_by_date": f"/api/forms/templates?updatedAfter={thirty_days_ago}",
                "get_oldest_first": "/api/forms/templates?sortOrder=asc"
            }
        })
        
    except Exception as e:
        return jsonify({
            "error": f"获取最近模板时发生错误: {str(e)}",
            "status": "error"
        }), 500