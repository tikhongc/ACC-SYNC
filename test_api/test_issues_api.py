#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Issues API 完整测试脚本
测试所有 Issues API 端点，包括使用模拟数据
"""

import sys
import io
import requests
import json
import time
from datetime import datetime, timedelta

# 设置UTF-8输出（Windows兼容）
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 测试配置
BASE_URL = "http://localhost:8080"
TEST_PROJECT_ID = "b.1eea4119-3553-4167-b93d-3a3d5d07d33d"

# 测试结果统计
test_results = {
    "passed": [],
    "failed": [],
    "skipped": []
}

def print_header(title):
    """打印标题"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def print_test(test_name):
    """打印测试名称"""
    print(f"\n【测试】{test_name}")
    print("-" * 70)

def record_result(test_name, passed, message=""):
    """记录测试结果"""
    if passed:
        test_results["passed"].append(test_name)
        print(f"✅ 通过: {test_name}")
    else:
        test_results["failed"].append((test_name, message))
        print(f"❌ 失败: {test_name}")
        if message:
            print(f"   原因: {message}")

def test_auth_status():
    """测试认证状态"""
    print_test("1. 认证状态检查")
    try:
        response = requests.get(f"{BASE_URL}/api/auth/check", timeout=10)
        result = response.json()
        
        print(f"状态码: {response.status_code}")
        
        if result.get("authenticated"):
            print(f"✅ 用户已认证")
            if result.get("user_info"):
                print(f"用户信息: {result['user_info'].get('name', 'N/A')}")
            record_result("认证检查", True)
            return True
        else:
            print("❌ 用户未认证")
            record_result("认证检查", False, "用户未认证")
            return False
    except Exception as e:
        print(f"❌ 异常: {str(e)}")
        record_result("认证检查", False, str(e))
        return False

def test_user_profile():
    """测试用户档案 API"""
    print_test("2. 用户档案 - GET /api/issues/projects/{projectId}/user-profile")
    try:
        url = f"{BASE_URL}/api/issues/projects/{TEST_PROJECT_ID}/user-profile"
        start = time.time()
        response = requests.get(url, timeout=30)
        elapsed = time.time() - start
        
        print(f"状态码: {response.status_code}")
        print(f"响应时间: {elapsed:.2f}s")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                profile = result.get("data", {})
                print(f"✅ 成功")
                print(f"   用户ID: {profile.get('id', 'N/A')}")
                print(f"   项目管理员: {profile.get('isProjectAdmin', False)}")
                print(f"   权限: {profile.get('permissionLevels', [])}")
                record_result("用户档案API", True)
                return True
        
        record_result("用户档案API", False, response.text[:100])
        return False
    except Exception as e:
        record_result("用户档案API", False, str(e))
        return False

def test_issue_types():
    """测试议题类型 API"""
    print_test("3. 议题类型 - GET /api/issues/projects/{projectId}/issue-types")
    try:
        url = f"{BASE_URL}/api/issues/projects/{TEST_PROJECT_ID}/issue-types"
        start = time.time()
        response = requests.get(url, params={"includeSubtypes": "true", "limit": 20}, timeout=30)
        elapsed = time.time() - start
        
        print(f"状态码: {response.status_code}")
        print(f"响应时间: {elapsed:.2f}s")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                types = result.get("data", {}).get("results", [])
                print(f"✅ 成功获取 {len(types)} 个议题类型")
                if types:
                    print(f"   示例: {types[0].get('title', 'N/A')}")
                    if types[0].get('subtypes'):
                        print(f"   子类型数: {len(types[0]['subtypes'])}")
                record_result("议题类型API", True)
                return True
        
        record_result("议题类型API", False, response.text[:100])
        return False
    except Exception as e:
        record_result("议题类型API", False, str(e))
        return False

def test_attribute_definitions():
    """测试属性定义 API"""
    print_test("4. 属性定义 - GET /api/issues/projects/{projectId}/attribute-definitions")
    try:
        url = f"{BASE_URL}/api/issues/projects/{TEST_PROJECT_ID}/attribute-definitions"
        start = time.time()
        response = requests.get(url, params={"limit": 20}, timeout=30)
        elapsed = time.time() - start
        
        print(f"状态码: {response.status_code}")
        print(f"响应时间: {elapsed:.2f}s")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                attrs = result.get("data", {}).get("results", [])
                print(f"✅ 成功获取 {len(attrs)} 个属性定义")
                if attrs:
                    print(f"   示例: {attrs[0].get('title')} ({attrs[0].get('dataType')})")
                record_result("属性定义API", True)
                return True
        
        error_msg = response.text[:100] if response.status_code != 502 else "502 Bad Gateway (Autodesk端)"
        record_result("属性定义API", False, error_msg)
        return False
    except Exception as e:
        record_result("属性定义API", False, str(e))
        return False

