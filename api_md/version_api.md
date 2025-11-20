Documentation /Data Management API /Reference Guide
Versions
GET	projects/:project_id/versions/:version_id
Returns the version with the given version_id.

New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data/v1/projects/:project_id/versions/:version_id
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

version_id
string
The unique identifier of a version.
Response
HTTP Status Code Summary
200
OK
Successful retrieval of a specific version.
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
The object containing information on the version of the resource.
Example
Successful retrieval of a specific version.

Request
curl -v 'https://developer.api.autodesk.com/data/v1/projects/:project_id/versions/:version_id' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D2"
    }
  },
  "data": {
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
          "href": "https://developer.api.autodesk.com/schema/v1/versions/versions%3Aautodesk.bim360%3AFile-1.0"
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
      },
      "derivatives": {
        "data": {
          "type": "derivatives",
          "id": "dXJuOmFkc2sud2lwcWE6ZnMuZmlsZTp2Zi50X3hodWwwYVFkbWhhN2FBaVBuXzlnP3ZlcnNpb249MQ"
        },
        "meta": {
          "link": {
            "href": "/modelderivative/v2/designdata/dXJuOmFkc2sud2lwcWE6ZnMuZmlsZTp2Zi50X3hodWwwYVFkbWhhN2FBaVBuXzlnP3ZlcnNpb249MQ/manifest?scopes=b360project.6f8813fe-31a7-4440-bc63-d8ca97c856b4,global,O2tenant.tenantId"
          }
        }
      },
      "thumbnails": {
        "data": {
          "type": "thumbnails",
          "id": "dXJuOmFkc2sud2lwcWE6ZnMuZmlsZTp2Zi50X3hodWwwYVFkbWhhN2FBaVBuXzlnP3ZlcnNpb249MQ"
        },
        "meta": {
          "link": {
            "href": "/modelderivative/v2/designdata/dXJuOmFkc2sud2lwcWE6ZnMuZmlsZTp2Zi50X3hodWwwYVFkbWhhN2FBaVBuXzlnP3ZlcnNpb249MQ/thumbnail?scopes=b360project.295285be-9cac-44d6-b365-625ebd327483,global,O2tenant.tenantId"
          }
        }
      },
      "downloadFormats": {
        "links": {
          "related": {
            "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D2/downloadFormats"
          }
        }
      }
    }
  }

Documentation /Data Management API /Reference Guide
Versions
GET	projects/:project_id/versions/:version_id/downloadFormats
Returns a collection of file formats this version could be converted to and downloaded as.

New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data/v1/projects/:project_id/versions/:version_id/downloadFormats
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

version_id
string
The unique identifier of a version.
Response
HTTP Status Code Summary
200
OK
Successful retrieval of the available download formats for a specific version.
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
The object containing information on the download_formats of the resource.
Example
Successful retrieval of the available download formats for a specific version.

Request
curl -v 'https://developer.api.autodesk.com/data/v1/projects/:project_id/versions/:version_id/downloadFormats' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "/data/v1/projects/{some_project_id}/versions/{some_version_id}/downloadFormats"
    }
  },
  "data": {
    "type": "downloadFormats",
    "id": "96af4f60-53b8-4efe-b890-1eaa9ea5cb08",
    "attributes": {
      "formats": [
        {
          "fileType": "pdf"
        },
        {
          "fileType": "dwg"
        }
      ]
    }
  }
}Documentation /Data Management API /Reference Guide
Versions
GET	projects/:project_id/versions/:version_id/downloads
Returns a set of already available downloads for this version.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data/v1/projects/:project_id/versions/:version_id/downloads
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

version_id
string
The unique identifier of a version.
Request
Query String Parameters
filter[format.fileType]
array: string
Filter by the file type of the download object.
Response
HTTP Status Code Summary
200
OK
Successful retrieval of the available downloads collection associated with a specific version.
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
The array of download objects.
Example
Successful retrieval of the available downloads collection associated with a specific version.

Request
curl -v 'https://developer.api.autodesk.com/data/v1/projects/:project_id/versions/:version_id/downloads' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "/data/v1/projects/{project_id}/downloads"
    }
  },
  "data": [
    {
      "type": "downloads",
      "id": "{download_id}",
      "attributes": {
        "format": {
          "fileType": "pdf"
        }
      },
      "relationships": {
        "source": {
          "links": {
            "related": {
              "href": "/data/v1/projects/{project_id}/downloads/{download_id}/source"
            }
          },
          "data": {
            "type": "versions",
            "id": "{version_id}"
          }
        },
        "storage": {
          "data": {
            "type": "objects",
            "id": "urn:adsk.objects:os.object:{wip_bucket}/{guid}.pdf"
          },
          "meta": {
            "link": {
              "href": "/oss/v2/buckets/{wip_bucket}/objects/{guid}.pdf?scopes={list_of_scopes}"
            }
          }
        }
      },
      "links": {
        "self": {
          "href": "/data/v1/projects/{project_id}/downloads/{download_id}"
        }
      }
    }
  ]
}Documentation /Data Management API /Reference Guide
Versions
GET	projects/:project_id/versions/:version_id/item
Returns the item the given version is associated with.

