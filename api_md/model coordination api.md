Documentation /Autodesk Construction Cloud APIs /API Reference
Model Set
POST	containers/:containerId/modelsets
Creates a model set within a given container specifying the folder used to determine the set of model document lineages comprising the model set.

Currently only a single folder is supported; however, sub-folders are supported.

The response contains information about the created model set job.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/bim360/modelset/v3/containers/:containerId/modelsets
Authentication Context	
user context required
Required OAuth Scopes	
data:create, data:write
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via a three-legged OAuth flow.
Content-Type*
string
Must be application/json
x-ads-region
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container in which the model set is created.
Request
Body Structure
 Expand all
modelSetId
string: UUID
The GUID that uniquely identifies the model set. If this value is not supplied a new GUID is created.
name*
string
The name of the model set. This name must be unique within the specified container. Min length: 1 Max length: 64.
description
string
A textual description of the model set. Min length: 1 Max length: 1024.
isDisabled
boolean
Indicates if new versions are created for model set changes.
folders*
array: object
A single folder URN that contains a set of document lineages that are added to the model set. Min items: 1 Max items: 1.
* Required
Response
HTTP Status Code Summary
202
Accepted
The model set job associated with this request
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
409
Conflict
Limit exceeded for enabled model sets, create a disabled model set or disable an existing model set, or a model set with the same name already exists.
415
Unsupported Media Type
The Content-Type header must be application/json.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (202)
 Expand all
jobId
string: UUID
The GUID that uniquely identifies the job.
modelSetId
string: UUID
The GUID that uniquely identifies the model set associated with the job.
resource
string
The resource associated with the job.
createdIssueIds
array: string: UUID
If this job tracks the creation of model set inspection issues, the IDs of the created issues.
status
enum: string
The current job status. Possible values: Failed, Running, Succeeded, Archived.
job
object
A job.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Response
Body Structure (409)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example
Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets' \
     -X POST \
     -H 'Authorization: Bearer <token>' \
     -H 'Content-Type: application/json' \
     -d '{
           "name": "Formal Coordination",
           "description": "Space for coordinating all disciplines",
           "folders": [
             {
               "folderUrn": "urn:adsk.wipprod:fs.folder:co.WI8roO18TU2Cl3P9y64z4w"
             }
           ]
         }'
Show Less
Response (202)
{
  "jobId": "49244371-ee08-9afa-01f8-26fcd8ecb03d",
  "modelSetId": "00fb28a5-e8a4-2755-562a-7c2f0fc87911",
  "status": "Succeeded",
  "job": {
    "operation": "OperationName",
    "seed": {}
  }
}
Show Less
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}
Show Less
Response (409)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}
Documentation /Autodesk Construction Cloud APIs /API Reference
Model Set
GET	containers/:containerId/modelsets
Retrieves a list of model sets in a given container that match the provided search parameters.

The response contains a list of matching model sets, restricted by the number specified by the pageLimit property. If set (that is, if there are more results than can be displayed at once), you can provide the continuationToken property in the response in a separate call to retrieve additional results.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/modelset/v3/containers/:containerId/modelsets
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
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
Request
Query Parameters
pageLimit
int
The maximum number of model sets to return in a page. If not set, the default page limit is used, as determined by the server.
continuationToken
string
The token indicating the start of the page. If not set, the first page is retrieved.
name
string
A model set name filter. This is an equality filter.
folderUrn
string
A folder URN filter.
includeDisabled
boolean
Determines whether to include disabled model sets.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
page
object
Paging information associated with a paging response.
modelSets
array: object
List of model set summaries.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example #1 (no query parameters)
Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets' \
     -H 'Authorization: Bearer <token>'
Example #2 (with all query parameters)
Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets?pageLimit=134&continuationToken=10&name=Formal+Coordination&folderUrn=urn%3aadsk.wipprod%3afs.folder%3aco.WI8roO18TU2Cl3P9y64z4w&includeDisabled=False' \
     -H 'Authorization: Bearer <token>'
Response (200)
{
  "page": {
    "continuationToken": "10"
  },
  "modelSets": [
    {
      "modelSetId": "00fb28a5-e8a4-2755-562a-7c2f0fc87911",
      "containerId": "f0f4f36a-ac64-687f-b132-8efe04b22454",
      "name": "Formal Coordination",
      "description": "Space for coordinating all disciplines",
      "createdBy": "PD23PXGV8V3V",
      "createdTime": "2015-10-21T16:31:44Z",
      "isDisabled": true,
      "isDeleted": false
    }
  ]
}
Show Less
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}
Documentation /Autodesk Construction Cloud APIs /API Reference
Model Set
GET	containers/:containerId/jobs/:jobId
Retrieves information about a given container job.

All calls to the containers resource result in a job. You can use this endpoint to track the progress of these jobs.

You can find the x-ads-region to use from the GET hubs endpoint, under data.attributes.region. See GET hubs/:hub_id for more information.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/modelset/v3/containers/:containerId/jobs/:jobId
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
x-ads-region*
enum: string
The region the container resides in.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
jobId
string: UUID
The GUID that uniquely identifies the job.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
jobId
string: UUID
The GUID that uniquely identifies the job.
containerId
string: UUID
The GUID that uniquely identifies the container associated with the job.
status
enum: string
The current job status. Possible values: Failed, Running, Succeeded, Archived.
job
object
A job.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example
Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/jobs/49244371-ee08-9afa-01f8-26fcd8ecb03d' \
     -H 'Authorization: Bearer <token>'
Response (200)
{
  "jobId": "49244371-ee08-9afa-01f8-26fcd8ecb03d",
  "containerId": "f0f4f36a-ac64-687f-b132-8efe04b22454",
  "status": "Succeeded",
  "job": {
    "operation": "OperationName",
    "seed": {}
  }
}
Show Less
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}
Documentation /Autodesk Construction Cloud APIs /API Reference
Model Set
GET	containers/:containerId/modelsets/:modelSetId
Retrieves a requested model set based on the model set ID.

Returns the requested model set object.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/modelset/v3/containers/:containerId/modelsets/:modelSetId
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
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
modelSetId
string: UUID
The GUID that uniquely identifies the model set.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
modelSetId
string: UUID
The GUID that uniquely identifies the model set.
modelSetType
enum: string
The type of content this model set tracks. Possible values: Plans, ProjectFiles.
containerId
string: UUID
The GUID that uniquely identifies the container.
folders
array: object
The ModelSetFolders that determine the documents included in the model set.
name
string
The name of the model set. This name must be unique within the specified container. Min length: 1 Max length: 64.
description
string
A textual description of the model set. Min length: 1 Max length: 1024.
createdBy
string
The unique identifier of the user who created the model set.
createdTime
datetime: ISO 8601
The date and time that the model set was created.
isDisabled
boolean
If set to true, a model set version is not automatically created following changes to documents within the model set.
tipVersion
int
The version number of the most recent version of the model set.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example
Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911' \
     -H 'Authorization: Bearer <token>'
Response (200)
{
  "modelSetId": "00fb28a5-e8a4-2755-562a-7c2f0fc87911",
  "modelSetType": "Plans",
  "containerId": "f0f4f36a-ac64-687f-b132-8efe04b22454",
  "folders": [
    {
      "folderUrn": "urn:adsk.wipprod:fs.folder:co.WI8roO18TU2Cl3P9y64z4w"
    }
  ],
  "name": "Formal Coordination",
  "description": "Space for coordinating all disciplines",
  "createdBy": "PD23PXGV8V3V",
  "createdTime": "2015-10-21T16:31:44Z",
  "isDisabled": true,
  "tipVersion": 120
}
Show Less
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}
Documentation /Autodesk Construction Cloud APIs /API Reference
Model Set
POST	containers/:containerId/issues/viewcontext
Retrieves the view context around a set of visual inspection issues, such as the model set and documents with which it is associated.

The BIM360 Issues API can be used to obtain individual issues. See GET issues/:issueId for more information.

