Documentation /Webhooks API /Reference Guide
dm.version.added
Event:	
dm.version.added
System:	
data (Data Management)
Scope:	
folder
Trigger:	
When a new version of an item is added to a Folder.
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.version.added/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
            },
            "filter": "$[?(@.ext=='txt')]",
            "hookAttribute": {
                "myfoo": 34,
                "projectId": "someURN",
                "myobject": {
                  "nested": true
                }
            }
        }'
Show More
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
  "version": "1.0",
  "resourceUrn": "urn:adsk.wipprod:fs.file:vf.0zvdp3CoTzWDcZC_wL0kJA?version=1",
  "hook": {
    "system": "data",
    "event": "dm.version.added",
    "hookId": "1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "tenant": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g",
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
      "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
    },
    "urn": "urn:adsk.webhooks:events.hook:1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "status": "active",
    "__self__": "/systems/data/events/dm.version.added/hooks/1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce"
  },
  "payload": {
    "ext": "txt",
    "modifiedTime": "2017-09-06T03:08:53+0000",
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
    "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.chOa5mlkR6mjN-PEx8-r8Q",
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

Documentation /Webhooks API /Reference Guide
dm.version.modified
Event:	
dm.version.modified
System:	
data (Data Management)
Scope:	
folder
Trigger:	
When a version of an item is modified.
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.version.modified/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
            },
            "hookAttribute": {
                "myfoo": 34,
                "projectId": "someURN",
                "myobject": {
                  "nested": true
                }
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
  "version": "1.0",
  "resourceUrn": "urn:adsk.wipprod:fs.file:vf.0zvdp3CoTzWDdZC_wL0kJA?version=1",
  "hook": {
    "system": "data",
    "event": "dm.version.modified",
    "hookId": "1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "tenant": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "************",
    "createdDate": "2017-09-22T02:38:32.341+0000",
    "creatorType": "Application",
    "hookAttribute": {
      "myfoo": 34,
      "projectId": "someURN",
      "myobject": {
        "nested": true
      }
    },
    "scope": {
      "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
    },
    "urn": "urn:adsk.webhooks:events.hook:1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "status": "active",
    "__self__": "/systems/data/events/dm.version.modified/hooks/1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce"
  },
  "payload": {
    "ext": "txt",
    "modifiedTime": "2017-09-06T03:04:48+0000",
    "lineageUrn": "urn:adsk.wipprod:dm.lineage:53ZAFeM4SSu-WrRAdCO-LA",
    "sizeInBytes": 36,
    "hidden": false,
    "indexable": true,
    "project": "4f8b8b74-3853-473d-85c4-4e8a8bff885b",
    "source": "urn:adsk.wipprod:fs.file:vf.53ZAFeM4SSu-WrRAdCO-LA?version=1",
    "modification_flags": "{\"newVersion\":false,\"accessDefOrScopeChange\":false,\"metadataOnly\":true}",
    "version": "1",
    "contentURL": "urn:adsk.objects:os.object:wip.dm.qa/3bbfde79-aae5-47e5-a7d0-364d5471ab74.txt",
    "user_info": {
      "id": "*************"
    },
    "name": "0854da0c-4131-4080-bb5e-a7d764e7a24b.txt",
    "modifiedBy": "*************",
    "state": "CONTENT_AVAILABLE",
    "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.chOa5mlkR6mjN-PEx8-r8Q",
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

Documentation /Webhooks API /Reference Guide
dm.version.deleted
Event:	
dm.version.deleted
System:	
data (Data Management)
Scope:	
folder
Trigger:	
When a version of an item is deleted from a Folder.
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.version.deleted/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
            },
            "hookAttribute": {
                "myfoo": 34,
                "projectId": "someURN",
                "myobject": {
                  "nested": true
                }
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
  "version": "1.0",
  "resourceUrn": "urn:adsk.wipprod:fs.file:vf.0zvdp3CoTzWDcZD_wL0kJA?version=1",
  "hook": {
    "system": "data",
    "event": "dm.version.deleted",
    "hookId": "1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "tenant": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "************",
    "createdDate": "2017-09-22T02:38:32.341+0000",
    "creatorType": "Application",
    "hookAttribute": {
      "myfoo": 34,
      "projectId": "someURN",
      "myobject": {
        "nested": true
      }
    },
    "scope": {
      "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
    },
    "urn": "urn:adsk.webhooks:events.hook:1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "status": "active",
    "__self__": "/systems/data/events/dm.version.deleted/hooks/1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce"
  },
  "payload": {
    "ext": "txt",
    "lineageUrn": "urn:adsk.wipprod:dm.lineage:dpMNjxQGTyqYuSbgLh9k3Q",
    "sizeInBytes": 1866,
    "source": "urn:adsk.wipprod:fs.file:vf.dpMNjxQGTyqYuSbgLh9k3Q",
    "mimeType": "application/txt",
    "user_info": {
      "id": "X*********"
    },
    "name": "DELETE.TEST.TEST4.txt",
    "state": "CONTENT_AVAILABLE",
    "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.8LuL30zSQi-bkQOzQyVIMg",
    "ancestors": [
      {
        "name": "wipe29c69f6",
        "urn": "urn:adsk.wipprod:fs.folder:co.nZBVD7UhS2q9tdpfeEDA7g"
      },
      {
        "name": "webhooks test",
        "urn": "urn:adsk.wipprod:fs.folder:co.TR3nwAKhTSCCLtk64TNvCg"
      },
      {
        "name": "SomeTest",
        "urn": "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw"
      },
      {
        "name": "TEST4TEST",
        "urn": "urn:adsk.wipprod:fs.folder:co.38I_kW4GSv-iITC6lrxEVQ"
      },
      {
        "name": "TEST4FOLDER2",
        "urn": "urn:adsk.wipprod:fs.folder:co.8LuL30zSQi-bkQOzQyVIMg"
      }
    ],
    "project": "2628361",
    "tenant": "646284"
  }
}


Documentation /Webhooks API /Reference Guide
dm.version.moved
Event:	
dm.version.moved
System:	
data (Data Management)
Scope:	
folder
Trigger:	
When a version of an item is moved into this Folder from another Folder.
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.version.moved/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
            },
            "hookAttribute": {
                "myfoo": 34,
                "projectId": "someURN",
                "myobject": {
                  "nested": true
                }
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
  "version": "1.0",
  "resourceUrn": "urn:adsk.wipprod:fs.file:vf.0zvdp3CoTaWDcZC_wL0kJA?version=1",
  "hook": {
    "system": "data",
    "event": "dm.version.moved",
    "hookId": "1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "tenant": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "************",
    "createdDate": "2017-09-22T02:38:32.341+0000",
    "creatorType": "Application",
    "hookAttribute": {
      "myfoo": 34,
      "projectId": "someURN",
      "myobject": {
        "nested": true
      }
    },
    "scope": {
      "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
    },
    "urn": "urn:adsk.webhooks:events.hook:1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "status": "active",
    "__self__": "/systems/data/events/dm.version.moved/hooks/1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce"
  },
  "payload": {
    "ext": "txt",
    "modifiedTime": "2017-09-06T02:55:53+0000",
    "lineageUrn": "urn:adsk.wipprod:dm.lineage:CNgdQa47T6CC9jfKBPC5zg",
    "sizeInBytes": 36,
    "hidden": false,
    "indexable": true,
    "project": "4f8b8b74-3853-473d-85c4-4e8a8bff885b",
    "source": "urn:adsk.wipprod:fs.file:vf.CNgdQa47T6CC9jfKBPC5zg?version=1",
    "modification_flags": "{\"newVersion\":false,\"accessDefOrScopeChange\":true,\"metadataOnly\":true}",
    "version": "1",
    "target": "urn:adsk.wipprod:fs.file:vf.CNgdQa47T6CC9jfKBPC5zg?version=1",
    "contentURL": "urn:adsk.objects:os.object:wip.dm.qa/4c04beab-29f1-425b-9c26-9218cb442e18.txt",
    "user_info": {
      "id": "*************"
    },
    "name": "aa71eae9-5d9a-42e5-9658-101c1a5959e8.txt",
    "context": {
      "lineage": {
        "reserved": false,
        "reservedUserName": null,
        "reservedUserId": null,
        "reservedTime": null,
        "unreservedUserName": null,
        "unreservedUserId": null,
        "unreservedTime": null,
        "createUserId": "*************",
        "createTime": "2021-09-30T22:46:31+0000",
        "createUserName": "john.smith",
        "lastModifiedUserId": "*************",
        "lastModifiedTime": "2021-09-30T23:33:59+0000",
        "lastModifiedUserName": "john.smith"
      },
      "operation": "Move",
      "sourceParentFolderUrn": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
    },
    "modifiedBy": "*************",
    "state": "CONTENT_AVAILABLE",
    "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.chOa5mlkR6mjN-PEx8-r8Q",
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

Documentation /Webhooks API /Reference Guide
dm.version.moved.out
Event:	
dm.version.moved.out
System:	
data (Data Management)
Scope:	
folder
Trigger:	
When a version of an item is moved out of this Folder into another Folder.
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.version.moved.out/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
            },
            "hookAttribute": {
                "myfoo": 34,
                "projectId": "someURN",
                "myobject": {
                  "nested": true
                }
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
  "version": "1.0",
  "resourceUrn": "urn:adsk.wipprod:fs.file:vf.0zvdp3CoTaWDcZC_wL0kJA?version=1",
  "hook": {
    "system": "data",
    "event": "dm.version.moved.out",
    "hookId": "1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "tenant": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "************",
    "createdDate": "2017-09-22T02:38:32.341+0000",
    "creatorType": "Application",
    "hookAttribute": {
      "myfoo": 34,
      "projectId": "someURN",
      "myobject": {
        "nested": true
      }
    },
    "scope": {
      "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
    },
    "urn": "urn:adsk.webhooks:events.hook:1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "status": "active",
    "__self__": "/systems/data/events/dm.version.moved.out/hooks/1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce"
  },
  "payload": {
    "ext": "txt",
    "modifiedTime": "2017-09-06T02:55:53+0000",
    "lineageUrn": "urn:adsk.wipprod:dm.lineage:CNgdQa47T6CC9jfKBPC5zg",
    "sizeInBytes": 36,
    "hidden": false,
    "indexable": true,
    "project": "4f8b8b74-3853-473d-85c4-4e8a8bff885b",
    "source": "urn:adsk.wipprod:fs.file:vf.CNgdQa47T6CC9jfKBPC5zg?version=1",
    "modification_flags": "{\"newVersion\":false,\"accessDefOrScopeChange\":true,\"metadataOnly\":true}",
    "version": "1",
    "target": "urn:adsk.wipprod:fs.file:vf.CNgdQa47T6CC9jfKBPC5zg?version=1",
    "contentURL": "urn:adsk.objects:os.object:wip.dm.qa/4c04beab-29f1-425b-9c26-9218cb442e18.txt",
    "user_info": {
      "id": "*************"
    },
    "name": "aa71eae9-5d9a-42e5-9658-101c1a5959e8.txt",
    "context": {
      "lineage": {
        "reserved": false,
        "reservedUserName": null,
        "reservedUserId": null,
        "reservedTime": null,
        "unreservedUserName": null,
        "unreservedUserId": null,
        "unreservedTime": null,
        "createUserId": "*************",
        "createTime": "2021-09-30T22:46:31+0000",
        "createUserName": "john.smith",
        "lastModifiedUserId": "*************",
        "lastModifiedTime": "2021-09-30T23:33:59+0000",
        "lastModifiedUserName": "john.smith"
      },
      "operation": "Move",
      "sourceParentFolderUrn": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
    },
    "modifiedBy": "*************",
    "state": "CONTENT_AVAILABLE",
    "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.chOa5mlkR6mjN-PEx8-r8Q",
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

Documentation /Webhooks API /Reference Guide
dm.version.copied
Event:	
dm.version.copied
System:	
data (Data Management)
Scope:	
folder
Trigger:	
When a version of an item is copied to a Folder.
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.version.copied/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
            },
            "hookAttribute": {
                "myfoo": 34,
                "projectId": "someURN",
                "myobject": {
                  "nested": true
                }
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
  "version": "1.0",
  "resourceUrn": "urn:adsk.wipprod:fs.file:vf.0zvdp3CoTzWDcZC_wL0kJA?version=1",
  "hook": {
    "system": "data",
    "event": "dm.version.copied",
    "hookId": "1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "tenant": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "************",
    "createdDate": "2017-09-22T02:38:32.341+0000",
    "creatorType": "Application",
    "hookAttribute": {
      "myfoo": 34,
      "projectId": "someURN",
      "myobject": {
        "nested": true
      }
    },
    "scope": {
      "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
    },
    "urn": "urn:adsk.webhooks:events.hook:1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "status": "active",
    "__self__": "/systems/data/events/dm.version.copied/hooks/1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce"
  },
  "payload": {
    "ext": "txt",
    "modifiedTime": "2017-09-07T15:55:59+0000",
    "creator": "X*********",
    "lineageUrn": "urn:adsk.wipprod:dm.lineage:WwifVx5AQ_ueYuEWeyT5ew",
    "sizeInBytes": 1866,
    "hidden": false,
    "indexable": true,
    "source": "urn:adsk.wipprod:fs.file:vf.kYkVlfL6SE-So4KNcCWAGQ?version=1",
    "mimeType": "application/txt",
    "version": "1",
    "target": "urn:adsk.wipprod:fs.file:vf.WwifVx5AQ_ueYuEWeyT5ew?version=1",
    "user_info": {
      "id": "X*********"
    }
}

Documentation /Webhooks API /Reference Guide
dm.version.copied.out
Event:	
dm.version.copied.out
System:	
data (Data Management)
Scope:	
folder
Trigger:	
When a version of an item is out of this Folder into another Folder.
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.version.copied.out/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
            },
            "hookAttribute": {
                "myfoo": 34,
                "projectId": "someURN",
                "myobject": {
                  "nested": true
                }
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
  "version": "1.0",
  "resourceUrn": "urn:adsk.wipprod:fs.file:vf.0zvdp3CoTzWDcZC_wL0kJA?version=1",
  "hook": {
    "system": "data",
    "event": "dm.version.copied.out",
    "hookId": "1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "tenant": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "************",
    "createdDate": "2022-04-04T02:38:32.341+0000",
    "creatorType": "Application",
    "hookAttribute": {
      "myfoo": 34,
      "projectId": "someURN",
      "myobject": {
        "nested": true
      }
    },
    "scope": {
      "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
    },
    "urn": "urn:adsk.webhooks:events.hook:1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "status": "active",
    "__self__": "/systems/data/events/dm.version.copied.out/hooks/1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce"
  },
  "payload": {
    "ext": "txt",
    "modifiedTime": "2022-04-04T15:55:59+0000",
    "creator": "X*********",
    "lineageUrn": "urn:adsk.wipprod:dm.lineage:WwifVx5AQ_ueYuEWeyT5ew",
    "sizeInBytes": 1866,
    "hidden": false,
    "indexable": true,
    "source": "urn:adsk.wipprod:fs.file:vf.kYkVlfL6SE-So4KNcCWAGQ?version=1",
    "mimeType": "application/txt",
    "version": "1",
    "target": "urn:adsk.wipprod:fs.file:vf.WwifVx5AQ_ueYuEWeyT5ew?version=1",
    "user_info": {
      "id": "X*********"
    }
}

Documentation /Webhooks API /Reference Guide
dm.lineage.reserved
Event:	
dm.lineage.reserved
System:	
data (Data Management)
Scope:	
folder
Trigger:	
When a item and its versions are reserved so only one user can modify it.
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.lineage.reserved/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
            },
            "hookAttribute": {
                "myfoo": 34,
                "projectId": "someURN",
                "myobject": {
                  "nested": true
                }
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
  "version": "1.0",
  "resourceUrn": "urn:adsk.wipprod:fs.file:vf.0zvdp3CoTaWDcZC_wL0kJA?version=1",
  "hook": {
    "system": "data",
    "event": "dm.lineage.reserved",
    "hookId": "1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "tenant": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "************",
    "createdDate": "2017-09-22T02:38:32.341+0000",
    "creatorType": "Application",
    "hookAttribute": {
      "myfoo": 34,
      "projectId": "someURN",
      "myobject": {
        "nested": true
      }
    },
    "scope": {
      "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
    },
    "urn": "urn:adsk.webhooks:events.hook:1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "status": "active",
    "__self__": "/systems/data/events/dm.lineage.reserved/hooks/1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce"
  },
  "payload": {
    "ext": "txt",
    "modifiedTime": "2017-09-06T02:55:53+0000",
    "lineageUrn": "urn:adsk.wipprod:dm.lineage:CNgdQa47T6CC9jfKBPC5zg",
    "sizeInBytes": 36,
    "hidden": false,
    "indexable": true,
    "project": "4f8b8b74-3853-473d-85c4-4e8a8bff885b",
    "source": "urn:adsk.wipprod:fs.file:vf.CNgdQa47T6CC9jfKBPC5zg?version=1",
    "modification_flags": "{\"newVersion\":false,\"accessDefOrScopeChange\":true,\"metadataOnly\":true}",
    "version": "1",
    "target": "urn:adsk.wipprod:fs.file:vf.CNgdQa47T6CC9jfKBPC5zg?version=1",
    "contentURL": "urn:adsk.objects:os.object:wip.dm.qa/4c04beab-29f1-425b-9c26-9218cb442e18.txt",
    "user_info": {
      "id": "*************"
    },
    "name": "aa71eae9-5d9a-42e5-9658-101c1a5959e8.txt",
    "context": {
      "lineage": {
        "reserved": true,
        "reservedUserName": "john.smith",
        "reservedUserId": "*************",
        "reservedTime": "2021-09-30T21:53:28+0000",
        "unreservedUserName": null,
        "unreservedUserId": null,
        "unreservedTime": null,
        "createUserId": "*************",
        "createTime": "2021-09-22T22:15:27+0000",
        "createUserName": "john.smith",
        "lastModifiedUserId": "*************",
        "lastModifiedTime": "2021-09-22T22:15:27+0000",
        "lastModifiedUserName": "john.smith"
      },
      "operation": "ReserveLineage"
    },
    "modifiedBy": "*************",
    "state": "CONTENT_AVAILABLE",
    "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.chOa5mlkR6mjN-PEx8-r8Q",
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


Documentation /Webhooks API /Reference Guide
dm.lineage.unreserved
Event:	
dm.lineage.unreserved
System:	
data (Data Management)
Scope:	
folder
Trigger:	
When a reservation on an item and its versions is removed so anyone with appropriate permissions can modify it.
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.lineage.unreserved/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
            },
            "hookAttribute": {
                "myfoo": 34,
                "projectId": "someURN",
                "myobject": {
                  "nested": true
                }
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
  "version": "1.0",
  "resourceUrn": "urn:adsk.wipprod:fs.file:vf.0zvdp3CoTaWDcZC_wL0kJA?version=1",
  "hook": {
    "system": "data",
    "event": "dm.lineage.unreserved",
    "hookId": "1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "tenant": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "************",
    "createdDate": "2017-09-22T02:38:32.341+0000",
    "creatorType": "Application",
    "hookAttribute": {
      "myfoo": 34,
      "projectId": "someURN",
      "myobject": {
        "nested": true
      }
    },
    "scope": {
      "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
    },
    "urn": "urn:adsk.webhooks:events.hook:1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "status": "active",
    "__self__": "/systems/data/events/dm.lineage.unreserved/hooks/1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce"
  },
  "payload": {
    "ext": "txt",
    "modifiedTime": "2017-09-06T02:55:53+0000",
    "lineageUrn": "urn:adsk.wipprod:dm.lineage:CNgdQa47T6CC9jfKBPC5zg",
    "sizeInBytes": 36,
    "hidden": false,
    "indexable": true,
    "project": "4f8b8b74-3853-473d-85c4-4e8a8bff885b",
    "source": "urn:adsk.wipprod:fs.file:vf.CNgdQa47T6CC9jfKBPC5zg?version=1",
    "modification_flags": "{\"newVersion\":false,\"accessDefOrScopeChange\":true,\"metadataOnly\":true}",
    "version": "1",
    "target": "urn:adsk.wipprod:fs.file:vf.CNgdQa47T6CC9jfKBPC5zg?version=1",
    "contentURL": "urn:adsk.objects:os.object:wip.dm.qa/4c04beab-29f1-425b-9c26-9218cb442e18.txt",
    "user_info": {
      "id": "*************"
    },
    "name": "aa71eae9-5d9a-42e5-9658-101c1a5959e8.txt",
    "context": {
      "lineage": {
        "reserved": false,
        "reservedUserName": null,
        "reservedUserId": null,
        "reservedTime": null,
        "unreservedUserName": "john.smith",
        "unreservedUserId": "*************",
        "unreservedTime": "2021-09-30T22:12:40+0000",
        "createUserId": "*************",
        "createTime": "2021-09-22T22:15:27+0000",
        "createUserName": "john.smith",
        "lastModifiedUserId": "*************",
        "lastModifiedTime": "2021-09-22T22:15:27+0000",
        "lastModifiedUserName": "john.smith"
      },
      "operation": "UnReserveLineage"
    },
    "modifiedBy": "*************",
    "state": "CONTENT_AVAILABLE",
    "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.chOa5mlkR6mjN-PEx8-r8Q",
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

Documentation /Webhooks API /Reference Guide
dm.lineage.updated
Event:	
dm.lineage.updated
System:	
data (Data Management)
Scope:	
folder
Trigger:	
When a item is updated.
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.lineage.updated/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
            },
            "hookAttribute": {
                "myfoo": 34,
                "projectId": "someURN",
                "myobject": {
                  "nested": true
                }
            }
        }'
Show More
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
  "version": "1.0",
  "resourceUrn": "urn:adsk.wipprod:fs.file:vf.0zvdp3CoTaWDcZC_wL0kJA?version=1",
  "hook": {
    "system": "data",
    "event": "dm.lineage.updated",
    "hookId": "1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "tenant": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "************",
    "createdDate": "2017-09-22T02:38:32.341+0000",
    "creatorType": "Application",
    "hookAttribute": {
      "myfoo": 34,
      "projectId": "someURN",
      "myobject": {
        "nested": true
      }
    },
    "scope": {
      "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
    },
    "urn": "urn:adsk.webhooks:events.hook:1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "status": "active",
    "__self__": "/systems/data/events/dm.lineage.updated/hooks/1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce"
  },
  "payload": {
    "ext": "txt",
    "modifiedTime": "2017-09-06T02:55:53+0000",
    "lineageUrn": "urn:adsk.wipprod:dm.lineage:CNgdQa47T6CC9jfKBPC5zg",
    "sizeInBytes": 36,
    "hidden": false,
    "indexable": true,
    "project": "4f8b8b74-3853-473d-85c4-4e8a8bff885b",
    "source": "urn:adsk.wipprod:fs.file:vf.CNgdQa47T6CC9jfKBPC5zg?version=1",
    "modification_flags": "{\"newVersion\":false,\"accessDefOrScopeChange\":true,\"metadataOnly\":true}",
    "version": "1",
    "target": "urn:adsk.wipprod:fs.file:vf.CNgdQa47T6CC9jfKBPC5zg?version=1",
    "contentURL": "urn:adsk.objects:os.object:wip.dm.qa/4c04beab-29f1-425b-9c26-9218cb442e18.txt",
    "user_info": {
      "id": "*************"
    },
    "name": "aa71eae9-5d9a-42e5-9658-101c1a5959e8.txt",
    "context": {
      "lineage": {
        "reserved": true,
        "reservedUserName": "john.smith",
        "reservedUserId": "*************",
        "reservedTime": "2021-09-30T21:53:28+0000",
        "unreservedUserName": null,
        "unreservedUserId": null,
        "unreservedTime": null,
        "createUserId": "*************",
        "createTime": "2021-09-22T22:15:27+0000",
        "createUserName": "john.smith",
        "lastModifiedUserId": "*************",
        "lastModifiedTime": "2021-09-22T22:15:27+0000",
        "lastModifiedUserName": "john.smith"
      },
      "operation": "UpdateLineages"
    },
    "modifiedBy": "*************",
    "state": "CONTENT_AVAILABLE",
    "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.chOa5mlkR6mjN-PEx8-r8Q",
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

Documentation /Webhooks API /Reference Guide
dm.folder.added
Event:	
dm.folder.added
System:	
data (Data Management)
Scope:	
folder
Trigger:	
When a Folder is added to a Folder
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.folder.added/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
            },
            "hookAttribute": {
                "myfoo": 34,
                "projectId": "someURN",
                "myobject": {
                  "nested": true
                }
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
  "version": "1.0",
  "resourceUrn": "urn:adsk.wipprod:fs.folder:co.HGJKYimOQomuJU1E1tSmfg",
  "hook": {
    "system": "data",
    "event": "dm.folder.added",
    "hookId": "1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "tenant": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "************",
    "createdDate": "2017-09-22T02:38:32.341+0000",
    "creatorType": "Application",
    "hookAttribute": {
      "myfoo": 34,
      "projectId": "someURN",
      "myobject": {
        "nested": true
      }
    },
    "scope": {
      "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
    },
    "urn": "urn:adsk.webhooks:events.hook:1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "status": "active",
    "__self__": "/systems/data/events/dm.folder.added/hooks/1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce"
  },
  "payload": {
    "modifiedTime": "2017-09-06T02:51:12+0000",
    "creator": "*************",
    "hidden": false,
    "folderAggregatePath": "/tenant-646284/group-2628361/SomeTest/SubFolder/1d5b6c87-f5e9-49a8-8552-164f81ebb526",
    "indexable": false,
    "project": "2628361",
    "source": "urn:adsk.wipprod:fs.folder:co.HGJKYimOQomuJU1E1tSmfg",
    "user_info": {
      "id": "*************"
    },
    "name": "1d5b6c87-f5e9-49a8-8552-164f81ebb526",
    "createdTime": "2017-09-06T02:51:12+0000",
    "modifiedBy": "*************",
    "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.y_o08KU1R6SKX90sFL3GRw",
    "ancestors": [
      {
        "urn": "urn:adsk.wipprod:fs.folder:co.nZBVD7UhS2q9tdpfeEDA7g",
        "name": "wipe29c69f6"
      },
      {
        "urn": "urn:adsk.wipprod:fs.folder:co.TR3nwAKhTSCCLtk64TNvCg",
        "name": "webhooks test"
      },
      {
        "urn": "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw",
        "name": "SomeTest"
      },
      {
        "urn": "urn:adsk.wipprod:fs.folder:co.y_o08KU1R6SKX90sFL3GRw",
        "name": "SubFolder"
      }
    ],
    "tenant": "646284"
  }
}

Documentation /Webhooks API /Reference Guide
dm.folder.modified
Event:	
dm.folder.modified
System:	
data (Data Management)
Scope:	
folder
Trigger:	
When a Folder is modified.
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.folder.modified/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
            },
            "hookAttribute": {
                "myfoo": 34,
                "projectId": "someURN",
                "myobject": {
                  "nested": true
                }
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
  "version": "1.0",
  "resourceUrn": "urn:adsk.wipprod:fs.folder:co.XuYJk7guQt-Bvg5mbBzXYg",
  "hook": {
    "system": "data",
    "event": "dm.folder.modified",
    "hookId": "1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "tenant": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "************",
    "createdDate": "2017-09-22T02:38:32.341+0000",
    "creatorType": "Application",
    "hookAttribute": {
      "myfoo": 34,
      "projectId": "someURN",
      "myobject": {
        "nested": true
      }
    },
    "scope": {
      "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
    },
    "urn": "urn:adsk.webhooks:events.hook:1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "status": "active",
    "__self__": "/systems/data/events/dm.folder.modified/hooks/1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce"
  },
  "payload": {
    "modifiedTime": "2017-09-06T03:00:31+0000",
    "hidden": false,
    "folderAggregatePath": "/tenant-646284/group-2628361/SomeTest/new 75029ab8-894b-489b-89d1-d15badc158be",
    "indexable": false,
    "project": "2628361",
    "source": "urn:adsk.wipprod:fs.folder:co.XuYJk7guQt-Bvg5mbBzXYg",
    "modification_flags": "{\"newVersion\":false,\"accessDefOrScopeChange\":false,\"metadataOnly\":false}",
    "user_info": {
      "id": "*************"
    },
    "name": "new 75029ab8-894b-489b-89d1-d15badc158be",
    "modifiedBy": "*************",
    "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw",
    "ancestors": [
      {
        "urn": "urn:adsk.wipprod:fs.folder:co.nZBVD7UhS2q9tdpfeEDA7g",
        "name": "wipe29c69f6"
      },
      {
        "urn": "urn:adsk.wipprod:fs.folder:co.TR3nwAKhTSCCLtk64TNvCg",
        "name": "webhooks test"
      },
      {
        "urn": "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw",
        "name": "SomeTest"
      }
    ],
    "tenant": "646284"
  }
}

Documentation /Webhooks API /Reference Guide
dm.folder.deleted
Event:	
dm.folder.deleted
System:	
data (Data Management)
Scope:	
folder
Trigger:	
When a Folder is deleted.
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.folder.deleted/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
            },
            "hookAttribute": {
                "myfoo": 34,
                "projectId": "someURN",
                "myobject": {
                  "nested": true
                }
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
  "version": "1.0",
  "resourceUrn": "urn:adsk.wipprod:fs.folder:co.zoc-UxwjS6SyF8WPZ_zJ1Q",
  "hook": {
    "system": "data",
    "event": "dm.folder.deleted",
    "hookId": "1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "tenant": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "************",
    "createdDate": "2017-09-22T02:38:32.341+0000",
    "creatorType": "Application",
    "hookAttribute": {
      "myfoo": 34,
      "projectId": "someURN",
      "myobject": {
        "nested": true
      }
    },
    "scope": {
      "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
    },
    "urn": "urn:adsk.webhooks:events.hook:1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "status": "active",
    "__self__": "/systems/data/events/dm.folder.deleted/hooks/1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce"
  },
  "payload": {
    "user_info": {
      "id": "X*********"
    },
    "name": "Test3",
    "indexable": false,
    "branchName": "master",
    "source": "urn:adsk.wipprod:fs.folder:co.zoc-UxwjS6SyF8WPZ_zJ1Q",
    "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw",
    "ancestors": [
      {
        "name": "wipe29c69f6",
        "urn": "urn:adsk.wipprod:fs.folder:co.nZBVD7UhS2q9tdpfeEDA7g"
      },
      {
        "name": "webhooks test",
        "urn": "urn:adsk.wipprod:fs.folder:co.TR3nwAKhTSCCLtk64TNvCg"
      },
      {
        "name": "SomeTest",
        "urn": "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw"
      }
    ],
    "project": "2628361",
    "tenant": "646284"
  }
}

Documentation /Webhooks API /Reference Guide
dm.folder.purged
Event:	
dm.folder.purged
System:	
data (Data Management)
Scope:	
folder
Trigger:	
When a Folder is purged.
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.folder.purged/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
            },
            "hookAttribute": {
                "myfoo": 34,
                "projectId": "someURN",
                "myobject": {
                  "nested": true
                }
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
  "version": "1.0",
  "resourceUrn": "urn:adsk.wipprod:fs.folder:co.zoc-UxwjS6SyF8WPZ_zJ1Q",
  "hook": {
    "system": "data",
    "event": "dm.folder.purged",
    "hookId": "1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "tenant": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "************",
    "createdDate": "2017-09-22T02:38:32.341+0000",
    "creatorType": "Application",
    "hookAttribute": {
      "myfoo": 34,
      "projectId": "someURN",
      "myobject": {
        "nested": true
      }
    },
    "scope": {
      "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
    },
    "urn": "urn:adsk.webhooks:events.hook:1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "status": "active",
    "__self__": "/systems/data/events/dm.folder.purged/hooks/1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce"
  },
  "payload": {
    "user_info": {
      "id": "X*********"
    },
    "name": "Test3",
    "indexable": false,
    "branchName": "master",
    "source": "urn:adsk.wipprod:fs.folder:co.zoc-UxwjS6SyF8WPZ_zJ1Q",
    "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw",
    "ancestors": [
      {
        "name": "wipe29c69f6",
        "urn": "urn:adsk.wipprod:fs.folder:co.nZBVD7UhS2q9tdpfeEDA7g"
      },
      {
        "name": "webhooks test",
        "urn": "urn:adsk.wipprod:fs.folder:co.TR3nwAKhTSCCLtk64TNvCg"
      },
      {
        "name": "SomeTest",
        "urn": "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw"
      }
    ],
    "project": "2628361",
    "tenant": "646284"
  }
}