New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data/v1/projects/:project_id/versions/:version_id/item
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

version_id
string
The unique identifier of a version.
Response
HTTP Status Code Summary
200
OK
Successful retrieval of a specific item.
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
The object containing information on the item.
included
array: object
The other resources included within this item.
Example
Successful retrieval of a specific item.

Request
curl -v 'https://developer.api.autodesk.com/data/v1/projects/:project_id/versions/:version_id/item' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:hC6k4hndRWaeIVhIjvHu8w"
    }
  },
  "data": {
    "type": "items",
    "id": "urn:adsk.wipprod:dm.lineage:hC6k4hndRWaeIVhIjvHu8w",
    "attributes": {
      "displayName": "my_model.rvt",
      "createTime": "2018-01-17T11:52:11.0000000Z",
      "createUserId": "BW9RM76WZBGL",
      "createUserName": "John Doe",
      "lastModifiedTime": "2018-01-17T11:53:19.0000000Z",
      "lastModifiedUserId": "BW9RM76WZBGL",
      "lastModifiedUserName": "John Doe",
      "hidden": false,
      "reserved": false,
      "extension": {
        "type": "items:autodesk.bim360:C4RModel",
        "version": "1.0.0",
        "schema": {
          "href": "https://developer.api.autodesk.com/schema/v1/versions/items:autodesk.bim360:C4RModel-1.0.0"
        },
        "data": {
          "sourceFileName": "my_model.rvt"
        }
      }
    },
    "links": {
      "self": {
        "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:hC6k4hndRWaeIVhIjvHu8w"
      },
      "webView": {
        "href": "https://docs.b360.autodesk.com/projects/c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Afs.folder%3Aco.0J4paz_FQgWPX2QRsaBkiw/detail/viewer/items/urn:adsk.wipprod:dm.lineage:hC6k4hndRWaeIVhIjvHu8w"
      }
    },
    "relationships": {
      "tip": {
        "data": {
          "type": "versions",
          "id": "urn:adsk.wipprod:fs.file:vf.hC6k4hndRWaeIVhIjvHu8w?version=2"
        },
        "links": {
          "related": {
            "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:hC6k4hndRWaeIVhIjvHu8w/tip"
          }
        }
      },
      "versions": {
        "links": {
          "related": {
            "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:hC6k4hndRWaeIVhIjvHu8w/versions"
          }
        }
      },
      "parent": {
        "data": {
          "type": "folders",
          "id": "urn:adsk.wipprod:fs.folder:co.sdfedf8wef"
        },
        "links": {
          "related": {
            "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:hC6k4hndRWaeIVhIjvHu8w/parent"
          }
        }
      },
      "refs": {
        "links": {
          "self": {
            "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:hC6k4hndRWaeIVhIjvHu8w/relationships/refs"
          },
          "related": {
            "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:hC6k4hndRWaeIVhIjvHu8w/refs"
          }
        }
      },
      "links": {
        "links": {
          "self": {
            "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:hC6k4hndRWaeIVhIjvHu8w/relationships/links"
          }
        }
      }
    }
  },
  "included": [
    {
      "type": "versions",
      "id": "urn:adsk.wipprod:fs.file:vf.hC6k4hndRWaeIVhIjvHu8w?version=2",
      "attributes": {
        "name": "my_model.rvt",
        "displayName": "my_model",
        "createTime": "2018-01-17T11:52:34.0000000Z",
        "createUserId": "BW9RM76WZBGL",
        "createUserName": "John Doe",
        "lastModifiedTime": "2018-01-17T11:53:20.0000000Z",
        "lastModifiedUserId": "BW9RM76WZBGL",
        "lastModifiedUserName": "John Doe",
        "versionNumber": 2,
        "mimeType": "application/vnd.autodesk.r360",
        "fileType": "rvt",
        "extension": {
          "type": "versions:autodesk.bim360:C4RModel",
          "version": "1.0.0",
          "schema": {
            "href": "https://developer.api.autodesk.com/schema/v1/versions/versions:autodesk.bim360:C4RModel-1.0.0"
          },
          "data": {
            "modelVersion": 2,
            "projectGuid": "project-guid",
            "originalItemUrn": "urn:adsk.wipprod:dm.lineage:hC6k4hndRWaeIVhIjvHu8w",
            "isCompositeDesign": false,
            "modelType": "multiuser",
            "mimeType": "application/vnd.autodesk.r360",
            "modelGuid": "model-guid",
            "processState": "PROCESSING_COMPLETE",
            "extractionState": "SUCCESS",
            "splittingState": "NOT_SPLIT",
            "reviewState": "NOT_IN_REVIEW",
            "revisionDisplayLabel": "2",
            "sourceFileName": "my_model.rvt",
            "conformingStatus": "NONE"
          }
        }
      },
      "links": {
        "self": {
          "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn:adsk.wipprod:fs.file:vf.hC6k4hndRWaeIVhIjvHu8w%3Fversion=2"
        },
        "webView": {
          "href": "https://docs.b360.autodesk.com/projects/c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Afs.folder%3Aco.0J4paz_FQgWPX2QRsaBkiw/detail/viewer/items/urn:adsk.wipprod:fs.file:vf.hC6k4hndRWaeIVhIjvHu8w%3Fversion%3D2"
        }
      },
      "relationships": {
        "item": {
          "data": {
            "type": "items",
            "id": "urn:adsk.wipprod:dm.lineage:hC6k4hndRWaeIVhIjvHu8w"
          },
          "links": {
            "related": {
              "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn:adsk.wipprod:fs.file:vf.hC6k4hndRWaeIVhIjvHu8w%3Fversion=2/item"
            }
          }
        },
        "links": {
          "links": {
            "self": {
              "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn:adsk.wipprod:fs.file:vf.hC6k4hndRWaeIVhIjvHu8w%3Fversion=2/relationships/links"
            }
          }
        },
        "refs": {
          "links": {
            "self": {
              "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn:adsk.wipprod:fs.file:vf.hC6k4hndRWaeIVhIjvHu8w%3Fversion=2/relationships/refs"
            },
            "related": {
              "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn:adsk.wipprod:fs.file:vf.hC6k4hndRWaeIVhIjvHu8w%3Fversion=2/refs"
            }
          }
        },
        "downloadFormats": {
          "links": {
            "related": {
              "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn:adsk.wipprod:fs.file:vf.hC6k4hndRWaeIVhIjvHu8w%3Fversion=2/downloadFormats"
            }
          }
        },
        "derivatives": {
          "data": {
            "type": "derivatives",
            "id": "derivative-id"
          },
          "meta": {
            "link": {
              "href": "https://developer.api.autodesk.com/modelderivative/v2/designdata/derivative-id/manifest?scopes=b360project.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d,O2tenant.tenant-id"
            }
          }
        },
        "thumbnails": {
          "data": {
            "type": "thumbnails",
            "id": "derivative-id"
          },
          "meta": {
            "link": {
              "href": "https://developer.api.autodesk.com/modelderivative/v2/designdata/derivative-id/thumbnail?scopes=b360project.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d,O2tenant.tenant-id"
            }
          }
        },
        "storage": {
          "data": {
            "type": "objects",
            "id": "urn:adsk.objects:os.object:wip.dm.prod/3c8f6bbc-fe5c-4815-a92e-8b8635e7b1cb.rvt"
          },
          "meta": {
            "link": {
              "href": "https://developer.api.autodesk.com/oss/v2/buckets/wip.dm.prod/objects/3c8f6bbc-fe5c-4815-a92e-8b8635e7b1cb.rvt?scopes=b360project.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d,O2tenant.tenant-id"
            }
          }
        }
      }
    }
  ]
}
Documentation /Data Management API /Reference Guide
Versions
GET	projects/:project_id/versions/:version_id/refs
Returns the resources (items, folders, and versions) that have a custom relationship with the given version_id. Custom relationships can be established between a version of an item and other resources within the data domain service (folders, items, and versions).

