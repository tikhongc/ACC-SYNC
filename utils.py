# -*- coding: utf-8 -*-
"""
增强的工具函数模块 - 优化Token管理
包含自动刷新、持久化存储、失效重试等功能
"""

import json
import os
import time
import threading
import requests
from datetime import datetime, timedelta
import config

# Token管理 - 使用多层存储策略
try:
    from flask import session
except ImportError:
    session = {}

# 全局token存储（内存 + 持久化）
_token_storage = {
    'access_token': None,
    'refresh_token': None,
    'expires_at': None,
    'updated_at': None,
    'refresh_attempts': 0,
    'last_refresh_attempt': None,
    'next_auto_refresh_at': None  # 下次自动刷新的预计时间
}

# 线程锁，确保token操作的线程安全
_token_lock = threading.Lock()

# 持久化存储文件路径
PERSISTENT_TOKEN_FILE = os.path.join(os.path.dirname(__file__), '.token_cache.json')

# Token配置
TOKEN_REFRESH_THRESHOLD = 600  # 提前10分钟刷新
MAX_REFRESH_ATTEMPTS = 3
REFRESH_RETRY_DELAY = 5  # 刷新失败后等待5秒重试

# 2-legged token存储
_two_legged_token_storage = {
    'access_token': None,
    'expires_at': None,
    'updated_at': None
}


def get_access_token():
    """获取有效的access token，支持智能自动刷新"""
    with _token_lock:
        current_time = time.time()
        
        # 1. 检查内存中的token
        if _token_storage['access_token']:
            expires_at = _token_storage['expires_at']
            
            # 如果token有充足的有效期（超过5分钟），直接返回
            if expires_at and current_time < (expires_at - 300):
                return _token_storage['access_token']
            
            # 如果token即将过期或已过期，但有refresh_token，尝试刷新
            if _token_storage['refresh_token']:
                should_refresh = False
                
                if not expires_at:
                    should_refresh = True
                    print("[Token] No expiry info, refreshing token...")
                elif current_time >= expires_at:
                    should_refresh = True 
                    print("[Token] Token expired, refreshing...")
                elif current_time > (expires_at - TOKEN_REFRESH_THRESHOLD):
                    should_refresh = True
                    print(f"[Token] Token expires in {int((expires_at - current_time)/60)} min, refreshing...")
                
                if should_refresh:
                    # 临时绕过频率限制，允许即时刷新
                    original_last_attempt = _token_storage.get('last_refresh_attempt')
                    if (original_last_attempt and 
                        current_time - original_last_attempt < REFRESH_RETRY_DELAY):
                        print("[Token] Bypassing refresh frequency limit for immediate request")
                        _token_storage['last_refresh_attempt'] = None
                    
                    # 直接调用内部刷新逻辑，避免重复获取锁
                    refreshed_token = _refresh_token_unlocked(source="auto")
                    if refreshed_token:
                        return refreshed_token
                    
                    # 如果刷新失败，恢复原始的last_attempt时间
                    if original_last_attempt:
                        _token_storage['last_refresh_attempt'] = original_last_attempt
            
            # 如果token还没完全过期，临时返回原token
            if expires_at and current_time < expires_at:
                print("[Token] Using potentially expired token temporarily")
                return _token_storage['access_token']
        
        # 2. 尝试从持久化存储加载
        if _load_from_persistent_storage():
            return _token_storage['access_token']
        
        # 3. 尝试从会话获取
        if _load_from_session():
            return _token_storage['access_token']
        
        # 4. 兼容旧版本文件存储
        return _get_token_from_file()


