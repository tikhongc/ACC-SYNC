# -*- coding: utf-8 -*-
"""
认证相关的 API 模块
处理 OAuth 认证、token 管理等功能
"""

import requests
import json
import time
from datetime import datetime
from flask import Blueprint, request, redirect, jsonify
import config
import utils

auth_bp = Blueprint('auth', __name__)


def get_projects_from_hub(hub_id, headers):
    """
    从指定Hub获取所有项目
    """
    try:
        # 使用正确的API端点获取Hub下的项目
        projects_resp = requests.get(
            f"{config.AUTODESK_API_BASE}/project/v1/hubs/{hub_id}/projects",
            headers=headers,
            timeout=(10, 15)
        )
        
        if projects_resp.status_code == 200:
            projects_data = projects_resp.json()
            print(f"成功获取到 {len(projects_data.get('data', []))} 个项目")
            return projects_data
        else:
            print(f"获取项目失败: HTTP {projects_resp.status_code}")
            print(f"响应内容: {projects_resp.text[:200]}")
            # 返回空的项目数据结构
            return {"data": [], "jsonapi": {"version": "1.0"}}
            
    except Exception as e:
        print(f"获取Hub项目时出错: {str(e)}")
        return {"data": [], "jsonapi": {"version": "1.0"}}


def enhance_project_data(projects_data, headers, hub_id, real_account_id):
    """
    增强项目数据，添加详细的项目信息、状态和权限范围
    """
    if not projects_data or 'data' not in projects_data:
        return projects_data
    
    enhanced_data = projects_data.copy()
    enhanced_projects = []
    
    try:
        # 获取ACC项目详细信息
        acc_projects_resp = requests.get(
            f"{config.AUTODESK_API_BASE}/construction/admin/v1/accounts/{real_account_id}/projects",
            headers=headers,
            timeout=(5, 10)
        )
        
        acc_projects = {}
        if acc_projects_resp.status_code == 200:
            acc_data = acc_projects_resp.json()
            for project in acc_data.get('results', []):
                project_id = project.get('id')
                # 同时存储原始ID和带"b."前缀的ID，以确保能匹配
                acc_projects[project_id] = project
                if not project_id.startswith('b.'):
                    acc_projects[f'b.{project_id}'] = project
                else:
                    # 如果原始ID有"b."前缀，也存储不带前缀的版本
                    acc_projects[project_id[2:]] = project
        
        # 遍历原始项目数据并增强
        for project in projects_data.get('data', []):
            enhanced_project = project.copy()
            project_id = project.get('id', '')
            
            print(f"处理项目: {project_id}, 名称: {project.get('attributes', {}).get('name', 'Unknown')}")
            
            # 确保attributes对象存在
            if 'attributes' not in enhanced_project:
                enhanced_project['attributes'] = {}
            attributes = enhanced_project['attributes']
            
            # 确保基本属性都有默认值
            if 'name' not in attributes or not attributes['name']:
                attributes['name'] = 'Unknown Project'
            
            # 尝试从ACC Admin API获取更详细信息
            if project_id in acc_projects:
                acc_project = acc_projects[project_id]
                
                # 更新状态信息（保留现有值或使用ACC值）
                attributes['status'] = acc_project.get('status', attributes.get('status', 'active'))
                attributes['jobNumber'] = acc_project.get('jobNumber', attributes.get('jobNumber', ''))
                attributes['projectType'] = acc_project.get('type', attributes.get('projectType', ''))
                attributes['startDate'] = acc_project.get('startDate', attributes.get('startDate', ''))
                attributes['endDate'] = acc_project.get('endDate', attributes.get('endDate', ''))
                attributes['currency'] = acc_project.get('currency', attributes.get('currency', ''))
                attributes['timezone'] = acc_project.get('timezone', attributes.get('timezone', ''))
                attributes['language'] = acc_project.get('language', attributes.get('language', ''))
                
                # 添加权限范围信息
                try:
                    attributes['permissions'] = determine_project_permissions(project_id, headers)
                except Exception as perm_error:
                    print(f"权限检查失败: {str(perm_error)}")
                    attributes['permissions'] = {
                        'scope': '基础访问',
                        'level': 'member',
                        'description': '标准项目访问权限'
                    }
            else:
                # 如果无法从ACC API获取信息，确保所有必要属性都有默认值
                attributes['status'] = attributes.get('status', 'active')
                attributes['jobNumber'] = attributes.get('jobNumber', '')
                attributes['projectType'] = attributes.get('projectType', '')
                attributes['startDate'] = attributes.get('startDate', '')
                attributes['endDate'] = attributes.get('endDate', '')
                attributes['currency'] = attributes.get('currency', '')
                attributes['timezone'] = attributes.get('timezone', '')
                attributes['language'] = attributes.get('language', '')
                attributes['permissions'] = {
                    'scope': '基础访问',
                    'level': 'member',
                    'description': '标准项目访问权限'
                }
            
            # 确保permissions对象完整
            if 'permissions' in attributes and attributes['permissions']:
                permissions = attributes['permissions']
                if 'scope' not in permissions:
                    permissions['scope'] = '基础访问'
                if 'level' not in permissions:
                    permissions['level'] = 'member'
                if 'description' not in permissions:
                    permissions['description'] = '标准项目访问权限'
            else:
                attributes['permissions'] = {
                    'scope': '基础访问',
                    'level': 'member',
                    'description': '标准项目访问权限'
                }
            
            enhanced_projects.append(enhanced_project)
        
        enhanced_data['data'] = enhanced_projects
        
    except Exception as e:
        print(f"增强项目数据时出错: {str(e)}")
        # 如果增强失败，确保返回具有完整默认属性的数据
        for project in projects_data.get('data', []):
            if 'attributes' not in project:
                project['attributes'] = {}
            attributes = project['attributes']
            
            # 设置默认值
            if 'name' not in attributes or not attributes['name']:
                attributes['name'] = 'Unknown Project'
            attributes['status'] = attributes.get('status', 'active')
            attributes['jobNumber'] = attributes.get('jobNumber', '')
            attributes['projectType'] = attributes.get('projectType', '')
            attributes['startDate'] = attributes.get('startDate', '')
            attributes['endDate'] = attributes.get('endDate', '')
            attributes['currency'] = attributes.get('currency', '')
            attributes['timezone'] = attributes.get('timezone', '')
            attributes['language'] = attributes.get('language', '')
            attributes['permissions'] = {
                'scope': '基础访问',
                'level': 'member',
                'description': '标准项目访问权限'
            }
        
        return projects_data
    
    return enhanced_data


