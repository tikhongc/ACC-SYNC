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