def _refresh_token_unlocked(force=False, source="unknown"):
    """内部token刷新函数 - 不使用锁，假设调用者已经获取了锁
    
    Args:
        force (bool): 是否强制刷新，忽略频率限制
        source (str): 调用来源，用于日志记录
    
    Returns:
        str|None: 成功时返回access_token，失败时返回None
    """
    if not _token_storage['refresh_token']:
        print(f"[Token] [{source}] No refresh token available")
        return None
    
    # 检查OAuth配置
    if not config.CLIENT_ID or not config.CLIENT_SECRET:
        print(f"[Token] [{source}] OAuth config incomplete")
        return None
    
    current_time = time.time()
    
    # 检查刷新频率限制（除非强制刷新）
    if not force and _token_storage.get('last_refresh_attempt'):
        time_since_last = current_time - _token_storage['last_refresh_attempt']
        if time_since_last < REFRESH_RETRY_DELAY:
            print(f"[Token] [{source}] Refresh too frequent, skipping")
        return None
    
    # 检查最大重试次数（除非强制刷新）
    if not force and _token_storage['refresh_attempts'] >= config.MAX_TOKEN_REFRESH_ATTEMPTS:
        print(f"[Token] [{source}] Max refresh attempts exceeded")
        return None
    
    try:
        print(f"[Token] [{source}] 开始刷新token (尝试 {_token_storage['refresh_attempts'] + 1})...")
        
        # 更新尝试记录
        _token_storage['last_refresh_attempt'] = current_time
        if not force:
            _token_storage['refresh_attempts'] += 1
        
        # 构建刷新请求
        refresh_data = {
            'grant_type': 'refresh_token',
            'refresh_token': _token_storage['refresh_token'],
            'client_id': config.CLIENT_ID,
            'client_secret': config.CLIENT_SECRET,
        }
        
        response = requests.post(
            f"{config.AUTODESK_AUTH_URL}/token",
            data=refresh_data,
            timeout=10
        )
        
        if response.status_code == 200:
            token_data = response.json()
            
            # 保存新的token（不使用锁，因为我们已经在锁内）
            success = _save_tokens_unlocked(
                access_token=token_data.get('access_token'),
                refresh_token=token_data.get('refresh_token', _token_storage['refresh_token']),
                expires_in=token_data.get('expires_in', 3600)
            )
            
            if success:
                # 重置刷新计数器
                _token_storage['refresh_attempts'] = 0
                _token_storage['last_refresh_attempt'] = None
                print(f"[Token] [{source}] Token刷新成功")
                return token_data.get('access_token')
            else:
                print(f"[Token] [{source}] Failed to save refreshed token")
                return None
        
        elif response.status_code in [400, 401]:
            # refresh_token过期或无效
            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
            error_type = error_data.get('error', 'unknown')
            error_desc = error_data.get('error_description', response.text[:200])
            
            print(f"[Token] [{source}] Refresh token无效或过期: {error_type} - {error_desc}")
            
            if error_type == 'invalid_grant' or response.status_code == 401:
                # refresh_token过期，清除所有token
                print(f"[Token] [{source}] 清除过期的tokens，需要重新认证")
                _clear_expired_tokens()
                return None
            else:
                print(f"[Token] [{source}] 刷新失败: {error_desc}")
                return None
        
        else:
            # 其他HTTP错误
            error_msg = f"HTTP {response.status_code}: {response.text[:200]}"
            print(f"[Token] [{source}] 刷新请求失败: {error_msg}")
            return None
            
    except requests.exceptions.Timeout:
        print(f"[Token] [{source}] 请求超时")
        return None
    except requests.exceptions.ConnectionError:
        print(f"[Token] [{source}] 网络连接错误")
        return None
    except Exception as e:
        print(f"[Token] [{source}] 刷新过程中发生异常: {str(e)}")
    return None


