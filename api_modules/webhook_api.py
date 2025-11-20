# -*- coding: utf-8 -*-
"""
Webhook API 模块
处理 Autodesk Platform Services 的事件通知
"""

import requests
import json
import hmac
import hashlib
import logging
from datetime import datetime
from flask import Blueprint, request, jsonify
import config
import utils

webhook_bp = Blueprint('webhook', __name__)

# 配置 Webhook 日志
webhook_logger = logging.getLogger('webhook')
webhook_logger.setLevel(logging.INFO)

# Webhook 配置
WEBHOOK_SECRET = "acc-sync-webhook-secret-2024"  # 生产环境中应该使用环境变量
AUTODESK_WEBHOOK_IPS = [
    '52.41.51.138',
    '34.218.156.43',
    '54.148.84.38',
    '52.89.19.129',
    # Autodesk webhook IP 地址
]

@webhook_bp.route('/api/webhook/autodesk', methods=['POST'])
def handle_autodesk_webhook():
    """处理 Autodesk Webhook 通知"""
    webhook_logger.info(f"收到 Webhook 请求: {request.remote_addr}")
    
    try:
        # 1. 验证请求来源IP（可选）
        if not verify_webhook_ip():
            webhook_logger.warning(f"未授权的IP地址: {request.remote_addr}")
            # 在开发环境中可以注释掉这个检查
            # return jsonify({'error': 'Unauthorized IP'}), 403
        
        # 2. 验证请求签名（可选，如果Autodesk支持）
        signature = request.headers.get('X-Adsk-Signature')
        if signature and not verify_signature(request.data, signature):
            webhook_logger.warning("Webhook 签名验证失败")
            return jsonify({'error': 'Invalid signature'}), 401
        
        # 3. 解析事件数据
        event_data = request.json
        if not event_data:
            webhook_logger.error("空的事件数据")
            return jsonify({'error': 'Empty event data'}), 400
        
        webhook_logger.info(f"事件数据: {json.dumps(event_data, indent=2)}")
        
        # 4. 处理事件
        result = process_webhook_event(event_data)
        
        if result:
            webhook_logger.info("Webhook 处理成功")
            return jsonify({'status': 'success', 'message': 'Event processed'}), 200
        else:
            webhook_logger.error("Webhook 处理失败")
            return jsonify({'status': 'error', 'message': 'Event processing failed'}), 500
            
    except Exception as e:
        webhook_logger.error(f"Webhook 处理异常: {str(e)}")
        return jsonify({'error': str(e)}), 500

def verify_webhook_ip():
    """验证请求来源 IP"""
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    if client_ip:
        # 处理多个IP的情况（负载均衡）
        client_ip = client_ip.split(',')[0].strip()
    
    # 在开发环境中允许本地IP
    if client_ip in ['127.0.0.1', 'localhost', '::1']:
        return True
    
    return client_ip in AUTODESK_WEBHOOK_IPS

def verify_signature(payload, signature):
    """验证 Webhook 签名"""
    if not signature:
        return True  # 如果没有签名，跳过验证
    
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    # 支持不同的签名格式
    if signature.startswith('sha256='):
        signature = signature[7:]
    
    return hmac.compare_digest(signature, expected_signature)

def process_webhook_event(event_data):
    """处理 Webhook 事件"""
    event_type = event_data.get('eventType')
    resource_urn = event_data.get('resourceUrn')
    project_id = event_data.get('projectId')
    
    webhook_logger.info(f"处理事件: {event_type}, 资源: {resource_urn}, 项目: {project_id}")
    
    try:
        if event_type == 'dm.version.added':
            return handle_file_added(event_data)
        elif event_type == 'dm.version.modified':
            return handle_file_modified(event_data)
        elif event_type == 'dm.version.deleted':
            return handle_file_deleted(event_data)
        elif event_type == 'dm.folder.added':
            return handle_folder_added(event_data)
        elif event_type == 'dm.folder.modified':
            return handle_folder_modified(event_data)
        elif event_type == 'dm.folder.deleted':
            return handle_folder_deleted(event_data)
        else:
            webhook_logger.warning(f"未知事件类型: {event_type}")
            return True  # 返回成功，避免重复发送
            
    except Exception as e:
        webhook_logger.error(f"事件处理异常: {str(e)}")
        return False

