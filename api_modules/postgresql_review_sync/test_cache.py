"""
测试 Cachetools 缓存功能
"""

import sys
import os
import time
import json

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from api_modules.postgresql_review_sync.review_sync_manager_enhanced import (
    CacheToolsManager,
    get_enhanced_sync_manager
)


def test_cache_basic_operations():
    """测试缓存基本操作"""
    print("\n" + "=" * 60)
    print("测试 1: 缓存基本操作")
    print("=" * 60)
    
    cache = CacheToolsManager(ttl=5, max_size=100, enabled=True)
    
    # 测试 SET 和 GET
    print("\n1. 测试 SET 和 GET:")
    cache.set('test', 'key1', value={'data': 'value1'})
    result = cache.get('test', 'key1')
    print(f"   ✓ SET/GET: {result}")
    assert result == {'data': 'value1'}, "GET 返回值不正确"
    
    # 测试不存在的键
    print("\n2. 测试不存在的键:")
    result = cache.get('test', 'nonexistent')
    print(f"   ✓ 不存在的键返回: {result}")
    assert result is None, "不存在的键应返回 None"
    
    # 测试 DELETE
    print("\n3. 测试 DELETE:")
    cache.delete('test', 'key1')
    result = cache.get('test', 'key1')
    print(f"   ✓ DELETE 后 GET: {result}")
    assert result is None, "删除后应返回 None"
    
    print("\n✅ 基本操作测试通过")


def test_cache_ttl():
    """测试缓存 TTL 过期"""
    print("\n" + "=" * 60)
    print("测试 2: 缓存 TTL 过期")
    print("=" * 60)
    
    cache = CacheToolsManager(ttl=2, max_size=100, enabled=True)
    
    # 设置缓存
    print("\n1. 设置缓存（TTL=2秒）:")
    cache.set('test', 'ttl_key', value={'data': 'will_expire'})
    result = cache.get('test', 'ttl_key')
    print(f"   ✓ 立即获取: {result}")
    assert result is not None, "应该能获取到值"
    
    # 等待过期
    print("\n2. 等待 3 秒后再获取:")
    time.sleep(3)
    result = cache.get('test', 'ttl_key')
    print(f"   ✓ 过期后获取: {result}")
    assert result is None, "过期后应返回 None"
    
    print("\n✅ TTL 过期测试通过")


def test_cache_max_size():
    """测试缓存最大容量"""
    print("\n" + "=" * 60)
    print("测试 3: 缓存最大容量（LRU）")
    print("=" * 60)
    
    cache = CacheToolsManager(ttl=60, max_size=5, enabled=True)
    
    # 填满缓存
    print("\n1. 填充 5 个条目（max_size=5）:")
    for i in range(5):
        cache.set('test', f'key{i}', value=f'value{i}')
    
    stats = cache.get_stats()
    print(f"   ✓ 当前大小: {stats['current_size']}/{stats['max_size']}")
    assert stats['current_size'] == 5, "应该有 5 个条目"
    
    # 添加第 6 个条目，应触发 LRU 淘汰
    print("\n2. 添加第 6 个条目（触发 LRU）:")
    cache.set('test', 'key5', value='value5')
    stats = cache.get_stats()
    print(f"   ✓ 当前大小: {stats['current_size']}/{stats['max_size']}")
    assert stats['current_size'] <= 5, "应该保持在最大容量"
    
    print("\n✅ 最大容量测试通过")


def test_cache_pattern_clear():
    """测试模式匹配清除"""
    print("\n" + "=" * 60)
    print("测试 4: 模式匹配清除")
    print("=" * 60)
    
    cache = CacheToolsManager(ttl=60, max_size=100, enabled=True)
    
    # 设置多个不同前缀的缓存
    print("\n1. 设置多个缓存:")
    cache.set('api', 'endpoint1', value='data1')
    cache.set('api', 'endpoint2', value='data2')
    cache.set('db', 'query1', value='data3')
    cache.set('db', 'query2', value='data4')
    
    stats = cache.get_stats()
    print(f"   ✓ 总共: {stats['current_size']} 个条目")
    
    # 清除 api 前缀的缓存
    print("\n2. 清除 'api:' 前缀的缓存:")
    count = cache.clear_pattern('api:')
    print(f"   ✓ 清除了 {count} 个条目")
    
    # 验证
    assert cache.get('api', 'endpoint1') is None, "api 缓存应被清除"
    assert cache.get('db', 'query1') is not None, "db 缓存应保留"
    
    print("\n✅ 模式匹配清除测试通过")


