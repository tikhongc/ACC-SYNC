# -*- coding: utf-8 -*-
"""
File Download API
提供單文件下載的後端 API 接口

API:
POST /api/files/download - 下載單個文件
"""

import sys
import os
import re
import tempfile
import requests
from functools import wraps
from typing import Dict, Any, Optional

# Windows 環境 UTF-8 編碼設置
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'

from flask import Blueprint, jsonify, request, send_file

# 導入認證工具
import utils

# 創建 Blueprint
file_download_bp = Blueprint('file_download', __name__, url_prefix='/api/files')


# ========================================
# 異常處理裝飾器
# ========================================

def handle_exceptions(f):
    """統一異常處理裝飾器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
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
# File Download Manager 類
# ========================================

class FileDownloadManager:
    """文件下載管理器 - 封裝單文件下載邏輯"""

    def __init__(self):
        pass

    def normalize_urn_to_lineage(self, urn: str) -> str:
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

    def sanitize_filename(self, filename: str) -> str:
        """
        清理文件名，移除非法字符

        Args:
            filename: 原始文件名

        Returns:
            清理後的安全文件名
        """
        # Windows 非法字符
        illegal_chars = '<>:"/\\|?*'
        safe_name = filename

        for char in illegal_chars:
            safe_name = safe_name.replace(char, '_')

        # 移除前後空格
        safe_name = safe_name.strip()

        # 限制文件名長度 (保留扩展名)
        max_length = 200
        if len(safe_name) > max_length:
            name_parts = safe_name.rsplit('.', 1)
            if len(name_parts) == 2:
                name, ext = name_parts
                safe_name = name[:max_length - len(ext) - 1] + '.' + ext
            else:
                safe_name = safe_name[:max_length]

        return safe_name

    def download_file(self, urn: str, project_id: str, file_name: Optional[str] = None) -> Dict[str, Any]:
        """
        下載單個文件

        Args:
            urn: 文件 URN（支持多種格式）
            project_id: 項目 ID（支持 b.xxx 格式）
            file_name: 可選的文件名（用於下載時的文件名）

        Returns:
            {
                'success': bool,
                'file_path': str,       # 臨時文件路徑
                'file_name': str,       # 文件名
                'file_size': int,       # 文件大小（字節）
                'error': str (optional) # 錯誤信息
            }
        """
        temp_file_path = None

        try:
            # 1. 清理 project_id（移除 b. 前綴如果存在）
            clean_project_id = project_id[2:] if project_id.startswith('b.') else project_id

            # 2. 獲取 access token
            access_token = utils.get_access_token()
            if not access_token:
                return {
                    'success': False,
                    'error': 'Access token not found',
                    'error_type': 'unauthorized'
                }

            # 3. Normalize URN to lineage format
            full_lineage_urn = self.normalize_urn_to_lineage(urn)

            print(f"[FileDownload] Original URN: {urn}")
            print(f"[FileDownload] Normalized lineage URN: {full_lineage_urn}")

            # 4. 使用 Data Management API 獲取 item 信息（包含 storage location）
            item_url = f"https://developer.api.autodesk.com/data/v1/projects/b.{clean_project_id}/items/{full_lineage_urn}"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            item_response = requests.get(item_url, headers=headers, timeout=30)

            if item_response.status_code != 200:
                raise Exception(f"Failed to get item info: {item_response.status_code} - {item_response.text}")

            item_data = item_response.json()

            # 5. 從響應中提取 storage location
            storage_data = None
            if 'included' in item_data:
                for included_item in item_data['included']:
                    if included_item.get('type') == 'versions':
                        storage_rel = included_item.get('relationships', {}).get('storage', {})
                        storage_data = storage_rel.get('data', {})
                        break

            if not storage_data or not storage_data.get('id'):
                raise Exception("Storage location not found in item response")

            storage_id = storage_data['id']
            print(f"[FileDownload] Storage ID: {storage_id}")

            # 6. 解析 storage URN 以獲取 bucket 和 object key
            # Format: urn:adsk.objects:os.object:BUCKET/OBJECT_KEY
            if not storage_id.startswith('urn:adsk.objects:os.object:'):
                raise Exception(f"Invalid storage URN format: {storage_id}")

            storage_path = storage_id.replace('urn:adsk.objects:os.object:', '')
            if '/' not in storage_path:
                raise Exception(f"Invalid storage path format: {storage_path}")

            bucket_key, object_key = storage_path.split('/', 1)
            print(f"[FileDownload] Bucket: {bucket_key}, Object: {object_key}")

            # 7. 獲取 S3 簽名下載 URL
            s3_url = f"https://developer.api.autodesk.com/oss/v2/buckets/{bucket_key}/objects/{object_key}/signeds3download"
            s3_response = requests.get(s3_url, headers=headers, timeout=30)

            if s3_response.status_code != 200:
                raise Exception(f"Failed to get S3 signed URL: {s3_response.status_code} - {s3_response.text}")

            s3_data = s3_response.json()
            download_url = s3_data.get('url')

            if not download_url:
                raise Exception("No download URL in S3 response")

            print(f"[FileDownload] Got S3 signed URL")

            # 8. 如果沒有提供文件名，嘗試從 item_data 中提取
            if not file_name:
                try:
                    file_name = item_data.get('data', {}).get('attributes', {}).get('displayName', 'download')
                except:
                    file_name = 'download'

            # 清理文件名
            safe_filename = self.sanitize_filename(file_name)

            # 9. 下載文件到臨時目錄（不需要 Authorization header，因為 URL 已經簽名）
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=f"_{safe_filename}")
            temp_file_path = temp_file.name
            temp_file.close()

            download_response = requests.get(download_url, timeout=300, stream=True)

            if download_response.status_code != 200:
                raise Exception(f"Download failed: HTTP {download_response.status_code}")

            with open(temp_file_path, 'wb') as f:
                for chunk in download_response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            file_size = os.path.getsize(temp_file_path)
            print(f"[FileDownload] Downloaded: {safe_filename} ({file_size} bytes)")

            return {
                'success': True,
                'file_path': temp_file_path,
                'file_name': safe_filename,
                'file_size': file_size
            }

        except Exception as e:
            print(f"[FileDownload] Error: {e}")
            # 清理臨時文件（如果創建了）
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                except:
                    pass

            return {
                'success': False,
                'error': str(e)
            }


# ========================================
# API 路由
# ========================================

# 創建管理器實例
file_download_manager = FileDownloadManager()


@file_download_bp.route('/download', methods=['POST', 'OPTIONS'])
@handle_exceptions
def download_file():
    """
    API: 下載單個文件

    POST /api/files/download

    Request Body:
        {
            "urn": "string (required)",           # 文件 URN（支持多種格式）
            "project_id": "string (required)",    # 項目 ID（支持 b.xxx 格式）
            "file_name": "string (optional)"      # 文件名（用於下載時的文件名）
        }

    Returns:
        - 成功: 返回文件流 (application/octet-stream)
        - 失敗: 返回 JSON 錯誤信息

    Example:
        {
            "urn": "urn:adsk.wipprod:fs.file:vf.xxx?version=1",
            "project_id": "b.1eea4119-3553-4167-b93d-3a3d5d07d33d",
            "file_name": "example.pdf"
        }
    """
    # 處理 CORS preflight OPTIONS 請求
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    data = request.get_json()

    # 驗證必填參數
    if not data:
        return jsonify({
            'success': False,
            'error': 'Request body is required'
        }), 400

    urn = data.get('urn')
    project_id = data.get('project_id')

    if not urn:
        return jsonify({
            'success': False,
            'error': 'urn is required'
        }), 400

    if not project_id:
        return jsonify({
            'success': False,
            'error': 'project_id is required'
        }), 400

    file_name = data.get('file_name')

    # 執行下載
    print(f"[API] Starting file download for URN: {urn}")
    result = file_download_manager.download_file(urn, project_id, file_name)

    if not result.get('success'):
        return jsonify({
            'success': False,
            'error': result.get('error', 'Failed to download file'),
            'error_type': 'download_failed'
        }), 500

    file_path = result['file_path']
    file_name = result['file_name']
    file_size = result['file_size']

    print(f"[API] File download successful: {file_name} ({file_size} bytes)")

    try:
        # 發送文件
        response = send_file(
            file_path,
            mimetype='application/octet-stream',
            as_attachment=True,
            download_name=file_name
        )

        # 添加自定義響應頭
        response.headers['X-File-Size'] = str(file_size)
        response.headers['Content-Disposition'] = f'attachment; filename="{file_name}"'

        # 註冊清理回調（在響應發送後刪除臨時文件）
        @response.call_on_close
        def cleanup():
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"[API] Cleaned up temp file: {file_path}")
            except Exception as e:
                print(f"[API] Failed to cleanup temp file: {e}")

        return response

    except Exception as e:
        print(f"[API] Error sending file: {e}")
        # 清理臨時文件
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

        return jsonify({
            'success': False,
            'error': f'Failed to send file: {str(e)}',
            'error_type': 'internal_error'
        }), 500


# ========================================
# Blueprint 註冊說明
# ========================================

"""
在主應用中註冊此 Blueprint:

from api_modules.file_CDE_function.file_download import file_download_bp

app.register_blueprint(file_download_bp)

所有路由將自動掛載到 /api/files 前綴下
"""
