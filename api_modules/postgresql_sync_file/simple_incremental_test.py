#!/usr/bin/env python3
"""
Simple Incremental Sync Test
Tests the incremental sync method directly
"""

import asyncio
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from api_modules.postgresql_sync_file.postgresql_sync_manager import optimized_postgresql_sync_manager
import utils

async def test_incremental_sync():
    """Test incremental sync directly"""
    
    print("=== Simple Incremental Sync Test ===")
    
    # Get authentication
    token = utils.get_access_token()
    if not token:
        print("ERROR: Failed to get access token")
        return False
    
    headers = {'Authorization': f'Bearer {token}'}
    project_id = 'b.1eea4119-3553-4167-b93d-3a3d5d07d33d'
    
    print(f"Project ID: {project_id}")
    print(f"Token: {'*' * 20}...{token[-10:]}")
    print()
    
    try:
        # Test incremental sync
        print("Running incremental sync...")
        start_time = datetime.now()
        
        result = await optimized_postgresql_sync_manager.optimized_incremental_sync(
            project_id=project_id,
            max_depth=5,
            include_custom_attributes=True,
            headers=headers
        )
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print(f"Sync completed in {duration:.2f} seconds")
        print()
        print("=== RESULT ===")
        print(f"Status: {result.get('status')}")
        print(f"Architecture: {result.get('architecture_version', 'v2')}")
        print(f"Folders synced: {result.get('folders_synced', 0)}")
        print(f"Files synced: {result.get('files_synced', 0)}")
        print(f"Versions synced: {result.get('versions_synced', 0)}")
        print(f"Custom attributes synced: {result.get('custom_attrs_synced', 0)}")
        print(f"Duration: {result.get('duration_seconds', duration):.2f}s")
        print(f"Optimization efficiency: {result.get('optimization_efficiency', 0):.1f}%")
        
        if result.get('status') == 'success':
            total_synced = (result.get('folders_synced', 0) + 
                          result.get('files_synced', 0) + 
                          result.get('versions_synced', 0) + 
                          result.get('custom_attrs_synced', 0))
            
            if total_synced > 0:
                print(f"\nSUCCESS: Detected {total_synced} changes!")
                return True
            else:
                print("\nINFO: No changes detected (this is normal if no new files were uploaded)")
                return True
        elif result.get('status') == 'no_changes':
            print("\nINFO: Smart skip optimization - no changes detected")
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
    print("Starting Simple Incremental Sync Test...")
    print("=" * 50)
    
    success = asyncio.run(test_incremental_sync())
    
    print("=" * 50)
    if success:
        print("Test PASSED: Incremental sync is working correctly")
        sys.exit(0)
    else:
        print("Test FAILED: Incremental sync has issues")
        sys.exit(1)
