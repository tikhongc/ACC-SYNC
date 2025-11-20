-- ================================================================
-- Transmittal Module Database Schema
-- ================================================================
-- Purpose: Independent transmittal (document transmission) management system
-- Architecture: Multi-database (one database per project)
-- Created: 2025-01-18
-- ================================================================

-- ================================================================
-- Main Transmittal Table
-- ================================================================
-- Stores the main transmittal metadata and header information
-- One transmittal can contain multiple documents and recipients
-- ================================================================

CREATE TABLE IF NOT EXISTS transmittals_workflow_transmittals (
    -- Primary identification
    id UUID PRIMARY KEY,

    -- Autodesk identifiers
    bim360_account_id UUID NOT NULL,
    bim360_project_id UUID NOT NULL,

    -- Transmittal sequence (auto-incrementing within project)
    sequence_id INTEGER NOT NULL,

    -- Transmittal content
    title VARCHAR(500) NOT NULL,
    message TEXT,  -- Optional message/description for the transmittal
    status INTEGER NOT NULL,  -- Status code (e.g., 2 = SENT/ACTIVE)
    docs_count INTEGER NOT NULL DEFAULT 0,

    -- Creator information
    create_user_id UUID NOT NULL,
    create_user_name VARCHAR(255) NOT NULL,
    create_user_company_id UUID,
    create_user_company_name VARCHAR(255),

    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,

    -- Ensure unique sequence per project
    CONSTRAINT uq_transmittal_sequence UNIQUE (bim360_project_id, sequence_id)
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_transmittals_project
    ON transmittals_workflow_transmittals(bim360_project_id, sequence_id);

CREATE INDEX IF NOT EXISTS idx_transmittals_account_project
    ON transmittals_workflow_transmittals(bim360_account_id, bim360_project_id);

CREATE INDEX IF NOT EXISTS idx_transmittals_status
    ON transmittals_workflow_transmittals(status);

CREATE INDEX IF NOT EXISTS idx_transmittals_created
    ON transmittals_workflow_transmittals(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_transmittals_creator
    ON transmittals_workflow_transmittals(create_user_id);

-- Table comments
COMMENT ON TABLE transmittals_workflow_transmittals IS 'Main transmittal table storing document transmission records';
COMMENT ON COLUMN transmittals_workflow_transmittals.sequence_id IS 'Auto-incrementing transmittal number within project';
COMMENT ON COLUMN transmittals_workflow_transmittals.status IS 'Transmittal status code (e.g., 1=DRAFT, 2=SENT, 3=CANCELLED)';
COMMENT ON COLUMN transmittals_workflow_transmittals.docs_count IS 'Number of documents attached to this transmittal';


-- ================================================================
-- Document Association Table
-- ================================================================
-- Links documents/files to transmittals (many-to-many relationship)
-- Same document version can appear in multiple transmittals
-- ================================================================

CREATE TABLE IF NOT EXISTS transmittals_transmittal_documents (
    -- Primary identification
    id UUID PRIMARY KEY,

    -- Foreign key to main transmittal table
    workflow_transmittal_id UUID NOT NULL,

    -- Autodesk identifiers
    bim360_account_id UUID NOT NULL,
    bim360_project_id UUID NOT NULL,

    -- Document/file information
    urn VARCHAR(500) NOT NULL,  -- File version URN (full ACC format)
    file_name VARCHAR(500) NOT NULL,
    version_number INTEGER NOT NULL,
    revision_number INTEGER NOT NULL,
    parent_folder_urn VARCHAR(255) NOT NULL,

    -- Last modification tracking
    last_modified_time TIMESTAMP WITH TIME ZONE NOT NULL,
    last_modified_user_id VARCHAR(50) NOT NULL,
    last_modified_user_name VARCHAR(255) NOT NULL,

    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,

    -- Foreign key constraint with cascade delete
    CONSTRAINT fk_documents_transmittal
        FOREIGN KEY (workflow_transmittal_id)
        REFERENCES transmittals_workflow_transmittals(id)
        ON DELETE CASCADE,

    -- Prevent duplicate document versions in same transmittal
    CONSTRAINT uq_transmittal_document_version
        UNIQUE (workflow_transmittal_id, urn, version_number)
);

-- Indexes for joins and lookups
CREATE INDEX IF NOT EXISTS idx_docs_transmittal
    ON transmittals_transmittal_documents(workflow_transmittal_id);

CREATE INDEX IF NOT EXISTS idx_docs_project_urn
    ON transmittals_transmittal_documents(bim360_project_id, urn);

CREATE INDEX IF NOT EXISTS idx_docs_filename
    ON transmittals_transmittal_documents(file_name);

CREATE INDEX IF NOT EXISTS idx_docs_modified
    ON transmittals_transmittal_documents(last_modified_time DESC);

-- Table comments
COMMENT ON TABLE transmittals_transmittal_documents IS 'Association table linking documents to transmittals';
COMMENT ON COLUMN transmittals_transmittal_documents.urn IS 'File version URN (shortened format from ACC API)';
COMMENT ON COLUMN transmittals_transmittal_documents.version_number IS 'File version number';
COMMENT ON COLUMN transmittals_transmittal_documents.revision_number IS 'File revision number (usually matches version)';


-- ================================================================
-- Recipients Table (Project Members)
-- ================================================================
-- Tracks project members who receive transmittals
-- Includes view/download tracking for recipient engagement
-- ================================================================

CREATE TABLE IF NOT EXISTS transmittals_transmittal_recipients (
    -- Primary identification
    id UUID PRIMARY KEY,

    -- Foreign key to main transmittal table
    workflow_transmittal_id UUID NOT NULL,

    -- Autodesk identifiers
    bim360_account_id UUID NOT NULL,
    bim360_project_id UUID NOT NULL,

    -- Recipient user information
    user_id UUID NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    company_name VARCHAR(255),

    -- Engagement tracking
    viewed_at TIMESTAMP WITH TIME ZONE,      -- NULL = not viewed yet
    downloaded_at TIMESTAMP WITH TIME ZONE,  -- NULL = not downloaded yet

    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,

    -- Foreign key constraint with cascade delete
    CONSTRAINT fk_recipients_transmittal
        FOREIGN KEY (workflow_transmittal_id)
        REFERENCES transmittals_workflow_transmittals(id)
        ON DELETE CASCADE,

    -- Prevent duplicate recipients per transmittal
    CONSTRAINT uq_transmittal_recipient
        UNIQUE (workflow_transmittal_id, user_id)
);

-- Indexes for queries and tracking
CREATE INDEX IF NOT EXISTS idx_recipients_transmittal
    ON transmittals_transmittal_recipients(workflow_transmittal_id);

CREATE INDEX IF NOT EXISTS idx_recipients_user
    ON transmittals_transmittal_recipients(user_id);

CREATE INDEX IF NOT EXISTS idx_recipients_email
    ON transmittals_transmittal_recipients(email);

CREATE INDEX IF NOT EXISTS idx_recipients_viewed
    ON transmittals_transmittal_recipients(viewed_at)
    WHERE viewed_at IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_recipients_downloaded
    ON transmittals_transmittal_recipients(downloaded_at)
    WHERE downloaded_at IS NOT NULL;

-- Table comments
COMMENT ON TABLE transmittals_transmittal_recipients IS 'Project member recipients of transmittals with engagement tracking';
COMMENT ON COLUMN transmittals_transmittal_recipients.viewed_at IS 'Timestamp when recipient viewed the transmittal (NULL = not viewed)';
COMMENT ON COLUMN transmittals_transmittal_recipients.downloaded_at IS 'Timestamp when recipient downloaded documents (NULL = not downloaded)';


-- ================================================================
-- Non-Member Recipients Table (External Users)
-- ================================================================
-- Stores external recipients (not project members)
-- Typically receive transmittals via email with limited access
-- ================================================================

CREATE TABLE IF NOT EXISTS transmittals_transmittal_non_members (
    -- Primary identification
    id UUID PRIMARY KEY,

    -- Foreign key to main transmittal table
    workflow_transmittal_id UUID NOT NULL,

    -- Autodesk identifiers
    bim360_account_id UUID NOT NULL,
    bim360_project_id UUID NOT NULL,

    -- External user information
    email VARCHAR(255) NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    company_name VARCHAR(255),
    role VARCHAR(255),  -- Business role/title

    -- Engagement tracking
    viewed_at TIMESTAMP WITH TIME ZONE,      -- NULL = not viewed yet
    downloaded_at TIMESTAMP WITH TIME ZONE,  -- NULL = not downloaded yet

    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,

    -- Foreign key constraint with cascade delete
    CONSTRAINT fk_non_members_transmittal
        FOREIGN KEY (workflow_transmittal_id)
        REFERENCES transmittals_workflow_transmittals(id)
        ON DELETE CASCADE,

    -- Prevent duplicate external recipients per transmittal
    CONSTRAINT uq_transmittal_non_member
        UNIQUE (workflow_transmittal_id, email)
);

-- Indexes for queries
CREATE INDEX IF NOT EXISTS idx_non_members_transmittal
    ON transmittals_transmittal_non_members(workflow_transmittal_id);

CREATE INDEX IF NOT EXISTS idx_non_members_email
    ON transmittals_transmittal_non_members(email);

CREATE INDEX IF NOT EXISTS idx_non_members_viewed
    ON transmittals_transmittal_non_members(viewed_at)
    WHERE viewed_at IS NOT NULL;

-- Table comments
COMMENT ON TABLE transmittals_transmittal_non_members IS 'External (non-project member) recipients of transmittals';
COMMENT ON COLUMN transmittals_transmittal_non_members.email IS 'Email address for external recipient (required for access)';
COMMENT ON COLUMN transmittals_transmittal_non_members.role IS 'Business role/title of external recipient';


-- ================================================================
-- Helper Functions and Views (Optional)
-- ================================================================

-- View: Transmittal Summary with Document Count
CREATE OR REPLACE VIEW v_transmittal_summary AS
SELECT
    t.id,
    t.bim360_project_id,
    t.sequence_id,
    t.title,
    t.status,
    t.create_user_name,
    t.create_user_company_name,
    t.created_at,
    t.updated_at,
    COUNT(DISTINCT d.id) AS actual_docs_count,
    COUNT(DISTINCT r.id) AS recipient_count,
    COUNT(DISTINCT n.id) AS non_member_count,
    COUNT(DISTINCT CASE WHEN r.viewed_at IS NOT NULL THEN r.id END) AS viewed_count,
    COUNT(DISTINCT CASE WHEN r.downloaded_at IS NOT NULL THEN r.id END) AS downloaded_count
FROM transmittals_workflow_transmittals t
LEFT JOIN transmittals_transmittal_documents d ON t.id = d.workflow_transmittal_id
LEFT JOIN transmittals_transmittal_recipients r ON t.id = r.workflow_transmittal_id
LEFT JOIN transmittals_transmittal_non_members n ON t.id = n.workflow_transmittal_id
GROUP BY t.id, t.bim360_project_id, t.sequence_id, t.title, t.status,
         t.create_user_name, t.create_user_company_name, t.created_at, t.updated_at;

COMMENT ON VIEW v_transmittal_summary IS 'Summary view of transmittals with document and recipient counts';


-- View: Recipient Engagement Report
CREATE OR REPLACE VIEW v_recipient_engagement AS
SELECT
    t.id AS transmittal_id,
    t.sequence_id,
    t.title,
    r.user_name,
    r.email,
    r.company_name,
    r.created_at AS recipient_added_at,
    r.viewed_at,
    r.downloaded_at,
    CASE
        WHEN r.downloaded_at IS NOT NULL THEN 'Downloaded'
        WHEN r.viewed_at IS NOT NULL THEN 'Viewed'
        ELSE 'Not Viewed'
    END AS engagement_status,
    EXTRACT(EPOCH FROM (r.viewed_at - t.created_at)) / 3600 AS hours_to_view,
    EXTRACT(EPOCH FROM (r.downloaded_at - r.viewed_at)) / 3600 AS hours_to_download
FROM transmittals_workflow_transmittals t
JOIN transmittals_transmittal_recipients r ON t.id = r.workflow_transmittal_id;

COMMENT ON VIEW v_recipient_engagement IS 'Recipient engagement tracking with time-to-view and time-to-download metrics';


-- ================================================================
-- Verification Query
-- ================================================================
-- Run this query after table creation to verify structure
-- ================================================================

/*
SELECT
    schemaname,
    tablename,
    tableowner
FROM pg_tables
WHERE tablename LIKE 'transmittals_%'
ORDER BY tablename;

SELECT
    table_name,
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name LIKE 'transmittals_%'
ORDER BY table_name, ordinal_position;
*/
