Documentation /Data Management API /Reference Guide
Hubs
GET	hubs
Returns a collection of accessible hubs for this member.

Hubs represent BIM 360 Team hubs, Fusion Team hubs (formerly known as A360 Team hubs), A360 Personal hubs, or BIM 360 Docs accounts. Team hubs include BIM 360 Team hubs and Fusion Team hubs (formerly known as A360 Team hubs). Personal hubs include A360 Personal hubs. Only active hubs are listed.

Note that for BIM 360 Docs, a hub ID corresponds to an account ID in the BIM 360 API. To convert an account ID into a hub ID you need to add a "b." prefix. For example, an account ID of c8b0c73d-3ae9 translates to a hub ID of b.c8b0c73d-3ae9.

New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/project/v1/hubs
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
Query String Parameters
filter[id]
array: string
Filter by the id of the ref target.
filter[name]
array: string
Filter by the name of the ref target.
filter[extension.type]
array: string
Filter by extension type. Possible values: hubs:autodesk.core:Hub (team hubs), hubs:autodesk.bim360:Account (BIM 360 Docs accounts), hubs:autodesk.a360:PersonalHub (personal hubs).
Response
HTTP Status Code Summary
200
OK
Successful retrieval of the hubs collection.
401
Unauthorized
The supplied Authorization header was not valid or the supplied token scope was not acceptable. Verify Authentication and try again.
403
Forbidden
The request was successfully validated but permission is not granted or the application has not been white-listed. Do not try again unless you solve permissions first.
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
The array of hub objects.
Example
Successful retrieval of the hubs collection.

Request
curl -v 'https://developer.api.autodesk.com/project/v1/hubs' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "/project/v1/hubs"
    }
  },
  "data": [
    {
      "type": "hubs",
      "id": "a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjE",
      "attributes": {
        "name": "my team hub",
        "extension": {
          "type": "hubs:autodesk.core:Hub",
          "version": "1.0",
          "schema": {
            "href": "/schema/v1/versions/hubs%3Aautodesk.core%3AHub-1.0"
          },
          "data": {}
        },
        "region": "US"
      },
      "links": {
        "self": {
          "href": "/project/v1/hubs/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjE"
        }
      },
      "relationships": {
        "projects": {
          "links": {
            "related": {
              "href": "/project/v1/hubs/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjE/projects"
            }
          }
        },
        "pimCollection": {
          "data": {
            "type": "collection",
            "id": "co.d41d8cd00998ecf8427e"
          }
        }
      }
    },
    {
      "type": "hubs",
      "id": "a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjI=",
      "attributes": {
        "name": "my personal hub",
        "extension": {
          "type": "hubs:autodesk.a360:PersonalHub",
          "version": "1.0",
          "schema": {
            "href": "/schema/v1/versions/hubs%3Aautodesk.a360%3APersonalHub-1.0"
          },
          "data": {}
        },
        "region": "US"
      },
      "links": {
        "self": {
          "href": "/project/v1/hubs/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjI="
        }
      },
      "relationships": {
        "projects": {
          "links": {
            "related": {
              "href": "/project/v1/hubs/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjI=/projects"
            }
          }
        },
        "pimCollection": {
          "data": {
            "type": "collection",
            "id": "co.368e3dc4144c0ff253d6"
          }
        }
      }
    }
  ]
}

Documentation /Data Management API /Reference Guide
Hubs
GET	hubs/:hub_id
Returns data on a specific hub_id.

Note that for BIM 360 Docs, a hub ID corresponds to an account ID in the BIM 360 API. To convert an account ID into a hub ID you need to add a "b." prefix. For example, an account ID of c8b0c73d-3ae9 translates to a hub ID of b.c8b0c73d-3ae9.

New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/project/v1/hubs/:hub_id
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
hub_id
string
The unique identifier of a hub.
Response
HTTP Status Code Summary
200
OK
Successful retrieval of a specific hub.
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
The object containing information on the hub.
Example
Successful retrieval of a specific hub.

Request
curl -v 'https://developer.api.autodesk.com/project/v1/hubs/:hub_id' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "/project/v1/hubs/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjE"
    }
  },
  "data": {
    "type": "hubs",
    "id": "a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjE",
    "attributes": {
      "name": "my hub",
      "extension": {
        "data": {},
        "version": "1.0",
        "type": "hubs:autodesk.core:Hub",
        "schema": {
          "href": "/schema/v1/versions/hubs%3Aautodesk.core%3AHub-1.0"
        }
      },
      "region": "US"
    },
    "relationships": {
      "projects": {
        "links": {
          "related": {
            "href": "/project/v1/hubs/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjE/projects"
          }
        }
      },
      "pimCollection": {
        "data": {
          "type": "collection",
          "id": "co.d41d8cd00998ecf8427e"
        }
      }
    },
    "links": {
      "self": {
        "href": "/project/v1/hubs/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjE"
      }
    }
  }
}

Documentation /Data Management API /Reference Guide
Projects
GET	hubs/:hub_id/projects
Returns a collection of projects for a given hub_id. A project represents a BIM 360 Team project, a Fusion Team project, a BIM 360 Docs project, or an A360 Personal project. Multiple projects can be created within a single hub. Only active projects are listed.

Note that for BIM 360 Docs, a hub ID corresponds to an account ID in the BIM 360 API. To convert an account ID into a hub ID you need to add a "b." prefix. For example, an account ID of c8b0c73d-3ae9 translates to a hub ID of b.c8b0c73d-3ae9.

Similarly, for BIM 360 Docs, the project ID in the Data Management API corresponds to the project ID in the BIM 360 API. To convert a project ID in the BIM 360 API into a project ID in the Data Management API you need to add a "b." prefix. For example, a project ID of c8b0c73d-3ae9 translates to a project ID of b.c8b0c73d-3ae9.

New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/project/v1/hubs/:hub_id/projects
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
hub_id
string
The unique identifier of a hub.
Request
Query String Parameters
filter[id]
array: string
Filter by the id of the ref target.
filter[extension.type]
array: string
Filter by the extension type.
page[number]
int
Specifies what page to return. Page numbers start at 0, so the first page is page 0.
page[limit]
int
Specifies the maximum number of elements to return in the page. The default value is 200. The min value is 1. The max value is 200.
Response
HTTP Status Code Summary
200
OK
Successful retrieval of the projects collection associated with a specific hub.
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers. The client SHOULD NOT repeat the request without modifications. The response body may give an indication of what is wrong with the request.
401
Unauthorized
The supplied Authorization header was not valid or the supplied token scope was not acceptable. Verify Authentication and try again.
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
The array of project objects.
Example
Successful retrieval of the projects collection associated with a specific hub.

Request
curl -v 'https://developer.api.autodesk.com/project/v1/hubs/:hub_id/projects' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "https://developer.api.autodesk.com/project/v1/hubs/b.622cb5d1-581b-4a46-a6d9-4ebc68ea4051/projects"
    }
  },
  "data": [
    {
      "type": "projects",
      "id": "b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d",
      "attributes": {
        "name": "my project",
        "scopes": [
          "global"
        ],
        "extension": {
          "type": "projects:autodesk.bim360:Project",
          "version": "1.0",
          "schema": {
            "href": "https://developer.api.autodesk.com/schema/v1/versions/projects:autodesk.bim360:Project-1.0"
          },
          "data": {
            "projectType": "BIM360"
          }
        }
      },
      "links": {
        "self": {
          "href": "https://developer.api.autodesk.com/project/v1/hubs/b.622cb5d1-581b-4a46-a6d9-4ebc68ea4051/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d"
        },
        "webView": {
          "href": "https://docs.b360.autodesk.com/projects/c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d"
        }
      },
      "relationships": {
        "hub": {
          "data": {
            "type": "hubs",
            "id": "b.622cb5d1-581b-4a46-a6d9-4ebc68ea4051"
          },
          "links": {
            "related": {
              "href": "https://developer.api.autodesk.com/project/v1/hubs/b.622cb5d1-581b-4a46-a6d9-4ebc68ea4051"
            }
          }
        },
        "rootFolder": {
          "data": {
            "type": "folders",
            "id": "urn:adsk.wipprod:fs.folder:co.lw7b0sXUQ-6hWRgf34hBuw"
          },
          "meta": {
            "link": {
              "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn:adsk.wipprod:fs.folder:co.lw7b0sXUQ-6hWRgf34hBuw"
            }
          }
        },
        "topFolders": {
          "links": {
            "related": {
              "href": "https://developer.api.autodesk.com/project/v1/hubs/b.622cb5d1-581b-4a46-a6d9-4ebc68ea4051/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/topFolders"
            }
          }
        },
        "issues": {
          "data": {
            "type": "issueContainerId",
            "id": "93f8bd6a-2222-415c-8d58-c8fa7c292044"
          },
          "meta": {
            "link": {
              "href": "https://developer.api.autodesk.com/issues/v1/containers/93f8bd6a-2222-415c-8d58-c8fa7c292044/issues"
            }
          }
        },
        "submittals": {
          "data": {
            "type": "submittalContainerId",
            "id": "c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d"
          },
          "meta": {
            "link": {
              "href": "https://developer.api.autodesk.com/submittals/v1/containers/c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items"
            }
          }
        },
        "rfis": {
          "data": {
            "type": "rfisContainerId",
            "id": "93f8bd6a-2222-415c-8d58-c8fa7c292044"
          },
          "meta": {
            "link": {
              "href": "https://developer.api.autodesk.com/bim360/rfis/v1/containers/93f8bd6a-2222-415c-8d58-c8fa7c292044/rfis"
            }
          }
        },
        "markups": {
          "data": {
            "type": "markupsContainerId",
            "id": "93f8bd6a-2222-415c-8d58-c8fa7c292044"
          },
          "meta": {
            "link": {
              "href": "https://developer.api.autodesk.com/issues/v1/containers/93f8bd6a-2222-415c-8d58-c8fa7c292044/markups"
            }
          }
        },
        "checklists": {
          "data": {
            "type": "checklistsContainerId",
            "id": "93f8bd6a-2222-415c-8d58-c8fa7c292044"
          },
          "meta": {
            "link": {
              "href": "https://developer.api.autodesk.com/bim360/checklists/v1/containers/93f8bd6a-2222-415c-8d58-c8fa7c292044/instances"
            }
          }
        },
        "cost": {
          "data": {
            "type": "costContainerId",
            "id": "c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d"
          },
          "meta": {
            "link": {
              "href": "https://developer.api.autodesk.com/cost/v1/containers/c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/budgets"
            }
          }
        },
        "locations": {
          "data": {
            "type": "locationsContainerId",
            "id": "5010258a-a341-4d95-8046-3905e1a983a6"
          },
          "meta": {
            "link": {
              "href": "https://developer.api.autodesk.com/bim360/locations/v2/containers/5010258a-a341-4d95-8046-3905e1a983a6/trees/default/nodes"
            }
          }
        }
      }
    }
  ]
}
Show Less
Example
Successful retrieval of the projects collection associated with a specific hub with pagination.

