# ACC-SYNC 动态项目选择功能实现总结

## 功能概述

实现了动态项目选择功能，用户现在可以在使用 Reviews API 和 Forms API 之前选择具体的项目，而不是固定使用默认项目。

## 实现的功能

### 1. 通用项目选择组件 (ProjectSelector.vue)

- **位置**: `frontend/src/components/ProjectSelector.vue`
- **功能**: 
  - 显示所有可用项目列表
  - 支持单选和多选模式
  - 显示项目名称、ID、状态和权限范围
  - 提供搜索和筛选功能
  - 支持手动刷新项目列表
  - 显示项目缓存时间和统计信息

### 2. 项目数据存储管理 (projectStore.js)

- **位置**: `frontend/src/utils/projectStore.js`
- **功能**:
  - 管理项目数据的localStorage缓存
  - 24小时缓存过期机制
  - 保存和获取当前选中的项目
  - 提供项目数据的CRUD操作
  - 智能缓存刷新策略

### 3. 登录后项目信息预加载

- **修改文件**: `frontend/src/views/AuthSuccess.vue`
- **功能**:
  - 认证成功后自动获取并缓存项目信息
  - 显示预加载进度和结果
  - 为后续API调用做准备

### 4. 首页入口逻辑更新

- **修改文件**: `frontend/src/views/Home.vue`
- **功能**:
  - Forms API和Reviews API按钮点击后先弹出项目选择对话框
  - 选择项目后保存到localStorage并跳转到相应页面
  - 携带项目信息作为URL参数传递

### 5. Forms API页面项目支持

- **修改文件**: `frontend/src/views/FormsData.vue`
- **功能**:
  - 支持从URL参数或localStorage获取项目信息
  - 未选择项目时自动弹出项目选择对话框
  - API调用时动态传递项目ID参数

### 6. Reviews API页面项目支持

- **修改文件**: `frontend/src/views/Reviews.vue`
- **功能**:
  - 支持从URL参数或localStorage获取项目信息
  - 未选择项目时自动弹出项目选择对话框
  - API调用时动态传递项目ID参数

### 7. 后端API动态项目ID支持

- **修改文件**: 
  - `api_modules/forms_api.py`
  - `api_modules/reviews_api.py`
- **功能**:
  - Forms API支持通过`projectId`参数动态指定项目
  - Reviews API支持通过`projectId`参数动态指定项目
  - 所有导出API支持动态项目ID
  - 保持向后兼容，未提供参数时使用默认项目ID

### 8. 数据导出项目选择功能

- **修改文件**: `frontend/src/views/Home.vue`
- **功能**:
  - 所有导出按钮点击后弹出项目选择对话框
  - 支持JSON和Blob两种响应类型的下载
  - 下载文件名包含项目信息和时间戳
  - 智能处理不同API的响应格式

## 用户流程

### 新的操作流程

1. **用户登录** → 系统自动预加载项目信息到localStorage
2. **点击API入口** (Forms/Reviews) → 弹出项目选择对话框
3. **选择项目** → 保存选择并跳转到对应页面
4. **页面加载** → 使用选中的项目ID调用API获取数据

### 数据导出流程

1. **点击导出按钮** → 弹出项目选择对话框
2. **选择项目** → 使用选中项目ID调用导出API
3. **文件下载** → 自动下载包含项目信息的JSON文件

### 项目信息缓存策略

- **缓存时长**: 24小时
- **选中项目**: 2小时过期
- **自动刷新**: 缓存过期时自动从API获取最新数据
- **手动刷新**: 项目选择对话框中的刷新按钮

## 技术特性

### 前端技术

- **Vue 3 Composition API**: Reviews页面使用现代Vue语法
- **Vue 2 Options API**: Forms页面和组件保持现有架构
- **Element Plus**: UI组件库
- **LocalStorage**: 客户端数据持久化
- **响应式设计**: 支持移动端显示

### 后端技术

- **Flask Blueprint**: 模块化API架构
- **动态参数**: 支持URL参数传递项目ID
- **向后兼容**: 保持现有API调用方式

### 数据管理

- **缓存优先**: 优先使用本地缓存数据
- **智能刷新**: 根据缓存状态决定是否重新获取
- **状态管理**: 统一的项目状态管理

## 文件清单

### 新增文件
- `frontend/src/components/ProjectSelector.vue` - 项目选择组件
- `frontend/src/utils/projectStore.js` - 项目数据存储管理
- `FEATURE_SUMMARY.md` - 功能总结文档

### 修改文件
- `frontend/src/views/Home.vue` - 首页入口逻辑
- `frontend/src/views/FormsData.vue` - Forms页面项目支持
- `frontend/src/views/Reviews.vue` - Reviews页面项目支持
- `frontend/src/views/AuthSuccess.vue` - 登录成功页面预加载
- `api_modules/forms_api.py` - Forms API动态项目支持
- `api_modules/reviews_api.py` - Reviews API动态项目支持

## 兼容性说明

- **向后兼容**: 现有API调用方式仍然有效
- **渐进增强**: 用户可以选择使用新功能或保持原有方式
- **数据安全**: 项目选择信息仅存储在客户端，不影响服务器状态

## 未来扩展

1. **批量操作**: 支持多项目批量数据获取
2. **项目权限**: 更细粒度的项目权限控制
3. **数据同步**: 跨项目数据同步和比较功能
4. **项目模板**: 基于项目类型的模板化操作

## 测试建议

1. 测试项目选择对话框的显示和交互
2. 验证项目信息缓存和过期机制
3. 测试不同项目的API数据获取
4. 验证URL参数和localStorage的项目信息传递
5. 测试缓存刷新和错误处理机制
