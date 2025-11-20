# -*- coding: utf-8 -*-
"""
Test Script for Transmittal Create APIs

Tests the following endpoints:
1. POST /api/transmittals/create - Create a new transmittal
2. POST /api/transmittals/<id>/documents - Add documents to transmittal
3. POST /api/transmittals/<id>/recipients - Add recipients to transmittal

Usage:
    python test_transmittal_create.py

Requirements:
    - Flask server running on localhost:8080
    - Database connection configured
"""

import requests
import json
import uuid
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8080"
PROJECT_ID = "1eea4119-3553-4167-b93d-3a3d5d07d33d"  # Without b. prefix

# Test data
TEST_TRANSMITTAL = {
    "project_id": PROJECT_ID,
    "title": "Test Transmittal - " + datetime.now().strftime("%Y%m%d_%H%M%S"),
    "message": "This is a test transmittal created by automated test script.",
    "created_by_user_id": None,
    "created_by_user_name": "Test User",
    "created_by_company_id": None,
    "created_by_company_name": "Test Company"
}

TEST_DOCUMENTS = [
    {
        "urn": "test-urn-001",
        "file_name": "Document_A.pdf",
        "version_number": 1
    },
    {
        "urn": "test-urn-002",
        "file_name": "Document_B.dwg",
        "version_number": 2
    },
    {
        "urn": "test-urn-003",
        "file_name": "Document_C.xlsx",
        "version_number": 1
    }
]

TEST_RECIPIENTS = [
    {
        "user_id": str(uuid.uuid4()),
        "user_name": "John Doe",
        "email": "john.doe@example.com",
        "company_name": "Company A"
    },
    {
        "user_id": str(uuid.uuid4()),
        "user_name": "Jane Smith",
        "email": "jane.smith@example.com",
        "company_name": "Company B"
    },
    {
        "user_id": str(uuid.uuid4()),
        "user_name": "Bob Wilson",
        "email": "bob.wilson@example.com",
        "company_name": "Company A"
    },
    # Duplicate email to test deduplication
    {
        "user_id": str(uuid.uuid4()),
        "user_name": "John Doe Duplicate",
        "email": "john.doe@example.com",  # Same email as first recipient
        "company_name": "Company C"
    }
]


