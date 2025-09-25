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
                    print("🔄 No expiry info, refreshing token...")
                elif current_time >= expires_at:
                    should_refresh = True 
                    print("🔄 Token expired, refreshing...")
                elif current_time > (expires_at - TOKEN_REFRESH_THRESHOLD):
                    should_refresh = True
                    print(f"🔄 Token expires in {int((expires_at - current_time)/60)} min, refreshing...")
                
                if should_refresh:
                    # 临时绕过频率限制，允许即时刷新
                    original_last_attempt = _token_storage.get('last_refresh_attempt')
                    if (original_last_attempt and 
                        current_time - original_last_attempt < REFRESH_RETRY_DELAY):
                        print("⚠️ Bypassing refresh frequency limit for immediate request")
                        _token_storage['last_refresh_attempt'] = None
                    
                    refreshed_token = _attempt_token_refresh()
                    if refreshed_token:
                        return refreshed_token
                    
                    # 如果刷新失败，恢复原始的last_attempt时间
                    if original_last_attempt:
                        _token_storage['last_refresh_attempt'] = original_last_attempt
            
            # 如果token还没完全过期，临时返回原token
            if expires_at and current_time < expires_at:
                print("⚠️ Using potentially expired token temporarily")
                return _token_storage['access_token']
        
        # 2. 尝试从持久化存储加载
        if _load_from_persistent_storage():
            return _token_storage['access_token']
        
        # 3. 尝试从会话获取
        if _load_from_session():
            return _token_storage['access_token']
        
        # 4. 兼容旧版本文件存储
        return _get_token_from_file()


def _attempt_token_refresh():
    """尝试刷新access token"""
    if not _token_storage['refresh_token']:
        print("No refresh token available")
        return None
    
    # 检查刷新频率限制
    current_time = time.time()
    if (_token_storage['last_refresh_attempt'] and 
        current_time - _token_storage['last_refresh_attempt'] < REFRESH_RETRY_DELAY):
        print("Refresh attempt too frequent, skipping")
        return None
    
    if _token_storage['refresh_attempts'] >= config.MAX_TOKEN_REFRESH_ATTEMPTS:
        print(f"Max refresh attempts ({config.MAX_TOKEN_REFRESH_ATTEMPTS}) exceeded")
        return None
    
    try:
        print("🔄 Attempting to refresh access token...")
        _token_storage['last_refresh_attempt'] = current_time
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
            
            # 保存新的token
            success = save_tokens(
                access_token=token_data.get('access_token'),
                refresh_token=token_data.get('refresh_token', _token_storage['refresh_token']),
                expires_in=token_data.get('expires_in', 3600)
            )
            
            if success:
                # 重置刷新计数器
                _token_storage['refresh_attempts'] = 0
                print("✅ Token refreshed successfully")
                return token_data.get('access_token')
        else:
            print(f"❌ Token refresh failed: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Token refresh error: {str(e)}")
    
    return None


def save_tokens(access_token, refresh_token=None, expires_in=3600):
    """保存tokens到多个存储层"""
    with _token_lock:
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
        
        print(f"✅ Token saved successfully: {access_token[:20]}... (expires in {expires_in}s)")
        return True


def _save_to_session(access_token, refresh_token, expires_at):
    """保存到Flask会话"""
    try:
        if session and hasattr(session, '__setitem__'):
            session['access_token'] = access_token
            session['token_expires_at'] = expires_at
            if refresh_token:
                session['refresh_token'] = refresh_token
            session.permanent = True  # 使会话持久化
            print("📝 Token saved to session")
    except Exception as e:
        print(f"⚠️ Failed to save to session: {e}")


def _save_to_persistent_storage():
    """保存到持久化文件"""
    try:
        token_data = {
            'access_token': _token_storage['access_token'],
            'refresh_token': _token_storage['refresh_token'],
            'expires_at': _token_storage['expires_at'],
            'updated_at': _token_storage['updated_at'],
            'next_auto_refresh_at': _token_storage['next_auto_refresh_at'],
            'saved_at': time.time()
        }
        
        with open(PERSISTENT_TOKEN_FILE, 'w') as f:
            json.dump(token_data, f, indent=2)
        
        print("💾 Token saved to persistent storage")
    except Exception as e:
        print(f"⚠️ Failed to save to persistent storage: {e}")


