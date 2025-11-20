#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件树 API - Flask 端点

提供两个核心接口：
1. GET /api/file-tree - 获取文件树（优先使用缓存）
2. POST /api/file-tree/invalidate - 清空缓存
"""

from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
from typing import Dict, Tuple
import logging
import traceback
import sys
import os

# 为了支持相对导入和直接导入，使用 try-except
try:
    from .file_tree_builder import get_file_tree, invalidate_file_tree_cache
except ImportError:
    from file_tree_builder import get_file_tree, invalidate_file_tree_cache

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建蓝图
file_tree_bp = Blueprint('file_tree', __name__, url_prefix='/api')


# ============================================================================
# 配置 - 数据库连接参数（应该从环境变量或配置文件读取）
# ============================================================================

def get_db_params() -> Dict[str, str]:
    """获取数据库连接参数"""
    return {
        'host': "ep-soft-mountain-a4jqpy5e-pooler.us-east-1.aws.neon.tech",
        'port': 5432,
        'database': "neondb",
        'user': "neondb_owner",
        'password': "npg_a2nxljG8LOSP",
        'sslmode': 'require'
    }


# ============================================================================
# API 端点
# ============================================================================

@file_tree_bp.route('/file-tree', methods=['GET'])
def get_file_tree_api():
    """
    获取文件树 API

    查询参数:
        - project_id (必需): 项目ID
        - force_refresh (可选): 是否强制刷新缓存 (true/false)

    返回:
        {
            "success": true/false,
            "data": { tree structure } or null,
            "from_cache": true/false,
            "metadata": {
                "cached_at": "2025-11-16T10:00:00Z",
                "cache_hit": true/false,
                "message": "..."
            },
            "error": "error message" (if success=false)
        }
    """
    try:
        # 验证请求参数
        project_id = request.args.get('project_id')
        force_refresh = request.args.get('force_refresh', 'false').lower() == 'true'

        if not project_id:
            return jsonify({
                "success": False,
                "error": "Missing required parameter: project_id"
            }), 400

        logger.info(f"获取文件树请求: project_id={project_id}, force_refresh={force_refresh}")

        # 获取数据库连接参数
        db_params = get_db_params()

        # 调用业务逻辑
        tree, from_cache = get_file_tree(project_id, db_params, force_refresh)

        if tree is None:
            return jsonify({
                "success": False,
                "error": "Failed to build file tree",
                "metadata": {
                    "project_id": project_id
                }
            }), 500

        # 成功返回
        return jsonify({
            "success": True,
            "data": tree,
            "from_cache": from_cache,
            "metadata": {
                "project_id": project_id,
                "cached_at": datetime.now(timezone.utc).isoformat(),
                "cache_hit": from_cache,
                "message": "Cache hit" if from_cache else "Cache miss - tree rebuilt"
            }
        }), 200

    except Exception as e:
        logger.error(f"获取文件树失败: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500


@file_tree_bp.route('/file-tree/invalidate', methods=['POST'])
def invalidate_file_tree_cache_api():
    """
    清空文件树缓存 API

    请求体:
        {
            "project_id": "project-id-xxx"
        }

    返回:
        {
            "success": true/false,
            "data": {
                "project_id": "...",
                "invalidated_at": "2025-11-16T10:00:00Z"
            },
            "error": "error message" (if success=false)
        }
    """
    try:
        # 获取请求数据
        data = request.get_json() or {}
        project_id = data.get('project_id')

        if not project_id:
            return jsonify({
                "success": False,
                "error": "Missing required parameter: project_id"
            }), 400

        logger.info(f"清空文件树缓存请求: project_id={project_id}")

        # 获取数据库连接参数
        db_params = get_db_params()

        # 调用业务逻辑
        success = invalidate_file_tree_cache(project_id, db_params)

        if not success:
            return jsonify({
                "success": False,
                "error": "Failed to invalidate cache",
                "data": {
                    "project_id": project_id
                }
            }), 500

        # 成功返回
        return jsonify({
            "success": True,
            "data": {
                "project_id": project_id,
                "invalidated_at": datetime.now(timezone.utc).isoformat()
            }
        }), 200

    except Exception as e:
        logger.error(f"清空缓存失败: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500


@file_tree_bp.route('/file-tree/cache-status', methods=['GET'])
def get_cache_status_api():
    """
    获取缓存状态 API（辅助接口）

    查询参数:
        - project_id (必需): 项目ID

    返回:
        {
            "success": true/false,
            "data": {
                "project_id": "...",
                "cached": true/false,
                "cache_size_bytes": 1024,
                "total_folders": 10,
                "total_files": 50,
                "last_updated": "2025-11-16T10:00:00Z",
                "last_build_time_ms": 150.5
            }
        }
    """
    try:
        project_id = request.args.get('project_id')

        if not project_id:
            return jsonify({
                "success": False,
                "error": "Missing required parameter: project_id"
            }), 400

        logger.info(f"获取缓存状态请求: project_id={project_id}")

        # 获取数据库连接参数
        db_params = get_db_params()

        # 连接数据库查询缓存状态
        import psycopg2
        import psycopg2.extras

        try:
            conn = psycopg2.connect(**db_params)
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            sql = """
            SELECT
                project_id,
                (cached_tree IS NOT NULL) as cached,
                tree_size_bytes,
                total_folders,
                total_files,
                last_updated,
                last_build_time_ms
            FROM file_tree_cache
            WHERE project_id = %s
            """

            cur.execute(sql, (project_id,))
            result = cur.fetchone()
            cur.close()
            conn.close()

            if result:
                return jsonify({
                    "success": True,
                    "data": {
                        "project_id": result['project_id'],
                        "cached": result['cached'],
                        "cache_size_bytes": result['tree_size_bytes'],
                        "total_folders": result['total_folders'],
                        "total_files": result['total_files'],
                        "last_updated": result['last_updated'].isoformat() if result['last_updated'] else None,
                        "last_build_time_ms": float(result['last_build_time_ms']) if result['last_build_time_ms'] else None
                    }
                }), 200
            else:
                return jsonify({
                    "success": True,
                    "data": {
                        "project_id": project_id,
                        "cached": False,
                        "cache_size_bytes": 0,
                        "message": "No cache entry found"
                    }
                }), 200

        except Exception as e:
            logger.error(f"查询缓存状态失败: {str(e)}")
            return jsonify({
                "success": False,
                "error": f"Failed to query cache status: {str(e)}"
            }), 500

    except Exception as e:
        logger.error(f"获取缓存状态失败: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500


# ============================================================================
# 健康检查端点
# ============================================================================

@file_tree_bp.route('/file-tree/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        "status": "healthy",
        "service": "file-tree-api",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 200


# ============================================================================
# Flask 应用集成示例
# ============================================================================

def create_app():
    """创建 Flask 应用（示例）"""
    from flask import Flask

    app = Flask(__name__)

    # 注册蓝图
    app.register_blueprint(file_tree_bp)

    return app


if __name__ == '__main__':
    # 本地开发用（不要在生产环境使用）
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
