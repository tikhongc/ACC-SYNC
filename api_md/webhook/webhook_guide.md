Webhooks API
The Webhooks API enables applications to listen to APS events and receive notifications when they occur. When an event is triggered, the Webhooks service sends a notification to a callback URL you have defined.

You can customize the types of events and resources for which you receive notifications. For example, you can set up a webhook to send notifications when files are modified or deleted in a specified hub or project.

Below is quick summary of this workflow:

Identify the data for which you want to receive notifications.
Use the Webhooks API to create one or more hooks.
The Webhooks service will notify the webhook when there is a change in the data.

API Basics
Webhooks APIs allow applications to subscribe to APS events, and receive notifications when they occur. When an event is triggered, the Webhooks API sends a notification to a callback URL. Callback URL is set when a webhook is created.

There are four key elements to a webhook:

The target service of interest.
The events from the target service to subscribe. Please check Supported Events section for additional information.
The callback URL i.e. URL where the Webhooks service will notify when the events occur.
The Scope i.e. the domain of the data for which this webhook was created.
Webhook
A webhook can be created by simply making a POST request to webhooks/v1/systems/:system/events/:event/hooks. You can find additional details in the Reference Guide.

curl -X 'POST'
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.version.added/hooks'
     -H 'Content-Type: application/json'
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "scope": {
                 "folder": "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw"
            }
      }'
Show Less
Callback
When the event occurs, the webhooks service sends a payload to the callback URL as an HTTP POST request. The webhook service expects a 2xx response to the HTTP POST request. The response must be received within 6 seconds. A non-2xx response or no response within 6 seconds is considered an error.

When there is no error from the registered callback URL, the Webhooks service guarantees at least once delivery. In the event of an error, the call will be retried four times, with the final attempt being at least 48 hours after the initial attempt. If last retry attempt fails, the webhook will be disabled and it will need to be re-enabled using PATCH systems/:system/events/:event/hooks/:hook_id.

Secret Token
Webhooks API also supports setting a secret token to prevent callback spoofing. When your secret token is set, Webhooks Service uses it to create a hash signature for each payload. This hash signature is passed along with each request, as the header x-adsk-signature. In order to validate that the request came from Autodesk Webhooks service, subscribers should compute a hash using their token, and ensure that the hash from Webhooks Service matches. Webhooks uses an HMAC hexdigest to compute the hash. Note: Tokens can be set on a per user (user context) or per application basis.

Getting Started
Take a look at our How-to Guide to see how to add your first webhook in Webhooks API.
Field Guide
This section outlines the attributes for each of the objects exposed by the Webhooks API.

Understanding Scope for a Webhook
Webhooks are targeted to provide updates on specific range of data within a Hub. For example you could subscribe to file added event for a Project within a Hub or a sub folder within a Project. In Webhooks terminology, it is referred as scope of the Webhook. Scopes are recursive in nature i.e. if you choose your scope to be a Project, then you will get notification for all folders and sub-folders within the Project. Please note that, webhook only supports folder scope. A webhook can be registered on a Project with Root Folder scope and hence can receive callbacks for all events within that Project and its children.

Webhook
A webhook represents a registered callback URL in a system for a specific event. This callback URL will be called by the system when the event is triggered. Each webhook is defined within a scope where the event can be trigger.

Schema
Attribute	Description
hookId	Unique identifier of the webhook.
event	Type of event that webhook was created for.
system	Type of system where webhook was created.
callbackUrl	URL called when the event type for this system happens.
createdBy	Identifier of the creator. Service or user id.
creatorType	Type of the creator of the webhook. It can be Application for 2-Legged Token and O2User for 3-Legged Token.
scope	Extent to where the event will be triggered. Please refer to the individual event specification pages for valid scopes. For example, Data Management events.
hookAttribute	JSON object that can be used by you to store/set some custom information. Maximum size of JSON object (content) should be less than 1KB. Object will be send back to you on callback payload. Check version added sample
filter	JsonPath expression that can be used by you to filter the callbacks you receive based on the payload of the callback. Check version added sample
urn	Unique identifier of the webhook in URN format.
status	Status of the webhook. Possible values are: active, inactive and reactivated.
hubId	Optional. Should be provided if the user may be a member of a large number of projects. This hub ID corresponds to an account ID in the BIM 360 API, prefixed by “b.”
projectId	Optional. Should be provided if the user may be a member of a large number of projects. This project ID corresponds to the project ID in the BIM 360 API, prefixed by “b.”
autoReactivateHook	Optional. Flag to enable the hook for the automatic reactivation flow. Default: false. Please see Event Delivery Guarantees for more details.
hookExpiry	Optional. ISO8601 formatted date and time when the hook should expire and automatically be deleted. Default: null (never expires).
__self__	Reference to itself.
Example Object
{
    "hookId": "2a96cc80-97da-11e7-a2e5-6fa1bae9fd46",
    "tenant": "228780",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "*********",
    "event": "dm.version.added",
    "createdDate": "2017-09-12T16:48:13.128+0000",
    "system": "data",
    "creatorType": "O2User",
    "scope": {
        "folder": "urn:adsk.wipprod:fs.folder:co.WGiFD3Y-T4GdynbaM5ojeQ"
    },
    "urn": "urn:adsk.webhooks:events.hook:2a96cc80-97da-11e7-a2e5-6fa1bae9fd46",
    "status": "active",
    "autoReactivateHook": false,
    "hookExpiry": "2017-09-21T17:04:10.444Z",
    "__self__": "/systems/data/events/dm.version.added/hooks/2a96cc80-97da-11e7-a2e5-6fa1bae9fd46"
}
Show Less
Secret Token
As you expose your application endpoint to receive calls from the Webhooks service, you probably want that endpoint to only receive data from your configured webhooks. Your secret token enables you to validate that the call comes from the Webhooks service.

