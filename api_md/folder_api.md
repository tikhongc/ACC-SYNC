Documentation /Data Management API /Reference Guide
Folders
GET	projects/:project_id/folders/:folder_id
Returns the folder by ID for any folder within a given project. All folders or sub-folders within a project are associated with their own unique ID, including the root folder.

New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data/v1/projects/:project_id/folders/:folder_id
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
If-Modified-Since
string
If the resource has not been modified since, the response will be a 304 without any body; the Last-Modified response header will contain the date of last modification.
x-user-id
string
In a two-legged authentication context, the app has access to all users specified by the administrator in the SaaS integrations UI. By providing this header, the API call will be limited to act on behalf of only the user specified.
* Required
Request
URI Parameters
project_id
string
The unique identifier of a project.
For BIM 360 Docs, the project ID in the Data Management API corresponds to the project ID in the BIM 360 API. To convert a project ID in the BIM 360 API into a project ID in the Data Management API you need to add a “b." prefix. For example, a project ID of c8b0c73d-3ae9 translates to a project ID of b.c8b0c73d-3ae9.

folder_id
string
The unique identifier of a folder.
Response
HTTP Status Code Summary
200
OK
Successful retrieval of a specific folder.
304
Not Modified
The specified resource has not been modified since.
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers. The client SHOULD NOT repeat the request without modifications. The response body may give an indication of what is wrong with the request.
403
Forbidden
The request was successfully validated but permission is not granted or the application has not been white-listed. Do not try again unless you solve permissions first.
404
Not Found
The specified resource was not found.
Response
Body Structure (200)
 Expand all
jsonapi
object
The JSON API object.
links
object
Information on links to this resource.
data
object
The object containing information on the folder.
Example
Successful retrieval of a specific folder.

Request
curl -v 'https://developer.api.autodesk.com/data/v1/projects/:project_id/folders/:folder_id' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w"
    }
  },
  "data": {
    "type": "folders",
    "id": "urn:adsk.wipprod:dm.folder:hC6k4hndRWaeIVhIjvHu8w",
    "attributes": {
      "name": "Plans",
      "displayName": "Plans",
      "createTime": "2015-11-27T11:11:23.000Z",
      "createUserId": "BW9RM76WZBGL",
      "createUserName": "John Doe",
      "lastModifiedTime": "2015-11-27T11:11:27.000Z",
      "lastModifiedUserId": "BW9RM76WZBGL",
      "lastModifiedUserName": "John Doe",
      "lastModifiedTimeRollup": "2015-11-27T11:11:27.000Z",
      "objectCount": 4,
      "hidden": false,
      "extension": {
        "type": "folders:autodesk.bim360:Folder",
        "version": "1.0",
        "schema": {
          "href": "https://developer.api.autodesk.com/schema/v1/versions/folders%3Aautodesk.bim360%3AFolder-1.0"
        },
        "data": {
          "allowedTypes": [
            "folders",
            "items:autodesk.bim360:File",
            "items:autodesk.bim360:Document",
            "items:autodesk.bim360:TitleBlock"
          ],
          "visibleTypes": [
            "folders",
            "items:autodesk.bim360:Document"
          ],
          "namingStandardIds": []
        }
      }
    },
    "links": {
      "self": {
        "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w"
      },
      "webView": {
        "href": "https://docs.b360.autodesk.com/projects/c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w"
      }
    },
    "relationships": {
      "parent": {
        "links": {
          "related": {
            "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w/parent"
          }
        },
        "data": {
          "type": "folders",
          "id": "urn:adsk.wipprod:dm.folder:sdfedf8wefl"
        }
      },
      "refs": {
        "links": {
          "self": {
            "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w/relationships/refs"
          },
          "related": {
            "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w/refs"
          }
        }
      },
      "links": {
        "links": {
          "self": {
            "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w/relationships/links"
          }
        }
      },
      "contents": {
        "links": {
          "related": {
            "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w/contents"
          }
        }
      }
    }
  }
}

Documentation /Data Management API /Reference Guide
Folders
GET	projects/:project_id/folders/:folder_id/contents
Returns a collection of items and folders within a folder. Items represent word documents, fusion design files, drawings, spreadsheets, etc.

Notes:

The tip version for each item resource is included by default in the included array of the payload.
New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data/v1/projects/:project_id/folders/:folder_id/contents
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
string
The unique identifier of a project.
For BIM 360 Docs, the project ID in the Data Management API corresponds to the project ID in the BIM 360 API. To convert a project ID in the BIM 360 API into a project ID in the Data Management API you need to add a “b." prefix. For example, a project ID of c8b0c73d-3ae9 translates to a project ID of b.c8b0c73d-3ae9.

folder_id
string
The unique identifier of a folder.
Request
Query String Parameters
filter[type]
array: string
Filter by the type of the objects in the folder. Supported values include folders and items.
filter[id]
array: string
Filter by the id of the ref target.
filter[extension.type]
array: string
Filter by the extension type.
filter[lastModifiedTimeRollup]
array: string
Filter by the lastModifiedTimeRollup in attributes
Supported values are date-time string in the form YYYY-MM-DDTHH:MM:SS.000000Z or YYYY-MM-DDTHH:MM:SS based on RFC3339

page[number]
int
Specifies what page to return. Page numbers start at 0, so the first page is page 0.
page[limit]
int
Specifies the maximum number of elements to return in the page. The default value is 200. The min value is 1. The max value is 200.
includeHidden
boolean
true: response will also include items and folders that were deleted from BIM 360 Docs projects.
false (default): response will not include items and folders that were deleted from BIM 360 Docs projects.

To return only items and folders that were deleted from BIM 360 Docs projects, see the Filtering section.

Response
HTTP Status Code Summary
200
OK
Successful retrieval of the folder contents collection associated with a specific folder.
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers. The client SHOULD NOT repeat the request without modifications. The response body may give an indication of what is wrong with the request.
403
Forbidden
The request was successfully validated but permission is not granted or the application has not been white-listed. Do not try again unless you solve permissions first.
404
Not Found
The specified resource was not found.
Response
Body Structure (200)
 Expand all
jsonapi
object
The JSON API object.
links
object
Information on links to this resource.
data
array: object
The array of data objects.
included
array: object
The array of resources included within this resource.
Example
Successful retrieval of the folder contents collection associated with a specific folder.

