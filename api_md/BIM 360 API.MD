Account Admin APi：

Documentation /BIM 360 API /API Reference
Projects
GET	projects
Query all the projects in a specific BIM 360 account.

Note that this endpoint is ONLY compatible with BIM 360 projects. It is not compatible with Autodesk Construction Cloud (ACC) projects. For more information about compatibility between between BIM 360 and ACC, see the Compatibility section.

Resource Information
Method and URI（US）	
GET	https://developer.api.autodesk.com/hq/v1/accounts/:account_id/projects
Method and URI（Legacy）	
GET	https://developer.api.autodesk.com/hq/v1/regions/eu/accounts/:account_id/projects
Authentication Context	
app only
Required OAuth Scopes	
account:read
Data Formats	
JSON
Request
Headers
Authorization
yes
Must be Bearer <token>, where <token> is obtained via a two-legged OAuth flow.
Region
no
Specifies the region where the service is located. Possible values: US, EMEA. For the full list of supported regions, see the Regions page.
URI Parameters
account_id
string: UUID
The account ID of the projects. This corresponds to hub ID in the Data Management API. To convert a hub ID into an account ID you need to remove the “b." prefix. For example, a hub ID of b.c8b0c73d-3ae9 translates to an account ID of c8b0c73d-3ae9.
Request
Query String Parameters
limit
int
Response array’s size
Default value: 10
Max limit: 100
offset
int
Offset of response array
Default value: 0
sort
string
Comma-separated fields to sort by in ascending order

Prepending a field with - sorts in descending order
Invalid fields and whitespaces will be ignored
field
string
Comma-separated fields to include in response

id will always be returned
Invalid fields will be ignored
Response
HTTP Status Code Summary
200
OK
The request has succeeded.
400
Bad Request
The request could not be understood by the server due to malformed syntax.
403
Forbidden
Unauthorized
404
Not Found
The resource cannot be found.
409
Conflict
The request could not be completed due to a conflict with the current state of the resource.
422
Unprocessable Entity
The request was unable to be followed due to restrictions.
500
Internal Server Error
An unexpected error occurred on the server.
Response
Body Structure (200)
A successful response is an array of projects, flat JSON objects with the following attributes:

id
string: UUID
Project ID
account_id
string: UUID
Account ID
name
string
Name of the project
Max length: 255
start_date
date
The starting date of a project; must be earlier than end_date

Format: YYYY-MM-DD
end_date
date
The ending date of a project; must be later than start_date

Format: YYYY-MM-DD
project_type
string
The type of project; accepts preconfigured and customized project types

Max length: 255

Refer to the preconfigured project_type list in
the Parameters guide.
value
float
Monetary value of the project
currency
enum: string
Currency for project value

Refer to the currency list in the Parameters guide.
status
enum: string
The status of project.

Possible values:
active: project is active with at least one project admin added
pending: project has been created but pending becuase no project admin added
inactive: project is suspended
archived: project is archived and displayed only in the archived list
job_number
string
Project job number to connect a BIM 360 project to project or job in a financial or ERP system.

Max length: 100
address_line_1
string
Project address line 1

Max length: 255
address_line_2
string
Project address line 2

Max length: 255
city
string
City in which project is located

Max length: 255
state_or_province
enum: string
State or province in which project is located

Max length: 255

Note that the state_or_province value depends on the selected country value; see the valid values in the state_or_province list in the Parameters guide.
postal_code
string
Postal code for the project location

Max length: 255
country
enum: string
Country for this project

Refer to the country list in the Parameters guide.
business_unit_id
string: UUID
The business unit ID of this project
timezone
string
Time zone for this project

Refer to the timezone list in the Parameters guide.
language
enum: string
Language of the project; applicable to the BIM 360 Field service only

Possible values:
en: English
de: German
construction_type
enum: string
Type of construction

Refer to the construction_type list in the Parameters guide.
contract_type
enum: string
Contract Type for your project

Refer to the constract_type list in the Parameters guide.
last_sign_in
datetime: ISO 8601
Timestamp of the last sign in, YYYY-MM-DDThh:mm:ss.sssZ format
Example
Successful Listing of Projects (200)

Request
curl -v 'https://developer.api.autodesk.com/hq/v1/accounts/e3d5ef8d-5c37-4b9d-925d-1e6d24753ace/projects?limit=1&offset=0&sort=name' \
  -H 'Authorization: Bearer 9ezBnx9Rd5D1xG4KMt6b72T4w0MG'
Response
[
  {
    "id": "aca11a7a-bd17-47cd-ab99-6548d0e6fe25",
    "account_id": "e3d5ef8d-5c37-4b9d-925d-1e6d24753ace",
    "name": "construction_project",
    "start_date": "2015-05-02",
    "end_date": "2016-04-03",
    "project_type": "office",
    "value": 3000.0,
    "currency": "USD",
    "status": "pending",
    "job_number": "0219-01",
    "address_line_1": "The Fifth Avenue",
    "address_line_2": "#301",
    "city": "New York",
    "state_or_province": "New York",
    "postal_code": "10011",
    "country": "United States",
    "business_unit_id": "c17e6837-96cd-4839-868e-051a2ad65d28",
    "timezone": "America/New_York",
    "language": "en",
    "construction_type": "Renovation",
    "contract_type": "Design-Bid",
    "last_sign_in": null,
    "created_at": "2016-04-05T07:26:20.858Z",
    "updated_at": "2016-04-05T07:31:26.290Z"
  }
]


Documentation /BIM 360 API /API Reference
accounts/:account_id/projects
GET	accounts/{accountId}/projects
Retrieves a list of the projects in the specified account. If the user is an account admin or executive then all projects are returned; otherwise only projects that the user is assigned to are returned.

You can also use this endpoint to retrieve a list of project templates by setting the filter[classification] parameter to template or the filter[type] parameter to Template Project.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/admin/v1/accounts/:accountId/projects
Authentication Context	
user context optional
Required OAuth Scopes	
account:read
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via either a two-legged or three-legged OAuth flow.
Region
string
Specifies the region where your request should be routed. If not set, the request is routed automatically, which may result in a slight increase in latency.
Possible values: US, EMEA. For a complete list of supported regions, see the Regions page.

User-Id
string
The ID of a user on whose behalf your request is acting.
Your app has access to all users specified by the administrator in the SaaS integrations UI. Provide this header value to identify the user to be affected by the request.

You can use either the user’s ACC ID (id), or their Autodesk ID (autodeskId).

Note that this header is required for Account Admin POST, PATCH, and DELETE endpoints if you want to use a 2-legged authentication context. This header is optional for Account Admin GET endpoints.

* Required
Request
URI Parameters
accountId
string: UUID
The ID of the ACC account that contains the project being created or the projects being retrieved. This corresponds to the hub ID in the Data Management API. To convert a hub ID into an account ID, remove the “b." prefix. For example, a hub ID of b.c8b0c73d-3ae9 translates to an account ID of c8b0c73d-3ae9.
Request
Query String Parameters
fields
array: string
A comma-separated list of the project fields to include in the response. Default value: all fields.
Possible values: accountId, addressLine1, addressLine2, businessUnitId, city, companyCount, constructionType, country, createdAt, deliveryMethod, endDate, imageUrl, jobNumber, lastSignIn, latitude, longitude, memberCount, name, platform, postalCode, products, projectValue, sheetCount, startDate, stateOrProvince, status, thumbnailImageUrl, timezone, type and updatedAt.

filter[classification]
array: string
Filters projects by classification. Possible values:
production – Standard production projects. template – Project templates that can be cloned to create production projects. component – Placeholder projects that contain standardized components (e.g., forms) for use across projects. Only one component project is permitted per account. Known as a library in the ACC unified products UI. sample – The single sample project automatically created upon ACC trial setup. Only one sample project is permitted per account.

Max length: 255

filter[platform]
array: string
Filters by platform. Possible values: acc (Autodesk Construction Cloud) and bim360 (BIM 360).
Max length: 255

filter[products]
array: string
A comma-separated list of the products that the returned projects must use. Only projects that use one or more of the listed products are returned.
Note that every product that can be used in a project on the same platform (ACC or BIM 360) is activated for the project. All products associated with the project are returned in the response.

Some products are exclusive to ACC or to BIM 360, others are available on both platforms. Specify only the products on the appropriate platform for the projects you want to retrieve.

Possible ACC values: accountAdministration, autoSpecs, build, buildingConnected, capitalPlanning, cloudWorksharing, cost, designCollaboration, docs, financials, insight, modelCoordination, projectAdministration, takeoff, and workshopxr.

Possible BIM 360 values: accountAdministration, assets, cloudWorksharing, costManagement, designCollaboration, documentManagement, field, fieldManagement, glue, insight, modelCoordination, plan, projectAdministration, projectHome, projectManagement, and quantification.

filter[name]
string
Filters projects by name. Supports partial matches when used with filterTextMatch. For example filter[name]=ABCco&filterTextMatch=startsWith returns projects whose names start with “ABCco”.
Max length: 255

filter[type]
array: string
Filters by project type. To exclude a type, prefix it with - (e.g., -Bridge excludes bridge projects).
Possible values: Airport, Assisted Living / Nursing Home, Bridge, Canal / Waterway, Convention Center, Court House, Data Center, Dams / Flood Control / Reservoirs, Demonstration Project, Dormitory, Education Facility, Government Building, Harbor / River Development, Hospital, Hotel / Motel, Library, Manufacturing / Factory, Medical Laboratory, Medical Office, Military Facility, Mining Facility, Multi-Family Housing, Museum, Oil & Gas,``Plant``, Office, OutPatient Surgery Center, Parking Structure / Garage, Performing Arts, Power Plant, Prison / Correctional Facility, Rail, Recreation Building, Religious Building, Research Facility / Laboratory, Restaurant, Retail, Seaport, Single-Family Housing, Solar Farm, Stadium/Arena, Streets / Roads / Highways, Template Project, Theme Park, Training Project, Transportation Building, Tunnel, Utilities, Warehouse (non-manufacturing), Waste Water / Sewers, Water Supply, Wind Farm.

filter[status]
array: string
Filters projects by status. Possible values: active, pending, archived, suspended.
filter[businessUnitId]
string: UUID
The ID of the business unit that returned projects must be associated with.
Note that you can obtain this ID value by calling the GET business_units_structure endpoint to retrieve a list of business units. Use the id field of the returned business unit that you want to filter by.

Max length: 255

filter[jobNumber]
string
Filters by a user-defined project identifier. Supports partial matches when used with filterTextMatch. For example, filter[jobNumber]=HP-0002&filterTextMatch=equals returns projects where the job number is exactly “HP-0002”.
Max length: 255

filter[updatedAt]
string
Filters projects updated within a specific date range in ISO 8601 format. For example:
Date range: 2023-03-02T00:00:00.000Z..2023-03-03T23:59:59 .999Z Specific start date: 2023-03-02T00:00:00.000Z.. Specific end date: ..2023-03-02T23:59:59.999Z

For more details, see JSON API Filtering.

Max length: 100

filterTextMatch
enum:string
Specifies how text-based filters should match values in supported fields.
This parameter can be used in any endpoint that supports text-based filtering (e.g., filter[name], filter[jobNumber], filter[companyName], etc.).

Possible values:

contains (default) – Matches if the field contains the specified text anywhere

startsWith – Matches if the field starts with the specified text

endsWith – Matches if the field ends with the specified text

equals – Matches only if the field exactly matches the specified text

Matching is case-insensitive.

Wildcards and regular expressions are not supported.

sort
array: string
Sorts results by specified fields. Multiple fields can be used in order of priority. Each field can be followed by asc (ascending) or desc (descending). Default: asc.
For example, sort=name,createdAt desc sorts projects by name, then by creation date (newest first).

Possible values: name (the default), startDate, endDate, type, status, jobNumber, constructionType, deliveryMethod, contractType, currentPhase, companyCount, memberCount, createdAt and updatedAt.

limit
int
The maximum number of records to return in the response.
Default: 20

Minimum: 1

Maximum: 200 (If a larger value is provided, only 200 records are returned)

offset
int
The index of the first record to return.
Used for pagination in combination with the limit parameter.

Example: limit=20 and offset=40 returns records 41–60.

Response
HTTP Status Code Summary
200
OK
A list of requested projects.
400
Bad Request
The request could not be understood by the server due to malformed syntax.
401
Unauthorized
Request has not been applied because it lacks valid authentication credentials for the target resource.
403
Forbidden
The server understood the request but refuses to authorize it.
404
Not Found
The resource could not be found.
406
Not Acceptable
The server cannot produce a response matching the list of acceptable values defined in the request.
410
Access to the target resource is no longer available.
429
Too Many Requests
User has sent too many requests in a given amount of time.
500
Internal Server Error
An unexpected error occurred on the server.
503
Service Unavailable
Server is not ready to handle the request.
Response
Body Structure (200)
 Expand all
pagination
object
Contains pagination details for the records returned by the endpoint.
results
array: object
The requested page of projects.
Example 1
A list of requested projects.

Request
curl -v 'https://developer.api.autodesk.com/construction/admin/v1/accounts/d73fc742-4538-401c-8d0f-853b49b750b2/projects?fields=name,platform&filter[classification]=production,sample&filter[products]=build,docs&filter[name]=Sample Project&filter[type]=Convention Center,-Bridge&filter[status]=active,pending&filter[businessUnitId]=802a4a61-3507-4d4e-8e3c-242a31cc0549&filter[dataServiceId]=bd44763a-5184-483f-85e7-5d97fe589d55&filter[jobNumber]=HP-0002&filter[updatedAt]=2019-06-01T00:00:00.000Z..&filterTextMatch=contains&sort=name desc&limit=20' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 20,
    "offset": 10,
    "totalResults": 121,
    "nextUrl": "https://resource?limit=20&offset=30",
    "previousUrl": "https://resource?limit=20&offset=0"
  },
  "results": [
    {
      "id": "3e354e66-ac8b-41dd-9bc1-93fc182c25dd",
      "accountId": "d73fc742-4538-401c-8d0f-853b49b750b2",
      "addressLine1": "123 Main Street",
      "addressLine2": "Suite 2",
      "adminGroupId": "3456543",
      "businessUnitId": "802a4a61-3507-4d4e-8e3c-242a31cc0549",
      "city": "San Francisco",
      "classification": "production",
      "companyCount": 10,
      "constructionType": "New Construction",
      "contractType": "Unit Price",
      "country": "United States",
      "createdAt": "2018-01-01T12:45:00.000Z",
      "currentPhase": "Design",
      "deliveryMethod": "Design-Bid",
      "endDate": "2015-12-31",
      "imageUrl": "https://s3.us-east-1.amazonaws.com/project_image.png",
      "jobNumber": "HP-0002",
      "lastSignIn": "2019-01-01T12:45:00.000Z",
      "latitude": "37.773972",
      "longitude": "-122.431297",
      "memberCount": 100,
      "memberGroupId": "3456542",
      "name": "Sample Project",
      "platform": "bim360",
      "postalCode": "94001",
      "projectValue": {
        "value": 1650000,
        "currency": "USD"
      },
      "products": [
        {
          "key": "documentManagement",
          "status": "active",
          "icon": "https://s3.us-east-1.amazonaws.com/documentManagement.png",
          "name": "Document Management"
        },
        {
          "key": "fieldManagement",
          "status": "activating",
          "icon": "https://s3.us-east-1.amazonaws.com/fieldManagement.png",
          "name": "Field Management"
        }
      ],
      "sheetCount": 512,
      "startDate": "2010-01-01",
      "stateOrProvince": "California",
      "status": "active",
      "templateId": "10d18e9e-22ae-4186-a79c-819097afb646",
      "thumbnailImageUrl": "https://s3.us-east-1.amazonaws.com/project_thumbnail_image.png",
      "timezone": "America/Los_Angeles",
      "type": "Hospital",
      "updatedAt": "2019-01-01T12:45:00.000Z"
    }
  ]
}
Show Less
Example 2
A list of requested project templates.

Request
curl -v 'https://developer.api.autodesk.com/construction/admin/v1/accounts/063da365-32e5-452b-ac9a-b760635d42f3/projects?filter[classification]=template&filter[type]=Template%20Project&filter[updatedAt]=2019-06-01T00:00:00.000Z..&filterTextMatch=contains&sort=name desc&limit=20' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 20,
    "offset": 0,
    "totalResults": 5
  },
  "results": [
    {
      "id": "32a14c32-4916-4992-a33d-6d0b41c434a9",
      "accountId": "063da365-32e5-452b-ac9a-b760635d42f3",
      "addressLine1": null,
      "addressLine2": null,
      "adminGroupId": "226779812",
      "businessUnitId": null,
      "city": null,
      "classification": "template",
      "companyCount": 1,
      "constructionType": null,
      "contractType": null,
      "country": "US",
      "createdAt": "2022-11-29T07:40:52.109Z",
      "currentPhase": null,
      "deliveryMethod": null,
      "endDate": null,
      "imageUrl": "https://bim360-ea-ue1-prod-storage.s3.amazonaws.com/project-default-1.0.png",
      "jobNumber": null,
      "lastSignIn": null,
      "latitude": null,
      "longitude": null,
      "memberCount": 2,
      "memberGroupId": "226779811",
      "name": "ACC_Template",
      "platform": "acc",
      "postalCode": null,
      "projectValue": {
        "value": 0,
        "currency": "USD"
      },
      "products": [
        {
          "key": "docs",
          "name": "Docs",
          "status": "active",
          "language": "en",
          "icon": "https://bim360-ea-ue1-prod-storage.s3.amazonaws.com/products/docs.svg"
        },
        {
          "key": "designCollaboration",
          "name": "Design Collaboration",
          "status": "active",
          "language": "en",
          "icon": "https://bim360-ea-ue1-prod-storage.s3.amazonaws.com/products/dc.svg"
        },
        {
          "key": "modelCoordination",
          "name": "Model Coordination",
          "status": "active",
          "language": "en",
          "icon": "https://bim360-ea-ue1-prod-storage.s3.amazonaws.com/products/model.svg"
        }
      ],
      "sheetCount": null,
      "startDate": null,
      "stateOrProvince": null,
      "status": "active",
      "templateId": null,
      "thumbnailImageUrl": "https://bim360-ea-ue1-prod-storage.s3.amazonaws.com/project-default-1.0.png",
      "timezone": null,
      "type": "Template Project",
      "updatedAt": "2022-11-29T07:40:56.661Z"
    }
  ]
}

Documentation /BIM 360 API /API Reference
Projects
GET	projects/:project_id
Query the details of a specific BIM 360 project.

Note that this endpoint is ONLY compatible with BIM 360 projects. It is not compatible with Autodesk Construction Cloud (ACC) projects. For more information about compatibility between between BIM 360 and ACC, see the Compatibility section.

Resource Information
Method and URI（US）	
GET	https://developer.api.autodesk.com/hq/v1/accounts/:account_id/projects/:project_id
Method and URI（Legacy）	
GET	https://developer.api.autodesk.com/hq/v1/regions/eu/accounts/:account_id/projects/:project_id
Authentication Context	
app only
Required OAuth Scopes	
account:read
Data Formats	
JSON
Request
Headers
Authorization
yes
Must be Bearer <token>, where <token> is obtained via a two-legged OAuth flow.
Region
no
Specifies the region where the service is located. Possible values: US, EMEA. For the full list of supported regions, see the Regions page.
Request
URI Parameters
account_id
string: UUID
The account ID of the project. This corresponds to hub ID in the Data Management API. To convert a hub ID into an account ID you need to remove the “b." prefix. For example, a hub ID of b.c8b0c73d-3ae9 translates to an account ID of c8b0c73d-3ae9.
project_id
string: UUID
The ID of the project. This corresponds to project ID in the Data Management API. To convert a project ID in the Data Management API into a project ID in the BIM 360 API you need to remove the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.
Response
HTTP Status Code Summary
200
OK
The request has succeeded.
400
Bad Request
The request could not be understood by the server due to malformed syntax.
403
Forbidden
Unauthorized
404
Not Found
The resource cannot be found.
409
Conflict
The request could not be completed due to a conflict with the current state of the resource.
422
Unprocessable Entity
The request was unable to be followed due to restrictions.
500
Internal Server Error
An unexpected error occurred on the server.
Response
Body Structure (200)
The response body is a single, flat JSON object with the following attributes.

id
string: UUID
Project ID
account_id
string: UUID
Account ID
name
string
Name of the project
Max length: 255
start_date
date
The starting date of a project; must be earlier than end_date

Format: YYYY-MM-DD
end_date
date
The ending date of a project; must be later than start_date

Format: YYYY-MM-DD
project_type
string
The type of project; accepts preconfigured and customized project types

Max length: 255

Refer to the preconfigured project_type list in
the Parameters guide.
value
float
Monetary value of the project
currency
enum: string
Currency for project value

Refer to the currency list in the Parameters guide.
status
enum: string
The status of project.

Possible values:
active: project is active with at least one project admin added
pending: project has been created but pending becuase no project admin added
inactive: project is suspended
archived: project is archived and displayed only in the archived list
job_number
string
Project job number to connect a BIM 360 project to project or job in a financial or ERP system.

Max length: 100
address_line_1
string
Project address line 1

Max length: 255
address_line_2
string
Project address line 2

Max length: 255
city
string
City in which project is located

Max length: 255
state_or_province
enum: string
State or province in which project is located

Max length: 255

Note that the state_or_province value depends on the selected country value; see the valid values in the state_or_province list in the Parameters guide.
postal_code
string
Postal code for the project location

Max length: 255
country
enum: string
Country for this project

Refer to the country list in the Parameters guide.
business_unit_id
string: UUID
The business unit ID of this project
timezone
string
Time zone for this project

Refer to the timezone list in the Parameters guide.
language
enum: string
Language of the project; applicable to the BIM 360 Field service only

Possible values:
en: English
de: German
construction_type
enum: string
Type of construction

Refer to the construction_type list in the Parameters guide.
contract_type
enum: string
Contract Type for your project

Refer to the constract_type list in the Parameters guide.
last_sign_in
datetime: ISO 8601
Timestamp of the last sign in, YYYY-MM-DDThh:mm:ss.sssZ format
service_types
enum: string
The services in which the project has been activated. Multiple services are separated with commas.
Note that in order for the service to be set as active in the BIM 360 Account Administration UI, you need to add an admin user to the service.

Refer to the preconfigured service_type list in
the Parameters guide.
Example
Successful Listing of a Requested Project (200)

Request
curl -v 'https://developer.api.autodesk.com/hq/v1/accounts/e3d5ef8d-5c37-4b9d-925d-1e6d24753ace/projects/aca11a7a-bd17-47cd-ab99-6548d0e6fe25' \
  -H 'Authorization: Bearer 9ezBnx9Rd5D1xG4KMt6b72T4w0MG'
Response
{
  "id": "aca11a7a-bd17-47cd-ab99-6548d0e6fe25",
  "account_id": "e3d5ef8d-5c37-4b9d-925d-1e6d24753ace",
  "name": "construction_project",
  "start_date": "2015-05-02",
  "end_date": "2016-04-03",
  "project_type": "office",
  "value": 3000.0,
  "currency": "USD",
  "status": "pending",
  "job_number": "0219-01",
  "address_line_1": "The Fifth Avenue",
  "address_line_2": "#301",
  "city": "New York",
  "state_or_province": "New York",
  "postal_code": "10011",
  "country": "United States",
  "business_unit_id": "c17e6837-96cd-4839-868e-051a2ad65d28",
  "timezone": "America/New_York",
  "language": "en",
  "construction_type": "Renovation",
  "contract_type": "Design-Bid",
  "last_sign_in": null,
  "service_types": "glue,doc_manager",
  "created_at": "2016-04-05T07:26:20.858Z",
  "updated_at": "2016-04-05T07:31:26.290Z"
}


Documentation /BIM 360 API /API Reference
projects/:project_id
GET	projects/{projectId}
Retrieves a project specified by project ID. You can find the project ID by calling GET /accounts/{accountId}/projects and examining results.id in the response.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/admin/v1/projects/:projectId
Authentication Context	
user context optional
Required OAuth Scopes	
account:read
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via either a two-legged or three-legged OAuth flow.
Region
string
Specifies the region where your request should be routed. If not set, the request is routed automatically, which may result in a slight increase in latency.
Possible values: US, EMEA. For a complete list of supported regions, see the Regions page.

User-Id
string
The ID of a user on whose behalf your request is acting.
Your app has access to all users specified by the administrator in the SaaS integrations UI. Provide this header value to identify the user to be affected by the request.

You can use either the user’s ACC ID (id), or their Autodesk ID (autodeskId).

Note that this header is required for Account Admin POST, PATCH, and DELETE endpoints if you want to use a 2-legged authentication context. This header is optional for Account Admin GET endpoints.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project. This corresponds to project ID in the Data Management API. To convert a project ID in the Data Management API into a project ID in the ACC API you need to remove the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.
Request
Query String Parameters
fields
array: string
A comma-separated list of the project fields to include in the response. Default value: all fields.
Possible values: accountId, addressLine1, addressLine2, businessUnitId, city, companyCount, constructionType, country, createdAt, deliveryMethod, endDate, imageUrl, jobNumber, lastSignIn, latitude, longitude, memberCount, name, platform, postalCode, products, projectValue, sheetCount, startDate, stateOrProvince, status, thumbnailImageUrl, timezone, type and updatedAt.

Response
HTTP Status Code Summary
200
OK
The requested project.
400
Bad Request
The request could not be understood by the server due to malformed syntax.
401
Unauthorized
Request has not been applied because it lacks valid authentication credentials for the target resource.
403
Forbidden
The server understood the request but refuses to authorize it.
404
Not Found
The resource could not be found.
406
Not Acceptable
The server cannot produce a response matching the list of acceptable values defined in the request.
409
Conflict
The request could not be completed due to a conflict with the current state of the resource.
410
Access to the target resource is no longer available.
429
Too Many Requests
User has sent too many requests in a given amount of time.
500
Internal Server Error
An unexpected error occurred on the server.
503
Service Unavailable
Server is not ready to handle the request.
Response
Body Structure (200)
 Expand all
id
string: UUID
The internally generated ID for the project.
name
string
The name of the project.
Max length: 255

startDate
null,string
The estimated start date for the project, in ISO 8601 format.
endDate
null,string
The estimated end date for the project, in ISO 8601 format.
type
string
The type of the project. Any value is accepted, but the following are recommended:
Possible values: Convention Center, Data Center, Hotel / Motel, Office, Parking Structure / Garage, Performing Arts, Restaurant, Retail, Stadium / Arena, Theme Park, Warehouse (non-manufacturing), Assisted Living / Nursing Home, Hospital, Medical Laboratory, Medical Office, OutPatient Surgery Center, Court House, Dormitory, Education Facility, Government Building, Library, Military Facility, Museum, Prison / Correctional Facility, Recreation Building, Religious Building, Research Facility / Laboratory, Multi-Family Housing, Single-Family Housing, Airport, Bridge, Canal / Waterway, Dams / Flood Control / Reservoirs, Harbor / River Development, Rail, Seaport, Streets / Roads / Highways, Transportation Building, Tunnel, Waste Water / Sewers, Water Supply, Manufacturing / Factory, Mining Facility, Oil & Gas, Plant, Power Plant, Solar Farm, Utilities, Wind Farm, Demonstration Project, Template Project and Training Project.

Max length: 255

classification
enum:string
The classification of the project. Possible values:
production – Standard project.
template – A project that serves as a template for creating new projects.
component – A placeholder project containing reusable components (e.g., forms). Only one component project is allowed per account. Known as a library in the ACC UI.
sample – A single sample project automatically created for ACC trials (limited to one per account).
projectValue
object
Contains details about the estimated cost of the project, including the amount (value) and the currency (currency).
status
enum:string
The status of the project.
Possible values: active, pending, archived and suspended.

jobNumber
string
A user-defined identifier for the project. This value is assigned when the project is created and can be used to filter projects. It supports partial matches when used with filterTextMatch.
Max length: 100

addressLine1
null,string
The first line of the project’s address.
Max length: 255

addressLine2
null,string
Additional address details for the project location.
Max length: 255

city
null,string
The city wher the project is located.
Max length: 255

stateOrProvince
null,string
The state or province where the project is located. It must be a valid name or an ISO 3166-2 code. The provided state or province must exist in the country of the project.
Max length: 255

postalCode
null,string
The postal or ZIP code of the project location.
Max length: 255

country
null,string
The country where the project is located, using an ISO 3166-1 code.
Max length: 255

latitude
null,string
The latitude coordinate of the project location.
Max length: 25

longitude
null,string
The longitude coordinate of the project location.
Max length: 25

timezone
null,string
The time zone where the project is located. It must be a valid IANA time zone name from the IANA Time Zone Database (e.g., America/New_York). If no time zone is set, this field may be null. Possible values: Pacific/Honolulu, America/Juneau, America/Los_Angeles, America/Phoenix, America/Denver, America/Chicago, America/New_York, America/Indiana/Indianapolis, Pacific/Pago_Pago, Pacific/Midway, America/Tijuana, America/Chihuahua, America/Mazatlan, America/Guatemala, America/Mexico_City, America/Monterrey, America/Regina, America/Bogota, America/Lima, America/Caracas, America/Halifax, America/Guyana, America/La_Paz, America/Santiago, America/St_Johns, America/Sao_Paulo, America/Argentina/Buenos_Aires, America/Godthab, Atlantic/South_Georgia, Atlantic/Azores, Atlantic/Cape_Verde, Africa/Casablanca, Europe/Dublin, Europe/Lisbon, Europe/London, Africa/Monrovia, Etc/UTC, Europe/Amsterdam, Europe/Belgrade, Europe/Berlin, Europe/Bratislava, Europe/Brussels, Europe/Budapest, Europe/Copenhagen, Europe/Ljubljana, Europe/Madrid, Europe/Paris, Europe/Prague, Europe/Rome, Europe/Sarajevo, Europe/Skopje, Europe/Stockholm, Europe/Vienna, Europe/Warsaw, Africa/Algiers, Europe/Zagreb, Europe/Athens, Europe/Bucharest, Africa/Cairo, Africa/Harare, Europe/Helsinki, Europe/Istanbul, Asia/Jerusalem, Europe/Kiev, Africa/Johannesburg, Europe/Riga, Europe/Sofia, Europe/Tallinn, Europe/Vilnius, Asia/Baghdad, Asia/Kuwait, Europe/Minsk, Africa/Nairobi, Asia/Riyadh, Asia/Tehran, Asia/Muscat, Asia/Baku, Europe/Moscow, Asia/Tbilisi, Asia/Yerevan, Asia/Kabul, Asia/Karachi, Asia/Tashkent, Asia/Kolkata, Asia/Colombo, Asia/Kathmandu, Asia/Almaty, Asia/Dhaka, Asia/Yekaterinburg, Asia/Rangoon, Asia/Bangkok, Asia/Jakarta, Asia/Novosibirsk, Asia/Shanghai, Asia/Chongqing, Asia/Hong_Kong, Asia/Krasnoyarsk, Asia/Kuala_Lumpur, Australia/Perth, Asia/Singapore, Asia/Taipei, Asia/Ulaanbaatar, Asia/Urumqi, Asia/Irkutsk, Asia/Tokyo, Asia/Seoul, Australia/Adelaide, Australia/Darwin, Australia/Brisbane, Australia/Melbourne, Pacific/Guam, Australia/Hobart, Pacific/Port_Moresby, Australia/Sydney, Asia/Yakutsk, Pacific/Noumea, Asia/Vladivostok, Pacific/Auckland, Pacific/Fiji, Asia/Kamchatka, Asia/Magadan, Pacific/Majuro, Pacific/Guadalcanal, Pacific/Tongatapu, Pacific/Apia, Pacific/Fakaofo
constructionType
string
The type of construction for the project. Recommended values: New Construction, Renovation. Any value is accepted.
deliveryMethod
string
The method used to deliver the project. Recommended values include Design-Bid-Build, Construction Management (CM) at Risk, and Integrated Project Delivery (IPD). Any value is accepted.
contractType
string
The type of contract for the project. For example, Lump Sum, Cost Plus, Guaranteed Maximum Price, Unit Price. Any value is accepted.
currentPhase
string
The current phase of the project. Recommended values include, Concept, Design, Bidding, Planning, Preconstruction, Construction, Commissioning, Warranty, Complete, Facility Management, Operation, Strategic Definition, Preparation and Brief, Concept Design, Developed Design, Technical Design, Construction, Handover and Close Out and In Use.
Any value is accepted.

imageUrl
string
The URL of the main image associated with the project. This field can be null.
Max length: 255

thumbnailImageUrl
string
The URL of the project’s thumbnail image. This field can be null.
Max length: 255

createdAt
datetime: ISO 8601
The timestamp when the project was created, in ISO 8601 format. This value is set at creation and does not change.
updatedAt
datetime: ISO 8601
The timestamp when the project was last updated, in ISO 8601 format. This reflects changes to project fields but not updates to resources within the project.
accountId
string: UUID
The account ID associated with the project.
sheetCount
null,integer
The total number of sheets associated with the project.
Note that this field is relevant only in responses. It is ignored in requests.

platform
enum:string
The APS platform where the project is stored. Possible values: acc, bim360.
Note that this field is relevant only in responses. It is ignored in requests.

businessUnitId
string: UUID
The ID of the business unit that the project is associated with.
lastSignIn
datetime: ISO 8601
The timestamp of the last time someone signed into the project.
memberGroupId
string
Not relevant
Max length: 25

adminGroupId
string
Not relevant
Max length: 25

products
array
An array of the product objects associated with the project.
Note that this array is relevant only in responses. It is ignored in requests.

When a project is created, every product in the same account as the project is activated for the project. You can call PATCH users/:userId to separately activate one or more of the returned products for each user assigned to the project.

companyCount
int
The total number of companies associated with the project.
Note that this field is relevant only in responses. It is ignored in requests.

memberCount
int
The total number of members on the project.
Note that this field is relevant only in responses. It is ignored in requests.

templateId
string: UUID
The ID of the project that was used as a template to create this project.
Example
The requested project.

Request
curl -v 'https://developer.api.autodesk.com/construction/admin/v1/projects/367d5cc2-9008-462c-96e5-c9491db85d93?fields=name,platform' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "id": "3e354e66-ac8b-41dd-9bc1-93fc182c25dd",
  "name": "Sample Project",
  "startDate": "2010-01-01",
  "endDate": "2015-12-31",
  "type": "Hospital",
  "classification": "production",
  "projectValue": {
    "value": 1650000,
    "currency": "USD"
  },
  "status": "active",
  "jobNumber": "HP-0002",
  "addressLine1": "123 Main Street",
  "addressLine2": "Suite 2",
  "city": "San Francisco",
  "stateOrProvince": "California",
  "postalCode": "94001",
  "country": "United States",
  "latitude": "37.773972",
  "longitude": "-122.431297",
  "timezone": "America/Los_Angeles",
  "constructionType": "New Construction",
  "deliveryMethod": "Design-Bid",
  "contractType": "Unit Price",
  "currentPhase": "Design",
  "imageUrl": "https://s3.us-east-1.amazonaws.com/project_image.png",
  "thumbnailImageUrl": "https://s3.us-east-1.amazonaws.com/project_thumbnail_image.png",
  "createdAt": "2018-01-01T12:45:00.000Z",
  "updatedAt": "2019-01-01T12:45:00.000Z",
  "accountId": "d73fc742-4538-401c-8d0f-853b49b750b2",
  "sheetCount": 512,
  "platform": "acc",
  "businessUnitId": "802a4a61-3507-4d4e-8e3c-242a31cc0549",
  "lastSignIn": "2019-01-01T12:45:00.000Z",
  "memberGroupId": "3456542",
  "adminGroupId": "3456543",
  "products": [
    {
      "key": "docs",
      "status": "active",
      "icon": "https://bim360-ea-ue1-prod-storage.s3.amazonaws.com/products/docs.svg",
      "name": "Docs",
      "language": "en"
    },
    {
      "key": "designCollaboration",
      "status": "activating",
      "icon": "https://bim360-ea-ue1-prod-storage.s3.amazonaws.com/products/dc.svg",
      "name": "Design Collaboration",
      "language": "en"
    },
    {
      "key": "modelCoordination",
      "status": "activating",
      "icon": "https://bim360-ea-ue1-prod-storage.s3.amazonaws.com/products/model.svg",
      "name": "Model Coordination",
      "language": "en"
    },
    {
      "key": "takeoff",
      "status": "activating",
      "icon": "https://bim360-ea-ue1-prod-storage.s3.amazonaws.com/products/quantify.svg",
      "name": "Takeoff",
      "language": "en"
    },
    {
      "key": "autoSpecs",
      "status": "activating",
      "icon": "https://bim360-ea-ue1-prod-storage.s3.amazonaws.com/tools/autospecs.svg",
      "name": "AutoSpecs",
      "language": "en"
    },
    {
      "key": "build",
      "status": "activating",
      "icon": "https://bim360-ea-ue1-prod-storage.s3.amazonaws.com/products/build.svg",
      "name": "Build",
      "language": "en"
    },
    {
      "key": "cost",
      "status": "activating",
      "icon": "https://bim360-ea-ue1-prod-storage.s3.amazonaws.com/products/cost.svg",
      "name": "Cost Management",
      "language": "en"
    },
    {
      "key": "insight",
      "status": "activating",
      "icon": "https://bim360-ea-ue1-prod-storage.s3.amazonaws.com/products/insight.svg",
      "name": "Insight",
      "language": "en"
    },
    {
      "key": "projectAdministration",
      "status": "activating",
      "icon": "https://bim360-ea-ue1-prod-storage.s3.amazonaws.com/tools/settings.svg",
      "name": "Project Admin",
      "language": "en"
    },
    {
      "key": "accountAdministration",
      "status": "activating",
      "icon": "hhttps://bim360-ea-ue1-prod-storage.s3.amazonaws.com/tools/settings.svg",
      "name": "Account Admin",
      "language": "en"
    }
  ],
  "companyCount": 10,
  "memberCount": 100,
  "templateId": null
}

Documentation /BIM 360 API /API Reference
Companies
GET	companies
Query all the partner companies in a specific BIM 360 account.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/hq/v1/accounts/:account_id/companies
Method and URI (Legacy)	
GET	https://developer.api.autodesk.com/hq/v1/regions/eu/accounts/:account_id/companies
Authentication Context	
app only
Required OAuth Scopes	
account:read
Data Format	
JSON
Request
Headers
Authorization
yes
Must be Bearer <token>, where <token> is obtained via a two-legged OAuth flow.
Region
no
Specifies the region where the service is located. Possible values: US, EMEA. For the full list of supported regions, see the Regions page.
Request
URI Parameters
account_id
string: UUID
The account ID of the company. This corresponds to hub ID in the Data Management API. To convert a hub ID into an account ID you need to remove the “b." prefix. For example, a hub ID of b.c8b0c73d-3ae9 translates to an account ID of c8b0c73d-3ae9.
Request
Query String Parameters
limit
int
Response array’s size
Default value: 10
Max limit: 100
offset
int
Offset of response array
Default value: 0
sort
string
Comma-separated fields to sort by in ascending order

Prepending a field with - sorts in descending order
Invalid fields and whitespaces will be ignored
field
string
Comma-separated fields to include in response

id will always be returned
Invalid fields will be ignored
Response
HTTP Status Code Summary
200
OK
The request has succeeded
400
Bad Request
The request could not be understood by the server due to malformed syntax
403
Forbidden
Unauthorized
404
Not Found
The resource cannot be found
409
Conflict
The request could not be completed due to a conflict with the current state of the resource
422
Unprocessable Entity
The request was unable to be followed due to restrictions
500
Internal Server Error
An unexpected error occurred on the server
Response
Body Structure (200)
A successful response is an array of companies, flat JSON objects with the following attributes:

id
string: UUID
Company ID
account_id
string: UUID
Account ID
name
string
Company name should be unique under an account

Max length: 255
trade
string
Trade type based on specialization

Refer to the trade list in the Parameters guide.
address_line_1
string
Company address line 1

Max length: 255
address_line_2
string
Company address line 2

Max length: 255
city
string
City in which company is located

Max length: 255
state_or_province
enum: string
State or province in which company is located

Max length: 255

Note that the state_or_province value depends on the selected country value; see the valid values in the state_or_province list in the Parameters guide.
postal_code
string
Postal code for the company location

Max length: 255
country
enum: string
Country for this company

Refer to the country list in the Parameters guide.
phone
string
Business phone number for the company

Max length: 255
website_url
string
Company website

Max length: 255
description
string
Short description or overview for company

Max length: 255
erp_id
string
Used to associate a company in BIM 360 with the company data in an ERP system
tax_id
string
Used to associate a company in BIM 360 with the company data from public and industry sources
Example
Successful Listing of Companies in an Account (200)

Request
curl -v 'https://developer.api.autodesk.com/hq/v1/accounts/80793a28-f9b1-4888-9533-5f00cddcd6fb/companies?limit=1&offset=0' \
  -H 'Authorization: Bearer 07YyCEjv3qs8FA7ysntmsuErYXHv'
Response
[
  {
    "id": "fc830fd8-f1ef-4cd6-9163-fb115dc698d7",
    "account_id": "80793a28-f9b1-4888-9533-5f00cddcd6fb",
    "name": "Autodesk",
    "trade": "Concrete",
    "address_line_1": "The Fifth Avenue",
    "address_line_2": "#301",
    "city": "New York",
    "postal_code": "10011",
    "state_or_province": "New York",
    "country": "United States",
    "phone": "(503)623-1525",
    "website_url": "http://www.autodesk.com",
    "description": "Autodesk, Inc., is a leader in 3D design, engineering and entertainment software.",
    "created_at": "2016-05-20T02:24:21.400Z",
    "updated_at": "2016-05-20T02:24:21.400Z",
    "erp_id": "c79bf096-5a3e-41a4-aaf8-a771ed329047",
    "tax_id": "213-73-8867"
  }
]

Documentation /BIM 360 API /API Reference
Companies
GET	companies/:company_id
Query the details of a specific partner company.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/hq/v1/accounts/:account_id/companies/:company_id
Method and URI (Legacy)	
GET	https://developer.api.autodesk.com/hq/v1/regions/eu/accounts/:account_id/companies/:company_id
Authentication Context	
app only
Required OAuth Scopes	
account:read
Data Formats	
JSON
Request
Headers
Authorization
yes
Must be Bearer <token>, where <token> is obtained via a two-legged OAuth flow.
Region
no
Specifies the region where the service is located. Possible values: US, EMEA. For the full list of supported regions, see the Regions page.
Request
URI Parameters
account_id
string: UUID
The account ID of the company. This corresponds to hub ID in the Data Management API. To convert a hub ID into an account ID you need to remove the “b." prefix. For example, a hub ID of b.c8b0c73d-3ae9 translates to an account ID of c8b0c73d-3ae9.
company_id
string: UUID
Company ID
Response
HTTP Status Code Summary
200
OK
The request has succeeded.
400
Bad Request
The request could not be understood by the server due to malformed syntax.
403
Forbidden
Unauthorized
404
Not Found
The resource cannot be found.
409
Conflict
The request could not be completed due to a conflict with the current state of the resource.
422
Unprocessable Entity
The request was unable to be followed due to restrictions.
500
Internal Server Error
An unexpected error occurred on the server.
Response
Body Structure (200)
A successful response is a company, a flat JSON object with the following attributes:

id
string: UUID
Company ID
account_id
string: UUID
Account ID
name
string
Company name should be unique under an account

Max length: 255
trade
string
Trade type based on specialization

Refer to the trade list in the Parameters guide.
address_line_1
string
Company address line 1

Max length: 255
address_line_2
string
Company address line 2

Max length: 255
city
string
City in which company is located

Max length: 255
state_or_province
enum: string
State or province in which company is located

Max length: 255

Note that the state_or_province value depends on the selected country value; see the valid values in the state_or_province list in the Parameters guide.
postal_code
string
Postal code for the company location

Max length: 255
country
enum: string
Country for this company

Refer to the country list in the Parameters guide.
phone
string
Business phone number for the company

Max length: 255
website_url
string
Company website

Max length: 255
description
string
Short description or overview for company

Max length: 255
erp_id
string
Used to associate a company in BIM 360 with the company data in an ERP system
tax_id
string
Used to associate a company in BIM 360 with the company data from public and industry sources
Example
Successful Listing of a Requested Company (200)

Request
curl -v 'https://developer.api.autodesk.com/hq/v1/accounts/80793a28-f9b1-4888-9533-5f00cddcd6fb/companies/fc830fd8-f1ef-4cd6-9163-fb115dc698d7' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "id": "fc830fd8-f1ef-4cd6-9163-fb115dc698d7",
  "account_id": "80793a28-f9b1-4888-9533-5f00cddcd6fb",
  "name": "Autodesk",
  "trade": "Concrete",
  "address_line_1": "The Fifth Avenue",
  "address_line_2": "#301",
  "city": "New York",
  "postal_code": "10011",
  "state_or_province": "New York",
  "country": "United States",
  "phone": "(503)623-1525",
  "website_url": "http://www.autodesk.com",
  "description": "Autodesk, Inc., is a leader in 3D design, engineering and entertainment software.",
  "created_at": "2016-05-20T02:24:21.400Z",
  "updated_at": "2016-05-20T02:24:21.400Z",
  "erp_id": "c79bf096-5a3e-41a4-aaf8-a771ed329047",
  "tax_id": "213-73-8867"
}

Documentation /BIM 360 API /API Reference
Companies
GET	companies/search
Search partner companies in a specific BIM 360 account by name.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/hq/v1/accounts/:account_id/companies/search
Method and URI (Legacy)	
GET	https://developer.api.autodesk.com/hq/v1/regions/eu/accounts/:account_id/companies/search
Authentication Context	
app only
Required OAuth Scopes	
account:read
Data Formats	
JSON
Request
Headers
Authorization
yes
Must be Bearer <token>, where <token> is obtained via a two-legged OAuth flow.
Region
no
Specifies the region where the service is located. Possible values: US, EMEA. For the full list of supported regions, see the Regions page.
Request
URI Parameters
account_id
string: UUID
The account ID of the company. This corresponds to hub ID in the Data Management API. To convert a hub ID into an account ID you need to remove the “b." prefix. For example, a hub ID of b.c8b0c73d-3ae9 translates to an account ID of c8b0c73d-3ae9.
Request
Query String Parameters
name
string
Company name to match
Max length: 255
trade
string
Company trade to match
Max length: 255
operator
enum: string
Boolean operator to use: OR (default) or AND
partial
bool
If true (default), perform a fuzzy match
limit
int
Response array’s size
Default value: 10
Max limit: 100
offset
int
Offset of response array
Default value: 0
sort
string
Comma-separated fields to sort by in ascending order

Prepending a field with - sorts in descending order.
Invalid fields and whitespaces will be ignored.
field
string
Comma-separated fields to include in response

id will always be returned.
Invalid fields will be ignored.
Response
HTTP Status Code Summary
200
OK
The request has succeeded.
400
Bad Request
The request could not be understood by the server due to malformed syntax.
403
Forbidden
Unauthorized
404
Not Found
The resource cannot be found.
409
Conflict
The request could not be completed due to a conflict with the current state of the resource.
422
Unprocessable Entity
The request was unable to be followed due to restrictions.
500
Internal Server Error
An unexpected error occurred on the server.
Response
Body Structure (200)
A successful response is an array of companies, flat JSON objects with the following attributes:

id
string: UUID
Company ID
account_id
string: UUID
Account ID
name
string
Company name should be unique under an account

Max length: 255
trade
string
Trade type based on specialization

Refer to the trade list in the Parameters guide.
address_line_1
string
Company address line 1

Max length: 255
address_line_2
string
Company address line 2

Max length: 255
city
string
City in which company is located

Max length: 255
state_or_province
enum: string
State or province in which company is located

Max length: 255

Note that the state_or_province value depends on the selected country value; see the valid values in the state_or_province list in the Parameters guide.
postal_code
string
Postal code for the company location

Max length: 255
country
enum: string
Country for this company

Refer to the country list in the Parameters guide.
phone
string
Business phone number for the company

Max length: 255
website_url
string
Company website

Max length: 255
description
string
Short description or overview for company

Max length: 255
erp_id
string
Used to associate a company in BIM 360 with the company data in an ERP system
tax_id
string
Used to associate a company in BIM 360 with the company data from public and industry sources
Example
Successful Search for Company by Name (200)

Reqeust
curl -v 'https://developer.api.autodesk.com/hq/v1/accounts/80793a28-f9b1-4888-9533-5f00cddcd6fb/companies/search?name=Autodesk&limit=1&offset=0' \
  -H 'Authorization: Bearer KmE9JOw2PrRpqEhFsrFWbyktnnQA'
Response
[
  {
    "id": "fc830fd8-f1ef-4cd6-9163-fb115dc698d7",
    "account_id": "80793a28-f9b1-4888-9533-5f00cddcd6fb",
    "name": "Autodesk",
    "trade": "Concrete",
    "address_line_1": "The Fifth Avenue",
    "address_line_2": "#301",
    "city": "New York",
    "postal_code": "10011",
    "state_or_province": "New York",
    "country": "United States",
    "phone": "(503)623-1525",
    "website_url": "http://www.autodesk.com",
    "description": "Autodesk, Inc., is a leader in 3D design, engineering and entertainment software.",
    "created_at": "2016-05-20T02:24:21.400Z",
    "updated_at": "2016-05-20T06:28:58.490Z",
    "erp_id": "c79bf096-5a3e-41a4-aaf8-a771ed329047",
    "tax_id": "213-73-8867"
  }
]

Documentation /BIM 360 API /API Reference
Companies
GET	projects/:project_id/companies
Query all the partner companies in a specific BIM 360 project.

To query all the partner companies in the account, see GET companies.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/hq/v1/accounts/:account_id/projects/:project_id/companies
Method and URI (Legacy)	
GET	https://developer.api.autodesk.com/hq/v1/regions/eu/accounts/:account_id/projects/:project_id/companies
Authentication Context	
app only
Required OAuth Scopes	
account:read
Data Format	
JSON
Request
Headers
Authorization
yes
Must be Bearer <token>, where <token> is obtained via a two-legged OAuth flow.
Region
no
Specifies the region where the service is located. Possible values: US, EMEA. For the full list of supported regions, see the Regions page.
Request
URI Parameters
account_id
string: UUID
The account ID of the project. This corresponds to hub ID in the Data Management API. To convert a hub ID into an account ID you need to remove the “b." prefix. For example, a hub ID of b.c8b0c73d-3ae9 translates to an account ID of c8b0c73d-3ae9.
project_id
string: UUID
The ID of the project. This corresponds to project ID in the Data Management API. To convert a project ID in the Data Management API into a project ID in the BIM 360 API you need to remove the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.
Request
Query String Parameters
limit
int
Response array’s size
Default value: 10
Max limit: 100
offset
int
Offset of response array
Default value: 0
sort
string
Comma-separated fields to sort by in ascending order

Prepending a field with - sorts in descending order
Invalid fields and whitespaces will be ignored
field
string
Comma-separated fields to include in response

id will always be returned
Invalid fields will be ignored
Response
HTTP Status Code Summary
200
OK
The request has succeeded
400
Bad Request
The request could not be understood by the server due to malformed syntax
403
Forbidden
Unauthorized
404
Not Found
The resource cannot be found
409
Conflict
The request could not be completed due to a conflict with the current state of the resource
422
Unprocessable Entity
The request was unable to be followed due to restrictions
500
Internal Server Error
An unexpected error occurred on the server
Response
Body Structure (200)
A successful response is an array of companies, flat JSON objects with the following attributes:

id
string: UUID
Company ID
account_id
string: UUID
Account ID
project_id
string: UUID
Project ID
name
string
Company name should be unique under an account

Max length: 255
trade
string
Trade type based on specialization

Refer to the trade list in the Parameters guide.
address_line_1
string
Company address line 1

Max length: 255
address_line_2
string
Company address line 2

Max length: 255
city
string
City in which company is located

Max length: 255
state_or_province
enum: string
State or province in which company is located

Max length: 255

Note that the state_or_province value depends on the selected country value; see the valid values in the state_or_province list in the Parameters guide.
postal_code
string
Postal code for the company location

Max length: 255
country
enum: string
Country for this company

Refer to the country list in the Parameters guide.
phone
string
Business phone number for the company

Max length: 255
website_url
string
Company website

Max length: 255
description
string
Short description or overview for company

Max length: 255
erp_id
string
Used to associate a company in BIM 360 with the company data in an ERP system
tax_id
string
Used to associate a company in BIM 360 with the company data from public and industry sources
member_group_id
string
The Autodesk ID of the company; used to identify which company is assigned to an RFI or Issue.
Example
Successful Listing of Companies in an Account (200)

Request
curl -v 'https://developer.api.autodesk.com/hq/v1/accounts/80793a28-f9b1-4888-9533-5f00cddcd6fb/projects/1e4bdc48-1bd7-4a4f-a91f-bd238cce5830/companies?limit=1&offset=0' \
  -H 'Authorization: Bearer 07YyCEjv3qs8FA7ysntmsuErYXHv'
Response
[
  {
    "id": "fc830fd8-f1ef-4cd6-9163-fb115dc698d7",
    "account_id": "80793a28-f9b1-4888-9533-5f00cddcd6fb",
    "project_id": "1e4bdc48-1bd7-4a4f-a91f-bd238cce5830",
    "name": "Autodesk",
    "trade": "Concrete",
    "address_line_1": "The Fifth Avenue",
    "address_line_2": "#301",
    "city": "New York",
    "postal_code": "10011",
    "state_or_province": "New York",
    "country": "United States",
    "phone": "(503)623-1525",
    "website_url": "http://www.autodesk.com",
    "description": "Autodesk, Inc., is a leader in 3D design, engineering and entertainment software.",
    "created_at": "2016-05-20T02:24:21.400Z",
    "updated_at": "2016-05-20T02:24:21.400Z",
    "erp_id": "c79bf096-5a3e-41a4-aaf8-a771ed329047",
    "tax_id": "213-73-8867",
    "member_group_id": "764893"
  }
]


Documentation /BIM 360 API /API Reference
accounts/:accountId/companies
GET	accounts/{accountId}/companies
Returns a list of companies in an account.

You can also use this endpoint to filter out the list of companies by setting the filter parameters.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/admin/v1/accounts/:accountId/companies
Authentication Context	
user context optional
Required OAuth Scopes	
account:read
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via either a two-legged or three-legged OAuth flow.
Region
string
Specifies the region where your request should be routed. If not set, the request is routed automatically, which may result in a slight increase in latency.
Possible values: US, EMEA. For a complete list of supported regions, see the Regions page.

User-Id
string
The ID of a user on whose behalf your request is acting.
Your app has access to all users specified by the administrator in the SaaS integrations UI. Provide this header value to identify the user to be affected by the request.

You can use either the user’s ACC ID (id), or their Autodesk ID (autodeskId).

Note that this header is required for Account Admin POST, PATCH, and DELETE endpoints if you want to use a 2-legged authentication context. This header is optional for Account Admin GET endpoints.

* Required
Request
URI Parameters
accountId
string: UUID
The ID of the ACC account that contains the project being created or the projects being retrieved. This corresponds to the hub ID in the Data Management API. To convert a hub ID into an account ID, remove the “b." prefix. For example, a hub ID of b.c8b0c73d-3ae9 translates to an account ID of c8b0c73d-3ae9.
Request
Query String Parameters
filter[name]
string
Filter companies by name. Can be a partial match based on the value of filterTextMatch provided.
Max length: 255

filter[trade]
string
Filter companies by trade. Can be a partial match based on the value of filterTextMatch provided.
Max length: 255

filter[erpId]
string
Filter companies by ERP Id. Can be a partial match based on the value of filterTextMatch provided.
Max length: 255

filter[taxId]
string
Filter companies by tax Id. Can be a partial match based on the value of filterTextMatch provided.
Max length: 255

filter[updatedAt]
string
Filter companies by updated at date range. The range must be specified with dates in an ISO-8601 format with time required. The start and end dates of the range should be separated by .. One of the dates in the range may be omitted. For example, to get everything on or before June 1, 2019 the range would be ..2019-06-01T23:59:59.999Z. To get everything after June 1, 2019 the range would be 2019-06-01T00:00:00.000Z...
Max length: 100

orFilters
array: string
List of filtered fields to apply an “or” operator. Valid list of fields are erpId, name, taxId, trade, updatedAt.
filterTextMatch
enum:string
Specifies how text-based filters should match values in supported fields.
This parameter can be used in any endpoint that supports text-based filtering (e.g., filter[name], filter[jobNumber], filter[companyName], etc.).

Possible values:

contains (default) – Matches if the field contains the specified text anywhere

startsWith – Matches if the field starts with the specified text

endsWith – Matches if the field ends with the specified text

equals – Matches only if the field exactly matches the specified text

Matching is case-insensitive.

Wildcards and regular expressions are not supported.

sort
array: string
The list of fields to sort by. When multiple fields are listed the later property is used to sort the resources where the previous fields have the same value. Each property can be followed by a direction modifier of either asc (ascending) or desc (descending). If no direction is specified then asc is assumed. Valid fields for sorting are name, trade, erpId, taxId, status, createdAt, updatedAt, projectSize and userSize. Default sort is name.
fields
array: string
List of fields to return in the response. Defaults to all fields. Valid list of fields are accountId, name, trade, addresses, websiteUrl, description, erpId, taxId, imageUrl, status, createdAt, updatedAt, projectSize, userSize and originalName.
limit
int
The maximum number of records to return in the response.
Default: 20

Minimum: 1

Maximum: 200 (If a larger value is provided, only 200 records are returned)

offset
int
The index of the first record to return.
Used for pagination in combination with the limit parameter.

Example: limit=20 and offset=40 returns records 41–60.

Response
HTTP Status Code Summary
200
OK
The list of requested companies.
400
Bad Request
The request could not be understood by the server due to malformed syntax.
401
Unauthorized
Request has not been applied because it lacks valid authentication credentials for the target resource.
403
Forbidden
The server understood the request but refuses to authorize it.
404
Not Found
The resource could not be found.
406
Not Acceptable
The server cannot produce a response matching the list of acceptable values defined in the request.
410
Access to the target resource is no longer available.
429
Too Many Requests
User has sent too many requests in a given amount of time.
500
Internal Server Error
An unexpected error occurred on the server.
503
Service Unavailable
Server is not ready to handle the request.
Response
Body Structure (200)
 Expand all
pagination
object
Contains pagination details for the records returned by the endpoint.
results
array: object
The requested page of companies.
Example
The list of requested companies.

Request
curl -v 'https://developer.api.autodesk.com/construction/admin/v1/accounts/d73fc742-4538-401c-8d0f-853b49b750b2/companies?filter[name]=Plumbing unlimited&filter[trade]=Plumbing&filter[erpId]=companyErpId&filter[taxId]=434920482-22&filter[updatedAt]=2019-06-01T00:00:00.000Z..&orFilters=name,trade&filterTextMatch=contains&sort=name&fields=name&limit=20' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 20,
    "offset": 10,
    "totalResults": 121,
    "nextUrl": "https://resource?limit=20&offset=30",
    "previousUrl": "https://resource?limit=20&offset=0"
  },
  "results": [
    {
      "id": "d1163421-e7eb-4862-ac15-b33777ba42de",
      "accountId": "d73fc742-4538-401c-8d0f-853b49b750b2",
      "name": "Plumbing Unlimited",
      "trade": "Plumbing",
      "addresses": [
        {
          "type": "Main",
          "addressLine1": "123 Main Street",
          "addressLine2": "Suite 2",
          "city": "San Francisco",
          "stateOrProvince": "California",
          "postalCode": "94001",
          "country": "US",
          "phone": "555-555-5555"
        }
      ],
      "websiteUrl": "https://www.plumbingunlimited.com",
      "description": "Plumbing subcontractor in southern California",
      "erpId": "12345678",
      "taxId": "87654321",
      "imageUrl": "https://images.acc.autodesk.com/plumbingunlimited.png",
      "status": "active",
      "createdAt": "2018-01-01T12:45:00.000Z",
      "updatedAt": "2018-01-01T12:45:00.000Z",
      "originalName": "",
      "projectSize": 3,
      "userSize": 12
    }
  ]
}

Documentation /BIM 360 API /API Reference
Account Users
GET	users
Query all the users in a specific BIM 360 account.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/hq/v1/accounts/:account_id/users
Method and URI (Legacy)	
GET	https://developer.api.autodesk.com/hq/v1/regions/eu/accounts/:account_id/users
Authentication Context	
app only
Required OAuth Scopes	
account:read
Data Formats	
JSON
Request
Headers
Authorization
yes
Must be Bearer <token>, where <token> is obtained via a two-legged OAuth flow.
Region
no
Specifies the region where the service is located. Possible values: US, EMEA. For the full list of supported regions, see the Regions page.
Request
URI Parameters
account_id
string: UUID
The account ID of the users. This corresponds to hub ID in the Data Management API. To convert a hub ID into an account ID you need to remove the “b." prefix. For example, a hub ID of b.c8b0c73d-3ae9 translates to an account ID of c8b0c73d-3ae9.
Request
Query String Parameters
limit
int
Response array’s size
Default value: 10
Max limit: 100
offset
int
Offset of response array
Default value: 0
sort
string
Comma-separated fields to sort by in ascending order

Prepending a field with - sorts in descending order
Invalid fields and whitespaces will be ignored
field
string
Comma-separated fields to include in response

id will always be returned
Invalid fields will be ignored
Response
HTTP Status Code Summary
200
OK
The request has succeeded.
400
Bad Request
The request could not be understood by the server due to malformed syntax.
403
Forbidden
Unauthorized
404
Not Found
The resource cannot be found.
409
Conflict
The request could not be completed due to a conflict with the current state of the resource.
422
Unprocessable Entity
The request was unable to be followed due to restrictions.
500
Internal Server Error
An unexpected error occurred on the server.
Response
Body Structure (200)
A successful response is an array of users, flat JSON objects with the following attributes:

id
string: UUID
BIM 360 user ID
account_id
string: UUID
Account ID
role
string
The role of the user in the account

Possible values:
account_admin: user has BIM 360 account administration access
account_user : normal project user
project_admin: user has Project administration privileges at a service level
status
string
Status of the user in the system

Possible values:
active: user is active and has logged into the system sucessfully
inactive: user is disabled
pending: user is invited and is yet to accept the invitation
not_invited: user is not invited
company_id
string: UUID
The user’s default company ID in BIM 360
company_name
string
The name of the user’s default company name in BIM 360
last_sign_in
datetime: ISO 8601
The time and date of the user’s most recent sign-in, in ISO 8601 format (YYYY-MM-DDThh:mm:ss.sssZ). Note that this field is not supported by ACC Unified products. The value is updated only when the user logs into one of the following services associated with the specified BIM 360 account: BIM 360 Account Admin, BIM 360 Project Admin, BIM 360 Document Management, BIM 360 Field (Classic), or BIM 360 Plan.
email
string
User’s email

Max length: 255
name
string
Default display name

Max length: 255
nickname
string
Nick name for user

Max length: 255
first_name
string
User’s first name

Max length: 255
last_name
string
User’s last name

Max length: 255
uid
string
User’s Autodesk ID
image_url
string
URL for user’s profile image

Max length: 255
address_line_1
string
User’s address line 1

Max length: 255
address_line_2
string
User’s address line 2

Max length: 255
city
string
City in which user is located

Max length: 255
state_or_province
enum: string
State or province in which user is located

Max length: 255

Note that the state_or_province value depends on the selected country value; see the valid values in the state_or_province list in the Parameters guide.
postal_code
string
Postal code for the user’s location

Max length: 255
country
enum: string
Country for this user

Refer to the country list in the Parameters guide.
phone
string
Contact phone number for the user

Max length: 255
company
string
Company information from the Autodesk user profile

Max length: 255

Note that this is different from company in BIM 360.
job_title
string
User’s job title

Max length: 255
industry
string
Industry information for user

Max length: 255
about_me
string
Short description about the user

Max length: 255
default_role
string
The user’s default role.

default_role_id
string
The ID of the default role.

created_at
datetime: ISO 8601
YYYY-MM-DDThh:mm:ss.sssZ format
updated_at
datetime: ISO 8601
YYYY-MM-DDThh:mm:ss.sssZ format
Example
Successful Listing of Users in an Account (200)

Request
curl -v 'https://developer.api.autodesk.com/hq/v1/accounts/efec10ec-a367-49fd-ab92-c70185fbb660/users' \
  -H 'Authorization: Bearer XZvCJNhdxESsBRIH28MfLf2hKL5O'
Response
[
  {
    "id": "a75e8769-621e-40b6-a524-0cffdd2f784e",
    "account_id": "9dbb160e-b904-458b-bc5c-ed184687592d",
    "status": "active",
    "role": "account_admin",
    "company_id": "28e4e819-8ab2-432c-b3fb-3a94b53a91cd",
    "company_name": "Autodesk",
    "last_sign_in": "2016-04-05T07:27:20.858Z",
    "email": "john.smith@mail.com",
    "name": "John Smith",
    "nickname": "Johnny",
    "first_name": "John",
    "last_name": "Smith",
    "uid": "L9EBJKCGCXBB",
    "image_url": "http://static-dc.autodesk.net/etc/designs/v201412151200/autodesk/adsk-design/images/autodesk_header_logo_140x23.png",
    "address_line_1": "The Fifth Avenue",
    "address_line_2": "#301",
    "city": "New York",
    "postal_code": "10011",
    "state_or_province": "New York",
    "country": "United States",
    "phone": "(634)329-2353",
    "company": "Autodesk",
    "job_title": "Software Developer",
    "industry": "IT",
    "about_me": "Nothing here",
    "default_role": "BIM Manager",
    "default_role_id": "4e7e02ae-2994-4210-9153-84bfb9a23a63",
    "created_at": "2015-06-26T14:47:39.458Z",
    "updated_at": "2016-04-07T07:15:29.261Z"
  }
]

Documentation /BIM 360 API /API Reference
Account Users
GET	users/:user_id
Query the details of a specific user.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/hq/v1/accounts/:account_id/users/:user_id
Method and URI (Legacy)	
GET	https://developer.api.autodesk.com/hq/v1/regions/eu/accounts/:account_id/users/:user_id
Authentication Context	
app only
Required OAuth Scopes	
account:read
Data Formats	
JSON
Request
Headers
Authorization
yes
Must be Bearer <token>, where <token> is obtained via a two-legged OAuth flow.
Region
no
Specifies the region where the service is located. Possible values: US, EMEA. For the full list of supported regions, see the Regions page.
Request
URI Parameters
account_id
string: UUID
The account ID of the user. This corresponds to hub ID in the Data Management API. To convert a hub ID into an account ID you need to remove the “b." prefix. For example, a hub ID of b.c8b0c73d-3ae9 translates to an account ID of c8b0c73d-3ae9.
user_id
string: UUID
User ID
Response
HTTP Status Code Summary
200
OK
The request has succeeded.
400
Bad Request
The request could not be understood by the server due to malformed syntax.
403
Forbidden
Unauthorized
404
Not Found
The resource cannot be found.
409
Conflict
The request could not be completed due to a conflict with the current state of the resource.
422
Unprocessable Entity
The request was unable to be followed due to restrictions.
500
Internal Server Error
An unexpected error occurred on the server.
Response
Body Structure (200)
A successful response is a user, a flat JSON object with the following attributes:

id
string: UUID
User ID
account_id
string: UUID
Account ID
role
string
The role of the user in the account

Possible values:
account_admin: user has BIM 360 account administration access
account_user : normal project user
project_admin: user has Project administration privileges at a service level
status
string
Status of the user in the system

Possible values:
active: user is active and has logged into the system sucessfully
inactive: user is disabled
pending: user is invited and is yet to accept the invitation
not_invited: user is not invited
company_id
string: UUID
The user’s default company ID in BIM 360
company_name
string
The name of the user’s default company name in BIM 360
last_sign_in
datetime: ISO 8601
The time and date of the user’s most recent sign-in, in ISO 8601 format (YYYY-MM-DDThh:mm:ss.sssZ). Note that this field is not supported by ACC Unified products. The value is updated only when the user logs into one of the following services associated with the specified BIM 360 account: BIM 360 Account Admin, BIM 360 Project Admin, BIM 360 Document Management, BIM 360 Field (Classic), or BIM 360 Plan.
email
string
User’s email

Max length: 255
name
string
Default display name

Max length: 255
nickname
string
Nick name for user

Max length: 255
first_name
string
User’s first name

Max length: 255
last_name
string
User’s last name

Max length: 255
uid
string
User’s Autodesk ID
image_url
string
URL for user’s profile image

Max length: 255
address_line_1
string
User’s address line 1

Max length: 255
address_line_2
string
User’s address line 2

Max length: 255
city
string
City in which user is located

Max length: 255
state_or_province
enum: string
State or province in which user is located

Max length: 255

Note that the state_or_province value depends on the selected country value; see the valid values in the state_or_province list in the Parameters guide.
postal_code
string
Postal code for the user’s location

Max length: 255
country
enum: string
Country for this user

Refer to the country list in the Parameters guide.
phone
string
Contact phone number for the user

Max length: 255
company
string
Company information from the Autodesk user profile

Max length: 255

Note that this is different from company in BIM 360.
job_title
string
User’s job title

Max length: 255
industry
string
Industry information for user

Max length: 255
about_me
string
Short description about the user

Max length: 255
default_role
string
The user’s default role.

default_role_id
string
The ID of the default role.

created_at
datetime: ISO 8601
YYYY-MM-DDThh:mm:ss.sssZ format
updated_at
datetime: ISO 8601
YYYY-MM-DDThh:mm:ss.sssZ format
Example
Successful Listing of a Requested User (200)

Request
curl -v 'https://developer.api.autodesk.com/hq/v1/accounts/9dbb160e-b904-458b-bc5c-ed184687592d/users/a75e8769-621e-40b6-a524-0cffdd2f784e' \
  -H 'Authorization: Bearer XZvCJNhdxESsBRIH28MfLf2hKL5O'
Response
{
  "id": "a75e8769-621e-40b6-a524-0cffdd2f784e",
  "account_id": "9dbb160e-b904-458b-bc5c-ed184687592d",
  "status": "active",
  "role": "account_admin",
  "company_id": "28e4e819-8ab2-432c-b3fb-3a94b53a91cd",
  "company_name": "Autodesk",
  "last_sign_in": "2016-04-05T07:27:20.858Z",
  "email": "john.smith@autodesk.com",
  "name": "John Smith",
  "nickname": "Johnny",
  "first_name": "John",
  "last_name": "Smith",
  "uid": "L9EBJKCGCXBB",
  "image_url": "http://static-dc.autodesk.net/etc/designs/v201412151200/autodesk/adsk-design/images/autodesk_header_logo_140x23.png",
  "address_line_1": "The Fifth Avenue",
  "address_line_2": "#301",
  "city": "New York",
  "postal_code": "10011",
  "state_or_province": "New York",
  "country": "United States",
  "phone": "(634)329-2353",
  "company": "Autodesk",
  "job_title": "Software Developer",
  "industry": "IT",
  "about_me": "Nothing here",
  "default_role": "BIM Manager",
  "default_role_id": "4e7e02ae-2994-4210-9153-84bfb9a23a63",
  "created_at": "2015-06-26T14:47:39.458Z",
  "updated_at": "2016-04-07T07:15:29.261Z"
}

Documentation /BIM 360 API /API Reference
Account Users
GET	users/search
Search users in the master member directory of a specific BIM 360 account by specified fields.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/hq/v1/accounts/:account_id/users/search
Method and URI (Legacy)	
GET	https://developer.api.autodesk.com/hq/v1/regions/eu/accounts/:account_id/users/search
Authentication Context	
app only
Required OAuth Scopes	
account:read
Data Formats	
JSON
Request
Headers
HTTP Headers	Type	Required	Description
Authorization	string	yes	Must be Bearer <token>, where <token> is obtained via a two-legged OAuth flow.
Region	string	no	Specifies the region where the service is located. Possible values: US, EMEA. For the full list of supported regions, see the Regions page.
Request
URI Parameters
account_id
string: UUID
The account ID of the users. This corresponds to hub ID in the Data Management API. To convert a hub ID into an account ID you need to remove the “b." prefix. For example, a hub ID of b.c8b0c73d-3ae9 translates to an account ID of c8b0c73d-3ae9.
Request
Query String Parameters
name
string
User name to match
Max length: 255
email
string
User email to match
Max length: 255
company_name
string
User company to match
Max length: 255
operator
enum: string
Boolean operator to use: OR (default) or AND
partial
bool
If true (default), perform a fuzzy match
limit
int
Response array’s size
Default value: 10
Max limit: 100
offset
int
Offset of response array
Default value: 0
sort
string
Comma-separated fields to sort by in ascending order

Prepending a field with - sorts in descending order.
Invalid fields and whitespaces will be ignored.
field
string
Comma-separated fields to include in response

id will always be returned.
Invalid fields will be ignored.
Response
HTTP Status Code Summary
200
OK
The request has succeeded.
400
Bad Request
The request could not be understood by the server due to malformed syntax.
403
Forbidden
Unauthorized
404
Not Found
The resource cannot be found.
409
Conflict
The request could not be completed due to a conflict with the current state of the resource.
422
Unprocessable Entity
The request was unable to be followed due to restrictions.
500
Internal Server Error
An unexpected error occurred on the server.
Response
Body Structure (200)
A successful response is an array of users, flat JSON objects with the following attributes:

id
string: UUID
User ID
account_id
string: UUID
Account ID
role
string
The role of the user in the account

Possible values:
account_admin: user has BIM 360 account administration access
account_user : normal project user
project_admin: user has Project administration privileges at a service level
status
string
Status of the user in the system

Possible values:
active: user is active and has logged into the system sucessfully
inactive: user is disabled
pending: user is invited and is yet to accept the invitation
not_invited: user is not invited
company_id
string: UUID
The user’s default company ID in BIM 360
company_name
string
The name of the user’s default company name in BIM 360
last_sign_in
datetime: ISO 8601
The time and date of the user’s most recent sign-in, in ISO 8601 format (YYYY-MM-DDThh:mm:ss.sssZ). Note that this field is not supported by ACC Unified products. The value is updated only when the user logs into one of the following services associated with the specified BIM 360 account: BIM 360 Account Admin, BIM 360 Project Admin, BIM 360 Document Management, BIM 360 Field (Classic), or BIM 360 Plan.
email
string
User’s email

Max length: 255
name
string
Default display name

Max length: 255
nickname
string
Nick name for user

Max length: 255
first_name
string
User’s first name

Max length: 255
last_name
string
User’s last name

Max length: 255
uid
string
User’s Autodesk ID
image_url
string
URL for user’s profile image

Max length: 255
address_line_1
string
User’s address line 1

Max length: 255
address_line_2
string
User’s address line 2

Max length: 255
city
string
City in which user is located

Max length: 255
state_or_province
enum: string
State or province in which user is located

Max length: 255

Note that the state_or_province value depends on the selected country value; see the valid values in the state_or_province list in the Parameters guide.
postal_code
string
Postal code for the user’s location

Max length: 255
country
enum: string
Country for this user

Refer to the country list in the Parameters guide.
phone
string
Contact phone number for the user

Max length: 255
company
string
Company information from the Autodesk user profile

Max length: 255

Note that this is different from company in BIM 360.
job_title
string
User’s job title

Max length: 255
industry
string
Industry information for user

Max length: 255
about_me
string
Short description about the user

Max length: 25
default_role
string
The user’s default role.

default_role_id
string
The ID of the default role.

created_at
datetime: ISO 8601
YYYY-MM-DDThh:mm:ss.sssZ format
updated_at
datetime: ISO 8601
YYYY-MM-DDThh:mm:ss.sssZ format
Example
Successful Search for Users by Email Address (200)

Request
curl -v 'https://developer.api.autodesk.com/hq/v1/accounts/efec10ec-a367-49fd-ab92-c70185fbb660/users/search?email=john.smith2%40gamil.com&limit=1' \
  -H 'Authorization: Bearer XZvCJNhdxESsBRIH28MfLf2hKL5O'
Response
[
  {
    "id": "579d4408-39a4-4b3a-9474-6e781e68ab94",
    "account_id": "9dbb160e-b904-458b-bc5c-ed184687592d",
    "status": "pending",
    "role": "account_admin",
    "company_id": "14e95a5e-02eb-49aa-a39a-447d90544873",
    "company_name": "Autodesk",
    "email": "john.smith@mail.com",
    "name": "John Smith",
    "nickname": "Johnny",
    "first_name": "John",
    "last_name": "Smith",
    "uid": "L9EBJKCGCXBB",
    "image_url": "http://static-dc.autodesk.net/etc/designs/v201412151200/autodesk/adsk-design/images/autodesk_header_logo_140x23.png",
    "last_sign_in": null,
    "address_line_1": "The Fifth Avenue",
    "address_line_2": "#301",
    "city": "New York",
    "postal_code": "10011",
    "state_or_province": "New York",
    "country": "United States",
    "phone": "(634)329-2353",
    "company": "Autodesk",
    "job_title": "Software Developer",
    "industry": "IT",
    "about_me": "Nothing here",
    "default_role": "BIM Manager",
    "default_role_id": "4e7e02ae-2994-4210-9153-84bfb9a23a63",
    "created_at": "2015-04-29T06:59:05.582Z",
    "updated_at": "2015-04-29T06:59:05.582Z"
  }
]

Documentation /BIM 360 API /API Reference
projects/:project_id/users
GET	projects/{projectId}/users
Retrieves information about a filtered subset of users in the specified project.

There are two primary reasons to do this:

To verify that all users assigned to the project have been activated as members of the project.
To check other information about users, such as their project user ID, roles, and products.
Note that if you want to retrieve information about users associated with a particular Autodesk account, call the GET users endpoint.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/admin/v1/projects/:projectId/users
Authentication Context	
user context optional
Required OAuth Scopes	
account:read
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via either a two-legged or three-legged OAuth flow.
Region
string
Specifies the region where your request should be routed. If not set, the request is routed automatically, which may result in a slight increase in latency.
Possible values: US, EMEA. For a complete list of supported regions, see the Regions page.

User-Id
string
The ID of a user on whose behalf your request is acting.
Your app has access to all users specified by the administrator in the SaaS integrations UI. Provide this header value to identify the user to be affected by the request.

You can use either the user’s ACC ID (id), or their Autodesk ID (autodeskId).

Note that this header is required for Account Admin POST, PATCH, and DELETE endpoints if you want to use a 2-legged authentication context. This header is optional for Account Admin GET endpoints.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project. This corresponds to project ID in the Data Management API. To convert a project ID in the Data Management API into a project ID in the ACC API you need to remove the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.
Request
Query String Parameters
filter[products]
array: string
A comma-separated list of the products that the returned users must have access to in the specified project. Only users that have access to one or more of the specified products are returned.
Note that every product in the same account as the project is activated for the project, and a separate subset of these products is active for each user. This endpoint can retrieve users from ACC or BIM 360 projects.

Some products are exclusive to ACC or to BIM 360, others are available on both platforms. Specify only the products on the appropriate platform for the users you want to retrieve.

Possible ACC values: accountAdministration, autoSpecs, build, buildingConnected, capitalPlanning, cloudWorksharing, cost, designCollaboration, docs, financials, insight, modelCoordination, projectAdministration, takeoff, and workshopxr.

Possible BIM 360 values: accountAdministration, assets, cloudWorksharing, costManagement, designCollaboration, documentManagement, field, fieldManagement, glue, insight, modelCoordination, plan, projectAdministration, projectHome, projectManagement, and quantification.

filter[name]
string
A user name or name pattern that the returned users must have. Can be a partial match based on the value of filterTextMatch that you provide.
For example:

filter[name]=Sample filterTextMatch=startsWith

Max length: 255

filter[email]
string
A user email address or address pattern that the returned users must have. This can be a partial match based on the value of filterTextMatch that you provide.
For example:

filter[email]=sample filterTextMatch=startsWith

Max length: 255

filter[accessLevels]
array: string
A list of user access levels that the returned users must have.
Possible values: accouantAdmin, projectAdmin, executive.

Max length: 255

filter[companyId]
string
The ID of a company that the returned users must represent.
Max length: 255

filter[companyName]
string
The name of a company that returned users must be associated with. Can be a partial match based on the value of filterTextMatch that you provide.
For example: filter[companyName]=Sample filterTextMatch=startsWith

Max length: 255

filter[autodeskId]
array: string
A list of the Autodesk IDs of users to retrieve.
filter[id]
array: string: uuid
A list of the ACC IDs of users to retrieve.
filter[roleId]
string: UUID
The ID of a user role that the returned users must have.
To obtain a role ID for this filter, you can inspect the roleId field in previous responses to this endpoint or to the GET projects/:projectId/users/:userId endpoint.

Max length: 255

filter[roleIds]
array: string: uuid
A list of the IDs of user roles that the returned users must have.
To obtain a role ID for this filter, you can inspect the roleId field in previous responses to this endpoint or to the GET projects/:projectId/users/:userId endpoint.

filter[status]
array: string
A list of statuses that the returned project users must be in. The default values are active and pending.
Possible values: active, pending, and deleted.

sort
array: string
A list of fields to sort the returned users by. Multiple sort fields are applied in sequence order - each sort field produces groupings of projects with the same values of that field; the next sort field applies within the groupings produced by the previous sort field.
Each property can be followed by a direction modifier of either asc (ascending) or desc (descending). The default is asc.

Possible values: name, email, firstName, lastName, addressLine1, addressLine2, city, companyName, stateOrProvince, status, phone, postalCode, country and addedOn. Default value: name.

fields
array: string
A list of the project fields to include in the response. Default value: all fields.
Possible values: name, email, firstName, lastName, autodeskId, analyticsId, addressLine1, addressLine2, city, stateOrProvince, postalCode, country, imageUrl, phone, jobTitle, industry, aboutMe, companyId, accessLevels, roleIds, roles, status, addedOn and products.

orFilters
array: string
A list of user fields to combine with the SQL OR operator for filtering the returned project users. The OR is automatically incorporated between the fields; any one of them can produce a valid match.
Possible values: id, name, email, autodeskId, status and accessLevels.

filterTextMatch
enum:string
Specifies how text-based filters should match values in supported fields.
This parameter can be used in any endpoint that supports text-based filtering (e.g., filter[name], filter[jobNumber], filter[companyName], etc.).

Possible values:

contains (default) – Matches if the field contains the specified text anywhere

startsWith – Matches if the field starts with the specified text

endsWith – Matches if the field ends with the specified text

equals – Matches only if the field exactly matches the specified text

Matching is case-insensitive.

Wildcards and regular expressions are not supported.

limit
int
The maximum number of records to return in the response.
Default: 20

Minimum: 1

Maximum: 200 (If a larger value is provided, only 200 records are returned)

offset
int
The index of the first record to return.
Used for pagination in combination with the limit parameter.

Example: limit=20 and offset=40 returns records 41–60.

Response
HTTP Status Code Summary
200
OK
A list of requested project users.
400
Bad Request
The request could not be understood by the server due to malformed syntax.
401
Unauthorized
Request has not been applied because it lacks valid authentication credentials for the target resource.
403
Forbidden
The server understood the request but refuses to authorize it.
404
Not Found
The resource could not be found.
406
Not Acceptable
The server cannot produce a response matching the list of acceptable values defined in the request.
409
Conflict
The request could not be completed due to a conflict with the current state of the resource.
410
Access to the target resource is no longer available.
429
Too Many Requests
User has sent too many requests in a given amount of time.
500
Internal Server Error
An unexpected error occurred on the server.
503
Service Unavailable
Server is not ready to handle the request.
Response
Body Structure (200)
 Expand all
pagination
object
Contains pagination details for the records returned by the endpoint.
results
array: object
The requested page of project users.
Example
A list of requested project users.

Request
curl -v 'https://developer.api.autodesk.com/construction/admin/v1/projects/367d5cc2-9008-462c-96e5-c9491db85d93/users?filter[products]=build,cost&filter[name]=Sample User&filter[email]=sampleUser1@autodesk.com&filter[accessLevels]=accountAdmin,executive&filter[companyId]=d1163421-e7eb-4862-ac15-b33777ba42de&filter[companyName]=Sample Company&filter[autodeskId]=User123,User124&filter[id]=39712a51-bd64-446a-9c72-48c4e43d0a0d,d1163421-e7eb-4862-ac15-b33777ba42de&filter[roleId]=cda845af-05f0-4c46-9108-71b993946c35&filter[roleIds]=cda845af-05f0-4c46-9108-71b993946c35,b8e84a73-7506-4d3f-b221-93691df2a359&filter[status]=active,pending&sort=name&fields=name,email&orFilters=id,name&filterTextMatch=contains&limit=20' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 20,
    "offset": 10,
    "totalResults": 121,
    "nextUrl": "https://resource?limit=20&offset=30",
    "previousUrl": "https://resource?limit=20&offset=0"
  },
  "results": [
    {
      "email": "sampleUser1@autodesk.com",
      "id": "39712a51-bd64-446a-9c72-48c4e43d0a0d",
      "name": "Bob Smith",
      "firstName": "Bob",
      "lastName": "Smith",
      "autodeskId": "USER123A",
      "analyticsId": "SOMEID123",
      "addressLine1": "123 Main Street",
      "addressLine2": "Suite 2",
      "city": "San Francisco",
      "stateOrProvince": "California",
      "postalCode": "94001",
      "country": "United States",
      "imageUrl": "https://s3.amazonaws.com:443/com.autodesk.storage.public.dev/oxygen/USER123A/profilepictures/x20.jpg",
      "phone": {
        "number": "123-345-1234",
        "phoneType": "mobile",
        "extension": "10"
      },
      "jobTitle": "Owner",
      "industry": "Architecture & Construction Service Providers",
      "aboutMe": "Bob has been in construction for 25 years.",
      "accessLevels": {
        "accountAdmin": true,
        "projectAdmin": true,
        "executive": true
      },
      "addedOn": "2018-01-01T12:45:00.000Z",
      "updatedAt": "2018-01-01T12:45:00.000Z",
      "companyId": "c32ffb13-83f8-43fb-bddf-3e5c0c2dda24",
      "companyName": "Sample Company",
      "roleIds": [
        "cda845af-05f0-4c46-9108-71b993946c35",
        "b8e84a73-7506-4d3f-b221-93691df2a359"
      ],
      "roles": [
        {
          "id": "cda845af-05f0-4c46-9108-71b993946c35",
          "name": "Architect"
        },
        {
          "id": "b8e84a73-7506-4d3f-b221-93691df2a359",
          "name": "Engineer"
        }
      ],
      "status": "active",
      "products": [
        {
          "key": "projectAdministration",
          "access": "administrator"
        },
        {
          "key": "designCollaboration",
          "access": "administrator"
        },
        {
          "key": "build",
          "access": "administrator"
        },
        {
          "key": "cost",
          "access": "administrator"
        },
        {
          "key": "modelCoordination",
          "access": "administrator"
        },
        {
          "key": "docs",
          "access": "administrator"
        },
        {
          "key": "insight",
          "access": "administrator"
        },
        {
          "key": "takeoff",
          "access": "administrator"
        }
      ]
    }
  ]
}

Documentation /BIM 360 API /API Reference
projects/:project_id/users/:user_id
GET	projects/{projectId}/users/{userId}
Retrieves detailed information about the specified user in a project.

There are two primary reasons to do this:

To verify that the user has been activated as a member of the project.
To check other information about the user, such as their project user ID, roles, and products.
Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/admin/v1/projects/:projectId/users/:userId
Authentication Context	
user context optional
Required OAuth Scopes	
account:read
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via either a two-legged or three-legged OAuth flow.
Region
string
Specifies the region where your request should be routed. If not set, the request is routed automatically, which may result in a slight increase in latency.
Possible values: US, EMEA. For a complete list of supported regions, see the Regions page.

User-Id
string
The ID of a user on whose behalf your request is acting.
Your app has access to all users specified by the administrator in the SaaS integrations UI. Provide this header value to identify the user to be affected by the request.

You can use either the user’s ACC ID (id), or their Autodesk ID (autodeskId).

Note that this header is required for Account Admin POST, PATCH, and DELETE endpoints if you want to use a 2-legged authentication context. This header is optional for Account Admin GET endpoints.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project. This corresponds to project ID in the Data Management API. To convert a project ID in the Data Management API into a project ID in the ACC API you need to remove the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.
userId
string
The ID of the user. To find the ID call GET users. You can use either the ACC ID (id) or the Autodesk ID (autodeskId).
Request
Query String Parameters
fields
array: string
A list of the project user fields to include in the response. Separate multiple values with commas.
Possible values: name, email, firstName, lastName, autodeskId, addressLine1, addressLine2, city, stateOrProvince, postalCode, country, imageUrl, lastSignIn, phone, jobTitle, industry, aboutMe, createdAt, updatedAt, accessLevels, companyId, roleIds, roles, status, addedOn, and products.

Response
HTTP Status Code Summary
200
OK
Information about the requested project user.
400
Bad Request
The request could not be understood by the server due to malformed syntax.
401
Unauthorized
Request has not been applied because it lacks valid authentication credentials for the target resource.
403
Forbidden
The server understood the request but refuses to authorize it.
404
Not Found
The resource could not be found.
406
Not Acceptable
The server cannot produce a response matching the list of acceptable values defined in the request.
409
Conflict
The request could not be completed due to a conflict with the current state of the resource.
410
Access to the target resource is no longer available.
429
Too Many Requests
User has sent too many requests in a given amount of time.
500
Internal Server Error
An unexpected error occurred on the server.
503
Service Unavailable
Server is not ready to handle the request.
Response
Body Structure (200)
 Expand all
email
string
The email of the user.
Max length: 255

id
string: UUID
The ACC ID of the user.
name
string
The full name of the user.
Max length: 255

firstName
string
The user’s first name. This data syncs from the user’s Autodesk profile.
Max length: 255

lastName
string
The user’s last name. This data syncs from the user’s Autodesk profile.
Max length: 255

autodeskId
string
The ID of the user’s Autodesk profile.
Max length: 255

analyticsId
string
Not relevant
addressLine1
string
The user’s address line 1. This data syncs from the user’s Autodesk profile.
Max length: 255

addressLine2
string
The user’s address line 2. This data syncs from the user’s Autodesk profile.
Max length: 255

city
string
The User’s city. This data syncs from the user’s Autodesk profile.
Max length: 255

stateOrProvince
string
The state or province of the user. The accepted values here change depending on which country is provided. This data syncs from the user’s Autodesk profile.
Max length: 255

postalCode
string
The zip or postal code of the user. This data syncs from the user’s Autodesk profile.
Max length: 255

country
string
The user’s country. This data syncs from the user’s Autodesk profile.
Max length: 255

imageUrl
string
The URL of the user’s avatar. This data syncs from the user’s Autodesk profile.
Max length: 255

phone
object
The user’s phone number. This data syncs from the user’s Autodesk profile.
jobTitle
string
The user’s job title. This data syncs from the user’s Autodesk profile.
Max length: 255

industry
string
The industry the user works in. This data syncs from the user’s Autodesk profile.
Max length: 255

aboutMe
string
A short bio about the user. This data syncs from the user’s Autodesk profile.
Max length: 255

accessLevels
object
Flags that identify a returned user’s access levels in the account or project.
addedOn
datetime: ISO 8601
The timestamp when the user was first given access to any product on the project.
updatedAt
datetime: ISO 8601
The timestamp when the project user was last updated, in ISO 8601 format.
companyId
null,string
The ID of the company that the user is representing in the project. To obtain a list of all company IDs associated with a project, call GET projects/:projectId/companies.
companyName
null,string
The name of the company to which the user belongs.
Max length: 255

roleIds
array: string
A list of IDs of the roles that the user belongs to in the project.
roles
array: object
A list of the role IDs and names that are associated with the user in the project.
status
string
The status of the user in the project. A pending user could be waiting for their products to activate, or the user hasn’t accepted an email to create an account with Autodesk.
Possible values:

active: The user has been added to the project.
pending: The user is in the process of being added to the project.
disabled: The user has been temporarily suspended from the project.
deleted: The user has been removed from the project.
products
array: object
Information about the products activated in the specified project for this user.
Example
Information about the requested project user.

Request
curl -v 'https://developer.api.autodesk.com/construction/admin/v1/projects/367d5cc2-9008-462c-96e5-c9491db85d93/users/6cc15635-2fbd-4f73-afbe-abd833408a1d?fields=name' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "email": "sampleUser1@autodesk.com",
  "id": "39712a51-bd64-446a-9c72-48c4e43d0a0d",
  "name": "Bob Smith",
  "firstName": "Bob",
  "lastName": "Smith",
  "autodeskId": "USER123A",
  "analyticsId": "SOMEID123",
  "addressLine1": "123 Main Street",
  "addressLine2": "Suite 2",
  "city": "San Francisco",
  "stateOrProvince": "California",
  "postalCode": "94001",
  "country": "United States",
  "imageUrl": "https://s3.amazonaws.com:443/com.autodesk.storage.public.dev/oxygen/USER123A/profilepictures/x20.jpg",
  "phone": {
    "number": "123-345-1234",
    "phoneType": "mobile",
    "extension": "10"
  },
  "jobTitle": "Owner",
  "industry": "Architecture & Construction Service Providers",
  "aboutMe": "Bob has been in construction for 25 years.",
  "accessLevels": {
    "accountAdmin": true,
    "projectAdmin": true,
    "executive": true
  },
  "addedOn": "2018-01-01T12:45:00.000Z",
  "updatedAt": "2018-01-01T12:45:00.000Z",
  "companyId": "c32ffb13-83f8-43fb-bddf-3e5c0c2dda24",
  "companyName": "Sample Company",
  "roleIds": [
    "cda845af-05f0-4c46-9108-71b993946c35",
    "b8e84a73-7506-4d3f-b221-93691df2a359"
  ],
  "roles": [
    {
      "id": "cda845af-05f0-4c46-9108-71b993946c35",
      "name": "Architect"
    },
    {
      "id": "b8e84a73-7506-4d3f-b221-93691df2a359",
      "name": "Engineer"
    }
  ],
  "status": "active",
  "products": [
    {
      "key": "projectAdministration",
      "access": "administrator"
    },
    {
      "key": "designCollaboration",
      "access": "administrator"
    },
    {
      "key": "build",
      "access": "administrator"
    },
    {
      "key": "cost",
      "access": "administrator"
    },
    {
      "key": "modelCoordination",
      "access": "administrator"
    },
    {
      "key": "docs",
      "access": "administrator"
    },
    {
      "key": "insight",
      "access": "administrator"
    },
    {
      "key": "takeoff",
      "access": "administrator"
    }
  ]
}

Documentation /BIM 360 API /API Reference
Project Roles
GET	projects/:project_id/industry_roles
Retrieves the industry roles for the project. For example, contractor and architect.

Note that this endpoint is version 2 (v2) - you need to use ../v2/.. in the URI.

Note that this endpoint is ONLY compatible with BIM 360 projects. It is not compatible with Autodesk Construction Cloud (ACC) projects. For more information about compatibility between between BIM 360 and ACC, see the Compatibility section.

Resource Information
Method and URI (US)	
GET	https://developer.api.autodesk.com/hq/v2/accounts/:account_id/projects/:project_id/industry_roles
Method and URI (Legacy)	
GET	https://developer.api.autodesk.com/hq/v2/regions/eu/accounts/:account_id/projects/:project_id/industry_roles
Authentication Context	
user context optional
Required OAuth Scopes	
account:read
Data Formats	
JSON
Request
Headers
Authorization
yes
Must be Bearer <token>, where <token> is obtained via either a two-legged or three-legged OAuth flow.
Content-Type
yes
Must be application/json
Region
no
Specifies the region where the service is located. Possible values: US, EMEA. For the full list of supported regions, see the Regions page.
Request
URI Parameters
account_id
string
The account ID. This corresponds to hub ID in the Data Management API. To convert a hub ID into an account ID you need to remove the “b." prefix. For example, a hub ID of b.c8b0c73d-3ae9 translates to an account ID of c8b0c73d-3ae9.
project_id
string
The project ID. This corresponds to project ID in the Data Management API. To convert a project ID in the Data Management API into a project ID in the BIM 360 API you need to remove the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.
Response
HTTP Status Code Summary
200
OK
The request has succeeded.
400
Bad Request
The request could not be understood by the server due to malformed syntax.
403
Forbidden
Unauthorized
404
Not Found
The resource cannot be found.
409
Conflict
The request could not be completed due to a conflict with the current state of the resource.
422
Unprocessable Entity
The request was unable to be followed due to restrictions.
500
Internal Server Error
An unexpected error occurred on the server.
Response
Body Structure (200)
A successful response returns an array of JSON objects with the following attributes:

 Expand all
id
string
The industry role ID.
name
string
The name of the industry role.
project_id
string
The project ID.
services
object

member_group_id
string
The Autodesk ID of the industry role; used to identify which role is assigned to an RFI or Issue.
Example
Successful Retrieval of Industry Roles (200)

Request
curl -v 'https://developer.api.autodesk.com/hq/v2/accounts/9dbb160e-b904-458b-bc5c-ed184687592d/projects/2c9958f4-722e-47cf-bd6e-6d0a7b20d50e/industry_roles' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer XZvCJNhdxESsBRIH28MfLf2hKL5O'
Response
[
  {
    "id": "5502171c-9e38-427e-a49a-40fa6821dec4",
    "project_id": "2c9958f4-722e-47cf-bd6e-6d0a7b20d50e",
    "name": "Contractor",
    "services": {
      "project_administration": {
      "access_level": "admin"
    },
      "document_management": {
      "access_level": "admin"
      }
    },
    "member_group_id": "768654"
  }
]

Documentation /BIM 360 API /API Reference
Jobs
GET	jobs/:job_id
Returns the job status. Used to track asynchronous operations when an instant response is not possible. This endpoint is currently used only with the BIM 360 Project creation process when project settings from an existing BIM 360 Field project are used as a template for a new BIM 360 Field project.

Note that this endpoint is ONLY compatible with BIM 360 projects. It is not compatible with Autodesk Construction Cloud (ACC) projects. For more information about compatibility between between BIM 360 and ACC, see the Compatibility section.

Resource Information
Method and URI（US)	
GET	https://developer.api.autodesk.com/hq/v1/accounts/:account_id/jobs/:job_id
Method and URI（Legacy)	
GET	https://developer.api.autodesk.com/hq/v1/regions/eu/accounts/:account_id/jobs/:job_id
Authentication Context	
app only
Required OAuth Scopes	
account:read
Data Format	
JSON
Request
Headers
Authorization
yes
Must be Bearer <token>, where <token> is obtained via a two-legged OAuth flow.
Region
no
Specifies the region where the service is located. Possible values: US, EMEA. For the full list of supported regions, see the Regions page.
Request
URI Parameters
account_id
string: UUID
The account ID of the job. This corresponds to hub ID in the Data Management API. To convert a hub ID into an account ID you need to remove the “b." prefix. For example, a hub ID of b.c8b0c73d-3ae9 translates to an account ID of c8b0c73d-3ae9.
job_id
string: UUID
Job ID

For jobs that create new BIM 360 Field projects based on templates, this value can be found in the copy_project_job_id attribute in the JSON response of the POST projects endpoint.
Response
HTTP Status Code Summary
200
OK
The request has succeeded.
400
Bad Request
The request could not be understood by the server due to malformed syntax.
403
Forbidden
Unauthorized
404
Not Found
The resource cannot be found.
409
Conflict
The request could not be completed due to a conflict with the current state of the resource.
422
Unprocessable Entity
The request was unable to be followed due to restrictions.
500
Internal Server Error
An unexpected error occurred on the server.
Response
Body Structure (200)
A successful response returns the requested job object with the following attributes:

 Expand all
id
string: UUID
Job ID
account_id
string: UUID
Account ID
name
string
The name of the job; currently always copy_project_job
(copying project settings from an existing BIM 360 Field
project to a new project)
status
enum:string
Job status

Possible values:
completed: the job has been completed
in progress: the job is in progress
details
object
Additional information about the job
Example
Successful Retrieval of Job Status (200)

Request
curl -v 'https://developer.api.autodesk.com/hq/v1/accounts/e3d5ef8d-5c37-4b9d-925d-1e6d24753ace/jobs/aca11a7abd1747cdab996548d0e6fe25'
  -H "Authorization: Bearer 9ezBnx9Rd5D1xG4KMt6b72T4w0MG"
Response
{
  "id": "aca11a7abd1747cdab996548d0e6fe25",
  "account_id": "e3d5ef8d-5c37-4b9d-925d-1e6d24753ace",
  "name": "copy_project_job",
  "status": "completed",
  "details": {
    "project_id": "80793a28-f9b1-4888-9533-5f00cddcd6fb",
    "template_project_id": "fda4ab9e-ab82-4ba9-8d6c-ae7dbd7cee31",
    "include_companies": "true",
    "include_locations": "false"
  }
}

Asset api 如下：
Documentation /BIM 360 API /API Reference
Assets
POST	assets:batch-get V2
Returns a specified set of assets.

This endpoint accepts an object with an array of one or more asset IDs and returns an array of assets corresponding to each of those IDs. Invalid asset IDs will simply be omitted from the response and the client is responsible for identifying missing results.

To understand the basics of assets and the Assets settings that define them, see the Assets Field Guide.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/bim360/assets/v2/projects/{projectId}/assets:batch-get
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
* Required
Request
URI Parameters
projectId
string
The BIM 360 project ID. Must be a UUID or a project ID of the form “b.{UUID}”.
Request
Query String Parameters
includeCustomAttributes
boolean
Specifies whether or not returned assets include custom attributes or not. If true, they’re included. If false, they’re not. Default is false.
includeDeleted
boolean
Whether or not soft-deleted object should be included in the response. If true, soft-deleted objects are returned. If false, they are not. The default is false.
Request
Body Structure
Request payload for fetching a batch of assets by IDs

ids
array: string
An array of unique IDs of assets to fetch.
Response
HTTP Status Code Summary
200
OK
Successfully returned a batch of assets.
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
The request was not accepted because the rate limit was exceeded due to too many requests being made.
500
Internal Server Error
An unexpected error occurred on the server
Response
Body Structure (200)
 Expand all
results
array: object
Returned assets
Example
Successfully returned a batch of assets.

Request
curl -v 'https://developer.api.autodesk.com/bim360/assets/v2/projects/:projectId/assets:batch-get?includeCustomAttributes=true&includeDeleted=true' \
  -X 'POST' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a' \
  -H 'Content-Type: application/json' \
  -d '{
        "ids": [
          "6cdd4356-a719-4964-9fd7-0c505e731ac7"
        ]
      }'
Show Less
Response
{
  "results": [
    {
      "id": "b302d910-b5e3-46ba-81d8-6b6d30406e14",
      "createdAt": "2020-05-01T06:00:00.000Z",
      "createdBy": "LA7ZL85MU7ML",
      "updatedAt": "2020-05-01T06:00:00.000Z",
      "updatedBy": "LA7ZL85MU7ML",
      "deletedAt": "2020-05-01T06:00:00.000Z",
      "deletedBy": "LA7ZL85MU7ML",
      "isActive": true,
      "version": 1,
      "clientAssetId": "MVS-3D2",
      "categoryId": "42",
      "statusId": "84eb6a10-dde3-475f-aaf4-b5df3aebbd0b",
      "description": "AC unit for basement",
      "locationId": "826e102a-36de-41e7-8c58-1b1696ccbba8",
      "barcode": "F0086728",
      "customAttributes": {
        "ca1": true,
        "ca2": 6.5,
        "ca4": "688f8cfb-0eb4-4289-9d18-96007875dec3",
        "ca5": [
          "9e653094-8d9e-4050-a97a-24d9c5a3786f",
          "e88357bc-e3dd-4cd8-a9e2-6d659b301e7f"
        ],
        "ca6": "text value"
      },
      "companyId": "07b5f07d-c54a-4236-a086-f84192fabdb3"
    }
  ]
}

Documentation /BIM 360 API /API Reference
Assets
GET	assets V2
Searches for and returns all specified assets within a project visible to the authenticated user.

This endpoint accepts a set of optional asset property filters, then uses supplied filters to search for and return assets within a project that satisfy those filters. If no filters are set, this endpoint returns all assets within a project.

The endpoint paginates returned assets. If you don’t specify pagination fields, your query will execute using the default page size. If you want to specify a different a page size, use the limit query parameter.

A paginated response to a query includes pagination information that may contain a nextUrl field. Use the URL it provides to request the next page in the query, then use the nextUrl field in that subsequent response to request the next page in the query, and so on until the response contains no nextUrl value, which means the query is finished returning objects. Note that you should not edit the nextUrl value to alter filter and sort values.

If you want to create your own sequence of requests to retrieve all of a query’s pages without using nextUrl, you can use the cursorState value returned by each request to specify where the next request should start the next page.

To understand the basics of assets and the Assets settings that define them, see the Assets Field Guide.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/assets/v2/projects/{projectId}/assets
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
The BIM 360 project ID. Must be a UUID or a project ID of the form “b.{UUID}”.
Request
Query String Parameters
cursorState
string
An opaque cursor token that identifies where the next page of paginated results should start. It’s returned in each paginated response so that it can be supplied in the next request to continue paginated results. If a paginated response contains no cursorState value, then there are no further pages to return.
Omit this field to initiate a paginated request or to restart pagination.

limit
int
The maximum number of objects that can be returned in a page. A request might return fewer objects than the limit if the Assets service runs out of specified objects to return - at the end of a set of paged results, for example. The maximum limit is 200; the default limit is 25.
filter[categoryId]
array
An exploded array of category IDs to which all returned objects must belong. For example, ?filter[categoryId]=123&filter[categoryId]=456.
filter[statusLabel]
array
An exploded array of status labels. Each returned object must have one of the statuses bearing any of these labels, case-insensitive. For example, ?filter[statusLabel]=ordered&filter[statusLabel]=delivered.
filter[statusId]
array
An exploded array of status IDs. Each returned object must have one of the statuses specified by the IDs. For example, ?filter[statusId]=84eb6a10-dde3-475f-aaf4-b5df3aebbd0b&filter[statusId]=5ba5c1af-fcd6-4506-b5e4-f20f5321dd69.
filter[locationId]
array
An exploded array of location IDs. Each returned object must be associated with one of the locations specified by the IDs. To specify sub-locations of a location, provide a single location ID here and then set the includeSubLocations field in the request to true. For example, ?filter[locationId]=826e102a-36de-41e7-8c58-1b1696ccbba8&filter[locationId]=cee49807-fcc4-43ae-80a2-8ca819dfa70d.
filter[customAttributes]
object
A custom attribute and value that each returned object must have. This filter is keyed by the custom attribute’s name field and set equal to the desired value. As an example, ?filter[customAttributes][ca1]=true. Use this field multiple times to specify more than one custom attribute filter.
The value supplied for a custom attribute filter must match the type specified by the attribute. Values can be:

A single value, or exploded array of values, of string, boolean, or number (for text, numeric, date, boolean, select, or multi_select types). Note that a string value for a text data type will perform a case-insensitive, substring match.
A range of values (inclusive) in the form: startValue..endValue (for numeric or date Types).
Partial ranges (inclusive): ...endValue or startValue.. (for numeric or date Types).
Select and Multi-Select filters should use Custom Attribute Value IDs as values.

Note that explicit value filters and range filters for a given attribute cannot be used in conjunction.

Examples (without URL escaping)

Example 1) Filter a boolean custom attribute:
?filter[customAttributes][ca1]=true

Example 2) Filter a numeric range custom attribute:
?filter[customAttributes][ca2]=1..5

Example 3) Filter a date custom attribute to on or before a given date:
?filter[customAttributes][ca3]=..2020-11-01

Example 4) Filter a select custom attribute:
?filter[customAttributes][ca4]=b959daad-4d00-4209-9acc-e900ac5832cf

Example 5) Filter a multi_select custom attribute to multiple values:
?filter[customAttributes][ca5]=63801bb7-db1f-49bf-9000-a392a5879f22&filter[customAttributes][ca5]=757d0934-a4a0-4af8-821d-64d611e84a56

Example 6) Filter a text custom attribute to a given input:
?filter[customAttributes][ca6]=Some text input

filter[searchText]
string
A string that must be contained within any of a returned object’s searchable text fields, including text custom attributes. searchText is case-insensitive, and will match substrings as well as full strings.
filter[updatedAt]
string
A string that specifies a date and time or a date and time range at which all returned objects mast have been updated. A single date and time takes this format: YYYY-MM-DDThh:mm:ss.SSSZ, A date and time range takes this format: YYYY-MM-DDThh:mm:ss.SSSZ..YYYY-MM-DDThh:mm:ss.SSSZ. Range queries can be closed or open in either direction: YYYY-MM-DDThh:mm:ss.SSSZ.. or ..YYYY-MM-DDThh:mm:ss.SSSZ.
sort
string
A string that specifies how to sort returned objects. The string provides a valid API field name with an optional direction, either asc (ascending) or desc (descending). In the case of custom attributes, use dot notation to specify the attribute by name—for example, customAttributes.ca3 desc. The string may contain multiple comma-separated expressions for secondary sorts. The default sort order is asc if not provided.
includeCustomAttributes
boolean
Specifies whether or not returned assets include custom attributes or not. If true, they’re included. If false, they’re not. Default is false.
includeDeleted
boolean
Whether or not soft-deleted object should be included in the response. If true, soft-deleted objects are returned. If false, they are not. The default is false.
includeSubLocations
boolean
Specifies whether or not to consider sub-locations when filtering by locationId. For this setting to work, the request must contain only a single for filter[locationId]. If true, the search looks for assets within the specified location and in all the sub-locations of the specified location. If false, the search looks for assets only within the specified location(s). Default is false.
Response
HTTP Status Code Summary
200
OK
Successfully returned a page of assets.
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
The request was not accepted because the rate limit was exceeded due to too many requests being made.
500
Internal Server Error
An unexpected error occurred on the server
Response
Body Structure (200)
 Expand all
pagination
object
results
array: object
Result assets
Example
Successfully returned a page of assets.

Request
curl -v 'https://developer.api.autodesk.com/bim360/assets/v2/projects/:projectId/assets?cursorState=eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9&filter[customAttributes]=[object Object]&filter[searchText]=Air Handler&filter[updatedAt]=2020-05-01T06:00:00.000Z..&sort=createdAt asc,clientAssetId desc&includeCustomAttributes=true&includeDeleted=true' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 25,
    "cursorState": "eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9",
    "nextUrl": "https://developer.api.autodesk.com/bim360/assets/v1/projects/04605b7a-0c53-421e-8e11-c743e75ac10a/assets?cursorState=eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9"
  },
  "results": [
    {
      "id": "b302d910-b5e3-46ba-81d8-6b6d30406e14",
      "createdAt": "2020-05-01T06:00:00.000Z",
      "createdBy": "LA7ZL85MU7ML",
      "updatedAt": "2020-05-01T06:00:00.000Z",
      "updatedBy": "LA7ZL85MU7ML",
      "deletedAt": "2020-05-01T06:00:00.000Z",
      "deletedBy": "LA7ZL85MU7ML",
      "isActive": true,
      "version": 1,
      "clientAssetId": "MVS-3D2",
      "categoryId": "42",
      "statusId": "84eb6a10-dde3-475f-aaf4-b5df3aebbd0b",
      "description": "AC unit for basement",
      "locationId": "826e102a-36de-41e7-8c58-1b1696ccbba8",
      "barcode": "F0086728",
      "customAttributes": {
        "ca1": true,
        "ca2": 6.5,
        "ca4": "688f8cfb-0eb4-4289-9d18-96007875dec3",
        "ca5": [
          "9e653094-8d9e-4050-a97a-24d9c5a3786f",
          "e88357bc-e3dd-4cd8-a9e2-6d659b301e7f"
        ],
        "ca6": "text value"
      },
      "companyId": "07b5f07d-c54a-4236-a086-f84192fabdb3"
    }
  ]
}

Documentation /BIM 360 API /API Reference
Categories
GET	categories
Searches for and returns all specified categories.

This endpoint accepts a set of optional category property filters, then uses supplied filters to search for and return categories within a project that satisfy those filters. If no filters are set, this endpoint returns all categories within a project.

Note that although the endpoint returns pagination fields for API consistency, the endpoint does not support pagination in requests.

To understand the basics of categories, category inheritance, and the Assets settings that define them, see the Assets Field Guide.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/assets/v1/projects/{projectId}/categories
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
The BIM 360 project ID. Must be a UUID or a project ID of the form “b.{UUID}”.
Request
Query String Parameters
filter[isActive]
boolean
Specifies whether or not to return categories that are active. If true, return only active categories. If false, return only inactive categories. Default is to return both active and inactive categories, to ensure full tree structure is returned (conversely, full tree structure is not guaranteed when filtering active or inactive categories).
Note that this behavior is different than that of the includeDeleted flag other endpoints use.

filter[parentId]
string
Specifies the parent category ID of returned categories. The query returns only categories that are direct child categories of the specified category.
filter[maxDepth]
number
Specifies the depth of the category tree to return, starting with the root category. Depth 0 means to return only the root category. Depth 4, for example, means to return only the root category and categories that are four levels of inheritance deep, but not to return categories that are five or more levels deep.
Note that this can be used in conjunction with filter[parentId], but that the depth is still computed from the root category, not the parent category specified by the filter.

filter[updatedAt]
string
A string that specifies a date and time or a date and time range at which all returned objects mast have been updated. A single date and time takes this format: YYYY-MM-DDThh:mm:ss.SSSZ, A date and time range takes this format: YYYY-MM-DDThh:mm:ss.SSSZ..YYYY-MM-DDThh:mm:ss.SSSZ. Range queries can be closed or open in either direction: YYYY-MM-DDThh:mm:ss.SSSZ.. or ..YYYY-MM-DDThh:mm:ss.SSSZ.
includeUid
boolean
If provided, and set to true, the globally-unique category uid field will be present in the response. The globally unique category ID is used with the (upcoming) v3 category APIs. The option to include the globally-unique ID with the v1 category APIs is to help consumers transition to the new IDs.
Response
HTTP Status Code Summary
200
OK
Successfully returned a page of categories.
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
The request was not accepted because the rate limit was exceeded due to too many requests being made.
500
Internal Server Error
An unexpected error occurred on the server
Response
Body Structure (200)
 Expand all
pagination
object
The pagination object.
results
array: object
Result categories
Example
Successfully returned a page of categories.

Request
curl -v 'https://developer.api.autodesk.com/bim360/assets/v1/projects/:projectId/categories?filter[isActive]=true&filter[parentId]=122&filter[maxDepth]=3&filter[updatedAt]=2020-05-01T06:00:00.000Z..&includeUid=true' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 25,
    "offset": 0,
    "totalResults": 100
  },
  "results": [
    {
      "id": "123",
      "createdAt": "2020-05-01T06:00:00.000Z",
      "createdBy": "LA7ZL85MU7ML",
      "updatedAt": "2020-05-01T06:00:00.000Z",
      "updatedBy": "LA7ZL85MU7ML",
      "deletedAt": "2020-05-01T06:00:00.000Z",
      "deletedBy": "LA7ZL85MU7ML",
      "isActive": true,
      "name": "Electrical",
      "description": "Electrical Outlets",
      "uid": "b4511bcd-e141-4253-8607-26b194de4ae3",
      "parentId": "122",
      "isRoot": false,
      "isLeaf": false,
      "subcategoryIds": [
        "124",
        "125"
      ]
    }
  ]
}

Documentation /BIM 360 API /API Reference
Status-Sets
GET	status-step-sets
Searches for and returns all specified status sets.

This endpoint accepts a set of optional status set query parameters (described below), then uses those parameters to search for and return status sets within a project that satisfy those parameters. If no parameters are set, this endpoint returns all active status sets within a project.

The endpoint paginates returned status sets. If you don’t specify pagination fields, your query will execute using the default page size. If you want to specify a different a page size, use the limit query parameter.

A paginated response to a query includes pagination information that may contain a nextUrl field. Use the URL it provides to request the next page in the query, then use the nextUrl field in that subsequent response to request the next page in the query, and so on until the response contains no nextUrl value, which means the query is finished returning objects. Note that you should not edit the nextUrl value to alter filter and sort values.

If you want to create your own sequence of requests to retrieve all of a query’s pages without using nextUrl, you can use the cursorState value returned by each request to specify where the next request should start the next page.

To understand the basics of status sets, and the Assets settings that define them, see the Assets Field Guide.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/assets/v1/projects/{projectId}/status-step-sets
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
The BIM 360 project ID. Must be a UUID or a project ID of the form “b.{UUID}”.
Request
Query String Parameters
limit
int
The maximum number of objects that can be returned in a page. A request might return fewer objects than the limit if the Assets service runs out of specified objects to return - at the end of a set of paged results, for example. The maximum limit is 200; the default limit is 25.
cursorState
string
An opaque cursor token that identifies where the next page of paginated results should start. It’s returned in each paginated response so that it can be supplied in the next request to continue paginated results. If a paginated response contains no cursorState value, then there are no further pages to return.
Omit this field to initiate a paginated request or to restart pagination.

includeDeleted
boolean
Whether or not soft-deleted object should be included in the response. If true, soft-deleted objects are returned. If false, they are not. The default is false.
filter[updatedAt]
string
A string that specifies a date and time or a date and time range at which all returned objects mast have been updated. A single date and time takes this format: YYYY-MM-DDThh:mm:ss.SSSZ, A date and time range takes this format: YYYY-MM-DDThh:mm:ss.SSSZ..YYYY-MM-DDThh:mm:ss.SSSZ. Range queries can be closed or open in either direction: YYYY-MM-DDThh:mm:ss.SSSZ.. or ..YYYY-MM-DDThh:mm:ss.SSSZ.
Response
HTTP Status Code Summary
200
OK
Successfully returned a page of status sets.
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
The request was not accepted because the rate limit was exceeded due to too many requests being made.
500
Internal Server Error
An unexpected error occurred on the server
Response
Body Structure (200)
 Expand all
pagination
object
results
array: object
Result status sets
Example
Successfully returned a page of status sets.

Request
curl -v 'https://developer.api.autodesk.com/bim360/assets/v1/projects/:projectId/status-step-sets?cursorState=eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9&includeDeleted=true&filter[updatedAt]=2020-05-01T06:00:00.000Z..' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 25,
    "cursorState": "eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9",
    "nextUrl": "https://developer.api.autodesk.com/bim360/assets/v1/projects/04605b7a-0c53-421e-8e11-c743e75ac10a/assets?cursorState=eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9"
  },
  "results": [
    {
      "id": "b302d910-b5e3-46ba-81d8-6b6d30406e14",
      "createdAt": "2020-05-01T06:00:00.000Z",
      "createdBy": "LA7ZL85MU7ML",
      "updatedAt": "2020-05-01T06:00:00.000Z",
      "updatedBy": "LA7ZL85MU7ML",
      "deletedAt": "2020-05-01T06:00:00.000Z",
      "deletedBy": "LA7ZL85MU7ML",
      "isActive": true,
      "version": 1,
      "projectId": "f74a012c-62fd-4988-ac2b-c5b4fd937724",
      "name": "Spatiotemporal Status Set",
      "description": "My really cool status step set",
      "isDefault": false,
      "values": [
        {
          "label": "Functional-Testing",
          "description": "Custom Functional Testing Status",
          "color": "green",
          "statusStepSetId": "6eb35939-e5fb-453a-98ed-e2e11f326e73",
          "id": "b302d910-b5e3-46ba-81d8-6b6d30406e14",
          "createdAt": "2020-05-01T06:00:00.000Z",
          "createdBy": "LA7ZL85MU7ML",
          "updatedAt": "2020-05-01T06:00:00.000Z",
          "updatedBy": "LA7ZL85MU7ML",
          "deletedAt": "2020-05-01T06:00:00.000Z",
          "deletedBy": "LA7ZL85MU7ML",
          "isActive": true,
          "version": 1,
          "projectId": "f74a012c-62fd-4988-ac2b-c5b4fd937724",
          "bucket": "custom_functional_testing_status_1582935184385",
          "sortOrder": 1
        }
      ]
    }
  ]
}

Documentation /BIM 360 API /API Reference
Status-Sets
POST	status-step-sets:batch-get
Returns a specified set of status sets.

This endpoint accepts an object with an array of one or more status set IDs and returns an array of status sets corresponding to each of those IDs. Invalid status set IDs will simply be omitted from the response and the client is responsible for identifying missing results.

To understand the basics of status sets, and the Assets settings that define them, see the Assets Field Guide.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/bim360/assets/v1/projects/{projectId}/status-step-sets:batch-get
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
* Required
Request
URI Parameters
projectId
string
The BIM 360 project ID. Must be a UUID or a project ID of the form “b.{UUID}”.
Request
Query String Parameters
includeDeleted
boolean
Whether or not soft-deleted object should be included in the response. If true, soft-deleted objects are returned. If false, they are not. The default is false.
Request
Body Structure
Request payload for fetching a batch of status sets by IDs

ids
array: string
An array of unique IDs of status sets to fetch.
Response
HTTP Status Code Summary
200
OK
Successfully returned a batch of status sets.
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
The request was not accepted because the rate limit was exceeded due to too many requests being made.
500
Internal Server Error
An unexpected error occurred on the server
Response
Body Structure (200)
 Expand all
results
array: object
Returned status sets
Example
Successfully returned a batch of status sets.

Request
curl -v 'https://developer.api.autodesk.com/bim360/assets/v1/projects/:projectId/status-step-sets:batch-get?includeDeleted=true' \
  -X 'POST' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a' \
  -H 'Content-Type: application/json' \
  -d '{
        "ids": [
          "6eb35939-e5fb-453a-98ed-e2e11f326e73"
        ]
      }'
Show Less
Response
{
  "results": [
    {
      "id": "b302d910-b5e3-46ba-81d8-6b6d30406e14",
      "createdAt": "2020-05-01T06:00:00.000Z",
      "createdBy": "LA7ZL85MU7ML",
      "updatedAt": "2020-05-01T06:00:00.000Z",
      "updatedBy": "LA7ZL85MU7ML",
      "deletedAt": "2020-05-01T06:00:00.000Z",
      "deletedBy": "LA7ZL85MU7ML",
      "isActive": true,
      "version": 1,
      "projectId": "f74a012c-62fd-4988-ac2b-c5b4fd937724",
      "name": "Spatiotemporal Status Set",
      "description": "My really cool status step set",
      "isDefault": false,
      "values": [
        {
          "label": "Functional-Testing",
          "description": "Custom Functional Testing Status",
          "color": "green",
          "statusStepSetId": "6eb35939-e5fb-453a-98ed-e2e11f326e73",
          "id": "b302d910-b5e3-46ba-81d8-6b6d30406e14",
          "createdAt": "2020-05-01T06:00:00.000Z",
          "createdBy": "LA7ZL85MU7ML",
          "updatedAt": "2020-05-01T06:00:00.000Z",
          "updatedBy": "LA7ZL85MU7ML",
          "deletedAt": "2020-05-01T06:00:00.000Z",
          "deletedBy": "LA7ZL85MU7ML",
          "isActive": true,
          "version": 1,
          "projectId": "f74a012c-62fd-4988-ac2b-c5b4fd937724",
          "bucket": "custom_functional_testing_status_1582935184385",
          "sortOrder": 1
        }
      ]
    }
  ]
}

Documentation /BIM 360 API /API Reference
Status-Sets
POST	category-status-step-sets/status-step-sets:batch-get
Returns status set assignments associated with a specified set of categories. It can return just explicit status set assignments or both explicitly and inherited status set assignments.

An explicitly-assigned status set is assigned to a category so that the status set overrides the status set that would otherwise be inherited from the category’s parent.

When this endpoint is set to return both explicitly-defined and inherited status set assignments, it returns a status set assignment for each of the specified categories. If some of these categories have inherited status sets, it means that those inherited status sets may appear more than once in the return, but will each show a different associated category. An additional field inheritedFromCategoryId will be added to the assignment record to indicate which category the status set assignment is inherited from.

When this endpoint is set to return only explicit status set assignments, it ignores any specified categories that inherit their status set. Returned status set assignments appear once each and show their category associations with the category where the status set was assigned. Any specified categories with inherited status sets don’t return a status set.

To understand the basics of status sets, inheritance, and the Assets settings that define them, see the Assets Field Guide.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/bim360/assets/v1/projects/{projectId}/category-status-step-sets/status-step-sets:batch-get
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
* Required
Request
URI Parameters
projectId
string
The BIM 360 project ID. Must be a UUID or a project ID of the form “b.{UUID}”.
Request
Query String Parameters
includeInherited
boolean
Specifies whether or not to return status sets for categories that inherit their status set. If true, returns a status set (inherited or not) for each specified category. If false, returns only explicitly-defined status sets associated with the specified categories. Default is false.
Request
Body Structure
ids
array: string
A set of unique IDs of categories to return status set assignments for.
Response
HTTP Status Code Summary
200
OK
Successfully returned the status sets for the specified category IDs.
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
The request was not accepted because the rate limit was exceeded due to too many requests being made.
500
Internal Server Error
An unexpected error occurred on the server
Response
Body Structure (200)
 Expand all
results
array: object
Returned status set category assignments.
Example
Successfully returned the status sets for the specified category IDs.

Request
curl -v 'https://developer.api.autodesk.com/bim360/assets/v1/projects/:projectId/category-status-step-sets/status-step-sets:batch-get' \
  -X 'POST' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a' \
  -H 'Content-Type: application/json' \
  -d '{
        "ids": [
          "123"
        ]
      }'
Show Less
Response
{
  "results": [
    {
      "categoryId": "124",
      "statusStepSetId": "6eb35939-e5fb-453a-98ed-e2e11f326e73",
      "inheritedFromCategoryId": "123"
    }
  ]
}

Documentation /BIM 360 API /API Reference
Statuses
POST	asset-statuses:batch-get
Returns a specified set of statuses.

This endpoint accepts an object with an array of one or more status IDs and returns an array of statuses corresponding to each of those IDs. Invalid status IDs will simply be omitted from the response and the client is responsible for identifying missing results.

To understand the basics of asset statuses, and the Assets settings that define them, see the Assets Field Guide.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/bim360/assets/v1/projects/{projectId}/asset-statuses:batch-get
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
* Required
Request
URI Parameters
projectId
string
The BIM 360 project ID. Must be a UUID or a project ID of the form “b.{UUID}”.
Request
Query String Parameters
includeDeleted
boolean
Whether or not soft-deleted object should be included in the response. If true, soft-deleted objects are returned. If false, they are not. The default is false.
Request
Body Structure
ids
array: string
Unique IDs of entities to fetch
Response
HTTP Status Code Summary
200
OK
Successfully returned a batch of statuses.
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
The request was not accepted because the rate limit was exceeded due to too many requests being made.
500
Internal Server Error
An unexpected error occurred on the server
Response
Body Structure (200)
 Expand all
results
array: object
Returned statuses
Example
Successfully returned a batch of statuses.

Request
curl -v 'https://developer.api.autodesk.com/bim360/assets/v1/projects/:projectId/asset-statuses:batch-get?includeDeleted=true' \
  -X 'POST' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a' \
  -H 'Content-Type: application/json' \
  -d '{
        "ids": [
          "84eb6a10-dde3-475f-aaf4-b5df3aebbd0b"
        ]
      }'
Show Less
Response
{
  "results": [
    {
      "label": "Functional-Testing",
      "description": "Custom Functional Testing Status",
      "color": "green",
      "statusStepSetId": "6eb35939-e5fb-453a-98ed-e2e11f326e73",
      "id": "b302d910-b5e3-46ba-81d8-6b6d30406e14",
      "createdAt": "2020-05-01T06:00:00.000Z",
      "createdBy": "LA7ZL85MU7ML",
      "updatedAt": "2020-05-01T06:00:00.000Z",
      "updatedBy": "LA7ZL85MU7ML",
      "deletedAt": "2020-05-01T06:00:00.000Z",
      "deletedBy": "LA7ZL85MU7ML",
      "isActive": true,
      "version": 1,
      "projectId": "f74a012c-62fd-4988-ac2b-c5b4fd937724",
      "bucket": "custom_functional_testing_status_1582935184385",
      "sortOrder": 1
    }
  ]
}

Documentation /BIM 360 API /API Reference
Statuses
GET	asset-statuses
Searches for and returns all specified asset statuses.

This endpoint accepts a set of optional status query parameters (described below), then uses those parameters to search for and return statuses within a project that satisfy those parameters. If no parameters are set, this endpoint returns all active statuses within a project.

The endpoint paginates returned statuses. If you don’t specify pagination fields, your query will execute using the default page size. If you want to specify a different a page size, use the limit query parameter.

A paginated response to a query includes pagination information that may contain a nextUrl field. Use the URL it provides to request the next page in the query, then use the nextUrl field in that subsequent response to request the next page in the query, and so on until the response contains no nextUrl value, which means the query is finished returning objects. Note that you should not edit the nextUrl value to alter filter and sort values.

If you want to create your own sequence of requests to retrieve all of a query’s pages without using nextUrl, you can use the cursorState value returned by each request to specify where the next request should start the next page.

To understand the basics of asset statuses, and the Assets settings that define them, see the Assets Field Guide.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/assets/v1/projects/{projectId}/asset-statuses
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
The BIM 360 project ID. Must be a UUID or a project ID of the form “b.{UUID}”.
Request
Query String Parameters
cursorState
string
An opaque cursor token that identifies where the next page of paginated results should start. It’s returned in each paginated response so that it can be supplied in the next request to continue paginated results. If a paginated response contains no cursorState value, then there are no further pages to return.
Omit this field to initiate a paginated request or to restart pagination.

limit
int
The maximum number of objects that can be returned in a page. A request might return fewer objects than the limit if the Assets service runs out of specified objects to return - at the end of a set of paged results, for example. The maximum limit is 200; the default limit is 25.
includeDeleted
boolean
Whether or not soft-deleted object should be included in the response. If true, soft-deleted objects are returned. If false, they are not. The default is false.
filter[updatedAt]
string
A string that specifies a date and time or a date and time range at which all returned objects mast have been updated. A single date and time takes this format: YYYY-MM-DDThh:mm:ss.SSSZ, A date and time range takes this format: YYYY-MM-DDThh:mm:ss.SSSZ..YYYY-MM-DDThh:mm:ss.SSSZ. Range queries can be closed or open in either direction: YYYY-MM-DDThh:mm:ss.SSSZ.. or ..YYYY-MM-DDThh:mm:ss.SSSZ.
Response
HTTP Status Code Summary
200
OK
Successfully returned a page of statuses.
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
The request was not accepted because the rate limit was exceeded due to too many requests being made.
500
Internal Server Error
An unexpected error occurred on the server
Response
Body Structure (200)
 Expand all
pagination
object
results
array: object
Result statuses
Example
Successfully returned a page of statuses.

Request
curl -v 'https://developer.api.autodesk.com/bim360/assets/v1/projects/:projectId/asset-statuses?cursorState=eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9&includeDeleted=true&filter[updatedAt]=2020-05-01T06:00:00.000Z..' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 25,
    "cursorState": "eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9",
    "nextUrl": "https://developer.api.autodesk.com/bim360/assets/v1/projects/04605b7a-0c53-421e-8e11-c743e75ac10a/assets?cursorState=eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9"
  },
  "results": [
    {
      "label": "Functional-Testing",
      "description": "Custom Functional Testing Status",
      "color": "green",
      "statusStepSetId": "6eb35939-e5fb-453a-98ed-e2e11f326e73",
      "id": "b302d910-b5e3-46ba-81d8-6b6d30406e14",
      "createdAt": "2020-05-01T06:00:00.000Z",
      "createdBy": "LA7ZL85MU7ML",
      "updatedAt": "2020-05-01T06:00:00.000Z",
      "updatedBy": "LA7ZL85MU7ML",
      "deletedAt": "2020-05-01T06:00:00.000Z",
      "deletedBy": "LA7ZL85MU7ML",
      "isActive": true,
      "version": 1,
      "projectId": "f74a012c-62fd-4988-ac2b-c5b4fd937724",
      "bucket": "custom_functional_testing_status_1582935184385",
      "sortOrder": 1
    }
  ]
}

Documentation /BIM 360 API /API Reference
Custom-Attributes
POST	custom-attributes:batch-get
Returns a specified set of custom attributes.

This endpoint accepts an object with an array of one or more custom attribute IDs, and/or an array of one or more custom attribute names, and returns an array of custom attributes corresponding to each of those IDs and/or names. Invalid custom attribute IDs and/or names will simply be omitted from the response and the client is responsible for identifying missing results.

To understand the basics of custom attributes, and the Assets settings that define them, see the Assets Field Guide.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/bim360/assets/v1/projects/{projectId}/custom-attributes:batch-get
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
* Required
Request
URI Parameters
projectId
string
The BIM 360 project ID. Must be a UUID or a project ID of the form “b.{UUID}”.
Request
Query String Parameters
includeDeleted
boolean
Whether or not soft-deleted object should be included in the response. If true, soft-deleted objects are returned. If false, they are not. The default is false.
Request
Body Structure
ids
array: string
Unique IDs of Custom Attributes to fetch. One or both of these body structure fields must be present to specify at least one custom attribute.
names
array: string
Unique names of custom attributes to fetch. One or both of these body structure fields must be present to specify at least one custom attribute. Note that the unique name of a custom attribute is not the display name of the attribute, but the immutable name returned by the attribute’s name field.
Response
HTTP Status Code Summary
200
OK
Successfully returned a batch of custom attributes.
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
The request was not accepted because the rate limit was exceeded due to too many requests being made.
500
Internal Server Error
An unexpected error occurred on the server
Response
Body Structure (200)
 Expand all
results
array: object
Returned custom attributes
Example
Successfully returned a batch of custom attributes.

Request
curl -v 'https://developer.api.autodesk.com/bim360/assets/v1/projects/:projectId/custom-attributes:batch-get?includeDeleted=true' \
  -X 'POST' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a' \
  -H 'Content-Type: application/json' \
  -d '{
        "ids": [
          "3063f212-6ce9-494e-b749-eb73b4445bf0"
        ],
        "names": [
          "ca1"
        ]
      }'
Show Less
Response
{
  "results": [
    {
      "displayName": "Elevator Speed",
      "description": "The average speed of an elevator in meters per second",
      "enumValues": [
        "Custom Select Value"
      ],
      "requiredOnIngress": true,
      "maxLengthOnIngress": 100,
      "defaultValue": "2019-01-01",
      "dataType": "multi_select",
      "id": "b302d910-b5e3-46ba-81d8-6b6d30406e14",
      "createdAt": "2020-05-01T06:00:00.000Z",
      "createdBy": "LA7ZL85MU7ML",
      "updatedAt": "2020-05-01T06:00:00.000Z",
      "updatedBy": "LA7ZL85MU7ML",
      "deletedAt": "2020-05-01T06:00:00.000Z",
      "deletedBy": "LA7ZL85MU7ML",
      "isActive": true,
      "version": 1,
      "projectId": "f74a012c-62fd-4988-ac2b-c5b4fd937724",
      "name": "ca1",
      "values": [
        {
          "id": "b302d910-b5e3-46ba-81d8-6b6d30406e14",
          "createdAt": "2020-05-01T06:00:00.000Z",
          "createdBy": "LA7ZL85MU7ML",
          "updatedAt": "2020-05-01T06:00:00.000Z",
          "updatedBy": "LA7ZL85MU7ML",
          "deletedAt": "2020-05-01T06:00:00.000Z",
          "deletedBy": "LA7ZL85MU7ML",
          "isActive": true,
          "version": 1,
          "projectId": "f74a012c-62fd-4988-ac2b-c5b4fd937724",
          "customAttributeId": "3063f212-6ce9-494e-b749-eb73b4445bf0",
          "displayName": "Custom Select Value"
        }
      ]
    }
  ]
}

Documentation /BIM 360 API /API Reference
Custom-Attributes
GET	custom-attributes
Searches for and returns all specified custom attributes.

This endpoint accepts a set of optional custom attribute query parameters (described below), then uses those parameters to search for and return custom attributes within a project that satisfy those parameters. If no parameters are set, this endpoint returns all active custom attributes within a project.

This endpoint paginates returned custom attributes. If you don’t specify pagination fields, your query will execute using the default page size. If you want to specify a different a page size, use the limit query parameter.

A paginated response to a query includes pagination information that may contain a nextUrl field. Use the URL it provides to request the next page in the query, then use the nextUrl field in that subsequent response to request the next page in the query, and so on until the response contains no nextUrl value, which means the query is finished returning objects. Note that you should not edit the nextUrl value to alter filter and sort values.

If you want to create your own sequence of requests to retrieve all of a query’s pages without using nextUrl, you can use the cursorState value returned by each request to specify where the next request should start the next page.

To understand the basics of custom attributes, and the Assets settings that define them, see the Assets Field Guide.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/assets/v1/projects/{projectId}/custom-attributes
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
The BIM 360 project ID. Must be a UUID or a project ID of the form “b.{UUID}”.
Request
Query String Parameters
limit
int
The maximum number of objects that can be returned in a page. A request might return fewer objects than the limit if the Assets service runs out of specified objects to return - at the end of a set of paged results, for example. The maximum limit is 200; the default limit is 25.
cursorState
string
An opaque cursor token that identifies where the next page of paginated results should start. It’s returned in each paginated response so that it can be supplied in the next request to continue paginated results. If a paginated response contains no cursorState value, then there are no further pages to return.
Omit this field to initiate a paginated request or to restart pagination.

includeDeleted
boolean
Whether or not soft-deleted object should be included in the response. If true, soft-deleted objects are returned. If false, they are not. The default is false.
filter[updatedAt]
string
A string that specifies a date and time or a date and time range at which all returned objects mast have been updated. A single date and time takes this format: YYYY-MM-DDThh:mm:ss.SSSZ, A date and time range takes this format: YYYY-MM-DDThh:mm:ss.SSSZ..YYYY-MM-DDThh:mm:ss.SSSZ. Range queries can be closed or open in either direction: YYYY-MM-DDThh:mm:ss.SSSZ.. or ..YYYY-MM-DDThh:mm:ss.SSSZ.
Response
HTTP Status Code Summary
200
OK
Successfully returned a page of custom attributes.
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
The request was not accepted because the rate limit was exceeded due to too many requests being made.
500
Internal Server Error
An unexpected error occurred on the server
Response
Body Structure (200)
 Expand all
pagination
object
results
array: object
Result custom attributes
Example
Successfully returned a page of custom attributes.

Request
curl -v 'https://developer.api.autodesk.com/bim360/assets/v1/projects/:projectId/custom-attributes?cursorState=eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9&includeDeleted=true&filter[updatedAt]=2020-05-01T06:00:00.000Z..' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 25,
    "cursorState": "eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9",
    "nextUrl": "https://developer.api.autodesk.com/bim360/assets/v1/projects/04605b7a-0c53-421e-8e11-c743e75ac10a/assets?cursorState=eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9"
  },
  "results": [
    {
      "displayName": "Elevator Speed",
      "description": "The average speed of an elevator in meters per second",
      "enumValues": [
        "Custom Select Value"
      ],
      "requiredOnIngress": true,
      "maxLengthOnIngress": 100,
      "defaultValue": "2019-01-01",
      "dataType": "multi_select",
      "id": "b302d910-b5e3-46ba-81d8-6b6d30406e14",
      "createdAt": "2020-05-01T06:00:00.000Z",
      "createdBy": "LA7ZL85MU7ML",
      "updatedAt": "2020-05-01T06:00:00.000Z",
      "updatedBy": "LA7ZL85MU7ML",
      "deletedAt": "2020-05-01T06:00:00.000Z",
      "deletedBy": "LA7ZL85MU7ML",
      "isActive": true,
      "version": 1,
      "projectId": "f74a012c-62fd-4988-ac2b-c5b4fd937724",
      "name": "ca1",
      "values": [
        {
          "id": "b302d910-b5e3-46ba-81d8-6b6d30406e14",
          "createdAt": "2020-05-01T06:00:00.000Z",
          "createdBy": "LA7ZL85MU7ML",
          "updatedAt": "2020-05-01T06:00:00.000Z",
          "updatedBy": "LA7ZL85MU7ML",
          "deletedAt": "2020-05-01T06:00:00.000Z",
          "deletedBy": "LA7ZL85MU7ML",
          "isActive": true,
          "version": 1,
          "projectId": "f74a012c-62fd-4988-ac2b-c5b4fd937724",
          "customAttributeId": "3063f212-6ce9-494e-b749-eb73b4445bf0",
          "displayName": "Custom Select Value"
        }
      ]
    }
  ]
}

Documentation /BIM 360 API /API Reference
Custom-Attributes
GET	categories/:categoryId/custom-attributes
Returns the custom attribute assignments for a specified category.

This endpoint can return only custom attributes that are explicitly assigned to the specified category, ignoring inherited custom attributes, or it can include both explicitly assigned and inherited custom attributes.

When this endpoint is set to return both explicitly-assigned and inherited custom attributes, custom attributes that are inherited for this category will have an additonal field inheritedFromCategoryId to indicate which category the custom attribute assignment is inherited from.

Note that although the endpoint returns pagination fields for API consistency, the endpoint does not support pagination. All assigned custom attributes, explicit or inherited, will be returned in the first page of results.

To understand the basics of custom attributes, inheritance, and the Assets settings that define them, see the Assets Field Guide.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/assets/v1/projects/{projectId}/categories/{categoryId}/custom-attributes
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
The BIM 360 project ID. Must be a UUID or a project ID of the form “b.{UUID}”.
categoryId
string
The category ID
Request
Query String Parameters
includeInherited
boolean
Specifies whether or not to return custom attributes that were inherited from the specified category’s parent category. If true, then it returns inherited custom attributes. If false, then it returns only custom attributes explicitly assigned to the specified category. Default is false.
Response
HTTP Status Code Summary
200
OK
Successfully returned the specified category’s Asset custom attributes.
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
The request was not accepted because the rate limit was exceeded due to too many requests being made.
500
Internal Server Error
An unexpected error occurred on the server
Response
Body Structure (200)
 Expand all
pagination
object
The pagination object.
results
array: object
Result custom attributes
Example
Successfully returned the specified category’s Asset custom attributes.

Request
curl -v 'https://developer.api.autodesk.com/bim360/assets/v1/projects/:projectId/categories/123/custom-attributes' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 25,
    "offset": 0,
    "totalResults": 100
  },
  "results": [
    {
      "displayName": "Elevator Speed",
      "description": "The average speed of an elevator in meters per second",
      "enumValues": [
        "Custom Select Value"
      ],
      "requiredOnIngress": true,
      "maxLengthOnIngress": 100,
      "defaultValue": "2019-01-01",
      "dataType": "multi_select",
      "id": "b302d910-b5e3-46ba-81d8-6b6d30406e14",
      "createdAt": "2020-05-01T06:00:00.000Z",
      "createdBy": "LA7ZL85MU7ML",
      "updatedAt": "2020-05-01T06:00:00.000Z",
      "updatedBy": "LA7ZL85MU7ML",
      "deletedAt": "2020-05-01T06:00:00.000Z",
      "deletedBy": "LA7ZL85MU7ML",
      "isActive": true,
      "version": 1,
      "projectId": "f74a012c-62fd-4988-ac2b-c5b4fd937724",
      "name": "ca1",
      "values": [
        {
          "id": "b302d910-b5e3-46ba-81d8-6b6d30406e14",
          "createdAt": "2020-05-01T06:00:00.000Z",
          "createdBy": "LA7ZL85MU7ML",
          "updatedAt": "2020-05-01T06:00:00.000Z",
          "updatedBy": "LA7ZL85MU7ML",
          "deletedAt": "2020-05-01T06:00:00.000Z",
          "deletedBy": "LA7ZL85MU7ML",
          "isActive": true,
          "version": 1,
          "projectId": "f74a012c-62fd-4988-ac2b-c5b4fd937724",
          "customAttributeId": "3063f212-6ce9-494e-b749-eb73b4445bf0",
          "displayName": "Custom Select Value"
        }
      ],
      "inheritedFromCategoryId": "123"
    }
  ]
}

Documentation /BIM 360 API /API Reference
Error-Codes
GET	error-codes
Retrieves a list of all error codes returned by the Assets API.

You can use this information to allow the client to better handle error responses programmatically.

Note that although the response is in a paginated format, all results will be returned for every request.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/assets/v1/error-codes
Authentication Context	
No security required
Required OAuth Scopes	
No scopes required
Data Format	
JSON
Response
HTTP Status Code Summary
200
OK
Successfully retrieved all error codes.
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
The request was not accepted because the rate limit was exceeded due to too many requests being made.
500
Internal Server Error
An unexpected error occurred on the server
Response
Body Structure (200)
 Expand all
pagination
object
The pagination object.
results
array: object
A list of Assets API errors.
Example
Successfully retrieved all error codes.

Request
curl -v 'https://developer.api.autodesk.com/bim360/assets/v1/error-codes'
Response
{
  "pagination": {
    "limit": 61,
    "offset": 0,
    "totalResults": 61
  },
  "results": [
    {
      "name": "FIELD_EXCEEDS_MAX_LENGTH",
      "description": "A string field exceeds the max allowed length.",
      "httpStatusCode": 400,
      "metadataKeys": [
        "fieldName",
        "maxStringLength"
      ]
    }
  ]
}

Documentation /BIM 360 API /API Reference
Error-Codes
GET	error-codes/:errorCodeName
Retrieves details about an error code by name.

To find a list of error codes, call GET error-codes.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/assets/v1/error-codes/{errorCodeName}
Authentication Context	
No security required
Required OAuth Scopes	
No scopes required
Data Format	
JSON
Request
URI Parameters
errorCodeName
string
The name of an error code returned in an error response, in the errorCode field.
Response
HTTP Status Code Summary
200
OK
Successfully retrieved the error code details.
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
The request was not accepted because the rate limit was exceeded due to too many requests being made.
500
Internal Server Error
An unexpected error occurred on the server
Response
Body Structure (200)
name
string
The error code name.
description
string
A description of the error.
httpStatusCode
number
The HTTP status code typically returned when this error occurs.
Note that there may be exceptions, for example, if an internal server error occurs the status code associated with this error may be different.

metadataKeys
array: string
The metadata keys relevant to the error code.
Example
Successfully retrieved the error code details.

Request
curl -v 'https://developer.api.autodesk.com/bim360/assets/v1/error-codes/FIELD_EXCEEDS_MAX_LENGTH'
Response
{
  "name": "FIELD_EXCEEDS_MAX_LENGTH",
  "description": "A string field exceeds the max allowed length.",
  "httpStatusCode": 400,
  "metadataKeys": [
    "fieldName",
    "maxStringLength"
  ]
}

checklist api :

Documentation /BIM 360 API /API Reference
Instances
GET	containers/{containerId}/instances
Retrieves information about all the BIM 360 Field Management checklists in a project, including details about their statuses, priorities, and assignees. To get more information about a single checklist, for example, details about checklist items, sections, attachments, and signatures, see GET instances/:id.

New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is not compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/checklists/v1/containers/{containerId}/instances
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
containerId
string
Each project is assigned a container that stores all the checklists for the project. To find the ID, see the Retrieve a Container ID tutorial.
Request
Query String Parameters
sort
enum:string
Sort the checklists by title, templateType.id, or scheduledDate. For example, sort=title. Separate multiple values with commas. To sort in descending order add a - before the sort criteria; for example, sort=-title. For more details, see JSON API Sorting. Possible values: templateType.id, title, scheduledDate
filter[templateTypeId]
number
Retrieves checklists associated with the specified template type. For example, filter[templateTypeId]=1 or queryFilter[templateType.id]=1 or queryFilter[templateTypeId]=1. Possible values: 1 (quality), 6 (punch List), 11 (safety), 15 (commissioning). Separate multiple values with commas. For more details, see JSON API Filtering.
filter[statusId]
number
Retrieves checklists with the specified status. For example, filter[statusId]=3 or queryFilter[status.id]=3 or queryFilter[statusId]=3. Possible values: 1 (not scheduled), 2 (scheduled), 3 (in progress), 4 (completed), 5 (signed off), 6 (pending signature), 7 (not started). Separate multiple values with commas. For more details, see JSON API Filtering.
filter[assigneeIds]
string
Retrieves checklists assigned to the specified user. For example, filter[assigneeIds]=PER8KQPK2JRT or queryFilter[assignees.assigneeId]=PER8KQPK2JRT or queryFilter[assigneeIds]=PER8KQPK2JRT. Use the assignee’s Autodesk ID. To check a user`s Autodesk ID, call GET users and check the uid. Note that you need to use a 2-legged token to call GET users. For more details, see JSON API Filtering.
filter[scheduledDate]
datetime: ISO 8601
Retrieves checklists with the specified scheduled date. Value is the timestamp of the date in the following format: YYYY-MM-DDThh:mm:ss.sz, or a date range in the following format: YYYY-MM-DDThh:mm:ss.sz...YYYY-MM-DDThh:mm:ss.sz. For more details, see JSON API Filtering.
limit
number
The number of checklists to return in the response payload. Default value: 50. For example, to limit the response to two checklists per page, use page[limit]=2 or limit=2. For more details, see JSON API Paging.
offset
number
The page number that you want to begin checklist results from; for example, page[offset]=20 or offset=20. For more details, see JSON API Paging.
fields[instances]
string
Specify which attributes you want to appear in the response. Separate multiple values with commas; for example, fields[instances]=createdAt,templateType. For more details, see JSON API Sparse Fieldsets.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request header
403
Forbidden
The request has not been applied because it lacks valid authentication credentials for the target resource
410
Forbidden
500
Internal Server Error
An unexpected error occurred on the server
Response
Body Structure (200)
 Expand all
jsonapi
object
The JSON API object.
meta
object
The meta object.
links
object
The links object.
data
array: object
The data object.
Example
Success

Request
curl -v 'https://developer.api.autodesk.com/bim360/checklists/v1/containers/efca79bd-3865-4e68-88d5-30d982175c7d/instances?sort=title&filter[templateTypeId]=1&filter[statusId]=3&filter[assigneeIds]=NZFGQS2CTCCC&filter[scheduledDate]=2017-09-13T10:25:03.000Z&limit=10' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "meta": {
    "offset": 0,
    "limit": 50,
    "total": 210
  },
  "links": {
    "self": "/containers/efca79bd-3865-4e68-88d5-30d982175c7d/instances?page[offset]=50",
    "first": "/containers/efca79bd-3865-4e68-88d5-30d982175c7d/instances?page[offset]=0",
    "last": "/containers/efca79bd-3865-4e68-88d5-30d982175c7d/instances?page[offset]=200",
    "next": "/containers/efca79bd-3865-4e68-88d5-30d982175c7d/instances?page[offset]=100",
    "prev": "/containers/efca79bd-3865-4e68-88d5-30d982175c7d/instances?page[offset]=0"
  },
  "data": [
    {
      "id": "41",
      "type": "instances",
      "attributes": {
        "instanceRevision": "fesd3",
        "urn": "urn:adsk.checklists.cs.instance:efca79bd-3865-4e68-88d5-30d982175c7d/41",
        "scheduledDate": "2018-05-24T15:29:29.772Z",
        "location": "3ba7a68b-1cd2-4a63-a08a-cdda3e94e5ea",
        "title": "Painting Checklist",
        "templateVersionId": 1433,
        "createdBy": "1QAZ2WSX",
        "modifiedBy": "1QAZ2WSX",
        "updatedAt": "2018-05-23T08:18:55.098Z",
        "createdAt": "2018-05-23T08:18:55.098Z",
        "deletedAt": "2018-05-23T08:18:55.098Z",
        "trades": [],
        "instructions": "detailed description",
        "templateType": {
          "id": 1,
          "name": "Quality",
          "permittedAttributes": [
            "id"
          ]
        },
        "status": {
          "id": 4,
          "name": "Completed",
          "urgency": 0,
          "permittedAttributes": [
            "id"
          ]
        },
        "signaturesStatus": "None",
        "assignees": [
          {
            "id": 13200,
            "assigneeId": "93TNJUDDTJXL",
            "name": "John Doe",
            "type": {
              "id": 1,
              "name": "User",
              "permittedAttributes": [
                "id"
              ]
            },
            "permittedAttributes": [
              "assigneeId",
              "name",
              "type"
            ]
          }
        ],
        "progress": 0,
        "completedItemsCount": 0,
        "permittedActions": [
          "canArchive",
          "canEdit"
        ],
        "permittedAttributes": [
          "title",
          "location",
          "scheduledDate",
          "sections",
          "assignees",
          "status"
        ],
        "allowSectionAssignee": true,
        "signatures": [
          {
            "urn": "urn:adsk.checklists.cs.instance.signature:efca79bd-3865-4e68-88d5-30d982175c7d/41",
            "instanceRevision": "fesd3",
            "instanceId": 11453,
            "index": 11,
            "requiredBy": "IKEA",
            "isRequired": true,
            "definedAt": "Template",
            "requiredName": "Carlos",
            "requiredCompany": "IKEA",
            "isSigned": true,
            "formalSignature": {
              "instanceSignedRevision": "fesd6",
              "signedName": "Rodrigo",
              "signedCompany": "IKEA",
              "signedAt": "2018-05-23T08:18:55.098Z",
              "graphic": {
                "type": "SVG",
                "content": "<svg> .... </svg>",
                "permittedAttributes": [
                  "content",
                  "type"
                ]
              },
              "permittedAttributes": [
                "instanceSignedRevision",
                "signedName",
                "signedCompany",
                "signedAt",
                "graphic"
              ]
            },
            "updatedAt": "2018-05-23T08:18:55.098Z",
            "createdAt": "2018-05-23T08:18:55.098Z",
            "deletedAt": "2018-05-23T08:18:55.098Z",
            "submittedBy": "1QAZ2WSX",
            "permittedAttributes": [
              "requiredName",
              "requiredCompany",
              "correlationId"
            ],
            "permittedActions": [
              "canEdit"
            ]
          }
        ]
      },
      "relationships": {
        "sections": {
          "links": {
            "self": "",
            "related": ""
          },
          "meta": {},
          "data": [
            {
              "type": "instance_sections",
              "id": "1"
            }
          ]
        },
        "container": {
          "links": {
            "self": "",
            "related": ""
          },
          "meta": {},
          "data": {
            "type": "containers",
            "id": "efca79bd-3865-4e68-88d5-30d982175c7d"
          }
        },
        "createdFrom": {
          "links": {
            "self": "",
            "related": ""
          },
          "meta": {},
          "data": {
            "type": "templates",
            "id": "66"
          }
        }
      },
      "meta": {
        "totalItems": 1,
        "totalSections": 1,
        "totalRequiredSignatures": 3,
        "totalSignedSignatures": 1,
        "totalUnsignedSignatures": 2
      },
      "links": {
        "self": "",
        "related": ""
      }
    }
  ]
}

Documentation /BIM 360 API /API Reference
Instances
GET	containers/{containerId}/instances/{id}
Retrieves detailed information about a single BIM 360 Field Management checklist (instance). For example, details about checklist items, sections and attachments. To retrieve a detailed response, you need to use the include query string parameter. For information about all the checklists in a project, see GET instances. If the response payload includes data about the checklist’s sections, items, and attachments, you can reconstruct a checklist from the data by linking between the checklist hierarchy in the relationship objects, by following these instuctions:

Find the list of checklist sections in the data.relationships.sections.data array, and note the type (instance_sections) and id for each section.
Find the items that are associated with each section by searching for the section objects in the included array, using the section’s type and id values that you found in the previous step. In the relationships object in the included section object you can find the list of items for that section. Note the type and id for each item (included.sections.relationships.items.data).
Find the attachments that are associated with each item by searching for the item objects in the included array, using the item’s type and id you found in the previous step. In the relationships object in the included item object you can find the list of attachments for that item.
../../../../../_images/checklistsRelations.png
Note that the order of the sections, items, and attachments are determined by the index attribute.

New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is not compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/checklists/v1/containers/{containerId}/instances/{id}
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
containerId
string
Each project is assigned a container that stores all the checklists for the project. To find the ID, see the Retrieve a Container ID tutorial.
id
string
The ID of the checklist.
Request
Query String Parameters
include
array
Include additional data about the checklist’s items, sections, and attachments. Possible values: sections - sections sections.items - items sections.items.attachments - attachments For example, include=sections,sections.items,items.attachments.
fields[instances]
string
Specify which attributes you want to appear in the response. Separate multiple values with commas; for example, fields[instances]=createdAt,templateType. For more details, see JSON API Sparse Fieldsets.
signatures
string
Indicates whether the reponse should include the checklist’s instance-level signature.
If true, this endpoint will return the instance-level signatures object containing the requested checklist’s final signoff signature, along with all section signatures.
If false, this endpoint will not return the instance-level signatures object for the requested checklist, but will still return the section signatures.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request header
403
Forbidden
The request has not been applied because it lacks valid authentication credentials for the target resource
404
Not Found
The resource cannot be found
410
Forbidden
500
Internal Server Error
An unexpected error occurred on the server
Response
Body Structure (200)
 Expand all
jsonapi
object
The JSON API object.
meta
object
The meta object.
links
object
The links object.
data
object
The data object.
included
array: object
A list of the items (instance_items), sections (instance_sections), and attachments (instance_item_attachments) in the checklist. The contents of the list is defined in the request using the include parameter.
Example
Success

Request
curl -v 'https://developer.api.autodesk.com/bim360/checklists/v1/containers/efca79bd-3865-4e68-88d5-30d982175c7d/instances/41?include=sections,sections.items,sections.items.attachments&signatures=true' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "meta": {},
  "links": {
    "self": "",
    "related": ""
  },
  "data": {
    "id": "41",
    "type": "instances",
    "attributes": {
      "instanceRevision": "fesd3",
      "urn": "urn:adsk.checklists.cs.instance:efca79bd-3865-4e68-88d5-30d982175c7d/41",
      "scheduledDate": "2018-05-24T15:29:29.772Z",
      "location": "3ba7a68b-1cd2-4a63-a08a-cdda3e94e5ea",
      "title": "Painting Checklist",
      "templateVersionId": 1433,
      "createdBy": "1QAZ2WSX",
      "modifiedBy": "1QAZ2WSX",
      "updatedAt": "2018-05-23T08:18:55.098Z",
      "createdAt": "2018-05-23T08:18:55.098Z",
      "deletedAt": "2018-05-23T08:18:55.098Z",
      "trades": [],
      "instructions": "detailed description",
      "templateType": {
        "id": 1,
        "name": "Quality",
        "permittedAttributes": [
          "id"
        ]
      },
      "status": {
        "id": 4,
        "name": "Completed",
        "urgency": 0,
        "permittedAttributes": [
          "id"
        ]
      },
      "signaturesStatus": "None",
      "assignees": [
        {
          "id": 13200,
          "assigneeId": "93TNJUDDTJXL",
          "name": "John Doe",
          "type": {
            "id": 1,
            "name": "User",
            "permittedAttributes": [
              "id"
            ]
          },
          "permittedAttributes": [
            "assigneeId",
            "name",
            "type"
          ]
        }
      ],
      "progress": 0,
      "completedItemsCount": 0,
      "permittedActions": [
        "canArchive",
        "canEdit"
      ],
      "permittedAttributes": [
        "title",
        "location",
        "scheduledDate",
        "sections",
        "assignees",
        "status"
      ],
      "allowSectionAssignee": true,
      "signatures": [
        {
          "urn": "urn:adsk.checklists.cs.instance.signature:efca79bd-3865-4e68-88d5-30d982175c7d/41",
          "instanceRevision": "fesd3",
          "instanceId": 11453,
          "index": 11,
          "requiredBy": "IKEA",
          "isRequired": true,
          "definedAt": "Template",
          "requiredName": "Carlos",
          "requiredCompany": "IKEA",
          "isSigned": true,
          "formalSignature": {
            "instanceSignedRevision": "fesd6",
            "signedName": "Rodrigo",
            "signedCompany": "IKEA",
            "signedAt": "2018-05-23T08:18:55.098Z",
            "graphic": {
              "type": "SVG",
              "content": "<svg> .... </svg>",
              "permittedAttributes": [
                "content",
                "type"
              ]
            },
            "permittedAttributes": [
              "instanceSignedRevision",
              "signedName",
              "signedCompany",
              "signedAt",
              "graphic"
            ]
          },
          "updatedAt": "2018-05-23T08:18:55.098Z",
          "createdAt": "2018-05-23T08:18:55.098Z",
          "deletedAt": "2018-05-23T08:18:55.098Z",
          "submittedBy": "1QAZ2WSX",
          "permittedAttributes": [
            "requiredName",
            "requiredCompany",
            "correlationId"
          ],
          "permittedActions": [
            "canEdit"
          ]
        }
      ]
    },
    "relationships": {
      "sections": {
        "links": {
          "self": "",
          "related": ""
        },
        "meta": {},
        "data": [
          {
            "type": "instance_sections",
            "id": "1"
          }
        ]
      },
      "container": {
        "links": {
          "self": "",
          "related": ""
        },
        "meta": {},
        "data": {
          "type": "containers",
          "id": "efca79bd-3865-4e68-88d5-30d982175c7d"
        }
      },
      "createdFrom": {
        "links": {
          "self": "",
          "related": ""
        },
        "meta": {},
        "data": {
          "type": "templates",
          "id": "66"
        }
      }
    },
    "meta": {
      "totalItems": 1,
      "totalSections": 1,
      "totalRequiredSignatures": 3,
      "totalSignedSignatures": 1,
      "totalUnsignedSignatures": 2
    },
    "links": {
      "self": "",
      "related": ""
    }
  },
  "included": [
    {
      "id": "1",
      "type": "instance_sections",
      "attributes": {
        "urn": "urn:adsk.checklists.cs.instance.section:efca79bd-3865-4e68-88d5-30d982175c7d/1",
        "templateSectionId": 55,
        "modifiedBy": "1Qaz2wsX",
        "updatedAt": "2018-05-23T08:18:55.098Z",
        "status": "Not Completed",
        "title": "Inspection",
        "number": 1,
        "index": 1,
        "sectionNumbering": {
          "id": 1,
          "name": "Numeric",
          "permittedAttributes": [
            "id"
          ]
        },
        "itemsNumbering": {
          "id": 1,
          "name": "Numeric",
          "permittedAttributes": [
            "id"
          ]
        },
        "assignees": [
          {
            "id": 13200,
            "assigneeId": "93TNJUDDTJXL",
            "type": {
              "id": 1,
              "permittedAttributes": [
                "id"
              ]
            },
            "permittedAttributes": [
              "assigneeId",
              "type"
            ]
          }
        ],
        "permittedActions": [
          "canEdit"
        ],
        "permittedAttributes": [
          "items",
          "assignees",
          "status"
        ],
        "sectionSignatures": [
          {
            "id": "a3126196-2904-443b-ac90-075929ab00f3",
            "urn": "urn:adsk.checklists.cs.item.signature:050b690c-7e79-409a-8e5c-4f3ad46532f7/a3126196-2904-443b-ac90-075929ab00f3",
            "ossUrn": "urn:adsk.objects:os.object:checklists.prod.us/a3126196-2904-443b-ac90-075929ab00f3",
            "instanceSectionId": 3037806,
            "index": 2,
            "requiredBy": "",
            "isRequired": true,
            "signedName": "Abhishek",
            "signedCompany": "Autodesk",
            "submittedBy": "NLA9LL7CPK4X",
            "signedAt": "2021-05-26T17:15:50.475Z",
            "createdAt": "2021-04-16T11:27:09.130Z",
            "updatedAt": "2021-04-16T11:27:09.130Z",
            "deletedAt": "2021-05-27T17:15:50.475Z",
            "instructions": "",
            "uploadStatus": "Completed"
          }
        ]
      },
      "relationships": {
        "items": {
          "links": {
            "self": "string",
            "related": "string"
          },
          "meta": {},
          "data": [
            {
              "type": "instance_items",
              "id": "601501"
            }
          ]
        }
      },
      "links": {
        "self": "string",
        "related": "string"
      },
      "meta": {}
    },
    {
      "id": "601501",
      "type": "instance_items",
      "attributes": {
        "urn": "urn:adsk.checklists.cs.instance.item:efca79bd-3865-4e68-88d5-30d982175c7d/601501",
        "templateItemId": 111,
        "value": "string",
        "answer": [
          "033dfcec-6531-4663-91c6-f7c78c6db537",
          "bd03a9db-54db-48da-b865-2eb3af9460d2"
        ],
        "title": "Painting Technique",
        "responseType": {
          "id": 7,
          "name": "list_multiple",
          "metadata": {
            "listResponse": {
              "id": "d17c647b-6555-4641-bf8c-35ee07cfa08d",
              "possibleAnswers": [
                {
                  "id": "033dfcec-6531-4663-91c6-f7c78c6db537",
                  "index": 0,
                  "value": "Spray",
                  "conformanceType": 1
                },
                {
                  "id": "bd03a9db-54db-48da-b865-2eb3af9460d2",
                  "index": 1,
                  "value": "Roller",
                  "conformanceType": 2
                },
                {
                  "id": "5be1e5ab-ac90-4e29-935d-89bfa04f61e6",
                  "index": 2,
                  "value": "Brush",
                  "conformanceType": 1
                }
              ]
            }
          },
          "permittedAttributes": [
            "id"
          ]
        },
        "isRequired": true,
        "modifiedBy": "1Qaz2wsX",
        "updatedAt": "2018-05-23T08:18:55.098Z",
        "index": 1,
        "itemId": 1,
        "itemVersionId": 1,
        "number": 1,
        "sectionNumbering": {
          "id": 1,
          "name": "Numeric",
          "permittedAttributes": [
            "id"
          ]
        },
        "itemsNumbering": {
          "id": 1,
          "name": "Numeric",
          "permittedAttributes": [
            "id"
          ]
        },
        "permittedActions": [
          "canEdit"
        ],
        "permittedAttributes": [
          "value",
          "note",
          "attachments",
          "answer"
        ],
        "note": {
          "content": "string"
        }
      },
      "relationships": {
        "attachments": {
          "links": {
            "self": "string",
            "related": "string"
          },
          "meta": {},
          "data": [
            {
              "type": "instance_item_attachments",
              "id": "89d298ef-1a51-4fe8-8592-30d1d56c2704"
            }
          ]
        }
      },
      "links": {
        "self": "string",
        "related": "string"
      },
      "meta": {}
    },
    {
      "id": "89d298ef-1a51-4fe8-8592-30d1d56c2704",
      "type": "instance_item_attachments",
      "attributes": {
        "name": "f7330310-64af-11e8-a9b1-49ecc6364378",
        "attachmentType": "OSS",
        "mimeType": "image/jpeg",
        "uploadStatus": "COMPLETED",
        "urns": [
          {
            "urn": "urn:adsk.wipprod:fs.file:vf.iW3Jgz4BROu8v_N6oD1BsQ?version=1",
            "type": "WIP"
          },
          {
            "urn": "urn:adsk.objects:os.object:wip.dm.prod/cdca6e9b-d20c-4fc5-ad5c-46e3f25fd1f1",
            "type": "OSS"
          },
          {
            "urn": "urn:adsk.checklists.cs.attachment:efca79bd-3865-4e68-88d5-30d982175c7d/89d298ef-1a51-4fe8-8592-30d1d56c2704",
            "type": "CHECKLIST"
          }
        ],
        "createdAt": "2018-05-23T08:18:55.098Z",
        "updatedAt": "2018-05-23T08:18:55.098Z",
        "modifiedBy": "1Qaz2wsX",
        "createdBy": "1Qaz2wsX",
        "permittedActions": [
          "canArchive",
          "canEdit"
        ],
        "permittedAttributes": [
          "mimeType",
          "uploadStatus"
        ]
      },
      "relationships": {
        "container": {
          "links": {
            "self": "string",
            "related": "string"
          },
          "meta": {},
          "data": {
            "type": "containers",
            "id": "efca79bd-3865-4e68-88d5-30d982175c7d"
          }
        },
        "item": {
          "links": {
            "self": "string",
            "related": "string"
          },
          "meta": {},
          "data": [
            {
              "type": "instance_items",
              "id": "601501"
            }
          ]
        }
      },
      "links": {
        "self": "string",
        "related": "string"
      },
      "meta": {}
    }
  ]
}


Documentation /BIM 360 API /API Reference
Templates
GET	containers/{containerId}/templates
Retrieves information about all the BIM 360 Field Management templates in a project, including details about the items, sections, and attachments in the template. To get information about a single template, see GET templates/:id.

Filtering

You can configure the response payload by setting up filter, pagination and sorting parameters. You can also specify which types of data appear in the response.

Filtering follows one of the following formats:

param[<fieldName>]=<matchValue>
param=<matchValue>
New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is not compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/checklists/v1/containers/{containerId}/templates
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
containerId
string
Each project is assigned a container that stores all the checklists for the project. To find the ID, see the Retrieve a Container ID tutorial.
Request
Query String Parameters
sort
enum:string
Sort the template by title or templateType.name or templateTypeName. For example, sort=title. Separate multiple values with commas. To sort in descending order add a - before the sort criteria. For example, sort=-title. For more details, see JSON API Sorting. Possible values: templateType.name, title
filter[templateTypeId]
number
Retrieves templates associated with the specified type. For example, filter[templateTypeId]=1 or queryFilter[templateTypeId]=1. Possible values: 1 (quality), 6 (punch List), 11 (safety), 15 (commissioning). Separate multiple values with commas. For more details, see JSON API Filtering.
limit
number
The number of templates to return in the response payload. Default value: 50. For example, to limit the response to two templates per page, use page[limit]=2 or limit=2. For more details, see JSON API Paging.
page[offset]
number
matchValue is the page number that you want to begin templates results from; for example, page[offset]=50 or offset=50. For more details, see JSON API Paging.
fields[templates]
string
Specify which attributes you want to appear in the response. Separate multiple values with commas. For example, fields[templates] = createdAt, templateType. For more details, see JSON API Sparse Fieldsets.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request header
403
Forbidden
The request has not been applied because it lacks valid authentication credentials for the target resource
410
Forbidden
500
Internal Server Error
An unexpected error occurred on the server
Response
Body Structure (200)
 Expand all
jsonapi
object
The JSON API object.
meta
object
The meta object.
links
object
link for navigation when pagination is possible
data
array: object
The data object.
Example
Success

Request
curl -v 'https://developer.api.autodesk.com/bim360/checklists/v1/containers/efca79bd-3865-4e68-88d5-30d982175c7d/templates?sort=title&filter[templateTypeId]=1&limit=10' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "meta": {
    "offset": 0,
    "limit": 50,
    "total": 210
  },
  "links": {
    "self": "/containers/efca79bd-3865-4e68-88d5-30d982175c7d/templates?page[offset]=50",
    "first": "/containers/efca79bd-3865-4e68-88d5-30d982175c7d/templates?page[offset]=0",
    "last": "/containers/efca79bd-3865-4e68-88d5-30d982175c7d/templates?page[offset]=200",
    "next": "/containers/efca79bd-3865-4e68-88d5-30d982175c7d/templates?page[offset]=100",
    "prev": "/containers/efca79bd-3865-4e68-88d5-30d982175c7d/templates?page[offset]=0"
  },
  "data": [
    {
      "id": "11453",
      "type": "templates",
      "attributes": {
        "title": "Painting Template",
        "trades": [],
        "versionId": "1",
        "createdBy": "1Qaz2wsX",
        "updatedAt": "2018-05-23T08:18:55.098Z",
        "createdAt": "2018-05-23T08:18:55.098Z",
        "instructions": "detailed description",
        "templateType": {
          "id": 1,
          "name": "Quality",
          "permittedAttributes": [
            "id"
          ]
        },
        "allowSectionAssignee": false,
        "permittedActions": [
          "canArchive",
          "canEdit",
          "canCreateChecklist"
        ],
        "permittedAttributes": [
          "title",
          "instruction",
          "templateType",
          "sections"
        ],
        "signatures": [
          {
            "index": 0,
            "isRequired": true,
            "requiredBy": "IKEA"
          }
        ]
      },
      "relationships": {
        "container": {
          "links": {
            "self": "",
            "related": ""
          },
          "meta": {},
          "data": {
            "type": "containers",
            "id": "efca79bd-3865-4e68-88d5-30d982175c7d"
          }
        }
      },
      "links": {
        "self": "",
        "related": ""
      },
      "meta": {
        "totalItems": "",
        "totalSections": "",
        "totalInstances": ""
      }
    }
  ]
}

Documentation /BIM 360 API /API Reference
Templates
GET	containers/{containerId}/templates/{id}
Retrieves information about a specific BIM 360 Field Management template, including details about the items, sections, and attachments in the template. To get information about all the templates in the project, see GET templates.

New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is not compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/checklists/v1/containers/{containerId}/templates/{id}
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
containerId
string
Each project is assigned a container that stores all the checklists for the project. To find the ID, see the Retrieve a Container ID tutorial.
id
string
The ID of the checklist.
Request
Query String Parameters
fields[templates]
string
Specify which attributes you want to appear in the response. Separate multiple values with commas. For example, fields[templates] = createdAt, templateType. For more details, see JSON API Sparse Fieldsets.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request header
403
Forbidden
The request has not been applied because it lacks valid authentication credentials for the target resource
404
Not Found
The resource cannot be found
410
Forbidden
500
Internal Server Error
An unexpected error occurred on the server
Response
Body Structure (200)
 Expand all
jsonapi
object
The JSON API object.
meta
object
The meta object.
links
object
The links object.
data
object
The data object.
Example
Success

Request
curl -v 'https://developer.api.autodesk.com/bim360/checklists/v1/containers/efca79bd-3865-4e68-88d5-30d982175c7d/templates/11453' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "meta": {},
  "links": {
    "self": "",
    "related": ""
  },
  "data": {
    "id": "11453",
    "type": "templates",
    "attributes": {
      "title": "Painting Template",
      "trades": [],
      "versionId": "1",
      "createdBy": "1Qaz2wsX",
      "updatedAt": "2018-05-23T08:18:55.098Z",
      "createdAt": "2018-05-23T08:18:55.098Z",
      "instructions": "detailed description",
      "templateType": {
        "id": 1,
        "name": "Quality",
        "permittedAttributes": [
          "id"
        ]
      },
      "signatures": [
        {
          "index": 0,
          "isRequired": true,
          "requiredBy": "IKEA"
        }
      ],
      "sections": [
        {
          "id": 1,
          "title": "Inspection",
          "number": 1,
          "index": 1,
          "instructions": "A detailed description.",
          "sectionNumbering": {
            "id": 1,
            "name": "Numeric",
            "permittedAttributes": [
              "id"
            ]
          },
          "itemsNumbering": {
            "id": 1,
            "name": "Numeric",
            "permittedAttributes": [
              "id"
            ]
          },
          "items": [
            {
              "id": 1,
              "itemId": 18,
              "itemVersionId": 2,
              "number": 1,
              "index": 1,
              "isRequired": true,
              "title": "Painting Technique",
              "instructions": [
                {
                  "id": 11,
                  "data": "A description of an item.",
                  "permittedAttributes": [
                    "data",
                    "type"
                  ],
                  "type": {
                    "id": 1,
                    "name": "text",
                    "permittedAttributes": [
                      "id"
                    ]
                  }
                }
              ],
              "responseType": {
                "id": 7,
                "name": "list_multiple",
                "metadata": {
                  "listResponse": {
                    "id": "d17c647b-6555-4641-bf8c-35ee07cfa08d",
                    "possibleAnswers": [
                      {
                        "id": "b092a299-906c-489f-bd06-f53c898bae7c",
                        "index": 0,
                        "value": "Roller",
                        "conformanceType": 1
                      }
                    ]
                  }
                },
                "permittedAttributes": [
                  "id"
                ]
              },
              "supplementalAttachments": [
                {
                  "id": "89d298ef-1a51-4fe8-8592-30d1d56c2704",
                  "lineageUrn": "urn:adsk.wipqa:dm.lineage:kWOX5QRIaeStefBEuQNf3GBw",
                  "permittedAttributes": [
                    [
                      "lineageUrn"
                    ]
                  ]
                }
              ],
              "permittedAttributes": [
                [
                  "itemId",
                  "number",
                  "index",
                  "isRequired",
                  "supplementalAttachments"
                ]
              ]
            }
          ],
          "permittedAttributes": [
            "number",
            "title",
            "instructions",
            "index",
            "sectionNumbering",
            "items",
            "itemNumbering"
          ]
        }
      ],
      "allowSectionAssignee": false,
      "permittedActions": [
        "canArchive",
        "canEdit",
        "canCreateChecklist"
      ],
      "permittedAttributes": [
        "title",
        "instruction",
        "templateType",
        "sections"
      ]
    },
    "relationships": {
      "container": {
        "links": {
          "self": "",
          "related": ""
        },
        "meta": {},
        "data": {
          "type": "containers",
          "id": "efca79bd-3865-4e68-88d5-30d982175c7d"
        }
      }
    },
    "links": {
      "self": "",
      "related": ""
    },
    "meta": {
      "totalItems": "",
      "totalSections": "",
      "totalInstances": ""
    }
  }
}

以下是DATA CONNECTOR API :
Documentation /BIM 360 API /API Reference
Requests
GET	accounts/{accountId}/requests
Returns an array of data requests that the authenticated user has created in the specified account. The user must have executive overview or project administrator permissions.

Returned information for each request in the array includes the request ID, information about when the request was created, the attribute values defined by the request, and when the last and next job spawned by the request has occurred and will occur.

To understand the basics of requests, the jobs they spawn, and the data extracts returned by the jobs, see the Data Connector API Field Guide.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data-connector/v1/accounts/:accountId/requests
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
accountId
string: UUID
The account ID. You can derive it from your hub ID if necessary: Use GET hubs in the Data Management API to retrieve your hub ID. Remove the initial “b.” from the hub ID to get your account ID.
Request
Query String Parameters
sort
string
The sort order of returned data connector objects. Possible values: asc ascending by date (earliest to latest date), desc descending by date (latest to earliest date).
limit
int
The number of data connector objects to return. Default value: 20
offset
int
The number of data objects to skip before starting to starting to collect the result set. Default value: 0
sortFields
string
A string of comma-separated names of the fields by which to sort the returned data requests. The results are sorted by the first field, then by the second field, and so on. Requests are sorted by each field in ascending order by default; you can prepend any field name with a hyphen ( - ) to sort in descending order. Invalid fields and whitespaces are ignored.
Possible values: isActive, accountId, createdBy, createdByEmail, createdAt, updatedBy, updatedAt, scheduleInterval, reoccuringInterval, effectiveFrom, effectiveTo, startDate, endDate.

filter[field_to_filter]
string
Return only the data requests in which the specified field has the specified value. Use the following format in the endpoint URL: filter[field_to_filter]=_filter_value_.
Note that you can provide multiple request filters in the URL, but you may not filter on multiple values of the same field.

Possible field_to_filter values: projectId, createdAt, updatedAt, scheduleInterval, reocurringInterval, effectiveFrom, effectiveTo, isActive, startDate, endDate. You can also retrieve all data requests in the current account by specifying filter[projectId]=null.

For the createdAt and updatedAt fields (which accept a date range), specify the range in the form firstdate..lastdate, in ISO 8601 format with the time required. You can alternatively omit the first date (for example, to get everything on or before June 1, 2019 the range would be ..2019-06-01T23:59:59.999Z). You can also omit the last date (for example, to get everything after June 1, 2019 the range would be 2019-06-01T00:00:00.000Z..)

Additional notes on using startDate and endDate:

If you provide only startDate or endDate (but not both), Data Connector uses that single date for both startDate and endDate.
If you request more than the Maximum Date Range Allowed for an extraction, the default date range as documented in the schema documentation is returned.
For the activities service group, data replication can be delayed up to 20 minutes, so your requests should account for that delay.
Response
HTTP Status Code Summary
200
OK
Successfully retrieved an array of data requests.
400
Bad Request
The parameters are invalid.
401
Unauthorized
The provided bearer token is invalid.
403
Forbidden
Forbidden. The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The resource or endpoint cannot be found.
429
Too Many Requests
Rate limited exceeded; wait some time before retrying.
500
Internal Server Error
An unexpected error occurred on the server.
503
Service Unavailable
Service unavailable.
Response
Body Structure (200)
 Expand all
pagination
object
Information about the pagination used to return the results array.
results
array: object
The returned array of data request records.
Example
Successfully retrieved an array of data requests.

Request
curl -v 'https://developer.api.autodesk.com/data-connector/v1/accounts/:accountId/requests?sort=asc&limit=20&offset=0&sortFields=createdByEmail,-createdAt&filter[field_to_filter]=_filter_value_' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 20,
    "offset": 0,
    "totalResults": 100
  },
  "results": [
    {
      "id": "ce9bc188-1e18-11eb-adc1-0242ac120002",
      "description": "My Company Data Extract",
      "isActive": true,
      "accountId": "f9abf4c8-1f51-4b26-a6b7-6ac0639cb138",
      "projectId": null,
      "projectIdList": "[ \"ffffffff-1f51-4b26-a6b7-6ac0639cb138\", \"aaaaaaaa-1f51-4b26-a6b7-6ac0639cb138\" ]",
      "createdBy": "ABCDEFGHI",
      "createdByEmail": "joe.user@mycompany.com",
      "createdAt": "2020-11-06T19:09:40.106Z",
      "updatedBy": "ABCDEFGHI",
      "updatedAt": "2020-11-06T19:09:40.106Z",
      "scheduleInterval": "ONE_TIME",
      "reoccuringInterval": null,
      "effectiveFrom": "2020-11-06T19:09:40.106Z",
      "effectiveTo": "2020-11-12T19:09:40.106Z",
      "lastQueuedAt": null,
      "serviceGroups": [
        "admin",
        "issues"
      ],
      "callbackUrl": "https://api.mycompany.com/autodesk/jobinfo",
      "sendEmail": true,
      "startDate": "2023-06-06T00:00:00.000Z",
      "endDate": "2023-06-06T12:00:00.000Z",
      "dateRange": "LAST_MONTH",
      "projectStatus": "active"
    }
  ]
}

Documentation /BIM 360 API /API Reference
Requests
POST	accounts/{accountId}/requests
Creates a data request for an authenticated user. The user can optionally limit the request to one project. The user must have executive overview or project administrator permissions.

As a successfully created data request spawns jobs, those jobs will send status email to the data request creator when completed. If the data request contains a callback URL, jobs will also call that URL when completed. Data Connector requests and their resulting jobs are subject to rate limits: an account can create a maximum of 24 jobs within a 24-hour period, and an individual user can create up to 24 jobs within the same timeframe. For more details, see the Rate Limits page.

To understand the basics of requests, the jobs they spawn, and the data extracts returned by the jobs, see the Data Connector API Field Guide.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/data-connector/v1/accounts/:accountId/requests
Authentication Context	
user context required
Required OAuth Scopes	
data:create
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
* Required
Request
URI Parameters
accountId
string: UUID
The account ID. You can derive it from your hub ID if necessary: Use GET hubs in the Data Management API to retrieve your hub ID. Remove the initial “b.” from the hub ID to get your account ID.
Request
Body Structure
description
string
The user-entered description of this data request.
isActive
boolean
The data request’s active/inactive status. Possible values: true the request is active; false the request is inactive. If not supplied, the default value is true.
scheduleInterval
string
The scheduling interval unit for jobs spawned by this data request. This value is multiplied by the reoccurringInterval attribute to specify the length of the recurring interval at which jobs run. Possible values:
ONE_TIME: Run the job only once
DAY: Set the recurring job interval in days
WEEK: Set the recurring job interval in weeks
MONTH: Set the recurring job interval in months
YEAR: Set the recurring job interval in years
Note that recurring jobs start at the day and time when the request first spawns a job. This may be at the date and time specified in the attribute effectiveFrom.

reoccuringInterval
int
The number of scheduleInterval units to wait between job execution for the request. For example, a scheduleInterval value of WEEK and a reoccuringInterval value of 2 means the job will run every two weeks.
This value is required and must be a non-zero integer for all values of scheduleInterval except for a scheduleInterval value of ONE_TIME, in which case this value is ignored.

effectiveFrom
datetime: ISO 8601
The date and time when a one-time job execution or a recurring interval schedule begins, presented in ISO 8601 format. If the date and time is before the current time, execution of scheduling begins immediately. This value is required.
effectiveTo
datetime: ISO 8601
The date and time when the recurring interval schedule ends, presented in ISO 8601 format. This value must not be supplied for scheduleInterval values of ONE_TIME, but is required for all other scheduleInterval values.
serviceGroups
array: string
The service groups from which to extract data, separated by commas. This required value must identify at least one service group.
Possible values: all, activities, admin, assets, checklists, cost, dailylogs, forms, iq, issues, locations, markups, meetingminutes, photos, relationships, reviews, rfis, schedule, sheets, submittals, submittalsacc, transmittals.

Note that the admin service includes both project and account admin, and all produces an extract containing all currently available service groups.

callbackUrl
string
The callback URL specified for the data request. If specified, the Data Connection service calls the URL each time a job executes for the request. The service sends a POST request that provides job execution information. The JSON payload in the POST request contains the following: { "accountId": "account_id", "requestId": "request_id", "jobId": "data_connector_job_id", "state": "complete", "success": true or false }.
If not specified, the Data Connection service does not provide a callback.

sendEmail
boolean
Send a notification email to the user upon job completion. Values: true or false (default is true)
projectId
string
(Legacy): A single project ID for the data request. Superseded by projectIdList.
projectIdList
array: string
A list of up to 50 project IDs for the data request, which can include a single project or multiple projects. If projectId is also included, projectIdList takes precedence. Required for users with project admin permissions. Optional for users with executive overview permissions, who by default receive data for all projects unless projectIdList is provided.
startDate
string
The start date and time for the data extraction, in ISO 8601 format.
This field applies only to schemas supporting date range extraction. The detailed schema documentation delivered with each data extract identifies the schemas and tables that support date range extraction.

Additional notes on using startDate and endDate:

If you provide only startDate or endDate (but not both), Data Connector uses that single date for both startDate and endDate.
If you request more than the Maximum Date Range Allowed for an extraction, the default date range as documented in the schema documentation is returned.
For the activities service group, data replication can be delayed up to 20 minutes, so your requests should account for that delay.
endDate
string
The end date and time for the data extraction, in ISO 8601 format.
This field applies only to schemas supporting date range extraction. The detailed schema documentation delivered with each data extract identifies the schemas and tables that support date range extraction.

Additional notes on using startDate and endDate:

If you provide only startDate or endDate (but not both), Data Connector uses that single date for both startDate and endDate.
If you request more than the Maximum Date Range Allowed for an extraction, the default date range as documented in the schema documentation is returned.
For the activities service group, data replication can be delayed up to 20 minutes, so your requests should account for that delay.
dateRange
string
Specifies the timeframe for extracting data in a scheduled request (DAY, WEEK, MONTH, YEAR). Currently, it is applicable only to the Activities service. Possible values:
TODAY: The current calendar day, from 00:00 UTC to the time the request is made.
YESTERDAY: The entire previous calendar day (00:00 UTC to 23:59 UTC).
PAST_7_DAYS: The last 7 days, including the current day.
MONTH_TO_DATE: From the start of the current calendar month (00:00 UTC on the 1st) to the time the request is made.
LAST_MONTH: The entire previous calendar month (00:00 UTC on the 1st to 23:59 UTC on the last day).
projectStatus
string
The types of projects to be included in a request. The possible values are:
all: - all projects (default)
archived: archived projects only
active: active project only
Response
HTTP Status Code Summary
201
Created
Successfully created a data request that is described in the response.
400
Bad Request
The parameters are invalid.
401
Unauthorized
The provided bearer token is invalid.
403
Forbidden
Forbidden. The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The resource or endpoint cannot be found.
429
Too Many Requests
Rate limited exceeded; wait some time before retrying.
500
Internal Server Error
An unexpected error occurred on the server.
503
Service Unavailable
Service unavailable.
Response
Body Structure (201)
id
string: UUID
The ID of the data request.
description
string
The user-entered description of this data request. If not supplied, the default value is a null string.
isActive
boolean
The data request’s active/inactive status. Possible values: true the request is active; false the request is inactive.
accountId
string: UUID
The account ID.
projectId
string: UUID
(Legacy): A single project ID for the data request. Superseded by projectIdList.
projectIdList
array: string
A list of up to 50 project IDs included in the data request. This field contains the project IDs for which data is being extracted. If both projectId and projectIdList were included in the request, this field contains the values from projectIdList.
createdBy
string
The BIM 360 / ACC user ID of the user who created the data request.
createdByEmail
string
The email address of the user who created the data request.
createdAt
datetime: ISO 8601
The date and time the data request was created, presented in ISO 8601 format.
updatedBy
string
The BIM 360 / ACC user ID of the user who last updated the data request.
updatedAt
datetime: ISO 8601
The date and time the data request was last updated, presented in ISO 8601 format.
scheduleInterval
string
The scheduling interval unit for jobs spawned by this data request. This value is multiplied by the reoccurringInterval attribute to specify the length of the recurring interval at which jobs run. Possible values:
ONE_TIME: Run the job only once
DAY: Set the recurring job interval in days
WEEK: Set the recurring job interval in weeks
MONTH: Set the recurring job interval in months
YEAR: Set the recurring job interval in years
reoccuringInterval
int
The number of scheduleInterval units to wait between job execution for the request. For example, a scheduleInterval value of WEEK and a reoccuringInterval value of 2 means the job will run every two weeks.
effectiveFrom
datetime: ISO 8601
The date and time when a one-time job execution or a recurring interval schedule begins, presented in ISO 8601 format.
effectiveTo
datetime: ISO 8601
The date and time when the recurring interval schedule ends, presented in ISO 8601 format.
lastQueuedAt
datetime: ISO 8601
The date and time the last job for this data request was scheduled to execute, presented in ISO 8601 format.
serviceGroups
array: string
The service groups from which data has been extracted, separated by commas.
Possible values: all, activities, admin, assets, checklists, cost, dailylogs, forms, iq, issues, locations, markups, meetingminutes, photos, relationships, reviews, rfis, schedule, sheets, submittals, submittalsacc, transmittals.

Note that the admin service includes both project and account admin, and all indicates that the extract contains all currently available service groups.

callbackUrl
string
The callback URL specified for the data request. If specified, the Data Connection service calls the URL each time a job executes for the request. The service sends a POST request that provides job execution information. The JSON payload in the POST request contains the following: { "accountId": "account_id", "requestId": "request_id", "jobId": "data_connector_job_id", "state": "complete", "success": true or false }.
sendEmail
boolean
Send a notification email to the user upon job completion. Values: true or false (default is true)
startDate
string
The start date and time for the data extraction, in ISO 8601 format.
This field applies only to schemas supporting date range extraction. The detailed schema documentation delivered with each data extract identifies the schemas and tables that support date range extraction.

Additional notes on using startDate and endDate:

If you provide only startDate or endDate (but not both), Data Connector uses that single date for both startDate and endDate.
If you request more than the Maximum Date Range Allowed for an extraction, the default date range as documented in the schema documentation is returned.
For the activities service group, data replication can be delayed up to 20 minutes, so your requests should account for that delay.
endDate
string
The end date and time for the data extraction, in ISO 8601 format.
This field applies only to schemas supporting date range extraction. The detailed schema documentation delivered with each data extract identifies the schemas and tables that support date range extraction.

Additional notes on using startDate and endDate:

If you provide only startDate or endDate (but not both), Data Connector uses that single date for both startDate and endDate.
If you request more than the Maximum Date Range Allowed for an extraction, the default date range as documented in the schema documentation is returned.
For the activities service group, data replication can be delayed up to 20 minutes, so your requests should account for that delay.
dateRange
string
The timeframe used for extracting data in the request. Currently, it is applicable only to the Activities service. This field contains the value specified in the request, indicating the range of data included in the response. Possible values:
TODAY: Data for the current day (from 00:00 UTC to the time the request was made).
YESTERDAY: Data for the previous calendar day (from 00:00 UTC to 23:59 UTC).
PAST_7_DAYS: Data for the last 7 days, including the current day.
MONTH_TO_DATE: Data from the start of the current calendar month (00:00 UTC on the 1st) to the time the request was made.
LAST_MONTH: Data for the entire previous calendar month (00:00 UTC on the 1st to 23:59 UTC on the last day).
projectStatus
string
The types of projects to be included in a request. The possible values are:
all: - all projects (default)
archived: archived projects only
active: active project only
Example
Successfully created a data request that is described in the response.

Request
curl -v 'https://developer.api.autodesk.com/data-connector/v1/accounts/:accountId/requests' \
  -X 'POST' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a' \
  -H 'Content-Type: application/json' \
  -d '{
        "description": "My Company Data Extract",
        "isActive": true,
        "scheduleInterval": "ONE_TIME",
        "reoccuringInterval": null,
        "effectiveFrom": "2020-11-06T19:09:40.106Z",
        "effectiveTo": "2020-11-12T19:09:40.106Z",
        "serviceGroups": [
          "admin",
          "issues"
        ],
        "callbackUrl": "https://api.mycompany.com/autodesk/jobinfo",
        "sendEmail": true,
        "projectId": null,
        "projectIdList": "[ \"ffffffff-1f51-4b26-a6b7-6ac0639cb138\", \"aaaaaaaa-1f51-4b26-a6b7-6ac0639cb138\" ]",
        "startDate": "2023-06-06T00:00:00.000Z",
        "endDate": "2023-06-06T12:00:00.000Z",
        "dateRange": "LAST_MONTH",
        "projectStatus": "active"
      }'
Show Less
Response
{
  "id": "ce9bc188-1e18-11eb-adc1-0242ac120002",
  "description": "My Company Data Extract",
  "isActive": true,
  "accountId": "f9abf4c8-1f51-4b26-a6b7-6ac0639cb138",
  "projectId": null,
  "projectIdList": "[ \"ffffffff-1f51-4b26-a6b7-6ac0639cb138\", \"aaaaaaaa-1f51-4b26-a6b7-6ac0639cb138\" ]",
  "createdBy": "ABCDEFGHI",
  "createdByEmail": "joe.user@mycompany.com",
  "createdAt": "2020-11-06T19:09:40.106Z",
  "updatedBy": "ABCDEFGHI",
  "updatedAt": "2020-11-06T19:09:40.106Z",
  "scheduleInterval": "ONE_TIME",
  "reoccuringInterval": null,
  "effectiveFrom": "2020-11-06T19:09:40.106Z",
  "effectiveTo": "2020-11-12T19:09:40.106Z",
  "lastQueuedAt": null,
  "serviceGroups": [
    "admin",
    "issues"
  ],
  "callbackUrl": "https://api.mycompany.com/autodesk/jobinfo",
  "sendEmail": true,
  "startDate": "2023-06-06T00:00:00.000Z",
  "endDate": "2023-06-06T12:00:00.000Z",
  "dateRange": "LAST_MONTH",
  "projectStatus": "active"
}

Documentation /BIM 360 API /API Reference
Requests
GET	accounts/{accountId}/requests/{requestId}
Returns information about a specified data request created earlier by the authenticated user. Note that the user must have executive overview or project administrator permissions.

Returned information includes the request ID, information about when the request was created, the attribute values defined by the request, and when the last and next job spawned by the request has occurred and will occur.

To get request IDs for your requests, use GET requests.

To understand the basics of requests, the jobs they spawn, and the data extracts returned by the jobs, see the Data Connector API Field Guide.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data-connector/v1/accounts/:accountId/requests/:requestId
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
accountId
string: UUID
The account ID. You can derive it from your hub ID if necessary: Use GET hubs in the Data Management API to retrieve your hub ID. Remove the initial “b.” from the hub ID to get your account ID.
requestId
string: UUID
The ID of the specified request
Response
HTTP Status Code Summary
200
OK
Successfully returned a data request.
400
Bad Request
The parameters are invalid.
401
Unauthorized
The provided bearer token is invalid.
403
Forbidden
Forbidden. The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The resource or endpoint cannot be found.
429
Too Many Requests
Rate limited exceeded; wait some time before retrying.
500
Internal Server Error
An unexpected error occurred on the server.
503
Service Unavailable
Service unavailable.
Response
Body Structure (200)
id
string: UUID
The ID of the data request.
description
string
The user-entered description of this data request. If not supplied, the default value is a null string.
isActive
boolean
The data request’s active/inactive status. Possible values: true the request is active; false the request is inactive.
accountId
string: UUID
The account ID.
projectId
string: UUID
(Legacy): A single project ID for the data request. Superseded by projectIdList.
projectIdList
array: string
A list of up to 50 project IDs included in the data request. This field contains the project IDs for which data is being extracted. If both projectId and projectIdList were included in the request, this field contains the values from projectIdList.
createdBy
string
The BIM 360 / ACC user ID of the user who created the data request.
createdByEmail
string
The email address of the user who created the data request.
createdAt
datetime: ISO 8601
The date and time the data request was created, presented in ISO 8601 format.
updatedBy
string
The BIM 360 / ACC user ID of the user who last updated the data request.
updatedAt
datetime: ISO 8601
The date and time the data request was last updated, presented in ISO 8601 format.
scheduleInterval
string
The scheduling interval unit for jobs spawned by this data request. This value is multiplied by the reoccurringInterval attribute to specify the length of the recurring interval at which jobs run. Possible values:
ONE_TIME: Run the job only once
DAY: Set the recurring job interval in days
WEEK: Set the recurring job interval in weeks
MONTH: Set the recurring job interval in months
YEAR: Set the recurring job interval in years
reoccuringInterval
int
The number of scheduleInterval units to wait between job execution for the request. For example, a scheduleInterval value of WEEK and a reoccuringInterval value of 2 means the job will run every two weeks.
effectiveFrom
datetime: ISO 8601
The date and time when a one-time job execution or a recurring interval schedule begins, presented in ISO 8601 format.
effectiveTo
datetime: ISO 8601
The date and time when the recurring interval schedule ends, presented in ISO 8601 format.
lastQueuedAt
datetime: ISO 8601
The date and time the last job for this data request was scheduled to execute, presented in ISO 8601 format.
serviceGroups
array: string
The service groups from which data has been extracted, separated by commas.
Possible values: all, activities, admin, assets, checklists, cost, dailylogs, forms, iq, issues, locations, markups, meetingminutes, photos, relationships, reviews, rfis, schedule, sheets, submittals, submittalsacc, transmittals.

Note that the admin service includes both project and account admin, and all indicates that the extract contains all currently available service groups.

callbackUrl
string
The callback URL specified for the data request. If specified, the Data Connection service calls the URL each time a job executes for the request. The service sends a POST request that provides job execution information. The JSON payload in the POST request contains the following: { "accountId": "account_id", "requestId": "request_id", "jobId": "data_connector_job_id", "state": "complete", "success": true or false }.
sendEmail
boolean
Send a notification email to the user upon job completion. Values: true or false (default is true)
startDate
string
The start date and time for the data extraction, in ISO 8601 format.
This field applies only to schemas supporting date range extraction. The detailed schema documentation delivered with each data extract identifies the schemas and tables that support date range extraction.

Additional notes on using startDate and endDate:

If you provide only startDate or endDate (but not both), Data Connector uses that single date for both startDate and endDate.
If you request more than the Maximum Date Range Allowed for an extraction, the default date range as documented in the schema documentation is returned.
For the activities service group, data replication can be delayed up to 20 minutes, so your requests should account for that delay.
endDate
string
The end date and time for the data extraction, in ISO 8601 format.
This field applies only to schemas supporting date range extraction. The detailed schema documentation delivered with each data extract identifies the schemas and tables that support date range extraction.

Additional notes on using startDate and endDate:

If you provide only startDate or endDate (but not both), Data Connector uses that single date for both startDate and endDate.
If you request more than the Maximum Date Range Allowed for an extraction, the default date range as documented in the schema documentation is returned.
For the activities service group, data replication can be delayed up to 20 minutes, so your requests should account for that delay.
dateRange
string
The timeframe used for extracting data in the request. Currently, it is applicable only to the Activities service. This field contains the value specified in the request, indicating the range of data included in the response. Possible values:
TODAY: Data for the current day (from 00:00 UTC to the time the request was made).
YESTERDAY: Data for the previous calendar day (from 00:00 UTC to 23:59 UTC).
PAST_7_DAYS: Data for the last 7 days, including the current day.
MONTH_TO_DATE: Data from the start of the current calendar month (00:00 UTC on the 1st) to the time the request was made.
LAST_MONTH: Data for the entire previous calendar month (00:00 UTC on the 1st to 23:59 UTC on the last day).
projectStatus
string
The types of projects to be included in a request. The possible values are:
all: - all projects (default)
archived: archived projects only
active: active project only
Example
Successfully returned a data request.

Request
curl -v 'https://developer.api.autodesk.com/data-connector/v1/accounts/:accountId/requests/:requestId' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "id": "ce9bc188-1e18-11eb-adc1-0242ac120002",
  "description": "My Company Data Extract",
  "isActive": true,
  "accountId": "f9abf4c8-1f51-4b26-a6b7-6ac0639cb138",
  "projectId": null,
  "projectIdList": "[ \"ffffffff-1f51-4b26-a6b7-6ac0639cb138\", \"aaaaaaaa-1f51-4b26-a6b7-6ac0639cb138\" ]",
  "createdBy": "ABCDEFGHI",
  "createdByEmail": "joe.user@mycompany.com",
  "createdAt": "2020-11-06T19:09:40.106Z",
  "updatedBy": "ABCDEFGHI",
  "updatedAt": "2020-11-06T19:09:40.106Z",
  "scheduleInterval": "ONE_TIME",
  "reoccuringInterval": null,
  "effectiveFrom": "2020-11-06T19:09:40.106Z",
  "effectiveTo": "2020-11-12T19:09:40.106Z",
  "lastQueuedAt": null,
  "serviceGroups": [
    "admin",
    "issues"
  ],
  "callbackUrl": "https://api.mycompany.com/autodesk/jobinfo",
  "sendEmail": true,
  "startDate": "2023-06-06T00:00:00.000Z",
  "endDate": "2023-06-06T12:00:00.000Z",
  "dateRange": "LAST_MONTH",
  "projectStatus": "active"
}

Documentation /BIM 360 API /API Reference
Requests
PATCH	accounts/{accountId}/requests/{requestId}
Updates the attributes of an existing data request created earlier by the authenticated user. Note that the user must have executive overview or project administrator permissions.

The attribute values provided in this request’s body structure are the values used in the update. You need only specify the attribute values you want to update. Any attributes not specified are not updated.

The attribute values returned in the response body structure describe the current attribute values of the updated data request.

To get request IDs for your requests, use GET requests.

To understand the basics of requests, the jobs they spawn, and the data extracts returned by the jobs, see the Data Connector API Field Guide.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
PATCH	https://developer.api.autodesk.com/data-connector/v1/accounts/:accountId/requests/:requestId
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
Content-Type*
string
Must be application/json
* Required
Request
URI Parameters
accountId
string: UUID
The account ID. You can derive it from your hub ID if necessary: Use GET hubs in the Data Management API to retrieve your hub ID. Remove the initial “b.” from the hub ID to get your account ID.
requestId
string: UUID
The ID of the specified request
Request
Body Structure
isActive
boolean
The data request’s active/inactive status. Possible values: true the request is active; false the request is inactive.
description
string
The user-entered description of this data request.
scheduleInterval
string
The scheduling interval unit for jobs spawned by this data request. This value is multiplied by the reoccurringInterval attribute to specify the length of the recurring interval at which jobs run. Possible values:
ONE_TIME: Run the job only once
DAY: Set the recurring job interval in days
WEEK: Set the recurring job interval in weeks
MONTH: Set the recurring job interval in months
YEAR: Set the recurring job interval in years
Note that recurring jobs start at the day and time when the request first spawns a job. This may be at the date and time specified in the attribute effectiveFrom.

This value is required.

reoccuringInterval
int
The number of scheduleInterval units to wait between job execution for the request. For example, a scheduleInterval value of WEEK and a reoccuringInterval value of 2 means the job will run every two weeks.
effectiveFrom
datetime: ISO 8601
The date and time when a one-time job execution or a recurring interval schedule begins, presented in ISO 8601 format.
effectiveTo
datetime: ISO 8601
The date and time when the recurring interval schedule ends, presented in ISO 8601 format.
serviceGroups
array: string
The service groups from which to extract data, separated by commas.
Possible values: all, activities, admin, assets, checklists, cost, dailylogs, forms, iq, issues, locations, markups, meetingminutes, photos, relationships, reviews, rfis, schedule, sheets, submittals, submittalsacc, transmittals.

Note that the admin service includes both project and account admin, and all produces an extract containing all currently available service groups.

callbackUrl
string
The callback URL specified for the data request. If specified, the Data Connection service calls the URL each time a job executes for the request. The service sends a POST request that provides job execution information. The JSON payload in the POST request contains the following: { "accountId": "account_id", "requestId": "request_id", "jobId": "data_connector_job_id", "state": "complete", "success": true or false }.
If not specified, the Data Connection service does not provide a callback.

sendEmail
boolean
Send a notification email to the user upon job completion. Values: true or false (default is true)
projectId
string
(Legacy): A single project ID for the data request. Superseded by projectIdList.
projectIdList
string
A list of up to 50 project IDs for the data request, which can include a single project or multiple projects. If projectId is also included, projectIdList takes precedence. Required for users with project admin permissions. Optional for users with executive overview permissions, who by default receive data for all projects unless projectIdList is provided.
startDate
string
The start date and time for the data extraction, in ISO 8601 format.
This field applies only to schemas supporting date range extraction. The detailed schema documentation delivered with each data extract identifies the schemas and tables that support date range extraction.

Additional notes on using startDate and endDate:

If you provide only startDate or endDate (but not both), Data Connector uses that single date for both startDate and endDate.
If you request more than the Maximum Date Range Allowed for an extraction, the default date range as documented in the schema documentation is returned.
For the activities service group, data replication can be delayed up to 20 minutes, so your requests should account for that delay.
endDate
string
The end date and time for the data extraction, in ISO 8601 format.
This field applies only to schemas supporting date range extraction. The detailed schema documentation delivered with each data extract identifies the schemas and tables that support date range extraction.

Additional notes on using startDate and endDate:

If you provide only startDate or endDate (but not both), Data Connector uses that single date for both startDate and endDate.
If you request more than the Maximum Date Range Allowed for an extraction, the default date range as documented in the schema documentation is returned.
For the activities service group, data replication can be delayed up to 20 minutes, so your requests should account for that delay.
Response
HTTP Status Code Summary
200
OK
The specified data request was successfully updated and now has these attribute values.
400
Bad Request
The parameters are invalid.
401
Unauthorized
The provided bearer token is invalid.
403
Forbidden
Forbidden. The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The resource or endpoint cannot be found.
429
Too Many Requests
Rate limited exceeded; wait some time before retrying.
500
Internal Server Error
An unexpected error occurred on the server.
503
Service Unavailable
Service unavailable.
Response
Body Structure (200)
id
string: UUID
The ID of the data request.
description
string
The user-entered description of this data request. If not supplied, the default value is a null string.
isActive
boolean
The data request’s active/inactive status. Possible values: true the request is active; false the request is inactive.
accountId
string: UUID
The account ID.
projectId
string: UUID
(Legacy): A single project ID for the data request. Superseded by projectIdList.
projectIdList
array: string
A list of up to 50 project IDs included in the data request. This field contains the project IDs for which data is being extracted. If both projectId and projectIdList were included in the request, this field contains the values from projectIdList.
createdBy
string
The BIM 360 / ACC user ID of the user who created the data request.
createdByEmail
string
The email address of the user who created the data request.
createdAt
datetime: ISO 8601
The date and time the data request was created, presented in ISO 8601 format.
updatedBy
string
The BIM 360 / ACC user ID of the user who last updated the data request.
updatedAt
datetime: ISO 8601
The date and time the data request was last updated, presented in ISO 8601 format.
scheduleInterval
string
The scheduling interval unit for jobs spawned by this data request. This value is multiplied by the reoccurringInterval attribute to specify the length of the recurring interval at which jobs run. Possible values:
ONE_TIME: Run the job only once
DAY: Set the recurring job interval in days
WEEK: Set the recurring job interval in weeks
MONTH: Set the recurring job interval in months
YEAR: Set the recurring job interval in years
reoccuringInterval
int
The number of scheduleInterval units to wait between job execution for the request. For example, a scheduleInterval value of WEEK and a reoccuringInterval value of 2 means the job will run every two weeks.
effectiveFrom
datetime: ISO 8601
The date and time when a one-time job execution or a recurring interval schedule begins, presented in ISO 8601 format.
effectiveTo
datetime: ISO 8601
The date and time when the recurring interval schedule ends, presented in ISO 8601 format.
lastQueuedAt
datetime: ISO 8601
The date and time the last job for this data request was scheduled to execute, presented in ISO 8601 format.
serviceGroups
array: string
The service groups from which data has been extracted, separated by commas.
Possible values: all, activities, admin, assets, checklists, cost, dailylogs, forms, iq, issues, locations, markups, meetingminutes, photos, relationships, reviews, rfis, schedule, sheets, submittals, submittalsacc, transmittals.

Note that the admin service includes both project and account admin, and all indicates that the extract contains all currently available service groups.

callbackUrl
string
The callback URL specified for the data request. If specified, the Data Connection service calls the URL each time a job executes for the request. The service sends a POST request that provides job execution information. The JSON payload in the POST request contains the following: { "accountId": "account_id", "requestId": "request_id", "jobId": "data_connector_job_id", "state": "complete", "success": true or false }.
sendEmail
boolean
Send a notification email to the user upon job completion. Values: true or false (default is true)
startDate
string
The start date and time for the data extraction, in ISO 8601 format.
This field applies only to schemas supporting date range extraction. The detailed schema documentation delivered with each data extract identifies the schemas and tables that support date range extraction.

Additional notes on using startDate and endDate:

If you provide only startDate or endDate (but not both), Data Connector uses that single date for both startDate and endDate.
If you request more than the Maximum Date Range Allowed for an extraction, the default date range as documented in the schema documentation is returned.
For the activities service group, data replication can be delayed up to 20 minutes, so your requests should account for that delay.
endDate
string
The end date and time for the data extraction, in ISO 8601 format.
This field applies only to schemas supporting date range extraction. The detailed schema documentation delivered with each data extract identifies the schemas and tables that support date range extraction.

Additional notes on using startDate and endDate:

If you provide only startDate or endDate (but not both), Data Connector uses that single date for both startDate and endDate.
If you request more than the Maximum Date Range Allowed for an extraction, the default date range as documented in the schema documentation is returned.
For the activities service group, data replication can be delayed up to 20 minutes, so your requests should account for that delay.
dateRange
string
The timeframe used for extracting data in the request. Currently, it is applicable only to the Activities service. This field contains the value specified in the request, indicating the range of data included in the response. Possible values:
TODAY: Data for the current day (from 00:00 UTC to the time the request was made).
YESTERDAY: Data for the previous calendar day (from 00:00 UTC to 23:59 UTC).
PAST_7_DAYS: Data for the last 7 days, including the current day.
MONTH_TO_DATE: Data from the start of the current calendar month (00:00 UTC on the 1st) to the time the request was made.
LAST_MONTH: Data for the entire previous calendar month (00:00 UTC on the 1st to 23:59 UTC on the last day).
projectStatus
string
The types of projects to be included in a request. The possible values are:
all: - all projects (default)
archived: archived projects only
active: active project only
Example
The specified data request was successfully updated and now has these attribute values.

Request
curl -v 'https://developer.api.autodesk.com/data-connector/v1/accounts/:accountId/requests/:requestId' \
  -X 'PATCH' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a' \
  -H 'Content-Type: application/json' \
  -d '{
        "isActive": true,
        "description": "My Company Data Extract",
        "scheduleInterval": "ONE_TIME",
        "reoccuringInterval": null,
        "effectiveFrom": "2020-11-06T19:09:40.106Z",
        "effectiveTo": "2020-11-12T19:09:40.106Z",
        "serviceGroups": [
          "admin",
          "issues"
        ],
        "callbackUrl": "https://api.mycompany.com/autodesk/jobinfo",
        "sendEmail": true,
        "projectId": null,
        "projectIdList": "[ \"ffffffff-1f51-4b26-a6b7-6ac0639cb138\", \"aaaaaaaa-1f51-4b26-a6b7-6ac0639cb138\" ]",
        "startDate": "2023-06-06T00:00:00.000Z",
        "endDate": "2023-06-06T12:00:00.000Z"
      }'
Show Less
Response
{
  "id": "ce9bc188-1e18-11eb-adc1-0242ac120002",
  "description": "My Company Data Extract",
  "isActive": true,
  "accountId": "f9abf4c8-1f51-4b26-a6b7-6ac0639cb138",
  "projectId": null,
  "projectIdList": "[ \"ffffffff-1f51-4b26-a6b7-6ac0639cb138\", \"aaaaaaaa-1f51-4b26-a6b7-6ac0639cb138\" ]",
  "createdBy": "ABCDEFGHI",
  "createdByEmail": "joe.user@mycompany.com",
  "createdAt": "2020-11-06T19:09:40.106Z",
  "updatedBy": "ABCDEFGHI",
  "updatedAt": "2020-11-06T19:09:40.106Z",
  "scheduleInterval": "ONE_TIME",
  "reoccuringInterval": null,
  "effectiveFrom": "2020-11-06T19:09:40.106Z",
  "effectiveTo": "2020-11-12T19:09:40.106Z",
  "lastQueuedAt": null,
  "serviceGroups": [
    "admin",
    "issues"
  ],
  "callbackUrl": "https://api.mycompany.com/autodesk/jobinfo",
  "sendEmail": true,
  "startDate": "2023-06-06T00:00:00.000Z",
  "endDate": "2023-06-06T12:00:00.000Z",
  "dateRange": "LAST_MONTH",
  "projectStatus": "active"
}

Documentation /BIM 360 API /API Reference
Requests
DELETE	accounts/{accountId}/requests/{requestId}
Deletes the specified data request created earlier by the authenticated user. Note that the user must have executive overview or project administrator permissions.

To get request IDs for your requests, use GET requests.

To understand the basics of requests, the jobs they spawn, and the data extracts returned by the jobs, see the Data Connector API Field Guide.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
DELETE	https://developer.api.autodesk.com/data-connector/v1/accounts/:accountId/requests/:requestId
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
* Required
Request
URI Parameters
accountId
string: UUID
The account ID. You can derive it from your hub ID if necessary: Use GET hubs in the Data Management API to retrieve your hub ID. Remove the initial “b.” from the hub ID to get your account ID.
requestId
string: UUID
The ID of the specified request
Response
HTTP Status Code Summary
204
No Content
The specified object is successfully deleted.
400
Bad Request
The parameters are invalid.
401
Unauthorized
The provided bearer token is invalid.
403
Forbidden
Forbidden. The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The resource or endpoint cannot be found.
429
Too Many Requests
Rate limited exceeded; wait some time before retrying.
500
Internal Server Error
An unexpected error occurred on the server.
503
Service Unavailable
Service unavailable.
Response
Body Structure (204)
Response for 204 has no body.

Example
The specified object is successfully deleted.

Request
curl -v 'https://developer.api.autodesk.com/data-connector/v1/accounts/:accountId/requests/:requestId' \
  -X 'DELETE' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
204 No Content

Documentation /BIM 360 API /API Reference
Jobs
GET	accounts/{accountId}/requests/{requestId}/jobs
Returns an array of data connector jobs associated with a request that was created by the authenticated user. The user must have project administrator or executive overview permissions.

Returned information for each job in the array includes the job ID, the ID of its associated request, the ID of the account where the request was created, and the ID and email address of the user who created the request. It also includes information about when the job was created, when it was started and completed (if it has been), its completion status, and its current execution status.

To get request IDs for your requests, use GET requests.

To understand the basics of requests, the jobs they spawn, and the data extracts returned by the jobs, see the Data Connector API Field Guide.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data-connector/v1/accounts/:accountId/requests/:requestId/jobs
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
accountId
string: UUID
The account ID. You can derive it from your hub ID if necessary: Use GET hubs in the Data Management API to retrieve your hub ID. Remove the initial “b.” from the hub ID to get your account ID.
requestId
string: UUID
The ID of the specified request
Request
Query String Parameters
sort
string
The sort order of returned data connector objects. Possible values: asc ascending by date (earliest to latest date), desc descending by date (latest to earliest date).
limit
int
The number of data connector objects to return. Default value: 20
offset
int
The number of data objects to skip before starting to starting to collect the result set. Default value: 0
Response
HTTP Status Code Summary
200
OK
Successfully retrieved an array of jobs associated with the specified data request.
400
Bad Request
The parameters are invalid.
401
Unauthorized
The provided bearer token is invalid.
403
Forbidden
Forbidden. The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The resource or endpoint cannot be found.
429
Too Many Requests
Rate limited exceeded; wait some time before retrying.
500
Internal Server Error
An unexpected error occurred on the server.
503
Service Unavailable
Service unavailable.
Response
Body Structure (200)
 Expand all
pagination
object
Information about the pagination used to return the results array.
results
array: object
An array of job records.
Example
Successfully retrieved an array of jobs associated with the specified data request.

Request
curl -v 'https://developer.api.autodesk.com/data-connector/v1/accounts/:accountId/requests/:requestId/jobs?sort=asc&limit=20&offset=0' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 20,
    "offset": 0,
    "totalResults": 100
  },
  "results": [
    {
      "id": "ce9bc188-1e18-11eb-adc1-0242ac120002",
      "requestId": "a5a8e90f-3dbe-4b08-9b8e-16e8049ce31e",
      "accountId": "f9abf4c8-1f51-4b26-a6b7-6ac0639cb138",
      "projectId": null,
      "projectIdList": "[ \"ffffffff-1f51-4b26-a6b7-6ac0639cb138\", \"aaaaaaaa-1f51-4b26-a6b7-6ac0639cb138\" ]",
      "createdBy": "ABCDEFGHI",
      "createdByEmail": "joe.user@mycompany.com",
      "createdAt": "2020-11-06T19:09:40.106Z",
      "status": "complete",
      "completionStatus": "success",
      "startedAt": "2020-11-06T19:10:00.106Z",
      "completedAt": "2020-11-06T19:29:40.106Z",
      "sendEmail": true,
      "progress": "",
      "lastDownloadedBy": "joe.user@mycompany.com",
      "lastDownloadedAt": "2021-11-06T19:09:40.106Z",
      "startDate": "2023-06-06T00:00:00.000Z",
      "endDate": "2023-06-06T12:00:00.000Z"
    }
  ]
}

Documentation /BIM 360 API /API Reference
Jobs
GET	accounts/{accountId}/jobs
Returns an array of Data Connector jobs spawned by requests from the authenticated user. The array can contain all jobs associated with a specified project, or all jobs associated with all projects in the user’s account. The user must have project administrator or executive overview permissions:

Users with project administrator permissions may retrieve jobs for one project.
Users with executive overview permissions may retrieve jobs for one project or all projects in their account.
Returned information for each job in the array includes the job ID, the ID of its associated request, the ID of the account where the request was created, and the ID and email address of the user who created the request. It also includes information about when the job was created, when it was started and completed (if it has been), its completion status, and its current execution status.

To get request IDs for your requests, use GET requests.

To understand the basics of requests, the jobs they spawn, and the data extracts returned by the jobs, see the Data Connector API Field Guide.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data-connector/v1/accounts/:accountId/jobs
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
accountId
string: UUID
The account ID. You can derive it from your hub ID if necessary: Use GET hubs in the Data Management API to retrieve your hub ID. Remove the initial “b.” from the hub ID to get your account ID.
Request
Query String Parameters
sort
string
The sort order of returned data connector objects. Possible values: asc ascending by date (earliest to latest date), desc descending by date (latest to earliest date).
limit
int
The number of data connector objects to return. Default value: 20
offset
int
The number of data objects to skip before starting to starting to collect the result set. Default value: 0
projectId
string
Project ID of the returned Data Connector objects.
sortFields
string
A string of comma-separated names of the fields by which to sort the returned jobs. The results are sorted by the first field, then by the second field, and so on. Jobs are sorted by each field in ascending order by default; you can prepend any field name with a hyphen ( - ) to sort in descending order. Invalid fields and whitespaces are ignored.
Possible values: projectId, createdBy, createdByEmail, createdAt, status, completionStatus, startedAt, completedAt, startDate, endDate.

filter[field_to_filter]
string
Return only the Data Connector jobs in which the specified field has the specified value. Use the following format in the endpoint URL: filter[field_to_filter]=_filter_value_.
Note that you can provide multiple job filters in the URL, but you may not filter on multiple values of the same field.

Possible field_to_filter values: projectId, createdAt, status, completionStatus, startedAt, completedAt, startDate, endDate. You can also retrieve all Data Connector jobs in the current account by specifying filter[projectId]=null.

For the createdAt, startedAt, and completedAt fields (which accept a date range), specify the range in the form firstdate..lastdate, in ISO 8601 format with the time required. You can alternatively omit the first date (for example, to get everything on or before June 1, 2019 the range would be ..2019-06-01T23:59:59.999Z). You can also omit the last date (for example, to get everything after June 1, 2019 the range would be 2019-06-01T00:00:00.000Z..)

Additional notes on using startDate and endDate:

If you provide only startDate or endDate (but not both), Data Connector uses that single date for both startDate and endDate.
If you request more than the Maximum Date Range Allowed for an extraction, the default date range as documented in the schema documentation is returned.
For the activities service group, data replication can be delayed up to 20 minutes, so your requests should account for that delay.
Response
HTTP Status Code Summary
200
OK
Successfully retrieved an array of jobs associated with the specified data request.
400
Bad Request
The parameters are invalid.
401
Unauthorized
The provided bearer token is invalid.
403
Forbidden
Forbidden. The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The resource or endpoint cannot be found.
429
Too Many Requests
Rate limited exceeded; wait some time before retrying.
500
Internal Server Error
An unexpected error occurred on the server.
503
Service Unavailable
Service unavailable.
Response
Body Structure (200)
 Expand all
pagination
object
Information about the pagination used to return the results array.
results
array: object
An array of job records.
Example
Successfully retrieved an array of jobs associated with the specified data request.

Request
curl -v 'https://developer.api.autodesk.com/data-connector/v1/accounts/:accountId/jobs?sort=asc&limit=20&offset=0&projectId=ffffffff-1f51-4b26-a6b7-6ac0639cb138&sortFields=createdByEmail,-createdAt&filter[field_to_filter]=_filter_value_' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 20,
    "offset": 0,
    "totalResults": 100
  },
  "results": [
    {
      "id": "ce9bc188-1e18-11eb-adc1-0242ac120002",
      "requestId": "a5a8e90f-3dbe-4b08-9b8e-16e8049ce31e",
      "accountId": "f9abf4c8-1f51-4b26-a6b7-6ac0639cb138",
      "projectId": null,
      "projectIdList": "[ \"ffffffff-1f51-4b26-a6b7-6ac0639cb138\", \"aaaaaaaa-1f51-4b26-a6b7-6ac0639cb138\" ]",
      "createdBy": "ABCDEFGHI",
      "createdByEmail": "joe.user@mycompany.com",
      "createdAt": "2020-11-06T19:09:40.106Z",
      "status": "complete",
      "completionStatus": "success",
      "startedAt": "2020-11-06T19:10:00.106Z",
      "completedAt": "2020-11-06T19:29:40.106Z",
      "sendEmail": true,
      "progress": "",
      "lastDownloadedBy": "joe.user@mycompany.com",
      "lastDownloadedAt": "2021-11-06T19:09:40.106Z",
      "startDate": "2023-06-06T00:00:00.000Z",
      "endDate": "2023-06-06T12:00:00.000Z"
    }
  ]
}

Documentation /BIM 360 API /API Reference
Jobs
GET	accounts/{accountId}/jobs
Returns an array of Data Connector jobs spawned by requests from the authenticated user. The array can contain all jobs associated with a specified project, or all jobs associated with all projects in the user’s account. The user must have project administrator or executive overview permissions:

Users with project administrator permissions may retrieve jobs for one project.
Users with executive overview permissions may retrieve jobs for one project or all projects in their account.
Returned information for each job in the array includes the job ID, the ID of its associated request, the ID of the account where the request was created, and the ID and email address of the user who created the request. It also includes information about when the job was created, when it was started and completed (if it has been), its completion status, and its current execution status.

To get request IDs for your requests, use GET requests.

To understand the basics of requests, the jobs they spawn, and the data extracts returned by the jobs, see the Data Connector API Field Guide.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data-connector/v1/accounts/:accountId/jobs
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
accountId
string: UUID
The account ID. You can derive it from your hub ID if necessary: Use GET hubs in the Data Management API to retrieve your hub ID. Remove the initial “b.” from the hub ID to get your account ID.
Request
Query String Parameters
sort
string
The sort order of returned data connector objects. Possible values: asc ascending by date (earliest to latest date), desc descending by date (latest to earliest date).
limit
int
The number of data connector objects to return. Default value: 20
offset
int
The number of data objects to skip before starting to starting to collect the result set. Default value: 0
projectId
string
Project ID of the returned Data Connector objects.
sortFields
string
A string of comma-separated names of the fields by which to sort the returned jobs. The results are sorted by the first field, then by the second field, and so on. Jobs are sorted by each field in ascending order by default; you can prepend any field name with a hyphen ( - ) to sort in descending order. Invalid fields and whitespaces are ignored.
Possible values: projectId, createdBy, createdByEmail, createdAt, status, completionStatus, startedAt, completedAt, startDate, endDate.

filter[field_to_filter]
string
Return only the Data Connector jobs in which the specified field has the specified value. Use the following format in the endpoint URL: filter[field_to_filter]=_filter_value_.
Note that you can provide multiple job filters in the URL, but you may not filter on multiple values of the same field.

Possible field_to_filter values: projectId, createdAt, status, completionStatus, startedAt, completedAt, startDate, endDate. You can also retrieve all Data Connector jobs in the current account by specifying filter[projectId]=null.

For the createdAt, startedAt, and completedAt fields (which accept a date range), specify the range in the form firstdate..lastdate, in ISO 8601 format with the time required. You can alternatively omit the first date (for example, to get everything on or before June 1, 2019 the range would be ..2019-06-01T23:59:59.999Z). You can also omit the last date (for example, to get everything after June 1, 2019 the range would be 2019-06-01T00:00:00.000Z..)

Additional notes on using startDate and endDate:

If you provide only startDate or endDate (but not both), Data Connector uses that single date for both startDate and endDate.
If you request more than the Maximum Date Range Allowed for an extraction, the default date range as documented in the schema documentation is returned.
For the activities service group, data replication can be delayed up to 20 minutes, so your requests should account for that delay.
Response
HTTP Status Code Summary
200
OK
Successfully retrieved an array of jobs associated with the specified data request.
400
Bad Request
The parameters are invalid.
401
Unauthorized
The provided bearer token is invalid.
403
Forbidden
Forbidden. The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The resource or endpoint cannot be found.
429
Too Many Requests
Rate limited exceeded; wait some time before retrying.
500
Internal Server Error
An unexpected error occurred on the server.
503
Service Unavailable
Service unavailable.
Response
Body Structure (200)
 Expand all
pagination
object
Information about the pagination used to return the results array.
results
array: object
An array of job records.
Example
Successfully retrieved an array of jobs associated with the specified data request.

Request
curl -v 'https://developer.api.autodesk.com/data-connector/v1/accounts/:accountId/jobs?sort=asc&limit=20&offset=0&projectId=ffffffff-1f51-4b26-a6b7-6ac0639cb138&sortFields=createdByEmail,-createdAt&filter[field_to_filter]=_filter_value_' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 20,
    "offset": 0,
    "totalResults": 100
  },
  "results": [
    {
      "id": "ce9bc188-1e18-11eb-adc1-0242ac120002",
      "requestId": "a5a8e90f-3dbe-4b08-9b8e-16e8049ce31e",
      "accountId": "f9abf4c8-1f51-4b26-a6b7-6ac0639cb138",
      "projectId": null,
      "projectIdList": "[ \"ffffffff-1f51-4b26-a6b7-6ac0639cb138\", \"aaaaaaaa-1f51-4b26-a6b7-6ac0639cb138\" ]",
      "createdBy": "ABCDEFGHI",
      "createdByEmail": "joe.user@mycompany.com",
      "createdAt": "2020-11-06T19:09:40.106Z",
      "status": "complete",
      "completionStatus": "success",
      "startedAt": "2020-11-06T19:10:00.106Z",
      "completedAt": "2020-11-06T19:29:40.106Z",
      "sendEmail": true,
      "progress": "",
      "lastDownloadedBy": "joe.user@mycompany.com",
      "lastDownloadedAt": "2021-11-06T19:09:40.106Z",
      "startDate": "2023-06-06T00:00:00.000Z",
      "endDate": "2023-06-06T12:00:00.000Z"
    }
  ]
}

Documentation /BIM 360 API /API Reference
Jobs
GET	accounts/{accountId}/jobs/{jobId}
Returns information about a specified job that was spawned by a data request created by the authenticated user. The user must have project administrator or executive overview permissions.

Returned information includes the job ID, the ID of its request, the ID of the account where the request was created, and the ID and email address of the user who created the request. It also includes information about when the job was created, when it was started and completed (if it has been), its completion status, and its current execution status.

To get job IDs for a request, use GET requests/:requestId/jobs.

To understand the basics of requests, the jobs they spawn, and the data extracts returned by the jobs, see the Data Connector API Field Guide.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data-connector/v1/accounts/:accountId/jobs/:jobId
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
* Required
Request
URI Parameters
accountId
string: UUID
The account ID. You can derive it from your hub ID if necessary: Use GET hubs in the Data Management API to retrieve your hub ID. Remove the initial “b.” from the hub ID to get your account ID.
jobId
string: UUID
The job ID
Response
HTTP Status Code Summary
200
OK
Successfully retrieved information about the specified job.
400
Bad Request
The parameters are invalid.
401
Unauthorized
The provided bearer token is invalid.
403
Forbidden
Forbidden. The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The resource or endpoint cannot be found.
429
Too Many Requests
Rate limited exceeded; wait some time before retrying.
500
Internal Server Error
An unexpected error occurred on the server.
503
Service Unavailable
Service unavailable.
Response
Body Structure (200)
id
string: UUID
The job ID.
requestId
string: UUID
The ID of the data request that spawned the job.
accountId
string: UUID
The account ID.
projectId
string: UUID
The project ID.
projectIdList
array: string
The list of project IDs
createdBy
string
The BIM 360 / ACC user ID of the user who created the data request that spawned this job.
createdByEmail
string
The email address of the user who created the data request that spawned this job.
createdAt
datetime: ISO 8601
The date and time the job was created, presented in ISO 8601 format.
status
string
The current status of the job. Possible values: queued, running, complete.
completionStatus
string
The completion status for completed jobs. Possible values: success, failed, cancelled.
startedAt
datetime: ISO 8601
The date and time the job was started, presented in ISO 8601 format. If the job has not yet started, the value is null.
completedAt
datetime: ISO 8601
The date and time the job was completed, presented in ISO 8601 format. If the job has not yet completed, the value is null.
sendEmail
boolean
Send a notification email when the job completes.
progress
int
Job progress indicator (0 to 100 percent)
lastDownloadedBy
string
The ID of the user who last downloaded this job data.
lastDownloadedAt
datetime: ISO 8601
The last date and time that a user downloaded this job data, in ISO 8601 format.
startDate
string
The start date and time for the data extraction, in ISO 8601 format.
This field applies only to schemas that support date range extraction. The detailed schema documentation delivered with each data extract identifies the schemas and tables that support date range extraction.

endDate
string
The end date and time for the data extraction, in ISO 8601 format.
This field applies only to schemas that support date range extraction. The detailed schema documentation delivered with each data extract identifies the schemas and tables that support date range extraction.

Example
Successfully retrieved information about the specified job.

Request
curl -v 'https://developer.api.autodesk.com/data-connector/v1/accounts/:accountId/jobs/:jobId' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "id": "ce9bc188-1e18-11eb-adc1-0242ac120002",
  "requestId": "a5a8e90f-3dbe-4b08-9b8e-16e8049ce31e",
  "accountId": "f9abf4c8-1f51-4b26-a6b7-6ac0639cb138",
  "projectId": null,
  "projectIdList": "[ \"ffffffff-1f51-4b26-a6b7-6ac0639cb138\", \"aaaaaaaa-1f51-4b26-a6b7-6ac0639cb138\" ]",
  "createdBy": "ABCDEFGHI",
  "createdByEmail": "joe.user@mycompany.com",
  "createdAt": "2020-11-06T19:09:40.106Z",
  "status": "complete",
  "completionStatus": "success",
  "startedAt": "2020-11-06T19:10:00.106Z",
  "completedAt": "2020-11-06T19:29:40.106Z",
  "sendEmail": true,
  "progress": "",
  "lastDownloadedBy": "joe.user@mycompany.com",
  "lastDownloadedAt": "2021-11-06T19:09:40.106Z",
  "startDate": "2023-06-06T00:00:00.000Z",
  "endDate": "2023-06-06T12:00:00.000Z"
}

Documentation /BIM 360 API /API Reference
Jobs
DELETE	accounts/{accountId}/jobs/{jobId}
Cancels the specified running job spawned by a data request created by the authenticated user. The user must have project administrator or executive overview permissions.

Use GET requests/:requestId/jobs to get the jobs spawned by a request along with their job IDs. A cancelled job will still appear as a spawned job with a completion status of cancelled.

To understand the basics of requests, the jobs they spawn, and the data extracts returned by the jobs, see the Data Connector API Field Guide.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
DELETE	https://developer.api.autodesk.com/data-connector/v1/accounts/:accountId/jobs/:jobId
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
* Required
Request
URI Parameters
accountId
string: UUID
The account ID. You can derive it from your hub ID if necessary: Use GET hubs in the Data Management API to retrieve your hub ID. Remove the initial “b.” from the hub ID to get your account ID.
jobId
string: UUID
The job ID
Response
HTTP Status Code Summary
204
No Content
The specified object is successfully deleted.
400
Bad Request
The parameters are invalid.
401
Unauthorized
The provided bearer token is invalid.
403
Forbidden
Forbidden. The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The resource or endpoint cannot be found.
429
Too Many Requests
Rate limited exceeded; wait some time before retrying.
500
Internal Server Error
An unexpected error occurred on the server.
503
Service Unavailable
Service unavailable.
Response
Body Structure (204)
Response for 204 has no body.

Example
The specified object is successfully deleted.

Request
curl -v 'https://developer.api.autodesk.com/data-connector/v1/accounts/:accountId/jobs/:jobId' \
  -X 'DELETE' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
204 No Content

Documentation /BIM 360 API /API Reference
Data
GET	accounts/{accountId}/jobs/{jobId}/data-listing
Returns an array of information about the files contained within the data extract created by a specified job. The job must be spawned by a data request that was created by the authenticated user. The user must have executive overview or project administrator permissions.

The array provides a name, creation date, and size for each file in the data extract. You can retrieve any or all of the files using GET jobs/:jobId/data/:name. Its reference page describes the file types within a data extract.

If the job was cancelled or otherwise failed to create a data extract, this endpoint returns a 404 error “The requested resource does not exist.”

To get job IDs for a request, use GET requests/:requestId/jobs.

To understand the basics of requests, the jobs they spawn, and the data extracts returned by the jobs, see the Data Connector API Field Guide.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data-connector/v1/accounts/:accountId/jobs/:jobId/data-listing
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
accountId
string: UUID
The account ID. You can derive it from your hub ID if necessary: Use GET hubs in the Data Management API to retrieve your hub ID. Remove the initial “b.” from the hub ID to get your account ID.
jobId
string: UUID
The job ID
Response
HTTP Status Code Summary
200
OK
Successfully returned an array of information about data extract files for the specified job.
400
Bad Request
The parameters are invalid.
401
Unauthorized
The provided bearer token is invalid.
403
Forbidden
Forbidden. The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The resource or endpoint cannot be found.
429
Too Many Requests
Rate limited exceeded; wait some time before retrying.
500
Internal Server Error
An unexpected error occurred on the server.
503
Service Unavailable
Service unavailable.
Response
Body Structure (200)
name
string
The name of the file.
createdAt
datetime: ISO 8601
The date and time the file was created, presented in ISO 8601 format.
size
int
The size of the file in bytes.
Example
Successfully returned an array of information about data extract files for the specified job.

Request
curl -v 'https://developer.api.autodesk.com/data-connector/v1/accounts/:accountId/jobs/:jobId/data-listing' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
[
  {
    "name": "admin_companies.csv",
    "createdAt": "2020-11-06T19:09:40.106Z",
    "size": "123456"
  }
]

Documentation /BIM 360 API /API Reference
Data
GET	accounts/{accountId}/jobs/{jobId}/data/{name}
Returns a signed URL that you can contact to retrieve a single specified file from a specified job’s data extract. You can examine a data extract’s available files, their names, and their sizes using GET jobs/:jobId/data-listing. The information it returns can help you plan what you would like to retrieve using this endpoint, useful if you want to retrieve only part of a data extract to avoid downloading large but unnecessary files. The user must have executive overview or project administrator permissions.

Each data extract contains three types of files:

One CSV file for each service group specified for the data extract. Each CSV file contains all the data returned for that service group. The data is in CSV format.
A README file that lists the CSV files and describes in detail the schema used for each CSV file.
A master ZIP file that contains all of the CSV files and the accompanying README file.
To retrieve the entire data extract, use this endpoint to retrieve the ZIP file. If you don’t know the schema for the CSV files in the data extract, retrieve the README file for detailed schema descriptions. You can also use this endpoint to retrieve a single CSV file without retrieving the rest of the data extract’s CSV files.

The secure signed URL this endpoint returns is valid for 60 seconds. If you don’t request data from the URL within that time, the URL no longer works. Once you’ve requested data, though, the download can take as long as necessary.

To get job IDs for a request, use GET requests/:requestId/jobs.

To understand the basics of requests, the jobs they spawn, and the data extracts returned by the jobs, see the Data Connector API Field Guide.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data-connector/v1/accounts/:accountId/jobs/:jobId/data/:name
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
accountId
string: UUID
The account ID. You can derive it from your hub ID if necessary: Use GET hubs in the Data Management API to retrieve your hub ID. Remove the initial “b.” from the hub ID to get your account ID.
jobId
string: UUID
The job ID
name
string: UUID
Name of the file to retrieve
Response
HTTP Status Code Summary
200
OK
Successfully set up a job extract file for retrieval from a returned signed URL
400
Bad Request
The parameters are invalid.
401
Unauthorized
The provided bearer token is invalid.
403
Forbidden
Forbidden. The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The resource or endpoint cannot be found.
429
Too Many Requests
Rate limited exceeded; wait some time before retrying.
500
Internal Server Error
An unexpected error occurred on the server.
503
Service Unavailable
Service unavailable.
Response
Body Structure (200)
size
int
The size of the file in bytes.
name
string
The name of the file.
signedUrl
string
The signed URL to contact to download the specified file. Note that this URL will be valid for 60 seconds from the time of this response.
Example
Successfully set up a job extract file for retrieval from a returned signed URL

Request
curl -v 'https://developer.api.autodesk.com/data-connector/v1/accounts/:accountId/jobs/:jobId/data/:name' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "size": "123456",
  "name": "admin_companies.csv",
  "signedUrl": "https://bim360dc-p-ue1-extracts.s3.amazonaws.com/data/9be6b2cd-e9e8-4861-aa45-c96668a9f6bd/d023d0cf-b603-4de9-b240-a0e8a85bbf8d/autodesk_data_extract.zip?AWSAccessKeyId=ASIAWZ7KRFT5TZSCKIYO&Expires=1604690406&Signature=cb5HR%2FthOATYIAqW41ojbfptMsM%3D&x-amz-security-token=IQoJb3JpZ2luX2VjELT%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIHQdYa9Z%2BhS3u5EmRfEoz1KFwm2xCvLK6pH1Go2q88%2BWAiEAy7KMbb%2FKBww1XWxR0B%2FepB0Syt6jOhXTahznLrCWKcYq2gEIHBACGgw0NjgxMDY0MjM1NDciDHewqYuFoS8GY2PlZCq3AZG8jsIKx5egqYARC2N%2F7%2B72nkATTV6PwomhMOsAb9eZhIBCR%2F861wvtM1%2B4gEfu8LN9gWMNI%2BvmHcWC92kC1lujXM1Klpq8KksSxN8%2Bt5aurFPwZ465iespRnEHKB7jX2KUzCVDPCpZ7NDTvcsy0TdqLU82L0p%2Bw6fTT0QhGuykRuhn%2FURLbtzVHvx4wi3R2kSEJ9DWGkAaWR96h76vCFDaC9o2VmLEjKww88YunnYKQcAqIhGEBTD2vpb9BTrgAVGy7Cavc8LDgwuoS7LBt%2FmE6iPohyfILcksPL5NYl3yvaUhYW%2FX9w1mgLgpnuEt4rcdcrUOTcOdjRFmqvA9%2FVPFXD%2FCWxzDRU6V3U%2BC1dZi5Y4lV3AfodZyhsJI9aSkX2D0xDMpuV%2FDiX0HyCCVk3awuCQDfPtlWqbMVzW9zzO5d6JBThIIxdEGq1Nwe677anh1WQGY%2Fuemcc4fyZRTx%2Br0i%2B8Z35YtR0pEKfvp7GQhV7d%2FSfh%2FYL58QMvvciH4yBqkcMba8SwDJQQV03Q%2FrQX2vqVOq%2BSFCijaXalvPjQp"
}

Documentation /BIM 360 API /API Reference
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

Documentation /BIM 360 API /API Reference
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

Documentation /BIM 360 API /API Reference
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

Documentation /BIM 360 API /API Reference
Documents
POST	projects/{project_id}/versions/{version_id}/exports
Exports a single page from an uploaded PDF file into a new PDF file. You can also export the page’s markups (annotations) and hyperlinks.

Note that you can only export a page from a PDF file that was uploaded to the Plans folder or to a folder nested under the Plans folder (attributes.extension.data.actions: SPLIT). BIM 360 Document Management splits these files into separate pages (sheets) when they are uploaded, and assigns a separate ID to each page. You can identify exportable PDF files, by searching for files with the following combination of properties:

attributes.extension.type: items:autodesk.bim360.Document (identifies all files that are split into separate pages)
attributes.extension.data.sourceFileName: <filename>.pdf (identifies all PDF files)
You can export PDF pages both from PDF files that were uploaded via the BIM 360 Document Management UI and from PDF files that were uploaded via BIM 360 endpoints. For more details about uploading documents to BIM 360 via the BIM 360 endpoints, see the File Upload tutorial.

Note that this endpoint is asynchronous and initiates a job that runs in the background, rather than halting execution of your program. The response returns an export ID that you can use to poll GET projects/:project_id/versions/:version_id/exports/:export_id to verify the status of the job. When the job is complete, you can retrieve the data you need to download the exported page.

Note that when exporting the same file version again, this POST endpoint returns the same response structure as the GET projects/:project_id/versions/:version_id/exports/:export_id endpoint. A new signed URL is generated, and the previous one remains active until it expires after two minutes.

Note that the user must have permission to view files. For information about permissions, see the Help documentation.

For more details about exporting PDF files, see the PDF Export tutorial.

For more information about Document Management endpoints, see the Data Management API

Note that this endpoint is ONLY compatible with BIM 360 projects. It is not compatible with Autodesk Construction Cloud (ACC) projects. For more information about compatibility between between BIM 360 and ACC, see the Compatibility section.

Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/bim360/docs/v1/projects/:project_id/versions/:version_id/exports
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
string: UUID
The ID of the project. This corresponds to project ID in the Data Management API. To convert a project ID in the Data Management API into a project ID in the BIM 360 API you need to remove the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.
version_id
string
The URL-encoded version ID (URN) of the page to export.
When a file is uploaded to BIM 360 Document Management, a corresponding version ID is created for the file.

Every time the file is saved a new version is created. When a PDF file is uploaded to the Plans folder or to a child of the Plans folder, BIM 360 assigns a separate version ID to each page of the PDF. The user needs to select the version ID that corresponds to the page that he/she wants to export.

To export the latest version (tip) of the page, use GET projects/:project_id/folders/:folder_id/contents to find the ID.

To export an alternative version of the page, use GET projects/:project_id/items/:item_id/versions to find the ID.

Request
Body Structure
includeMarkups
boolean
true: export the page with markups (annotations). Note that the endpoint only exports published and unarchived markups.
false: (default) export the page without markups.

You can manage a page’s markups by opening the page in the Document Management module.

includeHyperlinks
boolean
true: export the page with hyperlinks.
false: (default) export the page without hyperlinks.

Note that all hyperlinks in the page are exported, including external links and internal links to other BIM 360 documents, whether the links were imported when the PDF was originally uploaded or whether they were added within BIM 360 Document Management.

Response
HTTP Status Code Summary
202
Accepted
Successfully created an export job.
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
The project or exported document does not exist.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (202)
id
string: UUID
The unique identifier of the export job.
status
enum:string
The status of the export job. Possible values: committed, completed, failed
Example
Successfully created an export job.

Request
curl -v 'https://developer.api.autodesk.com/bim360/docs/v1/projects/c0337487-5b66-422b-a284-c273b424af54/versions/urn%3Aadsk.wipqa%3Afs.file%3Avf.pf3frU0gTZaOotKXg2h1Fw%3Fversion%3D1/exports' \
  -X 'POST' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a' \
  -H 'Content-Type: application/json' \
  -d '{
        "includeMarkups": true,
        "includeHyperlinks": true
      }'
Show Less
Response
{
  "id": "eed4fd1d-57fc-4e41-9c19-1d7b8ec2cf25",
  "status": "committed"
}

Documentation /BIM 360 API /API Reference
Documents
GET	projects/{project_id}/versions/{version_id}/exports/{export_id}
Returns the status of a PDF export job, as well as data you need to download the exported file when the export is complete.

The POST projects/:project_id/versions/:version_id/exports endpoint initiates the job, and returns a job ID to be used in this endpoint.

To download the exported PDF file after the job is complete, use GET :urn/manifest/:derivativeurn.

For more information about Document Management endpoints, see the Data Management API

Note that this endpoint is ONLY compatible with BIM 360 projects. It is not compatible with Autodesk Construction Cloud (ACC) projects. For more information about compatibility between between BIM 360 and ACC, see the Compatibility section.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/docs/v1/projects/:project_id/versions/:version_id/exports/:export_id
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
The ID of the project. This corresponds to project ID in the Data Management API. To convert a project ID in the Data Management API into a project ID in the BIM 360 API you need to remove the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.
version_id
string
The URL-encoded version ID (URN) of the exported page; selected when initiating POST projects/:project_id/versions/:version_id/exports.
export_id
string: UUID
The ID of the export job; returned when initiating POST projects/:project_id/versions/:version_id/exports.
Response
HTTP Status Code Summary
200
OK
The request has succeeded.
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
The project, exported document or job does not exist.
429
Too Many Requests
Rate limit exceeded; wait some time before retrying.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
id
string: UUID
The ID of the export job.
status
enum:string
The status of the export job. Possible values: committed, completed, failed. When the job is complete, an object representing the result of the job is returned in the response.
data
object
Example
The request has succeeded.

Request
curl -v 'https://developer.api.autodesk.com/bim360/docs/v1/projects/c0337487-5b66-422b-a284-c273b424af54/versions/urn%3Aadsk.wipqa%3Afs.file%3Avf.pf3frU0gTZaOotKXg2h1Fw%3Fversion%3D1/exports/433d07ec-32a2-44eb-a5eb-b41090bfe932' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "id": "433d07ec-32a2-44eb-a5eb-b41090bfe932",
  "status": "completed",
  "data": {
    "versionUrn": "dXJuOmFkc2sud2lwcWE6ZnMuZmlsZTp2Zi5wZjNmclUwZ1RaYU9vdEtYZzJoMUZ3P3ZlcnNpb249MQ",
    "resourceId": "urn:adsk.viewing:fs.file:dXJuOmFkc2sud2lwcWE6ZnMuZmlsZTp2Zi5wZjNmclUwZ1RaYU9vdEtYZzJoMUZ3P3ZlcnNpb249MQ/output/qXP_ZA5_3EqJoq5zqvnLHA/h8YAl4KMcEe9-L5SaEXY6A.pdf",
    "signedUrl": "https://autodesk-360-translation-storage.s3.amazonaws.com/9358_dXJuOmFkc2sud2lwcWE6ZnMuZmlsZTp2Zi5jb1pWZEdIclNMMkJ4SGJZTEFhVWF3P3ZlcnNpb249MQ/output/4/page.pdf?X-Amz-Security-Token={token}&X-Amz-Algorithm={algorithm}&X-Amz-Date={date}&X-Amz-SignedHeaders={header}&X-Amz-Expires={expire}&X-Amz-Credential={credential}&X-Amz-Signature={sign}"
  }
}

Documentation /BIM 360 API /API Reference
Naming Standards (beta)
GET	projects/{projectId}/naming-standards/{id}
Retrieves the file naming standard for a project.

You need to configure the file naming standard in the UI. For more information, see the BIM 360 File Naming Standard help documentation.

Note that the order of the objects that the endpoint returns in the response corresponds to the order of the fields that you set for the naming standard in the UI.

Note that we currently support one file naming standard per project.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/docs/v1/projects/:projectId/naming-standards/:id
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
x-ads-region
string
The region to which your request should be routed. If not set, the request is routed automatically but may incur a small latency increase.
Possible values: US, EMEA.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
This corresponds to project ID in the Data Management API. To convert a project ID in the Data Management API into a project ID in the BIM 360 API you need to remove the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

To learn how to find the project ID, see the Retrieve BIM 360 Account and Project ID tutorial.

id
string: UUID
The ID of the file naming standard.
The file naming standard is applied to the project files folder or its subfolders. To find the ID:

For the project files folder, call GET hubs/:hub_id/projects/:project_id/topFolders.
For subfolders, call GET projects/:project_id/folders/:folder_id/contents.
For a specific folder, call GET projects/:project_id/folders/:folder_id.
The ID is under data.attributes.extension.data.namingStandardIds.

Response
HTTP Status Code Summary
200
OK
Successfully retrieved the file naming standard.
400
Bad Request
The parameters of the requested operation are invalid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The file naming standard does not exist.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
id
string: UUID
The ID of file naming standard.
name
string
The name of the file naming standard.
definition
object
The file naming standard format.
Example
Successfully retrieved the file naming standard.

Request
curl -v 'https://developer.api.autodesk.com/bim360/docs/v1/projects/c0337487-5b66-422b-a284-c273b424af54/naming-standards/68097e38-bcae-4fb6-9da2-89eca69bccc8' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "id": "68097e38-bcae-4fb6-9da2-89eca69bccc8",
  "name": "Default - ISO 19650",
  "definition": {
    "fields": [
      {
        "attributeId": 333879,
        "name": "Project",
        "type": "ALPHANUMERIC",
        "description": "Project code.",
        "optional": false,
        "maxLength": 6,
        "minLength": 2,
        "defaultValue": "PROJ"
      },
      {
        "attributeId": 333880,
        "name": "Originator",
        "type": "ARRAY",
        "description": "Code representing the organization creating the file.",
        "options": [
          {
            "value": "XXX",
            "description": "Example Organization"
          },
          {
            "value": "ARC",
            "description": "Architect"
          }
        ],
        "optional": false,
        "defaultValue": null
      },
      {
        "attributeId": 333881,
        "name": "Volume/System",
        "type": "ARRAY",
        "description": "Code for System reference",
        "options": [
          {
            "value": "ZZ",
            "description": "All Volumes/Systems"
          },
          {
            "value": "XX",
            "description": "No Volume/System applicable"
          }
        ],
        "optional": false
      },
      {
        "attributeId": 333882,
        "name": "Level/Location",
        "type": "ARRAY",
        "description": "Code representing the Level/Location relevant to the file.",
        "options": [
          {
            "value": "ZZ",
            "description": "Multiple Levels/Locations"
          },
          {
            "value": "XX",
            "description": "No Level/Location applicable"
          },
          {
            "value": "00",
            "description": "Base Level"
          },
          {
            "value": "01",
            "description": "Level 01"
          },
          {
            "value": "02",
            "description": "Level 02"
          },
          {
            "value": "M1",
            "description": "Mezzanine above Level 01"
          },
          {
            "value": "M2",
            "description": "Mezzanine above Level 02"
          },
          {
            "value": "B1",
            "description": "Basement Level 1"
          },
          {
            "value": "B2",
            "description": "Basement Level 2"
          }
        ],
        "optional": false,
        "defaultValue": null
      },
      {
        "attributeId": 333883,
        "name": "Type",
        "type": "ARRAY",
        "description": "Code representing the type of file.",
        "options": [
          {
            "value": "AF",
            "description": "Animation File (of a model)"
          },
          {
            "value": "BQ",
            "description": "Bill of Quantities"
          },
          {
            "value": "CA",
            "description": "Calculations"
          },
          {
            "value": "CM",
            "description": "Combined Model (combined multidiscipline model)"
          },
          {
            "value": "CO",
            "description": "Correspondence"
          },
          {
            "value": "CP",
            "description": "Cost Plan"
          },
          {
            "value": "CR",
            "description": "Clash Rendition"
          },
          {
            "value": "DB",
            "description": "Database"
          },
          {
            "value": "DR",
            "description": "Drawing Rendition"
          },
          {
            "value": "FN",
            "description": "File Note"
          },
          {
            "value": "HS",
            "description": "Health and Safety"
          },
          {
            "value": "IE",
            "description": "Information Exchange file"
          },
          {
            "value": "M2",
            "description": "2D model"
          },
          {
            "value": "M3",
            "description": "3D model"
          },
          {
            "value": "MI",
            "description": "Minutes / Action Notes"
          },
          {
            "value": "MR",
            "description": "Model Rendition for other renditions"
          },
          {
            "value": "MS",
            "description": "Method Statement"
          },
          {
            "value": "PP",
            "description": "Presentation"
          },
          {
            "value": "PR",
            "description": "Programme"
          },
          {
            "value": "RD",
            "description": "Room Data sheet"
          },
          {
            "value": "RI",
            "description": "Request for Information"
          },
          {
            "value": "RP",
            "description": "Report"
          },
          {
            "value": "SA",
            "description": "Schedule of Accommodation"
          },
          {
            "value": "SH",
            "description": "Schedule"
          },
          {
            "value": "SN",
            "description": "Snagging List"
          },
          {
            "value": "SP",
            "description": "Specification"
          },
          {
            "value": "SU",
            "description": "Survey"
          },
          {
            "value": "VS",
            "description": "Visualization"
          }
        ],
        "optional": false,
        "defaultValue": null
      },
      {
        "attributeId": 333884,
        "name": "Role",
        "type": "ARRAY",
        "description": "Codes for disciplines and roles.",
        "options": [
          {
            "value": "A",
            "description": "Architect"
          },
          {
            "value": "B",
            "description": "Building Surveyor"
          },
          {
            "value": "C",
            "description": "Civil Engineer"
          },
          {
            "value": "D",
            "description": "Drainage Engineer"
          },
          {
            "value": "E",
            "description": "Electrical Engineer"
          },
          {
            "value": "F",
            "description": "Facilities Manager"
          },
          {
            "value": "G",
            "description": "Geographical and Land Surveyor"
          },
          {
            "value": "H",
            "description": "Heating and Ventilation Designer (deprecated)"
          },
          {
            "value": "I",
            "description": "Interior Designer"
          },
          {
            "value": "K",
            "description": "Client"
          },
          {
            "value": "L",
            "description": "Landscape Architect"
          },
          {
            "value": "M",
            "description": "Mechanical Engineer"
          },
          {
            "value": "P",
            "description": "Public Health Engineer"
          },
          {
            "value": "Q",
            "description": "Quantity Surveyor"
          },
          {
            "value": "S",
            "description": "Structural Engineer"
          },
          {
            "value": "T",
            "description": "Town and Country Planner"
          },
          {
            "value": "W",
            "description": "Contractor"
          },
          {
            "value": "X",
            "description": "Subcontractor"
          },
          {
            "value": "Y",
            "description": "Specialist Designer"
          },
          {
            "value": "Z",
            "description": "General (non-disciplinary)"
          }
        ],
        "optional": false,
        "defaultValue": null
      },
      {
        "attributeId": 333885,
        "name": "Number",
        "type": "NUMERIC",
        "description": "Sequential Number.",
        "optional": false,
        "maxLength": 6,
        "minLength": 4,
        "defaultValue": "1111"
      }
    ],
    "metadata": [
      {
        "attributeId": 333886,
        "name": "Status",
        "type": "ARRAY",
        "description": "The Suitability Code.",
        "options": [
          {
            "value": "S0",
            "description": "Initial status"
          },
          {
            "value": "S1",
            "description": "Suitable for coordination"
          },
          {
            "value": "S2",
            "description": "Suitable for information"
          },
          {
            "value": "S3",
            "description": "Suitable for review and comment"
          },
          {
            "value": "S4",
            "description": "Suitable for stage approval"
          },
          {
            "value": "S6",
            "description": "Suitable for PIM authorization"
          },
          {
            "value": "S7",
            "description": "Suitable for AIM authorization"
          },
          {
            "value": "A0",
            "description": "Authorized and accepted for Strategy work stage"
          },
          {
            "value": "A1",
            "description": "Authorized and accepted for Brief work stage"
          },
          {
            "value": "A2",
            "description": "Authorized and accepted for Concept work stage"
          },
          {
            "value": "A3",
            "description": "Authorized and accepted for Definition work stage"
          },
          {
            "value": "A4",
            "description": "Authorized and accepted for Design work stage"
          },
          {
            "value": "A5",
            "description": "Authorized and accepted for Construct and Commission work stage"
          },
          {
            "value": "A6",
            "description": "Authorized and accepted for Handover and Close-out work stage"
          },
          {
            "value": "A7",
            "description": "Authorized and accepted for Operation and End-of-Life work stage"
          },
          {
            "value": "B0",
            "description": "Partial sign-off for Strategy work stage"
          },
          {
            "value": "B1",
            "description": "Partial sign-off for Brief work stage"
          },
          {
            "value": "B2",
            "description": "Partial sign-off for Concept work stage"
          },
          {
            "value": "B3",
            "description": "Partial sign-off for Definition work stage"
          },
          {
            "value": "B4",
            "description": "Partial sign-off for Design work stage"
          },
          {
            "value": "B5",
            "description": "Partial sign-off for Construct and Commission work stage"
          },
          {
            "value": "B6",
            "description": "Partial sign-off for Handover and Close-out work stage"
          },
          {
            "value": "B7",
            "description": "Partial sign-off for Operation and End-of-Life work stage"
          },
          {
            "value": "CR",
            "description": "As constructed record document"
          }
        ],
        "optional": true,
        "defaultValue": null
      },
      {
        "attributeId": 333887,
        "name": "Revision",
        "type": "ALPHANUMERIC",
        "description": "Code for revision of data.",
        "optional": true,
        "maxLength": 8,
        "minLength": 3,
        "defaultValue": "S01"
      },
      {
        "attributeId": 333888,
        "name": "Classification",
        "type": "CLASSIFICATION",
        "description": "Code to reference asset.",
        "optional": true,
        "defaultValue": null
      }
    ],
    "delimiter": "-"
  }
}
Documentation /BIM 360 API /API Reference
Permissions (beta)
POST	projects/{project_id}/folders/{folder_id}/permissions:batch-create
Assign permissions to multiple users, roles, and companies for a BIM 360 Document Management folder.

For more information about folder permissions, see the BIM 360 Help documentation or the ACC Files Help documentation.

For details about updating a user’s permissions, see the Update a User’s Folder Permissions tutorial.

If you are calling this endpoint on behalf of a user, the user needs to have CONTROL permissions for the folder.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/bim360/docs/v1/projects/:project_id/folders/:folder_id/permissions:batch-create
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
The ID of the project. This corresponds to project ID in the Data Management API. To convert a project ID in the Data Management API into a project ID in the BIM 360 API you need to remove the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.
folder_id
string
The ID (URN) of the folder.
For details about how to find the URN, follow the initial steps (1-3) in the Download Files tutorial.

Request
Body Structure
A list of permission items to create in this folder.

subjectId*
string: UUID
The ID of the user, role, or company. To verify the subjectId:
For a user, use GET users.
For a role, use GET roles
For a company, use GET companies
autodeskId
string
The Autodesk ID of the user, role or company.
subjectType*
enum:string
The type of subject. Possible values: USER, COMPANY, ROLE
actions*
array: string
Permitted actions for the user, role, or company. The permission action group is different in BIM 360 Document Management and ACC Build Files.
The six permission levels in BIM 360 Document Management correspond to one or more actions:
View Only: VIEW, COLLABORATE
View/Download: VIEW, DOWNLOAD, COLLABORATE
Upload Only: PUBLISH
View/Download+Upload: PUBLISH, VIEW, DOWNLOAD, COLLABORATE
View/Download+Upload+Edit: PUBLISH, VIEW, DOWNLOAD, COLLABORATE, EDIT
Full controller: PUBLISH, VIEW, DOWNLOAD, COLLABORATE, EDIT, CONTROL
The six permission levels in Autodesk Construction Cloud correspond to one or more actions:
View Only: VIEW, COLLABORATE
View/Download: VIEW, DOWNLOAD, COLLABORATE
View/Download+PublishMarkups: VIEW, DOWNLOAD, COLLABORATE, PUBLISH_MARKUP
View/Download+PublishMarkups+Upload: PUBLISH, VIEW, DOWNLOAD, COLLABORATE, PUBLISH_MARKUP
View/Download+PublishMarkups+Upload+Edit: PUBLISH, VIEW, DOWNLOAD, COLLABORATE, PUBLISH_MARKUP, EDIT
Full controller: PUBLISH, VIEW, DOWNLOAD, COLLABORATE, PUBLISH_MARKUP, EDIT, CONTROL
See the BIM 360 Help documentation or the ACC Files Help documentation for more details about each permission level.

Note that the full set of permissions assigned to the user, role, or company is a combination of actions and inheritActions.

* Required
Response
HTTP Status Code Summary
200
OK
Successfully created permissions
400
Bad Request
Operation failed because of bad input
403
Forbidden
The user does not have permission to perform this operation.
404
Not Found
The project or folder does not exist
422
Unprocessable Entity
The payload contains unprocessable data
423
Locked
The folder is temporarily inaccessible because it is being used by another operation.
429
Too Many Requests
The server has received too many requests.
500
Internal Server Error
Operation failed because of an internal server error
Response
Body Structure (200)
 Expand all
results
array: object
The results object.
Example
Successfully created permissions

Request
curl -v 'https://developer.api.autodesk.com/bim360/docs/v1/projects/c0337487-5b66-422b-a284-c273b424af54/folders/urn:adsk.wipprod:fs.folder:co.9g7HeA2wRqOxLlgLJ40UGQ/permissions:batch-create' \
  -X 'POST' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a' \
  -H 'Content-Type: application/json' \
  -d '[
        {
          "subjectId": "684c4e47-7720-4961-b0e9-ff5966d82edb",
          "autodeskId": "45GPJ4KAX789",
          "subjectType": "USER",
          "actions": [
            "PUBLISH"
          ]
        }
      ]'
Show Less
Response
{
  "results": [
    {
      "subjectId": "684c4e47-7720-4961-b0e9-ff5966d82edb",
      "subjectType": "USER",
      "actions": [
        "PUBLISH"
      ]
    }
  ]
}
Documentation /BIM 360 API /API Reference
Permissions (beta)
GET	projects/{project_id}/folders/{folder_id}/permissions
Retrieves information about the permissions assigned to users, roles and companies for a BIM 360 Document Management folder, including details about the name and the status.

For information about the different types of permissions you can assign to a user, role or company, see the Help documentation.

For more details about retrieving a user’s permissions, see the Retrieve Permissions tutorial.

If you are calling this endpoint on behalf of a user, the user needs to have VIEW permissions for the folder.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/docs/v1/projects/:project_id/folders/:folder_id/permissions
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
The ID of the project. This corresponds to project ID in the Data Management API. To convert a project ID in the Data Management API into a project ID in the BIM 360 API you need to remove the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.
folder_id
string
The ID (URN) of the folder.
For details about how to find the URN, follow the initial steps (1-3) in the Download Files tutorial.

Response
HTTP Status Code Summary
200
OK
Successfully retrieved a list of permissions
400
Bad Request
Operation failed because of bad input
403
Forbidden
The user does not have permission to perform this operation.
404
Not Found
The project or folder does not exist
429
Too Many Requests
The server has received too many requests.
500
Internal Server Error
Operation failed because of an internal server error
Response
Body Structure (200)
subjectId
string: UUID
The ID of the user, role, or company. For example, this corresponds to the id, roleId, or companyId in the response for GET /users/user_id.
autodeskId
string
The Autodesk ID of the user, role or company.
name
string
The name of the user, role, or company.
email
string
The user’s email. Only relevant if the subject is a user.
userType
enum:string
The type of project user. Possible values: PROJECT_ADMIN or PROJECT_MEMBER. Only relevant if the subject is a user.
subjectType
enum:string
The type of subject. Possible values: USER, COMPANY, ROLE
subjectStatus
enum:string
The status of the user, role, or company. Possible values:
For a user: INACTIVE, ACTIVE, PENDING, DISABLED
For a role: INACTIVE, ACTIVE
For a company: ACTIVE
actions
array: string
Permitted actions for the user, role, or company. The permission action group is different in BIM 360 Document Management and ACC Files.
The six permission levels in BIM 360 Document Management correspond to one or more actions:
View Only: VIEW, COLLABORATE
View/Download: VIEW, DOWNLOAD, COLLABORATE
Upload Only: PUBLISH
View/Download+Upload: PUBLISH, VIEW, DOWNLOAD, COLLABORATE
View/Download+Upload+Edit: PUBLISH, VIEW, DOWNLOAD, COLLABORATE, EDIT
Full controller: PUBLISH, VIEW, DOWNLOAD, COLLABORATE, EDIT, CONTROL
The six permission levels in ACC correspond to one or more actions:
View Only: VIEW, COLLABORATE
View/Download: VIEW, DOWNLOAD, COLLABORATE
View/Download+PublishMarkups: VIEW, DOWNLOAD, COLLABORATE, PUBLISH_MARKUP
View/Download+PublishMarkups+Upload: PUBLISH, VIEW, DOWNLOAD, COLLABORATE, PUBLISH_MARKUP
View/Download+PublishMarkups+Upload+Edit: PUBLISH, VIEW, DOWNLOAD, COLLABORATE, PUBLISH_MARKUP, EDIT
Full controller: PUBLISH, VIEW, DOWNLOAD, COLLABORATE, PUBLISH_MARKUP, EDIT, CONTROL
See the BIM 360 Help documentation or the ACC Files Help documentation for more details about each permission group.

Note that the full set of permissions assigned to the user, role, or company is a combination of actions and inheritActions.

inheritActions
array: string
Permissions inherited by the user, role, or company from a higher level folder. The permission action group is different in BIM 360 Document Management and ACC Files.
The six permission levels in BIM 360 Document Management correspond to one or more actions:
View Only: VIEW, COLLABORATE
View/Download: VIEW, DOWNLOAD, COLLABORATE
Upload Only: PUBLISH
View/Download+Upload: PUBLISH, VIEW, DOWNLOAD, COLLABORATE
View/Download+Upload+Edit: PUBLISH, VIEW, DOWNLOAD, COLLABORATE, EDIT
Full controller: PUBLISH, VIEW, DOWNLOAD, COLLABORATE, EDIT, CONTROL
The six permission levels in ACC correspond to one or more actions:
View Only: VIEW, COLLABORATE
View/Download: VIEW, DOWNLOAD, COLLABORATE
View/Download+PublishMarkups: VIEW, DOWNLOAD, COLLABORATE, PUBLISH_MARKUP
View/Download+PublishMarkups+Upload: PUBLISH, VIEW, DOWNLOAD, COLLABORATE, PUBLISH_MARKUP
View/Download+PublishMarkups+Upload+Edit: PUBLISH, VIEW, DOWNLOAD, COLLABORATE, PUBLISH_MARKUP, EDIT
Full controller: PUBLISH, VIEW, DOWNLOAD, COLLABORATE, PUBLISH_MARKUP, EDIT, CONTROL
See the BIM 360 Help documentation or the ACC Files Help documentation for more details about each permission group.

Note that the full set of permissions assigned to the user, role, or company is a combination of actions and inheritActions.

Note that project administrators’ permissions are non-inherited actions for the root folder, and inherited actions for all other folders.

Example
Successfully retrieved a list of permissions

Request
curl -v 'https://developer.api.autodesk.com/bim360/docs/v1/projects/c0337487-5b66-422b-a284-c273b424af54/folders/urn:adsk.wipprod:fs.folder:co.9g7HeA2wRqOxLlgLJ40UGQ/permissions' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
[
  {
    "subjectId": "684c4e47-7720-4961-b0e9-ff5966d82edb",
    "autodeskId": "45GPJ4KAX789",
    "name": "John Smith",
    "email": "john.smith@mail.com",
    "userType": "PROJECT_ADMIN",
    "subjectType": "USER",
    "subjectStatus": "ACTIVE",
    "actions": [
      "PUBLISH"
    ],
    "inheritActions": [
      "PUBLISH"
    ]
  }
]


以下是ISSUES-V2 API：
Documentation /BIM 360 API /API Reference
Issues Profile
GET	users/me
Returns the current user permissions in the current project.

This operation is available to every valid member of this project.

Note that this endpoint is ONLY compatible with BIM 360 projects. It is not compatible with Autodesk Construction Cloud (ACC) projects. For more information about compatibility between between BIM 360 and ACC, see the Compatibility section.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/issues/v2/containers/:containerId/users/me
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
containerId
string
The ID of the container.
Each project is assigned to a container that stores all the issues for the project.

Use the Data Management API to retrieve the container ID. For more information, see the Retrieve Issues Container ID tutorial.

Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
Invalid input
401
Unauthorized
The supplied Authorization header was not valid. Verify Authentication and try again
403
Forbidden
The request was successfully validated but permission is not granted
404
Not Found
Container not found
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
The permission level of the user in the current project.
You can also verify a user’s assignment permissions by checking the permittedActions or permissionLevels attributes.

Each permission level corresponds to a combination of values in the response.

View All: read - Can view the ‘data:read’ only endpoints.
Create: create - Can create for my company.
View and Create: read, create - Can create for other companies.
Full control: create, read, write - Can manage issues.
Possible values: create, read, write

Example
Success

Request
curl -v 'https://developer.api.autodesk.com/issues/v2/containers/a5f49f04-59bb-477c-97e6-6833cb50bdac/users/me' \
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
        "open"
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
    }
  },
  "permissionLevels": [
    "read"
  ]

  Documentation /BIM 360 API /API Reference
Issue Types
GET	containers/{containerId}/issue-types
Retrieves a project’s issue types. To also include issue subtypes in the response, use the include=subtypes query string parameter.

This operation is available to every valid member of this project.

Note that by default this endpoint will not return deleted items.

Note that this endpoint is ONLY compatible with BIM 360 projects. It is not compatible with Autodesk Construction Cloud (ACC) projects. For more information about compatibility between between BIM 360 and ACC, see the Compatibility section.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/issues/v2/containers/:containerId/issue-types
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
containerId
string
The ID of the container.
Each project is assigned to a container that stores all the issues for the project.

Use the Data Management API to retrieve the container ID. For more information, see the Retrieve Issues Container ID tutorial.

Request
Query String Parameters
include
string
Add include=subtypes to add the subtypes for each type.
limit
int
Add limit=20 to limit the results count, maximum limit - limit=200 (together with the offset to support pagination).
offset
int
Add offset=20 to get partial results (together with the limit to support pagination).
filter[updatedAt]
string
Retrieves types that were last updated at the specified date and time range, in one of the following URL-encoded formats: YYYY-MM-DDThh:mm:ss.sz or YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03 or 2022-02-28T22:00:00.000Z..2022-03-28T22:00:00.000Z
Specific day: e.g., 2022-03-02 or 2022-02-28T22:00:00.000Z
Specific start date: e.g., 2022-03-02.. or 2022-02-28T22:00:00.000Z..
Specific end date: e.g., ..2022-03-02 or ..2022-02-28T22:00:00.000Z
For more details, see JSON API Filtering.

filter[deletedAt]
string
Retrieves types that were last deleted at the specified date and time range, in one of the following URL-encoded formats: YYYY-MM-DDThh:mm:ss.sz or YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03 or 2022-02-28T22:00:00.000Z..2022-03-28T22:00:00.000Z
Specific day: e.g., 2022-03-02 or 2022-02-28T22:00:00.000Z
Specific start date: e.g., 2022-03-02.. or 2022-02-28T22:00:00.000Z..
Specific end date: e.g., ..2022-03-02 or ..2022-02-28T22:00:00.000Z
To include non-deleted items in the response, add null to the filter: filter[deletedAt]=null,YYYY-MM-DDThh:mm:ss.sz..YYYY-MM-DDThh:mm:ss.sz.

For more details, see JSON API Filtering.

filter[isActive]
boolean
Filter types by status, e.g. filter[isActive]=true will only return active types. Default value: undefined (meaning both active & inactive issue types will return).
Response
HTTP Status Code Summary
200
OK
List of issue types
400
Bad Request
Invalid input
401
Unauthorized
The supplied Authorization header was not valid. Verify Authentication and try again
403
Forbidden
The request was successfully validated but permission is not granted
404
Not Found
Container not found
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
curl -v 'https://developer.api.autodesk.com/issues/v2/containers/a5f49f04-59bb-477c-97e6-6833cb50bdac/issue-types?include=subtypes&limit=20&offset=20&filter[isActive]=true' \
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
          "id": "1110f111-6c54-4b01-90e6-d701748f1111",
          "issueTypeId": "2220f222-6c54-4b01-90e6-d701748f0222",
          "title": "Clash",
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
      "statusSet": "bim360",
      "createdBy": "A3RGM375QTZ7",
      "createdAt": "2018-07-22T15:05:58.033Z",
      "updatedBy": "A3RGM375QTZ7",
      "updatedAt": "2018-07-22T15:05:58.033Z",
      "deletedBy": "A3RGM375QTZ7",
      "deletedAt": "2018-07-22T15:05:58.033Z"
    }
  ]
}

Documentation /BIM 360 API /API Reference
Issue Attribute Definitions
GET	containers/{containerId}/issue-attribute-definitions
Retrieves information about issue custom attributes for a project, including the custom attribute title, description and type.

For example, the possible values for a dropdown list, the IDs, the names and whether the attribute is visible.

Note that this endpoint is ONLY compatible with BIM 360 projects. It is not compatible with Autodesk Construction Cloud (ACC) projects. For more information about compatibility between between BIM 360 and ACC, see the Compatibility section.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/issues/v2/containers/:containerId/issue-attribute-definitions
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
containerId
string
The ID of the container.
Each project is assigned to a container that stores all the issues for the project.

Use the Data Management API to retrieve the container ID. For more information, see the Retrieve Issues Container ID tutorial.

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
Retrieves items that were last created at the specified date and time range, in one of the following URL-encoded formats: YYYY-MM-DDThh:mm:ss.sz or YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03 or 2022-02-28T22:00:00.000Z..2022-03-28T22:00:00.000Z
Specific day: e.g., 2022-03-02 or 2022-02-28T22:00:00.000Z
Specific start date: e.g., 2022-03-02.. or 2022-02-28T22:00:00.000Z..
Specific end date: e.g., ..2022-03-02 or ..2022-02-28T22:00:00.000Z
For more details, see JSON API Filtering.

filter[updatedAt]
datetime: ISO 8601
Retrieves items that were last updated at the specified date and time range, in one of the following URL-encoded formats: YYYY-MM-DDThh:mm:ss.sz or YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03 or 2022-02-28T22:00:00.000Z..2022-03-28T22:00:00.000Z
Specific day: e.g., 2022-03-02 or 2022-02-28T22:00:00.000Z
Specific start date: e.g., 2022-03-02.. or 2022-02-28T22:00:00.000Z..
Specific end date: e.g., ..2022-03-02 or ..2022-02-28T22:00:00.000Z
For more details, see JSON API Filtering.

filter[deletedAt]
datetime: ISO 8601
Retrieves items that were last deleted at the specified date and time range, in one of the following URL-encoded formats: YYYY-MM-DDThh:mm:ss.sz or YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03 or 2022-02-28T22:00:00.000Z..2022-03-28T22:00:00.000Z
Specific day: e.g., 2022-03-02 or 2022-02-28T22:00:00.000Z
Specific start date: e.g., 2022-03-02.. or 2022-02-28T22:00:00.000Z..
Specific end date: e.g., ..2022-03-02 or ..2022-02-28T22:00:00.000Z
To include non-deleted items in the response, add null to the filter: filter[deletedAt]=null,YYYY-MM-DDThh:mm:ss.sz..YYYY-MM-DDThh:mm:ss.sz.

For more details, see JSON API Filtering.

filter[dataType]
enum:string
Retrieves issue custom attribute definitions with the specified data type. Possible values: list, text, paragraph, numeric. For example, filter[dataType]=text,numeric.
Response
HTTP Status Code Summary
200
OK
List of issue attribute definitions
400
Bad Request
Invalid input
401
Unauthorized
The supplied Authorization header was not valid. Verify Authentication and try again
403
Forbidden
The request was successfully validated but permission is not granted
404
Not Found
Container not found
Response
Body Structure (200)
 Expand all
pagination
object
The pagination object.
results
array: object
A list of issue attribute definitions.
Example
List of issue attribute definitions

Request
curl -v 'https://developer.api.autodesk.com/issues/v2/containers/a5f49f04-59bb-477c-97e6-6833cb50bdac/issue-attribute-definitions?filter[dataType]=text' \
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
      "isRequiredDefault": false,
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

ocumentation /BIM 360 API /API Reference
Issue Attribute Mappings
GET	containers/{containerId}/issue-attribute-mappings
Retrieves information about the issue custom attributes that are assigned to issue categories and issue types.

Note that by default, this endpoint only retrieves custom attributes that were directly assigned to the issue category or issue type. It does not retrieve inherited custom attributes.

Note that this endpoint is ONLY compatible with BIM 360 projects. It is not compatible with Autodesk Construction Cloud (ACC) projects. For more information about compatibility between between BIM 360 and ACC, see the Compatibility section.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/issues/v2/containers/:containerId/issue-attribute-mappings
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
containerId
string
The ID of the container.
Each project is assigned to a container that stores all the issues for the project.

Use the Data Management API to retrieve the container ID. For more information, see the Retrieve Issues Container ID tutorial.

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
Retrieves items that were last created at the specified date and time range, in one of the following URL-encoded formats: YYYY-MM-DDThh:mm:ss.sz or YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03 or 2022-02-28T22:00:00.000Z..2022-03-28T22:00:00.000Z
Specific day: e.g., 2022-03-02 or 2022-02-28T22:00:00.000Z
Specific start date: e.g., 2022-03-02.. or 2022-02-28T22:00:00.000Z..
Specific end date: e.g., ..2022-03-02 or ..2022-02-28T22:00:00.000Z
For more details, see JSON API Filtering.

filter[updatedAt]
datetime: ISO 8601
Retrieves items that were last updated at the specified date and time range, in one of the following URL-encoded formats: YYYY-MM-DDThh:mm:ss.sz or YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03 or 2022-02-28T22:00:00.000Z..2022-03-28T22:00:00.000Z
Specific day: e.g., 2022-03-02 or 2022-02-28T22:00:00.000Z
Specific start date: e.g., 2022-03-02.. or 2022-02-28T22:00:00.000Z..
Specific end date: e.g., ..2022-03-02 or ..2022-02-28T22:00:00.000Z
For more details, see JSON API Filtering.

filter[deletedAt]
datetime: ISO 8601
Retrieves items that were last deleted at the specified date and time range, in one of the following URL-encoded formats: YYYY-MM-DDThh:mm:ss.sz or YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03 or 2022-02-28T22:00:00.000Z..2022-03-28T22:00:00.000Z
Specific day: e.g., 2022-03-02 or 2022-02-28T22:00:00.000Z
Specific start date: e.g., 2022-03-02.. or 2022-02-28T22:00:00.000Z..
Specific end date: e.g., ..2022-03-02 or ..2022-02-28T22:00:00.000Z
To include non-deleted items in the response, add null to the filter: filter[deletedAt]=null,YYYY-MM-DDThh:mm:ss.sz..YYYY-MM-DDThh:mm:ss.sz.

For more details, see JSON API Filtering.

filter[attributeDefinitionId]
string
Retrieves issue custom attribute mappings associated with the specified issue custom attribute definitions. Separate multiple values with commas. For example: filter[attributeDefinitionId]=18ee5858-cbf1-451a-a525-7c6ff8156775.
filter[mappedItemId]
string
Retrieves issue custom attribute mappings associated with the specified items (container, type, or subtype). Separate multiple values with commas. For example: filter[mappedItemId]=18ee5858-cbf1-451a-a525-7c6ff8156775.
filter[isRequired]
string
Retrieves issue custom attribute mappings associated with custom attributes that are either required or not required. Possible values: true, false. For example: filter[isRequired]=true.
Response
HTTP Status Code Summary
200
OK
List of issue attribute mappings
400
Bad Request
Invalid input
401
Unauthorized
The supplied Authorization header was not valid. Verify Authentication and try again
403
Forbidden
The request was successfully validated but permission is not granted
404
Not Found
Container not found
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
curl -v 'https://developer.api.autodesk.com/issues/v2/containers/a5f49f04-59bb-477c-97e6-6833cb50bdac/issue-attribute-mappings?filter[attributeDefinitionId]=18ee5858-cbf1-451a-a525-7c6ff8156775&filter[mappedItemId]=18ee5858-cbf1-451a-a525-7c6ff81567aa&filter[isRequired]=true' \
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
      "attributeDefinitionId": "1110f111-6c54-4b01-90e6-d701748f1333",
      "mappedItemType": "issueType",
      "mappedItemId": "2220f222-6c54-4b01-90e6-d701748f0222",
      "order": 2,
      "isRequired": false,
      "permittedActions": [
        "delete"
      ],
      "permittedAttributes": [
        "isRequired"
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
Documentation /BIM 360 API /API Reference
Issue Root Cause Categories
GET	containers/{containerId}/issue-root-cause-categories
Retrieves a list of supported root cause categories and root causes that you can allocate to an issue. For example, Coordination, Design, Quality and Safety.

Note that by default, this endpoint only returns root cause categories. To include root causes you need to add the include query string parameter (include=rootcauses).

Note that this endpoint is ONLY compatible with BIM 360 projects. It is not compatible with Autodesk Construction Cloud (ACC) projects. For more information about compatibility between between BIM 360 and ACC, see the Compatibility section.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/issues/v2/containers/:containerId/issue-root-cause-categories
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
containerId
string
The ID of the container.
Each project is assigned to a container that stores all the issues for the project.

Use the Data Management API to retrieve the container ID. For more information, see the Retrieve Issues Container ID tutorial.

Request
Query String Parameters
include
string
Add include=rootcauses to add the root causes for each category.
limit
int
Add limit=20 to limit the results count (together with the offset to support pagination).
offset
int
Add offset=20 to get partial results (together with the limit to support pagination).
filter[updatedAt]
string
Retrieves root cause categories that were last updated at the specified date and time range, in in one of the following URL-encoded formats: YYYY-MM-DDThh:mm:ss.sz or YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
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
401
Unauthorized
The supplied Authorization header was not valid. Verify Authentication and try again
403
Forbidden
The request was successfully validated but permission is not granted
404
Not Found
Container not found
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
curl -v 'https://developer.api.autodesk.com/issues/v2/containers/a5f49f04-59bb-477c-97e6-6833cb50bdac/issue-root-cause-categories?include=rootcauses&limit=20&offset=20' \
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


Documentation /BIM 360 API /API Reference
Issues
GET	containers/{containerId}/issues
Retrieves information about all the issues in a project, including count of the associated comments and attachments.

Note that this endpoint is ONLY compatible with BIM 360 projects. It is not compatible with Autodesk Construction Cloud (ACC) projects. For more information about compatibility between between BIM 360 and ACC, see the Compatibility section.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/issues/v2/containers/:containerId/issues
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
containerId
string
The ID of the container.
Each project is assigned to a container that stores all the issues for the project.

Use the Data Management API to retrieve the container ID. For more information, see the Retrieve Issues Container ID tutorial.

Request
Query String Parameters
filter[id]
string
Filter issues by the unique issue ID. Separate multiple values with commas
filter[qualityUrns]
string
Filter issues by quality URNs (for example checklist). Separate multiple values with commas.
filter[issueTypeId]
string
Filter issues by the unique identifier of the type of the issue. Separate multiple values with commas
filter[issueSubtypeId]
string
Filter issues by the unique identifier of the subtype of the issue. Separate multiple values with commas
filter[status]
string
Filter issues by the unique identifier of the current status of the issue. Separate multiple values with commas
filter[linkedDocumentUrn]
array: string
Filter issues by linked file/document URN’s. Separate multiple values with commas. To filter by maximum version, add “@[version-number]” after the urn. For example, to retrieve the issues of 2 file/document URN’s, use filter[linkedDocumentUrn]=urn%3Aadsk.wipstg%3Adm.lineage%3A7RBfH69GTuuhXnzG5e4oew%2Curn%3Aadsk.wipstg%3Adm.lineage%3A-Rv5HsqqRwiGCM72YhmnOA@1
filter[dueDate]
string
Filter issues by due date, in the following URL-encoded format: YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03
Specific day: e.g., 2022-03-03
Specific start date: e.g., 2022-03-02..
Specific end date: e.g., ..2022-03-02
For more details, see JSON API Filtering.

filter[createdAt]
datetime: ISO 8601
Filter issues that were last created at specified date and time, in one of the following URL-encoded formats: YYYY-MM-DDThh:mm:ss.sz or YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03 or 2022-02-28T22:00:00.000Z..2022-03-28T22:00:00.000Z
Specific day: e.g., 2022-03-02 or 2022-02-28T22:00:00.000Z
Specific start date: e.g., 2022-03-02.. or 2022-02-28T22:00:00.000Z..
Specific end date: e.g., ..2022-03-02 or ..2022-02-28T22:00:00.000Z
For more details, see JSON API Filtering.

filter[clientCreatedAt]
datetime: ISO 8601
Filter issues that were last client created at specified date and time, in one of the following URL-encoded formats: YYYY-MM-DDThh:mm:ss.sz or YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03 or 2022-02-28T22:00:00.000Z..2022-03-28T22:00:00.000Z
Specific day: e.g., 2022-03-02 or 2022-02-28T22:00:00.000Z
Specific start date: e.g., 2022-03-02.. or 2022-02-28T22:00:00.000Z..
Specific end date: e.g., ..2022-03-02 or ..2022-02-28T22:00:00.000Z
For more details, see JSON API Filtering.

filter[createdBy]
array: string
Filter issues by the unique identifier of the user who created the issue. Separate multiple values with commas
filter[openedAt]
datetime: ISO 8601
Filter issues that were last opened at specified date and time, in one of the following URL-encoded formats: YYYY-MM-DDThh:mm:ss.sz or YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03 or 2022-02-28T22:00:00.000Z..2022-03-28T22:00:00.000Z
Specific day: e.g., 2022-03-02 or 2022-02-28T22:00:00.000Z
Specific start date: e.g., 2022-03-02.. or 2022-02-28T22:00:00.000Z..
Specific end date: e.g., ..2022-03-02 or ..2022-02-28T22:00:00.000Z
For more details, see JSON API Filtering.

filter[openedBy]
array: string
Filter issues by the unique identifier of the user who opened the issue. Separate multiple values with commas
filter[updatedAt]
datetime: ISO 8601
Filter issues that were last updated at specified date and time, in one of the following URL-encoded formats: YYYY-MM-DDThh:mm:ss.sz or YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03 or 2022-02-28T22:00:00.000Z..2022-03-28T22:00:00.000Z
Specific day: e.g., 2022-03-02 or 2022-02-28T22:00:00.000Z
Specific start date: e.g., 2022-03-02.. or 2022-02-28T22:00:00.000Z..
Specific end date: e.g., ..2022-03-02 or ..2022-02-28T22:00:00.000Z
For more details, see JSON API Filtering.

filter[clientUpdatedAt]
datetime: ISO 8601
Filter issues that were last client updated at specified date and time, in one of the following URL-encoded formats: YYYY-MM-DDThh:mm:ss.sz or YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03 or 2022-02-28T22:00:00.000Z..2022-03-28T22:00:00.000Z
Specific day: e.g., 2022-03-02 or 2022-02-28T22:00:00.000Z
Specific start date: e.g., 2022-03-02.. or 2022-02-28T22:00:00.000Z..
Specific end date: e.g., ..2022-03-02 or ..2022-02-28T22:00:00.000Z
For more details, see JSON API Filtering.

filter[updatedBy]
array: string
Filter issues by the unique identifier of the user who updated the issue. Separate multiple values with commas
filter[assignedTo]
array: string
Filter issues by the unique identifier of the current assignee of this issue. Separate multiple values with commas
filter[rootCauseId]
array: string: uuid
Filter issues by the unique identifier of the type of root cause for the issue. Separate multiple values with commas
filter[locationId]
array: string: uuid
Filter issues by the unique LBS (Location Breakdown Structure) identifier that relates to the issue. Separate multiple values with commas
filter[subLocationId]
array: string: uuid
Filter issues by the unique LBS (Location Breakdown Structure) identifier that relates to the issue and retreives also all issues with sub locations. Separate multiple values with commas
filter[closedBy]
array: string
Filter issues by the unique identifier of the user who closed the issue. Separate multiple values with commas
filter[closedAt]
datetime: ISO 8601
Filter issues that were last closed at specified date and time, in one of the following URL-encoded formats: YYYY-MM-DDThh:mm:ss.sz or YYYY-MM-DD. Separate multiple values with commas. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03 or 2022-02-28T22:00:00.000Z..2022-03-28T22:00:00.000Z
Specific day: e.g., 2022-03-02 or 2022-02-28T22:00:00.000Z
Specific start date: e.g., 2022-03-02.. or 2022-02-28T22:00:00.000Z..
Specific end date: e.g., ..2022-03-02 or ..2022-02-28T22:00:00.000Z
For more details, see JSON API Filtering.

filter[search]
string
Filter issues using ‘search’ criteia. this will filter both title and issues display Id. For example, use filter[search]=300
filter[displayId]
int
Filter issues by the chronological user-friendly identifier. Separate multiple values with commas
filter[assignedToType]
string
Filter issues by the type of the current assignee of this issue. Separate multiple values with commas
filter[ownerId]
string
Filter issues by the user who owns this issue. Separate multiple values with commas
filter[customAttributes]
array: string
Filter issues by the custom attributes. Each custom attribute filter should be defined by it’s uuid. For example, filter[customAttributes][f227d940-ae9b-4722-9297-389f4411f010]=1,2,3. Separate multiple values with commas.
limit
int
Return specified number of issues. Acceptable values are 1-100. Default value is 100
offset
int
Return issues starting from the specified offset number. Default value is 0
sort
array: string
Sort issues by specified fields. Separate multiple values with commas. To sort in descending order add a - before the sort criteria. For example, sortBy=status,-displayId,-dueDate,customAttributes[5c07cbe2-256a-48f1-b35b-2e5e00914104]
fields
array: string
Return only specific fields in issue object. Separate multiple values with commas. Fields which will be returned in any case: id, title, status, issueTypeId, ownerId
Response
HTTP Status Code Summary
200
OK
Returns all issues in combination with pagination details
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers. The client SHOULD NOT repeat the request without modifications. The response body may give an indication of what is wrong with the request
401
Unauthorized
The supplied Authorization header was not valid. Verify Authentication and try again
403
Forbidden
The request was successfully validated but permission is not granted
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
Returns all issues in combination with pagination details

Request
curl -v 'https://developer.api.autodesk.com/issues/v2/containers/a5f49f04-59bb-477c-97e6-6833cb50bdac/issues?filter[id]=a5f49f04-59bb-477c-97e6-6833cb50bdac,a5f49f04-59bb-477c-97e6-6833cb50b123&filter[qualityUrns]=urn:some.checklist.urn.3,urn:some.checklist.urn.1&filter[issueTypeId]=a5f49f04-59bb-477c-97e6-6833cb50bdac,a5f49f04-59bb-477c-97e6-6833cb50b123&filter[issueSubtypeId]=a5f49f04-59bb-477c-97e6-6833cb50bdac,a5f49f04-59bb-477c-97e6-6833cb50b123&filter[status]=a5f49f04-59bb-477c-97e6-6833cb50bdac,a5f49f04-59bb-477c-97e6-6833cb50b123' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": "",
    "offset": "",
    "totalResults": ""
  },
  "results": [
    {
      "id": "3570f222-6c54-4b01-90e6-e701749f0222",
      "containerId": "2220f222-6c54-4b01-90e6-d701748f0222",
      "displayId": 7,
      "title": "Door missing a screw",
      "description": "The door is missing a screw, please fix this",
      "snapshotUrn": "",
      "snapshotWipUrn": "",
      "issueTypeId": "8770f222-6c54-4e01-93e6-e701749f0222",
      "issueSubtypeId": "1370f222-6c54-3a01-93e6-e701749f0222",
      "status": "open",
      "assignedTo": "A3RGM375QTZ7",
      "assignedToType": "user",
      "dueDate": "2018-07-25",
      "locationId": "35de6f24-39f5-4808-ba5f-6cbbe2a858e1",
      "locationDetails": "issue location details",
      "linkedDocuments": [
        {
          "type": "TwoDVectorPushpin",
          "urn": "urn:adsk.wipprod:dm.lineage:0C9edNQuT2SrfoyKQ1Gv_Q",
          "createdBy": "",
          "createdAt": "",
          "createdAtVersion": 1,
          "closedBy": "",
          "closedAt": "",
          "closedAtVersion": 1,
          "details": {
            "viewable": {
              "id": "",
              "name": "",
              "is3D": "",
              "guid": "",
              "viewableId": ""
            },
            "position": {
              "x": "",
              "y": "",
              "z": ""
            },
            "objectId": "",
            "externalId": "",
            "viewerState": {}
          }
        }
      ],
      "links": [
        {
          "type": "checklist",
          "data": {
            "urn1": "urn:adsk.checklists.cs.instance:f0aa1265-ecf1-4fe6-b192-dcebf34be020/505",
            "urn2": "urn:adsk.checklists.cs.instance:f0aa1265-ecf1-4fe6-b192-dcebf34be021/506"
          }
        }
      ],
      "ownerId": "owner Id",
      "rootCauseId": "2370f222-6c54-3a01-93e6-f701772f0222",
      "officialResponse": {
        "response": "",
        "respondedAt": "",
        "respondedBy": ""
      },
      "issueTemplateId": "",
      "permittedStatuses": [
        "open"
      ],
      "permittedAttributes": [
        "title"
      ],
      "permittedActions": {},
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
      "clientCreatedAt": "2000-02-04T09:44:58.867Z",
      "clientUpdatedAt": "2000-02-04T09:44:58.867Z",
      "customAttributes": [
        {
          "attributeDefinitionId": "2220f222-6c54-4b01-90e6-d701748f0888",
          "value": "fast",
          "type": "numeric",
          "title": "Secondary Title"
        }
      ]
    }
  ]
}

Documentation /BIM 360 API /API Reference
Issues
GET	containers/{containerId}/issues/{issueId}
Retrieves detailed information about a single issue. For general information about all the issues in a project, see GET issues.

Note that this endpoint is ONLY compatible with BIM 360 projects. It is not compatible with Autodesk Construction Cloud (ACC) projects. For more information about compatibility between between BIM 360 and ACC, see the Compatibility section.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/issues/v2/containers/:containerId/issues/:issueId
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
containerId
string
The ID of the container.
Each project is assigned to a container that stores all the issues for the project.

Use the Data Management API to retrieve the container ID. For more information, see the Retrieve Issues Container ID tutorial.

issueId
string
The unique issue ID
Response
HTTP Status Code Summary
200
OK
Returns the requested issue
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers. The client SHOULD NOT repeat the request without modifications. The response body may give an indication of what is wrong with the request
401
Unauthorized
The supplied Authorization header was not valid. Verify Authentication and try again
403
Forbidden
The request was successfully validated but permission is not granted
404
Not Found
Container or Issue not found
Response
Body Structure (200)
 Expand all
id
string: UUID
The unique identifier of the issue.
containerId
string: UUID
The unique identifier of the container issue is part of
displayId
int
The chronological user-friendly identifier of the issue
title
string
The title of the issue.
Max length: 4200

description
string
The description and purpose of the issue.
Max length: 10000

snapshotUrn
string
Not relevant
snapshotWipUrn
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
The unique identifier of the current status of the issue Possible values: draft, open, work_completed, ready_to_inspect, in_dispute, not_approved, answered, void, closed
assignedTo
string
The unique Autodesk ID of the User/Company/Role of the current assignee for this issue. Note that if you select an assignee ID, you also need to select a type (assignedToType).
assignedToType
enum:string
The type of the current assignee of this issue. Possible values: user, company, role, null.
dueDate
string
The due date of the issue, in ISO8601 format.
locationId
string: UUID
The unique LBS (Location Breakdown Structure) identifier that relates to the issue.
locationDetails
string
The location as plain text that relates to the issue.
Max length: 8300

linkedDocuments
array: object
The list of files/documents related to this issue with specific details depending on the type of relationship. Currently linkedDocuments can contain only one item at maximum.
links
array: object
A collection of links to checklists. For example, a list of resource URN’s in the Checklist service that this issue is related to.
To filter by links use the filter[qualityUrns].

Hint, currently links can contain only one item at maximum.

ownerId
string
The unique identifier of the user who owns this issue. Used in case this issue was created on-behalf of another person
Max length: 100

rootCauseId
string: UUID
The unique identifier of the type of root cause for the issue.
officialResponse
object
The official response of the user for the issue
issueTemplateId
string: UUID
Not relevant
permittedStatuses
array: string
A list of statuses accessible to the current user, this is based on the current status of the issue and the user permissions.
Possible Values: draft, open, work_completed, ready_to_inspect, in_dispute, not_approved, answered, void, closed.

permittedAttributes
array: string
A list of attributes the current user can manipulate in the current context. issueTypeId, linkedDocument, links, ownerId, officialResponse, rootCauseId, snapshotUrn are not applicable.
Possible Values: title, description, issueTypeId, issueSubtypeId, status, assignedTo, assignedToType, dueDate, locationId, locationDetails, linkedDocuments, links, ownerId, rootCauseId, officialResponse, customAttributes, clientUpdatedAt, snapshotUrn.

permittedActions
object
The list of actions permitted for the user for this issue in its current state.
Possible Values: assign_all, assign_same_company, assign_creator_or_owner, clear_assignee, add_comment, add_attachment, remove_attachment.

The following values are not relevant: add_attachment, remove_attachment.

commentCount
int
The number of comments in this issue.
attachmentCount
int
The number of attachments added to this issue
openedBy
string
The unique identifier of the user who opened the issue.
openedAt
datetime: ISO 8601
The date and time the issue was opened, in ISO8601 format.
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
clientCreatedAt
datetime: ISO 8601
Not relevant
clientUpdatedAt
datetime: ISO 8601
Not relevant
customAttributes
array: object
A list of custom attributes of the specific issue.
Example
Returns the requested issue

Request
curl -v 'https://developer.api.autodesk.com/issues/v2/containers/a5f49f04-59bb-477c-97e6-6833cb50bdac/issues/a5f49f04-59bb-477c-97e6-6833cb50bdac' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "id": "3570f222-6c54-4b01-90e6-e701749f0222",
  "containerId": "2220f222-6c54-4b01-90e6-d701748f0222",
  "displayId": 7,
  "title": "Door missing a screw",
  "description": "The door is missing a screw, please fix this",
  "snapshotUrn": "",
  "snapshotWipUrn": "",
  "issueTypeId": "8770f222-6c54-4e01-93e6-e701749f0222",
  "issueSubtypeId": "1370f222-6c54-3a01-93e6-e701749f0222",
  "status": "open",
  "assignedTo": "A3RGM375QTZ7",
  "assignedToType": "user",
  "dueDate": "2018-07-25",
  "locationId": "35de6f24-39f5-4808-ba5f-6cbbe2a858e1",
  "locationDetails": "issue location details",
  "linkedDocuments": [
    {
      "type": "TwoDVectorPushpin",
      "urn": "urn:adsk.wipprod:dm.lineage:0C9edNQuT2SrfoyKQ1Gv_Q",
      "createdBy": "",
      "createdAt": "",
      "createdAtVersion": 1,
      "closedBy": "",
      "closedAt": "",
      "closedAtVersion": 1,
      "details": {
        "viewable": {
          "id": "",
          "name": "",
          "is3D": "",
          "guid": "",
          "viewableId": ""
        },
        "position": {
          "x": "",
          "y": "",
          "z": ""
        },
        "objectId": "",
        "externalId": "",
        "viewerState": {}
      }
    }
  ],
  "links": [
    {
      "type": "checklist",
      "data": {
        "urn1": "urn:adsk.checklists.cs.instance:f0aa1265-ecf1-4fe6-b192-dcebf34be020/505",
        "urn2": "urn:adsk.checklists.cs.instance:f0aa1265-ecf1-4fe6-b192-dcebf34be021/506"
      }
    }
  ],
  "ownerId": "owner Id",
  "rootCauseId": "2370f222-6c54-3a01-93e6-f701772f0222",
  "officialResponse": {
    "response": "",
    "respondedAt": "",
    "respondedBy": ""
  },
  "issueTemplateId": "",
  "permittedStatuses": [
    "open"
  ],
  "permittedAttributes": [
    "title"
  ],
  "permittedActions": {},
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
  "clientCreatedAt": "2000-02-04T09:44:58.867Z",
  "clientUpdatedAt": "2000-02-04T09:44:58.867Z",
  "customAttributes": [
    {
      "attributeDefinitionId": "2220f222-6c54-4b01-90e6-d701748f0888",
      "value": "fast",
      "type": "numeric",
      "title": "Secondary Title"
    }
  ]
}

Documentation /BIM 360 API /API Reference
Issue Comments
GET	containers/{containerId}/issues/{issueId}/comments
Get all the comments for a specific issue.

Note that this endpoint is ONLY compatible with BIM 360 projects. It is not compatible with Autodesk Construction Cloud (ACC) projects. For more information about compatibility between between BIM 360 and ACC, see the Compatibility section.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/issues/v2/containers/:containerId/issues/:issueId/comments
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
containerId
string
The ID of the container.
Each project is assigned to a container that stores all the issues for the project.

Use the Data Management API to retrieve the container ID. For more information, see the Retrieve Issues Container ID tutorial.

issueId
string
The unique issue ID
Request
Query String Parameters
limit
int
Add limit=20 to limit the results count, maximum limit - limit=200 (together with the offset to support pagination).
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
401
Unauthorized
The supplied Authorization header was not valid. Verify Authentication and try again
403
Forbidden
The request was successfully validated but permission is not granted
404
Not Found
Container or Issue not found
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
curl -v 'https://developer.api.autodesk.com/issues/v2/containers/a5f49f04-59bb-477c-97e6-6833cb50bdac/issues/a5f49f04-59bb-477c-97e6-6833cb50bdac/comments?limit=20&offset=20' \
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
      "body": "Hey Aharon, please validate that this is even possible before starting to work on the issue.",
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

Documentation /BIM 360 API /API Reference
Issue Attachments
GET	containers/{containerId}/issues/{issueId}/attachments
Get all attachments (by default will not return deleted attachments).

Note that this endpoint is ONLY compatible with BIM 360 projects. It is not compatible with Autodesk Construction Cloud (ACC) projects. For more information about compatibility between between BIM 360 and ACC, see the Compatibility section.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/issues/v2/containers/:containerId/issues/:issueId/attachments
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
containerId
string
The ID of the container.
Each project is assigned to a container that stores all the issues for the project.

Use the Data Management API to retrieve the container ID. For more information, see the Retrieve Issues Container ID tutorial.

issueId
string
The unique issue ID
Request
Query String Parameters
filter[status]
string
Filter attachments by status. Separate multiple values with commas
limit
int
Add limit=20 to limit the results count, maximum limit - limit=200 (together with the offset to support pagination).
offset
int
Add offset=20 to get partial results (together with the limit to support pagination).
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
Invalid ID supplied
401
Unauthorized
The supplied Authorization header was not valid. Verify Authentication and try again
403
Forbidden
The request was successfully validated but permission is not granted
404
Not Found
Container or Issue not found
Response
Body Structure (200)
 Expand all
pagination
object
The pagination object.
results
array: object
Example
Success

Request
curl -v 'https://developer.api.autodesk.com/issues/v2/containers/a5f49f04-59bb-477c-97e6-6833cb50bdac/issues/a5f49f04-59bb-477c-97e6-6833cb50bdac/attachments?filter[status]=file-uploaded,completed&limit=20&offset=20' \
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
      "issueId": "1110f111-6c54-4b01-90e6-d701748f1111",
      "name": "Darth Vader",
      "urn": "urn:adsk.wipqa:fs.folder:co.LymIC3w5SEOE6jXChqmkqg",
      "createdBy": "A3RGM375QTZ7",
      "updatedBy": "A3RGM375QTZ7",
      "deletedBy": "A3RGM375QTZ7",
      "createdAt": "2018-07-22T15:05:58.033Z",
      "updatedAt": "2018-07-22T15:05:58.033Z",
      "deletedAt": "2018-07-22T15:05:58.033Z",
      "markupMetadata": {},
      "attachmentType": "photo",
      "status": "completed",
      "clientCreatedAt": "A3RGM375QTZ7",
      "clientUpdatedAt": "2018-07-22T15:05:58.033Z",
      "urnType": "dm",
      "wipUrn": {},
      "permittedActions": [
        "remove_attachment"
      ],
      "permittedAttributes": [
        "name"
      ],
      "urnVersion": 1
    }
  ]
}


Documentation /BIM 360 API /API Reference
nodes
GET	v2/containers/{containerId}/trees/{treeId}/nodes
Retrieves the locations (nodes) for a project using the location breakdown structure (tree). To retrieve the path of a location, use the filter.

You configure the locations in BIM 360 Project Admin. For information about locations, see the BIM 360 help documentation.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/locations/v2/containers/:containerId/trees/:treeId/nodes
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
region
string
Specifies the region where the service is located. Possible values: US, EMEA.
* Required
Request
URI Parameters
containerId
string: UUID
The container ID. To find the ID, see the Retrieve a container ID tutorial.
treeId
string
Must be default. Currently you can only add one tree (default) to a container.
Request
Query String Parameters
filter[id]
array: string
Retrieves information about a specified node (location) in the tree. To retrieve multiple nodes, separate values with commas. For example, filter[id]=88e07ccb-4594-4dc5-8973-304412b8fa96,de9aca33-5e0c-4668-85fa-f96273db4b35. Note that the response includes the path of the node in the tree.
To find the node ID, call this endpoint and check the value for results.id.

Note that when you use this parameter, the server ignores the offset and limit parameters, and the response includes the path of the node in the tree.

limit
int
The maximum number of nodes per page. Acceptable values: 1-10000. Default value: 10000.
offset
int
The node index from which the pagination starts. This is zero-based.
Response
HTTP Status Code Summary
200
OK
Succeeded
400
Bad Request
Bad request
403
Forbidden
Forbidden. The caller has no permission to perform this operation.
404
Not Found
The specified container or tree was not found.
Response
Body Structure (200)
 Expand all
pagination
object
results
array: object
Example
Succeeded

Request
curl -v 'https://developer.api.autodesk.com/bim360/locations/v2/containers/:containerId/trees/:treeId/nodes' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 3,
    "offset": 0,
    "totalResults": 7,
    "nextUrl": "/locations/v2/containers/4a327b27-897c-4e5a-8e48-6e01c21377f3/trees/default/nodes?limit=3&offset=3"
  },
  "results": [
    {
      "id": "5add4375-f223-4201-88b9-8049e68416aa",
      "parentId": null,
      "type": "Root",
      "name": "Project",
      "description": "Project description",
      "barcode": null,
      "order": 0,
      "documentCount": 0,
      "areaDefined": false
    },
    {
      "id": "d14ce3a6-e61b-4ab0-a9be-5acf7b5366df",
      "parentId": "5add4375-f223-4201-88b9-8049e68416aa",
      "type": "Area",
      "name": "Area 1",
      "description": "An Area 1 node",
      "barcode": "ABC123",
      "order": 0,
      "documentCount": 2,
      "areaDefined": true
    },
    {
      "id": "8da1faf2-a72f-421b-89df-00d77e545faf",
      "parentId": "5add4375-f223-4201-88b9-8049e68416aa",
      "type": "Area",
      "name": "Area 2",
      "description": "An Area 2 node",
      "barcode": "DEF456",
      "order": 1,
      "documentCount": 3,
      "areaDefined": true
    }
  ]
}


以下是MODEL COORDINATION:

Documentation /BIM 360 API /API Reference
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

Documentation /BIM 360 API /API Reference
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

Documentation /BIM 360 API /API Reference
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

Documentation /BIM 360 API /API Reference
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

Documentation /BIM 360 API /API Reference
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

Documentation /BIM 360 API /API Reference
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



Documentation /BIM 360 API /API Reference
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


Documentation /BIM 360 API /API Reference
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

Documentation /BIM 360 API /API Reference
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
Documentation /BIM 360 API /API Reference
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

Documentation /BIM 360 API /API Reference
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
Documentation /BIM 360 API /API Reference
Clash Test
GET	containers/:containerId/modelsets/:modelSetId/versions/:version/tests
Retrieves a list of summaries for all clash tests that have been executed for a given model set version. If no tests have yet been completed for the specified model set version, no tests are returned.

The response contains a list of matching clash test summaries, restricted by the number specified by the pageLimit property. If set (that is, if there are more results than can be displayed at once), you can provide the continuationToken property in the response in a separate call to retrieve additional results.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/clash/v3/containers/:containerId/modelsets/:modelSetId/versions/:version/tests
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
curl -v 'https://developer.api.autodesk.com/bim360/clash/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911/versions/42/tests' \
     -H 'Authorization: Bearer <token>'
Example #2 (with all query parameters)
Request
curl -v 'https://developer.api.autodesk.com/bim360/clash/v3/containers/f0f4f36a-ac64-687f-b132-8efe04b22454/modelsets/00fb28a5-e8a4-2755-562a-7c2f0fc87911/versions/42/tests?status=Success&pageLimit=134&continuationToken=10' \
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

Documentation /BIM 360 API /API Reference
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
Documentation /BIM 360 API /API Reference
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
補充：還有寫clash相關api沒記錄下來。

Model Properties api ：
Documentation /BIM 360 API /API Reference
Index
GET	projects/:projectId/indexes/:indexId/fields
Retrieve a specific fields dictionary associated with a properties index. Since the fields dictionary, once created, is immutable, the response will set a long expiration HTTP header for efficient client side caching.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/index/v2/projects/:projectId/indexes/:indexId/fields
Authentication Context	
user context required
Required OAuth Scopes	
data:read
Data Format	
json.gz
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
projectId
string: UUID
The project ID.
indexId
string
The index ID.
Response
HTTP Status Code Summary
200
OK
The response is provided in the [line-delimited JSON streaming format (LDJSON)](https://de.wikipedia.org/wiki/JSON_streaming) with the definition of one field per line.
303
Redirect Method
The response is provided in the [line-delimited JSON streaming format (LDJSON)](https://de.wikipedia.org/wiki/JSON_streaming) with the definition of one field per line.
401
Unauthorized
Response in case of an error.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
429
Too Many Requests
Rate limit exceeded. Wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
key
string
The unique identifier for the attribute in file version.
category
string
The property database attribute category, can be null.
type
enum: string
field data type.
Possible values: Unknown, Boolean, Integer, Double, Blob, DbKey, String, LocalizableString, DateTime, GeoLocation, Position

name
string
The property database attribute name.
uom
string
The property database attribute data type context or unit of measurement, e.g., “m”, “ft”, “m^2”, “kip/inch^2”.
Response
Body Structure (303)
key
string
The unique identifier for the attribute in file version.
category
string
The property database attribute category, can be null.
type
enum: string
field data type.
Possible values: Unknown, Boolean, Integer, Double, Blob, DbKey, String, LocalizableString, DateTime, GeoLocation, Position

name
string
The property database attribute name.
uom
string
The property database attribute data type context or unit of measurement, e.g., “m”, “ft”, “m^2”, “kip/inch^2”.
Response
Body Structure (401)
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
curl -v 'https://developer.api.autodesk.com/construction/index/v2/projects/cd743656-f130-48bd-96e6-948175313637/indexes/da39a3ee5e6b4b0d/fields' \
     -H 'Authorization: Bearer <token>'
Response (200)
{
  "key": "p8e7b8610",
  "category": "Materials and Finishes",
  "type": "Double",
  "name": "Concrete compression",
  "uom": "kip/inch^2"
}
Response (303)
{
  "key": "p8e7b8610",
  "category": "Materials and Finishes",
  "type": "Double",
  "name": "Concrete compression",
  "uom": "kip/inch^2"
}
Response (401)
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

Documentation /BIM 360 API /API Reference
Index
GET	projects/:projectId/indexes/:indexId/manifest
Retrieve a specific manifest associated with a properties index. Since the manifest, once created, is immutable, the response will set a long expiration HTTP header for efficient client side caching.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/index/v2/projects/:projectId/indexes/:indexId/manifest
Authentication Context	
user context required
Required OAuth Scopes	
data:read
Data Format	
json
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
projectId
string: UUID
The project ID.
indexId
string
The index ID.
Response
HTTP Status Code Summary
200
OK
Returns the index manifest
401
Unauthorized
Response in case of an error.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
429
Too Many Requests
Rate limit exceeded. Wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
schema
enum: string
current schema version.
Possible values: 2.0.0

projectId
string: UUID
project ID.
status
enum: string
manifest status.
Possible values: Failed, Running, Succeeded

createdAt
datetime: ISO 8601
creation timestamp.
seedFiles
array: object
seed files.
errors
array: object
errors.
stats
array: object
High level statistics about the diff index
Response
Body Structure (401)
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
curl -v 'https://developer.api.autodesk.com/construction/index/v2/projects/cd743656-f130-48bd-96e6-948175313637/indexes/da39a3ee5e6b4b0d/manifest' \
     -H 'Authorization: Bearer <token>'
Response (200)
{
  "schema": "2.0.0",
  "projectId": "d88f5314-90c3-4ccd-9460-810097580b12",
  "status": "Succeeded",
  "createdAt": "2020-06-30T06:43:51.391Z",
  "seedFiles": [
    {
      "lineageId": "344b06a3",
      "lineageUrn": "urn:adsk.wipstg:dm.lineage:-7p38avKTMGWp2vcCW568Q",
      "versionUrn": "urn:adsk.wipstg:fs.file:vf.-7p38avKTMGWp2vcCW568Q?version=2",
      "databases": [
        {
          "id": "b834bb65",
          "offsets": "urn:adsk.viewing:fs.file:dXJuOmFkc2sud2lwc3RnOmZzLmZpbGU6dmYuLTdwMzhhdktUTUdXcDJ2Y0NXNTY4UT92ZXJzaW9uPTI/output/Resource/objects_offs.json.gz",
          "attributes": "urn:adsk.viewing:fs.file:dXJuOmFkc2sud2lwc3RnOmZzLmZpbGU6dmYuLTdwMzhhdktUTUdXcDJ2Y0NXNTY4UT92ZXJzaW9uPTI/output/Resource/objects_attrs.json.gz",
          "values": "urn:adsk.viewing:fs.file:dXJuOmFkc2sud2lwc3RnOmZzLmZpbGU6dmYuLTdwMzhhdktUTUdXcDJ2Y0NXNTY4UT92ZXJzaW9uPTI/output/Resource/objects_vals.json.gz",
          "mapping": "urn:adsk.viewing:fs.file:dXJuOmFkc2sud2lwc3RnOmZzLmZpbGU6dmYuLTdwMzhhdktUTUdXcDJ2Y0NXNTY4UT92ZXJzaW9uPTI/output/Resource/objects_avs.json.gz",
          "ids": "urn:adsk.viewing:fs.file:dXJuOmFkc2sud2lwc3RnOmZzLmZpbGU6dmYuLTdwMzhhdktUTUdXcDJ2Y0NXNTY4UT92ZXJzaW9uPTI/output/Resource/objects_ids.json.gz"
        }
      ],
      "views": [
        {
          "id": "cf7900d3",
          "urn": "urn:adsk.wipstg:fs.file:vf.-7p38avKTMGWp2vcCW568Q?version=2",
          "is3d": "true",
          "viewableName": "{3D}",
          "viewableId": "845097d1-c3be-4a6f-9dbe-51582fa6d465-002c2f04",
          "viewableGuid": "5d41dda7-eea1-eff5-77dd-ee1aa81fc3a8"
        },
        {
          "id": "7ca0051c",
          "urn": "urn:adsk.wipstg:fs.file:vf.-7p38avKTMGWp2vcCW568Q?version=2",
          "is3d": "false",
          "viewableName": "New Construction",
          "viewableId": "c884ae1b-61e7-4f9d-0001-719e20b22d0b-0032d30d",
          "viewableGuid": "8ac4ddd7-61f9-c4fa-a216-d771f8ed260a"
        }
      ]
    }
  ],
  "errors": []
}
Show Less
Response (401)
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

Documentation /BIM 360 API /API Reference
Index
GET	projects/:projectId/indexes/:indexId/properties
Retrieve the specific properties index. Since the properties index, once created, is immutable, the response will set a long expiration HTTP header for efficient client side caching.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/index/v2/projects/:projectId/indexes/:indexId/properties
Authentication Context	
user context required
Required OAuth Scopes	
data:read
Data Format	
json.gz
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
projectId
string: UUID
The project ID.
indexId
string
The index ID.
Response
HTTP Status Code Summary
200
OK
The response is provided in the [line-delimited JSON streaming format (LDJSON)](https://de.wikipedia.org/wiki/JSON_streaming) with the properties of one object per line.
303
Redirect Method
The response is provided in the [line-delimited JSON streaming format (LDJSON)](https://de.wikipedia.org/wiki/JSON_streaming) with the properties of one object per line.
401
Unauthorized
Response in case of an error.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
429
Too Many Requests
Rate limit exceeded. Wait some time before retrying. The Retry-After header might provide the amount of the time to wait.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
lmvId
int
Object database id from the original seed file property database (_objects_id.id).
dbId
string
Property database id (the property database the object originated from).
props
object
Property database property keyed values.
propsHash
string
Hash used to determine whether object properties have changed between different versions.
propsIgnored
object
Property database property values that are not considered for property change tracking.
geomHash
string
Hash used to determine whether the object geometry has changed between different versions.
bboxMin
object
Minimum [x, y, z]-coords of the 3D-bbox.
bboxMax
object
Maximum [x, y, z]-coords of the 3D-bbox.
views
array: string
List of corresponding view IDs in the index manifest that this object is visible in.
svf2Id
int
The stable SVF2 ID of the object.
lineageId
string
The lineage ID of the object; the (svf2Id, lineageId)-pair allows to track a specific object across several versions.
externalId
string
The external ID of the object.
Response
Body Structure (303)
lmvId
int
Object database id from the original seed file property database (_objects_id.id).
dbId
string
Property database id (the property database the object originated from).
props
object
Property database property keyed values.
propsHash
string
Hash used to determine whether object properties have changed between different versions.
propsIgnored
object
Property database property values that are not considered for property change tracking.
geomHash
string
Hash used to determine whether the object geometry has changed between different versions.
bboxMin
object
Minimum [x, y, z]-coords of the 3D-bbox.
bboxMax
object
Maximum [x, y, z]-coords of the 3D-bbox.
views
array: string
List of corresponding view IDs in the index manifest that this object is visible in.
svf2Id
int
The stable SVF2 ID of the object.
lineageId
string
The lineage ID of the object; the (svf2Id, lineageId)-pair allows to track a specific object across several versions.
externalId
string
The external ID of the object.
Response
Body Structure (401)
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
curl -v 'https://developer.api.autodesk.com/construction/index/v2/projects/cd743656-f130-48bd-96e6-948175313637/indexes/da39a3ee5e6b4b0d/properties' \
     -H 'Authorization: Bearer <token>'
Response (200)
{
  "svf2Id": "1510",
  "lineageId": "344b06a3",
  "externalId": "546a5f5b-1aeb-43f9-b1f2-530ebe1e4c4a-0032d24c",
  "lmvId": "5721",
  "dbId": "455c17b4",
  "props": {
    "p00723fa6": "Main Model",
    "p01bbdcf2": "FIRST FLOOR",
    "p08bc1e88": "0",
    "p10f4572e": "505.527528165408",
    "p153cb174": "CONCESSION/ NATURE STORE 115 [991729]",
    "p188478f2": "0",
    "p1d45bc4f": "4",
    "p20d8441e": "Rooms",
    "p29ff6f58": "115",
    "p5264cd49": "1",
    "p532f0ad6": "New Construction",
    "p562c91d5": "8",
    "p5eddc473": "Revit Rooms",
    "p6ab86626": "FIRST FLOOR",
    "p78f04c1e": "99.54644577473422",
    "pa7275c45": "-2000160",
    "pb2959cb7": "0",
    "pc838ff15": "OCCUPANCY",
    "pdf772b6f": "CONCESSION/ NATURE STORE",
    "pe2ac2e1d": "8",
    "pef87fde6": "0"
  },
  "propsHash": "46681c9a",
  "propsIgnored": {
    "p93e93af5": "5599"
  },
  "geomHash": "c9f2684f",
  "bbox": {
    "min": [
      "-54.80051040649414",
      "1.0369148254394531",
      "-5.971645355224609"
    ],
    "max": [
      "-33.66492462158203",
      "31.324600219726562",
      "2.0283546447753906"
    ]
  },
  "views": [
    "7ca0051c"
  ]
}
Show Less
Response (303)
{
  "svf2Id": "1510",
  "lineageId": "344b06a3",
  "externalId": "546a5f5b-1aeb-43f9-b1f2-530ebe1e4c4a-0032d24c",
  "lmvId": "5721",
  "dbId": "455c17b4",
  "props": {
    "p00723fa6": "Main Model",
    "p01bbdcf2": "FIRST FLOOR",
    "p08bc1e88": "0",
    "p10f4572e": "505.527528165408",
    "p153cb174": "CONCESSION/ NATURE STORE 115 [991729]",
    "p188478f2": "0",
    "p1d45bc4f": "4",
    "p20d8441e": "Rooms",
    "p29ff6f58": "115",
    "p5264cd49": "1",
    "p532f0ad6": "New Construction",
    "p562c91d5": "8",
    "p5eddc473": "Revit Rooms",
    "p6ab86626": "FIRST FLOOR",
    "p78f04c1e": "99.54644577473422",
    "pa7275c45": "-2000160",
    "pb2959cb7": "0",
    "pc838ff15": "OCCUPANCY",
    "pdf772b6f": "CONCESSION/ NATURE STORE",
    "pe2ac2e1d": "8",
    "pef87fde6": "0"
  },
  "propsHash": "46681c9a",
  "propsIgnored": {
    "p93e93af5": "5599"
  },
  "geomHash": "c9f2684f",
  "bbox": {
    "min": [
      "-54.80051040649414",
      "1.0369148254394531",
      "-5.971645355224609"
    ],
    "max": [
      "-33.66492462158203",
      "31.324600219726562",
      "2.0283546447753906"
    ]
  },
  "views": [
    "7ca0051c"
  ]
}
Show Less
Response (401)
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

還有很多model properties相關的index 和 diff沒有記錄，需要時候再提示。

以下是relatonships 相關API：

Documentation /BIM 360 API /API Reference
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

Documentation /BIM 360 API /API Reference
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
Show More
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

Documentation /BIM 360 API /API Reference
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

Documentation /BIM 360 API /API Reference
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

Documentation /BIM 360 API /API Reference
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

Documentation /BIM 360 API /API Reference
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
Show Less
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

Documentation /BIM 360 API /API Reference
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

以下是RFIS API:

Documentation /BIM 360 API /API Reference
RFIs
GET	rfis
Retrieves information about all the BIM 360 RFIs (requests for information) in a project, including details about their associated comments and attachments. To get more detailed information about a single RFI see GET rfis/:id.

You can retrieve both document-related (pusphin) RFIs and project-related RFIs.

To verify whether an RFI is document-related (pusphin) or project-related, check the linkedDocument attribute in the response. If the RFI is project-related the linkedDocument will be assigned a null value, if the RFI is document-related, it will be assigned an ID.

BIM 360 RFIs are managed in the BIM 360 Project Management module.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/rfis/v2/containers/:containerId/rfis
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
containerId
string
The ID of the container. Each project is assigned a container that stores all the RFIs for the project. To find the ID, see the Retrieve a Container ID tutorial.
Request
Query String Parameters
limit
int
The number of RFIs to return in the response payload. Acceptable values: 1-200. Default value: 10. For example, to limit the response to two RFIs per page, use limit=2
offset
int
The page number that you want to begin RFI results from. For example, to begin the results from page three, use offset=3
sort
array: string
Sort the RFIs by createdAt, status, dueDate, title, location, updatedAt, costImpact, scheduleImpact, priority, discipline, category, reference, customIdentifier. For example, sort=status ASC. Separate multiple values with commas. To sort in descending order add a DESC after the sort criteria. For example, sort=status DESC.
filter[status]
array: string
Retrieves RFIs with the specified status. Possible values: draft, submitted, open, rejected, answered, closed & void. For example, filter[status]=open
filter[includeHidden]
boolean
Not relevant
filter[linkedDocument]
array: string
Retrieves pushpin RFIs that are associated with the specified document. Specify the document’s item ID. For example, filter[linkedDocument]=urn:adsk.wipprod:dm.lineage:tFbo9zuDTW-nPh45gnM4gA.
filter[linkedDocumentVersion]
int
Retrieves pushpin RFIs that are associated with the specified document. Specify the document’s version ID. For example, filter[linkedDocument]=urn:adsk.wipprod:fs.file:7_5NcbL1Q1GSjRLJe9ffvw&filter[linkedDocumentVersion]=1.
filter[assignedTo]
array: string
Retrieves RFIs in the project that were assigned to the specified user. Use the user’s Autodesk ID. For example, filter[assignedTo]=PER8KQPK2JRT. To find the ID call GET users/me and check user.id.
filter[createdAt]
string
Retrieves RFIs created after the specfied date, in the following format: YYYY-MM-DDThh:mm:ss.sz, or a date range in the following format: YYYY-MM-DDThh:mm:ss.sz..YYYY-MM-DDThh:mm:ss.sz.
filter[createdBy]
array: string
Retrieves RFIs in the project that were created by the specified user. Use the user’s Autodesk ID. For example, filter[createdBy]=PER8KQPK2JRT. To find the ID call GET users/me and check user.id.
filter[dueDate]
string
Retrieves RFIs with the specified due date, in the following format: YYYY-MM-DDThh:mm:ss.sz, or a date range in the following format: YYYY-MM-DDThh:mm:ss.sz..YYYY-MM-DDThh:mm:ss.sz.
filter[search]
string
Searches for a specified string in the following fields: title, question, and officialResponse, and retrieves RFIs where the string is found. This includes RFIs where the string matches part of a field. For example, filter[search]=window.
filter[costImpact]
array: string
Retrieves RFIs with the specified cost impact value. For example, filter[costImpact]=Yes
filter[scheduleImpact]
array: string
Retrieves RFIs with the specified schedule impact value. For example, filter[scheduleImpact]=Yes
filter[priority]
array: string
Retrieves RFIs with the specified priority level. For example, filter[priority]=High
filter[id]
array: string
Retrieves a list of specified RFIs. To find the RFI IDs call GET rfis and check results.id.
filter[discipline]
array: string
Retrieves RFIs with the specified discipline type. For example, filter[discipline]=Architectural
filter[category]
array: string
Retrieves RFIs with the specified category type. For example, filter[category]=Constructability
fields
array: string
Specify which attributes you want to appear in the response. Separate multiple values with commas. For example, fields=createdBy, question.
Response
HTTP Status Code Summary
200
OK
List of rfis
400
Bad Request
The parameters are invalid
401
Unauthorized
The provided bearer token is not valid
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation
500
Internal Server Error
An unknown error occurred on the server
Response
Body Structure (200)
 Expand all
results
array: object
The list of RFIs.
pagination
object
The pagination object.
Example
List of rfis

Request
curl -v 'https://developer.api.autodesk.com/bim360/rfis/v2/containers/:containerId/rfis' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "results": [
    {
      "id": "31a3f98d-34a8-4d4c-a362-3cc9de44f89c",
      "customIdentifier": "ID-1234",
      "title": "RFI - pipe is not in right place",
      "question": "Where should we put the pipe?",
      "virtualFolderUrn": "",
      "status": "open",
      "assignedTo": "PER8KQPK2JRT",
      "managerId": "PER8KQPK2JRT",
      "constructionManagerId": "PER8KQPK2JRT",
      "architectId": "PER8KQPK2JRT",
      "reviewerId": "PER8KQPK2JRT",
      "assignedToType": "user",
      "dueDate": "2018-01-12T13:06:39.216Z",
      "location": {
        "description": "In the middle of the room"
      },
      "linkedDocument": "2018-01-12T13:06:39.216Z",
      "linkedDocumentVersion": "urn:adsk.wipprod:fs.file:7_5NcbL1Q1GSjRLJe9ffvw",
      "linkedDocumentCloseVersion": 1,
      "attachmentsCount": 12,
      "commentsCount": 15,
      "officialResponse": "The measurements are correct.",
      "respondedAt": "2018-01-12T13:06:39.216Z",
      "respondedBy": "PER8KQPK2JRT",
      "createdBy": "PER8KQPK2JRT",
      "createdAt": "2018-07-22T15:05:58.033Z",
      "updatedBy": "PER8KQPK2JRT",
      "updatedAt": "2018-07-22T15:05:58.033Z",
      "closedAt": "2018-07-22T15:05:58.033Z",
      "closedBy": "PER8KQPK2JRT",
      "containerId": "31a3f98d-34a8-4d4c-a362-3cc9de44f89c",
      "projectId": "31a3f98d-34a8-4d4c-a362-3cc9de44f89c",
      "suggestedAnswer": "The measurements are correct.",
      "coReviewers": [
        "PER8KQPK2JRT"
      ],
      "distributionList": [
        "PER8KQPK2JRT"
      ],
      "answeredAt": "2018-07-22T15:05:58.033Z",
      "answeredBy": "PER8KQPK2JRT",
      "costImpact": "Yes",
      "scheduleImpact": "Yes",
      "priority": "High",
      "discipline": [
        "Architectural"
      ],
      "category": [
        "Constructability"
      ],
      "reference": "ID-1234",
      "sheetMetadata": "",
      "pushpinAttributes": ""
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "totalResults": 97
  }
}

Documentation /BIM 360 API /API Reference
RFIs
GET	rfis/:id
Retrieves detailed information about a single BIM 360 RFI (request for information), including the type of workflow roles assigned to the user, whether the user is permitted to create RFIs, which states the user can create the RFIs in, and the attributes that are required when creating the RFIs in the different states. For general information about all the RFIs in a project, see GET rfis.

We strongly recommend calling this endpoint before updating RFIs, in order to verify the most up-to-date permissions and actions.

You can retrieve both document-related (pusphin) RFIs and project-related RFIs.

To verify whether an RFI is document-related (pushpin) or project-related, check the linkedDocument attribute in the response. If the RFI is project-related the linkedDocument will not have a value, if the RFI is document-related, it will be assigned an ID.

BIM 360 RFIs are managed in the BIM 360 Project Management module.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/rfis/v2/containers/:containerId/rfis/:rfiId
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
containerId
string
The ID of the container. Each project is assigned a container that stores all the RFIs for the project. To find the ID, see the Retrieve a Container ID tutorial.
rfiId
string
The ID of the RFI.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters are invalid
401
Unauthorized
The provided bearer token is not valid
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation
404
Not Found
RFI not found
500
Internal Server Error
An unknown error occurred on the server
Response
Body Structure (200)
 Expand all
id
string
The ID of the RFI.
customIdentifier
string
The identifier of the RFI given by user.
title
string
The name of the RFI.
question
string,null
The RFI question.
virtualFolderUrn
string,null
Not relevant
status
enum:string
The status of the RFI. Note that the possible statuses of the RFI depends on the workflow type assigned to the RFI.
For a default workflow with a single reviewer (US), you can potentially use the following statuses: draft, submitted, open, answered, rejected, closed, void. For a workflow with an additional reviewer (EMEA), you can potentially use the following statuses: draft, submitted, openRev1,, openRev2, rejectedRev1`, rejectedManager, answeredRev1, answeredManager, closed, void.

For more information about different workflows and statuses, see the RFI help documentation.

To check the workflow type of an RFI, call GET users/me and check workflow.type.

To check which statuses the user can potentially open the RFI with, call GET rfis/:id. Possible values: draft, submitted, open, openRev1, openRev2, rejected, rejectedRev1, rejectedManager, answered, answeredRev1, answeredManager, closed, void

assignedTo
string
The Autodesk ID of the user.
Max length: 255

managerId
string
The Autodesk ID of the user.
Max length: 255

constructionManagerId
string
The Autodesk ID of the user.
Max length: 255

architectId
string
The Autodesk ID of the user.
Max length: 255

reviewerId
string
The Autodesk ID of the user.
Max length: 255

assignedToType
enum:string
The type of assignee. Will always be user.
dueDate
string,null
The timestamp of the due date for the RFI, in the following format: YYYY-MM-DDThh:mm:ss.sz.
location
object
The location object.
linkedDocument
string
The document ID associated with the RFI. Identifies whether this RFI is a pushpin RFI or a project-related RFI. A pushpin is a visual marker that denotes the location of an RFI in a document. A project-related RFI is assigned a null value, and a pushpin RFI is assigned the item ID of the document associated with the pushpin.
linkedDocumentVersion
int
The document’s version ID associated with the RFI. Only relevant for pushpin RFIs.
linkedDocumentCloseVersion
int
The version of the document when the RFI is closed.
attachmentsCount
int
The number of attachments associated with the RFI.
commentsCount
int
The number of comments associated with the RFI.
officialResponse
string
An official response for the RFI.
respondedAt
datetime: ISO 8601
The date and time when the RFI was responded to, in the following format: YYYY-MM-DDThh:mm:ss.sz.
respondedBy
string
The Autodesk ID of the user who responded to the RFI. To check the name of the user, call GET projects/users.
createdBy
string
The Autodesk ID of the user who created the RFI. To check the name of the user, call GET projects/users.
createdAt
datetime: ISO 8601
The date and time the RFI was created, in the following format: YYYY-MM-DDThh:mm:ss.sz.
updatedBy
string
The Autodesk ID of the user who updated the RFI. To check the name of the user, call GET projects/users.
updatedAt
datetime: ISO 8601
The date and time the RFI was updated, in the following format: YYYY-MM-DDThh:mm:ss.sz.
closedAt
datetime: ISO 8601
The date and time the RFI was closed, in the following format: YYYY-MM-DDThh:mm:ss.sz.
closedBy
string
The Autodesk ID of the user who closed the RFI. To check the name of the user, call GET projects/users.
containerId
string
The ID of the container.
projectId
string
The ID of the project.
suggestedAnswer
string
The suggested answer for the RFI.
coReviewers
array: string
A list of alternative reviewers.
distributionList
array: string
The list of users who will be notified of changes to the RFI.
answeredAt
datetime: ISO 8601
The date and time the RFI was answered, in the following format: YYYY-MM-DDThh:mm:ss.sz.
answeredBy
string
The Autodesk ID of the user who answered the RFI. To check the name of the user, call GET projects/users.
costImpact
string,null
The cost impact status of the RFI. Possible values: null, Yes, No, Unknown.
scheduleImpact
string,null
The schedule impact status of the RFI. Possible values: null, Yes, No, Unknown.
priority
string,null
The priority status of the RFI. Possible values: null, High, Normal, Low.
discipline
array: string
The disciplines of the RFI.
category
array: string
The categories of the RFI.
reference
string
An external ID; typically used when the RFI was created in another system.
Max length: 20

sheetMetadata
object,null
Data about the document associated with the RFI. Only relevant for pushpin RFIs.
pushpinAttributes
object,null
Data about the pushpin RFI. Only relevant for pushpin RFIs. For more details, see the RFI pushpin tutorials.
permittedActions
object
The list of actions that are permitted for the user.
Example
Success

Request
curl -v 'https://developer.api.autodesk.com/bim360/rfis/v2/containers/:containerId/rfis/:rfiId' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "id": "31a3f98d-34a8-4d4c-a362-3cc9de44f89c",
  "customIdentifier": "ID-1234",
  "title": "RFI - pipe is not in right place",
  "question": "Where should we put the pipe?",
  "virtualFolderUrn": "",
  "status": "open",
  "assignedTo": "PER8KQPK2JRT",
  "managerId": "PER8KQPK2JRT",
  "constructionManagerId": "PER8KQPK2JRT",
  "architectId": "PER8KQPK2JRT",
  "reviewerId": "PER8KQPK2JRT",
  "assignedToType": "user",
  "dueDate": "2018-01-12T13:06:39.216Z",
  "location": {
    "description": "In the middle of the room"
  },
  "linkedDocument": "2018-01-12T13:06:39.216Z",
  "linkedDocumentVersion": "urn:adsk.wipprod:fs.file:7_5NcbL1Q1GSjRLJe9ffvw",
  "linkedDocumentCloseVersion": 1,
  "attachmentsCount": 12,
  "commentsCount": 15,
  "officialResponse": "The measurements are correct.",
  "respondedAt": "2018-01-12T13:06:39.216Z",
  "respondedBy": "PER8KQPK2JRT",
  "createdBy": "PER8KQPK2JRT",
  "createdAt": "2018-07-22T15:05:58.033Z",
  "updatedBy": "PER8KQPK2JRT",
  "updatedAt": "2018-07-22T15:05:58.033Z",
  "closedAt": "2018-07-22T15:05:58.033Z",
  "closedBy": "PER8KQPK2JRT",
  "containerId": "31a3f98d-34a8-4d4c-a362-3cc9de44f89c",
  "projectId": "31a3f98d-34a8-4d4c-a362-3cc9de44f89c",
  "suggestedAnswer": "The measurements are correct.",
  "coReviewers": [
    "PER8KQPK2JRT"
  ],
  "distributionList": [
    "PER8KQPK2JRT"
  ],
  "answeredAt": "2018-07-22T15:05:58.033Z",
  "answeredBy": "PER8KQPK2JRT",
  "costImpact": "Yes",
  "scheduleImpact": "Yes",
  "priority": "High",
  "discipline": [
    "Architectural"
  ],
  "category": [
    "Constructability"
  ],
  "reference": "ID-1234",
  "sheetMetadata": "",
  "pushpinAttributes": "",
  "permittedActions": {
    "updateRfi": {
      "permittedStatuses": [
        {
          "status": "open",
          "requiredAttributes": [
            {
              "name": "assignedTo",
              "values": [
                {
                  "value": "PER8KQPK2JRT",
                  "type": "user"
                }
              ]
            }
          ]
        }
      ],
      "permittedAttributes": [
        {
          "name": "assignedTo",
          "values": [
            {
              "value": "PER8KQPK2JRT",
              "type": "user"
            }
          ]
        }
      ]
    },
    "createComment": "",
    "createAttachment": "",
    "linkPCO": "",
    "createDocumentReference": "",
    "removeDocumentReference": "",
    "togglePushpinVisibility": ""
  }
}

Documentation /BIM 360 API /API Reference
RFIs
GET	users/me
Retrieves information about an end user, including the type of workflow roles assigned to the user, whether the user is permitted to create RFIs, which states the user can create the RFIs in, and the attributes that are required when creating the RFIs in the different states.

We strongly recommend calling this endpoint before creating RFIs, in order to verify the most up-to-date permissions and actions.

Users who have been assigned either creator (projectSC) or manager (projectGC) workflow roles can create RFIs. All users in the project are automatically assigned the creator workflow role. To assign creator or manager workflow roles to project members, open the BIM 360 Project Admin module, select the Services tab, and select the Project Management section.

Note that only users who are members of a project can potentially create and edit RFIs for the project. To check which users are members of a project, call GET projects/users. If a user is not a project member, the endpoint will return an error.

If the createRfi object appears in the response in the permittedActions object, it indicates that the user can create RFIs.

Currently, you can only assign workflow roles (creator, manager, reviewer) in the UI. To assign workflow roles, open the BIM 360 Project Admin module, select the Services tab, and select the Project Management section.

The following table describes the Project Admin module workflow role names and the corresponding RFIs API names:

Project Admin Module Workflow Role Name	RFIs API Workflow Role Name
Creator	Subcontractor (projectSC)
Manager	General Contractor (projectGC)
Reviewer 1 (EMEA workflow)	Construction Manager (projectCM)
Reviewer (US workflow) / Reviewer 2 (EMEA workflow)	Architect (projectArch)
For information about RFI workflow role permissions, see the RFIs help documentation.

Currently, you can only select an RFI workflow type for an RFI in the UI. To assign an RFI workflow to an RFI, see the RFIs help documentation

The following table describes the Project Admin module names and the corresponding RFIs API names:

Project Admin Module Workflow Type Name	RFIs API Workflow Type Name
Default Workflow	US
Workflow with Additional Reviewer	EMEA
Note that you can use either type of workflow in the US and in EMEA.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/rfis/v2/containers/:containerId/users/me
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
containerId
string
The ID of the container. Each project is assigned a container that stores all the RFIs for the project. To find the ID, see the Retrieve a Container ID tutorial.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters are invalid
401
Unauthorized
The provided bearer token is not valid
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation
500
Internal Server Error
An unknown error occurred on the server
Response
Body Structure (200)
 Expand all
user
object
User data object
permittedActions
object
The list of actions that are permitted for the user.
workflow
object
The RFIs workflow data object for the user
Example
Success

Request
curl -v 'https://developer.api.autodesk.com/bim360/rfis/v2/containers/:containerId/users/me' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "user": {
    "id": "BZPWJWWWMLSV",
    "name": "Jon Doe",
    "role": "project_admin"
  },
  "permittedActions": {
    "createRfi": {
      "permittedStatuses": [
        {
          "status": "open",
          "requiredAttributes": [
            {
              "name": "assignedTo",
              "values": [
                {
                  "value": "PER8KQPK2JRT",
                  "type": "user"
                }
              ]
            }
          ]
        }
      ]
    }
  },
  "workflow": {
    "roles": [
      "projectSC"
    ],
    "type": "US"
  }
}

Documentation /BIM 360 API /API Reference
Comments
GET	comments
Retrieves all the comments associated with a BIM 360 Project Management RFI.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/rfis/v2/containers/:containerId/rfis/:rfiId/comments
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
containerId
string
The ID of the container. Each project is assigned a container that stores all the RFIs for the project. To find the ID, see the Retrieve a Container ID tutorial.
rfiId
string
The ID of the RFI.
Request
Query String Parameters
limit
int
The number of RFIs to return in the response payload. Acceptable values: 1-200. Default value: 10. For example, to limit the response to two RFIs per page, use limit=2
offset
int
The page number that you want to begin RFI results from. For example, to begin the results from page three, use offset=3
sort
array: string
The fields to sort the list by
fields
array: string
Specify which attributes you want to see in the response. Separate multiple values with commas. For example, fields=title,description.
filter[createdAt]
string
Retrieves comments created after the specfied date, in the following format: YYYY-MM-DDThh:mm:ss.sz, or a date range in the following format: YYYY-MM-DDThh:mm:ss.sz..YYYY-MM-DDThh:mm:ss.sz.
filter[createdBy]
array: string
Retrieves comments that were created by the specified user. Use the user’s Autodesk ID. For example, filter[created]=PER8KQPK2JRT. To find the ID call GET users/me and check user.id.
Response
HTTP Status Code Summary
200
OK
Comment Records
400
Bad Request
The parameters are invalid
401
Unauthorized
The provided bearer token is not valid
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation
404
Not Found
RFI not found
500
Internal Server Error
An unknown error occurred on the server
Response
Body Structure (200)
 Expand all
results
array: object
The list of comments.
pagination
object
The pagination object.
Example
Comment Records

Request
curl -v 'https://developer.api.autodesk.com/bim360/rfis/v2/containers/:containerId/rfis/:rfiId/comments' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "results": [
    {
      "id": "94ce6921-e8f9-4bc5-bf5a-1a8f543a2564",
      "rfiId": "0d302fc6-00a5-45ca-a9df-4427b9247c81",
      "body": "This needs more attention.",
      "createdBy": "PER8KQPK2JRT",
      "createdAt": "2018-08-01T08:56:48.699Z",
      "updatedAt": "2019-08-01T08:56:48.699Z"
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "totalResults": 97
  }
}

Documentation /BIM 360 API /API Reference
Attachments
GET	attachments
Retrieves information about all the attachments in a project associated with a specific BIM 360 Project Management RFI.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/bim360/rfis/v2/containers/:containerId/rfis/:rfiId/attachments
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
containerId
string
The ID of the container. Each project is assigned a container that stores all the RFIs for the project. To find the ID, see the Retrieve a Container ID tutorial.
rfiId
string
The ID of the RFI.
Request
Query String Parameters
limit
int
The number of RFIs to return in the response payload. Acceptable values: 1-200. Default value: 10. For example, to limit the response to two RFIs per page, use limit=2
offset
int
The page number that you want to begin RFI results from. For example, to begin the results from page three, use offset=3
fields
array: string
Specify which attributes you want to see in the response. Separate multiple values with commas. For example, fields=title,description.
filter[includeDeleted]
boolean
Include deleted attachments in the response.
sort
array: string
Sort the attachments by specified attributes. For example, sort=createdAt. Separate multiple values with commas.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters are invalid
401
Unauthorized
The provided bearer token is not valid
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation
500
Internal Server Error
An unknown error occurred on the server
Response
Body Structure (200)
 Expand all
results
array: object
The list of attachments.
pagination
object
The pagination object.
Example
Success

Request
curl -v 'https://developer.api.autodesk.com/bim360/rfis/v2/containers/:containerId/rfis/:rfiId/attachments' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "results": [
    {
      "id": "c911852d-5957-4145-9c8d-e7cfe9d564df",
      "rfiId": "0d302fc6-00a5-45ca-a9df-4427b9247c81",
      "createdAt": "2018-08-01T08:56:48.699Z",
      "updatedAt": "",
      "createdBy": "PER8KQPK2JRT",
      "deletedAt": "2018-08-01T08:56:48.699Z",
      "deletedBy": "PER8KQPK2JRT",
      "name": "Photo.png",
      "url": "null",
      "urn": "urn:adsk.wipprod:dm.lineage:1t7QY9-JSxCB0TLh1qMvFQ",
      "urnType": "dm",
      "attachmentType": "photo",
      "permittedActions": {
        "removeAttachment": ""
      }
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "totalResults": 97
  }
}