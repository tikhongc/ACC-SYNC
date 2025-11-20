Documentation /Autodesk Construction Cloud APIs /API Reference
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

Documentation /Autodesk Construction Cloud APIs /API Reference
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

Documentation /Autodesk Construction Cloud APIs /API Reference
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

Documentation /Autodesk Construction Cloud APIs /API Reference
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

Documentation /Autodesk Construction Cloud APIs /API Reference
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

Documentation /Autodesk Construction Cloud APIs /API Reference
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

Documentation /Autodesk Construction Cloud APIs /API Reference
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

Documentation /Autodesk Construction Cloud APIs /API Reference
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

Documentation /Autodesk Construction Cloud APIs /API Reference
users/:user_id/projects
GET	accounts/{accountId}/users/{userId}/projects
Returns a list of projects for a specified user within an Autodesk Construction Cloud (ACC) or BIM 360 account. Only projects the user participates in will be returned. The calling user must be an account administrator.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/admin/v1/accounts/:accountId/users/:userId/projects
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
userId
string
The ID of the user. To find the ID call GET users. You can use either the ACC ID (id) or the Autodesk ID (autodeskId).
Request
Query String Parameters
filter[id]
array: string: uuid
A list of project IDs to filter by.
fields
array: string
A comma-separated list of user project fields to include in the response. If not specified, all available fields are included by default.
Possible values: accessLevels, accountId, addressLine1, addressLine2, city, constructionType, country, createdAt, classification, deliveryMethod, endDate, imageUrl, jobNumber, latitude, longitude, name, platform, postalCode, projectValue, sheetCount, startDate, stateOrProvince, status, thumbnailImageUrl, timezone, type, updatedAt, contractType and currentPhase.

filter[classification]
array: string
Filters projects by classification. Possible values:
production – Standard production projects. template – Project templates that can be cloned to create production projects. component – Placeholder projects that contain standardized components (e.g., forms) for use across projects. Only one component project is permitted per account. Known as a library in the ACC unified products UI. sample – The single sample project automatically created upon ACC trial setup. Only one sample project is permitted per account.

Max length: 255

filter[name]
string
Filters projects by name. Supports partial matches when used with filterTextMatch. For example filter[name]=ABCco&filterTextMatch=startsWith returns projects whose names start with “ABCco”.
Max length: 255

filter[platform]
array: string
Filters by platform. Possible values: acc (Autodesk Construction Cloud) and bim360 (BIM 360).
Max length: 255

filter[status]
array: string
Filters projects by status. Possible values: active, pending, archived, suspended.
filter[type]
array: string
Filters by project type. To exclude a type, prefix it with - (e.g., -Bridge excludes bridge projects).
Possible values: Airport, Assisted Living / Nursing Home, Bridge, Canal / Waterway, Convention Center, Court House, Data Center, Dams / Flood Control / Reservoirs, Demonstration Project, Dormitory, Education Facility, Government Building, Harbor / River Development, Hospital, Hotel / Motel, Library, Manufacturing / Factory, Medical Laboratory, Medical Office, Military Facility, Mining Facility, Multi-Family Housing, Museum, Oil & Gas,``Plant``, Office, OutPatient Surgery Center, Parking Structure / Garage, Performing Arts, Power Plant, Prison / Correctional Facility, Rail, Recreation Building, Religious Building, Research Facility / Laboratory, Restaurant, Retail, Seaport, Single-Family Housing, Solar Farm, Stadium/Arena, Streets / Roads / Highways, Template Project, Theme Park, Training Project, Transportation Building, Tunnel, Utilities, Warehouse (non-manufacturing), Waste Water / Sewers, Water Supply, Wind Farm.

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

filter[accessLevels]
array: string
Filters projects by user access level. Possible values: projectAdmin, projectMember.
Max length: 255

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
A list of fields to sort the returned user projects by. Multiple sort fields are applied in sequence order — each sort field produces groupings of projects with the same values of that field; the next sort field applies within the groupings produced by the previous sort field.
Each property can be followed by a direction modifier of either asc (ascending) or desc (descending). The default is asc.

Possible values: name (the default), startDate, endDate, type, status, jobNumber, constructionType, deliveryMethod, contractType, currentPhase, createdAt, updatedAt and platform.

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
A list of requested user projects.
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
A list of user projects matching the request criteria.
Example
A list of requested user projects.

Request
curl -v 'https://developer.api.autodesk.com/construction/admin/v1/accounts/d73fc742-4538-401c-8d0f-853b49b750b2/users/6cc15635-2fbd-4f73-afbe-abd833408a1d/projects?filter[id]=39712a51-bd64-446a-9c72-48c4e43d0a0d,d1163421-e7eb-4862-ac15-b33777ba42de&fields=name,platform&filter[classification]=production,sample&filter[name]=Sample Project&filter[platform]=acc,bim360&filter[status]=active,pending&filter[type]=Convention Center,-Bridge&filter[jobNumber]=HP-0002&filter[updatedAt]=2019-06-01T00:00:00.000Z..&filter[accessLevels]=projectAdmin&filterTextMatch=contains&sort=name desc&limit=20' \
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
      "accessLevels": {
        "projectAdmin": true,
        "projectMember": true
      }
    }
  ]
}
Documentation /Autodesk Construction Cloud APIs /API Reference
users/:user_id/products
GET	accounts/{accountId}/users/{userId}/products
Returns a list of ACC products the user is associated with in their assigned projects.

Only account administrators can call this endpoint.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/admin/v1/accounts/:accountId/users/:userId/products
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
userId
string
The ID of the user. To find the ID call GET users. You can use either the ACC ID (id) or the Autodesk ID (autodeskId).
Request
Query String Parameters
filter[projectId]
array: string: uuid
A list of project IDs. Only results where the user is associated with one or more of the specified projects are returned.
filter[key]
array: string
Filters the list of products by product key — a machine-readable identifier for an ACC product (such as docs, build, or cost).
You can specify one or more keys to return only those products the user is associated with.

Example: filter[key]=docs,build

Possible values: accountAdministration, autoSpecs, build, buildingConnected, capitalPlanning, cloudWorksharing, cost, designCollaboration, docs, financials, insight, modelCoordination, projectAdministration, takeoff, and workshopxr.

fields
array: string
List of fields to return in the response. Defaults to all fields.
Possible values: projectIds, name and icon.

sort
array: string
The list of fields to sort by.
Each property can be followed by a direction modifier of either asc (ascending) or desc (descending). The default is asc.

Possible values: name.

Default is the order in database.

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
A list of products associated with the user
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
A list of ACC products the user is associated with.
Example
A list of products associated with the user

Request
curl -v 'https://developer.api.autodesk.com/construction/admin/v1/accounts/d73fc742-4538-401c-8d0f-853b49b750b2/users/6cc15635-2fbd-4f73-afbe-abd833408a1d/products?filter[projectId]=39712a51-bd64-446a-9c72-48c4e43d0a0d,d1163421-e7eb-4862-ac15-b33777ba42de&filter[key]=build,docs&fields=name&sort=name&limit=20' \
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
      "key": "assets",
      "icon": "https://s3.us-east-1.amazonaws.com/product_icon.png",
      "name": "Document Management",
      "projectIds": [
        "3e354e66-ac8b-41dd-9bc1-93fc182c25dd"
      ]
    }
  ]
}


Documentation /Autodesk Construction Cloud APIs /API Reference
users/:user_id/roles
GET	accounts/{accountId}/users/{userId}/roles
Returns the roles assigned to a specific user across the projects they belong to.

Only users with account admin permissions can call this endpoint. To verify a user’s permissions, call GET users.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/admin/v1/accounts/:accountId/users/:userId/roles
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
userId
string
The ID of the user. To find the ID call GET users. You can use either the ACC ID (id) or the Autodesk ID (autodeskId).
Request
Query String Parameters
filter[projectId]
array: string: uuid
A list of project IDs. Only results where the user is associated with one or more of the specified projects are returned.
filter[status]
array: string
Filters roles by their status. Accepts one or more of the following values:
active – The role is currently in use.

inactive – The role has been removed or is no longer in use.

filter[name]
string
Filters roles by name.
By default, this performs a partial match (case-insensitive).

You can control how the match behaves by using the filterTextMatch parameter. For example, to match only names that start with (startsWith), end with (endsWith), or exactly equal (equals) the provided value.

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

fields
array: string
A comma-separated list of response fields to include. Defaults to all fields if not specified.
Use this parameter to reduce the response size by retrieving only the fields you need.

Possible values:

projectIds – Projects where the user holds this role

name – Role name

status – Role status (active or inactive)

key – Internal key used to translate the role name

createdAt – Timestamp when the role was created

updatedAt – Timestamp when the role was last updated

sort
array: string
Sorts the results by one or more fields.
Each field can be followed by a direction modifier:

asc – Ascending order (default)

desc – Descending order

Possible values: name, createdAt, updatedAt.

Default sort: name asc

Example: sort=name,updatedAt desc

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
A list of requested roles associated with the user
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
The requested page of roles associated with the user.
Example
A list of requested roles associated with the user

Request
curl -v 'https://developer.api.autodesk.com/construction/admin/v1/accounts/d73fc742-4538-401c-8d0f-853b49b750b2/users/6cc15635-2fbd-4f73-afbe-abd833408a1d/roles?filter[projectId]=39712a51-bd64-446a-9c72-48c4e43d0a0d,d1163421-e7eb-4862-ac15-b33777ba42de&filter[status]=active&filter[name]=Architect&filterTextMatch=contains&fields=name&sort=name&limit=20' \
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
      "id": "287d5cc2-9008-462c-96e5-c9491db85d97",
      "status": "active",
      "name": "Architect",
      "key": "architect",
      "createdAt": "2018-01-01T12:45:00.000Z",
      "updatedAt": "2019-01-01T12:45:00.000Z",
      "projectIds": [
        "3e354e66-ac8b-41dd-9bc1-93fc182c25dd"
      ]
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
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

Documentation /Autodesk Construction Cloud APIs /API Reference
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

Documentation /Autodesk Construction Cloud APIs /API Reference
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
Documentation /Autodesk Construction Cloud APIs /API Reference
Business Units
GET	business_units_structure
Query all the business units in a specific BIM 360 account.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/hq/v1/accounts/:account_id/business_units_structure
Method and URI（Legacy）	
GET	https://developer.api.autodesk.com/hq/v1/regions/eu/accounts/:account_id/business_units_structure
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
The account ID of the business unit. This corresponds to hub ID in the Data Management API. To convert a hub ID into an account ID you need to remove the “b." prefix. For example, a hub ID of b.c8b0c73d-3ae9 translates to an account ID of c8b0c73d-3ae9.
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
The request could not be completed due to a conflict with the current state of the resource.
422
Unprocessable Entity
The request was unable to be followed due to restrictions
500
Internal Server Error
An unexpected error occurred on the server
Response
Body Structure (200)
A successful response is a business unit, a flat JSON object with the following attributes:

 Expand all
business_units
array:object
Example
Successful Listing of Account Business Units (200)

Request
curl -v 'https://developer.api.autodesk.com/hq/v1/accounts/e3d5ef8d-5c37-4b9d-925d-1e6d24753ace/business_units_structure' \
   -H 'Authorization: Bearer 9ezBnx9Rd5D1xG4KMt6b72T4w0MG'
