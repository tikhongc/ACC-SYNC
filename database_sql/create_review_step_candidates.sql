-- 创建评审步骤候选人配置表
-- 用于存储每个评审实例的候选人配置（基于工作流模板，但可以修改）

CREATE TABLE IF NOT EXISTS review_step_candidates (
    id SERIAL PRIMARY KEY,
    
    -- 关联信息（只关联评审实例）
    review_id INTEGER NOT NULL REFERENCES reviews(id) ON DELETE CASCADE,
    step_id VARCHAR(50) NOT NULL,
    
    -- 步骤基本信息（冗余存储，便于查询）
    step_name VARCHAR(255),
    step_type VARCHAR(50),
    step_order INTEGER,
    
    -- 候选人配置（核心数据）
    candidates JSONB NOT NULL DEFAULT '{
        "users": [],
        "roles": [], 
        "companies": []
    }',
    
    -- 配置来源和状态
    source VARCHAR(50) DEFAULT 'workflow_template' CHECK (source IN ('workflow_template', 'manual', 'custom', 'test_setup', 'acc_sync', 'api_sync')),
    is_active BOOLEAN DEFAULT true,
    
    -- 时间戳
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- 唯一约束
    UNIQUE(review_id, step_id)
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_review_step_candidates_review_id ON review_step_candidates(review_id);
CREATE INDEX IF NOT EXISTS idx_review_step_candidates_step_id ON review_step_candidates(step_id);
CREATE INDEX IF NOT EXISTS idx_review_step_candidates_source ON review_step_candidates(source);

-- 创建更新时间触发器
CREATE OR REPLACE FUNCTION update_review_step_candidates_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_update_review_step_candidates_updated_at ON review_step_candidates;

CREATE TRIGGER trigger_update_review_step_candidates_updated_at
    BEFORE UPDATE ON review_step_candidates
    FOR EACH ROW
    EXECUTE FUNCTION update_review_step_candidates_updated_at();

-- 添加注释
COMMENT ON TABLE review_step_candidates IS '评审步骤候选人配置表 - 存储每个评审实例的候选人配置';
COMMENT ON COLUMN review_step_candidates.review_id IS '关联的评审ID';
COMMENT ON COLUMN review_step_candidates.step_id IS '步骤ID';
COMMENT ON COLUMN review_step_candidates.candidates IS '候选人配置 JSON';
COMMENT ON COLUMN review_step_candidates.source IS '配置来源：workflow(工作流模板), custom(用户自定义), acc_sync(ACC同步)';
