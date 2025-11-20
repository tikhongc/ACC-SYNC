# -*- coding: utf-8 -*-
"""
Data Management API 模块
处理 Autodesk Platform Services Data Management API 的基础功能
包括项目、文件夹、文件的基本操作和权限管理
"""

import requests
import json
import time
from datetime import datetime
from flask import Blueprint, jsonify, request
import config
import utils

data_management_bp = Blueprint('data_management', __name__)


def get_hub_projects(hub_id, headers):
    """获取指定Hub下的所有项目"""
    try:
        projects_url = f"{config.AUTODESK_API_BASE}/project/v1/hubs/{hub_id}/projects"
        response = requests.get(projects_url, headers=headers, timeout=(10, 30))
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ 获取Hub项目失败: {response.status_code} - {response.text}")
            return {"data": []}
            
    except Exception as e:
        print(f"❌ 获取Hub项目时出错: {str(e)}")
        return {"data": []}


def get_project_details(project_id, headers):
    """获取项目详细信息"""
    try:
        # 尝试通过不同的API获取项目详细信息
        
        # 1. 尝试通过 Construction Admin API
        admin_url = f"{config.AUTODESK_API_BASE}/construction/admin/v1/projects/{project_id}"
        admin_resp = requests.get(admin_url, headers=headers, timeout=(5, 10))
        
        if admin_resp.status_code == 200:
            admin_data = admin_resp.json()
            return {
                "source": "admin_api",
                "data": admin_data,
                "permissions": {
                    "admin_access": True,
                    "can_manage_users": True,
                    "can_manage_settings": True
                }
            }
        
        # 2. 如果Admin API失败，尝试基础项目信息
        print(f"⚠️ Admin API 访问失败 ({admin_resp.status_code})，尝试基础API")
        
        # 通过Hub API获取基础项目信息
        hubs_resp = requests.get(f"{config.AUTODESK_API_BASE}/project/v1/hubs", headers=headers)
        if hubs_resp.status_code == 200:
            hubs_data = hubs_resp.json()
            for hub in hubs_data.get('data', []):
                hub_id = hub.get('id')
                projects_data = get_hub_projects(hub_id, headers)
                
                for project in projects_data.get('data', []):
                    if project.get('id') == project_id:
                        return {
                            "source": "project_api",
                            "data": project,
                            "permissions": {
                                "admin_access": False,
                                "can_read": True,
                                "can_write": False  # 需要进一步检查
                            }
                        }
        
        return None
        
    except Exception as e:
        print(f"❌ 获取项目详细信息时出错: {str(e)}")
        return None


def check_folder_permissions(project_id, folder_id, headers):
    """检查文件夹权限"""
    try:
        # 尝试获取文件夹内容来判断读权限
        contents_url = f"{config.AUTODESK_API_BASE}/project/v1/projects/{project_id}/folders/{folder_id}/contents"
        contents_resp = requests.get(contents_url, headers=headers, timeout=(5, 10))
        
        permissions = {
            "can_read": contents_resp.status_code == 200,
            "can_write": False,
            "can_delete": False,
            "can_create": False
        }
        
        if contents_resp.status_code == 200:
            # 如果能读取，尝试检查写权限（通过尝试创建一个测试请求，但不实际执行）
            # 注意：这里只是检查API端点的可访问性，不实际创建内容
            
            # 检查是否有创建权限的迹象（通过响应头或其他方式）
            response_headers = contents_resp.headers
            if 'Allow' in response_headers:
                allowed_methods = response_headers['Allow'].upper()
                permissions["can_create"] = 'POST' in allowed_methods
                permissions["can_write"] = 'PUT' in allowed_methods or 'PATCH' in allowed_methods
                permissions["can_delete"] = 'DELETE' in allowed_methods
        
        return permissions
        
    except Exception as e:
        print(f"⚠️ 检查文件夹权限时出错: {str(e)}")
        return {
            "can_read": False,
            "can_write": False,
            "can_delete": False,
            "can_create": False,
            "error": str(e)
        }


