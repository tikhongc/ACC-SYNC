# -*- coding: utf-8 -*-
"""
文件权限同步 API 模块
专门处理 ACC 项目文件夹权限的同步和管理
使用 Autodesk BIM 360 Docs API (Beta)
"""

import requests
import json
import os
import time
from datetime import datetime
from flask import Blueprint, jsonify, request, send_file
import config
import utils

permissions_sync_bp = Blueprint('permissions_sync', __name__)


class PermissionLevel:
    """权限级别定义"""
    
    # ACC 权限级别映射
    ACC_PERMISSION_LEVELS = {
        "VIEW_ONLY": {
            "level": 1,
            "name": "View",
            "actions": ["VIEW", "COLLABORATE"],
            "description": "Can only view files"
        },
        "VIEW_DOWNLOAD": {
            "level": 2,
            "name": "查看/下载",
            "actions": ["VIEW", "DOWNLOAD", "COLLABORATE"],
            "description": "Can view and download files"
        },
        "VIEW_DOWNLOAD_MARKUP": {
            "level": 3,
            "name": "查看/下载/标记",
            "actions": ["VIEW", "DOWNLOAD", "COLLABORATE", "PUBLISH_MARKUP"],
            "description": "可以查看、下载文件和发布标记"
        },
        "VIEW_DOWNLOAD_MARKUP_UPLOAD": {
            "level": 4,
            "name": "查看/下载/标记/上传",
            "actions": ["PUBLISH", "VIEW", "DOWNLOAD", "COLLABORATE", "PUBLISH_MARKUP"],
            "description": "可以查看、下载、发布标记和上传文件"
        },
        "FULL_EDIT": {
            "level": 5,
            "name": "Full Edit",
            "actions": ["PUBLISH", "VIEW", "DOWNLOAD", "COLLABORATE", "PUBLISH_MARKUP", "EDIT"],
            "description": "可以查看、下载、发布标记、上传和编辑文件"
        },
        "FULL_CONTROL": {
            "level": 6,
            "name": "Full Control",
            "actions": ["PUBLISH", "VIEW", "DOWNLOAD", "COLLABORATE", "PUBLISH_MARKUP", "EDIT", "CONTROL"],
            "description": "Has full control permissions for the folder"
        }
    }


def clean_project_id(project_id):
    """清理项目ID，移除'b.'前缀"""
    return project_id.replace("b.", "") if project_id.startswith("b.") else project_id


def get_folder_permissions_from_api(project_id, folder_id, headers):
    """
    从官方API获取文件夹权限信息
    """
    try:
        # 清理项目ID
        clean_proj_id = clean_project_id(project_id)
        
        # 构建API URL
        api_url = f"{config.AUTODESK_API_BASE}/bim360/docs/v1/projects/{clean_proj_id}/folders/{folder_id}/permissions"
        
        print(f"🔍 调用权限API: {api_url}")
        
        response = requests.get(api_url, headers=headers, timeout=(10, 30))
        
        if response.status_code == 200:
            permissions_data = response.json()
            
            return {
                "status": "success",
                "data": permissions_data,
                "api_url": api_url,
                "retrieved_at": datetime.now().isoformat()
            }
            
        elif response.status_code == 403:
            return {
                "status": "error",
                "error": "权限不足，需要VIEW权限才能查看文件夹权限",
                "error_code": "INSUFFICIENT_PERMISSIONS",
                "http_status": 403
            }
            
        elif response.status_code == 404:
            return {
                "status": "error",
                "error": "Project or folder does not exist",
                "error_code": "NOT_FOUND",
                "http_status": 404
            }
            
        elif response.status_code == 429:
            return {
                "status": "error",
                "error": "请求过于频繁，请稍后重试",
                "error_code": "RATE_LIMIT",
                "http_status": 429
            }
            
        else:
            return {
                "status": "error",
                "error": f"API调用失败: HTTP {response.status_code}",
                "details": response.text[:500],
                "error_code": "API_ERROR",
                "http_status": response.status_code
            }
            
    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "error": "API请求超时",
            "error_code": "TIMEOUT"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"调用权限API时出错: {str(e)}",
            "error_code": "EXCEPTION"
        }


