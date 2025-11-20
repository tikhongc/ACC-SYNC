

Documentation /Webhooks API /Reference Guide
GET	systems/:system/events/:event/hooks/:hook_id
Get details of a webhook based on its webhook ID

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/webhooks/v1/systems/:system/events/:event/hooks/:hook_id
Authentication Context	
app only/ user context required
Required OAuth Scopes	
data:read
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via OAuth
Content-Type*
string
application/json
x-ads-region
string
Specifies the geographical location (region) of the server that the request is executed on. Supported values are the following, but the default value is US:
US : (Default) Retrieves information regarding the specified webhook that was previously registered in a data center dedicated to serve the United States.
EMEA : Retrieves information regarding the specified webhook that was previously registered in a data center dedicated to serve the European Union, Middle East, and Africa.
AUS : (Beta) Retrieves information regarding the specified webhook that was previously registered in a data center dedicated to serve Australia.
GBR : Retrieves information regarding the specified webhook that was previously registered in a data center dedicated to serve United Kingdom.
JPN : Retrieves information regarding the specified webhook that was previously registered in a data center dedicated to serve Japan.
DEU : Retrieves information regarding the specified webhook that was previously registered in a data center dedicated to serve Germany.
CAN : Retrieves information regarding the specified webhook that was previously registered in a data center dedicated to serve Canada.
IND : Retrieves information regarding the specified webhook that was previously registered in a data center dedicated to serve India.
* Required
Request
URI Parameters
system
string
A system for example: data
for Data Management
event
string
Type of event. See Supported Events
hook_id
string
Id of the webhook to retrieve
Request
Query String Parameters
region
string
Specifies the geographical location (region) of the server that the request is executed on. Supported values are the following, but the default value is US:
US : (Default) Processes request in a data center dedicated to serve the United States.
EMEA : Processes request in a data center dedicated to serve the European Union, Middle East, and Africa.
AUS : (Beta) Processes request in a data center dedicated to serve Australia.
The x-ads-region header also specifies the region. If you specify both, x-ads-region has precedence.

Response
HTTP Status Code Summary
200
OK
Successful.
400
BAD REQUEST
The request is invalid.
401
UNAUTHORIZED
Invalid authorization header.
403
FORBIDDEN
Access denied regardless of authorization status.
404
NOT FOUND
The specified resource was not found.
500
INTERNAL SERVICE ERROR
Unexpected service interruption
Response
Body Structure (200)
 Expand all
hookID
string
Webhook ID
callbackUrl
string
Callback URL registered for the webhook
createdBy
string
Client ID or User ID
createdDate
date
Date and time when webhook was created
event
string
Type of event
hookAttribute
object
Custom metadata which will be less than 1KB in size.
scope
object
An object that represents the extent to where the event is monitored. For example, if the scope is folder, the webhooks service generates a notification for the specified event occurring in any sub folder or item within that folder
status
string
active if webhook is active; otherwise inactive
hubId
string
Optional: account ID in the BIM 360 API (if supplied upon hook creation)
projectId
string
Optional: project ID in the BIM 360 API (if supplied upon hook creation)
hookExpiry
string
Optional: ISO8601 formatted date and time when the hook should expire and automatically be deleted. null or not present means the hook never expires.
urn
string
URN of the webhook
__self__
string
Location of this webhook relative to /webhooks/v1/
Example
Successful Retrieval of a webhook (200):

Request
curl -X 'GET'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.version.added/hooks/05f10350-991a-11e7-8cd7-91969336b9c2'\
     -H 'Authorization: Bearer 0X6mpTyg5IbH6YI8Okz2XJGpEDeK'
Response
HTTP/1.1 200
Date: Thu, 14 Sep 2017 06:57:51 GMT
Location: https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.version.added/hooks/0f60f6a0-996c-11e7-abf3-51d68cff984c
Content-Length: 665
Connection: keep-alive
{
  "hookId": "05f10350-991a-11e7-8cd7-91969336b9c2",
  "tenant": "urn:adsk.wipprod:fs.folder:co.VsFvE6y5SNKnhSnogSeqcg",
  "callbackUrl": "http://cf069e23.ngrok.io/callback_test",
  "createdBy": "********",
  "event": "dm.version.added",
  "createdDate": "2017-09-14T06:57:50.597+0000",
  "lastUpdatedDate" : "2020-09-14T17:04:10.444+0000",
  "system": "data",
  "creatorType": "Application",
  "status" : "active",
  "autoReactivateHook": false,
  "hookExpiry": "2017-09-21T17:04:10.444Z",
  "scope": {
      "folder": "urn:adsk.wipprod:fs.folder:co.VsFvE6y5SNKnhSnogSeqcg"
  },
  "urn": "urn:adsk.webhooks:events.hook:05f10350-991a-11e7-8cd7-91969336b9c2",
  "__self__": "/systems/data/events/dm.version.added/hooks/05f10350-991a-11e7-8cd7-91969336b9c2"
}

Documentation /Webhooks API /Reference Guide
GET	systems/:system/events/:event/hooks
Retrieves a paginated list of all the webhooks for a specified event. If the pageState query string is not specified, the first page is returned.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/webhooks/v1/systems/:system/events/:event/hooks
Authentication Context	
app only/ user context required
Required OAuth Scopes	
data:read
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via OAuth
x-ads-region
string
Specifies the geographical location (region) of the server that the request is executed on. Supported values are the following, but the default value is US:
US : (Default) Retrieves the webhooks that were registered in a data center dedicated to serve the United States.
EMEA : Retrieves the webhooks that were registered in a data center dedicated to serve the European Union, Middle East, and Africa.
AUS : (Beta) Retrieves the webhooks that were registered in a data center dedicated to serve Australia.
GBR : Retrieves the webhooks that were registered in a data center dedicated to serve United Kingdom.
JPN : Retrieves the webhooks that were registered in a data center dedicated to serve Japan.
DEU : Retrieves the webhooks that were registered in a data center dedicated to serve Germany.
CAN : Retrieves the webhooks that were registered in a data center dedicated to serve Canada.
IND : Retrieves the webhooks that were registered in a data center dedicated to serve India.
* Required
Request
URI Parameters
system
string
System for example: data
event
string
Type of event. See Supported Events
Request
Query String Parameters
region
string
Specifies the geographical location (region) of the server that the request is executed on. Supported values are the following, but the default value is US:
US : (Default) Processes request in a data center dedicated to serve the United States.
EMEA : Processes request in a data center dedicated to serve the European Union, Middle East, and Africa.
AUS : (Beta) Processes request in a data center dedicated to serve Australia.
The x-ads-region header also specifies the region. If you specify both, x-ads-region has precedence.

Request
Query String Parameters
scopeName
String
Scope name used to create hook. For example : folder
scopeValue
String
Scope value used to create hook. If scopeValue is present then scopeName must be present, otherwise scopeValue would be ignored.
pageState
String
Base64 encoded string used to return the next page of the list of webhooks. This can be obtained from the next field of the previous page. PagingState instances are not portable and implementation is subject to change across versions. Default page size is 200.
status
String
Status of the hooks. Options: ‘active’, ‘inactive’
region
string
Specifies the geographical location (region) of the server that the request is executed on. Supported values are the following, but the default value is US:
US : (Default) Retrieves the webhooks that were registered in a data center dedicated to serve the United States.
EMEA : Retrieves the webhooks that were registered in a data center dedicated to serve the European Union, Middle East, and Africa.
AUS : (Beta) Retrieves the webhooks that were registered in a data center dedicated to serve Australia.
GBR : Retrieves the webhooks that were registered in a data center dedicated to serve United Kingdom.
JPN : Retrieves the webhooks that were registered in a data center dedicated to serve Japan.
DEU : Retrieves the webhooks that were registered in a data center dedicated to serve Germany.
CAN : Retrieves the webhooks that were registered in a data center dedicated to serve Canada.
IND : Retrieves the webhooks that were registered in a data center dedicated to serve India.
The x-ads-region header also specifies the region. If you specify both, x-ads-region has precedence.

Response
HTTP Status Code Summary
200
OK
Success.
204
EMPTY
No webhooks exist.
400
BAD REQUEST
The request is invalid.
401
UNAUTHORIZED
Invalid authorization header.
403
FORBIDDEN
Access denied regardless of authorization status.
404
NOT FOUND
The specified resource was not found.
500
INTERNAL SERVICE ERROR
Unexpected service interruption
Response
Body Structure (200)
 Expand all
links
object
An object containing links to other pages of the paginated list of webhooks
data
array: object
An array of webhook objects
Example
Successful Retrieval of webhooks (200):

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