The response contains context for the set of visual inspection issues.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/bim360/modelset/v3/containers/:containerId/issues/viewcontext
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
Content-Type*
string
Must be application/json
x-ads-region
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
Request
Body Structure
array: string: UUID*
array: string: UUID
The set of issue IDs to find the view context objects for. Min items: 1 Max items: 1.
* Required
Response
HTTP Status Code Summary
200
OK
The set of inspection issue view context objects.
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
415
Unsupported Media Type
The Content-Type header must be application/json.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
issueId
string: UUID
The ID of the inspection issue for retrieving the issue.
modelSetId
string: UUID
The ID of the model set with which inspection issue is associated.
documents
array: object
The list of documents visible when the issue was created.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example
Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/issues/viewcontext' \
     -X POST \
     -H 'Authorization: Bearer <token>' \
     -H 'Content-Type: application/json' \
     -d '[
           "d98c1dd4-008f-04b2-e980-0998ecf8427e"
         ]'
Response (200)
[
  {
    "issueId": "53e6a6c7-5bc9-7b2d-920b-b73efecd8fc1",
    "modelSetId": "00fb28a5-e8a4-2755-562a-7c2f0fc87911",
    "documents": [
      {
        "lineageUrn": "urn:adsk.wipprod:dm.lineage:jvMF7mrHR7OwG_DToKsJUA",
        "viewableName": "Level 1"
      }
    ]
  }
]
Show Less
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}
Documentation /Autodesk Construction Cloud APIs /API Reference
Model Set
GET	containers/:containerId/modelsets/:modelSetId/jobs/:jobId
Retrieves information about a given model set job.

Many PATCH and POST calls to model set endpoints result in a job. You can use this endpoint to track the progress of these jobs.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/modelset/v3/containers/:containerId/modelsets/:modelSetId/jobs/:jobId
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
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
modelSetId
string: UUID
The GUID that uniquely identifies the model set.
jobId
string: UUID
The GUID that uniquely identifies the job.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
jobId
string: UUID
The GUID that uniquely identifies the job.
modelSetId
string: UUID
The GUID that uniquely identifies the model set associated with the job.
resource
string
The resource associated with the job.
createdIssueIds
array: string: UUID
If this job tracks the creation of model set inspection issues, the IDs of the created issues.
status
enum: string
The current job status. Possible values: Failed, Running, Succeeded, Archived.
job
object
A job.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example
Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911/jobs/49244371-ee08-9afa-01f8-26fcd8ecb03d' \
     -H 'Authorization: Bearer <token>'
Response (200)
{
  "jobId": "49244371-ee08-9afa-01f8-26fcd8ecb03d",
  "modelSetId": "00fb28a5-e8a4-2755-562a-7c2f0fc87911",
  "status": "Succeeded",
  "job": {
    "operation": "OperationName",
    "seed": {}
  }
}
Show Less
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}
Documentation /Autodesk Construction Cloud APIs /API Reference
Model Set
GET	containers/:containerId/modelsets/:modelSetId/screenshots/:screenShotId
Retrieves a specific screenshot based on the screenshot ID.

Newly uploaded screenshots can be retrieved with this endpoint. You must first associate the screenshot with a model set view.

Returns the requested screenshot file.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/modelset/v3/containers/:containerId/modelsets/:modelSetId/screenshots/:screenShotId
Authentication Context	
user context required
Required OAuth Scopes	
data:read
Data Format	
PNG Image, JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via a three-legged OAuth flow.
x-ads-region
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
modelSetId
string: UUID
The GUID that uniquely identifies the model set.
screenShotId
string: UUID
The GUID that uniquely identifies the screenshot.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example
Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911/screenshots/3b86f3bf-4292-5d29-231b-6c934f5e28b8' \
     -H 'Authorization: Bearer <token>'
Response (200)
Response is binary.

Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}
Documentation /Autodesk Construction Cloud APIs /API Reference
Model Set: Versions
GET	containers/:containerId/modelsets/:modelSetId/versions
Retrieves a list of versions of a given model set.

The response contains a list of model set versions, restricted by the number specified by the pageLimit property. If set (that is, if there are more results than can be displayed at once), you can provide the continuationToken property in the response in a separate call to retrieve additional results.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/modelset/v3/containers/:containerId/modelsets/:modelSetId/versions
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
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
modelSetId
string: UUID
The GUID that uniquely identifies the model set.
Request
Query Parameters
status
array: enum: string
The statuses to filter the model set versions.
pageLimit
int
The maximum number of model set versions to return in a page. If not set, the default page limit is used, as determined by the server.
continuationToken
string
The token indicating the start of the page. If not set, the first page is retrieved.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
page
object
Paging information associated with a paging response.
modelSetVersions
array: object
List of model set version summaries.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example #1 (no query parameters)
Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911/versions' \
     -H 'Authorization: Bearer <token>'
Example #2 (with all query parameters)
Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911/versions?status=Successful&pageLimit=134&continuationToken=10' \
     -H 'Authorization: Bearer <token>'
Response (200)
{
  "page": {
    "continuationToken": "10"
  },
  "modelSetVersions": [
    {
      "version": 42,
      "createTime": "2015-10-21T16:29:30Z",
      "status": "Successful"
    }
  ]
}
Show Less
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Model Set: Versions
GET	containers/:containerId/modelsets/:modelSetId/versions/latest
Retrieves the latest version of a given model set based on the model set ID.

Returns the requested model set version object.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/modelset/v3/containers/:containerId/modelsets/:modelSetId/versions/latest
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
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
modelSetId
string: UUID
The GUID that uniquely identifies the model set.
Request
Query Parameters
status
array: enum: string
The statuses to filter the model set version.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
modelSetId
string: UUID
The GUID that uniquely identifies the model set.
version
int
The model set version number.
createTime
datetime: ISO 8601
The date and time that the model set version was created.
status
enum: string
The creation status of the model set version. Possible values: Pending, Processing, Successful, Partial, Failed.
documentVersions
array: object
The document versions included in this version of the model set.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example #1 (no query parameters)
Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911/versions/latest' \
     -H 'Authorization: Bearer <token>'
Example #2 (with all query parameters)
Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911/versions/latest?status=Successful' \
     -H 'Authorization: Bearer <token>'
Response (200)
{
  "modelSetId": "00fb28a5-e8a4-2755-562a-7c2f0fc87911",
  "version": 42,
  "createTime": "2015-10-21T16:29:30Z",
  "status": "Successful",
  "documentVersions": [
    {
      "documentLineage": {
        "lineageUrn": "urn:adsk.wipprod:dm.lineage:jvMF7mrHR7OwG_DToKsJUA",
        "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.WI8roO18TU2Cl3P9y64z4w",
        "isAligned": false,
        "tipVersionUrn": "urn:adsk.wipprod:fs.file:vf.jvMF7mrHR7OwG_DToKsJUA?version=1"
      },
      "documentStatus": "Succeeded",
      "forgeType": "versions:autodesk.bim360:Document",
      "versionUrn": "urn:adsk.wipprod:fs.file:vf.jvMF7mrHR7OwG_DToKsJUA?version=1",
      "displayName": "example_document.rvt",
      "viewableName": "Level 1",
      "createUserId": "PD23PXGV8V3V",
      "createTime": "2015-10-21T16:29:30Z",
      "viewableGuid": "b1e3fda8-9a15-8cb9-9951-6f4781f8f897",
      "viewableId": "2df27d58-d1c2-467b-be10-80baf501cb87-0008ebd5",
      "viewableMime": "application/autodesk-svf",
      "bubbleUrn": "urn:adsk.wipprod:fs.file:vf.M7KsPcpXTn6nPPRhrQnjGA?version=1",
      "originalSeedFileVersionUrn": "urn:adsk.wipprod:fs.file:vf.M7KsPcpXTn6nPPRhrQnjGA?version=1",
      "originalSeedFileVersionName": "Hospital_Architectural.rvt"
    }
  ]
}
Show Less
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}


Documentation /Autodesk Construction Cloud APIs /API Reference
Model Set: Versions
GET	containers/:containerId/modelsets/:modelSetId/versions/:version
Retrieves a specific version of a given model set based on the model set ID and version number.

Returns the requested model set version object.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/modelset/v3/containers/:containerId/modelsets/:modelSetId/versions/:version
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
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
modelSetId
string: UUID
The GUID that uniquely identifies the model set.
version
int
The model set version number.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
modelSetId
string: UUID
The GUID that uniquely identifies the model set.
version
int
The model set version number.
createTime
datetime: ISO 8601
The date and time that the model set version was created.
status
enum: string
The creation status of the model set version. Possible values: Pending, Processing, Successful, Partial, Failed.
documentVersions
array: object
The document versions included in this version of the model set.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example
Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911/versions/42' \
     -H 'Authorization: Bearer <token>'
