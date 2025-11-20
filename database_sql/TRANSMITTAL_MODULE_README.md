# Transmittal Module Documentation

## 📋 概述

Transmittal（传输单）模块是 ACC-SYNC 系统的独立模块，用于管理项目文档的传输记录。该模块支持从 CSV 文件同步传输单数据到 PostgreSQL 数据库。

## 🏗️ 架构设计

### 数据库表结构

**四个核心表：**

1. **transmittals_workflow_transmittals** - 传输单主表
   - 存储传输单的基本信息（标题、状态、创建者等）
   - 主键：`id` (UUID)
   - 唯一约束：`(bim360_project_id, sequence_id)`

2. **transmittals_transmittal_documents** - 文档关联表
   - 存储传输单包含的文档列表
   - 外键：`workflow_transmittal_id` → `workflow_transmittals.id`
   - 唯一约束：`(workflow_transmittal_id, urn, version_number)`

3. **transmittals_transmittal_recipients** - 项目成员接收者表
   - 存储项目成员接收者及查看/下载状态
   - 外键：`workflow_transmittal_id` → `workflow_transmittals.id`
   - 唯一约束：`(workflow_transmittal_id, user_id)`
   - 追踪字段：`viewed_at`, `downloaded_at`

4. **transmittals_transmittal_non_members** - 外部接收者表
   - 存储非项目成员的外部接收者
   - 外键：`workflow_transmittal_id` → `workflow_transmittals.id`
   - 唯一约束：`(workflow_transmittal_id, email)`

### 表关系图

```
transmittals_workflow_transmittals (1)
    ├──< transmittals_transmittal_documents (M)
    ├──< transmittals_transmittal_recipients (M)
    └──< transmittals_transmittal_non_members (M)
```

### 数据库视图

**v_transmittal_summary** - 传输单汇总视图
- 包含文档数量、接收者数量、查看/下载统计

**v_recipient_engagement** - 接收者参与度视图
- 追踪接收者的查看和下载行为
- 计算查看时间和下载时间指标

## 📁 文件结构

```
ACC-SYNC/
├── database_sql/
│   ├── transmittal_schema.sql           # 数据库表结构定义
│   ├── create_transmittal_tables.py     # 表创建脚本
│   └── transmittal_data_access.py       # 数据访问层（DAL）
├── api_modules/
│   └── transmittal_csv_sync.py          # CSV 同步脚本
├── transmittal/                         # CSV 数据文件夹
│   ├── transmittals_workflow_transmittals.csv
│   ├── transmittals_transmittal_documents.csv
│   ├── transmittals_transmittal_recipients.csv
│   └── transmittals_transmittal_non_members.csv
└── test_transmittal_sync.py             # 测试脚本
```

## 🚀 快速开始

### 1. 创建数据库表

首先需要在项目数据库中创建 transmittal 表：

```bash
# 创建表结构
python database_sql/create_transmittal_tables.py <project_id>

# 示例
python database_sql/create_transmittal_tables.py b.1eea4119-3553-4167-b93d-3a3d5d07d33d
```

**选项：**
- `--drop` - 删除现有表后重新创建（⚠️ 谨慎使用！）

**输出示例：**
```
📖 Reading schema from: database_sql/transmittal_schema.sql
✓ Schema loaded (15234 characters)

🔌 Connecting to project database for: b.1eea4119-...
✓ Connected to: acc_project_1eea4119_3553_4167_b93d_3a3d5d07d33d

🔍 Checking existing tables...
  ○ transmittals_workflow_transmittals not found
  ○ transmittals_transmittal_documents not found
  ...

🏗️  Creating tables...

✅ Verifying created tables...
  ✓ transmittals_workflow_transmittals
    - Columns: 13
    - Rows: 0
  ...
```

### 2. 准备 CSV 数据文件

确保 `transmittal/` 文件夹中包含以下 4 个 CSV 文件：

- `transmittals_workflow_transmittals.csv` - 主传输单数据
- `transmittals_transmittal_documents.csv` - 文档关联数据
- `transmittals_transmittal_recipients.csv` - 项目成员接收者
- `transmittals_transmittal_non_members.csv` - 外部接收者

**CSV 文件要求：**
- UTF-8 编码（支持 BOM）
- 第一行必须是列名（header）
- 日期时间格式：ISO 8601（例如：`2024-01-18T10:30:45Z`）
- UUID 格式：标准 UUID 字符串
- 空值：空字符串或不填写

### 3. 执行 CSV 同步

```bash
# 从 CSV 文件同步到数据库
python api_modules/transmittal_csv_sync.py <project_id>

# 示例
python api_modules/transmittal_csv_sync.py b.1eea4119-3553-4167-b93d-3a3d5d07d33d
```

**同步流程：**
1. ✅ 验证 CSV 文件是否存在
2. 📖 读取所有 CSV 文件
3. 🔌 连接到项目数据库
4. 🗑️  清空现有 transmittal 数据（TRUNCATE CASCADE）
5. 💾 按顺序插入数据（主表 → 子表）
6. ✅ 验证同步结果

