# -*- coding: utf-8 -*-
"""
数据同步策略设计文档
基于方案1（优化的单次遍历）+ 方案2（优化的数据库设计）
定义如何高效地将ACC API数据同步到优化的MongoDB结构中
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import logging
import pytz

logger = logging.getLogger(__name__)

# ============================================================================
# 同步策略枚举
# ============================================================================

class SyncType(Enum):
    """同步类型"""
    FULL_SYNC = "full_sync"              # 完全同步
    INCREMENTAL_SYNC = "incremental_sync" # 增量同步
    FOLDER_SYNC = "folder_sync"          # 文件夹同步
    FILE_SYNC = "file_sync"              # 文件同步
    VERSION_SYNC = "version_sync"        # 版本同步
    METADATA_SYNC = "metadata_sync"      # 元数据同步

class SyncPriority(Enum):
    """同步优先级"""
    HIGH = "high"      # 高优先级
    MEDIUM = "medium"  # 中优先级
    LOW = "low"        # 低优先级

class SyncStatus(Enum):
    """同步状态"""
    PENDING = "pending"      # 等待中
    RUNNING = "running"      # 运行中
    COMPLETED = "completed"  # 已完成
    FAILED = "failed"        # 失败
    CANCELLED = "cancelled"  # 已取消

# ============================================================================
# 数据同步策略配置
# ============================================================================

SYNC_STRATEGY_CONFIG = {
    # 批量处理配置
    "batch_processing": {
        "folder_batch_size": 50,        # 文件夹批量大小
        "file_batch_size": 100,         # 文件批量大小
        "version_batch_size": 200,      # 版本批量大小
        "parallel_workers": 8,          # 并行工作线程数
        "api_rate_limit": 10,           # API调用速率限制（每秒）
        "batch_delay_ms": 100           # 批次间延迟（毫秒）
    },
    
    # 同步间隔配置
    "sync_intervals": {
        "full_sync": timedelta(days=7),      # 完全同步：每周
        "incremental_sync": timedelta(hours=6), # 增量同步：每6小时
        "metadata_sync": timedelta(hours=1),    # 元数据同步：每小时
        "version_sync": timedelta(minutes=30)   # 版本同步：每30分钟
    },
    
    # 重试配置
    "retry_config": {
        "max_retries": 3,               # 最大重试次数
        "retry_delay_base": 2,          # 重试延迟基数（秒）
        "retry_delay_multiplier": 2,    # 重试延迟倍数
        "timeout_seconds": 300          # 超时时间（秒）
    },
    
    # 数据保留配置
    "data_retention": {
        "sync_task_history_days": 30,   # 同步任务历史保留天数
        "error_log_days": 7,            # 错误日志保留天数
        "version_history_limit": 100    # 版本历史限制
    }
}

# ============================================================================
# 数据转换映射
# ============================================================================

class DataTransformer:
    """数据转换器 - 将ACC API数据转换为优化的数据库格式"""
    
    @staticmethod
    def transform_project_data(api_data: Dict[str, Any]) -> Dict[str, Any]:
        """转换项目数据"""
        return {
            "id": api_data.get("id"),
            "name": api_data.get("attributes", {}).get("name", "Unknown"),
            "description": api_data.get("attributes", {}).get("description", ""),
            "hub_id": api_data.get("relationships", {}).get("hub", {}).get("data", {}).get("id"),
            "account_id": api_data.get("relationships", {}).get("account", {}).get("data", {}).get("id"),
            "status": "active",
            
            "sync_info": {
                "last_sync_time": datetime.now(),
                "sync_status": "completed",
                "sync_duration_seconds": 0.0,
                "sync_error": None,
                "sync_version": "1.0.0"
            },
            
            "statistics": {
                "total_folders": 0,
                "total_files": 0,
                "total_size_bytes": 0,
                "max_depth": 0,
                "file_types_count": {},
                "last_calculated": datetime.now()
            },
            
            "metadata": {
                "create_time": api_data.get("attributes", {}).get("createTime"),
                "create_user_id": api_data.get("attributes", {}).get("createUserId"),
                "create_user_name": api_data.get("attributes", {}).get("createUserName"),
                "last_modified_time": api_data.get("attributes", {}).get("lastModifiedTime"),
                "last_modified_user_id": api_data.get("attributes", {}).get("lastModifiedUserId"),
                "last_modified_user_name": api_data.get("attributes", {}).get("lastModifiedUserName")
            }
        }
    
    @staticmethod
    def transform_folder_data(api_data: Dict[str, Any], project_id: str, 
                            parent_id: str = None, path: str = "", depth: int = 0) -> Dict[str, Any]:
        """转换文件夹数据"""
        attributes = api_data.get("attributes", {})
        folder_name = attributes.get("displayName", attributes.get("name", "Unknown"))
        
        # 构建路径
        if path and path != "Project Files":
            full_path = f"{path}/{folder_name}"
        else:
            full_path = folder_name
        
        path_segments = full_path.split("/") if full_path else []
        
        return {
            "id": api_data.get("id"),
            "project_id": project_id,
            "name": folder_name,
            "display_name": folder_name,
            "parent_id": parent_id,
            
            "path": full_path,
            "path_segments": path_segments,
            "depth": depth,
            
            # Direct fields for PostgreSQL (not in metadata JSONB)
            "create_time": DataTransformer._parse_datetime(attributes.get("createTime")),
            "create_user_id": attributes.get("createUserId"),
            "create_user_name": attributes.get("createUserName"),
            "last_modified_time": DataTransformer._parse_datetime(attributes.get("lastModifiedTime")),
            "last_modified_user_id": attributes.get("lastModifiedUserId"),
            "last_modified_user_name": attributes.get("lastModifiedUserName"),
            "last_modified_time_rollup": DataTransformer._parse_datetime(attributes.get("lastModifiedTimeRollup")),
            "object_count": attributes.get("objectCount", 0),
            "total_size": attributes.get("size", 0),
            "hidden": attributes.get("hidden", False),
            
            "metadata": {
                "display_name": folder_name,
                "path_attr": attributes.get("path"),
                "original_attributes": attributes
            },
            
            "extension": attributes.get("extension", {}),
            
            "custom_attribute_definitions": {
                "has_definitions": False,
                "definitions": {},
                "total_count": 0,
                "last_sync_time": None
            },
            
            "children_stats": {
                "direct_folders": 0,
                "direct_files": 0,
                "total_folders": 0,
                "total_files": 0,
                "total_size": 0
            },
            
            "sync_info": {
                "sync_status": "completed",
                "api_source": "data_management_api"
            }
        }
    
    @staticmethod
    def transform_file_data(api_data: Dict[str, Any], project_id: str, 
                          parent_folder_id: str, folder_path: str, depth: int = 0) -> Dict[str, Any]:
        """转换文件数据"""
        attributes = api_data.get("attributes", {})
        file_name = attributes.get("displayName", attributes.get("name", "Unknown"))
        
        # 构建完整路径
        full_path = f"{folder_path}/{file_name}" if folder_path else file_name
        path_segments = full_path.split("/") if full_path else []
        
        # 提取文件类型
        extension_data = attributes.get("extension", {})
        file_type = DataTransformer._extract_file_type(extension_data)
        
        # Extract URN information from relationships
        relationships = api_data.get("relationships", {})
        tip_version = relationships.get("tip", {}).get("data", {})
        
        return {
            "id": api_data.get("id"),
            "project_id": project_id,
            "name": file_name,
            "display_name": file_name,
            "parent_folder_id": parent_folder_id,
            
            "folder_path": folder_path,
            "full_path": full_path,
            "path_segments": path_segments,
            "depth": depth,
            
            # URN information for versions and custom attributes
            "file_urn": api_data.get("id"),  # Item URN
            "tip_version_urn": tip_version.get("id") if tip_version else None,
            "storage_location": attributes.get("storageLocation"),
            
            # Direct fields for PostgreSQL (not in metadata JSONB)
            "create_time": DataTransformer._parse_datetime(attributes.get("createTime")),
            "create_user_id": attributes.get("createUserId"),
            "create_user_name": attributes.get("createUserName"),
            "last_modified_time": DataTransformer._parse_datetime(attributes.get("lastModifiedTime")),
            "last_modified_user_id": attributes.get("lastModifiedUserId"),
            "last_modified_user_name": attributes.get("lastModifiedUserName"),
            "file_size": attributes.get("size", 0),
            "file_type": file_type,
            "hidden": attributes.get("hidden", False),
            "reserved": attributes.get("reserved", False),
            "reserved_time": DataTransformer._parse_datetime(attributes.get("reservedTime")),
            "reserved_user_id": attributes.get("reservedUserId"),
            "reserved_user_name": attributes.get("reservedUserName"),
            
            "metadata": {
                "display_name": file_name,
                "original_attributes": attributes
            },
            
            "file_info": {
                "extension": extension_data,
                "file_type": file_type,
                "mime_type": None,  # 将从版本信息中获取
                "category": DataTransformer._categorize_file_type(file_type)
            },
            
            "current_version": {
                "version_id": None,
                "version_number": 1,
                "file_size": 0,
                "storage_size": 0,
                "mime_type": None,
                "create_time": None,
                "create_user_id": None,
                "create_user_name": None,
                "urn": None,
                "item_urn": None,
                "storage_urn": None,
                "lineage_urn": None,
                "review_state": None,
                "review_info": {}
            },
            
            "versions_summary": {
                "total_versions": 0,
                "latest_version_number": 1,
                "first_version_time": None,
                "latest_version_time": None,
                "has_review_states": False
            },
            
            "custom_attributes": {
                "has_attributes": False,
                "attributes": {},
                "total_count": 0,
                "last_sync_time": None
            },
            
            "sync_info": {
                "sync_status": "completed",
                "api_source": "data_management_api",
                "versions_synced": False
            }
        }
    
    @staticmethod
    def transform_version_data(api_data: Dict[str, Any], file_id: str, project_id: str) -> Dict[str, Any]:
        """转换版本数据"""
        attributes = api_data.get("attributes", {})
        
        # 提取URN信息
        version_urn = api_data.get("id")
        item_urn = api_data.get("relationships", {}).get("item", {}).get("data", {}).get("id")
        storage_urn = api_data.get("relationships", {}).get("storage", {}).get("data", {}).get("id")
        lineage_urn = api_data.get("relationships", {}).get("derivatives", {}).get("data", {}).get("id")
        
        # 提取review信息
        extension_data = attributes.get("extension", {}).get("data", {})
        review_state = extension_data.get("reviewState")
        
        return {
            "_id": version_urn,
            "file_id": file_id,
            "project_id": project_id,
            "version_number": attributes.get("versionNumber", 1),
            
            "urn": version_urn,
            "item_urn": item_urn,
            "storage_urn": storage_urn,
            "lineage_urn": lineage_urn,
            
            "metadata": {
                "display_name": attributes.get("displayName", "Unknown"),
                "create_time": DataTransformer._parse_datetime(attributes.get("createTime")),
                "create_user_id": attributes.get("createUserId"),
                "create_user_name": attributes.get("createUserName"),
                "last_modified_time": DataTransformer._parse_datetime(attributes.get("lastModifiedTime")),
                "last_modified_user_id": attributes.get("lastModifiedUserId"),
                "last_modified_user_name": attributes.get("lastModifiedUserName"),
                "file_size": attributes.get("storageSize", 0) or attributes.get("fileSize", 0),
                "storage_size": attributes.get("storageSize", 0),
                "mime_type": attributes.get("mimeType")
            },
            
            "review_info": {
                "review_state": review_state,
                "approval_status": extension_data.get("approvalStatus", {}),
                "review_workflow_id": extension_data.get("reviewWorkflowId"),
                "review_step": extension_data.get("reviewStep"),
                "reviewers": extension_data.get("reviewers", [])
            },
            
            "extension": attributes.get("extension", {}),
            
            "custom_attributes": {
                "has_attributes": False,
                "attributes": {},
                "last_sync_time": None
            },
            
            "download_info": {
                "download_url": attributes.get("downloadUrl"),
                "storage_location": attributes.get("storageLocation"),
                "derivatives": {},
                "last_checked": None
            },
            
            "sync_info": {
                "sync_status": "completed",
                "api_source": "data_management_api"
            }
        }
    
    @staticmethod
    def _parse_datetime(date_string: str) -> Optional[datetime]:
        """解析日期时间字符串并转换为北京时间"""
        if not date_string:
            return None
        try:
            # 北京时区
            beijing_tz = pytz.timezone('Asia/Shanghai')
            
            # 尝试不同的日期格式
            formats = [
                "%Y-%m-%dT%H:%M:%S.%fZ",      # 标准微秒格式
                "%Y-%m-%dT%H:%M:%S.0000000Z", # 7位小数格式 (ACC API常用)
                "%Y-%m-%dT%H:%M:%SZ",         # 无微秒格式
                "%Y-%m-%dT%H:%M:%S+0000",     # 带时区格式
                "%Y-%m-%dT%H:%M:%S",          # 简单格式
                "%Y-%m-%d %H:%M:%S"           # 空格分隔格式
            ]
            
            parsed_dt = None
            
            # 特殊处理7位小数的格式
            if ".0000000Z" in date_string:
                # 将7位小数转换为6位小数（Python支持的最大微秒精度）
                date_string_fixed = date_string.replace(".0000000Z", ".000000Z")
                try:
                    parsed_dt = datetime.strptime(date_string_fixed, "%Y-%m-%dT%H:%M:%S.%fZ")
                except ValueError:
                    pass
            
            # 如果特殊处理失败，尝试其他格式
            if not parsed_dt:
                for fmt in formats:
                    try:
                        parsed_dt = datetime.strptime(date_string, fmt)
                        break
                    except ValueError:
                        continue
            
            if parsed_dt:
                # 如果解析成功，假设输入是UTC时间，转换为北京时间
                if parsed_dt.tzinfo is None:
                    # 添加UTC时区信息
                    parsed_dt = parsed_dt.replace(tzinfo=pytz.UTC)
                
                # 转换为北京时间
                beijing_dt = parsed_dt.astimezone(beijing_tz)
                
                # 返回naive datetime（去掉时区信息，但时间已经是北京时间）
                return beijing_dt.replace(tzinfo=None)
            
            logger.warning(f"无法解析日期时间: {date_string}")
            return None
            
        except Exception as e:
            logger.error(f"解析日期时间出错: {str(e)}")
            return None
    
    @staticmethod
    def _extract_file_type(extension_data: Dict[str, Any]) -> str:
        """提取文件类型"""
        if not extension_data:
            return "unknown"
        
        # 尝试从不同字段提取文件类型
        file_type = extension_data.get("type", "").lower()
        if file_type:
            return file_type
        
        # 从版本信息中提取
        version_data = extension_data.get("version", {})
        if version_data:
            file_type = version_data.get("type", "").lower()
            if file_type:
                return file_type
        
        return "unknown"
    
    @staticmethod
    def _categorize_file_type(file_type: str) -> str:
        """文件类型分类"""
        if not file_type or file_type == "unknown":
            return "other"
        
        # 定义文件类型分类
        categories = {
            "drawing": ["dwg", "dxf", "dwf", "dwfx"],
            "model": ["rvt", "rfa", "rte", "rft", "3dm", "skp", "ifc"],
            "document": ["pdf", "doc", "docx", "txt", "rtf"],
            "spreadsheet": ["xls", "xlsx", "csv"],
            "presentation": ["ppt", "pptx"],
            "image": ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "svg"],
            "cad": ["step", "stp", "iges", "igs", "sat"],
            "archive": ["zip", "rar", "7z", "tar", "gz"]
        }
        
        file_type_lower = file_type.lower()
        for category, types in categories.items():
            if file_type_lower in types:
                return category
        
        return "other"

# ============================================================================
# 同步策略实现
# ============================================================================

class SyncStrategy:
    """同步策略基类"""
    
    def __init__(self, sync_type: SyncType, priority: SyncPriority = SyncPriority.MEDIUM):
        self.sync_type = sync_type
        self.priority = priority
        self.status = SyncStatus.PENDING
        self.start_time = None
        self.end_time = None
        self.error_message = None
        self.progress = 0.0
        
    def execute(self, **kwargs) -> bool:
        """执行同步策略"""
        raise NotImplementedError("子类必须实现execute方法")
    
    def validate_parameters(self, **kwargs) -> bool:
        """验证参数"""
        return True
    
    def estimate_duration(self, **kwargs) -> timedelta:
        """估算执行时间"""
        return timedelta(minutes=10)  # 默认估算
    
    def get_progress(self) -> float:
        """获取进度百分比"""
        return self.progress

class FullSyncStrategy(SyncStrategy):
    """完全同步策略"""
    
    def __init__(self):
        super().__init__(SyncType.FULL_SYNC, SyncPriority.HIGH)
    
    def execute(self, project_id: str, **kwargs) -> bool:
        """执行完全同步"""
        try:
            self.status = SyncStatus.RUNNING
            self.start_time = datetime.now()
            
            # 1. 同步项目基本信息 (5%)
            self.progress = 5.0
            
            # 2. 获取完整文件夹结构 (20%)
            self.progress = 20.0
            
            # 3. 批量同步文件夹数据 (40%)
            self.progress = 40.0
            
            # 4. 批量同步文件数据 (70%)
            self.progress = 70.0
            
            # 5. 同步版本信息 (90%)
            self.progress = 90.0
            
            # 6. 更新统计信息 (100%)
            self.progress = 100.0
            
            self.status = SyncStatus.COMPLETED
            self.end_time = datetime.now()
            return True
            
        except Exception as e:
            self.status = SyncStatus.FAILED
            self.error_message = str(e)
            self.end_time = datetime.now()
            logger.error(f"完全同步失败: {str(e)}")
            return False
    
    def estimate_duration(self, **kwargs) -> timedelta:
        """估算完全同步时间"""
        # 根据项目大小估算
        estimated_folders = kwargs.get("estimated_folders", 1000)
        estimated_files = kwargs.get("estimated_files", 10000)
        
        # 基础时间 + 文件夹时间 + 文件时间
        base_time = 60  # 1分钟基础时间
        folder_time = estimated_folders * 0.1  # 每个文件夹0.1秒
        file_time = estimated_files * 0.05     # 每个文件0.05秒
        
        total_seconds = base_time + folder_time + file_time
        return timedelta(seconds=total_seconds)

class IncrementalSyncStrategy(SyncStrategy):
    """增量同步策略"""
    
    def __init__(self):
        super().__init__(SyncType.INCREMENTAL_SYNC, SyncPriority.MEDIUM)
    
    def execute(self, project_id: str, since: datetime = None, **kwargs) -> bool:
        """执行增量同步"""
        try:
            self.status = SyncStatus.RUNNING
            self.start_time = datetime.now()
            
            # 如果没有指定时间，使用上次同步时间
            if not since:
                since = datetime.now() - timedelta(hours=6)
            
            # 1. 检查项目变更 (10%)
            self.progress = 10.0
            
            # 2. 同步变更的文件夹 (40%)
            self.progress = 40.0
            
            # 3. 同步变更的文件 (70%)
            self.progress = 70.0
            
            # 4. 同步新版本 (90%)
            self.progress = 90.0
            
            # 5. 更新统计 (100%)
            self.progress = 100.0
            
            self.status = SyncStatus.COMPLETED
            self.end_time = datetime.now()
            return True
            
        except Exception as e:
            self.status = SyncStatus.FAILED
            self.error_message = str(e)
            self.end_time = datetime.now()
            logger.error(f"增量同步失败: {str(e)}")
            return False

# ============================================================================
# 同步管理器
# ============================================================================

class SyncManager:
    """同步管理器"""
    
    def __init__(self):
        self.active_syncs = {}
        self.sync_history = []
        
    def create_sync_task(self, strategy: SyncStrategy, **parameters) -> str:
        """创建同步任务"""
        task_id = f"{strategy.sync_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        task_data = {
            "task_id": task_id,
            "strategy": strategy,
            "parameters": parameters,
            "created_at": datetime.now(),
            "status": SyncStatus.PENDING
        }
        
        self.active_syncs[task_id] = task_data
        return task_id
    
    def execute_sync(self, task_id: str) -> bool:
        """执行同步任务"""
        if task_id not in self.active_syncs:
            logger.error(f"同步任务不存在: {task_id}")
            return False
        
        task = self.active_syncs[task_id]
        strategy = task["strategy"]
        parameters = task["parameters"]
        
        try:
            # 验证参数
            if not strategy.validate_parameters(**parameters):
                logger.error(f"同步任务参数验证失败: {task_id}")
                return False
            
            # 执行同步
            success = strategy.execute(**parameters)
            
            # 更新任务状态
            task["status"] = strategy.status
            task["completed_at"] = datetime.now()
            
            # 移动到历史记录
            self.sync_history.append(task)
            del self.active_syncs[task_id]
            
            return success
            
        except Exception as e:
            logger.error(f"执行同步任务失败: {task_id}, {str(e)}")
            task["status"] = SyncStatus.FAILED
            task["error"] = str(e)
            return False
    
    def get_sync_status(self, task_id: str) -> Dict[str, Any]:
        """获取同步状态"""
        if task_id in self.active_syncs:
            task = self.active_syncs[task_id]
            strategy = task["strategy"]
            
            return {
                "task_id": task_id,
                "sync_type": strategy.sync_type.value,
                "status": strategy.status.value,
                "progress": strategy.get_progress(),
                "start_time": strategy.start_time,
                "estimated_duration": strategy.estimate_duration(**task["parameters"]),
                "error_message": strategy.error_message
            }
        
        # 在历史记录中查找
        for task in self.sync_history:
            if task["task_id"] == task_id:
                strategy = task["strategy"]
                return {
                    "task_id": task_id,
                    "sync_type": strategy.sync_type.value,
                    "status": strategy.status.value,
                    "progress": 100.0 if strategy.status == SyncStatus.COMPLETED else 0.0,
                    "start_time": strategy.start_time,
                    "end_time": strategy.end_time,
                    "error_message": strategy.error_message
                }
        
        return {"error": "任务不存在"}

# ============================================================================
# 使用示例
# ============================================================================

SYNC_USAGE_EXAMPLES = """
# 数据同步策略使用示例

