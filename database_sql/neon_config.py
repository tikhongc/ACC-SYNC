# -*- coding: utf-8 -*-
"""
Neon PostgreSQL数据库配置
使用Neon云端PostgreSQL服务
"""

import os
from typing import Optional
import asyncpg
import asyncio
from contextlib import asynccontextmanager
import logging

logger = logging.getLogger(__name__)

class NeonPostgreSQLConfig:
    """Neon PostgreSQL数据库配置类"""
    
    def __init__(self):
        # Neon PostgreSQL连接配置
        # 从您提供的连接字符串解析
        self.connection_url = "postgresql://neondb_owner:npg_a2nxljG8LOSP@ep-soft-mountain-a4jqpy5e-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
        
        # 分离的连接参数
        self.host = "ep-soft-mountain-a4jqpy5e-pooler.us-east-1.aws.neon.tech"
        self.port = 5432
        self.database = "neondb"
        self.user = "neondb_owner"
        self.password = "npg_a2nxljG8LOSP"
        
        # SSL配置（Neon要求SSL）
        self.ssl = "require"
        self.channel_binding = "require"
        
        # 连接池配置
        self.min_connections = 2
        self.max_connections = 10
        self.connection_timeout = 30
        
        # 连接池实例
        self._pool: Optional[asyncpg.Pool] = None
    
    @property
    def connection_string(self) -> str:
        """获取连接字符串"""
        return self.connection_url
    
    @property
    def connection_string_safe(self) -> str:
        """获取安全的连接字符串（隐藏密码）"""
        return f"postgresql://{self.user}:***@{self.host}:{self.port}/{self.database}?sslmode={self.ssl}&channel_binding={self.channel_binding}"
    
    async def create_pool(self) -> asyncpg.Pool:
        """创建连接池"""
        if self._pool is None:
            try:
                logger.info(f"正在创建Neon PostgreSQL连接池: {self.connection_string_safe}")
                
                # 使用连接字符串创建连接池
                self._pool = await asyncpg.create_pool(
                    dsn=self.connection_url,
                    min_size=self.min_connections,
                    max_size=self.max_connections,
                    command_timeout=self.connection_timeout,
                    server_settings={
                        'application_name': 'ACC_SYNC_NEON',
                        'timezone': 'UTC'
                    }
                )
                
                logger.info("Neon PostgreSQL连接池创建成功")
                
                # 测试连接
                async with self._pool.acquire() as conn:
                    version = await conn.fetchval("SELECT version()")
                    logger.info(f"Neon PostgreSQL版本: {version[:100]}...")
                    
                    # 测试数据库信息
                    db_name = await conn.fetchval("SELECT current_database()")
                    current_user = await conn.fetchval("SELECT current_user")
                    logger.info(f"数据库: {db_name}, 用户: {current_user}")
                
            except Exception as e:
                logger.error(f"创建Neon PostgreSQL连接池失败: {str(e)}")
                raise
        
        return self._pool
    
    async def close_pool(self):
        """关闭连接池"""
        if self._pool:
            logger.info("正在关闭Neon PostgreSQL连接池")
            await self._pool.close()
            self._pool = None
            logger.info("Neon PostgreSQL连接池已关闭")
    
    @asynccontextmanager
    async def get_connection(self):
        """获取数据库连接的上下文管理器"""
        if self._pool is None:
            await self.create_pool()
        
        async with self._pool.acquire() as connection:
            try:
                yield connection
            except Exception as e:
                logger.error(f"数据库操作错误: {str(e)}")
                raise

# 全局Neon PostgreSQL配置实例
neon_postgresql_config = NeonPostgreSQLConfig()

# 便捷函数
async def get_neon_postgresql_pool():
    """获取Neon PostgreSQL连接池"""
    return await neon_postgresql_config.create_pool()

async def close_neon_postgresql_pool():
    """关闭Neon PostgreSQL连接池"""
    await neon_postgresql_config.close_pool()


class NeonConfig:
    """Synchronous Neon PostgreSQL configuration for psycopg2"""
    
    def __init__(self):
        # Use the same connection details as NeonPostgreSQLConfig
        self.host = "ep-soft-mountain-a4jqpy5e-pooler.us-east-1.aws.neon.tech"
        self.port = 5432
        self.database = "neondb"
        self.user = "neondb_owner"
        self.password = "npg_a2nxljG8LOSP"
        self.ssl = "require"
    
    def get_db_params(self) -> dict:
        """Get database connection parameters for psycopg2"""
        return {
            'host': self.host,
            'port': self.port,
            'database': self.database,
            'user': self.user,
            'password': self.password,
            'sslmode': self.ssl
        }
    
    def get_connection_string(self) -> str:
        """Get connection string"""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?sslmode={self.ssl}"

if __name__ == "__main__":
    # 直接运行此文件进行连接测试
    async def main():
        # 设置日志级别
        logging.basicConfig(level=logging.INFO)
        
        try:
            pool = await get_neon_postgresql_pool()
            print("🎉 Neon PostgreSQL连接配置成功!")
        except Exception as e:
            print(f"💥 Neon PostgreSQL连接配置失败: {e}")
        finally:
            await close_neon_postgresql_pool()
    
    asyncio.run(main())