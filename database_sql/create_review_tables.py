"""
Create Review System Database Tables
Executes the review_system_schema.sql file to create all necessary tables
"""

import sys
import os

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from database_sql.neon_config import NeonConfig
from database_sql.review_data_access import ReviewDataAccess


def create_tables():
    """Create all review system tables"""
    print("\n" + "="*80)
    print("CREATING REVIEW SYSTEM DATABASE TABLES")
    print("="*80)
    
    try:
        # Read SQL schema file
        schema_file = os.path.join(current_dir, 'review_system_schema.sql')
        
        if not os.path.exists(schema_file):
            print(f"ERROR: Schema file not found: {schema_file}")
            return False
        
        print(f"\nReading schema file: {schema_file}")
        
        with open(schema_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        print(f"  Schema file size: {len(sql_content)} characters")
        
        # Connect to database
        print("\nConnecting to database...")
        config = NeonConfig()
        da = ReviewDataAccess(config.get_db_params())
        
        print("  Database connection successful")
        
        # Execute SQL
        print("\nExecuting SQL schema...")
        print("  This may take a few moments...")
        
        with da.get_cursor() as cursor:
            # Execute the entire SQL file
            cursor.execute(sql_content)
            print("  SQL execution successful")
        
        # Verify tables were created
        print("\nVerifying tables...")
        
        tables = [
            'workflows',
            'reviews', 
            'review_file_versions',
            'review_progress',
            'review_comments',
            'approval_decisions',
            'review_notifications',
            'workflow_templates'
        ]
        
        with da.get_cursor() as cursor:
            for table in tables:
                cursor.execute(f"""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = '{table}'
                    )
                """)
                result = cursor.fetchone()
                exists = result[0] if isinstance(result, tuple) else result.get('exists', False)
                status = "[OK]" if exists else "[MISSING]"
                print(f"  {status} Table '{table}'")
                
                if not exists:
                    print(f"    WARNING: Table '{table}' was not created!")
        
        # Check views
        print("\nVerifying views...")
        views = ['reviews_overview', 'pending_tasks_view']
        
        with da.get_cursor() as cursor:
            for view in views:
                cursor.execute(f"""
                    SELECT EXISTS (
                        SELECT FROM information_schema.views 
                        WHERE table_schema = 'public' 
                        AND table_name = '{view}'
                    )
                """)
                result = cursor.fetchone()
                exists = result[0] if isinstance(result, tuple) else result.get('exists', False)
                status = "[OK]" if exists else "[MISSING]"
                print(f"  {status} View '{view}'")
        
        print("\n" + "="*80)
        print("DATABASE TABLES CREATED SUCCESSFULLY!")
        print("="*80)
        
        return True
    
    except Exception as e:
        print(f"\nERROR: Failed to create tables")
        print(f"  Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point"""
    success = create_tables()
    
    if success:
        print("\nNext steps:")
        print("  1. Run the simple test to verify: python database_sql\\simple_test.py")
        print("  2. Run full sync: python database_sql\\full_review_sync.py --project-id <your-project-id>")
        sys.exit(0)
    else:
        print("\nTable creation failed. Please check the error messages above.")
        sys.exit(1)


if __name__ == "__main__":
    main()