Response
{
  "business_units":[
   {
     "id": "933df8fd-abb2-4e4e-8f79-95ba2afebc6c",
     "account_id": "e3d5ef8d-5c37-4b9d-925d-1e6d24753ace",
     "parent_id": null,
     "name": "North America",
     "description": "USA, Canada",
     "path": null,
     "created_at": "2016-04-11T03:49:09.176Z",
     "updated_at": "2016-04-11T03:49:09.176Z"
   },
   {
     "id": "fda4ab9e-ab82-4ba9-8d6c-ae7dbd7cee31",
     "account_id": "e3d5ef8d-5c37-4b9d-925d-1e6d24753ace",
     "parent_id": "933df8fd-abb2-4e4e-8f79-95ba2afebc6c",
     "name": "USA Western Region",
     "description": "California, Nevada, Washington",
     "path": "North America",
     "created_at": "2016-04-11T03:49:09.176Z",
     "updated_at": "2016-04-11T03:49:09.176Z"
   }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
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
GET	https://developer.api.autodesk.com/construction/assets/v2/projects/{projectId}/assets
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
The Autodesk Construction Cloud project ID. Must be a UUID or a project ID of the form “b.{UUID}”.
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
curl -v 'https://developer.api.autodesk.com/construction/assets/v2/projects/:projectId/assets?cursorState=eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9&filter[customAttributes]=[object Object]&filter[searchText]=Air Handler&filter[updatedAt]=2020-05-01T06:00:00.000Z..&sort=createdAt asc,clientAssetId desc&includeCustomAttributes=true&includeDeleted=true' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 25,
    "cursorState": "eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9",
    "nextUrl": "https://developer.api.autodesk.com/construction/assets/v1/projects/04605b7a-0c53-421e-8e11-c743e75ac10a/assets?cursorState=eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9"
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

Documentation /Autodesk Construction Cloud APIs /API Reference
Categories
GET	categories
Searches for and returns all specified categories.

This endpoint accepts a set of optional category property filters, then uses supplied filters to search for and return categories within a project that satisfy those filters. If no filters are set, this endpoint returns all categories within a project.

Note that although the endpoint returns pagination fields for API consistency, the endpoint does not support pagination in requests.

To understand the basics of categories, category inheritance, and the Assets settings that define them, see the Assets Field Guide.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/assets/v1/projects/{projectId}/categories
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
The Autodesk Construction Cloud project ID. Must be a UUID or a project ID of the form “b.{UUID}”.
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
curl -v 'https://developer.api.autodesk.com/construction/assets/v1/projects/:projectId/categories?filter[isActive]=true&filter[parentId]=122&filter[maxDepth]=3&filter[updatedAt]=2020-05-01T06:00:00.000Z..&includeUid=true' \
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

Documentation /Autodesk Construction Cloud APIs /API Reference
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
GET	https://developer.api.autodesk.com/construction/assets/v1/projects/{projectId}/status-step-sets
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
The Autodesk Construction Cloud project ID. Must be a UUID or a project ID of the form “b.{UUID}”.
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
curl -v 'https://developer.api.autodesk.com/construction/assets/v1/projects/:projectId/status-step-sets?cursorState=eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9&includeDeleted=true&filter[updatedAt]=2020-05-01T06:00:00.000Z..' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 25,
    "cursorState": "eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9",
    "nextUrl": "https://developer.api.autodesk.com/construction/assets/v1/projects/04605b7a-0c53-421e-8e11-c743e75ac10a/assets?cursorState=eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9"
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

Documentation /Autodesk Construction Cloud APIs /API Reference
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
GET	https://developer.api.autodesk.com/construction/assets/v1/projects/{projectId}/asset-statuses
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
The Autodesk Construction Cloud project ID. Must be a UUID or a project ID of the form “b.{UUID}”.
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
curl -v 'https://developer.api.autodesk.com/construction/assets/v1/projects/:projectId/asset-statuses?cursorState=eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9&includeDeleted=true&filter[updatedAt]=2020-05-01T06:00:00.000Z..' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 25,
    "cursorState": "eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9",
    "nextUrl": "https://developer.api.autodesk.com/construction/assets/v1/projects/04605b7a-0c53-421e-8e11-c743e75ac10a/assets?cursorState=eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9"
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

Documentation /Autodesk Construction Cloud APIs /API Reference
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
GET	https://developer.api.autodesk.com/construction/assets/v1/projects/{projectId}/custom-attributes
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
The Autodesk Construction Cloud project ID. Must be a UUID or a project ID of the form “b.{UUID}”.
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
curl -v 'https://developer.api.autodesk.com/construction/assets/v1/projects/:projectId/custom-attributes?cursorState=eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9&includeDeleted=true&filter[updatedAt]=2020-05-01T06:00:00.000Z..' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 25,
    "cursorState": "eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9",
    "nextUrl": "https://developer.api.autodesk.com/construction/assets/v1/projects/04605b7a-0c53-421e-8e11-c743e75ac10a/assets?cursorState=eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9"
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

Documentation /Autodesk Construction Cloud APIs /API Reference
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
GET	https://developer.api.autodesk.com/construction/assets/v1/projects/{projectId}/categories/{categoryId}/custom-attributes
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
The Autodesk Construction Cloud project ID. Must be a UUID or a project ID of the form “b.{UUID}”.
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
curl -v 'https://developer.api.autodesk.com/construction/assets/v1/projects/:projectId/categories/123/custom-attributes' \
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

Autospecs 是 Autodesk Construction Cloud (ACC) 平台中的一項功能，專門用於自動化處理和管理建築專案的施工規範書 (specifications)。

Documentation /Autodesk Construction Cloud APIs /API Reference
project metadata
GET	projects/{projectId}/metadata
Retrieves Autospecs-related information about the specified ACC project, including details about the project versions and the region.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/autospecs/v1/projects/{projectId}/metadata
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
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b.” prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Response
HTTP Status Code Summary
200
OK
OK
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
projectId
string
The ACC project ID.
region
enum:string
The region of the specification PDFs that were uploaded for this project. Currently, AutoSpecs supports CSI MasterFormat for the United States and Canada. Possible values: USA, Canada, Others
versions
array: object
Information about the versions for the project.
Example
Successful retrieval of project metadata

Request
curl -v 'https://developer.api.autodesk.com/construction/autospecs/v1/projects/:projectId/metadata' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
    "projectId": "06ca50d7-00ee-485e-a4b0-01ff3ffa7977",
    "region": "CANADA",
    "versions": [
        {
            "name": "Issued For Construction",
            "status": "Completed",
            "currentVersion": true,
            "createdAt": "2023-01-04T10:12:45.000Z",
            "updatedAt": "2023-01-17T09:54:27.000Z",
            "id": "2268"
        },
        {
            "name": "Confederation Heights",
            "status": "Completed",
            "currentVersion": false,
            "createdAt": "2022-11-02T05:04:11.000Z",
            "updatedAt": "2022-11-02T05:05:01.000Z",
            "id": "2062"
        }
    ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
smartregister
GET	projects/{projectId}/version/{versionId}/smartregister
Retrieves the submittal logs (Smart Register) that are part of the specification PDFs that were imported into AutoSpecs. Note that before you can access the submittal logs the import of the specification PDFs needs to be complete. To verify the status of the import, call GET metadata and check that the status is Completed.

Note that we do not currently support updating the Smart Register or Smart Register filtering. In addition, we do not currently support the following columns from the UI: Source version, PDF link, Submittal type group, and Date Issued.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/autospecs/v1/projects/{projectId}/version/{versionId}/smartregister
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
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b.” prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

versionId
string
The AutoSpecs version ID of the project. For information about how to find the version ID, see the first few steps of the Retrieve Submittal Log tutorial.
Response
HTTP Status Code Summary
200
OK
OK
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
submittalsHeading
string
The name of the submittal sub section. This is equivalent to Sub section name column in the UI.
divisionCode
string
The division code associated with the submittal. This is the equivalent to the Division column in the UI.
divisionName
string
The division name associated with the submittal. This is equivalent to the name in the Division filter in the UI.
submittalId
string
The index of the submittal in the submittal log. This is the equivalent to the Submittal number column in the UI.
specNumber
string
The CSI specification code of the submittal. This is equivalent to the Section number column in the UI.
specName
string
The CSI specification name of the submittal. This is equivalent of the Section name column in the UI.
submittalDescription
string
The description of the submittal. This is equivalent to the Submittal description column in the UI.
specCategory
enum:string
The type of specification category associated with the submittal. This is equivalent to Submittal type in the UI. Possible values: Test Reports, Shop Drawings, Schedules, Samples, Sample Warranty, Reports, Qualification Data, QUALITY ASSURANCE, Product Data, Performance Data, Mfg. Instructions, Meeting/Conferences, Drawings, Delegated-Design, Certifications, Certificates, Calculations, Attic Stock, Demonstrations, General Warranties, O&M Manuals, Special Warranties, LEED, As-Builts, TESTS AND INSPECTIONS, General, Manufacturers Instructions, Substitutions, Mix Design, Others
targetDate
string
The submittal target date, in ISO 8601 format. This is equivalent to the Target date column in the UI.
userNotes
string
The user notes associcated with the submittal. This is equivalent to the User notes column in the UI.
paraCode
string
The submittal sub section code. This is equivalent to the Sub section number column in the UI.
targetGroup
enum:string
The submittal group associcated with the submittal. This is equivalent to the Submittal group column in the UI. Possible values: ACTION AND INFORMATIONAL, Closeout Submittals, DIVISION 01 REQUIREMENTS, Field Quality Control, Mockups, QUALITY ASSURANCE, TESTS AND INSPECTIONS
versionName
string
The version name provided by the user when creating the version.
Example
Successful retrieval of submittal logs

Request
curl -v 'https://developer.api.autodesk.com/construction/autospecs/v1/projects/:projectId/version/:versionId/smartregister' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
[
  {
    "submittalsHeading": "SHOP DRAWINGS",
    "divisionCode": "03",
    "divisionName": "Concrete",
    "specNumber": "03 20 00",
    "specName": "HEAD OFFICE RENEWAL",
    "submittalDescription": ".1 Submit shop drawings and bar lists in accordance with Section 01 33 00\nSubmittal Procedures. Allow ten working days for shop drawing review before\ncommencing fabrication.\n.2 Indicate on shop drawings, bar bending details, lists, quantities of\nreinforcement and wire mesh, sizes, spacing, locations of reinforcement and\nmechanical splices if approved by Consultant, with identifying code marks to\npermit correct placement without reference to structural drawings. Indicate\nsizes, spacing and locations of chairs, spacers and hangers. Prepare\nreinforcement drawings in accordance with Reinforcing Steel Manual of\nStandard Practice - by Reinforcing Steel Institute of Canada. ANSI/ACI 315\nand ACI 315R, Manual of Engineering and Placing Drawings for Reinforced\nConcrete Structure.\n.3 Indicate &#x28;and detail&#x29; all proposed construction joints.\n.4 Show reinforced concrete and reinforced masonry walls and beams in full\nelevation and detail all bars.\n.5 When requested, for slab construction, show top and bottom layer slab\nreinforcing on separate plans. Detail sections to fully illustrate bar placement\nat dowels, curbs, openings, changes of elevation, beams, stairs, and areas of\ncongested steel, and wherever else required.\n.6 Detail placement of reinforcing where special conditions occur.\n.7 Design and detail lap lengths and bar development lengths to CAN/CSA-A23.1\nand CAN3-A23.3, unless otherwise specified on drawings. Use Class B\ntension splices unless otherwise noted.\n.8 Indicate details for placement of dowels.\n.9 CAD drawings of the Consultant may be used asa background for the\npreparation of shop drawings provided thata license agreement, provided by\nthe Consultant, is signed by the reinforcing trade.",
    "specCategory": "Shop Drawings",
    "targetDate": null,
    "userNotes": null,
    "paraCode": "1.4",
    "targetGroup": "ACTION AND INFORMATIONAL",
    "versionName": "Issued For Construction",
    "specSubmittalNumber": 0,
    "submittalId": "1"
  },
  {
    "submittalsHeading": "SOURCE QUALITY CONTROL",
    "divisionCode": "03",
    "divisionName": "Concrete",
    "specNumber": "03 20 00",
    "specName": "HEAD OFFICE RENEWAL",
    "submittalDescription": "Upon request, provide Consultant with certified copy of mill test report of\nreinforcing steel to be supplied, showing physical and chemical analysis,\ncorresponding to identification tagging of material at the fabrication plant\nprior to commencing reinforcing work.",
    "specCategory": "Test Reports",
    "targetDate": null,
    "userNotes": null,
    "paraCode": "2.3-.1",
    "targetGroup": "QUALITY ASSURANCE",
    "versionName": "Issued For Construction",
    "specSubmittalNumber": 0,
    "submittalId": "2"
  },
  {
    "submittalsHeading": "SOURCE QUALITY CONTROL",
    "divisionCode": "03",
    "divisionName": "Concrete",
    "specNumber": "03 20 00",
    "specName": "HEAD OFFICE RENEWAL",
    "submittalDescription": "Inform Consultant of proposed source of material to be supplied. Unidentified\nreinforcement shall not be allowed.",
    "specCategory": "Quality Assurance",
    "targetDate": null,
    "userNotes": null,
    "paraCode": "2.3-.2",
    "targetGroup": "QUALITY ASSURANCE",
    "versionName": "Issued For Construction",
    "specSubmittalNumber": 0,
    "submittalId": "3"
  }
]

Documentation /Autodesk Construction Cloud APIs /API Reference
requirements
GET	projects/{projectId}/version/{versionId}/requirements
Retrieves the number of submittals for the submittal groups in each submittal section. To retrieve all submittal data from the Smart Register, call GET smartregister.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/autospecs/v1/projects/{projectId}/version/{versionId}/requirements
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
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b.” prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

versionId
string
The AutoSpecs version ID of the project. For information about how to find the version ID, see the first few steps of the Retrieve Submittal Log tutorial.
Response
HTTP Status Code Summary
200
OK
OK
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
divisionCode
string
The division code associated with the submittal. This is the equivalent to the Division column in the UI.
divisionName
string
The division name associated with the submittal. This is equivalent to the name in the Division filter in the UI.
specSections
array: object
A list of specification divisions and groups.
Example
Successful retrieval of the number of submittals for the submittal groups in each submittal section

Request
curl -v 'https://developer.api.autodesk.com/construction/autospecs/v1/projects/:projectId/version/:versionId/requirements' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
[
  {
    "divisionCode": "01",
    "divisionName": "General Requirements",
    "specSections": [
      {
        "specName": "STRUCTURAL TESTS AND SPECIAL INSPECTIONS",
        "specCode": "01 45 33",
        "submittalGroups": [
          {
            "submittalGroup": "DIVISION 01 REQUIREMENTS",
            "total": 4
          }
        ]
      }
    ]
  },
  {
    "divisionCode": "03",
    "divisionName": "Concrete",
    "specSections": [
      {
        "specName": "CONCRETE REINFORCING",
        "specCode": "03 20 00",
        "submittalGroups": [
          {
            "submittalGroup": "ACTION AND INFORMATIONAL",
            "total": 5
          },
          {
            "submittalGroup": "QUALITY ASSURANCE",
            "total": 1
          },
          {
            "submittalGroup": "TESTS AND INSPECTIONS",
            "total": 1
          }
        ]
      }
    ]
  }
]

Documentation /Autodesk Construction Cloud APIs /API Reference
summary
GET	projects/{projectId}/version/{versionId}/submittalsSummary
Retrieves the number of submittals for each submittal group and each submittal type. To retrieve all submittal data from the Smart Register, call GET smartregister

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/autospecs/v1/projects/{projectId}/version/{versionId}/submittalsSummary
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
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b.” prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

versionId
string
The AutoSpecs version ID of the project. For information about how to find the version ID, see the first few steps of the Retrieve Submittal Log tutorial.
Response
HTTP Status Code Summary
200
OK
OK
401
Unauthorized
The provided bearer token is not valid.
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation.
404
Not Found
The requested resource could not be found.
500
Internal Server Error
An unknown error occurred on the server.
Response
Body Structure (200)
 Expand all
submittalGroups
array: object
A list of submittal groups.
Example
Successful retrieval of the number of submittals for each submittal group and each submittal type

Request
curl -v 'https://developer.api.autodesk.com/construction/autospecs/v1/projects/:projectId/version/:versionId/submittalsSummary' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "submittalGroups": [
    {
      "submittalGroupTypes": [
        {
          "submittalType": "LEED",
          "total": 2
        },
        {
          "submittalType": "Mfg. Instructions",
          "total": 1
        },
        {
          "submittalType": "Others",
          "total": 1
        },
        {
          "submittalType": "Product Data",
          "total": 3
        },
        {
          "submittalType": "Qualification Data",
          "total": 1
        },
        {
          "submittalType": "Reports",
          "total": 1
        },
        {
          "submittalType": "Samples",
          "total": 1
        },
        {
          "submittalType": "Shop Drawings",
          "total": 3
        }
      ],
      "submittalGroup": "Action And Informational",
      "total": 13
    },
    {
      "submittalGroup": "Mockups",
      "total": 1
    },
    {
      "submittalGroup": "Quality Assurance",
      "total": 12
    },
    {
      "submittalGroup": "Tests And Inspections",
      "total": 3
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
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

Documentation /Autodesk Construction Cloud APIs /API Reference
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

Documentation /Autodesk Construction Cloud APIs /API Reference
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

Documentation /Autodesk Construction Cloud APIs /API Reference
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

Documentation /Autodesk Construction Cloud APIs /API Reference
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

Documentation /Autodesk Construction Cloud APIs /API Reference
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

Documentation /Autodesk Construction Cloud APIs /API Reference
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

Documentation /Autodesk Construction Cloud APIs /API Reference
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

Documentation /Autodesk Construction Cloud APIs /API Reference
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

以下是文件api：
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

Documentation /Autodesk Construction Cloud APIs /API Reference
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
Show Less
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

Documentation /Autodesk Construction Cloud APIs /API Reference
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

Documentation /Autodesk Construction Cloud APIs /API Reference
Linked Files
GET	construction/rcm/v1/projects/{projectId}/published-versions/{versionId}/linked-files
Retrieves metadata and signed download URLs for a published version of a Revit (RVT) cloud model, whether workshared or non-workshared, and any Revit files linked to it.

You can also use this endpoint to retrieve a temporary download link for a specific published host model version, even if it has no linked models.

This API is only supported for models published after February 7, 2025.

The Authorization header token can be obtained through either the three-legged OAuth flow or the two-legged OAuth flow with user impersonation, which requires the x-user-Id header.

For details on how to use this endpoint, see the Download RVT Files from a Published Model tutorial.

Note that this endpoint is compatible with both BIM 360 and Autodesk Construction Cloud (ACC) projects.
Note that for a 3-legged OAuth flow or for a 2-legged OAuth flow with user impersonation (x-user-id), the user must have at least download permission to the Revit (RVT) cloud model.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/rcm/v1/projects/{projectId}/published-versions/{versionId}/linked-files
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
Must be Bearer <token>, where <token> is obtained via either a two-legged or three-legged OAuth flow.
x-user-id
string
The ID of the user on whose behalf the request is made. This header is only required when using two-legged authentication with user impersonation. It is not needed for three-legged authentication.
By providing this header, the API call is limited to act on behalf of the user specified. The user must have at least download permission to the host model.

Your application can act on behalf of any user who has been authorized in the SaaS Integrations UI. You can only provide the user’s Autodesk ID (autodeskId) as the value of this header.

* Required
Request
URI Parameters
projectId
string
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can provide the project ID with or without the “b." prefix.

Example with prefix: b.563a4c30-e30d-4869-ac02-2a18b6447abe
Example without prefix: 563a4c30-e30d-4869-ac02-2a18b6447abe
versionId
string
The URL-encoded version ID (URN) of the published Revit model version for which you want to retrieve linked files.
When a Cloud Workshared Revit model is published in BIM 360 or the Autodesk Construction Cloud (ACC), a new version ID is created for each published Revit model version.

Every time a model is updated and published, it receives a new unique version ID.

You must provide a version ID to retrieve the linked files for that specific published Revit model version.

To retrieve the latest (tip) version ID, use GET projects/:project_id/folders/:folder_id/contents. To filter out non-cloud workshared Revit files, use the items:autodesk.bim360:C4RModel filter .

To retrieve a specific past version, use GET projects/:project_id/items/:item_id/versions.

For more details about retrieving the version ID, see the Retrieve Signed URLs for Linked RVT Files tutorial.

Request
Query String Parameters
limit
int
The maximum number of linked models to return in a single request. Maxium: 600. Default: 600.
offset
int
The index at which the endpoint starts returning results. Used for pagination. Default: 0.
This is a zero-based index (if set to 100, results start from the 101st entry).

filter
object
Specifies criteria for filtering the linked files by name or publish status.
Filter by file name:
Example: filter[name]=StructuralModel_2023.rvt&filter[name]=ArchitecturalModel_2023.rvt
Filter by publish status:
Published files: filter[publishStatus]=published
Unpublished files: filter[publishStatus]=notPublished
Both published and unpublished: filter[publishStatus]=published,notPublished
includeHost
boolean
Indicates whether to include the signed URL for the host model in the response.
true (default): the host model’s signed URL is included.

false: only includes the signed URLs of the linked files.

Response
HTTP Status Code Summary
200
OK
OK, Success.
400
Bad Request
Bad request. The request contained invalid parameters or malformed syntax.
401
Unauthorized
Unauthorized. The request is missing authentication credentials or contains an invalid authorization token.
403
Forbidden
Forbidden. The user does not have permission to access the project or requested version.
404
Not Found
Not found. The requested version does not exist or was published before this feature was released.
500
Internal Server Error
Internal server error. An unexpected error occurred while processing the request.
Response
Body Structure (200)
 Expand all
hostFile
object
Metadata about the host model (the main Revit model that contains linked files). This object is only returned in the response when includeHost is set to true.
linkedFiles
object
A list of linked Revit (RVT) models associated with the requested published model version. This object contains a list of linked files and pagination details.
Example
OK, Success.

Request
curl -v 'https://developer.api.autodesk.com//construction/rcm/v1/projects/563a4c30-e30d-4869-ac02-2a18b6447abe/published-versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D2/linked-files?limit=100&offset=200&includeHost=true' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "hostFile": {
    "modelName": "Arch.rvt",
    "signedUrl": "https://cdn.us.oss.api.autodesk.com/com.autodesk.oss-persistent/us-east-1/3f/bf/5f/0137a7d9dc53af930bc1b527320d50fb5f/wip.dm.prod?response-content-type=application%2Foctet-stream&response-content-disposition=attachment%3B+filename%3D%977d69b1-43e7-40fa-8ece-6ec4602892f3.rvt%22&Expires=1643864703&Signature=00PZYS6gL~Nc6aRG2HAhOCKYl0xtqsuujMJ~VKSXm1vBa-OxS4lPQBSlTx5bswpLBe1W6Rz94eIZW2sPN-v6Mzz~JyXNZ-V9Z7zlBoE1VoQhspLioC225hxq6ZmDSU5QnZXuNDV4ih~p1n3xacYvUvQWX-ONAGVUgQvZ253Svw~qx-pO4j-Yh4kVRmzDZqQut1xOI5ZGH6JFGhXLSzkgbYcfYx6fvCxnvYUJrgAcqncIwGVewI3uC0I84Fzrj8nXE8ojuojqJP0pNlxkfBe~2LfjjzqKDKaNvfC2Grt12j9QgC~cN7nQCRcVUhExpoV1VVB5x3AkVTJ-q5NoedvsfO__&Key-Pair-Id=95HRZD7MMO1UK",
    "itemId": "urn:adsk.wipprod:dm.lineage:f909RzMKR4mhc3O7UBY_3g",
    "versionId": "urn:adsk.wipprod:fs.file:vf.f909RzMKR4mhc3O7UBY_3g?version=2",
    "size": 2003,
    "publishStatus": "published"
  },
  "linkedFiles": {
    "pagination": {
      "limit": 100,
      "offset": 200,
      "nextUrl": "https://developer.api.autodesk.com/construction/rcm/v1/projects/563a4c30-e30d-4869-ac02-2a18b6447abe/published-versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D2/linked-files?offset=300&limit=100",
      "nextOffset": 300,
      "totalResults": 305
    },
    "results": [
      {
        "modelName": "StructuralModel_2023.rvt",
        "signedUrl": "https://cdn.us.oss.api.autodesk.com/com.autodesk.oss-persistent/us-east-1/3f/bf/5f/0137a7d9dc53af930bc1b527320d50fb5f/wip.dm.prod?response-content-type=application%2Foctet-stream&response-content-disposition=attachment%3B+filename%3D%977d69b1-43e7-40fa-8ece-6ec4602892f3.rvt%22&Expires=1643864703&Signature=00PZYS6gL~Nc6aRG2HAhOCKYl0xtqsuujMJ~VKSXm1vBa-OxS4lPQBSlTx5bswpLBe1W6Rz94eIZW2sPN-v6Mzz~JyXNZ-V9Z7zlBoE1VoQhspLioC225hxq6ZmDSU5QnZXuNDV4ih~p1n3xacYvUvQWX-ONAGVUgQvZ253Svw~qx-pO4j-Yh4kVRmzDZqQut1xOI5ZGH6JFGhXLSzkgbYcfYx6fvCxnvYUJrgAcqncIwGVewI3uC0I84Fzrj8nXE8ojuojqJP0pNlxkfBe~2LfjjzqKDKaNvfC2Grt12j9QgC~cN7nQCRcVUhExpoV1VVB5x3AkVTJ-q5NoedvsfO__&Key-Pair-Id=95HRZD7MMO1UK",
        "itemId": "urn:adsk.wipprod:dm.lineage:XYZ123003443we",
        "versionId": "urn:adsk.wipprod:fs.file:vf.e7r4RzMKR4mhc3Oc4y6?version=1",
        "publishStatus": "published"
      }
    ]
  }
}

Documentation /Autodesk Construction Cloud APIs /API Reference
List packages
GET	projects/{projectId}/packages
Retrieves a list of all packages within a specified ACC project.

With two-legged authentication, returns all packages in the project. With two-legged authentication and the x-user-id header, or with three-legged authentication, returns only the packages that the specified or current user has permission to access.

For information about creating packages, see the Create Packages documentation.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/packages/v1/projects/{projectId}/packages
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
The Autodesk ID of the user on whose behalf the request is made.
This header is required only when using two-legged authentication. It is not needed for three-legged authentication.

Your application can access only those users who are assigned to it in the SaaS Integrations UI.

Only user Autodesk IDs (autodeskId) are supported.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
You can retrieve the project ID using the Data Management API. For more details, see the Retrieve a Project ID tutorial.

You may provide the project ID with or without the b. prefix:

With prefix: b.657a5565-09b7-48e0-bd03-acacfe42efaf
Without prefix: 657a5565-09b7-48e0-bd03-acacfe42efaf
Request
Query String Parameters
limit
int
The number of packages to return in the response payload.
Possible values: 1-200. Default: 200. For example: limit=2.

offset
int
The number of packages that you want to begin retrieving results from.
Default: 0. For example: offset=10

filter[createdBy]
string
Filters results by the Autodesk ID of the users who created the packages.
You can provide a single Autodesk ID or a comma-separated list of IDs.

filter[updatedBy]
string
Filters results by the Autodesk ID of the users who last updated the packages.
You can provide a single Autodesk ID or a comma-separated list of IDs.

To find the IDs call GET users

filter[createdAt]
string
Filter packages by their creation time. Use an ISO 8601 date-time range in the format startDate..endDate.
Either date may be omitted to specify an open-ended range.

Examples:

After a specific time: 2025-03-26T16:00:00.000Z..
Before a specific time: ..2025-03-28T15:59:59.999Z
Between two times: 2025-03-26T16:00:00.000Z..2025-03-28T15:59:59.999Z
filter[updatedAt]
string
Filter packages by their last update time. Use an ISO 8601 date-time range in the format startDate..endDate.
Either date may be omitted to specify an open-ended range.

Examples:

After a specific time: 2025-03-26T16:00:00.000Z..
Before a specific time: ..2025-03-28T15:59:59.999Z
Between two times: 2025-03-26T16:00:00.000Z..2025-03-28T15:59:59.999Z
sort
enum:string
Sorts the results by a supported field.
By default, results are sorted in ascending (asc) order. To sort in descending order, add desc after the field name.

Format: sort=fieldName [desc]

Possible values: name, createdAt, updatedAt, displayId,

Examples:

Sort by name (ascending): sort=name
Sort by creation time (descending): sort=createdAt desc
filter[versionType]
enum:string
Filters results by the version type of the packages.
Possible values:

FIXED – Files in the package remain fixed at selected versions.
CURRENT – Files in the package automatically update to the latest current versions.
For more details, see the Flexible Package Types documentation.

Response
HTTP Status Code Summary
200
OK
Successfully retrieved a list of packages
400
Bad Request
Bad request. The input parameters were invalid.
403
Forbidden
Forbidden. The user does not have permission to access this resource.
404
Not Found
Not found. The resource does not exist or is inaccessible.
500
Internal Server Error
An unexpected server error occurred.
Response
Body Structure (200)
 Expand all
results
array: object
The list of results.
pagination
object
The pagination information for the response. This object is included when results are returned in multiple pages.
Example
Successfully retrieved a list of packages

Request
curl -v 'https://developer.api.autodesk.com/construction/packages/v1/projects/657a5565-09b7-48e0-bd03-acacfe42efaf/packages?limit=200&filter[createdBy]=L9VDREARJ7X2,9NGKQKPXAUHG&filter[updatedBy]=L9VDREARJ7X2,9NGKQKPXAUHG&filter[createdAt]=2025-03-26T16:00:00.000Z..2025-03-28T15:59:59.999Z&filter[updatedAt]=2025-03-26T16:00:00.000Z..2025-03-28T15:59:59.999Z&sort=name&filter[versionType]=FIXED' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "results": [
    {
      "id": "c25d1273-41e3-4e04-be1e-f4c1ba809d14",
      "displayId": 8642,
      "name": "Milestones",
      "description": "This package contains all the files related to the milestones.",
      "createdAt": "2025-03-27T01:28:28.272Z",
      "createdBy": "L9VDREARJ7X2",
      "updatedAt": "2025-03-27T03:25:48.884Z",
      "updatedBy": "L9VDREARJ7X2",
      "locked": true,
      "lockedBy": "L9VDREARJ7X2",
      "lockedAt": "2025-03-27T03:25:48.884Z",
      "resourceCount": 2,
      "versionType": "FIXED"
    }
  ],
  "pagination": {
    "limit": 200,
    "offset": 0,
    "nextUrl": "https://developer.api.autodesk.com/construction/packages/v1/projects/657a5565-09b7-48e0-bd03-acacfe42efaf/packages?limit=200&offset=400",
    "totalResults": 8618
  }
}
Documentation /Autodesk Construction Cloud APIs /API Reference
List package resources
GET	projects/{projectId}/packages/{packageId}/resources
Retrieves a list of file versions (“resources”) within a specified package.

With two-legged authentication, returns all resources in the package. With two-legged authentication and the x-user-id header, or with three-legged authentication, returns only the resources the current user has permission to access.

The results include deleted files (indicated by isDeleted=true), whether the file itself was deleted or its parent folder was deleted.

For information about adding files to a package, see the Add Files documentation.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/packages/v1/projects/{projectId}/packages/{packageId}/resources
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
The Autodesk ID of the user on whose behalf the request is made.
This header is required only when using two-legged authentication. It is not needed for three-legged authentication.

Your application can access only those users who are assigned to it in the SaaS Integrations UI.

Only user Autodesk IDs (autodeskId) are supported.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
You can retrieve the project ID using the Data Management API. For more details, see the Retrieve a Project ID tutorial.

You may provide the project ID with or without the b. prefix:

With prefix: b.657a5565-09b7-48e0-bd03-acacfe42efaf
Without prefix: 657a5565-09b7-48e0-bd03-acacfe42efaf
packageId
string: UUID
The ID of the package.
To find the package ID, call GET packages.

Request
Query String Parameters
limit
int
The number of resources to return in the response payload.
Possible values: 1-1000. Default: 200. For example: limit=2.

offset
int
The number of resources that you want to begin retrieving results from.
Default: 0. For example: offset=10.

filter[fileType]
string
Filter by file type. This can be a single value or a comma-separated list of values.
For example: filter[fileType]=pdf,rvt. Refer to Supported Files for more details.

filter[version]
string
Filter by file version number. This can be a single value or a comma-separated list of values.
For example: filter[version]=1,2,3

sort
enum:string
Provide options to sort on single field, in ascending (asc) by default or descending (desc) order.
Possible values of sorting field: name, description, updatedAt, approvalStatus, version. For example: sort=name desc.

Response
HTTP Status Code Summary
200
OK
Successfully retrieved file versions in a package
400
Bad Request
Bad request. The input parameters were invalid.
403
Forbidden
Forbidden. The user does not have permission to access this resource.
404
Not Found
Not found. The resource does not exist or is inaccessible.
500
Internal Server Error
An unexpected server error occurred.
Response
Body Structure (200)
 Expand all
results
array: object
The list of results.
pagination
object
The pagination information for the response. This object is included when results are returned in multiple pages.
Example
Successfully retrieved file versions in a package

Request
curl -v 'https://developer.api.autodesk.com/construction/packages/v1/projects/657a5565-09b7-48e0-bd03-acacfe42efaf/packages/c25d1273-41e3-4e04-be1e-f4c1ba809d14/resources?limit=200&filter[fileType]=pdf,rvt&filter[version]=1,2,3&sort=name' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "results": [
    {
      "urn": "urn:adsk.wip:fs.file:vf.betLCOhhTF6o1ACTFdEbXA?version=1",
      "id": "f16e92f0-64be-4ae1-bcd6-dd2ad004c8d2",
      "createdAt": "2025-03-27T03:29:48.000Z",
      "createdBy": "L9VDREARJ7X2",
      "createdByName": "John Smith",
      "updatedAt": "2025-03-05T08:14:53.000Z",
      "updatedBy": "L9VDREARJ7X2",
      "updatedByName": "John Smith",
      "name": "101-BIMicon-CD-L2-DR-A-A40-010-R1.pdf",
      "description": "BIM icon CD L2 DR A40 010 R1",
      "isDeleted": false,
      "entityType": "SEED_FILE",
      "parentFolderUrn": "urn:adsk.wip:fs.folder:co.rbR46ACySm6qdS4vAOdDDA",
      "storageUrn": "urn:adsk.objects:os.object:wip.dm.prod/c4a75bbc-24eb-41a3-a58b-48e51942222e.pdf",
      "customAttributes": [
        {
          "id": 123,
          "type": "array",
          "name": "Drawing Type",
          "value": "General"
        }
      ],
      "version": 1,
      "approvalStatus": {
        "id": "f44e623d-f04f-47fe-8195-efc43d1d985b",
        "label": "Approved",
        "value": "approved"
      },
      "fileType": "pdf"
    }
  ],
  "pagination": {
    "limit": 200,
    "offset": 0,
    "nextUrl": "https://developer.api.autodesk.com/construction/packages/v1/projects/657a5565-09b7-48e0-bd03-acacfe42efaf/packages/c25d1273-41e3-4e04-be1e-f4c1ba809d14/resources?limit=100&offset=200",
    "totalResults": 100
  }
}

以下是Form API:
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
projectId
string
Unique indentifier of the project the template belongs to.
id
string
The unique identifier of the template.
name
string
Display name of template.
status
string
Status of template: "active", "inactive" (archived), or "deleted"
templateType
string
User supplied type of template
userPermissions
array
Permissions on this template assigned to individual users.
groupPermissions
array
Permissions on this template assigned to companies and roles.
createdBy
string
The unique identifier of the user who created the template.
updatedAt
datetime: ISO 8601
When the template was last updated, UTC date and time in ISO-8601 format.
isPdf
boolean
A flag that indicates whether the template has a PDF or not.
pdfUrl
string
For PDF forms, the URL to download the form’s PDF.
forms
object
Reference to fetch forms created from this template.
pagination
object
Request pagination information.
offset
int
Number of items skipped.
limit
int
Number of items returned.
totalResults
int
Total number of items that can be returned.
nextUrl
string
URL for the next page of items. Next page url is null on the last page.


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

以下是ISSUE API:
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

以下是Location api :
Documentation /  文档/ Autodesk Construction Cloud APIs /API Reference
nodes
GET	v2/projects/{projectId}/trees/{treeId}/nodes
Retrieves an array of nodes (locations) from the specified locations tree (LBS). Returns all nodes in the tree by default.

To include each node’s path (an array of its ancestor nodes’ names) in the response, use the filter[id] parameter to specify a comma-separated list of nodes to return.

For more information about working with a locations tree, see the Configure a Locations Tree tutorial.

For more details about the Locations API, see Locations API Field Guide .

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/locations/v2/projects/:projectId/trees/:treeId/nodes
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
The region where the Locations service you are using is located. Possible values: US, EMEA. For the full list of supported regions, see the Regions page.
* Required
Request
URI Parameters
projectId
string: UUID
The identifier of the project that contains your locations tree.
Use the Data Management API to retrieve the relevant ACC account and project IDs.

treeId
string
Must be default. Currently a project can contain only the default tree.
Request
Query String Parameters
filter[id]
array: string
Specifies one or more nodes (locations) in the LBS tree to retrieve. Separate multiple node IDs with commas (no space); for example, filter[id]=88e07ccb-4594-4dc5-8973-304412b8fa96,de9aca33-5e0c-4668-85fa-f96273db4b35.
To find node IDs, call this endpoint and check the value of results.id in the returned nodes.

Note that when you use this parameter, the server ignores the limit and offset parameters, and each node in the response includes a path array containing its ancestor nodes in the tree.

limit
int
The maximum number of location nodes to return per page. Acceptable values: 1-10000. Default value: 10000.
offset
int
The node index at which the pagination starts. This is zero-based; for example, with a value of 6, the response starts with the seventh node.
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
The specified project or tree was not found.
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
curl -v 'https://developer.api.autodesk.com/construction/locations/v2/projects/:projectId/trees/:treeId/nodes' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 3,
    "offset": 0,
    "totalResults": 7,
    "nextUrl": "/locations/v2/projects/4a327b27-897c-4e5a-8e48-6e01c21377f3/trees/default/nodes?limit=3&offset=3"
  },
  "results": [
    {
      "id": "5add4375-f223-4201-88b9-8049e68416aa",
      "parentId": null,
      "type": "Root",
      "name": "Project",
      "description": null,
      "barcode": null,
      "order": 0
    },
    {
      "id": "d14ce3a6-e61b-4ab0-a9be-5acf7b5366df",
      "parentId": "5add4375-f223-4201-88b9-8049e68416aa",
      "type": "Area",
      "name": "Floor 1",
      "description": null,
      "barcode": "ABC123",
      "order": 0
    },
    {
      "id": "8da1faf2-a72f-421b-89df-00d77e545faf",
      "parentId": "5add4375-f223-4201-88b9-8049e68416aa",
      "type": "Area",
      "name": "Floor 2",
      "description": null,
      "barcode": "DEF456",
      "order": 1
    }
  ]
}
總結
總而言之，GET /nodes 這個 API 是任何需要與 ACC 位置功能整合的外部應用程式的基礎。開發者會使用它來：