GET	systems/:system/hooks
Retrieves a paginated list of all the webhooks for a specified system. If the pageState query string is not specified, the first page is returned.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/webhooks/v1/systems/:system/hooks
Authentication Context	
app only/ user context required
Required OAuth Scopes	
data:read
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via OAuth
x-ads-region
string
Specifies the geographical location (region) of the server that the request is executed on. Supported values are the following, but the default value is US:
US : (Default) Retrieves the webhooks that were registered in a data center dedicated to serve the United States.
EMEA : Retrieves the webhooks that were registered in a data center dedicated to serve the European Union, Middle East, and Africa.
AUS : (Beta) Retrieves the webhooks that were registered in a data center dedicated to serve Australia.
GBR : Retrieves the webhooks that were registered in a data center dedicated to serve United Kingdom.
JPN : Retrieves the webhooks that were registered in a data center dedicated to serve Japan.
DEU : Retrieves the webhooks that were registered in a data center dedicated to serve Germany.
CAN : Retrieves the webhooks that were registered in a data center dedicated to serve Canada.
IND : Retrieves the webhooks that were registered in a data center dedicated to serve India.
* Required
Request
URI Parameters
system
string
System for example: data
Request
Query String Parameters
status
string
Status of the hooks. Options: ‘active’, ‘inactive’
pageState
string
Base64 encoded string used to return the next page of the list of webhooks. This can be obtained from the next field of the previous page. PagingState instances are not portable and implementation is subject to change across versions. Default page size is 200.
region
string
Optional parameter to specify the region the request will be run in. Supported values are the following, but the default value is US:
US : (Default) Retrieves the webhooks that were registered in a data center dedicated to serve the United States.
EMEA : Retrieves the webhooks that were registered in a data center dedicated to serve the European Union, Middle East, and Africa.
AUS : (Beta) Retrieves the webhooks that were registered in a data center dedicated to serve Australia.
GBR : Retrieves the webhooks that were registered in a data center dedicated to serve United Kingdom.
JPN : Retrieves the webhooks that were registered in a data center dedicated to serve Japan.
DEU : Retrieves the webhooks that were registered in a data center dedicated to serve Germany.
CAN : Retrieves the webhooks that were registered in a data center dedicated to serve Canada.
IND : Retrieves the webhooks that were registered in a data center dedicated to serve India.
The x-ads-region header also specifies the region. If you specify both, x-ads-region has precedence.

Response
HTTP Status Code Summary
200
OK
Success.
204
EMPTY
No webhooks exist.
400
BAD REQUEST
The request is invalid.
401
UNAUTHORIZED
Invalid authorization header.
403
FORBIDDEN
Access denied regardless of authorization status.
404
NOT FOUND
The specified resource was not found.
500
INTERNAL SERVICE ERROR
Unexpected service interruption
Response
Body Structure (200)
 Expand all
links
object
An object containing links to other pages of the paginated list of webhooks
data
array: object
An array of webhook objects
Example
Successful Retrieval of webhooks (200):

Request
curl -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/hooks?pageState=BNNBEACAtgALYWRzay53aXBkZXYNZnMuZmlsZS5hZGRlZAZmb2xkZXIydXJuOmFkc2sud2lwcWE6ZnMuZm9sZGVyOmNvLlRSM253QUtoVFNDQ0x0azY0VE52Q2cydXJuOmFkc2sud2lwcWE6ZnMuZm9sZGVyOmNvLlRSM253QUtoVFNDQ0x0azY0VE52Q2ctaHR0cDovL2FwaS53ZWJob29raW5ib3guY29tL2kvM0l6eGlLZndmL2luL3gy8H____3wf____Twpc5_2RqlBtCsLMPJlT9kABA=='\
     -H 'Authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
Response
HTTP/1.1 200
Content-Type: application/json
Date: Fri, 14 Sep 2017 17:14:09 GMT
Connection: keep-alive
{

  "links": {
    "next": "/systems/data/hooks?pageState=AMMAEACAtgALYWRzay53aXBkZXYNZnMuZmlsZS5hZGRlZAZmb2xkZXIydXJuOmFkc2sud2lwcWE6ZnMuZm9sZGVyOmNvLlRSM253QUtoVFNDQ0x0azY0VE52Q2cydXJuOmFkc2sud2lwcWE6ZnMuZm9sZGVyOmNvLlRSM253QUtoVFNDQ0x0azY0VE52Q2ctaHR0cDovL2FwaS53ZWJob29raW5ib3guY29tL2kvM0l6eGlLZndmL2luL3gy8H____3wf____Twpc5_2RqlBtCsLMPJlT9kABA=="
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
    "hookExpiry": "2017-09-21T17:04:10.444Z",
    "scope" : {
      "folder" : "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw"
    },
    "urn" : "urn:adsk.webhooks:events.hook:0f60f6a0-996c-11e7-abf3-51d68cff984c",
    "__self__" : "/systems/data/events/dm.version.added/hooks/0f60f6a0-996c-11e7-abf3-51d68cff984c"
  }, {
    "hookId" : "1f63f6a4-106c-11e7-qrf9-72d68cff984d",
    "tenant" : "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw",
    "callbackUrl" : "http://bf067e05.ngrok.io/callback",
    "createdBy" : "*********",
    "event" : "dm.version.copied",
    "createdDate" : "2017-09-14T17:04:10.564+0000",
    "lastUpdatedDate" : "2020-09-14T17:04:10.444+0000",
    "system" : "data",
    "creatorType": "Application",
    "status" : "active",
    "autoReactivateHook": false,
    "scope" : {
      "folder" : "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw"
    },
    "urn" : "urn:adsk.webhooks:events.hook:1f63f6a4-106c-11e7-qrf9-72d68cff984d",
    "__self__" : "/systems/data/events/dm.version.copied/hooks/1f63f6a4-106c-11e7-qrf9-72d68cff984d"
  }]

}

Documentation /Webhooks API /Reference Guide
GET	systems/:system/hooks
Retrieves a paginated list of all the webhooks for a specified system. If the pageState query string is not specified, the first page is returned.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/webhooks/v1/systems/:system/hooks
Authentication Context	
app only/ user context required
Required OAuth Scopes	
data:read
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via OAuth
x-ads-region
string
Specifies the geographical location (region) of the server that the request is executed on. Supported values are the following, but the default value is US:
US : (Default) Retrieves the webhooks that were registered in a data center dedicated to serve the United States.
EMEA : Retrieves the webhooks that were registered in a data center dedicated to serve the European Union, Middle East, and Africa.
AUS : (Beta) Retrieves the webhooks that were registered in a data center dedicated to serve Australia.
GBR : Retrieves the webhooks that were registered in a data center dedicated to serve United Kingdom.
JPN : Retrieves the webhooks that were registered in a data center dedicated to serve Japan.
DEU : Retrieves the webhooks that were registered in a data center dedicated to serve Germany.
CAN : Retrieves the webhooks that were registered in a data center dedicated to serve Canada.
IND : Retrieves the webhooks that were registered in a data center dedicated to serve India.
* Required
Request
URI Parameters
system
string
System for example: data
Request
Query String Parameters
status
string
Status of the hooks. Options: ‘active’, ‘inactive’
pageState
string
Base64 encoded string used to return the next page of the list of webhooks. This can be obtained from the next field of the previous page. PagingState instances are not portable and implementation is subject to change across versions. Default page size is 200.
region
string
Optional parameter to specify the region the request will be run in. Supported values are the following, but the default value is US:
US : (Default) Retrieves the webhooks that were registered in a data center dedicated to serve the United States.
EMEA : Retrieves the webhooks that were registered in a data center dedicated to serve the European Union, Middle East, and Africa.
AUS : (Beta) Retrieves the webhooks that were registered in a data center dedicated to serve Australia.
GBR : Retrieves the webhooks that were registered in a data center dedicated to serve United Kingdom.
JPN : Retrieves the webhooks that were registered in a data center dedicated to serve Japan.
DEU : Retrieves the webhooks that were registered in a data center dedicated to serve Germany.
CAN : Retrieves the webhooks that were registered in a data center dedicated to serve Canada.
IND : Retrieves the webhooks that were registered in a data center dedicated to serve India.
The x-ads-region header also specifies the region. If you specify both, x-ads-region has precedence.

Response
HTTP Status Code Summary
200
OK
Success.
204
EMPTY
No webhooks exist.
400
BAD REQUEST
The request is invalid.
401
UNAUTHORIZED
Invalid authorization header.
403
FORBIDDEN
Access denied regardless of authorization status.
404
NOT FOUND
The specified resource was not found.
500
INTERNAL SERVICE ERROR
Unexpected service interruption
Response
Body Structure (200)
 Expand all
