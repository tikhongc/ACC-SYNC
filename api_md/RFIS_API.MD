Documentation /Autodesk Construction Cloud APIs /API Reference
RFIs
POST	rfi-search
Retrieves information about all the RFIs (Requests for Information) in a project, including details about their associated comments and attachments.

To retrieve full information for a specific RFI, use GET rfis/:id.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/construction/rfis/v3/projects/:projectId/search:rfis
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
Must be Bearer <token>, where <token> is obtained via a three-legged OAuth flow.
Content-Type*
string
Must be application/json
* Required
Request
URI Parameters
projectId
string
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Request
Body Structure
Search request

 Expand all
limit
int
The number of RFIs to return. Default: 10. Maximum: 200.
offset
int
The number of items to skip before starting the result set. Default: 0.
search
string
Searches for a string in the title, question, and officialResponse fields.
sort
array: object
A list of sort rules to apply. Each item includes a field to sort by and the sort order.
filter
object
A set of optional filters to narrow the results. You can combine multiple filters.
fields
array: string
Specify which attributes to include in the response.
Use this to limit the response to only the fields you need.

For example, fields=id, title.

Response
HTTP Status Code Summary
200
OK
A list of RFIs
400
Bad Request
The parameters are invalid
401
Unauthorized
The provided bearer token is not valid
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation
500
Internal Server Error
An unknown error occurred on the server
Response
Body Structure (200)
 Expand all
results
array: object
The list of RFIs.
pagination
object
The pagination object.
Example
A list of RFIs

Request
curl -v 'https://developer.api.autodesk.com/construction/rfis/v3/projects/:projectId/search:rfis' \
  -X 'POST' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a' \
  -H 'Content-Type: application/json' \
  -d '{
        "limit": 10,
        "offset": 0,
        "search": "HVAC duct routing",
        "sort": [
          {
            "field": "createdAt",
            "order": "DESC"
          }
        ],
        "filter": {
          "status": "draft",
          "officialResponseStatus": "answered",
          "includeHidden": false,
          "assignedTo": [
            "PER8KQPK2JRT"
          ],
          "locations": [
            "AJJASD2-FFE3",
            "JTOEN-FFD33"
          ],
          "createdAt": "2018-08-01T08:56:48.699Z",
          "updatedAt": "2018-08-01T08:56:48.699Z",
          "closedAt": "2018-08-01T08:56:48.699Z",
          "createdBy": [
            "PER8KQPK2JRT"
          ],
          "dueDate": "2018-08-01T08:56:48.699Z",
          "costImpact": "Yes",
          "scheduleImpact": "Yes",
          "priority": "Low",
          "id": [
            "1e6d1d7b-1b1b-4b1b-8b1b-1b1b1b1b1b1b"
          ],
          "reference": "RFI-235-A1",
          "discipline": "Architechural",
          "category": "Constructability",
          "customAttributes": "fd9a1234-aaaa-4444-bbbb-8888aa77ee66: value-id-1",
          "rfiTypeId": [
            "1e6d1d7b-1b1b-4b1b-8b1b-1b1b1b1b1b1b"
          ]
        },
        "fields": [
          "id"
        ]
      }'
