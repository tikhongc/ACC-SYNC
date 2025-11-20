# -*- coding: utf-8 -*-
"""
账户管理API模块
Account Management API Module

提供用户、角色、公司的查询接口
Provides query interfaces for users, roles, and companies
"""

import json
import psycopg2
import psycopg2.extras
from flask import Blueprint, jsonify, request
from typing import Dict, List, Optional, Any
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from database_sql.neon_config import NeonConfig

# 创建Blueprint - 使用唯一的名称避免与原有account_bp冲突
account_bp = Blueprint('account_cde', __name__)


class AccountManager:
    """账户管理器类 - Account Manager Class"""

    def __init__(self):
        """初始化数据库配置"""
        self.neon_config = NeonConfig()
        self.db_params = self.neon_config.get_db_params()

    def get_connection(self):
        """获取数据库连接 - Get database connection"""
        return psycopg2.connect(**self.db_params)

    def _parse_json_fields(self, record: Dict[str, Any], json_fields: List[str]) -> Dict[str, Any]:
        """
        解析JSON字段
        Parse JSON fields in the record

        Args:
            record: 数据库记录 - Database record
            json_fields: 需要解析的JSON字段列表 - List of JSON fields to parse

        Returns:
            解析后的记录 - Parsed record
        """
        for field in json_fields:
            if record.get(field):
                try:
                    if isinstance(record[field], str):
                        record[field] = json.loads(record[field])
                except (json.JSONDecodeError, TypeError):
                    record[field] = [] if field in ['account_roles', 'role_ids'] else {}
            else:
                record[field] = [] if field in ['account_roles', 'role_ids'] else {}
        return record

    def get_users_list(self,
                       page: int = 1,
                       page_size: int = 20,
                       status: Optional[str] = None,
                       company_id: Optional[str] = None,
                       role_id: Optional[str] = None,
                       account_id: Optional[str] = None) -> Dict[str, Any]:
        """
        获取用户列表
        Get users list with pagination and filters

        Args:
            page: 页码 - Page number
            page_size: 每页数量 - Items per page
            status: 用户状态过滤 - User status filter
            company_id: 公司ID过滤 - Company ID filter
            role_id: 角色ID过滤 - Role ID filter
            account_id: 账户ID过滤 - Account ID filter

        Returns:
            用户列表和分页信息 - Users list with pagination info
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # 构建查询条件 - Build query conditions
            conditions = []
            params = []

            if status:
                conditions.append("u.status = %s")
                params.append(status)

            if company_id:
                conditions.append("u.company_id = %s")
                params.append(company_id)

            if role_id:
                conditions.append("(u.default_role_id = %s OR u.account_roles @> %s::jsonb)")
                params.append(role_id)
                params.append(json.dumps([{"id": role_id}]))

            if account_id:
                conditions.append("u.account_id = %s")
                params.append(account_id)

            where_clause = ""
            if conditions:
                where_clause = "WHERE " + " AND ".join(conditions)

            # 查询总数 - Count total
            count_sql = f"""
                SELECT COUNT(*) as total
                FROM users u
                {where_clause}
            """
            cursor.execute(count_sql, params)
            total_count = cursor.fetchone()['total']

            # 计算分页 - Calculate pagination
            offset = (page - 1) * page_size
            total_pages = (total_count + page_size - 1) // page_size

            # 查询用户列表 - Query users list
            sql = f"""
                SELECT
                    u.user_id,
                    u.account_id,
                    u.email,
                    u.name,
                    u.status,
                    u.company_id,
                    u.default_role_id,
                    u.account_roles,
                    u.created_at,
                    u.updated_at,
                    c.name as company_name,
                    c.trade as company_trade,
                    c.country as company_country,
                    r.name as default_role_name,
                    r.description as default_role_description,
                    a.name as account_name,
                    pu.autodesk_id
                FROM users u
                LEFT JOIN companies c ON u.company_id = c.company_id
                LEFT JOIN roles r ON u.default_role_id = r.role_id
                LEFT JOIN accounts a ON u.account_id = a.account_id
                LEFT JOIN LATERAL (
                    SELECT autodesk_id
                    FROM project_users
                    WHERE user_id = u.user_id
                    LIMIT 1
                ) pu ON true
                {where_clause}
                ORDER BY u.created_at DESC
                LIMIT %s OFFSET %s
            """

            cursor.execute(sql, params + [page_size, offset])
            users = cursor.fetchall()

            # 解析JSON字段 - Parse JSON fields
            users_list = []
            for user in users:
                user_dict = dict(user)
                user_dict = self._parse_json_fields(user_dict, ['account_roles'])

                # 格式化时间戳 - Format timestamps
                if user_dict.get('created_at'):
                    user_dict['created_at'] = user_dict['created_at'].isoformat()
                if user_dict.get('updated_at'):
                    user_dict['updated_at'] = user_dict['updated_at'].isoformat()

                users_list.append(user_dict)

            print(f"[DEBUG] Got {len(users_list)} users, total: {total_count}")

            return {
                'users': users_list,
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total_count': total_count,
                    'total_pages': total_pages,
                    'has_next': page < total_pages,
                    'has_prev': page > 1
                },
                'filters_applied': {
                    'status': status,
                    'company_id': company_id,
                    'role_id': role_id,
                    'account_id': account_id
                }
            }

        except Exception as e:
            print(f"[ERROR] Failed to get users list: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()

    def get_roles_with_users(self,
                            page: int = 1,
                            page_size: int = 20,
                            account_id: Optional[str] = None) -> Dict[str, Any]:
        """
        获取角色列表，每个角色包含关联的用户
        Get roles list, each role contains associated users

        Args:
            page: 页码 - Page number
            page_size: 每页数量 - Items per page
            account_id: 账户ID过滤 - Account ID filter

        Returns:
            角色列表和分页信息 - Roles list with pagination info
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # 构建查询条件 - Build query conditions
            where_clause = ""
            params = []

            if account_id:
                where_clause = "WHERE r.account_id = %s OR r.account_id IS NULL"
                params.append(account_id)

            # 查询总数 - Count total
            count_sql = f"""
                SELECT COUNT(*) as total
                FROM roles r
                {where_clause}
            """
            cursor.execute(count_sql, params)
            total_count = cursor.fetchone()['total']

            # 计算分页 - Calculate pagination
            offset = (page - 1) * page_size
            total_pages = (total_count + page_size - 1) // page_size

            # 查询角色列表 - Query roles list
            sql = f"""
                SELECT
                    r.role_id,
                    r.account_id,
                    r.name,
                    r.description,
                    r.created_at,
                    r.updated_at
                FROM roles r
                {where_clause}
                ORDER BY r.created_at DESC
                LIMIT %s OFFSET %s
            """

            cursor.execute(sql, params + [page_size, offset])
            roles = cursor.fetchall()

            # 为每个角色查询关联的用户 - Query associated users for each role
            roles_list = []
            for role in roles:
                role_dict = dict(role)

                # 格式化时间戳 - Format timestamps
                if role_dict.get('created_at'):
                    role_dict['created_at'] = role_dict['created_at'].isoformat()
                if role_dict.get('updated_at'):
                    role_dict['updated_at'] = role_dict['updated_at'].isoformat()

                # 查询使用此角色的用户 - Query users with this role
                # 包括：1) default_role_id匹配的用户  2) account_roles中包含此角色的用户
                users_sql = """
                    SELECT DISTINCT
                        u.user_id,
                        u.account_id,
                        u.email,
                        u.name,
                        u.status,
                        u.company_id,
                        c.name as company_name,
                        u.created_at,
                        u.updated_at,
                        pu.autodesk_id
                    FROM users u
                    LEFT JOIN companies c ON u.company_id = c.company_id
                    LEFT JOIN LATERAL (
                        SELECT autodesk_id
                        FROM project_users
                        WHERE user_id = u.user_id
                        LIMIT 1
                    ) pu ON true
                    WHERE u.default_role_id = %s
                       OR u.account_roles::text LIKE %s
                    ORDER BY u.name
                """

                role_id = role_dict['role_id']
                print(f"[DEBUG] Searching users for role_id: {role_id}")

                cursor.execute(users_sql, [
                    role_id,
                    f'%"{role_id}"%'
                ])
                users = cursor.fetchall()

                print(f"[DEBUG] Found {len(users)} users for role: {role_dict['name']} (role_id: {role_id})")

                # 格式化用户数据 - Format user data
                users_list = []
                for user in users:
                    user_dict = dict(user)
                    if user_dict.get('created_at'):
                        user_dict['created_at'] = user_dict['created_at'].isoformat()
                    if user_dict.get('updated_at'):
                        user_dict['updated_at'] = user_dict['updated_at'].isoformat()
                    users_list.append(user_dict)

                role_dict['users'] = users_list
                role_dict['users_count'] = len(users_list)

                roles_list.append(role_dict)

            print(f"[DEBUG] Got {len(roles_list)} roles, total: {total_count}")

            return {
                'roles': roles_list,
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total_count': total_count,
                    'total_pages': total_pages,
                    'has_next': page < total_pages,
                    'has_prev': page > 1
                },
                'filters_applied': {
                    'account_id': account_id
                }
            }

        except Exception as e:
            print(f"[ERROR] Failed to get roles list: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()

    def get_companies_with_users(self,
                                 page: int = 1,
                                 page_size: int = 20,
                                 account_id: Optional[str] = None,
                                 trade: Optional[str] = None) -> Dict[str, Any]:
        """
        获取公司列表，每个公司包含关联的用户
        Get companies list, each company contains associated users

        Args:
            page: 页码 - Page number
            page_size: 每页数量 - Items per page
            account_id: 账户ID过滤 - Account ID filter
            trade: 行业类型过滤 - Trade type filter

        Returns:
            公司列表和分页信息 - Companies list with pagination info
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # 构建查询条件 - Build query conditions
            conditions = []
            params = []

            if account_id:
                conditions.append("c.account_id = %s")
                params.append(account_id)

            if trade:
                conditions.append("c.trade = %s")
                params.append(trade)

            where_clause = ""
            if conditions:
                where_clause = "WHERE " + " AND ".join(conditions)

            # 查询总数 - Count total
            count_sql = f"""
                SELECT COUNT(*) as total
                FROM companies c
                {where_clause}
            """
            cursor.execute(count_sql, params)
            total_count = cursor.fetchone()['total']

            # 计算分页 - Calculate pagination
            offset = (page - 1) * page_size
            total_pages = (total_count + page_size - 1) // page_size

            # 查询公司列表 - Query companies list
            sql = f"""
                SELECT
                    c.company_id,
                    c.account_id,
                    c.name,
                    c.trade,
                    c.country,
                    c.created_at,
                    c.updated_at,
                    a.name as account_name
                FROM companies c
                LEFT JOIN accounts a ON c.account_id = a.account_id
                {where_clause}
                ORDER BY c.created_at DESC
                LIMIT %s OFFSET %s
            """

            cursor.execute(sql, params + [page_size, offset])
            companies = cursor.fetchall()

            # 为每个公司查询关联的用户 - Query associated users for each company
            companies_list = []
            for company in companies:
                company_dict = dict(company)

                # 格式化时间戳 - Format timestamps
                if company_dict.get('created_at'):
                    company_dict['created_at'] = company_dict['created_at'].isoformat()
                if company_dict.get('updated_at'):
                    company_dict['updated_at'] = company_dict['updated_at'].isoformat()

                # 查询属于此公司的用户 - Query users belonging to this company
                users_sql = """
                    SELECT
                        u.user_id,
                        u.account_id,
                        u.email,
                        u.name,
                        u.status,
                        u.default_role_id,
                        u.account_roles,
                        r.name as default_role_name,
                        u.created_at,
                        u.updated_at,
                        pu.autodesk_id
                    FROM users u
                    LEFT JOIN roles r ON u.default_role_id = r.role_id
                    LEFT JOIN LATERAL (
                        SELECT autodesk_id
                        FROM project_users
                        WHERE user_id = u.user_id
                        LIMIT 1
                    ) pu ON true
                    WHERE u.company_id = %s
                    ORDER BY u.name
                """

                cursor.execute(users_sql, [company_dict['company_id']])
                users = cursor.fetchall()

                # 格式化用户数据 - Format user data
                users_list = []
                for user in users:
                    user_dict = dict(user)
                    user_dict = self._parse_json_fields(user_dict, ['account_roles'])

                    if user_dict.get('created_at'):
                        user_dict['created_at'] = user_dict['created_at'].isoformat()
                    if user_dict.get('updated_at'):
                        user_dict['updated_at'] = user_dict['updated_at'].isoformat()
                    users_list.append(user_dict)

                company_dict['users'] = users_list
                company_dict['users_count'] = len(users_list)

                companies_list.append(company_dict)

            print(f"[DEBUG] Got {len(companies_list)} companies, total: {total_count}")

            return {
                'companies': companies_list,
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total_count': total_count,
                    'total_pages': total_pages,
                    'has_next': page < total_pages,
                    'has_prev': page > 1
                },
                'filters_applied': {
                    'account_id': account_id,
                    'trade': trade
                }
            }

        except Exception as e:
            print(f"[ERROR] Failed to get companies list: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()


# 创建全局管理器实例 - Create global manager instance
account_manager = AccountManager()


# ============================================================================
# API路由定义 - API Route Definitions
# ============================================================================

@account_bp.route('/api/accounts/users', methods=['GET'])
def get_users():
    """
    获取用户列表API
    Get users list API

    Query Parameters:
        - page: 页码 (default: 1)
        - page_size: 每页数量 (default: 20)
        - status: 用户状态过滤 (active/inactive/pending)
        - company_id: 公司ID过滤
        - role_id: 角色ID过滤
        - account_id: 账户ID过滤

    Returns:
        JSON response with users list and pagination info
    """
    try:
        # 获取查询参数 - Get query parameters
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        status = request.args.get('status')
        company_id = request.args.get('company_id')
        role_id = request.args.get('role_id')
        account_id = request.args.get('account_id')

        # 参数验证 - Parameter validation
        if page < 1:
            return jsonify({
                "error": "Page number must be >= 1",
                "status": "bad_request"
            }), 400

        if page_size < 1 or page_size > 100:
            return jsonify({
                "error": "Page size must be between 1 and 100",
                "status": "bad_request"
            }), 400

        # 调用管理器方法 - Call manager method
        result = account_manager.get_users_list(
            page=page,
            page_size=page_size,
            status=status,
            company_id=company_id,
            role_id=role_id,
            account_id=account_id
        )

        return jsonify({
            "status": "success",
            "data": result
        }), 200

    except Exception as e:
        print(f"[ERROR] Get users failed: {str(e)}")
        return jsonify({
            "error": f"Failed to get users: {str(e)}",
            "status": "error"
        }), 500


@account_bp.route('/api/accounts/roles', methods=['GET'])
def get_roles():
    """
    获取角色列表API（包含关联用户）
    Get roles list API (with associated users)

    Query Parameters:
        - page: 页码 (default: 1)
        - page_size: 每页数量 (default: 20)
        - account_id: 账户ID过滤

    Returns:
        JSON response with roles list (each role contains users array) and pagination info
    """
    try:
        # 获取查询参数 - Get query parameters
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        account_id = request.args.get('account_id')

        # 参数验证 - Parameter validation
        if page < 1:
            return jsonify({
                "error": "Page number must be >= 1",
                "status": "bad_request"
            }), 400

        if page_size < 1 or page_size > 100:
            return jsonify({
                "error": "Page size must be between 1 and 100",
                "status": "bad_request"
            }), 400

        # 调用管理器方法 - Call manager method
        result = account_manager.get_roles_with_users(
            page=page,
            page_size=page_size,
            account_id=account_id
        )

        return jsonify({
            "status": "success",
            "data": result
        }), 200

    except Exception as e:
        print(f"[ERROR] Get roles failed: {str(e)}")
        return jsonify({
            "error": f"Failed to get roles: {str(e)}",
            "status": "error"
        }), 500


@account_bp.route('/api/accounts/companies', methods=['GET'])
def get_companies():
    """
    获取公司列表API（包含关联用户）
    Get companies list API (with associated users)

    Query Parameters:
        - page: 页码 (default: 1)
        - page_size: 每页数量 (default: 20)
        - account_id: 账户ID过滤
        - trade: 行业类型过滤

    Returns:
        JSON response with companies list (each company contains users array) and pagination info
    """
    try:
        # 获取查询参数 - Get query parameters
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 20, type=int)
        account_id = request.args.get('account_id')
        trade = request.args.get('trade')

        # 参数验证 - Parameter validation
        if page < 1:
            return jsonify({
                "error": "Page number must be >= 1",
                "status": "bad_request"
            }), 400

        if page_size < 1 or page_size > 100:
            return jsonify({
                "error": "Page size must be between 1 and 100",
                "status": "bad_request"
            }), 400

        # 调用管理器方法 - Call manager method
        result = account_manager.get_companies_with_users(
            page=page,
            page_size=page_size,
            account_id=account_id,
            trade=trade
        )

        return jsonify({
            "status": "success",
            "data": result
        }), 200

    except Exception as e:
        print(f"[ERROR] Get companies failed: {str(e)}")
        return jsonify({
            "error": f"Failed to get companies: {str(e)}",
            "status": "error"
        }), 500


# ============================================================================
# 模块说明 - Module Info
# ============================================================================

"""
API端点总结 - API Endpoints Summary:

1. GET /api/accounts/users
   - 返回用户列表 - Returns users list
   - 支持分页和多种过滤条件 - Supports pagination and multiple filters
   - 包含公司和角色信息 - Includes company and role information

2. GET /api/accounts/roles
   - 返回角色列表 - Returns roles list
   - 每个角色包含关联的用户数组 - Each role contains associated users array
   - 支持分页 - Supports pagination

3. GET /api/accounts/companies
   - 返回公司列表 - Returns companies list
   - 每个公司包含关联的用户数组 - Each company contains associated users array
   - 支持分页和过滤 - Supports pagination and filters

所有API遵循统一的响应格式：
All APIs follow unified response format:
{
    "status": "success",
    "data": {
        "items": [...],
        "pagination": {...},
        "filters_applied": {...}
    }
}
"""
