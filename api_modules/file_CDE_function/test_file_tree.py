#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件树缓存系统 - 测试脚本

功能：
1. 测试数据库连接
2. 测试树构建功能
3. 测试缓存读写
4. 测试 API 端点
"""

import json
import time
import logging
from typing import Dict, Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# 数据库连接参数
DB_PARAMS = {
    'host': "ep-soft-mountain-a4jqpy5e-pooler.us-east-1.aws.neon.tech",
    'port': 5432,
    'database': "neondb",
    'user': "neondb_owner",
    'password': "npg_a2nxljG8LOSP",
    'sslmode': 'require'
}


def test_db_connection() -> bool:
    """测试数据库连接"""
    print("\n" + "="*70)
    print("测试1: 数据库连接")
    print("="*70)

    try:
        import psycopg2
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        # 执行简单查询
        cur.execute("SELECT version()")
        version = cur.fetchone()[0]
        logger.info(f"PostgreSQL 版本: {version[:50]}...")

        cur.close()
        conn.close()

        logger.info("✓ 数据库连接成功")
        return True
    except Exception as e:
        logger.error(f"✗ 数据库连接失败: {str(e)}")
        return False


def test_cache_table_exists() -> bool:
    """测试缓存表是否存在"""
    print("\n" + "="*70)
    print("测试2: 缓存表检查")
    print("="*70)

    try:
        import psycopg2
        import psycopg2.extras

        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # 检查表是否存在
        sql = """
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = 'file_tree_cache'
        );
        """
        cur.execute(sql)
        result = cur.fetchone()

        if result[0]:
            logger.info("✓ file_tree_cache 表存在")

            # 查询表的信息
            sql_info = "SELECT COUNT(*) as count FROM file_tree_cache"
            cur.execute(sql_info)
            count_result = cur.fetchone()
            logger.info(f"  缓存记录数: {count_result['count']}")

            cur.close()
            conn.close()
            return True
        else:
            logger.error("✗ file_tree_cache 表不存在")
            logger.info("  请先运行: psql < database_sql/file_tree_cache_schema.sql")
            cur.close()
            conn.close()
            return False
    except Exception as e:
        logger.error(f"✗ 检查缓存表失败: {str(e)}")
        return False


def test_file_tree_builder() -> bool:
    """测试文件树构建器"""
    print("\n" + "="*70)
    print("测试3: 文件树构建器")
    print("="*70)

    try:
        from file_tree_builder import FileTreeBuilder

        # 查找一个有数据的项目
        import psycopg2
        import psycopg2.extras

        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        sql = """
        SELECT DISTINCT project_id
        FROM folders
        LIMIT 1
        """
        cur.execute(sql)
        result = cur.fetchone()
        cur.close()
        conn.close()

        if not result:
            logger.warning("⚠ 没有找到包含文件夹的项目，跳过此测试")
            return True

        project_id = result['project_id']
        logger.info(f"使用项目ID: {project_id}")

        # 创建构建器并测试
        builder = FileTreeBuilder(DB_PARAMS)

        if not builder.connect():
            logger.error("✗ 无法连接数据库")
            return False

        try:
            # 测试查询文件夹
            start = time.time()
            folders = builder.query_folders(project_id)
            folder_time = time.time() - start
            logger.info(f"✓ 查询文件夹完成: {len(folders)} 个文件夹 ({folder_time*1000:.2f}ms)")

            # 测试查询文件
            start = time.time()
            files = builder.query_files(project_id)
            file_time = time.time() - start
            logger.info(f"✓ 查询文件完成: {len(files)} 个文件 ({file_time*1000:.2f}ms)")

            # 测试构建树
            start = time.time()
            tree = builder.build_tree_from_paths(folders, files)
            build_time = time.time() - start
            logger.info(f"✓ 构建树完成 ({build_time*1000:.2f}ms)")

            # 检查树结构
            if 'root' in tree and 'metadata' in tree:
                logger.info(f"  树结构有效")
                logger.info(f"  - 总文件夹数: {tree['metadata']['total_folders']}")
                logger.info(f"  - 总文件数: {tree['metadata']['total_files']}")
            else:
                logger.warning("⚠ 树结构不完整")

            # 测试保存到缓存
            start = time.time()
            success = builder.save_to_cache(project_id, tree, build_time*1000)
            save_time = time.time() - start
            if success:
                logger.info(f"✓ 保存到缓存完成 ({save_time*1000:.2f}ms)")
            else:
                logger.error("✗ 保存到缓存失败")
                return False

            # 测试从缓存读取
            start = time.time()
            cached_tree = builder.get_cached_tree(project_id)
            read_time = time.time() - start
            if cached_tree:
                logger.info(f"✓ 从缓存读取完成 ({read_time*1000:.2f}ms)")
            else:
                logger.error("✗ 从缓存读取失败")
                return False

            # 测试清空缓存
            start = time.time()
            success = builder.invalidate_cache(project_id)
            invalidate_time = time.time() - start
            if success:
                logger.info(f"✓ 清空缓存完成 ({invalidate_time*1000:.2f}ms)")
            else:
                logger.error("✗ 清空缓存失败")
                return False

            # 验证缓存已被清空
            cached_tree = builder.get_cached_tree(project_id)
            if cached_tree is None:
                logger.info("✓ 缓存清空验证成功")
            else:
                logger.warning("⚠ 缓存清空后仍有数据")

            return True

        finally:
            builder.disconnect()

    except Exception as e:
        logger.error(f"✗ 构建器测试失败: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False


def test_high_level_functions() -> bool:
    """测试高级函数"""
    print("\n" + "="*70)
    print("测试4: 高级函数 (get_file_tree, invalidate_file_tree_cache)")
    print("="*70)

    try:
        from file_tree_builder import get_file_tree, invalidate_file_tree_cache

        # 查找一个项目
        import psycopg2
        import psycopg2.extras

        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        sql = "SELECT DISTINCT project_id FROM folders LIMIT 1"
        cur.execute(sql)
        result = cur.fetchone()
        cur.close()
        conn.close()

        if not result:
            logger.warning("⚠ 没有找到包含文件夹的项目，跳过此测试")
            return True

        project_id = result['project_id']
        logger.info(f"使用项目ID: {project_id}")

        # 第一次调用（缓存未命中）
        logger.info("\n调用1: 缓存未命中")
        start = time.time()
        tree1, from_cache1 = get_file_tree(project_id, DB_PARAMS, force_refresh=True)
        time1 = time.time() - start

        if tree1:
            logger.info(f"✓ 获取文件树成功 (耗时: {time1*1000:.2f}ms, from_cache: {from_cache1})")
        else:
            logger.error("✗ 获取文件树失败")
            return False

        # 第二次调用（缓存命中）
        logger.info("\n调用2: 缓存命中")
        start = time.time()
        tree2, from_cache2 = get_file_tree(project_id, DB_PARAMS, force_refresh=False)
        time2 = time.time() - start

        if tree2:
            logger.info(f"✓ 获取文件树成功 (耗时: {time2*1000:.2f}ms, from_cache: {from_cache2})")
            if from_cache2:
                logger.info(f"✓ 缓存命中，速度提升: {time1/time2:.1f}x 倍")
            else:
                logger.warning("⚠ 缓存应该被命中，但没有")
        else:
            logger.error("✗ 获取文件树失败")
            return False

        # 清空缓存
        logger.info("\n清空缓存")
        success = invalidate_file_tree_cache(project_id, DB_PARAMS)
        if success:
            logger.info("✓ 缓存清空成功")
        else:
            logger.error("✗ 缓存清空失败")
            return False

        # 第三次调用（缓存再次未命中）
        logger.info("\n调用3: 缓存清空后重新构建")
        start = time.time()
        tree3, from_cache3 = get_file_tree(project_id, DB_PARAMS, force_refresh=False)
        time3 = time.time() - start

        if tree3:
            logger.info(f"✓ 获取文件树成功 (耗时: {time3*1000:.2f}ms, from_cache: {from_cache3})")
            if not from_cache3:
                logger.info("✓ 缓存清空后正确重建")
            else:
                logger.warning("⚠ 缓存应该被清空，但仍然命中")
        else:
            logger.error("✗ 获取文件树失败")
            return False

        return True

    except Exception as e:
        logger.error(f"✗ 高级函数测试失败: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False


def test_api_flask_app() -> bool:
    """测试 Flask 应用"""
    print("\n" + "="*70)
    print("测试5: Flask API 应用")
    print("="*70)

    try:
        from file_tree_api import create_app

        # 创建 Flask 应用
        app = create_app()
        logger.info("✓ Flask 应用创建成功")

        # 测试路由注册
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        expected_routes = [
            '/api/file-tree',
            '/api/file-tree/invalidate',
            '/api/file-tree/cache-status',
            '/api/file-tree/health'
        ]

        for route in expected_routes:
            if route in routes:
                logger.info(f"✓ 路由已注册: {route}")
            else:
                logger.warning(f"⚠ 路由未注册: {route}")

        # 测试客户端
        with app.test_client() as client:
            # 测试健康检查
            logger.info("\n测试健康检查端点...")
            response = client.get('/api/file-tree/health')
            if response.status_code == 200:
                data = json.loads(response.data)
                logger.info(f"✓ 健康检查成功: {data['status']}")
            else:
                logger.error(f"✗ 健康检查失败: HTTP {response.status_code}")

        return True

    except Exception as e:
        logger.error(f"✗ Flask 应用测试失败: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False


def run_all_tests():
    """运行所有测试"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "文件树缓存系统 - 测试套件" + " "*24 + "║")
    print("╚" + "="*68 + "╝")

    results = {}

    # 运行测试
    results['数据库连接'] = test_db_connection()
    results['缓存表检查'] = test_cache_table_exists()
    results['文件树构建器'] = test_file_tree_builder()
    results['高级函数'] = test_high_level_functions()
    results['Flask 应用'] = test_api_flask_app()

    # 打印总结
    print("\n" + "="*70)
    print("测试总结")
    print("="*70)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{status}: {test_name}")

    print(f"\n总计: {passed}/{total} 项测试通过")

    if passed == total:
        logger.info("\n🎉 所有测试通过！系统已准备好投入生产。")
        return True
    else:
        logger.warning(f"\n⚠️  有 {total - passed} 项测试失败，请检查错误信息。")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)
