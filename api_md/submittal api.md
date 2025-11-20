Documentation /Autodesk Construction Cloud APIs /API Reference
Attachments
GET	projects/{projectId}/items/{itemId}/attachments
Retrieve information about attachments associated with a specified item. You can use the information to download attachments. For more information, see the Download Submittal Attachments tutorial.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/submittals/v2/projects/:projectId/items/:itemId/attachments
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
itemId
string
The ID of the submittal item. To find the item ID, call GET items.
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Request
Query String Parameters
limit
int
The maximum number of results per page. Possible values: 1- 50. Default value: 20. For example, to limit the response to two results per page, use limit=2.
offset
int
The number of results to skip before starting to return data. For example, to skip the first 20 results, include offset=20 in the query string. For more details, see the JSON API Paging Help documentation.
sort
string
Sort attachments by specific fields in either ascending (asc) or descending (desc) order. Separate multiple criteria with commas. For example, statusId asc.
Possible values: id, isFileUploaded, asyncState, createdBy, createdAt, updatedBy, updatedAt, name, uploadUrn, urn, urnPage, resourceUrns, urnTypeId, urnVersion, revision, categoryId, isReview, isResponse.

filter[categoryId]
string
Filter attachments by category identifier. Multiple values can be separated by commas.
filter[revision]
string
Filter items with the specified revision number. You can specify multiple values. Separate multiple values with commas. For example, filter[revision]=1.
filter[isFileUploaded]
string
true: to filter files that are uploaded.
false: to filter files that are not uploaded.

Response
HTTP Status Code Summary
200
OK
An attachments list.
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers.
401
Unauthorized
Invalid or missing authorization header. Verify the Bearer token and try again.
403
Forbidden
The user is not authorized to perform this action.
404
Not Found
The specified resource was not found.
500
Internal Server Error
An unexpected error occurred on the server while processing the request.
Response
Body Structure (200)
 Expand all
pagination
object
Describes pagination details for the response, including information about the current page and navigation to other pages.
results
array: object
The list of attachments.
Example
An attachments list.

Request
curl -v 'https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/items/767b5888-2c6a-413d-8487-613966dd64ce/attachments' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'



