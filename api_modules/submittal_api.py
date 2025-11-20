"""
Autodesk Construction Cloud - Submittal API Module

This module provides comprehensive access to the Submittal API endpoints,
allowing management of submittal items, review workflows, and related resources.

API Documentation: https://aps.autodesk.com/en/docs/acc/v1/reference/http/submittals/
"""

import requests
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class SubmittalAPI:
    """
    Submittal API client for Autodesk Construction Cloud.
    
    This class provides methods to interact with submittal items, review workflows,
    attachments, and all related resources in ACC projects.
    """
    
    def __init__(self, access_token: str, base_url: str = "https://developer.api.autodesk.com"):
        """
        Initialize the Submittal API client.
        
        Args:
            access_token: OAuth 2.0 access token (three-legged)
            base_url: Base URL for the API (default: Autodesk API endpoint)
        """
        self.access_token = access_token
        self.base_url = base_url
        self.submittal_base = f"{base_url}/construction/submittals/v2"
        
    def _get_headers(self) -> Dict[str, str]:
        """Get standard headers for API requests."""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Make an HTTP request with error handling.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            url: Full URL for the request
            **kwargs: Additional arguments passed to requests
            
        Returns:
            Response object
            
        Raises:
            requests.exceptions.RequestException: If request fails
        """
        try:
            response = requests.request(method, url, headers=self._get_headers(), **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {method} {url} - {str(e)}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response: {e.response.text}")
            raise
    
    # ========================================================================
    # Items API
    # ========================================================================
    
    def get_items(self, project_id: str, **params) -> Dict[str, Any]:
        """
        Retrieve all submittal items in a project.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            **params: Optional query parameters:
                - limit: Max results per page (1-50, default: 20)
                - offset: Number of results to skip
                - sort: Sort by fields (e.g., "createdAt desc")
                - search: Search string
                - filter[title]: Filter by title
                - filter[statusId]: Filter by status ID
                - filter[specId]: Filter by spec ID
                - filter[ballInCourtUsers]: Filter by user ID
                - filter[ballInCourtCompanies]: Filter by company ID
                - filter[responseId]: Filter by response ID
                - filter[typeId]: Filter by type ID
                - filter[packageId]: Filter by package ID
                - filter[stateId]: Filter by state ID
                - filter[identifier]: Filter by submittal item ID
                - filter[revision]: Filter by revision number
                - filter[manager]: Filter by manager Autodesk ID
                - filter[subcontractor]: Filter by subcontractor ID
                - filter[createdBy]: Filter by creator ID
                - filter[watchers]: Filter by watcher ID
                - filter[dueDate]: Filter by due date (YYYY-MM-DD)
                - filter[createdAt]: Filter by creation date
                - filter[updatedAt]: Filter by update date
                
        Returns:
            Dictionary containing:
                - results: List of submittal items
                - pagination: Pagination information
                
        Example:
            >>> items = api.get_items(project_id, limit=50, filter={'statusId': '2'})
        """
        url = f"{self.submittal_base}/projects/{project_id}/items"
        response = self._make_request("GET", url, params=params)
        return response.json()
    
    def get_item(self, project_id: str, item_id: str) -> Dict[str, Any]:
        """
        Retrieve a single submittal item by ID.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            item_id: Submittal item ID (UUID)
            
        Returns:
            Dictionary containing submittal item details
            
        Example:
            >>> item = api.get_item(project_id, item_id)
            >>> print(item['title'])
        """
        url = f"{self.submittal_base}/projects/{project_id}/items/{item_id}"
        response = self._make_request("GET", url)
        return response.json()
    
    def get_item_revisions(self, project_id: str, item_id: str, **params) -> Dict[str, Any]:
        """
        Retrieve revision history of a submittal item.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            item_id: Submittal item ID (UUID)
            **params: Optional query parameters:
                - limit: Max results per page (1-50, default: 20)
                - offset: Number of results to skip
                
        Returns:
            Dictionary containing:
                - results: List of item revisions
                - pagination: Pagination information
                
        Example:
            >>> revisions = api.get_item_revisions(project_id, item_id)
        """
        url = f"{self.submittal_base}/projects/{project_id}/items/{item_id}/revisions"
        response = self._make_request("GET", url, params=params)
        return response.json()
    
    def get_attachments(self, project_id: str, item_id: str, **params) -> Dict[str, Any]:
        """
        Retrieve attachments associated with a submittal item.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            item_id: Submittal item ID (UUID)
            **params: Optional query parameters:
                - limit: Max results per page (1-50, default: 20)
                - offset: Number of results to skip
                - sort: Sort by fields
                - filter[categoryId]: Filter by category ID
                - filter[revision]: Filter by revision number
                - filter[isFileUploaded]: Filter by upload status ('true'/'false')
                
        Returns:
            Dictionary containing:
                - results: List of attachments
                - pagination: Pagination information
                
        Example:
            >>> attachments = api.get_attachments(project_id, item_id)
        """
        url = f"{self.submittal_base}/projects/{project_id}/items/{item_id}/attachments"
        response = self._make_request("GET", url, params=params)
        return response.json()
    
    def validate_custom_identifier(self, project_id: str, custom_identifier: str, 
                                   spec_id: Optional[str] = None) -> bool:
        """
        Validate a custom identifier for a submittal item.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            custom_identifier: Custom identifier to validate
            spec_id: Spec ID (required for spec sequence projects)
            
        Returns:
            True if identifier is valid (HTTP 204)
            
        Raises:
            requests.exceptions.HTTPError: If identifier is invalid (HTTP 409) or other error
            
        Example:
            >>> is_valid = api.validate_custom_identifier(project_id, "A-111")
        """
        url = f"{self.submittal_base}/projects/{project_id}/items:validate-custom-identifier"
        params = {}
        if spec_id:
            params['specId'] = spec_id
        
        data = {"customIdentifier": custom_identifier}
        response = self._make_request("POST", url, params=params, json=data)
        return response.status_code == 204
    
    def get_next_custom_identifier(self, project_id: str, spec_id: Optional[str] = None) -> Dict[str, str]:
        """
        Get the next available custom identifier for a submittal item.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            spec_id: Spec ID (required for spec sequence projects)
            
        Returns:
            Dictionary containing:
                - previousCustomIdentifier: Last created identifier
                - nextCustomIdentifier: Next available identifier
                
        Example:
            >>> identifiers = api.get_next_custom_identifier(project_id)
            >>> print(identifiers['nextCustomIdentifier'])
        """
        url = f"{self.submittal_base}/projects/{project_id}/items:next-custom-identifier"
        params = {}
        if spec_id:
            params['specId'] = spec_id
        
        response = self._make_request("GET", url, params=params)
        return response.json()
    
    # ========================================================================
    # Item Types API
    # ========================================================================
    
    def get_item_types(self, project_id: str, **params) -> Dict[str, Any]:
        """
        Retrieve all submittal item types for a project.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            **params: Optional query parameters:
                - limit: Max results per page (1-50, default: 20)
                - offset: Number of results to skip
                
        Returns:
            Dictionary containing:
                - results: List of item types
                - pagination: Pagination information
                
        Example:
            >>> types = api.get_item_types(project_id)
        """
        url = f"{self.submittal_base}/projects/{project_id}/item-types"
        response = self._make_request("GET", url, params=params)
        return response.json()
    
    def get_item_type(self, project_id: str, type_id: str) -> Dict[str, Any]:
        """
        Retrieve a single submittal item type by ID.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            type_id: Item type ID (UUID)
            
        Returns:
            Dictionary containing item type details
            
        Example:
            >>> item_type = api.get_item_type(project_id, type_id)
        """
        url = f"{self.submittal_base}/projects/{project_id}/item-types/{type_id}"
        response = self._make_request("GET", url)
        return response.json()
    
    # ========================================================================
    # Metadata API
    # ========================================================================
    
    def get_metadata(self, project_id: str) -> Dict[str, Any]:
        """
        Retrieve project metadata and static values for submittals.
        
        This includes submittal roles, user types, statuses, responses,
        and project-specific information like custom identifier sequence type.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            
        Returns:
            Dictionary containing:
                - submittalRoles: List of submittal roles
                - attachmentUrnTypes: List of attachment URN types
                - itemTypes: List of submittal item types
                - userTypes: Types of users
                - statuses: List of statuses
                - responses: List of responses
                - attachmentCategories: List of attachment categories
                - customIdentifierSequenceType: Sequence type (1=Global, 2=Spec)
                - and more...
                
        Example:
            >>> metadata = api.get_metadata(project_id)
            >>> sequence_type = metadata['customIdentifierSequenceType']
        """
        url = f"{self.submittal_base}/projects/{project_id}/metadata"
        response = self._make_request("GET", url)
        return response.json()
    
    # ========================================================================
    # Packages API
    # ========================================================================
    
    def get_packages(self, project_id: str, **params) -> Dict[str, Any]:
        """
        Retrieve all packages for a project.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            **params: Optional query parameters:
                - limit: Max results per page (1-50, default: 20)
                - offset: Number of results to skip
                - sort: Sort by fields (e.g., "spec asc")
                - filter[identifier]: Filter by package ID
                - filter[title]: Filter by title
                - filter[specId]: Filter by spec ID (UUID)
                - filter[spec.identifier]: Filter by spec section ID
                - search: Search string
                
        Returns:
            Dictionary containing:
                - results: List of packages
                - pagination: Pagination information
                
        Example:
            >>> packages = api.get_packages(project_id, search="Electrical")
        """
        url = f"{self.submittal_base}/projects/{project_id}/packages"
        response = self._make_request("GET", url, params=params)
        return response.json()
    
    def get_package(self, project_id: str, package_id: str) -> Dict[str, Any]:
        """
        Retrieve a single package by ID.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            package_id: Package ID (UUID)
            
        Returns:
            Dictionary containing package details
            
        Example:
            >>> package = api.get_package(project_id, package_id)
        """
        url = f"{self.submittal_base}/projects/{project_id}/packages/{package_id}"
        response = self._make_request("GET", url)
        return response.json()
    
    # ========================================================================
    # Responses API
    # ========================================================================
    
    def get_responses(self, project_id: str, **params) -> Dict[str, Any]:
        """
        Retrieve all responses for a project.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            **params: Optional query parameters:
                - limit: Max results per page (1-50, default: 20)
                - offset: Number of results to skip
                
        Returns:
            Dictionary containing:
                - results: List of responses
                - pagination: Pagination information
                
        Example:
            >>> responses = api.get_responses(project_id)
        """
        url = f"{self.submittal_base}/projects/{project_id}/responses"
        response = self._make_request("GET", url, params=params)
        return response.json()
    
    def get_response(self, project_id: str, response_id: str) -> Dict[str, Any]:
        """
        Retrieve a single response by ID.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            response_id: Response ID (UUID)
            
        Returns:
            Dictionary containing response details
            
        Example:
            >>> response = api.get_response(project_id, response_id)
        """
        url = f"{self.submittal_base}/projects/{project_id}/responses/{response_id}"
        response = self._make_request("GET", url)
        return response.json()
    
    # ========================================================================
    # Settings - Mappings API
    # ========================================================================
    
    def get_settings_mappings(self, project_id: str, **params) -> Dict[str, Any]:
        """
        Retrieve users, roles, and companies assigned the manager role.
        
        Only users, roles, or companies retrieved from this endpoint can be
        set as a manager in a submittal item.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            **params: Optional query parameters:
                - limit: Max results per page (1-50, default: 20)
                - offset: Number of results to skip
                - filter[autodeskId]: Comma-separated list of Autodesk IDs
                
        Returns:
            Dictionary containing:
                - results: List of user-role mappings
                - pagination: Pagination information
                
        Example:
            >>> mappings = api.get_settings_mappings(project_id)
        """
        url = f"{self.submittal_base}/projects/{project_id}/settings/mappings"
        response = self._make_request("GET", url, params=params)
        return response.json()
    
    # ========================================================================
    # Specs API
    # ========================================================================
    
    def get_specs(self, project_id: str, **params) -> Dict[str, Any]:
        """
        Retrieve all spec sections for a project.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            **params: Optional query parameters:
                - limit: Max results per page (1-50, default: 20)
                - offset: Number of results to skip
                - search: Search string
                - sort: Sort by fields (e.g., "identifier asc")
                - filter[identifier]: Filter by spec section ID
                
        Returns:
            Dictionary containing:
                - results: List of spec sections
                - pagination: Pagination information
                
        Example:
            >>> specs = api.get_specs(project_id, search="Materials")
        """
        url = f"{self.submittal_base}/projects/{project_id}/specs"
        response = self._make_request("GET", url, params=params)
        return response.json()
    
    def get_spec(self, project_id: str, spec_id: str) -> Dict[str, Any]:
        """
        Retrieve a single spec section by ID.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            spec_id: Spec section ID (UUID)
            
        Returns:
            Dictionary containing spec section details
            
        Example:
            >>> spec = api.get_spec(project_id, spec_id)
        """
        url = f"{self.submittal_base}/projects/{project_id}/specs/{spec_id}"
        response = self._make_request("GET", url)
        return response.json()
    
    # ========================================================================
    # Steps API
    # ========================================================================
    
    def get_steps(self, project_id: str, item_id: str, **params) -> Dict[str, Any]:
        """
        Retrieve review steps associated with a submittal item.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            item_id: Submittal item ID (UUID)
            **params: Optional query parameters:
                - limit: Max results per page (1-50, default: 20)
                - offset: Number of results to skip
                
        Returns:
            Dictionary containing:
                - results: List of review steps
                - pagination: Pagination information
                
        Example:
            >>> steps = api.get_steps(project_id, item_id)
        """
        url = f"{self.submittal_base}/projects/{project_id}/items/{item_id}/steps"
        response = self._make_request("GET", url, params=params)
        return response.json()
    
    def get_step(self, project_id: str, item_id: str, step_id: str) -> Dict[str, Any]:
        """
        Retrieve a single review step by ID.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            item_id: Submittal item ID (UUID)
            step_id: Step ID (UUID)
            
        Returns:
            Dictionary containing step details including tasks
            
        Example:
            >>> step = api.get_step(project_id, item_id, step_id)
        """
        url = f"{self.submittal_base}/projects/{project_id}/items/{item_id}/steps/{step_id}"
        response = self._make_request("GET", url)
        return response.json()
    
    # ========================================================================
    # Tasks API
    # ========================================================================
    
    def get_tasks(self, project_id: str, item_id: str, step_id: str, **params) -> Dict[str, Any]:
        """
        Retrieve tasks associated with a review step.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            item_id: Submittal item ID (UUID)
            step_id: Step ID (UUID)
            **params: Optional query parameters:
                - limit: Max results per page (1-50, default: 20)
                - offset: Number of results to skip
                
        Returns:
            Dictionary containing:
                - results: List of tasks
                - pagination: Pagination information
                
        Example:
            >>> tasks = api.get_tasks(project_id, item_id, step_id)
        """
        url = f"{self.submittal_base}/projects/{project_id}/items/{item_id}/steps/{step_id}/tasks"
        response = self._make_request("GET", url, params=params)
        return response.json()
    
    def get_task(self, project_id: str, item_id: str, step_id: str, task_id: str) -> Dict[str, Any]:
        """
        Retrieve a single task by ID.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            item_id: Submittal item ID (UUID)
            step_id: Step ID (UUID)
            task_id: Task ID (UUID)
            
        Returns:
            Dictionary containing task details
            
        Example:
            >>> task = api.get_task(project_id, item_id, step_id, task_id)
        """
        url = f"{self.submittal_base}/projects/{project_id}/items/{item_id}/steps/{step_id}/tasks/{task_id}"
        response = self._make_request("GET", url)
        return response.json()
    
    # ========================================================================
    # Templates API
    # ========================================================================
    
    def get_templates(self, project_id: str, **params) -> Dict[str, Any]:
        """
        Retrieve review templates for a project.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            **params: Optional query parameters:
                - limit: Max results per page (1-50, default: 20)
                - offset: Number of results to skip
                - sort: Sort by fields (e.g., "name asc")
                
        Returns:
            Dictionary containing:
                - results: List of review templates with steps and tasks
                - pagination: Pagination information
                
        Example:
            >>> templates = api.get_templates(project_id)
        """
        url = f"{self.submittal_base}/projects/{project_id}/templates"
        response = self._make_request("GET", url, params=params)
        return response.json()
    
    # ========================================================================
    # User Profile API
    # ========================================================================
    
    def get_user_profile(self, project_id: str) -> Dict[str, Any]:
        """
        Retrieve the current user's profile, roles, and permitted actions.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            
        Returns:
            Dictionary containing:
                - id: User's Autodesk ID
                - roles: List of assigned roles (1=Manager, 2=User, 4=Admin)
                - permittedActions: List of actions user can perform
                
        Example:
            >>> profile = api.get_user_profile(project_id)
            >>> print(f"User ID: {profile['id']}")
            >>> print(f"Roles: {profile['roles']}")
        """
        url = f"{self.submittal_base}/projects/{project_id}/users/me"
        response = self._make_request("GET", url)
        return response.json()
    
    # ========================================================================
    # Helper Methods
    # ========================================================================
    
    def get_workflow_activity_log(self, project_id: str, item_id: str) -> List[Dict[str, Any]]:
        """
        Get complete workflow activity log for a submittal item.
        
        This method combines multiple API calls to create a comprehensive activity log
        similar to what's shown in the ACC UI, including:
        - Item creation
        - File attachments added
        - Workflow state changes
        - Review submissions and responses
        - Comments and final responses
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            item_id: Submittal item ID (UUID)
            
        Returns:
            List of activity events sorted by timestamp, each containing:
                - timestamp: ISO 8601 datetime
                - event_type: Type of activity (created, submitted, reviewed, etc.)
                - description: Human-readable description
                - user_id: User who performed the action (if available)
                - details: Additional event-specific data
                
        Example:
            >>> activities = api.get_workflow_activity_log(project_id, item_id)
            >>> for activity in activities:
            ...     print(f"{activity['timestamp']}: {activity['description']}")
        """
        activities = []
        
        try:
            # 1. Get item basic info for creation event
            item = self.get_item(project_id, item_id)
            
            # Add item creation event
            if 'createdAt' in item:
                activities.append({
                    'timestamp': item['createdAt'],
                    'event_type': 'item_created',
                    'description': f"Item was created: {item.get('title', 'Untitled')}",
                    'user_id': item.get('createdBy'),
                    'details': {
                        'title': item.get('title'),
                        'identifier': item.get('identifier'),
                        'customIdentifier': item.get('customIdentifier')
                    }
                })
            
            # 2. Get attachments for file addition events
            try:
                attachments_response = self.get_attachments(project_id, item_id)
                attachments = attachments_response.get('results', [])
                
                for attachment in attachments:
                    if 'createdAt' in attachment:
                        activities.append({
                            'timestamp': attachment['createdAt'],
                            'event_type': 'file_added',
                            'description': f"A file reference was added: {attachment.get('name', 'Unknown file')}",
                            'user_id': attachment.get('createdBy'),
                            'details': {
                                'filename': attachment.get('name'),
                                'attachment_id': attachment.get('id'),
                                'is_uploaded': attachment.get('isFileUploaded'),
                                'revision': attachment.get('revision')
                            }
                        })
            except Exception as e:
                logger.warning(f"Could not retrieve attachments: {e}")
            
            # 3. Get revision history for workflow events
            try:
                revisions_response = self.get_item_revisions(project_id, item_id)
                revisions = revisions_response.get('results', [])
                
                for revision in revisions:
                    # Submitted to manager event
                    if 'receivedFromSubmitter' in revision and revision['receivedFromSubmitter']:
                        activities.append({
                            'timestamp': revision['receivedFromSubmitter'],
                            'event_type': 'submitted_to_manager',
                            'description': "Submitted to manager",
                            'user_id': revision.get('submittedBy'),
                            'details': {
                                'revision': revision.get('revision'),
                                'manager': revision.get('manager'),
                                'manager_type': revision.get('managerType')
                            }
                        })
                    
                    # Sent to review event
                    if 'sentToReview' in revision and revision['sentToReview']:
                        activities.append({
                            'timestamp': revision['sentToReview'],
                            'event_type': 'sent_to_review',
                            'description': "Sent for review",
                            'user_id': revision.get('sentToReviewBy'),
                            'details': {
                                'revision': revision.get('revision')
                            }
                        })
                    
                    # Returned from review event
                    if 'receivedFromReview' in revision and revision['receivedFromReview']:
                        activities.append({
                            'timestamp': revision['receivedFromReview'],
                            'event_type': 'returned_from_review',
                            'description': "Returned to manager",
                            'user_id': revision.get('respondedBy'),
                            'details': {
                                'revision': revision.get('revision'),
                                'response_comment': revision.get('responseComment')
                            }
                        })
                    
                    # Final response submitted event
                    if 'respondedAt' in revision and revision['respondedAt']:
                        response_comment = revision.get('responseComment', '')
                        activities.append({
                            'timestamp': revision['respondedAt'],
                            'event_type': 'final_response_submitted',
                            'description': f"Final response submitted: {response_comment}" if response_comment else "Final response submitted",
                            'user_id': revision.get('respondedBy'),
                            'details': {
                                'revision': revision.get('revision'),
                                'response_id': revision.get('responseId'),
                                'response_comment': response_comment
                            }
                        })
                    
                    # Published/Closed and distributed event
                    if 'publishedDate' in revision and revision['publishedDate']:
                        activities.append({
                            'timestamp': revision['publishedDate'],
                            'event_type': 'closed_and_distributed',
                            'description': "Closed and distributed",
                            'user_id': revision.get('publishedBy'),
                            'details': {
                                'revision': revision.get('revision')
                            }
                        })
                    
                    # Process steps and tasks for detailed workflow events
                    if 'steps' in revision:
                        for step in revision['steps']:
                            # Step started event
                            if 'startedAt' in step and step['startedAt']:
                                activities.append({
                                    'timestamp': step['startedAt'],
                                    'event_type': 'step_started',
                                    'description': f"Review step {step.get('stepNumber', 'N/A')} started",
                                    'user_id': None,
                                    'details': {
                                        'step_id': step.get('stepId'),
                                        'step_number': step.get('stepNumber'),
                                        'due_date': step.get('dueDate')
                                    }
                                })
                            
                            # Step completed event
                            if 'completedAt' in step and step['completedAt']:
                                activities.append({
                                    'timestamp': step['completedAt'],
                                    'event_type': 'step_completed',
                                    'description': f"Review step {step.get('stepNumber', 'N/A')} completed",
                                    'user_id': None,
                                    'details': {
                                        'step_id': step.get('stepId'),
                                        'step_number': step.get('stepNumber')
                                    }
                                })
                            
                            # Process tasks within steps
                            if 'tasks' in step:
                                for task in step['tasks']:
                                    # Task response/comment event
                                    if 'respondedAt' in task and task['respondedAt']:
                                        comment = task.get('responseComment', '')
                                        activities.append({
                                            'timestamp': task['respondedAt'],
                                            'event_type': 'comment_added',
                                            'description': f"Comment was added: {comment}" if comment else "Comment was added",
                                            'user_id': task.get('respondedBy'),
                                            'details': {
                                                'task_id': task.get('taskId'),
                                                'assigned_to': task.get('assignedTo'),
                                                'assigned_to_type': task.get('assignedToType'),
                                                'response_id': task.get('responseId'),
                                                'response_comment': comment,
                                                'is_required': task.get('isRequired')
                                            }
                                        })
            except Exception as e:
                logger.warning(f"Could not retrieve revisions: {e}")
            
            # 4. Get current steps and tasks for active workflow state
            try:
                steps_response = self.get_steps(project_id, item_id)
                current_steps = steps_response.get('results', [])
                
                for step in current_steps:
                    # Current step events (if not already captured in revisions)
                    if 'startedAt' in step and step['startedAt']:
                        # Check if this event is already in activities to avoid duplicates
                        existing_event = any(
                            act['timestamp'] == step['startedAt'] and 
                            act['event_type'] == 'step_started'
                            for act in activities
                        )
                        if not existing_event:
                            activities.append({
                                'timestamp': step['startedAt'],
                                'event_type': 'step_started',
                                'description': f"Review step {step.get('stepNumber', 'N/A')} started",
                                'user_id': step.get('createdBy'),
                                'details': {
                                    'step_id': step.get('id'),
                                    'step_number': step.get('stepNumber'),
                                    'status': step.get('status'),
                                    'due_date': step.get('dueDate')
                                }
                            })
                    
                    # Process current tasks
                    if 'tasks' in step:
                        for task in step['tasks']:
                            if 'respondedAt' in task and task['respondedAt']:
                                # Check for duplicates
                                existing_event = any(
                                    act['timestamp'] == task['respondedAt'] and 
                                    act['event_type'] == 'comment_added' and
                                    act['details'].get('task_id') == task.get('id')
                                    for act in activities
                                )
                                if not existing_event:
                                    comment = task.get('responseComment', '')
                                    activities.append({
                                        'timestamp': task['respondedAt'],
                                        'event_type': 'comment_added',
                                        'description': f"Comment was added: {comment}" if comment else "Comment was added",
                                        'user_id': task.get('respondedBy'),
                                        'details': {
                                            'task_id': task.get('id'),
                                            'assigned_to': task.get('assignedTo'),
                                            'assigned_to_type': task.get('assignedToType'),
                                            'response_id': task.get('responseId'),
                                            'response_comment': comment,
                                            'status': task.get('status')
                                        }
                                    })
            except Exception as e:
                logger.warning(f"Could not retrieve current steps: {e}")
            
        except Exception as e:
            logger.error(f"Error building workflow activity log: {e}")
            raise
        
        # Sort activities by timestamp
        activities.sort(key=lambda x: x['timestamp'])
        
        logger.info(f"Built workflow activity log with {len(activities)} events for item {item_id}")
        return activities
    
    def get_all_items_paginated(self, project_id: str, page_size: int = 50, **params) -> List[Dict[str, Any]]:
        """
        Retrieve all submittal items using pagination.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            page_size: Number of items per page (max 50)
            **params: Additional filter parameters
            
        Returns:
            List of all submittal items
            
        Example:
            >>> all_items = api.get_all_items_paginated(project_id)
        """
        all_items = []
        offset = 0
        params['limit'] = min(page_size, 50)
        
        while True:
            params['offset'] = offset
            response = self.get_items(project_id, **params)
            
            items = response.get('results', [])
            if not items:
                break
            
            all_items.extend(items)
            
            pagination = response.get('pagination', {})
            total_results = pagination.get('totalResults', 0)
            
            offset += len(items)
            
            # Check if we've retrieved all items
            if offset >= total_results:
                break
        
        logger.info(f"Retrieved {len(all_items)} submittal items from project {project_id}")
        return all_items
    
    def search_items_by_title(self, project_id: str, title: str) -> List[Dict[str, Any]]:
        """
        Search for submittal items by title.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            title: Title to search for
            
        Returns:
            List of matching submittal items
            
        Example:
            >>> items = api.search_items_by_title(project_id, "Shop Drawings")
        """
        response = self.get_items(project_id, search=title)
        return response.get('results', [])
    
    def get_items_by_status(self, project_id: str, status_id: str) -> List[Dict[str, Any]]:
        """
        Get all submittal items with a specific status.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            status_id: Status ID (1=Required, 2=Open, 3=Closed, 4=Void, 5=Empty, 6=Draft)
            
        Returns:
            List of submittal items with the specified status
            
        Example:
            >>> open_items = api.get_items_by_status(project_id, "2")
        """
        params = {'filter[statusId]': status_id}
        return self.get_all_items_paginated(project_id, **params)
    
    def get_item_with_full_details(self, project_id: str, item_id: str) -> Dict[str, Any]:
        """
        Get a submittal item with all related details (steps, tasks, attachments).
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            item_id: Submittal item ID (UUID)
            
        Returns:
            Dictionary containing item with enriched data
            
        Example:
            >>> item_details = api.get_item_with_full_details(project_id, item_id)
        """
        item = self.get_item(project_id, item_id)
        
        # Get steps with tasks
        try:
            steps_response = self.get_steps(project_id, item_id)
            item['steps'] = steps_response.get('results', [])
        except Exception as e:
            logger.warning(f"Could not retrieve steps: {e}")
            item['steps'] = []
        
        # Get attachments
        try:
            attachments_response = self.get_attachments(project_id, item_id)
            item['attachments'] = attachments_response.get('results', [])
        except Exception as e:
            logger.warning(f"Could not retrieve attachments: {e}")
            item['attachments'] = []
        
        # Get revisions
        try:
            revisions_response = self.get_item_revisions(project_id, item_id)
            item['revisions'] = revisions_response.get('results', [])
        except Exception as e:
            logger.warning(f"Could not retrieve revisions: {e}")
            item['revisions'] = []
        
        return item
    
    def format_activity_log_for_display(self, project_id: str, item_id: str, 
                                      include_user_names: bool = True) -> List[Dict[str, Any]]:
        """
        Get formatted activity log with user names resolved for display.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            item_id: Submittal item ID (UUID)
            include_user_names: Whether to resolve user IDs to names
            
        Returns:
            List of formatted activity events with user names
            
        Example:
            >>> formatted_log = api.format_activity_log_for_display(project_id, item_id)
        """
        activities = self.get_workflow_activity_log(project_id, item_id)
        
        if not include_user_names:
            return activities
        
        # Get user mappings for name resolution
        user_cache = {}
        
        try:
            # Get settings mappings to resolve some user names
            mappings_response = self.get_settings_mappings(project_id)
            mappings = mappings_response.get('results', [])
            
            for mapping in mappings:
                autodesk_id = mapping.get('autodeskId')
                if autodesk_id:
                    user_cache[autodesk_id] = {
                        'name': autodesk_id,  # Fallback to ID if no name available
                        'type': mapping.get('userType', '1')
                    }
        except Exception as e:
            logger.warning(f"Could not retrieve user mappings: {e}")
        
        # Enhance activities with user information
        for activity in activities:
            user_id = activity.get('user_id')
            if user_id and user_id in user_cache:
                activity['user_name'] = user_cache[user_id]['name']
                activity['user_type'] = user_cache[user_id]['type']
            elif user_id:
                activity['user_name'] = user_id  # Fallback to ID
                activity['user_type'] = '1'  # Default to user type
            else:
                activity['user_name'] = 'System'
                activity['user_type'] = 'system'
        
        return activities
    
    def get_activity_summary(self, project_id: str, item_id: str) -> Dict[str, Any]:
        """
        Get a summary of workflow activity for a submittal item.
        
        Args:
            project_id: Project ID (without 'b.' prefix)
            item_id: Submittal item ID (UUID)
            
        Returns:
            Dictionary containing activity summary statistics
            
        Example:
            >>> summary = api.get_activity_summary(project_id, item_id)
            >>> print(f"Total events: {summary['total_events']}")
        """
        activities = self.get_workflow_activity_log(project_id, item_id)
        
        # Count events by type
        event_counts = {}
        for activity in activities:
            event_type = activity['event_type']
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        # Get unique users involved
        users = set()
        for activity in activities:
            if activity.get('user_id'):
                users.add(activity['user_id'])
        
        # Calculate timeline
        timestamps = [activity['timestamp'] for activity in activities if activity.get('timestamp')]
        
        summary = {
            'total_events': len(activities),
            'event_counts': event_counts,
            'unique_users': len(users),
            'users_involved': list(users),
            'first_activity': min(timestamps) if timestamps else None,
            'last_activity': max(timestamps) if timestamps else None,
            'has_comments': any(act['event_type'] == 'comment_added' for act in activities),
            'has_attachments': any(act['event_type'] == 'file_added' for act in activities),
            'current_status': None  # Will be filled from item data
        }
        
        # Get current item status
        try:
            item = self.get_item(project_id, item_id)
            summary['current_status'] = {
                'state_id': item.get('stateId'),
                'state_name': get_state_name(item.get('stateId', '')),
                'status_id': item.get('statusId'),
                'status_name': get_status_name(item.get('statusId', ''))
            }
        except Exception as e:
            logger.warning(f"Could not get current item status: {e}")
        
        return summary


# ============================================================================
# Utility Functions
# ============================================================================

def convert_project_id(project_id_with_prefix: str) -> str:
    """
    Convert a project ID from Data Management API format to Submittal API format.
    
    The Submittal API requires project IDs without the 'b.' prefix.
    
    Args:
        project_id_with_prefix: Project ID with 'b.' prefix (e.g., 'b.a4be0c34a-4ab7')
        
    Returns:
        Project ID without prefix (e.g., 'a4be0c34a-4ab7')
        
    Example:
        >>> submittal_project_id = convert_project_id('b.a4be0c34a-4ab7')
        >>> print(submittal_project_id)  # 'a4be0c34a-4ab7'
    """
    if project_id_with_prefix.startswith('b.'):
        return project_id_with_prefix[2:]
    return project_id_with_prefix


def get_status_name(status_id: str) -> str:
    """
    Get human-readable status name from status ID.
    
    Args:
        status_id: Status ID as string
        
    Returns:
        Status name
    """
    status_map = {
        '1': 'Required',
        '2': 'Open',
        '3': 'Closed',
        '4': 'Void',
        '5': 'Empty',
        '6': 'Draft'
    }
    return status_map.get(status_id, 'Unknown')


def get_state_name(state_id: str) -> str:
    """
    Get human-readable state name from state ID.
    
    Args:
        state_id: State ID as string
        
    Returns:
        State name with description
    """
    state_map = {
        'sbc-1': 'Waiting for Submission',
        'mgr-1': 'Open - Submitted',
        'rev': 'Open - In Review',
        'mgr-2': 'Open - Reviewed',
        'sbc-2': 'Closed',
        'void': 'Voided',
        'draft': 'Draft'
    }
    return state_map.get(state_id, 'Unknown')


def get_user_type_name(user_type: str) -> str:
    """
    Get human-readable user type name from user type ID.
    
    Args:
        user_type: User type ID as string
        
    Returns:
        User type name
    """
    type_map = {
        '1': 'User',
        '2': 'Company',
        '3': 'Role'
    }
    return type_map.get(user_type, 'Unknown')


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    """
    Example usage of the Submittal API.
    
    Note: This requires a valid three-legged OAuth token with data:read scope.
    """
    
    # Initialize API client
    access_token = "YOUR_ACCESS_TOKEN"  # Replace with actual token
    api = SubmittalAPI(access_token)
    
    # Project ID (without 'b.' prefix)
    project_id = "9eae7d59-1469-4389-bfb2-4114e2ba5545"
    
    try:
        # Get user profile
        print("Getting user profile...")
        profile = api.get_user_profile(project_id)
        print(f"User ID: {profile['id']}")
        print(f"Roles: {profile['roles']}")
        
        # Get project metadata
        print("\nGetting project metadata...")
        metadata = api.get_metadata(project_id)
        print(f"Custom Identifier Sequence Type: {metadata['customIdentifierSequenceType']}")
        
        # Get all submittal items
        print("\nGetting submittal items...")
        items_response = api.get_items(project_id, limit=10)
        items = items_response['results']
        print(f"Found {len(items)} items")
        
        # Get details for first item
        if items:
            item = items[0]
            print(f"\nItem Details:")
            print(f"  ID: {item['id']}")
            print(f"  Title: {item['title']}")
            print(f"  Status: {get_status_name(item['statusId'])}")
            print(f"  State: {get_state_name(item['stateId'])}")
            
            # Get full details including steps and attachments
            full_details = api.get_item_with_full_details(project_id, item['id'])
            print(f"  Steps: {len(full_details.get('steps', []))}")
            print(f"  Attachments: {len(full_details.get('attachments', []))}")
            
            # Get workflow activity log
            print(f"\nWorkflow Activity Log:")
            try:
                activities = api.get_workflow_activity_log(project_id, item['id'])
                for activity in activities[-5:]:  # Show last 5 activities
                    print(f"  {activity['timestamp']}: {activity['description']}")
                
                # Get activity summary
                summary = api.get_activity_summary(project_id, item['id'])
                print(f"\nActivity Summary:")
                print(f"  Total Events: {summary['total_events']}")
                print(f"  Users Involved: {summary['unique_users']}")
                print(f"  Has Comments: {summary['has_comments']}")
                print(f"  Has Attachments: {summary['has_attachments']}")
                
            except Exception as e:
                print(f"  Could not retrieve activity log: {e}")
        
        # Get specs
        print("\nGetting spec sections...")
        specs = api.get_specs(project_id, limit=5)
        print(f"Found {len(specs['results'])} specs")
        
        # Get templates
        print("\nGetting review templates...")
        templates = api.get_templates(project_id)
        print(f"Found {len(templates['results'])} templates")
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

