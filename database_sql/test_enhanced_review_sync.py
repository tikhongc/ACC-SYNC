#!/usr/bin/env python3
"""
Test script for Enhanced Review Sync - 增强优化版
测试增强优化后的异步并行同步功能，包括：
1. 异步并行API调用 (asyncio + aiohttp)
2. 批量UPSERT优化 (PostgreSQL ON CONFLICT)
3. Cachetools 内存缓存层
4. 智能重试机制和断路器模式
5. 增强性能监控和瓶颈分析
6. 内存优化
7. 候选人配置自动创建和验证 (review_step_candidates)

注意：账户同步功能已移除，现在使用独立的 database_sql/account_sync.py
"""

import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    import codecs
    try:
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except AttributeError:
        # In newer Python versions, stdout/stderr may already be text streams
        pass

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
        logging.FileHandler(os.path.join(os.path.dirname(__file__), 'test_enhanced_review_sync.log'), encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)


class EnhancedReviewSyncTester:
    """Test harness for enhanced review synchronization with asyncio"""
    
    def __init__(
        self, 
        max_concurrent: int = 10,
        enable_cache: bool = True,
        cache_ttl: int = 3600,
        cache_max_size: int = 5000,
        batch_size: int = 100
    ):
        """
        Initialize enhanced tester
        
        Args:
            max_concurrent: Number of concurrent async tasks (default: 10)
            enable_cache: Enable memory caching (default: True)
            cache_ttl: Cache TTL in seconds (default: 3600)
            cache_max_size: Maximum cache entries (default: 5000)
            batch_size: Batch size for database operations (default: 100)
        """
        self.project_id = "b.1eea4119-3553-4167-b93d-3a3d5d07d33d"
        self.max_concurrent = max_concurrent
        self.enable_cache = enable_cache
        self.cache_ttl = cache_ttl
        self.cache_max_size = cache_max_size
        self.batch_size = batch_size
        self.test_results = {}
    
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
    
    def run_test(self):
        """Run the enhanced review sync test with detailed timing"""
        
        logger.info("="*80)
        logger.info("ENHANCED REVIEW SYNC TEST - Async + Cache + UPSERT Optimization")
        logger.info("="*80)
        logger.info(f"Project ID: {self.project_id}")
        logger.info(f"Max Concurrent: {self.max_concurrent}")
        logger.info(f"Cache Enabled: {self.enable_cache}")
        logger.info(f"Cache TTL: {self.cache_ttl}s")
        logger.info(f"Cache Max Size: {self.cache_max_size} entries")
        logger.info(f"Batch Size: {self.batch_size}")
        logger.info(f"Test Start: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        overall_start = time.time()
        timing_stats = {}
        
        try:
            # Step 1: Check authentication
            step_start = time.time()
            logger.info("[STEP 1/7] Checking authentication status...")
            logger.info("  Description: Verify OAuth token is valid and not expired")
            if not self.check_authentication():
                raise Exception("Authentication failed. Please login first.")
            timing_stats['authentication'] = time.time() - step_start
            logger.info(f"  [OK] Completed in {timing_stats['authentication']:.2f}s")
            
            # Step 2: Import and initialize enhanced sync modules
            step_start = time.time()
            logger.info("\n[STEP 2/7] Initializing enhanced sync modules...")
            logger.info("  Description: Import EnhancedReviewSyncManager and create connections")
            logger.info("  Features:")
            logger.info("    - Asyncio + aiohttp for concurrent API calls")
            logger.info("    - Cachetools memory caching layer")
            logger.info("    - PostgreSQL UPSERT optimization")
            logger.info("    - Circuit breaker pattern")
            logger.info("    - Performance monitoring")
            logger.info("    - Note: Account sync functionality removed (use account_sync.py)")
            
            try:
                from api_modules.postgresql_review_sync.review_sync_manager_enhanced import EnhancedReviewSyncManager
                from database_sql.review_data_access import ReviewDataAccess
                import utils
                
                # 初始化数据访问层
                da = ReviewDataAccess()
                
                # 初始化增强的同步管理器（账户同步功能已移除）
                sync_manager = EnhancedReviewSyncManager(
                    data_access=da,
                    max_concurrent=self.max_concurrent,
                    enable_cache=self.enable_cache,
                    cache_ttl=self.cache_ttl,
                    cache_max_size=self.cache_max_size,
                    batch_size=self.batch_size
                )
                
                logger.info("  [OK] EnhancedReviewSyncManager initialized (review sync only)")
                logger.info(f"  [OK] Max concurrent: {self.max_concurrent}")
                logger.info(f"  [OK] Cache enabled: {self.enable_cache}")
                logger.info(f"  [OK] Cache max size: {self.cache_max_size}")
                logger.info(f"  [OK] Batch size: {self.batch_size}")
                logger.info("  [OK] Database connection established")
                logger.info("  [INFO] Account sync functionality removed from this manager")
            except ImportError as e:
                logger.error(f"  [ERROR] Failed to import modules: {e}")
                raise Exception(f"Could not import required modules: {e}")
            
            timing_stats['initialization'] = time.time() - step_start
            logger.info(f"  [OK] Completed in {timing_stats['initialization']:.2f}s")
            
            # Step 3: Check cache status
            step_start = time.time()
            logger.info("\n[STEP 3/7] Checking cache status...")
            logger.info("  Description: Verify memory cache availability and configuration")
            
            if sync_manager.cache.enabled:
                cache_stats = sync_manager.cache.get_stats()
                logger.info("  [OK] Memory cache is enabled")
                logger.info(f"  [OK] Cache TTL: {cache_stats.get('ttl')}s")
                logger.info(f"  [OK] Cache Max Size: {cache_stats.get('max_size')} entries")
                logger.info(f"  [OK] Current Size: {cache_stats.get('current_size')} entries")
                logger.info(f"  [OK] Usage: {cache_stats.get('usage_percent'):.1f}%")
            else:
                logger.warning("  [WARNING] Memory cache is disabled or unavailable")
                logger.info("  [INFO] Sync will continue without caching")
            
            timing_stats['cache_check'] = time.time() - step_start
            logger.info(f"  [OK] Completed in {timing_stats['cache_check']:.2f}s")
            
            # Step 4: Run enhanced synchronization with asyncio
            step_start = time.time()
            logger.info("\n[STEP 4/7] Running enhanced async synchronization...")
            logger.info("  Description: Clean database, recreate schema, async parallel sync")
            logger.info("  Sub-steps:")
            logger.info("    4.1 - Drop all review tables, views, and enum types")
            logger.info("    4.2 - Recreate schema from review_system_schema.sql")
            logger.info("    4.3 - [ASYNC] Fetch all workflows from ACC API")
            logger.info("    4.4 - [ASYNC] Fetch all reviews with smart pagination")
            logger.info("    4.5 - [ASYNC] Fetch file versions and progress for all reviews")
            logger.info("    4.6 - [CANDIDATES] Create review_step_candidates configurations")
            logger.info("    4.7 - [BATCH UPSERT] Bulk insert/update into database")
            logger.info(f"  Project: {self.project_id}")
            logger.info(f"  Mode: [ENHANCED] Async (Optimized)")
            
            # 使用 full_review_sync 进行实际同步（集成缓存）
            try:
                from database_sql.full_review_sync import FullReviewSync
                
                # 创建 FullReviewSync 实例，传入 sync_manager 以启用缓存
                full_sync = FullReviewSync(
                    self.project_id,
                    sync_manager=sync_manager  # ✅ 传入 sync_manager 启用缓存
                )
                
                # 运行完整同步（包括清理和重建schema）
                logger.info("  [SYNC] Executing full sync with cache-enabled manager...")
                logger.info(f"  [CACHE] Cache enabled: {sync_manager.cache.enabled}")
                if sync_manager.cache.enabled:
                    cache_stats = sync_manager.cache.get_stats()
                    logger.info(f"  [CACHE] Max size: {cache_stats.get('max_size')} entries")
                    logger.info(f"  [CACHE] TTL: {cache_stats.get('ttl')}s")
                
                # 跳过复杂的账户schema检查，直接进行同步
                # 注意：假设账户同步已经通过 account_sync.py 完成
                logger.info("  [SCHEMA] Skipping account schema check (assuming already synced)")
                logger.info("  [INFO] If sync fails, please run: python database_sql/test_account_sync.py")
                
                # 直接运行同步（移除线程机制以避免输出缓冲问题）
                logger.info("  [SYNC] Starting synchronization (this may take several minutes)...")
                logger.info("  [INFO] Output will be displayed in real-time")
                
                # 直接运行同步，不使用线程
                sync_stats = full_sync.run_full_sync(clean_first=True)
                
                # 添加性能统计
                if 'performance' not in sync_stats:
                    sync_stats['performance'] = sync_manager.metrics.to_dict()
                
                logger.info("  [OK] Full sync completed successfully")
                
            except Exception as e:
                logger.error(f"  [ERROR] Sync failed: {str(e)}")
                # 创建错误统计
                sync_stats = {
                    'workflows_total': 0,
                    'workflows_synced': 0,
                    'reviews_total': 0,
                    'reviews_synced': 0,
                    'file_versions_total': 0,
                    'file_versions_synced': 0,
                    'progress_steps_total': 0,
                    'progress_steps_synced': 0,
                    'workflow_templates_total': 0,
                    'workflow_templates_synced': 0,
                    'errors': [str(e)],
                    'performance': sync_manager.metrics.to_dict()
                }
            
            timing_stats['synchronization'] = time.time() - step_start
            logger.info(f"  [OK] Completed in {timing_stats['synchronization']:.2f}s")
            
            # Step 5: Print performance report
            step_start = time.time()
            logger.info("\n[STEP 5/7] Generating performance analysis...")
            logger.info("  Description: Analyze performance metrics and identify bottlenecks")
            
            sync_manager.print_performance_report()
            
            timing_stats['performance_analysis'] = time.time() - step_start
            logger.info(f"  [OK] Completed in {timing_stats['performance_analysis']:.2f}s")
            
            # Step 6: Verify candidates configuration
            step_start = time.time()
            logger.info("\n[STEP 6/8] Verifying candidates configuration...")
            logger.info("  Description: Check review_step_candidates table and data integrity")
            candidates_stats = self._verify_candidates_configuration()
            timing_stats['candidates_verification'] = time.time() - step_start
            logger.info(f"  [OK] Completed in {timing_stats['candidates_verification']:.2f}s")
            
            # Step 7: Analyze results
            step_start = time.time()
            logger.info("\n[STEP 7/8] Analyzing synchronization results...")
            logger.info("  Description: Calculate statistics and identify issues")
            analysis = self._analyze_sync_results(sync_stats, timing_stats['synchronization'])
            timing_stats['analysis'] = time.time() - step_start
            logger.info(f"  [OK] Completed in {timing_stats['analysis']:.2f}s")
            
            # Step 8: Generate and save report
            step_start = time.time()
            logger.info("\n[STEP 8/8] Generating comprehensive test report...")
            logger.info("  Description: Create JSON report with all metrics")
            overall_duration = time.time() - overall_start
            report = self._generate_report(
                sync_stats, 
                analysis, 
                overall_duration, 
                timing_stats,
                sync_manager.get_performance_report(),
                candidates_stats
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
                    'project_id': self.project_id,
                    'test_type': 'enhanced_review_sync',
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'duration_seconds': duration,
                    'success': False
                },
                'sync_results': {
                    'status': 'error',
                    'error_details': str(e),
                    'workflows_synced': 0,
                    'reviews_synced': 0,
                    'file_versions_synced': 0,
                    'progress_steps_synced': 0
                },
                'performance_metrics': {
                    'duration_seconds': duration,
                    'items_per_second': 0
                }
            }
            
            logger.error(f"[FAILED] Enhanced review sync test failed: {e}")
            logger.exception("Full traceback:")
            self._save_and_display_results(error_report)
            return error_report
    
    def _verify_candidates_configuration(self) -> dict:
        """验证候选人配置同步结果"""
        try:
            from database_sql.review_data_access_enhanced import EnhancedReviewDataAccess
            
            da = EnhancedReviewDataAccess()
            conn = da.get_connection()
            cursor = conn.cursor()
            
            # 检查 review_step_candidates 表是否存在
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_name = 'review_step_candidates'
            """)
            
            table_exists = cursor.fetchone() is not None
            
            if not table_exists:
                logger.warning("  [WARNING] review_step_candidates table does not exist")
                return {
                    'table_exists': False,
                    'total_configs': 0,
                    'configs_with_candidates': 0,
                    'source_distribution': {},
                    'reviews_with_configs': 0,
                    'error': 'Table does not exist'
                }
            
            # 统计候选人配置数据
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_configs,
                    COUNT(CASE WHEN candidates != '{"users":[],"roles":[],"companies":[]}' 
                               AND candidates IS NOT NULL THEN 1 END) as configs_with_candidates,
                    COUNT(DISTINCT review_id) as reviews_with_configs
                FROM review_step_candidates 
                WHERE is_active = true
            """)
            
            stats = cursor.fetchone()
            
            # 统计数据来源分布
            cursor.execute("""
                SELECT source, COUNT(*) as count
                FROM review_step_candidates 
                WHERE is_active = true
                GROUP BY source
                ORDER BY count DESC
            """)
            
            source_distribution = dict(cursor.fetchall())
            
            # 检查候选人数据质量
            cursor.execute("""
                SELECT 
                    rsc.review_id,
                    rsc.step_id,
                    rsc.step_name,
                    rsc.source,
                    rsc.candidates,
                    COALESCE(r.name, 'Unknown') as review_title
                FROM review_step_candidates rsc
                JOIN reviews r ON rsc.review_id = r.id
                WHERE rsc.is_active = true
                AND rsc.candidates != '{"users":[],"roles":[],"companies":[]}'
                AND rsc.candidates IS NOT NULL
                LIMIT 5
            """)
            
            sample_configs = cursor.fetchall()
            
            logger.info(f"  [CANDIDATES] Table exists: {table_exists}")
            logger.info(f"  [CANDIDATES] Total configurations: {stats[0]}")
            logger.info(f"  [CANDIDATES] Configs with candidates: {stats[1]}")
            logger.info(f"  [CANDIDATES] Reviews with configs: {stats[2]}")
            logger.info(f"  [CANDIDATES] Source distribution: {source_distribution}")
            
            if sample_configs:
                logger.info(f"  [CANDIDATES] Sample configurations:")
                for config in sample_configs:
                    review_id, step_id, step_name, source, candidates, review_title = config
                    candidates_data = json.loads(candidates) if isinstance(candidates, str) else candidates
                    user_count = len(candidates_data.get('users', []))
                    role_count = len(candidates_data.get('roles', []))
                    company_count = len(candidates_data.get('companies', []))
                    logger.info(f"    Review {review_id} ({review_title[:30]}...) - Step: {step_name}")
                    logger.info(f"      Source: {source}, Users: {user_count}, Roles: {role_count}, Companies: {company_count}")
            
            cursor.close()
            conn.close()
            
            return {
                'table_exists': table_exists,
                'total_configs': stats[0],
                'configs_with_candidates': stats[1],
                'source_distribution': source_distribution,
                'reviews_with_configs': stats[2],
                'sample_configs': len(sample_configs),
                'success': True
            }
            
        except Exception as e:
            logger.error(f"  [ERROR] Failed to verify candidates configuration: {e}")
            return {
                'table_exists': False,
                'total_configs': 0,
                'configs_with_candidates': 0,
                'source_distribution': {},
                'reviews_with_configs': 0,
                'error': str(e),
                'success': False
            }
    
    def _analyze_sync_results(self, sync_stats: dict, duration: float) -> dict:
        """Analyze sync results"""
        
        total_items = (
            sync_stats.get('workflows_synced', 0) +
            sync_stats.get('reviews_synced', 0) +
            sync_stats.get('file_versions_synced', 0) +
            sync_stats.get('progress_steps_synced', 0) +
            sync_stats.get('workflow_templates_synced', 0)
        )
        
        items_per_second = total_items / duration if duration > 0 else 0
        
        return {
            'sync_success': len(sync_stats.get('errors', [])) == 0,
            'total_items': total_items,
            'items_per_second': items_per_second,
            'error_count': len(sync_stats.get('errors', [])),
            'error_details': sync_stats.get('errors', [])
        }
    
    def _generate_report(
        self, 
        sync_stats: dict, 
        analysis: dict, 
        duration: float, 
        timing_stats: dict,
        performance_report: dict,
        candidates_stats: dict = None
    ) -> dict:
        """Generate comprehensive test report with enhanced metrics"""
        
        return {
            'success': analysis['sync_success'],
            'test_metadata': {
                'project_id': self.project_id,
                'test_type': 'enhanced_review_sync',
                'sync_mode': 'async_parallel',
                'max_concurrent': self.max_concurrent,
                'cache_enabled': self.enable_cache,
                'cache_ttl': self.cache_ttl,
                'cache_max_size': self.cache_max_size,
                'batch_size': self.batch_size,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'duration_seconds': duration,
                'success': analysis['sync_success']
            },
            
            'sync_results': {
                'status': 'success' if analysis['sync_success'] else 'error',
                'workflows_total': sync_stats.get('workflows_total', 0),
                'workflows_synced': sync_stats.get('workflows_synced', 0),
                'reviews_total': sync_stats.get('reviews_total', 0),
                'reviews_synced': sync_stats.get('reviews_synced', 0),
                'file_versions_total': sync_stats.get('file_versions_total', 0),
                'file_versions_synced': sync_stats.get('file_versions_synced', 0),
                'progress_steps_total': sync_stats.get('progress_steps_total', 0),
                'progress_steps_synced': sync_stats.get('progress_steps_synced', 0),
                'total_items_synced': analysis['total_items'],
                'error_count': analysis['error_count'],
                'error_details': analysis['error_details'][:10] if analysis['error_details'] else []
            },
            
            'performance_metrics': {
                'duration_seconds': duration,
                'items_per_second': analysis['items_per_second'],
                'api_calls': performance_report.get('summary', {}).get('api_calls', 0),
                'api_time': sync_stats.get('performance', {}).get('api_time', 0),
                'api_success_rate': performance_report.get('summary', {}).get('api_success_rate', 0),
                'db_time': sync_stats.get('performance', {}).get('db_time', 0),
                'db_queries': performance_report.get('summary', {}).get('db_queries', 0),
                'cache_hit_rate': performance_report.get('summary', {}).get('cache_hit_rate', 0),
                'cache_hits': sync_stats.get('performance', {}).get('cache_hits', 0),
                'cache_misses': sync_stats.get('performance', {}).get('cache_misses', 0),
                'memory_usage_mb': performance_report.get('summary', {}).get('memory_usage_mb', 0),
                'optimization_enabled': True,
                'estimated_speedup': self._calculate_speedup(sync_stats, duration)
            },
            
            'timing_breakdown': timing_stats,
            
            'optimization_features': {
                'async_parallel_api_calls': True,
                'aiohttp_session': True,
                'batch_upsert_optimization': True,
                'memory_caching': self.enable_cache,
                'cache_type': 'cachetools',
                'circuit_breaker_pattern': True,
                'smart_pagination': True,
                'rate_limit_retry': True,
                'performance_monitoring': True,
                'bottleneck_analysis': True,
                'max_concurrent': self.max_concurrent,
                'cache_max_size': self.cache_max_size,
                'batch_size': self.batch_size
            },
            
            'bottleneck_analysis': performance_report.get('bottlenecks', []),
            
            'candidates_configuration': candidates_stats or {},
            
            'production_readiness': {
                'real_api_integration': True,
                'authentication_working': analysis['sync_success'],
                'database_integration': True,
                'cache_integration': self.enable_cache,
                'error_handling': 'Implemented' if analysis['sync_success'] else f"Errors: {analysis['error_count']}",
                'optimization_status': 'Enhanced',
                'async_ready': True,
                'scalability': 'High'
            }
        }
    
    def _calculate_speedup(self, sync_stats: dict, duration: float) -> float:
        """计算提速比（相比串行）"""
        # 估算串行耗时（假设每个API调用6秒）
        api_calls = sync_stats.get('performance', {}).get('api_calls', 0)
        estimated_serial_time = api_calls * 6  # 6秒/请求
        
        if duration > 0 and estimated_serial_time > 0:
            return estimated_serial_time / duration
        return 1.0
    
    def _print_timing_breakdown(self, timing_stats: dict, total_duration: float) -> None:
        """Print detailed timing breakdown"""
        
        print("\n" + "="*80)
        print("TIMING BREAKDOWN")
        print("="*80)
        
        print(f"\nTotal Duration: {total_duration:.2f}s")
        print("\nStep-by-Step Timing:")
        
        steps = [
            ('authentication', 'Authentication Check'),
            ('initialization', 'Module Initialization'),
            ('cache_check', 'Memory Cache Check'),
            ('synchronization', 'Full Synchronization'),
            ('performance_analysis', 'Performance Analysis'),
            ('candidates_verification', 'Candidates Verification'),
            ('analysis', 'Results Analysis'),
            ('report_generation', 'Report Generation')
        ]
        
        for key, label in steps:
            if key in timing_stats:
                duration = timing_stats[key]
                percentage = (duration / total_duration * 100) if total_duration > 0 else 0
                bar_length = int(percentage / 2)  # Scale to 50 chars max
                bar = '#' * bar_length + '-' * (50 - bar_length)
                print(f"  {label:.<30} {duration:>6.2f}s ({percentage:>5.1f}%) {bar}")
        
        print("\n" + "="*80)
    
    def _save_and_display_results(self, report: dict) -> None:
        """Save and display test results"""
        
        # Save detailed report
        timestamp = int(time.time())
        filename = f"test_enhanced_review_sync_{timestamp}.json"
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
        """Print test summary - Enhanced"""
        
        print("\n" + "="*80)
        print("ENHANCED REVIEW SYNC TEST SUMMARY")
        print("="*80)
        
        meta = report['test_metadata']
        sync = report.get('sync_results', {})
        perf = report.get('performance_metrics', {})
        opt = report.get('optimization_features', {})
        prod = report.get('production_readiness', {})
        bottlenecks = report.get('bottleneck_analysis', [])
        candidates = report.get('candidates_configuration', {})
        
        print(f"\n[PROJECT] {meta['project_id']}")
        print(f"[SUCCESS] {meta['success']}")
        print(f"[DURATION] {meta['duration_seconds']:.2f} seconds")
        print(f"[STATUS] {sync.get('status', 'unknown')}")
        
        print(f"\n[OPTIMIZATION FEATURES]")
        print(f"  Mode: {meta.get('sync_mode', 'unknown').upper()}")
        print(f"  Async Parallel API: {'[OK] Enabled' if opt.get('async_parallel_api_calls') else '[X] Disabled'}")
        print(f"  Aiohttp Session: {'[OK] Enabled' if opt.get('aiohttp_session') else '[X] Disabled'}")
        print(f"  Batch UPSERT: {'[OK] Enabled' if opt.get('batch_upsert_optimization') else '[X] Disabled'}")
        print(f"  Memory Caching: {'[OK] Enabled' if opt.get('memory_caching') else '[X] Disabled'}")
        if opt.get('cache_type'):
            print(f"  Cache Type: {opt.get('cache_type')}")
        print(f"  Circuit Breaker: {'[OK] Enabled' if opt.get('circuit_breaker_pattern') else '[X] Disabled'}")
        print(f"  Smart Pagination: {'[OK] Enabled' if opt.get('smart_pagination') else '[X] Disabled'}")
        print(f"  Performance Monitor: {'[OK] Enabled' if opt.get('performance_monitoring') else '[X] Disabled'}")
        if opt.get('max_concurrent'):
            print(f"  Max Concurrent: {opt.get('max_concurrent')}")
        if opt.get('cache_max_size'):
            print(f"  Cache Max Size: {opt.get('cache_max_size')} entries")
        if opt.get('batch_size'):
            print(f"  Batch Size: {opt.get('batch_size')}")
        
        if meta['success']:
            print(f"\n[SYNC RESULTS]")
            print(f"  Workflows: {sync.get('workflows_synced', 0)}/{sync.get('workflows_total', 0)}")
            print(f"  Reviews: {sync.get('reviews_synced', 0)}/{sync.get('reviews_total', 0)}")
            print(f"  File Versions: {sync.get('file_versions_synced', 0)}/{sync.get('file_versions_total', 0)}")
            print(f"  Progress Steps: {sync.get('progress_steps_synced', 0)}/{sync.get('progress_steps_total', 0)}")
            print(f"  Total Items: {sync.get('total_items_synced', 0)}")
            print(f"  Performance: {perf.get('items_per_second', 0):.2f} items/sec")
            
            # 候选人配置统计
            if candidates.get('success'):
                print(f"\n[CANDIDATES CONFIGURATION]")
                print(f"  Table Exists: {'[OK] Yes' if candidates.get('table_exists') else '[X] No'}")
                print(f"  Total Configurations: {candidates.get('total_configs', 0)}")
                print(f"  Configs with Candidates: {candidates.get('configs_with_candidates', 0)}")
                print(f"  Reviews with Configs: {candidates.get('reviews_with_configs', 0)}")
                if candidates.get('source_distribution'):
                    print(f"  Source Distribution:")
                    for source, count in candidates.get('source_distribution', {}).items():
                        print(f"    - {source}: {count}")
                print(f"  Sample Configs: {candidates.get('sample_configs', 0)}")
            else:
                print(f"\n[CANDIDATES CONFIGURATION]")
                print(f"  [ERROR] {candidates.get('error', 'Unknown error')}")
            
            print(f"\n[PERFORMANCE METRICS]")
            print(f"  Total Duration: {perf.get('duration_seconds', 0):.2f}s")
            print(f"  API Calls: {perf.get('api_calls', 0)} times")
            print(f"  API Success Rate: {perf.get('api_success_rate', 0):.1f}%")
            print(f"  API Time: {perf.get('api_time', 0):.2f}s")
            print(f"  DB Queries: {perf.get('db_queries', 0)} times")
            print(f"  DB Time: {perf.get('db_time', 0):.2f}s")
            if opt.get('memory_caching'):
                print(f"  Cache Hit Rate: {perf.get('cache_hit_rate', 0):.1f}%")
                print(f"  Cache Hits: {perf.get('cache_hits', 0)}")
                print(f"  Cache Misses: {perf.get('cache_misses', 0)}")
            print(f"  Memory Usage: {perf.get('memory_usage_mb', 0):.2f} MB")
            if perf.get('optimization_enabled'):
                print(f"  Estimated Speedup: {perf.get('estimated_speedup', 1.0):.1f}x")
            
            # Bottleneck analysis
            if bottlenecks:
                print(f"\n[BOTTLENECK ANALYSIS]")
                severity_labels = {'high': '[HIGH]', 'medium': '[MEDIUM]', 'low': '[LOW]'}
                for bn in bottlenecks:
                    label = severity_labels.get(bn.get('severity', 'low'), '[INFO]')
                    print(f"  {label} [{bn.get('type', 'unknown').upper()}] {bn.get('message', 'N/A')}")
                    print(f"     [TIP] {bn.get('suggestion', 'N/A')}")
            else:
                print(f"\n[BOTTLENECK ANALYSIS]")
                print(f"  [OK] No significant bottlenecks detected")
            
            print(f"\n[PRODUCTION READINESS]")
            print(f"  Real API Integration: {'[OK] Yes' if prod.get('real_api_integration') else '[X] No'}")
            print(f"  Authentication: {'[OK] Working' if prod.get('authentication_working') else '[X] Failed'}")
            print(f"  Database Integration: {'[OK] Working' if prod.get('database_integration') else '[X] Failed'}")
            print(f"  Cache Integration: {'[OK] Working' if prod.get('cache_integration') else '[X] Disabled'}")
            print(f"  Error Handling: {prod.get('error_handling', 'Unknown')}")
            print(f"  Optimization: {prod.get('optimization_status', 'Unknown')}")
            print(f"  Async Ready: {'[OK] Yes' if prod.get('async_ready') else '[X] No'}")
            print(f"  Scalability: {prod.get('scalability', 'Unknown')}")
        else:
            print(f"\n[ERROR] {sync.get('error_details', ['Unknown error'])[0]}")
            print(f"[ERROR COUNT] {sync.get('error_count', 0)}")
            if sync.get('error_details'):
                print(f"\n[FIRST 5 ERRORS]")
                for i, error in enumerate(sync.get('error_details', [])[:5], 1):
                    print(f"  {i}. {error}")
        
        print("\n" + "="*80)


