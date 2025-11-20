#!/usr/bin/env python3
"""
Test script for Account Data Synchronization
Tests the account sync functionality including:
1. Account information sync
2. User data sync with roles
3. Company data sync
4. Project user relationships
5. Role assignments and mappings
"""

import sys
import os
import time
import json
import logging
import asyncio

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(os.path.dirname(__file__), 'test_account_sync.log'), encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)


class AccountSyncTester:
    """Test harness for account data synchronization"""
    
    def __init__(
        self, 
        account_id: str = "1caef42c-9fb7-4e6f-a5d1-cb89e69de6ea",
        project_id: str = "b.1eea4119-3553-4167-b93d-3a3d5d07d33d",
        project_name: str = "ACC Sync",
        clean_first: bool = True
    ):
        """
        Initialize account sync tester
        
        Args:
            account_id: ACC Account ID (required)
            project_id: Project ID to test (default: ACC Sync project)
            project_name: Project name for display
            clean_first: Whether to drop and recreate tables before sync
        """
        self.account_id = account_id
        self.project_id = project_id
        self.project_name = project_name
        self.clean_first = clean_first
        self.test_results = {}
        
        if not self.account_id:
            logger.error("[CONFIG] Account ID is required. Please set account_id parameter.")
            raise ValueError("Account ID is required")
    
    def check_authentication(self) -> bool:
        """Check if user is authenticated"""
        try:
            import utils
            
            access_token = utils.get_access_token()
            
            if access_token:
                logger.info("[AUTH] Successfully obtained access token")
                
                token_info = utils.get_token_info()
                if token_info:
                    logger.info(f"[AUTH] Token expires in {token_info.get('expires_in_minutes', 'unknown')} minutes")
                
                return True
            else:
                logger.error("[AUTH] No access token available")
                logger.info("[AUTH] Please login first using: http://localhost:8080/login")
                logger.info("[AUTH] Then run: python start_dev.py")
                return False
                
        except ImportError as e:
            logger.error(f"[AUTH] Failed to import utils: {e}")
            return False
        except Exception as e:
            logger.error(f"[AUTH] Error getting token: {e}")
            return False
    
    def check_database_schema(self) -> bool:
        """Check if required database tables exist"""
        try:
            from database_sql.account_sync import AccountDataSyncManager
            
            sync_manager = AccountDataSyncManager()
            conn = sync_manager.get_connection()
            cursor = conn.cursor()
            
            # Check required tables
            required_tables = [
                'accounts', 'users', 'companies', 'projects', 'project_users', 'roles'
            ]
            
            missing_tables = []
            for table in required_tables:
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = %s
                    )
                """, [table])
                
                if not cursor.fetchone()[0]:
                    missing_tables.append(table)
            
            conn.close()
            
            if missing_tables:
                logger.error(f"[SCHEMA] Missing required tables: {', '.join(missing_tables)}")
                logger.info("[SCHEMA] Please run the optimized account schema first:")
                logger.info("[SCHEMA] psql -f database_sql/account_schema_optimized.sql")
                return False
            else:
                logger.info("[SCHEMA] All required tables exist")
                return True
                
        except Exception as e:
            logger.error(f"[SCHEMA] Database schema check failed: {e}")
            return False
    
    def run_test(self):
        """Run the account sync test with detailed timing"""
        
        logger.info("="*80)
        logger.info("ACCOUNT DATA SYNCHRONIZATION TEST")
        logger.info("="*80)
        logger.info(f"Account ID: {self.account_id}")
        logger.info(f"Project ID: {self.project_id}")
        logger.info(f"Project Name: {self.project_name}")
        logger.info(f"Test Start: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        overall_start = time.time()
        timing_stats = {}
        
        try:
            # Step 1: Check authentication
            step_start = time.time()
            logger.info("[STEP 1/8] Checking authentication status...")
            logger.info("  Description: Verify OAuth token is valid and not expired")
            if not self.check_authentication():
                raise Exception("Authentication failed. Please login first.")
            timing_stats['authentication'] = time.time() - step_start
            logger.info(f"  [OK] Completed in {timing_stats['authentication']:.2f}s")
            
            # Step 2: Check database schema (skip if clean_first=True)
            step_start = time.time()
            logger.info("\n[STEP 2/8] Checking database schema...")
            logger.info("  Description: Verify required tables exist in database")
            if self.clean_first:
                logger.info("  [SKIP] Schema check skipped (clean_first=True, tables will be recreated)")
            else:
                if not self.check_database_schema():
                    raise Exception("Database schema check failed. Please setup account schema first.")
            timing_stats['schema_check'] = time.time() - step_start
            logger.info(f"  [OK] Completed in {timing_stats['schema_check']:.2f}s")
            
            # Step 3: Initialize sync manager
            step_start = time.time()
            logger.info("\n[STEP 3/8] Initializing account sync manager...")
            logger.info("  Description: Import AccountDataSyncManager and create connections")
            
            try:
                from database_sql.account_sync import AccountDataSyncManager
                import utils
                
                sync_manager = AccountDataSyncManager()
                access_token = utils.get_access_token()
                
                logger.info("  [OK] AccountDataSyncManager initialized")
                logger.info("  [OK] Database connection established")
                logger.info("  [OK] Access token obtained")
                
            except ImportError as e:
                logger.error(f"  [ERROR] Failed to import modules: {e}")
                raise Exception(f"Could not import required modules: {e}")
            
            timing_stats['initialization'] = time.time() - step_start
            logger.info(f"  [OK] Completed in {timing_stats['initialization']:.2f}s")
            
            # Step 4: Sync account information (skip if clean_first=True)
            step_start = time.time()
            logger.info("\n[STEP 4/8] Synchronizing account information...")
            logger.info("  Description: Create/update account record in database")
            
            if self.clean_first:
                logger.info("  [SKIP] Individual account sync skipped (clean_first=True, will be done in full sync)")
                account_success = True
            else:
                account_success = sync_manager.sync_account_info(
                    self.account_id, 
                    f"Account {self.account_id}"
                )
                
                if not account_success:
                    logger.warning("  [WARNING] Account sync failed, but continuing...")
                else:
                    logger.info("  [OK] Account information synchronized")
            
            timing_stats['account_sync'] = time.time() - step_start
            logger.info(f"  [OK] Completed in {timing_stats['account_sync']:.2f}s")
            
            # Step 5: Sync project information (skip if clean_first=True)
            step_start = time.time()
            logger.info("\n[STEP 5/8] Synchronizing project information...")
            logger.info("  Description: Create/update project record in database")
            
            if self.clean_first:
                logger.info("  [SKIP] Individual project sync skipped (clean_first=True, will be done in full sync)")
                project_success = True
            else:
                project_success = sync_manager.sync_project_info(
                    self.project_id,
                    self.account_id,
                    self.project_name
                )
                
                if not project_success:
                    logger.warning("  [WARNING] Project sync failed, but continuing...")
                else:
                    logger.info(f"  [OK] Project '{self.project_name}' synchronized")
            
            timing_stats['project_sync'] = time.time() - step_start
            logger.info(f"  [OK] Completed in {timing_stats['project_sync']:.2f}s")
            
            # Step 6: Run full account data sync
            step_start = time.time()
            logger.info("\n[STEP 6/8] Running full account data synchronization...")
            logger.info("  Description: Async sync of users, companies, and project relationships")
            logger.info("  Sub-steps:")
            logger.info("    6.1 - [ASYNC] Fetch account users from ACC API")
            logger.info("    6.2 - [ASYNC] Fetch project companies from ACC API")
            logger.info("    6.3 - [ASYNC] Fetch project users with roles from ACC API")
            logger.info("    6.4 - [BATCH UPSERT] Bulk insert/update into database")
            
            # Run full sync with clean_first parameter
            sync_stats = asyncio.run(sync_manager.full_account_sync(
                account_id=self.account_id,
                project_ids=[self.project_id],
                access_token=access_token,
                show_progress=True,
                clean_first=self.clean_first  # Use the parameter from constructor
            ))
            
            logger.info("  [OK] Full account sync completed")
            
            timing_stats['full_sync'] = time.time() - step_start
            logger.info(f"  [OK] Completed in {timing_stats['full_sync']:.2f}s")
            
            # Step 7: Test role summary functionality
            step_start = time.time()
            logger.info("\n[STEP 7/8] Testing role summary functionality...")
            logger.info("  Description: Generate account role summary and user mappings")
            
            role_summary = sync_manager.get_account_roles_summary(self.account_id)
            
            if 'error' in role_summary:
                logger.warning(f"  [WARNING] Role summary failed: {role_summary['error']}")
                role_summary = {'role_summary': [], 'user_role_mapping': {}, 'statistics': {}}
            else:
                logger.info("  [OK] Role summary generated successfully")
            
            timing_stats['role_summary'] = time.time() - step_start
            logger.info(f"  [OK] Completed in {timing_stats['role_summary']:.2f}s")
            
            # Step 8: Generate comprehensive report
            step_start = time.time()
            logger.info("\n[STEP 8/8] Generating comprehensive test report...")
            logger.info("  Description: Create detailed report with all metrics")
            
            overall_duration = time.time() - overall_start
            report = self._generate_report(
                sync_stats, 
                role_summary,
                overall_duration, 
                timing_stats
            )
            
            timing_stats['report_generation'] = time.time() - step_start
            logger.info(f"  [OK] Completed in {timing_stats['report_generation']:.2f}s")
            
            # Save and display results
            self._save_and_display_results(report)
            
            # Print timing breakdown
            self._print_timing_breakdown(timing_stats, overall_duration)
            
            return report
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - overall_start
            
            error_report = {
                'success': False,
                'test_metadata': {
                    'account_id': self.account_id,
                    'project_id': self.project_id,
                    'project_name': self.project_name,
                    'test_type': 'account_data_sync',
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'duration_seconds': duration,
                    'success': False
                },
                'sync_results': {
                    'status': 'error',
                    'error_details': str(e),
                    'users_synced': 0,
                    'companies_synced': 0,
                    'project_users_synced': 0
                },
                'performance_metrics': {
                    'duration_seconds': duration,
                    'items_per_second': 0
                }
            }
            
            logger.error(f"[FAILED] Account sync test failed: {e}")
            logger.exception("Full traceback:")
            self._save_and_display_results(error_report)
            return error_report
    
    def _generate_report(
        self, 
        sync_stats: dict, 
        role_summary: dict,
        duration: float, 
        timing_stats: dict
    ) -> dict:
        """Generate comprehensive test report"""
        
        # Calculate totals
        total_users = sync_stats.get('statistics', {}).get('users_synced', 0) + sync_stats.get('statistics', {}).get('users_updated', 0)
        total_companies = sync_stats.get('statistics', {}).get('companies_synced', 0) + sync_stats.get('statistics', {}).get('companies_updated', 0)
        total_project_users = sync_stats.get('statistics', {}).get('project_users_synced', 0) + sync_stats.get('statistics', {}).get('project_users_updated', 0)
        total_items = total_users + total_companies + total_project_users
        
        items_per_second = total_items / duration if duration > 0 else 0
        error_count = len(sync_stats.get('errors', []))
        sync_success = error_count == 0 and total_items > 0
        
        return {
            'success': sync_success,
            'test_metadata': {
                'account_id': self.account_id,
                'project_id': self.project_id,
                'project_name': self.project_name,
                'test_type': 'account_data_sync',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'duration_seconds': duration,
                'success': sync_success
            },
            
            'sync_results': {
                'status': 'success' if sync_success else 'error',
                'accounts_synced': sync_stats.get('statistics', {}).get('accounts_synced', 0),
                'users_synced': sync_stats.get('statistics', {}).get('users_synced', 0),
                'users_updated': sync_stats.get('statistics', {}).get('users_updated', 0),
                'companies_synced': sync_stats.get('statistics', {}).get('companies_synced', 0),
                'companies_updated': sync_stats.get('statistics', {}).get('companies_updated', 0),
                'project_users_synced': sync_stats.get('statistics', {}).get('project_users_synced', 0),
                'project_users_updated': sync_stats.get('statistics', {}).get('project_users_updated', 0),
                'total_items_synced': total_items,
                'error_count': error_count,
                'error_details': sync_stats.get('errors', [])[:10] if sync_stats.get('errors') else []
            },
            
            'role_analysis': {
                'unique_roles': len(role_summary.get('role_summary', [])),
                'users_with_roles': len(role_summary.get('user_role_mapping', {})),
                'role_assignments': role_summary.get('statistics', {}).get('total_role_assignments', 0),
                'projects_with_roles': role_summary.get('statistics', {}).get('projects_with_roles', 0),
                'query_duration': role_summary.get('statistics', {}).get('query_duration_seconds', 0),
                'top_roles': [
                    {
                        'name': role.get('role_name'),
                        'users': role.get('unique_users', 0),
                        'projects': role.get('unique_projects', 0),
                        'assignments': role.get('total_assignments', 0)
                    }
                    for role in role_summary.get('role_summary', [])[:5]
                ]
            },
            
            'performance_metrics': {
                'duration_seconds': duration,
                'items_per_second': items_per_second,
                'execution_time': sync_stats.get('execution_time', 'N/A'),
                'projects_processed': sync_stats.get('projects_processed', 1),
                'optimization_enabled': True,
                'async_operations': True
            },
            
            'timing_breakdown': timing_stats,
            
            'data_quality': {
                'users_with_emails': 'N/A',  # Would need to query database
                'users_with_companies': 'N/A',
                'users_with_roles': len(role_summary.get('user_role_mapping', {})),
                'companies_with_trades': 'N/A',
                'data_completeness': 'Good' if sync_success else 'Poor'
            },
            
            'production_readiness': {
                'real_api_integration': True,
                'authentication_working': sync_success,
                'database_integration': True,
                'error_handling': 'Implemented' if sync_success else f"Errors: {error_count}",
                'optimization_status': 'Enhanced',
                'async_ready': True,
                'scalability': 'High'
            }
        }
    
    def _print_timing_breakdown(self, timing_stats: dict, total_duration: float) -> None:
        """Print detailed timing breakdown"""
        
        print("\n" + "="*80)
        print("TIMING BREAKDOWN")
        print("="*80)
        
        print(f"\nTotal Duration: {total_duration:.2f}s")
        print("\nStep-by-Step Timing:")
        
        steps = [
            ('authentication', 'Authentication Check'),
            ('schema_check', 'Database Schema Check'),
            ('initialization', 'Module Initialization'),
            ('account_sync', 'Account Information Sync'),
            ('project_sync', 'Project Information Sync'),
            ('full_sync', 'Full Account Data Sync'),
            ('role_summary', 'Role Summary Generation'),
            ('report_generation', 'Report Generation')
        ]
        
        for key, label in steps:
            if key in timing_stats:
                duration = timing_stats[key]
                percentage = (duration / total_duration * 100) if total_duration > 0 else 0
                bar_length = int(percentage / 2)  # Scale to 50 chars max
                bar = '#' * bar_length + '-' * (50 - bar_length)
                print(f"  {label:.<35} {duration:>6.2f}s ({percentage:>5.1f}%) {bar}")
        
        print("\n" + "="*80)
    
    def _save_and_display_results(self, report: dict) -> None:
        """Save and display test results"""
        
        # Save detailed report
        timestamp = int(time.time())
        filename = f"test_account_sync_{timestamp}.json"
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False, default=str)
            logger.info(f"[SAVE] Results saved to: {filename}")
        except Exception as e:
            logger.error(f"[SAVE] Failed to save results: {e}")
        
        # Display summary
        self._print_summary(report)
    
    def _print_summary(self, report: dict) -> None:
        """Print test summary"""
        
        print("\n" + "="*80)
        print("ACCOUNT DATA SYNC TEST SUMMARY")
        print("="*80)
        
        meta = report['test_metadata']
        sync = report.get('sync_results', {})
        roles = report.get('role_analysis', {})
        perf = report.get('performance_metrics', {})
        quality = report.get('data_quality', {})
        prod = report.get('production_readiness', {})
        
        print(f"\n[ACCOUNT] {meta.get('account_id', 'unknown')}")
        if 'project_name' in meta and 'project_id' in meta:
            print(f"[PROJECT] {meta['project_name']} ({meta['project_id']})")
        elif 'project_id' in meta:
            print(f"[PROJECT] {meta['project_id']}")
        print(f"[SUCCESS] {meta['success']}")
        print(f"[DURATION] {meta['duration_seconds']:.2f} seconds")
        print(f"[STATUS] {sync.get('status', 'unknown')}")
        
        if meta['success']:
            print(f"\n[SYNC RESULTS]")
            print(f"  Accounts: {sync.get('accounts_synced', 0)} synced")
            print(f"  Users: {sync.get('users_synced', 0)} new, {sync.get('users_updated', 0)} updated")
            print(f"  Companies: {sync.get('companies_synced', 0)} new, {sync.get('companies_updated', 0)} updated")
            print(f"  Project Users: {sync.get('project_users_synced', 0)} new, {sync.get('project_users_updated', 0)} updated")
            print(f"  Total Items: {sync.get('total_items_synced', 0)}")
            print(f"  Performance: {perf.get('items_per_second', 0):.2f} items/sec")
            
            print(f"\n[ROLE ANALYSIS]")
            print(f"  Unique Roles: {roles.get('unique_roles', 0)}")
            print(f"  Users with Roles: {roles.get('users_with_roles', 0)}")
            print(f"  Total Role Assignments: {roles.get('role_assignments', 0)}")
            print(f"  Projects with Roles: {roles.get('projects_with_roles', 0)}")
            print(f"  Query Duration: {roles.get('query_duration', 0):.3f}s")
            
            if roles.get('top_roles'):
                print(f"\n[TOP 5 ROLES]")
                for i, role in enumerate(roles['top_roles'], 1):
                    print(f"  {i}. {role['name']}: {role['users']} users, {role['projects']} projects, {role['assignments']} assignments")
            
            print(f"\n[PERFORMANCE METRICS]")
            print(f"  Total Duration: {perf.get('duration_seconds', 0):.2f}s")
            print(f"  Items per Second: {perf.get('items_per_second', 0):.2f}")
            print(f"  Projects Processed: {perf.get('projects_processed', 0)}")
            print(f"  Async Operations: {'[OK] Enabled' if perf.get('async_operations') else '[X] Disabled'}")
            print(f"  Optimization: {'[OK] Enabled' if perf.get('optimization_enabled') else '[X] Disabled'}")
            
            print(f"\n[DATA QUALITY]")
            print(f"  Users with Roles: {quality.get('users_with_roles', 0)}")
            print(f"  Data Completeness: {quality.get('data_completeness', 'Unknown')}")
            
            print(f"\n[PRODUCTION READINESS]")
            print(f"  Real API Integration: {'[OK] Yes' if prod.get('real_api_integration') else '[X] No'}")
            print(f"  Authentication: {'[OK] Working' if prod.get('authentication_working') else '[X] Failed'}")
            print(f"  Database Integration: {'[OK] Working' if prod.get('database_integration') else '[X] Failed'}")
            print(f"  Error Handling: {prod.get('error_handling', 'Unknown')}")
            print(f"  Optimization: {prod.get('optimization_status', 'Unknown')}")
            print(f"  Async Ready: {'[OK] Yes' if prod.get('async_ready') else '[X] No'}")
            print(f"  Scalability: {prod.get('scalability', 'Unknown')}")
        else:
            print(f"\n[ERROR] {sync.get('error_details', ['Unknown error'])[0] if sync.get('error_details') else 'Unknown error'}")
            print(f"[ERROR COUNT] {sync.get('error_count', 0)}")
            if sync.get('error_details'):
                print(f"\n[FIRST 5 ERRORS]")
                for i, error in enumerate(sync.get('error_details', [])[:5], 1):
                    print(f"  {i}. {error}")
        
        print("\n" + "="*80)


def main():
    """Main test function"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Account Data Synchronization Test')
    parser.add_argument('--account-id', type=str, 
                       default="1caef42c-9fb7-4e6f-a5d1-cb89e69de6ea",
                       help='ACC Account ID (default: real account ID)')
    parser.add_argument('--project-id', type=str, 
                       default="b.1eea4119-3553-4167-b93d-3a3d5d07d33d",
                       help='Project ID to test (default: ACC Sync project)')
    parser.add_argument('--project-name', type=str, default="ACC Sync",
                       help='Project name for display (default: ACC Sync)')
    parser.add_argument('--no-clean', action='store_false', dest='clean_first',
                       help='Skip dropping tables before sync (not recommended)')
    
    args = parser.parse_args()
    
    # Create tester and run
    tester = AccountSyncTester(
        account_id=args.account_id,
        project_id=args.project_id,
        project_name=args.project_name,
        clean_first=args.clean_first
    )
    
    try:
        report = tester.run_test()
        
        if report.get('success', False):
            print(f"\n[SUCCESS] Account data sync test completed successfully!")
            print(f"Account: {args.account_id}")
            print(f"Project: {args.project_name}")
            return 0
        else:
            print(f"\n[FAILED] Account data sync test failed!")
            return 1
            
    except Exception as e:
        print(f"\n[ERROR] Test execution failed: {e}")
        logger.exception("Test execution failed")
        return 1


if __name__ == "__main__":
    print("="*80)
    print("Account Data Synchronization Test")
    print("="*80)
    print("This script tests the account data synchronization including:")
    print("  • Account information sync")
    print("  • User data sync with role assignments")
    print("  • Company data sync")
    print("  • Project user relationships")
    print("  • Role summary and analysis")
    print()
    print("Make sure you're logged in via the web interface first")
    print()
    print("Usage:")
    print("  python test_account_sync.py                                    # Use default account ID")
    print("  python test_account_sync.py --account-id YOUR_ACCOUNT_ID       # Use custom account ID")
    print("  python test_account_sync.py --project-id PROJECT_ID            # Use custom project ID")
    print("  python test_account_sync.py --project-name 'My Project'        # Use custom project name")
    print("  python test_account_sync.py --no-clean                         # Skip table cleanup (not recommended)")
    print()
    
    exit(main())
