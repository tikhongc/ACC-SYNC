# -*- coding: utf-8 -*-
"""
Test database connection for permissions sync
Quick validation of configuration
"""

import asyncio
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

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_modules.permissions_db_sync import PermissionsDatabaseSync, DEFAULT_PROJECT_ID


async def test_connection():
    """Test database connection and folder query"""
    print("=" * 60)
    print("Permissions Sync Database Connection Test")
    print("=" * 60)

    syncer = PermissionsDatabaseSync(DEFAULT_PROJECT_ID)

    try:
        # Test connection
        print("\n1. Testing database connection...")
        await syncer.connect()
        print("   OK Database connected successfully")

        # Test query folders
        print("\n2. Querying folders from database...")
        folders = await syncer.get_all_folder_ids()
        print(f"   OK Found {len(folders)} folders")

        if folders:
            print("\n3. First 5 folders:")
            for i, (folder_id, folder_name, folder_path) in enumerate(folders[:5], 1):
                print(f"   {i}. {folder_name}")
                print(f"      ID: {folder_id}")
                print(f"      Path: {folder_path}")

        print("\n" + "=" * 60)
        print("OK All tests passed!")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"\nX Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        await syncer.close()


if __name__ == "__main__":
    success = asyncio.run(test_connection())
    sys.exit(0 if success else 1)
