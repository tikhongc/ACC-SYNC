# -*- coding: utf-8 -*-
"""
简化的同步记录设计
只记录成功完成的同步，使用中国时间
"""

from datetime import datetime
import pytz

# 中国时区
CHINA_TZ = pytz.timezone('Asia/Shanghai')

# 简化的同步记录集合设计
SIMPLIFIED_SYNC_SCHEMA = {
    # 同步历史记录集合 - 只记录成功的完整同步
    "sync_history": {
        "_id": "ObjectId",
        "project_id": "string",
        "sync_type": "string",  # full_sync, incremental_sync
        
        # 同步结果 - 只记录成功的结果
        "results": {
            "folders_synced": "int",
            "files_synced": "int", 
            "versions_synced": "int",
            "total_size_bytes": "long",  # 修复total_size问题
            "duration_seconds": "float"
        },
        
        # 时间信息 - 使用中国时间
        "sync_time": "datetime",  # 同步完成时间（中国时间）
        "created_at": "datetime"  # 记录创建时间（中国时间）
    }
}

def get_china_time():
    """获取当前中国时间"""
    return datetime.now(CHINA_TZ)

def format_china_time(dt):
    """格式化中国时间显示"""
    if dt.tzinfo is None:
        # 如果没有时区信息，假设是UTC时间，转换为中国时间
        dt = pytz.utc.localize(dt).astimezone(CHINA_TZ)
    elif dt.tzinfo != CHINA_TZ:
        # 如果有时区信息但不是中国时间，转换为中国时间
        dt = dt.astimezone(CHINA_TZ)
    
    return dt.strftime('%Y-%m-%d %H:%M:%S')

# 简化的同步记录创建函数
def create_sync_record(project_id: str, sync_type: str, results: dict) -> dict:
    """创建简化的同步记录"""
    china_time = get_china_time()
    
    return {
        "project_id": project_id,
        "sync_type": sync_type,
        "results": {
            "folders_synced": results.get("folders_synced", 0),
            "files_synced": results.get("files_synced", 0),
            "versions_synced": results.get("versions_synced", 0),
            "total_size_bytes": results.get("total_size", 0),
            "duration_seconds": results.get("duration_seconds", 0.0)
        },
        "sync_time": china_time,
        "created_at": china_time
    }
