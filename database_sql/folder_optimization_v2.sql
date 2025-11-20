-- ============================================================================
-- 文件夹表优化设计 V2
-- 基于实际数据分析的优化建议
-- ============================================================================

-- 1. 优化后的文件夹表结构
CREATE TABLE IF NOT EXISTS folders (
    id VARCHAR(500) PRIMARY KEY,
    project_id VARCHAR(255) NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(500) NOT NULL,
    display_name VARCHAR(500),
    parent_id VARCHAR(500) REFERENCES folders(id) ON DELETE CASCADE,
    
    -- 🔑 路径优化：预计算路径信息
    path TEXT NOT NULL,  -- 完整路径
    path_segments TEXT[] DEFAULT '{}',  -- 路径分段数组
    depth INTEGER DEFAULT 0 CHECK (depth >= 0),  -- 层级深度
    
    -- 🔑 核心优化：时间戳信息
    create_time TIMESTAMP WITH TIME ZONE,
    create_user_id VARCHAR(100),
    create_user_name VARCHAR(200),
    last_modified_time TIMESTAMP WITH TIME ZONE,
    last_modified_user_id VARCHAR(100),
    last_modified_user_name VARCHAR(200),
    
    -- 🚀 关键优化：rollup时间戳（用于智能跳过）
    last_modified_time_rollup TIMESTAMP WITH TIME ZONE,  -- 包含子文件夹的最新修改时间
    
    -- 🔑 统计信息优化（避免实时计算）
    object_count INTEGER DEFAULT 0,  -- 直接子项数量
    total_files_count INTEGER DEFAULT 0,  -- 递归文件总数
    total_folders_count INTEGER DEFAULT 0,  -- 递归文件夹总数
    total_size BIGINT DEFAULT 0,  -- 递归总大小
    
    -- 状态信息
    hidden BOOLEAN DEFAULT FALSE,
    
    -- 扩展信息
    extension JSONB DEFAULT '{}'::jsonb,
    metadata JSONB DEFAULT '{}'::jsonb,
    
    -- 🔑 性能优化：预计算字段
    project_path TEXT GENERATED ALWAYS AS (project_id || '::' || path) STORED,
    name_lower TEXT GENERATED ALWAYS AS (LOWER(name)) STORED,
    
    -- 同步信息
    sync_info JSONB DEFAULT '{}'::jsonb,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. 🚀 关键性能索引
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_folders_project_parent ON folders (project_id, parent_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_folders_path ON folders USING gin(path_segments);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_folders_depth ON folders (project_id, depth);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_folders_rollup_time ON folders (last_modified_time_rollup);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_folders_project_path ON folders (project_path);

-- 3. 🔑 智能跳过优化：文件夹层次结构视图
CREATE OR REPLACE VIEW folder_hierarchy AS
WITH RECURSIVE folder_tree AS (
    -- 根文件夹
    SELECT 
        id,
        project_id,
        name,
        parent_id,
        path,
        depth,
        last_modified_time_rollup,
        ARRAY[id] as folder_path_ids,
        ARRAY[name] as folder_path_names
    FROM folders 
    WHERE parent_id IS NULL
    
    UNION ALL
    
    -- 子文件夹
    SELECT 
        f.id,
        f.project_id,
        f.name,
        f.parent_id,
        f.path,
        f.depth,
        f.last_modified_time_rollup,
        ft.folder_path_ids || f.id,
        ft.folder_path_names || f.name
    FROM folders f
    JOIN folder_tree ft ON f.parent_id = ft.id
    WHERE f.depth < 20  -- 防止无限递归
)
SELECT * FROM folder_tree;

-- 4. 🚀 智能跳过函数：检查文件夹是否需要同步
CREATE OR REPLACE FUNCTION should_sync_folder(
    p_folder_id VARCHAR(500),
    p_last_sync_time TIMESTAMP WITH TIME ZONE
) RETURNS BOOLEAN AS $$
DECLARE
    folder_rollup_time TIMESTAMP WITH TIME ZONE;
BEGIN
    -- 获取文件夹的rollup时间
    SELECT last_modified_time_rollup 
    INTO folder_rollup_time
    FROM folders 
    WHERE id = p_folder_id;
    
    -- 如果rollup时间晚于上次同步时间，需要同步
    RETURN (folder_rollup_time IS NULL OR folder_rollup_time > p_last_sync_time);
END;
$$ LANGUAGE plpgsql;

-- 5. 🔑 统计信息更新触发器
CREATE OR REPLACE FUNCTION update_folder_stats() RETURNS TRIGGER AS $$
BEGIN
    -- 更新父文件夹的统计信息
    IF TG_OP = 'INSERT' THEN
        -- 新增文件/文件夹时更新统计
        UPDATE folders 
        SET 
            object_count = object_count + 1,
            total_files_count = CASE WHEN NEW.parent_id IS NOT NULL THEN total_files_count + 1 ELSE total_files_count END,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = NEW.parent_id;
        
    ELSIF TG_OP = 'DELETE' THEN
        -- 删除文件/文件夹时更新统计
        UPDATE folders 
        SET 
            object_count = GREATEST(0, object_count - 1),
            total_files_count = GREATEST(0, total_files_count - 1),
            updated_at = CURRENT_TIMESTAMP
        WHERE id = OLD.parent_id;
    END IF;
    
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

-- 6. 🚀 Rollup时间更新函数（关键优化）
CREATE OR REPLACE FUNCTION update_folder_rollup_time(
    p_folder_id VARCHAR(500),
    p_new_time TIMESTAMP WITH TIME ZONE
) RETURNS VOID AS $$
DECLARE
    current_folder_id VARCHAR(500);
BEGIN
    current_folder_id := p_folder_id;
    
    -- 递归更新所有父文件夹的rollup时间
    WHILE current_folder_id IS NOT NULL LOOP
        UPDATE folders 
        SET 
            last_modified_time_rollup = GREATEST(
                COALESCE(last_modified_time_rollup, p_new_time), 
                p_new_time
            ),
            updated_at = CURRENT_TIMESTAMP
        WHERE id = current_folder_id
        RETURNING parent_id INTO current_folder_id;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- 7. 🔑 文件夹路径查询优化视图
CREATE OR REPLACE VIEW folder_paths AS
SELECT 
    f.id,
    f.project_id,
    f.name,
    f.path,
    f.depth,
    f.last_modified_time_rollup,
    -- 快速获取所有祖先文件夹
    (
        WITH RECURSIVE ancestors AS (
            SELECT parent_id, 1 as level
            FROM folders 
            WHERE id = f.id AND parent_id IS NOT NULL
            
            UNION ALL
            
            SELECT p.parent_id, a.level + 1
            FROM folders p
            JOIN ancestors a ON p.id = a.parent_id
            WHERE p.parent_id IS NOT NULL AND a.level < 10
        )
        SELECT array_agg(parent_id ORDER BY level DESC)
        FROM ancestors
    ) as ancestor_ids,
    
    -- 快速获取直接子文件夹数量
    (SELECT COUNT(*) FROM folders WHERE parent_id = f.id) as direct_subfolder_count,
    
    -- 快速获取直接文件数量
    (SELECT COUNT(*) FROM files WHERE parent_folder_id = f.id) as direct_file_count
FROM folders f;

-- 8. 🚀 批量路径更新函数（用于数据修复）
CREATE OR REPLACE FUNCTION rebuild_folder_paths(p_project_id VARCHAR(255) DEFAULT NULL) 
RETURNS INTEGER AS $$
DECLARE
    updated_count INTEGER := 0;
    folder_rec RECORD;
BEGIN
    -- 重建指定项目或所有项目的文件夹路径
    FOR folder_rec IN 
        WITH RECURSIVE folder_paths AS (
            -- 根文件夹
            SELECT 
                id, 
                project_id,
                name,
                parent_id,
                name as computed_path,
                ARRAY[name] as computed_segments,
                0 as computed_depth
            FROM folders 
            WHERE parent_id IS NULL 
            AND (p_project_id IS NULL OR project_id = p_project_id)
            
            UNION ALL
            
            -- 子文件夹
            SELECT 
                f.id,
                f.project_id,
                f.name,
                f.parent_id,
                fp.computed_path || '/' || f.name,
                fp.computed_segments || f.name,
                fp.computed_depth + 1
            FROM folders f
            JOIN folder_paths fp ON f.parent_id = fp.id
            WHERE fp.computed_depth < 20
        )
        SELECT * FROM folder_paths
    LOOP
        UPDATE folders 
        SET 
            path = folder_rec.computed_path,
            path_segments = folder_rec.computed_segments,
            depth = folder_rec.computed_depth,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = folder_rec.id
        AND (
            path != folder_rec.computed_path OR 
            path_segments != folder_rec.computed_segments OR 
            depth != folder_rec.computed_depth
        );
        
        IF FOUND THEN
            updated_count := updated_count + 1;
        END IF;
    END LOOP;
    
    RETURN updated_count;
END;
$$ LANGUAGE plpgsql;

-- 9. 🔑 性能监控视图
CREATE OR REPLACE VIEW folder_performance_stats AS
SELECT 
    project_id,
    COUNT(*) as total_folders,
    MAX(depth) as max_depth,
    AVG(depth) as avg_depth,
    SUM(object_count) as total_objects,
    SUM(total_files_count) as total_files,
    MAX(last_modified_time_rollup) as latest_activity,
    COUNT(CASE WHEN last_modified_time_rollup > NOW() - INTERVAL '1 day' THEN 1 END) as active_folders_24h,
    COUNT(CASE WHEN object_count > 100 THEN 1 END) as large_folders
FROM folders
GROUP BY project_id;

-- 10. 创建触发器
CREATE TRIGGER trigger_update_folder_stats
    AFTER INSERT OR DELETE ON files
    FOR EACH ROW
    EXECUTE FUNCTION update_folder_stats();

COMMENT ON TABLE folders IS '优化的文件夹表，包含智能跳过和性能优化功能';
COMMENT ON COLUMN folders.last_modified_time_rollup IS '包含所有子项的最新修改时间，用于智能跳过同步';
COMMENT ON COLUMN folders.total_files_count IS '递归统计的文件总数，避免实时计算';
COMMENT ON FUNCTION should_sync_folder IS '智能跳过函数：判断文件夹是否需要同步';
COMMENT ON FUNCTION update_folder_rollup_time IS '更新文件夹rollup时间的核心函数';