## 1. 完全同步
```python
from database.data_sync_strategy import SyncManager, FullSyncStrategy

# 创建同步管理器
sync_manager = SyncManager()

# 创建完全同步策略
full_sync = FullSyncStrategy()

# 创建同步任务
task_id = sync_manager.create_sync_task(
    strategy=full_sync,
    project_id="b.1eea4119-3553-4167-b93d-3a3d5d07d33d",
    max_depth=10,
    include_versions=True,
    include_custom_attributes=True
)

# 执行同步
success = sync_manager.execute_sync(task_id)

# 检查状态
status = sync_manager.get_sync_status(task_id)
print(f"同步状态: {status}")
```

## 2. 增量同步
```python
from datetime import datetime, timedelta
from database.data_sync_strategy import IncrementalSyncStrategy

# 创建增量同步策略
incremental_sync = IncrementalSyncStrategy()

# 从6小时前开始增量同步
since_time = datetime.now() - timedelta(hours=6)

task_id = sync_manager.create_sync_task(
    strategy=incremental_sync,
    project_id="b.1eea4119-3553-4167-b93d-3a3d5d07d33d",
    since=since_time
)

success = sync_manager.execute_sync(task_id)
```

## 3. 数据转换
```python
from database.data_sync_strategy import DataTransformer

# 转换ACC API数据为数据库格式
api_folder_data = {
    "id": "urn:adsk.wipprod:fs.folder:co.xxx",
    "attributes": {
        "displayName": "Design Documents",
        "createTime": "2024-01-01T10:00:00Z",
        "createUserId": "user123",
        "objectCount": 25
    }
}

db_folder_data = DataTransformer.transform_folder_data(
    api_data=api_folder_data,
    project_id="b.1eea4119-3553-4167-b93d-3a3d5d07d33d",
    parent_id="parent_folder_id",
    path="/Project Files",
    depth=1
)

print(f"转换后的文件夹数据: {db_folder_data}")
```

## 4. 批量数据操作
```python
from database.data_access_layer import get_dal

# 获取数据访问层
dal = get_dal()

# 批量插入文件夹
folders_data = [db_folder_data]  # 转换后的文件夹数据列表
result = dal.batch_upsert_folders(folders_data)
print(f"批量操作结果: {result}")

# 获取项目统计
stats = dal.get_project_statistics("b.1eea4119-3553-4167-b93d-3a3d5d07d33d")
print(f"项目统计: {stats}")
```
"""
