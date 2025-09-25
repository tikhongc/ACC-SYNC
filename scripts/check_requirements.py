#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境依赖检查脚本
检查Python和Node.js环境是否正确安装
"""

import subprocess
import sys
import os

def check_python():
    """检查Python环境"""
    print("🐍 检查Python环境...")
    try:
        version = sys.version_info
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    except Exception as e:
        print(f"   ❌ Python检查失败: {e}")
        return False

def check_node():
    """检查Node.js环境"""
    print("🟢 检查Node.js环境...")
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, check=True)
        version = result.stdout.strip()
        print(f"   ✅ Node.js {version}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("   ❌ 未找到Node.js")
        print("   📥 请从以下地址下载安装:")
        print("   🔗 https://nodejs.org/")
        return False

def check_npm():
    """检查npm环境"""
    print("📦 检查npm环境...")
    try:
        # 尝试多种方式检查npm
        commands = ['npm', 'npm.cmd', 'npm.exe']
        for cmd in commands:
            try:
                result = subprocess.run([cmd, '-v'], capture_output=True, text=True, check=True)
                version = result.stdout.strip()
                print(f"   ✅ npm {version}")
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        print("   ❌ 未找到npm")
        print("   💡 npm通常随Node.js一起安装")
        return False
    except Exception as e:
        print(f"   ❌ npm检查失败: {e}")
        return False

def check_flask_deps():
    """检查Flask依赖"""
    print("🌶️ 检查Flask依赖...")
    try:
        import flask
        print(f"   ✅ Flask {flask.__version__}")
        
        import requests
        print(f"   ✅ requests {requests.__version__}")
        
        return True
    except ImportError as e:
        print(f"   ❌ 缺少Python依赖: {e}")
        print("   📦 请运行: pip install flask requests")
        return False

def main():
    print("🔍 ACC 表单同步 PoC - 环境依赖检查")
    print("=" * 50)
    
    checks = [
        ("Python", check_python()),
        ("Flask依赖", check_flask_deps()),
        ("Node.js", check_node()),
        ("npm", check_npm())
    ]
    
    print("=" * 50)
    print("📊 检查结果:")
    
    all_passed = True
    for name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"   {status} {name}")
        if not passed:
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("🎉 所有依赖检查通过！")
        print("🚀 可以运行: python start_dev.py")
    else:
        print("⚠️ 部分依赖缺失")
        print("💡 推荐方案:")
        if checks[0][1] and checks[1][1]:  # Python和Flask都OK
            print("   🔧 只运行后端: python start_flask.py")
        print("   📥 安装Node.js后运行完整版: python start_dev.py")
    
    print("=" * 50)

if __name__ == '__main__':
    main()