def refresh_access_token(force=False, source="unknown"):
    """统一的token刷新函数 - 被自动和手动刷新共同使用
    
    Args:
        force (bool): 是否强制刷新，忽略频率限制
        source (str): 调用来源，用于日志记录
    
    Returns:
        tuple: (success: bool, result: str|dict, error_code: str|None)
    """
    with _token_lock:
        if not _token_storage['refresh_token']:
            return False, "没有可用的refresh token", "no_refresh_token"
        
        # 检查OAuth配置
        if not config.CLIENT_ID or not config.CLIENT_SECRET:
            return False, "OAuth配置不完整", "config_incomplete"
        
        current_time = time.time()
        
        # 检查刷新频率限制（除非强制刷新）
        if not force and _token_storage.get('last_refresh_attempt'):
            time_since_last = current_time - _token_storage['last_refresh_attempt']
            if time_since_last < REFRESH_RETRY_DELAY:
                return False, f"刷新过于频繁，请等待{REFRESH_RETRY_DELAY - int(time_since_last)}秒", "too_frequent"
        
        # 检查最大重试次数（除非强制刷新）
        if not force and _token_storage['refresh_attempts'] >= config.MAX_TOKEN_REFRESH_ATTEMPTS:
            return False, f"已达到最大重试次数({config.MAX_TOKEN_REFRESH_ATTEMPTS})", "max_attempts_exceeded"
        
        # 调用内部无锁刷新函数
        access_token = _refresh_token_unlocked(force=force, source=source)
        if access_token:
            # 构造token_data用于返回
            token_data = {
                'access_token': access_token,
                'expires_in': 3600  # 默认值，实际值已经在_save_tokens_unlocked中处理
            }
            return True, token_data, None
        else:
            # 根据当前状态确定错误类型
            if not _token_storage.get('refresh_token'):
                return False, "Refresh token已过期，需要重新登录", "refresh_token_expired"
            else:
                return False, "Token刷新失败", "refresh_failed"


def _clear_expired_tokens():
    """清除过期的tokens"""
    _token_storage.update({
        'access_token': None,
        'refresh_token': None,
        'expires_at': None,
        'updated_at': None,
        'refresh_attempts': 0,
        'last_refresh_attempt': None,
        'next_auto_refresh_at': None
    })
    
    # 清除持久化存储
    try:
        if os.path.exists(PERSISTENT_TOKEN_FILE):
            os.remove(PERSISTENT_TOKEN_FILE)
            print("[Token] 已清除持久化token文件")
    except Exception as e:
        print(f"[Token] 清除持久化文件失败: {e}")


def _attempt_token_refresh():
    """兼容性函数 - 调用新的统一刷新函数"""
    success, result, error_code = refresh_access_token(source="auto")
    if success and isinstance(result, dict):
        return result.get('access_token')
    return None


def _save_tokens_unlocked(access_token, refresh_token=None, expires_in=3600):
    """保存tokens到多个存储层（不使用锁，假设调用者已经获取了锁）"""
    current_time = time.time()
    expires_at = current_time + expires_in
    
    # 计算下次自动刷新时间（提前TOKEN_REFRESH_THRESHOLD秒）
    next_auto_refresh_at = expires_at - TOKEN_REFRESH_THRESHOLD
    
    # 更新内存存储
    _token_storage.update({
        'access_token': access_token,
        'refresh_token': refresh_token or _token_storage.get('refresh_token'),
        'expires_at': expires_at,
        'updated_at': current_time,
        'refresh_attempts': 0,  # 重置刷新计数
        'next_auto_refresh_at': next_auto_refresh_at
    })
    
    # 保存到会话
    _save_to_session(access_token, refresh_token, expires_at)
    
    # 保存到持久化存储
    _save_to_persistent_storage()
    
    print(f"[Token] Token saved successfully: {access_token[:20]}... (expires in {expires_in}s)")
    return True


def save_tokens(access_token, refresh_token=None, expires_in=3600):
    """保存tokens到多个存储层"""
    with _token_lock:
        return _save_tokens_unlocked(access_token, refresh_token, expires_in)


def _save_to_session(access_token, refresh_token, expires_at):
    """保存到Flask会话"""
    try:
        if session and hasattr(session, '__setitem__'):
            session['access_token'] = access_token
            session['token_expires_at'] = expires_at
            if refresh_token:
                session['refresh_token'] = refresh_token
            session.permanent = True  # 使会话持久化
            print("[Token] Token saved to session")
    except Exception as e:
        print(f"[Token] Failed to save to session: {e}")