respond:
{
  "pagination": {
    "limit": 10,
    "offset": 100,
    "totalResults": 25,
    "previousUrl": "https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/items/767b5888-2c6a-413d-8487-613966dd64ce/attachments?limit=5&offset=10",
    "nextUrl": null
  },
  "results": [
    {
      "id": "1d0a9b65-f411-4eb2-b6bb-69f8ea483207",
      "itemId": "2df3b4cf-16f4-496e-8173-7125f31e3dd1",
      "taskId": "1ab2ae43-fb33-4868-be85-03f4873915fc",
      "name": "attachment-document.pdf",
      "isFileUploaded": "true",
      "url": null,
      "asyncState": "1",
      "uploadUrn": "urn:adsk.objects:os.object:wip.dm.prod/1a8148a6-d74e-4a6b-8cf2-38f2074f87d1.pdf",
      "urn": "urn:adsk.wipprod:fs.file:vf.TQW6YsrTTFGrJVJKAaK_ew?version=1",
      "urnVersion": 1,
      "revisionFolderUrn": "urn:adsk.wipprod:fs.folder:co.3is_lyUzTxu6nNXobG2P7Q\"",
      "revision": 0,
      "urnTypeId": "2",
      "categoryId": "1",
      "urnPage": null,
      "resourceUrns": null,
      "createdBy": "WD43ZJGKDFLFH",
      "createdAt": "2018-02-01T12:09:24.198466Z",
      "updatedAt": "2018-02-01T12:09:24.198466Z",
      "updatedBy": "WD43ZJGKDFLFH",
      "duplicatedFrom": "f4635373-a5b4-456c-af8d-e0446652967c",
      "permittedActions": [
        {
          "id": "Attachment::update",
          "fields": {
            "isFileUploaded": []
          },
          "mandatoryFields": [
            "isFileUploaded"
          ],
          "transitions": [
            ""
          ]
        }
      ]
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Items
GET	projects/{projectId}/items
Retrieves information about all the submittal items in a project that the user has permission to view.

Note that only managers can access submittals items in draft state.

Note also that submittal items in void state are excluded by default.

For information about submittal items, see the Help documentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/submittals/v2/projects/:projectId/items
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
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Request
Query String Parameters
limit
int
The maximum number of results per page. Possible values: 1- 50. Default value: 20. For example, to limit the response to two results per page, use limit=2.
offset
int
The number of results to skip before starting to return data. For example, to skip the first 20 results, include offset=20 in the query string. For more details, see the JSON API Paging Help documentation.
sort
string
Sort items by specified fields. Separate multiple values with commas. To sort in descending or ascending order, add desc or asc after the sort criteria. For example, statusId asc.
Possible values: ballInCourtUsers, ballInCourtCompanies, ballInCourtRoles, ballInCourtType, customIdentifier, customIdentifierHumanReadable, createdAt, createdBy, description, dueDate, id, identifier, leadTime, manager, managerType, managerDueDate, package.identifier, package.spec.identifier, packageId, packageIdentifier, packageSpecIdentifier, packageTitle, priority, publishedBy, publishedDate, receivedFromReview, receivedFromSubmitter, requiredApprovalDate, requiredDate, requiredOnJobDate, respondedAt, respondedBy, response.value, responseComment, responseId, revision, sentToReview, sentToReviewBy, sentToSubmitter, spec.identifier, specId, specIdentifier, specTitle, stateId, statusId, subcontractor, subcontractorType, submittedBy, submitterDueDate, subsection, title, type.value, typeId, updatedAt, updatedBy, watchers.

search
string
Search for items by querying a specified string within specific fields (identifier, title, specIdentifier, ballInCourt), and retrieve the associated items that match the search criteria. This includes items where the string matches part of a field. For example, search=1.
filter[title]
string
Filter items with the specified title. You can specify multiple values. Separate multiple values with commas. For example, filter[title]="Shop Drawings".
filter[statusId]
string
Filter items with the specified status ID. You can specify multiple values. Separate multiple values with commas. For example, filter[statusId]=1
filter[specId]
string
Filter items with the specified spec ID. You can specify multiple values. Separate multiple values with commas. For example, filter[specId]=b4aa3864-5706-4a7b-b06c-a792e8b2df23
filter[ballInCourtUsers]
string
Filter items associated with the specified ball-in-court user ID. You can specify multiple users. Separate multiple values with commas. For example, filter[ballInCourtUsers]=HNRCQ6JTWAED.
filter[ballInCourtCompanies]
string
Filter items associated with the specified ball-in-court company ID. You can specify multiple companies. Separate multiple values with commas. For example, filter[ballInCourtCompanies]=WD43ZJGKDFLFH.
filter[ballInCourtRoles]
string
Filter items associated with the specified ball-in-court role ID. You can specify multiple roles. Separate multiple values with commas. For example, filter[ballInCourtRoles]=WD43ZJGKDFLFH.
filter[responseId]
string
Filter items with the specified final response ID. You can specify multiple IDs. You can specify multiple values. Separate multiple values with commas. For example, filter[responseId]=1w66d30b-7dc1-4a65-991d-d739a1381rf4.
filter[reviewResponseId]
string
Filter items with the specified review response ID. You can specify multiple IDs. You can specify multiple values. Separate multiple values with commas. For example, filter[reviewResponseId]=1w66d30b-7dc1-4a65-991d-d739a1381rf4.
filter[typeId]
string
Filter items with the specified type ID. You can specify multiple values. Separate multiple values with commas. For example, filter[typeId]=06fa0c1b-6462-459d-8a38-0aff11bfe868.
filter[packageId]
string
Filter items with the specified package ID. You can specify multiple values. Separate multiple values with commas. For example, filter[packageId]=06fa0c1b-6462-459d-8a38-0aff11bfe868. In order to filter items with no package, use ‘noPackage’ value.
filter[stateId]
string
Filter items with the specified state ID. You can specify multiple values. Separate multiple values with commas. For example, filter[stateId]=rev.
filter[identifier]
string
Filter items with the specified submittal item ID (the submittal item ID in the UI). You can specify multiple values. Separate multiple values with commas. For example, filter[identifier]=2.
filter[leadTime]
string
Filter items with the specified lead time. You can specify multiple values. Separate multiple values with commas. For example, filter[leadTime]=100.
filter[revision]
string
Filter items with the specified revision number. You can specify multiple values. Separate multiple values with commas. For example, filter[revision]=1.
filter[manager]
string
Filter items with the specified manager Autodesk ID. You can specify multiple values. Separate multiple values with commas. For example, filter[manager]=WD43ZJGKDFLFH.
filter[managerType]
string
Filter items with the specified manager type. You can specify multiple values. Separate multiple values with commas. For example, filter[managerType]=1.
filter[subcontractor]
string
Filter items with the specified subcontractor Autodesk ID. You can specify multiple values. Separate multiple values with commas. For example, filter[subcontractor]=WD43ZJGKDFLFH.
filter[subcontractorType]
string
Filter items with the specified subcontractor type. You can specify multiple values. Separate multiple values with commas. For example, filter[subcontractorType]=1.
filter[createdBy]
string
Filter items that were created by the specified user by specifying the user’s Autodesk ID. For example, filter[createdBy]=PER8KQPK2JRT. To find the ID call GET users.
filter[watchers]
string
Filter items that are associated with the specified watcher, by specifying the watcher’s Autodesk ID. For example, filter[watchers]=PER8KQPK2JRT. You can specify more than one watcher. Separate multiple values with commas. To find the ID call GET users.
filter[dueDate]
string
Filter items with the specified due date, using the following URL-encoded format YYYY-MM-DD. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03
Specific day: e.g., 2022-03-02
For more details, see JSON API Filtering.

filter[submitterDueDate]
string
Filter items with the specified submitter’s due date, using the following URL-encoded format YYYY-MM-DD. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03
Specific day: e.g., 2022-03-02
For more details, see JSON API Filtering.

filter[managerDueDate]
string
Filter items with the specified manager’s due date, using the following URL-encoded format YYYY-MM-DD. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03
Specific day: e.g., 2022-03-02
For more details, see JSON API Filtering.

filter[createdAt]
string
Filter items with the specified creation date, using the following URL-encoded format YYYY-MM-DD. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03
Specific day: e.g., 2022-03-02
For more details, see JSON API Filtering.

filter[sentToSubmitter]
string
Filter items based on the date they were sent to the submitter. Use the following URL-encoded format: YYYY-MM-DD. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03
Specific day: e.g., 2022-03-02
For more details, see JSON API Filtering.

filter[receivedFromSubmitter]
string
Filter items based on the date they were received from the submitter. Use the following URL-encoded format: YYYY-MM-DD. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03
Specific day: e.g., 2022-03-02
For more details, see JSON API Filtering.

filter[sentToReview]
string
Filter items based on the date they were sent for review, in the URL-encoded format: YYYY-MM-DD. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03
Specific day: e.g., 2022-03-02
For more details, see JSON API Filtering.

filter[receivedFromReview]
string
Filter items based on the date they were moved forward by the reviewer using the URL-encoded format: YYYY-MM-DD. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03
Specific day: e.g., 2022-03-02
For more details, see JSON API Filtering.

filter[publishedDate]
string
Filter items based on their published date using the following URL-encoded format: YYYY-MM-DD. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03
Specific day: e.g., 2022-03-02
For more details, see JSON API Filtering.

filter[requiredDate]
string
Filter items based on the date the responsible contractor needs to submit the submittal to the submittal manager, using the following URL-encoded format: YYYY-MM-DD. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03
Specific day: e.g., 2022-03-02
For more details, see JSON API Filtering.

filter[requiredApprovalDate]
string
Filter items based on their required approval date using the following URL-encoded format: YYYY-MM-DD. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03
Specific day: e.g., 2022-03-02
For more details, see JSON API Filtering.

filter[requiredOnJobDate]
string
Filter items based on their required on-job (jobsite) date using the following URL-encoded format: YYYY-MM-DD. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03
Specific day: e.g., 2022-03-02
For more details, see JSON API Filtering.

filter[updatedAt]
string
Filter items by their last updated date using the following URL-encoded format: YYYY-MM-DD. We support the following filtering options:
Date range: e.g., 2022-03-02..2022-03-03
Specific day: e.g., 2022-03-02
For more details, see JSON API Filtering.

filter[id]
string
Filter submittal items by their unique internal submittal item ID (UUID). You can specify multiple values. Separate multiple values with commas. For example filter[id]=b8cc9324-6759-4f07-8ce3-725d5afd4f11.
Response
HTTP Status Code Summary
200
OK
A list of items.
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers.
401
Unauthorized
Invalid or missing authorization header. Verify the Bearer token and try again.
403
Forbidden
The user is not authorized to perform this action.
404
Not Found
The specified resource was not found.
500
Internal Server Error
An unexpected error occurred on the server while processing the request.
Response
Body Structure (200)
 Expand all
results
array: object
The list of submittal items.
pagination
object
Describes pagination details for the response, including information about the current page and navigation to other pages.
Example
A list of items.

Request
curl -v 'https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/items' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "results": [
    {
      "id": "b8cc9324-6759-4f07-8ce3-725d5afd4f11",
      "identifier": 1111,
      "customIdentifier": "A-111",
      "customIdentifierHumanReadable": "0001-A-111",
      "typeId": "06fa0c1b-6462-459d-8a38-0aff11bfe868",
      "specId": "62d6f245-b470-4af4-802b-4cb94b5dead1",
      "specIdentifier": "09-5300",
      "specTitle": "Acoustical Ceilings",
      "subsection": "1.05-B",
      "title": "Shop Drawings",
      "description": "Detailed plans by subcontractor, showing project dimensions.",
      "priority": "Low",
      "revision": 0,
      "stateId": "mgr-1",
      "statusId": "1",
      "ballInCourtUsers": [
        "WD43ZJGKDFLFH"
      ],
      "ballInCourtCompanies": [
        "WD43ZJGKDFLFH"
      ],
      "ballInCourtRoles": [
        "WD43ZJGKDFLFH"
      ],
      "ballInCourtType": "reviewer",
      "manager": "WD43ZJGKDFLFH",
      "managerType": "1",
      "subcontractor": "WD43ZJGKDFLFH",
      "subcontractorType": "1",
      "watchers": [
        {
          "id": "224356",
          "userType": "2"
        },
        {
          "id": "3522614",
          "userType": "3"
        }
      ],
      "dueDate": "2018-02-15",
      "requiredOnJobDate": "2018-02-15",
      "leadTime": 100,
      "requiredDate": "2018-02-15",
      "requiredApprovalDate": "2018-02-15",
      "submitterDueDate": "2018-02-15",
      "sentToSubmitter": "2018-02-01T12:09:24.198466Z",
      "receivedFromSubmitter": "2018-02-01T12:09:24.198466Z",
      "submittedBy": "WD43ZJGKDFLFH",
      "managerDueDate": "2018-02-15",
      "sentToReview": "2018-02-01T12:09:24.198466Z",
      "sentToReviewBy": "WD43ZJGKDFLFH",
      "receivedFromReview": "2018-02-01T12:09:24.198466Z",
      "publishedDate": "2018-02-01T12:09:24.198466Z",
      "publishedBy": "WD43ZJGKDFLFH",
      "responseId": "2d46d30b-7dc1-4a65-991d-d739a1381eb8",
      "responseComment": "Revisions required before approval.",
      "respondedAt": "2018-02-01T12:09:24.198466Z",
      "respondedBy": "WD43ZJGKDFLFH",
      "packageId": "e8302552-fc5a-42ac-ba4b-e9de9760c356",
      "packageIdentifier": "222",
      "packageTitle": "my package1",
      "packageSpecIdentifier": "A-500",
      "folderUrn": "urn:adsk.wipprod:fs.file:vf.hvNfeldTPm_aDqRNZgKjD",
      "revisionsFoldersUrns": {
        "0": {
          "folderUrnCreatedAt": "2018-01-28 09:26:36.371607",
          "revision": 0,
          "folderUrn": "urn:adsk.wipprod:fs.folder:co.r04fl5B7QCa1731EeH5dYDQ"
        }
      },
      "createdAt": "2018-02-01T12:09:24.198466Z",
      "createdBy": "WD43ZJGKDFLFH",
      "updatedAt": "2018-04-04T12:09:24.198466Z",
      "updatedBy": "WD43ZJGKDFLFH",
      "permittedActions": [
        {
          "id": "Item::update",
          "fields": {
            "subcontractor": [],
            "manager": []
          },
          "mandatoryFields": [
            ""
          ],
          "transitions": [
            {
              "id": "rev::void",
              "name": "Send to void",
              "stateFrom": {
                "id": "rev",
                "name": "Review"
              },
              "stateTo": {
                "id": "void",
                "name": "Void"
              },
              "transitionFields": [
                "subcontractor",
                "subcontractorType",
                "watchers",
                "responseId"
              ],
              "mandatoryFields": [
                "responseId"
              ],
              "actionId": "ITEM_TRANSITION_REV_VOID"
            }
          ]
        }
      ]
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 100,
    "totalResults": 25,
    "previousUrl": "https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/settings/mappings?offset=10&limit=100",
    "nextUrl": null
  }
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Items
GET	projects/{projectId}/items/{itemId}
Retrieve information about a single submittal item that the user has permission to view. For information about submittal items, see the Help documentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/submittals/v2/projects/:projectId/items/:itemId
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
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

itemId
string
The ID of the submittal item. To find the item ID, call GET items.
Response
HTTP Status Code Summary
200
OK
Successfully retrieved a submittal item.
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers.
401
Unauthorized
Invalid or missing authorization header. Verify the Bearer token and try again.
403
Forbidden
The user is not authorized to perform this action.
404
Not Found
The specified resource was not found.
500
Internal Server Error
An unexpected error occurred on the server while processing the request.
Response
Body Structure (200)
 Expand all
id
string: UUID
The internal, globally unique identifier (UUID) for the submittal item.
identifier
int
The unique ID assigned to the submittal item within the UI. This ID is system-generated and serves as a reference for users interacting with submittal items through the UI. For example, 111.
customIdentifier
string
customIdentifier and customIdentifierHumanReadable relate to the Number column in the UI. Submittal managers assign custom numbers to items (manually or automatically). Custom numbers are configured either in global numbering format: <global number>, or in spec section numbering format: <spec ID>-<sequential number>.
For projects with a global numbering format, both customIdentifier and customIdentifierHumanReadable represent the global number.

For projects with a spec section numbering format (<spec ID>-<sequential number>), customIdentifier represents the sequential number. For example, for a full number of 033100-01, customIdentifier is 01.

Note that for unnumbered items customIdentifier is null.

For more information on custom numbering, see the Help documentation.

customIdentifierHumanReadable
string
customIdentifierHumanReadable and customIdentifier relate to the Number column in the UI. Submittal managers assign custom numbers to items (manually or automatically). Custom numbers are configured either in global numbering format: <global number>, or in spec section numbering format: <spec ID>-<sequential number>.
For projects with a global numbering format, both customIdentifier and customIdentifierHumanReadable represent the global number.

For projects with a spec section numbering format (<spec ID>-<sequential number>), customIdentifierHumanReadable represents the full number - both the spec ID and the sequential number. For example, for a full number of 033100-01, customIdentifierHumanReadable is 033100-01.

Note that for unnumbered items customIdentifierHumanReadable is Unspecified. For spec section numbering it also includes the spec ID. For example, 033100-Unspecified.

For more information on custom numbering, see the Help documentation.

typeId
string
The ID representing the type of submittal item.
specId
string: UUID
The unique identifier (UUID) of the spec assigned to the submittal item.
specIdentifier
string
The identifier of the spec section that is associated with the submittal item. The identifier is assigned to the spec section in the UI.
specTitle
string
The title of the spec associated with the submittal item.
subsection
string
The sub-spec section associated with the submittal item, providing additional categorization within the main spec.
title
string
The title of the submittal item.
description
string
The description of the submittal item.
priority
enum:string
The priority of the submittal item.
Possible values:

Low
Normal
High
revision
int
The revision number of the submittal item, indicating the version of the item in the submittal workflow. For example, 1 for the initial submission or 2 for the first revision.
stateId
enum:string
The current state of the submittal item after the transition.
Possible values:

sbc-1 (Waiting for Submission) - Assigned to the Responsible Contractor, who needs to submit the submittal to the Manager.

mgr-1 (Open - Submitted) - Assigned to the Manager, who needs to prepare the submittal item for review.

rev (Open - In Review) - Under review by the reviewers defined in the submittal item’s review workflow.

mgr-2 (Open - Reviewed) - The review is complete, and the submittal is returned to the Manager, who needs to set the final response and close the submittal.

sbc-2: (Closed) - The submittal has been closed and assigned to the Responsible Contractor.

void (Voided) - The submittal item has been voided.

draft (Draft) - Assigned to the Manager, who must send the submittal item to the Responsible Contractor.

statusId
enum:string
The status of the submittal item.
Possible values: 1 - (Required), 2 - (Open), 3 - (Closed), 4 - (Void), 5 - (Empty), 6 - (Draft).

To retrieve the full list of possible statuses, call GET metadata.

ballInCourtUsers
array: string
The Autodesk IDs of users who are currently assigned to the submittal item at this stage of the workflow.
ballInCourtCompanies
array: string
The member group IDs of the companies currently assigned to the submittal item at this stage of the workflow.
ballInCourtRoles
array: string
The member group IDs of user roles that are currently assigned to the submittal item at this stage of the workflow.
ballInCourtType
enum:string
‘The type of submittal role assigned to the user currently assigned to the submittal item.
Possible values: reviewer, manager, subcontractor.’

manager
string
The ID that was assigned to the manager of the submittal item.
To determine the type of the manager (user, role, or company), refer to the manager type (managerType) attribute. In order to get more info about the manager, use:

GET projects/users to verify the actual name of the user in case the typs is a user (1).
GET companies to determine the name of the company in case the typs is a company (2).
Note that we do not currently support verifying names of roles.

managerType
enum:string
The type of manager associated with the submittal item.
Possible values: 1 (user), 2 (company), 3 (role).

subcontractor
string
The ID that was assigned to the subcontractor for the submittal item. If a non-manager user created the submittal item and chose a manager, they are automatically assigned as the subcontractor of the submittal item. In order to get more info about the subcontractor, use:
GET projects/users to verify the actual name of the user in case the typs is a user (1).
GET companies to determine the name of the company in case the typs is a company (2).
Note that we do not currently support verifying names of roles.

subcontractorType
enum:string
The type of subcontractor associated with the submittal item.
Possible values: 1 (user), 2 (company), 3 (role).

watchers
array: object
A list of project watchers, who can be individual users, roles, or companies.
dueDate
string
The due date for the submittal item, formatted as YYYY-MM-DD in UTC (ISO 8601). For example, 2018-02-15.
requiredOnJobDate
string
The date when the materials are expected to arrive on the construction site, formatted as YYYY-MM-DD in UTC (ISO 8601). For example, 2018-02-15.
leadTime
int
The duration (in days) from the approval of the submittal to delivery of materials or products to the construction site.
requiredDate
string
The date by which the Responsible Contractor must submit the submittal to the submittal manager, formatted as YYYY-MM-DD in UTC (ISO 8601). For example, 2018-02-15.
requiredApprovalDate
string
The date by which approval for the submittal is required, formatted as YYYY-MM-DD in UTC (ISO 8601). For example, 2018-02-15.
submitterDueDate
string
The date by which the subcontractor is expected to submit the submittal to the manager, formatted as YYYY-MM-DD in UTC (ISO 8601). For example, 2018-02-15. This corresponds to the sbc-1 state Waiting for submission.
sentToSubmitter
datetime: ISO 8601
The date and time when the submittal was sent to the subcontractor for review, formatted as YYYY-MM-DDTHH:mm:ss.SSSSSSZ (ISO 8601) in UTC. For example, 2018-02-15T12:09:24.198466Z. This corresponds to transition to the sbc-1 state.
receivedFromSubmitter
datetime: ISO 8601
The date when the submittal was received back from the subcontractor after review, formatted as YYYY-MM-DDTHH:mm:ss.SSSSSSZ (ISO 8601) in UTC. For example, 2018-02-15T12:09:24.198466Z. This corresponds to transition to mgr-1 state Open (Submitted).
submittedBy
string
The Autodesk ID of the user who submitted the submittal item. This is the user who transitioned the item to the manager.
managerDueDate
string
The date by which the manager is expected to prepare the submittal item for review, formatted as YYYY-MM-DD in UTC (ISO 8601). For example, 2018-02-15. This corresponds to the mgr-1 state Open (Submitted).
sentToReview
datetime: ISO 8601
The date and time when the submittal item transitioned to the rev state (Open - In review), formatted as YYYY-MM-DDTHH:mm:ss.SSSSSSZ (ISO 8601) in UTC. For example, 2018-02-15T12:09:24.198466Z.
sentToReviewBy
string
The Autodesk ID of the user who transitioned the item to the rev state (Open - In review).
receivedFromReview
datetime: ISO 8601
The date and time when the submittal item transitioned from the rev state (Open - In Review) to the mgr-2 state (Close and distribute), formatted as YYYY-MM-DD (ISO 8601) in UTC. For example, 2022-03-02T12:09:24Z.
publishedDate
datetime: ISO 8601
The date when the manager closed and distributed the submittal item, in the following format: YYYY-MM-DD (ISO 8601) in UTC. For example, 2018-02-15.
publishedBy
string
The Autodesk ID of the user who published the submittal item.
responseId
string
The ID of the response associated with the submittal item, linking to the specific feedback or action taken.
responseComment
string
The body of the response comment, containing feedback or instructions related to the submittal item.
respondedAt
datetime: ISO 8601
The date and time when the response was added, formatted as YYYY-MM-DDTHH:mm:ss.SSSSSSZ (ISO 8601) in UTC. For example, 2018-02-15T12:09:24.198466Z.
respondedBy
string
The Autodesk ID of the user that gave the response to the submittal item.
packageId
string: UUID
The ID of the package associated with the submittal item.
packageIdentifier
string
The package identifier as displayed in the UI.
packageTitle
string
The title of the package associated with the submittal item.
packageSpecIdentifier
string
The identifier of the submittal spec associated with the package. This value corresponds to the “Spec section” displayed in the UI, such as 1 - Cement.
folderUrn
string
The URN of the folder that contains the attachments associated with the submittal items.
revisionsFoldersUrns
object
An object containing URNs that represent folders associated with the revisions of the submittal item. These URNs can be used to access and identify specific folders related to submittal item revisions within the system.
createdAt
datetime: ISO 8601
The date and time when the submittal item was originally created, formatted as YYYY-MM-DDTHH:mm:ss.SSSSSSZ (ISO 8601) in UTC. For example, 2018-02-15T12:09:24.198466Z.
createdBy
string
The Autodesk ID of the user who created the submittal item.
updatedAt
datetime: ISO 8601
The time and date when the submittal item was last updated, formatted as YYYY-MM-DDTHH:mm:ss.SSSSSSZ (ISO 8601) in UTC. For example, 2018-02-15T12:09:24.198466Z.
updatedBy
string
The Autodesk ID of the user who last updated the submittal item.
permittedActions
array: object
The list of actions the user is allowed to perform on the submittal item.
Example
Successfully retrieved a submittal item.

Request
curl -v 'https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/items/767b5888-2c6a-413d-8487-613966dd64ce' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "id": "b8cc9324-6759-4f07-8ce3-725d5afd4f11",
  "identifier": 1111,
  "customIdentifier": "A-111",
  "customIdentifierHumanReadable": "0001-A-111",
  "typeId": "06fa0c1b-6462-459d-8a38-0aff11bfe868",
  "specId": "62d6f245-b470-4af4-802b-4cb94b5dead1",
  "specIdentifier": "09-5300",
  "specTitle": "Acoustical Ceilings",
  "subsection": "1.05-B",
  "title": "Shop Drawings",
  "description": "Detailed plans by subcontractor, showing project dimensions.",
  "priority": "Low",
  "revision": 0,
  "stateId": "mgr-1",
  "statusId": "1",
  "ballInCourtUsers": [
    "WD43ZJGKDFLFH"
  ],
  "ballInCourtCompanies": [
    "WD43ZJGKDFLFH"
  ],
  "ballInCourtRoles": [
    "WD43ZJGKDFLFH"
  ],
  "ballInCourtType": "reviewer",
  "manager": "WD43ZJGKDFLFH",
  "managerType": "1",
  "subcontractor": "WD43ZJGKDFLFH",
  "subcontractorType": "1",
  "watchers": [
    {
      "id": "224356",
      "userType": "2"
    },
    {
      "id": "3522614",
      "userType": "3"
    }
  ],
  "dueDate": "2018-02-15",
  "requiredOnJobDate": "2018-02-15",
  "leadTime": 100,
  "requiredDate": "2018-02-15",
  "requiredApprovalDate": "2018-02-15",
  "submitterDueDate": "2018-02-15",
  "sentToSubmitter": "2018-02-01T12:09:24.198466Z",
  "receivedFromSubmitter": "2018-02-01T12:09:24.198466Z",
  "submittedBy": "WD43ZJGKDFLFH",
  "managerDueDate": "2018-02-15",
  "sentToReview": "2018-02-01T12:09:24.198466Z",
  "sentToReviewBy": "WD43ZJGKDFLFH",
  "receivedFromReview": "2018-02-01T12:09:24.198466Z",
  "publishedDate": "2018-02-01T12:09:24.198466Z",
  "publishedBy": "WD43ZJGKDFLFH",
  "responseId": "2d46d30b-7dc1-4a65-991d-d739a1381eb8",
  "responseComment": "Revisions required before approval.",
  "respondedAt": "2018-02-01T12:09:24.198466Z",
  "respondedBy": "WD43ZJGKDFLFH",
  "packageId": "e8302552-fc5a-42ac-ba4b-e9de9760c356",
  "packageIdentifier": "222",
  "packageTitle": "my package1",
  "packageSpecIdentifier": "A-500",
  "folderUrn": "urn:adsk.wipprod:fs.file:vf.hvNfeldTPm_aDqRNZgKjD",
  "revisionsFoldersUrns": {
    "0": {
      "folderUrnCreatedAt": "2018-01-28 09:26:36.371607",
      "revision": 0,
      "folderUrn": "urn:adsk.wipprod:fs.folder:co.r04fl5B7QCa1731EeH5dYDQ"
    }
  },
  "createdAt": "2018-02-01T12:09:24.198466Z",
  "createdBy": "WD43ZJGKDFLFH",
  "updatedAt": "2018-04-04T12:09:24.198466Z",
  "updatedBy": "WD43ZJGKDFLFH",
  "permittedActions": [
    {
      "id": "Item::update",
      "fields": {
        "subcontractor": [],
        "manager": []
      },
      "mandatoryFields": [
        ""
      ],
      "transitions": [
        {
          "id": "rev::void",
          "name": "Send to void",
          "stateFrom": {
            "id": "rev",
            "name": "Review"
          },
          "stateTo": {
            "id": "void",
            "name": "Void"
          },
          "transitionFields": [
            "subcontractor",
            "subcontractorType",
            "watchers",
            "responseId"
          ],
          "mandatoryFields": [
            "responseId"
          ],
          "actionId": "ITEM_TRANSITION_REV_VOID"
        }
      ]
    }
  ]
}


Documentation /Autodesk Construction Cloud APIs /API Reference
Items
GET	projects/{projectId}/items/{itemId}/revisions
Retrieves the revision history of a specified submittal item, returning previous versions of its fields and associated workflow details. Each revision contains information about the item’s previous states.

To retrieve the most recent version of a submittal item, call GET item.

For more details about submittal revisions, see the Help documentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/submittals/v2/projects/:projectId/items/:itemId/revisions
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
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

itemId
string
The ID of the submittal item. To find the item ID, call GET items.
Request
Query String Parameters
limit
int
The maximum number of results per page. Possible values: 1- 50. Default value: 20. For example, to limit the response to two results per page, use limit=2.
offset
int
The number of results to skip before starting to return data. For example, to skip the first 20 results, include offset=20 in the query string. For more details, see the JSON API Paging Help documentation.
Response
HTTP Status Code Summary
200
OK
The request was successful, returning a list of item revisions.
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers.
401
Unauthorized
Invalid or missing authorization header. Verify the Bearer token and try again.
403
Forbidden
The user is not authorized to perform this action.
404
Not Found
The specified resource was not found.
500
Internal Server Error
An unexpected error occurred on the server while processing the request.
Response
Body Structure (200)
 Expand all
pagination
object
Describes pagination details for the response, including information about the current page and navigation to other pages.
results
array: object
A list of revisions associated with the specified submittal item.
Example
The request was successful, returning a list of item revisions.

Request
curl -v 'https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/items/767b5888-2c6a-413d-8487-613966dd64ce/revisions' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 10,
    "offset": 100,
    "totalResults": 25,
    "previousUrl": "https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/items/767b5888-2c6a-413d-8487-613966dd64ce/revisions?limit=5&offset=10",
    "nextUrl": null
  },
  "results": [
    {
      "itemId": "767b5888-2c6a-413d-8487-613966dd64ce",
      "revision": 2,
      "manager": "WD43ZJGKDFLFH",
      "managerType": "1",
      "subcontractor": "WD43ZJGKDFLFH",
      "subcontractorType": "1",
      "submitterDueDate": "2018-02-15",
      "sentToSubmitter": "2018-02-01T12:09:24.198466Z",
      "receivedFromSubmitter": "2018-02-01T12:09:24.198466Z",
      "submittedBy": "WD43ZJGKDFLFH",
      "managerDueDate": "2018-02-15",
      "sentToReview": "2018-02-01T12:09:24.198466Z",
      "sentToReviewBy": "WD43ZJGKDFLFH",
      "receivedFromReview": "2018-02-01T12:09:24.198466Z",
      "publishedDate": "2018-02-01T12:09:24.198466Z",
      "publishedBy": "WD43ZJGKDFLFH",
      "responseId": "2d46d30b-7dc1-4a65-991d-d739a1381eb8",
      "responseComment": "Additional details needed on material compliance.",
      "respondedAt": "2024-02-03T12:09:24.198466Z",
      "respondedBy": "WD43ZJGKDFLFH",
      "reviewerDueDate": "2018-02-01T12:09:24.198466Z",
      "steps": [
        {
          "stepId": "d6635799-e973-4c9c-80d8-fb4b3591ef6b",
          "revision": 1,
          "stepNumber": 1,
          "daysToRespond": 10,
          "dueDate": "2024-02-15",
          "startedAt": "2024-03-21T23:15:49.406000Z",
          "completedAt": "2018-02-21T23:04:49.406000Z",
          "createdAt": "2024-03-21T23:04:49.406000Z",
          "updatedAt": "2024-03-24T23:04:49.406000Z",
          "tasks": [
            {
              "taskId": "4d539b8f-c522-4f1c-9743-d7fdfa9e9c9e",
              "stepId": "d6635799-e973-4c9c-80d8-fb4b3591ef6b",
              "itemId": "2df3b4cf-16f4-496e-8173-7125f31e3dd1",
              "revision": 1,
              "assignedTo": "WD43ZJGKDFLFH",
              "assignedToType": "1",
              "isRequired": true,
              "responseId": "2d46d30b-7dc1-4a65-991d-d739a1381eb8",
              "responseComment": "Please revise and resubmit with missing specifications.",
              "respondedAt": "2024-02-03T12:09:24.198466Z",
              "respondedBy": "WD43ZJGKDFLFH",
              "startedAt": "2024-03-21T23:15:49.406Z",
              "completedAt": "2024-03-24T23:04:49.406Z",
              "completedBy": "WD43ZJGKDFLFH",
              "createdAt": "2024-03-21T23:04:49.406Z",
              "updatedAt": "2024-03-24T23:04:49.406Z"
            }
          ]
        }
      ]
    }
  ]
}
Documentation /Autodesk Construction Cloud APIs /API Reference
Items
GET	projects/{projectId}/items/{itemId}/revisions
Retrieves the revision history of a specified submittal item, returning previous versions of its fields and associated workflow details. Each revision contains information about the item’s previous states.

To retrieve the most recent version of a submittal item, call GET item.

For more details about submittal revisions, see the Help documentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/submittals/v2/projects/:projectId/items/:itemId/revisions
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
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

itemId
string
The ID of the submittal item. To find the item ID, call GET items.
Request
Query String Parameters
limit
int
The maximum number of results per page. Possible values: 1- 50. Default value: 20. For example, to limit the response to two results per page, use limit=2.
offset
int
The number of results to skip before starting to return data. For example, to skip the first 20 results, include offset=20 in the query string. For more details, see the JSON API Paging Help documentation.
Response
HTTP Status Code Summary
200
OK
The request was successful, returning a list of item revisions.
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers.
401
Unauthorized
Invalid or missing authorization header. Verify the Bearer token and try again.
403
Forbidden
The user is not authorized to perform this action.
404
Not Found
The specified resource was not found.
500
Internal Server Error
An unexpected error occurred on the server while processing the request.
Response
Body Structure (200)
 Expand all
pagination
object
Describes pagination details for the response, including information about the current page and navigation to other pages.
results
array: object
A list of revisions associated with the specified submittal item.
Example
The request was successful, returning a list of item revisions.

Request
curl -v 'https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/items/767b5888-2c6a-413d-8487-613966dd64ce/revisions' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 10,
    "offset": 100,
    "totalResults": 25,
    "previousUrl": "https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/items/767b5888-2c6a-413d-8487-613966dd64ce/revisions?limit=5&offset=10",
    "nextUrl": null
  },
  "results": [
    {
      "itemId": "767b5888-2c6a-413d-8487-613966dd64ce",
      "revision": 2,
      "manager": "WD43ZJGKDFLFH",
      "managerType": "1",
      "subcontractor": "WD43ZJGKDFLFH",
      "subcontractorType": "1",
      "submitterDueDate": "2018-02-15",
      "sentToSubmitter": "2018-02-01T12:09:24.198466Z",
      "receivedFromSubmitter": "2018-02-01T12:09:24.198466Z",
      "submittedBy": "WD43ZJGKDFLFH",
      "managerDueDate": "2018-02-15",
      "sentToReview": "2018-02-01T12:09:24.198466Z",
      "sentToReviewBy": "WD43ZJGKDFLFH",
      "receivedFromReview": "2018-02-01T12:09:24.198466Z",
      "publishedDate": "2018-02-01T12:09:24.198466Z",
      "publishedBy": "WD43ZJGKDFLFH",
      "responseId": "2d46d30b-7dc1-4a65-991d-d739a1381eb8",
      "responseComment": "Additional details needed on material compliance.",
      "respondedAt": "2024-02-03T12:09:24.198466Z",
      "respondedBy": "WD43ZJGKDFLFH",
      "reviewerDueDate": "2018-02-01T12:09:24.198466Z",
      "steps": [
        {
          "stepId": "d6635799-e973-4c9c-80d8-fb4b3591ef6b",
          "revision": 1,
          "stepNumber": 1,
          "daysToRespond": 10,
          "dueDate": "2024-02-15",
          "startedAt": "2024-03-21T23:15:49.406000Z",
          "completedAt": "2018-02-21T23:04:49.406000Z",
          "createdAt": "2024-03-21T23:04:49.406000Z",
          "updatedAt": "2024-03-24T23:04:49.406000Z",
          "tasks": [
            {
              "taskId": "4d539b8f-c522-4f1c-9743-d7fdfa9e9c9e",
              "stepId": "d6635799-e973-4c9c-80d8-fb4b3591ef6b",
              "itemId": "2df3b4cf-16f4-496e-8173-7125f31e3dd1",
              "revision": 1,
              "assignedTo": "WD43ZJGKDFLFH",
              "assignedToType": "1",
              "isRequired": true,
              "responseId": "2d46d30b-7dc1-4a65-991d-d739a1381eb8",
              "responseComment": "Please revise and resubmit with missing specifications.",
              "respondedAt": "2024-02-03T12:09:24.198466Z",
              "respondedBy": "WD43ZJGKDFLFH",
              "startedAt": "2024-03-21T23:15:49.406Z",
              "completedAt": "2024-03-24T23:04:49.406Z",
              "completedBy": "WD43ZJGKDFLFH",
              "createdAt": "2024-03-21T23:04:49.406Z",
              "updatedAt": "2024-03-24T23:04:49.406Z"
            }
          ]
        }
      ]
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Items
GET	projects/{projectId}/items/{itemId}
Retrieve information about a single submittal item that the user has permission to view. For information about submittal items, see the Help documentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/submittals/v2/projects/:projectId/items/:itemId
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
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

itemId
string
The ID of the submittal item. To find the item ID, call GET items.
Response
HTTP Status Code Summary
200
OK
Successfully retrieved a submittal item.
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers.
401
Unauthorized
Invalid or missing authorization header. Verify the Bearer token and try again.
403
Forbidden
The user is not authorized to perform this action.
404
Not Found
The specified resource was not found.
500
Internal Server Error
An unexpected error occurred on the server while processing the request.
Response
Body Structure (200)
 Expand all
id
string: UUID
The internal, globally unique identifier (UUID) for the submittal item.
identifier
int
The unique ID assigned to the submittal item within the UI. This ID is system-generated and serves as a reference for users interacting with submittal items through the UI. For example, 111.
customIdentifier
string
customIdentifier and customIdentifierHumanReadable relate to the Number column in the UI. Submittal managers assign custom numbers to items (manually or automatically). Custom numbers are configured either in global numbering format: <global number>, or in spec section numbering format: <spec ID>-<sequential number>.
For projects with a global numbering format, both customIdentifier and customIdentifierHumanReadable represent the global number.

For projects with a spec section numbering format (<spec ID>-<sequential number>), customIdentifier represents the sequential number. For example, for a full number of 033100-01, customIdentifier is 01.

Note that for unnumbered items customIdentifier is null.

For more information on custom numbering, see the Help documentation.

customIdentifierHumanReadable
string
customIdentifierHumanReadable and customIdentifier relate to the Number column in the UI. Submittal managers assign custom numbers to items (manually or automatically). Custom numbers are configured either in global numbering format: <global number>, or in spec section numbering format: <spec ID>-<sequential number>.
For projects with a global numbering format, both customIdentifier and customIdentifierHumanReadable represent the global number.

For projects with a spec section numbering format (<spec ID>-<sequential number>), customIdentifierHumanReadable represents the full number - both the spec ID and the sequential number. For example, for a full number of 033100-01, customIdentifierHumanReadable is 033100-01.

Note that for unnumbered items customIdentifierHumanReadable is Unspecified. For spec section numbering it also includes the spec ID. For example, 033100-Unspecified.

For more information on custom numbering, see the Help documentation.

typeId
string
The ID representing the type of submittal item.
specId
string: UUID
The unique identifier (UUID) of the spec assigned to the submittal item.
specIdentifier
string
The identifier of the spec section that is associated with the submittal item. The identifier is assigned to the spec section in the UI.
specTitle
string
The title of the spec associated with the submittal item.
subsection
string
The sub-spec section associated with the submittal item, providing additional categorization within the main spec.
title
string
The title of the submittal item.
description
string
The description of the submittal item.
priority
enum:string
The priority of the submittal item.
Possible values:

Low
Normal
High
revision
int
The revision number of the submittal item, indicating the version of the item in the submittal workflow. For example, 1 for the initial submission or 2 for the first revision.
stateId
enum:string
The current state of the submittal item after the transition.
Possible values:

sbc-1 (Waiting for Submission) - Assigned to the Responsible Contractor, who needs to submit the submittal to the Manager.

mgr-1 (Open - Submitted) - Assigned to the Manager, who needs to prepare the submittal item for review.

rev (Open - In Review) - Under review by the reviewers defined in the submittal item’s review workflow.

mgr-2 (Open - Reviewed) - The review is complete, and the submittal is returned to the Manager, who needs to set the final response and close the submittal.

sbc-2: (Closed) - The submittal has been closed and assigned to the Responsible Contractor.

void (Voided) - The submittal item has been voided.

draft (Draft) - Assigned to the Manager, who must send the submittal item to the Responsible Contractor.

statusId
enum:string
The status of the submittal item.
Possible values: 1 - (Required), 2 - (Open), 3 - (Closed), 4 - (Void), 5 - (Empty), 6 - (Draft).

To retrieve the full list of possible statuses, call GET metadata.

ballInCourtUsers
array: string
The Autodesk IDs of users who are currently assigned to the submittal item at this stage of the workflow.
ballInCourtCompanies
array: string
The member group IDs of the companies currently assigned to the submittal item at this stage of the workflow.
ballInCourtRoles
array: string
The member group IDs of user roles that are currently assigned to the submittal item at this stage of the workflow.
ballInCourtType
enum:string
‘The type of submittal role assigned to the user currently assigned to the submittal item.
Possible values: reviewer, manager, subcontractor.’

manager
string
The ID that was assigned to the manager of the submittal item.
To determine the type of the manager (user, role, or company), refer to the manager type (managerType) attribute. In order to get more info about the manager, use:

GET projects/users to verify the actual name of the user in case the typs is a user (1).
GET companies to determine the name of the company in case the typs is a company (2).
Note that we do not currently support verifying names of roles.

managerType
enum:string
The type of manager associated with the submittal item.
Possible values: 1 (user), 2 (company), 3 (role).

subcontractor
string
The ID that was assigned to the subcontractor for the submittal item. If a non-manager user created the submittal item and chose a manager, they are automatically assigned as the subcontractor of the submittal item. In order to get more info about the subcontractor, use:
GET projects/users to verify the actual name of the user in case the typs is a user (1).
GET companies to determine the name of the company in case the typs is a company (2).
Note that we do not currently support verifying names of roles.

subcontractorType
enum:string
The type of subcontractor associated with the submittal item.
Possible values: 1 (user), 2 (company), 3 (role).

watchers
array: object
A list of project watchers, who can be individual users, roles, or companies.
dueDate
string
The due date for the submittal item, formatted as YYYY-MM-DD in UTC (ISO 8601). For example, 2018-02-15.
requiredOnJobDate
string
The date when the materials are expected to arrive on the construction site, formatted as YYYY-MM-DD in UTC (ISO 8601). For example, 2018-02-15.
leadTime
int
The duration (in days) from the approval of the submittal to delivery of materials or products to the construction site.
requiredDate
string
The date by which the Responsible Contractor must submit the submittal to the submittal manager, formatted as YYYY-MM-DD in UTC (ISO 8601). For example, 2018-02-15.
requiredApprovalDate
string
The date by which approval for the submittal is required, formatted as YYYY-MM-DD in UTC (ISO 8601). For example, 2018-02-15.
submitterDueDate
string
The date by which the subcontractor is expected to submit the submittal to the manager, formatted as YYYY-MM-DD in UTC (ISO 8601). For example, 2018-02-15. This corresponds to the sbc-1 state Waiting for submission.
sentToSubmitter
datetime: ISO 8601
The date and time when the submittal was sent to the subcontractor for review, formatted as YYYY-MM-DDTHH:mm:ss.SSSSSSZ (ISO 8601) in UTC. For example, 2018-02-15T12:09:24.198466Z. This corresponds to transition to the sbc-1 state.
receivedFromSubmitter
datetime: ISO 8601
The date when the submittal was received back from the subcontractor after review, formatted as YYYY-MM-DDTHH:mm:ss.SSSSSSZ (ISO 8601) in UTC. For example, 2018-02-15T12:09:24.198466Z. This corresponds to transition to mgr-1 state Open (Submitted).
submittedBy
string
The Autodesk ID of the user who submitted the submittal item. This is the user who transitioned the item to the manager.
managerDueDate
string
The date by which the manager is expected to prepare the submittal item for review, formatted as YYYY-MM-DD in UTC (ISO 8601). For example, 2018-02-15. This corresponds to the mgr-1 state Open (Submitted).
sentToReview
datetime: ISO 8601
The date and time when the submittal item transitioned to the rev state (Open - In review), formatted as YYYY-MM-DDTHH:mm:ss.SSSSSSZ (ISO 8601) in UTC. For example, 2018-02-15T12:09:24.198466Z.
sentToReviewBy
string
The Autodesk ID of the user who transitioned the item to the rev state (Open - In review).
receivedFromReview
datetime: ISO 8601
The date and time when the submittal item transitioned from the rev state (Open - In Review) to the mgr-2 state (Close and distribute), formatted as YYYY-MM-DD (ISO 8601) in UTC. For example, 2022-03-02T12:09:24Z.
publishedDate
datetime: ISO 8601
The date when the manager closed and distributed the submittal item, in the following format: YYYY-MM-DD (ISO 8601) in UTC. For example, 2018-02-15.
publishedBy
string
The Autodesk ID of the user who published the submittal item.
responseId
string
The ID of the response associated with the submittal item, linking to the specific feedback or action taken.
responseComment
string
The body of the response comment, containing feedback or instructions related to the submittal item.
respondedAt
datetime: ISO 8601
The date and time when the response was added, formatted as YYYY-MM-DDTHH:mm:ss.SSSSSSZ (ISO 8601) in UTC. For example, 2018-02-15T12:09:24.198466Z.
respondedBy
string
The Autodesk ID of the user that gave the response to the submittal item.
packageId
string: UUID
The ID of the package associated with the submittal item.
packageIdentifier
string
The package identifier as displayed in the UI.
packageTitle
string
The title of the package associated with the submittal item.
packageSpecIdentifier
string
The identifier of the submittal spec associated with the package. This value corresponds to the “Spec section” displayed in the UI, such as 1 - Cement.
folderUrn
string
The URN of the folder that contains the attachments associated with the submittal items.
revisionsFoldersUrns
object
An object containing URNs that represent folders associated with the revisions of the submittal item. These URNs can be used to access and identify specific folders related to submittal item revisions within the system.
createdAt
datetime: ISO 8601
The date and time when the submittal item was originally created, formatted as YYYY-MM-DDTHH:mm:ss.SSSSSSZ (ISO 8601) in UTC. For example, 2018-02-15T12:09:24.198466Z.
createdBy
string
The Autodesk ID of the user who created the submittal item.
updatedAt
datetime: ISO 8601
The time and date when the submittal item was last updated, formatted as YYYY-MM-DDTHH:mm:ss.SSSSSSZ (ISO 8601) in UTC. For example, 2018-02-15T12:09:24.198466Z.
updatedBy
string
The Autodesk ID of the user who last updated the submittal item.
permittedActions
array: object
The list of actions the user is allowed to perform on the submittal item.
Example
Successfully retrieved a submittal item.

Request
curl -v 'https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/items/767b5888-2c6a-413d-8487-613966dd64ce' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "id": "b8cc9324-6759-4f07-8ce3-725d5afd4f11",
  "identifier": 1111,
  "customIdentifier": "A-111",
  "customIdentifierHumanReadable": "0001-A-111",
  "typeId": "06fa0c1b-6462-459d-8a38-0aff11bfe868",
  "specId": "62d6f245-b470-4af4-802b-4cb94b5dead1",
  "specIdentifier": "09-5300",
  "specTitle": "Acoustical Ceilings",
  "subsection": "1.05-B",
  "title": "Shop Drawings",
  "description": "Detailed plans by subcontractor, showing project dimensions.",
  "priority": "Low",
  "revision": 0,
  "stateId": "mgr-1",
  "statusId": "1",
  "ballInCourtUsers": [
    "WD43ZJGKDFLFH"
  ],
  "ballInCourtCompanies": [
    "WD43ZJGKDFLFH"
  ],
  "ballInCourtRoles": [
    "WD43ZJGKDFLFH"
  ],
  "ballInCourtType": "reviewer",
  "manager": "WD43ZJGKDFLFH",
  "managerType": "1",
  "subcontractor": "WD43ZJGKDFLFH",
  "subcontractorType": "1",
  "watchers": [
    {
      "id": "224356",
      "userType": "2"
    },
    {
      "id": "3522614",
      "userType": "3"
    }
  ],
  "dueDate": "2018-02-15",
  "requiredOnJobDate": "2018-02-15",
  "leadTime": 100,
  "requiredDate": "2018-02-15",
  "requiredApprovalDate": "2018-02-15",
  "submitterDueDate": "2018-02-15",
  "sentToSubmitter": "2018-02-01T12:09:24.198466Z",
  "receivedFromSubmitter": "2018-02-01T12:09:24.198466Z",
  "submittedBy": "WD43ZJGKDFLFH",
  "managerDueDate": "2018-02-15",
  "sentToReview": "2018-02-01T12:09:24.198466Z",
  "sentToReviewBy": "WD43ZJGKDFLFH",
  "receivedFromReview": "2018-02-01T12:09:24.198466Z",
  "publishedDate": "2018-02-01T12:09:24.198466Z",
  "publishedBy": "WD43ZJGKDFLFH",
  "responseId": "2d46d30b-7dc1-4a65-991d-d739a1381eb8",
  "responseComment": "Revisions required before approval.",
  "respondedAt": "2018-02-01T12:09:24.198466Z",
  "respondedBy": "WD43ZJGKDFLFH",
  "packageId": "e8302552-fc5a-42ac-ba4b-e9de9760c356",
  "packageIdentifier": "222",
  "packageTitle": "my package1",
  "packageSpecIdentifier": "A-500",
  "folderUrn": "urn:adsk.wipprod:fs.file:vf.hvNfeldTPm_aDqRNZgKjD",
  "revisionsFoldersUrns": {
    "0": {
      "folderUrnCreatedAt": "2018-01-28 09:26:36.371607",
      "revision": 0,
      "folderUrn": "urn:adsk.wipprod:fs.folder:co.r04fl5B7QCa1731EeH5dYDQ"
    }
  },
  "createdAt": "2018-02-01T12:09:24.198466Z",
  "createdBy": "WD43ZJGKDFLFH",
  "updatedAt": "2018-04-04T12:09:24.198466Z",
  "updatedBy": "WD43ZJGKDFLFH",
  "permittedActions": [
    {
      "id": "Item::update",
      "fields": {
        "subcontractor": [],
        "manager": []
      },
      "mandatoryFields": [
        ""
      ],
      "transitions": [
        {
          "id": "rev::void",
          "name": "Send to void",
          "stateFrom": {
            "id": "rev",
            "name": "Review"
          },
          "stateTo": {
            "id": "void",
            "name": "Void"
          },
          "transitionFields": [
            "subcontractor",
            "subcontractorType",
            "watchers",
            "responseId"
          ],
          "mandatoryFields": [
            "responseId"
          ],
          "actionId": "ITEM_TRANSITION_REV_VOID"
        }
      ]
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Items
POST	projects/{projectId}/items:validate-custom-identifier
Validates a custom identifier for a submittal item in a project. It ensures the identifier is not currently in use and adheres to the required formatting rules. Use this endpoint to validate a custom identifier you intend to use.

For information about custom numbering in Submittals, see the Help documentation.

For details on validating custom identifiers in the Submittal workflow, see the Create Submittal Item tutorial.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/construction/submittals/v2/projects/:projectId/items:validate-custom-identifier
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
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Request
Query String Parameters
specId
string: UUID
The item spec ID. This parameter is only required when the project is in spec sequence type (as opposed to global sequence).
To verify the sequence type, call GET metadata, and check customIdentifierSequenceType.

To get the spec ID call GET specs, and select the relevant ID (id).

Request
Body Structure
customIdentifier*
string
The customIdentifier is used to ensure that the chosen identifier adheres to format rules and is unique within the project. Submittal managers can assign custom numbers manually or automatically.
When validating a custom identifier, consider the following rules:

Ensure the identifier is unique within the project.
For global sequences, ensure it is unique within the entire project.
For spec sequences, ensure it is unique within the specific spec section.
Spec sequence is in the format <spec_identifier>-<sequential_number>. You only need to specify the sequential number. The full number - <spec_identifier>-<sequential_number> - appears in the response payload in the customIdentifierHumanReadable attribute.
Regardless of whether the project uses a global or spec sequence, you should always provide only the sequential number portion without the spec ID when sending the customIdentifier.

For more information on custom numbering, see the Help documentation.

* Required
Response
HTTP Status Code Summary
204
No Content
Validating a Custom Identifier.
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers.
401
Unauthorized
Invalid or missing authorization header. Verify the Bearer token and try again.
403
Forbidden
The user is not authorized to perform this action.
404
Not Found
The specified resource was not found.
409
Conflict
The custom identifier is already taken
500
Internal Server Error
An unexpected error occurred on the server while processing the request.
Response
Body Structure (204)
Response for 204 has no body.

Example
Validating a Custom Identifier.

Request
curl -v 'https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/items:validate-custom-identifier' \
  -X 'POST' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a' \
  -H 'Content-Type: application/json' \
  -d '{
        "customIdentifier": "01"
      }'
Response
204 No Content

Documentation /Autodesk Construction Cloud APIs /API Reference
Items
GET	projects/{projectId}/items:next-custom-identifier
Retrieves the next available custom identifier for a submittal item in a project. The identifier is generated based on specific rules:

Sequentially increments the last created item’s number, relative to either the whole project for a global sequence or the specific spec for a spec sequence.
Skips numbers already in use.
Reuses deleted or cleared numbers.
Increments digits appropriately, and manages leading zeros without increasing character count unless necessary.
For information about custom numbering in Submittals, see the Help documentation.

For details on using custom identifiers in the Submittal workflow, see the Create Submittal Item tutorial.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/submittals/v2/projects/:projectId/items:next-custom-identifier
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
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Request
Query String Parameters
specId
string: UUID
The item spec ID. This parameter is only required when the project is in spec sequence type (as opposed to global sequence).
To verify the sequence type, call GET metadata, and check customIdentifierSequenceType.

To get the spec ID, call GET specs, and select the relevant ID (id).

Response
HTTP Status Code Summary
200
OK
Details of the last created and the next available custom identifiers.
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers.
401
Unauthorized
Invalid or missing authorization header. Verify the Bearer token and try again.
403
Forbidden
The user is not authorized to perform this action.
404
Not Found
The specified resource was not found.
500
Internal Server Error
An unexpected error occurred on the server while processing the request.
Response
Body Structure (200)
previousCustomIdentifier
string
The last created custom identifier.
nextCustomIdentifier
string
The next available custom identifier for the project.
Example
Details of the last created and the next available custom identifiers.

Request
curl -v 'https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/items:next-custom-identifier' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "previousCustomIdentifier": "0001",
  "nextCustomIdentifier": "0002"
}

Documentation /Autodesk Construction Cloud APIs /API Reference
ItemTypes
GET	projects/{projectId}/item-types
Retrieves all submittal itme types for the specified project. Submittal item types categorize the various submittal items submitted for review and approval in a construction project. Examples of submittal item types could be Attic Stock or Sample.

For more information about submittal item types, see the Help documentation.

For details on using submittal item types, refer to the Create Submittal Item tutorial.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/submittals/v2/projects/:projectId/item-types
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
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Request
Query String Parameters
limit
int
The maximum number of results per page. Possible values: 1- 50. Default value: 20. For example, to limit the response to two results per page, use limit=2.
offset
int
The number of results to skip before starting to return data. For example, to skip the first 20 results, include offset=20 in the query string. For more details, see the JSON API Paging Help documentation.
Response
HTTP Status Code Summary
200
OK
A list of item types.
401
Unauthorized
Invalid or missing authorization header. Verify the Bearer token and try again.
403
Forbidden
The user is not authorized to perform this action.
404
Not Found
The specified resource was not found.
500
Internal Server Error
An unexpected error occurred on the server while processing the request.
Response
Body Structure (200)
 Expand all
pagination
object
Describes pagination details for the response, including information about the current page and navigation to other pages.
results
array: object
The list of submittal types.
Example
A list of item types.

Request
curl -v 'https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/item-types' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 10,
    "offset": 100,
    "totalResults": 25,
    "previousUrl": "https://developer.api.autodesk.com/construction/submittals/v2/projects/87e0e671-7837-4bee-91de-93fd3af9eb53/item-types?limit=5&offset=10",
    "nextUrl": "https://developer.api.autodesk.com/construction/submittals/v2/projects/87e0e671-7837-4bee-91de-93fd3af9eb53/item-types?limit=5"
  },
  "results": [
    {
      "id": "5bab7f9b-61cf-45bc-8bce-f88ddd9d380e",
      "key": "my-type",
      "value": "Attic Stock",
      "platformId": "attic stock",
      "isActive": true,
      "isInUse": true,
      "createdBy": "WD43ZJGKDFLFH",
      "createdAt": "2018-02-01T12:09:24.198466Z",
      "updatedAt": "2018-02-01T12:09:24.198466Z",
      "updatedBy": "WD43ZJGKDFLFH"
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
ItemTypes
GET	projects/{projectId}/item-types/{id}
Retrieve the information about a single submittal type. For more information about submittal types, see the Help documnentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/submittals/v2/projects/:projectId/item-types/:id
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
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

id
string
The ID of the submittal item to retrieve revisions for. To obtain this ID, call GET items.
Response
HTTP Status Code Summary
200
OK
Successful retrieval of item type
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers.
401
Unauthorized
Invalid or missing authorization header. Verify the Bearer token and try again.
403
Forbidden
The user is not authorized to perform this action.
404
Not Found
The specified resource was not found.
500
Internal Server Error
An unexpected error occurred on the server while processing the request.
Response
Body Structure (200)
id
string: UUID
The internal, globally unique identifier (UUID) for the item type.
key
string
Not relevant
value
string
The name of the submittal item type.
platformId
string
Not relevant
isActive
boolean
true: (default) if the submittal item type has not been deleted.
false: if the submittal item type has been deleted.

isInUse
boolean
true: if the submittal item type is currently associated with a submittal item.
false: if the submittal item type is not currently associated with a submittal item.

createdBy
string
The Autodesk ID of the user who created the submittal item type.
createdAt
datetime: ISO 8601
The date and time when the submittal item type was originally created.
updatedAt
datetime: ISO 8601
The date and time when the submittal item type was last updated.
updatedBy
string
The Autodesk ID of the user who last updated the submittal item type.
Example
Successful retrieval of item type

Request
curl -v 'https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/item-types/:id' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "id": "5bab7f9b-61cf-45bc-8bce-f88ddd9d380e",
  "key": "my-type",
  "value": "Attic Stock",
  "platformId": "attic stock",
  "isActive": true,
  "isInUse": true,
  "createdBy": "WD43ZJGKDFLFH",
  "createdAt": "2018-02-01T12:09:24.198466Z",
  "updatedAt": "2018-02-01T12:09:24.198466Z",
  "updatedBy": "WD43ZJGKDFLFH"
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Metadata
GET	projects/{projectId}/metadata
Retrieves project metadata and static values needed for creating submittal items and translating retrieved data.

This endpoint serves two main purposes:

To retrieve static values, such as submittal roles, user types, and statuses.
To obtain project-specific information, like the custom identifier sequence type, which indicates whether the project uses a global or spec sequence.
For detailed steps on creating submittal items, refer to the Create Submittal Item tutorial.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/submittals/v2/projects/:projectId/metadata
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
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Response
HTTP Status Code Summary
200
OK
A successfully retrieved submittal project’s metadata.
401
Unauthorized
Invalid or missing authorization header. Verify the Bearer token and try again.
403
Forbidden
The user is not authorized to perform this action.
404
Not Found
The specified resource was not found.
500
Internal Server Error
An unexpected error occurred on the server while processing the request.
Response
Body Structure (200)
 Expand all
id
string: UUID
The unique identifier (UUID) for the metadata object.
submittalRoles
array: object
A list of submittal roles within the project.
attachmentUrnTypes
array: object
A list of attachment URN types.
itemTypes
array: object
A list of submittal item types. This is the same as calling GET item-types
adminMappingsSubmittalRoles
array: object
A list of admin mappings for submittal roles.
userTypes
array: object
Types of users, such as individual users, companies, and roles.
statuses
array: object
A list of statuses representing different stages of a submittal item.
responses
array: object
A list of responses.This is the same as calling GET responses
attachmentCategories
array: object
A list of attachment categories.
attachmentTypes
array: object
A list of attachment types.
isManagerMappingDefined
boolean
true: if there is at least one manager mapping in the project.
false: if there are no manager mappings in the project.

noPackagesInProject
boolean
true: if there are no packages in the project.
false: if there are packages in the project.

noItemsInProject
boolean
true: if there are no submittal items in the project.
false: if there are submittal items in the project.

responseCategories
array: object
A list of categories for responses to submittals.
defaultValues
object
An object containing the default values for various settings and configurations in the project.
customIdentifierSequenceType
enum:string
The custom numbering sequence type for the current project. Possible values: 1 (Global sequence), 2 (Spec sequence).
Example
A successfully retrieved submittal project’s metadata.

Request
curl -v 'https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/metadata' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "id": "e8302552-fc5a-42ac-ba4b-e9de9760c356",
  "submittalRoles": [
    {
      "id": "4",
      "key": "admin",
      "value": "Admin"
    }
  ],
  "attachmentUrnTypes": [
    {
      "id": "2",
      "key": "dm",
      "value": "DM"
    }
  ],
  "itemTypes": [
    {
      "id": "5bab7f9b-61cf-45bc-8bce-f88ddd9d380e",
      "key": "my-type",
      "value": "Attic Stock",
      "platformId": "attic stock",
      "isActive": true,
      "isInUse": true,
      "createdBy": "WD43ZJGKDFLFH",
      "createdAt": "2018-02-01T12:09:24.198466Z",
      "updatedAt": "2018-02-01T12:09:24.198466Z",
      "updatedBy": "WD43ZJGKDFLFH"
    }
  ],
  "adminMappingsSubmittalRoles": [
    {
      "id": "4",
      "key": "admin",
      "value": "Admin"
    }
  ],
  "userTypes": [
    {
      "id": "2",
      "key": "company",
      "value": "Company"
    }
  ],
  "statuses": [
    {
      "id": "2",
      "key": "open",
      "value": "Open"
    }
  ],
  "responses": [
    {
      "id": "5bab7f9b-61cf-45bc-8bce-f88ddd9d380e",
      "key": "my response",
      "value": "Approved",
      "platformId": "approved",
      "isActive": false,
      "categoryId": "1",
      "isApproval": false,
      "isInUse": false,
      "createdBy": "WD43ZJGKDFLFH",
      "createdAt": "2018-02-01T12:09:24.198466Z",
      "updatedAt": "2018-02-01T12:09:24.198466Z",
      "updatedBy": "WD43ZJGKDFLFH"
    }
  ],
  "attachmentCategories": [
    {
      "id": "2",
      "key": "for_review",
      "value": "For Review"
    }
  ],
  "attachmentTypes": [
    {
      "id": "2",
      "key": "photo",
      "value": "Photo"
    }
  ],
  "isManagerMappingDefined": false,
  "noPackagesInProject": false,
  "noItemsInProject": false,
  "responseCategories": [
    {
      "id": "1",
      "value": "Approved",
      "isApproval": "true"
    }
  ],
  "defaultValues": {
    "watchers": [
      {
        "id": "224356",
        "userType": "2"
      },
      {
        "id": "3522614",
        "userType": "3"
      }
    ],
    "manager": "WD43ZJGKDFLFH",
    "reviewTime": 7,
    "updatedAt": "2018-02-01T12:09:24.198466Z",
    "updatedBy": "WD43ZJGKDFLFH"
  },
  "customIdentifierSequenceType": "1"
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Packages
GET	projects/{projectId}/packages
Retrieve all the packages for the specified project. For information about packages, see the Help documentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/submittals/v2/projects/:projectId/packages
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
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Request
Query String Parameters
limit
int
The maximum number of results per page. Possible values: 1- 50. Default value: 20. For example, to limit the response to two results per page, use limit=2.
offset
int
The number of results to skip before starting to return data. For example, to skip the first 20 results, include offset=20 in the query string. For more details, see the JSON API Paging Help documentation.
sort
string
Sort packages by specified fields. Separate multiple values with commas. To sort in descending or ascending order, add desc or asc after the sort criteria. For example, spec asc.
Possible values: id, identifier, title, description, spec, spec.identifier.

filter[identifier]
string
Filter packages with the specified package ID (the package ID in the UI). You can specify multiple values. Separate multiple values with commas. For example, filter[identifier]=2.
filter[title]
string
Filter packages with the specified title. You can specify multiple values. Separate multiple values with commas. For example, filter[title]=Structural Steel.
filter[specId]
string
Filter packages with the associated specified spec section internal, globally unique ID (UUID). You can specify multiple values. Separate multiple values with commas. For example, filter[specId]=b4aa3864-5706-4a7b-b06c-a792e8b2df23.
filter[spec.identifier]
string
Filter packages with the associated specified section ID (the spec section ID in the UI). You can specify multiple values. Separate multiple values with commas. For example, filter[identifier]=2.
search
string
Search for packages by querying a specified string within specific fields (identifier, title, spec.identifier), and retrieve the associated packages that match the search criteria. This includes packages where the string matches part of a field. For example, search=1.
Response
HTTP Status Code Summary
200
OK
Successful retrieval of packages
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers.
401
Unauthorized
Invalid or missing authorization header. Verify the Bearer token and try again.
403
Forbidden
The user is not authorized to perform this action.
404
Not Found
The specified resource was not found.
500
Internal Server Error
An unexpected error occurred on the server while processing the request.
Response
Body Structure (200)
 Expand all
pagination
object
Describes pagination details for the response, including information about the current page and navigation to other pages.
results
array: object
The list of packages.
Example
Successful retrieval of packages

Request
curl -v 'https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/packages' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 10,
    "offset": 100,
    "totalResults": 25,
    "previousUrl": "https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/settings/mappings?offset=10&limit=100",
    "nextUrl": null
  },
  "results": [
    {
      "id": "e8302552-fc5a-42ac-ba4b-e9de9760c356",
      "specId": "e6111f96-8437-491e-a1ae-16fd53f0cbef",
      "title": "my package1",
      "identifier": 222,
      "description": "Electrical specifications",
      "specIdentifier": "A-500",
      "permittedActions": [
        {
          "id": "Item::update",
          "fields": {
            "subcontractor": [],
            "manager": []
          },
          "mandatoryFields": [
            ""
          ],
          "transitions": [
            {
              "id": "rev::void",
              "name": "Send to void",
              "stateFrom": {
                "id": "rev",
                "name": "Review"
              },
              "stateTo": {
                "id": "void",
                "name": "Void"
              },
              "transitionFields": [
                "subcontractor",
                "subcontractorType",
                "watchers",
                "responseId"
              ],
              "mandatoryFields": [
                "responseId"
              ],
              "actionId": "ITEM_TRANSITION_REV_VOID"
            }
          ]
        }
      ]
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Packages
GET	projects/{projectId}/packages/{id}
Retrieve details about a single package. For information about packages, see the Help documentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/submittals/v2/projects/:projectId/packages/:id
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
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

id
string
The ID of the submittal item to retrieve revisions for. To obtain this ID, call GET items.
Response
HTTP Status Code Summary
200
OK
A successfully retrieved package
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers.
401
Unauthorized
Invalid or missing authorization header. Verify the Bearer token and try again.
403
Forbidden
The user is not authorized to perform this action.
404
Not Found
The specified resource was not found.
500
Internal Server Error
An unexpected error occurred on the server while processing the request.
Response
Body Structure (200)
 Expand all
id
string: UUID
The internal, globally unique identifier (UUID) for the package.
specId
string: UUID
The internal, globally unique identifier (UUID) of the spec associated with the package.
title
string
The title of the package.
identifier
int
The unique ID assigned to the package within the UI.
description
string
The description of the package.
specIdentifier
string
The unique ID of the spec assigned to the package in the UI, specific to each project.
permittedActions
array: object
The list of actions the user is allowed to perform on the submittal item.
Example
A successfully retrieved package

Request
curl -v 'https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/packages/:id' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "id": "e8302552-fc5a-42ac-ba4b-e9de9760c356",
  "specId": "e6111f96-8437-491e-a1ae-16fd53f0cbef",
  "title": "my package1",
  "identifier": 222,
  "description": "Electrical specifications",
  "specIdentifier": "A-500",
  "permittedActions": [
    {
      "id": "Item::update",
      "fields": {
        "subcontractor": [],
        "manager": []
      },
      "mandatoryFields": [
        ""
      ],
      "transitions": [
        {
          "id": "rev::void",
          "name": "Send to void",
          "stateFrom": {
            "id": "rev",
            "name": "Review"
          },
          "stateTo": {
            "id": "void",
            "name": "Void"
          },
          "transitionFields": [
            "subcontractor",
            "subcontractorType",
            "watchers",
            "responseId"
          ],
          "mandatoryFields": [
            "responseId"
          ],
          "actionId": "ITEM_TRANSITION_REV_VOID"
        }
      ]
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Responses
GET	projects/{projectId}/responses
Retrieves all the responses for the specified project.

For more information about submittal item responses, see the Help documentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/submittals/v2/projects/:projectId/responses
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
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Request
Query String Parameters
limit
int
The maximum number of results per page. Possible values: 1- 50. Default value: 20. For example, to limit the response to two results per page, use limit=2.
offset
int
The number of results to skip before starting to return data. For example, to skip the first 20 results, include offset=20 in the query string. For more details, see the JSON API Paging Help documentation.
Response
HTTP Status Code Summary
200
OK
A list of responses for the specified project.
401
Unauthorized
Invalid or missing authorization header. Verify the Bearer token and try again.
403
Forbidden
The user is not authorized to perform this action.
404
Not Found
The specified resource was not found.
500
Internal Server Error
An unexpected error occurred on the server while processing the request.
Response
Body Structure (200)
 Expand all
pagination
object
Describes pagination details for the response, including information about the current page and navigation to other pages.
results
array: object
The list of all responses for the specified project.
Example
A list of responses for the specified project.

Request
curl -v 'https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/responses' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 10,
    "offset": 100,
    "totalResults": 25,
    "previousUrl": "https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/responses?limit=5&offset=10",
    "nextUrl": null
  },
  "results": [
    {
      "id": "5bab7f9b-61cf-45bc-8bce-f88ddd9d380e",
      "key": "my response",
      "value": "Approved",
      "platformId": "approved",
      "isActive": false,
      "categoryId": "1",
      "isApproval": false,
      "isInUse": false,
      "createdBy": "WD43ZJGKDFLFH",
      "createdAt": "2018-02-01T12:09:24.198466Z",
      "updatedAt": "2018-02-01T12:09:24.198466Z",
      "updatedBy": "WD43ZJGKDFLFH"
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Responses
GET	projects/{projectId}/responses/{id}
Retrieve details about a single submittal response for the specified project, see the Help documentation.

Note that this endpoint is not compatible with BIM 360 projects.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/submittals/v2/projects/:projectId/responses/:id
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
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

id
string
The ID of the submittal item to retrieve revisions for. To obtain this ID, call GET items.
Response
HTTP Status Code Summary
200
OK
Successful retrieval of response
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers.
401
Unauthorized
Invalid or missing authorization header. Verify the Bearer token and try again.
403
Forbidden
The user is not authorized to perform this action.
404
Not Found
The specified resource was not found.
500
Internal Server Error
An unexpected error occurred on the server while processing the request.
Response
Body Structure (200)
id
string: UUID
The internal, globally unique identifier (UUID) for the response.
key
string
Not relevant
value
string
The content of the response.
platformId
string
Not relevant
isActive
boolean
true: if the response was not deleted.
false: if the response was deleted.

categoryId
string
The type of response. Possible values: 1 (Approved), 2 (Revise and submit), 3 (Rejected).
isApproval
boolean
true: settings this response for a submittal item means an approval.
false: settings this response for a submittal item means dis-approval.

This attribute is taken from the related categoryId

isInUse
boolean
true: if the response is currently associated with a submittal item.
false: if the response is not currently associated with a submittal item.

createdBy
string
The Autodesk ID of the user who created the response.
createdAt
datetime: ISO 8601
The time and date when the response was created.
updatedAt
datetime: ISO 8601
The time and date when the response was last updated.
updatedBy
string
The Autodesk ID of the user who last updated the response.
Example
Successful retrieval of response

Request
curl -v 'https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/responses/:id' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "id": "5bab7f9b-61cf-45bc-8bce-f88ddd9d380e",
  "key": "my response",
  "value": "Approved",
  "platformId": "approved",
  "isActive": false,
  "categoryId": "1",
  "isApproval": false,
  "isInUse": false,
  "createdBy": "WD43ZJGKDFLFH",
  "createdAt": "2018-02-01T12:09:24.198466Z",
  "updatedAt": "2018-02-01T12:09:24.198466Z",
  "updatedBy": "WD43ZJGKDFLFH"
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Settings - Mappings
GET	projects/{projectId}/settings/mappings
Retrieves users, roles, and companies assigned the manager role in the current project. Only users, roles, or companies retrieved from this endpoint can be set as a manager in a submittal item.

For more information about submittal administration, see the Help documentation.

For information on how mappings are used in the Submittal workflow, see the Create Submittal Item tutorial.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/submittals/v2/projects/:projectId/settings/mappings
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
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Request
Query String Parameters
limit
int
The maximum number of results per page. Possible values: 1- 50. Default value: 20. For example, to limit the response to two results per page, use limit=2.
offset
int
The number of results to skip before starting to return data. For example, to skip the first 20 results, include offset=20 in the query string. For more details, see the JSON API Paging Help documentation.
filter[autodeskId]
string
Comma-seperated list of Autodesk IDs for which the mappings will be returned.
Response
HTTP Status Code Summary
200
OK
Successful retrieval of user-role mappings.
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers.
401
Unauthorized
Invalid or missing authorization header. Verify the Bearer token and try again.
403
Forbidden
The user is not authorized to perform this action.
404
Not Found
The specified resource was not found.
500
Internal Server Error
An unexpected error occurred on the server while processing the request.
Response
Body Structure (200)
 Expand all
pagination
object
Describes pagination details for the response, including information about the current page and navigation to other pages.
results
array: object
A list of user-role mappings defined by administrators.
Example
Successful retrieval of user-role mappings.

Request
curl -v 'https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/settings/mappings' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 10,
    "offset": 100,
    "totalResults": 25,
    "previousUrl": "https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/settings/mappings?offset=10&limit=100",
    "nextUrl": null
  },
  "results": [
    {
      "id": "ab1754f6-92f1-4caa-87df-e05ba7b917a6",
      "userType": "1",
      "oxygenId": "WD43ZJGKDFLFH",
      "autodeskId": "WD43ZJGKDFLFH",
      "submittalsRole": "1",
      "updatedBy": "WD43ZJGKDFLFH",
      "updatedAt": "2024-02-11T14:14:30.225223Z",
      "createdBy": "WD43ZJGKDFLFH",
      "createdAt": "2024-02-11T14:14:30.225223Z"
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Specs
GET	projects/{projectId}/specs
Retrieve all the spec sections for the specified project. For information about spec sections, see the Help documentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/submittals/v2/projects/:projectId/specs
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
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Request
Query String Parameters
limit
int
The maximum number of results per page. Possible values: 1- 50. Default value: 20. For example, to limit the response to two results per page, use limit=2.
offset
int
The number of results to skip before starting to return data. For example, to skip the first 20 results, include offset=20 in the query string. For more details, see the JSON API Paging Help documentation.
search
string
Search for spec sections by querying a specified string within specific fields (identifier, title), and retrieve the associated items that match the search criteria. This includes spec sections where the string matches part of a field. For example, search=1.
sort
string
Sort spec sections by specified fields. Separate multiple values with commas. To sort in descending or ascending order, add desc or asc after the sort criteria. For example, identifier asc. Possible values: identifier, title.
filter[identifier]
string
Filter spec sections with the specified spec section ID (the spec section ID in the UI). You can specify multiple values. Separate multiple values with commas. For example, filter[identifier]=2.
Response
HTTP Status Code Summary
200
OK
Successful retrieval of spec sections
403
Forbidden
Unauthorized
Response
Body Structure (200)
 Expand all
pagination
object
Describes pagination details for the response, including information about the current page and navigation to other pages.
results
array: object
The list of spec sections.
Example
Successful retrieval of spec sections

Request
curl -v 'https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/specs' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 10,
    "offset": 100,
    "totalResults": 25,
    "previousUrl": "https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/settings/mappings?offset=10&limit=100",
    "nextUrl": null
  },
  "results": [
    {
      "id": "e6111f96-8437-491e-a1ae-16fd53f0cbef",
      "title": "Materials",
      "identifier": "500",
      "createdBy": "WD43ZJGKDFLFH",
      "createdAt": "2018-02-01T12:09:24.198466Z",
      "updatedBy": "WD43ZJGKDFLFH",
      "updatedAt": "2018-02-01T12:09:24.198466Z"
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Specs
GET	projects/{projectId}/specs/{id}
Retrieve the details about a single spec section. For information about spec sections, see the Help documentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/submittals/v2/projects/:projectId/specs/:id
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
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

id
string
The ID of the submittal item to retrieve revisions for. To obtain this ID, call GET items.
Response
HTTP Status Code Summary
200
OK
Successful request to create a new spec section.
403
Forbidden
Unauthorized
Response
Body Structure (200)
id
string: UUID
The internal, globally unique identifier (UUID) for the spec section.
title
string
The title of the spec section.
identifier
string
The unique ID assigned to the spec section within the UI.
createdBy
string
The Autodesk ID of the user who created the spec section.
createdAt
datetime: ISO 8601
The time and date when the spec section was created.
updatedBy
string
The Autodesk ID of the user who last updated the spec section.
updatedAt
datetime: ISO 8601
The time and date when spec section was last updated.
Example
Successful request to create a new spec section.

Request
curl -v 'https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/specs/:id' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "id": "e6111f96-8437-491e-a1ae-16fd53f0cbef",
  "title": "Materials",
  "identifier": "500",
  "createdBy": "WD43ZJGKDFLFH",
  "createdAt": "2018-02-01T12:09:24.198466Z",
  "updatedBy": "WD43ZJGKDFLFH",
  "updatedAt": "2018-02-01T12:09:24.198466Z"
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Steps
GET	projects/{projectId}/items/{itemId}/steps
Retrieves a list of review steps associated with a specific submittal item.

Review steps represent sequential stages in the submittal review process. Each step contains one or more tasks, which assign responsibility for completing specific actions within that step. Tasks are tied to reviewers (represented in the UI as members, roles, or companies) and must be completed to progress to the next review step.

For a detailed overview of the submittal workflow, see the Manage Submittal Item Transitions tutorial.

For more information about submittals and their lifecycle, see the Help documentation.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/submittals/v2/projects/:projectId/items/:itemId/steps
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
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

itemId
string
The ID of the submittal item. To find the item ID, call GET items.
Request
Query String Parameters
limit
int
The maximum number of results per page. Possible values: 1- 50. Default value: 20. For example, to limit the response to two results per page, use limit=2.
offset
int
The number of results to skip before starting to return data. For example, to skip the first 20 results, include offset=20 in the query string. For more details, see the JSON API Paging Help documentation.
Response
HTTP Status Code Summary
200
OK
Review steps for the submittal item successfully retrieved.
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers.
401
Unauthorized
Invalid or missing authorization header. Verify the Bearer token and try again.
403
Forbidden
The user is not authorized to perform this action.
404
Not Found
The specified resource was not found.
500
Internal Server Error
An unexpected error occurred on the server while processing the request.
Response
Body Structure (200)
 Expand all
pagination
object
Describes pagination details for the response, including information about the current page and navigation to other pages.
results
array: object
Review steps associated with the specified submittal item.
Example
Review steps for the submittal item successfully retrieved.

Request
curl -v 'https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/items/767b5888-2c6a-413d-8487-613966dd64ce/steps' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 10,
    "offset": 100,
    "totalResults": 25,
    "previousUrl": "https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/items/767b5888-2c6a-413d-8487-613966dd64ce/steps?limit=5&offset=10",
    "nextUrl": null
  },
  "results": [
    {
      "id": "84eb33cd-4a42-42b7-95dd-3900035c3407",
      "itemId": "2df3b4cf-16f4-496e-8173-7125f31e3dd1",
      "status": "in-progress",
      "stepNumber": 1,
      "daysToRespond": 10,
      "dueDate": "2024-02-15",
      "tasks": [
        {
          "id": "4d539b8f-c522-4f1c-9743-d7fdfa9e9c9e",
          "stepId": "d6635799-e973-4c9c-80d8-fb4b3591ef6b",
          "status": "completed",
          "assignedTo": "WD43ZJGKDFLFH",
          "assignedToType": "1",
          "isRequired": true,
          "stepDueDate": "2024-02-15",
          "responseId": "2d46d30b-7dc1-4a65-991d-d739a1381eb8",
          "responseComment": "Approved without changes.",
          "respondedAt": "2024-02-03T12:09:24.198466Z",
          "respondedBy": "WD43ZJGKDFLFH",
          "createdAt": "2024-03-21T23:04:49.406Z",
          "createdBy": "WD43ZJGKDFLFH",
          "updatedAt": "2024-03-24T23:04:49.406674Z",
          "updatedBy": "WD43ZJGKDFLFH",
          "startedAt": "2024-03-21T23:15:49.406894Z",
          "completedAt": "2024-03-24T23:04:49.4066344Z",
          "completedBy": "WD43ZJGKDFLFH",
          "permittedActions": [
            {
              "id": "Task::partial_update",
              "fields": {
                "responseComment": [],
                "responseId": []
              },
              "mandatoryFields": [
                "responseId"
              ],
              "transitions": [
                ""
              ]
            }
          ]
        }
      ],
      "createdAt": "2024-03-21T23:04:49.406Z",
      "createdBy": "WD43ZJGKDFLFH",
      "updatedAt": "2024-03-24T23:04:49.406Z",
      "updatedBy": "WD43ZJGKDFLFH",
      "startedAt": "2024-03-21T23:15:49.406Z",
      "completedAt": "2024-03-24T23:04:49.406Z",
      "permittedActions": [
        {
          "id": "Step::overwrite_step",
          "fields": {
            "tasks": []
          },
          "mandatoryFields": [
            "tasks"
          ],
          "transitions": [
            ""
          ]
        }
      ]
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Steps
GET	projects/{projectId}/items/{itemId}/steps/{stepId}
Retrieves information about a single review step associated with a submittal item.

A review step is a stage in the submittal review process that may include one or more tasks, each assigning responsibility to a reviewer (represented in the UI as a Member, Role, or Company) for completing specific actions.

For a detailed overview of the submittal workflow, see the Manage Submittal Item Transitions tutorial.

For more information about submittals and their lifecycle, see the Help documentation.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/submittals/v2/projects/:projectId/items/:itemId/steps/:stepId
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
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

itemId
string
The ID of the submittal item. To find the item ID, call GET items.
stepId
string
The ID of the review step associated with the submittal item. To find the step ID, call GET steps.
Response
HTTP Status Code Summary
200
OK
Submittal item step successfully retrieved.
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers.
401
Unauthorized
Invalid or missing authorization header. Verify the Bearer token and try again.
403
Forbidden
The user is not authorized to perform this action.
404
Not Found
The specified resource was not found.
500
Internal Server Error
An unexpected error occurred on the server while processing the request.
Response
Body Structure (200)
 Expand all
id
string: UUID
The internal, globally unique identifier (UUID) for the step.
itemId
string: UUID
The ID of the item associated with the step.
status
enum:string
The current status of the step. Possible values: not-started, in-progress, completed.
stepNumber
number
The number representing the order of the steps, where 1 is the first step.
daysToRespond
number
Specifies a dynamic due date. When the step starts, the due date is calculated based on this field.
dueDate
string
The due date of the step in the format YYYY-MM-DD (ISO 8601) in UTC. For example, 2018-02-15.
tasks
array: object
The list of tasks associated with the step.
createdAt
datetime: ISO 8601
The date and time when the step was created, formatted as YYYY-MM-DDTHH:mm:ss.SSSSSSZ (ISO 8601) in UTC. For example, 2025-01-20T12:00:00.198466Z.
createdBy
string
The Autodesk ID of the user that created the step.
updatedAt
datetime: ISO 8601
The date and time when the step was last updated, formatted as YYYY-MM-DDTHH:mm:ss.SSSSSSZ (ISO 8601) in UTC. For example, 2025-01-20T12:00:00.198466Z.
updatedBy
string
The Autodesk ID of the user that updated the step.
startedAt
datetime: ISO 8601
The date and time when the step transitioned to In Progress in the backend. This corresponds to the step being marked as Started in the UI, formatted as YYYY-MM-DDTHH:mm:ss.SSSSSSZ (ISO 8601) in UTC. For example, 2025-01-20T12:00:00.198466Z.
completedAt
datetime: ISO 8601
The date and time when the step was completed, formatted as YYYY-MM-DDTHH:mm:ss.SSSSSSZ (ISO 8601) in UTC. For example, 2025-01-20T12:00:00.198466Z.
permittedActions
array: object
A list of actions that the user is allowed to perform on the step.
Example
Submittal item step successfully retrieved.

Request
curl -v 'https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/items/767b5888-2c6a-413d-8487-613966dd64ce/steps/b79059cc-611b-4769-80b7-f8db9a2dfcdf' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "id": "84eb33cd-4a42-42b7-95dd-3900035c3407",
  "itemId": "2df3b4cf-16f4-496e-8173-7125f31e3dd1",
  "status": "in-progress",
  "stepNumber": 1,
  "daysToRespond": 10,
  "dueDate": "2024-02-15",
  "tasks": [
    {
      "id": "4d539b8f-c522-4f1c-9743-d7fdfa9e9c9e",
      "stepId": "d6635799-e973-4c9c-80d8-fb4b3591ef6b",
      "status": "completed",
      "assignedTo": "WD43ZJGKDFLFH",
      "assignedToType": "1",
      "isRequired": true,
      "stepDueDate": "2024-02-15",
      "responseId": "2d46d30b-7dc1-4a65-991d-d739a1381eb8",
      "responseComment": "Approved without changes.",
      "respondedAt": "2024-02-03T12:09:24.198466Z",
      "respondedBy": "WD43ZJGKDFLFH",
      "createdAt": "2024-03-21T23:04:49.406Z",
      "createdBy": "WD43ZJGKDFLFH",
      "updatedAt": "2024-03-24T23:04:49.406674Z",
      "updatedBy": "WD43ZJGKDFLFH",
      "startedAt": "2024-03-21T23:15:49.406894Z",
      "completedAt": "2024-03-24T23:04:49.4066344Z",
      "completedBy": "WD43ZJGKDFLFH",
      "permittedActions": [
        {
          "id": "Task::partial_update",
          "fields": {
            "responseComment": [],
            "responseId": []
          },
          "mandatoryFields": [
            "responseId"
          ],
          "transitions": [
            ""
          ]
        }
      ]
    }
  ],
  "createdAt": "2024-03-21T23:04:49.406Z",
  "createdBy": "WD43ZJGKDFLFH",
  "updatedAt": "2024-03-24T23:04:49.406Z",
  "updatedBy": "WD43ZJGKDFLFH",
  "startedAt": "2024-03-21T23:15:49.406Z",
  "completedAt": "2024-03-24T23:04:49.406Z",
  "permittedActions": [
    {
      "id": "Step::overwrite_step",
      "fields": {
        "tasks": []
      },
      "mandatoryFields": [
        "tasks"
      ],
      "transitions": [
        ""
      ]
    }
  ]
}


Documentation /Autodesk Construction Cloud APIs /API Reference
Submittals Profile
GET	users/me
Retrieves the Autodesk ID, assigned roles, and permitted actions for the current user within a specified project.

This endpoint serves two main purposes:

To retrieve the Autodesk ID and roles of the current user in Submittals.
To obtain the list of actions the user is permitted to perform in the system, such as Item::create and Spec::create.
For more information on roles and permissions in Submittals, refer to the Help documentation.

For detailed steps on creating submittal items, refer to the Create Submittal Item tutorial.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/submittals/v2/projects/:projectId/users/me
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
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Response
HTTP Status Code Summary
200
OK
Returns user details.
401
Unauthorized
Invalid or missing authorization header. Verify the Bearer token and try again.
403
Forbidden
The user is not authorized to perform this action.
404
Not Found
The specified resource was not found.
500
Internal Server Error
An unexpected error occurred on the server while processing the request.
Response
Body Structure (200)
 Expand all
id
string
The AutodeskId for the current user.
roles
array: string
The roles assigned to the user in Submittals. Possible values: 1 - Manager, 2 - User, 4 - Admin
permittedActions
array: object
A list of actions that the user is allowed to perform
Example
Returns user details.

Request
curl -v 'https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/users/me' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "id": "GJDGNLSX7B8T",
  "roles": [
    "1",
    "2",
    "4"
  ],
  "permittedActions": [
    {
      "id": "Item::create",
      "fields": {},
      "mandatoryFields": [
        ""
      ],
      "transitions": [
        {
          "id": "create::mgr-1",
          "name": "Create",
          "stateFrom": {
            "id": "create",
            "name": "Create"
          },
          "stateTo": {
            "id": "mgr-1",
            "name": "MGR 1"
          },
          "transitionFields": [
            "manager",
            "managerType",
            "stateId",
            "title",
            "description",
            "priority"
          ],
          "mandatoryFields": [
            [
              "manager",
              "managerType",
              "stateId",
              "title"
            ]
          ],
          "actionId": "ITEM_TRANSITION_CREATE_MGR1"
        }
      ]
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Tasks
GET	projects/{projectId}/items/{itemId}/steps/{stepId}/tasks
Retrieves a list of tasks associated with a specific review step of a submittal item in a project.

Tasks represent individual actions assigned to reviewers within a review step of the submittal review process. Each task must be completed to advance to the next review step. A review step must have at least one task (reviewer) to initiate the review process.

Currently, the public API does not support creating new steps, but tasks and their statuses can be queried for each step.

To learn more about using this endpoint within the submittal workflow, see the Process Submittal Items tutorial.

For more information about submittals and their lifecycle, see the Process Submittal Help documentation.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/submittals/v2/projects/:projectId/items/:itemId/steps/:stepId/tasks
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
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

itemId
string
The ID of the submittal item. To find the item ID, call GET items.
stepId
string
The ID of the review step associated with the submittal item. To find the step ID, call GET steps.
Request
Query String Parameters
limit
int
The maximum number of results per page. Possible values: 1- 50. Default value: 20. For example, to limit the response to two results per page, use limit=2.
offset
int
The number of results to skip before starting to return data. For example, to skip the first 20 results, include offset=20 in the query string. For more details, see the JSON API Paging Help documentation.
Response
HTTP Status Code Summary
200
OK
List of tasks successfully retrieved.
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers.
401
Unauthorized
Invalid or missing authorization header. Verify the Bearer token and try again.
403
Forbidden
The user is not authorized to perform this action.
404
Not Found
The specified resource was not found.
500
Internal Server Error
An unexpected error occurred on the server while processing the request.
Response
Body Structure (200)
 Expand all
pagination
object
Describes pagination details for the response, including information about the current page and navigation to other pages.
results
array: object
Tasks associated with the specified review step.
Example
List of tasks successfully retrieved.

Request
curl -v 'https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/items/767b5888-2c6a-413d-8487-613966dd64ce/steps/b79059cc-611b-4769-80b7-f8db9a2dfcdf/tasks' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 10,
    "offset": 100,
    "totalResults": 25,
    "previousUrl": "https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/items/767b5888-2c6a-413d-8487-613966dd64ce/steps/b79059cc-611b-4769-80b7-f8db9a2dfcdf/tasks?limit=5&offset=10",
    "nextUrl": null
  },
  "results": [
    {
      "id": "4d539b8f-c522-4f1c-9743-d7fdfa9e9c9e",
      "stepId": "d6635799-e973-4c9c-80d8-fb4b3591ef6b",
      "status": "completed",
      "assignedTo": "WD43ZJGKDFLFH",
      "assignedToType": "1",
      "isRequired": true,
      "stepDueDate": "2024-02-15",
      "responseId": "2d46d30b-7dc1-4a65-991d-d739a1381eb8",
      "responseComment": "Approved without changes.",
      "respondedAt": "2024-02-03T12:09:24.198466Z",
      "respondedBy": "WD43ZJGKDFLFH",
      "createdAt": "2024-03-21T23:04:49.406Z",
      "createdBy": "WD43ZJGKDFLFH",
      "updatedAt": "2024-03-24T23:04:49.406674Z",
      "updatedBy": "WD43ZJGKDFLFH",
      "startedAt": "2024-03-21T23:15:49.406894Z",
      "completedAt": "2024-03-24T23:04:49.4066344Z",
      "completedBy": "WD43ZJGKDFLFH",
      "permittedActions": [
        {
          "id": "Task::partial_update",
          "fields": {
            "responseComment": [],
            "responseId": []
          },
          "mandatoryFields": [
            "responseId"
          ],
          "transitions": [
            ""
          ]
        }
      ]
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Tasks
GET	projects/{projectId}/items/{itemId}/steps/{stepId}/tasks/{taskId}
Retrieves details of a specific task associated with a review step in a submittal item. A task represents the assignment of responsibility for completing a specific step in the review process. Tasks may correspond to a reviewer, such as an individual user (Member), a role, or a company.

To learn more about using this endpoint within the submittal workflow, see the Process Submittal Items tutorial.

For more information about submittals and their lifecycle, see the Process Submittal Help documentation.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/submittals/v2/projects/:projectId/items/:itemId/steps/:stepId/tasks/:taskId
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
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

itemId
string
The ID of the submittal item. To find the item ID, call GET items.
stepId
string
The ID of the review step associated with the submittal item. To find the step ID, call GET steps.
taskId
string
The ID of the task. To get the task ID, call GET tasks.
Response
HTTP Status Code Summary
200
OK
Task details successfully retrieved.
400
Bad Request
The request could not be understood by the server due to malformed syntax or missing request headers.
401
Unauthorized
Invalid or missing authorization header. Verify the Bearer token and try again.
403
Forbidden
The user is not authorized to perform this action.
404
Not Found
The specified resource was not found.
500
Internal Server Error
An unexpected error occurred on the server while processing the request.
Response
Body Structure (200)
 Expand all
id
string: UUID
The internal, globally unique identifier (UUID) for the task.
stepId
string: UUID
The ID of the review step associated with the task.
status
enum:string
The current status of the task. Possible values: not-started, in-progress, completed.
assignedTo
string
The Autodesk ID or member group ID of the user, company, or role assigned to the task.
assignedToType
enum:string
Specifies whether the task is assigned to a user, company, or role. Possible values: 1 (user), 2 (company), 3 (role).
isRequired
boolean
true: the task is required to complete the step.
false: (default) the task is not required to complete the step.

stepDueDate
string
The due date of the related step, formatted as YYYY-MM-DD (ISO 8601) in UTC. For example, 2025-01-20.
responseId
string: UUID
The ID of the response associated with the task, linking to the specific feedback or action taken.
responseComment
string
The content of the response comment, providing feedback or instructions related to the task.
respondedAt
datetime: ISO 8601
The date and time when the response was added, formatted as YYYY-MM-DDTHH:mm:ss.SSSSSSZ (ISO 8601) in UTC. For example, 2025-01-20T12:00:00.198466Z.
respondedBy
string
The Autodesk ID of the user who provided the response to the task.
createdAt
datetime: ISO 8601
The date and time when the task was originally created, formatted as YYYY-MM-DDTHH:mm:ss.SSSSSSZ (ISO 8601) in UTC. For example, 2025-01-20T12:00:00.198466Z.
createdBy
string
The Autodesk ID of the user who created the task.
updatedAt
datetime: ISO 8601
The date and time when the task was last updated, formatted as YYYY-MM-DDTHH:mm:ss.SSSSSSZ (ISO 8601) in UTC. For example, 2025-01-20T12:00:00.198466Z.
updatedBy
string
The Autodesk ID of the user who last updated the task.
startedAt
datetime: ISO 8601
The date and time when the related step was marked as started (In Progress), formatted as YYYY-MM-DDTHH:mm:ss.SSSSSSZ (ISO 8601) in UTC. For example, 2025-01-20T12:00:00.198466Z.
completedAt
datetime: ISO 8601
The date and time when the task was completed, formatted as YYYY-MM-DDTHH:mm:ss.SSSSSSZ (ISO 8601) in UTC. For example, 2025-01-20T12:00:00.198466Z.
completedBy
string
The Autodesk ID of the user who completed the task.
permittedActions
array: object
A list of actions that the user is allowed to perform on the task within the submittal workflow.
Example
Task details successfully retrieved.

Request
curl -v 'https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/items/767b5888-2c6a-413d-8487-613966dd64ce/steps/b79059cc-611b-4769-80b7-f8db9a2dfcdf/tasks/f2bc8b34-7e95-4317-b298-0ed80c3eba6d' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "id": "4d539b8f-c522-4f1c-9743-d7fdfa9e9c9e",
  "stepId": "d6635799-e973-4c9c-80d8-fb4b3591ef6b",
  "status": "completed",
  "assignedTo": "WD43ZJGKDFLFH",
  "assignedToType": "1",
  "isRequired": true,
  "stepDueDate": "2024-02-15",
  "responseId": "2d46d30b-7dc1-4a65-991d-d739a1381eb8",
  "responseComment": "Approved without changes.",
  "respondedAt": "2024-02-03T12:09:24.198466Z",
  "respondedBy": "WD43ZJGKDFLFH",
  "createdAt": "2024-03-21T23:04:49.406Z",
  "createdBy": "WD43ZJGKDFLFH",
  "updatedAt": "2024-03-24T23:04:49.406674Z",
  "updatedBy": "WD43ZJGKDFLFH",
  "startedAt": "2024-03-21T23:15:49.406894Z",
  "completedAt": "2024-03-24T23:04:49.4066344Z",
  "completedBy": "WD43ZJGKDFLFH",
  "permittedActions": [
    {
      "id": "Task::partial_update",
      "fields": {
        "responseComment": [],
        "responseId": []
      },
      "mandatoryFields": [
        "responseId"
      ],
      "transitions": [
        ""
      ]
    }
  ]
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Templates
GET	projects/{projectId}/templates
Retrieves a list of review templates available for a project. Each review template contains predefined steps and tasks that streamline the review workflow and can be applied to submittal items during their creation using POST items.

Currently, review templates must be created in the UI. For instructions on creating review templates, see the Submittal Review Templates Help documentation.

For a detailed overview of the submittal workflow, see the Manage Submittal Item Transitions tutorial.

Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/submittals/v2/projects/:projectId/templates
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
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You need to convert the project ID into a project ID for the ACC API by removing the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Request
Query String Parameters
limit
int
The maximum number of results per page. Possible values: 1- 50. Default value: 20. For example, to limit the response to two results per page, use limit=2.
offset
int
The number of results to skip before starting to return data. For example, to skip the first 20 results, include offset=20 in the query string. For more details, see the JSON API Paging Help documentation.
sort
string
A comma-delimited list of fields to sort by in the format field asc or field desc.
Possible values: id, name, createdAt, createdBy, updatedAt, updatedBy.

For example: sort=id asc.

Response
HTTP Status Code Summary
200
OK
A successful request returning review templates with steps and tasks.
401
Unauthorized
Invalid or missing authorization header. Verify the Bearer token and try again.
403
Forbidden
The user is not authorized to perform this action.
404
Not Found
The specified resource was not found.
500
Internal Server Error
An unexpected error occurred on the server while processing the request.
Response
Body Structure (200)
 Expand all
pagination
object
Describes pagination details for the response, including information about the current page and navigation to other pages.
results
array: object
The list of templates retrieved in the API response. Each template includes its steps and associated tasks.
Example
A successful request returning review templates with steps and tasks.

Request
curl -v 'https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/templates' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 10,
    "offset": 100,
    "totalResults": 25,
    "previousUrl": "https://developer.api.autodesk.com/construction/submittals/v2/projects/9eae7d59-1469-4389-bfb2-4114e2ba5545/templates?limit=5&offset=10",
    "nextUrl": null
  },
  "results": [
    {
      "id": "56abeb4a-c450-4c34-a23d-a49e5e47ef2a",
      "name": "Structural Review Template",
      "steps": [
        {
          "id": "54e9ca56-54b8-4492-b140-d6c0454d70fe",
          "stepNumber": 1,
          "daysToRespond": 10,
          "tasks": [
            {
              "id": "63d901e6-e148-4b29-8330-92dfe91e8d07",
              "assignedTo": "WD43ZJGKDFLFH",
              "assignedToType": "1",
              "isRequired": true
            }
          ]
        }
      ],
      "createdAt": "2018-02-21T23:04:49.406673Z",
      "createdBy": "WD43ZJGKDFLFH",
      "updatedAt": "2018-02-21T23:04:49.406Z",
      "updatedBy": "WD43ZJGKDFLFH",
      "watchers": [
        {
          "id": "224356",
          "userType": "2"
        },
        {
          "id": "3522614",
          "userType": "3"
        }
      ]
    }
  ]
}