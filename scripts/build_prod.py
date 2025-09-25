#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生产环境构建脚本
构建Vue前端并集成到Flask静态文件中
"""

import subprocess
import sys
import os
import shutil

def build_vue():
    """构建Vue前端"""
    print("🎨 构建Vue前端...")
    
    # 进入前端目录
    os.chdir('frontend')
    
    # 检查是否安装了依赖
    if not os.path.exists('node_modules'):
        print("📦 安装前端依赖...")
        subprocess.run(['npm', 'install'], check=True)
    
    # 构建前端
    print("🔨 构建前端应用...")
    subprocess.run(['npm', 'run', 'build'], check=True)
    
    # 返回根目录
    os.chdir('..')

def setup_flask_static():
    """配置Flask静态文件"""
    print("🔧 配置Flask静态文件...")
    
    # 确保构建目录存在
    if not os.path.exists('static/dist'):
        print("❌ 前端构建失败，dist目录不存在")
        return False
    
    print("✅ 前端构建完成，文件已复制到 static/dist/")
    return True

def main():
    print("🚀 构建 ACC 表单同步 PoC 生产环境")
    print("=" * 50)
    
    try:
        # 构建Vue前端
        build_vue()
        
        # 配置Flask静态文件
        if setup_flask_static():
            print("=" * 50)
            print("✅ 生产环境构建完成！")
            print("📋 部署信息:")
            print("   - 启动命令: python app.py")
            print("   - 访问地址: http://localhost:8080")
            print("   - 前端文件: static/dist/")
            print("=" * 50)
        else:
            print("❌ 构建失败")
            sys.exit(1)
            
    except subprocess.CalledProcessError as e:
        print(f"❌ 构建过程中出错: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
