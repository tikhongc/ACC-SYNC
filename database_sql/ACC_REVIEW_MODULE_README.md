# ACC Review 模块后端实现

## 概述

本项目实现了完整的ACC Review模块后端功能，支持从ACC API获取review数据并在本地CDE平台进行增删改查操作。

## 实现特性

### ✅ 已完成功能

1. **数据库结构扩展**
   - ✅ 创建 `user_members` 表缓存项目用户
   - ✅ 创建 `review_candidates` 表管理候选人分配
   - ✅ 扩展 `workflow_templates` 表支持ACC模板映射
   - ✅ 创建 `workflow_notes` 表管理工作流备注

2. **用户管理系统**
   - ✅ 从ACC API同步项目用户到本地数据库
   - ✅ 支持用户状态管理和过滤查询
   - ✅ 提供用户统计和公司分布信息

3. **候选人分配系统**
   - ✅ 支持用户/角色/公司三种候选人类型
   - ✅ 灵活的候选人分配到workflow步骤
   - ✅ 候选人管理和更新功能

4. **工作流模板系统**
   - ✅ 从ACC同步工作流模板
   - ✅ 支持1-5步骤的标准模板类型
   - ✅ 本地模板创建和管理
   - ✅ 模板配置和候选人映射

5. **评审CRUD操作**
   - ✅ 完整的评审创建、读取、更新、删除
   - ✅ 评审状态管理和文件关联
   - ✅ 分页查询和过滤功能

6. **步骤进度管理**
   - ✅ 步骤认领和提交功能
   - ✅ 状态转换和流程控制
   - ✅ 发送回发起人功能
   - ✅ 用户待处理任务查询

7. **多层级评论系统**
   - ✅ 步骤级别评论管理
   - ✅ 工作流级别备注管理
   - ✅ 评论的增删改查功能
   - ✅ 内部备注和可见性控制

8. **文件审批状态管理**
   - ✅ 文件审批状态更新
   - ✅ 批量审批功能
   - ✅ 审批历史记录
   - ✅ 文件状态统计和时间线

## 技术架构

### 数据库设计

#### 新增表结构

1. **user_members** - 项目用户缓存表
   ```sql
   - user_acc_id: ACC用户ID
   - autodesk_id: Autodesk ID
   - name, email: 基本信息
   - company_id, company_name: 公司信息
   - access_levels, roles: 权限和角色
   - status: 用户状态 (active/pending/deleted)
   ```

2. **review_candidates** - 评审候选人表
   ```sql
   - review_id: 关联评审
   - step_id: 步骤ID
   - candidate_type: 候选人类型 (user/role/company)
   - candidate_acc_id: 候选人ACC ID
   - user_member_id: 关联用户成员
   - is_key_reviewer: 是否关键审核者
   ```

3. **workflow_notes** - 工作流备注表
   ```sql
   - workflow_id, review_id: 关联对象
   - note_type: 备注类型
   - content: 备注内容
   - is_visible_to_reviewers: 可见性控制
   - priority: 优先级
   ```

4. **workflow_templates** (扩展)
   ```sql
   - acc_template_id: ACC模板映射
   - template_type: 模板类型 (one_step到five_step)
   - steps_config: 详细步骤配置
   - approval_status_options: 审批状态选项
   ```

### API模块结构

```
api_modules/
├── candidate_assignment_api.py   # 候选人分配API
├── review_crud_api.py            # 评审CRUD API
├── step_progress_api.py          # 步骤进度API
├── comment_system_api.py         # 评论系统API
├── approval_status_api.py        # 审批状态API
└── review_module_integration.py  # 模块集成
```

## API端点

### 用户同步 API

- `POST /api/user-sync/projects/{project_id}/sync` - 同步项目用户
- `GET /api/user-sync/projects/{project_id}/users` - 获取缓存用户列表
- `GET /api/user-sync/projects/{project_id}/users/{user_acc_id}` - 获取用户详情
- `GET /api/user-sync/projects/{project_id}/stats` - 获取用户统计

### 候选人分配 API

- `POST /api/candidates/reviews/{review_id}/assign` - 分配候选人
- `GET /api/candidates/reviews/{review_id}` - 获取评审候选人
- `PUT /api/candidates/{candidate_id}` - 更新候选人
- `DELETE /api/candidates/{candidate_id}` - 移除候选人

### 候选人管理 API

- `GET /api/candidates/projects/{project_id}/available` - 获取可用候选人
- `GET /api/candidates/workflows/{workflow_id}` - 获取工作流候选人配置
- `GET /api/candidates/reviews/{review_id}/missing` - 检查缺失候选人的步骤
- `POST /api/candidates/reviews/{review_id}/fix` - 修复缺失的候选人信息

### 模板同步 API

- `POST /api/template-sync/projects/{project_id}/sync` - 同步工作流模板
- `POST /api/template-sync/templates` - 创建本地模板
- `GET /api/template-sync/templates` - 获取模板列表
- `GET /api/template-sync/templates/{template_uuid}` - 获取模板详情

### 评审 CRUD API