Notes:

Each relationship is defined by the id of the object at the other end of the relationship, together with type, attributes, and relationships links.
Callers will typically use a filter parameter to restrict the response to the custom relationship types (filter[meta.refType]) they are interested in.
The response body will have an included array which contains the ref resources that are involved in the relationship, which is essentially the GET projects/:project_id/versions/:version_id/relationships/refs endpoint.
New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data/v1/projects/:project_id/versions/:version_id/refs
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

version_id
string
The unique identifier of a version.
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
The data object.
included
object
The object containing information on the ref of the resource.
Example
Successful retrieval of a resource collection.

Request
curl -v 'https://developer.api.autodesk.com/data/v1/projects/:project_id/versions/:version_id/refs' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "/data/v1/projects/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjEjMjAyMzAzMTcwMDAwMDAx/versions/urn:adsk.wipprod:fs.file:vf.b909RzMKR4mhc3O7UBY_8g/refs"
    }
  },
  "data": [
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
          "href": "/data/v1/projects/b.6f8813fe-31a7-4440-bc63-d8ca97c856b4/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D2"
        }
      },
      "relationships": {
        "item": {
          "links": {
            "related": {
              "href": "/data/v1/projects/b.6f8813fe-31a7-4440-bc63-d8ca97c856b4/items/urn%3Aadsk.wipprod%3Adm.lineage%3Ab909RzMKR4mhc3O7UBY_8g"
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
              "href": "/data/v1/projects/b.6f8813fe-31a7-4440-bc63-d8ca97c856b4/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D2/relationships/refs"
            },
            "related": {
              "href": "/data/v1/projects/b.6f8813fe-31a7-4440-bc63-d8ca97c856b4/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D2/refs"
            }
          }
        },
        "links": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.6f8813fe-31a7-4440-bc63-d8ca97c856b4/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D2/relationships/links"
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
          "href": "/data/v1/projects/b.6f8813fe-31a7-4440-bc63-d8ca97c856b4/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D1"
        }
      },
      "relationships": {
        "item": {
          "links": {
            "related": {
              "href": "/data/v1/projects/b.6f8813fe-31a7-4440-bc63-d8ca97c856b4/items/urn%3Aadsk.wipprod%3Adm.lineage%3Ab909RzMKR4mhc3O7UBY_8g"
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
              "href": "/data/v1/projects/b.6f8813fe-31a7-4440-bc63-d8ca97c856b4/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D1/relationships/refs"
            },
            "related": {
              "href": "/data/v1/projects/b.6f8813fe-31a7-4440-bc63-d8ca97c856b4/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D1/refs"
            }
          }
        },
        "links": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.6f8813fe-31a7-4440-bc63-d8ca97c856b4/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D1/relationships/links"
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
        "reservedTime": "2016-04-01T11:10:20.000Z",
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
              "href": "/data/v1/projects/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjEjMjAyMzAzMTcwMDAwMDAx/items/urn%3Aadsk.wipprod%3Adm.lineage%3AhC6k4hndRWaeIVhIjvHu8w/tip"
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
              "href": "/data/v1/projects/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjEjMjAyMzAzMTcwMDAwMDAx/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/parent"
            }
          }
        },
        "versions": {
          "links": {
            "related": {
              "href": "/data/v1/projects/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjEjMjAyMzAzMTcwMDAwMDAx/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/versions"
            }
          }
        },
        "refs": {
          "links": {
            "self": {
              "href": "/data/v1/projects/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjEjMjAyMzAzMTcwMDAwMDAx/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/relationships/refs"
            },
            "related": {
              "href": "/data/v1/projects/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjEjMjAyMzAzMTcwMDAwMDAx/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/refs"
            }
          }
        },
        "links": {
          "links": {
            "self": {
              "href": "/data/v1/projects/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjEjMjAyMzAzMTcwMDAwMDAx/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/relationships/links"
            }
          }
        }
      },
      "links": {
        "self": {
          "href": "/data/v1/projects/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjEjMjAyMzAzMTcwMDAwMDAx/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g"
        }
      }
    }
  ]
