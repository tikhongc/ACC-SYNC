# -*- coding: utf-8 -*-
"""
Autospecs + Packages API 模組
處理 ACC Autospecs 和 Packages 相關的 API 功能
Autospecs API 用於讀取從施工規範書自動提取的送審記錄，Packages API 用於管理文件包
"""

import requests
import json
from flask import Blueprint, jsonify, request
from datetime import datetime
import config
import utils
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import unquote

autospecs_packages_bp = Blueprint('autospecs_packages', __name__)

# Autospecs + Packages API 相關功能實現


def _normalize_autospecs_identifier(item_id):
    """標準化 Autospecs 標識符，處理 URL 編碼等"""
    if not item_id:
        return ""
    
    # URL 解碼
    decoded_id = unquote(item_id)
    
    return decoded_id


def _analyze_autospecs_status(status):
    """分析 Autospecs 狀態並返回狀態類型用於 UI 顯示"""
    status_map = {
        'pending': 'warning',
        'approved': 'success',
        'rejected': 'danger',
        'under_review': 'info',
        'completed': 'success',
        'cancelled': 'secondary'
    }
    return status_map.get(status.lower() if status else '', 'info')


def _analyze_autospecs_category(category):
    """分析 Autospecs 類型並返回類型用於 UI 顯示"""
    category_map = {
        'shop drawings': 'primary',
        'test reports': 'info',
        'product data': 'success',
        'samples': 'warning',
        'certificates': 'info',
        'warranties': 'secondary'
    }
    return category_map.get(category.lower() if category else '', 'info')


def _format_autospecs_submittal_data(submittal_data):
    """格式化 Autospecs 送審記錄數據"""
    if not submittal_data:
        return None
    
    # basicInfo
    submittal_id = submittal_data.get('submittalId', '')
    submittal_description = submittal_data.get('submittalDescription', '')
    spec_number = submittal_data.get('specNumber', '')
    spec_name = submittal_data.get('specName', '')
    
    # 分類信息
    division_code = submittal_data.get('divisionCode', '')
    division_name = submittal_data.get('divisionName', '')
    spec_category = submittal_data.get('specCategory', '')
    submittals_heading = submittal_data.get('submittalsHeading', '')
    
    # 日期和狀態
    target_date = submittal_data.get('targetDate', '')
    
    # 其他屬性
    user_notes = submittal_data.get('userNotes', '')
    para_code = submittal_data.get('paraCode', '')
    target_group = submittal_data.get('targetGroup', '')
    version_name = submittal_data.get('versionName', '')
    
    formatted_submittal = {
        # basicInfo
        'id': submittal_id,
        'description': submittal_description,
        'spec_number': spec_number,
        'spec_name': spec_name,
        
        # 分類信息
        'division_code': division_code,
        'division_name': division_name,
        'spec_category': spec_category,
        'spec_category_type': _analyze_autospecs_category(spec_category),
        'submittals_heading': submittals_heading,
        
        # 日期信息
        'target_date': utils.format_timestamp(target_date) if target_date else '',
        
        # 其他屬性
        'user_notes': user_notes,
        'para_code': para_code,
        'target_group': target_group,
        'version_name': version_name,
        
        # 計算字段
        'has_target_date': bool(target_date),
        'has_notes': bool(user_notes),
        'display_name': f"{submittal_id}: {submittal_description}" if submittal_id and submittal_description else submittal_description or f"Submittal {submittal_id}",
        'division_display': f"{division_code} - {division_name}" if division_code and division_name else division_name or division_code,
        
        # 原始數據（用於調試）
        'raw_data': submittal_data
    }
    
    # 計算是否逾期（使用北京时间）
    if target_date:
        try:
            from datetime import datetime, timezone, timedelta
            target_datetime = datetime.fromisoformat(target_date.replace('Z', '+00:00'))
            # 转换为北京时间进行比较
            beijing_tz = timezone(timedelta(hours=8))
            target_beijing = target_datetime.astimezone(beijing_tz)
            now_beijing = datetime.now(beijing_tz)
            formatted_submittal['is_overdue'] = target_beijing < now_beijing
        except:
            formatted_submittal['is_overdue'] = False
    else:
        formatted_submittal['is_overdue'] = False
    
    return formatted_submittal