Tokens are used to sign the callback payload for webhooks when an event occurs. Each application or user can register a secure token using its own client id or user id that will be later used to sign the payload.

Schema
Attribute	Description
token	Alphanumeric token used to sign event callback’s payload.
Example Object
{
    "token":"eyJhbGciOiJIUzI1NiIsImtpZCI6Imp3dF9zeW1tZXRyaWNfa2V5In0"
}
Documentation /Webhooks API /Developer's Guide
Callback Filtering
What is Callback Filtering
When a hook with filter attribute is created, you can filter out a callback if its event payload does not match the filter attribute. You can find a property to filter from the payload section for any Supported Events. For example, filter attribute $[?(@.ext==’txt’)] can be used to filter dm.version.added callbacks based on the extension of a file.

Hook filter attribute is defined in JsonPath format, check it out for for more details about the syntax of JsonPath expression. http://jsonpath.herokuapp.com/ can be used to test the JsonPath expressions.

Filter Formats
With the Single Filter format, you specify a single JsonPath expression in the filter field. For example: $[?(@.ext==’txt’)]

With the Multiple Filter format, you can specify a list of JsonPath expressions, all of which must be match for the hook to be triggered. For example: [“$[?(@.sizeInBytes>=1048576)]”,”$[?(@.ext==’f3d’)]”]

See example 3 for an example of using the OR operator along with the AND operator. An OR operator can also be used by itself in the same expression without the AND operator as needed.

Example 1
Create an dm.version.added event hook with file extension filtering:

Create a Webhook
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.version.added/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "scope": {
                 "folder": "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw"
            },
            "hookAttribute": {
                 /* Custom metadata */
                 "myfoo": 33,
                 "projectId": "someURN",
                 "myobject": {
                      "nested": true
                 }
            },
            "filter": "$[?(@.ext=='txt')]"
      }'
Show Less
Callback Payload
{
  "version": "1.0",
  "resourceUrn": "urn:adsk.wipprod:fs.file:vf.0zvdp3CoTzWDcZC_wL0kJA?version=1",
  "hook": {
    "system": "data",
    "event": "dm.version.added",
    "hookId": "1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "tenant": "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "*************",
    "createdDate": "2017-09-22T02:38:32.341+0000",
    "creatorType": "Application",
    "filter": "$[?(@.ext=='txt')]",
    "hookAttribute": {
      "myfoo": 34,
      "projectId": "someURN",
      "myobject": {
        "nested": true
      }
    },
    "scope": {
      "folder": "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw"
    },
    "urn": "urn:adsk.webhooks:events.hook:1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "status": "active",
    "__self__": "/systems/data/events/dm.version.added/hooks/1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce"
  },
  "payload": {
    "ext": "txt",
    "modifiedTime": "2017-09-25T03:08:53+0000",
    "creator": "*************",
    "lineageUrn": "urn:adsk.wipprod:dm.lineage:0zvdp3CoTzWDcZC_wL0kJA",
    "sizeInBytes": 36,
    "hidden": false,
    "indexable": true,
    "project": "4f8b8b74-3853-473d-85c4-4e8a8bff885b",
    "source": "urn:adsk.wipprod:fs.file:vf.0zvdp3CoTzWDcZC_wL0kJA?version=1",
    "version": "1",
    "user_info": {
      "id": "*************"
    },
    "name": "dc829fc5-bd21-4444-8d8f-735ae4fe736f.txt",
    "createdTime": "2017-09-06T03:08:53+0000",
    "modifiedBy": "*************",
    "state": "CONTENT_AVAILABLE",
    "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw",
    "ancestors": [
      {
        "urn": "urn:adsk.wipprod:fs.folder:co.woxoClweRCeMWn-HFbXGdQ",
        "name": "b662c88c-85e3-45c7-a9cc-6c77a31462a4"
      },
      {
        "urn": "urn:adsk.wipprod:fs.folder:co.XFrPsQGxRomOJzyL1-z7Tg",
        "name": "292139e5-5f7f-402c-90f0-e61b53f38aad-account-root-folder"
      },
      {
        "urn": "urn:adsk.wipprod:fs.folder:co.6a5Ylw9mRDus2bhttmH7dw",
        "name": "4f8b8b74-3853-473d-85c4-4e8a8bff885b-root-folder"
      },
      {
        "urn": "urn:adsk.wipprod:fs.folder:co.bXJiDx2ySve30xhul5Ihuw",
        "name": "Project Files"
      },
      {
        "urn": "urn:adsk.wipprod:fs.folder:co.chOa5mlkR6mjN-PEx8-r8Q",
        "name": "SomeTest"
      }
    ],
    "tenant": "292139e5-5f7f-402c-90f0-e61b53f38aad"
  }
}
Show Less
Example 2
Create an extraction.finished event hook with status filtering:

Create a Webhook
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/derivative/events/extraction.finished/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "scope": {
                 "workflow": "my-workflow-id"
            },
            "filter": "$[?(@.Payload.status in ['failed','timeout'])]"
      }'
Show Less
Callback Payload
{
  "version": "1.0",
  "resourceUrn": "dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2htZHRlc3RzdGcvQ2FzZUlubmVyLmlwdA",
  "hook": {
    "hookId": "a228fb60-106b-11e8-9774-490cff0c6aae",
    "tenant": "my-workflow-id",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "*************",
    "event": "extraction.finished",
    "createdDate": "2018-02-13T03:11:50.294+0000",
    "system": "derivative",
    "creatorType": "Application",
    "status": "active",
    "scope": {
      "workflow": "my-workflow-id"
    },
    "urn": "urn:adsk.webhooks:events.hook:a228fb60-106b-11e8-9774-490cff0c6aae",
    "__self__": "/systems/derivative/events/extraction.finished/hooks/a228fb60-106b-11e8-9774-490cff0c6aae"
  },
  "payload": {
    "TimeStamp": 1513134729128,
    "URN": "dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2htZHRlc3RzdGcvQ2FzZUlubmVyLmlwdA",
    "EventType": "EXTRACTION_FINISHED",
    "Payload": {
      "status": "failed",
      "scope": "7dca556c-e041-444a-91cf-cdea18a7699e",
      "registerKey": []
    }
  }
}
Show Less
Example 3
Create an extraction.finished event hook with status filtering matching multiple values with an AND (&&) operator along with the OR (||) operator:

Create a Webhook
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/derivative/events/extraction.finished/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "scope": {
                 "workflow": "my-workflow-id"
            },
            "filter": "$[?((@.EventType == 'EXTRACTION_FINISHED' && @.Payload.status == 'failed') || 'test123' in @.Payload.registerKey[*].name)]"
      }'
Show Less
Callback Payload
{
  "version": "1.0",
  "resourceUrn": "dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2htZHRlc3RzdGcvQ2FzZUlubmVyLmlwdA",
  "hook": {
    "hookId": "a228fb60-106b-11e8-9774-490cff0c6aae",
    "tenant": "my-workflow-id",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "*************",
    "event": "extraction.finished",
    "createdDate": "2018-02-13T03:11:50.294+0000",
    "system": "derivative",
    "creatorType": "Application",
    "status": "active",
    "scope": {
      "workflow": "my-workflow-id"
    },
    "urn": "urn:adsk.webhooks:events.hook:a228fb60-106b-11e8-9774-490cff0c6aae",
    "__self__": "/systems/derivative/events/extraction.finished/hooks/a228fb60-106b-11e8-9774-490cff0c6aae"
  },
  "payload": {
    "TimeStamp": 1513134729128,
    "URN": "dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6d2htZHRlc3RzdGcvQ2FzZUlubmVyLmlwdA",
    "EventType": "EXTRACTION_FINISHED",
    "Payload": {
        "status": "failed",
        "scope": "7dca556c-e041-444a-91cf-cdea18a7699e",
        "registerKey": [{
          "name": "test123"
        }]
    }
  }
}
Event Delivery Guarantees
The Webhooks service retries a number of times to deliver the event to the client in the event of failure on the first attempt.