Documentation /Data Management API /Reference Guide
Versions
GET	projects/:project_id/versions/:version_id/relationships/links
Returns a collection of links for the given item_id-version_id object. Custom relationships can be established between a version of an item and other external resources residing outside the data domain service. A link’s href defines the target URI to access a resource.

New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data/v1/projects/:project_id/versions/:version_id/relationships/links
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

version_id
string
The unique identifier of a version.
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
curl -v 'https://developer.api.autodesk.com/data/v1/projects/:project_id/versions/:version_id/relationships/links' \
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
}Documentation /Data Management API /Reference Guide
Versions
GET	projects/:project_id/versions/:version_id/relationships/refs
Returns the custom relationships that are associated with the given version_id. Custom relationships can be established between a version of an item and other resources within the data domain service (folders, items, and versions).

Notes:

Each relationship is defined by the id of the object at the other end of the relationship, together with type, specific reference meta including extension data.
Callers will typically use a filter parameter to restrict the response to the custom relationship types (filter[meta.refType]) they are interested in.
The response body will have an included array which contains the resources that are involved in the relationship, which is essentially the GET projects/:project_id/versions/:version_id/refs endpoint.
To get custom relationships for multiple versions, see the ListRefs command.
New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data/v1/projects/:project_id/versions/:version_id/relationships/refs
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

