#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Forge Viewer URL 生成 API

提供接口生成 Autodesk Forge Viewer 的预览链接
"""

from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
import logging
import traceback
import base64
from urllib.parse import urlencode
import sys
import os

# 为了支持相对导入和直接导入，使用 try-except
try:
    # 相对导入
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    from utils import get_access_token
except ImportError:
    # 直接导入
    from ACC_SYNC.utils import get_access_token

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建蓝图
forge_viewer_bp = Blueprint('forge_viewer', __name__, url_prefix='/api')

# Forge Viewer 基础 URL
FORGE_VIEWER_BASE_URL = "https://example.jarvisbim.com.cn/help/online-forge-viewer"


# ============================================================================
# URN 格式化函数
# ============================================================================

def normalize_urn_for_viewer(urn: str, version: int = 1) -> str:
    """
    将 URN 标准化为 Forge Viewer 所需的 fs.file 格式

    处理多种 URN 格式：
    1. 短格式（仅 ID）: "5PfUdMeESQ6S8XmZ5lCPaw"
       -> "urn:adsk.wipprod:fs.file:vf.5PfUdMeESQ6S8XmZ5lCPaw?version=1"

    2. 完整 fs.file 格式: "urn:adsk.wipprod:fs.file:vf.xxx?version=1"
       -> 保持不变

    3. dm.lineage 格式: "urn:adsk.wipprod:dm.lineage:xxx"
       -> "urn:adsk.wipprod:fs.file:vf.xxx?version=1"

    Args:
        urn: 输入的 URN（任意格式）
        version: 版本号（默认为 1）

    Returns:
        标准化后的 fs.file 格式 URN
    """
    import re

    if not urn:
        return urn

    # 已经是完整的 fs.file 格式，直接返回
    if urn.startswith('urn:adsk.wipprod:fs.file:vf.') and '?version=' in urn:
        logger.info(f"URN 已经是完整格式: {urn}")
        return urn

    # 提取文件 ID（支持多种格式）
    file_id = None

    # 格式 1: dm.lineage 格式
    if 'dm.lineage:' in urn:
        match = re.search(r'dm\.lineage:([^?]+)', urn)
        if match:
            file_id = match.group(1)
            logger.info(f"从 dm.lineage 格式提取 ID: {file_id}")

    # 格式 2: fs.file 格式但缺少 version
    elif 'fs.file:vf.' in urn:
        match = re.search(r'fs\.file:vf\.([^?]+)', urn)
        if match:
            file_id = match.group(1)
            logger.info(f"从 fs.file 格式提取 ID: {file_id}")

    # 格式 3: 纯 ID（短格式）
    elif not urn.startswith('urn:'):
        file_id = urn
        logger.info(f"检测到短格式 URN: {file_id}")

    # 如果成功提取到 file_id，构建完整的 fs.file URN
    if file_id:
        normalized_urn = f"urn:adsk.wipprod:fs.file:vf.{file_id}?version={version}"
        logger.info(f"URN 标准化: {urn} -> {normalized_urn}")
        return normalized_urn

    # 无法识别的格式，返回原始 URN
    logger.warning(f"无法识别的 URN 格式，返回原始值: {urn}")
    return urn


# ============================================================================
# API 端点
# ============================================================================

@forge_viewer_bp.route('/forge-viewer/url', methods=['GET', 'POST', 'OPTIONS'])
def generate_forge_viewer_url():
    """
    生成 Forge Viewer 预览 URL

    支持 GET 和 POST 两种请求方式

    GET 请求参数:
        - urn (必需): 文件的 URN (会自动进行 base64 编码)
        - use_current_token (可选): 是否使用当前系统的 token (true/false, 默认 true)
        - token (可选): 自定义 access token (如果 use_current_token=false)

    POST 请求体:
        {
            "urn": "urn:adsk.wipprod:fs.file:vf.xxx",
            "use_current_token": true,  // 可选，默认 true
            "token": "custom_token"     // 可选，自定义 token
        }

    返回:
        {
            "success": true/false,
            "data": {
                "viewer_url": "https://example.jarvisbim.com.cn/help/online-forge-viewer?urn=xxx&token=xxx",
                "urn": "原始 URN",
                "urn_encoded": "base64 编码后的 URN",
                "token_used": "access_token 前缀...",
                "generated_at": "2025-11-20T10:00:00Z"
            },
            "error": "error message" (if success=false)
        }
    """
    try:
        # 处理 OPTIONS 预检请求
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200

        # 根据请求方法获取参数
        if request.method == 'GET':
            urn = request.args.get('urn')
            use_current_token = request.args.get('use_current_token', 'true').lower() == 'true'
            custom_token = request.args.get('token')
            version = request.args.get('version', 1, type=int)
        else:  # POST
            data = request.get_json() or {}
            urn = data.get('urn')
            use_current_token = data.get('use_current_token', True)
            custom_token = data.get('token')
            version = data.get('version', 1)

        # 验证必需参数
        if not urn:
            return jsonify({
                "success": False,
                "error": "Missing required parameter: urn"
            }), 400

        logger.info(f"生成 Forge Viewer URL 请求: urn={urn}, use_current_token={use_current_token}, version={version}")

        # 标准化 URN 为 fs.file 格式
        normalized_urn = normalize_urn_for_viewer(urn, version=version)

        # 获取 access token
        access_token = None
        if use_current_token:
            # 使用系统的 token
            access_token = get_access_token()
            if not access_token:
                return jsonify({
                    "success": False,
                    "error": "Failed to get access token. Please ensure you are authenticated."
                }), 401
            logger.info(f"使用系统 token: {access_token[:20]}...")
        elif custom_token:
            # 使用自定义 token
            access_token = custom_token
            logger.info(f"使用自定义 token: {access_token[:20]}...")
        else:
            return jsonify({
                "success": False,
                "error": "No token available. Either enable use_current_token or provide a custom token."
            }), 400

        # 对 URN 进行 base64 编码
        try:
            # 使用标准化后的 URN 进行编码
            urn_encoded = base64.b64encode(normalized_urn.encode('utf-8')).decode('utf-8')
            logger.info(f"URN base64 编码成功: {normalized_urn} -> {urn_encoded[:50]}...")
        except Exception as e:
            logger.error(f"URN base64 编码失败: {str(e)}")
            return jsonify({
                "success": False,
                "error": f"Failed to encode URN: {str(e)}"
            }), 400

        # 构建查询参数
        query_params = {
            'urn': urn_encoded,
            'token': access_token
        }

        # 生成完整的 Forge Viewer URL
        viewer_url = f"{FORGE_VIEWER_BASE_URL}?{urlencode(query_params)}"

        # 成功返回
        return jsonify({
            "success": True,
            "data": {
                "viewer_url": viewer_url,
                "urn": urn,
                "urn_normalized": normalized_urn,
                "urn_encoded": urn_encoded,
                "token_used": f"{access_token[:20]}..." if access_token else None,
                "generated_at": datetime.now(timezone.utc).isoformat()
            }
        }), 200

    except Exception as e:
        logger.error(f"生成 Forge Viewer URL 失败: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500


@forge_viewer_bp.route('/forge-viewer/batch-urls', methods=['POST', 'OPTIONS'])
def generate_batch_forge_viewer_urls():
    """
    批量生成 Forge Viewer 预览 URL

    请求体:
        {
            "urns": [
                "urn:adsk.wipprod:fs.file:vf.xxx",
                "urn:adsk.wipprod:fs.file:vf.yyy"
            ],
            "use_current_token": true,  // 可选，默认 true
            "token": "custom_token"     // 可选，自定义 token
        }

    返回:
        {
            "success": true/false,
            "data": {
                "total": 2,
                "results": [
                    {
                        "urn": "urn:adsk.wipprod:fs.file:vf.xxx",
                        "viewer_url": "https://...",
                        "success": true
                    },
                    {
                        "urn": "urn:adsk.wipprod:fs.file:vf.yyy",
                        "viewer_url": "https://...",
                        "success": true
                    }
                ],
                "generated_at": "2025-11-20T10:00:00Z"
            }
        }
    """
    try:
        # 处理 OPTIONS 预检请求
        if request.method == 'OPTIONS':
            return jsonify({"status": "ok"}), 200

        data = request.get_json() or {}
        urns = data.get('urns', [])
        use_current_token = data.get('use_current_token', True)
        custom_token = data.get('token')
        version = data.get('version', 1)

        if not urns or not isinstance(urns, list):
            return jsonify({
                "success": False,
                "error": "Missing or invalid parameter: urns (must be a non-empty array)"
            }), 400

        logger.info(f"批量生成 Forge Viewer URL 请求: {len(urns)} 个 URN, version={version}")

        # 获取 access token
        access_token = None
        if use_current_token:
            access_token = get_access_token()
            if not access_token:
                return jsonify({
                    "success": False,
                    "error": "Failed to get access token. Please ensure you are authenticated."
                }), 401
        elif custom_token:
            access_token = custom_token
        else:
            return jsonify({
                "success": False,
                "error": "No token available. Either enable use_current_token or provide a custom token."
            }), 400

        # 批量处理每个 URN
        results = []
        for urn in urns:
            try:
                # 标准化 URN
                normalized_urn = normalize_urn_for_viewer(urn, version=version)

                # 对 URN 进行 base64 编码
                urn_encoded = base64.b64encode(normalized_urn.encode('utf-8')).decode('utf-8')

                # 构建查询参数
                query_params = {
                    'urn': urn_encoded,
                    'token': access_token
                }

                # 生成完整的 Forge Viewer URL
                viewer_url = f"{FORGE_VIEWER_BASE_URL}?{urlencode(query_params)}"

                results.append({
                    "urn": urn,
                    "urn_normalized": normalized_urn,
                    "urn_encoded": urn_encoded,
                    "viewer_url": viewer_url,
                    "success": True
                })

            except Exception as e:
                logger.error(f"处理 URN {urn} 失败: {str(e)}")
                results.append({
                    "urn": urn,
                    "viewer_url": None,
                    "success": False,
                    "error": str(e)
                })

        # 成功返回
        return jsonify({
            "success": True,
            "data": {
                "total": len(urns),
                "results": results,
                "generated_at": datetime.now(timezone.utc).isoformat()
            }
        }), 200

    except Exception as e:
        logger.error(f"批量生成 Forge Viewer URL 失败: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500


# ============================================================================
# 健康检查端点
# ============================================================================

@forge_viewer_bp.route('/forge-viewer/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        "status": "healthy",
        "service": "forge-viewer-api",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "base_url": FORGE_VIEWER_BASE_URL
    }), 200


# ============================================================================
# Flask 应用集成示例
# ============================================================================

def create_app():
    """创建 Flask 应用（示例）"""
    from flask import Flask

    app = Flask(__name__)

    # 注册蓝图
    app.register_blueprint(forge_viewer_bp)

    return app


if __name__ == '__main__':
    # 本地开发用（不要在生产环境使用）
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)
