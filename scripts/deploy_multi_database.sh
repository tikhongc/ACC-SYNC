#!/bin/bash
# ACC 多數據庫部署腳本
# 用於部署和管理每項目一個數據庫的架構

set -e

# 配置
DB_HOST="localhost"
DB_PORT="5432"
DB_USER="neondb_owner"
DB_PASSWORD="npg_a2nxljG8LOSP"
ADMIN_DB="postgres"
SCHEMA_FILE="database_sql/optimized_schema_v2.sql"
CONFIG_FILE="projects_config.yaml"

# 顏色輸出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日誌函數
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 檢查依賴
check_dependencies() {
    log_info "Checking dependencies..."
    
    if ! command -v psql &> /dev/null; then
        log_error "psql is not installed. Please install PostgreSQL client."
        exit 1
    fi
    
    if ! command -v python3 &> /dev/null; then
        log_error "python3 is not installed."
        exit 1
    fi
    
    if [ ! -f "$SCHEMA_FILE" ]; then
        log_error "Schema file not found: $SCHEMA_FILE"
        exit 1
    fi
    
    log_success "All dependencies are available"
}

# 測試數據庫連接
test_connection() {
    log_info "Testing database connection..."
    
    if PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$ADMIN_DB" -c "SELECT 1;" &> /dev/null; then
        log_success "Database connection successful"
    else
        log_error "Failed to connect to database"
        exit 1
    fi
}

# 創建項目數據庫
create_project_database() {
    local project_id="$1"
    local db_name="acc_project_$(echo "$project_id" | sed 's/[b\.]//g' | sed 's/-/_/g')"
    
    log_info "Creating database for project: $project_id"
    log_info "Database name: $db_name"
    
    # 檢查數據庫是否已存在
    if PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$ADMIN_DB" -lqt | cut -d \| -f 1 | grep -qw "$db_name"; then
        log_warning "Database $db_name already exists, skipping creation"
        return 0
    fi
    
    # 創建數據庫
    if PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$ADMIN_DB" -c "CREATE DATABASE \"$db_name\";" &> /dev/null; then
        log_success "Created database: $db_name"
    else
        log_error "Failed to create database: $db_name"
        return 1
    fi
    
    # 初始化架構
    if PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$db_name" -f "$SCHEMA_FILE" &> /dev/null; then
        log_success "Initialized schema for database: $db_name"
    else
        log_error "Failed to initialize schema for database: $db_name"
        return 1
    fi
    
    return 0
}