def _format_package_data(package_data):
    """格式化 Package 數據"""
    if not package_data:
        return None
    
    # basicInfo
    package_id = package_data.get('id', '')
    display_id = package_data.get('displayId', '')
    name = package_data.get('name', '')
    description = package_data.get('description', '')
    
    # 狀態信息
    locked = package_data.get('locked', False)
    version_type = package_data.get('versionType', '')
    resource_count = package_data.get('resourceCount', 0)
    
    # 日期和人員
    created_at = package_data.get('createdAt', '')
    created_by = package_data.get('createdBy', '')
    updated_at = package_data.get('updatedAt', '')
    updated_by = package_data.get('updatedBy', '')
    
    formatted_package = {
        # basicInfo
        'id': package_id,
        'display_id': display_id,
        'name': name,
        'description': description,
        
        # 狀態信息
        'locked': locked,
        'version_type': version_type,
        'resource_count': resource_count,
        'status': 'locked' if locked else 'active',
        'status_type': 'secondary' if locked else 'success',
        
        # 日期和人員
        'created_at': utils.format_timestamp(created_at) if created_at else '',
        'created_by': created_by,
        'updated_at': utils.format_timestamp(updated_at) if updated_at else '',
        'updated_by': updated_by,
        
        # 計算字段
        'has_resources': resource_count > 0,
        'is_empty': resource_count == 0,
        'display_name': f"{display_id}: {name}" if display_id and name else name or f"Package {package_id}",
        
        # 原始數據（用於調試）
        'raw_data': package_data
    }
    
    return formatted_package


def _format_package_resource_data(resource_data):
    """格式化 Package 資源數據"""
    if not resource_data:
        return None
    
    # basicInfo
    resource_id = resource_data.get('id', '')
    urn = resource_data.get('urn', '')
    name = resource_data.get('name', '')
    version = resource_data.get('version', 0)
    file_type = resource_data.get('fileType', '')
    
    # 狀態信息
    is_deleted = resource_data.get('isDeleted', False)
    parent_folder_urn = resource_data.get('parentFolderUrn', '')
    
    # 自訂屬性和審核狀態
    custom_attributes = resource_data.get('customAttributes', [])
    approval_status = resource_data.get('approvalStatus', {})
    
    formatted_resource = {
        # basicInfo
        'id': resource_id,
        'urn': urn,
        'name': name,
        'version': version,
        'file_type': file_type.upper() if file_type else 'UNKNOWN',
        
        # 狀態信息
        'is_deleted': is_deleted,
        'parent_folder_urn': parent_folder_urn,
        'status': 'deleted' if is_deleted else 'active',
        'status_type': 'danger' if is_deleted else 'success',
        
        # 自訂屬性和審核
        'custom_attributes': custom_attributes,
        'custom_attributes_count': len(custom_attributes) if custom_attributes else 0,
        'approval_status': approval_status,
        'has_approval_status': bool(approval_status),
        
        # 計算字段
        'has_custom_attributes': len(custom_attributes) > 0 if custom_attributes else False,
        'display_name': f"{name} (v{version})" if name and version else name or f"Resource {resource_id}",
        
        # 原始數據（用於調試）
        'raw_data': resource_data
    }
    
    return formatted_resource


# ==================== Autospecs API 端點 ====================