links
object
An object containing links to other pages of the paginated list of webhooks
data
array: object
An array of webhook objects
Example
Successful Retrieval of webhooks (200):

Request
curl -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/hooks?pageState=BNNBEACAtgALYWRzay53aXBkZXYNZnMuZmlsZS5hZGRlZAZmb2xkZXIydXJuOmFkc2sud2lwcWE6ZnMuZm9sZGVyOmNvLlRSM253QUtoVFNDQ0x0azY0VE52Q2cydXJuOmFkc2sud2lwcWE6ZnMuZm9sZGVyOmNvLlRSM253QUtoVFNDQ0x0azY0VE52Q2ctaHR0cDovL2FwaS53ZWJob29raW5ib3guY29tL2kvM0l6eGlLZndmL2luL3gy8H____3wf____Twpc5_2RqlBtCsLMPJlT9kABA=='\
     -H 'Authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
Response
HTTP/1.1 200
Content-Type: application/json
Date: Fri, 14 Sep 2017 17:14:09 GMT
Connection: keep-alive
{

  "links": {
    "next": "/systems/data/hooks?pageState=AMMAEACAtgALYWRzay53aXBkZXYNZnMuZmlsZS5hZGRlZAZmb2xkZXIydXJuOmFkc2sud2lwcWE6ZnMuZm9sZGVyOmNvLlRSM253QUtoVFNDQ0x0azY0VE52Q2cydXJuOmFkc2sud2lwcWE6ZnMuZm9sZGVyOmNvLlRSM253QUtoVFNDQ0x0azY0VE52Q2ctaHR0cDovL2FwaS53ZWJob29raW5ib3guY29tL2kvM0l6eGlLZndmL2luL3gy8H____3wf____Twpc5_2RqlBtCsLMPJlT9kABA=="
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
    "hookExpiry": "2017-09-21T17:04:10.444Z",
    "scope" : {
      "folder" : "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw"
    },
    "urn" : "urn:adsk.webhooks:events.hook:0f60f6a0-996c-11e7-abf3-51d68cff984c",
    "__self__" : "/systems/data/events/dm.version.added/hooks/0f60f6a0-996c-11e7-abf3-51d68cff984c"
  }, {
    "hookId" : "1f63f6a4-106c-11e7-qrf9-72d68cff984d",
    "tenant" : "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw",
    "callbackUrl" : "http://bf067e05.ngrok.io/callback",
    "createdBy" : "*********",
    "event" : "dm.version.copied",
    "createdDate" : "2017-09-14T17:04:10.564+0000",
    "lastUpdatedDate" : "2020-09-14T17:04:10.444+0000",
    "system" : "data",
    "creatorType": "Application",
    "status" : "active",
    "autoReactivateHook": false,
    "scope" : {
      "folder" : "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw"
    },
    "urn" : "urn:adsk.webhooks:events.hook:1f63f6a4-106c-11e7-qrf9-72d68cff984d",
    "__self__" : "/systems/data/events/dm.version.copied/hooks/1f63f6a4-106c-11e7-qrf9-72d68cff984d"
  }]

}

Documentation /Webhooks API /Reference Guide
GET	hooks
Retrieves a paginated list of all the webhooks. If the pageState query string is not specified, the first page is returned.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/webhooks/v1/hooks
Authentication Context	
app only/ user context required
Required OAuth Scopes	
data:read
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via OAuth
x-ads-region
string
Specifies the geographical location (region) of the server that the request is executed on. Supported values are the following, but the default value is US:
US : (Default) Retrieves the webhooks that were registered in a data center dedicated to serve the United States.
EMEA : Retrieves the webhooks that were registered in a data center dedicated to serve the European Union, Middle East, and Africa.
AUS : (Beta) Retrieves the webhooks that were registered in a data center dedicated to serve Australia.
GBR : Retrieves the webhooks that were registered in a data center dedicated to serve United Kingdom.
JPN : Retrieves the webhooks that were registered in a data center dedicated to serve Japan.
DEU : Retrieves the webhooks that were registered in a data center dedicated to serve Germany.
CAN : Retrieves the webhooks that were registered in a data center dedicated to serve Canada.
IND : Retrieves the webhooks that were registered in a data center dedicated to serve India.
* Required
Request
Query String Parameters
pageState
String
Base64 encoded string used to return the next page of the list of webhooks. This can be obtained from the next field of the previous page. PagingState instances are not portable and implementation is subject to change across versions. Default page size is 200.
status
String
Status of the hooks. Options: ‘active’, ‘inactive’
region
string
Specifies the geographical location (region) of the server that the request is executed on. Supported values are the following, but the default value is US:
US : (Default) Retrieves the webhooks that were registered in a data center dedicated to serve the United States.
EMEA : Retrieves the webhooks that were registered in a data center dedicated to serve the European Union, Middle East, and Africa.
AUS : (Beta) Retrieves the webhooks that were registered in a data center dedicated to serve Australia.
GBR : Retrieves the webhooks that were registered in a data center dedicated to serve United Kingdom.
JPN : Retrieves the webhooks that were registered in a data center dedicated to serve Japan.
DEU : Retrieves the webhooks that were registered in a data center dedicated to serve Germany.
CAN : Retrieves the webhooks that were registered in a data center dedicated to serve Canada.
IND : Retrieves the webhooks that were registered in a data center dedicated to serve India.
The x-ads-region header also specifies the region. If you specify both, x-ads-region has precedence.

Response
HTTP Status Code Summary
200
OK
Success.
204
EMPTY
No webhooks exist.
400
BAD REQUEST
The request is invalid.
401
UNAUTHORIZED
Invalid authorization header.
403
FORBIDDEN
Access denied regardless of authorization status.
404
NOT FOUND
The specified resource was not found.
500
INTERNAL SERVICE ERROR
Unexpected service interruption
Response
Body Structure (200)
 Expand all
links
object
An object containing links to other pages of the paginated list of webhooks
data
array: object
An array of webhook objects
Example
Successful Retrieval of webhooks (200):

Request
curl -v 'https://developer.api.autodesk.com/webhooks/v1/hooks?pageState=BNNBEACAtgALYWRzay53aXBkZXYNZnMuZmlsZS5hZGRlZAZmb2xkZXIydXJuOmFkc2sud2lwcWE6ZnMuZm9sZGVyOmNvLlRSM253QUtoVFNDQ0x0azY0VE52Q2cydXJuOmFkc2sud2lwcWE6ZnMuZm9sZGVyOmNvLlRSM253QUtoVFNDQ0x0azY0VE52Q2ctaHR0cDovL2FwaS53ZWJob29raW5ib3guY29tL2kvM0l6eGlLZndmL2luL3gy8H____3wf____Twpc5_2RqlBtCsLMPJlT9kABA=='\
     -H 'Authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'
Response
HTTP/1.1 200
Content-Type: application/json
Date: Fri, 14 Sep 2017 17:14:09 GMT
Connection: keep-alive
{
  "links": {
    "next": "/hooks?pageState=AMMAEACAtgALYWRzay53aXBkZXYNZnMuZmlsZS5hZGRlZAZmb2xkZXIydXJuOmFkc2sud2lwcWE6ZnMuZm9sZGVyOmNvLlRSM253QUtoVFNDQ0x0azY0VE52Q2cydXJuOmFkc2sud2lwcWE6ZnMuZm9sZGVyOmNvLlRSM253QUtoVFNDQ0x0azY0VE52Q2ctaHR0cDovL2FwaS53ZWJob29raW5ib3guY29tL2kvM0l6eGlLZndmL2luL3gy8H____3wf____Twpc5_2RqlBtCsLMPJlT9kABA=="
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
    "status": "active",
    "autoReactivateHook": false,
    "hookExpiry": "2017-09-21T17:04:10.444Z",
    "scope" : {
      "folder" : "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw"
    },
    "urn" : "urn:adsk.webhooks:events.hook:0f60f6a0-996c-11e7-abf3-51d68cff984c",
    "__self__" : "/systems/data/events/dm.version.added/hooks/0f60f6a0-996c-11e7-abf3-51d68cff984c"
  }, {
    "hookId" : "1f63f6a4-106c-11e7-qrf9-72d68cff984d",
    "tenant" : "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw",
    "callbackUrl" : "http://bf067e05.ngrok.io/callback",
    "createdBy" : "*********",
    "event" : "dm.version.copied",
    "createdDate" : "2017-09-14T17:04:10.564+0000",
    "lastUpdatedDate" : "2020-09-14T17:04:10.444+0000",
    "system" : "data",
    "creatorType": "Application",
    "status" : "active",
    "autoReactivateHook": false,
    "scope" : {
      "folder" : "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw"
    },
    "urn" : "urn:adsk.webhooks:events.hook:1f63f6a4-106c-11e7-qrf9-72d68cff984d",
    "__self__" : "/systems/data/events/dm.version.copied/hooks/1f63f6a4-106c-11e7-qrf9-72d68cff984d"
  }]

}

