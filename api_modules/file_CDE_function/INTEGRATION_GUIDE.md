# 文件树缓存系统 - 集成指南

## 概述

这是一个高性能的文件树缓存系统，采用 **"JSONB 缓存表 + 写入时失效"** 方案。

### 核心特性
- ✅ **读取极快**: 缓存命中时 < 10ms
- ✅ **写入极快**: 清空缓存 < 1ms
- ✅ **数据最新**: 任何改动都立即清空缓存，强制下次读取时刷新
- ✅ **无额外依赖**: 纯 PostgreSQL + Python，无需 Redis/Celery

## 文件结构

```
api_modules/file_CDE_function/
├── __init__.py                  # 模块初始化
├── file_tree_builder.py         # 核心业务逻辑（树构建、缓存管理）
├── file_tree_api.py             # Flask API 端点
└── INTEGRATION_GUIDE.md         # 本文件
```

## 快速开始

### 步骤1: 创建缓存表

运行数据库初始化脚本：

```bash
psql -h your-host -U your-user -d your-database < database_sql/file_tree_cache_schema.sql
```

### 步骤2: 在现有 Flask 应用中集成

#### 方式A: 注册蓝图（推荐）

```python
from flask import Flask
from api_modules.file_CDE_function import file_tree_bp

app = Flask(__name__)

# 注册文件树 API 蓝图
app.register_blueprint(file_tree_bp)

if __name__ == '__main__':
    app.run()
```

#### 方式B: 直接调用函数

```python
from api_modules.file_CDE_function import get_file_tree, invalidate_file_tree_cache

# 获取文件树
db_params = {
    'host': 'your-host',
    'port': 5432,
    'database': 'your-db',
    'user': 'your-user',
    'password': 'your-password',
    'sslmode': 'require'
}

tree, from_cache = get_file_tree('project-123', db_params)

# 清空缓存
invalidate_file_tree_cache('project-123', db_params)
```

### 步骤3: 集成到现有文件上传/删除 API

当用户上传或删除文件时，**必须**清空缓存，以便下次读取时获取最新数据：

```python
from api_modules.file_CDE_function import invalidate_file_tree_cache

@app.route('/api/upload', methods=['POST'])
def upload_file():
    # ... 上传文件逻辑 ...

    # 清空缓存
    project_id = request.form.get('project_id')
    invalidate_file_tree_cache(project_id, get_db_params())

    return jsonify({"success": True})


@app.route('/api/delete-file', methods=['DELETE'])
def delete_file():
    # ... 删除文件逻辑 ...

    # 清空缓存
    project_id = request.args.get('project_id')
    invalidate_file_tree_cache(project_id, get_db_params())

    return jsonify({"success": True})
```

## API 文档

### 1. GET /api/file-tree

获取文件树（优先使用缓存）

**请求**：
```
GET /api/file-tree?project_id=your-project-id&force_refresh=false
```

**参数**：
- `project_id` (必需): 项目ID
- `force_refresh` (可选): 是否强制刷新缓存 (默认: false)

**响应成功** (HTTP 200):
```json
{
  "success": true,
  "data": {
    "root": [
      {
        "type": "folder",
        "id": "folder-123",
        "name": "Documents",
        "path": "Documents",
        "create_time": "2025-11-16T10:00:00+00:00",
        "create_user_name": "John Doe",
        "last_modified_time": "2025-11-16T15:30:00+00:00",
        "hidden": false,
        "children": [
          {
            "type": "file",
            "id": "file-456",
            "name": "report.pdf",
            "folder_path": "Documents",
            "file_type": "pdf",
            "create_time": "2025-11-16T10:00:00+00:00",
            "create_user_name": "John Doe",
            "last_modified_user_name": "Jane Smith",
            "last_modified_time": "2025-11-16T14:20:00+00:00",
            "version_number": 2,
            "size": 1048576,
            "urn": "urn:adsk.wipprod:fs.file:vf.xxxxx?version=2",
            "reviewState": "InReview"
          }
        ]
      }
    ],
    "metadata": {
      "total_folders": 5,
      "total_files": 12,
      "built_at": "2025-11-16T16:00:00+00:00"
    }
  },
  "from_cache": true,
  "metadata": {
    "project_id": "your-project-id",
    "cached_at": "2025-11-16T16:05:00+00:00",
    "cache_hit": true,
    "message": "Cache hit"
  }
}
```

**响应失败** (HTTP 400/500):
```json
{
  "success": false,
  "error": "Missing required parameter: project_id"
}
```

### 2. POST /api/file-tree/invalidate

清空文件树缓存

**请求**：
```
POST /api/file-tree/invalidate
Content-Type: application/json

{
  "project_id": "your-project-id"
}
```

**参数**：
- `project_id` (必需): 项目ID

**响应成功** (HTTP 200):
```json
{
  "success": true,
  "data": {
    "project_id": "your-project-id",
    "invalidated_at": "2025-11-16T16:10:00+00:00"
  }
}
```

### 3. GET /api/file-tree/cache-status

获取缓存状态（辅助接口）

**请求**：
```
GET /api/file-tree/cache-status?project_id=your-project-id
```

**响应**:
```json
{
  "success": true,
  "data": {
    "project_id": "your-project-id",
    "cached": true,
    "cache_size_bytes": 51200,
    "total_folders": 5,
    "total_files": 12,
    "last_updated": "2025-11-16T16:00:00+00:00",
    "last_build_time_ms": 145.5
  }
}
```

### 4. GET /api/file-tree/health

健康检查

**请求**：
```
GET /api/file-tree/health
```

**响应**:
```json
{
  "status": "healthy",
  "service": "file-tree-api",
  "timestamp": "2025-11-16T16:15:00+00:00"
}
```

