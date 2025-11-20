#!/usr/bin/env python3
"""
V2数据库分步初始化脚本
将复杂的SQL脚本分解为多个步骤执行，避免语法错误
"""

import asyncio
import sys
import os
sys.path.append('.')
from database_sql.optimized_data_access import get_optimized_postgresql_dal

class V2DatabaseStepByStepInitializer:
    def __init__(self):
        self.dal = None
        
    async def initialize(self):
        """分步初始化V2数据库"""
        self.dal = await get_optimized_postgresql_dal()
        
        steps = [
            ("Create Extensions", self.step_1_extensions),
            ("Cleanup Existing Objects", self.step_2_cleanup),
            ("Create Functions", self.step_3_functions),
            ("Create Basic Tables", self.step_4_basic_tables),
            ("Create Related Tables", self.step_5_related_tables),
            ("Add Foreign Keys", self.step_6_foreign_keys),
            ("Add Unique Constraints", self.step_7_unique_constraints),
            ("Create Views", self.step_8_views),
            ("Create Triggers", self.step_9_triggers),
            ("Create Indexes", self.step_10_indexes)
        ]
        
        async with self.dal.get_connection() as conn:
            for step_name, step_func in steps:
                try:
                    print(f"Executing step: {step_name}...")
                    await step_func(conn)
                    print(f"OK: {step_name} completed")
                except Exception as e:
                    print(f"ERROR: {step_name} failed: {e}")
                    raise e
        
        print("SUCCESS: V2 database initialization completed!")
        
    async def step_1_extensions(self, conn):
        """步骤1: 创建扩展"""
        await conn.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
        await conn.execute('CREATE EXTENSION IF NOT EXISTS "btree_gin"')
        
    async def step_2_cleanup(self, conn):
        """步骤2: 清理现有对象"""
        cleanup_sql = [
            "DROP TABLE IF EXISTS custom_attribute_values CASCADE",
            "DROP TABLE IF EXISTS custom_attribute_definitions CASCADE",
            "DROP TABLE IF EXISTS file_versions CASCADE",
            "DROP TABLE IF EXISTS files CASCADE",
            "DROP TABLE IF EXISTS folders CASCADE",
            "DROP TABLE IF EXISTS sync_tasks CASCADE",
            "DROP TABLE IF EXISTS module_relations CASCADE",
            "DROP TABLE IF EXISTS projects CASCADE",
            "DROP VIEW IF EXISTS files_with_current_version CASCADE",
            "DROP VIEW IF EXISTS file_applicable_attributes CASCADE",
            "DROP FUNCTION IF EXISTS manage_current_version() CASCADE",
            "DROP FUNCTION IF EXISTS update_updated_at_column() CASCADE"
        ]
        
        for sql in cleanup_sql:
            await conn.execute(sql)
            
    async def step_3_functions(self, conn):
        """步骤3: 创建函数"""
        await conn.execute("""
            CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS $func$
            BEGIN
                NEW.updated_at = CURRENT_TIMESTAMP;
                RETURN NEW;
            END;
            $func$ LANGUAGE plpgsql
        """)
        
    async def step_4_basic_tables(self, conn):
        """步骤4: 创建基础表"""
        
        # Projects table
        await conn.execute("""
            CREATE TABLE projects (
                id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(500) NOT NULL,
                description TEXT,
                hub_id VARCHAR(255),
                account_id VARCHAR(255),
                status VARCHAR(50) DEFAULT 'active',
                last_sync_time TIMESTAMP WITH TIME ZONE,
                last_full_sync_time TIMESTAMP WITH TIME ZONE,
                sync_status VARCHAR(50) DEFAULT 'never_synced',
                sync_stats JSONB DEFAULT '{}',
                statistics JSONB DEFAULT '{}',
                metadata JSONB DEFAULT '{}',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Folders table
        await conn.execute("""
            CREATE TABLE folders (
                id VARCHAR(500) PRIMARY KEY,
                project_id VARCHAR(255) NOT NULL,
                name VARCHAR(500) NOT NULL,
                display_name VARCHAR(500),
                parent_id VARCHAR(500),
                path TEXT NOT NULL,
                path_segments TEXT[] DEFAULT '{}',
                depth INTEGER DEFAULT 0,
                create_time TIMESTAMP WITH TIME ZONE,
                create_user_id VARCHAR(100),
                create_user_name VARCHAR(200),
                last_modified_time TIMESTAMP WITH TIME ZONE,
                last_modified_user_id VARCHAR(100),
                last_modified_user_name VARCHAR(200),
                last_modified_time_rollup TIMESTAMP WITH TIME ZONE,
                object_count INTEGER DEFAULT 0,
                total_object_count INTEGER DEFAULT 0,
                total_file_size BIGINT DEFAULT 0,
                hidden BOOLEAN DEFAULT FALSE,
                metadata JSONB DEFAULT '{}',
                folder_permissions JSONB DEFAULT '{}',
                folder_settings JSONB DEFAULT '{}',
                sync_info JSONB DEFAULT '{}',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Files table
        await conn.execute("""
            CREATE TABLE files (
                id VARCHAR(500) PRIMARY KEY,
                project_id VARCHAR(255) NOT NULL,
                name VARCHAR(500) NOT NULL,
                display_name VARCHAR(500),
                parent_folder_id VARCHAR(500),
                folder_path TEXT NOT NULL DEFAULT '',
                full_path TEXT NOT NULL,
                path_segments TEXT[] DEFAULT '{}',
                depth INTEGER DEFAULT 0,
                create_time TIMESTAMP WITH TIME ZONE,
                create_user_id VARCHAR(100),
                create_user_name VARCHAR(200),
                last_modified_time TIMESTAMP WITH TIME ZONE,
                last_modified_user_id VARCHAR(100),
                last_modified_user_name VARCHAR(200),
                file_type VARCHAR(50),
                mime_type VARCHAR(100),
                reserved BOOLEAN DEFAULT FALSE,
                hidden BOOLEAN DEFAULT FALSE,
                metadata JSONB DEFAULT '{}',
                file_permissions JSONB DEFAULT '{}',
                file_settings JSONB DEFAULT '{}',
                review_info JSONB DEFAULT '{}',
                sync_info JSONB DEFAULT '{}',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
    async def step_5_related_tables(self, conn):
        """步骤5: 创建关联表"""
        
        # File versions table
        await conn.execute("""
            CREATE TABLE file_versions (
                id VARCHAR(500) PRIMARY KEY,
                file_id VARCHAR(500) NOT NULL,
                project_id VARCHAR(255) NOT NULL,
                version_number INTEGER NOT NULL,
                urn VARCHAR(500) UNIQUE NOT NULL,
                item_urn VARCHAR(500),
                storage_urn VARCHAR(500),
                lineage_urn VARCHAR(500),
                create_time TIMESTAMP WITH TIME ZONE,
                create_user_id VARCHAR(100),
                create_user_name VARCHAR(200),
                last_modified_time TIMESTAMP WITH TIME ZONE,
                last_modified_user_id VARCHAR(100),
                last_modified_user_name VARCHAR(200),
                file_size BIGINT DEFAULT 0,
                storage_size BIGINT DEFAULT 0,
                mime_type VARCHAR(100),
                process_state VARCHAR(50),
                is_current_version BOOLEAN DEFAULT FALSE,
                version_status VARCHAR(20) DEFAULT 'active',
                metadata JSONB DEFAULT '{}',
                review_info JSONB DEFAULT '{}',
                extension JSONB DEFAULT '{}',
                download_info JSONB DEFAULT '{}',
                download_url TEXT,
                sync_info JSONB DEFAULT '{}',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Custom attribute definitions table
        await conn.execute("""
            CREATE TABLE custom_attribute_definitions (
                id SERIAL PRIMARY KEY,
                attr_id INTEGER NOT NULL,
                project_id VARCHAR(255) NOT NULL,
                scope_type VARCHAR(20) NOT NULL DEFAULT 'project',
                scope_folder_id VARCHAR(500),
                inherit_to_subfolders BOOLEAN DEFAULT TRUE,
                name VARCHAR(200) NOT NULL,
                type VARCHAR(50) NOT NULL,
                array_values JSONB,
                description TEXT,
                is_required BOOLEAN DEFAULT FALSE,
                default_value TEXT,
                validation_rules JSONB DEFAULT '{}',
                sync_info JSONB DEFAULT '{}',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Custom attribute values table
        await conn.execute("""
            CREATE TABLE custom_attribute_values (
                id SERIAL PRIMARY KEY,
                file_id VARCHAR(500) NOT NULL,
                attr_definition_id INTEGER NOT NULL,
                project_id VARCHAR(255) NOT NULL,
                value TEXT,
                value_date TIMESTAMP WITH TIME ZONE,
                value_number DECIMAL(15,4),
                value_boolean BOOLEAN,
                value_array JSONB,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_by_user_id VARCHAR(100),
                updated_by_user_name VARCHAR(200),
                validation_status VARCHAR(20) DEFAULT 'valid',
                validation_errors JSONB DEFAULT '[]',
                sync_info JSONB DEFAULT '{}',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Sync tasks table
        await conn.execute("""
            CREATE TABLE sync_tasks (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                project_id VARCHAR(255) NOT NULL,
                task_type VARCHAR(50) NOT NULL,
                status VARCHAR(50) NOT NULL DEFAULT 'pending',
                config JSONB DEFAULT '{}',
                started_at TIMESTAMP WITH TIME ZONE,
                completed_at TIMESTAMP WITH TIME ZONE,
                duration_seconds INTEGER,
                result JSONB DEFAULT '{}',
                error_info JSONB DEFAULT '{}',
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Module relations table
        await conn.execute("""
            CREATE TABLE module_relations (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                subject_type VARCHAR(50) NOT NULL,
                subject_id VARCHAR(500) NOT NULL,
                module_type VARCHAR(50) NOT NULL,
                module_id VARCHAR(500) NOT NULL,
                relation_type VARCHAR(50) NOT NULL,
                status VARCHAR(50) DEFAULT 'active',
                relation_data JSONB DEFAULT '{}',
                project_id VARCHAR(255) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
    async def step_6_foreign_keys(self, conn):
        """步骤6: 添加外键约束"""
        foreign_keys = [
            "ALTER TABLE folders ADD CONSTRAINT fk_folders_project FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE",
            "ALTER TABLE files ADD CONSTRAINT fk_files_project FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE",
            "ALTER TABLE files ADD CONSTRAINT fk_files_folder FOREIGN KEY (parent_folder_id) REFERENCES folders(id) ON DELETE SET NULL",
            "ALTER TABLE file_versions ADD CONSTRAINT fk_versions_file FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE",
            "ALTER TABLE file_versions ADD CONSTRAINT fk_versions_project FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE",
            "ALTER TABLE custom_attribute_definitions ADD CONSTRAINT fk_attr_def_project FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE",
            "ALTER TABLE custom_attribute_definitions ADD CONSTRAINT fk_attr_def_folder FOREIGN KEY (scope_folder_id) REFERENCES folders(id) ON DELETE CASCADE",
            "ALTER TABLE custom_attribute_values ADD CONSTRAINT fk_attr_val_file FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE",
            "ALTER TABLE custom_attribute_values ADD CONSTRAINT fk_attr_val_def FOREIGN KEY (attr_definition_id) REFERENCES custom_attribute_definitions(id) ON DELETE CASCADE",
            "ALTER TABLE custom_attribute_values ADD CONSTRAINT fk_attr_val_project FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE",
            "ALTER TABLE sync_tasks ADD CONSTRAINT fk_sync_project FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE",
            "ALTER TABLE module_relations ADD CONSTRAINT fk_module_project FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE"
        ]
        
        for fk_sql in foreign_keys:
            await conn.execute(fk_sql)
            
    async def step_7_unique_constraints(self, conn):
        """步骤7: 添加唯一约束"""
        unique_constraints = [
            "ALTER TABLE file_versions ADD CONSTRAINT uk_file_version UNIQUE (file_id, version_number)",
            "ALTER TABLE custom_attribute_values ADD CONSTRAINT uk_attr_value UNIQUE (file_id, attr_definition_id)",
            "ALTER TABLE module_relations ADD CONSTRAINT uk_module_relation UNIQUE (subject_type, subject_id, module_type, module_id, relation_type)"
        ]
        
        # Handle the complex constraint separately
        await conn.execute("""
            CREATE UNIQUE INDEX uk_attr_def_idx ON custom_attribute_definitions 
            (attr_id, project_id, COALESCE(scope_folder_id, ''))
        """)
        
        for uk_sql in unique_constraints:
            await conn.execute(uk_sql)
            
    async def step_8_views(self, conn):
        """步骤8: 创建视图"""
        
        # Files with current version view
        await conn.execute("""
            CREATE VIEW files_with_current_version AS
            SELECT 
                f.*,
                fv.version_number as current_version_number,
                fv.file_size as current_file_size,
                fv.storage_size as current_storage_size,
                fv.storage_urn as current_storage_urn,
                fv.download_url as current_download_url,
                fv.process_state as current_process_state,
                fv.mime_type as current_mime_type,
                fv.create_time as version_create_time,
                fv.create_user_id as version_create_user_id,
                fv.create_user_name as version_create_user_name,
                fv.review_info as current_review_info
            FROM files f
            LEFT JOIN file_versions fv ON f.id = fv.file_id AND fv.is_current_version = true
        """)
        
        # File applicable attributes view
        await conn.execute("""
            CREATE VIEW file_applicable_attributes AS
            SELECT DISTINCT
                f.id as file_id,
                cad.id as attr_definition_id,
                cad.attr_id,
                cad.name as attr_name,
                cad.type as attr_type,
                cad.is_required,
                cad.default_value,
                cad.scope_type,
                cad.scope_folder_id
            FROM files f
            JOIN custom_attribute_definitions cad ON cad.project_id = f.project_id AND cad.scope_type = 'project'
        """)
        
    async def step_9_triggers(self, conn):
        """步骤9: 创建触发器"""
        
        # Version management trigger function
        await conn.execute("""
            CREATE OR REPLACE FUNCTION manage_current_version()
            RETURNS TRIGGER AS $func$
            BEGIN
                IF TG_OP = 'INSERT' THEN
                    IF NEW.version_number >= (
                        SELECT COALESCE(MAX(version_number), 0) 
                        FROM file_versions 
                        WHERE file_id = NEW.file_id
                    ) THEN
                        UPDATE file_versions 
                        SET is_current_version = false 
                        WHERE file_id = NEW.file_id AND id != NEW.id;
                        
                        NEW.is_current_version = true;
                    END IF;
                END IF;
                
                RETURN NEW;
            END;
            $func$ LANGUAGE plpgsql
        """)
        
        # Create triggers
        triggers = [
            "CREATE TRIGGER manage_current_version_trigger BEFORE INSERT ON file_versions FOR EACH ROW EXECUTE FUNCTION manage_current_version()",
            "CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects FOR EACH ROW EXECUTE FUNCTION update_updated_at_column()",
            "CREATE TRIGGER update_folders_updated_at BEFORE UPDATE ON folders FOR EACH ROW EXECUTE FUNCTION update_updated_at_column()",
            "CREATE TRIGGER update_files_updated_at BEFORE UPDATE ON files FOR EACH ROW EXECUTE FUNCTION update_updated_at_column()",
            "CREATE TRIGGER update_file_versions_updated_at BEFORE UPDATE ON file_versions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column()",
            "CREATE TRIGGER update_custom_attribute_definitions_updated_at BEFORE UPDATE ON custom_attribute_definitions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column()",
            "CREATE TRIGGER update_custom_attribute_values_updated_at BEFORE UPDATE ON custom_attribute_values FOR EACH ROW EXECUTE FUNCTION update_updated_at_column()",
            "CREATE TRIGGER update_sync_tasks_updated_at BEFORE UPDATE ON sync_tasks FOR EACH ROW EXECUTE FUNCTION update_updated_at_column()",
            "CREATE TRIGGER update_module_relations_updated_at BEFORE UPDATE ON module_relations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column()"
        ]
        
        for trigger_sql in triggers:
            await conn.execute(trigger_sql)
            
    async def step_10_indexes(self, conn):
        """步骤10: 创建索引"""
        indexes = [
            "CREATE INDEX idx_projects_status ON projects (status)",
            "CREATE INDEX idx_folders_project_id ON folders (project_id)",
            "CREATE INDEX idx_files_project_id ON files (project_id)",
            "CREATE INDEX idx_files_full_path ON files (project_id, full_path)",
            "CREATE INDEX idx_files_review_info ON files USING GIN (review_info)",
            "CREATE INDEX idx_file_versions_file_id ON file_versions (file_id)",
            "CREATE INDEX idx_file_versions_current ON file_versions (file_id) WHERE is_current_version = true",
            "CREATE INDEX idx_file_versions_review_info ON file_versions USING GIN (review_info)",
            "CREATE INDEX idx_custom_attr_definitions_project ON custom_attribute_definitions (project_id)",
            "CREATE INDEX idx_custom_attr_values_file_id ON custom_attribute_values (file_id)",
            "CREATE INDEX idx_sync_tasks_project_id ON sync_tasks (project_id)",
            "CREATE INDEX idx_module_relations_subject ON module_relations (subject_type, subject_id)",
            "CREATE INDEX idx_module_relations_project ON module_relations (project_id)"
        ]
        
        for index_sql in indexes:
            await conn.execute(index_sql)

async def main():
    """主函数"""
    print("Starting V2 database step-by-step initialization...")
    
    initializer = V2DatabaseStepByStepInitializer()
    
    try:
        await initializer.initialize()
        
        # 验证创建的表
        dal = await get_optimized_postgresql_dal()
        async with dal.get_connection() as conn:
            tables = await conn.fetch("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name
            """)
            
            views = await conn.fetch("""
                SELECT table_name 
                FROM information_schema.views 
                WHERE table_schema = 'public' 
                ORDER BY table_name
            """)
            
            print(f"\nCreated tables: {[t['table_name'] for t in tables]}")
            print(f"Created views: {[v['table_name'] for v in views]}")
            print(f"Total: {len(tables)} tables, {len(views)} views")
            
    except Exception as e:
        print(f"ERROR: Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
    return 0

if __name__ == "__main__":
    exit(asyncio.run(main()))
