-- ============================================================================
-- 添加 review_file_versions 到 file_versions 的外键约束
-- ============================================================================
-- 
-- 用途：为现有数据库添加外键约束，确保数据完整性
-- 
-- 执行前提：
-- 1. file_versions 表必须存在
-- 2. file_versions.urn 字段必须有唯一索引
-- 3. review_file_versions 表中的所有 file_version_urn 都必须在 file_versions.urn 中存在
-- 
-- ============================================================================

-- 步骤 1: 检查是否有不匹配的数据
DO $$
DECLARE
    unmatched_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO unmatched_count
    FROM review_file_versions rfv
    LEFT JOIN file_versions fv ON rfv.file_version_urn = fv.urn
    WHERE fv.urn IS NULL;
    
    IF unmatched_count > 0 THEN
        RAISE WARNING '发现 % 条 review_file_versions 记录的 file_version_urn 在 file_versions 表中不存在', unmatched_count;
        RAISE WARNING '请先运行文件同步或清理这些记录';
        
        -- 显示不匹配的记录
        RAISE NOTICE '不匹配的记录示例:';
        FOR i IN 1..LEAST(unmatched_count, 5) LOOP
            RAISE NOTICE '  - URN: %', (
                SELECT file_version_urn 
                FROM review_file_versions rfv
                LEFT JOIN file_versions fv ON rfv.file_version_urn = fv.urn
                WHERE fv.urn IS NULL
                LIMIT 1 OFFSET (i-1)
            );
        END LOOP;
        
        RAISE EXCEPTION '无法添加外键约束：存在不匹配的数据';
    ELSE
        RAISE NOTICE '✓ 数据完整性检查通过：所有 file_version_urn 都存在于 file_versions 表中';
    END IF;
END $$;

-- 步骤 2: 删除旧的外键约束（如果存在）
ALTER TABLE review_file_versions 
    DROP CONSTRAINT IF EXISTS fk_review_file_version_urn;

-- 步骤 3: 添加外键约束
ALTER TABLE review_file_versions
    ADD CONSTRAINT fk_review_file_version_urn 
    FOREIGN KEY (file_version_urn) 
    REFERENCES file_versions(urn) 
    ON DELETE RESTRICT;  -- 防止删除正在被评审的文件版本

-- 步骤 4: 验证约束
DO $$
BEGIN
    IF EXISTS (
        SELECT 1 
        FROM information_schema.table_constraints 
        WHERE constraint_name = 'fk_review_file_version_urn'
        AND table_name = 'review_file_versions'
    ) THEN
        RAISE NOTICE '✓ 外键约束添加成功！';
        RAISE NOTICE '  约束名称: fk_review_file_version_urn';
        RAISE NOTICE '  引用关系: review_file_versions.file_version_urn -> file_versions.urn';
        RAISE NOTICE '  删除策略: RESTRICT (防止删除正在被评审的文件版本)';
    ELSE
        RAISE EXCEPTION '外键约束添加失败';
    END IF;
END $$;

-- ============================================================================
-- 完成
-- ============================================================================

-- 查看约束详情
SELECT 
    tc.constraint_name,
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name,
    rc.delete_rule
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
JOIN information_schema.referential_constraints AS rc
    ON rc.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
AND tc.table_name = 'review_file_versions'
AND tc.constraint_name = 'fk_review_file_version_urn';

