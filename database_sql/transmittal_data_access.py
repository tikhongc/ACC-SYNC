# -*- coding: utf-8 -*-
"""
Transmittal Data Access Layer
==============================
Provides database access methods for transmittal module.

Features:
    - CRUD operations for all transmittal tables
    - Batch INSERT operations for efficient syncing
    - Uses psycopg2 for PostgreSQL connection (synchronous)
    - Transaction support for data integrity
    - Query helpers for common use cases
"""

import psycopg2
from psycopg2.extras import RealDictCursor, execute_batch
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from uuid import UUID
from contextlib import contextmanager


def get_connection(connection_params: Optional[Dict] = None):
    """
    Get database connection using psycopg2

    Args:
        connection_params: Optional connection parameters

    Returns:
        psycopg2 connection object
    """
    if connection_params:
        return psycopg2.connect(**connection_params)

    # Default connection using neon_config settings
    try:
        from database_sql.neon_config import NeonConfig
        config = NeonConfig()

        conn_params = config.get_db_params()
        return psycopg2.connect(**conn_params)
    except ImportError:
        # Fallback
        import os
        return psycopg2.connect(
            host=os.getenv('DB_HOST', 'ep-soft-mountain-a4jqpy5e-pooler.us-east-1.aws.neon.tech'),
            port=os.getenv('DB_PORT', 5432),
            database=os.getenv('DB_NAME', 'neondb'),
            user=os.getenv('DB_USER', 'neondb_owner'),
            password=os.getenv('DB_PASSWORD', 'npg_a2nxljG8LOSP'),
            sslmode='require'
        )


