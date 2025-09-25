# -*- coding: utf-8 -*-
"""
ACC 表单同步 PoC - 重构后的主应用文件
模块化结构，清晰分离不同功能
"""

from flask import Flask, redirect, jsonify
from flask_cors import CORS
import config

# 配置Flask会话
app = Flask(__name__)
app.secret_key = config.SECRET_KEY if hasattr(config, 'SECRET_KEY') else 'your-secret-key-change-in-production'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False

# 配置CORS - 允许Vue前端访问并支持cookies
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    },
    r"/health": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
        "supports_credentials": True
    },
    r"/auth/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "supports_credentials": True
    }
})

# 导入各个模块的蓝图
from api_modules.auth_api import auth_bp
from api_modules.forms_api import forms_bp
from api_modules.data_connector_api import data_connector_bp
from api_modules.reviews_api import reviews_bp

# Flask应用已在上面创建并配置

# 注册蓝图
app.register_blueprint(auth_bp)
app.register_blueprint(forms_bp)
app.register_blueprint(data_connector_bp)
app.register_blueprint(reviews_bp)

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
            "reviews_api - Reviews API 模块"
        ],
        "endpoints": {
            "auth_api": [
                {"path": "/api/auth/check", "method": "GET", "description": "检查认证状态", "acc_api": None},
                {"path": "/api/auth/token-info", "method": "GET", "description": "获取Token信息", "acc_api": None},
                {"path": "/api/auth/refresh-token", "method": "POST", "description": "刷新Token", "acc_api": "POST https://developer.api.autodesk.com/authentication/v2/token"},
                {"path": "/api/auth/logout", "method": "POST", "description": "用户登出", "acc_api": None},
                {"path": "/api/auth/account-info", "method": "GET", "description": "获取账户信息", "acc_api": "GET https://developer.api.autodesk.com/userprofile/v1/users/@me"},
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

# Vue前端路由
@app.route('/api')
@app.route('/')
def vue_app():
    """Vue前端应用 - 根据环境选择开发或生产版本"""
    import os
    
    # 生产环境：检查构建后的Vue文件
    if os.path.exists('static/dist/index.html'):
        return app.send_static_file('dist/index.html')
    
    # 开发环境：直接重定向到Vue开发服务器
    # 认证检查由Vue前端的路由守卫处理
    return redirect('http://localhost:3000/')

# OAuth认证入口
@app.route('/auth/start')
def start_auth():
    """开始OAuth认证流程"""
    import uuid
    from flask import session
    
    # 清理之前的认证状态
    session.pop('oauth_state', None)
    session.pop('access_token', None)
    session.pop('refresh_token', None)
    session.pop('token_expires_at', None)
    
    # 清理内存中的token存储
    import utils
    utils.clear_tokens()
    
    # 生成唯一的state参数来防止CSRF攻击和重复请求
    state = str(uuid.uuid4())
    session['oauth_state'] = state
    
    auth_url = f"{config.AUTODESK_AUTH_URL}/authorize"
    params = {
        'response_type': 'code',
        'client_id': config.CLIENT_ID,
        'redirect_uri': config.CALLBACK_URL,
        'scope': config.SCOPES,
        'state': state
    }
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    
    print(f"Starting OAuth flow with state: {state}")
    return redirect(f"{auth_url}?{query_string}")

if __name__ == '__main__':
    print("🎯 启动 ACC 表单同步 PoC 服务...")
    print(f"🔧 配置信息:")
    print(f"   - Client ID: {config.CLIENT_ID}")
    print(f"   - Callback URL: {config.CALLBACK_URL}")
    print(f"   - Scopes: {config.SCOPES}")
    print(f"   - Debug: {config.DEBUG}")
    print(f"   - Port: {config.PORT}")
    print(f"   - Auto Token Refresh: {config.AUTO_REFRESH_ENABLED}")
    print("🚀 服务启动中...")
    
    # 启动后台token监控器
    import utils
    if config.AUTO_REFRESH_ENABLED:
        utils.start_background_token_monitor()
    else:
        print("⚠️ 自动token刷新已禁用")
    
    try:
        app.run(debug=config.DEBUG, host='127.0.0.1', port=config.PORT)
    finally:
        # 应用关闭时停止后台监控器
        utils.stop_background_token_monitor()
        print("👋 应用已关闭")
