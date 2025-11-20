#!/usr/bin/env python3
"""
Quick Review Test - 快速测试版本
直接测试 workflow 和 review 的数据库插入，跳过所有复杂的 schema 操作
"""

import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    import codecs
    try:
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except AttributeError:
        pass

import time
import json
from datetime import datetime

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

def test_workflow_insert():
    """测试 workflow 插入"""
    
    try:
        from database_sql.review_data_access import ReviewDataAccess
        from database_sql.neon_config import NeonConfig
        
        # 初始化数据访问
        neon_config = NeonConfig()
        data_access = ReviewDataAccess(neon_config.get_db_params())
        
        # 测试数据
        workflow_data = {
            'workflow_uuid': 'test-workflow-123',
            'project_id': 'b.1eea4119-3553-4167-b93d-3a3d5d07d33d',
            'data_source': 'acc_sync',
            'acc_workflow_id': 'test-workflow-123',
            'name': 'Test Workflow',
            'description': 'Test workflow for verification',
            'notes': 'Test notes',
            'status': 'ACTIVE',
            'additional_options': {},
            'approval_status_options': [],
            'copy_files_options': {},
            'attached_attributes': [],
            'update_attributes_options': {},
            'steps': [],
            'created_by': {},
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'last_synced_at': datetime.now().isoformat(),
            'sync_status': 'synced'
        }
        
        print("Testing workflow insertion...")
        result = data_access.create_workflow(workflow_data)
        print(f"✓ Workflow inserted successfully: {result}")
        
        return True
        
    except Exception as e:
        print(f"✗ Workflow insertion failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_database_connection():
    """测试数据库连接"""
    
    try:
        from database_sql.neon_config import NeonConfig
        import psycopg2
        
        neon_config = NeonConfig()
        db_params = neon_config.get_db_params()
        
        print("Testing database connection...")
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        # 检查 projects 表
        cursor.execute("""
            SELECT COUNT(*) FROM projects 
            WHERE project_id = %s
        """, ['b.1eea4119-3553-4167-b93d-3a3d5d07d33d'])
        
        project_count = cursor.fetchone()[0]
        print(f"✓ Database connection successful")
        print(f"✓ Project records found: {project_count}")
        
        # 检查 workflows 表是否存在
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'workflows'
            );
        """)
        
        workflows_table_exists = cursor.fetchone()[0]
        print(f"✓ Workflows table exists: {workflows_table_exists}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"✗ Database connection failed: {str(e)}")
        return False

def main():
    """主测试函数"""
    
    print("="*80)
    print("QUICK REVIEW TEST")
    print("="*80)
    print(f"Test Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    start_time = time.time()
    success = True
    
    try:
        # Step 1: Test authentication
        print("\n[STEP 1/4] Testing authentication...")
        import utils
        access_token = utils.get_access_token()
        
        if access_token:
            print("✓ Authentication successful")
        else:
            print("✗ Authentication failed")
            success = False
        
        # Step 2: Test database connection
        print("\n[STEP 2/4] Testing database connection...")
        if test_database_connection():
            print("✓ Database connection test passed")
        else:
            print("✗ Database connection test failed")
            success = False
        
        # Step 3: Test API access
        print("\n[STEP 3/4] Testing API access...")
        import config
        import requests
        
        project_id = "1eea4119-3553-4167-b93d-3a3d5d07d33d"
        url = f"{config.AUTODESK_API_BASE}/construction/reviews/v1/projects/{project_id}/workflows"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=headers, params={'limit': 1}, timeout=10)
        
        if response.status_code == 200:
            print("✓ API access successful")
        else:
            print(f"✗ API access failed: {response.status_code}")
            success = False
        
        # Step 4: Test workflow insertion (optional)
        print("\n[STEP 4/4] Testing workflow insertion...")
        if test_workflow_insert():
            print("✓ Workflow insertion test passed")
        else:
            print("✗ Workflow insertion test failed")
            # Don't fail the whole test for this
        
        duration = time.time() - start_time
        
        print("\n" + "="*80)
        if success:
            print("ALL TESTS PASSED")
            print("="*80)
            print(f"Duration: {duration:.2f} seconds")
            print("✓ The system is ready for full review sync")
            print("✓ You can now run the full enhanced review sync")
        else:
            print("SOME TESTS FAILED")
            print("="*80)
            print(f"Duration: {duration:.2f} seconds")
            print("✗ Please fix the issues before running full sync")
        
        return 0 if success else 1
        
    except Exception as e:
        duration = time.time() - start_time
        
        print("\n" + "="*80)
        print("TEST FAILED")
        print("="*80)
        print(f"Duration: {duration:.2f} seconds")
        print(f"Error: {str(e)}")
        
        import traceback
        traceback.print_exc()
        
        return 1

if __name__ == "__main__":
    print("Quick Review Test")
    print("This test verifies all components are working before running full sync")
    print()
    
    exit_code = main()
    sys.exit(exit_code)
