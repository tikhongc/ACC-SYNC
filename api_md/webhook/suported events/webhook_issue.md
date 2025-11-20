ACC Issue Events
The Webhooks service currently exposes the following types of Autodesk Construction Cloud (ACC) Issue events.

Note that all ACC Issues events apply to both placement and non-placement issues, except for issue.unlinked-1.0, which applies only to placement issues.

Placement issues are currently read-only in the Issues API — they can be retrieved using GET issues, but cannot be created or updated via the API.

System	Event	Description
autodesk.construction.issues	issue.created-1.0	When an issue is created.
autodesk.construction.issues	issue.updated-1.0	When an issue is updated.
autodesk.construction.issues	issue.deleted-1.0	When an issue is deleted.
autodesk.construction.issues	issue.restored-1.0	When an issue is restored.
autodesk.construction.issues	issue.unlinked-1.0	When an issue is unlinked from a placement.
Note: For more information about ACC Issues, see the ACC Issues API documentation.

Documentation /Webhooks API /Reference Guide
issue.created-1.0
Event:	
issue.created-1.0
System:	
autodesk.construction.issues
Scope:	
project
Trigger:	
When an issue is created.
Note that this event applies to both placement and non-placement issues.

Placement issues are currently read-only in the Issues API — they can be retrieved using GET issues, but cannot be created or updated via the API.

Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/autodesk.construction.issues/events/issue.created-1.0/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
           "callbackUrl": "http://bf067e05.ngrok.io/callback",
           "scope": {
             "project": "your-project-id"
           }
         }'
Show Less
Callback Payload
Headers
x-adsk-delivery-id
string
Payload delivery ID.
x-adsk-signature
string
Hash-signature of the payload using the secret token as the key.
It is prefixed with sha1hash=. Your callback endpoint can
verify the signature to validate the integrity of the payload.
Example Body
{
  "version": "1.0",
  "resourceUrn": "urn:adsk.issues:issues.issue:520aff8e-78a5-41fd-9b39-34e89c547953",
  "hook": {
    "hookId": "13f9a9eb-3cdb-4dc8-a04a-d12015c63d40",
    "tenant": "713c69f7-6131-4199-b260-5cd48f82a1de",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "V73BQ6TVMLWR",
    "event": "issue.created-1.0",
    "createdDate": "2025-04-20T12:02:16.598+00:00",
    "lastUpdatedDate": "2025-04-20T12:02:16.417+00:00",
    "system": "autodesk.construction.issues",
    "creatorType": "O2User",
    "status": "active",
    "scope": {
      "project": "713c69f7-6131-4199-b260-5cd48f82a1de"
    },
    "autoReactivateHook": true,
    "urn": "urn:adsk.webhooks:events.hook:13f9a9eb-3cdb-4dc8-a04a-d12015c63d40",
    "callbackWithEventPayloadOnly": false,
    "__self__": "/systems/autodesk.construction.issues/events/issue.created-1.0/hooks/13f9a9eb-3cdb-4dc8-a04a-d12015c63d40"
  },
  "payload":
  {
    "projectId": "713c69f7-6131-4199-b260-5cd48f82a1de",
    "id": "520aff8e-78a5-41fd-9b39-34e89c547953",
    "status": "open",
    "updatedAt": "2025-04-20T12:03:35.399Z",
    "issueTypeId": "6516bdd7-7300-4a8f-aa9c-3a2fd7fb59db",
    "issueSubtypeId": "b80b583b-34ab-4d19-8b84-3119955999fc",
    "assignedToType": null,
    "assignedTo": null,
    "dueDate": null,
    "watchers": []
  }
}

Documentation /Webhooks API /Reference Guide
issue.updated-1.0
Event:	
issue.updated-1.0
System:	
autodesk.construction.issues
Scope:	
project
Trigger:	
When an issue is updated.
Note that this event applies to both placement and non-placement issues.

Placement issues are currently read-only in the Issues API — they can be retrieved using GET issues, but cannot be created or updated via the API.

Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/autodesk.construction.issues/events/issue.updated-1.0/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
           "callbackUrl": "http://bf067e05.ngrok.io/callback",
           "scope": {
             "project": "your-project-id"
           }
         }'
