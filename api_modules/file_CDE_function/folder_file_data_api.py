# -*- coding: utf-8 -*-
"""
Folder and File Data API Module
Provides database-backed APIs for folder permissions, custom attributes, and file versions
"""

from flask import Blueprint, jsonify, request
import psycopg2
import psycopg2.extras
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import logging
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database_sql.neon_config import NeonConfig

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Blueprint
folder_file_data_bp = Blueprint('folder_file_data', __name__, url_prefix='/api/folder-file-data')


class FolderFileDataAccess:
    """Data access layer for folder and file queries"""

    def __init__(self):
        """Initialize with database configuration"""
        neon_config = NeonConfig()
        self.db_params = neon_config.get_db_params()

    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(**self.db_params)

    def get_folder_permissions(self, project_id: str, folder_id: str) -> Optional[Dict]:
        """
        Get folder permissions from database

        Args:
            project_id: Project ID
            folder_id: Folder ID (URN format)

        Returns:
            Dict containing permissions data or None if not found
        """
        try:
            conn = self.get_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            query = """
                SELECT
                    id,
                    name,
                    path,
                    permissions,
                    permissions_sync_time
                FROM folders
                WHERE id = %s AND project_id = %s
            """

            cur.execute(query, (folder_id, project_id))
            result = cur.fetchone()

            cur.close()
            conn.close()

            if result:
                return {
                    "folder_id": result['id'],
                    "folder_name": result['name'],
                    "folder_path": result['path'],
                    "permissions": result['permissions'] if result['permissions'] else {},
                    "permissions_sync_time": result['permissions_sync_time'].isoformat() if result['permissions_sync_time'] else None
                }

            return None

        except Exception as e:
            logger.error(f"Error getting folder permissions: {str(e)}")
            raise

    def get_folder_custom_attribute_definitions(self, project_id: str, folder_id: str) -> List[Dict]:
        """
        Get custom attribute definitions for a folder (including inherited project-level attributes)

        Args:
            project_id: Project ID
            folder_id: Folder ID (URN format)

        Returns:
            List of custom attribute definitions
        """
        try:
            conn = self.get_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            query = """
                -- Folder-level attributes
                SELECT
                    id,
                    attr_id,
                    project_id,
                    scope_type,
                    scope_folder_id,
                    name,
                    type,
                    array_values,
                    description,
                    is_required,
                    default_value,
                    inherit_to_subfolders,
                    created_at,
                    updated_at
                FROM custom_attribute_definitions
                WHERE scope_type = 'folder'
                  AND scope_folder_id = %s
                  AND project_id = %s

                UNION

                -- Project-level attributes (applicable to all folders)
                SELECT
                    id,
                    attr_id,
                    project_id,
                    scope_type,
                    scope_folder_id,
                    name,
                    type,
                    array_values,
                    description,
                    is_required,
                    default_value,
                    inherit_to_subfolders,
                    created_at,
                    updated_at
                FROM custom_attribute_definitions
                WHERE scope_type = 'project'
                  AND project_id = %s

                ORDER BY scope_type DESC, name ASC
            """

            cur.execute(query, (folder_id, project_id, project_id))
            results = cur.fetchall()

            cur.close()
            conn.close()

            return [dict(row) for row in results]

        except Exception as e:
            logger.error(f"Error getting folder custom attribute definitions: {str(e)}")
            raise

    def get_file_custom_attributes(self, project_id: str, file_id: str) -> Dict:
        """
        Get custom attribute values for a file

        Args:
            project_id: Project ID
            file_id: File ID (URN format)

        Returns:
            Dict containing file info and custom attributes
        """
        try:
            conn = self.get_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # Get file basic info
            file_query = """
                SELECT
                    f.id,
                    f.name,
                    f.display_name,
                    f.file_type,
                    f.parent_folder_id,
                    f.folder_path,
                    fv.version_number as current_version,
                    fv.file_size as current_file_size,
                    fv.review_state
                FROM files f
                LEFT JOIN file_versions fv ON f.id = fv.file_id AND fv.is_current_version = true
                WHERE f.id = %s AND f.project_id = %s
            """

            cur.execute(file_query, (file_id, project_id))
            file_info = cur.fetchone()

            if not file_info:
                cur.close()
                conn.close()
                return None

            # Get custom attributes
            attributes_query = """
                SELECT
                    cad.id as definition_id,
                    cad.attr_id,
                    cad.name as attr_name,
                    cad.type as attr_type,
                    cad.scope_type,
                    cad.is_required,
                    cav.value as text_value,
                    cav.value_date,
                    cav.value_number,
                    cav.value_boolean,
                    cav.value_array,
                    cav.updated_at,
                    cav.updated_by_user_name
                FROM custom_attribute_values cav
                JOIN custom_attribute_definitions cad ON cav.attr_definition_id = cad.id
                WHERE cav.file_id = %s AND cav.project_id = %s
                ORDER BY cad.name
            """

            cur.execute(attributes_query, (file_id, project_id))
            attributes = cur.fetchall()

            cur.close()
            conn.close()

            # Process attributes to get actual values based on type
            processed_attributes = []
            for attr in attributes:
                attr_dict = dict(attr)

                # Determine the actual value based on type
                if attr['attr_type'] == 'string':
                    attr_dict['value'] = attr['text_value']
                elif attr['attr_type'] == 'date':
                    attr_dict['value'] = attr['value_date'].isoformat() if attr['value_date'] else None
                elif attr['attr_type'] == 'number':
                    attr_dict['value'] = float(attr['value_number']) if attr['value_number'] else None
                elif attr['attr_type'] == 'boolean':
                    attr_dict['value'] = attr['value_boolean']
                elif attr['attr_type'] == 'array':
                    attr_dict['value'] = attr['value_array']
                else:
                    attr_dict['value'] = attr['text_value']

                # Remove raw value fields
                for key in ['text_value', 'value_date', 'value_number', 'value_boolean', 'value_array']:
                    attr_dict.pop(key, None)

                processed_attributes.append(attr_dict)

            return {
                "file_info": dict(file_info),
                "custom_attributes": processed_attributes,
                "attributes_count": len(processed_attributes)
            }

        except Exception as e:
            logger.error(f"Error getting file custom attributes: {str(e)}")
            raise

    def get_file_versions(self, project_id: str, file_id: str, include_current_only: bool = False) -> Dict:
        """
        Get all versions of a file

        Args:
            project_id: Project ID
            file_id: File ID (URN format)
            include_current_only: If True, only return current version

        Returns:
            Dict containing file info and version history
        """
        try:
            conn = self.get_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            # Get file basic info
            file_query = """
                SELECT
                    id,
                    name,
                    display_name,
                    file_type,
                    mime_type,
                    parent_folder_id,
                    folder_path,
                    full_path,
                    create_time,
                    create_user_name,
                    last_modified_time,
                    last_modified_user_name
                FROM files
                WHERE id = %s AND project_id = %s
            """

            cur.execute(file_query, (file_id, project_id))
            file_info = cur.fetchone()

            if not file_info:
                cur.close()
                conn.close()
                return None

            # Get file versions
            if include_current_only:
                versions_query = """
                    SELECT
                        id as version_id,
                        version_number,
                        urn,
                        item_urn,
                        storage_urn,
                        file_size,
                        storage_size,
                        mime_type,
                        process_state,
                        is_current_version,
                        review_state,
                        version_status,
                        create_time,
                        create_user_id,
                        create_user_name,
                        download_url,
                        created_at,
                        updated_at
                    FROM file_versions
                    WHERE file_id = %s AND is_current_version = true
                    ORDER BY version_number DESC
                """
            else:
                versions_query = """
                    SELECT
                        id as version_id,
                        version_number,
                        urn,
                        item_urn,
                        storage_urn,
                        file_size,
                        storage_size,
                        mime_type,
                        process_state,
                        is_current_version,
                        review_state,
                        version_status,
                        create_time,
                        create_user_id,
                        create_user_name,
                        download_url,
                        created_at,
                        updated_at
                    FROM file_versions
                    WHERE file_id = %s
                    ORDER BY version_number DESC
                """

            cur.execute(versions_query, (file_id,))
            versions = cur.fetchall()

            cur.close()
            conn.close()

            # Calculate statistics
            total_size = sum(v['file_size'] or 0 for v in versions)
            current_version = next((v for v in versions if v['is_current_version']), None)

            return {
                "file_info": dict(file_info),
                "versions": [dict(v) for v in versions],
                "summary": {
                    "total_versions": len(versions),
                    "current_version": current_version['version_number'] if current_version else None,
                    "total_size_bytes": total_size,
                    "in_review": any(v['review_state'] == 'InReview' for v in versions)
                }
            }

        except Exception as e:
            logger.error(f"Error getting file versions: {str(e)}")
            raise


