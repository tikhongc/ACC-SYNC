"""
用户管理API模块
提供项目用户查询和管理功能
"""

import requests
import time
from datetime import datetime
from flask import Blueprint, jsonify, request
import utils

users_bp = Blueprint('users', __name__)

@users_bp.route('/api/users/project/<project_id>/users')
def get_project_users(project_id):
    """
    获取项目的用户列表
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
        print(f"🔍 获取项目用户列表: {project_id}")
        start_time = time.time()
        
        # 获取查询参数
        limit = request.args.get('limit', 200, type=int)  # 默认获取最多200个用户
        offset = request.args.get('offset', 0, type=int)
        filter_name = request.args.get('filter[name]', '')
        filter_email = request.args.get('filter[email]', '')
        filter_status = request.args.get('filter[status]', 'active,pending')
        sort = request.args.get('sort', 'name')
        
        # 构建API URL - 需要移除项目ID的"b."前缀
        clean_project_id = project_id.replace('b.', '') if project_id.startswith('b.') else project_id
        api_url = f"https://developer.api.autodesk.com/construction/admin/v1/projects/{clean_project_id}/users"
        
        # 构建查询参数
        params = {
            'limit': limit,
            'offset': offset,
            'sort': sort,
            'fields': 'name,email,firstName,lastName,autodeskId,imageUrl,phone,jobTitle,industry,aboutMe,accessLevels,companyId,companyName,roleIds,roles,status,addedOn,products'
        }
        
        if filter_name:
            params['filter[name]'] = filter_name
        if filter_email:
            params['filter[email]'] = filter_email
        if filter_status:
            params['filter[status]'] = filter_status
        
        print(f"📡 调用API: {api_url}")
        print(f"📋 查询参数: {params}")
        
        response = requests.get(api_url, headers=headers, params=params)
        
        if response.status_code == 200:
            api_data = response.json()
            
            # 处理用户数据
            users = []
            for user in api_data.get('results', []):
                processed_user = {
                    'id': user.get('id'),
                    'name': user.get('name'),
                    'email': user.get('email'),
                    'firstName': user.get('firstName'),
                    'lastName': user.get('lastName'),
                    'autodeskId': user.get('autodeskId'),
                    'imageUrl': user.get('imageUrl'),
                    'phone': user.get('phone'),
                    'jobTitle': user.get('jobTitle'),
                    'industry': user.get('industry'),
                    'aboutMe': user.get('aboutMe'),
                    'companyId': user.get('companyId'),
                    'companyName': user.get('companyName'),
                    'status': user.get('status'),
                    'addedOn': user.get('addedOn'),
                    'accessLevels': user.get('accessLevels', {}),
                    'roles': user.get('roles', []),
                    'roleIds': user.get('roleIds', []),
                    'products': user.get('products', [])
                }
                users.append(processed_user)
            
            # 统计信息
            pagination = api_data.get('pagination', {})
            statistics = {
                'total_users': pagination.get('totalResults', len(users)),
                'active_users': len([u for u in users if u.get('status') == 'active']),
                'pending_users': len([u for u in users if u.get('status') == 'pending']),
                'companies': len(set([u.get('companyName') for u in users if u.get('companyName')])),
                'roles': len(set([role.get('name') for u in users for role in u.get('roles', []) if role.get('name')])),
                'query_duration_seconds': round(time.time() - start_time, 2)
            }
            
            result = {
                'project_id': project_id,
                'query_time': datetime.now().isoformat(),
                'users': users,
                'statistics': statistics,
                'pagination': pagination
            }
            
            print(f"✅ 用户列表获取成功:")
            print(f"   👥 总用户数: {statistics['total_users']}")
            print(f"   ✅ 活跃用户: {statistics['active_users']}")
            print(f"   ⏳ 待激活用户: {statistics['pending_users']}")
            print(f"   🏢 公司数: {statistics['companies']}")
            print(f"   🎭 角色数: {statistics['roles']}")
            print(f"   ⏱️ 查询耗时: {statistics['query_duration_seconds']} 秒")
            
            return jsonify({
                "status": "success",
                "message": f"成功获取项目用户列表，共 {statistics['total_users']} 个用户",
                "data": result
            })
            
        else:
            error_msg = f"API调用失败: {response.status_code}"
            if response.text:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('message', error_msg)
                except:
                    error_msg = response.text
            
            print(f"❌ 获取用户列表失败: {error_msg}")
            return jsonify({
                "error": error_msg,
                "status": "error",
                "project_id": project_id
            }), response.status_code
            
    except Exception as e:
        print(f"❌ 获取用户列表时出错: {str(e)}")
        return jsonify({
            "error": f"获取用户列表失败: {str(e)}",
            "status": "error",
            "project_id": project_id
        }), 500


@users_bp.route('/api/users/project/<project_id>/users/<user_id>')
def get_project_user_detail(project_id, user_id):
    """
    获取项目中特定用户的详细信息
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
        print(f"🔍 获取用户详细信息: {user_id} in project {project_id}")
        
        # 构建API URL - 需要移除项目ID的"b."前缀
        clean_project_id = project_id.replace('b.', '') if project_id.startswith('b.') else project_id
        api_url = f"https://developer.api.autodesk.com/construction/admin/v1/projects/{clean_project_id}/users/{user_id}"
        
        # 获取所有字段
        params = {
            'fields': 'name,email,firstName,lastName,autodeskId,analyticsId,addressLine1,addressLine2,city,stateOrProvince,postalCode,country,imageUrl,phone,jobTitle,industry,aboutMe,accessLevels,companyId,roleIds,roles,status,addedOn,products'
        }
        
        print(f"📡 调用API: {api_url}")
        
        response = requests.get(api_url, headers=headers, params=params)
        
        if response.status_code == 200:
            user_data = response.json()
            
            print(f"✅ 用户详细信息获取成功: {user_data.get('name', 'Unknown')}")
            
            return jsonify({
                "status": "success",
                "message": f"成功获取用户详细信息",
                "data": user_data
            })
            
        else:
            error_msg = f"API调用失败: {response.status_code}"
            if response.text:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('message', error_msg)
                except:
                    error_msg = response.text
            
            print(f"❌ 获取用户详细信息失败: {error_msg}")
            return jsonify({
                "error": error_msg,
                "status": "error",
                "project_id": project_id,
                "user_id": user_id
            }), response.status_code
            
    except Exception as e:
        print(f"❌ 获取用户详细信息时出错: {str(e)}")
        return jsonify({
            "error": f"获取用户详细信息失败: {str(e)}",
            "status": "error",
            "project_id": project_id,
            "user_id": user_id
        }), 500