def parse_permissions_data(permissions_data):
    """
    解析权限数据，转换为结构化格式
    """
    parsed_data = {
        "users": [],
        "roles": [],
        "companies": [],
        "summary": {
            "total_subjects": len(permissions_data),
            "users_count": 0,
            "roles_count": 0,
            "companies_count": 0
        }
    }
    
    for permission in permissions_data:
        subject_type = permission.get("subjectType", "").upper()
        
        # 合并直接权限和继承权限
        direct_actions = permission.get("actions", [])
        inherit_actions = permission.get("inheritActions", [])
        all_actions = list(set(direct_actions + inherit_actions))
        
        # 确定权限级别
        permission_level_info = determine_permission_level(all_actions)
        
        permission_record = {
            "subject_id": permission.get("subjectId"),
            "autodesk_id": permission.get("autodeskId"),
            "name": permission.get("name"),
            "email": permission.get("email"),
            "user_type": permission.get("userType"),
            "subject_type": subject_type,
            "subject_status": permission.get("subjectStatus"),
            "direct_actions": direct_actions,
            "inherit_actions": inherit_actions,
            "all_actions": all_actions,
            "permission_level": permission_level_info["level"],
            "permission_name": permission_level_info["name"],
            "permission_description": permission_level_info["description"],
            "detailed_permissions": {
                "canView": "VIEW" in all_actions,
                "canDownload": "DOWNLOAD" in all_actions,
                "canCollaborate": "COLLABORATE" in all_actions,
                "canPublishMarkup": "PUBLISH_MARKUP" in all_actions,
                "canUpload": "PUBLISH" in all_actions,
                "canEdit": "EDIT" in all_actions,
                "canControl": "CONTROL" in all_actions
            }
        }
        
        # 按类型分类
        if subject_type == "USER":
            parsed_data["users"].append(permission_record)
            parsed_data["summary"]["users_count"] += 1
        elif subject_type == "ROLE":
            parsed_data["roles"].append(permission_record)
            parsed_data["summary"]["roles_count"] += 1
        elif subject_type == "COMPANY":
            parsed_data["companies"].append(permission_record)
            parsed_data["summary"]["companies_count"] += 1
    
    return parsed_data


def determine_permission_level(actions):
    """
    根据权限动作确定权限级别
    """
    actions_set = set(actions)
    
    # 从高到低检查权限级别
    for level_key, level_info in reversed(list(PermissionLevel.ACC_PERMISSION_LEVELS.items())):
        level_actions_set = set(level_info["actions"])
        if level_actions_set.issubset(actions_set):
            return level_info
    
    # 如果没有匹配的权限级别，返回最低级别
    return {
        "level": 0,
        "name": "No Permission",
        "description": "No permissions"
    }


def get_project_folders_recursive(project_id, headers, max_depth=10):
    """
    递归获取项目的所有文件夹
    """
    try:
        # 获取顶级文件夹
        hub_id = None
        
        try:
            hubs_resp = requests.get(f"{config.AUTODESK_API_BASE}/project/v1/hubs", headers=headers)
            if hubs_resp.status_code == 200:
                hubs_data = hubs_resp.json()
                for hub in hubs_data.get('data', []):
                    hub_id = hub.get('id')
                    break
        except Exception as e:
            print(f"Hub API调用失败: {e}")
        
        # 如果无法通过API获取Hub，尝试使用企业账户映射
        if not hub_id:
            print("尝试使用企业账户映射获取Hub ID")
            import utils
            enterprise_hub_id, _, _ = utils.get_enterprise_hub_info()
            if enterprise_hub_id:
                hub_id = enterprise_hub_id
                print(f"使用企业Hub ID: {hub_id}")
        
        if not hub_id:
            raise Exception("Valid Hub ID not found")
        
        # 获取顶级文件夹
        top_folders_url = f"{config.AUTODESK_API_BASE}/project/v1/hubs/{hub_id}/projects/{project_id}/topFolders"
        response = requests.get(top_folders_url, headers=headers, timeout=(10, 30))
        
        if response.status_code != 200:
            raise Exception(f"Failed to get top-level folders: {response.status_code}")
        
        top_folders_data = response.json()
        all_folders = []
        
        # 递归获取所有文件夹
        for top_folder in top_folders_data.get('data', []):
            folder_info = {
                "id": top_folder.get('id'),
                "name": top_folder.get('attributes', {}).get('displayName', 'Unknown'),
                "path": top_folder.get('attributes', {}).get('displayName', 'Unknown'),
                "level": 0,
                "parent_id": None
            }
            all_folders.append(folder_info)
            
            # 递归获取子文件夹
            sub_folders = get_sub_folders_recursive(
                project_id, top_folder.get('id'), headers, 
                folder_info["path"], 1, max_depth
            )
            all_folders.extend(sub_folders)
        
        return all_folders
        
    except Exception as e:
        print(f"❌ 获取项目文件夹时出错: {str(e)}")
        return []