# Initialize data access
data_access = FolderFileDataAccess()


# ============================================================================
# Helper Functions
# ============================================================================

def success_response(data: Any, message: str = None) -> Dict:
    """Create a standardized success response"""
    return {
        "success": True,
        "data": data,
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


def error_response(error: str, code: str = None) -> Dict:
    """Create a standardized error response"""
    return {
        "success": False,
        "error": error,
        "error_code": code,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


def validate_required_param(param_name: str, param_value: Any) -> bool:
    """Validate required parameter"""
    if not param_value:
        raise ValueError(f"Missing required parameter: {param_name}")
    return True


# ============================================================================
# API Routes
# ============================================================================

@folder_file_data_bp.route('/folders/<path:folder_id>/permissions', methods=['GET'])
def get_folder_permissions(folder_id: str):
    """
    Get folder permissions from database

    Query Parameters:
        - project_id (required): Project ID

    Returns:
        JSON response with folder permissions data
    """
    try:
        project_id = request.args.get('project_id')
        validate_required_param('project_id', project_id)

        logger.info(f"Getting permissions for folder: {folder_id}, project: {project_id}")

        result = data_access.get_folder_permissions(project_id, folder_id)

        if not result:
            return jsonify(error_response("Folder not found", "FOLDER_NOT_FOUND")), 404

        return jsonify(success_response(result)), 200

    except ValueError as e:
        return jsonify(error_response(str(e), "VALIDATION_ERROR")), 400
    except Exception as e:
        logger.error(f"Error in get_folder_permissions: {str(e)}")
        return jsonify(error_response(f"Internal server error: {str(e)}", "INTERNAL_ERROR")), 500


@folder_file_data_bp.route('/folders/<path:folder_id>/custom-attribute-definitions', methods=['GET'])
def get_folder_custom_attribute_definitions(folder_id: str):
    """
    Get custom attribute definitions for a folder (including inherited project-level attributes)

    Query Parameters:
        - project_id (required): Project ID

    Returns:
        JSON response with custom attribute definitions
    """
    try:
        project_id = request.args.get('project_id')
        validate_required_param('project_id', project_id)

        logger.info(f"Getting custom attribute definitions for folder: {folder_id}, project: {project_id}")

        attributes = data_access.get_folder_custom_attribute_definitions(project_id, folder_id)

        # Calculate summary
        folder_level = sum(1 for attr in attributes if attr['scope_type'] == 'folder')
        project_level = sum(1 for attr in attributes if attr['scope_type'] == 'project')

        result = {
            "folder_id": folder_id,
            "attributes": attributes,
            "summary": {
                "total": len(attributes),
                "folder_level": folder_level,
                "project_level": project_level
            }
        }

        return jsonify(success_response(result)), 200

    except ValueError as e:
        return jsonify(error_response(str(e), "VALIDATION_ERROR")), 400
    except Exception as e:
        logger.error(f"Error in get_folder_custom_attribute_definitions: {str(e)}")
        return jsonify(error_response(f"Internal server error: {str(e)}", "INTERNAL_ERROR")), 500


@folder_file_data_bp.route('/files/<path:file_id>/custom-attributes', methods=['GET'])
def get_file_custom_attributes(file_id: str):
    """
    Get custom attribute values for a file

    Query Parameters:
        - project_id (required): Project ID

    Returns:
        JSON response with file info and custom attributes
    """
    try:
        project_id = request.args.get('project_id')
        validate_required_param('project_id', project_id)

        logger.info(f"Getting custom attributes for file: {file_id}, project: {project_id}")

        result = data_access.get_file_custom_attributes(project_id, file_id)

        if not result:
            return jsonify(error_response("File not found", "FILE_NOT_FOUND")), 404

        return jsonify(success_response(result)), 200

    except ValueError as e:
        return jsonify(error_response(str(e), "VALIDATION_ERROR")), 400
    except Exception as e:
        logger.error(f"Error in get_file_custom_attributes: {str(e)}")
        return jsonify(error_response(f"Internal server error: {str(e)}", "INTERNAL_ERROR")), 500


@folder_file_data_bp.route('/files/<path:file_id>/versions', methods=['GET'])
def get_file_versions(file_id: str):
    """
    Get all versions of a file

    Query Parameters:
        - project_id (required): Project ID
        - current_only (optional): If 'true', only return current version

    Returns:
        JSON response with file info and version history
    """
    try:
        project_id = request.args.get('project_id')
        validate_required_param('project_id', project_id)

        current_only = request.args.get('current_only', 'false').lower() == 'true'

        logger.info(f"Getting versions for file: {file_id}, project: {project_id}, current_only: {current_only}")

        result = data_access.get_file_versions(project_id, file_id, current_only)

        if not result:
            return jsonify(error_response("File not found", "FILE_NOT_FOUND")), 404

        return jsonify(success_response(result)), 200

    except ValueError as e:
        return jsonify(error_response(str(e), "VALIDATION_ERROR")), 400
    except Exception as e:
        logger.error(f"Error in get_file_versions: {str(e)}")
        return jsonify(error_response(f"Internal server error: {str(e)}", "INTERNAL_ERROR")), 500


@folder_file_data_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint

    Returns:
        JSON response with service status
    """
    try:
        # Test database connection
        conn = data_access.get_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        conn.close()

        return jsonify({
            "status": "healthy",
            "service": "folder_file_data_api",
            "database": "connected",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 200

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            "status": "unhealthy",
            "service": "folder_file_data_api",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), 503


# ============================================================================
# Module Info
# ============================================================================

if __name__ == '__main__':
    print("Folder File Data API Module")
    print("=" * 60)
    print("Available endpoints:")
    print("  GET /api/folder-file-data/folders/<folder_id>/permissions")
    print("  GET /api/folder-file-data/folders/<folder_id>/custom-attribute-definitions")
    print("  GET /api/folder-file-data/files/<file_id>/custom-attributes")
    print("  GET /api/folder-file-data/files/<file_id>/versions")
    print("  GET /api/folder-file-data/health")
    print("=" * 60)
