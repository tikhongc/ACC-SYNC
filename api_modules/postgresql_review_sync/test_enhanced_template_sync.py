#!/usr/bin/env python3
"""
增强模板同步功能测试脚本
测试整合后的工作流模板同步功能
"""

import asyncio
import sys
import os
import json
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from api_modules.postgresql_review_sync.review_sync_manager_enhanced import EnhancedReviewSyncManager
    from database_sql.review_data_access import ReviewDataAccess
    import utils
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保所有依赖模块都已正确安装")
    sys.exit(1)


class TemplateIntegrationTester:
    """模板集成测试器"""
    
    def __init__(self):
        """初始化测试器"""
        self.sync_manager = None
        self.test_project_id = "b.563a4c30-e30d-4869-ac02-2a18b6447abe"  # 示例项目ID
        
    def setup(self):
        """设置测试环境"""
        try:
            print("🔧 初始化增强同步管理器...")
            
            # 初始化数据访问层
            da = ReviewDataAccess()
            
            # 初始化增强同步管理器
            self.sync_manager = EnhancedReviewSyncManager(
                data_access=da,
                max_concurrent=5,  # 测试时使用较小的并发数
                enable_cache=True,
                cache_ttl=1800,
                cache_max_size=1000,
                batch_size=50
            )
            
            print("✅ 增强同步管理器初始化成功")
            return True
            
        except Exception as e:
            print(f"❌ 设置失败: {str(e)}")
            return False
    
    def test_base_templates(self):
        """测试基础模板功能"""
        print("\n" + "="*60)
        print("🧪 测试基础模板功能")
        print("="*60)
        
        try:
            # 测试获取基础模板
            print("📋 获取基础模板列表...")
            base_templates = self.sync_manager.get_base_templates()
            
            if base_templates:
                print(f"✅ 成功获取 {len(base_templates)} 个基础模板:")
                for template in base_templates:
                    print(f"   - {template['name']} ({template['template_key']}) - {template['steps_count']} 步骤")
            else:
                print("⚠ 没有找到基础模板，可能需要先运行数据库初始化脚本")
            
            # 测试按分类获取
            print("\n📋 按分类获取基础模板...")
            standard_templates = self.sync_manager.get_base_templates(category='standard')
            group_templates = self.sync_manager.get_base_templates(category='group')
            
            print(f"   标准模板: {len(standard_templates)} 个")
            print(f"   组审核模板: {len(group_templates)} 个")
            
            # 测试基于基础模板创建工作流
            if base_templates:
                print("\n🔨 测试基于基础模板创建工作流...")
                test_template = base_templates[0]
                
                workflow_data = {
                    'name': f"测试工作流 - {test_template['name']}",
                    'description': f"基于 {test_template['name']} 创建的测试工作流",
                    'steps_config': [
                        {
                            'candidates': {
                                'roles': ['Project Manager'],
                                'users': [],
                                'companies': []
                            }
                        }
                    ]
                }
                
                result = self.sync_manager.create_workflow_from_base_template(
                    test_template['template_key'], workflow_data
                )
                
                if result['status'] == 'success':
                    print("✅ 成功基于基础模板创建工作流配置")
                    print(f"   工作流名称: {result['workflow_config']['name']}")
                    print(f"   步骤数量: {result['workflow_config']['steps_count']}")
                else:
                    print(f"❌ 创建失败: {result.get('error', 'Unknown error')}")
            
            return True
            
        except Exception as e:
            print(f"❌ 基础模板测试失败: {str(e)}")
            return False
    
    async def test_template_sync(self):
        """测试模板同步功能"""
        print("\n" + "="*60)
        print("🧪 测试模板同步功能")
        print("="*60)
        
        try:
            # 获取访问令牌
            access_token = utils.get_access_token()
            if not access_token:
                print("⚠ 未找到访问令牌，跳过模板同步测试")
                return False
            
            print("🔑 访问令牌获取成功")
            
            # 创建异步HTTP会话并测试模板同步
            import aiohttp
            async with aiohttp.ClientSession() as session:
                print(f"🎯 开始测试模板同步: {self.test_project_id}")
                
                # 测试模板同步（不获取详细数据）
                print("\n📋 测试基础模板同步（不获取详细数据）...")
                result_basic = await self.sync_manager.sync_workflow_templates_enhanced(
                    session=session,
                    project_id=self.test_project_id,
                    access_token=access_token,
                    fetch_detailed_data=False,
                    show_progress=True
                )
                
                print(f"基础同步结果: {json.dumps(result_basic, indent=2, ensure_ascii=False, default=str)}")
                
                # 测试模板同步（获取详细数据）
                print("\n🔍 测试详细模板同步（获取详细数据）...")
                result_detailed = await self.sync_manager.sync_workflow_templates_enhanced(
                    session=session,
                    project_id=self.test_project_id,
                    access_token=access_token,
                    fetch_detailed_data=True,
                    show_progress=True
                )
                
                print(f"详细同步结果: {json.dumps(result_detailed, indent=2, ensure_ascii=False, default=str)}")
                
                return True
                
        except Exception as e:
            print(f"❌ 模板同步测试失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    async def test_full_integration(self):
        """测试完整集成功能"""
        print("\n" + "="*60)
        print("🧪 测试完整集成功能")
        print("="*60)
        
        try:
            # 获取访问令牌
            access_token = utils.get_access_token()
            if not access_token:
                print("⚠ 未找到访问令牌，跳过完整集成测试")
                return False
            
            # 测试完整项目同步
            account_id = "test_account_id"  # 替换为实际的账户ID
            
            print(f"🚀 开始完整项目同步测试...")
            result = await self.sync_manager.full_project_sync_with_account_data(
                account_id=account_id,
                project_id=self.test_project_id,
                access_token=access_token,
                sync_account_data=False,  # 跳过账户数据同步
                sync_templates=True,
                fetch_detailed_template_data=True,
                show_progress=True
            )
            
            print(f"\n📊 完整同步结果:")
            print(f"   执行时间: {result.get('execution_time', 'N/A')}")
            print(f"   同步组件: {result.get('sync_components', {})}")
            
            # 显示同步统计
            sync_stats = result.get('sync_statistics', {})
            if sync_stats:
                print(f"\n📈 同步统计:")
                print(f"   模板: {sync_stats.get('templates_synced', 0)} 新增, {sync_stats.get('templates_updated', 0)} 更新")
                print(f"   工作流: {sync_stats.get('workflows_synced', 0)} 新增, {sync_stats.get('workflows_updated', 0)} 更新")
                print(f"   评审: {sync_stats.get('reviews_synced', 0)} 新增, {sync_stats.get('reviews_updated', 0)} 更新")
            
            # 显示性能指标
            performance = result.get('performance_metrics', {})
            if performance:
                summary = performance.get('summary', {})
                print(f"\n⚡ 性能指标:")
                print(f"   API调用: {summary.get('api_calls', 0)} 次")
                print(f"   缓存命中率: {summary.get('cache_hit_rate', 0):.1f}%")
                print(f"   数据库查询: {summary.get('db_queries', 0)} 次")
            
            return True
            
        except Exception as e:
            print(f"❌ 完整集成测试失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def test_performance_analysis(self):
        """测试性能分析功能"""
        print("\n" + "="*60)
        print("🧪 测试性能分析功能")
        print("="*60)
        
        try:
            # 获取性能报告
            print("📊 获取性能报告...")
            report = self.sync_manager.get_performance_report()
            
            print("✅ 性能报告生成成功")
            
            # 打印性能报告
            print("\n📈 性能分析报告:")
            self.sync_manager.print_performance_report()
            
            return True
            
        except Exception as e:
            print(f"❌ 性能分析测试失败: {str(e)}")
            return False
    
    async def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始增强模板同步功能集成测试")
        print("=" * 80)
        print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"测试项目: {self.test_project_id}")
        print("=" * 80)
        
        # 设置测试环境
        if not self.setup():
            print("❌ 测试环境设置失败，退出测试")
            return False
        
        test_results = []
        
        # 运行各项测试
        tests = [
            ("基础模板功能", self.test_base_templates),
            ("模板同步功能", self.test_template_sync),
            ("完整集成功能", self.test_full_integration),
            ("性能分析功能", self.test_performance_analysis),
        ]
        
        for test_name, test_func in tests:
            print(f"\n🧪 运行测试: {test_name}")
            try:
                if asyncio.iscoroutinefunction(test_func):
                    result = await test_func()
                else:
                    result = test_func()
                test_results.append((test_name, result))
            except Exception as e:
                print(f"❌ 测试 {test_name} 出现异常: {str(e)}")
                test_results.append((test_name, False))
        
        # 生成测试报告
        print("\n" + "=" * 80)
        print("📋 测试结果汇总")
        print("=" * 80)
        
        passed = 0
        total = len(test_results)
        
        for test_name, result in test_results:
            status = "✅ 通过" if result else "❌ 失败"
            print(f"   {test_name}: {status}")
            if result:
                passed += 1
        
        print(f"\n📊 测试统计: {passed}/{total} 通过")
        
        if passed == total:
            print("🎉 所有测试通过！")
        else:
            print("⚠ 部分测试失败，请检查错误信息")
        
        return passed == total


async def main():
    """主函数"""
    tester = TemplateIntegrationTester()
    success = await tester.run_all_tests()
    
    if success:
        print("\n✅ 增强模板同步功能集成测试完成")
        return 0
    else:
        print("\n❌ 测试失败")
        return 1


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n⚠ 测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试运行失败: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