def get_folder_metadata(project_id, folder_id, headers):
    """获取文件夹的详细元数据"""
    try:
        # 获取文件夹basicInfo
        folder_url = f"{config.AUTODESK_API_BASE}/project/v1/projects/{project_id}/folders/{folder_id}"
        folder_resp = requests.get(folder_url, headers=headers, timeout=(5, 10))
        
        if folder_resp.status_code != 200:
            print(f"⚠️ 无法获取文件夹信息: {folder_resp.status_code}")
            return None
        
        folder_data = folder_resp.json()
        
        # 获取文件夹内容统计
        contents_url = f"{config.AUTODESK_API_BASE}/project/v1/projects/{project_id}/folders/{folder_id}/contents"
        contents_resp = requests.get(contents_url, headers=headers, timeout=(5, 10))
        
        contents_count = 0
        subfolders_count = 0
        files_count = 0
        
        if contents_resp.status_code == 200:
            contents_data = contents_resp.json()
            contents_list = contents_data.get('data', [])
            contents_count = len(contents_list)
            
            for item in contents_list:
                if item.get('type') == 'folders':
                    subfolders_count += 1
                else:
                    files_count += 1
        
        # 检查权限
        permissions = check_folder_permissions(project_id, folder_id, headers)
        
        metadata = {
            "folder_info": folder_data,
            "statistics": {
                "total_items": contents_count,
                "subfolders": subfolders_count,
                "files": files_count
            },
            "permissions": permissions,
            "last_checked": datetime.now().isoformat()
        }
        
        return metadata
        
    except Exception as e:
        print(f"❌ 获取文件夹元数据时出错: {str(e)}")
        return None


@data_management_bp.route('/api/data-management/hubs')
def get_all_hubs():
    """获取用户可访问的所有Hub"""
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
        print("🔍 获取所有Hub信息")
        
        hubs_resp = requests.get(f"{config.AUTODESK_API_BASE}/project/v1/hubs", headers=headers)
        
        if hubs_resp.status_code != 200:
            return jsonify({
                "error": f"获取Hub信息失败: {hubs_resp.status_code}",
                "status": "error"
            }), 400
        
        hubs_data = hubs_resp.json()
        enhanced_hubs = []
        
        # 为每个Hub获取项目信息
        for hub in hubs_data.get('data', []):
            hub_id = hub.get('id')
            hub_attributes = hub.get('attributes', {})
            
            print(f"📋 处理Hub: {hub_attributes.get('name', 'Unknown')}")
            
            # 获取Hub下的项目
            projects_data = get_hub_projects(hub_id, headers)
            projects_count = len(projects_data.get('data', []))
            
            enhanced_hub = {
                "id": hub_id,
                "name": hub_attributes.get('name', 'Unknown'),
                "region": hub_attributes.get('region'),
                "type": hub.get('type'),
                "projects_count": projects_count,
                "projects": projects_data.get('data', [])[:5],  # 只返回前5个项目作为预览
                "attributes": hub_attributes
            }
            
            enhanced_hubs.append(enhanced_hub)
        
        return jsonify({
            "status": "success",
            "data": {
                "hubs": enhanced_hubs,
                "total_hubs": len(enhanced_hubs)
            }
        })
        
    except Exception as e:
        print(f"❌ 获取Hub信息时出错: {str(e)}")
        return jsonify({
            "error": f"获取Hub信息失败: {str(e)}",
            "status": "error"
        }), 500


@data_management_bp.route('/api/data-management/hubs/<hub_id>/projects')
def get_hub_projects_api(hub_id):
    """获取指定Hub下的所有项目"""
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
        print(f"🔍 获取Hub项目: {hub_id}")
        
        projects_data = get_hub_projects(hub_id, headers)
        enhanced_projects = []
        
        # 为每个项目获取详细信息
        for project in projects_data.get('data', []):
            project_id = project.get('id')
            project_attributes = project.get('attributes', {})
            
            print(f"📋 处理项目: {project_attributes.get('name', 'Unknown')}")
            
            # 获取项目详细信息
            project_details = get_project_details(project_id, headers)
            
            enhanced_project = {
                "id": project_id,
                "name": project_attributes.get('name', 'Unknown'),
                "type": project.get('type'),
                "attributes": project_attributes,
                "details": project_details,
                "last_checked": datetime.now().isoformat()
            }
            
            enhanced_projects.append(enhanced_project)
        
        return jsonify({
            "status": "success",
            "hub_id": hub_id,
            "data": {
                "projects": enhanced_projects,
                "total_projects": len(enhanced_projects)
            }
        })
        
    except Exception as e:
        print(f"❌ 获取Hub项目时出错: {str(e)}")
        return jsonify({
            "error": f"获取Hub项目失败: {str(e)}",
            "status": "error"
        }), 500


