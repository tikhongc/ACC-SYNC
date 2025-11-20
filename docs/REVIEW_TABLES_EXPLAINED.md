# Review 相关表的概念说明

## 核心概念区别

### 1. `review_step_candidates` - 步骤候选人配置表（静态配置）

**用途**：存储每个审批步骤的候选审批人配置

**数据来源**：从 workflow 定义创建

**特点**：
- ✅ **静态配置**：定义了"谁可以审批这个步骤"
- ✅ **来自 workflow**：在创建 review 时从 workflow.steps 复制
- ✅ **可修改**：虽然来自 workflow，但可以针对特定 review 进行调整
- ✅ **权限控制**：API 使用这个表来验证用户是否有权限审批

**数据结构**：
```json
{
  "review_id": 10,
  "step_id": "step_1",
  "step_name": "Initial Review",
  "step_type": "REVIEWER",
  "step_order": 1,
  "candidates": {
    "users": [
      {
        "autodeskId": "user123",
        "name": "John Doe",
        "email": "john@example.com"
      }
    ],
    "roles": ["project_manager", "lead_engineer"],
    "companies": ["company_abc"]
  },
  "source": "workflow_template",
  "is_active": true
}
```

**创建时机**：
- 创建 review 时立即创建
- 每个 workflow 步骤对应一条记录
- 数量 = workflow.steps 的数量

---

### 2. `review_progress` - 审批进度记录表（动态历史）

**用途**：记录审批步骤的实际执行历史和状态

**数据来源**：初始时从 workflow 创建，执行时不断更新

**特点**：
- ✅ **动态记录**：记录"这个步骤的执行状态是什么"
- ✅ **执行历史**：包含谁审批了、何时审批、审批结果等
- ✅ **状态跟踪**：PENDING → IN_PROGRESS → COMPLETED/REJECTED
- ✅ **时间记录**：started_at, completed_at, due_date 等

**数据结构**：
```json
{
  "review_id": 10,
  "step_id": "step_1",
  "step_name": "Initial Review",
  "step_type": "REVIEWER",
  "step_order": 1,
  "status": "COMPLETED",
  "decision": "APPROVED",
  "comments": "Looks good, approved",
  "completed_by": {
    "autodeskId": "user123",
    "name": "John Doe"
  },
  "started_at": "2025-11-11T10:00:00Z",
  "completed_at": "2025-11-11T14:30:00Z",
  "due_date": "2025-11-12T18:00:00Z"
}
```

**生命周期**：
1. **初始化**：创建 review 时，所有步骤都创建为 PENDING
2. **开始**：第一个步骤设置 started_at
3. **执行中**：用户审批时更新状态、决策、评论等
4. **完成**：设置 completed_at、completed_by、decision

---

## 数据流程图

```
┌─────────────────┐
│  Workflow       │
│  定义步骤和     │
│  默认候选人     │
└────────┬────────┘
         │
         │ 创建 Review 时
         ├─────────────────────────────────┐
         │                                 │
         ▼                                 ▼
┌─────────────────────┐         ┌──────────────────────┐
│ review_step_        │         │ review_progress      │
│ candidates          │         │                      │
│ (静态配置)          │         │ (动态记录)           │
├─────────────────────┤         ├──────────────────────┤
│ • 谁可以审批        │         │ • 当前状态           │
│ • 候选人列表        │         │ • 执行历史           │
│ • 权限配置          │         │ • 审批结果           │
│                     │         │ • 时间记录           │
└─────────────────────┘         └──────────────────────┘
         │                                 │
         │                                 │
         │ 权限检查                        │ 状态更新
         ▼                                 ▼
┌─────────────────────────────────────────────────────┐
│              用户审批操作                           │
│  1. 检查 step_candidates 确认权限                  │
│  2. 更新 review_progress 记录执行结果              │
└─────────────────────────────────────────────────────┘
```

---

## 关键区别对比

| 特性 | review_step_candidates | review_progress |
|------|------------------------|-----------------|
| **性质** | 静态配置 | 动态记录 |
| **用途** | 定义权限 | 记录历史 |
| **数据来源** | workflow 定义 | 实际执行 |
| **更新频率** | 很少（除非修改权限） | 频繁（每次审批） |
| **记录数量** | = workflow 步骤数 | = workflow 步骤数（初始） |
| **关键字段** | candidates | status, decision, completed_by |
| **API 使用** | 权限验证 | 状态查询和更新 |

---

## 常见误区

### ❌ 错误理解 1：review_progress 从 workflow 创建

