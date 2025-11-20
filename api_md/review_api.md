ACC Reviews API Field Guide
This guide introduces the Autodesk Construction Cloud (ACC) Reviews API, which allows access to resources related to the Reviews tool in ACC projects.

For more information about how Reviews work in ACC, see the Reviews Help.

How the Reviews API Works
The Reviews API provides read and write access to Reviews and associated data in your ACC project. This includes:

Retrieving approval workflows configured for reviews
Retrieving review instances generated from those approval workflows
Retrieving the files and file versions currently under a review
Retrieving the approval workflow assigned to a specific review
Retrieving approval statuses for each file version across all reviews
Retrieving step-by-step progress of a review
Creating approval workflows with customized configurations
Creating reviews for multiple files using specific approval workflows
Terminology
These terms are specific to the Reviews API:

Approval Workflow
A defined sequence of steps and candidate reviewers/approvers used to guide the file review process.

Each workflow can include multiple Initial Review steps and a Final Review step.

Review
An instance of an Approval Workflow that has been started for specific file versions. Review candidates are assigned according to the original approval workflow.

Note that modifying the workflow does not affect existing reviews created from it.

Version
A specific version of a file uploaded to ACC. A review typically targets one or more versions of a file.

Approval Status
Represents the current state of a version in the review process. Possible values include:

IN_REVIEW
APPROVED
REJECTED
Note that a file version may be part of multiple reviews. If any associated review is still open, the status remains IN_REVIEW.

Step
A workflow consists of multiple steps. Initial Review steps involve one or more reviewers. The Final Review step is typically the approval step.

Candidate

A user assigned to a step in an approval workflow. Candidates can be:

Initiator — Starts the review.

Reviewer — Reviews files and adds comments.

Approver — Gives final approval.

Progress
The progress of a review instance shows its overall status and records the actions taken by candidates at each step of the workflow.

Candidate
A candidate is a user assigned to a step in an approval workflow. Candidates fall into three roles:

Initiator: The user who can start a review.
Reviewer: The user who reviews files and adds comments in reviewer steps.
Approver: The user who gives final approval in the approver step.
Limitations
The Reviews API does not support:

Editing approval workflows or existing review instances
Updating or deleting file versions that are under review
Adding or removing reviewers or approvers from a review instance
Modifying custom attributes associated with a review instance
Retrieving activity logs of a review instance
Exporting review reports
Proactively sending notifications to reviewers or approvers of a review instance
Processing or completing a review (for example, Starting a review, Completing steps, or Submitting decisions)

GET	projects/{projectId}/workflows
Retrieves all approval workflows used for file reviews in a given project.

Each workflow defines the steps, reviewers, durations, approval statuses, and post-review actions used when creating new reviews.

For more details about approval workflows, see the Help documentation.

The Authorization header token can be obtained through either the three-legged OAuth flow or the two-legged OAuth flow with user impersonation, which requires the x-user-id header.

To retrieve the exact workflow that was applied to a specific review, call GET reviews/:reviewId/workflow.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/reviews/v1/projects/{projectId}/workflows
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
The ID of a user on whose behalf the request is made. Your application has access to all users specified by the administrator in the SaaS Integrations UI. Use this header to specify which user should be affected by the request.
This header is only required when using two-legged authentication. It is not needed for three-legged authentication.

Only user’s Autodesk ID (autodeskId) can be accepted.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can provide the project ID with or without the “b." prefix.

Example with prefix: b.563a4c30-e30d-4869-ac02-2a18b6447abe
Example without prefix: 563a4c30-e30d-4869-ac02-2a18b6447abe
Request
Query String Parameters
limit
int
The maximum number of approval workflows to return in a single request. Possible values: 1-50. Maximum: 50. Default: 50. For example: limit=2.
offset
int
The index at which the endpoint starts returning results. Used for pagination. Default: 0. For example: offset=10.
sort
string
Specifies a single field to sort the results by. The default order is ascending (asc); to sort in descending order, add desc. Possible sorting fields: name, status, updatedAt. For example: sort=name desc.
filter[initiator]
boolean
Filters the results based on who initiated the workflow. For example: filter[initiator]=true.
true: return only workflows initiated by the current user. This filter is ignored if the user is a project admin.

false: (default) return workflows regardless of who initiated them.

Note that this filter cannot be used together with filter[status].

filter[status]
enum:string
Filters the results by workflow status. For example: filter[status]=INACTIVE. Possible values:
ACTIVE: return only active workflows.

INACTIVE: return only inactive (disabled) workflows.

Default: ACTIVE.

Note that this filter cannot be used together with filter[initiator].

Response
HTTP Status Code Summary
200
OK
Successfully retrieved the list of approval workflows
400
Bad Request
Bad request. The input parameters were invalid.
403
Forbidden
Forbidden. The user does not have permission to access this resource.
404
Not Found
Not found. The resource does not exist or is inaccessible.
500
Internal Server Error
An unexpected server error occurred.
Response
Body Structure (200)
 Expand all
results
array: object
A list of approval workflows in the project.
pagination
object
Metadata about the paginated results.
Example
Successfully retrieved the list of approval workflows

