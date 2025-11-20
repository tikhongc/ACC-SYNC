"""
自定义属性API模块
提供获取和管理文件夹自定义属性定义的功能
"""

import requests
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from flask import Blueprint, request, jsonify
import utils

logger = logging.getLogger(__name__)

class CustomAttributesAPI:
    """自定义属性API类"""
    
    def __init__(self):
        self.base_url = "https://developer.api.autodesk.com/bim360/docs/v1"
        
    def get_custom_attribute_definitions(self, project_id: str, folder_id: str, 
                                       limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """
        获取指定文件夹的自定义属性定义
        
        Args:
            project_id: 项目ID
            folder_id: 文件夹ID (URL编码的URN)
            limit: 返回结果数量限制 (1-200, 默认100)
            offset: 偏移量 (默认0)
            
        Returns:
            包含自定义属性定义列表和分页信息的字典
        """
        try:
            # 获取访问令牌
            token = utils.get_access_token()
            if not token:
                return {"error": "Unable to get access token"}
            
            # 处理项目ID格式 - 移除 "b." 前缀
            clean_project_id = project_id
            if project_id.startswith('b.'):
                clean_project_id = project_id[2:]
            
            # 构建请求URL
            url = f"{self.base_url}/projects/{clean_project_id}/folders/{folder_id}/custom-attribute-definitions"
            
            # 设置请求头
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            # 设置查询参数
            params = {
                'limit': min(max(limit, 1), 200),  # 限制在1-200之间
                'offset': max(offset, 0)  # 确保非负数
            }
            
            logger.info(f"获取自定义属性定义: project_id={project_id}, folder_id={folder_id}")
            
            # 发送请求
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # 处理响应数据
                processed_data = self._process_custom_attributes_response(data)
                
                logger.info(f"成功获取 {len(processed_data.get('results', []))} 个自定义属性定义")
                return processed_data
                
            else:
                error_msg = f"获取自定义属性定义失败: HTTP {response.status_code}"
                if response.text:
                    try:
                        error_data = response.json()
                        if 'message' in error_data:
                            error_msg += f" - {error_data['message']}"
                    except:
                        error_msg += f" - {response.text[:200]}"
                
                logger.error(error_msg)
                return {"error": error_msg}
                
        except requests.exceptions.Timeout:
            error_msg = "请求超时，请稍后重试"
            logger.error(f"获取自定义属性定义超时: {error_msg}")
            return {"error": error_msg}
            
        except requests.exceptions.RequestException as e:
            error_msg = f"网络请求错误: {str(e)}"
            logger.error(f"获取自定义属性定义网络错误: {error_msg}")
            return {"error": error_msg}
            
        except Exception as e:
            error_msg = f"获取自定义属性定义时发生未知错误: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}
    
    def _process_custom_attributes_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理自定义属性定义响应数据
        
        Args:
            data: 原始响应数据
            
        Returns:
            处理后的数据
        """
        try:
            results = data.get('results', [])
            processed_results = []
            
            for attr in results:
                processed_attr = {
                    'id': attr.get('id'),
                    'name': attr.get('name'),
                    'type': attr.get('type'),
                    'description': attr.get('description', ''),
                    'required': attr.get('required', False),
                    'arrayValues': attr.get('arrayValues', []),
                    'defaultValue': attr.get('defaultValue'),
                    'maxLength': attr.get('maxLength'),
                    'minLength': attr.get('minLength'),
                    'displayName': self._get_display_name(attr),
                    'typeDisplayName': self._get_type_display_name(attr.get('type')),
                    'hasOptions': bool(attr.get('arrayValues'))
                }
                processed_results.append(processed_attr)
            
            return {
                'results': processed_results,
                'pagination': data.get('pagination', {}),
                'summary': {
                    'total_attributes': len(processed_results),
                    'string_attributes': len([a for a in processed_results if a['type'] == 'string']),
                    'array_attributes': len([a for a in processed_results if a['type'] == 'array']),
                    'date_attributes': len([a for a in processed_results if a['type'] == 'date']),
                    'number_attributes': len([a for a in processed_results if a['type'] == 'number']),
                    'required_attributes': len([a for a in processed_results if a['required']])
                }
            }
            
        except Exception as e:
            logger.error(f"处理自定义属性定义响应数据时出错: {str(e)}")
            return data
    
    def _get_display_name(self, attr: Dict[str, Any]) -> str:
        """获取属性的显示名称"""
        name = attr.get('name', '')
        if attr.get('required'):
            return f"{name} *"
        return name
    
    def _get_type_display_name(self, attr_type: str) -> str:
        """获取属性类型的显示名称"""
        type_map = {
            'string': 'Text',
            'array': 'Options',
            'date': 'Date',
            'number': 'Number',
            'boolean': 'Boolean'
        }
        return type_map.get(attr_type, attr_type)
    
    def get_file_custom_attributes(self, project_id: str, version_ids: List[str]) -> Dict[str, Any]:
        """
        获取文件版本的自定义属性值
        
        Args:
            project_id: 项目ID
            version_ids: 文件版本ID列表
            
        Returns:
            包含文件自定义属性值的字典
        """
        try:
            # 获取访问令牌
            token = utils.get_access_token()
            if not token:
                return {"error": "Unable to get access token"}
            
            # 处理项目ID格式 - 移除 "b." 前缀
            clean_project_id = project_id
            if project_id.startswith('b.'):
                clean_project_id = project_id[2:]
            
            # 构建请求URL
            url = f"{self.base_url}/projects/{clean_project_id}/versions:batch-get"
            
            # 设置请求头
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            # 构建请求体 - 根据API文档，不需要includeCustomAttributes参数，自定义属性会自动包含
            payload = {
                "urns": version_ids
            }
            
            logger.info(f"获取文件自定义属性值: project_id={project_id}, versions={len(version_ids)}")
            
            # 发送POST请求
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                # 添加调试信息
                logger.info(f"ACC API响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
                
                # 处理响应数据
                processed_data = self._process_file_custom_attributes_response(data)
                
                logger.info(f"成功获取 {len(processed_data.get('results', []))} 个文件的自定义属性")
                return processed_data
                
            else:
                error_msg = f"获取文件自定义属性值失败: HTTP {response.status_code}"
                if response.text:
                    try:
                        error_data = response.json()
                        if 'message' in error_data:
                            error_msg += f" - {error_data['message']}"
                    except:
                        error_msg += f" - {response.text[:200]}"
                
                logger.error(error_msg)
                return {"error": error_msg}
                
        except requests.exceptions.Timeout:
            error_msg = "请求超时，请稍后重试"
            logger.error(f"获取文件自定义属性值超时: {error_msg}")
            return {"error": error_msg}
            
        except requests.exceptions.RequestException as e:
            error_msg = f"网络请求错误: {str(e)}"
            logger.error(f"获取文件自定义属性值网络错误: {error_msg}")
            return {"error": error_msg}
            
        except Exception as e:
            error_msg = f"获取文件自定义属性值时发生未知错误: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}
    
    def _process_file_custom_attributes_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        处理文件自定义属性值响应数据
        
        Args:
            data: 原始响应数据
            
        Returns:
            处理后的数据
        """
        try:
            results = data.get('results', [])
            processed_results = {}
            
            logger.info(f"🔍 DEBUG: 處理 {len(results)} 個文件的響應數據")
            
            for file_data in results:
                # 根据API文档，主要字段是urn
                version_id = file_data.get('urn')
                # 如果urn为空，尝试从其他字段获取
                if not version_id:
                    version_id = file_data.get('id') or file_data.get('versionUrn')
                
                # 根据API文档，customAttributes是直接在根级别的数组
                custom_attributes = file_data.get('customAttributes', [])
                
                logger.info(f"🔍 DEBUG: 文件 {version_id} 找到 {len(custom_attributes)} 個自定義屬性")
                logger.info(f"🔍 DEBUG: 自定義屬性數據: {custom_attributes}")
                
                # 处理自定义属性 - 将数组转换为字典格式
                processed_attributes = {}
                if isinstance(custom_attributes, list):
                    for attr in custom_attributes:
                        if isinstance(attr, dict):
                            attr_id = attr.get('id')
                            attr_name = attr.get('name')
                            attr_value = attr.get('value')
                            attr_type = attr.get('type')
                            
                            if attr_id:  # 确保有ID
                                processed_attributes[str(attr_id)] = {
                                    'id': attr_id,
                                    'name': attr_name,
                                    'value': attr_value,
                                    'type': attr_type,
                                    'displayValue': self._format_attribute_value(attr_value, attr_type)
                                }
                
                processed_results[version_id] = {
                    'customAttributes': processed_attributes,
                    'hasCustomAttributes': len(processed_attributes) > 0
                }
            
            return {
                'results': processed_results,
                'total_files': len(processed_results)
            }
            
        except Exception as e:
            logger.error(f"处理文件自定义属性值响应数据时出错: {str(e)}")
            return data
    
    def _format_attribute_value(self, value: Any, attr_type: str) -> str:
        """格式化属性值用于显示"""
        if value is None:
            return ""
        
        if attr_type == 'date' and value:
            try:
                # 尝试格式化日期，转换为北京时间
                from datetime import datetime, timezone, timedelta
                if isinstance(value, str):
                    date_obj = datetime.fromisoformat(value.replace('Z', '+00:00'))
                    # 转换为北京时间（UTC+8）
                    beijing_tz = timezone(timedelta(hours=8))
                    beijing_date = date_obj.astimezone(beijing_tz)
                    return beijing_date.strftime('%Y-%m-%d')
            except:
                pass
        
        return str(value)

    def get_folder_custom_attributes_summary(self, project_id: str, folder_id: str) -> Dict[str, Any]:
        """
        获取文件夹自定义属性摘要信息
        
        Args:
            project_id: 项目ID
            folder_id: 文件夹ID
            
        Returns:
            自定义属性摘要信息
        """
        try:
            # 获取所有自定义属性定义
            result = self.get_custom_attribute_definitions(project_id, folder_id, limit=200)
            
            if 'error' in result:
                return result
            
            # 返回摘要信息
            return {
                'success': True,
                'summary': result.get('summary', {}),
                'total_count': len(result.get('results', [])),
                'has_custom_attributes': len(result.get('results', [])) > 0
            }
            
        except Exception as e:
            error_msg = f"获取自定义属性摘要时发生错误: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}

# 创建全局实例
custom_attributes_api = CustomAttributesAPI()

def get_custom_attribute_definitions(project_id: str, folder_id: str, 
                                   limit: int = 100, offset: int = 0) -> Dict[str, Any]:
    """
    获取自定义属性定义的便捷函数
    
    Args:
        project_id: 项目ID
        folder_id: 文件夹ID
        limit: 结果数量限制
        offset: 偏移量
        
    Returns:
        自定义属性定义数据
    """
    return custom_attributes_api.get_custom_attribute_definitions(
        project_id, folder_id, limit, offset
    )

def get_folder_custom_attributes_summary(project_id: str, folder_id: str) -> Dict[str, Any]:
    """
    获取文件夹自定义属性摘要的便捷函数
    
    Args:
        project_id: 项目ID
        folder_id: 文件夹ID
        
    Returns:
        自定义属性摘要信息
    """
    return custom_attributes_api.get_folder_custom_attributes_summary(project_id, folder_id)

# 创建蓝图
custom_attributes_bp = Blueprint('custom_attributes', __name__, url_prefix='/api/custom-attributes')

@custom_attributes_bp.route('/projects/<project_id>/folders/<path:folder_id>/definitions', methods=['GET'])
def get_folder_custom_attribute_definitions(project_id, folder_id):
    """
    获取指定文件夹的自定义属性定义
    
    Args:
        project_id: 项目ID
        folder_id: 文件夹ID (URL编码的URN)
        
    Query Parameters:
        limit: 返回结果数量限制 (1-200, 默认100)
        offset: 偏移量 (默认0)
        
    Returns:
        JSON响应包含自定义属性定义列表
    """
    try:
        # 获取查询参数
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # 调用API获取数据
        result = custom_attributes_api.get_custom_attribute_definitions(
            project_id, folder_id, limit, offset
        )
        
        if 'error' in result:
            return jsonify(result), 400
            
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"获取自定义属性定义时发生错误: {str(e)}")
        return jsonify({"error": f"获取自定义属性定义失败: {str(e)}"}), 500

