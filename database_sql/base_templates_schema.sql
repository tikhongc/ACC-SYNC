-- ============================================================================
-- 基础模板表 - 存储系统预定义的工作流模板结构
-- ============================================================================

-- 基础模板表
CREATE TABLE IF NOT EXISTS base_templates (
    id SERIAL PRIMARY KEY,
    template_key VARCHAR(50) UNIQUE NOT NULL,  -- 'one_step', 'two_step_group' 等
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50) DEFAULT 'standard',   -- 'standard', 'group', 'advanced'
    
    -- 基础结构配置
    steps_count INTEGER NOT NULL,
    base_steps_config JSONB NOT NULL,          -- 基础步骤结构（无具体参数）
    
    -- 模板特征
    has_group_review BOOLEAN DEFAULT FALSE,
    complexity_level VARCHAR(20) DEFAULT 'simple',  -- 'simple', 'moderate', 'complex'
    
    -- 默认配置
    default_time_allowed INTEGER DEFAULT 3,
    default_time_unit VARCHAR(20) DEFAULT 'CALENDAR_DAYS',
    
    -- 系统字段
    is_system_template BOOLEAN DEFAULT TRUE,
    display_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_base_templates_category ON base_templates(category);
CREATE INDEX IF NOT EXISTS idx_base_templates_active ON base_templates(is_active);
CREATE INDEX IF NOT EXISTS idx_base_templates_display_order ON base_templates(display_order);

-- 更新workflow_templates表的template_type枚举，添加组审核类型
DO $$
BEGIN
    -- 检查并添加新的模板类型
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.check_constraints 
        WHERE constraint_name LIKE '%workflow_templates_template_type_check%'
        AND check_clause LIKE '%two_step_group%'
    ) THEN
        -- 删除旧的约束
        ALTER TABLE workflow_templates DROP CONSTRAINT IF EXISTS workflow_templates_template_type_check;
        
        -- 添加新的约束
        ALTER TABLE workflow_templates ADD CONSTRAINT workflow_templates_template_type_check 
        CHECK (template_type IN (
            'one_step', 'two_step', 'three_step', 'four_step', 'five_step', 
            'two_step_group', 'three_step_group', 'four_step_group', 'five_step_group',
            'custom'
        ));
    END IF;
END $$;

-- 添加基础模板关联字段到workflow_templates表
ALTER TABLE workflow_templates ADD COLUMN IF NOT EXISTS base_template_key VARCHAR(50);
ALTER TABLE workflow_templates ADD COLUMN IF NOT EXISTS template_characteristics JSONB DEFAULT '{}'::jsonb;

-- 创建外键关联（可选）
-- ALTER TABLE workflow_templates ADD CONSTRAINT fk_base_template 
--     FOREIGN KEY (base_template_key) REFERENCES base_templates(template_key);

-- 插入预定义基础模板数据
INSERT INTO base_templates (template_key, name, description, steps_count, base_steps_config, has_group_review, category, display_order) 
VALUES 
-- 标准审批模板
('one_step', 'One Step Approval', '单步审批流程', 1, 
'[{"id":"step_1","name":"Review","type":"REVIEWER","order":1,"reviewer_type":"SINGLE_REVIEWER","time_allowed":3,"time_unit":"CALENDAR_DAYS","enable_sent_back":true,"group_review":{"enabled":false},"candidates":{"users":[],"roles":[],"companies":[]}}]'::jsonb, 
FALSE, 'standard', 1),

('two_step', 'Two Step Approval', '两步审批流程', 2, 
'[{"id":"step_1","name":"Initial Review","type":"REVIEWER","order":1,"reviewer_type":"SINGLE_REVIEWER","time_allowed":3,"time_unit":"CALENDAR_DAYS","enable_sent_back":true,"group_review":{"enabled":false},"candidates":{"users":[],"roles":[],"companies":[]}},{"id":"step_2","name":"Final Review","type":"APPROVER","order":2,"reviewer_type":"SINGLE_REVIEWER","time_allowed":3,"time_unit":"CALENDAR_DAYS","enable_sent_back":true,"group_review":{"enabled":false},"candidates":{"users":[],"roles":[],"companies":[]}}]'::jsonb, 
FALSE, 'standard', 2),