Request
curl -v 'https://developer.api.autodesk.com/project/v1/hubs/:hub_id/projects?page[number]=1&page[limit]=2' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "/project/v1/hubs/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjE/projects"
    },
    "first": {
        "href": "project/v1/hubs/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjE/projects?page%5Bnumber%5D=0&page%5Blimit%5D=2"
    },
    "prev": {
        "href": "/project/v1/hubs/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjE/projects?page%5Bnumber%5D=0&page%5Blimit%5D=2"
    },
    "next": {
        "href": "/project/v1/hubs/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjE/projects?page%5Bnumber%5D=2&page%5Blimit%5D=2"
    }
  },
  "data": [
    {
      "type": "projects",
      "id": "a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjEjMjAyMzAzMTcwMDAwMDAx",
      "attributes": {
        "name": "my project",
        "scopes": [
          "global"
        ],
        "extension": {
          "type": "projects:autodesk.core:Project",
          "version": "1.0",
          "schema": {
            "href": "/schema/v1/versions/projects%3Aautodesk.core%3AProject-1.0"
          },
          "data": {
              "projectType": "ACC"
          }
        }
      },
      "links": {
        "self": {
          "href": "/project/v1/hubs/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjE/projects/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjEjMjAyMzAzMTcwMDAwMDAx"
        }
      },
      "relationships": {
        "hub": {
          "data": {
            "type": "hubs",
            "id": "a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjE"
          },
          "links": {
            "related": {
              "href": "/project/v1/hubs/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjE"
            }
          }
        },
        "rootFolder": {
          "data": {
            "type": "folders",
            "id": "urn:adsk.wipprod:dm.folder:hC6k4hndRWaeIVhIjvHu8w"
          },
          "meta": {
            "link": {
              "href": "/data/v1/projects/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjEjMjAyMzAzMTcwMDAwMDAx/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w"
            }
          }
        },
        "topFolders": {
          "links": {
            "related": {
              "href": "/project/v1/hubs/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjE/projects/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjEjMjAyMzAzMTcwMDAwMDAx/topFolders"
            }
          }
        }
      }
    },
    {
      "type": "projects",
      "id": "a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjEjMjAyMzAzMTcwMDAwMDAx",
      "attributes": {
        "name": "my project",
        "scopes": [
          "global"
        ],
        "extension": {
          "type": "projects:autodesk.core:Project",
          "version": "1.0",
          "schema": {
            "href": "/schema/v1/versions/projects%3Aautodesk.core%3AProject-1.0"
          },
          "data": {}
        }
      },
      "links": {
        "self": {
          "href": "/project/v1/hubs/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjE/projects/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjEjMjAyMzAzMTcwMDAwMDAx"
        }
      },
      "relationships": {
        "hub": {
          "data": {
            "type": "hubs",
            "id": "a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjE"
          },
          "links": {
            "related": {
              "href": "/project/v1/hubs/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjE"
            }
          }
        },
        "rootFolder": {
          "data": {
            "type": "folders",
            "id": "urn:adsk.wipprod:dm.folder:hC6k4hndRWaeIVhIjvHu8w"
          },
          "meta": {
            "link": {
              "href": "/data/v1/projects/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjEjMjAyMzAzMTcwMDAwMDAx/folders/urn%3Aadsk.wipprod%3Adm.folder%3AhC6k4hndRWaeIVhIjvHu8w"
            }
          }
        },
        "topFolders": {
          "links": {
            "related": {
              "href": "/project/v1/hubs/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjE/projects/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjEjMjAyMzAzMTcwMDAwMDAx/topFolders"
            }
          }
        }
      }
    }
  ]
}

Documentation /Data Management API /Reference Guide
Projects
GET	hubs/:hub_id/projects/:project_id
Returns a project for a given project_id.

Note that for BIM 360 Docs, a hub ID corresponds to an account ID in the BIM 360 API. To convert an account ID into a hub ID you need to add a "b." prefix. For example, an account ID of c8b0c73d-3ae9 translates to a hub ID of b.c8b0c73d-3ae9.

Similarly, for BIM 360 Docs, the project ID in the Data Management API corresponds to the project ID in the BIM 360 API. To convert a project ID in the BIM 360 API into a project ID in the Data Management API you need to add a "b." prefix. For example, a project ID of c8b0c73d-3ae9 translates to a project ID of b.c8b0c73d-3ae9.

New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/project/v1/hubs/:hub_id/projects/:project_id
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
hub_id
string
The unique identifier of a hub.
project_id
string
The unique identifier of a project.
For BIM 360 Docs, the project ID in the Data Management API corresponds to the project ID in the BIM 360 API. To convert a project ID in the BIM 360 API into a project ID in the Data Management API you need to add a “b." prefix. For example, a project ID of c8b0c73d-3ae9 translates to a project ID of b.c8b0c73d-3ae9.

Response
HTTP Status Code Summary
200
OK
Successful retrieval of a specific project.
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
The object containing information on the project.
Example
Successful retrieval of a specific project.

Request
curl -v 'https://developer.api.autodesk.com/project/v1/hubs/:hub_id/projects/:project_id' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "https://developer.api.autodesk.com/project/v1/hubs/b.622cb5d1-581b-4a46-a6d9-4ebc68ea4051/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d"
    }
  },
  "data": {
    "type": "projects",
    "id": "b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d",
    "attributes": {
      "name": "my project",
      "scopes": [
        "global"
      ],
      "extension": {
        "type": "projects:autodesk.bim360:Project",
        "version": "1.0",
        "schema": {
          "href": "https://developer.api.autodesk.com/schema/v1/versions/projects:autodesk.bim360:Project-1.0"
        },
        "data": {
          "projectType": "BIM360"
        }
      }
    },
    "links": {
      "self": {
        "href": "https://developer.api.autodesk.com/project/v1/hubs/b.622cb5d1-581b-4a46-a6d9-4ebc68ea4051/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d"
      },
      "webView": {
        "href": "https://docs.b360.autodesk.com/projects/c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d"
      }
    },
    "relationships": {
      "hub": {
        "data": {
          "type": "hubs",
          "id": "b.622cb5d1-581b-4a46-a6d9-4ebc68ea4051"
        },
        "links": {
          "related": {
            "href": "https://developer.api.autodesk.com/project/v1/hubs/b.622cb5d1-581b-4a46-a6d9-4ebc68ea4051"
          }
        }
      },
      "rootFolder": {
        "data": {
          "type": "folders",
          "id": "urn:adsk.wipprod:fs.folder:co.lw7b0sXUQ-6hWRgf34hBuw"
        },
        "meta": {
          "link": {
            "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn:adsk.wipprod:fs.folder:co.lw7b0sXUQ-6hWRgf34hBuw"
          }
        }
      },
      "topFolders": {
        "links": {
          "related": {
            "href": "https://developer.api.autodesk.com/project/v1/hubs/b.622cb5d1-581b-4a46-a6d9-4ebc68ea4051/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/topFolders"
          }
        }
      },
      "issues": {
        "data": {
          "type": "issueContainerId",
          "id": "93f8bd6a-2222-415c-8d58-c8fa7c292044"
        },
        "meta": {
          "link": {
            "href": "https://developer.api.autodesk.com/issues/v1/containers/93f8bd6a-2222-415c-8d58-c8fa7c292044/issues"
          }
        }
      },
      "submittals": {
        "data": {
          "type": "submittalContainerId",
          "id": "c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d"
        },
        "meta": {
          "link": {
            "href": "https://developer.api.autodesk.com/submittals/v1/containers/c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items"
          }
        }
      },
      "rfis": {
        "data": {
          "type": "rfisContainerId",
          "id": "93f8bd6a-2222-415c-8d58-c8fa7c292044"
        },
        "meta": {
          "link": {
            "href": "https://developer.api.autodesk.com/bim360/rfis/v1/containers/93f8bd6a-2222-415c-8d58-c8fa7c292044/rfis"
          }
        }
      },
      "markups": {
        "data": {
          "type": "markupsContainerId",
          "id": "93f8bd6a-2222-415c-8d58-c8fa7c292044"
        },
        "meta": {
          "link": {
            "href": "https://developer.api.autodesk.com/issues/v1/containers/93f8bd6a-2222-415c-8d58-c8fa7c292044/markups"
          }
        }
      },
      "checklists": {
        "data": {
          "type": "checklistsContainerId",
          "id": "93f8bd6a-2222-415c-8d58-c8fa7c292044"
        },
        "meta": {
          "link": {
            "href": "https://developer.api.autodesk.com/bim360/checklists/v1/containers/93f8bd6a-2222-415c-8d58-c8fa7c292044/instances"
          }
        }
      },
      "cost": {
        "data": {
          "type": "costContainerId",
          "id": "c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d"
        },
        "meta": {
          "link": {
            "href": "https://developer.api.autodesk.com/cost/v1/containers/c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/budgets"
          }
        }
      },
      "locations": {
        "data": {
          "type": "locationsContainerId",
          "id": "5010258a-a341-4d95-8046-3905e1a983a6"
        },
        "meta": {
          "link": {
            "href": "https://developer.api.autodesk.com/bim360/locations/v2/containers/5010258a-a341-4d95-8046-3905e1a983a6/trees/default/nodes"
          }
        }
      }
    }
  }
}