Retry Attempts
By default, all events that fail to deliver on the first attempt are subjected to retry for 8 times over the span of the next 48 hours in an exponential delayed fashion.
If the event fails to deliver after all the retry attempts, the backend system records the failure by maintaining a counter against the hook.
The Webhooks service applies the retry logic to 5 events that arrive for the hook.
If all 5 events fail to deliver, the hook is inactivated by updating the hook status to inactive.
Enhanced Retry With Automatic Hook Reactivation
The Webhooks service has the capability to automatically reactivate the hook after it becomes inactive. This is controlled by the flag autoReactivateHook that can be set on the hook. The hook with autoReactivateHook flag set is subjected to an automatic hook reactivation lifecycle.

Automatic Hook Reactivation Flag
The hook with autoReactivateHook flag set to true becomes a candidate for automatic hook reactivation lifecycle. By default, the flag is set to false.
The flag can be set when the hook is created using POST API call or updated later using the PATCH API call.
Automatic Hook Reactivation Lifecycle
If the hook has the autoReactivateHook flag set, then it becomes the candidate for the automatic hook reactivation lifecycle.

After the hook becomes inactive after the normal retry attempts, the Webhooks service runs a background process to pick all the hooks that became inactivate before 7 days from the current date and updates the hook to reactivated status.
The Webhooks service will accept an event for the hook for a one-time delivery attempt.
If the event delivery is successful, the hook status is updated to active.
If the event delivery fails, the hook status is updated to inactive. The backend system records the failure by maintaining a counter against the hook.
The Webhooks service applies the automatic hook reactivation lifecycle logic 5 times before the hook is made permanently inactive. This also makes the autoReactivateHook flag to false on the hook.
APS Rate Limits and Quotas
The Autodesk Platform Service (APS) provides a set of cloud resources that are shared among many applications and services. Autodesk strives to ensure that there are plenty of cloud resources to serve all platform users. However, runaway applications and malicious attacks can quickly consume resources and diminish service. To avoid overconsumption and service degradation, APS sets rate limits and quotas for users of each of its services. This page describes how those rate limits and quotas work.

Rate Limits
Rate limits are simple: a rate limit sets the maximum number of API calls an application can make per minute. Rate limits help keep the number of API calls within the capacity of the service, and guard against instability and attacks such as denial-of-service attacks. This ensures availability and consistent quality of service for all users.

The rate limits may vary by each service or by endpoints within a service. Rate limits are currently placed at a generous level that shouldn’t cause problems with applications running under normal circumstances. They may come into play and limit an application if the application generates an unusually high volume of API calls.

Rate limits are not guaranteed service levels. If a service is overloaded for any reason, request rate limits may effectively drop until the overload condition ends.

Notification
When an application exceeds the published rate limit for a given endpoint, the API returns an HTTP 429 "Too many requests" response code. The response header has a parameter named Retry-After that specifies how many seconds to wait before making a new request. We strongly recommend that you retry a request only after the waiting period has elapsed.

The following example shows a typical 429 response.

Response Header (429)
HTTP/1.1 429 Too Many Requests
Content-Type: application/json
Retry-After: 25
Server: Apigee Router
Content-Length: 44
Response Body (429)
{"developerMessage":"Quota limit exceeded."}
Quotas
Quotas come into play after a service request is accepted. A quota limits an application’s use of resources as the application carries out activities within an APS service. Quotas may limit, for example, file sizes uploaded, downloaded, and processed; the amount of processing time allowed per job; an application’s monthly service consumption; and so on. Each APS service may have a set of built-in quotas. They may also offer custom quotas that a user or application can set to lower resource consumption below the built-in limits if desired to further restrict resource use.

Note again that quotas are not guaranteed service levels. Quota limits may drop temporarily if a service is overloaded.

Notification
Exceeding a quota typically occurs when an API request specifies excessive resource use. The service receiving the request replies with an error response that specifies the quota violation. Sometimes, where resource use doesn’t occur until after a request is received (the request places a job on a queue, for example), the quota violation occurs during later execution and throws an error there. In that case the requester may set up a callback to provide error notification. If a callback isn’t possible, the requester can poll regularly (but not too frequently) to make sure that execution is carried out correctly.

Scope
The scope of APS rate limits and quotas (how widely or narrowly they apply) varies across APIs and resource types. Scope is defined by how request rate or resource use is tallied: on the client side whether it’s tallied per user ID or application, for example, and on the service side whether it’s applied across an entire API, for example, or to individual endpoints or resources within an API.

