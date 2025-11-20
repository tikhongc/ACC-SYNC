@echo off
REM ACC 多數據庫部署腳本 - Windows 版本
REM 用於部署和管理每項目一個數據庫的架構

setlocal enabledelayedexpansion

REM 配置
set DB_HOST=localhost
set DB_PORT=5432
set DB_USER=neondb_owner
set DB_PASSWORD=npg_a2nxljG8LOSP
set ADMIN_DB=postgres
set SCHEMA_FILE=database_sql\optimized_schema_v2.sql
set CONFIG_FILE=projects_config.yaml

REM 顏色輸出（Windows 10+ 支持 ANSI 顏色）
set RED=[31m
set GREEN=[32m
set YELLOW=[33m
set BLUE=[34m
set NC=[0m

REM 日誌函數
:log_info
echo %BLUE%[INFO]%NC% %~1
goto :eof

:log_success
echo %GREEN%[SUCCESS]%NC% %~1
goto :eof

:log_warning
echo %YELLOW%[WARNING]%NC% %~1
goto :eof

:log_error
echo %RED%[ERROR]%NC% %~1
goto :eof

REM 檢查依賴
:check_dependencies
call :log_info "Checking dependencies..."

where psql >nul 2>&1
if errorlevel 1 (
    call :log_error "psql is not installed. Please install PostgreSQL client."
    exit /b 1
)

where python >nul 2>&1
if errorlevel 1 (
    call :log_error "python is not installed."
    exit /b 1
)

if not exist "%SCHEMA_FILE%" (
    call :log_error "Schema file not found: %SCHEMA_FILE%"
    exit /b 1
)

call :log_success "All dependencies are available"
goto :eof

REM 測試數據庫連接
:test_connection
call :log_info "Testing database connection..."

set PGPASSWORD=%DB_PASSWORD%
psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %ADMIN_DB% -c "SELECT 1;" >nul 2>&1
if errorlevel 1 (
    call :log_error "Failed to connect to database"
    exit /b 1
)

call :log_success "Database connection successful"
goto :eof

REM 創建項目數據庫
:create_project_database
set project_id=%~1
set db_name=acc_project_%project_id:b.=%
set db_name=%db_name:-=_%
set db_name=%db_name:.=_%

call :log_info "Creating database for project: %project_id%"
call :log_info "Database name: %db_name%"

REM 檢查數據庫是否已存在
set PGPASSWORD=%DB_PASSWORD%
for /f %%i in ('psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %ADMIN_DB% -t -c "SELECT 1 FROM pg_database WHERE datname = '%db_name%'"') do (
    call :log_warning "Database %db_name% already exists, skipping creation"
    goto :eof
)

REM 創建數據庫
set PGPASSWORD=%DB_PASSWORD%
psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %ADMIN_DB% -c "CREATE DATABASE \"%db_name%\";" >nul 2>&1
if errorlevel 1 (
    call :log_error "Failed to create database: %db_name%"
    exit /b 1
)

call :log_success "Created database: %db_name%"

REM 初始化架構
set PGPASSWORD=%DB_PASSWORD%
psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %db_name% -f %SCHEMA_FILE% >nul 2>&1
if errorlevel 1 (
    call :log_error "Failed to initialize schema for database: %db_name%"
    exit /b 1
)

call :log_success "Initialized schema for database: %db_name%"
goto :eof

REM 從配置文件批量創建數據庫
:batch_create_from_config
call :log_info "Creating databases from configuration file: %CONFIG_FILE%"

if not exist "%CONFIG_FILE%" (
    call :log_error "Configuration file not found: %CONFIG_FILE%"
    exit /b 1
)

REM 使用 Python 解析 YAML 並提取項目 ID
python -c "import yaml; config=yaml.safe_load(open('%CONFIG_FILE%', 'r')); projects=config.get('projects', {}); [print(project_id) for project_id in projects.keys()]" > temp_projects.txt

set success_count=0
set total_count=0

for /f "delims=" %%i in (temp_projects.txt) do (
    set /a total_count+=1
    call :create_project_database "%%i"
    if not errorlevel 1 (
        set /a success_count+=1
    )
)

del temp_projects.txt

call :log_success "Created %success_count% out of %total_count% project databases"
goto :eof

REM 列出所有項目數據庫
:list_project_databases
call :log_info "Listing all project databases..."

set PGPASSWORD=%DB_PASSWORD%
psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %ADMIN_DB% -c "SELECT datname as database_name, pg_size_pretty(pg_database_size(datname)) as size, (SELECT count(*) FROM pg_stat_activity WHERE datname = d.datname) as connections FROM pg_database d WHERE datname LIKE 'acc_project_%%' ORDER BY datname;"
goto :eof

REM 刪除項目數據庫
:delete_project_database
set project_id=%~1
set db_name=acc_project_%project_id:b.=%
set db_name=%db_name:-=_%
set db_name=%db_name:.=_%

call :log_warning "Deleting database for project: %project_id%"
call :log_warning "Database name: %db_name%"

set /p confirm="Are you sure you want to delete database '%db_name%'? (yes/no): "
if not "%confirm%"=="yes" (
    call :log_info "Operation cancelled"
    goto :eof
)

REM 終止所有連接
set PGPASSWORD=%DB_PASSWORD%
psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %ADMIN_DB% -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '%db_name%' AND pid <> pg_backend_pid();" >nul 2>&1

REM 刪除數據庫
set PGPASSWORD=%DB_PASSWORD%
psql -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %ADMIN_DB% -c "DROP DATABASE IF EXISTS \"%db_name%\";" >nul 2>&1
if errorlevel 1 (
    call :log_error "Failed to delete database: %db_name%"
    exit /b 1
)

call :log_success "Deleted database: %db_name%"
goto :eof

REM 備份項目數據庫
:backup_project_database
set project_id=%~1
set db_name=acc_project_%project_id:b.=%
set db_name=%db_name:-=_%
set db_name=%db_name:.=_%
set backup_dir=backups
set timestamp=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set timestamp=%timestamp: =0%
set backup_file=%backup_dir%\%db_name%_%timestamp%.sql

call :log_info "Backing up database: %db_name%"

REM 創建備份目錄
if not exist "%backup_dir%" mkdir "%backup_dir%"

REM 執行備份
set PGPASSWORD=%DB_PASSWORD%
pg_dump -h %DB_HOST% -p %DB_PORT% -U %DB_USER% -d %db_name% > "%backup_file%"
if errorlevel 1 (
    call :log_error "Failed to backup database: %db_name%"
    exit /b 1
)

call :log_success "Backup created: %backup_file%"
goto :eof

REM 顯示幫助信息
:show_help
echo ACC Multi-Database Deployment Script (Windows)
echo.
echo Usage: %~nx0 [COMMAND] [OPTIONS]
echo.
echo Commands:
echo   check           Check dependencies and database connection
echo   create PROJECT_ID   Create database for specific project
echo   batch-create    Create databases for all projects in config file
echo   list            List all project databases
echo   delete PROJECT_ID   Delete database for specific project
echo   backup PROJECT_ID   Backup specific project database
echo   help            Show this help message
echo.
echo Examples:
echo   %~nx0 check
echo   %~nx0 create b.1eea4119-3553-4167-b93d-3a3d5d07d33d
echo   %~nx0 batch-create
echo   %~nx0 list
echo   %~nx0 backup b.1eea4119-3553-4167-b93d-3a3d5d07d33d
goto :eof

REM 主函數
:main
if "%~1"=="check" (
    call :check_dependencies
    call :test_connection
) else if "%~1"=="create" (
    if "%~2"=="" (
        call :log_error "Project ID is required"
        echo Usage: %~nx0 create PROJECT_ID
        exit /b 1
    )
    call :check_dependencies
    call :test_connection
    call :create_project_database "%~2"
) else if "%~1"=="batch-create" (
    call :check_dependencies
    call :test_connection
    call :batch_create_from_config
) else if "%~1"=="list" (
    call :check_dependencies
    call :test_connection
    call :list_project_databases
) else if "%~1"=="delete" (
    if "%~2"=="" (
        call :log_error "Project ID is required"
        echo Usage: %~nx0 delete PROJECT_ID
        exit /b 1
    )
    call :check_dependencies
    call :test_connection
    call :delete_project_database "%~2"
) else if "%~1"=="backup" (
    if "%~2"=="" (
        call :log_error "Project ID is required"
        echo Usage: %~nx0 backup PROJECT_ID
        exit /b 1
    )
    call :check_dependencies
    call :test_connection
    call :backup_project_database "%~2"
) else if "%~1"=="help" (
    call :show_help
) else if "%~1"=="--help" (
    call :show_help
) else if "%~1"=="-h" (
    call :show_help
) else if "%~1"=="" (
    call :show_help
) else (
    call :log_error "Unknown command: %~1"
    call :show_help
    exit /b 1
)

goto :eof

REM 執行主函數
call :main %*