Response (200)
{
  "modelSetId": "00fb28a5-e8a4-2755-562a-7c2f0fc87911",
  "version": 42,
  "createTime": "2015-10-21T16:29:30Z",
  "status": "Successful",
  "documentVersions": [
    {
      "documentLineage": {
        "lineageUrn": "urn:adsk.wipprod:dm.lineage:jvMF7mrHR7OwG_DToKsJUA",
        "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.WI8roO18TU2Cl3P9y64z4w",
        "isAligned": false,
        "tipVersionUrn": "urn:adsk.wipprod:fs.file:vf.jvMF7mrHR7OwG_DToKsJUA?version=1"
      },
      "documentStatus": "Succeeded",
      "forgeType": "versions:autodesk.bim360:Document",
      "versionUrn": "urn:adsk.wipprod:fs.file:vf.jvMF7mrHR7OwG_DToKsJUA?version=1",
      "displayName": "example_document.rvt",
      "viewableName": "Level 1",
      "createUserId": "PD23PXGV8V3V",
      "createTime": "2015-10-21T16:29:30Z",
      "viewableGuid": "b1e3fda8-9a15-8cb9-9951-6f4781f8f897",
      "viewableId": "2df27d58-d1c2-467b-be10-80baf501cb87-0008ebd5",
      "viewableMime": "application/autodesk-svf",
      "bubbleUrn": "urn:adsk.wipprod:fs.file:vf.M7KsPcpXTn6nPPRhrQnjGA?version=1",
      "originalSeedFileVersionUrn": "urn:adsk.wipprod:fs.file:vf.M7KsPcpXTn6nPPRhrQnjGA?version=1",
      "originalSeedFileVersionName": "Hospital_Architectural.rvt"
    }
  ]
}
Show Less
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Model Set: Versions
PATCH	containers/:containerId/modelsets/:modelSetId/versions:enable
Enables automatic version creation for a given model set.

If enabled, model set version creation is triggered when the model set folders’ content changes, or if a call is explicitly made to the ‘POST Create Model Set Versions’ endpoint. If disabled, only an explicit call to the ‘POST Create Model Set Versions’ endpoint triggers new version creation.

The response contains information about the created model set job.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
PATCH	https://developer.api.autodesk.com/bim360/modelset/v3/containers/:containerId/modelsets/:modelSetId/versions:enable
Authentication Context	
user context required
Required OAuth Scopes	
data:write
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via a three-legged OAuth flow.
x-ads-region
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
modelSetId
string: UUID
The GUID that uniquely identifies the model set.
Response
HTTP Status Code Summary
202
Accepted
The model set job associated with this request
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
409
Conflict
Limit exceeded for enabled model sets, please disable an existing model set.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (202)
 Expand all
jobId
string: UUID
The GUID that uniquely identifies the job.
modelSetId
string: UUID
The GUID that uniquely identifies the model set associated with the job.
resource
string
The resource associated with the job.
createdIssueIds
array: string: UUID
If this job tracks the creation of model set inspection issues, the IDs of the created issues.
status
enum: string
The current job status. Possible values: Failed, Running, Succeeded, Archived.
job
object
A job.
operation
string
The operation associated with the job.
seed
object
The JSON payload which seeded the job.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Response
Body Structure (409)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example
Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911/versions:enable' \
     -X PATCH \
     -H 'Authorization: Bearer <token>'
Response (202)
{
  "jobId": "49244371-ee08-9afa-01f8-26fcd8ecb03d",
  "modelSetId": "00fb28a5-e8a4-2755-562a-7c2f0fc87911",
  "status": "Succeeded",
  "job": {
    "operation": "OperationName",
    "seed": {}
  }
}
Show Less
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}
Show Less
Response (409)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Model Set: Versions
PATCH	containers/:containerId/modelsets/:modelSetId/versions:disable
Disables automatic version creation for a given model set.

If enabled, model set version creation is triggered when the model set folders’ content changes, or if a call is explicitly made to the ‘POST Create Model Set Versions’ endpoint. If disabled, only an explicit call to the ‘POST Create Model Set Versions’ endpoint triggers new version creation.

The response contains information about the created model set job.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
PATCH	https://developer.api.autodesk.com/bim360/modelset/v3/containers/:containerId/modelsets/:modelSetId/versions:disable
Authentication Context	
user context required
Required OAuth Scopes	
data:write
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via a three-legged OAuth flow.
x-ads-region
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
modelSetId
string: UUID
The GUID that uniquely identifies the model set.
Response
HTTP Status Code Summary
202
Accepted
The model set job associated with this request
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (202)
 Expand all
jobId
string: UUID
The GUID that uniquely identifies the job.
modelSetId
string: UUID
The GUID that uniquely identifies the model set associated with the job.
resource
string
The resource associated with the job.
createdIssueIds
array: string: UUID
If this job tracks the creation of model set inspection issues, the IDs of the created issues.
status
enum: string
The current job status. Possible values: Failed, Running, Succeeded, Archived.
job
object
A job.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example
Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911/versions:disable' \
     -X PATCH \
     -H 'Authorization: Bearer <token>'
Response (202)
{
  "jobId": "49244371-ee08-9afa-01f8-26fcd8ecb03d",
  "modelSetId": "00fb28a5-e8a4-2755-562a-7c2f0fc87911",
  "status": "Succeeded",
  "job": {
    "operation": "OperationName",
    "seed": {}
  }
}
Show Less
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Model Set: Views
GET	containers/:containerId/modelsets/:modelSetId/views
Retrieves a list of model set views in a given model set that match the provided search parameters.

The response contains a list of matching views, restricted by the number specified by the pageLimit property. If set (that is, if there are more results than can be displayed at once), you can provide the continuationToken property in the response in a separate call to retrieve additional results.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/modelset/v3/containers/:containerId/modelsets/:modelSetId/views
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
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
modelSetId
string: UUID
The GUID that uniquely identifies the model set.
Request
Query Parameters
pageLimit
int
The maximum number of views to return in a page. If not set, the default page limit is used, as determined by the server.
continuationToken
string
The token indicating the start of the page. If not set, the first page is retrieved.
createdBy
string
Filters the returned views by the createdBy property.
modifiedBy
string
Filters the returned views by the modifiedBy property.
after
datetime: ISO 8601
Filters the returned views to those created or modified after the given time.
before
datetime: ISO 8601
Filters the returned views to those created or modified before the given time.
isPrivate
boolean
If set to true, filters the returned views to only those belonging to this user.
sortBy
array: enum: string
Defines properties to sort the returned views by.
sortDirection
enum: string
Defines the sort direction. Possible values: Asc, Desc.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
page
object
Paging information associated with a paging response.
modelSetViews
array: object
The list of model set views.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example #1 (no query parameters)
Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911/views' \
     -H 'Authorization: Bearer <token>'
Example #2 (with all query parameters)
Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911/views?pageLimit=134&continuationToken=10&createdBy=PD23PXGV8V3V&modifiedBy=PD23PXGV8V3V&after=2015-10-21T16%3a30%3a39Z&before=2015-10-21T16%3a29%3a47Z&isPrivate=False&sortBy=Name&sortDirection=Asc' \
     -H 'Authorization: Bearer <token>'
Response (200)
{
  "page": {
    "continuationToken": "10"
  },
  "modelSetViews": [
    {
      "name": "L1 - All disciplines",
      "description": "All discipline models for Level 1",
      "isPrivate": false,
      "definition": [
        {
          "lineageUrn": "urn:adsk.wipprod:dm.lineage:jvMF7mrHR7OwG_DToKsJUA",
          "viewableName": "Level 1"
        }
      ],
      "viewId": "7ed27144-ac06-4b72-5dd6-76bee05854be",
      "createdBy": "PD23PXGV8V3V",
      "createdTime": "2015-10-21T16:31:44Z"
    }
  ]
}
Show Less
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}


Documentation /Autodesk Construction Cloud APIs /API Reference
Model Set: Views
GET	containers/:containerId/modelsets/:modelSetId/views/:viewId
Retrieves a specific model set view based on the view ID.