@autospecs_packages_bp.route('/api/autospecs-packages/<project_id>/autospecs/metadata')
def get_autospecs_metadata(project_id):
    """獲取專案的 Autospecs 版本資訊"""
    access_token = utils.get_access_token()
    if not access_token:
        return jsonify({
            "error": "未找到 Access Token，請先進行認證",
            "status": "unauthorized"
        }), 401
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        # 調用 Autodesk Construction Cloud Autospecs API
        metadata_url = f"{config.AUTODESK_API_BASE}/construction/autospecs/v1/projects/{project_id}/metadata"
        
        print(f"Autospecs 元數據 API 請求 URL: {metadata_url}")
        
        metadata_resp = requests.get(metadata_url, headers=headers, timeout=30)
        
        print(f"Autospecs 元數據 API 響應狀態碼: {metadata_resp.status_code}")
        
        if metadata_resp.status_code != 200:
            error_text = metadata_resp.text
            print(f"Autospecs 元數據 API 錯誤響應: {error_text}")
            raise Exception(f"獲取 Autospecs 元數據失敗: {metadata_resp.status_code} - {error_text}")
        
        try:
            metadata_data = metadata_resp.json()
            print(f"Autospecs 元數據 API 響應數據: {metadata_data}")
        except json.JSONDecodeError as e:
            print(f"JSON 解析錯誤: {e}")
            raise Exception(f"API 響應數據格式錯誤: {str(e)}")
        
        if not metadata_data:
            print("API 返回空 Autospecs 元數據")
            metadata_data = {"versions": [], "region": ""}
        
        # 提取版本信息
        versions = metadata_data.get("versions", [])
        region = metadata_data.get("region", "")
        
        # 格式化版本數據
        formatted_versions = []
        for version in versions:
            formatted_version = {
                'id': version.get('id', ''),
                'name': version.get('name', ''),
                'status': version.get('status', ''),
                'current_version': version.get('currentVersion', False),
                'created_at': utils.format_timestamp(version.get('createdAt', '')),
                'updated_at': utils.format_timestamp(version.get('updatedAt', '')),
                'status_type': _analyze_autospecs_status(version.get('status', '')),
                'is_current': version.get('currentVersion', False)
            }
            formatted_versions.append(formatted_version)
        
        # 統計信息
        total_versions = len(formatted_versions)
        current_versions = len([v for v in formatted_versions if v['is_current']])
        completed_versions = len([v for v in formatted_versions if v['status'].lower() == 'completed'])
        
        stats = {
            'total_versions': total_versions,
            'current_versions': current_versions,
            'completed_versions': completed_versions,
            'region': region
        }
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "region": region,
            "stats": stats,
            "versions": formatted_versions,
            "raw_data": metadata_data,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"獲取 Autospecs 元數據時出錯: {str(e)}")
        return jsonify({
            "error": f"獲取 Autospecs 元數據失敗: {str(e)}",
            "status": "error"
        }), 500


@autospecs_packages_bp.route('/api/autospecs-packages/<project_id>/autospecs/<version_id>/smartregister')
def get_autospecs_smartregister(project_id, version_id):
    """獲取指定版本的送審記錄 (Smart Register)"""
    access_token = utils.get_access_token()
    if not access_token:
        return jsonify({
            "error": "未找到 Access Token，請先進行認證",
            "status": "unauthorized"
        }), 401
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        # 調用 Autodesk Construction Cloud Autospecs API
        smartregister_url = f"{config.AUTODESK_API_BASE}/construction/autospecs/v1/projects/{project_id}/version/{version_id}/smartregister"
        
        print(f"Autospecs Smart Register API 請求 URL: {smartregister_url}")
        
        smartregister_resp = requests.get(smartregister_url, headers=headers, timeout=30)
        
        print(f"Autospecs Smart Register API 響應狀態碼: {smartregister_resp.status_code}")
        
        if smartregister_resp.status_code != 200:
            error_text = smartregister_resp.text
            print(f"Autospecs Smart Register API 錯誤響應: {error_text}")
            raise Exception(f"獲取 Smart Register 失敗: {smartregister_resp.status_code} - {error_text}")
        
        try:
            smartregister_data = smartregister_resp.json()
            print(f"Autospecs Smart Register API 響應數據: {smartregister_data}")
        except json.JSONDecodeError as e:
            print(f"JSON 解析錯誤: {e}")
            raise Exception(f"API 響應數據格式錯誤: {str(e)}")
        
        if not smartregister_data:
            print("API 返回空 Smart Register 數據")
            smartregister_data = []
        
        # 如果返回的是字典，提取數據數組
        if isinstance(smartregister_data, dict):
            submittals_list = smartregister_data.get('data', smartregister_data.get('submittals', []))
        else:
            submittals_list = smartregister_data if isinstance(smartregister_data, list) else []
        
        # 格式化送審記錄數據
        formatted_submittals = []
        for submittal in submittals_list:
            formatted_submittal = _format_autospecs_submittal_data(submittal)
            if formatted_submittal:
                formatted_submittals.append(formatted_submittal)
        
        # 生成統計信息
        total_submittals = len(formatted_submittals)
        
        # 分類統計
        division_counts = {}
        category_counts = {}
        overdue_count = 0
        with_notes_count = 0
        
        for submittal in formatted_submittals:
            # 統計分項
            division = submittal['division_name']
            if division:
                division_counts[division] = division_counts.get(division, 0) + 1
            
            # 統計類別
            category = submittal['spec_category']
            if category:
                category_counts[category] = category_counts.get(category, 0) + 1
            
            # 統計逾期和備註
            if submittal['is_overdue']:
                overdue_count += 1
            if submittal['has_notes']:
                with_notes_count += 1
        
        stats = {
            "total_submittals": total_submittals,
            "division_counts": division_counts,
            "category_counts": category_counts,
            "overdue_count": overdue_count,
            "with_notes_count": with_notes_count,
            "overdue_rate": round((overdue_count / total_submittals) * 100, 1) if total_submittals > 0 else 0,
            "notes_rate": round((with_notes_count / total_submittals) * 100, 1) if total_submittals > 0 else 0
        }
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "version_id": version_id,
            "stats": stats,
            "submittals": formatted_submittals,
            "raw_data": submittals_list,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"獲取 Smart Register 時出錯: {str(e)}")
        return jsonify({
            "error": f"獲取 Smart Register 失敗: {str(e)}",
            "status": "error"
        }), 500


