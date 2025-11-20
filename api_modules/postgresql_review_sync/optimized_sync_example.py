"""
优化版同步管理器使用示例
展示如何使用并行API调用、批量数据库插入等优化功能
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from api_modules.postgresql_review_sync.review_sync_manager import ReviewSyncManager
from database_sql.review_data_access import ReviewDataAccess


def example_1_parallel_sync():
    """
    示例1: 使用并行同步评审
    
    这是最推荐的方式，可以大幅提升同步速度
    """
    print("=" * 80)
    print("示例1: 并行批量同步评审")
    print("=" * 80)
    
    # 初始化同步管理器（设置并发线程数）
    sync_manager = ReviewSyncManager(max_workers=10)
    
    # 模拟API客户端（实际使用时替换为真实的API客户端）
    class MockAPIClient:
        def get(self, url, params=None):
            # 这里应该是真实的API调用
            # 例如: requests.get(base_url + url, params=params, headers=headers)
            return {'results': [], 'pagination': {'totalResults': 0}}
    
    api_client = MockAPIClient()
    project_id = "your-project-id"
    
    # 步骤1: 使用智能分页获取所有评审列表
    print("\n步骤1: 获取评审列表...")
    reviews = sync_manager.fetch_all_reviews_with_pagination(
        api_client=api_client,
        project_id=project_id,
        limit_per_page=50,
        show_progress=True
    )
    
    # 步骤2: 并行同步评审详细数据
    print("\n步骤2: 并行同步评审...")
    if reviews:
        stats = sync_manager.sync_reviews_batch_parallel(
            acc_reviews=reviews,
            api_client=api_client,
            project_id=project_id,
            show_progress=True
        )
        
        print("\n最终统计:")
        print(f"  成功同步: {stats['reviews_synced']} 个")
        print(f"  更新: {stats['reviews_updated']} 个")
        print(f"  总耗时: {stats['performance']['total_time']:.2f}秒")
    else:
        print("没有找到评审")


def example_2_traditional_sync():
    """
    示例2: 传统串行同步（用于对比）
    
    保持向后兼容，但速度较慢
    """
    print("\n" + "=" * 80)
    print("示例2: 传统串行同步（对比）")
    print("=" * 80)
    
    sync_manager = ReviewSyncManager()
    
    # 假设已经有评审数据
    reviews = []  # 从API获取的评审列表
    
    # 使用传统方法同步
    stats = sync_manager.sync_reviews_batch(
        acc_reviews=reviews,
        show_progress=True
    )
    
    print(f"\n串行同步完成，耗时: {stats['performance']['total_time']:.2f}秒")


def example_3_batch_operations():
    """
    示例3: 批量数据库操作
    
    展示如何使用批量插入功能
    """
    print("\n" + "=" * 80)
    print("示例3: 批量数据库操作")
    print("=" * 80)
    
    da = ReviewDataAccess()
    
    # 批量插入文件版本
    files_data = [
        {
            'review_id': 1,
            'file_urn': 'urn:adsk:file:1',
            'file_name': 'file1.pdf',
            'approval_status': 'PENDING'
        },
        {
            'review_id': 1,
            'file_urn': 'urn:adsk:file:2',
            'file_name': 'file2.pdf',
            'approval_status': 'PENDING'
        }
    ]
    
    print("\n批量插入文件版本...")
    try:
        count = da.batch_insert_review_files(files_data)
        print(f"✓ 成功插入 {count} 个文件版本")
    except Exception as e:
        print(f"✗ 批量插入失败: {e}")
    
    # 批量插入进度步骤
    steps_data = [
        {
            'review_id': 1,
            'step_id': 'step1',
            'step_name': 'Review',
            'step_type': 'REVIEWER',
            'step_order': 1,
            'status': 'PENDING'
        },
        {
            'review_id': 1,
            'step_id': 'step2',
            'step_name': 'Approve',
            'step_type': 'APPROVER',
            'step_order': 2,
            'status': 'PENDING'
        }
    ]
    
    print("\n批量插入进度步骤...")
    try:
        count = da.batch_insert_review_steps(steps_data)
        print(f"✓ 成功插入 {count} 个进度步骤")
    except Exception as e:
        print(f"✗ 批量插入失败: {e}")


def example_4_performance_comparison():
    """
    示例4: 性能对比
    
    对比串行和并行的性能差异
    """
    print("\n" + "=" * 80)
    print("示例4: 性能对比分析")
    print("=" * 80)
    
    # 假设参数
    num_reviews = 8
    api_calls_per_review = 3  # versions, progress, workflow
    avg_api_time = 6  # 秒
    
    # 串行计算
    serial_time = num_reviews * api_calls_per_review * avg_api_time
    
    # 并行计算（10个并发线程）
    max_workers = 10
    total_api_calls = num_reviews * api_calls_per_review
    parallel_time = (total_api_calls / max_workers) * avg_api_time
    
    # 输出对比
    print(f"\n假设条件:")
    print(f"  评审数量: {num_reviews}")
    print(f"  每个评审API调用: {api_calls_per_review}")
    print(f"  平均API响应时间: {avg_api_time}秒")
    print(f"  并发线程数: {max_workers}")
    
    print(f"\n性能对比:")
    print(f"  串行同步耗时: {serial_time:.0f}秒 ({serial_time/60:.1f}分钟)")
    print(f"  并行同步耗时: {parallel_time:.0f}秒 ({parallel_time/60:.1f}分钟)")
    print(f"  节省时间: {serial_time - parallel_time:.0f}秒")
    print(f"  提速比: {serial_time / parallel_time:.1f}x")
    print(f"  效率提升: {(serial_time - parallel_time) / serial_time * 100:.1f}%")
    
    print(f"\n实际效果:")
    print(f"  ✓ 从 {serial_time/60:.1f}分钟 降至 {parallel_time/60:.1f}分钟")
    print(f"  ✓ 节省 {(serial_time - parallel_time)/60:.1f}分钟")
    print(f"  ✓ 提升 {(serial_time - parallel_time) / serial_time * 100:.0f}%")


def example_5_api_rate_limiting():
    """
    示例5: API限流处理
    
    展示如何处理API限流
    """
    print("\n" + "=" * 80)
    print("示例5: API限流处理")
    print("=" * 80)
    
    print("\n自动限流重试功能:")
    print("  ✓ 检测429错误（Too Many Requests）")
    print("  ✓ 指数退避重试（1秒 -> 2秒 -> 4秒）")
    print("  ✓ 最多重试3次")
    print("  ✓ 自动降低并发数")
    
    print("\n建议配置:")
    print("  - 小项目（<50评审）: max_workers=5")
    print("  - 中项目（50-200评审）: max_workers=10")
    print("  - 大项目（>200评审）: max_workers=15")
    
    print("\nAPI限流阈值参考:")
    print("  - ACC API通常限制: 100-300 请求/分钟")
    print("  - 建议并发: 5-15 线程")
    print("  - 每秒请求数: 避免超过 5 req/s")


def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("🚀 优化版审批系统同步管理器 - 使用示例")
    print("=" * 80)
    
    # 运行示例
    try:
        # example_1_parallel_sync()  # 需要真实API客户端
        # example_2_traditional_sync()
        # example_3_batch_operations()  # 需要数据库连接
        example_4_performance_comparison()
        example_5_api_rate_limiting()
        
        print("\n" + "=" * 80)
        print("✓ 示例运行完成")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

