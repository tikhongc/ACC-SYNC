Documentation /Autodesk Construction Cloud APIs /API Reference
Issues Profile
GET	users/me
Returns the current user permissions.

Note that if a user with View and assign issues for their company permissions attempts to assign a user from a another company to the issue, it will return an error. You can verify a user’s assignment permissions by checking the permittedActions or permissionLevels attributes.

This operation is available to everyone.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/issues/v1/projects/{projectId}/users/me
Authentication Context	
user context required
Required OAuth Scopes	
data:read
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via a three-legged OAuth flow.
x-ads-region
string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA.

For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
Invalid input
403
Forbidden
Unauthorized
404
Not Found
Project not found
500
Internal Server Error
Internal server error
Response
Body Structure (200)
 Expand all
id
string
The user’s Autodesk ID.
isProjectAdmin
boolean
States whether the current logged in user is a system admin.
canManageTemplates
boolean
Not relevant
issues
object
permissionLevels
array: string
The permission level of the user. Each permission level corresponds to a combination of values in the response. For example, a combination of read and create in the response, corresponds to a Full visibility permission level.
Note that if a user with View and assign issues for their company permissions attempts to assign a user from a another company to the issue, it will return an error. In addition, the user can both create and view issues for their own company. You can also verify a user’s assignment permissions by checking the permittedActions or permissionLevels attributes.

Edit, view, and assign This permission level is split into two sub-levels:
View and assign to their company (previously known as Create for my company) : create and the permittedActions array must include assign-same-company
View issues for their company. Assign issues to anyone. : create and the permittedActions array must include assign-all
Full visibility (previously known as Create for other companies): create, read
Manage issues: create, read, write
Possible values: create, read, write.

For more details about the permission levels, see Issues Permissions.

Example
Success