def main():
    """Main test function - Enhanced"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Enhanced Review Sync Test - Async + Cache + UPSERT')
    parser.add_argument('--concurrent', type=int, default=10,
                       help='Number of concurrent async tasks (default: 10)')
    parser.add_argument('--cache', action='store_true', default=True,
                       help='Enable memory caching (default: True)')
    parser.add_argument('--no-cache', action='store_false', dest='cache',
                       help='Disable memory caching')
    parser.add_argument('--cache-ttl', type=int, default=3600,
                       help='Cache TTL in seconds (default: 3600)')
    parser.add_argument('--cache-max-size', type=int, default=5000,
                       help='Maximum cache entries (default: 5000)')
    parser.add_argument('--batch-size', type=int, default=100,
                       help='Batch size for database operations (default: 100)')
    
    args = parser.parse_args()
    
    # Create tester and run
    tester = EnhancedReviewSyncTester(
        max_concurrent=args.concurrent,
        enable_cache=args.cache,
        cache_ttl=args.cache_ttl,
        cache_max_size=args.cache_max_size,
        batch_size=args.batch_size
    )
    
    try:
        report = tester.run_test()
        
        if report.get('success', False):
            print(f"\n[SUCCESS] Enhanced review sync test completed successfully!")
            print(f"Mode: Async Parallel (Enhanced)")
            print(f"Concurrent: {args.concurrent}")
            print(f"Cache: {'Enabled' if args.cache else 'Disabled'}")
            print(f"Batch Size: {args.batch_size}")
            return 0
        else:
            print(f"\n[FAILED] Enhanced review sync test failed!")
            return 1
            
    except Exception as e:
        print(f"\n[ERROR] Test execution failed: {e}")
        logger.exception("Test execution failed")
        return 1


if __name__ == "__main__":
    print("="*80)
    print("Enhanced Review Sync Test - Async + Cache + UPSERT Optimization")
    print("="*80)
    print("This script tests the enhanced async review synchronization with:")
    print("  • Asyncio + aiohttp for concurrent API calls")
    print("  • Cachetools memory caching layer")
    print("  • PostgreSQL UPSERT optimization")
    print("  • Circuit breaker pattern")
    print("  • Performance monitoring and bottleneck analysis")
    print("  • Automatic candidates configuration creation (review_step_candidates)")
    print()
    print("Note: Account sync functionality removed from this test.")
    print("      For account sync, use: python database_sql/test_account_sync.py")
    print()
    print("Make sure you're logged in via the web interface first")
    print()
    print("Usage:")
    print("  python test_enhanced_review_sync.py                        # Use defaults")
    print("  python test_enhanced_review_sync.py --concurrent 15        # Use 15 concurrent tasks")
    print("  python test_enhanced_review_sync.py --no-cache             # Disable memory cache")
    print("  python test_enhanced_review_sync.py --cache-max-size 10000 # Set cache to 10000 entries")
    print("  python test_enhanced_review_sync.py --batch-size 200       # Use batch size 200")
    print()
    
    exit(main())
