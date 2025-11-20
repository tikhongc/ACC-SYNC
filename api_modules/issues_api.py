# -*- coding: utf-8 -*-
"""
Issues API 模块
处理 Autodesk Construction Cloud (ACC) Issues API 的功能
支持议题的即时同步、获取详细信息、留言和附件等操作
"""

import requests
import json
import time
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
import config
import utils
from .urn_download_simple import get_document_info_by_urn

issues_bp = Blueprint('issues', __name__)

# 配置常量 - 基于性能测试结果
DEFAULT_ISSUES_LIMIT = 50  # 最佳性能值（测试结果：24秒响应）
MAX_ISSUES_LIMIT = 100     # API 最大支持值
BATCH_SIZE = 50            # 批量处理大小


def normalize_project_id(project_id):
    """
    移除项目ID中的 'b.' 前缀（如果存在）
    ACC Issues API 需要不带前缀的项目ID
    
    Args:
        project_id (str): 项目ID（可能包含 'b.' 前缀）
    
    Returns:
        str: 清理后的项目ID
    """
    return project_id.replace("b.", "") if project_id.startswith("b.") else project_id


def enhance_linked_documents(linked_documents, project_id, access_token=None):
    """
    增强linkedDocuments信息，通过URN获取具体的文件名称和详细信息
    
    Args:
        linked_documents (list): 原始linkedDocuments数据
        project_id (str): 项目ID
        access_token (str): 访问令牌
    
    Returns:
        list: 增强后的linkedDocuments数据
    """
    if not linked_documents or not isinstance(linked_documents, list):
        return linked_documents
    
    if not access_token:
        access_token = utils.get_access_token()
    
    if not access_token:
        print("⚠️ 无法获取访问令牌，跳过linkedDocuments增强")
        return linked_documents
    
    enhanced_documents = []
    
    for doc in linked_documents:
        try:
            # 保留原始数据
            enhanced_doc = doc.copy()
            
            # 获取URN
            urn = doc.get('urn')
            if not urn:
                print(f"⚠️ linkedDocument缺少URN: {doc}")
                enhanced_documents.append(enhanced_doc)
                continue
            
            print(f"🔍 增强linkedDocument URN: {urn}")
            
            # 通过URN获取文档详细信息
            doc_info_result = get_document_info_by_urn(urn, project_id, access_token)
            
            if doc_info_result and doc_info_result.get('success'):
                doc_info = doc_info_result.get('document_info', {})
                
                # 增强文档信息
                enhanced_doc['enhanced_info'] = {
                    'name': doc_info.get('name', 'Unknown Document'),
                    'file_type': doc_info.get('file_type', 'unknown'),
                    'file_size': doc_info.get('file_size', 0),
                    'mime_type': doc_info.get('mime_type', 'application/octet-stream'),
                    'version_number': doc_info.get('version_number', 1),
                    'create_time': doc_info.get('create_time'),
                    'last_modified_time': doc_info.get('last_modified_time'),
                    'storage_urn': doc_info.get('storage_urn'),
                    'enhanced_at': datetime.now().isoformat()
                }
                
                # 为了向后兼容，也在根级别添加name字段
                if not enhanced_doc.get('name'):
                    enhanced_doc['name'] = doc_info.get('name', 'Unknown Document')
                
                print(f"✅ 成功增强文档信息: {doc_info.get('name')}")
            else:
                # 如果无法获取详细信息，添加基本的增强信息
                enhanced_doc['enhanced_info'] = {
                    'name': 'Unknown Document',
                    'file_type': 'unknown',
                    'file_size': 0,
                    'mime_type': 'application/octet-stream',
                    'version_number': 1,
                    'create_time': None,
                    'last_modified_time': None,
                    'storage_urn': urn,
                    'enhanced_at': datetime.now().isoformat(),
                    'error': doc_info_result.get('error') if doc_info_result else 'Failed to get document info'
                }
                
                if not enhanced_doc.get('name'):
                    enhanced_doc['name'] = 'Unknown Document'
                
                print(f"⚠️ 无法获取文档详细信息: {doc_info_result.get('error') if doc_info_result else 'Unknown error'}")
            
            enhanced_documents.append(enhanced_doc)
            
        except Exception as e:
            print(f"❌ 增强linkedDocument时出错: {str(e)}")
            # 出错时保留原始数据
            enhanced_documents.append(doc)
    
    return enhanced_documents


def calculate_quick_statistics(issues):
    """
    基于当前议题数据快速计算统计信息
    避免重复API调用，提高性能
    
    Args:
        issues (list): 议题列表
    
    Returns:
        dict: 快速统计信息
    """
    if not issues:
        return {
            "total_issues": 0,
            "status_breakdown": {},
            "assignee_type_breakdown": {},
            "recent_activity": 0,
            "note": "Quick statistics based on current page data"
        }
    
    stats = {
        "total_issues": len(issues),
        "status_breakdown": {},
        "assignee_type_breakdown": {},
        "recent_activity": 0,
        "note": f"基于当前 {len(issues)} 个议题的快速统计"
    }
    
    # 统计状态分布
    for issue in issues:
        status = issue.get('status', 'unknown')
        stats['status_breakdown'][status] = stats['status_breakdown'].get(status, 0) + 1
        
        # 统计分配类型
        assigned_type = issue.get('assignedToType', 'unassigned')
        if not issue.get('assignedTo'):
            assigned_type = 'unassigned'
        stats['assignee_type_breakdown'][assigned_type] = stats['assignee_type_breakdown'].get(assigned_type, 0) + 1
        
        # 统计最近活动（24小时内更新的议题）
        if issue.get('updatedAt'):
            try:
                updated_time = datetime.fromisoformat(issue['updatedAt'].replace('Z', '+00:00'))
                if (datetime.now().replace(tzinfo=updated_time.tzinfo) - updated_time).days < 1:
                    stats['recent_activity'] += 1
            except:
                pass
    
    return stats