Documentation /Webhooks API /Reference Guide
GET	app/hooks
Retrieves a paginated list of webhooks created in the context of a Client or Application. This API accepts 2-legged token of the application only. If the pageState query string is not specified, the first page is returned.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/webhooks/v1/app/hooks
Authentication Context	
app only (2-legged token)
Required OAuth Scopes	
data:read
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via OAuth. A 2-legged token is required for this API.
x-ads-region
string
Specifies the geographical location (region) of the server that the request is executed on. Supported values are the following, but the default value is US:
US : (Default) Retrieves the webhooks that were registered in a data center dedicated to serve the United States.
EMEA : Retrieves the webhooks that were registered in a data center dedicated to serve the European Union, Middle East, and Africa.
AUS : (Beta) Retrieves the webhooks that were registered in a data center dedicated to serve Australia.
GBR : Retrieves the webhooks that were registered in a data center dedicated to serve United Kingdom.
JPN : Retrieves the webhooks that were registered in a data center dedicated to serve Japan.
DEU : Retrieves the webhooks that were registered in a data center dedicated to serve Germany.
CAN : Retrieves the webhooks that were registered in a data center dedicated to serve Canada.
IND : Retrieves the webhooks that were registered in a data center dedicated to serve India.
* Required
Request
Query String Parameters
pageState
String
Base64 encoded string used to return the next page of the list of webhooks. This can be obtained from the next field of the previous page. PagingState instances are not portable and implementation is subject to change across versions. Default page size is 200.
status
String
Status of the hooks. Options: ‘active’, ‘inactive’. Default is ‘active’.
sort
String
Sort order of the hooks based on last updated time. Options: ‘asc’, ‘desc’. Default is ‘desc’.
region
string
Specifies the geographical location (region) of the server that the request is executed on. Supported values are the following, but the default value is US:
US : (Default) Retrieves the webhooks that were registered in a data center dedicated to serve the United States.
EMEA : Retrieves the webhooks that were registered in a data center dedicated to serve the European Union, Middle East, and Africa.
AUS : (Beta) Retrieves the webhooks that were registered in a data center dedicated to serve Australia.
GBR : Retrieves the webhooks that were registered in a data center dedicated to serve United Kingdom.
JPN : Retrieves the webhooks that were registered in a data center dedicated to serve Japan.
DEU : Retrieves the webhooks that were registered in a data center dedicated to serve Germany.
CAN : Retrieves the webhooks that were registered in a data center dedicated to serve Canada.
IND : Retrieves the webhooks that were registered in a data center dedicated to serve India.
The x-ads-region header also specifies the region. If you specify both, x-ads-region has precedence.

Response
HTTP Status Code Summary
200
OK
Success.
204
EMPTY
No webhooks exist.
400
BAD REQUEST
The request is invalid.
401
UNAUTHORIZED
Invalid authorization header.
403
FORBIDDEN
Access denied regardless of authorization status.
404
NOT FOUND
The specified resource was not found.
500
INTERNAL SERVICE ERROR
Unexpected service interruption
Response
Body Structure (200)
 Expand all
links
object
An object containing links to other pages of the paginated list of webhooks
data
array: object
An array of webhook objects
Example
Successful Retrieval of webhooks (200):

Request
curl -v 'https://developer.api.autodesk.com/webhooks/v1/app/hooks?sort=desc&status=inactive&pageState=BNNBEACAtgALYWRzay53aXBkZXYNZnMuZmlsZS5hZGRlZAZmb2xkZXIydXJuOmFkc2sud2lwcWE6ZnMuZm9sZGVyOmNvLlRSM253QUtoVFNDQ0x0azY0VE52Q2cydXJuOmFkc2sud2lwcWE6ZnMuZm9sZGVyOmNvLlRSM253QUtoVFNDQ0x0azY0VE52Q2ctaHR0cDovL2FwaS53ZWJob29raW5ib3guY29tL2kvM0l6eGlLZndmL2luL3gy8H____3wf____Twpc5_2RqlBtCsLMPJlT9kABA=='\
     -H 'Authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'
Response
HTTP/1.1 200
Content-Type: application/json
Date: Fri, 14 Sep 2017 17:14:09 GMT
Connection: keep-alive
{
  "links": {
    "next": "/hooks?pageState=AMMAEACAtgALYWRzay53aXBkZXYNZnMuZmlsZS5hZGRlZAZmb2xkZXIydXJuOmFkc2sud2lwcWE6ZnMuZm9sZGVyOmNvLlRSM253QUtoVFNDQ0x0azY0VE52Q2cydXJuOmFkc2sud2lwcWE6ZnMuZm9sZGVyOmNvLlRSM253QUtoVFNDQ0x0azY0VE52Q2ctaHR0cDovL2FwaS53ZWJob29raW5ib3guY29tL2kvM0l6eGlLZndmL2luL3gy8H____3wf____Twpc5_2RqlBtCsLMPJlT9kABA=="
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
    "status": "active",
    "autoReactivateHook": false,
    "hookExpiry": "2017-09-21T17:04:10.444Z",
    "scope" : {
      "folder" : "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw"
    },
    "urn" : "urn:adsk.webhooks:events.hook:0f60f6a0-996c-11e7-abf3-51d68cff984c",
    "__self__" : "/systems/data/events/dm.version.added/hooks/0f60f6a0-996c-11e7-abf3-51d68cff984c"
  }, {
    "hookId" : "1f63f6a4-106c-11e7-qrf9-72d68cff984d",
    "tenant" : "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw",
    "callbackUrl" : "http://bf067e05.ngrok.io/callback",
    "createdBy" : "*********",
    "event" : "dm.version.copied",
    "createdDate" : "2017-09-14T17:04:10.564+0000",
    "lastUpdatedDate" : "2020-09-14T17:04:10.444+0000",
    "system" : "data",
    "creatorType": "Application",
    "status" : "active",
    "autoReactivateHook": false,
    "scope" : {
      "folder" : "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw"
    },
    "urn" : "urn:adsk.webhooks:events.hook:1f63f6a4-106c-11e7-qrf9-72d68cff984d",
    "__self__" : "/systems/data/events/dm.version.copied/hooks/1f63f6a4-106c-11e7-qrf9-72d68cff984d"
  }]

}

Documentation /Webhooks API /Reference Guide
POST	systems/:system/events/:event/hooks
Add new webhook to receive the notification on a specified event.

Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/webhooks/v1/systems/:system/events/:event/hooks
Authentication Context	
app only/ user context required
Required OAuth Scopes	
data:read data:write
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via OAuth
Content-Type*
string
Must be application/json
x-ads-region
string
Specifies the geographical location (region) of the server that the request is executed on. Supported values are the following, but the default value is US:
US : (Default) Register a new webhook in a data center dedicated to serve the United States.
EMEA : Register a new webhook in a data center dedicated to serve the European Union, Middle East, and Africa.
AUS : (Beta) Register a new webhook in a data center dedicated to serve Australia.
GBR : Register a new webhook in a data center dedicated to serve United Kingdom.
JPN : Register a new webhook in a data center dedicated to serve Japan.
DEU : Register a new webhook in a data center dedicated to serve Germany.
CAN : Register a new webhook in a data center dedicated to serve Canada.
IND : Register a new webhook in a data center dedicated to serve India.
* Required
Request
URI Parameters
system
string
A system for example: data
for Data Management
event
string
Type of event. See Supported Events
Request
Query String Parameters
region
string
Specifies the geographical location (region) of the server that the request is executed on. Supported values are the following, but the default value is US:
US : (Default) Processes request in a data center dedicated to serve the United States.
EMEA : Processes request in a data center dedicated to serve the European Union, Middle East, and Africa.
AUS : (Beta) Processes request in a data center dedicated to serve Australia.
The x-ads-region header also specifies the region. If you specify both, x-ads-region has precedence.

