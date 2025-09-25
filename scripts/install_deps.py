#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
依赖安装脚本
安装Python和Node.js依赖
"""

import subprocess
import sys
import os

def install_python_deps():
    """安装Python依赖"""
    print("📦 安装Python依赖...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'config/requirements.txt'], check=True)
        print("✅ Python依赖安装成功")
    except subprocess.CalledProcessError as e:
        print(f"❌ Python依赖安装失败: {e}")
        return False
    return True

def install_node_deps():
    """安装Node.js依赖"""
    print("📦 安装Node.js依赖...")
    
    # 检查npm是否可用
    try:
        subprocess.run(['npm', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ npm命令未找到，请先安装Node.js")
        print("📥 下载地址: https://nodejs.org/")
        print("💡 安装Node.js后重新运行此脚本")
        return False
    
    # 检查frontend目录
    if not os.path.exists('frontend'):
        print("❌ frontend目录不存在")
        return False
    
    original_dir = os.getcwd()
    try:
        os.chdir('frontend')
        print("📁 在frontend目录中安装依赖...")
        subprocess.run(['npm', 'install'], check=True)
        print("✅ Node.js依赖安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Node.js依赖安装失败: {e}")
        return False
    except FileNotFoundError:
        print("❌ npm命令未找到，请确保Node.js已正确安装")
        return False
    finally:
        os.chdir(original_dir)

def main():
    print("🚀 安装 ACC 表单同步 PoC 依赖")
    print("=" * 50)
    
    python_success = False
    node_success = False
    
    # 安装Python依赖
    python_success = install_python_deps()
    
    # 安装Node.js依赖
    node_success = install_node_deps()
    
    print("=" * 50)
    print("📋 安装结果:")
    print(f"   Python依赖: {'✅ 成功' if python_success else '❌ 失败'}")
    print(f"   Node.js依赖: {'✅ 成功' if node_success else '❌ 失败'}")
    print("=" * 50)
    
    if python_success and node_success:
        print("✅ 所有依赖安装完成！")
        print("💡 现在可以运行: python start_dev.py")
    elif python_success:
        print("⚠️  Python依赖已安装，但Node.js依赖安装失败")
        print("💡 你仍然可以运行Flask后端: python app.py")
        print("🔧 要使用完整功能，请先安装Node.js，然后重新运行此脚本")
    else:
        print("❌ 依赖安装失败，请检查错误信息")

if __name__ == '__main__':
    main()