class TransmittalDataAccess:
    """Data access layer for transmittal module"""

    def __init__(self, connection_params: Optional[Dict] = None):
        """
        Initialize data access layer.

        Args:
            connection_params: Optional database connection parameters
        """
        self.connection_params = connection_params

    @contextmanager
    def get_cursor(self, cursor_factory=RealDictCursor):
        """Context manager for database cursor"""
        conn = get_connection(self.connection_params)
        cursor = conn.cursor(cursor_factory=cursor_factory)
        try:
            yield conn, cursor
        finally:
            cursor.close()
            conn.close()

    # ================================================================
    # Transmittal CRUD Operations
    # ================================================================

    def batch_insert_transmittals(self, transmittals: List[Dict]) -> int:
        """
        Batch insert workflow transmittals.

        Args:
            transmittals: List of transmittal dictionaries

        Returns:
            Number of records inserted
        """
        if not transmittals:
            return 0

        query = """
            INSERT INTO transmittals_workflow_transmittals (
                id, bim360_account_id, bim360_project_id, sequence_id,
                title, status, create_user_id, create_user_name,
                docs_count, created_at, updated_at,
                create_user_company_id, create_user_company_name
            ) VALUES (
                %(id)s, %(bim360_account_id)s, %(bim360_project_id)s, %(sequence_id)s,
                %(title)s, %(status)s, %(create_user_id)s, %(create_user_name)s,
                %(docs_count)s, %(created_at)s, %(updated_at)s,
                %(create_user_company_id)s, %(create_user_company_name)s
            )
            ON CONFLICT (id) DO UPDATE SET
                title = EXCLUDED.title,
                status = EXCLUDED.status,
                docs_count = EXCLUDED.docs_count,
                updated_at = EXCLUDED.updated_at
        """

        with self.get_cursor() as (conn, cursor):
            execute_batch(cursor, query, transmittals)
            conn.commit()
            return len(transmittals)

    def get_transmittal_by_id(self, transmittal_id: UUID) -> Optional[Dict]:
        """
        Get a transmittal by ID.

        Args:
            transmittal_id: Transmittal UUID

        Returns:
            Transmittal dictionary or None if not found
        """
        query = """
            SELECT * FROM transmittals_workflow_transmittals
            WHERE id = %s
        """
        with self.get_cursor() as (conn, cursor):
            cursor.execute(query, (transmittal_id,))
            return cursor.fetchone()

    def get_transmittals_by_project(
        self,
        project_id: UUID,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict]:
        """
        Get transmittals for a project.

        Args:
            project_id: Project UUID
            limit: Maximum number of results
            offset: Offset for pagination

        Returns:
            List of transmittal dictionaries
        """
        query = """
            SELECT * FROM transmittals_workflow_transmittals
            WHERE bim360_project_id = %s
            ORDER BY sequence_id DESC
            LIMIT %s OFFSET %s
        """
        with self.get_cursor() as (conn, cursor):
            cursor.execute(query, (project_id, limit, offset))
            return cursor.fetchall()

    # ================================================================
    # Document CRUD Operations
    # ================================================================

    def batch_insert_documents(self, documents: List[Dict]) -> int:
        """
        Batch insert transmittal documents.

        Args:
            documents: List of document dictionaries

        Returns:
            Number of records inserted
        """
        if not documents:
            return 0

        query = """
            INSERT INTO transmittals_transmittal_documents (
                id, workflow_transmittal_id, bim360_account_id, bim360_project_id,
                urn, file_name, version_number, revision_number,
                parent_folder_urn, last_modified_time,
                last_modified_user_id, last_modified_user_name,
                created_at, updated_at
            ) VALUES (
                %(id)s, %(workflow_transmittal_id)s, %(bim360_account_id)s, %(bim360_project_id)s,
                %(urn)s, %(file_name)s, %(version_number)s, %(revision_number)s,
                %(parent_folder_urn)s, %(last_modified_time)s,
                %(last_modified_user_id)s, %(last_modified_user_name)s,
                %(created_at)s, %(updated_at)s
            )
            ON CONFLICT (workflow_transmittal_id, urn, version_number) DO UPDATE SET
                file_name = EXCLUDED.file_name,
                updated_at = EXCLUDED.updated_at
        """

        with self.get_cursor() as (conn, cursor):
            execute_batch(cursor, query, documents)
            conn.commit()
            return len(documents)

    def get_documents_by_transmittal(self, transmittal_id: UUID) -> List[Dict]:
        """
        Get all documents for a transmittal.

        Args:
            transmittal_id: Transmittal UUID

        Returns:
            List of document dictionaries
        """
        query = """
            SELECT * FROM transmittals_transmittal_documents
            WHERE workflow_transmittal_id = %s
            ORDER BY file_name
        """
        with self.get_cursor() as (conn, cursor):
            cursor.execute(query, (transmittal_id,))
            return cursor.fetchall()

    # ================================================================
    # Recipient CRUD Operations
    # ================================================================

    def batch_insert_recipients(self, recipients: List[Dict]) -> int:
        """
        Batch insert transmittal recipients (project members).

        Args:
            recipients: List of recipient dictionaries

        Returns:
            Number of records inserted
        """
        if not recipients:
            return 0

        query = """
            INSERT INTO transmittals_transmittal_recipients (
                id, workflow_transmittal_id, bim360_account_id, bim360_project_id,
                user_id, user_name, email, company_name,
                viewed_at, downloaded_at, created_at, updated_at
            ) VALUES (
                %(id)s, %(workflow_transmittal_id)s, %(bim360_account_id)s, %(bim360_project_id)s,
                %(user_id)s, %(user_name)s, %(email)s, %(company_name)s,
                %(viewed_at)s, %(downloaded_at)s, %(created_at)s, %(updated_at)s
            )
            ON CONFLICT (workflow_transmittal_id, user_id) DO UPDATE SET
                user_name = EXCLUDED.user_name,
                email = EXCLUDED.email,
                updated_at = EXCLUDED.updated_at
        """

        with self.get_cursor() as (conn, cursor):
            execute_batch(cursor, query, recipients)
            conn.commit()
            return len(recipients)

    def get_recipients_by_transmittal(self, transmittal_id: UUID) -> List[Dict]:
        """
        Get all recipients for a transmittal.

        Args:
            transmittal_id: Transmittal UUID

        Returns:
            List of recipient dictionaries
        """
        query = """
            SELECT * FROM transmittals_transmittal_recipients
            WHERE workflow_transmittal_id = %s
            ORDER BY user_name
        """
        with self.get_cursor() as (conn, cursor):
            cursor.execute(query, (transmittal_id,))
            return cursor.fetchall()

    # ================================================================
    # Non-Member Recipient CRUD Operations
    # ================================================================

    def batch_insert_non_members(self, non_members: List[Dict]) -> int:
        """
        Batch insert non-member recipients.

        Args:
            non_members: List of non-member dictionaries

        Returns:
            Number of records inserted
        """
        if not non_members:
            return 0

        query = """
            INSERT INTO transmittals_transmittal_non_members (
                id, bim360_account_id, bim360_project_id,
                email, first_name, last_name, company_name, role,
                workflow_transmittal_id, viewed_at, downloaded_at,
                created_at, updated_at
            ) VALUES (
                %(id)s, %(bim360_account_id)s, %(bim360_project_id)s,
                %(email)s, %(first_name)s, %(last_name)s, %(company_name)s, %(role)s,
                %(workflow_transmittal_id)s, %(viewed_at)s, %(downloaded_at)s,
                %(created_at)s, %(updated_at)s
            )
            ON CONFLICT (workflow_transmittal_id, email) DO UPDATE SET
                first_name = EXCLUDED.first_name,
                last_name = EXCLUDED.last_name,
                updated_at = EXCLUDED.updated_at
        """

        with self.get_cursor() as (conn, cursor):
            execute_batch(cursor, query, non_members)
            conn.commit()
            return len(non_members)

    def get_non_members_by_transmittal(self, transmittal_id: UUID) -> List[Dict]:
        """
        Get all non-member recipients for a transmittal.

        Args:
            transmittal_id: Transmittal UUID

        Returns:
            List of non-member dictionaries
        """
        query = """
            SELECT * FROM transmittals_transmittal_non_members
            WHERE workflow_transmittal_id = %s
            ORDER BY email
        """
        with self.get_cursor() as (conn, cursor):
            cursor.execute(query, (transmittal_id,))
            return cursor.fetchall()

    # ================================================================
    # Bulk Operations
    # ================================================================

    def truncate_all_tables(self) -> Dict[str, bool]:
        """
        Truncate all transmittal tables (delete all data).
        Use with caution! This is for full sync operations.

        Returns:
            Dict mapping table names to success status
        """
        tables = [
            'transmittals_transmittal_non_members',
            'transmittals_transmittal_recipients',
            'transmittals_transmittal_documents',
            'transmittals_workflow_transmittals'
        ]

        result = {}

        with self.get_cursor() as (conn, cursor):
            for table in tables:
                try:
                    cursor.execute(f"TRUNCATE TABLE {table} CASCADE")
                    result[table] = True
                except Exception as e:
                    print(f"Error truncating {table}: {e}")
                    result[table] = False
            conn.commit()

        return result

    def get_table_counts(self) -> Dict[str, int]:
        """
        Get row counts for all transmittal tables.

        Returns:
            Dict mapping table names to row counts
        """
        tables = [
            'transmittals_workflow_transmittals',
            'transmittals_transmittal_documents',
            'transmittals_transmittal_recipients',
            'transmittals_transmittal_non_members'
        ]

        counts = {}

        with self.get_cursor() as (conn, cursor):
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                counts[table] = cursor.fetchone()['count']

        return counts

    # ================================================================
    # Query Helpers
    # ================================================================

    def get_transmittal_summary(self, transmittal_id: UUID) -> Optional[Dict]:
        """
        Get comprehensive transmittal summary with all related data counts.

        Args:
            transmittal_id: Transmittal UUID

        Returns:
            Summary dictionary or None if not found
        """
        query = """
            SELECT * FROM v_transmittal_summary
            WHERE id = %s
        """
        with self.get_cursor() as (conn, cursor):
            cursor.execute(query, (transmittal_id,))
            return cursor.fetchone()

    def search_transmittals(
        self,
        project_id: UUID,
        search_term: Optional[str] = None,
        status: Optional[int] = None,
        creator_id: Optional[UUID] = None,
        limit: int = 100
    ) -> List[Dict]:
        """
        Search transmittals with filters.

        Args:
            project_id: Project UUID
            search_term: Search in title (optional)
            status: Filter by status (optional)
            creator_id: Filter by creator (optional)
            limit: Maximum results

        Returns:
            List of matching transmittals
        """
        conditions = ["bim360_project_id = %s"]
        params = [project_id]

        if search_term:
            conditions.append("title ILIKE %s")
            params.append(f"%{search_term}%")

        if status is not None:
            conditions.append("status = %s")
            params.append(status)

        if creator_id:
            conditions.append("create_user_id = %s")
            params.append(creator_id)

        params.append(limit)

        query = f"""
            SELECT * FROM transmittals_workflow_transmittals
            WHERE {' AND '.join(conditions)}
            ORDER BY created_at DESC
            LIMIT %s
        """

        with self.get_cursor() as (conn, cursor):
            cursor.execute(query, params)
            return cursor.fetchall()
