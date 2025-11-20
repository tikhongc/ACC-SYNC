# 文件夹权限同步到数据库模块

## 概述

此模块用于将 ACC 项目文件夹的权限数据同步到 PostgreSQL 数据库的 `folders` 表中。

## 功能特性

- ✅ 从数据库轮询获取所有文件夹 ID
- ✅ 调用 ACC BIM 360 Docs API 获取每个文件夹的权限
- ✅ 解析权限数据为结构化 JSON 格式
- ✅ 批量更新数据库中的权限列
- ✅ 支持速率限制和错误处理
- ✅ 详细的统计信息和日志

## 数据库准备

### 1. 运行 Schema 迁移

首先确保 `folders` 表包含权限列。如果是新安装，运行以下迁移脚本：

```bash
# 连接到 neondb 数据库
psql postgresql://neondb_owner:npg_a2nxljG8LOSP@ep-soft-mountain-a4jqpy5e-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require

# 执行迁移脚本
\i database_sql/add_permissions_column.sql
```

或者使用 Python：

```python
import asyncpg
import asyncio

async def run_migration():
    conn = await asyncpg.connect(
        host='ep-soft-mountain-a4jqpy5e-pooler.us-east-1.aws.neon.tech',
        port=5432,
        database='neondb',
        user='neondb_owner',
        password='npg_a2nxljG8LOSP',
        ssl='require'
    )

    with open('database_sql/add_permissions_column.sql', 'r', encoding='utf-8') as f:
        migration_sql = f.read()

    await conn.execute(migration_sql)
    await conn.close()

asyncio.run(run_migration())
```

### 2. 验证 Schema 变更

检查 `folders` 表是否包含新列：

```sql
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'folders'
  AND column_name IN ('permissions', 'permissions_sync_time');
```

预期输出：
```
     column_name      | data_type | is_nullable
----------------------+-----------+-------------
 permissions          | jsonb     | YES
 permissions_sync_time| timestamp | YES
```

## 使用方法

### 基本用法

```bash
# 使用默认参数同步权限
python api_modules/permissions_db_sync.py
```

### 带参数运行

```bash
# 指定项目 ID
python api_modules/permissions_db_sync.py --project-id b.1eea4119-3553-4167-b93d-3a3d5d07d33d

# 调整批量大小（每批次更新的文件夹数量）
python api_modules/permissions_db_sync.py --batch-size 100

# 调整 API 调用延迟（避免限流）
python api_modules/permissions_db_sync.py --delay 0.5

# 组合使用
python api_modules/permissions_db_sync.py \
  --project-id b.1eea4119-3553-4167-b93d-3a3d5d07d33d \
  --batch-size 50 \
  --delay 0.2
```

## 权限 JSON 结构

存储在 `folders.permissions` 列中的 JSON 结构如下：

```json
{
  "users": [
    {
      "subject_id": "user123",
      "autodesk_id": "ABCD1234",
      "name": "John Doe",
      "email": "john.doe@example.com",
      "user_type": "standard",
      "subject_type": "USER",
      "subject_status": "active",
      "direct_actions": ["VIEW", "DOWNLOAD"],
      "inherit_actions": ["COLLABORATE"],
      "all_actions": ["VIEW", "DOWNLOAD", "COLLABORATE"],
      "permission_level": 2,
      "permission_name": "查看/下载",
      "permission_description": "Can view and download files",
      "detailed_permissions": {
        "canView": true,
        "canDownload": true,
        "canCollaborate": true,
        "canPublishMarkup": false,
        "canUpload": false,
        "canEdit": false,
        "canControl": false
      }
    }
  ],
  "roles": [
    {
      "subject_id": "role456",
      "name": "Project Manager",
      "subject_type": "ROLE",
      "all_actions": ["PUBLISH", "VIEW", "DOWNLOAD", "COLLABORATE", "PUBLISH_MARKUP", "EDIT"],
      "permission_level": 5,
      "permission_name": "Full Edit",
      ...
    }
  ],
  "companies": [
    {
      "subject_id": "company789",
      "name": "Contractor ABC",
      "subject_type": "COMPANY",
      ...
    }
  ],
  "summary": {
    "total_subjects": 15,
    "users_count": 8,
    "roles_count": 5,
    "companies_count": 2
  },
  "sync_time": "2025-11-19T17:45:30.123456"
}
```