Show Less
Callback Payload
Headers
x-adsk-delivery-id
string
Payload delivery ID.
x-adsk-signature
string
Hash-signature of the payload using the secret token as the key.
It is prefixed with sha1hash=. Your callback endpoint can
verify the signature to validate the integrity of the payload.
Example Body
{
  "version": "1.0",
  "resourceUrn": "urn:adsk.issues:issues.issue:b52f7f6a-f5e2-4e45-bec6-6de286eb3ecd",
  "hook": {
    "hookId": "46af6a80-d378-4d1e-9dcc-c729954e0f8c",
    "tenant": "1ab92088-f630-4401-8769-23d6fbb1d4ed",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "V73BQ6TVMLWR",
    "event": "issue.updated-1.0",
    "createdDate": "2025-04-07T13:52:41.899+00:00",
    "lastUpdatedDate": "2025-04-07T13:52:41.591+00:00",
    "system": "autodesk.construction.issues",
    "creatorType": "O2User",
    "status": "active",
    "scope": {
      "project": "1ab92088-f630-4401-8769-23d6fbb1d4ed"
    },
    "autoReactivateHook": true,
    "urn": "urn:adsk.webhooks:events.hook:46af6a80-d378-4d1e-9dcc-c729954e0f8c",
    "callbackWithEventPayloadOnly": false,
    "__self__": "/systems/autodesk.construction.issues/events/issue.updated-1.0/hooks/46af6a80-d378-4d1e-9dcc-c729954e0f8c"
  },
  "payload":
  {
    "projectId": "1ab92088-f630-4401-8769-23d6fbb1d4ed",
    "id": "b52f7f6a-f5e2-4e45-bec6-6de286eb3ecd",
    "status": "open",
    "updatedAt": "2025-04-20T12:08:09.619Z",
    "issueTypeId": "4e4281fa-a869-4c0a-a3b3-288d328bac8f",
    "issueSubtypeId": "92981f00-d3dc-404a-b2db-12e8c5e89157",
    "assignedToType": null,
    "assignedTo": null,
    "dueDate": null,
    "watchers": [
      "V73BQ6TVMLWR"
    ],
    "changedAttributes": [
      "watcher_objects"
    ]
  }
}

Documentation /Webhooks API /Reference Guide
issue.deleted-1.0
Event:	
issue.deleted-1.0
System:	
autodesk.construction.issues
Scope:	
project
Trigger:	
When an issue is deleted.
Note that this event applies to both placement and non-placement issues.

Placement issues are currently read-only in the Issues API — they can be retrieved using GET issues, but cannot be created or updated via the API.

Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/autodesk.construction.issues/events/issue.deleted-1.0/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
           "callbackUrl": "http://bf067e05.ngrok.io/callback",
           "scope": {
             "project": "your-project-id"
           }
         }'
Show Less
Callback Payload
Headers
x-adsk-delivery-id
string
Payload delivery ID.
x-adsk-signature
string
Hash-signature of the payload using the secret token as the key.
It is prefixed with sha1hash=. Your callback endpoint can
verify the signature to validate the integrity of the payload.
Example Body
{
  "version": "1.0",
  "resourceUrn": "urn:adsk.issues:issues.issue:b52f7f6a-f5e2-4e45-bec6-6de286eb3ecd",
  "hook": {
    "hookId": "1fbe2ed7-27b7-4c76-8cdc-f9790e99e9e5",
    "tenant": "1ab92088-f630-4401-8769-23d6fbb1d4ed",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "V73BQ6TVMLWR",
    "event": "issue.deleted-1.0",
    "createdDate": "2025-04-07T13:52:41.929+00:00",
    "lastUpdatedDate": "2025-04-07T13:52:41.591+00:00",
    "system": "autodesk.construction.issues",
    "creatorType": "O2User",
    "status": "active",
    "scope": {
      "project": "1ab92088-f630-4401-8769-23d6fbb1d4ed"
    },
    "autoReactivateHook": true,
    "urn": "urn:adsk.webhooks:events.hook:1fbe2ed7-27b7-4c76-8cdc-f9790e99e9e5",
    "callbackWithEventPayloadOnly": false,
    "__self__": "/systems/autodesk.construction.issues/events/issue.deleted-1.0/hooks/1fbe2ed7-27b7-4c76-8cdc-f9790e99e9e5"
  },
  "payload":
  {
    "projectId": "1ab92088-f630-4401-8769-23d6fbb1d4ed",
    "id": "b52f7f6a-f5e2-4e45-bec6-6de286eb3ecd",
    "status": "open",
    "updatedAt": "2025-04-20T12:08:57.068Z",
    "issueTypeId": "4e4281fa-a869-4c0a-a3b3-288d328bac8f",
    "issueSubtypeId": "92981f00-d3dc-404a-b2db-12e8c5e89157",
    "assignedToType": null,
    "assignedTo": null,
    "dueDate": null,
    "watchers": [
      "V73BQ6TVMLWR"
    ]
  }
}

Documentation /Webhooks API /Reference Guide
issue.restored-1.0
Event:	
issue.restored-1.0
System:	
autodesk.construction.issues
Scope:	
project
Trigger:	
When an issue is restored.
Note that this event applies to both placement and non-placement issues.

Placement issues are currently read-only in the Issues API — they can be retrieved using GET issues, but cannot be created or updated via the API.

Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/autodesk.construction.issues/events/issue.restored-1.0/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
           "callbackUrl": "http://bf067e05.ngrok.io/callback",
           "scope": {
             "project": "your-project-id"
           }
         }'
