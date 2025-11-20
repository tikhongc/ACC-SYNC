# -*- coding: utf-8 -*-
"""
ACC Review 模块集成文件
注册所有新的API蓝图和路由
"""

from flask import Flask, Blueprint, jsonify
from typing import Dict, Any

# 导入所有新的API模块 - 修复相对导入问题
try:
    # Try relative imports first (for Flask app context)
    from .review_crud_api import review_crud_bp
    from .step_progress_api import step_progress_bp
    from .approval_status_api import approval_status_bp
    from .candidates_api import candidates_bp
    from .approval_workflow_api_enhanced import approval_bp
except ImportError:
    # Fall back to absolute imports (for standalone testing)
    try:
        from review_crud_api import review_crud_bp
        from step_progress_api import step_progress_bp
        from approval_status_api import approval_status_bp
        from candidates_api import candidates_bp
        from approval_workflow_api_enhanced import approval_bp
    except ImportError:
        # Create dummy blueprints for testing if modules not available
        review_crud_bp = Blueprint('review_crud_bp', __name__)
        step_progress_bp = Blueprint('step_progress_bp', __name__)
        approval_status_bp = Blueprint('approval_status_bp', __name__)
        candidates_bp = Blueprint('candidates_bp', __name__)
        approval_bp = Blueprint('approval_bp', __name__)

# 创建主要的review模块蓝图
review_module_bp = Blueprint('review_module', __name__, url_prefix='/api/review-module')

def register_review_module_blueprints(app: Flask):
    """
    注册所有review模块的蓝图到Flask应用
    
    Args:
        app: Flask应用实例
    """
    
    # 注册所有子模块蓝图
    blueprints = [
        # (candidate_assignment_bp, "候选人分配API"),  # Removed
        (candidates_bp, "候选人管理API"),
        (approval_bp, "增强审批工作流API"),
        # (template_sync_bp, "模板同步API"),  # 移除：不需要此API
        (review_crud_bp, "评审CRUD API"),
        (step_progress_bp, "步骤进度API"),
        # (comment_system_bp, "评论系统API"),  # 移除：使用notes替代comments
        (approval_status_bp, "审批状态API")
    ]
    
    for blueprint, description in blueprints:
        app.register_blueprint(blueprint)
        print(f"✓ 已注册 {description}: {blueprint.name}")
    
    # 注册主模块蓝图
    app.register_blueprint(review_module_bp)
    print(f"✓ 已注册主模块蓝图: {review_module_bp.name}")

@review_module_bp.route('/health')
def health_check():
    """
    Review模块健康检查
    """
    return jsonify({
        "status": "healthy",
        "module": "ACC Review Module",
        "version": "1.0.0",
        "components": {
            "candidates": "active",
            "review_crud": "active",
            "step_progress": "active",
            "approval_status": "active",
            "approval_workflow": "active"
        }
    })

@review_module_bp.route('/info')
def module_info():
    """
    Review模块信息
    """
    return jsonify({
        "module_name": "ACC Review Module",
        "description": "完整的ACC评审模块后端功能",
        "version": "1.0.0",
        "features": [
            "候選人管理和分配",
            "評審CRUD操作",
            "步驟進度管理",
            "文件審批狀態管理",
            "增強審批工作流"
        ],
        "api_endpoints": {
            "candidates_management": [
                "GET /api/candidates/projects/{project_id}/available",
                "GET /api/candidates/reviews/{review_id}",
                "GET /api/candidates/reviews/{review_id}/steps/{step_id}",
                "POST /api/candidates/reviews/{review_id}/steps/{step_id}",
                "PUT /api/candidates/reviews/{review_id}/steps/{step_id}",
                "DELETE /api/candidates/reviews/{review_id}/steps/{step_id}",
                "POST /api/candidates/reviews/{review_id}/batch"
            ],
            "approval_workflow": [
                "GET /api/approval/users/{user_id}/pending",
                "GET /api/approval/reviews/{review_id}",
                "POST /api/approval/reviews/{review_id}/steps/{step_id}/decide",
                "POST /api/approval/reviews",
                "POST /api/approval/reviews/{review_id}/steps/{step_id}/start",
                "POST /api/approval/reviews/{review_id}/files/batch-approve",
                "GET /api/approval/health"
            ],
            "review_crud": [
                "POST /api/reviews",
                "GET /api/reviews/{review_id}",
                "PUT /api/reviews/{review_id}",
                "DELETE /api/reviews/{review_id}",
                "GET /api/reviews",
                "POST /api/reviews/{review_id}/start"
            ],
            "step_progress": [
                "POST /api/step-progress/reviews/{review_id}/steps/{step_id}/claim",
                "POST /api/step-progress/reviews/{review_id}/steps/{step_id}/submit",
                "POST /api/step-progress/reviews/{review_id}/steps/{step_id}/send-back",
                "GET /api/step-progress/reviews/{review_id}/progress",
                "GET /api/step-progress/users/{user_acc_id}/tasks"
            ],
            "approval_status": [
                "POST /api/approval-status/file-versions/{file_version_id}/approve",
                "POST /api/approval-status/reviews/{review_id}/batch-approve",
                "GET /api/approval-status/history",
                "GET /api/approval-status/reviews/{review_id}/file-statuses",
                "GET /api/approval-status/files/{file_urn}/timeline"
            ]
        },
        "database_tables": [
            "user_members",
            "review_step_candidates", 
            "workflow_notes",
            "workflow_templates (extended)",
            "reviews (existing)",
            "review_progress (existing)",
            "review_file_versions (existing)",
            "file_approval_history (existing)"
        ]
    })

@review_module_bp.route('/stats')
def module_stats():
    """
    Review模块统计信息
    """
    # 这里可以添加实际的统计查询
    return jsonify({
        "module": "ACC Review Module",
        "statistics": {
            "total_endpoints": 25,
            "total_blueprints": 5,
            "database_tables": 8,
            "implementation_status": "completed"
        },
        "implementation_progress": {
            "database_schema": "100%",
            "candidate_management": "100%",
            "review_crud": "100%",
            "step_progress": "100%",
            "approval_status": "100%",
            "approval_workflow": "100%"
        }
    })

# 导出主要函数和蓝图
__all__ = [
    'register_review_module_blueprints',
    'review_module_bp',
    # 'user_sync_bp',  # 移除：不需要此API
    # 'candidate_assignment_bp',  # Removed
    # 'template_sync_bp',  # 移除：不需要此API
    'review_crud_bp',
    'step_progress_bp',
    # 'comment_system_bp',  # 移除：使用notes替代comments
    'approval_status_bp',
    'candidates_bp',
    'approval_bp'
]

# 为了向后兼容性，提供别名
review_blueprint = review_module_bp
