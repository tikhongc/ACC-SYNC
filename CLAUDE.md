# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

ACC-SYNC is an Autodesk Construction Cloud (ACC) data synchronization system that syncs project data (files, folders, reviews, workflows) from ACC APIs to PostgreSQL databases. The system supports both file management sync and review/approval workflow sync with multi-database architecture (one database per project).

## Key Development Commands

### Database Operations

**Initialize Database Schema:**
```bash
# Create optimized database schema v2
python database_sql/init_v2_database.py

# Clean and recreate database for a project
python database_sql/clean_and_recreate.py <project_id>

# Create review system tables
python database_sql/create_review_tables.py
```

**Multi-Database Management:**
```bash
# Initialize multi-database environment
python database_sql/multi_database_cli.py init

# Create project-specific database
python database_sql/multi_database_cli.py create <project_id>

# List all project databases
python database_sql/multi_database_cli.py list
```

**Run Database Tests:**
```bash
# Test file sync to PostgreSQL
python api_modules/postgresql_sync_file/production_acc_sync_test.py

# Test review sync with enhanced features
python database_sql/test_enhanced_review_sync.py

# Test account sync
python database_sql/test_account_sync.py

# Test complete file approval workflow (comprehensive)
python test_complete_file_approval_workflow.py

# Test all review CDE function API modules
python test_api_functions.py
```

### Application Development

**Start Development Server:**
```bash
# Start both Flask backend and Vue frontend
python start_dev.py

# Start Flask backend only
python start_flask_only.py

# Direct Flask startup
python app.py
```

**Frontend Development:**
```bash
cd frontend
npm install
npm run dev      # Development server
npm run build    # Production build
```

## Architecture

### Multi-Database Architecture

The system uses **one PostgreSQL database per project** pattern managed by `ACCMultiDatabaseManager`:

- **Configuration:** `projects_config.yaml` stores project-to-database mappings
- **Naming Convention:** `acc_project_{normalized_project_id}` (e.g., `acc_project_1eea4119_3553_4167_b93d_3a3d5d07d33d`)
- **Connection Pooling:** Lazy-loaded connection pools with automatic cleanup for inactive databases
- **Admin Operations:** Performed on `postgres` database for CREATE/DROP DATABASE operations

### Review/Approval Workflow Architecture

Located in `api_modules/review_CDE_function/`:

**Enterprise File Approval Workflow System:**

The review module provides a complete enterprise-grade file approval workflow system with six core API modules:

1. **Approval Workflow Engine** (`approval_workflow_api_enhanced.py`)
   - Core workflow execution and state management
   - Three-tier permission validation (users, roles, companies)
   - Approval decision processing and workflow progression
   - API: `/api/approval/*`

2. **Review CRUD Management** (`review_crud_api.py`)
   - Complete review lifecycle management (create, read, update, delete)
   - Review status state machine (DRAFT → OPEN → CLOSED)
   - File version association management
   - API: `/api/reviews/*`

3. **Step Progress Management** (`step_progress_api.py`)
   - Step lifecycle management and status tracking
   - Step delegation and claim functionality
   - Approval history and audit trail
   - API: `/api/step-progress/*`

4. **File Approval Status** (`approval_status_api.py`)
   - Individual and batch file approval operations
   - File-level approval status tracking (PENDING, APPROVED, REJECTED)
   - Complete approval history audit
   - API: `/api/approval-status/*`

5. **Candidates Management** (`candidates_api.py`)
   - Dynamic approval step candidate configuration
   - User/role/company-based approval assignments
   - Project-wide candidate availability management
   - API: `/api/candidates/*`

6. **Module Integration** (`review_module_integration.py`)
   - Unified Flask Blueprint registration
   - Cross-module coordination and health monitoring
   - API: `/api/review-module/*`

**Core Workflow Concepts:**

- **Static Configuration** (`review_step_candidates`): Template-driven candidate assignments
- **Dynamic History** (`review_progress`): Runtime step execution tracking
- **Permission Hierarchy**: User → Role → Company level authorization
- **Flexible Approval Options**: Custom approval labels mapped to core APPROVED/REJECTED values
- **Complete Audit Trail**: Every action, decision, and state change tracked

**Workflow State Machine:**
```
Review: DRAFT → OPEN → CLOSED/CANCELLED/ARCHIVED
Step: PENDING → CLAIMED → COMPLETED/REJECTED/SENT_BACK
File: PENDING → APPROVED/REJECTED
```

### Core Database Schema (V2 Optimized)

Located in `database_sql/optimized_schema_v2.sql`:

**Key Tables:**
- `projects` - Project metadata with sync status tracking
- `folders` - Folder hierarchy with `last_modified_time_rollup` for smart skip optimization
- `files` - File metadata (version-agnostic)
- `file_versions` - All file versions with detailed metadata
- `custom_attribute_definitions` - Custom attribute schemas per project
- `custom_attribute_values` - Custom attribute values for files
- `sync_tasks` - Sync operation tracking with performance stats

**Critical Optimization Fields:**
- `folders.last_modified_time_rollup` - Enables smart branch skipping in incremental sync
- `projects.last_sync_time` - Reference point for incremental sync
- `sync_tasks.performance_stats` - JSONB field tracking optimization efficiency

### File Sync Architecture

Located in `api_modules/postgresql_sync_file/`:

**Three-Layer Service Pattern:**

1. **Routes Layer** (`postgresql_sync_routes.py`)
   - HTTP endpoint: `/api/postgresql-sync/project/{project_id}/sync`
   - Parameters: `sync_type` (full_sync/incremental_sync), `performance_mode`, `max_depth`
   - Response: Standardized JSON with task UUID and performance stats

2. **Service Layer** (`postgresql_sync_service.py`)
   - `PostgreSQLSyncService` orchestrates sync operations
   - Handles top-level rollup check for project-level skip optimization
   - Manages task lifecycle and performance tracking

3. **Manager Layer** (`postgresql_sync_manager.py`)
   - `OptimizedPostgreSQLSyncManager` implements five-layer optimization strategy:
     1. Smart branch skipping (rollup-based)
     2. Batch API calls (concurrent with semaphore control)
     3. File-level timestamp comparison
     4. Batch database operations (PostgreSQL COPY + UPSERT)
     5. Memory management with garbage collection

**Data Flow:**
```
ACC API → BFS Traversal → Batch API Calls → Data Transformation → Batch DB Operations
                ↓
          Smart Skip Checks (using rollup timestamps)
```

### Review Sync Architecture

Located in `api_modules/postgresql_review_sync/`:

**Enhanced Sync Manager** (`review_sync_manager_enhanced.py`):
- Async/await pattern with `aiohttp` for parallel API calls
- Redis caching layer for API responses (optional)
- Batch UPSERT operations using PostgreSQL `ON CONFLICT`
- Circuit breaker pattern for API resilience
- Performance monitoring with bottleneck analysis

**Review Schema** (in `database_sql/review_system_schema.sql`):
- `workflows` / `workflow_templates` - Approval workflow definitions
- `reviews` - Review instances linked to files
- `review_file_versions` - Files under review
- `review_progress` - Step-by-step progress tracking
- `user_members` - Cached project users
- `review_step_candidates` - User/role/company candidates for review steps
- `workflow_notes` - Workflow annotation and comments
- `file_approval_history` - File approval audit trail

**Key Features:**
- 4x faster than original implementation (async + batch operations)
- 10x reduction in database queries (batch UPSERT)
- Optional Redis caching for 60%+ cache hit rates
- Configurable performance modes: DEV, PROD, TEST (in `sync_config.py`)

### Data Access Layer

**Optimized PostgreSQL DAL** (`database_sql/optimized_data_access.py`):
- Async connection pooling with `asyncpg`
- Batch operations: `batch_upsert_folders`, `batch_upsert_files`, `batch_upsert_file_versions`
- Incremental sync support: `get_folders_for_smart_skip_check`, `get_last_sync_time`
- Project lifecycle: `ensure_project_exists`, `update_project_sync_status`

**Review Data Access** (`database_sql/review_data_access_enhanced.py`):
- PostgreSQL `ON CONFLICT` for efficient UPSERT
- Batch operations for workflows, reviews, file versions, progress steps
- Connection reuse patterns for performance

## Important Implementation Details

### BFS Traversal Strategies

The file sync implements **layered BFS processing** (recommended for 50K-500K files):

1. Process folders level-by-level (depth 0, 1, 2, ...)
2. Batch API calls for all folders at current level
3. Insert current level to database before moving to next level
4. Maintains parent-child referential integrity naturally

**Alternatives:**
- Memory BFS: Store all data in memory then bulk insert (good for <50K files)
- Streaming BFS: Insert immediately as items are discovered (for >100K files)

### Incremental Sync Optimization

**Five-Layer Strategy:**

1. **Top-level Rollup Check** - If max rollup time ≤ last sync time, skip entire project
2. **Smart Branch Filtering** - Skip folder branches where rollup ≤ last sync time
3. **File Timestamp Comparison** - Only process files with lastModifiedTime > last sync time
4. **Batch API Operations** - Concurrent folder content fetching with semaphore
5. **Batch DB Operations** - Single transaction for all changes

**Result:** 70-100% optimization efficiency, 80%+ API call reduction

### Time Zone Handling