# ==================== Packages API 端點 ====================

@autospecs_packages_bp.route('/api/autospecs-packages/<project_id>/packages')
def get_project_packages(project_id):
    """獲取專案中所有的 packages"""
    access_token = utils.get_access_token()
    if not access_token:
        return jsonify({
            "error": "未找到 Access Token，請先進行認證",
            "status": "unauthorized"
        }), 401
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # 獲取查詢參數
    limit = request.args.get('limit', 50, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    try:
        # 調用 Autodesk Construction Cloud Packages API
        packages_url = f"{config.AUTODESK_API_BASE}/construction/packages/v1/projects/{project_id}/packages"
        
        # 添加查詢參數
        params = {}
        if limit:
            params['limit'] = min(limit, 200)  # 最大 200
        if offset:
            params['offset'] = offset
        
        print(f"Packages API 請求 URL: {packages_url}")
        print(f"Packages API 請求參數: {params}")
        
        packages_resp = requests.get(packages_url, headers=headers, params=params, timeout=30)
        
        print(f"Packages API 響應狀態碼: {packages_resp.status_code}")
        
        if packages_resp.status_code != 200:
            error_text = packages_resp.text
            print(f"Packages API 錯誤響應: {error_text}")
            raise Exception(f"獲取 Packages 失敗: {packages_resp.status_code} - {error_text}")
        
        try:
            packages_data = packages_resp.json()
            print(f"Packages API 響應數據: {packages_data}")
        except json.JSONDecodeError as e:
            print(f"JSON 解析錯誤: {e}")
            raise Exception(f"API 響應數據格式錯誤: {str(e)}")
        
        if not packages_data:
            print("API 返回空 Packages 數據")
            packages_data = {"data": [], "pagination": {}}
        
        # 提取包列表和分頁信息
        packages_list = packages_data.get("data", packages_data.get("packages", []))
        pagination = packages_data.get("pagination", {})
        
        # 格式化 Packages 數據
        formatted_packages = []
        for package in packages_list:
            formatted_package = _format_package_data(package)
            if formatted_package:
                formatted_packages.append(formatted_package)
        
        # 生成統計信息
        total_packages = pagination.get('totalResults', len(formatted_packages))
        
        # 狀態統計
        locked_packages = len([p for p in formatted_packages if p['locked']])
        active_packages = len([p for p in formatted_packages if not p['locked']])
        empty_packages = len([p for p in formatted_packages if p['is_empty']])
        with_resources = len([p for p in formatted_packages if p['has_resources']])
        
        # 版本類型統計
        version_type_counts = {}
        total_resources = 0
        
        for package in formatted_packages:
            version_type = package['version_type']
            if version_type:
                version_type_counts[version_type] = version_type_counts.get(version_type, 0) + 1
            total_resources += package['resource_count']
        
        stats = {
            "total_packages": total_packages,
            "current_page_count": len(formatted_packages),
            "locked_packages": locked_packages,
            "active_packages": active_packages,
            "empty_packages": empty_packages,
            "with_resources": with_resources,
            "version_type_counts": version_type_counts,
            "total_resources": total_resources,
            "avg_resources_per_package": round(total_resources / len(formatted_packages), 1) if formatted_packages else 0
        }
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "stats": stats,
            "packages": formatted_packages,
            "pagination": pagination,
            "raw_data": packages_list,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"獲取 Packages 時出錯: {str(e)}")
        return jsonify({
            "error": f"獲取 Packages 失敗: {str(e)}",
            "status": "error"
        }), 500