def test_cache_stats():
    """测试缓存统计"""
    print("\n" + "=" * 60)
    print("测试 5: 缓存统计")
    print("=" * 60)
    
    cache = CacheToolsManager(ttl=60, max_size=100, enabled=True)
    
    # 添加一些缓存
    for i in range(10):
        cache.set('test', f'key{i}', value=f'value{i}')
    
    # 获取统计
    stats = cache.get_stats()
    print(f"\n缓存统计:")
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    assert stats['enabled'] == True, "缓存应该启用"
    assert stats['current_size'] == 10, "应该有 10 个条目"
    assert stats['max_size'] == 100, "最大容量应该是 100"
    assert stats['ttl'] == 60, "TTL 应该是 60"
    assert stats['usage_percent'] == 10.0, "使用率应该是 10%"
    
    print("\n✅ 缓存统计测试通过")


def test_sync_manager_integration():
    """测试与同步管理器的集成"""
    print("\n" + "=" * 60)
    print("测试 6: 与同步管理器集成")
    print("=" * 60)
    
    try:
        # 创建同步管理器
        print("\n1. 创建同步管理器:")
        sync_manager = get_enhanced_sync_manager(
            max_concurrent=10,
            enable_cache=True,
            cache_ttl=3600,
            cache_max_size=5000,
            batch_size=100
        )
        print("   ✓ 同步管理器创建成功")
        
        # 检查缓存状态
        print("\n2. 检查缓存状态:")
        cache_stats = sync_manager.cache.get_stats()
        print(f"   缓存状态: {json.dumps(cache_stats, indent=2, ensure_ascii=False)}")
        assert cache_stats['enabled'] == True, "缓存应该启用"
        
        # 测试缓存操作
        print("\n3. 测试缓存操作:")
        sync_manager.cache.set('test', 'integration', value={'test': 'data'})
        result = sync_manager.cache.get('test', 'integration')
        print(f"   ✓ 缓存读写: {result}")
        assert result == {'test': 'data'}, "缓存读写应该正常"
        
        # 查看性能指标
        print("\n4. 性能指标:")
        metrics = sync_manager.metrics.to_dict()
        print(f"   API 调用: {metrics['api_calls']}")
        print(f"   缓存命中: {metrics['cache_hits']}")
        print(f"   缓存未命中: {metrics['cache_misses']}")
        
        print("\n✅ 集成测试通过")
        
    except Exception as e:
        print(f"\n❌ 集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        raise


def test_cache_disabled():
    """测试禁用缓存"""
    print("\n" + "=" * 60)
    print("测试 7: 禁用缓存")
    print("=" * 60)
    
    cache = CacheToolsManager(ttl=60, max_size=100, enabled=False)
    
    # 尝试操作
    print("\n1. 尝试 SET（缓存已禁用）:")
    result = cache.set('test', 'key', value='value')
    print(f"   ✓ SET 返回: {result}")
    assert result == False, "禁用时 SET 应返回 False"
    
    print("\n2. 尝试 GET（缓存已禁用）:")
    result = cache.get('test', 'key')
    print(f"   ✓ GET 返回: {result}")
    assert result is None, "禁用时 GET 应返回 None"
    
    # 检查统计
    print("\n3. 检查统计:")
    stats = cache.get_stats()
    print(f"   ✓ 统计: {stats}")
    assert stats['enabled'] == False, "统计应显示禁用"
    
    print("\n✅ 禁用缓存测试通过")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("开始测试 Cachetools 缓存功能")
    print("=" * 60)
    
    tests = [
        test_cache_basic_operations,
        test_cache_ttl,
        test_cache_max_size,
        test_cache_pattern_clear,
        test_cache_stats,
        test_cache_disabled,
        test_sync_manager_integration,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"\n❌ 测试失败: {test.__name__}")
            print(f"   错误: {e}")
            import traceback
            traceback.print_exc()
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"✅ 通过: {passed}/{len(tests)}")
    print(f"❌ 失败: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n🎉 所有测试通过！")
    else:
        print(f"\n⚠️ 有 {failed} 个测试失败")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

