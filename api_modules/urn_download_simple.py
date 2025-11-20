# -*- coding: utf-8 -*-
"""
Simple URN Download Module
Provides unified URN download functionality with ASCII-only output
"""

import requests
import json
from urllib.parse import quote
import config
import utils


class URNDownloadManager:
    """URN Download Manager - Provides unified URN download functionality"""
    
    def __init__(self):
        self.base_url = config.AUTODESK_API_BASE
    
    def get_document_info_by_urn(self, urn, project_id=None, access_token=None):
        """
        获取URN对应的文档详细信息，包括文件名
        
        Args:
            urn (str): 文档URN标识符
            project_id (str): 项目ID (对于dm.lineage类型URN必需)
            access_token (str): 访问令牌
            
        Returns:
            dict: 包含文档信息的结果
        """
        if not access_token:
            access_token = utils.get_access_token()
            
        if not access_token:
            return {
                "success": False,
                "error": "Access token not found",
                "status": "unauthorized"
            }
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        print(f"[URN Info] Getting document info for URN: {urn}")
        
        # 根据URN类型选择不同的信息获取方法
        if 'dm.lineage:' in urn:
            return self._get_document_lineage_info(urn, project_id, headers)
        elif 'os.object:' in urn:
            return self._get_oss_object_info(urn, headers)
        else:
            return {
                "success": False,
                "error": f"Unsupported URN type: {urn}",
                "status": "unsupported_urn_type",
                "urn": urn
            }
    
    def _get_document_lineage_info(self, lineage_urn, project_id, headers):
        """获取Document Lineage类型URN的文档信息"""
        try:
            if not project_id:
                return {
                    "success": False,
                    "error": "Project ID is required for Document Lineage URN",
                    "status": "missing_project_id",
                    "urn": lineage_urn
                }
            
            print(f"[Document Lineage Info] Processing: {lineage_urn}")
            
            # 清理项目ID
            clean_project_id = project_id[2:] if project_id.startswith('b.') else project_id
            
            # 获取版本信息
            versions_url = f"{self.base_url}/data/v1/projects/b.{clean_project_id}/items/{quote(lineage_urn, safe='')}/versions"
            
            print(f"Getting versions info: {versions_url}")
            versions_resp = requests.get(versions_url, headers=headers, timeout=30)
            
            if versions_resp.status_code == 200:
                versions_data = versions_resp.json()
                versions = versions_data.get('data', [])
                
                if versions:
                    latest_version = versions[0]  # 第一个通常是最新版本
                    version_id = latest_version.get('id')
                    
                    # 从版本数据中提取文件信息
                    attributes = latest_version.get('attributes', {})
                    file_name = attributes.get('displayName') or attributes.get('name', 'Unknown Document')
                    file_type = attributes.get('fileType', 'unknown')
                    file_size = attributes.get('storageSize', 0)
                    version_number = attributes.get('versionNumber', 1)
                    create_time = attributes.get('createTime')
                    last_modified_time = attributes.get('lastModifiedTime')
                    
                    # 获取存储URN
                    storage_relationship = latest_version.get('relationships', {}).get('storage', {})
                    storage_urn = None
                    if storage_relationship:
                        storage_data = storage_relationship.get('data', {})
                        storage_urn = storage_data.get('id')
                    
                    return {
                        "success": True,
                        "document_info": {
                            "name": file_name,
                            "file_type": file_type,
                            "file_size": file_size,
                            "version_number": version_number,
                            "version_id": version_id,
                            "create_time": create_time,
                            "last_modified_time": last_modified_time,
                            "lineage_urn": lineage_urn,
                            "storage_urn": storage_urn,
                            "mime_type": self._get_mime_type_from_extension(file_name)
                        },
                        "urn": lineage_urn
                    }
                else:
                    return {
                        "success": False,
                        "error": "No versions found for this lineage",
                        "status": "no_versions",
                        "urn": lineage_urn
                    }
            else:
                print(f"Failed to get versions: {versions_resp.status_code} - {versions_resp.text}")
                return {
                    "success": False,
                    "error": f"Failed to get versions: {versions_resp.status_code}",
                    "status": "versions_api_failed",
                    "urn": lineage_urn
                }
                
        except Exception as e:
            print(f"ERROR: Document Lineage info failed: {e}")
            return {
                "success": False,
                "error": f"Document Lineage info failed: {str(e)}",
                "status": "info_failed",
                "urn": lineage_urn
            }
    
    def _get_oss_object_info(self, storage_urn, headers):
        """获取OSS Object类型URN的文档信息"""
        try:
            print(f"[OSS Object Info] Processing: {storage_urn}")
            
            # 解析存储URN: urn:adsk.objects:os.object:bucket/object_key
            if 'os.object:' not in storage_urn:
                return {
                    "success": False,
                    "error": "Invalid OSS Object URN format",
                    "status": "invalid_urn",
                    "urn": storage_urn
                }
            
            object_part = storage_urn.split('os.object:')[1]
            
            # 分离bucket和object key
            if '/' in object_part:
                bucket_key = object_part.split('/')[0]
                object_key = '/'.join(object_part.split('/')[1:])
            else:
                bucket_key = 'wip.dm.prod'  # 默认bucket
                object_key = object_part
            
            print(f"Parsed OSS URN: bucket={bucket_key}, object={object_key}")
            
            # 从object_key中提取文件名
            file_name = object_key.split('/')[-1] if '/' in object_key else object_key
            
            # 尝试获取OSS对象详细信息
            encoded_object_key = quote(object_key, safe='')
            oss_details_url = f"{self.base_url}/oss/v2/buckets/{bucket_key}/objects/{encoded_object_key}/details"
            
            print(f"Getting OSS object details: {oss_details_url}")
            
            try:
                oss_resp = requests.get(oss_details_url, headers=headers, timeout=30)
                
                if oss_resp.status_code == 200:
                    oss_data = oss_resp.json()
                    
                    return {
                        "success": True,
                        "document_info": {
                            "name": file_name,
                            "file_type": self._get_file_extension(file_name),
                            "file_size": oss_data.get('size', 0),
                            "version_number": 1,
                            "create_time": oss_data.get('createdDate'),
                            "last_modified_time": oss_data.get('lastModifiedDate'),
                            "storage_urn": storage_urn,
                            "bucket": bucket_key,
                            "object_key": object_key,
                            "mime_type": self._get_mime_type_from_extension(file_name)
                        },
                        "urn": storage_urn
                    }
                else:
                    print(f"OSS details API failed: {oss_resp.status_code}, using fallback info")
            except Exception as e:
                print(f"OSS details request failed: {e}, using fallback info")
            
            # 如果无法获取详细信息，返回basicInfo
            return {
                "success": True,
                "document_info": {
                    "name": file_name,
                    "file_type": self._get_file_extension(file_name),
                    "file_size": 0,
                    "version_number": 1,
                    "create_time": None,
                    "last_modified_time": None,
                    "storage_urn": storage_urn,
                    "bucket": bucket_key,
                    "object_key": object_key,
                    "mime_type": self._get_mime_type_from_extension(file_name)
                },
                "urn": storage_urn,
                "note": "Basic info only - detailed info unavailable"
            }
                
        except Exception as e:
            print(f"ERROR: OSS Object info failed: {e}")
            return {
                "success": False,
                "error": f"OSS Object info failed: {str(e)}",
                "status": "info_failed",
                "urn": storage_urn
            }
    
    def _get_file_extension(self, filename):
        """从文件名中提取文件扩展名"""
        if '.' in filename:
            return filename.split('.')[-1].lower()
        return 'unknown'
    
    def _get_mime_type_from_extension(self, filename):
        """根据文件扩展名获取MIME类型"""
        ext = self._get_file_extension(filename)
        mime_types = {
            'pdf': 'application/pdf',
            'dwg': 'application/acad',
            'dxf': 'application/dxf',
            'rvt': 'application/vnd.autodesk.revit',
            'ifc': 'application/x-step',
            'nwd': 'application/vnd.autodesk.navisworks',
            'nwc': 'application/vnd.autodesk.navisworks',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'bmp': 'image/bmp',
            'tiff': 'image/tiff',
            'doc': 'application/msword',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'xls': 'application/vnd.ms-excel',
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'ppt': 'application/vnd.ms-powerpoint',
            'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'txt': 'text/plain',
            'csv': 'text/csv',
            'xml': 'application/xml',
            'zip': 'application/zip',
            'rar': 'application/x-rar-compressed'
        }
        return mime_types.get(ext, 'application/octet-stream')
    
    def download_by_urn(self, urn, access_token=None, document_name=None):
        """
        Generic method to download files by URN
        
        Args:
            urn (str): File URN identifier
            access_token (str): Access token
            document_name (str): Document name (optional)
            
        Returns:
            dict: Download result with download link or error info
        """
        if not access_token:
            access_token = utils.get_access_token()
            
        if not access_token:
            return {
                "success": False,
                "error": "Access token not found",
                "status": "unauthorized"
            }
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        print(f"[URN Download] Processing URN: {urn}")
        
        # Choose download method based on URN type
        if 'dm.lineage:' in urn:
            return self._download_document_lineage(urn, headers, document_name)
        elif 'os.object:' in urn:
            return self._download_oss_object(urn, headers, document_name)
        else:
            return {
                "success": False,
                "error": f"Unsupported URN type: {urn}",
                "status": "unsupported_urn_type"
            }
    
    def _download_document_lineage(self, lineage_urn, headers, document_name=None):
        """Download Document Lineage type URN"""
        return {
            "success": False,
            "error": "Document Lineage download requires project ID",
            "status": "missing_project_id",
            "urn": lineage_urn
        }
    
    def _download_oss_object(self, storage_urn, headers, document_name=None):
        """Download OSS Object type URN"""
        try:
            print(f"[OSS Object] Processing storage URN: {storage_urn}")
            
            # Parse storage URN: urn:adsk.objects:os.object:bucket/object_key
            if 'os.object:' not in storage_urn:
                return {
                    "success": False,
                    "error": "Invalid OSS Object URN format",
                    "status": "invalid_urn"
                }
            
            object_part = storage_urn.split('os.object:')[1]
            
            # Separate bucket and object key
            if '/' in object_part:
                bucket_key = object_part.split('/')[0]
                object_key = '/'.join(object_part.split('/')[1:])
            else:
                bucket_key = 'wip.dm.prod'  # Default bucket
                object_key = object_part
            
            print(f"Parsed OSS URN: bucket={bucket_key}, object={object_key}")
            
            # Get OSS signed download link
            encoded_object_key = quote(object_key, safe='')
            oss_signed_url = f"{self.base_url}/oss/v2/buckets/{bucket_key}/objects/{encoded_object_key}/signeds3download"
            
            print(f"Getting OSS signed download link: {oss_signed_url}")
            
            oss_resp = requests.get(oss_signed_url, headers=headers, timeout=30)
            
            if oss_resp.status_code == 200:
                try:
                    # Parse JSON response
                    oss_data = oss_resp.json()
                    signed_download_url = oss_data.get('url', '')
                    
                    print(f"Extracted download URL: {signed_download_url[:100]}...")
                    
                    if signed_download_url and signed_download_url.startswith('http'):
                        print(f"SUCCESS: Got OSS signed download link")
                        return {
                            "success": True,
                            "download_url": signed_download_url,
                            "document_name": document_name or object_key,
                            "requires_auth": False,
                            "method": "oss_signed_download",
                            "urn": storage_urn
                        }
                    else:
                        print(f"Invalid URL in OSS response: '{signed_download_url}'")
                        return {
                            "success": False,
                            "error": "Invalid download URL from OSS API",
                            "status": "invalid_download_url"
                        }
                except json.JSONDecodeError as e:
                    print(f"Failed to parse OSS API response as JSON: {e}")
                    # Fallback to text parsing
                    signed_download_url = oss_resp.text.strip().strip('"')
                    
                    if signed_download_url and signed_download_url.startswith('http'):
                        print(f"SUCCESS: Got OSS signed download link (text mode)")
                        return {
                            "success": True,
                            "download_url": signed_download_url,
                            "document_name": document_name or object_key,
                            "requires_auth": False,
                            "method": "oss_signed_download",
                            "urn": storage_urn
                        }
                    else:
                        return {
                            "success": False,
                            "error": "Invalid download URL from OSS API",
                            "status": "invalid_download_url"
                        }
            else:
                print(f"OSS signed API failed: {oss_resp.status_code} - {oss_resp.text}")
                return {
                    "success": False,
                    "error": f"OSS signed API failed: {oss_resp.status_code}",
                    "status": "oss_api_failed",
                    "response": oss_resp.text
                }
                
        except Exception as e:
            print(f"ERROR: OSS Object download failed: {e}")
            return {
                "success": False,
                "error": f"OSS Object download failed: {str(e)}",
                "status": "download_failed"
            }
    
    def download_document_lineage_with_project(self, lineage_urn, project_id, headers, document_name=None):
        """
        Download Document Lineage (requires project ID)
        """
        try:
            print(f"[Document Lineage] Processing lineage URN: {lineage_urn}, project: {project_id}")
            
            # Clean project ID
            clean_project_id = project_id[2:] if project_id.startswith('b.') else project_id
            
            # Get versions for the lineage item
            versions_url = f"{self.base_url}/data/v1/projects/b.{clean_project_id}/items/{quote(lineage_urn, safe='')}/versions"
            
            print(f"Getting versions for lineage: {versions_url}")
            versions_resp = requests.get(versions_url, headers=headers, timeout=30)
                
            if versions_resp.status_code == 200:
                versions_data = versions_resp.json()
                versions = versions_data.get('data', [])
                    
                if versions:
                    latest_version = versions[0]  # First is usually latest
                    version_id = latest_version.get('id')
                        
                    if version_id:
                        print(f"Found latest version: {version_id}")
                            
                        # Get downloads for this version
                        downloads_url = f"{self.base_url}/data/v1/projects/b.{clean_project_id}/versions/{quote(version_id, safe='')}/downloads"
                            
                        print(f"Getting downloads for version: {downloads_url}")
                        downloads_resp = requests.get(downloads_url, headers=headers, timeout=30)
                            
                        # Try to get storage URN from version first (more reliable)
                        storage_relationship = latest_version.get('relationships', {}).get('storage', {})
                        if storage_relationship:
                            storage_data = storage_relationship.get('data', {})
                            actual_storage_urn = storage_data.get('id')
                            
                            if actual_storage_urn and 'os.object:' in actual_storage_urn:
                                print(f"Found storage URN from version: {actual_storage_urn}")
                                
                                # Recursively call OSS download method
                                return self._download_oss_object(actual_storage_urn, headers, document_name)
                        
                        # If storage URN not available, try downloads API
                        if downloads_resp.status_code == 200:
                            downloads_data = downloads_resp.json()
                            downloads = downloads_data.get('data', [])
                            
                            if downloads:
                                # Use the first available download
                                download_item = downloads[0]
                                
                                # Get the download URL from the source relationship
                                source_relationship = download_item.get('relationships', {}).get('source', {})
                                if source_relationship:
                                    source_links = source_relationship.get('links', {})
                                    download_url = source_links.get('related')
                                    
                                    if download_url:
                                        print(f"Found download URL: {download_url}")
                                        return {
                                            "success": True,
                                            "download_url": download_url,
                                            "document_name": document_name,
                                            "requires_auth": True,
                                            "method": "data_management_downloads",
                                            "urn": lineage_urn
                                        }
                        else:
                            print(f"Downloads API failed: {downloads_resp.status_code} - trying storage URN fallback")
                        
                        return {
                            "success": False,
                            "error": "No downloads or storage URN available for this version",
                            "status": "no_downloads_available"
                        }
                    else:
                        return {
                            "success": False,
                            "error": "No version ID found",
                            "status": "no_version_id"
                        }
                else:
                    return {
                        "success": False,
                        "error": "No versions found for this lineage",
                        "status": "no_versions"
                    }
            else:
                print(f"Failed to get versions: {versions_resp.status_code} - {versions_resp.text}")
                return {
                    "success": False,
                    "error": f"Failed to get versions: {versions_resp.status_code}",
                    "status": "versions_api_failed"
                }
                
        except Exception as e:
            print(f"ERROR: Document Lineage download failed: {e}")
            return {
                "success": False,
                "error": f"Document Lineage download failed: {str(e)}",
                "status": "download_failed"
            }


