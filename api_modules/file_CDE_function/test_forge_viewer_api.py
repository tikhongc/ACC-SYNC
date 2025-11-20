#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Forge Viewer API 测试脚本

演示如何使用 Forge Viewer URL 生成 API
"""

import requests
import json

# API 基础 URL
BASE_URL = "http://localhost:8080"

def test_generate_viewer_url_get():
    """测试 GET 请求生成 Viewer URL"""
    print("=" * 70)
    print("测试 1: GET 请求生成 Forge Viewer URL")
    print("=" * 70)

    # 示例 URN
    urn = "urn:adsk.wipprod:fs.file:vf.BpecaZkCRhSpeKT3CXYIiA?version=1"

    params = {
        'urn': urn,
        'use_current_token': 'true'
    }

    try:
        response = requests.get(f"{BASE_URL}/api/forge-viewer/url", params=params)
        print(f"状态码: {response.status_code}")
        print(f"响应内容:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))

        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"\n✅ 成功生成 Viewer URL:")
                print(f"   {data['data']['viewer_url']}")

    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")

    print()


def test_generate_viewer_url_post():
    """测试 POST 请求生成 Viewer URL"""
    print("=" * 70)
    print("测试 2: POST 请求生成 Forge Viewer URL (使用自定义 token)")
    print("=" * 70)

    # 示例 URN 和 Token
    urn = "urn:adsk.wipprod:fs.file:vf.BpecaZkCRhSpeKT3CXYIiA?version=1"
    custom_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IlZiakZvUzhQU3lYODQyMV95dndvRUdRdFJEa19SUzI1NiIsInBpLmF0bSI6ImFzc2MifQ..."

    payload = {
        'urn': urn,
        'use_current_token': False,
        'token': custom_token
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/forge-viewer/url",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        print(f"状态码: {response.status_code}")
        print(f"响应内容:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))

        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"\n✅ 成功生成 Viewer URL:")
                print(f"   {data['data']['viewer_url']}")

    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")

    print()


def test_batch_generate_viewer_urls():
    """测试批量生成 Viewer URLs"""
    print("=" * 70)
    print("测试 3: 批量生成 Forge Viewer URLs")
    print("=" * 70)

    # 示例多个 URNs
    urns = [
        "urn:adsk.wipprod:fs.file:vf.BpecaZkCRhSpeKT3CXYIiA?version=1",
        "urn:adsk.wipprod:fs.file:vf.XyzExample123?version=2",
        "urn:adsk.wipprod:fs.file:vf.AnotherExample456?version=1"
    ]

    payload = {
        'urns': urns,
        'use_current_token': True
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/forge-viewer/batch-urls",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        print(f"状态码: {response.status_code}")
        print(f"响应内容:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))

        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"\n✅ 成功批量生成 {data['data']['total']} 个 Viewer URLs")
                for i, result in enumerate(data['data']['results'], 1):
                    if result['success']:
                        print(f"\n   [{i}] URN: {result['urn'][:50]}...")
                        print(f"       URL: {result['viewer_url'][:80]}...")

    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")

    print()


def test_health_check():
    """测试健康检查端点"""
    print("=" * 70)
    print("测试 4: 健康检查")
    print("=" * 70)

    try:
        response = requests.get(f"{BASE_URL}/api/forge-viewer/health")
        print(f"状态码: {response.status_code}")
        print(f"响应内容:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"❌ 请求失败: {str(e)}")

    print()


def main():
    """主函数"""
    print("\n")
    print("🔧 Forge Viewer API 测试")
    print()

    # 测试健康检查
    test_health_check()

    # 测试 GET 请求
    test_generate_viewer_url_get()

    # 测试 POST 请求
    test_generate_viewer_url_post()

    # 测试批量生成
    test_batch_generate_viewer_urls()

    print("=" * 70)
    print("✅ 所有测试完成")
    print("=" * 70)


if __name__ == '__main__':
    main()
