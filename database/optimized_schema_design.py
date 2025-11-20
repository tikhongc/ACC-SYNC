# -*- coding: utf-8 -*-
"""
优化的MongoDB数据库架构设计
基于方案1（优化的单次遍历）+ 方案2（优化的数据库设计）的组合
暂时不考虑权限信息，专注于文件和文件夹的核心数据结构
"""

from datetime import datetime
from typing import Dict, List, Any, Optional

# ============================================================================
# 数据库集合设计
# ============================================================================

OPTIMIZED_COLLECTIONS_SCHEMA = {
    
    # 1. 项目基本信息集合
    "projects": {
        "_id": "string",  # project_id (例如: b.1eea4119-3553-4167-b93d-3a3d5d07d33d)
        "name": "string",
        "description": "string",
        "hub_id": "string",
        "account_id": "string", 
        "status": "string",  # active/inactive/archived
        
        # 同步状态信息
        "sync_info": {
            "last_sync_time": "datetime",
            "sync_status": "string",  # success/error/in_progress/pending
            "sync_duration_seconds": "float",
            "sync_error": "string",  # 错误信息
            "sync_version": "string"  # 同步版本号
        },
        
        # 项目统计信息
        "statistics": {
            "total_folders": "int",
            "total_files": "int", 
            "total_size_bytes": "long",
            "max_depth": "int",
            "file_types_count": "object",  # {pdf: 10, dwg: 5, ...}
            "last_calculated": "datetime"
        },
        
        # 元数据
        "metadata": {
            "create_time": "datetime",
            "create_user_id": "string",
            "create_user_name": "string",
            "last_modified_time": "datetime",
            "last_modified_user_id": "string",
            "last_modified_user_name": "string"
        },
        
        "created_at": "datetime",
        "updated_at": "datetime"
    },
    
    # 2. 文件夹集合（扁平化存储）
    "folders": {
        "_id": "string",  # folder_id (例如: urn:adsk.wipprod:fs.folder:co.xxx)
        "project_id": "string",
        "name": "string",
        "display_name": "string",
        "parent_id": "string",  # null for root folders
        
        # 路径信息（用于快速查询和显示）
        "path": "string",  # 完整路径 (例如: /Project Files/Design/Architectural)
        "path_segments": ["string"],  # 路径分段 ["Project Files", "Design", "Architectural"]
        "depth": "int",  # 层级深度，从0开始
        
        # 基本属性
        "metadata": {
            "display_name": "string",
            "create_time": "datetime",
            "create_user_id": "string", 
            "create_user_name": "string",
            "last_modified_time": "datetime",
            "last_modified_user_id": "string",
            "last_modified_user_name": "string",
            "last_modified_time_rollup": "datetime",  # 包括子文件/版本的最后修改时间
            "object_count": "int",  # 直接子项数量
            "size": "long",  # 文件夹大小
            "hidden": "boolean",
            "path_attr": "string"  # API返回的path属性
        },
        
        # 扩展属性
        "extension": "object",  # 原始extension数据
        
        # 自定义属性定义（文件夹特有）
        "custom_attribute_definitions": {
            "has_definitions": "boolean",
            "definitions": "object",  # {attr_id: {name, type, required, ...}}
            "total_count": "int",
            "last_sync_time": "datetime"
        },
        
        # 子项统计信息
        "children_stats": {
            "direct_folders": "int",  # 直接子文件夹数量
            "direct_files": "int",    # 直接子文件数量
            "total_folders": "int",   # 递归子文件夹总数
            "total_files": "int",     # 递归子文件总数
            "total_size": "long",     # 递归总大小
            "last_calculated": "datetime"
        },
        
        # 同步信息
        "sync_info": {
            "sync_time": "datetime",
            "sync_status": "string",
            "api_source": "string"
        },
        
        # 索引优化字段
        "project_path": "string",  # project_id + path 组合，用于复合查询
        "parent_path": "string",   # 父路径，用于查询子文件夹
        
        "created_at": "datetime",
        "updated_at": "datetime"
    },
    
    # 3. 文件集合（扁平化存储）
    "files": {
        "_id": "string",  # file_id (例如: urn:adsk.wipprod:dm.lineage:xxx)
        "project_id": "string",
        "name": "string",
        "display_name": "string", 
        "parent_folder_id": "string",
        
        # 路径信息
        "folder_path": "string",  # 所在文件夹的完整路径
        "full_path": "string",    # 文件的完整路径（包含文件名）
        "path_segments": ["string"],  # 完整路径分段
        "depth": "int",  # 文件所在层级深度
        
        # 基本元数据
        "metadata": {
            "display_name": "string",
            "create_time": "datetime", 
            "create_user_id": "string",
            "create_user_name": "string",
            "last_modified_time": "datetime",
            "last_modified_user_id": "string",
            "last_modified_user_name": "string",
            "last_modified_time_rollup": "datetime",
            "size": "long",
            "hidden": "boolean",
            
            # 文件特有属性
            "reserved": "boolean",  # 是否被保留
            "reserved_time": "datetime",
            "reserved_user_id": "string", 
            "reserved_user_name": "string"
        },
        
        # 文件类型和扩展信息
        "file_info": {
            "extension": "object",  # 原始extension数据
            "file_type": "string",  # 提取的文件类型 (pdf, dwg, rvt, etc.)
            "mime_type": "string",
            "category": "string"    # 文件分类 (drawing, model, document, etc.)
        },
        
        # 当前版本信息（快速访问）
        "current_version": {
            "version_id": "string",  # 当前版本的URN
            "version_number": "int",
            "file_size": "long",
            "storage_size": "long", 
            "mime_type": "string",
            "create_time": "datetime",
            "create_user_id": "string",
            "create_user_name": "string",
            
            # URN信息
            "urn": "string",           # version URN
            "item_urn": "string",      # item URN  
            "storage_urn": "string",   # storage URN
            "lineage_urn": "string",   # lineage URN
            
            # Review状态信息（从extension.data提取）
            "review_state": "string",  # approved, rejected, pending, etc.
            "review_info": "object"    # 详细review信息
        },
        
        # 版本历史摘要
        "versions_summary": {
            "total_versions": "int",
            "latest_version_number": "int",
            "first_version_time": "datetime",
            "latest_version_time": "datetime",
            "has_review_states": "boolean"
        },
        
        # 自定义属性
        "custom_attributes": {
            "has_attributes": "boolean",
            "attributes": "object",  # {attr_name: attr_value}
            "total_count": "int",
            "last_sync_time": "datetime"
        },
        
        # 同步信息
        "sync_info": {
            "sync_time": "datetime",
            "sync_status": "string", 
            "api_source": "string",
            "versions_synced": "boolean"
        },
        
        # 索引优化字段
        "project_folder": "string",  # project_id + folder_path 组合
        "project_type": "string",    # project_id + file_type 组合
        "name_lower": "string",      # 小写文件名，用于搜索
        
        "created_at": "datetime",
        "updated_at": "datetime"
    },
    
    # 4. 文件版本集合（独立存储，支持版本历史查询）
    "file_versions": {
        "_id": "string",  # version_id (version URN)
        "file_id": "string",  # 关联的文件ID
        "project_id": "string",
        "version_number": "int",
        
        # URN信息
        "urn": "string",           # version URN
        "item_urn": "string",      # item URN
        "storage_urn": "string",   # storage URN  
        "lineage_urn": "string",   # lineage URN
        
        # 版本元数据
        "metadata": {
            "display_name": "string",
            "create_time": "datetime",
            "create_user_id": "string",
            "create_user_name": "string", 
            "last_modified_time": "datetime",
            "last_modified_user_id": "string",
            "last_modified_user_name": "string",
            "file_size": "long",
            "storage_size": "long",
            "mime_type": "string"
        },
        
        # Review状态信息
        "review_info": {
            "review_state": "string",  # 从extension.data.reviewState提取
            "approval_status": "object",  # 审批状态详情
            "review_workflow_id": "string",
            "review_step": "string",
            "reviewers": ["object"]  # 审核者信息
        },
        
        # 扩展属性
        "extension": "object",  # 完整的extension数据
        
        # 自定义属性（版本级别）
        "custom_attributes": {
            "has_attributes": "boolean",
            "attributes": "object",
            "last_sync_time": "datetime"
        },
        
        # 下载信息
        "download_info": {
            "download_url": "string",
            "storage_location": "string",
            "derivatives": "object",  # derivative信息
            "last_checked": "datetime"
        },
        
        # 同步信息
        "sync_info": {
            "sync_time": "datetime",
            "sync_status": "string",
            "api_source": "string"
        },
        
        "created_at": "datetime",
        "updated_at": "datetime"
    },
    
    # 5. 同步任务记录集合
    "sync_tasks": {
        "_id": "ObjectId",
        "project_id": "string",
        "task_type": "string",  # full_sync, incremental_sync, folder_sync, file_sync
        "task_status": "string",  # pending, running, completed, failed
        
        # 任务参数
        "parameters": {
            "max_depth": "int",
            "include_versions": "boolean",
            "include_custom_attributes": "boolean",
            "target_folder_ids": ["string"],
            "file_types": ["string"]
        },
        
        # 任务进度
        "progress": {
            "total_items": "int",
            "processed_items": "int",
            "success_count": "int",
            "error_count": "int",
            "current_stage": "string",
            "percentage": "float"
        },
        
        # 任务结果
        "results": {
            "folders_synced": "int",
            "files_synced": "int", 
            "versions_synced": "int",
            "errors": ["object"],
            "warnings": ["object"],
            "duration_seconds": "float"
        },
        
        # 时间信息
        "start_time": "datetime",
        "end_time": "datetime",
        "created_at": "datetime",
        "updated_at": "datetime"
    }
}