def _save_to_persistent_storage():
    """保存到持久化文件"""
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(PERSISTENT_TOKEN_FILE), exist_ok=True)
        
        token_data = {
            'access_token': _token_storage['access_token'],
            'refresh_token': _token_storage['refresh_token'],
            'expires_at': _token_storage['expires_at'],
            'updated_at': _token_storage['updated_at'],
            'next_auto_refresh_at': _token_storage['next_auto_refresh_at'],
            'saved_at': time.time(),
            'version': '2.0'  # 添加版本标识
        }
        
        # 先写入临时文件，然后重命名，确保原子性操作
        temp_file = PERSISTENT_TOKEN_FILE + '.tmp'
        with open(temp_file, 'w') as f:
            json.dump(token_data, f, indent=2)
        
        # 原子性重命名
        if os.path.exists(temp_file):
            if os.path.exists(PERSISTENT_TOKEN_FILE):
                os.remove(PERSISTENT_TOKEN_FILE)
            os.rename(temp_file, PERSISTENT_TOKEN_FILE)
        
        print("[Token] Token saved to persistent storage")
    except Exception as e:
        print(f"[Token] Failed to save to persistent storage: {e}")
        # 清理临时文件
        temp_file = PERSISTENT_TOKEN_FILE + '.tmp'
        if os.path.exists(temp_file):
            try:
                os.remove(temp_file)
            except:
                pass


def _load_from_persistent_storage():
    """从持久化存储加载token"""
    try:
        if not os.path.exists(PERSISTENT_TOKEN_FILE):
            print("[Token] No persistent token file found")
            return False
        
        with open(PERSISTENT_TOKEN_FILE, 'r') as f:
            token_data = json.load(f)
        
        # 检查文件版本
        version = token_data.get('version', '1.0')
        print(f"[Token] Loading token from persistent storage (version {version})")
        
        expires_at = token_data.get('expires_at')
        current_time = time.time()
        
        # 检查token是否仍然有效（给予一些缓冲时间）
        if expires_at and current_time < (expires_at - TOKEN_REFRESH_THRESHOLD):
            _token_storage.update({
                'access_token': token_data.get('access_token'),
                'refresh_token': token_data.get('refresh_token'),
                'expires_at': expires_at,
                'updated_at': token_data.get('updated_at'),
                'next_auto_refresh_at': token_data.get('next_auto_refresh_at', expires_at - TOKEN_REFRESH_THRESHOLD if expires_at else None),
                'refresh_attempts': 0,
                'last_refresh_attempt': None
            })
            print(f"[Token] Valid token loaded from persistent storage (expires in {int((expires_at - current_time)/60)} minutes)")
            return True
        else:
            print(f"[Token] Persistent token expired (expired {int((current_time - expires_at)/60) if expires_at else 'unknown'} minutes ago)")
            # 如果token过期但有refresh_token，尝试刷新
            if token_data.get('refresh_token'):
                print("[Token] Attempting to refresh expired token from persistent storage")
                _token_storage.update({
                    'access_token': None,  # 清除过期的access_token
                    'refresh_token': token_data.get('refresh_token'),
                    'expires_at': None,
                    'updated_at': None,
                    'refresh_attempts': 0,
                    'last_refresh_attempt': None
                })
                # 直接调用内部刷新函数，因为调用者已经持有锁
                refreshed_token = _refresh_token_unlocked(source="persistent_storage")
                if refreshed_token:
                    print("[Token] Token refreshed successfully from persistent storage")
                    return True
                else:
                    print("[Token] Failed to refresh token from persistent storage")
            else:
                print("[Token] No refresh token available in persistent storage")
            
    except json.JSONDecodeError as e:
        print(f"[Token] Corrupted persistent token file: {e}")
        # 备份损坏的文件并删除
        try:
            backup_file = PERSISTENT_TOKEN_FILE + '.corrupted'
            os.rename(PERSISTENT_TOKEN_FILE, backup_file)
            print(f"[Token] Corrupted file backed up to {backup_file}")
        except:
            pass
    except Exception as e:
        print(f"[Token] Failed to load from persistent storage: {e}")
    
    return False


