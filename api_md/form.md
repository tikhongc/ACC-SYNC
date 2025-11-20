Documentation /Autodesk Construction Cloud APIs /API Reference
Templates
GET	v1/projects/{projectId}/form-templates
Returns all project’s form templates the user has access to.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/forms/v1/projects/:projectId/form-templates
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
string
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Request
Query String Parameters
offset
int
The number of records to skip before returning the result records. Defaults to 0. Increase this value in subsequent requests to continue getting results when the number of records exceeds the requested limit.
limit
int
The number of records to return in a single request. Can be a number between 1 and 50. Defaults to 50.
updatedAfter
datetime: ISO 8601
Return Templates updated after specified time.
updatedBefore
datetime: ISO 8601
Return Templates updated before specified time.
sortOrder
enum:string
Return Templates in specified sorted order. Possible values: desc, asc
Response
HTTP Status Code Summary
200
OK
Form Templates.
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request header
401
Unauthorized
The request was not accepted because it lacked valid authentication credentials
403
Forbidden
The request was not accepted because the client is authenticated, but is not authorized to access the target resource
404
Not Found
The resource cannot be found
429
Too Many Requests
The request could not be completed due to a conflict with the current state of the target resource
500
Internal Server Error
The request could not be completed due to a conflict with the current state of the target resource
Response
Body Structure (200)
 Expand all
data
array: object
List of form templates in the project.
pagination
object
Request pagination information.


Documentation /Autodesk Construction Cloud APIs /API Reference
Forms
GET	v1/projects/{projectId}/forms
Returns a paginated list of forms in a project. Forms are sorted by updatedAt, most recent first.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/forms/v1/projects/:projectId/forms
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
string
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Request
Query String Parameters
offset
int
The number of records to skip before returning the result records. Defaults to 0. Increase this value in subsequent requests to continue getting results when the number of records exceeds the requested limit.
limit
int
The number of records to return in a single request. Can be a number between 1 and 50. Defaults to 50.
ids
array: string
An array of Form IDs to retrieve.
formDateMin
string
Return Forms with formDate at or after specified date.
formDateMax
string
Return Forms with formDate at or before specified date.
updatedAfter
datetime: ISO 8601
Return Forms updated after a specified time.
updatedBefore
datetime: ISO 8601
Return Forms updated before a specified time.
templateId
string
Return Forms on template with given ID.
statuses
array: string
Return Forms with given statuses.
sortBy
string
Return Forms sorted by specified attribute.
sortOrder
string
Return Forms in specified sorted order.
locationIds
array: string
A sequence of location IDs. Each returned object must be associated with one of the locations specified by the IDs. For example, ?locationId=123e102a-36de-14e7-8c56-1b1234ccbba8&locationId=cee45678-fcc4-43ae-80a2-8ca819dfa70d. See the usage example in the Retrieve Forms Associated With Locations tutorial.
Response
HTTP Status Code Summary
200
OK
Forms in project at specified page.
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request header
401
Unauthorized
The request was not accepted because it lacked valid authentication credentials
403
Forbidden
The request was not accepted because the client is authenticated, but is not authorized to access the target resource
404
Not Found
The resource cannot be found
429
Too Many Requests
The request could not be completed due to a conflict with the current state of the target resource
500
Internal Server Error
The request could not be completed due to a conflict with the current state of the target resource
Response
Body Structure (200)
 Expand all
data
array: object
List of forms in the project.
pagination
object
Request pagination information.
Example
Request
curl -v 'https://developer.api.autodesk.com/construction/forms/v1/projects/:projectId/forms' \
-H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "data": [
      {
          "status": "draft",
          "id": "932da979-e537-4530-b8aa-18607ac6db37",
          "projectId": "9ba6681e-1952-4d54-aac4-9de6d9858dd4",
          "formNum": 1,
          "name": "Daily Safety Inspection",
          "formDate": "2020-11-20",
          "assigneeId": "fc830fd8-f1ef-4cd6-9163-fb115dc698d7",
          "assigneeType": "company",
          "locationId": "d14ce3a6-e61b-4ab0-a9be-5acf7b5366df",
          "updatedAt": "2020-11-20T16:14:27.615127+00:00",
          "createdBy": "USER123A",
          "notes": "Form notes",
          "description": "Form description",
          "formTemplate": {
              "status": "active",
              "id": "2f634a22-779d-4930-9f08-8391a41fea05",
              "projectId": "9ba6681e-1952-4d54-aac4-9de6d9858dd4",
              "name": "Daily Report",
              "templateType": "pg.template_type.daily_report"
          },
          "pdfValues": [
              {
              "name": "CommentsRow1",
              "value": "Observed Masks and Face Covering"
              }
          ],
          "pdfUrl": "https://link.to/form.pdf",
          "weather": {
              "summaryKey": "Clear",
              "precipitationAccumulation": 2.3,
              "precipitationAccumulationUnit": "in",
              "temperatureMin": 47.1,
              "temperatureMax": 65.1,
              "temperatureUnit": "Fahrenheit",
              "humidity": 0.2,
              "windSpeed": 12.5,
              "windGust": 34.6,
              "speedUnit": "km/h",
              "windBearing": 18,
              "hourlyWeather": [
              {
                  "id": 1234,
                  "hour": "07:00:00",
                  "temp": 54.12,
                  "windSpeed": 14.2,
                  "windBearing": 14,
                  "humidity": 0.24,
                  "fetchedAt": null,
                  "createdAt": "2021-01-20T20:38:32+00:00",
                  "updatedAt": "2021-01-20T20:38:32+00:00"
              }
              ],
              "provider": "weatherkit"
          },
          "tabularValues": {
              "worklogEntries": null,
              "materialsEntries": null,
              "equipmentEntries": null
          },
          "customValues": [],
          "lastReopenedBy": "USER123A",
          "lastSubmitterSignature": "PHN2ZyBoZWlnaHQ9IjIwMCIgd2lkdGg9IjUwMCI+PHBvbHlsaW5lIHBvaW50cz0iMjAsMjAgNDAsMjUgNjAsNDAgODAsMTIwIDEyMCwxNDAgMjAwLDE4MCIgc3R5bGU9ImZpbGw6bm9uZTtzdHJva2U6YmxhY2s7c3Ryb2tlLXdpZHRoOjMiIC8+PC9zdmc+",
          "userCreatedAt": "2019-01-20T12:14:27.615127+00:00",
          "createdAt": "2019-01-20T12:14:28.000000+00:00"
      }
  ],
  "pagination": {
      "offset": 0,
      "limit": 50,
      "totalResults": 1,
      "nextUrl": null
  }
}

