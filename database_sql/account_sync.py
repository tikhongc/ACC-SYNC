"""
Account data synchronization script
Specialized for syncing ACC accounts, users, companies, and role information
Based on AccountRolesList.vue pattern design
"""

import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
import json
import time
import asyncio
import aiohttp
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from database_sql.neon_config import NeonConfig
    import psycopg2
    import psycopg2.extras
    # Import utils for 2-legged token support
    from utils import get_two_legged_token
except ImportError:
    print("Warning: Could not import database dependencies")
    NeonConfig = None
    psycopg2 = None
    get_two_legged_token = None

@dataclass
class AccountSyncStats:
    """账户同步统计"""
    accounts_synced: int = 0
    users_synced: int = 0
    users_updated: int = 0
    companies_synced: int = 0
    companies_updated: int = 0
    project_users_synced: int = 0
    project_users_updated: int = 0
    roles_synced: int = 0
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []

class AccountDataSyncManager:
    """账户数据同步管理器"""
    
    def __init__(self):
        """初始化同步管理器"""
        self.neon_config = NeonConfig() if NeonConfig else None
        self.db_params = self.neon_config.get_db_params() if self.neon_config else {}
        self.stats = AccountSyncStats()
    
    def get_connection(self):
        """获取数据库连接"""
        if not psycopg2:
            raise Exception("psycopg2 not available")
        return psycopg2.connect(**self.db_params)
    
    def drop_account_tables(self, show_progress: bool = True) -> bool:
        """
        Drop all account-related tables to prevent data corruption
        
        Args:
            show_progress: Whether to show progress messages
            
        Returns:
            True if successful, False otherwise
        """
        if show_progress:
            print("\n[DROP]  Dropping account tables to prevent data corruption...")
        
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Drop tables in reverse dependency order
            tables_to_drop = [
                'project_users',  # References users and projects
                'users',          # References accounts and companies
                'projects',       # References accounts
                'companies',      # References accounts
                'roles',          # References accounts
                'accounts'        # Base table
            ]
            
            for table in tables_to_drop:
                try:
                    cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
                    if show_progress:
                        print(f"   [OK] Dropped table: {table}")
                except Exception as e:
                    if show_progress:
                        print(f"   [WARN] Warning dropping {table}: {e}")
            
            # Drop enum types if they exist
            enum_types = [
                'user_status_type',
                'trade_type'
            ]
            
            for enum_type in enum_types:
                try:
                    cursor.execute(f"DROP TYPE IF EXISTS {enum_type} CASCADE")
                    if show_progress:
                        print(f"   [OK] Dropped enum type: {enum_type}")
                except Exception as e:
                    if show_progress:
                        print(f"   [WARN] Warning dropping {enum_type}: {e}")
            
            conn.commit()
            
            if show_progress:
                print("   [SUCCESS] All account tables dropped successfully")
            
            return True
            
        except Exception as e:
            if conn:
                conn.rollback()
            error_msg = f"Failed to drop account tables: {str(e)}"
            self.stats.errors.append(error_msg)
            if show_progress:
                print(f"   [FAILED] {error_msg}")
            return False
            
        finally:
            if conn:
                conn.close()
    
    def create_account_schema(self, show_progress: bool = True) -> bool:
        """
        Create account schema from optimized SQL file
        
        Args:
            show_progress: Whether to show progress messages
            
        Returns:
            True if successful, False otherwise
        """
        if show_progress:
            print("\n[CREATE]  Creating account schema...")
        
        conn = None
        try:
            import os
            import re
            
            # Find the schema file
            schema_file = os.path.join(os.path.dirname(__file__), 'account_schema_optimized.sql')
            
            if not os.path.exists(schema_file):
                error_msg = f"Schema file not found: {schema_file}"
                self.stats.errors.append(error_msg)
                if show_progress:
                    print(f"   [FAILED] {error_msg}")
                return False
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Read schema file
            with open(schema_file, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            
            # Execute the entire schema as one transaction
            # This handles multi-line functions and DO blocks correctly
            try:
                cursor.execute(schema_sql)
                conn.commit()
                
                if show_progress:
                    print("   [SUCCESS] Account schema created successfully")
                
                return True
                
            except Exception as e:
                # If full execution fails, try to execute in chunks
                if show_progress:
                    print(f"   [WARN] Full execution failed, trying chunk execution: {e}")
                
                conn.rollback()
                
                # Split by major sections, preserving DO blocks and functions
                sections = self._split_sql_into_sections(schema_sql)
                
                for i, section in enumerate(sections):
                    if section.strip() and not section.strip().startswith('--'):
                        try:
                            cursor.execute(section)
                            conn.commit()
                        except Exception as section_error:
                            # Some statements might fail if objects already exist, that's OK
                            if ('already exists' not in str(section_error).lower() and 
                                'does not exist' not in str(section_error).lower()):
                                if show_progress:
                                    print(f"   [WARN] Warning executing section {i+1}: {section_error}")
                            conn.rollback()  # Reset transaction state
                
                if show_progress:
                    print("   [SUCCESS] Account schema created successfully (with warnings)")
                
                return True
            
        except Exception as e:
            if conn:
                conn.rollback()
            error_msg = f"Failed to create account schema: {str(e)}"
            self.stats.errors.append(error_msg)
            if show_progress:
                print(f"   [FAILED] {error_msg}")
            return False
            
        finally:
            if conn:
                conn.close()
    
    def _split_sql_into_sections(self, sql_content: str) -> List[str]:
        """
        Split SQL content into logical sections, preserving multi-line constructs
        """
        import re
        
        # Remove comments but preserve structure
        lines = sql_content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Keep non-comment lines and section headers
            if not line.strip().startswith('--') or line.strip().startswith('-- ====='):
                cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines)
        
        # Split by major sections (marked by comment blocks)
        sections = re.split(r'\n-- =+[^=]*=+\n', content)
        
        # Also split by major SQL constructs
        all_sections = []
        for section in sections:
            if section.strip():
                # Further split by DO blocks, functions, and major statements
                subsections = re.split(r'(?<=\$\$;)\s*\n|(?<=;)\s*\n(?=CREATE|DROP|DO)', section)
                all_sections.extend([s.strip() for s in subsections if s.strip()])
        
        return all_sections
    
    # ========================================================================
    # 账户同步
    # ========================================================================
    
    def sync_project_info(self, project_id: str, account_id: str, project_name: str = None) -> bool:
        """
        同步项目基本信息
        
        Args:
            project_id: 项目ID
            account_id: 账户ID
            project_name: 项目名称（可选）
            
        Returns:
            是否成功
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 首先确保账户记录存在
            cursor.execute("""
                SELECT EXISTS (
                    SELECT 1 FROM accounts 
                    WHERE account_id = %s
                );
            """, [account_id])
            
            account_exists = cursor.fetchone()[0]
            
            if not account_exists:
                print(f"[INFO] Creating account record for project sync: {account_id}")
                cursor.execute("""
                    INSERT INTO accounts (account_id, name, created_at, updated_at)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (account_id) DO NOTHING
                """, [
                    account_id,
                    f"Account {account_id}",
                    datetime.now(timezone.utc),
                    datetime.now(timezone.utc)
                ])
                print(f"[OK] Account record created: {account_id}")
            
            # UPSERT项目信息
            cursor.execute("""
                INSERT INTO projects (project_id, account_id, name, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (project_id)
                DO UPDATE SET
                    name = COALESCE(EXCLUDED.name, projects.name),
                    updated_at = EXCLUDED.updated_at
            """, [
                project_id,
                account_id,
                project_name or f"Project {project_id}",
                datetime.now(timezone.utc),
                datetime.now(timezone.utc)
            ])
            
            conn.commit()
            print(f"[OK] Project sync successful: {project_id}")
            return True
            
        except Exception as e:
            if conn:
                conn.rollback()
            error_msg = f"Project sync failed: {str(e)}"
            self.stats.errors.append(error_msg)
            print(f"[ERROR] {error_msg}")
            return False
            
        finally:
            if conn:
                conn.close()
    
    def sync_account_info(self, account_id: str, account_name: str = None) -> bool:
        """
        同步账户基本信息
        
        Args:
            account_id: ACC账户ID
            account_name: 账户名称（可选）
            
        Returns:
            是否成功
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # UPSERT账户信息
            cursor.execute("""
                INSERT INTO accounts (account_id, name, last_synced_at, sync_status, updated_at)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (account_id)
                DO UPDATE SET
                    name = COALESCE(EXCLUDED.name, accounts.name),
                    last_synced_at = EXCLUDED.last_synced_at,
                    sync_status = EXCLUDED.sync_status,
                    updated_at = EXCLUDED.updated_at
            """, [
                account_id,
                account_name or f"Account {account_id}",
                datetime.now(timezone.utc),
                'synced',
                datetime.now(timezone.utc)
            ])
            
            conn.commit()
            self.stats.accounts_synced += 1
            print(f"[OK] Account sync successful: {account_id}")
            return True
            
        except Exception as e:
            if conn:
                conn.rollback()
            error_msg = f"Account sync failed: {str(e)}"
            self.stats.errors.append(error_msg)
            print(f"[ERROR] {error_msg}")
            return False
            
        finally:
            if conn:
                conn.close()
    
    # ========================================================================
    # 用户同步 (基于 ACC Account Users API)
    # ========================================================================
    
    async def sync_account_users(
        self, 
        session: aiohttp.ClientSession,
        account_id: str,
        headers: Dict[str, str],
        show_progress: bool = True
    ) -> Dict[str, Any]:
        """
        同步账户用户 (GET /hq/v1/accounts/:account_id/users)
        使用2-legged token进行认证
        
        Args:
            session: aiohttp会话
            account_id: 账户ID
            headers: 请求头（将被2-legged token覆盖）
            show_progress: 是否显示进度
            
        Returns:
            同步结果
        """
        if show_progress:
            print(f"\n[USERS] Starting account users sync: {account_id}")
        
        try:
            # 获取2-legged token用于账户级API
            if get_two_legged_token is None:
                raise Exception("2-legged token function not available")
            
            two_legged_token = get_two_legged_token()
            if not two_legged_token:
                raise Exception("Failed to obtain 2-legged token")
            
            # 使用2-legged token的headers
            account_headers = {
                "Authorization": f"Bearer {two_legged_token}",
                "Content-Type": "application/json"
            }
            
            # 获取所有用户（分页）
            all_users = await self._fetch_all_account_users(session, account_id, account_headers, show_progress)
            
            if not all_users:
                print("   [WARN] 未获取到用户数据")
                return {'users_synced': 0, 'users_updated': 0}
            
            # 批量同步到数据库
            inserted, updated = self._batch_upsert_users(account_id, all_users)
            
            self.stats.users_synced += inserted
            self.stats.users_updated += updated
            
            if show_progress:
                print(f"   [OK] 用户同步完成: {inserted}个新增, {updated}个更新")
            
            return {
                'users_synced': inserted,
                'users_updated': updated,
                'total_users': len(all_users)
            }
            
        except Exception as e:
            error_msg = f"同步账户用户失败: {str(e)}"
            self.stats.errors.append(error_msg)
            print(f"   [ERROR] {error_msg}")
            return {'users_synced': 0, 'users_updated': 0}
    
    async def _fetch_all_account_users(
        self,
        session: aiohttp.ClientSession,
        account_id: str,
        headers: Dict[str, str],
        show_progress: bool = True
    ) -> List[Dict]:
        """获取所有账户用户（分页）"""
        all_users = []
        offset = 0
        limit = 100  # API最大限制
        
        while True:
            url = f"https://developer.api.autodesk.com/hq/v1/accounts/{account_id}/users"
            params = {
                'limit': limit,
                'offset': offset,
                'sort': 'name'
            }
            
            if show_progress:
                print(f"   📡 获取用户数据: offset={offset}, limit={limit}")
            
            async with session.get(url, headers=headers, params=params) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"API调用失败: {response.status} - {error_text}")
                
                users = await response.json()
                
                if not users:
                    break
                
                all_users.extend(users)
                
                if show_progress:
                    print(f"      获取到 {len(users)} 个用户，总计 {len(all_users)}")
                
                # 检查是否还有更多数据
                if len(users) < limit:
                    break
                
                offset += limit
        
        return all_users
    
    def _batch_upsert_users(self, account_id: str, users: List[Dict]) -> Tuple[int, int]:
        """批量UPSERT用户"""
        if not users:
            return 0, 0
        
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 准备批量UPSERT SQL（简化版）
            upsert_sql = """
                INSERT INTO users (
                    user_id, account_id, email, name, status, company_id,
                    default_role_id, account_roles, created_at, updated_at
                ) VALUES (
                    %(user_id)s, %(account_id)s, %(email)s, %(name)s, %(status)s, %(company_id)s,
                    %(default_role_id)s, %(account_roles)s, %(created_at)s, %(updated_at)s
                )
                ON CONFLICT (user_id)
                DO UPDATE SET
                    email = EXCLUDED.email,
                    name = EXCLUDED.name,
                    status = EXCLUDED.status,
                    company_id = EXCLUDED.company_id,
                    default_role_id = EXCLUDED.default_role_id,
                    account_roles = EXCLUDED.account_roles,
                    updated_at = EXCLUDED.updated_at
                RETURNING (xmax = 0) AS inserted
            """
            
            # 处理每个用户
            results = []
            for user in users:
                try:
                    user_data = self._transform_user_data(account_id, user)
                    cursor.execute(upsert_sql, user_data)
                    result = cursor.fetchone()
                    if result:
                        results.append(result)
                except Exception as e:
                    error_msg = f"处理用户失败 {user.get('id', 'unknown')}: {str(e)}"
                    self.stats.errors.append(error_msg)
                    print(f"      [ERROR] {error_msg}")
            
            conn.commit()
            
            # 统计结果 (users return single boolean value)
            inserted = sum(1 for result in results if result[0] == True)
            updated = len(results) - inserted
            
            return inserted, updated
            
        except Exception as e:
            if conn:
                conn.rollback()
            error_msg = f"批量UPSERT用户失败: {str(e)}"
            self.stats.errors.append(error_msg)
            print(f"      [ERROR] {error_msg}")
            raise
            
        finally:
            if conn:
                conn.close()
    
    def _transform_user_data(self, account_id: str, user: Dict) -> Dict:
        """转换用户数据为数据库格式（简化版）"""
        now = datetime.now(timezone.utc)
        
        # 解析时间戳
        created_at = None
        if user.get('created_at'):
            try:
                created_at = datetime.fromisoformat(user['created_at'].replace('Z', '+00:00'))
            except:
                pass
        
        updated_at = None
        if user.get('updated_at'):
            try:
                updated_at = datetime.fromisoformat(user['updated_at'].replace('Z', '+00:00'))
            except:
                pass
        
        # 构建账户级角色列表
        account_roles = []
        if user.get('default_role'):
            account_roles.append({
                'id': user.get('default_role_id'),
                'name': user.get('default_role')
            })
        
        # Handle role association - now that we sync roles, we can use the role ID
        default_role_id = user.get('default_role_id')
        # Keep the role ID if it exists, it should be in roles table now
        
        return {
            'user_id': user.get('id'),
            'account_id': account_id,
            'email': user.get('email'),
            'name': user.get('name'),
            'status': user.get('status', 'active'),
            'company_id': user.get('company_id'),
            'default_role_id': default_role_id,  # Set to NULL to avoid FK constraint
            'account_roles': json.dumps(account_roles),
            'created_at': created_at or now,
            'updated_at': updated_at or now
        }
    
    # ========================================================================
    # 公司同步 (基于 ACC Companies API)
    # ========================================================================
    
    async def sync_project_companies(
        self,
        session: aiohttp.ClientSession,
        account_id: str,
        project_id: str,
        headers: Dict[str, str],
        show_progress: bool = True
    ) -> Dict[str, Any]:
        """
        同步项目公司 (GET /hq/v1/accounts/:account_id/projects/:project_id/companies)
        使用2-legged token进行认证
        
        Args:
            session: aiohttp会话
            account_id: 账户ID
            project_id: 项目ID
            headers: 请求头（将被2-legged token覆盖）
            show_progress: 是否显示进度
            
        Returns:
            同步结果
        """
        if show_progress:
            print(f"\n[COMPANIES] 开始同步项目公司: {project_id}")
        
        try:
            # 获取2-legged token用于账户级API
            if get_two_legged_token is None:
                raise Exception("2-legged token function not available")
            
            two_legged_token = get_two_legged_token()
            if not two_legged_token:
                raise Exception("Failed to obtain 2-legged token")
            
            # 使用2-legged token的headers
            account_headers = {
                "Authorization": f"Bearer {two_legged_token}",
                "Content-Type": "application/json"
            }
            
            # 获取所有公司（分页）
            all_companies = await self._fetch_all_project_companies(
                session, account_id, project_id, account_headers, show_progress
            )
            
            if not all_companies:
                print("   [WARN] 未获取到公司数据")
                return {'companies_synced': 0, 'companies_updated': 0}
            
            # 批量同步到数据库
            inserted, updated = self._batch_upsert_companies(account_id, project_id, all_companies)
            
            self.stats.companies_synced += inserted
            self.stats.companies_updated += updated
            
            if show_progress:
                print(f"   [OK] 公司同步完成: {inserted}个新增, {updated}个更新")
            
            return {
                'companies_synced': inserted,
                'companies_updated': updated,
                'total_companies': len(all_companies)
            }
            
        except Exception as e:
            error_msg = f"同步项目公司失败: {str(e)}"
            self.stats.errors.append(error_msg)
            print(f"   [ERROR] {error_msg}")
            return {'companies_synced': 0, 'companies_updated': 0}
    
    async def _fetch_all_project_companies(
        self,
        session: aiohttp.ClientSession,
        account_id: str,
        project_id: str,
        headers: Dict[str, str],
        show_progress: bool = True
    ) -> List[Dict]:
        """获取所有项目公司（分页）"""
        all_companies = []
        offset = 0
        limit = 100  # API最大限制
        
        while True:
            url = f"https://developer.api.autodesk.com/hq/v1/accounts/{account_id}/projects/{project_id}/companies"
            params = {
                'limit': limit,
                'offset': offset,
                'sort': 'name'
            }
            
            if show_progress:
                print(f"   📡 获取公司数据: offset={offset}, limit={limit}")
            
            async with session.get(url, headers=headers, params=params) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"API调用失败: {response.status} - {error_text}")
                
                companies = await response.json()
                
                if not companies:
                    break
                
                all_companies.extend(companies)
                
                if show_progress:
                    print(f"      获取到 {len(companies)} 个公司，总计 {len(all_companies)}")
                
                # 检查是否还有更多数据
                if len(companies) < limit:
                    break
                
                offset += limit
        
        return all_companies
    
    def _batch_upsert_companies(self, account_id: str, project_id: str, companies: List[Dict]) -> Tuple[int, int]:
        """批量UPSERT公司"""
        if not companies:
            return 0, 0
        
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 准备批量UPSERT SQL（简化版）
            upsert_sql = """
                INSERT INTO companies (
                    company_id, account_id, name, trade, country, created_at, updated_at
                ) VALUES (
                    %(company_id)s, %(account_id)s, %(name)s, %(trade)s, %(country)s, %(created_at)s, %(updated_at)s
                )
                ON CONFLICT (company_id)
                DO UPDATE SET
                    name = EXCLUDED.name,
                    trade = EXCLUDED.trade,
                    country = EXCLUDED.country,
                    updated_at = EXCLUDED.updated_at
                RETURNING (xmax = 0) AS inserted
            """
            
            # 处理每个公司
            results = []
            for company in companies:
                try:
                    company_data = self._transform_company_data(account_id, project_id, company)
                    cursor.execute(upsert_sql, company_data)
                    result = cursor.fetchone()
                    if result:
                        results.append(result)
                except Exception as e:
                    error_msg = f"处理公司失败 {company.get('id', 'unknown')}: {str(e)}"
                    self.stats.errors.append(error_msg)
                    print(f"      [ERROR] {error_msg}")
            
            conn.commit()
            
            # 统计结果 (companies return single boolean value)
            inserted = sum(1 for result in results if result[0] == True)
            updated = len(results) - inserted
            
            return inserted, updated
            
        except Exception as e:
            if conn:
                conn.rollback()
            error_msg = f"批量UPSERT公司失败: {str(e)}"
            self.stats.errors.append(error_msg)
            print(f"      [ERROR] {error_msg}")
            raise
            
        finally:
            if conn:
                conn.close()
    
    def _transform_company_data(self, account_id: str, project_id: str, company: Dict) -> Dict:
        """转换公司数据为数据库格式（简化版）"""
        now = datetime.now(timezone.utc)
        
        # 解析时间戳
        created_at = None
        if company.get('created_at'):
            try:
                created_at = datetime.fromisoformat(company['created_at'].replace('Z', '+00:00'))
            except:
                pass
        
        updated_at = None
        if company.get('updated_at'):
            try:
                updated_at = datetime.fromisoformat(company['updated_at'].replace('Z', '+00:00'))
            except:
                pass
        
        # Handle empty trade values
        trade = company.get('trade')
        if trade == '' or trade is None:
            trade = None  # Use NULL instead of empty string for enum
        
        return {
            'company_id': company.get('id'),
            'account_id': account_id,
            'name': company.get('name'),
            'trade': trade,
            'country': company.get('country'),
            'created_at': created_at or now,
            'updated_at': updated_at or now
        }
    
    # ========================================================================
    # 角色同步 (从项目用户数据中提取)
    # ========================================================================
    
    async def sync_roles_from_project_users(
        self,
        session: aiohttp.ClientSession,
        account_id: str,
        project_ids: List[str],
        headers: Dict[str, str],
        show_progress: bool = True
    ) -> Dict[str, Any]:
        """
        从项目用户数据中提取并同步角色信息
        
        Args:
            session: aiohttp会话
            project_ids: 项目ID列表
            headers: 请求头
            show_progress: 是否显示进度
            
        Returns:
            同步结果
        """
        if show_progress:
            print(f"\n[ROLES] Extracting roles from project users...")
        
        try:
            all_roles = set()  # 使用set避免重复
            
            # 获取2-legged token用于账户级API
            if get_two_legged_token is None:
                raise Exception("2-legged token function not available")
            
            two_legged_token = get_two_legged_token()
            if not two_legged_token:
                raise Exception("Failed to obtain 2-legged token")
            
            # 使用2-legged token的headers
            account_headers = {
                "Authorization": f"Bearer {two_legged_token}",
                "Content-Type": "application/json"
            }
            
            # 从账户用户数据中提取角色
            account_users = await self._fetch_all_account_users(session, account_id, account_headers, False)
            for user in account_users:
                # 提取默认角色
                if user.get('default_role_id') and user.get('default_role'):
                    all_roles.add((user['default_role_id'], user['default_role']))
            
            # 从每个项目的用户数据中提取角色
            for project_id in project_ids:
                project_users = await self._fetch_all_project_users(session, project_id, headers, False)
                
                for user in project_users:
                    # 提取角色信息
                    roles = user.get('roles', [])
                    for role in roles:
                        if role.get('id') and role.get('name'):
                            all_roles.add((role['id'], role['name']))
            
            if not all_roles:
                if show_progress:
                    print("   [WARN] No roles found in project users data")
                return {'roles_synced': 0}
            
            # 批量同步角色到数据库
            inserted = self._batch_upsert_roles(all_roles, show_progress)
            
            self.stats.roles_synced = inserted
            
            if show_progress:
                print(f"   [OK] Roles sync completed: {inserted} roles synced")
            
            return {
                'roles_synced': inserted,
                'total_roles': len(all_roles)
            }
            
        except Exception as e:
            error_msg = f"Role sync failed: {str(e)}"
            self.stats.errors.append(error_msg)
            if show_progress:
                print(f"   [ERROR] {error_msg}")
            return {'roles_synced': 0}
    
    def _batch_upsert_roles(self, roles_set: set, show_progress: bool = True) -> int:
        """批量UPSERT角色"""
        if not roles_set:
            return 0
        
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 准备批量UPSERT SQL
            upsert_sql = """
                INSERT INTO roles (
                    role_id, name, description, created_at, updated_at
                ) VALUES (
                    %(role_id)s, %(name)s, %(description)s, %(created_at)s, %(updated_at)s
                )
                ON CONFLICT (role_id)
                DO UPDATE SET
                    name = EXCLUDED.name,
                    updated_at = EXCLUDED.updated_at
                RETURNING (xmax = 0) AS inserted
            """
            
            # 处理每个角色
            results = []
            now = datetime.now(timezone.utc)
            
            for role_id, role_name in roles_set:
                try:
                    role_data = {
                        'role_id': role_id,
                        'name': role_name,
                        'description': f"Role: {role_name}",  # 简单描述
                        'created_at': now,
                        'updated_at': now
                    }
                    cursor.execute(upsert_sql, role_data)
                    result = cursor.fetchone()
                    if result:
                        results.append(result)
                except Exception as e:
                    error_msg = f"Process role failed {role_id}: {str(e)}"
                    self.stats.errors.append(error_msg)
                    if show_progress:
                        print(f"      [ERROR] {error_msg}")
            
            conn.commit()
            
            # 统计结果 (roles return single boolean value)
            inserted = sum(1 for result in results if result[0] == True)
            
            return inserted
            
        except Exception as e:
            if conn:
                conn.rollback()
            error_msg = f"Batch UPSERT roles failed: {str(e)}"
            self.stats.errors.append(error_msg)
            if show_progress:
                print(f"      [ERROR] {error_msg}")
            raise
            
        finally:
            if conn:
                conn.close()
    
    # ========================================================================
    # 项目用户同步 (基于现有的 ACC Project Users API)
    # ========================================================================
    
    async def sync_project_users(
        self,
        session: aiohttp.ClientSession,
        project_id: str,
        headers: Dict[str, str],
        show_progress: bool = True
    ) -> Dict[str, Any]:
        """
        同步项目用户 (GET /construction/admin/v1/projects/:project_id/users)
        
        Args:
            session: aiohttp会话
            project_id: 项目ID
            headers: 请求头
            show_progress: 是否显示进度
            
        Returns:
            同步结果
        """
        if show_progress:
            print(f"\n[PROJ_USERS] 开始同步项目用户: {project_id}")
        
        try:
            # 获取所有项目用户（分页）
            all_users = await self._fetch_all_project_users(session, project_id, headers, show_progress)
            
            if not all_users:
                print("   [WARN] 未获取到项目用户数据")
                return {'project_users_synced': 0, 'project_users_updated': 0}
            
            # 批量同步到数据库
            inserted, updated = self._batch_upsert_project_users(project_id, all_users)
            
            self.stats.project_users_synced += inserted
            self.stats.project_users_updated += updated
            
            if show_progress:
                print(f"   [OK] 项目用户同步完成: {inserted}个新增, {updated}个更新")
            
            return {
                'project_users_synced': inserted,
                'project_users_updated': updated,
                'total_project_users': len(all_users)
            }
            
        except Exception as e:
            error_msg = f"同步项目用户失败: {str(e)}"
            self.stats.errors.append(error_msg)
            print(f"   [ERROR] {error_msg}")
            return {'project_users_synced': 0, 'project_users_updated': 0}
    
    async def _fetch_all_project_users(
        self,
        session: aiohttp.ClientSession,
        project_id: str,
        headers: Dict[str, str],
        show_progress: bool = True
    ) -> List[Dict]:
        """获取所有项目用户（分页）"""
        all_users = []
        offset = 0
        limit = 200  # API最大限制
        
        # 清理项目ID前缀
        clean_project_id = project_id.replace('b.', '') if project_id.startswith('b.') else project_id
        
        while True:
            url = f"https://developer.api.autodesk.com/construction/admin/v1/projects/{clean_project_id}/users"
            params = {
                'limit': limit,
                'offset': offset,
                'sort': 'name',
                'fields': 'name,email,firstName,lastName,autodeskId,analyticsId,addressLine1,addressLine2,city,stateOrProvince,postalCode,country,imageUrl,phone,jobTitle,industry,aboutMe,accessLevels,companyId,companyName,roleIds,roles,status,addedOn,products'
            }
            
            if show_progress:
                print(f"   📡 获取项目用户数据: offset={offset}, limit={limit}")
            
            async with session.get(url, headers=headers, params=params) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"API调用失败: {response.status} - {error_text}")
                
                data = await response.json()
                users = data.get('results', [])
                
                if not users:
                    break
                
                all_users.extend(users)
                
                # 检查是否还有更多数据
                pagination = data.get('pagination', {})
                total_results = pagination.get('totalResults', len(users))
                
                if show_progress:
                    print(f"      获取到 {len(users)} 个用户，总计 {len(all_users)}/{total_results}")
                
                if offset + len(users) >= total_results:
                    break
                
                offset += limit
        
        return all_users
    
    def _batch_upsert_project_users(self, project_id: str, users: List[Dict]) -> Tuple[int, int]:
        """批量UPSERT项目用户"""
        if not users:
            return 0, 0
        
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 准备批量UPSERT SQL
            upsert_sql = """
                INSERT INTO project_users (
                    project_id, user_id, project_user_id, autodesk_id, analytics_id,
                    status, access_levels, role_ids, roles, products,
                    project_company_id, project_company_name, added_on,
                    last_synced_at, sync_status, created_at, updated_at
                ) VALUES (
                    %(project_id)s, %(user_id)s, %(project_user_id)s, %(autodesk_id)s, %(analytics_id)s,
                    %(status)s, %(access_levels)s, %(role_ids)s, %(roles)s, %(products)s,
                    %(project_company_id)s, %(project_company_name)s, %(added_on)s,
                    %(last_synced_at)s, %(sync_status)s, %(created_at)s, %(updated_at)s
                )
                ON CONFLICT (project_id, user_id)
                DO UPDATE SET
                    project_user_id = EXCLUDED.project_user_id,
                    autodesk_id = EXCLUDED.autodesk_id,
                    analytics_id = EXCLUDED.analytics_id,
                    status = EXCLUDED.status,
                    access_levels = EXCLUDED.access_levels,
                    role_ids = EXCLUDED.role_ids,
                    roles = EXCLUDED.roles,
                    products = EXCLUDED.products,
                    project_company_id = EXCLUDED.project_company_id,
                    project_company_name = EXCLUDED.project_company_name,
                    added_on = EXCLUDED.added_on,
                    last_synced_at = EXCLUDED.last_synced_at,
                    sync_status = EXCLUDED.sync_status,
                    updated_at = EXCLUDED.updated_at
                RETURNING id, (xmax = 0) AS inserted
            """
            
            # 处理每个用户
            results = []
            for user in users:
                try:
                    user_data = self._transform_project_user_data(project_id, user)
                    cursor.execute(upsert_sql, user_data)
                    result = cursor.fetchone()
                    if result:
                        results.append(result)
                except Exception as e:
                    error_msg = f"处理项目用户失败 {user.get('id', 'unknown')}: {str(e)}"
                    self.stats.errors.append(error_msg)
                    print(f"      [ERROR] {error_msg}")
            
            conn.commit()
            
            # 统计结果 (project_users return id and boolean)
            inserted = sum(1 for _, is_insert in results if is_insert)
            updated = len(results) - inserted
            
            return inserted, updated
            
        except Exception as e:
            if conn:
                conn.rollback()
            error_msg = f"批量UPSERT项目用户失败: {str(e)}"
            self.stats.errors.append(error_msg)
            print(f"      [ERROR] {error_msg}")
            raise
            
        finally:
            if conn:
                conn.close()
    
    def _transform_project_user_data(self, project_id: str, user: Dict) -> Dict:
        """转换项目用户数据为数据库格式"""
        now = datetime.now(timezone.utc)
        
        # 解析时间戳
        added_on = None
        if user.get('addedOn'):
            try:
                added_on = datetime.fromisoformat(user['addedOn'].replace('Z', '+00:00'))
            except:
                pass
        
        return {
            'project_id': project_id,
            'user_id': user.get('id'),
            'project_user_id': user.get('id'),  # 在项目用户API中，这通常是同一个ID
            'autodesk_id': user.get('autodeskId'),
            'analytics_id': user.get('analyticsId'),
            'status': user.get('status', 'active'),
            'access_levels': json.dumps(user.get('accessLevels', {})),
            'role_ids': json.dumps(user.get('roleIds', [])),
            'roles': json.dumps(user.get('roles', [])),
            'products': json.dumps(user.get('products', [])),
            'project_company_id': user.get('companyId'),
            'project_company_name': user.get('companyName'),
            'added_on': added_on,
            'last_synced_at': now,
            'sync_status': 'synced',
            'created_at': now,
            'updated_at': now
        }
    
    # ========================================================================
    # 角色汇总分析 (基于 AccountRolesList.vue 的模式)
    # ========================================================================
    
    def get_account_roles_summary(self, account_id: str) -> Dict[str, Any]:
        """
        获取账户角色汇总（类似 AccountRolesList.vue 的功能）
        
        Args:
            account_id: 账户ID
            
        Returns:
            角色汇总数据
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            start_time = time.time()
            
            # 获取角色汇总统计
            cursor.execute("""
                WITH role_stats AS (
                    SELECT 
                        jsonb_array_elements(pu.roles)->>'name' as role_name,
                        jsonb_array_elements(pu.roles)->>'id' as role_id,
                        COUNT(DISTINCT pu.user_id) as unique_users,
                        COUNT(DISTINCT pu.project_id) as unique_projects,
                        COUNT(*) as total_assignments,
                        array_agg(DISTINCT pu.project_id) as projects,
                        array_agg(DISTINCT jsonb_build_object(
                            'user_id', u.user_id,
                            'user_name', u.name,
                            'user_email', u.email,
                            'status', pu.status,
                            'project_id', pu.project_id
                        )) as users
                    FROM project_users pu
                    JOIN users u ON pu.user_id = u.user_id
                    WHERE u.account_id = %s
                    AND jsonb_array_length(pu.roles) > 0
                    GROUP BY jsonb_array_elements(pu.roles)->>'name', jsonb_array_elements(pu.roles)->>'id'
                )
                SELECT * FROM role_stats
                ORDER BY unique_users DESC, role_name ASC
            """, [account_id])
            
            role_summary = [dict(row) for row in cursor.fetchall()]
            
            # 获取总体统计 (fixed to avoid set-returning function in aggregate)
            cursor.execute("""
                WITH role_expanded AS (
                    SELECT 
                        pu.user_id,
                        pu.project_id,
                        jsonb_array_elements(pu.roles)->>'name' as role_name
                    FROM project_users pu
                    JOIN users u ON pu.user_id = u.user_id
                    WHERE u.account_id = %s
                    AND jsonb_array_length(pu.roles) > 0
                )
                SELECT 
                    COUNT(DISTINCT role_name) as unique_roles,
                    COUNT(*) as total_role_assignments,
                    COUNT(DISTINCT user_id) as users_with_roles,
                    COUNT(DISTINCT project_id) as projects_with_roles
                FROM role_expanded
            """, [account_id])
            
            statistics = dict(cursor.fetchone()) if cursor.rowcount > 0 else {}
            
            # 获取用户角色映射 (fixed to avoid set-returning function in aggregate)
            cursor.execute("""
                WITH user_roles_expanded AS (
                    SELECT 
                        u.user_id,
                        u.name as user_name,
                        u.email as user_email,
                        jsonb_array_elements(pu.roles)->>'name' as role_name
                    FROM users u
                    JOIN project_users pu ON u.user_id = pu.user_id
                    WHERE u.account_id = %s
                    AND jsonb_array_length(pu.roles) > 0
                )
                SELECT 
                    user_id,
                    user_name,
                    user_email,
                    array_agg(DISTINCT role_name) as roles
                FROM user_roles_expanded
                GROUP BY user_id, user_name, user_email
            """, [account_id])
            
            user_role_mapping = {row['user_id']: dict(row) for row in cursor.fetchall()}
            
            query_duration = time.time() - start_time
            statistics['query_duration_seconds'] = round(query_duration, 3)
            
            # 获取角色表中的所有角色及其用户统计
            cursor.execute("""
                SELECT 
                    r.role_id,
                    r.name as role_name,
                    r.description,
                    r.created_at,
                    -- 统计使用此角色作为默认角色的用户数
                    COUNT(DISTINCT u.user_id) as users_with_default_role,
                    -- 统计在项目中使用此角色的用户数
                    COUNT(DISTINCT pu_role.user_id) as users_in_projects,
                    -- 统计使用此角色的项目数
                    COUNT(DISTINCT pu_role.project_id) as projects_using_role
                FROM roles r
                LEFT JOIN users u ON r.role_id = u.default_role_id
                LEFT JOIN (
                    SELECT DISTINCT 
                        pu.user_id, 
                        pu.project_id,
                        jsonb_array_elements(pu.roles)->>'id' as role_id
                    FROM project_users pu
                    WHERE jsonb_array_length(pu.roles) > 0
                ) pu_role ON r.role_id = pu_role.role_id
                GROUP BY r.role_id, r.name, r.description, r.created_at
                ORDER BY users_with_default_role DESC, users_in_projects DESC, r.name ASC
            """)
            
            roles_detail = [dict(row) for row in cursor.fetchall()]
            
            return {
                'role_summary': role_summary,
                'user_role_mapping': user_role_mapping,
                'roles_detail': roles_detail,  # 新增：角色详细信息
                'statistics': statistics,
                'query_time': datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            error_msg = f"获取角色汇总失败: {str(e)}"
            print(f"[ERROR] {error_msg}")
            return {
                'role_summary': [],
                'user_role_mapping': {},
                'statistics': {},
                'error': error_msg
            }
            
        finally:
            if conn:
                conn.close()
    
    def get_users_by_role(self, role_id: str = None, role_name: str = None) -> Dict[str, Any]:
        """
        获取指定角色下的所有用户
        
        Args:
            role_id: 角色ID
            role_name: 角色名称 (如果没有role_id)
            
        Returns:
            角色及其用户信息
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # 构建查询条件
            if role_id:
                role_condition = "r.role_id = %s"
                role_param = role_id
            elif role_name:
                role_condition = "r.name = %s"
                role_param = role_name
            else:
                raise ValueError("Must provide either role_id or role_name")
            
            # 查询角色信息
            cursor.execute(f"""
                SELECT role_id, name, description, created_at
                FROM roles r
                WHERE {role_condition}
            """, [role_param])
            
            role_info = cursor.fetchone()
            if not role_info:
                return {'error': 'Role not found'}
            
            role_info = dict(role_info)
            
            # 查询使用此角色作为默认角色的用户
            cursor.execute(f"""
                SELECT 
                    u.user_id,
                    u.name as user_name,
                    u.email,
                    u.status,
                    c.name as company_name,
                    'default_role' as role_type
                FROM users u
                LEFT JOIN companies c ON u.company_id = c.company_id
                LEFT JOIN roles r ON u.default_role_id = r.role_id
                WHERE {role_condition}
            """, [role_param])
            
            default_role_users = [dict(row) for row in cursor.fetchall()]
            
            # 查询在项目中使用此角色的用户
            cursor.execute(f"""
                SELECT DISTINCT
                    u.user_id,
                    u.name as user_name,
                    u.email,
                    u.status,
                    c.name as company_name,
                    pu.project_id,
                    p.name as project_name,
                    'project_role' as role_type
                FROM users u
                LEFT JOIN companies c ON u.company_id = c.company_id
                JOIN project_users pu ON u.user_id = pu.user_id
                LEFT JOIN projects p ON pu.project_id = p.project_id
                JOIN roles r ON r.role_id = %s
                WHERE pu.roles @> jsonb_build_array(jsonb_build_object('id', r.role_id))
                AND jsonb_array_length(pu.roles) > 0
            """, [role_param])
            
            project_role_users = [dict(row) for row in cursor.fetchall()]
            
            # 合并用户列表（去重）
            all_users = {}
            
            # 添加默认角色用户
            for user in default_role_users:
                user_id = user['user_id']
                if user_id not in all_users:
                    all_users[user_id] = user
                    all_users[user_id]['role_types'] = []
                all_users[user_id]['role_types'].append('default_role')
            
            # 添加项目角色用户
            for user in project_role_users:
                user_id = user['user_id']
                if user_id not in all_users:
                    all_users[user_id] = user
                    all_users[user_id]['role_types'] = []
                if 'project_role' not in all_users[user_id]['role_types']:
                    all_users[user_id]['role_types'].append('project_role')
                
                # 添加项目信息
                if 'projects' not in all_users[user_id]:
                    all_users[user_id]['projects'] = []
                all_users[user_id]['projects'].append({
                    'project_id': user['project_id'],
                    'project_name': user['project_name']
                })
            
            return {
                'role_info': role_info,
                'users': list(all_users.values()),
                'total_users': len(all_users),
                'default_role_users': len(default_role_users),
                'project_role_users': len(project_role_users)
            }
            
        except Exception as e:
            error_msg = f"Query users by role failed: {str(e)}"
            print(f"[ERROR] {error_msg}")
            return {'error': error_msg}
            
        finally:
            if conn:
                conn.close()
    
    # ========================================================================
    # 完整同步流程
    # ========================================================================
    
    async def full_account_sync(
        self,
        account_id: str,
        project_ids: List[str],
        access_token: str,
        show_progress: bool = True,
        clean_first: bool = True
    ) -> Dict[str, Any]:
        """
        完整的账户数据同步
        
        Args:
            account_id: 账户ID
            project_ids: 项目ID列表
            access_token: 访问令牌
            show_progress: 是否显示进度
            clean_first: 是否先清理数据库表
            
        Returns:
            同步结果统计
        """
        if show_progress:
            print(f"\n[START] Starting full account data synchronization")
            print(f"   Account ID: {account_id}")
            print(f"   Projects: {len(project_ids)}")
            print(f"   Clean first: {clean_first}")
            print("=" * 60)
        
        start_time = time.time()
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # 重置统计
        self.stats = AccountSyncStats()
        
        # Step 0: Clean database if requested
        if clean_first:
            if show_progress:
                print(f"\n[CLEAN] Cleaning database to prevent data corruption...")
            
            # Drop existing tables
            drop_success = self.drop_account_tables(show_progress)
            if not drop_success:
                if show_progress:
                    print("   [WARN] Warning: Failed to drop some tables, continuing anyway...")
            
            # Recreate schema
            schema_success = self.create_account_schema(show_progress)
            if not schema_success:
                error_msg = "Failed to create account schema"
                self.stats.errors.append(error_msg)
                if show_progress:
                    print(f"   [FAILED] {error_msg}")
                return {
                    'account_id': account_id,
                    'projects_processed': 0,
                    'statistics': {
                        'accounts_synced': 0,
                        'users_synced': 0,
                        'users_updated': 0,
                        'companies_synced': 0,
                        'companies_updated': 0,
                        'project_users_synced': 0,
                        'project_users_updated': 0,
                        'total_errors': len(self.stats.errors)
                    },
                    'errors': self.stats.errors,
                    'execution_time': f"{time.time() - start_time:.2f}s",
                    'sync_time': datetime.now(timezone.utc).isoformat()
                }
        
        async with aiohttp.ClientSession() as session:
            # 1. 同步账户信息
            if show_progress:
                print(f"\n[SYNC] Syncing account information...")
            self.sync_account_info(account_id)
            
            # 2. 同步项目信息和公司 (必须在用户之前)
            for project_id in project_ids:
                if show_progress:
                    print(f"\n[PROJECT] Processing project: {project_id}")
                
                # 同步项目基本信息
                self.sync_project_info(project_id, account_id)
                
                # 同步项目公司 (必须在用户之前，因为用户表有外键引用)
                await self.sync_project_companies(session, account_id, project_id, headers, show_progress)
            
            # 3. 同步角色 (在用户之前，因为用户表有外键引用)
            if show_progress:
                print(f"\n[ROLES] Syncing roles...")
            await self.sync_roles_from_project_users(session, account_id, project_ids, headers, show_progress)
            
            # 4. 同步用户 (在公司和角色同步完成后)
            if show_progress:
                print(f"\n[USERS] Syncing account users...")
            await self.sync_account_users(session, account_id, headers, show_progress)
            
            # 5. 同步项目用户 (在用户和公司都同步完成后)
            for project_id in project_ids:
                if show_progress:
                    print(f"\n[PROJ_USERS] Processing project users: {project_id}")
                
                # 同步项目用户
                await self.sync_project_users(session, project_id, headers, show_progress)
        
        total_time = time.time() - start_time
        
        # 生成最终报告
        result = {
            'account_id': account_id,
            'projects_processed': len(project_ids),
            'statistics': {
                'accounts_synced': self.stats.accounts_synced,
                'users_synced': self.stats.users_synced,
                'users_updated': self.stats.users_updated,
                'companies_synced': self.stats.companies_synced,
                'companies_updated': self.stats.companies_updated,
                'project_users_synced': self.stats.project_users_synced,
                'project_users_updated': self.stats.project_users_updated,
                'total_errors': len(self.stats.errors)
            },
            'errors': self.stats.errors,
            'execution_time': f"{total_time:.2f}秒",
            'sync_time': datetime.now(timezone.utc).isoformat()
        }
        
        if show_progress:
            print("\n" + "=" * 60)
            print("[STATS] 同步完成统计:")
            print(f"   账户: {self.stats.accounts_synced}个")
            print(f"   用户: {self.stats.users_synced}个新增, {self.stats.users_updated}个更新")
            print(f"   公司: {self.stats.companies_synced}个新增, {self.stats.companies_updated}个更新")
            print(f"   项目用户: {self.stats.project_users_synced}个新增, {self.stats.project_users_updated}个更新")
            print(f"   错误: {len(self.stats.errors)}个")
            print(f"   总耗时: {total_time:.2f}秒")
            
            if self.stats.errors:
                print(f"\n[FAILED] 错误详情:")
                for error in self.stats.errors[:5]:  # 只显示前5个错误
                    print(f"   - {error}")
                if len(self.stats.errors) > 5:
                    print(f"   ... 还有 {len(self.stats.errors) - 5} 个错误")
        
        return result