Request
curl -v 'https://developer.api.autodesk.com/construction/reviews/v1/projects/563a4c30-e30d-4869-ac02-2a18b6447abe/workflows?limit=2&offset=10&sort=sort=name desc&filter[initiator]=true&filter[status]=ACTIVE' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "results": [
    {
      "name": "Final Structural Review",
      "description": "Used to review structural plans before finalizing IFC drawings.",
      "notes": "Please check all rebar annotations before approving. Include markup if changes are required.",
      "additionalOptions": {
        "allowInitiatorToEdit": true
      },
      "id": "4e609369-e950-4097-b7d3-e6cf1c3c5415",
      "status": "ACTIVE",
      "approvalStatusOptions": [
        {
          "label": "Approved w/ comments",
          "value": "APPROVED",
          "id": "b2a3c3b7-4fef-40a4-868b-981b23e7182f",
          "builtIn": false
        }
      ],
      "steps": [
        {
          "name": "Reviewer",
          "type": "REVIEWER",
          "duration": 3,
          "dueDateType": "CALENDAR_DAY",
          "groupReview": {
            "enabled": true,
            "type": "MINIMUM",
            "min": 3
          },
          "id": "Lane_uJtTI3vjaF",
          "candidates": {
            "roles": [
              {
                "autodeskId": "1473817",
                "name": "Architect"
              }
            ],
            "users": [
              {
                "autodeskId": "HWUBNU689CRU",
                "name": "James Smith"
              }
            ],
            "companies": [
              {
                "autodeskId": "26980302",
                "name": "Autodesk Co. Ltd."
              }
            ]
          }
        }
      ],
      "copyFilesOptions": {
        "enabled": true,
        "allowOverride": false,
        "condition": "ANY",
        "folderUrn": "urn:adsk.wipprod:fs.folder:co.CplBAmvXRWGqsvN1Nabvd2",
        "includeMarkups": false,
        "disableOverrideMarkupSetting": false
      },
      "attachedAttributes": [
        {
          "id": 1001,
          "required": false
        }
      ],
      "updateAttributesOptions": {
        "enableAttachedAttributes": false,
        "updateSourceAndCopiedFiles": false
      },
      "createdAt": "2024-07-07T09:21:17.577Z",
      "updatedAt": "2025-01-07T08:43:10.189Z"
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "totalResults": 100,
    "nextUrl": "https://developer.api.autodesk.com/construction/reviews/v1/projects/497f6eca-6276-4993-bfeb-53cbbbba6f08/workflows?limit=50&offset=50"
  }
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Get an Approval Workflow
GET	projects/{projectId}/workflows/{workflowId}
Retrieves a specific approval workflow in the project by workflow ID.

The workflow defines the steps, reviewers, durations, approval statuses and post-review actions used when creating new reviews.

For more details about approval workflows, see the Help documentation.

The Authorization header token can be obtained through either the three-legged OAuth flow or the two-legged OAuth flow with user impersonation, which requires the x-user-id header.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/reviews/v1/projects/{projectId}/workflows/{workflowId}
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
The ID of a user on whose behalf the request is made. Your application has access to all users specified by the administrator in the SaaS Integrations UI. Use this header to specify which user should be affected by the request.
This header is only required when using two-legged authentication. It is not needed for three-legged authentication.

Only user’s Autodesk ID (autodeskId) can be accepted.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can provide the project ID with or without the “b." prefix.

Example with prefix: b.563a4c30-e30d-4869-ac02-2a18b6447abe
Example without prefix: 563a4c30-e30d-4869-ac02-2a18b6447abe
workflowId
string: UUID
The ID of the approval workflow.
To find available workflow IDs, call GET Workflows.

Response
HTTP Status Code Summary
200
OK
Successfully retrieved the approval workflow.
400
Bad Request
Bad request. The input parameters were invalid.
403
Forbidden
Forbidden. The user does not have permission to access this resource.
404
Not Found
Not found. The resource does not exist or is inaccessible.
500
Internal Server Error
An unexpected server error occurred.
Response
Body Structure (200)
 Expand all
name
string
The name of the workflow. It must be unique within the project.
Max length: 255

description
string
A description of the workflow.
Max length: 4096

notes
string
A custom note associated with the workflow. Visible to all reviewers during the review process.
Max length: 4096

additionalOptions
object
Workflow-level settings that control whether the initiator can modify certain fields when starting a review.
id
string: UUID
The unique identifier of the approval workflow returned in the response. This ID can be used in subsequent API calls to reference this workflow.
status
enum:string
The current status of the approval workflow. Possible values:
ACTIVE: the workflow is active and available for use.

INACTIVE: the workflow has been deactivated and cannot be used to create new reviews.

approvalStatusOptions
array: object
A list of approval status options defined for this workflow. It includes two built-in options by default (typically APPROVED and REJECTED), and may also include custom statuses added by the user.
steps
array: object
A list of steps defined in the approval workflow. Each step defines who reviews the files, how long they have, and whether it involves multiple reviewers.
copyFilesOptions
object
(Copy approved files in the UI) The configuration for copying approved files to a target folder when the review is complete.
attachedAttributes
array: object
(Update Attributes in the UI) The list of attributes added in the Update Attributes action.
These attributes will be applied to the approved files in the target folder, or optionally also in the source folder depending on the configuration.

updateAttributesOptions
object
The configuration for applying attribute updates when a review is completed. This applies only if the workflow includes a file copy action and the Update Attributes action is enabled.
createdAt
datetime: ISO 8601
The date and time when the workflow was created.
updatedAt
datetime: ISO 8601
The date and time when the workflow was last updated.
Example
Successfully retrieved the approval workflow.

Request
curl -v 'https://developer.api.autodesk.com/construction/reviews/v1/projects/563a4c30-e30d-4869-ac02-2a18b6447abe/workflows/2483599f-b62a-42fb-aa5e-888468fb63eb' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "name": "Final Structural Review",
  "description": "Used to review structural plans before finalizing IFC drawings.",
  "notes": "Please check all rebar annotations before approving. Include markup if changes are required.",
  "additionalOptions": {
    "allowInitiatorToEdit": true
  },
  "id": "4e609369-e950-4097-b7d3-e6cf1c3c5415",
  "status": "ACTIVE",
  "approvalStatusOptions": [
    {
      "label": "Approved w/ comments",
      "value": "APPROVED",
      "id": "b2a3c3b7-4fef-40a4-868b-981b23e7182f",
      "builtIn": false
    }
  ],
  "steps": [
    {
      "name": "Reviewer",
      "type": "REVIEWER",
      "duration": 3,
      "dueDateType": "CALENDAR_DAY",
      "groupReview": {
        "enabled": true,
        "type": "MINIMUM",
        "min": 3
      },
      "id": "Lane_uJtTI3vjaF",
      "candidates": {
        "roles": [
          {
            "autodeskId": "1473817",
            "name": "Architect"
          }
        ],
        "users": [
          {
            "autodeskId": "HWUBNU689CRU",
            "name": "James Smith"
          }
        ],
        "companies": [
          {
            "autodeskId": "26980302",
            "name": "Autodesk Co. Ltd."
          }
        ]
      }
    }
  ],
  "copyFilesOptions": {
    "enabled": true,
    "allowOverride": false,
    "condition": "ANY",
    "folderUrn": "urn:adsk.wipprod:fs.folder:co.CplBAmvXRWGqsvN1Nabvd2",
    "includeMarkups": false,
    "disableOverrideMarkupSetting": false
  },
  "attachedAttributes": [
    {
      "id": 1001,
      "required": false
    }
  ],
  "updateAttributesOptions": {
    "enableAttachedAttributes": false,
    "updateSourceAndCopiedFiles": false
  },
  "createdAt": "2024-07-07T09:21:17.577Z",
  "updatedAt": "2025-01-07T08:43:10.189Z"
}


Documentation /Autodesk Construction Cloud APIs /API Reference
List Reviews
GET	projects/{projectId}/reviews
Retrieves the list of reviews created in the specified project.

It includes basic information such as review ID, name, status, initiator, and current step information.

For more details about reviews, see the Help documentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/reviews/v1/projects/{projectId}/reviews
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
The ID of a user on whose behalf the request is made. Your application has access to all users specified by the administrator in the SaaS Integrations UI. Use this header to specify which user should be affected by the request.
This header is only required when using two-legged authentication. It is not needed for three-legged authentication.

Only user’s Autodesk ID (autodeskId) can be accepted.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can provide the project ID with or without the “b." prefix.

