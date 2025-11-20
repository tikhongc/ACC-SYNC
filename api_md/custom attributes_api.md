Documentation /Autodesk Construction Cloud APIs /API Reference
Custom Attributes (beta)
POST	projects/{project_id}/versions:batch-get
Retrieves a list of custom attribute values for multiple BIM 360 Document Management documents. For information about custom attributes, see the Help documentation. This endpoint also retrieves information about a document’s approval status and revision number.

You can either retrieve the custom attributes using the version ID or the item ID. If you use the item ID it returns the custom attributes for the latest (tip) version of the file. For information about finding the version ID and item ID for a document, see the initial steps of the Download File tutorial.

Note that this endpoint only retrieves custom attributes that have been assigned a value. To retrieve the full list of the document’s custom attributes including custom attributes that have not been assigned a value, call GET custom-attribute-definitions.

To assign values to a document’s custom attributes or to clear custom attribute values, call POST custom-attributes:batch-update.

For more details about custom attributes, see the Update Custom Attributes tutorial.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/bim360/docs/v1/projects/:project_id/versions:batch-get
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
Content-Type*
string
Must be application/json
x-user-id
string
In a two-legged authentication context, the app has access to all users specified by the administrator in the SaaS integrations UI. By providing this header, the API call will be limited to act on behalf of only the user specified.
* Required
Request
URI Parameters
project_id
string
The ID of the project. This corresponds to project ID in the Data Management API. To convert a project ID in the Data Management API into a project ID in the BIM 360 API you need to remove the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.
Request
Body Structure
urns*
array: string
A list of version IDs or item IDs. If you use item IDs it retrieves the values for the latest (tip) versions. You can specify up to 50 documents. To find the version ID and item ID of a document follow the initial steps of the Download Files tutorial.
* Required
Response
HTTP Status Code Summary
200
OK
Successful retrieval of versions.
400
Bad Request
The parameters of the requested operation are invalid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The project does not exist.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
results
array: object
The list of results.
errors
array: object
The list of errors.
Example
Successful retrieval of versions.

Request
curl -v 'https://developer.api.autodesk.com/bim360/docs/v1/projects/:project_id/versions:batch-get' \
  -X 'POST' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a' \
  -H 'Content-Type: application/json' \
  -d '{
        "urns": [
          "urn:adsk.wipprod:fs.file:vf.zSoimiozRD6qdgHwfykp_w?version=6",
          "urn:adsk.wipprod:dm.lineage:AS3XD9MzQvu4MakMF-w7vQ"
        ]
      }'