Returns the requested model set view object.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/modelset/v3/containers/:containerId/modelsets/:modelSetId/views/:viewId
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
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
modelSetId
string: UUID
The GUID that uniquely identifies the model set.
viewId
string: UUID
The GUID that uniquely identifies the view.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
name
string
The name of the model set view. Min length: 1 Max length: 64.
description
string
The description of the model set view. Min length: 1 Max length: 1024.
isPrivate
boolean
Determines whether the view is only accessible to its creator.
definition
array: object
The definition of models in a model set view, which is used to track the same models through time. Min items: 1 Max items: 1000.
viewId
string: UUID
The GUID that uniquely identifies the view.
createdBy
string
The ID of the user or service that created the view.
createdTime
datetime: ISO 8601
The date and time that the view was created.
modifiedBy
string
The ID of the user or service that last modified the view.
modifiedTime
datetime: ISO 8601
The date and time that the view was last modified.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example
Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911/views/7ed27144-ac06-4b72-5dd6-76bee05854be' \
     -H 'Authorization: Bearer <token>'
Response (200)
{
  "name": "L1 - All disciplines",
  "description": "All discipline models for Level 1",
  "isPrivate": false,
  "definition": [
    {
      "lineageUrn": "urn:adsk.wipprod:dm.lineage:jvMF7mrHR7OwG_DToKsJUA",
      "viewableName": "Level 1"
    }
  ],
  "viewId": "7ed27144-ac06-4b72-5dd6-76bee05854be",
  "createdBy": "PD23PXGV8V3V",
  "createdTime": "2015-10-21T16:31:44Z"
}
Show Less
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Model Set: Views
GET	containers/:containerId/modelsets/:modelSetId/versions/:version/views
Retrieves a list of all model set views in a given model set as they exist in a specific model set version.

This operation determines which specific versions of the document lineages contained in each view are present in the given model set version.

The response contains a list of matching view versions, restricted by the number specified by the pageLimit property. If set (that is, if there are more results than can be displayed at once), you can provide the continuationToken property in the response in a separate call to retrieve additional results.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/modelset/v3/containers/:containerId/modelsets/:modelSetId/versions/:version/views
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
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
modelSetId
string: UUID
The GUID that uniquely identifies the model set.
version
int
The model set version number.
Request
Query Parameters
pageLimit
int
The maximum number of views to return in a page. If not set, the default page limit is used, as determined by the server.
continuationToken
string
The token indicating the start of the page. If not set, the first page is retrieved.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
page
object
Paging information associated with a paging response.
modelSetViewVersions
array: object
The list of model set view versions.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example #1 (no query parameters)
Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911/versions/42/views' \
     -H 'Authorization: Bearer <token>'
Example #2 (with all query parameters)
Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911/versions/42/views?pageLimit=134&continuationToken=10' \
     -H 'Authorization: Bearer <token>'
Response (200)
{
  "page": {
    "continuationToken": "10"
  },
  "modelSetViewVersions": [
    {
      "viewId": "7ed27144-ac06-4b72-5dd6-76bee05854be",
      "modelSetId": "00fb28a5-e8a4-2755-562a-7c2f0fc87911",
      "documentVersions": [
        {
          "documentLineage": {
            "lineageUrn": "urn:adsk.wipprod:dm.lineage:jvMF7mrHR7OwG_DToKsJUA",
            "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.WI8roO18TU2Cl3P9y64z4w",
            "isAligned": false,
            "tipVersionUrn": "urn:adsk.wipprod:fs.file:vf.jvMF7mrHR7OwG_DToKsJUA?version=1"
          },
          "documentStatus": "Succeeded",
          "forgeType": "versions:autodesk.bim360:Document",
          "versionUrn": "urn:adsk.wipprod:fs.file:vf.jvMF7mrHR7OwG_DToKsJUA?version=1",
          "displayName": "example_document.rvt",
          "viewableName": "Level 1",
          "createUserId": "PD23PXGV8V3V",
          "createTime": "2015-10-21T16:29:30Z",
          "viewableGuid": "b1e3fda8-9a15-8cb9-9951-6f4781f8f897",
          "viewableId": "2df27d58-d1c2-467b-be10-80baf501cb87-0008ebd5",
          "viewableMime": "application/autodesk-svf",
          "bubbleUrn": "urn:adsk.wipprod:fs.file:vf.M7KsPcpXTn6nPPRhrQnjGA?version=1",
          "originalSeedFileVersionUrn": "urn:adsk.wipprod:fs.file:vf.M7KsPcpXTn6nPPRhrQnjGA?version=1",
          "originalSeedFileVersionName": "Hospital_Architectural.rvt"
        }
      ],
      "version": 42
    }
  ]
}
Show Less
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Model Set: Views
GET	containers/:containerId/modelsets/:modelSetId/versions/:version/views/:viewId
Retrieves a model set view as it exists in a specific model set version.

This operation determines which specific versions of the document lineages contained in the given view are present in the given model set version.

Returns the requested model set view version object.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/modelset/v3/containers/:containerId/modelsets/:modelSetId/versions/:version/views/:viewId
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
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
modelSetId
string: UUID
The GUID that uniquely identifies the model set.
version
int
The model set version number.
viewId
string: UUID
The GUID that uniquely identifies the view.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
viewId
string: UUID
The GUID that uniquely identifies the view.
modelSetId
string: UUID
The GUID that uniquely identifies the model set.
documentVersions
array: object
The document versions included in this version of the model set.
version
int
The model set version number.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example
Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911/versions/42/views/7ed27144-ac06-4b72-5dd6-76bee05854be' \
     -H 'Authorization: Bearer <token>'
Response (200)
{
  "viewId": "7ed27144-ac06-4b72-5dd6-76bee05854be",
  "modelSetId": "00fb28a5-e8a4-2755-562a-7c2f0fc87911",
  "documentVersions": [
    {
      "documentLineage": {
        "lineageUrn": "urn:adsk.wipprod:dm.lineage:jvMF7mrHR7OwG_DToKsJUA",
        "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.WI8roO18TU2Cl3P9y64z4w",
        "isAligned": false,
        "tipVersionUrn": "urn:adsk.wipprod:fs.file:vf.jvMF7mrHR7OwG_DToKsJUA?version=1"
      },
      "documentStatus": "Succeeded",
      "forgeType": "versions:autodesk.bim360:Document",
      "versionUrn": "urn:adsk.wipprod:fs.file:vf.jvMF7mrHR7OwG_DToKsJUA?version=1",
      "displayName": "example_document.rvt",
      "viewableName": "Level 1",
      "createUserId": "PD23PXGV8V3V",
      "createTime": "2015-10-21T16:29:30Z",
      "viewableGuid": "b1e3fda8-9a15-8cb9-9951-6f4781f8f897",
      "viewableId": "2df27d58-d1c2-467b-be10-80baf501cb87-0008ebd5",
      "viewableMime": "application/autodesk-svf",
      "bubbleUrn": "urn:adsk.wipprod:fs.file:vf.M7KsPcpXTn6nPPRhrQnjGA?version=1",
      "originalSeedFileVersionUrn": "urn:adsk.wipprod:fs.file:vf.M7KsPcpXTn6nPPRhrQnjGA?version=1",
      "originalSeedFileVersionName": "Hospital_Architectural.rvt"
    }
  ],
  "version": 42
}
Show Less
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Model Set: Views
GET	containers/:containerId/modelsets/:modelSetId/views/:viewId/jobs/:jobId
Retrieves information about a given model set view job.

Many PATCH, POST and DELETE calls to model set views endpoints will result in a job. You can use this endpoint to track the progress of these jobs.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/modelset/v3/containers/:containerId/modelsets/:modelSetId/views/:viewId/jobs/:jobId
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
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
modelSetId
string: UUID
The GUID that uniquely identifies the model set.
viewId
string: UUID
The GUID that uniquely identifies the view.
jobId
string: UUID
The GUID that uniquely identifies the job.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
jobId
string: UUID
The GUID that uniquely identifies the job.
viewId
string: UUID
The GUID that uniquely identifies the view associated with the job.
status
enum: string
The current job status. Possible values: Failed, Running, Succeeded, Archived.
job
object
A job.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example
Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911/views/7ed27144-ac06-4b72-5dd6-76bee05854be/jobs/49244371-ee08-9afa-01f8-26fcd8ecb03d' \
     -H 'Authorization: Bearer <token>'
