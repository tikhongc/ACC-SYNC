-- ============================================================================
-- 优化的PostgreSQL数据库架构 V2 - 基于数据分析的优化方案
-- 核心改进：删除无用null字段，优化文件版本设计，改进自定义属性关联
-- ============================================================================

-- 启用必要的扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- ============================================================================
-- 1. 项目表 (保持不变)
-- ============================================================================

CREATE TABLE IF NOT EXISTS projects (
    id VARCHAR(255) PRIMARY KEY,  -- project_id
    name VARCHAR(500) NOT NULL,
    description TEXT,
    hub_id VARCHAR(255),
    account_id VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'archived')),
    
    -- 🔑 优化：添加同步优化字段
    last_sync_time TIMESTAMP WITH TIME ZONE,  -- 上次同步时间
    last_full_sync_time TIMESTAMP WITH TIME ZONE,  -- 上次全量同步时间
    sync_status VARCHAR(50) DEFAULT 'never_synced',  -- 同步状态
    
    -- 同步统计信息 (JSONB)
    sync_stats JSONB DEFAULT '{}'::jsonb,
    
    -- 项目统计信息
    statistics JSONB DEFAULT '{}'::jsonb,
    
    -- 元数据
    metadata JSONB DEFAULT '{}'::jsonb,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 2. 文件夹表 (保持不变)
-- ============================================================================

CREATE TABLE IF NOT EXISTS folders (
    id VARCHAR(500) PRIMARY KEY,  -- folder_id
    project_id VARCHAR(255) NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(500) NOT NULL,
    display_name VARCHAR(500),
    parent_id VARCHAR(500),  -- self-reference, null for root folders
    
    -- 路径信息
    path TEXT NOT NULL,  -- 完整路径
    path_segments TEXT[] DEFAULT '{}',  -- 路径分段数组
    depth INTEGER DEFAULT 0 CHECK (depth >= 0),  -- 层级深度
    
    -- 🔑 核心优化字段：时间戳信息
    create_time TIMESTAMP WITH TIME ZONE,
    create_user_id VARCHAR(100),
    create_user_name VARCHAR(200),
    last_modified_time TIMESTAMP WITH TIME ZONE,
    last_modified_user_id VARCHAR(100),
    last_modified_user_name VARCHAR(200),
    last_modified_time_rollup TIMESTAMP WITH TIME ZONE,  -- 🚀 智能跳过核心字段
    
    -- 统计信息
    object_count INTEGER DEFAULT 0,
    total_size BIGINT DEFAULT 0,
    
    -- 状态和权限
    hidden BOOLEAN DEFAULT FALSE,
    
    -- 基本属性 (JSONB for flexibility)
    metadata JSONB DEFAULT '{}'::jsonb,
    
    -- 扩展属性（原始API数据）
    extension JSONB DEFAULT '{}'::jsonb,
    
    -- 子项统计信息
    children_stats JSONB DEFAULT '{}'::jsonb,
    
    -- 同步信息
    sync_info JSONB DEFAULT '{}'::jsonb,

    -- 🔑 新增：文件夹权限信息
    permissions JSONB DEFAULT '{}'::jsonb,  -- 存储文件夹权限数据
    permissions_sync_time TIMESTAMP WITH TIME ZONE,  -- 权限同步时间

    -- 索引优化字段（生成列）
    project_path TEXT GENERATED ALWAYS AS (project_id || '::' || path) STORED,
    parent_path TEXT GENERATED ALWAYS AS (
        CASE 
            WHEN parent_id IS NULL THEN project_id || '::'
            ELSE project_id || '::' || SUBSTRING(path FROM 1 FOR LENGTH(path) - LENGTH(name) - 1)
        END
    ) STORED,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- 外键约束
    FOREIGN KEY (parent_id) REFERENCES folders(id) ON DELETE SET NULL
);

-- ============================================================================
-- 3. 🔑 优化的文件表 - 删除无用null字段，移除版本相关冗余
-- ============================================================================