Documentation /Webhooks API /Reference Guide
dm.folder.moved
Event:	
dm.folder.moved
System:	
data (Data Management)
Scope:	
folder
Trigger:	
When a Folder is moved.
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.folder.moved/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
            },
            "hookAttribute": {
                "myfoo": 34,
                "projectId": "someURN",
                "myobject": {
                  "nested": true
                }
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
  "version": "1.0",
  "resourceUrn": "urn:adsk.wipprod:fs.folder:co.8LuL30zSQi-bkQOzQyVIMg",
  "hook": {
    "system": "data",
    "event": "dm.folder.moved",
    "hookId": "1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "tenant": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "************",
    "createdDate": "2017-09-22T02:38:32.341+0000",
    "creatorType": "Application",
    "hookAttribute": {
      "myfoo": 34,
      "projectId": "someURN",
      "myobject": {
        "nested": true
      }
    },
    "scope": {
      "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
    },
    "urn": "urn:adsk.webhooks:events.hook:1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "status": "active",
    "__self__": "/systems/data/events/dm.folder.moved/hooks/1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce"
  },
  "payload": {
    "modifiedTime": "2017-09-07T15:56:27+0000",
    "hidden": false,
    "folderAggregatePath": "/tenant-646284/group-2628361/SomeTest/TEST4TEST/TEST4FOLDER2",
    "indexable": false,
    "source": "urn:adsk.wipprod:fs.folder:co.8LuL30zSQi-bkQOzQyVIMg",
    "modification_flags": "{\"newVersion\":false,\"accessDefOrScopeChange\":true,\"metadataOnly\":true}",
    "target": "urn:adsk.wipprod:fs.folder:co.8LuL30zSQi-bkQOzQyVIMg",
    "jobId": "1skznhmQSai2fCwLjzKVbQ",
    "user_info": {
      "id": "X*********"
    },
    "name": "TEST4FOLDER2",
    "modifiedBy": "X*********",
    "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.38I_kW4GSv-iITC6lrxEVQ",
    "ancestors": [
      {
        "name": "wipe29c69f6",
        "urn": "urn:adsk.wipprod:fs.folder:co.nZBVD7UhS2q9tdpfeEDA7g"
      },
      {
        "name": "webhooks test",
        "urn": "urn:adsk.wipprod:fs.folder:co.TR3nwAKhTSCCLtk64TNvCg"
      },
      {
        "name": "SomeTest",
        "urn": "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw"
      },
      {
        "name": "TEST4TEST",
        "urn": "urn:adsk.wipprod:fs.folder:co.38I_kW4GSv-iITC6lrxEVQ"
      }
    ],
    "project": "2628361",
    "tenant": "646284"
  }
}