# ============================================================================
# 索引设计
# ============================================================================

OPTIMIZED_INDEXES = {
    "projects": [
        {"_id": 1},  # 主键
        {"sync_info.last_sync_time": -1},  # 按同步时间排序
        {"sync_info.sync_status": 1},      # 按同步状态查询
        {"statistics.total_files": -1},    # 按文件数量排序
        {"created_at": -1}                 # 按创建时间排序
    ],
    
    "folders": [
        {"_id": 1},  # 主键
        {"project_id": 1, "path": 1},      # 项目路径查询（复合索引）
        {"project_path": 1},               # 项目路径组合查询
        {"parent_id": 1},                  # 父文件夹查询
        {"project_id": 1, "depth": 1},     # 按层级查询
        {"project_id": 1, "parent_id": 1}, # 项目父文件夹查询
        {"path_segments": 1},              # 路径分段查询
        {"sync_info.sync_time": -1},       # 同步时间排序
        {"metadata.last_modified_time": -1}, # 修改时间排序
        {"children_stats.total_files": -1}, # 按文件数量排序
        {"name": "text", "display_name": "text"}  # 文本搜索
    ],
    
    "files": [
        {"_id": 1},  # 主键
        {"project_id": 1, "folder_path": 1},     # 项目文件夹查询（复合索引）
        {"project_folder": 1},                   # 项目文件夹组合查询
        {"parent_folder_id": 1},                 # 父文件夹查询
        {"project_id": 1, "file_info.file_type": 1}, # 项目文件类型查询
        {"project_type": 1},                     # 项目类型组合查询
        {"current_version.review_state": 1},     # Review状态查询
        {"current_version.urn": 1},              # URN查询
        {"file_info.file_type": 1},              # 文件类型查询
        {"metadata.last_modified_time": -1},     # 修改时间排序
        {"current_version.file_size": -1},       # 文件大小排序
        {"sync_info.sync_time": -1},             # 同步时间排序
        {"name_lower": 1},                       # 文件名搜索
        {"name": "text", "display_name": "text"} # 文本搜索
    ],
    
    "file_versions": [
        {"_id": 1},  # 主键
        {"file_id": 1, "version_number": -1},   # 文件版本查询（复合索引）
        {"project_id": 1, "review_info.review_state": 1}, # 项目Review状态查询
        {"urn": 1},                              # URN查询
        {"item_urn": 1},                         # Item URN查询
        {"storage_urn": 1},                      # Storage URN查询
        {"lineage_urn": 1},                      # Lineage URN查询
        {"metadata.create_time": -1},            # 创建时间排序
        {"sync_info.sync_time": -1}              # 同步时间排序
    ],
    
    "sync_tasks": [
        {"_id": 1},  # 主键
        {"project_id": 1, "start_time": -1},    # 项目任务历史查询
        {"task_status": 1, "start_time": -1},   # 任务状态查询
        {"task_type": 1},                       # 任务类型查询
        {"start_time": -1}                      # 时间排序
    ]
}