**错误**：认为 review_progress 应该从 workflow 定义创建

**正确**：
- `review_step_candidates` 从 workflow 创建（配置）
- `review_progress` 只是初始化为 PENDING 状态，然后记录实际执行

### ❌ 错误理解 2：两个表存储相同信息

**错误**：认为两个表是重复的

**正确**：
- `review_step_candidates`：配置层（谁可以做）
- `review_progress`：执行层（谁做了什么）

### ❌ 错误理解 3：progress 记录会超过 workflow 步骤数

**错误**：担心 progress 记录会无限增长

**正确**：
- 初始时 progress 记录数 = workflow 步骤数
- 每个步骤只有一条记录，不会重复创建
- 如果发现超过，说明数据同步有问题

---

## API 使用示例

### 1. 创建 Review（正确流程）

```python
# 步骤 1: 创建 review 记录
review_id = create_review(project_id, workflow_id, name, ...)

# 步骤 2: 从 workflow 初始化 step_candidates（配置）
initialize_review_step_candidates_from_workflow(review_id, workflow_id)

# 步骤 3: 初始化 progress 记录（初始状态）
initialize_review_progress_from_workflow(review_id, workflow_id)
```

### 2. 检查审批权限

```python
# 从 step_candidates 获取候选人配置
candidates = get_step_candidates(review_id, step_id)

# 检查用户是否在候选人列表中
has_permission = check_user_in_candidates(user_id, candidates)
```

### 3. 提交审批决策

```python
# 先检查权限（使用 step_candidates）
if not has_permission_to_approve(user_id, review_id, step_id):
    return "Permission denied"

# 更新进度记录（更新 progress）
update_review_progress(
    review_id=review_id,
    step_id=step_id,
    status='COMPLETED',
    decision='APPROVED',
    completed_by=user_info,
    completed_at=now
)
```

---

## 数据库约束注意事项

### review_step_candidates

**source 字段约束**：
```sql
CHECK (source IN (
    'workflow_template',  -- 从 workflow 模板创建
    'manual',             -- 手动创建
    'custom',             -- 自定义
    'test_setup',         -- 测试设置
    'acc_sync',           -- ACC 同步
    'api_sync'            -- API 同步
))
```

⚠️ **注意**：使用 `'workflow_template'` 而不是 `'workflow_definition'`

### review_progress

**status 字段约束**：
```sql
CHECK (status IN (
    'PENDING',      -- 待处理
    'CLAIMED',      -- 已认领
    'UNCLAIMED',    -- 未认领
    'IN_PROGRESS',  -- 进行中
    'SUBMITTED',    -- 已提交
    'APPROVED',     -- 已批准
    'REJECTED',     -- 已拒绝
    'SKIPPED',      -- 已跳过
    'VOID'          -- 作废
))
```

⚠️ **注意**：没有 `'NOT_STARTED'` 状态，使用 `'PENDING'` 代替

---

## 最佳实践

### 1. 创建 Review 时

```python
# ✅ 正确：先创建 step_candidates，再创建 progress
create_review_step_candidates(review_id, workflow_id)  # 配置权限
create_review_progress(review_id, workflow_id)         # 初始化状态

# ❌ 错误：只创建 progress，忘记 step_candidates
create_review_progress(review_id, workflow_id)
```

### 2. 审批时

```python
# ✅ 正确：先检查 step_candidates，再更新 progress
if check_permission_in_step_candidates(user_id, review_id, step_id):
    update_review_progress(review_id, step_id, decision)

# ❌ 错误：直接更新 progress，不检查权限
update_review_progress(review_id, step_id, decision)
```

### 3. 查询待审批

```python
# ✅ 正确：JOIN 两个表
SELECT r.*, rp.status, rsc.candidates
FROM reviews r
JOIN review_progress rp ON r.id = rp.review_id
JOIN review_step_candidates rsc ON r.id = rsc.review_id 
    AND r.current_step_id = rsc.step_id
WHERE rp.status = 'PENDING'
  AND user_in_candidates(user_id, rsc.candidates)

# ❌ 错误：只查 progress，不验证权限
SELECT * FROM review_progress WHERE status = 'PENDING'
```

---

## 总结

- **`review_step_candidates`** = 配置表 = "谁可以审批"
- **`review_progress`** = 历史表 = "谁审批了，结果如何"

两个表配合使用：
1. 创建时：从 workflow 同时初始化两个表
2. 审批时：用 candidates 检查权限，用 progress 记录结果
3. 查询时：JOIN 两个表获取完整信息

记住：**Candidates 是配置，Progress 是历史！**