Example with prefix: b.563a4c30-e30d-4869-ac02-2a18b6447abe
Example without prefix: 563a4c30-e30d-4869-ac02-2a18b6447abe
Request
Query String Parameters
limit
int
The maximum number of reviews to retrieve.
Possible values: 1-50. Maximum: 50. Default: 50. For example: limit=2.

offset
int
The index of the first result to return (zero-based).
Default: 0. For example: offset=10.

sort
string
Sorts the results by a single field.
Use the format fieldName (ascending) or fieldName desc (descending).

If no direction is specified, sorting defaults to ascending.

Possible values: name, status, sequenceId, currentStepDueDate, createdAt, finishedAt.

For example: sort=createdAt desc.

filter[workflowId]
string: UUID
Filter by a specific approval workflow ID in URL-encoded format.
For example: filter[workflowId]=497f6eca-6276-4993-bfeb-53cbbbba6f08.

filter[status]
string
Filter by the review status in URL-encoded format.
Possible values: OPEN, CLOSED, VOID, FAILED.

For example: filter[status]=OPEN.

Reviews with status FAILED are only visible to project administrators.

filter[currentStepDueDate]
string
Filter by the due date of the current review step in URL-encoded format.
Provide a date range using the format startDate..endDate.

Both values must be in ISO 8601 format.

For example: filter[updatedAt]=2023-06-01..2023-06-30.

filter[createdAt]
string
Filter by review creation date in URL-encoded format.
Provide a date range using the format startDate..endDate.

Both values must be in ISO 8601 format.

For example: filter[createdAt]=2023-06-01..2023-06-30

filter[updatedAt]
string
Filter by the review’s last updated date in URL-encoded format.
Provide a date range using the format startDate..endDate.

Both values must be in ISO 8601 format.

For example: filter[updatedAt]=2023-06-01..2023-06-30.

filter[finishedAt]
string
Filter by the date the review was finished, in URL-encoded format.
Provide a date range using the format startDate..endDate.

Both values must be in ISO 8601 format.

For example: filter[finishedAt]=2023-06-01..2023-06-30.

filter[nextActionByUser]
string
Filter by Autodesk ID of a user responsible for the next action, in URL-encoded format.
This includes reviews assigned directly to the user or to their role or company.

For example: filter[nextActionByUser]=A96JX8NUKRLVFWSR.

filter[nextActionByRole]
string
Filter by Autodesk ID of a role responsible for the next action, in URL-encoded format.
For example: filter[nextActionByRole]=1572818.

filter[nextActionByCompany]
string
Filter by Autodesk ID of a company responsible for the next action, in URL-encoded format.
For example: filter[nextActionByCompany]=81768771.

filter[name]
string
Filter by review name in URL-encoded format.
Retrieves reviews with names that contain the specified string (not case-sensitive).

For example: filter[name]=Apartment retrieves reviews like Apartment Block A and apartment_rendering.

filter[sequenceId]
int
Filter by review sequence ID in URL-encoded format.
Retrieves reviews with sequence IDs that partially match the specified number.

For example: filter[sequenceId]=11 may retrieve 113 and 211.

filter[archived]
boolean
Filter by archive status in URL-encoded format.
true: retrieves only archived reviews.

false: retrieves only active (non-archived) reviews.

If omitted, only active reviews are retrieved.

For example: filter[archived]=false.

filter[archivedBy]
string
Filter by the Autodesk ID of the user who archived the review, in URL-encoded format. To find the ID, call GET users.
It only takes effect when filter[archived]=true is also set.

For example: filter[archivedBy]=A96JX8NUKRLVFWSR.

filter[archivedAt]
string
Filter by the date the review was archived, in URL-encoded format.
It only applies if filter[archived]=true.

Provide a date range using the format startDate..endDate.

Both values must be in ISO 8601 format.

For example: filter[archivedAt]=2023-06-01..2023-06-30.

Response
HTTP Status Code Summary
200
OK
Successfully retrieved the list of reviews
400
Bad Request
Bad request. The input parameters were invalid.
403
Forbidden
Forbidden. The user does not have permission to access this resource.
404
Not Found
Not found. The resource does not exist or is inaccessible.
500
Internal Server Error
An unexpected server error occurred.
Response
Body Structure (200)
 Expand all
results
array: object
A list of reviews matching the request parameters
pagination
object
Metadata about the paginated results.
Example
Successfully retrieved the list of reviews

