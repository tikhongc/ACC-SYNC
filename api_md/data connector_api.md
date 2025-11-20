Documentation /Autodesk Construction Cloud APIs /API Reference
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