Documentation /Autodesk Construction Cloud APIs /API Reference
Relationship: Utilities
GET	utility/relationships:writable
Retrieves a list of entity types that are compatible with each other, to establish whether you can create relationships between them or to delete those relationships. For example, between an asset and a document.

Note that some entity types belong to a bim360 domain, and others to a construction domain.

To learn how this endpoint is used, see the Create a Relationship tutorial.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/relationship/v2/utility/relationships:writable
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
Response
HTTP Status Code Summary
200
OK
Success
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
domain
string
The domain to which the entity types belong.
For example: autodesk-bim360-asset

To learn more about domains and entities, see the Relationship Service Field Guide.

entityTypes
array: object
The list of entity types in the domain.
Example
Request
curl -v 'https://developer.api.autodesk.com/bim360/relationship/v2/utility/relationships:writable' \
     -H 'Authorization: Bearer <token>'
Response (200)
[
  {
    "domain": "autodesk-bim360-asset",
    "entityTypes": [
      {
        "entityType": "asset",
        "allow": [
          {
            "domain": "autodesk-bim360-documentmanagement",
            "entityTypes": [
              "documentlineage"
            ]
          }
        ]
      }
    ]
  }
]


Documentation /Autodesk Construction Cloud APIs /API Reference
Relationship: Sync
POST	containers/:containerId/relationships:syncStatus
Retrieves the relationship synchronization status for the caller as one or more synchronization tokens. This can be based on an optional array of input tokens.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/bim360/relationship/v2/containers/:containerId/relationships:syncStatus
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
referenceId
string
An optional reference passed by the caller and returned by the service.
syncToken
string
The token that can be used to obtain data via the synchronization endpoint.
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
results
array: object
The array of sync tokens.
errors
array: object
The array of errors associated with the request for sync tokens.
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
curl -v 'https://developer.api.autodesk.com/bim360/relationship/v2/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/relationships:syncStatus' \
     -X POST \
     -H 'Authorization: Bearer <token>' \
     -H 'Content-Type: application/json' \
     -d '[
           {
             "syncToken": "eyAibGFzdENoZWNrZWQiOiIyMDE5LTEwLTE4VDEyOjEwOjA3Ljc5NloiIH0="
           }
         ]'