('three_step', 'Three Step Approval', '三步审批流程', 3, 
'[{"id":"step_1","name":"Initial Review","type":"REVIEWER","order":1,"reviewer_type":"SINGLE_REVIEWER","time_allowed":3,"time_unit":"CALENDAR_DAYS","enable_sent_back":true,"group_review":{"enabled":false},"candidates":{"users":[],"roles":[],"companies":[]}},{"id":"step_2","name":"Secondary Review","type":"REVIEWER","order":2,"reviewer_type":"SINGLE_REVIEWER","time_allowed":3,"time_unit":"CALENDAR_DAYS","enable_sent_back":true,"group_review":{"enabled":false},"candidates":{"users":[],"roles":[],"companies":[]}},{"id":"step_3","name":"Final Review","type":"APPROVER","order":3,"reviewer_type":"SINGLE_REVIEWER","time_allowed":3,"time_unit":"CALENDAR_DAYS","enable_sent_back":true,"group_review":{"enabled":false},"candidates":{"users":[],"roles":[],"companies":[]}}]'::jsonb, 
FALSE, 'standard', 3),

('four_step', 'Four Step Approval', '四步审批流程', 4, 
'[{"id":"step_1","name":"Initial Review","type":"REVIEWER","order":1,"reviewer_type":"SINGLE_REVIEWER","time_allowed":3,"time_unit":"CALENDAR_DAYS","enable_sent_back":true,"group_review":{"enabled":false},"candidates":{"users":[],"roles":[],"companies":[]}},{"id":"step_2","name":"Secondary Review","type":"REVIEWER","order":2,"reviewer_type":"SINGLE_REVIEWER","time_allowed":3,"time_unit":"CALENDAR_DAYS","enable_sent_back":true,"group_review":{"enabled":false},"candidates":{"users":[],"roles":[],"companies":[]}},{"id":"step_3","name":"Tertiary Review","type":"REVIEWER","order":3,"reviewer_type":"SINGLE_REVIEWER","time_allowed":3,"time_unit":"CALENDAR_DAYS","enable_sent_back":true,"group_review":{"enabled":false},"candidates":{"users":[],"roles":[],"companies":[]}},{"id":"step_4","name":"Final Review","type":"APPROVER","order":4,"reviewer_type":"SINGLE_REVIEWER","time_allowed":3,"time_unit":"CALENDAR_DAYS","enable_sent_back":true,"group_review":{"enabled":false},"candidates":{"users":[],"roles":[],"companies":[]}}]'::jsonb, 
FALSE, 'standard', 4),

('five_step', 'Five Step Approval', '五步审批流程', 5, 
'[{"id":"step_1","name":"Initial Review","type":"REVIEWER","order":1,"reviewer_type":"SINGLE_REVIEWER","time_allowed":3,"time_unit":"CALENDAR_DAYS","enable_sent_back":true,"group_review":{"enabled":false},"candidates":{"users":[],"roles":[],"companies":[]}},{"id":"step_2","name":"Secondary Review","type":"REVIEWER","order":2,"reviewer_type":"SINGLE_REVIEWER","time_allowed":3,"time_unit":"CALENDAR_DAYS","enable_sent_back":true,"group_review":{"enabled":false},"candidates":{"users":[],"roles":[],"companies":[]}},{"id":"step_3","name":"Tertiary Review","type":"REVIEWER","order":3,"reviewer_type":"SINGLE_REVIEWER","time_allowed":3,"time_unit":"CALENDAR_DAYS","enable_sent_back":true,"group_review":{"enabled":false},"candidates":{"users":[],"roles":[],"companies":[]}},{"id":"step_4","name":"Quaternary Review","type":"REVIEWER","order":4,"reviewer_type":"SINGLE_REVIEWER","time_allowed":3,"time_unit":"CALENDAR_DAYS","enable_sent_back":true,"group_review":{"enabled":false},"candidates":{"users":[],"roles":[],"companies":[]}},{"id":"step_5","name":"Final Review","type":"APPROVER","order":5,"reviewer_type":"SINGLE_REVIEWER","time_allowed":3,"time_unit":"CALENDAR_DAYS","enable_sent_back":true,"group_review":{"enabled":false},"candidates":{"users":[],"roles":[],"companies":[]}}]'::jsonb, 
FALSE, 'standard', 5),

