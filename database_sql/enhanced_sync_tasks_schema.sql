-- ============================================================================
-- 增强的同步任务表设计 - 支持多模块扩展
-- 解决sync_tasks表为空的问题，并为未来模块扩展做准备
-- ============================================================================

-- 删除现有表（如果存在）
DROP TABLE IF EXISTS sync_tasks CASCADE;

-- 创建增强的同步任务表
CREATE TABLE sync_tasks (
    -- 基本标识
    id SERIAL PRIMARY KEY,
    task_uuid VARCHAR(36) UNIQUE NOT NULL,  -- 任务UUID
    project_id VARCHAR(255) NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    
    -- 任务类型和模块信息
    task_type VARCHAR(100) NOT NULL CHECK (task_type IN (
        'full_sync', 'incremental_sync', 'folder_sync', 'file_sync', 
        'optimized_full_sync', 'optimized_incremental_sync',
        'review_sync', 'permission_sync', 'custom_attribute_sync'  -- 未来模块
    )),
    module_type VARCHAR(50) DEFAULT 'file_management' CHECK (module_type IN (
        'file_management', 'review', 'permission', 'custom_attributes', 'other'
    )),
    
    -- 任务状态
    task_status VARCHAR(50) DEFAULT 'pending' CHECK (task_status IN (
        'pending', 'running', 'completed', 'failed', 'cancelled'
    )),
    
    -- 性能和配置
    performance_mode VARCHAR(50) DEFAULT 'standard' CHECK (performance_mode IN (
        'standard', 'high_performance', 'memory_optimized', 'conservative'
    )),
    
    -- 任务参数（JSONB存储灵活配置）
    parameters JSONB DEFAULT '{}'::jsonb,
    
    -- 任务进度（实时更新）
    progress JSONB DEFAULT '{}'::jsonb,
    
    -- 🔑 核心同步结果字段
    sync_results JSONB DEFAULT '{}'::jsonb,  -- 详细同步结果
    
    -- 🔑 同步内容标记（便于查询和统计）
    synced_file_tree BOOLEAN DEFAULT FALSE,           -- 是否同步了文件树（文件和文件夹metadata）
    synced_versions BOOLEAN DEFAULT FALSE,            -- 是否同步了文件版本
    synced_custom_attributes_definitions BOOLEAN DEFAULT FALSE,  -- 是否同步了自定义属性定义
    synced_custom_attributes_values BOOLEAN DEFAULT FALSE,      -- 是否同步了自定义属性值
    synced_permissions BOOLEAN DEFAULT FALSE,         -- 是否同步了权限
    synced_reviews BOOLEAN DEFAULT FALSE,             -- 是否同步了评审（未来扩展）
    
    -- 🔑 统计信息（便于快速查询）
    folders_synced INTEGER DEFAULT 0,
    files_synced INTEGER DEFAULT 0,
    versions_synced INTEGER DEFAULT 0,
    custom_attrs_synced INTEGER DEFAULT 0,
    permissions_synced INTEGER DEFAULT 0,
    reviews_synced INTEGER DEFAULT 0,  -- 未来扩展
    
    -- 性能统计
    performance_stats JSONB DEFAULT '{}'::jsonb,
    
    -- 错误信息
    error_message TEXT,
    error_details JSONB DEFAULT '{}'::jsonb,
    
    -- 时间信息
    start_time TIMESTAMP WITH TIME ZONE,
    end_time TIMESTAMP WITH TIME ZONE,
    duration_seconds DECIMAL(10,3),
    
    -- 🔑 用户信息
    started_by_user_id VARCHAR(100),
    started_by_user_name VARCHAR(200),
    
    -- 审计字段
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 索引优化
-- ============================================================================

-- 基本查询索引
CREATE INDEX IF NOT EXISTS idx_sync_tasks_project_time 
ON sync_tasks (project_id, start_time DESC);

CREATE INDEX IF NOT EXISTS idx_sync_tasks_status_time 
ON sync_tasks (task_status, start_time DESC);

CREATE INDEX IF NOT EXISTS idx_sync_tasks_uuid 
ON sync_tasks (task_uuid);

CREATE INDEX IF NOT EXISTS idx_sync_tasks_type_module 
ON sync_tasks (task_type, module_type);

-- 复合查询索引
CREATE INDEX IF NOT EXISTS idx_sync_tasks_project_status_time 
ON sync_tasks (project_id, task_status, start_time DESC);

CREATE INDEX IF NOT EXISTS idx_sync_tasks_module_status_time 
ON sync_tasks (module_type, task_status, start_time DESC);

-- JSONB索引
CREATE INDEX IF NOT EXISTS idx_sync_tasks_sync_results_gin 
ON sync_tasks USING GIN (sync_results);

CREATE INDEX IF NOT EXISTS idx_sync_tasks_performance_stats_gin 
ON sync_tasks USING GIN (performance_stats);

-- ============================================================================
-- 便捷视图
-- ============================================================================

-- 同步历史统一视图
CREATE OR REPLACE VIEW sync_history_view AS
SELECT 
    task_uuid,
    project_id,
    task_type,
    module_type,
    task_status,
    performance_mode,
    
    -- 同步内容摘要
    CASE 
        WHEN synced_file_tree THEN '文件树'
        ELSE ''
    END ||
    CASE 
        WHEN synced_versions THEN CASE WHEN synced_file_tree THEN '+版本' ELSE '版本' END
        ELSE ''
    END ||
    CASE 
        WHEN synced_custom_attributes_definitions OR synced_custom_attributes_values 
        THEN CASE WHEN synced_file_tree OR synced_versions THEN '+自定义属性' ELSE '自定义属性' END
        ELSE ''
    END ||
    CASE 
        WHEN synced_permissions THEN CASE WHEN synced_file_tree OR synced_versions OR synced_custom_attributes_definitions OR synced_custom_attributes_values THEN '+权限' ELSE '权限' END
        ELSE ''
    END ||
    CASE 
        WHEN synced_reviews THEN CASE WHEN synced_file_tree OR synced_versions OR synced_custom_attributes_definitions OR synced_custom_attributes_values OR synced_permissions THEN '+评审' ELSE '评审' END
        ELSE ''
    END AS sync_content_summary,
    
    -- 统计摘要
    folders_synced,
    files_synced,
    versions_synced,
    custom_attrs_synced,
    permissions_synced,
    reviews_synced,
    
    -- 时间信息
    start_time,
    end_time,
    duration_seconds,
    
    -- 用户信息
    started_by_user_name,
    
    created_at
FROM sync_tasks
ORDER BY start_time DESC;

-- 项目同步摘要视图
CREATE OR REPLACE VIEW project_sync_summary_view AS
SELECT 
    project_id,
    COUNT(*) as total_syncs,
    COUNT(CASE WHEN task_status = 'completed' THEN 1 END) as successful_syncs,
    COUNT(CASE WHEN task_status = 'failed' THEN 1 END) as failed_syncs,
    COUNT(CASE WHEN task_type = 'full_sync' THEN 1 END) as full_syncs,
    COUNT(CASE WHEN task_type LIKE '%incremental%' THEN 1 END) as incremental_syncs,
    MAX(start_time) as last_sync_time,
    MAX(CASE WHEN task_status = 'completed' THEN start_time END) as last_successful_sync,
    AVG(CASE WHEN task_status = 'completed' THEN duration_seconds END) as avg_duration_seconds,
    SUM(folders_synced) as total_folders_synced,
    SUM(files_synced) as total_files_synced,
    SUM(versions_synced) as total_versions_synced
FROM sync_tasks
GROUP BY project_id;

-- ============================================================================
-- 触发器 - 自动更新时间戳
-- ============================================================================

CREATE OR REPLACE FUNCTION update_sync_task_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    
    -- 自动计算持续时间
    IF NEW.end_time IS NOT NULL AND NEW.start_time IS NOT NULL THEN
        NEW.duration_seconds = EXTRACT(EPOCH FROM (NEW.end_time - NEW.start_time));
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER sync_tasks_update_timestamp
    BEFORE UPDATE ON sync_tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_sync_task_timestamp();

-- ============================================================================
-- 示例查询
-- ============================================================================

-- 查询项目的同步历史
/*
SELECT * FROM sync_history_view 
WHERE project_id = 'your-project-id' 
ORDER BY start_time DESC 
LIMIT 10;
*/

-- 查询所有模块的同步统计
/*
SELECT 
    module_type,
    COUNT(*) as total_tasks,
    COUNT(CASE WHEN task_status = 'completed' THEN 1 END) as completed_tasks,
    AVG(duration_seconds) as avg_duration
FROM sync_tasks 
GROUP BY module_type;
*/

-- 查询最近24小时的同步活动
/*
SELECT * FROM sync_history_view 
WHERE start_time >= NOW() - INTERVAL '24 hours'
ORDER BY start_time DESC;
*/

-- ============================================================================
-- 完成提示
-- ============================================================================

DO $$
BEGIN
    RAISE NOTICE '🚀 增强的sync_tasks表创建成功!';
    RAISE NOTICE '📊 主要改进:';
    RAISE NOTICE '   - 支持多模块扩展（review、permission等）';
    RAISE NOTICE '   - 详细的同步内容标记字段';
    RAISE NOTICE '   - 统计信息字段便于快速查询';
    RAISE NOTICE '   - 便捷视图支持统一的同步历史界面';
    RAISE NOTICE '   - 完整的索引策略优化查询性能';
    RAISE NOTICE '✅ 现在同步任务将正确记录到数据库中';
END $$;
