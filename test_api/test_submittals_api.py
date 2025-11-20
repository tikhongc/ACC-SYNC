#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Submittal API 完整测试脚本
测试所有 Submittal API 端点的功能
"""

import requests
import json
import sys
import os
from datetime import datetime
from colorama import init, Fore, Style

# 设置控制台编码
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# 初始化 colorama
init(autoreset=True, strip=False, convert=True)

# 测试配置
BASE_URL = "http://127.0.0.1:8080"
PROJECT_ID = "b.1eea4119-3553-4167-b93d-3a3d5d07d33d"  # 使用带 b. 前缀的项目ID

# 测试结果统计
test_results = {
    'total': 0,
    'passed': 0,
    'failed': 0,
    'skipped': 0
}


def print_header(text):
    """打印测试标题"""
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}{text:^80}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")


def print_test(test_name):
    """打印测试名称"""
    print(f"{Fore.YELLOW}[TEST] {test_name}{Style.RESET_ALL}")


def print_success(message):
    """打印成功消息"""
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")


def print_error(message):
    """打印错误消息"""
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")


def print_info(message):
    """打印信息消息"""
    print(f"{Fore.BLUE}ℹ {message}{Style.RESET_ALL}")


def print_warning(message):
    """打印警告消息"""
    print(f"{Fore.MAGENTA}⚠ {message}{Style.RESET_ALL}")


def make_request(method, endpoint, **kwargs):
    """
    发送 HTTP 请求
    
    Args:
        method: HTTP 方法 (GET, POST, etc.)
        endpoint: API 端点
        **kwargs: 其他请求参数
        
    Returns:
        tuple: (success, response, error_message)
    """
    url = f"{BASE_URL}{endpoint}"
    
    try:
        response = requests.request(method, url, timeout=30, **kwargs)
        
        if response.status_code in [200, 201, 204]:
            return True, response, None
        else:
            error_msg = f"状态码 {response.status_code}"
            try:
                error_data = response.json()
                if 'error' in error_data:
                    error_msg += f": {error_data['error']}"
            except:
                error_msg += f": {response.text[:200]}"
            
            return False, response, error_msg
            
    except requests.exceptions.Timeout:
        return False, None, "请求超时"
    except requests.exceptions.ConnectionError:
        return False, None, "连接失败 - 请确保服务器正在运行"
    except Exception as e:
        return False, None, f"请求异常: {str(e)}"


def run_test(test_name, method, endpoint, expected_keys=None, **kwargs):
    """
    运行单个测试
    
    Args:
        test_name: 测试名称
        method: HTTP 方法
        endpoint: API 端点
        expected_keys: 期望响应中包含的键列表
        **kwargs: 其他请求参数
        
    Returns:
        bool: 测试是否通过
    """
    global test_results
    test_results['total'] += 1
    
    print_test(test_name)
    print_info(f"请求: {method} {endpoint}")
    
    success, response, error = make_request(method, endpoint, **kwargs)
    
    if not success:
        print_error(f"测试失败: {error}")
        test_results['failed'] += 1
        return False
    
    # 检查响应内容
    try:
        if response.status_code == 204:
            print_success(f"测试通过 (状态码 {response.status_code})")
            test_results['passed'] += 1
            return True
            
        data = response.json()
        
        # 检查期望的键
        if expected_keys:
            missing_keys = [key for key in expected_keys if key not in data]
            if missing_keys:
                print_error(f"响应缺少键: {', '.join(missing_keys)}")
                test_results['failed'] += 1
                return False
        
        # 打印响应摘要
        if 'results' in data:
            count = len(data.get('results', []))
            print_success(f"测试通过 - 获取 {count} 条记录")
            
            # 显示分页信息
            if 'pagination' in data:
                pagination = data['pagination']
                print_info(f"分页: offset={pagination.get('offset', 0)}, "
                          f"limit={pagination.get('limit', 0)}, "
                          f"totalResults={pagination.get('totalResults', 0)}")
        else:
            print_success(f"测试通过")
        
        test_results['passed'] += 1
        return True
        
    except json.JSONDecodeError:
        print_error("响应不是有效的 JSON")
        test_results['failed'] += 1
        return False
    except Exception as e:
        print_error(f"验证响应时出错: {str(e)}")
        test_results['failed'] += 1
        return False


def test_get_items():
    """测试获取 Submittal 项目列表"""
    print_header("测试 1: 获取 Submittal 项目列表")
    
    # 测试 1.1: 基本获取
    result1 = run_test(
        "获取项目列表 (默认参数)",
        "GET",
        f"/api/submittals/{PROJECT_ID}/items",
        expected_keys=['results', 'pagination']
    )
    
    # 测试 1.2: 带分页参数
    result2 = run_test(
        "获取项目列表 (limit=10, offset=0)",
        "GET",
        f"/api/submittals/{PROJECT_ID}/items?limit=10&offset=0",
        expected_keys=['results', 'pagination']
    )
    
    # 测试 1.3: 带排序参数
    result3 = run_test(
        "获取项目列表 (按更新时间降序)",
        "GET",
        f"/api/submittals/{PROJECT_ID}/items?sort=updatedAt+desc&limit=5",
        expected_keys=['results', 'pagination']
    )
    
    # 测试 1.4: 带状态过滤
    result4 = run_test(
        "获取项目列表 (过滤开放状态)",
        "GET",
        f"/api/submittals/{PROJECT_ID}/items?filter[statusId]=2&limit=10",
        expected_keys=['results', 'pagination']
    )
    
    return all([result1, result2, result3, result4])


def test_get_item():
    """测试获取单个 Submittal 项目"""
    print_header("测试 2: 获取单个 Submittal 项目")
    
    # 首先获取一个项目ID
    print_info("先获取一个项目ID用于测试...")
    success, response, error = make_request(
        "GET",
        f"/api/submittals/{PROJECT_ID}/items?limit=1"
    )
    
    if not success or not response:
        print_warning("无法获取项目ID，跳过此测试")
        test_results['total'] += 1
        test_results['skipped'] += 1
        return False
    
    try:
        data = response.json()
        items = data.get('results', [])
        
        if not items:
            print_warning("项目中没有 Submittal 项目，跳过此测试")
            test_results['total'] += 1
            test_results['skipped'] += 1
            return False
        
        item_id = items[0]['id']
        print_info(f"使用项目ID: {item_id}")
        
        # 测试获取单个项目
        result = run_test(
            "获取单个项目详情",
            "GET",
            f"/api/submittals/{PROJECT_ID}/items/{item_id}",
            expected_keys=['id', 'title']
        )
        
        return result
        
    except Exception as e:
        print_error(f"获取项目ID时出错: {str(e)}")
        test_results['total'] += 1
        test_results['skipped'] += 1
        return False


def test_get_attachments():
    """测试获取附件列表"""
    print_header("测试 3: 获取 Submittal 附件")
    
    # 首先获取一个项目ID
    print_info("先获取一个项目ID用于测试...")
    success, response, error = make_request(
        "GET",
        f"/api/submittals/{PROJECT_ID}/items?limit=1"
    )
    
    if not success or not response:
        print_warning("无法获取项目ID，跳过此测试")
        test_results['total'] += 1
        test_results['skipped'] += 1
        return False
    
    try:
        data = response.json()
        items = data.get('results', [])
        
        if not items:
            print_warning("项目中没有 Submittal 项目，跳过此测试")
            test_results['total'] += 1
            test_results['skipped'] += 1
            return False
        
        item_id = items[0]['id']
        print_info(f"使用项目ID: {item_id}")
        
        # 测试获取附件
        result = run_test(
            "获取项目附件列表",
            "GET",
            f"/api/submittals/{PROJECT_ID}/items/{item_id}/attachments",
            expected_keys=['results', 'pagination']
        )
        
        return result
        
    except Exception as e:
        print_error(f"测试附件时出错: {str(e)}")
        test_results['total'] += 1
        test_results['skipped'] += 1
        return False


def test_get_revisions():
    """测试获取修订历史"""
    print_header("测试 4: 获取 Submittal 修订历史")
    
    # 首先获取一个项目ID
    print_info("先获取一个项目ID用于测试...")
    success, response, error = make_request(
        "GET",
        f"/api/submittals/{PROJECT_ID}/items?limit=1"
    )
    
    if not success or not response:
        print_warning("无法获取项目ID，跳过此测试")
        test_results['total'] += 1
        test_results['skipped'] += 1
        return False
    
    try:
        data = response.json()
        items = data.get('results', [])
        
        if not items:
            print_warning("项目中没有 Submittal 项目，跳过此测试")
            test_results['total'] += 1
            test_results['skipped'] += 1
            return False
        
        item_id = items[0]['id']
        print_info(f"使用项目ID: {item_id}")
        
        # 测试获取修订历史
        result = run_test(
            "获取项目修订历史",
            "GET",
            f"/api/submittals/{PROJECT_ID}/items/{item_id}/revisions",
            expected_keys=['results', 'pagination']
        )
        
        return result
        
    except Exception as e:
        print_error(f"测试修订历史时出错: {str(e)}")
        test_results['total'] += 1
        test_results['skipped'] += 1
        return False


def test_get_metadata():
    """测试获取元数据"""
    print_header("测试 5: 获取项目元数据")
    
    result = run_test(
        "获取项目元数据 (responses, itemTypes, templates, specs)",
        "GET",
        f"/api/submittals/{PROJECT_ID}/metadata",
        expected_keys=['responses', 'itemTypes', 'templates', 'specs']
    )
    
    return result


def test_get_responses():
    """测试获取响应类型"""
    print_header("测试 6: 获取响应类型列表")
    
    result = run_test(
        "获取项目响应类型",
        "GET",
        f"/api/submittals/{PROJECT_ID}/responses",
        expected_keys=['results', 'pagination']
    )
    
    return result


def test_get_item_types():
    """测试获取项目类型"""
    print_header("测试 7: 获取 Submittal 类型")
    
    result = run_test(
        "获取 Submittal 类型列表",
        "GET",
        f"/api/submittals/{PROJECT_ID}/item-types",
        expected_keys=['results', 'pagination']
    )
    
    return result


def test_get_templates():
    """测试获取审核流程模板"""
    print_header("测试 8: 获取审核流程模板")
    
    result = run_test(
        "获取审核流程模板列表",
        "GET",
        f"/api/submittals/{PROJECT_ID}/templates",
        expected_keys=['results', 'pagination']
    )
    
    return result


def test_get_specs():
    """测试获取规格列表"""
    print_header("测试 9: 获取规格列表")
    
    result = run_test(
        "获取项目规格列表",
        "GET",
        f"/api/submittals/{PROJECT_ID}/specs",
        expected_keys=['results', 'pagination']
    )
    
    return result


def test_get_packages():
    """测试获取包列表"""
    print_header("测试 10: 获取 Submittal 包")
    
    result = run_test(
        "获取 Submittal 包列表",
        "GET",
        f"/api/submittals/{PROJECT_ID}/packages",
        expected_keys=['results', 'pagination']
    )
    
    return result


def test_jarvis_endpoints():
    """测试 Jarvis 端点"""
    print_header("测试 11: Jarvis 端点")
    
    # 测试 11.1: 获取所有数据
    result1 = run_test(
        "Jarvis - 获取完整数据",
        "GET",
        f"/api/submittals/jarvis/{PROJECT_ID}",
        expected_keys=['items', 'metadata', 'packages']
    )
    
    # 测试 11.2: 获取所有元数据
    result2 = run_test(
        "Jarvis - 获取所有元数据",
        "GET",
        f"/api/submittals/jarvis/{PROJECT_ID}/metadata",
        expected_keys=['responses', 'itemTypes', 'templates', 'specs']
    )
    
    return all([result1, result2])


def print_summary():
    """打印测试摘要"""
    print_header("测试摘要")
    
    total = test_results['total']
    passed = test_results['passed']
    failed = test_results['failed']
    skipped = test_results['skipped']
    
    pass_rate = (passed / total * 100) if total > 0 else 0
    
    print(f"总测试数: {total}")
    print(f"{Fore.GREEN}通过: {passed}{Style.RESET_ALL}")
    print(f"{Fore.RED}失败: {failed}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}跳过: {skipped}{Style.RESET_ALL}")
    print(f"\n通过率: {Fore.GREEN if pass_rate >= 80 else Fore.YELLOW}{pass_rate:.1f}%{Style.RESET_ALL}")
    
    if failed == 0 and skipped == 0:
        print(f"\n{Fore.GREEN}{'🎉 所有测试通过！':^80}{Style.RESET_ALL}")
    elif failed == 0:
        print(f"\n{Fore.YELLOW}{'⚠ 部分测试被跳过':^80}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}{'❌ 部分测试失败':^80}{Style.RESET_ALL}")


def main():
    """主测试函数"""
    print_header("Submittal API 完整测试")
    print_info(f"测试服务器: {BASE_URL}")
    print_info(f"测试项目: {PROJECT_ID}")
    print_info(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查服务器连接
    print_info("\n检查服务器连接...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print_success("服务器连接正常")
    except Exception as e:
        print_error(f"无法连接到服务器: {str(e)}")
        print_error("请确保 Flask 服务器正在运行 (python app.py)")
        sys.exit(1)
    
    # 运行所有测试
    try:
        test_get_items()
        test_get_item()
        test_get_attachments()
        test_get_revisions()
        test_get_metadata()
        test_get_responses()
        test_get_item_types()
        test_get_templates()
        test_get_specs()
        test_get_packages()
        test_jarvis_endpoints()
        
    except KeyboardInterrupt:
        print_warning("\n\n测试被用户中断")
    except Exception as e:
        print_error(f"\n\n测试过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # 打印摘要
    print_summary()
    
    # 返回退出码
    sys.exit(0 if test_results['failed'] == 0 else 1)


if __name__ == "__main__":
    main()