# ============================================================================
# 便捷函数
# ============================================================================

def get_account_sync_manager() -> AccountDataSyncManager:
    """获取账户同步管理器实例"""
    return AccountDataSyncManager()


async def sync_account_data(
    account_id: str,
    project_ids: List[str],
    access_token: str,
    show_progress: bool = True,
    clean_first: bool = True
) -> Dict[str, Any]:
    """
    便捷的账户数据同步函数
    
    Args:
        account_id: 账户ID
        project_ids: 项目ID列表
        access_token: 访问令牌
        show_progress: 是否显示进度
        clean_first: 是否先清理数据库表
        
    Returns:
        同步结果
    """
    manager = get_account_sync_manager()
    return await manager.full_account_sync(account_id, project_ids, access_token, show_progress, clean_first)


if __name__ == "__main__":
    # 测试代码
    print("账户数据同步脚本测试")
    print("=" * 60)
    
    try:
        manager = get_account_sync_manager()
        print("[OK] 账户同步管理器初始化成功")
        
        # 测试角色汇总功能
        # account_id = "your-account-id"
        # summary = manager.get_account_roles_summary(account_id)
        # print(f"\n角色汇总测试:")
        # print(json.dumps(summary, indent=2, ensure_ascii=False, default=str))
        
    except Exception as e:
        print(f"[ERROR] 错误: {e}")
        import traceback
        traceback.print_exc()