def test_attribute_mappings():
    """测试属性映射 API"""
    print_test("5. 属性映射 - GET /api/issues/projects/{projectId}/attribute-mappings")
    try:
        url = f"{BASE_URL}/api/issues/projects/{TEST_PROJECT_ID}/attribute-mappings"
        start = time.time()
        response = requests.get(url, params={"limit": 20}, timeout=30)
        elapsed = time.time() - start
        
        print(f"状态码: {response.status_code}")
        print(f"响应时间: {elapsed:.2f}s")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                mappings = result.get("data", {}).get("results", [])
                print(f"✅ 成功获取 {len(mappings)} 个属性映射")
                record_result("属性映射API", True)
                return True
        
        record_result("属性映射API", False, response.text[:100])
        return False
    except Exception as e:
        record_result("属性映射API", False, str(e))
        return False

def test_root_cause_categories():
    """测试根本原因类别 API"""
    print_test("6. 根本原因类别 - GET /api/issues/projects/{projectId}/root-cause-categories")
    try:
        url = f"{BASE_URL}/api/issues/projects/{TEST_PROJECT_ID}/root-cause-categories"
        start = time.time()
        response = requests.get(url, params={"includeRootCauses": "true", "limit": 20}, timeout=60)
        elapsed = time.time() - start
        
        print(f"状态码: {response.status_code}")
        print(f"响应时间: {elapsed:.2f}s")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                categories = result.get("data", {}).get("results", [])
                print(f"✅ 成功获取 {len(categories)} 个根本原因类别")
                record_result("根本原因类别API", True)
                return True
        
        error_msg = "504 Gateway Timeout (Autodesk端)" if response.status_code == 504 else response.text[:100]
        record_result("根本原因类别API", False, error_msg)
        return False
    except Exception as e:
        record_result("根本原因类别API", False, str(e))
        return False

def test_issues_list():
    """测试议题列表 API - 使用 limit=50"""
    print_test("7. 议题列表 - GET /api/issues/projects/{projectId}/list (limit=50)")
    try:
        url = f"{BASE_URL}/api/issues/projects/{TEST_PROJECT_ID}/list"
        start = time.time()
        response = requests.get(url, params={"limit": 50, "_t": int(time.time() * 1000)}, timeout=90)
        elapsed = time.time() - start
        
        print(f"状态码: {response.status_code}")
        print(f"响应时间: {elapsed:.2f}s")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                issues = result.get("data", {}).get("results", [])
                print(f"✅ 成功获取 {len(issues)} 个议题")
                print(f"   分页: limit={result.get('pagination', {}).get('limit')}")
                print(f"   有更多: {result.get('pagination', {}).get('has_more')}")
                
                if issues:
                    first_issue = issues[0]
                    print(f"   示例: {first_issue.get('displayId')} - {first_issue.get('title', 'N/A')[:50]}")
                    record_result("议题列表API (limit=50)", True)
                    return first_issue.get('id')
                else:
                    print(f"   ⚠️  项目中没有议题数据")
                    record_result("议题列表API (limit=50)", True, "无议题数据但API正常")
                    return None
        
        error_msg = "Autodesk API超时" if response.status_code in [500, 504] else response.text[:100]
        record_result("议题列表API (limit=50)", False, error_msg)
        return None
    except Exception as e:
        record_result("议题列表API (limit=50)", False, str(e))
        return None

