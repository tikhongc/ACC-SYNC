# ACC 表单同步 PoC

Autodesk Construction Cloud (ACC) 表单数据同步概念验证项目



## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置应用

编辑 `config.py` 文件，设置你的 Autodesk 应用信息：

```python
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
CALLBACK_URL = 'http://localhost:8080/api/auth/callback'
```

### 3. 启动服务

```bash
python app.py
```

### 4. 开始使用

1. 访问 `http://localhost:8080/` 开始 OAuth 认证
2. 认证成功后选择相应的功能进行测试

## 📋 功能模块

### 🔐 认证模块 (auth_api.py)

- OAuth 2.0 三步认证流程
- Token 自动保存和刷新
- 用户账户信息获取

**主要端点：**
- `GET /` - 开始认证
- `GET /api/auth/callback` - OAuth 回调
- `GET /api/auth/refresh` - 刷新 token
- `GET /api/auth/account-info` - 账户信息

### 📋 Forms API 模块 (forms_api.py)

- ACC Forms API 集成
- 表单数据获取和分析
- JSON 数据导出功能

**主要端点：**
- `GET /api/forms/jarvis` - 获取 JARVIS 项目表单
- `GET /api/forms/export-json` - 导出 JSON 数据
- `GET /api/test/forms` - Forms API 测试

### 🔄 Data Connector API 模块 (data_connector_api.py)

- Data Connector API 批量导出
- 多版本端点自动测试
- 任务状态监控

**主要端点：**
- `GET /api/data-connector/sync` - 同步表单数据
- `GET /api/data-connector/monitor` - 监控任务状态

### 🧪 测试模块 (test_api.py)

- 各种 API 端点测试
- 诊断和故障排除
- 替代方案探索

**主要端点：**
- `GET /api/test/export` - 测试数据导出
- `GET /api/test/alternative` - 替代方案测试

### 🛠️ 工具模块 (utils.py)

- Token 管理函数
- HTML 响应生成
- 数据处理辅助函数

## 🎯 PoC 目标

1. **数据导出请求** - 成功向 ACC 提交数据导出任务
2. **任务轮询** - 监控导出任务进度
3. **数据下载** - 获取导出的表单数据
4. **工作流重建** - 基于表单数据重建工作流历史

## 🔧 配置说明

### OAuth 配置

在 `config.py` 中配置以下参数：

```python
CLIENT_ID = 'your_autodesk_app_client_id'
CLIENT_SECRET = 'your_autodesk_app_client_secret'
CALLBACK_URL = 'http://localhost:8080/api/auth/callback'
SCOPES = 'account:read data:read data:write viewables:read'
```

### 项目配置

```python
JARVIS_PROJECT_ID = "b.a5d9ae79-8653-4de1-bf7a-9dcbbe4db13e"  # 目标项目 ID
TOKEN_FILE = 'token.md'  # Token 存储文件
DEBUG = True  # 调试模式
PORT = 8080  # 服务端口
```

## 📊 API 使用流程

### 推荐流程

1. **认证** → `GET /`
2. **Data Connector 同步** → `GET /api/data-connector/sync`
3. **监控任务** → `GET /api/data-connector/monitor`
4. **备选方案** → `GET /api/forms/jarvis`

### 故障排除流程

1. **测试导出** → `GET /api/test/export`
2. **替代方案** → `GET /api/test/alternative`
3. **Forms API 测试** → `GET /api/test/forms`

## 🔍 故障排除

### 常见问题

1. **403 权限错误**
   - 检查 OAuth scopes 配置
   - 确认 Autodesk 应用权限设置
   - 验证 Account ID 格式

2. **404 端点不存在**
   - API 版本可能已更新
   - 检查端点 URL 格式
   - 尝试不同的 API 版本

3. **Token 过期**
   - 使用刷新功能更新 token
   - 重新进行 OAuth 认证

## 📈 性能优化

- 模块化设计便于维护和扩展
- 统一的错误处理和日志记录
- 响应式 HTML 界面设计
- 自动化的 token 管理

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目。

## 📄 许可证

本项目仅用于概念验证和学习目的。