Documentation /Data Management API /Reference Guide
Projects
GET	hubs/:hub_id/projects/:project_id/hub
Returns the hub for a given project_id.

New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/project/v1/hubs/:hub_id/projects/:project_id/hub
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
hub_id
string
The unique identifier of a hub.
project_id
string
The unique identifier of a project.
For BIM 360 Docs, the project ID in the Data Management API corresponds to the project ID in the BIM 360 API. To convert a project ID in the BIM 360 API into a project ID in the Data Management API you need to add a “b." prefix. For example, a project ID of c8b0c73d-3ae9 translates to a project ID of b.c8b0c73d-3ae9.

Response
HTTP Status Code Summary
200
OK
Successful retrieval of a specific hub.
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
The object containing information on the hub.
Example
Successful retrieval of a specific hub.

Request
curl -v 'https://developer.api.autodesk.com/project/v1/hubs/:hub_id/projects/:project_id/hub' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "/project/v1/hubs/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjE"
    }
  },
  "data": {
    "type": "hubs",
    "id": "a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjE",
    "attributes": {
      "name": "my hub",
      "extension": {
        "data": {},
        "version": "1.0",
        "type": "hubs:autodesk.core:Hub",
        "schema": {
          "href": "/schema/v1/versions/hubs%3Aautodesk.core%3AHub-1.0"
        }
      },
      "region": "US"
    },
    "relationships": {
      "projects": {
        "links": {
          "related": {
            "href": "/project/v1/hubs/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjE/projects"
          }
        }
      },
      "pimCollection": {
        "data": {
          "type": "collection",
          "id": "co.d41d8cd00998ecf8427e"
        }
      }
    },
    "links": {
      "self": {
        "href": "/project/v1/hubs/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjE"
      }
    }
  }
}

Documentation /Data Management API /Reference Guide
Projects
GET	hubs/:hub_id/projects/:project_id/topFolders
Returns the details of the highest level folders the user has access to for a given project. The user must have at least read access to the folders.

If the user is a Project Admin, it returns all top level folders in the project. Otherwise, it returns all the highest level folders in the folder hierarchy the user has access to.

Note that when users have access to a folder, access is automatically granted to its subfolders.

New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/project/v1/hubs/:hub_id/projects/:project_id/topFolders
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
hub_id
string
The unique identifier of a hub.
project_id
string
The unique identifier of a project.
For BIM 360 Docs, the project ID in the Data Management API corresponds to the project ID in the BIM 360 API. To convert a project ID in the BIM 360 API into a project ID in the Data Management API you need to add a “b." prefix. For example, a project ID of c8b0c73d-3ae9 translates to a project ID of b.c8b0c73d-3ae9.

Request
Query String Parameters
excludeDeleted
boolean
Specify whether to exclude deleted folders in response for BIM 360 Docs projects when user context is provided.
true: response will exclude deleted folders for BIM 360 Docs projects.

false (default): response will not exclude deleted folders for BIM 360 Docs projects.

projectFilesOnly
boolean
Specify whether only Project Files folder or its subfolders will be returned for BIM 360 Docs projects when user context is provided.
true: response will include only Project Files folder and its subfolders for BIM 360 Docs projects.

false (default): response will include all available folders.

Response
HTTP Status Code Summary
200
OK
Successful retrieval of the top folders’ details.
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
The array of folder objects.
Example
Successful retrieval of the top folders’ details.

Request
curl -v 'https://developer.api.autodesk.com/project/v1/hubs/:hub_id/projects/:project_id/topFolders' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "/project/v1/hubs/b.622cb5d1-581b-4a46-a6d9-4ebc68ea4051/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/topFolders"
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
            "isRoot": false,
            "folderType": "normal",
            "folderParents": [
              {
                "urn": "urn:adsk.wipprod:fs.folder:co.R3JhbmRwYXJlbnQK",
                "isRoot": true,
                "title": "Project Files",
                "parentUrn": "urn:adsk.wipprod:fs.folder:co.R3JlYXQgR3JhbmRwYXJlbnQK"
              },
              {
                "urn": "urn:adsk.wipprod:fs.folder:co.5-pCTuRbQI2fosqUJoNJ9w",
                "isRoot": false,
                "title": "ViewOnlySupportTest",
                "parentUrn": "urn:adsk.wipprod:fs.folder:co.UGFyZW50Cg"
              }
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
  ]
}

Documentation /Data Management API /Reference Guide
Projects
GET	projects/:project_id/downloads/:download_id
Returns the details for a specific download.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data/v1/projects/:project_id/downloads/:download_id
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

download_id
string
The unique identifier of a download job.
Response
HTTP Status Code Summary
200
OK
Successful retrieval of the details for a specific download object.
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
The object containing information on the download resource.
Example
Successful retrieval of the details for a specific download object.

Request
curl -v 'https://developer.api.autodesk.com/data/v1/projects/:project_id/downloads/:download_id' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "/data/v1/projects/{project_id}/downloads/{download_id}"
    }
  },
  "data": {
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
}

Documentation /Data Management API /Reference Guide
Projects
GET	projects/:project_id/jobs/:job_id
Returns the job_id object.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data/v1/projects/:project_id/jobs/:job_id
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

job_id
string
The unique identifier of a job.
Response
HTTP Status Code Summary
200
OK
Successful retrieval of the details for a specific job.
303
Redirect
The request has been redirected to a new location.
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
The object containing information on the task job.
Example
Successful retrieval of the details for a specific job.

Request
curl -v 'https://developer.api.autodesk.com/data/v1/projects/:project_id/jobs/:job_id' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "/data/v1/projects/{project_id}/jobs/{job_id}"
    }
  },
  "data": {
    "type": "jobs",
    "id": "{job_id}",
    "attributes": {
      "status": "queued"
    },
    "links": {
      "self": {
        "href": "/data/v1/projects/{project_id}/jobs/{job_id}"
      }
    }
  }
}

Documentation /Data Management API /Reference Guide
Projects
POST	projects/:project_id/downloads
Request the creation of a new download for a specific and supported file type. The fileType specified in the POST body needs to be contained in the list of supported file types returned by the GET projects/:project_id/versions/:version_id/downloadFormats endpoint for the specified version_id.

Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/data/v1/projects/:project_id/downloads
Authentication Context	
user context optional
Required OAuth Scopes	
data:create
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via either a two-legged or three-legged OAuth flow.
Content-Type*
string
Must be application/vnd.api+json
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

Request
Body Structure
describe the download to be created.

 Expand all
jsonapi*
object
The JSON API object.
data*
object
The data object.
* Required
Response
HTTP Status Code Summary
202
Accepted
Successful creation of a job.
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
Body Structure (202)
 Expand all
jsonapi
object
The JSON API object.
links
object
Information on links to this resource.
data
object
The object containing information on the task job.
Example
Successful creation of a job.

Request
curl -v 'https://developer.api.autodesk.com/data/v1/projects/:project_id/downloads' \
  -X 'POST' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a' \
  -H 'Content-Type: application/vnd.api+json' \
  -d '{
        "jsonapi": {
          "version": "1.0"
        },
        "data": {
          "type": "downloads",
          "attributes": {
            "format": {
              "fileType": "dwf"
            }
          },
          "relationships": {
            "source": {
              "data": {
                "type": "versions",
                "id": "{version_id}"
              }
            }
          }
        }
      }'
