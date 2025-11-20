# -*- coding: utf-8 -*-
"""
权限同步到数据库模块
从 ACC API 获取文件夹权限并存储到数据库的 folders 表
"""

import asyncio
import asyncpg
import requests
import json
import time
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import logging
import sys
import os

# 添加父目录到路径以导入配置
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
import utils
from database_sql.neon_config import NeonConfig

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 固定的项目 ID
DEFAULT_PROJECT_ID = "b.1eea4119-3553-4167-b93d-3a3d5d07d33d"


class PermissionLevel:
    """权限级别定义"""

    # ACC 权限级别映射
    ACC_PERMISSION_LEVELS = {
        "VIEW_ONLY": {
            "level": 1,
            "name": "View",
            "actions": ["VIEW", "COLLABORATE"],
            "description": "Can only view files"
        },
        "VIEW_DOWNLOAD": {
            "level": 2,
            "name": "查看/下载",
            "actions": ["VIEW", "DOWNLOAD", "COLLABORATE"],
            "description": "Can view and download files"
        },
        "VIEW_DOWNLOAD_MARKUP": {
            "level": 3,
            "name": "查看/下载/标记",
            "actions": ["VIEW", "DOWNLOAD", "COLLABORATE", "PUBLISH_MARKUP"],
            "description": "可以查看、下载文件和发布标记"
        },
        "VIEW_DOWNLOAD_MARKUP_UPLOAD": {
            "level": 4,
            "name": "查看/下载/标记/上传",
            "actions": ["PUBLISH", "VIEW", "DOWNLOAD", "COLLABORATE", "PUBLISH_MARKUP"],
            "description": "可以查看、下载、发布标记和上传文件"
        },
        "FULL_EDIT": {
            "level": 5,
            "name": "Full Edit",
            "actions": ["PUBLISH", "VIEW", "DOWNLOAD", "COLLABORATE", "PUBLISH_MARKUP", "EDIT"],
            "description": "可以查看、下载、发布标记、上传和编辑文件"
        },
        "FULL_CONTROL": {
            "level": 6,
            "name": "Full Control",
            "actions": ["PUBLISH", "VIEW", "DOWNLOAD", "COLLABORATE", "PUBLISH_MARKUP", "EDIT", "CONTROL"],
            "description": "Has full control permissions for the folder"
        }
    }


def clean_project_id(project_id: str) -> str:
    """清理项目ID，移除'b.'前缀"""
    return project_id.replace("b.", "") if project_id.startswith("b.") else project_id


def determine_permission_level(actions: List[str]) -> Dict:
    """根据权限动作确定权限级别"""
    actions_set = set(actions)

    # 从高到低检查权限级别
    for level_key, level_info in reversed(list(PermissionLevel.ACC_PERMISSION_LEVELS.items())):
        level_actions_set = set(level_info["actions"])
        if level_actions_set.issubset(actions_set):
            return level_info

    # 如果没有匹配的权限级别，返回最低级别
    return {
        "level": 0,
        "name": "No Permission",
        "description": "No permissions"
    }


def get_folder_permissions_from_api(project_id: str, folder_id: str, headers: Dict) -> Dict:
    """
    从官方API获取文件夹权限信息
    """
    try:
        # 清理项目ID
        clean_proj_id = clean_project_id(project_id)

        # 构建API URL
        api_url = f"{config.AUTODESK_API_BASE}/bim360/docs/v1/projects/{clean_proj_id}/folders/{folder_id}/permissions"

        response = requests.get(api_url, headers=headers, timeout=(10, 30))

        if response.status_code == 200:
            permissions_data = response.json()

            return {
                "status": "success",
                "data": permissions_data,
                "api_url": api_url,
                "retrieved_at": datetime.now().isoformat()
            }

        elif response.status_code == 403:
            return {
                "status": "error",
                "error": "权限不足，需要VIEW权限才能查看文件夹权限",
                "error_code": "INSUFFICIENT_PERMISSIONS",
                "http_status": 403
            }

        elif response.status_code == 404:
            return {
                "status": "error",
                "error": "Project or folder does not exist",
                "error_code": "NOT_FOUND",
                "http_status": 404
            }

        elif response.status_code == 429:
            return {
                "status": "error",
                "error": "请求过于频繁，请稍后重试",
                "error_code": "RATE_LIMIT",
                "http_status": 429
            }

        else:
            return {
                "status": "error",
                "error": f"API调用失败: HTTP {response.status_code}",
                "details": response.text[:500],
                "error_code": "API_ERROR",
                "http_status": response.status_code
            }

    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "error": "API请求超时",
            "error_code": "TIMEOUT"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"调用权限API时出错: {str(e)}",
            "error_code": "EXCEPTION"
        }


