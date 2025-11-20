# Forge Viewer URL 生成 API 文档

## 概述

本 API 提供 Autodesk Forge Viewer 预览链接的生成功能，支持单个和批量 URN 的 URL 生成。

**基础 URL**: `http://localhost:8080/api/forge-viewer`

## 功能特性

- ✅ 自动 base64 编码 URN
- ✅ 支持使用系统 token 或自定义 token
- ✅ 支持 GET 和 POST 两种请求方式
- ✅ 支持批量生成 Viewer URLs
- ✅ 完整的错误处理和日志记录
- ✅ 健康检查端点

## API 端点

### 1. 生成单个 Forge Viewer URL

#### GET `/api/forge-viewer/url`

**查询参数**:

| 参数 | 类型 | 必需 | 默认值 | 说明 |
|------|------|------|--------|------|
| `urn` | string | ✅ | - | 文件的 URN，例如：`urn:adsk.wipprod:fs.file:vf.xxx?version=1` |
| `use_current_token` | boolean | ❌ | `true` | 是否使用当前系统的 access token |
| `token` | string | ❌ | - | 自定义 access token (当 `use_current_token=false` 时需要) |

**示例请求**:

```bash
# 使用系统 token
curl "http://localhost:8080/api/forge-viewer/url?urn=urn:adsk.wipprod:fs.file:vf.BpecaZkCRhSpeKT3CXYIiA?version=1&use_current_token=true"

# 使用自定义 token
curl "http://localhost:8080/api/forge-viewer/url?urn=urn:adsk.wipprod:fs.file:vf.xxx&use_current_token=false&token=YOUR_TOKEN_HERE"
```

**成功响应** (200):

```json
{
  "success": true,
  "data": {
    "viewer_url": "https://example.jarvisbim.com.cn/help/online-forge-viewer?urn=dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLkJwZWNhWmtDUmhTcGVrVDNDWFlJaUE/dmVyc2lvbj0x&token=eyJhbGci...",
    "urn": "urn:adsk.wipprod:fs.file:vf.BpecaZkCRhSpeKT3CXYIiA?version=1",
    "urn_encoded": "dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLkJwZWNhWmtDUmhTcGVrVDNDWFlJaUE/dmVyc2lvbj0x",
    "token_used": "eyJhbGciOiJSUzI1NiI...",
    "generated_at": "2025-11-20T10:00:00.000Z"
  }
}
```

---

#### POST `/api/forge-viewer/url`

**请求体**:

```json
{
  "urn": "urn:adsk.wipprod:fs.file:vf.BpecaZkCRhSpeKT3CXYIiA?version=1",
  "use_current_token": true,  // 可选，默认 true
  "token": "custom_token"     // 可选，自定义 token
}
```

**示例请求**:

```bash
curl -X POST "http://localhost:8080/api/forge-viewer/url" \
  -H "Content-Type: application/json" \
  -d '{
    "urn": "urn:adsk.wipprod:fs.file:vf.BpecaZkCRhSpeKT3CXYIiA?version=1",
    "use_current_token": true
  }'
```

**成功响应**: 与 GET 请求相同

---

### 2. 批量生成 Forge Viewer URLs

#### POST `/api/forge-viewer/batch-urls`

**请求体**:

```json
{
  "urns": [
    "urn:adsk.wipprod:fs.file:vf.xxx?version=1",
    "urn:adsk.wipprod:fs.file:vf.yyy?version=2"
  ],
  "use_current_token": true,  // 可选，默认 true
  "token": "custom_token"     // 可选，自定义 token
}
```

**示例请求**:

```bash
curl -X POST "http://localhost:8080/api/forge-viewer/batch-urls" \
  -H "Content-Type: application/json" \
  -d '{
    "urns": [
      "urn:adsk.wipprod:fs.file:vf.BpecaZkCRhSpeKT3CXYIiA?version=1",
      "urn:adsk.wipprod:fs.file:vf.XyzExample123?version=2"
    ],
    "use_current_token": true
  }'
```

**成功响应** (200):

