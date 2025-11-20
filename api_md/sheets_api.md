Documentation /Autodesk Construction Cloud APIs /API Reference
Version Sets
GET	projects/{projectId}/version-sets
Retrieves a list of version sets.

To get a list of sheets that are associated with a version set, call GET sheets with the filter[versionSetId].

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/sheets/v1/projects/{projectId}/version-sets
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
The ID of the user on whose behalf the API request is made. This header is optional when using a 2-legged OAuth2, but required if using 2-legged OAuth2 with user impersonation.
When using 2-legged OAuth2 without user impersonation, your app has access to all users defined by the administrator in the SaaS integrations UI. However, when user impersonation is enabled, the API call is restricted to act only on behalf of the specified user. This header is not relevant for 3-legged OAuth2.

You can use either the user’s ACC ID (id), or their Autodesk ID (autodeskId).

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project. Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can use a project ID either with a “b.” prefix or without a “b.” prefix. For instance, a project ID of “b.a4be0c34a-4ab7” can also be referred to as “a4be0c34a-4ab7”.
Request
Query String Parameters
offset
int
The starting point for the results, specified by item number. The default value is 0. For example, use offset=3 to start the results from the third item.
limit
int
The maximum number of results to return per page. The default is 200.
sort
string
Sort the version sets by issuanceDate or name. You need to add whether to sort in ascending (asc) or descending (desc) order. For example, sort=issuanceDate desc.
collectionId
string
Filter by sheet collection. If not provided, only results in the ungrouped collection are returned.
Possible values:

The UUID of an existing collection: Returns only the results within that collection.
* Returns results from all collections.
Response
HTTP Status Code Summary
200
OK
Successfully retrieved the list of version sets.
400
Bad Request
The parameters of the requested operation are invalid.
403
Forbidden
The user or client represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource cannot be found.
429
Too Many Requests
The server has received too many requests.
500
Internal Server Error
An unexpected error occurred on the server.
Response
Body Structure (200)
 Expand all
results
array: object
The list of results.
pagination
object
Pagination information for paged data.
Example
Successfully retrieved the list of version sets.

Request
curl -v 'https://developer.api.autodesk.com/construction/sheets/v1/projects/9ba6681e-1952-4d54-aac4-9de6d9858dd4/version-sets?limit=100&sort=issuanceDate desc' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "results": [
    {
      "id": "7c2ecde0-2406-49f9-9199-50176848a0b7",
      "name": "one set",
      "issuanceDate": "2021-07-01",
      "createdAt": "2021-07-01T05:21:05.391Z",
      "createdBy": "45GPJ4KAX789",
      "createdByName": "John Smith",
      "updatedAt": "2021-07-01T05:21:05.391Z",
      "updatedBy": "45GPJ4KAX789",
      "updatedByName": "John Smith",
      "collection": {
        "id": "619ef887-974f-45e4-9775-461e6a62d784",
        "name": "Group 1"
      }
    }
  ],
  "pagination": {
    "limit": 100,
    "offset": 0,
    "previousUrl": "",
    "nextUrl": "",
    "totalResults": 1
  }

  Documentation /Autodesk Construction Cloud APIs /API Reference
Version Sets
PATCH	projects/{projectId}/version-sets/{versionSetId}
Updates a version set.

To get a list of sheets that are associated with a version set, call GET sheets with the version set ID filter (filter[versionSetId]).

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
PATCH	https://developer.api.autodesk.com/construction/sheets/v1/projects/{projectId}/version-sets/{versionSetId}
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
The ID of the user on whose behalf the API request is made. This header is optional when using a 2-legged OAuth2, but required if using 2-legged OAuth2 with user impersonation.
When using 2-legged OAuth2 without user impersonation, your app has access to all users defined by the administrator in the SaaS integrations UI. However, when user impersonation is enabled, the API call is restricted to act only on behalf of the specified user. This header is not relevant for 3-legged OAuth2.

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
versionSetId
string
The ID of the version set. To find the version set ID, call GET version-sets.
Request
Body Structure
name
string
The name of the version set.
The max length is 255.
Should not be space only.
These handlings will be applied to the name before using it to create version set:

Spaces at the end or beginning will be removed.
Continuous spaces inside will be reduced to one.
Max length: 255

issuanceDate
datetime: ISO 8601
The issuance date of the version set, in ISO-8601 date format (YYYY-MM-DD).
Response
HTTP Status Code Summary
200
OK
Successfully updated the version set.
400
Bad Request
The parameters of the requested operation are invalid.
403
Forbidden
The user or client represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource cannot be found.
409
Conflict
The request could not be completed due to a conflict with the current state of the target resource.
429
Too Many Requests
The server has received too many requests.
500
Internal Server Error
An unexpected error occurred on the server.
Response
Body Structure (200)
 Expand all
id
string: UUID
The ID of the version set.
name
string
The name of the version set.
issuanceDate
datetime: ISO 8601
The issuance date of the version set, in ISO-8601 date format (YYYY-MM-DD).
createdAt
datetime: ISO 8601
The time when the version set was created, in ISO-8601 format (YYYY-MM-DDTHH:mm:ss.SSSZ).
createdBy
string
The ID of the user who created the version set.
createdByName
string
The name of the user who created the version set.
updatedAt
datetime: ISO 8601
The time when the version set was last updated, in ISO-8601 format (YYYY-MM-DDTHH:mm:ss.SSSZ).
updatedBy
string
The ID of the user who last updated the version set.
updatedByName
string
The name of the user who last updated the version set.
collection
object
The collection object, if assigned. If no collection is assigned, this value is null.
Example
Successfully updated the version set.