Response (200)
{
  "jobId": "49244371-ee08-9afa-01f8-26fcd8ecb03d",
  "viewId": "7ed27144-ac06-4b72-5dd6-76bee05854be",
  "status": "Succeeded",
  "job": {
    "operation": "OperationName",
    "seed": {}
  }
}
Show Less
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Clash Test
GET	containers/:containerId/modelsets/:modelSetId/tests
Retrieves a list of summaries for all clash tests that have been executed for a given model set. If no tests have yet been completed for the specified model set, no tests are returned.

The response contains a list of matching clash test summaries, restricted by the number specified by the pageLimit property. If set (that is, if there are more results than can be displayed at once), you can provide the continuationToken property in the response in a separate call to retrieve additional results.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/clash/v3/containers/:containerId/modelsets/:modelSetId/tests
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
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
modelSetId
string: UUID
The GUID that uniquely identifies the model set.
Request
Query Parameters
status
enum: string
Filters the list of returned clash tests by this status. Possible values: Pending, Processing, Success, Failed.
pageLimit
int
The maximum number of clash tests to return in a page. If not set, the default page limit is used, as determined by the server.
continuationToken
string
The token indicating the start of the page. If not set, the first page is retrieved.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
page
object
Paging information associated with a paging response.
tests
array: object
A list of clash tests.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example #1 (no query parameters)
Request
curl -v 'https://developer.api.autodesk.com/bim360/clash/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911/tests' \
     -H 'Authorization: Bearer <token>'
Example #2 (with all query parameters)
Request
curl -v 'https://developer.api.autodesk.com/bim360/clash/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911/tests?status=Success&pageLimit=134&continuationToken=10' \
     -H 'Authorization: Bearer <token>'
Response (200)
{
  "page": {},
  "tests": [
    {
      "id": "74b70bb8-8802-a1fd-f201-890375a60c8f",
      "modelSetId": "00fb28a5-e8a4-2755-562a-7c2f0fc87911",
      "modelSetVersion": 94,
      "status": "Success"
    }
  ]
}
Show Less
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}


Documentation /Autodesk Construction Cloud APIs /API Reference
Clash Test
GET	containers/:containerId/tests/:testId
Retrieves a requested clash test based on the clash test ID.

Returns the requested clash test object.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/clash/v3/containers/:containerId/tests/:testId
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
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
testId
string: UUID
The GUID that uniquely identifies the clash test.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
id
string: UUID
The GUID that uniquely identifies the clash test.
completedOn
datetime: ISO 8601
The date and time that the clash test was completed.
modelSetId
string: UUID
The GUID that uniquely identifies the model set associated with the clash test.
modelSetVersion
int
The version number of the model set associated with the clash test.
status
enum: string
The status of the clash test. If the status is Success, the results of the clash test are available for use. Possible values: Pending, Processing, Success, Failed.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example
Request
curl -v 'https://developer.api.autodesk.com/bim360/clash/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/tests/c40b4498-1baa-405d-4fe9-423514bbbf10' \
     -H 'Authorization: Bearer <token>'
Response (200)
{
  "id": "74b70bb8-8802-a1fd-f201-890375a60c8f",
  "modelSetId": "00fb28a5-e8a4-2755-562a-7c2f0fc87911",
  "modelSetVersion": 94,
  "status": "Success"
}
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Clash Test
GET	containers/:containerId/tests/:testId/resources
Retrieves information about a given clash test result resources.

When a clash test against a model set version is successful it produces three file resources that contain the raw clash instances and the documents (models) to which these clash results pertain. See the Field Guide section of the API documentation for details.

Returns a list of URLs and secure headers necessary to access the resources generated for the given clash test.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/clash/v3/containers/:containerId/tests/:testId/resources
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
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
testId
string: UUID
The GUID that uniquely identifies the clash test.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
page
object
Paging information associated with a paging response.
resources
array: object
A list of clash test resources.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example
Request
curl -v 'https://developer.api.autodesk.com/bim360/clash/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/tests/c40b4498-1baa-405d-4fe9-423514bbbf10/resources' \
     -H 'Authorization: Bearer <token>'
Response (200)
{
  "page": {},
  "resources": [
    {
      "type": "scope-version-clash.1.0.0",
      "extension": "json.gz",
      "url": "https://example.com/6f760056-db07-4239-ba4c-d9739ac50142/file.json.gz?token=da39a3ee5e6b4b0d3255bfef95601890afd80709",
      "headers": {},
      "validUntil": "2015-10-21T16:29:19Z"
    }
  ]
}
Show Less
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}
Documentation /Autodesk Construction Cloud APIs /API Reference
Clash Test: Closed Clash Groups
POST	containers/:containerId/tests/:testId/clashes:close
Adds a batch of new closed clash groups to the given clash test.

Clash groups that are closed are not presented should they occur in subsequent clash tests. The clash is still present in the model; it is not necessary to remove it.

The response contains information about the created clash group job.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/bim360/clash/v3/containers/:containerId/tests/:testId/clashes:close
Authentication Context	
user context required
Required OAuth Scopes	
data:create, data:write
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via a three-legged OAuth flow.
Content-Type*
string
Must be application/json
x-ads-region
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
testId
string: UUID
The GUID that uniquely identifies the clash test.
Request
Body Structure
id
string: UUID
The unique identifier of the new closed clash group.
title*
string
The title of the new closed clash group. Max length: 128.
description
string
The description of the new closed clash group. Max length: 1024.
reason*
enum: string
The reason that the clash group is being closed. Possible values: OTHER, VALID_INTERFACE, VALID_PENETRATION, MINIMAL_OVERLAP, ITEM_CAN_FLEX, MODEL_INACCURACY, FIELD_FIX.
screenShots
array: string: UUID
The unique identifiers of screenshots to be associated with the new closed clash group. Max items: 5.
clashes*
array: int
The clashes to be included in the new closed clash group. Min items: 1 Max items: 1000.
* Required
Response
HTTP Status Code Summary
202
Accepted
The request has been accepted for processing, but the processing has not been completed.
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
415
Unsupported Media Type
The Content-Type header must be application/json.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (202)
 Expand all
jobId
string: UUID
The GUID that uniquely identifies the job.
groups
array: string: UUID
The GUIDs that uniquely identify the clash groups associated with the job.
createdIssueIds
array: string: UUID
If this job tracks the creation of assigned clashes, the IDs of the created issues.
status
enum: string
The current job status. Possible values: Failed, Running, Succeeded, Archived.
job
object
A job.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example
Request
curl -v 'https://developer.api.autodesk.com/bim360/clash/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/tests/c40b4498-1baa-405d-4fe9-423514bbbf10/clashes:close' \
     -X POST \
     -H 'Authorization: Bearer <token>' \
     -H 'Content-Type: application/json' \
     -d '[
           {
             "title": "Ceiling 2'\'' x 2'\'' grid and 411 other objects.",
             "description": "Objects expected in ceiling.",
             "reason": "OTHER",
             "screenShots": [
               "d98c1dd4-008f-04b2-e980-0998ecf8427e"
             ],
             "clashes": [
               2019963136
             ]
           }
         ]'
Show Less
Response (202)
{
  "jobId": "49244371-ee08-9afa-01f8-26fcd8ecb03d",
  "groups": [
    "d98c1dd4-008f-04b2-e980-0998ecf8427e"
  ],
  "status": "Succeeded",
  "job": {
    "seed": {}
  }
}
Show Less
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}
Documentation /Autodesk Construction Cloud APIs /API Reference
Clash Test: Closed Clash Groups
GET	containers/:containerId/tests/:testId/clashes/closed
Retrieves the state of all closed clash groups in a particular model set, relative to a specified clash test.

This endpoint takes the clashes contained within each closed clash group stored in the system for all clash tests on the same model set, and intersects them with the results of the specified clash test. Clashes which were present when the clash group was first defined can then be resolved.

The response contains a list of closed clash groups, restricted by the number specified by the pageLimit property. If set (that is, if there are more results than can be displayed at once), you can provide the continuationToken property in the response in a separate call to retrieve additional results.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/clash/v3/containers/:containerId/tests/:testId/clashes/closed
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
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
testId
string: UUID
The GUID that uniquely identifies the clash test.
Request
Query Parameters
pageLimit
int
The maximum number of closed clash groups to return in a page. If not set, the default page limit is used, as determined by the server.
continuationToken
string
The token indicating the start of the page. If not set, the first page is retrieved.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
page
object
Paging information associated with a paging response.
modelSetId
string: UUID
The GUID that uniquely identifies the model set.
modelSetVersion
int
The model set version number.
groups
array: object
The list of clash groups intersected with the specified clash test.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example #1 (no query parameters)
Request
curl -v 'https://developer.api.autodesk.com/bim360/clash/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/tests/c40b4498-1baa-405d-4fe9-423514bbbf10/clashes/closed' \
     -H 'Authorization: Bearer <token>'