# Global instance
urn_download_manager = URNDownloadManager()


def download_by_urn(urn, access_token=None, document_name=None):
    """
    Generic URN download function (convenience method)
    """
    return urn_download_manager.download_by_urn(urn, access_token, document_name)


def download_document_lineage(lineage_urn, project_id, access_token=None, document_name=None):
    """
    Download Document Lineage convenience method
    """
    if not access_token:
        access_token = utils.get_access_token()
        
    if not access_token:
        return {
            "success": False,
            "error": "Access token not found",
            "status": "unauthorized"
        }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    return urn_download_manager.download_document_lineage_with_project(
        lineage_urn, project_id, headers, document_name
    )


def download_oss_object(storage_urn, access_token=None, document_name=None):
    """
    Download OSS Object convenience method
    """
    if not access_token:
        access_token = utils.get_access_token()
        
    if not access_token:
        return {
            "success": False,
            "error": "Access token not found",
            "status": "unauthorized"
        }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    return urn_download_manager._download_oss_object(storage_urn, headers, document_name)


def get_document_info_by_urn(urn, project_id=None, access_token=None):
    """
    获取URN对应的文档详细信息的便利函数
    
    Args:
        urn (str): 文档URN标识符
        project_id (str): 项目ID (对于dm.lineage类型URN必需)
        access_token (str): 访问令牌
        
    Returns:
        dict: 包含文档信息的结果
    """
    return urn_download_manager.get_document_info_by_urn(urn, project_id, access_token)
