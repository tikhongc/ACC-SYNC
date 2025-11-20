# 快速启动指南

## 问题诊断

测试失败的原因：
1. **404 错误** - 服务器需要重启以加载新的 Blueprint
2. **模块导入错误** - 已修复

## 解决步骤

### 1. 重启服务器

```bash
# 停止当前运行的服务器（按 Ctrl+C）

# 重新启动服务器
python start_dev.py
```

### 2. 验证 Blueprint 注册

启动服务器后，查看控制台输出，应该看到类似：

```
✅ Blueprint registered: folder_file_data
   - /api/folder-file-data/folders/<folder_id>/permissions
   - /api/folder-file-data/folders/<folder_id>/custom-attribute-definitions
   - /api/folder-file-data/files/<file_id>/custom-attributes
   - /api/folder-file-data/files/<file_id>/versions
   - /api/folder-file-data/health
```

### 3. 测试健康检查

```bash
curl http://localhost:8080/api/folder-file-data/health
```

预期响应：
```json
{
  "status": "healthy",
  "service": "folder_file_data_api",
  "database": "connected",
  "timestamp": "..."
}
```

### 4. 运行完整测试

```bash
cd api_modules/file_CDE_function
python test_folder_file_data_api.py
```

## 测试数据准备

确保数据库中有以下数据：

1. **文件夹权限数据** - 运行权限同步：
   ```bash
   python api_modules/permissions_db_sync.py
   ```

2. **自定义属性** - 确保 `custom_attribute_definitions` 表有数据

3. **文件和版本** - 确保 `files` 和 `file_versions` 表有数据

## 快速验证

### 使用 cURL

```bash
# 健康检查
curl "http://localhost:8080/api/folder-file-data/health"

# 获取文件夹权限
curl "http://localhost:8080/api/folder-file-data/folders/urn:adsk.wipprod:fs.folder:co.7ajfDFd6TuWQCKLqpyf9NA/permissions?project_id=b.1eea4119-3553-4167-b93d-3a3d5d07d33d"

# 获取自定义属性定义
curl "http://localhost:8080/api/folder-file-data/folders/urn:adsk.wipprod:fs.folder:co.7ajfDFd6TuWQCKLqpyf9NA/custom-attribute-definitions?project_id=b.1eea4119-3553-4167-b93d-3a3d5d07d33d"
```

### 使用浏览器

访问以下 URL（需要 URL 编码）:

```
http://localhost:8080/api/folder-file-data/health
```

## 常见问题

### Q: 仍然返回 404？
**A:** 检查 `app.py` 中是否正确导入和注册了 Blueprint：

```python
from api_modules.file_CDE_function.folder_file_data_api import folder_file_data_bp
app.register_blueprint(folder_file_data_bp)
```

### Q: 数据库连接错误？
**A:** 检查 `database_sql/neon_config.py` 配置是否正确

### Q: 权限数据为空？
**A:** 运行权限同步脚本：
```bash
python api_modules/permissions_db_sync.py
```

### Q: 文件夹/文件未找到？
**A:** 使用数据库中实际存在的 ID 进行测试

## 下一步

1. ✅ 重启服务器
2. ✅ 验证健康检查
3. ✅ 运行完整测试套件
4. ✅ 根据实际数据调整测试参数