Show Less
Response
{
  "results": [
    {
      "id": "31a3f98d-34a8-4d4c-a362-3cc9de44f89c",
      "customIdentifier": "ID-1234",
      "title": "RFI - pipe is not in right place",
      "question": "Where should we put the pipe?",
      "virtualFolderUrn": "urn:adsk.wip:fs.folder:co.1838SAGCQ3SPn7lqOXMaJQ",
      "status": "open",
      "previousStatus": "submitted",
      "workflowType": "US",
      "assignedTo": [
        {
          "id": "PER8KQPK2JRT",
          "type": "user"
        }
      ],
      "managerId": "KOR8KQPK2GHF",
      "constructionManagerId": "ALW8KQPK2PTB",
      "architects": [
        {
          "type": "user",
          "id": "TKG8KQPK2MNB"
        }
      ],
      "reviewers": [
        {
          "type": "user",
          "id": "IKJ8KQPK2WDV"
        }
      ],
      "dueDate": "2018-01-12T13:06:39.216Z",
      "locationDescription": "In the middle of the room.",
      "locations": [
        "AJJASD2-FFE3",
        "JTOEN-FFD33"
      ],
      "commentsCount": 15,
      "officialResponse": "The measurements are correct.",
      "officialResponseStatus": "answered",
      "officialResponseActors": [
        {
          "id": "AJJASD2-FFE3",
          "type": "user"
        },
        {
          "id": "JTOEN-FFD33",
          "type": "user"
        }
      ],
      "officialResponseEditByManagerState": true,
      "respondedAt": "2018-01-12T13:06:39.216Z",
      "respondedBy": "RFV8KQPK2KHF",
      "createdBy": "PER8KQPK2JRT",
      "createdAt": "2018-07-22T15:05:58.033Z",
      "updatedBy": "ZXC8KQPK2CVB",
      "updatedAt": "2018-07-22T15:05:58.033Z",
      "closedAt": "2018-07-22T15:05:58.033Z",
      "closedBy": "SER8KQPK2JRT",
      "containerId": "31a3f98d-34a8-4d4c-a362-3cc9de44f89c",
      "projectId": "31a3f98d-34a8-4d4c-a362-3cc9de44f89c",
      "suggestedAnswer": "The measurements are correct.",
      "coReviewers": [
        {
          "id": "WSX8KQPK2JRMJ",
          "type": "user"
        }
      ],
      "watchers": [
        {
          "id": "PER8KQPK2JRT",
          "type": "user"
        }
      ],
      "answeredAt": "2018-07-22T15:05:58.033Z",
      "answeredBy": "FGD8KQPK2JKK",
      "costImpact": "Yes",
      "scheduleImpact": "Yes",
      "priority": "High",
      "discipline": [
        "Architectural"
      ],
      "category": [
        "Constructability"
      ],
      "reference": "ID-1234",
      "customAttributes": [
        {
          "id": "c911852d-5957-4145-9c8d-e7cfe9d564df",
          "values": [
            ""
          ],
          "isSelectable": false
        }
      ],
      "rfiTypeId": "c911852d-5957-4145-9c8d-e7cfe9d564df",
      "bridgedSource": "",
      "bridgedTarget": "",
      "bridgeSyncOutdated": "",
      "syncVersion": "",
      "permittedActions": {
        "share": "",
        "nudge": ""
      }
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "totalResults": 97
  }
}


Documentation /Autodesk Construction Cloud APIs /API Reference
RFIs
GET	rfis/:id
Retrieves detailed information about a specific RFI (Request for Information) in Autodesk Construction Cloud (ACC).

To check which RFI states a user can create RFIs in, and which attributes are required per state, use GET users/me.

For an overview of how RFIs work in the ACC web interface, see the Help documentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/rfis/v3/projects/:projectId/rfis/:rfiId
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
Must be Bearer <token>, where <token> is obtained via a three-legged OAuth flow.
* Required
Request
URI Parameters
projectId
string
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

rfiId
string
The ID of the RFI. To find the ID, call POST search:rfis.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters are invalid
401
Unauthorized
The provided bearer token is not valid
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation
404
Not Found
RFI not found
500
Internal Server Error
An unknown error occurred on the server
Response
Body Structure (200)
 Expand all
id
string
The system-generated ID of the RFI.
customIdentifier
string
The user-defined identifier of the RFI.
title
string
The title of the RFI.
question
string,null
The question submitted in the RFI.
virtualFolderUrn
string,null
The URN of the virtual folder created for the RFI. This folder stores all attachments related to the RFI.
The virtualFolderUrn is required when uploading attachments to an RFI. See the Upload Attachment tutorial for more details.

status
enum:string
The current status of the RFI. Available values depend on the RFI’s workflow type:
For single-reviewer workflows (US):
Possible values: draft, submitted, open, answered, rejected, closed, void.

For multi-reviewer workflows (EMEA):
Possible values: draft, submitted, openRev1 (manager), openRev2 (reviewers), answeredRev1, answeredManager, closed, void.

To determine the workflow type, call GET users/me and check the workflowType value.

For details on RFI workflows in the ACC UI, see About RFI Workflows – Autodesk Help.

previousStatus
enum:string
The previous status of the RFI, if one exists. This field is omitted if the RFI has no prior status (e.g., when newly created).
For single-reviewer workflows (US):
Possible values: draft, submitted, open, answered, rejected, closed, void.

For multi-reviewer workflows (EMEA):
Possible values: draft, submitted, openRev1 (manager), openRev2 (reviewers), answeredRev1, answeredManager, closed, void.

To determine the workflow type, call GET users/me and check the workflowType value.

For details on RFI workflows in the ACC UI, see About RFI Workflows – Autodesk Help.

workflowType
enum:string
The workflow type assigned to the RFI, which determines the allowed status transitions and the review path. Possible values:
US: Single-reviewer workflow
EU: Multi-reviewer workflow
This value affects how statuses like submitted, openRev1, or answeredManager behave. For status definitions, see the status and previousStatus fields.

assignedTo
array: object
The list of users assigned to the RFI.
managerId
string
The Autodesk ID of the user designated as the RFI Manager.
To find details about the user, call GET users.

constructionManagerId
string
The Autodesk ID of the user designated as the Construction Manager for this RFI.
To find details about the user, call GET users.

architects
array: object
The list of architect users associated with the RFI.
reviewers
array: object
The list of users assigned to review the RFI before it is closed.
dueDate
string,null
The date and time by which a response to the RFI is expected, in ISO 8601 format (YYYY-MM-DDThh:mm:ss.sZ).
locationDescription
string,null
The default text for the Location field when creating a new RFI.
Note that the API does not auto-populate this value. Clients are responsible for applying the default if desired.

To retrieve the default value configured for this field, call GET rfi-types.

locations
array: string
A list of predefined location IDs associated with the RFI, based on the project’s Location Breakdown Structure (LBS). To get more information about the locations, call GET nodes.
commentsCount
int
The number of comments associated with the RFI.
officialResponse
string
The text of the official response submitted for the RFI.
Always empty when creating an RFI.

officialResponseStatus
enum:string
The status of the official response to the RFI.
Possible values: unanswered, answered.

Always unanswered when creating an RFI.

officialResponseActors
array: object
The list of users who contributed to the official response.
Always empty when creating an RFI.

officialResponseEditByManagerState
boolean
true: the RFI Manager is allowed to edit the official response after submission.
false: editing the official response is disabled. (default).

respondedAt
datetime: ISO 8601
The date and time when the RFI was officially responded to, in ISO 8601 format (YYYY-MM-DDThh:mm:ss.sZ).
respondedBy
string
The Autodesk ID of the user who submitted the official response to the RFI.
To find details about the user, call GET users.

createdBy
string
The Autodesk ID of the user who created the RFI.
To find details about the user, call GET users.

createdAt
datetime: ISO 8601
The date and time when the RFI was created, in ISO 8601 format (YYYY-MM-DDThh:mm:ss.sZ).
updatedBy
string
The Autodesk ID of the user who last updated the RFI.
To find details about the user, call GET users.

updatedAt
datetime: ISO 8601
The date and time when the RFI was last updated, in ISO 8601 format (YYYY-MM-DDThh:mm:ss.sZ).
closedAt
datetime: ISO 8601
The date and time when the RFI was closed, in ISO 8601 format (YYYY-MM-DDThh:mm:ss.sZ).
closedBy
string
The Autodesk ID of the user who closed the RFI.
To find details about the user, call GET users.

containerId
string
The ID of the container.
projectId
string
The Autodesk ID of the project the RFI belongs to.
suggestedAnswer
string
A suggested answer for the RFI, typically entered by the assignee before submission of the official response.
coReviewers
array: object
A list of reviewers assigned to the RFI. Each entry may represent a user, role, or company.
watchers
array: object
A list of watchers who are notified about changes to the RFI. Each entry may represent a user, role, or company.
answeredAt
datetime: ISO 8601
The date and time when the official response to the RFI was submitted, in ISO 8601 format (YYYY-MM-DDThh:mm:ss.sZ).
Empty when creating an RFI.

answeredBy
string
The Autodesk ID of the user who submitted the official response to the RFI.
To find details about the user, call GET users.

Empty when creating an RFI.

costImpact
string,null
The default cost impact value for new RFIs of this type.
Possible values: null, Yes, No, Unknown.

To check whether cost impact options are enabled and to retrieve the default value, call GET rfi-types.

scheduleImpact
string,null
The default schedule impact value for new RFIs of this type.
Possible values: null, Yes, No, Unknown.

To verify whether schedule impact tracking is enabled for the project and what the default value is, call GET rfi-types.

priority
string,null
The default priority for new RFIs of this type.
The available priority values are configured in Project Admin.

If no default is set, this field is null.

Note that the API does not auto-populate this value when creating an RFI. Clients are responsible for applying the default if desired.

The valid priority options can be retrieved by calling GET rfi-types <en/docs/acc/v1/reference/http/rfis-RFI-types-GET/>_. Some possible values: ``null`, High, Normal, Low.

discipline
array: string
The discipline associated with the RFI. To retrieve the supported values for the current project, call GET rfi-types.
Some possible values: Building Management System, Electrical Substation, Security, Audio Visual, Food Service, Fire Alarm, Power Systems, Design Systems Integrator, Signage, Pathways, Cabling, Networks, Distributed Antenna System, Lighting, Vertical Transportation, Roofing, Architectural, Civil/Site, Concrete, Electrical, Exterior Envelope, Fire Protection, Interior/Finishes, Landscaping, Masonry, Mechanical, Plumbing, Structural, Other.’

category
array: string
A list of predefined categories to assign to the RFI.
Categories help group RFIs for filtering and reporting. Each value must match a category configured in the project’s RFI settings. Categories are case-sensitive and project-specific.

RFI categories are configured in Project Admin and may differ between projects. Call GET rfi-types to retrieve the allowed values for this field.

Some possible values: Code Compliance, Constructability, Design Coordination, Documentation Conflict, Documentation Incomplete, Field condition, Other.

reference
string
A user-provided text reference related to the RFI, such as a model number or spec reference, typically used when the RFI was created in another system.
Max length: 20

customAttributes
array: object
A list of custom attributes associated with the RFI.
rfiTypeId
string: UUID
The ID of the default RFI type assigned to the project. This is the unique identifier of the RFI type that will be selected by default when creating a new RFI.
bridgedSource
boolean
Not relevant
bridgedTarget
boolean
Not relevant
bridgeSyncOutdated
boolean
Not relevant
syncVersion
number
Not relevant
responses
array: object
A list of responses associated with this RFI.
Always empty when creating an RFI.

draftResponses
array: object
A list of draft responses associated with this RFI.
Always empty when creating an RFI.

permittedActions
object
The list of actions that are permitted for the user.
maxAssignees
int
The max amount of assignees permitted base on the RFIs current status.
Example
Success

Request
curl -v 'https://developer.api.autodesk.com/construction/rfis/v3/projects/:projectId/rfis/:rfiId' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "id": "31a3f98d-34a8-4d4c-a362-3cc9de44f89c",
  "customIdentifier": "ID-1234",
  "title": "RFI - pipe is not in right place",
  "question": "Where should we put the pipe?",
  "virtualFolderUrn": "urn:adsk.wip:fs.folder:co.1838SAGCQ3SPn7lqOXMaJQ",
  "status": "open",
  "previousStatus": "submitted",
  "workflowType": "US",
  "assignedTo": [
    {
      "id": "PER8KQPK2JRT",
      "type": "user"
    }
  ],
  "managerId": "KOR8KQPK2GHF",
  "constructionManagerId": "ALW8KQPK2PTB",
  "architects": [
    {
      "type": "user",
      "id": "TKG8KQPK2MNB"
    }
  ],
  "reviewers": [
    {
      "type": "user",
      "id": "IKJ8KQPK2WDV"
    }
  ],
  "dueDate": "2018-01-12T13:06:39.216Z",
  "locationDescription": "In the middle of the room.",
  "locations": [
    "AJJASD2-FFE3",
    "JTOEN-FFD33"
  ],
  "commentsCount": 15,
  "officialResponse": "The measurements are correct.",
  "officialResponseStatus": "answered",
  "officialResponseActors": [
    {
      "id": "AJJASD2-FFE3",
      "type": "user"
    },
    {
      "id": "JTOEN-FFD33",
      "type": "user"
    }
  ],
  "officialResponseEditByManagerState": true,
  "respondedAt": "2018-01-12T13:06:39.216Z",
  "respondedBy": "RFV8KQPK2KHF",
  "createdBy": "PER8KQPK2JRT",
  "createdAt": "2018-07-22T15:05:58.033Z",
  "updatedBy": "ZXC8KQPK2CVB",
  "updatedAt": "2018-07-22T15:05:58.033Z",
  "closedAt": "2018-07-22T15:05:58.033Z",
  "closedBy": "SER8KQPK2JRT",
  "containerId": "31a3f98d-34a8-4d4c-a362-3cc9de44f89c",
  "projectId": "31a3f98d-34a8-4d4c-a362-3cc9de44f89c",
  "suggestedAnswer": "The measurements are correct.",
  "coReviewers": [
    {
      "id": "WSX8KQPK2JRMJ",
      "type": "user"
    }
  ],
  "watchers": [
    {
      "id": "PER8KQPK2JRT",
      "type": "user"
    }
  ],
  "answeredAt": "2018-07-22T15:05:58.033Z",
  "answeredBy": "FGD8KQPK2JKK",
  "costImpact": "Yes",
  "scheduleImpact": "Yes",
  "priority": "High",
  "discipline": [
    "Architectural"
  ],
  "category": [
    "Constructability"
  ],
  "reference": "ID-1234",
  "customAttributes": [
    {
      "id": "c911852d-5957-4145-9c8d-e7cfe9d564df",
      "values": [
        ""
      ],
      "isSelectable": false
    }
  ],
  "rfiTypeId": "c911852d-5957-4145-9c8d-e7cfe9d564df",
  "bridgedSource": "",
  "bridgedTarget": "",
  "bridgeSyncOutdated": "",
  "syncVersion": "",
  "responses": [
    {
      "id": "c911852d-5957-4145-9c8d-e7cfe9d564df",
      "state": "draft",
      "rfiId": "w332252d-5957-4145-9c8d-e7cfe9d975aj",
      "text": "The pipe should be placed in the corner",
      "status": "answered",
      "createdBy": "PER8KQPK2JRT",
      "onBehalf": "PER8KQPK2JRT",
      "isEditable": true,
      "createdAt": "2018-07-22T15:05:58.033Z",
      "updatedBy": "PER8KQPK2JRT",
      "updatedAt": "2018-07-22T15:05:58.033Z",
      "deletedAt": "2018-07-22T15:05:58.033Z"
    }
  ],
  "draftResponses": [
    {
      "id": "c911852d-5957-4145-9c8d-e7cfe9d564df",
      "state": "draft",
      "rfiId": "w332252d-5957-4145-9c8d-e7cfe9d975aj",
      "text": "The pipe should be placed in the corner",
      "status": "answered",
      "createdBy": "PER8KQPK2JRT",
      "onBehalf": "PER8KQPK2JRT",
      "isEditable": true,
      "createdAt": "2018-07-22T15:05:58.033Z",
      "updatedBy": "PER8KQPK2JRT",
      "updatedAt": "2018-07-22T15:05:58.033Z",
      "deletedAt": "2018-07-22T15:05:58.033Z"
    }
  ],
  "permittedActions": {
    "share": "",
    "nudge": "",
    "updateRfi": {
      "permittedStatuses": {
        "wfUS": [
          {
            "status": "open",
            "maxAssignees": "",
            "requiredAttributes": [
              {
                "name": "assignedTo",
                "values": [
                  {
                    "value": "PER8KQPK2JRT",
                    "type": "user"
                  }
                ]
              }
            ],
            "permittedAttributes": [
              {
                "name": "assignedTo",
                "values": [
                  {
                    "value": "PER8KQPK2JRT",
                    "type": "user"
                  }
                ]
              }
            ]
          }
        ],
        "wfEU": [
          {
            "status": "open",
            "maxAssignees": "",
            "requiredAttributes": [
              {
                "name": "assignedTo",
                "values": [
                  {
                    "value": "PER8KQPK2JRT",
                    "type": "user"
                  }
                ]
              }
            ],
            "permittedAttributes": [
              {
                "name": "assignedTo",
                "values": [
                  {
                    "value": "PER8KQPK2JRT",
                    "type": "user"
                  }
                ]
              }
            ]
          }
        ]
      },
      "permittedAttributes": [
        {
          "name": "assignedTo",
          "values": [
            {
              "value": "PER8KQPK2JRT",
              "type": "user"
            }
          ]
        }
      ],
      "useCustomAttributes": ""
    },
    "createComment": "",
    "createResponse": "",
    "createResponseOnBehalf": "",
    "remainingReviewers": [
      {
        "id": "PER8KQPK2JRT",
        "type": "user"
      }
    ],
    "createDocumentReference": "",
    "removeDocumentReference": ""
  },
  "maxAssignees": 10
}


Documentation /Autodesk Construction Cloud APIs /API Reference
RFIs
GET	users/me
Retrieves information about the current user in the context of the specified project. The response includes the user’s assigned RFI workflow roles, whether the user is permitted to create RFIs, the workflow states in which the user can create RFIs, and the attributes required in each state.

We strongly recommend calling this endpoint before creating an RFI, to ensure the user has the necessary permissions and the latest configuration for the project.

The RFIs API does not currently support adding users to a project or assigning workflow roles. Only project members can create or edit RFIs.

To add responses or attachments to the RFI, call POST responses after the RFI is created.

Users can create RFIs if they are assigned either the creator (projectSC) or manager (projectGC) workflow role. These roles must be explicitly configured in the RFI tool settings by going to RFIs → Settings → Permissions in the Autodesk Construction Cloud (ACC) web interface. There is no default workflow role, so project members will not be able to create RFIs unless one of these roles is assigned.

To check if a user can create RFIs, look for the createRfi object inside the permittedActions section of the response.

Workflow roles must be assigned manually via the UI. There is currently no API support for modifying workflow roles.

The table below lists the Project Admin workflow role names and their corresponding RFIs API role names:

Project Admin Module Workflow Role Name	RFIs API Workflow Role Name
Creator	Subcontractor (projectSC)
Manager	General Contractor (projectGC)
Reviewer 1 (EMEA workflow)	Construction Manager (projectCoordinator)
Reviewer (US workflow) / Reviewer 2 (EMEA workflow)	Architect (projectReviewer)
For more information, see the RFIs permissions documentation.

The table below shows the workflow names used in the Project Admin UI and their corresponding values in the RFIs API:

Project Admin Module Workflow Type Name	RFIs API Workflow Type Name
Default Workflow	US
Workflow with Additional Reviewer	EMEA
You can use either workflow type (US or EMEA) in both the US and EMEA regions. To assign a workflow type to a project, use the Project Admin UI.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/rfis/v3/projects/:projectId/users/me
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
Must be Bearer <token>, where <token> is obtained via a three-legged OAuth flow.
* Required
Request
URI Parameters
projectId
string
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters are invalid
401
Unauthorized
The provided bearer token is not valid
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation
500
Internal Server Error
An unknown error occurred on the server
Response
Body Structure (200)
 Expand all
user
object
The current user’s details.
permittedActions
object
The list of actions that are permitted for the user.
workflow
object
The user’s assigned workflow roles and workflow type for RFIs in the current project.
defaultRfiType
string: UUID
The ID of the default RFI type assigned to the project. This is the unique identifier of the RFI type that will be selected by default when creating a new RFI.
externalUsers
array: object
Not relevant
maintenanceEndDate
string
Not relevant
Example
Success

Request
curl -v 'https://developer.api.autodesk.com/construction/rfis/v3/projects/:projectId/users/me' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "user": {
    "id": "BZPWJWWWMLSV",
    "name": "Jon Doe",
    "role": "project_admin"
  },
  "permittedActions": {
    "createRfi": {
      "permittedStatuses": {
        "wfUS": [
          {
            "status": "open",
            "maxAssignees": "",
            "requiredAttributes": [
              {
                "name": "assignedTo",
                "values": [
                  {
                    "value": "PER8KQPK2JRT",
                    "type": "user"
                  }
                ]
              }
            ],
            "permittedAttributes": [
              {
                "name": "assignedTo",
                "values": [
                  {
                    "value": "PER8KQPK2JRT",
                    "type": "user"
                  }
                ]
              }
            ]
          }
        ],
        "wfEU": [
          {
            "status": "open",
            "maxAssignees": "",
            "requiredAttributes": [
              {
                "name": "assignedTo",
                "values": [
                  {
                    "value": "PER8KQPK2JRT",
                    "type": "user"
                  }
                ]
              }
            ],
            "permittedAttributes": [
              {
                "name": "assignedTo",
                "values": [
                  {
                    "value": "PER8KQPK2JRT",
                    "type": "user"
                  }
                ]
              }
            ]
          }
        ]
      }
    }
  },
  "workflow": {
    "roles": [
      "projectSC"
    ],
    "type": "US"
  },
  "defaultRfiType": "c911852d-5957-4145-9c8d-e7cfe9d564df",
  "externalUsers": [
    {
      "email": "",
      "autodeskId": ""
    }
  ],
  "maintenanceEndDate": ""
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Rfi Types
GET	rfi-types
Retrieves the list of RFI types configured for the specified project.

Each RFI type defines the default values and permitted options used when creating or updating RFIs. This includes the available discipline, category, and priority values, as well as the list of users, companies, or roles who can be assigned to workflow roles such as manager, reviewer, and watcher.

Call this endpoint before creating or updating an RFI to:

Retrieve the available options for configurable fields such as discipline, category, priority, costImpact, and scheduleImpact.
Get the list of potential assignees for workflow roles.
Determine the default due date offset for an RFI type.
The values returned by this endpoint reflect the configuration set by project admins in ACC Docs and Project Management.

For more information about creating and updating RFIs, see POST rfis and PATCH rfis/:id.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/rfis/v3/projects/:projectId/rfi-types
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
Must be Bearer <token>, where <token> is obtained via a three-legged OAuth flow.
* Required
Request
URI Parameters
projectId
string
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Request
Query String Parameters
limit
int
The number of RFIs to return in the response. Acceptable values: 1–200. Default: 10. For example, to limit the response to two items per page, use limit=2
offset
int
The number of items to skip before starting to return results.
For example, to begin the results from the fourth item, use offset=3.

filter[status]
array: string
Filters the response to only include RFI types with the specified status. Possible values: active, inactive, hidden.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters are invalid
401
Unauthorized
The provided bearer token is not valid
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation
500
Internal Server Error
An unknown error occurred on the server
Response
Body Structure (200)
 Expand all
results
array: object
The list of RFI types configured for the project.
pagination
object
The pagination object.
Example
Success

Request
curl -v 'https://developer.api.autodesk.com/construction/rfis/v3/projects/:projectId/rfi-types' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "results": [
    {
      "id": "c911852d-5957-4145-9c8d-e7cfe9d564df",
      "name": "Type 1",
      "wfType": "US",
      "status": "active",
      "isDefault": true,
      "projectReviewer": [
        {
          "id": "PER8KQPK2JRT",
          "type": "user"
        }
      ],
      "projectCoordinator": [
        {
          "id": "PER8KQPK2JRT",
          "type": "user"
        }
      ],
      "manager": [
        {
          "id": "PER8KQPK2JRT",
          "type": "user"
        }
      ],
      "watchers": [
        {
          "id": "PER8KQPK2JRT",
          "type": "user"
        }
      ],
      "dueDateOffset": 7,
      "locationDescription": "In the middle of the room.",
      "costImpact": "Yes",
      "scheduleImpact": "Yes",
      "priority": "High",
      "discipline": [
        "Architectural"
      ],
      "category": [
        "Constructability"
      ],
      "reference": "",
      "bridgeTargetProjectIds": ""
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "totalResults": 97
  }
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Custom Attributes
GET	custom-attributes
Retrieves all custom attribute definitions for a project.

Use this endpoint to list available attributes and their allowed values when creating or updating RFIs.

For more information on setting up custom attributes, see the Custom RFI Fields help topic.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/rfis/v3/projects/:projectId/attributes
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
Must be Bearer <token>, where <token> is obtained via a three-legged OAuth flow.
* Required
Request
URI Parameters
projectId
string
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Request
Query String Parameters
limit
int
The number of RFIs to return in the response. Acceptable values: 1–200. Default: 10. For example, to limit the response to two items per page, use limit=2
offset
int
The number of items to skip before starting to return results.
For example, to begin the results from the fourth item, use offset=3.

filter[status]
array: string
Filters the response to only include custom attributes with the specified status. Possible values: active, inactive, hidden.
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters are invalid
401
Unauthorized
The provided bearer token is not valid
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation
500
Internal Server Error
An unknown error occurred on the server
Response
Body Structure (200)
 Expand all
results
array: object
The list of custom attributes.
pagination
object
The pagination object.
Example
Success

Request
curl -v 'https://developer.api.autodesk.com/construction/rfis/v3/projects/:projectId/attributes' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "results": [
    {
      "id": "c911852d-5957-4145-9c8d-e7cfe9d564df",
      "name": "Attribute 1",
      "type": "text",
      "description": "This is a description of the attribute",
      "status": "active",
      "multipleChoice": false,
      "possibleValues": [
        {
          "id": "c911852d-5957-4145-9c8d-e7cfe9d564df",
          "name": "Value 1"
        }
      ]
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "totalResults": 97
  }
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Custom-Identifier
GET	custom-identifier
Returns the current and next available RFI custom identifier for the project.

Use this endpoint to display or pre-fill the next custom RFI number when creating a new RFI. The identifier is automatically incremented and skips numbers that are already in use.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/rfis/v3/projects/:projectId/rfis/custom-identifier
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
Must be Bearer <token>, where <token> is obtained via a three-legged OAuth flow.
* Required
Request
URI Parameters
projectId
string
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Response
HTTP Status Code Summary
200
OK
Details of the last created and the next available custom identifiers.
400
Bad Request
The parameters are invalid
401
Unauthorized
The provided bearer token is not valid
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation
500
Internal Server Error
An unknown error occurred on the server
Response
Body Structure (200)
current
string,null
The last custom identifier that was used for an RFI in this project.
next
string
The next available custom identifier for the project.
Example
Details of the last created and the next available custom identifiers.

Request
curl -v 'https://developer.api.autodesk.com/construction/rfis/v3/projects/:projectId/rfis/custom-identifier' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "current": "353",
  "next": "354"
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Attachments
GET	rfis/:id/attachments
Retrieves a list of attachments for a specific RFI.

Use this endpoint to access all files uploaded to the RFI, including official responses, additional documents, and markups.

You can filter the results by attachment type or use pagination to retrieve large sets.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/rfis/v3/projects/:projectId/rfis/:rfiId/attachments
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
Must be Bearer <token>, where <token> is obtained via a three-legged OAuth flow.
* Required
Request
URI Parameters
projectId
string
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

rfiId
string
The ID of the RFI. To find the ID, call POST search:rfis.
Request
Query String Parameters
limit
int
The number of attachments to return in the response. Possible values: 1–200. Default: 10.
For example, to limit the response to two attachments per page, use limit=2.

offset
int
The number of items to skip before starting to return results.
For example, to begin the results from the fourth item, use offset=3.

filter[attachmentTypes]
array: string
Filters the response to only include attachments of the specified types.
Possible values: rfiResponse, rfiOfficialResponse, rfiWebHiddenFiles, bridgeFiles.

If not provided, the default filter is: rfiResponse, rfiOfficialResponse.

Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters are invalid
401
Unauthorized
The provided bearer token is not valid
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation
404
Not Found
RFI not found
500
Internal Server Error
An unknown error occurred on the server
Response
Body Structure (200)
 Expand all
results
array: object
The list of attachments.
pagination
object
The pagination object.
Example
Success

Request
curl -v 'https://developer.api.autodesk.com/construction/rfis/v3/projects/:projectId/rfis/:rfiId/attachments' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "results": [
    {
      "attachmentId": "1234852d-5957-4145-9c8d-e7cfe9d564df",
      "attachmentType": "rfiResponse",
      "displayName": "Structural Plan - Rev A.pdf",
      "fileName": "revA_plan_final_v2.pdf",
      "storageUrn": "urn:adsk.objects:os.object:wip.dm.qa/b232ff3f-eff7-4e17-a486-362de84230a3.png",
      "domainEntityId": "c911852d-5957-4145-9c8d-e7cfe9d564df",
      "docsId": "c911852d-5957-4145-9c8d-e7cfe9d564df",
      "containerId": "12302fc6-00a5-45ca-a9df-4427b9247123",
      "rfiId": "0d302fc6-00a5-45ca-a9df-4427b9247c81",
      "lineageUrn": "urn:adsk.wipprod:dm.lineage:1t7QY9-JSxCB0TLh1qMvFQ",
      "fileSize": 1024,
      "fileType": "png",
      "version": 1,
      "versionUrn": "urn:adsk.wipprod:fs.file:vf.1HROnsnfQgq4N0b-nUoGge?version=1",
      "tipVersionUrn": "urn:adsk.wipprod:fs.file:vf.1HROnsnfQgq4N0b-nUoGge?version=1",
      "bubbleUrn": "urn:adsk.objects:os.object:modelderivative/building.rvt",
      "createdOn": "2018-08-01T08:56:48.699Z",
      "createdBy": "PER8KQPK2JRT",
      "modifiedOn": "2018-08-01T08:56:48.699Z",
      "modifiedBy": "PER8KQPK2JRT",
      "createdByName": "Jill Sharp",
      "isDeleted": false,
      "deletedOn": "2018-08-01T08:56:48.699Z",
      "deletedBy": "PER8KQPK2JRT"
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "totalResults": 97
  }
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Comments
GET	v3/projects/{projectId}/rfis/{rfiId}/comments
Retrieves a list of comments associated with a specific RFI.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/rfis/v3/projects/:projectId/rfis/:rfiId/comments
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
Must be Bearer <token>, where <token> is obtained via a three-legged OAuth flow.
* Required
Request
URI Parameters
projectId
string
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

rfiId
string
The ID of the RFI. To find the ID, call POST search:rfis.
Request
Query String Parameters
limit
int
The number of RFIs to return in the response. Acceptable values: 1–200. Default: 10. For example, to limit the response to two items per page, use limit=2
offset
int
The number of items to skip before starting to return results.
For example, to begin the results from the fourth item, use offset=3.

sort
array: string
The fields to sort the list by
fields
array: string
Specify which attributes you want to see in the response. Separate multiple values with commas. For example, fields = title,description.
filter[createdAt]
string
Retrieves comments created after the specified date, in the following format: YYYY-MM-DDThh:mm:ss.sz, or a date range in the following format: YYYY-MM-DDThh:mm:ss.sz..YYYY-MM-DDThh:mm:ss.sz.
filter[createdBy]
array: string
Retrieves comments created by the user. For example, filter[createdBy]=PER8KQPK2JRT
Response
HTTP Status Code Summary
200
OK
Success
400
Bad Request
The parameters are invalid
401
Unauthorized
The provided bearer token is not valid
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation
404
Not Found
RFI not found
500
Internal Server Error
An unknown error occurred on the server
Response
Body Structure (200)
 Expand all
results
array: object
A list of comments associated with the RFI.
pagination
object
The pagination object.
Example
Success

Request
curl -v 'https://developer.api.autodesk.com/construction/rfis/v3/projects/:projectId/rfis/:rfiId/comments' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "results": [
    {
      "id": "94ce6921-e8f9-4bc5-bf5a-1a8f543a2564",
      "body": "This needs more attention.",
      "createdBy": "PER8KQPK2JRT",
      "createdAt": "2018-08-01T08:56:48.699Z",
      "updatedAt": "2019-08-01T08:56:48.699Z",
      "source": "web"
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "totalResults": 97
  }
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Workflows
GET	workflow
Retrieves the workflow configuration for a given project, including the workflow type, description, and the mapping between project roles and their permitted assignees.

This endpoint helps clients understand which users, companies, or roles are allowed to participate in specific workflow actions within a project.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/rfis/v3/projects/:projectId/workflow
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
Must be Bearer <token>, where <token> is obtained via a three-legged OAuth flow.
* Required
Request
URI Parameters
projectId
string
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Response
HTTP Status Code Summary
200
OK
OK
400
Bad Request
The parameters are invalid
401
Unauthorized
The provided bearer token is not valid
403
Forbidden
The user or service represented by the bearer token does not have permission to perform this operation
500
Internal Server Error
An unknown error occurred on the server
Response
Body Structure (200)
 Expand all
workflowType
enum:string
The region type of the workflow. Possible values: US, EU.
description
string
A description of the workflow
projectRolesMapping
array: object
A list of project roles and their corresponding permitted assignees.
Example
OK

Request
curl -v 'https://developer.api.autodesk.com/construction/rfis/v3/projects/:projectId/workflow' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "workflowType": "US",
  "description": "Support for RFI creation. Review and response with Creator, Manager and Reviewer workflow roles.",
  "projectRolesMapping": [
    {
      "name": "projectGC",
      "permittedAssignees": [
        {
          "id": "PER8KQPK2JRT",
          "type": "user"
        }
      ]
    }
  ]
}
