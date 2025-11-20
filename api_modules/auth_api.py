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
    
    # 权限缓存，避免重复检查相同项目
    permissions_cache = {}
    
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
                
                # 获取真实的项目权限信息（使用缓存）
                clean_project_id = project_id.replace('b.', '') if project_id.startswith('b.') else project_id
                if clean_project_id in permissions_cache:
                    print(f"🔍 使用缓存的项目权限: {project_id}")
                    attributes['permissions'] = permissions_cache[clean_project_id]
                else:
                    print(f"🔍 开始获取项目权限: {project_id}")
                    try:
                        permissions = determine_project_permissions(project_id, headers)
                        print(f"✅ 权限检查完成: {permissions}")
                        attributes['permissions'] = permissions
                        permissions_cache[clean_project_id] = permissions
                    except Exception as perm_error:
                        print(f"❌ 权限检查失败: {str(perm_error)}")
                        import traceback
                        print(f"📋 权限检查错误详情: {traceback.format_exc()}")
                        # 设置默认权限
                        default_permissions = {
                            'scope': 'Permission check failed',
                            'level': 'member',
                            'description': f'权限检查异常: {str(perm_error)}'
                        }
                        attributes['permissions'] = default_permissions
                        permissions_cache[clean_project_id] = default_permissions
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
                
                # 获取真实的项目权限信息（使用缓存）
                clean_project_id = project_id.replace('b.', '') if project_id.startswith('b.') else project_id
                if clean_project_id in permissions_cache:
                    print(f"🔍 使用缓存的项目权限(无ACC数据): {project_id}")
                    attributes['permissions'] = permissions_cache[clean_project_id]
                else:
                    print(f"🔍 开始获取项目权限(无ACC数据): {project_id}")
                    try:
                        permissions = determine_project_permissions(project_id, headers)
                        print(f"✅ 权限检查完成(无ACC数据): {permissions}")
                        attributes['permissions'] = permissions
                        permissions_cache[clean_project_id] = permissions
                    except Exception as perm_error:
                        print(f"❌ 权限检查失败(无ACC数据): {str(perm_error)}")
                        import traceback
                        print(f"📋 权限检查错误详情: {traceback.format_exc()}")
                        # 设置默认权限
                        default_permissions = {
                            'scope': 'Permission check failed',
                            'level': 'member',
                            'description': f'权限检查异常: {str(perm_error)}'
                        }
                        attributes['permissions'] = default_permissions
                        permissions_cache[clean_project_id] = default_permissions
            
            # 确保permissions对象完整（但不覆盖已设置的权限）
            if 'permissions' in attributes and attributes['permissions']:
                permissions = attributes['permissions']
                # 只在缺少字段时添加默认值，不覆盖已有值
                if 'scope' not in permissions or not permissions['scope']:
                    permissions['scope'] = 'Basic access'
                if 'level' not in permissions or not permissions['level']:
                    permissions['level'] = 'member'
                if 'description' not in permissions or not permissions['description']:
                    permissions['description'] = 'Standard project access permissions'
                print(f"✅ 权限信息已设置: {permissions}")
            else:
                # 如果没有权限信息，设置默认值
                print("⚠️ 没有权限信息，使用默认值")
                attributes['permissions'] = {
                    'scope': 'Project access',
                    'level': 'member',
                    'description': 'Standard project access permissions'
                }
            
            enhanced_projects.append(enhanced_project)
        
        enhanced_data['data'] = enhanced_projects
        
    except Exception as e:
        print(f"❌ 增强项目数据时出错: {str(e)}")
        import traceback
        print(f"📋 错误详情: {traceback.format_exc()}")
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
                'scope': 'Basic access',
                'level': 'member',
                'description': 'Standard project access permissions'
            }
        
        return projects_data
    
    return enhanced_data


