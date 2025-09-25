# -*- coding: utf-8 -*-
"""
配置文件
包含所有应用配置常量
"""

# OAuth 配置
CLIENT_ID = 'bGDqFEODECJApej6by82LNnAKAduq5RPQgPSaJoOBPNsV9AS'
CLIENT_SECRET = 'u0X9nVgKpajuAWdTprkgXK9SYhbTuQABG4csXEA9TuWMx0vVAwQekYWDdtSqhAYg'  # 需要设置真实的 secret
CALLBACK_URL = 'http://localhost:8080/api/auth/callback'
SCOPES = 'account:read data:read data:write data:create data:search viewables:read'

# OAuth优化配置 - 请求更长的token有效期
OAUTH_ADDITIONAL_PARAMS = {
    'access_type': 'offline',  # 请求refresh_token
    'prompt': 'consent',       # 强制显示同意页面以获取refresh_token
    'duration': 'permanent'    # 请求永久授权
}

# Token配置 - 优化设置
TOKEN_REFRESH_THRESHOLD = 600  # 提前10分钟刷新token
MAX_TOKEN_REFRESH_ATTEMPTS = 3  # 最大刷新尝试次数
AUTO_REFRESH_ENABLED = True  # 启用自动刷新
PERSISTENT_TOKEN_STORAGE = True  # 启用持久化存储

# API 端点
AUTODESK_AUTH_URL = "https://developer.api.autodesk.com/authentication/v2"
AUTODESK_API_BASE = "https://developer.api.autodesk.com"

# 默认项目ID (JARVIS 2025 Dev)
JARVIS_PROJECT_ID = "b.a5d9ae79-8653-4de1-bf7a-9dcbbe4db13e"

# Flask 配置
DEBUG = True
PORT = 8080

# Flask会话密钥 - 生产环境中应该使用更安全的密钥
SECRET_KEY = 'acc-forms-sync-poc-secret-key-change-in-production'

# 监测配置
MONITORING_INTERVAL_SECONDS = 30  # 监察间隔（秒）- 默认30秒
MONITORING_ENABLED = True  # 是否启用监测功能