## 权限级别定义

| 级别 | 名称 | 权限动作 | 描述 |
|------|------|----------|------|
| 1 | View Only | VIEW, COLLABORATE | 仅查看 |
| 2 | 查看/下载 | VIEW, DOWNLOAD, COLLABORATE | 可查看和下载 |
| 3 | 查看/下载/标记 | VIEW, DOWNLOAD, COLLABORATE, PUBLISH_MARKUP | 可查看、下载和标记 |
| 4 | 查看/下载/标记/上传 | PUBLISH, VIEW, DOWNLOAD, COLLABORATE, PUBLISH_MARKUP | 可查看、下载、标记和上传 |
| 5 | Full Edit | PUBLISH, VIEW, DOWNLOAD, COLLABORATE, PUBLISH_MARKUP, EDIT | 完全编辑权限 |
| 6 | Full Control | PUBLISH, VIEW, DOWNLOAD, COLLABORATE, PUBLISH_MARKUP, EDIT, CONTROL | 完全控制权限 |

## 查询示例

### 查询特定文件夹的权限

```sql
SELECT
    id,
    name,
    path,
    permissions,
    permissions_sync_time
FROM folders
WHERE id = 'urn:adsk.wipprod:fs.folder:co.-H8cmM_MR8uh4BRntHM0Tw';
```

### 查询所有有权限数据的文件夹

```sql
SELECT
    id,
    name,
    path,
    permissions->>'summary' as permission_summary,
    permissions_sync_time
FROM folders
WHERE permissions IS NOT NULL
  AND permissions != '{}'::jsonb
ORDER BY permissions_sync_time DESC;
```

### 查询特定用户的权限

```sql
SELECT
    f.id,
    f.name,
    f.path,
    u.value->>'name' as user_name,
    u.value->>'email' as user_email,
    u.value->>'permission_name' as permission_level
FROM folders f,
     jsonb_array_elements(f.permissions->'users') as u
WHERE u.value->>'email' = 'john.doe@example.com';
```

### 统计权限分布

```sql
SELECT
    COUNT(*) as total_folders,
    COUNT(CASE WHEN permissions IS NOT NULL AND permissions != '{}'::jsonb THEN 1 END) as folders_with_permissions,
    SUM((permissions->'summary'->>'users_count')::int) as total_user_permissions,
    SUM((permissions->'summary'->>'roles_count')::int) as total_role_permissions,
    SUM((permissions->'summary'->>'companies_count')::int) as total_company_permissions
FROM folders
WHERE project_id = 'b.1eea4119-3553-4167-b93d-3a3d5d07d33d';
```

### 查询最近同步的文件夹

```sql
SELECT
    id,
    name,
    path,
    permissions_sync_time,
    permissions->'summary' as summary
FROM folders
WHERE permissions_sync_time IS NOT NULL
ORDER BY permissions_sync_time DESC
LIMIT 10;
```

## 性能优化

### 索引

脚本依赖以下索引进行高效查询：

1. **GIN 索引** - 用于 JSONB 查询：
   ```sql
   CREATE INDEX idx_folders_permissions_gin ON folders USING GIN (permissions);
   ```

2. **同步时间索引** - 用于增量同步：
   ```sql
   CREATE INDEX idx_folders_permissions_sync_time
   ON folders (project_id, permissions_sync_time DESC)
   WHERE permissions_sync_time IS NOT NULL;
   ```

### 批量更新