# 從配置文件批量創建數據庫
batch_create_from_config() {
    log_info "Creating databases from configuration file: $CONFIG_FILE"
    
    if [ ! -f "$CONFIG_FILE" ]; then
        log_error "Configuration file not found: $CONFIG_FILE"
        exit 1
    fi
    
    # 使用 Python 解析 YAML 並提取項目 ID
    project_ids=$(python3 -c "
import yaml
with open('$CONFIG_FILE', 'r') as f:
    config = yaml.safe_load(f)
    projects = config.get('projects', {})
    for project_id in projects.keys():
        print(project_id)
")
    
    if [ -z "$project_ids" ]; then
        log_warning "No projects found in configuration file"
        return 0
    fi
    
    local success_count=0
    local total_count=0
    
    while IFS= read -r project_id; do
        if [ -n "$project_id" ]; then
            total_count=$((total_count + 1))
            if create_project_database "$project_id"; then
                success_count=$((success_count + 1))
            fi
        fi
    done <<< "$project_ids"
    
    log_success "Created $success_count out of $total_count project databases"
}

# 列出所有項目數據庫
list_project_databases() {
    log_info "Listing all project databases..."
    
    PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$ADMIN_DB" -c "
        SELECT 
            datname as database_name,
            pg_size_pretty(pg_database_size(datname)) as size,
            (SELECT count(*) FROM pg_stat_activity WHERE datname = d.datname) as connections
        FROM pg_database d 
        WHERE datname LIKE 'acc_project_%' 
        ORDER BY datname;
    "
}

# 刪除項目數據庫
delete_project_database() {
    local project_id="$1"
    local db_name="acc_project_$(echo "$project_id" | sed 's/[b\.]//g' | sed 's/-/_/g')"
    
    log_warning "Deleting database for project: $project_id"
    log_warning "Database name: $db_name"
    
    # 確認操作
    read -p "Are you sure you want to delete database '$db_name'? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        log_info "Operation cancelled"
        return 0
    fi
    
    # 終止所有連接
    PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$ADMIN_DB" -c "
        SELECT pg_terminate_backend(pid)
        FROM pg_stat_activity
        WHERE datname = '$db_name' AND pid <> pg_backend_pid();
    " &> /dev/null
    
    # 刪除數據庫
    if PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$ADMIN_DB" -c "DROP DATABASE IF EXISTS \"$db_name\";" &> /dev/null; then
        log_success "Deleted database: $db_name"
    else
        log_error "Failed to delete database: $db_name"
        return 1
    fi
}

# 清理不活躍的數據庫
cleanup_inactive_databases() {
    log_info "Cleaning up inactive databases..."
    
    # 獲取沒有活躍連接的項目數據庫
    inactive_dbs=$(PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$ADMIN_DB" -t -c "
        SELECT d.datname 
        FROM pg_database d 
        WHERE d.datname LIKE 'acc_project_%' 
        AND NOT EXISTS (
            SELECT 1 FROM pg_stat_activity a 
            WHERE a.datname = d.datname AND a.state = 'active'
        );
    " | tr -d ' ')
    
    if [ -z "$inactive_dbs" ]; then
        log_info "No inactive databases found"
        return 0
    fi
    
    log_info "Found inactive databases:"
    echo "$inactive_dbs"
    
    read -p "Do you want to archive these databases? (yes/no): " confirm
    if [ "$confirm" = "yes" ]; then
        # 這裡可以添加歸檔邏輯，比如備份到另一個位置
        log_info "Database archiving would be implemented here"
    fi
}

# 備份項目數據庫
backup_project_database() {
    local project_id="$1"
    local db_name="acc_project_$(echo "$project_id" | sed 's/[b\.]//g' | sed 's/-/_/g')"
    local backup_dir="backups"
    local timestamp=$(date +"%Y%m%d_%H%M%S")
    local backup_file="$backup_dir/${db_name}_${timestamp}.sql"
    
    log_info "Backing up database: $db_name"
    
    # 創建備份目錄
    mkdir -p "$backup_dir"
    
    # 執行備份
    if PGPASSWORD="$DB_PASSWORD" pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$db_name" > "$backup_file"; then
        log_success "Backup created: $backup_file"
        
        # 壓縮備份文件
        if gzip "$backup_file"; then
            log_success "Backup compressed: ${backup_file}.gz"
        fi
    else
        log_error "Failed to backup database: $db_name"
        return 1
    fi
}

# 顯示幫助信息
show_help() {
    echo "ACC Multi-Database Deployment Script"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  check           Check dependencies and database connection"
    echo "  create PROJECT_ID   Create database for specific project"
    echo "  batch-create    Create databases for all projects in config file"
    echo "  list            List all project databases"
    echo "  delete PROJECT_ID   Delete database for specific project"
    echo "  cleanup         Clean up inactive databases"
    echo "  backup PROJECT_ID   Backup specific project database"
    echo "  help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 check"
    echo "  $0 create b.1eea4119-3553-4167-b93d-3a3d5d07d33d"
    echo "  $0 batch-create"
    echo "  $0 list"
    echo "  $0 backup b.1eea4119-3553-4167-b93d-3a3d5d07d33d"
}

# 主函數
main() {
    case "$1" in
        "check")
            check_dependencies
            test_connection
            ;;
        "create")
            if [ -z "$2" ]; then
                log_error "Project ID is required"
                echo "Usage: $0 create PROJECT_ID"
                exit 1
            fi
            check_dependencies
            test_connection
            create_project_database "$2"
            ;;
        "batch-create")
            check_dependencies
            test_connection
            batch_create_from_config
            ;;
        "list")
            check_dependencies
            test_connection
            list_project_databases
            ;;
        "delete")
            if [ -z "$2" ]; then
                log_error "Project ID is required"
                echo "Usage: $0 delete PROJECT_ID"
                exit 1
            fi
            check_dependencies
            test_connection
            delete_project_database "$2"
            ;;
        "cleanup")
            check_dependencies
            test_connection
            cleanup_inactive_databases
            ;;
        "backup")
            if [ -z "$2" ]; then
                log_error "Project ID is required"
                echo "Usage: $0 backup PROJECT_ID"
                exit 1
            fi
            check_dependencies
            test_connection
            backup_project_database "$2"
            ;;
        "help"|"--help"|"-h"|"")
            show_help
            ;;
        *)
            log_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# 執行主函數
main "$@"