def get_sub_folders_recursive(project_id, folder_id, headers, parent_path, current_depth, max_depth):
    """
    递归获取子文件夹
    """
    if current_depth >= max_depth:
        return []
    
    try:
        contents_url = f"{config.AUTODESK_API_BASE}/data/v1/projects/{project_id}/folders/{folder_id}/contents"
        response = requests.get(contents_url, headers=headers, timeout=(10, 30))
        
        if response.status_code != 200:
            return []
        
        contents_data = response.json()
        sub_folders = []
        
        for item in contents_data.get('data', []):
            if item.get('type') == 'folders':
                item_id = item.get('id')
                item_name = item.get('attributes', {}).get('displayName', 'Unknown')
                folder_path = f"{parent_path}/{item_name}"
                
                folder_info = {
                    "id": item_id,
                    "name": item_name,
                    "path": folder_path,
                    "level": current_depth,
                    "parent_id": folder_id
                }
                sub_folders.append(folder_info)
                
                # 继续递归
                deeper_folders = get_sub_folders_recursive(
                    project_id, item_id, headers, folder_path, 
                    current_depth + 1, max_depth
                )
                sub_folders.extend(deeper_folders)
        
        return sub_folders
        
    except Exception as e:
        print(f"❌ 获取子文件夹时出错: {str(e)}")
        return []


@permissions_sync_bp.route('/api/permissions-sync/folder/<project_id>/<folder_id>')
def get_single_folder_permissions(project_id, folder_id):
    """
    获取单个文件夹的权限信息
    """
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
        # 获取权限数据
        permissions_result = get_folder_permissions_from_api(project_id, folder_id, headers)
        
        if permissions_result["status"] != "success":
            return jsonify(permissions_result), 400
        
        # 解析权限数据
        parsed_permissions = parse_permissions_data(permissions_result["data"])
        
        return jsonify({
            "status": "success",
            "project_id": project_id,
            "folder_id": folder_id,
            "permissions": parsed_permissions,
            "api_info": {
                "api_url": permissions_result["api_url"],
                "retrieved_at": permissions_result["retrieved_at"]
            }
        })
        
    except Exception as e:
        return jsonify({
            "error": f"获取文件夹权限失败: {str(e)}",
            "status": "error"
        }), 500


@permissions_sync_bp.route('/api/permissions-sync/project/<project_id>/sync')
def sync_project_permissions(project_id):
    """
    同步整个项目的文件夹权限
    """
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
        print(f"🚀 开始同步项目权限: {project_id}")
        start_time = time.time()
        
        # 获取参数
        max_depth = request.args.get('maxDepth', 5, type=int)
        include_empty_folders = request.args.get('includeEmptyFolders', 'true').lower() == 'true'
        
        # 获取所有文件夹
        print("📁 获取项目文件夹结构...")
        all_folders = get_project_folders_recursive(project_id, headers, max_depth)
        
        if not all_folders:
            return jsonify({
                "error": "Unable to get project folders",
                "status": "error"
            }), 404
        
        print(f"📊 找到 {len(all_folders)} 个文件夹，开始同步权限...")
        
        # 同步每个文件夹的权限
        permissions_data = {
            "project_id": project_id,
            "sync_time": datetime.now().isoformat(),
            "folders": [],
            "statistics": {
                "total_folders": len(all_folders),
                "successful_syncs": 0,
                "failed_syncs": 0,
                "total_users": 0,
                "total_roles": 0,
                "total_companies": 0,
                "sync_duration_seconds": 0
            },
            "errors": []
        }
        
        for i, folder in enumerate(all_folders):
            folder_id = folder["id"]
            folder_name = folder["name"]
            folder_path = folder["path"]
            
            print(f"🔍 同步文件夹权限 ({i+1}/{len(all_folders)}): {folder_name}")
            
            # 获取文件夹权限
            permissions_result = get_folder_permissions_from_api(project_id, folder_id, headers)
            
            if permissions_result["status"] == "success":
                # 解析权限数据
                parsed_permissions = parse_permissions_data(permissions_result["data"])
                
                folder_permissions = {
                    "folder_info": folder,
                    "permissions": parsed_permissions,
                    "sync_status": "success",
                    "sync_time": permissions_result["retrieved_at"]
                }
                
                permissions_data["folders"].append(folder_permissions)
                permissions_data["statistics"]["successful_syncs"] += 1
                permissions_data["statistics"]["total_users"] += parsed_permissions["summary"]["users_count"]
                permissions_data["statistics"]["total_roles"] += parsed_permissions["summary"]["roles_count"]
                permissions_data["statistics"]["total_companies"] += parsed_permissions["summary"]["companies_count"]
                
            else:
                # 记录错误
                error_info = {
                    "folder_id": folder_id,
                    "folder_name": folder_name,
                    "folder_path": folder_path,
                    "error": permissions_result.get("error"),
                    "error_code": permissions_result.get("error_code"),
                    "http_status": permissions_result.get("http_status")
                }
                
                permissions_data["errors"].append(error_info)
                permissions_data["statistics"]["failed_syncs"] += 1
                
                # 如果不包含空文件夹，也添加basicInfo
                if include_empty_folders:
                    folder_permissions = {
                        "folder_info": folder,
                        "permissions": None,
                        "sync_status": "error",
                        "error": permissions_result.get("error")
                    }
                    permissions_data["folders"].append(folder_permissions)
            
            # 添加延迟避免API限流
            time.sleep(0.2)
        
        # 更新统计信息
        end_time = time.time()
        permissions_data["statistics"]["sync_duration_seconds"] = round(end_time - start_time, 2)
        
        print(f"✅ 权限同步完成:")
        print(f"   📁 成功: {permissions_data['statistics']['successful_syncs']}")
        print(f"   ❌ 失败: {permissions_data['statistics']['failed_syncs']}")
        print(f"   👥 用户: {permissions_data['statistics']['total_users']}")
        print(f"   🎭 角色: {permissions_data['statistics']['total_roles']}")
        print(f"   🏢 公司: {permissions_data['statistics']['total_companies']}")
        print(f"   ⏱️ 耗时: {permissions_data['statistics']['sync_duration_seconds']} 秒")
        
        return jsonify({
            "status": "success",
            "message": f"成功同步 {permissions_data['statistics']['successful_syncs']} 个文件夹的权限",
            "data": permissions_data
        })
        
    except Exception as e:
        return jsonify({
            "error": f"同步项目权限失败: {str(e)}",
            "status": "error"
        }), 500