def _load_from_session():
    """从会话加载token"""
    try:
        if session and hasattr(session, 'get') and session.get('access_token'):
            token = session.get('access_token')
            expires_at = session.get('token_expires_at')
            refresh_token = session.get('refresh_token')
            
            current_time = time.time()
            
            # 检查token是否仍然有效
            if expires_at and current_time < (expires_at - TOKEN_REFRESH_THRESHOLD):
                _token_storage.update({
                    'access_token': token,
                    'refresh_token': refresh_token,
                    'expires_at': expires_at,
                    'updated_at': current_time,
                    'next_auto_refresh_at': expires_at - TOKEN_REFRESH_THRESHOLD if expires_at else None,
                    'refresh_attempts': 0
                })
                print("Token loaded from session")
                return True
        
    except Exception as e:
        print(f"Failed to load from session: {e}")
    
    return False


def get_refresh_token():
    """获取refresh token"""
    with _token_lock:
        return (_token_storage.get('refresh_token') or 
                (session.get('refresh_token') if hasattr(session, 'get') else None))


def clear_tokens():
    """清除所有token存储"""
    with _token_lock:
        # 清除内存存储
        _token_storage.update({
            'access_token': None,
            'refresh_token': None,
            'expires_at': None,
            'updated_at': None,
            'refresh_attempts': 0,
            'last_refresh_attempt': None,
            'next_auto_refresh_at': None
        })
        
        # 清除会话
        try:
            if hasattr(session, 'pop'):
                session.pop('access_token', None)
                session.pop('refresh_token', None)
                session.pop('token_expires_at', None)
        except Exception as e:
            print(f"[TOKEN] Failed to clear session: {e}")
        
        # 清除持久化存储
        try:
            if os.path.exists(PERSISTENT_TOKEN_FILE):
                os.remove(PERSISTENT_TOKEN_FILE)
                print("[TOKEN] Persistent token file removed")
        except Exception as e:
            print(f"[TOKEN] Failed to remove persistent token file: {e}")
        
        # 清除旧版本文件
        try:
            if hasattr(config, 'TOKEN_FILE') and os.path.exists(config.TOKEN_FILE):
                os.remove(config.TOKEN_FILE)
                print("[TOKEN] Legacy token file removed")
        except Exception as e:
            print(f"Failed to remove legacy token file: {e}")
        
        print("[TOKEN] All tokens cleared")


def is_token_valid():
    """检查token是否有效"""
    with _token_lock:
        return bool(_token_storage.get('access_token') and 
                   _token_storage.get('expires_at') and 
                   time.time() < _token_storage['expires_at'])


def get_token_info():
    """获取token信息（用于调试）"""
    with _token_lock:
        expires_at = _token_storage.get('expires_at')
        updated_at = _token_storage.get('updated_at')
        next_auto_refresh_at = _token_storage.get('next_auto_refresh_at')
        current_time = time.time()
        
        # 计算距离下次自动刷新的时间
        next_auto_refresh_in_minutes = None
        next_auto_refresh_in_seconds = None
        if next_auto_refresh_at and next_auto_refresh_at > current_time:
            next_auto_refresh_in_seconds = int(next_auto_refresh_at - current_time)
            next_auto_refresh_in_minutes = int(next_auto_refresh_in_seconds / 60)
        
        info = {
            'has_access_token': bool(_token_storage.get('access_token')),
            'has_refresh_token': bool(_token_storage.get('refresh_token')),
            'expires_at': datetime.fromtimestamp(expires_at).isoformat() if expires_at else None,
            'updated_at': datetime.fromtimestamp(updated_at).isoformat() if updated_at else None,
            'is_valid': bool(_token_storage.get('access_token') and expires_at and current_time < expires_at),
            'expires_in_minutes': int((expires_at - current_time) / 60) if expires_at else None,
            'refresh_attempts': _token_storage.get('refresh_attempts', 0),
            'last_refresh_attempt': datetime.fromtimestamp(_token_storage['last_refresh_attempt']).isoformat() if _token_storage.get('last_refresh_attempt') else None,
            'needs_refresh': expires_at and current_time > (expires_at - TOKEN_REFRESH_THRESHOLD) if expires_at else False,
            # 新增的下次自动刷新时间信息
            'next_auto_refresh_at': datetime.fromtimestamp(next_auto_refresh_at).isoformat() if next_auto_refresh_at else None,
            'next_auto_refresh_in_minutes': next_auto_refresh_in_minutes,
            'next_auto_refresh_in_seconds': next_auto_refresh_in_seconds
        }
        
        return info