# ============================================================================
# 数据验证规则
# ============================================================================

VALIDATION_RULES = {
    "projects": {
        "required_fields": ["_id", "name", "sync_info", "statistics"],
        "field_types": {
            "_id": str,
            "name": str,
            "sync_info.sync_status": str,
            "statistics.total_folders": int,
            "statistics.total_files": int
        }
    },
    
    "folders": {
        "required_fields": ["_id", "project_id", "name", "path", "depth"],
        "field_types": {
            "_id": str,
            "project_id": str,
            "name": str,
            "path": str,
            "depth": int
        }
    },
    
    "files": {
        "required_fields": ["_id", "project_id", "name", "parent_folder_id", "current_version"],
        "field_types": {
            "_id": str,
            "project_id": str,
            "name": str,
            "parent_folder_id": str,
            "current_version.version_number": int
        }
    }
}

# ============================================================================
# 集合大小估算和分片策略
# ============================================================================

COLLECTION_SIZING = {
    "projects": {
        "estimated_documents": 100,        # 预估100个项目
        "avg_document_size_kb": 2,         # 平均2KB每个文档
        "growth_rate": "low"               # 增长率低
    },
    
    "folders": {
        "estimated_documents": 50000,      # 预估5万个文件夹
        "avg_document_size_kb": 1,         # 平均1KB每个文档
        "growth_rate": "medium"            # 增长率中等
    },
    
    "files": {
        "estimated_documents": 500000,     # 预估50万个文件
        "avg_document_size_kb": 2,         # 平均2KB每个文档
        "growth_rate": "high"              # 增长率高
    },
    
    "file_versions": {
        "estimated_documents": 2000000,    # 预估200万个版本
        "avg_document_size_kb": 3,         # 平均3KB每个文档
        "growth_rate": "high"              # 增长率高
    }
}

# 分片策略（适用于大型部署）
SHARDING_STRATEGY = {
    "files": {
        "shard_key": {"project_id": 1, "_id": 1},
        "reason": "按项目分片，确保同项目数据在同一分片"
    },
    
    "file_versions": {
        "shard_key": {"project_id": 1, "file_id": 1},
        "reason": "按项目和文件分片，版本数据与文件数据就近存储"
    }
}

# ============================================================================
# 性能优化建议
# ============================================================================

PERFORMANCE_OPTIMIZATION = {
    "connection_pooling": {
        "max_pool_size": 100,
        "min_pool_size": 10,
        "max_idle_time_ms": 30000
    },
    
    "read_preferences": {
        "primary_read": ["sync_tasks", "projects"],  # 需要强一致性
        "secondary_read": ["folders", "files", "file_versions"]  # 可以读从库
    },
    
    "write_concerns": {
        "acknowledged": ["projects", "sync_tasks"],  # 需要确认写入
        "unacknowledged": ["folders", "files"]       # 可以异步写入
    },
    
    "aggregation_optimization": {
        "use_indexes": True,
        "allow_disk_use": True,
        "max_time_ms": 30000
    }
}
