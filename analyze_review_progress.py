#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
檢查 review_progress 表，確認 step_id 的使用和完整性
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

async def analyze_review_progress():
    """分析 review_progress 表中的 step_id 使用情況"""
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
        database=db_config['admin_database']
    )

    print("=" * 80)
    print("Review Progress 表 Step ID 分析")
    print("=" * 80)

    # 檢查 review_progress 表是否存在
    table_exists = await conn.fetchval("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = 'review_progress'
        );
    """)

    if not table_exists:
        print("\n❌ review_progress 表不存在")
        await conn.close()
        return

    print("\n✅ 找到 review_progress 表")

    # 獲取 review_progress 的統計信息
    total_records = await conn.fetchval("SELECT COUNT(*) FROM review_progress")
    print(f"\nreview_progress 總記錄數: {total_records}")

    if total_records == 0:
        print("\n⚠ review_progress 表為空")
        await conn.close()
        return

    # 查詢 review_progress 和對應的 workflow 信息
    query = """
        SELECT
            rp.id,
            rp.review_id,
            rp.step_id,
            rp.step_name,
            rp.step_type,
            rp.step_order,
            rp.status,
            r.name as review_name,
            r.workflow_id,
            w.name as workflow_name,
            w.workflow_uuid,
            w.steps
        FROM review_progress rp
        JOIN reviews r ON rp.review_id = r.id
        LEFT JOIN workflows w ON r.workflow_id = w.id
        ORDER BY rp.review_id, rp.step_order;
    """

    rows = await conn.fetch(query)

    print(f"\n找到 {len(rows)} 條 review_progress 記錄\n")

    # 分析數據
    step_id_usage = defaultdict(list)
    reviews_data = defaultdict(list)
    orphaned_step_ids = []  # 在 review_progress 中但不在任何 workflow 中的 step_id

    # 收集所有 workflow 中的 step IDs
    workflow_step_ids = set()

    for row in rows:
        step_id = row['step_id']
        review_id = row['review_id']

        # 記錄 step_id 的使用
        step_id_usage[step_id].append({
            'progress_id': row['id'],
            'review_id': review_id,
            'review_name': row['review_name'],
            'workflow_id': row['workflow_id'],
            'workflow_name': row['workflow_name'],
            'step_order': row['step_order'],
            'step_name': row['step_name'],
            'status': row['status']
        })

        # 按 review 分組
        reviews_data[review_id].append({
            'step_id': step_id,
            'step_name': row['step_name'],
            'step_type': row['step_type'],
            'step_order': row['step_order'],
            'status': row['status']
        })

        # 檢查 step_id 是否在 workflow 的 steps 中
        if row['steps']:
            steps = row['steps']
            if isinstance(steps, str):
                try:
                    steps = json.loads(steps)
                except:
                    steps = []

            if isinstance(steps, list):
                for step in steps:
                    if isinstance(step, dict) and 'id' in step:
                        workflow_step_ids.add(step['id'])

                # 檢查當前 step_id 是否在 workflow 中
                step_ids_in_workflow = [s.get('id') for s in steps if isinstance(s, dict) and 'id' in s]
                if step_id not in step_ids_in_workflow:
                    orphaned_step_ids.append({
                        'progress_id': row['id'],
                        'review_id': review_id,
                        'step_id': step_id,
                        'workflow_id': row['workflow_id'],
                        'workflow_name': row['workflow_name']
                    })

    # 報告結果
    print("=" * 80)
    print("分析結果")
    print("=" * 80)

    print(f"\n1. Step ID 使用統計:")
    print(f"   - 唯一 step IDs 數量: {len(step_id_usage)}")
    print(f"   - 總 step 實例數: {len(rows)}")
    print(f"   - 涉及的 reviews 數量: {len(reviews_data)}")

    # 檢查重複使用的 step IDs
    reused_step_ids = {step_id: usage for step_id, usage in step_id_usage.items() if len(usage) > 1}

    if reused_step_ids:
        print(f"\n2. ⚠ 發現重複使用的 step IDs: {len(reused_step_ids)} 個")
        print("\n   這些 step IDs 被多個 review_progress 記錄使用:")

        for step_id, usages in sorted(reused_step_ids.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
            print(f"\n   Step ID: '{step_id}'")
            print(f"     使用次數: {len(usages)}")
            print(f"     使用在以下 reviews:")

            # 按 review 分組
            by_review = defaultdict(list)
            for usage in usages:
                by_review[usage['review_id']].append(usage)

            for review_id, review_usages in sorted(by_review.items())[:3]:  # 只顯示前3個
                review_name = review_usages[0]['review_name']
                workflow_name = review_usages[0]['workflow_name']
                print(f"       - Review ID {review_id} ({review_name})")
                print(f"         Workflow: {workflow_name}")
                print(f"         出現 {len(review_usages)} 次:")
                for ru in review_usages:
                    print(f"           * Step {ru['step_order']}: {ru['step_name']} ({ru['status']})")

            if len(by_review) > 3:
                print(f"       ... 還有 {len(by_review) - 3} 個 reviews 使用此 step ID")
    else:
        print(f"\n2. ✅ 所有 step IDs 在不同的 review_progress 記錄中都是唯一使用的")

    # 檢查孤立的 step IDs
    if orphaned_step_ids:
        print(f"\n3. ⚠ 發現孤立的 step IDs: {len(orphaned_step_ids)} 個")
        print("\n   這些 step IDs 在 review_progress 中存在，但不在對應的 workflow.steps 中:")

        orphaned_by_step_id = defaultdict(list)
        for orphan in orphaned_step_ids:
            orphaned_by_step_id[orphan['step_id']].append(orphan)

        for step_id, orphans in sorted(orphaned_by_step_id.items())[:10]:
            print(f"\n   Step ID: '{step_id}'")
            print(f"     孤立記錄數: {len(orphans)}")
            for orphan in orphans[:3]:
                print(f"       - Progress ID: {orphan['progress_id']}, Review ID: {orphan['review_id']}")
                print(f"         Workflow: {orphan['workflow_name']} (ID: {orphan['workflow_id']})")

            if len(orphans) > 3:
                print(f"       ... 還有 {len(orphans) - 3} 條孤立記錄")
    else:
        print(f"\n3. ✅ 所有 review_progress 中的 step IDs 都在對應的 workflow.steps 中")

    # 按 review 顯示詳細信息
    print(f"\n\n" + "=" * 80)
    print("按 Review 分組的 Step 使用情況")
    print("=" * 80)

    for review_id, steps in sorted(reviews_data.items())[:5]:  # 只顯示前5個 reviews
        print(f"\nReview ID: {review_id}")
        if steps:
            print(f"  Review 名稱: {step_id_usage[steps[0]['step_id']][0]['review_name']}")
            print(f"  Workflow: {step_id_usage[steps[0]['step_id']][0]['workflow_name']}")
            print(f"  步驟數: {len(steps)}")
            print(f"  步驟列表:")
            for step in sorted(steps, key=lambda x: x['step_order']):
                print(f"    [{step['step_order']}] {step['step_id']} - {step['step_name']}")
                print(f"         類型: {step['step_type']}, 狀態: {step['status']}")

    if len(reviews_data) > 5:
        print(f"\n  ... 還有 {len(reviews_data) - 5} 個 reviews")

    # 建議
    print(f"\n\n" + "=" * 80)
    print("建議")
    print("=" * 80)

    if reused_step_ids:
        print("\n⚠ 發現 step IDs 重複使用問題")
        print("\n說明:")
        print("  - 同一個 step_id 在多個 review_progress 記錄中使用")
        print("  - 這是正常的，因為不同的 reviews 可能使用相同的 workflow template")
        print("  - review_progress 表使用 (review_id, step_id) 的組合來唯一標識步驟")
        print("\n當前設計評估: ✅ 正常")
        print("  - review_progress 有條件唯一索引:")
        print("    CREATE UNIQUE INDEX idx_review_progress_unique_active")
        print("    ON review_progress(review_id, step_id)")
        print("    WHERE status NOT IN ('SENT_BACK', 'COMPLETED');")
        print("\n  這確保了:")
        print("    1. 在同一個 review 中，活躍的 step_id 是唯一的")
        print("    2. 不同的 reviews 可以使用相同的 step_id (來自相同的 workflow template)")
        print("    3. 支持 send-back 功能（歷史步驟可以重複）")
    else:
        print("\n✅ Step IDs 使用正常")

    if orphaned_step_ids:
        print("\n⚠ 發現孤立的 step IDs")
        print("\n可能的原因:")
        print("  1. Workflow 的 steps 被修改或刪除")
        print("  2. Review 創建後 workflow 被更新")
        print("  3. 數據同步問題")
        print("\n建議:")
        print("  1. 檢查這些 reviews 的完整性")
        print("  2. 考慮添加外鍵約束或觸發器來維護一致性")
        print("  3. 在 workflow 更新時同步更新相關的 reviews")
    else:
        print("\n✅ 數據完整性良好，無孤立的 step IDs")

    print("\n")
    await conn.close()

if __name__ == '__main__':
    asyncio.run(analyze_review_progress())
