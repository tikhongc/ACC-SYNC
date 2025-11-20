# -*- coding: utf-8 -*-
"""
Transmittal Management API
提供传输单管理的后端 API 接口

APIs:
1. GET  /api/transmittals/<project_id>/list - 获取传输单列表
2. GET  /api/transmittals/<transmittal_id>/documents - 获取传输单文档列表
3. GET  /api/transmittals/<transmittal_id>/recipients - 获取传输单接收者列表
4. POST /api/transmittals/<transmittal_id>/mark-viewed - 标记用户已查看
5. POST /api/transmittals/<transmittal_id>/mark-downloaded - 标记用户已下载
6. POST /api/transmittals/<transmittal_id>/download-zip - 打包下载文件 (TODO)
"""

import sys
import os
from functools import wraps
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
import tempfile
import zipfile
import requests
import shutil
from pathlib import Path
import time
import threading
import atexit

# Windows 环境 UTF-8 编码设置
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from flask import Blueprint, jsonify, request, send_file
import psycopg2
import psycopg2.extras
from psycopg2.extras import RealDictCursor

# 导入数据库配置和数据访问层
from database_sql.neon_config import NeonConfig
from database_sql.transmittal_data_access import TransmittalDataAccess

# 导入认证工具和下载管理器
import utils
from api_modules.urn_download_simple import URNDownloadManager

# 创建 Blueprint
transmittal_bp = Blueprint('transmittal', __name__, url_prefix='/api/transmittals')


# ========================================
# ZIP 文件清理工具
# ========================================

class ZipFileCleanup:
    """ZIP 文件延迟清理管理器"""

    def __init__(self):
        self.pending_files = []
        self.cleanup_delay = 300  # 5分钟后清理
        atexit.register(self.cleanup_all)

    def schedule_cleanup(self, file_path: str, delay: int = None):
        """
        调度文件清理任务

        Args:
            file_path: 要清理的文件路径
            delay: 延迟时间(秒)，默认使用 cleanup_delay
        """
        if delay is None:
            delay = self.cleanup_delay

        self.pending_files.append(file_path)

        def cleanup_task():
            time.sleep(delay)
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"[Cleanup] Removed ZIP file: {file_path}")
                    if file_path in self.pending_files:
                        self.pending_files.remove(file_path)
            except Exception as e:
                print(f"[Cleanup] Error removing file {file_path}: {e}")

        # 启动后台清理线程
        cleanup_thread = threading.Thread(target=cleanup_task, daemon=True)
        cleanup_thread.start()
        print(f"[Cleanup] Scheduled cleanup for: {file_path} (in {delay}s)")

    def cleanup_all(self):
        """立即清理所有待处理的文件"""
        for file_path in list(self.pending_files):
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"[Cleanup] Emergency cleanup: {file_path}")
            except Exception as e:
                print(f"[Cleanup] Error in emergency cleanup: {e}")
        self.pending_files.clear()


# 全局清理管理器实例
zip_cleanup = ZipFileCleanup()


# ========================================
# 异常处理装饰器
# ========================================