version_id
string
The unique identifier of a version.
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
curl -v 'https://developer.api.autodesk.com/data/v1/projects/:project_id/versions/:version_id/relationships/refs' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "/data/v1/projects/b.5ae9543e-abd5-45c5-8718-33d26652267f/versions/urn:adsk.wipprod:fs.file:vf.b909RzMKR4mhc3O7UBY_8g/relationships/refs"
    },
    "related": {
      "href": "/data/v1/projects/b.5ae9543e-abd5-45c5-8718-33d26652267f/versions/urn:adsk.wipprod:fs.file:vf.b909RzMKR4mhc3O7UBY_8g/refs"
    }
  },
  "data": [
    {
      "type": "versions",
      "id": "urn:adsk.wipprod:fs.file:vf.b909RzMKR4mhc3O7UBY_8g?version=2",
      "meta": {
        "refType": "xrefs",
        "fromId": "urn:adsk.wipprod:fs.file:vf.b909RzMKR4mhc3O7UBY_8g?version=2",
        "fromType": "versions",
        "toId": "urn:adsk.wipprod:fs.file:vf.b909RzMKR4mhc3O7UBY_8g?version=1",
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
          "href": "/data/v1/projects/b.6f8813fe-31a7-4440-bc63-d8ca97c856b4/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D2"
        }
      },
      "relationships": {
        "item": {
          "links": {
            "related": {
              "href": "/data/v1/projects/b.6f8813fe-31a7-4440-bc63-d8ca97c856b4/items/urn%3Aadsk.wipprod%3Adm.lineage%3Ab909RzMKR4mhc3O7UBY_8g"
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
              "href": "/data/v1/projects/b.6f8813fe-31a7-4440-bc63-d8ca97c856b4/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D2/relationships/refs"
            },
            "related": {
              "href": "/data/v1/projects/b.6f8813fe-31a7-4440-bc63-d8ca97c856b4/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D2/refs"
            }
          }
        },
        "links": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.6f8813fe-31a7-4440-bc63-d8ca97c856b4/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D2/relationships/links"
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
          "href": "/data/v1/projects/b.6f8813fe-31a7-4440-bc63-d8ca97c856b4/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D1"
        }
      },
      "relationships": {
        "item": {
          "links": {
            "related": {
              "href": "/data/v1/projects/b.6f8813fe-31a7-4440-bc63-d8ca97c856b4/items/urn%3Aadsk.wipprod%3Adm.lineage%3Ab909RzMKR4mhc3O7UBY_8g"
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
              "href": "/data/v1/projects/b.6f8813fe-31a7-4440-bc63-d8ca97c856b4/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D1/relationships/refs"
            },
            "related": {
              "href": "/data/v1/projects/b.6f8813fe-31a7-4440-bc63-d8ca97c856b4/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D1/refs"
            }
          }
        },
        "links": {
          "links": {
            "self": {
              "href": "/data/v1/projects/b.6f8813fe-31a7-4440-bc63-d8ca97c856b4/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g%3Fversion%3D1/relationships/links"
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
        "reservedTime": "2016-04-01T11:10:20.000Z",
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
              "href": "/data/v1/projects/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjEjMjAyMzAzMTcwMDAwMDAx/items/urn%3Aadsk.wipprod%3Adm.lineage%3AhC6k4hndRWaeIVhIjvHu8w/tip"
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
              "href": "/data/v1/projects/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjEjMjAyMzAzMTcwMDAwMDAx/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/parent"
            }
          }
        },
        "versions": {
          "links": {
            "related": {
              "href": "/data/v1/projects/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjEjMjAyMzAzMTcwMDAwMDAx/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/versions"
            }
          }
        },
        "refs": {
          "links": {
            "self": {
              "href": "/data/v1/projects/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjEjMjAyMzAzMTcwMDAwMDAx/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/relationships/refs"
            },
            "related": {
              "href": "/data/v1/projects/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjEjMjAyMzAzMTcwMDAwMDAx/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/refs"
            }
          }
        },
        "links": {
          "links": {
            "self": {
              "href": "/data/v1/projects/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjEjMjAyMzAzMTcwMDAwMDAx/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/relationships/links"
            }
          }
        }
      },
      "links": {
        "self": {
          "href": "/data/v1/projects/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjEjMjAyMzAzMTcwMDAwMDAx/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g"
        }
      }
    }
  ]
}

}



}