Documentation /Webhooks API /Reference Guide
dm.folder.moved.out
Event:	
dm.folder.moved.out
System:	
data (Data Management)
Scope:	
folder
Trigger:	
When a Folder is moved out of this Folder into another Folder.
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.folder.moved.out/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
            },
            "hookAttribute": {
                "myfoo": 34,
                "projectId": "someURN",
                "myobject": {
                  "nested": true
                }
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
  "version": "1.0",
  "resourceUrn": "urn:adsk.wipprod:fs.folder:co.8LuL30zSQi-bkQOzQyVIMg",
  "hook": {
    "system": "data",
    "event": "dm.folder.moved.out",
    "hookId": "1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "tenant": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "************",
    "createdDate": "2022-04-04T02:38:32.341+0000",
    "creatorType": "Application",
    "hookAttribute": {
      "myfoo": 34,
      "projectId": "someURN",
      "myobject": {
        "nested": true
      }
    },
    "scope": {
      "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
    },
    "urn": "urn:adsk.webhooks:events.hook:1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "status": "active",
    "__self__": "/systems/data/events/dm.folder.moved.out/hooks/1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce"
  },
  "payload": {
    "modifiedTime": "2022-04-04T15:56:27+0000",
    "hidden": false,
    "folderAggregatePath": "/tenant-646284/group-2628361/SomeTest/TEST4TEST/TEST4FOLDER2",
    "indexable": false,
    "source": "urn:adsk.wipprod:fs.folder:co.8LuL30zSQi-bkQOzQyVIMg",
    "modification_flags": "{\"newVersion\":false,\"accessDefOrScopeChange\":true,\"metadataOnly\":true}",
    "target": "urn:adsk.wipprod:fs.folder:co.8LuL30zSQi-bkQOzQyVIMg",
    "jobId": "1skznhmQSai2fCwLjzKVbQ",
    "user_info": {
      "id": "X*********"
    },
    "name": "TEST4FOLDER2",
    "modifiedBy": "X*********",
    "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.38I_kW4GSv-iITC6lrxEVQ",
    "ancestors": [
      {
        "name": "wipe29c69f6",
        "urn": "urn:adsk.wipprod:fs.folder:co.nZBVD7UhS2q9tdpfeEDA7g"
      },
      {
        "name": "webhooks test",
        "urn": "urn:adsk.wipprod:fs.folder:co.TR3nwAKhTSCCLtk64TNvCg"
      },
      {
        "name": "SomeTest",
        "urn": "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw"
      },
      {
        "name": "TEST4TEST",
        "urn": "urn:adsk.wipprod:fs.folder:co.38I_kW4GSv-iITC6lrxEVQ"
      }
    ],
    "project": "2628361",
    "tenant": "646284"
  }
}

