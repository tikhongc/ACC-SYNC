Documentation /Webhooks API /How-to Guide
Creating a Webhook and Listening to BuildingConnected Events
This walkthrough demonstrates how to create a webhook to register callbacks for BuildingConnected events. The steps include finding the scope ID for the events, choosing the event type for the webhook to listen for, preparing to handle callbacks, and creating the webhook.

For more details about the BuildingConnected API, see the BuildingConnected Field Guide.

Before You Begin
Create a BuildingConnecteed account.
Link the BuildingConnected user to an Autodesk ID. See How to connect your Autodesk ID to BuildingConnected for details.
Subscribe to the relevant BuildingConnected product for each event:
For Bid events subcribe to BuildingConnected Pro.
For Opportunity events subcribe to Bid Board Pro.
Register an app, and select the BuildingConnected API.
Acquire a 3-legged OAuth token with data:read and data:create authentication scopes. For information about authentication scopes, see the Scopes section in the Data Management API Basics page.
Step 1 : Find the Scope ID for BuildingConnected Events
The Webhooks service uses the company ID as the scope for BuildingConnected events. To retrieve the company ID (results.companyId), call GET users/me </en/docs/buildingconnected/v2/reference/http/buildingconnected-users-me-GET/>`_.

For more information about webhook scopes, see the Field Guide.

Step 2 : Select an Event Type for Webhook Registration
The Webhooks service currently supports the events listed on the BuildingConnected Events page.

You can specify multiple event types by including wildcards in the event type name. This is done using the asterisk (*) character, which represents zero or more characters in the name. For example, if you specify opportunity.comment.*-1.0, it will correspond to opportunity.comment.created-1.0, opportunity.comment.deleted-1.0, and opportunity.comment.updated-1.0.

For more information about event types and wildcards, see Supported Events.

Step 3 : Prepare to Manage Callbacks
A webhook requires a callback URL to which it will send the event data. To get started with setting up a local server, see Configuring Your Server.

Step 4 : Create a Webhook
Create a webhook by calling POST events/:event/hooks.

Hook Attribute
In some situations, specific data (such as salesforceId) might not be included in the event notification. To include such custom information in the callback payload, you can configure the webhook accordingly.

Supply the hookAttribute property with a JSON object that you want to include in the callback, such as the salesforceId, or any other details from your app.

For more information, see the Field Guide.

Filter
You might want to filter the callbacks you receive based on the payload of the callback.

Provide the filter attribute in the endpoint request payload with a JSONPath expression that specifies the callback payload field values you want to filter on.

For more information, see Callback Filtering.

Example Input Values
The input values used in this example are as follows:

system	
autodesk.construction.bc
event	
opportunity.comment.created (You can use wildcards here, such as opportunity.comment.* or *)
callback URL	
http://bf067e05.ngrok.io/callback
scope key	
project (This is the scope name for BuildingConnected events)
scope value	
d6a37470-0539-40eb-89ff-9aeb8680066d (This is the UUID of the project)
hookAttribute	
{ "projectId": "d6a37470-0539-40eb-89ff-9aeb8680066d" }
Authorization token	
Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz
Request
curl -X 'POST'
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/autodesk.construction.bc/events/opportunity.comment.created/hooks'
     -H 'Content-Type: application/json'
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'
     -d '{
           "callbackUrl": "http://bf067e05.ngrok.io/callback",
           "scope": {
             "companyId": "594206015caedd954831e5b8"
           },
           "hookAttribute": {
             "projectId": "d6a37470-0539-40eb-89ff-9aeb8680066d"
           }
         }'
Show Less
Response
Upon completion, you should receive a 201 status response from the server. The response will also include a Location header, which you need to use if you plan to delete the webhook in the future.

To verify and view the properties of the newly-created webhook, navigate to the URL provided in the Location field.

HTTP/1.1 201
Date: Thu, 14 Sep 2017 16:45:05 GMT
Location: https://developer.api.autodesk.com/webhooks/v1/systems/autodesk.construction.bc/events/opportunity.comment.created/hooks/0f60f6a0-996c-11e7-abf3-51d68cff984c
Content-Length: 0
Connection: keep-alive
Your configured callbackUrl should receive the notifications when a new comment is added to an opportunity for your company 594206015caedd954831e5b8.


Documentation /Webhooks API /How-to Guide
Creating a Webhook and Listening to Events
This walkthrough explains how to create a Webhook to register callbacks for Data Management events.

Before You Begin
Make sure that you have registered an app and successfully acquired an OAuth token .
See the Authentication and Scopes section in the API Basics for the appropriate token based on the data you are accessing.
All requests to the Webhooks Service require the data:read scope.
You need data:create scope to create a hook.
Step 1 : Find the Scope ID for events
The URNs for a particular Folder can be easily accessed using Data Management GET APIs. Please note that only folder is supported for webhooks, you can use root folder URN to create hook on the project level.

Example: GET projects/:project_id/folders/:folder_id

../../../_images/get-dm-folders.png
Field Guide
For more information about scope and webhook take a look at our Field Guide.

Step 2 : Choose event type to register the Webhook on
Webhooks service currently exposes the following types of Data Management events. Wildcards can also be specified by using the character “*” to represent the matching placeholder to substitute zero or more characters in the event type.

See Supported Events for more information about event types and wildcards.

Step 3 : Preparing to handle Callbacks
A webhook requires a callback URL where the event data is sent. See Configuring Your Server to get you started with a local server setup.

Step 4 : Create a Webhook
A webhook is created by making a POST request to webhooks/v1/systems/:system/events/:event/hooks. You can find additional details in the Reference Guide.

Example
Values used in this example are:

system	
data
event	
dm.version.added wildcards can be used here like so: dm.*
callback URL	
http://bf067e05.ngrok.io/callback
scope key	
folder scope name for Data Management events
scope value	
urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw which is a Folder URN
hookAttribute	
{ "projectId": "a.cGVyc29uYWwGcGUy0WN1NTg41z1wNTcwOD1yNDA4NDgyNg" } which is Project Id.
filter	
$[?(@.ext=='txt')] which is the extension of the item.
Authorization token	
Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz
Hook Attribute
In some scenarios some data will not be available like projectId when receiving the event but you want to have it. Use the hookAttribute property to include custom information, such as the projectId or any other information from your app. When registering the hook, add a hookAttribute key with JSON object you want to have available on your callback payload.

For more information please take a look at Field Guide

Filter
In some scenarios, you might want to filter the callbacks you receive based on the payload of the callback. When registering the hook, add a filter key with a JsonPath expression string you want the events to be filtered with.

For more information please take a look at Callback Filtering

Request
curl -X 'POST'
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.version.added/hooks'
     -H 'Content-Type: application/json'
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "scope": {
                 "folder": "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw"
            },
            "hookAttribute": {
              "projectId": "a.cGVyc29uYWwGcGUy0WN1NTg41z1wNTcwOD1yNDA4NDgyNg"
            },
            "filter": "$[?(@.ext=='txt')]"
      }'
Show Less
Response
You should receive a successful response from the server with status of 201. Additionally, you should receive Location header in the response. Location information is required to delete a webhook. Navigate to the Location URL to validate and obtain the properties of the newly-created webhook.

HTTP/1.1 201
Date: Thu, 14 Sep 2017 16:45:05 GMT
Location: https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.version.added/hooks/0f60f6a0-996c-11e7-abf3-51d68cff984c
Content-Length: 0
Connection: keep-alive
Your configured callbackUrl should receive the notifications when a file is added to the Folder urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw.

Documentation /Webhooks API /How-to Guide
Creating a Webhook and Listening to ACC Issue Events
This walkthrough demonstrates how to create a webhook to register callbacks for Autodesk Construction Cloud (ACC) Issue events. The steps include finding the scope ID for the events, choosing the event type for the webhook to listen for, preparing to handle callbacks, and creating the webhook.

For more details about the Autodesk Construction Cloud (ACC) Issues API, see the Issues API Field Guide.

Before You Begin
Register an app and select the ACC Issues API.
Acquire a 3-legged OAuth token with data:read and data:create scopes. These are required to access the Webhooks API and to create a webhook. For more information about scopes, see the Scopes section in the Authentication API.
Only users with Project Admin permissions can successfully create webhooks for ACC Issues.
Step 1 : Find the Scope ID for Events
The Webhooks service uses the project ID as the scope for ACC Issue events. To find the project ID, see the `Retrieve Project ID /en/docs/acc/v1/tutorials/getting-started/retrieve-account-and-project-id/>`_ tutorial.

For more information about webhook scopes, see the Field Guide.

Step 2 : Select an Event Type for Webhook Registration
The Webhooks service currently supports the events listed on the ACC Issue Events page.

You can specify multiple event types by including wildcards in the event type name using the asterisk (*) character, which matches zero or more characters in the name. For example:

issue.* matches all issue-related events
* matches all events in the system
For more information about event types and wildcards, see Supported Events.

Step 3 : Prepare to Manage Callbacks
A webhook requires a callback URL to which it will send the event data. To get started with setting up a local server, see Configuring Your Server.

Step 4 : Create a Webhook
Create a webhook by calling POST events/:event/hooks.

Hook Attribute
In some situations, specific data (such as the projectId) might not be included in the event notification. To include such custom information in the callback payload, you can configure the webhook accordingly.

Supply the hookAttribute property with a JSON object that you want to include in the callback, such as the projectId or any other details from your app.

For more information, see the Webhooks Field Guide.

Filter
You might want to filter the callbacks you receive based on the payload of the callback.

Provide the filter attribute in the endpoint request payload with a JSONPath expression that specifies the callback payload field values you want to filter on.

For more information, see Callback Filtering.

Example Input Values
The input values used in this example are as follows:

Request
curl -X 'POST'
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/autodesk.construction.issues/events/issue.created-1.0/hooks'
     -H 'Content-Type: application/json'
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'
     -d '{
           "callbackUrl": "http://bf067e05.ngrok.io/callback",
           "scope": {
             "project": "d6a37470-0539-40eb-89ff-9aeb8680066d"
           },
           "hookAttribute": {
             "projectId": "d6a37470-0539-40eb-89ff-9aeb8680066d"
           }
         }'
Show Less
Response
Upon completion, you should receive a 201 status response from the server. The response will also include a Location header, which you need to use if you plan to delete the webhook in the future.

To verify and view the properties of the newly-created webhook, navigate to the URL provided in the Location field.

HTTP/1.1 201
Date: Sun, 20 Apr 2025 16:45:05 GMT
Location: https://developer.api.autodesk.com/webhooks/v1/systems/autodesk.construction.issues/events/issue.created-1.0/hooks/0f60f6a0-996c-11e7-abf3-51d68cff984c
Content-Length: 0
Connection: keep-alive
Note that creating a webhook for ACC Issues requires Project Admin permissions for the target project.

Your configured callbackUrl should receive the notifications when a new issue is created in the project d6a37470-0539-40eb-89ff-9aeb8680066d.

Documentation /Webhooks API /How-to Guide
Creating a Webhook and Listening to ACC Reviews Events
This walkthrough demonstrates how to create a Webhook to register callbacks for specified types of Autodesk Construction Cloud (ACC) Reviews events. The steps include finding the scope ID for the events, choosing the event type for the webhook to listen for, preparing to handle callbacks, and creating the webhook.

For more details about the Reviews API, see the Reviews Field Guide.

Before You Begin
Make sure that you have registered an app and successfully acquired an OAuth token .
The Reviews Webhook supports only 3-legged OAuth tokens. See Get a 3-legged OAuth token to acquire a 3-legged OAuth token with scopes.
All requests to the Webhooks Service require the data:read scope.
You need the data:create scope to create a webhook.
Specify the region header to indicate the region in which the request is executed. The default value is US. You can also provide a specific region API value. For more details, see Region. The region parameter must remain consistent with the value used at creation time when listing, querying, or deleting webhooks.
Step 1: Find the Scope ID for Events
The Webhooks service uses the project ID as the scope for ACC Reviews events. To find the project ID, see the Retrieve Project ID tutorial.

For more information about webhook scopes, see the Field Guide.

Step 2: Select an Event Type for Webhook Registration
The Webhooks service currently supports the events listed on the Reviews Events page.

You can specify multiple event types by including wildcards in the event type name using the asterisk (*) character, which matches zero or more characters in the name. For example, specifying review.*-1.0 will match review.created-1.0 and review.closed-1.0.

For more information about event types and wildcards, see Supported Events.

Step 3: Prepare to Manage Callbacks
A webhook requires a callback URL to which the event data can be sent. See Configuring Your Server to get started with a local server setup.

Step 4: Create a Webhook
A webhook is created by making a POST request to webhooks/v1/systems/:system/events/:event/hooks. You can find additional details in the endpoint documentation.

Hook Attribute
In some scenarios, certain data (such as projectId) are not included in the event notification. You can define the webhook to include such custom information in the callback payload.

Provide the hookAttribute property with a JSON object that you want to include in the callback, such as the projectId or any other information from your app.

For more information, see the Webhooks Field Guide.

Filter
You might want to filter the callbacks you receive based on the payload of the callback.

Provide the filter attribute in the endpoint request payload with a JSONPath expression that specifies the callback payload field values to filter on.

For more information, see Callback Filtering.

Example Input Values
Values used in this example are:

system	
autodesk.construction.reviews
event	
review.created-1.0 (Wildcards can be used here, e.g. review.* or *)
callback URL	
http://bf067e05.ngrok.io/callback
scope key	
project (Scope name for Reviews events)
scope value	
d6a37470-0539-40eb-89ff-9aeb8680066d (The ID of the project, in UUID format)
hookAttribute	
{ "projectId": "d6a37470-0539-40eb-89ff-9aeb8680066d" } (The ID of the project, in UUID format)
Authorization token	
Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz
Request
curl -X 'POST'
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/autodesk.construction.reviews/events/review.created-1.0/hooks'
     -H 'Content-Type: application/json'
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'
     -H 'region: US'
     -d '{
           "callbackUrl": "http://bf067e05.ngrok.io/callback",
           "scope": {
             "project": "d6a37470-0539-40eb-89ff-9aeb8680066d"
           },
           "hookAttribute": {
             "projectId": "d6a37470-0539-40eb-89ff-9aeb8680066d"
           }
         }'
Show Less
Response
You should receive a successful response from the server with status of 201. Additionally, the response includes a Location header. The Location information is required to delete a webhook.

Navigate to the Location URL to validate and obtain the properties of the newly-created webhook.

HTTP/1.1 201
Date: Thu, 14 Sep 2017 16:45:05 GMT
Location: https://developer.api.autodesk.com/webhooks/v1/systems/autodesk.construction.reviews/events/review.created-1.0/hooks/0f60f6a0-996c-11e7-abf3-51d68cff984c
Content-Length: 0
Connection: keep-alive
Your configured callbackUrl should receive the notifications when a new review item is added to project d6a37470-0539-40eb-89ff-9aeb8680066d.

Receive the Callback Events
After a review is created, the callback event is sent to the callbackUrl with the following payload:

{
  "version": "1.0",
  "resourceUrn": "a4a3613c-c9dd-4e59-9d38-7b5a9857db9d",
  "hook": {
      "hookId": "9872fd3e-e2d0-44f0-845e-44b4ec9a16e8",
      "tenant": "d6a37470-0539-40eb-89ff-9aeb8680066d",
      "callbackUrl": "http://bf067e05.ngrok.io/callback",
      "createdBy": "GTMMJRRXST63",
      "event": "review.created-1.0",
      "createdDate": "2024-09-05T06:02:40.925+00:00",
      "lastUpdatedDate": "2024-09-05T06:02:40.921+00:00",
      "system": "autodesk.construction.reviews",
      "creatorType": "O2User",
      "status": "active",
      "scope": {
          "project": "d6a37470-0539-40eb-89ff-9aeb8680066d"
      },
      "hookAttribute": {
          "projectId": "d6a37470-0539-40eb-89ff-9aeb8680066d"
      },
      "autoReactivateHook": true,
      "urn": "urn:adsk.webhooks:events.hook:9872fd3e-e2d0-44f0-845e-44b4ec9a16e8",
      "callbackWithEventPayloadOnly": false,
      "__self__": "/systems/autodesk.construction.reviews/events/review.created-1.0/hooks/9872fd3e-e2d0-44f0-845e-44b4ec9a16e8"
  },
  "payload": {
    "roundNum": 1,
    "sequenceId": "16",
    "status": "OPEN"
  }
Show Less
}

Receive Events Restrictions
The user who creates a webhook can only receive notifications for Reviews that they have permission to view within the project.

If the user is a project admin, they will receive all Review creation and closure events.
If the user is a project member:
If the user is listed in the Reviewer or Approver candidates, they will receive creation and closure events for those Reviews.
If the user is only listed in the Initiator candidates, they will receive creation and closure events only for the Reviews they initiated.
As a project member, the user will not receive events for Reviews that are unrelated to them.

Retrieve your Webhooks
This walkthrough demonstrates how to retrieve your webhooks.

Before You Begin
Register an app
Successfully acquire an OAuth token with appropriate authentication scopes.
Retrieve your webhooks
List of webhooks can be retrieved by sending a GET request to webhooks/v1/systems/:system/events/:event/hooks

Note: There are multiple ways to retrieve list of webhooks.

Endpoint	Description
GET systems/:system/events/:event/hooks/:hook_id	Retrieves the details about a webhook for a specified event.
GET systems/:system/events/:event/hooks	Retrieves a paginated list of all the webhooks for a specified event in a system.
GET systems/:system/hooks	Retrieves a paginated list of all the webhooks of a specified system.
GET hooks	Retrieves a paginated list of all the webhooks.
You can find additional details in API Reference section.

Example
Request
curl -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.version.added/hooks?scopeName=folder&scopeValue=urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw&pageState=BNNBEACAtgALYWRzay53aXBkZXYNZnMuZmlsZS5hZGRlZAZmb2xkZXIydXJuOmFkc2sud2lwcWE6ZnMuZm9sZGVyOmNvLlRSM253QUtoVFNDQ0x0azY0VE52Q2cydXJuOmFkc2sud2lwcWE6ZnMuZm9sZGVyOmNvLlRSM253QUtoVFNDQ0x0azY0VE52Q2ctaHR0cDovL2FwaS53ZWJob29raW5ib3guY29tL2kvM0l6eGlLZndmL2luL3gy8H____3wf____Twpc5_2RqlBtCsLMPJlT9kABA=='\
     -H 'Authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'
Response
HTTP/1.1 200
Content-Type: application/json
Date: Fri, 14 Sep 2017 17:14:09 GMT
Content-Length: 662
Connection: keep-alive
{
  "links": {
    "next": "/systems/data/events/dm.version.added/hooks?pageState=AMMAEACAtgALYWRzay53aXBkZXYNZnMuZmlsZS5hZGRlZAZmb2xkZXIydXJuOmFkc2sud2lwcWE6ZnMuZm9sZGVyOmNvLlRSM253QUtoVFNDQ0x0azY0VE52Q2cydXJuOmFkc2sud2lwcWE6ZnMuZm9sZGVyOmNvLlRSM253QUtoVFNDQ0x0azY0VE52Q2ctaHR0cDovL2FwaS53ZWJob29raW5ib3guY29tL2kvM0l6eGlLZndmL2luL3gy8H____3wf____Twpc5_2RqlBtCsLMPJlT9kABA=="
  },
  "data": [{
    "hookId" : "0f60f6a0-996c-11e7-abf3-51d68cff984c",
    "tenant" : "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw",
    "callbackUrl" : "http://bf067e05.ngrok.io/callback",
    "createdBy" : "*********",
    "event" : "dm.version.added",
    "createdDate" : "2017-09-14T17:04:10.444+0000",
    "lastUpdatedDate" : "2020-09-14T17:04:10.444+0000",
    "system" : "data",
    "creatorType": "Application",
    "status" : "active",
    "autoReactivateHook": false,
    "scope" : {
      "folder" : "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw"
    },
    "urn" : "urn:adsk.webhooks:events.hook:0f60f6a0-996c-11e7-abf3-51d68cff984c",
    "__self__" : "/systems/data/events/dm.version.added/hooks/0f60f6a0-996c-11e7-abf3-51d68cff984c"
  }]
}

Documentation /Webhooks API /How-to Guide
Delete a Webhook
This walkthrough demonstrates how to delete a webhook.

Before You Begin
Register an app
Successfully acquire an OAuth token with appropriate authentication scopes.
Step 1 : Obtain the webhook ID
You must first obtain hookId or Location of the webhook that needs to be deleted. Note that Location URL contains webhook ID.

There are multiple ways to find hookId or Location URL of webhook:

When you create a webhook, you receive Location URL in Header of HTTP response.
List of your Webhooks returns Location in __self__ attribute of response-body. hookID attribute in response-body represents webhook ID.
Step 2 : Delete the webhook
You can delete your webhooks by sending a DELETE request to webhooks/v1/systems/:system/events/:event/hooks/:hook_id.

You can find additional details in the Reference Guide.

Example
Request
curl -X DELETE\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.version.added/hooks/0f60f6a0-996c-11e7-abf3-51d68cff984c'\
     -H 'Authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'
Response
HTTP/1.1 204
Date: Fri, 15 Sep 2017 16:26:40 GMT
Content-Length: 0
Connection: keep-alive
You should receive a delete successful response from the server with status of 204.


Configuring your Local Server
This walkthrough shows how to test your hooks against a localhost server.

Step 1 : Configuring ngrok
For Webhooks service to send notifications to your localhost server, you may like to use ngrok. You can find more information on ngrok at https://ngrok.com.

Download ngrok

After downloading ngrok, you can expose your localhost by running command:

./ngrok http 5678
You should see output like:

Session Status                online
Version                       2.2.8
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    http://bf067e05.ngrok.io -> localhost:5678
Forwarding                    https://bf067e05.ngrok.io -> localhost:5678
Take note of the *.ngrok.io URL. In this case, it is: http://bf067e05.ngrok.io

Step 2 : Running the localhost server
Assuming our callback URL for Webhooks is going to be http://bf067e05.ngrok.io/callback; we need to configure POST /callback endpoint of localhost:5678.

Which means, local server localhost should listen to POST request at /callback path.

Here is an example of localhost server in golang:

package main

import (
      "fmt"
      "io/ioutil"
      "log"
      "net/http"
)

const PORT = 5678

func callbackHandler(w http.ResponseWriter, req *http.Request) {
      body, _ := ioutil.ReadAll(req.Body)
      fmt.Printf("Payload \n %s", body)
}

func main() {
      http.HandleFunc("/callback", callbackHandler)
      log.Fatal(http.ListenAndServe(fmt.Sprintf(":%v", PORT), nil))
}
Show Less
Alternatively, you can learn more about Sinatra and find a Sinatra application here. Or, you can create localhost in any language or tool of your choice.

Then, run your localhost server.

At this stage, you should have http://localhost:5678/callback as callbackUrl. You can use http://bf067e05.ngrok.io/callback in Step 4 for creating a hook.

Documentation /Webhooks API /How-to Guide
How to verify payload signature
Webhooks Documentation
Check our documentation here to understand how to create hooks and set up your secure token to sign your callback payload. This page demonstrates how to verify payload signature using a simple Node JS server receiving callback from the Webhooks service.

Verify using Node.js
Prerequisites: * Install Node JS.

Create a new server with express-js
Open your favorite command line and run $ npm init to initialize a new node project. Create a file called app.js and add the following lines.

var express = require('express');

app.listen(3000, function () {
      console.log('Listening on port 3000!');
});
Now run you server by executing $ node app.js

$ node app.js
Listening on port 3000!
Add new endpoint for callback
Create a new endpoint where you will receive webhooks notifications.

app.post("/callback", function(req, res){
         res.send();
});
Create webhook for your server
Now you have your server running you must configure the Webhooks service to send notification to your server.

Check here to see how to create new hooks in our Step-by-Step guide.

{
  "callbackUrl":"http://localhost:3000/callback",
  "scope":{
    "folder":"urn:adsk.wipprod:fs.folder:co.q2d7wQwVTJSICAdBl-REQw"
  }
}
Note: the above hook is using localhost as callback url and it will not be reachable from the Webhooks service. Check how to use ngrok to open a secure tunnel to localhost here.

Configure server to verify signature
This example uses the Crypto library bundled with Node to calculate HMAC-SHA1 signature.

var bodyParser = require('body-parser');
var app = express();
var WEBHOOKS_SECRET = "<YOUR_TOKEN_HERE>";

function verifySignature(req, res, buf, encoding) {
      const signature = req.header('x-adsk-signature');
  if(!signature) { return; }

  // use utf-8 encoding by default
  const body    = buf.toString(encoding);
  const hmac    = crypto.createHmac('sha1', WEBHOOKS_SECRET);
  const calcSignature = 'sha1hash=' + hmac.update(body).digest('hex');
  req.signature_match = (calcSignature === signature);
}

app.use(bodyParser.json({
  inflate: true,
  limit: '1024kb',
  type: 'application/json',
  verify: verifySignature
}));

app.post("/callback", function(req, res){
      if(!req.signature_match) {
          return res.status(403).send('not called from webhooks service');
      }

      res.status(204).send();
});
Show Less
Download full example
var express = require('express');
var bodyParser = require('body-parser');
var crypto = require('crypto');
var app = express();
var WEBHOOKS_SECRET = "<YOUR_TOKEN_HERE>";

function verifySignature(req, res, buf, encoding) {
  const signature = req.header('x-adsk-signature');
  if(!signature) { return; }

  // use utf-8 encoding by default
  const body    = buf.toString(encoding);
  const hmac    = crypto.createHmac('sha1', WEBHOOKS_SECRET);
  const calcSignature = 'sha1hash=' + hmac.update(body).digest('hex');
  req.signature_match = (calcSignature === signature);
}

app.use(bodyParser.json({
  inflate: true,
  limit: '1024kb',
  type: 'application/json',
  verify: verifySignature
}));

app.post("/callback", function(req, res){
  if(!req.signature_match) {
    return res.status(403).send('not called from webhooks service');
  }

  res.status(204).send();

  // do whatever work needs to be done with the webhooks payload
  const body = req.body;
  console.log(body);
});

app.listen(3000, function () {
  console.log('Listening on port 3000!');
});
