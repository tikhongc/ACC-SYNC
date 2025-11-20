"""
添加 review_file_versions 到 file_versions 的外键约束
"""

import sys
import os
import codecs

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    try:
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except AttributeError:
        pass

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from database_sql.neon_config import NeonConfig
import psycopg2


def add_foreign_key():
    """添加外键约束"""
    
    print("="*80)
    print("添加 review_file_versions -> file_versions 外键约束")
    print("="*80)
    
    # 连接数据库
    neon_config = NeonConfig()
    conn = None
    
    try:
        conn = psycopg2.connect(**neon_config.get_db_params())
        cursor = conn.cursor()
        
        # 读取 SQL 文件
        sql_file = os.path.join(current_dir, 'add_file_version_foreign_key.sql')
        
        print(f"\n读取 SQL 文件: {sql_file}")
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql = f.read()
        
        print("\n执行 SQL...")
        cursor.execute(sql)
        conn.commit()
        
        print("\n✓ 外键约束添加成功！")
        
        cursor.close()
        
    except psycopg2.Error as e:
        print(f"\n✗ 数据库错误: {e}")
        if conn:
            conn.rollback()
        sys.exit(1)
    
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        if conn:
            conn.rollback()
        sys.exit(1)
    
    finally:
        if conn:
            conn.close()
    
    print("\n" + "="*80)


if __name__ == "__main__":
    add_foreign_key()