在自己的應用程式中顯示一個位置選擇的下拉選單或樹狀圖。

當使用者建立一個問題 (Issue) 或上傳一張照片時，可以讓他們關聯到一個精確的工地位置。

讀取並展示某個物件（如資產、問題）的詳細位置資訊。

以下是Photo api:
Documentation /Autodesk Construction Cloud APIs /API Reference
Photo
GET	photos/:photoId
Return a single media (photo or video)

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/photos/v1/projects/:projectId/photos/:photoId
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
Unique identifier of the project.
photoId
string
Unique identifier of the media.
Request
Query String Parameters
include
array
Extra fields to be returned for each Photo Objects. (e.g. signedUrls) Will always be: signedUrls
Response
HTTP Status Code Summary
200
OK
Successful return of a media
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request header
403
Forbidden
The request was not accepted because it lacked valid authentication credentials
404
Not Found
The resource cannot be found
410
Gone
The resource was deleted by a user and cannot be return
Response
Body Structure (200)
 Expand all
createdAt
datetime: ISO 8601
The time when the media was created at (ISO8601 Date time format in UTC).
createdBy
string
The actor that created the media. This is an Autodesk ID.
deletedAt
datetime: ISO 8601
The time when the media was deleted at (ISO8601 Date time format in UTC).
deletedBy
string
The actor that deleted the media. This is an Autodesk ID.
description
string
Description of the media
id
string: UUID
The ID of the media.
Max length: 36