Request
Body Structure
callbackUrl*
string
Callback URL registered for the webhook
scope*
object
An object that represents the extent to where the event is monitored. For example, if the scope is folder, the webhooks service generates a notification for the specified event occurring in any sub folder or item within that folder. Please refer to the individual event specification pages for valid scopes. For example, Data Management events.
hookAttribute
object
A user-defined JSON object, which you can use to store/set some custom information. The maximum size of the JSON object (content) should be less than 1KB
filter
string
JsonPath expression that can be used by you to filter the callbacks you receive.
hubId
string
Optional field which should be provided if the user is a member of a large number of projects. This hub ID corresponds to an account ID in the BIM 360 API, prefixed by “b.”
projectId
string
Optional field which should be provided if the user is a member of a large number of projects. This project ID corresponds to the project ID in the BIM 360 API, prefixed by “b.”
tenant
string
The tenant that the event is from. If the tenant is specified on the hook, then either the tenant or the scopeValue of the event must match the tenant of the hook.
autoReactivateHook
boolean
Optional. Flag to enable the hook for the automatic reactivation flow. Please see Event Delivery Guarantees for more details.
hookExpiry
string
Optional. ISO8601 formatted date and time when the hook should expire and automatically be deleted. Not providing this parameter means the hook never expires.
callbackWithEventPayloadOnly
boolean
Optional. If “true”, the callback request payload only contains the event payload, without additional information on the hook. Hook attributes will not be accessible if this is “true”. Defaults to “false”.
* Required
Response
HTTP Status Code Summary
201
OK
Successful.
400
BAD REQUEST
The request is invalid.
401
UNAUTHORIZED
Invalid authorization header.
403
FORBIDDEN
Access denied regardless of authorization status.
404
NOT FOUND
The specified resource was not found.
409
CONFLICT
The specified webhook already exists.
500
INTERNAL SERVICE ERROR
Unexpected service interruption
Example
Successful Creation of a webhook (201)
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.version.added/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "autoReactivateHook": false,
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
            "hookExpiry": "2017-09-21T17:04:10.444Z"
      }'
Show Less
Response
HTTP/1.1 201
Date: Thu, 14 Sep 2017 16:45:05 GMT
Location: https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.version.added/hooks/0f60f6a0-996c-11e7-abf3-51d68cff984c
Content-Length: 0
Connection: keep-alive


Documentation /Webhooks API /Reference Guide
POST	systems/:system/hooks
Add new webhooks to receive the notification on all the events.

Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/webhooks/v1/systems/:system/hooks
Authentication Context	
app only/ user context required
Required OAuth Scopes	
data:read data:write
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via OAuth
Content-Type*
string
Must be application/json
x-ads-region
string
Specifies the geographical location (region) of the server that the request is executed on. Supported values are the following, but the default value is US:
US : (Default) Register new webhooks in a data center dedicated to serve the United States.
EMEA : Register new webhooks in a data center dedicated to serve the European Union, Middle East, and Africa.
AUS : (Beta) Register new webhooks in a data center dedicated to serve Australia.
GBR : Register new webhooks in a data center dedicated to serve United Kingdom.
JPN : Register new webhooks in a data center dedicated to serve Japan.
DEU : Register new webhooks in a data center dedicated to serve Germany.
CAN : Register new webhooks in a data center dedicated to serve Canada.
IND : Register new webhooks in a data center dedicated to serve India.
* Required
Request
URI Parameters
system
string
A system for example: data
for Data Management
region
string
Optional parameter to specify the region the request will be run in. Supported values are the following, but the default value is US:
US :
EMEA :
AUS : (Beta) Australia (Beta)
GBR : United Kingdom
JPN : Japan
DEU : Germany
CAN : Canada
IND : India
The x-ads-region header also specifies the region. If you specify both, x-ads-region has precedence.

Request
Body Structure
callbackUrl*
string
Callback URL registered for the webhook
scope*
object
An object that represents the extent to where the event is monitored. For example, if the scope is folder, the webhooks service generates a notification for the specified event occurring in any sub folder or item within that folder. Please refer to the individual event specification pages for valid scopes. For example, Data Management events.
hookAttribute
object
A user-defined JSON object, which you can use to store/set some custom information. The maximum size of the JSON object (content) should be less than 1KB
filter
string
JsonPath expression that can be used by you to filter the callbacks you receive.
hubId
string
Optional field which should be provided if the user is a member of a large number of projects. This hub ID corresponds to an account ID in the BIM 360 API, prefixed by “b.”
projectId
string
Optional field which should be provided if the user is a member of a large number of projects. This project ID corresponds to the project ID in the BIM 360 API, prefixed by “b.”
tenant
string
The tenant that the event is from. If the tenant is specified on the hook, then either the tenant or the scopeValue of the event must match the tenant of the hook.
autoReactivateHook
boolean
Optional. Flag to enable the hook for the automatic reactivation flow. Please see Event Delivery Guarantees for more details.
hookExpiry
string
Optional. ISO8601 formatted date and time when the hook should expire and automatically be deleted. Not providing this parameter means the hook never expires.
callbackWithEventPayloadOnly
boolean
Optional. If “true”, the callback request payload only contains the event payload, without additional information on the hook. Hook attributes will not be accessible if this is “true”. Defaults to “false”.
* Required
Response
HTTP Status Code Summary
201
OK
Successful creation of one or more hooks.
400
BAD REQUEST
The request is invalid.
401
UNAUTHORIZED
Invalid authorization header.
403
FORBIDDEN
Access denied regardless of authorization status.
404
NOT FOUND
The specified resource was not found.
500
INTERNAL SERVICE ERROR
Unexpected service interruption
Response
Body Structure (201)
hooks
array: object
An array of webhook objects created by this request
hooks.hooks[i]
object
An element of the array. Represents a webhook
hooks.hooks[i].hookId
string
Webhook ID
hooks.hooks[i].callbackUrl
string
Callback URL registered for the webhook
hooks.hooks[i].createdBy
string
Client ID or User ID
hooks.hooks[i].createdDate
date
Date and time when webhook was created
hooks.hooks[i].event
string
Type of event that is being monitored. Wildcard values can potentially represent more than one event being monitored depending on the matching pattern.
hooks.hooks[i].scope
object
An object that represents the extent to where the event is monitored. For example, if the scope is folder, the webhooks service generates a notification for the specified event occurring in any sub folder or item within that folder
hooks.hooks[i].scope.folder
string
Data Management event scope, see here for more information
hooks.hooks[i].scope.workflow
string
Model Derivative event scope, see here for more information.
hooks.hooks[i].status
string
active if webhook is active; otherwise inactive
hooks.hooks[i].urn
string
URN of the webhook
hooks.hooks[i].hookExpiry
string
Optional: ISO8601 formatted date and time when the hook should expire and automatically be deleted. null or not present means the hook never expires.
hooks.hooks[i].__self__
string
Location of this webhook relative to /webhooks/v1/
Example
Successful Creation of a webhook (201):

Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "scope": {
                 "folder": "urn:adsk.wipprod:fs.folder:co.CHO-BbcmTsigjzymYeRCmQ"
            }
      }'
Show Less
Response
HTTP/1.1 201
Date: Thu, 14 Sep 2017 16:45:05 GMT
Location: https://developer.api.autodesk.com/webhooks/v1/systems/data/hooks
Content-Length: 0
Connection: keep-alive

