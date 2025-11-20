# -*- coding: utf-8 -*-
"""
Submittal API Blueprint for Flask
提供 Submittal 相关的 API 端点
"""

from flask import Blueprint, request, jsonify, session
from api_modules.submittal_api import SubmittalAPI, convert_project_id
import utils
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

submittals_bp = Blueprint('submittals', __name__, url_prefix='/api/submittals')

# 創建測試端點藍圖
test_submittals_bp = Blueprint('test_submittals', __name__, url_prefix='/api/test/submittals')


def get_submittal_client():
    """获取 Submittal API 客户端实例"""
    access_token = utils.get_access_token()
    if not access_token:
        return None
    return SubmittalAPI(access_token=access_token)


@submittals_bp.route('/<project_id>/items', methods=['GET'])
def get_items(project_id):
    """
    获取项目的所有 Submittal 项目列表
    
    Query Parameters:
        - limit: 每页数量 (1-50, 默认 20)
        - offset: 偏移量 (默认 0)
        - sort: 排序字段 (例如: 'updatedAt desc')
        - filter[statusId]: 状态过滤
    """
    try:
        client = get_submittal_client()
        if not client:
            return jsonify({'error': 'Unauthorized, please login first'}), 401
        
        # 移除 'b.' 前缀（Submittal API 要求）
        clean_project_id = convert_project_id(project_id)
        
        # 获取查询参数并验证
        # 注意：Autodesk Submittal API 的 limit 上限是 50，不是 100
        limit = request.args.get('limit', 20, type=int)
        limit = min(max(limit, 1), 50)  # 限制在 1-50 之间
        
        offset = request.args.get('offset', 0, type=int)
        sort = request.args.get('sort', None)
        
        # 构建过滤器参数
        params = {
            'limit': limit,
            'offset': offset
        }
        
        if sort:
            params['sort'] = sort
        
        # 添加 filter 参数
        for key, value in request.args.items():
            if key.startswith('filter['):
                params[key] = value
        
        result = client.get_items(
            project_id=clean_project_id,
            **params
        )
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"获取 Submittal 项目列表失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


@submittals_bp.route('/<project_id>/items/<item_id>', methods=['GET'])
def get_item(project_id, item_id):
    """获取单个 Submittal 项目的详细信息"""
    try:
        client = get_submittal_client()
        if not client:
            return jsonify({'error': 'Unauthorized, please login first'}), 401
        
        clean_project_id = convert_project_id(project_id)
        result = client.get_item(project_id=clean_project_id, item_id=item_id)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"获取 Submittal 项目详情失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


@submittals_bp.route('/<project_id>/items/<item_id>/attachments', methods=['GET'])
def get_attachments(project_id, item_id):
    """获取 Submittal 项目的附件列表"""
    try:
        client = get_submittal_client()
        if not client:
            return jsonify({'error': 'Unauthorized, please login first'}), 401
        
        clean_project_id = convert_project_id(project_id)
        
        # 限制在 API 允许的范围内 (1-50)
        limit = request.args.get('limit', 50, type=int)
        limit = min(max(limit, 1), 50)
        offset = request.args.get('offset', 0, type=int)
        
        result = client.get_attachments(
            project_id=clean_project_id,
            item_id=item_id,
            limit=limit,
            offset=offset
        )
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"获取附件列表失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


@submittals_bp.route('/<project_id>/items/<item_id>/revisions', methods=['GET'])
def get_revisions(project_id, item_id):
    """获取 Submittal 项目的修订历史和审核流程"""
    try:
        client = get_submittal_client()
        if not client:
            return jsonify({'error': 'Unauthorized, please login first'}), 401
        
        clean_project_id = convert_project_id(project_id)
        
        # 限制在 API 允许的范围内 (1-50)
        limit = request.args.get('limit', 50, type=int)
        limit = min(max(limit, 1), 50)
        offset = request.args.get('offset', 0, type=int)
        
        result = client.get_item_revisions(
            project_id=clean_project_id,
            item_id=item_id,
            limit=limit,
            offset=offset
        )
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"获取修订历史失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


