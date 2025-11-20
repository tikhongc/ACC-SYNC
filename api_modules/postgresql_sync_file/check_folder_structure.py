#!/usr/bin/env python3
"""
Check Folder Structure Script
Analyzes the actual folder structure in the database
"""

import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from database_sql.optimized_data_access import get_optimized_postgresql_dal

async def check_folder_structure():
    """Check the actual folder structure in database"""
    
    print("=== Database Folder Structure Analysis ===")
    
    project_id = 'b.1eea4119-3553-4167-b93d-3a3d5d07d33d'
    
    try:
        dal = await get_optimized_postgresql_dal()
        
        async with dal.get_connection() as conn:
            # 1. Check all folders
            print("1. All folders in database:")
            query1 = """
            SELECT 
                id, name, parent_id, depth, path,
                last_modified_time, last_modified_time_rollup
            FROM folders 
            WHERE project_id = $1 
            ORDER BY depth, name
            LIMIT 20
            """
            
            all_folders = await conn.fetch(query1, project_id)
            print(f"   Total folders found: {len(all_folders)}")
            
            for folder in all_folders:
                print(f"\n   Folder: {folder['name']}")
                print(f"     ID: {folder['id']}")
                print(f"     Parent ID: {folder['parent_id']}")
                print(f"     Depth: {folder['depth']}")
                print(f"     Path: {folder['path']}")
                print(f"     Last Modified: {folder['last_modified_time']}")
                print(f"     Rollup Time: {folder['last_modified_time_rollup']}")
            
            print("\n" + "="*50)
            
            # 2. Check parent_id patterns
            print("2. Parent ID analysis:")
            query2 = """
            SELECT 
                parent_id,
                COUNT(*) as count,
                array_agg(name ORDER BY name) as folder_names
            FROM folders 
            WHERE project_id = $1 
            GROUP BY parent_id
            ORDER BY count DESC
            """
            
            parent_analysis = await conn.fetch(query2, project_id)
            
            for row in parent_analysis:
                parent_id = row['parent_id']
                count = row['count']
                names = row['folder_names'][:5]  # Show first 5 names
                
                if parent_id is None:
                    print(f"   NULL parent_id: {count} folders")
                elif parent_id == '':
                    print(f"   Empty string parent_id: {count} folders")
                else:
                    print(f"   Parent '{parent_id}': {count} folders")
                print(f"     Sample names: {names}")
            
            print("\n" + "="*50)
            
            # 3. Check depth distribution
            print("3. Depth distribution:")
            query3 = """
            SELECT 
                depth,
                COUNT(*) as count,
                array_agg(name ORDER BY name) as sample_names
            FROM folders 
            WHERE project_id = $1 
            GROUP BY depth
            ORDER BY depth
            """
            
            depth_analysis = await conn.fetch(query3, project_id)
            
            for row in depth_analysis:
                depth = row['depth']
                count = row['count']
                sample_names = row['sample_names'][:3]  # Show first 3 names
                
                print(f"   Depth {depth}: {count} folders")
                print(f"     Sample: {sample_names}")
            
            print("\n" + "="*50)
            
            # 4. Find potential root folders
            print("4. Potential root folders (depth 0 or minimal parent references):")
            query4 = """
            SELECT 
                id, name, parent_id, depth, path
            FROM folders 
            WHERE project_id = $1 
              AND (depth = 0 OR parent_id NOT IN (
                  SELECT DISTINCT id FROM folders WHERE project_id = $1
              ))
            ORDER BY depth, name
            """
            
            root_candidates = await conn.fetch(query4, project_id)
            
            print(f"   Found {len(root_candidates)} potential root folders:")
            for folder in root_candidates:
                print(f"     {folder['name']} (ID: {folder['id']}, Parent: {folder['parent_id']}, Depth: {folder['depth']})")
            
            print("\n" + "="*50)
            
            # 5. Check files count
            print("5. Files count:")
            query5 = """
            SELECT COUNT(*) as file_count
            FROM files 
            WHERE project_id = $1
            """
            
            file_result = await conn.fetchrow(query5, project_id)
            print(f"   Total files: {file_result['file_count']}")
            
            # 6. Check file versions count
            query6 = """
            SELECT COUNT(*) as version_count
            FROM file_versions 
            WHERE project_id = $1
            """
            
            version_result = await conn.fetchrow(query6, project_id)
            print(f"   Total file versions: {version_result['version_count']}")
        
        print("\n=== Analysis Complete ===")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(check_folder_structure())