**输出示例：**
```
📋 Step 1: Validating CSV files...
✓ All 4 CSV files found in c:\...\transmittal

📖 Step 2: Reading CSV files...
  ✓ transmittals_workflow_transmittals.csv: 4 rows
  ✓ transmittals_transmittal_documents.csv: 9 rows
  ✓ transmittals_transmittal_recipients.csv: 12 rows
  ✓ transmittals_transmittal_non_members.csv: 0 rows

🔌 Step 3: Connecting to database...
✓ Connected to: acc_project_1eea4119_...

🗑️  Step 4: Clearing existing transmittal data...
  ✓ transmittals_transmittal_non_members
  ✓ transmittals_transmittal_recipients
  ✓ transmittals_transmittal_documents
  ✓ transmittals_workflow_transmittals

💾 Step 5: Inserting data into database...
  → Inserting workflow_transmittals...
    ✓ 4 records inserted
  → Inserting transmittal_documents...
    ✓ 9 records inserted
  ...

✅ Step 6: Verifying sync...
  ✓ workflow_transmittals: 4 records
  ✓ transmittal_documents: 9 records
  ✓ transmittal_recipients: 12 records
  ✓ transmittal_non_members: 0 records

======================================================================
📊 TRANSMITTAL CSV FULL SYNC REPORT
======================================================================
Status: ✅ SUCCESS
Total Records: 25
Duration: 0.8s
```

### 4. 运行测试

验证模块功能是否正常：

```bash
# 运行完整测试套件
python test_transmittal_sync.py <project_id>

# 示例
python test_transmittal_sync.py b.1eea4119-3553-4167-b93d-3a3d5d07d33d
```

**测试覆盖范围：**
1. 数据库连接测试
2. 表结构验证
3. CSV 文件验证
4. 完整同步操作测试
5. 数据完整性验证（外键关系）
6. 查询功能测试
7. 数据库视图测试

**输出示例：**
```
======================================================================
🧪 TRANSMITTAL MODULE TEST SUITE
======================================================================

🔧 Test 1: Database Connection
✅ PASS - Database Connection
  └─ Connected to acc_project_... (PostgreSQL 16.6)

🔧 Test 2: Table Structure Verification
✅ PASS - Table Structure
  └─ All 4 tables exist

...

======================================================================
📊 TEST SUMMARY
======================================================================
Total Tests: 7
Passed: 7 ✅
Failed: 0 ❌
Success Rate: 100.0%
```

## 💻 编程使用

### 数据访问层 (DAL) 使用

```python
import asyncio
from database_sql.multi_database_manager import ACCMultiDatabaseManager
from database_sql.transmittal_data_access import TransmittalDataAccess

async def example_usage():
    # 1. 获取数据库连接池
    db_manager = ACCMultiDatabaseManager()
    pool = await db_manager.get_project_database('b.xxx-xxx-xxx')

    # 2. 创建数据访问层实例
    dal = TransmittalDataAccess(pool)

    # 3. 查询传输单
    project_id = 'xxx-xxx-xxx'
    transmittals = await dal.get_transmittals_by_project(project_id, limit=10)

    # 4. 获取传输单详情
    transmittal_id = transmittals[0]['id']
    transmittal = await dal.get_transmittal_by_id(transmittal_id)

    # 5. 获取关联文档
    documents = await dal.get_documents_by_transmittal(transmittal_id)

    # 6. 获取接收者
    recipients = await dal.get_recipients_by_transmittal(transmittal_id)

    # 7. 更新接收者参与度
    from datetime import datetime
    await dal.update_recipient_engagement(
        transmittal_id=transmittal_id,
        user_id='xxx-xxx-xxx',
        viewed_at=datetime.now()
    )

    # 8. 搜索传输单
    results = await dal.search_transmittals(
        project_id=project_id,
        search_term='设计',
        status=2,
        limit=50
    )

    # 9. 获取汇总视图
    summary = await dal.get_transmittal_summary(transmittal_id)
    print(f"文档数量: {summary['actual_docs_count']}")
    print(f"接收者数量: {summary['recipient_count']}")
    print(f"已查看: {summary['viewed_count']}")

asyncio.run(example_usage())
```

### 批量操作

```python
async def batch_operations():
    dal = TransmittalDataAccess(pool)

    # 批量插入传输单
    transmittals = [
        {
            'id': 'xxx-xxx-xxx',
            'bim360_project_id': 'xxx-xxx-xxx',
            'sequence_id': 1,
            'title': '测试传输单',
            'status': 2,
            # ... 其他字段
        },
        # 更多传输单...
    ]
    inserted, updated = await dal.batch_upsert_transmittals(transmittals)
    print(f"插入: {inserted}, 更新: {updated}")

    # 批量插入文档
    documents = [...]
    inserted, updated = await dal.batch_upsert_documents(documents)

    # 获取表统计
    counts = await dal.get_table_counts()
    print(counts)
    # {'transmittals_workflow_transmittals': 4, ...}
```

## 🔍 数据库查询示例

### 直接 SQL 查询