Rate Limit Scope
Rate limits on the client side may apply per user ID or per application. On the service side, a rate limit may apply across an entire API or to individual endpoints within an API, changing from one endpoint to another.

Quota Scope
Quotas on the client side may apply per user ID or per application. On the service side, they may apply to a particular resource type, to the underlying engine servicing a request, to an endpoint, or other qualifying attributes. Because quotas are typically resource-specific, their scope is often narrowly defined.

API specific rate limit and quota pages spell out the scope for each API’s rate limit and quota.

Requesting Rate Limit and Quota Changes
If a rate limit or quota causes problems for an application with reasonable resource use, you can request a limit or quota change by contacting support via https://aps.autodesk.com/get-help.
Webhooks Rate Limits and Quotas
The Webhooks service observes a set of rate limits to ensure that all clients get sufficient service and that runaway applications don’t consume excessive resources. APS Rate Limits and Quotas describes rate limits in general.

Rate Limits
These rate limits apply to each of the Webhook’s API’s endpoints. Note that these rates are not service guarantees. In the uncommon case where total service use is too high across all clients, accepted request rates may drop until traffic subsides.

Scope
The Webhooks service sets a separate rate limit for each application (specified by client ID) per API endpoint. For example, an application can’t exceed the specified limit of 300 requests per minute when calling the API endpoint GET systems/:system/events/:event/hooks/:hook_id.

The application can, however, exceed 300 combined requests per minute if those requests go to separate endpoints and requests to each endpoint don’t violate each endpoint’s specified rate limit. For example, an application could make 320 requests per minute if 290 requests go to GET systems/:system/events/:event/hooks/:hook_id (limit 300) and 30 go to POST systems/:system/events/:event/hooks (limit 50).

Violation Notification
If an application exceeds an endpoint’s rate limit, the Webhooks service returns an HTTP 429 error (described in detail in APS Rate Limits and Quotas).

Webhooks Endpoint Rate Limits
These rate limits apply to webhooks endpoints within the Webhooks API.

Method	Endpoint	Limit (requests/minute)
GET	systems/:system/events/:event/hooks/:hook_id	300
GET	systems/:system/events/:event/hooks	300
GET	systems/:system/hooks	300
GET	hooks	300
POST	systems/:system/events/:event/hooks	50
POST	systems/:system/hooks	50
PATCH	systems/:system/events/:event/hooks/:hook_id	300
DELETE	systems/:system/events/:event/hooks/:hook_id	300
Tokens Endpoint Rate Limits
These rate limits apply to tokens endpoints within the Webhooks API.

Method	Endpoint	Limit (requests/minute)
POST	tokens	50
PUT	tokens/@me	50
DELETE	tokens/@me	50
Quotas
Webhooks quotas limit an app’s resource consumption when using the Webhooks service.

Scope
Quotas are enforced for each event type for a given scope.

Event Type Quotas
The Webhooks service has a Event Type Quota of 1000 hooks per event type for a given scope. Note that you are not allowed to register the same callback URL more than once for the same scope and event type.

Quota Violation Notification
The Webhooks service returns an HTTP 400 error, with the message “Failed to create more than 1000 hooks for same scope” if an application attempts to go past the quota.

Changing Limits
APS Rate Limits and Quotas describes how to request rate limit changes for APS APIs.



GDPR Compliance
The General Data Protection Regulation (GDPR) is a set of rules that protect the digital privacy of the citizens of the European Union (EU). Businesses and organizations serving users in Europe are legally required to comply with GDPR. Accordingly, Autodesk serves users in the Europe, Middle East, and Africa (EMEA) region from a dedicated data center that is physically separated from the US data center.

If you are a user in the EMEA region, the physical storage of your data is bound by GDPR regulations. You must always save the webhooks related data you generate in a data center that exclusively serves the EMEA region.

Generating/Accessing EMEA specific data
There are generally several ways to generate and access EMEA based webhooks related data and this varies between each of the Webhooks API endpoints. Each of the API endpoints defines what options are supported and some of those options may include any of the following:

Through the region query param, the EMEA value can be passed in to designate the specific data center.
Through the x-ads-region header value, the EMEA value can be passed in to designate the specific data center.
Note: For any of the options noted above, by default if no value is provided, then US will be used by default. Other region values are also supported depending on the individual API endpoints.

Potential problems with regions
If you generate webhooks data in one region, but access the same data with different values for the region header or query param, the system may not be able to access those resources.

You may receive a 404 error when accessing the webhooks data as a result. At that point if the information is correct, then verifying that the correct region values are used would be the next step to troubleshoot the issue.