@autospecs_packages_bp.route('/api/autospecs-packages/<project_id>/packages/<package_id>/resources')
def get_package_resources(project_id, package_id):
    """獲取特定 package 中包含的所有文件資源"""
    access_token = utils.get_access_token()
    if not access_token:
        return jsonify({
            "error": "未找到 Access Token，請先進行認證",
            "status": "unauthorized"
        }), 401
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        # 調用 Autodesk Construction Cloud Packages API
        resources_url = f"{config.AUTODESK_API_BASE}/construction/packages/v1/projects/{project_id}/packages/{package_id}/resources"
        
        print(f"Package Resources API 請求 URL: {resources_url}")
        
        resources_resp = requests.get(resources_url, headers=headers, timeout=30)
        
        print(f"Package Resources API 響應狀態碼: {resources_resp.status_code}")
        
        if resources_resp.status_code != 200:
            error_text = resources_resp.text
            print(f"Package Resources API 錯誤響應: {error_text}")
            raise Exception(f"獲取 Package Resources 失敗: {resources_resp.status_code} - {error_text}")
        
        try:
            resources_data = resources_resp.json()
            print(f"Package Resources API 響應數據: {resources_data}")
        except json.JSONDecodeError as e:
            print(f"JSON 解析錯誤: {e}")
            raise Exception(f"API 響應數據格式錯誤: {str(e)}")
        
        if not resources_data:
            print("API 返回空 Package Resources 數據")
            resources_data = {"data": []}
        
        # 提取資源列表
        resources_list = resources_data.get("data", resources_data.get("resources", []))
        
        # 格式化 Resources 數據
        formatted_resources = []
        for resource in resources_list:
            formatted_resource = _format_package_resource_data(resource)
            if formatted_resource:
                formatted_resources.append(formatted_resource)
        
        # 生成統計信息
        total_resources = len(formatted_resources)
        
        # 狀態統計
        active_resources = len([r for r in formatted_resources if not r['is_deleted']])
        deleted_resources = len([r for r in formatted_resources if r['is_deleted']])
        with_custom_attributes = len([r for r in formatted_resources if r['has_custom_attributes']])
        with_approval_status = len([r for r in formatted_resources if r['has_approval_status']])
        
        # 文件類型統計
        file_type_counts = {}
        version_counts = {}
        
        for resource in formatted_resources:
            # 統計文件類型
            file_type = resource['file_type']
            if file_type:
                file_type_counts[file_type] = file_type_counts.get(file_type, 0) + 1
            
            # 統計版本
            version = resource['version']
            if version:
                version_counts[version] = version_counts.get(version, 0) + 1
        
        stats = {
            "total_resources": total_resources,
            "active_resources": active_resources,
            "deleted_resources": deleted_resources,
            "with_custom_attributes": with_custom_attributes,
            "with_approval_status": with_approval_status,
            "file_type_counts": file_type_counts,
            "version_counts": version_counts,
            "deletion_rate": round((deleted_resources / total_resources) * 100, 1) if total_resources > 0 else 0,
            "approval_rate": round((with_approval_status / total_resources) * 100, 1) if total_resources > 0 else 0
        }
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "package_id": package_id,
            "stats": stats,
            "resources": formatted_resources,
            "raw_data": resources_list,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"獲取 Package Resources 時出錯: {str(e)}")
        return jsonify({
            "error": f"獲取 Package Resources 失敗: {str(e)}",
            "status": "error"
        }), 500


# ==================== 簡化路由（Jarvis 風格）====================

@autospecs_packages_bp.route('/api/autospecs-packages/jarvis/autospecs/metadata')
def get_jarvis_autospecs_metadata():
    """獲取指定項目的 Autospecs 元數據（簡化路由）"""
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 參數",
            "message": "請在請求中提供 projectId 參數，例如: ?projectId=your-project-id",
            "status": "error"
        }), 400
    
    print(f"🚀 Autospecs + Packages API: 使用項目 ID: {project_id}")
    
    return get_autospecs_metadata(project_id)


@autospecs_packages_bp.route('/api/autospecs-packages/jarvis/autospecs/<version_id>/smartregister')
def get_jarvis_autospecs_smartregister(version_id):
    """獲取指定項目和版本的 Smart Register（簡化路由）"""
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 參數",
            "message": "請在請求中提供 projectId 參數",
            "status": "error"
        }), 400
    
    return get_autospecs_smartregister(project_id, version_id)


@autospecs_packages_bp.route('/api/autospecs-packages/jarvis/packages')
def get_jarvis_packages():
    """獲取指定項目的 Packages（簡化路由）"""
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 參數",
            "message": "請在請求中提供 projectId 參數，例如: ?projectId=your-project-id",
            "status": "error"
        }), 400
    
    print(f"🚀 Autospecs + Packages API: 使用項目 ID: {project_id}")
    
    return get_project_packages(project_id)


