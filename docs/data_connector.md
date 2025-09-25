Documentation /Autodesk Construction Cloud APIs /How-to Guide
Submit a Data Request
This phase of the tutorial demonstrates how to submit a data request that extracts service data from within a BIM 360/ACC account. In this tutorial, your data request will be a recurring request that spawns a job once every week, and returns extracted data for seven different services.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with data:create, data:read, and data:write scopes. The token’s authenticated user must have executive overview permissions or project administrator permissions.
Verify that you have access to a relevant BIM 360/ACC account that contains at least one project. If you don’t know your account ID, you can derive it from your hub ID: Use GET hubs in the Data Management API to retrieve your hub ID. Remove the initial “b.” from the hub ID to get your account ID. For example, a hub ID of b.c8b0c73d-3ae9 translates to an account ID of c8b0c73d-3ae9.
Step 1: Determine Your Data Parameters
To make a data request, you’ll have to provide request parameter values that correctly specify the type of data extraction you want the Data Connector service to perform and to provide other useful information stored with the request:

description contains a text string describing the data request, in this case "My Weekly Extract".
scheduleInterval specifies the interval unit we’ll use for scheduling. In this case we measure in weeks, so the value is WEEK.
reoccuringInterval specifies the number of units to wait between job spawns. Because we want this request to spawn a job once every week, the value is 1.
effectiveFrom and effectiveTo define the starting and ending times for the recurring jobs. It’s during this time that the jobs spawn and execute, starting on the effectiveFrom time and ending on the effectiveTo time. These two values define date and time in ISO 8601 format. For this example, we’ll set a one-year interval. Our example values: 2020-11-19T16:00:00Z start time, 2021-11-19T16:00:00Z end time.
serviceGroups defines the scope of the data extraction for this data request: the services for which we want to examine data. In this case, we look at admin, issues, locations, submittals, cost, and rfis. You can also specify all to extract data for all service groups. Note that the admin service covers both project and account administration.
projectId specifies which project to extract data from. Usage depends on the permissions level of the authenticated user:
Executive Overview permissions — (optional) If neither projectId or projectIdList is specified, the request will apply to all projects in the user’s account.
Project Administrator permissions — (required) If neither projectId or ``projectIdList` is specified, the request will fail.
projectIdList specifies the list of projects to extract data from. projectId can be omitted if projectIdList is used. If both are provided, projectIdList takes precedence. The user needs to have either Executive Overview permission, or Project Administrator permission in all the projects provided in the list. Otherwise, the request will fail.
projectStatus specifies the scope of the projects based on the project status. Use active if only data extraction from active projects is required.
Step 2: Create a Data Request
Create a data request using the POST requests endpoint, specifying the account ID of your account. This tutorial demonstrates recurring data requests for two scenarios:

Retrieving data for a specific list of projects using projectIdList.
Retrieving data for all active projects in the account using projectStatus.
Scenario 1: Requesting Data for Specific Projects
If the user wants to extract data for specific projects, include the projectIdList field in the request payload. This field specifies up to 50 project IDs.

Request
curl -X POST 'https://developer.api.autodesk.com/data-connector/v1/accounts/<accountId>/requests' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <authToken>' \
-d '

{
    "description": "My Weekly Extract",
    "scheduleInterval": "WEEK",
    "reoccuringInterval": 1,
    "effectiveFrom": "2020-11-19T16:00:00Z",
    "effectiveTo": "2021-11-19T16:00:00Z",
    "serviceGroups": ["admin", "issues", "locations", "submittals", "cost", "rfis"],
    "projectIdList": [
    "ffffffff-1f51-4b26-a6b7-6ac0639cb138",
    "aaaaaaaa-1f51-4b26-a6b7-6ac0639cb138"        ]
}'
Show Less
Response
{
    "id": "55e410c5-4294-44ce-becf-68e1cfd6738c",
    "isActive": true,
    "accountId": "872264f8-2433-498d-8d36-16649ecb13fe",
    "projectId": null,
    "projectIdList": [
    "ffffffff-1f51-4b26-a6b7-6ac0639cb138",
    "aaaaaaaa-1f51-4b26-a6b7-6ac0639cb138"
  ],
    "description": "My Weekly Extract",
    "createdBy": "73f00c25-a5f9-4c05-861d-ce56d54fa649",
    "createdByEmail": "your.name@autodesk.com",
    "updatedBy": "73f00c25-a5f9-4c05-861d-ce56d54fa649",
    "scheduleInterval": "WEEK",
    "reoccuringInterval": 1,
    "effectiveFrom": "2020-11-19T16:00:00.000Z",
    "effectiveTo": "2021-11-19T16:00:00.000Z",
    "nextExecAt": "2020-11-19T16:00:00.000Z",
    "serviceGroups": [
        "admin",
        "issues",
        "locations",
        "submittals",
        "cost",
        "rfis"
    ],
    "callbackUrl": null,
    "lastQueuedAt": null,
    "updatedAt": "2020-11-19T16:32:13.545Z",
    "createdAt": "2020-11-19T16:32:13.545Z",
    "deletedAt": null    }
Show Less
Scenario 2: Requesting Data for Active Projects
If the user has executive overview permissions and wants to retrieve data for all active projects in the account, use the projectStatus field.

Request
curl -X POST 'https://developer.api.autodesk.com/data-connector/v1/accounts/<accountId>/requests' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <authToken>' \
-d '

{
    "description": "My Weekly Extract",
    "scheduleInterval": "WEEK",
    "reoccuringInterval": 1,
    "effectiveFrom": "2020-11-19T16:00:00Z",
    "effectiveTo": "2021-11-19T16:00:00Z",
    "serviceGroups": ["admin", "issues", "locations", "submittals", "cost", "rfis"],
    "projectStatus": "active"
}'
Show More
Response
{
    "id": "55e410c5-4294-44ce-becf-68e1cfd6738c",
    "isActive": true,
    "accountId": "872264f8-2433-498d-8d36-16649ecb13fe",
    "description": "My Weekly Extract",
    "createdBy": "73f00c25-a5f9-4c05-861d-ce56d54fa649",
    "createdByEmail": "your.name@autodesk.com",
    "updatedBy": "73f00c25-a5f9-4c05-861d-ce56d54fa649",
    "scheduleInterval": "WEEK",
    "reoccuringInterval": 1,
    "effectiveFrom": "2020-11-19T16:00:00.000Z",
    "effectiveTo": "2021-11-19T16:00:00.000Z",
    "nextExecAt": "2020-11-19T16:00:00.000Z",
    "serviceGroups": [
        "admin",
        "issues",
        "locations",
        "submittals",
        "cost",
        "rfis"
    ],
    "callbackUrl": null,
    "lastQueuedAt": null,
    "updatedAt": "2020-11-19T16:32:13.545Z",
    "createdAt": "2020-11-19T16:32:13.545Z",
"deletedAt": null,
"projectStatus": "active"
Show Less
The response reports the data request settings and status, and includes an id value that provides the data request ID. Use the data request ID to specify this data request when calling other Data Connector API endpoints. If you don’t save the ID, you can query the API (as we’ll do in the next example) for the data request IDs of your data requests currently stored by the Data Connector service.

Notice that optional field values not set in the request get set to default values.


Documentation /Autodesk Construction Cloud APIs /How-to Guide
Find and Update a Data Request
This tutorial shows how to find and update an existing data request stored by the Data Connector service. For this example, we’ll change the description of the data request created in the last tutorial. We’ll start by retrieving all your currently saved data requests so that we can find the appropriate data request and its data request ID. We’ll then examine the data request’s current settings, and change its description.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with data:create, data:read, and data:write scopes. The token’s authenticated user must have executive overview permissions.
Verify that you have access to a relevant BIM 360 account that contains at least one project. If you don’t know your account ID, you can derive it from your hub ID: Use GET hubs in the Data Management API to retrieve your hub ID. Remove the initial “b.” from the hub ID to get your account ID. For example, a hub ID of b.c8b0c73d-3ae9 translates to an account ID of c8b0c73d-3ae9.
Step 1: Get a List of Saved Requests
Use GET requests to retrieve a list of your saved data requests. This endpoint retrieves a list that is restricted to the requester’s saved data requests, so it won’t list any data requests created by other users. If you have many saved data requests, you can set request parameters to limit the number of returned requests, offset the point where you start returning requests, and set sort order. We won’t specify any of this, so the endpoint will use default settings of ascending sort order, a limit of 20 requests, and no offset.

Request
curl -X GET 'https://developer.api.autodesk.com/data-connector/v1/accounts/<accountId>/requests?limit=20&sort=desc' \
-H 'Authorization: Bearer <authToken>'
Response
{
    "pagination": {
        "limit": 20,
        "offset": 0,
        "totalResults": 1
    },
    "results": [
        {
            "id": "55e410c5-4294-44ce-becf-68e1cfd6738c",
            "description": "My Weekly Extract",
            "isActive": true,
            "accountId": "872264f8-2433-498d-8d36-16649ecb13fe",
            "projectId": "ffffffff-1f51-4b26-a6b7-6ac0639cb138",
            "createdBy": "73f00c25-a5f9-4c05-861d-ce56d54fa649",
            "createdByEmail": "your.name@autodesk.com",
            "updatedBy": "73f00c25-a5f9-4c05-861d-ce56d54fa649",
            "scheduleInterval": "WEEK",
            "reoccuringInterval": 1,
            "effectiveFrom": "2020-11-19T16:00:00.000Z",
            "effectiveTo": "2021-11-19T16:00:00.000Z",
            "lastQueuedAt": "2020-11-19T16:32:54.725Z",
            "nextExecAt": "2020-11-26T16:00:00.000Z",
            "serviceGroups": [
                "admin",
                "issues",
                "locations",
                "submittals",
                "cost",
                "rfis"
            ],
            "callbackUrl": null,
            "createdAt": "2020-11-19T16:32:13.545Z",
            "updatedAt": "2020-11-19T16:32:54.728Z",
            "deletedAt": null
        }
    ]
}
Show Less
The results returned by this endpoint report the ID, settings, and status of each data request (in this case just the single data request we created in the last tutorial). We’ll use the ID of the data request in the next step when we update the data request.

Note that if you have the ID of a single data request for which you want to see status, you can use the GET requests/:requestId endpoint instead of this endpoint to retrieve the request’s status without having to list other data requests.

Step 2: Change Your Request’s Active Status
To update your data request’s description, use the PATCH requests endpoint. It accepts a set of parameter settings that you want to change in the data request. You don’t need to specify all the parameters settings, just the one you want to change. In this example, it’s description. We’ll change it to “My Updated Weekly Extract”.

Request
curl -X PATCH 'https://developer.api.autodesk.com/data-connector/v1/accounts/<accountId>/requests/<requestId>' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <authToken>' \
-d '{
    "description": "My Updated Weekly Extract"
}'
Response
{
    "id": "55e410c5-4294-44ce-becf-68e1cfd6738c",
    "description": "My Updated Weekly Extract",
    "isActive": true,
    "accountId": "872264f8-2433-498d-8d36-16649ecb13fe",
    "projectId": "ffffffff-1f51-4b26-a6b7-6ac0639cb138",
    "createdBy": "73f00c25-a5f9-4c05-861d-ce56d54fa649",
    "createdByEmail": "your.name@autodesk.com",
    "updatedBy": "73f00c25-a5f9-4c05-861d-ce56d54fa649",
    "scheduleInterval": "WEEK",
    "reoccuringInterval": 1,
    "effectiveFrom": "2020-11-19T16:00:00.000Z",
    "effectiveTo": "2021-11-19T16:00:00.000Z",
    "lastQueuedAt": "2020-11-19T16:32:54.725Z",
    "nextExecAt": "2020-11-26T16:00:00.000Z",
    "callbackUrl": null,
    "createdAt": "2020-11-19T16:32:13.545Z",
    "updatedAt": "2020-11-19T16:35:13.912Z",
    "deletedAt": null,
    "serviceGroups": [
        "admin",
        "issues",
        "locations",
        "submittals",
        "cost",
        "rfis"
    ]
}
Show Less
The response contains the updated parameter settings for your specified data request.


Documentation /Autodesk Construction Cloud APIs /How-to Guide
Find a Job and Retrieve Its Data Extract
When an active data request spawns a job, the job extracts data for specified services. To retrieve and examine that data, you need the ID of the job. You receive that ID through the email notification that the job sends on completion and, if you specified a callback URL, a post that the job sends on completion. You may also retrieve a list of jobs spawned by the data request. There you can find the ID of a job whose data extract you wish to examine.

To retrieve the job’s data extract, first use the job ID to retrieve descriptions of the files in the data extract. You can use those descriptions to determine which of the files you’d like to examine, and then request a URL where you can retrieve your desired files.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with data:create, data:read, and data:write scopes. The token’s authenticated user must have executive overview permissions.
Verify that you have access to a relevant BIM 360 account that contains at least one project. If you don’t know your account ID, you can derive it from your hub ID: Use GET hubs in the Data Management API to retrieve your hub ID. Remove the initial “b.” from the hub ID to get your account ID. For example, a hub ID of b.c8b0c73d-3ae9 translates to an account ID of c8b0c73d-3ae9.
Step 1: Get a List of Jobs Spawned By Your Data Request
In this example, we’ll assume you don’t have the ID of the job whose data extract you want. Use the GET requests/:requestId/jobs endpoint to retrieve a list of the jobs that your data request has spawned, or use the GET jobs endpoint to retrieve a list of all the jobs that were spawned for the project you specify. If you think there are many spawned jobs, you can set request parameters to limit the number of returned job descriptions, offset the point where you start returning requests, and set sort order. We won’t specify any of this, so the endpoint will use default settings of ascending sort order, a limit of 20 requests, and no offset.

You’ll need the ID of the data request that spawned the jobs, something you retrieved in the previous tutorials.

Request
curl -X GET 'https://developer.api.autodesk.com/data-connector/v1/accounts/<accountId>/requests/<requestId>/jobs?sort=desc&limit=10&offset=0' \
-H 'Authorization: Bearer <authToken>'
Response
{
    "pagination": {
        "limit": 10,
        "offset": 0,
        "totalResults": 1
    },
    "results": [
        {
            "id": "9bd7c8a0-9fde-478b-82b7-44098d27c1c1",
            "requestId": "55e410c5-4294-44ce-becf-68e1cfd6738c",
            "accountId": "872264f8-2433-498d-8d36-16649ecb13fe",
            "projectId": "ffffffff-1f51-4b26-a6b7-6ac0639cb138",
            "createdBy": "73f00c25-a5f9-4c05-861d-ce56d54fa649",
            "createdByEmail": "your.name@autodesk.com",
            "status": "complete",
            "completionStatus": "success",
            "startedAt": "2020-11-19T16:33:04.688Z",
            "completedAt": "2020-11-19T16:34:05.293Z",
            "createdAt": "2020-11-19T16:32:54.672Z"
        }
    ]
}
Show Less
The response provides an array of job records (in this case, just a single job), each with information about a job’s status. The beginning of each record is the ID of the job, which you’ll use to specify the job in subsequent endpoint calls.

Step 2: Examine the Files Contained in the Job’s Data Extract
To see a list of the files contained in your job’s data extract, use the GET jobs/:jobId/data-listing endpoint and use the job ID to specify the job.

Request
curl -X GET 'https://developer.api.autodesk.com/data-connector/v1/accounts/<accountId>/jobs/<jobId>/data-listing' \
-H 'Authorization: Bearer <authToken>'
Response
[
    {
        "name": "README.html",
        "createdAt": "2020-11-19T16:34:04.579Z",
        "size": 8892
    },
    {
        "name": "admin_account_services.csv",
        "createdAt": "2020-11-19T16:33:05.058Z",
        "size": 117
    }

...numerous other .csv file listings...

    {
        "name": "admin_users.csv",
        "createdAt": "2020-11-19T16:33:05.106Z",
        "size": 3104
    },
    {
        "name": "autodesk_data_extract.zip",
        "createdAt": "2020-11-19T16:34:04.591Z",
        "size": 53792
    },

...numerous other .csv file listings...

    {
        "name": "submittals_specs.csv",
        "createdAt": "2020-11-19T16:33:35.170Z",
        "size": 125
    }
]
Show Less
The first file is a README file that contains information about the schema used in each of the CSV files in the data extract. Listed a bit later is a ZIP file that contains all of the other files in the data extract including the README file. The other files are each CSV files for a particular type of object within a service. Each of the file descriptions returns the filename, when the file was created, and the size of the file in bytes.

Step 3: Retrieve a File From a Data Extract
Once you have a job ID and the filename of the file in the data extract that you’d like to retrieve, use GET jobs/:jobId/data/:name to get a signed URL where you can retrieve that data, in this case the ZIP file that contains all the files in the extract along with information about the schemas used.

Request
curl -X GET 'https://developer.api.autodesk.com/data-connector/v1/accounts/<accountId>/jobs/<jobId>/data/autodesk_data_extract.zip' \
-H 'Authorization: Bearer <authToken>'
Response
{
    "name": "autodesk_data_extract.zip",
    "size": 53792,
    "signedUrl": "https://bim360dc-p-ue1-extracts.s3.amazonaws.com/data/872264e8-2433-498d-8d36-16649ecb13fe/9bd7c8a0-9fde-478b-82b7-44098d27c1c1/autodesk_data_extract.zip?AWSAccessKeyId=ASIAWZ7KRFT5U5KAQRUI&Expires=1605806413&Signature=5T68bvEaz0f6p4U%2FDZgmpub957c%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEOn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCICvo%2F3hehNnqaTXjleNDCmA6p%2F3yWvrsonrBE4nql5ZZAiEAtjSD1kSupwy2vr%2Bp%2Ftt4TBbHj%2BqorI9iRSMeZzTJe1kq2gEIYhACGgw0NjgxMDY0MjM1NDciDDV9RA39yMDubKMpOSq3AWO%2BzbHgSMkHe180nF2Pj050zZiwml94Ux0CJvGtOzfLrQXHWuEjSsddk6DllxLKp%2BGlFBezGkPeRnAlZRVrDXlAyJu%2FensrqPmPXmugluRmvfblAehj7%2FqwsRTFCbJhzJELMQ40GvyEBMXJMJ5gQ8lcAXrxg6TReuBr8mSHmn5U%2F5r56HwwwO3ddOgw%2FfwUY8mQ%2BIjpbF45EMKDJxCqdL2zA2quQKZ617O4%2FIq4eJl6%2F42J10nK%2FzC%2Ft9r9BTrgASDpnOPAkrMIl44%2FXyucqjMQ8A9Dk8DLAKQiV2SXYxdGyONXLpDdCYc0ZGlVcSOGIJq0J2QYMFKAABT6BipiGq%2FFn8RYeWSZO17Y%2FogJCC6TZipvJD0XbYm%2Bi%2FGfRO9%2BPjK8y1DAPtZE1SWA%2F21uWEigbNXTt9AWKnYUzdojNoz9uFKEmRXf8HA95AU%2Ftc3Q%2FxMoV0f8b0h%2FtbecyljXxCMRfnrhGJ1uaSGTIyVpHuDti0hWCDxFjVODC4mUYqrQoKzwQC6jNjohVqiagKZVNK5MTlA6jhp6U9xQdn8tCOjO"
}
Use the signed URL returned in the response within 60 seconds. It will return the specified ZIP file from the data extract.