isPublic
boolean
If true the media is public and visible to everyone
latitude
number
Latitude in decimal degrees
locked
boolean
If true the media cannot be deleted or edited
longitude
number
Longitude in decimal degrees
mediaType
enum:string
The type of the media (NORMAL is for a normal photo) Possible values: NORMAL, INFRARED, PHOTOSPHERE, VIDEO
projectId
string: UUID
The id of the project
Max length: 36

signedUrls
object
URLs to the media’s assets. Accessible by anyone but is short-lived. Must be explicitly requested via `include field
size
number
Filesize of the media in bytes
takenAt
datetime: ISO 8601
The time when the media was captured by the camera at (ISO8601 Date time format in UTC).
title
string
Title of the media
type
enum:string
The type of object this media was initially added with Possible values: FIELD-REPORT, FORM, ISSUE, RFI, MARKUP, ASSET, GALLERY, MEETING, SUBMITTAL, LOGO
updatedAt
datetime: ISO 8601
The time when the media was last updated (ISO8601 Date time format in UTC).
updatedBy
string
The actor that last updated the media. This is an Autodesk ID.
urls
object
URLs to the media’s assets. Requires API auth headers (data:read) to access it.
userCreatedAt
datetime: ISO 8601
The time when the media was added to the project at (whether it was offline/locally or online) at (ISO8601 Date time format in UTC).
Example
Success retrieval of a media

Request
curl -v 'https://developer.api.autodesk.com/construction/photos/projects/36c0838c-0360-4cfa-b2c6-85e0056ec7e8/photos/5439bfb7-8006-4388-a454-f02560f99566?include=signedUrls' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "createdAt": "2021-03-14T10:20:33",
  "createdBy": "PER8KQPK2JRT",
  "deletedAt": "2021-03-19T11:50:33",
  "deletedBy": "PER8KQPK2JRT",
  "description": "The left side of the office",
  "id": "5439bfb7-8006-4388-a454-f02560f99566",
  "isPublic": false,
  "latitude": 37.757497,
  "locked": false,
  "longitude": -122.42115,
  "mediaType": "NORMAL",
  "projectId": "36c0838c-0360-4cfa-b2c6-85e0056ec7e8",
  "signedUrls": {
    "fileUrl": "https://s3.amazonaws.com/com.autodesk.oss-persistent/f0/7b/66/4df1b73d0cc643e6179b85eae7d8d529d2/ce8edd30-ef28-467c-8d99-7d7051097ee0?response-content-disposition=attachment%3B%20filename%3D%22c35b8b28-859e-4256-a3bc-41772a673260.jpg%22&response-content-type=image%2Fjpeg&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEKP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIQCOKZyru7bEOWhRlJOiFZUwLwGSFSWPO5VknX%2BIisldAwIgWN6g5zYxXLOzdiZgR4sYuyY4qr1k1SAQOTOCI7EOmKIqvQMI3P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw5OTM3ODk5OTIwNjMiDK0wr6QcJBV%2BrqLz7iqRA55WGaeF1IZVyH5XzR%2FyR72VqyCRIEwm9D3Pt%2BTOxtaNa519ldQcvjYptWrlwnrgr1T9c3jxtEXxHZveX3XwgaSQq7JyHACBAMVwkKABwczEzPOryCvIJBWjgr2ABoYGr0dDCFdh9IjdoDrOrXDDesn4I5GamK%2BdNzXBR1MJH3ocmoZXxrmaJGigr62ShQ3q7AoqMgIX55XH8DnYMP4k9OlGGJsL7P80OnvOXfNLFl9EVJp5jnp%2BT1eO3FezRxc%2FqkeTG7t6QHh87P4cJKzWV9pW3AQoYvBKyQ5uJn5WA8%2FFg%2BhzYalr5Y%2B4%2FneB0xfn7WS2I%2FvjIo6rOkIqx7K3Ty1p1kuZ6e64%2BlEXx8mYHO2NOYobbSf%2Fx%2B7FU1rhZqvqUGB%2BRoMXFI%2FIkaxe%2B%2Ba6sZYV6Dm6bcim835asw%2B48vkt3XLZ6kBNqOJMdqvIBp%2F7opV9Bc4%2BMkhPc6wT%2BwAoQ0jHGuNZiLh%2BsxcB8EtwziI18v5LFw6WmffTQD3oc8WTb9xUZmoQ8qDq5z%2FY4%2BY2EAq6MNaP7oIGOusBXz4xrUPPH0cr5UO912gp6aysXFnqxu55it8zqPwiGI2Xe0RlaMTAMh1jwDZ4LZD4N2NERk%2F%2BlR1KaRk2Jvo34HIXVnUqNWlYAR3TyV2intl8wwJWlgKQH6DI%2BzwOJ27kDToULG5TQpQk6xAQaToplmERCien7Pi8vlb0JNBCzkoKNh40Z1wPxcS%2BitdU0IkD0n39bvWy5uG0hoUuifHr53vaf7eqFRSdrd%2B%2BYuJ00yT%2FtWS6FLpLKCSgZw8GKoAq3PpfPggmg99bAju7H%2FD8xfVgBPhb91tEGCCdyub4jDtj6euoUFXK%2FiMIVg%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20210324T193346Z&X-Amz-SignedHeaders=host&X-Amz-Expires=60&X-Amz-Credential=ASIA6OYT73R75HNE4VUO%2F20210324%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=e694954290d485482c6334b39b591c87e4a16ba2425f05da1dc25faf47afba2d",
    "thumbnailUrl": "https://s3.amazonaws.com/com.autodesk.oss-opsstaging-persistent/81/b8/3d/e2855b46af2060d595ce31923310079c4b/ce8edd30-ef28-467c-8d99-7d7051097ee0?response-content-disposition=attachment%3B%20filename%3D%22c35b8b28-859e-4256-a3bc-41772a673260_t.jpg%22&response-content-type=image%2Fjpeg&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEKP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIQCOKZyru7bEOWhRlJOiFZUwLwGSFSWPO5VknX%2BIisldAwIgWN6g5zYxXLOzdiZgR4sYuyY4qr1k1SAQOTOCI7EOmKIqvQMI3P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw5OTM3ODk5OTIwNjMiDK0wr6QcJBV%2BrqLz7iqRA55WGaeF1IZVyH5XzR%2FyR72VqyCRIEwm9D3Pt%2BTOxtaNa519ldQcvjYptWrlwnrgr1T9c3jxtEXxHZveX3XwgaSQq7JyHACBAMVwkKABwczEzPOryCvIJBWjgr2ABoYGr0dDCFdh9IjdoDrOrXDDesn4I5GamK%2BdNzXBR1MJH3ocmoZXxrmaJGigr62ShQ3q7AoqMgIX55XH8DnYMP4k9OlGGJsL7P80OnvOXfNLFl9EVJp5jnp%2BT1eO3FezRxc%2FqkeTG7t6QHh87P4cJKzWV9pW3AQoYvBKyQ5uJn5WA8%2FFg%2BhzYalr5Y%2B4%2FneB0xfn7WS2I%2FvjIo6rOkIqx7K3Ty1p1kuZ6e64%2BlEXx8mYHO2NOYobbSf%2Fx%2B7FU1rhZqvqUGB%2BRoMXFI%2FIkaxe%2B%2Ba6sZYV6Dm6bcim835asw%2B48vkt3XLZ6kBNqOJMdqvIBp%2F7opV9Bc4%2BMkhPc6wT%2BwAoQ0jHGuNZiLh%2BsxcB8EtwziI18v5LFw6WmffTQD3oc8WTb9xUZmoQ8qDq5z%2FY4%2BY2EAq6MNaP7oIGOusBXz4xrUPPH0cr5UO912gp6aysXFnqxu55it8zqPwiGI2Xe0RlaMTAMh1jwDZ4LZD4N2NERk%2F%2BlR1KaRk2Jvo34HIXVnUqNWlYAR3TyV2intl8wwJWlgKQH6DI%2BzwOJ27kDToULG5TQpQk6xAQaToplmERCien7Pi8vlb0JNBCzkoKNh40Z1wPxcS%2BitdU0IkD0n39bvWy5uG0hoUuifHr53vaf7eqFRSdrd%2B%2BYuJ00yT%2FtWS6FLpLKCSgZw8GKoAq3PpfPggmg99bAju7H%2FD8xfVgBPhb91tEGCCdyub4jDtj6euoUFXK%2FiMIVg%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20210324T193346Z&X-Amz-SignedHeaders=host&X-Amz-Expires=60&X-Amz-Credential=ASIA6OYT73R75HNE4VUO%2F20210324%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=fac56130302305057c9ae301503860edb2d296c43dcfb5a59ebf3744f5126baa"
  },
  "size": 11359,
  "takenAt": "2021-03-13T18:15:00",
  "title": "Office Dry Wall",
  "type": "FIELD-REPORT",
  "updatedAt": "2021-03-14T11:20:33",
  "updatedBy": "PER8KQPK2JRT",
  "urls": {
    "fileUrl": "https://developer.api.autodesk.com/construction/photos/assets/ce8edd30-ef28-467c-8d99-7d7051097ee0/c35b8b28-859e-4256-a3bc-41772a673260.jpg\"",
    "thumbnailUrl": "https://developer.api.autodesk.com/construction/photos/assets/ce8edd30-ef28-467c-8d99-7d7051097ee0/c35b8b28-859e-4256-a3bc-41772a673260_t.jpg\""
  },
  "userCreatedAt": "2021-03-13T18:20:33"
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Photos
POST	photos:filter
Searches for and returns all specified media (photo or video) within a project visible to the authenticated user.

This endpoint accepts a set of optional media property filters, then uses supplied filters to search for and return media within a project that satisfy those filters. If no filters are set, this endpoint returns all assets within a project.

The endpoint paginates returned media. If you don’t specify pagination fields, your query will execute using the default page size. If you want to specify a different a page size, define the limit in the request body.

A paginated response includes pagination information that may contain a field nextPost Use the data it provides (url, body) as the request url and body respectively to request the next page in the query. Repeat until the response contains no nextPost value, which means the query is finished returning objects.

Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/construction/photos/v1/projects/:projectId/photos:filter
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
Unique identifier of the project.
Request
Body Structure
 Expand all
cursorState
string
An opaque cursor token that identifies where the next page of paginated results should start. It’s returned in each paginated response so that it can be supplied in the next request to continue paginated results. If a paginated response contains no cursorState value, then there are no further pages to return. If provided, all other body parameters are ignored.
filter
object
Parameters to filter media by
include
array: string
Extra fields to be returned for each Photo Objects (e.g. signedUrls) Will always be: signedUrls
limit
int
The maximum number of objects that can be returned in a page. A request might return fewer objects than the limit if the Photos service runs out of specified objects to return - at the end of a set of paged results, for example. The maximum limit is 50; the default limit is 25.
sort
array: string
Define how results are sorted. Provide the field (createdAt, takenAt) and the direction (asc, desc) eg. ["createdAt", "asc"]
Response
HTTP Status Code Summary
200
OK
Successful return of the filtered media
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request header
403
Forbidden
The request was not accepted because it lacked valid authentication credentials
Response
Body Structure (200)
 Expand all
pagination
object
Pagination details
results
array: object
The filtered media
Example
Success retrieval of filtered media

Request
curl -v 'https://developer.api.autodesk.com/construction/photos/projects/36c0838c-0360-4cfa-b2c6-85e0056ec7e8/photos:filter' \
  -X 'POST' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a' \
  -H 'Content-Type: application/json' \
  -d '{
        "cursorState": "eyJsaW1pdCI6MjUsICJ0aXRsZSI6ICJ3YWxsIn0Ks",
        "filter": {
          "createdAt": "2021-03-14T10:10:00..2021-03-16T10:15:00",
          "createdBy": [
            "NCSNR6R5NHUD",
            "5QCVQ6JAUTHB"
          ],
          "id": [
            "0c96ea4c-bd3d-4b80-9eb6-c123e1faecd5",
            "5439bfb7-8006-4388-a454-f02560f99566"
          ],
          "mediaType": [
            "NORMAL"
          ],
          "takenAt": "2021-03-12T10:10:00..2021-03-15T10:15:00",
          "title": "dry wall"
        },
        "include": [
          "signedUrls"
        ],
        "limit": 25,
        "sort": [
          "createdAt",
          "asc"
        ]
      }'
Show Less
Response
{
  "pagination": {
    "limit": 25,
    "nextPost": {
      "body": {
        "cursorState": "eyJsaW1pdCI6MjUsICJ0aXRsZSI6ICJ3YWxsIn0Ks"
      },
      "url": "https://developer.api.autodesk.com/construction/photos/v1/projects/8e52b200-f856-4f17-a57c-c03ba2f6673a/photos:filter"
    }
  },
  "results": [
    {
      "createdAt": "2021-03-14T10:20:33",
      "createdBy": "PER8KQPK2JRT",
      "deletedAt": "2021-03-19T11:50:33",
      "deletedBy": "PER8KQPK2JRT",
      "description": "The left side of the office",
      "id": "5439bfb7-8006-4388-a454-f02560f99566",
      "isPublic": false,
      "latitude": 37.757497,
      "locked": false,
      "longitude": -122.42115,
      "mediaType": "NORMAL",
      "projectId": "36c0838c-0360-4cfa-b2c6-85e0056ec7e8",
      "signedUrls": {
        "fileUrl": "https://s3.amazonaws.com/com.autodesk.oss-persistent/f0/7b/66/4df1b73d0cc643e6179b85eae7d8d529d2/ce8edd30-ef28-467c-8d99-7d7051097ee0?response-content-disposition=attachment%3B%20filename%3D%22c35b8b28-859e-4256-a3bc-41772a673260.jpg%22&response-content-type=image%2Fjpeg&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEKP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIQCOKZyru7bEOWhRlJOiFZUwLwGSFSWPO5VknX%2BIisldAwIgWN6g5zYxXLOzdiZgR4sYuyY4qr1k1SAQOTOCI7EOmKIqvQMI3P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw5OTM3ODk5OTIwNjMiDK0wr6QcJBV%2BrqLz7iqRA55WGaeF1IZVyH5XzR%2FyR72VqyCRIEwm9D3Pt%2BTOxtaNa519ldQcvjYptWrlwnrgr1T9c3jxtEXxHZveX3XwgaSQq7JyHACBAMVwkKABwczEzPOryCvIJBWjgr2ABoYGr0dDCFdh9IjdoDrOrXDDesn4I5GamK%2BdNzXBR1MJH3ocmoZXxrmaJGigr62ShQ3q7AoqMgIX55XH8DnYMP4k9OlGGJsL7P80OnvOXfNLFl9EVJp5jnp%2BT1eO3FezRxc%2FqkeTG7t6QHh87P4cJKzWV9pW3AQoYvBKyQ5uJn5WA8%2FFg%2BhzYalr5Y%2B4%2FneB0xfn7WS2I%2FvjIo6rOkIqx7K3Ty1p1kuZ6e64%2BlEXx8mYHO2NOYobbSf%2Fx%2B7FU1rhZqvqUGB%2BRoMXFI%2FIkaxe%2B%2Ba6sZYV6Dm6bcim835asw%2B48vkt3XLZ6kBNqOJMdqvIBp%2F7opV9Bc4%2BMkhPc6wT%2BwAoQ0jHGuNZiLh%2BsxcB8EtwziI18v5LFw6WmffTQD3oc8WTb9xUZmoQ8qDq5z%2FY4%2BY2EAq6MNaP7oIGOusBXz4xrUPPH0cr5UO912gp6aysXFnqxu55it8zqPwiGI2Xe0RlaMTAMh1jwDZ4LZD4N2NERk%2F%2BlR1KaRk2Jvo34HIXVnUqNWlYAR3TyV2intl8wwJWlgKQH6DI%2BzwOJ27kDToULG5TQpQk6xAQaToplmERCien7Pi8vlb0JNBCzkoKNh40Z1wPxcS%2BitdU0IkD0n39bvWy5uG0hoUuifHr53vaf7eqFRSdrd%2B%2BYuJ00yT%2FtWS6FLpLKCSgZw8GKoAq3PpfPggmg99bAju7H%2FD8xfVgBPhb91tEGCCdyub4jDtj6euoUFXK%2FiMIVg%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20210324T193346Z&X-Amz-SignedHeaders=host&X-Amz-Expires=60&X-Amz-Credential=ASIA6OYT73R75HNE4VUO%2F20210324%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=e694954290d485482c6334b39b591c87e4a16ba2425f05da1dc25faf47afba2d",
        "thumbnailUrl": "https://s3.amazonaws.com/com.autodesk.oss-opsstaging-persistent/81/b8/3d/e2855b46af2060d595ce31923310079c4b/ce8edd30-ef28-467c-8d99-7d7051097ee0?response-content-disposition=attachment%3B%20filename%3D%22c35b8b28-859e-4256-a3bc-41772a673260_t.jpg%22&response-content-type=image%2Fjpeg&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEKP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIQCOKZyru7bEOWhRlJOiFZUwLwGSFSWPO5VknX%2BIisldAwIgWN6g5zYxXLOzdiZgR4sYuyY4qr1k1SAQOTOCI7EOmKIqvQMI3P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw5OTM3ODk5OTIwNjMiDK0wr6QcJBV%2BrqLz7iqRA55WGaeF1IZVyH5XzR%2FyR72VqyCRIEwm9D3Pt%2BTOxtaNa519ldQcvjYptWrlwnrgr1T9c3jxtEXxHZveX3XwgaSQq7JyHACBAMVwkKABwczEzPOryCvIJBWjgr2ABoYGr0dDCFdh9IjdoDrOrXDDesn4I5GamK%2BdNzXBR1MJH3ocmoZXxrmaJGigr62ShQ3q7AoqMgIX55XH8DnYMP4k9OlGGJsL7P80OnvOXfNLFl9EVJp5jnp%2BT1eO3FezRxc%2FqkeTG7t6QHh87P4cJKzWV9pW3AQoYvBKyQ5uJn5WA8%2FFg%2BhzYalr5Y%2B4%2FneB0xfn7WS2I%2FvjIo6rOkIqx7K3Ty1p1kuZ6e64%2BlEXx8mYHO2NOYobbSf%2Fx%2B7FU1rhZqvqUGB%2BRoMXFI%2FIkaxe%2B%2Ba6sZYV6Dm6bcim835asw%2B48vkt3XLZ6kBNqOJMdqvIBp%2F7opV9Bc4%2BMkhPc6wT%2BwAoQ0jHGuNZiLh%2BsxcB8EtwziI18v5LFw6WmffTQD3oc8WTb9xUZmoQ8qDq5z%2FY4%2BY2EAq6MNaP7oIGOusBXz4xrUPPH0cr5UO912gp6aysXFnqxu55it8zqPwiGI2Xe0RlaMTAMh1jwDZ4LZD4N2NERk%2F%2BlR1KaRk2Jvo34HIXVnUqNWlYAR3TyV2intl8wwJWlgKQH6DI%2BzwOJ27kDToULG5TQpQk6xAQaToplmERCien7Pi8vlb0JNBCzkoKNh40Z1wPxcS%2BitdU0IkD0n39bvWy5uG0hoUuifHr53vaf7eqFRSdrd%2B%2BYuJ00yT%2FtWS6FLpLKCSgZw8GKoAq3PpfPggmg99bAju7H%2FD8xfVgBPhb91tEGCCdyub4jDtj6euoUFXK%2FiMIVg%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20210324T193346Z&X-Amz-SignedHeaders=host&X-Amz-Expires=60&X-Amz-Credential=ASIA6OYT73R75HNE4VUO%2F20210324%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=fac56130302305057c9ae301503860edb2d296c43dcfb5a59ebf3744f5126baa"
      },
      "size": 11359,
      "takenAt": "2021-03-13T18:15:00",
      "title": "Office Dry Wall",
      "type": "FIELD-REPORT",
      "updatedAt": "2021-03-14T11:20:33",
      "updatedBy": "PER8KQPK2JRT",
      "urls": {
        "fileUrl": "https://developer.api.autodesk.com/construction/photos/assets/ce8edd30-ef28-467c-8d99-7d7051097ee0/c35b8b28-859e-4256-a3bc-41772a673260.jpg\"",
        "thumbnailUrl": "https://developer.api.autodesk.com/construction/photos/assets/ce8edd30-ef28-467c-8d99-7d7051097ee0/c35b8b28-859e-4256-a3bc-41772a673260_t.jpg\""
      },
      "userCreatedAt": "2021-03-13T18:20:33"
    }
  ]
}

以下是review api:
Documentation /Autodesk Construction Cloud APIs /API Reference
Get an Approval Workflow
GET	projects/{projectId}/workflows/{workflowId}
Retrieves a specific approval workflow in the project by workflow ID.

The workflow defines the steps, reviewers, durations, approval statuses and post-review actions used when creating new reviews.

For more details about approval workflows, see the Help documentation.

The Authorization header token can be obtained through either the three-legged OAuth flow or the two-legged OAuth flow with user impersonation, which requires the x-user-id header.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/reviews/v1/projects/{projectId}/workflows/{workflowId}
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
The ID of a user on whose behalf the request is made. Your application has access to all users specified by the administrator in the SaaS Integrations UI. Use this header to specify which user should be affected by the request.
This header is only required when using two-legged authentication. It is not needed for three-legged authentication.

Only user’s Autodesk ID (autodeskId) can be accepted.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can provide the project ID with or without the “b." prefix.

Example with prefix: b.563a4c30-e30d-4869-ac02-2a18b6447abe
Example without prefix: 563a4c30-e30d-4869-ac02-2a18b6447abe
workflowId
string: UUID
The ID of the approval workflow.
To find available workflow IDs, call GET Workflows.

Response
HTTP Status Code Summary
200
OK
Successfully retrieved the approval workflow.
400
Bad Request
Bad request. The input parameters were invalid.
403
Forbidden
Forbidden. The user does not have permission to access this resource.
404
Not Found
Not found. The resource does not exist or is inaccessible.
500
Internal Server Error
An unexpected server error occurred.
Response
Body Structure (200)
 Expand all
name
string
The name of the workflow. It must be unique within the project.
Max length: 255

description
string
A description of the workflow.
Max length: 4096

notes
string
A custom note associated with the workflow. Visible to all reviewers during the review process.
Max length: 4096

additionalOptions
object
Workflow-level settings that control whether the initiator can modify certain fields when starting a review.
id
string: UUID
The unique identifier of the approval workflow returned in the response. This ID can be used in subsequent API calls to reference this workflow.
status
enum:string
The current status of the approval workflow. Possible values:
ACTIVE: the workflow is active and available for use.

INACTIVE: the workflow has been deactivated and cannot be used to create new reviews.

approvalStatusOptions
array: object
A list of approval status options defined for this workflow. It includes two built-in options by default (typically APPROVED and REJECTED), and may also include custom statuses added by the user.
steps
array: object
A list of steps defined in the approval workflow. Each step defines who reviews the files, how long they have, and whether it involves multiple reviewers.
copyFilesOptions
object
(Copy approved files in the UI) The configuration for copying approved files to a target folder when the review is complete.
attachedAttributes
array: object
(Update Attributes in the UI) The list of attributes added in the Update Attributes action.
These attributes will be applied to the approved files in the target folder, or optionally also in the source folder depending on the configuration.

updateAttributesOptions
object
The configuration for applying attribute updates when a review is completed. This applies only if the workflow includes a file copy action and the Update Attributes action is enabled.
createdAt
datetime: ISO 8601
The date and time when the workflow was created.
updatedAt
datetime: ISO 8601
The date and time when the workflow was last updated.
Example
Successfully retrieved the approval workflow.

Request
curl -v 'https://developer.api.autodesk.com/construction/reviews/v1/projects/563a4c30-e30d-4869-ac02-2a18b6447abe/workflows/2483599f-b62a-42fb-aa5e-888468fb63eb' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "name": "Final Structural Review",
  "description": "Used to review structural plans before finalizing IFC drawings.",
  "notes": "Please check all rebar annotations before approving. Include markup if changes are required.",
  "additionalOptions": {
    "allowInitiatorToEdit": true
  },
  "id": "4e609369-e950-4097-b7d3-e6cf1c3c5415",
  "status": "ACTIVE",
  "approvalStatusOptions": [
    {
      "label": "Approved w/ comments",
      "value": "APPROVED",
      "id": "b2a3c3b7-4fef-40a4-868b-981b23e7182f",
      "builtIn": false
    }
  ],
  "steps": [
    {
      "name": "Reviewer",
      "type": "REVIEWER",
      "duration": 3,
      "dueDateType": "CALENDAR_DAY",
      "groupReview": {
        "enabled": true,
        "type": "MINIMUM",
        "min": 3
      },
      "id": "Lane_uJtTI3vjaF",
      "candidates": {
        "roles": [
          {
            "autodeskId": "1473817",
            "name": "Architect"
          }
        ],
        "users": [
          {
            "autodeskId": "HWUBNU689CRU",
            "name": "James Smith"
          }
        ],
        "companies": [
          {
            "autodeskId": "26980302",
            "name": "Autodesk Co. Ltd."
          }
        ]
      }
    }
  ],
  "copyFilesOptions": {
    "enabled": true,
    "allowOverride": false,
    "condition": "ANY",
    "folderUrn": "urn:adsk.wipprod:fs.folder:co.CplBAmvXRWGqsvN1Nabvd2",
    "includeMarkups": false,
    "disableOverrideMarkupSetting": false
  },
  "attachedAttributes": [
    {
      "id": 1001,
      "required": false
    }
  ],
  "updateAttributesOptions": {
    "enableAttachedAttributes": false,
    "updateSourceAndCopiedFiles": false
  },
  "createdAt": "2024-07-07T09:21:17.577Z",
  "updatedAt": "2025-01-07T08:43:10.189Z"
}

Documentation /Autodesk Construction Cloud APIs /API Reference
List Approval Workflows
GET	projects/{projectId}/workflows
Retrieves all approval workflows used for file reviews in a given project.

Each workflow defines the steps, reviewers, durations, approval statuses, and post-review actions used when creating new reviews.

For more details about approval workflows, see the Help documentation.

The Authorization header token can be obtained through either the three-legged OAuth flow or the two-legged OAuth flow with user impersonation, which requires the x-user-id header.

To retrieve the exact workflow that was applied to a specific review, call GET reviews/:reviewId/workflow.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/reviews/v1/projects/{projectId}/workflows
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
The ID of a user on whose behalf the request is made. Your application has access to all users specified by the administrator in the SaaS Integrations UI. Use this header to specify which user should be affected by the request.
This header is only required when using two-legged authentication. It is not needed for three-legged authentication.

Only user’s Autodesk ID (autodeskId) can be accepted.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can provide the project ID with or without the “b." prefix.

Example with prefix: b.563a4c30-e30d-4869-ac02-2a18b6447abe
Example without prefix: 563a4c30-e30d-4869-ac02-2a18b6447abe
Request
Query String Parameters
limit
int
The maximum number of approval workflows to return in a single request. Possible values: 1-50. Maximum: 50. Default: 50. For example: limit=2.
offset
int
The index at which the endpoint starts returning results. Used for pagination. Default: 0. For example: offset=10.
sort
string
Specifies a single field to sort the results by. The default order is ascending (asc); to sort in descending order, add desc. Possible sorting fields: name, status, updatedAt. For example: sort=name desc.
filter[initiator]
boolean
Filters the results based on who initiated the workflow. For example: filter[initiator]=true.
true: return only workflows initiated by the current user. This filter is ignored if the user is a project admin.

false: (default) return workflows regardless of who initiated them.

Note that this filter cannot be used together with filter[status].

filter[status]
enum:string
Filters the results by workflow status. For example: filter[status]=INACTIVE. Possible values:
ACTIVE: return only active workflows.

INACTIVE: return only inactive (disabled) workflows.

Default: ACTIVE.

Note that this filter cannot be used together with filter[initiator].

Response
HTTP Status Code Summary
200
OK
Successfully retrieved the list of approval workflows
400
Bad Request
Bad request. The input parameters were invalid.
403
Forbidden
Forbidden. The user does not have permission to access this resource.
404
Not Found
Not found. The resource does not exist or is inaccessible.
500
Internal Server Error
An unexpected server error occurred.
Response
Body Structure (200)
 Expand all
results
array: object
A list of approval workflows in the project.
pagination
object
Metadata about the paginated results.
Example
Successfully retrieved the list of approval workflows

Request
curl -v 'https://developer.api.autodesk.com/construction/reviews/v1/projects/563a4c30-e30d-4869-ac02-2a18b6447abe/workflows?limit=2&offset=10&sort=sort=name desc&filter[initiator]=true&filter[status]=ACTIVE' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "results": [
    {
      "name": "Final Structural Review",
      "description": "Used to review structural plans before finalizing IFC drawings.",
      "notes": "Please check all rebar annotations before approving. Include markup if changes are required.",
      "additionalOptions": {
        "allowInitiatorToEdit": true
      },
      "id": "4e609369-e950-4097-b7d3-e6cf1c3c5415",
      "status": "ACTIVE",
      "approvalStatusOptions": [
        {
          "label": "Approved w/ comments",
          "value": "APPROVED",
          "id": "b2a3c3b7-4fef-40a4-868b-981b23e7182f",
          "builtIn": false
        }
      ],
      "steps": [
        {
          "name": "Reviewer",
          "type": "REVIEWER",
          "duration": 3,
          "dueDateType": "CALENDAR_DAY",
          "groupReview": {
            "enabled": true,
            "type": "MINIMUM",
            "min": 3
          },
          "id": "Lane_uJtTI3vjaF",
          "candidates": {
            "roles": [
              {
                "autodeskId": "1473817",
                "name": "Architect"
              }
            ],
            "users": [
              {
                "autodeskId": "HWUBNU689CRU",
                "name": "James Smith"
              }
            ],
            "companies": [
              {
                "autodeskId": "26980302",
                "name": "Autodesk Co. Ltd."
              }
            ]
          }
        }
      ],
      "copyFilesOptions": {
        "enabled": true,
        "allowOverride": false,
        "condition": "ANY",
        "folderUrn": "urn:adsk.wipprod:fs.folder:co.CplBAmvXRWGqsvN1Nabvd2",
        "includeMarkups": false,
        "disableOverrideMarkupSetting": false
      },
      "attachedAttributes": [
        {
          "id": 1001,
          "required": false
        }
      ],
      "updateAttributesOptions": {
        "enableAttachedAttributes": false,
        "updateSourceAndCopiedFiles": false
      },
      "createdAt": "2024-07-07T09:21:17.577Z",
      "updatedAt": "2025-01-07T08:43:10.189Z"
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "totalResults": 100,
    "nextUrl": "https://developer.api.autodesk.com/construction/reviews/v1/projects/497f6eca-6276-4993-bfeb-53cbbbba6f08/workflows?limit=50&offset=50"
  }
}

Documentation /Autodesk Construction Cloud APIs /API Reference
List Reviews
GET	projects/{projectId}/reviews
Retrieves the list of reviews created in the specified project.

It includes basic information such as review ID, name, status, initiator, and current step information.

For more details about reviews, see the Help documentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/reviews/v1/projects/{projectId}/reviews
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
The ID of a user on whose behalf the request is made. Your application has access to all users specified by the administrator in the SaaS Integrations UI. Use this header to specify which user should be affected by the request.
This header is only required when using two-legged authentication. It is not needed for three-legged authentication.

Only user’s Autodesk ID (autodeskId) can be accepted.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can provide the project ID with or without the “b." prefix.

Example with prefix: b.563a4c30-e30d-4869-ac02-2a18b6447abe
Example without prefix: 563a4c30-e30d-4869-ac02-2a18b6447abe
Request
Query String Parameters
limit
int
The maximum number of reviews to retrieve.
Possible values: 1-50. Maximum: 50. Default: 50. For example: limit=2.

offset
int
The index of the first result to return (zero-based).
Default: 0. For example: offset=10.

sort
string
Sorts the results by a single field.
Use the format fieldName (ascending) or fieldName desc (descending).

If no direction is specified, sorting defaults to ascending.

Possible values: name, status, sequenceId, currentStepDueDate, createdAt, finishedAt.

For example: sort=createdAt desc.

filter[workflowId]
string: UUID
Filter by a specific approval workflow ID in URL-encoded format.
For example: filter[workflowId]=497f6eca-6276-4993-bfeb-53cbbbba6f08.

filter[status]
string
Filter by the review status in URL-encoded format.
Possible values: OPEN, CLOSED, VOID, FAILED.

For example: filter[status]=OPEN.

Reviews with status FAILED are only visible to project administrators.

filter[currentStepDueDate]
string
Filter by the due date of the current review step in URL-encoded format.
Provide a date range using the format startDate..endDate.

Both values must be in ISO 8601 format.

For example: filter[updatedAt]=2023-06-01..2023-06-30.

filter[createdAt]
string
Filter by review creation date in URL-encoded format.
Provide a date range using the format startDate..endDate.

Both values must be in ISO 8601 format.

For example: filter[createdAt]=2023-06-01..2023-06-30

filter[updatedAt]
string
Filter by the review’s last updated date in URL-encoded format.
Provide a date range using the format startDate..endDate.

Both values must be in ISO 8601 format.

For example: filter[updatedAt]=2023-06-01..2023-06-30.

filter[finishedAt]
string
Filter by the date the review was finished, in URL-encoded format.
Provide a date range using the format startDate..endDate.

Both values must be in ISO 8601 format.

For example: filter[finishedAt]=2023-06-01..2023-06-30.

filter[nextActionByUser]
string
Filter by Autodesk ID of a user responsible for the next action, in URL-encoded format.
This includes reviews assigned directly to the user or to their role or company.

For example: filter[nextActionByUser]=A96JX8NUKRLVFWSR.

filter[nextActionByRole]
string
Filter by Autodesk ID of a role responsible for the next action, in URL-encoded format.
For example: filter[nextActionByRole]=1572818.

filter[nextActionByCompany]
string
Filter by Autodesk ID of a company responsible for the next action, in URL-encoded format.
For example: filter[nextActionByCompany]=81768771.

filter[name]
string
Filter by review name in URL-encoded format.
Retrieves reviews with names that contain the specified string (not case-sensitive).

For example: filter[name]=Apartment retrieves reviews like Apartment Block A and apartment_rendering.

filter[sequenceId]
int
Filter by review sequence ID in URL-encoded format.
Retrieves reviews with sequence IDs that partially match the specified number.

For example: filter[sequenceId]=11 may retrieve 113 and 211.

filter[archived]
boolean
Filter by archive status in URL-encoded format.
true: retrieves only archived reviews.

false: retrieves only active (non-archived) reviews.

If omitted, only active reviews are retrieved.

For example: filter[archived]=false.

filter[archivedBy]
string
Filter by the Autodesk ID of the user who archived the review, in URL-encoded format. To find the ID, call GET users.
It only takes effect when filter[archived]=true is also set.

For example: filter[archivedBy]=A96JX8NUKRLVFWSR.

filter[archivedAt]
string
Filter by the date the review was archived, in URL-encoded format.
It only applies if filter[archived]=true.

Provide a date range using the format startDate..endDate.

Both values must be in ISO 8601 format.

For example: filter[archivedAt]=2023-06-01..2023-06-30.

Response
HTTP Status Code Summary
200
OK
Successfully retrieved the list of reviews
400
Bad Request
Bad request. The input parameters were invalid.
403
Forbidden
Forbidden. The user does not have permission to access this resource.
404
Not Found
Not found. The resource does not exist or is inaccessible.
500
Internal Server Error
An unexpected server error occurred.
Response
Body Structure (200)
 Expand all
results
array: object
A list of reviews matching the request parameters
pagination
object
Metadata about the paginated results.
Example
Successfully retrieved the list of reviews

Request
curl -v 'https://developer.api.autodesk.com/construction/reviews/v1/projects/563a4c30-e30d-4869-ac02-2a18b6447abe/reviews?limit=2&offset=10&sort=createdAt desc&filter[workflowId]=497f6eca-6276-4993-bfeb-53cbbbba6f08&filter[status]=OPEN&filter[currentStepDueDate]=2023-06-01..2023-06-30&filter[createdAt]=2023-06-01..2023-06-30&filter[updatedAt]=2023-06-01..2023-06-30&filter[finishedAt]=2023-06-01..2023-06-30&filter[nextActionByUser]=A96JX8NUKRLVFWSR&filter[nextActionByRole]=1572818&filter[nextActionByCompany]=81768771&filter[name]=Apartment&filter[sequenceId]=11&filter[archivedBy]=A96JX8NUKRLVFWSR&filter[archivedAt]=2023-06-01..2023-06-30' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "results": [
    {
      "id": "37d5145b-c634-407c-b0b4-a65197e43fce",
      "sequenceId": 23,
      "name": "3rd Floor Design Review",
      "status": "OPEN",
      "currentStepId": "Lane_uJtTI3vjaF",
      "currentStepDueDate": "2024-11-09T01:42:16.600Z",
      "createdBy": {
        "autodeskId": "HWUBNU689CRU",
        "name": "James Smith"
      },
      "createdAt": "2024-11-06T01:42:17.476Z",
      "updatedAt": "2024-11-07T12:33:36.421Z",
      "finishedAt": "2024-11-10T02:33:17.336Z",
      "archived": false,
      "archivedBy": {
        "autodeskId": "TTFMLCMCRG5F",
        "name": "Tim Hudson"
      },
      "archivedAt": "2024-11-19T01:38:27.306Z",
      "workflowId": "0b43cedf-5c02-462b-8166-7dfbb13d3476",
      "nextActionBy": {
        "claimedBy": [
          {
            "autodeskId": "HWUBNU689CRU",
            "name": "James Smith"
          }
        ],
        "candidates": {
          "roles": [
            {
              "autodeskId": "1473817",
              "name": "Architect"
            }
          ],
          "users": [
            {
              "autodeskId": "HWUBNU689CRU",
              "name": "James Smith"
            }
          ],
          "companies": [
            {
              "autodeskId": "26980302",
              "name": "Autodesk Co. Ltd."
            }
          ]
        }
      }
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "totalResults": 100,
    "nextUrl": "https://developer.api.autodesk.com/construction/reviews/v1/projects/497f6eca-6276-4993-bfeb-53cbbbba6f08/reviews?limit=50&offset=50"
  }
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Get a Review
GET	projects/{projectId}/reviews/{reviewId}
Retrieves a specific review in the specified project by review ID.

It includes basic information such as review ID, name, status, initiator, and current step information.

For more details about reviews, see the Help documentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/reviews/v1/projects/{projectId}/reviews/{reviewId}
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
The ID of a user on whose behalf the request is made. Your application has access to all users specified by the administrator in the SaaS Integrations UI. Use this header to specify which user should be affected by the request.
This header is only required when using two-legged authentication. It is not needed for three-legged authentication.

Only user’s Autodesk ID (autodeskId) can be accepted.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can provide the project ID with or without the “b." prefix.

Example with prefix: b.563a4c30-e30d-4869-ac02-2a18b6447abe
Example without prefix: 563a4c30-e30d-4869-ac02-2a18b6447abe
reviewId
string: UUID
The unique ID of the review. It must be in UUID format — not the numeric sequence ID shown in the Reviews UI. To find the review ID, call GET reviews.
Response
HTTP Status Code Summary
200
OK
Successfully retrieved the review.
400
Bad Request
Bad request. The input parameters were invalid.
403
Forbidden
Forbidden. The user does not have permission to access this resource.
404
Not Found
Not found. The resource does not exist or is inaccessible.
500
Internal Server Error
An unexpected server error occurred.
Response
Body Structure (200)
 Expand all
id
string: UUID
The unique identifier of the review.
sequenceId
int
A unique, auto-incrementing number assigned to the review when it is first submitted.
This ID does not change, even if the review is sent back to the initiator and goes through multiple rounds. It identifies the review within the project and reflects the order in which reviews were created.

name
string
The name of the review.
status
enum:string
The current status of the review.
Possible values: OPEN, CLOSED, VOID, FAILED.

currentStepId
string
The ID of the current step in the review.
currentStepDueDate
datetime: ISO 8601
The due date of the current step.
createdBy
object
Information about the user who initiated the review.
createdAt
datetime: ISO 8601
The date time when the review was initiated.
updatedAt
datetime: ISO 8601
The date time when the review was last updated.
finishedAt
datetime: ISO 8601
The date time when the review was completed.
archived
boolean
Indicates whether the review has been archived.
true: the review is archived.

false: (default) the review is active.

archivedBy
object
Information about the user who archived the review.
archivedAt
datetime: ISO 8601
The date and time when the review was archived. If the review has not been archived, this value is null.
workflowId
string: UUID
The unique identifier (UUID) of the approval workflow used to create this review.
nextActionBy
object
Information about the claimers and candidates responsible for the current step.
Example
Successfully retrieved the review.

Request
curl -v 'https://developer.api.autodesk.com/construction/reviews/v1/projects/563a4c30-e30d-4869-ac02-2a18b6447abe/reviews/73c8b3ec-eea2-4240-9c69-f9563e2fec0c' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "id": "37d5145b-c634-407c-b0b4-a65197e43fce",
  "sequenceId": 23,
  "name": "3rd Floor Design Review",
  "status": "OPEN",
  "currentStepId": "Lane_uJtTI3vjaF",
  "currentStepDueDate": "2024-11-09T01:42:16.600Z",
  "createdBy": {
    "autodeskId": "HWUBNU689CRU",
    "name": "James Smith"
  },
  "createdAt": "2024-11-06T01:42:17.476Z",
  "updatedAt": "2024-11-07T12:33:36.421Z",
  "finishedAt": "2024-11-10T02:33:17.336Z",
  "archived": false,
  "archivedBy": {
    "autodeskId": "TTFMLCMCRG5F",
    "name": "Tim Hudson"
  },
  "archivedAt": "2024-11-19T01:38:27.306Z",
  "workflowId": "0b43cedf-5c02-462b-8166-7dfbb13d3476",
  "nextActionBy": {
    "claimedBy": [
      {
        "autodeskId": "HWUBNU689CRU",
        "name": "James Smith"
      }
    ],
    "candidates": {
      "roles": [
        {
          "autodeskId": "1473817",
          "name": "Architect"
        }
      ],
      "users": [
        {
          "autodeskId": "HWUBNU689CRU",
          "name": "James Smith"
        }
      ],
      "companies": [
        {
          "autodeskId": "26980302",
          "name": "Autodesk Co. Ltd."
        }
      ]
    }
  }
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Get the Workflow For This Review
GET	projects/{projectId}/reviews/{reviewId}/workflow
Retrieves the approval workflow associated with a specific review.

This endpoint provides the exact workflow structure used when the review was created, including its steps, candidates, approval status options, and post-review actions.

To retrieve all workflows defined in a project (not just for one review), call GET workflows.

For more details about reviews, see the Help documentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/reviews/v1/projects/{projectId}/reviews/{reviewId}/workflow
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
* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can provide the project ID with or without the “b." prefix.

Example with prefix: b.563a4c30-e30d-4869-ac02-2a18b6447abe
Example without prefix: 563a4c30-e30d-4869-ac02-2a18b6447abe
reviewId
string: UUID
The unique ID of the review. It must be in UUID format — not the numeric sequence ID shown in the Reviews UI. To find the review ID, call GET reviews.
Response
HTTP Status Code Summary
200
OK
Successfully retrieved the requested review workflow data
400
Bad Request
Bad request. The input parameters were invalid.
403
Forbidden
Forbidden. The user does not have permission to access this resource.
404
Not Found
Not found. The resource does not exist or is inaccessible.
500
Internal Server Error
An unexpected server error occurred.
Response
Body Structure (200)
 Expand all
name
string
The name of the workflow. It must be unique within the project.
Max length: 255

description
string
A description of the workflow.
Max length: 4096

notes
string
A custom note associated with the workflow. Visible to all reviewers during the review process.
Max length: 4096

additionalOptions
object
Workflow-level settings that control whether the initiator can modify certain fields when starting a review.
id
string: UUID
The ID of the workflow.
approvalStatusOptions
array: object
A list of file review status options to the workflow, which contains two built in options returned by the system.
steps
array: object
A list of steps specify the details for each step in the workflow.
copyFilesOptions
object
(Copy approved files in the UI) The configuration for copying approved files to a target folder when the review is complete.
attachedAttributes
array: object
(Update Attributes in the UI) The list of attributes added in the Update Attributes action.
These attributes will be applied to the approved files in the target folder, or optionally also in the source folder depending on the configuration.

updateAttributesOptions
object
The configuration for applying attribute updates when a review is completed. This applies only if the workflow includes a file copy action and the Update Attributes action is enabled.
Example
Successfully retrieved the requested review workflow data

Request
curl -v 'https://developer.api.autodesk.com/construction/reviews/v1/projects/563a4c30-e30d-4869-ac02-2a18b6447abe/reviews/73c8b3ec-eea2-4240-9c69-f9563e2fec0c/workflow' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "name": "Final Structural Review",
  "description": "Used to review structural plans before finalizing IFC drawings.",
  "notes": "Please check all rebar annotations before approving. Include markup if changes are required.",
  "additionalOptions": {
    "allowInitiatorToEdit": true
  },
  "id": "dab28823-7ecc-47b4-a92a-37540d777751",
  "approvalStatusOptions": [
    {
      "label": "Approved w/ comments",
      "value": "APPROVED",
      "id": "b2a3c3b7-4fef-40a4-868b-981b23e7182f",
      "builtIn": false
    }
  ],
  "steps": [
    {
      "name": "Reviewer",
      "type": "REVIEWER",
      "duration": 3,
      "dueDateType": "CALENDAR_DAY",
      "groupReview": {
        "enabled": true,
        "type": "MINIMUM",
        "min": 3
      },
      "id": "Lane_uJtTI3vjaF",
      "candidates": {
        "roles": [
          {
            "autodeskId": "1473817",
            "name": "Architect"
          }
        ],
        "users": [
          {
            "autodeskId": "HWUBNU689CRU",
            "name": "James Smith"
          }
        ],
        "companies": [
          {
            "autodeskId": "26980302",
            "name": "Autodesk Co. Ltd."
          }
        ]
      }
    }
  ],
  "copyFilesOptions": {
    "enabled": true,
    "allowOverride": false,
    "condition": "ANY",
    "folderUrn": "urn:adsk.wipprod:fs.folder:co.CplBAmvXRWGqsvN1Nabvd2",
    "includeMarkups": false,
    "disableOverrideMarkupSetting": false
  },
  "attachedAttributes": [
    {
      "id": 1001,
      "required": false
    }
  ],
  "updateAttributesOptions": {
    "enableAttachedAttributes": false,
    "updateSourceAndCopiedFiles": false
  }
}

Documentation /Autodesk Construction Cloud APIs /API Reference
List Review Progress
GET	projects/{projectId}/reviews/{reviewId}/progress
Retrieves the progress of a specific review in the specified project.

This endpoint tracks the current state of each step in the review’s approval workflow, showing the assigned candidates, whether steps have been claimed or submitted, and who performed each action. Results are returned in reverse chronological order (most recent action first).

Note that this endpoint only returns data for the current round of the review.

To retrieve the review’s configuration and metadata, call GET reviews/:reviewId.

For more details about reviews, see the Help documentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/reviews/v1/projects/{projectId}/reviews/{reviewId}/progress
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
The ID of a user on whose behalf the request is made. Your application has access to all users specified by the administrator in the SaaS Integrations UI. Use this header to specify which user should be affected by the request.
This header is only required when using two-legged authentication. It is not needed for three-legged authentication.

Only user’s Autodesk ID (autodeskId) can be accepted.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can provide the project ID with or without the “b." prefix.

Example with prefix: b.563a4c30-e30d-4869-ac02-2a18b6447abe
Example without prefix: 563a4c30-e30d-4869-ac02-2a18b6447abe
reviewId
string: UUID
The unique ID of the review.
This must be the UUID, not the numeric sequence ID shown in the Reviews UI.

To find the review ID, call GET reviews.

Request
Query String Parameters
limit
int
The maximum number of review-progress records to return. Valid range: 1–50. Default: 50. For example: limit=2.
offset
int
The zero-based index of the first record to return. Use with limit for pagination. Default: 0. For example: offset=10.
Response
HTTP Status Code Summary
200
OK
The review progress was retrieved successfully.
400
Bad Request
Bad request. The input parameters were invalid.
403
Forbidden
Forbidden. The user does not have permission to access this resource.
404
Not Found
Not found. The resource does not exist or is inaccessible.
500
Internal Server Error
An unexpected server error occurred.
Response
Body Structure (200)
 Expand all
results
array: object
The list of review-progress records, returned in reverse chronological order.
pagination
object
Metadata about the paginated results.
Example
The review progress was retrieved successfully.

Request
curl -v 'https://developer.api.autodesk.com/construction/reviews/v1/projects/563a4c30-e30d-4869-ac02-2a18b6447abe/reviews/73c8b3ec-eea2-4240-9c69-f9563e2fec0c/progress?limit=2&offset=10' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "results": [
    {
      "stepId": "Lane_uJtTI3vjaF",
      "stepName": "Reviewer",
      "claimedBy": {
        "autodeskId": "HWUBNU689CRU",
        "name": "James Smith"
      },
      "actionBy": {
        "autodeskId": "HWUBNU689CRU",
        "name": "James Smith"
      },
      "candidates": {
        "roles": [
          {
            "autodeskId": "1473817",
            "name": "Architect"
          }
        ],
        "users": [
          {
            "autodeskId": "HWUBNU689CRU",
            "name": "James Smith"
          }
        ],
        "companies": [
          {
            "autodeskId": "26980302",
            "name": "Autodesk Co. Ltd."
          }
        ]
      },
      "endTime": "2024-11-19T01:38:27.306Z",
      "notes": "Please check all rebar annotations before approving. Include markup if changes are required.",
      "status": "CLAIMED"
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "totalResults": 100,
    "nextUrl": "https://developer.api.autodesk.com/construction/reviews/v1/projects/497f6eca-6276-4993-bfeb-53cbbbba6f08/reviews/73c8b3ec-eea2-4240-9c69-f9563e2fec0c/progress?limit=10&offset=10"
  }
}

Documentation /Autodesk Construction Cloud APIs /API Reference
List Review Versions
GET	projects/{projectId}/reviews/{reviewId}/versions
Retrieves the file versions included in the latest round of the specified review.

A review may go through multiple rounds when the “Back to initiator” feature is used. This endpoint only returns data from the most recent round.

The response includes approval statuses, file version names, copied version URNs (if applicable), and any custom attributes captured during the review.

For more details about reviews, see the Help documentation.

Note that to export reviewing files using these version URNs, see Step 3 in the PDF File Export tutorial.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/reviews/v1/projects/{projectId}/reviews/{reviewId}/versions
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
The ID of a user on whose behalf the request is made. Your application has access to all users specified by the administrator in the SaaS Integrations UI. Use this header to specify which user should be affected by the request.
This header is only required when using two-legged authentication. It is not needed for three-legged authentication.

Only user’s Autodesk ID (autodeskId) can be accepted.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can provide the project ID with or without the “b." prefix.

Example with prefix: b.563a4c30-e30d-4869-ac02-2a18b6447abe
Example without prefix: 563a4c30-e30d-4869-ac02-2a18b6447abe
reviewId
string: UUID
The unique ID of the review. It must be in UUID format — not the numeric sequence ID shown in the Reviews UI. To find the review ID, call GET reviews.
Request
Query String Parameters
limit
int
The number of file versions to return in the response. Possible values: 1-50. Maximum: 50. Default: 50. For example: limit=2.
offset
int
The index of the first result to return (zero-based). Default: 0. For example: offset=10.
filter[approveStatus]
array
Filters the results based on the approval status assigned to each file during the review. It should be URL-encoded.
The filter applies to the label of the approval status, as defined in the workflow — not the internal value.

For example, if your workflow includes a status labeled Approved with comments, you would filter using that label:

filter[approveStatus]=Approved with comments.

This is especially useful when a workflow includes multiple approval options with customized labels.

Note: It supports multiple values.

For example, if you want to filter with 2 labels: both Approved and Rejected, you could filter with the query string:

filter[approveStatus]=Approved&filter[approveStatus]=Rejected

Response
HTTP Status Code Summary
200
OK
Successfully retrieved the file versions in the latest review round
400
Bad Request
Bad request. The input parameters were invalid.
403
Forbidden
Forbidden. The user does not have permission to access this resource.
404
Not Found
Not found. The resource does not exist or is inaccessible.
500
Internal Server Error
An unexpected server error occurred.
Response
Body Structure (200)
 Expand all
results
array: object
A list of file versions included in the latest round of the review.
pagination
object
Metadata about the paginated results.
Example
Successfully retrieved the file versions in the latest review round

Request
curl -v 'https://developer.api.autodesk.com/construction/reviews/v1/projects/563a4c30-e30d-4869-ac02-2a18b6447abe/reviews/73c8b3ec-eea2-4240-9c69-f9563e2fec0c/versions?limit=2&offset=10&filter[approveStatus]=Approved' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "results": [
    {
      "urn": "urn:adsk.wipprod:fs.file:vf.Zvg8qMkjQ26MBJjIA2ZjeU?version=1",
      "itemUrn": "urn:adsk.wipprod:dm.lineage:Zvg8qMkjQ26MBJjIA2ZjeU",
      "approveStatus": {
        "id": "f44e623d-f04f-47fe-8195-efc43d1d985b",
        "label": "Approved",
        "value": "APPROVED"
      },
      "reviewContent": {
        "name": "3rd Floor 3D Models (shared).pdf",
        "customAttributes": [
          {
            "id": 1001,
            "type": "string",
            "name": "Reference Document Number",
            "value": "X-3910-3DWA"
          }
        ]
      },
      "copiedFileVersionUrn": "urn:adsk.wipprod:fs.file:vf.Zvg8qMkjQ26MBJjIA2ZjeK?version=3",
      "name": "3rd Floor 3D Models.pdf"
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "totalResults": 100,
    "nextUrl": "https://developer.api.autodesk.com/construction/reviews/v1/projects/497f6eca-6276-4993-bfeb-53cbbbba6f08/reviews/73c8b3ec-eea2-4240-9c69-f9563e2fec0c/versions?limit=10&offset=10"
  }
}

Documentation /Autodesk Construction Cloud APIs /API Reference
List Approval Statuses of a Version
GET	projects/{projectId}/versions/{versionId}/approval-statuses
Retrieves the full approval records and review references of a specific file version.

This includes all reviews the version has participated in, along with each review’s status (e.g., OPEN, CLOSED) and the file’s approval status (e.g., APPROVED, REJECTED) within that review.

The results are sorted in reverse chronological order within each group: those in the “In Review” status and those in the “Finished Review” status (Approved or Rejected), based on the review’s sequenceId.

This endpoint is typically used in the Files tool, where you can view the file’s activity across multiple reviews.

For more context, see the Help documentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/reviews/v1/projects/{projectId}/versions/{versionId}/approval-statuses
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
The ID of a user on whose behalf the request is made. Your application has access to all users specified by the administrator in the SaaS Integrations UI. Use this header to specify which user should be affected by the request.
This header is only required when using two-legged authentication. It is not needed for three-legged authentication.

Only user’s Autodesk ID (autodeskId) can be accepted.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can provide the project ID with or without the “b." prefix.

Example with prefix: b.563a4c30-e30d-4869-ac02-2a18b6447abe
Example without prefix: 563a4c30-e30d-4869-ac02-2a18b6447abe
versionId
string
The URL-encoded unique identifier (URN) of the file version whose review and approval history you want to retrieve.
For example, encode urn:adsk.wipprod:fs.file:vf.Ibsc4cPuQEqBHRJdBjhr6w?version=2``as ``urn%3Aadsk.wipprod%3Afs.file%3Avf.Ibsc4cPuQEqBHRJdBjhr6w%3Fversion%3D2.

To find the latest version, call GET versions and check the urn field.

Request
Query String Parameters
limit
int
The maximum number of results to return in the response. Possible values: 1–50. Maximum: 50. Default: 50. For example: limit=2.
offset
int
The number of results to skip from the beginning of the list. Used for pagination. Default: 0. For example: offset=10.
Response
HTTP Status Code Summary
200
OK
Successfully retrieved the review and approval history for the file version
400
Bad Request
Bad request. The input parameters were invalid.
403
Forbidden
Forbidden. The user does not have permission to access this resource.
404
Not Found
Not found. The resource does not exist or is inaccessible.
500
Internal Server Error
An unexpected server error occurred.
Response
Body Structure (200)
 Expand all
results
array: object
A list of approval statuses and related review information for the specified file version.
pagination
object
Metadata about the paginated results.
Example
Successfully retrieved the review and approval history for the file version

Request
curl -v 'https://developer.api.autodesk.com/construction/reviews/v1/projects/563a4c30-e30d-4869-ac02-2a18b6447abe/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.Ibsc4cPuQEqBHRJdBjhr6w%3Fversion%3D2/approval-statuses?limit=2&offset=10' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "results": [
    {
      "approvalStatus": {
        "id": "f44e623d-f04f-47fe-8195-efc43d1d985b",
        "label": "Approved",
        "value": "APPROVED"
      },
      "review": {
        "id": "37d5145b-c634-407c-b0b4-a65197e43fce",
        "sequenceId": 23,
        "status": "OPEN"
      }
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "totalResults": 100,
    "nextUrl": "https://developer.api.autodesk.com/construction/reviews/v1/projects/497f6eca-6276-4993-bfeb-53cbbbba6f08/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.Ibsc4cPuQEqBHRJdBjhr6w%3Fversion%3D2/approval-statuses?limit=50&offset=50"
  }
}

以下是 RFIS API：
Documentation /Autodesk Construction Cloud APIs /API Reference
RFIs
POST	rfi-search
Retrieves information about all the RFIs (Requests for Information) in a project, including details about their associated comments and attachments.

To retrieve full information for a specific RFI, use GET rfis/:id.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/construction/rfis/v3/projects/:projectId/search:rfis
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
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Request
Body Structure
Search request

 Expand all
limit
int
The number of RFIs to return. Default: 10. Maximum: 200.
offset
int
The number of items to skip before starting the result set. Default: 0.
search
string
Searches for a string in the title, question, and officialResponse fields.
sort
array: object
A list of sort rules to apply. Each item includes a field to sort by and the sort order.
filter
object
A set of optional filters to narrow the results. You can combine multiple filters.
fields
array: string
Specify which attributes to include in the response.
Use this to limit the response to only the fields you need.

For example, fields=id, title.

Response
HTTP Status Code Summary
200
OK
A list of RFIs
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
A list of RFIs

Request
curl -v 'https://developer.api.autodesk.com/construction/rfis/v3/projects/:projectId/search:rfis' \
  -X 'POST' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a' \
  -H 'Content-Type: application/json' \
  -d '{
        "limit": 10,
        "offset": 0,
        "search": "HVAC duct routing",
        "sort": [
          {
            "field": "createdAt",
            "order": "DESC"
          }
        ],
        "filter": {
          "status": "draft",
          "officialResponseStatus": "answered",
          "includeHidden": false,
          "assignedTo": [
            "PER8KQPK2JRT"
          ],
          "locations": [
            "AJJASD2-FFE3",
            "JTOEN-FFD33"
          ],
          "createdAt": "2018-08-01T08:56:48.699Z",
          "updatedAt": "2018-08-01T08:56:48.699Z",
          "closedAt": "2018-08-01T08:56:48.699Z",
          "createdBy": [
            "PER8KQPK2JRT"
          ],
          "dueDate": "2018-08-01T08:56:48.699Z",
          "costImpact": "Yes",
          "scheduleImpact": "Yes",
          "priority": "Low",
          "id": [
            "1e6d1d7b-1b1b-4b1b-8b1b-1b1b1b1b1b1b"
          ],
          "reference": "RFI-235-A1",
          "discipline": "Architechural",
          "category": "Constructability",
          "customAttributes": "fd9a1234-aaaa-4444-bbbb-8888aa77ee66: value-id-1",
          "rfiTypeId": [
            "1e6d1d7b-1b1b-4b1b-8b1b-1b1b1b1b1b1b"
          ]
        },
        "fields": [
          "id"
        ]
      }'
Show Less
Response
{
  "results": [
    {
      "id": "31a3f98d-34a8-4d4c-a362-3cc9de44f89c",
      "customIdentifier": "ID-1234",
      "title": "RFI - pipe is not in right place",
      "question": "Where should we put the pipe?",
      "virtualFolderUrn": "urn:adsk.wip:fs.folder:co.1838SAGCQ3SPn7lqOXMaJQ",
      "status": "open",
      "previousStatus": "submitted",
      "workflowType": "US",
      "assignedTo": [
        {
          "id": "PER8KQPK2JRT",
          "type": "user"
        }
      ],
      "managerId": "KOR8KQPK2GHF",
      "constructionManagerId": "ALW8KQPK2PTB",
      "architects": [
        {
          "type": "user",
          "id": "TKG8KQPK2MNB"
        }
      ],
      "reviewers": [
        {
          "type": "user",
          "id": "IKJ8KQPK2WDV"
        }
      ],
      "dueDate": "2018-01-12T13:06:39.216Z",
      "locationDescription": "In the middle of the room.",
      "locations": [
        "AJJASD2-FFE3",
        "JTOEN-FFD33"
      ],
      "commentsCount": 15,
      "officialResponse": "The measurements are correct.",
      "officialResponseStatus": "answered",
      "officialResponseActors": [
        {
          "id": "AJJASD2-FFE3",
          "type": "user"
        },
        {
          "id": "JTOEN-FFD33",
          "type": "user"
        }
      ],
      "officialResponseEditByManagerState": true,
      "respondedAt": "2018-01-12T13:06:39.216Z",
      "respondedBy": "RFV8KQPK2KHF",
      "createdBy": "PER8KQPK2JRT",
      "createdAt": "2018-07-22T15:05:58.033Z",
      "updatedBy": "ZXC8KQPK2CVB",
      "updatedAt": "2018-07-22T15:05:58.033Z",
      "closedAt": "2018-07-22T15:05:58.033Z",
      "closedBy": "SER8KQPK2JRT",
      "containerId": "31a3f98d-34a8-4d4c-a362-3cc9de44f89c",
      "projectId": "31a3f98d-34a8-4d4c-a362-3cc9de44f89c",
      "suggestedAnswer": "The measurements are correct.",
      "coReviewers": [
        {
          "id": "WSX8KQPK2JRMJ",
          "type": "user"
        }
      ],
      "watchers": [
        {
          "id": "PER8KQPK2JRT",
          "type": "user"
        }
      ],
      "answeredAt": "2018-07-22T15:05:58.033Z",
      "answeredBy": "FGD8KQPK2JKK",
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
      "customAttributes": [
        {
          "id": "c911852d-5957-4145-9c8d-e7cfe9d564df",
          "values": [
            ""
          ],
          "isSelectable": false
        }
      ],
      "rfiTypeId": "c911852d-5957-4145-9c8d-e7cfe9d564df",
      "bridgedSource": "",
      "bridgedTarget": "",
      "bridgeSyncOutdated": "",
      "syncVersion": "",
      "permittedActions": {
        "share": "",
        "nudge": ""
      }
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "totalResults": 97
  }
}
Documentation /Autodesk Construction Cloud APIs /API Reference
RFIs
GET	rfis/:id
Retrieves detailed information about a specific RFI (Request for Information) in Autodesk Construction Cloud (ACC).

To check which RFI states a user can create RFIs in, and which attributes are required per state, use GET users/me.

For an overview of how RFIs work in the ACC web interface, see the Help documentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/rfis/v3/projects/:projectId/rfis/:rfiId
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

rfiId
string
The ID of the RFI. To find the ID, call POST search:rfis.
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
The system-generated ID of the RFI.
customIdentifier
string
The user-defined identifier of the RFI.
title
string
The title of the RFI.
question
string,null
The question submitted in the RFI.
virtualFolderUrn
string,null
The URN of the virtual folder created for the RFI. This folder stores all attachments related to the RFI.
The virtualFolderUrn is required when uploading attachments to an RFI. See the Upload Attachment tutorial for more details.

status
enum:string
The current status of the RFI. Available values depend on the RFI’s workflow type:
For single-reviewer workflows (US):
Possible values: draft, submitted, open, answered, rejected, closed, void.

For multi-reviewer workflows (EMEA):
Possible values: draft, submitted, openRev1 (manager), openRev2 (reviewers), answeredRev1, answeredManager, closed, void.

To determine the workflow type, call GET users/me and check the workflowType value.

For details on RFI workflows in the ACC UI, see About RFI Workflows – Autodesk Help.

previousStatus
enum:string
The previous status of the RFI, if one exists. This field is omitted if the RFI has no prior status (e.g., when newly created).
For single-reviewer workflows (US):
Possible values: draft, submitted, open, answered, rejected, closed, void.

For multi-reviewer workflows (EMEA):
Possible values: draft, submitted, openRev1 (manager), openRev2 (reviewers), answeredRev1, answeredManager, closed, void.

To determine the workflow type, call GET users/me and check the workflowType value.

For details on RFI workflows in the ACC UI, see About RFI Workflows – Autodesk Help.

workflowType
enum:string
The workflow type assigned to the RFI, which determines the allowed status transitions and the review path. Possible values:
US: Single-reviewer workflow
EU: Multi-reviewer workflow
This value affects how statuses like submitted, openRev1, or answeredManager behave. For status definitions, see the status and previousStatus fields.

assignedTo
array: object
The list of users assigned to the RFI.
managerId
string
The Autodesk ID of the user designated as the RFI Manager.
To find details about the user, call GET users.

constructionManagerId
string
The Autodesk ID of the user designated as the Construction Manager for this RFI.
To find details about the user, call GET users.

architects
array: object
The list of architect users associated with the RFI.
reviewers
array: object
The list of users assigned to review the RFI before it is closed.
dueDate
string,null
The date and time by which a response to the RFI is expected, in ISO 8601 format (YYYY-MM-DDThh:mm:ss.sZ).
locationDescription
string,null
The default text for the Location field when creating a new RFI.
Note that the API does not auto-populate this value. Clients are responsible for applying the default if desired.

To retrieve the default value configured for this field, call GET rfi-types.

locations
array: string
A list of predefined location IDs associated with the RFI, based on the project’s Location Breakdown Structure (LBS). To get more information about the locations, call GET nodes.
commentsCount
int
The number of comments associated with the RFI.
officialResponse
string
The text of the official response submitted for the RFI.
Always empty when creating an RFI.

officialResponseStatus
enum:string
The status of the official response to the RFI.
Possible values: unanswered, answered.

Always unanswered when creating an RFI.

officialResponseActors
array: object
The list of users who contributed to the official response.
Always empty when creating an RFI.

officialResponseEditByManagerState
boolean
true: the RFI Manager is allowed to edit the official response after submission.
false: editing the official response is disabled. (default).

respondedAt
datetime: ISO 8601
The date and time when the RFI was officially responded to, in ISO 8601 format (YYYY-MM-DDThh:mm:ss.sZ).
respondedBy
string
The Autodesk ID of the user who submitted the official response to the RFI.
To find details about the user, call GET users.

createdBy
string
The Autodesk ID of the user who created the RFI.
To find details about the user, call GET users.

createdAt
datetime: ISO 8601
The date and time when the RFI was created, in ISO 8601 format (YYYY-MM-DDThh:mm:ss.sZ).
updatedBy
string
The Autodesk ID of the user who last updated the RFI.
To find details about the user, call GET users.

updatedAt
datetime: ISO 8601
The date and time when the RFI was last updated, in ISO 8601 format (YYYY-MM-DDThh:mm:ss.sZ).
closedAt
datetime: ISO 8601
The date and time when the RFI was closed, in ISO 8601 format (YYYY-MM-DDThh:mm:ss.sZ).
closedBy
string
The Autodesk ID of the user who closed the RFI.
To find details about the user, call GET users.

containerId
string
The ID of the container.
projectId
string
The Autodesk ID of the project the RFI belongs to.
suggestedAnswer
string
A suggested answer for the RFI, typically entered by the assignee before submission of the official response.
coReviewers
array: object
A list of reviewers assigned to the RFI. Each entry may represent a user, role, or company.
watchers
array: object
A list of watchers who are notified about changes to the RFI. Each entry may represent a user, role, or company.
answeredAt
datetime: ISO 8601
The date and time when the official response to the RFI was submitted, in ISO 8601 format (YYYY-MM-DDThh:mm:ss.sZ).
Empty when creating an RFI.

answeredBy
string
The Autodesk ID of the user who submitted the official response to the RFI.
To find details about the user, call GET users.

Empty when creating an RFI.

costImpact
string,null
The default cost impact value for new RFIs of this type.
Possible values: null, Yes, No, Unknown.

To check whether cost impact options are enabled and to retrieve the default value, call GET rfi-types.

scheduleImpact
string,null
The default schedule impact value for new RFIs of this type.
Possible values: null, Yes, No, Unknown.

To verify whether schedule impact tracking is enabled for the project and what the default value is, call GET rfi-types.

priority
string,null
The default priority for new RFIs of this type.
The available priority values are configured in Project Admin.

If no default is set, this field is null.

Note that the API does not auto-populate this value when creating an RFI. Clients are responsible for applying the default if desired.

The valid priority options can be retrieved by calling GET rfi-types <en/docs/acc/v1/reference/http/rfis-RFI-types-GET/>_. Some possible values: ``null`, High, Normal, Low.