Request
curl -v 'https://developer.api.autodesk.com/data/v1/projects/:project_id/folders/:folder_id/contents' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3Asdfedf8wefl/contents?page%5Bnumber%5D=3"
    },
    "first": {
      "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3Asdfedf8wefl/contents?page%5Bnumber%5D=0"
    },
    "prev": {
      "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3Asdfedf8wefl/contents?page%5Bnumber%5D=2"
    },
    "next": {
      "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3Asdfedf8wefl/contents?page%5Bnumber%5D=4"
    }
  },
  "data": [
    {
      "type": "folders",
      "id": "urn:adsk.wipprod:dm.folder:hC6k4hndRWaeIVhIjvHu8w",
      "attributes": {
        "name": "Plans",
        "displayName": "Plans",
        "createTime": "2015-11-27T11:11:23.000Z",
        "createUserId": "BW9RM76WZBGL",
        "createUserName": "John Doe",
        "lastModifiedTime": "2015-11-27T11:11:27.000Z",
        "lastModifiedTimeRollup": "2015-11-27T11:11:27.000Z",
        "lastModifiedUserId": "BW9RM76WZBGL",
        "lastModifiedUserName": "John Doe",
        "path": "/dm-test-root/f0cb4ba0-7722-0133-9814-0eeb7bad1e3b",
        "objectCount": 4,
        "hidden": false,
        "extension": {
          "type": "folders:autodesk.bim360:Folder",
          "version": "1.0",
          "schema": {
            "href": "/schema/v1/versions/folders%3Aautodesk.bim360%3AFolder-1.0"
          },
          "data": {
            "allowedTypes": [
              "folders",
              "items:autodesk.bim360:File",
              "items:autodesk.bim360:Document",
              "items:autodesk.bim360:TitleBlock"
            ],
            "visibleTypes": [
              "folders",
              "items:autodesk.bim360:Document"
            ],
            "namingStandardIds": []
          }
        }
      },
      "links": {
        "self": {
          "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w"
        }
      },
      "relationships": {
        "parent": {
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3Asdfedf8wefl"
            }
          },
          "data": {
            "type": "folders",
            "id": "urn:adsk.wipprod:dm.folder:sdfedf8wefl"
          }
        },
        "refs": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w/relationships/refs"
            },
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w/refs"
            }
          }
        },
        "links": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w/relationships/links"
            }
          }
        },
        "contents": {
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w/contents"
            }
          }
        }
      }
    },
    {
      "type": "items",
      "id": "urn:adsk.wipprod:dm.lineage:hC6k4hndRWaeIVhIjvHu8w",
      "attributes": {
        "displayName": "my file",
        "createTime": "2015-11-27T11:11:23.000Z",
        "createUserId": "BW9RM76WZBGL",
        "createUserName": "John Doe",
        "lastModifiedTime": "2015-11-27T11:11:27.000Z",
        "lastModifiedUserId": "BW9RM76WZBGL",
        "lastModifiedUserName": "John Doe",
        "lastModifiedTimeRollup": "2015-11-27T11:11:27.000Z",
        "hidden": false,
        "reserved": true,
        "reservedTime": "2015-11-27T11:11:25.000Z",
        "reservedUserId": "BW9RM76WZBGL",
        "reservedUserName": "John Doe",
        "extension": {
          "type": "items:autodesk.bim360:File",
          "version": "1.0",
          "schema": {
            "href": "/schema/v1/versions/items%3Aautodesk.bim360%3AFile-1.0"
          },
          "data": {}
        }
      },
      "links": {
        "self": {
          "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3AhC6k4hndRWaeIVhIjvHu8w"
        }
      },
      "relationships": {
        "tip": {
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3AhC6k4hndRWaeIVhIjvHu8w/tip"
            }
          },
          "data": {
            "type": "versions",
            "id": "urn:adsk.wipprod:fs.file:vf.d34fdsg3g?version=2"
          }
        },
        "versions": {
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3AhC6k4hndRWaeIVhIjvHu8w/versions"
            }
          }
        },
        "refs": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3AhC6k4hndRWaeIVhIjvHu8w/relationships/refs"
            },
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3AhC6k4hndRWaeIVhIjvHu8w/refs"
            }
          }
        },
        "links": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3AhC6k4hndRWaeIVhIjvHu8w/relationships/links"
            }
          }
        },
        "parent": {
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3Asdfedf8wefl"
            }
          },
          "data": {
            "type": "folders",
            "id": "urn:adsk.wipprod:dm.folder:sdfedf8wefl"
          }
        }
      }
    }
  ],
  "included": [
    {
      "type": "versions",
      "id": "urn:adsk.wipprod:fs.file:vf.d34fdsg3g?version=2",
      "attributes": {
        "name": "version-test.pdf",
        "displayName": "version-test.pdf",
        "createTime": "2016-04-01T11:09:03.000Z",
        "createUserId": "BW9RM76WZBGL",
        "createUserName": "John Doe",
        "lastModifiedTime": "2016-04-01T11:11:18.000Z",
        "lastModifiedUserId": "BW9RM76WZBGL",
        "lastModifiedUserName": "John Doe",
        "versionNumber": 2,
        "mimeType": "application/pdf",
        "extension": {
          "type": "versions:autodesk.bim360:File",
          "version": "1.0",
          "schema": {
            "href": "/schema/v1/versions/versions%3Aautodesk.bim360%3AFile-1.0"
          },
          "data": {
            "tempUrn": null,
            "properties": {},
            "storageUrn": "urn:adsk.objects:os.object:wip.dm.prod/3c8f6bbc-fe5c-4815-a92e-8b8635e7b1cb.pdf",
            "storageType": "OSS",
            "conformingStatus": "NONE"
          }
        }
      },
      "links": {
        "self": {
          "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D1"
        },
        "webView": {
          "href": "https://docs.b360.autodesk.com/projects/c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Afs.folder%3Aco.0J4paz_FQgWPX2QRsaBkiw/detail/viewer/items/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D1"
        }
      },
      "relationships": {
        "item": {
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3Ab909RzMKR4mhc3O7UBY_8g"
            }
          },
          "data": {
            "type": "items",
            "id": "urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g"
          }
        },
        "refs": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D1/relationships/refs"
            },
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D1/refs"
            }
          }
        },
        "links": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D1/relationships/links"
            }
          }
        },
        "storage": {
          "meta": {
            "link": {
              "href": "/oss/v2/buckets/wipbucket/objects/3c8f6bbc-fe5c-4815-a92e-8b8635e7b1cb.pdf?scopes=b360project.6f8813fe-31a7-4440-bc63-d8ca97c856b4,global,O2tenant.tenantId"
            }
          },
          "data": {
            "type": "objects",
            "id": "urn:adsk.objects:os.object:wip.dm.prod/3c8f6bbc-fe5c-4815-a92e-8b8635e7b1cb.pdf"
          }
        }
      }
    }
  ]
}

Documentation /Data Management API /Reference Guide
Folders
GET	projects/:project_id/folders/:folder_id/parent
Returns the parent folder (if it exists). In a project, subfolders and resource items are stored under a folder except the root folder which does not have a parent of its own.

New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data/v1/projects/:project_id/folders/:folder_id/parent
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
string
The unique identifier of a project.
For BIM 360 Docs, the project ID in the Data Management API corresponds to the project ID in the BIM 360 API. To convert a project ID in the BIM 360 API into a project ID in the Data Management API you need to add a “b." prefix. For example, a project ID of c8b0c73d-3ae9 translates to a project ID of b.c8b0c73d-3ae9.

folder_id
string
The unique identifier of a folder.
Response
HTTP Status Code Summary
200
OK
Successful retrieval of a specific folder.
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers. The client SHOULD NOT repeat the request without modifications. The response body may give an indication of what is wrong with the request.
403
Forbidden
The request was successfully validated but permission is not granted or the application has not been white-listed. Do not try again unless you solve permissions first.
404
Not Found
The specified resource was not found.
Response
Body Structure (200)
 Expand all