- `POST /api/reviews` - 创建评审
- `GET /api/reviews/{review_id}` - 获取评审详情
- `PUT /api/reviews/{review_id}` - 更新评审
- `DELETE /api/reviews/{review_id}` - 删除评审
- `GET /api/reviews` - 获取评审列表
- `POST /api/reviews/{review_id}/start` - 启动评审

### 步骤进度 API

- `POST /api/step-progress/reviews/{review_id}/steps/{step_id}/claim` - 认领步骤
- `POST /api/step-progress/reviews/{review_id}/steps/{step_id}/submit` - 提交步骤
- `POST /api/step-progress/reviews/{review_id}/steps/{step_id}/send-back` - 发送回发起人
- `GET /api/step-progress/reviews/{review_id}/progress` - 获取步骤进度
- `GET /api/step-progress/users/{user_acc_id}/tasks` - 获取用户任务

### 评论系统 API

- `POST /api/comments/reviews/{review_id}/steps/{step_id}/comments` - 添加步骤评论
- `POST /api/comments/workflow-notes` - 添加工作流备注
- `GET /api/comments/reviews/{review_id}/steps/comments` - 获取步骤评论
- `GET /api/comments/workflow-notes` - 获取工作流备注
- `PUT /api/comments/reviews/{review_id}/steps/{step_id}/comments/{comment_id}` - 更新评论
- `DELETE /api/comments/reviews/{review_id}/steps/{step_id}/comments/{comment_id}` - 删除评论

### 审批状态 API

- `POST /api/approval-status/file-versions/{file_version_id}/approve` - 更新文件审批
- `POST /api/approval-status/reviews/{review_id}/batch-approve` - 批量审批
- `GET /api/approval-status/history` - 获取审批历史
- `GET /api/approval-status/reviews/{review_id}/file-statuses` - 获取文件状态统计
- `GET /api/approval-status/files/{file_urn}/timeline` - 获取文件时间线

## 使用方法

### 1. 数据库初始化

```sql
-- 执行数据库schema更新
psql -d your_database -f database_sql/review_system_schema.sql
```

### 2. 注册API蓝图

```python
from api_modules.review_module_integration import register_review_module_blueprints

# 在Flask应用中注册
app = Flask(__name__)
register_review_module_blueprints(app)
```

### 3. 基本工作流程

#### 步骤1: 同步项目用户
```bash
POST /api/user-sync/projects/{project_id}/sync
```

#### 步骤2: 同步工作流模板
```bash
POST /api/template-sync/projects/{project_id}/sync
```

#### 步骤3: 创建评审
```json
POST /api/reviews
{
  "name": "文件评审",
  "project_id": "project123",
  "workflow_id": 1,
  "file_versions": [
    {
      "file_urn": "urn:adsk.objects:os.object:bucket/file.dwg",
      "file_name": "design.dwg",
      "version_number": 1
    }
  ]
}
```

#### 步骤4: 分配候选人
```json
POST /api/candidates/reviews/{review_id}/assign
{
  "step_assignments": [
    {
      "step_id": "step_1",
      "step_name": "Initial Review",
      "candidates": [
        {
          "type": "user",
          "acc_id": "user123",
          "name": "John Doe",
          "is_key_reviewer": true
        }
      ]
    }
  ]
}
```

#### 步骤5: 启动评审
```bash
POST /api/reviews/{review_id}/start
```

## 配置要求

### 环境变量
- `DATABASE_URL`: PostgreSQL数据库连接字符串
- `ACC_CLIENT_ID`: ACC应用客户端ID
- `ACC_CLIENT_SECRET`: ACC应用客户端密钥

### 依赖包
- Flask
- psycopg2-binary
- requests
- python-dateutil

## 性能优化

1. **数据库索引**: 为所有新表添加了适当的索引
2. **批量操作**: 支持批量用户同步和文件审批
3. **分页查询**: 评审列表支持分页和过滤
4. **JSON字段**: 使用JSONB存储复杂数据结构
5. **连接池**: 建议使用数据库连接池

## 错误处理

所有API端点都包含完整的错误处理：
- 参数验证
- 数据库事务回滚
- 详细的错误消息
- HTTP状态码

## 扩展性

系统设计支持：
- 新的候选人类型
- 自定义工作流步骤
- 额外的审批状态
- 更多的评论类型
- 自定义字段扩展

## 监控和日志

- 所有操作都有详细的控制台日志
- 支持性能监控和统计
- 错误跟踪和调试信息

## 安全考虑

- 用户身份验证集成
- 权限控制和访问验证
- 数据输入验证和清理
- SQL注入防护

## 测试建议

1. **单元测试**: 每个管理器类的方法
2. **集成测试**: API端点的完整流程
3. **性能测试**: 大量数据的处理能力
4. **安全测试**: 权限和数据验证

## 维护和更新

- 定期同步ACC API的变更
- 数据库schema版本管理
- API版本兼容性
- 性能监控和优化

---

## 联系信息

如有问题或需要支持，请联系开发团队。

**实现状态**: ✅ 完成
**版本**: 1.0.0
**最后更新**: 2025-11-10