- 默认批量大小：50 个文件夹/批次
- 可通过 `--batch-size` 参数调整
- 使用 PostgreSQL 事务确保数据一致性

### 速率限制

- 默认 API 调用延迟：0.2 秒
- 可通过 `--delay` 参数调整
- 避免触发 ACC API 限流（429 错误）

## 错误处理

脚本包含以下错误处理机制：

1. **API 错误处理**：
   - 403: 权限不足
   - 404: 文件夹不存在
   - 429: API 限流
   - 超时处理

2. **数据库错误**：
   - 连接失败重试
   - 事务回滚

3. **统计错误信息**：
   ```json
   {
     "errors": [
       {
         "folder_id": "...",
         "folder_name": "...",
         "folder_path": "...",
         "error": "权限不足",
         "error_code": "INSUFFICIENT_PERMISSIONS",
         "http_status": 403
       }
     ]
   }
   ```

## 输出示例

```
Starting permissions sync for project b.1eea4119-3553-4167-b93d-3a3d5d07d33d...
2025-11-19 17:45:30,123 - INFO - 正在连接到数据库: neondb
2025-11-19 17:45:31,456 - INFO - 成功连接到数据库: neondb
2025-11-19 17:45:31,789 - INFO - 正在从数据库获取所有文件夹...
2025-11-19 17:45:32,012 - INFO - 找到 150 个文件夹，开始同步权限...
2025-11-19 17:45:32,234 - INFO - 同步文件夹权限 (1/150): Project Files
2025-11-19 17:45:33,456 - INFO - 批量更新了 50 个文件夹的权限
...
2025-11-19 17:50:15,789 - INFO - ==================================================
2025-11-19 17:50:15,790 - INFO - 权限同步完成!
2025-11-19 17:50:15,790 - INFO -   总文件夹数: 150
2025-11-19 17:50:15,790 - INFO -   成功同步: 145
2025-11-19 17:50:15,790 - INFO -   失败同步: 5
2025-11-19 17:50:15,790 - INFO -   总用户权限: 350
2025-11-19 17:50:15,790 - INFO -   总角色权限: 120
2025-11-19 17:50:15,790 - INFO -   总公司权限: 15
2025-11-19 17:50:15,790 - INFO -   耗时: 283.01 秒
2025-11-19 17:50:15,790 - INFO - ==================================================
```

## 相关文件

- **Schema 文件**: `database_sql/optimized_schema_v2.sql`
- **迁移脚本**: `database_sql/add_permissions_column.sql`
- **同步脚本**: `api_modules/permissions_db_sync.py`
- **权限 API**: `api_modules/permissions_sync_api.py`（原始 API 模块）

## 注意事项

1. **认证要求**：需要先通过 Web 界面登录获取 Access Token
2. **数据库**：所有表都在 `neondb` 数据库中，不是独立的项目数据库
3. **API 限制**：注意 ACC API 的速率限制，适当调整 `--delay` 参数
4. **权限要求**：需要至少有 VIEW 权限才能查看文件夹权限
5. **数据量**：大型项目可能需要较长时间完成同步

## 故障排查

### 数据库连接失败

```
错误: database "acc_project_..." does not exist
```

**解决方案**：检查是否使用正确的数据库名称 `neondb`

### 认证失败

```
错误: 未找到 Access Token，请先进行认证
```

**解决方案**：
1. 访问 http://localhost:8080/login
2. 完成 OAuth 登录
3. 重新运行脚本

### API 限流

```
错误: 请求过于频繁，请稍后重试
```

**解决方案**：增加 `--delay` 参数值：
```bash
python api_modules/permissions_db_sync.py --delay 0.5
```

## 未来改进

- [ ] 增量同步（仅同步变更的文件夹）
- [ ] 并发 API 调用（使用 asyncio + aiohttp）
- [ ] 权限变更通知
- [ ] 权限审计报告生成
- [ ] 支持命令行指定特定文件夹

## 许可

内部使用工具