Show Less
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "/data/v1/projects/{project_id}/jobs/{job_id}"
    }
  },
  "data": {
    "type": "jobs",
    "id": "{job_id}",
    "attributes": {
      "status": "queued"
    },
    "links": {
      "self": {
        "href": "/data/v1/projects/{project_id}/jobs/{job_id}"
      }
    }
  }
}

以下是FOLDERS API：
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

cumentation /Data Management API /Reference Guide
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

以下是ITEMS API:

Documentation /Data Management API /Reference Guide
Items
GET	projects/:project_id/items/:item_id
Retrieves metadata for a specified item. Items represent word documents, fusion design files, drawings, spreadsheets, etc.

Notes:

The tip version for the item is included in the included array of the payload.
To retrieve metadata for multiple items, see the ListItems command.
New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data/v1/projects/:project_id/items/:item_id
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

item_id
string
The unique identifier of an item.
Request
Query String Parameters
includePathInProject
boolean
Specify whether to return pathInProject attribute in response for BIM 360 Docs projects. pathInProject is the relative path of the item starting from project’s root folder.
true: response will include pathInProject attribute for BIM 360 Docs projects.

false (default): response will not include pathInProject attribute for BIM 360 Docs projects.

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
curl -v 'https://developer.api.autodesk.com/data/v1/projects/:project_id/items/:item_id' \
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
Items
GET	projects/:project_id/items/:item_id/parent
Returns the "parent" folder for the given item.

New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data/v1/projects/:project_id/items/:item_id/parent
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

item_id
string
The unique identifier of an item.
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
curl -v 'https://developer.api.autodesk.com/data/v1/projects/:project_id/items/:item_id/parent' \
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
Items
GET	projects/:project_id/items/:item_id/refs
Returns the resources (items, folders, and versions) that have a custom relationship with the given item_id. Custom relationships can be established between an item and other resources within the data domain service (folders, items, and versions).

Notes:

Each relationship is defined by the id of the object at the other end of the relationship, together with type, attributes, and relationships links.
Callers will typically use a filter parameter to restrict the response to the custom relationship types (filter[meta.refType]) they are interested in.
The response body will have an included array which contains the ref resources that are involved in the relationship, which is essentially the GET projects/:project_id/items/:item_id/relationships/refs endpoint.
New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data/v1/projects/:project_id/items/:item_id/refs
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

item_id
string
The unique identifier of an item.
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
curl -v 'https://developer.api.autodesk.com/data/v1/projects/:project_id/items/:item_id/refs' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "/data/v1/projects/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjEjMjAyMzAzMTcwMDAwMDAx/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/refs"
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
}

Documentation /Data Management API /Reference Guide
Items
GET	projects/:project_id/items/:item_id/relationships/links
Returns a collection of links for the given item_id. Custom relationships can be established between an item and other external resources residing outside the data domain service. A link’s href defines the target URI to access a resource.

New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data/v1/projects/:project_id/items/:item_id/relationships/links
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

item_id
string
The unique identifier of an item.
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
curl -v 'https://developer.api.autodesk.com/data/v1/projects/:project_id/items/:item_id/relationships/links' \
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
Items
GET	projects/:project_id/items/:item_id/relationships/refs
Returns the custom relationships that are associated with the given item_id. Custom relationships can be established between an item and other resources within the data domain service (folders, items, and versions).

Notes:

Each relationship is defined by the id of the object at the other end of the relationship, together with type, specific reference meta including extension data.
Callers will typically use a filter parameter to restrict the response to the custom relationship types (filter[meta.refType]) they are interested in.
The response body will have an included array which contains the resources that are involved in the relationship, which is essentially the GET projects/:project_id/items/:item_id/refs endpoint.
New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data/v1/projects/:project_id/items/:item_id/relationships/refs
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

item_id
string
The unique identifier of an item.
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
curl -v 'https://developer.api.autodesk.com/data/v1/projects/:project_id/items/:item_id/relationships/refs' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "/data/v1/projects/b.5ae9543e-abd5-45c5-8718-33d26652267f/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/relationships/refs"
    },
    "related": {
      "href": "/data/v1/projects/b.5ae9543e-abd5-45c5-8718-33d26652267f/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/refs"
    }
  },
  "data": [
    {
      "type": "items",
      "id": "urn:adsk.wipprod:fs.file:vf.b909RzMKR4mhc3O7UBY_8g?version=2",
      "meta": {
        "refType": "xrefs",
        "fromId": "urn:adsk.wipprod:fs.file:vf.b909RzMKR4mhc3O7UBY_8g?version=2",
        "fromType": "versions",
        "toId": "urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g",
        "toType": "items",
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
        "reservedTime": "2016-04-01T11:10:00.000Z",
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
Items
GET	projects/:project_id/items/:item_id/tip
Returns the “tip” version for the given item. Multiple versions of a resource item can be uploaded in a project. The tip version is the most recent one.

New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data/v1/projects/:project_id/items/:item_id/tip
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

item_id
string
The unique identifier of an item.
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
curl -v 'https://developer.api.autodesk.com/data/v1/projects/:project_id/items/:item_id/tip' \
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
}

Documentation /Data Management API /Reference Guide
Items
GET	projects/:project_id/items/:item_id/versions
Returns versions for the given item. Multiple versions of a resource item can be uploaded in a project.

New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/data/v1/projects/:project_id/items/:item_id/versions
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

item_id
string
The unique identifier of an item.
Request
Query String Parameters
filter[id]
array: string
Filter by the id of the ref target.
filter[extension.type]
array: string
Filter by the extension type.
filter[versionNumber]
array: integer: int32
Filter by versionNumber.
page[number]
int
Specifies what page to return. Page numbers start at 0, so the first page is page 0.
page[limit]
int
Specifies the maximum number of elements to return in the page. The default value is 200. The min value is 1. The max value is 200.
Response
HTTP Status Code Summary
200
OK
Successful retrieval of the versions collection associated with a specific item.
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
The array of version objects.
Example
Successful retrieval of the versions collection associated with a specific item.

Request
curl -v 'https://developer.api.autodesk.com/data/v1/projects/:project_id/items/:item_id/versions' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g/versions?page%5Bnumber%5D=3"
    },
    "first": {
      "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g/versions?page%5Bnumber%5D=0"
    },
    "prev": {
      "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g/versions?page%5Bnumber%5D=2"
    },
    "next": {
      "href": "/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn%3Aadsk.wipprod%3Afs.file%3Avf.b909RzMKR4mhc3O7UBY_8g/versions?page%5Bnumber%5D=4"
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
    }
  ]
}

以下是versions api :

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
}

Documentation /Data Management API /Reference Guide
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
}

Documentation /Data Management API /Reference Guide
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
}

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
}

Documentation /Data Management API /Reference Guide
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

Commands 相關：

Documentation /Data Management API /Reference Guide
Commands
CheckPermission
Checks if a user has permission to perform specified actions on specified resources.

The user’s identity is derived from the x-user-id header parameter (in a 2-Legged call), or from the Authorization Bearer token (in a 3-Legged call). The actions being checked for and the resources are specified in the JSON payload sent with the request. The resources can be folders, items, or even specified versions of an item.

The JSON response contains an array named permissions, where each element represents a resource that was checked. Each element of the array contains a permission attribute, which becomes true only if the user is permitted to perform all the specified actions for that resource. It becomes false even if one action is not permitted. To determine what action was not permitted, inspect the details object.

You can check up to 50 resources at a time.

The terms used to identify permitted actions by the CheckPermission command can be different from the terms used by the product you usually interact with. For example, the term Admin, which is used by the CheckPermissions command, is referred to as Manage by Fusion 360.

The following table shows which BIM 360 actions you can check for and the equivalent CheckPermission terminology. Note that the command checks for all possible actions assigned to the user, including actions associated with the roles and companies assigned to the user.

BIM 360 Action	CheckPermission Terms
view	view
download	download
upload	upload
collaborate	collaborate
edit	create, updateMetaData
full control	admin
For information about which actions are assigned to different BIM 360 permission levels, see the Help documentation.

The following table compares the terms used by BIM 360 Team, Fusion Team, and A360 Personal with the terms used by the CheckPermissions command.

BIM360 Team, Fusion Team, A360 Personal Term		CheckPermission Term
read
(Download and view specified resource)
read
download
view
(View specified resource without downloading)
view
collaborate
(Add comments to the specified resource)
collaborate
write
(Write and upload to the specified resource)
write
create
upload
updateMetaData
delete
(Delete the specified resource)
delete
manage
(Perform administrative operations on specified resource)
admin
share
(Share the specified resource)
share
Note: CheckPermission is a Data Management command. Unlike typical CRUD operations, commands let you perform complex operations on multiple resources. For more details see Commands .