Documentation /Webhooks API /Reference Guide
dm.folder.copied
Event:	
dm.folder.copied
System:	
data (Data Management)
Scope:	
folder
Trigger:	
When a Folder is copied.
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.folder.copied/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
            },
            "hookAttribute": {
                "myfoo": 34,
                "projectId": "someURN",
                "myobject": {
                  "nested": true
                }
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
  "version": "1.0",
  "resourceUrn": "urn:adsk.wipprod:fs.folder:co.3BV7RRciQgeI09aWS7uxlg",
  "hook": {
    "system": "data",
    "event": "dm.folder.copied",
    "hookId": "1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "tenant": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "************",
    "createdDate": "2017-09-22T02:38:32.341+0000",
    "creatorType": "Application",
    "hookAttribute": {
      "myfoo": 34,
      "projectId": "someURN",
      "myobject": {
        "nested": true
      }
    },
    "scope": {
      "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
    },
    "urn": "urn:adsk.webhooks:events.hook:1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "status": "active",
    "__self__": "/systems/data/events/dm.folder.copied/hooks/1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce"
  },
  "payload": {
    "modifiedTime": "2017-09-07T16:06:33+0000",
    "creator": "X*********",
    "hidden": false,
    "folderAggregatePath": "/tenant-646284/group-2628361/SomeTest/test1/test2",
    "indexable": false,
    "source": "urn:adsk.wipprod:fs.folder:co.3BV7RRciQgeI09aWS7uxlg",
    "target": "urn:adsk.wipprod:fs.folder:co.RF60BYY8RqqMzfkgQnyz4A",
    "jobId": "idJMu9N4TPa5lQbbKxgApA",
    "user_info": {
      "id": "X*********"
    },
    "name": "test2",
    "createdTime": "2017-09-07T16:06:33+0000",
    "modifiedBy": "X*********",
    "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.Wq0L1_fFTDKA7fZiUbLmbw",
    "ancestors": [
      {
        "name": "wipe29c69f6",
        "urn": "urn:adsk.wipprod:fs.folder:co.nZBVD7UhS2q9tdpfeEDA7g"
      },
      {
        "name": "webhooks test",
        "urn": "urn:adsk.wipprod:fs.folder:co.TR3nwAKhTSCCLtk64TNvCg"
      },
      {
        "name": "SomeTest",
        "urn": "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw"
      },
      {
        "name": "test1",
        "urn": "urn:adsk.wipprod:fs.folder:co.Wq0L1_fFTDKA7fZiUbLmbw"
      }
    ],
    "project": "2628361",
    "tenant": "646284"
  }
}