Example #2 (with all query parameters)
Request
curl -v 'https://developer.api.autodesk.com/bim360/clash/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/tests/c40b4498-1baa-405d-4fe9-423514bbbf10/clashes/closed?pageLimit=134&continuationToken=10' \
     -H 'Authorization: Bearer <token>'
Response (200)
{
  "page": {},
  "modelSetId": "00fb28a5-e8a4-2755-562a-7c2f0fc87911",
  "modelSetVersion": 94,
  "groups": [
    {
      "id": "74b70bb8-8802-a1fd-f201-890375a60c8f",
      "originalClashTestId": "dadf49a9-3496-20d1-308d-a9bee3b0a9a4",
      "createdAtVersion": 77,
      "existing": [
        2019963136
      ],
      "resolved": [
        2019963136
      ]
    }
  ]
}
Show More
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}
Documentation /Autodesk Construction Cloud APIs /API Reference
Clash Test: Closed Clash Groups
POST	containers/:containerId/tests/:testId/clashes:close
Adds a batch of new closed clash groups to the given clash test.

Clash groups that are closed are not presented should they occur in subsequent clash tests. The clash is still present in the model; it is not necessary to remove it.

The response contains information about the created clash group job.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/bim360/clash/v3/containers/:containerId/tests/:testId/clashes:close
Authentication Context	
user context required
Required OAuth Scopes	
data:create, data:write
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via a three-legged OAuth flow.
Content-Type*
string
Must be application/json
x-ads-region
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
testId
string: UUID
The GUID that uniquely identifies the clash test.
Request
Body Structure
id
string: UUID
The unique identifier of the new closed clash group.
title*
string
The title of the new closed clash group. Max length: 128.
description
string
The description of the new closed clash group. Max length: 1024.
reason*
enum: string
The reason that the clash group is being closed. Possible values: OTHER, VALID_INTERFACE, VALID_PENETRATION, MINIMAL_OVERLAP, ITEM_CAN_FLEX, MODEL_INACCURACY, FIELD_FIX.
screenShots
array: string: UUID
The unique identifiers of screenshots to be associated with the new closed clash group. Max items: 5.
clashes*
array: int
The clashes to be included in the new closed clash group. Min items: 1 Max items: 1000.
* Required
Response
HTTP Status Code Summary
202
Accepted
The request has been accepted for processing, but the processing has not been completed.
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
415
Unsupported Media Type
The Content-Type header must be application/json.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (202)
 Expand all
jobId
string: UUID
The GUID that uniquely identifies the job.
groups
array: string: UUID
The GUIDs that uniquely identify the clash groups associated with the job.
createdIssueIds
array: string: UUID
If this job tracks the creation of assigned clashes, the IDs of the created issues.
status
enum: string
The current job status. Possible values: Failed, Running, Succeeded, Archived.
job
object
A job.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example
Request
curl -v 'https://developer.api.autodesk.com/bim360/clash/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/tests/c40b4498-1baa-405d-4fe9-423514bbbf10/clashes:close' \
     -X POST \
     -H 'Authorization: Bearer <token>' \
     -H 'Content-Type: application/json' \
     -d '[
           {
             "title": "Ceiling 2'\'' x 2'\'' grid and 411 other objects.",
             "description": "Objects expected in ceiling.",
             "reason": "OTHER",
             "screenShots": [
               "d98c1dd4-008f-04b2-e980-0998ecf8427e"
             ],
             "clashes": [
               2019963136
             ]
           }
         ]'
Show More
Response (202)
{
  "jobId": "49244371-ee08-9afa-01f8-26fcd8ecb03d",
  "groups": [
    "d98c1dd4-008f-04b2-e980-0998ecf8427e"
  ],
  "status": "Succeeded",
  "job": {
    "seed": {}
  }
}
Show Less
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}
Documentation /Autodesk Construction Cloud APIs /API Reference
Clash Test: Closed Clash Groups
POST	containers/:containerId/tests/:testId/clashes/closed
Retrieves the state of the specified closed clash groups, relative to a specified clash test.

This endpoint takes the clashes contained within each specified closed clash group, and intersects them with the results of the specified clash test. Clashes that were present when the clash group was first defined may have been resolved in this clash test.

The response contains a list of closed clash groups.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/bim360/clash/v3/containers/:containerId/tests/:testId/clashes/closed
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
Content-Type*
string
Must be application/json
x-ads-region
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
testId
string: UUID
The GUID that uniquely identifies the clash test.
Request
Body Structure
array: string: UUID*
array: string: UUID
The array of clash group IDs to find the detail for. Min items: 1 Max items: 20.
* Required
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
415
Unsupported Media Type
The Content-Type header must be application/json.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
id
string: UUID
The unique identifier of the closed clash group.
clashTestId
string: UUID
The unique identifier of the clash test associated with the closed clash group.
title
string
The title of the closed clash group. Max length: 128.
description
string
The description of the closed clash group. Max length: 1024.
reason
enum: string
The reason for closing this clash group. Possible values: OTHER, VALID_INTERFACE, VALID_PENETRATION, MINIMAL_OVERLAP, ITEM_CAN_FLEX, MODEL_INACCURACY, FIELD_FIX.
screenShots
array: string: UUID
The unique identifiers of screenshots associated with the closed clash group. Max items: 5.
createdBy
string
The unique identifier of the user who created the closed clash group.
createdOn
datetime: ISO 8601
The date and time that the closed clash group was created.
clashData
object
The clash data associated with a clash group.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example
Request
curl -v 'https://developer.api.autodesk.com/bim360/clash/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/tests/c40b4498-1baa-405d-4fe9-423514bbbf10/clashes/closed' \
     -X POST \
     -H 'Authorization: Bearer <token>' \
     -H 'Content-Type: application/json' \
     -d '[
           "d98c1dd4-008f-04b2-e980-0998ecf8427e"
         ]'
Response (200)
[
  {
    "id": "74b70bb8-8802-a1fd-f201-890375a60c8f",
    "clashTestId": "21469f89-986a-c194-ae45-cefade1c7bde",
    "title": "Ceiling 2' x 2' grid and 411 other objects.",
    "description": "Objects expected in ceiling.",
    "reason": "OTHER",
    "screenShots": [
      "d98c1dd4-008f-04b2-e980-0998ecf8427e"
    ],
    "createdBy": "PD23PXGV8V3V",
    "createdOn": "2015-10-21T16:32:22Z",
    "clashData": {
      "documents": [
        {
          "id": 184,
          "urn": "urn:adsk.wipprod:fs.file:vf.jvMF7mrHR7OwG_DToKsJUA?version=1",
          "viewableName": "Level 1"
        }
      ],
      "clashes": [
        {
          "id": 184,
          "clash": [
            212
          ],
          "dist": 114.1678367952799,
          "status": "New"
        }
      ],
      "clashInstances": [
        {
          "cid": 75,
          "ldid": 1,
          "loid": 91,
          "lvid": 69,
          "rdid": 147,
          "roid": 246,
          "rvid": 243
        }
      ]
    }
  }
]
Show More
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Clash Test: Closed Clash Groups
GET	containers/:containerId/modelsets/:modelSetId/clashes/closed
Retrieves a list of closed clash groups in a given model set which match the provided search parameters.

