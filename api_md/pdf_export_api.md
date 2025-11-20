Documentation /Autodesk Construction Cloud APIs /API Reference
Export PDF Files
POST	projects/{projectId}/exports
Exports one or more individual PDFs, or 2D views and sheets (from DWG or RVT files) as PDFs from the ACC files module. All PDFs are packaged into a single ZIP file.

Notes:

A maximum of 200 files may be exported in a single operation (in a ZIP file).
For DWG files, 2D views can only be exported from DWG files uploaded after May 1, 2023.
For RVT files, 2D views and sheets can only be exported from RVT files created with Revit 2022 or newer versions. The name of each sheet or view in the exported result is a combination of the type, level name, and sheet/view name, e.g., Sheets - A001, Views - Structure Plan - A001.
The files can be exported once they’ve been successfully uploaded and processed. For more details about uploading files, see the Upload Files help documentation. For DWG or RVT file, if it is not processed completely, the exporting will skip it and the status will be partialSuccess.

A user must have at least download permission to perform this export operation. For more information about permissions, see the Folder Permissions help documentation.

The file created for export is specified by a file version ID, which identifies a specific version of the file. For how to get version ID, see the tutorial Export Files.

Exporting markups and links:

You can export files with both standard markups and feature markups (Issues and Photos are the currently supported features). For more information about feature markups, see the Feature Markups and Measurement help documentation.
For each markup type (standard, Issues, and Photos), you can specify whether to export published markups, unpublished markups, or both. For more information about published and unpublished markups, see the Create and Style Markups help documentation.
With standard markups, you can also specify whether to include attached links. For more information about markups links, see the Markups Links and References help documentation.
Note that this endpoint is asynchronous and initiates a job that runs in the background, rather than halting execution of your program. The response returns an export ID that you can use to poll GET /projects/{projectId}/exports/{exportId} to verify the status of the job. When the job is completed, an S3 signed url will be available for downloading the exported result.

For more details about exporting files, see the Export Files tutorial.

Note that this endpoint is not compatible with BIM 360 projects. For BIM 360 projects use POST versions/{version_id}/exports.

Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/construction/files/v1/projects/{projectId}/exports
Authentication Context	
user context optional
Required OAuth Scopes	
data:write
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via either a two-legged or three-legged OAuth flow.
x-user-id
string
The ID of a user on whose behalf your API request is acting. Required if you’re using a 2-legged authentication context, which must be 2-legged OAuth2 security with user impersonation.
The app has access to all users specified by the administrator in the SaaS integrations UI. By providing this header, the API call will be limited to act on behalf of only the user specified.

You can use either the user’s ACC ID (id), or their Autodesk ID (autodeskId).

Content-Type*
string
Must be application/json
* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project. Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can use a project ID either with a “b.” prefix or without a “b.” prefix. For instance, a project ID of “b.a4be0c34a-4ab7” can also be referred to as “a4be0c34a-4ab7”.
Request
Body Structure
The request body includes the URNs of the file versions to export, and the types of markups to include with the exported files.

 Expand all
options
object
The criteria for the markups and links to include with the exported files.
Note that unpublished markups are those visible only to their creator.

fileVersions*
array: string
A list of file version URNs. A maximum of 200 files may be included.
* Required
Response
HTTP Status Code Summary
202
Accepted
Successfully created an export job.
400
Bad Request
The parameters of the requested operation are invalid.
Sample error code with possible messages:

ERR_BAD_INPUT:
Multiple documents only can be exported as a ZIP file.
2D views and sheets in DWG or RVT format can only be exported as a ZIP file.
Some resources are not valid types (only PDF, DWG, and RVT are accepted).
401
Unauthorized
The provided bearer token is not valid.
Sample error code with possible messages:

ERR_AUTHENTICATED_ERROR:
Authentication header is not correct
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
Sample error code with possible messages:

ERR_NOT_ALLOWED:
Account inactive
Project inactive
User inactive
Api access deny
User {userId} does not have download permission on resource {resource}
404
Not Found
The resources requested, e.g. project, account, user, and any files included, do not exist.
Sample error code with possible messages:

ERR_RESOURCE_NOT_EXIST:
Some resources are not found
Account not found
Project not found
Project user not found
422
Unprocessable Entity
The total file size exceeds the 10GB maximum limit.
Sample error code with possible messages:

ERR_FILES_TOO_LARGE:
The overall file size is over 10GB.
500
Internal Server Error
An unknown error occurred on the server.
Sample error code with possible messages:

ERR_INTERNAL_SERVER_ERROR:
Request failed for internal exception xxx
Failed to get account
Failed to get project
Failed to get user
Response
Body Structure (202)
id
string: UUID
The ID of the PDF export job.
status
enum:string
The status of the PDF export job. Possible values: successful, processing, failed
Example
Successfully created an export job.