Show Less
Response
{
  "results": [
    {
      "urn": "urn:adsk.wipprod:fs.file:vf.AS3XD9MzQvu4MakMF-w7vQ?version=1",
      "itemUrn": "urn:adsk.wipprod:dm.lineage:AS3XD9MzQvu4MakMF-w7vQ",
      "name": "Oct.pdf",
      "title": "Bin Work",
      "number": "",
      "createTime": "2019-04-18T03:33:36+0000",
      "createUserId": "CGZ5PG7PZMAS",
      "createUserName": "Tom Jerry",
      "lastModifiedTime": "2019-04-18T03:33:36+0000",
      "lastModifiedUserId": "CGZ5PG7PZMAS",
      "lastModifiedUserName": "2019-04-18T03:33:36+0000",
      "storageUrn": "urn:adsk.objects:os.object:wip.dm.prod/c4a75bbc-24eb-41a3-a58b-48e51942222e.pdf",
      "storageSize": 7164826,
      "entityType": "SEED_FILE",
      "revisionNumber": 1,
      "processState": "PROCESSING_COMPLETE",
      "approvalStatus": {
        "label": "Approved w/ comments.",
        "value": "approved"
      },
      "customAttributes": [
        {
          "id": 123,
          "type": "array",
          "name": "Drawing Type",
          "value": "General"
        }
      ]
    }
  ],
  "errors": [
    {
      "urn": "urn:adsk.wipprod:fs.file:vf.zSoimiozRD6qdgHwfykp_w?version=6",
      "code": "ERR_RESOURCE_NOT_EXIST",
      "title": "The resource does not exist",
      "detail": "The resource XXX does not exist."
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Custom Attributes (beta)
GET	projects/{project_id}/folders/{folder_id}/custom-attribute-definitions
Retrieves a complete list of custom attribute definitions for all the documents in a specific folder, including custom attributes that have not been assigned a value, as well as the potential drop-down (array) values.

To assign values to a document’s custom attributes or to clear custom attribute values, call POST custom-attributes:batch-update.

To retrieve the values that were assigned to a document’s custom attributes, call POST versions:batch-get.

For more details about custom attributes, see the Update Custom Attributes tutorial.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/docs/v1/projects/:project_id/folders/:folder_id/custom-attribute-definitions
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
In a two-legged authentication context, the app has access to all users specified by the administrator in the SaaS integrations UI. By providing this header, the API call will be limited to act on behalf of only the user specified.
* Required
Request
URI Parameters
project_id
string: UUID
The ID of the project. This corresponds to the project ID in the Data Management API. To convert a project ID in the Data Management API to a project ID in the BIM 360 API you need to remove the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.
folder_id
string
The URL-encoded ID (URN) of the folder.
For details about how to find the URN, follow the initial steps (1-3) of the Download Files tutorial.

Request
Query String Parameters
limit
int
The number of results to return in the response. Acceptable values: 1-200. Default value: 10. For example, to limit the response to two custom attributes per page, use limit=2.
offset
int
The item number that you want to begin results from. Default value: 0. For example, to begin the results from item three, use offset=3.
Response
HTTP Status Code Summary
200
OK
Successfully retrieved the list of custom attribute definitions.
400
Bad Request
The parameters of the requested operation are invalid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The project or folder does not exist.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
results
array: object
The list of results.
pagination
object
Pagination information when data must be returned page by page.
Example
Successfully retrieved the list of custom attribute definitions.

Request
curl -v 'https://developer.api.autodesk.com/bim360/docs/v1/projects/c0337487-5b66-422b-a284-c273b424af54/folders/urn%3Aadsk.wipprod%3Afs.folder%3Aco.9g7HeA2wRqOxLlgLJ40UGQ/custom-attribute-definitions' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "results": [
    {
      "id": 1001,
      "name": "Drawing Stage",
      "type": "string"
    },
    {
      "id": 1002,
      "name": "Publish Date",
      "type": "date"
    },
    {
      "id": 1003,
      "name": "Drawing Type",
      "type": "array",
      "arrayValues": [
        "Details",
        "General",
        "Plans",
        "Schedules"
      ]
    },
    {
      "id": 1004,
      "name": "Original Number",
      "type": "string"
    }
  ],
  "pagination": {
    "limit": 100,
    "offset": 200,
    "totalResults": 500,
    "previousUrl": "",
    "nextUrl": ""
  }
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Custom Attributes (beta)
POST	projects/{project_id}/folders/{folder_id}/custom-attribute-definitions
Adds a custom attribute to a folder.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/bim360/docs/v1/projects/:project_id/folders/:folder_id/custom-attribute-definitions
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
Content-Type*
string
Must be application/json
x-user-id
string
In a two-legged authentication context, the app has access to all users specified by the administrator in the SaaS integrations UI. By providing this header, the API call will be limited to act on behalf of only the user specified.
* Required
Request
URI Parameters
project_id
string: UUID
The ID of the project. This corresponds to the project ID in the Data Management API. To convert a project ID in the Data Management API to a project ID in the BIM 360 API you need to remove the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.
folder_id
string
The URL-encoded ID (URN) of the folder.
For details about how to find the URN, follow the initial steps (1-3) of the Download Files tutorial.

Request
Body Structure
name*
string
The name of the attribute. It needs to be unique within the folder.
type*
enum:string
The type of attribute. Possible values: string (text field), date, array (drop-list).
arrayValues
array: string
A list of possible values for the attribute. Only relevant for drop-list attributes.
* Required
Response
HTTP Status Code Summary
201
Created
Successfully added a custom attribute.
400
Bad Request
The parameters of the requested operation are invalid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The project or folder does not exist.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (201)
id
int
The ID of the attribute.
name
string
The name of the attribute.
type
enum:string
The type of attribute. Possible values: string (text field), date, array (drop-list).
arrayValues
array: string
A list of possible values for the attribute. Only relevant for drop-list attributes.
Example
Successfully added a custom attribute.

Request
curl -v 'https://developer.api.autodesk.com/bim360/docs/v1/projects/c0337487-5b66-422b-a284-c273b424af54/folders/urn%3Aadsk.wipprod%3Afs.folder%3Aco.9g7HeA2wRqOxLlgLJ40UGQ/custom-attribute-definitions' \
  -X 'POST' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a' \
  -H 'Content-Type: application/json' \
  -d '{
        "name": "Drawing Type",
        "type": "array",
        "arrayValues": [
          "Details",
          "General",
          "Plans",
          "Schedules"
        ]
      }'
Show Less
Response
{
  "id": 123,
  "name": "Drawing Type",
  "type": "array",
  "arrayValues": [
    "Details",
    "General",
    "Plans",
    "Schedules"
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Custom Attributes (beta)
POST	projects/{project_id}/versions/{version_id}/custom-attributes:batch-update
Assigns values to custom attributes for multiple documents. This endpoint also clears custom attribute values.

For information about custom attributes, see the Help documentation.

To retrieve values that were assigned to a document’s custom attributes, call POST versions:batch-get.

To retrieve the full list of the document’s custom attributes including custom attributes that have not been assigned a value, call GET custom-attribute-definitions.

For more details about custom attributes, see the Update Custom Attributes tutorial.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/bim360/docs/v1/projects/:project_id/versions/:version_id/custom-attributes:batch-update
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
Content-Type*
string
Must be application/json
x-user-id
string
In a two-legged authentication context, the app has access to all users specified by the administrator in the SaaS integrations UI. By providing this header, the API call will be limited to act on behalf of only the user specified.
* Required
Request
URI Parameters
project_id
string: UUID
The ID of the project. This corresponds to the project ID in the Data Management API. To convert a project ID in the Data Management API to a project ID in the BIM 360 API you need to remove the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.
version_id
string
The URL-encoded ID (URN) of the version. To find the version ID of a document follow the initial steps of the Download Files tutorial.
Request
Body Structure
id*
string
The ID of the custom attribute. To find the ID, call GET custom-attribute-definitions.
value*
string
The value of the custom attribute. If you are assigning a value to a drop-list attribute, call GET custom-attribute-definitions to retrieve a list of possible values. If you are clearing a custom attribute value, assign a null value to the attribute.
For text field (string) attributes, the max length is 255.
Date attributes need to be compliant with ISO8601. Milliseconds are discarded.
* Required
Response
HTTP Status Code Summary
200
OK
Successfully updated the custom attribute values.
400
Bad Request
The parameters of the requested operation are invalid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The project or version does not exist.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
results
array: object
The list of results.
Example
Successfully updated the custom attribute values.

Request
curl -v 'https://developer.api.autodesk.com/bim360/docs/v1/projects/c0337487-5b66-422b-a284-c273b424af54/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.AS3XD9MzQvu4MakMF-w7vQ%3Fversion%3D1/custom-attributes:batch-update' \
  -X 'POST' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a' \
  -H 'Content-Type: application/json' \
  -d '[
        {
          "id": 1001,
          "value": "checked"
        },
        {
          "id": 1002,
          "value": "2020-03-31T16:00:00.000Z"
        },
        {
          "id": 1003,
          "value": "v2"
        }
      ]'
Show Less
Response
{
  "results": [
    {
      "id": 1001,
      "name": "column1",
      "type": "string",
      "value": "checked"
    },
    {
      "id": 1002,
      "name": "column2",
      "type": "date",
      "value": "2020-03-31T16:00:00.000Z"
    },
    {
      "id": 1003,
      "name": "column3",
      "type": "array",
      "value": "v2"
    },
    {
      "id": 1004,
      "name": "column4",
      "type": "string",
      "value": "anything"
    }
  ]
}