def determine_project_permissions(project_id, headers):
    """
    确定用户在项目中的权限范围
    """
    try:
        # 尝试访问项目管理端点来判断权限级别
        admin_resp = requests.get(
            f"{config.AUTODESK_API_BASE}/construction/admin/v1/projects/{project_id}",
            headers=headers,
            timeout=(3, 5)
        )
        
        if admin_resp.status_code == 200:
            return {
                'scope': '项目管理',
                'level': 'admin',
                'description': '完整的项目管理权限'
            }
        elif admin_resp.status_code == 403:
            # 尝试数据访问权限
            data_resp = requests.get(
                f"{config.AUTODESK_API_BASE}/project/v1/hubs/{project_id.replace('b.', ':')}/projects",
                headers=headers,
                timeout=(3, 5)
            )
            
            if data_resp.status_code == 200:
                return {
                    'scope': '数据访问',
                    'level': 'member',
                    'description': '项目数据读写权限'
                }
            else:
                return {
                    'scope': '只读访问',
                    'level': 'viewer',
                    'description': '仅查看权限'
                }
        else:
            return {
                'scope': '未知权限',
                'level': 'unknown',
                'description': '权限级别未确定'
            }
            
    except Exception as e:
        print(f"确定项目权限时出错: {str(e)}")
        return {
            'scope': '基础访问',
            'level': 'member',
            'description': '标准项目访问权限'
        }




