# -*- coding: utf-8 -*-
"""
Data Connector API 模块
处理 Autodesk Construction Cloud Data Connector 相关功能
"""

import requests
import json
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
import config
import utils

data_connector_bp = Blueprint('data_connector', __name__)


def is_project_active(project_status):
    """
    判断项目是否为活跃状态
    根据 Data Connector 文档，支持多种状态表示方式
    """
    if project_status is None:
        # 根据文档，如果状态为空，默认认为是活跃的
        return True
    
    # 转换为字符串并统一为小写
    status_str = str(project_status).lower().strip()
    
    # 根据 Data Connector 文档和常见状态值判断
    active_statuses = [
        "active",      # 标准活跃状态
        "活跃",        # 中文活跃
        "启用",        # 中文启用
        "enabled",     # 英文启用
        "running",     # 运行中
        "open",        # 开放
        "ongoing",     # 进行中
        ""             # 空字符串默认为活跃
    ]
    
    return status_str in active_statuses


def clean_project_ids(project_ids):
    """
    清理项目ID：移除"b."前缀
    Data Connector API需要纯UUID格式，不能带"b."前缀
    """
    cleaned_projects = []
    for project_id in project_ids:
        if project_id.startswith('b.'):
            cleaned_projects.append(project_id[2:])  # 移除"b."前缀
        else:
            cleaned_projects.append(project_id)
    return cleaned_projects


@data_connector_bp.route('/api/data-connector/get-projects')
def get_available_projects():
    """获取用户可访问的项目列表（用于创建数据请求）"""
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
        # 复用auth_api中的项目获取逻辑
        # 1. 获取Hub信息
        hubs_resp = requests.get(f"{config.AUTODESK_API_BASE}/project/v1/hubs", headers=headers)
        if hubs_resp.status_code != 200:
            return jsonify({
                "error": f"无法获取Hub信息: {hubs_resp.status_code}",
                "status": "error"
            }), 400
        
        hubs_data = hubs_resp.json()
        hub_id, real_account_id, hub_name = utils.get_real_account_id(hubs_data)
        
        # 2. 获取Hub下的所有项目（复用auth_api逻辑）
        projects_resp = requests.get(
            f"{config.AUTODESK_API_BASE}/project/v1/hubs/{hub_id}/projects",
            headers=headers,
            timeout=(10, 15)
        )
        
        if projects_resp.status_code != 200:
            return jsonify({
                "error": f"无法获取项目列表: {projects_resp.status_code}",
                "status": "error"
            }), 400
        
        projects_data = projects_resp.json()
        projects_list = []
        
        # 3. 处理项目数据，只返回必要信息
        for project in projects_data.get('data', []):
            project_info = {
                "id": project.get('id'),
                "name": project.get('attributes', {}).get('name'),
                "status": project.get('attributes', {}).get('status'),
                "type": project.get('type'),
                "isActive": is_project_active(project.get('attributes', {}).get('status'))
            }
            projects_list.append(project_info)
        
        # 4. 筛选活跃项目
        active_projects = [p for p in projects_list if p['isActive']]
        
        return jsonify({
            "status": "success",
            "hub": {
                "id": hub_id,
                "name": hub_name,
                "accountId": real_account_id
            },
            "projects": {
                "total": len(projects_list),
                "active": len(active_projects),
                "list": projects_list
            }
        })
        
    except Exception as e:
        return jsonify({
            "error": f"获取项目列表失败: {str(e)}",
            "status": "error"
        }), 500