```json
{
  "success": true,
  "data": {
    "total": 2,
    "results": [
      {
        "urn": "urn:adsk.wipprod:fs.file:vf.BpecaZkCRhSpeKT3CXYIiA?version=1",
        "urn_encoded": "dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLkJwZWNhWmtDUmhTcGVrVDNDWFlJaUE/dmVyc2lvbj0x",
        "viewer_url": "https://example.jarvisbim.com.cn/help/online-forge-viewer?urn=...&token=...",
        "success": true
      },
      {
        "urn": "urn:adsk.wipprod:fs.file:vf.XyzExample123?version=2",
        "urn_encoded": "dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLlh5ekV4YW1wbGUxMjM/dmVyc2lvbj0y",
        "viewer_url": "https://example.jarvisbim.com.cn/help/online-forge-viewer?urn=...&token=...",
        "success": true
      }
    ],
    "generated_at": "2025-11-20T10:00:00.000Z"
  }
}
```

---

### 3. 健康检查

#### GET `/api/forge-viewer/health`

**示例请求**:

```bash
curl "http://localhost:8080/api/forge-viewer/health"
```

**成功响应** (200):

```json
{
  "status": "healthy",
  "service": "forge-viewer-api",
  "timestamp": "2025-11-20T10:00:00.000Z",
  "base_url": "https://example.jarvisbim.com.cn/help/online-forge-viewer"
}
```

---

## 错误响应

### 400 Bad Request

缺少必需参数或参数格式错误：

```json
{
  "success": false,
  "error": "Missing required parameter: urn"
}
```

### 401 Unauthorized

无法获取 access token：

```json
{
  "success": false,
  "error": "Failed to get access token. Please ensure you are authenticated."
}
```

### 500 Internal Server Error

服务器内部错误：

```json
{
  "success": false,
  "error": "Internal server error: <error details>"
}
```

---

## 使用示例

### Python 示例

```python
import requests
import json

# 1. 使用 GET 请求生成单个 URL
urn = "urn:adsk.wipprod:fs.file:vf.BpecaZkCRhSpeKT3CXYIiA?version=1"
response = requests.get(
    "http://localhost:8080/api/forge-viewer/url",
    params={'urn': urn, 'use_current_token': 'true'}
)
data = response.json()
if data['success']:
    print(f"Viewer URL: {data['data']['viewer_url']}")

# 2. 使用 POST 请求批量生成 URLs
urns = [
    "urn:adsk.wipprod:fs.file:vf.xxx?version=1",
    "urn:adsk.wipprod:fs.file:vf.yyy?version=2"
]
response = requests.post(
    "http://localhost:8080/api/forge-viewer/batch-urls",
    json={'urns': urns, 'use_current_token': True}
)
data = response.json()
if data['success']:
    for result in data['data']['results']:
        print(f"URN: {result['urn']}")
        print(f"URL: {result['viewer_url']}\n")
```

### JavaScript 示例

```javascript
// 1. 使用 fetch 生成单个 URL
const urn = "urn:adsk.wipprod:fs.file:vf.BpecaZkCRhSpeKT3CXYIiA?version=1";
const response = await fetch(
  `http://localhost:8080/api/forge-viewer/url?urn=${encodeURIComponent(urn)}&use_current_token=true`
);
const data = await response.json();
if (data.success) {
  console.log('Viewer URL:', data.data.viewer_url);
}

// 2. 使用 POST 批量生成 URLs
const urns = [
  "urn:adsk.wipprod:fs.file:vf.xxx?version=1",
  "urn:adsk.wipprod:fs.file:vf.yyy?version=2"
];
const response = await fetch('http://localhost:8080/api/forge-viewer/batch-urls', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ urns, use_current_token: true })
});
const data = await response.json();
if (data.success) {
  data.data.results.forEach(result => {
    console.log('URN:', result.urn);
    console.log('URL:', result.viewer_url);
  });
}
```

### Vue.js 示例

```vue
<script setup>
import { ref } from 'vue'
import axios from 'axios'

const urn = ref('')
const viewerUrl = ref('')