discipline
array: string
The discipline associated with the RFI. To retrieve the supported values for the current project, call GET rfi-types.
Some possible values: Building Management System, Electrical Substation, Security, Audio Visual, Food Service, Fire Alarm, Power Systems, Design Systems Integrator, Signage, Pathways, Cabling, Networks, Distributed Antenna System, Lighting, Vertical Transportation, Roofing, Architectural, Civil/Site, Concrete, Electrical, Exterior Envelope, Fire Protection, Interior/Finishes, Landscaping, Masonry, Mechanical, Plumbing, Structural, Other.’

category
array: string
A list of predefined categories to assign to the RFI.
Categories help group RFIs for filtering and reporting. Each value must match a category configured in the project’s RFI settings. Categories are case-sensitive and project-specific.

RFI categories are configured in Project Admin and may differ between projects. Call GET rfi-types to retrieve the allowed values for this field.

Some possible values: Code Compliance, Constructability, Design Coordination, Documentation Conflict, Documentation Incomplete, Field condition, Other.

reference
string
A user-provided text reference related to the RFI, such as a model number or spec reference, typically used when the RFI was created in another system.
Max length: 20

customAttributes
array: object
A list of custom attributes associated with the RFI.
rfiTypeId
string: UUID
The ID of the default RFI type assigned to the project. This is the unique identifier of the RFI type that will be selected by default when creating a new RFI.
bridgedSource
boolean
Not relevant
bridgedTarget
boolean
Not relevant
bridgeSyncOutdated
boolean
Not relevant
syncVersion
number
Not relevant
responses
array: object
A list of responses associated with this RFI.
Always empty when creating an RFI.

