#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
分析 workflows 表中的 step IDs，檢查是否存在跨 workflow 的重複
"""

import asyncio
import asyncpg
import yaml
import json
import sys
import os
from collections import defaultdict
from typing import Dict, List, Set, Tuple

# 設置 UTF-8 編碼輸出
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

class WorkflowStepAnalyzer:
    def __init__(self):
        self.config = self._load_config()
        self.db_config = self.config['global']['database']

    def _load_config(self):
        """加載配置文件"""
        with open('projects_config.yaml', 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    async def connect_to_database(self, database_name: str):
        """連接到指定的數據庫"""
        return await asyncpg.connect(
            host=self.db_config['host'],
            port=self.db_config['port'],
            user=self.db_config['user'],
            password=self.db_config['password'],
            database=database_name
        )

    async def get_all_project_databases(self) -> List[str]:
        """獲取所有項目數據庫名稱"""
        databases = []
        for project_id, project_config in self.config.get('projects', {}).items():
            if project_config.get('status') == 'active':
                databases.append(project_config['database'])
        return databases

    async def analyze_workflows_in_database(self, database_name: str) -> Dict:
        """分析單個數據庫中的 workflows 表"""
        print(f"\n{'='*80}")
        print(f"正在分析數據庫: {database_name}")
        print(f"{'='*80}")

        try:
            conn = await self.connect_to_database(database_name)

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
                    created_at
                FROM workflows
                WHERE steps IS NOT NULL AND steps != '[]'::jsonb
                ORDER BY id;
            """

            rows = await conn.fetch(query)

            if not rows:
                print(f"⚠ 數據庫中沒有找到任何 workflows")
                await conn.close()
                return {
                    'database': database_name,
                    'total_workflows': 0,
                    'workflows': [],
                    'step_id_usage': {},
                    'duplicates': []
                }

            print(f"\n找到 {len(rows)} 個 workflows\n")

            # 分析結果
            workflows_data = []
            step_id_to_workflows = defaultdict(list)  # step_id -> [(workflow_id, workflow_name)]

            for row in rows:
                workflow_id = row['workflow_id']
                workflow_name = row['workflow_name']
                steps = row['steps']  # JSONB array

                # 解析 steps JSONB
                step_ids = []
                if steps:
                    for step in steps:
                        if isinstance(step, dict) and 'id' in step:
                            step_id = step['id']
                            step_ids.append(step_id)
                            step_id_to_workflows[step_id].append({
                                'workflow_id': workflow_id,
                                'workflow_name': workflow_name,
                                'workflow_uuid': row['workflow_uuid'],
                                'acc_workflow_id': row['acc_workflow_id'],
                                'step': step
                            })

                workflows_data.append({
                    'workflow_id': workflow_id,
                    'workflow_name': workflow_name,
                    'workflow_uuid': row['workflow_uuid'],
                    'acc_workflow_id': row['acc_workflow_id'],
                    'status': row['status'],
                    'data_source': row['data_source'],
                    'created_at': str(row['created_at']),
                    'step_ids': step_ids,
                    'step_count': len(step_ids),
                    'steps': steps  # 保留完整的 steps 數據
                })

                # 打印 workflow 信息
                print(f"Workflow ID: {workflow_id}")
                print(f"  名稱: {workflow_name}")
                print(f"  UUID: {row['workflow_uuid']}")
                print(f"  ACC ID: {row['acc_workflow_id']}")
                print(f"  狀態: {row['status']}")
                print(f"  數據源: {row['data_source']}")
                print(f"  步驟數: {len(step_ids)}")
                print(f"  Step IDs: {step_ids}")
                print()

            # 查找重複的 step IDs
            duplicates = []
            for step_id, usage_list in step_id_to_workflows.items():
                if len(usage_list) > 1:
                    duplicates.append({
                        'step_id': step_id,
                        'usage_count': len(usage_list),
                        'used_in_workflows': usage_list
                    })

            await conn.close()

            return {
                'database': database_name,
                'total_workflows': len(rows),
                'workflows': workflows_data,
                'step_id_usage': dict(step_id_to_workflows),
                'duplicates': duplicates
            }

        except Exception as e:
            print(f"❌ 分析數據庫 {database_name} 時發生錯誤: {e}")
            import traceback
            traceback.print_exc()
            return {
                'database': database_name,
                'error': str(e),
                'total_workflows': 0,
                'workflows': [],
                'step_id_usage': {},
                'duplicates': []
            }

    async def analyze_all_databases(self):
        """分析所有數據庫"""
        databases = await self.get_all_project_databases()

        if not databases:
            print("❌ 沒有找到任何活動的項目數據庫")
            return

        print(f"\n找到 {len(databases)} 個活動的項目數據庫")
        print(f"數據庫列表: {databases}")

        all_results = []

        for db_name in databases:
            result = await self.analyze_workflows_in_database(db_name)
            all_results.append(result)

        # 生成綜合報告
        self.generate_report(all_results)

    def generate_report(self, results: List[Dict]):
        """生成分析報告"""
        print("\n" + "="*80)
        print("綜合分析報告")
        print("="*80)

        total_workflows = sum(r['total_workflows'] for r in results)
        databases_with_workflows = sum(1 for r in results if r['total_workflows'] > 0)

        print(f"\n總計:")
        print(f"  - 分析的數據庫數: {len(results)}")
        print(f"  - 包含 workflows 的數據庫數: {databases_with_workflows}")
        print(f"  - workflows 總數: {total_workflows}")

        # 檢查每個數據庫內的重複
        print(f"\n{'='*80}")
        print("數據庫內 Step ID 重複分析")
        print(f"{'='*80}")

        has_duplicates_within_db = False

        for result in results:
            if result['duplicates']:
                has_duplicates_within_db = True
                print(f"\n❌ 數據庫: {result['database']}")
                print(f"   發現 {len(result['duplicates'])} 個重複的 step IDs\n")

                for dup in result['duplicates']:
                    print(f"   Step ID: '{dup['step_id']}'")
                    print(f"   使用次數: {dup['usage_count']}")
                    print(f"   使用的 workflows:")
                    for usage in dup['used_in_workflows']:
                        print(f"     - Workflow ID: {usage['workflow_id']}")
                        print(f"       名稱: {usage['workflow_name']}")
                        print(f"       UUID: {usage['workflow_uuid']}")
                        print(f"       Step 詳情: {json.dumps(usage['step'], ensure_ascii=False, indent=10)}")
                    print()

        if not has_duplicates_within_db:
            print("\n✅ 所有數據庫內部均未發現 step ID 重複")

        # 檢查跨數據庫的重複（不太可能，但也檢查一下）
        print(f"\n{'='*80}")
        print("跨數據庫 Step ID 分析")
        print(f"{'='*80}")

        cross_db_step_ids = defaultdict(list)

        for result in results:
            db_name = result['database']
            for step_id, workflows in result.get('step_id_usage', {}).items():
                cross_db_step_ids[step_id].append({
                    'database': db_name,
                    'workflows': workflows
                })

        cross_db_duplicates = {
            step_id: usage_list
            for step_id, usage_list in cross_db_step_ids.items()
            if len(usage_list) > 1
        }

        if cross_db_duplicates:
            print(f"\n⚠ 發現 {len(cross_db_duplicates)} 個跨數據庫重複的 step IDs\n")
            for step_id, usage_list in cross_db_duplicates.items():
                print(f"   Step ID: '{step_id}'")
                print(f"   出現在 {len(usage_list)} 個數據庫中:")
                for usage in usage_list:
                    print(f"     - 數據庫: {usage['database']}")
                    print(f"       使用的 workflows: {len(usage['workflows'])} 個")
                    for wf in usage['workflows'][:2]:  # 只顯示前2個
                        print(f"         * {wf['workflow_name']} (ID: {wf['workflow_id']})")
                print()
        else:
            print("\n✅ 未發現跨數據庫的 step ID 重複")

        # 建議
        print(f"\n{'='*80}")
        print("建議")
        print(f"{'='*80}\n")

        if has_duplicates_within_db or cross_db_duplicates:
            print("❌ 發現 Step ID 重複問題！\n")
            print("建議的解決方案:")
            print("1. 為每個 workflow 使用唯一的 step ID 命名策略")
            print("   例如: '{workflow_uuid}_{step_order}' 或 '{workflow_id}_step_{order}'")
            print()
            print("2. 實施 step ID 唯一性約束:")
            print("   - 在創建 workflow 時自動生成唯一的 step IDs")
            print("   - 使用 UUID 或組合鍵確保唯一性")
            print()
            print("3. 數據修復:")
            print("   - 識別所有重複的 step IDs")
            print("   - 為重複的 steps 重新生成唯一 IDs")
            print("   - 同步更新相關的 review_progress 表中的 step_id 引用")
            print()
            print("4. 添加數據庫約束或應用層驗證:")
            print("   - 在 workflow 創建/更新時驗證 step IDs 唯一性")
            print("   - 考慮添加數據庫觸發器確保 steps JSONB 中的 IDs 唯一")
        else:
            print("✅ 未發現 step ID 重複問題")
            print()
            print("建議的最佳實踐:")
            print("1. 維持當前的 step ID 唯一性策略")
            print("2. 在創建新 workflow 時確保 step IDs 不與現有的重複")
            print("3. 考慮實施自動化的唯一性驗證機制")

        print()

async def main():
    analyzer = WorkflowStepAnalyzer()
    await analyzer.analyze_all_databases()

if __name__ == '__main__':
    asyncio.run(main())
