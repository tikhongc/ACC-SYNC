"""
文件树构建优化函数
支持智能分支跳过以提高性能
"""

import time
from .file_sync_api import get_folder_contents, get_item_versions, FileTreeNode


def build_file_tree_recursive_optimized(project_id, folder_id, headers, parent_node=None, max_depth=10, current_depth=0, target_folder_ids=None, folder_path_mapping=None, current_path=""):
    """递归构建文件树结构（支持智能分支跳过优化）"""
    if current_depth >= max_depth:
        print(f"⚠️ 达到最大递归深度 {max_depth}，停止遍历")
        return []
    
    print(f"📁 遍历文件夹 (深度 {current_depth}): {folder_id}")
    
    # 获取文件夹内容
    contents_data = get_folder_contents(project_id, folder_id, headers)
    nodes = []
    
    for item in contents_data.get('data', []):
        item_id = item.get('id')
        item_type = item.get('type')
        attributes = item.get('attributes', {})
        item_name = attributes.get('displayName', attributes.get('name', 'Unknown'))
        
        # 构建当前项目的路径
        if current_path and current_path != "Project Files":
            item_path = f"{current_path}/{item_name}"
        else:
            item_path = item_name
        
        # 如果是文件夹且启用了目标文件夹过滤，检查是否应该跳过
        if item_type == 'folders' and target_folder_ids and folder_path_mapping:
            should_skip = should_skip_folder_branch_optimized(item_id, item_name, item_path, target_folder_ids, folder_path_mapping)
            if should_skip:
                print(f"   ⏭️ 跳过不相关分支: {item_name} (路径: {item_path})")
                continue
            else:
                print(f"   ✅ 目标相关分支，继续遍历: {item_name}")
        
        # 创建节点
        node = FileTreeNode(
            item_id=item_id,
            name=item_name,
            item_type='folder' if item_type == 'folders' else 'file',
            parent_id=folder_id
        )
        
        # 添加属性信息
        node.attributes = {
            'displayName': item_name,
            'createTime': attributes.get('createTime'),
            'createUserId': attributes.get('createUserId'),
            'createUserName': attributes.get('createUserName'),
            'lastModifiedTime': attributes.get('lastModifiedTime'),
            'lastModifiedUserId': attributes.get('lastModifiedUserId'),
            'lastModifiedUserName': attributes.get('lastModifiedUserName'),
            'lastModifiedTimeRollup': attributes.get('lastModifiedTimeRollup'),  # 新增：包括子文件/版本的最后修改时间
            'objectCount': attributes.get('objectCount', 0),
            'size': attributes.get('size', 0),
            'path': attributes.get('path'),  # 新增：文件夹路径
            'hidden': attributes.get('hidden', False),  # 新增：是否隐藏
            'extension': attributes.get('extension', {})
        }
        
        # 如果是文件，添加文件特有的属性
        if item_type != 'folders':
            node.attributes.update({
                'reserved': attributes.get('reserved', False),  # 是否被保留
                'reservedTime': attributes.get('reservedTime'),  # 保留时间
                'reservedUserId': attributes.get('reservedUserId'),  # 保留者ID
                'reservedUserName': attributes.get('reservedUserName')  # 保留者名称
            })
        
        # 添加基本权限信息（从属性中提取）
        node.permissions = {
            'canRead': True,  # 如果能获取到就说明有读权限
            'canWrite': False,  # 需要进一步检查
            'canDelete': False,  # 需要进一步检查
            'createUserId': attributes.get('createUserId'),
            'lastModifiedUserId': attributes.get('lastModifiedUserId')
        }
        
        if item_type == 'folders':
            # 递归处理子文件夹
            print(f"📂 处理子文件夹: {item_name}")
            child_nodes = build_file_tree_recursive_optimized(
                project_id, item_id, headers, node, max_depth, current_depth + 1,
                target_folder_ids, folder_path_mapping, item_path
            )
            node.children = child_nodes
        else:
            # 处理文件，获取版本信息
            print(f"📄 处理文件: {item_name}")
            versions = get_item_versions(project_id, item_id, headers)
            node.versions = versions
            
            # 从版本信息中提取更多属性
            if versions:
                latest_version = versions[0]  # 通常第一个是最新版本
                version_attributes = latest_version.get('attributes', {})
                # 获取文件大小，尝试多个字段
                file_size = (version_attributes.get('storageSize', 0) or 
                           version_attributes.get('fileSize', 0) or
                           latest_version.get('storageSize', 0) or
                           latest_version.get('fileSize', 0))
                
                node.attributes.update({
                    'versionNumber': version_attributes.get('versionNumber'),
                    'mimeType': version_attributes.get('mimeType'),
                    'fileSize': file_size,
                    'storageSize': file_size,  # 添加storageSize字段
                    'downloadUrl': version_attributes.get('downloadUrl')
                })
                
                # 调试输出
                if file_size == 0:
                    print(f"⚠️ 文件 {item_name} 版本大小为0，版本属性: {version_attributes}")
                    print(f"   完整版本信息: {latest_version}")
        
        nodes.append(node)
        
        # 优化：只在处理文件时添加小延迟，文件夹不需要延迟
        if item_type != 'folders':
            time.sleep(0.05)  # 减少延迟时间
    
    return nodes