@custom_attributes_bp.route('/projects/<project_id>/folders/<path:folder_id>/summary', methods=['GET'])
def get_folder_custom_attributes_summary_endpoint(project_id, folder_id):
    """
    获取文件夹自定义属性摘要信息
    
    Args:
        project_id: 项目ID
        folder_id: 文件夹ID
        
    Returns:
        JSON响应包含自定义属性摘要信息
    """
    try:
        # 调用API获取摘要数据
        result = custom_attributes_api.get_folder_custom_attributes_summary(project_id, folder_id)
        
        if 'error' in result:
            return jsonify(result), 400
            
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"获取自定义属性摘要时发生错误: {str(e)}")
        return jsonify({"error": f"获取自定义属性摘要失败: {str(e)}"}), 500

@custom_attributes_bp.route('/projects/<project_id>/files/custom-attributes', methods=['POST'])
def get_files_custom_attributes(project_id):
    """
    获取多个文件的自定义属性值
    
    Args:
        project_id: 项目ID
        
    Request Body:
        {
            "version_ids": ["urn:adsk.wipprod:fs.file:vf.xxx", ...]
        }
        
    Returns:
        JSON响应包含文件自定义属性值
    """
    try:
        # 获取请求体数据
        data = request.get_json()
        if not data or 'version_ids' not in data:
            return jsonify({"error": "请求体中缺少version_ids参数"}), 400
        
        version_ids = data['version_ids']
        if not isinstance(version_ids, list) or not version_ids:
            return jsonify({"error": "version_ids必须是非空数组"}), 400
        
        # 调用API获取数据
        result = custom_attributes_api.get_file_custom_attributes(project_id, version_ids)
        
        if 'error' in result:
            return jsonify(result), 400
            
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"获取文件自定义属性值时发生错误: {str(e)}")
        return jsonify({"error": f"获取文件自定义属性值失败: {str(e)}"}), 500

@custom_attributes_bp.route('/health', methods=['GET'])
def custom_attributes_health():
    """自定义属性API健康检查"""
    return jsonify({
        "status": "healthy",
        "service": "custom_attributes_api",
        "timestamp": datetime.now().isoformat()
    })
