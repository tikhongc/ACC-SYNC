"""
同步配置文件
定义增强同步管理器的配置选项
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class SyncConfig:
    """同步配置"""
    
    # 并发控制
    max_concurrent: int = 10  # 最大并发数
    batch_size: int = 100  # 批量操作大小
    
    # Redis缓存配置
    enable_cache: bool = True  # 是否启用缓存
    cache_ttl: int = 3600  # 缓存过期时间（秒）
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_db: int = 0
    
    # 断路器配置
    circuit_breaker_threshold: int = 5  # 失败阈值
    circuit_breaker_timeout: int = 60  # 超时时间（秒）
    
    # 重试配置
    max_retries: int = 3  # 最大重试次数
    retry_backoff_factor: float = 2.0  # 退避因子
    
    # 性能监控
    enable_performance_tracking: bool = True
    enable_memory_profiling: bool = False
    
    # 日志配置
    log_level: str = 'INFO'
    log_to_file: bool = True
    log_file_path: Optional[str] = None
    
    @classmethod
    def development(cls) -> 'SyncConfig':
        """开发环境配置"""
        return cls(
            max_concurrent=5,
            batch_size=50,
            enable_cache=False,
            log_level='DEBUG'
        )
    
    @classmethod
    def production(cls) -> 'SyncConfig':
        """生产环境配置"""
        return cls(
            max_concurrent=20,
            batch_size=200,
            enable_cache=True,
            cache_ttl=7200,
            log_level='INFO',
            log_to_file=True
        )
    
    @classmethod
    def testing(cls) -> 'SyncConfig':
        """测试环境配置"""
        return cls(
            max_concurrent=3,
            batch_size=10,
            enable_cache=False,
            log_level='DEBUG'
        )


# 预定义配置
DEV_CONFIG = SyncConfig.development()
PROD_CONFIG = SyncConfig.production()
TEST_CONFIG = SyncConfig.testing()