@data_connector_bp.route('/api/data-connector/test-request', methods=['POST'])
def test_data_request_format():
    """测试数据请求格式是否正确（不实际创建请求）"""
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
        # 获取请求参数
        request_data = request.get_json()
        if not request_data:
            return jsonify({
                "error": "请求体不能为空",
                "status": "error"
            }), 400
        
        selected_projects = request_data.get('selectedProjects', [])
        request_config = request_data.get('requestConfig', {})
        
        # 清理项目ID：移除"b."前缀（Data Connector API需要纯UUID）
        cleaned_projects = clean_project_ids(selected_projects)
        print(f"测试 - 原始项目ID: {selected_projects}")
        print(f"测试 - 清理后项目ID: {cleaned_projects}")
        
        # 获取Account ID
        hubs_resp = requests.get(f"{config.AUTODESK_API_BASE}/project/v1/hubs", headers=headers)
        if hubs_resp.status_code != 200:
            return jsonify({
                "error": f"无法获取Hub信息: {hubs_resp.status_code}",
                "status": "error"
            }), 400
        
        hubs_data = hubs_resp.json()
        hub_id, real_account_id, hub_name = utils.get_real_account_id(hubs_data)
        
        # 构建数据请求配置（与实际创建请求相同的逻辑）
        is_one_time = request_config.get('isOneTime', False)
        
        if is_one_time:
            effective_from = datetime.now().replace(microsecond=0)
            effective_to = effective_from + timedelta(hours=1)
            schedule_interval = "DAY"
            reoccuring_interval = 1
        else:
            effective_from = datetime.now().replace(microsecond=0)
            if request_config.get('scheduleInterval') == 'DAY':
                effective_to = effective_from + timedelta(days=request_config.get('duration', 30))
            elif request_config.get('scheduleInterval') == 'WEEK':
                effective_to = effective_from + timedelta(weeks=request_config.get('duration', 12))
            else:  # MONTH
                effective_to = effective_from + timedelta(days=request_config.get('duration', 365))
            
            schedule_interval = request_config.get('scheduleInterval', 'WEEK')
            reoccuring_interval = request_config.get('reoccuringInterval', 1)
        
        test_config = {
            "description": request_config.get('description', 'Data Extract Request'),
            "scheduleInterval": schedule_interval,
            "reoccuringInterval": reoccuring_interval,
            "effectiveFrom": effective_from.isoformat() + "Z",
            "effectiveTo": effective_to.isoformat() + "Z",
            "serviceGroups": request_config.get('serviceGroups', ["admin", "issues", "locations", "submittals", "cost", "rfis"]),
            "projectIdList": cleaned_projects
        }
        
        # 验证必填字段
        validation_errors = []
        
        if not test_config["description"]:
            validation_errors.append("description 不能为空")
        
        if not test_config["scheduleInterval"]:
            validation_errors.append("scheduleInterval 不能为空")
        
        if not test_config["serviceGroups"]:
            validation_errors.append("serviceGroups 不能为空")
        
        if not cleaned_projects:
            validation_errors.append("projectIdList 不能为空")
        
        # 验证时间格式
        try:
            datetime.fromisoformat(test_config["effectiveFrom"].replace('Z', '+00:00'))
            datetime.fromisoformat(test_config["effectiveTo"].replace('Z', '+00:00'))
        except ValueError as e:
            validation_errors.append(f"时间格式错误: {str(e)}")
        
        return jsonify({
            "status": "success",
            "message": "请求格式验证完成",
            "validation_errors": validation_errors,
            "is_valid": len(validation_errors) == 0,
            "test_config": test_config,
            "api_url": f"{config.AUTODESK_API_BASE}/data-connector/v1/accounts/{real_account_id}/requests",
            "account_info": {
                "hub_id": hub_id,
                "account_id": real_account_id,
                "hub_name": hub_name
            },
            "project_id_mapping": {
                "original": selected_projects,
                "cleaned": cleaned_projects
            }
        })
        
    except Exception as e:
        return jsonify({
            "error": f"测试请求格式失败: {str(e)}",
            "status": "error"
        }), 500