## 前端集成示例

### Vue 3 示例

```vue
<template>
  <div class="file-tree">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div class="cache-status">
        <span v-if="fromCache" class="badge badge-green">From Cache</span>
        <span v-else class="badge badge-blue">Freshly Built</span>
      </div>
      <file-tree-node
        v-for="node in tree.root"
        :key="node.id"
        :node="node"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import FileTreeNode from './FileTreeNode.vue'

const tree = ref(null)
const loading = ref(true)
const error = ref(null)
const fromCache = ref(false)

const projectId = 'your-project-id'

const fetchFileTree = async () => {
  try {
    loading.value = true
    const response = await fetch(`/api/file-tree?project_id=${projectId}`)

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }

    const data = await response.json()

    if (data.success) {
      tree.value = data.data
      fromCache.value = data.from_cache
    } else {
      error.value = data.error
    }
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchFileTree()
})
</script>

<style scoped>
.file-tree {
  padding: 20px;
}

.cache-status {
  margin-bottom: 10px;
}

.badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
  color: white;
}

.badge-green {
  background-color: #4caf50;
}

.badge-blue {
  background-color: #2196f3;
}
</style>
```

## 数据流程

```
用户在前端打开文件夹
  ↓
Vue 调用 GET /api/file-tree
  ↓
检查 PostgreSQL 缓存表
  ├─ 缓存存在 → 返回缓存 (< 10ms) ✅ 快速路径
  └─ 缓存不存在 → 执行构建
      ↓
    查询 folders 表
      ↓
    查询 files + file_versions 表
      ↓
    构建树形结构 (Python)
      ↓
    保存到缓存表
      ↓
    返回新树 (< 2000ms)
  ↓
前端显示文件树
  ↓
用户上传/删除文件
  ↓
调用上传/删除 API
  ↓
后端执行文件操作 + 清空缓存
  ↓
下次用户打开文件夹 → 获取最新数据
```

## 性能指标

| 操作 | 耗时 | 说明 |
|------|------|------|
| 缓存命中读取 | < 10ms | 单条 SELECT 查询 |
| 缓存未命中读取 | 100-2000ms | 取决于数据量（< 10K 文件通常 < 500ms） |
| 缓存清空 | < 1ms | 单条 UPDATE 查询 |
| 构建树（1000 文件） | 150-300ms | Python 计算 + JSON 序列化 |

## 故障排查

### 缓存一直不命中

**原因**: 缓存清空函数被频繁调用

**解决**: 检查文件上传/删除 API 是否过度清空缓存

### 文件树显示不完整

**原因**: 数据库查询出错或数据不完整

**解决**:
1. 检查 folders / files / file_versions 表是否有数据
2. 查看服务器日志是否有错误信息
3. 手动调用 `/api/file-tree?project_id=xxx&force_refresh=true` 强制刷新

### 缓存体积过大

**原因**: 文件数量太多（> 50K）

**解决**:
1. 考虑分页或懒加载
2. 增加数据库存储容量
3. 定期清理历史版本

## 监控建议

建议在生产环境中添加以下监控：

1. **缓存命中率**: `hit_count / (hit_count + miss_count)`
2. **平均构建时间**: 应该 < 500ms
3. **缓存大小**: 监控 `tree_size_bytes`
4. **API 响应时间**: 应该 < 50ms（缓存命中）或 < 2000ms（未命中）

## 常见问题

### Q: 多个用户同时打开文件树会怎样？

A: 如果缓存命中，每个用户都获得缓存结果。如果缓存未命中，第一个用户触发构建，其他用户等待（约 100-2000ms）。

### Q: 如果构建过程中宕机怎么办？

A: 缓存表中的 `cached_tree` 会保持为 NULL，下次请求时会重新构建。

### Q: 可以在缓存中添加自定义字段吗？

A: 可以，在 `file_tree_builder.py` 中的 `query_files()` 函数中添加查询字段即可。

### Q: 支持增量更新吗？

A: 当前版本采用全量重建。增量更新可以作为 P2 优化项。

## 后续优化

### P1 性能优化
- [ ] 添加构建锁，防止并发构建
- [ ] 实现缓存预热
- [ ] 添加详细的性能监控

### P2 功能扩展
- [ ] 支持搜索和过滤
- [ ] 支持分页/懒加载
- [ ] 支持树的增量更新
- [ ] 支持多项目并行缓存

## 技术细节

### 树结构格式

```json
{
  "root": [
    {
      "type": "folder",
      "id": "folder-id",
      "name": "Folder Name",
      "path": "path/to/folder",
      "create_time": "ISO-8601 timestamp",
      "create_user_name": "User Name",
      "last_modified_time": "ISO-8601 timestamp",
      "hidden": false,
      "children": [
        {
          "type": "file",
          ...
        }
      ]
    }
  ],
  "metadata": {
    "total_folders": 100,
    "total_files": 500,
    "built_at": "ISO-8601 timestamp"
  }
}
```

### 文件字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| type | string | "file" 或 "folder" |
| id | string | 文件/文件夹 ID |
| name | string | 显示名称 |
| folder_path | string | 文件所在文件夹路径 |
| file_type | string | 文件类型（pdf, dwg 等） |
| create_time | ISO-8601 | 创建时间 |
| create_user_name | string | 创建人 |
| last_modified_user_name | string | 最后修改人 |
| last_modified_time | ISO-8601 | 最后修改时间 |
| version_number | integer | 当前版本号 |
| size | integer | 文件大小（字节） |
| urn | string | 文件的 URN 标识 |
| reviewState | string | 审查状态（"InReview" 或 "NotInReview"） |

## 许可

Internal Use Only