New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/data/v1/projects/:project_id/commands
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
Must be Bearer <token>, where <token> is obtained by means of a two-legged or three-legged OAuth flow.
x-user-id
string
In a two-legged authentication context, the app has access to all users specified by the administrator in the SaaS integrations UI. By providing this header, the API call is limited to act only on behalf of the specified user.
Content-Type*
string
Must be application/vnd.api+json.
* Required
Request
URI Parameters
project_id
string
The unique identifier of a project.
For BIM 360 Docs, the project ID in the Data Management API corresponds to the project ID in the BIM 360 API. To convert a project ID in the BIM 360 API into a project ID in the Data Management API you need to add a “b." prefix. For example, a project ID of c8b0c73d-3ae9 translates to a project ID of b.c8b0c73d-3ae9.

Request
Body Structure
The POST body is a JSON object with the following attributes.

 Expand all
jsonapi*
object
The JSON API object.
data*
object
The data object.
* Required
Response
HTTP Status Code Summary
200
OK
Successful execution of a command.
400
Bad Input
The request could not be understood by the server due to malformed syntax or missing request headers. The client SHOULD NOT repeat the request without modifications. The response body may give an indication of what is wrong with the request.
403
Forbidden
The request was successfully validated but permission is not granted or the application has not been white-listed. Do not try again unless you solve permissions first.
404
Not Found
The specified resource was not found.
Response
Body Structure (200)
A successful response returns a JSON object with the following attributes.

 Expand all
jsonapi
object
The JSON API object.
data
object
The object containing information on the command.
Example
Successful Execution of CheckPermission (200)

Request
curl  -X POST "https://developer.api.autodesk.com/data/v1/projects/a.ZXhhbXBsZTp3aXAxZnFhYXV0b2Rlc2sxNjEjMjAyMzAzMTcwMDAwMDAx/commands/" \
  -H "Authorization: Bearer kEnG562yz5bhE9igXf2YTcZ2bu0z" \
  -H "Content-Type: application/vnd.api+json" \
  -d ' \
      {
         "jsonapi":{
            "version":"1.0"
         },
         "data":{
            "type":"commands",
            "attributes":{
               "extension":{
                  "type":"commands:autodesk.core:CheckPermission",
                  "version":"1.0.0",
                  "data":{
                     "requiredActions":[
                        "download",
                        "view",
                        "write"
                     ]
                  }
               }
            },
            "relationships":{
               "resources":{
                  "data":[
                     {
                        "type":"folders",
                        "id":"urn:adsk.wipprod:dm.folder:hC6k4hndRWaeIVhIjvHu8w"
                     },
                     {
                        "type":"folders",
                        "id":"urn:adsk.wipprod:dm.folder:iC6k4hndRW5eIVhIjvHu8n"
                     },
                     {
                        "type":"folders",
                        "id":"urn:adsk.wipprod:dm.folder:jC6k4hndRW5eIVhIjvHu9x"
                     }
                  ]
               }
            }
         }
      }'
Show Less
Response
{
  "data": {
    "type": "commands",
    "id": "d3bbe753-ae0a-450d-bbe3-cfd4648f0437",
    "attributes": {
      "extension": {
        "data": {
          "permissions": [
            {
              "type": "folders",
              "id": "urn:adsk.wipprod:dm.folder:hC6k4hndRWaeIVhIjvHu8w",
              "details": {
                "create": true,
                "download": true,
                "view": true
              },
              "permission": true
            },
            {
              "type": "folders",
              "id": "urn:adsk.wipprod:dm.folder:iC6k4hndRW5eIVhIjvHu8n",
              "details": {
                "create": false,
                "download": true,
                "view": true
              },
              "permission": false
            },
            {
              "type": "folders",
              "id": "urn:adsk.wipprod:dm.folder:jC6k4hndRW5eIVhIjvHu9x",
              "details": {
                "create": false,
                "download": false,
                "view": false
              },
              "permission": false
            }
          ],
          "requiredActions": [
            "create",
            "download",
            "view"
          ]
        },
        "version": "1.0.0",
        "type": "commands:autodesk.core:CheckPermission",
        "schema": { "href": "https://developer.api.autodesk.com/schema/v1/versions/commands:autodesk.core:CheckPermission-1.0.0" }
      }
    },
    "relationships": {
        "resources": {
          "data": [
            {
              "type": "folders",
              "id": "urn:adsk.wipprod:dm.folder:hC6k4hndRWaeIVhIjvHu8w"
            },
            {
              "type": "folders",
              "id": "urn:adsk.wipprod:dm.folder:iC6k4hndRW5eIVhIjvHu8n"
            },
            {
              "type": "folders",
              "id": "urn:adsk.wipprod:dm.folder:jC6k4hndRW5eIVhIjvHu9x"
            }
          ]
        }
    }
  },
  "jsonapi": {
    "version": "1.0"
  }
}

Documentation /Data Management API /Reference Guide
Commands
ListRefs
Retrieves the custom relationships between specified versions of items and other resources in the data domain service (folders, items, and versions). You can retrieve the relationships of up to 50 versions.

Note that ListRefs is a Data Management command. Commands enable you to perform complex operations on multiple resources rather than standard CRUD operations. For more details about commands, see the Commands overview section.

New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/data/v1/projects/:project_id/commands
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
Content-Type*
string
Must be application/vnd.api+json.
* Required
Request
URI Parameters
project_id
string
The unique identifier of a project.
For BIM 360 Docs, the project ID in the Data Management API corresponds to the project ID in the BIM 360 API. To convert a project ID in the BIM 360 API into a project ID in the Data Management API you need to add a “b." prefix. For example, a project ID of c8b0c73d-3ae9 translates to a project ID of b.c8b0c73d-3ae9.

Request
Body Structure
The POST body is a JSON object with the following attributes.

 Expand all
jsonapi*
object
The JSON API object.
data*
object
The data object.
* Required
Response
HTTP Status Code Summary
200
OK
Successful execution of a command.
400
Bad Input
The request could not be understood by the server due to malformed syntax or missing request headers. The client SHOULD NOT repeat the request without modifications. The response body may give an indication of what is wrong with the request.
403
Forbidden
The request was successfully validated but permission is not granted or the application has not been white-listed. Do not try again unless you solve permissions first.
404
Not Found
The specified resource was not found.
Response
Body Structure (200)
A successful response returns a JSON object with the following attributes.

 Expand all
jsonapi
object
The JSON API object.
data
object
The data object.
included
array: object
List of relationships for each version that was passed in data.relationships.resources.data.
Example
Successful Execution of a Command (200)

Request
curl -X POST -H "Authorization: Bearer kEnG562yz5bhE9igXf2YTcZ2bu0z" -H "Content-Type: application/vnd.api+json" -d '
{
    "jsonapi": {
        "version": "1.0"
    },
    "data": {
        "type": "commands",
        "attributes": {
            "extension": {
                "type": "commands:autodesk.core:ListRefs",
                "version": "1.0.0"
            }
        },
        "relationships": {
            "resources": {
                "data": [
                    {
                        "type": "versions",
                        "id": "urn:adsk.wipqa:fs.file:vf.3pGffROYQx6efm0eR26DEg?version=1"
                    }
                ]
            }
        }
    }
}' "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/commands/"
Show Less
Response
{
    "jsonapi": {
        "version": "1.0"
    },
    "data": {
        "type": "commands",
        "id": "61f0f2fe-a71f-4004-a5e4-de0ce2cd968c",
        "attributes": {
            "status": "complete",
            "extension": {
                "type": "commands:autodesk.core:ListRefs",
                "version": "1.0.0"
            }
        },
        "relationships": {
            "resources": {
                "data": [
                    {
                        "type": "versions",
                        "id": "urn:adsk.wipqa:fs.file:vf.3fcaI3iqS56R8OHUMdDSdg?version=1",
                        "meta": {
                            "refType": "derived",
                            "fromId": "urn:adsk.wipqa:fs.file:vf.3fcaI3iqS56R8OHUMdDSdg?version=1",
                            "fromType": "versions",
                            "toId": "urn:adsk.wipqa:fs.file:vf.3pGffROYQx6efm0eR26DEg?version=1",
                            "toType": "versions",
                            "direction": "to",
                            "extension": {
                                "type": "derived:autodesk.bim360:FileToDocument",
                                "version": "1.0",
                                "schema": {
                                    "href": "https://developer.api.autodesk.com/schema/v1/versions/derived:autodesk.bim360:FileToDocument-1.0"
                                },
                                "data": {}
                            }
                        }
                    }
                ]
            }
        }
    },
    "included": [
        {
            "type": "items",
            "id": "urn:adsk.wipqa:dm.lineage:3pGffROYQx6efm0eR26DEg",
            "attributes": {
                "displayName": "",
                "hidden": false,
                "reserved": false,
                "extension": {
                    "type": "items:autodesk.bim360:Document",
                    "version": "1.0",
                    "schema": {
                        "href": "https://developer.api.autodesk.com/schema/v1/versions/items:autodesk.bim360:Document-1.0"
                    },
                    "data": {}
                }
            },
            "links": {
                "self": {
                    "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipqa:dm.lineage:3pGffROYQx6efm0eR26DEg"
                },
                "webView": {
                    "href": "https://docs.b360.autodesk.com/projects/c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Afs.folder%3Aco.0J4paz_FQgWPX2QRsaBkiw/detail/viewer/items/urn:adsk.wipqa:dm.lineage:3pGffROYQx6efm0eR26DEg"
                }
            }
        },
        {
            "type": "items",
            "id": "urn:adsk.wipqa:dm.lineage:3fcaI3iqS56R8OHUMdDSdg",
            "attributes": {
                "displayName": "BD4359-A-SK035-009_WC_Mock-up_Plan.pdf",
                "hidden": false,
                "reserved": false,
                "extension": {
                    "type": "items:autodesk.bim360:File",
                    "version": "1.0",
                    "schema": {
                        "href": "https://developer.api.autodesk.com/schema/v1/versions/items:autodesk.bim360:File-1.0"
                    },
                    "data": {}
                }
            },
            "links": {
                "self": {
                    "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipqa:dm.lineage:3fcaI3iqS56R8OHUMdDSdg"
                }
            }
        },
        {
            "type": "versions",
            "id": "urn:adsk.wipqa:fs.file:vf.3pGffROYQx6efm0eR26DEg?version=1",
            "attributes": {
                "name": "SK035 INFORMATION",
                "displayName": "SK035 INFORMATION",
                "versionNumber": 1,
                "extension": {
                    "type": "versions:autodesk.bim360:Document",
                    "version": "1.0",
                    "schema": {
                        "href": "https://developer.api.autodesk.com/schema/v1/versions/versions:autodesk.bim360:Document-1.0"
                    },
                    "data": {
                        "processState": "PROCESSING_COMPLETE",
                        "viewableId": "1",
                        "viewableGuid": "bcd84049-3c9a-469f-b053-40cd535fe883",
                        "viewableName": "1",
                        "viewableOrder": 1
                    }
                }
            },
            "links": {
                "self": {
                    "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn:adsk.wipqa:fs.file:vf.3pGffROYQx6efm0eR26DEg%3Fversion=1"
                }
            }
        },
        {
            "type": "versions",
            "id": "urn:adsk.wipqa:fs.file:vf.3fcaI3iqS56R8OHUMdDSdg?version=1",
            "attributes": {
                "name": "BD4359-A-SK035-009_WC_Mock-up_Plan.pdf",
                "displayName": "BD4359-A-SK035-009_WC_Mock-up_Plan.pdf",
                "versionNumber": 1,
                "storageSize": 46197,
                "fileType": "pdf",
                "extension": {
                    "type": "versions:autodesk.bim360:File",
                    "version": "1.0",
                    "schema": {
                        "href": "https://developer.api.autodesk.com/schema/v1/versions/versions:autodesk.bim360:File-1.0"
                    },
                    "data": {
                        "processState": "PROCESSING_COMPLETE",
                        "extractionState": "SUCCESS",
                        "splittingState": "SPLIT",
                        "reviewState": "ACCEPTED",
                        "revisionDisplayLabel": "1"
                    }
                }
            },
            "links": {
                "self": {
                    "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn:adsk.wipqa:fs.file:vf.3fcaI3iqS56R8OHUMdDSdg%3Fversion=1"
                }
            }
        }
    ]
}

