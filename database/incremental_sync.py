# -*- coding: utf-8 -*-
"""
增量同步实现
提供高效的增量数据更新策略
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Set
from pymongo import MongoClient
from .data_access_layer import DataAccessLayer
from .data_sync_strategy import DataTransformer

logger = logging.getLogger(__name__)

class IncrementalSyncManager:
    """增量同步管理器"""
    
    def __init__(self, dal: DataAccessLayer = None):
        self.dal = dal or DataAccessLayer()
        
    def get_last_sync_time(self, project_id: str, sync_type: str = "full") -> Optional[datetime]:
        """获取上次同步时间"""
        try:
            db = self.dal.connect()
            
            # 从项目信息中获取上次同步时间
            project = db.projects.find_one({"_id": project_id})
            if project and project.get("sync_info"):
                return project["sync_info"].get("last_sync_time")
            
            # 从同步任务记录中获取
            last_task = db.sync_tasks.find_one(
                {
                    "project_id": project_id,
                    "task_type": sync_type,
                    "task_status": "completed"
                },
                sort=[("end_time", -1)]
            )
            
            if last_task:
                return last_task.get("end_time")
            
            # 如果没有记录，返回一周前
            return datetime.now() - timedelta(days=7)
            
        except Exception as e:
            logger.error(f"获取上次同步时间失败: {str(e)}")
            return datetime.now() - timedelta(days=7)
    
    def detect_changes(self, project_id: str, since: datetime = None) -> Dict[str, List[str]]:
        """
        检测变更
        
        Returns:
            Dict包含:
            - new_folders: 新增文件夹ID列表
            - updated_folders: 更新文件夹ID列表  
            - deleted_folders: 删除文件夹ID列表
            - new_files: 新增文件ID列表
            - updated_files: 更新文件ID列表
            - deleted_files: 删除文件ID列表
        """
        if not since:
            since = self.get_last_sync_time(project_id)
        
        try:
            db = self.dal.connect()
            
            changes = {
                "new_folders": [],
                "updated_folders": [],
                "deleted_folders": [],
                "new_files": [],
                "updated_files": [],
                "deleted_files": []
            }
            
            # 检测文件夹变更
            # 新增和更新的文件夹（通过sync_time判断）
            folder_query = {
                "project_id": project_id,
                "sync_info.sync_time": {"$gte": since}
            }
            
            changed_folders = list(db.folders.find(folder_query, {"_id": 1, "created_at": 1, "updated_at": 1}))
            
            for folder in changed_folders:
                folder_id = folder["_id"]
                created_at = folder.get("created_at")
                
                if created_at and created_at >= since:
                    changes["new_folders"].append(folder_id)
                else:
                    changes["updated_folders"].append(folder_id)
            
            # 检测文件变更
            file_query = {
                "project_id": project_id,
                "sync_info.sync_time": {"$gte": since}
            }
            
            changed_files = list(db.files.find(file_query, {"_id": 1, "created_at": 1, "updated_at": 1}))
            
            for file in changed_files:
                file_id = file["_id"]
                created_at = file.get("created_at")
                
                if created_at and created_at >= since:
                    changes["new_files"].append(file_id)
                else:
                    changes["updated_files"].append(file_id)
            
            # TODO: 检测删除的项目（需要从API对比）
            # 这需要获取API的完整列表并与数据库对比
            
            logger.info(f"检测到变更: {changes}")
            return changes
            
        except Exception as e:
            logger.error(f"检测变更失败: {str(e)}")
            return {
                "new_folders": [],
                "updated_folders": [],
                "deleted_folders": [],
                "new_files": [],
                "updated_files": [],
                "deleted_files": []
            }
    
    def incremental_sync_folders(self, project_id: str, api_folders_data: List[Dict[str, Any]], 
                                since: datetime = None) -> Dict[str, int]:
        """
        增量同步文件夹
        
        Args:
            project_id: 项目ID
            api_folders_data: 从API获取的文件夹数据
            since: 增量同步起始时间
            
        Returns:
            同步结果统计
        """
        try:
            if not since:
                since = self.get_last_sync_time(project_id)
            
            db = self.dal.connect()
            
            # 获取现有文件夹ID集合
            existing_folders = set(
                folder["_id"] for folder in 
                db.folders.find({"project_id": project_id}, {"_id": 1})
            )
            
            # 分类API数据
            new_folders = []
            updated_folders = []
            api_folder_ids = set()
            
            for api_folder in api_folders_data:
                folder_id = api_folder.get("id")
                if not folder_id:
                    continue
                    
                api_folder_ids.add(folder_id)
                
                # 检查是否需要更新
                attributes = api_folder.get("attributes", {})
                last_modified = attributes.get("lastModifiedTime")
                
                if folder_id in existing_folders:
                    # 检查是否在增量时间范围内修改
                    if last_modified:
                        try:
                            modified_time = DataTransformer._parse_datetime(last_modified)
                            if modified_time and modified_time >= since:
                                updated_folders.append(api_folder)
                        except:
                            # 如果时间解析失败，保守地包含在更新中
                            updated_folders.append(api_folder)
                else:
                    new_folders.append(api_folder)
            
            # 检测删除的文件夹
            deleted_folder_ids = existing_folders - api_folder_ids
            
            stats = {
                "new": 0,
                "updated": 0,
                "deleted": 0,
                "errors": 0
            }
            
            # 处理新增文件夹
            if new_folders:
                logger.info(f"处理 {len(new_folders)} 个新增文件夹")
                new_folder_data = []
                
                for api_folder in new_folders:
                    try:
                        # 需要构建路径信息，这里简化处理
                        db_folder = DataTransformer.transform_folder_data(
                            api_data=api_folder,
                            project_id=project_id,
                            parent_id=api_folder.get("relationships", {}).get("parent", {}).get("data", {}).get("id"),
                            path="",  # 需要从父文件夹构建
                            depth=0   # 需要计算实际深度
                        )
                        new_folder_data.append(db_folder)
                    except Exception as e:
                        logger.error(f"转换新增文件夹失败: {str(e)}")
                        stats["errors"] += 1
                
                if new_folder_data:
                    result = self.dal.batch_upsert_folders(new_folder_data)
                    stats["new"] = result["inserted"] + result["updated"]
            
            # 处理更新文件夹
            if updated_folders:
                logger.info(f"处理 {len(updated_folders)} 个更新文件夹")
                updated_folder_data = []
                
                for api_folder in updated_folders:
                    try:
                        # 获取现有文件夹信息以保持路径
                        existing_folder = db.folders.find_one({"_id": api_folder.get("id")})
                        if existing_folder:
                            db_folder = DataTransformer.transform_folder_data(
                                api_data=api_folder,
                                project_id=project_id,
                                parent_id=existing_folder.get("parent_id"),
                                path=existing_folder.get("path", ""),
                                depth=existing_folder.get("depth", 0)
                            )
                            updated_folder_data.append(db_folder)
                    except Exception as e:
                        logger.error(f"转换更新文件夹失败: {str(e)}")
                        stats["errors"] += 1
                
                if updated_folder_data:
                    result = self.dal.batch_upsert_folders(updated_folder_data)
                    stats["updated"] = result["inserted"] + result["updated"]
            
            # 处理删除文件夹
            if deleted_folder_ids:
                logger.info(f"处理 {len(deleted_folder_ids)} 个删除文件夹")
                delete_result = db.folders.delete_many({"_id": {"$in": list(deleted_folder_ids)}})
                stats["deleted"] = delete_result.deleted_count
                
                # 同时删除这些文件夹下的文件
                file_delete_result = db.files.delete_many({"parent_folder_id": {"$in": list(deleted_folder_ids)}})
                logger.info(f"同时删除了 {file_delete_result.deleted_count} 个文件")
            
            logger.info(f"文件夹增量同步完成: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"文件夹增量同步失败: {str(e)}")
            return {"new": 0, "updated": 0, "deleted": 0, "errors": 1}
    
    def incremental_sync_files(self, project_id: str, api_files_data: List[Dict[str, Any]], 
                              since: datetime = None) -> Dict[str, int]:
        """
        增量同步文件
        
        Args:
            project_id: 项目ID
            api_files_data: 从API获取的文件数据
            since: 增量同步起始时间
            
        Returns:
            同步结果统计
        """
        try:
            if not since:
                since = self.get_last_sync_time(project_id)
            
            db = self.dal.connect()
            
            # 获取现有文件ID集合
            existing_files = set(
                file["_id"] for file in 
                db.files.find({"project_id": project_id}, {"_id": 1})
            )
            
            # 分类API数据
            new_files = []
            updated_files = []
            api_file_ids = set()
            
            for api_file in api_files_data:
                file_id = api_file.get("id")
                if not file_id:
                    continue
                    
                api_file_ids.add(file_id)
                
                # 检查是否需要更新
                attributes = api_file.get("attributes", {})
                last_modified = attributes.get("lastModifiedTime")
                
                if file_id in existing_files:
                    # 检查是否在增量时间范围内修改
                    if last_modified:
                        try:
                            modified_time = DataTransformer._parse_datetime(last_modified)
                            if modified_time and modified_time >= since:
                                updated_files.append(api_file)
                        except:
                            # 如果时间解析失败，保守地包含在更新中
                            updated_files.append(api_file)
                else:
                    new_files.append(api_file)
            
            # 检测删除的文件
            deleted_file_ids = existing_files - api_file_ids
            
            stats = {
                "new": 0,
                "updated": 0,
                "deleted": 0,
                "errors": 0
            }
            
            # 处理新增文件
            if new_files:
                logger.info(f"处理 {len(new_files)} 个新增文件")
                new_file_data = []
                
                for api_file in new_files:
                    try:
                        # 获取父文件夹信息
                        parent_id = api_file.get("relationships", {}).get("parent", {}).get("data", {}).get("id")
                        parent_folder = db.folders.find_one({"_id": parent_id}) if parent_id else None
                        
                        folder_path = parent_folder.get("path", "") if parent_folder else ""
                        depth = (parent_folder.get("depth", 0) + 1) if parent_folder else 0
                        
                        db_file = DataTransformer.transform_file_data(
                            api_data=api_file,
                            project_id=project_id,
                            parent_folder_id=parent_id,
                            folder_path=folder_path,
                            depth=depth
                        )
                        new_file_data.append(db_file)
                    except Exception as e:
                        logger.error(f"转换新增文件失败: {str(e)}")
                        stats["errors"] += 1
                
                if new_file_data:
                    result = self.dal.batch_upsert_files(new_file_data)
                    stats["new"] = result["inserted"] + result["updated"]
            
            # 处理更新文件
            if updated_files:
                logger.info(f"处理 {len(updated_files)} 个更新文件")
                updated_file_data = []
                
                for api_file in updated_files:
                    try:
                        # 获取现有文件信息
                        existing_file = db.files.find_one({"_id": api_file.get("id")})
                        if existing_file:
                            db_file = DataTransformer.transform_file_data(
                                api_data=api_file,
                                project_id=project_id,
                                parent_folder_id=existing_file.get("parent_folder_id"),
                                folder_path=existing_file.get("folder_path", ""),
                                depth=existing_file.get("depth", 0)
                            )
                            updated_file_data.append(db_file)
                    except Exception as e:
                        logger.error(f"转换更新文件失败: {str(e)}")
                        stats["errors"] += 1
                
                if updated_file_data:
                    result = self.dal.batch_upsert_files(updated_file_data)
                    stats["updated"] = result["inserted"] + result["updated"]
            
            # 处理删除文件
            if deleted_file_ids:
                logger.info(f"处理 {len(deleted_file_ids)} 个删除文件")
                
                # 删除文件版本
                version_delete_result = db.file_versions.delete_many({"file_id": {"$in": list(deleted_file_ids)}})
                logger.info(f"删除了 {version_delete_result.deleted_count} 个文件版本")
                
                # 删除文件
                file_delete_result = db.files.delete_many({"_id": {"$in": list(deleted_file_ids)}})
                stats["deleted"] = file_delete_result.deleted_count
            
            logger.info(f"文件增量同步完成: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"文件增量同步失败: {str(e)}")
            return {"new": 0, "updated": 0, "deleted": 0, "errors": 1}
    
    def incremental_sync_versions(self, project_id: str, file_id: str, 
                                 api_versions_data: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        增量同步文件版本
        
        Args:
            project_id: 项目ID
            file_id: 文件ID
            api_versions_data: 从API获取的版本数据
            
        Returns:
            同步结果统计
        """
        try:
            db = self.dal.connect()
            
            # 获取现有版本
            existing_versions = set(
                version["_id"] for version in 
                db.file_versions.find({"file_id": file_id}, {"_id": 1})
            )
            
            new_versions = []
            updated_versions = []
            api_version_ids = set()
            
            for api_version in api_versions_data:
                version_id = api_version.get("id")
                if not version_id:
                    continue
                    
                api_version_ids.add(version_id)
                
                if version_id in existing_versions:
                    updated_versions.append(api_version)
                else:
                    new_versions.append(api_version)
            
            stats = {
                "new": 0,
                "updated": 0,
                "deleted": 0,
                "errors": 0
            }
            
            # 处理新增和更新版本
            all_versions = new_versions + updated_versions
            if all_versions:
                version_data = []
                
                for api_version in all_versions:
                    try:
                        db_version = DataTransformer.transform_version_data(
                            api_data=api_version,
                            file_id=file_id,
                            project_id=project_id
                        )
                        version_data.append(db_version)
                    except Exception as e:
                        logger.error(f"转换版本数据失败: {str(e)}")
                        stats["errors"] += 1
                
                if version_data:
                    result = self.dal.batch_upsert_file_versions(version_data)
                    stats["new"] = len(new_versions)
                    stats["updated"] = len(updated_versions)
                    
                    # 更新文件的当前版本信息
                    if version_data:
                        latest_version = max(version_data, key=lambda v: v.get("version_number", 0))
                        self._update_file_current_version(file_id, latest_version)
            
            logger.info(f"版本增量同步完成: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"版本增量同步失败: {str(e)}")
            return {"new": 0, "updated": 0, "deleted": 0, "errors": 1}
    
    def _update_file_current_version(self, file_id: str, latest_version_data: Dict[str, Any]):
        """更新文件的当前版本信息"""
        try:
            db = self.dal.connect()
            
            current_version_info = {
                "version_id": latest_version_data.get("_id"),
                "version_number": latest_version_data.get("version_number", 1),
                "file_size": latest_version_data.get("metadata", {}).get("file_size", 0),
                "storage_size": latest_version_data.get("metadata", {}).get("storage_size", 0),
                "mime_type": latest_version_data.get("metadata", {}).get("mime_type"),
                "create_time": latest_version_data.get("metadata", {}).get("create_time"),
                "create_user_id": latest_version_data.get("metadata", {}).get("create_user_id"),
                "create_user_name": latest_version_data.get("metadata", {}).get("create_user_name"),
                "urn": latest_version_data.get("urn"),
                "item_urn": latest_version_data.get("item_urn"),
                "storage_urn": latest_version_data.get("storage_urn"),
                "lineage_urn": latest_version_data.get("lineage_urn"),
                "review_state": latest_version_data.get("review_info", {}).get("review_state"),
                "review_info": latest_version_data.get("review_info", {})
            }
            
            # 更新版本摘要
            versions_summary = {
                "latest_version_number": latest_version_data.get("version_number", 1),
                "latest_version_time": latest_version_data.get("metadata", {}).get("create_time"),
                "has_review_states": bool(latest_version_data.get("review_info", {}).get("review_state"))
            }
            
            db.files.update_one(
                {"_id": file_id},
                {
                    "$set": {
                        "current_version": current_version_info,
                        "versions_summary.latest_version_number": versions_summary["latest_version_number"],
                        "versions_summary.latest_version_time": versions_summary["latest_version_time"],
                        "versions_summary.has_review_states": versions_summary["has_review_states"],
                        "updated_at": datetime.now()
                    }
                }
            )
            
        except Exception as e:
            logger.error(f"更新文件当前版本失败: {str(e)}")
    
    def update_sync_timestamp(self, project_id: str, sync_type: str = "incremental"):
        """更新同步时间戳"""
        try:
            now = datetime.now()
            
            # 更新项目同步信息
            self.dal.update_project_sync_status(project_id, "completed")
            
            # 记录同步任务
            db = self.dal.connect()
            sync_task = {
                "project_id": project_id,
                "task_type": sync_type,
                "task_status": "completed",
                "start_time": now,
                "end_time": now,
                "results": {
                    "sync_type": sync_type,
                    "completed_at": now
                }
            }
            
            db.sync_tasks.insert_one(sync_task)
            logger.info(f"更新同步时间戳: {project_id} - {sync_type}")
            
        except Exception as e:
            logger.error(f"更新同步时间戳失败: {str(e)}")

# 便利函数
def create_incremental_sync_manager() -> IncrementalSyncManager:
    """创建增量同步管理器"""
    return IncrementalSyncManager()

# 使用示例
INCREMENTAL_SYNC_EXAMPLES = """
# 增量同步使用示例

## 1. 基本增量同步
```python
from database.incremental_sync import create_incremental_sync_manager

# 创建增量同步管理器
sync_manager = create_incremental_sync_manager()

# 获取上次同步时间
project_id = "b.1eea4119-3553-4167-b93d-3a3d5d07d33d"
last_sync = sync_manager.get_last_sync_time(project_id)
print(f"上次同步时间: {last_sync}")

# 检测变更
changes = sync_manager.detect_changes(project_id)
print(f"检测到的变更: {changes}")
```

## 2. 文件夹增量同步
```python
# 假设从API获取了文件夹数据
api_folders_data = [
    {
        "id": "folder_id_1",
        "attributes": {
            "displayName": "新文件夹",
            "lastModifiedTime": "2024-11-04T10:00:00Z"
        }
    }
]

# 执行增量同步
result = sync_manager.incremental_sync_folders(project_id, api_folders_data)
print(f"文件夹同步结果: {result}")
```

## 3. 文件增量同步
```python
# 假设从API获取了文件数据
api_files_data = [
    {
        "id": "file_id_1",
        "attributes": {
            "displayName": "新文件.pdf",
            "lastModifiedTime": "2024-11-04T10:00:00Z"
        }
    }
]

# 执行增量同步
result = sync_manager.incremental_sync_files(project_id, api_files_data)
print(f"文件同步结果: {result}")
```

## 4. 版本增量同步
```python
# 为特定文件同步版本
file_id = "urn:adsk.wipprod:dm.lineage:xxx"
api_versions_data = [
    {
        "id": "version_id_1",
        "attributes": {
            "versionNumber": 2,
            "createTime": "2024-11-04T10:00:00Z"
        }
    }
]

result = sync_manager.incremental_sync_versions(project_id, file_id, api_versions_data)
print(f"版本同步结果: {result}")
```

## 5. 完整增量同步流程
```python
from datetime import datetime, timedelta

def perform_incremental_sync(project_id: str):
    sync_manager = create_incremental_sync_manager()
    
    # 1. 获取上次同步时间
    since = sync_manager.get_last_sync_time(project_id)
    print(f"从 {since} 开始增量同步")
    
    # 2. 从API获取变更数据（这里需要调用实际的API）
    # api_folders = get_folders_since(project_id, since)
    # api_files = get_files_since(project_id, since)
    
    # 3. 执行增量同步
    # folder_result = sync_manager.incremental_sync_folders(project_id, api_folders, since)
    # file_result = sync_manager.incremental_sync_files(project_id, api_files, since)
    
    # 4. 更新同步时间戳
    sync_manager.update_sync_timestamp(project_id, "incremental")
    
    print("增量同步完成")

# 执行增量同步
perform_incremental_sync("b.1eea4119-3553-4167-b93d-3a3d5d07d33d")
```
"""
