# 文件版本架构迁移指南

## 架构变更说明

### 变更前（旧架构）
```
review_file_versions 表包含所有文件信息：
- file_urn
- file_name
- file_size
- file_extension
- version_number
- 等等...
```

### 变更后（新架构）
```
file_versions 表（主表，在 optimized_schema_v2.sql）：
- urn (主键)
- file_id
- file_name
- file_size
- version_number
- 等等...

review_file_versions 表（关联表）：
- review_id
- file_version_urn (引用 file_versions.urn)
- approval_status (审批状态)
- approval_comments
- 等审批相关字段
```

## 数据迁移步骤

### 1. 确保 file_versions 表已创建
```sql
-- 检查表是否存在
SELECT EXISTS (
    SELECT FROM information_schema.tables 
    WHERE table_name = 'file_versions'
);
```

### 2. 迁移现有数据（如果有）
```sql
-- 从旧的 review_file_versions 提取唯一文件版本到 file_versions
INSERT INTO file_versions (
    urn, file_id, project_id, file_name, file_size, 
    file_extension, version_number, item_urn, 
    mime_type, created_at
)
SELECT DISTINCT
    version_urn as urn,
    file_urn as file_id,
    (SELECT project_id FROM reviews WHERE id = rfv.review_id LIMIT 1) as project_id,
    file_name,
    file_size,
    file_extension,
    version_number,
    item_urn,
    NULL as mime_type,
    created_at
FROM review_file_versions rfv
WHERE version_urn IS NOT NULL
ON CONFLICT (urn) DO NOTHING;

-- 备份旧表
ALTER TABLE review_file_versions RENAME TO review_file_versions_old;

-- 创建新的 review_file_versions 表（参考 review_system_schema.sql）
CREATE TABLE review_file_versions (
    id SERIAL PRIMARY KEY,
    review_id INTEGER NOT NULL REFERENCES reviews(id) ON DELETE CASCADE,
    file_version_urn TEXT NOT NULL,
    approval_status approval_status_type DEFAULT 'PENDING',
    approval_status_id VARCHAR(36),
    approval_status_value VARCHAR(20),
    approval_label VARCHAR(100),
    approval_comments TEXT,
    approval_conditions TEXT,
    review_content JSONB DEFAULT '{}'::jsonb,
    custom_attributes JSONB DEFAULT '[]'::jsonb,
    copied_file_version_urn TEXT,
    copy_target_folder TEXT,
    copy_settings JSONB DEFAULT '{}'::jsonb,
    local_file_path TEXT,
    thumbnail_url TEXT,
    tags JSONB DEFAULT '[]'::jsonb,
    approval_history JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    approved_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(review_id, file_version_urn)
);

-- 迁移审批数据到新表
INSERT INTO review_file_versions (
    review_id, file_version_urn, approval_status,
    approval_status_id, approval_status_value, approval_label,
    approval_comments, review_content, custom_attributes,
    copied_file_version_urn, tags, approval_history,
    created_at, updated_at, approved_at
)
SELECT 
    review_id,
    version_urn as file_version_urn,
    approval_status,
    approval_status_id,
    approval_status_value,
    approval_label,
    approval_comments,
    review_content,
    custom_attributes,
    copied_file_version_urn,
    tags,
    approval_history,
    created_at,
    updated_at,
    approved_at
FROM review_file_versions_old
WHERE version_urn IS NOT NULL;

-- 验证数据迁移
SELECT 
    (SELECT COUNT(*) FROM review_file_versions_old) as old_count,
    (SELECT COUNT(*) FROM review_file_versions) as new_count,
    (SELECT COUNT(*) FROM file_versions) as file_versions_count;
```

### 3. 创建索引
```sql
CREATE INDEX idx_review_file_versions_review ON review_file_versions(review_id);
CREATE INDEX idx_review_file_versions_status ON review_file_versions(approval_status);
CREATE INDEX idx_review_file_versions_urn ON review_file_versions(file_version_urn);
CREATE INDEX idx_review_file_versions_tags ON review_file_versions USING GIN (tags);
```

## 代码变更清单

### ✅ 已完成
1. `review_system_schema.sql` - 表结构更新
2. `review_sync_manager_enhanced.py` - `_sync_review_file_versions()` 方法
3. `review_data_access.py` - `batch_insert_review_files()` 方法

### ⚠️ 需要注意
- `postgresql_sync_manager.py` - **不需要修改**（继续同步到 file_versions）
- 查询文件信息时需要 JOIN file_versions 表

## 查询示例

### 获取评审的文件及详情
```sql
SELECT 
    r.id as review_id,
    r.name as review_name,
    rfv.approval_status,
    rfv.approval_comments,
    fv.file_name,
    fv.file_size,
    fv.version_number,
    fv.mime_type,
    fv.create_user_name
FROM reviews r
JOIN review_file_versions rfv ON r.id = rfv.review_id
JOIN file_versions fv ON rfv.file_version_urn = fv.urn
WHERE r.id = $1;
```

### 查找文件在哪些评审中
```sql
SELECT 
    fv.file_name,
    fv.version_number,
    r.name as review_name,
    r.status as review_status,
    rfv.approval_status
FROM file_versions fv
JOIN review_file_versions rfv ON fv.urn = rfv.file_version_urn
JOIN reviews r ON rfv.review_id = r.id
WHERE fv.urn = $1;
```

## 优势

1. **消除数据冗余**：文件信息只存储一次
2. **数据一致性**：文件更新自动反映到所有评审
3. **解耦设计**：文件同步和评审同步独立
4. **查询灵活**：可以轻松追踪文件的评审历史

## 回滚方案

如果需要回滚到旧架构：

```sql
-- 恢复旧表
DROP TABLE review_file_versions;
ALTER TABLE review_file_versions_old RENAME TO review_file_versions;

-- 删除 file_versions 表（如果不需要）
-- DROP TABLE file_versions;
```

## 注意事项

1. **同步顺序**：必须先运行文件同步（postgresql_sync_manager），再运行评审同步（review_sync_manager）
2. **外键约束**：如果使用外键，确保 file_versions 中存在对应的 urn
3. **性能**：JOIN 查询可能比单表查询稍慢，但数据一致性更好
4. **备份**：迁移前务必备份数据

## 测试清单

- [ ] file_versions 表已创建
- [ ] 数据已成功迁移
- [ ] 索引已创建
- [ ] 代码已更新
- [ ] 同步功能测试通过
- [ ] 查询功能测试通过
- [ ] 性能测试通过