{
    "hooks": [
        {
            "hookId": "04f1033e-aa58-11e7-abc4-cec278b6b50a",
            "tenant": "urn:adsk.wipprod:fs.folder:co.CHO-BbcmTsigjzymYeRCmQ",
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "createdBy": "*****",
            "event": "dm.version.added",
            "createdDate": "2017-09-19T18:58:16.636+0000",
            "lastUpdatedDate" : "2020-09-14T17:04:10.444+0000",
            "system": "data",
            "creatorType": "O2User",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.CHO-BbcmTsigjzymYeRCmQ"
            },
            "status": "active",
            "autoReactivateHook": false,
            "urn": "urn:adsk.webhooks:events.hook:04f1033e-aa58-11e7-abc4-cec278b6b50a",
            "__self__": "/systems/data/events/dm.version.added/hooks/04f1033e-aa58-11e7-abc4-cec278b6b50a"
        },
        {
            "hookId": "04f1092e-aa58-11e7-abc4-cec278b6b50a",
            "tenant": "urn:adsk.wipprod:fs.folder:co.CHO-BbcmTsigjzymYeRCmQ",
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "createdBy": "*****",
            "event": "dm.version.copied",
            "createdDate": "2017-09-19T18:58:16.312+0000",
            "lastUpdatedDate" : "2020-09-14T17:04:10.444+0000",
            "system": "data",
            "creatorType": "O2User",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.CHO-BbcmTsigjzymYeRCmQ"
            },
            "status": "active",
            "autoReactivateHook": false,
            "urn": "urn:adsk.webhooks:events.hook:04f1092e-aa58-11e7-abc4-cec278b6b50a",
            "__self__": "/systems/data/events/dm.version.copied/hooks/04f1092e-aa58-11e7-abc4-cec278b6b50a"
        },
        {
            "hookId": "04f10a50-aa58-11e7-abc4-cec278b6b50a",
            "tenant": "urn:adsk.wipprod:fs.folder:co.CHO-BbcmTsigjzymYeRCmQ",
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "createdBy": "*****",
            "event": "dm.version.deleted",
            "createdDate": "2017-09-19T18:58:16.716+0000",
            "lastUpdatedDate" : "2020-09-14T17:04:10.444+0000",
            "system": "data",
            "creatorType": "O2User",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.CHO-BbcmTsigjzymYeRCmQ"
            },
            "status": "active",
            "autoReactivateHook": true,
            "urn": "urn:adsk.webhooks:events.hook:04f10a50-aa58-11e7-abc4-cec278b6b50a",
            "__self__": "/systems/data/events/dm.version.deleted/hooks/04f10a50-aa58-11e7-abc4-cec278b6b50a"
        },
        {
            "hookId": "04f10b22-aa58-11e7-abc4-cec278b6b50a",
            "tenant": "urn:adsk.wipprod:fs.folder:co.CHO-BbcmTsigjzymYeRCmQ",
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "createdBy": "*****",
            "event": "dm.version.modified",
            "createdDate": "2017-09-19T18:58:16.121+0000",
            "lastUpdatedDate" : "2020-09-14T17:04:10.444+0000",
            "system": "data",
            "creatorType": "O2User",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.CHO-BbcmTsigjzymYeRCmQ"
            },
            "status": "active",
            "autoReactivateHook": false,
            "urn": "urn:adsk.webhooks:events.hook:04f10b22-aa58-11e7-abc4-cec278b6b50a",
            "__self__": "/systems/data/events/dm.version.modified/hooks/04f10b22-aa58-11e7-abc4-cec278b6b50a"
        },
        {
            "hookId": "04f10bea-aa58-11e7-abc4-cec278b6b50a",
            "tenant": "urn:adsk.wipprod:fs.folder:co.CHO-BbcmTsigjzymYeRCmQ",
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "createdBy": "*****",
            "event": "dm.version.moved",
            "createdDate": "2017-09-19T18:58:16.819+0000",
            "lastUpdatedDate" : "2020-09-14T17:04:10.444+0000",
            "system": "data",
            "creatorType": "O2User",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.CHO-BbcmTsigjzymYeRCmQ"
            },
            "status": "active",
            "urn": "urn:adsk.webhooks:events.hook:04f10bea-aa58-11e7-abc4-cec278b6b50a",
            "__self__": "/systems/data/events/dm.version.moved/hooks/04f10bea-aa58-11e7-abc4-cec278b6b50a"
        },
        {
            "hookId": "04f10ca8-aa58-11e7-abc4-cec278b6b50a",
            "tenant": "urn:adsk.wipprod:fs.folder:co.CHO-BbcmTsigjzymYeRCmQ",
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "createdBy": "*****",
            "event": "dm.folder.added",
            "createdDate": "2017-09-19T18:58:16.636+0000",
            "lastUpdatedDate" : "2020-09-14T17:04:10.444+0000",
            "system": "data",
            "creatorType": "O2User",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.CHO-BbcmTsigjzymYeRCmQ"
            },
            "status": "active",
            "autoReactivateHook": false,
            "urn": "urn:adsk.webhooks:events.hook:04f10ca8-aa58-11e7-abc4-cec278b6b50a",
            "__self__": "/systems/data/events/dm.folder.added/hooks/04f10ca8-aa58-11e7-abc4-cec278b6b50a"
        },
        {
            "hookId": "04f10d70-aa58-11e7-abc4-cec278b6b50a",
            "tenant": "urn:adsk.wipprod:fs.folder:co.CHO-BbcmTsigjzymYeRCmQ",
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "createdBy": "*****",
            "event": "dm.folder.copied",
            "createdDate": "2017-09-19T18:58:16.215+0000",
            "lastUpdatedDate" : "2020-09-14T17:04:10.444+0000",
            "system": "data",
            "creatorType": "O2User",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.CHO-BbcmTsigjzymYeRCmQ"
            },
            "status": "active",
            "autoReactivateHook": true,
            "urn": "urn:adsk.webhooks:events.hook:04f10d70-aa58-11e7-abc4-cec278b6b50a",
            "__self__": "/systems/data/events/dm.folder.copied/hooks/04f10d70-aa58-11e7-abc4-cec278b6b50a"
        },
        {
            "hookId": "04f10e2e-aa58-11e7-abc4-cec278b6b50a",
            "tenant": "urn:adsk.wipprod:fs.folder:co.CHO-BbcmTsigjzymYeRCmQ",
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "createdBy": "*****",
            "event": "dm.folder.deleted",
            "createdDate": "2017-09-19T18:58:16.896+0000",
            "lastUpdatedDate" : "2020-09-14T17:04:10.444+0000",
            "system": "data",
            "creatorType": "O2User",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.CHO-BbcmTsigjzymYeRCmQ"
            },
            "status": "active",
            "autoReactivateHook": true,
            "urn": "urn:adsk.webhooks:events.hook:04f10e2e-aa58-11e7-abc4-cec278b6b50a",
            "__self__": "/systems/data/events/dm.folder.deleted/hooks/04f10e2e-aa58-11e7-abc4-cec278b6b50a"
        },
        {
            "hookId": "04f10e2e-aa58-11e7-abc4-cec278b6b50a",
            "tenant": "urn:adsk.wipprod:fs.folder:co.CHO-BbcmTsigjzymYeRCmQ",
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "createdBy": "*****",
            "event": "dm.folder.purged",
            "createdDate": "2017-09-19T18:58:16.896+0000",
            "lastUpdatedDate" : "2020-09-14T17:04:10.444+0000",
            "system": "data",
            "creatorType": "O2User",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.CHO-BbcmTsigjzymYeRCmQ"
            },
            "status": "active",
            "autoReactivateHook": true,
            "urn": "urn:adsk.webhooks:events.hook:04f10e2e-aa58-11e7-abc4-cec278b6b50a",
            "__self__": "/systems/data/events/dm.folder.purged/hooks/04f10e2e-aa58-11e7-abc4-cec278b6b50a"
        },
        {
            "hookId": "04f112d4-aa58-11e7-abc4-cec278b6b50a",
            "tenant": "urn:adsk.wipprod:fs.folder:co.CHO-BbcmTsigjzymYeRCmQ",
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "createdBy": "*****",
            "event": "dm.folder.modified",
            "createdDate": "2017-09-19T18:58:16.771+0000",
            "lastUpdatedDate" : "2020-09-14T17:04:10.444+0000",
            "system": "data",
            "creatorType": "O2User",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.CHO-BbcmTsigjzymYeRCmQ"
            },
            "status": "active",
            "autoReactivateHook": false,
            "urn": "urn:adsk.webhooks:events.hook:04f112d4-aa58-11e7-abc4-cec278b6b50a",
            "__self__": "/systems/data/events/dm.folder.modified/hooks/04f112d4-aa58-11e7-abc4-cec278b6b50a"
        },
        {
            "hookId": "04f113d8-aa58-11e7-abc4-cec278b6b50a",
            "tenant": "urn:adsk.wipprod:fs.folder:co.CHO-BbcmTsigjzymYeRCmQ",
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "createdBy": "*****",
            "event": "dm.folder.moved",
            "createdDate": "2017-09-19T18:58:16.229+0000",
            "lastUpdatedDate" : "2020-09-14T17:04:10.444+0000",
            "system": "data",
            "creatorType": "O2User",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.CHO-BbcmTsigjzymYeRCmQ"
            },
            "status": "active",
            "autoReactivateHook": false,
            "urn": "urn:adsk.webhooks:events.hook:04f113d8-aa58-11e7-abc4-cec278b6b50a",
            "__self__": "/systems/data/events/dm.folder.moved/hooks/04f113d8-aa58-11e7-abc4-cec278b6b50a"
        }
    ]
}

Documentation /Webhooks API /Reference Guide
PATCH	systems/:system/events/:event/hooks/:hook_id
Partially update a webhook based on its webhook ID. The only fields that may be updated are: status, filter, hookAttribute, and hookExpiry.

