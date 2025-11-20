# -*- coding: utf-8 -*-
"""
Transmittal Module Test Script
===============================
Comprehensive test script for transmittal module functionality.

Usage:
    python test_transmittal_sync.py

Test Coverage:
    1. Database connection test
    2. Table structure verification
    3. CSV file validation
    4. Full sync operation test
    5. Data integrity verification
    6. Query functionality test
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from database_sql.transmittal_data_access import TransmittalDataAccess, get_connection
from api_modules.transmittal_csv_sync import TransmittalCSVSync


class TransmittalModuleTest:
    """Comprehensive test suite for transmittal module"""

    def __init__(self):
        self.dal = TransmittalDataAccess()
        self.sync_manager = TransmittalCSVSync()
        self.test_results = []

    def log_test(self, test_name: str, passed: bool, details: str = ""):
        """Log a test result"""
        status = "[PASS]" if passed else "[FAIL]"
        self.test_results.append({
            'test_name': test_name,
            'passed': passed,
            'details': details
        })
        print(f"{status} - {test_name}")
        if details:
            print(f"    {details}")

    def test_database_connection(self) -> bool:
        """Test 1: Database connection"""
        print("\nTest 1: Database Connection")
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0]
            pg_version = version.split(',')[0]

            cursor.execute("SELECT current_database()")
            db_name = cursor.fetchone()[0]

            cursor.close()
            conn.close()

            self.log_test(
                "Database Connection",
                True,
                f"Connected to {db_name} ({pg_version})"
            )
            return True
        except Exception as e:
            self.log_test("Database Connection", False, str(e))
            return False

    def test_table_structure(self) -> bool:
        """Test 2: Table structure verification"""
        print("\nTest 2: Table Structure Verification")
        try:
            conn = get_connection()
            cursor = conn.cursor()

            required_tables = [
                'transmittals_workflow_transmittals',
                'transmittals_transmittal_documents',
                'transmittals_transmittal_recipients',
                'transmittals_transmittal_non_members'
            ]

            all_exist = True
            missing_tables = []

            for table in required_tables:
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables
                        WHERE table_schema = 'public'
                        AND table_name = %s
                    )
                """, (table,))

                exists = cursor.fetchone()[0]

                if not exists:
                    all_exist = False
                    missing_tables.append(table)

            cursor.close()
            conn.close()

            if all_exist:
                self.log_test(
                    "Table Structure",
                    True,
                    f"All {len(required_tables)} tables exist"
                )
            else:
                self.log_test(
                    "Table Structure",
                    False,
                    f"Missing tables: {', '.join(missing_tables)}"
                )

            return all_exist

        except Exception as e:
            self.log_test("Table Structure", False, str(e))
            return False

    def test_csv_validation(self) -> bool:
        """Test 3: CSV file validation"""
        print("\nTest 3: CSV File Validation")
        try:
            all_valid, found_files, missing_files = self.sync_manager.validate_csv_files()

            if all_valid:
                self.log_test(
                    "CSV File Validation",
                    True,
                    f"All {len(found_files)} CSV files found"
                )
            else:
                self.log_test(
                    "CSV File Validation",
                    False,
                    f"Missing files: {', '.join(missing_files)}"
                )

            return all_valid

        except Exception as e:
            self.log_test("CSV File Validation", False, str(e))
            return False

    def test_full_sync(self) -> bool:
        """Test 4: Full sync operation"""
        print("\nTest 4: Full Sync Operation")
        try:
            result = self.sync_manager.sync_to_database()

            if result['success']:
                details = f"{result['total_records']} records synced in {result['duration_seconds']:.2f}s"
                self.log_test("Full Sync Operation", True, details)
            else:
                self.log_test("Full Sync Operation", False, result.get('error', 'Unknown error'))

            return result['success']

        except Exception as e:
            self.log_test("Full Sync Operation", False, str(e))
            return False

    def test_data_integrity(self) -> bool:
        """Test 5: Data integrity verification"""
        print("\nTest 5: Data Integrity Verification")
        try:
            # Get table counts
            counts = self.dal.get_table_counts()

            # Verify parent-child relationships
            conn = get_connection()
            cursor = conn.cursor()

            # Check foreign key integrity
            cursor.execute("""
                SELECT COUNT(*) FROM transmittals_transmittal_documents d
                WHERE NOT EXISTS (
                    SELECT 1 FROM transmittals_workflow_transmittals t
                    WHERE t.id = d.workflow_transmittal_id
                )
            """)
            orphaned_docs = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*) FROM transmittals_transmittal_recipients r
                WHERE NOT EXISTS (
                    SELECT 1 FROM transmittals_workflow_transmittals t
                    WHERE t.id = r.workflow_transmittal_id
                )
            """)
            orphaned_recipients = cursor.fetchone()[0]

            cursor.execute("""
                SELECT COUNT(*) FROM transmittals_transmittal_non_members n
                WHERE NOT EXISTS (
                    SELECT 1 FROM transmittals_workflow_transmittals t
                    WHERE t.id = n.workflow_transmittal_id
                )
            """)
            orphaned_non_members = cursor.fetchone()[0]

            cursor.close()
            conn.close()

            total_orphaned = orphaned_docs + orphaned_recipients + orphaned_non_members

            if total_orphaned == 0:
                details = f"All relationships valid. Tables: {counts}"
                self.log_test("Data Integrity", True, details)
                return True
            else:
                details = f"Found {total_orphaned} orphaned records"
                self.log_test("Data Integrity", False, details)
                return False

        except Exception as e:
            self.log_test("Data Integrity", False, str(e))
            return False

    def test_query_functionality(self) -> bool:
        """Test 6: Query functionality"""
        print("\nTest 6: Query Functionality")
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Get first transmittal
            cursor.execute("""
                SELECT * FROM transmittals_workflow_transmittals
                ORDER BY sequence_id
                LIMIT 1
            """)

            first_transmittal = cursor.fetchone()

            if not first_transmittal:
                cursor.close()
                conn.close()
                self.log_test("Query Functionality", False, "No transmittals found")
                return False

            transmittal_id = first_transmittal[0]  # id is first column

            cursor.close()
            conn.close()

            # Test various queries
            tests_passed = []

            # Test 1: Get transmittal by ID
            transmittal = self.dal.get_transmittal_by_id(transmittal_id)
            tests_passed.append(transmittal is not None)

            # Test 2: Get documents
            documents = self.dal.get_documents_by_transmittal(transmittal_id)
            tests_passed.append(isinstance(documents, list))

            # Test 3: Get recipients
            recipients = self.dal.get_recipients_by_transmittal(transmittal_id)
            tests_passed.append(isinstance(recipients, list))

            # Test 4: Get table counts
            counts = self.dal.get_table_counts()
            tests_passed.append(len(counts) == 4)

            all_passed = all(tests_passed)
            details = f"Passed {sum(tests_passed)}/{len(tests_passed)} query tests"

            self.log_test("Query Functionality", all_passed, details)
            return all_passed

        except Exception as e:
            self.log_test("Query Functionality", False, str(e))
            return False

    def test_views(self) -> bool:
        """Test 7: Database views"""
        print("\nTest 7: Database Views")
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Test v_transmittal_summary view
            cursor.execute("SELECT COUNT(*) FROM v_transmittal_summary")
            summary_count = cursor.fetchone()[0]

            # Test v_recipient_engagement view
            cursor.execute("SELECT COUNT(*) FROM v_recipient_engagement")
            engagement_count = cursor.fetchone()[0]

            cursor.close()
            conn.close()

            details = f"Summary view: {summary_count} rows, Engagement view: {engagement_count} rows"
            self.log_test("Database Views", True, details)
            return True

        except Exception as e:
            self.log_test("Database Views", False, str(e))
            return False

    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)

        total_tests = len(self.test_results)
        passed_tests = sum(1 for t in self.test_results if t['passed'])
        failed_tests = total_tests - passed_tests

        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} [PASS]")
        print(f"Failed: {failed_tests} [FAIL]")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")

        if failed_tests > 0:
            print("\n[FAIL] Failed Tests:")
            for result in self.test_results:
                if not result['passed']:
                    print(f"  - {result['test_name']}")
                    if result['details']:
                        print(f"      {result['details']}")

        print("=" * 70)

        return failed_tests == 0

    def run_all_tests(self) -> bool:
        """Run all tests"""
        print("=" * 70)
        print("TRANSMITTAL MODULE TEST SUITE")
        print("=" * 70)
        print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)

        # Run tests in order
        self.test_database_connection()
        self.test_table_structure()
        self.test_csv_validation()
        self.test_full_sync()
        self.test_data_integrity()
        self.test_query_functionality()
        self.test_views()

        # Print summary
        all_passed = self.print_summary()

        return all_passed


def main():
    """Main execution function"""
    print("Description:")
    print("  Runs comprehensive tests for the transmittal module.")
    print("  Tests include database connection, table structure, CSV validation,")
    print("  full sync operation, data integrity, and query functionality.\n")

    # Run tests
    test_suite = TransmittalModuleTest()
    all_passed = test_suite.run_all_tests()

    # Exit with appropriate code
    sys.exit(0 if all_passed else 1)


if __name__ == '__main__':
    # Set UTF-8 encoding for Windows
    if sys.platform.startswith('win'):
        os.environ['PYTHONIOENCODING'] = 'utf-8'

    # Run main
    main()
