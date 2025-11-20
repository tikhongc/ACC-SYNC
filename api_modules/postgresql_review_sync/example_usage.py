#!/usr/bin/env python3
"""
增强版审批同步系统 - 使用示例
演示所有核心功能的使用方法
"""

import sys
import os
import asyncio

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


# ============================================================================
# 示例 1: 基础同步（批量 UPSERT）
# ============================================================================

def example_1_basic_sync():
    """示例 1: 基础同步 - 使用批量 UPSERT"""
    
    print("\n" + "="*80)
    print("示例 1: 基础同步 - 批量 UPSERT")
    print("="*80)
    
    from review_sync_manager_enhanced import EnhancedReviewSyncManager
    from database_sql.review_data_access_enhanced import EnhancedReviewDataAccess
    
    # 初始化
    da = EnhancedReviewDataAccess()
    sync_manager = EnhancedReviewSyncManager(
        data_access=da,
        max_concurrent=10,
        enable_cache=False  # 暂不启用缓存
    )
    
    # 模拟工作流数据
    workflows = [
        {
            'id': 'workflow-1',
            'projectId': 'project-123',
            'name': 'Design Review',
            'status': 'ACTIVE',
            'steps': []
        },
        {
            'id': 'workflow-2',
            'projectId': 'project-123',
            'name': 'Final Approval',
            'status': 'ACTIVE',
            'steps': []
        }
    ]
    
    # 批量 UPSERT
    inserted, updated = sync_manager.batch_upsert_workflows(workflows)
    
    print(f"\n✓ 工作流同步完成:")
    print(f"  - 新建: {inserted} 个")
    print(f"  - 更新: {updated} 个")
    
    # 再次运行（应该全部更新）
    inserted, updated = sync_manager.batch_upsert_workflows(workflows)
    
    print(f"\n✓ 再次同步:")
    print(f"  - 新建: {inserted} 个")
    print(f"  - 更新: {updated} 个")


# ============================================================================
# 示例 2: 异步并行同步
# ============================================================================

async def example_2_async_sync():
    """示例 2: 异步并行同步"""
    
    print("\n" + "="*80)
    print("示例 2: 异步并行同步")
    print("="*80)
    
    from review_sync_manager_enhanced import EnhancedReviewSyncManager
    from database_sql.review_data_access_enhanced import EnhancedReviewDataAccess
    import utils
    
    # 初始化
    da = EnhancedReviewDataAccess()
    sync_manager = EnhancedReviewSyncManager(
        data_access=da,
        max_concurrent=15,
        enable_cache=True
    )
    
    # 获取 API 客户端
    api_client = utils.ReviewsAPIClient()
    project_id = "b.1eea4119-3553-4167-b93d-3a3d5d07d33d"
    
    # 获取评审列表
    print("\n📥 获取评审列表...")
    reviews_result = api_client.get_reviews(project_id, limit=10)
    reviews = reviews_result.get('results', [])
    
    print(f"✓ 找到 {len(reviews)} 个评审")
    
    # 异步并行同步
    print("\n🚀 开始异步并行同步...")
    stats = await sync_manager.async_sync_reviews_parallel(
        api_client,
        project_id,
        reviews,
        show_progress=True
    )
    
    print(f"\n✓ 同步完成:")
    print(f"  - 新建: {stats.get('reviews_synced', 0)} 个")
    print(f"  - 更新: {stats.get('reviews_updated', 0)} 个")


# ============================================================================
# 示例 3: Redis 缓存
# ============================================================================