draftResponses
array: object
A list of draft responses associated with this RFI.
Always empty when creating an RFI.

permittedActions
object
The list of actions that are permitted for the user.
maxAssignees
int
The max amount of assignees permitted base on the RFIs current status.
Example
Success

Request
curl -v 'https://developer.api.autodesk.com/construction/rfis/v3/projects/:projectId/rfis/:rfiId' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "id": "31a3f98d-34a8-4d4c-a362-3cc9de44f89c",
  "customIdentifier": "ID-1234",
  "title": "RFI - pipe is not in right place",
  "question": "Where should we put the pipe?",
  "virtualFolderUrn": "urn:adsk.wip:fs.folder:co.1838SAGCQ3SPn7lqOXMaJQ",
  "status": "open",
  "previousStatus": "submitted",
  "workflowType": "US",
  "assignedTo": [
    {
      "id": "PER8KQPK2JRT",
      "type": "user"
    }
  ],
  "managerId": "KOR8KQPK2GHF",
  "constructionManagerId": "ALW8KQPK2PTB",
  "architects": [
    {
      "type": "user",
      "id": "TKG8KQPK2MNB"
    }
  ],
  "reviewers": [
    {
      "type": "user",
      "id": "IKJ8KQPK2WDV"
    }
  ],
  "dueDate": "2018-01-12T13:06:39.216Z",
  "locationDescription": "In the middle of the room.",
  "locations": [
    "AJJASD2-FFE3",
    "JTOEN-FFD33"
  ],
  "commentsCount": 15,
  "officialResponse": "The measurements are correct.",
  "officialResponseStatus": "answered",
  "officialResponseActors": [
    {
      "id": "AJJASD2-FFE3",
      "type": "user"
    },
    {
      "id": "JTOEN-FFD33",
      "type": "user"
    }
  ],
  "officialResponseEditByManagerState": true,
  "respondedAt": "2018-01-12T13:06:39.216Z",
  "respondedBy": "RFV8KQPK2KHF",
  "createdBy": "PER8KQPK2JRT",
  "createdAt": "2018-07-22T15:05:58.033Z",
  "updatedBy": "ZXC8KQPK2CVB",
  "updatedAt": "2018-07-22T15:05:58.033Z",
  "closedAt": "2018-07-22T15:05:58.033Z",
  "closedBy": "SER8KQPK2JRT",
  "containerId": "31a3f98d-34a8-4d4c-a362-3cc9de44f89c",
  "projectId": "31a3f98d-34a8-4d4c-a362-3cc9de44f89c",
  "suggestedAnswer": "The measurements are correct.",
  "coReviewers": [
    {
      "id": "WSX8KQPK2JRMJ",
      "type": "user"
    }
  ],
  "watchers": [
    {
      "id": "PER8KQPK2JRT",
      "type": "user"
    }
  ],
  "answeredAt": "2018-07-22T15:05:58.033Z",
  "answeredBy": "FGD8KQPK2JKK",
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
  "customAttributes": [
    {
      "id": "c911852d-5957-4145-9c8d-e7cfe9d564df",
      "values": [
        ""
      ],
      "isSelectable": false
    }
  ],
  "rfiTypeId": "c911852d-5957-4145-9c8d-e7cfe9d564df",
  "bridgedSource": "",
  "bridgedTarget": "",
  "bridgeSyncOutdated": "",
  "syncVersion": "",
  "responses": [
    {
      "id": "c911852d-5957-4145-9c8d-e7cfe9d564df",
      "state": "draft",
      "rfiId": "w332252d-5957-4145-9c8d-e7cfe9d975aj",
      "text": "The pipe should be placed in the corner",
      "status": "answered",
      "createdBy": "PER8KQPK2JRT",
      "onBehalf": "PER8KQPK2JRT",
      "isEditable": true,
      "createdAt": "2018-07-22T15:05:58.033Z",
      "updatedBy": "PER8KQPK2JRT",
      "updatedAt": "2018-07-22T15:05:58.033Z",
      "deletedAt": "2018-07-22T15:05:58.033Z"
    }
  ],
  "draftResponses": [
    {
      "id": "c911852d-5957-4145-9c8d-e7cfe9d564df",
      "state": "draft",
      "rfiId": "w332252d-5957-4145-9c8d-e7cfe9d975aj",
      "text": "The pipe should be placed in the corner",
      "status": "answered",
      "createdBy": "PER8KQPK2JRT",
      "onBehalf": "PER8KQPK2JRT",
      "isEditable": true,
      "createdAt": "2018-07-22T15:05:58.033Z",
      "updatedBy": "PER8KQPK2JRT",
      "updatedAt": "2018-07-22T15:05:58.033Z",
      "deletedAt": "2018-07-22T15:05:58.033Z"
    }
  ],
  "permittedActions": {
    "share": "",
    "nudge": "",
    "updateRfi": {
      "permittedStatuses": {
        "wfUS": [
          {
            "status": "open",
            "maxAssignees": "",
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
          }
        ],
        "wfEU": [
          {
            "status": "open",
            "maxAssignees": "",
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
          }
        ]
      },
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
      ],
      "useCustomAttributes": ""
    },
    "createComment": "",
    "createResponse": "",
    "createResponseOnBehalf": "",
    "remainingReviewers": [
      {
        "id": "PER8KQPK2JRT",
        "type": "user"
      }
    ],
    "createDocumentReference": "",
    "removeDocumentReference": ""
  },
  "maxAssignees": 10
}


