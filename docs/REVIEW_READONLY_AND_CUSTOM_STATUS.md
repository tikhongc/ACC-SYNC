# Review 只读状态和自定义审批状态功能

## 📋 功能概述

本次优化实现了两个核心功能：

1. **Review 只读状态保护**：CLOSED、CANCELLED、ARCHIVED 状态的 review 无法修改
2. **自定义审批状态支持**：支持从 workflow 配置中读取自定义审批状态选项

## 🎯 核心概念

### 1. Review 状态管理

#### 可修改状态
- `DRAFT`：草稿状态
- `IN_PROGRESS`：进行中
- `PENDING`：待处理

#### 只读状态（不可修改）
- `CLOSED`：已关闭
- `CANCELLED`：已取消
- `ARCHIVED`：已归档

### 2. 审批状态（Approval Status）

#### 核心值（Core Values）
所有审批决策最终只有两个核心值：
- `APPROVED`：已批准
- `REJECTED`：已拒绝

#### 自定义标签（Custom Labels）
Workflow 可以配置多个审批状态选项，但它们的 `value` 都映射到核心值：

```json
[
  {
    "id": "f44e623d-f04f-47fe-8195-efc43d1d985b",
    "label": "已批准",
    "value": "APPROVED",
    "builtIn": true
  },
  {
    "id": "b2a3c3b7-4fef-40a4-868b-981b23e7182f",
    "label": "已拒绝",
    "value": "REJECTED",
    "builtIn": true
  },
  {
    "id": "80b2cd26-cfab-42b4-ae75-aa1bd286326f",
    "label": "已批准且带注释",
    "value": "APPROVED",
    "builtIn": false
  }
]
```

## 🔧 实现细节

### 新增辅助方法

#### 1. `_check_review_is_modifiable(review_id, cursor)`

检查 review 是否可以修改。

**参数：**
- `review_id`: Review ID
- `cursor`: 数据库游标

**返回：**
- `(bool, str)`: (是否可修改, 错误消息)

**示例：**
```python
can_modify, error_msg = manager._check_review_is_modifiable(review_id, cursor)
if not can_modify:
    return {
        'success': False,
        'error': error_msg,
        'error_type': 'invalid_state'
    }
```

#### 2. `_get_workflow_approval_status_options(workflow_id, cursor)`

获取 workflow 配置的自定义审批状态选项。

**参数：**
- `workflow_id`: Workflow ID
- `cursor`: 数据库游标

**返回：**
- `List[Dict]`: 审批状态选项列表

**示例：**
```python
custom_options = manager._get_workflow_approval_status_options(workflow_id, cursor)
# [
#   {"id": "...", "label": "已批准", "value": "APPROVED", "builtIn": true},
#   ...
# ]
```

#### 3. `_validate_approval_decision(decision, workflow_id, cursor)`

验证审批决策是否有效（只验证核心值）。

**参数：**
- `decision`: 决策值（APPROVED 或 REJECTED）
- `workflow_id`: Workflow ID
- `cursor`: 数据库游标

**返回：**
- `(bool, str, List[str])`: (是否有效, 错误消息, 有效决策列表)

**示例：**
```python
is_valid, error_msg, valid_options = manager._validate_approval_decision(
    'APPROVED', workflow_id, cursor
)
if not is_valid:
    return {'success': False, 'error': error_msg}
```

### 修改的 API 端点

所有修改操作的 API 都添加了状态检查和决策验证：

#### 1. `POST /api/approval/reviews/<int:review_id>/steps/<step_id>/start`

启动审批步骤（claim step）

**新增检查：**
- ✅ Review 状态检查（只读保护）

#### 2. `POST /api/approval/reviews/<int:review_id>/steps/<step_id>/submit`

提交审批决策

**新增检查：**
- ✅ Review 状态检查（只读保护）
- ✅ 决策值验证（APPROVED/REJECTED）
- ✅ 文件级决策验证

#### 3. `POST /api/approval/reviews/<int:review_id>/files/batch-approve`

批量审批文件

**新增检查：**
- ✅ Review 状态检查（只读保护）
- ✅ 每个文件的决策值验证

## 🎨 前后端职责分离

### 前端职责

1. **读取配置**：从 `workflow.approval_status_options` 读取审批状态配置
2. **显示选项**：向用户展示 `label`（如"已批准"、"已批准且带注释"）
3. **提交值**：提交时使用对应的 `value`（APPROVED 或 REJECTED）

**示例代码：**
```javascript
// 1. 获取 workflow 配置
const workflow = await fetchWorkflow(workflowId);
const statusOptions = workflow.approval_status_options;

// 2. 显示给用户
statusOptions.forEach(option => {
  // 显示 option.label 给用户选择
  // 例如: "已批准"、"已拒绝"、"已批准且带注释"
});

// 3. 用户选择后，提交对应的 value
const selectedOption = statusOptions.find(opt => opt.label === userSelection);
await submitDecision({
  decision: selectedOption.value  // "APPROVED" 或 "REJECTED"
});
```

### 后端职责

1. **验证核心值**：只验证 `decision` 是否为 `APPROVED` 或 `REJECTED`
2. **不做映射**：不需要进行 label 到 value 的映射
3. **提供配置**：通过 API 返回 `approval_status_options` 供前端使用

## 📊 数据库结构

### workflows 表