def example_3_redis_cache():
    """示例 3: Redis 缓存使用"""
    
    print("\n" + "="*80)
    print("示例 3: Redis 缓存")
    print("="*80)
    
    from review_sync_manager_enhanced import EnhancedReviewSyncManager
    from database_sql.review_data_access_enhanced import EnhancedReviewDataAccess
    
    # 初始化（启用缓存）
    da = EnhancedReviewDataAccess()
    sync_manager = EnhancedReviewSyncManager(
        data_access=da,
        enable_cache=True,
        cache_ttl=300,  # 5 分钟
        redis_host='localhost',
        redis_port=6379
    )
    
    if not sync_manager.cache.enabled:
        print("\n⚠ Redis 未启用，跳过缓存示例")
        return
    
    # 设置缓存
    print("\n📝 设置缓存...")
    test_data = {'name': 'Test Review', 'status': 'OPEN'}
    sync_manager.cache.set('test', 'review-1', value=test_data)
    print("✓ 缓存已设置")
    
    # 获取缓存
    print("\n📖 读取缓存...")
    cached_data = sync_manager.cache.get('test', 'review-1')
    print(f"✓ 缓存数据: {cached_data}")
    
    # 删除缓存
    print("\n🗑️  删除缓存...")
    sync_manager.cache.delete('test', 'review-1')
    print("✓ 缓存已删除")
    
    # 验证删除
    cached_data = sync_manager.cache.get('test', 'review-1')
    print(f"✓ 验证: {cached_data} (应为 None)")


# ============================================================================
# 示例 4: 性能监控
# ============================================================================

def example_4_performance_monitoring():
    """示例 4: 性能监控"""
    
    print("\n" + "="*80)
    print("示例 4: 性能监控")
    print("="*80)
    
    from review_sync_manager_enhanced import EnhancedReviewSyncManager
    from database_sql.review_data_access_enhanced import EnhancedReviewDataAccess
    import time
    
    # 初始化
    da = EnhancedReviewDataAccess()
    sync_manager = EnhancedReviewSyncManager(
        data_access=da,
        max_concurrent=10
    )
    
    # 模拟一些操作
    print("\n⏱️  执行一些操作...")
    
    # 模拟 API 调用
    sync_manager.metrics.api_calls += 10
    sync_manager.metrics.api_time += 2.5
    sync_manager.metrics.cache_hits += 7
    sync_manager.metrics.cache_misses += 3
    
    # 模拟数据库操作
    sync_manager.metrics.db_queries += 5
    sync_manager.metrics.db_time += 0.8
    
    sync_manager.metrics.total_time = 3.5
    
    # 获取性能报告
    print("\n📊 生成性能报告...")
    report = sync_manager.get_performance_report()
    
    # 显示关键指标
    summary = report['summary']
    print(f"\n✓ 性能指标:")
    print(f"  - 总耗时: {summary['total_time']:.2f}秒")
    print(f"  - API 调用: {summary['api_calls']} 次")
    print(f"  - 缓存命中率: {summary['cache_hit_rate']:.1f}%")
    print(f"  - 数据库查询: {summary['db_queries']} 次")
    
    # 打印完整报告
    print("\n" + "-"*80)
    sync_manager.print_performance_report()


# ============================================================================
# 示例 5: 断路器模式
# ============================================================================

def example_5_circuit_breaker():
    """示例 5: 断路器模式"""
    
    print("\n" + "="*80)
    print("示例 5: 断路器模式")
    print("="*80)
    
    from review_sync_manager_enhanced import EnhancedReviewSyncManager
    from database_sql.review_data_access_enhanced import EnhancedReviewDataAccess
    
    # 初始化
    da = EnhancedReviewDataAccess()
    sync_manager = EnhancedReviewSyncManager(data_access=da)
    
    # 查看初始状态
    print(f"\n🔵 初始状态: {sync_manager.circuit_breaker['state']}")
    print(f"   失败次数: {sync_manager.circuit_breaker['failures']}")
    
    # 模拟失败
    print("\n⚠️  模拟 API 失败...")
    for i in range(5):
        sync_manager.record_failure()
        print(f"   失败 {i+1}/5 - 状态: {sync_manager.circuit_breaker['state']}")
    
    # 检查断路器
    print(f"\n🔴 断路器状态: {sync_manager.circuit_breaker['state']}")
    
    if sync_manager.check_circuit_breaker():
        print("✓ 可以执行 API 调用")
    else:
        print("✗ 断路器已打开，暂停 API 调用")
    
    # 模拟恢复
    print("\n🔄 等待超时后尝试恢复...")
    import time
    sync_manager.circuit_breaker['last_failure_time'] = time.time() - 61  # 超过 60 秒
    
    if sync_manager.check_circuit_breaker():
        print("🟡 断路器进入半开状态")
        
        # 模拟成功
        sync_manager.record_success()
        print(f"🟢 断路器状态: {sync_manager.circuit_breaker['state']}")