Request
curl -v 'https://developer.api.autodesk.com/construction/files/v1/projects/9ba6681e-1952-4d54-aac4-9de6d9858dd4/exports' \
  -X 'POST' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a' \
  -H 'Content-Type: application/json' \
  -d '{
        "options": {
          "outputFileName": "output_file_name",
          "standardMarkups": {
            "includePublishedMarkups": true,
            "includeUnpublishedMarkups": true,
            "includeMarkupLinks": false
          },
          "issueMarkups": {
            "includePublishedMarkups": false,
            "includeUnpublishedMarkups": false
          },
          "photoMarkups": {
            "includePublishedMarkups": false,
            "includeUnpublishedMarkups": false
          }
        },
        "fileVersions": [
          "urn:adsk.wip.file:vf.fileId?version=2"
        ]
      }'
Show Less
Response
{
  "id": "636e6a96-d4d2-43e6-b67a-db8618fc0ff9",
  "status": "processing"
}

Autodesk Construction Cloud APIs /API Reference
Export Status and Result
GET	projects/{projectId}/exports/{exportId}
Retrieves the status of an export job. The S3 signed URL (in result.output.signedUrl) will be available for downloading the exported file.

The export job ID is obtained from POST /projects/{projectId}/exports.

Note that only the authenticated user who launched the export job may use this endpoint to retrieve the signed URL. The signed URL will be available for 1 hour, and will expire thereafter. If you haven’t downloaded the file yet, you must create a new export job for the same files.

For more details about exporting files, see the Export Files tutorial.

Note that this endpoint is not compatible with BIM 360 projects. For BIM 360 projects use GET versions/{version_id}/exports/{export_id}.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/files/v1/projects/{projectId}/exports/{exportId}
Authentication Context	
user context optional
Required OAuth Scopes	
data:read
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via either a two-legged or three-legged OAuth flow.
x-user-id
string
The ID of a user on whose behalf your API request is acting. Required if you’re using a 2-legged authentication context, which must be 2-legged OAuth2 security with user impersonation.
The app has access to all users specified by the administrator in the SaaS integrations UI. By providing this header, the API call will be limited to act on behalf of only the user specified.

You can use either the user’s ACC ID (id), or their Autodesk ID (autodeskId).

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project. Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can use a project ID either with a “b.” prefix or without a “b.” prefix. For instance, a project ID of “b.a4be0c34a-4ab7” can also be referred to as “a4be0c34a-4ab7”.
exportId
string
The ID of the export job. The export ID is generated when you initialize an export job using POST exports.
Response
HTTP Status Code Summary
200
OK
Successfully get the export job status
400
Bad Request
The parameters of the requested operation are invalid.
Sample error code with possible messages:

ERR_BAD_INPUT:
Failed to parse the token
401
Unauthorized
The provided bearer token is not valid.
Sample error code with possible messages:

ERR_AUTHENTICATED_ERROR:
Authentication header is not correct
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
Sample error code with possible messages:

ERR_NOT_ALLOWED:
Account inactive
Project inactive
User inactive
Api access deny
User {userId} does not have download permission on resource {resource}
404
Not Found
The project, project user or the exporting job is not found
Sample error code with possible messages:

ERR_RESOURCE_NOT_EXIST:
Project not found
Project user not found
The job does not exist
500
Internal Server Error
An unknown error occurred on the server.
Sample error code with possible messages:

ERR_INTERNAL_SERVER_ERROR:
Request failed for internal exception xxx
Failed to get account
Failed to get project
Failed to get user
ERR_WORKFLOW_TIMEOUT
Workflow Timeout Error
Response
Body Structure (200)
 Expand all
id
string: UUID
The ID of the PDF export job.
status
string
The status of the PDF export job.
result
object
The result of a completed export job:
If the exporting job’s status value is successful, the downloadable signed url will be included in the result.output object
If the exporting job’s status value is failed (e.g. the files have been deleted), the result.error object will be present with details.
If the exporting job’s status value is partialSuccess (e.g. when some dwg/rvt files do not contain any exportable views or sheets), the result.output.failedFiles object will be present with file urn and reason.
Example
Successfully retrieved export data

Request
curl -v 'https://developer.api.autodesk.com/construction/files/v1/projects/9ba6681e-1952-4d54-aac4-9de6d9858dd4/exports/5b4bb914-c123-4f10-87e3-579ef934aaf9' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response (200 with signedUrl)
{
  "id": "5b4bb914-c123-4f10-87e3-579ef934aaf9",
  "status": "successful",
  "result": {
    "output": {
      "signedUrl": "https://signedUrl"
    }
  }
}
Show Less
Response (200 with failed result)
{
  "id": "5b4bb914-c123-4f10-87e3-579ef934aaf9",
  "status": "failed",
  "result": {
    "error": {
      "code": "401",
      "title": "ERR_AUTHORIZATION_ERROR",
      "detail": "Authentication header is not correct"
    }
  }
}
Show More
Response (200 with partial successful result)
{
  "id": "5b4bb914-c123-4f10-87e3-579ef934aaf9",
  "status": "partialSuccess",
  "result": {
    "signedUrl": "https://signedUrl",
    "failedFiles": [{
      "id": "fileUrn",
      "reason": "ERR_NO_PROCESSABLE_FILES",
      "detail": "This file does not contain any 2d pdf files or still under processing."
    }]
  }
}