@permissions_sync_bp.route('/api/permissions-sync/project/<project_id>/download')
def download_project_permissions(project_id):
    """
    下载项目权限数据为JSON文件
    """
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
        # 首先同步权限数据
        print(f"🔄 准备下载项目权限数据: {project_id}")
        
        max_depth = request.args.get('maxDepth', 5, type=int)
        include_empty_folders = request.args.get('includeEmptyFolders', 'true').lower() == 'true'
        
        # 获取所有文件夹
        all_folders = get_project_folders_recursive(project_id, headers, max_depth)
        
        if not all_folders:
            return jsonify({
                "error": "Unable to get project folders",
                "status": "error"
            }), 404
        
        # 同步权限数据
        permissions_data = {
            "project_id": project_id,
            "export_time": datetime.now().isoformat(),
            "export_parameters": {
                "max_depth": max_depth,
                "include_empty_folders": include_empty_folders
            },
            "folders": [],
            "statistics": {
                "total_folders": len(all_folders),
                "successful_syncs": 0,
                "failed_syncs": 0,
                "total_users": 0,
                "total_roles": 0,
                "total_companies": 0
            },
            "errors": []
        }
        
        for folder in all_folders:
            folder_id = folder["id"]
            
            # 获取文件夹权限
            permissions_result = get_folder_permissions_from_api(project_id, folder_id, headers)
            
            if permissions_result["status"] == "success":
                parsed_permissions = parse_permissions_data(permissions_result["data"])
                
                folder_permissions = {
                    "folder_info": folder,
                    "permissions": parsed_permissions,
                    "sync_status": "success",
                    "sync_time": permissions_result["retrieved_at"]
                }
                
                permissions_data["folders"].append(folder_permissions)
                permissions_data["statistics"]["successful_syncs"] += 1
                permissions_data["statistics"]["total_users"] += parsed_permissions["summary"]["users_count"]
                permissions_data["statistics"]["total_roles"] += parsed_permissions["summary"]["roles_count"]
                permissions_data["statistics"]["total_companies"] += parsed_permissions["summary"]["companies_count"]
                
            else:
                error_info = {
                    "folder_id": folder_id,
                    "folder_name": folder["name"],
                    "folder_path": folder["path"],
                    "error": permissions_result.get("error"),
                    "error_code": permissions_result.get("error_code")
                }
                
                permissions_data["errors"].append(error_info)
                permissions_data["statistics"]["failed_syncs"] += 1
            
            time.sleep(0.1)  # 避免API限流
        
        # 创建下载文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"project_{project_id}_permissions_{timestamp}.json"
        
        # 确保下载目录存在
        download_dir = "downloads"
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        
        file_path = os.path.join(download_dir, filename)
        
        # 写入JSON文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(permissions_data, f, ensure_ascii=False, indent=2)
        
        print(f"📁 权限数据已保存到: {file_path}")
        
        # 返回文件下载
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/json'
        )
        
    except Exception as e:
        return jsonify({
            "error": f"下载权限数据失败: {str(e)}",
            "status": "error"
        }), 500


@permissions_sync_bp.route('/api/permissions-sync/permission-levels')
def get_permission_levels():
    """
    获取权限级别定义
    """
    return jsonify({
        "status": "success",
        "permission_levels": PermissionLevel.ACC_PERMISSION_LEVELS,
        "description": "ACC文件夹权限级别定义"
    })