Documentation /Data Management API /Reference Guide
Commands
ListItems
Retrieves metadata for up to 50 specified items. For example, an item name, or the date it was created. It returns the tip (latest) version of the items.

Note that ListItems is a Data Management command. Commands enable you to perform complex operations on multiple resources rather than standard CRUD operations. For more details about commands, see the Commands overview section.

New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/data/v1/projects/:project_id/commands
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
Content-Type*
string
Must be application/vnd.api+json.
* Required
Request
URI Parameters
project_id
string
The unique identifier of a project.
For BIM 360 Docs, the project ID in the Data Management API corresponds to the project ID in the BIM 360 API. To convert a project ID in the BIM 360 API into a project ID in the Data Management API you need to add a “b." prefix. For example, a project ID of c8b0c73d-3ae9 translates to a project ID of b.c8b0c73d-3ae9.

Request
Body Structure
The POST body is a JSON object with the following attributes.

 Expand all
jsonapi*
object
The JSON API object.
data*
object
The data object.
* Required
Response
HTTP Status Code Summary
200
OK
Successful execution of a command.
400
Bad Input
The request could not be understood by the server due to malformed syntax or missing request headers. The client SHOULD NOT repeat the request without modifications. The response body may give an indication of what is wrong with the request.
403
Forbidden
The request was successfully validated but permission is not granted or the application has not been white-listed. Do not try again unless you solve permissions first.
404
Not Found
The specified resource was not found.
Response
Body Structure (200)
A successful response returns a JSON object with the following attributes.

 Expand all
jsonapi
object
The JSON API object.
data
object
The data object.
included
array:object
List of metadata for the tip (latest) version of each item.
Example
Successful Execution of a Command (200)

Request
curl -X POST -v "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/commands" -H "Authorization: Bearer kEnG562yz5bhE9igXf2YTcZ2bu0z" -H "Content-Type: application/vnd.api+json" -d '
{
  "jsonapi": {
    "version": "1.0"
  },
  "data": {
    "type": "commands",
    "attributes": {
      "extension": {
        "type": "commands:autodesk.core:ListItems",
        "version": "1.1.0",
        "data": {
          "includePathInProject": true
        }
      }
    },
    "relationships": {
      "resources": {
        "data": [
          {
            "type": "items",
            "id": "urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g"
          }
        ]
      }
    }
  }
}'
Show Less
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "data": {
    "type": "commands",
    "id": "fa214233-abef-4c48-a3de-253bde80cfe4",
    "attributes": {
      "status": "complete",
      "extension": {
        "type": "commands:autodesk.core:ListItems",
        "version": "1.0.0"
      }
    },
    "relationships": {
      "resources": {
        "data": [
          {
            "type": "items",
            "id": "urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g",
            "meta": {
              "type": "items",
              "id": "urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g",
              "attributes": {
                "displayName": "version-test",
                "createTime": "2016-04-01T11:09:03.000Z",
                "createUserId": "BW9RM76WZBGL",
                "createUserName": "Eason Kang",
                "lastModifiedTime": "2016-04-01T11:11:18.000Z",
                "lastModifiedUserId": "BW9RM76WZBGL",
                "lastModifiedUserName": "Eason Kang",
                "hidden": false,
                "reserved": false,
                "extension": {
                  "type": "items:autodesk.bim360:File",
                  "version": "1.0",
                  "schema": {
                    "href": "https://developer.api.autodesk.com/schema/v1/versions/items:autodesk.bim360:File-1.0"
                  },
                  "data": {

                  }
                },
                "pathInProject": "/Project Files/ExampleFolder/SubFolder/4d7daeda-6g7a-4aac-a52a-158833233da3"
              },
              "links": {
                "self": {
                  "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g"
                },
                "webView": {
                  "href": "https://docs.b360.autodesk.com/projects/c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Afs.folder%3Aco.0J4paz_FQgWPX2QRsaBkiw/detail/viewer/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g"
                }
              },
              "relationships": {
                "tip": {
                  "data": {
                    "type": "versions",
                    "id": "urn:adsk.wipprod:fs.file:vf.wX8PdF8GSa27Zw-Vgd939Q?version=1"
                  },
                  "links": {
                    "related": {
                      "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/tip"
                    }
                  }
                },
                "versions": {
                  "links": {
                    "related": {
                      "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/versions"
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
                      "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/parent"
                    }
                  }
                },
                "refs": {
                  "links": {
                    "self": {
                      "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/relationships/refs"
                    },
                    "related": {
                      "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/refs"
                    }
                  }
                },
                "links": {
                  "links": {
                    "self": {
                      "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/items/urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g/relationships/links"
                    }
                  }
                }
              }
            }
          }
        ]
      }
    }
  },
  "included": [
    {
      "type": "versions",
      "id": "urn:adsk.wipprod:fs.file:vf.d34fdsg3g?version=2",
      "attributes": {
        "name": "version-test.pdf",
        "displayName": "version-test",
        "createTime": "2016-04-01T11:09:03.000Z",
        "createUserId": "BW9RM76WZBGL",
        "createUserName": "Eason Kang",
        "lastModifiedTime": "2016-04-01T11:11:18.000Z",
        "lastModifiedUserId": "BW9RM76WZBGL",
        "lastModifiedUserName": "Eason Kang",
        "versionNumber": 1,
        "fileType": "pdf",
        "extension": {
          "type": "versions:autodesk.bim360:File",
          "version": "1.0",
          "schema": {
            "href": "https://developer.api.autodesk.com/schema/v1/versions/versions:autodesk.bim360:File-1.0"
          },
          "data": {
            "processState": "PROCESSING_COMPLETE",
            "extractionState": "SUCCESS",
            "splittingState": "SPLIT",
            "reviewState": "ACCEPTED",
            "revisionDisplayLabel": "1"
          }
        }
      },
      "links": {
        "self": {
          "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn:adsk.wipprod:fs.file:vf.d34fdsg3g?version=2"
        },
        "webView": {
          "href": "https://docs.b360.autodesk.com/projects/c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/folders/urn%3Aadsk.wipprod%3Afs.folder%3Aco.0J4paz_FQgWPX2QRsaBkiw/detail/viewer/items/urn:adsk.wipprod:fs.file:vf.d34fdsg3g%3Fversion%3D2"
        }
      },
      "relationships": {
        "item": {
          "data": {
            "type": "items",
            "id": "urn:adsk.wipprod:dm.lineage:b909RzMKR4mhc3O7UBY_8g"
          },
          "links": {
            "related": {
              "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn:adsk.wipprod:fs.file:vf.d34fdsg3g?version=2/item"
            }
          }
        },
        "links": {
          "links": {
            "self": {
              "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn:adsk.wipprod:fs.file:vf.d34fdsg3g?version=2/relationships/links"
            }
          }
        },
        "refs": {
          "links": {
            "self": {
              "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn:adsk.wipprod:fs.file:vf.d34fdsg3g?version=2/relationships/refs"
            },
            "related": {
              "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn:adsk.wipprod:fs.file:vf.d34fdsg3g?version=2/refs"
            }
          }
        },
        "downloadFormats": {
          "links": {
            "related": {
              "href": "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/versions/urn:adsk.wipprod:fs.file:vf.d34fdsg3g?version=2/downloadFormats"
            }
          }
        },
        "derivatives": {
          "data": {
            "type": "derivatives",
            "id": "dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLmQzNGZkc2czZw_dmVyc2lvbj0x"
          },
          "meta": {
            "link": {
              "href": "https://developer.api.autodesk.com/modelderivative/v2/designdata/dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLmQzNGZkc2czZw_dmVyc2lvbj0x/manifest"
            }
          }
        },
        "thumbnails": {
          "data": {
            "type": "thumbnails",
            "id": "dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLmQzNGZkc2czZw_dmVyc2lvbj0x"
          },
          "meta": {
            "link": {
              "href": "https://developer.api.autodesk.com/modelderivative/v2/designdata/dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLmQzNGZkc2czZw_dmVyc2lvbj0x/thumbnail"
            }
          }
        },
        "storage": {
          "data": {
            "type": "objects",
            "id": "urn:adsk.objects:os.object:wip.dm.prod/3c8f6bbc-fe5c-4815-a92e-8b8635e7b1cb.pdf"
          },
          "meta": {
            "link": {
              "href": "https://developer.api.autodesk.com/oss/v2/buckets/wip.dm.prod/objects/3c8f6bbc-fe5c-4815-a92e-8b8635e7b1cb.pdf"
            }
          }
        }
      }
    }
  ]
}