@users_bp.route('/api/users/project/<project_id>/download-users')
def download_project_users(project_id):
    """
    下载项目用户数据的JSON文件
    """
    access_token = utils.get_access_token()
    if not access_token:
        return jsonify({
            "error": "未找到 Access Token，请先进行认证",
            "status": "unauthorized"
        }), 401
    
    try:
        print(f"📥 准备下载项目用户数据: {project_id}")
        
        # 获取完整的用户列表（不分页）
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # 构建API URL
        clean_project_id = project_id.replace('b.', '') if project_id.startswith('b.') else project_id
        api_url = f"https://developer.api.autodesk.com/construction/admin/v1/projects/{clean_project_id}/users"
        
        params = {
            'limit': 200,  # 最大限制
            'offset': 0,
            'sort': 'name',
            'fields': 'name,email,firstName,lastName,autodeskId,analyticsId,addressLine1,addressLine2,city,stateOrProvince,postalCode,country,imageUrl,phone,jobTitle,industry,aboutMe,accessLevels,companyId,companyName,roleIds,roles,status,addedOn,products'
        }
        
        response = requests.get(api_url, headers=headers, params=params)
        
        if response.status_code == 200:
            api_data = response.json()
            
            # 构建导出数据
            export_data = {
                "project_id": project_id,
                "export_time": datetime.now().isoformat(),
                "export_parameters": {
                    "include_all_fields": True,
                    "sort_by": "name"
                },
                "users": api_data.get('results', []),
                "statistics": {
                    "total_users": len(api_data.get('results', [])),
                    "active_users": len([u for u in api_data.get('results', []) if u.get('status') == 'active']),
                    "pending_users": len([u for u in api_data.get('results', []) if u.get('status') == 'pending']),
                    "companies": len(set([u.get('companyName') for u in api_data.get('results', []) if u.get('companyName')])),
                    "roles": len(set([role.get('name') for u in api_data.get('results', []) for role in u.get('roles', []) if role.get('name')]))
                },
                "pagination": api_data.get('pagination', {})
            }
            
            print(f"✅ 用户数据导出准备完成，共 {len(api_data.get('results', []))} 个用户")
            
            # 返回JSON数据供前端下载
            from flask import Response
            import json
            
            json_str = json.dumps(export_data, indent=2, ensure_ascii=False)
            
            response = Response(
                json_str,
                mimetype='application/json',
                headers={
                    'Content-Disposition': f'attachment; filename=project_{clean_project_id}_users_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                }
            )
            
            return response
            
        else:
            error_msg = f"API调用失败: {response.status_code}"
            return jsonify({
                "error": error_msg,
                "status": "error"
            }), response.status_code
            
    except Exception as e:
        print(f"❌ 下载用户数据时出错: {str(e)}")
        return jsonify({
            "error": f"下载用户数据失败: {str(e)}",
            "status": "error"
        }), 500


@users_bp.route('/api/users/project/<project_id>/roles')
def get_project_roles(project_id):
    """
    获取项目的角色列表
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
        print(f"🔍 获取项目角色列表: {project_id}")
        start_time = time.time()
        
        # 构建API URL - 需要移除项目ID的"b."前缀
        clean_project_id = project_id.replace('b.', '') if project_id.startswith('b.') else project_id
        api_url = f"https://developer.api.autodesk.com/construction/admin/v1/projects/{clean_project_id}/roles"
        
        print(f"📡 调用API: {api_url}")
        
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            api_data = response.json()
            
            # 处理角色数据
            roles = []
            for role in api_data.get('results', []):
                processed_role = {
                    'id': role.get('id'),
                    'name': role.get('name'),
                    'description': role.get('description'),
                    'permissions': role.get('permissions', []),
                    'memberCount': role.get('memberCount', 0),
                    'isDefault': role.get('isDefault', False),
                    'createdAt': role.get('createdAt'),
                    'updatedAt': role.get('updatedAt')
                }
                roles.append(processed_role)
            
            # 统计信息
            statistics = {
                'total_roles': len(roles),
                'default_roles': len([r for r in roles if r.get('isDefault')]),
                'custom_roles': len([r for r in roles if not r.get('isDefault')])
            }
            
            elapsed_time = time.time() - start_time
            print(f"✅ 角色列表获取成功: {len(roles)} 个角色 (耗时: {elapsed_time:.2f}s)")
            
            result = {
                "project_id": project_id,
                "roles": roles,
                "statistics": statistics,
                "request_time": datetime.now().isoformat(),
                "response_time_seconds": elapsed_time
            }
            
            return jsonify({
                "status": "success",
                "data": result
            })
            
        else:
            error_msg = f"API调用失败: {response.status_code}"
            if response.text:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('message', error_msg)
                except:
                    error_msg = response.text
            
            print(f"❌ 获取角色列表失败: {error_msg}")
            return jsonify({
                "error": error_msg,
                "status": "error",
                "project_id": project_id
            }), response.status_code
            
    except Exception as e:
        print(f"❌ 获取角色列表时出错: {str(e)}")
        return jsonify({
            "error": f"获取角色列表失败: {str(e)}",
            "status": "error",
            "project_id": project_id
        }), 500


@users_bp.route('/api/users/project/<project_id>/companies')
def get_project_companies(project_id):
    """
    获取项目的公司列表 - 使用2-legged token (app only)
    """
    # 项目公司API需要使用2-legged token (app only)
    access_token = utils.get_two_legged_token()
    if not access_token:
        return jsonify({
            "error": "未找到 2-legged Access Token，无法访问项目公司API",
            "status": "unauthorized"
        }), 401
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        print(f"🔍 获取项目公司列表: {project_id}")
        start_time = time.time()
        
        # 获取账户信息 - 使用3-legged token
        user_access_token = utils.get_access_token()
        if not user_access_token:
            return jsonify({
                "error": "未找到用户 Access Token，无法获取账户信息",
                "status": "error",
                "project_id": project_id
            }), 401
            
        user_headers = {
            "Authorization": f"Bearer {user_access_token}",
            "Content-Type": "application/json"
        }
        
        account_info_response = requests.get(
            "https://developer.api.autodesk.com/project/v1/hubs",
            headers=user_headers
        )
        
        if account_info_response.status_code != 200:
            return jsonify({
                "error": "Unable to get account information",
                "status": "error",
                "project_id": project_id
            }), 500
        
        hubs = account_info_response.json().get('data', [])
        if not hubs:
            return jsonify({
                "error": "Account information not found",
                "status": "error", 
                "project_id": project_id
            }), 404
        
        # 获取账户ID (移除b.前缀)
        account_id = hubs[0]['id'].replace('b.', '') if hubs[0]['id'].startswith('b.') else hubs[0]['id']
        
        # 构建正确的项目公司API URL - 这个API包含member_group_id
        clean_project_id = project_id.replace('b.', '') if project_id.startswith('b.') else project_id
        api_url = f"https://developer.api.autodesk.com/hq/v1/accounts/{account_id}/projects/{clean_project_id}/companies"
        
        # 添加查询参数
        params = {
            'limit': 100,  # 获取更多公司
            'offset': 0,
            'sort': 'name'
        }
        
        print(f"📡 调用项目公司API: {api_url}")
        print(f"📋 查询参数: {params}")
        print(f"🔑 请求头: Authorization: Bearer {access_token[:20]}...")
        print(f"📊 账户ID: {account_id}")
        print(f"📊 项目ID: {clean_project_id}")
        
        response = requests.get(api_url, headers=headers, params=params, timeout=30)
        
        print(f"📈 响应状态码: {response.status_code}")
        print(f"📄 响应头: {dict(response.headers)}")
        if response.status_code != 200:
            print(f"❌ 错误响应内容: {response.text[:500]}")
        
        if response.status_code == 200:
            # 项目公司API返回的是数组，不是带results的对象
            api_data = response.json()
            companies_list = api_data if isinstance(api_data, list) else api_data.get('results', [])
            
            # 处理公司数据，包含member_group_id
            companies = []
            for company in companies_list:
                processed_company = {
                    'id': company.get('id'),
                    'name': company.get('name'),
                    'member_group_id': company.get('member_group_id'),  # 🔑 关键字段 - 直接从API获取
                    'account_id': company.get('account_id'),
                    'project_id': company.get('project_id'),
                    'trade': company.get('trade'),
                    'description': company.get('description'),
                    'address': {
                        'line1': company.get('address_line_1'),
                        'line2': company.get('address_line_2'),
                        'city': company.get('city'),
                        'state': company.get('state_or_province'),
                        'postal_code': company.get('postal_code'),
                        'country': company.get('country')
                    },
                    'phone': company.get('phone'),
                    'website': company.get('website_url'),
                    'erp_id': company.get('erp_id'),
                    'tax_id': company.get('tax_id'),
                    'created_at': company.get('created_at'),
                    'updated_at': company.get('updated_at')
                }
                companies.append(processed_company)
                
                # 打印每个公司的member_group_id以便调试
                if company.get('member_group_id'):
                    print(f"✅ 公司 '{company.get('name')}' 的 member_group_id: {company.get('member_group_id')}")
                else:
                    print(f"⚠️ 公司 '{company.get('name')}' 没有 member_group_id")
            
            print(f"📊 API返回 {len(companies)} 个公司，其中 {len([c for c in companies if c.get('member_group_id')])} 个有member_group_id")
            
            # 统计信息
            statistics = {
                'total_companies': len(companies),
                'companies_with_members': len([c for c in companies if c.get('memberCount', 0) > 0]),
                'companies_with_member_group_id': len([c for c in companies if c.get('member_group_id')])
            }
            
            elapsed_time = time.time() - start_time
            print(f"✅ 公司列表获取成功: {len(companies)} 个公司 (耗时: {elapsed_time:.2f}s)")
            
            result = {
                "project_id": project_id,
                "companies": companies,
                "statistics": statistics,
                "request_time": datetime.now().isoformat(),
                "response_time_seconds": elapsed_time
            }
            
            return jsonify({
                "status": "success",
                "data": result
            })
            
        else:
            error_msg = f"API调用失败: {response.status_code}"
            if response.text:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('message', error_msg)
                except:
                    error_msg = response.text
            
            print(f"❌ 获取公司列表失败: {error_msg}")
            return jsonify({
                "error": error_msg,
                "status": "error",
                "project_id": project_id
            }), response.status_code
            
    except Exception as e:
        print(f"❌ 获取公司列表时出错: {str(e)}")
        return jsonify({
            "error": f"获取公司列表失败: {str(e)}",
            "status": "error",
            "project_id": project_id
        }), 500