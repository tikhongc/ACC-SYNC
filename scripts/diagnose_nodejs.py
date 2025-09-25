#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Node.js环境诊断脚本
帮助诊断Node.js和npm安装问题
"""

import subprocess
import sys
import os

def check_command(cmd, description):
    """检查命令是否可用"""
    print(f"🔍 检查 {description}...")
    try:
        result = subprocess.run([cmd, '--version'], capture_output=True, check=True, text=True)
        print(f"   ✅ {cmd}: {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        print(f"   ❌ {cmd}: 命令未找到")
        return False
    except subprocess.CalledProcessError as e:
        print(f"   ❌ {cmd}: 执行失败 - {e}")
        return False

def check_path():
    """检查PATH环境变量"""
    print("🔍 检查PATH环境变量...")
    path = os.environ.get('PATH', '')
    node_paths = [p for p in path.split(os.pathsep) if 'node' in p.lower()]
    if node_paths:
        print("   ✅ 找到Node.js相关路径:")
        for p in node_paths:
            print(f"      - {p}")
    else:
        print("   ⚠️  PATH中未找到Node.js相关路径")

def find_nodejs_installation():
    """查找Node.js安装位置"""
    print("🔍 查找Node.js安装位置...")
    
    # Windows常见安装路径
    common_paths = [
        r"C:\Program Files\nodejs",
        r"C:\Program Files (x86)\nodejs",
        os.path.expanduser("~\\AppData\\Roaming\\npm"),
        os.path.expanduser("~\\AppData\\Local\\npm"),
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            print(f"   ✅ 找到: {path}")
            # 检查该路径下的文件
            try:
                files = os.listdir(path)
                relevant_files = [f for f in files if f.lower().startswith(('node', 'npm'))]
                if relevant_files:
                    print(f"      包含文件: {', '.join(relevant_files[:5])}")
            except:
                pass
    
    # 尝试使用where命令查找
    try:
        result = subprocess.run(['where', 'node'], capture_output=True, check=True, text=True)
        print(f"   ✅ node位置: {result.stdout.strip()}")
    except:
        print("   ❌ 无法通过where命令找到node")

def suggest_solutions():
    """提供解决方案建议"""
    print("\n🔧 建议的解决方案:")
    print("1. 重新安装Node.js:")
    print("   - 访问 https://nodejs.org/")
    print("   - 下载LTS版本")
    print("   - 确保勾选'Add to PATH'选项")
    print("")
    print("2. 手动添加到PATH:")
    print("   - 找到Node.js安装目录（通常是 C:\\Program Files\\nodejs）")
    print("   - 将该路径添加到系统PATH环境变量")
    print("")
    print("3. 重启相关程序:")
    print("   - 重启命令行/PowerShell")
    print("   - 重启IDE（如VS Code）")
    print("   - 如果必要，重启计算机")
    print("")
    print("4. 使用替代方案:")
    print("   - 运行: python start_flask_only.py")
    print("   - 或直接运行: python app.py")

def main():
    print("🚀 Node.js环境诊断")
    print("=" * 50)
    
    # 检查各种命令
    node_ok = check_command('node', 'Node.js')
    npm_ok = check_command('npm', 'npm')
    npx_ok = check_command('npx', 'npx')
    
    print()
    check_path()
    print()
    find_nodejs_installation()
    
    print("\n" + "=" * 50)
    print("📋 诊断结果:")
    print(f"   Node.js: {'✅' if node_ok else '❌'}")
    print(f"   npm: {'✅' if npm_ok else '❌'}")
    print(f"   npx: {'✅' if npx_ok else '❌'}")
    
    if node_ok and npm_ok:
        print("\n✅ Node.js环境正常！可以运行: python start_dev.py")
    elif node_ok and not npm_ok:
        print("\n⚠️  Node.js已安装但npm不可用")
        suggest_solutions()
    else:
        print("\n❌ Node.js环境有问题")
        suggest_solutions()

if __name__ == '__main__':
    main()