Resource Information
Method and URI	
PATCH	https://developer.api.autodesk.com/webhooks/v1/systems/:system/events/:event/hooks/:hook_id
Authentication Context	
app only/ user context required
Required OAuth Scopes	
data:read data:write
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via OAuth
Content-Type*
string
application/json
x-ads-region
string
Specifies the geographical location (region) of the server that the request is executed on. Supported values are the following, but the default value is US:
US : (Default) Updates information for the webhook that was previously registered in a data center dedicated to serve the United States.
EMEA : Updates information for the webhook that was previously registered in a data center dedicated to serve the European Union, Middle East, and Africa.
AUS : (Beta) Updates information for the webhook that was previously registered in a data center dedicated to serve Australia.
GBR : Updates information for the webhook that was previously registered in a data center dedicated to serve United Kingdom.
JPN : Updates information for the webhook that was previously registered in a data center dedicated to serve Japan.
DEU : Updates information for the webhook that was previously registered in a data center dedicated to serve Germany.
CAN : Updates information for the webhook that was previously registered in a data center dedicated to serve Canada.
IND : Updates information for the webhook that was previously registered in a data center dedicated to serve India.
* Required
Request
URI Parameters
system
string
A system for example: data
for Data Management
event
string
Type of event. See Supported Events
hook_id
string
Id of the webhook to modify
Request
Body Structure
status
string
active if webhook is active; otherwise inactive
filter
string
JsonPath expression that can be used by you to filter the callbacks you receive.
hookAttribute
object
A user-defined JSON object, which you can use to store/set some custom information. The maximum size of the JSON object (content) should be less than 1KB
token
string
A secret token that is used to generate a hash signature, which is passed along with notification requests to the callback URL
autoReactivateHook
boolean
Flag to enable the hook for the automatic reactivation flow. Please see webhook field guide for more details.
hookExpiry
string
ISO8601 formatted date and time when the hook should expire and automatically be deleted. Providing null or an empty string updates the hook so that it never expires.
Request
Query String Parameters
region
string
Specifies the geographical location (region) of the server that the request is executed on. Supported values are the following, but the default value is US:
US : (Default) Processes request in a data center dedicated to serve the United States.
EMEA : Processes request in a data center dedicated to serve the European Union, Middle East, and Africa.
AUS : (Beta) Processes request in a data center dedicated to serve Australia.
The x-ads-region header also specifies the region. If you specify both, x-ads-region has precedence.

Response
HTTP Status Code Summary
200
OK
Successful.
400
BAD REQUEST
The request is invalid.
401
UNAUTHORIZED
Invalid authorization header.
403
FORBIDDEN
Access denied regardless of authorization status.
404
NOT FOUND
The specified resource was not found.
500
INTERNAL SERVICE ERROR
Unexpected service interruption
Example 1
Successful Patch of a webhook:

Request
curl -X 'PATCH'
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.version.added/hooks/05f10350-991a-11e7-8cd7-91969336b9c2'
     -H 'Content-Type: application/json'
     -H 'Authorization: Bearer 0X6mpTyg5IbH6YI8Okz2XJGpEDeK'
     -d '{
            "status": "active",
            "autoReactivateHook": false,
            "filter": "$[?(@.ext=='txt')]",
            "hookAttribute": {
                 /* Custom metadata */
                 "myfoo": 34,
                 "projectId": "someURN",
                 "myobject": {
                      "nested": true
                 }
            }
      }'
Show Less
Response
HTTP/1.1 204
Date: Fri, 15 Sep 2017 19:11:00 GMT
Content-Length: 0
Connection: keep-alive
Example 2
Successful deactivation of a webhook:

Request
curl -X 'PATCH'
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.version.added/hooks/05f10350-991a-11e7-8cd7-91969336b9c2'
     -H 'Content-Type: application/json'
     -H 'Authorization: Bearer 0X6mpTyg5IbH6YI8Okz2XJGpEDeK'
     -d '{
            "status": "inactive"
      }'
Response
HTTP/1.1 204
Date: Fri, 15 Sep 2017 19:11:00 GMT
Content-Length: 0
Connection: keep-alive
Example 3
Successful removal of existing filter and hook attributes:

Request
curl -X 'PATCH'
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.version.added/hooks/05f10350-991a-11e7-8cd7-91969336b9c2'
     -H 'Content-Type: application/json'
     -H 'Authorization: Bearer 0X6mpTyg5IbH6YI8Okz2XJGpEDeK'
     -d '{
            "filter": null,
            "hookAttribute": null
      }'
Show Less
Response
HTTP/1.1 204
Date: Fri, 15 Sep 2017 19:11:00 GMT
Content-Length: 0
Connection: keep-alive
Example 4
Successful update of hook expiry to a later date and time:

Request
curl -X 'PATCH'
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.version.added/hooks/05f10350-991a-11e7-8cd7-91969336b9c2'
     -H 'Content-Type: application/json'
     -H 'Authorization: Bearer 0X6mpTyg5IbH6YI8Okz2XJGpEDeK'
     -d '{
            "hookExpiry": ""2017-09-22T17:04:10.444Z""
      }'
Response
HTTP/1.1 204
Date: Fri, 15 Sep 2017 19:11:00 GMT
Content-Length: 0
Connection: keep-alive

Documentation /Webhooks API /Reference Guide
DELETE	systems/:system/events/:event/hooks/:hook_id
Deletes a webhook based on webhook ID

Resource Information
Method and URI	
DELETE	https://developer.api.autodesk.com/webhooks/v1/systems/:system/events/:event/hooks/:hook_id
Authentication Context	
app only/ user context required
Required OAuth Scopes	
data:read data:write
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via OAuth
Content-Type*
string
application/json
x-ads-region
string
Specifies the geographical location (region) of the server that the request is executed on. Supported values are the following, but the default value is US:
US : (Default) Removes the webhook that was previously registered in a data center dedicated to serve the United States.
EMEA : Removes the webhook that was previously registered in a data center dedicated to serve the European Union, Middle East, and Africa.
AUS : (Beta) Removes the webhook that was previously registered in a data center dedicated to serve Australia.
GBR : Removes the webhook that was previously registered in a data center dedicated to serve United Kingdom.
JPN : Removes the webhook that was previously registered in a data center dedicated to serve Japan.
DEU : Removes the webhook that was previously registered in a data center dedicated to serve Germany.
CAN : Removes the webhook that was previously registered in a data center dedicated to serve Canada.
IND : Removes the webhook that was previously registered in a data center dedicated to serve India.
* Required
Request
URI Parameters
system
string
A system for example: data
for Data Management
event
string
Type of event. See Supported Events
hook_id
string
Webhook ID to delete
Request
Query String Parameters
region
string
Specifies the geographical location (region) of the server that the request is executed on. Supported values are the following, but the default value is US:
US : (Default) Processes request in a data center dedicated to serve the United States.
EMEA : Processes request in a data center dedicated to serve the European Union, Middle East, and Africa.
AUS : (Beta) Processes request in a data center dedicated to serve Australia.
The x-ads-region header also specifies the region. If you specify both, x-ads-region has precedence.

Response
HTTP Status Code Summary
204
OK
Delete operation is successful.
400
BAD REQUEST
The request is invalid.
401
UNAUTHORIZED
Invalid authorization header.
403
FORBIDDEN
Access denied regardless of authorization status.
404
NOT FOUND
The specified resource was not found.
500
INTERNAL SERVICE ERROR
Unexpected service interruption
Examples
Successful Deletion of a webhook (204):

Request
curl -X DELETE\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.version.added/hooks/0f60f6a0-996c-11e7-abf3-51d68cff984c'\
     -H 'Authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'
Response
HTTP/1.1 204
Date: Fri, 15 Sep 2017 16:26:40 GMT
Content-Length: 0
Connection: keep-alive

Documentation /Webhooks API /Reference Guide
POST	tokens
Add a new Webhook secret token

Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/webhooks/v1/tokens
Authentication Context	
app only/ user context required
Required OAuth Scopes	
data:read data:write
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via OAuth
Content-Type*
string
Must be application/json
x-ads-region
string
Specifies the geographical location (region) of the server that the request is executed on. Supported values are the following, but the default value is US:
US : (Default) Save the token in a data center dedicated to serve the United States.
EMEA : Save the token in a data center dedicated to serve the European Union, Middle East, and Africa.
AUS : (Beta) Save the token in a data center dedicated to serve Australia.
GBR : Save the token in a data center dedicated to serve United Kingdom.
JPN : Save the token in a data center dedicated to serve Japan.
DEU : Save the token in a data center dedicated to serve Germany.
CAN : Save the token in a data center dedicated to serve Canada.
IND : Save the token in a data center dedicated to serve India.
* Required
Request
URI Parameters
region
string
Specifies the geographical location (region) of the server that the request is executed on. Supported values are the following, but the default value is US:
US : (Default) Save the token in a data center dedicated to serve the United States.
EMEA : Save the token in a data center dedicated to serve the European Union, Middle East, and Africa.
AUS : (Beta) Save the token in a data center dedicated to serve Australia.
GBR : Save the token in a data center dedicated to serve United Kingdom.
JPN : Save the token in a data center dedicated to serve Japan.
DEU : Save the token in a data center dedicated to serve Germany.
CAN : Save the token in a data center dedicated to serve Canada.
IND : Save the token in a data center dedicated to serve India.
The x-ads-region header also specifies the region. If you specify both, x-ads-region has precedence.