Documentation /Autodesk Construction Cloud APIs /API Reference
RFIs
GET	users/me
Retrieves information about the current user in the context of the specified project. The response includes the user’s assigned RFI workflow roles, whether the user is permitted to create RFIs, the workflow states in which the user can create RFIs, and the attributes required in each state.

We strongly recommend calling this endpoint before creating an RFI, to ensure the user has the necessary permissions and the latest configuration for the project.

The RFIs API does not currently support adding users to a project or assigning workflow roles. Only project members can create or edit RFIs.

To add responses or attachments to the RFI, call POST responses after the RFI is created.

Users can create RFIs if they are assigned either the creator (projectSC) or manager (projectGC) workflow role. These roles must be explicitly configured in the RFI tool settings by going to RFIs → Settings → Permissions in the Autodesk Construction Cloud (ACC) web interface. There is no default workflow role, so project members will not be able to create RFIs unless one of these roles is assigned.

To check if a user can create RFIs, look for the createRfi object inside the permittedActions section of the response.

Workflow roles must be assigned manually via the UI. There is currently no API support for modifying workflow roles.

The table below lists the Project Admin workflow role names and their corresponding RFIs API role names:

Project Admin Module Workflow Role Name	RFIs API Workflow Role Name
Creator	Subcontractor (projectSC)
Manager	General Contractor (projectGC)
Reviewer 1 (EMEA workflow)	Construction Manager (projectCoordinator)
Reviewer (US workflow) / Reviewer 2 (EMEA workflow)	Architect (projectReviewer)
For more information, see the RFIs permissions documentation.

