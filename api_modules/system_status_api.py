# -*- coding: utf-8 -*-
"""
系统状态API模块 - 优化版本
提供全面的系统健康检查、API状态监控和性能指标
"""

import time
import psutil
import threading
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
import requests
import config
import utils

system_status_bp = Blueprint('system_status', __name__)

# 系统状态缓存
_status_cache = {
    'last_update': None,
    'system_health': {},
    'api_status': {},
    'performance_metrics': {},
    'cache_duration': 30  # 缓存30秒
}

# 状态检查锁
_status_lock = threading.Lock()

def get_system_performance():
    """获取系统性能指标"""
    try:
        # CPU使用率
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # 内存使用情况
        memory = psutil.virtual_memory()
        memory_info = {
            'total': memory.total,
            'available': memory.available,
            'percent': memory.percent,
            'used': memory.used
        }
        
        # 磁盘使用情况
        disk = psutil.disk_usage('/')
        disk_info = {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'percent': (disk.used / disk.total) * 100
        }
        
        # 网络统计
        network = psutil.net_io_counters()
        network_info = {
            'bytes_sent': network.bytes_sent,
            'bytes_recv': network.bytes_recv,
            'packets_sent': network.packets_sent,
            'packets_recv': network.packets_recv
        }
        
        return {
            'cpu_percent': cpu_percent,
            'memory': memory_info,
            'disk': disk_info,
            'network': network_info,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'error': f'获取系统性能指标失败: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }

def check_api_endpoints_health():
    """检查关键API端点的健康状态"""
    endpoints_to_check = [
        {'path': '/api/auth/check', 'method': 'GET', 'name': 'Authentication Check'},
        {'path': '/api/auth/token-info', 'method': 'GET', 'name': 'Token Information'},
        {'path': '/health', 'method': 'GET', 'name': 'Basic Health Check'},
    ]
    
    results = {}
    base_url = f"http://127.0.0.1:{config.PORT}"
    
    for endpoint in endpoints_to_check:
        start_time = time.time()
        try:
            if endpoint['method'] == 'GET':
                response = requests.get(f"{base_url}{endpoint['path']}", timeout=5)
            else:
                response = requests.post(f"{base_url}{endpoint['path']}", timeout=5)
            
            response_time = (time.time() - start_time) * 1000  # 转换为毫秒
            
            results[endpoint['path']] = {
                'name': endpoint['name'],
                'status': 'healthy' if response.status_code < 400 else 'unhealthy',
                'status_code': response.status_code,
                'response_time_ms': round(response_time, 2),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            results[endpoint['path']] = {
                'name': endpoint['name'],
                'status': 'error',
                'error': str(e),
                'response_time_ms': round(response_time, 2),
                'timestamp': datetime.now().isoformat()
            }
    
    return results

def get_token_health_status():
    """获取Token健康状态"""
    try:
        token_info = utils.get_token_info()
        monitor_status = utils.get_monitor_status()
        
        # 判断Token整体健康状态
        if token_info.get('is_valid'):
            if token_info.get('expires_in_minutes', 0) > 30:
                token_health = 'healthy'
            elif token_info.get('expires_in_minutes', 0) > 10:
                token_health = 'warning'
            else:
                token_health = 'critical'
        else:
            token_health = 'invalid'
        
        return {
            'health_status': token_health,
            'token_info': token_info,
            'monitor_status': monitor_status,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'health_status': 'error',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def get_api_modules_status():
    """获取所有API模块的状态"""
    modules = [
        'auth_api', 'forms_api', 'data_connector_api', 'reviews_api', 
        'rfis_api', 'file_sync_api', 'data_management_api', 'webhook_api',
        'download_config_api', 'permissions_sync_api', 'users_api',
        'custom_attributes_api', 'account_api', 'issues_api', 'submittals_api'
    ]
    
    module_status = {}
    for module in modules:
        try:
            # 检查模块是否已注册（通过检查蓝图）
            from flask import current_app
            blueprints = current_app.blueprints
            
            # 根据模块名推断蓝图名
            blueprint_name = module.replace('_api', '')
            
            if blueprint_name in blueprints:
                module_status[module] = {
                    'status': 'registered',
                    'blueprint_name': blueprint_name,
                    'endpoints_count': len(blueprints[blueprint_name].deferred_functions)
                }
            else:
                module_status[module] = {
                    'status': 'not_registered',
                    'blueprint_name': blueprint_name
                }
        except Exception as e:
            module_status[module] = {
                'status': 'error',
                'error': str(e)
            }
    
    return module_status

@system_status_bp.route('/api/system-status/health', methods=['GET'])
def comprehensive_health_check():
    """综合健康检查端点"""
    try:
        with _status_lock:
            current_time = time.time()
            
            # 检查缓存是否有效
            if (_status_cache['last_update'] and 
                current_time - _status_cache['last_update'] < _status_cache['cache_duration']):
                return jsonify({
                    'status': 'success',
                    'cached': True,
                    'cache_age_seconds': round(current_time - _status_cache['last_update'], 2),
                    **_status_cache['system_health']
                })
            
            # 获取各项健康指标
            performance_metrics = get_system_performance()
            api_endpoints_health = check_api_endpoints_health()
            token_health = get_token_health_status()
            modules_status = get_api_modules_status()
            
            # 计算整体健康状态
            overall_health = 'healthy'
            health_issues = []
            
            # 检查系统性能
            if performance_metrics.get('cpu_percent', 0) > 80:
                overall_health = 'warning'
                health_issues.append('CPU使用率过高')
            
            if performance_metrics.get('memory', {}).get('percent', 0) > 85:
                overall_health = 'warning'
                health_issues.append('High memory usage')
            
            # 检查Token状态
            if token_health.get('health_status') in ['critical', 'invalid']:
                overall_health = 'critical'
                health_issues.append('Token状态异常')
            elif token_health.get('health_status') == 'warning':
                if overall_health == 'healthy':
                    overall_health = 'warning'
                health_issues.append('Token即将过期')
            
            # 检查API端点
            unhealthy_endpoints = [
                path for path, status in api_endpoints_health.items() 
                if status.get('status') != 'healthy'
            ]
            if unhealthy_endpoints:
                if overall_health == 'healthy':
                    overall_health = 'warning'
                health_issues.append(f'{len(unhealthy_endpoints)}个API端点异常')
            
            # 构建响应
            health_data = {
                'overall_health': overall_health,
                'health_issues': health_issues,
                'performance_metrics': performance_metrics,
                'api_endpoints_health': api_endpoints_health,
                'token_health': token_health,
                'modules_status': modules_status,
                'system_info': {
                    'timestamp': datetime.now().isoformat(),
                    'uptime_seconds': time.time() - getattr(config, 'START_TIME', time.time()),
                    'version': getattr(config, 'VERSION', '1.0.0')
                }
            }
            
            # 更新缓存
            _status_cache['last_update'] = current_time
            _status_cache['system_health'] = health_data
            
            return jsonify({
                'status': 'success',
                'cached': False,
                **health_data
            })
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'健康检查失败: {str(e)}',
            'timestamp': datetime.now().isoformat()
        }), 500

@system_status_bp.route('/api/system-status/performance', methods=['GET'])
def get_performance_metrics():
    """获取系统性能指标"""
    try:
        metrics = get_system_performance()
        return jsonify({
            'status': 'success',
            'performance_metrics': metrics
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'获取性能指标失败: {str(e)}'
        }), 500

@system_status_bp.route('/api/system-status/api-endpoints', methods=['GET'])
def get_api_endpoints_status():
    """获取API端点状态"""
    try:
        endpoints_health = check_api_endpoints_health()
        return jsonify({
            'status': 'success',
            'api_endpoints': endpoints_health,
            'summary': {
                'total_endpoints': len(endpoints_health),
                'healthy_endpoints': len([e for e in endpoints_health.values() if e.get('status') == 'healthy']),
                'unhealthy_endpoints': len([e for e in endpoints_health.values() if e.get('status') != 'healthy'])
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'获取API端点状态失败: {str(e)}'
        }), 500

@system_status_bp.route('/api/system-status/token', methods=['GET'])
def get_token_status():
    """获取Token状态详情"""
    try:
        token_health = get_token_health_status()
        return jsonify({
            'status': 'success',
            'token_health': token_health
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'获取Token状态失败: {str(e)}'
        }), 500

@system_status_bp.route('/api/system-status/modules', methods=['GET'])
def get_modules_status():
    """获取API模块状态"""
    try:
        modules_status = get_api_modules_status()
        
        # 统计信息
        total_modules = len(modules_status)
        registered_modules = len([m for m in modules_status.values() if m.get('status') == 'registered'])
        
        return jsonify({
            'status': 'success',
            'modules_status': modules_status,
            'summary': {
                'total_modules': total_modules,
                'registered_modules': registered_modules,
                'unregistered_modules': total_modules - registered_modules
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'获取模块状态失败: {str(e)}'
        }), 500

@system_status_bp.route('/api/system-status/cache/clear', methods=['POST'])
def clear_status_cache():
    """清除状态缓存"""
    try:
        with _status_lock:
            _status_cache['last_update'] = None
            _status_cache['system_health'] = {}
            _status_cache['api_status'] = {}
            _status_cache['performance_metrics'] = {}
        
        return jsonify({
            'status': 'success',
            'message': 'Status cache cleared'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'清除缓存失败: {str(e)}'
        }), 500

@system_status_bp.route('/api/system-status/config', methods=['GET'])
def get_system_config():
    """获取系统配置信息"""
    try:
        config_info = {
            'debug_mode': getattr(config, 'DEBUG', False),
            'port': getattr(config, 'PORT', 5000),
            'auto_refresh_enabled': getattr(config, 'AUTO_REFRESH_ENABLED', True),
            'max_token_refresh_attempts': getattr(config, 'MAX_TOKEN_REFRESH_ATTEMPTS', 3),
            'token_refresh_threshold': getattr(utils, 'TOKEN_REFRESH_THRESHOLD', 600),
            'cache_duration': _status_cache['cache_duration'],
            'version': getattr(config, 'VERSION', '1.0.0')
        }
        
        return jsonify({
            'status': 'success',
            'config': config_info
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'获取系统配置失败: {str(e)}'
        }), 500

@system_status_bp.route('/api/system-status/diagnostics', methods=['GET'])
def run_system_diagnostics():
    """运行系统诊断"""
    try:
        diagnostics = {
            'timestamp': datetime.now().isoformat(),
            'checks': {}
        }
        
        # 检查配置完整性
        required_configs = ['CLIENT_ID', 'CLIENT_SECRET', 'CALLBACK_URL', 'SCOPES']
        config_check = {
            'status': 'pass',
            'missing_configs': []
        }
        
        for config_name in required_configs:
            if not hasattr(config, config_name) or not getattr(config, config_name):
                config_check['status'] = 'fail'
                config_check['missing_configs'].append(config_name)
        
        diagnostics['checks']['oauth_config'] = config_check
        
        # 检查Token状态
        token_info = utils.get_token_info()
        token_check = {
            'status': 'pass' if token_info.get('is_valid') else 'fail',
            'has_access_token': token_info.get('has_access_token', False),
            'has_refresh_token': token_info.get('has_refresh_token', False),
            'expires_in_minutes': token_info.get('expires_in_minutes')
        }
        diagnostics['checks']['token_status'] = token_check
        
        # 检查后台监控
        monitor_status = utils.get_monitor_status()
        monitor_check = {
            'status': 'pass' if monitor_status.get('is_running') else 'warning',
            'is_running': monitor_status.get('is_running', False),
            'auto_refresh_enabled': monitor_status.get('auto_refresh_enabled', False)
        }
        diagnostics['checks']['background_monitor'] = monitor_check
        
        # 检查系统资源
        performance = get_system_performance()
        resource_check = {
            'status': 'pass',
            'warnings': []
        }
        
        if performance.get('cpu_percent', 0) > 80:
            resource_check['status'] = 'warning'
            resource_check['warnings'].append('CPU使用率过高')
        
        if performance.get('memory', {}).get('percent', 0) > 85:
            resource_check['status'] = 'warning'
            resource_check['warnings'].append('High memory usage')
        
        diagnostics['checks']['system_resources'] = resource_check
        
        # 计算整体诊断结果
        all_checks = diagnostics['checks'].values()
        if any(check.get('status') == 'fail' for check in all_checks):
            diagnostics['overall_status'] = 'fail'
        elif any(check.get('status') == 'warning' for check in all_checks):
            diagnostics['overall_status'] = 'warning'
        else:
            diagnostics['overall_status'] = 'pass'
        
        return jsonify({
            'status': 'success',
            'diagnostics': diagnostics
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'系统诊断失败: {str(e)}'
        }), 500

# 健康检查端点（兼容性）
@system_status_bp.route('/api/system-status/simple-health', methods=['GET'])
def simple_health_check():
    """简单健康检查端点"""
    return jsonify({
        'status': 'healthy',
        'service': 'ACC数据同步系统',
        'timestamp': datetime.now().isoformat(),
        'version': getattr(config, 'VERSION', '1.0.0')
    })
