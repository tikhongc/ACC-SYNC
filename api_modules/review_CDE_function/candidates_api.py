# -*- coding: utf-8 -*-
"""
简化的候选人管理 API
专注于 review_step_candidates 配置表的 CRUD 操作
"""

import json
import psycopg2
import psycopg2.extras
from flask import Blueprint, request, jsonify
from typing import Dict, List, Any, Optional
import sys
import os

# 添加数据库访问路径
sys.path.append(os.path.join(os.path.dirname(__file__), '../../database_sql'))

try:
    from review_data_access_enhanced import EnhancedReviewDataAccess
except ImportError:
    from database_access import DatabaseAccess as EnhancedReviewDataAccess

# 创建蓝图
candidates_bp = Blueprint('candidates', __name__)

class CandidatesManager:
    """候选人配置管理器 - 专注于 review_step_candidates 表"""
    
    def __init__(self):
        self.da = EnhancedReviewDataAccess()
    
    def get_connection(self):
        """获取数据库连接"""
        return self.da.get_connection()
    
    def _standardize_candidates(self, candidates: Dict) -> Dict:
        """标准化候选人数据格式"""
        if not isinstance(candidates, dict):
            return {'users': [], 'roles': [], 'companies': []}
        
        return {
            'users': candidates.get('users', []),
            'roles': candidates.get('roles', []),
            'companies': candidates.get('companies', [])
        }
    
    # ========================================================================
    # 核心 CRUD 操作
    # ========================================================================
    
    def get_step_candidates(self, review_id: int, step_id: str) -> Dict[str, Any]:
        """
        获取指定步骤的候选人配置
        
        Args:
            review_id: 评审ID
            step_id: 步骤ID
            
        Returns:
            候选人配置信息
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            cursor.execute("""
                SELECT 
                    id, review_id, step_id, step_name, step_type, step_order,
                    candidates, source, is_active, created_at, updated_at
                FROM review_step_candidates 
                WHERE review_id = %s AND step_id = %s AND is_active = true
            """, [review_id, step_id])
            
            result = cursor.fetchone()
            
            if result:
                return {
                    'success': True,
                    'data': {
                        'id': result['id'],
                        'review_id': result['review_id'],
                        'step_id': result['step_id'],
                        'step_name': result['step_name'],
                        'step_type': result['step_type'],
                        'step_order': result['step_order'],
                        'candidates': result['candidates'],
                        'source': result['source'],
                        'is_active': result['is_active'],
                        'created_at': result['created_at'].isoformat() if result['created_at'] else None,
                        'updated_at': result['updated_at'].isoformat() if result['updated_at'] else None
                    }
                }
            else:
                return {
                    'success': False,
                    'error': f'未找到评审 {review_id} 步骤 {step_id} 的候选人配置',
                    'data': None
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'获取候选人配置失败: {str(e)}',
                'data': None
            }
        finally:
            if conn:
                conn.close()
    
    def get_review_candidates(self, review_id: int) -> Dict[str, Any]:
        """
        获取评审所有步骤的候选人配置
        
        Args:
            review_id: 评审ID
            
        Returns:
            所有步骤的候选人配置
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            cursor.execute("""
                SELECT 
                    id, review_id, step_id, step_name, step_type, step_order,
                    candidates, source, is_active, created_at, updated_at
                FROM review_step_candidates 
                WHERE review_id = %s AND is_active = true
                ORDER BY step_order ASC
            """, [review_id])
            
            results = cursor.fetchall()
            
            steps_config = []
            for result in results:
                steps_config.append({
                    'id': result['id'],
                    'review_id': result['review_id'],
                    'step_id': result['step_id'],
                    'step_name': result['step_name'],
                    'step_type': result['step_type'],
                    'step_order': result['step_order'],
                    'candidates': result['candidates'],
                    'source': result['source'],
                    'is_active': result['is_active'],
                    'created_at': result['created_at'].isoformat() if result['created_at'] else None,
                    'updated_at': result['updated_at'].isoformat() if result['updated_at'] else None
                })
            
            return {
                'success': True,
                'data': {
                    'review_id': review_id,
                    'steps_count': len(steps_config),
                    'steps': steps_config
                }
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'获取评审候选人配置失败: {str(e)}',
                'data': None
            }
        finally:
            if conn:
                conn.close()
    
    def create_step_candidates(self, review_id: int, step_id: str, step_config: Dict) -> Dict[str, Any]:
        """
        创建步骤候选人配置
        
        Args:
            review_id: 评审ID
            step_id: 步骤ID
            step_config: 步骤配置信息
            
        Returns:
            创建结果
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # 标准化候选人数据
            candidates = self._standardize_candidates(step_config.get('candidates', {}))
            
            cursor.execute("""
                INSERT INTO review_step_candidates (
                    review_id, step_id, step_name, step_type, step_order,
                    candidates, source, is_active
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id, created_at, updated_at
            """, [
                review_id,
                step_id,
                step_config.get('step_name', ''),
                step_config.get('step_type', ''),
                step_config.get('step_order', 0),
                psycopg2.extras.Json(candidates),
                step_config.get('source', 'custom'),
                True
            ])
            
            result = cursor.fetchone()
            conn.commit()
            
            return {
                'success': True,
                'message': f'成功创建步骤 {step_id} 的候选人配置',
                'data': {
                    'id': result['id'],
                    'review_id': review_id,
                    'step_id': step_id,
                    'candidates': candidates,
                    'created_at': result['created_at'].isoformat(),
                    'updated_at': result['updated_at'].isoformat()
                }
            }
                
        except psycopg2.IntegrityError as e:
            return {
                'success': False,
                'error': f'候选人配置已存在或数据冲突: {str(e)}',
                'data': None
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'创建候选人配置失败: {str(e)}',
                'data': None
            }
        finally:
            if conn:
                conn.close()
    
    def update_step_candidates(self, review_id: int, step_id: str, candidates: Dict) -> Dict[str, Any]:
        """
        更新步骤候选人配置
        
        Args:
            review_id: 评审ID
            step_id: 步骤ID
            candidates: 新的候选人配置
            
        Returns:
            更新结果
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # 标准化候选人数据
            standardized_candidates = self._standardize_candidates(candidates)
            
            cursor.execute("""
                UPDATE review_step_candidates 
                SET 
                    candidates = %s,
                    source = 'custom',
                    updated_at = CURRENT_TIMESTAMP
                WHERE review_id = %s AND step_id = %s AND is_active = true
                RETURNING id, updated_at
            """, [
                psycopg2.extras.Json(standardized_candidates),
                review_id,
                step_id
            ])
            
            result = cursor.fetchone()
            
            if result:
                conn.commit()
                return {
                    'success': True,
                    'message': f'成功更新步骤 {step_id} 的候选人配置',
                    'data': {
                        'id': result['id'],
                        'review_id': review_id,
                        'step_id': step_id,
                        'candidates': standardized_candidates,
                        'updated_at': result['updated_at'].isoformat()
                    }
                }
            else:
                return {
                    'success': False,
                    'error': f'未找到评审 {review_id} 步骤 {step_id} 的候选人配置',
                    'data': None
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'更新候选人配置失败: {str(e)}',
                'data': None
            }
        finally:
            if conn:
                conn.close()
    
    def delete_step_candidates(self, review_id: int, step_id: str) -> Dict[str, Any]:
        """
        删除步骤候选人配置（软删除）
        
        Args:
            review_id: 评审ID
            step_id: 步骤ID
            
        Returns:
            删除结果
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            cursor.execute("""
                UPDATE review_step_candidates 
                SET 
                    is_active = false,
                    updated_at = CURRENT_TIMESTAMP
                WHERE review_id = %s AND step_id = %s AND is_active = true
                RETURNING id
            """, [review_id, step_id])
            
            result = cursor.fetchone()
            
            if result:
                conn.commit()
                return {
                    'success': True,
                    'message': f'成功删除步骤 {step_id} 的候选人配置',
                    'data': {'id': result['id']}
                }
            else:
                return {
                    'success': False,
                    'error': f'未找到评审 {review_id} 步骤 {step_id} 的候选人配置',
                    'data': None
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'删除候选人配置失败: {str(e)}',
                'data': None
            }
        finally:
            if conn:
                conn.close()
    
    # ========================================================================
    # 辅助功能
    # ========================================================================
    
    def get_available_candidates(self, project_id: str) -> Dict[str, Any]:
        """
        获取项目中所有可用的候选人（用户、角色、公司）
        
        Args:
            project_id: 项目ID
            
        Returns:
            可用候选人列表
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # 获取用户
            cursor.execute("""
                SELECT DISTINCT 
                    user_name as name,
                    user_id as autodeskId,
                    email
                FROM project_users 
                WHERE project_id = %s
                ORDER BY user_name
            """, [project_id])
            users = cursor.fetchall()
            
            # 获取角色
            cursor.execute("""
                SELECT DISTINCT 
                    role_name as name,
                    role_id as id
                FROM project_roles 
                WHERE project_id = %s
                ORDER BY role_name
            """, [project_id])
            roles = cursor.fetchall()
            
            # 获取公司
            cursor.execute("""
                SELECT DISTINCT 
                    company_name as name,
                    company_id as autodeskId
                FROM project_companies 
                WHERE project_id = %s
                ORDER BY company_name
            """, [project_id])
            companies = cursor.fetchall()
            
            return {
                'success': True,
                'data': {
                    'project_id': project_id,
                    'users': [dict(user) for user in users],
                    'roles': [dict(role) for role in roles],
                    'companies': [dict(company) for company in companies]
                }
            }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'获取可用候选人失败: {str(e)}',
                'data': None
            }
        finally:
            if conn:
                conn.close()