The table below shows the workflow names used in the Project Admin UI and their corresponding values in the RFIs API:

Project Admin Module Workflow Type Name	RFIs API Workflow Type Name
Default Workflow	US
Workflow with Additional Reviewer	EMEA
You can use either workflow type (US or EMEA) in both the US and EMEA regions. To assign a workflow type to a project, use the Project Admin UI.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/rfis/v3/projects/:projectId/users/me
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
The current user’s details.
permittedActions
object
The list of actions that are permitted for the user.
workflow
object
The user’s assigned workflow roles and workflow type for RFIs in the current project.
defaultRfiType
string: UUID
The ID of the default RFI type assigned to the project. This is the unique identifier of the RFI type that will be selected by default when creating a new RFI.
externalUsers
array: object
Not relevant
maintenanceEndDate
string
Not relevant
Example
Success

Request
curl -v 'https://developer.api.autodesk.com/construction/rfis/v3/projects/:projectId/users/me' \
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
      "permittedStatuses": {
        "wfUS": [
          {
            "status": "open",
            "maxAssignees": "",
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
          }
        ],
        "wfEU": [
          {
            "status": "open",
            "maxAssignees": "",
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
          }
        ]
      }
    }
  },
  "workflow": {
    "roles": [
      "projectSC"
    ],
    "type": "US"
  },
  "defaultRfiType": "c911852d-5957-4145-9c8d-e7cfe9d564df",
  "externalUsers": [
    {
      "email": "",
      "autodeskId": ""
    }
  ],
  "maintenanceEndDate": ""
}

