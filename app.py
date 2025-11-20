# -*- coding: utf-8 -*-
"""
ACC 表单同步 PoC - 重构后的主应用文件
模块化结构，清晰分离不同功能
請使用start_dev.py來啟動此應用程式
"""

import sys
import os
import tempfile

# 设置控制台编码以支持Unicode字符
if sys.platform.startswith('win'):
    try:
        # 尝试设置UTF-8编码
        os.system('chcp 65001 > nul')
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        # 如果失败，使用ASCII安全模式
        pass

from flask import Flask, redirect, jsonify, request, send_from_directory
from flask_cors import CORS
import config

# 安全的打印函数，处理编码问题
def safe_print(message):
    """安全的打印函数，避免Unicode编码错误"""
    try:
        print(message)
    except UnicodeEncodeError:
        # 如果出现编码错误，使用ASCII安全版本
        safe_message = message.encode('ascii', 'replace').decode('ascii')
        print(safe_message)

# 配置Flask会话
app = Flask(__name__)
app.secret_key = config.SECRET_KEY if hasattr(config, 'SECRET_KEY') else 'your-secret-key-change-in-production'
app.config['SESSION_TYPE'] = 'filesystem'
# Vercel 的可写目录只有 /tmp，强制会话文件写入该处
app.config['SESSION_FILE_DIR'] = os.path.join(tempfile.gettempdir(), 'flask_session')
app.config['SESSION_PERMANENT'] = False

# 初始化Flask-Session
try:
    from flask_session import Session
    Session(app)
    safe_print(f"Flask-Session initialized (Dir: {app.config['SESSION_FILE_DIR']})")
except ImportError:
    safe_print("Warning: Flask-Session not available")
    pass

# 配置CORS - 允许所有本地开发源访问（开发环境）
# Allow all local development origins (development environment)
# 注意：使用正则表达式匹配所有localhost和127.0.0.1的端口，同时支持credentials

import re

# 允許前端來源取自配置（部署時設定 FRONTEND_ORIGIN），本地開發仍允許 localhost
frontend_origin = getattr(config, 'FRONTEND_ORIGIN', 'http://localhost:3000')
cors_origins = [
    re.compile(r"^http://localhost:\d+$"),
    re.compile(r"^http://127\.0\.0\.1:\d+$"),
    frontend_origin
]

CORS(app,
     origins=cors_origins,
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
     allow_headers=["Content-Type", "Authorization", "X-Requested-With", "Accept"],
     expose_headers=["Content-Disposition", "X-File-Count", "X-Total-Size", "X-Failed-Files", "X-File-Size"],
     supports_credentials=True,
     max_age=3600)

# Session cookie 設定，允許跨站 Cookie（HTTPS）
app.config['SESSION_COOKIE_SAMESITE'] = getattr(config, 'SESSION_COOKIE_SAMESITE', 'None')
app.config['SESSION_COOKIE_SECURE'] = getattr(config, 'SESSION_COOKIE_SECURE', True)

# 导入各个模块的蓝图


# 导入文件管理模块蓝图 (从app2.py迁移)
from api_modules.file_CDE_function import file_tree_bp, forge_viewer_bp
from api_modules.file_CDE_function.folder_file_data_api import folder_file_data_bp
from api_modules.file_CDE_function.file_download import file_download_bp

# 导入账户CDE功能模块蓝图 (从app2.py迁移)
# 使用别名避免与现有account_bp冲突
from api_modules.account_CDE_function.account_api import account_bp as account_cde_bp

# 导入工作流CRUD模块蓝图 (从app2.py迁移)
from api_modules.review_CDE_function.workflow_crud_api import workflow_crud_bp

# 导入Transmittal CDE功能模块蓝图
from api_modules.transmittal_CDE_function.transmittal import transmittal_bp

# 导入新的数据库同步API蓝图
try:
    from api_modules.file_sync_db_api import file_sync_db_bp
    FILE_SYNC_DB_API_AVAILABLE = True
except ImportError as e:
    safe_print(f"Warning: File sync database API not available: {e}")
    FILE_SYNC_DB_API_AVAILABLE = False

# 导入Relations API蓝图
try:
    from api_modules.data_management_relations_api import relations_bp
    RELATIONS_API_AVAILABLE = True
except ImportError as e:
    RELATIONS_API_AVAILABLE = False