@auth_bp.route('/api/auth/callback', methods=['POST', 'GET'])
def callback():
    """OAuth 认证回调处理"""
    from flask import session
    
    code = request.args.get('code')
    error = request.args.get('error')
    state = request.args.get('state')
    
    print(f"OAuth callback received - code: {bool(code)}, state: {state}, error: {error}")
    
    # 检查是否有错误
    if error:
        error_description = request.args.get('error_description', 'Unknown error')
        print(f"OAuth error: {error} - {error_description}")
        return f"""
        <html>
        <head><title>认证错误</title></head>
        <body>
            <h1>认证失败</h1>
            <p>错误: {error}</p>
            <p>描述: {error_description}</p>
            <script>
                window.parent.postMessage({{
                    type: 'oauth_error',
                    error: '{error}',
                    error_description: '{error_description}'
                }}, 'http://localhost:3000');
                setTimeout(function() {{
                    window.close();
                }}, 3000);
            </script>
        </body>
        </html>
        """
    
    if not code:
        print("No authorization code received")
        return f"""
        <html>
        <head><title>认证失败</title></head>
        <body>
            <h1>认证失败</h1>
            <p>未收到授权码</p>
            <script>
                window.parent.postMessage({{
                    type: 'oauth_error',
                    error: 'no_code',
                    error_description: '未收到授权码'
                }}, 'http://localhost:3000');
                setTimeout(function() {{
                    window.close();
                }}, 3000);
            </script>
        </body>
        </html>
        """
    
    # 验证state参数（如果设置了的话）
    if state:
        session_state = session.get('oauth_state')
        print(f"State validation - received: {state}, session: {session_state}")
        if not session_state or state != session_state:
            print("State parameter validation failed")
            return f"""
            <html>
            <head><title>认证失败</title></head>
            <body>
                <h1>认证失败</h1>
                <p>状态验证失败，可能的CSRF攻击</p>
                <script>
                    window.parent.postMessage({{
                        type: 'oauth_error',
                        error: 'state_validation_failed',
                        error_description: '状态验证失败，可能的CSRF攻击'
                    }}, 'http://localhost:3000');
                    setTimeout(function() {{
                        window.close();
                    }}, 3000);
                </script>
            </body>
            </html>
            """
        # 清除已使用的state
        session.pop('oauth_state', None)
    
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': config.CLIENT_ID,
        'client_secret': config.CLIENT_SECRET,
        'redirect_uri': config.CALLBACK_URL
    }
    
    token_url = f"{config.AUTODESK_AUTH_URL}/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    try:
        print(f"Requesting token from: {token_url}")
        print(f"Payload: {payload}")
        resp = requests.post(token_url, data=payload, headers=headers)
        
        print(f"Token response status: {resp.status_code}")
        print(f"Token response headers: {resp.headers}")
        print(f"Token response text: {resp.text}")
        
        if resp.status_code != 200:
            print(f"Token request failed: {resp.status_code} - {resp.text}")
            # 创建一个简单的错误页面而不是重定向
            return f"""
            <html>
            <head><title>认证失败</title></head>
            <body>
                <h1>认证失败</h1>
                <p>状态码: {resp.status_code}</p>
                <p>错误信息: {resp.text}</p>
                <script>
                    window.parent.postMessage({{
                        type: 'oauth_error',
                        error: 'token_request_failed',
                        error_description: '状态码: {resp.status_code}, 错误信息: {resp.text}'
                    }}, 'http://localhost:3000');
                    setTimeout(function() {{
                        window.close();
                    }}, 5000);
                </script>
            </body>
            </html>
            """
        
        resp_json = resp.json()
        print(f"Token response JSON: {json.dumps(resp_json, indent=2)}")
        
        # 检查响应是否包含access_token
        if not resp_json.get('access_token'):
            print("No access_token in response")
            return f"""
            <html>
            <head><title>认证失败</title></head>
            <body>
                <h1>认证失败</h1>
                <p>未收到access_token</p>
                <p>响应内容: {json.dumps(resp_json, indent=2)}</p>
                <script>
                    window.parent.postMessage({{
                        type: 'oauth_error',
                        error: 'no_access_token',
                        error_description: '未收到access_token'
                    }}, 'http://localhost:3000');
                    setTimeout(function() {{
                        window.close();
                    }}, 5000);
                </script>
            </body>
            </html>
            """
        
        # 保存 token 到内存和会话（优化版）
        expires_in = resp_json.get('expires_in', 3600)
        
        # 如果Autodesk返回的expires_in较短，尝试请求更长的有效期
        if expires_in < 7200:  # 如果少于2小时，记录但仍然使用
            print(f"⚠️ Token有效期较短: {expires_in}秒 ({expires_in/3600:.1f}小时)")
        
        success = utils.save_tokens(
            access_token=resp_json.get('access_token'),
            refresh_token=resp_json.get('refresh_token'),
            expires_in=expires_in
        )
        
        if success:
            print("Token saved successfully, redirecting to success page")
            # 创建一个简单的成功页面，然后重定向
            return f"""
            <html>
            <head><title>认证成功</title></head>
            <body>
                <h1>认证成功！</h1>
                <p>正在重定向到应用...</p>
                <script>
                    window.parent.postMessage({{
                        type: 'oauth_success',
                        message: '认证成功'
                    }}, 'http://localhost:3000');
                    setTimeout(function() {{
                        window.close();
                        window.location.href = 'http://localhost:3000/#/auth/success';
                    }}, 1000);
                </script>
            </body>
            </html>
            """
        else:
            print("Failed to save token")
            return f"""
            <html>
            <head><title>认证失败</title></head>
            <body>
                <h1>Token保存失败</h1>
                <script>
                    window.parent.postMessage({{
                        type: 'oauth_error',
                        error: 'token_save_failed',
                        error_description: 'Token保存失败'
                    }}, 'http://localhost:3000');
                    setTimeout(function() {{
                        window.close();
                    }}, 3000);
                </script>
            </body>
            </html>
            """
        
    except Exception as e:
        print(f"Exception during token exchange: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"""
        <html>
        <head><title>认证异常</title></head>
        <body>
            <h1>认证过程中发生异常</h1>
            <p>错误: {str(e)}</p>
            <script>
                window.parent.postMessage({{
                    type: 'oauth_error',
                    error: 'exception',
                    error_description: '认证过程中发生异常: {str(e)}'
                }}, 'http://localhost:3000');
                setTimeout(function() {{
                    window.close();
                }}, 5000);
            </script>
        </body>
        </html>
        """


@auth_bp.route('/api/auth/check')
def check_auth():
    """检查用户认证状态，支持自动Token刷新"""
    try:
        print("🔍 Auth check requested")
        
        # 使用get_access_token()，这会自动处理Token刷新
        access_token = utils.get_access_token()
        
        if access_token:
            # 获取Token详细信息
            with utils._token_lock:
                expires_at = utils._token_storage.get('expires_at')
                current_time = time.time()
                expires_in_minutes = int((expires_at - current_time)/60) if expires_at else None
            
            print(f"✅ Valid token found, expires in {expires_in_minutes} minutes")
            return jsonify({
                "authenticated": True,
                "has_token": True,
                "token_preview": access_token[:20] + "..." if access_token else None,
                "message": "用户已认证",
                "expires_in_minutes": expires_in_minutes
            })
        else:
            print("❌ No valid token available")
            return jsonify({
                "authenticated": False,
                "message": "未找到有效的 Access Token，请先进行认证",
                "has_token": False,
                "token_expired": True
            }), 401
                
    except Exception as e:
        print(f"❌ Auth check error: {str(e)}")
        return jsonify({
            "authenticated": False,
            "message": f"认证检查出错: {str(e)}",
            "error": "internal_error"
        }), 500


@auth_bp.route('/api/auth/token-info')
def token_info():
    """获取详细的token信息"""
    try:
        print("🔍 Token info requested")
        
        # 使用utils.get_token_info()获取完整的token信息（包括新的时间字段）
        info = utils.get_token_info()
        
        print(f"📊 Token info: valid={info['is_valid']}, expires_in={info['expires_in_minutes']}min")
        if info.get('next_auto_refresh_in_minutes') is not None:
            print(f"🔄 Next refresh in: {info['next_auto_refresh_in_minutes']}min")
        
        return jsonify({
            "status": "success",
            "token_info": info
        })
            
    except Exception as e:
        print(f"❌ Token info error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"获取token信息出错: {str(e)}",
            "token_info": {
                'has_access_token': False,
                'has_refresh_token': False,
                'is_valid': False
            }
        }), 500


@auth_bp.route('/api/auth/refresh-token', methods=['POST'])
def refresh_token():
    """手动刷新token"""
    try:
        print("🔄 Manual token refresh requested")
        
        # 简化版本，直接执行刷新逻辑
        with utils._token_lock:
            refresh_token_val = utils._token_storage.get('refresh_token')
            
            if not refresh_token_val:
                return jsonify({
                    "status": "error",
                    "message": "没有可用的refresh token"
                }), 400
            
            # 执行token刷新
            try:
                refresh_data = {
                    'grant_type': 'refresh_token',
                    'refresh_token': refresh_token_val,
                    'client_id': config.CLIENT_ID,
                    'client_secret': config.CLIENT_SECRET,
                }
                
                response = requests.post(
                    f"{config.AUTODESK_AUTH_URL}/token",
                    data=refresh_data,
                    timeout=10
                )
                
                if response.status_code == 200:
                    token_data = response.json()
                    
                    # 保存新的token
                    current_time = time.time()
                    expires_at = current_time + token_data.get('expires_in', 3600)
                    
                    utils._token_storage.update({
                        'access_token': token_data.get('access_token'),
                        'refresh_token': token_data.get('refresh_token', refresh_token_val),
                        'expires_at': expires_at,
                        'updated_at': current_time,
                        'refresh_attempts': 0
                    })
                    
                    print("✅ Token refreshed successfully")
                    
                    return jsonify({
                        "status": "success",
                        "message": "Token刷新成功",
                        "token_info": {
                            'has_access_token': True,
                            'has_refresh_token': True,
                            'is_valid': True,
                            'expires_in_minutes': int(token_data.get('expires_in', 3600) / 60),
                            'expires_at': datetime.fromtimestamp(expires_at).isoformat()
                        }
                    })
                else:
                    error_msg = f"刷新失败: HTTP {response.status_code} - {response.text[:200]}"
                    print(f"❌ {error_msg}")
                    return jsonify({
                        "status": "error",
                        "message": error_msg
                    }), 400
                    
            except requests.RequestException as e:
                error_msg = f"网络请求失败: {str(e)}"
                print(f"❌ {error_msg}")
                return jsonify({
                    "status": "error",
                    "message": error_msg
                }), 500
            
    except Exception as e:
        print(f"❌ Token refresh error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"刷新token时发生错误: {str(e)}"
        }), 500


@auth_bp.route('/api/auth/logout', methods=['POST'])
def logout():
    """用户登出，清除所有token"""
    try:
        utils.clear_tokens()
        return jsonify({
            "status": "success",
            "message": "已成功登出，所有token已清除"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"登出时发生错误: {str(e)}"
        }), 500


@auth_bp.route('/api/auth/account-info')
def account_info():
    """获取用户账户信息"""
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
        # 获取用户信息
        user_resp = requests.get(f"{config.AUTODESK_API_BASE}/userprofile/v1/users/@me", headers=headers)
        
        if user_resp.status_code != 200:
            raise Exception(f"获取用户信息失败: {user_resp.status_code}")
        
        user_data = user_resp.json()
        
        # 获取Hub信息
        hubs_resp = requests.get(f"{config.AUTODESK_API_BASE}/project/v1/hubs", headers=headers)
        hubs_data = hubs_resp.json() if hubs_resp.status_code == 200 else {}
        
        hub_id, real_account_id, hub_name = utils.get_real_account_id(hubs_data)
        
        # 获取Hub下的所有项目
        projects_data = get_projects_from_hub(hub_id, headers)
        
        # 获取详细的项目信息，包括状态和权限
        enhanced_projects = enhance_project_data(projects_data, headers, hub_id, real_account_id)
        
        return jsonify({
            "status": "success",
            "user": user_data,
            "projects": enhanced_projects,
            "hub": {
                "hubId": hub_id,
                "hubName": hub_name,
                "realAccountId": real_account_id
            }
        })
        
    except Exception as e:
        return jsonify({
            "error": f"获取账户信息时发生错误: {str(e)}",
            "status": "error"
        }), 500



@auth_bp.route('/api/auth/projects')
def get_projects():
    """通用的项目信息获取API - 统一数据源"""
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
        print(f"🚀 开始获取项目信息，使用access_token: {access_token[:20]}...")
        
        # 获取Hub信息
        hubs_resp = requests.get(f"{config.AUTODESK_API_BASE}/project/v1/hubs", headers=headers)
        print(f"📊 Hub API响应状态: {hubs_resp.status_code}")
        
        if hubs_resp.status_code != 200:
            print(f"❌ Hub API响应内容: {hubs_resp.text}")
            raise Exception(f"获取Hub失败: {hubs_resp.status_code} - {hubs_resp.text}")
            
        hubs_data = hubs_resp.json()
        print(f"📋 获取到Hub数据: {len(hubs_data.get('data', []))} 个Hub")
        
        hub_id, real_account_id, hub_name = utils.get_real_account_id(hubs_data)
        print(f"🏢 使用Hub: {hub_name} (ID: {hub_id}, Account: {real_account_id})")
        
        # 获取Hub下的所有项目
        projects_data = get_projects_from_hub(hub_id, headers)
        print(f"📁 原始项目数据: {len(projects_data.get('data', []))} 个项目")
        
        # 获取详细的项目信息，包括状态和权限
        enhanced_projects = enhance_project_data(projects_data, headers, hub_id, real_account_id)
        print(f"✨ 增强后项目数据: {len(enhanced_projects.get('data', []))} 个项目")
        
        # 转换为ProjectSelector需要的格式
        project_list = []
        if enhanced_projects and 'data' in enhanced_projects:
            for project in enhanced_projects['data']:
                # 获取项目属性
                attributes = project.get('attributes', {})
                permissions = attributes.get('permissions', {
                    'scope': '基础访问',
                    'level': 'member',
                    'description': '标准项目访问权限'
                })
                
                print(f"🔄 转换项目: {attributes.get('name', 'Unknown')} - 权限: {permissions}")
                
                project_info = {
                    'id': project.get('id'),
                    'name': attributes.get('name', 'Unknown'),
                    'type': attributes.get('projectType', ''),
                    'status': attributes.get('status', 'active'),
                    'isActive': attributes.get('status', 'active') == 'active',
                    'attributes': {
                        'name': attributes.get('name', 'Unknown'),
                        'projectType': attributes.get('projectType', ''),
                        'status': attributes.get('status', 'active'),
                        'permissions': permissions
                    }
                }
                project_list.append(project_info)
        
        print(f"📤 最终返回项目列表: {len(project_list)} 个项目")
        
        # 准备返回给前端的完整数据，包含时间戳用于缓存管理
        response_data = {
            "status": "success",
            "projects": {
                "list": project_list,
                "total": len(project_list)
            },
            "hub": {
                "hubId": hub_id,
                "hubName": hub_name,
                "realAccountId": real_account_id
            },
            "cache_info": {
                "timestamp": int(time.time()),
                "expires_in_hours": 24  # 缓存24小时
            }
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"获取项目信息时出错: {str(e)}")
        return jsonify({
            "error": f"获取项目信息时发生错误: {str(e)}",
            "status": "error"
        }), 500


@auth_bp.route('/api/auth/debug-projects')
def debug_projects():
    """调试项目获取功能"""
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
    
    debug_info = {}
    
    try:
        # 1. 获取Hubs
        hubs_resp = requests.get(f"{config.AUTODESK_API_BASE}/project/v1/hubs", headers=headers)
        debug_info["hubs_api"] = {
            "status_code": hubs_resp.status_code,
            "url": f"{config.AUTODESK_API_BASE}/project/v1/hubs"
        }
        
        if hubs_resp.status_code == 200:
            hubs_data = hubs_resp.json()
            debug_info["hubs_found"] = len(hubs_data.get('data', []))
            
            # 获取第一个Hub的信息
            if hubs_data.get('data'):
                first_hub = hubs_data['data'][0]
                hub_id = first_hub.get('id')
                hub_name = first_hub.get('attributes', {}).get('name')
                
                debug_info["first_hub"] = {
                    "id": hub_id,
                    "name": hub_name
                }
                
                # 2. 获取Hub下的项目
                projects_resp = requests.get(
                    f"{config.AUTODESK_API_BASE}/project/v1/hubs/{hub_id}/projects",
                    headers=headers
                )
                
                debug_info["projects_api"] = {
                    "status_code": projects_resp.status_code,
                    "url": f"{config.AUTODESK_API_BASE}/project/v1/hubs/{hub_id}/projects"
                }
                
                if projects_resp.status_code == 200:
                    projects_data = projects_resp.json()
                    debug_info["projects_found"] = len(projects_data.get('data', []))
                    debug_info["projects_list"] = []
                    
                    for project in projects_data.get('data', []):
                        project_info = {
                            "id": project.get('id'),
                            "name": project.get('attributes', {}).get('name'),
                            "status": project.get('attributes', {}).get('status'),
                            "type": project.get('type')
                        }
                        debug_info["projects_list"].append(project_info)
                else:
                    debug_info["projects_api"]["error"] = projects_resp.text[:300]
        else:
            debug_info["hubs_api"]["error"] = hubs_resp.text[:300]
            
        return jsonify({
            "status": "success",
            "debug_info": debug_info
        })
        
    except Exception as e:
        return jsonify({
            "error": f"调试过程中发生错误: {str(e)}",
            "status": "error",
            "debug_info": debug_info
        }), 500


@auth_bp.route('/api/auth/monitor-status', methods=['GET'])
def monitor_status():
    """获取后台token监控状态"""
    try:
        # 获取监控状态
        monitor_status = utils.get_monitor_status()
        
        # 获取token信息
        token_info = utils.get_token_info()
        
        return jsonify({
            "status": "success",
            "monitor_status": monitor_status,
            "token_info": token_info,
            "message": "后台监控状态获取成功"
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"获取监控状态失败: {str(e)}"
        }), 500


