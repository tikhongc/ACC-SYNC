Documentation /Webhooks API /Reference Guide
item.clone
Event:	
item.clone
System:	
adsk.flc.production (Fusion Lifecycle)
Scope:	
workspace
Trigger:	
When a Fusion Lifecycle item is cloned
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/adsk.flc.production/events/item.clone/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://callbackUrl.com/clone",
            "scope": {
                "workspace" : "urn:adsk.plm:tenant.workspace:TENANT.721"
            }
        }'
Show Less
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
Example Body
{
      "version" : "1.0",
      "resourceUrn" : "urn:adsk.plm:tenant.workspace.item:TENANT.721.109598",
      "hook" : {
        "hookId" : "7eceb920-6fde-11e8-a574-7b39610424dd",
        "tenant" : "TENANT",
        "callbackUrl" : "http://callbackUrl.com/clone",
        "createdBy" : "************",
        "event" : "item.clone",
        "createdDate" : "2018-06-14T14:23:23.570+0000",
        "system" : "adsk.flc.production",
        "creatorType" : "O2User",
        "status" : "active",
        "scope" : {
          "workspace" : "urn:adsk.plm:tenant.workspace:TENANT.721"
        },
        "urn" : "urn:adsk.webhooksdev:events.hook:7eceb920-6fde-11e8-a574-7b39610424dd",
        "__self__" : "/systems/adsk.flc.production/events/item.clone/hooks/7eceb920-6fde-11e8-a574-7b39610424dd"
      },
      "payload" : {
        "ItemUrn" : "urn:adsk.plm:tenant.workspace.item:TENANT.721.109597",
        "ItemDescription" : "NU000521",
        "NewItemUrn" : "urn:adsk.plm:tenant.workspace.item:TENANT.721.109598",
        "NewItemDescription" : "NU00052-2"
      }
}

Documentation /Webhooks API /Reference Guide
item.create
Event:	
item.create
System:	
adsk.flc.production (Fusion Lifecycle)
Scope:	
workspace
Trigger:	
When a Fusion Lifecycle item is created
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/adsk.flc.production/events/item.create/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://callbackUrl.com/create",
            "scope": {
                "workspace" : "urn:adsk.plm:tenant.workspace:TENANT.721"
            }
        }'
Show Less
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
Example Body
{
      "version" : "1.0",
      "resourceUrn" : "urn:adsk.plm:tenant.workspace.item:TENANT.721.109597",
      "hook" : {
        "hookId" : "7eceb920-6fde-11e8-a574-7b39610424dd",
        "tenant" : "TENANT",
        "callbackUrl" : "http://callbackurl.com/create",
        "createdBy" : "************",
        "event" : "item.create",
        "createdDate" : "2018-06-14T14:23:23.570+0000",
        "system" : "adsk.flc.production",
        "creatorType" : "O2User",
        "status" : "active",
        "scope" : {
          "workspace" : "urn:adsk.plm:tenant.workspace:TENANT.721"
        },
        "urn" : "urn:adsk.webhooks:events.hook:7eceb920-6fde-11e8-a574-7b39610424dd",
        "__self__" : "/systems/adsk.flc.production/events/item.create/hooks/7eceb920-6fde-11e8-a574-7b39610424dd"
      },
      "payload" : {
        "ItemUrn" : "urn:adsk.plm:tenant.workspace.item:TENANT.721.109597",
        "ItemDescription" : "NU000521"
      }
}

Documentation /Webhooks API /Reference Guide
item.lock
Event:	
item.lock
System:	
adsk.flc.production (Fusion Lifecycle)
Scope:	
workspace
Trigger:	
When a Fusion Lifecycle item transitions into a locked state
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/adsk.flc.production/events/item.lock/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://callbackUrl.com/lock",
            "scope": {
                "workspace" : "urn:adsk.plm:tenant.workspace:TENANT.721"
            }
        }'