```sql
CREATE TABLE workflows (
    id SERIAL PRIMARY KEY,
    workflow_uuid UUID,
    name VARCHAR(255),
    approval_status_options JSONB,  -- 自定义审批状态选项
    ...
);
```

### reviews 表

```sql
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    review_uuid UUID,
    workflow_id INTEGER REFERENCES workflows(id),
    status VARCHAR(50),  -- DRAFT, IN_PROGRESS, PENDING, CLOSED, CANCELLED, ARCHIVED
    ...
);
```

## 🧪 测试覆盖

测试脚本：`test_readonly_and_custom_status.py`

### 测试场景

1. **CLOSED review 只读测试**
   - ✅ 将 review 状态改为 CLOSED
   - ✅ 验证无法修改
   - ✅ 恢复状态

2. **自定义状态验证测试**
   - ✅ 验证 APPROVED 决策
   - ✅ 验证 REJECTED 决策
   - ✅ 验证无效决策被拒绝
   - ✅ 获取自定义状态选项

3. **数据结构验证测试**
   - ✅ 验证所有选项包含必需字段（id, label, value, builtIn）
   - ✅ 验证所有 value 都是 APPROVED 或 REJECTED
   - ✅ 验证前后端职责分离

### 测试结果

```
============================================================
所有测试完成！
============================================================
✓ CLOSED review 只读保护正常工作
✓ 自定义审批状态验证正常工作
✓ approval_status_options 数据结构完整
✓ 前后端职责分离清晰
```

## 📝 API 使用示例

### 1. 获取 Workflow 的审批状态选项

```bash
GET /api/workflows/{workflow_id}
```

**响应：**
```json
{
  "id": 1,
  "name": "Standard Review Workflow",
  "approval_status_options": [
    {
      "id": "f44e623d-f04f-47fe-8195-efc43d1d985b",
      "label": "已批准",
      "value": "APPROVED",
      "builtIn": true
    },
    {
      "id": "b2a3c3b7-4fef-40a4-868b-981b23e7182f",
      "label": "已拒绝",
      "value": "REJECTED",
      "builtIn": true
    },
    {
      "id": "80b2cd26-cfab-42b4-ae75-aa1bd286326f",
      "label": "已批准且带注释",
      "value": "APPROVED",
      "builtIn": false
    }
  ]
}
```

### 2. 提交审批决策

```bash
POST /api/approval/reviews/{review_id}/steps/{step_id}/submit
```

**请求体：**
```json
{
  "user_id": "test_user",
  "decision": "APPROVED",  // 使用 value，不是 label
  "comments": "审批通过",
  "file_decisions": [
    {
      "file_id": 123,
      "decision": "APPROVED",  // 使用 value
      "comments": "文件无问题"
    }
  ]
}
```

### 3. 尝试修改 CLOSED review（会失败）

```bash
POST /api/approval/reviews/{review_id}/steps/{step_id}/start
```

**响应（失败）：**
```json
{
  "success": false,
  "error": "Review is CLOSED and cannot be modified. Only DRAFT, IN_PROGRESS, or PENDING reviews can be modified.",
  "error_type": "invalid_state"
}
```

## ⚠️ 注意事项

### 1. 状态检查顺序

所有修改操作都应该：
1. 首先检查 review 是否可修改
2. 然后进行权限验证
3. 最后执行业务逻辑

### 2. 决策值格式

- ✅ 正确：使用 `APPROVED` 或 `REJECTED`（大写）
- ❌ 错误：使用 label（如"已批准"）
- ❌ 错误：使用小写（如"approved"）

### 3. 错误处理

当 review 不可修改时，返回：
```json
{
  "success": false,
  "error": "Review is {status} and cannot be modified...",
  "error_type": "invalid_state"
}
```

HTTP 状态码：`400 Bad Request`

## 🔄 与现有功能的兼容性

### 兼容性说明

1. **向后兼容**：现有的 API 调用不受影响
2. **渐进式增强**：如果 workflow 没有配置 `approval_status_options`，使用默认值
3. **数据迁移**：不需要迁移现有数据

### 默认行为

如果 workflow 没有配置 `approval_status_options`：
- 系统默认只接受 `APPROVED` 和 `REJECTED`
- 不影响现有功能

## 📚 相关文件

### 核心文件
- `api_modules/review_CDE_function/approval_workflow_api_enhanced.py` - 主要实现
- `test_readonly_and_custom_status.py` - 测试脚本

### 数据库表
- `workflows` - 存储 approval_status_options
- `reviews` - 存储 review 状态
- `review_progress` - 存储审批进度
- `review_file_versions` - 存储文件审批状态

## 🎉 总结

### 实现的功能

✅ Review 只读状态保护（CLOSED/CANCELLED/ARCHIVED 不可修改）  
✅ 自定义审批状态支持（从 workflow 配置读取）  
✅ 简化的验证逻辑（只验证核心值 APPROVED/REJECTED）  
✅ 清晰的前后端职责分离  
✅ 完整的测试覆盖  

### 设计优势

1. **简单高效**：后端只验证核心值，不做复杂映射
2. **灵活可扩展**：支持自定义审批状态标签
3. **职责清晰**：前端负责显示和映射，后端负责验证
4. **安全可靠**：只读状态保护防止误操作

### 下一步建议

1. 添加审批历史查询 API
2. 支持审批条件配置
3. 添加审批通知功能
4. 实现审批统计报表