@submittals_bp.route('/<project_id>/items/<item_id>/steps', methods=['GET'])
def get_steps(project_id, item_id):
    """获取 Submittal 项目的审核步骤和任务"""
    try:
        client = get_submittal_client()
        if not client:
            return jsonify({'error': 'Unauthorized, please login first'}), 401
        
        clean_project_id = convert_project_id(project_id)
        
        # 限制在 API 允许的范围内 (1-50)
        limit = request.args.get('limit', 50, type=int)
        limit = min(max(limit, 1), 50)
        offset = request.args.get('offset', 0, type=int)
        
        result = client.get_steps(
            project_id=clean_project_id,
            item_id=item_id,
            limit=limit,
            offset=offset
        )
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"获取审核步骤失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


@submittals_bp.route('/<project_id>/items/<item_id>/steps/<step_id>', methods=['GET'])
def get_step(project_id, item_id, step_id):
    """获取单个审核步骤的详细信息"""
    try:
        client = get_submittal_client()
        if not client:
            return jsonify({'error': 'Unauthorized, please login first'}), 401
        
        clean_project_id = convert_project_id(project_id)
        
        result = client.get_step(
            project_id=clean_project_id,
            item_id=item_id,
            step_id=step_id
        )
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"获取审核步骤详情失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


@submittals_bp.route('/<project_id>/metadata', methods=['GET'])
def get_metadata(project_id):
    """
    获取项目的 Submittal 元数据
    包括: responses, item-types, workflow templates 等
    """
    try:
        client = get_submittal_client()
        if not client:
            return jsonify({'error': 'Unauthorized, please login first'}), 401
        
        clean_project_id = convert_project_id(project_id)
        
        # 并发获取所有元数据
        metadata = {
            'responses': client.get_responses(clean_project_id),
            'itemTypes': client.get_item_types(clean_project_id),
            'templates': client.get_templates(clean_project_id),
            'specs': client.get_specs(clean_project_id)
        }
        
        return jsonify(metadata)
    
    except Exception as e:
        logger.error(f"获取元数据失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


@submittals_bp.route('/<project_id>/responses', methods=['GET'])
def get_responses(project_id):
    """获取项目的响应类型列表"""
    try:
        client = get_submittal_client()
        if not client:
            return jsonify({'error': 'Unauthorized, please login first'}), 401
        
        clean_project_id = convert_project_id(project_id)
        result = client.get_responses(project_id=clean_project_id)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"获取响应类型失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


@submittals_bp.route('/<project_id>/item-types', methods=['GET'])
def get_item_types(project_id):
    """获取项目的 Submittal 类型列表"""
    try:
        client = get_submittal_client()
        if not client:
            return jsonify({'error': 'Unauthorized, please login first'}), 401
        
        clean_project_id = convert_project_id(project_id)
        result = client.get_item_types(project_id=clean_project_id)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"获取类型列表失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


@submittals_bp.route('/<project_id>/templates', methods=['GET'])
def get_templates(project_id):
    """获取项目的审核流程模板列表"""
    try:
        client = get_submittal_client()
        if not client:
            return jsonify({'error': 'Unauthorized, please login first'}), 401
        
        clean_project_id = convert_project_id(project_id)
        result = client.get_templates(project_id=clean_project_id)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"获取模板列表失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


@submittals_bp.route('/<project_id>/specs', methods=['GET'])
def get_specs(project_id):
    """获取项目的规格列表"""
    try:
        client = get_submittal_client()
        if not client:
            return jsonify({'error': 'Unauthorized, please login first'}), 401
        
        clean_project_id = convert_project_id(project_id)
        result = client.get_specs(project_id=clean_project_id)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"获取规格列表失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


@submittals_bp.route('/<project_id>/packages', methods=['GET'])
def get_packages(project_id):
    """获取项目的 Submittal 包列表"""
    try:
        client = get_submittal_client()
        if not client:
            return jsonify({'error': 'Unauthorized, please login first'}), 401
        
        clean_project_id = convert_project_id(project_id)
        
        # 限制在 API 允许的范围内 (1-50)
        limit = request.args.get('limit', 50, type=int)
        limit = min(max(limit, 1), 50)
        offset = request.args.get('offset', 0, type=int)
        
        result = client.get_packages(
            project_id=clean_project_id,
            limit=limit,
            offset=offset
        )
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"获取包列表失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


@submittals_bp.route('/jarvis/<project_id>', methods=['GET'])
def get_all_data(project_id):
    """
    Jarvis 端点：获取完整的 Submittal 数据
    包括所有项目、元数据等
    """
    try:
        client = get_submittal_client()
        if not client:
            return jsonify({'error': 'Unauthorized, please login first'}), 401
        
        clean_project_id = convert_project_id(project_id)
        
        # 获取所有数据（使用 API 允许的最大 limit: 50）
        data = {
            'items': client.get_items(project_id=clean_project_id, limit=50),
            'metadata': {
                'responses': client.get_responses(clean_project_id),
                'itemTypes': client.get_item_types(clean_project_id),
                'templates': client.get_templates(clean_project_id),
                'specs': client.get_specs(clean_project_id)
            },
            'packages': client.get_packages(project_id=clean_project_id, limit=50)
        }
        
        return jsonify(data)
    
    except Exception as e:
        logger.error(f"获取完整数据失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


@submittals_bp.route('/jarvis/<project_id>/metadata', methods=['GET'])
def get_all_metadata(project_id):
    """Jarvis 端点：获取所有元数据"""
    try:
        client = get_submittal_client()
        if not client:
            return jsonify({'error': 'Unauthorized, please login first'}), 401
        
        clean_project_id = convert_project_id(project_id)
        
        metadata = {
            'responses': client.get_responses(clean_project_id),
            'itemTypes': client.get_item_types(clean_project_id),
            'templates': client.get_templates(clean_project_id),
            'specs': client.get_specs(clean_project_id)
        }
        
        return jsonify(metadata)
    
    except Exception as e:
        logger.error(f"获取元数据失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


@submittals_bp.route('/debug/<project_id>/items/<item_id>/workflow', methods=['GET'])
def debug_workflow(project_id, item_id):
    """
    调试 Submittal 工作流问题
    
    Query Parameters:
        - detailed: 是否返回详细信息 (true/false, 默认 false)
    """
    try:
        client = get_submittal_client()
        if not client:
            return jsonify({'error': 'Unauthorized, please login first'}), 401
        
        clean_project_id = convert_project_id(project_id)
        detailed = request.args.get('detailed', 'false').lower() == 'true'
        
        # 导入调试工具 (如果存在)
        try:
            from debug_submittal_workflow import SubmittalWorkflowDebugger
        except ImportError:
            return jsonify({'error': 'Debug tool module not found'}), 500
        
        debugger = SubmittalWorkflowDebugger(utils.get_access_token())
        debug_results = debugger.debug_workflow_issue(project_id, item_id)
        
        # 如果不需要详细信息，只返回摘要
        if not detailed:
            summary = {
                'project_id': project_id,
                'item_id': item_id,
                'diagnosis': debug_results.get('diagnosis', {}),
                'workflow_status': {
                    'has_templates': debug_results.get('checks', {}).get('templates', {}).get('has_templates', False),
                    'templates_count': debug_results.get('checks', {}).get('templates', {}).get('count', 0),
                    'has_revisions': debug_results.get('checks', {}).get('revisions', {}).get('has_revisions', False),
                    'revisions_count': debug_results.get('checks', {}).get('revisions', {}).get('count', 0),
                    'has_steps': debug_results.get('checks', {}).get('steps', {}).get('has_steps', False),
                    'steps_count': debug_results.get('checks', {}).get('steps', {}).get('count', 0),
                    'item_state': debug_results.get('checks', {}).get('item_details', {}).get('state_id'),
                    'item_status': debug_results.get('checks', {}).get('item_details', {}).get('status_id'),
                    'workflow_eligible': debug_results.get('checks', {}).get('workflow_eligibility', {}).get('eligible', False)
                }
            }
            return jsonify(summary)
        
        return jsonify(debug_results)
    
    except Exception as e:
        logger.error(f"工作流调试失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


@submittals_bp.route('/debug/<project_id>/workflow-status', methods=['GET'])
def get_workflow_status(project_id):
    """
    获取项目的整体工作流状态
    """
    try:
        client = get_submittal_client()
        if not client:
            return jsonify({'error': 'Unauthorized, please login first'}), 401
        
        clean_project_id = convert_project_id(project_id)
        
        # 获取项目basicInfo
        try:
            metadata = client.get_metadata(clean_project_id)
            templates_response = client.get_templates(clean_project_id)
            items_response = client.get_items(clean_project_id, limit=10)
            
            templates = templates_response.get('results', [])
            items = items_response.get('results', [])
            
            # 统计不同状态的项目
            status_counts = {}
            state_counts = {}
            workflow_items = 0
            
            for item in items:
                status_id = item.get('statusId')
                state_id = item.get('stateId')
                
                status_counts[status_id] = status_counts.get(status_id, 0) + 1
                state_counts[state_id] = state_counts.get(state_id, 0) + 1
                
                # 检查是否在工作流状态
                if state_id in ['mgr-1', 'rev', 'mgr-2', 'sbc-2']:
                    workflow_items += 1
            
            status = {
                'project_id': project_id,
                'project_configured': {
                    'has_manager_mapping': metadata.get('isManagerMappingDefined', False),
                    'has_templates': len(templates) > 0,
                    'templates_count': len(templates),
                    'custom_identifier_sequence_type': metadata.get('customIdentifierSequenceType'),
                    'no_packages': metadata.get('noPackagesInProject', True),
                    'no_items': metadata.get('noItemsInProject', True)
                },
                'items_summary': {
                    'total_items': len(items),
                    'items_in_workflow': workflow_items,
                    'status_distribution': status_counts,
                    'state_distribution': state_counts
                },
                'templates': [
                    {
                        'id': t.get('id'),
                        'name': t.get('name'),
                        'steps_count': len(t.get('steps', []))
                    } for t in templates
                ],
                'recommendations': []
            }
            
            # 生成建议
            if not status['project_configured']['has_templates']:
                status['recommendations'].append("项目没有配置审核模板，需要在 ACC UI 中创建审核模板")
            
            if not status['project_configured']['has_manager_mapping']:
                status['recommendations'].append("项目没有配置管理员映射，可能影响工作流分配")
            
            if status['items_summary']['items_in_workflow'] == 0:
                status['recommendations'].append("没有项目处于工作流状态，检查项目是否已提交审核")
            
            return jsonify(status)
            
        except Exception as e:
            logger.error(f"获取工作流状态失败: {str(e)}")
            return jsonify({'error': f"获取工作流状态失败: {str(e)}"}), 500
    
    except Exception as e:
        logger.error(f"工作流状态检查失败: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ========================================================================
# Test Endpoints for Frontend Development
# ========================================================================

@test_submittals_bp.route('/test-workflow-log/<project_id>/<item_id>', methods=['GET'])
def test_workflow_log(project_id, item_id):
    """
    测试端点：获取 Submittal 工作流活动日志
    
    这个端点专门为前端开发提供，整合多个 API 调用来构建完整的活动日志
    """
    try:
        client = get_submittal_client()
        if not client:
            return jsonify({'error': 'Unauthorized, please login first'}), 401
        
        clean_project_id = convert_project_id(project_id)
        
        # 初始化响应数据结构
        response_data = {
            'test_summary': {
                'success': True,
                'has_errors': False,
                'error_count': 0,
                'api_calls_made': [],
                'timestamp': datetime.now().isoformat()
            },
            'workflow_log': {
                'success': False,
                'activities': [],
                'error': None
            },
            'formatted_display': {
                'success': False,
                'formatted_activities': [],
                'error': None
            },
            'activity_summary': {
                'success': False,
                'data': None,
                'error': None
            },
            'item_details': {
                'success': False,
                'data': None,
                'error': None
            },
            'attachments': {
                'success': False,
                'data': [],
                'error': None
            },
            'revisions': {
                'success': False,
                'data': [],
                'error': None
            },
            'steps': {
                'success': False,
                'data': [],
                'error': None
            }
        }
        
        # 1. 获取基础工作流活动日志
        try:
            logger.info(f"获取工作流活动日志: {clean_project_id}/{item_id}")
            activities = client.get_workflow_activity_log(clean_project_id, item_id)
            response_data['workflow_log']['success'] = True
            response_data['workflow_log']['activities'] = activities
            response_data['test_summary']['api_calls_made'].append('get_workflow_activity_log')
            logger.info(f"成功获取 {len(activities)} 个活动记录")
        except Exception as e:
            error_msg = f"获取工作流活动日志失败: {str(e)}"
            logger.error(error_msg)
            response_data['workflow_log']['error'] = error_msg
            response_data['test_summary']['has_errors'] = True
            response_data['test_summary']['error_count'] += 1
        
        # 2. 获取格式化的活动日志用于显示
        try:
            logger.info(f"获取格式化活动日志: {clean_project_id}/{item_id}")
            formatted_activities = client.format_activity_log_for_display(clean_project_id, item_id)
            response_data['formatted_display']['success'] = True
            response_data['formatted_display']['formatted_activities'] = formatted_activities
            response_data['test_summary']['api_calls_made'].append('format_activity_log_for_display')
            logger.info(f"成功格式化 {len(formatted_activities)} 个活动记录")
        except Exception as e:
            error_msg = f"格式化活动日志失败: {str(e)}"
            logger.error(error_msg)
            response_data['formatted_display']['error'] = error_msg
            response_data['test_summary']['has_errors'] = True
            response_data['test_summary']['error_count'] += 1
        
        # 3. 获取活动摘要
        try:
            logger.info(f"获取活动摘要: {clean_project_id}/{item_id}")
            summary = client.get_activity_summary(clean_project_id, item_id)
            response_data['activity_summary']['success'] = True
            response_data['activity_summary']['data'] = summary
            response_data['test_summary']['api_calls_made'].append('get_activity_summary')
            logger.info(f"成功获取活动摘要")
        except Exception as e:
            error_msg = f"获取活动摘要失败: {str(e)}"
            logger.error(error_msg)
            response_data['activity_summary']['error'] = error_msg
            response_data['test_summary']['has_errors'] = True
            response_data['test_summary']['error_count'] += 1
        
        # 4. 获取项目详情
        try:
            logger.info(f"获取项目详情: {clean_project_id}/{item_id}")
            item_details = client.get_item(clean_project_id, item_id)
            response_data['item_details']['success'] = True
            response_data['item_details']['data'] = item_details
            response_data['test_summary']['api_calls_made'].append('get_item')
            logger.info(f"成功获取项目详情")
        except Exception as e:
            error_msg = f"获取项目详情失败: {str(e)}"
            logger.error(error_msg)
            response_data['item_details']['error'] = error_msg
            response_data['test_summary']['has_errors'] = True
            response_data['test_summary']['error_count'] += 1
        
        # 5. 获取附件列表
        try:
            logger.info(f"获取附件列表: {clean_project_id}/{item_id}")
            attachments_response = client.get_attachments(clean_project_id, item_id)
            attachments = attachments_response.get('results', [])
            response_data['attachments']['success'] = True
            response_data['attachments']['data'] = attachments
            response_data['test_summary']['api_calls_made'].append('get_attachments')
            logger.info(f"成功获取 {len(attachments)} 个附件")
        except Exception as e:
            error_msg = f"获取附件列表失败: {str(e)}"
            logger.error(error_msg)
            response_data['attachments']['error'] = error_msg
            response_data['test_summary']['has_errors'] = True
            response_data['test_summary']['error_count'] += 1
        
        # 6. 获取修订历史
        try:
            logger.info(f"获取修订历史: {clean_project_id}/{item_id}")
            revisions_response = client.get_item_revisions(clean_project_id, item_id)
            revisions = revisions_response.get('results', [])
            response_data['revisions']['success'] = True
            response_data['revisions']['data'] = revisions
            response_data['test_summary']['api_calls_made'].append('get_item_revisions')
            logger.info(f"成功获取 {len(revisions)} 个修订记录")
        except Exception as e:
            error_msg = f"获取修订历史失败: {str(e)}"
            logger.error(error_msg)
            response_data['revisions']['error'] = error_msg
            response_data['test_summary']['has_errors'] = True
            response_data['test_summary']['error_count'] += 1
        
        # 7. 获取审核步骤
        try:
            logger.info(f"获取审核步骤: {clean_project_id}/{item_id}")
            steps_response = client.get_steps(clean_project_id, item_id)
            steps = steps_response.get('results', [])
            response_data['steps']['success'] = True
            response_data['steps']['data'] = steps
            response_data['test_summary']['api_calls_made'].append('get_steps')
            logger.info(f"成功获取 {len(steps)} 个审核步骤")
        except Exception as e:
            error_msg = f"获取审核步骤失败: {str(e)}"
            logger.error(error_msg)
            response_data['steps']['error'] = error_msg
            response_data['test_summary']['has_errors'] = True
            response_data['test_summary']['error_count'] += 1
        
        # 更新测试摘要
        response_data['test_summary']['success'] = not response_data['test_summary']['has_errors']
        
        logger.info(f"测试工作流日志完成: 成功={response_data['test_summary']['success']}, "
                   f"错误数={response_data['test_summary']['error_count']}, "
                   f"API调用={len(response_data['test_summary']['api_calls_made'])}")
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"测试工作流日志时出错: {str(e)}")
        return jsonify({
            'test_summary': {
                'success': False,
                'has_errors': True,
                'error_count': 1,
                'api_calls_made': [],
                'timestamp': datetime.now().isoformat()
            },
            'error': f"测试工作流日志失败: {str(e)}"
        }), 500