The response contains a list of matching closed clash groups, restricted by the number specified by the pageLimit property. If set (that is, if there are more results than can be displayed at once), you can provide the continuationToken property in the response in a separate call to retrieve additional results.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/clash/v3/containers/:containerId/modelsets/:modelSetId/clashes/closed
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
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
modelSetId
string: UUID
The GUID that uniquely identifies the model set.
Request
Query Parameters
pageLimit
int
The maximum number of closed clash groups to return in a page. If not set, the default page limit is used, as determined by the server.
continuationToken
string
The token indicating the start of the page. If not set, the first page is retrieved.
clashTestId
string: UUID
Filters the returned closed clash groups by the clashTestId property.
reason
string
Filters the returned closed clash groups by the reason property.
createdBy
string
Filters the returned closed clash groups by the createdBy property.
after
datetime: ISO 8601
Filters the returned closed clash groups to those created or modified after the given time.
before
datetime: ISO 8601
Filters the returned closed clash groups to those created or modified before the given time.
sort
enum: string
Defines the sort direction. Possible values: Asc, Desc.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
page
object
Paging information associated with a paging response.
groups
array: object
The set of closed clash groups on this page.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example #1 (no query parameters)
Request
curl -v 'https://developer.api.autodesk.com/bim360/clash/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911/clashes/closed' \
     -H 'Authorization: Bearer <token>'
Example #2 (with all query parameters)
Request
curl -v 'https://developer.api.autodesk.com/bim360/clash/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911/clashes/closed?pageLimit=134&continuationToken=10&clashTestId=21469f89-986a-c194-ae45-cefade1c7bde&reason=VALID_INTERFACE&createdBy=PD23PXGV8V3V&after=2015-10-21T16%3a30%3a39Z&before=2015-10-21T16%3a29%3a47Z&sort=Asc' \
     -H 'Authorization: Bearer <token>'
Response (200)
{
  "page": {},
  "groups": [
    {
      "id": "74b70bb8-8802-a1fd-f201-890375a60c8f",
      "clashTestId": "21469f89-986a-c194-ae45-cefade1c7bde",
      "title": "Ceiling 2' x 2' grid and 411 other objects.",
      "description": "Objects expected in ceiling.",
      "reason": "OTHER",
      "screenShots": [
        "d98c1dd4-008f-04b2-e980-0998ecf8427e"
      ],
      "createdBy": "PD23PXGV8V3V",
      "createdOn": "2015-10-21T16:32:22Z",
      "clashes": [
        2019963136
      ]
    }
  ]
}
Show Less
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}


Documentation /Autodesk Construction Cloud APIs /API Reference
Clash Test: Assigned Clash Groups
GET	containers/:containerId/tests/:testId/clashes/assigned
Retrieves the state of all assigned clash groups in a particular model set, relative to a specified clash test.

This endpoint takes the clashes contained within each assigned clash group stored in the system for all clash tests on the same model set, and intersects them with the results of the specified clash test. Clashes which were present when the clash group was first defined may now be resolved.

The response contains a list of assigned clash groups, restricted by the number specified by the pageLimit property. If set (that is, if there are more results than can be displayed at once), you can provide the continuationToken property in the response in a separate call to retrieve additional results.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/clash/v3/containers/:containerId/tests/:testId/clashes/assigned
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
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
testId
string: UUID
The GUID that uniquely identifies the clash test.
Request
Query Parameters
pageLimit
int
The maximum number of assigned clash groups to return in a page. If not set, the default page limit is used, as determined by the server.
continuationToken
string
The token indicating the start of the page. If not set, the first page is retrieved.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
page
object
Paging information associated with a paging response.
modelSetId
string: UUID
The GUID that uniquely identifies the model set.
modelSetVersion
int
The model set version number.
groups
array: object
The list of clash groups intersected with the specified clash test.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example #1 (no query parameters)
Request
curl -v 'https://developer.api.autodesk.com/bim360/clash/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/tests/c40b4498-1baa-405d-4fe9-423514bbbf10/clashes/assigned' \
     -H 'Authorization: Bearer <token>'
Example #2 (with all query parameters)
Request
curl -v 'https://developer.api.autodesk.com/bim360/clash/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/tests/c40b4498-1baa-405d-4fe9-423514bbbf10/clashes/assigned?pageLimit=134&continuationToken=10' \
     -H 'Authorization: Bearer <token>'
Response (200)
{
  "page": {},
  "modelSetId": "00fb28a5-e8a4-2755-562a-7c2f0fc87911",
  "modelSetVersion": 94,
  "groups": [
    {
      "id": "74b70bb8-8802-a1fd-f201-890375a60c8f",
      "originalClashTestId": "dadf49a9-3496-20d1-308d-a9bee3b0a9a4",
      "createdAtVersion": 77,
      "existing": [
        2019963136
      ],
      "resolved": [
        2019963136
      ]
    }
  ]
}
Show Less
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Clash Test: Assigned Clash Groups
POST	containers/:containerId/tests/:testId/clashes/assigned
Retrieves the state of the specified assigned clash groups, relative to a specified clash test.

This endpoint takes the clashes contained within each specified assigned clash group, and intersects them with the results of the specified clash test. Clashes that were present when the clash group was first defined may have been resolved in this clash test.

This method can accept either a list of assigned clash group IDs or a list of BIM 360 Issue GUIDs. To retrieve results by BIM 360 Issue GUID, set the issues query parameter to true.

The response contains a list of assigned clash groups.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/bim360/clash/v3/containers/:containerId/tests/:testId/clashes/assigned
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
Content-Type*
string
Must be application/json
x-ads-region
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
testId
string: UUID
The GUID that uniquely identifies the clash test.
Request
Query Parameters
issues
boolean
If set to true, the query is performed on issue IDs instead of clash group IDs.
Request
Body Structure
array: string: UUID*
array: string: UUID
The list of clash group IDs OR BIM 360 issue IDs to query (depending on the value of the issues query parameter). Min items: 1 Max items: 20.
* Required
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
415
Unsupported Media Type
The Content-Type header must be application/json.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
id
string: UUID
The unique identifier of the assigned clash group.
clashTestId
string: UUID
The unique identifier of the clash test associated with the assigned clash group.
issueId
string: UUID
The unique identifier of the issue associated with the assigned clash group.
createdBy
string
The unique identifier of the user who created the assigned clash group.
createdOn
datetime: ISO 8601
The date and time that the assigned clash group was created.
clashData
object
The clash data associated with a clash group.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example #1 (no query parameters)
Request
curl -v 'https://developer.api.autodesk.com/bim360/clash/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/tests/c40b4498-1baa-405d-4fe9-423514bbbf10/clashes/assigned' \
     -X POST \
     -H 'Authorization: Bearer <token>' \
     -H 'Content-Type: application/json' \
     -d '[
           "d98c1dd4-008f-04b2-e980-0998ecf8427e"
         ]'
Example #2 (with all query parameters)
Request
curl -v 'https://developer.api.autodesk.com/bim360/clash/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/tests/c40b4498-1baa-405d-4fe9-423514bbbf10/clashes/assigned?issues=True' \
     -X POST \
     -H 'Authorization: Bearer <token>' \
     -H 'Content-Type: application/json' \
     -d '[
           "d98c1dd4-008f-04b2-e980-0998ecf8427e"
         ]'
Response (200)
[
  {
    "id": "74b70bb8-8802-a1fd-f201-890375a60c8f",
    "clashTestId": "21469f89-986a-c194-ae45-cefade1c7bde",
    "issueId": "53e6a6c7-5bc9-7b2d-920b-b73efecd8fc1",
    "createdBy": "PD23PXGV8V3V",
    "createdOn": "2015-10-21T16:32:22Z",
    "clashData": {
      "documents": [
        {
          "id": 184,
          "urn": "urn:adsk.wipprod:fs.file:vf.jvMF7mrHR7OwG_DToKsJUA?version=1",
          "viewableName": "Level 1"
        }
      ],
      "clashes": [
        {
          "id": 184,
          "clash": [
            212
          ],
          "dist": 114.1678367952799,
          "status": "New"
        }
      ],
      "clashInstances": [
        {
          "cid": 75,
          "ldid": 1,
          "loid": 91,
          "lvid": 69,
          "rdid": 147,
          "roid": 246,
          "rvid": 243
        }
      ]
    }
  }
]
Show Less
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}
Documentation /Autodesk Construction Cloud APIs /API Reference
Clash Test: Assigned Clash Groups
GET	containers/:containerId/modelsets/:modelSetId/clashes/assigned
Retrieves a list of assigned clash groups in a given model set which match the provided search parameters.

