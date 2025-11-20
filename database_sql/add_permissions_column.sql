-- ============================================================================
-- 数据库迁移脚本：添加文件夹权限列
-- 用于将权限数据直接存储到 folders 表
-- ============================================================================

-- 添加权限 JSONB 列到 folders 表
ALTER TABLE folders
ADD COLUMN IF NOT EXISTS permissions JSONB DEFAULT '{}'::jsonb;

-- 添加权限同步时间列
ALTER TABLE folders
ADD COLUMN IF NOT EXISTS permissions_sync_time TIMESTAMP WITH TIME ZONE;

-- 添加注释说明
COMMENT ON COLUMN folders.permissions IS '文件夹权限数据，包含 users、roles、companies 和 summary';
COMMENT ON COLUMN folders.permissions_sync_time IS '权限最后同步时间';

-- 创建 GIN 索引以支持 JSONB 查询
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_folders_permissions_gin
ON folders USING GIN (permissions);

-- 创建权限同步时间索引，用于增量同步
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_folders_permissions_sync_time
ON folders (project_id, permissions_sync_time DESC)
WHERE permissions_sync_time IS NOT NULL;

-- ============================================================================
-- 验证脚本执行结果
-- ============================================================================

DO $$
DECLARE
    col_exists boolean;
BEGIN
    -- 检查 permissions 列是否存在
    SELECT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'folders' AND column_name = 'permissions'
    ) INTO col_exists;

    IF col_exists THEN
        RAISE NOTICE '✅ permissions 列添加成功';
    ELSE
        RAISE EXCEPTION '❌ permissions 列添加失败';
    END IF;

    -- 检查 permissions_sync_time 列是否存在
    SELECT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'folders' AND column_name = 'permissions_sync_time'
    ) INTO col_exists;

    IF col_exists THEN
        RAISE NOTICE '✅ permissions_sync_time 列添加成功';
    ELSE
        RAISE EXCEPTION '❌ permissions_sync_time 列添加失败';
    END IF;

    RAISE NOTICE '🚀 文件夹权限列迁移完成！';
END $$;