def _load_from_persistent_storage():
    """从持久化存储加载token"""
    try:
        if not os.path.exists(PERSISTENT_TOKEN_FILE):
            return False
        
        with open(PERSISTENT_TOKEN_FILE, 'r') as f:
            token_data = json.load(f)
        
        expires_at = token_data.get('expires_at')
        current_time = time.time()
        
        # 检查token是否仍然有效
        if expires_at and current_time < (expires_at - TOKEN_REFRESH_THRESHOLD):
            _token_storage.update({
                'access_token': token_data.get('access_token'),
                'refresh_token': token_data.get('refresh_token'),
                'expires_at': expires_at,
                'updated_at': token_data.get('updated_at'),
                'next_auto_refresh_at': token_data.get('next_auto_refresh_at', expires_at - TOKEN_REFRESH_THRESHOLD if expires_at else None),
                'refresh_attempts': 0
            })
            print("📂 Token loaded from persistent storage")
            return True
        else:
            print("📂 Persistent token expired, attempting refresh")
            # 如果token过期但有refresh_token，尝试刷新
            if token_data.get('refresh_token'):
                _token_storage['refresh_token'] = token_data.get('refresh_token')
                return _attempt_token_refresh() is not None
            
    except Exception as e:
        print(f"⚠️ Failed to load from persistent storage: {e}")
    
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
                print("🔄 Token loaded from session")
                return True
        
    except Exception as e:
        print(f"⚠️ Failed to load from session: {e}")
    
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
            print(f"⚠️ Failed to clear session: {e}")
        
        # 清除持久化存储
        try:
            if os.path.exists(PERSISTENT_TOKEN_FILE):
                os.remove(PERSISTENT_TOKEN_FILE)
                print("🗑️ Persistent token file removed")
        except Exception as e:
            print(f"⚠️ Failed to remove persistent token file: {e}")
        
        # 清除旧版本文件
        try:
            if hasattr(config, 'TOKEN_FILE') and os.path.exists(config.TOKEN_FILE):
                os.remove(config.TOKEN_FILE)
                print("🗑️ Legacy token file removed")
        except Exception as e:
            print(f"⚠️ Failed to remove legacy token file: {e}")
        
        print("🧹 All tokens cleared")


def is_token_valid():
    """检查token是否有效"""
    token = get_access_token()
    return token is not None


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
    """强制刷新token"""
    with _token_lock:
        if not _token_storage.get('refresh_token'):
            return False, "No refresh token available"
        
        # 重置刷新计数器以允许强制刷新
        _token_storage['refresh_attempts'] = 0
        _token_storage['last_refresh_attempt'] = None
        
        refreshed_token = _attempt_token_refresh()
        if refreshed_token:
            return True, "Token refreshed successfully"
        else:
            return False, "Token refresh failed"


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
            print("📦 Migrated token from legacy file storage")
        
        return access_token
        
    except Exception as e:
        print(f"⚠️ Error reading legacy token file: {str(e)}")
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
                return "✅ Token 已保存到增强存储系统"
        
        return "❌ 无效的token数据格式"
    except Exception as e:
        return f"❌ 保存 token 失败: {str(e)}"


# 导入原有的其他工具函数
def get_real_account_id(projects_data):
    """从项目数据中提取真实的 Account ID"""
    if "data" not in projects_data or len(projects_data["data"]) == 0:
        return None, None, None
    
    hub_id = projects_data["data"][0]["id"]
    real_account_id = hub_id[2:] if hub_id.startswith("b.") else hub_id
    hub_name = projects_data["data"][0]["attributes"]["name"]
    
    return hub_id, real_account_id, hub_name


def format_timestamp(timestamp_str):
    """格式化时间戳字符串"""
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
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
    """后台token监控函数"""
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
                
                # 简化的刷新条件：token即将过期（10分钟内）或已过期
                needs_refresh = (
                    current_time > (expires_at - TOKEN_REFRESH_THRESHOLD) or
                    current_time >= expires_at
                )
                
                # 频率限制：避免过于频繁的刷新尝试
                can_refresh = (
                    _token_storage.get('last_refresh_attempt') is None or
                    current_time - _token_storage['last_refresh_attempt'] > REFRESH_RETRY_DELAY
                )
                
                if needs_refresh and can_refresh:
                    
                    print("🔄 Background token monitor: Token needs refresh")
                    refreshed_token = _attempt_token_refresh()
                    if refreshed_token:
                        print("✅ Background token monitor: Token refreshed successfully")
                    else:
                        print("❌ Background token monitor: Token refresh failed")
    
    except Exception as e:
        print(f"⚠️ Background token monitor error: {str(e)}")
    
    # 安排下一次检查（如果定时器仍在运行）
    if _timer_running:
        _schedule_next_check()


def _schedule_next_check():
    """安排下一次token检查"""
    global _background_timer
    
    if not _timer_running:
        return
    
    # 每1分钟检查一次token状态（从5分钟优化到1分钟）
    check_interval = 60  # 1分钟 = 60秒
    
    _background_timer = threading.Timer(check_interval, _background_token_monitor)
    _background_timer.daemon = True  # 设置为守护线程，主程序退出时自动结束
    _background_timer.start()


def start_background_token_monitor():
    """启动后台token监控"""
    global _timer_running, _background_timer
    
    if _timer_running:
        print("🔄 Background token monitor is already running")
        return
    
    if not config.AUTO_REFRESH_ENABLED:
        print("🔄 Auto refresh is disabled in config")
        return
    
    _timer_running = True
    print("🚀 Starting background token monitor...")
    
    # 立即执行一次检查
    _background_token_monitor()


def stop_background_token_monitor():
    """停止后台token监控"""
    global _timer_running, _background_timer
    
    _timer_running = False
    
    if _background_timer:
        _background_timer.cancel()
        _background_timer = None
    
    print("⏹️ Background token monitor stopped")


def get_monitor_status():
    """获取监控状态"""
    return {
        'is_running': _timer_running,
        'has_timer': _background_timer is not None,
        'auto_refresh_enabled': config.AUTO_REFRESH_ENABLED
    }