jsonapi
object
The JSON API object.
links
object
Information on links to this resource.
data
object
The object containing information on the folder.
Example
Successful retrieval of a specific folder.

Request
curl -v 'https://developer.api.autodesk.com/data/v1/projects/:project_id/folders/:folder_id/parent' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w"
    }
  },
  "data": {
    "type": "folders",
    "id": "urn:adsk.wipprod:dm.folder:hC6k4hndRWaeIVhIjvHu8w",
    "attributes": {
      "name": "Plans",
      "displayName": "Plans",
      "createTime": "2015-11-27T11:11:23.000Z",
      "createUserId": "BW9RM76WZBGL",
      "createUserName": "John Doe",
      "lastModifiedTime": "2015-11-27T11:11:27.000Z",
      "lastModifiedUserId": "BW9RM76WZBGL",
      "lastModifiedUserName": "John Doe",
      "lastModifiedTimeRollup": "2015-11-27T11:11:27.000Z",
      "objectCount": 4,
      "hidden": false,
      "extension": {
        "type": "folders:autodesk.bim360:Folder",
        "version": "1.0",
        "schema": {
          "href": "https://developer.api.autodesk.com/schema/v1/versions/folders%3Aautodesk.bim360%3AFolder-1.0"
        },
        "data": {
          "allowedTypes": [
            "folders",
            "items:autodesk.bim360:File",
            "items:autodesk.bim360:Document",
            "items:autodesk.bim360:TitleBlock"
          ],
          "visibleTypes": [
            "folders",
            "items:autodesk.bim360:Document"
          ],
          "namingStandardIds": []
        }
      }
    },
    "links": {
      "self": {
        "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w"
      },
      "webView": {
        "href": "https://docs.b360.autodesk.com/projects/c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w"
      }
    },
    "relationships": {
      "parent": {
        "links": {
          "related": {
            "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w/parent"
          }
        },
        "data": {
          "type": "folders",
          "id": "urn:adsk.wipprod:dm.folder:sdfedf8wefl"
        }
      },
      "refs": {
        "links": {
          "self": {
            "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w/relationships/refs"
          },
          "related": {
            "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w/refs"
          }
        }
      },
      "links": {
        "links": {
          "self": {
            "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w/relationships/links"
          }
        }
      },
      "contents": {
        "links": {
          "related": {
            "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w/contents"
          }
        }
      }
    }
  }
}

Documentation /Data Management API /Reference Guide
Folders
GET	projects/:project_id/folders/:folder_id/refs
Returns the resources (items, folders, and versions) that have a custom relationship with the given folder_id. Custom relationships can be established between a folder and other resources within the data domain service (folders, items, and versions).

Notes:

Each relationship is defined by the id of the object at the other end of the relationship, together with type, attributes, and relationships links.
Callers will typically use a filter parameter to restrict the response to the custom relationship types (filter[meta.refType]) they are interested in.
The response body will have an included array which contains the ref resources that are involved in the relationship, which is essentially the GET projects/:project_id/folders/:folder_id/relationships/refs endpoint.
New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data/v1/projects/:project_id/folders/:folder_id/refs
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
string
The unique identifier of a project.
For BIM 360 Docs, the project ID in the Data Management API corresponds to the project ID in the BIM 360 API. To convert a project ID in the BIM 360 API into a project ID in the Data Management API you need to add a “b." prefix. For example, a project ID of c8b0c73d-3ae9 translates to a project ID of b.c8b0c73d-3ae9.

folder_id
string
The unique identifier of a folder.
Request
Query String Parameters
filter[type]
array: string
Filter by the type of the ref target. Supported values include folders, items, and versions.
filter[id]
array: string
Filter by the id of the ref target.
filter[extension.type]
array: string
Filter by the extension type.
Response
HTTP Status Code Summary
200
OK
Successful retrieval of a resource collection.
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers. The client SHOULD NOT repeat the request without modifications. The response body may give an indication of what is wrong with the request.
403
Forbidden
The request was successfully validated but permission is not granted or the application has not been white-listed. Do not try again unless you solve permissions first.
404
Not Found
The specified resource was not found.
Response
Body Structure (200)
 Expand all
jsonapi
object
The JSON API object.
links
object
Information on links to this resource.
data
array: object
The array of data objects.
included
array: object
The array of resources included within this resource.
Example
Successful retrieval of a resource collection.