Request
curl -v 'https://developer.api.autodesk.com/construction/sheets/v1/projects/9ba6681e-1952-4d54-aac4-9de6d9858dd4/version-sets/7c2ecde0-2406-49f9-9199-50176848a0b7' \
  -X 'PATCH' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a' \
  -H 'Content-Type: application/json' \
  -d '{
        "name": "one set",
        "issuanceDate": "2021-07-01"
      }'
Show Less
Response
{
  "id": "7c2ecde0-2406-49f9-9199-50176848a0b7",
  "name": "one set",
  "issuanceDate": "2021-07-01",
  "createdAt": "2021-07-01T05:21:05.391Z",
  "createdBy": "45GPJ4KAX789",
  "createdByName": "John Smith",
  "updatedAt": "2021-07-01T05:21:05.391Z",
  "updatedBy": "45GPJ4KAX789",
  "updatedByName": "John Smith",
  "collection": {
    "id": "619ef887-974f-45e4-9775-461e6a62d784",
    "name": "Group 1"
  }
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Version Sets
POST	projects/{projectId}/version-sets:batch-get
Retrieves a list of version sets.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/construction/sheets/v1/projects/{projectId}/version-sets:batch-get
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
The ID of the user on whose behalf the API request is made. This header is optional when using a 2-legged OAuth2, but required if using 2-legged OAuth2 with user impersonation.
When using 2-legged OAuth2 without user impersonation, your app has access to all users defined by the administrator in the SaaS integrations UI. However, when user impersonation is enabled, the API call is restricted to act only on behalf of the specified user. This header is not relevant for 3-legged OAuth2.

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
ids
array: string
The IDs of the version sets to retrieve.
The max number of items is 200.
Response
HTTP Status Code Summary
200
OK
Successfully retrieved the list of version sets.
400
Bad Request
The parameters of the requested operation are invalid.
403
Forbidden
The user or client represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource cannot be found.
429
Too Many Requests
The server has received too many requests.
500
Internal Server Error
An unexpected error occurred on the server.
Response
Body Structure (200)
 Expand all
results
array: object
The list of results.
Example
Successfully retrieved the list of version sets.

Request
curl -v 'https://developer.api.autodesk.com/construction/sheets/v1/projects/9ba6681e-1952-4d54-aac4-9de6d9858dd4/version-sets:batch-get' \
  -X 'POST' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a' \
  -H 'Content-Type: application/json' \
  -d '{
        "ids": [
          "7c2ecde0-2406-49f9-9199-50176848a0b7"
        ]
      }'
Show Less
Response
{
  "results": [
    {
      "id": "7c2ecde0-2406-49f9-9199-50176848a0b7",
      "name": "one set",
      "issuanceDate": "2021-07-01",
      "createdAt": "2021-07-01T05:21:05.391Z",
      "createdBy": "45GPJ4KAX789",
      "createdByName": "John Smith",
      "updatedAt": "2021-07-01T05:21:05.391Z",
      "updatedBy": "45GPJ4KAX789",
      "updatedByName": "John Smith",
      "collection": {
        "id": "619ef887-974f-45e4-9775-461e6a62d784",
        "name": "Group 1"
      }
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Uploads
GET	projects/{projectId}/uploads
Checks the processing status of all the uploaded files in the project.

For more details about uploading sheets, see the Upload Sheets tutorial.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/sheets/v1/projects/{projectId}/uploads
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
The ID of the user on whose behalf the API request is made. This header is optional when using a 2-legged OAuth2, but required if using 2-legged OAuth2 with user impersonation.
When using 2-legged OAuth2 without user impersonation, your app has access to all users defined by the administrator in the SaaS integrations UI. However, when user impersonation is enabled, the API call is restricted to act only on behalf of the specified user. This header is not relevant for 3-legged OAuth2.

You can use either the user’s ACC ID (id), or their Autodesk ID (autodeskId).

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project. Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can use a project ID either with a “b.” prefix or without a “b.” prefix. For instance, a project ID of “b.a4be0c34a-4ab7” can also be referred to as “a4be0c34a-4ab7”.
Request
Query String Parameters
offset
int
The starting point for the results, specified by item number. The default value is 0. For example, use offset=3 to start the results from the third item.
limit
int
The number of results to return in the response.
sort
string
Sort the uploads by createdAt or issuanceDate. You need to add whether to sort in ascending (asc) or descending (desc) order. For example, sort=issuanceDate desc.
Response
HTTP Status Code Summary
200
OK
Successfully retrieved a list of uploads.
400
Bad Request
The parameters of the requested operation are invalid.
403
Forbidden
The user or client represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource cannot be found.
429
Too Many Requests
The server has received too many requests.
500
Internal Server Error
An unexpected error occurred on the server.
Response
Body Structure (200)
 Expand all
results
array: object
The list of results.
pagination
object
Pagination information for paged data.
Example
Successfully retrieved a list of uploads.

Request
curl -v 'https://developer.api.autodesk.com/construction/sheets/v1/projects/9ba6681e-1952-4d54-aac4-9de6d9858dd4/uploads?sort=createdAt desc' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "results": [
    {
      "id": "5cb5d9da-060e-421e-bca9-97dd8b5cd800",
      "versionSetId": "7c2ecde0-2406-49f9-9199-50176848a0b7",
      "status": "PENDING",
      "createdAt": "2021-07-01T05:21:05.391Z",
      "createdBy": "45GPJ4KAX789",
      "createdByName": "John Smith",
      "updatedAt": "2021-07-01T05:21:05.391Z",
      "updatedBy": "45GPJ4KAX789",
      "updatedByName": "John Smith",
      "publishedAt": "2021-07-01T05:21:05.391Z",
      "publishedBy": "45GPJ4KAX789",
      "publishedByName": "John Smith",
      "publishedCount": 1
    }
  ],
  "pagination": {
    "limit": 100,
    "offset": 0,
    "previousUrl": "",
    "nextUrl": "",
    "totalResults": 1
  }
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Uploads
GET	projects/{projectId}/uploads/{uploadId}
Checks the processing status of a specific uploaded file.

For more details about uploading sheets, see the Upload Sheets tutorial.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/sheets/v1/projects/{projectId}/uploads/{uploadId}
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
The ID of the user on whose behalf the API request is made. This header is optional when using a 2-legged OAuth2, but required if using 2-legged OAuth2 with user impersonation.
When using 2-legged OAuth2 without user impersonation, your app has access to all users defined by the administrator in the SaaS integrations UI. However, when user impersonation is enabled, the API call is restricted to act only on behalf of the specified user. This header is not relevant for 3-legged OAuth2.

You can use either the user’s ACC ID (id), or their Autodesk ID (autodeskId).

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project. Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can use a project ID either with a “b.” prefix or without a “b.” prefix. For instance, a project ID of “b.a4be0c34a-4ab7” can also be referred to as “a4be0c34a-4ab7”.
uploadId
string
The ID of the upload. The upload ID is generated when you create an upload object.
Response
HTTP Status Code Summary
200
OK
Successfully retrieved an upload.
400
Bad Request
The parameters of the requested operation are invalid.
403
Forbidden
The user or client represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource cannot be found.
429
Too Many Requests
The server has received too many requests.
500
Internal Server Error
An unexpected error occurred on the server.
Response
Body Structure (200)
id
string: UUID
The ID of the upload.
versionSetId
string: UUID
The ID of the version set where the upload creates sheets to.
status
enum:string
The status of the upload. Possible values:
PENDING: the uploaded files are waiting for to be processed.
PROCESSING: the uploaded files are being processed.
IN_REVIEW: the file upload process is complete. The sheets are ready for review. You can now call GET review-sheets, PATCH review-sheets, or POST review-sheets:publish.
FAILED: the file upload process failed. One of the final status of an upload.
UPDATING_VERSION_SET: the target version set is being updated.
PUBLISHING: the review sheets are being published.
PUBLISHED: the review sheets have been published.
createdAt
datetime: ISO 8601
The time when the upload was created, in ISO-8601 format (YYYY-MM-DDTHH:mm:ss.SSSZ).
createdBy
string
The ID of the user who created the upload.
createdByName
string
The name of the user who created the upload.
updatedAt
datetime: ISO 8601
The time when the upload was last updated, in ISO-8601 format (YYYY-MM-DDTHH:mm:ss.SSSZ).
updatedBy
string
The ID of the user who last updated the upload.
updatedByName
string
The name of the user who last updated the upload.
publishedAt
datetime: ISO 8601
The time when all the review sheets of the upload were published, in ISO-8601 format (YYYY-MM-DDTHH:mm:ss.SSSZ).
publishedBy
string
The ID of the user who published all the review sheets of the upload.
publishedByName
string
The name of the user who published all the review sheets of the upload.
publishedCount
int
The number of files that have been published by the upload.
Example
Successfully retrieved an upload.

Request
curl -v 'https://developer.api.autodesk.com/construction/sheets/v1/projects/9ba6681e-1952-4d54-aac4-9de6d9858dd4/uploads/5cb5d9da-060e-421e-bca9-97dd8b5cd800' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "id": "5cb5d9da-060e-421e-bca9-97dd8b5cd800",
  "versionSetId": "7c2ecde0-2406-49f9-9199-50176848a0b7",
  "status": "PENDING",
  "createdAt": "2021-07-01T05:21:05.391Z",
  "createdBy": "45GPJ4KAX789",
  "createdByName": "John Smith",
  "updatedAt": "2021-07-01T05:21:05.391Z",
  "updatedBy": "45GPJ4KAX789",
  "updatedByName": "John Smith",
  "publishedAt": "2021-07-01T05:21:05.391Z",
  "publishedBy": "45GPJ4KAX789",
  "publishedByName": "John Smith",
  "publishedCount": 1
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Uploads
GET	projects/{projectId}/uploads/{uploadId}/review-sheets
Retrieves a list of review sheets. This endpoint is typically used during the process of uploading files to the ACC Sheets tool. It enables you to review the sheets that you uploaded before publishing them. For more details, see the Upload Sheets tutorial.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/sheets/v1/projects/{projectId}/uploads/{uploadId}/review-sheets
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
The ID of the user on whose behalf the API request is made. This header is optional when using a 2-legged OAuth2, but required if using 2-legged OAuth2 with user impersonation.
When using 2-legged OAuth2 without user impersonation, your app has access to all users defined by the administrator in the SaaS integrations UI. However, when user impersonation is enabled, the API call is restricted to act only on behalf of the specified user. This header is not relevant for 3-legged OAuth2.

You can use either the user’s ACC ID (id), or their Autodesk ID (autodeskId).

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project. Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can use a project ID either with a “b.” prefix or without a “b.” prefix. For instance, a project ID of “b.a4be0c34a-4ab7” can also be referred to as “a4be0c34a-4ab7”.
uploadId
string
The ID of the upload. The upload ID is generated when you create an upload object.
Request
Query String Parameters
offset
int
The starting point for the results, specified by item number. The default value is 0. For example, use offset=3 to start the results from the third item.
limit
int
The number of results to return in the response.
Response
HTTP Status Code Summary
200
OK
Successfully retrieved the list of review sheets.
400
Bad Request
The parameters of the requested operation are invalid.
403
Forbidden
The user or client represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource cannot be found.
429
Too Many Requests
The server has received too many requests.
500
Internal Server Error
An unexpected error occurred on the server.
Response
Body Structure (200)
 Expand all
results
array: object
The list of results.
pagination
object
Pagination information for paged data.
Example
Successfully retrieved the list of review sheets.

Request
curl -v 'https://developer.api.autodesk.com/construction/sheets/v1/projects/9ba6681e-1952-4d54-aac4-9de6d9858dd4/uploads/5cb5d9da-060e-421e-bca9-97dd8b5cd800/review-sheets' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "results": [
    {
      "id": "0d7a5883-1694-3078-a06d-ad24413f8b06",
      "page": 1,
      "fileName": "example.pdf",
      "number": "A-01",
      "title": "Floor One",
      "deleted": false,
      "tags": [
        "april",
        "floor"
      ],
      "rotation": 0,
      "processingState": "READY"
    }
  ],
  "pagination": {
    "limit": 100,
    "offset": 0,
    "previousUrl": "",
    "nextUrl": "",
    "totalResults": 1
  }
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Uploads
POST	projects/{projectId}/uploads/{uploadId}/thumbnails:batch-get
Retrieves a list of thumbnails for the specified review sheets.

Note that the thumbnails are stored in AWS S3 and will expire after 30 days (the count starts from the time that the upload was created). When the thumbnails expire you will get a 404 (NotFound) error when you try to access the S3 signed URL.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/construction/sheets/v1/projects/{projectId}/uploads/{uploadId}/thumbnails:batch-get
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
The ID of the user on whose behalf the API request is made. This header is optional when using a 2-legged OAuth2, but required if using 2-legged OAuth2 with user impersonation.
When using 2-legged OAuth2 without user impersonation, your app has access to all users defined by the administrator in the SaaS integrations UI. However, when user impersonation is enabled, the API call is restricted to act only on behalf of the specified user. This header is not relevant for 3-legged OAuth2.

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
uploadId
string
The ID of the upload. The upload ID is generated when you create an upload object.
Request
Body Structure
reviewSheetIds*
array: string
The IDs of the review sheets you want to get the thumbnails from. To find the review sheet IDs, call GET review-sheets.
The max number of items is 100.
type*
enum:string
The size type of the thumbnails. Possible values:
big: the max size will be 512 pixels.
small: the max size will be 256 pixels.
tiny: the max size will be 64 pixels.
* Required
Response
HTTP Status Code Summary
200
OK
Successfully retrieved the thumbnails.
400
Bad Request
The parameters of the requested operation are invalid.
403
Forbidden
The user or client represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource cannot be found.
429
Too Many Requests
The server has received too many requests.
500
Internal Server Error
An unexpected error occurred on the server.
Response
Body Structure (200)
 Expand all
results
array: object
The list of results.
Example
Successfully retrieved the thumbnails.

Request
curl -v 'https://developer.api.autodesk.com/construction/sheets/v1/projects/9ba6681e-1952-4d54-aac4-9de6d9858dd4/uploads/5cb5d9da-060e-421e-bca9-97dd8b5cd800/thumbnails:batch-get' \
  -X 'POST' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a' \
  -H 'Content-Type: application/json' \
  -d '{
        "reviewSheetIds": [
          "0d7a5883-1694-3078-a06d-ad24413f8b06"
        ],
        "type": "big"
      }'
Show Less
Response
{
  "results": [
    {
      "reviewSheetId": "0d7a5883-1694-3078-a06d-ad24413f8b06",
      "size": [
        512,
        256
      ],
      "signedUrl": "https://s3.us-east-1.amazonaws.com/rnd-shredder-buckets-sheetprocessing-1elowz1cchtl4/6e2cc934-709b-4f2e-81f8-727ab9a6c799.png?AWSAccessKeyId=ASIAZ6NF4RTV3JEBINXH&Signature=enZvg1McCp1GK%2BOL0ufG2aaCoAc%3D&x-amz-security-token=FwoGZXIvYXdzEAsaDEbuDLTNK4D8HPMr2yKtATOjYhoq23UUeFwdbTZ2T463lprZrvjK5eIdQ0o6OpyHkRDK%2FwEe5Dw67P9qyGc97q3Kw6zKlva3j88TENeN%2BJY0MOEYglhTrkgj3KnelyNm8ymhXwpmZZaa94ezy9Se707MvQsWueHQnzy%2BR%2BycRzE84C%2FxjlRAoG5REonzsHylkS8NJzvmbAwV9SxuUD4xXgHnnjfbnWbwXk8xf31v%2BkyHvoGb0EFQz4WoU9%2FvKOm12IEGMi2I6v0durq5t7Hl81SbiAMXDtzA%2F4tgFhnct9pn9kEqVrUDGzGntnW%2BV5GfUlM%3D&Expires=1614162667"
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Sheets
GET	projects/{projectId}/sheets
Retrieves information about the sheets in a project.

By default, this endpoint only returns sheets with the newest issuance date (this includes future issuance dates).

To return all the sheets in a project, set the currentOnly filter to false.

To return sheets from a specific version set, use the version set ID filter (filter[versionSetId]).

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/sheets/v1/projects/{projectId}/sheets
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
The ID of the user on whose behalf the API request is made. This header is optional when using a 2-legged OAuth2, but required if using 2-legged OAuth2 with user impersonation.
When using 2-legged OAuth2 without user impersonation, your app has access to all users defined by the administrator in the SaaS integrations UI. However, when user impersonation is enabled, the API call is restricted to act only on behalf of the specified user. This header is not relevant for 3-legged OAuth2.

You can use either the user’s ACC ID (id), or their Autodesk ID (autodeskId).

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project. Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can use a project ID either with a “b.” prefix or without a “b.” prefix. For instance, a project ID of “b.a4be0c34a-4ab7” can also be referred to as “a4be0c34a-4ab7”.
Request
Query String Parameters
currentOnly
boolean
true to only return versions of the sheets with the newest issuance date (this includes future issuance dates). This is only relevant if you uploaded multiple versions of the same sheet that were assigned the same number identifier. If you do not assign a value to the version set ID filter (filter[versionSetId]) this defaults to true.
false to return all sheets in the project.
If you specify a value for the version set ID filter (filter[versionSetId]) this defaults to false. If you do not specify a version set, the default is true.

filter[versionSetId]
string
Filter sheets by the version set ID. If you assign a value to this filter, currentOnly defaults to false. If you do not assign a value, currentOnly default to true.
filter[tags]
string
Filter sheets by tags. You can filter by multiple tags. For example, filter[tags]=architecture&filter[tags]=structure returns sheets that include both architecture and structure tags.
Use filter[tags]=__UNTAGGED to only return sheets without any tags.

fields
string
Specify which attributes you want to appear in the response. You can specify multiple attributes. For example, to only return the sheet ID and sheet number in the response, use fields=id&fields=number.
searchText
string
Search for sheets with the specified text. The API only searches in the number and title attributes. You can specify a string or part of a string. The search is case sensitive. You can only use one search string per call. For example, searchText=kitchen.
withAllTags
boolean
true to return sheets that contain all search tags.
false to return sheets that contain at least one tag.
If filter[tags]=__UNTAGGED is already in query parameters, withAllTags does not work.

isDeleted
boolean
true to only return deleted sheets.
false to only return non-deleted sheets.
The default value is false. You cannot retrieve both deleted and non-deleted sheets in one call.

offset
int
The starting point for the results, specified by item number. The default value is 0. For example, use offset=3 to start the results from the third item.
limit
int
The number of results to return in the response. Acceptable values: 1-100. Default value: 100.
collectionId
string
Filter by sheet collection. If not provided, only results in the ungrouped collection are returned.
Possible values:

The UUID of an existing collection: Returns only the results within that collection.
* Returns results from all collections.
Response
HTTP Status Code Summary
200
OK
Successfully retrieved the list of sheets.
400
Bad Request
The parameters of the requested operation are invalid.
403
Forbidden
The user or client represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource cannot be found.
429
Too Many Requests
The server has received too many requests.
500
Internal Server Error
An unexpected error occurred on the server.
Response
Body Structure (200)
 Expand all
results
array: object
The list of results.
pagination
object
Pagination information for paged data.
Example
Successfully retrieved the list of sheets.

Request
curl -v 'https://developer.api.autodesk.com/construction/sheets/v1/projects/9ba6681e-1952-4d54-aac4-9de6d9858dd4/sheets?currentOnly=true&filter[versionSetId]=7c2ecde0-2406-49f9-9199-50176848a0b7&filter[tags]=floor' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "results": [
    {
      "id": "0d7a5883-1694-3078-a06d-ad24413f8b06",
      "number": "A-01",
      "versionSet": {
        "id": "7c2ecde0-2406-49f9-9199-50176848a0b7",
        "name": "one set",
        "issuanceDate": "2021-07-01",
        "deleted": false
      },
      "createdAt": "2021-07-01T05:21:05.391Z",
      "createdBy": "45GPJ4KAX789",
      "createdByName": "John Smith",
      "updatedAt": "2021-07-01T05:21:05.391Z",
      "updatedBy": "45GPJ4KAX789",
      "updatedByName": "John Smith",
      "title": "Floor One",
      "uploadFileName": "example.pdf",
      "uploadId": "5cb5d9da-060e-421e-bca9-97dd8b5cd800",
      "tags": [
        "april",
        "floor"
      ],
      "paperSize": [
        1000,
        600
      ],
      "isCurrent": true,
      "deleted": false,
      "deletedAt": "",
      "deletedBy": "",
      "deletedByName": "",
      "viewable": {
        "urn": "urn:adsk.bimdocs:seed:207edb73-69c2-43d2-ba0e-e2ffe9fdcb56",
        "guid": "cc3eb847-737f-3408-bdbd-e2628a02b8de"
      },
      "collection": {
        "id": "619ef887-974f-45e4-9775-461e6a62d784",
        "name": "Group 1"
      }
    }
  ],
  "pagination": {
    "limit": 100,
    "offset": 0,
    "previousUrl": "",
    "nextUrl": "",
    "totalResults": 1
  }
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Sheets
POST	projects/{projectId}/sheets:batch-get
Retrieves a list of sheets by IDs.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/construction/sheets/v1/projects/{projectId}/sheets:batch-get
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
The ID of the user on whose behalf the API request is made. This header is optional when using a 2-legged OAuth2, but required if using 2-legged OAuth2 with user impersonation.
When using 2-legged OAuth2 without user impersonation, your app has access to all users defined by the administrator in the SaaS integrations UI. However, when user impersonation is enabled, the API call is restricted to act only on behalf of the specified user. This header is not relevant for 3-legged OAuth2.

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
ids*
array: string
The IDs of the sheets to retrieve.
The max number of items is 200.
* Required
Response
HTTP Status Code Summary
200
OK
Successfully retrieved the list of sheets.
400
Bad Request
The parameters of the requested operation are invalid.
403
Forbidden
The user or client represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource cannot be found.
429
Too Many Requests
The server has received too many requests.
500
Internal Server Error
An unexpected error occurred on the server.
Response
Body Structure (200)
 Expand all
results
array: object
The list of results.
Example
Successfully retrieved the list of sheets.

Request
curl -v 'https://developer.api.autodesk.com/construction/sheets/v1/projects/9ba6681e-1952-4d54-aac4-9de6d9858dd4/sheets:batch-get' \
  -X 'POST' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a' \
  -H 'Content-Type: application/json' \
  -d '{
        "ids": [
          "0d7a5883-1694-3078-a06d-ad24413f8b06"
        ]
      }'
Show More
Response
{
  "results": [
    {
      "id": "0d7a5883-1694-3078-a06d-ad24413f8b06",
      "number": "A-01",
      "versionSet": {
        "id": "7c2ecde0-2406-49f9-9199-50176848a0b7",
        "name": "one set",
        "issuanceDate": "2021-07-01",
        "deleted": false
      },
      "createdAt": "2021-07-01T05:21:05.391Z",
      "createdBy": "45GPJ4KAX789",
      "createdByName": "John Smith",
      "updatedAt": "2021-07-01T05:21:05.391Z",
      "updatedBy": "45GPJ4KAX789",
      "updatedByName": "John Smith",
      "title": "Floor One",
      "uploadFileName": "example.pdf",
      "uploadId": "5cb5d9da-060e-421e-bca9-97dd8b5cd800",
      "tags": [
        "april",
        "floor"
      ],
      "paperSize": [
        1000,
        600
      ],
      "isCurrent": true,
      "deleted": false,
      "deletedAt": "",
      "deletedBy": "",
      "deletedByName": "",
      "viewable": {
        "urn": "urn:adsk.bimdocs:seed:207edb73-69c2-43d2-ba0e-e2ffe9fdcb56",
        "guid": "cc3eb847-737f-3408-bdbd-e2628a02b8de"
      },
      "collection": {
        "id": "619ef887-974f-45e4-9775-461e6a62d784",
        "name": "Group 1"
      }
    }
  ]
}

POST	projects/{projectId}/sheets:batch-restore
Restores deleted sheets. The sheet is restored to the version set it was associated with when it was deleted.

Note that sheet numbers need to be unique within a version set. If you try to restore a sheet to a version set that includes an existing sheet with the same number, it will not restore the sheet. The errors object in the response gives information about unrestored sheets.

To delete sheets, call POST sheets:batch-delete.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/construction/sheets/v1/projects/{projectId}/sheets:batch-restore
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
The ID of the user on whose behalf the API request is made. This header is optional when using a 2-legged OAuth2, but required if using 2-legged OAuth2 with user impersonation.
When using 2-legged OAuth2 without user impersonation, your app has access to all users defined by the administrator in the SaaS integrations UI. However, when user impersonation is enabled, the API call is restricted to act only on behalf of the specified user. This header is not relevant for 3-legged OAuth2.

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
ids*
array: string
The IDs of the sheets to restore. To find the IDs of deleted sheets you want to restore, call GET sheets using the isDeleted=true filter.
The max number of items is 200.
* Required
Response
HTTP Status Code Summary
200
OK
Successfully restored sheets.
400
Bad Request
The parameters of the requested operation are invalid.
403
Forbidden
The user or client represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource cannot be found.
409
Conflict
The request could not be completed due to a conflict with the current state of the target resource.
429
Too Many Requests
The server has received too many requests.
500
Internal Server Error
An unexpected error occurred on the server.
Response
Body Structure (200)
 Expand all
results
array: object
The list of sheets that were successfully restored.
errors
array: object
The list of sheets that were not restored. Sheets are usually not restored because a sheet with the same number exists in the version set.
Example
Successfully restored sheets.

Request
curl -v 'https://developer.api.autodesk.com/construction/sheets/v1/projects/9ba6681e-1952-4d54-aac4-9de6d9858dd4/sheets:batch-restore' \
  -X 'POST' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a' \
  -H 'Content-Type: application/json' \
  -d '{
        "ids": [
          "0d7a5883-1694-3078-a06d-ad24413f8b06"
        ]
      }'
Show More
Response
{
  "results": [
    {
      "id": "0d7a5883-1694-3078-a06d-ad24413f8b06"
    }
  ],
  "errors": [
    {
      "sheetId": "",
      "code": "",
      "title": "",
      "detail": ""
    }
  ]
}Documentation /Autodesk Construction Cloud APIs /API Reference
Exports
POST	projects/{projectId}/exports
Exports up to 1000 sheets from the from the Sheets tool in ACC Build into a new downloadble PDF file.

You can export any published sheets. For details about publishing sheets, see the Add and Publish Sheets to the Field help documentation.

To perform the export operation, a user must have at least export permission. For more information on permissions, see the Sheets Permissions help documentation.

The POST export endpoint enables the export of PDFs with both standard and feature markups. The supported features currently include Issues and Photos. For additional details on feature markups, see the Feature Markups help documentation.

This endpoint provides the flexibility to designate which types of markups you would like to export. This can be published, unpublished, or both, and is applicable to each markup type including standard, Issues, and Photos. For more information about published and unpublished markups, see the Create and Style Markups help documentation.

This endpoint gives you the flexibility to decide which types of markups to export, be it published, unpublished, or both. This is applicable to each markup type including standard, Issues, and Photos. For more information about published and unpublished markups, see the Create and Style Markups help documentation.

In the case of standard markups, the endpoint also allows the inclusion of attached links to relevant Sheets, Files, RFIs, Forms, Submittals, and Assets. For more information about markup links, see the Add References to Markups help documentation.

Note that this endpoint is asynchronous and initiates a job that runs in the background, rather than halting execution of your program. The response returns an export ID which you can use to poll GET exports/:exportId to check the job’s status. When the job is complete, you can retrieve the data you need to download the exported sheets.

For more details about exporting sheets, see the Export and Print Sheets tutorial.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/construction/sheets/v1/projects/{projectId}/exports
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
The ID of the user on whose behalf the API request is made. This header is optional when using a 2-legged OAuth2, but required if using 2-legged OAuth2 with user impersonation.
When using 2-legged OAuth2 without user impersonation, your app has access to all users defined by the administrator in the SaaS integrations UI. However, when user impersonation is enabled, the API call is restricted to act only on behalf of the specified user. This header is not relevant for 3-legged OAuth2.

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
 Expand all
options
object
The criteria for the markups and links that should be included with the exported sheets.
Note that unpublished markups are only visible to their creator.

sheets
array: string
The list of sheet UUIDs that you want to include in the export. A maximum of 1000 sheets can be included.
Response
HTTP Status Code Summary
202
Accepted
Successfully created an export job
400
Bad Request
The parameters of the requested operation are invalid.
Sample error code with possible messages:

ERR_BAD_INPUT:
Failed to parse the token
User id is required
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
API access denied
User {userId} does not have download permission on resource {resource}
404
Not Found
The requested resources, such as the project, account, user, or sheet do not exist.
Sample error code with possible messages:

ERR_RESOURCE_NOT_EXIST:
Some resources are not found
Account not found
Project not found
Project user not found
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
The ID of the export job. Use the ID to poll GET exports/:exportId to check the job’s status. When the job is complete, you can retrieve the data you need to download the exported sheets.
status
enum:string
The status of the export job; will always be: processing
Example
Successfully created an export job

Request
curl -v 'https://developer.api.autodesk.com/construction/sheets/v1/projects/9ba6681e-1952-4d54-aac4-9de6d9858dd4/exports' \
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
        "sheets": [
          ""
        ]
      }'
Show Less
Response
{
  "id": "5b4bb914-c123-4f10-87e3-579ef934aaf9",
  "status": "processing"
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Exports
GET	projects/{projectId}/exports/{exportId}
Retrieves the status of a PDF sheet export job, as well as the signed URL required to download the exported file once the export process is complete.

To initiate a sheet export, use POST exports. This will return an export ID which should be used with this endpoint.

Note that only the authenticated user who initiated the export job can retrieve the signed URL using this endpoint. This signed URL will be available for one hour. If you need to download the file after this period, you will need to make another call to POST exports.

For more details about exporting sheets, see the Export Sheets tutorial.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/sheets/v1/projects/{projectId}/exports/{exportId}
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
The ID of the user on whose behalf the API request is made. This header is optional when using a 2-legged OAuth2, but required if using 2-legged OAuth2 with user impersonation.
When using 2-legged OAuth2 without user impersonation, your app has access to all users defined by the administrator in the SaaS integrations UI. However, when user impersonation is enabled, the API call is restricted to act only on behalf of the specified user. This header is not relevant for 3-legged OAuth2.

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
Successfully retrieved export data
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
API access denied
User {userId} does not have download permission on resource {resource}
404
Not Found
The requested resources, such as the project, account, user, sheet, or job, do not exist.
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
Response
Body Structure (200)
 Expand all
id
string: UUID
The ID of the sheets export job.
status
enum:string
The status of the sheets export job. Possible values: successful, processing, failed
result
object
The result of a completed export job.
If the status is successful, a downloadable signed URL will be included in the result.output object.
If the status value is failed (e.g., because some files were deleted), the result.error object will include details of the error.
Example
Successfully retrieved export data

Request
curl -v 'https://developer.api.autodesk.com/construction/sheets/v1/projects/9ba6681e-1952-4d54-aac4-9de6d9858dd4/exports/5b4bb914-c123-4f10-87e3-579ef934aaf9' \
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

Documentation /Autodesk Construction Cloud APIs /API Reference
Collections
GET	projects/{projectId}/collections
Retrieves information about all the collections in a project. You can use GET sheets to return all the sheets associated with a specific collection.

For more information about Sheets collections, see the Help documentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/sheets/v1/projects/{projectId}/collections
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
The ID of the user on whose behalf the API request is made. This header is optional when using a 2-legged OAuth2, but required if using 2-legged OAuth2 with user impersonation.
When using 2-legged OAuth2 without user impersonation, your app has access to all users defined by the administrator in the SaaS integrations UI. However, when user impersonation is enabled, the API call is restricted to act only on behalf of the specified user. This header is not relevant for 3-legged OAuth2.

You can use either the user’s ACC ID (id), or their Autodesk ID (autodeskId).

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project. Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can use a project ID either with a “b.” prefix or without a “b.” prefix. For instance, a project ID of “b.a4be0c34a-4ab7” can also be referred to as “a4be0c34a-4ab7”.
Request
Query String Parameters
offset
int
The starting point for the results, specified by item number. The default value is 0. For example, use offset=3 to start the results from the third item.
limit
int
The number of results to return in the response.
Response
HTTP Status Code Summary
200
OK
Successfully retrieved the collections data.
400
Bad Request
The request parameters are invalid.
Sample error code and message:

ERR_BAD_INPUT:
Failed to parse the token
401
Unauthorized
The provided bearer token is invalid.
Sample error code and message:

ERR_AUTHENTICATED_ERROR:
Authentication header is incorrect
403
Forbidden
The user or service associated with the bearer token does not have permission to perform this operation.
Sample error code and messages:

ERR_NOT_ALLOWED:
Account inactive
Project inactive
User inactive
API access denied
User {userId} does not have download permission on resource {resource}
404
Not Found
The requested resource (e.g., project, account, user, sheet, or collection) does not exist.
Sample error code and messages:

ERR_RESOURCE_NOT_EXIST:
Project not found
Project user not found
Collection does not exist
500
Internal Server Error
An unexpected error occurred on the server.
Sample error code and messages:

ERR_INTERNAL_SERVER_ERROR:
Request failed due to internal exception xxx
Failed to retrieve account
Failed to retrieve project
Failed to retrieve user
Response
Body Structure (200)
 Expand all
results
array: object
The list of collections.
pagination
object
Pagination information for paged data.
Example
Successfully retrieved the collections data.

Request
curl -v 'https://developer.api.autodesk.com/construction/sheets/v1/projects/9ba6681e-1952-4d54-aac4-9de6d9858dd4/collections' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "results": [
    {
      "id": "619ef887-974f-45e4-9775-461e6a62d784",
      "name": "Group 1",
      "createdAt": "2024-11-04T08:12:23.041Z",
      "createdBy": "45GPJ4KAX789",
      "createdByName": "John Smith",
      "updatedAt": "2024-11-04T08:12:23.041Z",
      "updatedBy": "45GPJ4KAX789",
      "updatedByName": "John Smith"
    }
  ],
  "pagination": {
    "limit": 100,
    "offset": 0,
    "previousUrl": "",
    "nextUrl": "",
    "totalResults": 1
  }
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Collections
GET	projects/{projectId}/collections/{collectionId}
Retrieves a specific collection by its unique ID.

You can use GET sheets to return all the sheets associated with a specific collection.

For more information about Sheets collections, see the Help documentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/sheets/v1/projects/{projectId}/collections/{collectionId}
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
The ID of the user on whose behalf the API request is made. This header is optional when using a 2-legged OAuth2, but required if using 2-legged OAuth2 with user impersonation.
When using 2-legged OAuth2 without user impersonation, your app has access to all users defined by the administrator in the SaaS integrations UI. However, when user impersonation is enabled, the API call is restricted to act only on behalf of the specified user. This header is not relevant for 3-legged OAuth2.

You can use either the user’s ACC ID (id), or their Autodesk ID (autodeskId).

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project. Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can use a project ID either with a “b.” prefix or without a “b.” prefix. For instance, a project ID of “b.a4be0c34a-4ab7” can also be referred to as “a4be0c34a-4ab7”.
collectionId
string: UUID
The ID of the collection, To find the collection ID, call GET collections.
Response
HTTP Status Code Summary
200
OK
Successfully retrieved collection data
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
API access denied
User {userId} does not have download permission on resource {resource}
404
Not Found
The requested resources, such as the project, account, user, sheet, or collection, do not exist.
Sample error code with possible messages:

ERR_RESOURCE_NOT_EXIST:
Project not found
Project user not found
The collection does not exist
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
Body Structure (200)
id
string: UUID
The unique identifier of the collection.
name
string
The name of the collection. This corresponds to the Name column in the ACC Sheets Collections Settings UI.
createdAt
datetime: ISO 8601
The date and time the collection was created.
createdBy
string
The Autodesk ID of the user who created the collection.
createdByName
string
The name of the user who created the collection.
updatedAt
datetime: ISO 8601
The date and time the collection was last updated.
updatedBy
string
The Autodesk ID of the user who last updated the collection.
updatedByName
string
The name of the user who last updated the collection.
Example
Successfully retrieved collection data

Request
curl -v 'https://developer.api.autodesk.com/construction/sheets/v1/projects/9ba6681e-1952-4d54-aac4-9de6d9858dd4/collections/5cb5d9da-060e-421e-bca9-97dd8b5cd800' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "id": "619ef887-974f-45e4-9775-461e6a62d784",
  "name": "Group 1",
  "createdAt": "2024-11-04T08:12:23.041Z",
  "createdBy": "45GPJ4KAX789",
  "createdByName": "John Smith",
  "updatedAt": "2024-11-04T08:12:23.041Z",
  "updatedBy": "45GPJ4KAX789",
  "updatedByName": "John Smith"
}

