#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理 Review 表以解决外键约束问题

在进行文件同步之前，需要先清理 review 相关的表，
因为 review_file_versions 表对 file_versions 表有外键约束。

用法：
    python database_sql/clean_review_tables_before_file_sync.py

执行顺序：
    1. 运行此脚本清理 review 表
    2. 运行文件同步: python api_modules/postgresql_sync_file/production_acc_sync_test.py
    3. （可选）运行 review 同步: python database_sql/test_enhanced_review_sync.py
"""

import sys
import os

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import psycopg2
from database_sql.neon_config import NeonConfig


def clean_review_tables():
    """
    清理所有 review 相关的表、视图和类型
    这将解除对 file_versions 表的外键约束
    """
    print("=" * 80)
    print("清理 Review 表以解除外键约束")
    print("=" * 80)
    print()
    print("说明：此操作将删除所有 review 相关的数据")
    print("包括：reviews, workflows, file_approval_history 等")
    print()

    # 获取用户确认
    confirm = input("是否继续？(yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("操作已取消")
        return False

    print("\n正在连接数据库...")

    conn = None
    cursor = None

    try:
        # 获取数据库配置
        neon_config = NeonConfig()
        db_params = neon_config.get_db_params()

        # 连接数据库
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        print("✓ 数据库连接成功")
        print("\n正在删除 review 相关对象...")

        # 删除所有 review 相关的表、视图和类型
        drop_sql = """
        -- Drop views
        DROP VIEW IF EXISTS reviews_overview CASCADE;
        DROP VIEW IF EXISTS pending_tasks_view CASCADE;

        -- Drop materialized views
        DROP MATERIALIZED VIEW IF EXISTS mv_file_approval_summary CASCADE;

        -- Drop tables (CASCADE will handle dependencies)
        DROP TABLE IF EXISTS file_approval_history CASCADE;
        DROP TABLE IF EXISTS review_notifications CASCADE;
        DROP TABLE IF EXISTS approval_decisions CASCADE;
        DROP TABLE IF EXISTS review_comments CASCADE;
        DROP TABLE IF EXISTS review_progress CASCADE;
        DROP TABLE IF EXISTS review_file_versions CASCADE;
        DROP TABLE IF EXISTS review_candidates CASCADE;
        DROP TABLE IF EXISTS review_step_candidates CASCADE;
        DROP TABLE IF EXISTS workflow_notes CASCADE;
        DROP TABLE IF EXISTS reviews CASCADE;
        DROP TABLE IF EXISTS workflow_templates CASCADE;
        DROP TABLE IF EXISTS workflows CASCADE;

        -- Drop enum types
        DROP TYPE IF EXISTS data_source_type CASCADE;
        DROP TYPE IF EXISTS workflow_status_type CASCADE;
        DROP TYPE IF EXISTS review_status_type CASCADE;
        DROP TYPE IF EXISTS approval_status_type CASCADE;
        DROP TYPE IF EXISTS step_type CASCADE;
        DROP TYPE IF EXISTS candidate_type CASCADE;
        DROP TYPE IF EXISTS reviewer_type CASCADE;
        DROP TYPE IF EXISTS time_unit_type CASCADE;
        """

        cursor.execute(drop_sql)
        conn.commit()

        print("✓ 所有 review 表、视图和类型已成功删除")
        print()
        print("=" * 80)
        print("清理完成！")
        print("=" * 80)
        print()
        print("后续步骤：")
        print("  1. 运行文件同步：")
        print("     python api_modules/postgresql_sync_file/production_acc_sync_test.py")
        print()
        print("  2. （可选）重新同步 review 数据：")
        print("     python database_sql/test_enhanced_review_sync.py")
        print()

        return True

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"\n❌ 错误：{str(e)}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def verify_cleanup():
    """验证清理结果"""
    print("\n正在验证清理结果...")

    conn = None
    cursor = None

    try:
        neon_config = NeonConfig()
        db_params = neon_config.get_db_params()
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # 检查 review 相关表是否还存在
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_name IN (
                'reviews', 'workflows', 'review_file_versions',
                'review_progress', 'file_approval_history',
                'review_step_candidates', 'workflow_notes'
            )
            AND table_schema = 'public'
        """)

        remaining_tables = cursor.fetchall()

        if remaining_tables:
            print(f"⚠️  警告：仍有 {len(remaining_tables)} 个表存在：")
            for table in remaining_tables:
                print(f"   - {table[0]}")
            return False
        else:
            print("✓ 验证通过：所有 review 表已清理")
            return True

    except Exception as e:
        print(f"验证失败：{str(e)}")
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    print()
    print("清理 Review 表工具")
    print("解决文件同步时的外键约束冲突")
    print()

    # 执行清理
    success = clean_review_tables()

    if success:
        # 验证清理结果
        verify_cleanup()
        print("\n✅ 现在可以安全地运行文件同步了！")
        sys.exit(0)
    else:
        print("\n❌ 清理失败，请检查错误信息")
        sys.exit(1)