def handle_exceptions(f):
    """统一异常处理装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except psycopg2.Error as e:
            return jsonify({
                'success': False,
                'error': f'Database operation failed: {str(e)}',
                'error_type': 'database_error'
            }), 500
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': f'Invalid input: {str(e)}',
                'error_type': 'validation_error'
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Internal server error: {str(e)}',
                'error_type': 'internal_error'
            }), 500
    return decorated_function


# ========================================
# Transmittal Manager 类
# ========================================

class TransmittalManager:
    """传输单管理器 - 封装业务逻辑"""

    def __init__(self):
        self.neon_config = NeonConfig()
        self.db_params = self.neon_config.get_db_params()
        self.urn_manager = URNDownloadManager()

    def get_connection(self):
        """获取数据库连接"""
        return psycopg2.connect(**self.db_params)

    def get_transmittals_list(self, project_id: str, limit: int = 100, offset: int = 0) -> Dict[str, Any]:
        """
        获取项目的传输单列表

        Args:
            project_id: 项目ID (支持 b.xxx 格式)
            limit: 每页数量
            offset: 偏移量

        Returns:
            {
                'success': bool,
                'data': List[Dict],
                'total': int,
                'limit': int,
                'offset': int
            }
        """
        conn = None
        cursor = None
        try:
            # 清理 project_id (移除 b. 前缀如果存在)
            clean_project_id = project_id[2:] if project_id.startswith('b.') else project_id

            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            # 查询总数
            count_sql = """
                SELECT COUNT(*) as total
                FROM transmittals_workflow_transmittals
                WHERE bim360_project_id = %s::uuid
            """
            cursor.execute(count_sql, (clean_project_id,))
            total = cursor.fetchone()['total']

            # 查询数据并关联统计信息
            query_sql = """
                SELECT
                    t.id,
                    t.bim360_account_id,
                    t.bim360_project_id,
                    t.sequence_id,
                    t.title,
                    t.status,
                    t.docs_count,
                    t.create_user_id,
                    t.create_user_name,
                    t.create_user_company_id,
                    t.create_user_company_name,
                    t.created_at,
                    t.updated_at,
                    COUNT(DISTINCT r.id) + COUNT(DISTINCT n.id) AS recipient_count
                FROM transmittals_workflow_transmittals t
                LEFT JOIN transmittals_transmittal_recipients r ON t.id = r.workflow_transmittal_id
                LEFT JOIN transmittals_transmittal_non_members n ON t.id = n.workflow_transmittal_id
                WHERE t.bim360_project_id = %s::uuid
                GROUP BY t.id, t.bim360_account_id, t.bim360_project_id, t.sequence_id,
                         t.title, t.status, t.docs_count, t.create_user_id, t.create_user_name,
                         t.create_user_company_id, t.create_user_company_name, t.created_at, t.updated_at
                ORDER BY t.sequence_id DESC
                LIMIT %s OFFSET %s
            """
            cursor.execute(query_sql, (clean_project_id, limit, offset))
            transmittals = cursor.fetchall()

            # 状态码映射
            STATUS_MAP = {
                1: 'DRAFT',
                2: 'SENT',
                3: 'COMPLETED',
                4: 'CANCELLED'
            }

            # 转换为可序列化的格式，并映射字段名
            result = []
            for t in transmittals:
                item = dict(t)

                # 转换 UUID 为字符串
                for key in ['id', 'bim360_account_id', 'bim360_project_id', 'create_user_id', 'create_user_company_id']:
                    if item.get(key):
                        item[key] = str(item[key])

                # 转换时间戳为 ISO 格式
                for key in ['created_at', 'updated_at']:
                    if item.get(key):
                        item[key] = item[key].isoformat()

                # 映射字段名以匹配前端期望
                mapped_item = {
                    'id': item['id'],
                    'transmittal_number': f"T-{item['sequence_id']:04d}",  # 格式化为 T-0001
                    'subject': item['title'],
                    'status': STATUS_MAP.get(item['status'], 'UNKNOWN'),  # 转换状态码为字符串
                    'document_count': item['docs_count'],
                    'recipient_count': item.get('recipient_count', 0),
                    'due_date': None,  # 数据库暂无此字段
                    'created_by_name': item['create_user_name'],
                    'created_by_email': None,  # 数据库暂无此字段
                    'created_at': item['created_at'],
                    'updated_at': item['updated_at'],
                    # 保留原始字段供详情页使用
                    'sequence_id': item['sequence_id'],
                    'bim360_project_id': item['bim360_project_id'],
                }

                result.append(mapped_item)

            return {
                'success': True,
                'data': result,
                'total': total,
                'limit': limit,
                'offset': offset
            }

        except Exception as e:
            raise Exception(f"Failed to get transmittals list: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_transmittal_documents(self, transmittal_id: str) -> Dict[str, Any]:
        """
        获取指定传输单的文档列表

        Args:
            transmittal_id: 传输单ID (UUID)

        Returns:
            {
                'success': bool,
                'transmittal_id': str,
                'data': List[Dict],
                'count': int
            }
        """
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            query_sql = """
                SELECT
                    id,
                    workflow_transmittal_id,
                    urn,
                    file_name,
                    version_number,
                    revision_number,
                    parent_folder_urn,
                    last_modified_time,
                    last_modified_user_id,
                    last_modified_user_name
                FROM transmittals_transmittal_documents
                WHERE workflow_transmittal_id = %s::uuid
                ORDER BY file_name
            """
            cursor.execute(query_sql, (transmittal_id,))
            documents = cursor.fetchall()

            # 转换为可序列化的格式，并映射字段名
            result = []
            for doc in documents:
                item = dict(doc)
                # 转换 UUID 为字符串
                for key in ['id', 'workflow_transmittal_id', 'last_modified_user_id']:
                    if item.get(key):
                        item[key] = str(item[key])
                # 转换时间戳为 ISO 格式
                if item.get('last_modified_time'):
                    item['last_modified_time'] = item['last_modified_time'].isoformat()

                # 映射字段名以匹配前端期望
                mapped_item = {
                    'id': item['id'],
                    'display_name': item['file_name'],
                    'version_number': item['version_number'],
                    'size': None,  # 数据库暂无此字段
                    'last_modified_time': item['last_modified_time'],
                    # 保留原始字段
                    'urn': item['urn'],
                    'file_name': item['file_name'],
                    'revision_number': item['revision_number'],
                    'parent_folder_urn': item['parent_folder_urn'],
                    'last_modified_user_id': item.get('last_modified_user_id'),
                    'last_modified_user_name': item.get('last_modified_user_name'),
                }
                result.append(mapped_item)

            return {
                'success': True,
                'transmittal_id': transmittal_id,
                'data': result,
                'count': len(result)
            }

        except Exception as e:
            raise Exception(f"Failed to get transmittal documents: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_transmittal_recipients(self, transmittal_id: str) -> Dict[str, Any]:
        """
        获取指定传输单的接收者列表（包括项目成员和外部接收者）

        Args:
            transmittal_id: 传输单ID (UUID)

        Returns:
            {
                'success': bool,
                'transmittal_id': str,
                'data': {
                    'members': List[Dict],     # 项目成员接收者
                    'non_members': List[Dict]  # 外部接收者
                },
                'total_count': int
            }
        """
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            # 查询项目成员接收者
            members_sql = """
                SELECT
                    id,
                    workflow_transmittal_id,
                    bim360_account_id,
                    bim360_project_id,
                    user_id,
                    user_name,
                    email,
                    company_name,
                    viewed_at,
                    downloaded_at,
                    created_at,
                    updated_at
                FROM transmittals_transmittal_recipients
                WHERE workflow_transmittal_id = %s::uuid
                ORDER BY user_name
            """
            cursor.execute(members_sql, (transmittal_id,))
            members = cursor.fetchall()

            # 查询外部接收者
            non_members_sql = """
                SELECT
                    id,
                    workflow_transmittal_id,
                    bim360_account_id,
                    bim360_project_id,
                    email,
                    first_name,
                    last_name,
                    company_name,
                    role,
                    viewed_at,
                    downloaded_at,
                    created_at,
                    updated_at
                FROM transmittals_transmittal_non_members
                WHERE workflow_transmittal_id = %s::uuid
                ORDER BY email
            """
            cursor.execute(non_members_sql, (transmittal_id,))
            non_members = cursor.fetchall()

            # 转换项目成员为可序列化格式
            members_result = []
            for member in members:
                item = dict(member)
                # 转换 UUID
                for key in ['id', 'workflow_transmittal_id', 'bim360_account_id', 'bim360_project_id', 'user_id']:
                    if item.get(key):
                        item[key] = str(item[key])
                # 转换时间戳
                for key in ['viewed_at', 'downloaded_at', 'created_at', 'updated_at']:
                    if item.get(key):
                        item[key] = item[key].isoformat()

                # 映射字段名以匹配前端期望
                mapped_item = {
                    'id': item['id'],
                    'name': item['user_name'],
                    'email': item['email'],
                    'role_name': item.get('company_name'),  # 使用公司名作为角色
                    'type': 'member',
                    'viewed_at': item.get('viewed_at'),
                    'downloaded_at': item.get('downloaded_at'),
                }
                members_result.append(mapped_item)

            # 转换外部接收者为可序列化格式
            non_members_result = []
            for non_member in non_members:
                item = dict(non_member)
                # 转换 UUID
                for key in ['id', 'workflow_transmittal_id', 'bim360_account_id', 'bim360_project_id']:
                    if item.get(key):
                        item[key] = str(item[key])
                # 转换时间戳
                for key in ['viewed_at', 'downloaded_at', 'created_at', 'updated_at']:
                    if item.get(key):
                        item[key] = item[key].isoformat()

                # 映射字段名以匹配前端期望
                full_name = f"{item.get('first_name', '')} {item.get('last_name', '')}".strip()
                mapped_item = {
                    'id': item['id'],
                    'name': full_name if full_name else item['email'],
                    'email': item['email'],
                    'role_name': item.get('role') or item.get('company_name'),
                    'type': 'non_member',
                    'viewed_at': item.get('viewed_at'),
                    'downloaded_at': item.get('downloaded_at'),
                }
                non_members_result.append(mapped_item)

            # 合并两类接收者返回单一列表
            all_recipients = members_result + non_members_result

            return {
                'success': True,
                'transmittal_id': transmittal_id,
                'data': all_recipients,  # 返回合并后的单一列表
                'total_count': len(all_recipients)
            }

        except Exception as e:
            raise Exception(f"Failed to get transmittal recipients: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def mark_viewed(self, transmittal_id: str, email: str) -> Dict[str, Any]:
        """
        标记用户已查看传输单（更新 viewed_at）

        Args:
            transmittal_id: 传输单ID (UUID)
            email: 用户邮箱

        Returns:
            {
                'success': bool,
                'transmittal_id': str,
                'email': str,
                'viewed_at': str (ISO format),
                'user_type': 'member' | 'non_member'
            }
        """
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            current_time = datetime.utcnow()

            # 先尝试更新项目成员表
            update_member_sql = """
                UPDATE transmittals_transmittal_recipients
                SET viewed_at = %s, updated_at = %s
                WHERE workflow_transmittal_id = %s::uuid
                  AND email = %s
                  AND viewed_at IS NULL
                RETURNING id, user_name
            """
            cursor.execute(update_member_sql, (current_time, current_time, transmittal_id, email))
            member_result = cursor.fetchone()

            if member_result:
                # 更新成功 - 是项目成员
                conn.commit()
                return {
                    'success': True,
                    'transmittal_id': transmittal_id,
                    'email': email,
                    'viewed_at': current_time.isoformat() + 'Z',
                    'user_type': 'member',
                    'user_name': member_result['user_name']
                }

            # 如果不是项目成员，尝试更新外部接收者表
            update_non_member_sql = """
                UPDATE transmittals_transmittal_non_members
                SET viewed_at = %s, updated_at = %s
                WHERE workflow_transmittal_id = %s::uuid
                  AND email = %s
                  AND viewed_at IS NULL
                RETURNING id, first_name, last_name
            """
            cursor.execute(update_non_member_sql, (current_time, current_time, transmittal_id, email))
            non_member_result = cursor.fetchone()

            if non_member_result:
                # 更新成功 - 是外部接收者
                conn.commit()
                full_name = f"{non_member_result.get('first_name', '')} {non_member_result.get('last_name', '')}".strip()
                return {
                    'success': True,
                    'transmittal_id': transmittal_id,
                    'email': email,
                    'viewed_at': current_time.isoformat() + 'Z',
                    'user_type': 'non_member',
                    'user_name': full_name if full_name else email
                }

            # 用户不存在或已经查看过
            conn.rollback()
            return {
                'success': False,
                'error': 'User not found in recipients or already viewed',
                'transmittal_id': transmittal_id,
                'email': email
            }

        except Exception as e:
            if conn:
                conn.rollback()
            raise Exception(f"Failed to mark viewed: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def mark_downloaded(self, transmittal_id: str, email: str) -> Dict[str, Any]:
        """
        标记用户已下载传输单文件（更新 downloaded_at）

        Args:
            transmittal_id: 传输单ID (UUID)
            email: 用户邮箱

        Returns:
            {
                'success': bool,
                'transmittal_id': str,
                'email': str,
                'downloaded_at': str (ISO format),
                'user_type': 'member' | 'non_member'
            }
        """
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            current_time = datetime.utcnow()

            # 先尝试更新项目成员表
            update_member_sql = """
                UPDATE transmittals_transmittal_recipients
                SET downloaded_at = %s,
                    viewed_at = COALESCE(viewed_at, %s),
                    updated_at = %s
                WHERE workflow_transmittal_id = %s::uuid
                  AND email = %s
                RETURNING id, user_name
            """
            cursor.execute(update_member_sql, (current_time, current_time, current_time, transmittal_id, email))
            member_result = cursor.fetchone()

            if member_result:
                # 更新成功 - 是项目成员
                conn.commit()
                return {
                    'success': True,
                    'transmittal_id': transmittal_id,
                    'email': email,
                    'downloaded_at': current_time.isoformat() + 'Z',
                    'user_type': 'member',
                    'user_name': member_result['user_name']
                }

            # 如果不是项目成员，尝试更新外部接收者表
            update_non_member_sql = """
                UPDATE transmittals_transmittal_non_members
                SET downloaded_at = %s,
                    viewed_at = COALESCE(viewed_at, %s),
                    updated_at = %s
                WHERE workflow_transmittal_id = %s::uuid
                  AND email = %s
                RETURNING id, first_name, last_name
            """
            cursor.execute(update_non_member_sql, (current_time, current_time, current_time, transmittal_id, email))
            non_member_result = cursor.fetchone()

            if non_member_result:
                # 更新成功 - 是外部接收者
                conn.commit()
                full_name = f"{non_member_result.get('first_name', '')} {non_member_result.get('last_name', '')}".strip()
                return {
                    'success': True,
                    'transmittal_id': transmittal_id,
                    'email': email,
                    'downloaded_at': current_time.isoformat() + 'Z',
                    'user_type': 'non_member',
                    'user_name': full_name if full_name else email
                }

            # 用户不存在或已经下载过
            conn.rollback()
            return {
                'success': False,
                'error': 'User not found in recipients or already downloaded',
                'transmittal_id': transmittal_id,
                'email': email
            }

        except Exception as e:
            if conn:
                conn.rollback()
            raise Exception(f"Failed to mark downloaded: {str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def create_zip_package(self, transmittal_id: str) -> Dict[str, Any]:
        """
        创建传输单文件的 ZIP 压缩包

        Args:
            transmittal_id: 传输单ID (UUID)

        Returns:
            {
                'success': bool,
                'zip_path': str,              # ZIP 文件路径
                'zip_filename': str,          # ZIP 文件名
                'file_count': int,            # 打包的文件数量
                'total_size': int,            # 总大小(字节)
                'failed_files': List[Dict],   # 下载失败的文件列表
                'transmittal_info': Dict      # 传输单信息
            }
        """
        conn = None
        cursor = None
        temp_dir = None
        zip_path = None

        try:
            # 1. 获取传输单基本信息
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            transmittal_sql = """
                SELECT
                    id,
                    bim360_project_id,
                    sequence_id,
                    title,
                    docs_count
                FROM transmittals_workflow_transmittals
                WHERE id = %s::uuid
            """
            cursor.execute(transmittal_sql, (transmittal_id,))
            transmittal_info = cursor.fetchone()

            if not transmittal_info:
                return {
                    'success': False,
                    'error': f'Transmittal not found: {transmittal_id}'
                }

            transmittal_dict = dict(transmittal_info)
            project_id = str(transmittal_dict['bim360_project_id'])
            sequence_id = transmittal_dict['sequence_id']
            title = transmittal_dict['title']

            # 2. 获取所有文档
            documents_sql = """
                SELECT
                    id,
                    urn,
                    file_name,
                    version_number,
                    revision_number
                FROM transmittals_transmittal_documents
                WHERE workflow_transmittal_id = %s::uuid
                ORDER BY file_name
            """
            cursor.execute(documents_sql, (transmittal_id,))
            documents = cursor.fetchall()

            if not documents:
                return {
                    'success': False,
                    'error': 'No documents found in this transmittal'
                }

            # 3. 获取 access token
            access_token = utils.get_access_token()
            if not access_token:
                return {
                    'success': False,
                    'error': 'Access token not found',
                    'error_type': 'unauthorized'
                }

            # 4. 创建临时目录
            temp_dir = tempfile.mkdtemp(prefix='transmittal_')
            print(f"[ZIP] Created temp directory: {temp_dir}")

            # 5. 下载所有文件
            downloaded_files = []
            failed_files = []
            total_size = 0

            for idx, doc in enumerate(documents, 1):
                doc_dict = dict(doc)
                urn = doc_dict['urn']
                file_name = doc_dict['file_name']
                version_number = doc_dict.get('version_number', 1)

                print(f"[ZIP] Downloading {idx}/{len(documents)}: {file_name}")

                # 安全的文件名 (移除非法字符)
                safe_filename = self._sanitize_filename(file_name)

                # 添加版本号到文件名
                if version_number and version_number > 1:
                    name_parts = safe_filename.rsplit('.', 1)
                    if len(name_parts) == 2:
                        safe_filename = f"{name_parts[0]}_v{version_number}.{name_parts[1]}"
                    else:
                        safe_filename = f"{safe_filename}_v{version_number}"

                try:
                    # 1. Normalize URN to lineage format
                    full_lineage_urn = self._normalize_urn_to_lineage(urn)

                    print(f"[ZIP] Original URN: {urn}")
                    print(f"[ZIP] Normalized lineage URN: {full_lineage_urn}")

                    # 2. 使用 Data Management API 获取 item 信息（包含 storage location）
                    item_url = f"https://developer.api.autodesk.com/data/v1/projects/b.{project_id}/items/{full_lineage_urn}"
                    headers = {
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                    }

                    item_response = requests.get(item_url, headers=headers, timeout=30)

                    if item_response.status_code != 200:
                        raise Exception(f"Failed to get item info: {item_response.status_code} - {item_response.text}")

                    item_data = item_response.json()

                    # 3. 从响应中提取 storage location
                    storage_data = None
                    if 'included' in item_data:
                        for included_item in item_data['included']:
                            if included_item.get('type') == 'versions':
                                storage_rel = included_item.get('relationships', {}).get('storage', {})
                                storage_data = storage_rel.get('data', {})
                                break

                    if not storage_data or not storage_data.get('id'):
                        raise Exception(f"Storage location not found in item response")

                    storage_id = storage_data['id']
                    print(f"[ZIP] Storage ID: {storage_id}")

                    # 4. 解析 storage URN 以获取 bucket 和 object key
                    # Format: urn:adsk.objects:os.object:BUCKET/OBJECT_KEY
                    if not storage_id.startswith('urn:adsk.objects:os.object:'):
                        raise Exception(f"Invalid storage URN format: {storage_id}")

                    storage_path = storage_id.replace('urn:adsk.objects:os.object:', '')
                    if '/' not in storage_path:
                        raise Exception(f"Invalid storage path format: {storage_path}")

                    bucket_key, object_key = storage_path.split('/', 1)
                    print(f"[ZIP] Bucket: {bucket_key}, Object: {object_key}")

                    # 5. 获取 S3 签名下载 URL
                    s3_url = f"https://developer.api.autodesk.com/oss/v2/buckets/{bucket_key}/objects/{object_key}/signeds3download"
                    s3_response = requests.get(s3_url, headers=headers, timeout=30)

                    if s3_response.status_code != 200:
                        raise Exception(f"Failed to get S3 signed URL: {s3_response.status_code} - {s3_response.text}")

                    s3_data = s3_response.json()
                    download_url = s3_data.get('url')

                    if not download_url:
                        raise Exception(f"No download URL in S3 response")

                    print(f"[ZIP] Got S3 signed URL")

                    # 6. 下载文件（不需要 Authorization header，因为 URL 已经签名）
                    file_path = os.path.join(temp_dir, safe_filename)
                    download_response = requests.get(download_url, timeout=300, stream=True)

                    if download_response.status_code == 200:
                        with open(file_path, 'wb') as f:
                            for chunk in download_response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)

                        file_size = os.path.getsize(file_path)
                        total_size += file_size

                        downloaded_files.append({
                            'file_name': safe_filename,
                            'original_name': file_name,
                            'file_path': file_path,
                            'file_size': file_size,
                            'urn': urn
                        })

                        print(f"[ZIP] ✓ Downloaded: {safe_filename} ({file_size} bytes)")
                    else:
                        failed_files.append({
                            'file_name': file_name,
                            'urn': urn,
                            'error': f'Download failed: HTTP {download_response.status_code}'
                        })
                        print(f"[ZIP] ✗ Download failed: {file_name} (HTTP {download_response.status_code})")

                except Exception as e:
                    failed_files.append({
                        'file_name': file_name,
                        'urn': urn,
                        'error': str(e)
                    })
                    print(f"[ZIP] ✗ Exception downloading {file_name}: {e}")

            # 6. 创建 ZIP 文件
            if not downloaded_files:
                return {
                    'success': False,
                    'error': 'No files were successfully downloaded',
                    'failed_files': failed_files
                }

            # 创建 ZIP 文件名
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            safe_title = self._sanitize_filename(title) if title else f"transmittal_{sequence_id}"
            zip_filename = f"{safe_title}_{timestamp}.zip"
            zip_path = os.path.join(tempfile.gettempdir(), zip_filename)

            print(f"[ZIP] Creating ZIP archive: {zip_path}")

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_info in downloaded_files:
                    zipf.write(file_info['file_path'], arcname=file_info['file_name'])
                    print(f"[ZIP] Added to archive: {file_info['file_name']}")

            zip_size = os.path.getsize(zip_path)
            print(f"[ZIP] ✓ ZIP created: {zip_filename} ({zip_size} bytes)")

            return {
                'success': True,
                'zip_path': zip_path,
                'zip_filename': zip_filename,
                'file_count': len(downloaded_files),
                'total_size': zip_size,
                'failed_files': failed_files,
                'transmittal_info': {
                    'id': transmittal_id,
                    'sequence_id': sequence_id,
                    'title': title,
                    'project_id': project_id
                }
            }

        except Exception as e:
            print(f"[ZIP] ERROR: {e}")
            raise Exception(f"Failed to create ZIP package: {str(e)}")

        finally:
            # 清理临时文件
            if temp_dir and os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir)
                    print(f"[ZIP] Cleaned up temp directory: {temp_dir}")
                except Exception as e:
                    print(f"[ZIP] Warning: Failed to cleanup temp directory: {e}")

            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def _sanitize_filename(self, filename: str) -> str:
        """
        清理文件名，移除非法字符

        Args:
            filename: 原始文件名

        Returns:
            清理后的安全文件名
        """
        # Windows 非法字符
        illegal_chars = '<>:"/\\|?*'
        safe_name = filename

        for char in illegal_chars:
            safe_name = safe_name.replace(char, '_')

        # 移除前后空格
        safe_name = safe_name.strip()

        # 限制文件名长度 (保留扩展名)
        max_length = 200
        if len(safe_name) > max_length:
            name_parts = safe_name.rsplit('.', 1)
            if len(name_parts) == 2:
                name, ext = name_parts
                safe_name = name[:max_length - len(ext) - 1] + '.' + ext
            else:
                safe_name = safe_name[:max_length]

        return safe_name

    def _normalize_urn_to_lineage(self, urn: str) -> str:
        """
        Normalize URN to lineage format for API calls

        Handles multiple URN formats:
        1. urn:adsk.wipprod:fs.file:vf.-rYcWE1gQauykAmg0SRmgQ?version=1 -> urn:adsk.wipprod:dm.lineage:-rYcWE1gQauykAmg0SRmgQ
        2. 5PfUdMeESQ6S8XmZ5lCPaw -> urn:adsk.wipprod:dm.lineage:5PfUdMeESQ6S8XmZ5lCPaw
        3. urn:adsk.wipprod:dm.lineage:xxx -> unchanged

        Args:
            urn: The URN in any format

        Returns:
            Normalized URN in lineage format
        """
        import re

        if not urn:
            return urn

        # If it's already a lineage URN, return as-is
        if urn.startswith('urn:adsk.wipprod:dm.lineage:'):
            return urn

        # Handle fs.file format: urn:adsk.wipprod:fs.file:vf.XXXXX?version=N
        if 'fs.file:vf.' in urn:
            # Extract the ID part after vf. and before ?version
            match = re.search(r'fs\.file:vf\.([^?]+)', urn)
            if match:
                file_id = match.group(1)
                return f"urn:adsk.wipprod:dm.lineage:{file_id}"

        # Handle plain ID (no prefix)
        if not urn.startswith('urn:'):
            return f"urn:adsk.wipprod:dm.lineage:{urn}"

        # Unknown format, return as-is
        return urn


# ========================================
# API 路由
# ========================================

# 创建管理器实例
transmittal_manager = TransmittalManager()


@transmittal_bp.route('/<project_id>/list', methods=['GET'])
@handle_exceptions
def get_transmittals_list(project_id):
    """
    API 1: 获取传输单列表

    GET /api/transmittals/<project_id>/list

    Query Parameters:
        - limit: 每页数量 (默认: 100)
        - offset: 偏移量 (默认: 0)

    Returns:
        {
            "success": true,
            "data": [...],
            "total": 123,
            "limit": 100,
            "offset": 0
        }
    """
    # 获取查询参数
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)

    # 参数验证
    if limit < 1 or limit > 1000:
        return jsonify({
            'success': False,
            'error': 'Limit must be between 1 and 1000'
        }), 400

    if offset < 0:
        return jsonify({
            'success': False,
            'error': 'Offset must be >= 0'
        }), 400

    # 调用管理器获取数据
    result = transmittal_manager.get_transmittals_list(project_id, limit, offset)

    return jsonify(result), 200


@transmittal_bp.route('/<transmittal_id>/documents', methods=['GET'])
@handle_exceptions
def get_transmittal_documents(transmittal_id):
    """
    API 2: 获取传输单文档列表

    GET /api/transmittals/<transmittal_id>/documents

    Returns:
        {
            "success": true,
            "transmittal_id": "xxx-xxx-xxx",
            "data": [...],
            "count": 10
        }
    """
    result = transmittal_manager.get_transmittal_documents(transmittal_id)
    return jsonify(result), 200


@transmittal_bp.route('/<transmittal_id>/recipients', methods=['GET'])
@handle_exceptions
def get_transmittal_recipients(transmittal_id):
    """
    API 3: 获取传输单接收者列表（包括项目成员和外部接收者）

    GET /api/transmittals/<transmittal_id>/recipients

    Returns:
        {
            "success": true,
            "transmittal_id": "xxx-xxx-xxx",
            "data": {
                "members": [...],
                "non_members": [...]
            },
            "total_count": 15
        }
    """
    result = transmittal_manager.get_transmittal_recipients(transmittal_id)
    return jsonify(result), 200


@transmittal_bp.route('/<transmittal_id>/mark-viewed', methods=['POST'])
@handle_exceptions
def mark_viewed(transmittal_id):
    """
    API 4: 标记用户已查看传输单

    POST /api/transmittals/<transmittal_id>/mark-viewed

    Request Body:
        {
            "email": "user@example.com"
        }

    Returns:
        {
            "success": true,
            "transmittal_id": "xxx-xxx-xxx",
            "email": "user@example.com",
            "viewed_at": "2025-01-18T10:30:45Z",
            "user_type": "member",
            "user_name": "John Doe"
        }
    """
    data = request.get_json()

    if not data or 'email' not in data:
        return jsonify({
            'success': False,
            'error': 'Email is required in request body'
        }), 400

    email = data['email'].strip()

    if not email:
        return jsonify({
            'success': False,
            'error': 'Email cannot be empty'
        }), 400

    result = transmittal_manager.mark_viewed(transmittal_id, email)

    if result.get('success'):
        return jsonify(result), 200
    else:
        return jsonify(result), 404


@transmittal_bp.route('/<transmittal_id>/mark-downloaded', methods=['POST'])
@handle_exceptions
def mark_downloaded(transmittal_id):
    """
    API 5: 标记用户已下载传输单文件

    POST /api/transmittals/<transmittal_id>/mark-downloaded

    Request Body:
        {
            "email": "user@example.com"
        }

    Returns:
        {
            "success": true,
            "transmittal_id": "xxx-xxx-xxx",
            "email": "user@example.com",
            "downloaded_at": "2025-01-18T10:35:00Z",
            "user_type": "member",
            "user_name": "John Doe"
        }

    Note: 下载操作会自动设置 viewed_at (如果尚未设置)
    """
    data = request.get_json()

    if not data or 'email' not in data:
        return jsonify({
            'success': False,
            'error': 'Email is required in request body'
        }), 400

    email = data['email'].strip()

    if not email:
        return jsonify({
            'success': False,
            'error': 'Email cannot be empty'
        }), 400

    result = transmittal_manager.mark_downloaded(transmittal_id, email)

    if result.get('success'):
        return jsonify(result), 200
    else:
        return jsonify(result), 404


@transmittal_bp.route('/<transmittal_id>/download-zip', methods=['POST'])
@handle_exceptions
def download_zip(transmittal_id):
    """
    API 6: 打包下载传输单所有文件为 ZIP

    POST /api/transmittals/<transmittal_id>/download-zip

    可选请求体参数:
        {
            "email": "user@example.com"  # 如果提供，会自动标记该用户已下载
        }

    流程:
    1. 从 transmittals_transmittal_documents 表获取所有文档的 URN
    2. 使用 utils.get_access_token() 获取 ACC API token
    3. 使用 URNDownloadManager 批量下载文件
    4. 将所有文件打包成 ZIP
    5. 返回 ZIP 文件流供下载

    返回:
        - 成功: 返回 ZIP 文件流 (application/zip)
        - 失败: 返回 JSON 错误信息

    注意:
        - 下载大量文件可能需要较长时间
        - ZIP 文件在发送后会自动清理
        - 如果部分文件下载失败，会在响应头中包含失败列表
    """
    try:
        # 检查是否需要标记用户已下载
        email = None
        data = request.get_json(silent=True)
        if data and 'email' in data:
            email = data['email'].strip()

        # 创建 ZIP 压缩包
        print(f"[API] Starting ZIP creation for transmittal: {transmittal_id}")
        result = transmittal_manager.create_zip_package(transmittal_id)

        if not result.get('success'):
            return jsonify({
                'success': False,
                'error': result.get('error', 'Failed to create ZIP package'),
                'error_type': 'zip_creation_failed'
            }), 500

        zip_path = result['zip_path']
        zip_filename = result['zip_filename']
        file_count = result['file_count']
        total_size = result['total_size']
        failed_files = result.get('failed_files', [])

        print(f"[API] ZIP created successfully: {zip_filename} ({file_count} files, {total_size} bytes)")

        # 如果提供了 email，标记用户已下载
        if email:
            try:
                mark_result = transmittal_manager.mark_downloaded(transmittal_id, email)
                if mark_result.get('success'):
                    print(f"[API] Marked as downloaded for user: {email}")
                else:
                    print(f"[API] Warning: Failed to mark downloaded for {email}: {mark_result.get('error')}")
            except Exception as e:
                print(f"[API] Warning: Exception marking downloaded: {e}")

        # 准备响应头
        headers = {
            'X-File-Count': str(file_count),
            'X-Total-Size': str(total_size),
            'Content-Disposition': f'attachment; filename="{zip_filename}"'
        }

        # 如果有失败的文件，添加到响应头
        if failed_files:
            import json
            headers['X-Failed-Files'] = json.dumps(failed_files)
            print(f"[API] Warning: {len(failed_files)} files failed to download")

        # 调度 ZIP 文件清理 (5分钟后删除)
        zip_cleanup.schedule_cleanup(zip_path, delay=300)

        # 发送文件
        response = send_file(
            zip_path,
            mimetype='application/zip',
            as_attachment=True,
            download_name=zip_filename
        )

        # 添加自定义响应头
        for key, value in headers.items():
            response.headers[key] = value

        return response

    except Exception as e:
        print(f"[API] Error in download_zip: {e}")
        # 清理可能已创建的 ZIP 文件
        if 'zip_path' in locals() and os.path.exists(zip_path):
            try:
                os.remove(zip_path)
                print(f"[API] Cleaned up failed ZIP: {zip_path}")
            except Exception as cleanup_error:
                print(f"[API] Failed to cleanup ZIP: {cleanup_error}")

        return jsonify({
            'success': False,
            'error': f'Failed to create ZIP download: {str(e)}',
            'error_type': 'internal_error'
        }), 500


@transmittal_bp.route('/create', methods=['POST'])
@handle_exceptions
def create_transmittal():
    """
    API 7: Create a new transmittal

    POST /api/transmittals/create

    Request Body:
        {
            "project_id": "uuid",
            "title": "string",
            "message": "string (optional)",
            "created_by_user_id": "uuid (optional)",
            "created_by_user_name": "string",
            "created_by_company_id": "uuid (optional)",
            "created_by_company_name": "string (optional)"
        }

    Returns:
        {
            "success": true,
            "transmittal_id": "uuid",
            "sequence_id": 123
        }
    """
    import uuid as uuid_module

    data = request.get_json()

    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400

    # Validate required fields
    if not data.get('project_id'):
        return jsonify({
            'success': False,
            'error': 'project_id is required'
        }), 400

    if not data.get('title'):
        return jsonify({
            'success': False,
            'error': 'title is required'
        }), 400

    conn = None
    cursor = None
    try:
        conn = transmittal_manager.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Clean project_id (remove b. prefix if present)
        project_id = data['project_id']
        if project_id.startswith('b.'):
            project_id = project_id[2:]

        # Get next sequence_id for this project
        seq_sql = """
            SELECT COALESCE(MAX(sequence_id), 0) + 1 as next_seq
            FROM transmittals_workflow_transmittals
            WHERE bim360_project_id = %s::uuid
        """
        cursor.execute(seq_sql, (project_id,))
        next_seq = cursor.fetchone()['next_seq']

        # Generate UUID for new transmittal
        transmittal_id = str(uuid_module.uuid4())

        # Get account_id from project (use project_id as account_id for now)
        # In real scenario, this should be fetched from project configuration
        account_id = project_id

        # Create transmittal
        current_time = datetime.utcnow()

        # Handle optional user_id
        created_by_user_id = data.get('created_by_user_id')
        if created_by_user_id == '' or created_by_user_id is None:
            created_by_user_id = str(uuid_module.uuid4())  # Generate a placeholder UUID

        insert_sql = """
            INSERT INTO transmittals_workflow_transmittals (
                id,
                bim360_account_id,
                bim360_project_id,
                sequence_id,
                title,
                message,
                status,
                docs_count,
                create_user_id,
                create_user_name,
                create_user_company_id,
                create_user_company_name,
                created_at,
                updated_at
            ) VALUES (
                %s::uuid,
                %s::uuid,
                %s::uuid,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s::uuid,
                %s,
                %s::uuid,
                %s,
                %s,
                %s
            )
            RETURNING id, sequence_id
        """

        # Handle optional company_id
        company_id = data.get('created_by_company_id')
        if company_id == '' or company_id is None:
            company_id = None

        cursor.execute(insert_sql, (
            transmittal_id,
            account_id,
            project_id,
            next_seq,
            data['title'],
            data.get('message'),
            2,  # Status 2 = SENT
            0,  # Initial docs_count
            created_by_user_id,
            data.get('created_by_user_name', 'System User'),
            company_id,
            data.get('created_by_company_name'),
            current_time,
            current_time
        ))

        result = cursor.fetchone()
        conn.commit()

        print(f"[API] Created transmittal: {transmittal_id}, sequence: {next_seq}")

        return jsonify({
            'success': True,
            'transmittal_id': str(result['id']),
            'sequence_id': result['sequence_id']
        }), 201

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"[API] Error creating transmittal: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@transmittal_bp.route('/<transmittal_id>/documents', methods=['POST'])
@handle_exceptions
def add_transmittal_documents(transmittal_id):
    """
    API 8: Add documents to a transmittal

    POST /api/transmittals/<transmittal_id>/documents

    Request Body:
        {
            "documents": [
                {
                    "urn": "string (required)",
                    "file_name": "string (required)",
                    "version_number": "integer"
                }
            ]
        }

    Returns:
        {
            "success": true,
            "transmittal_id": "uuid",
            "documents_added": 5
        }
    """
    import uuid as uuid_module

    data = request.get_json()

    if not data or 'documents' not in data:
        return jsonify({
            'success': False,
            'error': 'documents array is required'
        }), 400

    documents = data['documents']
    if not documents or len(documents) == 0:
        return jsonify({
            'success': False,
            'error': 'At least one document is required'
        }), 400

    conn = None
    cursor = None
    try:
        conn = transmittal_manager.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Get transmittal info
        transmittal_sql = """
            SELECT bim360_account_id, bim360_project_id
            FROM transmittals_workflow_transmittals
            WHERE id = %s::uuid
        """
        cursor.execute(transmittal_sql, (transmittal_id,))
        transmittal = cursor.fetchone()

        if not transmittal:
            return jsonify({
                'success': False,
                'error': f'Transmittal not found: {transmittal_id}'
            }), 404

        account_id = str(transmittal['bim360_account_id'])
        project_id = str(transmittal['bim360_project_id'])

        # Insert documents
        current_time = datetime.utcnow()
        docs_added = 0

        for doc in documents:
            if not doc.get('urn') or not doc.get('file_name'):
                continue

            doc_id = str(uuid_module.uuid4())

            # Try to get file details - this is optional, use defaults if not found
            file_details = None
            try:
                # Use savepoint to handle potential errors
                cursor.execute("SAVEPOINT file_details_check")

                # Try to find in file_versions table first
                file_details_sql = """
                    SELECT
                        fv.create_time as last_modified_time,
                        fv.create_user_id as last_modified_user_id,
                        fv.create_user_name as last_modified_user_name,
                        f.parent_folder_id as parent_folder_urn
                    FROM file_versions fv
                    JOIN files f ON fv.file_id = f.id
                    WHERE fv.urn = %s AND fv.version_number = %s
                    LIMIT 1
                """
                cursor.execute(file_details_sql, (
                    doc['urn'],
                    doc.get('version_number', 1)
                ))
                file_details = cursor.fetchone()

                # If no result from file_versions, try files table directly
                if not file_details:
                    file_only_sql = """
                        SELECT
                            last_modified_time,
                            last_modified_user_id,
                            last_modified_user_name,
                            parent_folder_id as parent_folder_urn
                        FROM files
                        WHERE id = %s OR name = %s
                        LIMIT 1
                    """
                    cursor.execute(file_only_sql, (
                        doc['urn'],
                        doc.get('file_name', '')
                    ))
                    file_details = cursor.fetchone()

                cursor.execute("RELEASE SAVEPOINT file_details_check")
            except Exception as e:
                # Rollback to savepoint to recover from error
                try:
                    cursor.execute("ROLLBACK TO SAVEPOINT file_details_check")
                except:
                    pass  # Ignore rollback errors
                print(f"[API] Warning: Could not fetch file details: {e}")

            insert_doc_sql = """
                INSERT INTO transmittals_transmittal_documents (
                    id,
                    workflow_transmittal_id,
                    bim360_account_id,
                    bim360_project_id,
                    urn,
                    file_name,
                    version_number,
                    revision_number,
                    parent_folder_urn,
                    last_modified_time,
                    last_modified_user_id,
                    last_modified_user_name,
                    created_at,
                    updated_at
                ) VALUES (
                    %s::uuid,
                    %s::uuid,
                    %s::uuid,
                    %s::uuid,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
            """

            # Use file details if available, otherwise use defaults
            last_modified_time = file_details['last_modified_time'] if file_details else current_time
            last_modified_user_id = file_details['last_modified_user_id'] if file_details else 'system'
            last_modified_user_name = file_details['last_modified_user_name'] if file_details else 'System'
            parent_folder_urn = file_details['parent_folder_urn'] if file_details else ''

            cursor.execute(insert_doc_sql, (
                doc_id,
                transmittal_id,
                account_id,
                project_id,
                doc['urn'],
                doc['file_name'],
                doc.get('version_number', 1),
                doc.get('revision_number', doc.get('version_number', 1)),
                parent_folder_urn,
                last_modified_time,
                last_modified_user_id,
                last_modified_user_name,
                current_time,
                current_time
            ))
            docs_added += 1

        # Update docs_count in transmittal
        update_count_sql = """
            UPDATE transmittals_workflow_transmittals
            SET docs_count = %s, updated_at = %s
            WHERE id = %s::uuid
        """
        cursor.execute(update_count_sql, (docs_added, current_time, transmittal_id))

        conn.commit()

        print(f"[API] Added {docs_added} documents to transmittal: {transmittal_id}")

        return jsonify({
            'success': True,
            'transmittal_id': transmittal_id,
            'documents_added': docs_added
        }), 201

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"[API] Error adding documents: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@transmittal_bp.route('/<transmittal_id>/recipients', methods=['POST'])
@handle_exceptions
def add_transmittal_recipients(transmittal_id):
    """
    API 9: Add recipients to a transmittal

    POST /api/transmittals/<transmittal_id>/recipients

    Request Body:
        {
            "recipients": [
                {
                    "user_id": "uuid",
                    "user_name": "string",
                    "email": "string",
                    "company_name": "string (optional)"
                }
            ]
        }

    Returns:
        {
            "success": true,
            "transmittal_id": "uuid",
            "recipients_added": 5
        }
    """
    import uuid as uuid_module

    data = request.get_json()

    if not data or 'recipients' not in data:
        return jsonify({
            'success': False,
            'error': 'recipients array is required'
        }), 400

    recipients = data['recipients']
    if not recipients or len(recipients) == 0:
        return jsonify({
            'success': False,
            'error': 'At least one recipient is required'
        }), 400

    conn = None
    cursor = None
    try:
        conn = transmittal_manager.get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Get transmittal info
        transmittal_sql = """
            SELECT bim360_account_id, bim360_project_id
            FROM transmittals_workflow_transmittals
            WHERE id = %s::uuid
        """
        cursor.execute(transmittal_sql, (transmittal_id,))
        transmittal = cursor.fetchone()

        if not transmittal:
            return jsonify({
                'success': False,
                'error': f'Transmittal not found: {transmittal_id}'
            }), 404

        account_id = str(transmittal['bim360_account_id'])
        project_id = str(transmittal['bim360_project_id'])

        # Insert recipients (deduplicate by email)
        current_time = datetime.utcnow()
        recipients_added = 0
        seen_emails = set()

        for recipient in recipients:
            email = recipient.get('email', '').strip().lower()
            if not email or email in seen_emails:
                continue

            seen_emails.add(email)
            recipient_id = str(uuid_module.uuid4())

            # Handle user_id
            user_id = recipient.get('user_id')
            if not user_id or user_id == '':
                user_id = str(uuid_module.uuid4())  # Generate placeholder

            insert_recipient_sql = """
                INSERT INTO transmittals_transmittal_recipients (
                    id,
                    workflow_transmittal_id,
                    bim360_account_id,
                    bim360_project_id,
                    user_id,
                    user_name,
                    email,
                    company_name,
                    viewed_at,
                    downloaded_at,
                    created_at,
                    updated_at
                ) VALUES (
                    %s::uuid,
                    %s::uuid,
                    %s::uuid,
                    %s::uuid,
                    %s::uuid,
                    %s,
                    %s,
                    %s,
                    NULL,
                    NULL,
                    %s,
                    %s
                )
                ON CONFLICT (workflow_transmittal_id, user_id) DO NOTHING
            """

            cursor.execute(insert_recipient_sql, (
                recipient_id,
                transmittal_id,
                account_id,
                project_id,
                user_id,
                recipient.get('user_name', recipient.get('name', email)),
                email,
                recipient.get('company_name'),
                current_time,
                current_time
            ))

            if cursor.rowcount > 0:
                recipients_added += 1

        conn.commit()

        print(f"[API] Added {recipients_added} recipients to transmittal: {transmittal_id}")

        return jsonify({
            'success': True,
            'transmittal_id': transmittal_id,
            'recipients_added': recipients_added
        }), 201

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"[API] Error adding recipients: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# ========================================
# Blueprint 注册说明
# ========================================

"""
在主应用中注册此 Blueprint:

from api_modules.transmittal_CDE_function.transmittal import transmittal_bp

app.register_blueprint(transmittal_bp)

所有路由将自动挂载到 /api/transmittals 前缀下
"""
