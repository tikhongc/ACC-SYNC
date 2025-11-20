# -*- coding: utf-8 -*-
"""
文件审批状态管理API模块
实现文件审批状态管理和历史记录功能
"""

import json
from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from typing import Dict, List, Optional, Any
import utils

# 添加数据库访问
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../database_sql'))
from neon_config import NeonConfig
import psycopg2
import psycopg2.extras

approval_status_bp = Blueprint('approval_status', __name__)

class ApprovalStatusManager:
    """审批状态管理器"""
    
    def __init__(self):
        """初始化审批状态管理器"""
        self.neon_config = NeonConfig()
        self.db_params = self.neon_config.get_db_params()
    
    def get_connection(self):
        """获取数据库连接"""
        return psycopg2.connect(**self.db_params)
    
    def update_file_approval_status(
        self, 
        file_version_id: int, 
        approval_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        更新文件审批状态
        
        Args:
            file_version_id: 文件版本ID
            approval_data: 审批数据
            {
                "approval_status": "APPROVED" | "REJECTED" | "PENDING",
                "approval_comments": "审批评论",
                "approved_by": {"autodeskId": "xxx", "name": "xxx"},
                "conditions": "审批条件",
                "review_id": 123,
                "step_id": "step_1"
            }
            
        Returns:
            更新结果
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # 检查文件版本是否存在并获取文件信息
            cursor.execute("""
                SELECT rfv.file_version_urn, rfv.review_id, f.name
                FROM review_file_versions rfv
                LEFT JOIN file_versions fv ON rfv.file_version_urn = fv.urn
                LEFT JOIN files f ON fv.file_id = f.id
                WHERE rfv.id = %s
            """, [file_version_id])

            result = cursor.fetchone()
            if not result:
                raise ValueError("文件版本不存在")

            file_version_urn, review_id, file_name = result
            
            now = datetime.now(timezone.utc)
            approval_status = approval_data.get('approval_status')
            approved_by = approval_data.get('approved_by', {})
            
            # 更新文件版本审批状态
            cursor.execute("""
                UPDATE review_file_versions 
                SET approval_status = %s,
                    approval_comments = %s,
                    approved_at = %s,
                    updated_at = %s
                WHERE id = %s
            """, [
                approval_status,
                approval_data.get('approval_comments'),
                now if approval_status in ['APPROVED', 'REJECTED'] else None,
                now,
                file_version_id
            ])
            
            # 创建审批历史记录
            self._create_approval_history(
                cursor, file_version_urn, file_name, review_id, approval_data, now
            )
            
            conn.commit()
            
            return {
                'file_version_id': file_version_id,
                'approval_status': approval_status,
                'status': 'updated'
            }
            
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"✗ 更新文件审批状态失败: {str(e)}")
            raise
            
        finally:
            if conn:
                conn.close()
    
    def _create_approval_history(
        self, 
        cursor, 
        file_urn: str, 
        file_name: str, 
        review_id: int,
        approval_data: Dict,
        timestamp: datetime
    ):
        """创建审批历史记录"""
        # 获取评审信息
        cursor.execute("""
            SELECT review_uuid, name, status FROM reviews WHERE id = %s
        """, [review_id])
        
        review_info = cursor.fetchone()
        if not review_info:
            return
        
        review_uuid, review_name, review_status = review_info
        
        # 插入审批历史
        cursor.execute("""
            INSERT INTO file_approval_history (
                file_version_urn, file_name, review_id, review_acc_id,
                review_name, review_status, approval_status_value,
                approval_status_label, approval_status_type,
                approved_by, approved_at, is_current, is_latest_in_review,
                created_at, synced_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """, [
            file_urn,
            file_name,
            review_id,
            review_uuid,
            review_name,
            review_status,
            approval_data.get('approval_status'),
            approval_data.get('approval_status', '').title(),
            'manual',  # 手动审批
            json.dumps(approval_data.get('approved_by', {})),
            timestamp,
            True,  # 当前状态
            True,  # 评审中最新状态
            timestamp,
            timestamp
        ])
        
        # 将之前的记录标记为非当前状态
        cursor.execute("""
            UPDATE file_approval_history 
            SET is_current = false, is_latest_in_review = false
            WHERE file_version_urn = %s AND review_id = %s AND id != (
                SELECT id FROM file_approval_history 
                WHERE file_version_urn = %s AND review_id = %s 
                ORDER BY created_at DESC LIMIT 1
            )
        """, [file_urn, review_id, file_urn, review_id])
    
    def batch_update_file_approvals(
        self, 
        review_id: int, 
        batch_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        批量更新文件审批状态
        
        Args:
            review_id: 评审ID
            batch_data: 批量数据
            {
                "approval_status": "APPROVED",
                "approval_comments": "批量审批",
                "approved_by": {"autodeskId": "xxx", "name": "xxx"},
                "file_version_ids": [1, 2, 3],
                "step_id": "step_1"
            }
            
        Returns:
            批量更新结果
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            file_version_ids = batch_data.get('file_version_ids', [])
            if not file_version_ids:
                raise ValueError("未指定文件版本")
            
            stats = {
                'total_files': len(file_version_ids),
                'updated_files': 0,
                'errors': []
            }
            
            # 批量更新每个文件
            for file_version_id in file_version_ids:
                try:
                    # 复制批量数据用于单个文件
                    file_approval_data = batch_data.copy()
                    file_approval_data['review_id'] = review_id
                    
                    # 更新单个文件（不提交事务）
                    self._update_single_file_approval(cursor, file_version_id, file_approval_data)
                    stats['updated_files'] += 1
                    
                except Exception as e:
                    error_msg = f"文件 {file_version_id} 更新失败: {str(e)}"
                    stats['errors'].append(error_msg)
                    print(f"✗ {error_msg}")
            
            conn.commit()
            
            return {
                'review_id': review_id,
                'batch_approval_status': batch_data.get('approval_status'),
                'statistics': stats
            }
            
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"✗ 批量更新文件审批失败: {str(e)}")
            raise
            
        finally:
            if conn:
                conn.close()
    
    def _update_single_file_approval(self, cursor, file_version_id: int, approval_data: Dict):
        """更新单个文件审批状态（内部方法，不提交事务）"""
        # 检查文件版本并获取文件信息
        cursor.execute("""
            SELECT rfv.file_version_urn, rfv.review_id, f.name
            FROM review_file_versions rfv
            LEFT JOIN file_versions fv ON rfv.file_version_urn = fv.urn
            LEFT JOIN files f ON fv.file_id = f.id
            WHERE rfv.id = %s
        """, [file_version_id])

        result = cursor.fetchone()
        if not result:
            raise ValueError(f"文件版本 {file_version_id} 不存在")

        file_version_urn, review_id, file_name = result
        
        now = datetime.now(timezone.utc)
        approval_status = approval_data.get('approval_status')
        
        # 更新文件版本
        cursor.execute("""
            UPDATE review_file_versions 
            SET approval_status = %s,
                approval_comments = %s,
                approved_at = %s,
                updated_at = %s
            WHERE id = %s
        """, [
            approval_status,
            approval_data.get('approval_comments'),
            now if approval_status in ['APPROVED', 'REJECTED'] else None,
            now,
            file_version_id
        ])
        
        # 创建审批历史
        self._create_approval_history(
            cursor, file_version_urn, file_name, review_id, approval_data, now
        )
    
    def get_file_approval_history(
        self, 
        file_urn: str = None, 
        review_id: int = None,
        limit: int = 50
    ) -> List[Dict]:
        """
        获取文件审批历史
        
        Args:
            file_urn: 文件URN（可选）
            review_id: 评审ID（可选）
            limit: 限制数量
            
        Returns:
            审批历史列表
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # 构建查询条件
            where_conditions = []
            params = []
            
            if file_urn:
                where_conditions.append("file_version_urn = %s")
                params.append(file_urn)
            
            if review_id:
                where_conditions.append("review_id = %s")
                params.append(review_id)
            
            where_clause = ""
            if where_conditions:
                where_clause = f"WHERE {' AND '.join(where_conditions)}"
            
            params.append(limit)
            
            cursor.execute(f"""
                SELECT * FROM file_approval_history 
                {where_clause}
                ORDER BY created_at DESC
                LIMIT %s
            """, params)
            
            history = []
            for record in cursor.fetchall():
                record_dict = dict(record)
                
                # 解析JSON字段
                if record_dict.get('approved_by'):
                    try:
                        record_dict['approved_by'] = json.loads(record_dict['approved_by'])
                    except:
                        record_dict['approved_by'] = {}
                
                history.append(record_dict)
            
            return history
            
        except Exception as e:
            print(f"✗ 获取文件审批历史失败: {str(e)}")
            return []
            
        finally:
            if conn:
                conn.close()
    
    def get_review_file_statuses(self, review_id: int) -> Dict[str, Any]:
        """
        获取评审文件状态统计
        
        Args:
            review_id: 评审ID
            
        Returns:
            文件状态统计
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            # 获取文件状态统计
            cursor.execute("""
                SELECT 
                    approval_status,
                    COUNT(*) as count
                FROM review_file_versions 
                WHERE review_id = %s
                GROUP BY approval_status
            """, [review_id])
            
            status_counts = {row['approval_status']: row['count'] for row in cursor.fetchall()}
            
            # 获取文件详情
            cursor.execute("""
                SELECT
                    id,
                    file_version_urn,
                    approval_status,
                    approval_comments,
                    approved_at,
                    updated_at
                FROM review_file_versions
                WHERE review_id = %s
                ORDER BY id
            """, [review_id])
            
            files = [dict(file) for file in cursor.fetchall()]
            
            # 计算总体统计
            total_files = len(files)
            approved_files = status_counts.get('APPROVED', 0)
            rejected_files = status_counts.get('REJECTED', 0)
            pending_files = status_counts.get('PENDING', 0)
            
            approval_rate = (approved_files / total_files * 100) if total_files > 0 else 0
            
            return {
                'review_id': review_id,
                'total_files': total_files,
                'status_counts': status_counts,
                'approval_rate': round(approval_rate, 2),
                'files': files,
                'summary': {
                    'approved': approved_files,
                    'rejected': rejected_files,
                    'pending': pending_files,
                    'completion_rate': round((approved_files + rejected_files) / total_files * 100, 2) if total_files > 0 else 0
                }
            }
            
        except Exception as e:
            print(f"✗ 获取评审文件状态失败: {str(e)}")
            return {
                'review_id': review_id,
                'total_files': 0,
                'status_counts': {},
                'approval_rate': 0,
                'files': [],
                'summary': {'approved': 0, 'rejected': 0, 'pending': 0, 'completion_rate': 0}
            }
            
        finally:
            if conn:
                conn.close()
    
    def get_file_approval_timeline(self, file_urn: str) -> List[Dict]:
        """
        获取文件审批时间线
        
        Args:
            file_urn: 文件URN
            
        Returns:
            审批时间线
        """
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            cursor.execute("""
                SELECT 
                    fah.*,
                    r.name as review_name,
                    r.status as review_status
                FROM file_approval_history fah
                LEFT JOIN reviews r ON fah.review_id = r.id
                WHERE fah.file_version_urn = %s
                ORDER BY fah.created_at ASC
            """, [file_urn])
            
            timeline = []
            for record in cursor.fetchall():
                record_dict = dict(record)
                
                # 解析JSON字段
                if record_dict.get('approved_by'):
                    try:
                        record_dict['approved_by'] = json.loads(record_dict['approved_by'])
                    except:
                        record_dict['approved_by'] = {}
                
                timeline.append(record_dict)
            
            return timeline
            
        except Exception as e:
            print(f"✗ 获取文件审批时间线失败: {str(e)}")
            return []
            
        finally:
            if conn:
                conn.close()