Request
curl -v 'https://developer.api.autodesk.com/data/v1/projects/:project_id/folders/:folder_id/refs' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn:adsk.wipprod:dm.folder:hC6k4hndRWaeIVhIjvHu8w/refs"
    }
  },
  "data": [
    {
      "type": "folders",
      "id": "urn:adsk.wipprod:dm.folder:hC6k4hndRWaeIVhIjvHu8w",
      "attributes": {
        "name": "Plans",
        "displayName": "Plans",
        "createTime": "2015-11-27T11:11:23.000Z",
        "createUserId": "BW9RM76WZBGL",
        "createUserName": "John Doe",
        "lastModifiedTime": "2015-11-27T11:11:27.000Z",
        "lastModifiedUserId": "BW9RM76WZBGL",
        "lastModifiedUserName": "John Doe",
        "objectCount": 4,
        "hidden": false,
        "extension": {
          "type": "folders:autodesk.bim360:Folder",
          "version": "1.0",
          "schema": {
            "href": "https://developer.api.autodesk.com/schema/v1/versions/folders%3Aautodesk.bim360%3AFolder-1.0"
          },
          "data": {
            "allowedTypes": [
              "folders",
              "items:autodesk.bim360:File",
              "items:autodesk.bim360:Document",
              "items:autodesk.bim360:TitleBlock"
            ],
            "visibleTypes": [
              "folders",
              "items:autodesk.bim360:Document"
            ],
            "namingStandardIds": []
          }
        }
      },
      "links": {
        "self": {
          "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w",
          "webView": {
            "href": "https://docs.b360.autodesk.com/projects/c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w"
          }
        }
      },
      "relationships": {
        "parent": {
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w/parent"
            }
          },
          "data": {
            "type": "folders",
            "id": "urn:adsk.wipprod:dm.folder:sdfedf8wefl"
          }
        },
        "refs": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w/relationships/refs"
            },
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w/refs"
            }
          }
        },
        "links": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w/relationships/links"
            }
          }
        },
        "contents": {
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w/contents"
            }
          }
        }
      }
    },
    {
      "type": "versions",
      "id": "urn:adsk.wipprod:fs.file:vf.b909RzMKR4mhc3O7UBY_8g?version=2",
      "attributes": {
        "name": "version-test.pdf",
        "displayName": "version-test.pdf",
        "createTime": "2016-04-01T11:12:35.000Z",
        "createUserId": "BW9RM76WZBGL",
        "createUserName": "John Doe",
        "lastModifiedTime": "2016-04-01T11:15:22.000Z",
        "lastModifiedUserId": "BW9RM76WZBGL",
        "lastModifiedUserName": "John Doe",
        "versionNumber": 2,
        "mimeType": "application/pdf",
        "extension": {
          "type": "versions:autodesk.bim360:File",
          "version": "1.0",
          "schema": {
            "href": "/schema/v1/versions/versions%3Aautodesk.bim360%3AFile-1.0"
          },
          "data": {
            "tempUrn": null,
            "properties": {},
            "storageUrn": "urn:adsk.objects:os.object:wip.dm.prod/9f8bdc3f-e29c-4ada-ab7b-bb8dfa821163.pdf",
            "storageType": "OSS",
            "conformingStatus": "NONE"
          }
        }
      },
      "links": {
        "self": {
          "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D2"
        },
        "webView": {
          "href": "https://docs.b360.autodesk.com/projects/c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Afs.folder%3Aco.0J4paz_FQgWPX2QRsaBkiw/detail/viewer/items/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D2"
        }
      },
      "relationships": {
        "item": {
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3Ab909RzMKR4mhc3O7UBY_8g"
            }
          },
          "data": {
            "type": "items",
            "id": "urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g"
          }
        },
        "refs": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D2/relationships/refs"
            },
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D2/refs"
            }
          }
        },
        "links": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D2/relationships/links"
            }
          }
        },
        "storage": {
          "meta": {
            "link": {
              "href": "/oss/v2/buckets/wipbucket/objects/9f8bdc3f-e29c-4ada-ab7b-bb8dfa821163.pdf?scopes=b360project.6f8813fe-31a7-4440-bc63-d8ca97c856b4,global,O2tenant.tenantId"
            }
          },
          "data": {
            "type": "objects",
            "id": "urn:adsk.objects:os.object:wip.dm.prod/9f8bdc3f-e29c-4ada-ab7b-bb8dfa821163.pdf"
          }
        }
      }
    },
    {
      "type": "versions",
      "id": "urn:adsk.wipprod:fs.file:vf.b909RzMKR4mhc3O7UBY_8g?version=1",
      "attributes": {
        "name": "version-test.pdf",
        "displayName": "version-test.pdf",
        "createTime": "2016-04-01T11:09:03.000Z",
        "createUserId": "BW9RM76WZBGL",
        "createUserName": "John Doe",
        "lastModifiedTime": "2016-04-01T11:11:18.000Z",
        "lastModifiedUserId": "BW9RM76WZBGL",
        "lastModifiedUserName": "John Doe",
        "versionNumber": 1,
        "mimeType": "application/pdf",
        "extension": {
          "type": "versions:autodesk.bim360:File",
          "version": "1.0",
          "schema": {
            "href": "/schema/v1/versions/versions%3Aautodesk.bim360%3AFile-1.0"
          },
          "data": {
            "tempUrn": null,
            "properties": {},
            "storageUrn": "urn:adsk.objects:os.object:wip.dm.prod/3c8f6bbc-fe5c-4815-a92e-8b8635e7b1cb.pdf",
            "storageType": "OSS",
            "conformingStatus": "NONE"
          }
        }
      },
      "links": {
        "self": {
          "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D1"
        },
        "webView": {
          "href": "https://docs.b360.autodesk.com/projects/c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Afs.folder%3Aco.0J4paz_FQgWPX2QRsaBkiw/detail/viewer/items/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D1"
        }
      },
      "relationships": {
        "item": {
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3Ab909RzMKR4mhc3O7UBY_8g"
            }
          },
          "data": {
            "type": "items",
            "id": "urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g"
          }
        },
        "refs": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D1/relationships/refs"
            },
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D1/refs"
            }
          }
        },
        "links": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D1/relationships/links"
            }
          }
        },
        "storage": {
          "meta": {
            "link": {
              "href": "/oss/v2/buckets/wipbucket/objects/3c8f6bbc-fe5c-4815-a92e-8b8635e7b1cb.pdf?scopes=b360project.6f8813fe-31a7-4440-bc63-d8ca97c856b4,global,O2tenant.tenantId"
            }
          },
          "data": {
            "type": "objects",
            "id": "urn:adsk.objects:os.object:wip.dm.prod/3c8f6bbc-fe5c-4815-a92e-8b8635e7b1cb.pdf"
          }
        }
      }
    },
    {
      "type": "items",
      "id": "urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g",
      "attributes": {
        "displayName": "version-test.pdf",
        "createTime": "2016-04-01T11:09:03.000Z",
        "createUserId": "BW9RM76WZBGL",
        "createUserName": "John Doe",
        "lastModifiedTime": "2016-04-01T11:11:18.000Z",
        "lastModifiedUserId": "BW9RM76WZBGL",
        "lastModifiedUserName": "John Doe",
        "hidden": false,
        "reserved": true,
        "reservedTime": "2016-04-01T11:10:08.000Z",
        "reservedUserId": "BW9RM76WZBGL",
        "reservedUserName": "John Doe",
        "extension": {
          "data": {},
          "version": "1.0",
          "type": "items:autodesk.bim360:File",
          "schema": {
            "href": "https://developer.api.autodesk.com/schema/v1/versions/items%3Aautodesk.bim360%3AFile-1.0"
          }
        }
      },
      "relationships": {
        "tip": {
          "data": {
            "type": "versions",
            "id": "urn:adsk.wipprod:fs.file:vf.b909RzMKR4mhc3O7UBY_8g?version=2"
          },
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3AhC6k4hndRWaeIVhIjvHu8w/tip"
            }
          }
        },
        "parent": {
          "data": {
            "type": "folders",
            "id": "urn:adsk.wipprod:dm.folder:sdfedf8wefl"
          },
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/parent"
            }
          }
        },
        "versions": {
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/versions"
            }
          }
        },
        "refs": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/relationships/refs"
            },
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/refs"
            }
          }
        },
        "links": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/relationships/links"
            }
          }
        }
      },
      "links": {
        "self": {
          "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g"
        },
        "webView": {
          "href": "https://docs.b360.autodesk.com/projects/c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Afs.folder%3Aco.0J4paz_FQgWPX2QRsaBkiw/detail/viewer/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g"
        }
      }
    }
  ]
}

Documentation /Data Management API /Reference Guide
Folders
GET	projects/:project_id/folders/:folder_id/relationships/links
Returns a collection of links for the given folder_id. Custom relationships can be established between a folder and other external resources residing outside the data domain service. A link’s href defines the target URI to access a resource.

New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data/v1/projects/:project_id/folders/:folder_id/relationships/links
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
string
The unique identifier of a project.
For BIM 360 Docs, the project ID in the Data Management API corresponds to the project ID in the BIM 360 API. To convert a project ID in the BIM 360 API into a project ID in the Data Management API you need to add a “b." prefix. For example, a project ID of c8b0c73d-3ae9 translates to a project ID of b.c8b0c73d-3ae9.

folder_id
string
The unique identifier of a folder.
Response
HTTP Status Code Summary
200
OK
Successful retrieval of the links collection associated with a specific resource.
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers. The client SHOULD NOT repeat the request without modifications. The response body may give an indication of what is wrong with the request.
403
Forbidden
The request was successfully validated but permission is not granted or the application has not been white-listed. Do not try again unless you solve permissions first.
404
Not Found
The specified resource was not found.
Response
Body Structure (200)
 Expand all