@autospecs_packages_bp.route('/api/autospecs-packages/jarvis/packages/<package_id>/resources')
def get_jarvis_package_resources(package_id):
    """獲取指定項目和包的資源（簡化路由）"""
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 參數",
            "message": "請在請求中提供 projectId 參數",
            "status": "error"
        }), 400
    
    return get_package_resources(project_id, package_id)


# ==================== 綜合統計和分析接口 ====================

@autospecs_packages_bp.route('/api/autospecs-packages/<project_id>/statistics')
def get_autospecs_packages_statistics(project_id):
    """獲取項目 Autospecs + Packages 的綜合統計分析"""
    try:
        # 獲取 Autospecs 元數據
        metadata_response = get_autospecs_metadata(project_id)
        
        if hasattr(metadata_response, 'get_json'):
            metadata_data = metadata_response.get_json()
        else:
            metadata_data = metadata_response
        
        # 獲取 Packages 數據
        packages_response = get_project_packages(project_id)
        
        if hasattr(packages_response, 'get_json'):
            packages_data = packages_response.get_json()
        else:
            packages_data = packages_response
        
        # 綜合統計
        statistics = {
            'overview': {
                'has_autospecs': metadata_data.get('success', False),
                'has_packages': packages_data.get('success', False),
                'total_versions': 0,
                'total_packages': 0,
                'total_submittals': 0,
                'total_resources': 0
            },
            'autospecs_stats': {},
            'packages_stats': {},
            'integration_analysis': {
                'data_sources': [],
                'coverage': 'unknown',
                'recommendations': []
            }
        }
        
        # 處理 Autospecs 統計
        if metadata_data.get('success'):
            autospecs_stats = metadata_data.get('stats', {})
            statistics['overview']['total_versions'] = autospecs_stats.get('total_versions', 0)
            statistics['autospecs_stats'] = autospecs_stats
            statistics['integration_analysis']['data_sources'].append('autospecs')
        
        # 處理 Packages 統計
        if packages_data.get('success'):
            packages_stats = packages_data.get('stats', {})
            statistics['overview']['total_packages'] = packages_stats.get('total_packages', 0)
            statistics['overview']['total_resources'] = packages_stats.get('total_resources', 0)
            statistics['packages_stats'] = packages_stats
            statistics['integration_analysis']['data_sources'].append('packages')
        
        # 分析數據覆蓋率和建議
        data_sources = statistics['integration_analysis']['data_sources']
        if 'autospecs' in data_sources and 'packages' in data_sources:
            statistics['integration_analysis']['coverage'] = 'complete'
            statistics['integration_analysis']['recommendations'] = [
                '數據源完整，可以進行完整的 Autospecs + Packages 管理',
                '建議定期同步 Autospecs 和 Packages 數據',
                '可以建立送審記錄與文件包的關聯分析'
            ]
        elif 'autospecs' in data_sources:
            statistics['integration_analysis']['coverage'] = 'partial_autospecs'
            statistics['integration_analysis']['recommendations'] = [
                '僅有 Autospecs 數據，建議啟用 Packages 功能',
                '可以查看送審記錄，但無法管理文件包',
                '建議上傳施工規範書以獲得更完整的送審記錄'
            ]
        elif 'packages' in data_sources:
            statistics['integration_analysis']['coverage'] = 'partial_packages'
            statistics['integration_analysis']['recommendations'] = [
                '僅有 Packages 數據，建議啟用 Autospecs 功能',
                '可以管理文件包，但缺少自動提取的送審記錄',
                '建議手動創建送審記錄或使用 Autospecs 功能'
            ]
        else:
            statistics['integration_analysis']['coverage'] = 'none'
            statistics['integration_analysis']['recommendations'] = [
                '暫無 Autospecs + Packages 相關數據',
                '建議啟用 Autospecs 功能並上傳施工規範書',
                '建議使用 Packages 功能管理送審文件'
            ]
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "statistics": statistics,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"獲取 Autospecs + Packages 統計時出錯: {str(e)}")
        return jsonify({
            "error": f"獲取 Autospecs + Packages 統計失敗: {str(e)}",
            "status": "error"
        }), 500


@autospecs_packages_bp.route('/api/autospecs-packages/jarvis/statistics')
def get_jarvis_autospecs_packages_statistics():
    """獲取指定項目的 Autospecs + Packages 統計（簡化路由）"""
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 參數",
            "message": "請在請求中提供 projectId 參數",
            "status": "error"
        }), 400
    
    return get_autospecs_packages_statistics(project_id)