Show Less
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
Example Body
{
      "version" : "1.0",
      "resourceUrn" : "urn:adsk.plm:tenant.workspace.item:TENANT.721.109597",
      "hook" : {
        "hookId" : "7eceb920-6fde-11e8-a574-7b39610424dd",
        "tenant" : "TENANT",
        "callbackUrl" : "http://callbackurl.com/lock",
        "createdBy" : "************",
        "event" : "item.lock",
        "createdDate" : "2018-06-14T14:23:23.570+0000",
        "system" : "adsk.flc.production",
        "creatorType" : "O2User",
        "status" : "active",
        "scope" : {
          "workspace" : "urn:adsk.plm:tenant.workspace:TENANT.721"
        },
        "urn" : "urn:adsk.webhooks:events.hook:7eceb920-6fde-11e8-a574-7b39610424dd",
        "__self__" : "/systems/adsk.flc.production/events/item.lock/hooks/7eceb920-6fde-11e8-a574-7b39610424dd"
      },
      "payload" : {
        "ItemUrn" : "urn:adsk.plm:tenant.workspace.item:TENANT.721.109597",
        "ItemDescription" : "NU000521"
      }
}


Documentation /Webhooks API /Reference Guide
item.release
Event:	
item.release
System:	
adsk.flc.production (Fusion Lifecycle)
Scope:	
workspace
Trigger:	
When a Fusion Lifecycle item is released
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/adsk.flc.production/events/item.release/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://callbackUrl.com/release",
            "scope": {
                "workspace" : "urn:adsk.plm:tenant.workspace:TENANT.721"
            }
        }'
Show Less
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
Example Body
{
      "version" : "1.0",
      "resourceUrn" : "urn:adsk.plm:tenant.workspace.item:TENANT.721.109597",
      "hook" : {
        "hookId" : "7eceb920-6fde-11e8-a574-7b39610424dd",
        "tenant" : "TENANT",
        "callbackUrl" : "http://callbackurl.com/release",
        "createdBy" : "************",
        "event" : "item.release",
        "createdDate" : "2018-06-14T14:23:23.570+0000",
        "system" : "adsk.flc.production",
        "creatorType" : "O2User",
        "status" : "active",
        "scope" : {
          "workspace" : "urn:adsk.plm:tenant.workspace:TENANT.721"
        },
        "urn" : "urn:adsk.webhooks:events.hook:7eceb920-6fde-11e8-a574-7b39610424dd",
        "__self__" : "/systems/adsk.flc.production/events/item.release/hooks/7eceb920-6fde-11e8-a574-7b39610424dd"
      },
      "payload" : {
        "ItemUrn" : "urn:adsk.plm:tenant.workspace.item:TENANT.721.109597",
        "ItemDescription" : "NU000521",
        "NewItemUrn" : "urn:adsk.plm:tenant.workspace.item:TENANT.722.109597",
        "NewItemDescription" : "NU00052-2"
      }
}



Documentation /Webhooks API /Reference Guide
item.unlock
Event:	
item.unlock
System:	
adsk.flc.production (Fusion Lifecycle)
Scope:	
workspace
Trigger:	
When an FLC item transitions from locked state to an unlocked state
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/adsk.flc.production/events/item.unlock/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://callbackUrl.com/unlock",
            "scope": {
                "workspace" : "urn:adsk.plm:tenant.workspace:TENANT.721"
            }
        }'
Show Less
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
Example Body
{
      "version" : "1.0",
      "resourceUrn" : "urn:adsk.plm:tenant.workspace.item:TENANT.721.109597",
      "hook" : {
        "hookId" : "7eceb920-6fde-11e8-a574-7b39610424dd",
        "tenant" : "TENANT",
        "callbackUrl" : "http://callbackurl.com/unlock",
        "createdBy" : "************",
        "event" : "item.unlock",
        "createdDate" : "2018-06-14T14:23:23.570+0000",
        "system" : "adsk.flc.production",
        "creatorType" : "O2User",
        "status" : "active",
        "scope" : {
          "workspace" : "urn:adsk.plm:tenant.workspace:TENANT.721"
        },
        "urn" : "urn:adsk.webhooks:events.hook:7eceb920-6fde-11e8-a574-7b39610424dd",
        "__self__" : "/systems/adsk.flc.production/events/item.unlock/hooks/7eceb920-6fde-11e8-a574-7b39610424dd"
      },
      "payload" : {
        "ItemUrn" : "urn:adsk.plm:tenant.workspace.item:TENANT.721.109597",
        "ItemDescription" : "NU000521"
      }
}