def parse_permissions_data(permissions_data: List[Dict]) -> Dict:
    """
    解析权限数据，转换为结构化格式
    """
    parsed_data = {
        "users": [],
        "roles": [],
        "companies": [],
        "summary": {
            "total_subjects": len(permissions_data),
            "users_count": 0,
            "roles_count": 0,
            "companies_count": 0
        }
    }

    for permission in permissions_data:
        subject_type = permission.get("subjectType", "").upper()

        # 合并直接权限和继承权限
        direct_actions = permission.get("actions", [])
        inherit_actions = permission.get("inheritActions", [])
        all_actions = list(set(direct_actions + inherit_actions))

        # 确定权限级别
        permission_level_info = determine_permission_level(all_actions)

        permission_record = {
            "subject_id": permission.get("subjectId"),
            "autodesk_id": permission.get("autodeskId"),
            "name": permission.get("name"),
            "email": permission.get("email"),
            "user_type": permission.get("userType"),
            "subject_type": subject_type,
            "subject_status": permission.get("subjectStatus"),
            "direct_actions": direct_actions,
            "inherit_actions": inherit_actions,
            "all_actions": all_actions,
            "permission_level": permission_level_info["level"],
            "permission_name": permission_level_info["name"],
            "permission_description": permission_level_info["description"],
            "detailed_permissions": {
                "canView": "VIEW" in all_actions,
                "canDownload": "DOWNLOAD" in all_actions,
                "canCollaborate": "COLLABORATE" in all_actions,
                "canPublishMarkup": "PUBLISH_MARKUP" in all_actions,
                "canUpload": "PUBLISH" in all_actions,
                "canEdit": "EDIT" in all_actions,
                "canControl": "CONTROL" in all_actions
            }
        }

        # 按类型分类
        if subject_type == "USER":
            parsed_data["users"].append(permission_record)
            parsed_data["summary"]["users_count"] += 1
        elif subject_type == "ROLE":
            parsed_data["roles"].append(permission_record)
            parsed_data["summary"]["roles_count"] += 1
        elif subject_type == "COMPANY":
            parsed_data["companies"].append(permission_record)
            parsed_data["summary"]["companies_count"] += 1

    return parsed_data