@data_connector_bp.route('/api/data-connector/create-batch', methods=['POST'])
def create_batch_data_requests():
    """为选定的项目创建批量数据请求"""
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
        # 获取请求参数
        request_data = request.get_json()
        if not request_data:
            return jsonify({
                "error": "请求体不能为空",
                "status": "error"
            }), 400
        
        selected_projects = request_data.get('selectedProjects', [])
        request_config = request_data.get('requestConfig', {})
        
        # 清理项目ID：移除"b."前缀（Data Connector API需要纯UUID）
        cleaned_projects = clean_project_ids(selected_projects)
        print(f"🔧 项目ID清理:")
        print(f"   原始项目ID: {selected_projects}")
        print(f"   清理后项目ID: {cleaned_projects}")
        
        if not cleaned_projects:
            return jsonify({
                "error": "请至少选择一个项目",
                "status": "error"
            }), 400
        
        # 获取Account ID
        hubs_resp = requests.get(f"{config.AUTODESK_API_BASE}/project/v1/hubs", headers=headers)
        if hubs_resp.status_code != 200:
            return jsonify({
                "error": f"无法获取Hub信息: {hubs_resp.status_code}",
                "status": "error"
            }), 400
        
        hubs_data = hubs_resp.json()
        hub_id, real_account_id, hub_name = utils.get_real_account_id(hubs_data)
        
        # 构建数据请求配置
        # 处理一次性请求 vs 定期请求
        is_one_time = request_config.get('isOneTime', False)
        
        if is_one_time:
            # 一次性请求：优化执行策略
            effective_from = datetime.now().replace(microsecond=0)
            
            # 检查当前时间，如果接近调度窗口则立即执行
            current_hour = effective_from.hour
            
            # 如果在UTC 15:30-16:30之间，设置为立即执行（对应北京时间23:30-00:30）
            if 15 <= current_hour <= 16:
                effective_from = effective_from - timedelta(minutes=5)  # 设置为5分钟前，确保立即触发
            
            effective_to = effective_from + timedelta(hours=2)  # 2小时窗口，确保执行
            schedule_interval = "DAY"  # 使用DAY，但通过时间窗口控制
            reoccuring_interval = 1
        else:
            # 定期请求：使用用户配置
            effective_from = datetime.now().replace(microsecond=0)
            if request_config.get('scheduleInterval') == 'DAY':
                effective_to = effective_from + timedelta(days=request_config.get('duration', 30))
            elif request_config.get('scheduleInterval') == 'WEEK':
                effective_to = effective_from + timedelta(weeks=request_config.get('duration', 12))
            else:  # MONTH
                effective_to = effective_from + timedelta(days=request_config.get('duration', 365))
            
            schedule_interval = request_config.get('scheduleInterval', 'WEEK')
            reoccuring_interval = request_config.get('reoccuringInterval', 1)
        
        base_config = {
            "description": request_config.get('description', 'Data Extract Request'),
            "scheduleInterval": schedule_interval,
            "reoccuringInterval": reoccuring_interval,
            "effectiveFrom": effective_from.isoformat() + "Z",
            "effectiveTo": effective_to.isoformat() + "Z",
            "serviceGroups": request_config.get('serviceGroups', ["admin", "issues", "locations", "submittals", "cost", "rfis"]),
            "projectIdList": cleaned_projects
        }
        
        print(f"✅ 创建数据请求配置:")
        print(f"{json.dumps(base_config, indent=2)}")
        
        # 创建数据请求
        api_url = f"{config.AUTODESK_API_BASE}/data-connector/v1/accounts/{real_account_id}/requests"
        
        response = requests.post(
            api_url,
                headers=headers, 
            json=base_config,
                timeout=(10, 30)
            )
            
        if response.status_code == 201:
            result_data = response.json()
            print(f"🎉 数据请求创建成功: {result_data.get('id')}")
            return jsonify({
                    "status": "success",
                "message": f"成功为 {len(cleaned_projects)} 个项目创建数据请求",
                "request_id": result_data.get("id"),
                "request_details": result_data,
                "projects_count": len(cleaned_projects),
                "selected_projects": cleaned_projects,
                "original_projects": selected_projects
                })
        else:
            error_details = response.text[:500]
            print(f"❌ Data Connector API 错误:")
            print(f"   状态码: {response.status_code}")
            print(f"   URL: {api_url}")
            print(f"   请求配置: {json.dumps(base_config, indent=2)}")
            print(f"   响应内容: {error_details}")
            
            return jsonify({
                "error": f"创建数据请求失败: HTTP {response.status_code}",
                "details": error_details,
                "status": "error",
                "api_url": api_url,
                "request_config": base_config,
                "debug_info": {
                    "status_code": response.status_code,
                    "response_headers": dict(response.headers),
                    "request_url": api_url,
                    "request_body": base_config,
                    "project_id_mapping": {
                        "original": selected_projects,
                        "cleaned": cleaned_projects
                    }
                }
            }), 400
        
    except Exception as e:
        return jsonify({
            "error": f"创建批量数据请求失败: {str(e)}",
            "status": "error"
        }), 500


@data_connector_bp.route('/api/data-connector/requests/<request_id>/jobs')
def get_request_jobs(request_id):
    """获取指定请求的作业列表"""
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
        # 获取Account ID
        projects_resp = requests.get(f"{config.AUTODESK_API_BASE}/project/v1/hubs", headers=headers)
        projects_data = projects_resp.json() if projects_resp.status_code == 200 else {}
        hub_id, real_account_id, hub_name = utils.get_real_account_id(projects_data)
        
        # 获取请求参数
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        sort = request.args.get('sort', 'desc')
        
        # 构建API URL
        api_url = f"{config.AUTODESK_API_BASE}/data-connector/v1/accounts/{real_account_id}/requests/{request_id}/jobs"
        params = {
            'limit': limit,
            'offset': offset,
            'sort': sort
        }
        
        response = requests.get(api_url, headers=headers, params=params, timeout=(5, 10))
        
        if response.status_code == 200:
            jobs_data = response.json()
            return jsonify({
            "status": "success",
                "request_id": request_id,
                "jobs": jobs_data,
                "account_id": real_account_id
            })
        else:
            return jsonify({
                "error": f"获取作业列表失败: HTTP {response.status_code}",
                "details": response.text[:200],
                "status": "error"
            }), 400
        
    except Exception as e:
        return jsonify({
            "error": f"获取作业列表失败: {str(e)}",
            "status": "error"
        }), 500


