#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实现reviewState属性到file_versions表

功能：
1. 添加review_state列到file_versions表
2. 创建compute_file_version_review_state函数
3. 创建update_file_version_review_state触发器
4. 创建idx_file_versions_review_state索引
5. 回填所有现有数据的reviewState值
"""

import psycopg2
import psycopg2.extras
from typing import Dict, Tuple
import sys
import io
from datetime import datetime

# 设置标准输出编码为UTF-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 数据库连接配置
DB_CONFIG = {
    'host': "ep-soft-mountain-a4jqpy5e-pooler.us-east-1.aws.neon.tech",
    'port': 5432,
    'database': "neondb",
    'user': "neondb_owner",
    'password': "npg_a2nxljG8LOSP",
    'sslmode': 'require'
}


class ReviewStateImplementor:
    """实现reviewState功能"""

    def __init__(self):
        self.conn = None
        self.cur = None
        self.errors = []
        self.logs = []

    def log(self, message: str, level: str = "INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] [{level}] {message}"
        self.logs.append(log_msg)
        print(log_msg)

    def connect(self):
        """连接数据库"""
        try:
            self.log("正在连接到数据库...")
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            self.log("数据库连接成功！", "SUCCESS")
            return True
        except Exception as e:
            self.log(f"数据库连接失败: {str(e)}", "ERROR")
            self.errors.append(f"Connection error: {str(e)}")
            return False

    def disconnect(self):
        """断开数据库连接"""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        self.log("数据库连接已关闭")

    def execute_sql(self, sql: str, params=None, description: str = "") -> bool:
        """执行SQL语句"""
        try:
            if description:
                self.log(f"执行: {description}...")

            if params:
                self.cur.execute(sql, params)
            else:
                self.cur.execute(sql)

            self.conn.commit()

            if self.cur.rowcount > 0:
                self.log(f"✓ {description} 成功 (影响行数: {self.cur.rowcount})", "SUCCESS")
            else:
                self.log(f"✓ {description} 成功", "SUCCESS")

            return True
        except Exception as e:
            self.conn.rollback()
            error_msg = f"{description} 失败: {str(e)}"
            self.log(error_msg, "ERROR")
            self.errors.append(error_msg)
            return False

    def check_column_exists(self, table: str, column: str) -> bool:
        """检查列是否存在"""
        try:
            sql = """
            SELECT EXISTS (
                SELECT FROM information_schema.columns
                WHERE table_name = %s AND column_name = %s
            );
            """
            self.cur.execute(sql, (table, column))
            result = self.cur.fetchone()
            return result[0] if result else False
        except Exception as e:
            self.log(f"检查列是否存在失败: {str(e)}", "ERROR")
            return False

    def check_function_exists(self, function_name: str) -> bool:
        """检查函数是否存在"""
        try:
            sql = """
            SELECT EXISTS (
                SELECT FROM information_schema.routines
                WHERE routine_name = %s
            );
            """
            self.cur.execute(sql, (function_name,))
            result = self.cur.fetchone()
            return result[0] if result else False
        except Exception as e:
            self.log(f"检查函数是否存在失败: {str(e)}", "ERROR")
            return False

    def step1_add_review_state_column(self) -> bool:
        """步骤1: 添加review_state列"""
        self.log("\n" + "="*70)
        self.log("步骤1: 添加review_state列到file_versions表", "INFO")
        self.log("="*70)

        # 检查列是否已存在
        if self.check_column_exists('file_versions', 'review_state'):
            self.log("review_state列已存在，跳过此步骤", "WARN")
            return True

        sql = """
        ALTER TABLE file_versions
        ADD COLUMN review_state VARCHAR(20) DEFAULT 'NotInReview'
            CHECK (review_state IN ('InReview', 'NotInReview'));
        """

        return self.execute_sql(sql, description="添加review_state列")

    def step2_create_compute_function(self) -> bool:
        """步骤2: 创建compute_file_version_review_state函数"""
        self.log("\n" + "="*70)
        self.log("步骤2: 创建compute_file_version_review_state函数", "INFO")
        self.log("="*70)

        sql = """
        CREATE OR REPLACE FUNCTION compute_file_version_review_state(p_file_version_urn VARCHAR(500))
        RETURNS VARCHAR(20) AS $$
        DECLARE
            pending_count INTEGER;
        BEGIN
            -- 检查是否存在任何pending状态的review_file_versions
            SELECT COUNT(*) INTO pending_count
            FROM review_file_versions
            WHERE file_version_urn = p_file_version_urn
            AND approval_status = 'PENDING';

            -- 如果存在pending的review，返回InReview，否则返回NotInReview
            IF pending_count > 0 THEN
                RETURN 'InReview';
            ELSE
                RETURN 'NotInReview';
            END IF;
        END;
        $$ LANGUAGE plpgsql;
        """

        return self.execute_sql(sql, description="创建compute_file_version_review_state函数")

    def step3_create_trigger_function(self) -> bool:
        """步骤3: 创建update_file_version_review_state触发器函数"""
        self.log("\n" + "="*70)
        self.log("步骤3: 创建update_file_version_review_state触发器函数", "INFO")
        self.log("="*70)

        sql = """
        CREATE OR REPLACE FUNCTION update_file_version_review_state()
        RETURNS TRIGGER AS $$
        DECLARE
            v_new_review_state VARCHAR(20);
        BEGIN
            -- 计算新的review状态
            SELECT compute_file_version_review_state(COALESCE(NEW.file_version_urn, OLD.file_version_urn))
            INTO v_new_review_state;

            -- 更新对应的file_version记录
            UPDATE file_versions
            SET review_state = v_new_review_state
            WHERE urn = COALESCE(NEW.file_version_urn, OLD.file_version_urn);

            RETURN COALESCE(NEW, OLD);
        END;
        $$ LANGUAGE plpgsql;
        """

        return self.execute_sql(sql, description="创建update_file_version_review_state函数")

    def step4_create_trigger(self) -> bool:
        """步骤4: 创建trigger"""
        self.log("\n" + "="*70)
        self.log("步骤4: 创建trigger_update_file_version_review_state触发器", "INFO")
        self.log("="*70)

        # 先删除已存在的触发器
        try:
            sql_drop = """
            DROP TRIGGER IF EXISTS trigger_update_file_version_review_state ON review_file_versions;
            """
            self.cur.execute(sql_drop)
            self.conn.commit()
            self.log("删除旧触发器 (如果存在)", "INFO")
        except Exception as e:
            self.log(f"删除旧触发器失败: {str(e)}", "WARN")

        sql = """
        CREATE TRIGGER trigger_update_file_version_review_state
            AFTER INSERT OR UPDATE OR DELETE ON review_file_versions
            FOR EACH ROW EXECUTE FUNCTION update_file_version_review_state();
        """

        return self.execute_sql(sql, description="创建trigger_update_file_version_review_state")

    def step5_create_index(self) -> bool:
        """步骤5: 创建性能索引"""
        self.log("\n" + "="*70)
        self.log("步骤5: 创建idx_file_versions_review_state索引", "INFO")
        self.log("="*70)

        # 先删除已存在的索引
        try:
            sql_drop = """
            DROP INDEX IF EXISTS idx_file_versions_review_state;
            """
            self.cur.execute(sql_drop)
            self.conn.commit()
            self.log("删除旧索引 (如果存在)", "INFO")
        except Exception as e:
            self.log(f"删除旧索引失败: {str(e)}", "WARN")

        # CREATE INDEX CONCURRENTLY 需要在autocommit模式下执行
        try:
            old_autocommit = self.conn.autocommit
            self.conn.autocommit = True

            sql = """
            CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_file_versions_review_state
            ON file_versions (review_state)
            WHERE review_state = 'InReview';
            """

            self.log("执行: 创建idx_file_versions_review_state索引...")
            self.cur.execute(sql)
            self.log("✓ 创建idx_file_versions_review_state索引 成功", "SUCCESS")

            self.conn.autocommit = old_autocommit
            return True
        except Exception as e:
            self.conn.autocommit = False
            error_msg = f"创建idx_file_versions_review_state索引 失败: {str(e)}"
            self.log(error_msg, "ERROR")
            self.errors.append(error_msg)
            return False

    def step6_create_backfill_function(self) -> bool:
        """步骤6: 创建回填函数"""
        self.log("\n" + "="*70)
        self.log("步骤6: 创建backfill_file_version_review_states函数", "INFO")
        self.log("="*70)

        sql = """
        CREATE OR REPLACE FUNCTION backfill_file_version_review_states()
        RETURNS TABLE (
            updated_count INTEGER,
            in_review_count INTEGER,
            not_in_review_count INTEGER
        ) AS $$
        DECLARE
            v_updated_count INTEGER := 0;
            v_in_review_count INTEGER := 0;
            v_not_in_review_count INTEGER := 0;
            v_file_version RECORD;
        BEGIN
            -- 遍历所有file_versions，计算并更新reviewState
            FOR v_file_version IN
                SELECT id, urn FROM file_versions
            LOOP
                -- 计算该版本的review_state
                UPDATE file_versions
                SET review_state = compute_file_version_review_state(v_file_version.urn),
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = v_file_version.id;

                v_updated_count := v_updated_count + 1;
            END LOOP;

            -- 统计结果
            SELECT COUNT(*) INTO v_in_review_count FROM file_versions WHERE review_state = 'InReview';
            SELECT COUNT(*) INTO v_not_in_review_count FROM file_versions WHERE review_state = 'NotInReview';

            RETURN QUERY SELECT v_updated_count, v_in_review_count, v_not_in_review_count;
        END;
        $$ LANGUAGE plpgsql;
        """

        return self.execute_sql(sql, description="创建backfill_file_version_review_states函数")

    def step7_backfill_data(self) -> bool:
        """步骤7: 回填现有数据"""
        self.log("\n" + "="*70)
        self.log("步骤7: 回填现有file_versions数据的reviewState", "INFO")
        self.log("="*70)

        try:
            self.log("执行回填函数...")
            sql = "SELECT * FROM backfill_file_version_review_states();"
            self.cur.execute(sql)
            result = self.cur.fetchone()
            self.conn.commit()

            if result:
                updated_count, in_review_count, not_in_review_count = result
                self.log(f"✓ 回填完成:", "SUCCESS")
                self.log(f"  - 更新总数: {updated_count}", "SUCCESS")
                self.log(f"  - InReview数: {in_review_count}", "SUCCESS")
                self.log(f"  - NotInReview数: {not_in_review_count}", "SUCCESS")
                return True
            else:
                self.log("回填函数执行失败", "ERROR")
                return False
        except Exception as e:
            self.conn.rollback()
            error_msg = f"回填数据失败: {str(e)}"
            self.log(error_msg, "ERROR")
            self.errors.append(error_msg)
            return False

    def verify_implementation(self) -> bool:
        """验证实现"""
        self.log("\n" + "="*70)
        self.log("验证: 检查所有组件是否成功创建", "INFO")
        self.log("="*70)

        all_ok = True

        # 检查列
        if self.check_column_exists('file_versions', 'review_state'):
            self.log("✓ review_state列已存在", "SUCCESS")
        else:
            self.log("✗ review_state列不存在", "ERROR")
            all_ok = False

        # 检查函数
        if self.check_function_exists('compute_file_version_review_state'):
            self.log("✓ compute_file_version_review_state函数已存在", "SUCCESS")
        else:
            self.log("✗ compute_file_version_review_state函数不存在", "ERROR")
            all_ok = False

        if self.check_function_exists('update_file_version_review_state'):
            self.log("✓ update_file_version_review_state函数已存在", "SUCCESS")
        else:
            self.log("✗ update_file_version_review_state函数不存在", "ERROR")
            all_ok = False

        if self.check_function_exists('backfill_file_version_review_states'):
            self.log("✓ backfill_file_version_review_states函数已存在", "SUCCESS")
        else:
            self.log("✗ backfill_file_version_review_states函数不存在", "ERROR")
            all_ok = False

        # 检查数据示例
        try:
            sql = "SELECT COUNT(*) as total, review_state FROM file_versions GROUP BY review_state;"
            self.cur.execute(sql)
            results = self.cur.fetchall()

            self.log("✓ file_versions数据统计:", "SUCCESS")
            for row in results:
                self.log(f"  - {row['review_state']}: {row['total']} 条记录", "SUCCESS")
        except Exception as e:
            self.log(f"✗ 查询数据统计失败: {str(e)}", "ERROR")
            all_ok = False

        return all_ok

    def run(self) -> bool:
        """运行完整的实现流程"""
        try:
            # 连接数据库
            if not self.connect():
                return False

            # 执行各个步骤
            steps = [
                self.step1_add_review_state_column,
                self.step2_create_compute_function,
                self.step3_create_trigger_function,
                self.step4_create_trigger,
                self.step5_create_index,
                self.step6_create_backfill_function,
                self.step7_backfill_data,
                self.verify_implementation
            ]

            for step in steps:
                if not step():
                    self.log(f"步骤失败: {step.__name__}", "ERROR")
                    if self.errors:
                        return False

            # 总结
            self.log("\n" + "="*70)
            self.log("实现完成!", "SUCCESS")
            self.log("="*70)

            if self.errors:
                self.log(f"\n⚠️  遇到 {len(self.errors)} 个错误:", "WARN")
                for error in self.errors:
                    self.log(f"  - {error}", "ERROR")
                return False
            else:
                self.log("✓ 所有步骤完成，没有错误!", "SUCCESS")
                return True

        except Exception as e:
            self.log(f"实现过程中发生异常: {str(e)}", "ERROR")
            return False
        finally:
            self.disconnect()


def main():
    """主函数"""
    implementor = ReviewStateImplementor()
    success = implementor.run()

    # 打印日志
    print("\n" + "="*70)
    print("完整日志:")
    print("="*70)
    for log_msg in implementor.logs:
        print(log_msg)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
