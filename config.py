# -*- coding: utf-8 -*-
"""
配置文件
包含所有应用配置常量
"""

import os

#khalil test
CLIENT_ID = os.getenv('AUTODESK_CLIENT_ID', 'yQBYQHFIEOMwXwen4lBauTmepwTntzIXOuSr9vMKJGRpqh7w')
CLIENT_SECRET = os.getenv('AUTODESK_CLIENT_SECRET', 'PONH9545nWHJJUfVzvDzJe0MUoni1v5ov3PRHNz4Gy0h5WquHsaNTpe8wwsh3t6y')
CALLBACK_URL = os.getenv('AUTODESK_CALLBACK_URL', 'http://localhost:8080/api/auth/callback')
# 前端來源（用於回調 postMessage/redirect），可在部署時設定，例如 https://app.example.com
FRONTEND_ORIGIN = os.getenv('FRONTEND_ORIGIN', 'http://localhost:3000')
# 更新scope权限，添加bucket相关权限以支持文件下载
SCOPES = 'account:read account:write data:read data:write data:create viewables:read bucket:read bucket:create'

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

# 项目配置说明
# 注意：从版本2.0开始，应用程序使用动态项目选择
# 不再依赖硬编码的项目ID，所有API调用都需要通过projectId参数指定项目


# Flask 配置
DEBUG = True
PORT = 8080

# 跨域/Session 設置（跨站 Cookie 需要 SameSite=None 且 Secure）
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True

# Flask会话密钥 - 生产环境中应该使用更安全的密钥
SECRET_KEY = 'acc-forms-sync-poc-secret-key-change-in-production'

# 监测配置
MONITORING_INTERVAL_SECONDS = 30  # 监察间隔（秒）- 默认30秒
MONITORING_ENABLED = True  # 是否启用监测功能

# 数据库同步配置
ENABLE_REVIEW_SYNC = True  # 启用Review数据同步
ENABLE_FILE_SYNC = True    # 启用文件数据同步

# 系统状态API配置
VERSION = '2.1.0'  # 系统版本号
START_TIME = None  # 启动时间，将在应用启动时设置
SYSTEM_STATUS_CACHE_DURATION = 30  # 系统状态缓存时间（秒）

# 企业账户映射配置
# 当Hub API无法访问时，使用此映射来识别企业用户
ENTERPRISE_ACCOUNT_MAPPING = {
    'khalil.chiu@isbim.com.hk': {
        'account_id': '1caef42c-9fb7-4e6f-a5d1-cb89e69de6ea',
        'hub_id': 'b.1caef42c-9fb7-4e6f-a5d1-cb89e69de6ea',
        'hub_name': 'isbim Enterprise Account'
    }
    # 可以在这里添加更多企业用户映射
}