jsonapi
object
The JSON API object.
links
object
Information on links to this resource.
data
array: object
The array of link objects.
Example
Successful retrieval of the links collection associated with a specific resource.

Request
curl -v 'https://developer.api.autodesk.com/data/v1/projects/:project_id/folders/:folder_id/relationships/links' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "/data/v1/projects/{some_project_id}/folders/{some_folder_id}/relationships/links"
    }
  },
  "data": [
    {
      "type": "links",
      "id": "96af4f60-53b8-4efe-b890-1eaa9ea5cb08",
      "meta": {
        "link": {
          "href": "/oss/v2/buckets/wipbucket/objects/myfolder.zip"
        },
        "data": {
          "type": "objects",
          "id": "urn:adsk.objects:os.object:wipbucket/myfolder.zip"
        },
        "mimeType": "application/x-zip-compressed",
        "extension": {
          "type": "links:A360:DownloadArchiveFolder",
          "version": "1.0",
          "schema": {
            "href": "/schema/v1/versions/links%3AA360%3ADownloadArchiveFolder-1.0"
          },
          "data": {
            "createdTime": "2015-05-22T14:56:28.000Z"
          }
        }
      }
    },
    {
      "type": "links",
      "id": "cf755d5e-7876-41c2-a58e-2175f9b0cd4b",
      "meta": {
        "link": {
          "href": "/a360/v2/items/{a360folder_id}/create_archive"
        },
        "extension": {
          "type": "links:A360:CreateFolderArchive",
          "version": "1.0",
          "schema": {
            "href": "/schema/v1/versions/links%3AA360%3ACreateFolderArchive-1.0"
          }
        }
      }
    }
  ]
}

Documentation /Data Management API /Reference Guide
Folders
GET	projects/:project_id/folders/:folder_id/relationships/refs
Returns the custom relationships that are associated with the given folder_id. Custom relationships can be established between a folder and other resources within the data domain service (folders, items, and versions).

Notes:

Each relationship is defined by the id of the object at the other end of the relationship, together with type, specific reference meta including extension data.
Callers will typically use a filter parameter to restrict the response to the custom relationship types (filter[meta.refType]) they are interested in.
The response body will have an included array which contains the resources that are involved in the relationship, which is essentially the GET projects/:project_id/folders/:folder_id/refs endpoint.
New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data/v1/projects/:project_id/folders/:folder_id/relationships/refs
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
string
The unique identifier of a project.
For BIM 360 Docs, the project ID in the Data Management API corresponds to the project ID in the BIM 360 API. To convert a project ID in the BIM 360 API into a project ID in the Data Management API you need to add a “b." prefix. For example, a project ID of c8b0c73d-3ae9 translates to a project ID of b.c8b0c73d-3ae9.

folder_id
string
The unique identifier of a folder.
Request
Query String Parameters
filter[type]
array: string
Filter by the type of the ref target. Supported values include folders, items, and versions.
filter[id]
array: string
Filter by the id of the ref target.
filter[refType]
enum:string
Filter by refType. Possible values: derived, dependencies, auxiliary, xrefs, includes
filter[direction]
enum:string
Filter by the direction of the reference. Possible values: from, to
filter[extension.type]
array: string
Filter by the extension type.
Response
HTTP Status Code Summary
200
OK
Successful retrieval of the refs collection associated with a specific resource.
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers. The client SHOULD NOT repeat the request without modifications. The response body may give an indication of what is wrong with the request.
403
Forbidden
The request was successfully validated but permission is not granted or the application has not been white-listed. Do not try again unless you solve permissions first.
404
Not Found
The specified resource was not found.
Response
Body Structure (200)
 Expand all
jsonapi
object
The JSON API object.
links
object
Information on links to this resource.
data
array: object
The array of ref objects.
included
array: object
The array of resources included within this resource.
Example
Successful retrieval of the refs collection associated with a specific resource.

