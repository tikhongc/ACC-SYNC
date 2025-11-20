# Transmittal CDE Function API

传输单内容交付环境(CDE)功能的后端API模块。

## 📋 概述

本模块提供了完整的传输单管理API，包括:
- 传输单列表查询
- 文档列表获取
- 接收者管理
- 用户行为追踪(查看/下载)
- 批量文件打包下载

## 🚀 快速开始

### 1. 注册 Blueprint

在主应用中注册 Blueprint:

```python
from api_modules.transmittal_CDE_function.transmittal import transmittal_bp

# Flask 应用
app.register_blueprint(transmittal_bp)
```

所有 API 将自动挂载到 `/api/transmittals` 路径下。

### 2. 依赖项

确保以下模块已正确安装和配置:

- ✅ PostgreSQL 数据库 (通过 `NeonConfig`)
- ✅ Transmittal 数据库表 (参考 `database_sql/transmittal_schema.sql`)
- ✅ URN 下载管理器 (`api_modules/urn_download_simple.py`)
- ✅ 认证工具 (`utils.get_access_token()`)

## 📡 API 端点

### API 1: 获取传输单列表

获取指定项目的传输单列表，支持分页。

**请求:**
```http
GET /api/transmittals/<project_id>/list?limit=100&offset=0
```

**参数:**
- `project_id` (路径参数) - 项目ID (支持 `b.xxx` 格式)
- `limit` (查询参数) - 每页数量，默认100，最大1000
- `offset` (查询参数) - 偏移量，默认0

**响应示例:**
```json
{
  "success": true,
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "bim360_project_id": "1eea4119-3553-4167-b93d-3a3d5d07d33d",
      "sequence_id": 5,
      "title": "设计图纸传输 - 第一批",
      "status": 2,
      "docs_count": 10,
      "create_user_name": "张三",
      "created_at": "2025-01-18T10:30:45Z",
      "updated_at": "2025-01-18T15:20:30Z"
    }
  ],
  "total": 25,
  "limit": 100,
  "offset": 0
}
```

---

### API 2: 获取传输单文档列表

获取指定传输单包含的所有文档。

**请求:**
```http
GET /api/transmittals/<transmittal_id>/documents
```

**参数:**
- `transmittal_id` (路径参数) - 传输单ID (UUID)

**响应示例:**
```json
{
  "success": true,
  "transmittal_id": "550e8400-e29b-41d4-a716-446655440000",
  "data": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "workflow_transmittal_id": "550e8400-e29b-41d4-a716-446655440000",
      "urn": "urn:adsk.wipprod:dm.lineage:abc123",
      "file_name": "建筑平面图.dwg",
      "version_number": 3,
      "revision_number": "A",
      "last_modified_time": "2025-01-18T09:15:00Z",
      "last_modified_user_name": "李四"
    }
  ],
  "count": 10
}
```

---

### API 3: 获取传输单接收者列表

获取传输单的所有接收者(包括项目成员和外部接收者)。

**请求:**
```http
GET /api/transmittals/<transmittal_id>/recipients
```

**参数:**
- `transmittal_id` (路径参数) - 传输单ID (UUID)

**响应示例:**
```json
{
  "success": true,
  "transmittal_id": "550e8400-e29b-41d4-a716-446655440000",
  "data": {
    "members": [
      {
        "id": "770e8400-e29b-41d4-a716-446655440002",
        "type": "member",
        "user_name": "王五",
        "email": "wangwu@example.com",
        "company_name": "ABC建筑事务所",
        "viewed_at": "2025-01-18T11:30:00Z",
        "downloaded_at": "2025-01-18T11:35:00Z"
      }
    ],
    "non_members": [
      {
        "id": "880e8400-e29b-41d4-a716-446655440003",
        "type": "non_member",
        "email": "external@contractor.com",
        "first_name": "赵",
        "last_name": "六",
        "company_name": "XYZ施工公司",
        "viewed_at": null,
        "downloaded_at": null
      }
    ]
  },
  "total_count": 15
}
```

---

### API 4: 标记用户已查看

更新指定用户的查看时间戳。

**请求:**
```http
POST /api/transmittals/<transmittal_id>/mark-viewed
Content-Type: application/json

{
  "email": "user@example.com"
}
```

**参数:**
- `transmittal_id` (路径参数) - 传输单ID (UUID)
- `email` (请求体) - 用户邮箱

**响应示例:**
```json
{
  "success": true,
  "transmittal_id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "viewed_at": "2025-01-18T16:45:30Z",
  "user_type": "member",
  "user_name": "张三"
}
```

**注意:**
- 仅更新尚未查看的记录 (`viewed_at IS NULL`)
- 自动识别用户类型(项目成员或外部接收者)
- 如果用户已查看或不存在，返回 404

---

### API 5: 标记用户已下载

更新指定用户的下载时间戳。

