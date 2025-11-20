# -*- coding: utf-8 -*-
"""
数据访问层 (Data Access Layer)
提供对优化数据库结构的高级操作接口
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import DuplicateKeyError, BulkWriteError
from .mongodb_config import MongoDBConfig, get_collection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataAccessLayer:
    """数据访问层主类"""
    
    def __init__(self, db_config: MongoDBConfig = None):
        self.db_config = db_config or MongoDBConfig()
        self.database = None
        
    def connect(self):
        """连接数据库"""
        if not self.database:
            self.database = self.db_config.get_database()
        return self.database
    
    # ============================================================================
    # 项目相关操作
    # ============================================================================
    
    def create_or_update_project(self, project_data: Dict[str, Any]) -> bool:
        """创建或更新项目"""
        try:
            db = self.connect()
            project_id = project_data["_id"]
            
            # 添加时间戳
            now = datetime.now()
            if "_id" not in project_data or not db.projects.find_one({"_id": project_id}):
                project_data["created_at"] = now
            project_data["updated_at"] = now
            
            # 使用upsert操作
            result = db.projects.replace_one(
                {"_id": project_id},
                project_data,
                upsert=True
            )
            
            logger.info(f"项目 {project_id} {'更新' if result.matched_count > 0 else '创建'}成功")
            return True
            
        except Exception as e:
            logger.error(f"创建/更新项目失败: {str(e)}")
            return False
    
    def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """获取项目信息"""
        try:
            db = self.connect()
            return db.projects.find_one({"_id": project_id})
        except Exception as e:
            logger.error(f"获取项目信息失败: {str(e)}")
            return None
    
    def list_projects(self, limit: int = 100) -> List[Dict[str, Any]]:
        """列出所有项目"""
        try:
            db = self.connect()
            return list(db.projects.find().limit(limit).sort("updated_at", -1))
        except Exception as e:
            logger.error(f"列出项目失败: {str(e)}")
            return []
    
    def update_project_sync_status(self, project_id: str, status: str, 
                                 duration: float = None, error: str = None) -> bool:
        """更新项目同步状态"""
        try:
            import pytz
            # 統一使用中國時區
            china_tz = pytz.timezone('Asia/Shanghai')
            china_time = datetime.now(china_tz)
            
            db = self.connect()
            update_data = {
                "sync_info.sync_status": status,
                "sync_info.last_sync_time": china_time,
                "updated_at": china_time
            }
            
            if duration is not None:
                update_data["sync_info.sync_duration_seconds"] = duration
            if error:
                update_data["sync_info.sync_error"] = error
            
            result = db.projects.update_one(
                {"_id": project_id},
                {"$set": update_data}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"更新项目同步状态失败: {str(e)}")
            return False
    
    def clear_project_data(self, project_id: str) -> Dict[str, int]:
        """
        清除項目的所有相關數據（用於全量同步前的數據清理）
        
        Args:
            project_id: 項目ID
            
        Returns:
            清理結果統計字典
        """
        try:
            db = self.connect()
            logger.info(f"🧹 開始清除項目 {project_id} 的所有數據...")
            
            # 清除文件夾數據
            folders_result = db.folders.delete_many({"project_id": project_id})
            logger.info(f"  清除文件夾: {folders_result.deleted_count} 個")
            
            # 清除文件數據  
            files_result = db.files.delete_many({"project_id": project_id})
            logger.info(f"  清除文件: {files_result.deleted_count} 個")
            
            # 清除文件版本數據
            versions_result = db.file_versions.delete_many({"project_id": project_id})
            logger.info(f"  清除文件版本: {versions_result.deleted_count} 個")
            
            # 清除自定義屬性數據（如果存在）
            attributes_deleted = 0
            if "custom_attributes" in db.list_collection_names():
                attributes_result = db.custom_attributes.delete_many({"project_id": project_id})
                attributes_deleted = attributes_result.deleted_count
                logger.info(f"  清除自定義屬性: {attributes_deleted} 個")
            
            # 重置項目統計數據，但保留項目基本信息
            project_reset_result = db.projects.update_one(
                {"_id": project_id},
                {
                    "$unset": {
                        "statistics": "",
                        "sync_info.last_full_sync": ""
                    },
                    "$set": {
                        "sync_info.sync_status": "clearing_data",
                        "updated_at": datetime.now()
                    }
                }
            )
            
            clear_stats = {
                "folders_deleted": folders_result.deleted_count,
                "files_deleted": files_result.deleted_count, 
                "versions_deleted": versions_result.deleted_count,
                "attributes_deleted": attributes_deleted,
                "project_reset": 1 if project_reset_result.modified_count > 0 else 0
            }
            
            total_deleted = sum(clear_stats.values())
            logger.info(f"✅ 項目數據清理完成，共清除 {total_deleted} 條記錄")
            
            return clear_stats
            
        except Exception as e:
            logger.error(f"❌ 清除項目數據失敗: {str(e)}")
            raise Exception(f"清除項目數據失敗: {str(e)}")
    
    # ============================================================================
    # 文件夹相关操作
    # ============================================================================
    
    def create_or_update_folder(self, folder_data: Dict[str, Any]) -> bool:
        """创建或更新单个文件夹"""
        try:
            db = self.connect()
            folder_id = folder_data["_id"]
            
            # 添加时间戳
            now = datetime.now()
            if "_id" not in folder_data or not db.folders.find_one({"_id": folder_id}):
                folder_data["created_at"] = now
            folder_data["updated_at"] = now
            
            # 添加组合索引字段
            if "project_id" in folder_data and "path" in folder_data:
                folder_data["project_path"] = f"{folder_data['project_id']}#{folder_data['path']}"
            
            # 使用upsert操作
            result = db.folders.replace_one(
                {"_id": folder_id},
                folder_data,
                upsert=True
            )
            
            logger.info(f"文件夹 {folder_id} {'更新' if result.matched_count > 0 else '创建'}成功")
            return True
            
        except Exception as e:
            logger.error(f"创建/更新文件夹失败: {str(e)}")
            return False

    def batch_upsert_folders(self, folders_data: List[Dict[str, Any]]) -> Dict[str, int]:
        """批量插入或更新文件夹"""
        try:
            db = self.connect()
            
            if not folders_data:
                return {"inserted": 0, "updated": 0, "errors": 0}
            
            # 准备批量操作
            operations = []
            now = datetime.now()
            
            for folder_data in folders_data:
                folder_id = folder_data["_id"]
                
                # 添加时间戳和索引优化字段
                folder_data["updated_at"] = now
                if "created_at" not in folder_data:
                    folder_data["created_at"] = now
                
                # 添加组合索引字段
                folder_data["project_path"] = f"{folder_data['project_id']}#{folder_data['path']}"
                if folder_data.get("parent_id"):
                    parent_path = folder_data["path"].rsplit("/", 1)[0] if "/" in folder_data["path"] else ""
                    folder_data["parent_path"] = parent_path
                
                from pymongo import ReplaceOne
                operations.append(
                    ReplaceOne(
                        filter={"_id": folder_id},
                        replacement=folder_data,
                        upsert=True
                    )
                )
            
            # 执行批量操作
            result = db.folders.bulk_write(operations, ordered=False)
            
            stats = {
                "inserted": result.upserted_count,
                "updated": result.modified_count,
                "errors": 0
            }
            
            logger.info(f"批量文件夹操作完成: 插入 {stats['inserted']}, 更新 {stats['updated']}")
            return stats
            
        except BulkWriteError as e:
            logger.error(f"批量文件夹操作部分失败: {len(e.details['writeErrors'])} 个错误")
            return {"inserted": 0, "updated": 0, "errors": len(e.details['writeErrors'])}
        except Exception as e:
            logger.error(f"批量文件夹操作失败: {str(e)}")
            return {"inserted": 0, "updated": 0, "errors": len(folders_data)}
    
    def get_folders_by_project(self, project_id: str, parent_id: str = None, 
                              max_depth: int = None) -> List[Dict[str, Any]]:
        """获取项目的文件夹列表"""
        try:
            db = self.connect()
            
            # 构建查询条件
            query = {"project_id": project_id}
            if parent_id:
                query["parent_id"] = parent_id
            if max_depth is not None:
                query["depth"] = {"$lte": max_depth}
            
            return list(db.folders.find(query).sort("path", 1))
            
        except Exception as e:
            logger.error(f"获取项目文件夹失败: {str(e)}")
            return []
    
    def get_folder_tree(self, project_id: str, root_folder_id: str = None) -> List[Dict[str, Any]]:
        """获取文件夹树结构"""
        try:
            db = self.connect()
            
            # 构建聚合管道
            pipeline = [
                {"$match": {"project_id": project_id}},
                {"$sort": {"depth": 1, "path": 1}}
            ]
            
            if root_folder_id:
                pipeline[0]["$match"]["$or"] = [
                    {"_id": root_folder_id},
                    {"path": {"$regex": f"^{root_folder_id}/"}}
                ]
            
            folders = list(db.folders.aggregate(pipeline))
            
            # 构建树结构
            folder_map = {f["_id"]: f for f in folders}
            tree = []
            
            for folder in folders:
                folder["children"] = []
                parent_id = folder.get("parent_id")
                
                if parent_id and parent_id in folder_map:
                    folder_map[parent_id]["children"].append(folder)
                else:
                    tree.append(folder)
            
            return tree
            
        except Exception as e:
            logger.error(f"获取文件夹树失败: {str(e)}")
            return []
    
    def search_folders(self, project_id: str, search_text: str, limit: int = 50) -> List[Dict[str, Any]]:
        """搜索文件夹"""
        try:
            db = self.connect()
            
            # 使用正则表达式搜索
            query = {
                "project_id": project_id,
                "$or": [
                    {"name": {"$regex": search_text, "$options": "i"}},
                    {"display_name": {"$regex": search_text, "$options": "i"}},
                    {"path": {"$regex": search_text, "$options": "i"}}
                ]
            }
            
            return list(db.folders.find(query).limit(limit).sort("path", 1))
            
        except Exception as e:
            logger.error(f"搜索文件夹失败: {str(e)}")
            return []
    
    # ============================================================================
    # 文件相关操作
    # ============================================================================
    
    def create_or_update_file(self, file_data: Dict[str, Any]) -> bool:
        """创建或更新单个文件"""
        try:
            db = self.connect()
            file_id = file_data["_id"]
            
            # 添加时间戳
            now = datetime.now()
            if "_id" not in file_data or not db.files.find_one({"_id": file_id}):
                file_data["created_at"] = now
            file_data["updated_at"] = now
            
            # 添加组合索引字段
            if "project_id" in file_data and "folder_path" in file_data:
                file_data["project_folder"] = f"{file_data['project_id']}#{file_data['folder_path']}"
            
            # 添加小写文件名用于搜索
            if "name" in file_data:
                file_data["name_lower"] = file_data["name"].lower()
            
            # 使用upsert操作
            result = db.files.replace_one(
                {"_id": file_id},
                file_data,
                upsert=True
            )
            
            logger.info(f"文件 {file_id} {'更新' if result.matched_count > 0 else '创建'}成功")
            return True
            
        except Exception as e:
            logger.error(f"创建/更新文件失败: {str(e)}")
            return False

    def batch_upsert_files(self, files_data: List[Dict[str, Any]]) -> Dict[str, int]:
        """批量插入或更新文件"""
        try:
            db = self.connect()
            
            if not files_data:
                return {"inserted": 0, "updated": 0, "errors": 0}
            
            # 准备批量操作
            operations = []
            now = datetime.now()
            
            for file_data in files_data:
                file_id = file_data["_id"]
                
                # 添加时间戳和索引优化字段
                file_data["updated_at"] = now
                if "created_at" not in file_data:
                    file_data["created_at"] = now
                
                # 添加组合索引字段
                file_data["project_folder"] = f"{file_data['project_id']}#{file_data['folder_path']}"
                if file_data.get("file_info", {}).get("file_type"):
                    file_data["project_type"] = f"{file_data['project_id']}#{file_data['file_info']['file_type']}"
                
                # 添加小写文件名用于搜索
                file_data["name_lower"] = file_data["name"].lower()
                
                from pymongo import ReplaceOne
                operations.append(
                    ReplaceOne(
                        filter={"_id": file_id},
                        replacement=file_data,
                        upsert=True
                    )
                )
            
            # 执行批量操作
            result = db.files.bulk_write(operations, ordered=False)
            
            stats = {
                "inserted": result.upserted_count,
                "updated": result.modified_count,
                "errors": 0
            }
            
            logger.info(f"批量文件操作完成: 插入 {stats['inserted']}, 更新 {stats['updated']}")
            return stats
            
        except BulkWriteError as e:
            logger.error(f"批量文件操作部分失败: {len(e.details['writeErrors'])} 个错误")
            return {"inserted": 0, "updated": 0, "errors": len(e.details['writeErrors'])}
        except Exception as e:
            logger.error(f"批量文件操作失败: {str(e)}")
            return {"inserted": 0, "updated": 0, "errors": len(files_data)}
    
    def get_files_by_folder(self, project_id: str, folder_path: str = None, 
                           file_types: List[str] = None, limit: int = 1000) -> List[Dict[str, Any]]:
        """获取文件夹中的文件"""
        try:
            db = self.connect()
            
            # 构建查询条件
            query = {"project_id": project_id}
            if folder_path:
                query["folder_path"] = folder_path
            if file_types:
                query["file_info.file_type"] = {"$in": file_types}
            
            return list(db.files.find(query).limit(limit).sort("name", 1))
            
        except Exception as e:
            logger.error(f"获取文件夹文件失败: {str(e)}")
            return []
    
    def search_files(self, project_id: str, search_text: str = None, 
                    file_types: List[str] = None, review_states: List[str] = None,
                    limit: int = 100) -> List[Dict[str, Any]]:
        """搜索文件"""
        try:
            db = self.connect()
            
            # 构建查询条件
            query = {"project_id": project_id}
            
            if search_text:
                # 使用正则表达式搜索，避免文本索引问题
                query["$or"] = [
                    {"name_lower": {"$regex": search_text.lower()}},
                    {"display_name": {"$regex": search_text, "$options": "i"}},
                    {"full_path": {"$regex": search_text, "$options": "i"}}
                ]
            
            if file_types:
                query["file_info.file_type"] = {"$in": file_types}
            
            if review_states:
                query["current_version.review_state"] = {"$in": review_states}
            
            return list(db.files.find(query).limit(limit).sort("metadata.last_modified_time", -1))
            
        except Exception as e:
            logger.error(f"搜索文件失败: {str(e)}")
            return []
    
    def get_files_by_review_state(self, project_id: str, review_state: str, 
                                 limit: int = 100) -> List[Dict[str, Any]]:
        """根据review状态获取文件"""
        try:
            db = self.connect()
            
            query = {
                "project_id": project_id,
                "current_version.review_state": review_state
            }
            
            return list(db.files.find(query).limit(limit).sort("metadata.last_modified_time", -1))
            
        except Exception as e:
            logger.error(f"根据review状态获取文件失败: {str(e)}")
            return []
    
    # ============================================================================
    # 文件版本相关操作
    # ============================================================================
    
    def create_or_update_file_version(self, version_data: Dict[str, Any]) -> bool:
        """创建或更新单个文件版本"""
        try:
            db = self.connect()
            version_id = version_data["_id"]
            
            # 添加时间戳
            now = datetime.now()
            if "_id" not in version_data or not db.file_versions.find_one({"_id": version_id}):
                version_data["created_at"] = now
            version_data["updated_at"] = now
            
            # 使用upsert操作
            result = db.file_versions.replace_one(
                {"_id": version_id},
                version_data,
                upsert=True
            )
            
            logger.debug(f"文件版本 {version_id} {'更新' if result.matched_count > 0 else '创建'}成功")
            return True
            
        except Exception as e:
            logger.error(f"创建/更新文件版本失败: {str(e)}")
            return False

    def batch_upsert_file_versions(self, versions_data: List[Dict[str, Any]]) -> Dict[str, int]:
        """批量插入或更新文件版本"""
        try:
            db = self.connect()
            
            if not versions_data:
                return {"inserted": 0, "updated": 0, "errors": 0}
            
            # 准备批量操作
            operations = []
            now = datetime.now()
            
            for version_data in versions_data:
                version_id = version_data["_id"]
                
                # 添加时间戳
                version_data["updated_at"] = now
                if "created_at" not in version_data:
                    version_data["created_at"] = now
                
                from pymongo import ReplaceOne
                operations.append(
                    ReplaceOne(
                        filter={"_id": version_id},
                        replacement=version_data,
                        upsert=True
                    )
                )
            
            # 执行批量操作
            result = db.file_versions.bulk_write(operations, ordered=False)
            
            stats = {
                "inserted": result.upserted_count,
                "updated": result.modified_count,
                "errors": 0
            }
            
            logger.info(f"批量版本操作完成: 插入 {stats['inserted']}, 更新 {stats['updated']}")
            return stats
            
        except BulkWriteError as e:
            logger.error(f"批量版本操作部分失败: {len(e.details['writeErrors'])} 个错误")
            return {"inserted": 0, "updated": 0, "errors": len(e.details['writeErrors'])}
        except Exception as e:
            logger.error(f"批量版本操作失败: {str(e)}")
            return {"inserted": 0, "updated": 0, "errors": len(versions_data)}
    
    def get_file_versions(self, file_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """获取文件的所有版本"""
        try:
            db = self.connect()
            
            return list(db.file_versions.find(
                {"file_id": file_id}
            ).limit(limit).sort("version_number", -1))
            
        except Exception as e:
            logger.error(f"获取文件版本失败: {str(e)}")
            return []
    
    def get_version_by_urn(self, urn: str) -> Optional[Dict[str, Any]]:
        """根据URN获取版本信息"""
        try:
            db = self.connect()
            
            # 尝试不同的URN字段
            query = {"$or": [
                {"urn": urn},
                {"item_urn": urn},
                {"storage_urn": urn},
                {"lineage_urn": urn}
            ]}
            
            return db.file_versions.find_one(query)
            
        except Exception as e:
            logger.error(f"根据URN获取版本失败: {str(e)}")
            return None
    
    # ============================================================================
    # 简化的同步历史记录操作
    # ============================================================================
    
    def create_sync_history_record(self, project_id: str, sync_type: str, results: dict) -> bool:
        """创建简化的同步历史记录 - 只记录成功的同步"""
        try:
            from .simplified_sync_schema import create_sync_record
            
            db = self.connect()
            record = create_sync_record(project_id, sync_type, results)
            
            result = db.sync_history.insert_one(record)
            logger.info(f"创建同步历史记录成功: {result.inserted_id}")
            return True
            
        except Exception as e:
            logger.error(f"创建同步历史记录失败: {str(e)}")
            return False
    
    def get_sync_history(self, project_id: str, limit: int = 20, offset: int = 0, 
                        sync_type: str = None) -> List[Dict[str, Any]]:
        """获取项目同步历史记录"""
        try:
            from .simplified_sync_schema import format_china_time
            
            db = self.connect()
            
            # 构建查询条件
            query = {"project_id": project_id}
            if sync_type:
                query["sync_type"] = sync_type
            
            # 查询记录
            records = list(db.sync_history.find(query)
                          .sort("sync_time", -1)
                          .skip(offset)
                          .limit(limit))
            
            # 格式化时间显示
            for record in records:
                if "_id" in record:
                    record["_id"] = str(record["_id"])
                
                # 格式化时间为中国时间字符串
                if "sync_time" in record and record["sync_time"]:
                    record["sync_time_formatted"] = format_china_time(record["sync_time"])
                if "created_at" in record and record["created_at"]:
                    record["created_at_formatted"] = format_china_time(record["created_at"])
            
            return records
            
        except Exception as e:
            logger.error(f"获取同步历史记录失败: {str(e)}")
            return []
    
    def get_sync_history_count(self, project_id: str, sync_type: str = None) -> int:
        """获取同步历史记录总数"""
        try:
            db = self.connect()
            
            query = {"project_id": project_id}
            if sync_type:
                query["sync_type"] = sync_type
            
            return db.sync_history.count_documents(query)
            
        except Exception as e:
            logger.error(f"获取同步历史记录总数失败: {str(e)}")
            return 0

    # ============================================================================
    # 同步任务相关操作（保留用于向后兼容）
    # ============================================================================
    
    def create_sync_task(self, task_data: Dict[str, Any]) -> Optional[str]:
        """创建同步任务"""
        try:
            db = self.connect()
            
            task_data["created_at"] = datetime.now()
            task_data["updated_at"] = datetime.now()
            
            result = db.sync_tasks.insert_one(task_data)
            logger.info(f"创建同步任务成功: {result.inserted_id}")
            return str(result.inserted_id)
            
        except Exception as e:
            logger.error(f"创建同步任务失败: {str(e)}")
            return None
    
    def update_sync_task(self, task_id: str, update_data: Dict[str, Any]) -> bool:
        """更新同步任务"""
        try:
            db = self.connect()
            
            update_data["updated_at"] = datetime.now()
            
            result = db.sync_tasks.update_one(
                {"_id": task_id},
                {"$set": update_data}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"更新同步任务失败: {str(e)}")
            return False
    
    def update_sync_task_status(self, task_id: str, status: str, results: Dict[str, Any] = None, duration: float = None) -> bool:
        """更新同步任务状态"""
        try:
            db = self.connect()
            
            update_data = {
                "task_status": status,
                "updated_at": datetime.now()
            }
            
            if results:
                update_data["results"] = results
            
            if duration is not None:
                update_data["duration_seconds"] = duration
                update_data["end_time"] = datetime.now()
            
            result = db.sync_tasks.update_one(
                {"_id": task_id},
                {"$set": update_data}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"更新同步任务状态失败: {str(e)}")
            return False
    
    def get_sync_tasks(self, project_id: str = None, status: str = None, 
                      limit: int = 50) -> List[Dict[str, Any]]:
        """获取同步任务列表"""
        try:
            db = self.connect()
            
            query = {}
            if project_id:
                query["project_id"] = project_id
            if status:
                query["task_status"] = status
            
            return list(db.sync_tasks.find(query).limit(limit).sort("start_time", -1))
            
        except Exception as e:
            logger.error(f"获取同步任务失败: {str(e)}")
            return []
    
    # ============================================================================
    # 统计和分析
    # ============================================================================
    
    def update_project_statistics(self, project_id: str, stats: Dict[str, Any]) -> bool:
        """更新项目统计信息"""
        try:
            db = self.connect()
            
            result = db.projects.update_one(
                {"_id": project_id},
                {"$set": {
                    "statistics": stats,
                    "updated_at": datetime.now()
                }}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"更新项目统计失败: {str(e)}")
            return False

    def get_project_statistics(self, project_id: str) -> Dict[str, Any]:
        """获取项目统计信息"""
        try:
            db = self.connect()
            
            # 文件夹统计
            folder_stats = db.folders.aggregate([
                {"$match": {"project_id": project_id}},
                {"$group": {
                    "_id": None,
                    "total_folders": {"$sum": 1},
                    "max_depth": {"$max": "$depth"},
                    "avg_children": {"$avg": "$children_stats.direct_folders"}
                }}
            ])
            folder_stats = list(folder_stats)
            folder_stats = folder_stats[0] if folder_stats else {}
            
            # 文件统计
            file_stats = db.files.aggregate([
                {"$match": {"project_id": project_id}},
                {"$group": {
                    "_id": None,
                    "total_files": {"$sum": 1},
                    "total_size": {"$sum": "$current_version.file_size"},
                    "avg_file_size": {"$avg": "$current_version.file_size"}
                }}
            ])
            file_stats = list(file_stats)
            file_stats = file_stats[0] if file_stats else {}
            
            # 文件类型统计
            file_type_stats = db.files.aggregate([
                {"$match": {"project_id": project_id}},
                {"$group": {
                    "_id": "$file_info.file_type",
                    "count": {"$sum": 1},
                    "total_size": {"$sum": "$current_version.file_size"}
                }},
                {"$sort": {"count": -1}}
            ])
            file_type_stats = list(file_type_stats)
            
            # Review状态统计
            review_stats = db.files.aggregate([
                {"$match": {"project_id": project_id}},
                {"$group": {
                    "_id": "$current_version.review_state",
                    "count": {"$sum": 1}
                }},
                {"$sort": {"count": -1}}
            ])
            review_stats = list(review_stats)
            
            return {
                "project_id": project_id,
                "folders": {
                    "total_count": folder_stats.get("total_folders", 0),
                    "max_depth": folder_stats.get("max_depth", 0),
                    "avg_children": folder_stats.get("avg_children", 0)
                },
                "files": {
                    "total_count": file_stats.get("total_files", 0),
                    "total_size_bytes": file_stats.get("total_size", 0),
                    "avg_file_size_bytes": file_stats.get("avg_file_size", 0)
                },
                "file_types": {item["_id"]: item["count"] for item in file_type_stats if item["_id"]},
                "review_states": {item["_id"]: item["count"] for item in review_stats if item["_id"]},
                "generated_at": datetime.now()
            }
            
        except Exception as e:
            logger.error(f"获取项目统计失败: {str(e)}")
            return {}
    
    def get_recent_sync_tasks(self, project_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """获取项目最近的同步任务"""
        try:
            db = self.connect()
            query = {"project_id": project_id}
            tasks = list(db.sync_tasks.find(query).limit(limit).sort("start_time", -1))
            
            # 转换ObjectId和日期时间为字符串
            for task in tasks:
                if "_id" in task:
                    task["_id"] = str(task["_id"])
                for field in ["start_time", "end_time", "created_at", "updated_at"]:
                    if field in task and task[field]:
                        task[field] = task[field].isoformat() if hasattr(task[field], 'isoformat') else task[field]
            
            return tasks
            
        except Exception as e:
            logger.error(f"获取最近同步任务失败: {str(e)}")
            return []
    
    def update_sync_task_progress(self, task_id: str, progress_data: dict) -> bool:
        """更新同步任务进度"""
        try:
            from bson import ObjectId
            db = self.connect()
            
            update_data = {
                "progress": progress_data,
                "updated_at": datetime.now()
            }
            
            # 将字符串ID转换为ObjectId
            object_id = ObjectId(task_id) if isinstance(task_id, str) else task_id
            
            result = db.sync_tasks.update_one(
                {"_id": object_id},
                {"$set": update_data}
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"更新同步任务进度失败: {str(e)}")
            return False

    def get_sync_task_progress(self, task_id: str) -> Optional[Dict[str, Any]]:
        """获取同步任务进度"""
        try:
            from bson import ObjectId
            db = self.connect()
            
            # 将字符串ID转换为ObjectId
            object_id = ObjectId(task_id) if isinstance(task_id, str) else task_id
            task = db.sync_tasks.find_one({"_id": object_id})
            
            if task:
                # 转换ObjectId为字符串
                if "_id" in task:
                    task["_id"] = str(task["_id"])
                
                # 转换日期时间
                for field in ["start_time", "end_time", "created_at", "updated_at"]:
                    if field in task and task[field]:
                        task[field] = task[field].isoformat() if hasattr(task[field], 'isoformat') else task[field]
                
                return task
            
            return None
            
        except Exception as e:
            logger.error(f"获取同步任务进度失败: {str(e)}")
            return None

# 全局数据访问层实例
dal = DataAccessLayer()

# 便利函数
def get_dal() -> DataAccessLayer:
    """获取数据访问层实例"""
    return dal