def handle_file_added(event_data):
    """处理文件添加事件"""
    webhook_logger.info("处理文件添加事件")
    
    resource_urn = event_data.get('resourceUrn')
    project_id = event_data.get('projectId')
    
    # 触发增量同步
    try:
        sync_result = trigger_incremental_sync(project_id, resource_urn)
        webhook_logger.info(f"文件添加同步完成: {sync_result}")
        return True
    except Exception as e:
        webhook_logger.error(f"文件添加同步失败: {str(e)}")
        return False

def handle_file_modified(event_data):
    """处理文件修改事件"""
    webhook_logger.info("处理文件修改事件")
    
    resource_urn = event_data.get('resourceUrn')
    project_id = event_data.get('projectId')
    
    # 触发文件更新
    try:
        update_result = trigger_file_update(project_id, resource_urn)
        webhook_logger.info(f"文件修改同步完成: {update_result}")
        return True
    except Exception as e:
        webhook_logger.error(f"文件修改同步失败: {str(e)}")
        return False

def handle_file_deleted(event_data):
    """处理文件删除事件"""
    webhook_logger.info("处理文件删除事件")
    
    resource_urn = event_data.get('resourceUrn')
    project_id = event_data.get('projectId')
    
    # 触发文件删除
    try:
        delete_result = trigger_file_deletion(project_id, resource_urn)
        webhook_logger.info(f"文件删除处理完成: {delete_result}")
        return True
    except Exception as e:
        webhook_logger.error(f"文件删除处理失败: {str(e)}")
        return False

def handle_folder_added(event_data):
    """处理文件夹添加事件"""
    webhook_logger.info("处理文件夹添加事件")
    
    resource_urn = event_data.get('resourceUrn')
    project_id = event_data.get('projectId')
    
    # 触发文件夹同步
    try:
        sync_result = trigger_folder_sync(project_id, resource_urn)
        webhook_logger.info(f"文件夹添加同步完成: {sync_result}")
        return True
    except Exception as e:
        webhook_logger.error(f"文件夹添加同步失败: {str(e)}")
        return False

def handle_folder_modified(event_data):
    """处理文件夹修改事件"""
    webhook_logger.info("处理文件夹修改事件")
    return True  # 文件夹修改通常不需要特殊处理

def handle_folder_deleted(event_data):
    """处理文件夹删除事件"""
    webhook_logger.info("处理文件夹删除事件")
    
    resource_urn = event_data.get('resourceUrn')
    project_id = event_data.get('projectId')
    
    # 触发文件夹删除处理
    try:
        delete_result = trigger_folder_deletion(project_id, resource_urn)
        webhook_logger.info(f"文件夹删除处理完成: {delete_result}")
        return True
    except Exception as e:
        webhook_logger.error(f"文件夹删除处理失败: {str(e)}")
        return False

def trigger_incremental_sync(project_id, item_id):
    """触发增量同步"""
    webhook_logger.info(f"触发增量同步: 项目 {project_id}, 文件 {item_id}")
    
    # 这里可以调用现有的同步逻辑
    # 例如：重新扫描特定文件或文件夹
    
    try:
        # 调用文件树API来获取最新信息
        sync_url = f"http://localhost:{config.PORT}/api/file-sync/project/{project_id}/tree"
        params = {'maxDepth': 2, 'includeVersions': 'true'}
        
        response = requests.get(sync_url, params=params, timeout=60)
        
        if response.status_code == 200:
            webhook_logger.info("增量同步成功")
            return "sync_completed"
        else:
            webhook_logger.error(f"增量同步失败: {response.status_code}")
            return "sync_failed"
            
    except Exception as e:
        webhook_logger.error(f"增量同步异常: {str(e)}")
        return "sync_error"

def trigger_file_update(project_id, item_id):
    """触发文件更新"""
    webhook_logger.info(f"触发文件更新: 项目 {project_id}, 文件 {item_id}")
    
    # 可以在这里实现文件更新逻辑
    # 例如：重新下载文件，更新本地缓存等
    
    return "update_completed"

def trigger_file_deletion(project_id, item_id):
    """触发文件删除处理"""
    webhook_logger.info(f"触发文件删除: 项目 {project_id}, 文件 {item_id}")
    
    # 可以在这里实现文件删除逻辑
    # 例如：从本地缓存中删除文件记录
    
    return "deletion_completed"

def trigger_folder_sync(project_id, folder_id):
    """触发文件夹同步"""
    webhook_logger.info(f"触发文件夹同步: 项目 {project_id}, 文件夹 {folder_id}")
    
    # 可以在这里实现文件夹同步逻辑
    
    return "folder_sync_completed"