Show Less
Callback Payload
Headers
x-adsk-delivery-id
string
Payload delivery ID.
x-adsk-signature
string
Hash-signature of the payload using the secret token as the key.
It is prefixed with sha1hash=. Your callback endpoint can
verify the signature to validate the integrity of the payload.
Example Body
{
  "version": "1.0",
  "resourceUrn": "urn:adsk.issues:issues.issue:25c2b2fd-f942-4ab6-a805-9ce8b51a38e6",
  "hook": {
    "hookId": "478165d8-1817-446d-91a7-23291a6f4ca2",
    "tenant": "713c69f7-6131-4199-b260-5cd48f82a1de",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "V73BQ6TVMLWR",
    "event": "issue.restored-1.0",
    "createdDate": "2025-04-20T12:02:16.586+00:00",
    "lastUpdatedDate": "2025-04-20T12:02:16.417+00:00",
    "system": "autodesk.construction.issues",
    "creatorType": "O2User",
    "status": "active",
    "scope": {
      "project": "713c69f7-6131-4199-b260-5cd48f82a1de"
    },
    "autoReactivateHook": true,
    "urn": "urn:adsk.webhooks:events.hook:478165d8-1817-446d-91a7-23291a6f4ca2",
    "callbackWithEventPayloadOnly": false,
    "__self__": "/systems/autodesk.construction.issues/events/issue.restored-1.0/hooks/478165d8-1817-446d-91a7-23291a6f4ca2"
  },
  "payload":
  {
    "projectId": "713c69f7-6131-4199-b260-5cd48f82a1de",
    "id": "25c2b2fd-f942-4ab6-a805-9ce8b51a38e6",
    "status": "open",
    "updatedAt": "2025-04-20T12:04:48.688Z",
    "issueTypeId": "6516bdd7-7300-4a8f-aa9c-3a2fd7fb59db",
    "issueSubtypeId": "b80b583b-34ab-4d19-8b84-3119955999fc",
    "assignedToType": null,
    "assignedTo": null,
    "dueDate": null,
    "watchers": []
  }
}

Documentation /Webhooks API /Reference Guide
issue.unlinked-1.0
Event:	
issue.unlinked-1.0
System:	
autodesk.construction.issues
Scope:	
project
Trigger:	
When an issue is unlinked from a placement.
Note that this event applies only to placement issues — issues that are linked to a specific location on a drawing or model.

Placement issues are currently read-only in the Issues API — they can be retrieved using GET issues, but cannot be created, updated, or managed via the API.

Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/autodesk.construction.issues/events/issue.unlinked-1.0/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
           "callbackUrl": "http://bf067e05.ngrok.io/callback",
           "scope": {
             "project": "your-project-id"
           }
         }'
Show Less
Callback Payload
Headers
x-adsk-delivery-id
string
Payload delivery ID.
x-adsk-signature
string
Hash-signature of the payload using the secret token as the key.
It is prefixed with sha1hash=. Your callback endpoint can
verify the signature to validate the integrity of the payload.
Example Body
{
  "version": "1.0",
  "resourceUrn": "urn:adsk.issues:issues.issue:25c2b2fd-f942-4ab6-a805-9ce8b51a38e6",
  "hook": {
    "hookId": "478165d8-1817-446d-91a7-23291a6f4ca2",
    "tenant": "713c69f7-6131-4199-b260-5cd48f82a1de",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "V73BQ6TVMLWR",
    "event": "issue.unlinked-1.0",
    "createdDate": "2025-04-20T12:02:16.586+00:00",
    "lastUpdatedDate": "2025-04-20T12:02:16.417+00:00",
    "system": "autodesk.construction.issues",
    "creatorType": "O2User",
    "status": "active",
    "scope": {
      "project": "713c69f7-6131-4199-b260-5cd48f82a1de"
    },
    "autoReactivateHook": true,
    "urn": "urn:adsk.webhooks:events.hook:478165d8-1817-446d-91a7-23291a6f4ca2",
    "callbackWithEventPayloadOnly": false,
    "__self__": "/systems/autodesk.construction.issues/events/issue.unlinked-1.0/hooks/478165d8-1817-446d-91a7-23291a6f4ca2"
  },
  "payload":
  {
    "projectId": "713c69f7-6131-4199-b260-5cd48f82a1de",
    "id": "25c2b2fd-f942-4ab6-a805-9ce8b51a38e6",
    "status": "open",
    "updatedAt": "2025-04-20T12:04:48.688Z",
    "issueTypeId": "6516bdd7-7300-4a8f-aa9c-3a2fd7fb59db",
    "issueSubtypeId": "b80b583b-34ab-4d19-8b84-3119955999fc",
    "assignedToType": null,
    "assignedTo": null,
    "dueDate": null,
    "watchers": []
  }
}