# ============================================================================
# API 端点
# ============================================================================

# 创建管理器实例
candidates_manager = CandidatesManager()

@candidates_bp.route('/api/candidates/reviews/<int:review_id>/steps/<step_id>', methods=['GET'])
def get_step_candidates(review_id, step_id):
    """获取指定步骤的候选人配置"""
    result = candidates_manager.get_step_candidates(review_id, step_id)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 404

@candidates_bp.route('/api/candidates/reviews/<int:review_id>', methods=['GET'])
def get_review_candidates(review_id):
    """获取评审所有步骤的候选人配置"""
    result = candidates_manager.get_review_candidates(review_id)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 404

@candidates_bp.route('/api/candidates/reviews/<int:review_id>/steps/<step_id>', methods=['POST'])
def create_step_candidates(review_id, step_id):
    """创建步骤候选人配置"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': '请提供步骤配置数据'
            }), 400
        
        result = candidates_manager.create_step_candidates(review_id, step_id, data)
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'创建候选人配置失败: {str(e)}'
        }), 500

@candidates_bp.route('/api/candidates/reviews/<int:review_id>/steps/<step_id>/dynamic-update', methods=['PUT'])
def dynamic_update_step_candidates(review_id, step_id):
    """
    動態修改候選人配置 - 支持等待審閱和開始審閱階段

    Request Body:
    {
        "candidates": {
            "users": [{"autodeskId": "xxx", "name": "xxx", "email": "xxx"}],
            "roles": [{"id": "xxx", "name": "xxx"}],
            "companies": [{"autodeskId": "xxx", "name": "xxx"}]
        },
        "modifier_info": {"autodeskId": "xxx", "name": "xxx"},
        "modification_reason": "修改原因"
    }
    """
    try:
        data = request.get_json()
        if not data or 'candidates' not in data:
            return jsonify({
                'success': False,
                'error': '請提供候選人配置數據'
            }), 400

        candidates = data['candidates']
        modifier_info = data.get('modifier_info', {})
        modification_reason = data.get('modification_reason', '候選人列表更新')

        conn = None
        try:
            conn = candidates_manager.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # 1. 驗證review和step存在且處於可修改狀態
            cursor.execute("""
                SELECT
                    r.status as review_status,
                    rp.status as step_status,
                    rp.step_name,
                    rsc.candidates as current_candidates
                FROM reviews r
                JOIN review_progress rp ON r.id = rp.review_id
                JOIN review_step_candidates rsc ON rp.review_id = rsc.review_id AND rp.step_id = rsc.step_id
                WHERE r.id = %s AND rp.step_id = %s AND rsc.is_active = true
                ORDER BY rp.created_at DESC LIMIT 1
            """, [review_id, step_id])

            result = cursor.fetchone()
            if not result:
                return jsonify({
                    'success': False,
                    'error': '找不到指定的review步驟'
                }), 404

            review_status = result['review_status']
            step_status = result['step_status']
            step_name = result['step_name']
            current_candidates = result['current_candidates']

            # 2. 檢查狀態是否允許修改候選人
            modifiable_review_statuses = ['DRAFT', 'IN_PROGRESS', 'PENDING', 'OPEN']
            modifiable_step_statuses = ['PENDING', 'CLAIMED']  # 等待審閱和開始審閱階段

            if review_status not in modifiable_review_statuses:
                return jsonify({
                    'success': False,
                    'error': f'Review狀態 {review_status} 不允許修改候選人'
                }), 400

            if step_status not in modifiable_step_statuses:
                return jsonify({
                    'success': False,
                    'error': f'步驟狀態 {step_status} 不允許修改候選人。只有PENDING或CLAIMED狀態可以修改。'
                }), 400

            # 3. 更新候選人配置
            standardized_candidates = candidates_manager._standardize_candidates(candidates)

            from datetime import datetime, timezone
            now = datetime.now(timezone.utc)

            cursor.execute("""
                UPDATE review_step_candidates
                SET
                    candidates = %s,
                    updated_at = %s
                WHERE review_id = %s AND step_id = %s AND is_active = true
                RETURNING id
            """, [
                json.dumps(standardized_candidates),
                now,
                review_id,
                step_id
            ])

            updated_record = cursor.fetchone()
            if not updated_record:
                return jsonify({
                    'success': False,
                    'error': '更新候選人配置失敗'
                }), 500

            # 4. 記錄修改歷史到workflow_notes
            cursor.execute("""
                INSERT INTO workflow_notes (
                    review_id, note_type, title, content,
                    created_by, is_visible_to_reviewers, is_visible_to_initiators,
                    is_internal_note, priority, created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
                RETURNING id
            """, [
                review_id,
                'candidate_update',
                f'候選人配置更新 - {step_name}',
                f'步驟候選人列表已更新。修改原因: {modification_reason}',
                json.dumps(modifier_info),
                True,  # 對審閱者可見
                True,  # 對發起者可見
                False,  # 不是內部備註
                3,     # 普通優先級
                now,
                now
            ])

            note_id = cursor.fetchone()['id']

            conn.commit()

            # 5. 計算變更統計
            if isinstance(current_candidates, str):
                current_candidates = json.loads(current_candidates)

            old_user_count = len(current_candidates.get('users', []))
            new_user_count = len(standardized_candidates.get('users', []))

            return jsonify({
                'success': True,
                'message': f'候選人配置已成功更新',
                'data': {
                    'review_id': review_id,
                    'step_id': step_id,
                    'step_name': step_name,
                    'step_status': step_status,
                    'updated_candidates': standardized_candidates,
                    'change_summary': {
                        'old_user_count': old_user_count,
                        'new_user_count': new_user_count,
                        'user_count_change': new_user_count - old_user_count
                    },
                    'modifier': modifier_info,
                    'modification_reason': modification_reason,
                    'note_id': note_id,
                    'updated_at': now.isoformat()
                }
            }), 200

        except Exception as e:
            if conn:
                conn.rollback()
            raise

        finally:
            if conn:
                conn.close()

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'動態修改候選人失敗: {str(e)}'
        }), 500

@candidates_bp.route('/api/candidates/reviews/<int:review_id>/steps/<step_id>', methods=['PUT'])
def update_step_candidates(review_id, step_id):
    """更新步骤候选人配置"""
    try:
        data = request.get_json()
        if not data or 'candidates' not in data:
            return jsonify({
                'success': False,
                'error': '请提供候选人配置数据'
            }), 400
        
        result = candidates_manager.update_step_candidates(review_id, step_id, data['candidates'])
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'更新候选人配置失败: {str(e)}'
        }), 500

@candidates_bp.route('/api/candidates/reviews/<int:review_id>/steps/<step_id>', methods=['DELETE'])
def delete_step_candidates(review_id, step_id):
    """删除步骤候选人配置"""
    result = candidates_manager.delete_step_candidates(review_id, step_id)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 404

@candidates_bp.route('/api/candidates/projects/<project_id>/available', methods=['GET'])
def get_available_candidates(project_id):
    """获取项目中所有可用的候选人"""
    result = candidates_manager.get_available_candidates(project_id)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 500

# ============================================================================
# 批量操作端点
# ============================================================================

@candidates_bp.route('/api/candidates/reviews/<int:review_id>/batch', methods=['POST'])
def batch_update_candidates(review_id):
    """批量更新评审的候选人配置"""
    try:
        data = request.get_json()
        if not data or 'steps' not in data:
            return jsonify({
                'success': False,
                'error': '请提供步骤配置数据'
            }), 400
        
        results = []
        for step_config in data['steps']:
            step_id = step_config.get('step_id')
            candidates = step_config.get('candidates', {})
            
            if not step_id:
                continue
                
            result = candidates_manager.update_step_candidates(review_id, step_id, candidates)
            results.append({
                'step_id': step_id,
                'success': result['success'],
                'message': result.get('message', result.get('error', ''))
            })
        
        return jsonify({
            'success': True,
            'message': f'批量更新完成，处理了 {len(results)} 个步骤',
            'results': results
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'批量更新失败: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("候选人管理 API 模块")