def force_token_refresh():
    """强制刷新token - 使用统一的刷新函数"""
    success, result, error_code = refresh_access_token(force=True, source="force_refresh")
    
    if success:
        return True, "Token刷新成功"
    else:
        return False, f"Token刷新失败: {result} (错误码: {error_code})"


# 兼容性函数
def _get_token_from_file():
    """从文件获取token（兼容旧版本）"""
    try:
        if not hasattr(config, 'TOKEN_FILE') or not os.path.exists(config.TOKEN_FILE):
            return None
        
        with open(config.TOKEN_FILE, 'r') as f:
            content = f.read().strip()
        
        # 尝试解析
        try:
            import ast
            token_data = ast.literal_eval(content)
        except:
            try:
                token_data = json.loads(content)
            except:
                return None
        
        access_token = token_data.get('access_token')
        if access_token:
            # 迁移到新系统
            save_tokens(
                access_token=access_token,
                refresh_token=token_data.get('refresh_token'),
                expires_in=3600  # 默认1小时
            )
            print("Migrated token from legacy file storage")
        
        return access_token
        
    except Exception as e:
        print(f"Error reading legacy token file: {str(e)}")
        return None


def save_token_to_file(token_data):
    """保存token到文件（兼容性方法）"""
    try:
        # 直接使用新的保存方法
        if isinstance(token_data, dict):
            access_token = token_data.get('access_token')
            refresh_token = token_data.get('refresh_token')
            expires_in = token_data.get('expires_in', 3600)
            
            if access_token:
                save_tokens(access_token, refresh_token, expires_in)
                return "Token 已保存到增强存储系统"
        
        return "无效的token数据格式"
    except Exception as e:
        return f"保存 token 失败: {str(e)}"


# 导入原有的其他工具函数
def get_real_account_id(projects_data):
    """从项目数据中提取真实的 Account ID"""
    if "data" not in projects_data or len(projects_data["data"]) == 0:
        return None, None, None
    
    hub_id = projects_data["data"][0]["id"]
    real_account_id = hub_id[2:] if hub_id.startswith("b.") else hub_id
    hub_name = projects_data["data"][0]["attributes"]["name"]
    
    return hub_id, real_account_id, hub_name


def get_user_account_info(access_token):
    """
    获取用户账户信息的增强版本
    尝试多种API获取Hub/Account信息
    """
    import requests
    import config
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # 1. 首先尝试获取用户basicInfo
    try:
        user_resp = requests.get(f"{config.AUTODESK_API_BASE}/userprofile/v1/users/@me", headers=headers)
        if user_resp.status_code == 200:
            user_data = user_resp.json()
            user_id = user_data.get('userId')
            print(f"用户信息获取成功: {user_data.get('userName', 'Unknown')}")
        else:
            print(f"无法获取用户信息: {user_resp.status_code}")
            return None, None, None, None
    except Exception as e:
        print(f"获取用户信息时出错: {e}")
        return None, None, None, None
    
    # 2. 尝试Hub API
    try:
        hubs_resp = requests.get(f"{config.AUTODESK_API_BASE}/project/v1/hubs", headers=headers)
        if hubs_resp.status_code == 200:
            hubs_data = hubs_resp.json()
            if hubs_data.get('data'):
                hub_id, real_account_id, hub_name = get_real_account_id(hubs_data)
                if hub_id:
                    print(f"Hub信息获取成功: {hub_name}")
                    return hub_id, real_account_id, hub_name, user_data
    except Exception as e:
        print(f"Hub API调用出错: {e}")
    
    # 3. 如果没有Hub访问权限，检查是否为已知的企业用户
    print("[AUTH] 未找到Hub权限，检查已知企业账户")
    
    user_email = user_data.get('emailId', '')
    
    # 检查是否为已知企业用户 (使用配置文件中的映射)
    if user_email in config.ENTERPRISE_ACCOUNT_MAPPING:
        enterprise_info = config.ENTERPRISE_ACCOUNT_MAPPING[user_email]
        enterprise_account_id = enterprise_info['account_id']
        enterprise_hub_id = enterprise_info['hub_id']
        enterprise_hub_name = enterprise_info['hub_name']
        
        print(f"[AUTH] 找到企业账户映射: {user_email} -> {enterprise_account_id}")
        return enterprise_hub_id, enterprise_account_id, enterprise_hub_name, user_data
    
    # 4. 最后的fallback - 使用用户ID
    print("[AUTH] 使用用户ID作为fallback")
    fallback_hub_id = f"b.{user_id}"
    fallback_account_id = user_id
    fallback_hub_name = f"{user_data.get('firstName', '')} {user_data.get('lastName', '')}的个人账户"
    
    return fallback_hub_id, fallback_account_id, fallback_hub_name, user_data