@data_connector_bp.route('/api/data-connector/jobs/<job_id>/data-listing')
def get_job_data_listing(job_id):
    """获取作业的数据文件列表"""
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
        # 获取Account ID
        projects_resp = requests.get(f"{config.AUTODESK_API_BASE}/project/v1/hubs", headers=headers)
        projects_data = projects_resp.json() if projects_resp.status_code == 200 else {}
        hub_id, real_account_id, hub_name = utils.get_real_account_id(projects_data)
        
        # 构建API URL
        api_url = f"{config.AUTODESK_API_BASE}/data-connector/v1/accounts/{real_account_id}/jobs/{job_id}/data-listing"
        
        response = requests.get(api_url, headers=headers, timeout=(5, 10))
        
        if response.status_code == 200:
            files_data = response.json()
            return jsonify({
                "status": "success",
                "job_id": job_id,
                "files": files_data,
                "account_id": real_account_id
            })
        else:
            return jsonify({
                "error": f"获取文件列表失败: HTTP {response.status_code}",
                "details": response.text[:200],
                "status": "error"
            }), 400
        
    except Exception as e:
        return jsonify({
            "error": f"获取文件列表失败: {str(e)}",
            "status": "error"
        }), 500


@data_connector_bp.route('/api/data-connector/jobs/<job_id>/data/<filename>')
def get_job_data_download(job_id, filename):
    """获取作业数据文件的下载链接"""
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
        # 获取Account ID
        projects_resp = requests.get(f"{config.AUTODESK_API_BASE}/project/v1/hubs", headers=headers)
        projects_data = projects_resp.json() if projects_resp.status_code == 200 else {}
        hub_id, real_account_id, hub_name = utils.get_real_account_id(projects_data)
        
        # 构建API URL
        api_url = f"{config.AUTODESK_API_BASE}/data-connector/v1/accounts/{real_account_id}/jobs/{job_id}/data/{filename}"
        
        response = requests.get(api_url, headers=headers, timeout=(5, 10))
        
        if response.status_code == 200:
            download_data = response.json()
            return jsonify({
                "status": "success",
                "job_id": job_id,
                "filename": filename,
                "download_info": download_data,
                "account_id": real_account_id
            })
        else:
            return jsonify({
                "error": f"获取下载链接失败: HTTP {response.status_code}",
                "details": response.text[:200],
                "status": "error"
            }), 400
        
    except Exception as e:
        return jsonify({
            "error": f"获取下载链接失败: {str(e)}",
            "status": "error"
        }), 500


@data_connector_bp.route('/api/data-connector/requests')
def list_data_requests():
    """获取数据请求列表"""
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
        # 获取Account ID
        projects_resp = requests.get(f"{config.AUTODESK_API_BASE}/project/v1/hubs", headers=headers)
        projects_data = projects_resp.json() if projects_resp.status_code == 200 else {}
        hub_id, real_account_id, hub_name = utils.get_real_account_id(projects_data)
        
        # 获取请求参数
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)
        sort = request.args.get('sort', 'desc')
        
        # 构建API URL
        api_url = f"{config.AUTODESK_API_BASE}/data-connector/v1/accounts/{real_account_id}/requests"
        params = {
            'limit': limit,
            'offset': offset,
            'sort': sort
        }
        
        response = requests.get(api_url, headers=headers, params=params, timeout=(5, 10))
        
        if response.status_code == 200:
            return response.json()
        else:
            return jsonify({
                "error": f"获取数据请求列表失败: HTTP {response.status_code}",
                "status": "error"
            }), 400
        
    except Exception as e:
        return jsonify({
            "error": f"获取数据请求列表失败: {str(e)}",
            "status": "error"
        }), 500


@data_connector_bp.route('/api/data-connector/requests/<request_id>', methods=['DELETE'])
def delete_data_request(request_id):
    """删除数据请求（通过设置 isActive 为 false 来停用）"""
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
        # 获取Account ID
        projects_resp = requests.get(f"{config.AUTODESK_API_BASE}/project/v1/hubs", headers=headers)
        projects_data = projects_resp.json() if projects_resp.status_code == 200 else {}
        hub_id, real_account_id, hub_name = utils.get_real_account_id(projects_data)
        
        # 构建API URL
        api_url = f"{config.AUTODESK_API_BASE}/data-connector/v1/accounts/{real_account_id}/requests/{request_id}"
        
        # 使用 PATCH 方法设置 isActive 为 false 来停用请求
        payload = {
            'isActive': False
        }
        
        response = requests.patch(api_url, headers=headers, json=payload, timeout=(5, 10))
        
        if response.status_code == 200:
            return jsonify({
                "message": "数据请求已成功删除（停用）",
                "request_id": request_id,
                "status": "success",
                "data": response.json()
            })
        else:
            return jsonify({
                "error": f"删除数据请求失败: HTTP {response.status_code}",
                "details": response.text,
                "status": "error"
            }), response.status_code
            
    except Exception as e:
        return jsonify({
            "error": f"删除数据请求时发生错误: {str(e)}",
            "status": "error"
        }), 500