class PermissionsDatabaseSync:
    """权限同步到数据库的主类"""

    def __init__(self, project_id: str = DEFAULT_PROJECT_ID):
        self.project_id = project_id

        # Neon 数据库配置 - 使用默认的 neondb 数据库（所有项目共享）
        neon_config = NeonConfig()
        self.db_params = neon_config.get_db_params()

        self.pool: Optional[asyncpg.Pool] = None

        # 统计信息
        self.stats = {
            "total_folders": 0,
            "successful_syncs": 0,
            "failed_syncs": 0,
            "total_users": 0,
            "total_roles": 0,
            "total_companies": 0,
            "start_time": None,
            "end_time": None,
            "errors": []
        }

    async def connect(self):
        """创建数据库连接池"""
        try:
            logger.info(f"正在连接到数据库: {self.db_params['database']}")

            self.pool = await asyncpg.create_pool(
                host=self.db_params['host'],
                port=self.db_params['port'],
                database=self.db_params['database'],
                user=self.db_params['user'],
                password=self.db_params['password'],
                ssl='require',
                min_size=2,
                max_size=10,
                command_timeout=60
            )

            logger.info(f"成功连接到数据库: {self.db_params['database']}")

        except Exception as e:
            logger.error(f"连接数据库失败: {str(e)}")
            raise

    async def close(self):
        """关闭数据库连接池"""
        if self.pool:
            await self.pool.close()
            logger.info("数据库连接池已关闭")

    async def get_all_folder_ids(self) -> List[Tuple[str, str]]:
        """
        从数据库获取所有文件夹的 ID 和名称
        返回: [(folder_id, folder_name), ...]
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT id, name, path
                FROM folders
                WHERE project_id = $1
                ORDER BY depth, name
            """, self.project_id)

            return [(row['id'], row['name'], row['path']) for row in rows]

    async def update_folder_permissions(self, folder_id: str, permissions_json: Dict):
        """
        更新单个文件夹的权限数据
        """
        async with self.pool.acquire() as conn:
            await conn.execute("""
                UPDATE folders
                SET
                    permissions = $1::jsonb,
                    permissions_sync_time = $2,
                    updated_at = $3
                WHERE id = $4
            """,
            json.dumps(permissions_json, ensure_ascii=False),
            datetime.now(),
            datetime.now(),
            folder_id)

    async def batch_update_permissions(self, updates: List[Tuple[str, Dict]]):
        """
        批量更新文件夹权限
        updates: [(folder_id, permissions_json), ...]
        """
        if not updates:
            return

        async with self.pool.acquire() as conn:
            # 使用事务进行批量更新
            async with conn.transaction():
                for folder_id, permissions_json in updates:
                    await conn.execute("""
                        UPDATE folders
                        SET
                            permissions = $1::jsonb,
                            permissions_sync_time = $2,
                            updated_at = $3
                        WHERE id = $4
                    """,
                    json.dumps(permissions_json, ensure_ascii=False),
                    datetime.now(),
                    datetime.now(),
                    folder_id)

        logger.info(f"批量更新了 {len(updates)} 个文件夹的权限")

    async def sync_all_permissions(self, batch_size: int = 50, delay: float = 0.2):
        """
        同步所有文件夹的权限到数据库

        参数:
            batch_size: 每批次更新的文件夹数量
            delay: API 调用之间的延迟（秒），避免限流
        """
        self.stats["start_time"] = datetime.now()

        # 获取 access token
        access_token = utils.get_access_token()
        if not access_token:
            raise Exception("未找到 Access Token，请先进行认证")

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        # 获取所有文件夹 ID
        logger.info("正在从数据库获取所有文件夹...")
        folders = await self.get_all_folder_ids()
        self.stats["total_folders"] = len(folders)

        if not folders:
            logger.warning("数据库中没有找到文件夹")
            return self.stats

        logger.info(f"找到 {len(folders)} 个文件夹，开始同步权限...")

        # 准备批量更新
        updates = []

        for i, (folder_id, folder_name, folder_path) in enumerate(folders):
            logger.info(f"同步文件夹权限 ({i+1}/{len(folders)}): {folder_name}")

            # 调用 API 获取权限
            permissions_result = get_folder_permissions_from_api(
                self.project_id, folder_id, headers
            )

            if permissions_result["status"] == "success":
                # 解析权限数据
                parsed_permissions = parse_permissions_data(permissions_result["data"])

                # 添加同步时间
                parsed_permissions["sync_time"] = permissions_result["retrieved_at"]

                # 添加到批量更新列表
                updates.append((folder_id, parsed_permissions))

                # 更新统计
                self.stats["successful_syncs"] += 1
                self.stats["total_users"] += parsed_permissions["summary"]["users_count"]
                self.stats["total_roles"] += parsed_permissions["summary"]["roles_count"]
                self.stats["total_companies"] += parsed_permissions["summary"]["companies_count"]

            else:
                # 记录错误
                error_info = {
                    "folder_id": folder_id,
                    "folder_name": folder_name,
                    "folder_path": folder_path,
                    "error": permissions_result.get("error"),
                    "error_code": permissions_result.get("error_code"),
                    "http_status": permissions_result.get("http_status")
                }
                self.stats["errors"].append(error_info)
                self.stats["failed_syncs"] += 1

                logger.warning(f"获取文件夹 {folder_name} 权限失败: {permissions_result.get('error')}")

            # 批量更新数据库
            if len(updates) >= batch_size:
                await self.batch_update_permissions(updates)
                updates = []

            # 添加延迟避免 API 限流
            time.sleep(delay)

        # 处理剩余的更新
        if updates:
            await self.batch_update_permissions(updates)

        self.stats["end_time"] = datetime.now()
        duration = (self.stats["end_time"] - self.stats["start_time"]).total_seconds()

        # 打印统计信息
        logger.info("=" * 50)
        logger.info("权限同步完成!")
        logger.info(f"  总文件夹数: {self.stats['total_folders']}")
        logger.info(f"  成功同步: {self.stats['successful_syncs']}")
        logger.info(f"  失败同步: {self.stats['failed_syncs']}")
        logger.info(f"  总用户权限: {self.stats['total_users']}")
        logger.info(f"  总角色权限: {self.stats['total_roles']}")
        logger.info(f"  总公司权限: {self.stats['total_companies']}")
        logger.info(f"  耗时: {duration:.2f} 秒")
        logger.info("=" * 50)

        return self.stats


async def run_permissions_sync(project_id: str = DEFAULT_PROJECT_ID):
    """
    运行权限同步的主函数
    """
    syncer = PermissionsDatabaseSync(project_id)

    try:
        await syncer.connect()
        stats = await syncer.sync_all_permissions()
        return stats

    except Exception as e:
        logger.error(f"权限同步失败: {str(e)}")
        raise

    finally:
        await syncer.close()


# 命令行入口
if __name__ == "__main__":
    import argparse

    # Set UTF-8 encoding for Windows console
    if sys.platform == "win32":
        import codecs
        try:
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
            sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(description='Sync ACC folder permissions to database')
    parser.add_argument(
        '--project-id',
        type=str,
        default=DEFAULT_PROJECT_ID,
        help=f'Project ID (default: {DEFAULT_PROJECT_ID})'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=50,
        help='Batch size for folder updates (default: 50)'
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=0.2,
        help='Delay in seconds between API calls (default: 0.2)'
    )

    args = parser.parse_args()

    print(f"Starting permissions sync for project {args.project_id}...")

    try:
        stats = asyncio.run(run_permissions_sync(args.project_id))

        # Output final stats
        print("\nSync results:")
        print(json.dumps(stats, default=str, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Sync failed: {str(e)}")
        sys.exit(1)
