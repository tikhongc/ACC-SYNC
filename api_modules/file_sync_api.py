# -*- coding: utf-8 -*-
"""
文件同步 API 模块
处理 ACC 项目文件和文件夹的完整同步功能
使用 Autodesk Platform Services Data Management API
"""

import requests
import json
import os
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from flask import Blueprint, jsonify, request, send_file
import config
import utils

file_sync_bp = Blueprint('file_sync', __name__)

# 线程池用于并行处理
executor = ThreadPoolExecutor(max_workers=10)

def sanitize_user_info(user_id, user_name):
    """
    清理和标准化用户信息
    
    Args:
        user_id: 用户ID
        user_name: 用户名
        
    Returns:
        tuple: (cleaned_user_id, cleaned_user_name)
    """
    # 清理用户ID
    cleaned_user_id = None
    if user_id and str(user_id).strip():
        cleaned_user_id = str(user_id).strip()
    
    # 清理用户名
    cleaned_user_name = None
    if user_name and str(user_name).strip():
        cleaned_user_name = str(user_name).strip()
    
    return cleaned_user_id, cleaned_user_name

def get_permissions_parallel(project_id, folder_ids, headers):
    """
    并行获取多个文件夹的权限信息
    
    Args:
        project_id: 项目ID
        folder_ids: 文件夹ID列表
        headers: 请求头
        
    Returns:
        dict: {folder_id: permissions_result}
    """
    if not folder_ids:
        return {}
    
    print(f"🔄 并行获取 {len(folder_ids)} 个文件夹的权限信息")
    
    def get_single_permission(folder_id):
        try:
            return folder_id, get_folder_permissions_from_beta_api(project_id, folder_id, headers)
        except Exception as e:
            print(f"❌ 获取文件夹 {folder_id} 权限失败: {str(e)}")
            return folder_id, {"status": "error", "error": str(e)}
    
    # 使用线程池并行处理
    results = {}
    with ThreadPoolExecutor(max_workers=min(len(folder_ids), 5)) as pool:
        future_to_folder = {pool.submit(get_single_permission, folder_id): folder_id 
                           for folder_id in folder_ids}
        
        for future in as_completed(future_to_folder):
            folder_id, permission_result = future.result()
            results[folder_id] = permission_result
    
    print(f"✅ 并行权限获取完成: {len(results)} 个结果")
    return results

def get_versions_parallel(project_id, item_ids, headers):
    """
    并行获取多个文件的版本信息
    
    Args:
        project_id: 项目ID
        item_ids: 文件ID列表
        headers: 请求头
        
    Returns:
        dict: {item_id: versions_list}
    """
    if not item_ids:
        return {}
    
    print(f"🔄 并行获取 {len(item_ids)} 个文件的版本信息")
    
    def get_single_versions(item_id):
        try:
            return item_id, get_item_versions(project_id, item_id, headers)
        except Exception as e:
            print(f"❌ 获取文件 {item_id} 版本失败: {str(e)}")
            return item_id, []
    
    # 使用线程池并行处理
    results = {}
    with ThreadPoolExecutor(max_workers=min(len(item_ids), 8)) as pool:
        future_to_item = {pool.submit(get_single_versions, item_id): item_id 
                         for item_id in item_ids}
        
        for future in as_completed(future_to_item):
            item_id, versions = future.result()
            results[item_id] = versions
    
    print(f"✅ 并行版本获取完成: {len(results)} 个结果")
    return results


def get_multiple_folder_contents_batch(project_id, folder_ids, headers):
    """
    批量获取多个文件夹的内容
    
    Args:
        project_id: 项目ID
        folder_ids: 文件夹ID列表
        headers: 请求头
        
    Returns:
        dict: {folder_id: contents_data}
    """
    if not folder_ids:
        return {}
    
    print(f"🔄 批量获取 {len(folder_ids)} 个文件夹的内容")
    
    def get_single_folder_content(folder_id):
        try:
            return folder_id, get_folder_contents(project_id, folder_id, headers)
        except Exception as e:
            print(f"❌ 获取文件夹 {folder_id} 内容失败: {str(e)}")
            return folder_id, {"data": []}
    
    # 使用线程池批量处理
    results = {}
    with ThreadPoolExecutor(max_workers=min(len(folder_ids), 6)) as pool:
        future_to_folder = {pool.submit(get_single_folder_content, folder_id): folder_id 
                           for folder_id in folder_ids}
        
        for future in as_completed(future_to_folder):
            folder_id, content_data = future.result()
            results[folder_id] = content_data
    
    print(f"✅ 批量内容获取完成: {len(results)} 个结果")
    return results


def get_permissions_batch_api(project_id, folder_ids, headers):
    """
    批量权限API调用 - 尝试使用单个API调用获取多个文件夹权限
    如果不支持，则回退到并行调用
    """
    if not folder_ids:
        return {}
    
    # 检查是否支持批量权限API（这里假设暂时不支持，使用并行调用）
    # 未来如果Autodesk API支持批量权限查询，可以在这里实现
    
    print(f"🔄 使用并行方式批量获取权限（{len(folder_ids)} 个文件夹）")
    return get_permissions_parallel(project_id, folder_ids, headers)


def get_versions_batch_api(project_id, item_ids, headers):
    """
    批量版本API调用 - 尝试使用单个API调用获取多个文件版本
    如果不支持，则回退到并行调用
    """
    if not item_ids:
        return {}
    
    # 检查是否支持批量版本API（这里假设暂时不支持，使用并行调用）
    # 未来如果Autodesk API支持批量版本查询，可以在这里实现
    
    print(f"🔄 使用并行方式批量获取版本（{len(item_ids)} 个文件）")
    return get_versions_parallel(project_id, item_ids, headers)

# 延迟导入避免循环依赖
def get_custom_attributes_api():
    from api_modules.custom_attributes_api import custom_attributes_api
    return custom_attributes_api

def get_folder_custom_attribute_definitions(project_id, folder_id):
    """
    获取文件夹的自定义属性定义
    
    Args:
        project_id: 项目ID
        folder_id: 文件夹ID
        
    Returns:
        包含自定义属性定义的字典
    """
    try:
        print(f"📝 获取文件夹自定义属性定义: {folder_id}")
        
        # 调用自定义属性API
        custom_attrs_api = get_custom_attributes_api()
        result = custom_attrs_api.get_custom_attribute_definitions(project_id, folder_id)
        
        if 'error' in result:
            print(f"⚠️ 获取文件夹自定义属性定义失败: {result['error']}")
            return {}
        
        # 转换为简化格式
        definitions = {}
        for attr_def in result.get('results', []):
            attr_id = str(attr_def.get('id'))
            definitions[attr_id] = {
                'name': attr_def.get('name'),
                'displayName': attr_def.get('displayName'),
                'type': attr_def.get('type'),
                'required': attr_def.get('required', False),
                'description': attr_def.get('description', ''),
                'arrayValues': attr_def.get('arrayValues', [])
            }
        
        return {
            'customAttributeDefinitions': definitions,
            'hasCustomAttributeDefinitions': len(definitions) > 0,
            'totalDefinitions': len(definitions)
        }
        
    except Exception as e:
        print(f"⚠️ 获取文件夹自定义属性定义时出错: {str(e)}")
        return {}

def batch_get_files_custom_attributes(project_id, file_nodes):
    """
    批量获取文件的自定义属性
    
    Args:
        project_id: 项目ID
        file_nodes: 文件节点列表
        
    Returns:
        包含自定义属性的字典，key为版本ID
    """
    try:
        # 收集所有文件的版本ID
        version_ids = []
        for node in file_nodes:
            if hasattr(node, 'versions') and node.versions:
                # 获取最新版本的ID
                latest_version = node.versions[0]  # 假设第一个是最新版本
                version_id = latest_version.get('id')
                if version_id:
                    version_ids.append(version_id)
        
        if not version_ids:
            print("📝 没有找到文件版本ID，跳过自定义属性获取")
            return {}
        
        print(f"📝 批量获取 {len(version_ids)} 个文件的自定义属性")
        print(f"🔍 DEBUG: version_ids = {version_ids[:3]}..." if len(version_ids) > 3 else f"🔍 DEBUG: version_ids = {version_ids}")
        
        # 调用自定义属性API
        custom_attrs_api = get_custom_attributes_api()
        print(f"🔍 DEBUG: custom_attrs_api = {custom_attrs_api}")
        
        result = custom_attrs_api.get_file_custom_attributes(project_id, version_ids)
        print(f"🔍 DEBUG: API result = {result}")
        
        if 'error' in result:
            print(f"⚠️ 获取自定义属性失败: {result['error']}")
            return {}
        
        results_data = result.get('results', {})
        print(f"🔍 DEBUG: results_data keys = {list(results_data.keys())}")
        return results_data
        
    except Exception as e:
        print(f"⚠️ 批量获取自定义属性时出错: {str(e)}")
        return {}


class FileTreeNode:
    """文件树节点类，用于构建完整的文件夹结构"""
    def __init__(self, item_id, name, item_type, parent_id=None):
        self.id = item_id
        self.name = name
        self.type = item_type  # 'folder' or 'file'
        self.parent_id = parent_id
        self.children = []
        self.attributes = {}
        self.permissions = {}
        self.versions = []
    
    def to_dict(self, compact=False):
        """转换为字典格式
        
        Args:
            compact: 是否返回压缩格式（只包含必要字段）
        """
        if compact:
            # 压缩格式：只返回必要字段
            result = {
                'id': self.id,
                'name': self.name,
                'type': self.type,
                'children': [child.to_dict(compact=True) for child in self.children]
            }
            
            # 只包含关键属性
            if self.attributes:
                compact_attrs = {}
                
                # 通用属性（文件夹和文件都需要）
                # 用户信息
                if 'createUserId' in self.attributes:
                    compact_attrs['createUserId'] = self.attributes['createUserId']
                if 'createUserName' in self.attributes:
                    compact_attrs['createUserName'] = self.attributes['createUserName']
                if 'lastModifiedUserId' in self.attributes:
                    compact_attrs['lastModifiedUserId'] = self.attributes['lastModifiedUserId']
                if 'lastModifiedUserName' in self.attributes:
                    compact_attrs['lastModifiedUserName'] = self.attributes['lastModifiedUserName']
                
                # 时间信息
                if 'createTime' in self.attributes:
                    compact_attrs['createTime'] = self.attributes['createTime']
                if 'lastModifiedTime' in self.attributes:
                    compact_attrs['lastModifiedTime'] = self.attributes['lastModifiedTime']
                if 'lastModifiedTimeRollup' in self.attributes:
                    compact_attrs['lastModifiedTimeRollup'] = self.attributes['lastModifiedTimeRollup']
                
                # 文件夹特有属性
                if self.type == 'folder':
                    if 'objectCount' in self.attributes:
                        compact_attrs['objectCount'] = self.attributes['objectCount']
                    if 'path' in self.attributes:
                        compact_attrs['path'] = self.attributes['path']
                # 文件特有属性
                else:
                    if 'size' in self.attributes:
                        compact_attrs['size'] = self.attributes['size']
                    if 'extension' in self.attributes:
                        compact_attrs['extension'] = self.attributes['extension']
                    if 'fileSize' in self.attributes:
                        compact_attrs['fileSize'] = self.attributes['fileSize']
                    if 'storageSize' in self.attributes:
                        compact_attrs['storageSize'] = self.attributes['storageSize']
                    if 'mimeType' in self.attributes:
                        compact_attrs['mimeType'] = self.attributes['mimeType']
                    if 'versionNumber' in self.attributes:
                        compact_attrs['versionNumber'] = self.attributes['versionNumber']
                    # 文件保留信息
                    if 'reserved' in self.attributes:
                        compact_attrs['reserved'] = self.attributes['reserved']
                    if 'reservedTime' in self.attributes:
                        compact_attrs['reservedTime'] = self.attributes['reservedTime']
                    if 'reservedUserId' in self.attributes:
                        compact_attrs['reservedUserId'] = self.attributes['reservedUserId']
                    if 'reservedUserName' in self.attributes:
                        compact_attrs['reservedUserName'] = self.attributes['reservedUserName']
                
                # 通用状态属性
                if 'hidden' in self.attributes:
                    compact_attrs['hidden'] = self.attributes['hidden']
                
                if compact_attrs:
                    result['attributes'] = compact_attrs
            
            # 权限信息简化
            if self.permissions and self.permissions.get('status') == 'success':
                perm_data = self.permissions.get('data', {})
                if 'summary' in perm_data:
                    result['permissions'] = {
                        'status': 'success',
                        'summary': perm_data['summary']
                    }
            
            # 文件版本信息简化（只保留最新版本的关键信息）
            if self.versions and len(self.versions) > 0:
                latest = self.versions[0]
                result['latestVersion'] = {
                    'id': latest.get('id'),
                    'versionNumber': latest.get('versionNumber'),
                    'fileSize': latest.get('attributes', {}).get('fileSize') or latest.get('attributes', {}).get('storageSize'),
                    'lastModifiedTime': latest.get('attributes', {}).get('lastModifiedTime')
                }
            
            return result
        else:
            # 完整格式
            result = {
                'id': self.id,
                'name': self.name,
                'type': self.type,
                'parent_id': self.parent_id,
                'children': [child.to_dict() for child in self.children],
                'attributes': self.attributes,
                'permissions': self.permissions,
                'versions': self.versions
            }
            
            return result