Show Less
Response (200)
{
  "results": [
    {
      "moreData": true,
      "overwrite": false,
      "syncToken": "eyAibGFzdENoZWNrZWQiOiIyMDE5LTEwLTE4VDEyOjEwOjA3Ljc5NloiIH0="
    }
  ],
  "errors": [
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
      ],
      "syncToken": "eyAibGFzdENoZWNrZWQiOiIyMDE5LTEwLTE4VDEyOjEwOjA3Ljc5NloiIH0="
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
Relationship: Sync
POST	containers/:containerId/relationships:sync
Synchronise relationships using the (optional) synchronization token passed by the caller.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/bim360/relationship/v2/containers/:containerId/relationships:sync
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
 Expand all
syncToken
string
The token that can be used to obtain data via the synchronization endpoint.
filters
object
An array of filters on the initial request without a sync token.
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
current
object
A set of current data.
deleted
object
A set of deleted data.
moreData
boolean
If set to true, data is available for synchronization using the supplied synchronization token.
overwrite
boolean
If set to true, the data returned by the synchronization endpoint can be used to overwrite local copies.
nextSyncToken
string
The token that can be used to obtain data via the synchronization endpoint. If moreData is set to false, you can use this token to resume synchronization at a later point in time.
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
curl -v 'https://developer.api.autodesk.com/bim360/relationship/v2/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/relationships:sync' \
     -X POST \
     -H 'Authorization: Bearer <token>' \
     -H 'Content-Type: application/json' \
     -d '{}'
Response (200)
{
  "current": {
    "data": [
      {
        "id": "74b70bb8-8802-a1fd-f201-890375a60c8f",
        "createdOn": "2015-10-21T16:32:22Z",
        "isReadOnly": true,
        "isService": false,
        "isDeleted": false,
        "entities": [
          {
            "domain": "autodesk-bim360-asset",
            "type": "asset",
            "id": "2b95ba7a-3df5-4e99-a693-9c7cc15ee8c0",
            "createdOn": "2021-07-29T11:39:12+01:00"
          },
          {
            "domain": "autodesk-bim360-documentmanagement",
            "type": "documentlineage",
            "id": "urn:adsk.wipprod:dm.lineage:hC6k4hndRWaeIVhIjvHu8w",
            "createdOn": "2021-07-29T13:39:12+01:00"
          }
        ]
      }
    ]
  },
  "deleted": {
    "data": [
      {
        "id": "74b70bb8-8802-a1fd-f201-890375a60c8f",
        "createdOn": "2015-10-21T16:32:22Z",
        "isReadOnly": true,
        "isService": false,
        "isDeleted": false,
        "entities": [
          {
            "domain": "autodesk-bim360-asset",
            "type": "asset",
            "id": "2b95ba7a-3df5-4e99-a693-9c7cc15ee8c0",
            "createdOn": "2021-07-29T11:39:12+01:00"
          },
          {
            "domain": "autodesk-bim360-documentmanagement",
            "type": "documentlineage",
            "id": "urn:adsk.wipprod:dm.lineage:hC6k4hndRWaeIVhIjvHu8w",
            "createdOn": "2021-07-29T13:39:12+01:00"
          }
        ]
      }
    ]
  },
  "moreData": true,
  "overwrite": false,
  "nextSyncToken": "eyAibGFzdENoZWNrZWQiOiIyMDE5LTEwLTE4VDEyOjEwOjA3Ljc5NloiIH0="
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
Relationship: Search
POST	containers/:containerId/relationships:batch
Retrieves a list of one or more relationships by passing an array of relationship IDs.

The response contains a list of the requested relationship objects.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/bim360/relationship/v2/containers/:containerId/relationships:batch
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
The list of relationship IDs to retrieve.
Min items: 1 Max items: 50

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
The UUID that uniquely identifies the relationship.
createdOn
datetime: ISO 8601
The date and time the relationship was created.
isReadOnly
boolean
true if this relationship is read only for the current caller.
false if this relationship is not read only for the current caller.

isService
boolean
true if this relationship was created by a service.
false if this relationship was not created by a service.

isDeleted
boolean
true if this relationship is deleted.
false if this relationship is not deleted.

deletedOn
datetime: ISO 8601
The date and time the relationship was deleted.
entities
array: object
The entities contained in the relationship.
Min items: 2 Max items: 2

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
curl -v 'https://developer.api.autodesk.com/bim360/relationship/v2/containers/fbd6cb57-7d0e-4961-8c2c-69646514ef44/relationships:batch' \
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
    "createdOn": "2015-10-21T16:32:22Z",
    "isReadOnly": true,
    "isService": false,
    "isDeleted": false,
    "entities": [
      {
        "domain": "autodesk-bim360-asset",
        "type": "asset",
        "id": "2b95ba7a-3df5-4e99-a693-9c7cc15ee8c0",
        "createdOn": "2021-07-29T11:39:12+01:00"
      },
      {
        "domain": "autodesk-bim360-documentmanagement",
        "type": "documentlineage",
        "id": "urn:adsk.wipprod:dm.lineage:hC6k4hndRWaeIVhIjvHu8w",
        "createdOn": "2021-07-29T13:39:12+01:00"
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
Relationship: Search
GET	containers/:containerId/relationships:search
Retrieves a list of relationships that match the provided search parameters.

This endpoint supports filtering based on domain, entity type, and ID. The endpoint also supports the option to include deleted relationships. This search is additive for the domain -> type -> ID hierarchy.

Deleted relationships are only returned if the includeDeleted query parameter is set to true.

Callers also have the option to include withDomain, withType and withId to restrict the search to include relationships between domain entities. This endpoint supports the following query semantics:

All relationships that include an entity in domain X
All relationships that include an entity in domain X with type Y
All relationships that include an entity in domain X with type Y and ID Z
All relationships that include an entity in domain X with type Y and ID Z AND also include another entity in domain A
All relationships that include an entity in domain X with type Y and ID Z AND also include another entity in domain A and type B
All relationships that include an entity in domain X with type Y and ID Z AND also include another entity in domain A and type B and ID C
The response contains a list of relationships, restricted by the number specified by the pageLimit property. If set (that is, if there are more results than can be displayed at once), you can provide the continuationToken property in the response in a separate call to retrieve additional results.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/relationship/v2/containers/:containerId/relationships:search
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
domain
string
The relationship domain to search.
type
string
The entity type to search.
id
string
The entity ID to search.
createdAfter
datetime: ISO 8601
Filters the returned relationships to those created after the given time.
createdBefore
datetime: ISO 8601
Filters the returned relationships to those created before the given time.
withDomain
string
The WITH relationship domain to search.
withType
string
The WITH entity type to search.
withId
string
The WITH entity ID to search.
includeDeleted
boolean
Whether or not to include deleted relationships in the search.
onlyDeleted
boolean
Whether or not to only include deleted relationships in the search.
pageLimit
int
The maximum number of relationships to return in a page. If not set, the default page limit is used, as determined by the server.
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
relationships
array: object
The list of relationships.
Max items: 100

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
curl -v 'https://developer.api.autodesk.com/bim360/relationship/v2/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/relationships:search' \
     -H 'Authorization: Bearer <token>'
Example #2 (with all query parameters)
Request
curl -v 'https://developer.api.autodesk.com/bim360/relationship/v2/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/relationships:search?domain=autodesk-example-domain&type=example-type&id=b1d1e7d4-f0ed-11e9-81b4-2a2ae2dbcce4&createdAfter=2015-10-21T16%3a32%3a21Z&createdBefore=2015-10-21T16%3a30%3a45Z&withDomain=autodesk-bim360-issue&withType=issue&withId=bd17903c-7d3b-4e56-a79f-4cea00d430db&includeDeleted=True&onlyDeleted=True&pageLimit=134&continuationToken=10' \
     -H 'Authorization: Bearer <token>'
Response (200)
{
  "page": {
    "continuationToken": "10",
    "syncToken": "eyAibGFzdENoZWNrZWQiOiIyMDE5LTEwLTE4VDEyOjEwOjA3Ljc5NloiIH0="
  },
  "relationships": [
    {
      "id": "74b70bb8-8802-a1fd-f201-890375a60c8f",
      "createdOn": "2015-10-21T16:32:22Z",
      "isReadOnly": true,
      "isService": false,
      "isDeleted": false,
      "entities": [
        {
          "domain": "autodesk-bim360-asset",
          "type": "asset",
          "id": "2b95ba7a-3df5-4e99-a693-9c7cc15ee8c0",
          "createdOn": "2021-07-29T11:39:12+01:00"
        },
        {
          "domain": "autodesk-bim360-documentmanagement",
          "type": "documentlineage",
          "id": "urn:adsk.wipprod:dm.lineage:hC6k4hndRWaeIVhIjvHu8w",
          "createdOn": "2021-07-29T13:39:12+01:00"
        }
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
Relationship: Search
POST	containers/:containerId/relationships:intersect
Retrieves a list of relationships that contain the specified relationship entities.

Also accepts a set of WITH entities, that allow filtering down of the relationships results set to those that have matching entities in the WITH collection.

The response contains a list of relationships that contain entities matching the search criteria.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/bim360/relationship/v2/containers/:containerId/relationships:intersect
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
Query Parameters
includeDeleted
boolean
Whether or not to include deleted relationships in the search.
onlyDeleted
boolean
Whether or not to only include deleted relationships in the search.
pageLimit
int
The maximum number of relationships to return in a page. If not set, the default page limit is used, as determined by the server.
continuationToken
string
The token indicating the start of the page. If not set, the first page is retrieved.
Request
Body Structure
 Expand all
entities*
array: object
The list of entities to return relationships for.
Min items: 1 Max items: 20

withEntities
array: object
The optional list of entities to filter returned relationships by.
Min items: 1 Max items: 20

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
page
object
Paging information associated with a paging response.
relationships
array: object
The list of relationships.
Max items: 100

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
curl -v 'https://developer.api.autodesk.com/bim360/relationship/v2/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/relationships:intersect' \
     -X POST \
     -H 'Authorization: Bearer <token>' \
     -H 'Content-Type: application/json' \
     -d '{
           "entities": [
             {
               "domain": "autodesk-bim360-asset",
               "type": "asset",
               "id": "b1d1e7d4-f0ed-11e9-81b4-2a2ae2dbcce4"
             }
           ],
           "withEntities": [
             {
               "domain": "autodesk-example-domain",
               "type": "example-type",
               "id": "b1d1e7d4-f0ed-11e9-81b4-2a2ae2dbcce4"
             }
           ]
         }'
Show Less
Example #2 (with all query parameters)
Request
curl -v 'https://developer.api.autodesk.com/bim360/relationship/v2/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/relationships:intersect?includeDeleted=True&onlyDeleted=True&pageLimit=134&continuationToken=10' \
     -X POST \
     -H 'Authorization: Bearer <token>' \
     -H 'Content-Type: application/json' \
     -d '{
           "entities": [
             {
               "domain": "autodesk-bim360-asset",
               "type": "asset",
               "id": "b1d1e7d4-f0ed-11e9-81b4-2a2ae2dbcce4"
             }
           ],
           "withEntities": [
             {
               "domain": "autodesk-example-domain",
               "type": "example-type",
               "id": "b1d1e7d4-f0ed-11e9-81b4-2a2ae2dbcce4"
             }
           ]
         }'
Show More
Response (200)
{
  "page": {
    "continuationToken": "10",
    "syncToken": "eyAibGFzdENoZWNrZWQiOiIyMDE5LTEwLTE4VDEyOjEwOjA3Ljc5NloiIH0="
  },
  "relationships": [
    {
      "id": "74b70bb8-8802-a1fd-f201-890375a60c8f",
      "createdOn": "2015-10-21T16:32:22Z",
      "isReadOnly": true,
      "isService": false,
      "isDeleted": false,
      "entities": [
        {
          "domain": "autodesk-bim360-asset",
          "type": "asset",
          "id": "2b95ba7a-3df5-4e99-a693-9c7cc15ee8c0",
          "createdOn": "2021-07-29T11:39:12+01:00"
        },
        {
          "domain": "autodesk-bim360-documentmanagement",
          "type": "documentlineage",
          "id": "urn:adsk.wipprod:dm.lineage:hC6k4hndRWaeIVhIjvHu8w",
          "createdOn": "2021-07-29T13:39:12+01:00"
        }
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
Relationship: Search
GET	containers/:containerId/relationships/:relationshipId
Retrieves a requested relationship based on the relationship’s ID.

Returns the requested relationship object.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/relationship/v2/containers/:containerId/relationships/:relationshipId
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
relationshipId
string: UUID
The GUID that uniquely identifies the relationship.
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
id
string: UUID
The UUID that uniquely identifies the relationship.
createdOn
datetime: ISO 8601
The date and time the relationship was created.
isReadOnly
boolean
true if this relationship is read only for the current caller.
false if this relationship is not read only for the current caller.

isService
boolean
true if this relationship was created by a service.
false if this relationship was not created by a service.

isDeleted
boolean
true if this relationship is deleted.
false if this relationship is not deleted.

deletedOn
datetime: ISO 8601
The date and time the relationship was deleted.
entities
array: object
The entities contained in the relationship.
Min items: 2 Max items: 2

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
curl -v 'https://developer.api.autodesk.com/bim360/relationship/v2/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/relationships/ec69ef97-fde9-e002-bc1c-32cb41dc3239' \
     -H 'Authorization: Bearer <token>'
Response (200)
{
  "id": "74b70bb8-8802-a1fd-f201-890375a60c8f",
  "createdOn": "2015-10-21T16:32:22Z",
  "isReadOnly": true,
  "isService": false,
  "isDeleted": false,
  "entities": [
    {
      "domain": "autodesk-bim360-asset",
      "type": "asset",
      "id": "2b95ba7a-3df5-4e99-a693-9c7cc15ee8c0",
      "createdOn": "2021-07-29T11:39:12+01:00"
    },
    {
      "domain": "autodesk-bim360-documentmanagement",
      "type": "documentlineage",
      "id": "urn:adsk.wipprod:dm.lineage:hC6k4hndRWaeIVhIjvHu8w",
      "createdOn": "2021-07-29T13:39:12+01:00"
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
