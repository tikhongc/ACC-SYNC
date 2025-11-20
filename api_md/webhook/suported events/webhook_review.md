Documentation /Webhooks API /Reference Guide
review.created-1.0
Event:	
review.created-1.0
System:	
autodesk.construction.reviews
Scope:	
project
Trigger:	
When a review is created.
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/autodesk.construction.reviews/events/review.created-1.0/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -H 'region: US'\
     -d '{
            "callbackUrl": "https://d402-165-85-169-194.ngrok-free.app/callback",
            "scope": {
                "project": "48f5f5b1-d5d2-49a3-b311-bcb90c0b60cb"
            },
            "hookAttribute": {
                "projectId": "48f5f5b1-d5d2-49a3-b311-bcb90c0b60cb"
            }
        }'
Show More
The region header is US by default, or you can specify the region API value you want to use, see Region for more details.
Callback Payload
Headers
x-adsk-delivery-id
string
Payload delivery ID
x-adsk-signature
string
Hash-signature of the payload using secret token as the key.
It is prefixed with sha1hash=. Your callback endpoint can
verify the signature to validate the integrity of the payload.
Body Structure
 Expand all
version
string
The version of the callback payload. This is always 1.0.
resourceUrn
string
The UUID of the review that was created.
hook
object
The object that contains the details about the webhook.
payload
object
The object that contains details of the event that occurred.
Example Body
{
    "version": "1.0",
    "resourceUrn": "a4a3613c-c9dd-4e59-9d38-7b5a9857db9d",
    "hook": {
        "hookId": "afc16c9f-ddd5-470c-b4b9-dbab05775811",
        "tenant": "48f5f5b1-d5d2-49a3-b311-bcb90c0b60cb",
        "callbackUrl": "https://d402-165-85-169-194.ngrok-free.app/callback",
        "createdBy": "GTMMJRRXST63",
        "event": "review.created-1.0",
        "createdDate": "2024-09-05T06:02:40.925+00:00",
        "lastUpdatedDate": "2024-09-05T06:02:40.921+00:00",
        "system": "autodesk.construction.reviews",
        "creatorType": "O2User",
        "status": "active",
        "scope": {
            "project": "48f5f5b1-d5d2-49a3-b311-bcb90c0b60cb"
        },
        "hookAttribute": {
            "projectId": "48f5f5b1-d5d2-49a3-b311-bcb90c0b60cb"
        },
        "autoReactivateHook": true,
        "urn": "urn:adsk.webhooks:events.hook:afc16c9f-ddd5-470c-b4b9-dbab05775811",
        "callbackWithEventPayloadOnly": false,
        "__self__": "/systems/autodesk.construction.reviews/events/review.created-1.0/hooks/afc16c9f-ddd5-470c-b4b9-dbab05775811"
    },
    "payload": {
      "roundNum": 1,
      "sequenceId": "12",
      "status": "OPEN"
    }
}

Documentation /Webhooks API /Reference Guide
review.closed-1.0
Event:	
review.closed-1.0
System:	
autodesk.construction.reviews
Scope:	
project
Trigger:	
When a review is closed.
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/autodesk.construction.reviews/events/review.closed-1.0/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -H 'region: US'\
     -d '{
            "callbackUrl": "https://d402-165-85-169-194.ngrok-free.app/callback",
            "scope": {
                "project": "48f5f5b1-d5d2-49a3-b311-bcb90c0b60cb"
            },
            "hookAttribute": {
                "projectId": "48f5f5b1-d5d2-49a3-b311-bcb90c0b60cb"
            }
        }'
Show Less
The region header is US by default, or you can specify the region API value you want to use, see Region for more details.
Callback Payload
Headers
x-adsk-delivery-id
string
Payload delivery ID
x-adsk-signature
string
Hash-signature of the payload using secret token as the key.
It is prefixed with sha1hash=. Your callback endpoint can
verify the signature to validate the integrity of the payload.
Body Structure
 Expand all
version
string
The version of the callback payload. This is always 1.0.
resourceUrn
string
The UUID of the review that was closed.
hook
object
The object that contains the details about the webhook.
payload
object
The object that contains details of the event that occurred.
Example Body
{
    "version": "1.0",
    "resourceUrn": "a4a3613c-c9dd-4e59-9d38-7b5a9857db9d",
    "hook": {
        "hookId": "afc16c9f-ddd5-470c-b4b9-dbab05775811",
        "tenant": "48f5f5b1-d5d2-49a3-b311-bcb90c0b60cb",
        "callbackUrl": "https://d402-165-85-169-194.ngrok-free.app/callback",
        "createdBy": "GTMMJRRXST63",
        "event": "review.closed-1.0",
        "createdDate": "2024-09-05T06:02:40.925+00:00",
        "lastUpdatedDate": "2024-09-05T06:02:40.921+00:00",
        "system": "autodesk.construction.reviews",
        "creatorType": "O2User",
        "status": "active",
        "scope": {
            "project": "48f5f5b1-d5d2-49a3-b311-bcb90c0b60cb"
        },
        "hookAttribute": {
            "projectId": "48f5f5b1-d5d2-49a3-b311-bcb90c0b60cb"
        },
        "autoReactivateHook": true,
        "urn": "urn:adsk.webhooks:events.hook:afc16c9f-ddd5-470c-b4b9-dbab05775811",
        "callbackWithEventPayloadOnly": false,
        "__self__": "/systems/autodesk.construction.reviews/events/review.closed-1.0/hooks/afc16c9f-ddd5-470c-b4b9-dbab05775811"
    },
    "payload": {
      "roundNum": 2,
      "sequenceId": "14",
      "status": "CLOSED"
    }
}