# 导入新的任務追蹤API（獨立於同步邏輯）
try:
    from api_modules.task_tracking_api import task_tracking_bp
    TASK_TRACKING_API_AVAILABLE = True
    safe_print("✅ Task Tracking API module loaded successfully")
except ImportError as e:
    safe_print(f"⚠️ Task Tracking API module not available: {e}")
    TASK_TRACKING_API_AVAILABLE = False

# 导入優化同步API
try:
    from api_modules.optimized_sync_api import optimized_sync_bp
    OPTIMIZED_SYNC_API_AVAILABLE = True
    safe_print("✅ Optimized Sync API module loaded successfully")
except ImportError as e:
    safe_print(f"⚠️ Optimized Sync API module not available: {e}")
    OPTIMIZED_SYNC_API_AVAILABLE = False

# 导入Review CDE功能模块
try:
    from api_modules.review_CDE_function.review_module_integration import register_review_module_blueprints
    REVIEW_CDE_API_AVAILABLE = True
    safe_print("✅ Review CDE功能模块导入成功")
except ImportError as e:
    safe_print(f"⚠️ Review CDE功能模块不可用: {e}")
    REVIEW_CDE_API_AVAILABLE = False

# Flask应用已在上面创建并配置


# 注册从app2.py迁移的蓝图
app.register_blueprint(file_tree_bp)  # 文件树管理API
app.register_blueprint(forge_viewer_bp)  # Forge Viewer URL 生成 API
app.register_blueprint(folder_file_data_bp)  # 文件夹和文件数据API
app.register_blueprint(file_download_bp)  # 文件下载API
app.register_blueprint(account_cde_bp)  # 账户CDE功能API
app.register_blueprint(workflow_crud_bp)  # 工作流CRUD API
app.register_blueprint(transmittal_bp)  # Transmittal CDE功能API

# 注册Relations API蓝图（如果可用）
if RELATIONS_API_AVAILABLE:
    app.register_blueprint(relations_bp)

# 注册数据库同步API蓝图（如果可用）
if FILE_SYNC_DB_API_AVAILABLE:
    app.register_blueprint(file_sync_db_bp)

# 注册任務追蹤API蓝图（如果可用）
if TASK_TRACKING_API_AVAILABLE:
    app.register_blueprint(task_tracking_bp)
    # 啟動任務管理器
    try:
        from api_modules.task_lifecycle_manager import task_manager
        task_manager.start()
        safe_print("🚀 Task Lifecycle Manager started")
    except Exception as e:
        safe_print(f"⚠️ Failed to start Task Lifecycle Manager: {e}")

# 注册優化同步API蓝图（如果可用）
if OPTIMIZED_SYNC_API_AVAILABLE:
    app.register_blueprint(optimized_sync_bp)
    safe_print("🚀 Optimized Sync API registered successfully")

# 注册Review CDE功能模块（如果可用）
if REVIEW_CDE_API_AVAILABLE:
    register_review_module_blueprints(app)
    safe_print("🚀 Review CDE功能模块已註冊，包含以下API:")
    safe_print("   - Enhanced Approval Workflow API")
    safe_print("   - Review CRUD API")
    safe_print("   - Step Progress API (含委派和返回功能)")
    safe_print("   - Approval Status API")
    safe_print("   - Candidates API (含動態修改功能)")
    safe_print("   - 通知系統API")
    safe_print("   📊 總計約25個API端點已啟用")


