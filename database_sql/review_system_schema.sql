-- ============================================================================
-- 统一文件审批系统 - 完全可读写设计
-- 所有数据（包括ACC同步的）都可以在本地平台修改
-- Version: 1.0
-- Created: 2025-11-10
-- ============================================================================

-- 启用必要的扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- ============================================================================
-- 注意：基础表（accounts, projects）由 account_schema_optimized.sql 创建
-- 本 schema 只创建 review 相关的表和类型
-- ============================================================================

-- ============================================================================
-- 基础枚举类型
-- ============================================================================

-- 数据源类型 (如果不存在则创建)
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'data_source_type') THEN
        CREATE TYPE data_source_type AS ENUM ('acc_sync', 'local_system');
    END IF;
END $$;

-- 工作流状态 (如果不存在则创建)
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'workflow_status_type') THEN
        CREATE TYPE workflow_status_type AS ENUM ('ACTIVE', 'INACTIVE', 'DRAFT', 'ARCHIVED');
    END IF;
END $$;

-- 评审状态 (如果不存在则创建)
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'review_status_type') THEN
        CREATE TYPE review_status_type AS ENUM ('OPEN', 'CLOSED', 'VOID', 'FAILED', 'DRAFT', 'CANCELLED');
    END IF;
END $$;

-- 审批状态 (如果不存在则创建)
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'approval_status_type') THEN
        CREATE TYPE approval_status_type AS ENUM ('PENDING', 'APPROVED', 'REJECTED', 'IN_REVIEW');
    END IF;
END $$;

-- 步骤类型 (如果不存在则创建)
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'step_type') THEN
        CREATE TYPE step_type AS ENUM ('REVIEWER', 'APPROVER', 'INITIATOR', 'FINAL');
    END IF;
END $$;

-- 用户状态类型 (如果不存在则创建，兼容account schema)
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_status_type') THEN
        CREATE TYPE user_status_type AS ENUM ('active', 'inactive', 'pending', 'not_invited', 'deleted');
    END IF;
END $$;

-- 候选人类型 (如果不存在则创建)
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'candidate_type') THEN
        CREATE TYPE candidate_type AS ENUM ('user', 'role', 'company');
    END IF;
END $$;

-- 审核者类型 (如果不存在则创建)
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'reviewer_type') THEN
        CREATE TYPE reviewer_type AS ENUM ('SINGLE_REVIEWER', 'MULTIPLE_REVIEWERS', 'GROUP_APPROVAL');
    END IF;
END $$;

-- 时间类型 (如果不存在则创建)
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'time_unit_type') THEN
        CREATE TYPE time_unit_type AS ENUM ('CALENDAR_DAYS', 'WORKING_DAYS');
    END IF;
END $$;

-- ============================================================================
-- 1. 统一工作流表
-- ============================================================================
CREATE TABLE workflows (
    id SERIAL PRIMARY KEY,
    workflow_uuid VARCHAR(36) UNIQUE,
    project_id VARCHAR(255) NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    
    -- 数据源标识（仅用于追踪来源）
    data_source data_source_type NOT NULL DEFAULT 'local_system',
    acc_workflow_id VARCHAR(36),  -- ACC原始ID（用于同步映射）
    
    -- 基本信息（全部可编辑）
    name VARCHAR(255) NOT NULL,
    description TEXT,
    notes TEXT,
    status workflow_status_type DEFAULT 'ACTIVE',
    
    -- 工作流配置（全部可编辑）
    additional_options JSONB DEFAULT '{}'::jsonb,
    approval_status_options JSONB DEFAULT '[]'::jsonb,
    copy_files_options JSONB DEFAULT '{}'::jsonb,
    attached_attributes JSONB DEFAULT '[]'::jsonb,
    update_attributes_options JSONB DEFAULT '{}'::jsonb,
    
    -- 步骤配置（全部可编辑）
    steps JSONB DEFAULT '[]'::jsonb,
    
    -- 本地扩展字段
    tags JSONB DEFAULT '[]'::jsonb,
    custom_fields JSONB DEFAULT '{}'::jsonb,
    is_template BOOLEAN DEFAULT FALSE,
    template_category VARCHAR(100),
    
    -- 统计信息（系统自动计算）
    steps_count INTEGER GENERATED ALWAYS AS (jsonb_array_length(steps)) STORED,
    total_reviews INTEGER DEFAULT 0,
    active_reviews INTEGER DEFAULT 0,
    
    -- 创建者信息（存储完整用户对象）
    created_by JSONB DEFAULT '{}'::jsonb,
    
    -- 时间戳（全部可编辑）
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- 同步信息（仅用于系统管理）
    last_synced_at TIMESTAMP WITH TIME ZONE,
    sync_status VARCHAR(20) DEFAULT 'pending',
    
    -- 版本控制
    version INTEGER DEFAULT 1
);

-- ============================================================================
-- 2. 统一评审表
-- ============================================================================
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    review_uuid VARCHAR(36) UNIQUE NOT NULL,
    project_id VARCHAR(255) NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    workflow_id INTEGER REFERENCES workflows(id) ON DELETE SET NULL,
    
    -- 数据源标识
    data_source data_source_type NOT NULL DEFAULT 'local_system',
    acc_review_id VARCHAR(36),
    acc_sequence_id INTEGER,
    
    -- 基本信息（全部可编辑）
    name VARCHAR(255) NOT NULL,
    description TEXT,
    notes TEXT,  -- 评审备注（对应API的notes字段）
    status review_status_type DEFAULT 'DRAFT',
    
    -- 当前状态（全部可编辑）
    current_step_id VARCHAR(50),
    current_step_due_date TIMESTAMP WITH TIME ZONE,
    current_step_name VARCHAR(255),
    workflow_uuid VARCHAR(36),  -- 关联的工作流UUID
    
    -- 参与者信息（全部可编辑）
    created_by JSONB DEFAULT '{}'::jsonb,
    assigned_to JSONB DEFAULT '[]'::jsonb,
    next_action_by JSONB DEFAULT '{}'::jsonb,
    
    -- 归档信息（全部可编辑）
    archived BOOLEAN DEFAULT FALSE,
    archived_by JSONB DEFAULT '{}'::jsonb,
    archived_at TIMESTAMP WITH TIME ZONE,
    archived_reason TEXT,
    
    -- 本地扩展字段
    priority INTEGER DEFAULT 3 CHECK (priority BETWEEN 1 AND 5),
    tags JSONB DEFAULT '[]'::jsonb,
    custom_fields JSONB DEFAULT '{}'::jsonb,
    department VARCHAR(100),
    category VARCHAR(100),
    
    -- 统计信息（系统计算，但可手动调整）
    total_file_versions INTEGER DEFAULT 0,
    approved_versions INTEGER DEFAULT 0,
    rejected_versions INTEGER DEFAULT 0,
    pending_versions INTEGER DEFAULT 0,
    
    -- 进度信息（可编辑）
    current_step_number INTEGER DEFAULT 1,
    total_steps INTEGER DEFAULT 1,
    progress_percentage DECIMAL(5,2) DEFAULT 0,
    
    -- 时间戳（全部可编辑）
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP WITH TIME ZONE,
    finished_at TIMESTAMP WITH TIME ZONE,
    
    -- 同步信息
    last_synced_at TIMESTAMP WITH TIME ZONE,
    sync_status VARCHAR(20) DEFAULT 'pending'
);

