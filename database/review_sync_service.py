# -*- coding: utf-8 -*-
"""
Review数据同步服务
处理Reviews API响应数据到数据库的同步
"""

import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from .data_access_layer import DataAccessLayer

logger = logging.getLogger(__name__)

class ReviewSyncService:
    """Review数据同步服务 - 最小侵入性设计"""
    
    def __init__(self):
        self.dal = DataAccessLayer()
    
    def sync_review_data(self, api_response_data: Dict[str, Any], api_endpoint: str, project_id: str = None):
        """
        根据API响应数据同步到数据库
        
        Args:
            api_response_data: API响应数据
            api_endpoint: API端点类型
            project_id: 项目ID
        """
        try:
            if 'reviews' in api_endpoint:
                self._sync_reviews_list(api_response_data, project_id)
            elif 'workflows' in api_endpoint:
                self._sync_workflows_list(api_response_data, project_id)
            elif 'versions' in api_endpoint:
                self._sync_review_versions(api_response_data, project_id)
            elif 'approval-statuses' in api_endpoint:
                self._sync_approval_history(api_response_data, project_id)
            elif 'progress' in api_endpoint:
                self._sync_review_progress(api_response_data, project_id)
                
        except Exception as e:
            logger.error(f"Review数据同步失败: {str(e)}")
    
    def _sync_reviews_list(self, reviews_data: Dict[str, Any], project_id: str):
        """同步Reviews列表数据"""
        try:
            reviews = reviews_data.get('reviews', [])
            logger.info(f"开始同步 {len(reviews)} 个Review记录到数据库")
            
            for review in reviews:
                self._upsert_review(review, project_id)
                
        except Exception as e:
            logger.error(f"同步Reviews列表失败: {str(e)}")
    
    def _sync_workflows_list(self, workflows_data: Dict[str, Any], project_id: str):
        """同步Workflows数据"""
        try:
            workflows = workflows_data.get('workflows', [])
            logger.info(f"开始同步 {len(workflows)} 个Workflow记录到数据库")
            
            for workflow in workflows:
                self._upsert_workflow(workflow, project_id)
                
        except Exception as e:
            logger.error(f"同步Workflows列表失败: {str(e)}")
    
    def _sync_review_versions(self, versions_data: Dict[str, Any], project_id: str):
        """同步Review文件版本数据"""
        try:
            versions = versions_data.get('versions', [])
            review_id = versions_data.get('review_id')
            
            logger.info(f"开始同步Review {review_id} 的 {len(versions)} 个文件版本")
            
            for version in versions:
                self._upsert_review_file_association(version, review_id, project_id)
                
        except Exception as e:
            logger.error(f"同步Review版本失败: {str(e)}")
    
    def _sync_approval_history(self, approval_data: Dict[str, Any], project_id: str):
        """同步审批历史数据"""
        try:
            approval_history = approval_data.get('approval_history', [])
            version_id = approval_data.get('version_id')
            
            logger.info(f"开始同步文件版本 {version_id} 的 {len(approval_history)} 条审批历史")
            
            for approval in approval_history:
                self._upsert_review_activity(approval, project_id, "FILE_APPROVAL")
                
        except Exception as e:
            logger.error(f"同步审批历史失败: {str(e)}")
    
    def _sync_review_progress(self, progress_data: Dict[str, Any], project_id: str):
        """同步Review进度数据"""
        try:
            progress_list = progress_data.get('progress', [])
            review_id = progress_data.get('review_id')
            
            logger.info(f"开始同步Review {review_id} 的 {len(progress_list)} 条进度记录")
            
            for progress in progress_list:
                self._upsert_review_activity(progress, project_id, "STEP_PROGRESS", review_id)
                
        except Exception as e:
            logger.error(f"同步Review进度失败: {str(e)}")
    
    def _upsert_review(self, review_data: Dict[str, Any], project_id: str):
        """插入或更新Review记录"""
        try:
            db = self.dal.connect()
            
            # 提取Review基本信息
            review_doc = {
                "_id": review_data.get("id"),
                "project_id": project_id,
                "sequence_id": review_data.get("sequence_id", 0),
                "name": review_data.get("name", ""),
                "status": review_data.get("status", ""),
                "workflow_id": review_data.get("workflow_id", ""),
                "current_step_id": review_data.get("current_step_id", ""),
                
                # 基本信息
                "metadata": {
                    "created_at": self._parse_datetime(review_data.get("created_at")),
                    "updated_at": self._parse_datetime(review_data.get("updated_at")),
                    "finished_at": self._parse_datetime(review_data.get("finished_at")),
                    "current_step_due_date": self._parse_datetime(review_data.get("current_step_due_date")),
                    "created_by": review_data.get("created_by", {}),
                    "archived": review_data.get("archived", False),
                    "archived_by": review_data.get("archived_by", {}),
                    "archived_at": self._parse_datetime(review_data.get("archived_at"))
                },
                
                # 当前审阅者信息
                "current_reviewers": {
                    "claimed_by": review_data.get("next_action_by", {}).get("claimed_by", []),
                    "candidates": review_data.get("next_action_by", {}).get("candidates", {})
                },
                
                # 工作流进度摘要
                "workflow_progress": review_data.get("workflow_progress", {}),
                
                # 索引优化字段
                "project_status": f"{project_id}#{review_data.get('status', '')}",
                "workflow_step": f"{review_data.get('workflow_id', '')}#{review_data.get('current_step_id', '')}",
                
                # 同步信息
                "synced_at": datetime.now(),
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
            
            # 使用upsert操作
            result = db.reviews.replace_one(
                {"_id": review_doc["_id"]},
                review_doc,
                upsert=True
            )
            
            logger.debug(f"Review {review_doc['_id']} {'更新' if result.matched_count > 0 else '创建'}成功")
            
        except Exception as e:
            logger.error(f"更新Review记录失败 {review_data.get('id', 'unknown')}: {str(e)}")
    
    def _upsert_workflow(self, workflow_data: Dict[str, Any], project_id: str):
        """插入或更新Workflow记录"""
        try:
            db = self.dal.connect()
            
            workflow_doc = {
                "_id": workflow_data.get("id"),
                "project_id": project_id,
                "name": workflow_data.get("name", ""),
                "description": workflow_data.get("description", ""),
                "status": workflow_data.get("status", "ACTIVE"),
                
                # 工作流步骤
                "steps": workflow_data.get("steps", []),
                
                # 审批状态选项
                "approval_status_options": workflow_data.get("approval_status_options", []),
                
                "metadata": {
                    "created_at": self._parse_datetime(workflow_data.get("created_at")),
                    "updated_at": self._parse_datetime(workflow_data.get("updated_at"))
                },
                
                # 同步信息
                "synced_at": datetime.now(),
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
            
            result = db.review_workflows.replace_one(
                {"_id": workflow_doc["_id"]},
                workflow_doc,
                upsert=True
            )
            
            logger.debug(f"Workflow {workflow_doc['_id']} {'更新' if result.matched_count > 0 else '创建'}成功")
            
        except Exception as e:
            logger.error(f"更新Workflow记录失败 {workflow_data.get('id', 'unknown')}: {str(e)}")
    
    def _upsert_review_file_association(self, version_data: Dict[str, Any], review_id: str, project_id: str):
        """插入或更新Review-文件关联记录"""
        try:
            db = self.dal.connect()
            
            file_urn = version_data.get("urn", "")
            file_version_urn = version_data.get("urn", "")
            
            association_doc = {
                "_id": f"{review_id}#{file_urn}",
                "review_id": review_id,
                "project_id": project_id,
                "file_urn": file_urn,
                "file_version_urn": file_version_urn,
                "file_name": version_data.get("name", ""),
                
                # 当前审批状态
                "current_approval_status": version_data.get("approve_status", {}),
                
                # 关联信息
                "association_metadata": {
                    "added_at": datetime.now(),
                    "is_primary_file": True
                },
                
                # 索引优化
                "review_file": f"{review_id}#{file_urn}",
                "project_file": f"{project_id}#{file_urn}",
                
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
            
            result = db.review_file_associations.replace_one(
                {"_id": association_doc["_id"]},
                association_doc,
                upsert=True
            )
            
            logger.debug(f"Review文件关联 {association_doc['_id']} {'更新' if result.matched_count > 0 else '创建'}成功")
            
        except Exception as e:
            logger.error(f"更新Review文件关联失败: {str(e)}")
    
    def _upsert_review_activity(self, activity_data: Dict[str, Any], project_id: str, 
                               activity_type: str, review_id: str = None):
        """插入Review活动记录"""
        try:
            db = self.dal.connect()
            
            # 获取下一个序列号
            if not review_id:
                review_id = activity_data.get("review_id", "")
            
            sequence_number = self._get_next_sequence_number(review_id)
            
            activity_doc = {
                "review_id": review_id,
                "project_id": project_id,
                "activity_type": activity_type,
                "sequence_number": sequence_number,
                
                # 执行者信息
                "action_by": self._extract_action_by(activity_data),
                
                # 时间信息
                "timestamps": {
                    "action_taken_at": self._parse_datetime(activity_data.get("end_time") or 
                                                          activity_data.get("approved_at") or 
                                                          activity_data.get("created_at")),
                    "created_at": datetime.now()
                },
                
                # 索引优化字段
                "review_sequence": f"{review_id}#{sequence_number:03d}",
                
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
            
            # 根据活动类型添加特定信息
            if activity_type == "STEP_PROGRESS":
                activity_doc["step_info"] = {
                    "step_id": activity_data.get("step_id", ""),
                    "step_name": activity_data.get("step_name", ""),
                    "step_status": activity_data.get("status", ""),
                    "action_type": self._determine_action_type(activity_data)
                }
                activity_doc["candidates"] = activity_data.get("candidates", {})
                activity_doc["activity_summary"] = self._generate_step_activity_summary(activity_data)
                
            elif activity_type == "FILE_APPROVAL":
                activity_doc["file_info"] = {
                    "file_urn": activity_data.get("file_urn", ""),
                    "file_version_urn": activity_data.get("version_urn", ""),
                    "file_name": activity_data.get("file_name", ""),
                    "approval_status": activity_data.get("approval_status", {})
                }
                activity_doc["activity_summary"] = self._generate_file_activity_summary(activity_data)
            
            # 插入活动记录
            db.review_activities.insert_one(activity_doc)
            logger.debug(f"Review活动记录创建成功: {activity_type} for {review_id}")
            
        except Exception as e:
            logger.error(f"创建Review活动记录失败: {str(e)}")
    
    def _get_next_sequence_number(self, review_id: str) -> int:
        """获取Review的下一个序列号"""
        try:
            db = self.dal.connect()
            
            # 查找该Review的最大序列号
            last_activity = db.review_activities.find_one(
                {"review_id": review_id},
                sort=[("sequence_number", -1)]
            )
            
            if last_activity:
                return last_activity["sequence_number"] + 1
            else:
                return 1
                
        except Exception as e:
            logger.error(f"获取序列号失败: {str(e)}")
            return 1
    
    def _extract_action_by(self, activity_data: Dict[str, Any]) -> Dict[str, Any]:
        """提取执行者信息"""
        action_by = {}
        
        # 尝试从不同字段提取用户信息
        user_info = (activity_data.get("action_by") or 
                     activity_data.get("claimed_by") or 
                     activity_data.get("approved_by") or 
                     activity_data.get("created_by"))
        
        if user_info:
            if isinstance(user_info, list) and len(user_info) > 0:
                user_info = user_info[0]
            
            if isinstance(user_info, dict):
                action_by = {
                    "user_id": user_info.get("id", ""),
                    "name": user_info.get("name", ""),
                    "email": user_info.get("email", ""),
                    "role": user_info.get("role", "")
                }
        
        return action_by
    
    def _determine_action_type(self, activity_data: Dict[str, Any]) -> str:
        """确定操作类型"""
        status = activity_data.get("status", "").upper()
        
        if status == "CLAIMED":
            return "CLAIM"
        elif status == "SUBMITTED":
            return "SUBMIT"
        elif status in ["APPROVED", "COMPLETED"]:
            return "APPROVE"
        elif status == "REJECTED":
            return "REJECT"
        else:
            return "UNKNOWN"
    
    def _generate_step_activity_summary(self, activity_data: Dict[str, Any]) -> str:
        """生成步骤活动摘要"""
        action_by = self._extract_action_by(activity_data)
        step_name = activity_data.get("step_name", "Unknown Step")
        action_type = self._determine_action_type(activity_data)
        user_name = action_by.get("name", "Unknown User")
        
        action_map = {
            "CLAIM": "claimed",
            "SUBMIT": "submitted",
            "APPROVE": "approved",
            "REJECT": "rejected"
        }
        
        action_text = action_map.get(action_type, "processed")
        return f"{user_name} {action_text} {step_name} step"
    
    def _generate_file_activity_summary(self, activity_data: Dict[str, Any]) -> str:
        """生成文件活动摘要"""
        action_by = self._extract_action_by(activity_data)
        file_name = activity_data.get("file_name", "Unknown File")
        approval_status = activity_data.get("approval_status", {})
        user_name = action_by.get("name", "Unknown User")
        status_label = approval_status.get("label", "processed")
        
        return f"{user_name} {status_label.lower()} {file_name}"
    
    def _parse_datetime(self, date_string: str) -> Optional[datetime]:
        """解析日期时间字符串"""
        if not date_string:
            return None
        
        try:
            # 尝试不同的日期格式
            formats = [
                "%Y-%m-%dT%H:%M:%S.%fZ",
                "%Y-%m-%dT%H:%M:%SZ",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d %H:%M:%S"
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(date_string, fmt)
                except ValueError:
                    continue
            
            # 如果都失败了，返回None
            logger.warning(f"无法解析日期格式: {date_string}")
            return None
            
        except Exception as e:
            logger.error(f"解析日期时间失败: {str(e)}")
            return None


# 全局服务实例
review_sync_service = ReviewSyncService()