The response contains a list of matching assigned clash groups, restricted by the number specified by the pageLimit property. If set (that is, if there are more results than can be displayed at once), you can provide the continuationToken property in the response in a separate call to retrieve additional results.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/clash/v3/containers/:containerId/modelsets/:modelSetId/clashes/assigned
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
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
modelSetId
string: UUID
The GUID that uniquely identifies the model set.
Request
Query Parameters
pageLimit
int
The maximum number of assigned clash groups to return in a page. If not set, the default page limit is used, as determined by the server.
continuationToken
string
The token indicating the start of the page. If not set, the first page is retrieved.
clashTestId
string: UUID
Filters the returned assigned clash groups by the clashTestId property.
issueId
string: UUID
Filters the returned assigned clash groups by the issueId property.
createdBy
string
Filters the returned assigned clash groups by the createdBy property.
after
datetime: ISO 8601
Filters the returned assigned clash groups to those created or modified after the given time.
before
datetime: ISO 8601
Filters the returned assigned clash groups to those created or modified before the given time.
sort
enum: string
Defines the sort direction. Possible values: Asc, Desc.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
page
object
Paging information associated with a paging response.
groups
array: object
The set of assigned clash groups on this page.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example #1 (no query parameters)
Request
curl -v 'https://developer.api.autodesk.com/bim360/clash/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911/clashes/assigned' \
     -H 'Authorization: Bearer <token>'
Example #2 (with all query parameters)
Request
curl -v 'https://developer.api.autodesk.com/bim360/clash/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911/clashes/assigned?pageLimit=134&continuationToken=10&clashTestId=21469f89-986a-c194-ae45-cefade1c7bde&issueId=53e6a6c7-5bc9-7b2d-920b-b73efecd8fc1&createdBy=PD23PXGV8V3V&after=2015-10-21T16%3a30%3a39Z&before=2015-10-21T16%3a29%3a47Z&sort=Asc' \
     -H 'Authorization: Bearer <token>'
Response (200)
{
  "page": {},
  "groups": [
    {
      "id": "74b70bb8-8802-a1fd-f201-890375a60c8f",
      "clashTestId": "21469f89-986a-c194-ae45-cefade1c7bde",
      "issueId": "db74db66-1115-4270-beea-6c5bb1e60194",
      "createdBy": "PD23PXGV8V3V",
      "createdOn": "2015-10-21T16:32:22Z",
      "clashes": [
        2019963136
      ]
    }
  ]
}
Show Less
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Clash Test: Assigned Clash Groups
POST	containers/:containerId/clashes/assigned/viewcontext
Retrieves the view context around a set of assigned clash groups, such as the model set, and documents with which they are associated.

You can use the BIM360 Issues API to obtain individual issues. See GET issues/:issueId for more information.

The response contains context for the set of assigned clash groups.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/bim360/clash/v3/containers/:containerId/clashes/assigned/viewcontext
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
Content-Type*
string
Must be application/json
x-ads-region
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
Request
Body Structure
array: string: UUID*
array: string: UUID
A set of issue IDs. Min items: 1 Max items: 5.
* Required
Response
HTTP Status Code Summary
200
OK
The set of assigned clash group view context objects.
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
415
Unsupported Media Type
The Content-Type header must be application/json.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
issueId
string: UUID
The ID of the assigned clash group issue for retrieving the issue.
modelSetId
string: UUID
The ID of the model set this assigned clash group issue is associated with.
clashGroup
object
A Clash Group.
documents
array: object
The list of documents visible when the issue was created.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example
Request
curl -v 'https://developer.api.autodesk.com/bim360/clash/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/clashes/assigned/viewcontext' \
     -X POST \
     -H 'Authorization: Bearer <token>' \
     -H 'Content-Type: application/json' \
     -d '[
           "d98c1dd4-008f-04b2-e980-0998ecf8427e"
         ]'
Response (200)
[
  {
    "issueId": "53e6a6c7-5bc9-7b2d-920b-b73efecd8fc1",
    "modelSetId": "00fb28a5-e8a4-2755-562a-7c2f0fc87911",
    "clashGroup": {
      "id": "74b70bb8-8802-a1fd-f201-890375a60c8f",
      "clashTestId": "21469f89-986a-c194-ae45-cefade1c7bde",
      "issueId": "db74db66-1115-4270-beea-6c5bb1e60194",
      "createdBy": "PD23PXGV8V3V",
      "createdOn": "2015-10-21T16:32:22Z",
      "clashes": [
        2019963136
      ]
    },
    "documents": [
      {
        "lineageUrn": "urn:adsk.wipprod:dm.lineage:jvMF7mrHR7OwG_DToKsJUA",
        "viewableName": "Level 1"
      }
    ]
  }
]
Show Less
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Clash Test: Clash Groups Shared
GET	containers/:containerId/clashes/jobs/:jobId
Retrieves information about a given clash job.

Many POST calls to clash endpoints result in a job. This endpoint can be used to track the progress of these jobs.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/clash/v3/containers/:containerId/clashes/jobs/:jobId
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
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
jobId
string: UUID
The GUID that uniquely identifies the job.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
jobId
string: UUID
The GUID that uniquely identifies the job.
groups
array: string: UUID
The GUIDs that uniquely identify the clash groups associated with the job.
createdIssueIds
array: string: UUID
If this job tracks the creation of assigned clashes, the IDs of the created issues.
status
enum: string
The current job status. Possible values: Failed, Running, Succeeded, Archived.
job
object
A job.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example
Request
curl -v 'https://developer.api.autodesk.com/bim360/clash/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/clashes/jobs/49244371-ee08-9afa-01f8-26fcd8ecb03d' \
     -H 'Authorization: Bearer <token>'
Response (200)
{
  "jobId": "49244371-ee08-9afa-01f8-26fcd8ecb03d",
  "groups": [
    "d98c1dd4-008f-04b2-e980-0998ecf8427e"
  ],
  "status": "Succeeded",
  "job": {
    "seed": {}
  }
}
Show Less
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Clash Test: Clash Groups Shared
GET	containers/:containerId/modelsets/:modelSetId/screenshots/:screenShotId
Retrieves a specific screenshot based on the screenshot ID.

Newly uploaded screenshots can be retrieved with this endpoint and must first be associated with a closed clash group.

Returns the requested screenshot file.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/clash/v3/containers/:containerId/modelsets/:modelSetId/screenshots/:screenShotId
Authentication Context	
user context required
Required OAuth Scopes	
data:read
Data Format	
PNG Image, JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via a three-legged OAuth flow.
x-ads-region
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
modelSetId
string: UUID
The GUID that uniquely identifies the model set.
screenShotId
string: UUID
The GUID that uniquely identifies the screenshot.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example
Request
curl -v 'https://developer.api.autodesk.com/bim360/clash/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911/screenshots/3b86f3bf-4292-5d29-231b-6c934f5e28b8' \
     -H 'Authorization: Bearer <token>'
Response (200)
Response is binary.

Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}


Documentation /Autodesk Construction Cloud APIs /API Reference
Clash Test: Clash Groups Shared
GET	containers/:containerId/modelsets/:modelSetId/clashes/grouped
Retrieves a list of clashes associated with assigned or closed clash groups in a given model set.

The response contains a list of clash IDs that take part in closed or assigned clash groups.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/clash/v3/containers/:containerId/modelsets/:modelSetId/clashes/grouped
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
enum: string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA. For the full list of supported regions, see the Regions page.

* Required
Request
URI Parameters
containerId
string: UUID
The GUID that uniquely identifies the container.
modelSetId
string: UUID
The GUID that uniquely identifies the model set.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters of the requested operation are invalid.
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
clashes
array: int
The set of clashes that have been assigned or closed.
Response
Body Structure (400)
 Expand all
type
string
The error code.
title
string
A short title for the error.
detail
string
A more detailed, human readable description of the error, assuming that this message is not localized and is therefore EN-US. UI consumers can use the error.type value to provide a localized version of this error for presentation.
errors
array: object
A set of specific validation errors that need to be fixed.
Example
Request
curl -v 'https://developer.api.autodesk.com/bim360/clash/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911/clashes/grouped' \
     -H 'Authorization: Bearer <token>'
Response (200)
{
  "clashes": [
    2019963136
  ]
}
Response (400)
{
  "type": "BadInput",
  "title": "One or more input values in the request were bad",
  "detail": "The following parameters are invalid: containerId",
  "errors": [
    {
      "field": "containerId",
      "title": "Invalid parameter",
      "detail": "The value 'testing' is not valid.",
      "type": "BadInput"
    }
  ]
}