def trigger_folder_deletion(project_id, folder_id):
    """触发文件夹删除处理"""
    webhook_logger.info(f"触发文件夹删除: 项目 {project_id}, 文件夹 {folder_id}")
    
    # 可以在这里实现文件夹删除逻辑
    
    return "folder_deletion_completed"

@webhook_bp.route('/api/webhook/register', methods=['POST'])
def register_webhook():
    """注册 Webhook 端点"""
    access_token = utils.get_access_token()
    if not access_token:
        return jsonify({
            "error": "未找到 Access Token，请先进行认证",
            "status": "unauthorized"
        }), 401
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # 从请求中获取参数
    request_data = request.json or {}
    callback_url = request_data.get('callbackUrl', 'https://your-domain.com/api/webhook/autodesk')
    project_id = request_data.get('projectId', config.DEFAULT_PROJECT_ID)
    
    # 获取项目的Hub ID
    try:
        hubs_resp = requests.get(f"{config.AUTODESK_API_BASE}/project/v1/hubs", headers=headers)
        if hubs_resp.status_code != 200:
            return jsonify({
                "error": f"无法获取Hub信息: {hubs_resp.status_code}",
                "status": "error"
            }), 400
        
        hubs_data = hubs_resp.json()
        hub_id = None
        for hub in hubs_data.get('data', []):
            hub_id = hub.get('id')
            break
        
        if not hub_id:
            return jsonify({
                "error": "未找到有效的Hub ID",
                "status": "error"
            }), 400
        
        # 构建 Webhook 注册数据
        webhook_data = {
            "callbackUrl": callback_url,
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.4hSb5AaQSnuUmrJBJX2eyw"  # 项目根文件夹
            },
            "hookAttribute": {
                "projectId": project_id,
                "hubId": hub_id
            },
            "autoReactivateHook": True,
            "hookExpiry": "2025-12-31T23:59:59.000Z"
        }
        
        # 注册 Webhook
        webhook_url = f"{config.AUTODESK_API_BASE}/webhooks/v1/hooks/event"
        
        response = requests.post(webhook_url, headers=headers, json=webhook_data)
        
        if response.status_code == 201:
            hook_data = response.json()
            webhook_logger.info(f"Webhook 注册成功: {hook_data}")
            
            return jsonify({
                "status": "success",
                "message": "Webhook 注册成功",
                "hook_id": hook_data.get('hookId'),
                "callback_url": callback_url,
                "data": hook_data
            })
        else:
            webhook_logger.error(f"Webhook 注册失败: {response.status_code} - {response.text}")
            return jsonify({
                "error": f"Webhook 注册失败: {response.status_code}",
                "status": "error",
                "details": response.text
            }), 400
            
    except Exception as e:
        webhook_logger.error(f"Webhook 注册异常: {str(e)}")
        return jsonify({
            "error": f"Webhook 注册失败: {str(e)}",
            "status": "error"
        }), 500

@webhook_bp.route('/api/webhook/list', methods=['GET'])
def list_webhooks():
    """列出已注册的 Webhook"""
    access_token = utils.get_access_token()
    if not access_token:
        return jsonify({
            "error": "未找到 Access Token，请先进行认证",
            "status": "unauthorized"
        }), 401
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    try:
        webhook_url = f"{config.AUTODESK_API_BASE}/webhooks/v1/hooks"
        response = requests.get(webhook_url, headers=headers)
        
        if response.status_code == 200:
            hooks_data = response.json()
            return jsonify({
                "status": "success",
                "hooks": hooks_data
            })
        else:
            return jsonify({
                "error": f"获取 Webhook 列表失败: {response.status_code}",
                "status": "error",
                "details": response.text
            }), 400
            
    except Exception as e:
        return jsonify({
            "error": f"获取 Webhook 列表失败: {str(e)}",
            "status": "error"
        }), 500

@webhook_bp.route('/api/webhook/test', methods=['POST'])
def test_webhook():
    """测试 Webhook 端点"""
    webhook_logger.info("收到 Webhook 测试请求")
    
    # 模拟事件数据
    test_event = {
        "eventType": "dm.version.added",
        "resourceUrn": "urn:adsk.wipprod:dm.lineage:test123",
        "projectId": config.DEFAULT_PROJECT_ID,
        "timestamp": datetime.now().isoformat(),
        "test": True
    }
    
    result = process_webhook_event(test_event)
    
    return jsonify({
        "status": "success" if result else "error",
        "message": "Webhook 测试完成",
        "test_event": test_event,
        "result": result
    })
