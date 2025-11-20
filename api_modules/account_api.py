"""
账户管理API模块
提供账户、用户、公司、角色的查询和管理功能
基于AccountRolesList.vue的模式设计
"""

import json
import time
from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from typing import Dict, List, Optional, Any
import utils

# 添加数据库访问
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../database_sql'))

try:
    from neon_config import NeonConfig
    from account_sync import AccountDataSyncManager
    import psycopg2
    import psycopg2.extras
except ImportError as e:
    print(f"Warning: Could not import database dependencies: {e}")
    NeonConfig = None
    AccountDataSyncManager = None
    psycopg2 = None

account_bp = Blueprint('account', __name__)

class AccountManager:
    """账户管理器"""
    
    def __init__(self):
        """初始化账户管理器"""
        self.neon_config = NeonConfig()
        self.db_params = self.neon_config.get_db_params()
        self.sync_manager = AccountDataSyncManager()
    
    def get_connection(self):
        """获取数据库连接"""
        return psycopg2.connect(**self.db_params)
    
    def get_account_roles_summary(self, account_id: str) -> Dict[str, Any]:
        """
        获取账户角色汇总（类似AccountRolesList.vue）
        
        Args:
            account_id: 账户ID
            
        Returns:
            角色汇总数据
        """
        return self.sync_manager.get_account_roles_summary(account_id)
    
    def get_account_users(
        self, 
        account_id: str, 
        filters: Dict = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """
        获取账户用户列表
        
        Args:
            account_id: 账户ID
            filters: 过滤条件
            page: 页码
            page_size: 每页大小
            
        Returns:
            用户列表和分页信息
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # 构建查询条件
            where_conditions = ["account_id = %s"]
            params = [account_id]
            
            if filters:
                if filters.get('status'):
                    where_conditions.append("status = %s")
                    params.append(filters['status'])
                
                if filters.get('role'):
                    where_conditions.append("role = %s")
                    params.append(filters['role'])
                
                if filters.get('company_id'):
                    where_conditions.append("company_id = %s")
                    params.append(filters['company_id'])
                
                if filters.get('search'):
                    search_term = f"%{filters['search']}%"
                    where_conditions.append("(name ILIKE %s OR email ILIKE %s)")
                    params.extend([search_term, search_term])
            
            where_clause = f"WHERE {' AND '.join(where_conditions)}"
            
            # 获取总数
            count_sql = f"SELECT COUNT(*) FROM users {where_clause}"
            cursor.execute(count_sql, params)
            total_count = cursor.fetchone()[0]
            
            # 获取分页数据
            offset = (page - 1) * page_size
            list_sql = f"""
                SELECT 
                    u.*,
                    c.name as company_name_full,
                    c.trade as company_trade
                FROM users u
                LEFT JOIN companies c ON u.company_id = c.company_id
                {where_clause}
                ORDER BY u.name ASC
                LIMIT %s OFFSET %s
            """
            
            params.extend([page_size, offset])
            cursor.execute(list_sql, params)
            
            users = [dict(user) for user in cursor.fetchall()]
            
            # 计算分页信息
            total_pages = (total_count + page_size - 1) // page_size
            
            return {
                'users': users,
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total_count': total_count,
                    'total_pages': total_pages,
                    'has_next': page < total_pages,
                    'has_prev': page > 1
                },
                'filters_applied': filters or {}
            }
            
        except Exception as e:
            print(f"✗ 获取账户用户失败: {str(e)}")
            return {
                'users': [],
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total_count': 0,
                    'total_pages': 0,
                    'has_next': False,
                    'has_prev': False
                },
                'filters_applied': filters or {},
                'error': str(e)
            }
            
        finally:
            if conn:
                conn.close()
    
    def get_account_companies(
        self,
        account_id: str,
        project_id: str = None,
        filters: Dict = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """
        获取账户公司列表
        
        Args:
            account_id: 账户ID
            project_id: 项目ID（可选）
            filters: 过滤条件
            page: 页码
            page_size: 每页大小
            
        Returns:
            公司列表和分页信息
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # 构建查询条件
            where_conditions = ["account_id = %s"]
            params = [account_id]
            
            if project_id:
                where_conditions.append("(project_id = %s OR project_id IS NULL)")
                params.append(project_id)
            
            if filters:
                if filters.get('trade'):
                    where_conditions.append("trade = %s")
                    params.append(filters['trade'])
                
                if filters.get('country'):
                    where_conditions.append("country = %s")
                    params.append(filters['country'])
                
                if filters.get('search'):
                    search_term = f"%{filters['search']}%"
                    where_conditions.append("name ILIKE %s")
                    params.append(search_term)
            
            where_clause = f"WHERE {' AND '.join(where_conditions)}"
            
            # 获取总数
            count_sql = f"SELECT COUNT(*) FROM companies {where_clause}"
            cursor.execute(count_sql, params)
            total_count = cursor.fetchone()[0]
            
            # 获取分页数据
            offset = (page - 1) * page_size
            list_sql = f"""
                SELECT * FROM companies 
                {where_clause}
                ORDER BY name ASC
                LIMIT %s OFFSET %s
            """
            
            params.extend([page_size, offset])
            cursor.execute(list_sql, params)
            
            companies = [dict(company) for company in cursor.fetchall()]
            
            # 计算分页信息
            total_pages = (total_count + page_size - 1) // page_size
            
            return {
                'companies': companies,
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total_count': total_count,
                    'total_pages': total_pages,
                    'has_next': page < total_pages,
                    'has_prev': page > 1
                },
                'filters_applied': filters or {}
            }
            
        except Exception as e:
            print(f"✗ 获取账户公司失败: {str(e)}")
            return {
                'companies': [],
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total_count': 0,
                    'total_pages': 0,
                    'has_next': False,
                    'has_prev': False
                },
                'filters_applied': filters or {},
                'error': str(e)
            }
            
        finally:
            if conn:
                conn.close()
    
    def get_project_users(
        self,
        project_id: str,
        filters: Dict = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """
        获取项目用户列表
        
        Args:
            project_id: 项目ID
            filters: 过滤条件
            page: 页码
            page_size: 每页大小
            
        Returns:
            项目用户列表和分页信息
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # 构建查询条件
            where_conditions = ["pu.project_id = %s"]
            params = [project_id]
            
            if filters:
                if filters.get('status'):
                    where_conditions.append("pu.status = %s")
                    params.append(filters['status'])
                
                if filters.get('company_id'):
                    where_conditions.append("pu.project_company_id = %s")
                    params.append(filters['company_id'])
                
                if filters.get('search'):
                    search_term = f"%{filters['search']}%"
                    where_conditions.append("(u.name ILIKE %s OR u.email ILIKE %s)")
                    params.extend([search_term, search_term])
            
            where_clause = f"WHERE {' AND '.join(where_conditions)}"
            
            # 获取总数
            count_sql = f"""
                SELECT COUNT(*) 
                FROM project_users pu
                JOIN users u ON pu.user_id = u.user_id
                {where_clause}
            """
            cursor.execute(count_sql, params)
            total_count = cursor.fetchone()[0]
            
            # 获取分页数据
            offset = (page - 1) * page_size
            list_sql = f"""
                SELECT 
                    pu.*,
                    u.name as user_name,
                    u.email as user_email,
                    u.job_title,
                    u.company_name as account_company_name
                FROM project_users pu
                JOIN users u ON pu.user_id = u.user_id
                {where_clause}
                ORDER BY u.name ASC
                LIMIT %s OFFSET %s
            """
            
            params.extend([page_size, offset])
            cursor.execute(list_sql, params)
            
            project_users = []
            for row in cursor.fetchall():
                user_dict = dict(row)
                
                # 解析JSON字段
                json_fields = ['access_levels', 'role_ids', 'roles', 'products']
                for field in json_fields:
                    if user_dict.get(field):
                        try:
                            user_dict[field] = json.loads(user_dict[field])
                        except:
                            user_dict[field] = {} if field == 'access_levels' else []
                
                project_users.append(user_dict)
            
            # 计算分页信息
            total_pages = (total_count + page_size - 1) // page_size
            
            return {
                'project_users': project_users,
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total_count': total_count,
                    'total_pages': total_pages,
                    'has_next': page < total_pages,
                    'has_prev': page > 1
                },
                'filters_applied': filters or {}
            }
            
        except Exception as e:
            print(f"✗ 获取项目用户失败: {str(e)}")
            return {
                'project_users': [],
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total_count': 0,
                    'total_pages': 0,
                    'has_next': False,
                    'has_prev': False
                },
                'filters_applied': filters or {},
                'error': str(e)
            }
            
        finally:
            if conn:
                conn.close()
    
    def get_account_statistics(self, account_id: str) -> Dict[str, Any]:
        """
        获取账户统计信息
        
        Args:
            account_id: 账户ID
            
        Returns:
            统计信息
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # 获取基本统计
            cursor.execute("""
                SELECT 
                    COUNT(DISTINCT u.user_id) as total_users,
                    COUNT(DISTINCT u.user_id) FILTER (WHERE u.status = 'active') as active_users,
                    COUNT(DISTINCT u.user_id) FILTER (WHERE u.status = 'pending') as pending_users,
                    COUNT(DISTINCT c.company_id) as total_companies,
                    COUNT(DISTINCT u.company_id) as companies_with_users
                FROM users u
                LEFT JOIN companies c ON u.account_id = c.account_id
                WHERE u.account_id = %s
            """, [account_id])
            
            basic_stats = dict(cursor.fetchone()) if cursor.rowcount > 0 else {}
            
            # 获取角色统计
            cursor.execute("""
                SELECT 
                    COUNT(DISTINCT (jsonb_array_elements(pu.roles)->>'name')) as unique_roles,
                    COUNT(*) as total_role_assignments
                FROM project_users pu
                JOIN users u ON pu.user_id = u.user_id
                WHERE u.account_id = %s
                AND jsonb_array_length(pu.roles) > 0
            """, [account_id])
            
            role_stats = dict(cursor.fetchone()) if cursor.rowcount > 0 else {}
            
            # 获取公司分布
            cursor.execute("""
                SELECT 
                    c.name as company_name,
                    c.trade,
                    COUNT(u.user_id) as user_count
                FROM companies c
                LEFT JOIN users u ON c.company_id = u.company_id
                WHERE c.account_id = %s
                GROUP BY c.company_id, c.name, c.trade
                ORDER BY user_count DESC
                LIMIT 10
            """, [account_id])
            
            top_companies = [dict(row) for row in cursor.fetchall()]
            
            # 获取最近活动
            cursor.execute("""
                SELECT 
                    u.name as user_name,
                    u.last_sign_in,
                    u.last_synced_at
                FROM users u
                WHERE u.account_id = %s
                AND u.last_sign_in IS NOT NULL
                ORDER BY u.last_sign_in DESC
                LIMIT 5
            """, [account_id])
            
            recent_activity = [dict(row) for row in cursor.fetchall()]
            
            return {
                'account_id': account_id,
                'basic_statistics': basic_stats,
                'role_statistics': role_stats,
                'top_companies': top_companies,
                'recent_activity': recent_activity,
                'generated_at': datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            print(f"✗ 获取账户统计失败: {str(e)}")
            return {
                'account_id': account_id,
                'error': str(e),
                'generated_at': datetime.now(timezone.utc).isoformat()
            }
            
        finally:
            if conn:
                conn.close()

# 创建全局实例
if NeonConfig is not None and AccountDataSyncManager is not None and psycopg2 is not None:
    account_manager = AccountManager()
else:
    account_manager = None
    print("Warning: AccountManager not initialized due to missing database dependencies")

# ============================================================================
# API端点
# ============================================================================

@account_bp.route('/api/account/<account_id>/roles-summary')
def get_account_roles_summary(account_id):
    """
    获取账户角色汇总（类似AccountRolesList.vue）
    """
    try:
        result = account_manager.get_account_roles_summary(account_id)
        
        return jsonify({
            "status": "success",
            "data": result
        })
    except Exception as e:
        print(f"✗ 获取角色汇总失败: {str(e)}")
        return jsonify({
            "error": f"获取角色汇总失败: {str(e)}",
            "status": "error"
        }), 500

@account_bp.route('/api/account/<account_id>/users')
def get_account_users(account_id):
    """
    获取账户用户列表
    """
    try:
        # 获取查询参数
        filters = {}
        if request.args.get('status'):
            filters['status'] = request.args.get('status')
        if request.args.get('role'):
            filters['role'] = request.args.get('role')
        if request.args.get('company_id'):
            filters['company_id'] = request.args.get('company_id')
        if request.args.get('search'):
            filters['search'] = request.args.get('search')
        
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        
        result = account_manager.get_account_users(account_id, filters, page, page_size)
        
        return jsonify({
            "status": "success",
            "data": result
        })
    except Exception as e:
        print(f"✗ 获取账户用户失败: {str(e)}")
        return jsonify({
            "error": f"获取账户用户失败: {str(e)}",
            "status": "error"
        }), 500

@account_bp.route('/api/account/<account_id>/companies')
def get_account_companies(account_id):
    """
    获取账户公司列表
    """
    try:
        # 获取查询参数
        project_id = request.args.get('project_id')
        filters = {}
        if request.args.get('trade'):
            filters['trade'] = request.args.get('trade')
        if request.args.get('country'):
            filters['country'] = request.args.get('country')
        if request.args.get('search'):
            filters['search'] = request.args.get('search')
        
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        
        result = account_manager.get_account_companies(
            account_id, project_id, filters, page, page_size
        )
        
        return jsonify({
            "status": "success",
            "data": result
        })
        
    except Exception as e:
        print(f"✗ 获取账户公司失败: {str(e)}")
        return jsonify({
            "error": f"获取账户公司失败: {str(e)}",
            "status": "error"
        }), 500

@account_bp.route('/api/projects/<project_id>/users')
def get_project_users(project_id):
    """
    获取项目用户列表
    """
    try:
        # 获取查询参数
        filters = {}
        if request.args.get('status'):
            filters['status'] = request.args.get('status')
        if request.args.get('company_id'):
            filters['company_id'] = request.args.get('company_id')
        if request.args.get('search'):
            filters['search'] = request.args.get('search')
        
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        
        result = account_manager.get_project_users(project_id, filters, page, page_size)
        
        return jsonify({
            "status": "success",
            "data": result
        })
    except Exception as e:
        print(f"✗ 获取项目用户失败: {str(e)}")
        return jsonify({
            "error": f"获取项目用户失败: {str(e)}",
            "status": "error"
        }), 500

@account_bp.route('/api/account/<account_id>/statistics')
def get_account_statistics(account_id):
    """
    获取账户统计信息
    """
    try:
        result = account_manager.get_account_statistics(account_id)
        
        return jsonify({
            "status": "success",
            "data": result
        })
    except Exception as e:
        print(f"✗ 获取账户统计失败: {str(e)}")
        return jsonify({
            "error": f"获取账户统计失败: {str(e)}",
            "status": "error"
        }), 500

@account_bp.route('/api/account/<account_id>/sync', methods=['POST'])
def sync_account_data(account_id):
    """
    同步账户数据
    """
    try:
        data = request.get_json()
        project_ids = data.get('project_ids', [])
        
        access_token = utils.get_access_token()
        if not access_token:
            return jsonify({
                "error": "未找到访问令牌，请先进行认证",
                "status": "unauthorized"
            }), 401
    
        print(f"🔄 开始同步账户数据: {account_id}")
        start_time = time.time()
        
        # 执行同步（这里需要异步处理，简化为同步调用）
        import asyncio
        from database_sql.account_sync import sync_account_data
        
        result = asyncio.run(sync_account_data(
            account_id=account_id,
            project_ids=project_ids,
            access_token=access_token,
            show_progress=True
        ))
        
        elapsed_time = time.time() - start_time
        result['elapsed_time'] = f"{elapsed_time:.2f}秒"
        
        print(f"✓ 账户数据同步完成，耗时: {elapsed_time:.2f}秒")
        
        return jsonify({
            "status": "success",
            "message": "账户数据同步完成",
            "data": result
        })
        
    except Exception as e:
        print(f"✗ 账户数据同步失败: {str(e)}")
        return jsonify({
            "error": f"账户数据同步失败: {str(e)}",
            "status": "error"
        }), 500