def print_separator(title):
    """Print a separator line with title"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def print_response(response, show_body=True):
    """Print response details"""
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    if show_body:
        try:
            print(f"Response Body: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Response Body: {response.text}")


def test_create_transmittal():
    """
    Test 1: POST /api/transmittals/create

    Expected:
    - Returns 201 status code
    - Returns success: true
    - Returns transmittal_id (UUID)
    - Returns sequence_id (auto-incremented)
    """
    print_separator("TEST 1: Create Transmittal")

    url = f"{BASE_URL}/api/transmittals/create"
    print(f"URL: {url}")
    print(f"Method: POST")
    print(f"Request Body: {json.dumps(TEST_TRANSMITTAL, indent=2)}")

    try:
        response = requests.post(
            url,
            json=TEST_TRANSMITTAL,
            headers={"Content-Type": "application/json"}
        )

        print("\n--- Response ---")
        print_response(response)

        if response.status_code == 201:
            data = response.json()
            if data.get("success"):
                print("\n[PASS] Transmittal created successfully!")
                print(f"  - transmittal_id: {data.get('transmittal_id')}")
                print(f"  - sequence_id: {data.get('sequence_id')}")
                return data.get("transmittal_id")
            else:
                print(f"\n[FAIL] API returned success=false: {data.get('error')}")
        else:
            print(f"\n[FAIL] Unexpected status code: {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Could not connect to server. Is Flask running on port 8080?")
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")

    return None


def test_add_documents(transmittal_id):
    """
    Test 2: POST /api/transmittals/<id>/documents

    Expected:
    - Returns 201 status code
    - Returns success: true
    - Returns documents_added count
    - Updates docs_count in main transmittal
    """
    print_separator("TEST 2: Add Documents to Transmittal")

    if not transmittal_id:
        print("[SKIP] No transmittal_id provided")
        return False

    url = f"{BASE_URL}/api/transmittals/{transmittal_id}/documents"
    payload = {"documents": TEST_DOCUMENTS}

    print(f"URL: {url}")
    print(f"Method: POST")
    print(f"Transmittal ID: {transmittal_id}")
    print(f"Request Body: {json.dumps(payload, indent=2)}")

    try:
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        print("\n--- Response ---")
        print_response(response)

        if response.status_code == 201:
            data = response.json()
            if data.get("success"):
                print("\n[PASS] Documents added successfully!")
                print(f"  - documents_added: {data.get('documents_added')}")
                print(f"  - Expected: {len(TEST_DOCUMENTS)}")

                if data.get('documents_added') == len(TEST_DOCUMENTS):
                    print("  - Count matches!")
                    return True
                else:
                    print("  - Count mismatch!")
            else:
                print(f"\n[FAIL] API returned success=false: {data.get('error')}")
        else:
            print(f"\n[FAIL] Unexpected status code: {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Could not connect to server.")
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")

    return False


def test_add_recipients(transmittal_id):
    """
    Test 3: POST /api/transmittals/<id>/recipients

    Expected:
    - Returns 201 status code
    - Returns success: true
    - Returns recipients_added count
    - Deduplicates by email (4 input -> 3 unique)
    """
    print_separator("TEST 3: Add Recipients to Transmittal")

    if not transmittal_id:
        print("[SKIP] No transmittal_id provided")
        return False

    url = f"{BASE_URL}/api/transmittals/{transmittal_id}/recipients"
    payload = {"recipients": TEST_RECIPIENTS}

    print(f"URL: {url}")
    print(f"Method: POST")
    print(f"Transmittal ID: {transmittal_id}")
    print(f"Request Body: {json.dumps(payload, indent=2)}")
    print(f"\nNote: Sending {len(TEST_RECIPIENTS)} recipients with 1 duplicate email")
    print("Expected recipients_added: 3 (after deduplication)")

    try:
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        print("\n--- Response ---")
        print_response(response)

        if response.status_code == 201:
            data = response.json()
            if data.get("success"):
                recipients_added = data.get('recipients_added')
                print("\n[PASS] Recipients added successfully!")
                print(f"  - recipients_added: {recipients_added}")

                # Check deduplication (4 sent, 3 expected due to duplicate email)
                expected = 3
                if recipients_added == expected:
                    print(f"  - Deduplication working correctly! (4 -> 3)")
                    return True
                else:
                    print(f"  - Warning: Expected {expected}, got {recipients_added}")
            else:
                print(f"\n[FAIL] API returned success=false: {data.get('error')}")
        else:
            print(f"\n[FAIL] Unexpected status code: {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Could not connect to server.")
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")

    return False


def test_get_transmittal_details(transmittal_id):
    """
    Verify the created transmittal by fetching its documents and recipients
    """
    print_separator("VERIFICATION: Fetch Created Transmittal Details")

    if not transmittal_id:
        print("[SKIP] No transmittal_id provided")
        return

    # Get documents
    print("\n--- Fetching Documents ---")
    try:
        url = f"{BASE_URL}/api/transmittals/{transmittal_id}/documents"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"Documents count: {data.get('count', 0)}")
            if data.get('data'):
                for doc in data['data']:
                    print(f"  - {doc.get('file_name')} (v{doc.get('version_number')})")
        else:
            print(f"Failed to fetch documents: {response.status_code}")
    except Exception as e:
        print(f"Error fetching documents: {e}")

    # Get recipients
    print("\n--- Fetching Recipients ---")
    try:
        url = f"{BASE_URL}/api/transmittals/{transmittal_id}/recipients"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"Total recipients: {data.get('total_count', 0)}")
            if data.get('data'):
                for recipient in data['data']:
                    print(f"  - {recipient.get('name')} ({recipient.get('email')})")
        else:
            print(f"Failed to fetch recipients: {response.status_code}")
    except Exception as e:
        print(f"Error fetching recipients: {e}")


def test_validation_errors():
    """
    Test validation error handling
    """
    print_separator("TEST 4: Validation Error Handling")

    # Test missing required field
    print("\n--- Test: Missing title ---")
    url = f"{BASE_URL}/api/transmittals/create"
    payload = {
        "project_id": PROJECT_ID
        # Missing title
    }

    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 400:
            print("[PASS] Correctly rejected request with missing title")
        else:
            print(f"[WARN] Expected 400, got {response.status_code}")
    except Exception as e:
        print(f"[ERROR] {e}")

    # Test missing project_id
    print("\n--- Test: Missing project_id ---")
    payload = {
        "title": "Test"
        # Missing project_id
    }

    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 400:
            print("[PASS] Correctly rejected request with missing project_id")
        else:
            print(f"[WARN] Expected 400, got {response.status_code}")
    except Exception as e:
        print(f"[ERROR] {e}")

    # Test empty documents array
    print("\n--- Test: Empty documents array ---")
    url = f"{BASE_URL}/api/transmittals/invalid-id/documents"
    payload = {"documents": []}

    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 400:
            print("[PASS] Correctly rejected empty documents array")
        else:
            print(f"[INFO] Status: {response.status_code}")
    except Exception as e:
        print(f"[ERROR] {e}")


def run_all_tests():
    """Run all tests in sequence"""
    print("\n")
    print("*" * 60)
    print(" TRANSMITTAL CREATE API TEST SUITE")
    print("*" * 60)
    print(f"\nServer: {BASE_URL}")
    print(f"Project ID: {PROJECT_ID}")
    print(f"Timestamp: {datetime.now().isoformat()}")

    # Test 1: Create transmittal
    transmittal_id = test_create_transmittal()

    # Test 2: Add documents
    docs_success = test_add_documents(transmittal_id)

    # Test 3: Add recipients
    recipients_success = test_add_recipients(transmittal_id)

    # Verification
    test_get_transmittal_details(transmittal_id)

    # Test 4: Validation errors
    test_validation_errors()

    # Summary
    print_separator("TEST SUMMARY")
    print(f"Transmittal ID: {transmittal_id or 'FAILED'}")
    print(f"Create Transmittal: {'PASS' if transmittal_id else 'FAIL'}")
    print(f"Add Documents: {'PASS' if docs_success else 'FAIL'}")
    print(f"Add Recipients: {'PASS' if recipients_success else 'FAIL'}")

    if transmittal_id and docs_success and recipients_success:
        print("\n[SUCCESS] All tests passed!")
        return 0
    else:
        print("\n[FAILURE] Some tests failed!")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(run_all_tests())