-- ============================================================================
-- 3. 评审文件版本关联表
-- 注意：file_versions 表在 optimized_schema_v2.sql 中定义
-- 此表只存储评审相关的审批状态，不重复存储文件信息
-- ============================================================================
CREATE TABLE review_file_versions (
    id SERIAL PRIMARY KEY,
    review_id INTEGER NOT NULL REFERENCES reviews(id) ON DELETE CASCADE,
    
    -- 🔑 关联到 optimized_schema_v2.sql 中的 file_versions 表
    -- 引用 file_versions.urn，确保数据完整性
    file_version_urn TEXT NOT NULL,
    
    -- 审批状态（特定于此 review）
    approval_status approval_status_type DEFAULT 'PENDING',
    approval_status_id VARCHAR(36),
    approval_status_value VARCHAR(20),
    approval_label VARCHAR(100),
    approval_comments TEXT,
    approval_conditions TEXT,
    
    -- 评审内容（特定于此 review）
    review_content JSONB DEFAULT '{}'::jsonb,
    custom_attributes JSONB DEFAULT '[]'::jsonb,
    
    -- 复制信息
    copied_file_version_urn TEXT,
    copy_target_folder TEXT,
    copy_settings JSONB DEFAULT '{}'::jsonb,
    
    -- 本地扩展字段
    local_file_path TEXT,
    thumbnail_url TEXT,
    tags JSONB DEFAULT '[]'::jsonb,
    
    -- 审批历史
    approval_history JSONB DEFAULT '[]'::jsonb,
    
    -- 时间戳
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    approved_at TIMESTAMP WITH TIME ZONE,
    
    -- 🔑 约束：同一个文件版本在同一个评审中只能出现一次
    UNIQUE(review_id, file_version_urn),
    
    -- 🔑 外键约束：确保引用的文件版本存在
    -- 注意：此约束要求 file_versions 表必须先存在
    CONSTRAINT fk_review_file_version_urn 
        FOREIGN KEY (file_version_urn) 
        REFERENCES file_versions(urn) 
        ON DELETE RESTRICT  -- 防止删除正在被评审的文件版本
);