def determine_project_permissions(project_id, headers):
    """
    确定用户在项目中的权限范围
    """
    try:
        # 清理项目ID，移除'b.'前缀用于Admin API
        clean_project_id = project_id.replace('b.', '') if project_id.startswith('b.') else project_id
        
        print(f"🔍 检查项目权限: {project_id} -> {clean_project_id}")
        
        # 尝试访问项目用户管理端点来判断权限级别（更准确的权限检查）
        admin_resp = requests.get(
            f"{config.AUTODESK_API_BASE}/construction/admin/v1/projects/{clean_project_id}/users",
            headers=headers,
            params={'limit': 1},  # 只获取1个用户来测试权限
            timeout=(5, 10)
        )
        
        print(f"📊 Admin API 响应: {admin_resp.status_code}")
        print(f"🔗 API URL: {config.AUTODESK_API_BASE}/construction/admin/v1/projects/{clean_project_id}/users")
        
        if admin_resp.status_code == 200:
            # 能够访问用户管理API，说明有管理权限
            admin_data = admin_resp.json()
            user_count = len(admin_data.get('results', []))
            
            return {
                'scope': 'Project management',
                'level': 'admin',
                'description': f'完整的项目管理权限（可管理 {user_count} 个用户）'
            }
        elif admin_resp.status_code == 403:
            print("⚠️ 无项目管理权限")
            return {
                'scope': 'Data access',
                'level': 'member',
                'description': '项目数据读写权限（无管理权限）'
            }
                
        elif admin_resp.status_code == 404:
            print("❌ 项目不存在或无权访问")
            return {
                'scope': 'No permission',
                'level': 'none',
                'description': 'Project does not exist or no access permission'
            }
        else:
            print(f"⚠️ Admin API 返回未知状态: {admin_resp.status_code}")
            return {
                'scope': 'Unknown permission',
                'level': 'unknown',
                'description': f'权限级别未确定 (HTTP {admin_resp.status_code})'
            }
            
    except Exception as e:
        print(f"❌ 确定项目权限时出错: {str(e)}")
        return {
            'scope': 'Basic access',
            'level': 'member',
            'description': '标准项目访问权限（权限检查异常）'
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
                }}, '{config.FRONTEND_ORIGIN}');
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
                    error_description: 'Authorization code not received'
                }}, '{config.FRONTEND_ORIGIN}');
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
                    }}, '{config.FRONTEND_ORIGIN}');
                    setTimeout(function() {{
                        window.close();
                    }}, 3000);
                </script>
            </body>
            </html>
            """
        # 清除已使用的state
        session.pop('oauth_state', None)
    
    # 检查OAuth配置是否可用
    if not config.CLIENT_ID or not config.CLIENT_SECRET or not config.CALLBACK_URL:
        return utils.generate_html_response(
            "配置错误",
            '<div class="error">OAuth配置不完整。请设置环境变量：AUTODESK_CLIENT_ID, AUTODESK_CLIENT_SECRET, AUTODESK_CALLBACK_URL</div>'
        )
    
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
                    }}, '{config.FRONTEND_ORIGIN}');
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
                    }}, '{config.FRONTEND_ORIGIN}');
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
                        message: 'Authentication successful'
                    }}, '{config.FRONTEND_ORIGIN}');
                    setTimeout(function() {{
                        window.close();
                        window.location.href = '{config.FRONTEND_ORIGIN}/#/auth/success';
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
                    }}, '{config.FRONTEND_ORIGIN}');
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
            }}, '{config.FRONTEND_ORIGIN}');
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
                "message": "User authenticated",
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
    """手动刷新token - 使用统一的刷新函数"""
    try:
        print("🔄 Manual token refresh requested")
        
        # 使用统一的token刷新函数（函数内部会处理锁）
        success, result, error_code = utils.refresh_access_token(force=True, source="manual_api")
        
        if success:
            # 刷新成功，返回token信息
            token_data = result
            expires_in = token_data.get('expires_in', 3600)
            
            print("✅ Manual token refresh successful")
            return jsonify({
                "status": "success",
                "message": "Token刷新成功",
                "token_info": {
                    'has_access_token': True,
                    'has_refresh_token': True,
                    'is_valid': True,
                    'expires_in_minutes': int(expires_in / 60),
                    'expires_at': datetime.fromtimestamp(time.time() + expires_in).isoformat()
                }
            })
        else:
            # 刷新失败，根据错误码返回适当的HTTP状态码
            print(f"❌ Manual token refresh failed: {result} (code: {error_code})")
            
            if error_code == "no_refresh_token":
                return jsonify({
                    "status": "error",
                    "message": result,
                    "error_code": error_code,
                    "requires_reauth": True
                }), 400
            elif error_code == "refresh_token_expired":
                return jsonify({
                    "status": "error", 
                    "message": result,
                    "error_code": error_code,
                    "requires_reauth": True
                }), 401
            elif error_code == "config_incomplete":
                return jsonify({
                    "status": "error",
                    "message": result,
                    "error_code": error_code
                }), 500
            elif error_code in ["timeout", "connection_error"]:
                return jsonify({
                    "status": "error",
                    "message": result,
                    "error_code": error_code,
                    "retry_suggested": True
                }), 503
            else:
                return jsonify({
                    "status": "error",
                    "message": result,
                    "error_code": error_code
                }), 400
            
    except Exception as e:
        print(f"❌ Manual token refresh exception: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"刷新token时发生异常: {str(e)}",
            "error_code": "exception"
        }), 500


@auth_bp.route('/api/auth/get-token', methods=['GET'])
def get_token():
    """获取完整的access token用于复制"""
    try:
        print("🔍 Get full token requested")
        
        # 获取access token
        access_token = utils.get_access_token()
        
        if access_token:
            print("✅ Full token retrieved successfully")
            return jsonify({
                "status": "success",
                "access_token": access_token,
                "message": "Token获取成功"
            })
        else:
            print("❌ No valid token available")
            return jsonify({
                "status": "error",
                "message": "未找到有效的 Access Token，请先进行认证"
            }), 401
                
    except Exception as e:
        print(f"❌ Get token error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"获取token时发生错误: {str(e)}"
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
    print("🔍 account-info API 被调用")
    
    access_token = utils.get_access_token()
    if not access_token:
        print("❌ account-info: 未找到access token")
        return jsonify({
            "error": "未找到 Access Token，请先进行认证",
            "status": "unauthorized"
        }), 401
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        print("📋 account-info: 开始获取用户信息...")
        # 获取用户信息，增加超时设置
        user_resp = requests.get(
            f"{config.AUTODESK_API_BASE}/userprofile/v1/users/@me", 
            headers=headers,
            timeout=(10, 15)  # 连接超时10秒，读取超时15秒
        )
        
        if user_resp.status_code != 200:
            print(f"❌ account-info: 获取用户信息失败: {user_resp.status_code}")
            raise Exception(f"Failed to get user information: {user_resp.status_code}")
        
        user_data = user_resp.json()
        print(f"✅ account-info: 用户信息获取成功: {user_data.get('userName', 'Unknown')}")
        
        print("📋 account-info: 开始获取Hub信息...")
        # 使用增强的账户信息获取函数
        hub_id, real_account_id, hub_name, user_data_enhanced = utils.get_user_account_info(access_token)
        
        if not hub_id:
            print("⚠️ account-info: 无法获取Hub信息")
            # 如果无法获取Hub信息，只返回用户basicInfo
            return jsonify({
                "status": "success",
                "user": user_data,
                "projects": {"data": [], "jsonapi": {"version": "1.0"}},
                "hub": {
                    "hubId": None,
                    "hubName": None,
                    "realAccountId": None
                },
                "warning": "无法获取Hub信息，用户可能没有BIM 360/ACC账户权限"
            })
        
        # 检查是否是fallback Hub ID（用户没有真实Hub访问权限）
        # 修复：只有当Hub ID是通过fallback逻辑生成的才跳过项目获取
        # 真实的企业Hub通过Hubs API获取，fallback Hub通过用户ID构造
        is_fallback_hub = False
        
        # 尝试通过Hubs API验证这是否是真实的Hub
        try:
            hubs_resp = requests.get(f"{config.AUTODESK_API_BASE}/project/v1/hubs", headers=headers)
            if hubs_resp.status_code == 200:
                hubs_data = hubs_resp.json()
                # 检查当前hub_id是否在真实的Hubs列表中
                real_hub_ids = [hub.get('id') for hub in hubs_data.get('data', [])]
                if hub_id not in real_hub_ids:
                    is_fallback_hub = True
                    print(f"⚠️ account-info: Hub ID {hub_id} 不在真实Hub列表中，判定为fallback")
                else:
                    print(f"✅ account-info: Hub ID {hub_id} 是真实的企业Hub")
            else:
                print(f"⚠️ account-info: 无法验证Hub状态，继续获取项目")
        except Exception as e:
            print(f"⚠️ account-info: Hub验证出错: {e}，继续获取项目")
        
        if is_fallback_hub:
            print("⚠️ account-info: 检测到fallback Hub ID，跳过项目获取")
            projects_data = {"data": [], "jsonapi": {"version": "1.0"}}
            enhanced_projects = {"data": [], "jsonapi": {"version": "1.0"}}
        else:
            print("📋 account-info: 开始获取项目信息...")
            # 获取Hub下的所有项目
            projects_data = get_projects_from_hub(hub_id, headers)
            print(f"📋 account-info: 获取到 {len(projects_data.get('data', []))} 个项目")
            
            # 使用增强的项目数据处理，包含真实的权限检查
            print("📋 account-info: 开始增强项目数据...")
            enhanced_projects = enhance_project_data(projects_data, headers, hub_id, real_account_id)
            print(f"✅ account-info: 项目数据增强完成")
        
        print("✅ account-info: 账户信息获取完成")
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
        
    except requests.exceptions.Timeout as e:
        print(f"❌ account-info: 请求超时: {str(e)}")
        return jsonify({
            "error": "请求超时，请稍后重试",
            "status": "timeout"
        }), 408
    except requests.exceptions.ConnectionError as e:
        print(f"❌ account-info: 连接错误: {str(e)}")
        return jsonify({
            "error": "网络连接错误，请检查网络连接",
            "status": "connection_error"
        }), 503
    except Exception as e:
        print(f"❌ account-info: 未知错误: {str(e)}")
        return jsonify({
            "error": f"获取账户信息时发生错误: {str(e)}",
            "status": "error"
        }), 500



# 项目获取API - 从account_info中提取项目信息
@auth_bp.route('/api/auth/projects')
def get_projects():
    """获取用户可访问的项目列表"""
    print("🔍 projects API 被调用")
    
    access_token = utils.get_access_token()
    if not access_token:
        print("❌ projects: 未找到access token")
        return jsonify({
            "error": "未找到 Access Token，请先进行认证",
            "status": "unauthorized"
        }), 401
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        print("📋 projects: 开始获取Hub信息...")
        # 使用增强的账户信息获取函数
        hub_id, real_account_id, hub_name, user_data_enhanced = utils.get_user_account_info(access_token)
        
        if not hub_id:
            print("⚠️ projects: 无法获取Hub信息")
            # 如果无法获取Hub信息，返回空项目列表但不报错
            return jsonify({
                "status": "success",
                "projects": {"data": [], "jsonapi": {"version": "1.0"}},
                "hub": {
                    "hubId": None,
                    "hubName": None,
                    "realAccountId": None
                },
                "warning": "无法获取Hub信息，用户可能没有BIM 360/ACC账户权限"
            })
        
        # 检查是否是fallback Hub ID（用户没有真实Hub访问权限）
        is_fallback_hub = False
        
        # 尝试通过Hubs API验证这是否是真实的Hub
        try:
            hubs_resp = requests.get(f"{config.AUTODESK_API_BASE}/project/v1/hubs", headers=headers)
            if hubs_resp.status_code == 200:
                hubs_data = hubs_resp.json()
                # 检查当前hub_id是否在真实的Hubs列表中
                real_hub_ids = [hub.get('id') for hub in hubs_data.get('data', [])]
                if hub_id not in real_hub_ids:
                    is_fallback_hub = True
                    print(f"⚠️ projects: Hub ID {hub_id} 不在真实Hub列表中，判定为fallback")
                else:
                    print(f"✅ projects: Hub ID {hub_id} 是真实的企业Hub")
            else:
                print(f"⚠️ projects: 无法验证Hub状态，继续获取项目")
        except Exception as e:
            print(f"⚠️ projects: Hub验证出错: {e}，继续获取项目")
        
        if is_fallback_hub:
            print("⚠️ projects: 检测到fallback Hub ID，跳过项目获取")
            projects_data = {"data": [], "jsonapi": {"version": "1.0"}}
            enhanced_projects = {"data": [], "jsonapi": {"version": "1.0"}}
        else:
            print("📋 projects: 开始获取项目信息...")
            # 获取Hub下的所有项目
            projects_data = get_projects_from_hub(hub_id, headers)
            print(f"📋 projects: 获取到 {len(projects_data.get('data', []))} 个项目")
            
            # 使用增强的项目数据处理，包含真实的权限检查
            print("📋 projects: 开始增强项目数据...")
            enhanced_projects = enhance_project_data(projects_data, headers, hub_id, real_account_id)
            print(f"✅ projects: 项目数据增强完成")
        
        print("✅ projects: 项目信息获取完成")
        return jsonify({
            "status": "success",
            "projects": enhanced_projects,
            "hub": {
                "hubId": hub_id,
                "hubName": hub_name,
                "realAccountId": real_account_id
            }
        })
        
    except requests.exceptions.Timeout as e:
        print(f"❌ projects: 请求超时: {str(e)}")
        return jsonify({
            "error": "请求超时，请稍后重试",
            "status": "timeout"
        }), 408
    except requests.exceptions.ConnectionError as e:
        print(f"❌ projects: 连接错误: {str(e)}")
        return jsonify({
            "error": "网络连接错误，请检查网络连接",
            "status": "connection_error"
        }), 503
    except Exception as e:
        print(f"❌ projects: 未知错误: {str(e)}")
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
            "message": "Background monitoring status retrieved successfully"
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"获取监控状态失败: {str(e)}"
        }), 500