Documentation /Data Management API /Reference Guide
Commands
GetPublishModelJob
Verifies whether a Collaboration for Revit (C4R) model needs to be published to BIM 360 Docs.

Before using this command you need to:

Initiate collaboration through Revit, and select BIM 360 Docs. This creates the first version in BIM 360 Docs.
Modify the model locally, and synchronize the changes with the central model.
Every time you synchronize the current model with the central model, it sets the data attribute to null. When you publish the latest version to BIM 360 Docs (using the PublishModel command), it sets the status to processing or complete.

To publish the model to BIM 360 Docs, use the the PublishModel command.

For more details about the workflow for using the GetPublishModelJob command, see the Publish a C4R Model to BIM 360 Docs tutorial.

Note that GetPublishModelJob is a Data Management command. Commands enable you to perform complex operations on multiple resources rather than standard CRUD operations. For more details about commands, see the Commands overview section.

New! Autodesk Construction Cloud platform (ACC). Note that this endpoint is compatible with ACC projects. For more information about the Autodesk Construction Cloud APIs, see the Autodesk Construction Cloud documentation.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/data/v1/projects/:project_id/commands
Authentication Context	
user context required
Required OAuth Scopes	
data:read
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via either a two-legged or three-legged OAuth flow. Note that it will not accept a two-legged token, unless you add the x-user-id header.
x-user-id
string
In a two-legged authentication context, the app has access to all users specified by the administrator in the SaaS integrations UI. By providing this header, the API call will be limited to act on behalf of only the user specified.
Content-Type*
string
Must be application/vnd.api+json.
* Required
Note that for a three-legged OAuth flow or for a two-legged OAuth flow with user impersonation (x-user-id), the user must have at least view permission for the BIM 360 Docs folder you publish the model to.

Request
URI Parameters
project_id
string
The unique identifier of a project.
For BIM 360 Docs, the project ID in the Data Management API corresponds to the project ID in the BIM 360 API. To convert a project ID in the BIM 360 API into a project ID in the Data Management API you need to add a “b." prefix. For example, a project ID of c8b0c73d-3ae9 translates to a project ID of b.c8b0c73d-3ae9.

Request
Body Structure
The POST body is a JSON object with the following attributes.

 Expand all
jsonapi*
object
The JSON API object.
data*
object
The data object.
* Required
Response
HTTP Status Code Summary
200
OK
Successful execution of a command.
400
Bad Input
The request could not be understood by the server due to malformed syntax or missing request headers. The client SHOULD NOT repeat the request without modifications. The response body may give an indication of what is wrong with the request.
403
Forbidden
The request was successfully validated but permission is not granted or the application has not been white-listed. Do not try again unless you solve permissions first.
404
Not Found
The specified resource was not found.
Response
Body Structure (200)
Note that if you have updated the central model, the data attribute is set to null until you publish it. See the Examples below.

A successful response returns a JSON object with the following attributes.

 Expand all
jsonapi
object
The JSON API object.
data
object
The data object.
Example 1
Successful Retrieval of C4R Model Publish Status (200)

Request
  curl -X POST -v "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/commands/" -H "Authorization: Bearer kEnG562yz5bhE9igXf2YTcZ2bu0z" -H "Content-Type: application/vnd.api+json" -d '
  {
    "jsonapi": {
      "version": "1.0"
    },
    "data": {
      "type": "commands",
      "attributes": {
        "extension": {
          "type": "commands:autodesk.bim360:C4RModelGetPublishJob",
          "version": "1.0.0"
      }
    },
    "relationships": {
      "resources": {
        "data": [ { "type": "items", "id": "urn:adsk.wip:dm.file:hC6k4hndRWaeIVhIjvHu8w" } ]
      }
    }
  }
}'
Show Less
Response
{
  "data": {
    "type": "commands",
    "id": "d3bbe753-ae0a-450d-bbe3-cfd4648f0437",
    "attributes": {
      "status" : "complete",
      "extension": {
        "type": "commands:autodesk.bim360:C4RModelGetPublishJob",
        "version": "1.0.0"
      }
    }
  },
  "jsonapi": {
    "version": "1.0"
  }
}
Show Less
Example 2
Successful Retrieval of C4R Publish Status - Model Needs Publishing (200)

Note that if you have updated the central model, the data attribute is set to null until you publish it.

Request
  curl -X POST -v "https://developer.api.autodesk.com/data/v1/projects/b.c2960674-2d1e-4cc8-a5f0-4b9026fd3f5d/commands/" -H "Authorization: Bearer kEnG562yz5bhE9igXf2YTcZ2bu0z" -H "Content-Type: application/vnd.api+json" -d '
  {
    "jsonapi": {
      "version": "1.0"
    },
    "data": {
      "type": "commands",
      "attributes": {
        "extension": {
          "type": "commands:autodesk.bim360:C4RModelGetPublishJob",
          "version": "1.0.0"
      }
    },
    "relationships": {
      "resources": {
        "data": [ { "type": "items", "id": "urn:adsk.wip:dm.file:hC6k4hndRWaeIVhIjvHu8w" } ]
      }
    }
  }
}'
Show Less
Response
{
  "data": null
  "jsonapi": {
    "version": "1.0"
  }
}

OSS - BUCKETS API:

Documentation /Data Management API /Reference Guide
Buckets
GET	buckets
This endpoint will return the buckets owned by the application. This endpoint supports pagination.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/oss/v2/buckets
Authentication Context	
app-only
Required OAuth Scopes	
bucket:read
Data Format	
JSON
Request
Headers
Authorization*
string
Must be “Bearer <token>”, where <token> is obtained via POST token.
region
enum
The region where the buckets reside. Possible values:

- US - (Default) Data center for the US region.
- EMEA - Data center for the Europe, Middle East, and Africa regions.
- AUS - (Beta) Data center for the Australia region.
- CAN - Data centre for the Canada region.
- DEU - Data centre for the Germany region.
- IND - Data centre for the India region.
- JPN - Data centre for the Japan region.
- GBR - Data centre for the United Kingdom region.

Note:

1. Beta features are subject to change. Please avoid using them in production environments.
2. If you specify the region header as well as the region query parameter, the region header takes precedence.
* Required
Request
Query String Parameters
region
enum
The region where the buckets reside. Possible values:

- US - (Default) Data center for the US region.
- EMEA - Data center for the Europe, Middle East, and Africa regions.
- AUS - (Beta) Data center for the Australia region.
- CAN - Data centre for the Canada region.
- DEU - Data centre for the Germany region.
- IND - Data centre for the India region.
- JPN - Data centre for the Japan region.
- GBR - Data centre for the United Kingdom region.

Note:

1. Beta features are subject to change. Please avoid using them in production environments.
2. If you specify the region header as well as the region query parameter, the region header takes precedence.
limit
int
Limit to the response size,
Acceptable values: 1-100 Default = 10
startAt
string
Key to use as an offset to continue pagination This is typically the last bucket key found in a preceding GET buckets response
Response
HTTP Status Code Summary
200
OK
400
BAD REQUEST
The request could not be understood by the server due to malformed syntax or missing request headers. The client SHOULD NOT repeat the request without modifications. The response body may give an indication of what is wrong with the request.
401
UNAUTHORIZED
The supplied authorization header was not valid or the supplied token scope was not acceptable. Verify authentication and try again.
403
FORBIDDEN
Caller is not authorized to call this endpoint.
404
NOT FOUND
Resource not found.
500
INTERNAL SERVER ERROR
Internal failure while processing the request, reason depends on error.
Response
Body Structure (200)
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "items": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "bucketKey": {
            "type": "string"
          },
          "createDate": {
            "type": "integer"
          },
          "policyKey": {
            "type": "string"
          }
        },
        "required": [
          "bucketKey",
          "createDate",
          "policyKey"
        ]
      }
    },
    "next": {
      "type": "string"
    }
  },
  "required": [
    "items",
    "next"
  ]
}
Show More
items
array(buckets)
Array of items representing the buckets
bucketKey
string
Bucket key
createdDate
long
Timestamp in epoch time
policyKey
string
Policy values: transient, temporary, persistent
next
string
Next possible request
Example 1
Basic Successful List Bucket (200)

Request
curl -v "https://developer.api.autodesk.com/oss/v2/buckets"
  -X GET
  -H "Authorization: Bearer RhS6iEVMnEfl77MBSK3l2je06UHj"
Response
HTTP/1.1 200 OK
Access-Control-Allow-Credentials: true
Access-Control-Allow-Headers: Authorization, Accept-Encoding, Range, Content-Type
Access-Control-Allow-Methods: GET
Access-Control-Allow-Origin: *
Content-Type: application/json; charset=utf-8
Date: Wed, 25 May 2016 15:40:37 GMT
Server: Apigee Router
Content-Length: 1273
Connection: keep-alive
{
  "items" : [ {
    "bucketKey" : "00001fbf-8505-49ab-8a42-44c6a96adbd0",
    "createdDate" : 1441329298362,
    "policyKey" : "transient"
  }, {
    "bucketKey" : "0003114d",
    "createdDate" : 1440119769765,
    "policyKey" : "transient"
  }, {
    "bucketKey" : "0003fbc1-389a-4194-915a-38313797d753",
    "createdDate" : 1453886285506,
    "policyKey" : "transient"
  }, {
    "bucketKey" : "00048aa5",
    "createdDate" : 1436255268102,
    "policyKey" : "transient"
  }, {
    "bucketKey" : "000524bf",
    "createdDate" : 1453197455111,
    "policyKey" : "transient"
  }, {
    "bucketKey" : "0006db6d",
    "createdDate" : 1461978883040,
    "policyKey" : "transient"
  }, {
    "bucketKey" : "00074953-5d83-4aeb-b598-8f727703c94e",
    "createdDate" : 1447934893704,
    "policyKey" : "transient"
  }, {
    "bucketKey" : "00085601-78b2-44e4-82f3-a252fde022d2",
    "createdDate" : 1441504885576,
    "policyKey" : "transient"
  }, {
    "bucketKey" : "000b1e61-216e-4480-bcd3-9ec5ca56364f",
    "createdDate" : 1448268266859,
    "policyKey" : "transient"
  }, {
    "bucketKey" : "000e37cc",
    "createdDate" : 1437441338604,
    "policyKey" : "transient"
  } ],
  "next" : "https://developer.api.autodesk.com/oss/v2/buckets?region=US&startAt=000e37cc"
}
Show Less
Example 2
List Bucket - Invalid Limit (400)

Request
curl -v "https://developer.api.autodesk.com/oss/v2/buckets?limit=300"
  -X GET
  -H "Authorization: Bearer R4wQlRMQJgAtRG3IeD0IQ2Wwyk8C"
Response
HTTP/1.1 400 Bad Request
Access-Control-Allow-Credentials: true
Access-Control-Allow-Headers: Authorization, Accept-Encoding, Range, Content-Type
Access-Control-Allow-Methods: GET
Access-Control-Allow-Origin: *
Content-Type: application/json; charset=utf-8
Date: Wed, 25 May 2016 15:44:43 GMT
Server: Apigee Router
Content-Length: 26
Connection: keep-alive

{"reason":"Invalid limit"}

Documentation /Data Management API /Reference Guide
Buckets
GET	buckets/:bucketKey/details
Return bucket details in JSON format if the caller is the owner of the bucket. A request by any other application will result in a response of 403 Forbidden.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/oss/v2/buckets/:bucketKey/details
Authentication Context	
app-only
Required OAuth Scopes	
bucket:read
Data Format	
JSON
Request
Headers
Authorization*
string
Must be “Bearer <token>”, where <token> is obtained via POST token.
* Required
Request
URI Parameters
bucketKey*
string
URL-encoded bucket key for which to get details
* Required
Response
HTTP Status Code Summary
200
OK
Get bucket details was successful.
400
BAD REQUEST
The request could not be understood by the server due to malformed syntax or missing request headers. The client SHOULD NOT repeat the request without modifications. The response body may give an indication of what is wrong with the request.
401
UNAUTHORIZED
The supplied Authorization header was not valid or the supplied token scope was not acceptable. Verify Authentication and try again.
403
FORBIDDEN
The Authorization was successfully validated but permission is not granted. Don’t try again unless you solve permissions first.
404
NOT FOUND
The specified bucket does not exist.
500
INTERNAL SERVER ERROR
Internal failure while processing the request, reason depends on error.
Response
Body Structure (200)
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "bucketKey": {
      "required": true,
      "type": "string"
    },
    "bucketOwner": {
      "required": true,
      "type": "string"
    },
    "createdDate": {
      "required": true,
      "type": "integer"
    },
    "permissions": {
      "required": true,
      "type": "array",
      "items": {
        "type": [
          "object",
          "null"
        ],
        "properties": {
          "authId": {
            "required": true,
            "type": "string"
          },
          "access": {
            "required": true,
            "type": "string"
          }
        }
      }
    },
    "policyKey": {
      "required": true,
      "type": "string"
    }
  }
}
Show More
bucketKey
string
Bucket key
bucketOwner
string
Bucket owner
createdDate
long
Timestamp in epoch time
permissions
array
Representing applications with access granted at create time
authId
string
Application to grant access to
access
enum
Access values: full, read
policyKey
string
Policy values: transient, temporary, persisten
Example 1
Successful Bucket Details (200)

Request
curl -v "https://developer.api.autodesk.com/oss/v2/buckets/apptestbucket/details"
  -X GET
  -H "Authorization: Bearer efxXBK0aTv3MjSSQ6HbDsjnYRmCU"
  -H "Content-Type: application/json"
Response
HTTP/1.1 200 OK
Access-Control-Allow-Credentials: true
Access-Control-Allow-Headers: Authorization, Accept-Encoding, Range, Content-Type
Access-Control-Allow-Methods: GET
Access-Control-Allow-Origin: *
Content-Type: application/json; charset=utf-8
Date: Sat, 21 May 2016 00:17:24 GMT
Server: Apigee Router
Content-Length: 208
Connection: keep-alive

{
  "bucketKey":"apptestbucket",
  "bucketOwner":"RlKffonB1Ex52GlAbb7N8VJwLllOvpqG",
  "createdDate":1463785698600,
  "permissions":[
    {
      "authId":"RlKffonB1Ex52GlAbb7N8VJwLllOvpqG",
      "access":"full"
    }
  ],
  "policyKey":"transient"
}
Show Less
Example 2
Get Bucket Details - Forbidden (403)

If the bucket was created by Application A, and details were requested with a token for Application B, the response will be 403 Forbidden. In this case the token was generated by a different application than the other examples.

Request
curl -v "https://developer.api.autodesk.com/oss/v2/buckets/apptestbucket/details"
  -X GET
  -H "Authorization: Bearer u3Iu4XFKCMAqRguIxVGrHYiCfw4d"
  -H "Content-Type: application/json"
Response
HTTP/1.1 403 Forbidden
Access-Control-Allow-Credentials: true
Access-Control-Allow-Headers: Authorization, Accept-Encoding, Range, Content-Type
Access-Control-Allow-Methods: GET
Access-Control-Allow-Origin: *
Date: Tue, 24 May 2016 20:57:40 GMT
Server: Apigee Router
Content-Length: 0
Connection: keep-alive
Show Less
Example 3
Get Bucket Details - Bucket Not Found (404)

Request
curl -v "https://developer.api.autodesk.com/oss/v2/buckets/app2testbucket/details"
  -X GET
  -H "Authorization: Bearer kgEJWMJitdYbhfxghap8SbZqXMoS"
  -H "Content-Type: application/json"
Response
HTTP/1.1 404 Not Found
Access-Control-Allow-Credentials: true
Access-Control-Allow-Headers: Authorization, Accept-Encoding, Range, Content-Type
Access-Control-Allow-Methods: GET
Access-Control-Allow-Origin: *
Content-Type: application/json; charset=utf-8
Date: Tue, 24 May 2016 21:00:34 GMT
Server: Apigee Router
Content-Length: 29
Connection: keep-alive

{
  "reason":"Bucket not found"
}
還有很多oss相關api沒有記錄。