def get_enterprise_hub_info(user_email=None):
    """
    获取企业Hub信息的通用函数
    
    Args:
        user_email: 用户邮箱，如果不提供则尝试从当前token获取
    
    Returns:
        tuple: (hub_id, account_id, hub_name) 或 (None, None, None)
    """
    try:
        # 如果没有提供邮箱，尝试从当前token获取
        if not user_email:
            access_token = get_access_token()
            if access_token:
                headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                }
                
                user_resp = requests.get(f"{config.AUTODESK_API_BASE}/userprofile/v1/users/@me", headers=headers)
                if user_resp.status_code == 200:
                    user_data = user_resp.json()
                    user_email = user_data.get('emailId', '')
        
        # 检查企业账户映射
        if user_email and user_email in config.ENTERPRISE_ACCOUNT_MAPPING:
            enterprise_info = config.ENTERPRISE_ACCOUNT_MAPPING[user_email]
            return (
                enterprise_info['hub_id'],
                enterprise_info['account_id'], 
                enterprise_info['hub_name']
            )
        
        return None, None, None
        
    except Exception as e:
        print(f"获取企业Hub信息时出错: {e}")
        return None, None, None

def format_timestamp(timestamp_str):
    """格式化时间戳字符串，转换为北京时间（UTC+8）"""
    try:
        from datetime import timezone, timedelta
        
        # 解析时间戳
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        
        # 转换为北京时间（UTC+8）
        beijing_tz = timezone(timedelta(hours=8))
        beijing_dt = dt.astimezone(beijing_tz)
        
        return beijing_dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp_str


def safe_get_length(obj):
    """安全地获取对象长度，处理 None 值"""
    if obj is None:
        return 0
    return len(obj)


def generate_html_response(title, content):
    """生成标准的 HTML 响应"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .success {{ background-color: #d4edda; padding: 15px; border-radius: 5px; }}
            .error {{ background-color: #f8d7da; padding: 15px; border-radius: 5px; }}
            .info {{ background-color: #d1ecf1; padding: 15px; border-radius: 5px; }}
            .warning {{ background-color: #fff3cd; padding: 15px; border-radius: 5px; }}
            pre {{ background-color: #f8f9fa; padding: 10px; border-radius: 5px; overflow-x: auto; }}
            .button {{ 
                background-color: #007bff; 
                color: white; 
                padding: 10px 15px; 
                text-decoration: none; 
                border-radius: 5px; 
                margin: 5px; 
                display: inline-block;
            }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        {content}
    </body>
    </html>
    """
    return html


# ============================================
# 后台自动Token刷新机制
# ============================================

# 全局定时器控制
_background_timer = None
_timer_running = False


def _background_token_monitor():
    """后台token监控函数 - 简化版本，复用统一刷新逻辑"""
    global _timer_running
    
    if not _timer_running:
        return
    
    try:
        with _token_lock:
            # 检查是否需要刷新token
            if (_token_storage.get('access_token') and 
                _token_storage.get('refresh_token') and 
                _token_storage.get('expires_at')):
                
                current_time = time.time()
                expires_at = _token_storage['expires_at']
                
                # 检查token是否即将过期或已过期
                needs_refresh = (
                    current_time > (expires_at - TOKEN_REFRESH_THRESHOLD) or
                    current_time >= expires_at
                )
                
                if needs_refresh:
                    print("[Monitor] Token需要刷新，调用内部刷新函数")
                    refreshed_token = _refresh_token_unlocked(source="background_monitor")
                    
                    if refreshed_token:
                        print("[Monitor] 后台token刷新成功")
                    else:
                        print("[Monitor] 后台token刷新失败")
                        
                        # 如果refresh_token已被清除，说明过期了，停止监控器
                        if not _token_storage.get('refresh_token'):
                            print("[Monitor] Refresh token已过期，停止后台监控")
                            stop_background_token_monitor()
                            return
    
    except Exception as e:
        print(f"[Monitor] 后台token监控异常: {str(e)}")
    
    # 安排下一次检查（如果定时器仍在运行）
    if _timer_running:
        _schedule_next_check()


