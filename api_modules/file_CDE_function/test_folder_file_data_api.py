# -*- coding: utf-8 -*-
"""
Test script for folder_file_data_api.py
Tests all 4 API endpoints with real database data
"""

import requests
import json
import sys
import codecs

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    try:
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except AttributeError:
        pass

# Configuration
BASE_URL = "http://localhost:8080"
PROJECT_ID = "b.1eea4119-3553-4167-b93d-3a3d5d07d33d"

# Test data (you may need to replace these with actual IDs from your database)
FOLDER_ID = "urn:adsk.wipprod:fs.folder:co.7ajfDFd6TuWQCKLqpyf9NA"  # Project Files folder
FILE_ID = None  # Will be determined from database query


def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_response(response):
    """Print formatted response"""
    try:
        data = response.json()
        print(f"Status Code: {response.status_code}")
        print(f"Response:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")


def test_health_check():
    """Test health check endpoint"""
    print_header("Test 1: Health Check")

    url = f"{BASE_URL}/api/folder-file-data/health"
    print(f"GET {url}")

    try:
        response = requests.get(url)
        print_response(response)
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def test_get_folder_permissions():
    """Test get folder permissions endpoint"""
    print_header("Test 2: Get Folder Permissions")

    url = f"{BASE_URL}/api/folder-file-data/folders/{FOLDER_ID}/permissions"
    params = {"project_id": PROJECT_ID}

    print(f"GET {url}")
    print(f"Params: {params}")

    try:
        response = requests.get(url, params=params)
        print_response(response)
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def test_get_folder_custom_attribute_definitions():
    """Test get folder custom attribute definitions endpoint"""
    print_header("Test 3: Get Folder Custom Attribute Definitions")

    url = f"{BASE_URL}/api/folder-file-data/folders/{FOLDER_ID}/custom-attribute-definitions"
    params = {"project_id": PROJECT_ID}

    print(f"GET {url}")
    print(f"Params: {params}")

    try:
        response = requests.get(url, params=params)
        print_response(response)
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def test_get_file_custom_attributes():
    """Test get file custom attributes endpoint"""
    print_header("Test 4: Get File Custom Attributes")

    # First, get a file ID from the database
    import psycopg2
    import sys
    import os

    # Add project root to path
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    from database_sql.neon_config import NeonConfig

    try:
        neon_config = NeonConfig()
        db_params = neon_config.get_db_params()
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        cur.execute("""
            SELECT id, name
            FROM files
            WHERE project_id = %s
              AND parent_folder_id = %s
            LIMIT 1
        """, (PROJECT_ID, FOLDER_ID))

        result = cur.fetchone()
        cur.close()
        conn.close()

        if not result:
            print("No files found in the folder. Skipping this test.")
            return True

        file_id, file_name = result
        print(f"Testing with file: {file_name} (ID: {file_id})")

        url = f"{BASE_URL}/api/folder-file-data/files/{file_id}/custom-attributes"
        params = {"project_id": PROJECT_ID}

        print(f"GET {url}")
        print(f"Params: {params}")

        response = requests.get(url, params=params)
        print_response(response)

        # Store file_id for next test
        global FILE_ID
        FILE_ID = file_id

        return response.status_code == 200

    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def test_get_file_versions():
    """Test get file versions endpoint"""
    print_header("Test 5: Get File Versions")

    if not FILE_ID:
        print("No file ID available. Skipping this test.")
        return True

    url = f"{BASE_URL}/api/folder-file-data/files/{FILE_ID}/versions"
    params = {"project_id": PROJECT_ID}

    print(f"GET {url}")
    print(f"Params: {params}")

    try:
        response = requests.get(url, params=params)
        print_response(response)
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def test_get_file_versions_current_only():
    """Test get file versions endpoint with current_only parameter"""
    print_header("Test 6: Get File Versions (Current Only)")

    if not FILE_ID:
        print("No file ID available. Skipping this test.")
        return True

    url = f"{BASE_URL}/api/folder-file-data/files/{FILE_ID}/versions"
    params = {
        "project_id": PROJECT_ID,
        "current_only": "true"
    }

    print(f"GET {url}")
    print(f"Params: {params}")

    try:
        response = requests.get(url, params=params)
        print_response(response)
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("  Folder File Data API Test Suite")
    print("=" * 70)
    print(f"Base URL: {BASE_URL}")
    print(f"Project ID: {PROJECT_ID}")
    print(f"Folder ID: {FOLDER_ID}")

    tests = [
        ("Health Check", test_health_check),
        ("Get Folder Permissions", test_get_folder_permissions),
        ("Get Folder Custom Attribute Definitions", test_get_folder_custom_attribute_definitions),
        ("Get File Custom Attributes", test_get_file_custom_attributes),
        ("Get File Versions", test_get_file_versions),
        ("Get File Versions (Current Only)", test_get_file_versions_current_only)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\nUnexpected error in {test_name}: {str(e)}")
            results.append((test_name, False))

    # Print summary
    print_header("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n✓ All tests passed!")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