def test_issue_details(issue_id):
    """测试议题详情 API"""
    print_test("8. 议题详情 - GET /api/issues/projects/{projectId}/issues/{issueId}")
    
    if not issue_id:
        print("⏭️  跳过: 没有可用的议题ID（项目无议题数据）")
        test_results["skipped"].append("议题详情API")
        return False
    
    try:
        url = f"{BASE_URL}/api/issues/projects/{TEST_PROJECT_ID}/issues/{issue_id}"
        start = time.time()
        response = requests.get(url, timeout=30)
        elapsed = time.time() - start
        
        print(f"状态码: {response.status_code}")
        print(f"响应时间: {elapsed:.2f}s")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                issue = result.get("data", {})
                print(f"✅ 成功")
                print(f"   议题ID: {issue.get('id', 'N/A')[:20]}...")
                print(f"   标题: {issue.get('title', 'N/A')[:50]}")
                print(f"   状态: {issue.get('status', 'N/A')}")
                print(f"   分配给: {issue.get('assignedTo', 'N/A')}")
                record_result("议题详情API", True)
                return True
        
        record_result("议题详情API", False, response.text[:100])
        return False
    except Exception as e:
        record_result("议题详情API", False, str(e))
        return False

def test_issue_comments(issue_id):
    """测试议题留言 API"""
    print_test("9. 议题留言 - GET /api/issues/projects/{projectId}/issues/{issueId}/comments")
    
    if not issue_id:
        print("⏭️  跳过: 没有可用的议题ID")
        test_results["skipped"].append("议题留言API")
        return False
    
    try:
        url = f"{BASE_URL}/api/issues/projects/{TEST_PROJECT_ID}/issues/{issue_id}/comments"
        start = time.time()
        response = requests.get(url, params={"limit": 20}, timeout=30)
        elapsed = time.time() - start
        
        print(f"状态码: {response.status_code}")
        print(f"响应时间: {elapsed:.2f}s")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                comments = result.get("data", {}).get("results", [])
                print(f"✅ 成功获取 {len(comments)} 条留言")
                if comments:
                    print(f"   示例: {comments[0].get('body', '')[:50]}...")
                record_result("议题留言API", True)
                return True
        
        record_result("议题留言API", False, response.text[:100])
        return False
    except Exception as e:
        record_result("议题留言API", False, str(e))
        return False

def test_issue_attachments(issue_id):
    """测试议题附件 API"""
    print_test("10. 议题附件 - GET /api/issues/projects/{projectId}/issues/{issueId}/attachments")
    
    if not issue_id:
        print("⏭️  跳过: 没有可用的议题ID")
        test_results["skipped"].append("议题附件API")
        return False
    
    try:
        url = f"{BASE_URL}/api/issues/projects/{TEST_PROJECT_ID}/issues/{issue_id}/attachments"
        start = time.time()
        response = requests.get(url, timeout=30)
        elapsed = time.time() - start
        
        print(f"状态码: {response.status_code}")
        print(f"响应时间: {elapsed:.2f}s")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                attachments = result.get("data", {}).get("results", [])
                print(f"✅ 成功获取 {len(attachments)} 个附件")
                if attachments:
                    print(f"   示例: {attachments[0].get('displayName', 'N/A')}")
                record_result("议题附件API", True)
                return True
        
        record_result("议题附件API", False, response.text[:100])
        return False
    except Exception as e:
        record_result("议题附件API", False, str(e))
        return False

def test_issues_sync():
    """测试议题同步 API"""
    print_test("11. 议题同步 - GET /api/issues/projects/{projectId}/sync")
    try:
        last_sync_time = (datetime.now() - timedelta(hours=24)).isoformat()
        url = f"{BASE_URL}/api/issues/projects/{TEST_PROJECT_ID}/sync"
        start = time.time()
        response = requests.get(url, params={
            'lastSyncTime': last_sync_time,
            'batchSize': 50,
            'includeDetails': 'false'
        }, timeout=120)
        elapsed = time.time() - start
        
        print(f"状态码: {response.status_code}")
        print(f"响应时间: {elapsed:.2f}s")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                sync_result = result.get("sync_result", {})
                print(f"✅ 成功")
                print(f"   同步议题数: {sync_result.get('total_issues', 0)}")
                print(f"   同步时间: {sync_result.get('sync_time', 'N/A')[:19]}")
                record_result("议题同步API", True)
                return True
        
        error_msg = "依赖议题列表API" if response.status_code == 500 else response.text[:100]
        record_result("议题同步API", False, error_msg)
        return False
    except Exception as e:
        record_result("议题同步API", False, str(e))
        return False

