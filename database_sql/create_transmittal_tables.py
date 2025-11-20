# -*- coding: utf-8 -*-
"""
Transmittal Tables Creation Script
==================================
Creates transmittal module tables in the Neon PostgreSQL database.

Usage:
    python database_sql/create_transmittal_tables.py

Features:
    - Reads SQL schema from transmittal_schema.sql
    - Creates tables in Neon PostgreSQL database
    - Handles existing tables (IF NOT EXISTS)
    - Creates indexes and constraints
    - Creates helper views
    - Provides detailed status reporting
"""

import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor
from pathlib import Path
from datetime import datetime

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from database_sql.transmittal_data_access import get_connection


class TransmittalTableCreator:
    """Manages creation of transmittal module tables"""

    def __init__(self):
        self.schema_file = PROJECT_ROOT / "database_sql" / "transmittal_schema.sql"

    def read_schema_sql(self) -> str:
        """
        Read the transmittal schema SQL file.

        Returns:
            str: SQL content from schema file

        Raises:
            FileNotFoundError: If schema file doesn't exist
        """
        if not self.schema_file.exists():
            raise FileNotFoundError(
                f"Schema file not found: {self.schema_file}\n"
                f"Expected location: database_sql/transmittal_schema.sql"
            )

        with open(self.schema_file, 'r', encoding='utf-8') as f:
            return f.read()

    def table_exists(self, cursor, table_name: str) -> bool:
        """
        Check if a table exists in the database.

        Args:
            cursor: Database cursor
            table_name: Name of the table to check

        Returns:
            bool: True if table exists, False otherwise
        """
        query = """
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = %s
            )
        """
        cursor.execute(query, (table_name,))
        return cursor.fetchone()[0]

    def get_table_info(self, cursor, table_name: str) -> dict:
        """
        Get information about a table (row count, etc).

        Args:
            cursor: Database cursor
            table_name: Name of the table

        Returns:
            dict: Table information
        """
        # Get row count
        count_query = f"SELECT COUNT(*) FROM {table_name}"
        cursor.execute(count_query)
        row_count = cursor.fetchone()[0]

        # Get column count
        column_query = """
            SELECT COUNT(*)
            FROM information_schema.columns
            WHERE table_schema = 'public'
            AND table_name = %s
        """
        cursor.execute(column_query, (table_name,))
        column_count = cursor.fetchone()[0]

        return {
            'table_name': table_name,
            'row_count': row_count,
            'column_count': column_count
        }

    def create_tables(self, drop_existing: bool = False) -> dict:
        """
        Create transmittal tables in the database.

        Args:
            drop_existing: If True, drop existing tables before creating

        Returns:
            dict: Creation result with status and details
        """
        start_time = datetime.now()
        result = {
            'success': False,
            'database_name': 'neondb',
            'tables_created': [],
            'tables_existed': [],
            'views_created': [],
            'error': None,
            'duration_seconds': 0
        }

        try:
            # Read schema SQL
            print(f"Reading schema from: {self.schema_file}")
            schema_sql = self.read_schema_sql()
            print(f"[OK] Schema loaded ({len(schema_sql)} characters)\n")

            # Get database connection
            print(f"Connecting to Neon PostgreSQL database...")
            conn = get_connection()
            cursor = conn.cursor()
            result['database_name'] = conn.info.dbname
            print(f"[OK] Connected to: {result['database_name']}\n")

            # Check existing tables
            print("Checking existing tables...")
            tables_to_check = [
                'transmittals_workflow_transmittals',
                'transmittals_transmittal_documents',
                'transmittals_transmittal_recipients',
                'transmittals_transmittal_non_members'
            ]

            existing_tables = []
            for table in tables_to_check:
                exists = self.table_exists(cursor, table)
                if exists:
                    existing_tables.append(table)
                    print(f"  [WARNING] {table} already exists")
                else:
                    print(f"  [ ] {table} not found")

            # Drop existing tables if requested
            if drop_existing and existing_tables:
                print(f"\nDropping {len(existing_tables)} existing tables...")
                for table in existing_tables:
                    cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
                    print(f"  [OK] Dropped: {table}")
                conn.commit()
                existing_tables = []

            # Execute schema SQL
            print("\nCreating tables...")
            cursor.execute(schema_sql)
            conn.commit()

            # Verify created tables
            print("\n[OK] Verifying created tables...")
            for table in tables_to_check:
                exists = self.table_exists(cursor, table)
                if exists:
                    info = self.get_table_info(cursor, table)
                    print(f"  [OK] {table}")
                    print(f"    - Columns: {info['column_count']}")
                    print(f"    - Rows: {info['row_count']}")

                    if table in existing_tables:
                        result['tables_existed'].append(table)
                    else:
                        result['tables_created'].append(table)
                else:
                    print(f"  [FAIL] {table} - NOT CREATED!")

            # Check views
            print("\nVerifying created views...")
            view_query = """
                SELECT table_name
                FROM information_schema.views
                WHERE table_schema = 'public'
                AND table_name LIKE 'v_%transmittal%'
                ORDER BY table_name
            """
            cursor.execute(view_query)
            views = cursor.fetchall()
            for view_row in views:
                view_name = view_row[0]
                result['views_created'].append(view_name)
                print(f"  [OK] {view_name}")

            # Success
            result['success'] = True

            cursor.close()
            conn.close()

        except FileNotFoundError as e:
            result['error'] = str(e)
            print(f"\n[FAIL] Error: {e}")
        except psycopg2.Error as e:
            result['error'] = f"Database error: {e}"
            print(f"\n[FAIL] Database Error: {e}")
        except Exception as e:
            result['error'] = f"Unexpected error: {e}"
            print(f"\n[FAIL] Unexpected Error: {e}")
            import traceback
            traceback.print_exc()

        # Calculate duration
        result['duration_seconds'] = (datetime.now() - start_time).total_seconds()

        return result

    def print_summary(self, result: dict):
        """
        Print a formatted summary of the creation result.

        Args:
            result: Result dictionary from create_tables
        """
        print("\n" + "=" * 60)
        print("TRANSMITTAL TABLES CREATION SUMMARY")
        print("=" * 60)
        print(f"Database: {result['database_name']}")
        print(f"Duration: {result['duration_seconds']:.2f}s")
        print(f"Status: {'[OK] SUCCESS' if result['success'] else '[FAIL] FAILED'}")

        if result['tables_created']:
            print(f"\n[NEW] Tables Created ({len(result['tables_created'])}):")
            for table in result['tables_created']:
                print(f"  - {table}")

        if result['tables_existed']:
            print(f"\n[EXISTS] Tables Already Existed ({len(result['tables_existed'])}):")
            for table in result['tables_existed']:
                print(f"  - {table}")

        if result['views_created']:
            print(f"\n[VIEWS] Views Created ({len(result['views_created'])}):")
            for view in result['views_created']:
                print(f"  - {view}")

        if result['error']:
            print(f"\n[FAIL] Error: {result['error']}")

        print("=" * 60)


def main():
    """Main execution function"""
    # Check command line arguments
    drop_existing = '--drop' in sys.argv

    if drop_existing:
        print("WARNING: --drop flag detected. Existing tables will be dropped!")
        print("Press Ctrl+C within 3 seconds to cancel...\n")
        import time
        time.sleep(3)

    print("=" * 60)
    print("TRANSMITTAL MODULE - TABLE CREATION")
    print("=" * 60)
    print(f"Target: Neon PostgreSQL Cloud Database")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    # Create tables
    creator = TransmittalTableCreator()
    result = creator.create_tables(drop_existing=drop_existing)

    # Print summary
    creator.print_summary(result)

    # Exit with appropriate code
    sys.exit(0 if result['success'] else 1)


if __name__ == '__main__':
    # Set UTF-8 encoding for Windows
    if sys.platform.startswith('win'):
        os.environ['PYTHONIOENCODING'] = 'utf-8'

    # Run main
    main()