Request
curl -v 'https://developer.api.autodesk.com/data/v1/projects/:project_id/folders/:folder_id/relationships/refs' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn:adsk.wipprod:dm.folder:hC6k4hndRWaeIVhIjvHu8w/relationships/refs"
    },
    "related": {
      "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn:adsk.wipprod:dm.folder:hC6k4hndRWaeIVhIjvHu8w/refs"
    }
  },
  "data": [
    {
      "type": "folders",
      "id": "urn:adsk.wipprod:dm.folder:hC6k4hndRWaeIVhIjvHu8w",
      "meta": {
        "refType": "xrefs",
        "fromId": "urn:adsk.wipprod:dm.folder:hC6k4hndRWaeIVhIjvHu8w",
        "fromType": "folders",
        "toId": "urn:adsk.wipprod:fs.file:vf.b909RzMKR4mhc3O7UBY_8g?version=2",
        "toType": "versions",
        "direction": "from",
        "extension": {
          "type": "xrefs:my.custom:Xref",
          "version": "1.0",
          "schema": {
            "href": "/schema/v1/versions/xrefs:my.custom:Xref-1.0"
          },
          "data": {}
        }
      }
    }
  ],
  "included": [
    {
      "type": "folders",
      "id": "urn:adsk.wipprod:dm.folder:hC6k4hndRWaeIVhIjvHu8w",
      "attributes": {
        "name": "Plans",
        "displayName": "Plans",
        "createTime": "2015-11-27T11:11:23.000Z",
        "createUserId": "BW9RM76WZBGL",
        "createUserName": "John Doe",
        "lastModifiedTime": "2015-11-27T11:11:27.000Z",
        "lastModifiedUserId": "BW9RM76WZBGL",
        "lastModifiedUserName": "John Doe",
        "objectCount": 4,
        "hidden": false,
        "extension": {
          "type": "folders:autodesk.bim360:Folder",
          "version": "1.0",
          "schema": {
            "href": "https://developer.api.autodesk.com/schema/v1/versions/folders%3Aautodesk.bim360%3AFolder-1.0"
          },
          "data": {
            "allowedTypes": [
              "folders",
              "items:autodesk.bim360:File",
              "items:autodesk.bim360:Document",
              "items:autodesk.bim360:TitleBlock"
            ],
            "visibleTypes": [
              "folders",
              "items:autodesk.bim360:Document"
            ],
            "namingStandardIds": []
          }
        }
      },
      "links": {
        "self": {
          "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w"
        }
      },
      "relationships": {
        "parent": {
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w/parent"
            }
          },
          "data": {
            "type": "folders",
            "id": "urn:adsk.wipprod:dm.folder:sdfedf8wefl"
          }
        },
        "refs": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w/relationships/refs"
            },
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w/refs"
            }
          }
        },
        "links": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w/relationships/links"
            }
          }
        },
        "contents": {
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w/contents"
            }
          }
        }
      }
    },
    {
      "type": "versions",
      "id": "urn:adsk.wipprod:fs.file:vf.b909RzMKR4mhc3O7UBY_8g?version=2",
      "attributes": {
        "name": "version-test.pdf",
        "displayName": "version-test.pdf",
        "createTime": "2016-04-01T11:12:35.000Z",
        "createUserId": "BW9RM76WZBGL",
        "createUserName": "John Doe",
        "lastModifiedTime": "2016-04-01T11:15:22.000Z",
        "lastModifiedUserId": "BW9RM76WZBGL",
        "lastModifiedUserName": "John Doe",
        "versionNumber": 2,
        "mimeType": "application/pdf",
        "extension": {
          "type": "versions:autodesk.bim360:File",
          "version": "1.0",
          "schema": {
            "href": "/schema/v1/versions/versions%3Aautodesk.bim360%3AFile-1.0"
          },
          "data": {
            "tempUrn": null,
            "properties": {},
            "storageUrn": "urn:adsk.objects:os.object:wip.dm.prod/9f8bdc3f-e29c-4ada-ab7b-bb8dfa821163.pdf",
            "storageType": "OSS",
            "conformingStatus": "NONE"
          }
        }
      },
      "links": {
        "self": {
          "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D2"
        }
      },
      "relationships": {
        "item": {
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3Ab909RzMKR4mhc3O7UBY_8g"
            }
          },
          "data": {
            "type": "items",
            "id": "urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g"
          }
        },
        "refs": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D2/relationships/refs"
            },
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D2/refs"
            }
          }
        },
        "links": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D2/relationships/links"
            }
          }
        },
        "storage": {
          "meta": {
            "link": {
              "href": "/oss/v2/buckets/wipbucket/objects/9f8bdc3f-e29c-4ada-ab7b-bb8dfa821163.pdf?scopes=b360project.6f8813fe-31a7-4440-bc63-d8ca97c856b4,global,O2tenant.tenantId"
            }
          },
          "data": {
            "type": "objects",
            "id": "urn:adsk.objects:os.object:wip.dm.prod/9f8bdc3f-e29c-4ada-ab7b-bb8dfa821163.pdf"
          }
        }
      }
    },
    {
      "type": "versions",
      "id": "urn:adsk.wipprod:fs.file:vf.b909RzMKR4mhc3O7UBY_8g?version=1",
      "attributes": {
        "name": "version-test.pdf",
        "displayName": "version-test.pdf",
        "createTime": "2016-04-01T11:09:03.000Z",
        "createUserId": "BW9RM76WZBGL",
        "createUserName": "John Doe",
        "lastModifiedTime": "2016-04-01T11:11:18.000Z",
        "lastModifiedUserId": "BW9RM76WZBGL",
        "lastModifiedUserName": "John Doe",
        "versionNumber": 1,
        "mimeType": "application/pdf",
        "extension": {
          "type": "versions:autodesk.bim360:File",
          "version": "1.0",
          "schema": {
            "href": "/schema/v1/versions/versions%3Aautodesk.bim360%3AFile-1.0"
          },
          "data": {
            "tempUrn": null,
            "properties": {},
            "storageUrn": "urn:adsk.objects:os.object:wip.dm.prod/3c8f6bbc-fe5c-4815-a92e-8b8635e7b1cb.pdf",
            "storageType": "OSS",
            "conformingStatus": "NONE"
          }
        }
      },
      "links": {
        "self": {
          "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D1"
        }
      },
      "relationships": {
        "item": {
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3Ab909RzMKR4mhc3O7UBY_8g"
            }
          },
          "data": {
            "type": "items",
            "id": "urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g"
          }
        },
        "refs": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D1/relationships/refs"
            },
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D1/refs"
            }
          }
        },
        "links": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D1/relationships/links"
            }
          }
        },
        "storage": {
          "meta": {
            "link": {
              "href": "/oss/v2/buckets/wipbucket/objects/3c8f6bbc-fe5c-4815-a92e-8b8635e7b1cb.pdf?scopes=b360project.6f8813fe-31a7-4440-bc63-d8ca97c856b4,global,O2tenant.tenantId"
            }
          },
          "data": {
            "type": "objects",
            "id": "urn:adsk.objects:os.object:wip.dm.prod/3c8f6bbc-fe5c-4815-a92e-8b8635e7b1cb.pdf"
          }
        }
      }
    },
    {
      "type": "items",
      "id": "urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g",
      "attributes": {
        "displayName": "version-test.pdf",
        "createTime": "2016-04-01T11:09:03.000Z",
        "createUserId": "BW9RM76WZBGL",
        "createUserName": "John Doe",
        "lastModifiedTime": "2016-04-01T11:11:18.000Z",
        "lastModifiedUserId": "BW9RM76WZBGL",
        "lastModifiedUserName": "John Doe",
        "hidden": false,
        "reserved": true,
        "reservedTime": "2016-04-01T11:10:08.000Z",
        "reservedUserId": "BW9RM76WZBGL",
        "reservedUserName": "John Doe",
        "extension": {
          "data": {},
          "version": "1.0",
          "type": "items:autodesk.bim360:File",
          "schema": {
            "href": "https://developer.api.autodesk.com/schema/v1/versions/items%3Aautodesk.bim360%3AFile-1.0"
          }
        }
      },
      "relationships": {
        "tip": {
          "data": {
            "type": "versions",
            "id": "urn:adsk.wipprod:fs.file:vf.b909RzMKR4mhc3O7UBY_8g?version=2"
          },
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3AhC6k4hndRWaeIVhIjvHu8w/tip"
            }
          }
        },
        "parent": {
          "data": {
            "type": "folders",
            "id": "urn:adsk.wipprod:dm.folder:sdfedf8wefl"
          },
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/parent"
            }
          }
        },
        "versions": {
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/versions"
            }
          }
        },
        "refs": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/relationships/refs"
            },
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/refs"
            }
          }
        },
        "links": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/relationships/links"
            }
          }
        }
      },
      "links": {
        "self": {
          "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g"
        }
      }
    }
  ]
}

Documentation /Data Management API /Reference Guide
Folders
GET	projects/:project_id/folders/:folder_id/search
Filters the data of a folder and recursively in the subfolders of any project accessible to you, using the filter query string parameter. You can filter the following properties from the version payload: the type property, the id property, and any of the attributes object properties. For example, you can filter createTime, mimeType. It returns tip versions (latest versions) of properties where the filter conditions are satisfied. To verify the properties of the attributes object for a specific version, see the GET projects/:project_id/versions/:version_id.

To filter a folder's data without recursively filtering its subfolders, see the GET projects/:project_id/folders/:folder_id/contents endpoint.

New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data/v1/projects/:project_id/folders/:folder_id/search
Authentication Context	
user context optional
Required OAuth Scopes	
data:search data:read
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
string
The unique identifier of a project.
For BIM 360 Docs, the project ID in the Data Management API corresponds to the project ID in the BIM 360 API. To convert a project ID in the BIM 360 API into a project ID in the Data Management API you need to add a “b." prefix. For example, a project ID of c8b0c73d-3ae9 translates to a project ID of b.c8b0c73d-3ae9.

