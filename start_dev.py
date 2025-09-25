#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开发环境启动脚本
同时启动Flask后端和Vue前端开发服务器
"""

import subprocess
import sys
import os
import time
import threading

def get_npm_command():
    """检测可用的npm命令"""
    # 首先尝试npm
    try:
        subprocess.run(['npm', '--version'], capture_output=True, check=True)
        return 'npm'
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    # 然后尝试npx
    try:
        subprocess.run(['npx', '--version'], capture_output=True, check=True)
        return 'npx'
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    # 尝试通过node路径查找npm
    try:
        node_path = subprocess.run(['where', 'node'], capture_output=True, check=True, text=True).stdout.strip()
        if node_path:
            # 从node路径推断npm路径
            node_dir = os.path.dirname(node_path)
            npm_path = os.path.join(node_dir, 'npm.cmd')
            if os.path.exists(npm_path):
                return npm_path
            npm_path = os.path.join(node_dir, 'npm')
            if os.path.exists(npm_path):
                return npm_path
    except:
        pass
    
    return None

def start_flask():
    """启动Flask后端服务器"""
    print("🔧 启动Flask后端服务器...")
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    subprocess.run([sys.executable, 'app.py'])

def start_vue():
    """启动Vue前端开发服务器"""
    print("🎨 启动Vue前端开发服务器...")
    
    # 检查是否安装了Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, check=True, text=True)
        print(f"✅ Node.js版本: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ 未找到Node.js，请先安装Node.js")
        print("📥 下载地址: https://nodejs.org/")
        print("💡 或者直接运行Flask后端: python app.py")
        return
    
    # 检查npm命令可用性
    npm_cmd = get_npm_command()
    if not npm_cmd:
        print("❌ 未找到可用的npm命令")
        print("🔧 可能的解决方案:")
        print("   1. 重新安装Node.js: https://nodejs.org/")
        print("   2. 检查系统PATH是否包含npm路径")
        print("   3. 重启命令行/IDE后重试")
        print("💡 或者运行: python start_flask_only.py 仅启动后端")
        return
    else:
        if npm_cmd in ['npm', 'npx']:
            try:
                result = subprocess.run([npm_cmd, '--version'], capture_output=True, check=True, text=True)
                print(f"✅ {npm_cmd}版本: {result.stdout.strip()}")
            except:
                print(f"✅ 找到{npm_cmd}命令")
        else:
            print(f"✅ 找到npm命令: {npm_cmd}")
    
    # 保存当前目录
    original_dir = os.getcwd()
    
    try:
        # 切换到frontend目录
        frontend_path = os.path.join(original_dir, 'frontend')
        if not os.path.exists(frontend_path):
            print("❌ frontend目录不存在")
            return
            
        os.chdir(frontend_path)
        print(f"📁 切换到目录: {os.getcwd()}")
        
        # 检查package.json是否存在
        if not os.path.exists('package.json'):
            print("❌ frontend/package.json不存在")
            return
        
        # 检查是否安装了依赖
        if not os.path.exists('node_modules'):
            print("📦 安装前端依赖...")
            npm_cmd = get_npm_command()
            if not npm_cmd:
                print("❌ 无法找到可用的npm命令")
                return
            
            try:
                if npm_cmd == 'npx':
                    result = subprocess.run(['npx', 'npm', 'install'], check=True, capture_output=True, text=True)
                else:
                    result = subprocess.run([npm_cmd, 'install'], check=True, capture_output=True, text=True)
                print("✅ 依赖安装成功")
            except subprocess.CalledProcessError as e:
                print(f"❌ npm安装失败: {e}")
                print(f"错误输出: {e.stderr}")
                return
        else:
            print("✅ 依赖已存在")
        
        print("🎨 启动Vue开发服务器...")
        # 获取可用的npm命令
        npm_cmd = get_npm_command()
        if not npm_cmd:
            print("❌ 无法找到可用的npm命令")
            return
            
        # 使用非阻塞方式启动，并显示输出
        if npm_cmd == 'npx':
            cmd = ['npx', 'npm', 'run', 'dev']
        else:
            cmd = [npm_cmd, 'run', 'dev']
            
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # 实时显示输出
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
                
        # 检查进程退出状态
        return_code = process.poll()
        if return_code != 0:
            print(f"❌ Vue开发服务器启动失败，退出码: {return_code}")
        
    except Exception as e:
        print(f"❌ 启动Vue时发生错误: {e}")
    finally:
        # 恢复原始目录
        os.chdir(original_dir)

def main():
    print("🚀 启动 ACC 表单同步 PoC 开发环境")
    print("=" * 50)
    print("📋 服务信息:")
    print("   - Flask后端: http://localhost:8080")
    print("   - Vue前端:   http://localhost:3000")
    print("=" * 50)
    
    # 启动Flask后端 (在新线程中)
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    
    # 等待Flask启动
    time.sleep(2)
    
    # 启动Vue前端 (在主线程中，这样可以看到输出)
    try:
        start_vue()
    except KeyboardInterrupt:
        print("\n👋 开发服务器已停止")

if __name__ == '__main__':
    main()