@data_management_bp.route('/api/data-management/projects/<project_id>/details')
def get_project_details_api(project_id):
    """获取项目的详细信息和权限"""
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
        print(f"🔍 获取项目详细信息: {project_id}")
        
        # 获取项目详细信息
        project_details = get_project_details(project_id, headers)
        
        if not project_details:
            return jsonify({
                "error": "Unable to get project details",
                "status": "error"
            }), 404
        
        # 尝试获取容器信息（无论来源是什么）
        try:
            # 获取Hub列表来查找项目的关系数据
            hubs_resp = requests.get(f"{config.AUTODESK_API_BASE}/project/v1/hubs", headers=headers)
            if hubs_resp.status_code == 200:
                hubs_data = hubs_resp.json()
                project_data = None
                
                # 在所有Hub中查找项目
                for hub in hubs_data.get('data', []):
                    hub_id = hub.get('id')
                    projects_data = get_hub_projects(hub_id, headers)
                    
                    for project in projects_data.get('data', []):
                        if project.get('id') == project_id:
                            project_data = project
                            break
                    
                    if project_data:
                        break
                
                # 如果找到项目数据，提取容器信息
                if project_data:
                    relationships = project_data.get('relationships', {})
                    
                    # 提取容器ID信息
                    containers = {}
                    container_types = ['issues', 'markups', 'rfis', 'checklists', 'cost', 'locations']
                    for container_type in container_types:
                        if container_type in relationships:
                            container_data = relationships[container_type].get('data', {})
                            if container_data.get('id'):
                                containers[container_type] = {
                                    'id': container_data.get('id'),
                                    'type': container_data.get('type'),
                                    'url': relationships[container_type].get('meta', {}).get('link', {}).get('href')
                                }
                    
                    # 添加容器信息到项目详细信息中
                    if containers:
                        project_details['containers'] = containers
                        print(f"✅ 成功提取容器信息: {list(containers.keys())}")
                    else:
                        print("⚠️ 未找到容器信息")
                else:
                    print("⚠️ 未在Hub项目列表中找到项目")
            else:
                print(f"⚠️ 获取Hub列表失败: {hubs_resp.status_code}")
        except Exception as container_error:
            print(f"⚠️ 获取容器信息时出错: {str(container_error)}")
            # 不影响主要功能，继续执行
        
        # 获取项目的顶级文件夹
        try:
            hubs_resp = requests.get(f"{config.AUTODESK_API_BASE}/project/v1/hubs", headers=headers)
            if hubs_resp.status_code == 200:
                hubs_data = hubs_resp.json()
                hub_id = hubs_data.get('data', [{}])[0].get('id') if hubs_data.get('data') else None
                
                if hub_id:
                    top_folders_url = f"{config.AUTODESK_API_BASE}/project/v1/hubs/{hub_id}/projects/{project_id}/topFolders"
                    top_folders_resp = requests.get(top_folders_url, headers=headers)
                    
                    if top_folders_resp.status_code == 200:
                        top_folders_data = top_folders_resp.json()
                        project_details["top_folders"] = top_folders_data.get('data', [])
                        project_details["top_folders_count"] = len(top_folders_data.get('data', []))
        except Exception as e:
            print(f"⚠️ 获取顶级文件夹时出错: {str(e)}")
            project_details["top_folders"] = []
            project_details["top_folders_count"] = 0
        
        return jsonify({
            "status": "success",
            "project_id": project_id,
            "data": project_details
        })
        
    except Exception as e:
        print(f"❌ 获取项目详细信息时出错: {str(e)}")
        return jsonify({
            "error": f"获取项目详细信息失败: {str(e)}",
            "status": "error"
        }), 500