# 创建全局实例
approval_manager = ApprovalStatusManager()

@approval_status_bp.route('/api/approval-status/file-versions/<int:file_version_id>/approve', methods=['POST'])
def update_file_approval(file_version_id):
    """
    更新文件审批状态
    """
    try:
        data = request.get_json()
        
        if not data.get('approval_status'):
            return jsonify({
                "error": "缺少审批状态",
                "status": "bad_request"
            }), 400
        
        if not data.get('approved_by'):
            return jsonify({
                "error": "缺少审批人信息",
                "status": "bad_request"
            }), 400
        
        result = approval_manager.update_file_approval_status(file_version_id, data)
        
        return jsonify({
            "status": "success",
            "message": "文件审批状态更新成功",
            "data": result
        })
        
    except Exception as e:
        print(f"✗ 更新文件审批状态失败: {str(e)}")
        return jsonify({
            "error": f"更新文件审批状态失败: {str(e)}",
            "status": "error"
        }), 500

@approval_status_bp.route('/api/approval-status/reviews/<int:review_id>/batch-approve', methods=['POST'])
def batch_approve_files(review_id):
    """
    批量审批文件
    """
    try:
        data = request.get_json()
        
        if not data.get('approval_status'):
            return jsonify({
                "error": "缺少审批状态",
                "status": "bad_request"
            }), 400
        
        if not data.get('file_version_ids'):
            return jsonify({
                "error": "缺少文件版本ID列表",
                "status": "bad_request"
            }), 400
        
        if not data.get('approved_by'):
            return jsonify({
                "error": "缺少审批人信息",
                "status": "bad_request"
            }), 400
        
        result = approval_manager.batch_update_file_approvals(review_id, data)
        
        return jsonify({
            "status": "success",
            "message": "批量审批完成",
            "data": result
        })
        
    except Exception as e:
        print(f"✗ 批量审批失败: {str(e)}")
        return jsonify({
            "error": f"批量审批失败: {str(e)}",
            "status": "error"
        }), 500