def get_project_top_folders(project_id, headers):
    """获取项目的顶级文件夹"""
    try:
        # 首先尝试获取项目的Hub ID
        hub_id = None
        
        try:
            hubs_resp = requests.get(f"{config.AUTODESK_API_BASE}/project/v1/hubs", headers=headers)
            if hubs_resp.status_code == 200:
                hubs_data = hubs_resp.json()
                # 查找包含该项目的Hub
                for hub in hubs_data.get('data', []):
                    hub_id = hub.get('id')
                    break
        except Exception as e:
            print(f"Hub API调用失败: {e}")
        
        # 如果无法通过API获取Hub，尝试使用企业账户映射
        if not hub_id:
            print("尝试使用企业账户映射获取Hub ID")
            enterprise_hub_id, _, _ = utils.get_enterprise_hub_info()
            if enterprise_hub_id:
                hub_id = enterprise_hub_id
                print(f"使用企业Hub ID: {hub_id}")
        
        if not hub_id:
            raise Exception("Valid Hub ID not found")
        
        # 获取顶级文件夹 (带重试机制)
        top_folders_url = f"{config.AUTODESK_API_BASE}/project/v1/hubs/{hub_id}/projects/{project_id}/topFolders"
        print(f"🔍 获取顶级文件夹: {top_folders_url}")
        
        # 重试机制
        max_retries = 3
        retry_delay = 2  # 秒
        
        for attempt in range(max_retries):
            try:
                response = requests.get(top_folders_url, headers=headers, timeout=(10, 30))
                
                if response.status_code == 200:
                    print(f"✅ 获取顶级文件夹成功 (尝试 {attempt + 1}/{max_retries})")
                    return response.json()
                elif response.status_code == 503:
                    print(f"⚠️ 服务暂时不可用 (尝试 {attempt + 1}/{max_retries}): {response.status_code}")
                    if attempt < max_retries - 1:
                        print(f"   等待 {retry_delay} 秒后重试...")
                        time.sleep(retry_delay)
                        retry_delay *= 2  # 指数退避
                        continue
                else:
                    print(f"❌ 获取顶级文件夹失败: {response.status_code} - {response.text}")
                    break
                    
            except Exception as e:
                print(f"⚠️ 请求异常 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    print(f"   等待 {retry_delay} 秒后重试...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                else:
                    break
        
        print(f"❌ 所有重试都失败，返回空数据")
        return {"data": []}
            
    except Exception as e:
        print(f"❌ 获取顶级文件夹时出错: {str(e)}")
        return {"data": []}


def get_folder_contents(project_id, folder_id, headers, max_retries=3):
    """获取文件夹内容，支持重试机制"""
    for attempt in range(max_retries):
        try:
            # 使用正确的 Data Management API 端点
            contents_url = f"{config.AUTODESK_API_BASE}/data/v1/projects/{project_id}/folders/{folder_id}/contents"
            print(f"🔍 获取文件夹内容 (尝试 {attempt + 1}/{max_retries}): {folder_id}")
            
            response = requests.get(contents_url, headers=headers, timeout=(10, 30))
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # Rate limit
                wait_time = 2 ** attempt  # 指数退避
                print(f"⏳ API 限流，等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
                continue
            else:
                print(f"❌ 获取文件夹内容失败: {response.status_code} - {response.text}")
                return {"data": []}
                
        except requests.exceptions.Timeout:
            print(f"⏰ 请求超时 (尝试 {attempt + 1}/{max_retries})")
            if attempt < max_retries - 1:
                time.sleep(1)
                continue
        except Exception as e:
            print(f"❌ 获取文件夹内容时出错: {str(e)}")
            break
    
    return {"data": []}


def get_item_versions(project_id, item_id, headers):
    """获取文件的版本信息"""
    try:
        # 使用正确的 Data Management API 端点
        versions_url = f"{config.AUTODESK_API_BASE}/data/v1/projects/{project_id}/items/{item_id}/versions"
        response = requests.get(versions_url, headers=headers, timeout=(5, 15))
        
        if response.status_code == 200:
            return response.json().get('data', [])
        else:
            print(f"⚠️ 获取版本信息失败: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"⚠️ 获取版本信息时出错: {str(e)}")
        return []


def build_file_tree_recursive(project_id, folder_id, headers, parent_node=None, max_depth=10, current_depth=0, target_folder_ids=None, folder_path_mapping=None, current_path=""):
    """递归构建完整的文件树结构（支持分支跳过优化）"""
    if current_depth >= max_depth:
        print(f"⚠️ 达到最大递归深度 {max_depth}，停止遍历")
        return []
    
    print(f"📁 遍历文件夹 (深度 {current_depth}): {folder_id}")
    
    # 获取文件夹内容
    contents_data = get_folder_contents(project_id, folder_id, headers)
    nodes = []
    
    for item in contents_data.get('data', []):
        item_id = item.get('id')
        item_type = item.get('type')
        attributes = item.get('attributes', {})
        item_name = attributes.get('displayName', attributes.get('name', 'Unknown'))
        
        # 构建当前项目的路径
        if current_path and current_path != "Project Files":
            item_path = f"{current_path}/{item_name}"
        else:
            item_path = item_name
        
        # 如果是文件夹且启用了目标文件夹过滤，检查是否应该跳过
        if item_type == 'folders' and target_folder_ids and folder_path_mapping:
            from .file_sync_optimized import should_skip_folder_branch_optimized
            should_skip = should_skip_folder_branch_optimized(item_id, item_name, item_path, target_folder_ids, folder_path_mapping)
            if should_skip:
                print(f"   ⏭️ 跳过不相关分支: {item_name} (路径: {item_path})")
                continue
            else:
                print(f"   ✅ 目标相关分支，继续遍历: {item_name}")
        
        # 创建节点
        node = FileTreeNode(
            item_id=item_id,
            name=item_name,
            item_type='folder' if item_type == 'folders' else 'file',
            parent_id=folder_id
        )
        
        # 清理用户信息
        raw_create_user_id = attributes.get('createUserId')
        raw_create_user_name = attributes.get('createUserName')
        raw_modified_user_id = attributes.get('lastModifiedUserId')
        raw_modified_user_name = attributes.get('lastModifiedUserName')
        
        create_user_id, create_user_name = sanitize_user_info(
            raw_create_user_id, 
            raw_create_user_name
        )
        modified_user_id, modified_user_name = sanitize_user_info(
            raw_modified_user_id, 
            raw_modified_user_name
        )
        
        # 添加属性信息，处理可能为空的用户信息
        node.attributes = {
            'displayName': item_name,
            'createTime': attributes.get('createTime'),
            'createUserId': create_user_id,
            'createUserName': create_user_name,
            'lastModifiedTime': attributes.get('lastModifiedTime'),
            'lastModifiedUserId': modified_user_id,
            'lastModifiedUserName': modified_user_name,
            'lastModifiedTimeRollup': attributes.get('lastModifiedTimeRollup'),  # 新增：包括子文件/版本的最后修改时间
            'objectCount': attributes.get('objectCount', 0),
            'size': attributes.get('size', 0),
            'path': attributes.get('path'),  # 新增：文件夹路径
            'hidden': attributes.get('hidden', False),  # 新增：是否隐藏
            'extension': attributes.get('extension', {}),
            # 添加调试信息，记录原始API数据
            '_debug_api_attributes': {
                'createUserId_raw': attributes.get('createUserId'),
                'createUserName_raw': attributes.get('createUserName'),
                'lastModifiedUserId_raw': attributes.get('lastModifiedUserId'),
                'lastModifiedUserName_raw': attributes.get('lastModifiedUserName')
            } if hasattr(config, 'DEBUG') and config.DEBUG else {}
        }
        
        # 如果是文件，添加文件特有的属性
        if item_type != 'folders':
            node.attributes.update({
                'reserved': attributes.get('reserved', False),  # 是否被保留
                'reservedTime': attributes.get('reservedTime'),  # 保留时间
                'reservedUserId': attributes.get('reservedUserId'),  # 保留者ID
                'reservedUserName': attributes.get('reservedUserName')  # 保留者名称
            })
        
        # 添加基本权限信息（从属性中提取）
        node.permissions = {
            'canRead': True,  # 如果能获取到就说明有读权限
            'canWrite': False,  # 需要进一步检查
            'canDelete': False,  # 需要进一步检查
            'createUserId': create_user_id,
            'lastModifiedUserId': modified_user_id
        }
        
        if item_type == 'folders':
            # 递归处理子文件夹
            print(f"📂 处理子文件夹: {item_name}")
            child_nodes = build_file_tree_recursive(
                project_id, item_id, headers, node, max_depth, current_depth + 1,
                target_folder_ids, folder_path_mapping, item_path
            )
            node.children = child_nodes
        else:
            # 处理文件，获取版本信息
            print(f"📄 处理文件: {item_name}")
            versions = get_item_versions(project_id, item_id, headers)
            node.versions = versions
            
            # 从版本信息中提取更多属性
            if versions:
                latest_version = versions[0]  # 通常第一个是最新版本
                version_attributes = latest_version.get('attributes', {})
                # 获取文件大小，尝试多个字段
                file_size = (version_attributes.get('storageSize', 0) or 
                           version_attributes.get('fileSize', 0) or
                           latest_version.get('storageSize', 0) or
                           latest_version.get('fileSize', 0))
                
                node.attributes.update({
                    'versionNumber': version_attributes.get('versionNumber'),
                    'mimeType': version_attributes.get('mimeType'),
                    'fileSize': file_size,
                    'storageSize': file_size,  # 添加storageSize字段
                    'downloadUrl': version_attributes.get('downloadUrl')
                })
                
                # 调试输出
                if file_size == 0:
                    print(f"⚠️ 文件 {item_name} 版本大小为0，版本属性: {version_attributes}")
                    print(f"   完整版本信息: {latest_version}")
        
        nodes.append(node)
        
        # 添加小延迟避免API限流
        time.sleep(0.1)
    
    return nodes


@file_sync_bp.route('/api/file-sync/project/<project_id>/tree')
def get_project_file_tree(project_id):
    """获取项目的完整文件树结构"""
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
        print(f"🚀 开始同步项目文件树: {project_id}")
        start_time = time.time()
        
        # 获取最大深度参数
        max_depth = request.args.get('maxDepth', 10, type=int)
        include_versions = request.args.get('includeVersions', 'true').lower() == 'true'
        # 接收目标文件夹ID参数，支持多种格式
        target_folder_ids = []
        # 尝试不同的参数格式
        if request.args.getlist('target_folder_ids[]'):
            target_folder_ids = request.args.getlist('target_folder_ids[]')
        elif request.args.getlist('target_folder_ids'):
            target_folder_ids = request.args.getlist('target_folder_ids')
        else:
            # 尝试索引格式 target_folder_ids[0], target_folder_ids[1], ...
            i = 0
            while True:
                param_key = f'target_folder_ids[{i}]'
                if param_key in request.args:
                    target_folder_ids.append(request.args.get(param_key))
                    i += 1
                else:
                    break
        optimize_traversal = request.args.get('optimize_traversal', 'false').lower() == 'true'
        
        print(f"🎯 文件树构建参数: max_depth={max_depth}, target_folder_ids={target_folder_ids}, optimize_traversal={optimize_traversal}")
        
        # 获取顶级文件夹
        top_folders_data = get_project_top_folders(project_id, headers)
        
        if not top_folders_data.get('data'):
            return jsonify({
                "error": "Unable to get project top-level folders",
                "status": "error",
                "project_id": project_id
            }), 404
        
        # 构建完整的文件树
        project_tree = {
            'project_id': project_id,
            'sync_time': datetime.now().isoformat(),
            'top_folders': [],
            'statistics': {
                'total_folders': 0,
                'total_files': 0,
                'total_size': 0,
                'sync_duration_seconds': 0
            }
        }
        
        print(f"🔍 开始处理顶级文件夹，优化参数: optimize_traversal={optimize_traversal}, target_folder_ids={target_folder_ids}")
        
        total_folders = 0
        total_files = 0
        total_size = 0
        
        # 处理每个顶级文件夹
        for top_folder in top_folders_data.get('data', []):
            folder_id = top_folder.get('id')
            folder_attributes = top_folder.get('attributes', {})
            folder_name = folder_attributes.get('displayName', folder_attributes.get('name', 'Unknown'))
            
            print(f"📁 处理顶级文件夹: {folder_name}")
            
            # 创建顶级文件夹节点
            top_folder_node = FileTreeNode(
                item_id=folder_id,
                name=folder_name,
                item_type='folder',
                parent_id=None
            )
            
            top_folder_node.attributes = {
                'displayName': folder_name,
                'createTime': folder_attributes.get('createTime'),
                'createUserId': folder_attributes.get('createUserId'),
                'createUserName': folder_attributes.get('createUserName'),
                'lastModifiedTime': folder_attributes.get('lastModifiedTime'),
                'objectCount': folder_attributes.get('objectCount', 0)
            }
            
            # 递归构建子树
            print(f"🔧 调试: 到达递归构建子树部分")
            print(f"🔍 变量检查: optimize_traversal类型={type(optimize_traversal)}, 值={optimize_traversal}")
            print(f"🔍 变量检查: target_folder_ids类型={type(target_folder_ids)}, 值={target_folder_ids}")
            print(f"🔍 优化条件检查: optimize_traversal={optimize_traversal}, target_folder_ids={target_folder_ids}")
            
            # 初始化文件夹路径映射（在条件分支外初始化以避免变量作用域问题）
            folder_path_mapping = {}
            
            if optimize_traversal and target_folder_ids:
                print(f"✅ 进入优化分支")
                # 获取文件夹路径映射以支持智能分支跳过
                try:
                    folders_url = f"http://localhost:{config.PORT}/api/download-config/project/{project_id}/folders"
                    folders_response = requests.get(folders_url, params={'maxDepth': 10}, timeout=30)
                    if folders_response.status_code == 200:
                        folders_data = folders_response.json()
                        if folders_data.get('status') == 'success':
                            for folder in folders_data.get('data', {}).get('folders', []):
                                folder_id = folder.get('id')
                                if folder_id:
                                    folder_path_mapping[folder_id] = {
                                        'name': folder.get('name', ''),
                                        'path': folder.get('path', '')
                                    }
                            print(f"🗂️ 获取文件夹映射: {len(folder_path_mapping)} 个文件夹")
                            # 调试：显示目标文件夹的映射信息
                            for target_id in target_folder_ids:
                                if target_id in folder_path_mapping:
                                    target_info = folder_path_mapping[target_id]
                                    print(f"   🎯 目标文件夹 {target_id}: 名称='{target_info.get('name')}', 路径='{target_info.get('path')}'")
                                else:
                                    print(f"   ❌ 目标文件夹 {target_id} 不在映射中")
                except Exception as e:
                    print(f"⚠️ 获取文件夹映射失败: {str(e)}")
                    folder_path_mapping = {}
                
                from .file_sync_optimized import build_file_tree_recursive_optimized
                child_nodes = build_file_tree_recursive_optimized(
                    project_id, folder_id, headers, top_folder_node, max_depth, 0,
                    target_folder_ids, folder_path_mapping, "Project Files"
                )
            else:
                print(f"❌ 未进入优化分支，使用原始遍历")
                child_nodes = build_file_tree_recursive(
                    project_id, folder_id, headers, top_folder_node, max_depth, 0,
                    target_folder_ids, folder_path_mapping, "Project Files"
                )
            top_folder_node.children = child_nodes
            
            # 统计信息
            def count_nodes(nodes):
                folders = 0
                files = 0
                size = 0
                for node in nodes:
                    if node.type == 'folder':
                        folders += 1
                        f, fi, s = count_nodes(node.children)
                        folders += f
                        files += fi
                        size += s
                    else:
                        files += 1
                        # 获取文件大小，优先使用版本信息中的大小
                        file_size = 0
                        if node.versions:
                            latest_version = node.versions[0]
                            file_size = latest_version.get('fileSize', 0) or latest_version.get('storageSize', 0)
                        if file_size == 0:
                            file_size = node.attributes.get('size', 0) or node.attributes.get('storageSize', 0)
                        size += file_size
                return folders, files, size
            
            f, fi, s = count_nodes(child_nodes)
            total_folders += f + 1  # +1 for the top folder itself
            total_files += fi
            total_size += s
            
            project_tree['top_folders'].append(top_folder_node.to_dict())
        
        # 更新统计信息
        end_time = time.time()
        project_tree['statistics'] = {
            'total_folders': total_folders,
            'total_files': total_files,
            'total_size': total_size,
            'sync_duration_seconds': round(end_time - start_time, 2)
        }
        
        print(f"✅ 文件树同步完成:")
        print(f"   📁 文件夹: {total_folders}")
        print(f"   📄 文件: {total_files}")
        print(f"   💾 总大小: {total_size} bytes")
        print(f"   ⏱️ 耗时: {project_tree['statistics']['sync_duration_seconds']} 秒")
        
        return jsonify({
            "status": "success",
            "message": f"成功同步项目文件树，共 {total_folders} 个文件夹，{total_files} 个文件",
            "data": project_tree
        })
        
    except Exception as e:
        print(f"❌ 同步文件树时出错: {str(e)}")
        return jsonify({
            "error": f"同步文件树失败: {str(e)}",
            "status": "error",
            "project_id": project_id
        }), 500


@file_sync_bp.route('/api/file-sync/project/<project_id>/folder/<folder_id>')
def get_folder_tree(project_id, folder_id):
    """获取指定文件夹的子树结构"""
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
        max_depth = request.args.get('maxDepth', 2, type=int)
        
        print(f"🔍 获取文件夹子树: {folder_id}")
        
        # 构建子树
        child_nodes = build_file_tree_recursive(
            project_id, folder_id, headers, None, max_depth, 0
        )
        
        # 统计信息
        def count_nodes(nodes):
            folders = 0
            files = 0
            for node in nodes:
                if node.type == 'folder':
                    folders += 1
                    f, fi = count_nodes(node.children)
                    folders += f
                    files += fi
                else:
                    files += 1
            return folders, files
        
        total_folders, total_files = count_nodes(child_nodes)
        
        return jsonify({
            "status": "success",
            "folder_id": folder_id,
            "project_id": project_id,
            "children": [node.to_dict() for node in child_nodes],
            "statistics": {
                "total_folders": total_folders,
                "total_files": total_files
            }
        })
        
    except Exception as e:
        print(f"❌ 获取文件夹子树时出错: {str(e)}")
        return jsonify({
            "error": f"获取文件夹子树失败: {str(e)}",
            "status": "error"
        }), 500


@file_sync_bp.route('/api/file-sync/project/<project_id>/statistics')
def get_project_statistics(project_id):
    """获取项目的文件统计信息（快速版本，不构建完整树）"""
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
        print(f"📊 获取项目统计信息: {project_id}")
        
        # 获取顶级文件夹
        top_folders_data = get_project_top_folders(project_id, headers)
        
        statistics = {
            'project_id': project_id,
            'scan_time': datetime.now().isoformat(),
            'top_folders_count': len(top_folders_data.get('data', [])),
            'top_folders': []
        }
        
        # 获取每个顶级文件夹的basicInfo
        for top_folder in top_folders_data.get('data', []):
            folder_id = top_folder.get('id')
            folder_attributes = top_folder.get('attributes', {})
            folder_name = folder_attributes.get('displayName', folder_attributes.get('name', 'Unknown'))
            
            folder_info = {
                'id': folder_id,
                'name': folder_name,
                'object_count': folder_attributes.get('objectCount', 0),
                'create_time': folder_attributes.get('createTime'),
                'last_modified_time': folder_attributes.get('lastModifiedTime')
            }
            
            statistics['top_folders'].append(folder_info)
        
        return jsonify({
            "status": "success",
            "data": statistics
        })
        
    except Exception as e:
        print(f"❌ 获取项目统计信息时出错: {str(e)}")
        return jsonify({
            "error": f"获取项目统计信息失败: {str(e)}",
            "status": "error"
        }), 500


@file_sync_bp.route('/api/file-sync/download/<project_id>/<item_id>')
def get_download_url(project_id, item_id):
    """获取文件的下载链接"""
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
        # 获取文件版本信息
        versions = get_item_versions(project_id, item_id, headers)
        
        if not versions:
            return jsonify({
                "error": "File version information not found",
                "status": "error"
            }), 404
        
        # 获取最新版本的下载信息
        latest_version = versions[0]
        version_id = latest_version.get('id')
        
        # 使用新的下载方法 - Model Derivative API
        # 1. 获取derivative URN
        derivatives_relationship = latest_version.get('relationships', {}).get('derivatives', {})
        if not derivatives_relationship:
            return jsonify({
                "error": "文件没有可用的derivatives",
                "status": "error"
            }), 404
        
        derivative_urn = derivatives_relationship.get('data', {}).get('id')
        if not derivative_urn:
            return jsonify({
                "error": "无法获取derivative URN",
                "status": "error"
            }), 404
        
        # 2. 首先尝试直接获取原始文件（对所有文件类型）
        print(f"🔍 按照官方文档获取下载信息...")
        
        # 方式1: 优先使用storage关系获取原始文件（官方推荐方式）
        print("🔄 尝试从storage关系获取原始文件...")
        storage_relationship = latest_version.get('relationships', {}).get('storage')
        if storage_relationship:
            storage_data = storage_relationship.get('data', {})
            storage_id = storage_data.get('id')  # 例如: urn:adsk.objects:os.object:wip.dm.prod/977d69b1-43e7-40fa-8ece-6ec4602892f3.rvt
            storage_link = storage_relationship.get('meta', {}).get('link', {}).get('href')
            
            print(f"   Storage ID: {storage_id}")
            print(f"   Storage Link: {storage_link}")
            
            if storage_id and storage_id.startswith('urn:adsk.objects:os.object:'):
                # 解析storage ID获取bucket和object信息
                # 格式: urn:adsk.objects:os.object:bucket_key/object_key
                storage_path = storage_id.replace('urn:adsk.objects:os.object:', '')
                if '/' in storage_path:
                    bucket_key, object_key = storage_path.split('/', 1)
                    download_info = {
                        "method": "oss_signed_url",
                        "bucket_key": bucket_key,
                        "object_key": object_key,
                        "storage_id": storage_id,
                        "version_id": version_id
                    }
                    print(f"✅ 找到OSS存储信息: bucket={bucket_key}, object={object_key}")
                    
                    return jsonify({
                        "status": "success",
                        "download_info": download_info,
                        "version_info": latest_version,
                        "message": "找到原始文件存储位置，可直接下载"
                    })
                else:
                    print(f"   ⚠️ 无法解析storage路径: {storage_path}")
            elif storage_link:
                # 如果有直接的storage链接，使用它
                download_info = {
                    "method": "direct_storage_link",
                    "download_url": storage_link,
                    "version_id": version_id
                }
                print(f"✅ 找到直接存储链接: {storage_link}")
                
                return jsonify({
                    "status": "success",
                    "download_info": download_info,
                    "version_info": latest_version,
                    "message": "找到直接存储链接，可直接下载"
                })
            else:
                print("   ⚠️ 无效的storage信息")
        else:
            print("   ⚠️ 没有找到storage关系")
        
        # 方式2: 回退到storageLocation属性
        print("🔄 尝试从storageLocation属性获取...")
        version_attributes = latest_version.get('attributes', {})
        storage_location = version_attributes.get('storageLocation')
        print(f"   Storage location: {storage_location}")
        
        if storage_location and storage_location.startswith('urn:adsk.objects:os.object:'):
            storage_path = storage_location.replace('urn:adsk.objects:os.object:', '')
            if '/' in storage_path:
                bucket_key, object_key = storage_path.split('/', 1)
                download_info = {
                    "method": "oss_signed_url",
                    "bucket_key": bucket_key,
                    "object_key": object_key,
                    "storage_id": storage_location,
                    "version_id": version_id
                }
                print(f"✅ 从storageLocation找到OSS信息: bucket={bucket_key}, object={object_key}")
                
                return jsonify({
                    "status": "success",
                    "download_info": download_info,
                    "version_info": latest_version,
                    "message": "找到原始文件存储位置，可直接下载"
                })
            else:
                print(f"   ⚠️ 无法解析storageLocation: {storage_path}")
        else:
            print("   ⚠️ 没有找到有效的storageLocation")
        
        # 方式3: 对于PDF等需要derivatives的文件，尝试获取manifest
        print("🔄 尝试获取manifest信息（用于PDF等文件）...")
        manifest_url = f"{config.AUTODESK_API_BASE}/modelderivative/v2/designdata/{derivative_urn}/manifest"
        manifest_resp = requests.get(manifest_url, headers=headers)
        
        if manifest_resp.status_code != 200:
            print(f"   ⚠️ 获取manifest失败: {manifest_resp.status_code}")
            # 对于非PDF文件，这是正常的，返回错误信息
            return jsonify({
                "error": f"无法找到文件的下载方式。Storage关系和manifest都不可用。",
                "status": "error"
            }), 404
        
        manifest_data = manifest_resp.json()
        print("   ✅ 成功获取manifest信息")
        
        # 4. 如果还没找到，尝试从manifest中查找PDF等derivatives
        download_info = None
        
        # 方式3: 如果没有原始文件，查找完整PDF文件
        if not download_info:
            print("🔄 寻找完整PDF文件...")
            for derivative in manifest_data.get('derivatives', []):
                print(f"检查derivative: {derivative.get('outputType', 'unknown')}")
                
                # 检查是否有完整PDF输出
                if derivative.get('outputType') == 'pdf':
                    pdf_urn = derivative.get('urn')
                    if pdf_urn:
                        download_info = {
                            "method": "direct_pdf",
                            "derivative_urn": derivative_urn,
                            "pdf_urn": pdf_urn,
                            "download_base_url": f"{config.AUTODESK_API_BASE}/derivativeservice/v2/derivatives"
                        }
                        print(f"✅ 找到完整PDF输出: {pdf_urn}")
                        break
                
                # 也检查子级derivatives中的PDF
                for child in derivative.get('children', []):
                    if child.get('outputType') == 'pdf':
                        pdf_urn = child.get('urn')
                        if pdf_urn:
                            download_info = {
                                "method": "direct_pdf",
                                "derivative_urn": derivative_urn,
                                "pdf_urn": pdf_urn,
                                "download_base_url": f"{config.AUTODESK_API_BASE}/derivativeservice/v2/derivatives"
                            }
                            print(f"✅ 在子级中找到完整PDF输出: {pdf_urn}")
                            break
                    
                if download_info:
                    break
            
        # 方式4: 回退到PDF页面方式
        if not download_info:
            print("🔄 回退到PDF页面下载方式...")
            pdf_page_urns = []
            
            for derivative in manifest_data.get('derivatives', []):
                for child in derivative.get('children', []):
                    for subchild in child.get('children', []):
                        if subchild.get('role') == 'pdf-page':
                            pdf_page_urns.append(subchild.get('urn'))
            
            if pdf_page_urns:
                download_info = {
                    "method": "model_derivative",
                    "derivative_urn": derivative_urn,
                    "pdf_pages": pdf_page_urns,
                    "download_base_url": f"{config.AUTODESK_API_BASE}/derivativeservice/v2/derivatives"
                }
                print(f"✅ 找到 {len(pdf_page_urns)} 个PDF页面")
        
        if not download_info:
            return jsonify({
                "error": "No available download methods found",
                "status": "error"
            }), 404
        
        # 构建响应消息
        if download_info:
            if download_info.get('method') == 'oss_signed_url':
                message = "找到原始文件存储位置，可直接下载"
            elif download_info.get('method') == 'direct_storage_link':
                message = "找到直接存储链接，可直接下载"
            elif download_info.get('method') == 'direct_pdf':
                message = "找到完整PDF文件"
            elif download_info.get('method') == 'model_derivative':
                pdf_pages = download_info.get('pdf_pages', [])
                message = f"找到 {len(pdf_pages)} 个PDF页面可供下载"
            else:
                message = "Download method found"
        else:
            message = "No available download methods found"
        
        return jsonify({
            "status": "success",
            "download_info": download_info,
            "version_info": latest_version,
            "message": message
        })
            
    except Exception as e:
        print(f"❌ 获取下载链接时出错: {str(e)}")
        return jsonify({
            "error": f"获取下载链接失败: {str(e)}",
            "status": "error"
        }), 500


# ==================== 权限同步功能 ====================

def clean_project_id_for_permissions(project_id):
    """清理项目ID，移除'b.'前缀用于权限API"""
    return project_id.replace("b.", "") if project_id.startswith("b.") else project_id


def get_folder_permissions_from_beta_api(project_id, folder_id, headers):
    """
    从官方Beta API获取文件夹权限信息
    """
    try:
        # 清理项目ID
        clean_proj_id = clean_project_id_for_permissions(project_id)
        
        # 构建权限API URL
        permissions_url = f"{config.AUTODESK_API_BASE}/bim360/docs/v1/projects/{clean_proj_id}/folders/{folder_id}/permissions"
        
        print(f"🔍 获取文件夹权限: {permissions_url}")
        
        response = requests.get(permissions_url, headers=headers, timeout=(10, 30))
        
        if response.status_code == 200:
            permissions_data = response.json()
            
            # 解析权限数据
            parsed_permissions = parse_folder_permissions(permissions_data)
            
            return {
                "status": "success",
                "permissions": parsed_permissions,
                "raw_permissions": permissions_data,
                "api_url": permissions_url
            }
            
        elif response.status_code == 403:
            return {
                "status": "no_permission",
                "error": "权限不足，无法获取文件夹权限信息"
            }
            
        elif response.status_code == 404:
            return {
                "status": "not_found", 
                "error": "Project or folder does not exist"
            }
            
        else:
            return {
                "status": "api_error",
                "error": f"权限API调用失败: HTTP {response.status_code}",
                "details": response.text[:200]
            }
            
    except Exception as e:
        return {
            "status": "exception",
            "error": f"获取权限时出错: {str(e)}"
        }


def parse_folder_permissions(permissions_data):
    """
    解析文件夹权限数据
    """
    parsed = {
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
    
    # ACC权限级别映射
    permission_levels = {
        frozenset(["VIEW", "COLLABORATE"]): {"level": 1, "name": "View"},
        frozenset(["VIEW", "DOWNLOAD", "COLLABORATE"]): {"level": 2, "name": "View/Download"},
        frozenset(["VIEW", "DOWNLOAD", "COLLABORATE", "PUBLISH_MARKUP"]): {"level": 3, "name": "View/Download/Markup"},
        frozenset(["PUBLISH", "VIEW", "DOWNLOAD", "COLLABORATE", "PUBLISH_MARKUP"]): {"level": 4, "name": "View/Download/Markup/Upload"},
        frozenset(["PUBLISH", "VIEW", "DOWNLOAD", "COLLABORATE", "PUBLISH_MARKUP", "EDIT"]): {"level": 5, "name": "Full Edit"},
        frozenset(["PUBLISH", "VIEW", "DOWNLOAD", "COLLABORATE", "PUBLISH_MARKUP", "EDIT", "CONTROL"]): {"level": 6, "name": "Full Control"}
    }
    
    for permission in permissions_data:
        subject_type = permission.get("subjectType", "").upper()
        
        # 合并直接权限和继承权限
        direct_actions = permission.get("actions", [])
        inherit_actions = permission.get("inheritActions", [])
        all_actions = list(set(direct_actions + inherit_actions))
        
        # 确定权限级别
        actions_set = frozenset(all_actions)
        permission_info = {"level": 0, "name": "No Permission"}
        
        # 从高到低检查权限级别
        for level_actions, level_info in sorted(permission_levels.items(), key=lambda x: x[1]["level"], reverse=True):
            if level_actions.issubset(actions_set):
                permission_info = level_info
                break
        
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
            "permission_level": permission_info["level"],
            "permission_name": permission_info["name"],
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
            parsed["users"].append(permission_record)
            parsed["summary"]["users_count"] += 1
        elif subject_type == "ROLE":
            parsed["roles"].append(permission_record)
            parsed["summary"]["roles_count"] += 1
        elif subject_type == "COMPANY":
            parsed["companies"].append(permission_record)
            parsed["summary"]["companies_count"] += 1
    
    return parsed


def build_file_tree_with_permissions(project_id, folder_id, headers, parent_node=None, max_depth=10, current_depth=0, include_permissions=True, include_custom_attributes=True):
    """
    构建包含权限信息的文件树
    """
    if current_depth >= max_depth:
        print(f"⚠️ 达到最大递归深度 {max_depth}，停止遍历")
        return []
    
    print(f"📁 遍历文件夹 (深度 {current_depth}): {folder_id}")
    
    # 获取文件夹内容
    contents_data = get_folder_contents(project_id, folder_id, headers)
    nodes = []
    
    for item in contents_data.get('data', []):
        item_id = item.get('id')
        item_type = item.get('type')
        attributes = item.get('attributes', {})
        item_name = attributes.get('displayName', attributes.get('name', 'Unknown'))
        
        # 创建节点
        node = FileTreeNode(
            item_id=item_id,
            name=item_name,
            item_type='folder' if item_type == 'folders' else 'file',
            parent_id=folder_id
        )
        
        # 添加基本属性信息
        node.attributes = {
            'displayName': item_name,
            'createTime': attributes.get('createTime'),
            'createUserId': attributes.get('createUserId'),
            'createUserName': attributes.get('createUserName'),
            'lastModifiedTime': attributes.get('lastModifiedTime'),
            'lastModifiedUserId': attributes.get('lastModifiedUserId'),
            'lastModifiedUserName': attributes.get('lastModifiedUserName'),
            'lastModifiedTimeRollup': attributes.get('lastModifiedTimeRollup'),  # 新增：包括子文件/版本的最后修改时间
            'objectCount': attributes.get('objectCount', 0),
            'size': attributes.get('size', 0),
            'path': attributes.get('path'),  # 新增：文件夹路径
            'hidden': attributes.get('hidden', False),  # 新增：是否隐藏
            'extension': attributes.get('extension', {})
        }
        
        # 如果是文件，添加文件特有的属性
        if item_type != 'folders':
            node.attributes.update({
                'reserved': attributes.get('reserved', False),  # 是否被保留
                'reservedTime': attributes.get('reservedTime'),  # 保留时间
                'reservedUserId': attributes.get('reservedUserId'),  # 保留者ID
                'reservedUserName': attributes.get('reservedUserName')  # 保留者名称
            })
        
        # 获取权限信息（仅对文件夹）
        if item_type == 'folders' and include_permissions:
            print(f"🔐 获取文件夹权限: {item_name}")
            permissions_result = get_folder_permissions_from_beta_api(project_id, item_id, headers)
            
            if permissions_result["status"] == "success":
                node.permissions = {
                    "status": "success",
                    "data": permissions_result["permissions"],
                    "api_source": "beta_permissions_api"
                }
                print(f"✅ 成功获取权限: {permissions_result['permissions']['summary']['total_subjects']} 个主体")
            else:
                node.permissions = {
                    "status": permissions_result["status"],
                    "error": permissions_result.get("error"),
                    "api_source": "beta_permissions_api"
                }
                print(f"⚠️ 权限获取失败: {permissions_result.get('error')}")
            
            # 递归处理子文件夹
            child_nodes = build_file_tree_with_permissions(
                project_id, item_id, headers, node, max_depth, current_depth + 1, include_permissions, include_custom_attributes
            )
            node.children = child_nodes
            
        elif item_type != 'folders':
            # 处理文件，获取版本信息
            print(f"📄 处理文件: {item_name}")
            versions = get_item_versions(project_id, item_id, headers)
            node.versions = versions
            
            # 从版本信息中提取更多属性
            if versions:
                latest_version = versions[0]
                version_attributes = latest_version.get('attributes', {})
                file_size = (version_attributes.get('storageSize', 0) or 
                           version_attributes.get('fileSize', 0) or
                           latest_version.get('storageSize', 0) or
                           latest_version.get('fileSize', 0))
                
                node.attributes.update({
                    'versionNumber': version_attributes.get('versionNumber'),
                    'mimeType': version_attributes.get('mimeType'),
                    'fileSize': file_size,
                    'storageSize': file_size,
                    'downloadUrl': version_attributes.get('downloadUrl')
                })
        
        nodes.append(node)
        
        # 添加延迟避免API限流
        time.sleep(0.2)
    
    # 批量获取文件的自定义属性
    file_nodes = [node for node in nodes if node.type == 'file']
    if file_nodes and include_custom_attributes:
        print(f"📝 开始批量获取 {len(file_nodes)} 个文件的自定义属性")
        custom_attributes_data = batch_get_files_custom_attributes(project_id, file_nodes)
        
        # 将自定义属性添加到文件节点
        for node in file_nodes:
            if hasattr(node, 'versions') and node.versions:
                latest_version = node.versions[0]
                version_id = latest_version.get('id')
                
                if version_id and version_id in custom_attributes_data:
                    custom_attrs = custom_attributes_data[version_id]
                    node.attributes['customAttributes'] = custom_attrs.get('customAttributes', {})
                    node.attributes['hasCustomAttributes'] = custom_attrs.get('hasCustomAttributes', False)
                    print(f"✅ 文件 {node.name} 已添加自定义属性: {len(custom_attrs.get('customAttributes', {}))} 个")
                else:
                    node.attributes['customAttributes'] = {}
                    node.attributes['hasCustomAttributes'] = False
                    print(f"📝 文件 {node.name} 无自定义属性数据")
            else:
                # 确保所有文件节点都有这些字段
                node.attributes['customAttributes'] = {}
                node.attributes['hasCustomAttributes'] = False
    
    # 获取文件夹的自定义属性定义
    folder_nodes = [node for node in nodes if node.type == 'folder']
    if folder_nodes and include_custom_attributes:
        print(f"📝 开始获取 {len(folder_nodes)} 个文件夹的自定义属性定义")
        
        for node in folder_nodes:
            folder_custom_attrs = get_folder_custom_attribute_definitions(project_id, node.id)
            
            if folder_custom_attrs and folder_custom_attrs.get('customAttributeDefinitions'):
                node.attributes['customAttributeDefinitions'] = folder_custom_attrs.get('customAttributeDefinitions', {})
                node.attributes['hasCustomAttributeDefinitions'] = folder_custom_attrs.get('hasCustomAttributeDefinitions', False)
                node.attributes['totalCustomAttributeDefinitions'] = folder_custom_attrs.get('totalDefinitions', 0)
                print(f"✅ 文件夹 {node.name} 已添加自定义属性定义 ({folder_custom_attrs.get('totalDefinitions', 0)} 个)")
            else:
                node.attributes['customAttributeDefinitions'] = {}
                node.attributes['hasCustomAttributeDefinitions'] = False
                node.attributes['totalCustomAttributeDefinitions'] = 0
                print(f"📝 文件夹 {node.name} 无自定义属性定义")
    else:
        # 确保所有文件夹节点都有这些字段
        for node in folder_nodes:
            node.attributes['customAttributeDefinitions'] = {}
            node.attributes['hasCustomAttributeDefinitions'] = False
            node.attributes['totalCustomAttributeDefinitions'] = 0
    
    return nodes


def build_file_tree_with_permissions_parallel(project_id, folder_id, headers, parent_node=None, max_depth=10, current_depth=0, include_permissions=True, include_custom_attributes=True):
    """
    构建包含权限信息的文件树（并行版本）
    """
    if current_depth >= max_depth:
        print(f"⚠️ 达到最大递归深度 {max_depth}，停止遍历")
        return []
    
    print(f"📁 遍历文件夹 (深度 {current_depth}): {folder_id}")
    
    # 获取文件夹内容
    contents_data = get_folder_contents(project_id, folder_id, headers)
    nodes = []
    
    # 分离文件夹和文件
    folder_items = []
    file_items = []
    
    for item in contents_data.get('data', []):
        item_type = item.get('type')
        if item_type == 'folders':
            folder_items.append(item)
        else:
            file_items.append(item)
    
    # 收集需要并行处理的ID
    folder_ids_for_permissions = []
    file_ids_for_versions = []
    
    # 处理文件夹
    for item in folder_items:
        item_id = item.get('id')
        attributes = item.get('attributes', {})
        item_name = attributes.get('displayName', attributes.get('name', 'Unknown'))
        
        # 创建节点
        node = FileTreeNode(
            item_id=item_id,
            name=item_name,
            item_type='folder',
            parent_id=folder_id
        )
        
        # 添加属性信息
        node.attributes = {
            'displayName': item_name,
            'createTime': attributes.get('createTime'),
            'createUserId': attributes.get('createUserId'),
            'createUserName': attributes.get('createUserName'),
            'lastModifiedTime': attributes.get('lastModifiedTime'),
            'lastModifiedUserId': attributes.get('lastModifiedUserId'),
            'lastModifiedUserName': attributes.get('lastModifiedUserName'),
            'lastModifiedTimeRollup': attributes.get('lastModifiedTimeRollup'),  # 新增：包括子文件/版本的最后修改时间
            'objectCount': attributes.get('objectCount', 0),
            'path': attributes.get('path'),  # 新增：文件夹路径
            'hidden': attributes.get('hidden', False)  # 新增：是否隐藏
        }
        
        nodes.append(node)
        
        # 收集需要获取权限的文件夹ID
        if include_permissions:
            folder_ids_for_permissions.append(item_id)
    
    # 处理文件
    for item in file_items:
        item_id = item.get('id')
        attributes = item.get('attributes', {})
        item_name = attributes.get('displayName', attributes.get('name', 'Unknown'))
        
        # 创建节点
        node = FileTreeNode(
            item_id=item_id,
            name=item_name,
            item_type='file',
            parent_id=folder_id
        )
        
        # 添加属性信息
        node.attributes = {
            'displayName': item_name,
            'createTime': attributes.get('createTime'),
            'createUserId': attributes.get('createUserId'),
            'createUserName': attributes.get('createUserName'),
            'lastModifiedTime': attributes.get('lastModifiedTime'),
            'lastModifiedUserId': attributes.get('lastModifiedUserId'),
            'lastModifiedUserName': attributes.get('lastModifiedUserName'),
            'lastModifiedTimeRollup': attributes.get('lastModifiedTimeRollup'),  # 新增：包括版本的最后修改时间
            'size': attributes.get('size', 0),
            'hidden': attributes.get('hidden', False),  # 新增：是否隐藏
            'reserved': attributes.get('reserved', False),  # 新增：是否被保留
            'reservedTime': attributes.get('reservedTime'),  # 新增：保留时间
            'reservedUserId': attributes.get('reservedUserId'),  # 新增：保留者ID
            'reservedUserName': attributes.get('reservedUserName'),  # 新增：保留者名称
            'extension': attributes.get('extension', {})
        }
        
        nodes.append(node)
        
        # 收集需要获取版本的文件ID
        file_ids_for_versions.append(item_id)
    
    # 并行获取权限信息
    permissions_results = {}
    if include_permissions and folder_ids_for_permissions:
        permissions_results = get_permissions_parallel(project_id, folder_ids_for_permissions, headers)
    
    # 并行获取版本信息
    versions_results = {}
    if file_ids_for_versions:
        versions_results = get_versions_parallel(project_id, file_ids_for_versions, headers)
    
    # 将权限信息分配给文件夹节点
    for node in nodes:
        if node.type == 'folder' and node.id in permissions_results:
            permissions_result = permissions_results[node.id]
            if permissions_result["status"] == "success":
                node.permissions = {
                    "status": "success",
                    "data": permissions_result["permissions"],
                    "api_source": "beta_permissions_api"
                }
            else:
                node.permissions = {
                    "status": permissions_result["status"],
                    "error": permissions_result.get("error"),
                    "api_source": "beta_permissions_api"
                }
        
        # 将版本信息分配给文件节点
        elif node.type == 'file' and node.id in versions_results:
            node.versions = versions_results[node.id]
            
            # 从版本信息中提取更多属性
            if node.versions:
                latest_version = node.versions[0]
                version_attributes = latest_version.get('attributes', {})
                file_size = (version_attributes.get('storageSize', 0) or 
                           version_attributes.get('fileSize', 0) or
                           latest_version.get('storageSize', 0) or
                           latest_version.get('fileSize', 0))
                
                node.attributes.update({
                    'fileSize': file_size,
                    'storageSize': file_size,
                    'versionNumber': latest_version.get('versionNumber', 1),
                    'mimeType': version_attributes.get('mimeType'),
                    'fileType': version_attributes.get('fileType')
                })
    
    # 递归处理子文件夹（并行）
    folder_nodes = [node for node in nodes if node.type == 'folder']
    if folder_nodes and current_depth + 1 < max_depth:
        # 并行处理子文件夹
        with ThreadPoolExecutor(max_workers=min(len(folder_nodes), 3)) as pool:
            future_to_node = {}
            for node in folder_nodes:
                future = pool.submit(
                    build_file_tree_with_permissions_parallel,
                    project_id, node.id, headers, node, max_depth, current_depth + 1, 
                    include_permissions, include_custom_attributes
                )
                future_to_node[future] = node
            
            for future in as_completed(future_to_node):
                node = future_to_node[future]
                try:
                    child_nodes = future.result()
                    node.children = child_nodes
                except Exception as e:
                    print(f"❌ 处理子文件夹 {node.name} 失败: {str(e)}")
                    node.children = []
    
    return nodes


def build_file_tree_batch_optimized(project_id, folder_id, headers, parent_node=None, max_depth=10, current_depth=0, include_permissions=True, include_custom_attributes=True):
    """
    批量优化版本的文件树构建 - 减少API调用次数
    """
    if current_depth >= max_depth:
        print(f"⚠️ 达到最大递归深度 {max_depth}，停止遍历")
        return []
    
    print(f"📁 批量遍历文件夹 (深度 {current_depth}): {folder_id}")
    
    # 获取当前文件夹内容
    contents_data = get_folder_contents(project_id, folder_id, headers)
    nodes = []
    
    # 分离文件夹和文件
    folder_items = []
    file_items = []
    
    for item in contents_data.get('data', []):
        item_type = item.get('type')
        if item_type == 'folders':
            folder_items.append(item)
        else:
            file_items.append(item)
    
    # 收集所有需要处理的ID
    folder_ids_for_permissions = []
    file_ids_for_versions = []
    child_folder_ids = []
    
    # 处理文件夹
    for item in folder_items:
        item_id = item.get('id')
        attributes = item.get('attributes', {})
        item_name = attributes.get('displayName', attributes.get('name', 'Unknown'))
        
        # 创建节点
        node = FileTreeNode(
            item_id=item_id,
            name=item_name,
            item_type='folder',
            parent_id=folder_id
        )
        
        # 添加属性信息
        node.attributes = {
            'displayName': item_name,
            'createTime': attributes.get('createTime'),
            'createUserId': attributes.get('createUserId'),
            'createUserName': attributes.get('createUserName'),
            'lastModifiedTime': attributes.get('lastModifiedTime'),
            'lastModifiedUserId': attributes.get('lastModifiedUserId'),
            'lastModifiedUserName': attributes.get('lastModifiedUserName'),
            'lastModifiedTimeRollup': attributes.get('lastModifiedTimeRollup'),  # 新增：包括子文件/版本的最后修改时间
            'objectCount': attributes.get('objectCount', 0),
            'path': attributes.get('path'),  # 新增：文件夹路径
            'hidden': attributes.get('hidden', False)  # 新增：是否隐藏
        }
        
        nodes.append(node)
        
        # 收集ID用于批量处理
        if include_permissions:
            folder_ids_for_permissions.append(item_id)
        
        if current_depth + 1 < max_depth:
            child_folder_ids.append(item_id)
            print(f"📂 将在下一层遍历文件夹: {item_name} (当前深度: {current_depth}, 最大深度: {max_depth})")
    
    # 处理文件
    for item in file_items:
        item_id = item.get('id')
        attributes = item.get('attributes', {})
        item_name = attributes.get('displayName', attributes.get('name', 'Unknown'))
        
        # 创建节点
        node = FileTreeNode(
            item_id=item_id,
            name=item_name,
            item_type='file',
            parent_id=folder_id
        )
        
        # 添加属性信息
        node.attributes = {
            'displayName': item_name,
            'createTime': attributes.get('createTime'),
            'createUserId': attributes.get('createUserId'),
            'createUserName': attributes.get('createUserName'),
            'lastModifiedTime': attributes.get('lastModifiedTime'),
            'lastModifiedUserId': attributes.get('lastModifiedUserId'),
            'lastModifiedUserName': attributes.get('lastModifiedUserName'),
            'lastModifiedTimeRollup': attributes.get('lastModifiedTimeRollup'),  # 新增：包括版本的最后修改时间
            'size': attributes.get('size', 0),
            'hidden': attributes.get('hidden', False),  # 新增：是否隐藏
            'reserved': attributes.get('reserved', False),  # 新增：是否被保留
            'reservedTime': attributes.get('reservedTime'),  # 新增：保留时间
            'reservedUserId': attributes.get('reservedUserId'),  # 新增：保留者ID
            'reservedUserName': attributes.get('reservedUserName'),  # 新增：保留者名称
            'extension': attributes.get('extension', {})
        }
        
        nodes.append(node)
        file_ids_for_versions.append(item_id)
    
    # 批量获取权限信息
    permissions_results = {}
    if include_permissions and folder_ids_for_permissions:
        permissions_results = get_permissions_batch_api(project_id, folder_ids_for_permissions, headers)
    
    # 批量获取版本信息
    versions_results = {}
    if file_ids_for_versions:
        versions_results = get_versions_batch_api(project_id, file_ids_for_versions, headers)
    
    # 批量获取子文件夹内容（如果需要递归）
    child_contents_results = {}
    if child_folder_ids:
        print(f"🔄 批量获取 {len(child_folder_ids)} 个子文件夹内容")
        child_contents_results = get_multiple_folder_contents_batch(project_id, child_folder_ids, headers)
    
    # 分配权限信息给文件夹节点
    for node in nodes:
        if node.type == 'folder' and node.id in permissions_results:
            permissions_result = permissions_results[node.id]
            if permissions_result["status"] == "success":
                node.permissions = {
                    "status": "success",
                    "data": permissions_result["permissions"],
                    "api_source": "batch_permissions_api"
                }
            else:
                node.permissions = {
                    "status": permissions_result["status"],
                    "error": permissions_result.get("error"),
                    "api_source": "batch_permissions_api"
                }
        
        # 分配版本信息给文件节点
        elif node.type == 'file' and node.id in versions_results:
            node.versions = versions_results[node.id]
            
            # 从版本信息中提取更多属性
            if node.versions:
                latest_version = node.versions[0]
                version_attributes = latest_version.get('attributes', {})
                file_size = (version_attributes.get('storageSize', 0) or 
                           version_attributes.get('fileSize', 0) or
                           latest_version.get('storageSize', 0) or
                           latest_version.get('fileSize', 0))
                
                node.attributes.update({
                    'fileSize': file_size,
                    'storageSize': file_size,
                    'versionNumber': latest_version.get('versionNumber', 1),
                    'mimeType': version_attributes.get('mimeType'),
                    'fileType': version_attributes.get('fileType')
                })
    
    # 递归处理子文件夹（使用批量获取的内容）
    folder_nodes = [node for node in nodes if node.type == 'folder']
    print(f"🔄 检查递归条件: 文件夹数量={len(folder_nodes)}, 当前深度={current_depth}, 最大深度={max_depth}, 条件={current_depth + 1 < max_depth}")
    if folder_nodes and current_depth + 1 < max_depth:
        # 为每个子文件夹递归构建子树
        for node in folder_nodes:
            if node.id in child_contents_results:
                # 使用已经批量获取的内容，避免重复API调用
                child_contents = child_contents_results[node.id]
                print(f"🔄 递归处理子文件夹: {node.name} (深度 {current_depth} -> {current_depth + 1})")
                child_nodes = build_file_tree_from_contents(
                    project_id, node.id, child_contents, headers, node, 
                    max_depth, current_depth + 1, include_permissions, include_custom_attributes
                )
                node.children = child_nodes
    
    # 批量获取文件的自定义属性
    file_nodes = [node for node in nodes if node.type == 'file']
    if file_nodes and include_custom_attributes:
        print(f"📝 批量优化版本：开始获取 {len(file_nodes)} 个文件的自定义属性")
        custom_attributes_data = batch_get_files_custom_attributes(project_id, file_nodes)
        print(f"📝 批量优化版本：自定义属性API返回数据: {len(custom_attributes_data)} 个文件")
        
        # 将自定义属性添加到文件节点
        for node in file_nodes:
            if hasattr(node, 'versions') and node.versions:
                latest_version = node.versions[0]
                version_id = latest_version.get('id')
                
                if version_id and version_id in custom_attributes_data:
                    custom_attrs = custom_attributes_data[version_id]
                    node.attributes['customAttributes'] = custom_attrs.get('customAttributes', {})
                    node.attributes['hasCustomAttributes'] = custom_attrs.get('hasCustomAttributes', False)
                    print(f"✅ 批量优化版本：文件 {node.name} 已添加自定义属性: {len(custom_attrs.get('customAttributes', {}))} 个")
                else:
                    node.attributes['customAttributes'] = {}
                    node.attributes['hasCustomAttributes'] = False
                    print(f"📝 批量优化版本：文件 {node.name} 无自定义属性数据")
            else:
                # 确保所有文件节点都有这些字段
                node.attributes['customAttributes'] = {}
                node.attributes['hasCustomAttributes'] = False
    
    # 获取文件夹的自定义属性定义
    folder_nodes = [node for node in nodes if node.type == 'folder']
    print(f"🔍 DEBUG: folder_nodes={len(folder_nodes)}, include_custom_attributes={include_custom_attributes}")
    if folder_nodes and include_custom_attributes:
        print(f"📝 批量优化版本：开始获取 {len(folder_nodes)} 个文件夹的自定义属性定义")
        
        for node in folder_nodes:
            folder_custom_attrs = get_folder_custom_attribute_definitions(project_id, node.id)
            
            if folder_custom_attrs and folder_custom_attrs.get('customAttributeDefinitions'):
                node.attributes['customAttributeDefinitions'] = folder_custom_attrs.get('customAttributeDefinitions', {})
                node.attributes['hasCustomAttributeDefinitions'] = folder_custom_attrs.get('hasCustomAttributeDefinitions', False)
                node.attributes['totalCustomAttributeDefinitions'] = folder_custom_attrs.get('totalDefinitions', 0)
                print(f"✅ 批量优化版本：文件夹 {node.name} 已添加自定义属性定义 ({folder_custom_attrs.get('totalDefinitions', 0)} 个)")
            else:
                node.attributes['customAttributeDefinitions'] = {}
                node.attributes['hasCustomAttributeDefinitions'] = False
                node.attributes['totalCustomAttributeDefinitions'] = 0
                print(f"📝 批量优化版本：文件夹 {node.name} 无自定义属性定义")
    
    return nodes


def build_file_tree_from_contents(project_id, folder_id, contents_data, headers, parent_node=None, max_depth=10, current_depth=0, include_permissions=True, include_custom_attributes=True):
    """
    从已获取的内容数据构建文件树（避免重复API调用）
    """
    if current_depth >= max_depth:
        return []
    
    nodes = []
    
    # 分离文件夹和文件
    folder_items = []
    file_items = []
    
    for item in contents_data.get('data', []):
        item_type = item.get('type')
        if item_type == 'folders':
            folder_items.append(item)
        else:
            file_items.append(item)
    
    # 收集需要批量处理的ID
    folder_ids_for_permissions = []
    file_ids_for_versions = []
    
    # 处理文件夹
    for item in folder_items:
        item_id = item.get('id')
        attributes = item.get('attributes', {})
        item_name = attributes.get('displayName', attributes.get('name', 'Unknown'))
        
        node = FileTreeNode(
            item_id=item_id,
            name=item_name,
            item_type='folder',
            parent_id=folder_id
        )
        
        node.attributes = {
            'displayName': item_name,
            'createTime': attributes.get('createTime'),
            'createUserId': attributes.get('createUserId'),
            'createUserName': attributes.get('createUserName'),
            'lastModifiedTime': attributes.get('lastModifiedTime'),
            'lastModifiedUserId': attributes.get('lastModifiedUserId'),
            'lastModifiedUserName': attributes.get('lastModifiedUserName'),
            'lastModifiedTimeRollup': attributes.get('lastModifiedTimeRollup'),  # 新增：包括子文件/版本的最后修改时间
            'objectCount': attributes.get('objectCount', 0),
            'path': attributes.get('path'),  # 新增：文件夹路径
            'hidden': attributes.get('hidden', False)  # 新增：是否隐藏
        }
        
        nodes.append(node)
        
        if include_permissions:
            folder_ids_for_permissions.append(item_id)
    
    # 处理文件
    for item in file_items:
        item_id = item.get('id')
        attributes = item.get('attributes', {})
        item_name = attributes.get('displayName', attributes.get('name', 'Unknown'))
        
        node = FileTreeNode(
            item_id=item_id,
            name=item_name,
            item_type='file',
            parent_id=folder_id
        )
        
        node.attributes = {
            'displayName': item_name,
            'createTime': attributes.get('createTime'),
            'createUserId': attributes.get('createUserId'),
            'createUserName': attributes.get('createUserName'),
            'lastModifiedTime': attributes.get('lastModifiedTime'),
            'lastModifiedUserId': attributes.get('lastModifiedUserId'),
            'lastModifiedUserName': attributes.get('lastModifiedUserName'),
            'lastModifiedTimeRollup': attributes.get('lastModifiedTimeRollup'),  # 新增：包括版本的最后修改时间
            'size': attributes.get('size', 0),
            'hidden': attributes.get('hidden', False),  # 新增：是否隐藏
            'reserved': attributes.get('reserved', False),  # 新增：是否被保留
            'reservedTime': attributes.get('reservedTime'),  # 新增：保留时间
            'reservedUserId': attributes.get('reservedUserId'),  # 新增：保留者ID
            'reservedUserName': attributes.get('reservedUserName'),  # 新增：保留者名称
            'extension': attributes.get('extension', {})
        }
        
        nodes.append(node)
        file_ids_for_versions.append(item_id)
    
    # 批量获取权限和版本信息
    permissions_results = {}
    if include_permissions and folder_ids_for_permissions:
        permissions_results = get_permissions_batch_api(project_id, folder_ids_for_permissions, headers)
    
    versions_results = {}
    if file_ids_for_versions:
        versions_results = get_versions_batch_api(project_id, file_ids_for_versions, headers)
    
    # 分配数据
    for node in nodes:
        if node.type == 'folder' and node.id in permissions_results:
            permissions_result = permissions_results[node.id]
            if permissions_result["status"] == "success":
                node.permissions = {
                    "status": "success",
                    "data": permissions_result["permissions"],
                    "api_source": "batch_permissions_api"
                }
            else:
                node.permissions = {
                    "status": permissions_result["status"],
                    "error": permissions_result.get("error"),
                    "api_source": "batch_permissions_api"
                }
        
        elif node.type == 'file' and node.id in versions_results:
            node.versions = versions_results[node.id]
            
            if node.versions:
                latest_version = node.versions[0]
                version_attributes = latest_version.get('attributes', {})
                file_size = (version_attributes.get('storageSize', 0) or 
                           version_attributes.get('fileSize', 0) or
                           latest_version.get('storageSize', 0) or
                           latest_version.get('fileSize', 0))
                
                node.attributes.update({
                    'fileSize': file_size,
                    'storageSize': file_size,
                    'versionNumber': latest_version.get('versionNumber', 1),
                    'mimeType': version_attributes.get('mimeType'),
                    'fileType': version_attributes.get('fileType')
                })
    
    # 递归处理子文件夹（如果还没有达到最大深度）
    if current_depth + 1 < max_depth:
        folder_nodes = [node for node in nodes if node.type == 'folder']
        print(f"🔄 build_file_tree_from_contents 递归检查: 文件夹数量={len(folder_nodes)}, 当前深度={current_depth}, 最大深度={max_depth}")
        
        for node in folder_nodes:
            print(f"🔄 递归获取子文件夹内容: {node.name} (深度 {current_depth} -> {current_depth + 1})")
            # 获取子文件夹内容
            child_contents_data = get_folder_contents(project_id, node.id, headers)
            
            # 递归构建子树
            child_nodes = build_file_tree_from_contents(
                project_id, node.id, child_contents_data, headers, node, 
                max_depth, current_depth + 1, include_permissions, include_custom_attributes
            )
            node.children = child_nodes
    
    # 批量获取文件的自定义属性
    file_nodes = [node for node in nodes if node.type == 'file']
    if file_nodes and include_custom_attributes:
        print(f"📝 from_contents版本：开始获取 {len(file_nodes)} 个文件的自定义属性")
        custom_attributes_data = batch_get_files_custom_attributes(project_id, file_nodes)
        print(f"📝 from_contents版本：自定义属性API返回数据: {len(custom_attributes_data)} 个文件")
        
        # 将自定义属性添加到文件节点
        for node in file_nodes:
            if hasattr(node, 'versions') and node.versions:
                latest_version = node.versions[0]
                version_id = latest_version.get('id')
                
                if version_id and version_id in custom_attributes_data:
                    custom_attrs = custom_attributes_data[version_id]
                    node.attributes['customAttributes'] = custom_attrs.get('customAttributes', {})
                    node.attributes['hasCustomAttributes'] = custom_attrs.get('hasCustomAttributes', False)
                    print(f"✅ from_contents版本：文件 {node.name} 已添加自定义属性: {len(custom_attrs.get('customAttributes', {}))} 个")
                else:
                    node.attributes['customAttributes'] = {}
                    node.attributes['hasCustomAttributes'] = False
                    print(f"📝 from_contents版本：文件 {node.name} 无自定义属性数据")
            else:
                # 确保所有文件节点都有这些字段
                node.attributes['customAttributes'] = {}
                node.attributes['hasCustomAttributes'] = False
    
    # 获取文件夹的自定义属性定义
    folder_nodes = [node for node in nodes if node.type == 'folder']
    if folder_nodes and include_custom_attributes:
        print(f"📝 from_contents版本：开始获取 {len(folder_nodes)} 个文件夹的自定义属性定义")
        
        for node in folder_nodes:
            folder_custom_attrs = get_folder_custom_attribute_definitions(project_id, node.id)
            
            if folder_custom_attrs and folder_custom_attrs.get('customAttributeDefinitions'):
                node.attributes['customAttributeDefinitions'] = folder_custom_attrs.get('customAttributeDefinitions', {})
                node.attributes['hasCustomAttributeDefinitions'] = folder_custom_attrs.get('hasCustomAttributeDefinitions', False)
                node.attributes['totalCustomAttributeDefinitions'] = folder_custom_attrs.get('totalDefinitions', 0)
                print(f"✅ from_contents版本：文件夹 {node.name} 已添加自定义属性定义 ({folder_custom_attrs.get('totalDefinitions', 0)} 个)")
            else:
                node.attributes['customAttributeDefinitions'] = {}
                node.attributes['hasCustomAttributeDefinitions'] = False
                node.attributes['totalCustomAttributeDefinitions'] = 0
                print(f"📝 from_contents版本：文件夹 {node.name} 无自定义属性定义")
    
    return nodes


@file_sync_bp.route('/api/file-sync/project/<project_id>/folder/<folder_id>/children')
def get_folder_children_with_permissions(project_id, folder_id):
    """
    获取指定文件夹的子节点（懒加载）
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
        print(f"🔄 懒加载文件夹子节点: {folder_id}")
        start_time = time.time()
        
        # 获取参数
        max_depth = request.args.get('maxDepth', 1, type=int)  # 懒加载时只加载一层
        include_permissions = request.args.get('includePermissions', 'true').lower() == 'true'
        include_custom_attributes = request.args.get('includeCustomAttributes', 'true').lower() == 'true'
        compact_response = request.args.get('compact', 'false').lower() == 'true'  # 默认使用完整响应
        
        
        # 构建子树（使用批量优化版本）
        child_nodes = build_file_tree_batch_optimized(
            project_id, folder_id, headers, None, max_depth, 0, include_permissions, include_custom_attributes
        )
        
        # 统计信息
        total_folders = sum(1 for node in child_nodes if node.type == 'folder')
        total_files = sum(1 for node in child_nodes if node.type == 'file')
        
        end_time = time.time()
        
        result = {
            'folder_id': folder_id,
            'children': [node.to_dict(compact=compact_response) for node in child_nodes],
            'statistics': {
                'total_folders': total_folders,
                'total_files': total_files,
                'load_duration_seconds': round(end_time - start_time, 2)
            },
            'response_format': 'compact' if compact_response else 'full'
        }
        
        print(f"✅ 懒加载完成: {total_folders} 个文件夹，{total_files} 个文件，耗时 {result['statistics']['load_duration_seconds']} 秒")
        
        return jsonify({
            "status": "success",
            "message": f"成功加载文件夹子节点，共 {total_folders} 个文件夹，{total_files} 个文件",
            "data": result
        })
        
    except Exception as e:
        print(f"❌ 懒加载文件夹子节点时出错: {str(e)}")
        return jsonify({
            "error": f"加载文件夹子节点失败: {str(e)}",
            "status": "error",
            "folder_id": folder_id
        }), 500


@file_sync_bp.route('/api/file-sync/project/<project_id>/tree-with-permissions')
def get_project_file_tree_with_permissions(project_id):
    """
    获取项目的完整文件树结构（包含权限信息）
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
        print(f"🚀 开始同步项目文件树（含权限）: {project_id}")
        start_time = time.time()
        
        # 获取参数
        max_depth = request.args.get('maxDepth', 2, type=int)
        include_permissions = request.args.get('includePermissions', 'false').lower() == 'true'  # 默认不包含权限
        include_custom_attributes = request.args.get('includeCustomAttributes', 'false').lower() == 'true'  # 默认不包含自定义属性
        compact_response = request.args.get('compact', 'false').lower() == 'true'  # 主API默认完整响应
        
        # 优化：默认使用快速模式（不包含权限和自定义属性）
        fast_mode = not include_permissions and not include_custom_attributes
        if fast_mode:
            print(f"🚀 启用快速模式：深度={max_depth}, 权限={include_permissions}, 自定义属性={include_custom_attributes}")
        else:
            print(f"📊 启用完整模式：深度={max_depth}, 权限={include_permissions}, 自定义属性={include_custom_attributes}")
        
        # 获取顶级文件夹
        top_folders_data = get_project_top_folders(project_id, headers)
        
        if not top_folders_data.get('data'):
            return jsonify({
                "error": "Unable to get project top-level folders",
                "status": "error",
                "project_id": project_id
            }), 404
        
        # 构建完整的文件树（含权限）
        project_tree = {
            'project_id': project_id,
            'sync_time': datetime.now().isoformat(),
            'include_permissions': include_permissions,
            'top_folders': [],
            'statistics': {
                'total_folders': 0,
                'total_files': 0,
                'total_size': 0,
                'folders_with_permissions': 0,
                'permission_errors': 0,
                'sync_duration_seconds': 0
            },
            'permission_summary': {
                'total_users': 0,
                'total_roles': 0,
                'total_companies': 0
            }
        }
        
        total_folders = 0
        total_files = 0
        total_size = 0
        folders_with_permissions = 0
        permission_errors = 0
        total_users = 0
        total_roles = 0
        total_companies = 0
        
        # 处理每个顶级文件夹
        for top_folder in top_folders_data.get('data', []):
            folder_id = top_folder.get('id')
            folder_attributes = top_folder.get('attributes', {})
            folder_name = folder_attributes.get('displayName', folder_attributes.get('name', 'Unknown'))
            
            print(f"📁 处理顶级文件夹: {folder_name}")
            
            # 创建顶级文件夹节点
            top_folder_node = FileTreeNode(
                item_id=folder_id,
                name=folder_name,
                item_type='folder',
                parent_id=None
            )
            
            top_folder_node.attributes = {
                'displayName': folder_name,
                'createTime': folder_attributes.get('createTime'),
                'createUserId': folder_attributes.get('createUserId'),
                'createUserName': folder_attributes.get('createUserName'),
                'lastModifiedTime': folder_attributes.get('lastModifiedTime'),
                'objectCount': folder_attributes.get('objectCount', 0)
            }
            
            # 获取顶级文件夹权限
            if include_permissions:
                print(f"🔐 获取顶级文件夹权限: {folder_name}")
                permissions_result = get_folder_permissions_from_beta_api(project_id, folder_id, headers)
                
                if permissions_result["status"] == "success":
                    top_folder_node.permissions = {
                        "status": "success",
                        "data": permissions_result["permissions"],
                        "api_source": "beta_permissions_api"
                    }
                    folders_with_permissions += 1
                    
                    # 统计权限信息
                    perm_summary = permissions_result["permissions"]["summary"]
                    total_users += perm_summary.get("users_count", 0)
                    total_roles += perm_summary.get("roles_count", 0)
                    total_companies += perm_summary.get("companies_count", 0)
                    
                    print(f"✅ 顶级文件夹权限获取成功: {perm_summary['total_subjects']} 个主体")
                else:
                    top_folder_node.permissions = {
                        "status": permissions_result["status"],
                        "error": permissions_result.get("error"),
                        "api_source": "beta_permissions_api"
                    }
                    permission_errors += 1
                    print(f"⚠️ 顶级文件夹权限获取失败: {permissions_result.get('error')}")
            
            # 递归构建子树（含权限，使用批量优化版本）
            if fast_mode:
                # 快速模式：使用轻量级构建方法
                from .file_sync_optimized import build_file_tree_recursive_optimized
                child_nodes = build_file_tree_recursive_optimized(
                    project_id, folder_id, headers, top_folder_node, max_depth, 0
                )
            else:
                # 标准模式：使用批量优化版本
                child_nodes = build_file_tree_batch_optimized(
                    project_id, folder_id, headers, top_folder_node, max_depth, 0, include_permissions, include_custom_attributes
                )
            top_folder_node.children = child_nodes
            
            # 统计信息
            def count_nodes_and_permissions(nodes):
                folders = 0
                files = 0
                size = 0
                perm_folders = 0
                perm_errors = 0
                users = 0
                roles = 0
                companies = 0
                
                for node in nodes:
                    if node.type == 'folder':
                        folders += 1
                        
                        # 统计权限信息
                        if hasattr(node, 'permissions') and node.permissions:
                            if node.permissions.get("status") == "success":
                                perm_folders += 1
                                perm_data = node.permissions.get("data", {}).get("summary", {})
                                users += perm_data.get("users_count", 0)
                                roles += perm_data.get("roles_count", 0)
                                companies += perm_data.get("companies_count", 0)
                            else:
                                perm_errors += 1
                        
                        f, fi, s, pf, pe, u, r, c = count_nodes_and_permissions(node.children)
                        folders += f
                        files += fi
                        size += s
                        perm_folders += pf
                        perm_errors += pe
                        users += u
                        roles += r
                        companies += c
                    else:
                        files += 1
                        # 获取文件大小
                        file_size = 0
                        if node.versions:
                            latest_version = node.versions[0]
                            file_size = latest_version.get('fileSize', 0) or latest_version.get('storageSize', 0)
                        if file_size == 0:
                            file_size = node.attributes.get('size', 0) or node.attributes.get('storageSize', 0)
                        size += file_size
                
                return folders, files, size, perm_folders, perm_errors, users, roles, companies
            
            f, fi, s, pf, pe, u, r, c = count_nodes_and_permissions(child_nodes)
            total_folders += f + 1  # +1 for the top folder itself
            total_files += fi
            total_size += s
            folders_with_permissions += pf
            permission_errors += pe
            total_users += u
            total_roles += r
            total_companies += c
            
            project_tree['top_folders'].append(top_folder_node.to_dict(compact=compact_response))
        
        # 更新统计信息
        end_time = time.time()
        project_tree['statistics'] = {
            'total_folders': total_folders,
            'total_files': total_files,
            'total_size': total_size,
            'folders_with_permissions': folders_with_permissions,
            'permission_errors': permission_errors,
            'sync_duration_seconds': round(end_time - start_time, 2)
        }
        
        project_tree['permission_summary'] = {
            'total_users': total_users,
            'total_roles': total_roles,
            'total_companies': total_companies
        }
        
        print(f"✅ 文件树同步完成（含权限）:")
        print(f"   📁 文件夹: {total_folders}")
        print(f"   📄 文件: {total_files}")
        print(f"   💾 总大小: {total_size} bytes")
        print(f"   🔐 权限成功: {folders_with_permissions}")
        print(f"   ❌ 权限失败: {permission_errors}")
        print(f"   👥 总用户: {total_users}")
        print(f"   🎭 总角色: {total_roles}")
        print(f"   🏢 总公司: {total_companies}")
        print(f"   ⏱️ 耗时: {project_tree['statistics']['sync_duration_seconds']} 秒")
        
        return jsonify({
            "status": "success",
            "message": f"成功同步项目文件树，共 {total_folders} 个文件夹，{total_files} 个文件，{folders_with_permissions} 个文件夹获取权限成功",
            "data": project_tree
        })
        
    except Exception as e:
        print(f"❌ 同步文件树（含权限）时出错: {str(e)}")
        return jsonify({
            "error": f"同步文件树失败: {str(e)}",
            "status": "error",
            "project_id": project_id
        }), 500


def build_file_tree_fast_only(project_id, folder_id, headers, parent_node=None, max_depth=5, current_depth=0, include_custom_attributes=False):
    """
    纯净的快速文件树构建 - 不获取权限，可选自定义属性
    """
    if current_depth >= max_depth:
        print(f"⚠️ 达到最大递归深度 {max_depth}，停止遍历")
        return []
    
    print(f"📁 快速遍历文件夹 (深度 {current_depth}): {folder_id}")
    
    # 获取文件夹内容
    contents_data = get_folder_contents(project_id, folder_id, headers)
    nodes = []
    
    for item in contents_data.get('data', []):
        item_id = item.get('id')
        item_type = item.get('type')
        attributes = item.get('attributes', {})
        item_name = attributes.get('displayName', attributes.get('name', 'Unknown'))
        
        # 创建节点
        node = FileTreeNode(
            item_id=item_id,
            name=item_name,
            item_type='folder' if item_type == 'folders' else 'file',
            parent_id=folder_id
        )
        
        # 清理用户信息
        create_user_id, create_user_name = sanitize_user_info(
            attributes.get('createUserId'), 
            attributes.get('createUserName')
        )
        modified_user_id, modified_user_name = sanitize_user_info(
            attributes.get('lastModifiedUserId'), 
            attributes.get('lastModifiedUserName')
        )
        
        # 添加基础属性信息
        node.attributes = {
            'displayName': item_name,
            'createTime': attributes.get('createTime'),
            'createUserId': create_user_id,
            'createUserName': create_user_name,
            'lastModifiedTime': attributes.get('lastModifiedTime'),
            'lastModifiedUserId': modified_user_id,
            'lastModifiedUserName': modified_user_name,
            'lastModifiedTimeRollup': attributes.get('lastModifiedTimeRollup'),  # 新增：包括子文件/版本的最后修改时间
            'objectCount': attributes.get('objectCount', 0),
            'size': attributes.get('size', 0),
            'path': attributes.get('path'),  # 新增：文件夹路径
            'hidden': attributes.get('hidden', False),  # 新增：是否隐藏
            'extension': attributes.get('extension', {}),
            # 为文件夹添加自定义属性标记，表示可以按需加载
            'hasCustomAttributeDefinitions': item_type == 'folders',
            'customAttributeDefinitions': {},
            'totalCustomAttributeDefinitions': 0
        }
        
        # 如果是文件，添加文件特有的属性
        if item_type != 'folders':
            node.attributes.update({
                'reserved': attributes.get('reserved', False),  # 是否被保留
                'reservedTime': attributes.get('reservedTime'),  # 保留时间
                'reservedUserId': attributes.get('reservedUserId'),  # 保留者ID
                'reservedUserName': attributes.get('reservedUserName')  # 保留者名称
            })
        
        # 设置基本权限信息（不调用API）
        node.permissions = {
            'canRead': True,
            'canWrite': False,
            'canDelete': False
        }
        
        if item_type == 'folders':
            # 递归处理子文件夹
            print(f"📂 快速处理子文件夹: {item_name}")
            child_nodes = build_file_tree_fast_only(
                project_id, item_id, headers, node, max_depth, current_depth + 1, include_custom_attributes
            )
            node.children = child_nodes
        else:
            # 处理文件，获取基础版本信息
            print(f"📄 快速处理文件: {item_name}")
            versions = get_item_versions(project_id, item_id, headers)
            node.versions = versions
            
            # 从版本信息中提取基础属性
            if versions:
                latest_version = versions[0]
                version_attributes = latest_version.get('attributes', {})
                file_size = (version_attributes.get('storageSize', 0) or 
                           version_attributes.get('fileSize', 0) or
                           latest_version.get('storageSize', 0) or
                           latest_version.get('fileSize', 0))
                
                node.attributes.update({
                    'versionNumber': version_attributes.get('versionNumber'),
                    'mimeType': version_attributes.get('mimeType'),
                    'fileSize': file_size,
                    'storageSize': file_size,
                    # 为文件添加自定义属性标记，表示可以按需加载
                    'hasCustomAttributes': True,
                    'customAttributes': {},
                    'totalCustomAttributes': 0
                })
        
        nodes.append(node)
    
    # 批量获取文件的自定义属性（如果启用）
    if include_custom_attributes:
        file_nodes = [node for node in nodes if node.type == 'file']
        if file_nodes:
            print(f"📝 快速模式：开始获取 {len(file_nodes)} 个文件的自定义属性")
            custom_attributes_data = batch_get_files_custom_attributes(project_id, file_nodes)
            
            # 将自定义属性添加到文件节点
            for node in file_nodes:
                if hasattr(node, 'versions') and node.versions:
                    latest_version = node.versions[0]
                    version_id = latest_version.get('id')
                    
                    if version_id and version_id in custom_attributes_data:
                        custom_attrs = custom_attributes_data[version_id]
                        node.attributes['customAttributes'] = custom_attrs.get('customAttributes', {})
                        node.attributes['hasCustomAttributes'] = custom_attrs.get('hasCustomAttributes', False)
                        print(f"✅ 快速模式：文件 {node.name} 已添加自定义属性: {len(custom_attrs.get('customAttributes', {}))} 个")
                    else:
                        node.attributes['customAttributes'] = {}
                        node.attributes['hasCustomAttributes'] = False
                        print(f"📝 快速模式：文件 {node.name} 无自定义属性数据")
    
    return nodes


@file_sync_bp.route('/api/file-sync/project/<project_id>/tree-fast')
def get_project_file_tree_fast(project_id):
    """
    快速获取项目文件树结构（浅层，无权限）
    专门用于首次加载，提供更快的响应速度
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
        print(f"⚡ 开始快速同步项目文件树: {project_id}")
        start_time = time.time()
        
        # 获取参数，允许自定义属性加载
        max_depth = request.args.get('maxDepth', 5, type=int)  # 允许自定义深度
        include_permissions = False  # 不包含权限（保持快速）
        include_custom_attributes = request.args.get('includeCustomAttributes', 'false').lower() == 'true'  # 允许包含自定义属性
        
        # 获取顶级文件夹
        top_folders_data = get_project_top_folders(project_id, headers)
        
        if not top_folders_data.get('data'):
            return jsonify({
                "error": "Unable to get project top-level folders",
                "status": "error",
                "project_id": project_id
            }), 404
        
        # 构建快速文件树
        project_tree = {
            'project_id': project_id,
            'sync_time': datetime.now().isoformat(),
            'mode': 'fast',
            'max_depth': max_depth,
            'top_folders': [],
            'statistics': {
                'total_folders': 0,
                'total_files': 0,
                'sync_duration_seconds': 0
            }
        }
        
        total_folders = 0
        total_files = 0
        
        # 处理每个顶级文件夹（快速模式）
        for top_folder in top_folders_data.get('data', []):
            folder_id = top_folder.get('id')
            folder_attributes = top_folder.get('attributes', {})
            folder_name = folder_attributes.get('displayName', folder_attributes.get('name', 'Unknown'))
            
            print(f"📁 快速处理顶级文件夹: {folder_name}")
            
            # 创建顶级文件夹节点
            top_folder_node = FileTreeNode(
                item_id=folder_id,
                name=folder_name,
                item_type='folder',
                parent_id=None
            )
            
            # 清理顶级文件夹的用户信息
            create_user_id, create_user_name = sanitize_user_info(
                folder_attributes.get('createUserId'), 
                folder_attributes.get('createUserName')
            )
            modified_user_id, modified_user_name = sanitize_user_info(
                folder_attributes.get('lastModifiedUserId'), 
                folder_attributes.get('lastModifiedUserName')
            )
            
            # 基础属性（快速模式）
            top_folder_node.attributes = {
                'displayName': folder_name,
                'createTime': folder_attributes.get('createTime'),
                'createUserId': create_user_id,
                'createUserName': create_user_name,
                'lastModifiedTime': folder_attributes.get('lastModifiedTime'),
                'lastModifiedUserId': modified_user_id,
                'lastModifiedUserName': modified_user_name,
                'lastModifiedTimeRollup': folder_attributes.get('lastModifiedTimeRollup'),
                'objectCount': folder_attributes.get('objectCount', 0),
                'path': folder_attributes.get('path'),
                'hidden': folder_attributes.get('hidden', False)
            }
            
            # 快速构建子树（无权限，可选自定义属性）
            child_nodes = build_file_tree_fast_only(
                project_id, folder_id, headers, top_folder_node, max_depth, 0, include_custom_attributes
            )
            top_folder_node.children = child_nodes
            
            # 快速统计
            def count_nodes_fast(nodes):
                folders = 0
                files = 0
                for node in nodes:
                    if node.type == 'folder':
                        folders += 1
                        f, fi = count_nodes_fast(node.children)
                        folders += f
                        files += fi
                    else:
                        files += 1
                return folders, files
            
            f, fi = count_nodes_fast(child_nodes)
            total_folders += f + 1  # +1 for the top folder itself
            total_files += fi
            
            project_tree['top_folders'].append(top_folder_node.to_dict(compact=False))
        
        # 更新统计信息
        end_time = time.time()
        project_tree['statistics'] = {
            'total_folders': total_folders,
            'total_files': total_files,
            'sync_duration_seconds': round(end_time - start_time, 2)
        }
        
        print(f"✅ 快速文件树同步完成: {total_folders} 个文件夹, {total_files} 个文件, 耗时 {project_tree['statistics']['sync_duration_seconds']} 秒")
        
        return jsonify({
            "status": "success",
            "data": project_tree
        })
        
    except Exception as e:
        print(f"❌ 快速获取项目文件树时出错: {str(e)}")
        return jsonify({
            "error": f"快速获取项目文件树时出错: {str(e)}",
            "status": "error",
            "project_id": project_id
        }), 500


@file_sync_bp.route('/api/file-sync/project/<project_id>/download-with-permissions')
def download_project_files_with_permissions(project_id):
    """
    下载项目文件树和权限信息的JSON文件
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
        print(f"📥 准备下载项目文件和权限数据: {project_id}")
        
        # 获取参数
        max_depth = request.args.get('maxDepth', 2, type=int)
        include_permissions = request.args.get('includePermissions', 'true').lower() == 'true'
        include_custom_attributes = request.args.get('includeCustomAttributes', 'true').lower() == 'true'
        
        # 获取顶级文件夹
        top_folders_data = get_project_top_folders(project_id, headers)
        
        if not top_folders_data.get('data'):
            return jsonify({
                "error": "Unable to get project folders",
                "status": "error"
            }), 404
        
        # 构建完整数据
        export_data = {
            "project_id": project_id,
            "export_time": datetime.now().isoformat(),
            "export_parameters": {
                "max_depth": max_depth,
                "include_permissions": include_permissions,
                "include_custom_attributes": include_custom_attributes
            },
            "top_folders": [],
            "statistics": {
                "total_folders": 0,
                "total_files": 0,
                "total_size": 0,
                "folders_with_permissions": 0,
                "permission_errors": 0
            },
            "permission_summary": {
                "total_users": 0,
                "total_roles": 0,
                "total_companies": 0
            }
        }
        
        total_folders = 0
        total_files = 0
        total_size = 0
        folders_with_permissions = 0
        permission_errors = 0
        total_users = 0
        total_roles = 0
        total_companies = 0
        
        # 处理每个顶级文件夹
        for top_folder in top_folders_data.get('data', []):
            folder_id = top_folder.get('id')
            folder_attributes = top_folder.get('attributes', {})
            folder_name = folder_attributes.get('displayName', folder_attributes.get('name', 'Unknown'))
            
            print(f"📁 处理顶级文件夹: {folder_name}")
            
            # 创建顶级文件夹节点
            top_folder_node = FileTreeNode(
                item_id=folder_id,
                name=folder_name,
                item_type='folder',
                parent_id=None
            )
            
            top_folder_node.attributes = {
                'displayName': folder_name,
                'createTime': folder_attributes.get('createTime'),
                'createUserId': folder_attributes.get('createUserId'),
                'createUserName': folder_attributes.get('createUserName'),
                'lastModifiedTime': folder_attributes.get('lastModifiedTime'),
                'objectCount': folder_attributes.get('objectCount', 0)
            }
            
            # 获取权限信息
            if include_permissions:
                permissions_result = get_folder_permissions_from_beta_api(project_id, folder_id, headers)
                
                if permissions_result["status"] == "success":
                    top_folder_node.permissions = {
                        "status": "success",
                        "data": permissions_result["permissions"],
                        "api_source": "beta_permissions_api"
                    }
                    folders_with_permissions += 1
                    
                    perm_summary = permissions_result["permissions"]["summary"]
                    total_users += perm_summary.get("users_count", 0)
                    total_roles += perm_summary.get("roles_count", 0)
                    total_companies += perm_summary.get("companies_count", 0)
                else:
                    top_folder_node.permissions = {
                        "status": permissions_result["status"],
                        "error": permissions_result.get("error"),
                        "api_source": "beta_permissions_api"
                    }
                    permission_errors += 1
            
            # 递归构建子树
            child_nodes = build_file_tree_with_permissions(
                project_id, folder_id, headers, top_folder_node, max_depth, 0, include_permissions, include_custom_attributes
            )
            top_folder_node.children = child_nodes
            
            # 统计
            def count_all(nodes):
                folders = files = size = perm_folders = perm_errors = users = roles = companies = 0
                
                for node in nodes:
                    if node.type == 'folder':
                        folders += 1
                        if hasattr(node, 'permissions') and node.permissions:
                            if node.permissions.get("status") == "success":
                                perm_folders += 1
                                perm_data = node.permissions.get("data", {}).get("summary", {})
                                users += perm_data.get("users_count", 0)
                                roles += perm_data.get("roles_count", 0)
                                companies += perm_data.get("companies_count", 0)
                            else:
                                perm_errors += 1
                        
                        f, fi, s, pf, pe, u, r, c = count_all(node.children)
                        folders += f
                        files += fi
                        size += s
                        perm_folders += pf
                        perm_errors += pe
                        users += u
                        roles += r
                        companies += c
                    else:
                        files += 1
                        file_size = 0
                        if node.versions:
                            latest_version = node.versions[0]
                            file_size = latest_version.get('fileSize', 0) or latest_version.get('storageSize', 0)
                        if file_size == 0:
                            file_size = node.attributes.get('size', 0) or node.attributes.get('storageSize', 0)
                        size += file_size
                
                return folders, files, size, perm_folders, perm_errors, users, roles, companies
            
            f, fi, s, pf, pe, u, r, c = count_all(child_nodes)
            total_folders += f + 1
            total_files += fi
            total_size += s
            folders_with_permissions += pf
            permission_errors += pe
            total_users += u
            total_roles += r
            total_companies += c
            
            export_data['top_folders'].append(top_folder_node.to_dict())
            
            # 添加延迟
            time.sleep(0.1)
        
        # 更新统计信息
        export_data['statistics'] = {
            "total_folders": total_folders,
            "total_files": total_files,
            "total_size": total_size,
            "folders_with_permissions": folders_with_permissions,
            "permission_errors": permission_errors
        }
        
        export_data['permission_summary'] = {
            "total_users": total_users,
            "total_roles": total_roles,
            "total_companies": total_companies
        }
        
        # 创建下载文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        permissions_suffix = "_with_permissions" if include_permissions else ""
        filename = f"project_{project_id}_files{permissions_suffix}_{timestamp}.json"
        
        # 确保下载目录存在
        download_dir = "downloads"
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        
        file_path = os.path.join(download_dir, filename)
        
        # 写入JSON文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        print(f"📁 文件和权限数据已保存到: {file_path}")
        print(f"   📊 统计: {total_folders}文件夹, {total_files}文件, {folders_with_permissions}权限成功")
        
        # 返回文件下载
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/json'
        )
        
    except Exception as e:
        return jsonify({
            "error": f"下载文件和权限数据失败: {str(e)}",
            "status": "error"
        }), 500


@file_sync_bp.route('/api/file-sync/download-page/<project_id>/<item_id>/<int:page_num>')
def download_pdf_page(project_id, item_id, page_num):
    """下载PDF的指定页面"""
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
        # 1. 获取下载信息
        download_info_resp = requests.get(
            f"http://localhost:{config.PORT}/api/file-sync/download/{project_id}/{item_id}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        if download_info_resp.status_code != 200:
            return jsonify({
                "error": "Unable to get download information",
                "status": "error"
            }), 400
        
        download_data = download_info_resp.json()
        download_info = download_data.get('download_info', {})
        
        if download_info.get('method') != 'model_derivative':
            return jsonify({
                "error": "Unsupported download method",
                "status": "error"
            }), 400
        
        # 2. 获取指定页面的URN
        pdf_pages = download_info.get('pdf_pages', [])
        if page_num < 1 or page_num > len(pdf_pages):
            return jsonify({
                "error": f"页面编号无效，可用页面: 1-{len(pdf_pages)}",
                "status": "error"
            }), 400
        
        page_urn = pdf_pages[page_num - 1]
        download_base_url = download_info.get('download_base_url')
        
        # 3. 下载页面
        page_download_url = f"{download_base_url}/{page_urn}"
        print(f"🔗 下载页面 {page_num}: {page_download_url}")
        
        page_resp = requests.get(page_download_url, headers=headers, stream=True)
        
        if page_resp.status_code == 200:
            # 设置响应头
            response_headers = {
                'Content-Type': 'application/pdf',
                'Content-Disposition': f'attachment; filename="page_{page_num}.pdf"'
            }
            
            # 如果有Content-Length，也设置上
            if 'content-length' in page_resp.headers:
                response_headers['Content-Length'] = page_resp.headers['content-length']
            
            # 流式返回文件内容
            def generate():
                for chunk in page_resp.iter_content(chunk_size=8192):
                    if chunk:
                        yield chunk
            
            from flask import Response
            return Response(generate(), headers=response_headers)
        else:
            return jsonify({
                "error": f"下载页面失败: {page_resp.status_code}",
                "status": "error"
            }), 400
            
    except Exception as e:
        print(f"❌ 下载PDF页面时出错: {str(e)}")
        return jsonify({
            "error": f"下载PDF页面失败: {str(e)}",
            "status": "error"
        }), 500