# ============================================================================
# 示例 6: 配置管理
# ============================================================================

def example_6_configuration():
    """示例 6: 配置管理"""
    
    print("\n" + "="*80)
    print("示例 6: 配置管理")
    print("="*80)
    
    from sync_config import DEV_CONFIG, PROD_CONFIG, TEST_CONFIG
    from review_sync_manager_enhanced import EnhancedReviewSyncManager
    from database_sql.review_data_access_enhanced import EnhancedReviewDataAccess
    
    # 开发环境配置
    print("\n🔧 开发环境配置:")
    print(f"  - max_concurrent: {DEV_CONFIG.max_concurrent}")
    print(f"  - batch_size: {DEV_CONFIG.batch_size}")
    print(f"  - enable_cache: {DEV_CONFIG.enable_cache}")
    print(f"  - log_level: {DEV_CONFIG.log_level}")
    
    # 生产环境配置
    print("\n🚀 生产环境配置:")
    print(f"  - max_concurrent: {PROD_CONFIG.max_concurrent}")
    print(f"  - batch_size: {PROD_CONFIG.batch_size}")
    print(f"  - enable_cache: {PROD_CONFIG.enable_cache}")
    print(f"  - cache_ttl: {PROD_CONFIG.cache_ttl}")
    
    # 使用配置初始化
    print("\n✓ 使用生产配置初始化...")
    da = EnhancedReviewDataAccess()
    sync_manager = EnhancedReviewSyncManager(
        data_access=da,
        max_concurrent=PROD_CONFIG.max_concurrent,
        enable_cache=PROD_CONFIG.enable_cache,
        cache_ttl=PROD_CONFIG.cache_ttl,
        batch_size=PROD_CONFIG.batch_size
    )
    print("✓ 初始化完成")


# ============================================================================
# 主函数
# ============================================================================

def main():
    """运行所有示例"""
    
    print("\n" + "="*80)
    print("增强版审批同步系统 - 使用示例")
    print("="*80)
    
    import argparse
    
    parser = argparse.ArgumentParser(description='增强版审批同步系统使用示例')
    parser.add_argument('--example', type=int, choices=range(1, 7),
                       help='运行指定示例 (1-6)')
    parser.add_argument('--all', action='store_true',
                       help='运行所有示例')
    
    args = parser.parse_args()
    
    examples = {
        1: ('基础同步 - 批量 UPSERT', example_1_basic_sync),
        2: ('异步并行同步', lambda: asyncio.run(example_2_async_sync())),
        3: ('Redis 缓存', example_3_redis_cache),
        4: ('性能监控', example_4_performance_monitoring),
        5: ('断路器模式', example_5_circuit_breaker),
        6: ('配置管理', example_6_configuration)
    }
    
    try:
        if args.example:
            # 运行指定示例
            name, func = examples[args.example]
            print(f"\n运行示例 {args.example}: {name}")
            func()
        elif args.all:
            # 运行所有示例
            for num, (name, func) in examples.items():
                print(f"\n运行示例 {num}: {name}")
                try:
                    func()
                except Exception as e:
                    print(f"⚠ 示例 {num} 失败: {e}")
        else:
            # 显示菜单
            print("\n可用示例:")
            for num, (name, _) in examples.items():
                print(f"  {num}. {name}")
            print("\n使用方法:")
            print("  python example_usage.py --example 1    # 运行示例 1")
            print("  python example_usage.py --all          # 运行所有示例")
        
        print("\n" + "="*80)
        print("✓ 示例运行完成")
        print("="*80)
        
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