```sql
-- 获取所有传输单及统计
SELECT * FROM v_transmittal_summary
ORDER BY created_at DESC;

-- 查看接收者参与度
SELECT * FROM v_recipient_engagement
WHERE engagement_status = 'Not Viewed';

-- 查找特定项目的传输单
SELECT * FROM transmittals_workflow_transmittals
WHERE bim360_project_id = 'xxx-xxx-xxx'
ORDER BY sequence_id DESC;

-- 获取传输单的所有文档
SELECT d.file_name, d.version_number, d.last_modified_time
FROM transmittals_transmittal_documents d
WHERE d.workflow_transmittal_id = 'xxx-xxx-xxx'
ORDER BY d.file_name;

-- 检查接收者是否查看/下载
SELECT
    r.user_name,
    r.email,
    CASE
        WHEN r.downloaded_at IS NOT NULL THEN '已下载'
        WHEN r.viewed_at IS NOT NULL THEN '已查看'
        ELSE '未查看'
    END AS status,
    r.viewed_at,
    r.downloaded_at
FROM transmittals_transmittal_recipients r
WHERE r.workflow_transmittal_id = 'xxx-xxx-xxx';
```

## 🛠️ 常见操作

### 清空所有 transmittal 数据

```python
async def clear_all_data():
    dal = TransmittalDataAccess(pool)
    result = await dal.truncate_all_tables()
    print(result)
    # {'transmittals_workflow_transmittals': True, ...}
```

### 重新同步数据

```bash
# 方法 1: 使用 CSV 同步脚本（推荐）
python api_modules/transmittal_csv_sync.py <project_id>

# 方法 2: 删除表后重建
python database_sql/create_transmittal_tables.py <project_id> --drop
python api_modules/transmittal_csv_sync.py <project_id>
```

## ⚠️ 注意事项

### 数据完整性

1. **外键约束**
   - 所有子表都有 `ON DELETE CASCADE` 约束
   - 删除传输单会自动删除所有关联数据

2. **唯一约束**
   - 同一传输单不能包含相同文档的相同版本
   - 同一传输单不能有重复的接收者
   - 项目内传输单序列号 (`sequence_id`) 必须唯一

3. **空值处理**
   - `create_user_company_id` 和 `create_user_company_name` 可为 NULL
   - `viewed_at` 和 `downloaded_at` 默认为 NULL（表示未查看/下载）
   - 外部接收者的 `first_name`, `last_name`, `company_name`, `role` 可为 NULL

### CSV 文件格式

1. **编码**：必须使用 UTF-8（支持 BOM）
2. **日期格式**：ISO 8601 格式（`2024-01-18T10:30:45Z`）
3. **UUID 格式**：标准格式（`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`）
4. **空值表示**：留空或空字符串

### 性能优化

1. **批量操作**：使用 DAL 的批量方法（`batch_upsert_*`）
2. **索引利用**：查询时使用索引字段（`sequence_id`, `created_at`, `status`）
3. **连接池**：复用数据库连接池，避免频繁创建连接

## 🔧 故障排查

### 问题：CSV 文件未找到

```
❌ Missing CSV files: transmittals_workflow_transmittals.csv
Expected location: c:\Projects\...\transmittal
```

**解决方法：**
- 确保 `transmittal/` 文件夹存在
- 确保所有 4 个 CSV 文件都在该文件夹中
- 检查文件名拼写是否正确

### 问题：数据库表不存在

```
❌ Database Error: relation "transmittals_workflow_transmittals" does not exist
```

**解决方法：**
```bash
# 创建表结构
python database_sql/create_transmittal_tables.py <project_id>
```

### 问题：外键约束失败

```
❌ Foreign key constraint violation
```

**解决方法：**
- 确保 CSV 文件中的 `workflow_transmittal_id` 在主表中存在
- 同步时会自动按正确顺序插入（主表 → 子表）
- 如果手动插入数据，需要先插入主表再插入子表

### 问题：UUID 格式错误

```
❌ invalid input syntax for type uuid
```

**解决方法：**
- 检查 CSV 文件中的 UUID 格式
- 确保格式为：`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
- 不要使用简短格式或其他变体

## 📚 相关文档

- **数据库架构**：[database_sql/transmittal_schema.sql](database_sql/transmittal_schema.sql)
- **ACC-SYNC 主文档**：[CLAUDE.md](CLAUDE.md)
- **多数据库架构**：参考 `ACCMultiDatabaseManager` 类

## 🤝 贡献

如需添加新功能或修复 bug：

1. 修改数据库 schema：编辑 `transmittal_schema.sql`
2. 更新 DAL：编辑 `transmittal_data_access.py`
3. 更新同步逻辑：编辑 `transmittal_csv_sync.py`
4. 添加测试：编辑 `test_transmittal_sync.py`

## 📝 更新日志

### Version 1.0.0 (2025-01-18)

- ✅ 初始版本发布
- ✅ 4 个核心表结构
- ✅ CSV 全量同步功能
- ✅ 完整的 DAL 层
- ✅ 数据库视图支持
- ✅ 综合测试套件