def get_user_profile(project_id, headers):
    """
    获取当前用户档案和权限
    
    Args:
        project_id (str): 项目ID
        headers (dict): 请求头
    
    Returns:
        dict: 用户档案信息
    """
    try:
        # 规范化项目ID（移除 'b.' 前缀）
        project_id = normalize_project_id(project_id)
        user_url = f"{config.AUTODESK_API_BASE}/construction/issues/v1/projects/{project_id}/users/me"
        
        print(f"🔍 获取用户档案: {project_id}")
        
        response = requests.get(user_url, headers=headers, timeout=(10, 30))
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ 成功获取用户档案")
            return {
                "success": True,
                "data": user_data
            }
        else:
            print(f"❌ 获取用户档案失败: {response.status_code} - {response.text}")
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}",
                "status_code": response.status_code
            }
            
    except Exception as e:
        print(f"❌ 获取用户档案时出错: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


def get_issue_types(project_id, headers, include_subtypes=False, filters=None, pagination=None):
    """
    获取项目的议题类型（类别和子类型）
    
    Args:
        project_id (str): 项目ID
        headers (dict): 请求头
        include_subtypes (bool): 是否包含子类型
        filters (dict): 过滤条件
        pagination (dict): 分页参数
    
    Returns:
        dict: 议题类型数据
    """
    try:
        # 规范化项目ID（移除 'b.' 前缀）
        project_id = normalize_project_id(project_id)
        types_url = f"{config.AUTODESK_API_BASE}/construction/issues/v1/projects/{project_id}/issue-types"
        
        # 构建查询参数
        params = {}
        
        if include_subtypes:
            params['include'] = 'subtypes'
        
        # 添加过滤条件
        if filters:
            if filters.get('updatedAt'):
                params['filter[updatedAt]'] = filters['updatedAt']
            if filters.get('isActive') is not None:
                params['filter[isActive]'] = str(filters['isActive']).lower()
        
        # 添加分页参数
        if pagination:
            if pagination.get('limit'):
                params['limit'] = pagination['limit']
            if pagination.get('offset'):
                params['offset'] = pagination['offset']
        
        print(f"🔍 获取议题类型: {project_id}")
        
        response = requests.get(types_url, headers=headers, params=params, timeout=(10, 30))
        
        if response.status_code == 200:
            types_data = response.json()
            print(f"✅ 成功获取 {len(types_data.get('results', []))} 个议题类型")
            return {
                "success": True,
                "data": types_data
            }
        else:
            print(f"❌ 获取议题类型失败: {response.status_code} - {response.text}")
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}",
                "status_code": response.status_code
            }
            
    except Exception as e:
        print(f"❌ 获取议题类型时出错: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


def get_attribute_definitions(project_id, headers, filters=None, pagination=None):
    """
    获取议题自定义属性定义（自定义字段）
    
    Args:
        project_id (str): 项目ID
        headers (dict): 请求头
        filters (dict): 过滤条件
        pagination (dict): 分页参数
    
    Returns:
        dict: 属性定义数据
    """
    try:
        # 规范化项目ID（移除 'b.' 前缀）
        project_id = normalize_project_id(project_id)
        attrs_url = f"{config.AUTODESK_API_BASE}/construction/issues/v1/projects/{project_id}/issue-attribute-definitions"
        
        # 构建查询参数
        params = {}
        
        # 添加过滤条件
        if filters:
            if filters.get('createdAt'):
                params['filter[createdAt]'] = filters['createdAt']
            if filters.get('updatedAt'):
                params['filter[updatedAt]'] = filters['updatedAt']
            if filters.get('deletedAt'):
                params['filter[deletedAt]'] = filters['deletedAt']
            if filters.get('dataType'):
                params['filter[dataType]'] = filters['dataType']
        
        # 添加分页参数
        if pagination:
            if pagination.get('limit'):
                params['limit'] = pagination['limit']
            if pagination.get('offset'):
                params['offset'] = pagination['offset']
        else:
            params['limit'] = 200  # 默认最大值
        
        print(f"🔍 获取议题属性定义: {project_id}")
        
        response = requests.get(attrs_url, headers=headers, params=params, timeout=(10, 30))
        
        if response.status_code == 200:
            attrs_data = response.json()
            print(f"✅ 成功获取 {len(attrs_data.get('results', []))} 个属性定义")
            return {
                "success": True,
                "data": attrs_data
            }
        else:
            print(f"❌ 获取属性定义失败: {response.status_code} - {response.text}")
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}",
                "status_code": response.status_code
            }
            
    except Exception as e:
        print(f"❌ 获取属性定义时出错: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


def get_attribute_mappings(project_id, headers, filters=None, pagination=None):
    """
    获取议题自定义属性映射（字段分配到类型）
    
    Args:
        project_id (str): 项目ID
        headers (dict): 请求头
        filters (dict): 过滤条件
        pagination (dict): 分页参数
    
    Returns:
        dict: 属性映射数据
    """
    try:
        # 规范化项目ID（移除 'b.' 前缀）
        project_id = normalize_project_id(project_id)
        mappings_url = f"{config.AUTODESK_API_BASE}/construction/issues/v1/projects/{project_id}/issue-attribute-mappings"
        
        # 构建查询参数
        params = {}
        
        # 添加过滤条件
        if filters:
            if filters.get('createdAt'):
                params['filter[createdAt]'] = filters['createdAt']
            if filters.get('updatedAt'):
                params['filter[updatedAt]'] = filters['updatedAt']
            if filters.get('deletedAt'):
                params['filter[deletedAt]'] = filters['deletedAt']
            if filters.get('attributeDefinitionId'):
                params['filter[attributeDefinitionId]'] = filters['attributeDefinitionId']
            if filters.get('mappedItemId'):
                params['filter[mappedItemId]'] = filters['mappedItemId']
        
        # 添加分页参数
        if pagination:
            if pagination.get('limit'):
                params['limit'] = pagination['limit']
            if pagination.get('offset'):
                params['offset'] = pagination['offset']
        else:
            params['limit'] = 200  # 默认最大值
        
        print(f"🔍 获取议题属性映射: {project_id}")
        
        response = requests.get(mappings_url, headers=headers, params=params, timeout=(10, 30))
        
        if response.status_code == 200:
            mappings_data = response.json()
            print(f"✅ 成功获取 {len(mappings_data.get('results', []))} 个属性映射")
            return {
                "success": True,
                "data": mappings_data
            }
        else:
            print(f"❌ 获取属性映射失败: {response.status_code} - {response.text}")
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}",
                "status_code": response.status_code
            }
            
    except Exception as e:
        print(f"❌ 获取属性映射时出错: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


def get_root_cause_categories(project_id, headers, include_root_causes=False, filters=None, pagination=None):
    """
    获取议题根本原因类别
    
    Args:
        project_id (str): 项目ID
        headers (dict): 请求头
        include_root_causes (bool): 是否包含根本原因详情
        filters (dict): 过滤条件
        pagination (dict): 分页参数
    
    Returns:
        dict: 根本原因类别数据
    """
    try:
        # 规范化项目ID（移除 'b.' 前缀）
        project_id = normalize_project_id(project_id)
        root_causes_url = f"{config.AUTODESK_API_BASE}/construction/issues/v1/projects/{project_id}/issue-root-cause-categories"
        
        # 构建查询参数
        params = {}
        
        if include_root_causes:
            params['include'] = 'rootcauses'
        
        # 添加过滤条件
        if filters:
            if filters.get('updatedAt'):
                params['filter[updatedAt]'] = filters['updatedAt']
        
        # 添加分页参数
        if pagination:
            if pagination.get('limit'):
                params['limit'] = pagination['limit']
            if pagination.get('offset'):
                params['offset'] = pagination['offset']
        
        print(f"🔍 获取根本原因类别: {project_id}")
        
        response = requests.get(root_causes_url, headers=headers, params=params, timeout=(10, 30))
        
        if response.status_code == 200:
            root_causes_data = response.json()
            print(f"✅ 成功获取 {len(root_causes_data.get('results', []))} 个根本原因类别")
            return {
                "success": True,
                "data": root_causes_data
            }
        else:
            print(f"❌ 获取根本原因类别失败: {response.status_code} - {response.text}")
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}",
                "status_code": response.status_code
            }
            
    except Exception as e:
        print(f"❌ 获取根本原因类别时出错: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


def get_markups(container_id, headers, filters=None, pagination=None, sort=None):
    """
    获取项目中的标记（Markups）
    
    Args:
        container_id (str): 容器ID
        headers (dict): 请求头
        filters (dict): 过滤条件
        pagination (dict): 分页参数
        sort (str): 排序字段
    
    Returns:
        dict: 标记数据
    """
    try:
        markups_url = f"https://developer.api.autodesk.com/issues/v1/containers/{container_id}/markups"
        
        # 构建查询参数
        params = {}
        
        # 添加过滤条件
        if filters:
            if filters.get('target_urn'):
                params['filter[target_urn]'] = filters['target_urn']
            if filters.get('synced_after'):
                params['filter[synced_after]'] = filters['synced_after']
            if filters.get('created_at'):
                params['filter[created_at]'] = filters['created_at']
            if filters.get('created_by'):
                params['filter[created_by]'] = filters['created_by']
            if filters.get('status'):
                params['filter[status]'] = filters['status']
        
        # 添加分页参数
        if pagination:
            if pagination.get('limit'):
                params['page[limit]'] = pagination['limit']
            if pagination.get('offset'):
                params['page[offset]'] = pagination['offset']
        else:
            params['page[limit]'] = 10  # 默认值
        
        # 添加排序
        if sort:
            params['sort'] = sort
        
        # 修改headers以符合Markups API要求
        markups_headers = headers.copy()
        markups_headers['Content-Type'] = 'application/vnd.api+json'
        
        print(f"🔍 获取标记: {container_id}")
        
        response = requests.get(markups_url, headers=markups_headers, params=params, timeout=(10, 30))
        
        if response.status_code == 200:
            markups_data = response.json()
            print(f"✅ 成功获取标记数据")
            return {
                "success": True,
                "data": markups_data
            }
        else:
            print(f"❌ 获取标记失败: {response.status_code} - {response.text}")
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}",
                "status_code": response.status_code
            }
            
    except Exception as e:
        print(f"❌ 获取标记时出错: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


def get_issues_list(project_id, headers, filters=None, pagination=None, max_retries=3):
    """
    获取项目中的议题列表 - 带重试机制和超时优化
    
    Args:
        project_id (str): 项目ID
        headers (dict): 请求头
        filters (dict): 过滤条件
        pagination (dict): 分页参数
        max_retries (int): 最大重试次数 (默认3次)
    
    Returns:
        dict: 议题列表数据
    """
    # 规范化项目ID（移除 'b.' 前缀）
    project_id = normalize_project_id(project_id)
    # 构建API URL
    issues_url = f"{config.AUTODESK_API_BASE}/construction/issues/v1/projects/{project_id}/issues"
    
    # 构建查询参数
    params = {}
    
    # 添加过滤条件
    if filters:
        if filters.get('status'):
            params['filter[status]'] = filters['status']
        if filters.get('assignedTo'):
            params['filter[assignedTo]'] = filters['assignedTo']
        if filters.get('issueTypeId'):
            params['filter[issueTypeId]'] = filters['issueTypeId']
        if filters.get('createdBy'):
            params['filter[createdBy]'] = filters['createdBy']
        if filters.get('updatedSince'):
            params['filter[updatedAt][gte]'] = filters['updatedSince']
        if filters.get('createdSince'):
            params['filter[createdAt][gte]'] = filters['createdSince']
        if filters.get('dueDate'):
            params['filter[dueDate]'] = filters['dueDate']
        if filters.get('linkedDocumentUrn'):
            params['filter[linkedDocumentUrn]'] = filters['linkedDocumentUrn']
    
    # 添加分页参数，如果请求超过100条，自动分页
    if pagination:
        requested_limit = pagination.get('limit', DEFAULT_ISSUES_LIMIT)
        params['limit'] = min(requested_limit, MAX_ISSUES_LIMIT)  # API最大支持100条/次
        if pagination.get('offset'):
            params['offset'] = pagination['offset']
    else:
        params['limit'] = DEFAULT_ISSUES_LIMIT  # 默认限制：50（最佳性能）
    
    print(f"🔍 获取议题列表: {project_id}")
    print(f"📋 查询参数: {params}")
    
    # 重试机制 - 针对504超时错误
    for attempt in range(max_retries):
        try:
            # 增加超时时间：连接15秒，读取60秒
            response = requests.get(issues_url, headers=headers, params=params, timeout=(15, 60))
            
            if response.status_code == 200:
                issues_data = response.json()
                results = issues_data.get('results', [])
                print(f"✅ 成功获取 {len(results)} 个议题")
                
                # 如果需要获取更多数据（超过100条），自动分页获取
                if pagination and pagination.get('limit', 0) > 100:
                    return get_issues_list_paginated(project_id, headers, filters, pagination, max_retries)
                
                return {
                    "success": True,
                    "data": issues_data,
                    "total_count": len(results),
                    "has_more": len(results) == params.get('limit', 100)
                }
            elif response.status_code == 504:
                # Gateway Timeout - 需要重试
                print(f"⏰ 尝试 {attempt + 1}/{max_retries}: API网关超时 (504)")
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 2  # 指数退避: 2s, 4s, 8s
                    print(f"⏳ 等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                    continue
                else:
                    return {
                        "success": False,
                        "error": "API网关超时，请稍后重试或减少请求数据量",
                        "status_code": 504,
                        "retry_suggestion": "建议减少 limit 参数（如设为50）或稍后再试"
                    }
            elif response.status_code == 429:
                # Rate Limit - 需要等待
                print(f"⏰ 尝试 {attempt + 1}/{max_retries}: API请求频率限制 (429)")
                if attempt < max_retries - 1:
                    wait_time = 5 * (attempt + 1)  # 5s, 10s, 15s
                    print(f"⏳ 遇到频率限制，等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                    continue
                else:
                    return {
                        "success": False,
                        "error": "API请求频率超限，请稍后重试",
                        "status_code": 429
                    }
            else:
                print(f"❌ 获取议题列表失败: {response.status_code} - {response.text}")
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "status_code": response.status_code
                }
                
        except requests.exceptions.Timeout:
            print(f"⏰ 尝试 {attempt + 1}/{max_retries}: 请求超时")
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) * 2
                print(f"⏳ 等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
                continue
            else:
                return {
                    "success": False,
                    "error": "请求超时，服务器响应时间过长",
                    "status_code": 408,
                    "retry_suggestion": "建议减少 limit 参数（如设为50）或稍后再试"
                }
        except Exception as e:
            print(f"❌ 获取议题列表时出错: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    # 如果所有重试都失败
    return {
        "success": False,
        "error": "All retry attempts failed",
        "status_code": 500
    }


def get_issues_list_paginated(project_id, headers, filters=None, pagination=None, max_retries=3):
    """
    自动分页获取议题列表（用于大量数据请求）
    
    Args:
        project_id (str): 项目ID
        headers (dict): 请求头
        filters (dict): 过滤条件 (可选)
        pagination (dict): 分页参数 (必须包含limit)
        max_retries (int): 每次请求的最大重试次数
    
    Returns:
        dict: 合并后的议题列表数据
    """
    try:
        requested_limit = pagination.get('limit', 100)
        all_results = []
        offset = pagination.get('offset', 0)
        
        print(f"📄 开始分页获取议题，目标: {requested_limit} 条，起始偏移: {offset}")
        
        while len(all_results) < requested_limit:
            # 计算本次请求的数量（最多100条）
            remaining = requested_limit - len(all_results)
            current_limit = min(remaining, 100)
            
            # 构建本次请求的分页参数
            current_pagination = {
                'limit': current_limit,
                'offset': offset + len(all_results)
            }
            
            # 获取本批数据
            result = get_issues_list(project_id, headers, filters, current_pagination, max_retries)
            
            if not result['success']:
                # 如果失败但已经获取了部分数据，返回部分数据
                if all_results:
                    print(f"⚠️ 部分获取成功，返回已获取的 {len(all_results)} 条数据")
                    return {
                        "success": True,
                        "data": {"results": all_results},
                        "total_count": len(all_results),
                        "has_more": True,
                        "partial": True,
                        "warning": f"未能获取全部数据: {result.get('error')}"
                    }
                else:
                    return result
            
            batch_results = result['data'].get('results', [])
            all_results.extend(batch_results)
            
            print(f"📊 已获取 {len(all_results)}/{requested_limit} 条议题")
            
            # 如果本批数据少于请求数量，说明没有更多数据了
            if len(batch_results) < current_limit:
                print(f"✅ 已获取所有可用数据: {len(all_results)} 条")
                break
        
        return {
            "success": True,
            "data": {"results": all_results},
            "total_count": len(all_results),
            "has_more": len(all_results) == requested_limit
        }
        
    except Exception as e:
        print(f"❌ 分页获取议题时出错: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


def get_issue_details(project_id, issue_id, headers, enhance_documents=True):
    """
    获取单一议题的详细信息
    
    Args:
        project_id (str): 项目ID
        issue_id (str): 议题ID
        headers (dict): 请求头
        enhance_documents (bool): 是否增强linkedDocuments信息
    
    Returns:
        dict: 议题详细信息
    """
    try:
        # 规范化项目ID（移除 'b.' 前缀）
        normalized_project_id = normalize_project_id(project_id)
        issue_url = f"{config.AUTODESK_API_BASE}/construction/issues/v1/projects/{normalized_project_id}/issues/{issue_id}"
        
        print(f"🔍 获取议题详情: {issue_id}")
        
        response = requests.get(issue_url, headers=headers, timeout=(10, 30))
        
        if response.status_code == 200:
            issue_data = response.json()
            print(f"✅ 成功获取议题详情: {issue_data.get('title', 'Unknown')}")
            
            # 增强linkedDocuments信息
            if enhance_documents and issue_data.get('linkedDocuments'):
                print(f"🔧 开始增强linkedDocuments信息...")
                access_token = headers.get('Authorization', '').replace('Bearer ', '')
                enhanced_linked_docs = enhance_linked_documents(
                    issue_data['linkedDocuments'], 
                    project_id,  # 使用原始project_id（可能包含b.前缀）
                    access_token
                )
                issue_data['linkedDocuments'] = enhanced_linked_docs
                print(f"✅ linkedDocuments增强完成")
            
            return {
                "success": True,
                "data": issue_data
            }
        else:
            print(f"❌ 获取议题详情失败: {response.status_code} - {response.text}")
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}",
                "status_code": response.status_code
            }
            
    except Exception as e:
        print(f"❌ 获取议题详情时出错: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


def get_issue_comments(project_id, issue_id, headers, pagination=None):
    """
    获取议题的留言
    
    Args:
        project_id (str): 项目ID
        issue_id (str): 议题ID
        headers (dict): 请求头
        pagination (dict): 分页参数
    
    Returns:
        dict: 留言数据
    """
    try:
        # 规范化项目ID（移除 'b.' 前缀）
        project_id = normalize_project_id(project_id)
        comments_url = f"{config.AUTODESK_API_BASE}/construction/issues/v1/projects/{project_id}/issues/{issue_id}/comments"
        
        # 构建查询参数
        params = {}
        if pagination:
            if pagination.get('limit'):
                params['limit'] = pagination['limit']
            if pagination.get('offset'):
                params['offset'] = pagination['offset']
        else:
            params['limit'] = 50  # 默认限制
        
        # 注意: 如果 API 支持 sort，可以添加 params['sort'] = 'createdAt'
        
        print(f"🔍 获取议题留言: {issue_id}")
        
        response = requests.get(comments_url, headers=headers, params=params, timeout=(10, 30))
        
        if response.status_code == 200:
            comments_data = response.json()
            print(f"✅ 成功获取 {len(comments_data.get('results', []))} 条留言")
            return {
                "success": True,
                "data": comments_data,
                "total_count": len(comments_data.get('results', []))
            }
        else:
            print(f"❌ 获取议题留言失败: {response.status_code} - {response.text}")
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}",
                "status_code": response.status_code
            }
            
    except Exception as e:
        print(f"❌ 获取议题留言时出错: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


def get_issue_attachments(project_id, issue_id, headers):
    """
    获取议题的附件
    
    Args:
        project_id (str): 项目ID
        issue_id (str): 议题ID
        headers (dict): 请求头
    
    Returns:
        dict: 附件数据
    """
    try:
        # 规范化项目ID（移除 'b.' 前缀）
        project_id = normalize_project_id(project_id)
        attachments_url = f"{config.AUTODESK_API_BASE}/construction/issues/v1/projects/{project_id}/attachments/{issue_id}/items"
        
        print(f"🔍 获取议题附件: {issue_id}")
        
        response = requests.get(attachments_url, headers=headers, timeout=(10, 30))
        
        if response.status_code == 200:
            attachments_data = response.json()
            # Autodesk Issues API 返回的附件數據在 'attachments' 字段中，而不是 'results'
            attachments_list = attachments_data.get('attachments', [])
            print(f"✅ 成功获取 {len(attachments_list)} 个附件")
            
            # 為了保持與前端的兼容性，將數據格式化為期望的結構
            formatted_response = {
                "results": attachments_list,
                "pagination": attachments_data.get('pagination', {}),
                "raw_data": attachments_data  # 保留原始數據供調試
            }
            
            return {
                "success": True,
                "data": formatted_response,
                "total_count": len(attachments_list)
            }
        else:
            print(f"❌ 获取议题附件失败: {response.status_code} - {response.text}")
            return {
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}",
                "status_code": response.status_code
            }
            
    except Exception as e:
        print(f"❌ 获取议题附件时出错: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


def sync_issues_incremental(project_id, headers, last_sync_time=None, batch_size=100):
    """
    增量同步议题数据
    
    Args:
        project_id (str): 项目ID
        headers (dict): 请求头
        last_sync_time (str): 上次同步时间 (ISO格式)
        batch_size (int): 批次大小
    
    Returns:
        dict: 同步结果
    """
    try:
        # 规范化项目ID（移除 'b.' 前缀）
        project_id = normalize_project_id(project_id)
        print(f"🔄 开始增量同步议题: {project_id}")
        
        # 如果没有指定上次同步时间，使用24小时前
        if not last_sync_time:
            last_sync_time = (datetime.now() - timedelta(hours=24)).isoformat()
        
        print(f"📅 同步时间范围: {last_sync_time} 至今")
        
        # 设置过滤条件 - 获取指定时间后更新的议题
        filters = {
            'updatedSince': last_sync_time
        }
        
        all_issues = []
        offset = 0
        has_more = True
        
        while has_more:
            pagination = {
                'limit': batch_size,
                'offset': offset
            }
            
            # 获取议题列表
            result = get_issues_list(project_id, headers, filters, pagination)
            
            if not result['success']:
                return {
                    "success": False,
                    "error": f"获取议题列表失败: {result['error']}"
                }
            
            issues_batch = result['data'].get('results', [])
            all_issues.extend(issues_batch)
            
            # 检查是否还有更多数据
            has_more = result.get('has_more', False) and len(issues_batch) == batch_size
            offset += batch_size
            
            print(f"📋 已获取 {len(all_issues)} 个更新的议题")
        
        # 为每个议题获取详细信息（可选）
        enhanced_issues = []
        for issue in all_issues:
            issue_id = issue.get('id')
            if issue_id:
                # 获取议题详情
                details_result = get_issue_details(project_id, issue_id, headers)
                if details_result['success']:
                    enhanced_issue = details_result['data']
                    
                    # 获取留言数量（不获取具体内容以提高性能）
                    comments_result = get_issue_comments(project_id, issue_id, headers, {'limit': 1})
                    if comments_result['success']:
                        enhanced_issue['comments_available'] = comments_result['total_count'] > 0
                    
                    # 获取附件数量
                    attachments_result = get_issue_attachments(project_id, issue_id, headers)
                    if attachments_result['success']:
                        enhanced_issue['attachments_available'] = attachments_result['total_count'] > 0
                        enhanced_issue['attachments_count'] = attachments_result['total_count']
                    
                    enhanced_issues.append(enhanced_issue)
                else:
                    # 如果无法获取详情，使用原始数据
                    enhanced_issues.append(issue)
        
        sync_result = {
            "success": True,
            "sync_time": datetime.now().isoformat(),
            "last_sync_time": last_sync_time,
            "total_issues": len(enhanced_issues),
            "issues": enhanced_issues,
            "statistics": {
                "new_issues": 0,
                "updated_issues": len(enhanced_issues),
                "closed_issues": 0
            }
        }
        
        # 分析议题状态统计
        status_counts = {}
        for issue in enhanced_issues:
            status = issue.get('status', 'unknown')
            status_counts[status] = status_counts.get(status, 0) + 1
        
        sync_result['statistics']['status_breakdown'] = status_counts
        
        print(f"✅ 增量同步完成: {len(enhanced_issues)} 个议题")
        return sync_result
        
    except Exception as e:
        print(f"❌ 增量同步议题时出错: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


# API 路由定义

@issues_bp.route('/api/issues/projects/<project_id>/list')
def get_issues_list_api(project_id):
    """获取项目议题列表的API端点"""
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
        start_time = time.time()
        print(f"🚀 [优化] 获取议题列表: {project_id}")
        
        # 获取查询参数
        filters = {}
        if request.args.get('status'):
            filters['status'] = request.args.get('status')
        if request.args.get('assignedTo'):
            filters['assignedTo'] = request.args.get('assignedTo')
        if request.args.get('issueTypeId'):
            filters['issueTypeId'] = request.args.get('issueTypeId')
        if request.args.get('updatedSince'):
            filters['updatedSince'] = request.args.get('updatedSince')
        if request.args.get('createdSince'):
            filters['createdSince'] = request.args.get('createdSince')
        
        # 优化：限制默认请求量，提高响应速度
        requested_limit = request.args.get('limit', DEFAULT_ISSUES_LIMIT, type=int)
        if requested_limit > 100:
            print(f"⚠️ 请求量过大 ({requested_limit})，限制为100以提高性能")
            requested_limit = 100
            
        pagination = {
            'limit': requested_limit,
            'offset': request.args.get('offset', 0, type=int)
        }
        
        # 是否包含统计信息
        include_stats = request.args.get('include_stats', 'true').lower() == 'true'
        
        result = get_issues_list(project_id, headers, filters, pagination)
        
        if result['success']:
            response_data = {
                "status": "success",
                "project_id": project_id,
                "data": result['data'],
                "pagination": {
                    "limit": pagination['limit'],
                    "offset": pagination['offset'],
                    "has_more": result.get('has_more', False)
                },
                "response_time_seconds": round(time.time() - start_time, 2)
            }
            
            # 优化：基于当前数据计算快速统计信息，避免重复API调用
            if include_stats:
                issues = result['data'].get('results', [])
                quick_stats = calculate_quick_statistics(issues)
                response_data['quick_statistics'] = quick_stats
                print(f"✅ 包含快速统计信息: {len(issues)} 个议题")
            
            print(f"✅ [优化] 议题列表获取完成: {len(result['data'].get('results', []))} 个议题，耗时: {response_data['response_time_seconds']}s")
            
            return jsonify(response_data)
        else:
            return jsonify({
                "status": "error",
                "error": result['error'],
                "project_id": project_id,
                "response_time_seconds": round(time.time() - start_time, 2)
            }), result.get('status_code', 500)
            
    except Exception as e:
        print(f"❌ 议题列表API出错: {str(e)}")
        return jsonify({
            "status": "error",
            "error": f"获取议题列表失败: {str(e)}"
        }), 500


@issues_bp.route('/api/issues/projects/<project_id>/issues/<issue_id>')
def get_issue_details_api(project_id, issue_id):
    """获取单一议题详细信息的API端点"""
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
        # 检查是否需要增强linkedDocuments信息
        enhance_documents = request.args.get('enhanceDocuments', 'true').lower() == 'true'
        
        result = get_issue_details(project_id, issue_id, headers, enhance_documents)
        
        if result['success']:
            response_data = {
                "status": "success",
                "project_id": project_id,
                "issue_id": issue_id,
                "data": result['data']
            }
            
            # 如果启用了文档增强，添加相关信息
            if enhance_documents:
                linked_docs = result['data'].get('linkedDocuments', [])
                enhanced_count = sum(1 for doc in linked_docs if doc.get('enhanced_info'))
                response_data['enhancement_info'] = {
                    'documents_enhanced': enhanced_count,
                    'total_documents': len(linked_docs),
                    'enhancement_enabled': True
                }
            else:
                response_data['enhancement_info'] = {
                    'enhancement_enabled': False
                }
            
            return jsonify(response_data)
        else:
            return jsonify({
                "status": "error",
                "error": result['error'],
                "project_id": project_id,
                "issue_id": issue_id
            }), result.get('status_code', 500)
            
    except Exception as e:
        print(f"❌ 议题详情API出错: {str(e)}")
        return jsonify({
            "status": "error",
            "error": f"获取议题详情失败: {str(e)}"
        }), 500


@issues_bp.route('/api/issues/projects/<project_id>/issues/<issue_id>/comments')
def get_issue_comments_api(project_id, issue_id):
    """获取议题留言的API端点"""
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
        # 分页参数
        pagination = {
            'limit': request.args.get('limit', 50, type=int),
            'offset': request.args.get('offset', 0, type=int)
        }
        
        result = get_issue_comments(project_id, issue_id, headers, pagination)
        
        if result['success']:
            return jsonify({
                "status": "success",
                "project_id": project_id,
                "issue_id": issue_id,
                "data": result['data'],
                "pagination": pagination
            })
        else:
            return jsonify({
                "status": "error",
                "error": result['error'],
                "project_id": project_id,
                "issue_id": issue_id
            }), result.get('status_code', 500)
            
    except Exception as e:
        print(f"❌ 议题留言API出错: {str(e)}")
        return jsonify({
            "status": "error",
            "error": f"获取议题留言失败: {str(e)}"
        }), 500


@issues_bp.route('/api/issues/projects/<project_id>/issues/<issue_id>/attachments')
def get_issue_attachments_api(project_id, issue_id):
    """获取议题附件的API端点"""
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
        result = get_issue_attachments(project_id, issue_id, headers)
        
        if result['success']:
            return jsonify({
                "status": "success",
                "project_id": project_id,
                "issue_id": issue_id,
                "data": result['data']
            })
        else:
            return jsonify({
                "status": "error",
                "error": result['error'],
                "project_id": project_id,
                "issue_id": issue_id
            }), result.get('status_code', 500)
            
    except Exception as e:
        print(f"❌ 议题附件API出错: {str(e)}")
        return jsonify({
            "status": "error",
            "error": f"获取议题附件失败: {str(e)}"
        }), 500


@issues_bp.route('/api/issues/projects/<project_id>/sync')
def sync_issues_api(project_id):
    """增量同步议题的API端点"""
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
        # 获取同步参数
        last_sync_time = request.args.get('lastSyncTime')
        batch_size = request.args.get('batchSize', 100, type=int)
        include_details = request.args.get('includeDetails', 'true').lower() == 'true'
        
        print(f"🔄 开始同步议题 - 项目: {project_id}, 上次同步: {last_sync_time}")
        
        result = sync_issues_incremental(project_id, headers, last_sync_time, batch_size)
        
        if result['success']:
            response_data = {
                "status": "success",
                "project_id": project_id,
                "sync_result": result
            }
            
            # 如果不需要详细信息，移除议题详情以减少响应大小
            if not include_details:
                simplified_issues = []
                for issue in result['issues']:
                    simplified_issue = {
                        'id': issue.get('id'),
                        'displayId': issue.get('displayId'),
                        'title': issue.get('title'),
                        'status': issue.get('status'),
                        'updatedAt': issue.get('updatedAt'),
                        'assignedTo': issue.get('assignedTo')
                    }
                    simplified_issues.append(simplified_issue)
                
                response_data['sync_result']['issues'] = simplified_issues
            
            return jsonify(response_data)
        else:
            return jsonify({
                "status": "error",
                "error": result['error'],
                "project_id": project_id
            }), 500
            
    except Exception as e:
        print(f"❌ 同步议题API出错: {str(e)}")
        return jsonify({
            "status": "error",
            "error": f"同步议题失败: {str(e)}"
        }), 500


@issues_bp.route('/api/issues/projects/<project_id>/user-profile')
def get_user_profile_api(project_id):
    """获取当前用户档案的API端点"""
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
        result = get_user_profile(project_id, headers)
        
        if result['success']:
            return jsonify({
                "status": "success",
                "project_id": project_id,
                "data": result['data']
            })
        else:
            return jsonify({
                "status": "error",
                "error": result['error'],
                "project_id": project_id
            }), result.get('status_code', 500)
            
    except Exception as e:
        print(f"❌ 用户档案API出错: {str(e)}")
        return jsonify({
            "status": "error",
            "error": f"获取用户档案失败: {str(e)}"
        }), 500


@issues_bp.route('/api/issues/projects/<project_id>/issue-types')
def get_issue_types_api(project_id):
    """获取议题类型的API端点"""
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
        include_subtypes = request.args.get('includeSubtypes', 'false').lower() == 'true'
        
        filters = {}
        if request.args.get('updatedAt'):
            filters['updatedAt'] = request.args.get('updatedAt')
        if request.args.get('isActive'):
            filters['isActive'] = request.args.get('isActive').lower() == 'true'
        
        pagination = {
            'limit': request.args.get('limit', 100, type=int),
            'offset': request.args.get('offset', 0, type=int)
        }
        
        result = get_issue_types(project_id, headers, include_subtypes, filters, pagination)
        
        if result['success']:
            return jsonify({
                "status": "success",
                "project_id": project_id,
                "data": result['data']
            })
        else:
            return jsonify({
                "status": "error",
                "error": result['error'],
                "project_id": project_id
            }), result.get('status_code', 500)
            
    except Exception as e:
        print(f"❌ 议题类型API出错: {str(e)}")
        return jsonify({
            "status": "error",
            "error": f"获取议题类型失败: {str(e)}"
        }), 500


@issues_bp.route('/api/issues/projects/<project_id>/attribute-definitions')
def get_attribute_definitions_api(project_id):
    """获取属性定义的API端点"""
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
        filters = {}
        if request.args.get('dataType'):
            filters['dataType'] = request.args.get('dataType')
        
        pagination = {
            'limit': request.args.get('limit', 200, type=int),
            'offset': request.args.get('offset', 0, type=int)
        }
        
        result = get_attribute_definitions(project_id, headers, filters, pagination)
        
        if result['success']:
            return jsonify({
                "status": "success",
                "project_id": project_id,
                "data": result['data']
            })
        else:
            return jsonify({
                "status": "error",
                "error": result['error'],
                "project_id": project_id
            }), result.get('status_code', 500)
            
    except Exception as e:
        print(f"❌ 属性定义API出错: {str(e)}")
        return jsonify({
            "status": "error",
            "error": f"获取属性定义失败: {str(e)}"
        }), 500


@issues_bp.route('/api/issues/projects/<project_id>/attribute-mappings')
def get_attribute_mappings_api(project_id):
    """获取属性映射的API端点"""
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
        filters = {}
        if request.args.get('attributeDefinitionId'):
            filters['attributeDefinitionId'] = request.args.get('attributeDefinitionId')
        if request.args.get('mappedItemId'):
            filters['mappedItemId'] = request.args.get('mappedItemId')
        
        pagination = {
            'limit': request.args.get('limit', 200, type=int),
            'offset': request.args.get('offset', 0, type=int)
        }
        
        result = get_attribute_mappings(project_id, headers, filters, pagination)
        
        if result['success']:
            return jsonify({
                "status": "success",
                "project_id": project_id,
                "data": result['data']
            })
        else:
            return jsonify({
                "status": "error",
                "error": result['error'],
                "project_id": project_id
            }), result.get('status_code', 500)
            
    except Exception as e:
        print(f"❌ 属性映射API出错: {str(e)}")
        return jsonify({
            "status": "error",
            "error": f"获取属性映射失败: {str(e)}"
        }), 500


@issues_bp.route('/api/issues/projects/<project_id>/root-cause-categories')
def get_root_cause_categories_api(project_id):
    """获取根本原因类别的API端点"""
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
        include_root_causes = request.args.get('includeRootCauses', 'false').lower() == 'true'
        
        pagination = {
            'limit': request.args.get('limit', 100, type=int),
            'offset': request.args.get('offset', 0, type=int)
        }
        
        result = get_root_cause_categories(project_id, headers, include_root_causes, None, pagination)
        
        if result['success']:
            return jsonify({
                "status": "success",
                "project_id": project_id,
                "data": result['data']
            })
        else:
            return jsonify({
                "status": "error",
                "error": result['error'],
                "project_id": project_id
            }), result.get('status_code', 500)
            
    except Exception as e:
        print(f"❌ 根本原因类别API出错: {str(e)}")
        return jsonify({
            "status": "error",
            "error": f"获取根本原因类别失败: {str(e)}"
        }), 500


@issues_bp.route('/api/issues/containers/<container_id>/markups')
def get_markups_api(container_id):
    """获取标记的API端点"""
    access_token = utils.get_access_token()
    if not access_token:
        return jsonify({
            "error": "未找到 Access Token，请先进行认证",
            "status": "unauthorized"
        }), 401
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/vnd.api+json"  # Required by Markups API
    }
    
    # Add x-user-id header for two-legged authentication as required by Markups API
    # This is critical for the API to work properly
    try:
        # Get user ID from user profile API
        user_resp = requests.get(
            f"{config.AUTODESK_API_BASE}/userprofile/v1/users/@me",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=(5, 10)
        )
        
        if user_resp.status_code == 200:
            user_data = user_resp.json()
            user_id = user_data.get('userId')
            if user_id:
                headers['x-user-id'] = user_id
                print(f"🔑 添加 x-user-id header: {user_id}")
            else:
                print("⚠️ 用户资料中未找到userId，可能影响Markups API访问")
        else:
            print(f"⚠️ 获取用户资料失败 ({user_resp.status_code})，可能影响Markups API访问")
    except Exception as e:
        print(f"⚠️ 获取用户ID时出错: {str(e)}")
        # Continue without x-user-id header
    
    try:
        filters = {}
        if request.args.get('target_urn'):
            filters['target_urn'] = request.args.get('target_urn')
        if request.args.get('status'):
            filters['status'] = request.args.get('status')
        if request.args.get('created_by'):
            filters['created_by'] = request.args.get('created_by')
        
        pagination = {
            'limit': request.args.get('limit', 10, type=int),
            'offset': request.args.get('offset', 0, type=int)
        }
        
        sort = request.args.get('sort')
        
        result = get_markups(container_id, headers, filters, pagination, sort)
        
        if result['success']:
            return jsonify({
                "status": "success",
                "container_id": container_id,
                "data": result['data']
            })
        else:
            return jsonify({
                "status": "error",
                "error": result['error'],
                "container_id": container_id
            }), result.get('status_code', 500)
            
    except Exception as e:
        print(f"❌ 标记API出错: {str(e)}")
        return jsonify({
            "status": "error",
            "error": f"获取标记失败: {str(e)}"
        }), 500


@issues_bp.route('/api/issues/projects/<project_id>/statistics')
def get_issues_statistics_api(project_id):
    """获取项目议题统计信息的API端点 - 优化版本"""
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
        start_time = time.time()
        print(f"📊 [优化] 获取议题统计信息: {project_id}")
        
        # 优化：检查是否需要完整统计
        full_stats = request.args.get('full', 'false').lower() == 'true'
        
        if not full_stats:
            # 快速模式：只获取第一页数据进行估算
            print("⚡ 使用快速统计模式")
            result = get_issues_list(project_id, headers, pagination={'limit': 100, 'offset': 0})
            
            if not result['success']:
                return jsonify({
                    "status": "error",
                    "error": result['error'],
                    "project_id": project_id
                }), result.get('status_code', 500)
            
            issues = result['data'].get('results', [])
            quick_stats = calculate_quick_statistics(issues)
            
            return jsonify({
                "status": "success",
                "project_id": project_id,
                "statistics": quick_stats,
                "mode": "quick",
                "response_time_seconds": round(time.time() - start_time, 2)
            })
        
        # 完整模式：获取所有数据（保留原有逻辑）
        print("🔄 使用完整统计模式（较慢）")
        all_issues = []
        offset = 0
        batch_size = BATCH_SIZE  # 使用 50 获得最佳性能
        
        while True:
            result = get_issues_list(project_id, headers, pagination={'limit': batch_size, 'offset': offset})
            
            if not result['success']:
                return jsonify({
                    "status": "error",
                    "error": result['error'],
                    "project_id": project_id,
                    "response_time_seconds": round(time.time() - start_time, 2)
                }), result.get('status_code', 500)
            
            batch_issues = result['data'].get('results', [])
            if not batch_issues:
                break  # 没有更多数据
                
            all_issues.extend(batch_issues)
            
            # 如果返回的数据少于请求的限制，说明已经是最后一页
            if len(batch_issues) < batch_size:
                break
                
            offset += batch_size
            print(f"📊 已获取 {len(all_issues)} 个议题，继续获取...")
        
        print(f"📊 统计完成，共 {len(all_issues)} 个议题")
        issues = all_issues
        
        # 计算统计信息
        statistics = {
            "total_issues": len(issues),
            "status_breakdown": {},
            "priority_breakdown": {},
            "assignee_breakdown": {},
            "type_breakdown": {},
            "recent_activity": {
                "created_last_7_days": 0,
                "updated_last_7_days": 0,
                "closed_last_7_days": 0
            }
        }
        
        # 时间计算
        now = datetime.now()
        seven_days_ago = now - timedelta(days=7)
        
        for issue in issues:
            # 状态统计
            status = issue.get('status', 'unknown')
            statistics['status_breakdown'][status] = statistics['status_breakdown'].get(status, 0) + 1
            
            # 优先级统计
            priority = issue.get('priority', 'unknown')
            statistics['priority_breakdown'][priority] = statistics['priority_breakdown'].get(priority, 0) + 1
            
            # 分配人统计
            assigned_to = issue.get('assignedTo', 'unassigned')
            statistics['assignee_breakdown'][assigned_to] = statistics['assignee_breakdown'].get(assigned_to, 0) + 1
            
            # 类型统计
            issue_type = issue.get('issueTypeId', 'unknown')
            statistics['type_breakdown'][issue_type] = statistics['type_breakdown'].get(issue_type, 0) + 1
            
            # 最近活动统计
            try:
                created_at = datetime.fromisoformat(issue.get('createdAt', '').replace('Z', '+00:00'))
                if created_at >= seven_days_ago:
                    statistics['recent_activity']['created_last_7_days'] += 1
            except:
                pass
            
            try:
                updated_at = datetime.fromisoformat(issue.get('updatedAt', '').replace('Z', '+00:00'))
                if updated_at >= seven_days_ago:
                    statistics['recent_activity']['updated_last_7_days'] += 1
            except:
                pass
            
            if status in ['closed', 'resolved']:
                try:
                    closed_at = datetime.fromisoformat(issue.get('closedAt', '').replace('Z', '+00:00'))
                    if closed_at >= seven_days_ago:
                        statistics['recent_activity']['closed_last_7_days'] += 1
                except:
                    pass
        
        return jsonify({
            "status": "success",
            "project_id": project_id,
            "statistics": statistics,
            "generated_at": now.isoformat()
        })
        
    except Exception as e:
        print(f"❌ 获取议题统计API出错: {str(e)}")
        return jsonify({
            "status": "error",
            "error": f"获取议题统计失败: {str(e)}"
        }), 500


def get_issues_by_file_urn(project_id, file_urn, access_token=None):
    """
    根据文件URN获取相关的议题
    使用现有的 filter[linkedDocumentUrn] 参数
    
    Args:
        project_id (str): 项目ID
        file_urn (str): 文件URN
        access_token (str): 访问令牌（可选）
    
    Returns:
        dict: 包含相关议题的结果
    """
    try:
        # 获取访问令牌
        if not access_token:
            access_token = utils.get_access_token()
            
        if not access_token:
            return {
                'success': False,
                'error': 'Access token not found'
            }
        
        # 构建请求头
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # 构建过滤条件
        filters = {
            'linkedDocumentUrn': file_urn
        }
        
        # 设置分页参数
        pagination = {
            'limit': 100  # 获取最多100个相关议题
        }
        
        print(f"🔍 根据文件URN获取相关议题: {file_urn}")
        
        # 调用现有的get_issues_list函数
        response = get_issues_list(project_id, headers, filters, pagination)
        
        if response.get('success'):
            issues = response.get('data', {}).get('results', [])
            
            # 处理议题数据，添加关联类型信息
            processed_issues = []
            for issue in issues:
                # 分析关联类型
                relation_type = 'unknown'
                relation_info = {}
                
                # 检查linkedDocuments
                linked_docs = issue.get('linkedDocuments', [])
                for doc in linked_docs:
                    if doc.get('urn') == file_urn:
                        relation_type = 'linked_document'
                        relation_info = {
                            'type': doc.get('type', 'unknown'),
                            'createdBy': doc.get('createdBy'),
                            'createdAt': doc.get('createdAt'),
                            'details': doc.get('details', {})
                        }
                        break
                
                # 如果没有在linkedDocuments中找到，检查pushpin
                if relation_type == 'unknown':
                    # 检查pushpin属性（如果存在）
                    pushpin_attrs = issue.get('pushpinAttributes', [])
                    for pushpin in pushpin_attrs:
                        if file_urn in str(pushpin.get('objectId', '')):
                            relation_type = 'pushpin'
                            relation_info = pushpin
                            break
                
                processed_issue = {
                    'issue': issue,
                    'relation_type': relation_type,
                    'relation_info': relation_info
                }
                processed_issues.append(processed_issue)
            
            result = {
                'success': True,
                'data': {
                    'file_urn': file_urn,
                    'project_id': project_id,
                    'related_issues': processed_issues,
                    'count': len(processed_issues),
                    'total_found': len(issues)
                }
            }
            
            print(f"✅ 找到 {len(processed_issues)} 个与文件 {file_urn} 相关的议题")
            return result
        else:
            return response
            
    except Exception as e:
        print(f"❌ 根据文件URN获取议题失败: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


@issues_bp.route('/api/issues/projects/<project_id>/files/<path:file_urn>/issues', methods=['GET'])
def get_issues_by_file_urn_api(project_id, file_urn):
    """
    根据文件URN获取相关议题的API端点
    
    Args:
        project_id (str): 项目ID
        file_urn (str): 文件URN（URL编码）
    
    Returns:
        JSON: 相关议题列表
    """
    try:
        # URL解码文件URN
        from urllib.parse import unquote
        decoded_file_urn = unquote(file_urn)
        
        print(f"🔍 API请求: 获取文件相关议题")
        print(f"📁 项目ID: {project_id}")
        print(f"📄 文件URN: {decoded_file_urn}")
        
        # 获取访问令牌
        access_token = utils.get_access_token()
        if not access_token:
            return jsonify({
                'success': False,
                'error': 'Access token not found'
            }), 401
        
        # 调用核心函数
        result = get_issues_by_file_urn(project_id, decoded_file_urn, access_token)
        
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        print(f"❌ 文件议题API出错: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