def should_skip_folder_branch_optimized(folder_id, folder_name, folder_path, target_folder_ids, folder_path_mapping):
    """
    判断是否应该跳过某个文件夹分支（优化版本）
    """
    if not target_folder_ids or not folder_path_mapping:
        return False
    
    # 检查当前文件夹是否是目标文件夹
    if folder_id in target_folder_ids:
        return False
    
    # 检查当前文件夹是否可能包含目标文件夹
    for target_id in target_folder_ids:
        if target_id in folder_path_mapping:
            target_info = folder_path_mapping[target_id]
            target_name = target_info.get('name', '')
            target_path = target_info.get('path', '')
            
            # 检查路径匹配
            if target_path and folder_path:
                # 规范化路径比较
                normalized_target = target_path.replace('Project Files/', '').replace('Project Files', '').strip('/')
                normalized_current = folder_path.replace('Project Files/', '').replace('Project Files', '').strip('/')
                
                # 如果目标路径以当前路径开头，说明目标在当前分支下
                if (normalized_target.startswith(normalized_current + '/') or 
                    normalized_target == normalized_current or
                    normalized_current.startswith(normalized_target + '/')):
                    return False
            
            # 检查名称匹配
            if target_name and (folder_name.lower() == target_name.lower() or 
                              target_name.lower() in folder_path.lower() or
                              folder_path.lower().startswith(target_name.lower())):
                return False
    
    # 如果都不匹配，可以跳过这个分支
    return True


def should_skip_folder_branch_by_rollup_time(folder_data, last_sync_time):
    """
    基於 last_modified_time_rollup 判斷是否應該跳過整個文件夾分支
    
    Args:
        folder_data: 文件夾數據，包含 attributes
        last_sync_time: 上次同步時間
        
    Returns:
        bool: True 表示可以跳過，False 表示需要繼續處理
    """
    if not folder_data or not last_sync_time:
        return False
    
    try:
        attributes = folder_data.get('attributes', {})
        rollup_time_str = attributes.get('lastModifiedTimeRollup')
        
        if not rollup_time_str:
            # 沒有 rollup 時間，保守策略：不跳過
            return False
        
        # 解析 rollup 時間
        from .file_sync_db_api import parse_api_datetime
        rollup_time = parse_api_datetime(rollup_time_str)
        
        if not rollup_time:
            return False
        
        # 比較時間戳
        if hasattr(rollup_time, 'timestamp') and hasattr(last_sync_time, 'timestamp'):
            rollup_timestamp = rollup_time.timestamp()
            sync_timestamp = last_sync_time.timestamp()
            
            # 如果 rollup 時間 <= 上次同步時間，說明整個分支都沒有變更
            can_skip = rollup_timestamp <= sync_timestamp
            
            if can_skip:
                folder_name = attributes.get('displayName', attributes.get('name', 'Unknown'))
                print(f"Smart skip branch (rollup optimization): {folder_name} (rollup: {rollup_timestamp} <= sync: {sync_timestamp})")
            
            return can_skip
            
    except Exception as e:
        print(f"Warning: rollup time comparison failed: {str(e)}")
        return False
    
    return False