Body Structure
token*
string
A secret token that is used to generate a hash signature, which is passed along with notification requests to the callback URL
* Required
Response
HTTP Status Code Summary
200
OK
Successful.
400
BAD REQUEST
The request is invalid. Secret token already exists.
401
UNAUTHORIZED
Invalid authorization header.
403
FORBIDDEN
Access denied regardless of authorization status.
404
NOT FOUND
Endpoint does not exist.
500
INTERNAL SERVICE ERROR
Unexpected service interruption.
Response
Body Structure (200)
status
integer
A repititon of the response http status code
detail
array:string
An array of strings that provide a human readable description of the response
Example
Successful Creation of a Secret Token (200):

Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/tokens'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6Imp3dF9zeW1tZX'\
     -d '{
         "token":"awffbvdb3trf4fvdfbUyt39suHnbe5Mnrks3"
         }'
Response
HTTP/1.1 200
Date: Fri, 15 Sep 2017 19:11:00 GMT
Content-Length: 0
Connection: keep-alive

{
  "status": 200,
  "detail": [
      "Token created successfully for client: *****"
  ]
}
Documentation /Webhooks API /Reference Guide
PUT	tokens/@me
Update an existing Webhook secret token. Please note that the update can take up to 10 mins before being applied depending on the latest event delivery attempt which may still utilize the previous secret token. We recommend your callback accept both secret token values for a period of time to allow all requests to go through.

Resource Information
Method and URI	
PUT	https://developer.api.autodesk.com/webhooks/v1/tokens/@me
Authentication Context	
app only/ user context required
Required OAuth Scopes	
data:read data:write
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via OAuth
Content-Type*
string
Must be application/json
x-ads-region
string
Specifies the geographical location (region) of the server that the request is executed on. Supported values are the following, but the default value is US:
US : (Default) Updates the token that was previously saved in a data center dedicated to serve the United States.
EMEA : Updates the token that was previously saved in a data center dedicated to serve the European Union, Middle East, and Africa.
AUS : (Beta) Updates the token that was previously saved in a data center dedicated to serve Australia.
GBR : Updates the token that was previously saved in a data center dedicated to serve United Kingdom.
JPN : Updates the token that was previously saved in a data center dedicated to serve Japan.
DEU : Updates the token that was previously saved in a data center dedicated to serve Germany.
CAN : Updates the token that was previously saved in a data center dedicated to serve Canada.
IND : Updates the token that was previously saved in a data center dedicated to serve India.
* Required
Request
URI Parameters
region
string
Specifies the geographical location (region) of the server that the request is executed on. Supported values are the following, but the default value is US:
US : (Default) Updates the token that was previously saved in a data center dedicated to serve the United States.
EMEA : Updates the token that was previously saved in a data center dedicated to serve the European Union, Middle East, and Africa.
AUS : (Beta) Updates the token that was previously saved in a data center dedicated to serve Australia.
GBR : Updates the token that was previously saved in a data center dedicated to serve United Kingdom.
JPN : Updates the token that was previously saved in a data center dedicated to serve Japan.
DEU : Updates the token that was previously saved in a data center dedicated to serve Germany.
CAN : Updates the token that was previously saved in a data center dedicated to serve Canada.
IND : Updates the token that was previously saved in a data center dedicated to serve India.
The x-ads-region header also specifies the region. If you specify both, x-ads-region has precedence.

Body Structure
token*
string
The new secret token you want to use
* Required
Response
HTTP Status Code Summary
204
NO_CONTENT
Successful request but server is not returning any content.
400
BAD REQUEST
The request is invalid.
401
UNAUTHORIZED
Invalid authorization header.
403
FORBIDDEN
Access denied regardless of authorization status.
404
NOT FOUND
Endpoint or secret token does not exist.
500
INTERNAL SERVICE ERROR
Unexpected service interruption.
Example
Successful Update of a Secret Token (204):

Request
curl -X 'PUT'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/tokens/@me'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6Imp3dF9zeW1tZX'\
     -d '{
           "token":"awffbvdb3trf4fvdfbUyt39suHnbe5Mnrks1"
      }'
Response
HTTP/1.1 204
Date: Fri, 15 Sep 2017 19:11:00 GMT
Content-Length: 0
Connection: keep-alive

Documentation /Webhooks API /Reference Guide
DELETE	tokens/@me
Delete a Webhook secret token. Please note that the secret token can still be available for up to 10 mins depending on the latest event delivery attempt.

Resource Information
Method and URI	
DELETE	https://developer.api.autodesk.com/webhooks/v1/tokens/@me
Authentication Context	
app only/ user context required
Required OAuth Scopes	
data:read data:write
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via OAuth
Content-Type*
string
application/json
x-ads-region
string
Specifies the geographical location (region) of the server that the request is executed on. Supported values are the following, but the default value is US:
US : (Default) Deletes the token that was previously saved in a data center dedicated to serve the United States.
EMEA : Deletes the token that was previously saved in a data center dedicated to serve the European Union, Middle East, and Africa.
AUS : (Beta) Deletes the token that was previously saved in a data center dedicated to serve Australia.
GBR : Deletes the token that was previously saved in a data center dedicated to serve United Kingdom.
JPN : Deletes the token that was previously saved in a data center dedicated to serve Japan.
DEU : Deletes the token that was previously saved in a data center dedicated to serve Germany.
CAN : Deletes the token that was previously saved in a data center dedicated to serve Canada.
IND : Deletes the token that was previously saved in a data center dedicated to serve India.
* Required
URI Parameters
region
string
Specifies the geographical location (region) of the server that the request is executed on. Supported values are the following, but the default value is US:
US : (Default) Deletes the token that was previously saved in a data center dedicated to serve the United States.
EMEA : Deletes the token that was previously saved in a data center dedicated to serve the European Union, Middle East, and Africa.
AUS : (Beta) Deletes the token that was previously saved in a data center dedicated to serve Australia.
GBR : Deletes the token that was previously saved in a data center dedicated to serve United Kingdom.
JPN : Deletes the token that was previously saved in a data center dedicated to serve Japan.
DEU : Deletes the token that was previously saved in a data center dedicated to serve Germany.
CAN : Deletes the token that was previously saved in a data center dedicated to serve Canada.
IND : Deletes the token that was previously saved in a data center dedicated to serve India.
The x-ads-region header also specifies the region. If you specify both, x-ads-region has precedence.

Response
HTTP Status Code Summary
204
NO CONTENT
Successful deletion of secret token.
400
BAD REQUEST
The request is invalid.
401
UNAUTHORIZED
Invalid authorization header.
403
FORBIDDEN
Access denied regardless of authorization status.
404
NOT FOUND
Endpoint or secret token does not exist.
500
INTERNAL SERVICE ERROR
Unexpected service interruption.
Example
Successful Deletion of a Secret Token (204)

Request
curl -X 'DELETE'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/tokens/@me'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6Imp3dF9zeW1tZX'
Response
HTTP/1.1 204
Date: Fri, 15 Sep 2017 19:11:00 GMT
Content-Length: 0
Connection: keep-alive



可以參考github 的 sdk:
APS SDK for NodeJs
node.js npm license

The Autodesk Platform Services (APS) SDK for NodeJs helps NodeJs developer create applications that leverage the various APS services: Model Derivative, Data Management, OSS, Webhooks. More services soon.

Getting Help
Please use any of the following channels for support. Github issues to track SDK specific issues and feature requests.

Get Help at the Developer Portal has everything APS related.
Stackoverflow remember to tag autodesk-platform-services
Documentation, Tutorials & Samples
The Developer Portal has everything APS:

Documentation page for each service.
Visit APS Tutorials and select NodeJs tutorials.
Node Packages
Authentication
ACC Account Admin
ACC Issues
Data Management
Model Derivative
OSS
SDK Manager
Webhooks
Contributions
Contributions are welcome! Please make sure to read the contribution guidelines.

https://github.com/autodesk-platform-services/aps-sdk-node?tab=readme-ov-file


