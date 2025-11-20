#!/usr/bin/env python3
"""
Debug Timestamps Script
Checks the timestamp comparison logic between last_sync_time and rollup_time
"""

import asyncio
import sys
import os
from datetime import datetime, timezone

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from database_sql.optimized_data_access import get_optimized_postgresql_dal
from api_modules.postgresql_sync_file.postgresql_sync_manager import optimized_postgresql_sync_manager

async def debug_timestamps():
    """Debug timestamp comparison logic"""
    
    print("=== Timestamp Debug Analysis ===")
    
    project_id = 'b.1eea4119-3553-4167-b93d-3a3d5d07d33d'
    
    try:
        dal = await get_optimized_postgresql_dal()
        
        # 1. Get last sync time from database
        print("1. Getting last sync time from database...")
        last_sync_time = await dal.get_project_last_sync_time(project_id)
        
        if last_sync_time:
            print(f"   Last sync time: {last_sync_time}")
            print(f"   Type: {type(last_sync_time)}")
            print(f"   Timezone: {last_sync_time.tzinfo}")
            print(f"   ISO format: {last_sync_time.isoformat()}")
        else:
            print("   No last sync time found!")
            return
        
        print()
        
        # 2. Get top-level folders and their rollup times
        print("2. Getting top-level folders rollup times...")
        
        async with dal.get_connection() as conn:
            query = """
            SELECT 
                id, name, 
                last_modified_time,
                last_modified_time_rollup,
                parent_id,
                depth
            FROM folders 
            WHERE project_id = $1 
              AND depth = 0
            ORDER BY name
            LIMIT 10
            """
            
            folders = await conn.fetch(query, project_id)
            
            print(f"   Found {len(folders)} top-level folders:")
            
            for folder in folders:
                rollup_time = folder['last_modified_time_rollup']
                modified_time = folder['last_modified_time']
                
                print(f"\n   Folder: {folder['name']}")
                print(f"     ID: {folder['id']}")
                print(f"     Depth: {folder['depth']}")
                print(f"     Parent ID: {folder['parent_id']}")
                print(f"     Last Modified: {modified_time}")
                print(f"     Rollup Time: {rollup_time}")
                
                if rollup_time:
                    print(f"     Rollup Type: {type(rollup_time)}")
                    print(f"     Rollup Timezone: {rollup_time.tzinfo}")
                    print(f"     Rollup ISO: {rollup_time.isoformat()}")
                    
                    # Compare with last sync time
                    comparison_result = rollup_time <= last_sync_time
                    print(f"     Rollup <= Last Sync: {comparison_result}")
                    
                    if comparison_result:
                        print(f"     -> SKIP: This folder would be skipped")
                    else:
                        print(f"     -> PROCESS: This folder needs processing")
                        print(f"     -> Time diff: {rollup_time - last_sync_time}")
                else:
                    print(f"     -> PROCESS: No rollup time (NULL)")
        
        print()
        
        # 3. Test the smart branch filtering
        print("3. Testing smart branch filtering...")
        
        folders_to_check = await dal.get_folders_for_smart_skip_check(project_id, last_sync_time)
        print(f"   Folders needing check: {len(folders_to_check)}")
        
        for i, folder in enumerate(folders_to_check[:5]):  # Show first 5
            rollup_time_str = folder.get('last_modified_time_rollup')
            
            print(f"\n   Folder {i+1}: {folder.get('name')}")
            print(f"     Rollup (raw): {rollup_time_str}")
            print(f"     Rollup type: {type(rollup_time_str)}")
            
            # Test parsing
            parsed_rollup = optimized_postgresql_sync_manager._parse_datetime(rollup_time_str)
            print(f"     Parsed rollup: {parsed_rollup}")
            
            if parsed_rollup:
                print(f"     Parsed type: {type(parsed_rollup)}")
                print(f"     Parsed timezone: {parsed_rollup.tzinfo}")
                
                # Test comparison
                comparison = parsed_rollup <= last_sync_time
                print(f"     Comparison result: {comparison}")
                
                if not comparison:
                    print(f"     Time difference: {parsed_rollup - last_sync_time}")
        
        print()
        
        # 4. Check project-level rollup optimization
        print("4. Testing project-level rollup optimization...")
        
        async with dal.get_connection() as conn:
            query = """
            SELECT 
                MAX(last_modified_time_rollup) as max_rollup_time,
                COUNT(*) as total_top_level_folders,
                COUNT(CASE WHEN last_modified_time_rollup > $2 THEN 1 END) as folders_with_changes
            FROM folders 
            WHERE project_id = $1 
              AND depth = 0
              AND last_modified_time_rollup IS NOT NULL
            """
            
            result = await conn.fetchrow(query, project_id, last_sync_time)
            
            if result:
                max_rollup = result['max_rollup_time']
                total_folders = result['total_top_level_folders']
                folders_with_changes = result['folders_with_changes']
                
                print(f"   Max rollup time: {max_rollup}")
                print(f"   Total top folders: {total_folders}")
                print(f"   Folders with changes: {folders_with_changes}")
                
                if max_rollup:
                    can_skip_project = max_rollup <= last_sync_time
                    print(f"   Can skip entire project: {can_skip_project}")
                    
                    if can_skip_project:
                        print("   -> PROJECT SKIP: Entire project would be skipped!")
                    else:
                        print("   -> PROJECT PROCESS: Project needs processing")
                        print(f"   -> Max rollup vs last sync: {max_rollup} vs {last_sync_time}")
                        print(f"   -> Time difference: {max_rollup - last_sync_time}")
        
        print("\n=== Analysis Complete ===")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_timestamps())