@data_management_bp.route('/api/data-management/projects/<project_id>/containers')
def get_project_containers_api(project_id):
    """获取项目的容器ID信息"""
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
        print(f"🔍 获取项目容器信息: {project_id}")
        
        # 获取Hub列表
        hubs_resp = requests.get(f"{config.AUTODESK_API_BASE}/project/v1/hubs", headers=headers)
        if hubs_resp.status_code != 200:
            return jsonify({
                "error": "无法获取Hub信息",
                "status": "error"
            }), 500
        
        hubs_data = hubs_resp.json()
        project_data = None
        
        # 在所有Hub中查找项目
        for hub in hubs_data.get('data', []):
            hub_id = hub.get('id')
            projects_data = get_hub_projects(hub_id, headers)
            
            for project in projects_data.get('data', []):
                if project.get('id') == project_id:
                    project_data = project
                    break
            
            if project_data:
                break
        
        if not project_data:
            return jsonify({
                "error": "Specified project not found",
                "status": "error"
            }), 404
        
        # 提取容器ID信息
        relationships = project_data.get('relationships', {})
        containers = {}
        
        # 提取各种容器ID
        container_types = ['issues', 'markups', 'rfis', 'checklists', 'cost', 'locations']
        for container_type in container_types:
            if container_type in relationships:
                container_data = relationships[container_type].get('data', {})
                if container_data.get('id'):
                    containers[container_type] = {
                        'id': container_data.get('id'),
                        'type': container_data.get('type'),
                        'url': relationships[container_type].get('meta', {}).get('link', {}).get('href')
                    }
        
        return jsonify({
            "status": "success",
            "project_id": project_id,
            "data": {
                "containers": containers,
                "project_name": project_data.get('attributes', {}).get('name', 'Unknown'),
                "project_type": project_data.get('type')
            }
        })
        
    except Exception as e:
        print(f"❌ 获取项目容器信息时出错: {str(e)}")
        return jsonify({
            "error": f"获取项目容器信息失败: {str(e)}",
            "status": "error"
        }), 500


@data_management_bp.route('/api/data-management/projects/<project_id>/folders/<folder_id>/metadata')
def get_folder_metadata_api(project_id, folder_id):
    """获取文件夹的详细元数据和权限信息"""
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
        print(f"🔍 获取文件夹元数据: {folder_id}")
        
        metadata = get_folder_metadata(project_id, folder_id, headers)
        
        if not metadata:
            return jsonify({
                "error": "Unable to get folder metadata",
                "status": "error"
            }), 404
        
        return jsonify({
            "status": "success",
            "project_id": project_id,
            "folder_id": folder_id,
            "data": metadata
        })
        
    except Exception as e:
        print(f"❌ 获取文件夹元数据时出错: {str(e)}")
        return jsonify({
            "error": f"获取文件夹元数据失败: {str(e)}",
            "status": "error"
        }), 500


