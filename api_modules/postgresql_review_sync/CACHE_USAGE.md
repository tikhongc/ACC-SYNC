# 缓存使用说明 - Cachetools 替代 Redis

## 概述

本项目已将 Redis 缓存替换为 **cachetools** 内存缓存，适合部署到网站环境。

## 优势

✅ **无需额外服务** - 不需要部署和维护 Redis 服务器  
✅ **线程安全** - 支持多线程 Web 环境（Flask/Django）  
✅ **自动过期** - TTL 自动清理过期数据  
✅ **内存可控** - 自动 LRU 淘汰，防止内存溢出  
✅ **高性能** - 纯内存操作，速度快  
✅ **易于部署** - 只需 `pip install cachetools`

## 安装

```bash
pip install cachetools
```

或使用项目的 requirements.txt：

```bash
pip install -r config/requirements.txt
```

## 基本使用

### 1. 创建同步管理器

```python
from api_modules.postgresql_review_sync.review_sync_manager_enhanced import (
    EnhancedReviewSyncManager,
    get_enhanced_sync_manager
)

# 方式 1: 直接创建
sync_manager = EnhancedReviewSyncManager(
    max_concurrent=10,
    enable_cache=True,
    cache_ttl=3600,        # 缓存过期时间：1小时
    cache_max_size=5000,   # 最多缓存5000个条目
    batch_size=100
)

# 方式 2: 使用便捷函数
sync_manager = get_enhanced_sync_manager(
    max_concurrent=10,
    enable_cache=True,
    cache_ttl=3600,
    cache_max_size=5000,
    batch_size=100
)
```

### 2. 查看缓存统计

```python
# 获取缓存统计信息
cache_stats = sync_manager.cache.get_stats()
print(cache_stats)

# 输出示例:
# {
#     'enabled': True,
#     'current_size': 234,
#     'max_size': 5000,
#     'ttl': 3600,
#     'usage_percent': 4.68
# }
```

### 3. 手动操作缓存

```python
# 获取缓存
value = sync_manager.cache.get('api', 'some_key')

# 设置缓存
sync_manager.cache.set('api', 'some_key', value={'data': 'test'})

# 删除缓存
sync_manager.cache.delete('api', 'some_key')

# 清除匹配模式的缓存
count = sync_manager.cache.clear_pattern('api:')

# 清空所有缓存
sync_manager.cache.clear_all()
```

## 配置建议

根据网站规模选择合适的配置：

### 小型网站（< 1000 用户）

```python
sync_manager = EnhancedReviewSyncManager(
    enable_cache=True,
    cache_ttl=3600,      # 1小时
    cache_max_size=1000  # 1000条目
)
```

### 中型网站（1000-10000 用户）

```python
sync_manager = EnhancedReviewSyncManager(
    enable_cache=True,
    cache_ttl=1800,      # 30分钟
    cache_max_size=5000  # 5000条目
)
```

### 大型网站（> 10000 用户）

```python
sync_manager = EnhancedReviewSyncManager(
    enable_cache=True,
    cache_ttl=900,        # 15分钟
    cache_max_size=10000  # 10000条目
)
```

## 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `enable_cache` | bool | True | 是否启用缓存 |
| `cache_ttl` | int | 3600 | 缓存过期时间（秒） |
| `cache_max_size` | int | 1000 | 最大缓存条目数 |

## 性能监控

```python
# 获取完整性能报告
report = sync_manager.get_performance_report()

# 查看缓存命中率
cache_hit_rate = sync_manager.metrics.get_cache_hit_rate()
print(f"缓存命中率: {cache_hit_rate:.2f}%")

# 打印性能报告
sync_manager.print_performance_report()
```

## 与 Redis 的对比

| 特性 | Cachetools | Redis |
|------|-----------|-------|
| 部署复杂度 | ⭐ 简单 | ⭐⭐⭐ 复杂 |
| 性能 | ⭐⭐⭐⭐⭐ 极快 | ⭐⭐⭐⭐ 快 |
| 内存管理 | ⭐⭐⭐⭐ 自动 | ⭐⭐⭐ 需配置 |
| 持久化 | ❌ 不支持 | ✅ 支持 |
| 分布式 | ❌ 单进程 | ✅ 支持 |
| 线程安全 | ✅ 是 | ✅ 是 |
| 适用场景 | 单机Web应用 | 分布式系统 |

## 注意事项

1. **重启丢失** - 缓存数据存储在内存中，应用重启后会丢失
2. **单进程** - 如果使用多进程部署（如 Gunicorn），每个进程有独立的缓存
3. **内存占用** - 根据 `cache_max_size` 和数据大小，合理配置避免内存溢出

## 多进程部署建议

如果使用 Gunicorn 等多进程部署：

```bash
# 方案 1: 使用单进程 + 多线程
gunicorn -w 1 -k gthread --threads 4 app:app

# 方案 2: 如需多进程，考虑使用 Redis
# 每个进程有独立缓存，可能导致缓存命中率降低
gunicorn -w 4 app:app
```

## 迁移指南

从 Redis 迁移到 Cachetools 只需修改初始化参数：

```python
# 旧代码（Redis）
sync_manager = EnhancedReviewSyncManager(
    enable_cache=True,
    cache_ttl=3600,
    redis_host='localhost',  # ❌ 删除
    redis_port=6379,         # ❌ 删除
    batch_size=100
)

# 新代码（Cachetools）
sync_manager = EnhancedReviewSyncManager(
    enable_cache=True,
    cache_ttl=3600,
    cache_max_size=5000,     # ✅ 新增
    batch_size=100
)
```

## 故障排除

### 问题 1: 缓存未启用

```python
cache_stats = sync_manager.cache.get_stats()
if not cache_stats.get('enabled'):
    print("缓存未启用，请检查 cachetools 是否已安装")
    # 解决方案: pip install cachetools
```

### 问题 2: 内存占用过高

```python
# 减小缓存大小
sync_manager = EnhancedReviewSyncManager(
    cache_max_size=1000  # 从 5000 减少到 1000
)

# 或缩短过期时间
sync_manager = EnhancedReviewSyncManager(
    cache_ttl=900  # 从 3600 减少到 900（15分钟）
)
```

### 问题 3: 缓存命中率低

```python
# 增加缓存大小
sync_manager = EnhancedReviewSyncManager(
    cache_max_size=10000  # 增加到 10000
)

# 延长过期时间
sync_manager = EnhancedReviewSyncManager(
    cache_ttl=7200  # 增加到 2 小时
)
```

## 示例代码

完整的使用示例：

```python
import asyncio
from api_modules.postgresql_review_sync.review_sync_manager_enhanced import (
    get_enhanced_sync_manager
)

async def main():
    # 创建同步管理器
    sync_manager = get_enhanced_sync_manager(
        max_concurrent=10,
        enable_cache=True,
        cache_ttl=3600,
        cache_max_size=5000,
        batch_size=100
    )
    
    print("✓ 同步管理器初始化成功")
    
    # 查看缓存状态
    cache_stats = sync_manager.cache.get_stats()
    print(f"缓存状态: {cache_stats}")
    
    # 执行同步操作
    # ... 你的同步代码 ...
    
    # 查看性能报告
    sync_manager.print_performance_report()
    
    # 查看缓存命中率
    hit_rate = sync_manager.metrics.get_cache_hit_rate()
    print(f"缓存命中率: {hit_rate:.2f}%")

if __name__ == "__main__":
    asyncio.run(main())
```

## 更多信息

- cachetools 官方文档: https://cachetools.readthedocs.io/
- 项目代码: `api_modules/postgresql_review_sync/review_sync_manager_enhanced.py`