**请求:**
```http
POST /api/transmittals/<transmittal_id>/mark-downloaded
Content-Type: application/json

{
  "email": "user@example.com"
}
```

**参数:**
- `transmittal_id` (路径参数) - 传输单ID (UUID)
- `email` (请求体) - 用户邮箱

**响应示例:**
```json
{
  "success": true,
  "transmittal_id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "downloaded_at": "2025-01-18T16:50:00Z",
  "user_type": "member",
  "user_name": "张三"
}
```

**特殊功能:**
- 下载操作会自动设置 `viewed_at` (如果尚未设置)
- 仅更新尚未下载的记录 (`downloaded_at IS NULL`)
- 自动识别用户类型(项目成员或外部接收者)

---

### API 6: 打包下载传输单文件 (ZIP)

批量下载传输单的所有文档，打包成 ZIP 文件。

**请求:**
```http
POST /api/transmittals/<transmittal_id>/download-zip
Content-Type: application/json

{
  "email": "user@example.com"  // 可选
}
```

**参数:**
- `transmittal_id` (路径参数) - 传输单ID (UUID)
- `email` (请求体，可选) - 如果提供，会自动标记该用户已下载

**响应:**
- **成功**: 返回 ZIP 文件流 (`application/zip`)
- **失败**: 返回 JSON 错误信息

**响应头:**
```http
Content-Type: application/zip
Content-Disposition: attachment; filename="transmittal_title_20250118_165030.zip"
X-File-Count: 10
X-Total-Size: 52428800
X-Failed-Files: [...]  // 仅在部分文件下载失败时出现
```

**下载示例 (JavaScript):**
```javascript
fetch('/api/transmittals/550e8400-e29b-41d4-a716-446655440000/download-zip', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'user@example.com'
  })
})
.then(response => {
  // 检查失败文件
  const failedFiles = response.headers.get('X-Failed-Files');
  if (failedFiles) {
    console.warn('部分文件下载失败:', JSON.parse(failedFiles));
  }

  return response.blob();
})
.then(blob => {
  // 触发浏览器下载
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'transmittal.zip';
  a.click();
  window.URL.revokeObjectURL(url);
});
```

**注意事项:**
- ⏱️ 下载大量文件可能需要较长时间（取决于文件数量和大小）
- 🗑️ ZIP 文件会在发送后 5 分钟自动清理
- ⚠️ 如果部分文件下载失败，仍会创建 ZIP（包含成功的文件），失败列表在响应头中
- 🔐 需要有效的 ACC API token

**工作流程:**
1. 从数据库查询传输单的所有文档 URN
2. 使用 `URNDownloadManager` 获取每个文件的下载链接
3. 批量下载文件到临时目录
4. 将所有文件打包成 ZIP
5. 返回 ZIP 文件流
6. 调度后台任务清理临时文件

---

## 🔧 错误处理

所有 API 使用统一的错误响应格式:

**错误响应示例:**
```json
{
  "success": false,
  "error": "错误描述信息",
  "error_type": "database_error|validation_error|internal_error"
}
```

**常见错误类型:**

| HTTP 状态码 | error_type | 说明 |
|-----------|------------|------|
| 400 | validation_error | 参数验证失败 |
| 401 | unauthorized | 认证失败或 token 缺失 |
| 404 | not_found | 资源不存在 |
| 500 | database_error | 数据库操作失败 |
| 500 | internal_error | 内部服务器错误 |
| 500 | zip_creation_failed | ZIP 创建失败 |

---

## 🛠️ 技术实现

### 核心组件

1. **TransmittalManager** - 业务逻辑管理器
   - 数据库连接管理
   - CRUD 操作封装
   - ZIP 创建和文件下载

2. **URNDownloadManager** - 文件下载管理器
   - 支持 Document Lineage URN
   - 支持 OSS Object URN
   - 自动获取签名下载链接

3. **ZipFileCleanup** - ZIP 文件清理管理器
   - 延迟清理机制(默认5分钟)
   - 后台线程清理
   - 应用退出时强制清理

### 数据库连接

使用 `NeonConfig` 获取 PostgreSQL 连接参数:

```python
from database_sql.neon_config import NeonConfig

config = NeonConfig()
db_params = config.get_db_params()
conn = psycopg2.connect(**db_params)
```

### 文件名安全化

所有文件名会自动清理非法字符:

```python
# Windows 非法字符: < > : " / \ | ? *
safe_filename = self._sanitize_filename("原始文件名.dwg")
```

### 版本号处理

文档版本号会自动添加到文件名:

```
原始: 建筑平面图.dwg (version 3)
结果: 建筑平面图_v3.dwg
```

---

## 📊 性能优化

### 1. 批量下载优化

- 使用流式下载 (`stream=True`)
- 8KB 缓冲区读取
- 临时文件存储

### 2. ZIP 压缩

