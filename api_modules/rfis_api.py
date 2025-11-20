# -*- coding: utf-8 -*-
"""
RFIs API 相關模組
處理 ACC RFIs API 的所有功能，包括 RFI 數據獲取、搜索和詳情查看
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
from .urn_download_simple import download_by_urn, download_oss_object
from urllib.parse import unquote

# 导入Relations API
try:
    from api_modules.data_management_relations_api import RelationsManager
    RELATIONS_API_AVAILABLE = True
except ImportError as e:
    print(f"警告: 无法导入Relations API: {e}")
    RELATIONS_API_AVAILABLE = False

rfis_bp = Blueprint('rfis', __name__)

# RFIs API 相關功能實現


def _strip_project_id_prefix(project_id):
    """
    移除項目 ID 的 'b.' 前綴（RFIs API v3 要求）
    例如: 'b.1eea4119-3553-4167-b93d-3a3d5d07d33d' -> '1eea4119-3553-4167-b93d-3a3d5d07d33d'
    """
    if project_id and project_id.startswith('b.'):
        return project_id[2:]
    return project_id


def _normalize_rfi_identifier(rfi_id):
    """標準化 RFI 標識符，處理 URL 編碼等"""
    if not rfi_id:
        return ""
    
    # URL 解碼
    decoded_id = unquote(rfi_id)
    
    return decoded_id


def _analyze_rfi_status(status):
    """分析 RFI 狀態並返回狀態類型用於 UI 顯示"""
    status_map = {
        'open': 'warning',
        'answered': 'success',
        'closed': 'info',
        'draft': 'info',
        'void': 'danger'
    }
    return status_map.get(status.lower() if status else '', 'info')


def _analyze_rfi_priority(priority):
    """分析 RFI 優先級並返回優先級類型用於 UI 顯示"""
    priority_map = {
        'high': 'danger',
        'normal': 'info',
        'low': 'success'
    }
    return priority_map.get(priority.lower() if priority else '', 'info')


def _analyze_impact_assessment(cost_impact, schedule_impact):
    """分析影響評估"""
    impact_analysis = {
        'has_cost_impact': cost_impact and cost_impact.lower() == 'yes',
        'has_schedule_impact': schedule_impact and schedule_impact.lower() == 'yes',
        'cost_impact_status': cost_impact or 'Unknown',
        'schedule_impact_status': schedule_impact or 'Unknown',
        'overall_impact': 'high' if (cost_impact and cost_impact.lower() == 'yes') or (schedule_impact and schedule_impact.lower() == 'yes') else 'low'
    }
    
    return impact_analysis


def _clean_text(text):
    """清理文本，移除多餘的點號、星號和空白"""
    if not text or not isinstance(text, str):
        return text
    
    # 移除開頭的所有 *、. 和空白
    while text and (text[0] in ['*', '.', ' ', '\t']):
        text = text[1:]
    
    # 移除結尾的所有 .、* 和空白
    while text and (text[-1] in ['.', '*', ' ', '\t']):
        text = text[:-1]
    
    # 清理多餘空白
    text = text.strip()
    
    return text


def _get_custom_attribute_definitions(project_id, access_token):
    """獲取項目的custom attribute定義"""
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        attributes_url = f"{config.AUTODESK_API_BASE}/construction/rfis/v3/projects/{project_id}/attributes"
        
        print(f"📋 獲取custom attributes定義: {attributes_url}")
        
        response = requests.get(attributes_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            # 創建ID到名稱的映射
            attr_definitions = {}
            for attr in results:
                attr_id = attr.get('id', '')
                attr_name = attr.get('name', '')
                attr_type = attr.get('type', 'text')
                attr_description = attr.get('description', '')
                
                if attr_id:
                    attr_definitions[attr_id] = {
                        'name': attr_name or f'Attribute {attr_id[:8]}',
                        'type': attr_type,
                        'description': attr_description
                    }
            
            print(f"✅ 獲取到 {len(attr_definitions)} 個custom attribute定義")
            return attr_definitions
        else:
            print(f"⚠️ 獲取custom attributes定義失敗: {response.status_code}")
            return {}
    except Exception as e:
        print(f"❌ 獲取custom attributes定義異常: {e}")
        return {}


def _format_rfi_data(rfi_data, include_references=False, project_id=None):
    """格式化單個 RFI 數據"""
    if not rfi_data:
        return None
    
    # basicInfo
    rfi_id = rfi_data.get('id', '')
    custom_identifier = _clean_text(rfi_data.get('customIdentifier', ''))
    display_id = _clean_text(rfi_data.get('displayId', ''))
    title = _clean_text(rfi_data.get('title', ''))
    question = rfi_data.get('question', '')
    description = rfi_data.get('description', '')
    suggested_answer = rfi_data.get('suggestedAnswer', '')
    
    # 狀態和流程
    status = _clean_text(rfi_data.get('status', ''))
    previous_status = _clean_text(rfi_data.get('previousStatus', ''))
    workflow_type = _clean_text(rfi_data.get('workflowType', ''))
    
    # 人員指派
    assigned_to = rfi_data.get('assignedTo', {})
    assigned_to_type = rfi_data.get('assignedToType', '')
    manager_id = rfi_data.get('managerId', '')
    reviewer_id = rfi_data.get('reviewerId', '')
    reviewers = rfi_data.get('reviewers', [])
    created_by = rfi_data.get('createdBy', {})
    updated_by = rfi_data.get('updatedBy', {})
    closed_by = rfi_data.get('closedBy', {})
    
    # 日期和時程
    due_date = rfi_data.get('dueDate', '')
    start_date = rfi_data.get('startDate', '')
    created_at = rfi_data.get('createdAt', '')
    updated_at = rfi_data.get('updatedAt', '')
    closed_at = rfi_data.get('closedAt', '')
    
    # 影響評估
    cost_impact = _clean_text(rfi_data.get('costImpact', ''))
    schedule_impact = _clean_text(rfi_data.get('scheduleImpact', ''))
    
    # 分類和屬性
    priority = _clean_text(rfi_data.get('priority', ''))
    discipline = _clean_text(rfi_data.get('discipline', ''))
    category = _clean_text(rfi_data.get('category', ''))
    raw_custom_attributes = rfi_data.get('customAttributes', [])
    
    # 🔧 增強：處理真實的custom attributes數據結構
    custom_attributes = []
    reference = rfi_data.get('reference', '')
    
    print(f"📋 處理custom attributes: {len(raw_custom_attributes)} 個原始屬性")
    
    # 獲取custom attribute定義（如果有project_id的話）
    attr_definitions = {}
    if project_id:
        try:
            access_token = utils.get_access_token()
            if access_token:
                attr_definitions = _get_custom_attribute_definitions(project_id, access_token)
        except Exception as e:
            print(f"⚠️ 獲取attribute定義失敗: {e}")
    
    # 處理真實的custom attributes API數據結構
    if raw_custom_attributes and isinstance(raw_custom_attributes, list):
        for attr in raw_custom_attributes:
            if isinstance(attr, dict):
                attr_id = attr.get('id', '')
                attr_values = attr.get('values', [])
                is_selectable = attr.get('isSelectable', False)
                
                # 獲取屬性值 - 可能是數組
                attr_value = ''
                if attr_values and isinstance(attr_values, list):
                    # 過濾掉空值並連接
                    non_empty_values = [str(v).strip() for v in attr_values if v and str(v).strip()]
                    attr_value = ', '.join(non_empty_values) if non_empty_values else ''
                
                if attr_id:  # 只要有ID就添加，即使值為空
                    # 從定義中獲取真實名稱
                    attr_def = attr_definitions.get(attr_id, {})
                    attr_name = attr_def.get('name', f'Custom Attribute {len(custom_attributes) + 1}')
                    attr_type = attr_def.get('type', 'text' if not is_selectable else 'select')
                    attr_description = attr_def.get('description', '')
                    
                    custom_attributes.append({
                        'id': attr_id,
                        'name': attr_name,
                        'value': attr_value or '(empty)',
                        'type': attr_type,
                        'source': 'api_custom_attributes',
                        'isSelectable': is_selectable,
                        'rawValues': attr_values,
                        'description': attr_description
                    })
                    print(f"✅ 添加custom attribute: {attr_name} ({attr_id}) = {attr_value or '(empty)'}")
    
    # 如果沒有真實的custom attributes但有reference，將reference作為custom attribute
    if not custom_attributes and reference:
        custom_attributes = [{
            'name': 'External ID',
            'value': reference,
            'type': 'text',
            'source': 'reference_field'
        }]
        print(f"📝 從reference字段提取custom attribute: {reference}")
    
    # 檢查是否有其他可能的custom attribute字段
    potential_custom_fields = ['externalId', 'referenceId', 'customId', 'externalReference']
    for field in potential_custom_fields:
        field_value = rfi_data.get(field, '')
        if field_value and not any(attr.get('name') == field for attr in custom_attributes):
            custom_attributes.append({
                'name': field,
                'value': field_value,
                'type': 'text',
                'source': 'potential_custom_field'
            })
            print(f"📝 發現潛在custom attribute字段 {field}: {field_value}")
    
    print(f"🎯 最終處理得到 {len(custom_attributes)} 個custom attributes")
    
    # 確保這些字段是字符串類型（有些 API 可能返回列表或其他類型）
    if isinstance(priority, list):
        priority = ', '.join(str(_clean_text(str(p))) for p in priority) if priority else ''
    if isinstance(discipline, list):
        discipline = ', '.join(str(d) for d in discipline) if discipline else ''
    if isinstance(category, list):
        category = ', '.join(str(c) for c in category) if category else ''
    
    # 關聯文件和位置
    linked_document = rfi_data.get('linkedDocument', '')
    location_description = rfi_data.get('locationDescription', '')
    locations = rfi_data.get('locations', [])
    attachments_count = rfi_data.get('attachmentsCount', 0)
    comments_count = rfi_data.get('commentsCount', 0)
    
    # 調試信息
    print(f"🔍 RFI {rfi_id} - attachments_count: {attachments_count}, comments_count: {comments_count}")
    print(f"📊 原始數據中的 commentsCount: {rfi_data.get('commentsCount')}")
    
    # 回覆資訊
    official_response = rfi_data.get('officialResponse', '')
    official_response_status = rfi_data.get('officialResponseStatus', '')
    responded_at = rfi_data.get('respondedAt', '')
    responded_by = rfi_data.get('respondedBy', {})
    
    # 分析數據
    impact_analysis = _analyze_impact_assessment(cost_impact, schedule_impact)
    
    formatted_rfi = {
        # basicInfo
        'id': rfi_id,
        'custom_identifier': custom_identifier,
        'display_id': display_id,
        'title': title,
        'question': question,
        'description': description,
        'suggested_answer': suggested_answer,
        
        # 狀態和流程
        'status': status,
        'status_type': _analyze_rfi_status(status),
        'previous_status': previous_status,
        'workflow_type': workflow_type,
        
        # 人員指派
        'assigned_to': assigned_to,
        'assigned_to_type': assigned_to_type,
        'manager_id': manager_id,
        'reviewer_id': reviewer_id,
        'reviewers': reviewers,
        'created_by': created_by,
        'updated_by': updated_by,
        'closed_by': closed_by,
        
        # 日期和時程
        'due_date': utils.format_timestamp(due_date) if due_date else '',
        'start_date': utils.format_timestamp(start_date) if start_date else '',
        'created_at': utils.format_timestamp(created_at) if created_at else '',
        'updated_at': utils.format_timestamp(updated_at) if updated_at else '',
        'closed_at': utils.format_timestamp(closed_at) if closed_at else '',
        
        # 影響評估
        'cost_impact': cost_impact,
        'schedule_impact': schedule_impact,
        'impact_analysis': impact_analysis,
        
        # 分類和屬性
        'priority': priority,
        'priority_type': _analyze_rfi_priority(priority),
        'discipline': discipline,
        'category': category,
        'reference': reference,
        'custom_attributes': custom_attributes,
        'custom_attributes_count': len(custom_attributes) if custom_attributes else 0,
        
        # 關聯文件和位置
        'linked_document': linked_document,
        'location_description': location_description,
        'locations': locations,
        'attachments_count': attachments_count,
        'comments_count': comments_count,
        'has_attachments': attachments_count > 0,
        'has_comments': comments_count > 0,
        
        # 回覆資訊
        'official_response': official_response,
        'official_response_status': official_response_status,
        'responded_at': utils.format_timestamp(responded_at) if responded_at else '',
        'responded_by': responded_by,
        'has_response': bool(official_response),
        
        # 計算字段
        'is_open': status.lower() == 'open' if status else False,
        'is_closed': status.lower() == 'closed' if status else False,
        'is_answered': status.lower() == 'answered' if status else False,
        'is_draft': status.lower() == 'draft' if status else False,
        'is_overdue': False,  # 需要根據 due_date 計算
        'display_name': f"{display_id or custom_identifier}: {title}" if (display_id or custom_identifier) and title else title or f"RFI {rfi_id}",
        
        # 原始數據（用於調試）
        'raw_data': rfi_data
    }
    
    # 計算是否逾期（使用北京时间）
    if due_date:
        try:
            from datetime import datetime, timezone, timedelta
            due_datetime = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            # 转换为北京时间进行比较
            beijing_tz = timezone(timedelta(hours=8))
            due_beijing = due_datetime.astimezone(beijing_tz)
            now_beijing = datetime.now(beijing_tz)
            formatted_rfi['is_overdue'] = due_beijing < now_beijing and not formatted_rfi['is_closed']
        except:
            formatted_rfi['is_overdue'] = False
    
    # 添加参照信息（如果请求）
    if include_references and project_id and RELATIONS_API_AVAILABLE:
        try:
            relations_manager = RelationsManager()
            references = relations_manager.get_entity_references('rfi', rfi_id, project_id)
            formatted_rfi['references'] = references
            formatted_rfi['references_count'] = len(references)
            formatted_rfi['has_references'] = len(references) > 0
            
            # 统计参照类型
            ref_type_counts = {}
            for ref in references:
                ref_type = ref.get('ref_type', 'unknown')
                ref_type_counts[ref_type] = ref_type_counts.get(ref_type, 0) + 1
            formatted_rfi['reference_type_counts'] = ref_type_counts
            
        except Exception as e:
            print(f"获取RFI参照失败: {e}")
            formatted_rfi['references'] = []
            formatted_rfi['references_count'] = 0
            formatted_rfi['has_references'] = False
            formatted_rfi['reference_type_counts'] = {}
            formatted_rfi['references_error'] = str(e)
    else:
        # 默认值
        formatted_rfi['references'] = []
        formatted_rfi['references_count'] = 0
        formatted_rfi['has_references'] = False
        formatted_rfi['reference_type_counts'] = {}
    
    return formatted_rfi


@rfis_bp.route('/api/rfis/<project_id>/search', methods=['POST'])
@rfis_bp.route('/api/rfis/<project_id>/search%3Arfis', methods=['POST'])  # URL encoded colon
@rfis_bp.route('/api/rfis/<project_id>/searchrfis', methods=['POST'])  # Alternative without colon
def search_rfis(project_id):
    """搜索多個 RFIs"""
    # 移除 'b.' 前綴（RFIs API v3 要求純 UUID 格式）
    project_id = _strip_project_id_prefix(project_id)
    
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
    
    # 獲取請求體數據
    search_data = request.get_json() or {}
    
    # 獲取查詢參數
    limit = request.args.get('limit', 50, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    # 構建搜索請求體 - 根據API文檔優化
    search_payload = {
        'limit': min(limit, 200),  # 最大 200
        'offset': offset
    }
    
    # 處理搜索條件 - 根據API文檔格式化
    if search_data:
        # 處理文本搜索
        if 'search' in search_data and search_data['search']:
            search_text = str(search_data['search']).strip()
            if search_text:
                search_payload['search'] = search_text
        
        # 處理排序
        if 'sort' in search_data and search_data['sort']:
            if isinstance(search_data['sort'], list):
                search_payload['sort'] = search_data['sort']
            elif isinstance(search_data['sort'], dict):
                search_payload['sort'] = [search_data['sort']]
        
        # 處理過濾器 - 確保格式正確
        filter_obj = {}
        
        # 從search_data中提取過濾條件
        for key, value in search_data.items():
            if key in ['search', 'sort', 'limit', 'offset']:
                continue  # 這些已經處理過了
            elif key == 'filter' and isinstance(value, dict):
                # 如果直接提供了filter對象
                filter_obj.update(value)
            elif key in ['status', 'priority', 'discipline', 'category', 'assignedTo', 'createdBy']:
                # 直接的過濾字段
                if value:
                    if isinstance(value, list):
                        filter_obj[key] = value
                    else:
                        filter_obj[key] = [value] if key in ['assignedTo', 'createdBy', 'id', 'rfiTypeId'] else value
        
        # 只有當有過濾條件時才添加filter對象
        if filter_obj:
            search_payload['filter'] = filter_obj
    
    # 確保基本的搜索請求體結構正確
    if not search_payload.get('search') and not search_payload.get('filter'):
        # 如果沒有搜索條件，添加一個空的過濾器以確保API接受請求
        search_payload['filter'] = {}
    
    try:
        # 調用 Autodesk Construction Cloud RFIs API
        search_url = f"{config.AUTODESK_API_BASE}/construction/rfis/v3/projects/{project_id}/search:rfis"
        
        print(f"🔍 RFIs 搜索 API 請求:")
        print(f"   URL: {search_url}")
        print(f"   Project ID (原始): {request.args.get('projectId', 'N/A')}")
        print(f"   Project ID (處理後): {project_id}")
        print(f"   Headers: {headers}")
        print(f"   Payload: {json.dumps(search_payload, indent=2)}")
        
        # 驗證項目ID格式
        if not project_id or len(project_id) < 32:
            raise Exception(f"無效的項目ID格式: {project_id}")
        
        search_resp = requests.post(search_url, headers=headers, json=search_payload, timeout=30)
        
        print(f"📡 RFIs 搜索 API 響應:")
        print(f"   狀態碼: {search_resp.status_code}")
        print(f"   響應頭: {dict(search_resp.headers)}")
        
        if search_resp.status_code != 200:
            error_text = search_resp.text
            print(f"❌ RFIs 搜索 API 錯誤響應: {error_text}")
            
            # 提供更詳細的錯誤信息
            error_details = {
                "status_code": search_resp.status_code,
                "error_text": error_text,
                "request_url": search_url,
                "request_payload": search_payload,
                "project_id": project_id
            }
            
            # 嘗試解析錯誤響應
            try:
                error_json = search_resp.json()
                error_details["parsed_error"] = error_json
            except:
                pass
            
            return jsonify({
                "success": False,
                "error": f"RFI API 返回錯誤: {search_resp.status_code}",
                "message": error_text,
                "error_details": error_details,
                "suggestions": [
                    "檢查項目ID是否正確",
                    "確認用戶對該項目有RFI訪問權限",
                    "驗證Access Token是否有效",
                    "檢查項目是否支持RFI功能"
                ],
                "timestamp": datetime.now().isoformat()
            }), search_resp.status_code
        
        try:
            rfis_data = search_resp.json()
            print(f"RFIs 搜索 API 響應數據: {rfis_data}")
        except json.JSONDecodeError as e:
            print(f"JSON 解析錯誤: {e}")
            raise Exception(f"API 響應數據格式錯誤: {str(e)}")
        
        if not rfis_data:
            print("API 返回空 RFIs 數據")
            rfis_data = {"results": [], "pagination": {}}
        
        rfis_list = rfis_data.get("results", [])
        pagination = rfis_data.get("pagination", {})
        
        # 检查是否需要包含参照信息
        include_references = request.args.get('includeReferences', 'false').lower() == 'true'
        
        # 格式化 RFIs 數據
        formatted_rfis = []
        for rfi in rfis_list:
            formatted_rfi = _format_rfi_data(rfi, include_references, project_id)
            if formatted_rfi:
                formatted_rfis.append(formatted_rfi)
        
        # 生成統計信息
        total_rfis = pagination.get('totalResults', len(formatted_rfis))
        
        # 狀態統計
        status_counts = {}
        priority_counts = {}
        impact_counts = {'cost': 0, 'schedule': 0, 'both': 0, 'none': 0}
        
        for rfi in formatted_rfis:
            # 統計狀態
            status = rfi['status']
            if status:
                status_counts[status] = status_counts.get(status, 0) + 1
            
            # 統計優先級
            priority = rfi['priority']
            if priority:
                priority_counts[priority] = priority_counts.get(priority, 0) + 1
            
            # 統計影響
            impact_analysis = rfi['impact_analysis']
            if impact_analysis['has_cost_impact'] and impact_analysis['has_schedule_impact']:
                impact_counts['both'] += 1
            elif impact_analysis['has_cost_impact']:
                impact_counts['cost'] += 1
            elif impact_analysis['has_schedule_impact']:
                impact_counts['schedule'] += 1
            else:
                impact_counts['none'] += 1
        
        # 其他統計
        open_rfis = len([r for r in formatted_rfis if r['is_open']])
        closed_rfis = len([r for r in formatted_rfis if r['is_closed']])
        answered_rfis = len([r for r in formatted_rfis if r['is_answered']])
        overdue_rfis = len([r for r in formatted_rfis if r['is_overdue']])
        with_attachments = len([r for r in formatted_rfis if r['has_attachments']])
        with_responses = len([r for r in formatted_rfis if r['has_response']])
        
        stats = {
            "total_rfis": total_rfis,
            "current_page_count": len(formatted_rfis),
            "status_counts": status_counts,
            "priority_counts": priority_counts,
            "impact_counts": impact_counts,
            "open_rfis": open_rfis,
            "closed_rfis": closed_rfis,
            "answered_rfis": answered_rfis,
            "overdue_rfis": overdue_rfis,
            "with_attachments": with_attachments,
            "with_responses": with_responses,
            "completion_rate": round((closed_rfis / len(formatted_rfis)) * 100, 1) if formatted_rfis else 0,
            "response_rate": round((with_responses / len(formatted_rfis)) * 100, 1) if formatted_rfis else 0
        }
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "search_payload": search_payload,
            "stats": stats,
            "rfis": formatted_rfis,
            "pagination": pagination,
            "raw_data": rfis_list,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"搜索 RFIs 時出錯: {str(e)}")
        return jsonify({
            "error": f"搜索 RFIs 失敗: {str(e)}",
            "status": "error"
        }), 500


@rfis_bp.route('/api/rfis/<project_id>')
def get_project_rfis(project_id):
    """獲取項目的所有 RFIs（使用搜索 API）"""
    # 移除 'b.' 前綴（RFIs API v3 要求純 UUID 格式）
    project_id = _strip_project_id_prefix(project_id)
    
    # 使用搜索 API 獲取所有 RFIs
    search_data = {}
    
    # 從查詢參數獲取過濾條件
    status_filter = request.args.get('status')
    priority_filter = request.args.get('priority')
    discipline_filter = request.args.get('discipline')
    category_filter = request.args.get('category')
    
    if status_filter:
        search_data['status'] = status_filter
    if priority_filter:
        search_data['priority'] = priority_filter
    if discipline_filter:
        search_data['discipline'] = discipline_filter
    if category_filter:
        search_data['category'] = category_filter
    
    # 模擬 POST 請求
    from flask import request as flask_request
    original_method = flask_request.method
    original_json = getattr(flask_request, '_cached_json', None)
    
    try:
        # 臨時修改請求方法和數據
        flask_request.method = 'POST'
        flask_request._cached_json = (search_data, True)
        
        # 調用搜索函數
        return search_rfis(project_id)
        
    finally:
        # 恢復原始請求
        flask_request.method = original_method
        if original_json is not None:
            flask_request._cached_json = original_json
        else:
            if hasattr(flask_request, '_cached_json'):
                delattr(flask_request, '_cached_json')


@rfis_bp.route('/api/rfis/<project_id>/<rfi_id>')
def get_single_rfi(project_id, rfi_id):
    """獲取單個 RFI 的詳細信息"""
    # 移除 'b.' 前綴（RFIs API v3 要求純 UUID 格式）
    project_id = _strip_project_id_prefix(project_id)
    
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
        # 調用 Autodesk Construction Cloud RFIs API
        rfi_url = f"{config.AUTODESK_API_BASE}/construction/rfis/v3/projects/{project_id}/rfis/{rfi_id}"
        
        print(f"RFI 詳情 API 請求 URL: {rfi_url}")
        
        rfi_resp = requests.get(rfi_url, headers=headers, timeout=30)
        
        print(f"RFI 詳情 API 響應狀態碼: {rfi_resp.status_code}")
        
        if rfi_resp.status_code != 200:
            error_text = rfi_resp.text
            print(f"RFI 詳情 API 錯誤響應: {error_text}")
            raise Exception(f"獲取 RFI 詳情失敗: {rfi_resp.status_code} - {error_text}")
        
        try:
            rfi_data = rfi_resp.json()
            print(f"RFI 詳情 API 響應數據: {rfi_data}")
        except json.JSONDecodeError as e:
            print(f"JSON 解析錯誤: {e}")
            raise Exception(f"API 響應數據格式錯誤: {str(e)}")
        
        if not rfi_data:
            print("API 返回空 RFI 數據")
            return jsonify({
                "error": "RFI 不存在或無法訪問",
                "status": "not_found"
            }), 404
        
        # 检查是否需要包含参照信息
        include_references = request.args.get('includeReferences', 'false').lower() == 'true'
        
        # 格式化 RFI 數據
        formatted_rfi = _format_rfi_data(rfi_data, include_references, project_id)
        
        if not formatted_rfi:
            return jsonify({
                "error": "RFI 數據格式錯誤",
                "status": "error"
            }), 500
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "rfi_id": rfi_id,
            "rfi": formatted_rfi,
            "raw_data": rfi_data,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"獲取 RFI 詳情時出錯: {str(e)}")
        return jsonify({
            "error": f"獲取 RFI 詳情失敗: {str(e)}",
            "status": "error"
        }), 500


# ==================== 具體路由（必須在通用路由之前） ====================

@rfis_bp.route('/api/rfis/jarvis/test-download')
def test_download_route():
    """測試下載路由是否正常註冊"""
    import datetime
    return jsonify({
        "success": True,
        "message": "下載路由測試成功 - 新版本代碼正在運行",
        "route": "/api/rfis/jarvis/test-download",
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "2024-10-21-fixed",
        "features": [
            "URL validation added",
            "No more raw_urn returns",
            "Enhanced error handling",
            "Debug logging enabled"
        ]
    })


@rfis_bp.route('/api/rfis/jarvis/<rfi_id>/attachments/<attachment_id>/download', methods=['GET'])
def download_jarvis_rfi_attachment(rfi_id, attachment_id):
    """下載指定項目中指定 RFI 的附件（簡化路由）"""
    print(f"🔄 [JARVIS路由] 下載路由被調用: RFI ID = {rfi_id}, 附件 ID = {attachment_id}")
    
    project_id = request.args.get('projectId')
    print(f"🔄 [JARVIS路由] 項目 ID 參數: {project_id}")
    
    if not project_id:
        print(f"❌ [JARVIS路由] 缺少 projectId 參數")
        return jsonify({
            "error": "缺少必需的 projectId 參數",
            "message": "請在請求中提供 projectId 參數",
            "status": "error"
        }), 400
    
    print(f"🔄 [JARVIS路由] 調用主下載函數: download_rfi_attachment({project_id}, {rfi_id}, {attachment_id})")
    result = download_rfi_attachment(project_id, rfi_id, attachment_id)
    print(f"🔄 [JARVIS路由] 主下載函數返回結果類型: {type(result)}")
    
    return result


@rfis_bp.route('/api/rfis/jarvis/<rfi_id>/attachments')
def get_jarvis_rfi_attachments(rfi_id):
    """獲取指定項目中指定 RFI 的附件（簡化路由）"""
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 參數",
            "message": "請在請求中提供 projectId 參數",
            "status": "error"
        }), 400
    
    return get_rfi_attachments(project_id, rfi_id)


@rfis_bp.route('/api/rfis/jarvis/<rfi_id>/comments')
def get_jarvis_rfi_comments(rfi_id):
    """獲取指定項目中指定 RFI 的評論（簡化路由）"""
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 參數",
            "message": "請在請求中提供 projectId 參數",
            "status": "error"
        }), 400
    
    return get_rfi_comments(project_id, rfi_id)


@rfis_bp.route('/api/rfis/jarvis/workflow/<project_id>')
def get_rfi_workflow_config(project_id):
    """獲取 RFI 工作流配置"""
    # 移除 'b.' 前綴（RFIs API v3 要求純 UUID 格式）
    project_id = _strip_project_id_prefix(project_id)
    
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
        # 調用 Autodesk Construction Cloud RFIs Workflow API
        workflow_url = f"{config.AUTODESK_API_BASE}/construction/rfis/v3/projects/{project_id}/workflow"
        
        print(f"RFI 工作流 API 請求 URL: {workflow_url}")
        
        workflow_resp = requests.get(workflow_url, headers=headers, timeout=30)
        
        print(f"RFI 工作流 API 響應狀態碼: {workflow_resp.status_code}")
        
        if workflow_resp.status_code == 200:
            try:
                workflow_data = workflow_resp.json()
                print(f"RFI 工作流 API 響應數據: {workflow_data}")
                
                return jsonify({
                    "success": True,
                    "workflow": workflow_data,
                    "timestamp": datetime.now().isoformat(),
                    "project_id": project_id
                })
                
            except json.JSONDecodeError as e:
                print(f"JSON 解析錯誤: {e}")
                raise Exception(f"API 響應數據格式錯誤: {str(e)}")
        
        elif workflow_resp.status_code == 404:
            # 如果 API 不存在，返回默認配置
            print("RFI 工作流 API 不存在，返回默認配置")
            default_workflow = {
                "workflowType": "US",
                "description": "Default RFI workflow configuration",
                "projectRolesMapping": [
                    {
                        "name": "projectGC",
                        "permittedAssignees": []
                    },
                    {
                        "name": "projectSC", 
                        "permittedAssignees": []
                    },
                    {
                        "name": "projectCoordinator",
                        "permittedAssignees": []
                    },
                    {
                        "name": "projectReviewer",
                        "permittedAssignees": []
                    }
                ]
            }
            
            return jsonify({
                "success": True,
                "workflow": default_workflow,
                "timestamp": datetime.now().isoformat(),
                "project_id": project_id,
                "note": "Using default workflow configuration (API not available)"
            })
        
        else:
            error_text = workflow_resp.text
            print(f"RFI 工作流 API 錯誤響應: {error_text}")
            raise Exception(f"獲取 RFI 工作流配置失敗: {workflow_resp.status_code} - {error_text}")
    
    except Exception as e:
        print(f"獲取 RFI 工作流配置時發生錯誤: {str(e)}")
        
        # 返回默認配置作為備用
        default_workflow = {
            "workflowType": "US",
            "description": "Default RFI workflow configuration (fallback)",
            "projectRolesMapping": [
                {
                    "name": "projectGC",
                    "permittedAssignees": []
                },
                {
                    "name": "projectSC", 
                    "permittedAssignees": []
                },
                {
                    "name": "projectCoordinator",
                    "permittedAssignees": []
                },
                {
                    "name": "projectReviewer",
                    "permittedAssignees": []
                }
            ]
        }
        
        return jsonify({
            "success": True,
            "workflow": default_workflow,
            "timestamp": datetime.now().isoformat(),
            "project_id": project_id,
            "error": str(e),
            "note": "Using default workflow configuration due to API error"
        })


# ==================== 通用路由（必須在具體路由之後） ====================

@rfis_bp.route('/api/rfis/jarvis', methods=['GET', 'POST'])
def get_jarvis_rfis():
    """獲取項目的 RFIs 數據 - 支持動態項目 ID（GET 和 POST）"""
    # 獲取項目 ID - 必須通過參數提供
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 參數",
            "message": "請在請求中提供 projectId 參數，例如: ?projectId=your-project-id",
            "status": "error",
            "suggestion": "請先選擇一個項目，然後重試"
        }), 400
    
    print(f"🚀 RFIs API: 使用項目 ID: {project_id}")
    
    # 如果是 POST 請求，直接調用搜索函數
    if request.method == 'POST':
        return search_rfis(project_id)
    else:
        # GET 請求使用原來的方式
        return get_project_rfis(project_id)


@rfis_bp.route('/api/rfis/jarvis/<rfi_id>')
def get_jarvis_single_rfi(rfi_id):
    """獲取指定項目中的單個 RFI 詳情（簡化路由）"""
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 參數",
            "message": "請在請求中提供 projectId 參數",
            "status": "error"
        }), 400
    
    return get_single_rfi(project_id, rfi_id)


# ==================== RFI 附件相關接口 ====================

@rfis_bp.route('/api/rfis/<project_id>/<rfi_id>/attachments')
def get_rfi_attachments(project_id, rfi_id):
    """獲取 RFI 的附件列表"""
    # 移除 'b.' 前綴（RFIs API v3 要求純 UUID 格式）
    project_id = _strip_project_id_prefix(project_id)
    
    access_token = utils.get_access_token()
    if not access_token:
        return jsonify({
            "error": "未找到 Access Token，請先進行認證",
            "status": "unauthorized"
        }), 401
    
    try:
        # 使用 RFI 專用的附件 API 端點
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # 獲取查詢參數
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        attachment_types = request.args.getlist('filter[attachmentTypes]')
        
        params = {
            'limit': min(limit, 200),
            'offset': offset
        }
        
        # 如果沒有指定附件類型，使用默認值
        if attachment_types:
            params['filter[attachmentTypes]'] = attachment_types
        else:
            # 默認過濾器：rfiResponse, rfiOfficialResponse
            params['filter[attachmentTypes]'] = ['rfiResponse', 'rfiOfficialResponse']
        
        # 使用正確的 RFI 附件 API 端點
        attachments_url = f"{config.AUTODESK_API_BASE}/construction/rfis/v3/projects/{project_id}/rfis/{rfi_id}/attachments"
        
        print(f"RFI 附件 API 請求 URL: {attachments_url}")
        print(f"RFI 附件 API 請求參數: {params}")
        
        attachments_resp = requests.get(attachments_url, headers=headers, params=params, timeout=30)
        
        print(f"RFI 附件 API 響應狀態碼: {attachments_resp.status_code}")
        
        if attachments_resp.status_code != 200:
            error_text = attachments_resp.text
            print(f"RFI 附件 API 錯誤響應: {error_text}")
            # 如果獲取附件失敗，返回空列表而不是錯誤
            return jsonify({
                "success": True,
                "project_id": project_id,
                "rfi_id": rfi_id,
                "attachments": [],
                "message": f"無法獲取附件: {attachments_resp.status_code}",
                "timestamp": datetime.now().isoformat()
            })
        
        try:
            attachments_data = attachments_resp.json()
            print(f"RFI 附件 API 響應數據: {attachments_data}")
        except json.JSONDecodeError as e:
            print(f"JSON 解析錯誤: {e}")
            return jsonify({
                "success": True,
                "project_id": project_id,
                "rfi_id": rfi_id,
                "attachments": [],
                "message": "Attachment data format error",
                "timestamp": datetime.now().isoformat()
            })
        
        attachments_list = attachments_data.get("results", [])
        
        # 格式化附件數據（根據 RFI 附件 API 響應結構）
        # 處理附件數據並去重
        formatted_attachments = []
        seen_attachments = {}  # 用於去重：key = (name, file_size), value = attachment_info
        
        for attachment in attachments_list:
            # 跳過已刪除的附件
            if attachment.get('isDeleted', False):
                continue
                
            formatted_attachment = {
                'id': attachment.get('attachmentId', ''),
                'name': attachment.get('displayName', ''),
                'file_name': attachment.get('fileName', ''),
                'attachment_type': attachment.get('attachmentType', ''),
                'file_type': attachment.get('fileType', '').upper() if attachment.get('fileType') else 'UNKNOWN',
                'file_size': attachment.get('fileSize', 0),
                'version': attachment.get('version', 1),
                'created_time': utils.format_timestamp(attachment.get('createdOn', '')),
                'modified_time': utils.format_timestamp(attachment.get('modifiedOn', '')),
                'created_by': attachment.get('createdBy', ''),
                'created_by_name': attachment.get('createdByName', ''),
                'modified_by': attachment.get('modifiedBy', ''),
                'storage_urn': attachment.get('storageUrn', ''),
                'version_urn': attachment.get('versionUrn', ''),
                'lineage_urn': attachment.get('lineageUrn', ''),
                'is_deleted': attachment.get('isDeleted', False),
                'deleted_on': utils.format_timestamp(attachment.get('deletedOn', '')) if attachment.get('deletedOn') else '',
                'deleted_by': attachment.get('deletedBy', ''),
                'rfi_id': attachment.get('rfiId', ''),
                'container_id': attachment.get('containerId', ''),
                'docs_id': attachment.get('docsId', '')
            }
            
            # 去重邏輯：基於文件名和大小
            dedup_key = (formatted_attachment['name'], formatted_attachment['file_size'])
            
            if dedup_key in seen_attachments:
                # 如果已存在相同文件，比較版本和修改時間，保留最新的
                existing = seen_attachments[dedup_key]
                current_version = formatted_attachment['version']
                existing_version = existing['version']
                
                # 比較版本號，如果版本號相同則比較修改時間
                should_replace = False
                if current_version > existing_version:
                    should_replace = True
                elif current_version == existing_version:
                    # 版本號相同，比較修改時間
                    current_modified = formatted_attachment['modified_time']
                    existing_modified = existing['modified_time']
                    if current_modified > existing_modified:
                        should_replace = True
                
                if should_replace:
                    # 替換為更新的版本
                    print(f"🔄 替換重複附件: {formatted_attachment['name']} (v{existing_version} -> v{current_version})")
                    seen_attachments[dedup_key] = formatted_attachment
                else:
                    print(f"⏭️ 跳過舊版本附件: {formatted_attachment['name']} (v{current_version} <= v{existing_version})")
            else:
                # 新文件，直接添加
                seen_attachments[dedup_key] = formatted_attachment
        
        # 將去重後的附件轉換為列表
        formatted_attachments = list(seen_attachments.values())
        
        # 按修改時間倒序排列（最新的在前）
        formatted_attachments.sort(key=lambda x: x['modified_time'], reverse=True)
        
        print(f"📎 附件去重結果: 原始 {len(attachments_list)} 個 -> 去重後 {len(formatted_attachments)} 個")
        
        # 統計信息
        total_attachments = len(formatted_attachments)
        file_types = {}
        attachment_types = {}
        total_size = 0
        
        for attachment in formatted_attachments:
            # 統計文件類型
            file_type = attachment['file_type']
            file_types[file_type] = file_types.get(file_type, 0) + 1
            
            # 統計附件類型
            attachment_type = attachment['attachment_type']
            attachment_types[attachment_type] = attachment_types.get(attachment_type, 0) + 1
            
            # 計算總大小
            total_size += attachment['file_size']
        
        stats = {
            'total_attachments': total_attachments,
            'original_attachments_count': len(attachments_list),
            'duplicates_removed': len(attachments_list) - total_attachments,
            'file_types': file_types,
            'attachment_types': attachment_types,
            'total_size': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2) if total_size > 0 else 0
        }
        
        # 獲取分頁信息
        pagination = attachments_data.get("pagination", {})
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "rfi_id": rfi_id,
            "query_params": params,
            "stats": stats,
            "attachments": formatted_attachments,
            "pagination": pagination,
            "raw_data": attachments_list,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"獲取 RFI 附件時出錯: {str(e)}")
        return jsonify({
            "error": f"獲取 RFI 附件失敗: {str(e)}",
            "status": "error"
        }), 500


@rfis_bp.route('/api/rfis/<project_id>/<rfi_id>/attachments/<attachment_id>/download')
def download_rfi_attachment(project_id, rfi_id, attachment_id):
    """下載 RFI 附件"""
    print(f"🚀 [主下載函數] 開始處理下載請求:")
    print(f"   - project_id: {project_id}")
    print(f"   - rfi_id: {rfi_id}")
    print(f"   - attachment_id: {attachment_id}")
    
    # 移除 'b.' 前綴（RFIs API v3 要求純 UUID 格式）
    original_project_id = project_id
    project_id = _strip_project_id_prefix(project_id)
    print(f"   - 處理後的 project_id: {original_project_id} -> {project_id}")
    
    access_token = utils.get_access_token()
    if not access_token:
        return jsonify({
            "error": "未找到 Access Token，請先進行認證",
            "status": "unauthorized"
        }), 401
    
    try:
        # 首先獲取附件信息
        attachments_response = get_rfi_attachments(project_id, rfi_id)
        
        if hasattr(attachments_response, 'get_json'):
            attachments_data = attachments_response.get_json()
        else:
            attachments_data = attachments_response
        
        if not attachments_data or not attachments_data.get('success'):
            return jsonify({
                "error": "Unable to get attachment information",
                "status": "error"
            }), 500
        
        # 查找指定的附件
        target_attachment = None
        for attachment in attachments_data.get('attachments', []):
            if attachment.get('id') == attachment_id:
                target_attachment = attachment
                break
        
        if not target_attachment:
            return jsonify({
                "error": "Attachment does not exist",
                "status": "not_found"
            }), 404
        
        # 獲取下載 URL
        storage_urn = target_attachment.get('storage_urn')
        version_urn = target_attachment.get('version_urn')
        lineage_urn = target_attachment.get('lineage_urn')
        
        print(f"附件下載信息:")
        print(f"  - storage_urn: {storage_urn}")
        print(f"  - version_urn: {version_urn}")
        print(f"  - lineage_urn: {lineage_urn}")
        
        if not storage_urn and not version_urn and not lineage_urn:
            return jsonify({
                "error": "Unable to get attachment download link",
                "status": "error"
            }), 500
        
        # 使用通用URN下载模块
        attachment_name = target_attachment.get('name') or target_attachment.get('display_name') or target_attachment.get('file_name', 'Unknown file')
        download_result = None
        
        # 优先使用storage_urn
        if storage_urn:
            print(f"使用storage URN下载: {storage_urn}")
            download_result = download_by_urn(storage_urn, access_token, attachment_name)
        elif version_urn:
            print(f"使用version URN下载: {version_urn}")
            download_result = download_by_urn(version_urn, access_token, attachment_name)
        elif lineage_urn:
            print(f"使用lineage URN下载: {lineage_urn}")
            # 对于lineage URN，需要项目ID
            from .urn_download_simple import download_document_lineage
            download_result = download_document_lineage(lineage_urn, f"b.{project_id}", access_token, attachment_name)
        
        # 检查下载结果
        if download_result and download_result.get('success'):
            print(f"SUCCESS: 成功获取附件下载链接，文件名: {attachment_name}")
            return jsonify({
                "success": True,
                "download_url": download_result.get('download_url'),
                "attachment_name": download_result.get('document_name', attachment_name),
                "file_size": target_attachment.get('file_size', 0),
                "requires_auth": download_result.get('requires_auth', False),
                "method": download_result.get('method', 'urn_download_module')
            })
        
        # 如果下载失败，返回详细错误信息
        error_msg = "Unable to get attachment download link"
        if download_result:
            error_msg = download_result.get('error', error_msg)
        
        print(f"ERROR: 所有下载方法都失败了，无法获取附件下载链接")
        
        final_response = {
            "success": False,
            "error": error_msg,
            "attachment_name": attachment_name,
            "file_size": target_attachment.get('file_size', 0),
            "message": "此附件无法直接下载，请尝试以下方式",
            "suggestions": [
                "在 Autodesk Construction Cloud 网页版中下载",
                "联系项目管理员检查附件权限", 
                "检查附件是否已被删除或移动",
                "确认您有足够的项目权限"
            ],
            "debug_info": {
                "attachment_id": attachment_id,
                "rfi_id": rfi_id,
                "project_id": project_id,
                "version_urn": version_urn,
                "storage_urn": storage_urn,
                "lineage_urn": lineage_urn,
                "attachment_type": target_attachment.get('attachment_type', ''),
                "created_time": target_attachment.get('created_time', ''),
                "file_type": target_attachment.get('file_type', ''),
                "download_result": download_result,
                "methods_tried": ["URN Download Module"]
            }
        }
        
        return jsonify(final_response), 400
        
    except Exception as e:
        print(f"下載 RFI 附件時出錯: {str(e)}")
        return jsonify({
            "error": f"下載 RFI 附件失敗: {str(e)}",
            "status": "error"
        }), 500


# ==================== RFI 評論相關接口 ====================

@rfis_bp.route('/api/rfis/<project_id>/<rfi_id>/comments')
def get_rfi_comments(project_id, rfi_id):
    """獲取 RFI 的評論列表 - 直接調用 Autodesk API"""
    # 移除 'b.' 前綴（RFIs API v3 要求純 UUID 格式）
    project_id = _strip_project_id_prefix(project_id)
    
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
        # 直接調用 Autodesk RFI Comments API
        url = f"https://developer.api.autodesk.com/construction/rfis/v3/projects/{project_id}/rfis/{rfi_id}/comments"
        
        # 構建查詢參數（支持API文檔中的所有參數）
        params = {
            'limit': min(request.args.get('limit', 50, type=int), 200),  # 限制最大值為200
            'offset': request.args.get('offset', 0, type=int)
        }
        
        # 可選的排序參數
        sort_fields = request.args.getlist('sort')
        if sort_fields:
            params['sort'] = sort_fields
        
        # 可選的字段過濾參數
        fields = request.args.getlist('fields')
        if fields:
            params['fields'] = ','.join(fields)
        
        # 可選的創建時間過濾
        created_at_filter = request.args.get('filter[createdAt]')
        if created_at_filter:
            params['filter[createdAt]'] = created_at_filter
        
        # 可選的創建者過濾
        created_by_filter = request.args.getlist('filter[createdBy]')
        if created_by_filter:
            params['filter[createdBy]'] = created_by_filter
        
        print(f"🔍 調用 RFI Comments API: {url}")
        print(f"📊 參數: {params}")
        
        response = requests.get(url, headers=headers, params=params)
        
        print(f"📈 API 響應狀態碼: {response.status_code}")
        print(f"📄 API 響應內容: {response.text[:500]}...")  # 只顯示前500字符
        
        if response.status_code == 200:
            api_data = response.json()
            comments_list = api_data.get('results', [])
            
            print(f"🔍 解析後的API數據: {api_data}")
            print(f"📝 評論列表長度: {len(comments_list)}")
            print(f"📋 評論列表內容: {comments_list}")
            
            # 格式化評論數據
            formatted_comments = []
            for comment in comments_list:
                formatted_comment = {
                    'id': comment.get('id', ''),
                    'type': 'comment',
                    'content': comment.get('body', ''),
                    'author': {
                        'id': comment.get('createdBy', ''),
                        'name': comment.get('createdBy', '')  # 暫時使用ID，後續可以通過用戶API獲取真實姓名
                    },
                    'created_at': utils.format_timestamp(comment.get('createdAt', '')),
                    'updated_at': utils.format_timestamp(comment.get('updatedAt', '')),
                    'is_draft': False,
                    'source': comment.get('source', 'web'),
                    'raw_data': comment
                }
                formatted_comments.append(formatted_comment)
            
            # 統計信息
            pagination = api_data.get('pagination', {})
            total_comments = pagination.get('totalResults', len(formatted_comments))
            
            stats = {
                'total_comments': total_comments,
                'loaded_comments': len(formatted_comments),
                'has_comments': total_comments > 0,
                'pagination': pagination
            }
            
            result = {
                "success": True,
                "project_id": project_id,
                "rfi_id": rfi_id,
                "stats": stats,
                "comments": formatted_comments,
                "pagination": pagination,
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"✅ 成功返回評論數據: {len(formatted_comments)} 條評論")
            print(f"📊 統計信息: {stats}")
            
            return jsonify(result)
            
        elif response.status_code == 404:
            # RFI 不存在或沒有評論
            print("ℹ️ Autodesk API 返回 404 - RFI 沒有評論或 RFI 不存在")
            
            result = {
                "success": True,
                "project_id": project_id,
                "rfi_id": rfi_id,
                "stats": {
                    'total_comments': 0,
                    'loaded_comments': 0,
                    'has_comments': False
                },
                "comments": [],
                "message": "This RFI has no comments",
                "reason": "autodesk_api_404",
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"📋 返回空評論結果: {result}")
            return jsonify(result)
            
        else:
            error_msg = f"API 調用失敗: {response.status_code}"
            try:
                error_data = response.json()
                error_msg = error_data.get('message', error_msg)
            except:
                pass
            
            print(f"❌ RFI Comments API 錯誤: {response.status_code} - {error_msg}")
            return jsonify({
                "error": error_msg,
                "status_code": response.status_code,
                "status": "error"
            }), response.status_code
        
    except Exception as e:
        print(f"❌ 獲取 RFI 評論時出錯: {str(e)}")
        return jsonify({
            "error": f"獲取 RFI 評論失敗: {str(e)}",
            "status": "error"
        }), 500


# ==================== RFI 統計和分析接口 ====================

@rfis_bp.route('/api/rfis/<project_id>/statistics')
def get_rfis_statistics(project_id):
    """獲取項目 RFIs 的統計分析"""
    # 移除 'b.' 前綴（RFIs API v3 要求純 UUID 格式）
    project_id = _strip_project_id_prefix(project_id)
    
    try:
        # 獲取所有 RFIs
        rfis_response = get_project_rfis(project_id)
        
        # 檢查是否是 Flask 響應對象（包括錯誤響應）
        if hasattr(rfis_response, 'get_json'):
            rfis_data = rfis_response.get_json()
        elif isinstance(rfis_response, tuple):
            # 如果是錯誤響應元組 (response, status_code)
            response_obj, status_code = rfis_response
            if hasattr(response_obj, 'get_json'):
                error_data = response_obj.get_json()
                return jsonify({
                    "error": "無法獲取 RFIs 數據 - 上游服務返回錯誤",
                    "status": "error",
                    "upstream_error": error_data,
                    "upstream_status": status_code
                }), 500
            else:
                return jsonify({
                    "error": "無法獲取 RFIs 數據 - 上游服務返回錯誤",
                    "status": "error",
                    "upstream_status": status_code
                }), 500
        else:
            rfis_data = rfis_response
        
        if not rfis_data or not isinstance(rfis_data, dict) or not rfis_data.get('success'):
            return jsonify({
                "error": "無法獲取 RFIs 數據",
                "status": "error"
            }), 500
        
        rfis_list = rfis_data.get('rfis', [])
        
        # 詳細統計分析
        statistics = {
            'overview': {
                'total_rfis': len(rfis_list),
                'open_rfis': len([r for r in rfis_list if r['is_open']]),
                'closed_rfis': len([r for r in rfis_list if r['is_closed']]),
                'answered_rfis': len([r for r in rfis_list if r['is_answered']]),
                'overdue_rfis': len([r for r in rfis_list if r['is_overdue']]),
            },
            'status_distribution': {},
            'priority_distribution': {},
            'discipline_distribution': {},
            'category_distribution': {},
            'impact_analysis': {
                'cost_impact': len([r for r in rfis_list if r['impact_analysis']['has_cost_impact']]),
                'schedule_impact': len([r for r in rfis_list if r['impact_analysis']['has_schedule_impact']]),
                'both_impacts': len([r for r in rfis_list if r['impact_analysis']['has_cost_impact'] and r['impact_analysis']['has_schedule_impact']]),
                'no_impact': len([r for r in rfis_list if not r['impact_analysis']['has_cost_impact'] and not r['impact_analysis']['has_schedule_impact']])
            },
            'response_analysis': {
                'with_responses': len([r for r in rfis_list if r['has_response']]),
                'without_responses': len([r for r in rfis_list if not r['has_response']]),
                'response_rate': round((len([r for r in rfis_list if r['has_response']]) / len(rfis_list)) * 100, 1) if rfis_list else 0
            },
            'attachment_analysis': {
                'with_attachments': len([r for r in rfis_list if r['has_attachments']]),
                'without_attachments': len([r for r in rfis_list if not r['has_attachments']]),
                'total_attachments': sum([r['attachments_count'] for r in rfis_list])
            },
            'time_analysis': {
                'created_this_month': 0,
                'created_this_week': 0,
                'closed_this_month': 0,
                'closed_this_week': 0
            }
        }
        
        # 計算分布統計
        for rfi in rfis_list:
            try:
                # 狀態分布
                status = rfi.get('status', '')
                if status and isinstance(status, str):
                    statistics['status_distribution'][status] = statistics['status_distribution'].get(status, 0) + 1
                
                # 優先級分布
                priority = rfi.get('priority', '')
                if priority and isinstance(priority, str):
                    statistics['priority_distribution'][priority] = statistics['priority_distribution'].get(priority, 0) + 1
                
                # 專業領域分布
                discipline = rfi.get('discipline', '')
                if discipline and isinstance(discipline, str):
                    statistics['discipline_distribution'][discipline] = statistics['discipline_distribution'].get(discipline, 0) + 1
                
                # 類別分布
                category = rfi.get('category', '')
                if category and isinstance(category, str):
                    statistics['category_distribution'][category] = statistics['category_distribution'].get(category, 0) + 1
            except Exception as e:
                # 如果某個 RFI 數據有問題，跳過並繼續處理下一個
                print(f"警告：處理 RFI 統計時出錯: {str(e)}")
                continue
        
        # 計算完成率和效率指標
        total_rfis = statistics['overview']['total_rfis']
        if total_rfis > 0:
            statistics['efficiency_metrics'] = {
                'completion_rate': round((statistics['overview']['closed_rfis'] / total_rfis) * 100, 1),
                'response_rate': statistics['response_analysis']['response_rate'],
                'overdue_rate': round((statistics['overview']['overdue_rfis'] / total_rfis) * 100, 1),
                'attachment_rate': round((statistics['attachment_analysis']['with_attachments'] / total_rfis) * 100, 1)
            }
        else:
            statistics['efficiency_metrics'] = {
                'completion_rate': 0,
                'response_rate': 0,
                'overdue_rate': 0,
                'attachment_rate': 0
            }
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "statistics": statistics,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"獲取 RFIs 統計時出錯: {str(e)}")
        return jsonify({
            "error": f"獲取 RFIs 統計失敗: {str(e)}",
            "status": "error"
        }), 500


@rfis_bp.route('/api/rfis/jarvis/statistics')
def get_jarvis_rfis_statistics():
    """獲取指定項目的 RFIs 統計（簡化路由）"""
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 參數",
            "message": "請在請求中提供 projectId 參數",
            "status": "error"
        }), 400
    
    return get_rfis_statistics(project_id)


# ==================== RFI 配置和元數據接口 ====================

@rfis_bp.route('/api/rfis/<project_id>/users/me')
def get_rfi_user_permissions(project_id):
    """獲取當前用戶在項目中的 RFI 權限和工作流角色"""
    # 移除 'b.' 前綴（RFIs API v3 要求純 UUID 格式）
    project_id = _strip_project_id_prefix(project_id)
    
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
        # 調用 Autodesk Construction Cloud RFIs API
        users_me_url = f"{config.AUTODESK_API_BASE}/construction/rfis/v3/projects/{project_id}/users/me"
        
        print(f"RFI 用戶權限 API 請求 URL: {users_me_url}")
        
        users_me_resp = requests.get(users_me_url, headers=headers, timeout=30)
        
        print(f"RFI 用戶權限 API 響應狀態碼: {users_me_resp.status_code}")
        
        if users_me_resp.status_code != 200:
            error_text = users_me_resp.text
            print(f"RFI 用戶權限 API 錯誤響應: {error_text}")
            # 如果是 404 或其他非致命錯誤，返回空權限而不是拋出異常
            if users_me_resp.status_code in [403, 404]:
                return jsonify({
                    "success": True,
                    "project_id": project_id,
                    "user_permissions": {},
                    "message": f"無法獲取用戶權限 (HTTP {users_me_resp.status_code})",
                    "timestamp": datetime.now().isoformat()
                })
            raise Exception(f"獲取用戶權限失敗: {users_me_resp.status_code} - {error_text}")
        
        try:
            users_me_data = users_me_resp.json()
            print(f"RFI 用戶權限 API 響應數據: {users_me_data}")
        except json.JSONDecodeError as e:
            print(f"JSON 解析錯誤: {e}")
            raise Exception(f"API 響應數據格式錯誤: {str(e)}")
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "user_permissions": users_me_data,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"獲取 RFI 用戶權限時出錯: {str(e)}")
        return jsonify({
            "error": f"獲取 RFI 用戶權限失敗: {str(e)}",
            "status": "error"
        }), 500


@rfis_bp.route('/api/rfis/jarvis/users/me')
def get_jarvis_rfi_user_permissions():
    """獲取指定項目中當前用戶的 RFI 權限（簡化路由）"""
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 參數",
            "message": "請在請求中提供 projectId 參數",
            "status": "error"
        }), 400
    
    return get_rfi_user_permissions(project_id)


@rfis_bp.route('/api/rfis/<project_id>/rfi-types')
def get_rfi_types(project_id):
    """獲取項目的 RFI 類型配置"""
    # 移除 'b.' 前綴（RFIs API v3 要求純 UUID 格式）
    project_id = _strip_project_id_prefix(project_id)
    
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
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)
    status_filter = request.args.get('filter[status]', '')
    
    params = {
        'limit': min(limit, 200),
        'offset': offset
    }
    
    if status_filter:
        params['filter[status]'] = status_filter
    
    try:
        # 調用 Autodesk Construction Cloud RFIs API
        rfi_types_url = f"{config.AUTODESK_API_BASE}/construction/rfis/v3/projects/{project_id}/rfi-types"
        
        print(f"RFI 類型 API 請求 URL: {rfi_types_url}")
        print(f"RFI 類型 API 請求參數: {params}")
        
        rfi_types_resp = requests.get(rfi_types_url, headers=headers, params=params, timeout=30)
        
        print(f"RFI 類型 API 響應狀態碼: {rfi_types_resp.status_code}")
        
        if rfi_types_resp.status_code != 200:
            error_text = rfi_types_resp.text
            print(f"RFI 類型 API 錯誤響應: {error_text}")
            raise Exception(f"獲取 RFI 類型失敗: {rfi_types_resp.status_code} - {error_text}")
        
        try:
            rfi_types_data = rfi_types_resp.json()
            print(f"RFI 類型 API 響應數據: {rfi_types_data}")
        except json.JSONDecodeError as e:
            print(f"JSON 解析錯誤: {e}")
            raise Exception(f"API 響應數據格式錯誤: {str(e)}")
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "query_params": params,
            "rfi_types": rfi_types_data,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"獲取 RFI 類型時出錯: {str(e)}")
        return jsonify({
            "error": f"獲取 RFI 類型失敗: {str(e)}",
            "status": "error"
        }), 500


@rfis_bp.route('/api/rfis/jarvis/rfi-types')
def get_jarvis_rfi_types():
    """獲取指定項目的 RFI 類型配置（簡化路由）"""
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 參數",
            "message": "請在請求中提供 projectId 參數",
            "status": "error"
        }), 400
    
    return get_rfi_types(project_id)


@rfis_bp.route('/api/rfis/<project_id>/attributes')
def get_rfi_custom_attributes(project_id):
    """獲取項目的 RFI 自定義屬性定義"""
    # 移除 'b.' 前綴（RFIs API v3 要求純 UUID 格式）
    project_id = _strip_project_id_prefix(project_id)
    
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
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)
    status_filter = request.args.get('filter[status]', '')
    
    params = {
        'limit': min(limit, 200),
        'offset': offset
    }
    
    if status_filter:
        params['filter[status]'] = status_filter
    
    try:
        # 調用 Autodesk Construction Cloud RFIs API
        attributes_url = f"{config.AUTODESK_API_BASE}/construction/rfis/v3/projects/{project_id}/attributes"
        
        print(f"RFI 自定義屬性 API 請求 URL: {attributes_url}")
        print(f"RFI 自定義屬性 API 請求參數: {params}")
        
        attributes_resp = requests.get(attributes_url, headers=headers, params=params, timeout=30)
        
        print(f"RFI 自定義屬性 API 響應狀態碼: {attributes_resp.status_code}")
        
        if attributes_resp.status_code != 200:
            error_text = attributes_resp.text
            print(f"RFI 自定義屬性 API 錯誤響應: {error_text}")
            raise Exception(f"獲取自定義屬性失敗: {attributes_resp.status_code} - {error_text}")
        
        try:
            attributes_data = attributes_resp.json()
            print(f"RFI 自定義屬性 API 響應數據: {attributes_data}")
        except json.JSONDecodeError as e:
            print(f"JSON 解析錯誤: {e}")
            raise Exception(f"API 響應數據格式錯誤: {str(e)}")
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "query_params": params,
            "custom_attributes": attributes_data,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"獲取 RFI 自定義屬性時出錯: {str(e)}")
        return jsonify({
            "error": f"獲取 RFI 自定義屬性失敗: {str(e)}",
            "status": "error"
        }), 500


@rfis_bp.route('/api/rfis/jarvis/attributes')
def get_jarvis_rfi_custom_attributes():
    """獲取指定項目的 RFI 自定義屬性定義（簡化路由）"""
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 參數",
            "message": "請在請求中提供 projectId 參數",
            "status": "error"
        }), 400
    
    return get_rfi_custom_attributes(project_id)


@rfis_bp.route('/api/rfis/<project_id>/custom-identifier')
def get_rfi_custom_identifier(project_id):
    """獲取項目的下一個可用 RFI 自定義標識符"""
    # 移除 'b.' 前綴（RFIs API v3 要求純 UUID 格式）
    project_id = _strip_project_id_prefix(project_id)
    
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
        # 調用 Autodesk Construction Cloud RFIs API
        custom_id_url = f"{config.AUTODESK_API_BASE}/construction/rfis/v3/projects/{project_id}/rfis/custom-identifier"
        
        print(f"RFI 自定義標識符 API 請求 URL: {custom_id_url}")
        
        custom_id_resp = requests.get(custom_id_url, headers=headers, timeout=30)
        
        print(f"RFI 自定義標識符 API 響應狀態碼: {custom_id_resp.status_code}")
        
        if custom_id_resp.status_code != 200:
            error_text = custom_id_resp.text
            print(f"RFI 自定義標識符 API 錯誤響應: {error_text}")
            raise Exception(f"獲取自定義標識符失敗: {custom_id_resp.status_code} - {error_text}")
        
        try:
            custom_id_data = custom_id_resp.json()
            print(f"RFI 自定義標識符 API 響應數據: {custom_id_data}")
        except json.JSONDecodeError as e:
            print(f"JSON 解析錯誤: {e}")
            raise Exception(f"API 響應數據格式錯誤: {str(e)}")
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "custom_identifier": custom_id_data,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"獲取 RFI 自定義標識符時出錯: {str(e)}")
        return jsonify({
            "error": f"獲取 RFI 自定義標識符失敗: {str(e)}",
            "status": "error"
        }), 500


@rfis_bp.route('/api/rfis/jarvis/custom-identifier')
def get_jarvis_rfi_custom_identifier():
    """獲取指定項目的下一個可用 RFI 自定義標識符（簡化路由）"""
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 參數",
            "message": "請在請求中提供 projectId 參數",
            "status": "error"
        }), 400
    
    return get_rfi_custom_identifier(project_id)


@rfis_bp.route('/api/rfis/<project_id>/workflow')
def get_rfi_workflow(project_id):
    """獲取項目的 RFI 工作流配置"""
    # 移除 'b.' 前綴（RFIs API v3 要求純 UUID 格式）
    project_id = _strip_project_id_prefix(project_id)
    
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
        # 調用 Autodesk Construction Cloud RFIs API
        workflow_url = f"{config.AUTODESK_API_BASE}/construction/rfis/v3/projects/{project_id}/workflow"
        
        print(f"RFI 工作流 API 請求 URL: {workflow_url}")
        
        workflow_resp = requests.get(workflow_url, headers=headers, timeout=30)
        
        print(f"RFI 工作流 API 響應狀態碼: {workflow_resp.status_code}")
        
        if workflow_resp.status_code != 200:
            error_text = workflow_resp.text
            print(f"RFI 工作流 API 錯誤響應: {error_text}")
            raise Exception(f"獲取工作流配置失敗: {workflow_resp.status_code} - {error_text}")
        
        try:
            workflow_data = workflow_resp.json()
            print(f"RFI 工作流 API 響應數據: {workflow_data}")
        except json.JSONDecodeError as e:
            print(f"JSON 解析錯誤: {e}")
            raise Exception(f"API 響應數據格式錯誤: {str(e)}")
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "workflow": workflow_data,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"獲取 RFI 工作流時出錯: {str(e)}")
        return jsonify({
            "error": f"獲取 RFI 工作流失敗: {str(e)}",
            "status": "error"
        }), 500


@rfis_bp.route('/api/rfis/jarvis/workflow')
def get_jarvis_rfi_workflow():
    """獲取指定項目的 RFI 工作流配置（簡化路由）"""
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 參數",
            "message": "請在請求中提供 projectId 參數",
            "status": "error"
        }), 400
    
    return get_rfi_workflow(project_id)


# ==================== RFI 調試和測試接口 ====================

@rfis_bp.route('/api/rfis/debug/test-connection')
def test_rfi_api_connection():
    """測試 RFI API 連接和認證"""
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 參數",
            "message": "請在請求中提供 projectId 參數",
            "status": "error"
        }), 400
    
    # 移除 'b.' 前綴
    original_project_id = project_id
    project_id = _strip_project_id_prefix(project_id)
    
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
    
    test_results = {
        "project_id_original": original_project_id,
        "project_id_processed": project_id,
        "access_token_available": bool(access_token),
        "access_token_length": len(access_token) if access_token else 0,
        "tests": []
    }
    
    # 測試1: 用戶權限
    try:
        users_me_url = f"{config.AUTODESK_API_BASE}/construction/rfis/v3/projects/{project_id}/users/me"
        print(f"🧪 測試用戶權限: {users_me_url}")
        
        users_resp = requests.get(users_me_url, headers=headers, timeout=15)
        test_results["tests"].append({
            "test": "user_permissions",
            "url": users_me_url,
            "status_code": users_resp.status_code,
            "success": users_resp.status_code == 200,
            "response": users_resp.text[:500] if users_resp.text else None
        })
    except Exception as e:
        test_results["tests"].append({
            "test": "user_permissions",
            "success": False,
            "error": str(e)
        })
    
    # 測試2: RFI類型
    try:
        rfi_types_url = f"{config.AUTODESK_API_BASE}/construction/rfis/v3/projects/{project_id}/rfi-types"
        print(f"🧪 測試RFI類型: {rfi_types_url}")
        
        types_resp = requests.get(rfi_types_url, headers=headers, timeout=15)
        test_results["tests"].append({
            "test": "rfi_types",
            "url": rfi_types_url,
            "status_code": types_resp.status_code,
            "success": types_resp.status_code == 200,
            "response": types_resp.text[:500] if types_resp.text else None
        })
    except Exception as e:
        test_results["tests"].append({
            "test": "rfi_types",
            "success": False,
            "error": str(e)
        })
    
    # 測試3: 簡單搜索
    try:
        search_url = f"{config.AUTODESK_API_BASE}/construction/rfis/v3/projects/{project_id}/search:rfis"
        simple_payload = {
            "limit": 1,
            "offset": 0,
            "filter": {}
        }
        print(f"🧪 測試簡單搜索: {search_url}")
        print(f"🧪 搜索payload: {json.dumps(simple_payload, indent=2)}")
        
        search_resp = requests.post(search_url, headers=headers, json=simple_payload, timeout=15)
        test_results["tests"].append({
            "test": "simple_search",
            "url": search_url,
            "payload": simple_payload,
            "status_code": search_resp.status_code,
            "success": search_resp.status_code == 200,
            "response": search_resp.text[:1000] if search_resp.text else None
        })
    except Exception as e:
        test_results["tests"].append({
            "test": "simple_search",
            "success": False,
            "error": str(e)
        })
    
    # 統計測試結果
    successful_tests = sum(1 for test in test_results["tests"] if test.get("success"))
    total_tests = len(test_results["tests"])
    
    test_results["summary"] = {
        "total_tests": total_tests,
        "successful_tests": successful_tests,
        "failed_tests": total_tests - successful_tests,
        "success_rate": round((successful_tests / total_tests) * 100, 1) if total_tests > 0 else 0
    }
    
    return jsonify({
        "success": True,
        "message": "RFI API 連接測試完成",
        "test_results": test_results,
        "timestamp": datetime.now().isoformat()
    })


# ==================== RFI 参照相关接口 ====================

@rfis_bp.route('/api/rfis/<project_id>/<rfi_id>/references')
def get_rfi_references(project_id, rfi_id):
    """获取RFI的参照列表（调用通用Relations API）"""
    # 移除 'b.' 前綴（RFIs API v3 要求純 UUID 格式）
    project_id = _strip_project_id_prefix(project_id)
    
    if not RELATIONS_API_AVAILABLE:
        return jsonify({
            "success": False,
            "error": "Relations API 不可用",
            "message": "请确保已正确安装和配置 Data Management Relations API",
            "timestamp": datetime.now().isoformat()
        }), 503
    
    try:
        # 获取查询参数
        reference_types = request.args.get('types', '').split(',') if request.args.get('types') else None
        if reference_types:
            reference_types = [rt.strip() for rt in reference_types if rt.strip()]
        
        # 调用Relations API
        relations_manager = RelationsManager()
        references = relations_manager.get_entity_references('rfi', rfi_id, project_id, reference_types)
        
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
            target = ref.get('target', {})
            file_type = target.get('file_type', '')
            if file_type:
                stats['file_type_counts'][file_type] = stats['file_type_counts'].get(file_type, 0) + 1
            
            # 统计文件大小
            file_size = target.get('file_size', 0)
            if isinstance(file_size, (int, float)):
                stats['total_file_size'] += file_size
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "rfi_id": rfi_id,
            "reference_types": reference_types,
            "stats": stats,
            "references": references,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"获取RFI参照时出错: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"获取RFI参照失败: {str(e)}",
            "project_id": project_id,
            "rfi_id": rfi_id,
            "timestamp": datetime.now().isoformat()
        }), 500


@rfis_bp.route('/api/rfis/jarvis/<rfi_id>/references')
def get_jarvis_rfi_references(rfi_id):
    """获取指定项目中指定 RFI 的参照（简化路由）"""
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 参数",
            "message": "请在请求中提供 projectId 参数",
            "status": "error"
        }), 400
    
    return get_rfi_references(project_id, rfi_id)


@rfis_bp.route('/api/rfis/<project_id>/references/batch', methods=['POST'])
def get_rfis_references_batch(project_id):
    """批量获取多个RFI的参照"""
    # 移除 'b.' 前綴（RFIs API v3 要求純 UUID 格式）
    project_id = _strip_project_id_prefix(project_id)
    
    if not RELATIONS_API_AVAILABLE:
        return jsonify({
            "success": False,
            "error": "Relations API 不可用",
            "timestamp": datetime.now().isoformat()
        }), 503
    
    try:
        # 获取请求数据
        request_data = request.get_json() or {}
        rfi_ids = request_data.get('rfi_ids', [])
        reference_types = request_data.get('reference_types')
        
        if not rfi_ids:
            return jsonify({
                "success": False,
                "error": "请求体中缺少rfi_ids数组",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        # 限制批量请求数量
        if len(rfi_ids) > 20:
            return jsonify({
                "success": False,
                "error": "批量请求数量不能超过20个RFI",
                "timestamp": datetime.now().isoformat()
            }), 400
        
        # 构建批量请求
        batch_requests = []
        for rfi_id in rfi_ids:
            batch_requests.append({
                "entity_type": "rfi",
                "entity_id": rfi_id,
                "project_id": project_id,
                "reference_types": reference_types
            })
        
        # 调用Relations API的批量接口
        relations_manager = RelationsManager()
        results = []
        
        # 使用线程池并行处理
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_rfi = {}
            
            for rfi_id in rfi_ids:
                future = executor.submit(
                    relations_manager.get_entity_references,
                    'rfi', rfi_id, project_id, reference_types
                )
                future_to_rfi[future] = rfi_id
            
            # 收集结果
            for future in as_completed(future_to_rfi):
                rfi_id = future_to_rfi[future]
                try:
                    references = future.result()
                    results.append({
                        "success": True,
                        "rfi_id": rfi_id,
                        "references": references,
                        "reference_count": len(references)
                    })
                except Exception as e:
                    results.append({
                        "success": False,
                        "rfi_id": rfi_id,
                        "error": str(e)
                    })
        
        # 整体统计
        total_references = sum(r.get('reference_count', 0) for r in results if r.get('success'))
        successful_requests = sum(1 for r in results if r.get('success'))
        failed_requests = len(results) - successful_requests
        
        return jsonify({
            "success": True,
            "project_id": project_id,
            "batch_stats": {
                "total_rfis": len(rfi_ids),
                "successful_requests": successful_requests,
                "failed_requests": failed_requests,
                "total_references": total_references
            },
            "results": results,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"批量获取RFI参照时出错: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"批量获取RFI参照失败: {str(e)}",
            "project_id": project_id,
            "timestamp": datetime.now().isoformat()
        }), 500


@rfis_bp.route('/api/rfis/jarvis/references/batch', methods=['POST'])
def get_jarvis_rfis_references_batch():
    """批量获取指定项目中多个RFI的参照（简化路由）"""
    project_id = request.args.get('projectId')
    
    if not project_id:
        return jsonify({
            "error": "缺少必需的 projectId 参数",
            "message": "请在请求中提供 projectId 参数",
            "status": "error"
        }), 400
    
    return get_rfis_references_batch(project_id)
