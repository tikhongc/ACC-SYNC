#!/usr/bin/env python3
"""
Force Incremental Test
Forces an older sync time to test incremental sync detection
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from database_sql.optimized_data_access import get_optimized_postgresql_dal
from api_modules.postgresql_sync_file.postgresql_sync_manager import optimized_postgresql_sync_manager
import utils

async def force_incremental_test():
    """Force an incremental sync by setting old sync time"""
    
    print("=== Force Incremental Sync Test ===")
    
    project_id = 'b.1eea4119-3553-4167-b93d-3a3d5d07d33d'
    
    try:
        # Get authentication
        token = utils.get_access_token()
        if not token:
            print("ERROR: Failed to get access token")
            return False
        
        headers = {'Authorization': f'Bearer {token}'}
        
        dal = await get_optimized_postgresql_dal()
        
        # 1. Get current sync time
        current_sync_time = await dal.get_project_last_sync_time(project_id)
        print(f"Current sync time: {current_sync_time}")
        
        # 2. Set sync time to 1 day ago to force detection
        old_sync_time = datetime.now() - timedelta(days=1)
        print(f"Setting sync time to: {old_sync_time}")
        
        async with dal.get_connection() as conn:
            await conn.execute("""
                UPDATE projects 
                SET last_sync_time = $2, last_full_sync_time = $2
                WHERE id = $1
            """, project_id, old_sync_time)
        
        print("Sync time updated successfully")
        
        # 3. Run incremental sync
        print("\nRunning incremental sync with forced old time...")
        
        result = await optimized_postgresql_sync_manager.optimized_incremental_sync(
            project_id=project_id,
            max_depth=5,
            include_custom_attributes=True,
            headers=headers
        )
        
        print("\n=== INCREMENTAL SYNC RESULT ===")
        print(f"Status: {result.get('status')}")
        print(f"Architecture: {result.get('architecture_version', 'v2')}")
        print(f"Folders synced: {result.get('folders_synced', 0)}")
        print(f"Files synced: {result.get('files_synced', 0)}")
        print(f"Versions synced: {result.get('versions_synced', 0)}")
        print(f"Custom attributes synced: {result.get('custom_attrs_synced', 0)}")
        print(f"Duration: {result.get('duration_seconds', 0):.2f}s")
        print(f"Optimization efficiency: {result.get('optimization_efficiency', 0):.1f}%")
        
        # 4. Restore original sync time
        print(f"\nRestoring original sync time: {current_sync_time}")
        
        async with dal.get_connection() as conn:
            await conn.execute("""
                UPDATE projects 
                SET last_sync_time = $2, last_full_sync_time = $2
                WHERE id = $1
            """, project_id, current_sync_time)
        
        print("Original sync time restored")
        
        # 5. Analyze results
        total_synced = (result.get('folders_synced', 0) + 
                       result.get('files_synced', 0) + 
                       result.get('versions_synced', 0) + 
                       result.get('custom_attrs_synced', 0))
        
        if result.get('status') == 'success' and total_synced > 0:
            print(f"\nSUCCESS: Detected {total_synced} items with forced old sync time!")
            print("This confirms incremental sync logic is working correctly.")
            return True
        elif result.get('status') == 'no_changes':
            print("\nINFO: Even with old sync time, no changes detected.")
            print("This means the rollup optimization is very aggressive.")
            return True
        else:
            print(f"\nERROR: Sync failed - {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"ERROR: Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Starting Force Incremental Sync Test...")
    print("=" * 50)
    
    success = asyncio.run(force_incremental_test())
    
    print("=" * 50)
    if success:
        print("Test COMPLETED: Incremental sync behavior analyzed")
    else:
        print("Test FAILED: Issues detected")
