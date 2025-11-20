#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
仅启动Flask后端服务器的脚本
用于当前端开发服务器已经在运行时，只需要启动后端
"""

import sys
import os

def main():
    print("Starting Flask Backend Server Only...")
    print("=" * 50)
    print("Service Information:")
    print("   - Flask Backend: http://localhost:8080")
    print("=" * 50)
    
    # 设置环境变量
    os.environ['FLASK_ENV'] = 'development'
    os.environ['FLASK_DEBUG'] = '1'
    
    try:
        # 直接运行app.py
        import app
    except KeyboardInterrupt:
        print("\nFlask server stopped")
    except Exception as e:
        print(f"Error starting Flask server: {e}")

if __name__ == '__main__':
    main()