-- 组审批模板
('two_step_group', 'Two Step Group Approval', '两步组审批流程', 2, 
'[{"id":"step_1","name":"Initial Review","type":"REVIEWER","order":1,"reviewer_type":"GROUP_APPROVAL","time_allowed":3,"time_unit":"CALENDAR_DAYS","enable_sent_back":true,"group_review":{"enabled":true,"type":"MINIMUM","min":1},"candidates":{"users":[],"roles":[],"companies":[]}},{"id":"step_2","name":"Final Review","type":"APPROVER","order":2,"reviewer_type":"SINGLE_REVIEWER","time_allowed":3,"time_unit":"CALENDAR_DAYS","enable_sent_back":true,"group_review":{"enabled":false},"candidates":{"users":[],"roles":[],"companies":[]}}]'::jsonb, 
TRUE, 'group', 6),

('three_step_group', 'Three Step Group Approval', '三步组审批流程', 3, 
'[{"id":"step_1","name":"Initial Review","type":"REVIEWER","order":1,"reviewer_type":"GROUP_APPROVAL","time_allowed":3,"time_unit":"CALENDAR_DAYS","enable_sent_back":true,"group_review":{"enabled":true,"type":"MINIMUM","min":1},"candidates":{"users":[],"roles":[],"companies":[]}},{"id":"step_2","name":"Secondary Review","type":"REVIEWER","order":2,"reviewer_type":"GROUP_APPROVAL","time_allowed":3,"time_unit":"CALENDAR_DAYS","enable_sent_back":true,"group_review":{"enabled":true,"type":"MINIMUM","min":1},"candidates":{"users":[],"roles":[],"companies":[]}},{"id":"step_3","name":"Final Review","type":"APPROVER","order":3,"reviewer_type":"SINGLE_REVIEWER","time_allowed":3,"time_unit":"CALENDAR_DAYS","enable_sent_back":true,"group_review":{"enabled":false},"candidates":{"users":[],"roles":[],"companies":[]}}]'::jsonb, 
TRUE, 'group', 7),

('four_step_group', 'Four Step Group Approval', '四步组审批流程', 4, 
'[{"id":"step_1","name":"Initial Review","type":"REVIEWER","order":1,"reviewer_type":"GROUP_APPROVAL","time_allowed":3,"time_unit":"CALENDAR_DAYS","enable_sent_back":true,"group_review":{"enabled":true,"type":"MINIMUM","min":1},"candidates":{"users":[],"roles":[],"companies":[]}},{"id":"step_2","name":"Secondary Review","type":"REVIEWER","order":2,"reviewer_type":"GROUP_APPROVAL","time_allowed":3,"time_unit":"CALENDAR_DAYS","enable_sent_back":true,"group_review":{"enabled":true,"type":"MINIMUM","min":1},"candidates":{"users":[],"roles":[],"companies":[]}},{"id":"step_3","name":"Tertiary Review","type":"REVIEWER","order":3,"reviewer_type":"GROUP_APPROVAL","time_allowed":3,"time_unit":"CALENDAR_DAYS","enable_sent_back":true,"group_review":{"enabled":true,"type":"MINIMUM","min":1},"candidates":{"users":[],"roles":[],"companies":[]}},{"id":"step_4","name":"Final Review","type":"APPROVER","order":4,"reviewer_type":"SINGLE_REVIEWER","time_allowed":3,"time_unit":"CALENDAR_DAYS","enable_sent_back":true,"group_review":{"enabled":false},"candidates":{"users":[],"roles":[],"companies":[]}}]'::jsonb, 
TRUE, 'group', 8)

ON CONFLICT (template_key) DO UPDATE SET
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    base_steps_config = EXCLUDED.base_steps_config,
    updated_at = CURRENT_TIMESTAMP;

-- 添加注释
COMMENT ON TABLE base_templates IS '基础工作流模板表 - 存储系统预定义的模板结构';
COMMENT ON COLUMN base_templates.template_key IS '模板键值，用于程序中引用';
COMMENT ON COLUMN base_templates.base_steps_config IS '基础步骤配置，不包含具体的审核者信息';
COMMENT ON COLUMN base_templates.has_group_review IS '是否包含组审核步骤';
COMMENT ON COLUMN base_templates.complexity_level IS '模板复杂度：simple, moderate, complex';