@approval_status_bp.route('/api/approval-status/history')
def get_approval_history():
    """
    获取审批历史
    """
    try:
        file_urn = request.args.get('file_urn')
        review_id = request.args.get('review_id', type=int)
        limit = request.args.get('limit', 50, type=int)
        
        history = approval_manager.get_file_approval_history(file_urn, review_id, limit)
        
        return jsonify({
            "status": "success",
            "data": {
                "file_urn": file_urn,
                "review_id": review_id,
                "history": history,
                "total_records": len(history)
            }
        })
        
    except Exception as e:
        print(f"✗ 获取审批历史失败: {str(e)}")
        return jsonify({
            "error": f"获取审批历史失败: {str(e)}",
            "status": "error"
        }), 500

@approval_status_bp.route('/api/approval-status/reviews/<int:review_id>/file-statuses')
def get_review_file_statuses(review_id):
    """
    获取评审文件状态统计
    """
    try:
        result = approval_manager.get_review_file_statuses(review_id)
        
        return jsonify({
            "status": "success",
            "data": result
        })
        
    except Exception as e:
        print(f"✗ 获取评审文件状态失败: {str(e)}")
        return jsonify({
            "error": f"获取评审文件状态失败: {str(e)}",
            "status": "error"
        }), 500

@approval_status_bp.route('/api/approval-status/files/<path:file_urn>/timeline')
def get_file_timeline(file_urn):
    """
    获取文件审批时间线
    """
    try:
        timeline = approval_manager.get_file_approval_timeline(file_urn)
        
        return jsonify({
            "status": "success",
            "data": {
                "file_urn": file_urn,
                "timeline": timeline,
                "total_events": len(timeline)
            }
        })
        
    except Exception as e:
        print(f"✗ 获取文件审批时间线失败: {str(e)}")
        return jsonify({
            "error": f"获取文件审批时间线失败: {str(e)}",
            "status": "error"
        }), 500
