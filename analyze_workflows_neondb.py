#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
檢查 neondb 數據庫中的 workflows 表並分析 step IDs
"""

import asyncio
import asyncpg
import yaml
import json
import sys
import os
from collections import defaultdict

# 設置 UTF-8 編碼輸出
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

async def analyze_workflows():
    """分析 workflows 表中的 step IDs"""
    # 讀取配置
    with open('projects_config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    db_config = config['global']['database']

    # 連接到 neondb 數據庫
    conn = await asyncpg.connect(
        host=db_config['host'],
        port=db_config['port'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['admin_database']  # neondb
    )

    print("=" * 80)
    print("檢查數據庫中的表")
    print("=" * 80)

    # 檢查是否存在 workflows 表
    table_exists = await conn.fetchval("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = 'workflows'
        );
    """)

    if not table_exists:
        print("\n❌ workflows 表不存在於此數據庫中")

        # 列出所有表
        tables = await conn.fetch("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)

        print(f"\n可用的表 (共 {len(tables)} 個):")
        for table in tables:
            print(f"  - {table['table_name']}")

        await conn.close()
        return

    print("\n✅ 找到 workflows 表")

    # 查詢所有 workflows 的 steps 字段
    query = """
        SELECT
            id as workflow_id,
            name as workflow_name,
            steps,
            workflow_uuid,
            acc_workflow_id,
            status,
            data_source,
            project_id,
            created_at
        FROM workflows
        WHERE steps IS NOT NULL AND steps != '[]'::jsonb
        ORDER BY id;
    """

    rows = await conn.fetch(query)

    if not rows:
        print(f"\n⚠ 數據庫中沒有找到任何包含 steps 的 workflows")

        # 檢查總數
        total_count = await conn.fetchval("SELECT COUNT(*) FROM workflows")
        print(f"   workflows 表總記錄數: {total_count}")

        await conn.close()
        return

    print(f"\n找到 {len(rows)} 個包含 steps 的 workflows\n")
    print("=" * 80)
    print("詳細 Workflow 信息")
    print("=" * 80)

    # 分析結果
    workflows_data = []
    step_id_to_workflows = defaultdict(list)  # step_id -> [(workflow_id, workflow_name)]
    all_step_ids = set()

    for row in rows:
        workflow_id = row['workflow_id']
        workflow_name = row['workflow_name']
        steps = row['steps']  # JSONB array

        # 解析 steps JSONB - 處理不同格式
        step_ids = []
        steps_list = []

        if steps:
            # 如果 steps 是字符串，嘗試解析為 JSON
            if isinstance(steps, str):
                try:
                    steps = json.loads(steps)
                except:
                    pass

            # 確保 steps 是列表
            if isinstance(steps, list):
                steps_list = steps
            else:
                steps_list = []

            for i, step in enumerate(steps_list):
                # 跳過非字典類型的 step
                if not isinstance(step, dict):
                    continue

                if 'id' in step:
                    step_id = step['id']
                    step_ids.append(step_id)
                    all_step_ids.add(step_id)
                    step_id_to_workflows[step_id].append({
                        'workflow_id': workflow_id,
                        'workflow_name': workflow_name,
                        'workflow_uuid': row['workflow_uuid'],
                        'acc_workflow_id': row['acc_workflow_id'],
                        'project_id': row['project_id'],
                        'step_index': i,
                        'step': step
                    })

        workflows_data.append({
            'workflow_id': workflow_id,
            'workflow_name': workflow_name,
            'workflow_uuid': row['workflow_uuid'],
            'acc_workflow_id': row['acc_workflow_id'],
            'project_id': row['project_id'],
            'status': row['status'],
            'data_source': row['data_source'],
            'created_at': str(row['created_at']),
            'step_ids': step_ids,
            'step_count': len(step_ids),
            'steps': steps
        })

        # 打印 workflow 信息
        print(f"\nWorkflow ID: {workflow_id}")
        print(f"  名稱: {workflow_name}")
        print(f"  Project ID: {row['project_id']}")
        print(f"  UUID: {row['workflow_uuid']}")
        print(f"  ACC ID: {row['acc_workflow_id']}")
        print(f"  狀態: {row['status']}")
        print(f"  數據源: {row['data_source']}")
        print(f"  創建時間: {row['created_at']}")
        print(f"  步驟數: {len(step_ids)}")
        print(f"  Step IDs: {step_ids}")

        # 打印每個 step 的詳細信息
        if steps_list:
            print(f"\n  步驟詳情:")
            for i, step in enumerate(steps_list):
                if isinstance(step, dict):
                    print(f"    [{i}] ID: {step.get('id', 'N/A')}")
                    print(f"        Name: {step.get('name', 'N/A')}")
                    print(f"        Type: {step.get('type', 'N/A')}")
                    print(f"        Order: {step.get('order', 'N/A')}")
                else:
                    print(f"    [{i}] 非字典類型: {type(step).__name__} - {step}")

    # 分析重複
    print("\n" + "=" * 80)
    print("Step ID 重複分析")
    print("=" * 80)

    duplicates = []
    for step_id, usage_list in step_id_to_workflows.items():
        if len(usage_list) > 1:
            duplicates.append({
                'step_id': step_id,
                'usage_count': len(usage_list),
                'used_in_workflows': usage_list
            })

    if duplicates:
        print(f"\n❌ 發現 {len(duplicates)} 個重複的 step IDs\n")

        for dup in sorted(duplicates, key=lambda x: x['usage_count'], reverse=True):
            print(f"\nStep ID: '{dup['step_id']}'")
            print(f"  使用次數: {dup['usage_count']}")
            print(f"  使用的 workflows:")

            for usage in dup['used_in_workflows']:
                print(f"\n    Workflow ID: {usage['workflow_id']}")
                print(f"      名稱: {usage['workflow_name']}")
                print(f"      Project ID: {usage['project_id']}")
                print(f"      UUID: {usage['workflow_uuid']}")
                print(f"      ACC Workflow ID: {usage['acc_workflow_id']}")
                print(f"      Step 位置: 第 {usage['step_index'] + 1} 個步驟")
                print(f"      Step 詳情:")
                step = usage['step']
                print(f"        - Name: {step.get('name', 'N/A')}")
                print(f"        - Type: {step.get('type', 'N/A')}")
                print(f"        - Order: {step.get('order', 'N/A')}")
                if 'notes' in step:
                    print(f"        - Notes: {step.get('notes', 'N/A')}")

    else:
        print("\n✅ 未發現 step ID 重複")

    # 統計信息
    print("\n" + "=" * 80)
    print("統計摘要")
    print("=" * 80)
    print(f"\n總 workflows 數: {len(workflows_data)}")
    print(f"唯一 step IDs 總數: {len(all_step_ids)}")
    print(f"總 step 實例數: {sum(len(wf['step_ids']) for wf in workflows_data)}")
    print(f"發現重複的 step IDs: {len(duplicates)}")

    if duplicates:
        print(f"\n跨 workflow 重複的 step IDs 列表:")
        for dup in sorted(duplicates, key=lambda x: x['usage_count'], reverse=True):
            print(f"  - '{dup['step_id']}' (使用 {dup['usage_count']} 次)")

    # 建議
    print("\n" + "=" * 80)
    print("建議")
    print("=" * 80)

    if duplicates:
        print("\n❌ 發現 Step ID 重複問題！")
        print("\n潛在影響:")
        print("  1. review_progress 表中的 step_id 可能無法唯一標識步驟")
        print("  2. 不同 workflow 的 review 可能會混淆步驟引用")
        print("  3. 步驟狀態更新可能影響到錯誤的 review")

        print("\n建議的解決方案:")
        print("  1. 短期修復:")
        print("     - 使用複合鍵 (review_id, step_id) 來唯一標識步驟")
        print("     - 在查詢時始終結合 review_id 和 step_id")

        print("\n  2. 長期解決:")
        print("     - 為每個 workflow 實例的 step 生成唯一 ID")
        print("     - 格式建議: '{workflow_uuid}_{step_order}'")
        print("     - 或使用 UUID 為每個 step 生成全局唯一 ID")

        print("\n  3. 數據修復步驟:")
        print("     a. 備份當前數據")
        print("     b. 為所有 workflows 重新生成唯一 step IDs")
        print("     c. 更新 review_progress 表中的 step_id 引用")
        print("     d. 更新 review_step_candidates 表中的 step_id 引用")

        print("\n  4. 預防措施:")
        print("     - 在創建 workflow 時自動生成唯一 step IDs")
        print("     - 添加應用層驗證確保 step IDs 唯一性")
        print("     - 考慮使用數據庫觸發器驗證")
    else:
        print("\n✅ 未發現 step ID 重複問題")
        print("\n建議的最佳實踐:")
        print("  1. 維持當前的 step ID 唯一性策略")
        print("  2. 在創建新 workflow 時確保 step IDs 不與現有的重複")
        print("  3. 考慮實施自動化的唯一性驗證機制")
        print("  4. 定期運行此分析腳本檢查數據完整性")

    print("\n")
    await conn.close()

if __name__ == '__main__':
    asyncio.run(analyze_workflows())