Request
curl -v 'https://developer.api.autodesk.com/construction/issues/v1/projects/:projectId/users/me' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "id": "BXQXL7646C2R",
  "isProjectAdmin": true,
  "canManageTemplates": "",
  "issues": {
    "new": {
      "permittedActions": [
        "add_comment"
      ],
      "permittedAttributes": [
        "title"
      ],
      "permittedStatuses": [
        "draft",
        "open",
        "pending",
        "in_progress",
        "completed",
        "in_review",
        "not_approved",
        "in_dispute",
        "closed"
      ],
      "permitted_actions": [
        "add_comment"
      ],
      "permitted_attributes": [
        "title"
      ],
      "permitted_statuses": [
        "open"
      ]
    },
    "filter": {
      "permittedStatuses": [
        "draft",
        "open",
        "pending",
        "in_progress",
        "completed",
        "in_review",
        "not_approved",
        "in_dispute",
        "closed"
      ]
    }
  },
  "permissionLevels": [
    "read"
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Issue Types
GET	projects/{projectId}/issue-types
Retrieves a project’s categories and types. Note the following differences in terminology between the product and the API:

Product Name	API Name
Category	Type
Type	Subtype
Note that by default this endpoint does not return types (subtypes). To return types (subtypes), you need to add the include=subtypes query string parameter.

Note that this endpoint does not return deleted items.

This operation is available to everyone.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/issues/v1/projects/{projectId}/issue-types
Authentication Context	
user context required
Required OAuth Scopes	
data:read
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via a three-legged OAuth flow.
x-ads-region
string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA.

For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Request
Query String Parameters
include
string
Use include=subtypes to include the types (subtypes) for each category (type).
limit
int
Add limit=20 to limit the results count (together with the offset to support pagination).
offset
int
Add offset=20 to get partial results (together with the limit to support pagination).
filter[updatedAt]
string
Retrieves types that were last updated at the specified date and time, in in one of the following URL-encoded formats: YYYY-MM-DDThh:mm:ss.sz or YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03 or 2022-02-28T22:00:00.000Z..2022-03-28T22:00:00.000Z
Specific day: e.g., 2022-03-02 or 2022-02-28T22:00:00.000Z
Specific start date: e.g., 2022-03-02.. or 2022-02-28T22:00:00.000Z..
Specific end date: e.g., ..2022-03-02 or ..2022-02-28T22:00:00.000Z
For more details, see JSON API Filtering.

filter[isActive]
boolean
Filter types by status e.g. filter[isActive]=true will only return active types. Default value: undefined (meaning both active & inactive issue type categories will return).
Response
HTTP Status Code Summary
200
OK
List of issue types
400
Bad Request
Invalid input
403
Forbidden
Unauthorized
404
Not Found
Project not found
500
Internal Server Error
Internal server error
Response
Body Structure (200)
 Expand all
pagination
object
The pagination object.
results
array: object
A list of issue type categories.
Example
List of issue types

Request
curl -v 'https://developer.api.autodesk.com/construction/issues/v1/projects/:projectId/issue-types' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 10,
    "offset": 100,
    "totalResults": 25
  },
  "results": [
    {
      "id": "1110f111-6c54-4b01-90e6-d701748f1111",
      "containerId": "a5f49f04-59bb-477c-97e6-6833cb50bdac",
      "title": "Coordination",
      "isActive": true,
      "orderIndex": 2,
      "permittedActions": [
        "edit"
      ],
      "permittedAttributes": [
        "title"
      ],
      "subtypes": [
        {
          "id": "2220f222-6c54-4b01-90e6-d701748f0222",
          "issueTypeId": "1110f111-6c54-4b01-90e6-d701748f1111",
          "title": "Clash",
          "code": "exo",
          "isActive": true,
          "orderIndex": 5,
          "isReadOnly": false,
          "permittedActions": [
            "edit"
          ],
          "permittedAttributes": [
            "title"
          ],
          "createdBy": "A3RGM375QTZ7",
          "createdAt": "2018-07-22T15:05:58.033Z",
          "updatedBy": "A3RGM375QTZ7",
          "updatedAt": "2018-07-22T15:05:58.033Z",
          "deletedBy": "A3RGM375QTZ7",
          "deletedAt": "2018-07-22T15:05:58.033Z"
        }
      ],
      "statusSet": "gg",
      "createdBy": "A3RGM375QTZ7",
      "createdAt": "2018-07-22T15:05:58.033Z",
      "updatedBy": "A3RGM375QTZ7",
      "updatedAt": "2018-07-22T15:05:58.033Z",
      "deletedBy": "A3RGM375QTZ7",
      "deletedAt": "2018-07-22T15:05:58.033Z"
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Issue Attribute Definitions
GET	projects/{projectId}/issue-attribute-definitions
Retrieves information about issue custom attributes (custom fields) for a project, including the custom attribute title, description and type.

For example, the possible values for a dropdown list, the IDs, the names and whether the attribute is visible.

Note that custom attributes are known as custom fields in the ACC UI.

For information about creating issue custom attributes for a project, see the help documentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/issues/v1/projects/{projectId}/issue-attribute-definitions
Authentication Context	
user context required
Required OAuth Scopes	
data:read
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via a three-legged OAuth flow.
x-ads-region
string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA.

For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Request
Query String Parameters
limit
int
The number of custom attribute definitions to return in the response payload. For example, limit=2. Acceptable values: 1-200. Default value: 200.
offset
int
The number of custom attribute definitions you want to begin retrieving results from.
filter[createdAt]
datetime: ISO 8601
Retrieves items that were created at the specified date and time, in one of the following URL-encoded formats: YYYY-MM-DDThh:mm:ss.sz or YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03 or 2022-02-28T22:00:00.000Z..2022-03-28T22:00:00.000Z
Specific day: e.g., 2022-03-02 or 2022-02-28T22:00:00.000Z
Specific start date: e.g., 2022-03-02.. or 2022-02-28T22:00:00.000Z..
Specific end date: e.g., ..2022-03-02 or ..2022-02-28T22:00:00.000Z
For more details, see JSON API Filtering.

filter[updatedAt]
datetime: ISO 8601
Retrieves items that were last updated at the specified date and time, in one of the following URL-encoded formats: YYYY-MM-DDThh:mm:ss.sz or YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03 or 2022-02-28T22:00:00.000Z..2022-03-28T22:00:00.000Z
Specific day: e.g., 2022-03-02 or 2022-02-28T22:00:00.000Z
Specific start date: e.g., 2022-03-02.. or 2022-02-28T22:00:00.000Z..
Specific end date: e.g., ..2022-03-02 or ..2022-02-28T22:00:00.000Z
For more details, see JSON API Filtering.

filter[deletedAt]
datetime: ISO 8601
Retrieves types that were deleted at the specified date and time, in one of the following URL-encoded formats: YYYY-MM-DDThh:mm:ss.sz or YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03 or 2022-02-28T22:00:00.000Z..2022-03-28T22:00:00.000Z
Specific day: e.g., 2022-03-02 or 2022-02-28T22:00:00.000Z
Specific start date: e.g., 2022-03-02.. or 2022-02-28T22:00:00.000Z..
Specific end date: e.g., ..2022-03-02 or ..2022-02-28T22:00:00.000Z
To include non-deleted items in the response, add null to the filter: filter[deletedAt]=null,YYYY-MM-DDThh:mm:ss.sz...YYYY-MM-DDThh:mm:ss.sz.

For more details, see JSON API Filtering.

filter[dataType]
enum:string
Retrieves issue custom attribute definitions with the specified data type. Possible values: list (this corresponds to dropdown in the UI), text, paragraph, numeric. For example, filter[dataType]=text,numeric.
Response
HTTP Status Code Summary
200
OK
List of issue attribute definitions
400
Bad Request
Invalid input
403
Forbidden
Unauthorized
404
Not Found
Project not found
500
Internal Server Error
Internal server error
Response
Body Structure (200)
 Expand all
pagination
object
The pagination object.
results
array: object
A list of issue attribute definitions (custom fields).
Example
List of issue attribute definitions

Request
curl -v 'https://developer.api.autodesk.com/construction/issues/v1/projects/:projectId/issue-attribute-definitions' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 10,
    "offset": 100,
    "totalResults": 25
  },
  "results": [
    {
      "id": "1110f111-6c54-4b01-90e6-d701748f1111",
      "containerId": "2220f222-6c54-4b01-90e6-d701748f0222",
      "title": "Velocity",
      "description": "How long will it take for this issue to be resolved.",
      "dataType": "list",
      "metadata": {
        "list": {
          "options": [
            {
              "id": "802b87e0-60f6-4b1b-9cdf-37b53c731f17",
              "value": "option a"
            },
            {
              "id": "999b77e0-60f6-4b1b-9cdf-37b53c431f22",
              "value": "option b"
            }
          ]
        }
      },
      "permittedActions": [
        "edit"
      ],
      "permittedAttributes": [
        "title"
      ],
      "createdAt": "2018-07-22T15:05:58.033Z",
      "createdBy": "A3RGM375QTZ7",
      "updatedAt": "2018-07-22T15:05:58.033Z",
      "updatedBy": "A3RGM375QTZ7",
      "deletedAt": "2018-07-22T15:05:58.033Z",
      "deletedBy": "A3RGM375QTZ7"
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Issue Attribute Mappings
GET	projects/{projectId}/issue-attribute-mappings
Retrieves information about the issue custom attributes (custom fields) that are assigned to issue categories and issue types.

We do not currently support adding custom fields to issues. For information about adding custom fields to issues categories and types, see the help documentation.

Note that by default, this endpoint only retrieves custom attributes that were directly assigned to the issue category or issue type. It does not retrieve inherited custom attributes.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/issues/v1/projects/{projectId}/issue-attribute-mappings
Authentication Context	
user context required
Required OAuth Scopes	
data:read
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via a three-legged OAuth flow.
x-ads-region
string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA.

For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Request
Query String Parameters
limit
int
The number of custom attribute mappings to return in the response payload. For example, limit=2. Acceptable values: 1-200. Default value: 200.
offset
int
The number of custom attribute mappings you want to begin retrieving results from.
filter[createdAt]
datetime: ISO 8601
Retrieves items that were created at the specified date and time, in one of the following URL-encoded formats: YYYY-MM-DDThh:mm:ss.sz or YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03 or 2022-02-28T22:00:00.000Z..2022-03-28T22:00:00.000Z
Specific day: e.g., 2022-03-02 or 2022-02-28T22:00:00.000Z
Specific start date: e.g., 2022-03-02.. or 2022-02-28T22:00:00.000Z..
Specific end date: e.g., ..2022-03-02 or ..2022-02-28T22:00:00.000Z
For more details, see JSON API Filtering.

filter[updatedAt]
datetime: ISO 8601
Retrieves items that were last updated at the specified date and time, in one of the following URL-encoded formats: YYYY-MM-DDThh:mm:ss.sz or YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03 or 2022-02-28T22:00:00.000Z..2022-03-28T22:00:00.000Z
Specific day: e.g., 2022-03-02 or 2022-02-28T22:00:00.000Z
Specific start date: e.g., 2022-03-02.. or 2022-02-28T22:00:00.000Z..
Specific end date: e.g., ..2022-03-02 or ..2022-02-28T22:00:00.000Z
For more details, see JSON API Filtering.

filter[deletedAt]
datetime: ISO 8601
Retrieves types that were deleted at the specified date and time, in one of the following URL-encoded formats: YYYY-MM-DDThh:mm:ss.sz or YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03 or 2022-02-28T22:00:00.000Z..2022-03-28T22:00:00.000Z
Specific day: e.g., 2022-03-02 or 2022-02-28T22:00:00.000Z
Specific start date: e.g., 2022-03-02.. or 2022-02-28T22:00:00.000Z..
Specific end date: e.g., ..2022-03-02 or ..2022-02-28T22:00:00.000Z
To include non-deleted items in the response, add null to the filter: filter[deletedAt]=null,YYYY-MM-DDThh:mm:ss.sz...YYYY-MM-DDThh:mm:ss.sz.

For more details, see JSON API Filtering.

filter[attributeDefinitionId]
string
Retrieves issue custom attribute mappings associated with the specified issue custom attribute definitions. Separate multiple values with commas. For example: filter[attributeDefinitionId]=18ee5858-cbf1-451a-a525-7c6ff8156775.
filter[mappedItemId]
string
Retrieves issue custom attribute mappings associated with the specified items (project, type, or subtype). Separate multiple values with commas. For example: filter[mappedItemId]=18ee5858-cbf1-451a-a525-7c6ff8156775. Note that this does not retrieve inherited custom attribute mappings or custom attribute mappings of descendants.
Response
HTTP Status Code Summary
200
OK
List of issue attribute mappings
400
Bad Request
Invalid input
403
Forbidden
Unauthorized
404
Not Found
Project not found
500
Internal Server Error
Internal server error
Response
Body Structure (200)
 Expand all
pagination
object
The pagination object.
results
array: object
A list of issue attribute mappings.
Example
List of issue attribute mappings

Request
curl -v 'https://developer.api.autodesk.com/construction/issues/v1/projects/:projectId/issue-attribute-mappings' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 10,
    "offset": 100,
    "totalResults": 25
  },
  "results": [
    {
      "id": "1110f111-6c54-4b01-90e6-d701748f1111",
      "attributeDefinitionId": "1110f111-6c54-4b01-90e6-d701748f1333",
      "containerId": "2220f222-6c54-4b01-90e6-d701748f0222",
      "mappedItemType": "issueType",
      "mappedItemId": "2220f222-6c54-4b01-90e6-d701748f0222",
      "order": 2,
      "permittedActions": [
        "delete"
      ],
      "permittedAttributes": [
        ""
      ],
      "createdAt": "2018-07-22T15:05:58.033Z",
      "createdBy": "A3RGM375QTZ7",
      "updatedAt": "2018-07-22T15:05:58.033Z",
      "updatedBy": "A3RGM375QTZ7",
      "deletedAt": "2018-07-22T15:05:58.033Z",
      "deletedBy": "A3RGM375QTZ7"
    }
  ]
}


Documentation /Autodesk Construction Cloud APIs /API Reference
Issue Root Cause Categories
GET	projects/{projectId}/issue-root-cause-categories
Retrieves a list of supported root cause categories and root causes that you can allocate to an issue. For example, communication and coordination.

Note that by default, this endpoint only returns root cause categories. To include root causes you need to to add the include query string parameter (include=rootcauses).

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/issues/v1/projects/{projectId}/issue-root-cause-categories
Authentication Context	
user context required
Required OAuth Scopes	
data:read
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via a three-legged OAuth flow.
x-ads-region
string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA.

For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Request
Query String Parameters
include
string
Add ‘include=rootcauses’ to add the root causes for each category.
limit
int
Add limit=20 to limit the results count (together with the offset to support pagination).
offset
int
Add offset=20 to get partial results (together with the limit to support pagination).
filter[updatedAt]
string
Retrieves root cause categories updated at the specified date and time, in one of the following URL-encoded formats: YYYY-MM-DDThh:mm:ss.sz or YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03 or 2022-02-28T22:00:00.000Z..2022-03-28T22:00:00.000Z
Specific day: e.g., 2022-03-02 or 2022-02-28T22:00:00.000Z
Specific start date: e.g., 2022-03-02.. or 2022-02-28T22:00:00.000Z..
Specific end date: e.g., ..2022-03-02 or ..2022-02-28T22:00:00.000Z
For more details, see JSON API Filtering.

Response
HTTP Status Code Summary
200
OK
List of issue root cause categories
400
Bad Request
Invalid input
403
Forbidden
Unauthorized
404
Not Found
Project not found
500
Internal Server Error
Internal server error
Response
Body Structure (200)
 Expand all
pagination
object
The pagination object.
results
array: object
A list of issue root cause categories.
Example
List of issue root cause categories

Request
curl -v 'https://developer.api.autodesk.com/construction/issues/v1/projects/:projectId/issue-root-cause-categories' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 10,
    "offset": 100,
    "totalResults": 25
  },
  "results": [
    {
      "id": "1110f111-6c54-4b01-90e6-d701748f1111",
      "title": "Coordination",
      "isActive": false,
      "permittedActions": [
        "edit"
      ],
      "permittedAttributes": [
        "title"
      ],
      "rootCauses": [
        {
          "id": "2220f222-6c54-4b01-90e6-d701748f0222",
          "rootCauseCategoryId": "1110f111-6c54-4b01-90e6-d701748f1111",
          "title": "Constructability",
          "isActive": false,
          "permittedActions": [
            "edit"
          ],
          "permittedAttributes": [
            "title"
          ],
          "createdAt": "2018-07-22T15:05:58.033Z",
          "createdBy": "A3RGM375QTZ7",
          "updatedAt": "2018-07-22T15:05:58.033Z",
          "updatedBy": "A3RGM375QTZ7",
          "deletedAt": "2018-07-22T15:05:58.033Z",
          "deletedBy": "A3RGM375QTZ7"
        }
      ],
      "createdAt": "2018-07-22T15:05:58.033Z",
      "createdBy": "A3RGM375QTZ7",
      "updatedAt": "2018-07-22T15:05:58.033Z",
      "updatedBy": "A3RGM375QTZ7",
      "deletedAt": "2018-07-22T15:05:58.033Z",
      "deletedBy": "A3RGM375QTZ7"
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Issues
GET	projects/{projectId}/issues
Retrieves information about all the issues in a project, including details about their associated comments and attachments.

We support retrieving file-related (pushpin) issues. However, we do not currently support retrieving sheet-related issues from the ACC Build Sheets tool.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/issues/v1/projects/{projectId}/issues
Authentication Context	
user context required
Required OAuth Scopes	
data:read
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via a three-legged OAuth flow.
x-ads-region
string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA.

For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Request
Query String Parameters
filter[id]
array: string: uuid
Filter issues by the unique issue ID. Separate multiple values with commas.
filter[issueTypeId]
array: string: uuid
Filter issues by the unique identifier of the category of the issue. Note that the API name for category is type. Separate multiple values with commas.
filter[issueSubtypeId]
array: string: uuid
Filter issues by the unique identifier of the type of the issue. Note that the API name for type is subtype. Separate multiple values with commas.
filter[status]
string
Filter issues by their status. Separate multiple values with commas.
filter[linkedDocumentUrn]
array: string
Retrieves pushpin issues associated with the specified files. We support all file types that are compatible with the Files tool. You need to specify the URL-encoded file item IDs. To find the file item IDs, use the Data Management API.
Note that you need to specify the 3D model item ID, which retrieves all pushpins associated with all 2D sheets and views associated with the 3D model. Similarly, if you specify a specific PDF file it retrieves all the pushpin issues associated with all the PDF file pages. We do not currently support retrieving pushpin issues associated with a specific 2D sheet or view.

By default, it returns pushpins for the latest version of the file. To retrieve pushpins for a specific version of a file together with pushpins for all previous versions of the specified file version, specify the version number, in the following format: @[version-number].

For example, filter[linkedDocument]=urn%3Aadsk.wipprod%3Adm.lineage%3AtFbo9zuDTW-nPh45gnM4gA@2.

Separate multiple values with commas.

Note that we do not currently support filtering sheets from the ACC Build Sheets tool.

filter[dueDate]
string
Filter issues by due date, in one of the following URL-encoded format: YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03
Specific day: e.g., 2022-03-02
Specific start date: e.g., 2022-03-02..
Specific end date: e.g., ..2022-03-02
For more details, see JSON API Filtering.

filter[startDate]
string
Filter issues by start date, in one of the following URL-encoded format: YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03
Specific day: e.g., 2022-03-02
Specific start date: e.g., 2022-03-02..
Specific end date: e.g., ..2022-03-02
For more details, see JSON API Filtering.

filter[deleted]
boolean
Filter deleted issues. For example, filter[deleted]=true. If set to true it only returns deleted issues. If set to false it only returns undeleted issues. Note that we do not currently support returning both deleted and undeleted issues. Default value: false.
Project members with View and assign to their company and Full visibility can view deleted published and unpublished issues they originally created. Project members with Manage issues or Manage member permissions access can view all published issues that were deleted in a project. In addition, they can see unpublished deleted issues if they are an issue watcher, assignee, or creator.

For more information about deleted issues see the Help documentation.

filter[createdAt]
datetime: ISO 8601
Filter issues created at the specified date and time, in one of the following URL-encoded formats: YYYY-MM-DDThh:mm:ss.sz or YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03 or 2022-02-28T22:00:00.000Z..2022-03-28T22:00:00.000Z
Specific day: e.g., 2022-03-02 or 2022-02-28T22:00:00.000Z
Specific start date: e.g., 2022-03-02.. or 2022-02-28T22:00:00.000Z..
Specific end date: e.g., ..2022-03-02 or ..2022-02-28T22:00:00.000Z
For more details, see JSON API Filtering.

filter[createdBy]
array: string
Filter issues by the unique identifier of the user who created the issue. Separate multiple values with commas. For Example: A3RGM375QTZ7.
filter[updatedAt]
datetime: ISO 8601
Filter issues updated at the specified date and time, in one of the following URL-encoded formats: YYYY-MM-DDThh:mm:ss.sz or YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03 or 2022-02-28T22:00:00.000Z..2022-03-28T22:00:00.000Z
Specific day: e.g., 2022-03-02 or 2022-02-28T22:00:00.000Z
Specific start date: e.g., 2022-03-02.. or 2022-02-28T22:00:00.000Z..
Specific end date: e.g., ..2022-03-02 or ..2022-02-28T22:00:00.000Z
For more details, see JSON API Filtering.

filter[updatedBy]
array: string
Filter issues by the unique identifier of the user who updated the issue. Separate multiple values with commas. For Example: A3RGM375QTZ7.
filter[assignedTo]
array: string
Filter issues by the unique Autodesk ID of the User/Company/Role identifier of the current assignee of this issue. Separate multiple values with commas. For Example: A3RGM375QTZ7.
filter[rootCauseId]
array: string: uuid
Filter issues by the unique identifier of the type of root cause for the issue. Separate multiple values with commas.
filter[locationId]
array: string: uuid
Retrieves issues associated with the specified location but not the location’s sublocations. To also retrieve issues that relate to the locations’s sublocations use the sublocationId filter. Separate multiple values with commas.
filter[subLocationId]
array: string: uuid
Retrieves issues associated with the specified unique LBS (Location Breakdown Structure) identifier, as well as issues associated with the sub locations of the LBS identifier. Separate multiple values with commas.
filter[closedBy]
array: string
Filter issues by the unique identifier of the user who closed the issue. Separate multiple values with commas. For Example: A3RGM375QTZ7.
filter[closedAt]
datetime: ISO 8601
Filter issues closed at the specified date and time, in one of the following URL-encoded formats: YYYY-MM-DDThh:mm:ss.sz or YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03 or 2022-02-28T22:00:00.000Z..2022-03-28T22:00:00.000Z
Specific day: e.g., 2022-03-02 or 2022-02-28T22:00:00.000Z
Specific start date: e.g., 2022-03-02.. or 2022-02-28T22:00:00.000Z..
Specific end date: e.g., ..2022-03-02 or ..2022-02-28T22:00:00.000Z
For more details, see JSON API Filtering.

filter[search]
string
Filter issues using ‘search’ criteria. this will filter both title and issues display ID. For example, use filter[search]=300
filter[displayId]
int
Filter issues by the chronological user-friendly identifier. Separate multiple values with commas.
filter[assignedToType]
string
Filter issues by the type of the current assignee of this issue. Separate multiple values with commas. Possible values: Possible values: user, company, role, null. For Example: user.
filter[customAttributes]
array: string
Filter issues by the custom attributes. Each custom attribute filter should be defined by it’s uuid. For example: filter[customAttributes][f227d940-ae9b-4722-9297-389f4411f010]=1,2,3. Separate multiple values with commas.
filter[valid]
boolean
Only return valid issues (=no empty type/subtype). Default value: undefined (meaning will return both valid & invalid issues).
limit
int
Return specified number of issues. Acceptable values are 1-100. Default value: 100.
offset
int
Return issues starting from the specified offset number. Default value: 0.
sortBy
array: string
Sort issues by specified fields. Separate multiple values with commas. To sort in descending order add a - (minus sign) before the sort criteria. Possible values: displayId, title, description, status, assignedTo, assignedToType, dueDate, locationDetails, published, closedBy, closedAt, createdBy, createdAt, updatedAt, issueSubType, issueType, customAttributes, startDate, rootCause. For example: sortBy=status,-displayId,-dueDate,customAttributes[5c07cbe2-256a-48f1-b35b-2e5e00914104].
fields
array: string
Return only specific fields in issue object. Separate multiple values with commas. Fields which will be returned in any case: id, title, status, issueTypeId. Possible values: id, displayId, title, description, issueTypeId, issueSubtypeId, status, assignedTo, assignedToType, dueDate, startDate, locationId, locationDetails, rootCauseTitle, rootCauseId, permittedStatuses, permittedAttributes, permittedActions, published, commentCount, openedBy, openedAt, closedBy, closedAt, createdBy, createdAt, updatedBy, updatedAt, customAttributes.
Response
HTTP Status Code Summary
200
OK
List of relevant issues in combination with pagination details
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers. The client SHOULD NOT repeat the request without modifications. The response body may give an indication of what is wrong with the request
403
Forbidden
The request is valid but lacks the necessary permissions.
404
Not Found
The specified resource was not found
Response
Body Structure (200)
 Expand all
pagination
object
The pagination object defining the limit, offset, total number of issues, next and previous URL
results
array: object
The list of issues in the current page
Example
List of relevant issues in combination with pagination details

Request
curl -v 'https://developer.api.autodesk.com/construction/issues/v1/projects/:projectId/issues?filter[linkedDocumentUrn]=urn%3Aadsk.wipprod%3Afs.folder%3Aco.rLYHljHURdiG-o4HXOwByg%403' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 10,
    "offset": 100,
    "totalResults": 25
  },
  "results": [
    {
      "id": "3570f222-6c54-4b01-90e6-e701749f0222",
      "containerId": "2220f222-6c54-4b01-90e6-d701748f0222",
      "deleted": false,
      "deletedAt": "2018-07-22T15:05:58.033Z",
      "deletedBy": "A3RGM375QTZ7",
      "displayId": 7,
      "title": "Door missing a screw.",
      "description": "The door is missing a screw. Please fix this",
      "snapshotUrn": "",
      "issueTypeId": "8770f222-6c54-4e01-93e6-e701749f0222",
      "issueSubtypeId": "1370f222-6c54-3a01-93e6-e701749f0222",
      "status": "open",
      "assignedTo": "A3RGM375QTZ7",
      "assignedToType": "user",
      "dueDate": "2018-07-25",
      "startDate": "1982-06-01",
      "locationId": "35de6f24-39f5-4808-ba5f-6cbbe2a858e1",
      "locationDetails": "issue location details",
      "linkedDocuments": [
        {
          "type": "TwoDVectorPushpin",
          "urn": "urn:adsk.wipprod:dm.lineage:0C9edNQuT2SrfoyKQ1Gv_Q",
          "createdBy": "A3RGM375QTZ7",
          "createdAt": "2018-07-22T15:05:58.033Z",
          "createdAtVersion": 1,
          "closedBy": "A3RGM375QTZ7",
          "closedAt": "2018-08-22T15:05:58.033Z",
          "closedAtVersion": 1,
          "details": {
            "viewable": {
              "id": "24820322-7c54-4a01-93e6-e701749f0345",
              "guid": "24820322-7c54-4a01-93e6-e701749f0345",
              "viewableId": "42",
              "name": "3D view of the 3rd floor of the building",
              "is3D": true
            },
            "position": {
              "x": -0.35907751666652,
              "y": 0.23,
              "z": 0.9998
            },
            "objectId": 3,
            "externalId": "4",
            "viewerState": true
          }
        }
      ],
      "links": [
        {}
      ],
      "ownerId": "",
      "rootCauseId": "2370f222-6c54-3a01-93e6-f701772f0222",
      "officialResponse": {},
      "issueTemplateId": "",
      "permittedStatuses": [
        "open"
      ],
      "permittedAttributes": [
        "title"
      ],
      "published": true,
      "permittedActions": [
        "add_comment"
      ],
      "commentCount": 3,
      "attachmentCount": "",
      "openedBy": "A3RGM375QTZ7",
      "openedAt": "2018-07-22T15:05:58.033Z",
      "closedBy": "A3RGM375QTZ7",
      "closedAt": "2018-07-22T15:05:58.033Z",
      "createdBy": "A3RGM375QTZ7",
      "createdAt": "2018-07-22T15:05:58.033Z",
      "updatedBy": "A3RGM375QTZ7",
      "updatedAt": "2018-07-22T15:05:58.033Z",
      "watchers": [
        "A3RGM375QTZ7"
      ],
      "customAttributes": [
        {
          "attributeDefinitionId": "2220f222-6c54-4b01-90e6-d701748f0888",
          "value": "368",
          "type": "numeric",
          "title": "Cost Impact ($)"
        }
      ],
      "gpsCoordinates": {
        "latitude": 35.7795897,
        "longitude": -78.6381787
      },
      "snapshotHasMarkups": false
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Issues
GET	projects/{projectId}/issues/{issueId}
Retrieves detailed information about a single issue. For general information about all the issues in a project, see GET issues.

We support retrieving file-related (pushpin) issues. However, we do not currently support retrieving sheet-related issues from ACC Build Sheets tool.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/issues/v1/projects/{projectId}/issues/{issueId}
Authentication Context	
user context required
Required OAuth Scopes	
data:read
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via a three-legged OAuth flow.
x-ads-region
string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA.

For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

issueId
string: UUID
The unique identifier of the issue. To find the ID, call GET issues.
Response
HTTP Status Code Summary
200
OK
Returns the requested issue
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers. The client SHOULD NOT repeat the request without modifications. The response body may give an indication of what is wrong with the request
403
Forbidden
The request is valid but lacks the necessary permissions.
404
Not Found
The specified resource was not found
Response
Body Structure (200)
 Expand all
id
string: UUID
The unique identifier of the issue.
containerId
string: UUID
Not relevant
deleted
boolean
Indicates whether the issue was deleted. Default value: false.
Deleted issues can only be accessed by specific users. Project members with View and assign to their company and Full visibility permissions can view deleted published and unpublished issues they originally created. Project members with Manage issues or Manage member permissions access can view all published issues that were deleted in a project. In addition, they can see unpublished deleted issues if they are an issue watcher, assignee, or creator.

For more information about deleted issues see the Help documentation.

deletedAt
datetime: ISO 8601
The date and time the issue was deleted, in ISO8601 format. This is only relevant for deleted issues.
deletedBy
string
The Autodesk ID of the user who deleted the issue. This is only relevant for deleted issues.
displayId
int
The chronological user-friendly identifier of the issue.
title
string
The title of the issue. Maximum 100 characters.
description
string
A brief description of the issue and its purpose. Maximum 1000 characters.
snapshotUrn
string
Not relevant
issueTypeId
string: UUID
The unique identifier of the type of the issue.
issueSubtypeId
string: UUID
The unique identifier of the subtype of the issue.
status
enum:string
The current status of the issue.
Possible values: draft, open, pending, in_progress, completed, in_review, not_approved, in_dispute, closed.

For more information about statuses, see the Help documentation.

assignedTo
string
The unique Autodesk ID of the member, company, or role of the current assignee for this issue. Note that if you select an assignee ID, you also need to select a type (assignedToType).
assignedToType
string
The type of the current assignee of this issue. Possible values: user, company, role, null. Note that if you select a type, you also need to select the assignee ID (assignedTo).
dueDate
string
The due date of the issue, in ISO8601 format.
startDate
string
The start date of the issue, in ISO8601 format.
locationId
string: UUID
The unique LBS (Location Breakdown Structure) identifier that relates to the issue.
locationDetails
string
The location related to the issue, provided as plain text. Maximum 250 characters.
linkedDocuments
array: object
Information about the files associated with issues (pushpins).
links
array: object
Not relevant
ownerId
string
Not relevant
rootCauseId
string: UUID
The unique identifier of the type of root cause for the issue.
officialResponse
object
Not relevant
issueTemplateId
string: UUID
Not relevant
permittedStatuses
array: string
A list of statuses accessible to the current user, this is based on the current status of the issue and the user permissions.
Possible Values: open, pending, in_review, closed.

permittedAttributes
array: string
A list of attributes the current user can manipulate in the current context. issueTypeId, linkedDocument, links, ownerId, officialResponse, rootCauseId, snapshotUrn are not applicable.
Possible Values: title, description, issueTypeId, issueSubtypeId, status, assignedTo, assignedToType, dueDate, locationId, locationDetails, linkedDocuments, links, ownerId, rootCauseId, officialResponse, customAttributes, snapshotUrn, startDate, published, deleted, watchers.

published
boolean
States whether the issue is published. Default value: false (e.g. unpublished).
permittedActions
array: string
The list of actions permitted for the user for this issue in its current state.
Note that if a user with View and assign to their company permissions attempts to assign a user from a another company to the issue, it will return an error.

Possible Values: assign_all (can assign another user from another company to the issue), assign_same_company (can only assign another user from the same company to the issue), clear_assignee, delete, add_comment, add_attachment, remove_attachment.

The following values are not relevant: add_attachment, remove_attachment.

commentCount
int
The number of comments in this issue.
attachmentCount
int
Not relevant
openedBy
string
Not relevant
openedAt
datetime: ISO 8601
Not relevant
closedBy
string
The unique identifier of the user who closed the issue.
closedAt
datetime: ISO 8601
The date and time the issue was closed, in ISO8601 format.
createdBy
string
The unique identifier of the user who created the issue.
createdAt
datetime: ISO 8601
The date and time the issue was created, in ISO8601 format.
updatedBy
string
The unique identifier of the user who updated the issue.
updatedAt
datetime: ISO 8601
The date and time the issue was updated, in ISO8601 format.
watchers
array: string
The list of watchers for the issue. To find the name of the watcher, call GET users.
customAttributes
array: object
A list of custom attributes of the specific issue.
gpsCoordinates
object
A GPS Coordinate which represents the geo location of the issue.
snapshotHasMarkups
boolean
Not relevant
Example
Returns the requested issue

Request
curl -v 'https://developer.api.autodesk.com/construction/issues/v1/projects/:projectId/issues/:issueId' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "id": "3570f222-6c54-4b01-90e6-e701749f0222",
  "containerId": "2220f222-6c54-4b01-90e6-d701748f0222",
  "deleted": false,
  "deletedAt": "2018-07-22T15:05:58.033Z",
  "deletedBy": "A3RGM375QTZ7",
  "displayId": 7,
  "title": "Door missing a screw.",
  "description": "The door is missing a screw. Please fix this",
  "snapshotUrn": "",
  "issueTypeId": "8770f222-6c54-4e01-93e6-e701749f0222",
  "issueSubtypeId": "1370f222-6c54-3a01-93e6-e701749f0222",
  "status": "open",
  "assignedTo": "A3RGM375QTZ7",
  "assignedToType": "user",
  "dueDate": "2018-07-25",
  "startDate": "1982-06-01",
  "locationId": "35de6f24-39f5-4808-ba5f-6cbbe2a858e1",
  "locationDetails": "issue location details",
  "linkedDocuments": [
    {
      "type": "TwoDVectorPushpin",
      "urn": "urn:adsk.wipprod:dm.lineage:0C9edNQuT2SrfoyKQ1Gv_Q",
      "createdBy": "A3RGM375QTZ7",
      "createdAt": "2018-07-22T15:05:58.033Z",
      "createdAtVersion": 1,
      "closedBy": "A3RGM375QTZ7",
      "closedAt": "2018-08-22T15:05:58.033Z",
      "closedAtVersion": 1,
      "details": {
        "viewable": {
          "id": "24820322-7c54-4a01-93e6-e701749f0345",
          "guid": "24820322-7c54-4a01-93e6-e701749f0345",
          "viewableId": "42",
          "name": "3D view of the 3rd floor of the building",
          "is3D": true
        },
        "position": {
          "x": -0.35907751666652,
          "y": 0.23,
          "z": 0.9998
        },
        "objectId": 3,
        "externalId": "4",
        "viewerState": true
      }
    }
  ],
  "links": [
    {}
  ],
  "ownerId": "",
  "rootCauseId": "2370f222-6c54-3a01-93e6-f701772f0222",
  "officialResponse": {},
  "issueTemplateId": "",
  "permittedStatuses": [
    "open"
  ],
  "permittedAttributes": [
    "title"
  ],
  "published": true,
  "permittedActions": [
    "add_comment"
  ],
  "commentCount": 3,
  "attachmentCount": "",
  "openedBy": "A3RGM375QTZ7",
  "openedAt": "2018-07-22T15:05:58.033Z",
  "closedBy": "A3RGM375QTZ7",
  "closedAt": "2018-07-22T15:05:58.033Z",
  "createdBy": "A3RGM375QTZ7",
  "createdAt": "2018-07-22T15:05:58.033Z",
  "updatedBy": "A3RGM375QTZ7",
  "updatedAt": "2018-07-22T15:05:58.033Z",
  "watchers": [
    "A3RGM375QTZ7"
  ],
  "customAttributes": [
    {
      "attributeDefinitionId": "2220f222-6c54-4b01-90e6-d701748f0888",
      "value": "368",
      "type": "numeric",
      "title": "Cost Impact ($)"
    }
  ],
  "gpsCoordinates": {
    "latitude": 35.7795897,
    "longitude": -78.6381787
  },
  "snapshotHasMarkups": false
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Issue Comments
GET	projects/{projectId}/issues/{issueId}/comments
Get all the comments for a specific issue.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/issues/v1/projects/{projectId}/issues/{issueId}/comments
Authentication Context	
user context required
Required OAuth Scopes	
data:read
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via a three-legged OAuth flow.
x-ads-region
string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA.

For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

issueId
string: UUID
The unique identifier of the issue. To find the ID, call GET issues.
Request
Query String Parameters
sortBy
array: string
Sort issue comments by specified fields. Separate multiple values with commas. To sort in descending order add a - (minus sign) before the sort criteria. For example: sortBy=createdAt,-updatedAt. Possible values: createdAt, updatedAt, createdBy.
limit
int
Add limit=20 to limit the results count (together with the offset to support pagination).
offset
int
Add offset=20 to get partial results (together with the limit to support pagination).
Response
HTTP Status Code Summary
200
OK
List of comments of the specific requested issue in combination with pagination details
400
Bad Request
Invalid ID supplied
403
Forbidden
The request is valid but lacks the necessary permissions.
404
Not Found
Project not found
500
Internal Server Error
Internal server error
Response
Body Structure (200)
 Expand all
pagination
object
The pagination object.
results
array: object
A list of comments for the specified issue.
Example
List of comments of the specific requested issue in combination with pagination details

Request
curl -v 'https://developer.api.autodesk.com/construction/issues/v1/projects/:projectId/issues/:issueId/comments' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 10,
    "offset": 100,
    "totalResults": 25
  },
  "results": [
    {
      "id": "d26c0adb-bb27-4cec-b3ad-bae5ce5a0b29",
      "body": "Hey Aharon,\nPlease validate that this is even possible before starting work on the issue",
      "createdAt": "2018-07-22T15:05:58.033Z",
      "createdBy": "A3RGM375QTZ7",
      "updatedAt": "",
      "deletedAt": "",
      "clientCreatedAt": "A3RGM375QTZ7",
      "clientUpdatedAt": "2018-07-22T15:05:58.033Z",
      "permittedActions": [
        ""
      ],
      "permittedAttributes": [
        ""
      ]
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Issue Attachments
GET	attachments/:issueId/items
Retrieves all attachments for a specific issue in a project.

For details about retrieving metadata for a specific attachment, see the Retrieve Issue Attachment tutorial.

For details about downloading an attachment, see the Download Issue Attachment tutorial.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/issues/v1/projects/{projectId}/attachments/{issueId}/items
Authentication Context	
user context required
Required OAuth Scopes	
data:read
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via a three-legged OAuth flow.
* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

issueId
string: UUID
The unique identifier of the issue. To find the ID, call GET issues.
Response
HTTP Status Code Summary
200
OK
OK
400
Bad Request
Invalid input
403
Forbidden
The request is valid but lacks the necessary permissions.
404
Not Found
Issue not found
500
Internal Server Error
Internal server error
Response
Body Structure (200)
 Expand all
attachments
array: object
A collection of attachments linked to the issue.
Example
OK

Request
curl -v 'https://developer.api.autodesk.com/construction/issues/v1/projects/:projectId/attachments/:issueId/items' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "attachments": [
    {
      "attachmentId": "aea9f035-b63a-4e46-884d-3016454507e2",
      "displayName": "myfile.pdf",
      "fileName": "aea9f035-b63a-4e46-884d-3016454507e2.pdf",
      "attachmentType": "issue-attachment",
      "storageUrn": "urn:adsk.objects:os.object:wip.dm.prod/2a6d61f2-49df-4d7b.jpg",
      "fileSize": 1000000,
      "fileType": "png",
      "domainEntityId": "20c71442-d5b2-480b-9051-0ba108b62bb9",
      "lineageUrn": "urn:adsk.wipprod:dm.lineage:AeYgDtcTSuqYoyMweWFhhQ",
      "version": 32,
      "versionUrn": "urn:adsk.wipprod:fs.file:vf.1HROnsnfQgq4N0b-nUoGge?version=2",
      "tipVersionUrn": "urn:adsk.wipprod:fs.file:vf.1HROnsnfQgq4N0b-nUoGge?version=2",
      "bubbleUrn": "urn:adsk.objects:os.object:modelderivative/building.rvt",
      "createdBy": "A3RGM375QTZ7",
      "createdOn": "2018-07-22T15:05:58.033Z",
      "modifiedBy": "A3RGM375QTZ7",
      "modifiedOn": "2018-07-22T15:05:58.033Z",
      "deletedBy": "A3RGM375QTZ7",
      "deletedOn": "2018-07-22T15:05:58.033Z",
      "isDeleted": false
    }
  ]
}


Documentation /Markups API (DRAFT) /API Reference
Markups
GET	markups
Retrieves information about all the markups in a project, including details about when they were added and the user who added them.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/issues/v1/containers/:container_id/markups
Authentication Context	
user context required
Required OAuth Scopes	
data:read
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via either a two-legged or three-legged OAuth flow. Note that it will not accept a two-legged token, unless you add the x-user-id header.
x-user-id
string
In a two-legged authentication context, the app has access to all users specified by the administrator in the SaaS integrations UI. By providing this header, the API call will be limited to act on behalf of only the user specified.
Content-Type*
string
Must be application/vnd.api+json.
* Required
Request
URI Parameters
container_id
string
Each project is assigned a container that stores all the markups for the project. To find the ID, see the Retrieve a Container ID tutorial.
Request
Query String Parameters
You can configure the response payload by setting up filter, pagination and sorting parameters. You can also specify which types of data appear in the response.

Filtering follows one of the following formats:

param[<fieldName>]=<matchValue>
param=<matchValue>
filter[target_urn]
string
Retrieves markups associated with the specified drawing. You can specify up to 200 drawings. matchValue is the URN of the drawing in BIM 360 Docs. To find the URN, follow the initial steps in the Download a Document tutorial.
filter[synced_after]
datetime: ISO 8601
Retrieves markups synced after the specified date with BIM 360 Docs. matchValue is the timestamp of date in the following format: YYYY-MM-DDThh:mm:ss.sz.
filter[created_at]
datetime: ISO 8601
Retrieves markups created after the specfied date. matchValue is the timestamp of the date in the following format: YYYY-MM-DDThh:mm:ss.sz.
filter[created_by]
string
Retrieves markups created by the specified user. matchValue is the user’s BIM 360 ID. To verify the ID, see GET users.
filter[status]
enum: string
Retrieves markups with the specified status. Possible values: private, published, archived. Note that it only returns the user’s private markups.
page[limit]
int
matchValue is the number of markups to return in the response payload. Acceptable values: 1-100. Default value: 10. For example, to limit 2 markups per page, use page[limit]=2. For more details, see JSON API Pagination.
page[offset]
int
matchValue is the page number that you want to begin markup results from.
sort
enum: string
Sort the marukups by status, created_at, and updated_at. For example, sort=status. Separate multiple values with commas. To sort in descending order add a - before the sort criteria. For example, sort=-status. For more details, see JSON API Sorting.
fields[markups]
enum: string
Specify which attributes you want to appear in the response. Separate multiple values with commas. For example, fields[markups] = title, description.
include
enum: string
Include additional data about attachments, comments, changesets and the project (container) in the response. For example, links and attributes. Possible values: attachments, comments, changesets, container. For example, include=attachments.
Response
HTTP Status Code Summary
200
OK
The requested resource retrieval or update was successful. The relevant data is in the response body.
400
Bad Request
The parameters of the requested operation are invalid (e.g., an update attempted to set a read-only field).
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
422
Unprocessable Entity
The requested resource creation or update failed due to a validation error. Detailed error information is in the response body.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
data
array:object
meta
object
links
links
Example
Successful Retrieval of Markups Created After a Specified Date by a Specified User (200)

Request
curl -v 'https://developer.api.autodesk.com/issues/v1/containers/d944de3a9110-6d9d-46fa-8a50-cc9a4aa9/markups?filter[created_at]=2015-01-01&filter[created_by]=81YMKF4VRSPQ' \
  -H 'Content-Type: application/vnd.api+json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6Imp3dF9zeW1tZXRyaWNfa2V5In0'
Response
{
  "data": [
    {
      "id": "fc7ba9c77528-75bb-4658-94ae-43594ebc",
      "type": "markups",
      "links": {
        "self": "https://developer.api.autodesk.com/issues/v1/containers/d944de3a9110-6d9d-46fa-8a50-cc9a4aa9/markups/fc7ba9c77528-75bb-4658-94ae-43594ebc"
      },
      "attributes": {
        "created_at": "2015-01-01T00:00:00.000Z",
        "synced_at": "2015-01-01T00:00:00.000Z",
        "updated_at": "2015-01-01T00:00:00.000Z",
        "created_by": "81YMKF4VRSPQ",
        "description": "My First Markup",
        "target_urn": "urn:adsk.wipprod:dm.lineage:lnH0rZHYLd6Y8URnkizisn",
        "target_urn_page": null,
        "collection_urn": null,
        "resource_urns": null,
        "starting_version": 1,
        "close_version": null,
        "closed_at": null,
        "closed_by": null,
        "markup_metadata": null,
        "tags": null,
        "closable": true,
        "status": "open"
      },
      "relationships": {
        "container": {
          "links": {
            "self": "https://developer.api.autodesk.com/issues/v1/containers/d944de3a9110-6d9d-46fa-8a50-cc9a4aa9/markups/fc7ba9c77528-75bb-4658-94ae-43594ebc/relationships/container",
            "related": "https://developer.api.autodesk.com/issues/v1/containers/d944de3a9110-6d9d-46fa-8a50-cc9a4aa9/markups/fc7ba9c77528-75bb-4658-94ae-43594ebc/container"
          }
        }
      }
    },
    {
      "id": "ab6ba9c77528-75bb-4658-94ae-43594cba",
      "type": "markups",
      "links": {
        "self": "https://developer.api.autodesk.com/issues/v1/containers/d944de3a9110-6d9d-46fa-8a50-cc9a4aa9/markups/fc7ba9c77528-75bb-4658-94ae-43594ebc"
      },
      "attributes": {
        "created_at": "2015-01-01T00:00:00.000Z",
        "synced_at": "2015-01-01T00:00:00.000Z",
        "updated_at": "2015-01-01T00:00:00.000Z",
        "created_by": "81YMKF4VRSPQ",
        "description": "My Second Markup",
        "target_urn": "urn:adsk.wipprod:dm.lineage:lnH0rZHYLd6Y8URnkizisn",
        "target_urn_page": null,
        "collection_urn": null,
        "resource_urns": null,
        "starting_version": 1,
        "close_version": null,
        "closed_at": null,
        "closed_by": null,
        "markup_metadata": null,
        "tags": null,
        "closable": true,
        "status": "open"
      },
      "relationships": {
        "container": {
          "links": {
            "self": "https://developer.api.autodesk.com/issues/v1/containers/d944de3a9110-6d9d-46fa-8a50-cc9a4aa9/markups/fc7ba9c77528-75bb-4658-94ae-43594ebc/relationships/container",
            "related": "https://developer.api.autodesk.com/issues/v1/containers/d944de3a9110-6d9d-46fa-8a50-cc9a4aa9/markups/fc7ba9c77528-75bb-4658-94ae-43594ebc/container"
          }
        }
      }
    }
  ],
  "meta": {
    "record_count": 2
  },
  "links": {
    "first": "https://developer.api.autodesk.com/issues/v1/containers/d944de3a9110-6d9d-46fa-8a50-cc9a4aa9/markups?page%5Blimit%5D=5&page%5Boffset%5D=0",
    "previous": "https://developer.api.autodesk.com/issues/v1/containers/d944de3a9110-6d9d-46fa-8a50-cc9a4aa9/markups?page%5Blimit%5D=5&page%5Boffset%5D=5",
    "last": "https://developer.api.autodesk.com/issues/v1/containers/d944de3a9110-6d9d-46fa-8a50-cc9a4aa9/markups?page%5Blimit%5D=5&page%5Boffset%5D=7"
  }
}