# 项目缓存管理API
@app.route('/api/project-cache', methods=['POST'])
def update_project_cache():
    """更新项目缓存信息到session"""
    try:
        from flask import request, session
        
        data = request.get_json()
        if not data:
            return jsonify({
                'status': 'error',
                'error': '无效的请求数据'
            }), 400
        
        project_cache = data.get('project_cache', {})
        
        # 将项目缓存存储到session中
        session['project_cache'] = project_cache
        
        safe_print(f"✅ 项目缓存已更新，包含 {len(project_cache)} 个项目")
        
        return jsonify({
            'status': 'success',
            'message': f'项目缓存已更新，包含 {len(project_cache)} 个项目'
        })
        
    except Exception as e:
        safe_print(f"❌ 更新项目缓存失败: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

@app.route('/api/project-cache', methods=['GET'])
def get_project_cache():
    """获取当前的项目缓存信息"""
    try:
        from flask import session
        
        project_cache = session.get('project_cache', {})
        
        return jsonify({
            'status': 'success',
            'project_cache': project_cache,
            'count': len(project_cache)
        })
        
    except Exception as e:
        safe_print(f"❌ 获取项目缓存失败: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

# ACC_BACKUP 静态文件服务
@app.route('/acc-backup')
def acc_backup_index():
    """ACC备份平台主页"""
    try:
        import os
        from flask import send_from_directory
        acc_backup_dir = os.path.join(os.path.dirname(__file__), 'ACC_BACKUP')
        return send_from_directory(acc_backup_dir, 'index.html')
    except Exception as e:
        safe_print(f"Error serving ACC_BACKUP index: {e}")
        return jsonify({"error": "ACC_BACKUP page not found"}), 404

@app.route('/acc-backup/<path:filename>')
def acc_backup_static(filename):
    """ACC备份平台静态文件服务"""
    try:
        import os
        from flask import send_from_directory
        acc_backup_dir = os.path.join(os.path.dirname(__file__), 'ACC_BACKUP')
        return send_from_directory(acc_backup_dir, filename)
    except Exception as e:
        safe_print(f"Error serving ACC_BACKUP file {filename}: {e}")
        return jsonify({"error": "File not found"}), 404

# 健康检查端点
@app.route('/health')
def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "message": "ACC 数据同步后台服务运行正常",
        "modules": [
            "auth_api - 认证模块",
            "forms_api - Forms API 模块 (包含模板分析)", 
            "data_connector_api - Data Connector API 模块",
            "reviews_api - Reviews API 模块",
            "rfis_api - RFIs API 模块",
            "file_sync_api - 文件同步 API 模块",
            "data_management_api - Data Management API 模块",
            "webhook_api - Webhook 事件通知模块",
            "download_config_api - 下载配置和管理模块",
            "issues_api - Issues API 模块 (议题同步)",
            "submittals_api - Submittals API 模块 (提交资料)",
            "autospecs_packages_api - AutoSpecs 包管理模块",
            "review_workflow_api - 审批工作流模块",
            "system_status_api - 系统状态监控模块",
            "file_sync_db_api - 数据库同步API模块 (NEW)"
        ],
        "endpoints": {
            "auth_api": [
                {"path": "/api/auth/check", "method": "GET", "description": "检查认证状态", "acc_api": None},
                {"path": "/api/auth/token-info", "method": "GET", "description": "获取Token信息", "acc_api": None},
                {"path": "/api/auth/refresh-token", "method": "POST", "description": "刷新Token", "acc_api": "POST https://developer.api.autodesk.com/authentication/v2/token"},
                {"path": "/api/auth/logout", "method": "POST", "description": "用户登出", "acc_api": None},
                {"path": "/api/auth/account-info", "method": "GET", "description": "获取账户信息", "acc_api": "GET https://developer.api.autodesk.com/userprofile/v1/users/@me"},
                {"path": "/api/auth/projects", "method": "GET", "description": "获取用户可访问的项目列表", "acc_api": "GET https://developer.api.autodesk.com/project/v1/hubs/{hubId}/projects"},
                {"path": "/auth/start", "method": "GET", "description": "OAuth认证入口", "acc_api": "GET https://developer.api.autodesk.com/authentication/v2/authorize"}
            ],
            "forms_api": [
                {"path": "/api/forms/jarvis", "method": "GET", "description": "获取项目表单数据", "acc_api": "GET https://developer.api.autodesk.com/construction/forms/v2/projects/{projectId}/forms"},
                {"path": "/api/forms/templates", "method": "GET", "description": "获取表单模板", "acc_api": "GET https://developer.api.autodesk.com/construction/forms/v2/projects/{projectId}/form-templates"},
                {"path": "/api/forms/export-json", "method": "GET", "description": "导出表单JSON", "acc_api": None},
                {"path": "/api/forms/templates/export-json", "method": "GET", "description": "导出模板JSON", "acc_api": None}
            ],
            "data_connector_api": [
                {"path": "/api/data-connector/get-projects", "method": "GET", "description": "获取可用项目", "acc_api": "GET https://developer.api.autodesk.com/project/v1/hubs/{hubId}/projects"},
                {"path": "/api/data-connector/test-format", "method": "POST", "description": "测试数据请求格式", "acc_api": None},
                {"path": "/api/data-connector/create-batch-requests", "method": "POST", "description": "批量创建数据请求", "acc_api": "POST https://developer.api.autodesk.com/construction/dataconnector/v1/exchanges/{exchangeId}/collections/{collectionId}/requests"},
                {"path": "/api/data-connector/list-jobs", "method": "GET", "description": "列出数据作业", "acc_api": "GET https://developer.api.autodesk.com/construction/dataconnector/v1/exchanges/{exchangeId}/collections/{collectionId}/requests/{requestId}/jobs"},
                {"path": "/api/data-connector/get-job-data", "method": "GET", "description": "获取作业数据", "acc_api": "GET https://developer.api.autodesk.com/construction/dataconnector/v1/exchanges/{exchangeId}/collections/{collectionId}/requests/{requestId}/jobs/{jobId}/data"}
            ],
            "reviews_api": [
                {"path": "/api/reviews/jarvis", "method": "GET", "description": "获取项目评审数据", "acc_api": "GET https://developer.api.autodesk.com/construction/reviews/v1/projects/{projectId}/reviews"},
                {"path": "/api/reviews/workflows/jarvis", "method": "GET", "description": "获取工作流数据", "acc_api": "GET https://developer.api.autodesk.com/construction/workflows/v1/projects/{projectId}/workflows"}
            ],
            "rfis_api": [
                {"path": "/api/rfis/jarvis", "method": "GET", "description": "获取项目RFIs数据", "acc_api": "GET https://developer.api.autodesk.com/construction/rfis/v3/projects/{projectId}/rfis"},
                {"path": "/api/rfis/{projectId}/search", "method": "POST", "description": "搜索RFIs", "acc_api": "POST https://developer.api.autodesk.com/construction/rfis/v3/projects/{projectId}/search:rfis"},
                {"path": "/api/rfis/jarvis/{rfiId}", "method": "GET", "description": "获取单个RFI详情", "acc_api": "GET https://developer.api.autodesk.com/construction/rfis/v3/projects/{projectId}/rfis/{rfiId}"},
                {"path": "/api/rfis/jarvis/{rfiId}/attachments", "method": "GET", "description": "获取RFI附件", "acc_api": "GET https://developer.api.autodesk.com/construction/rfis/v3/projects/{projectId}/rfis/{rfiId}/attachments"},
                {"path": "/api/rfis/jarvis/{rfiId}/comments", "method": "GET", "description": "获取RFI评论", "acc_api": "GET https://developer.api.autodesk.com/construction/rfis/v3/projects/{projectId}/rfis/{rfiId}/comments"},
                {"path": "/api/rfis/jarvis/statistics", "method": "GET", "description": "获取RFIs统计分析", "acc_api": None},
                {"path": "/api/rfis/jarvis/users/me", "method": "GET", "description": "获取用户RFI权限", "acc_api": "GET https://developer.api.autodesk.com/construction/rfis/v3/projects/{projectId}/users/me"},
                {"path": "/api/rfis/jarvis/rfi-types", "method": "GET", "description": "获取RFI类型配置", "acc_api": "GET https://developer.api.autodesk.com/construction/rfis/v3/projects/{projectId}/rfi-types"},
                {"path": "/api/rfis/jarvis/attributes", "method": "GET", "description": "获取RFI自定义属性", "acc_api": "GET https://developer.api.autodesk.com/construction/rfis/v3/projects/{projectId}/attributes"},
                {"path": "/api/rfis/jarvis/custom-identifier", "method": "GET", "description": "获取RFI自定义标识符", "acc_api": "GET https://developer.api.autodesk.com/construction/rfis/v3/projects/{projectId}/rfis/custom-identifier"},
                {"path": "/api/rfis/jarvis/workflow", "method": "GET", "description": "获取RFI工作流配置", "acc_api": "GET https://developer.api.autodesk.com/construction/rfis/v3/projects/{projectId}/workflow"}
            ],
            "file_sync_api": [
                {"path": "/api/file-sync/project/{projectId}/tree", "method": "GET", "description": "获取项目完整文件树", "acc_api": "GET https://developer.api.autodesk.com/project/v1/hubs/{hubId}/projects/{projectId}/topFolders"},
                {"path": "/api/file-sync/project/{projectId}/folder/{folderId}", "method": "GET", "description": "获取文件夹子树", "acc_api": "GET https://developer.api.autodesk.com/project/v1/projects/{projectId}/folders/{folderId}/contents"},
                {"path": "/api/file-sync/project/{projectId}/statistics", "method": "GET", "description": "获取项目文件统计", "acc_api": None},
                {"path": "/api/file-sync/download/{projectId}/{itemId}", "method": "GET", "description": "获取文件下载链接", "acc_api": "GET https://developer.api.autodesk.com/project/v1/projects/{projectId}/versions/{versionId}/downloads"}
            ],
            "data_management_api": [
                {"path": "/api/data-management/hubs", "method": "GET", "description": "获取所有Hub", "acc_api": "GET https://developer.api.autodesk.com/project/v1/hubs"},
                {"path": "/api/data-management/hubs/{hubId}/projects", "method": "GET", "description": "获取Hub项目", "acc_api": "GET https://developer.api.autodesk.com/project/v1/hubs/{hubId}/projects"},
                {"path": "/api/data-management/projects/{projectId}/details", "method": "GET", "description": "获取项目详情", "acc_api": "GET https://developer.api.autodesk.com/construction/admin/v1/projects/{projectId}"},
                {"path": "/api/data-management/projects/{projectId}/containers", "method": "GET", "description": "获取项目容器ID", "acc_api": "GET https://developer.api.autodesk.com/project/v1/hubs/{hubId}/projects/{projectId}"},
                {"path": "/api/data-management/projects/{projectId}/folders/{folderId}/metadata", "method": "GET", "description": "获取文件夹元数据", "acc_api": "GET https://developer.api.autodesk.com/project/v1/projects/{projectId}/folders/{folderId}"},
                {"path": "/api/data-management/projects/{projectId}/folders/{folderId}/permissions", "method": "GET", "description": "检查文件夹权限", "acc_api": None},
                {"path": "/api/data-management/projects/{projectId}/items/{itemId}/versions", "method": "GET", "description": "获取文件版本", "acc_api": "GET https://developer.api.autodesk.com/project/v1/projects/{projectId}/items/{itemId}/versions"},
                {"path": "/api/data-management/search", "method": "GET", "description": "搜索项目和文件", "acc_api": None}
            ],
            "issues_api": [
                {"path": "/api/issues/projects/{projectId}/list", "method": "GET", "description": "获取项目议题列表", "acc_api": "GET https://developer.api.autodesk.com/construction/issues/v1/projects/{projectId}/issues"},
                {"path": "/api/issues/projects/{projectId}/issues/{issueId}", "method": "GET", "description": "获取单一议题详情", "acc_api": "GET https://developer.api.autodesk.com/construction/issues/v1/projects/{projectId}/issues/{issueId}"},
                {"path": "/api/issues/projects/{projectId}/issues/{issueId}/comments", "method": "GET", "description": "获取议题留言", "acc_api": "GET https://developer.api.autodesk.com/construction/issues/v1/projects/{projectId}/issues/{issueId}/comments"},
                {"path": "/api/issues/projects/{projectId}/issues/{issueId}/attachments", "method": "GET", "description": "获取议题附件", "acc_api": "GET https://developer.api.autodesk.com/construction/issues/v1/projects/{projectId}/attachments/{issueId}/items"},
                {"path": "/api/issues/projects/{projectId}/sync", "method": "GET", "description": "增量同步议题", "acc_api": None},
                {"path": "/api/issues/projects/{projectId}/statistics", "method": "GET", "description": "获取议题统计", "acc_api": None}
            ],
            "system_status_api": [
                {"path": "/api/system-status/health", "method": "GET", "description": "综合健康检查", "acc_api": None},
                {"path": "/api/system-status/performance", "method": "GET", "description": "获取系统性能指标", "acc_api": None},
                {"path": "/api/system-status/api-endpoints", "method": "GET", "description": "获取API端点状态", "acc_api": None},
                {"path": "/api/system-status/token", "method": "GET", "description": "获取Token状态详情", "acc_api": None},
                {"path": "/api/system-status/modules", "method": "GET", "description": "获取API模块状态", "acc_api": None},
                {"path": "/api/system-status/diagnostics", "method": "GET", "description": "运行系统诊断", "acc_api": None},
                {"path": "/api/system-status/config", "method": "GET", "description": "获取系统配置信息", "acc_api": None},
                {"path": "/api/system-status/cache/clear", "method": "POST", "description": "清除状态缓存", "acc_api": None}
            ],
            "file_sync_db_api": [
                {"path": "/api/file-sync-db/project/{projectId}/full-sync", "method": "POST", "description": "项目全量同步到数据库", "acc_api": None},
                {"path": "/api/file-sync-db/project/{projectId}/incremental-sync", "method": "POST", "description": "项目增量同步到数据库", "acc_api": None},
                {"path": "/api/file-sync-db/project/{projectId}/batch-sync", "method": "POST", "description": "项目批量优化同步到数据库", "acc_api": None},
                {"path": "/api/file-sync-db/project/{projectId}/sync-status", "method": "GET", "description": "获取项目同步状态", "acc_api": None},
                {"path": "/api/file-sync-db/project/{projectId}/sync-history", "method": "GET", "description": "获取项目同步历史记录", "acc_api": None},
                {"path": "/api/file-sync-db/project/{projectId}/folders", "method": "GET", "description": "从数据库获取项目文件夹列表", "acc_api": None},
                {"path": "/api/file-sync-db/project/{projectId}/files", "method": "GET", "description": "从数据库获取项目文件列表", "acc_api": None},
                {"path": "/api/file-sync-db/search", "method": "GET", "description": "搜索文件和文件夹", "acc_api": None},
                {"path": "/api/file-sync-db/health", "method": "GET", "description": "数据库同步健康检查", "acc_api": None}
            ]
        }
    }

# 配置API端点
@app.route('/api/config/monitoring')
def get_monitoring_config():
    """获取监测配置"""
    return jsonify({
        "status": "success",
        "data": {
            "interval_seconds": getattr(config, 'MONITORING_INTERVAL_SECONDS', 30),
            "enabled": getattr(config, 'MONITORING_ENABLED', True)
        }
    })

# 后端首页：显示运行状态
@app.route('/')
def index():
    """後端首頁：只顯示 API 執行狀態"""
    return jsonify({
        "status": "online",
        "message": "ACC-SYNC Python Backend is Running",
        "version": "1.0.0"
    })


# 如果需要跳轉到前端，可啟用以下方案 B
# @app.route('/')
# def index_redirect():
#     frontend_url = os.environ.get('FRONTEND_ORIGIN', 'https://your-frontend.vercel.app')
#     return redirect(frontend_url)

# OAuth认证入口
@app.route('/auth/start')
def start_auth():
    """开始OAuth认证流程"""
    safe_print("[AUTH] /auth/start endpoint called")
    
    try:
        import uuid
        import utils
        from flask import session
        safe_print("[AUTH] Imports successful")
        
        # 检查OAuth配置是否完整
        safe_print(f"[AUTH] Checking OAuth config:")
        safe_print(f"[AUTH]   CLIENT_ID: {config.CLIENT_ID[:10]}...{config.CLIENT_ID[-10:] if config.CLIENT_ID else 'None'}")
        safe_print(f"[AUTH]   CLIENT_SECRET: {'***' if config.CLIENT_SECRET else 'None'}")
        safe_print(f"[AUTH]   CALLBACK_URL: {config.CALLBACK_URL}")
        safe_print(f"[AUTH]   SCOPES: {config.SCOPES}")
        safe_print(f"[AUTH]   AUTH_URL: {config.AUTODESK_AUTH_URL}")
        
        if not config.CLIENT_ID or not config.CLIENT_SECRET or not config.CALLBACK_URL or not config.SCOPES:
            safe_print("[AUTH] OAuth configuration incomplete")
            return utils.generate_html_response(
                "配置错误",
                '''
                <div class="error">
                    <h2>OAuth配置不完整</h2>
                    <p>请设置以下环境变量：</p>
                    <ul>
                        <li>AUTODESK_CLIENT_ID</li>
                        <li>AUTODESK_CLIENT_SECRET</li>
                        <li>AUTODESK_CALLBACK_URL</li>
                        <li>AUTODESK_SCOPES</li>
                    </ul>
                    <p>或者创建 .env 文件并设置这些变量。</p>
                </div>
                '''
            )
        
        safe_print("[AUTH] OAuth configuration is complete")
        
        # 清理之前的认证状态
        safe_print("[AUTH] Clearing previous authentication state")
        session.pop('oauth_state', None)
        session.pop('access_token', None)
        session.pop('refresh_token', None)
        session.pop('token_expires_at', None)
        
        # 清理内存中的token存储（避免使用可能阻塞的utils.clear_tokens）
        try:
            # 直接清理内存存储，避免session相关的操作
            with utils._token_lock:
                utils._token_storage.update({
                    'access_token': None,
                    'refresh_token': None,
                    'expires_at': None,
                    'updated_at': None,
                    'refresh_attempts': 0,
                    'last_refresh_attempt': None,
                    'next_auto_refresh_at': None
                })
            safe_print("[AUTH] Memory tokens cleared")
        except Exception as e:
            safe_print(f"[AUTH] Failed to clear memory tokens: {e}")
        
        # 生成唯一的state参数来防止CSRF攻击和重复请求
        state = str(uuid.uuid4())
        session['oauth_state'] = state
        safe_print(f"[AUTH] Generated OAuth state: {state}")
        
        auth_url = f"{config.AUTODESK_AUTH_URL}/authorize"
        params = {
            'response_type': 'code',
            'client_id': config.CLIENT_ID,
            'redirect_uri': config.CALLBACK_URL,
            'scope': config.SCOPES,
            'state': state
        }
        
        # 正确编码URL参数，特别是scope参数包含空格
        from urllib.parse import urlencode
        query_string = urlencode(params)
        
        final_url = f"{auth_url}?{query_string}"
        safe_print(f"[AUTH] Generated OAuth URL components:")
        safe_print(f"[AUTH]   Base URL: {auth_url}")
        safe_print(f"[AUTH]   Query params: {query_string}")
        safe_print(f"[AUTH]   Final URL: {final_url}")
        safe_print(f"[AUTH] Redirecting to Autodesk OAuth...")
        
        return redirect(final_url)
        
    except Exception as e:
        safe_print(f"[AUTH] Error in /auth/start: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"Error in authentication start: {str(e)}", 500


if __name__ == '__main__':
    import signal
    import utils
    import atexit
    import time
    
    # 设置启动时间
    config.START_TIME = time.time()
    
    # 全局标志，防止重复清理
    _cleanup_done = False
    
    def cleanup_resources():
        """统一的资源清理函数"""
        global _cleanup_done
        if _cleanup_done:
            return
        _cleanup_done = True
        
        safe_print("Cleaning up resources...")
        utils.stop_background_token_monitor()
        
        # 关闭下载线程池
        try:
            from api_modules.download_config_api import shutdown_executor
            shutdown_executor()
        except Exception as e:
            safe_print(f"Error shutting down download executor: {e}")
        
        safe_print("Background services stopped")
    
    def signal_handler(signum, frame):
        """处理退出信号，确保正确清理资源"""
        safe_print(f"\nReceived signal {signum}, shutting down gracefully...")
        cleanup_resources()
        safe_print("Application closed")
        sys.exit(0)
    
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    if hasattr(signal, 'SIGTERM'):
        signal.signal(signal.SIGTERM, signal_handler)  # 终止信号（Unix）
    
    # 注册退出时清理函数（作为备用）
    atexit.register(cleanup_resources)
    
    safe_print("Starting ACC Form Sync PoC Service...")
    safe_print(f"Configuration:")
    safe_print(f"   - Client ID: {config.CLIENT_ID}")
    safe_print(f"   - Callback URL: {config.CALLBACK_URL}")
    safe_print(f"   - Scopes: {config.SCOPES}")
    safe_print(f"   - Debug: {config.DEBUG}")
    safe_print(f"   - Port: {config.PORT}")
    safe_print(f"   - Auto Token Refresh: {config.AUTO_REFRESH_ENABLED}")
    safe_print("Service starting...")
    
    # 启动后台token监控器
    if config.AUTO_REFRESH_ENABLED:
        utils.start_background_token_monitor()
    else:
        safe_print("Warning: Auto token refresh is disabled")
    
    try:
        app.run(debug=config.DEBUG, host='127.0.0.1', port=config.PORT, threaded=True, use_reloader=False)
    except KeyboardInterrupt:
        # 这个异常会被信号处理器处理，这里不需要额外处理
        pass
    except Exception as e:
        safe_print(f"Server error: {e}")
    finally:
        # 确保资源被清理（如果信号处理器没有被调用）
        cleanup_resources()
        safe_print("Application closed")