Documentation /Webhooks API /Reference Guide
dm.folder.copied.out
Event:	
dm.folder.copied.out
System:	
data (Data Management)
Scope:	
folder
Trigger:	
When a Folder is copied out of this Folder into another Folder.
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.folder.copied.out/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
            },
            "hookAttribute": {
                "myfoo": 34,
                "projectId": "someURN",
                "myobject": {
                  "nested": true
                }
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
  "version": "1.0",
  "resourceUrn": "urn:adsk.wipprod:fs.folder:co.3BV7RRciQgeI09aWS7uxlg",
  "hook": {
    "system": "data",
    "event": "dm.folder.copied.out",
    "hookId": "1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "tenant": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "************",
    "createdDate": "2022-04-04T02:38:32.341+0000",
    "creatorType": "Application",
    "hookAttribute": {
      "myfoo": 34,
      "projectId": "someURN",
      "myobject": {
        "nested": true
      }
    },
    "scope": {
      "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
    },
    "urn": "urn:adsk.webhooks:events.hook:1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "status": "active",
    "__self__": "/systems/data/events/dm.folder.copied.out/hooks/1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce"
  },
  "payload": {
    "modifiedTime": "2022-04-04T16:06:33+0000",
    "creator": "X*********",
    "hidden": false,
    "folderAggregatePath": "/tenant-646284/group-2628361/SomeTest/test1/test2",
    "indexable": false,
    "source": "urn:adsk.wipprod:fs.folder:co.3BV7RRciQgeI09aWS7uxlg",
    "target": "urn:adsk.wipprod:fs.folder:co.RF60BYY8RqqMzfkgQnyz4A",
    "jobId": "idJMu9N4TPa5lQbbKxgApA",
    "user_info": {
      "id": "X*********"
    },
    "name": "test2",
    "createdTime": "2022-04-04T16:06:33+0000",
    "modifiedBy": "X*********",
    "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.Wq0L1_fFTDKA7fZiUbLmbw",
    "ancestors": [
      {
        "name": "wipe29c69f6",
        "urn": "urn:adsk.wipprod:fs.folder:co.nZBVD7UhS2q9tdpfeEDA7g"
      },
      {
        "name": "webhooks test",
        "urn": "urn:adsk.wipprod:fs.folder:co.TR3nwAKhTSCCLtk64TNvCg"
      },
      {
        "name": "SomeTest",
        "urn": "urn:adsk.wipprod:fs.folder:co.wT5lCWlXSKeo3razOfHJAw"
      },
      {
        "name": "test1",
        "urn": "urn:adsk.wipprod:fs.folder:co.Wq0L1_fFTDKA7fZiUbLmbw"
      }
    ],
    "project": "2628361",
    "tenant": "646284"
  }
}