All datetime fields use `TIMESTAMP WITH TIME ZONE` in PostgreSQL. The sync manager includes China timezone conversion utilities:

- `_convert_to_china_timezone(dt)` - Convert datetime to Asia/Shanghai
- `_parse_datetime_to_china(datetime_str)` - Parse and convert to China TZ

Ensure consistent timezone handling across ACC API (UTC) and local database storage.

### Performance Modes

Three predefined configurations in file sync:

- **Standard:** batch_size=100, max_workers=8, api_delay=0.02s
- **High Performance:** batch_size=200, max_workers=16, api_delay=0.01s
- **Memory Optimized:** batch_size=50, max_workers=4, api_delay=0.05s

Review sync configurations in `api_modules/postgresql_review_sync/sync_config.py`:
- `DEV_CONFIG`, `PROD_CONFIG`, `TEST_CONFIG`

## Common Patterns

### Creating a Sync Task

```python
from api_modules.postgresql_sync_file.postgresql_sync_service import PostgreSQLSyncService

service = PostgreSQLSyncService()
result = await service.unified_sync(
    project_id="b.xxx",
    sync_type="incremental_sync",
    performance_mode="standard",
    max_depth=10,
    include_custom_attributes=True
)
# Returns: task_uuid, status, stats, performance_stats
```

### Working with Multi-Database Manager

```python
from database_sql.multi_database_manager import ACCMultiDatabaseManager

manager = ACCMultiDatabaseManager()
pool = await manager.get_project_database(project_id)

async with pool.acquire() as conn:
    result = await conn.fetch("SELECT * FROM folders LIMIT 10")
```

### Batch UPSERT Pattern

```python
from database_sql.review_data_access_enhanced import EnhancedReviewDataAccess

da = EnhancedReviewDataAccess()
inserted, updated = await da.batch_upsert_workflows(workflows_list)
```

## Environment Configuration

**Database Connection:**
Configuration typically in `projects_config.yaml`:
```yaml
global:
  database:
    host: localhost
    port: 5432
    user: neondb_owner
    password: <password>
    admin_database: postgres
```

**Flask Configuration:**
Main settings in `config.py`:
- OAuth credentials: `CLIENT_ID`, `CLIENT_SECRET`, `CALLBACK_URL`
- ACC API scopes and endpoints
- Token refresh configuration

**PostgreSQL Requirements:**
- PostgreSQL 12+ (14+ recommended)
- Extensions: `uuid-ossp`, `btree_gin`
- Minimum 4GB RAM, 8GB+ recommended for large projects

## Testing Patterns

### File Sync Testing

```python
# Test incremental sync
python api_modules/postgresql_sync_file/production_acc_sync_test.py

# Force incremental test
python api_modules/postgresql_sync_file/force_incremental_test.py

# Check folder structure
python api_modules/postgresql_sync_file/check_folder_structure.py
```

### Review Sync Testing

```python
# Enhanced review sync test (with async + caching)
python database_sql/test_enhanced_review_sync.py

# Simple review sync test
python database_sql/simple_review_sync_test.py

# Test specific review workflow
python test_approval_workflow_e2e.py
```

### Review Workflow API Testing

```bash
# Comprehensive end-to-end file approval workflow test
python test_complete_file_approval_workflow.py

# Test all API modules in review_CDE_function
python test_api_functions.py

# Simple approval test for basic functionality
python simple_approval_test.py

# Batch file approval workflow test
python test_batch_file_approval.py
```

## Key Constraints and Gotchas

1. **Project ID Format:** ACC project IDs start with `b.` prefix (e.g., `b.1eea4119-...`). Database names normalize this to `acc_project_1eea4119_...`

2. **Rollup Time Critical:** The `last_modified_time_rollup` field on folders MUST be accurate for incremental sync optimization to work. Full sync recalculates these values.

3. **File vs File Version:** The `files` table stores file metadata (stable), while `file_versions` stores version-specific data (storage URN, size, etc.). Use the relationship correctly.

4. **Custom Attributes:** Are folder-scoped in ACC. The definitions are per-folder, and files inherit applicable attributes based on their location.

5. **Async Context Required:** Review sync enhanced features require async context (use `asyncio.run()` or event loop)

6. **Connection Pool Management:** Each project database has its own connection pool. Inactive pools are cleaned up after 2 hours by default.

7. **API Rate Limiting:** ACC APIs have rate limits. Use `api_delay` parameter to throttle requests. Default 0.02s works well for most cases.

8. **Unicode Support:** All review workflow API modules require UTF-8 encoding declaration (`# -*- coding: utf-8 -*-`) for proper Chinese character support.

