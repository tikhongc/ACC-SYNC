-- ============================================================================
-- 文件树缓存表 - 用于存储构建好的文件树结构
-- 采用"JSONB缓存 + 写入时失效"策略
-- 性能特性：读取极快，写入极快，数据最新
-- ============================================================================

CREATE TABLE IF NOT EXISTS file_tree_cache (
    id SERIAL PRIMARY KEY,
    project_id VARCHAR(255) NOT NULL UNIQUE,  -- project_id from projects table

    -- 缓存的树结构 (JSONB格式)
    cached_tree JSONB,

    -- 缓存元数据
    last_updated TIMESTAMP WITH TIME ZONE,
    cache_version INTEGER DEFAULT 1,

    -- 统计信息
    tree_size_bytes INTEGER DEFAULT 0,  -- 缓存大小（字节）
    total_folders INTEGER DEFAULT 0,    -- 文件夹总数
    total_files INTEGER DEFAULT 0,      -- 文件总数
    max_depth INTEGER DEFAULT 0,        -- 树的最大深度

    -- 构建时间
    last_build_time_ms DECIMAL(10, 2),  -- 上次构建耗时（毫秒）

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引以加快查询
CREATE INDEX IF NOT EXISTS idx_file_tree_cache_project_id ON file_tree_cache (project_id);
CREATE INDEX IF NOT EXISTS idx_file_tree_cache_updated ON file_tree_cache (updated_at DESC);

-- 添加注释
COMMENT ON TABLE file_tree_cache IS '文件树缓存表 - 高性能缓存，采用写入时失效策略';
COMMENT ON COLUMN file_tree_cache.cached_tree IS '完整的树结构，为NULL表示缓存已清空，需要重建';
COMMENT ON COLUMN file_tree_cache.last_build_time_ms IS '用于监控性能，记录构建耗时';

-- ============================================================================
-- 缓存统计表（可选，用于监控）
-- ============================================================================

CREATE TABLE IF NOT EXISTS file_tree_cache_stats (
    id SERIAL PRIMARY KEY,
    project_id VARCHAR(255) NOT NULL,  -- project_id from projects table

    -- 统计指标
    hit_count BIGINT DEFAULT 0,          -- 缓存命中次数
    miss_count BIGINT DEFAULT 0,         -- 缓存未命中次数
    invalidate_count BIGINT DEFAULT 0,   -- 缓存清空次数

    -- 性能指标
    avg_build_time_ms DECIMAL(10, 2),    -- 平均构建时间
    max_build_time_ms DECIMAL(10, 2),    -- 最大构建时间

    -- 时间信息
    last_hit_time TIMESTAMP WITH TIME ZONE,
    last_miss_time TIMESTAMP WITH TIME ZONE,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_file_tree_cache_stats_project ON file_tree_cache_stats (project_id);

COMMENT ON TABLE file_tree_cache_stats IS '文件树缓存统计表 - 用于性能监控和分析';
