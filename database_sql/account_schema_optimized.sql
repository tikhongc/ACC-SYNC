-- ============================================================================
-- 优化的Account Schema - 简化版本
-- 删除冗余表，简化关联关系，保持核心功能
-- Version: 2.0 - Optimized
-- Created: 2025-11-11
-- ============================================================================

-- 启用必要的扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- ============================================================================
-- 基础枚举类型（简化）
-- ============================================================================

-- 用户状态类型
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_status_type') THEN
        CREATE TYPE user_status_type AS ENUM ('active', 'inactive', 'pending');
    END IF;
END $$;

-- 公司贸易类型（简化为核心类型）
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'trade_type') THEN
        CREATE TYPE trade_type AS ENUM (
            'General Contractor', 'Architect', 'Engineer', 'Consultant', 'Other'
        );
    END IF;
END $$;

-- ============================================================================
-- 1. 账户表（简化）
-- ============================================================================
CREATE TABLE IF NOT EXISTS accounts (
    account_id VARCHAR(36) PRIMARY KEY,  -- 直接使用ACC ID作为主键
    name VARCHAR(255) NOT NULL,
    region VARCHAR(10) DEFAULT 'US',
    
    -- 基本统计（可选）
    total_users INTEGER DEFAULT 0,
    total_projects INTEGER DEFAULT 0,
    
    -- 同步相关字段
    last_synced_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    sync_status VARCHAR(20) DEFAULT 'pending',
    
    -- 时间戳
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 2. 公司表（简化）
-- ============================================================================
CREATE TABLE IF NOT EXISTS companies (
    company_id VARCHAR(36) PRIMARY KEY,  -- 直接使用ACC ID作为主键
    account_id VARCHAR(36) NOT NULL REFERENCES accounts(account_id) ON DELETE CASCADE,
    
    -- 基本信息
    name VARCHAR(255) NOT NULL,
    trade trade_type,
    
    -- 联系信息（简化）
    country VARCHAR(255),
    
    -- 时间戳
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 3. 角色表（简化）
-- ============================================================================
CREATE TABLE IF NOT EXISTS roles (
    role_id VARCHAR(36) PRIMARY KEY,  -- 直接使用ACC ID作为主键
    account_id VARCHAR(36) REFERENCES accounts(account_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- 时间戳
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 4. 用户表（简化 + 角色关联）
-- ============================================================================
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(36) PRIMARY KEY,  -- 直接使用ACC ID作为主键
    account_id VARCHAR(36) NOT NULL REFERENCES accounts(account_id) ON DELETE CASCADE,
    
    -- 基本信息
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    status user_status_type DEFAULT 'active',
    
    -- 公司关联
    company_id VARCHAR(36) REFERENCES companies(company_id) ON DELETE SET NULL,
    
    -- 角色关联（新增）
    default_role_id VARCHAR(36) REFERENCES roles(role_id) ON DELETE SET NULL,  -- 默认角色
    account_roles JSONB DEFAULT '[]'::jsonb,  -- 账户级角色列表 [{id, name}]
    
    -- 时间戳
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 5. 项目表（新增）
-- ============================================================================
CREATE TABLE IF NOT EXISTS projects (
    project_id VARCHAR(100) PRIMARY KEY,  -- ACC Project ID (increased from 36 to handle longer IDs)
    account_id VARCHAR(36) NOT NULL REFERENCES accounts(account_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    
    -- 时间戳
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- 6. 项目用户关联表（保留，这是核心）
-- ============================================================================
CREATE TABLE IF NOT EXISTS project_users (
    id SERIAL PRIMARY KEY,
    project_id VARCHAR(100) NOT NULL REFERENCES projects(project_id) ON DELETE CASCADE,
    user_id VARCHAR(36) NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- 项目用户的额外标识符
    project_user_id VARCHAR(36),  -- 项目中的用户ID
    autodesk_id VARCHAR(36),      -- Autodesk ID
    analytics_id VARCHAR(36),     -- Analytics ID
    
    -- 项目中的状态和权限
    status user_status_type DEFAULT 'active',
    access_levels JSONB DEFAULT '{}'::jsonb,  -- {accountAdmin: true, projectAdmin: false, executive: true}
    
    -- 角色信息（项目级角色）
    role_ids JSONB DEFAULT '[]'::jsonb,  -- 角色ID列表
    roles JSONB DEFAULT '[]'::jsonb,     -- 项目中的角色列表 [{id, name}]
    products JSONB DEFAULT '[]'::jsonb,  -- 产品权限列表
    
    -- 项目中的公司信息（可能与账户级不同）
    project_company_id VARCHAR(36),
    project_company_name VARCHAR(255),
    
    -- 同步相关字段
    added_on TIMESTAMP WITH TIME ZONE,
    last_synced_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    sync_status VARCHAR(20) DEFAULT 'pending',
    
    -- 时间戳
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- 唯一约束
    UNIQUE(project_id, user_id)
);

-- ============================================================================
-- 索引优化（简化）
-- ============================================================================

-- 基本索引
CREATE INDEX IF NOT EXISTS idx_companies_account ON companies(account_id);
CREATE INDEX IF NOT EXISTS idx_companies_name ON companies(name);
CREATE INDEX IF NOT EXISTS idx_companies_trade ON companies(trade) WHERE trade IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_users_account ON users(account_id);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_company ON users(company_id) WHERE company_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_users_status ON users(status);
CREATE INDEX IF NOT EXISTS idx_users_default_role ON users(default_role_id) WHERE default_role_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_users_account_roles ON users USING GIN (account_roles);

CREATE INDEX IF NOT EXISTS idx_projects_account ON projects(account_id);
CREATE INDEX IF NOT EXISTS idx_projects_name ON projects(name);

CREATE INDEX IF NOT EXISTS idx_roles_account ON roles(account_id) WHERE account_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_roles_name ON roles(name);

-- 项目用户索引
CREATE INDEX IF NOT EXISTS idx_project_users_project ON project_users(project_id);
CREATE INDEX IF NOT EXISTS idx_project_users_user ON project_users(user_id);
CREATE INDEX IF NOT EXISTS idx_project_users_status ON project_users(status);
CREATE INDEX IF NOT EXISTS idx_project_users_roles ON project_users USING GIN (roles);
CREATE INDEX IF NOT EXISTS idx_project_users_role_ids ON project_users USING GIN (role_ids);
CREATE INDEX IF NOT EXISTS idx_project_users_access_levels ON project_users USING GIN (access_levels);
CREATE INDEX IF NOT EXISTS idx_project_users_sync_status ON project_users(sync_status);
CREATE INDEX IF NOT EXISTS idx_project_users_autodesk_id ON project_users(autodesk_id) WHERE autodesk_id IS NOT NULL;

-- ============================================================================
-- 触发器和函数（简化）
-- ============================================================================

-- 更新时间戳触发器函数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 为所有表添加更新时间戳触发器
DROP TRIGGER IF EXISTS update_accounts_updated_at ON accounts;
CREATE TRIGGER update_accounts_updated_at 
    BEFORE UPDATE ON accounts 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_companies_updated_at ON companies;
CREATE TRIGGER update_companies_updated_at 
    BEFORE UPDATE ON companies 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON users 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_projects_updated_at ON projects;
CREATE TRIGGER update_projects_updated_at 
    BEFORE UPDATE ON projects 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_roles_updated_at ON roles;
CREATE TRIGGER update_roles_updated_at 
    BEFORE UPDATE ON roles 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_project_users_updated_at ON project_users;
CREATE TRIGGER update_project_users_updated_at 
    BEFORE UPDATE ON project_users 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 用户统计更新函数（简化）
CREATE OR REPLACE FUNCTION update_account_user_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE accounts SET total_users = total_users + 1 WHERE account_id = NEW.account_id;
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE accounts SET total_users = total_users - 1 WHERE account_id = OLD.account_id;
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- 项目统计更新函数
CREATE OR REPLACE FUNCTION update_account_project_count()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE accounts SET total_projects = total_projects + 1 WHERE account_id = NEW.account_id;
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE accounts SET total_projects = total_projects - 1 WHERE account_id = OLD.account_id;
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- 创建统计触发器
DROP TRIGGER IF EXISTS trigger_update_account_user_count ON users;
CREATE TRIGGER trigger_update_account_user_count
    AFTER INSERT OR DELETE ON users
    FOR EACH ROW EXECUTE FUNCTION update_account_user_count();

DROP TRIGGER IF EXISTS trigger_update_account_project_count ON projects;
CREATE TRIGGER trigger_update_account_project_count
    AFTER INSERT OR DELETE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_account_project_count();

-- ============================================================================
-- 视图定义（简化）
-- ============================================================================

-- 用户详细信息视图
CREATE OR REPLACE VIEW user_details AS
SELECT 
    u.*,
    c.name as company_name_full,
    c.trade as company_trade,
    a.name as account_name,
    r.name as default_role_name,
    r.description as default_role_description
FROM users u
LEFT JOIN companies c ON u.company_id = c.company_id
LEFT JOIN accounts a ON u.account_id = a.account_id
LEFT JOIN roles r ON u.default_role_id = r.role_id;

-- 项目用户汇总视图
CREATE OR REPLACE VIEW project_user_summary AS
SELECT 
    pu.project_id,
    p.name as project_name,
    COUNT(*) as total_users,
    COUNT(*) FILTER (WHERE pu.status = 'active') as active_users,
    COUNT(*) FILTER (WHERE pu.status = 'pending') as pending_users,
    COUNT(DISTINCT pu.project_company_id) as companies_count,
    COUNT(*) FILTER (WHERE (pu.access_levels->>'projectAdmin')::boolean = true) as project_admins,
    COUNT(*) FILTER (WHERE (pu.access_levels->>'accountAdmin')::boolean = true) as account_admins
FROM project_users pu
JOIN projects p ON pu.project_id = p.project_id
GROUP BY pu.project_id, p.name;

-- 角色使用统计视图
CREATE OR REPLACE VIEW role_usage_stats AS
SELECT 
    r.*,
    COUNT(DISTINCT u.user_id) as users_with_default_role,
    COUNT(DISTINCT pu.user_id) as users_in_projects,
    COUNT(DISTINCT pu.project_id) as project_count
FROM roles r
LEFT JOIN users u ON r.role_id = u.default_role_id
LEFT JOIN project_users pu ON (
    pu.roles @> jsonb_build_array(jsonb_build_object('id', r.role_id)) OR
    pu.role_ids @> jsonb_build_array(r.role_id)
)
GROUP BY r.role_id;

-- ============================================================================
-- 注释说明
-- ============================================================================

COMMENT ON TABLE accounts IS '账户表 - 存储ACC账户的基本信息（简化版）';
COMMENT ON TABLE companies IS '公司表 - 存储ACC公司信息（简化版）';
COMMENT ON TABLE users IS '用户表 - 存储ACC账户用户信息，包含角色关联';
COMMENT ON TABLE projects IS '项目表 - 存储ACC项目信息';
COMMENT ON TABLE roles IS '角色表 - 存储ACC角色定义';
COMMENT ON TABLE project_users IS '项目用户关联表 - 存储用户在特定项目中的信息和权限';

COMMENT ON COLUMN users.default_role_id IS '用户的默认角色ID';
COMMENT ON COLUMN users.account_roles IS 'JSON格式的账户级角色列表';
COMMENT ON COLUMN project_users.access_levels IS 'JSON格式的访问级别配置';
COMMENT ON COLUMN project_users.role_ids IS 'JSON格式的项目级角色ID数组';
COMMENT ON COLUMN project_users.roles IS 'JSON格式的项目级角色详情数组';
COMMENT ON COLUMN project_users.products IS 'JSON格式的产品权限列表';
COMMENT ON COLUMN project_users.sync_status IS '同步状态: pending, synced, error';

-- ============================================================================
-- 优化说明
-- ============================================================================

/*
主要优化点：

✅ 删除的表：
- user_roles 表 - 角色关系直接存储在 users.account_roles 和 project_users.roles 中
- project_companies 表 - 通过用户的 company_id 间接管理公司关联

✅ 简化的字段：
- 删除了大量冗余的地址、联系信息字段
- 简化了枚举类型
- 统一使用ACC ID作为主键

✅ 角色管理优化：
- users.default_role_id - 用户的默认角色
- users.account_roles - 账户级角色列表（JSONB）
- project_users.roles - 项目级角色列表（JSONB）

✅ 保持的核心功能：
- 完整的用户、公司、项目管理
- 灵活的角色分配（账户级 + 项目级）
- 项目用户关联和权限管理
- 基本的统计和视图功能
*/