Documentation /Webhooks API /Reference Guide
dm.operation.started
Event:	
dm.operation.started
System:	
data (Data Management)
Scope:	
folder
Trigger:	
When a Data Management asynchronous operation starts
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.operation.started/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
            },
            "hookAttribute": {
                "myfoo": 34,
                "projectId": "someURN",
                "myobject": {
                  "nested": true
                }
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
Note: The tenant field in the body will only be available if WIP includes a scope including tenant in the event.

{
  "version": "1.0",
  "resourceUrn": "urn:adsk.wipprod:fs.folder:co.HGJKYimOQomuJU1E1tSmfg",
  "hook": {
    "system": "data",
    "event": "dm.operation.started",
    "hookId": "1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "tenant": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "************",
    "createdDate": "2017-09-22T02:38:32.341+0000",
    "creatorType": "Application",
    "hookAttribute": {
      "myfoo": 34,
      "projectId": "someURN",
      "myobject": {
        "nested": true
      }
    },
    "scope": {
      "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
    },
    "urn": "urn:adsk.webhooks:events.hook:1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "status": "active",
    "__self__": "/systems/data/events/dm.operation.started/hooks/1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce"
  },
  "payload": {
        "userInfo": {
            "id": "3WS7MJQPFJJB"
        },
        "progress": 0,
        "startTime": "2020-08-06T23:04:11+0000",
        "operationName": "DeleteFolderHandler",
        "state": "AVAILABLE",
        "message": "Delete a folder hierarchy asynchronously",
        "errors": [],
        "sourceResource": "urn:adsk.wipqa:fs.folder:co.Jryrw2XlTuOEuv4gAt0DIA",
        "eventContext": {
            "jobId": "K6cfWD2tRZ6zzAv2rF-mwg",
            "sourceAggregateUrnPath": "/urn:adsk.wipqa:fs.folder:co.woxoClweRCeMWn-HFbXGdQ/urn:adsk.wipqa:fs.folder:co.db0S9PIXS6-AbuCqwnD-4g",
            "sourceAggregatePath": "/RootFolder/subfolder1",
            "branchName": "master",
            "scopes": [
                "{\"sourceSystem\":\"adsk.wipqa\",\"type\":\"dmid\",\"id\":\"a360betawip1fqa:group:38256668\"}",
                "{\"sourceSystem\":\"adsk.wipqa\",\"type\":\"dmid\",\"id\":\"a360betawip1fqa:tenant:2315546\"}"
            ],
            "ancestors": [
                {
                    "title": "b662c88c-85e3-45c7-a9cc-6c77a31462a4",
                    "urn": "urn:adsk.wipqa:fs.folder:co.woxoClweRCeMWn-HFbXGdQ",
                    "dmid": ""
                },
                {
                    "title": "Valyria team QA-account-root-folder",
                    "urn": "urn:adsk.wipqa:fs.folder:co.C7_f4YaoTFGEJA6_81wiAA",
                    "dmid": "bim360qa:account:8cbdfbec-3f02-47c7-838d-8f2236d7040d"
                },
                {
                    "title": "04825481-5812-4fbb-9695-1e2e70f1d065-root-folder",
                    "urn": "urn:adsk.wipqa:fs.folder:co.Lf1SPmKYS5OK_CVplH_1VA",
                    "dmid": "bim360qa:project:04825481-5812-4fbb-9695-1e2e70f1d065"
                }
            ],
            "operation": "DeleteFolder",
            "sourceLastModifiedUserId": "3WS7MJQPFJJB"
        },
        "tenant": "2315546"
   }
}

Documentation /Webhooks API /Reference Guide
dm.operation.completed
Event:	
dm.operation.completed
System:	
data (Data Management)
Scope:	
folder
Trigger:	
When a Data Management asynchronous operation starts
Create a Webhook
Request
curl -X 'POST'\
     -v 'https://developer.api.autodesk.com/webhooks/v1/systems/data/events/dm.operation.completed/hooks'\
     -H 'Content-Type: application/json'\
     -H 'authorization: Bearer bNU4P0trbQKNSzxWksLPTzSbbmUz'\
     -d '{
            "callbackUrl": "http://bf067e05.ngrok.io/callback",
            "scope": {
                "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
            },
            "hookAttribute": {
                "myfoo": 34,
                "projectId": "someURN",
                "myobject": {
                  "nested": true
                }
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
Note: The tenant field in the body will only be available if WIP includes a scope including tenant in the event.

{
  "version": "1.0",
  "resourceUrn": "urn:adsk.wipprod:fs.folder:co.HGJKYimOQomuJU1E1tSmfg",
  "hook": {
    "system": "data",
    "event": "dm.operation.completed",
    "hookId": "1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "tenant": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g",
    "callbackUrl": "http://bf067e05.ngrok.io/callback",
    "createdBy": "************",
    "createdDate": "2017-09-22T02:38:32.341+0000",
    "creatorType": "Application",
    "hookAttribute": {
      "myfoo": 34,
      "projectId": "someURN",
      "myobject": {
        "nested": true
      }
    },
    "scope": {
      "folder": "urn:adsk.wipprod:fs.folder:co.s424tpjyS_yYBs5ozch94g"
    },
    "urn": "urn:adsk.webhooks:events.hook:1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce",
    "status": "active",
    "__self__": "/systems/data/events/dm.operation.completed/hooks/1fcd3e30-9f3f-11e7-951f-0fd5337ed5ce"
  },
  "payload": {
        "userInfo": {
            "id": "3WS7MJQPFJJB"
        },
        "progress": 100,
        "startTime": "2020-08-06T23:04:11+0000",
        "operationName": "DeleteFolderHandler",
        "state": "ENDED",
        "message": "Delete a folder hierarchy asynchronously",
        "errors": [],
        "sourceResource": "urn:adsk.wipqa:fs.folder:co.Jryrw2XlTuOEuv4gAt0DIA",
        "eventContext": {
            "jobId": "K6cfWD2tRZ6zzAv2rF-mwg",
            "sourceAggregateUrnPath": "/urn:adsk.wipqa:fs.folder:co.woxoClweRCeMWn-HFbXGdQ/urn:adsk.wipqa:fs.folder:co.db0S9PIXS6-AbuCqwnD-4g",
            "sourceAggregatePath": "/RootFolder/subfolder1",
            "branchName": "master",
            "scopes": [
                "{\"sourceSystem\":\"adsk.wipqa\",\"type\":\"dmid\",\"id\":\"a360betawip1fqa:group:38256668\"}",
                "{\"sourceSystem\":\"adsk.wipqa\",\"type\":\"dmid\",\"id\":\"a360betawip1fqa:tenant:2315546\"}"
            ],
            "ancestors": [
                {
                    "title": "b662c88c-85e3-45c7-a9cc-6c77a31462a4",
                    "urn": "urn:adsk.wipqa:fs.folder:co.woxoClweRCeMWn-HFbXGdQ",
                    "dmid": ""
                },
                {
                    "title": "Valyria team QA-account-root-folder",
                    "urn": "urn:adsk.wipqa:fs.folder:co.C7_f4YaoTFGEJA6_81wiAA",
                    "dmid": "bim360qa:account:8cbdfbec-3f02-47c7-838d-8f2236d7040d"
                },
                {
                    "title": "04825481-5812-4fbb-9695-1e2e70f1d065-root-folder",
                    "urn": "urn:adsk.wipqa:fs.folder:co.Lf1SPmKYS5OK_CVplH_1VA",
                    "dmid": "bim360qa:project:04825481-5812-4fbb-9695-1e2e70f1d065"
                }
            ],
            "operation": "DeleteFolder",
            "sourceLastModifiedUserId": "3WS7MJQPFJJB"
        },
        "tenant": "2315546"
   }
}
