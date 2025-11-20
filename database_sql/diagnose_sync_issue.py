"""
Diagnose Sync Issue Script
Check why database has no changes after sync
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
from database_sql.review_data_access import ReviewDataAccess
import psycopg2.extras

def diagnose_sync_issue():
    """诊断同步问题"""
    
    print("="*80)
    print("同步问题诊断")
    print("="*80)
    
    # 连接数据库
    neon_config = NeonConfig()
    da = ReviewDataAccess(neon_config.get_db_params())
    
    conn = None
    try:
        conn = da.get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # 1. 检查表是否存在
        print("\n1. 检查表结构")
        print("-" * 80)
        
        tables_to_check = [
            'workflows',
            'reviews', 
            'review_file_versions',
            'review_progress',
            'review_step_candidates',
            'file_versions'
        ]
        
        for table in tables_to_check:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = %s
                );
            """, [table])
            exists = cursor.fetchone()['exists']
            
            if exists:
                cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                count = cursor.fetchone()['count']
                print(f"✓ {table:30s} - 存在 ({count} 条记录)")
            else:
                print(f"✗ {table:30s} - 不存在")
        
        # 2. 检查 review_file_versions 表结构
        print("\n2. 检查 review_file_versions 表结构")
        print("-" * 80)
        
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'review_file_versions'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        if columns:
            print("字段列表:")
            for col in columns:
                nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
                print(f"  - {col['column_name']:30s} {col['data_type']:20s} {nullable}")
            
            # 检查关键字段
            column_names = [col['column_name'] for col in columns]
            
            print("\n关键字段检查:")
            if 'file_version_urn' in column_names:
                print("  ✓ file_version_urn 字段存在 (新架构)")
            elif 'file_urn' in column_names:
                print("  ✗ file_urn 字段存在 (旧架构) - 需要迁移!")
            else:
                print("  ✗ 缺少文件引用字段")
        else:
            print("✗ review_file_versions 表不存在")
        
        # 3. 检查约束
        print("\n3. 检查唯一约束")
        print("-" * 80)
        
        cursor.execute("""
            SELECT conname, pg_get_constraintdef(oid) as definition
            FROM pg_constraint
            WHERE conrelid = 'review_file_versions'::regclass
            AND contype = 'u';
        """)
        
        constraints = cursor.fetchall()
        if constraints:
            for constraint in constraints:
                print(f"  - {constraint['conname']}: {constraint['definition']}")
        else:
            print("  (无唯一约束)")
        
        # 4. 检查最近的同步记录
        print("\n4. 检查最近的同步记录")
        print("-" * 80)
        
        cursor.execute("""
            SELECT COUNT(*) as count,
                   MAX(last_synced_at) as last_sync
            FROM reviews
            WHERE last_synced_at IS NOT NULL;
        """)
        
        sync_info = cursor.fetchone()
        print(f"  同步的评审数量: {sync_info['count']}")
        print(f"  最后同步时间: {sync_info['last_sync']}")
        
        # 5. 检查 file_versions 表
        print("\n5. 检查 file_versions 表")
        print("-" * 80)
        
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'file_versions'
            );
        """)
        
        fv_exists = cursor.fetchone()['exists']
        
        if fv_exists:
            cursor.execute("SELECT COUNT(*) as count FROM file_versions")
            fv_count = cursor.fetchone()['count']
            print(f"  ✓ file_versions 表存在 ({fv_count} 条记录)")
            
            if fv_count > 0:
                cursor.execute("""
                    SELECT urn, file_id, version_number, created_at
                    FROM file_versions
                    ORDER BY created_at DESC
                    LIMIT 3
                """)
                
                print("\n  最近的文件版本:")
                for fv in cursor.fetchall():
                    print(f"    - URN: {fv['urn'][:50]}...")
                    print(f"      Version: {fv['version_number']}, Created: {fv['created_at']}")
        else:
            print("  ✗ file_versions 表不存在 - 需要先运行文件同步!")
        
        # 6. 检查 review_file_versions 数据
        print("\n6. 检查 review_file_versions 数据")
        print("-" * 80)
        
        cursor.execute("SELECT COUNT(*) as count FROM review_file_versions")
        rfv_count = cursor.fetchone()['count']
        
        if rfv_count > 0:
            print(f"  ✓ 有 {rfv_count} 条记录")
            
            cursor.execute("""
                SELECT id, review_id, 
                       CASE 
                           WHEN EXISTS (
                               SELECT 1 FROM information_schema.columns 
                               WHERE table_name = 'review_file_versions' 
                               AND column_name = 'file_version_urn'
                           ) THEN (SELECT file_version_urn FROM review_file_versions rfv2 WHERE rfv2.id = rfv.id)
                           ELSE (SELECT file_urn FROM review_file_versions rfv2 WHERE rfv2.id = rfv.id)
                       END as file_ref,
                       approval_status, created_at
                FROM review_file_versions rfv
                ORDER BY created_at DESC
                LIMIT 3
            """)
            
            print("\n  最近的记录:")
            for rfv in cursor.fetchall():
                print(f"    - Review ID: {rfv['review_id']}, Status: {rfv['approval_status']}")
                print(f"      File Ref: {rfv['file_ref'][:50] if rfv['file_ref'] else 'NULL'}...")
                print(f"      Created: {rfv['created_at']}")
        else:
            print("  ✗ 没有记录 - 同步可能失败!")
        
        # 7. 检查同步错误
        print("\n7. 建议")
        print("-" * 80)
        
        if not fv_exists or fv_count == 0:
            print("  ⚠️  file_versions 表为空或不存在")
            print("     建议：先运行文件同步 (postgresql_sync_manager.py)")
            print("     命令：python api_modules/postgresql_sync/postgresql_sync_manager.py")
        
        if 'file_urn' in column_names and 'file_version_urn' not in column_names:
            print("  ⚠️  review_file_versions 使用旧架构")
            print("     建议：运行架构迁移")
            print("     1. 备份数据")
            print("     2. 运行: python database_sql/full_review_sync.py --clean")
        
        if rfv_count == 0:
            print("  ⚠️  review_file_versions 表为空")
            print("     可能原因：")
            print("     1. 同步过程中发生错误")
            print("     2. file_version_urn 不匹配")
            print("     3. 批量插入失败")
        
        cursor.close()
        
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if conn:
            conn.close()
    
    print("\n" + "="*80)


if __name__ == "__main__":
    diagnose_sync_issue()