Documentation /Webhooks API /Reference Guide
item.update
Event:	
item.update
System:	
adsk.flc.production (Fusion Lifecycle)
Scope:	
workspace
Trigger:	
When the item details of a Fusion Lifecycle item are updated
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/adsk.flc.production/events/item.update/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://callbackUrl.com/update",
            "scope": {
                "workspace" : "urn:adsk.plm:tenant.workspace:TENANT.721"
            }
        }'
Show Less
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
Example Body
{
      "version" : "1.0",
      "resourceUrn" : "urn:adsk.plm:tenant.workspace.item:TENANT.721.109597",
      "hook" : {
        "hookId" : "7eceb920-6fde-11e8-a574-7b39610424dd",
        "tenant" : "TENANT",
        "callbackUrl" : "http://callbackurl.com/update",
        "createdBy" : "************",
        "event" : "item.update",
        "createdDate" : "2018-06-14T14:23:23.570+0000",
        "system" : "adsk.flc.production",
        "creatorType" : "O2User",
        "status" : "active",
        "scope" : {
          "workspace" : "urn:adsk.plm:tenant.workspace:TENANT.721"
        },
        "urn" : "urn:adsk.webhooks:events.hook:7eceb920-6fde-11e8-a574-7b39610424dd",
        "__self__" : "/systems/adsk.flc.production/events/item.update/hooks/7eceb920-6fde-11e8-a574-7b39610424dd"
      },
      "payload" : {
        "ItemUrn" : "urn:adsk.plm:tenant.workspace.item:TENANT.721.109597",
        "ItemDescription" : "NU000521"
      }
}

Documentation /Webhooks API /Reference Guide
workflow.transition
Event:	
workflow.transition
System:	
adsk.flc.production (Fusion Lifecycle)
Scope:	
workflow.transition
Trigger:	
When a specific transition is performed on a Fusion Lifecycle item
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/adsk.flc.production/events/workflow.transition/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://callbackUrl.com/transition",
            "scope": {
                "workflow.transition" : "urn:adsk.plm:tenant.workspace.workflow.transition:TENANT.721.1.12"
            }
        }'
Show Less
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
Example Body
{
  "version" : "1.0",
  "resourceUrn" : "urn:adsk.plm:tenant.workspace.item:TENANT.721.109597",
  "hook" : {
          "hookId" : "7eceb920-6fde-11e8-a574-7b39610424dd",
          "tenant" : "TENANT",
          "callbackUrl" : "http://callbackurl.com/transition",
          "createdBy" : "************",
          "event" : "workflow.transition",
          "createdDate" : "2018-06-14T14:23:23.570+0000",
          "system" : "adsk.flc.production",
          "creatorType" : "O2User",
          "status" : "active",
          "scope" : {
            "workflow.transition" : "urn:adsk.plm:tenant.workspace.workflow.transition:TENANT.721.1.12"
          },
          "urn" : "urn:adsk.webhooks:events.hook:7eceb920-6fde-11e8-a574-7b39610424dd",
          "__self__" : "/systems/adsk.flc.production/events/workflow.transition/hooks/7eceb920-6fde-11e8-a574-7b39610424dd"
        },
  "payload" : {
          "ItemUrn" : "urn:adsk.plm:tenant.workspace.item:TENANT.721.109597",
          "ItemDescription" : "NU000521"
        }
}

