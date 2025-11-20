# -*- coding: utf-8 -*-
"""
下载配置 API 模块
处理文件下载配置、缓存和异步下载功能
"""

import requests
import json
import os
import threading
import time
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, send_file
from concurrent.futures import ThreadPoolExecutor
import config
import utils
from .urn_download_simple import download_by_urn, download_oss_object

download_config_bp = Blueprint('download_config', __name__)

# 缓存配置
CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', 'cache')
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'ACC_BACKUP', 'assets')
CACHE_EXPIRY_HOURS = 24  # 缓存24小时

# 异步下载任务队列
download_tasks = {}
executor = None  # 延迟初始化

def get_executor():
    """获取线程池执行器，延迟初始化"""
    global executor
    if executor is None:
        executor = ThreadPoolExecutor(max_workers=4)
    return executor

def shutdown_executor():
    """关闭线程池执行器"""
    global executor
    if executor is not None:
        print("[Download] Shutting down ThreadPoolExecutor...")
        executor.shutdown(wait=True)
        executor = None
        print("[Download] ThreadPoolExecutor shutdown complete")

# 确保目录存在
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def get_project_name_from_cache(project_id):
    """从前端localStorage缓存中获取项目名称"""
    try:
        # 尝试从session中获取项目缓存信息
        from flask import session
        
        # 检查session中是否有项目信息
        if 'project_cache' in session:
            project_cache = session['project_cache']
            if isinstance(project_cache, dict) and project_id in project_cache:
                cached_name = project_cache[project_id]
                print(f"✅ 从session缓存获取项目名称: {cached_name} (ID: {project_id})")
                return cached_name
        
        # 如果session中没有，尝试从API获取（作为备选方案）
        return get_project_name_by_id_from_api(project_id)
        
    except Exception as e:
        print(f"❌ 从缓存获取项目名称时出错: {str(e)}")
        return get_project_name_by_id_from_api(project_id)

def get_project_name_by_id_from_api(project_id):
    """通过项目ID从API获取项目名称（备选方案）"""
    try:
        access_token = utils.get_access_token()
        if not access_token:
            print("⚠️ 无法获取访问令牌，使用默认项目名称")
            return 'Project Files'
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # 获取Hub信息
        hubs_resp = requests.get(f"{config.AUTODESK_API_BASE}/project/v1/hubs", headers=headers)
        if hubs_resp.status_code != 200:
            print(f"⚠️ 无法获取Hub信息: {hubs_resp.status_code}")
            return 'Project Files'
            
        hubs_data = hubs_resp.json()
        
        # 遍历所有Hub查找项目
        for hub in hubs_data.get('data', []):
            hub_id = hub.get('id')
            
            # 获取该Hub下的项目
            projects_resp = requests.get(
                f"{config.AUTODESK_API_BASE}/project/v1/hubs/{hub_id}/projects",
                headers=headers
            )
            
            if projects_resp.status_code == 200:
                projects_data = projects_resp.json()
                
                for project in projects_data.get('data', []):
                    if project.get('id') == project_id:
                        project_name = project.get('attributes', {}).get('name', 'Project Files')
                        print(f"✅ 找到项目: {project_name} (ID: {project_id})")
                        return project_name
        
        print(f"⚠️ 未找到项目ID: {project_id}")
        return 'Project Files'
        
    except Exception as e:
        print(f"❌ 获取项目名称时出错: {str(e)}")
        return 'Project Files'

def get_project_name_by_id(project_id):
    """通过项目ID获取项目名称（优先从缓存获取）"""
    return get_project_name_from_cache(project_id)

