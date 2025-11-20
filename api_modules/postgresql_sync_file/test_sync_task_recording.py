#!/usr/bin/env python3
"""
Test sync task recording functionality without requiring authentication
"""

import asyncio
import sys
import os
from datetime import datetime

# Add project paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

async def test_sync_task_recording():
    """Test the sync task recording functionality"""
    
    print("Testing sync task recording functionality...")
    
    try:
        from postgresql_sync_utils import TaskManager
        
        # Test 1: Generate task UUID
        task_uuid = TaskManager.generate_task_uuid()
        print(f"Generated task UUID: {task_uuid}")
        
        # Test 2: Create sync task record
        project_id = "b.1eea4119-3553-4167-b93d-3a3d5d07d33d"
        task_type = "optimized_full_sync"
        performance_mode = "standard"
        parameters = {
            'max_depth': 10,
            'include_custom_attributes': True,
            'test_mode': True
        }
        
        print("Creating sync task record...")
        task_created = await TaskManager.create_sync_task_record(
            project_id=project_id,
            task_uuid=task_uuid,
            task_type=task_type,
            performance_mode=performance_mode,
            parameters=parameters
        )
        
        if task_created:
            print("SUCCESS: Sync task record created")
            
            # Test 3: Complete sync task record
            print("Completing sync task record...")
            results = {
                'status': 'success',
                'message': 'Test sync completed successfully',
                'folders_synced': 15,
                'files_synced': 25,
                'custom_attrs_synced': 8,
                'versions_synced': 30,
                'duration_seconds': 45.5,
                'sync_type': 'optimized_full_sync',
                'synced_file_tree': True,
                'synced_versions': True,
                'synced_custom_attributes_definitions': True,
                'synced_custom_attributes_values': True,
                'synced_permissions': False,
                'performance_stats': {
                    'api_calls': 50,
                    'api_calls_saved': 10,
                    'optimization_efficiency': 85.5
                }
            }
            
            task_completed = await TaskManager.complete_sync_task_record(
                task_uuid, results
            )
            
            if task_completed:
                print("SUCCESS: Sync task record completed")
                
                # Verify in database
                from database_sql.optimized_data_access import get_optimized_postgresql_dal
                dal = await get_optimized_postgresql_dal()
                
                async with dal.get_connection() as conn:
                    record = await conn.fetchrow(
                        "SELECT * FROM sync_tasks WHERE task_uuid = $1", 
                        task_uuid
                    )
                    
                    if record:
                        print("SUCCESS: Sync task found in database")
                        print(f"  Task Status: {record['task_status']}")
                        print(f"  Folders Synced: {record['folders_synced']}")
                        print(f"  Files Synced: {record['files_synced']}")
                        print(f"  Versions Synced: {record['versions_synced']}")
                        print(f"  Custom Attrs Synced: {record['custom_attrs_synced']}")
                        print(f"  Duration: {record['duration_seconds']} seconds")
                        print(f"  Synced File Tree: {record['synced_file_tree']}")
                        print(f"  Synced Versions: {record['synced_versions']}")
                        print(f"  Synced Custom Attr Defs: {record['synced_custom_attributes_definitions']}")
                        print(f"  Synced Custom Attr Values: {record['synced_custom_attributes_values']}")
                        print(f"  Synced Permissions: {record['synced_permissions']}")
                        return True
                    else:
                        print("ERROR: Sync task not found in database")
                        return False
            else:
                print("ERROR: Failed to complete sync task record")
                return False
        else:
            print("ERROR: Failed to create sync task record")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main function"""
    success = await test_sync_task_recording()
    
    if success:
        print("\n" + "="*60)
        print("SYNC TASK RECORDING TEST: PASSED")
        print("The sync task recording functionality is working correctly!")
        print("="*60)
        return 0
    else:
        print("\n" + "="*60)
        print("SYNC TASK RECORDING TEST: FAILED")
        print("There are issues with the sync task recording functionality.")
        print("="*60)
        return 1

if __name__ == "__main__":
    exit(asyncio.run(main()))