Request
curl -v 'https://developer.api.autodesk.com/construction/reviews/v1/projects/563a4c30-e30d-4869-ac02-2a18b6447abe/reviews?limit=2&offset=10&sort=createdAt desc&filter[workflowId]=497f6eca-6276-4993-bfeb-53cbbbba6f08&filter[status]=OPEN&filter[currentStepDueDate]=2023-06-01..2023-06-30&filter[createdAt]=2023-06-01..2023-06-30&filter[updatedAt]=2023-06-01..2023-06-30&filter[finishedAt]=2023-06-01..2023-06-30&filter[nextActionByUser]=A96JX8NUKRLVFWSR&filter[nextActionByRole]=1572818&filter[nextActionByCompany]=81768771&filter[name]=Apartment&filter[sequenceId]=11&filter[archivedBy]=A96JX8NUKRLVFWSR&filter[archivedAt]=2023-06-01..2023-06-30' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'

  {
  "results": [
    {
      "id": "37d5145b-c634-407c-b0b4-a65197e43fce",
      "sequenceId": 23,
      "name": "3rd Floor Design Review",
      "status": "OPEN",
      "currentStepId": "Lane_uJtTI3vjaF",
      "currentStepDueDate": "2024-11-09T01:42:16.600Z",
      "createdBy": {
        "autodeskId": "HWUBNU689CRU",
        "name": "James Smith"
      },
      "createdAt": "2024-11-06T01:42:17.476Z",
      "updatedAt": "2024-11-07T12:33:36.421Z",
      "finishedAt": "2024-11-10T02:33:17.336Z",
      "archived": false,
      "archivedBy": {
        "autodeskId": "TTFMLCMCRG5F",
        "name": "Tim Hudson"
      },
      "archivedAt": "2024-11-19T01:38:27.306Z",
      "workflowId": "0b43cedf-5c02-462b-8166-7dfbb13d3476",
      "nextActionBy": {
        "claimedBy": [
          {
            "autodeskId": "HWUBNU689CRU",
            "name": "James Smith"
          }
        ],
        "candidates": {
          "roles": [
            {
              "autodeskId": "1473817",
              "name": "Architect"
            }
          ],
          "users": [
            {
              "autodeskId": "HWUBNU689CRU",
              "name": "James Smith"
            }
          ],
          "companies": [
            {
              "autodeskId": "26980302",
              "name": "Autodesk Co. Ltd."
            }
          ]
        }
      }
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "totalResults": 100,
    "nextUrl": "https://developer.api.autodesk.com/construction/reviews/v1/projects/497f6eca-6276-4993-bfeb-53cbbbba6f08/reviews?limit=50&offset=50"
  }
}


Documentation /Autodesk Construction Cloud APIs /API Reference
Get a Review
GET	projects/{projectId}/reviews/{reviewId}
Retrieves a specific review in the specified project by review ID.

It includes basic information such as review ID, name, status, initiator, and current step information.

For more details about reviews, see the Help documentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/reviews/v1/projects/{projectId}/reviews/{reviewId}
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
The ID of a user on whose behalf the request is made. Your application has access to all users specified by the administrator in the SaaS Integrations UI. Use this header to specify which user should be affected by the request.
This header is only required when using two-legged authentication. It is not needed for three-legged authentication.

Only user’s Autodesk ID (autodeskId) can be accepted.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can provide the project ID with or without the “b." prefix.

Example with prefix: b.563a4c30-e30d-4869-ac02-2a18b6447abe
Example without prefix: 563a4c30-e30d-4869-ac02-2a18b6447abe
reviewId
string: UUID
The unique ID of the review. It must be in UUID format — not the numeric sequence ID shown in the Reviews UI. To find the review ID, call GET reviews.
Response
HTTP Status Code Summary
200
OK
Successfully retrieved the review.
400
Bad Request
Bad request. The input parameters were invalid.
403
Forbidden
Forbidden. The user does not have permission to access this resource.
404
Not Found
Not found. The resource does not exist or is inaccessible.
500
Internal Server Error
An unexpected server error occurred.
Response
Body Structure (200)
 Expand all
id
string: UUID
The unique identifier of the review.
sequenceId
int
A unique, auto-incrementing number assigned to the review when it is first submitted.
This ID does not change, even if the review is sent back to the initiator and goes through multiple rounds. It identifies the review within the project and reflects the order in which reviews were created.

name
string
The name of the review.
status
enum:string
The current status of the review.
Possible values: OPEN, CLOSED, VOID, FAILED.

currentStepId
string
The ID of the current step in the review.
currentStepDueDate
datetime: ISO 8601
The due date of the current step.
createdBy
object
Information about the user who initiated the review.
createdAt
datetime: ISO 8601
The date time when the review was initiated.
updatedAt
datetime: ISO 8601
The date time when the review was last updated.
finishedAt
datetime: ISO 8601
The date time when the review was completed.
archived
boolean
Indicates whether the review has been archived.
true: the review is archived.

false: (default) the review is active.

archivedBy
object
Information about the user who archived the review.
archivedAt
datetime: ISO 8601
The date and time when the review was archived. If the review has not been archived, this value is null.
workflowId
string: UUID
The unique identifier (UUID) of the approval workflow used to create this review.
nextActionBy
object
Information about the claimers and candidates responsible for the current step.
Example
Successfully retrieved the review.

Request
curl -v 'https://developer.api.autodesk.com/construction/reviews/v1/projects/563a4c30-e30d-4869-ac02-2a18b6447abe/reviews/73c8b3ec-eea2-4240-9c69-f9563e2fec0c' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'

  {
  "id": "37d5145b-c634-407c-b0b4-a65197e43fce",
  "sequenceId": 23,
  "name": "3rd Floor Design Review",
  "status": "OPEN",
  "currentStepId": "Lane_uJtTI3vjaF",
  "currentStepDueDate": "2024-11-09T01:42:16.600Z",
  "createdBy": {
    "autodeskId": "HWUBNU689CRU",
    "name": "James Smith"
  },
  "createdAt": "2024-11-06T01:42:17.476Z",
  "updatedAt": "2024-11-07T12:33:36.421Z",
  "finishedAt": "2024-11-10T02:33:17.336Z",
  "archived": false,
  "archivedBy": {
    "autodeskId": "TTFMLCMCRG5F",
    "name": "Tim Hudson"
  },
  "archivedAt": "2024-11-19T01:38:27.306Z",
  "workflowId": "0b43cedf-5c02-462b-8166-7dfbb13d3476",
  "nextActionBy": {
    "claimedBy": [
      {
        "autodeskId": "HWUBNU689CRU",
        "name": "James Smith"
      }
    ],
    "candidates": {
      "roles": [
        {
          "autodeskId": "1473817",
          "name": "Architect"
        }
      ],
      "users": [
        {
          "autodeskId": "HWUBNU689CRU",
          "name": "James Smith"
        }
      ],
      "companies": [
        {
          "autodeskId": "26980302",
          "name": "Autodesk Co. Ltd."
        }
      ]
    }
  }
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Get the Workflow For This Review
GET	projects/{projectId}/reviews/{reviewId}/workflow
Retrieves the approval workflow associated with a specific review.

This endpoint provides the exact workflow structure used when the review was created, including its steps, candidates, approval status options, and post-review actions.

To retrieve all workflows defined in a project (not just for one review), call GET workflows.

For more details about reviews, see the Help documentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/reviews/v1/projects/{projectId}/reviews/{reviewId}/workflow
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
* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can provide the project ID with or without the “b." prefix.

Example with prefix: b.563a4c30-e30d-4869-ac02-2a18b6447abe
Example without prefix: 563a4c30-e30d-4869-ac02-2a18b6447abe
reviewId
string: UUID
The unique ID of the review. It must be in UUID format — not the numeric sequence ID shown in the Reviews UI. To find the review ID, call GET reviews.
Response
HTTP Status Code Summary
200
OK
Successfully retrieved the requested review workflow data
400
Bad Request
Bad request. The input parameters were invalid.
403
Forbidden
Forbidden. The user does not have permission to access this resource.
404
Not Found
Not found. The resource does not exist or is inaccessible.
500
Internal Server Error
An unexpected server error occurred.
Response
Body Structure (200)
 Expand all
name
string
The name of the workflow. It must be unique within the project.
Max length: 255

description
string
A description of the workflow.
Max length: 4096

notes
string
A custom note associated with the workflow. Visible to all reviewers during the review process.
Max length: 4096

additionalOptions
object
Workflow-level settings that control whether the initiator can modify certain fields when starting a review.
id
string: UUID
The ID of the workflow.
approvalStatusOptions
array: object
A list of file review status options to the workflow, which contains two built in options returned by the system.
steps
array: object
A list of steps specify the details for each step in the workflow.
copyFilesOptions
object
(Copy approved files in the UI) The configuration for copying approved files to a target folder when the review is complete.
attachedAttributes
array: object
(Update Attributes in the UI) The list of attributes added in the Update Attributes action.
These attributes will be applied to the approved files in the target folder, or optionally also in the source folder depending on the configuration.

updateAttributesOptions
object
The configuration for applying attribute updates when a review is completed. This applies only if the workflow includes a file copy action and the Update Attributes action is enabled.
Example
Successfully retrieved the requested review workflow data

Request
curl -v 'https://developer.api.autodesk.com/construction/reviews/v1/projects/563a4c30-e30d-4869-ac02-2a18b6447abe/reviews/73c8b3ec-eea2-4240-9c69-f9563e2fec0c/workflow' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
{
  "name": "Final Structural Review",
  "description": "Used to review structural plans before finalizing IFC drawings.",
  "notes": "Please check all rebar annotations before approving. Include markup if changes are required.",
  "additionalOptions": {
    "allowInitiatorToEdit": true
  },
  "id": "dab28823-7ecc-47b4-a92a-37540d777751",
  "approvalStatusOptions": [
    {
      "label": "Approved w/ comments",
      "value": "APPROVED",
      "id": "b2a3c3b7-4fef-40a4-868b-981b23e7182f",
      "builtIn": false
    }
  ],
  "steps": [
    {
      "name": "Reviewer",
      "type": "REVIEWER",
      "duration": 3,
      "dueDateType": "CALENDAR_DAY",
      "groupReview": {
        "enabled": true,
        "type": "MINIMUM",
        "min": 3
      },
      "id": "Lane_uJtTI3vjaF",
      "candidates": {
        "roles": [
          {
            "autodeskId": "1473817",
            "name": "Architect"
          }
        ],
        "users": [
          {
            "autodeskId": "HWUBNU689CRU",
            "name": "James Smith"
          }
        ],
        "companies": [
          {
            "autodeskId": "26980302",
            "name": "Autodesk Co. Ltd."
          }
        ]
      }
    }
  ],
  "copyFilesOptions": {
    "enabled": true,
    "allowOverride": false,
    "condition": "ANY",
    "folderUrn": "urn:adsk.wipprod:fs.folder:co.CplBAmvXRWGqsvN1Nabvd2",
    "includeMarkups": false,
    "disableOverrideMarkupSetting": false
  },
  "attachedAttributes": [
    {
      "id": 1001,
      "required": false
    }
  ],
  "updateAttributesOptions": {
    "enableAttachedAttributes": false,
    "updateSourceAndCopiedFiles": false
  }
}


Documentation /Autodesk Construction Cloud APIs /API Reference
List Review Progress
GET	projects/{projectId}/reviews/{reviewId}/progress
Retrieves the progress of a specific review in the specified project.

This endpoint tracks the current state of each step in the review’s approval workflow, showing the assigned candidates, whether steps have been claimed or submitted, and who performed each action. Results are returned in reverse chronological order (most recent action first).

Note that this endpoint only returns data for the current round of the review.

To retrieve the review’s configuration and metadata, call GET reviews/:reviewId.

For more details about reviews, see the Help documentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/reviews/v1/projects/{projectId}/reviews/{reviewId}/progress
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
The ID of a user on whose behalf the request is made. Your application has access to all users specified by the administrator in the SaaS Integrations UI. Use this header to specify which user should be affected by the request.
This header is only required when using two-legged authentication. It is not needed for three-legged authentication.

Only user’s Autodesk ID (autodeskId) can be accepted.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can provide the project ID with or without the “b." prefix.

Example with prefix: b.563a4c30-e30d-4869-ac02-2a18b6447abe
Example without prefix: 563a4c30-e30d-4869-ac02-2a18b6447abe
reviewId
string: UUID
The unique ID of the review.
This must be the UUID, not the numeric sequence ID shown in the Reviews UI.

To find the review ID, call GET reviews.

Request
Query String Parameters
limit
int
The maximum number of review-progress records to return. Valid range: 1–50. Default: 50. For example: limit=2.
offset
int
The zero-based index of the first record to return. Use with limit for pagination. Default: 0. For example: offset=10.
Response
HTTP Status Code Summary
200
OK
The review progress was retrieved successfully.
400
Bad Request
Bad request. The input parameters were invalid.
403
Forbidden
Forbidden. The user does not have permission to access this resource.
404
Not Found
Not found. The resource does not exist or is inaccessible.
500
Internal Server Error
An unexpected server error occurred.
Response
Body Structure (200)
 Expand all
results
array: object
The list of review-progress records, returned in reverse chronological order.
pagination
object
Metadata about the paginated results.
Example
The review progress was retrieved successfully.

Request
curl -v 'https://developer.api.autodesk.com/construction/reviews/v1/projects/563a4c30-e30d-4869-ac02-2a18b6447abe/reviews/73c8b3ec-eea2-4240-9c69-f9563e2fec0c/progress?limit=2&offset=10' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "results": [
    {
      "stepId": "Lane_uJtTI3vjaF",
      "stepName": "Reviewer",
      "claimedBy": {
        "autodeskId": "HWUBNU689CRU",
        "name": "James Smith"
      },
      "actionBy": {
        "autodeskId": "HWUBNU689CRU",
        "name": "James Smith"
      },
      "candidates": {
        "roles": [
          {
            "autodeskId": "1473817",
            "name": "Architect"
          }
        ],
        "users": [
          {
            "autodeskId": "HWUBNU689CRU",
            "name": "James Smith"
          }
        ],
        "companies": [
          {
            "autodeskId": "26980302",
            "name": "Autodesk Co. Ltd."
          }
        ]
      },
      "endTime": "2024-11-19T01:38:27.306Z",
      "notes": "Please check all rebar annotations before approving. Include markup if changes are required.",
      "status": "CLAIMED"
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "totalResults": 100,
    "nextUrl": "https://developer.api.autodesk.com/construction/reviews/v1/projects/497f6eca-6276-4993-bfeb-53cbbbba6f08/reviews/73c8b3ec-eea2-4240-9c69-f9563e2fec0c/progress?limit=10&offset=10"
  }
}


List Review Versions
GET	projects/{projectId}/reviews/{reviewId}/versions
Retrieves the file versions included in the latest round of the specified review.

A review may go through multiple rounds when the “Back to initiator” feature is used. This endpoint only returns data from the most recent round.

The response includes approval statuses, file version names, copied version URNs (if applicable), and any custom attributes captured during the review.

For more details about reviews, see the Help documentation.

Note that to export reviewing files using these version URNs, see Step 3 in the PDF File Export tutorial.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/reviews/v1/projects/{projectId}/reviews/{reviewId}/versions
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
The ID of a user on whose behalf the request is made. Your application has access to all users specified by the administrator in the SaaS Integrations UI. Use this header to specify which user should be affected by the request.
This header is only required when using two-legged authentication. It is not needed for three-legged authentication.

Only user’s Autodesk ID (autodeskId) can be accepted.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can provide the project ID with or without the “b." prefix.

Example with prefix: b.563a4c30-e30d-4869-ac02-2a18b6447abe
Example without prefix: 563a4c30-e30d-4869-ac02-2a18b6447abe
reviewId
string: UUID
The unique ID of the review. It must be in UUID format — not the numeric sequence ID shown in the Reviews UI. To find the review ID, call GET reviews.
Request
Query String Parameters
limit
int
The number of file versions to return in the response. Possible values: 1-50. Maximum: 50. Default: 50. For example: limit=2.
offset
int
The index of the first result to return (zero-based). Default: 0. For example: offset=10.
filter[approveStatus]
array
Filters the results based on the approval status assigned to each file during the review. It should be URL-encoded.
The filter applies to the label of the approval status, as defined in the workflow — not the internal value.

For example, if your workflow includes a status labeled Approved with comments, you would filter using that label:

filter[approveStatus]=Approved with comments.

This is especially useful when a workflow includes multiple approval options with customized labels.

Note: It supports multiple values.

For example, if you want to filter with 2 labels: both Approved and Rejected, you could filter with the query string:

filter[approveStatus]=Approved&filter[approveStatus]=Rejected

Response
HTTP Status Code Summary
200
OK
Successfully retrieved the file versions in the latest review round
400
Bad Request
Bad request. The input parameters were invalid.
403
Forbidden
Forbidden. The user does not have permission to access this resource.
404
Not Found
Not found. The resource does not exist or is inaccessible.
500
Internal Server Error
An unexpected server error occurred.
Response
Body Structure (200)
 Expand all
results
array: object
A list of file versions included in the latest round of the review.
pagination
object
Metadata about the paginated results.
Example
Successfully retrieved the file versions in the latest review round

Request
curl -v 'https://developer.api.autodesk.com/construction/reviews/v1/projects/563a4c30-e30d-4869-ac02-2a18b6447abe/reviews/73c8b3ec-eea2-4240-9c69-f9563e2fec0c/versions?limit=2&offset=10&filter[approveStatus]=Approved' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response

{
  "results": [
    {
      "urn": "urn:adsk.wipprod:fs.file:vf.Zvg8qMkjQ26MBJjIA2ZjeU?version=1",
      "itemUrn": "urn:adsk.wipprod:dm.lineage:Zvg8qMkjQ26MBJjIA2ZjeU",
      "approveStatus": {
        "id": "f44e623d-f04f-47fe-8195-efc43d1d985b",
        "label": "Approved",
        "value": "APPROVED"
      },
      "reviewContent": {
        "name": "3rd Floor 3D Models (shared).pdf",
        "customAttributes": [
          {
            "id": 1001,
            "type": "string",
            "name": "Reference Document Number",
            "value": "X-3910-3DWA"
          }
        ]
      },
      "copiedFileVersionUrn": "urn:adsk.wipprod:fs.file:vf.Zvg8qMkjQ26MBJjIA2ZjeK?version=3",
      "name": "3rd Floor 3D Models.pdf"
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "totalResults": 100,
    "nextUrl": "https://developer.api.autodesk.com/construction/reviews/v1/projects/497f6eca-6276-4993-bfeb-53cbbbba6f08/reviews/73c8b3ec-eea2-4240-9c69-f9563e2fec0c/versions?limit=10&offset=10"
  }
}


Documentation /Autodesk Construction Cloud APIs /API Reference
List Approval Statuses of a Version
GET	projects/{projectId}/versions/{versionId}/approval-statuses
Retrieves the full approval records and review references of a specific file version.

This includes all reviews the version has participated in, along with each review’s status (e.g., OPEN, CLOSED) and the file’s approval status (e.g., APPROVED, REJECTED) within that review.

The results are sorted in reverse chronological order within each group: those in the “In Review” status and those in the “Finished Review” status (Approved or Rejected), based on the review’s sequenceId.

This endpoint is typically used in the Files tool, where you can view the file’s activity across multiple reviews.

For more context, see the Help documentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
GET	https://developer.api.autodesk.com/construction/reviews/v1/projects/{projectId}/versions/{versionId}/approval-statuses
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
The ID of a user on whose behalf the request is made. Your application has access to all users specified by the administrator in the SaaS Integrations UI. Use this header to specify which user should be affected by the request.
This header is only required when using two-legged authentication. It is not needed for three-legged authentication.

Only user’s Autodesk ID (autodeskId) can be accepted.

* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can provide the project ID with or without the “b." prefix.

Example with prefix: b.563a4c30-e30d-4869-ac02-2a18b6447abe
Example without prefix: 563a4c30-e30d-4869-ac02-2a18b6447abe
versionId
string
The URL-encoded unique identifier (URN) of the file version whose review and approval history you want to retrieve.
For example, encode urn:adsk.wipprod:fs.file:vf.Ibsc4cPuQEqBHRJdBjhr6w?version=2``as ``urn%3Aadsk.wipprod%3Afs.file%3Avf.Ibsc4cPuQEqBHRJdBjhr6w%3Fversion%3D2.

To find the latest version, call GET versions and check the urn field.

Request
Query String Parameters
limit
int
The maximum number of results to return in the response. Possible values: 1–50. Maximum: 50. Default: 50. For example: limit=2.
offset
int
The number of results to skip from the beginning of the list. Used for pagination. Default: 0. For example: offset=10.
Response
HTTP Status Code Summary
200
OK
Successfully retrieved the review and approval history for the file version
400
Bad Request
Bad request. The input parameters were invalid.
403
Forbidden
Forbidden. The user does not have permission to access this resource.
404
Not Found
Not found. The resource does not exist or is inaccessible.
500
Internal Server Error
An unexpected server error occurred.
Response
Body Structure (200)
 Expand all
results
array: object
A list of approval statuses and related review information for the specified file version.
pagination
object
Metadata about the paginated results.
Example
Successfully retrieved the review and approval history for the file version

Request
curl -v 'https://developer.api.autodesk.com/construction/reviews/v1/projects/563a4c30-e30d-4869-ac02-2a18b6447abe/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.Ibsc4cPuQEqBHRJdBjhr6w%3Fversion%3D2/approval-statuses?limit=2&offset=10' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response

{
  "results": [
    {
      "approvalStatus": {
        "id": "f44e623d-f04f-47fe-8195-efc43d1d985b",
        "label": "Approved",
        "value": "APPROVED"
      },
      "review": {
        "id": "37d5145b-c634-407c-b0b4-a65197e43fce",
        "sequenceId": 23,
        "status": "OPEN"
      }
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "totalResults": 100,
    "nextUrl": "https://developer.api.autodesk.com/construction/reviews/v1/projects/497f6eca-6276-4993-bfeb-53cbbbba6f08/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.Ibsc4cPuQEqBHRJdBjhr6w%3Fversion%3D2/approval-statuses?limit=50&offset=50"
  }
}






POST

Documentation /Autodesk Construction Cloud APIs /API Reference
Create an Approval Workflow
POST	projects/{projectId}/workflows
Creates a new approval workflow in the specified project.

The workflow defines the steps, reviewers, durations, approval statuses, and post-review actions, and it can include customized configuration options. Note that updateAttributesOptions and attachedAttributes are not configurable and are automatically set to false.

For more details about approval workflows, see the Help documentation.

The Authorization header token can be obtained through either the three-legged OAuth flow or the two-legged OAuth flow with user impersonation, which requires the x-user-id header.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/construction/reviews/v1/projects/{projectId}/workflows
Authentication Context	
user context optional
Required OAuth Scopes	
data:write
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via either a two-legged or three-legged OAuth flow.
x-user-id
string
The ID of a user on whose behalf the request is made. Your application has access to all users specified by the administrator in the SaaS Integrations UI. Use this header to specify which user should be affected by the request.
This header is only required when using two-legged authentication. It is not needed for three-legged authentication.

Only user’s Autodesk ID (autodeskId) can be accepted.

Content-Type*
string
Must be application/json
* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can provide the project ID with or without the “b." prefix.

Example with prefix: b.563a4c30-e30d-4869-ac02-2a18b6447abe
Example without prefix: 563a4c30-e30d-4869-ac02-2a18b6447abe
Request
Body Structure
 Expand all
name*
string
The name of the workflow. It must be unique within the project.
Max length: 255

description
string
A description of the workflow.
Max length: 4096

notes
string
A custom note associated with the workflow. Visible to all reviewers during the review process.
Max length: 4096

additionalOptions
object
Workflow-level settings that control whether the initiator can modify certain fields when starting a review.
additionalApprovalStatusOptions
array: object
Custom approval statuses to add in addition to the built-in statuses (APPROVED, REJECTED). You can define up to 50.
copyFilesOptions*
object
(Copy approved files in the UI) The configuration for copying approved files to a target folder when the review is complete.
steps*
array: object
Defines the sequence of steps in the workflow. Steps run in the order they appear.
* Required
Response
HTTP Status Code Summary
201
Created
The workflow was created successfully.
400
Bad Request
Bad request. The input parameters were invalid.
403
Forbidden
Forbidden. The user does not have permission to access this resource.
404
Not Found
Not found. The resource does not exist or is inaccessible.
409
Conflict
Existing a same name workflow in the project
500
Internal Server Error
An unexpected server error occurred.
Response
Body Structure (201)
 Expand all
name
string
The name of the workflow. It must be unique within the project.
Max length: 255

description
string
A description of the workflow.
Max length: 4096

notes
string
A custom note associated with the workflow. Visible to all reviewers during the review process.
Max length: 4096

additionalOptions
object
Workflow-level settings that control whether the initiator can modify certain fields when starting a review.
id
string: UUID
The unique identifier of the approval workflow returned in the response. This ID can be used in subsequent API calls to reference this workflow.
status
enum:string
The current status of the approval workflow. Possible values:
ACTIVE: the workflow is active and available for use.

INACTIVE: the workflow has been deactivated and cannot be used to create new reviews.

approvalStatusOptions
array: object
A list of approval status options defined for this workflow. It includes two built-in options by default (typically APPROVED and REJECTED), and may also include custom statuses added by the user.
steps
array: object
A list of steps defined in the approval workflow. Each step defines who reviews the files, how long they have, and whether it involves multiple reviewers.
copyFilesOptions
object
(Copy approved files in the UI) The configuration for copying approved files to a target folder when the review is complete.
attachedAttributes
array: object
(Update Attributes in the UI) The list of attributes added in the Update Attributes action.
These attributes will be applied to the approved files in the target folder, or optionally also in the source folder depending on the configuration.

updateAttributesOptions
object
The configuration for applying attribute updates when a review is completed. This applies only if the workflow includes a file copy action and the Update Attributes action is enabled.
createdAt
datetime: ISO 8601
The date and time when the workflow was created.
updatedAt
datetime: ISO 8601
The date and time when the workflow was last updated.
Example
The workflow was created successfully.

Request
curl -v 'https://developer.api.autodesk.com/construction/reviews/v1/projects/563a4c30-e30d-4869-ac02-2a18b6447abe/workflows' \
  -X 'POST' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a' \
  -H 'Content-Type: application/json' \
  -d '{
        "name": "Final Structural Review",
        "description": "Used to review structural plans before finalizing IFC drawings.",
        "notes": "Please check all rebar annotations before approving. Include markup if changes are required.",
        "additionalOptions": {
          "allowInitiatorToEdit": true
        },
        "additionalApprovalStatusOptions": [
          {
            "label": "Approved w/ comments",
            "value": "APPROVED"
          }
        ],
        "copyFilesOptions": {
          "enabled": true,
          "allowOverride": false,
          "condition": "ANY",
          "folderUrn": "urn:adsk.wipprod:fs.folder:co.CplBAmvXRWGqsvN1Nabvd2",
          "includeMarkups": false,
          "disableOverrideMarkupSetting": false
        },
        "steps": [
          {
            "name": "Reviewer",
            "type": "REVIEWER",
            "duration": 3,
            "dueDateType": "CALENDAR_DAY",
            "groupReview": {
              "enabled": true,
              "type": "MINIMUM",
              "min": 3
            },
            "candidates": {
              "users": [
                {
                  "autodeskId": "HWUBNU689CRU"
                }
              ],
              "roles": [
                {
                  "autodeskId": "1473817"
                }
              ],
              "companies": [
                {
                  "autodeskId": "26980302"
                }
              ]
            }
          }
        ]
      }'
Show Less
Response
{
  "name": "Final Structural Review",
  "description": "Used to review structural plans before finalizing IFC drawings.",
  "notes": "Please check all rebar annotations before approving. Include markup if changes are required.",
  "additionalOptions": {
    "allowInitiatorToEdit": true
  },
  "id": "4e609369-e950-4097-b7d3-e6cf1c3c5415",
  "status": "ACTIVE",
  "approvalStatusOptions": [
    {
      "label": "Approved w/ comments",
      "value": "APPROVED",
      "id": "b2a3c3b7-4fef-40a4-868b-981b23e7182f",
      "builtIn": false
    }
  ],
  "steps": [
    {
      "name": "Reviewer",
      "type": "REVIEWER",
      "duration": 3,
      "dueDateType": "CALENDAR_DAY",
      "groupReview": {
        "enabled": true,
        "type": "MINIMUM",
        "min": 3
      },
      "id": "Lane_uJtTI3vjaF",
      "candidates": {
        "roles": [
          {
            "autodeskId": "1473817",
            "name": "Architect"
          }
        ],
        "users": [
          {
            "autodeskId": "HWUBNU689CRU",
            "name": "James Smith"
          }
        ],
        "companies": [
          {
            "autodeskId": "26980302",
            "name": "Autodesk Co. Ltd."
          }
        ]
      }
    }
  ],
  "copyFilesOptions": {
    "enabled": true,
    "allowOverride": false,
    "condition": "ANY",
    "folderUrn": "urn:adsk.wipprod:fs.folder:co.CplBAmvXRWGqsvN1Nabvd2",
    "includeMarkups": false,
    "disableOverrideMarkupSetting": false
  },
  "attachedAttributes": [
    {
      "id": 1001,
      "required": false
    }
  ],
  "updateAttributesOptions": {
    "enableAttachedAttributes": false,
    "updateSourceAndCopiedFiles": false
  },
  "createdAt": "2024-07-07T09:21:17.577Z",
  "updatedAt": "2025-01-07T08:43:10.189Z"
}

Documentation /Autodesk Construction Cloud APIs /API Reference
Create a Review
POST	projects/{projectId}/reviews
Creates a new review in the specified project using an existing approval workflow.

The review includes the selected files, workflow steps, reviewers, approval statuses, and related metadata.

For more details about reviews, see the Help documentation.

Note that this endpoint is not compatible with BIM 360 projects.
Resource Information
Method and URI	
POST	https://developer.api.autodesk.com/construction/reviews/v1/projects/{projectId}/reviews
Authentication Context	
user context optional
Required OAuth Scopes	
data:write
Data Format	
JSON
Request
Headers
Authorization*
string
Must be Bearer <token>, where <token> is obtained via either a two-legged or three-legged OAuth flow.
x-user-id
string
The ID of a user on whose behalf the request is made. Your application has access to all users specified by the administrator in the SaaS Integrations UI. Use this header to specify which user should be affected by the request.
This header is only required when using two-legged authentication. It is not needed for three-legged authentication.

Only user’s Autodesk ID (autodeskId) can be accepted.

Content-Type*
string
Must be application/json
* Required
Request
URI Parameters
projectId
string: UUID
The ID of the project.
Use the Data Management API to retrieve the project ID. For more information, see the Retrieve a Project ID tutorial. You can provide the project ID with or without the “b." prefix.

Example with prefix: b.563a4c30-e30d-4869-ac02-2a18b6447abe
Example without prefix: 563a4c30-e30d-4869-ac02-2a18b6447abe
Request
Body Structure
A request to create a new review in the specified project.

 Expand all
name*
string
The name of the review. Maximum length: 255 characters.
Max length: 255

fileVersions*
array: object
The file versions to include in the review. Maximum: 1000 items.
workflowId*
string: UUID
The ID of the approval workflow used to create the review.
To list available workflows, call GET workflows.

notes
string
A note about the review. In the UI, this appears as the Description field.
Maximum length: 4096 characters.

Max length: 4096

workflowOptions
object
Optional parameters that override approval workflow settings for this review (for example, steps, copy settings, or additional options).
* Required
Response
HTTP Status Code Summary
201
Created
The review was created successfully
400
Bad Request
Bad request. The input parameters were invalid.
403
Forbidden
Forbidden. The user does not have permission to access this resource.
404
Not Found
Not found. The resource does not exist or is inaccessible.
500
Internal Server Error
An unexpected server error occurred.
Response
Body Structure (201)
 Expand all
id
string: UUID
The unique identifier of the review.
sequenceId
int
A unique, auto-incrementing number assigned to the review when it is first submitted.
This ID does not change, even if the review is sent back to the initiator and goes through multiple rounds. It identifies the review within the project and reflects the order in which reviews were created.

name
string
The name of the review.
status
enum:string
The current status of the review.
Possible values: OPEN, CLOSED, VOID, FAILED.

currentStepId
string
The ID of the current step in the review.
currentStepDueDate
datetime: ISO 8601
The due date of the current step.
createdBy
object
Information about the user who initiated the review.
createdAt
datetime: ISO 8601
The date time when the review was initiated.
updatedAt
datetime: ISO 8601
The date time when the review was last updated.
finishedAt
datetime: ISO 8601
The date time when the review was completed.
archived
boolean
Indicates whether the review has been archived.
true: the review is archived.

false: (default) the review is active.

archivedBy
object
Information about the user who archived the review.
archivedAt
datetime: ISO 8601
The date and time when the review was archived. If the review has not been archived, this value is null.
workflowId
string: UUID
The unique identifier (UUID) of the approval workflow used to create this review.
nextActionBy
object
Information about the claimers and candidates responsible for the current step.
Example
The review was created successfully

Request
curl -v 'https://developer.api.autodesk.com/construction/reviews/v1/projects/563a4c30-e30d-4869-ac02-2a18b6447abe/reviews' \
  -X 'POST' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a' \
  -H 'Content-Type: application/json' \
  -d '{
        "name": "The 2nd Floor Design Review",
        "fileVersions": [
          {
            "urn": "urn:adsk.wipprod:fs.file:vf.hC6k4hndRWaeIVhIjvHu8w?version=1"
          }
        ],
        "workflowId": "43c4fa9b-0cbc-4b57-a121-9d7d46a3eaa4",
        "notes": "For the No. 3 Building on the 2nd floor, please review the design and provide feedback.",
        "workflowOptions": {
          "copyFilesOptions": {
            "folderUrn": "urn:adsk.wipprod:fs.folder:co.CplBAmvXRWGqsvN1Nabvd2"
          },
          "steps": [
            {
              "id": "Lane_068sgjq",
              "candidates": {
                "users": [
                  {
                    "autodeskId": "HWUBNU689CRU"
                  }
                ],
                "roles": [
                  {
                    "autodeskId": "1473817"
                  }
                ],
                "companies": [
                  {
                    "autodeskId": "26980302"
                  }
                ]
              }
            }
          ]
        }
      }'
Show Less
Response
{
  "id": "37d5145b-c634-407c-b0b4-a65197e43fce",
  "sequenceId": 23,
  "name": "3rd Floor Design Review",
  "status": "OPEN",
  "currentStepId": "Lane_uJtTI3vjaF",
  "currentStepDueDate": "2024-11-09T01:42:16.600Z",
  "createdBy": {
    "autodeskId": "HWUBNU689CRU",
    "name": "James Smith"
  },
  "createdAt": "2024-11-06T01:42:17.476Z",
  "updatedAt": "2024-11-07T12:33:36.421Z",
  "finishedAt": "2024-11-10T02:33:17.336Z",
  "archived": false,
  "archivedBy": {
    "autodeskId": "TTFMLCMCRG5F",
    "name": "Tim Hudson"
  },
  "archivedAt": "2024-11-19T01:38:27.306Z",
  "workflowId": "0b43cedf-5c02-462b-8166-7dfbb13d3476",
  "nextActionBy": {
    "claimedBy": [
      {
        "autodeskId": "HWUBNU689CRU",
        "name": "James Smith"
      }
    ],
    "candidates": {
      "roles": [
        {
          "autodeskId": "1473817",
          "name": "Architect"
        }
      ],
      "users": [
        {
          "autodeskId": "HWUBNU689CRU",
          "name": "James Smith"
        }
      ],
      "companies": [
        {
          "autodeskId": "26980302",
          "name": "Autodesk Co. Ltd."
        }
      ]
    }
  }
}