folder_id
string
The unique identifier of a folder.
Request
Query String Parameters
filter[*]
array: string
Filter the data. See the Filtering section for details.
page[number]
int
Specifies what page to return. Page numbers start at 0, so the first page is page 0. The minimum value to specify is 0 and the maximum is 49. For fewer results to page through, consider searching an inner folder.
Response
HTTP Status Code Summary
200
OK
Successful retrieval of the search results.
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers. The client SHOULD NOT repeat the request without modifications. The response body may give an indication of what is wrong with the request.
403
Forbidden
The request was successfully validated but permission is not granted or the application has not been white-listed. Do not try again unless you solve permissions first.
404
Not Found
The specified resource was not found.
Response
Body Structure (200)
 Expand all
jsonapi
object
The JSON API object.
links
object
The object containing information on links to this resource.
data
array: object
The object containing information on this resource.
included
array: object
Information on the latest versions of the items in this resource.
meta
object
The object containing metadata about the search results.
Example
Successful retrieval of the search results.

Request
curl -v 'https://developer.api.autodesk.com/data/v1/projects/:project_id/folders/:folder_id/search' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "data": [
    {
      "type": "versions",
      "id": "urn:adsk.wipprod:fs.file:vf.4cW918j8QsynzG0oZ6_Nbg?version=1",
      "attributes": {
        "name": "sample.txt",
        "displayName": "sample.txt",
        "createTime": "2016-11-09T13:11:27+00:00",
        "createUserId": "BW9RM76WZBGL",
        "createUserName": "John Doe",
        "lastModifiedTime": "2016-11-09T13:11:36+00:00",
        "lastModifiedUserId": "BW9RM76WZBGL",
        "lastModifiedUserName": "John Doe",
        "versionNumber": 1,
        "fileType": "txt",
        "extension": {
          "type": "versions:autodesk.bim360:File",
          "version": "1.0",
          "schema": {
            "href": "/schema/v1/versions/versions%3Aautodesk.bim360%3AFile-1.0"
          },
          "data": {
            "processState": "PROCESSING_COMPLETE",
            "extractionState": "UNSUPPORTED",
            "splittingState": "NOT_SPLIT",
            "conformingStatus": "NONE"
          }
        }
      },
      "links": {
        "self": {
          "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.4cW918j8QsynzG0oZ6_Nbg%3Fversion%3D1"
        },
        "webView": {
          "href": "https://docs.b360.autodesk.com/projects/c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Afs.folder%3Aco.0J4paz_FQgWPX2QRsaBkiw/detail/viewer/items/urn%3Aadsk.wipprod%3Afs.file%3Avf.4cW918j8QsynzG0oZ6_Nbg%3Fversion%3D1"
        }
      },
      "relationships": {
        "item": {
          "data": {
            "type": "items",
            "id": "urn:adsk.wipprod:dm.lineage:4cW918j8QsynzG0oZ6_Nbg"
          },
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.4cW918j8QsynzG0oZ6_Nbg%3Fversion%3D1/item"
            }
          }
        },
        "links": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.4cW918j8QsynzG0oZ6_Nbg%3Fversion%3D1/relationships/links"
            }
          }
        },
        "refs": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.4cW918j8QsynzG0oZ6_Nbg%3Fversion%3D1/relationships/refs"
            },
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.4cW918j8QsynzG0oZ6_Nbg%3Fversion%3D1/refs"
            }
          }
        },
        "downloadFormats": {
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.4cW918j8QsynzG0oZ6_Nbg%3Fversion%3D1/downloadFormats"
            }
          }
        },
        "derivatives": {
          "data": {
            "type": "derivatives",
            "id": "dXJuOmFkc2sud2lwc3RnOmZzLmZpbGU6dmYuNGNXOTE4ajhRc3luekcwb1o2X05iZz92ZXJzaW9uPTE"
          },
          "meta": {
            "link": {
              "href": "/modelderivative/v2/designdata/dXJuOmFkc2sud2lwc3RnOmZzLmZpbGU6dmYuNGNXOTE4ajhRc3luekcwb1o2X05iZz92ZXJzaW9uPTE/manifest?scopes=b360project.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d,global,O2tenant.tenantId"
            }
          }
        },
        "thumbnails": {
          "data": {
            "type": "thumbnails",
            "id": "dXJuOmFkc2sud2lwc3RnOmZzLmZpbGU6dmYuNGNXOTE4ajhRc3luekcwb1o2X05iZz92ZXJzaW9uPTE"
          },
          "meta": {
            "link": {
              "href": "/modelderivative/v2/designdata/dXJuOmFkc2sud2lwc3RnOmZzLmZpbGU6dmYuNGNXOTE4ajhRc3luekcwb1o2X05iZz92ZXJzaW9uPTE/thumbnail?scopes=b360project.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d,global,O2tenant.tenantId"
            }
          }
        },
        "storage": {
          "data": {
            "type": "objects",
            "id": "urn:adsk.objects:os.object:wip.dm.prod/095f7c56-2373-4831-9485-e3546dd501ba.txt"
          },
          "meta": {
            "link": {
              "href": "/oss/v2/buckets/wip.dm.prod/objects/095f7c56-2373-4831-9485-e3546dd501ba.txt?scopes=b360project.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d,global,O2tenant.tenantId"
            }
          }
        }
      }
    },
    {
      "type": "versions",
      "id": "urn:adsk.wipprod:fs.file:vf.jts1sOfCS6mdwCV38lKpGQ?version=1",
      "attributes": {
        "name": "sample.pdf",
        "displayName": "sample.pdf",
        "createTime": "2016-11-09T13:13:09+00:00",
        "createUserId": "BW9RM76WZBGL",
        "createUserName": "John Doe",
        "lastModifiedTime": "2016-11-09T13:13:42+00:00",
        "lastModifiedUserId": "BW9RM76WZBGL",
        "lastModifiedUserName": "John Doe",
        "versionNumber": 1,
        "fileType": "pdf",
        "extension": {
          "type": "versions:autodesk.bim360:File",
          "version": "1.0",
          "schema": {
            "href": "/schema/v1/versions/versions%3Aautodesk.bim360%3AFile-1.0"
          },
          "data": {
            "processState": "PROCESSING_COMPLETE",
            "extractionState": "SUCCESS",
            "splittingState": "NOT_SPLIT",
            "reviewState": "NOT_IN_REVIEW",
            "conformingStatus": "NONE"
          }
        }
      },
      "links": {
        "self": {
          "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.jts1sOfCS6mdwCV38lKpGQ%3Fversion%3D1"
        },
        "webView": {
          "href": "https://docs.b360.autodesk.com/projects/c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Afs.folder%3Aco.0J4paz_FQgWPX2QRsaBkiw/detail/viewer/items/urn%3Aadsk.wipprod%3Afs.file%3Avf.jts1sOfCS6mdwCV38lKpGQ%3Fversion%3D1"
        }
      },
      "relationships": {
        "item": {
          "data": {
            "type": "items",
            "id": "urn:adsk.wipprod:dm.lineage:jts1sOfCS6mdwCV38lKpGQ"
          },
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.jts1sOfCS6mdwCV38lKpGQ%3Fversion%3D1/item"
            }
          }
        },
        "links": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.jts1sOfCS6mdwCV38lKpGQ%3Fversion%3D1/relationships/links"
            }
          }
        },
        "refs": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.jts1sOfCS6mdwCV38lKpGQ%3Fversion%3D1/relationships/refs"
            },
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.jts1sOfCS6mdwCV38lKpGQ%3Fversion%3D1/refs"
            }
          }
        },
        "downloadFormats": {
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.jts1sOfCS6mdwCV38lKpGQ%3Fversion%3D1/downloadFormats"
            }
          }
        },
        "derivatives": {
          "data": {
            "type": "derivatives",
            "id": "dXJuOmFkc2sud2lwc3RnOmZzLmZpbGU6dmYuanRzMXNPZkNTNm1kd0NWMzhsS3BHUT92ZXJzaW9uPTE"
          },
          "meta": {
            "link": {
              "href": "/modelderivative/v2/designdata/dXJuOmFkc2sud2lwc3RnOmZzLmZpbGU6dmYuanRzMXNPZkNTNm1kd0NWMzhsS3BHUT92ZXJzaW9uPTE/manifest?scopes=b360project.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d,global,O2tenant.tenantId"
            }
          }
        },
        "thumbnails": {
          "data": {
            "type": "thumbnails",
            "id": "dXJuOmFkc2sud2lwc3RnOmZzLmZpbGU6dmYuanRzMXNPZkNTNm1kd0NWMzhsS3BHUT92ZXJzaW9uPTE"
          },
          "meta": {
            "link": {
              "href": "/modelderivative/v2/designdata/dXJuOmFkc2sud2lwc3RnOmZzLmZpbGU6dmYuanRzMXNPZkNTNm1kd0NWMzhsS3BHUT92ZXJzaW9uPTE/thumbnail?scopes=b360project.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d,global,O2tenant.tenantId"
            }
          }
        },
        "storage": {
          "data": {
            "type": "objects",
            "id": "urn:adsk.objects:os.object:wip.dm.prod/f5a8a8e8-9bbc-46cf-bce9-9cc34508c2d4.pdf"
          },
          "meta": {
            "link": {
              "href": "/oss/v2/buckets/wip.dm.prod/objects/f5a8a8e8-9bbc-46cf-bce9-9cc34508c2d4.pdf?scopes=b360project.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d,global,O2tenant.tenantId"
            }
          }
        }
      }
    }
  ],
  "included": [
    {
      "type": "items",
      "id": "urn:adsk.wipprod:dm.lineage:4cW918j8QsynzG0oZ6_Nbg",
      "attributes": {
        "displayName": "sample",
        "createTime": "2016-11-09T13:11:27+00:00",
        "createUserId": "BW9RM76WZBGL",
        "createUserName": "John Doe",
        "lastModifiedTime": "2016-11-09T13:11:36+00:00",
        "lastModifiedUserId": "BW9RM76WZBGL",
        "lastModifiedUserName": "John Doe",
        "hidden": false,
        "reserved": true,
        "reservedTime": "2016-11-09T13:11:30.000Z",
        "reservedUserId": "BW9RM76WZBGL",
        "reservedUserName": "John Doe",
        "extension": {
          "type": "items:autodesk.bim360:File",
          "version": "1.0",
          "schema": {
            "href": "/schema/v1/versions/items%3Aautodesk.bim360%3AFile-1.0"
          },
          "data": {}
        }
      },
      "links": {
        "self": {
          "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3A4cW918j8QsynzG0oZ6_Nbg"
        },
        "webView": {
          "href": "https://docs.b360.autodesk.com/projects/c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Afs.folder%3Aco.0J4paz_FQgWPX2QRsaBkiw/detail/viewer/items/urn%3Aadsk.wipprod%3Adm.lineage%3A4cW918j8QsynzG0oZ6_Nbg"
        }
      },
      "relationships": {
        "tip": {
          "data": {
            "type": "versions",
            "id": "urn:adsk.wipprod:fs.file:vf.4cW918j8QsynzG0oZ6_Nbg?version=1"
          },
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3A4cW918j8QsynzG0oZ6_Nbg/tip"
            }
          }
        },
        "versions": {
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3A4cW918j8QsynzG0oZ6_Nbg/versions"
            }
          }
        },
        "parent": {
          "data": {
            "type": "folders",
            "id": "urn:adsk.wipprod:fs.folder:co.KJRpLpSXRm66X2HB2Q7AQw"
          },
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3A4cW918j8QsynzG0oZ6_Nbg/parent"
            }
          }
        },
        "refs": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3A4cW918j8QsynzG0oZ6_Nbg/relationships/refs"
            },
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3A4cW918j8QsynzG0oZ6_Nbg/refs"
            }
          }
        },
        "links": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3A4cW918j8QsynzG0oZ6_Nbg/relationships/links"
            }
          }
        }
      }
    },
    {
      "type": "items",
      "id": "urn:adsk.wipprod:dm.lineage:jts1sOfCS6mdwCV38lKpGQ",
      "attributes": {
        "displayName": "sample",
        "createTime": "2016-11-09T13:13:09+00:00",
        "createUserId": "BW9RM76WZBGL",
        "createUserName": "John Doe",
        "lastModifiedTime": "2016-11-09T13:13:41+00:00",
        "lastModifiedUserId": "BW9RM76WZBGL",
        "lastModifiedUserName": "John Doe",
        "hidden": false,
        "reserved": true,
        "reservedTime": "2016-11-09T13:13:24.000Z",
        "reservedUserId": "BW9RM76WZBGL",
        "reservedUserName": "John Doe",
        "extension": {
          "type": "items:autodesk.bim360:File",
          "version": "1.0",
          "schema": {
            "href": "/schema/v1/versions/items%3Aautodesk.bim360%3AFile-1.0"
          },
          "data": {}
        }
      },
      "links": {
        "self": {
          "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3Ajts1sOfCS6mdwCV38lKpGQ"
        },
        "webView": {
          "href": "https://docs.b360.autodesk.com/projects/c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Afs.folder%3Aco.0J4paz_FQgWPX2QRsaBkiw/detail/viewer/items/urn%3Aadsk.wipprod%3Adm.lineage%3Ajts1sOfCS6mdwCV38lKpGQ"
        }
      },
      "relationships": {
        "tip": {
          "data": {
            "type": "versions",
            "id": "urn:adsk.wipprod:fs.file:vf.jts1sOfCS6mdwCV38lKpGQ?version=1"
          },
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3Ajts1sOfCS6mdwCV38lKpGQ/tip"
            }
          }
        },
        "versions": {
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3Ajts1sOfCS6mdwCV38lKpGQ/versions"
            }
          }
        },
        "parent": {
          "data": {
            "type": "folders",
            "id": "urn:adsk.wipprod:fs.folder:co.KJRpLpSXRm66X2HB2Q7AQw"
          },
          "links": {
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3Ajts1sOfCS6mdwCV38lKpGQ/parent"
            }
          }
        },
        "refs": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3Ajts1sOfCS6mdwCV38lKpGQ/relationships/refs"
            },
            "related": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3Ajts1sOfCS6mdwCV38lKpGQ/refs"
            }
          }
        },
        "links": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Adm.lineage%3Ajts1sOfCS6mdwCV38lKpGQ/relationships/links"
            }
          }
        }
      }
    }
  ]
}