CREATE TABLE IF NOT EXISTS files (
    id VARCHAR(500) PRIMARY KEY,  -- file_id
    project_id VARCHAR(255) NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(500) NOT NULL,
    display_name VARCHAR(500),
    parent_folder_id VARCHAR(500) REFERENCES folders(id) ON DELETE SET NULL,
    
    -- 路径信息 (修复null问题)
    folder_path TEXT NOT NULL DEFAULT '',  -- 所在文件夹的完整路径
    full_path TEXT NOT NULL,    -- 文件的完整路径（包含文件名）
    path_segments TEXT[] DEFAULT '{}',  -- 完整路径分段
    depth INTEGER DEFAULT 0 CHECK (depth >= 0),  -- 文件所在层级深度
    
    -- 🔑 核心优化字段：时间戳信息
    create_time TIMESTAMP WITH TIME ZONE,
    create_user_id VARCHAR(100),
    create_user_name VARCHAR(200),
    last_modified_time TIMESTAMP WITH TIME ZONE,  -- 🚀 增量同步核心字段
    last_modified_user_id VARCHAR(100),
    last_modified_user_name VARCHAR(200),
    
    -- 🔑 优化：只保留稳定的文件属性，版本相关信息移到版本表
    file_type VARCHAR(50),
    mime_type VARCHAR(100),
    
    -- 状态信息 (保留必要的预留字段，删除无用的null字段)
    reserved BOOLEAN DEFAULT FALSE,
    -- 删除: reserved_time, reserved_user_id, reserved_user_name (大部分为null)
    hidden BOOLEAN DEFAULT FALSE,
    
    -- 基本元数据
    metadata JSONB DEFAULT '{}'::jsonb,
    
    -- 文件类型和扩展信息
    file_info JSONB DEFAULT '{}'::jsonb,
    
    -- 🔑 优化：当前版本快速访问 (通过计算列或视图获取)
    -- 删除: current_version_id, version_number, file_size, storage_size, 
    --      storage_urn, download_url, process_state (移到版本表)
    
    -- 版本历史摘要
    versions_summary JSONB DEFAULT '{}'::jsonb,
    
    -- 同步信息
    sync_info JSONB DEFAULT '{}'::jsonb,
    
    -- 索引优化字段（生成列）
    project_folder TEXT GENERATED ALWAYS AS (project_id || '::' || COALESCE(folder_path, '')) STORED,
    project_type TEXT GENERATED ALWAYS AS (project_id || '::' || COALESCE(file_type, 'unknown')) STORED,
    name_lower TEXT GENERATED ALWAYS AS (LOWER(name)) STORED,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 4. 🔑 优化的自定义属性定义表 - 改进关联设计
-- ============================================================================

CREATE TABLE IF NOT EXISTS custom_attribute_definitions (
    id SERIAL PRIMARY KEY,
    attr_id INTEGER NOT NULL,  -- 属性ID (来自ACC API)
    project_id VARCHAR(255) NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    
    -- 🔑 优化：属性作用域设计
    scope_type VARCHAR(20) NOT NULL DEFAULT 'project' CHECK (scope_type IN ('project', 'folder')),
    scope_folder_id VARCHAR(500) REFERENCES folders(id) ON DELETE CASCADE,  -- 当scope_type='folder'时使用
    
    -- 属性定义
    name VARCHAR(200) NOT NULL,
    type VARCHAR(50) NOT NULL CHECK (type IN ('string', 'date', 'array', 'number', 'boolean')),
    array_values JSONB,  -- 用于存储下拉列表选项
    
    -- 元数据
    description TEXT,
    is_required BOOLEAN DEFAULT FALSE,
    default_value TEXT,
    
    -- 🔑 新增：属性继承规则
    inherit_to_subfolders BOOLEAN DEFAULT TRUE,  -- 是否继承到子文件夹
    
    -- 同步信息
    sync_info JSONB DEFAULT '{}'::jsonb,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- 🔑 优化的约束
    CONSTRAINT uk_custom_attr_def UNIQUE (attr_id, project_id, scope_type, COALESCE(scope_folder_id, '')),
    CONSTRAINT fk_custom_attr_def_project FOREIGN KEY (project_id) REFERENCES projects(id),
    CONSTRAINT fk_custom_attr_def_folder FOREIGN KEY (scope_folder_id) REFERENCES folders(id),
    
    -- 🔑 新增：作用域一致性约束
    CONSTRAINT chk_scope_consistency CHECK (
        (scope_type = 'project' AND scope_folder_id IS NULL) OR
        (scope_type = 'folder' AND scope_folder_id IS NOT NULL)
    )
);

-- ============================================================================
-- 5. 🔑 优化的自定义属性值表 - 强化关联和数据完整性
-- ============================================================================

CREATE TABLE IF NOT EXISTS custom_attribute_values (
    id SERIAL PRIMARY KEY,
    file_id VARCHAR(500) NOT NULL REFERENCES files(id) ON DELETE CASCADE,
    attr_definition_id INTEGER NOT NULL REFERENCES custom_attribute_definitions(id) ON DELETE CASCADE,
    project_id VARCHAR(255) NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    
    -- 🔑 优化：多类型值存储 (改进数据类型支持)
    value TEXT,
    value_date TIMESTAMP WITH TIME ZONE,  -- 专门存储日期类型值
    value_number DECIMAL(15,4),  -- 专门存储数值类型值
    value_boolean BOOLEAN,  -- 专门存储布尔类型值
    value_array JSONB,  -- 专门存储数组类型值
    
    -- 🔑 优化：属性更新时间和审计
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_by_user_id VARCHAR(100),
    updated_by_user_name VARCHAR(200),
    
    -- 🔑 新增：数据验证状态
    validation_status VARCHAR(20) DEFAULT 'valid' CHECK (validation_status IN ('valid', 'invalid', 'pending')),
    validation_errors JSONB DEFAULT '[]'::jsonb,
    
    -- 同步信息
    sync_info JSONB DEFAULT '{}'::jsonb,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- 🔑 优化的约束
    CONSTRAINT uk_custom_attr_value UNIQUE (file_id, attr_definition_id),
    CONSTRAINT fk_custom_attr_value_file FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE,
    CONSTRAINT fk_custom_attr_value_def FOREIGN KEY (attr_definition_id) REFERENCES custom_attribute_definitions(id) ON DELETE CASCADE,
    
    -- 🔑 新增：值类型一致性约束
    CONSTRAINT chk_value_type_consistency CHECK (
        (value IS NOT NULL AND value_date IS NULL AND value_number IS NULL AND value_boolean IS NULL AND value_array IS NULL) OR
        (value IS NULL AND value_date IS NOT NULL AND value_number IS NULL AND value_boolean IS NULL AND value_array IS NULL) OR
        (value IS NULL AND value_date IS NULL AND value_number IS NOT NULL AND value_boolean IS NULL AND value_array IS NULL) OR
        (value IS NULL AND value_date IS NULL AND value_number IS NULL AND value_boolean IS NOT NULL AND value_array IS NULL) OR
        (value IS NULL AND value_date IS NULL AND value_number IS NULL AND value_boolean IS NULL AND value_array IS NOT NULL)
    )
);

-- ============================================================================
-- 6. 🔑 优化的文件版本表 - 集中版本相关信息
-- ============================================================================

CREATE TABLE IF NOT EXISTS file_versions (
    id VARCHAR(500) PRIMARY KEY,  -- version_id (version URN)
    file_id VARCHAR(500) NOT NULL REFERENCES files(id) ON DELETE CASCADE,
    project_id VARCHAR(255) NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    version_number INTEGER NOT NULL CHECK (version_number > 0),
    
    -- URN信息
    urn VARCHAR(500) UNIQUE NOT NULL,           -- version URN
    item_urn VARCHAR(500),      -- item URN
    storage_urn VARCHAR(500),   -- storage URN
    lineage_urn VARCHAR(500),   -- lineage URN
    
    -- 🔑 版本时间戳信息 (删除无用的last_modified_*)
    create_time TIMESTAMP WITH TIME ZONE,
    create_user_id VARCHAR(100),
    create_user_name VARCHAR(200),
    
    -- 🔑 优化：集中所有版本相关信息
    file_size BIGINT DEFAULT 0,
    storage_size BIGINT DEFAULT 0,
    mime_type VARCHAR(100),
    process_state VARCHAR(50),
    download_url TEXT,  -- 从文件表移过来
    
    -- 🔑 新增：版本状态管理
    is_current_version BOOLEAN DEFAULT FALSE,  -- 是否为当前版本
    version_status VARCHAR(20) DEFAULT 'active' CHECK (version_status IN ('active', 'archived', 'deleted')),
    
    -- 版本元数据
    metadata JSONB DEFAULT '{}'::jsonb,
    
    -- Review状态信息
    review_info JSONB DEFAULT '{}'::jsonb,

    -- 🔑 新增：Review状态（InReview 或 NotInReview）
    review_state VARCHAR(20) DEFAULT 'NotInReview' CHECK (review_state IN ('InReview', 'NotInReview')),

    -- 扩展属性（完整的extension数据）
    extension JSONB DEFAULT '{}'::jsonb,
    
    -- 下载信息
    download_info JSONB DEFAULT '{}'::jsonb,
    
    -- 同步信息
    sync_info JSONB DEFAULT '{}'::jsonb,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- 🔑 优化的约束
    UNIQUE(file_id, version_number),
    
    -- 🔑 新增：确保每个文件只有一个当前版本
    EXCLUDE USING btree (file_id WITH =) WHERE (is_current_version = true)
);

-- ============================================================================
-- 7. 同步任务表 (保持不变)
-- ============================================================================

CREATE TABLE IF NOT EXISTS sync_tasks (
    id SERIAL PRIMARY KEY,
    task_uuid VARCHAR(36) UNIQUE NOT NULL,  -- 任务UUID
    project_id VARCHAR(255) REFERENCES projects(id) ON DELETE CASCADE,
    task_type VARCHAR(100) NOT NULL CHECK (task_type IN ('full_sync', 'incremental_sync', 'folder_sync', 'file_sync', 'optimized_full_sync', 'optimized_incremental_sync')),
    task_status VARCHAR(50) DEFAULT 'pending' CHECK (task_status IN ('pending', 'running', 'completed', 'failed', 'cancelled')),
    
    -- 🔑 优化：性能模式
    performance_mode VARCHAR(50) DEFAULT 'standard' CHECK (performance_mode IN ('standard', 'high_performance', 'conservative')),
    
    -- 任务参数
    parameters JSONB DEFAULT '{}'::jsonb,
    
    -- 任务进度
    progress JSONB DEFAULT '{}'::jsonb,
    
    -- 🔑 优化：性能统计
    performance_stats JSONB DEFAULT '{}'::jsonb,
    
    -- 任务结果
    results JSONB DEFAULT '{}'::jsonb,
    
    -- 错误信息
    error_message TEXT,
    error_details JSONB DEFAULT '{}'::jsonb,
    
    -- 时间信息
    start_time TIMESTAMP WITH TIME ZONE,
    end_time TIMESTAMP WITH TIME ZONE,
    duration_seconds DECIMAL(10,3),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 8. 模块关联表 (保持不变)
-- ============================================================================

CREATE TABLE IF NOT EXISTS module_relations (
    id SERIAL PRIMARY KEY,
    project_id VARCHAR(255) NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    
    -- 关联类型
    relation_type VARCHAR(100) NOT NULL,  -- file_to_rfi, file_to_submittal, file_to_review, etc.
    
    -- 源对象信息
    source_type VARCHAR(50) NOT NULL CHECK (source_type IN ('file', 'folder', 'version')),
    source_id VARCHAR(500) NOT NULL,      -- 源对象ID
    source_name VARCHAR(500),             -- 源对象名称
    
    -- 目标对象信息
    target_type VARCHAR(50) NOT NULL CHECK (target_type IN ('rfi', 'submittal', 'review', 'issue', 'form', 'transmittal')),
    target_id VARCHAR(500) NOT NULL,      -- 目标对象ID
    target_name VARCHAR(500),             -- 目标对象名称
    
    -- 关联元数据
    relation_metadata JSONB DEFAULT '{}'::jsonb,
    
    -- 同步信息
    sync_info JSONB DEFAULT '{}'::jsonb,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- 唯一约束（防止重复关联）
    UNIQUE(project_id, relation_type, source_type, source_id, target_type, target_id)
);

-- ============================================================================
-- 9. 🔑 新增：便捷视图 - 文件当前版本信息
-- ============================================================================

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
    fv.create_user_name as version_create_user_name
FROM files f
LEFT JOIN file_versions fv ON f.id = fv.file_id AND fv.is_current_version = true;

-- ============================================================================
-- 10. 🔑 新增：自定义属性继承视图
-- ============================================================================

CREATE VIEW file_applicable_attributes AS
WITH RECURSIVE folder_hierarchy AS (
    -- 获取文件所在文件夹
    SELECT f.id as file_id, f.parent_folder_id as folder_id, f.project_id, 0 as level
    FROM files f
    WHERE f.parent_folder_id IS NOT NULL
    
    UNION ALL
    
    -- 递归获取父文件夹
    SELECT fh.file_id, fo.parent_id as folder_id, fh.project_id, fh.level + 1
    FROM folder_hierarchy fh
    JOIN folders fo ON fh.folder_id = fo.id
    WHERE fo.parent_id IS NOT NULL AND fh.level < 10  -- 防止无限递归
)
SELECT DISTINCT
    fh.file_id,
    cad.id as attr_definition_id,
    cad.attr_id,
    cad.name as attr_name,
    cad.type as attr_type,
    cad.is_required,
    cad.default_value,
    cad.scope_type,
    cad.scope_folder_id
FROM folder_hierarchy fh
JOIN custom_attribute_definitions cad ON (
    (cad.scope_type = 'project' AND cad.project_id = fh.project_id) OR
    (cad.scope_type = 'folder' AND cad.scope_folder_id = fh.folder_id AND cad.inherit_to_subfolders = true)
)

UNION

-- 项目级别属性适用于所有文件
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
JOIN custom_attribute_definitions cad ON cad.project_id = f.project_id AND cad.scope_type = 'project';

-- ============================================================================
-- 创建更新时间戳的触发器函数
-- ============================================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- ============================================================================
-- 🔑 新增：当前版本管理触发器
-- ============================================================================

CREATE OR REPLACE FUNCTION manage_current_version()
RETURNS TRIGGER AS $$
BEGIN
    -- 当插入新版本时，如果是最新版本号，则设为当前版本
    IF TG_OP = 'INSERT' THEN
        -- 检查是否是该文件的最新版本
        IF NEW.version_number = (
            SELECT COALESCE(MAX(version_number), 0) + 1
            FROM file_versions
            WHERE file_id = NEW.file_id
        ) THEN
            -- 取消该文件其他版本的当前版本标记
            UPDATE file_versions
            SET is_current_version = false
            WHERE file_id = NEW.file_id AND id != NEW.id;

            -- 设置新版本为当前版本
            NEW.is_current_version = true;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ language 'plpgsql';

-- ============================================================================
-- 🔑 Review状态计算函数
-- ============================================================================

CREATE OR REPLACE FUNCTION compute_file_version_review_state(p_file_version_urn VARCHAR(500))
RETURNS VARCHAR(20) AS $$
DECLARE
    pending_count INTEGER;
BEGIN
    -- 检查是否存在任何pending状态的review_file_versions
    SELECT COUNT(*) INTO pending_count
    FROM review_file_versions
    WHERE file_version_urn = p_file_version_urn
    AND approval_status = 'PENDING';

    -- 如果存在pending的review，返回InReview，否则返回NotInReview
    IF pending_count > 0 THEN
        RETURN 'InReview';
    ELSE
        RETURN 'NotInReview';
    END IF;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- 为所有表创建更新时间戳触发器
-- ============================================================================

CREATE TRIGGER update_projects_updated_at 
    BEFORE UPDATE ON projects 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_folders_updated_at 
    BEFORE UPDATE ON folders 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_files_updated_at 
    BEFORE UPDATE ON files 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_custom_attribute_definitions_updated_at 
    BEFORE UPDATE ON custom_attribute_definitions 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_custom_attribute_values_updated_at 
    BEFORE UPDATE ON custom_attribute_values 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_file_versions_updated_at 
    BEFORE UPDATE ON file_versions 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_sync_tasks_updated_at 
    BEFORE UPDATE ON sync_tasks 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_module_relations_updated_at 
    BEFORE UPDATE ON module_relations 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 🔑 新增：版本管理触发器
CREATE TRIGGER manage_current_version_trigger
    BEFORE INSERT ON file_versions
    FOR EACH ROW EXECUTE FUNCTION manage_current_version();

-- ============================================================================
-- 🔑 数据迁移函数：初始化reviewState
-- ============================================================================

CREATE OR REPLACE FUNCTION backfill_file_version_review_states()
RETURNS TABLE (
    updated_count INTEGER,
    in_review_count INTEGER,
    not_in_review_count INTEGER
) AS $$
DECLARE
    v_updated_count INTEGER := 0;
    v_in_review_count INTEGER := 0;
    v_not_in_review_count INTEGER := 0;
    v_file_version RECORD;
BEGIN
    -- 遍历所有file_versions，计算并更新reviewState
    FOR v_file_version IN
        SELECT id, urn FROM file_versions
    LOOP
        -- 计算该版本的review_state
        UPDATE file_versions
        SET review_state = compute_file_version_review_state(v_file_version.urn),
            updated_at = CURRENT_TIMESTAMP
        WHERE id = v_file_version.id;

        v_updated_count := v_updated_count + 1;
    END LOOP;

    -- 统计结果
    SELECT COUNT(*) INTO v_in_review_count FROM file_versions WHERE review_state = 'InReview';
    SELECT COUNT(*) INTO v_not_in_review_count FROM file_versions WHERE review_state = 'NotInReview';

    RETURN QUERY SELECT v_updated_count, v_in_review_count, v_not_in_review_count;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- 🔑 优化索引策略
-- ============================================================================

-- 项目表索引
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_projects_last_sync_time 
ON projects (last_sync_time DESC) WHERE last_sync_time IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_projects_sync_status 
ON projects (sync_status);

-- 🚀 文件夹表核心优化索引
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_folders_project_rollup_time 
ON folders (project_id, last_modified_time_rollup DESC) 
WHERE last_modified_time_rollup IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_folders_project_modified_time 
ON folders (project_id, last_modified_time DESC) 
WHERE last_modified_time IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_folders_parent_path 
ON folders (parent_id, path) 
WHERE parent_id IS NOT NULL;

-- 🚀 文件表核心优化索引
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_files_project_modified_time 
ON files (project_id, last_modified_time DESC) 
WHERE last_modified_time IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_files_folder_modified 
ON files (parent_folder_id, last_modified_time DESC);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_files_project_folder_name 
ON files (project_id, parent_folder_id, name);

-- 🔑 新增：文件路径索引
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_files_full_path 
ON files (project_id, full_path);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_files_folder_path 
ON files (project_id, folder_path);

-- 🚀 自定义属性优化索引
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_custom_attr_definitions_project_scope 
ON custom_attribute_definitions (project_id, scope_type, scope_folder_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_custom_attr_definitions_attr_id 
ON custom_attribute_definitions (attr_id, project_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_custom_attr_values_file_def 
ON custom_attribute_values (file_id, attr_definition_id);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_custom_attr_values_project_updated 
ON custom_attribute_values (project_id, updated_at DESC);

-- 🔑 新增：自定义属性值类型索引
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_custom_attr_values_string 
ON custom_attribute_values (attr_definition_id, value) 
WHERE value IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_custom_attr_values_number 
ON custom_attribute_values (attr_definition_id, value_number) 
WHERE value_number IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_custom_attr_values_date 
ON custom_attribute_values (attr_definition_id, value_date) 
WHERE value_date IS NOT NULL;

-- 🔑 优化版本表索引
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_file_versions_file_version 
ON file_versions (file_id, version_number DESC);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_file_versions_current 
ON file_versions (file_id) 
WHERE is_current_version = true;

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_file_versions_project_create_time
ON file_versions (project_id, create_time DESC);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_file_versions_review_state
ON file_versions (review_state)
WHERE review_state = 'InReview';

-- 同步任务索引
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_sync_tasks_project_time 
ON sync_tasks (project_id, start_time DESC);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_sync_tasks_status_time 
ON sync_tasks (task_status, start_time DESC);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_sync_tasks_uuid 
ON sync_tasks (task_uuid);

-- JSONB 索引优化
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_files_file_info_gin 
ON files USING GIN (file_info);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_folders_metadata_gin
ON folders USING GIN (metadata);

-- 🔑 新增：文件夹权限索引
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_folders_permissions_gin
ON folders USING GIN (permissions);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_folders_permissions_sync_time
ON folders (project_id, permissions_sync_time DESC)
WHERE permissions_sync_time IS NOT NULL;

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_sync_tasks_performance_stats_gin
ON sync_tasks USING GIN (performance_stats);

-- ============================================================================
-- 完成提示
-- ============================================================================

DO $$
BEGIN
    RAISE NOTICE '🚀 优化的PostgreSQL schema V2创建成功!';
    RAISE NOTICE '📊 核心改进:';
    RAISE NOTICE '   - 删除无用null字段，减少存储空间';
    RAISE NOTICE '   - 优化文件版本设计，集中版本相关信息';
    RAISE NOTICE '   - 改进自定义属性关联，支持作用域和继承';
    RAISE NOTICE '   - 添加便捷视图和触发器，提升数据一致性';
    RAISE NOTICE '   - 强化索引策略，优化查询性能';
    RAISE NOTICE '✅ 准备进行数据迁移和同步逻辑更新';
END $$;
