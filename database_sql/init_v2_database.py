#!/usr/bin/env python3
"""
V2数据库初始化脚本
自动创建V2架构并执行必要的迁移
"""

import asyncio
import logging
import sys
import os
from typing import Dict, Any

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class V2DatabaseInitializer:
    """V2数据库初始化器"""
    
    def __init__(self):
        # Add project root to path for imports
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.join(current_dir, '..')
        if self.project_root not in sys.path:
            sys.path.insert(0, self.project_root)
        
        self.schema_v2_path = os.path.join(current_dir, 'final_v2_init.sql')
        self.migration_path = os.path.join(current_dir, 'migration_to_v2.sql')
        self.data_fix_path = os.path.join(current_dir, 'data_fix_scripts.sql')
    
    async def initialize_v2_database(self, force_recreate: bool = False) -> Dict[str, Any]:
        """初始化V2数据库"""
        
        logger.info("="*80)
        logger.info("V2 DATABASE INITIALIZATION")
        logger.info("="*80)
        
        try:
            # 1. 获取数据库连接
            logger.info("[STEP 1] Connecting to database...")
            
            from database_sql.optimized_data_access import get_optimized_postgresql_dal
            dal = await get_optimized_postgresql_dal()
            
            async with dal.get_connection() as conn:
                
                # 2. 检查当前架构版本
                logger.info("[STEP 2] Checking current database schema...")
                
                current_version = await self._detect_schema_version(conn)
                logger.info(f"[STEP 2] Current schema version: {current_version}")
                
                # 3. 决定初始化策略
                if current_version == "v2" and not force_recreate:
                    logger.info("[STEP 3] V2 schema already exists, skipping initialization")
                    return {
                        'success': True,
                        'action': 'skipped',
                        'message': 'V2 schema already exists',
                        'schema_version': 'v2'
                    }
                
                elif current_version == "v1" or current_version == "unknown" or force_recreate:
                    logger.info("[STEP 3] Creating V2 schema with clean initialization...")
                    result = await self._recreate_v2_schema(conn)
                
                else:
                    raise Exception(f"Unknown schema version: {current_version}")
                
                # 4. 验证V2架构
                logger.info("[STEP 4] Validating V2 schema...")
                validation_result = await self._validate_v2_schema(conn)
                
                if not validation_result['valid']:
                    raise Exception(f"V2 schema validation failed: {validation_result['errors']}")
                
                # 5. 执行数据修复
                logger.info("[STEP 5] Executing data fixes...")
                fix_result = await self._execute_data_fixes(conn)
                
                return {
                    'success': True,
                    'action': result.get('action', 'migrated'),
                    'schema_version': 'v2',
                    'validation': validation_result,
                    'data_fixes': fix_result,
                    'message': 'V2 database initialization completed successfully'
                }
                
        except Exception as e:
            logger.error(f"V2 database initialization failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'schema_version': 'unknown'
            }
    
    async def _detect_schema_version(self, conn) -> str:
        """检测当前数据库架构版本"""
        
        try:
            # 检查V2特有的字段
            v2_checks = [
                # 文件表是否缺少版本字段
                "SELECT column_name FROM information_schema.columns WHERE table_name = 'files' AND column_name = 'current_version_id'",
                # 文件版本表是否有当前版本标记
                "SELECT column_name FROM information_schema.columns WHERE table_name = 'file_versions' AND column_name = 'is_current_version'",
                # 自定义属性定义表是否有作用域字段
                "SELECT column_name FROM information_schema.columns WHERE table_name = 'custom_attribute_definitions' AND column_name = 'scope_type'",
                # 自定义属性值表是否有定义ID字段
                "SELECT column_name FROM information_schema.columns WHERE table_name = 'custom_attribute_values' AND column_name = 'attr_definition_id'"
            ]
            
            v2_indicators = 0
            
            # 检查文件表是否删除了版本字段 (V2特征)
            result = await conn.fetchrow(v2_checks[0])
            if not result:  # 没有current_version_id字段说明是V2
                v2_indicators += 1
            
            # 检查其他V2字段
            for check_query in v2_checks[1:]:
                result = await conn.fetchrow(check_query)
                if result:  # 有这些字段说明是V2
                    v2_indicators += 1
            
            # 检查基础表是否存在
            tables_query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
              AND table_name IN ('files', 'file_versions', 'folders', 'projects')
            """
            
            tables = await conn.fetch(tables_query)
            
            if len(tables) < 4:
                return "unknown"  # 基础表都不存在
            elif v2_indicators >= 3:
                return "v2"  # 大部分V2特征都存在
            else:
                return "v1"  # 基础表存在但缺少V2特征
                
        except Exception as e:
            logger.error(f"Schema version detection failed: {e}")
            return "unknown"
    
    async def _migrate_v1_to_v2(self, conn) -> Dict[str, Any]:
        """从V1迁移到V2"""
        
        try:
            logger.info("Executing V1 to V2 migration...")
            
            # 读取迁移脚本
            if not os.path.exists(self.migration_path):
                raise Exception(f"Migration script not found: {self.migration_path}")
            
            with open(self.migration_path, 'r', encoding='utf-8') as f:
                migration_sql = f.read()
            
            # 执行迁移脚本
            await conn.execute(migration_sql)
            
            logger.info("V1 to V2 migration completed successfully")
            
            return {
                'action': 'migrated',
                'from_version': 'v1',
                'to_version': 'v2'
            }
            
        except Exception as e:
            logger.error(f"Migration failed: {e}")
            raise Exception(f"V1 to V2 migration failed: {e}")
    
    async def _recreate_v2_schema(self, conn) -> Dict[str, Any]:
        """重新创建V2架构"""
        
        try:
            logger.info("Creating V2 schema with clean initialization...")
            
            # 读取清洁初始化脚本（包含删除和重建逻辑）
            if not os.path.exists(self.schema_v2_path):
                raise Exception(f"V2 clean init script not found: {self.schema_v2_path}")
            
            with open(self.schema_v2_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            
            # 执行清洁初始化脚本
            await conn.execute(schema_sql)
            
            logger.info("V2 clean initialization completed successfully")
            
            return {
                'action': 'recreated',
                'schema_version': 'v2'
            }
            
        except Exception as e:
            logger.error(f"Schema recreation failed: {e}")
            raise Exception(f"V2 schema recreation failed: {e}")
    
    async def _validate_v2_schema(self, conn) -> Dict[str, Any]:
        """验证V2架构"""
        
        try:
            validation_errors = []
            
            # 1. 检查必需的表
            required_tables = ['projects', 'folders', 'files', 'file_versions', 
                             'custom_attribute_definitions', 'custom_attribute_values', 
                             'sync_tasks', 'module_relations']
            
            tables_query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = ANY($1)
            """
            
            existing_tables = await conn.fetch(tables_query, required_tables)
            existing_table_names = [t['table_name'] for t in existing_tables]
            
            missing_tables = set(required_tables) - set(existing_table_names)
            if missing_tables:
                validation_errors.append(f"Missing tables: {missing_tables}")
            
            # 2. 检查V2特有字段
            v2_field_checks = [
                ("file_versions", "is_current_version"),
                ("custom_attribute_definitions", "scope_type"),
                ("custom_attribute_values", "attr_definition_id"),
                ("files", "folder_path")  # 应该存在
            ]
            
            for table_name, column_name in v2_field_checks:
                column_query = """
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = $1 AND column_name = $2
                """
                
                result = await conn.fetchrow(column_query, table_name, column_name)
                if not result:
                    validation_errors.append(f"Missing V2 field: {table_name}.{column_name}")
            
            # 3. 检查V2不应该存在的字段
            v2_removed_fields = [
                ("files", "current_version_id"),
                ("files", "version_number"),
                ("files", "storage_urn")
            ]
            
            for table_name, column_name in v2_removed_fields:
                column_query = """
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = $1 AND column_name = $2
                """
                
                result = await conn.fetchrow(column_query, table_name, column_name)
                if result:
                    validation_errors.append(f"V2 should not have field: {table_name}.{column_name}")
            
            # 4. 检查视图
            required_views = ['files_with_current_version', 'file_applicable_attributes']
            
            views_query = """
            SELECT table_name 
            FROM information_schema.views 
            WHERE table_schema = 'public' AND table_name = ANY($1)
            """
            
            existing_views = await conn.fetch(views_query, required_views)
            existing_view_names = [v['table_name'] for v in existing_views]
            
            missing_views = set(required_views) - set(existing_view_names)
            if missing_views:
                validation_errors.append(f"Missing views: {missing_views}")
            
            return {
                'valid': len(validation_errors) == 0,
                'errors': validation_errors,
                'tables_found': len(existing_table_names),
                'views_found': len(existing_view_names)
            }
            
        except Exception as e:
            logger.error(f"Schema validation failed: {e}")
            return {
                'valid': False,
                'errors': [f"Validation error: {e}"]
            }
    
    async def _execute_data_fixes(self, conn) -> Dict[str, Any]:
        """执行数据修复"""
        
        try:
            logger.info("Executing data fixes...")
            
            # 简单的数据修复 (不执行完整的修复脚本，避免复杂性)
            fixes_executed = []
            
            # 1. 确保文件路径不为空
            path_fix_query = """
            UPDATE files 
            SET folder_path = COALESCE(folder_path, ''),
                full_path = COALESCE(full_path, name)
            WHERE folder_path IS NULL OR full_path IS NULL OR full_path = ''
            """
            
            result = await conn.execute(path_fix_query)
            fixes_executed.append(f"Fixed file paths: {result}")
            
            # 2. 确保文件版本有当前版本标记
            version_fix_query = """
            WITH max_versions AS (
                SELECT file_id, MAX(version_number) as max_version
                FROM file_versions
                GROUP BY file_id
            )
            UPDATE file_versions fv
            SET is_current_version = true
            FROM max_versions mv
            WHERE fv.file_id = mv.file_id 
              AND fv.version_number = mv.max_version
              AND fv.is_current_version = false
            """
            
            result = await conn.execute(version_fix_query)
            fixes_executed.append(f"Fixed current version flags: {result}")
            
            return {
                'success': True,
                'fixes_executed': fixes_executed
            }
            
        except Exception as e:
            logger.error(f"Data fixes failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }

async def main():
    """主函数"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Initialize V2 Database')
    parser.add_argument('--force', action='store_true', help='Force recreate schema even if V2 exists')
    parser.add_argument('--check-only', action='store_true', help='Only check current schema version')
    
    args = parser.parse_args()
    
    initializer = V2DatabaseInitializer()
    
    try:
        if args.check_only:
            # 只检查版本
            from database_sql.optimized_data_access import get_optimized_postgresql_dal
            dal = await get_optimized_postgresql_dal()
            
            async with dal.get_connection() as conn:
                version = await initializer._detect_schema_version(conn)
                print(f"Current database schema version: {version}")
                return 0
        
        # 执行初始化
        result = await initializer.initialize_v2_database(force_recreate=args.force)
        
        if result['success']:
            print(f"V2 Database initialization successful!")
            print(f"   Action: {result.get('action', 'unknown')}")
            print(f"   Schema Version: {result.get('schema_version', 'unknown')}")
            
            validation = result.get('validation', {})
            if validation:
                print(f"   Tables: {validation.get('tables_found', 0)}")
                print(f"   Views: {validation.get('views_found', 0)}")
            
            return 0
        else:
            print(f"V2 Database initialization failed!")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            return 1
            
    except Exception as e:
        print(f"Initialization failed: {e}")
        logger.exception("Initialization failed")
        return 1

if __name__ == "__main__":
    print("V2 Database Initializer")
    print("This script will set up the optimized V2 database schema")
    print()
    
    exit(asyncio.run(main()))