def safe_write_file(file_path, content, filename=None, create_dirs=True):
    """安全写入文件，处理权限错误和文件名冲突，支持创建目录结构"""
    try:
        # 确保目录存在
        if create_dirs:
            dir_path = os.path.dirname(file_path)
            os.makedirs(dir_path, exist_ok=True)
        
        # 如果文件已存在，添加时间戳避免冲突
        if os.path.exists(file_path):
            dir_path = os.path.dirname(file_path)
            base_name, ext = os.path.splitext(os.path.basename(file_path))
            timestamp = int(time.time())
            new_filename = f"{base_name}_{timestamp}{ext}"
            file_path = os.path.join(dir_path, new_filename)
            if filename:
                filename = new_filename
        
        with open(file_path, 'wb') as f:
            f.write(content)
        
        return {
            'success': True,
            'file_path': file_path,
            'filename': filename or os.path.basename(file_path)
        }
        
    except PermissionError as pe:
        print(f"❌ 权限错误，尝试使用备用文件名: {str(pe)}")
        # 使用时间戳创建唯一文件名
        dir_path = os.path.dirname(file_path)
        base_name, ext = os.path.splitext(os.path.basename(file_path))
        timestamp = int(time.time())
        backup_filename = f"{base_name}_backup_{timestamp}{ext}"
        backup_path = os.path.join(dir_path, backup_filename)
        
        with open(backup_path, 'wb') as f:
            f.write(content)
        
        return {
            'success': True,
            'file_path': backup_path,
            'filename': backup_filename
        }
    except Exception as e:
        print(f"❌ 文件写入失败: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

@download_config_bp.route('/api/download-config/projects', methods=['GET'])
def get_available_projects():
    """获取可用的项目列表"""
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
        # 获取Hub信息
        hubs_resp = requests.get(f"{config.AUTODESK_API_BASE}/project/v1/hubs", headers=headers)
        if hubs_resp.status_code != 200:
            return jsonify({
                "error": f"无法获取Hub信息: {hubs_resp.status_code}",
                "status": "error"
            }), 400
        
        hubs_data = hubs_resp.json()
        projects = []
        
        for hub in hubs_data.get('data', []):
            hub_id = hub.get('id')
            hub_name = hub.get('attributes', {}).get('name', 'Unknown Hub')
            
            # 获取该Hub下的项目
            projects_resp = requests.get(
                f"{config.AUTODESK_API_BASE}/project/v1/hubs/{hub_id}/projects",
                headers=headers
            )
            
            if projects_resp.status_code == 200:
                projects_data = projects_resp.json()
                
                for project in projects_data.get('data', []):
                    project_info = {
                        'id': project.get('id'),
                        'name': project.get('attributes', {}).get('name', 'Unknown Project'),
                        'hub_id': hub_id,
                        'hub_name': hub_name,
                        'type': project.get('attributes', {}).get('extension', {}).get('data', {}).get('projectType', 'Unknown')
                    }
                    projects.append(project_info)
        
        return jsonify({
            "status": "success",
            "projects": projects,
            "count": len(projects)
        })
        
    except Exception as e:
        return jsonify({
            "error": f"获取项目列表失败: {str(e)}",
            "status": "error"
        }), 500

@download_config_bp.route('/api/download-config/project/<project_id>/folders', methods=['GET'])
def get_project_folders(project_id):
    """获取项目的文件夹结构"""
    access_token = utils.get_access_token()
    if not access_token:
        return jsonify({
            "error": "未找到 Access Token，请先进行认证",
            "status": "unauthorized"
        }), 401
    
    # 检查缓存
    cache_key = f"folders_{project_id}"
    cached_data = get_cached_data(cache_key)
    if cached_data:
        return jsonify({
            "status": "success",
            "data": cached_data,
            "cached": True
        })
    
    try:
        # 获取maxDepth参数
        max_depth = request.args.get('maxDepth', 20, type=int)
        
        # 获取项目文件树（遍历所有文件找寻文件夹）
        tree_url = f"http://localhost:{config.PORT}/api/file-sync/project/{project_id}/tree"
        params = {'maxDepth': max_depth, 'includeVersions': 'false'}  # 使用动态深度参数
        
        response = requests.get(tree_url, params=params, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                tree_data = data.get('data', {})
                
                # 提取文件夹结构
                folders = []
                
                def extract_folders(node, path="", level=0):
                    if level > 20:  # 增加递归深度以遍历所有文件夹
                        return
                    
                    current_path = f"{path}/{node.get('name', '')}" if path else node.get('name', '')
                    
                    if node.get('type') == 'folder':
                        folder_info = {
                            'id': node.get('id'),
                            'name': node.get('name'),
                            'path': current_path,
                            'level': level,
                            'file_count': count_files_in_folder(node),
                            'folder_count': count_folders_in_folder(node)
                        }
                        folders.append(folder_info)
                    
                    for child in node.get('children', []):
                        extract_folders(child, current_path, level + 1)
                
                for top_folder in tree_data.get('top_folders', []):
                    extract_folders(top_folder)
                
                # 缓存结果
                cache_data(cache_key, folders)
                
                return jsonify({
                    "status": "success",
                    "folders": folders,
                    "count": len(folders),
                    "cached": False
                })
            else:
                return jsonify({
                    "error": data.get('error', 'Unknown error'),
                    "status": "error"
                }), 400
        else:
            return jsonify({
                "error": f"获取文件夹失败: {response.status_code}",
                "status": "error"
            }), 400
            
    except Exception as e:
        return jsonify({
            "error": f"获取文件夹失败: {str(e)}",
            "status": "error"
        }), 500

@download_config_bp.route('/api/download-config/project/<project_id>/files', methods=['GET'])
def get_project_files(project_id):
    """获取项目的文件列表"""
    access_token = utils.get_access_token()
    if not access_token:
        return jsonify({
            "error": "未找到 Access Token，请先进行认证",
            "status": "unauthorized"
        }), 401
    
    # 获取查询参数 - 支持多种格式
    folder_ids = request.args.getlist('folder_ids')  # 支持多个文件夹
    if not folder_ids:
        # 尝试其他可能的参数名
        folder_ids = request.args.getlist('folder_ids[]')
    if not folder_ids and 'folder_ids' in request.args:
        # 单个值的情况
        folder_ids = [request.args.get('folder_ids')]
    
    file_types = request.args.getlist('file_types')  # 支持多个文件类型
    if not file_types:
        file_types = request.args.getlist('file_types[]')
    if not file_types and 'file_types' in request.args:
        file_types = [request.args.get('file_types')]
    
    # 调试参数解析
    print(f"🔍 API参数解析: folder_ids={folder_ids}, file_types={file_types}")
    print(f"🔍 原始请求参数: {dict(request.args)}")
    
    # 获取maxDepth参数，支持无限递归
    max_depth = request.args.get('maxDepth', 20, type=int)
    # 如果maxDepth设置为999或更大，则设置为一个很大的值来实现无限递归
    if max_depth >= 999:
        max_depth = 9999  # 设置一个实际上不可能达到的深度
    
    # 对于文件夹过滤，确保有足够的深度来遍历所有可能的子文件夹
    if folder_ids and max_depth < 15:
        max_depth = 15  # 确保能够遍历到深层嵌套的文件夹
        print(f"🔧 为文件夹过滤调整最大深度到: {max_depth}")
    
    # 检查是否有时间戳参数，如果有则跳过缓存
    bypass_cache = request.args.get('_t') is not None
    if bypass_cache:
        print(f"⚡ 检测到时间戳参数，跳过缓存直接获取最新数据")
    
    try:
        
        # 直接从后端获取项目名称
        project_name = get_project_name_by_id(project_id)
        print(f"📋 文件预览API - 从后端获取项目名称: '{project_name}', 项目ID: {project_id}")
        
        # 检查缓存（包含项目名称和搜索深度在缓存键中）
        # 清理文件夹ID中的无效字符（Windows文件名不允许冒号等字符）
        safe_folder_ids = []
        if folder_ids:
            for folder_id in sorted(folder_ids):
                # 移除URN前缀和无效字符，只保留最后的ID部分
                safe_id = folder_id.replace('urn:adsk.wipprod:fs.folder:co.', '').replace(':', '_')
                safe_folder_ids.append(safe_id)
        folder_key = '-'.join(safe_folder_ids) if safe_folder_ids else 'all'
        
        file_type_key = '-'.join(sorted(file_types)) if file_types else 'all'
        # 使用项目名称的安全版本作为缓存键的一部分
        safe_project_name = "".join(c for c in project_name if c.isalnum() or c in (' ', '-', '_')).replace(' ', '_')
        # 包含搜索深度以区分不同的搜索请求
        depth_key = f"d{max_depth}"
        cache_key = f"files_{project_id}_{safe_project_name}_{folder_key}_{file_type_key}_{depth_key}"
        
        # 只有在不跳过缓存时才检查和使用缓存
        if not bypass_cache:
            cached_data = get_cached_data(cache_key)
            if cached_data:
                print(f"📦 使用缓存数据，避免重复文件树遍历")
                print(f"   缓存键: {cache_key}")
                print(f"   缓存文件数: {len(cached_data.get('files', []))}")
                return jsonify({
                    "status": "success",
                    "data": cached_data,
                    "cached": True,
                    "message": "使用缓存数据，避免重复文件树遍历"
                })
        else:
            print(f"⚡ 跳过缓存检查，直接获取最新数据")
        
        # 如果有文件夹过滤，先获取文件夹结构建立ID到路径的映射
        folder_path_mapping = {}
        if folder_ids:
            folders_url = f"http://localhost:{config.PORT}/api/download-config/project/{project_id}/folders"
            folders_response = requests.get(folders_url, params={'maxDepth': 10}, timeout=60)
            if folders_response.status_code == 200:
                folders_data = folders_response.json()
                if folders_data.get('status') == 'success':
                    folders_list = folders_data.get('data', [])
                    for folder in folders_list:
                        folder_id = folder.get('id')
                        folder_path = folder.get('path', '')
                        folder_name = folder.get('name', '')
                        if folder_id:
                            folder_path_mapping[folder_id] = {
                                'path': folder_path,
                                'name': folder_name
                            }
            print(f"🗂️ 建立文件夹映射: {len(folder_path_mapping)} 个文件夹")
            # 调试：打印目标文件夹的映射信息
            for target_folder_id in folder_ids:
                if target_folder_id in folder_path_mapping:
                    mapping_info = folder_path_mapping[target_folder_id]
                    print(f"   📁 目标文件夹 {target_folder_id}: 路径='{mapping_info['path']}', 名称='{mapping_info['name']}'")
                else:
                    print(f"   ❌ 目标文件夹 {target_folder_id} 未在映射中找到")
        
        # 优化：当只需要特定文件夹时，使用更合理的搜索深度
        print(f"🔧 DEBUG: 准备使用 max_depth: {max_depth}")
        if folder_ids:
            print(f"🎯 文件夹过滤模式：目标文件夹 {folder_ids}")
            # 对于文件夹过滤，确保有足够的深度来遍历深层嵌套的文件夹
            # 特别是test文件夹有11层深的嵌套
            optimized_max_depth = max(max_depth, 25)  # 确保至少25层深度
            print(f"🚀 优化搜索深度：调整到 {optimized_max_depth} 层以支持深层嵌套")
        else:
            optimized_max_depth = max_depth
            print(f"🔧 DEBUG: 使用原始 max_depth: {optimized_max_depth}")
        
        # 获取项目文件树
        tree_url = f"http://localhost:{config.PORT}/api/file-sync/project/{project_id}/tree"
        params = {'maxDepth': optimized_max_depth, 'includeVersions': 'true'}
        
        # 如果有目标文件夹过滤，使用优化的遍历策略
        if folder_ids:
            # 正确传递列表参数
            for i, folder_id in enumerate(folder_ids):
                params[f'target_folder_ids[{i}]'] = folder_id
            params['optimize_traversal'] = 'true'  # 启用分支跳过优化
            print(f"🎯 传递目标文件夹过滤参数: {folder_ids}")
            print(f"⚡ 启用分支跳过优化")
            print(f"🔧 参数格式: {[(k, v) for k, v in params.items() if 'target_folder_ids' in k or 'optimize_traversal' in k]}")
        
        # 根据深度调整超时时间
        timeout = 180 if optimized_max_depth >= 20 else 120
        
        response = requests.get(tree_url, params=params, timeout=timeout)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                tree_data = data.get('data', {})
                
                # 提取文件信息和文件夾信息
                files = []
                folders = []  # 添加文件夾列表
                
                def extract_files(node, path="", proj_name="Project Files", is_root=True, parent_folder_id=None):
                    # 使用與file_sync_api一致的路徑構建邏輯
                    node_name = node.get('name', '')
                    node_type = node.get('type', '')
                    
                    # 构建当前项目的路径 - 與file_sync_api保持一致
                    if path and path != "Project Files":
                        current_path = f"{path}/{node_name}"
                    else:
                        current_path = node_name
                    
                    # 确定当前节点的文件夹ID
                    if node_type == 'folder':
                        current_folder_id = node.get('id')
                        
                        # 收集文件夹信息（跳過根節點 "Project Files"）
                        if not (is_root and node_name == 'Project Files'):
                            folder_info = {
                                'id': current_folder_id,
                                'name': node_name,
                                'path': current_path,  # 文件夹的完整路径
                                'parent_id': parent_folder_id
                            }
                            folders.append(folder_info)
                            print(f"   📁 收集文件夾信息: {node_name} -> {current_path}")
                    else:
                        current_folder_id = parent_folder_id
                    
                    # 调试信息：打印路径构建过程
                    node_name = node.get('name', '')
                    node_type = node.get('type', '')
                    print(f"   🔍 处理节点: 名称='{node_name}', 类型='{node_type}', 路径='{current_path}', 文件夹ID='{current_folder_id}'")
                    
                    # 如果是根节点且名称是"Project Files"，跳过这个名称
                    if is_root and node_name == 'Project Files':
                        # 直接处理子节点，不添加根节点名称到路径
                        print(f"   📁 处理根节点 'Project Files'，跳过根节点名称")
                        for child in node.get('children', []):
                            extract_files(child, "", proj_name, False, current_folder_id)
                        return
                    
                    # 优化：如果指定了文件夹过滤，检查当前分支是否可能包含目标文件夹
                    if folder_ids and node.get('type') == 'folder':
                        current_node_id = node.get('id')
                        node_name = node.get('name', '')
                        
                        # 检查当前文件夹是否是目标文件夹之一
                        is_target_folder = current_node_id in folder_ids
                        
                        # 检查当前文件夹是否可能是目标文件夹的父文件夹
                        might_contain_target = False
                        
                        # 方法1: 使用文件夹映射检查
                        for target_folder_id in folder_ids:
                            if target_folder_id in folder_path_mapping:
                                target_path = folder_path_mapping[target_folder_id]['path']
                                target_name = folder_path_mapping[target_folder_id]['name']
                                # 检查目标路径是否包含当前文件夹名称
                                if node_name in target_path or current_path in target_path:
                                    might_contain_target = True
                                    break
                        
                        # 方法2: 如果文件夹映射不完整，使用宽松的匹配策略
                        if not might_contain_target:
                            # 对于根级别的文件夹，总是继续遍历（避免过早跳过）
                            if path == "" or "/" not in current_path:
                                might_contain_target = True
                                print(f"   🔍 根级别文件夹，继续遍历: {node_name}")
                            else:
                                # 对于深层文件夹，检查名称是否匹配目标文件夹的某些特征
                                for target_folder_id in folder_ids:
                                    if target_folder_id in folder_path_mapping:
                                        target_info = folder_path_mapping[target_folder_id]
                                        target_name = target_info.get('name', '')
                                        target_path = target_info.get('path', '')
                                        
                                        # 检查当前路径是否是目标文件夹路径的一部分
                                        if target_path:
                                            normalized_target_path = target_path.replace('Project Files/', '')
                                            # 如果当前路径是目标路径的前缀，或者目标路径包含当前路径
                                            if (normalized_target_path.startswith(current_path + '/') or 
                                                current_path.startswith(normalized_target_path.split('/')[0])):
                                                might_contain_target = True
                                                print(f"   🔍 路径匹配，继续遍历: {node_name} (当前: {current_path}, 目标: {normalized_target_path})")
                                                break
                                        
                                        # 检查文件夹名称是否匹配
                                        if target_name and (node_name.lower() == target_name.lower() or 
                                                          target_name.lower() in current_path.lower() or
                                                          current_path.lower().startswith(target_name.lower())):
                                            might_contain_target = True
                                            print(f"   🔍 名称匹配，继续遍历: {node_name}")
                                            break
                        
                        # 智能分支跳过优化 - 只遍历相关的文件夹分支
                        if not is_target_folder and not might_contain_target:
                            print(f"   ⏭️ 跳过不相关分支: {node_name} (路径: {current_path})")
                            return
                        
                        # 显示分支遍历决策
                        if is_target_folder:
                            print(f"   ✅ 目标文件夹，继续遍历: {node_name}")
                        elif might_contain_target:
                            print(f"   🔍 可能包含目标，继续遍历: {node_name}")
                        else:
                            print(f"   🔍 继续遍历: {node_name}")
                    
                    if node.get('type') == 'file':
                        file_name = node.get('name', '')
                        file_ext = get_file_extension(file_name)
                        
                        # 文件类型过滤
                        if file_types and file_ext not in file_types:
                            return
                        
                        # 临时禁用文件夹过滤，查看所有文件
                        if folder_ids:
                            # 检查文件是否在指定的文件夹中（包括子文件夹）
                            file_in_target_folder = False
                            print(f"   🔍 检查文件 '{file_name}' 是否在目标文件夹中")
                            print(f"   📂 文件路径: '{current_path}', 父文件夹ID: '{current_folder_id}'")
                            print(f"   🎯 目标文件夹IDs: {folder_ids}")
                            
                            # 使用正确的路径匹配检查
                            for target_folder_id in folder_ids:
                                # 方法1: 直接检查父文件夹ID
                                if current_folder_id == target_folder_id:
                                    file_in_target_folder = True
                                    print(f"   ✅ 文件直接匹配父文件夹ID: {file_name} -> {target_folder_id}")
                                    break
                                
                                # 方法2: 检查文件是否在目标文件夹的子文件夹中
                                if is_file_in_target_folder_hierarchy(current_path, current_folder_id, target_folder_id, folder_path_mapping):
                                    file_in_target_folder = True
                                    print(f"   ✅ 文件在目标文件夹层次结构中: {file_name} -> {target_folder_id}")
                                    break
                            
                            if not file_in_target_folder:
                                print(f"   ❌ 文件 '{file_name}' 不在任何目标文件夹中，跳过")
                                return
                        
                        # 获取文件大小信息
                        file_size = 0
                        versions = node.get('versions', [])
                        if versions:
                            # 使用最新版本的文件大小
                            latest_version = versions[0]  # 版本按时间排序，第一个是最新的
                            file_size = latest_version.get('fileSize', 0) or latest_version.get('storageSize', 0)
                        
                        # 如果版本中没有大小信息，尝试从attributes获取
                        if file_size == 0:
                            file_size = node.get('attributes', {}).get('size', 0) or node.get('attributes', {}).get('storageSize', 0)
                        
                        # 构建显示路径，以项目名称为根
                        display_path = f"{proj_name}/{current_path}" if current_path else proj_name
                        
                        # 计算文件夹路径（不包含文件名）
                        # 修复：current_path 对于文件来说是完整路径（父文件夹路径/文件名）
                        # 需要提取文件夹部分（去掉文件名）
                        folder_path = ""
                        if current_path:
                            path_parts = current_path.split('/')
                            if len(path_parts) > 1:
                                # 有多个部分，最后一个是文件名，前面的是文件夹路径
                                folder_path = '/'.join(path_parts[:-1])
                                print(f"   📁 计算文件夹路径: '{current_path}' -> '{folder_path}'")
                            else:
                                # 只有一个部分（文件名），说明文件在根目录
                                folder_path = ""
                                print(f"   📁 文件在根目录: '{current_path}' -> 无子路径")
                        else:
                            print(f"   📁 空路径，文件在根目录")
                        
                        file_info = {
                            'id': node.get('id'),
                            'name': file_name,
                            'path': display_path,  # 显示路径包含项目名称
                            'original_path': current_path,  # 保存完整相对路径（包含文件名）
                            'folder_path': folder_path,  # 保存文件夹路径（不包含文件名）
                            'extension': file_ext,
                            'type': get_file_type_description(file_ext),
                            'size': file_size,
                            'versions': len(versions),
                            'last_modified': node.get('attributes', {}).get('lastModifiedTime'),
                            'downloadable': is_file_downloadable(file_ext),
                            'original_name': file_name  # 保存原始文件名
                        }
                        files.append(file_info)
                    
                    # 处理子节点（文件夹和文件）- 與file_sync_api保持一致
                    children = node.get('children', [])
                    for child in children:
                        # 对于子节点，当前节点的ID就是子节点的父文件夹ID
                        child_parent_folder_id = node.get('id') if node_type == 'folder' else parent_folder_id
                        # 使用當前路徑作為子節點的父路徑 - 與file_sync_api一致
                        next_path = current_path
                        print(f"   📂 递归处理子节点: 父节点='{node_name}' (ID: {node.get('id')}), 子节点='{child.get('name')}', 传递路径='{next_path}', 传递的父ID='{child_parent_folder_id}'")
                        extract_files(child, next_path, proj_name, False, child_parent_folder_id)
                
                for top_folder in tree_data.get('top_folders', []):
                    extract_files(top_folder, "", project_name, True, None)
                
                # 添加调试信息
                if folder_ids:
                    print(f"🔍 文件夹过滤结果: 目标文件夹={folder_ids}, 匹配文件数={len(files)}")
                
                # 按文件类型分组
                files_by_type = {}
                for file_info in files:
                    file_type = file_info['type']
                    if file_type not in files_by_type:
                        files_by_type[file_type] = []
                    files_by_type[file_type].append(file_info)
                
                result = {
                    'files': files,
                    'folders': folders,  # 添加文件夾信息
                    'files_by_type': files_by_type,
                    'total_count': len(files),
                    'folder_count': len(folders),  # 添加文件夾數量
                    'downloadable_count': len([f for f in files if f['downloadable']]),
                    'total_size': sum(f['size'] for f in files)
                }
                
                # 只有在不跳过缓存时才缓存结果
                if not bypass_cache:
                    cache_data(cache_key, result)
                    print(f"💾 数据已缓存，避免下次重复遍历")
                    print(f"   缓存键: {cache_key}")
                    print(f"   缓存文件数: {len(result.get('files', []))}")
                    print(f"   缓存文件夹数: {len(result.get('folders', []))}")
                else:
                    print(f"⚡ 跳过缓存保存，不缓存此次结果")
                
                return jsonify({
                    "status": "success",
                    "data": result,
                    "cached": False
                })
            else:
                return jsonify({
                    "error": data.get('error', 'Unknown error'),
                    "status": "error"
                }), 400
        else:
            return jsonify({
                "error": f"获取文件列表失败: {response.status_code}",
                "status": "error"
            }), 400
            
    except Exception as e:
        return jsonify({
            "error": f"获取文件列表失败: {str(e)}",
            "status": "error"
        }), 500

@download_config_bp.route('/api/download-config/project/<project_id>/debug', methods=['GET'])
def debug_project_files(project_id):
    """调试项目文件数量问题"""
    access_token = utils.get_access_token()
    if not access_token:
        return jsonify({
            "error": "未找到 Access Token，请先进行认证",
            "status": "unauthorized"
        }), 401
    
    try:
        # 获取maxDepth参数
        max_depth = request.args.get('maxDepth', 20, type=int)
        
        # 获取原始文件树（遍历所有层级以获取完整数据）
        tree_url = f"http://localhost:{config.PORT}/api/file-sync/project/{project_id}/tree"
        params = {'maxDepth': max_depth, 'includeVersions': 'true'}
        
        response = requests.get(tree_url, params=params, timeout=120)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                tree_data = data.get('data', {})
                
                # 统计原始数据
                def count_all_files(node):
                    count = 0
                    if node.get('type') == 'file':
                        count = 1
                    for child in node.get('children', []):
                        count += count_all_files(child)
                    return count
                
                def analyze_tree_structure(node, path="", level=0):
                    """分析树结构，返回详细信息"""
                    current_path = f"{path}/{node.get('name', '')}" if path else node.get('name', '')
                    node_info = {
                        'name': node.get('name', ''),
                        'type': node.get('type', 'unknown'),
                        'id': node.get('id', ''),
                        'path': current_path,
                        'level': level,
                        'children_count': len(node.get('children', [])),
                        'children': []
                    }
                    
                    for child in node.get('children', []):
                        child_info = analyze_tree_structure(child, current_path, level + 1)
                        node_info['children'].append(child_info)
                    
                    return node_info
                
                total_files_in_tree = 0
                tree_structure = []
                
                for top_folder in tree_data.get('top_folders', []):
                    total_files_in_tree += count_all_files(top_folder)
                    folder_structure = analyze_tree_structure(top_folder)
                    tree_structure.append(folder_structure)
                
                return jsonify({
                    "status": "success",
                    "debug_info": {
                        "project_id": project_id,
                        "tree_statistics": tree_data.get('statistics', {}),
                        "actual_file_count_in_tree": total_files_in_tree,
                        "top_folders_count": len(tree_data.get('top_folders', [])),
                        "tree_structure": tree_structure
                    }
                })
        
        return jsonify({
            "error": "Unable to get project file tree",
            "status": "error"
        }), 400
        
    except Exception as e:
        return jsonify({
            "error": f"调试失败: {str(e)}",
            "status": "error"
        }), 500

@download_config_bp.route('/api/download-config/download', methods=['POST'])
def start_download():
    """开始异步下载文件"""
    access_token = utils.get_access_token()
    if not access_token:
        return jsonify({
            "error": "未找到 Access Token，请先进行认证",
            "status": "unauthorized"
        }), 401
    
    try:
        request_data = request.json
        print(f"📥 收到下载请求: {json.dumps(request_data, indent=2, ensure_ascii=False)}")
        
        project_id = request_data.get('project_id')
        # 直接从后端获取项目名称，不依赖前端传递
        project_name = get_project_name_by_id(project_id)
        file_ids = request_data.get('file_ids', [])
        download_options = request_data.get('options', {})
        
        print(f"📋 解析参数: project_id={project_id}, project_name='{project_name}' (从后端获取), file_ids数量={len(file_ids)}")
        print(f"🔍 完整请求数据: {json.dumps(request_data, indent=2, ensure_ascii=False)}")
        print(f"🔧 下载选项: {json.dumps(download_options, indent=2, ensure_ascii=False)}")
        # 检查createFolders选项（在options数组中）
        create_folders = 'createFolders' in download_options.get('options', [])
        print(f"📁 createFolders选项: {create_folders}")
        print(f"📁 options数组: {download_options.get('options', [])}")
        
        # 智能获取文件路径信息，优先使用缓存避免重复遍历
        file_path_mapping = {}
        empty_folders = []  # 存储空文件夹信息
        if create_folders:
            print("🔍 获取文件路径信息和空文件夹...")
            try:
                # 优化策略：尝试从最近的API调用结果中获取路径信息
                # 检查是否有最近的文件列表缓存可以使用
                print(f"📁 智能路径获取：检查 {len(file_ids)} 个文件的路径信息")
                
                # 尝试调用文件列表API获取路径信息（这可能会使用缓存）
                files_params = {'project_name': project_name}
                files_response = requests.get(f"http://localhost:{config.PORT}/api/download-config/project/{project_id}/files", 
                                            params=files_params, timeout=30)
                if files_response.status_code == 200:
                    files_data = files_response.json()
                    if files_data.get('status') == 'success':
                        all_files = files_data.get('data', {}).get('files', [])
                        all_folders = files_data.get('data', {}).get('folders', [])
                        print(f"📋 从API获取到 {len(all_files)} 个文件信息和 {len(all_folders)} 个文件夹信息")
                        
                        # 只为我们需要下载的文件创建路径映射
                        matched_files = 0
                        for file_info in all_files:
                            file_id = file_info.get('id')
                            if file_id in file_ids:  # 只处理我们要下载的文件
                                folder_path = file_info.get('folder_path', '')
                                original_path = file_info.get('original_path', '')
                                file_name = file_info.get('name', '')
                                
                                print(f"   ✅ 找到下载文件: {file_name}")
                                print(f"      ID: {file_id}")
                                print(f"      文件夹路径: '{folder_path}'")
                                print(f"      原始路径: '{original_path}'")
                                
                                file_path_mapping[file_id] = {
                                    'path': folder_path,
                                    'name': file_name,
                                    'original_path': original_path
                                }
                                matched_files += 1
                        
                        # 收集空文件夹信息
                        file_folder_paths = set()
                        for file_info in all_files:
                            if file_info.get('id') in file_ids:
                                folder_path = file_info.get('folder_path', '')
                                if folder_path:
                                    file_folder_paths.add(folder_path)
                        
                        # 查找空文件夹（没有文件的文件夹）
                        for folder_info in all_folders:
                            folder_path = folder_info.get('path', '')
                            folder_name = folder_info.get('name', '')
                            if folder_path and folder_path not in file_folder_paths:
                                empty_folders.append({
                                    'path': folder_path,
                                    'name': folder_name
                                })
                                print(f"   📁 發現空文件夾: {folder_name} (路徑: {folder_path})")
                        
                        print(f"✅ 成功匹配 {matched_files}/{len(file_ids)} 个文件的路径信息")
                        print(f"📁 發現 {len(empty_folders)} 個空文件夾")
                        
                        if matched_files < len(file_ids):
                            print(f"⚠️ 有 {len(file_ids) - matched_files} 个文件未找到路径信息，下载时将使用动态获取")
                    else:
                        print(f"⚠️ 获取文件列表失败: {files_data.get('error')}")
                        print("🔄 将在下载时动态获取路径信息")
                else:
                    print(f"⚠️ 文件列表API调用失败: {files_response.status_code}")
                    print("🔄 将在下载时动态获取路径信息")
            except Exception as e:
                print(f"⚠️ 获取文件路径信息时出错: {str(e)}")
                print("🔄 将在下载时动态获取路径信息")
        else:
            print("📁 跳过文件夹结构创建")
        
        if not project_id or not file_ids:
            print(f"❌ 参数验证失败: project_id={project_id}, file_ids={file_ids}")
            return jsonify({
                "error": "缺少必要参数: project_id 和 file_ids",
                "status": "error"
            }), 400
        
        # 创建下载任务
        task_id = f"download_{int(time.time())}_{len(file_ids)}"
        
        download_task = {
            'task_id': task_id,
            'project_id': project_id,
            'project_name': project_name,  # 添加项目名称到任务中
            'file_ids': file_ids,
            'options': download_options,
            'status': 'pending',
            'progress': 0,
            'total_files': len(file_ids),
            'completed_files': 0,
            'failed_files': 0,
            'start_time': datetime.now().isoformat(),
            'estimated_completion': None,
            'downloaded_files': [],
            'file_progress': {},  # 每个文件的下载进度
            'file_path_mapping': file_path_mapping,  # 文件路径映射信息
            'empty_folders': empty_folders,  # 空文件夹信息
            'errors': []
        }
        
        download_tasks[task_id] = download_task
        print(f"💾 任务已存储: {task_id}, 当前任务总数: {len(download_tasks)}")
        
        # 提交异步任务
        future = get_executor().submit(execute_download_task, task_id, access_token)
        download_task['future'] = future
        
        print(f"🚀 异步任务已提交: {task_id}")
        
        return jsonify({
            "status": "success",
            "task_id": task_id,
            "message": f"开始下载 {len(file_ids)} 个文件",
            "estimated_time": f"{len(file_ids) * 2} 秒"  # 估算每个文件2秒
        })
        
    except Exception as e:
        return jsonify({
            "error": f"启动下载失败: {str(e)}",
            "status": "error"
        }), 500

@download_config_bp.route('/api/download-config/download/<task_id>/status', methods=['GET'])
def get_download_status(task_id):
    """获取下载任务状态"""
    if task_id not in download_tasks:
        return jsonify({
            "error": "Download task does not exist",
            "status": "error"
        }), 404
    
    task = download_tasks[task_id]
    
    # 计算进度
    if task['total_files'] > 0:
        task['progress'] = int((task['completed_files'] / task['total_files']) * 100)
    
    # 移除不需要序列化的字段
    response_task = {k: v for k, v in task.items() if k != 'future'}
    
    return jsonify({
        "status": "success",
        "task": response_task
    })

@download_config_bp.route('/api/download-config/download/<task_id>/cancel', methods=['POST'])
def cancel_download(task_id):
    """cancel下载任务"""
    if task_id not in download_tasks:
        return jsonify({
            "error": "Download task does not exist",
            "status": "error"
        }), 404
    
    task = download_tasks[task_id]
    
    # 尝试cancel任务
    if 'future' in task and not task['future'].done():
        task['future'].cancel()
    
    task['status'] = 'cancelled'
    
    return jsonify({
        "status": "success",
        "message": "Download task cancelled"
    })

@download_config_bp.route('/api/download-config/downloads', methods=['GET'])
def list_downloads():
    """列出所有下载任务"""
    print(f"📋 查询下载任务列表, 当前任务数: {len(download_tasks)}")
    
    tasks = []
    for task_id, task in download_tasks.items():
        print(f"   - 任务: {task_id}, 状态: {task.get('status')}")
        # 移除不需要序列化的字段
        task_info = {k: v for k, v in task.items() if k != 'future'}
        tasks.append(task_info)
    
    return jsonify({
        "status": "success",
        "tasks": tasks,
        "count": len(tasks)
    })

@download_config_bp.route('/api/download-config/clear-cache', methods=['POST'])
def clear_cache():
    """清除缓存"""
    try:
        import glob
        cache_files = glob.glob(os.path.join(CACHE_DIR, "*.json"))
        for cache_file in cache_files:
            os.remove(cache_file)
        
        return jsonify({
            "status": "success",
            "message": f"已清除 {len(cache_files)} 个缓存文件"
        })
    except Exception as e:
        return jsonify({
            "error": f"清除缓存失败: {str(e)}",
            "status": "error"
        }), 500

@download_config_bp.route('/api/download-config/file-types', methods=['GET'])
def get_supported_file_types():
    """获取支持的文件类型"""
    file_types = {
        'documents': {
            'name': 'Document Files',
            'extensions': ['pdf', 'doc', 'docx', 'txt', 'rtf', 'md'],
            'downloadable': True
        },
        'cad': {
            'name': 'CAD文件',
            'extensions': ['dwg', 'dxf', 'dwf'],
            'downloadable': True
        },
        'bim': {
            'name': 'BIM模型',
            'extensions': ['rvt', 'rfa', 'ifc'],
            'downloadable': True
        },
        '3d_models': {
            'name': '3D模型',
            'extensions': ['3dm', 'step', 'stp', 'iges', 'igs', 'obj', 'fbx', 'max', 'skp'],
            'downloadable': True
        },
        'images': {
            'name': 'Image Files',
            'extensions': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'],
            'downloadable': True
        },
        'spreadsheets': {
            'name': 'Spreadsheet Files',
            'extensions': ['xls', 'xlsx', 'csv'],
            'downloadable': True
        },
        'presentations': {
            'name': 'Presentation Files',
            'extensions': ['ppt', 'pptx'],
            'downloadable': True
        },
        'archives': {
            'name': 'Archive Files',
            'extensions': ['zip', 'rar', '7z', 'tar', 'gz'],
            'downloadable': True
        },
        'videos': {
            'name': 'Video Files',
            'extensions': ['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv'],
            'downloadable': True
        },
        'audio': {
            'name': 'Audio Files',
            'extensions': ['mp3', 'wav', 'aac', 'flac', 'ogg'],
            'downloadable': True
        }
    }
    
    return jsonify({
        "status": "success",
        "file_types": file_types
    })

@download_config_bp.route('/api/download-config/open-folder', methods=['POST'])
def open_download_folder():
    """打开下载文件夹"""
    try:
        request_data = request.json
        task_id = request_data.get('task_id')
        project_name = request_data.get('project_name', 'Project Files')
        
        if not task_id:
            return jsonify({
                "error": "缺少任务ID",
                "status": "error"
            }), 400
        
        # 构建文件夹路径
        folder_path = os.path.join(DOWNLOAD_DIR, project_name)
        
        # 确保文件夹存在
        if not os.path.exists(folder_path):
            return jsonify({
                "error": f"文件夹不存在: {folder_path}",
                "status": "error"
            }), 404
        
        # 根据操作系统打开文件夹
        import platform
        import subprocess
        
        system = platform.system()
        
        try:
            if system == "Windows":
                # Windows: 使用 os.startfile 或 subprocess 调用 explorer
                try:
                    # 方法1: 使用 os.startfile (Windows专用)
                    os.startfile(folder_path)
                except (OSError, AttributeError):
                    # 方法2: 使用 subprocess 调用 explorer
                    normalized_path = os.path.normpath(folder_path)
                    subprocess.run(['cmd', '/c', 'start', '', normalized_path], check=True, shell=True)
            elif system == "Darwin":  # macOS
                # macOS: 使用 open
                subprocess.run(['open', folder_path], check=True)
            elif system == "Linux":
                # Linux: 使用 xdg-open
                subprocess.run(['xdg-open', folder_path], check=True)
            else:
                return jsonify({
                    "error": f"不支持的操作系统: {system}",
                    "status": "error"
                }), 400
            
            return jsonify({
                "status": "success",
                "message": f"已打开文件夹: {folder_path}",
                "folder_path": folder_path
            })
            
        except subprocess.CalledProcessError as e:
            return jsonify({
                "error": f"打开文件夹失败: {str(e)}",
                "status": "error"
            }), 500
        except FileNotFoundError:
            return jsonify({
                "error": "System does not support folder opening functionality",
                "status": "error"
            }), 500
            
    except Exception as e:
        return jsonify({
            "error": f"打开文件夹失败: {str(e)}",
            "status": "error"
        }), 500

# 辅助函数
def count_files_in_folder(folder_node):
    """统计文件夹中的文件数量"""
    count = 0
    for child in folder_node.get('children', []):
        if child.get('type') == 'file':
            count += 1
        elif child.get('type') == 'folder':
            count += count_files_in_folder(child)
    return count

def count_folders_in_folder(folder_node):
    """统计文件夹中的子文件夹数量"""
    count = 0
    for child in folder_node.get('children', []):
        if child.get('type') == 'folder':
            count += 1 + count_folders_in_folder(child)
    return count

def get_file_extension(filename):
    """获取文件扩展名"""
    if '.' in filename:
        return filename.split('.')[-1].lower()
    return ''

def get_file_type_description(extension):
    """获取文件类型描述"""
    type_map = {
        'pdf': 'PDF Document',
        'doc': 'Word Document', 'docx': 'Word Document',
        'xls': 'Excel Spreadsheet', 'xlsx': 'Excel Spreadsheet',
        'ppt': 'PowerPoint', 'pptx': 'PowerPoint',
        'dwg': 'AutoCAD Drawing', 'dxf': 'AutoCAD Exchange File',
        'rvt': 'Revit Model', 'rfa': 'Revit Family File',
        'ifc': 'IFC Model',
        'jpg': 'JPEG Image', 'jpeg': 'JPEG Image', 'png': 'PNG Image', 'gif': 'GIF Image',
        'mp4': 'MP4 Video', 'avi': 'AVI Video', 'mov': 'MOV Video', 'wmv': 'WMV Video',
        'mp3': 'MP3 Audio', 'wav': 'WAV Audio',
        'zip': 'ZIP Archive', 'rar': 'RAR Archive', '7z': '7Z Archive',
        'md': 'Markdown Document', 'txt': 'Text Document'
    }
    return type_map.get(extension, f'{extension.upper()} File')

def is_file_downloadable(extension):
    """判断文件是否可下载"""
    downloadable_extensions = {
        'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
        'dwg', 'dxf', 'rvt', 'rfa', 'ifc',
        'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff',
        'zip', 'rar', '7z', 'txt', 'csv', 'md',  
        'mp4', 'avi', 'mov', 'wmv', 'flv',  # 视频文件
        'mp3', 'wav', 'aac', 'flac',  # 音频文件
        '3dm', 'step', 'stp', 'iges', 'igs', 'obj', 'fbx', 'max', 'skp'  # 3D模型
    }
    return extension in downloadable_extensions

def is_file_in_target_folder_hierarchy(file_path, current_folder_id, target_folder_id, folder_path_mapping):
    """
    检查文件是否在目标文件夹的层次结构中（包括子文件夹）
    使用严格的层次结构检查
    """
    if not target_folder_id or not folder_path_mapping:
        return False
    
    print(f"   🔍 检查文件夹层次结构: 文件='{file_path}', 当前文件夹='{current_folder_id}', 目标='{target_folder_id}'")
    
    # 获取目标文件夹信息
    if target_folder_id not in folder_path_mapping:
        print(f"   ❌ 目标文件夹不在映射中: {target_folder_id}")
        return False
    
    target_folder_info = folder_path_mapping[target_folder_id]
    target_folder_path = target_folder_info.get('path', '')
    target_folder_name = target_folder_info.get('name', '')
    
    print(f"   📁 目标文件夹信息: 名称='{target_folder_name}', 路径='{target_folder_path}'")
    
    # 方法1: 直接检查当前文件夹ID是否就是目标文件夹
    if current_folder_id == target_folder_id:
        print(f"   ✅ 当前文件夹就是目标文件夹: {current_folder_id}")
        return True
    
    # 方法2: 严格检查文件路径是否在目标文件夹下
    if target_folder_name and file_path:
        # 文件路径必须以"目标文件夹名称/"开头
        if file_path.startswith(target_folder_name + '/'):
            print(f"   ✅ 文件路径在目标文件夹下: {file_path} -> {target_folder_name}")
            return True
        else:
            print(f"   ❌ 文件路径不在目标文件夹下: {file_path} 不以 '{target_folder_name}/' 开头")
    
    # 方法3: 检查当前文件夹是否在目标文件夹的层次结构中
    if current_folder_id and current_folder_id in folder_path_mapping:
        current_folder_info = folder_path_mapping[current_folder_id]
        current_folder_path = current_folder_info.get('path', '')
        current_folder_name = current_folder_info.get('name', '')
        
        print(f"   📂 当前文件夹信息: 名称='{current_folder_name}', 路径='{current_folder_path}'")
        
        # 严格检查当前文件夹路径是否在目标文件夹路径下
        if target_folder_path and current_folder_path:
            # 规范化路径（移除 'Project Files/' 前缀）
            normalized_target_path = target_folder_path.replace('Project Files/', '').replace('Project Files', '').strip('/')
            normalized_current_path = current_folder_path.replace('Project Files/', '').replace('Project Files', '').strip('/')
            
            # 严格的层次关系检查：当前文件夹必须在目标文件夹下或就是目标文件夹
            if normalized_current_path == normalized_target_path:
                print(f"   ✅ 当前文件夹就是目标文件夹: '{normalized_current_path}'")
                return True
            elif normalized_current_path.startswith(normalized_target_path + '/'):
                print(f"   ✅ 当前文件夹在目标文件夹层次结构中: '{normalized_current_path}' -> '{normalized_target_path}'")
                return True
            else:
                print(f"   ❌ 当前文件夹不在目标文件夹层次结构中: '{normalized_current_path}' 不在 '{normalized_target_path}' 下")
    
    print(f"   ❌ 文件不在目标文件夹层次结构中")
    return False

def is_file_in_folder_by_path(file_path, target_folder_id, folder_path_mapping):
    """使用路径匹配检查文件是否在指定的文件夹中"""
    if not target_folder_id:
        print(f"   ❌ 目标文件夹ID为空")
        return False
    
    print(f"   🔍 检查文件是否在目标文件夹中: 文件='{file_path}', 目标文件夹ID='{target_folder_id}'")
    
    # 方法1: 使用文件夹映射进行精确匹配（如果可用）
    if folder_path_mapping and target_folder_id in folder_path_mapping:
        folder_info = folder_path_mapping[target_folder_id]
        target_folder_path = folder_info.get('path', '')
        target_folder_name = folder_info.get('name', '')
        
        print(f"   📁 使用文件夹映射: 名称='{target_folder_name}', 路径='{target_folder_path}'")
        
        # 检查文件路径是否以目标文件夹路径开头（精确匹配）
        if target_folder_path:
            # 规范化路径格式
            normalized_folder_path = target_folder_path.replace('Project Files/', '')
            normalized_file_path = file_path
            
            # 确保路径匹配是精确的（避免部分匹配）
            # 文件必须在目标文件夹内或其子文件夹内
            if normalized_file_path.startswith(normalized_folder_path + '/'):
                print(f"   ✅ 文件路径精确匹配文件夹: {file_path} -> {normalized_folder_path}")
                return True
            
            # 检查文件是否直接在目标文件夹根目录下
            # 例如: file_path="test/file.txt", target_folder_path="Project Files/test"
            if normalized_file_path.startswith(target_folder_name + '/'):
                print(f"   ✅ 文件在目标文件夹根目录: {file_path} -> {target_folder_name}")
                return True
        
        # 检查文件路径是否包含目标文件夹名称（严格匹配）
        if target_folder_name:
            path_parts = file_path.split('/')
            if target_folder_name in path_parts:
                # 确保文件夹名称匹配是完整的，且文件在该文件夹内
                folder_index = path_parts.index(target_folder_name)
                # 文件应该在文件夹之后的路径中，或者文件夹是路径的最后一部分（表示文件在该文件夹根目录）
                if folder_index < len(path_parts) - 1:
                    print(f"   ✅ 文件路径包含文件夹名称: {file_path} -> {target_folder_name}")
                    return True
                elif folder_index == len(path_parts) - 1 and len(path_parts) == 1:
                    # 特殊情况：文件路径只是文件夹名称，可能表示文件在该文件夹根目录
                    # 但这种情况需要额外验证，暂时不匹配
                    print(f"   ⚠️ 文件路径只包含文件夹名称，需要额外验证: {file_path}")
                    return False
    
    # 方法2: 严格匹配 - 如果无法通过路径映射确定文件是否在目标文件夹中，则排除该文件
    # 这确保只有明确属于目标文件夹的文件才会被包含，避免误匹配
    print(f"   ❌ 无法通过路径映射确定文件是否在目标文件夹中，排除该文件")
    return False

def is_file_in_folder(file_node, target_folder_id, file_path, parent_folder_id=None):
    """检查文件是否在指定的文件夹中（包括子文件夹）- 保留向后兼容性"""
    if not target_folder_id:
        return False
    
    target_folder_id_str = str(target_folder_id)
    file_name = file_node.get('name', '')
    
    # 方法1: 直接检查父文件夹ID
    if parent_folder_id and str(parent_folder_id) == target_folder_id_str:
        print(f"   ✅ 文件 '{file_name}' 匹配父文件夹ID")
        return True
    
    # 方法2: 检查文件路径中是否包含目标文件夹ID
    if target_folder_id_str in file_path:
        print(f"   ✅ 文件 '{file_name}' 路径包含目标文件夹ID")
        return True
    
    # 方法3: 检查路径的各个部分是否包含目标文件夹ID
    path_parts = file_path.split('/')
    for part in path_parts:
        if target_folder_id_str == part:
            print(f"   ✅ 文件 '{file_name}' 路径部分匹配")
            return True
    
    return False

def path_contains_folder(file_path, folder_id):
    """检查文件路径是否包含指定文件夹（保留向后兼容性）"""
    # 如果没有指定文件夹ID，则不过滤（返回False表示不包含）
    if not folder_id:
        return False
    
    # 如果没有文件路径，则不包含
    if not file_path:
        return False
    
    # 将文件夹ID转换为字符串进行比较
    folder_id_str = str(folder_id)
    
    # 检查路径中是否包含指定的文件夹ID
    # 支持多种匹配方式：直接包含、路径分隔符匹配等
    if folder_id_str in file_path:
        return True
    
    # 如果folder_id看起来像一个文件夹名称而不是ID，也进行匹配
    path_parts = file_path.split('/')
    return folder_id_str in path_parts

def get_cached_data(cache_key):
    """获取缓存数据"""
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")
    
    if os.path.exists(cache_file):
        try:
            # 检查缓存是否过期
            file_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if datetime.now() - file_time < timedelta(hours=CACHE_EXPIRY_HOURS):
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
    
    return None

def cache_data(cache_key, data):
    """缓存数据"""
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")
    
    try:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"缓存数据失败: {str(e)}")

def execute_download_task(task_id, access_token):
    """执行下载任务"""
    task = download_tasks[task_id]
    task['status'] = 'running'
    
    try:
        project_id = task['project_id']
        file_ids = task['file_ids']
        
        # 創建空文件夾
        empty_folders = task.get('empty_folders', [])
        project_name = task.get('project_name', 'Project Files')
        if empty_folders:
            print(f"📁 開始創建 {len(empty_folders)} 個空文件夾...")
            for folder_info in empty_folders:
                folder_path = folder_info.get('path', '')
                folder_name = folder_info.get('name', '')
                if folder_path:
                    try:
                        # 構建完整的文件夾路徑
                        full_folder_path = os.path.join(DOWNLOAD_DIR, project_name, folder_path)
                        os.makedirs(full_folder_path, exist_ok=True)
                        print(f"   ✅ 創建空文件夾: {folder_name} -> {full_folder_path}")
                    except Exception as e:
                        print(f"   ❌ 創建空文件夾失敗: {folder_name} - {str(e)}")
                        task['errors'].append(f"創建空文件夾失敗: {folder_name} - {str(e)}")
            print(f"📁 空文件夾創建完成")
        
        for i, file_id in enumerate(file_ids):
            try:
                # 初始化文件进度
                task['file_progress'][file_id] = {
                    'status': 'downloading',
                    'progress': 0,
                    'filename': f'文件_{i+1}',
                    'start_time': datetime.now().isoformat()
                }
                
                # 下载单个文件
                result = download_single_file(project_id, file_id, access_token, task)
                
                if result.get('success'):
                    task['completed_files'] += 1
                    # 记录详细的下载信息
                    download_record = {
                        'file_id': file_id,
                        'filename': result.get('filename'),
                        'original_name': result.get('original_name'),
                        'file_path': result.get('file_path'),
                        'relative_path': result.get('relative_path'),
                        'file_size': result.get('file_size', 0),
                        'original_size': result.get('original_size', 0),
                        'download_time': datetime.now().isoformat()
                    }
                    task['downloaded_files'].append(download_record)
                    
                    # 更新文件进度
                    task['file_progress'][file_id].update({
                        'status': 'completed',
                        'progress': 100,
                        'filename': result.get('original_name', f'文件_{i+1}'),
                        'end_time': datetime.now().isoformat()
                    })
                else:
                    task['failed_files'] += 1
                    error_msg = result.get('error', 'Unknown error')
                    task['errors'].append(f"文件 {file_id} 下载失败: {error_msg}")
                    
                    # 更新文件进度
                    task['file_progress'][file_id].update({
                        'status': 'failed',
                        'progress': 0,
                        'error': error_msg,
                        'end_time': datetime.now().isoformat()
                    })
                
                # 更新总进度
                task['progress'] = int(((i + 1) / len(file_ids)) * 100)
                
                # 短暂延迟避免API限流
                time.sleep(0.5)
                
            except Exception as e:
                task['failed_files'] += 1
                task['errors'].append(f"文件 {file_id} 下载异常: {str(e)}")
        
        task['status'] = 'completed' if task['failed_files'] == 0 else 'completed_with_errors'
        task['end_time'] = datetime.now().isoformat()
        
    except Exception as e:
        task['status'] = 'failed'
        task['errors'].append(f"任务执行失败: {str(e)}")
        task['end_time'] = datetime.now().isoformat()

def download_single_file(project_id, file_id, access_token, task=None):
    """下载单个文件"""
    try:
        # 获取下载信息
        download_info_url = f"http://localhost:{config.PORT}/api/file-sync/download/{project_id}/{file_id}"
        
        response = requests.get(download_info_url, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            download_info = data.get('download_info', {})
            version_info = data.get('version_info', {})
            
            # 获取原始文件名和路径信息
            # 優先使用文件路徑映射中的文件名，確保一致性
            mapped_filename = None
            if task and task.get('file_path_mapping'):
                file_path_info = task['file_path_mapping'].get(file_id)
                if file_path_info:
                    mapped_filename = file_path_info.get('name')
                    print(f"   📄 從映射獲取文件名: '{mapped_filename}'")
            
            # 如果映射中有文件名，使用映射的；否則使用版本信息中的
            original_name = mapped_filename or version_info.get('attributes', {}).get('name', f"file_{file_id.split(':')[-1]}")
            file_size = version_info.get('attributes', {}).get('storageSize', 0)
            
            print(f"   📄 Final filename used: '{original_name}' (Source: {'Mapping' if mapped_filename else 'Version info'})")
            
            # 获取文件的真实项目路径
            relative_path = ""
            task_options = task.get('options', {}) if task else {}
            create_folders = 'createFolders' in task_options.get('options', [])
            if task and create_folders:
                print(f"🔍 开始获取文件路径信息 - 文件ID: {file_id}")
                # 尝试从任务中获取文件路径信息
                file_path_info = None
                
                # 从任务的文件ID列表中查找当前文件的路径信息
                if task and task.get('file_path_mapping'):
                    file_path_info = task['file_path_mapping'].get(file_id)
                    print(f"   📁 文件路径映射信息: {file_path_info}")
                
                if file_path_info and 'path' in file_path_info:
                    # 使用项目的真实路径结构
                    folder_path = file_path_info['path']
                    print(f"   📂 从映射获取文件夹路径: '{folder_path}'")
                    
                    # folder_path 已经是不包含文件名的文件夹路径
                    relative_path = folder_path
                    print(f"   ✅ 最终使用的相对路径: '{relative_path}'")
                    
                    # 如果路径为空，说明文件在根目录
                    if not relative_path:
                        print(f"   📁 文件将保存在项目根目录")
                    else:
                        print(f"   📁 文件将保存在子目录: {relative_path}")
                else:
                    # 对于单文件下载，动态获取文件的真实路径
                    print(f"   🔍 映射中没有路径信息，尝试动态获取文件路径...")
                    try:
                        # 调用文件列表API获取单个文件的路径信息
                        files_params = {'project_name': task.get('project_name', '')}
                        files_response = requests.get(f"http://localhost:{config.PORT}/api/download-config/project/{project_id}/files", 
                                                    params=files_params, timeout=30)
                        if files_response.status_code == 200:
                            files_data = files_response.json()
                            if files_data.get('status') == 'success':
                                all_files = files_data.get('data', {}).get('files', [])
                                # 查找当前文件的路径信息
                                for file_info in all_files:
                                    if file_info.get('id') == file_id:
                                        folder_path = file_info.get('folder_path', '')
                                        dynamic_filename = file_info.get('name', '')
                                        relative_path = folder_path
                                        
                                        # 如果動態獲取的文件名與當前不同，更新文件名以確保一致性
                                        if dynamic_filename and dynamic_filename != original_name:
                                            print(f"   📄 動態獲取的文件名與原始不同: '{original_name}' -> '{dynamic_filename}'")
                                            original_name = dynamic_filename
                                        
                                        print(f"   ✅ 动态获取到文件路径: '{relative_path}', 文件名: '{original_name}'")
                                        break
                                else:
                                    print(f"   ⚠️ 在文件列表中未找到文件ID: {file_id}")
                                    raise Exception("File not found")
                            else:
                                print(f"   ⚠️ 获取文件列表失败: {files_data.get('error')}")
                                raise Exception("Failed to get file list")
                        else:
                            print(f"   ⚠️ 文件列表API调用失败: {files_response.status_code}")
                            raise Exception("API call failed")
                    except Exception as e:
                        print(f"   ❌ 动态获取路径失败: {str(e)}")
                        # 最后回退到简单的文件类型分类
                        file_extension = os.path.splitext(original_name)[1].lower()
                        if file_extension in ['.pdf', '.doc', '.docx']:
                            relative_path = "documents"
                        elif file_extension in ['.dwg', '.dxf']:
                            relative_path = "cad"
                        elif file_extension in ['.jpg', '.jpeg', '.png']:
                            relative_path = "images"
                        else:
                            relative_path = "others"
                        print(f"   🔄 回退到文件类型分类: '{relative_path}'")
            
            download_method = download_info.get('method')
            
            if download_method == 'oss_signed_url':
                # 使用OSS签名URL下载原始文件（官方推荐方式）
                bucket_key = download_info.get('bucket_key')
                object_key = download_info.get('object_key')
                
                print(f"🚀 使用OSS签名URL下载原始文件: {original_name}")
                print(f"   Bucket: {bucket_key}, Object: {object_key}")
                
                if bucket_key and object_key:
                    # 获取签名下载URL
                    signed_url_endpoint = f"{config.AUTODESK_API_BASE}/oss/v2/buckets/{bucket_key}/objects/{object_key}/signeds3download"
                    print(f"   获取签名URL: {signed_url_endpoint}")
                    
                    signed_resp = requests.get(signed_url_endpoint, headers={'Authorization': f'Bearer {access_token}'}, timeout=30)
                    
                    if signed_resp.status_code == 200:
                        signed_data = signed_resp.json()
                        download_url = signed_data.get('url')
                        file_size_from_oss = signed_data.get('size', 0)
                        
                        print(f"   ✅ 获得签名URL，文件大小: {file_size_from_oss} bytes")
                        
                        if download_url:
                            # 使用签名URL下载文件
                            print(f"   🔗 开始下载: {download_url[:100]}...")
                            
                            # 注意：签名URL不需要Authorization头
                            file_response = requests.get(download_url, timeout=300)  # 增加超时时间
                            
                            if file_response.status_code == 200:
                                # 使用原始文件名
                                filename = original_name
                                
                                # 确保文件名安全
                                filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.')).rstrip()
                                
                                # 根据相对路径创建完整路径，使用项目名称作为根目录
                                project_name = task.get('project_name', 'Project Files')
                                print(f"💾 文件保存 - 项目名称: '{project_name}', 相对路径: '{relative_path}', 文件名: '{filename}'")
                                if relative_path:
                                    file_path = os.path.join(DOWNLOAD_DIR, project_name, relative_path, filename)
                                    print(f"   📁 完整路径(有子目录): {file_path}")
                                else:
                                    file_path = os.path.join(DOWNLOAD_DIR, project_name, filename)
                                    print(f"   📁 完整路径(根目录): {file_path}")
                                
                                # 使用安全写入函数
                                write_result = safe_write_file(file_path, file_response.content, filename, create_dirs=True)
                                if not write_result['success']:
                                    return {'success': False, 'error': f'Failed to save file: {write_result["error"]}'}
                                
                                file_path = write_result['file_path']
                                filename = write_result['filename']
                                final_file_size = len(file_response.content)
                                
                                print(f"✅ OSS原始文件下载成功: {filename} ({final_file_size} bytes)")
                                
                                return {
                                    'success': True,
                                    'filename': filename,
                                    'file_path': file_path,
                                    'relative_path': relative_path,
                                    'original_name': original_name,
                                    'file_size': final_file_size,
                                    'original_size': file_size_from_oss or file_size,
                                    'download_method': 'oss_signed_url'
                                }
                            else:
                                print(f"❌ 签名URL下载失败: {file_response.status_code}")
                                return {'success': False, 'error': f'Signed URL download failed: {file_response.status_code}'}
                        else:
                            print("❌ 签名响应中没有URL")
                            return {'success': False, 'error': 'No URL in signed response'}
                    else:
                        print(f"❌ 获取签名URL失败: {signed_resp.status_code} - {signed_resp.text}")
                        return {'success': False, 'error': f'Failed to get signed URL: {signed_resp.status_code}'}
                else:
                    return {'success': False, 'error': 'Missing bucket_key or object_key'}
            
            elif download_method == 'direct_storage_link':
                # 直接使用存储链接下载
                download_url = download_info.get('download_url')
                
                print(f"🚀 使用直接存储链接下载: {original_name}")
                
                if download_url:
                    direct_response = requests.get(download_url, headers={'Authorization': f'Bearer {access_token}'}, timeout=120)
                    
                    if direct_response.status_code == 200:
                        # 使用原始文件名
                        filename = original_name
                        
                        # 确保文件名安全
                        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.')).rstrip()
                        
                        # 根据相对路径创建完整路径，使用项目名称作为根目录
                        project_name = task.get('project_name', 'Project Files')
                        if relative_path:
                            file_path = os.path.join(DOWNLOAD_DIR, project_name, relative_path, filename)
                        else:
                            file_path = os.path.join(DOWNLOAD_DIR, project_name, filename)
                        
                        # 处理文件名冲突
                        if os.path.exists(file_path):
                            base_name, ext = os.path.splitext(filename)
                            timestamp = int(time.time())
                            filename = f"{base_name}_{timestamp}{ext}"
                            if relative_path:
                                file_path = os.path.join(DOWNLOAD_DIR, project_name, relative_path, filename)
                            else:
                                file_path = os.path.join(DOWNLOAD_DIR, project_name, filename)
                        
                        try:
                            # 确保目录存在
                            os.makedirs(os.path.dirname(file_path), exist_ok=True)
                            with open(file_path, 'wb') as f:
                                f.write(direct_response.content)
                        except PermissionError as pe:
                            print(f"❌ 权限错误，尝试使用备用文件名: {str(pe)}")
                            base_name, ext = os.path.splitext(filename)
                            timestamp = int(time.time())
                            filename = f"{base_name}_backup_{timestamp}{ext}"
                            if relative_path:
                                file_path = os.path.join(DOWNLOAD_DIR, project_name, relative_path, filename)
                            else:
                                file_path = os.path.join(DOWNLOAD_DIR, project_name, filename)
                            # 确保目录存在
                            os.makedirs(os.path.dirname(file_path), exist_ok=True)
                            with open(file_path, 'wb') as f:
                                f.write(direct_response.content)
                        
                        final_file_size = len(direct_response.content)
                        
                        print(f"✅ Data Management API直接下载成功: {filename} ({final_file_size} bytes)")
                        
                        return {
                            'success': True,
                            'filename': filename,
                            'file_path': file_path,
                            'relative_path': relative_path,
                            'original_name': original_name,
                            'file_size': final_file_size,
                            'original_size': file_size,
                            'download_method': 'data_management_direct'
                        }
                    else:
                        print(f"❌ Data Management API直接下载失败: {direct_response.status_code}")
                        return {'success': False, 'error': f'Data Management direct download failed: {direct_response.status_code}'}
                else:
                    return {'success': False, 'error': 'No download URL provided'}
            
            elif download_method == 'direct_pdf':
                # 直接下载完整PDF
                pdf_urn = download_info.get('pdf_urn')
                download_url = f"{download_info.get('download_base_url')}/{pdf_urn}"
                
                print(f"📄 直接下载完整PDF: {original_name}")
                
                pdf_response = requests.get(download_url, headers={'Authorization': f'Bearer {access_token}'}, timeout=120)
                
                if pdf_response.status_code == 200:
                    # 使用原始文件名
                    base_name = os.path.splitext(original_name)[0]
                    filename = f"{base_name}.pdf"
                    
                    # 确保文件名安全
                    filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.')).rstrip()
                    
                    # 根据相对路径创建完整路径，使用项目名称作为根目录
                    project_name = task.get('project_name', 'Project Files')
                    if relative_path:
                        file_path = os.path.join(DOWNLOAD_DIR, project_name, relative_path, filename)
                    else:
                        file_path = os.path.join(DOWNLOAD_DIR, project_name, filename)
                    
                    # 处理文件名冲突，如果文件已存在则添加时间戳
                    if os.path.exists(file_path):
                        base_name, ext = os.path.splitext(filename)
                        timestamp = int(time.time())
                        filename = f"{base_name}_{timestamp}{ext}"
                        if relative_path:
                            file_path = os.path.join(DOWNLOAD_DIR, project_name, relative_path, filename)
                        else:
                            file_path = os.path.join(DOWNLOAD_DIR, project_name, filename)
                    
                    # 使用安全写入函数
                    write_result = safe_write_file(file_path, pdf_response.content, filename, create_dirs=True)
                    if not write_result['success']:
                        return {'success': False, 'error': f'Failed to save file: {write_result["error"]}'}
                    
                    file_path = write_result['file_path']
                    filename = write_result['filename']
                    
                    final_file_size = len(pdf_response.content)
                    
                    print(f"✅ 完整PDF下载成功: {filename} ({final_file_size} bytes)")
                    
                    return {
                        'success': True,
                        'filename': filename,
                        'file_path': file_path,
                        'relative_path': relative_path,
                        'original_name': original_name,
                        'file_size': final_file_size,
                        'original_size': file_size,
                        'download_method': 'direct_pdf'
                    }
                else:
                    print(f"❌ 直接PDF下载失败: {pdf_response.status_code}")
                    return {'success': False, 'error': f'Direct PDF download failed: {pdf_response.status_code}'}
            
            elif download_method == 'original_file':
                # 下载原始文件
                storage_location = download_info.get('storage_location')
                
                print(f"📁 下载原始文件: {original_name}")
                
                # 构建OSS下载URL
                # storage_location格式通常是: urn:adsk.objects:os.object:bucket/object_key
                if storage_location and storage_location.startswith('urn:adsk.objects:os.object:'):
                    object_path = storage_location.replace('urn:adsk.objects:os.object:', '')
                    
                    # 分离bucket和object_key
                    if '/' in object_path:
                        bucket_key, object_key = object_path.split('/', 1)
                        download_url = f"{config.AUTODESK_API_BASE}/oss/v2/buckets/{bucket_key}/objects/{object_key}"
                    else:
                        # 如果格式不符合预期，尝试直接使用
                        download_url = f"{config.AUTODESK_API_BASE}/oss/v2/buckets/{object_path}"
                    
                    print(f"🔗 OSS下载URL: {download_url}")
                    
                    file_response = requests.get(download_url, headers={'Authorization': f'Bearer {access_token}'}, timeout=120)
                    
                    if file_response.status_code == 200:
                        # 使用原始文件名
                        filename = original_name
                        
                        # 确保文件名安全
                        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.')).rstrip()
                        
                        # 根据相对路径创建完整路径，使用项目名称作为根目录
                        project_name = task.get('project_name', 'Project Files')
                        if relative_path:
                            file_path = os.path.join(DOWNLOAD_DIR, project_name, relative_path, filename)
                        else:
                            file_path = os.path.join(DOWNLOAD_DIR, project_name, filename)
                        
                        # 处理文件名冲突，如果文件已存在则添加时间戳
                        if os.path.exists(file_path):
                            base_name, ext = os.path.splitext(filename)
                            timestamp = int(time.time())
                            filename = f"{base_name}_{timestamp}{ext}"
                            if relative_path:
                                file_path = os.path.join(DOWNLOAD_DIR, project_name, relative_path, filename)
                            else:
                                file_path = os.path.join(DOWNLOAD_DIR, project_name, filename)
                        
                        try:
                            # 确保目录存在
                            os.makedirs(os.path.dirname(file_path), exist_ok=True)
                            with open(file_path, 'wb') as f:
                                f.write(file_response.content)
                        except PermissionError as pe:
                            print(f"❌ 权限错误，尝试使用备用文件名: {str(pe)}")
                            # 使用时间戳创建唯一文件名
                            base_name, ext = os.path.splitext(filename)
                            timestamp = int(time.time())
                            filename = f"{base_name}_backup_{timestamp}{ext}"
                            if relative_path:
                                file_path = os.path.join(DOWNLOAD_DIR, project_name, relative_path, filename)
                            else:
                                file_path = os.path.join(DOWNLOAD_DIR, project_name, filename)
                            # 确保目录存在
                            os.makedirs(os.path.dirname(file_path), exist_ok=True)
                            with open(file_path, 'wb') as f:
                                f.write(file_response.content)
                        
                        final_file_size = len(file_response.content)
                        
                        print(f"✅ 原始文件下载成功: {filename} ({final_file_size} bytes)")
                        
                        return {
                            'success': True,
                            'filename': filename,
                            'file_path': file_path,
                            'original_name': original_name,
                            'file_size': final_file_size,
                            'original_size': file_size,
                            'download_method': 'original_file'
                        }
                    else:
                        print(f"❌ 原始文件下载失败: {file_response.status_code}")
                        return {'success': False, 'error': f'Original file download failed: {file_response.status_code}'}
                else:
                    return {'success': False, 'error': 'Invalid storage location format'}
            
            elif download_method == 'model_derivative':
                # 下载所有PDF页面并合并
                pdf_pages = download_info.get('pdf_pages', [])
                download_base_url = download_info.get('download_base_url')
                
                if not pdf_pages:
                    print("❌ 没有找到PDF页面信息")
                    return {'success': False, 'error': 'No PDF pages found'}
                
                print(f"📄 开始下载 {len(pdf_pages)} 个PDF页面...")
                
                # 下载所有页面
                page_contents = []
                total_size = 0
                
                for i, page_urn in enumerate(pdf_pages):
                    try:
                        page_download_url = f"{download_base_url}/{page_urn}"
                        print(f"🔗 下载页面 {i+1}/{len(pdf_pages)}: {page_urn}")
                        
                        page_resp = requests.get(page_download_url, 
                                               headers={'Authorization': f'Bearer {access_token}'}, 
                                               timeout=60)
                        
                        if page_resp.status_code == 200:
                            page_contents.append(page_resp.content)
                            total_size += len(page_resp.content)
                            print(f"✅ 页面 {i+1} 下载成功 ({len(page_resp.content)} bytes)")
                        else:
                            print(f"❌ 页面 {i+1} 下载失败: {page_resp.status_code}")
                            # 继续下载其他页面，不因为一页失败而终止
                            
                    except Exception as e:
                        print(f"❌ 下载页面 {i+1} 时出错: {str(e)}")
                        continue
                
                if not page_contents:
                    return {'success': False, 'error': 'Failed to download any PDF pages'}
                
                # 如果只有一页，直接保存
                if len(page_contents) == 1:
                    base_name = os.path.splitext(original_name)[0]
                    filename = f"{base_name}.pdf"
                    
                    # 确保文件名安全
                    filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.')).rstrip()
                    
                    # 根据相对路径创建完整路径，使用项目名称作为根目录
                    project_name = task.get('project_name', 'Project Files')
                    if relative_path:
                        file_path = os.path.join(DOWNLOAD_DIR, project_name, relative_path, filename)
                    else:
                        file_path = os.path.join(DOWNLOAD_DIR, project_name, filename)
                    
                    # 处理文件名冲突
                    if os.path.exists(file_path):
                        base_name, ext = os.path.splitext(filename)
                        timestamp = int(time.time())
                        filename = f"{base_name}_{timestamp}{ext}"
                        if relative_path:
                            file_path = os.path.join(DOWNLOAD_DIR, project_name, relative_path, filename)
                        else:
                            file_path = os.path.join(DOWNLOAD_DIR, project_name, filename)
                    
                    try:
                        # 确保目录存在
                        os.makedirs(os.path.dirname(file_path), exist_ok=True)
                        with open(file_path, 'wb') as f:
                            f.write(page_contents[0])
                        
                        print(f"✅ 单页PDF保存成功: {filename}")
                        
                        return {
                            'success': True,
                            'filename': filename,
                            'file_path': file_path,
                            'original_name': original_name,
                            'file_size': len(page_contents[0]),
                            'original_size': file_size,
                            'download_method': 'single_pdf_page'
                        }
                    except Exception as e:
                        print(f"❌ 保存PDF文件失败: {str(e)}")
                        return {'success': False, 'error': f'Failed to save PDF: {str(e)}'}
                
                # 多页PDF需要合并 - 但这是最低优先级的方案
                # 先尝试保存所有页面为单独文件，提示用户手动合并
                base_name = os.path.splitext(original_name)[0]
                saved_pages = []
                project_name = task.get('project_name', 'Project Files')
                
                for i, content in enumerate(page_contents):
                    page_filename = f"{base_name}_page{i+1}.pdf"
                    page_filename = "".join(c for c in page_filename if c.isalnum() or c in (' ', '-', '_', '.')).rstrip()
                    
                    if relative_path:
                        page_path = os.path.join(DOWNLOAD_DIR, project_name, relative_path, page_filename)
                    else:
                        page_path = os.path.join(DOWNLOAD_DIR, project_name, page_filename)
                    
                    try:
                        # 确保目录存在
                        os.makedirs(os.path.dirname(page_path), exist_ok=True)
                        with open(page_path, 'wb') as f:
                            f.write(content)
                        saved_pages.append(page_filename)
                        print(f"✅ 保存页面 {i+1}: {page_filename}")
                    except Exception as e:
                        print(f"❌ 保存页面 {i+1} 失败: {str(e)}")
                
                if saved_pages:
                    print(f"⚠️ PDF文件有 {len(page_contents)} 页，已保存为单独文件。建议使用PDF工具手动合并。")
                    
                    return {
                        'success': True,
                        'filename': f"{base_name}_pages.txt",  # 创建一个说明文件
                        'file_path': DOWNLOAD_DIR,
                        'original_name': original_name,
                        'file_size': total_size,
                        'original_size': file_size,
                        'download_method': 'multiple_pdf_pages',
                        'saved_pages': saved_pages,
                        'note': f'PDF文件包含{len(page_contents)}页，已保存为单独文件，建议手动合并'
                    }
                
                return {'success': False, 'error': 'Failed to save PDF pages'}
        
        return {'success': False, 'error': 'Download failed'}
        
    except Exception as e:
        print(f"下载文件 {file_id} 失败: {str(e)}")
        return {'success': False, 'error': str(e)}

@download_config_bp.route('/api/download-config/download-urn', methods=['GET'])
def download_urn_endpoint():
    """URN下载端点 - 使用现有的urn_download_simple模块"""
    try:
        urn = request.args.get('urn')
        document_name = request.args.get('document_name')
        
        if not urn:
            return jsonify({
                'success': False,
                'error': 'URN参数缺失'
            }), 400
        
        print(f"[URN Download] 处理URN下载请求: {urn}")
        
        # 使用现有的URN下载功能
        if 'os.object:' in urn:
            # OSS Object类型（包括快照）
            result = download_oss_object(urn, document_name=document_name)
        else:
            # 通用下载方法
            result = download_by_urn(urn, document_name=document_name)
        
        print(f"[URN Download] 下载结果: {result.get('success', False)}")
        
        if result.get('success'):
            return jsonify(result)
        else:
            return jsonify(result), 400
        
    except Exception as e:
        print(f"[URN Download] 下载失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'下载失败: {str(e)}'
        }), 500