def test_issues_statistics():
    """测试议题统计 API"""
    print_test("12. 议题统计 - GET /api/issues/projects/{projectId}/statistics")
    try:
        url = f"{BASE_URL}/api/issues/projects/{TEST_PROJECT_ID}/statistics"
        start = time.time()
        response = requests.get(url, timeout=120)
        elapsed = time.time() - start
        
        print(f"状态码: {response.status_code}")
        print(f"响应时间: {elapsed:.2f}s")
        
        if response.status_code == 200:
            result = response.json()
            if result.get("status") == "success":
                stats = result.get("statistics", {})
                print(f"✅ 成功")
                print(f"   总议题数: {stats.get('total_issues', 0)}")
                print(f"   状态分布: {stats.get('status_breakdown', {})}")
                print(f"   最近活动: {stats.get('recent_activity', {})}")
                record_result("议题统计API", True)
                return True
        
        error_msg = "依赖议题列表API" if response.status_code in [500, 408] else response.text[:100]
        record_result("议题统计API", False, error_msg)
        return False
    except Exception as e:
        error_msg = "超时(依赖议题列表API)" if "timeout" in str(e).lower() else str(e)
        record_result("议题统计API", False, error_msg)
        return False

def print_summary():
    """打印测试总结"""
    print_header("测试总结")
    
    total = len(test_results["passed"]) + len(test_results["failed"]) + len(test_results["skipped"])
    passed = len(test_results["passed"])
    failed = len(test_results["failed"])
    skipped = len(test_results["skipped"])
    
    print(f"\n总测试数: {total}")
    print(f"✅ 通过: {passed}")
    print(f"❌ 失败: {failed}")
    print(f"⏭️  跳过: {skipped}")
    
    if test_results["passed"]:
        print("\n✅ 通过的测试:")
        for test in test_results["passed"]:
            print(f"  • {test}")
    
    if test_results["failed"]:
        print("\n❌ 失败的测试:")
        for test, error in test_results["failed"]:
            print(f"  • {test}")
            if error:
                print(f"    原因: {error[:80]}")
    
    if test_results["skipped"]:
        print("\n⏭️  跳过的测试:")
        for test in test_results["skipped"]:
            print(f"  • {test}")
    
    pass_rate = (passed / total * 100) if total > 0 else 0
    print(f"\n📊 通过率: {pass_rate:.1f}%")
    
    if pass_rate >= 80:
        print("\n🎉 测试结果优秀！")
    elif pass_rate >= 60:
        print("\n👍 测试结果良好")
    else:
        print("\n⚠️  需要检查失败的测试")

def test_health_check():
    """测试健康检查端点"""
    print_test("0. 健康检查 - GET /health")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            modules = result.get("modules", [])
            
            issues_module_found = any("issues_api" in module for module in modules)
            
            if issues_module_found:
                print("✅ Issues API 模块已注册")
                endpoints = result.get("endpoints", {}).get("issues_api", [])
                print(f"   端点数: {len(endpoints)}")
                for endpoint in endpoints[:5]:
                    print(f"   - {endpoint.get('method')} {endpoint.get('path')}")
                record_result("健康检查", True)
                return True
            else:
                print("❌ Issues API 模块未找到")
                record_result("健康检查", False, "模块未注册")
                return False
        else:
            record_result("健康检查", False, f"HTTP {response.status_code}")
            return False
    except Exception as e:
        record_result("健康检查", False, str(e))
        return False

def main():
    """主测试函数"""
    print_header("Issues API 完整测试")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"项目ID: {TEST_PROJECT_ID}")
    print(f"配置: limit=50 (最佳性能值)")
    
    # 0. 健康检查
    test_health_check()
    
    # 1. 认证检查
    if not test_auth_status():
        print("\n❌ 认证失败，请先登录")
        print("访问: http://localhost:8080/api/auth/login")
        return
    
    # 2-6. 元数据 API
    test_user_profile()
    test_issue_types()
    test_attribute_definitions()
    test_attribute_mappings()
    test_root_cause_categories()
    
    # 7. 议题列表 (核心)
    issue_id = test_issues_list()
    
    # 8-10. 单个议题 API
    test_issue_details(issue_id)
    test_issue_comments(issue_id)
    test_issue_attachments(issue_id)
    
    # 11-12. 高级功能 API
    test_issues_sync()
    test_issues_statistics()
    
    # 打印总结
    print_summary()
    
    print("\n" + "="*70)
    print("  测试完成")
    print("="*70)
    print(f"\n💡 提示:")
    print("  - limit=50 是经过测试的最佳性能值")
    print("  - 如果失败，检查 Autodesk 服务状态: https://health.autodesk.com")
    print("  - 详细文档: PERFORMANCE_OPTIMIZATION.md")
    print()

if __name__ == "__main__":
    main()
