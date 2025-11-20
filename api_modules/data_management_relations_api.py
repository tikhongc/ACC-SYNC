# -*- coding: utf-8 -*-
"""
Data Management Relations API 通用模块
处理所有与 Autodesk Data Management API 关系相关的功能
支持获取、创建、删除各种类型的关联关系
"""

import requests
import json
from flask import Blueprint, jsonify, request
from datetime import datetime
import config
import utils
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time
from .urn_download_simple import download_document_lineage, download_by_urn

relations_bp = Blueprint('relations', __name__)

# ==================== 核心关系管理类 ====================

class EntityMapper:
    """实体ID映射管理器"""
    
    def __init__(self):
        self.cache = {}
        self.cache_timeout = 300  # 5分钟缓存
    
    def _get_cache_key(self, entity_type, entity_id, project_id):
        """生成缓存键"""
        return f"{entity_type}:{project_id}:{entity_id}"
    
    def _is_cache_valid(self, cache_entry):
        """检查缓存是否有效"""
        if not cache_entry:
            return False
        return (time.time() - cache_entry['timestamp']) < self.cache_timeout
    
    def rfi_to_data_management_id(self, project_id, rfi_id, access_token):
        """将RFI ID映射到Data Management ID"""
        cache_key = self._get_cache_key('rfi', rfi_id, project_id)
        
        # 检查缓存
        if cache_key in self.cache and self._is_cache_valid(self.cache[cache_key]):
            return self.cache[cache_key]['data']
        
        try:
            # 方法1: 通过RFI API获取virtualFolderUrn
            rfi_data = self._get_rfi_data(project_id, rfi_id, access_token)
            if rfi_data:
                virtual_folder_urn = rfi_data.get('virtualFolderUrn')
                if virtual_folder_urn:
                    # 解析URN获取folder ID
                    folder_id = self._extract_id_from_urn(virtual_folder_urn)
                    if folder_id:
                        result = {
                            'type': 'folder',
                            'id': folder_id,
                            'urn': virtual_folder_urn
                        }
                        # 缓存结果
                        self.cache[cache_key] = {
                            'data': result,
                            'timestamp': time.time()
                        }
                        return result
            
            # 方法2: 通过RFI附件查找关联的文档
            attachments_data = self._get_rfi_attachments(project_id, rfi_id, access_token)
            if attachments_data:
                for attachment in attachments_data:
                    lineage_urn = attachment.get('lineage_urn')
                    docs_id = attachment.get('docs_id')
                    if lineage_urn or docs_id:
                        result = {
                            'type': 'item',
                            'id': docs_id or self._extract_id_from_urn(lineage_urn),
                            'urn': lineage_urn,
                            'source': 'attachment'
                        }
                        # 缓存结果
                        self.cache[cache_key] = {
                            'data': result,
                            'timestamp': time.time()
                        }
                        return result
            
            # 方法3: 搜索项目中包含RFI信息的items
            search_result = self._search_items_by_rfi(project_id, rfi_id, access_token)
            if search_result:
                result = search_result
                # 缓存结果
                self.cache[cache_key] = {
                    'data': result,
                    'timestamp': time.time()
                }
                return result
                
        except Exception as e:
            print(f"RFI ID映射失败: {e}")
        
        return None
    
    def issue_to_data_management_id(self, project_id, issue_id, access_token):
        """将Issue ID映射到Data Management ID"""
        cache_key = self._get_cache_key('issue', issue_id, project_id)
        
        # 检查缓存
        if cache_key in self.cache and self._is_cache_valid(self.cache[cache_key]):
            return self.cache[cache_key]['data']
        
        try:
            # Issues通常有pushpin_attributes包含文档信息
            issue_data = self._get_issue_data(project_id, issue_id, access_token)
            if issue_data:
                pushpin_attrs = issue_data.get('pushpin_attributes', {})
                object_id = pushpin_attrs.get('object_id')
                if object_id:
                    result = {
                        'type': 'item',
                        'id': object_id,
                        'source': 'pushpin'
                    }
                    # 缓存结果
                    self.cache[cache_key] = {
                        'data': result,
                        'timestamp': time.time()
                    }
                    return result
                    
        except Exception as e:
            print(f"Issue ID映射失败: {e}")
        
        return None
    
    def submittal_to_data_management_id(self, project_id, submittal_id, access_token):
        """将Submittal ID映射到Data Management ID"""
        cache_key = self._get_cache_key('submittal', submittal_id, project_id)
        
        # 检查缓存
        if cache_key in self.cache and self._is_cache_valid(self.cache[cache_key]):
            return self.cache[cache_key]['data']
        
        try:
            # 方法1: 通过Submittal API获取关联的文档信息
            submittal_data = self._get_submittal_data(project_id, submittal_id, access_token)
            if submittal_data:
                # 查找virtualFolderUrn或其他文档关联字段
                virtual_folder_urn = submittal_data.get('virtualFolderUrn')
                if virtual_folder_urn:
                    folder_id = self._extract_id_from_urn(virtual_folder_urn)
                    if folder_id:
                        result = {
                            'type': 'folder',
                            'id': folder_id,
                            'urn': virtual_folder_urn
                        }
                        # 缓存结果
                        self.cache[cache_key] = {
                            'data': result,
                            'timestamp': time.time()
                        }
                        return result
                
                # 方法2: 查找关联的文档或附件
                # 检查是否有文档相关的字段
                for field in ['documentUrn', 'attachmentUrn', 'fileUrn']:
                    if field in submittal_data and submittal_data[field]:
                        urn = submittal_data[field]
                        doc_id = self._extract_id_from_urn(urn)
                        if doc_id:
                            result = {
                                'type': 'item',
                                'id': doc_id,
                                'urn': urn,
                                'source': field
                            }
                            # 缓存结果
                            self.cache[cache_key] = {
                                'data': result,
                                'timestamp': time.time()
                            }
                            return result
            
            # 方法3: 通过Submittal附件查找关联的文档
            attachments_data = self._get_submittal_attachments(project_id, submittal_id, access_token)
            if attachments_data:
                for attachment in attachments_data:
                    lineage_urn = attachment.get('lineage_urn') or attachment.get('lineageUrn')
                    docs_id = attachment.get('docs_id') or attachment.get('documentId')
                    if lineage_urn or docs_id:
                        result = {
                            'type': 'item',
                            'id': docs_id or self._extract_id_from_urn(lineage_urn),
                            'urn': lineage_urn,
                            'source': 'attachment'
                        }
                        # 缓存结果
                        self.cache[cache_key] = {
                            'data': result,
                            'timestamp': time.time()
                        }
                        return result
            
            # 方法4: 搜索项目中包含Submittal信息的items
            search_result = self._search_items_by_submittal(project_id, submittal_id, access_token)
            if search_result:
                result = search_result
                # 缓存结果
                self.cache[cache_key] = {
                    'data': result,
                    'timestamp': time.time()
                }
                return result
                
        except Exception as e:
            print(f"Submittal ID映射失败: {e}")
        
        return None
    
    def _get_rfi_data(self, project_id, rfi_id, access_token):
        """获取RFI数据"""
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            # 移除'b.'前缀
            clean_project_id = project_id[2:] if project_id.startswith('b.') else project_id
            url = f"{config.AUTODESK_API_BASE}/construction/rfis/v3/projects/{clean_project_id}/rfis/{rfi_id}"
            
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"获取RFI数据失败: {e}")
        return None
    
    def _get_rfi_attachments(self, project_id, rfi_id, access_token):
        """获取RFI附件数据"""
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            # 移除'b.'前缀
            clean_project_id = project_id[2:] if project_id.startswith('b.') else project_id
            url = f"{config.AUTODESK_API_BASE}/construction/rfis/v3/projects/{clean_project_id}/rfis/{rfi_id}/attachments"
            
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                return data.get('results', [])
        except Exception as e:
            print(f"获取RFI附件数据失败: {e}")
        return []
    
    def _get_issue_data(self, project_id, issue_id, access_token):
        """获取Issue数据"""
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            url = f"{config.AUTODESK_API_BASE}/construction/issues/v1/projects/{project_id}/issues/{issue_id}"
            
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"获取Issue数据失败: {e}")
        return None
    
    def _get_issue_data(self, project_id, issue_id, access_token):
        """获取Issue数据"""
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            # 移除'b.'前缀
            clean_project_id = project_id[2:] if project_id.startswith('b.') else project_id
            url = f"{config.AUTODESK_API_BASE}/construction/issues/v1/projects/{clean_project_id}/issues/{issue_id}"
            
            print(f"Calling Issue API: {url}")
            response = requests.get(url, headers=headers, timeout=30)
            print(f"Issue API response: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Issue API success: {json.dumps(data, indent=2)}")
                return data
            else:
                print(f"Issue API failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"获取Issue数据失败: {e}")
            import traceback
            traceback.print_exc()
        return None
    
    def _get_submittal_data(self, project_id, submittal_id, access_token):
        """获取Submittal数据"""
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            # 移除'b.'前缀
            clean_project_id = project_id[2:] if project_id.startswith('b.') else project_id
            url = f"{config.AUTODESK_API_BASE}/construction/submittals/v2/projects/{clean_project_id}/items/{submittal_id}"
            
            print(f"Calling Submittal API: {url}")
            response = requests.get(url, headers=headers, timeout=30)
            print(f"Submittal API response: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Submittal API success: {json.dumps(data, indent=2)}")
                return data
            else:
                print(f"Submittal API failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"获取Submittal数据失败: {e}")
            import traceback
            traceback.print_exc()
        return None
    
    def _get_submittal_attachments(self, project_id, submittal_id, access_token):
        """获取Submittal附件数据"""
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            # 移除'b.'前缀
            clean_project_id = project_id[2:] if project_id.startswith('b.') else project_id
            url = f"{config.AUTODESK_API_BASE}/construction/submittals/v2/projects/{clean_project_id}/items/{submittal_id}/attachments"
            
            print(f"Calling Submittal Attachments API: {url}")
            response = requests.get(url, headers=headers, timeout=30)
            print(f"Submittal Attachments API response: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Submittal Attachments API success: {json.dumps(data, indent=2)}")
                return data.get('results', [])
            else:
                print(f"Submittal Attachments API failed: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"获取Submittal附件数据失败: {e}")
            import traceback
            traceback.print_exc()
        return []
    
    def _search_items_by_submittal(self, project_id, submittal_id, access_token):
        """在项目中搜索与Submittal相关的items"""
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            url = f"{config.AUTODESK_API_BASE}/data/v1/projects/{project_id}/items"
            
            # 搜索包含Submittal ID的items
            params = {
                'filter[displayName]': f"*{submittal_id}*"
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                items = data.get('data', [])
                if items:
                    # 返回第一个匹配的item
                    item = items[0]
                    return {
                        'type': 'item',
                        'id': item.get('id'),
                        'source': 'search'
                    }
        except Exception as e:
            print(f"搜索Submittal相关items失败: {e}")
        
        return None
    
    def _extract_id_from_urn(self, urn):
        """从URN中提取ID"""
        if not urn:
            return None
        
        try:
            # URN格式示例: urn:adsk.wip:fs.folder:co.1838SAGCQ3SPn7lqOXMaJQ
            parts = urn.split(':')
            if len(parts) >= 4:
                return parts[-1]  # 取最后一部分作为ID
        except Exception as e:
            print(f"URN解析失败: {e}")
        
        return None
    
    def _search_items_by_rfi(self, project_id, rfi_id, access_token):
        """在项目中搜索与RFI相关的items"""
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            url = f"{config.AUTODESK_API_BASE}/data/v1/projects/{project_id}/items"
            
            # 搜索包含RFI ID的items
            params = {
                'filter[displayName]': f"*{rfi_id}*"
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                items = data.get('data', [])
                if items:
                    # 返回第一个匹配的item
                    item = items[0]
                    return {
                        'type': 'item',
                        'id': item.get('id'),
                        'source': 'search'
                    }
        except Exception as e:
            print(f"搜索RFI相关items失败: {e}")
        
        return None


class RelationshipTypeManager:
    """关系类型管理器"""
    
    # 标准化关系类型映射
    REFERENCE_TYPES = {
        'document': 'xrefs',
        'file': 'includes', 
        'dependency': 'dependencies',
        'auxiliary': 'auxiliary',
        'derived': 'derived'
    }
    
    # 反向映射
    REVERSE_REFERENCE_TYPES = {v: k for k, v in REFERENCE_TYPES.items()}
    
    # 支持的目标类型
    TARGET_TYPES = ['items', 'versions', 'folders']
    
    # 支持的方向
    DIRECTIONS = ['from', 'to']
    
    # 支持的实体类型及其映射 (基于ACC完整分类)
    ENTITY_TYPES = {
        # 文档类
        'file': {
            'api_module': 'data_management',
            'display_name': 'File',
            'icon': 'Document',
            'category': 'document',
            'supported_references': ['document', 'version', 'dependency', 'markup'],
            'api_endpoints': {
                'get': '/data/v1/projects/{project_id}/items/{entity_id}',
                'references': '/api/files/{project_id}/{entity_id}/references'
            }
        },
        'document_package': {
            'api_module': 'data_management',
            'display_name': 'Document Package',
            'icon': 'FolderOpened',
            'category': 'document',
            'supported_references': ['document', 'file', 'dependency'],
            'api_endpoints': {
                'get': '/data/v1/projects/{project_id}/folders/{entity_id}',
                'references': '/api/document-packages/{project_id}/{entity_id}/references'
            }
        },
        'drawing': {
            'api_module': 'data_management',
            'display_name': 'Drawing',
            'icon': 'Picture',
            'category': 'document',
            'supported_references': ['document', 'file', 'version', 'markup', 'specification'],
            'api_endpoints': {
                'get': '/data/v1/projects/{project_id}/items/{entity_id}',
                'references': '/api/drawings/{project_id}/{entity_id}/references'
            }
        },
        'photo': {
            'api_module': 'photos',
            'display_name': 'Photo',
            'icon': 'Camera',
            'category': 'media',
            'supported_references': ['document', 'file', 'issue', 'rfi'],
            'api_endpoints': {
                'get': '/construction/photos/v3/projects/{project_id}/photos/{entity_id}',
                'references': '/api/photos/{project_id}/{entity_id}/references'
            }
        },
        
        # 工作流程类
        'submittal': {
            'api_module': 'submittals',
            'display_name': 'Submittal',
            'icon': 'Upload',
            'category': 'workflow',
            'supported_references': ['document', 'file', 'drawing', 'specification', 'photo'],
            'api_endpoints': {
                'get': '/construction/submittals/v3/projects/{project_id}/submittals/{entity_id}',
                'references': '/api/submittals/{project_id}/{entity_id}/references'
            }
        },
        'issue': {
            'api_module': 'issues',
            'display_name': 'Issue',
            'icon': 'Warning',
            'category': 'workflow',
            'supported_references': ['document', 'file', 'photo', 'drawing', 'rfi'],
            'api_endpoints': {
                'get': '/construction/issues/v3/projects/{project_id}/issues/{entity_id}',
                'references': '/api/issues/{project_id}/{entity_id}/references'
            }
        },
        'rfi': {
            'api_module': 'rfis',
            'display_name': 'RFI',
            'icon': 'QuestionFilled',
            'category': 'workflow',
            'supported_references': ['document', 'file', 'drawing', 'photo', 'issue', 'specification'],
            'api_endpoints': {
                'get': '/construction/rfis/v3/projects/{project_id}/rfis/{entity_id}',
                'references': '/api/rfis/{project_id}/{entity_id}/references'
            }
        },
        'correspondence': {
            'api_module': 'correspondence',
            'display_name': 'Correspondence',
            'icon': 'Message',
            'category': 'workflow',
            'supported_references': ['document', 'file', 'rfi', 'issue', 'submittal'],
            'api_endpoints': {
                'get': '/construction/correspondence/v3/projects/{project_id}/correspondence/{entity_id}',
                'references': '/api/correspondence/{project_id}/{entity_id}/references'
            }
        },
        
        # 管理类
        'schedule_activity': {
            'api_module': 'schedules',
            'display_name': 'Schedule Activity',
            'icon': 'Calendar',
            'category': 'management',
            'supported_references': ['document', 'file', 'drawing', 'submittal'],
            'api_endpoints': {
                'get': '/construction/schedules/v3/projects/{project_id}/activities/{entity_id}',
                'references': '/api/schedule-activities/{project_id}/{entity_id}/references'
            }
        },
        'specification': {
            'api_module': 'specifications',
            'display_name': 'Specification',
            'icon': 'Document',
            'category': 'management',
            'supported_references': ['document', 'file', 'drawing', 'submittal'],
            'api_endpoints': {
                'get': '/construction/specifications/v3/projects/{project_id}/specifications/{entity_id}',
                'references': '/api/specifications/{project_id}/{entity_id}/references'
            }
        },
        'asset': {
            'api_module': 'assets',
            'display_name': 'Asset',
            'icon': 'Box',
            'category': 'management',
            'supported_references': ['document', 'file', 'drawing', 'photo', 'specification'],
            'api_endpoints': {
                'get': '/construction/assets/v3/projects/{project_id}/assets/{entity_id}',
                'references': '/api/assets/{project_id}/{entity_id}/references'
            }
        },
        'form': {
            'api_module': 'forms',
            'display_name': 'Form',
            'icon': 'List',
            'category': 'management',
            'supported_references': ['document', 'file', 'photo', 'issue'],
            'api_endpoints': {
                'get': '/construction/forms/v3/projects/{project_id}/forms/{entity_id}',
                'references': '/api/forms/{project_id}/{entity_id}/references'
            }
        }
    }
    
    # 实体类别定义
    ENTITY_CATEGORIES = {
        'document': {
            'display_name': 'Document Category',
            'icon': 'Folder',
            'color': '#409eff',
            'entities': ['file', 'document_package', 'drawing']
        },
        'media': {
            'display_name': 'Media Category',
            'icon': 'Picture',
            'color': '#67c23a',
            'entities': ['photo']
        },
        'workflow': {
            'display_name': 'Workflow Category',
            'icon': 'Operation',
            'color': '#e6a23c',
            'entities': ['submittal', 'issue', 'rfi', 'correspondence']
        },
        'management': {
            'display_name': 'Management Category',
            'icon': 'Setting',
            'color': '#f56c6c',
            'entities': ['schedule_activity', 'specification', 'asset', 'form']
        }
    }
    
    def normalize_ref_type(self, ref_type):
        """标准化关系类型"""
        if ref_type in self.REFERENCE_TYPES:
            return self.REFERENCE_TYPES[ref_type]
        elif ref_type in self.REVERSE_REFERENCE_TYPES:
            return ref_type
        else:
            return 'xrefs'  # 默认类型
    
    def get_supported_types(self, entity_type):
        """获取实体支持的关系类型"""
        # 不同实体类型支持的关系类型可能不同
        entity_support = {
            'rfi': ['document', 'file', 'auxiliary'],
            'issue': ['document', 'file', 'dependency'],
            'submittal': ['document', 'file', 'derived'],
            'default': ['document', 'file', 'dependency', 'auxiliary']
        }
        
        return entity_support.get(entity_type, entity_support['default'])
    
    def format_ref_type_for_display(self, ref_type):
        """格式化关系类型用于显示"""
        display_names = {
            'xrefs': 'External References',
            'includes': 'Included Files',
            'dependencies': 'Dependencies',
            'auxiliary': 'Auxiliary Files',
            'derived': 'Derived Files'
        }
        
        return display_names.get(ref_type, ref_type)


class RelationsManager:
    """Data Management 关系管理器"""
    
    def __init__(self):
        self.base_url = f"{config.AUTODESK_API_BASE}/data/v1"
        self.entity_mapper = EntityMapper()
        self.type_manager = RelationshipTypeManager()
        self.cache = {}
        self.cache_timeout = 180  # 3分钟缓存
    
    def _get_cache_key(self, method, *args):
        """生成缓存键"""
        return f"{method}:" + ":".join(str(arg) for arg in args)
    
    def _is_cache_valid(self, cache_entry):
        """检查缓存是否有效"""
        if not cache_entry:
            return False
        return (time.time() - cache_entry['timestamp']) < self.cache_timeout
    
    def get_item_relationships(self, project_id, item_id, filters=None, access_token=None):
        """获取item的关系"""
        cache_key = self._get_cache_key('item_relationships', project_id, item_id, str(filters))
        
        # 检查缓存
        if cache_key in self.cache and self._is_cache_valid(self.cache[cache_key]):
            return self.cache[cache_key]['data']
        
        if not access_token:
            access_token = utils.get_access_token()
        
        if not access_token:
            raise Exception("Access token not found")
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # 构建URL
        encoded_item_id = urllib.parse.quote(item_id, safe='')
        url = f"{self.base_url}/projects/{project_id}/items/{encoded_item_id}/relationships/refs"
        
        # 构建查询参数
        params = {}
        if filters:
            if 'ref_types' in filters:
                ref_types = [self.type_manager.normalize_ref_type(rt) for rt in filters['ref_types']]
                params['filter[refType]'] = ','.join(ref_types)
            
            if 'target_types' in filters:
                params['filter[type]'] = ','.join(filters['target_types'])
            
            if 'direction' in filters:
                params['filter[direction]'] = filters['direction']
            
            if 'limit' in filters:
                params['limit'] = filters['limit']
            
            if 'offset' in filters:
                params['offset'] = filters['offset']
        
        try:
            print(f"获取item关系: {url}")
            print(f"查询参数: {params}")
            
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            print(f"Data Management API响应状态: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                relationships = self._format_relationships_data(data)
                
                # 缓存结果
                self.cache[cache_key] = {
                    'data': relationships,
                    'timestamp': time.time()
                }
                
                return relationships
            else:
                print(f"获取item关系失败: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            print(f"获取item关系时出错: {e}")
            return []
    
    def get_version_relationships(self, project_id, version_id, filters=None, access_token=None):
        """获取version的关系"""
        cache_key = self._get_cache_key('version_relationships', project_id, version_id, str(filters))
        
        # 检查缓存
        if cache_key in self.cache and self._is_cache_valid(self.cache[cache_key]):
            return self.cache[cache_key]['data']
        
        if not access_token:
            access_token = utils.get_access_token()
        
        if not access_token:
            raise Exception("Access token not found")
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # 构建URL
        encoded_version_id = urllib.parse.quote(version_id, safe='')
        url = f"{self.base_url}/projects/{project_id}/versions/{encoded_version_id}/relationships/refs"
        
        # 构建查询参数
        params = {}
        if filters:
            if 'ref_types' in filters:
                ref_types = [self.type_manager.normalize_ref_type(rt) for rt in filters['ref_types']]
                params['filter[refType]'] = ','.join(ref_types)
            
            if 'target_types' in filters:
                params['filter[type]'] = ','.join(filters['target_types'])
            
            if 'direction' in filters:
                params['filter[direction]'] = filters['direction']
            
            if 'limit' in filters:
                params['limit'] = filters['limit']
            
            if 'offset' in filters:
                params['offset'] = filters['offset']
        
        try:
            print(f"获取version关系: {url}")
            print(f"查询参数: {params}")
            
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            print(f"Data Management API响应状态: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                relationships = self._format_relationships_data(data)
                
                # 缓存结果
                self.cache[cache_key] = {
                    'data': relationships,
                    'timestamp': time.time()
                }
                
                return relationships
            else:
                print(f"获取version关系失败: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            print(f"获取version关系时出错: {e}")
            return []
    
    def _get_rfi_specific_references(self, rfi_id, project_id, reference_types=None, access_token=None):
        """获取RFI特有的参照关系（使用Relationship API）"""
        if not access_token:
            access_token = utils.get_access_token()
        
        references = []
        
        try:
            # 使用Relationship API获取真正的RFI参照
            container_id = project_id[2:] if project_id.startswith('b.') else project_id
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # 调用Relationship API搜索包含此RFI的关系
            search_url = f"https://developer.api.autodesk.com/bim360/relationship/v2/containers/{container_id}/relationships:search"
            
            params = {
                "domain": "autodesk-bim360-rfi",
                "type": "rfi", 
                "id": rfi_id,
                "pageLimit": 50
            }
            
            print(f"Calling Relationship API for RFI {rfi_id}")
            response = requests.get(search_url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                relationships = data.get('relationships', [])
                print(f"Found {len(relationships)} relationships from Relationship API")
                
                for relationship in relationships:
                    rel_id = relationship.get('id')
                    created_on = relationship.get('createdOn')
                    entities = relationship.get('entities', [])
                    
                    # 找到不是RFI的另一个实体（即参照的目标）
                    for entity in entities:
                        if entity.get('id') != rfi_id:  # 不是RFI本身
                            target_domain = entity.get('domain')
                            target_type = entity.get('type')
                            target_id = entity.get('id')
                            
                            # 格式化为我们的参照格式
                            references.append({
                                'id': rel_id,
                                'ref_type': 'document_reference',
                                'direction': 'from',
                                'source_id': rfi_id,
                                'source_type': 'rfi',
                                'target_id': target_id,
                                'target_type': target_type,
                                'extension_type': f'relationship_{target_domain}_{target_type}',
                                'target': {
                                    'id': target_id,
                                    'type': target_type,
                                    'name': self._get_document_name_from_lineage(target_id, access_token, project_id) or f"{target_type}: {target_id}",
                                    'file_type': 'document',
                                    'mime_type': 'application/octet-stream',
                                    'version_number': None,
                                    'create_time': created_on,
                                    'last_modified_time': None,
                                    'storage_urn': target_id,
                                    'web_view_url': None
                                }
                            })
                            
                            print(f"Found RFI relationship: {target_domain}/{target_type} - {target_id}")
            else:
                print(f"Relationship API failed: {response.status_code} - {response.text}")
            
            print(f"RFI {rfi_id} found {len(references)} total references")
            return references
            
        except Exception as e:
            print(f"Failed to get RFI references: {e}")
            return references
    
    def _get_submittal_specific_references(self, submittal_id, project_id, reference_types=None, access_token=None):
        """获取Submittal特有的参照关系（仅使用Relationship API）"""
        if not access_token:
            access_token = utils.get_access_token()
        
        references = []
        
        try:
            print(f"Getting Submittal references for ID: {submittal_id} in project: {project_id}")
            
            # 使用Relationship API搜索真正的参照关系
            relationship_references = self._get_submittal_relationship_api_references(
                submittal_id, project_id, access_token
            )
            references.extend(relationship_references)
            print(f"Found {len(relationship_references)} references from Relationship API")
            
            print(f"Submittal {submittal_id} found {len(references)} total references")
            return references
            
        except Exception as e:
            print(f"Failed to get Submittal references: {e}")
            import traceback
            traceback.print_exc()
            return references
    
    def _get_folder_contents_as_references(self, folder_urn, project_id, submittal_id, access_token):
        """从文件夹URN获取内容作为参照"""
        references = []
        
        try:
            # 从URN中提取folder ID
            folder_id = self.entity_mapper._extract_id_from_urn(folder_urn)
            if not folder_id:
                print(f"Could not extract folder ID from URN: {folder_urn}")
                return references
            
            headers = {"Authorization": f"Bearer {access_token}"}
            url = f"{config.AUTODESK_API_BASE}/data/v1/projects/{project_id}/folders/{folder_id}/contents"
            
            print(f"Getting folder contents from: {url}")
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                items = data.get('data', [])
                print(f"Found {len(items)} items in folder")
                
                for item in items:
                    item_id = item.get('id')
                    item_type = item.get('type')
                    attributes = item.get('attributes', {})
                    
                    if item_type in ['items', 'versions']:
                        reference = {
                            'id': f"folder_ref_{item_id}",
                            'ref_type': 'document_reference',
                            'direction': 'from',
                            'source_id': submittal_id,
                            'source_type': 'submittal',
                            'target_id': item_id,
                            'target_type': 'document',
                            'extension_type': f'folder_content_{item_type}',
                            'target': {
                                'id': item_id,
                                'type': item_type,
                                'name': attributes.get('displayName', f"Document {item_id}"),
                                'file_type': attributes.get('fileType', 'document'),
                                'mime_type': 'application/octet-stream',
                                'file_size': attributes.get('storageSize', 0),
                                'version_number': attributes.get('versionNumber', 1),
                                'create_time': attributes.get('createTime'),
                                'last_modified_time': attributes.get('lastModifiedTime'),
                                'storage_urn': folder_urn,
                                'web_view_url': None
                            }
                        }
                        references.append(reference)
                        
            else:
                print(f"Failed to get folder contents: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"Error getting folder contents: {e}")
        
        return references
    
    def _convert_attachments_to_references(self, attachments, submittal_id, access_token):
        """将附件转换为参照格式"""
        references = []
        
        for attachment in attachments:
            try:
                attachment_id = attachment.get('id')
                attachment_name = attachment.get('name', 'Unknown Attachment')
                attachment_urn = attachment.get('urn')
                file_size = attachment.get('fileSize', 0)
                created_at = attachment.get('createdAt')
                
                reference = {
                    'id': f"attachment_ref_{attachment_id}",
                    'ref_type': 'attachment_reference',
                    'direction': 'from',
                    'source_id': submittal_id,
                    'source_type': 'submittal',
                    'target_id': attachment_id,
                    'target_type': 'attachment',
                    'extension_type': 'submittal_attachment',
                    'target': {
                        'id': attachment_id,
                        'type': 'attachment',
                        'name': attachment_name,
                        'file_type': 'attachment',
                        'mime_type': 'application/octet-stream',
                        'file_size': file_size,
                        'version_number': 1,
                        'create_time': created_at,
                        'last_modified_time': None,
                        'storage_urn': attachment_urn,
                        'web_view_url': None
                    }
                }
                references.append(reference)
                
            except Exception as e:
                print(f"Error converting attachment to reference: {e}")
        
        return references
    
    def _get_issue_specific_references(self, issue_id, project_id, reference_types=None, access_token=None):
        """获取Issue特有的参照关系（使用多种方法）"""
        if not access_token:
            access_token = utils.get_access_token()
        
        references = []
        
        try:
            print(f"Getting Issue references for ID: {issue_id} in project: {project_id}")
            
            # 方法1: 通过Issue API获取pushpin_attributes中的文档关联
            issue_references = self._get_issue_pushpin_references(
                issue_id, project_id, access_token
            )
            references.extend(issue_references)
            print(f"Found {len(issue_references)} references from Issue pushpin attributes")
            
            # 方法2: 通过Issue附件获取关联的文档
            attachment_references = self._get_issue_attachment_references(
                issue_id, project_id, access_token
            )
            references.extend(attachment_references)
            print(f"Found {len(attachment_references)} references from Issue attachments")
            
            # 方法3: 使用Relationship API搜索真正的参照关系
            relationship_references = self._get_issue_relationship_api_references(
                issue_id, project_id, access_token
            )
            references.extend(relationship_references)
            print(f"Found {len(relationship_references)} references from Relationship API")
            
            print(f"Issue {issue_id} found {len(references)} total references")
            return references
            
        except Exception as e:
            print(f"Failed to get Issue references: {e}")
            import traceback
            traceback.print_exc()
            return references
    
    def _get_issue_pushpin_references(self, issue_id, project_id, access_token):
        """从Issue的pushpin_attributes获取文档参照"""
        references = []
        
        try:
            # 获取Issue详细数据
            issue_data = self._get_issue_data(project_id, issue_id, access_token)
            if not issue_data:
                return references
            
            # 检查pushpin_attributes
            pushpin_attrs = issue_data.get('pushpin_attributes', {})
            if pushpin_attrs:
                object_id = pushpin_attrs.get('object_id')
                viewer_state = pushpin_attrs.get('viewer_state', {})
                
                if object_id:
                    # 从object_id创建参照
                    reference = {
                        'id': f"pushpin_ref_{object_id}",
                        'ref_type': 'document_reference',
                        'direction': 'from',
                        'source_id': issue_id,
                        'source_type': 'issue',
                        'target_id': object_id,
                        'target_type': 'document',
                        'extension_type': 'issue_pushpin',
                        'target': {
                            'id': object_id,
                            'type': 'document',
                            'name': f"Pushpin Document {object_id[:8]}",
                            'file_type': 'document',
                            'mime_type': 'application/octet-stream',
                            'version_number': 1,
                            'create_time': issue_data.get('createdAt'),
                            'last_modified_time': issue_data.get('updatedAt'),
                            'storage_urn': object_id,
                            'web_view_url': None,
                            'viewer_state': viewer_state
                        }
                    }
                    references.append(reference)
                    print(f"Found pushpin reference: {object_id}")
            
            # 检查其他可能的文档关联字段
            for field_name in ['documentUrn', 'attachmentUrn', 'fileUrn', 'linkedDocuments']:
                if field_name in issue_data and issue_data[field_name]:
                    field_value = issue_data[field_name]
                    if isinstance(field_value, str):
                        doc_id = self._extract_id_from_urn(field_value) or field_value
                        reference = {
                            'id': f"issue_doc_ref_{doc_id}",
                            'ref_type': 'document_reference',
                            'direction': 'from',
                            'source_id': issue_id,
                            'source_type': 'issue',
                            'target_id': doc_id,
                            'target_type': 'document',
                            'extension_type': f'issue_{field_name.lower()}',
                            'target': {
                                'id': doc_id,
                                'type': 'document',
                                'name': f"Issue Document {doc_id[:8]}",
                                'file_type': 'document',
                                'mime_type': 'application/octet-stream',
                                'version_number': 1,
                                'create_time': issue_data.get('createdAt'),
                                'last_modified_time': issue_data.get('updatedAt'),
                                'storage_urn': field_value,
                                'web_view_url': None
                            }
                        }
                        references.append(reference)
                        print(f"Found issue document reference from {field_name}: {doc_id}")
                        
        except Exception as e:
            print(f"Error getting issue pushpin references: {e}")
        
        return references
    
    def _get_issue_attachment_references(self, issue_id, project_id, access_token):
        """从Issue附件获取参照"""
        references = []
        
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            # 移除'b.'前缀
            clean_project_id = project_id[2:] if project_id.startswith('b.') else project_id
            url = f"{config.AUTODESK_API_BASE}/construction/issues/v1/projects/{clean_project_id}/issues/{issue_id}/attachments"
            
            print(f"Calling Issue Attachments API: {url}")
            response = requests.get(url, headers=headers, timeout=30)
            print(f"Issue Attachments API response: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Issue Attachments API success: {json.dumps(data, indent=2)}")
                attachments = data.get('results', [])
                
                for attachment in attachments:
                    attachment_id = attachment.get('id')
                    attachment_name = attachment.get('name', 'Unknown Attachment')
                    attachment_urn = attachment.get('urn')
                    lineage_urn = attachment.get('lineage_urn') or attachment.get('lineageUrn')
                    file_size = attachment.get('fileSize', 0)
                    created_at = attachment.get('createdAt')
                    
                    reference = {
                        'id': f"issue_attachment_ref_{attachment_id}",
                        'ref_type': 'attachment_reference',
                        'direction': 'from',
                        'source_id': issue_id,
                        'source_type': 'issue',
                        'target_id': attachment_id,
                        'target_type': 'attachment',
                        'extension_type': 'issue_attachment',
                        'target': {
                            'id': attachment_id,
                            'type': 'attachment',
                            'name': attachment_name,
                            'file_type': 'attachment',
                            'mime_type': 'application/octet-stream',
                            'file_size': file_size,
                            'version_number': 1,
                            'create_time': created_at,
                            'last_modified_time': None,
                            'storage_urn': lineage_urn or attachment_urn,
                            'web_view_url': None
                        }
                    }
                    references.append(reference)
                    print(f"Found issue attachment reference: {attachment_name}")
            else:
                print(f"Issue Attachments API failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"Error getting issue attachment references: {e}")
        
        return references
    
    def _get_issue_relationship_api_references(self, issue_id, project_id, access_token):
        """使用Relationship API获取Issue关联关系"""
        references = []
        
        try:
            container_id = project_id[2:] if project_id.startswith('b.') else project_id
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # 调用Relationship API搜索包含此Issue的关系
            search_url = f"https://developer.api.autodesk.com/bim360/relationship/v2/containers/{container_id}/relationships:search"
            
            # 尝试多个可能的domain参数
            possible_domains = [
                "autodesk-bim360-issue",
                "autodesk-bim360-issues", 
                "autodesk-acc-issue",
                "autodesk-acc-issues",
                "bim360-issue",
                "bim360-issues",
                "autodesk-construction-issue",
                "autodesk-construction-issues"
            ]
            
            # 首先尝试正确的domain和entity type
            correct_params = {
                "domain": "autodesk-construction-issues",
                "type": "issue", 
                "id": issue_id,
                "pageLimit": 50
            }
            
            print(f"Trying correct Relationship API with domain: autodesk-construction-issues, type: issue")
            response = requests.get(search_url, headers=headers, params=correct_params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                relationships = data.get('relationships', [])
                print(f"Correct domain/type: Found {len(relationships)} relationships")
                
                if not relationships:
                    print("Correct domain/type returned 0 relationships, trying fallback options")
                    # 如果正确的参数没有找到关系，尝试其他组合
                    for domain in possible_domains:
                        for entity_type in ["issue", "issueitem"]:
                            params = {
                                "domain": domain,
                                "type": entity_type, 
                                "id": issue_id,
                                "pageLimit": 50
                            }
                            
                            print(f"Trying Relationship API with domain: {domain}, type: {entity_type}")
                            response = requests.get(search_url, headers=headers, params=params, timeout=30)
                            
                            if response.status_code == 200:
                                data = response.json()
                                relationships = data.get('relationships', [])
                                print(f"Domain {domain}, type {entity_type}: Found {len(relationships)} relationships")
                                
                                if relationships:  # 如果找到了关系，就使用这个组合
                                    print(f"Using domain: {domain}, type: {entity_type} (found {len(relationships)} relationships)")
                                    break
                            else:
                                print(f"Domain {domain}, type {entity_type}: API failed with {response.status_code}")
                        if relationships:  # 如果找到了关系，跳出外层循环
                            break
                
                for relationship in relationships:
                    rel_id = relationship.get('id')
                    created_on = relationship.get('createdOn')
                    entities = relationship.get('entities', [])
                    
                    print(f"Processing relationship {rel_id} with entities: {entities}")
                    
                    # 找到不是Issue的另一个实体（即参照的目标）
                    for entity in entities:
                        entity_id = entity.get('id')
                        entity_domain = entity.get('domain')
                        entity_type = entity.get('type')
                        print(f"Checking entity: domain={entity_domain}, type={entity_type}, id={entity_id}")
                        
                        if entity_id != issue_id:  # 不是Issue本身
                            target_domain = entity_domain
                            target_type = entity_type
                            target_id = entity_id
                            
                            # 获取参考的显示信息
                            display_info = self._get_reference_display_info(target_domain, target_type, target_id, access_token, project_id)
                            
                            # 格式化为我们的参照格式
                            references.append({
                                'id': rel_id,
                                'ref_type': display_info['ref_type'],
                                'direction': 'from',
                                'source_id': issue_id,
                                'source_type': 'issue',
                                'target_id': target_id,
                                'target_type': display_info['target_type'],
                                'extension_type': f'relationship_{target_domain}_{target_type}',
                                'markup_info': display_info.get('markup_info'),  # 标记相关的特殊信息
                                'target': {
                                    'id': target_id,
                                    'type': display_info['target_type'],
                                    'name': display_info['display_name'],
                                    'file_type': display_info['file_type'],
                                    'mime_type': 'application/octet-stream',
                                    'version_number': None,
                                    'create_time': created_on,
                                    'last_modified_time': None,
                                    'storage_urn': target_id,
                                    'web_view_url': display_info.get('web_view_url'),
                                    'description': display_info.get('description')
                                }
                            })
                            
                            print(f"Found Issue relationship: {target_domain}/{target_type} - {target_id}")
            else:
                print(f"Relationship API failed: {response.status_code} - {response.text}")
            
        except Exception as e:
            print(f"Failed to get Issue relationships: {e}")
        
        return references
    
    def _get_reference_display_info(self, target_domain, target_type, target_id, access_token, project_id):
        """获取参考的显示信息，特别处理标记相关的参考"""
        
        # 默认信息
        info = {
            'display_name': f"{target_type}: {target_id}",
            'target_type': target_type,
            'ref_type': 'document_reference',
            'file_type': 'document'
        }
        
        # 特殊处理标记相关的参考
        if target_domain == 'autodesk-construction-markup':
            if target_type == 'markupdocument':
                # 标记文档处理
                info.update({
                    'target_type': 'markupdocument',
                    'ref_type': 'markup_reference',
                    'file_type': 'markupdocument'
                })
                
                # 尝试获取真实文档名称
                doc_name = self._get_markup_document_name(target_id, access_token, project_id)
                if doc_name:
                    info['display_name'] = f"{doc_name}"
                    info['description'] = f"这是Issue关联的标记文档 '{doc_name}'，通常是PDF或图纸文件，上面有标记注释。在ACC中可能显示为图纸或文档，但带有标记注释。"
                else:
                    info['display_name'] = f"{target_id[:30]}..."
                    info['description'] = "这是Issue关联的标记文档，通常是PDF或图纸文件，上面有标记注释。在ACC中可能显示为图纸或文档，但带有标记注释。"
                
                # 添加标记信息
                info['markup_info'] = {
                    'type': 'markupdocument',
                    'category': 'Markup Related Reference',
                    'explanation': 'Markup document file, usually PDF or drawing file with markup annotations',
                    'acc_visibility': 'May display as drawing or document in ACC, but with markup annotations',
                    'technical_details': f'URN: {target_id}'
                }
                
                # 生成Web查看URL
                info['web_view_url'] = self._generate_markup_web_view_url(target_id, project_id)
                
            elif target_type == 'markup':
                # 标记数据处理
                info.update({
                    'target_type': 'markup',
                    'ref_type': 'markup_reference',
                    'file_type': 'markup'
                })
                
                info['display_name'] = f"🎯 标记数据: {target_id[:8]}..."
                info['description'] = "这是Issue创建时在图纸上做标记产生的数据，包含标记的坐标、颜色、文字等信息。这是标记功能的技术基础数据。"
                
                # 添加标记信息
                info['markup_info'] = {
                    'type': 'markup',
                    'category': 'Markup Related Reference',
                    'explanation': 'Markup data itself, containing coordinates, colors, text and other markup information',
                    'acc_visibility': 'Usually not directly displayed in ACC interface, but is the technical foundation for markup functionality',
                    'technical_details': f'Markup ID: {target_id}'
                }
        
        # 处理文档lineage
        elif target_domain == 'autodesk-bim360-documentmanagement' and target_type == 'documentlineage':
            doc_name = self._get_document_name_from_lineage(target_id, access_token, project_id)
            if doc_name:
                info['display_name'] = f"{doc_name}"
                info['description'] = f"这是Issue关联的项目文档 '{doc_name}'，在ACC的文档管理中可以直接访问和查看。"
            else:
                info['display_name'] = f"{target_id[:30]}..."
                info['description'] = "这是Issue关联的项目文档，在ACC的文档管理中可以直接访问和查看。"
            
            info['web_view_url'] = self._generate_document_web_view_url(target_id, project_id)
        
        # 处理RFI
        elif 'rfi' in target_domain and target_type == 'rfi':
            rfi_title = self._get_rfi_title(target_id, project_id, access_token)
            if rfi_title:
                info['display_name'] = f"❓ RFI: {rfi_title}"
                info['description'] = f"这是与Issue相关的RFI '{rfi_title}'，表示Issue和RFI之间存在业务关联。"
            else:
                info['display_name'] = f"❓ RFI: {target_id[:8]}..."
                info['description'] = "这是与Issue相关的RFI（Request for Information），表示Issue和RFI之间存在业务关联。"
            
            info.update({
                'target_type': 'rfi',
                'ref_type': 'rfi_reference',
                'file_type': 'rfi'
            })
            info['web_view_url'] = self._generate_rfi_web_view_url(target_id, project_id)
        
        # 其他类型保持原样，但添加简单说明
        else:
            info['description'] = f"这是一个{target_type}类型的参考，属于{target_domain}域。"
        
        return info
    
    def _get_markup_document_name(self, target_id, access_token, project_id):
        """获取标记文档的真实名称"""
        try:
            if 'fs.file:' in target_id:
                headers = {"Authorization": f"Bearer {access_token}"}
                full_project_id = project_id if project_id.startswith('b.') else f'b.{project_id}'
                
                import urllib.parse
                encoded_urn = urllib.parse.quote(target_id, safe='')
                
                # 尝试作为version获取
                version_url = f"{config.AUTODESK_API_BASE}/data/v1/projects/{full_project_id}/versions/{encoded_urn}"
                response = requests.get(version_url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if 'data' in data:
                        attributes = data['data'].get('attributes', {})
                        return attributes.get('displayName') or attributes.get('name')
        except Exception as e:
            print(f"Failed to get markup document name: {e}")
        
        return None
    
    def _get_rfi_title(self, rfi_id, project_id, access_token):
        """获取RFI标题"""
        try:
            rfi_data = self._get_rfi_data(project_id, rfi_id, access_token)
            if rfi_data:
                return rfi_data.get('title') or rfi_data.get('subject')
        except Exception as e:
            print(f"Failed to get RFI title: {e}")
        
        return None
    
    def _generate_markup_web_view_url(self, target_id, project_id):
        """生成标记文档的Web查看URL"""
        try:
            clean_project_id = project_id[2:] if project_id.startswith('b.') else project_id
            return f"https://acc.autodesk.com/docs/files/projects/{clean_project_id}?entityId={target_id}"
        except Exception as e:
            print(f"Failed to generate markup web view URL: {e}")
        return None
    
    def _generate_document_web_view_url(self, target_id, project_id):
        """生成文档的Web查看URL"""
        try:
            clean_project_id = project_id[2:] if project_id.startswith('b.') else project_id
            return f"https://acc.autodesk.com/docs/files/projects/{clean_project_id}?entityId={target_id}"
        except Exception as e:
            print(f"Failed to generate document web view URL: {e}")
        return None
    
    def _generate_rfi_web_view_url(self, target_id, project_id):
        """生成RFI的Web查看URL"""
        try:
            clean_project_id = project_id[2:] if project_id.startswith('b.') else project_id
            return f"https://acc.autodesk.com/build/rfis/projects/{clean_project_id}/rfis/{target_id}"
        except Exception as e:
            print(f"Failed to generate RFI web view URL: {e}")
        return None
    
    def _get_submittal_relationship_api_references(self, submittal_id, project_id, access_token):
        """使用Relationship API获取Submittal关联关系"""
        references = []
        
        try:
            container_id = project_id[2:] if project_id.startswith('b.') else project_id
            
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # 首先查询所有可用的domain和entity types
            utility_url = "https://developer.api.autodesk.com/bim360/relationship/v2/utility/relationships:writable"
            print(f"Querying available domains and entity types...")
            
            utility_response = requests.get(utility_url, headers=headers, timeout=30)
            if utility_response.status_code == 200:
                utility_data = utility_response.json()
                print(f"Available domains and entity types: {json.dumps(utility_data, indent=2)}")
                
                # 查找包含submittal的domain
                submittal_domains = []
                for domain_info in utility_data:
                    domain = domain_info.get('domain', '')
                    entity_types = domain_info.get('entityTypes', [])
                    for entity_type_info in entity_types:
                        entity_type = entity_type_info.get('entityType', '')
                        if 'submittal' in entity_type.lower() or 'submittal' in domain.lower():
                            submittal_domains.append((domain, entity_type))
                            print(f"Found potential submittal domain: {domain}, type: {entity_type}")
                
                if submittal_domains:
                    print(f"Found {len(submittal_domains)} potential submittal domains")
                else:
                    print("No submittal-specific domains found, will try common patterns")
            else:
                print(f"Failed to query utility endpoint: {utility_response.status_code} - {utility_response.text}")
            
            # 调用Relationship API搜索包含此Submittal的关系
            search_url = f"https://developer.api.autodesk.com/bim360/relationship/v2/containers/{container_id}/relationships:search"
            
            # 尝试多个可能的domain参数
            possible_domains = [
                "autodesk-bim360-submittal",
                "autodesk-bim360-submittals", 
                "autodesk-acc-submittal",
                "autodesk-acc-submittals",
                "bim360-submittal",
                "bim360-submittals",
                "autodesk-construction-submittal",
                "autodesk-construction-submittals"
            ]
            
            # 首先尝试正确的domain和entity type
            correct_params = {
                "domain": "autodesk-construction-submittals",
                "type": "submittalitem", 
                "id": submittal_id,
                "pageLimit": 50
            }
            
            print(f"Trying correct Relationship API with domain: autodesk-construction-submittals, type: submittalitem")
            response = requests.get(search_url, headers=headers, params=correct_params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                relationships = data.get('relationships', [])
                print(f"Correct domain/type: Found {len(relationships)} relationships")
                
                if relationships:
                    print(f"SUCCESS: Using correct domain/type (found {len(relationships)} relationships)")
                    params = correct_params
                else:
                    print("Correct domain/type returned 0 relationships, trying fallback options")
                    # 如果正确的参数没有找到关系，尝试其他组合
                    for domain in possible_domains:
                        for entity_type in ["submittal", "submittalitem"]:
                            params = {
                                "domain": domain,
                                "type": entity_type, 
                                "id": submittal_id,
                                "pageLimit": 50
                            }
                            
                            print(f"Trying Relationship API with domain: {domain}, type: {entity_type}")
                            response = requests.get(search_url, headers=headers, params=params, timeout=30)
                            
                            if response.status_code == 200:
                                data = response.json()
                                relationships = data.get('relationships', [])
                                print(f"Domain {domain}, type {entity_type}: Found {len(relationships)} relationships")
                                
                                if relationships:  # 如果找到了关系，就使用这个组合
                                    print(f"Using domain: {domain}, type: {entity_type} (found {len(relationships)} relationships)")
                                    break
                            else:
                                print(f"Domain {domain}, type {entity_type}: API failed with {response.status_code}")
                        if relationships:  # 如果找到了关系，跳出外层循环
                            break
                    else:
                        # 如果所有组合都失败了，使用默认的
                        params = correct_params
                        print(f"All combinations failed, using correct domain/type as default")
                        response = requests.get(search_url, headers=headers, params=params, timeout=30)
            else:
                print(f"Correct domain/type API failed: {response.status_code} - {response.text[:200]}")
                # 使用默认参数
                params = correct_params
                response = requests.get(search_url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                relationships = data.get('relationships', [])
                print(f"Found {len(relationships)} relationships from Relationship API")
                print(f"Full relationship data: {json.dumps(relationships, indent=2)}")
                
                for relationship in relationships:
                    rel_id = relationship.get('id')
                    created_on = relationship.get('createdOn')
                    entities = relationship.get('entities', [])
                    
                    print(f"Processing relationship {rel_id} with entities: {entities}")
                    
                    # 找到不是Submittal的另一个实体（即参照的目标）
                    for entity in entities:
                        entity_id = entity.get('id')
                        entity_domain = entity.get('domain')
                        entity_type = entity.get('type')
                        print(f"Checking entity: domain={entity_domain}, type={entity_type}, id={entity_id}")
                        print(f"Comparing with submittal_id: {submittal_id}")
                        
                        if entity_id != submittal_id:  # 不是Submittal本身
                            target_domain = entity_domain
                            target_type = entity_type
                            target_id = entity_id
                            
                            # 格式化为我们的参照格式
                            references.append({
                                'id': rel_id,
                                'ref_type': 'document_reference',
                                'direction': 'from',
                                'source_id': submittal_id,
                                'source_type': 'submittal',
                                'target_id': target_id,
                                'target_type': target_type,
                                'extension_type': f'relationship_{target_domain}_{target_type}',
                                'target': {
                                    'id': target_id,
                                    'type': target_type,
                                    'name': self._get_document_name_from_lineage(target_id, access_token, project_id) or f"{target_type}: {target_id}",
                                    'file_type': 'document',
                                    'mime_type': 'application/octet-stream',
                                    'version_number': None,
                                    'create_time': created_on,
                                    'last_modified_time': None,
                                    'storage_urn': target_id,
                                    'web_view_url': None
                                }
                            })
                            
                            print(f"Found Submittal relationship: {target_domain}/{target_type} - {target_id}")
            else:
                print(f"Relationship API failed: {response.status_code} - {response.text}")
            
        except Exception as e:
            print(f"Failed to get Submittal relationships: {e}")
        
        return references
    
    def _get_document_name_from_lineage(self, lineage_urn, access_token, project_id=None):
        """从lineage URN获取文档名称"""
        try:
            if "dm.lineage:" in lineage_urn:
                # 提取lineage ID
                lineage_id = lineage_urn.split("dm.lineage:")[-1]
                print(f"Trying to get document name for lineage: {lineage_id}")
                
                # 调用Data Management API获取lineage详情
                headers = {"Authorization": f"Bearer {access_token}"}
                
                # 如果没有提供project_id，无法调用Data Management API
                if not project_id:
                    print("Warning: No project_id provided for lineage lookup")
                    return f"Document_{lineage_id[:8]}"
                
                # Data Management API需要完整的project ID (包括'b.'前缀)
                full_project_id = project_id if project_id.startswith('b.') else f'b.{project_id}'
                
                # URL编码lineage URN
                import urllib.parse
                encoded_urn = urllib.parse.quote(lineage_urn, safe='')
                
                # 使用正确的Data Management API格式获取item信息
                item_url = f"{config.AUTODESK_API_BASE}/data/v1/projects/{full_project_id}/items/{encoded_urn}"
                print(f"Calling Data Management API: {item_url}")
                
                response = requests.get(item_url, headers=headers, timeout=30)
                print(f"Data Management API response: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"Data Management API success: {json.dumps(data, indent=2)}")
                    
                    if 'data' in data:
                        attributes = data['data'].get('attributes', {})
                        display_name = attributes.get('displayName', '')
                        if display_name:
                            print(f"Found document name: {display_name}")
                            return display_name
                else:
                    print(f"Data Management API failed: {response.status_code} - {response.text[:200]}")
                
                # 如果都失败了，返回基于URN的默认名称
                print(f"Could not get document name, using URN-based name")
                return f"Document_{lineage_id[:8]}"
            
            return None
        except Exception as e:
            print(f"Failed to get document name: {e}")
            import traceback
            traceback.print_exc()
            return None

    def get_entity_references(self, entity_type, entity_id, project_id, reference_types=None, access_token=None):
        """获取实体的参照关系"""
        if not access_token:
            access_token = utils.get_access_token()
        
        if not access_token:
            raise Exception("Access token not found")
        
        # RFI、Submittal和Issue使用特殊的参照处理逻辑
        if entity_type == 'rfi':
            return self._get_rfi_specific_references(entity_id, project_id, reference_types, access_token)
        elif entity_type == 'submittal':
            return self._get_submittal_specific_references(entity_id, project_id, reference_types, access_token)
        elif entity_type == 'issue':
            return self._get_issue_specific_references(entity_id, project_id, reference_types, access_token)
        
        # 其他实体类型使用Data Management API
        # 1. 将实体ID映射到Data Management ID
        dm_mapping = None
        # Issue已经在上面处理了，这里不需要再处理
        
        if not dm_mapping:
            print(f"无法映射{entity_type} ID {entity_id}到Data Management ID")
            return []
        
        # 2. 构建过滤器
        filters = {}
        
        if reference_types:
            if isinstance(reference_types, str):
                reference_types = reference_types.split(',')
            filters['ref_types'] = reference_types
        else:
            # 使用实体类型支持的默认参照类型
            filters['ref_types'] = self.type_manager.get_supported_types(entity_type)
        
        filters['target_types'] = ['items', 'versions', 'folders']
        filters['limit'] = 100  # 限制结果数量
        
        # 3. 获取关系
        relationships = []
        
        if dm_mapping['type'] == 'item':
            relationships = self.get_item_relationships(project_id, dm_mapping['id'], filters, access_token)
        elif dm_mapping['type'] == 'version':
            relationships = self.get_version_relationships(project_id, dm_mapping['id'], filters, access_token)
        elif dm_mapping['type'] == 'folder':
            # 文件夹类型的关系获取需要特殊处理
            relationships = self._get_folder_relationships(project_id, dm_mapping['id'], filters, access_token)
        
        # 4. 增强关系数据
        enhanced_relationships = self._enhance_relationships_data(relationships, project_id, access_token)
        
        return enhanced_relationships
    
    def _get_folder_relationships(self, project_id, folder_id, filters, access_token):
        """获取文件夹的关系（特殊处理）"""
        try:
            # 文件夹关系可能需要通过获取文件夹内容来间接获取
            headers = {"Authorization": f"Bearer {access_token}"}
            url = f"{self.base_url}/projects/{project_id}/folders/{folder_id}/contents"
            
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                items = data.get('data', [])
                
                # 对每个item获取其关系
                all_relationships = []
                for item in items[:10]:  # 限制处理数量
                    item_id = item.get('id')
                    if item_id:
                        item_relationships = self.get_item_relationships(project_id, item_id, filters, access_token)
                        all_relationships.extend(item_relationships)
                
                return all_relationships
            
        except Exception as e:
            print(f"获取文件夹关系失败: {e}")
        
        return []
    
    def _format_relationships_data(self, raw_data):
        """格式化关系数据"""
        relationships = []
        
        data_items = raw_data.get('data', [])
        included_items = raw_data.get('included', [])
        
        # 创建included items的映射
        included_map = {}
        for item in included_items:
            included_map[item.get('id')] = item
        
        for relationship in data_items:
            try:
                # 基本关系信息
                rel_id = relationship.get('id', '')
                rel_type = relationship.get('type', '')
                
                # 元数据
                meta = relationship.get('meta', {})
                ref_type = meta.get('refType', '')
                direction = meta.get('direction', '')
                extension = meta.get('extension', {})
                
                # 目标信息
                target_data = relationship.get('relationships', {}).get('target', {}).get('data', {})
                target_id = target_data.get('id', '')
                target_type = target_data.get('type', '')
                
                # 从included中获取目标详细信息
                target_details = included_map.get(target_id, {})
                target_attributes = target_details.get('attributes', {})
                
                formatted_relationship = {
                    'id': rel_id,
                    'type': rel_type,
                    'ref_type': ref_type,
                    'ref_type_display': self.type_manager.format_ref_type_for_display(ref_type),
                    'direction': direction,
                    'target': {
                        'id': target_id,
                        'type': target_type,
                        'name': target_attributes.get('displayName', ''),
                        'file_type': target_attributes.get('fileType', ''),
                        'file_size': target_attributes.get('storageSize', 0),
                        'created_time': target_attributes.get('createTime', ''),
                        'modified_time': target_attributes.get('lastModifiedTime', ''),
                        'version_number': target_attributes.get('versionNumber', 1)
                    },
                    'extension': extension,
                    'created_at': meta.get('createdAt', ''),
                    'created_by': meta.get('createdBy', '')
                }
                
                relationships.append(formatted_relationship)
                
            except Exception as e:
                print(f"格式化关系数据时出错: {e}")
                continue
        
        return relationships
    
    def _enhance_relationships_data(self, relationships, project_id, access_token):
        """增强关系数据，添加更多详细信息"""
        enhanced = []
        
        for relationship in relationships:
            try:
                enhanced_rel = relationship.copy()
                
                # 添加下载链接（如果是文件）
                target = relationship.get('target', {})
                if target.get('type') == 'versions':
                    download_url = self._get_download_url(project_id, target.get('id'), access_token)
                    if download_url:
                        enhanced_rel['target']['download_url'] = download_url
                
                # 添加预览链接
                preview_url = self._get_preview_url(project_id, target.get('id'), target.get('type'))
                if preview_url:
                    enhanced_rel['target']['preview_url'] = preview_url
                
                # 格式化时间
                if enhanced_rel['target'].get('created_time'):
                    enhanced_rel['target']['created_time_formatted'] = utils.format_timestamp(enhanced_rel['target']['created_time'])
                
                if enhanced_rel['target'].get('modified_time'):
                    enhanced_rel['target']['modified_time_formatted'] = utils.format_timestamp(enhanced_rel['target']['modified_time'])
                
                enhanced.append(enhanced_rel)
                
            except Exception as e:
                print(f"增强关系数据时出错: {e}")
                enhanced.append(relationship)  # 保留原始数据
        
        return enhanced
    
    def _get_download_url(self, project_id, version_id, access_token):
        """获取文件下载链接"""
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            encoded_version_id = urllib.parse.quote(version_id, safe='')
            url = f"{self.base_url}/projects/{project_id}/versions/{encoded_version_id}/downloads"
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('url', '')
        except Exception as e:
            print(f"获取下载链接失败: {e}")
        
        return None
    
    def _get_preview_url(self, project_id, item_id, item_type):
        """获取预览链接"""
        try:
            # 构建ACC web界面的预览链接
            if item_type in ['items', 'versions']:
                return f"https://docs.b360.autodesk.com/projects/{project_id}/folders/{item_id}"
        except Exception as e:
            print(f"构建预览链接失败: {e}")
        
        return None


# ==================== API端点实现 ====================

@relations_bp.route('/api/relations/projects/<project_id>/items/<item_id>')
def get_item_relations(project_id, item_id):
    """
    获取指定item的所有关系
    
    Query Parameters:
    - ref_types: 关系类型过滤 (xrefs,includes,dependencies)
    - target_types: 目标类型过滤 (items,versions,folders)
    - direction: 方向过滤 (from,to)
    - limit: 结果数量限制
    - offset: 分页偏移
    """
    try:
        # 获取查询参数
        ref_types = request.args.get('ref_types', '').split(',') if request.args.get('ref_types') else None
        target_types = request.args.get('target_types', '').split(',') if request.args.get('target_types') else None
        direction = request.args.get('direction')
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # 构建过滤器
        filters = {}
        if ref_types:
            filters['ref_types'] = [rt.strip() for rt in ref_types if rt.strip()]
        if target_types:
            filters['target_types'] = [tt.strip() for tt in target_types if tt.strip()]
        if direction:
            filters['direction'] = direction
        filters['limit'] = min(limit, 200)  # 最大200
        filters['offset'] = offset
        
        # 获取关系
        relations_manager = RelationsManager()
        relationships = relations_manager.get_item_relationships(project_id, item_id, filters)
        
        # 统计信息
        stats = {
            'total_relationships': len(relationships),
            'ref_type_counts': {},
            'target_type_counts': {},
            'direction_counts': {'from': 0, 'to': 0}
        }
        
        for rel in relationships:
            # 统计关系类型
            ref_type = rel.get('ref_type', 'unknown')
            stats['ref_type_counts'][ref_type] = stats['ref_type_counts'].get(ref_type, 0) + 1
            
            # 统计目标类型
            target_type = rel.get('target', {}).get('type', 'unknown')
            stats['target_type_counts'][target_type] = stats['target_type_counts'].get(target_type, 0) + 1
            
            # 统计方向
            direction = rel.get('direction', '')
            if direction in stats['direction_counts']:
                stats['direction_counts'][direction] += 1
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "item_id": item_id,
            "filters": filters,
            "stats": stats,
            "relationships": relationships,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"获取item关系时出错: {e}")
        return jsonify({
            "success": False,
            "error": f"获取item关系失败: {str(e)}",
            "project_id": project_id,
            "item_id": item_id,
            "timestamp": datetime.now().isoformat()
        }), 500


@relations_bp.route('/api/relations/projects/<project_id>/versions/<version_id>')
def get_version_relations(project_id, version_id):
    """获取指定version的所有关系"""
    try:
        # 获取查询参数
        ref_types = request.args.get('ref_types', '').split(',') if request.args.get('ref_types') else None
        target_types = request.args.get('target_types', '').split(',') if request.args.get('target_types') else None
        direction = request.args.get('direction')
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # 构建过滤器
        filters = {}
        if ref_types:
            filters['ref_types'] = [rt.strip() for rt in ref_types if rt.strip()]
        if target_types:
            filters['target_types'] = [tt.strip() for tt in target_types if tt.strip()]
        if direction:
            filters['direction'] = direction
        filters['limit'] = min(limit, 200)  # 最大200
        filters['offset'] = offset
        
        # 获取关系
        relations_manager = RelationsManager()
        relationships = relations_manager.get_version_relationships(project_id, version_id, filters)
        
        # 统计信息
        stats = {
            'total_relationships': len(relationships),
            'ref_type_counts': {},
            'target_type_counts': {}
        }
        
        for rel in relationships:
            ref_type = rel.get('ref_type', 'unknown')
            stats['ref_type_counts'][ref_type] = stats['ref_type_counts'].get(ref_type, 0) + 1
            
            target_type = rel.get('target', {}).get('type', 'unknown')
            stats['target_type_counts'][target_type] = stats['target_type_counts'].get(target_type, 0) + 1
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "version_id": version_id,
            "filters": filters,
            "stats": stats,
            "relationships": relationships,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"获取version关系时出错: {e}")
        return jsonify({
            "success": False,
            "error": f"获取version关系失败: {str(e)}",
            "project_id": project_id,
            "version_id": version_id,
            "timestamp": datetime.now().isoformat()
        }), 500


@relations_bp.route('/api/relations/references')
def get_references():
    """
    专门获取参照关系的端点
    支持多种实体类型：RFI, Issue, Submittal等
    
    Query Parameters:
    - entity_type: 实体类型 (rfi, issue, submittal)
    - entity_id: 实体ID
    - project_id: 项目ID
    - reference_types: 参照类型 (document, file, external)
    """
    try:
        # 获取查询参数
        entity_type = request.args.get('entity_type')
        entity_id = request.args.get('entity_id')
        project_id = request.args.get('project_id')
        reference_types = request.args.get('reference_types', '').split(',') if request.args.get('reference_types') else None
        
        # 验证必需参数
        if not all([entity_type, entity_id, project_id]):
            return jsonify({
                "success": False,
                "error": "缺少必需参数: entity_type, entity_id, project_id",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        # 验证实体类型
        type_manager = RelationshipTypeManager()
        supported_types = list(type_manager.ENTITY_TYPES.keys())
        if entity_type not in supported_types:
            return jsonify({
                "success": False,
                "error": f"不支持的实体类型: {entity_type}. 支持的类型: {', '.join(supported_types)}",
                "supported_types": supported_types,
                "entity_categories": type_manager.ENTITY_CATEGORIES,
                "timestamp": datetime.now().isoformat()
            }), 400
        
        # 获取参照关系
        relations_manager = RelationsManager()
        references = relations_manager.get_entity_references(
            entity_type, entity_id, project_id, reference_types
        )
        
        # 统计信息
        stats = {
            'total_references': len(references),
            'reference_type_counts': {},
            'file_type_counts': {},
            'total_file_size': 0
        }
        
        for ref in references:
            # 统计参照类型
            ref_type = ref.get('ref_type', 'unknown')
            stats['reference_type_counts'][ref_type] = stats['reference_type_counts'].get(ref_type, 0) + 1
            
            # 统计文件类型
            file_type = ref.get('target', {}).get('file_type', 'unknown')
            if file_type:
                stats['file_type_counts'][file_type] = stats['file_type_counts'].get(file_type, 0) + 1
            
            # 统计文件大小
            file_size = ref.get('target', {}).get('file_size', 0)
            if isinstance(file_size, (int, float)):
                stats['total_file_size'] += file_size
        
        return jsonify({
            "success": True,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "project_id": project_id,
            "reference_types": reference_types,
            "stats": stats,
            "references": references,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"获取参照关系时出错: {e}")
        return jsonify({
            "success": False,
            "error": f"获取参照关系失败: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500


@relations_bp.route('/api/relations/references/<project_id>/<entity_type>/<entity_id>/<reference_id>/download')
def download_reference_document(project_id, entity_type, entity_id, reference_id):
    """下载参照文档（复用附件下载逻辑）"""
    print(f"🚀 [参照下载] 开始处理下载请求:")
    print(f"   - project_id: {project_id}")
    print(f"   - entity_type: {entity_type}")
    print(f"   - entity_id: {entity_id}")
    print(f"   - reference_id: {reference_id}")
    
    access_token = utils.get_access_token()
    if not access_token:
        return jsonify({
            "error": "未找到 Access Token，请先进行认证",
            "status": "unauthorized"
        }), 401
    
    try:
        # 1. 获取参照信息
        relations_manager = RelationsManager()
        references = relations_manager.get_entity_references(entity_type, entity_id, project_id, None, access_token)
        
        # 2. 找到指定的参照
        target_reference = None
        for ref in references:
            if ref.get('id') == reference_id:
                target_reference = ref
                break
        
        if not target_reference:
            return jsonify({
                "error": "Reference does not exist",
                "status": "not_found"
            }), 404
        
        # 3. 获取参照的URN信息
        target_info = target_reference.get('target', {})
        storage_urn = target_info.get('storage_urn')
        target_id = target_reference.get('target_id')
        document_name = target_info.get('name', 'document')
        
        print(f"参照下载信息:")
        print(f"  - storage_urn: {storage_urn}")
        print(f"  - target_id: {target_id}")
        print(f"  - document_name: {document_name}")
        
        if not storage_urn and not target_id:
            return jsonify({
                "error": "Unable to get reference document download information",
                "status": "error"
            }), 500
        
        # 4. 使用通用URN下载模块
        download_result = None
        
        # 优先使用target_id，然后是storage_urn
        urn_to_use = target_id or storage_urn
        
        if urn_to_use and 'dm.lineage:' in urn_to_use:
            print(f"使用Document Lineage下载: {urn_to_use}")
            download_result = download_document_lineage(
                urn_to_use, project_id, access_token, document_name
            )
        elif urn_to_use:
            print(f"使用通用URN下载: {urn_to_use}")
            download_result = download_by_urn(urn_to_use, access_token, document_name)
        else:
            print("没有可用的URN进行下载")
            download_result = {
                "success": False,
                "error": "没有可用的URN进行下载",
                "status": "no_urn"
            }
        
        # 检查下载结果
        if download_result and download_result.get('success'):
            print(f"✅ 成功获取参照文档下载链接")
            return jsonify({
                "success": True,
                "download_url": download_result.get('download_url'),
                "document_name": download_result.get('document_name', document_name),
                "reference_id": reference_id,
                "requires_auth": download_result.get('requires_auth', False),
                "method": download_result.get('method', 'urn_download_module')
            })
        
        # 如果下载失败，返回错误信息
        error_msg = "Unable to get reference document download link"
        if download_result:
            error_msg = download_result.get('error', error_msg)
        
        return jsonify({
            "error": error_msg,
            "status": "error",
            "debug_info": {
                "reference_id": reference_id,
                "entity_type": entity_type,
                "entity_id": entity_id,
                "project_id": project_id,
                "storage_urn": storage_urn,
                "target_id": target_id,
                "document_name": document_name,
                "download_result": download_result,
                "methods_tried": ["URN Download Module"]
            }
        }), 500
        
    except Exception as e:
        print(f"参照下载失败: {str(e)}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@relations_bp.route('/api/relations/references/batch', methods=['POST'])
def get_references_batch():
    """
    批量获取多个实体的参照关系
    
    Request Body:
    {
        "requests": [
            {
                "entity_type": "rfi",
                "entity_id": "xxx",
                "project_id": "xxx",
                "reference_types": ["document", "file"]
            }
        ]
    }
    """
    try:
        # 获取请求数据
        request_data = request.get_json() or {}
        requests_list = request_data.get('requests', [])
        
        if not requests_list:
            return jsonify({
                "success": False,
                "error": "请求体中缺少requests数组",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        # 限制批量请求数量
        if len(requests_list) > 50:
            return jsonify({
                "success": False,
                "error": "批量请求数量不能超过50个",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        relations_manager = RelationsManager()
        results = []
        
        # 使用线程池并行处理
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_request = {}
            
            for req in requests_list:
                entity_type = req.get('entity_type')
                entity_id = req.get('entity_id')
                project_id = req.get('project_id')
                reference_types = req.get('reference_types')
                
                if not all([entity_type, entity_id, project_id]):
                    results.append({
                        "success": False,
                        "error": "Missing required parameters",
                        "request": req
                    })
                    continue
                
                future = executor.submit(
                    relations_manager.get_entity_references,
                    entity_type, entity_id, project_id, reference_types
                )
                future_to_request[future] = req
            
            # 收集结果
            for future in as_completed(future_to_request):
                req = future_to_request[future]
                try:
                    references = future.result()
                    results.append({
                        "success": True,
                        "entity_type": req.get('entity_type'),
                        "entity_id": req.get('entity_id'),
                        "project_id": req.get('project_id'),
                        "references": references,
                        "reference_count": len(references)
                    })
                except Exception as e:
                    results.append({
                        "success": False,
                        "error": str(e),
                        "request": req
                    })
        
        # 整体统计
        total_references = sum(r.get('reference_count', 0) for r in results if r.get('success'))
        successful_requests = sum(1 for r in results if r.get('success'))
        failed_requests = len(results) - successful_requests
        
        return jsonify({
            "success": True,
            "batch_stats": {
                "total_requests": len(requests_list),
                "successful_requests": successful_requests,
                "failed_requests": failed_requests,
                "total_references": total_references
            },
            "results": results,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"批量获取参照关系时出错: {e}")
        return jsonify({
            "success": False,
            "error": f"批量获取参照关系失败: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500


@relations_bp.route('/api/relations/search', methods=['POST'])
def search_relations():
    """
    通用关系搜索接口
    
    Request Body:
    {
        "project_id": "xxx",
        "source_id": "xxx",
        "source_type": "item|version",
        "filters": {
            "ref_types": ["xrefs", "includes"],
            "target_types": ["items", "versions"],
            "direction": "from|to"
        }
    }
    """
    try:
        # 获取请求数据
        search_data = request.get_json() or {}
        
        project_id = search_data.get('project_id')
        source_id = search_data.get('source_id')
        source_type = search_data.get('source_type', 'item')
        filters = search_data.get('filters', {})
        
        # 验证必需参数
        if not all([project_id, source_id]):
            return jsonify({
                "success": False,
                "error": "缺少必需参数: project_id, source_id",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        # 验证源类型
        if source_type not in ['item', 'version']:
            return jsonify({
                "success": False,
                "error": "source_type必须是'item'或'version'",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        # 获取关系
        relations_manager = RelationsManager()
        
        if source_type == 'item':
            relationships = relations_manager.get_item_relationships(project_id, source_id, filters)
        else:
            relationships = relations_manager.get_version_relationships(project_id, source_id, filters)
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "source_id": source_id,
            "source_type": source_type,
            "filters": filters,
            "relationships": relationships,
            "relationship_count": len(relationships),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"搜索关系时出错: {e}")
        return jsonify({
            "success": False,
            "error": f"搜索关系失败: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500


# ==================== 辅助端点 ====================

@relations_bp.route('/api/relations/types')
def get_supported_types():
    """获取支持的关系类型和实体类型"""
    type_manager = RelationshipTypeManager()
    
    # 构建支持的实体类型信息
    supported_entities = {}
    for entity_type, entity_config in type_manager.ENTITY_TYPES.items():
        supported_entities[entity_type] = {
            "display_name": entity_config['display_name'],
            "icon": entity_config['icon'],
            "category": entity_config['category'],
            "supported_references": entity_config['supported_references']
        }
    
    return jsonify({
        "success": True,
        "reference_types": type_manager.REFERENCE_TYPES,
        "target_types": type_manager.TARGET_TYPES,
        "directions": type_manager.DIRECTIONS,
        "entity_types": supported_entities,
        "entity_categories": type_manager.ENTITY_CATEGORIES,
        "timestamp": datetime.now().isoformat()
    })


@relations_bp.route('/api/relations/entity-categories')
def get_entity_categories():
    """获取实体分类信息"""
    type_manager = RelationshipTypeManager()
    
    return jsonify({
        "success": True,
        "categories": type_manager.ENTITY_CATEGORIES,
        "entity_types": type_manager.ENTITY_TYPES,
        "timestamp": datetime.now().isoformat()
    })


@relations_bp.route('/api/relations/health')
def health_check():
    """健康检查端点"""
    return jsonify({
        "success": True,
        "service": "Data Management Relations API",
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })
