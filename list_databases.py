#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
列出所有可用的數據庫
"""

import asyncio
import asyncpg
import yaml
import sys
import os

# 設置 UTF-8 編碼輸出
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

async def list_databases():
    """列出所有數據庫"""
    # 讀取配置
    with open('projects_config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    db_config = config['global']['database']

    # 連接到 admin 數據庫
    conn = await asyncpg.connect(
        host=db_config['host'],
        port=db_config['port'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['admin_database']
    )

    # 查詢所有數據庫
    databases = await conn.fetch("""
        SELECT datname
        FROM pg_database
        WHERE datistemplate = false
        ORDER BY datname;
    """)

    print("可用的數據庫列表:")
    print("=" * 80)
    for db in databases:
        print(f"  - {db['datname']}")

    print(f"\n總共: {len(databases)} 個數據庫")

    await conn.close()

if __name__ == '__main__':
    asyncio.run(list_databases())