9. **Review Workflow States:** Review workflow follows strict state machines. Only certain transitions are allowed (e.g., DRAFT → OPEN, PENDING → CLAIMED).

10. **Permission Validation:** Review workflow uses three-tier permission checking (user → role → company). Ensure proper user membership data for accurate permission validation.

11. **File Approval Granularity:** Individual files within a review can have different approval statuses. Batch operations are available but maintain individual file tracking.

12. **Workflow Template Integrity:** Workflow step definitions must use valid step types (REVIEWER, APPROVER, INITIATOR, FINAL). Custom approval options map to core APPROVED/REJECTED values.

## Documentation References

- **File Sync:** `api_modules/postgresql_sync_file/POSTGRESQL_OPTIMIZED_SYNC_SOLUTION.md`
- **Review Sync:** `api_modules/postgresql_review_sync/README_ENHANCED.md`
- **Review Module:** `database_sql/ACC_REVIEW_MODULE_README.md`
- **Review Workflow System:** `文件审批工作流系统功能详解.md` (Chinese comprehensive guide)
- **Database Schema:** `database_sql/optimized_schema_v2.sql`
- **Migration Guides:** `database_sql/MIGRATION_GUIDE_file_versions.md`

## When Working on New Features

1. **Adding New Sync Entity:** Update schema in `optimized_schema_v2.sql`, add DAL methods in `optimized_data_access.py`, implement sync logic in appropriate manager

2. **Optimizing Sync Performance:** Focus on the five-layer optimization strategy. Most gains come from smart skip logic (Layer 1-2) and batch operations (Layer 3-4)

3. **Database Changes:** Always use migrations for schema changes. Test with `clean_and_recreate.py` for development, but production needs proper migration scripts

4. **API Integration:** Follow the Routes → Service → Manager pattern. Keep HTTP concerns in routes, business logic in service, data operations in manager

5. **Performance Testing:** Use `sync_tasks` table to track performance stats. Monitor `optimization_efficiency` metric for incremental syncs (target >70%)

## Review Workflow Development Guidelines

### Working with Review Workflow APIs

1. **Module Structure:** Each API module follows the pattern:
   - `*_api.py` - Core manager class with business logic
   - Blueprint registration in `review_module_integration.py`
   - UTF-8 encoding declaration for Chinese support

2. **Testing Strategy:**
   - Use `test_complete_file_approval_workflow.py` for end-to-end testing
   - Use `test_api_functions.py` for individual module validation
   - Create test workflows with existing database projects/users/files
   - Validate both success paths and error handling

3. **Database Integration:**
   - All workflow APIs use direct PostgreSQL connections
   - JSONB columns for flexible data storage (workflow steps, approval options)
   - Proper enum type validation (step types, approval statuses)
   - Maintain referential integrity across workflow tables

4. **Permission Model:**
   ```python
   # Three-tier permission checking
   def _check_comprehensive_permissions(user_id, step_candidates):
       # 1. Direct user permission
       if user_id in step_candidates.get('users', []):
           return True
       # 2. Role-based permission
       if user_roles.intersection(step_candidates.get('roles', [])):
           return True
       # 3. Company-based permission
       if user_companies.intersection(step_candidates.get('companies', [])):
           return True
       return False
   ```

5. **State Management:**
   - Review states: `DRAFT`, `OPEN`, `CLOSED`, `CANCELLED`, `ARCHIVED`
   - Step states: `PENDING`, `CLAIMED`, `COMPLETED`, `REJECTED`, `SENT_BACK`
   - File approval states: `PENDING`, `APPROVED`, `REJECTED`
   - Always validate state transitions before updates

6. **Error Handling Best Practices:**
   - Graceful degradation for API format differences
   - Comprehensive logging for audit trails
   - Transaction rollback on critical failures
   - User-friendly error messages with technical details in logs

### Common Workflow Patterns

**Creating a Complete Workflow Test:**
```python
# 1. Create workflow template with valid step types
workflow_steps = [
    {"id": "initial_review", "type": "REVIEWER", "order": 1},
    {"id": "final_approval", "type": "APPROVER", "order": 2}
]

# 2. Create review with existing files
review_data = {
    'project_id': project_id,
    'workflow_id': workflow_id,
    'file_versions': existing_files
}

# 3. Execute workflow progression
claim_step() → approve_files() → submit_decision() → progress_workflow()
```

**Unicode and Encoding:**
```python
# Required at top of all API files
# -*- coding: utf-8 -*-
import os
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'
```

**Database Column Mapping:**
```python
# Common mapping issues to watch for:
'file_urn' → 'file_version_urn'  # Correct column name
'step_type' → valid enum values only (REVIEWER, APPROVER, INITIATOR, FINAL)
'status' → proper state machine values
```
