# -*- coding: utf-8 -*-
"""
Neon PostgreSQL环境配置
从您提供的连接信息配置
"""

# Neon PostgreSQL连接配置
DATABASE_URL = "postgresql://neondb_owner:npg_a2nxljG8LOSP@ep-soft-mountain-a4jqpy5e-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# 分离的连接参数
NEON_DB_USER = "neondb_owner"
NEON_DB_PASSWORD = "npg_a2nxljG8LOSP"
NEON_DB_HOST = "ep-soft-mountain-a4jqpy5e-pooler.us-east-1.aws.neon.tech"
NEON_DB_PORT = "5432"
NEON_DB_NAME = "neondb"

# SSL配置
NEON_SSL_MODE = "require"
NEON_CHANNEL_BINDING = "require"
