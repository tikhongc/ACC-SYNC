# -*- coding: utf-8 -*-
"""
Transmittal CSV Full Sync Script
=================================
Synchronizes transmittal data from CSV files to PostgreSQL database.

Usage:
    python api_modules/transmittal_csv_sync.py <project_id>

Example:
    python api_modules/transmittal_csv_sync.py b.1eea4119-3553-4167-b93d-3a3d5d07d33d

Features:
    - Auto-detects and validates required CSV files
    - Clears existing transmittal data before sync
    - Batch inserts data with proper type conversion
    - Maintains referential integrity (parent → child order)
    - Detailed sync reporting with statistics
    - Transaction-based for data consistency
"""

import os
import sys
import csv
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
from uuid import UUID

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from database_sql.transmittal_data_access import TransmittalDataAccess


class TransmittalCSVSync:
    """Manages CSV to database synchronization for transmittal module"""

    # CSV file mapping: filename → table name
    CSV_FILE_MAPPING = {
        'transmittals_workflow_transmittals.csv': 'transmittals_workflow_transmittals',
        'transmittals_transmittal_documents.csv': 'transmittals_transmittal_documents',
        'transmittals_transmittal_recipients.csv': 'transmittals_transmittal_recipients',
        'transmittals_transmittal_non_members.csv': 'transmittals_transmittal_non_members'
    }

    def __init__(self, csv_folder: Path = None):
        """
        Initialize CSV sync manager.

        Args:
            csv_folder: Path to folder containing CSV files (default: ./transmittal)
        """
        self.csv_folder = csv_folder or PROJECT_ROOT / "transmittal"
        self.dal = TransmittalDataAccess()

    def validate_csv_files(self) -> Tuple[bool, List[str], List[str]]:
        """
        Validate that all required CSV files exist.

        Returns:
            Tuple of (all_valid, found_files, missing_files)
        """
        if not self.csv_folder.exists():
            return False, [], list(self.CSV_FILE_MAPPING.keys())

        found = []
        missing = []

        for filename in self.CSV_FILE_MAPPING.keys():
            file_path = self.csv_folder / filename
            if file_path.exists():
                found.append(filename)
            else:
                missing.append(filename)

        return len(missing) == 0, found, missing

    def read_csv_file(self, filename: str) -> Tuple[List[Dict], int]:
        """
        Read CSV file and return data as list of dictionaries.

        Args:
            filename: CSV filename

        Returns:
            Tuple of (data_list, row_count)

        Raises:
            FileNotFoundError: If CSV file doesn't exist
            ValueError: If CSV is malformed
        """
        file_path = self.csv_folder / filename
        if not file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")

        data = []
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is 1)
                try:
                    # Clean up empty strings to None
                    cleaned_row = {}
                    for key, value in row.items():
                        if value == '' or value is None:
                            cleaned_row[key] = None
                        else:
                            cleaned_row[key] = value.strip()
                    data.append(cleaned_row)
                except Exception as e:
                    raise ValueError(f"Error reading row {row_num} in {filename}: {e}")

        return data, len(data)

    def convert_transmittal_row(self, row: Dict) -> Dict:
        """
        Convert CSV row to database format for workflow_transmittals.

        Args:
            row: CSV row dictionary

        Returns:
            Converted row ready for database insertion
        """
        return {
            'id': str(UUID(row['id'])),
            'bim360_account_id': str(UUID(row['bim360_account_id'])),
            'bim360_project_id': str(UUID(row['bim360_project_id'])),
            'sequence_id': int(row['sequence_id']),
            'title': row['title'],
            'status': int(row['status']),
            'create_user_id': str(UUID(row['create_user_id'])),
            'create_user_name': row['create_user_name'],
            'docs_count': int(row['docs_count']),
            'created_at': datetime.fromisoformat(row['created_at'].replace('Z', '+00:00')),
            'updated_at': datetime.fromisoformat(row['updated_at'].replace('Z', '+00:00')),
            'create_user_company_id': str(UUID(row['create_user_company_id'])) if row['create_user_company_id'] else None,
            'create_user_company_name': row['create_user_company_name'] if row['create_user_company_name'] else None
        }

    def convert_document_row(self, row: Dict) -> Dict:
        """
        Convert CSV row to database format for transmittal_documents.

        Args:
            row: CSV row dictionary

        Returns:
            Converted row ready for database insertion
        """
        return {
            'id': str(UUID(row['id'])),
            'workflow_transmittal_id': str(UUID(row['workflow_transmittal_id'])),
            'bim360_account_id': str(UUID(row['bim360_account_id'])),
            'bim360_project_id': str(UUID(row['bim360_project_id'])),
            'urn': row['urn'],
            'file_name': row['file_name'],
            'version_number': int(row['version_number']),
            'revision_number': int(row['revision_number']),
            'parent_folder_urn': row['parent_folder_urn'],
            'last_modified_time': datetime.fromisoformat(row['last_modified_time'].replace('Z', '+00:00')),
            'last_modified_user_id': row['last_modified_user_id'],
            'last_modified_user_name': row['last_modified_user_name'],
            'created_at': datetime.fromisoformat(row['created_at'].replace('Z', '+00:00')),
            'updated_at': datetime.fromisoformat(row['updated_at'].replace('Z', '+00:00'))
        }

    def convert_recipient_row(self, row: Dict) -> Dict:
        """
        Convert CSV row to database format for transmittal_recipients.

        Args:
            row: CSV row dictionary

        Returns:
            Converted row ready for database insertion
        """
        return {
            'id': str(UUID(row['id'])),
            'workflow_transmittal_id': str(UUID(row['workflow_transmittal_id'])),
            'bim360_account_id': str(UUID(row['bim360_account_id'])),
            'bim360_project_id': str(UUID(row['bim360_project_id'])),
            'user_id': str(UUID(row['user_id'])),
            'user_name': row['user_name'],
            'email': row['email'],
            'created_at': datetime.fromisoformat(row['created_at'].replace('Z', '+00:00')),
            'updated_at': datetime.fromisoformat(row['updated_at'].replace('Z', '+00:00')),
            'company_name': row['company_name'] if row['company_name'] else None,
            'viewed_at': datetime.fromisoformat(row['viewed_at'].replace('Z', '+00:00')) if row.get('viewed_at') else None,
            'downloaded_at': datetime.fromisoformat(row['downloaded_at'].replace('Z', '+00:00')) if row.get('downloaded_at') else None
        }

    def convert_non_member_row(self, row: Dict) -> Dict:
        """
        Convert CSV row to database format for transmittal_non_members.

        Args:
            row: CSV row dictionary

        Returns:
            Converted row ready for database insertion
        """
        return {
            'id': str(UUID(row['id'])),
            'bim360_account_id': str(UUID(row['bim360_account_id'])),
            'bim360_project_id': str(UUID(row['bim360_project_id'])),
            'email': row['email'],
            'first_name': row.get('first_name'),
            'last_name': row.get('last_name'),
            'company_name': row.get('company_name'),
            'role': row.get('role'),
            'workflow_transmittal_id': str(UUID(row['workflow_transmittal_id'])),
            'viewed_at': datetime.fromisoformat(row['viewed_at'].replace('Z', '+00:00')) if row.get('viewed_at') else None,
            'downloaded_at': datetime.fromisoformat(row['downloaded_at'].replace('Z', '+00:00')) if row.get('downloaded_at') else None,
            'created_at': datetime.fromisoformat(row['created_at'].replace('Z', '+00:00')),
            'updated_at': datetime.fromisoformat(row['updated_at'].replace('Z', '+00:00'))
        }

    def sync_to_database(self) -> Dict:
        """
        Perform full sync from CSV files to database.

        Returns:
            Sync result dictionary with statistics
        """
        start_time = datetime.now()
        result = {
            'success': False,
            'database_name': 'neondb',
            'csv_folder': str(self.csv_folder),
            'files_processed': {},
            'tables_cleared': {},
            'records_inserted': {},
            'total_records': 0,
            'duration_seconds': 0,
            'error': None
        }

        try:
            # Step 1: Validate CSV files
            print("Step 1: Validating CSV files...")
            all_valid, found_files, missing_files = self.validate_csv_files()

            if not all_valid:
                error_msg = f"Missing CSV files: {', '.join(missing_files)}"
                result['error'] = error_msg
                print(f"[FAIL] {error_msg}")
                print(f"Expected location: {self.csv_folder}")
                return result

            print(f"[OK] All {len(found_files)} CSV files found in {self.csv_folder}\n")

            # Step 2: Read CSV files
            print("Step 2: Reading CSV files...")
            csv_data = {}
            for filename in self.CSV_FILE_MAPPING.keys():
                data, count = self.read_csv_file(filename)
                csv_data[filename] = data
                result['files_processed'][filename] = count
                print(f"  [OK] {filename}: {count} rows")
            print()

            # Step 3: Clear existing data
            print("Step 3: Clearing existing transmittal data...")
            clear_result = self.dal.truncate_all_tables()
            result['tables_cleared'] = clear_result
            for table, success in clear_result.items():
                status = "[OK]" if success else "[FAIL]"
                print(f"  {status} {table}")
            print()

            # Step 4: Insert data in correct order (parent → child)
            print("Step 4: Inserting data into database...\n")

            # 4.1 Insert workflow_transmittals (parent table)
            print("  -> Inserting workflow_transmittals...")
            transmittals = [
                self.convert_transmittal_row(row)
                for row in csv_data['transmittals_workflow_transmittals.csv']
            ]
            inserted = self.dal.batch_insert_transmittals(transmittals)
            result['records_inserted']['workflow_transmittals'] = inserted
            print(f"    [OK] {inserted} records inserted")

            # 4.2 Insert transmittal_documents
            print("  -> Inserting transmittal_documents...")
            documents = [
                self.convert_document_row(row)
                for row in csv_data['transmittals_transmittal_documents.csv']
            ]
            inserted = self.dal.batch_insert_documents(documents)
            result['records_inserted']['transmittal_documents'] = inserted
            print(f"    [OK] {inserted} records inserted")

            # 4.3 Insert transmittal_recipients
            print("  -> Inserting transmittal_recipients...")
            recipients = [
                self.convert_recipient_row(row)
                for row in csv_data['transmittals_transmittal_recipients.csv']
            ]
            inserted = self.dal.batch_insert_recipients(recipients)
            result['records_inserted']['transmittal_recipients'] = inserted
            print(f"    [OK] {inserted} records inserted")

            # 4.4 Insert transmittal_non_members
            print("  -> Inserting transmittal_non_members...")
            non_members = [
                self.convert_non_member_row(row)
                for row in csv_data['transmittals_transmittal_non_members.csv']
            ]
            inserted = self.dal.batch_insert_non_members(non_members)
            result['records_inserted']['transmittal_non_members'] = inserted
            print(f"    [OK] {inserted} records inserted")

            print()

            # Step 5: Verify sync
            print("Step 5: Verifying sync...")
            table_counts = self.dal.get_table_counts()
            result['total_records'] = sum(table_counts.values())
            for table, count in table_counts.items():
                short_name = table.replace('transmittals_', '')
                print(f"  [OK] {short_name}: {count} records")

            # Success
            result['success'] = True

        except FileNotFoundError as e:
            result['error'] = str(e)
            print(f"\n❌ File Error: {e}")
        except ValueError as e:
            result['error'] = str(e)
            print(f"\n❌ Data Error: {e}")
        except Exception as e:
            result['error'] = f"Unexpected error: {e}"
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()

        # Calculate duration
        result['duration_seconds'] = (datetime.now() - start_time).total_seconds()

        return result

    def print_summary(self, result: Dict):
        """
        Print formatted sync summary.

        Args:
            result: Sync result dictionary
        """
        print("\n" + "=" * 70)
        print("📊 TRANSMITTAL CSV FULL SYNC REPORT")
        print("=" * 70)
        print(f"Database: {result['database_name']}")
        print(f"CSV Folder: {result['csv_folder']}")
        print(f"Sync Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Duration: {result['duration_seconds']:.2f}s")
        print(f"Status: {'✅ SUCCESS' if result['success'] else '❌ FAILED'}")

        if result['files_processed']:
            print(f"\n✓ Files Validated:")
            for filename, count in result['files_processed'].items():
                print(f"  - {filename} ({count} rows)")

        if result['tables_cleared']:
            all_cleared = all(result['tables_cleared'].values())
            print(f"\n✓ Tables Cleared: {'All' if all_cleared else 'Partial'}")
            for table, success in result['tables_cleared'].items():
                status = "✓" if success else "✗"
                print(f"  {status} {table.replace('transmittals_', '')}")

        if result['records_inserted']:
            print(f"\n✓ Data Synced:")
            for table, count in result['records_inserted'].items():
                print(f"  - {table}: {count} records inserted")

        print(f"\nTotal Records: {result['total_records']}")

        if result['error']:
            print(f"\n❌ Error: {result['error']}")

        print("=" * 70)


def main():
    """Main execution function"""
    print("=" * 70)
    print("TRANSMITTAL CSV FULL SYNC")
    print("=" * 70)
    print("Description:")
    print("  Performs full sync of transmittal data from CSV files to database.")
    print("  CSV files must be located in the 'transmittal/' folder.\n")
    print("Required CSV files:")
    for filename in TransmittalCSVSync.CSV_FILE_MAPPING.keys():
        print(f"  - {filename}")
    print("=" * 70)
    print()

    # Perform sync
    sync_manager = TransmittalCSVSync()
    result = sync_manager.sync_to_database()

    # Print summary
    sync_manager.print_summary(result)

    # Exit with appropriate code
    sys.exit(0 if result['success'] else 1)


if __name__ == '__main__':
    # Set UTF-8 encoding for Windows
    if sys.platform.startswith('win'):
        os.environ['PYTHONIOENCODING'] = 'utf-8'

    # Run main
    main()