def _schedule_next_check():
    """安排下一次token检查"""
    global _background_timer
    
    if not _timer_running:
        return
    
    # cancel之前的定时器（如果存在）
    if _background_timer:
        _background_timer.cancel()
    
    # 每1分钟检查一次token状态（从5分钟优化到1分钟）
    check_interval = 60  # 1分钟 = 60秒
    
    _background_timer = threading.Timer(check_interval, _background_token_monitor)
    # 设置为守护线程，允许程序正常退出
    _background_timer.daemon = True
    _background_timer.start()


def start_background_token_monitor():
    """启动后台token监控"""
    global _timer_running, _background_timer
    
    if _timer_running:
        print("[Monitor] Background token monitor is already running")
        return
    
    if not config.AUTO_REFRESH_ENABLED:
        print("[Monitor] Auto refresh is disabled in config")
        return
    
    _timer_running = True
    print("[Monitor] Starting background token monitor...")
    
    # 延迟执行第一次检查，避免阻塞启动过程
    # 使用线程来执行第一次检查，避免阻塞主线程
    def _delayed_first_check():
        # 等待2秒让Flask完全启动
        threading.Timer(2.0, _background_token_monitor).start()
    
    # 在单独的线程中启动延迟检查
    threading.Thread(target=_delayed_first_check, daemon=True).start()


def stop_background_token_monitor():
    """停止后台token监控"""
    global _timer_running, _background_timer
    
    # 如果已经停止，不重复执行
    if not _timer_running and _background_timer is None:
        return
    
    _timer_running = False
    
    if _background_timer:
        _background_timer.cancel()
        _background_timer = None
    
    print("[Monitor] Background token monitor stopped")


def get_monitor_status():
    """获取监控状态"""
    return {
        'is_running': _timer_running,
        'has_timer': _background_timer is not None,
        'auto_refresh_enabled': config.AUTO_REFRESH_ENABLED
    }


def get_two_legged_token():
    """
    获取2-legged OAuth token (Client Credentials)
    用于访问账户级别的API
    """
    with _token_lock:
        current_time = time.time()
        
        # 检查现有token是否有效
        if (_two_legged_token_storage['access_token'] and 
            _two_legged_token_storage['expires_at'] and 
            current_time < _two_legged_token_storage['expires_at'] - 60):  # 提前1分钟刷新
            return _two_legged_token_storage['access_token']
        
        # 获取新的2-legged token
        try:
            print("🔄 获取2-legged OAuth token...")
            
            token_url = "https://developer.api.autodesk.com/authentication/v2/token"
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
            }
            
            data = {
                'client_id': config.CLIENT_ID,
                'client_secret': config.CLIENT_SECRET,
                'grant_type': 'client_credentials',
                'scope': 'account:read'  # 只需要account:read权限
            }
            
            response = requests.post(token_url, headers=headers, data=data)
            
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get('access_token')
                expires_in = token_data.get('expires_in', 3600)
                
                # 存储token
                _two_legged_token_storage['access_token'] = access_token
                _two_legged_token_storage['expires_at'] = current_time + expires_in
                _two_legged_token_storage['updated_at'] = current_time
                
                print(f"✅ 2-legged token获取成功，有效期: {expires_in} 秒")
                return access_token
            else:
                error_msg = f"获取2-legged token失败: {response.status_code} - {response.text}"
                print(f"❌ {error_msg}")
                return None
                
        except Exception as e:
            print(f"❌ 获取2-legged token时出错: {str(e)}")
            return None