async function generateViewerUrl() {
  try {
    const response = await axios.post('http://localhost:8080/api/forge-viewer/url', {
      urn: urn.value,
      use_current_token: true
    })

    if (response.data.success) {
      viewerUrl.value = response.data.data.viewer_url
      // 可以直接在新窗口打开
      window.open(viewerUrl.value, '_blank')
    }
  } catch (error) {
    console.error('生成 Viewer URL 失败:', error)
  }
}
</script>

<template>
  <div>
    <input v-model="urn" placeholder="输入 URN" />
    <button @click="generateViewerUrl">生成预览链接</button>
    <div v-if="viewerUrl">
      <a :href="viewerUrl" target="_blank">打开 Viewer</a>
    </div>
  </div>
</template>
```

---

## 技术说明

### URN 编码

API 会自动将输入的 URN 进行 base64 编码，无需手动编码。

**输入**: `urn:adsk.wipprod:fs.file:vf.BpecaZkCRhSpeKT3CXYIiA?version=1`

**编码后**: `dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLkJwZWNhWmtDUmhTcGVrVDNDWFlJaUE/dmVyc2lvbj0x`

### Token 管理

- **使用系统 token** (`use_current_token=true`): API 会从 `utils.py` 的 `get_access_token()` 函数获取当前有效的 access token
- **使用自定义 token** (`use_current_token=false`): 需要在请求中提供 `token` 参数

### 日志记录

API 会记录所有请求和错误信息，便于调试和监控：

```
[2025-11-20 10:00:00] [INFO] forge_viewer_api - 生成 Forge Viewer URL 请求: urn=urn:adsk.wipprod:fs.file:vf.xxx..., use_current_token=True
[2025-11-20 10:00:00] [INFO] forge_viewer_api - 使用系统 token: eyJhbGciOiJSUzI1NiI...
[2025-11-20 10:00:00] [INFO] forge_viewer_api - URN base64 编码成功: dXJuOmFkc2sud2lwcH...
```

---

## 配置说明

### Forge Viewer 基础 URL

在 `forge_viewer_api.py` 中可以配置 Viewer 的基础 URL：

```python
FORGE_VIEWER_BASE_URL = "https://example.jarvisbim.com.cn/help/online-forge-viewer"
```

### Token 获取

Token 管理依赖于 `utils.py` 中的 `get_access_token()` 函数，该函数提供：

- 自动刷新过期 token
- 持久化存储
- 多层存储策略（内存 + 会话 + 文件）

---

## 测试

运行测试脚本：

```bash
python api_modules/file_CDE_function/test_forge_viewer_api.py
```

测试脚本会执行：
1. ✅ 健康检查测试
2. ✅ GET 请求生成单个 URL
3. ✅ POST 请求生成单个 URL
4. ✅ 批量生成 URLs

---

## 集成到主应用

API 已集成到主 Flask 应用 ([app2.py](c:\Projects\ACC-SYNC_DEMO1\ACC-SYNC_DEMO\ACC-SYNC\ACC-SYNC\app2.py:1))：

```python
from api_modules.file_CDE_function import forge_viewer_bp

app.register_blueprint(forge_viewer_bp)
```

启动应用后，API 端点会自动可用。

---

## 故障排除

### 问题 1: "Failed to get access token"

**原因**: 系统没有有效的 access token

**解决方法**:
- 确保已通过 OAuth 认证
- 检查 token 是否已过期
- 尝试使用自定义 token 参数

### 问题 2: "Failed to encode URN"

**原因**: URN 格式错误或包含无法编码的字符

**解决方法**:
- 检查 URN 格式是否正确
- 确保 URN 是有效的字符串

### 问题 3: CORS 错误

**原因**: 跨域请求被阻止

**解决方法**:
- 确保 Flask 应用已配置 CORS
- 检查 `app2.py` 中的 CORS 设置

---

## 更新日志

### v1.0.0 (2025-11-20)

- ✅ 初始版本发布
- ✅ 支持单个 URL 生成 (GET/POST)
- ✅ 支持批量 URL 生成
- ✅ 自动 base64 编码
- ✅ 集成系统 token 管理
- ✅ 完整的错误处理和日志

---

## 联系方式

如有问题或建议，请联系开发团队。