- 使用 `ZIP_DEFLATED` 压缩算法
- 边下载边打包(减少内存占用)

### 3. 资源清理

- 自动关闭数据库连接 (`try-finally`)
- 临时目录立即清理
- ZIP 文件延迟清理(5分钟)

---

## 🔒 安全考虑

1. **参数验证**
   - UUID 格式验证
   - Email 格式验证
   - 分页参数范围检查

2. **文件安全**
   - 文件名清理(防止路径遍历)
   - 临时文件隔离
   - 自动清理机制

3. **访问控制**
   - Token 认证检查
   - 项目权限验证(通过 project_id)

---

## 📝 使用示例

### Python 客户端

```python
import requests

BASE_URL = 'http://localhost:5000/api/transmittals'
PROJECT_ID = 'b.1eea4119-3553-4167-b93d-3a3d5d07d33d'
TRANSMITTAL_ID = '550e8400-e29b-41d4-a716-446655440000'

# 1. 获取传输单列表
response = requests.get(f'{BASE_URL}/{PROJECT_ID}/list?limit=20')
transmittals = response.json()

# 2. 获取文档列表
response = requests.get(f'{BASE_URL}/{TRANSMITTAL_ID}/documents')
documents = response.json()

# 3. 标记已查看
response = requests.post(
    f'{BASE_URL}/{TRANSMITTAL_ID}/mark-viewed',
    json={'email': 'user@example.com'}
)

# 4. 下载 ZIP
response = requests.post(
    f'{BASE_URL}/{TRANSMITTAL_ID}/download-zip',
    json={'email': 'user@example.com'}
)

if response.status_code == 200:
    with open('transmittal.zip', 'wb') as f:
        f.write(response.content)
    print(f"Downloaded: {response.headers.get('Content-Disposition')}")
```

### cURL 示例

```bash
# 获取传输单列表
curl "http://localhost:5000/api/transmittals/b.1eea4119-3553-4167-b93d-3a3d5d07d33d/list?limit=10"

# 标记已查看
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com"}' \
  "http://localhost:5000/api/transmittals/550e8400-e29b-41d4-a716-446655440000/mark-viewed"

# 下载 ZIP
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com"}' \
  --output transmittal.zip \
  "http://localhost:5000/api/transmittals/550e8400-e29b-41d4-a716-446655440000/download-zip"
```

---

## 🐛 故障排查

### 问题 1: Access token not found

**错误:**
```json
{
  "success": false,
  "error": "Access token not found",
  "error_type": "unauthorized"
}
```

**解决方法:**
- 确保 `utils.get_access_token()` 已正确配置
- 检查 OAuth 认证流程
- 验证 token 是否过期

---

### 问题 2: 数据库连接失败

**错误:**
```json
{
  "success": false,
  "error": "Database operation failed: ...",
  "error_type": "database_error"
}
```

**解决方法:**
```bash
# 检查数据库配置
python -c "from database_sql.neon_config import NeonConfig; print(NeonConfig().get_db_params())"

# 测试连接
psql -h <host> -U <user> -d <database>
```

---

### 问题 3: ZIP 下载失败

**错误:**
```json
{
  "success": false,
  "error": "No files were successfully downloaded",
  "failed_files": [...]
}
```

**可能原因:**
- URN 格式不正确
- ACC API 权限不足
- 网络连接问题
- 文件已被删除

**调试方法:**
- 检查服务器日志 (`[ZIP]` 前缀)
- 验证 URN 格式
- 测试 ACC API 连接

---

## 📚 相关文档

- **数据库模块**: [database_sql/TRANSMITTAL_MODULE_README.md](../../database_sql/TRANSMITTAL_MODULE_README.md)
- **URN 下载器**: [api_modules/urn_download_simple.py](../urn_download_simple.py)
- **数据库架构**: [database_sql/transmittal_schema.sql](../../database_sql/transmittal_schema.sql)

---

## 📝 更新日志

### Version 1.0.0 (2025-01-19)

- ✅ API 1: 传输单列表查询
- ✅ API 2: 文档列表获取
- ✅ API 3: 接收者列表获取
- ✅ API 4: 标记用户已查看
- ✅ API 5: 标记用户已下载
- ✅ API 6: ZIP 批量下载
- ✅ 自动文件清理机制
- ✅ 完整错误处理
- ✅ 文档和示例代码

---

## 🤝 贡献

如需添加新功能或修复 bug:

1. 编辑 `transmittal.py` 添加新的 API 或功能
2. 更新此 README 文档
3. 添加错误处理和日志记录
4. 测试所有边缘情况

---

## 📞 支持

如有问题或建议，请查阅:
- 主项目文档: [CLAUDE.md](../../CLAUDE.md)
- 数据库文档: [TRANSMITTAL_MODULE_README.md](../../database_sql/TRANSMITTAL_MODULE_README.md)