-- ============================================================================
-- 4. 评审进度表
-- ============================================================================
CREATE TABLE review_progress (
    id SERIAL PRIMARY KEY,
    review_id INTEGER NOT NULL REFERENCES reviews(id) ON DELETE CASCADE,
    
    -- 步骤信息（全部可编辑）
    step_id VARCHAR(50) NOT NULL,
    template_step_id VARCHAR(50),  -- 关联到 workflow template 的步骤ID（通过 step_order 自动填充）
    step_name VARCHAR(255) NOT NULL,
    step_type step_type NOT NULL,
    step_order INTEGER NOT NULL,
    
    -- 状态信息（全部可编辑）
    status VARCHAR(20) DEFAULT 'PENDING' CHECK (status IN (
        'PENDING', 'CLAIMED', 'UNCLAIMED', 'IN_PROGRESS', 'SUBMITTED',
        'APPROVED', 'REJECTED', 'SKIPPED', 'VOID', 'COMPLETED', 'SENT_BACK'
    )),
    
    -- 参与者信息（全部可编辑）
    assigned_to JSONB DEFAULT '[]'::jsonb,
    claimed_by JSONB DEFAULT '{}'::jsonb,  -- 认领该步骤的用户对象
    completed_by JSONB DEFAULT '{}'::jsonb,
    action_by JSONB DEFAULT '{}'::jsonb,  -- 执行操作的用户（来自API）
    candidates JSONB DEFAULT '{}'::jsonb,
    
    -- 审批结果（全部可编辑）
    decision VARCHAR(20),
    comments TEXT,
    conditions TEXT,
    attachments JSONB DEFAULT '[]'::jsonb,
    
    -- 本地扩展
    internal_notes TEXT,  -- 内部备注
    notes TEXT,  -- 步骤备注（来自工作流配置或API返回）
    local_comments JSONB DEFAULT '[]'::jsonb,  -- 本地扩展评论（用户添加的额外评论）
    escalation_level INTEGER DEFAULT 0,  -- 升级级别
    
    -- 时间信息（全部可编辑）
    due_date TIMESTAMP WITH TIME ZONE,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    end_time TIMESTAMP WITH TIME ZONE,  -- 步骤结束时间（来自API）
    reminder_sent_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 条件唯一索引：只对"活跃"步骤强制唯一性
-- ============================================================================
-- 原因：send-back 功能需要为同一步骤创建多条历史记录
-- 策略：
--   - 活跃步骤 (PENDING/CLAIMED/IN_PROGRESS) 必须唯一 → 支持 UPSERT
--   - 历史步骤 (SENT_BACK/COMPLETED) 可以重复 → 支持 send-back 和历史记录
-- 效果：
--   - ON CONFLICT (review_id, step_id) WHERE status NOT IN (...) 可以正常工作
--   - 同一步骤可以有多条 COMPLETED 或 SENT_BACK 记录
--   - 批量同步的 UPSERT 功能保持正常

CREATE UNIQUE INDEX idx_review_progress_unique_active
ON review_progress(review_id, step_id)
WHERE status NOT IN ('SENT_BACK', 'COMPLETED');

-- 性能索引：用于快速查询
CREATE INDEX idx_review_progress_review_step ON review_progress(review_id, step_id);
CREATE INDEX idx_review_progress_created_at ON review_progress(review_id, step_id, created_at DESC);
CREATE INDEX idx_review_progress_status ON review_progress(review_id, status);

-- ============================================================================
-- 5. 评审评论 - 已移除独立表，评论存储在 review_progress.notes 和 local_comments 字段
-- ============================================================================
-- review_comments 表已删除
-- API 评论存储在：review_progress.notes
-- 本地评论存储在：review_progress.local_comments (JSONB)

-- ============================================================================
-- 6. 审批决策表 - 已删除
-- ============================================================================
-- 审批决策信息已整合到 review_file_versions 和 review_progress 表中
-- review_file_versions 表包含文件级别的审批状态
-- review_progress 表包含步骤级别的决策信息

-- ============================================================================
-- 7. 通知表
-- ============================================================================
CREATE TABLE review_notifications (
    id SERIAL PRIMARY KEY,
    review_id INTEGER NOT NULL REFERENCES reviews(id) ON DELETE CASCADE,
    
    -- 通知信息（全部可编辑）
    notification_type VARCHAR(50) NOT NULL CHECK (notification_type IN (
        'review_assigned', 'review_due', 'review_approved', 'review_rejected',
        'comment_added', 'step_completed', 'review_completed', 'reminder', 'escalation'
    )),
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    
    -- 接收者信息（可编辑）
    recipient JSONB NOT NULL,
    sender JSONB,
    
    -- 状态信息（全部可编辑）
    is_read BOOLEAN DEFAULT FALSE,
    is_sent BOOLEAN DEFAULT FALSE,
    delivery_method VARCHAR(20) DEFAULT 'system' CHECK (delivery_method IN ('system', 'email', 'sms', 'webhook')),
    
    -- 相关数据（可编辑）
    related_data JSONB DEFAULT '{}'::jsonb,
    action_url TEXT,
    
    -- 本地扩展
    priority INTEGER DEFAULT 3 CHECK (priority BETWEEN 1 AND 5),
    expires_at TIMESTAMP WITH TIME ZONE,
    
    -- 时间戳（全部可编辑）
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    scheduled_at TIMESTAMP WITH TIME ZONE,
    sent_at TIMESTAMP WITH TIME ZONE,
    read_at TIMESTAMP WITH TIME ZONE
);

-- ============================================================================
-- 8. 审批模板表（用于快速创建工作流）
-- ============================================================================
CREATE TABLE workflow_templates (
    id SERIAL PRIMARY KEY,
    template_uuid VARCHAR(36) UNIQUE NOT NULL,
    
    -- 模板信息
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    industry VARCHAR(100),
    
    -- ACC 模板映射
    acc_template_id VARCHAR(36),             -- ACC 模板 ID（用于同步映射）
    data_source data_source_type DEFAULT 'local_system',
    
    -- 模板类型和步骤配置
    template_type VARCHAR(50) DEFAULT 'custom' CHECK (template_type IN (
        'one_step', 'two_step', 'three_step', 'four_step', 'five_step', 'custom'
    )),
    steps_count INTEGER DEFAULT 1 CHECK (steps_count BETWEEN 1 AND 10),
    
    -- 步骤配置（详细的步骤定义）
    steps_config JSONB DEFAULT '[]'::jsonb,  -- 步骤配置数组
    /*
    步骤配置结构示例：
    [
        {
            "id": "step_1",
            "name": "Initial Review",
            "type": "REVIEWER",
            "order": 1,
            "reviewer_type": "SINGLE_REVIEWER", // SINGLE_REVIEWER, MULTIPLE_REVIEWERS, GROUP_APPROVAL
            "time_allowed": 3,
            "time_unit": "CALENDAR_DAYS", // CALENDAR_DAYS, WORKING_DAYS
            "enable_sent_back": true,
            "group_review": {
                "enabled": false,
                "type": "MINIMUM", // MINIMUM, ALL
                "min": 1
            },
            "candidates": {
                "users": [],
                "roles": [],
                "companies": []
            }
        }
    ]
    */
    
    -- 模板配置（保留原有字段用于兼容）
    template_config JSONB NOT NULL,          -- 完整的工作流配置
    default_settings JSONB DEFAULT '{}'::jsonb,
    
    -- 高级配置
    additional_options JSONB DEFAULT '{}'::jsonb,  -- 额外选项
    approval_status_options JSONB DEFAULT '[]'::jsonb,  -- 审批状态选项
    copy_files_options JSONB DEFAULT '{}'::jsonb,       -- 文件复制选项
    attached_attributes JSONB DEFAULT '[]'::jsonb,      -- 附加属性
    update_attributes_options JSONB DEFAULT '{}'::jsonb, -- 属性更新选项
    
    -- 使用统计
    usage_count INTEGER DEFAULT 0,
    
    -- 创建者
    created_by_user_id VARCHAR(100),
    created_by_user_name VARCHAR(200),
    created_by JSONB DEFAULT '{}'::jsonb,    -- 创建者详细信息
    
    -- 状态
    is_active BOOLEAN DEFAULT TRUE,
    is_public BOOLEAN DEFAULT FALSE,
    is_template BOOLEAN DEFAULT TRUE,        -- 是否为模板
    
    -- 同步信息
    last_synced_at TIMESTAMP WITH TIME ZONE,
    sync_status VARCHAR(20) DEFAULT 'pending',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建部分唯一索引（只对非NULL值生效）
CREATE UNIQUE INDEX IF NOT EXISTS idx_workflow_templates_acc_template_id 
ON workflow_templates(acc_template_id) 
WHERE acc_template_id IS NOT NULL;

-- ============================================================================
-- 9. 项目用户视图（引用account schema的数据）
-- ============================================================================
-- 注意：此视图依赖于account schema中的project_users和users表
-- 只有当这些表存在时才创建视图
DO $$
BEGIN
    -- 检查project_users和users表是否存在
    IF EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'project_users') 
       AND EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users') THEN
        
        -- 创建用户成员视图
        CREATE OR REPLACE VIEW user_members AS
        SELECT 
            pu.id,
            pu.project_id,
            pu.user_id as user_acc_id,
            pu.autodesk_id,
            pu.analytics_id,
            u.name,
            u.email,
            -- 简化字段，移除不存在的字段
            NULL as first_name,
            NULL as last_name,
            NULL::jsonb as phone,
            NULL as address_line1,
            NULL as address_line2,
            NULL as city,
            NULL as state_or_province,
            NULL as postal_code,
            NULL as country,
            NULL as job_title,
            NULL as industry,
            NULL as about_me,
            NULL as image_url,
            pu.project_company_id as company_id,
            pu.project_company_name as company_name,
            pu.access_levels,
            pu.role_ids,
            pu.roles,
            pu.products,
            pu.status,
            pu.added_on,
            pu.last_synced_at as synced_at,
            pu.updated_at
        FROM project_users pu
        JOIN users u ON pu.user_id = u.user_id;
        
        RAISE NOTICE 'user_members view created successfully';
    ELSE
        RAISE NOTICE 'Skipping user_members view creation - required tables (project_users, users) do not exist';
    END IF;
END $$;

-- ============================================================================
-- 10. 评审候选人表 - 已废弃，使用 review_step_candidates 替代
-- ============================================================================
-- 注意：review_candidates 表已被 review_step_candidates 替代
-- review_step_candidates 表在 create_review_step_candidates.sql 中定义
-- 
-- 原 review_candidates 表的功能现在由以下两个表提供：
-- 1. review_step_candidates: 存储每个评审实例的候选人配置（基于工作流模板）
-- 2. review_progress: 存储实际的步骤执行记录和状态

-- ============================================================================
-- 11. 工作流备注表（工作流级别的备註管理）
-- ============================================================================
CREATE TABLE workflow_notes (
    id SERIAL PRIMARY KEY,
    
    -- 关联信息
    workflow_id INTEGER REFERENCES workflows(id) ON DELETE CASCADE,
    review_id INTEGER REFERENCES reviews(id) ON DELETE CASCADE,
    
    -- 备注信息
    note_type VARCHAR(50) DEFAULT 'general' CHECK (note_type IN (
        'general', 'instruction', 'warning', 'requirement', 'disclaimer'
    )),
    title VARCHAR(255),
    content TEXT NOT NULL,
    
    -- 创建者信息
    created_by JSONB DEFAULT '{}'::jsonb,    -- 创建者用户对象 {autodeskId, name}
    
    -- 可见性设置
    is_visible_to_reviewers BOOLEAN DEFAULT TRUE,
    is_visible_to_initiators BOOLEAN DEFAULT TRUE,
    is_internal_note BOOLEAN DEFAULT FALSE,  -- 是否为内部备注
    
    -- 优先级
    priority INTEGER DEFAULT 3 CHECK (priority BETWEEN 1 AND 5),
    
    -- 时间戳
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 12. 文件审批历史表（用于跟踪文件在多个评审中的审批记录）
-- ============================================================================
CREATE TABLE file_approval_history (
    id SERIAL PRIMARY KEY,
    
    -- 文件信息
    file_version_urn TEXT NOT NULL,
    file_item_urn TEXT,
    file_name VARCHAR(500),
    
    -- 评审信息
    review_id INTEGER REFERENCES reviews(id) ON DELETE CASCADE,
    review_acc_id VARCHAR(36),
    review_sequence_id INTEGER,
    review_status VARCHAR(50),
    review_name VARCHAR(255),
    
    -- 审批状态信息
    approval_status_id VARCHAR(36),
    approval_status_label VARCHAR(100),
    approval_status_value VARCHAR(20),
    approval_status_type VARCHAR(20),
    
    -- 审批人信息
    approved_by JSONB,
    approved_at TIMESTAMP WITH TIME ZONE,
    
    -- 状态标记
    is_current BOOLEAN DEFAULT FALSE,
    is_latest_in_review BOOLEAN DEFAULT FALSE,
    
    -- 时间戳
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    synced_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- 唯一约束：同一文件在同一评审中的同一审批状态只记录一次
    CONSTRAINT unique_file_review_approval UNIQUE (file_version_urn, review_acc_id, approval_status_id)
);

-- ============================================================================
-- 扩展sync_tasks表（如果存在）
-- ============================================================================
DO $$
BEGIN
    -- 检查sync_tasks表是否存在
    IF EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'sync_tasks') THEN
        -- 添加新列
        ALTER TABLE sync_tasks ADD COLUMN IF NOT EXISTS synced_reviews BOOLEAN DEFAULT FALSE;
        ALTER TABLE sync_tasks ADD COLUMN IF NOT EXISTS synced_workflows BOOLEAN DEFAULT FALSE;
        ALTER TABLE sync_tasks ADD COLUMN IF NOT EXISTS synced_comments BOOLEAN DEFAULT FALSE;
        ALTER TABLE sync_tasks ADD COLUMN IF NOT EXISTS reviews_synced INTEGER DEFAULT 0;
        ALTER TABLE sync_tasks ADD COLUMN IF NOT EXISTS workflows_synced INTEGER DEFAULT 0;
        ALTER TABLE sync_tasks ADD COLUMN IF NOT EXISTS comments_synced INTEGER DEFAULT 0;

        -- 更新任务类型约束
        ALTER TABLE sync_tasks DROP CONSTRAINT IF EXISTS sync_tasks_task_type_check;
        ALTER TABLE sync_tasks ADD CONSTRAINT sync_tasks_task_type_check
        CHECK (task_type IN (
            'full_sync', 'incremental_sync', 'folder_sync', 'file_sync',
            'optimized_full_sync', 'optimized_incremental_sync',
            'review_sync', 'workflow_sync', 'review_full_sync', 'review_incremental_sync'
        ));
        
        RAISE NOTICE 'sync_tasks table extended successfully';
    ELSE
        RAISE NOTICE 'Skipping sync_tasks table extension - table does not exist';
    END IF;
END $$;

-- ============================================================================
-- 索引优化
-- ============================================================================

-- 工作流索引
CREATE INDEX idx_workflows_project ON workflows(project_id);
CREATE INDEX idx_workflows_status ON workflows(status);
CREATE INDEX idx_workflows_source ON workflows(data_source);
CREATE INDEX idx_workflows_acc_id ON workflows(acc_workflow_id) WHERE acc_workflow_id IS NOT NULL;
CREATE INDEX idx_workflows_tags ON workflows USING GIN (tags);
CREATE INDEX idx_workflows_created_by ON workflows USING GIN (created_by);
CREATE INDEX idx_workflows_created_at ON workflows(created_at DESC);

-- 评审索引
CREATE INDEX idx_reviews_project ON reviews(project_id);
CREATE INDEX idx_reviews_status ON reviews(status);
CREATE INDEX idx_reviews_workflow ON reviews(workflow_id);
CREATE INDEX idx_reviews_priority ON reviews(priority);
CREATE INDEX idx_reviews_created_at ON reviews(created_at DESC);
CREATE INDEX idx_reviews_assigned ON reviews USING GIN (assigned_to);
CREATE INDEX idx_reviews_tags ON reviews USING GIN (tags);
CREATE INDEX idx_reviews_acc_id ON reviews(acc_review_id) WHERE acc_review_id IS NOT NULL;

-- 评审文件版本索引
CREATE INDEX idx_review_file_versions_review ON review_file_versions(review_id);
CREATE INDEX idx_review_file_versions_status ON review_file_versions(approval_status);
CREATE INDEX idx_review_file_versions_urn ON review_file_versions(file_version_urn);
CREATE INDEX idx_review_file_versions_tags ON review_file_versions USING GIN (tags);
CREATE INDEX idx_review_file_versions_unique ON review_file_versions(review_id, file_version_urn);

-- 进度索引
CREATE INDEX idx_progress_review ON review_progress(review_id);
CREATE INDEX idx_progress_status ON review_progress(status);
CREATE INDEX idx_progress_step ON review_progress(step_order);
CREATE INDEX idx_progress_template_step_id ON review_progress(template_step_id) WHERE template_step_id IS NOT NULL;
CREATE INDEX idx_progress_assigned ON review_progress USING GIN (assigned_to);
CREATE INDEX idx_progress_action_by ON review_progress USING GIN (action_by);
CREATE INDEX idx_progress_due_date ON review_progress(due_date) WHERE status IN ('PENDING', 'IN_PROGRESS');
CREATE INDEX idx_progress_end_time ON review_progress(end_time DESC);

-- 评论索引（已删除 - review_comments 表不再存在）

-- 决策索引
-- 审批决策表相关索引已删除（表已删除）

-- 通知索引
CREATE INDEX idx_notifications_review ON review_notifications(review_id);
CREATE INDEX idx_notifications_recipient ON review_notifications USING GIN (recipient);
CREATE INDEX idx_notifications_unread ON review_notifications(is_read) WHERE is_read = FALSE;
CREATE INDEX idx_notifications_type ON review_notifications(notification_type);
CREATE INDEX idx_notifications_priority ON review_notifications(priority);

-- 模板索引
CREATE INDEX idx_templates_category ON workflow_templates(category);
CREATE INDEX idx_templates_active ON workflow_templates(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_templates_type ON workflow_templates(template_type);
CREATE INDEX idx_templates_acc_id ON workflow_templates(acc_template_id) WHERE acc_template_id IS NOT NULL;
CREATE INDEX idx_templates_data_source ON workflow_templates(data_source);

-- 用户成员索引 (注意：user_members是视图，不能创建索引)
-- 索引应该在底层表 project_users 和 users 上创建，这些已在 account_schema.sql 中定义

-- 评审候选人索引 - 已废弃 (review_candidates 表已删除)
-- review_step_candidates 表的索引在 create_review_step_candidates.sql 中定义

-- 工作流备注索引
CREATE INDEX idx_workflow_notes_workflow ON workflow_notes(workflow_id) WHERE workflow_id IS NOT NULL;
CREATE INDEX idx_workflow_notes_review ON workflow_notes(review_id) WHERE review_id IS NOT NULL;
CREATE INDEX idx_workflow_notes_type ON workflow_notes(note_type);
CREATE INDEX idx_workflow_notes_visibility ON workflow_notes(is_visible_to_reviewers, is_visible_to_initiators);
CREATE INDEX idx_workflow_notes_priority ON workflow_notes(priority);
CREATE INDEX idx_workflow_notes_created ON workflow_notes(created_at DESC);

-- 文件审批历史索引
CREATE INDEX idx_file_approval_history_file_urn ON file_approval_history(file_version_urn);
CREATE INDEX idx_file_approval_history_review_id ON file_approval_history(review_id);
CREATE INDEX idx_file_approval_history_review_acc_id ON file_approval_history(review_acc_id);
CREATE INDEX idx_file_approval_history_status_value ON file_approval_history(approval_status_value);
CREATE INDEX idx_file_approval_history_is_current ON file_approval_history(is_current) WHERE is_current = true;
CREATE INDEX idx_file_approval_history_approved_at ON file_approval_history(approved_at);

-- ============================================================================
-- 实用视图
-- ============================================================================

-- 评审概览视图
CREATE OR REPLACE VIEW reviews_overview AS
SELECT
    r.id,
    r.review_uuid,
    r.project_id,
    r.name,
    r.status,
    r.priority,
    r.progress_percentage,
    r.current_step_name,
    r.data_source,
    
    -- 工作流信息
    w.name as workflow_name,
    w.steps_count as total_workflow_steps,
    
    -- 统计信息
    r.total_file_versions,
    r.approved_versions,
    r.rejected_versions,
    r.pending_versions,
    
    -- 参与者信息
    r.created_by,
    r.assigned_to,
    
    -- 时间信息
    r.created_at,
    r.updated_at,
    r.started_at,
    r.finished_at,
    r.current_step_due_date,
    
    -- 状态显示
    CASE r.status
        WHEN 'OPEN' THEN '进行中'
        WHEN 'CLOSED' THEN '已完成'
        WHEN 'DRAFT' THEN '草稿'
        WHEN 'CANCELLED' THEN '已取消'
        WHEN 'VOID' THEN '已作废'
        ELSE r.status::text
    END as status_display,
    
    -- 优先级显示
    CASE r.priority
        WHEN 1 THEN '最高'
        WHEN 2 THEN '高'
        WHEN 3 THEN '中'
        WHEN 4 THEN '低'
        WHEN 5 THEN '最低'
    END as priority_display,
    
    -- 数据源显示
    CASE r.data_source
        WHEN 'acc_sync' THEN 'ACC同步'
        WHEN 'local_system' THEN '本地创建'
    END as source_display

FROM reviews r
LEFT JOIN workflows w ON r.workflow_id = w.id
ORDER BY r.priority, r.created_at DESC;

-- 待处理任务视图
CREATE OR REPLACE VIEW pending_tasks_view AS
SELECT
    rp.id,
    rp.review_id,
    r.name as review_name,
    r.priority,
    rp.step_name,
    rp.status,
    rp.assigned_to,
    rp.due_date,
    rp.created_at,
    
    -- 逾期标识
    CASE
        WHEN rp.due_date < CURRENT_TIMESTAMP THEN TRUE
        ELSE FALSE
    END as is_overdue,
    
    -- 紧急程度
    CASE
        WHEN rp.due_date < CURRENT_TIMESTAMP THEN '逾期'
        WHEN rp.due_date < CURRENT_TIMESTAMP + INTERVAL '1 day' THEN '紧急'
        WHEN rp.due_date < CURRENT_TIMESTAMP + INTERVAL '3 days' THEN '即将到期'
        ELSE '正常'
    END as urgency_level

FROM review_progress rp
JOIN reviews r ON rp.review_id = r.id
WHERE rp.status IN ('PENDING', 'CLAIMED', 'IN_PROGRESS')
ORDER BY rp.due_date ASC, r.priority ASC;

-- 工作流使用统计视图
CREATE OR REPLACE VIEW workflow_statistics AS
SELECT
    w.id,
    w.workflow_uuid,
    w.name,
    w.status,
    w.steps_count,
    w.data_source,
    
    -- 评审统计
    COUNT(DISTINCT r.id) as total_reviews,
    COUNT(DISTINCT CASE WHEN r.status = 'OPEN' THEN r.id END) as open_reviews,
    COUNT(DISTINCT CASE WHEN r.status = 'CLOSED' THEN r.id END) as closed_reviews,
    COUNT(DISTINCT CASE WHEN r.status = 'DRAFT' THEN r.id END) as draft_reviews,
    
    -- 时间统计
    w.created_at,
    w.updated_at,
    MAX(r.created_at) as last_review_created_at

FROM workflows w
LEFT JOIN reviews r ON w.id = r.workflow_id
GROUP BY w.id, w.workflow_uuid, w.name, w.status, w.steps_count, w.data_source, w.created_at, w.updated_at
ORDER BY total_reviews DESC;

-- 评审活动统计视图（已移除 review_comments 引用）
CREATE OR REPLACE VIEW review_activity_stats AS
SELECT
    r.id as review_id,
    r.review_uuid,
    r.name as review_name,
    r.status,
    
    -- 文件统计
    COUNT(DISTINCT rfv.id) as file_count,
    
    -- 评论统计（从 review_progress 获取）
    COUNT(DISTINCT CASE WHEN rp.notes IS NOT NULL AND rp.notes != '' THEN rp.id END) as progress_with_notes,
    COUNT(DISTINCT CASE WHEN jsonb_array_length(rp.local_comments) > 0 THEN rp.id END) as progress_with_local_comments,
    
    -- 决策统计（从review_progress获取）
    COUNT(DISTINCT CASE WHEN rp.decision = 'APPROVED' THEN rp.id END) as approved_decisions,
    COUNT(DISTINCT CASE WHEN rp.decision = 'REJECTED' THEN rp.id END) as rejected_decisions,
    
    -- 进度统计
    COUNT(DISTINCT rp.id) as total_steps,
    COUNT(DISTINCT CASE WHEN rp.status IN ('APPROVED', 'SUBMITTED') THEN rp.id END) as completed_steps,
    
    -- 最新活动时间
    GREATEST(
        MAX(rfv.updated_at),
        MAX(rp.updated_at)
    ) as last_activity_at

FROM reviews r
LEFT JOIN review_file_versions rfv ON r.id = rfv.review_id
LEFT JOIN review_progress rp ON r.id = rp.review_id
GROUP BY r.id, r.review_uuid, r.name, r.status
ORDER BY last_activity_at DESC NULLS LAST;

-- 文件审批摘要物化视图
CREATE MATERIALIZED VIEW mv_file_approval_summary AS
SELECT 
    fah.file_version_urn,
    fah.file_name,
    COUNT(DISTINCT fah.review_id) AS total_reviews,
    COUNT(*) FILTER (WHERE fah.approval_status_value = 'APPROVED') AS approved_count,
    COUNT(*) FILTER (WHERE fah.approval_status_value = 'REJECTED') AS rejected_count,
    COUNT(*) FILTER (WHERE fah.review_status = 'OPEN') AS in_review_count,
    MAX(fah.approved_at) AS last_approved_at,
    CASE 
        WHEN COUNT(*) FILTER (WHERE fah.review_status = 'OPEN') > 0 THEN 'IN_REVIEW'
        WHEN COUNT(*) FILTER (WHERE fah.approval_status_value = 'REJECTED') > 0 THEN 'REJECTED'
        WHEN COUNT(*) FILTER (WHERE fah.approval_status_value = 'APPROVED') > 0 THEN 'APPROVED'
        ELSE 'UNKNOWN'
    END AS current_status,
    NOW() AS refreshed_at
FROM file_approval_history fah
GROUP BY fah.file_version_urn, fah.file_name;

-- 为物化视图创建唯一索引
CREATE UNIQUE INDEX idx_mv_file_approval_summary_urn ON mv_file_approval_summary(file_version_urn);
CREATE INDEX idx_mv_file_approval_summary_status ON mv_file_approval_summary(current_status);

-- ============================================================================
-- 触发器函数
-- ============================================================================

-- 自动更新统计信息
CREATE OR REPLACE FUNCTION update_review_statistics()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE reviews SET
        total_file_versions = (
            SELECT COUNT(*) FROM review_file_versions
            WHERE review_id = COALESCE(NEW.review_id, OLD.review_id)
        ),
        approved_versions = (
            SELECT COUNT(*) FROM review_file_versions
            WHERE review_id = COALESCE(NEW.review_id, OLD.review_id)
            AND approval_status = 'APPROVED'
        ),
        rejected_versions = (
            SELECT COUNT(*) FROM review_file_versions
            WHERE review_id = COALESCE(NEW.review_id, OLD.review_id)
            AND approval_status = 'REJECTED'
        ),
        pending_versions = (
            SELECT COUNT(*) FROM review_file_versions
            WHERE review_id = COALESCE(NEW.review_id, OLD.review_id)
            AND approval_status IN ('PENDING', 'IN_REVIEW')
        ),
        updated_at = CURRENT_TIMESTAMP
    WHERE id = COALESCE(NEW.review_id, OLD.review_id);
    
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_review_statistics
    AFTER INSERT OR UPDATE OR DELETE ON review_file_versions
    FOR EACH ROW EXECUTE FUNCTION update_review_statistics();

-- ============================================================================
-- 🔑 更新文件版本的reviewState状态
-- ============================================================================

CREATE OR REPLACE FUNCTION update_file_version_review_state()
RETURNS TRIGGER AS $$
DECLARE
    v_new_review_state VARCHAR(20);
BEGIN
    -- 计算新的review状态
    SELECT compute_file_version_review_state(COALESCE(NEW.file_version_urn, OLD.file_version_urn))
    INTO v_new_review_state;

    -- 更新对应的file_version记录
    UPDATE file_versions
    SET review_state = v_new_review_state
    WHERE urn = COALESCE(NEW.file_version_urn, OLD.file_version_urn);

    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_file_version_review_state
    AFTER INSERT OR UPDATE OR DELETE ON review_file_versions
    FOR EACH ROW EXECUTE FUNCTION update_file_version_review_state();

-- 自动更新工作流统计
CREATE OR REPLACE FUNCTION update_workflow_statistics()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE workflows SET
        total_reviews = (
            SELECT COUNT(*) FROM reviews
            WHERE workflow_id = COALESCE(NEW.workflow_id, OLD.workflow_id)
        ),
        active_reviews = (
            SELECT COUNT(*) FROM reviews
            WHERE workflow_id = COALESCE(NEW.workflow_id, OLD.workflow_id)
            AND status IN ('OPEN', 'DRAFT')
        ),
        updated_at = CURRENT_TIMESTAMP
    WHERE id = COALESCE(NEW.workflow_id, OLD.workflow_id);
    
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_workflow_statistics
    AFTER INSERT OR UPDATE OR DELETE ON reviews
    FOR EACH ROW 
    EXECUTE FUNCTION update_workflow_statistics();

-- 自动更新时间戳
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- 自动同步 workflow_id 和 workflow_uuid
-- ============================================================================

-- 为 workflows 表：自动生成 workflow_uuid（如果缺失）
CREATE OR REPLACE FUNCTION auto_generate_workflow_uuid()
RETURNS TRIGGER AS $$
BEGIN
    -- 如果 workflow_uuid 为空，自动生成
    IF NEW.workflow_uuid IS NULL THEN
        NEW.workflow_uuid = uuid_generate_v4()::VARCHAR(36);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_auto_generate_workflow_uuid
    BEFORE INSERT ON workflows
    FOR EACH ROW 
    EXECUTE FUNCTION auto_generate_workflow_uuid();

-- 为 reviews 表：自动同步 workflow_id 基于 workflow_uuid
CREATE OR REPLACE FUNCTION auto_sync_review_workflow_id()
RETURNS TRIGGER AS $$
DECLARE
    v_workflow_id INTEGER;
BEGIN
    -- 如果有 workflow_uuid 但没有 workflow_id，自动查找并设置
    IF NEW.workflow_uuid IS NOT NULL AND NEW.workflow_id IS NULL THEN
        SELECT id INTO v_workflow_id
        FROM workflows
        WHERE workflow_uuid = NEW.workflow_uuid OR acc_workflow_id = NEW.workflow_uuid
        LIMIT 1;
        
        IF v_workflow_id IS NOT NULL THEN
            NEW.workflow_id = v_workflow_id;
        END IF;
    END IF;
    
    -- 如果有 workflow_id 但没有 workflow_uuid，自动查找并设置
    IF NEW.workflow_id IS NOT NULL AND NEW.workflow_uuid IS NULL THEN
        SELECT workflow_uuid INTO NEW.workflow_uuid
        FROM workflows
        WHERE id = NEW.workflow_id
        LIMIT 1;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_auto_sync_review_workflow_id
    BEFORE INSERT OR UPDATE ON reviews
    FOR EACH ROW 
    EXECUTE FUNCTION auto_sync_review_workflow_id();

-- 为所有主要表添加更新时间戳触发器
CREATE TRIGGER trigger_workflows_update_timestamp
    BEFORE UPDATE ON workflows
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trigger_reviews_update_timestamp
    BEFORE UPDATE ON reviews
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trigger_file_versions_update_timestamp
    BEFORE UPDATE ON review_file_versions
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trigger_progress_update_timestamp
    BEFORE UPDATE ON review_progress
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

-- review_comments 表已删除，触发器已移除

-- approval_decisions 表触发器已删除（表已删除）

CREATE TRIGGER trigger_templates_update_timestamp
    BEFORE UPDATE ON workflow_templates
    FOR EACH ROW EXECUTE FUNCTION update_timestamp();

-- 自动更新评审进度百分比
CREATE OR REPLACE FUNCTION update_review_progress_percentage()
RETURNS TRIGGER AS $$
DECLARE
    total_steps_count INTEGER;
    completed_steps_count INTEGER;
    progress_pct DECIMAL(5,2);
BEGIN
    -- 获取总步骤数和已完成步骤数
    SELECT 
        COUNT(*),
        COUNT(*) FILTER (WHERE status IN ('APPROVED', 'SUBMITTED'))
    INTO total_steps_count, completed_steps_count
    FROM review_progress
    WHERE review_id = COALESCE(NEW.review_id, OLD.review_id);
    
    -- 计算进度百分比
    IF total_steps_count > 0 THEN
        progress_pct := (completed_steps_count::DECIMAL / total_steps_count::DECIMAL) * 100;
    ELSE
        progress_pct := 0;
    END IF;
    
    -- 更新评审表
    UPDATE reviews SET
        progress_percentage = progress_pct,
        total_steps = total_steps_count,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = COALESCE(NEW.review_id, OLD.review_id);
    
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_review_progress
    AFTER INSERT OR UPDATE OR DELETE ON review_progress
    FOR EACH ROW EXECUTE FUNCTION update_review_progress_percentage();

-- ============================================================================
-- 实用函数
-- ============================================================================

-- 创建评审（从工作流）
CREATE OR REPLACE FUNCTION create_review_from_workflow(
    p_workflow_id INTEGER,
    p_review_name VARCHAR(255),
    p_created_by_user_id VARCHAR(100),
    p_created_by_user_name VARCHAR(200)
)
RETURNS INTEGER AS $$
DECLARE
    v_review_id INTEGER;
    v_workflow_record RECORD;
    v_step JSONB;
    v_step_order INTEGER := 1;
BEGIN
    -- 获取工作流信息
    SELECT * INTO v_workflow_record FROM workflows WHERE id = p_workflow_id;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION '工作流不存在: %', p_workflow_id;
    END IF;
    
    -- 创建评审
    INSERT INTO reviews (
        review_uuid,
        project_id,
        workflow_id,
        name,
        workflow_uuid,
        created_by,
        status,
        total_steps
    ) VALUES (
        uuid_generate_v4()::VARCHAR(36),
        v_workflow_record.project_id,
        p_workflow_id,
        p_review_name,
        v_workflow_record.workflow_uuid,
        jsonb_build_object(
            'user_id', p_created_by_user_id,
            'user_name', p_created_by_user_name
        ),
        'DRAFT',
        jsonb_array_length(v_workflow_record.steps)
    )
    RETURNING id INTO v_review_id;
    
    -- 创建评审进度步骤
    FOR v_step IN SELECT * FROM jsonb_array_elements(v_workflow_record.steps)
    LOOP
        INSERT INTO review_progress (
            review_id,
            step_id,
            step_name,
            step_type,
            step_order,
            status
        ) VALUES (
            v_review_id,
            v_step->>'id',
            v_step->>'name',
            (v_step->>'type')::step_type,
            v_step_order,
            'PENDING'
        );
        
        v_step_order := v_step_order + 1;
    END LOOP;
    
    RETURN v_review_id;
END;
$$ LANGUAGE plpgsql;

-- 获取用户待处理任务
CREATE OR REPLACE FUNCTION get_user_pending_tasks(p_user_id VARCHAR(100))
RETURNS TABLE (
    review_id INTEGER,
    review_name VARCHAR(255),
    step_name VARCHAR(255),
    due_date TIMESTAMP WITH TIME ZONE,
    priority INTEGER,
    is_overdue BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        rp.review_id,
        r.name,
        rp.step_name,
        rp.due_date,
        r.priority,
        (rp.due_date < CURRENT_TIMESTAMP) as is_overdue
    FROM review_progress rp
    JOIN reviews r ON rp.review_id = r.id
    WHERE rp.status IN ('PENDING', 'CLAIMED', 'IN_PROGRESS')
    AND rp.assigned_to @> jsonb_build_array(jsonb_build_object('user_id', p_user_id))
    ORDER BY rp.due_date ASC NULLS LAST, r.priority ASC;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- 注释说明
-- ============================================================================

COMMENT ON TABLE workflows IS '统一工作流表 - 存储ACC同步和本地创建的工作流，全部可编辑';
COMMENT ON TABLE reviews IS '统一评审表 - 存储所有评审记录，支持完全的CRUD操作';
COMMENT ON TABLE review_file_versions IS '评审文件版本表 - 记录评审中的文件及其审批状态';
COMMENT ON TABLE review_progress IS '评审进度表 - 跟踪评审的每个步骤进度，评论存储在notes和local_comments字段';
-- approval_decisions 表注释已删除（表已删除）
COMMENT ON TABLE review_notifications IS '通知表 - 管理评审相关的通知消息';
COMMENT ON TABLE workflow_templates IS '工作流模板表 - 存储可重用的工作流模板，支持1-5步骤和高级配置';
COMMENT ON VIEW user_members IS '项目用户视图 - 引用account schema的用户数据';
-- COMMENT ON TABLE review_candidates - 表已删除，使用 review_step_candidates 替代
COMMENT ON TABLE workflow_notes IS '工作流备注表 - 管理工作流和评审级别的备注信息';
COMMENT ON TABLE file_approval_history IS '文件审批历史表 - 跟踪文件在多个评审中的审批记录';

COMMENT ON COLUMN workflows.data_source IS '数据源标识，仅用于追踪来源，不限制操作权限';
COMMENT ON COLUMN workflows.created_by IS '创建者信息对象 {autodeskId, name}';
COMMENT ON COLUMN reviews.data_source IS '数据源标识，仅用于追踪来源，不限制操作权限';
COMMENT ON COLUMN reviews.notes IS '评审备注（对应ACC API的notes字段）';
COMMENT ON COLUMN reviews.description IS '评审描述（本地扩展字段）';
COMMENT ON COLUMN workflows.acc_workflow_id IS 'ACC原始工作流ID，用于同步映射';
COMMENT ON COLUMN reviews.acc_review_id IS 'ACC原始评审ID，用于同步映射';
COMMENT ON COLUMN review_progress.template_step_id IS '关联到 workflow template 的步骤ID（通过 step_order 自动填充，用于匹配 review_step_candidates）';
COMMENT ON COLUMN review_progress.claimed_by IS '认领该步骤的用户对象（API返回单个对象）';
COMMENT ON COLUMN review_progress.action_by IS '执行操作的用户对象（来自ACC API）';
COMMENT ON COLUMN review_progress.end_time IS '步骤结束时间（来自ACC API）';
COMMENT ON COLUMN review_progress.notes IS '步骤备注（来自工作流配置或API返回）';
COMMENT ON COLUMN review_progress.local_comments IS '本地扩展评论数组，存储用户添加的额外评论 [{comment_id, user_id, user_name, comment, created_at, is_internal}]';
COMMENT ON COLUMN review_file_versions.approval_status IS '审批状态枚举值';
COMMENT ON COLUMN review_file_versions.approval_status_id IS '审批状态选项的UUID（来自ACC API）';
COMMENT ON COLUMN review_file_versions.approval_status_value IS '审批状态的内部值 (APPROVED/REJECTED等)';
COMMENT ON COLUMN review_file_versions.approval_label IS '审批状态的显示标签';

-- ============================================================================
-- 完成
-- ============================================================================