@data_management_bp.route('/api/data-management/projects/<project_id>/folders/<folder_id>/permissions')
def check_folder_permissions_api(project_id, folder_id):
    """检查文件夹权限"""
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
        print(f"🔍 检查文件夹权限: {folder_id}")
        
        permissions = check_folder_permissions(project_id, folder_id, headers)
        
        return jsonify({
            "status": "success",
            "project_id": project_id,
            "folder_id": folder_id,
            "permissions": permissions,
            "checked_at": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"❌ 检查文件夹权限时出错: {str(e)}")
        return jsonify({
            "error": f"检查文件夹权限失败: {str(e)}",
            "status": "error"
        }), 500


@data_management_bp.route('/api/data-management/projects/<project_id>/items/<item_id>/versions')
def get_item_versions_api(project_id, item_id):
    """获取文件的所有版本信息"""
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
        print(f"🔍 获取文件版本信息: {item_id}")
        
        versions_url = f"{config.AUTODESK_API_BASE}/project/v1/projects/{project_id}/items/{item_id}/versions"
        response = requests.get(versions_url, headers=headers, timeout=(10, 30))
        
        if response.status_code != 200:
            return jsonify({
                "error": f"获取版本信息失败: {response.status_code}",
                "status": "error"
            }), 400
        
        versions_data = response.json()
        versions_list = versions_data.get('data', [])
        
        # 增强版本信息
        enhanced_versions = []
        for version in versions_list:
            version_attributes = version.get('attributes', {})
            
            enhanced_version = {
                "id": version.get('id'),
                "type": version.get('type'),
                "version_number": version_attributes.get('versionNumber'),
                "display_name": version_attributes.get('displayName'),
                "create_time": version_attributes.get('createTime'),
                "create_user_id": version_attributes.get('createUserId'),
                "create_user_name": version_attributes.get('createUserName'),
                "last_modified_time": version_attributes.get('lastModifiedTime'),
                "last_modified_user_id": version_attributes.get('lastModifiedUserId'),
                "last_modified_user_name": version_attributes.get('lastModifiedUserName'),
                "file_size": version_attributes.get('storageSize'),
                "mime_type": version_attributes.get('mimeType'),
                "extension": version_attributes.get('extension', {}),
                "attributes": version_attributes
            }
            
            enhanced_versions.append(enhanced_version)
        
        return jsonify({
            "status": "success",
            "project_id": project_id,
            "item_id": item_id,
            "data": {
                "versions": enhanced_versions,
                "total_versions": len(enhanced_versions),
                "latest_version": enhanced_versions[0] if enhanced_versions else None
            }
        })
        
    except Exception as e:
        print(f"❌ 获取文件版本信息时出错: {str(e)}")
        return jsonify({
            "error": f"获取文件版本信息失败: {str(e)}",
            "status": "error"
        }), 500


@data_management_bp.route('/api/data-management/search')
def search_projects_and_files():
    """搜索项目和文件"""
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
        # 获取搜索参数
        query = request.args.get('q', '').strip()
        search_type = request.args.get('type', 'all')  # all, projects, files
        limit = request.args.get('limit', 20, type=int)
        
        if not query:
            return jsonify({
                "error": "Please provide search keywords",
                "status": "error"
            }), 400
        
        print(f"🔍 搜索: '{query}' (类型: {search_type})")
        
        results = {
            "query": query,
            "search_type": search_type,
            "results": {
                "projects": [],
                "files": [],
                "folders": []
            },
            "statistics": {
                "total_projects": 0,
                "total_files": 0,
                "total_folders": 0
            }
        }
        
        # 获取所有Hub和项目进行搜索
        if search_type in ['all', 'projects']:
            hubs_resp = requests.get(f"{config.AUTODESK_API_BASE}/project/v1/hubs", headers=headers)
            if hubs_resp.status_code == 200:
                hubs_data = hubs_resp.json()
                
                for hub in hubs_data.get('data', []):
                    hub_id = hub.get('id')
                    projects_data = get_hub_projects(hub_id, headers)
                    
                    for project in projects_data.get('data', []):
                        project_name = project.get('attributes', {}).get('name', '')
                        if query.lower() in project_name.lower():
                            results["results"]["projects"].append({
                                "id": project.get('id'),
                                "name": project_name,
                                "hub_id": hub_id,
                                "hub_name": hub.get('attributes', {}).get('name', ''),
                                "type": project.get('type'),
                                "attributes": project.get('attributes', {})
                            })
                            
                            if len(results["results"]["projects"]) >= limit:
                                break
        
        # 更新统计信息
        results["statistics"]["total_projects"] = len(results["results"]["projects"])
        results["statistics"]["total_files"] = len(results["results"]["files"])
        results["statistics"]["total_folders"] = len(results["results"]["folders"])
        
        return jsonify({
            "status": "success",
            "data": results
        })
        
    except Exception as e:
        print(f"❌ 搜索时出错: {str(e)}")
        return jsonify({
            "error": f"搜索失败: {str(e)}",
            "status": "error"
        }), 500
