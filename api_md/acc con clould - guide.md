Documentation /Autodesk Construction Cloud APIs /Developer's Guide
Autodesk Construction Cloud Platform (ACC) APIs
The unified Autodesk Construction Cloud platform (ACC) APIs allow developers to develop apps that integrate with the ACC platform to extend its capabilities in the construction ecosystem. The Autodesk Construction Cloud platform (ACC) is Autodesk’s new unified construction management software. For more information about ACC, see the Autodesk Construction Cloud website.

We currently offer the following APIs:

The Account Admin API automates creating and managing projects, assigning and managing project users, and managing member and partner company directories. You can also synchronize data with external systems.
The AutoSpecs API provides access to draft submittal logs that are extracted from construction project specification documents.
The Assets API creates and manages assets in the ACC Assets service. Use it to define the settings such as categories, custom attributes, and sets of statuses that are required to define assets, and then to create and modify assets within those settings. The API offers powerful search tools to retrieve specific sets of assets and other components, and it can modify both assets and the settings that define those assets.
The AutoSpecs API provides access to draft submittal logs that are extracted from construction project specification documents.
The Cost Management API provides access to the data stored in the ACC Cost Management module. It enables you to manage cost and budget changes to your projects, such as accessing budget, contract, and change order information. For example, you can extract budget data to export to external systems and import the data back to the ACC Cost Management module.
The Data Connector API retrieves data from ACC services such as Admin (both Project and Account), Issues, Locations, Submittals, Cost, and RFIs so the data can be used for local data analysis and other purposes. It works across multiple projects within an account, can set up data reporting on a regular schedule, and returns data in a format easily used by business intelligence tools.
The Files (Document Management) API lets you upload, access, and share 2D plans, 3D BIM models, and other project documents, as well as create packages to maximize collaboration. Note that the Files API is part of the Data Management API.
The Forms API provides access to the data stored in the ACC Forms module. The Forms tool enables your team to securely fill out, review, and manage project forms.
The Issues API creates and updates issues in your ACC projects. An issue is an item that is created in ACC for tracking, managing and communicating tasks, problems and other points of concern through to resolution. You can manage different types of issues, such as design, safety, and commissioning. We currently support issues that are associated with a project.
The Locations API enables you to configure the hierarchy (tree) of building areas (locations) in your project. A locations tree is commonly known as a location breakdown structure (LBS). With an LBS, users can identify the location associated with each of a project’s Assets, Issues, Photos, Forms, RFIs, and Submittals.
The Model Coordination API provides full access to the set of services used by the ACC Model Coordination web application. It enables users to detect and manage the issues that arise when 3D models from different design disciplines are combined into a unified project coordination space.
The Photos API provides access to the data stored in the ACC Photos module. The Photos tool is the single unified place to view and manage photos and videos in ACC.
The Relationships API creates, retrieves, and deletes links between entities across domains in ACC.
The Reviews API provides access to data related to reviews in ACC projects, including approval workflows, review metadata, and file versions currently under review. Use it to check review progress, approval statuses, and file-level review outcomes. It also allows you to create approval workflows and review instances.
The RFIs API allows you to create, track, and update RFIs (Requests for Information). An RFI is a formal question raised by one project member to another—often to clarify design intent, such as by an architect. The API supports the full RFI workflow: assigning members, transitioning between RFI states, adding comments, and submitting both responses and official responses. You can also attach files to responses and official responses. Attachments are supported for ACC RFIs, but pushpin RFIs—those linked to specific document locations—are not supported in ACC. For more details, see the help documentation.
The Sheets API publishes and distributes sheets for use in the field. We currently support managing sheets and version sets, as well as uploading, publishing, and exporting sheets.
The Submittals API enables you to create submittal items and provides read access to the data stored in the ACC Submittals module.
The Takeoff API retrieves settings, classification systems, packages, takeoff types, takeoff items and content views associated with a takeoff project. It’s also possible to update settings, create and update packages, create, update, delete and reimport classifications.
BIM 360 Compatibility
In order to enable your current BIM 360 apps and integrations to be compatible with ACC projects, we have ensured that many BIM 360 endpoints are compatible with ACC. This makes it possible for you to access ACC projects and use your BIM 360 apps and integrations with compatible ACC APIs before new ACC APIs are available. Note that your existing apps and integrations to BIM 360 and PlanGrid will continue to function as-is for the foreseeable future. For more information, see the section on BIM 360 Compatibility.

Releasing New ACC APIs
We will keep you informed as we are able to share additional details on our ACC API development roadmap and timing, and our customer success and support team will work with you to take advantage of new capabilities when you are ready.

If you need answers to specific questions on the use of the ACC APIs or how to ensure your apps are compatible with both BIM 360 and ACC projects, we encourage you to reach out so you can learn details and get expert advice. Check out the APS blog or drop us an email.

Documentation /Autodesk Construction Cloud APIs /How-to Guide
Retrieve ACC Assets Data
This tutorial demonstrates how to fetch your complete set of Autodesk Construction Cloud Asset data and project settings. This can be for the entirety of your Asset data, or filtered to a subset of Asset data.

This set will include the assets themselves, as well as all of the surrounding Asset project settings:

categories
status sets / Asset statuses
Asset custom attributes
Assignments of status sets and Asset custom attributes to categories
Usage of pagination and batch-fetch endpoints are subject to rate limiting. For more details on Assets API rate limits, see the Assets Rate Limits.

Pagination
Most of the endpoints detailed below are paginated. Assets API uses cursor-based pagination, in which an opaque cursorState token is used to track the state of the pagination. Each paginated response will contain a results section, in which the relevant entities themselves will be returned, and a pagination section which will return the information needed to continue the pagination to fetch the full set of result entities. Pagination fields are described as follows -

Field	Description
limit	The maximum number of entities that MAY be returned for the pagination request in the results section. The results MAY contain less than the limit due to filtering or for other reasons. Can be passed into any pagination request to limit the number of results returned.
offset	The offset of the first entity returned in the results section. The offset is returned for reference, but cannot be passed in explicitly for pagination requests (the offset is computed automatically from the cursorState).
cursorState	An opaque token to identify the subsequent pagination results. Can be passed in to the subsequent request to continue pagination. If cursorState is missing from the response, you have reached the end of the pagination and all results have been returned. To restart pagination, simply omit the cursorState from the pagination request.
nextUrl	The URL for the next paginated request. Contains the cursorState and any additional filters that have been applied. The cursorState is returned independently as well to give the client more flexibility in how they wish to paginate through entities. If nextUrl is missing from the response, you have reached the end of the pagination and all results have been returned.
totalResults	Not returned for all pagination endpoints, but if present will provide the total number of entities that can be returned through the pagination.
For more details about Autodesk Construction Cloud Assets API, see the Assets Field Guide.

Before You Begin
Register an app, and select the Data Management and Autodesk Construction Cloud APIs.
Acquire a 3-legged OAuth token with data:read scope.
Verify that you have access to the relevant Autodesk Construction Cloud account, project, and folder.
Retrieve the relevant ACC account and project ID. In this tutorial we will use the example project ID f6a1e3b5-abaa-4b01-b33a-5d55f36ba047, but you should replace that with the project ID you have retrieved for your project.
Step 1: Fetch Assets
To get the assets themselves, use the project ID (f6a1e3b5-abaa-4b01-b33a-5d55f36ba047) to call GET assets/v2/projects/:projectId/assets.

You will want to ensure you set the query parameter includeCustomAttributes=true if you wish to include Asset custom attribute data in your fetch. If you want to include deleted assets, you can set the query parameter includeDeleted=true as well.

If you want to fetch a more targeted set of assets, you can provide additional filters in your request. This could include filtering by category, status, a specific location or a location hierarchy, custom attribute value(s), or any combination thereof. A complete list of the filters available, and how they are used, can be found in the query parameter documentation for the asset pagination endpoint. Filters provided in the initial pagination request will automatically be added to the nextUrl field to continue the filtered pagination.

If you want to include only assets that have changed since previously retrieving assets, you can use the query parameter filter filter[updatedAt]={previousFetchTime}...

Request
curl 'https://developer.api.autodesk.com/construction/assets/v2/projects/f6a1e3b5-abaa-4b01-b33a-5d55f36ba047/assets?includeCustomAttributes=true' \
     -H 'Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT'
Response
{
  "results": [
    {
      "id": "a36ff5f6-8d51-43b1-a3da-ed748a63eb5b",
      "version": 1,
      "createdAt": "2021-01-05T20:37:28.731Z",
      "createdBy": "KKD4J2WE984T",
      "updatedAt": "2021-01-05T20:37:28.731Z",
      "updatedBy": "KKD4J2WE984T",
      "isActive": true,
      "categoryId": "12",
      "locationId": "2b2656fa-d5ff-4a1f-b022-c3e803cadbd3",
      "companyId": "9fd5d33e-6a51-4edc-a647-ed737162f65d",
      "clientAssetId": "MVS-3D2",
      "statusId": "f92f1b17-d0ff-427d-ba6d-7326eaf497b0",
      "customAttributes": {
        "ca1": "110"
      }
    },
    {
      "id": "c319622f-3f05-4bb4-b717-afe02b4cd3c3",
      "version": 2,
      "createdAt": "2021-01-05T20:37:28.732Z",
      "createdBy": "KKD4J2WE984T",
      "updatedAt": "2021-01-05T20:37:28.732Z",
      "updatedBy": "KKD4J2WE984T",
      "isActive": true,
      "categoryId": "13",
      "locationId": "de780160-6aaf-4e99-b1c1-fc9f5cedbfa7",
      "companyId": "9fd5d33e-6a51-4edc-a647-ed737162f65d",
      "clientAssetId": "MVS-3D3",
      "statusId": "fbcedb87-decb-4a17-826f-948e8d2585a5",
      "customAttributes": {
        "ca1": "110",
        "ca2": true,
        "ca6": "1942-11-27"
      }
    },
    {
      "id": "d1625a1c-5bab-464f-816c-a6b79d5da4af",
      "version": 3,
      "createdAt": "2021-01-05T20:37:28.733Z",
      "createdBy": "KKD4J2WE984T",
      "updatedAt": "2021-01-05T20:37:28.733Z",
      "updatedBy": "KKD4J2WE984T",
      "isActive": true,
      "categoryId": "13",
      "locationId": "8704717d-20f3-4586-b741-86891d727479",
      "companyId": "9fd5d33e-6a51-4edc-a647-ed737162f65d",
      "clientAssetId": "MVS-3E1",
      "statusId": "fbcedb87-decb-4a17-826f-948e8d2585a5",
      "customAttributes": {
        "ca1": "220",
        "ca2": false,
        "ca6": "1970-09-18"
      }
    }
  ],
  "pagination": {
    "limit": 3,
    "offset": 0,
    "cursorState": "eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9",
    "nextUrl": "https://developer.api.autodesk.com/construction/assets/v1/projects/f6a1e3b5-abaa-4b01-b33a-5d55f36ba047/assets?cursorState=eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9"
  }
}
Show Less
Step 2: Fetch Categories
To get the categories, use the project ID (f6a1e3b5-abaa-4b01-b33a-5d55f36ba047) to call GET assets/v1/projects/:projectId/categories.

If you want to include only active categories, you can set the query parameter filter[isActive]=true. Note that filtering to only active or inactive categories can result in the returned tree not being fully intact.

If you want to include only categories that have changed since previously retrieving categories, you can use the query parameter filter filter[updatedAt]={previousFetchTime}...

Request
curl 'https://developer.api.autodesk.com/construction/assets/v1/projects/f6a1e3b5-abaa-4b01-b33a-5d55f36ba047/categories' \
     -H 'Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT'
Response
{
  "results": [
    {
      "id": "10",
      "name": "ROOT",
      "description": "Auto-generated ROOT category for Assets Category Hierarchy",
      "createdAt": "2021-01-05T19:55:59.603Z",
      "createdBy": "assets-service",
      "updatedAt": "2021-01-05T19:55:59.603Z",
      "updatedBy": "assets-service",
      "subcategoryIds": [ "12" ],
      "isActive": true,
      "isRoot": true,
      "isLeaf": false
    },
    {
      "id": "12",
      "name": "Electrical",
      "parentId": "10",
      "createdAt": "2021-01-05T20:37:27.381Z",
      "createdBy": "KKD4J2WE984T",
      "updatedAt": "2021-01-05T20:37:27.381Z",
      "updatedBy": "KKD4J2WE984T",
      "subcategoryIds": [ "13" ],
      "isActive": true,
      "isRoot": false,
      "isLeaf": false
    },
    {
      "id": "13",
      "name": "Light Fixtures",
      "parentId": "12",
      "createdAt": "2021-01-05T20:37:27.648Z",
      "createdBy": "KKD4J2WE984T",
      "updatedAt": "2021-01-05T20:37:27.648Z",
      "updatedBy": "KKD4J2WE984T",
      "subcategoryIds": [ ],
      "isActive": true,
      "isRoot": false,
      "isLeaf": false
    },
  ],
  "pagination": {
    "totalResults": 3
  }
}
Show Less
Step 3: Fetch Status Sets And Asset Statuses
To get the status sets, use the project ID (f6a1e3b5-abaa-4b01-b33a-5d55f36ba047) to call GET assets/v1/projects/:projectId/status-step-sets.

If you want to include deactivated status sets and Asset statuses, you can set the query parameter includeDeleted=true.

Note: If you just want to fetch the Asset statuses directly, you can call GET assets/v1/projects/:projectId/asset-statuses, but all statuses will be returned nested by fetching the full set of status sets as well.

If you want to include only status sets that have changed since previously retrieving status sets, you can use the query parameter filter filter[updatedAt]={previousFetchTime}... Note that this will only reflect updates to the status sets themselves, not any of the contained statuses. To fetch Asset statuses that have been changed since a given time, you can call GET assets/v1/projects/:projectId/asset-statuses with filter[updatedAt]={previousFetchTime}...

Request
curl 'https://developer.api.autodesk.com/construction/assets/v1/projects/f6a1e3b5-abaa-4b01-b33a-5d55f36ba047/status-step-sets' \
     -H 'Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT'
Response
{
  "results": [
    {
      "id": "391e0d38-7ad2-41be-a87c-ca590f1fee91",
      "version": 2925,
      "projectId": "f6a1e3b5-abaa-4b01-b33a-5d55f36ba047",
      "name": "Default",
      "isDefault": true,
      "values": [
        {
          "id": "f92f1b17-d0ff-427d-ba6d-7326eaf497b0",
          "version": 11695,
          "description": "Specified",
          "bucket": "specified",
          "label": "Specified",
          "color": "blue",
          "projectId": "f6a1e3b5-abaa-4b01-b33a-5d55f36ba047",
          "statusStepSetId": "391e0d38-7ad2-41be-a87c-ca590f1fee91",
          "createdBy": "KKD4J2WE984T",
          "createdAt": "2020-02-26T18:58:40.163Z",
          "updatedBy": "KKD4J2WE984T",
          "updatedAt": "2020-02-26T18:58:40.163Z",
          "isActive": true
        },
        {
          "id": "ebac8429-1fa7-4d37-81c3-e3352f6a24ec",
          "version": 11693,
          "description": "Ordered",
          "bucket": "ordered",
          "label": "Ordered",
          "color": "yellow",
          "projectId": "f6a1e3b5-abaa-4b01-b33a-5d55f36ba047",
          "statusStepSetId": "391e0d38-7ad2-41be-a87c-ca590f1fee91",
          "createdBy": "KKD4J2WE984T",
          "createdAt": "2020-02-26T18:58:40.176Z",
          "updatedBy": "KKD4J2WE984T",
          "updatedAt": "2020-02-26T18:58:40.176Z",
          "isActive": true
        }
      ],
      "createdAt": "2020-02-26T18:58:40.130Z",
      "createdBy": "KKD4J2WE984T",
      "updatedAt": "2020-02-26T18:58:40.130Z",
      "updatedBy": "KKD4J2WE984T",
      "isActive": true
    },
    {
      "id": "f0fc7dc2-a325-4b1b-982b-584278f9a873",
      "version": 2926,
      "projectId": "f6a1e3b5-abaa-4b01-b33a-5d55f36ba047",
      "name": "Light Fixtures Statuses",
      "isDefault": false,
      "values": [
        {
          "id": "fbcedb87-decb-4a17-826f-948e8d2585a5",
          "version": 11694,
          "description": "Delivered",
          "bucket": "delivered",
          "label": "Delivered",
          "color": "red",
          "projectId": "f6a1e3b5-abaa-4b01-b33a-5d55f36ba047",
          "statusStepSetId": "f0fc7dc2-a325-4b1b-982b-584278f9a873",
          "createdBy": "KKD4J2WE984T",
          "createdAt": "2020-02-26T18:58:40.189Z",
          "updatedBy": "KKD4J2WE984T",
          "updatedAt": "2020-02-26T18:58:40.189Z",
          "isActive": true
        }
      ],
      "createdAt": "2020-02-26T18:58:40.130Z",
      "createdBy": "KKD4J2WE984T",
      "updatedAt": "2020-02-26T18:58:40.130Z",
      "updatedBy": "KKD4J2WE984T",
      "isActive": true
    }
  ],
  "pagination": {
    "limit": 3,
    "offset": 0
  }
}
Show Less
Step 4: Fetch Status Set to Category Assignments
To get the status set to category assignments, use the project ID (f6a1e3b5-abaa-4b01-b33a-5d55f36ba047) and category IDs obtained in Step 3 to call POST assets/v1/projects/:projectId/category-status-step-sets/status-step-sets:batch-get.

By default this will only return the status sets explicitly assigned to the given categories. If you wish to return each category’s effective status set assignment (taking inheritance into account), you can set the query parameter includeInherited=true.

Request
curl 'https://developer.api.autodesk.com/construction/assets/v1/projects/f6a1e3b5-abaa-4b01-b33a-5d55f36ba047/category-status-step-sets/status-step-sets:batch-get?includeInherited=true' \
     -X 'POST' \
     -H 'Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT' \
     -H 'Content-Type: application/json' \
     -d '{
           "ids": [
             "10",
             "12",
             "13",
           ]
         }'
Show Less
Response
{
  "results": [
    {
      "categoryId": "10",
      "statusStepSetId": "391e0d38-7ad2-41be-a87c-ca590f1fee91"
    },
    {
      "categoryId": "12",
      "statusStepSetId": "391e0d38-7ad2-41be-a87c-ca590f1fee91"
    },
    {
      "categoryId": "13",
      "statusStepSetId": "f0fc7dc2-a325-4b1b-982b-584278f9a873"
    }
  ]
}
Show Less
Step 5: Fetch Asset Custom Attributes
To get the Asset custom attributes, use the project ID (f6a1e3b5-abaa-4b01-b33a-5d55f36ba047) to call GET assets/v1/projects/:projectId/custom-attributes.

If you want to include deactivated custom attributes, you can set the query parameter includeDeleted=true.

If you want to include only custom attributes that have changed since previously retrieving custom attributes, you can use the query parameter filter filter[updatedAt]={previousFetchTime}...

Request
curl 'https://developer.api.autodesk.com/construction/assets/v1/projects/f6a1e3b5-abaa-4b01-b33a-5d55f36ba047/custom-attributes' \
     -H 'Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT'
Response
{
  "results": [
    {
      "id": "5903f625-9cb3-4c78-be51-468ec9073d2a",
      "version": 7485,
      "projectId": "f6a1e3b5-abaa-4b01-b33a-5d55f36ba047",
      "dataType": "numeric",
      "displayName": "Voltage",
      "name": "ca1",
      "description": "Voltage of the Electrical asset",
      "requiredOnIngress": true,
      "createdBy": "KKD4J2WE984T",
      "createdAt": "2020-03-22T23:09:03.730Z",
      "updatedBy": "KKD4J2WE984T",
      "updatedAt": "2020-12-18T22:16:44.083Z",
      "isActive": true
    },
    {
      "id": "e37911e0-1cc3-4f18-aa91-1ff1907e29d0",
      "version": 7486,
      "projectId": "f6a1e3b5-abaa-4b01-b33a-5d55f36ba047",
      "dataType": "boolean",
      "displayName": "Grounded",
      "name": "ca2",
      "description": "Is the Electrical asset grounded?",
      "requiredOnIngress": true,
      "createdBy": "KKD4J2WE984T",
      "createdAt": "2020-03-22T23:11:08.689Z",
      "updatedBy": "KKD4J2WE984T",
      "updatedAt": "2020-12-18T22:16:46.565Z",
      "isActive": true
    },
    {
      "id": "da5989c5-cdf5-40a3-8447-3168335637b5",
      "version": 5985,
      "projectId": "f6a1e3b5-abaa-4b01-b33a-5d55f36ba047",
      "dataType": "date",
      "displayName": "Install date",
      "name": "ca6",
      "requiredOnIngress": false,
      "createdBy": "KKD4J2WE984T",
      "createdAt": "2020-10-22T20:45:01.425Z",
      "updatedBy": "KKD4J2WE984T",
      "updatedAt": "2020-10-22T20:45:01.425Z",
      "isActive": true
    },
  ],
  "pagination": {
    "limit": 3,
    "offset": 0
  }
}
Show Less
Step 6: Fetch Category to Asset Custom Attribute Assignments
To get the Asset custom attributes assigned to a category, use the project ID (f6a1e3b5-abaa-4b01-b33a-5d55f36ba047) and category IDs obtained in Step 3 to call GET assets/v1/projects/:projectId/categories/:categoryId/custom-attributes.

A batch endpoint doe not yet exist for this call, so at this time a call must be made for each category ID individually to get the full set of assignments.

By default this will only return the custom attributes explicitly assigned to the given category. If you wish to return the full set of custom attributes assigned to the given category, you can set the query parameter includeInherited=true. When includeInherited=true is set, an additional field will be included in the response for each returned custom attribute inheritedFromCategoryId which will indicate from which explicit category assignment the custom attribute is inherited from.

Request
curl 'https://developer.api.autodesk.com/construction/assets/v1/projects/f6a1e3b5-abaa-4b01-b33a-5d55f36ba047/categories/13/custom-attributes?includeInherited=true' \
     -H 'Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT'
Response
{
  "results": [
    {
      "id": "5903f625-9cb3-4c78-be51-468ec9073d2a",
      "version": 7485,
      "projectId": "f6a1e3b5-abaa-4b01-b33a-5d55f36ba047",
      "dataType": "numeric",
      "displayName": "Voltage",
      "name": "ca1",
      "description": "Voltage of the Electrical asset",
      "requiredOnIngress": true,
      "createdBy": "KKD4J2WE984T",
      "createdAt": "2020-03-22T23:09:03.730Z",
      "updatedBy": "KKD4J2WE984T",
      "updatedAt": "2020-12-18T22:16:44.083Z",
      "isActive": true,
      "inheritedFromCategoryId": "10"
    },
    {
      "id": "e37911e0-1cc3-4f18-aa91-1ff1907e29d0",
      "version": 7486,
      "projectId": "f6a1e3b5-abaa-4b01-b33a-5d55f36ba047",
      "dataType": "boolean",
      "displayName": "Grounded",
      "name": "ca2",
      "description": "Is the Electrical asset grounded?",
      "requiredOnIngress": true,
      "createdBy": "KKD4J2WE984T",
      "createdAt": "2020-03-22T23:11:08.689Z",
      "updatedBy": "KKD4J2WE984T",
      "updatedAt": "2020-12-18T22:16:46.565Z",
      "isActive": true,
      "inheritedFromCategoryId": "13"
    },
    {
      "id": "da5989c5-cdf5-40a3-8447-3168335637b5",
      "version": 5985,
      "projectId": "f6a1e3b5-abaa-4b01-b33a-5d55f36ba047",
      "dataType": "date",
      "displayName": "Install date",
      "name": "ca6",
      "requiredOnIngress": false,
      "createdBy": "KKD4J2WE984T",
      "createdAt": "2020-10-22T20:45:01.425Z",
      "updatedBy": "KKD4J2WE984T",
      "updatedAt": "2020-10-22T20:45:01.425Z",
      "isActive": true,
      "inheritedFromCategoryId": "13"
    },
  ],
  "pagination": {
    "limit": 3,
    "offset": 0,
    "totalResults": 3
  }
}
Show Less
Step 7: Fetch Locations
The Locations API can be used to fetch location data for the locationId field on an asset via the GET Nodes endpoint.

In this example the Project ID is f6a1e3b5-abaa-4b01-b33a-5d55f36ba047.

Request
curl -v 'https://developer.api.autodesk.com/construction/locations/v2/projects/f6a1e3b5-abaa-4b01-b33a-5d55f36ba047/trees/default/nodes?filter[id]=2b2656fa-d5ff-4a1f-b022-c3e803cadbd3,de780160-6aaf-4e99-b1c1-fc9f5cedbfa7'
  -H 'Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT'
Response
{
    "results": [
      {
        "id": "2b2656fa-d5ff-4a1f-b022-c3e803cadbd3,
        "parentId": null,
        "type": "Root",
        "name": "Project",
        "description": "Project description",
        "order": 0,
        "documentCount": 0,
        "areaDefined": false
      },
      {
        "id": "de780160-6aaf-4e99-b1c1-fc9f5cedbfa7,
        "parentId": "2b2656fa-d5ff-4a1f-b022-c3e803cadbd3",
        "type": "Area",
        "name": "Area 1",
        "description": "An Area 1 node",
        "order": 0,
        "documentCount": 2,
        "areaDefined": true
      }
    ],
    "pagination": {
      "limit": 2,
      "offset": 0,
      "totalResults": 2,
      "nextUrl": "/locations/v2/projects/4a327b27-897c-4e5a-8e48-6e01c21377f3/trees/default/nodes?limit=2&offset=2"
    }
  }
Show Less
Step 8: Fetch Asset Relationships
Assets can be associated with other entities such as Issues, Forms, Photos, etc. You can use the Relationship API to search for all relationships associated with your project, or for a given Asset directly.

For the Relationship API, your Container ID will simply be your Project ID.

See the Relationship v2 APIs documentation.

You can search for all relationships in your project which include an “asset” type using the following query parameters:

Query Parameter	Value(s)
domain	The Assets Relationship domain: autodesk-bim360-asset (NOTE: the domain is the same for Autodesk Construction Cloud assets or BIM360 assets)
type	The Assets Relationship types (see below for available options)
id	OPTIONAL - ID of the Asset to search relationships for
withDomain	OPTIONAL - The related entity domain (see below for available options)
withType	OPTIONAL - The related entity type (see below for available options)
withId	OPTIONAL - The related entity ID. e.g. checklist ID, issue ID, checklist template ID
Supported Related Domains and Types
Note that this list of Parameters is not exhaustive. More information on the Relationship API will be provided as it becomes available.

Also note that different Domains and Types are available for Autodesk Construction Cloud asset relationships than for BIM30 asset relationships, and that this is not necessarily determined by the domain itself. For example, and issue in the autodesk-bim360-issue domain can be related to an Autodesk Construction Cloud asset, as seen in the table below.

Type	Related Domain	Related Type
asset	autodesk-bim360-issue	issue
asset	autodesk-bim360-documentmanagement	documentlineage
asset	autodesk-construction-photo	photo
asset	autodesk-construction-form	form
asset	autodesk-construction-sheet	sheetlineage
asset	autodesk-construction-submittals	submittalitem
category	autodesk-construction-form	formtemplate
Example
In this example the Project ID and Relationship container ID is f6a1e3b5-abaa-4b01-b33a-5d55f36ba047. We would like to query the Relationship API for all relationships with assets within this project.

Request
curl -v 'https://developer.api.autodesk.com/bim360/relationship/v2/containers/f6a1e3b5-abaa-4b01-b33a-5d55f36ba047/relationships:search?domain=autodesk-bim360-asset&type=asset' \
  -H 'Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT'
Response
{
  "page": {
    "continuationToken": "10",
    "syncToken": "eyAibGFzdENoZWNrZWQiOiIyMDE5LTEwLTE4VDEyOjEwOjA3Ljc5NloiIH0="
  },
  "relationships": [
    {
      "id": "e005c68b-53af-41d0-9e56-9be86cd9c5a9",
      "createdOn": "2020-07-28T19:52:44.262208+00:00",
      "isReadOnly": true,
      "isService": true,
      "isDeleted": false,
      "entities": [
        {
          "createdOn": "2020-07-28T19:52:44.198281+00:00",
          "domain": "autodesk-bim360-asset",
          "type": "asset",
          "id": "71fa0b41-cd23-4439-8def-4348a2a45d4b"
        },
        {
          "createdOn": "2020-07-28T19:52:44.198281+00:00",
          "domain": "autodesk-bim360-issue",
          "type": "issue",
          "id": "84929da1-f71c-4a4d-9535-32c23db9a378"
        }
      ]
    }
  ]
}
Show Less
For more information on querying the Relationship API, see the Relationship Querying Tutorial.

Once you have the entities and their relationships to the given assets you can use the relevant APIs to fetch the data for the given entities. This may require setting up access to other APIs, depending on what type of entities are linked to your Assets. See Retrieve Issues and Get Forms Endpoint for examples of retrieving related entities.

Documentation /Autodesk Construction Cloud APIs /How-to Guide
Retrieve a Smart Register
This tutorial demonstrates how to retrieve submittal logs that have been imported to the AutoSpecs Smart Register. The steps include retrieving the hub ID for the account in which you want to retrieve the submittal logs, retrieving the ID of the project in which you want to retrieve the submittal logs, retrieving the ID of the relevant version, and retrieving the Smart Register.

Before You Begin
Register an app, and select the Data Management and Autodesk Construction Cloud APIs.
Acquire a 3-legged OAuth token with the data:read scope.
Verify that you have access to the relevant ACC account and project. Ensure that the logged in user has access to AutoSpecs.
Upload a spec book to the project. See the Upload a Spec Book documentation for more details. Note the AutoSpecs API does not currently support uploading spec books.
Step 1: Find the Hub ID for the ACC Account
In order to retrieve the ID of the project in which you want to retrieve the Smart Register, you first need to retrieve the ID of the relevant account. Call GET hubs to find the hub ID for the ACC account that contains the Smart Register you want to retrieve.

Note that the ACC account ID corresponds to a Data Management hub ID. To convert an account ID into a hub ID you need to add a “b." prefix. For example, an account ID of d952a4eb-ad57-4d64-b9ab-d540b3b4522e translates to a hub ID of **b.**\d952a4eb-ad57-4d64-b9ab-d540b3b4522e.

Request
curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT" "https://developer.api.autodesk.com/project/v1/hubs"
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "https://developer.api.autodesk.com/project/v1/hubs"
    }
  },
  "data": [
    {
      "type": "hubs",
      "id": "b.86b832e9-b22b-2acf-344b-454b3431ac8c",
      "attributes": {
        "name": "My First Account",
        "extension": {
          "type": "hubs:autodesk.bim360:Account",
          "version": "1.0",
          "schema": {
            "href": "https://developer.api.autodesk.com/schema/v1/versions/hubs:autodesk.bim360:Account-1.0"
          },
          "data": {}
        }
      }
    }
  ]
}
Show Less
In this example, assume that the account (and the corresponding Data Management hub) that contains the Smart Register you want to retrieve is called My First Account.

Find the hub (data.name), and note the hub ID - b.86b832e9-b22b-2acf-344b-454b3431ac8c.

Step 2: Find the Project ID
Use the hub ID (b.86b832e9-b22b-2acf-344b-454b3431ac8c) to call GET hubs/:hub_id/projects to get a list of all the projects in the account.

Note that the project ID in ACC corresponds to the project ID in the Data Management API. To convert a project ID in ACC to a project ID in the Data Management API, you need to add a “b." prefix. For example, a project ID of 75c643d1-c80b-4bca-800f-111a1111aa1a translates to a project ID of **b.**\75c643d1-c80b-4bca-800f-111a1111aa1a.

Request
curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT" "https://developer.api.autodesk.com/project/v1/hubs/b.86b832e9-b22b-2acf-344b-454b3431ac8c/projects"
Response
  {
       "jsonapi": {
               "version": "1.0"
       },
       "links": {
               "self": {
                       "href": "https://developer.api.autodesk.com/project/v1/hubs/b.cGVyc29uYWw6cGUyOWNjZjMy/projects"
               }
       },
       "data": [{
               "type": "projects",
               "id": "b.75c643d1-c80b-4bca-800f-111a1111aa1a",
               "attributes": {
                       "name": "My First Project",
                       "extension": {
                               "type": "projects:autodesk.core:Project",
                               "version": "1.0"
                       }
               }
       }]
}
Show Less
In this example, assume that My First Project is the project that contains the Smart Register you want to retrieve.

Find the project (data.attributes.name), and note the project ID (data.id) - b.75c643d1-c80b-4bca-800f-111a1111aa1a.

Step 3: Find the Spec Version
Use the project ID (75c643d1-c80b-4bca-800f-111a1111aa1a) to call GET metadata to get a list of the spec versions for the project.

Note that you need to remove the “b." prefix from the project ID.

Request
curl -v 'https://developer.api.autodesk.com/construction/autospecs/v1/projects/75c643d1-c80b-4bca-800f-111a1111aa1a/metadata' \
     -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
 "projectId": "75c643d1-c80b-4bca-800f-111a1111aa1a",
 "region": "USA",
 "versions": [
  {
   "name": "IFC",
   "status": "Completed",
   "currentVersion": false,
   "createdAt": "2022-11-02T07:29:06.000Z",
   "updatedAt": "2022-11-02T07:29:25.000Z",
   "id": "100"
  },
  {
   "name": "IFC 2",
   "status": "Completed",
   "currentVersion": true,
   "createdAt": "2022-06-20T07:12:26.000Z",
   "updatedAt": "2022-09-22T14:03:16.000Z",
   "id": "101"
  }
 ]
}
Show Less
In this example, assume that you want to use the current spec version (currentVersion: true).

Note the spec version ID (versions.id) - 101 of the current version.

Note that before you can access the submittal logs the import of the specification PDFs needs to be complete. To verify the status of the import, check that the status is Completed.

Step 4: Retrieve the Smart Register
Use the project ID (75c643d1-c80b-4bca-800f-111a1111aa1a) and the version ID (101) to call GET smartregister to retrieve the Smart Register.

Request
curl -v 'https://developer.api.autodesk.com/construction/autospecs/v1/projects/75c643d1-c80b-4bca-800f-111a1111aa1a/version/101/smartregister' \
     -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
[
 {
  "submittalsHeading": "Metals",
  "divisionCode": "01",
  "divisionName": "GENERAL REQUIREMENTS",
  "specNumber": "017419",
  "specName": "CONSTRUCTION WASTE MANAGEMENT AND DISPOSAL",
  "submittalDescription": "Paint compatibility certificates",
  "specCategory": "Certificates",
  "targetDate": null,
  "userNotes": null,
  "paraCode": "051213",
  "targetGroup": "DIVISION 01 REQUIREMENTS",
  "versionName": null,
  "specSubmittalNumber": 0,
  "submittalId": "146"
 },
 {
  "submittalsHeading": "ACTION SUBMITTALS",
  "divisionCode": "01",
  "divisionName": "General Requirements",
  "specNumber": "017419",
  "specName": "CONSTRUCTION WASTE MANAGEMENT AND DISPOSAL",
  "submittalDescription": "Waste Management Plan : Submit plan within 30 days of date established for the Notice to",
  "specCategory": "Waste Management Plan",
  "targetDate": null,
  "userNotes": null,
  "paraCode": "1.5-A",
  "targetGroup": "DIVISION 01 REQUIREMENTS",
  "versionName": "v3",
  "specSubmittalNumber": 0,
  "submittalId": "147"
 },
 {
  "submittalsHeading": "ACTION SUBMITTALS",
  "divisionCode": "01",
  "divisionName": "General Requirements",
  "specNumber": "017419",
  "specName": "CONSTRUCTION WASTE MANAGEMENT AND DISPOSAL",
  "submittalDescription": "Waste Management Plan : Submit plan within 30 days of date established for the Notice to",
  "specCategory": "Waste Management Plan",
  "targetDate": null,
  "userNotes": null,
  "paraCode": "1.5-A",
  "targetGroup": "DIVISION 01 REQUIREMENTS",
  "versionName": "v3",
  "specSubmittalNumber": 0,
  "submittalId": "123"
 }
]
Show Less
Congratulations! You have retrieved a Smart Register.

Documentation /Autodesk Construction Cloud APIs /How-to Guide
Submit a Data Request
This phase of the tutorial demonstrates how to submit a data request that extracts service data from within a BIM 360/ACC account. In this tutorial, your data request will be a recurring request that spawns a job once every week, and returns extracted data for seven different services.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with data:create, data:read, and data:write scopes. The token’s authenticated user must have executive overview permissions or project administrator permissions.
Verify that you have access to a relevant BIM 360/ACC account that contains at least one project. If you don’t know your account ID, you can derive it from your hub ID: Use GET hubs in the Data Management API to retrieve your hub ID. Remove the initial “b.” from the hub ID to get your account ID. For example, a hub ID of b.c8b0c73d-3ae9 translates to an account ID of c8b0c73d-3ae9.
Step 1: Determine Your Data Parameters
To make a data request, you’ll have to provide request parameter values that correctly specify the type of data extraction you want the Data Connector service to perform and to provide other useful information stored with the request:

description contains a text string describing the data request, in this case "My Weekly Extract".
scheduleInterval specifies the interval unit we’ll use for scheduling. In this case we measure in weeks, so the value is WEEK.
reoccuringInterval specifies the number of units to wait between job spawns. Because we want this request to spawn a job once every week, the value is 1.
effectiveFrom and effectiveTo define the starting and ending times for the recurring jobs. It’s during this time that the jobs spawn and execute, starting on the effectiveFrom time and ending on the effectiveTo time. These two values define date and time in ISO 8601 format. For this example, we’ll set a one-year interval. Our example values: 2020-11-19T16:00:00Z start time, 2021-11-19T16:00:00Z end time.
serviceGroups defines the scope of the data extraction for this data request: the services for which we want to examine data. In this case, we look at admin, issues, locations, submittals, cost, and rfis. You can also specify all to extract data for all service groups. Note that the admin service covers both project and account administration.
projectId specifies which project to extract data from. Usage depends on the permissions level of the authenticated user:
Executive Overview permissions — (optional) If neither projectId or projectIdList is specified, the request will apply to all projects in the user’s account.
Project Administrator permissions — (required) If neither projectId or ``projectIdList` is specified, the request will fail.
projectIdList specifies the list of projects to extract data from. projectId can be omitted if projectIdList is used. If both are provided, projectIdList takes precedence. The user needs to have either Executive Overview permission, or Project Administrator permission in all the projects provided in the list. Otherwise, the request will fail.
projectStatus specifies the scope of the projects based on the project status. Use active if only data extraction from active projects is required.
Step 2: Create a Data Request
Create a data request using the POST requests endpoint, specifying the account ID of your account. This tutorial demonstrates recurring data requests for two scenarios:

Retrieving data for a specific list of projects using projectIdList.
Retrieving data for all active projects in the account using projectStatus.
Scenario 1: Requesting Data for Specific Projects
If the user wants to extract data for specific projects, include the projectIdList field in the request payload. This field specifies up to 50 project IDs.

Request
curl -X POST 'https://developer.api.autodesk.com/data-connector/v1/accounts/<accountId>/requests' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <authToken>' \
-d '

{
    "description": "My Weekly Extract",
    "scheduleInterval": "WEEK",
    "reoccuringInterval": 1,
    "effectiveFrom": "2020-11-19T16:00:00Z",
    "effectiveTo": "2021-11-19T16:00:00Z",
    "serviceGroups": ["admin", "issues", "locations", "submittals", "cost", "rfis"],
    "projectIdList": [
    "ffffffff-1f51-4b26-a6b7-6ac0639cb138",
    "aaaaaaaa-1f51-4b26-a6b7-6ac0639cb138"        ]
}'
Show Less
Response
{
    "id": "55e410c5-4294-44ce-becf-68e1cfd6738c",
    "isActive": true,
    "accountId": "872264f8-2433-498d-8d36-16649ecb13fe",
    "projectId": null,
    "projectIdList": [
    "ffffffff-1f51-4b26-a6b7-6ac0639cb138",
    "aaaaaaaa-1f51-4b26-a6b7-6ac0639cb138"
  ],
    "description": "My Weekly Extract",
    "createdBy": "73f00c25-a5f9-4c05-861d-ce56d54fa649",
    "createdByEmail": "your.name@autodesk.com",
    "updatedBy": "73f00c25-a5f9-4c05-861d-ce56d54fa649",
    "scheduleInterval": "WEEK",
    "reoccuringInterval": 1,
    "effectiveFrom": "2020-11-19T16:00:00.000Z",
    "effectiveTo": "2021-11-19T16:00:00.000Z",
    "nextExecAt": "2020-11-19T16:00:00.000Z",
    "serviceGroups": [
        "admin",
        "issues",
        "locations",
        "submittals",
        "cost",
        "rfis"
    ],
    "callbackUrl": null,
    "lastQueuedAt": null,
    "updatedAt": "2020-11-19T16:32:13.545Z",
    "createdAt": "2020-11-19T16:32:13.545Z",
    "deletedAt": null    }
Show Less
Scenario 2: Requesting Data for Active Projects
If the user has executive overview permissions and wants to retrieve data for all active projects in the account, use the projectStatus field.

Request
curl -X POST 'https://developer.api.autodesk.com/data-connector/v1/accounts/<accountId>/requests' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <authToken>' \
-d '

{
    "description": "My Weekly Extract",
    "scheduleInterval": "WEEK",
    "reoccuringInterval": 1,
    "effectiveFrom": "2020-11-19T16:00:00Z",
    "effectiveTo": "2021-11-19T16:00:00Z",
    "serviceGroups": ["admin", "issues", "locations", "submittals", "cost", "rfis"],
    "projectStatus": "active"
}'
Show Less
Response
{
    "id": "55e410c5-4294-44ce-becf-68e1cfd6738c",
    "isActive": true,
    "accountId": "872264f8-2433-498d-8d36-16649ecb13fe",
    "description": "My Weekly Extract",
    "createdBy": "73f00c25-a5f9-4c05-861d-ce56d54fa649",
    "createdByEmail": "your.name@autodesk.com",
    "updatedBy": "73f00c25-a5f9-4c05-861d-ce56d54fa649",
    "scheduleInterval": "WEEK",
    "reoccuringInterval": 1,
    "effectiveFrom": "2020-11-19T16:00:00.000Z",
    "effectiveTo": "2021-11-19T16:00:00.000Z",
    "nextExecAt": "2020-11-19T16:00:00.000Z",
    "serviceGroups": [
        "admin",
        "issues",
        "locations",
        "submittals",
        "cost",
        "rfis"
    ],
    "callbackUrl": null,
    "lastQueuedAt": null,
    "updatedAt": "2020-11-19T16:32:13.545Z",
    "createdAt": "2020-11-19T16:32:13.545Z",
"deletedAt": null,
"projectStatus": "active"
Show Less
The response reports the data request settings and status, and includes an id value that provides the data request ID. Use the data request ID to specify this data request when calling other Data Connector API endpoints. If you don’t save the ID, you can query the API (as we’ll do in the next example) for the data request IDs of your data requests currently stored by the Data Connector service.

Notice that optional field values not set in the request get set to default values.

Documentation /Autodesk Construction Cloud APIs /How-to Guide
Find and Update a Data Request
This tutorial shows how to find and update an existing data request stored by the Data Connector service. For this example, we’ll change the description of the data request created in the last tutorial. We’ll start by retrieving all your currently saved data requests so that we can find the appropriate data request and its data request ID. We’ll then examine the data request’s current settings, and change its description.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with data:create, data:read, and data:write scopes. The token’s authenticated user must have executive overview permissions.
Verify that you have access to a relevant BIM 360 account that contains at least one project. If you don’t know your account ID, you can derive it from your hub ID: Use GET hubs in the Data Management API to retrieve your hub ID. Remove the initial “b.” from the hub ID to get your account ID. For example, a hub ID of b.c8b0c73d-3ae9 translates to an account ID of c8b0c73d-3ae9.
Step 1: Get a List of Saved Requests
Use GET requests to retrieve a list of your saved data requests. This endpoint retrieves a list that is restricted to the requester’s saved data requests, so it won’t list any data requests created by other users. If you have many saved data requests, you can set request parameters to limit the number of returned requests, offset the point where you start returning requests, and set sort order. We won’t specify any of this, so the endpoint will use default settings of ascending sort order, a limit of 20 requests, and no offset.

Request
curl -X GET 'https://developer.api.autodesk.com/data-connector/v1/accounts/<accountId>/requests?limit=20&sort=desc' \
-H 'Authorization: Bearer <authToken>'
Response
{
    "pagination": {
        "limit": 20,
        "offset": 0,
        "totalResults": 1
    },
    "results": [
        {
            "id": "55e410c5-4294-44ce-becf-68e1cfd6738c",
            "description": "My Weekly Extract",
            "isActive": true,
            "accountId": "872264f8-2433-498d-8d36-16649ecb13fe",
            "projectId": "ffffffff-1f51-4b26-a6b7-6ac0639cb138",
            "createdBy": "73f00c25-a5f9-4c05-861d-ce56d54fa649",
            "createdByEmail": "your.name@autodesk.com",
            "updatedBy": "73f00c25-a5f9-4c05-861d-ce56d54fa649",
            "scheduleInterval": "WEEK",
            "reoccuringInterval": 1,
            "effectiveFrom": "2020-11-19T16:00:00.000Z",
            "effectiveTo": "2021-11-19T16:00:00.000Z",
            "lastQueuedAt": "2020-11-19T16:32:54.725Z",
            "nextExecAt": "2020-11-26T16:00:00.000Z",
            "serviceGroups": [
                "admin",
                "issues",
                "locations",
                "submittals",
                "cost",
                "rfis"
            ],
            "callbackUrl": null,
            "createdAt": "2020-11-19T16:32:13.545Z",
            "updatedAt": "2020-11-19T16:32:54.728Z",
            "deletedAt": null
        }
    ]
}
Show Less
The results returned by this endpoint report the ID, settings, and status of each data request (in this case just the single data request we created in the last tutorial). We’ll use the ID of the data request in the next step when we update the data request.

Note that if you have the ID of a single data request for which you want to see status, you can use the GET requests/:requestId endpoint instead of this endpoint to retrieve the request’s status without having to list other data requests.

Documentation /Autodesk Construction Cloud APIs /How-to Guide
Find a Job and Retrieve Its Data Extract
When an active data request spawns a job, the job extracts data for specified services. To retrieve and examine that data, you need the ID of the job. You receive that ID through the email notification that the job sends on completion and, if you specified a callback URL, a post that the job sends on completion. You may also retrieve a list of jobs spawned by the data request. There you can find the ID of a job whose data extract you wish to examine.

To retrieve the job’s data extract, first use the job ID to retrieve descriptions of the files in the data extract. You can use those descriptions to determine which of the files you’d like to examine, and then request a URL where you can retrieve your desired files.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with data:create, data:read, and data:write scopes. The token’s authenticated user must have executive overview permissions.
Verify that you have access to a relevant BIM 360 account that contains at least one project. If you don’t know your account ID, you can derive it from your hub ID: Use GET hubs in the Data Management API to retrieve your hub ID. Remove the initial “b.” from the hub ID to get your account ID. For example, a hub ID of b.c8b0c73d-3ae9 translates to an account ID of c8b0c73d-3ae9.
Step 1: Get a List of Jobs Spawned By Your Data Request
In this example, we’ll assume you don’t have the ID of the job whose data extract you want. Use the GET requests/:requestId/jobs endpoint to retrieve a list of the jobs that your data request has spawned, or use the GET jobs endpoint to retrieve a list of all the jobs that were spawned for the project you specify. If you think there are many spawned jobs, you can set request parameters to limit the number of returned job descriptions, offset the point where you start returning requests, and set sort order. We won’t specify any of this, so the endpoint will use default settings of ascending sort order, a limit of 20 requests, and no offset.

You’ll need the ID of the data request that spawned the jobs, something you retrieved in the previous tutorials.

Request
curl -X GET 'https://developer.api.autodesk.com/data-connector/v1/accounts/<accountId>/requests/<requestId>/jobs?sort=desc&limit=10&offset=0' \
-H 'Authorization: Bearer <authToken>'
Response
{
    "pagination": {
        "limit": 10,
        "offset": 0,
        "totalResults": 1
    },
    "results": [
        {
            "id": "9bd7c8a0-9fde-478b-82b7-44098d27c1c1",
            "requestId": "55e410c5-4294-44ce-becf-68e1cfd6738c",
            "accountId": "872264f8-2433-498d-8d36-16649ecb13fe",
            "projectId": "ffffffff-1f51-4b26-a6b7-6ac0639cb138",
            "createdBy": "73f00c25-a5f9-4c05-861d-ce56d54fa649",
            "createdByEmail": "your.name@autodesk.com",
            "status": "complete",
            "completionStatus": "success",
            "startedAt": "2020-11-19T16:33:04.688Z",
            "completedAt": "2020-11-19T16:34:05.293Z",
            "createdAt": "2020-11-19T16:32:54.672Z"
        }
    ]
}
Show Less
The response provides an array of job records (in this case, just a single job), each with information about a job’s status. The beginning of each record is the ID of the job, which you’ll use to specify the job in subsequent endpoint calls.

Step 2: Examine the Files Contained in the Job’s Data Extract
To see a list of the files contained in your job’s data extract, use the GET jobs/:jobId/data-listing endpoint and use the job ID to specify the job.

Request
curl -X GET 'https://developer.api.autodesk.com/data-connector/v1/accounts/<accountId>/jobs/<jobId>/data-listing' \
-H 'Authorization: Bearer <authToken>'
Response
[
    {
        "name": "README.html",
        "createdAt": "2020-11-19T16:34:04.579Z",
        "size": 8892
    },
    {
        "name": "admin_account_services.csv",
        "createdAt": "2020-11-19T16:33:05.058Z",
        "size": 117
    }

...numerous other .csv file listings...

    {
        "name": "admin_users.csv",
        "createdAt": "2020-11-19T16:33:05.106Z",
        "size": 3104
    },
    {
        "name": "autodesk_data_extract.zip",
        "createdAt": "2020-11-19T16:34:04.591Z",
        "size": 53792
    },

...numerous other .csv file listings...

    {
        "name": "submittals_specs.csv",
        "createdAt": "2020-11-19T16:33:35.170Z",
        "size": 125
    }
]
Show Less
The first file is a README file that contains information about the schema used in each of the CSV files in the data extract. Listed a bit later is a ZIP file that contains all of the other files in the data extract including the README file. The other files are each CSV files for a particular type of object within a service. Each of the file descriptions returns the filename, when the file was created, and the size of the file in bytes.

Step 3: Retrieve a File From a Data Extract
Once you have a job ID and the filename of the file in the data extract that you’d like to retrieve, use GET jobs/:jobId/data/:name to get a signed URL where you can retrieve that data, in this case the ZIP file that contains all the files in the extract along with information about the schemas used.

Request
curl -X GET 'https://developer.api.autodesk.com/data-connector/v1/accounts/<accountId>/jobs/<jobId>/data/autodesk_data_extract.zip' \
-H 'Authorization: Bearer <authToken>'
Response
{
    "name": "autodesk_data_extract.zip",
    "size": 53792,
    "signedUrl": "https://bim360dc-p-ue1-extracts.s3.amazonaws.com/data/872264e8-2433-498d-8d36-16649ecb13fe/9bd7c8a0-9fde-478b-82b7-44098d27c1c1/autodesk_data_extract.zip?AWSAccessKeyId=ASIAWZ7KRFT5U5KAQRUI&Expires=1605806413&Signature=5T68bvEaz0f6p4U%2FDZgmpub957c%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEOn%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCICvo%2F3hehNnqaTXjleNDCmA6p%2F3yWvrsonrBE4nql5ZZAiEAtjSD1kSupwy2vr%2Bp%2Ftt4TBbHj%2BqorI9iRSMeZzTJe1kq2gEIYhACGgw0NjgxMDY0MjM1NDciDDV9RA39yMDubKMpOSq3AWO%2BzbHgSMkHe180nF2Pj050zZiwml94Ux0CJvGtOzfLrQXHWuEjSsddk6DllxLKp%2BGlFBezGkPeRnAlZRVrDXlAyJu%2FensrqPmPXmugluRmvfblAehj7%2FqwsRTFCbJhzJELMQ40GvyEBMXJMJ5gQ8lcAXrxg6TReuBr8mSHmn5U%2F5r56HwwwO3ddOgw%2FfwUY8mQ%2BIjpbF45EMKDJxCqdL2zA2quQKZ617O4%2FIq4eJl6%2F42J10nK%2FzC%2Ft9r9BTrgASDpnOPAkrMIl44%2FXyucqjMQ8A9Dk8DLAKQiV2SXYxdGyONXLpDdCYc0ZGlVcSOGIJq0J2QYMFKAABT6BipiGq%2FFn8RYeWSZO17Y%2FogJCC6TZipvJD0XbYm%2Bi%2FGfRO9%2BPjK8y1DAPtZE1SWA%2F21uWEigbNXTt9AWKnYUzdojNoz9uFKEmRXf8HA95AU%2Ftc3Q%2FxMoV0f8b0h%2FtbecyljXxCMRfnrhGJ1uaSGTIyVpHuDti0hWCDxFjVODC4mUYqrQoKzwQC6jNjohVqiagKZVNK5MTlA6jhp6U9xQdn8tCOjO"
}
Use the signed URL returned in the response within 60 seconds. It will return the specified ZIP file from the data extract.

Documentation /Autodesk Construction Cloud APIs /How-to Guide
Export Files from the ACC Files Tool
This tutorial demonstrates how to export PDF, RVT and DWG files that were uploaded to the ACC Files module. The steps include finding the IDs of the files you want to export, exporting the files (you can optionally also export associated markups and hyperlinks), verifying the status of the export, getting a download link, and downloading the exported files.

Note that you can only export PDF, RVT, and DWG files. A maximum of 200 files is allowed in a single export operation. When exporting multiple files at once, they will be compressed and exported as a single ZIP file.

For more information about exporting files, see the Export Files help documentation.

Before You Begin
Register an app, and select Autodesk Construction Cloud API.
Provision your app to acquire access to your ACC account.
Acquire a 3-legged OAuth token with data:write scope.
Find the relevant hub ID and project ID for the project from which you want to export files by following the Retrieve a Project ID tutorial. Assume that the hub ID is b.cGVyc29uYWw6cGUyOWNjZjMy, and the project ID is b.139532ee-5cdb-4c9e-a293-652693991e65.
Verify that you have access to the relevant ACC project.
Step 1: Find the Folder ID of the Files to Export
You first need to find the folder ID of the folder containing the files you want to export. Start by retrieving the parent folder ID, then, if necessary, iterate through the child folders until you locate the correct folder ID.

To find the parent folder ID, use the hub ID (b.cGVyc29uYWw6cGUyOWNjZjMy) and project ID (b.139532ee-5cdb-4c9e-a293-652693991e65) to call GET hubs/:hub_id/projects/:project_id/topFolders.

Request
curl -X GET "https://developer.api.autodesk.com/project/v1/hubs/b.cGVyc29uYWw6cGUyOWNjZjMy/projects/b.139532ee-5cdb-4c9e-a293-652693991e65/topFolders" \
  -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT"
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "data": [
    {
      "type": "folders",
      "id": "urn:adsk.wipprod:fs.folder:co.BJU3PTc4Sd2CmXM492XUiA",
      "attributes": {
        "name": "Plans",
        "displayName": "Plans",
        "createTime": "2017-07-17T13:06:56.0000000Z",
        "createUserId": "",
        "createUserName": "",
        "lastModifiedTime": "2017-09-24T07:46:08.0000000Z",
        "lastModifiedUserId": "X9WYLGPNCHSL",
        "lastModifiedUserName": "John Smith",
        "objectCount": 4,
        "hidden": false,
        "extension": {
          "type": "folders:autodesk.bim360:Folder",
          "version": "1.0",
          "schema": {
            "href": "https://developer.api.autodesk.com/schema/v1/versions/folders:autodesk.bim360:Folder-1.0"
          },
          "data": {
            "visibleTypes": [
              "items:autodesk.bim360:Document"
            ],
            "actions": [
              "CONVERT",
              "SPLIT",
              "OCR"
            ],
            "allowedTypes": [
              "items:autodesk.bim360:File",
              "folders:autodesk.bim360:Folder",
              "items:autodesk.bim360:Document",
              "items:autodesk.bim360:TitleBlock",
              "items:autodesk.bim360:ReviewDocument"
            ]
          }
        }
      }
    }
  ]
}
Show Less
Note the folder ID - data.id (urn:adsk.wipprod:fs.folder:co.BJU3PTc4Sd2CmXM492XUiA).

If you want to export a file from a folder nested under the parent folder, you need to call GET projects/:project_id/folders/:folder_id/contents repeatedly through the hierarchy of folders until you find the folder ID of the folder that contains the files you want to export.

Step 2: Find the Version IDs of the Files to Export
To export the files, you’ll also need the version IDs of the files. To find the version IDs, use the project ID (b.139532ee-5cdb-4c9e-a293-652693991e65), and the folder ID (urn:adsk.wipprod:fs.folder:co.BJU3PTc4Sd2CmXM492XUiA) to call GET projects/:project_id/folders/:folder_id/contents.

Note that you need to URL-encode the folder ID - urn%3Aadsk.wipprod%3Afs.folder%3Aco.BJU3PTc4Sd2CmXM492XUiA.

Note that if you want to export a different version of the file, use GET projects/:project_id/items/:item_id/versions to find the relevant version ID.

Request
curl -X GET 'https://developer.api.autodesk.com/data/v1/projects/b.139532ee-5cdb-4c9e-a293-652693991e65/folders/urn%3Aadsk.wipprod%3Afs.folder%3Aco.BJU3PTc4Sd2CmXM492XUiA/contents' \
  -H 'authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT'
Response
Note that some lines in this payload example have been omitted for readability.

{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "https://developer.api.autodesk.com/data/v1/projects/b.94d60d03-1e8c-4f32-b146-dd3173e655d8/folders/urn:adsk.wipprod:fs.folder:co.hTcJTDRzTQCnxySVOg6avQ/contents"
    }
  },
  "data": [
    {
      "type": "items",
      "id": "urn:adsk.wipprod:dm.lineage:Ww95QMRfTSCJfbSdVat6FQ",
      "attributes": {
        "...": "..."
      },
      "relationships": {
        "tip": {
          "data": {
            "type": "versions",
            "id": "urn:adsk.wipprod:fs.file:vf.Ww95QMRfTSCJfbSdVat6FQ?version=1"
          }
        }
      }
    },
    {
      "type": "items",
      "id": "urn:adsk.wipprod:dm.lineage:15Rg8B38Qp-SEu6HzXlTNg",
      "attributes": {
        "...": "..."
      },
      "relationships": {
        "tip": {
          "data": {
            "type": "versions",
            "id": "urn:adsk.wipprod:fs.file:vf.15Rg8B38Qp-SEu6HzXlTNg?version=1"
          }
        }
      }
    }
  ],
  "included": [
    {
      "type": "versions",
      "id": "urn:adsk.wipprod:fs.file:vf.Ww95QMRfTSCJfbSdVat6FQ?version=1",
      "attributes": {
        "name": "A-101 FLOOR PLANS",
        "displayName": "A-101 FLOOR PLANS",
        "createTime": "2017-08-25T08:58:57.0000000Z",
        "createUserId": "200906020304322",
        "createUserName": "John Smith",
        "lastModifiedTime": "2017-08-25T08:59:05.0000000Z",
        "lastModifiedUserId": "200906020304322",
        "lastModifiedUserName": "John Smith",
        "versionNumber": 1,
        "extension": {
          "type": "versions:autodesk.bim360:Document",
          "version": "1.0",
          "schema": {
            "href": "https://developer.api.autodesk.com/schema/v1/versions/versions:autodesk.bim360:Document-1.0"
          },
          "data": {
            "...": "..."
          }
        }
      }
    },
    {
      "type": "versions",
      "id": "urn:adsk.wipprod:fs.file:vf.15Rg8B38Qp-SEu6HzXlTNg?version=1",
      "attributes": {
        "name": "A-102 FLOOR PLANS",
        "displayName": "A-102 FLOOR PLANS",
        "createTime": "2017-08-25T08:58:57.0000000Z",
        "createUserId": "200906020304322",
        "createUserName": "John Smith",
        "lastModifiedTime": "2017-08-25T08:59:05.0000000Z",
        "lastModifiedUserId": "200906020304322",
        "lastModifiedUserName": "John Smith",
        "versionNumber": 1,
        "extension": {
          "type": "versions:autodesk.bim360:Document",
          "version": "1.0",
          "schema": {
            "href": "https://developer.api.autodesk.com/schema/v1/versions/versions:autodesk.bim360:Document-1.0"
          },
          "data": {
            "...": "..."
          }
        }
      }
    }
  ]
}
Show Less
Find the name of the file you want to export - included[i].attributes.displayName (A-102 FLOOR PLANS). It is the name that appears in the ACC Files module UI. Note the version ID - included[i].id (urn:adsk.wipprod:fs.file:vf.15Rg8B38Qp-SEu6HzXlTNg?version=1).

Step 3: Export the Files
To export the file, use the project ID ((b.139532ee-5cdb-4c9e-a293-652693991e65) and the version ID (urn:adsk.wipprod:fs.file:vf.15Rg8B38Qp-SEu6HzXlTNg?version=1), to call POST exports.

Note that this endpoint is asynchronous and initiates a job that runs in the background rather than halting execution of your program. You can check whether the asynchronous job is complete by calling GET exports/{exportId}.

When exporting the markup file, you can also customize the output filename and export the file’s markup links. For more information about markup links, please see Markups Links and References Help Documentation.

This example exports all of the available markup types, published (public) and unpublished (private) markups, and all links attached to standard markups.

Request
curl -v 'https://developer.api.autodesk.com/construction/files/v1/projects/139532ee-5cdb-4c9e-a293-652693991e65/exports' \
  -X 'POST' \
  -H 'authorization: Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6Imp3dF9zeW1tZXRyaWNfa2V5In0' \
  -H 'content-type: application/json' \
  -d '{
      "options": {
        "outputFileName": "MyOutputFile",
        "standardMarkups": {
          "includePublishedMarkups": true,
          "includeUnpublishedMarkups": true,
          "includeMarkupLinks": true
        },
        "issueMarkups": {
          "includePublishedMarkups": true,
          "includeUnpublishedMarkups": true
        },
        "photoMarkups": {
          "includePublishedMarkups": true,
          "includeUnpublishedMarkups": true
        }
      },
      "fileVersions": [
        "urn:adsk.wipprod:fs.file:vf.15Rg8B38Qp-SEu6HzXlTNg?version=1"
      ]
    }'
Show Less
Response
{
  "id":"225eb2fb-d5b0-44c9-a50a-2c792d833f2e",
  "status":"processing"
}
Note the export ID (id - 225eb2fb-d5b0-44c9-a50a-2c792d833f2e). You use the export ID to verify the status of the export and to get a download link for the export.

Step 4: Verify the Status of the Export and Get a Download Link
To verify the status of the export and to retrieve the data you need to download the exported files when the export job is complete, use the project ID (b.139532ee-5cdb-4c9e-a293-652693991e65) and the export ID (225eb2fb-d5b0-44c9-a50a-2c792d833f2e) to call GET /exports/{exportId}.

When the status is successful the export is complete and a signed URL appears in the response, which you can use to download the sheets.

Request
curl -X GET 'https://developer.api.autodesk.com/construction/files/v1/projects/139532ee-5cdb-4c9e-a293-652693991e65/exports/225eb2fb-d5b0-44c9-a50a-2c792d833f2e' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response with successful status
{
  "id": "636e6a96-d4d2-43e6-b67a-db8618fc0ff9",
  "status": "successful",
  "result": {
    "output": {
      "signedUrl": "https://accpes-s-ue1-storage.s3.amazonaws.com/{bucketId}/jobs/{jobId}/result.pdf?response-content-disposition={fileName}&AWSAccessKeyId={awsKey}&Signature={signature}&x-amz-security-token={token}&Expires={expire}"
    }
  }
}
Show Less
Note the signed URL (result.output.signedUrl), which you can use for downloading the exported files directly from S3. The link is available for one hour. If you need to download the files after that, you need to call POST /projects/{projectId}/exports again.

Response with failed status
{
  "id": "636e6a96-d4d2-43e6-b67a-db8618fc0ff9",
  "status": "failed",
  "result": {
    "error": {
      "code": "401",
      "title": "ERR_AUTHORIZATION_ERROR",
      "detail": "Authentication header is not correct"
    }
  }
}
Show Less
Step 5: Download the Exported File
To download the files from the signed URL, use a GET method and the URL attribute (result.output.signedUrl) as the URI.

Note that you should not use a bearer token with this call.

Request
curl -X 'GET' -v 'https://accpes-s-ue1-storage.s3.amazonaws.com/{bucketId}/jobs/{jobId}/result.pdf?response-content-disposition={fileName}&AWSAccessKeyId={awsKey}&Signature={signature}&x-amz-security-token={token}&Expires={expire}'
Response:
Status Code: 200 OK
Content-Type:application/pdf
Content-Length:90616

with chunked content body
Congratulations! You have exported files from the ACC Files module.

Documentation /Autodesk Construction Cloud APIs /How-to Guide
Download Files from the ACC Files Tool
This tutorial demonstrates how to download files from the ACC Files tool. The steps include finding the ID of the folder that contains the file, locating the storage object for the file, generating a signed S3 URL, and downloading the file from the signed S3 URL.

For more details about the ACC files management, see the Data Management API.

Before You Begin
Register an app, and select the Data Management and Autodesk Construction Cloud APIs.
Acquire a 3-legged OAuth token with data:create data:read and data:write scopes.
Verify that you have access to the relevant ACC account and ACC project.
Note the name of the ACC account, project, and folder that contains the file you want to download.
Step 1: Find the Hub ID for the ACC Account
The first few steps of the tutorial demonstrate how to find the ID of the folder that contains the file you want to download, which invovles iterating through several Data Management endpoints.

Call GET hubs to find the hub ID for the ACC account that contains the file you want to download.

Note that the ACC account ID corresponds to a Data Management hub ID. To convert an account ID into a hub ID you need to add a “b." prefix. For example, an account ID of c8b0c73d-3ae9 translates to a hub ID of b.c8b0c73d-3ae9.

Request
curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT" "https://developer.api.autodesk.com/project/v1/hubs"
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "https://developer.api.autodesk.com/project/v1/hubs"
    }
  },
  "data": [
    {
      "type": "hubs",
      "id": "b.cGVyc29uYWw6cGUyOWNjZjMy",
      "attributes": {
        "name": "My First Account",
        "extension": {
          "type": "hubs:autodesk.acc:Account",
          "version": "1.0",
          "schema": {
            "href": "https://developer.api.autodesk.com/schema/v1/versions/hubs:autodesk.acc:Account-1.0"
          },
          "data": {}
        }
      }
    }
  ]
}
Show Less
In this example, assume that the account (and the corresponding Data Management hub) that contains the file you want to download is called My First Account.

Find the hub (data.name), and note the hub ID - b.cGVyc29uYWw6cGUyOWNjZjMy.

Step 2: Find the Project ID
Use the hub ID (b.cGVyc29uYWw6cGUyOWNjZjMy) to call GET hubs/:hub_id/projects to get a list of all the projects in the hub. Find the project ID of the project that contains the folder you want to download the file from.

Note that the project ID in ACC corresponds to the project ID in the Data Management API. To convert a project ID in ACC to a project ID in the Data Management API, you need to add a “b." prefix. For example, a project ID of a4be0c34a-4ab7 translates to a project ID of b.a4be0c34a-4ab7.

Request
curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT" "https://developer.api.autodesk.com/project/v1/hubs/b.cGVyc29uYWw6cGUyOWNjZjMy/projects"
Response
  {
       "jsonapi": {
               "version": "1.0"
       },
       "links": {
               "self": {
                       "href": "https://developer.api.autodesk.com/project/v1/hubs/b.cGVyc29uYWw6cGUyOWNjZjMy/projects"
               }
       },
       "data": [{
               "type": "projects",
               "id": "b.cGVyc29uYWw6d2l",
               "attributes": {
                       "name": "My First Project",
                       "extension": {
                               "type": "projects:autodesk.core:Project",
                               "version": "1.0"
                       }
               }
       }]
}
Show Less
In this example, assume that My First Project is the project that contains the folder you want to download the document from.

Find the project (data.attributes.name), and note the project ID (data.id) - b.cGVyc29uYWw6d2l.

Step 3: Find the Folder ID
Use the hub ID (b.cGVyc29uYWw6cGUyOWNjZjMy) and the project ID (b.cGVyc29uYWw6d2l) to call GET hubs/:hub_id/projects/:project_id/topFolders to get the top-level folders.

Request
curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT"
            "https://developer.api.autodesk.com/project/v1/hubs/b.cGVyc29uYWw6cGUyOWNjZjMy/projects/b.cGVyc29uYWw6d2l/topFolders"
Response
{
      "jsonapi": {
              "version": "1.0"
      },

      "data": [{
              "type": "folders",
              "id": "urn:adsk.wipprod:fs.folder:co.BJU3PTc4Sd2CmXM492XUiA",
              "attributes": {
                      "name": "Project Files",
                      "displayName": "Project Files",
                      "createTime": "2017-07-17T13:06:56.0000000Z",
                      "createUserId": "",
                      "createUserName": "",
                      "lastModifiedTime": "2017-09-24T07:46:08.0000000Z",
                      "lastModifiedUserId": "X9WYLGPNCHSL",
                      "lastModifiedUserName": "John Smith",
                      "objectCount": 4,
                      "hidden": false,
                      "extension": {
                              "type": "folders:autodesk.acc:Folder",
                              "version": "1.0",
                              "schema": {
                                      "href": "https://developer.api.autodesk.com/schema/v1/versions/folders:autodesk.acc:Folder-1.0"
                              },
                              "data": {
                                      "visibleTypes": [
                                              "items:autodesk.acc:File"
                                      ],
                                      "actions": [
                                              "CONVERT"
                                      ],
                                      "allowedTypes": [
                                              "items:autodesk.acc:File",
                                              "folders:autodesk.acc:Folder"
                                      ]
                              }
                      }
              }
      }]
}
Show Less
Find the relevant folder (data.attributes.name), and note the folder ID (data.id) - urn:adsk.wipprod:fs.folder:co.BJU3PTc4Sd2CmXM492XUiA

If you want to download a file from a folder nested under the top-level folder, you need to call GET projects/:project_id/folders/:folder_id/contents repeatedly through the hierarchy of folders until you find the Folder ID of the folder you want to upload the file to. For the first iteration, use the top-level folder ID (urn:adsk.wipprod:fs.folder:co.BJU3PTc4Sd2CmXM492XUiA).

Step 4: Find the Storage Object ID for the File
Use the project ID (b.cGVyc29uYWw6d2l) and the Projet Files folder ID (urn:adsk.wipprod:fs.folder:co.BJU3PTc4Sd2CmXM492XUiA) to call GET projects/:project_id/folders/:folder_id/contents to get the storage object ID.

Request
curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT"
    "https://developer.api.autodesk.com/data/v1/projects/b.cGVyc29uYWw6d2l/folders/urn:adsk.wipprod:fs.folder:co.BJU3PTc4Sd2CmXM492XUiA/contents"
Response
{
      "jsonapi": {
              "version": "1.0"
      },
      "included": [{
              "type": "versions",
              "id": "urn:adsk.wipprod:fs.file:vf.II0yMfUPQl6DaOl5z-dhcg?version=1",
              "attributes": {
                      "name": "My First File.dwg",
                      "displayName": "My First File.dwg",
                      "createTime": "2017-10-02T11:06:44.0000000Z",
                      "createUserId": "X9WYLGPNCHVK",
                      "createUserName": "John Smith",
                      "lastModifiedTime": "2017-10-02T11:07:45.0000000Z",
                      "lastModifiedUserId": "X9WYLGPNCHVK",
                      "lastModifiedUserName": "John Smith",
                      "versionNumber": 1,
                      "storageSize": 1952608,
                      "fileType": "dwg",
                      "extension": {
                              "type": "versions:autodesk.acc:File",
                              "version": "1.0",
                              "schema": {
                                      "href": "https://developer.api.autodesk.com/schema/v1/versions/versions:autodesk.acc:File-1.0"
                              },
                              "data": {
                                      "processState": "PROCESSING_COMPLETE",
                                      "extractionState": "FAILED",
                                      "splittingState": "NOT_SPLIT",
                                      "reviewState": "NOT_IN_REVIEW",
                                      "revisionDisplayLabel": "1"
                              }
                      }
              },
              "links": {
                      "relationships": {
                              "storage": {
                                      "data": {
                                              "type": "objects",
                                              "id": "urn:adsk.objects:os.object:wip.dm.prod/72d5e7e4-89a7-4cb9-9da0-2e2bbc61ca8e.dwg"
                                      },
                                      "meta": {
                                              "link": {
                                                      "href": "https://developer.api.autodesk.com/oss/v2/buckets/wip.dm.prod/objects/72d5e7e4-89a7-4cb9-9da0-2e2bbc61ca8e.dwg"
                                              }
                                      }
                              }
                      }
              }
      }]
Show Less
}

In this example, assume that My First File is the file that you want to download.

Find the file (included.attributes.name), and note the storage object ID (relationships.storage.data.id) - urn:adsk.objects:os.object:wip.dm.prod/72d5e7e4-89a7-4cb9-9da0-2e2bbc61ca8e.dwg.

The storage object ID includes of the following sections: <urn:adsk.objects:os.object>:<bucket_key>/<object_key>

Note the bucket key - wip.dm.prod and the storage object key - 72d5e7e4-89a7-4cb9-9da0-2e2bbc61ca8e.dwg

Step 5: Generate a Signed S3 URL
Use the bucket key (wip.dm.prod) and the object key (72d5e7e4-89a7-4cb9-9da0-2e2bbc61ca8e.dwg) to call GET buckets/:bucketKey/objects/:objectKey/signeds3download to generate a signed URL for the storage object, which you can use to download the file directly from S3.

Request
curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT" "https://developer.api.autodesk.com/oss/v2/buckets/wip.dm.prod/objects/72d5e7e4-89a7-4cb9-9da0-2e2bbc61ca8e.dwg/signeds3download"
Response
{
  "status": "complete",
  "url": "https://cdn.us.oss.api.autodesk.com/com.autodesk.oss-persistent/us-east-1/3f/bf/5f/0137a7d9dc53af930bc1b527320d50fb5f/wip.dm.prod?response-content-type=application%2Foctet-stream&response-content-disposition=attachment%3B+filename%3D%977d69b1-43e7-40fa-8ece-6ec4602892f3.rvt%22&Expires=1643864703&Signature=00PZYS6gL~Nc6aRG2HAhOCKYl0xtqsuujMJ~VKSXm1vBa-OxS4lPQBSlTx5bswpLBe1W6Rz94eIZW2sPN-v6Mzz~JyXNZ-V9Z7zlBoE1VoQhspLioC225hxq6ZmDSU5QnZXuNDV4ih~p1n3xacYvUvQWX-ONAGVUgQvZ253Svw~qx-pO4j-Yh4kVRmzDZqQut1xOI5ZGH6JFGhXLSzkgbYcfYx6fvCxnvYUJrgAcqncIwGVewI3uC0I84Fzrj8nXE8ojuojqJP0pNlxkfBe~2LfjjzqKDKaNvfC2Grt12j9QgC~cN7nQCRcVUhExpoV1VVB5x3AkVTJ-q5NoedvsfO__&Key-Pair-Id=95HRZD7MMO1UK",
  "params": {
    "content-type": "application/octet-stream",
    "content-disposition": "attachment; filename=\"977d69b1-43e7-40fa-8ece-6ec4602892f3.rvt\""
  },
  "size": 472424,
  "sha1": "ffbf5f0137a7d9dc53af930bc1b527320d50fb53"
}
Show Less
Step 6: Download the File
To download the file from the signed URL, use a GET method and the url attribute as the URI.

Note that you should not use a bearer token with this call.

Request
curl -X GET "https://cdn.us.oss.api.autodesk.com/com.autodesk.oss-persistent/us-east-1/3f/bf/5f/0137a7d9dc53af930bc1b527320d50fb5f/wip.dm.prod?response-content-type=application%2Foctet-stream&response-content-disposition=attachment%3B+filename%3D%977d69b1-43e7-40fa-8ece-6ec4602892f3.dwg%22&Expires=1643864703&Signature=00PZYS6gL~Nc6aRG2HAhOCKYl0xtqsuujMJ~VKSXm1vBa-OxS4lPQBSlTx5bswpLBe1W6Rz94eIZW2sPN-v6Mzz~JyXNZ-V9Z7zlBoE1VoQhspLioC225hxq6ZmDSU5QnZXuNDV4ih~p1n3xacYvUvQWX-ONAGVUgQvZ253Svw~qx-pO4j-Yh4kVRmzDZqQut1xOI5ZGH6JFGhXLSzkgbYcfYx6fvCxnvYUJrgAcqncIwGVewI3uC0I84Fzrj8nXE8ojuojqJP0pNlxkfBe~2LfjjzqKDKaNvfC2Grt12j9QgC~cN7nQCRcVUhExpoV1VVB5x3AkVTJ-q5NoedvsfO__&Key-Pair-Id=95HRZD7MMO1UK" --output "My First File.dwg"
Congratulations! You have downloaded a file from the ACC Files tool.

Documentation /Autodesk Construction Cloud APIs /How-to Guide
Download RVT Files from a Published Model
This tutorial demonstrates how to retrieve temporary download links (signed URLs) and metadata for a published version of a Cloud Workshared Revit (RVT) model, as well as for any linked RVT models it references.

The steps include finding the version ID of the published host model, generating signed URLs and metadata, and downloading the RVT files using the signed URLs.

You can also use this workflow to retrieve a download URL for a specific published host model version, even if no linked models are present.

Each time you retrieve the signed URLs, they are newly generated and valid for 1 hour.

Before You Begin
Register an app, and select the Data Management and Autodesk Construction Cloud APIs.
Acquire a 3-legged OAuth token with the data:read scope.
Verify that you have access to the relevant ACC or BIM 360 account, project, and folder.
Ensure that the Revit model has been published to the cloud from Revit, and that it is a Cloud Workshared model.
Step 1: Find the Hub ID for the BIM 360 or ACC Account
The first four steps show how to use Data Management endpoints to locate the version ID of the Revit host model. You first need to find the ID of the hub (account) that contains the project where the Revit host model is stored.

Call GET hubs to retrieve a list of the BIM 360 or ACC accounts your app has access to.

Note that the BIM 360 account ID corresponds to a Data Management hub ID. To convert an account ID into a hub ID you need to add a “b." prefix. For example, the account ID c8b0c73d-3ae9 becomes b.c8b0c73d-3ae9.

Request
curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT" "https://developer.api.autodesk.com/project/v1/hubs"
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "https://developer.api.autodesk.com/project/v1/hubs"
    }
  },
  "data": [
    {
      "type": "hubs",
      "id": "b.35da59e5-4acb-4979-85f1-518047215eaa",
      "attributes": {
        "name": "ACME Construction - East Coast",
        "extension": {
          "type": "hubs:autodesk.bim360:Account",
          "version": "1.0",
          "schema": {
            "href": "https://developer.api.autodesk.com/schema/v1/versions/hubs:autodesk.bim360:Account-1.0"
          },
          "data": {}
        }
      }
    }
  ]
}
Show Less
In this example, assume that the Cloud Workshared Revit model from which you want to retrieve the linked RVT files is stored in a hub called ACME Construction - East Coast.

Find the hub in the response (data.attributes.name), and note the hub ID (data.id) — b.35da59e5-4acb-4979-85f1-518047215eaa.

Step 2: Find the Project ID
Find the project that contains the Cloud Workshared Revit model from which you want to retrieve the linked RVT files.

Use the hub ID (b.35da59e5-4acb-4979-85f1-518047215eaa) to call GET hubs/:hub_id/projects to get a list of all the projects in the hub. Find the project ID of the project that contains the folder of the Cloud Workshared Revit model from which you want to retrieve the linked RVT files.

Note that the project ID in BIM 360 corresponds to the project ID in the Data Management API. To convert a project ID in BIM 360 or ACC to a project ID in the Data Management API, you need to add a “b." prefix. For example, a project ID of a4be0c34a-4ab7 translates to a project ID of b.a4be0c34a-4ab7.

Request
curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT" "https://developer.api.autodesk.com/project/v1/hubs/b.35da59e5-4acb-4979-85f1-518047215eaa/projects"
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "https://developer.api.autodesk.com/project/v1/hubs/b.35da59e5-4acb-4979-85f1-518047215eaa/projects"
    }
  },
  "data": [
    {
      "type": "projects",
      "id": "b.12cd67f0-07e5-4e54-b66b-fb8d1785357a",
      "attributes": {
        "name": "Main Office Tower",
        "extension": {
          "type": "projects:autodesk.core:Project",
          "version": "1.0"
        }
      }
    }
  ]
}
Show Less
In this example, assume that the Cloud Workshared Revit model from which you want to retrieve the linked RVT files is stored in a project called Main Office Tower

Find the project (data.attributes.name), and note the project ID (data.id) - b.12cd67f0-07e5-4e54-b66b-fb8d1785357a.

Step 3: Find the Project Files Folder ID
Find the folder where the Cloud Workshared Revit model is stored. Most models are stored in the Project Files folder.

Use the hub ID (b.35da59e5-4acb-4979-85f1-518047215eaa) and the project ID (b.12cd67f0-07e5-4e54-b66b-fb8d1785357a) to call GET hubs/:hub_id/projects/:project_id/topFolders to get the Project Files folder ID.

Request
curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT"
            "https://developer.api.autodesk.com/project/v1/hubs/b.35da59e5-4acb-4979-85f1-518047215eaa/projects/b.12cd67f0-07e5-4e54-b66b-fb8d1785357a/topFolders"
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "data": [
    {
      "type": "folders",
      "id": "urn:adsk.wipprod:fs.folder:co.BJU3PTc4Sd2CmXM492XUiA",
      "attributes": {
        "name": "Project Files",
        "displayName": "Project Files",
        "createTime": "2017-07-17T13:06:56.0000000Z",
        "createUserId": "",
        "createUserName": "",
        "lastModifiedTime": "2017-09-24T07:46:08.0000000Z",
        "lastModifiedUserId": "X9WYLGPNCHSL",
        "lastModifiedUserName": "John Smith",
        "objectCount": 4,
        "hidden": false,
        "extension": {
          "type": "folders:autodesk.bim360:Folder",
          "version": "1.0",
          "schema": {
            "href": "https://developer.api.autodesk.com/schema/v1/versions/folders:autodesk.bim360:Folder-1.0"
          },
          "data": {
            "visibleTypes": [
              "items:autodesk.bim360:File"
            ],
            "actions": [
              "CONVERT"
            ],
            "allowedTypes": [
              "items:autodesk.bim360:File",
              "folders:autodesk.bim360:Folder"
            ]
          }
        }
      }
    }
  ]
}
Show Less
Find the folder (data.attributes.name); in this example, the Project Files folder, and note the folder ID (data.id) - urn:adsk.wipprod:fs.folder:co.BJU3PTc4Sd2CmXM492XUiA

Step 4: Find the Latest Published Version ID
Use the project ID and the folder ID to call GET projects/:project_id/folders/:folder_id/contents to get the tip version ID of the Cloud Workshared Revit model from which you want to retreive the linked RVT files.

To filter out non-cloud workshared Revit files, apply the items:autodesk.bim360:C4RModel filter.

Request
curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT"
    "https://developer.api.autodesk.com/data/v1/projects/b.12cd67f0-07e5-4e54-b66b-fb8d1785357a/folders/urn:adsk.wipprod:fs.folder:co.BJU3PTc4Sd2CmXM492XUiA/contents?filter[attributes.extension.type]=items%3Aautodesk.bim360%3AC4RModel"
Response
{
"jsonapi": {
  "version": "1.0"
},
"links": {
  "self": {
    "href": "https://developer.api.autodesk.com/data/v1/projects/b.c8112490-4e08-435c-994b-64fe60fea507/folders/urn:adsk.wipprod:fs.folder:co.BJU3PTc4Sd2CmXM492XUiA/contents?filter[attributes.extension.type]=items:autodesk.bim360:C4RModel"
  }
},
"data": [
  {
    "type": "items",
    "id": "urn:adsk.wipprod:dm.lineage:hPW2BlBbQG2L5HjCOh7Z8Q",
    "attributes": {
      "displayName": "DemoModel",
      "createTime": "2018-02-22T17:51:11.0000000Z",
      "createUserId": "38SCJGX4R4PV",
      "createUserName": "John Doe",
      "lastModifiedTime": "2018-02-22T17:58:36.0000000Z",
      "lastModifiedUserId": "38SCJGX4R4PV",
      "lastModifiedUserName": "John Doe",
      "hidden": false,
      "reserved": false,
      "extension": {
        "type": "items:autodesk.bim360:C4RModel",
        "version": "1.0.0",
        "schema": {
          "href": "https://developer.api.autodesk.com/schema/v1/versions/items:autodesk.bim360:C4RModel-1.0.0"
        },
        "data": {}
      }
    }
  }
],
"included": [
  {
    "type": "versions",
    "id": "urn:adsk.wipprod:fs.file:vf.hPW2BlBbQG2L5HjCOh7Z8Q?version=3",
    "attributes": {
      "name": "DemoModel.rvt",
      "displayName": "DemoModel",
      "createTime": "2018-02-22T17:57:43.0000000Z",
      "createUserId": "38SCJGX4R4PV",
      "createUserName": "John Doe",
      "lastModifiedTime": "2018-02-22T17:58:37.0000000Z",
      "lastModifiedUserId": "38SCJGX4R4PV",
      "lastModifiedUserName": "John Doe",
      "versionNumber": 3,
      "mimeType": "application/vnd.autodesk.r360",
      "fileType": "rvt",
      "extension": {
        "type": "versions:autodesk.bim360:C4RModel",
        "version": "1.1.0",
        "schema": {
          "href": "https://developer.api.autodesk.com/schema/v1/versions/versions:autodesk.bim360:C4RModel-1.1.0"
        },
      }
    }
  }
]
Show Less
}

In this example, assume that the model from which you want to retrieve the linked RVT files is called DemoModel.

Find the model in the response (included[i].attributes.displayName), and note the latest published version ID (included[i].id) — urn:adsk.wipprod:fs.file:vf.hPW2BlBbQG2L5HjCOh7Z8Q?version=3.

Step 5: Retrieve Signed URLs for the Host and Linked Models
Use the project ID (b.12cd67f0-07e5-4e54-b66b-fb8d1785357a) and the version ID (urn:adsk.wipprod:fs.file:vf.hPW2BlBbQG2L5HjCOh7Z8Q?version=3) of the published Cloud Workshared Revit model to call GET construction/rcm/v1/projects/:project_id/published-versions/:version_id/linked-files. This call retrieves metadata and temporary download links (signed URLs) for:

The published version of the host model (unless you set includeHost=false)
Any Revit files that are linked into that version of the model.
Make sure the version ID in the request URL is URL-encoded.

Request
curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT"
"https://developer.api.autodesk.com/construction/rcm/v1/projects/b.12cd67f0-07e5-4e54-b66b-fb8d1785357a/published-versions/urn%3Aadsk.wipprod%3Adm.lineage%3AhPW2BlBbQG2L5HjCOh7Z8Q%3Fversion%3D3/linked-files"
Repsonse
{
  "hostFile": {
      "modelName": "DemoModel.rvt",
      "signedUrl": "https://c4r-s-ue1-project-data.s3.amazonaws.com/publish/0932a81e-e4e1-4e5b-8e65-8406ac3a2eed/version_10.rvt?AWSAccessKeyId",
      "itemId": "urn:adsk.wipprod:dm.lineage:hPW2BlBbQG2L5HjCOh7Z8Q",
      "versionId": "urn:adsk.wipprod:dm.lineage:hPW2BlBbQG2L5HjCOh7Z8Q?version=3",
      "size": 7184384,
      "publishStatus": "Published"
  },
  "linkedFiles": {
      "pagination": {
          "limit": 600,
          "offset": 0,
          "totalResults": 5
      },
      "results": [{
              "modelName": "Project_2.rvt",
              "signedUrl": "https://c4r-s-ue1-project-data.s3.amazonaws.com/publish/f553a4c1-fc68-4a7d-9459-66c9a9b4d958/version_7.rvt?AWSAccessKeyId",
              "itemId": "urn:adsk.wipstg:dm.lineage:K1IKTUl1Qji7vIEJ3E6FxA",
              "versionId": "urn:adsk.wipstg:fs.file:vf.K1IKTUl1Qji7vIEJ3E6FxA?version=6",
              "size": 5525504,
              "publishStatus": "Published"
          }, {
              "modelName": "Project_3.rvt",
              "signedUrl": "https://c4r-s-ue1-project-data.s3.amazonaws.com/publish/2a08695e-4d60-429c-a2d4-7e1c605be0b5/version_7.rvt?AWSAccessKeyId",
              "itemId": "urn:adsk.wipstg:dm.lineage:E4DVafMOTnqxZ5TiV4qMGw",
              "versionId": "urn:adsk.wipstg:fs.file:vf.BKbru6y-SlSYelQ1DJ0AmQ?version=3",
              "size": 5464064,
              "publishStatus": "Published"
          }, {
              "modelName": "Project_4.rvt",
              "signedUrl": "https://c4r-s-ue1-project-data.s3.amazonaws.com/publish/06c94ed0-1154-4e7f-933e-d0123d5e2a0c/version_10.rvt?AWSAccessKeyId",
              "itemId": "urn:adsk.wipstg:dm.lineage:1eML_KSoQVSkJRT3mkf8Ag",
              "versionId": "urn:adsk.wipstg:fs.file:vf.EIT81_eXRu6Sj_FD2llA_Q?version=3",
              "size": 5636096,
              "publishStatus": "Published"
          }, {
              "modelName": "rme_advanced_sample_project.rvt",
              "signedUrl": "https://c4r-s-ue1-project-data.s3.amazonaws.com/publish/317e60a0-eb91-4c93-9c83-79c92a27a243/version_23.rvt?AWSAccessKeyId",
              "itemId": "urn:adsk.wipstg:dm.lineage:JPmHHTXeQJ6Bna0vdKWeXA",
              "size": 37253120,
              "publishStatus": "NotPublished"
          }, {
              "modelName": "Project_5.rvt",
              "signedUrl": "https://c4r-s-ue1-project-data.s3.amazonaws.com/publish/358e20b7-a989-47e6-8abf-85dcbf41a684/version_6.rvt?AWSAccessKeyId",
              "itemId": "urn:adsk.wipstg:dm.lineage:svs0bN2gSFqPGYtpb9WL9Q",
              "size": 7450624,
              "publishStatus": "NotPublished"
          }
      ]
  }
Show Less
}

The response includes two top-level keys:

hostFile – Contains metadata and a signed URL for the host model. This object is returned by default unless includeHost=false is explicitly set in the request.
linkedFiles – Contains metadata and signed URLs for any Revit models that are linked into the specified version of the host model.
Step 6: Download the RVT Files
To download the host model or any of the linked RVT files, use a GET method and the corresponding signedUrl value from the response in Step 5 as the URI.

Note that you should not include a bearer token in this request.

Request
curl -X GET "https://c4r-s-ue1-project-data.s3.amazonaws.com/publish/0932a81e-e4e1-4e5b-8e65-8406ac3a2eed/version_10.rvt?AWSAccessKeyId"
Congratulations! You have downloaded a Revit model from ACC using a signed URL.

Documentation /Autodesk Construction Cloud APIs /How-to Guide
Retrieve Forms
This tutorial demonstrates how to retrieve a project’s Forms.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with the data:read scope.
Verify that you have access to the relevant ACC project.
Step 1: Find the Form Template IDs
Use the project ID (9ba6681e-1952-4d54-aac4-9de6d9858dd4) to retrieve the project’s Form Templates, by calling GET form-templates.

Request
curl "https://developer.api.autodesk.com/construction/forms/v1/projects/9ba6681e-1952-4d54-aac4-9de6d9858dd4/form-templates" -X GET \
  -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT" \
  -H "Content-Type: application/vnd.api+json"
Response
{
  "data": [
    {
      "projectId": "9ba6681e-1952-4d54-aac4-9de6d9858dd4",
      "id": "2f634a22-779d-4930-9f08-8391a41fea05",
      "name": "Daily Report",
      "status": "active",
      "templateType": "pg.template_type.daily_report",
      "userPermissions": [
        {
          "permissions": [
            "submit"
          ],
          "userId": "USER123A"
        }
      ],
      "groupPermissions": [
        {
          "permissions": [
            "manage"
          ],
          "roleKey": "hq_access_level:admin",
          "roleName": "Admin"
        }
      ],
      "createdBy": "USER123A",
      "updatedAt": "2020-11-20T16:13:33.615127+00:00",
      "isPdf": true,
      "pdfUrl": "https://link.to/form-template.pdf",
      "forms": {}
    }
  ],
  "pagination": {
    "offset": 0,
    "limit": 50,
    "totalResults": 1,
    "nextUrl": null
  }
}
Show Less
The response payload includes the Form Template IDs (data.id).

Step 2: Find the Form IDs
Use the project ID (9ba6681e-1952-4d54-aac4-9de6d9858dd4) and template ID (2f634a22-779d-4930-9f08-8391a41fea05) from previous step to retrieve the project’s Forms, by calling GET forms.

Request
curl "https://developer.api.autodesk.com/construction/forms/v1/projects/9ba6681e-1952-4d54-aac4-9de6d9858dd4/forms?templateId=2f634a22-779d-4930-9f08-8391a41fea05" -X GET \
  -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT" \
  -H "Content-Type: application/vnd.api+json"
Response
{
  "data": [
    {
      "status": "draft",
      "id": "932da979-e537-4530-b8aa-18607ac6db37",
      "projectId": "9ba6681e-1952-4d54-aac4-9de6d9858dd4",
      "formNum": 1,
      "formDate": "2020-11-20",
      "assigneeId": "USER123A",
      "locationId": "d14ce3a6-e61b-4ab0-a9be-5acf7b5366df",
      "updatedAt": "2020-11-20T16:14:27.615127+00:00",
      "createdBy": "USER123A",
      "notes": "Form notes",
      "description": "Form description",
      "formTemplate": {
        "status": "active",
        "id": "2f634a22-779d-4930-9f08-8391a41fea05",
        "projectId": "9ba6681e-1952-4d54-aac4-9de6d9858dd4",
        "name": "Daily Report",
        "templateType": "pg.template_type.daily_report"
      },
      "pdfValues": [],
      "pdfUrl": null,
      "weather": {
        "summaryKey": "clear",
        "precipitationAccumulation": 2.3,
        "precipitationAccumulationUnit": "in",
        "temperatureMin": 47.1,
        "temperatureMax": 65.1,
        "temperatureUnit": "Fahrenheit",
        "humidity": 0.2,
        "windSpeed": 12.5,
        "windGust": 34.6,
        "speedUnit": "mph",
        "windBearing": 18,
        "hourlyWeather": [
          {
            "id": 1234,
            "hour": "07:00:00",
            "temp": 54.12,
            "windSpeed": 14.2,
            "windBearing": 14,
            "humidity": 0.24,
            "fetchedAt": null,
            "createdAt": "2021-01-20T20:38:32+00:00",
            "updatedAt": "2021-01-20T20:38:32+00:00"
          }
        ]
      },
      "tabularValues": {
        "worklogEntries": [
          {
            "id": "cb95aceb-187a-3a8f-2e5f-502a555c03d5",
            "deleted": false,
            "trade": "Plumbers",
            "timespan": 21600000,
            "headcount": 4,
            "description": "change pipes"
          }
        ],
        "materialsEntries": [
          {
            "id": "2f7e534d-d084-594b-8aa6-147cb8fbc060",
            "deleted": false,
            "item": "Glue",
            "quantity": 3,
            "unit": "qt",
            "description": null
          }
        ],
        "equipmentEntries": [
          {
            "id": "84a32af6-b2b1-c3ae-c186-caef48fe4ffd",
            "deleted": false,
            "item": "Hammer",
            "timespan": 7200000,
            "quantity": 1,
            "description": null
          }
        ]
      },
      "customValues": [
        {
          "sectionLabel": "Observation",
          "itemLabel": "Masks / Face Protection",
          "valueName": "textVal",
          "textVal": "Yes",
          "notes": "Observed Masks and Face Protection"
        }
      ]
    }
  ],
  "pagination": {
    "offset": 0,
    "limit": 50,
    "totalResults": 1,
    "nextUrl": null
  }
}
Show Less
The response payload includes the Form IDs (data.id).

Congratulations! You have retrieved Forms.

Documentation /Autodesk Construction Cloud APIs /How-to Guide
Retrieve Forms Associated With Specific Locations
This tutorial demonstrates how to retrieve forms that are associated with a specific location in a project.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with the data:read scope.
Verify that you have access to the relevant ACC project, and find the project ID. In the example, the project ID is 9ba6681e-1952-4d54-aac4-9de6d9858dd4.
Step 1: Find the Locations for the Project
Use the project ID (9ba6681e-1952-4d54-aac4-9de6d9858dd4) to retrieve the locations for the project, by calling GET nodes

Request
curl -v 'https://developer.api.autodesk.com/construction/locations/v2/projects/9ba6681e-1952-4d54-aac4-9de6d9858dd4/trees/:treeId/nodes' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 3,
    "offset": 0,
    "totalResults": 7,
    "nextUrl": "/locations/v2/containers/4a327b27-897c-4e5a-8e48-6e01c21377f3/trees/default/nodes?limit=3&offset=3"
  },
  "results": [
    {
      "id": "5add4375-f223-4201-88b9-8049e68416aa",
      "parentId": null,
      "type": "Root",
      "name": "Project",
      "description": "Project description",
      "barcode": null,
      "order": 0,
      "documentCount": 0,
      "areaDefined": false
    },
    {
      "id": "d14ce3a6-e61b-4ab0-a9be-5acf7b5366df",
      "parentId": "5add4375-f223-4201-88b9-8049e68416aa",
      "type": "Area",
      "name": "Area 1",
      "description": "An Area 1 node",
      "barcode": "ABC123",
      "order": 0,
      "documentCount": 2,
      "areaDefined": true
    },
    {
      "id": "8da1faf2-a72f-421b-89df-00d77e545faf",
      "parentId": "5add4375-f223-4201-88b9-8049e68416aa",
      "type": "Area",
      "name": "Area 2",
      "description": "An Area 2 node",
      "barcode": "DEF456",
      "order": 1,
      "documentCount": 3,
      "areaDefined": true
    }
  ]
}
Show Less
The response payload includes the location IDs in the results object.

Step 2: Find the Forms
Use the project ID (9ba6681e-1952-4d54-aac4-9de6d9858dd4) and the location IDs that you retrieved in the previous step to call GET forms, and use the locations filter to only retrieve forms that are associated with the specified locations.

request
curl "https://developer.api.autodesk.com/construction/forms/v1/projects/9ba6681e-1952-4d54-aac4-9de6d9858dd4/forms?locationIds=8da1faf2-a72f-421b-89df-00d77e545faf&locationIds=d14ce3a6-e61b-4ab0-a9be-5acf7b5366df" -X GET \
  -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT" \
  -H "Content-Type: application/vnd.api+json"
response
{
  "data": [
    {
      "status": "draft",
      "id": "932da979-e537-4530-b8aa-18607ac6db37",
      "projectId": "9ba6681e-1952-4d54-aac4-9de6d9858dd4",
      "formNum": 1,
      "formDate": "2020-11-20",
      "assigneeId": "USER123A",
      "locationId": "d14ce3a6-e61b-4ab0-a9be-5acf7b5366df",
      "updatedAt": "2020-11-20T16:14:27.615127+00:00",
      "createdBy": "USER123A",
      "notes": "Form notes",
      "description": "Form description",
      "formTemplate": {
        "status": "active",
        "id": "2f634a22-779d-4930-9f08-8391a41fea05",
        "projectId": "9ba6681e-1952-4d54-aac4-9de6d9858dd4",
        "name": "Daily Report",
        "templateType": "pg.template_type.daily_report"
      },
      "pdfValues": [],
      "pdfUrl": null,
      "weather": {
        "summaryKey": "clear",
        "precipitationAccumulation": 2.3,
        "precipitationAccumulationUnit": "in",
        "temperatureMin": 47.1,
        "temperatureMax": 65.1,
        "temperatureUnit": "Fahrenheit",
        "humidity": 0.2,
        "windSpeed": 12.5,
        "windGust": 34.6,
        "speedUnit": "mph",
        "windBearing": 18,
        "hourlyWeather": [
          {
            "id": 1234,
            "hour": "07:00:00",
            "temp": 54.12,
            "windSpeed": 14.2,
            "windBearing": 14,
            "humidity": 0.24,
            "fetchedAt": null,
            "createdAt": "2021-01-20T20:38:32+00:00",
            "updatedAt": "2021-01-20T20:38:32+00:00"
          }
        ]
      },
      "tabularValues": {
        "worklogEntries": [
          {
            "id": "cb95aceb-187a-3a8f-2e5f-502a555c03d5",
            "deleted": false,
            "trade": "Plumbers",
            "timespan": 21600000,
            "headcount": 4,
            "description": "change pipes"
          }
        ],
        "materialsEntries": [
          {
            "id": "2f7e534d-d084-594b-8aa6-147cb8fbc060",
            "deleted": false,
            "item": "Glue",
            "quantity": 3,
            "unit": "qt",
            "description": null
          }
        ],
        "equipmentEntries": [
          {
            "id": "84a32af6-b2b1-c3ae-c186-caef48fe4ffd",
            "deleted": false,
            "item": "Hammer",
            "timespan": 7200000,
            "quantity": 1,
            "description": null
          }
        ]
      },
      "customValues": [
        {
          "sectionLabel": "Observation",
          "itemLabel": "Masks / Face Protection",
          "valueName": "numberVal",
          "numberVal": 1,
          "notes": "Observed Masks and Face Protection"
        }
      ]
    }
  ],
  "pagination": {
    "offset": 0,
    "limit": 50,
    "totalResults": 1,
    "nextUrl": null
  }
}
Show Less
The response payload includes the form IDs (data.id) that are associated with the specified locations.

Note that in this example the endpoint only returned a single form (locationId=d14ce3a6-e61b-4ab0-a9be-5acf7b5366df) even though it filtered for two locations. This is because only one of the two locations is associated with a form.

Congratulations! You have retrieved forms associated with specific locations.

Documentation /Autodesk Construction Cloud APIs /How-to Guide
Retrieve Issues
This tutorial demonstrates how to retrieve information about a project’s issues, including details about their associated comments and attachments.

Note that we do not currently support document-related (pusphin) issues or linked documents.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with the data:read scope.
Verify that you have access to the relevant account and ACC project.
Find the relevant project ID for the project you want to retrieve the issues from by following the Retrieve a Project ID tutorial. In this example, assume the project ID is f6a1e3b5-abaa-4b01-b33a-5d55f36ba047.
Find Issue Information
Use the project ID (f6a1e3b5-abaa-4b01-b33a-5d55f36ba047) to retrieve the project’s issues, by calling GET issues.

Request
curl -v 'https://developer.api.autodesk.com/construction/issues/v1/projects/f6a1e3b5-abaa-4b01-b33a-5d55f36ba047/issues' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 10,
    "offset": 100,
    "totalResults": 25
  },
  "results": [
    {
      "id": "3570f222-6c54-4b01-90e6-e701749f0222",
      "containerId": "f6a1e3b5-abaa-4b01-b33a-5d55f36ba047",
      "deleted": false,
      "displayId": 7,
      "title": "Door missing a screw",
      "description": "The door is missing a screw, please fix this",
      "snapshotUrn": "",
      "issueTypeId": "8770f222-6c54-4e01-93e6-e701749f0222",
      "issueSubtypeId": "1370f222-6c54-3a01-93e6-e701749f0222",
      "status": "open",
      "assignedTo": "A3RGM375QTZ7",
      "assignedToType": "user",
      "dueDate": "2018-07-25",
      "startDate": "1982-06-01",
      "locationId": "35de6f24-39f5-4808-ba5f-6cbbe2a858e1",
      "locationDetails": "issue location details",
      "linkedDocuments": [
        {}
      ],
      "links": [
        {}
      ],
      "ownerId": "",
      "rootCauseId": "2370f222-6c54-3a01-93e6-f701772f0222",
      "officialResponse": {},
      "issueTemplateId": "",
      "permittedStatuses": [
        "open"
      ],
      "permittedAttributes": [
        "title"
      ],
      "published": true,
      "permittedActions": {},
      "commentCount": 3,
      "attachmentCount": "",
      "openedBy": "A3RGM375QTZ7",
      "openedAt": "2018-07-22T15:05:58.033Z",
      "closedBy": "A3RGM375QTZ7",
      "closedAt": "2018-07-22T15:05:58.033Z",
      "createdBy": "A3RGM375QTZ7",
      "createdAt": "2018-07-22T15:05:58.033Z",
      "updatedBy": "A3RGM375QTZ7",
      "updatedAt": "2018-07-22T15:05:58.033Z",
      "watchers": [
        "A3RGM375QTZ7"
      ],
      "customAttributes": [
        {
          "attributeDefinitionId": "2220f222-6c54-4b01-90e6-d701748f0888",
          "value": "368",
          "type": "numeric",
          "title": "Cost Impact ($)"
        }
      ]
    }
  ]
}
Show Less
The response payload includes the issue IDs (data.id).

Documentation /Autodesk Construction Cloud APIs /How-to Guide
Download Issue References
This tutorial demonstrates how to download references such as ACC photos that are associated with ACC issues. The steps include, finding the ID of the relevant issue, using the Relationships API to find the IDs of the references (such as photos) associated with the relevant issue, retreiving a signed-URL of the reference, and using the signed-URL to download the reference.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with the data:read scope.
Verify that you have access to the relevant account and ACC project.
Find the relevant project ID for the project you want to create an issue in by following the Retrieve a Project ID tutorial. In this example, assume the project ID is f6a1e3b5-abaa-4b01-b33a-5d55f36ba047.
Step 1: Find the Relevant Issue
Find the ID of the issue you want to download the reference from, by calling GET issues using the project ID (f6a1e3b5-abaa-4b01-b33a-5d55f36ba047).

Request
curl -v 'https://developer.api.autodesk.com/construction/issues/v1/projects/f6a1e3b5-abaa-4b01-b33a-5d55f36ba047/issues' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 10,
    "offset": 100,
    "totalResults": 25
  },
  "results": [
    {
      "id": "3570f222-6c54-4b01-90e6-e701749f0222",
      "containerId": "2220f222-6c54-4b01-90e6-d701748f0222",
      "deleted": false,
      "displayId": 7,
      "title": "Door missing a screw",
      "description": "The door is missing a screw, please fix this",
      "snapshotUrn": "",
      "issueTypeId": "8770f222-6c54-4e01-93e6-e701749f0222",
      "issueSubtypeId": "1370f222-6c54-3a01-93e6-e701749f0222",
      "status": "open",
      "assignedTo": "A3RGM375QTZ7",
      "assignedToType": "user",
      "dueDate": "2018-07-25",
      "startDate": "1982-06-01",
      "locationId": "35de6f24-39f5-4808-ba5f-6cbbe2a858e1",
      "locationDetails": "issue location details",
      "linkedDocuments": [
        {}
      ],
      "links": [
        {}
      ],
      "ownerId": "",
      "rootCauseId": "2370f222-6c54-3a01-93e6-f701772f0222",
      "officialResponse": {},
      "issueTemplateId": "",
      "permittedStatuses": [
        "open"
      ],
      "permittedAttributes": [
        "title"
      ],
      "published": true,
      "permittedActions": {},
      "commentCount": 3,
      "attachmentCount": "",
      "openedBy": "A3RGM375QTZ7",
      "openedAt": "2018-07-22T15:05:58.033Z",
      "closedBy": "A3RGM375QTZ7",
      "closedAt": "2018-07-22T15:05:58.033Z",
      "createdBy": "A3RGM375QTZ7",
      "createdAt": "2018-07-22T15:05:58.033Z",
      "updatedBy": "A3RGM375QTZ7",
      "updatedAt": "2018-07-22T15:05:58.033Z",
      "watchers": [
        "A3RGM375QTZ7"
      ],
      "customAttributes": [
        {
          "attributeDefinitionId": "2220f222-6c54-4b01-90e6-d701748f0888",
          "value": "368",
          "type": "numeric",
          "title": "Cost Impact ($)"
        }
      ]
    }
  ]
}
Show Less
Note the ID (results.[id]) (3570f222-6c54-4b01-90e6-e701749f0222) of the issue you want to download the reference from.

Step 2: Find the Photo IDs
Use the Relationships API to find the photos that are associated with the relevant issue. Call POST relationships using the project ID (f6a1e3b5-abaa-4b01-b33a-5d55f36ba047) and the issue ID (3570f222-6c54-4b01-90e6-e701749f0222).

In the request body you need to specify an issue type and an autodesk-bim360-issue domain.

Note that container ID in the relationships ID is equivalent to the project ID.

Request
curl -v 'https://developer.api.autodesk.com/bim360/relationship/v2/containers/f6a1e3b5-abaa-4b01-b33a-5d55f36ba047/relationships:intersect' \
     -X POST \
     -H 'Authorization: Bearer <token>' \
     -H 'Content-Type: application/json' \
     -d '[
           {
             "entities": [
               {
                 "id": "fddd7bcb-91fd-47ff-aacc-a74fdf4f2c1a",
                 "type": "issue",
                 "domain": "autodesk-bim360-issue"
                }
            ]
           }
         ]'
Show Less
Response (200)
 [

   {
 "page": {
   "syncToken": "eyJMYXN0TW9kaWZpZWQiOnsiRGF0ZVRpbWUiOiIyMDIyLTAzLTAxVDE0OjE3OjM0Ljc4NzAzNTBaIiwiT2Zmc2V0TWludXRlcyI6MH0sIk9wZXJhdGlvbiI6MiwiT3JpZ2luYWxQYXJhbWV0ZXJzIjp7Il9fdHlwZSI6IlN0b3JlSW50ZXJzZWN0UmVsYXRpb25zaGlwczojQXV0b2Rlc2suTnVjbGV1cy5TdG9yZS5SZWxhdGlvbnNoaXBzLk9wZXJhdGlvbnMiLCJDYWxsZXJUeXBlIjoxLCJDb250YWluZXJJZCI6ImExZTBhYzE2LTI2MDMtNGVkMS04YjY0LTdkMTZhNjRjN2QwMSIsIkVudGl0aWVzIjpbeyJBY3Rpdml0eSI6bnVsbCwiRG9tYWluIjoiYXV0b2Rlc2stYmltMzYwLWlzc3VlIiwiRW50aXR5SWQiOiIxNzkyY2YwOC02NmNjLTQyOGUtOTdmYS0zMGNjNDI2NmE1MzkiLCJFbnRpdHlUeXBlIjoiaXNzdWUifV0sIkluY2x1ZGVEZWxldGVkIjpmYWxzZSwiTW9kaWZpZWRBZnRlciI6bnVsbCwiT25seURlbGV0ZWQiOmZhbHNlLCJPeHlnZW5JZCI6IlZVTUpQNEVFOU5ZOCIsIldpdGhFbnRpdGllcyI6bnVsbH0sIlZlcnNpb25OdW1iZXIiOjF9"
 },
 "relationships": [
   {
     "permission": null,
     "id": "b8f676fb-e39b-4557-b10f-f970030b6e41",
     "createdOn": "2022-03-01T14:17:34.781856+00:00",
     "isReadOnly": false,
     "isService": true,
     "isDeleted": false,
     "entities": [
       {
         "createdOn": "2022-01-26T15:17:41.772891+00:00",
         "domain": "autodesk-construction-photo",
         "type": "photo",
         "id": "5439bfb7-8006-4388-a454-f02560f99566"
       },
       {
         "createdOn": "2022-03-01T14:17:34.774043+00:00",
         "domain": "autodesk-bim360-issue",
         "type": "issue",
         "id": "1792cf08-66cc-428e-97fa-30cc4266a539"
       }
     ]
   }
 ]
}
Show Less
]

Note the photo ID (relationships.[entities.[id]]) (5439bfb7-8006-4388-a454-f02560f99566)

Step 3: Generate a Signed URL
Use the Photos API to generate a signed URL, which you can use to download the photo directly from S3.

Call GET photos using the project ID (f6a1e3b5-abaa-4b01-b33a-5d55f36ba047) and photo ID (5439bfb7-8006-4388-a454-f02560f99566). To generate the signed URL you need add the include query string parameter (include=signedUrls).

You need to repeat this step for each photo.

Request
curl -v 'https://developer.api.autodesk.com/construction/photos/v1/projects/f6a1e3b5-abaa-4b01-b33a-5d55f36ba047/photos/5439bfb7-8006-4388-a454-f02560f99566?include=signedUrls' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "createdAt": "2021-03-14T10:20:33",
  "createdBy": "PER8KQPK2JRT",
  "deletedAt": "2021-03-19T11:50:33",
  "deletedBy": "PER8KQPK2JRT",
  "description": "The left side of the office",
  "id": "5439bfb7-8006-4388-a454-f02560f99566",
  "isPublic": false,
  "latitude": 37.757497,
  "locked": false,
  "longitude": -122.42115,
  "mediaType": "NORMAL",
  "projectId": "5439bfb7-8006-4388-a454-f02560f99566",
  "signedUrls": {
    "fileUrl": "https://s3.amazonaws.com/com.autodesk.oss-persistent/f0/7b/66/4df1b73d0cc643e6179b85eae7d8d529d2/ce8edd30-ef28-467c-8d99-7d7051097ee0?response-content-disposition=attachment%3B%20filename%3D%22c35b8b28-859e-4256-a3bc-41772a673260.jpg%22&response-content-type=image%2Fjpeg&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEKP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIQCOKZyru7bEOWhRlJOiFZUwLwGSFSWPO5VknX%2BIisldAwIgWN6g5zYxXLOzdiZgR4sYuyY4qr1k1SAQOTOCI7EOmKIqvQMI3P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw5OTM3ODk5OTIwNjMiDK0wr6QcJBV%2BrqLz7iqRA55WGaeF1IZVyH5XzR%2FyR72VqyCRIEwm9D3Pt%2BTOxtaNa519ldQcvjYptWrlwnrgr1T9c3jxtEXxHZveX3XwgaSQq7JyHACBAMVwkKABwczEzPOryCvIJBWjgr2ABoYGr0dDCFdh9IjdoDrOrXDDesn4I5GamK%2BdNzXBR1MJH3ocmoZXxrmaJGigr62ShQ3q7AoqMgIX55XH8DnYMP4k9OlGGJsL7P80OnvOXfNLFl9EVJp5jnp%2BT1eO3FezRxc%2FqkeTG7t6QHh87P4cJKzWV9pW3AQoYvBKyQ5uJn5WA8%2FFg%2BhzYalr5Y%2B4%2FneB0xfn7WS2I%2FvjIo6rOkIqx7K3Ty1p1kuZ6e64%2BlEXx8mYHO2NOYobbSf%2Fx%2B7FU1rhZqvqUGB%2BRoMXFI%2FIkaxe%2B%2Ba6sZYV6Dm6bcim835asw%2B48vkt3XLZ6kBNqOJMdqvIBp%2F7opV9Bc4%2BMkhPc6wT%2BwAoQ0jHGuNZiLh%2BsxcB8EtwziI18v5LFw6WmffTQD3oc8WTb9xUZmoQ8qDq5z%2FY4%2BY2EAq6MNaP7oIGOusBXz4xrUPPH0cr5UO912gp6aysXFnqxu55it8zqPwiGI2Xe0RlaMTAMh1jwDZ4LZD4N2NERk%2F%2BlR1KaRk2Jvo34HIXVnUqNWlYAR3TyV2intl8wwJWlgKQH6DI%2BzwOJ27kDToULG5TQpQk6xAQaToplmERCien7Pi8vlb0JNBCzkoKNh40Z1wPxcS%2BitdU0IkD0n39bvWy5uG0hoUuifHr53vaf7eqFRSdrd%2B%2BYuJ00yT%2FtWS6FLpLKCSgZw8GKoAq3PpfPggmg99bAju7H%2FD8xfVgBPhb91tEGCCdyub4jDtj6euoUFXK%2FiMIVg%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20210324T193346Z&X-Amz-SignedHeaders=host&X-Amz-Expires=60&X-Amz-Credential=ASIA6OYT73R75HNE4VUO%2F20210324%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=e694954290d485482c6334b39b591c87e4a16ba2425f05da1dc25faf47afba2d",
    "thumbnailUrl": "https://s3.amazonaws.com/com.autodesk.oss-opsstaging-persistent/81/b8/3d/e2855b46af2060d595ce31923310079c4b/ce8edd30-ef28-467c-8d99-7d7051097ee0?response-content-disposition=attachment%3B%20filename%3D%22c35b8b28-859e-4256-a3bc-41772a673260_t.jpg%22&response-content-type=image%2Fjpeg&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEKP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIQCOKZyru7bEOWhRlJOiFZUwLwGSFSWPO5VknX%2BIisldAwIgWN6g5zYxXLOzdiZgR4sYuyY4qr1k1SAQOTOCI7EOmKIqvQMI3P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw5OTM3ODk5OTIwNjMiDK0wr6QcJBV%2BrqLz7iqRA55WGaeF1IZVyH5XzR%2FyR72VqyCRIEwm9D3Pt%2BTOxtaNa519ldQcvjYptWrlwnrgr1T9c3jxtEXxHZveX3XwgaSQq7JyHACBAMVwkKABwczEzPOryCvIJBWjgr2ABoYGr0dDCFdh9IjdoDrOrXDDesn4I5GamK%2BdNzXBR1MJH3ocmoZXxrmaJGigr62ShQ3q7AoqMgIX55XH8DnYMP4k9OlGGJsL7P80OnvOXfNLFl9EVJp5jnp%2BT1eO3FezRxc%2FqkeTG7t6QHh87P4cJKzWV9pW3AQoYvBKyQ5uJn5WA8%2FFg%2BhzYalr5Y%2B4%2FneB0xfn7WS2I%2FvjIo6rOkIqx7K3Ty1p1kuZ6e64%2BlEXx8mYHO2NOYobbSf%2Fx%2B7FU1rhZqvqUGB%2BRoMXFI%2FIkaxe%2B%2Ba6sZYV6Dm6bcim835asw%2B48vkt3XLZ6kBNqOJMdqvIBp%2F7opV9Bc4%2BMkhPc6wT%2BwAoQ0jHGuNZiLh%2BsxcB8EtwziI18v5LFw6WmffTQD3oc8WTb9xUZmoQ8qDq5z%2FY4%2BY2EAq6MNaP7oIGOusBXz4xrUPPH0cr5UO912gp6aysXFnqxu55it8zqPwiGI2Xe0RlaMTAMh1jwDZ4LZD4N2NERk%2F%2BlR1KaRk2Jvo34HIXVnUqNWlYAR3TyV2intl8wwJWlgKQH6DI%2BzwOJ27kDToULG5TQpQk6xAQaToplmERCien7Pi8vlb0JNBCzkoKNh40Z1wPxcS%2BitdU0IkD0n39bvWy5uG0hoUuifHr53vaf7eqFRSdrd%2B%2BYuJ00yT%2FtWS6FLpLKCSgZw8GKoAq3PpfPggmg99bAju7H%2FD8xfVgBPhb91tEGCCdyub4jDtj6euoUFXK%2FiMIVg%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20210324T193346Z&X-Amz-SignedHeaders=host&X-Amz-Expires=60&X-Amz-Credential=ASIA6OYT73R75HNE4VUO%2F20210324%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=fac56130302305057c9ae301503860edb2d296c43dcfb5a59ebf3744f5126baa"
  },
  "size": 11359,
  "takenAt": "2021-03-13T18:15:00",
  "title": "Office Dry Wall",
  "type": "FIELD-REPORT",
  "updatedAt": "2021-03-14T11:20:33",
  "updatedBy": "PER8KQPK2JRT",
  "urls": {
    "fileUrl": "https://developer.api.autodesk.com/construction/photos/assets/ce8edd30-ef28-467c-8d99-7d7051097ee0/c35b8b28-859e-4256-a3bc-41772a673260.jpg\"",
    "thumbnailUrl": "https://developer.api.autodesk.com/construction/photos/assets/ce8edd30-ef28-467c-8d99-7d7051097ee0/c35b8b28-859e-4256-a3bc-41772a673260_t.jpg\""
  },
  "userCreatedAt": "2021-03-13T18:20:33"
}
Show Less
Note the signed URL of the photo (signedUrl.fileUrl).

The signed URL expires after a short amount of time. See the X-Amz-Expires- value in the signed URL for the length of time. If the time expires you need to call GET photos again to get a new download link.

Step 4: Download the Photo
To download the photo from the signed URL, use a GET method and the signedUrl.fileUrl attribute as the URI.

Note that you should not use a bearer token with this call.

Request
curl -X GET "https://s3.amazonaws.com/com.autodesk.oss-persistent/f0/7b/66/4df1b73d0cc643e6179b85eae7d8d529d2/ce8edd30-ef28-467c-8d99-7d7051097ee0?response-content-disposition=attachment%3B%20filename%3D%22c35b8b28-859e-4256-a3bc-41772a673260.jpg%22&response-content-type=image%2Fjpeg&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEKP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIQCOKZyru7bEOWhRlJOiFZUwLwGSFSWPO5VknX%2BIisldAwIgWN6g5zYxXLOzdiZgR4sYuyY4qr1k1SAQOTOCI7EOmKIqvQMI3P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw5OTM3ODk5OTIwNjMiDK0wr6QcJBV%2BrqLz7iqRA55WGaeF1IZVyH5XzR%2FyR72VqyCRIEwm9D3Pt%2BTOxtaNa519ldQcvjYptWrlwnrgr1T9c3jxtEXxHZveX3XwgaSQq7JyHACBAMVwkKABwczEzPOryCvIJBWjgr2ABoYGr0dDCFdh9IjdoDrOrXDDesn4I5GamK%2BdNzXBR1MJH3ocmoZXxrmaJGigr62ShQ3q7AoqMgIX55XH8DnYMP4k9OlGGJsL7P80OnvOXfNLFl9EVJp5jnp%2BT1eO3FezRxc%2FqkeTG7t6QHh87P4cJKzWV9pW3AQoYvBKyQ5uJn5WA8%2FFg%2BhzYalr5Y%2B4%2FneB0xfn7WS2I%2FvjIo6rOkIqx7K3Ty1p1kuZ6e64%2BlEXx8mYHO2NOYobbSf%2Fx%2B7FU1rhZqvqUGB%2BRoMXFI%2FIkaxe%2B%2Ba6sZYV6Dm6bcim835asw%2B48vkt3XLZ6kBNqOJMdqvIBp%2F7opV9Bc4%2BMkhPc6wT%2BwAoQ0jHGuNZiLh%2BsxcB8EtwziI18v5LFw6WmffTQD3oc8WTb9xUZmoQ8qDq5z%2FY4%2BY2EAq6MNaP7oIGOusBXz4xrUPPH0cr5UO912gp6aysXFnqxu55it8zqPwiGI2Xe0RlaMTAMh1jwDZ4LZD4N2NERk%2F%2BlR1KaRk2Jvo34HIXVnUqNWlYAR3TyV2intl8wwJWlgKQH6DI%2BzwOJ27kDToULG5TQpQk6xAQaToplmERCien7Pi8vlb0JNBCzkoKNh40Z1wPxcS%2BitdU0IkD0n39bvWy5uG0hoUuifHr53vaf7eqFRSdrd%2B%2BYuJ00yT%2FtWS6FLpLKCSgZw8GKoAq3PpfPggmg99bAju7H%2FD8xfVgBPhb91tEGCCdyub4jDtj6euoUFXK%2FiMIVg%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20210324T193346Z&X-Amz-SignedHeaders=host&X-Amz-Expires=60&X-Amz-Credential=ASIA6OYT73R75HNE4VUO%2F20210324%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=e694954290d485482c6334b39b591c87e4a16ba2425f05da1dc25faf47afba2d"
Congratulations! You have downloaded a photo associated with an ACC issue.

Documentation /Autodesk Construction Cloud APIs /How-to Guide
Retrieve Issue Attachments
This tutorial demonstrates how to retrieve information about attachments associated with issues in an Autodesk Construction Cloud (ACC) project. The steps include finding issues in a project and retrieving attachment information for a specific issue.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with the data:read scope.
Verify that you have access to the relevant account and ACC project.
Find the relevant project ID for the project containing issues with attachments by following the Retrieve an Account ID and Project ID tutorial. In this example, assume the project ID is b8c45fe1-2ab3-4b71-8563-d9f9c5c2a7e5.
Step 1: Find Issues in Project
Find issues in your project by calling GET issues using the project ID (b8c45fe1-2ab3-4b71-8563-d9f9c5c2a7e5).

Request
curl -v 'https://developer.api.autodesk.com/construction/issues/v1/projects/b8c45fe1-2ab3-4b71-8563-d9f9c5c2a7e5/issues' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 100,
    "offset": 0,
    "totalResults": 2
  },
  "results": [
    {
      "id": "d4f9c2e1-3b8a-4c7d-9e2f-1a5b8c9d0e3f",
      "containerId": "b8c45fe1-2ab3-4b71-8563-d9f9c5c2a7e5",
      "displayId": 101,
      "title": "Structural beam alignment issue",
      "description": "The structural beam at grid line A-3 appears to be misaligned with the architectural drawings.",
      "status": "open",
      "issueType": "design",
      "issueSubType": "clash",
      "assignedTo": "A3RGM375QTZ7",
      "assignedToType": "user",
      "createdBy": "MFEGJ9W5GGQL",
      "createdAt": "2024-11-09T14:30:00.000Z",
      "updatedBy": "MFEGJ9W5GGQL",
      "updatedAt": "2024-11-09T15:45:30.000Z",
      "dueDate": "2024-11-20T17:00:00.000Z",
      "locationDetails": "Building A, Level 2, Grid A-3",
      "attachmentCount": 3,
      "permittedActions": ["view", "edit", "add_comment", "add_attachment"]
    },
    {
      "id": "e8a2b5f7-4d6c-4e9a-b1c3-7f2e9a8b4d6c",
      "containerId": "b8c45fe1-2ab3-4b71-8563-d9f9c5c2a7e5",
      "displayId": 102,
      "title": "HVAC duct clearance concern",
      "description": "Insufficient clearance for HVAC duct installation in mechanical room.",
      "status": "in_progress",
      "issueType": "quality",
      "issueSubType": "installation",
      "assignedTo": "B5THJ486RXW9",
      "assignedToType": "user",
      "createdBy": "A3RGM375QTZ7",
      "createdAt": "2024-11-08T09:15:00.000Z",
      "updatedBy": "B5THJ486RXW9",
      "updatedAt": "2024-11-09T10:20:15.000Z",
      "dueDate": "2024-11-18T17:00:00.000Z",
      "locationDetails": "Building B, Mechanical Room 1",
      "attachmentCount": 1,
      "permittedActions": ["view", "edit", "add_comment", "add_attachment"]
    }
  ]
}
Show Less
Note the ID of the issue for which you want to retrieve attachments. In this example, we’ll use the first issue (d4f9c2e1-3b8a-4c7d-9e2f-1a5b8c9d0e3f) which has 3 attachments (attachmentCount: 3).

Step 2: Retrieve Attachments for a Specific Issue
Retrieve information about all attachments associated with a specific issue by calling GET attachments using the project ID (b8c45fe1-2ab3-4b71-8563-d9f9c5c2a7e5) and the issue ID (d4f9c2e1-3b8a-4c7d-9e2f-1a5b8c9d0e3f).

Request
curl -v 'https://developer.api.autodesk.com/construction/issues/v1/projects/b8c45fe1-2ab3-4b71-8563-d9f9c5c2a7e5/attachments/d4f9c2e1-3b8a-4c7d-9e2f-1a5b8c9d0e3f/items' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "attachments": [
    {
      "attachmentId": "a9d330bc-411f-4aaf-874a-9844cc002d00",
      "displayName": "Structural Plan - Level 2.pdf",
      "fileName": "a9d330bc-411f-4aaf-874a-9844cc002d00.pdf",
      "attachmentType": "issue-attachment",
      "storageUrn": "urn:adsk.objects:os.object:issues-b8c45fe1-2ab3-4b71-8563-d9f9c5c2a7e5/a9d330bc-411f-4aaf-874a-9844cc002d00.pdf",
      "fileSize": 4729968,
      "fileType": "pdf",
      "domainEntityId": "d4f9c2e1-3b8a-4c7d-9e2f-1a5b8c9d0e3f",
      "lineageUrn": "urn:adsk.wipprod:dm.lineage:AeYgDtcTSuqYoyMweWFhhQ",
      "version": 1,
      "versionUrn": "urn:adsk.wipprod:fs.file:vf.1HROnsnfQgq4N0b-nUoGge?version=1",
      "tipVersionUrn": "urn:adsk.wipprod:fs.file:vf.1HROnsnfQgq4N0b-nUoGge?version=1",
      "createdBy": "MFEGJ9W5GGQL",
      "createdOn": "2024-11-09T14:32:15.000Z",
      "deletedBy": null,
      "deletedOn": null,
      "isDeleted": false
    },
    {
      "attachmentId": "f2e8c4a6-7b9d-4e1f-8c3a-5d7f9b2e6c8a",
      "displayName": "Photo - Beam Alignment Issue.jpg",
      "fileName": "f2e8c4a6-7b9d-4e1f-8c3a-5d7f9b2e6c8a.jpg",
      "attachmentType": "issue-attachment",
      "storageUrn": "urn:adsk.objects:os.object:issues-b8c45fe1-2ab3-4b71-8563-d9f9c5c2a7e5/f2e8c4a6-7b9d-4e1f-8c3a-5d7f9b2e6c8a.jpg",
      "fileSize": 2458746,
      "fileType": "jpg",
      "domainEntityId": "d4f9c2e1-3b8a-4c7d-9e2f-1a5b8c9d0e3f",
      "lineageUrn": "urn:adsk.wipprod:dm.lineage:BfZhEudTSvqYpyNxeGIjjR",
      "version": 1,
      "versionUrn": "urn:adsk.wipprod:fs.file:vf.2ISPotngRhq5O1c-oVpHhf?version=1",
      "tipVersionUrn": "urn:adsk.wipprod:fs.file:vf.2ISPotngRhq5O1c-oVpHhf?version=1",
      "createdBy": "MFEGJ9W5GGQL",
      "createdOn": "2024-11-09T14:45:22.000Z",
      "deletedBy": null,
      "deletedOn": null,
      "isDeleted": false
    },
    {
      "attachmentId": "c7b5e9f3-2a4d-4f8c-9e1b-6d3a8f5c2e7b",
      "displayName": "Specification Sheet - Steel Beam.pdf",
      "fileName": "c7b5e9f3-2a4d-4f8c-9e1b-6d3a8f5c2e7b.pdf",
      "attachmentType": "issue-attachment",
      "storageUrn": "urn:adsk.objects:os.object:issues-b8c45fe1-2ab3-4b71-8563-d9f9c5c2a7e5/c7b5e9f3-2a4d-4f8c-9e1b-6d3a8f5c2e7b.pdf",
      "fileSize": 856432,
      "fileType": "pdf",
      "domainEntityId": "d4f9c2e1-3b8a-4c7d-9e2f-1a5b8c9d0e3f",
      "lineageUrn": "urn:adsk.wipprod:dm.lineage:CgAiGvfUSvrZpzOyfHJkkS",
      "version": 1,
      "versionUrn": "urn:adsk.wipprod:fs.file:vf.3JTQpuohSiq6P2d-pWqIig?version=1",
      "tipVersionUrn": "urn:adsk.wipprod:fs.file:vf.3JTQpuohSiq6P2d-pWqIig?version=1",
      "createdBy": "A3RGM375QTZ7",
      "createdOn": "2024-11-09T15:10:45.000Z",
      "deletedBy": null,
      "deletedOn": null,
      "isDeleted": false
    }
  ]
}
Show Less
Congratulations! You have successfully retrieved attachment information for an issue in Autodesk Construction Cloud. You can use this information to display attachment details, check file sizes, or prepare for downloading specific attachments.

Documentation /Autodesk Construction Cloud APIs /How-to Guide
Download Issue Attachments
This tutorial demonstrates how to download attachments that were added to issues in ACC Issues. The steps include finding the issue containing the attachment you want to download, retrieving attachment information, generating a signed URL for the attachment, and using the signed URL to download the attachment.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with the data:read scope.
Verify that you have access to the relevant account and ACC project.
Find the relevant project ID for the project you want to download an attachment from. See the Retrieve a Project ID tutorial for more details. In this example, assume the project ID is b8c45fe1-2ab3-4b71-8563-d9f9c5c2a7e5.
Step 1: Find the Issue ID
Find the ID of the issue that contains the attachment you want to download by calling GET issues using the project ID (b8c45fe1-2ab3-4b71-8563-d9f9c5c2a7e5).

Request
curl -v 'https://developer.api.autodesk.com/construction/issues/v1/projects/b8c45fe1-2ab3-4b71-8563-d9f9c5c2a7e5/issues' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 100,
    "offset": 0,
    "totalResults": 2
  },
  "results": [
    {
      "id": "d4f9c2e1-3b8a-4c7d-9e2f-1a5b8c9d0e3f",
      "containerId": "b8c45fe1-2ab3-4b71-8563-d9f9c5c2a7e5",
      "displayId": 101,
      "title": "Structural beam alignment issue",
      "description": "The structural beam at grid line A-3 appears to be misaligned with the architectural drawings.",
      "status": "open",
      "issueType": "design",
      "issueSubType": "clash",
      "assignedTo": "A3RGM375QTZ7",
      "assignedToType": "user",
      "createdBy": "MFEGJ9W5GGQL",
      "createdAt": "2024-11-09T14:30:00.000Z",
      "updatedBy": "MFEGJ9W5GGQL",
      "updatedAt": "2024-11-09T15:45:30.000Z",
      "dueDate": "2024-11-20T17:00:00.000Z",
      "locationDetails": "Building A, Level 2, Grid A-3",
      "attachmentCount": 3,
      "permittedActions": ["view", "edit", "add_comment", "add_attachment"]
    },
    {
      "id": "e8a2b5f7-4d6c-4e9a-b1c3-7f2e9a8b4d6c",
      "containerId": "b8c45fe1-2ab3-4b71-8563-d9f9c5c2a7e5",
      "displayId": 102,
      "title": "HVAC duct clearance concern",
      "description": "Insufficient clearance for HVAC duct installation in mechanical room.",
      "status": "in_progress",
      "issueType": "quality",
      "issueSubType": "installation",
      "assignedTo": "B5THJ486RXW9",
      "assignedToType": "user",
      "createdBy": "A3RGM375QTZ7",
      "createdAt": "2024-11-08T09:15:00.000Z",
      "updatedBy": "B5THJ486RXW9",
      "updatedAt": "2024-11-09T10:20:15.000Z",
      "dueDate": "2024-11-18T17:00:00.000Z",
      "locationDetails": "Building B, Mechanical Room 1",
      "attachmentCount": 1,
      "permittedActions": ["view", "edit", "add_comment", "add_attachment"]
    }
  ]
}
Show Less
Note the ID of the issue that contains the attachment you want to download (results.id). In this example, we’ll use the first issue (d4f9c2e1-3b8a-4c7d-9e2f-1a5b8c9d0e3f) which has 3 attachments (attachmentCount: 3).

Step 2: Find the Attachment Information
Find the specific attachment you want to download by calling GET attachments using the project ID (b8c45fe1-2ab3-4b71-8563-d9f9c5c2a7e5) and the issue ID (d4f9c2e1-3b8a-4c7d-9e2f-1a5b8c9d0e3f).

Request
curl -v 'https://developer.api.autodesk.com/construction/issues/v1/projects/b8c45fe1-2ab3-4b71-8563-d9f9c5c2a7e5/attachments/d4f9c2e1-3b8a-4c7d-9e2f-1a5b8c9d0e3f/items' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "attachments": [
    {
      "attachmentId": "a9d330bc-411f-4aaf-874a-9844cc002d00",
      "displayName": "Structural Plan - Level 2.pdf",
      "fileName": "a9d330bc-411f-4aaf-874a-9844cc002d00.pdf",
      "attachmentType": "issue-attachment",
      "storageUrn": "urn:adsk.objects:os.object:wip.dm.prod/2a6d61f2-49df-4d7b.jpg",
      "fileSize": 4729968,
      "fileType": "pdf",
      "domainEntityId": "d4f9c2e1-3b8a-4c7d-9e2f-1a5b8c9d0e3f",
      "lineageUrn": "urn:adsk.wipprod:dm.lineage:AeYgDtcTSuqYoyMweWFhhQ",
      "version": 1,
      "versionUrn": "urn:adsk.wipprod:fs.file:vf.1HROnsnfQgq4N0b-nUoGge?version=1",
      "tipVersionUrn": "urn:adsk.wipprod:fs.file:vf.1HROnsnfQgq4N0b-nUoGge?version=1",
      "createdBy": "MFEGJ9W5GGQL",
      "createdOn": "2024-11-09T14:32:15.000Z",
      "deletedBy": null,
      "deletedOn": null,
      "isDeleted": false
    },
    {
      "attachmentId": "f2e8c4a6-7b9d-4e1f-8c3a-5d7f9b2e6c8a",
      "displayName": "Photo - Beam Alignment Issue.jpg",
      "fileName": "f2e8c4a6-7b9d-4e1f-8c3a-5d7f9b2e6c8a.jpg",
      "attachmentType": "issue-attachment",
      "storageUrn": "urn:adsk.objects:os.object:wip.dm.prod/2a6d61f2-49df-4d7b.jpg",
      "fileSize": 2458746,
      "fileType": "jpg",
      "domainEntityId": "d4f9c2e1-3b8a-4c7d-9e2f-1a5b8c9d0e3f",
      "lineageUrn": "urn:adsk.wipprod:dm.lineage:BfZhEudTSvqYpyNxeGIjjR",
      "version": 1,
      "versionUrn": "urn:adsk.wipprod:fs.file:vf.2ISPotngRhq5O1c-oVpHhf?version=1",
      "tipVersionUrn": "urn:adsk.wipprod:fs.file:vf.2ISPotngRhq5O1c-oVpHhf?version=1",
      "createdBy": "MFEGJ9W5GGQL",
      "createdOn": "2024-11-09T14:45:22.000Z",
      "deletedBy": null,
      "deletedOn": null,
      "isDeleted": false
    },
    {
      "attachmentId": "c7b5e9f3-2a4d-4f8c-9e1b-6d3a8f5c2e7b",
      "displayName": "Specification Sheet - Steel Beam.pdf",
      "fileName": "c7b5e9f3-2a4d-4f8c-9e1b-6d3a8f5c2e7b.pdf",
      "attachmentType": "issue-attachment",
      "storageUrn": "urn:adsk.objects:os.object:wip.dm.prod/1d6d61f2-21ut-3k5h.jpg",
      "fileSize": 856432,
      "fileType": "pdf",
      "domainEntityId": "d4f9c2e1-3b8a-4c7d-9e2f-1a5b8c9d0e3f",
      "lineageUrn": "urn:adsk.wipprod:dm.lineage:CgAiGvfUSvrZpzOyfHJkkS",
      "version": 1,
      "versionUrn": "urn:adsk.wipprod:fs.file:vf.3JTQpuohSiq6P2d-pWqIig?version=1",
      "tipVersionUrn": "urn:adsk.wipprod:fs.file:vf.3JTQpuohSiq6P2d-pWqIig?version=1",
      "createdBy": "A3RGM375QTZ7",
      "createdOn": "2024-11-09T15:10:45.000Z",
      "deletedBy": null,
      "deletedOn": null,
      "isDeleted": false
    }
  ]
}
Show Less
Find the attachment you want to download (attachments.displayName). In this example, we’ll download the “Photo - Beam Alignment Issue.jpg” file. Note the corresponding storage URN (attachments.storageUrn) - urn:adsk.objects:os.object:wip.dm.prod/2a6d61f2-49df-4d7b.jpg.

The storage URN follows the format: urn:adsk.objects:os.object:<bucket_key>/<object_key>

From the storage URN, extract: - Bucket Key: wip.dm.prod - Object Key: 2a6d61f2-49df-4d7b.jpg

Step 3: Generate a Signed S3 URL
Use the bucket key (wip.dm.prod) and object key (2a6d61f2-49df-4d7b.jpg) to call GET signeds3download to generate a signed URL for the storage object, which you can use to download the file directly from S3.

You need to repeat this step for each attachment.

Request
curl -X GET 'https://developer.api.autodesk.com/oss/v2/buckets/wip.dm.prod/objects/2a6d61f2-49df-4d7b.jpg/signeds3download' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "status": "complete",
  "url": "https://cdn.us.oss.api.autodesk.com/com.autodesk.oss-persistent/us-east-1/f2/e8/c4/a67b9d4e1f8c3a5d7f9b2e6c8a/issues-b8c45fe1-2ab3-4b71-8563-d9f9c5c2a7e5?response-content-type=image%2Fjpeg&response-content-disposition=attachment%3B+filename%3D%22Photo+-+Beam+Alignment+Issue.jpg%22&Expires=1699540803&Signature=xKmD2HsP9Lk4aRG2HAhOCKYl0xtqsuujMJ~VKSXm1vBa-OxS4lPQBSlTx5bswpLBe1W6Rz94eIZW2sPN-v6Mzz~JyXNZ-V9Z7zlBoE1VoQhspLioC225hxq6ZmDSU5QnZXuNDV4ih~p1n3xacYvUvQWX-ONAGVUgQvZ253Svw~qx-pO4j-Yh4kVRmzDZqQut1xOI5ZGH6JFGhXLSzkgbYcfYx6fvCxnvYUJrgAcqncIwGVewI3uC0I84Fzrj8nXE8ojuojqJP0pNlxkfBe~2LfjjzqKDKaNvfC2Grt12j9QgC~cN7nQCRcVUhExpoV1VVB5x3AkVTJ-q5NoedvsfO__&Key-Pair-Id=APKAI5JGPYQ5LGB7QA",
  "params": {
    "content-type": "image/jpeg",
    "content-disposition": "attachment; filename=\"Photo - Beam Alignment Issue.jpg\""
  },
  "size": 2458746,
  "sha1": "f2e8c4a67b9d4e1f8c3a5d7f9b2e6c8a9c1d3e5f"
}
Show Less
Note the signed URL (url) and file information: - URL: Use this to download the file - Content-Type: image/jpeg indicates this is a JPEG image - Size: 2458746 bytes (approximately 2.5 MB) - SHA1: Hash for file integrity verification

Step 4: Download the File
To download the file from the signed URL, use a GET method with the url attribute as the URI. You can save the file to your local system with the desired filename.

Important Notes: - Do not include a bearer token with this request - The signed URL expires after a short amount of time (usually 15 minutes). If the time expires you need to call GET signeds3download again to get a new download link.

Request
curl -X GET "https://cdn.us.oss.api.autodesk.com/com.autodesk.oss-persistent/us-east-1/f2/e8/c4/a67b9d4e1f8c3a5d7f9b2e6c8a/issues-b8c45fe1-2ab3-4b71-8563-d9f9c5c2a7e5?response-content-type=image%2Fjpeg&response-content-disposition=attachment%3B+filename%3D%22Photo+-+Beam+Alignment+Issue.jpg%22&Expires=1699540803&Signature=xKmD2HsP9Lk4aRG2HAhOCKYl0xtqsuujMJ~VKSXm1vBa-OxS4lPQBSlTx5bswpLBe1W6Rz94eIZW2sPN-v6Mzz~JyXNZ-V9Z7zlBoE1VoQhspLioC225hxq6ZmDSU5QnZXuNDV4ih~p1n3xacYvUvQWX-ONAGVUgQvZ253Svw~qx-pO4j-Yh4kVRmzDZqQut1xOI5ZGH6JFGhXLSzkgbYcfYx6fvCxnvYUJrgAcqncIwGVewI3uC0I84Fzrj8nXE8ojuojqJP0pNlxkfBe~2LfjjzqKDKaNvfC2Grt12j9QgC~cN7nQCRcVUhExpoV1VVB5x3AkVTJ-q5NoedvsfO__&Key-Pair-Id=APKAI5JGPYQ5LGB7QA" \
  --output "Photo - Beam Alignment Issue.jpg"
Response
The file will be downloaded and saved to your current directory with the specified filename. The HTTP response will be 200 OK with the file content in the response body.

Congratulations! You have successfully downloaded an attachment from an ACC issue. The file is now available on your local system for viewing, sharing, or further processing.

Documentation /Autodesk Construction Cloud APIs /How-to Guide
Retrieve Available Members Roles and Companies
This tutorial demonstrates how to determine the members of a project. This is important for users with Create for my company or Create for other companies permissions, who can only assign issues to members of the project.

In addition, the tutorial shows how to verify the company that was assigned to each user within the project. This information is important when the person assigning an issue has Create for my company permissions or when adding or removing a watcher who has Create for my company permissions. This is because an assigner with Create for my company permissions can only assign an issue to someone who is a member of the same company.

This workflow uses the Data Connector API to extract project user and user company data in CSV files.

Note that this workflow is a temporary method for determining permissions, and we will be releasing endpoints that directly retrieve project users by companies in the near future.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with the data:read scope.
Verify that you have project admin or executive overview permissions.
Verify that you have access to the relevant account and ACC project.
Find the relevant project ID for the project you want to retrieve users for by following the Retrieve an Account ID and Project ID tutorial. In this example, assume the account ID is g5s4e3b5-vbta-6b02-d23a-5d55f36ba876, and the project ID is f6a1e3b5-abaa-4b01-b33a-5d55f36ba047.
Step 1: Submit a Data Request
Submit a data request by calling POST requests using the project ID (f6a1e3b5-abaa-4b01-b33a-5d55f36ba047) to retrieve the data about the project including the members of the project and the companies associated with the users. Specify the admin service group to get information about users and companies.

In this tutorial we will use a callback URL to retrieve the data. For details about the workflow for polling the data see the Data Connector tutorials.

Note that the data extraction process can take time depending on the amount of data that you are retrieving.

We recommend that you set up the workflow to extract data once a day (DAY) so you can update your database every day. For more details about different data extraction interval options, see POST requests. Note that the user needs to have project admin or executive overview permissions.

Request
curl --location --request POST 'https://developer.api.autodesk.com/data-connector/v1/accounts/g5s4e3b5-vbta-6b02-d23a-5d55f36ba876/requests' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
  --header 'Content-Type: application/json' \
  --data-raw '{
      "description": "Issues Daily Extract",
      "scheduleInterval": "DAY",
      "effectiveFrom": "2022-09-08T13:54:05.332Z",
      "effectiveTo": "2023-11-19T16:00:00Z",
      "reoccuringInterval": 1,
      "serviceGroups": ["admin"],
      "projectId": "78246834-79c9-4271-b584-7252a5456f72",
      "callbackUrl": "<CALLBACK_URL>"
  }'
Show Less
Response
{
  "id": "6c2ceb8d-792b-4439-b6b1-def3e2c7b4f2",
  "description": "Issues Daily Extract",
  "isActive": true,
  "accountId": "g5s4e3b5-vbta-6b02-d23a-5d55f36ba876",
  "projectId": "78246834-79c9-4271-b584-7252a5456f72",
  "createdBy": "89ac8716-88c5-417f-ac02-935461db9ca1",
  "createdByEmail": "jon.doe@build.com",
  "createdAt": "2022-09-11T14:49:50.915Z",
  "updatedBy": "89ac8716-88c5-417f-ac02-935461db9ca1",
  "updatedAt": "2022-09-11T14:49:50.915Z",
  "scheduleInterval": "DAY",
  "reoccuringInterval": 1,
  "effectiveFrom": "2022-09-08T13:54:05.332Z",
  "effectiveTo": "2023-11-19T16:00:00Z",
  "lastQueuedAt": null,
  "serviceGroups": [
      "admin"
  ],
  "callbackUrl": "<CALLBACK_URL>",
  "sendEmail": true
}
Show Less
The data request has been submitted.

Step 2: Receive the Callback URL
Every time a Data Connector request has finished processing, you receive a notification to the callback URL with a JSON payload that includes details about the specific job.

The example below shows the type of data you should receive.

Request
curl --location --request POST '<CALLBACK_URL>' \
  --header 'Content-Type: application/json' \
  --data-raw '{
      "state": "complete",
      "accountId": "g5s4e3b5-vbta-6b02-d23a-5d55f36ba876",
      "requestId": "6b2b85d5-6629-456e-a8d3-4a68ef5b3188",
      "jobId": "b0783d6e-791f-4430-ac6d-35864cf266db",
      "success": true
  }'
Show Less
Note the jobId (b0783d6e-791f-4430-ac6d-35864cf266db) for the extraction, which you will need to use to retrieve the extracted data.

Step 3: Examine the Files Contained in the Job’s Data Extract
To see a list of the files contained in your job’s data extract, call GET jobs/:jobId/data-listing using the job ID (b0783d6e-791f-4430-ac6d-35864cf266db).

Request
curl -X GET 'https://developer.api.autodesk.com/data-connector/v1/accounts/<accountId>/jobs/<jobId>/data-listing' \
-H 'Authorization: Bearer <authToken>'
Response
[
{
    "name": "README.html",
    "createdAt": "2022-09-10T23:49:01.785Z",
    "size": 9738
},
{
    "name": "admin_account_services.csv",
    "createdAt": "2022-09-10T23:38:03.119Z",
    "size": 533
},
{
    "name": "admin_accounts.csv",
    "createdAt": "2022-09-10T23:38:02.911Z",
    "size": 141
},
{
    "name": "admin_companies.csv",
    "createdAt": "2022-09-10T23:38:02.903Z",
    "size": 633
},
{
    "name": "admin_project_companies.csv",
    "createdAt": "2022-09-10T23:38:02.959Z",
    "size": 424
},
{
    "name": "admin_project_products.csv",
    "createdAt": "2022-09-10T23:38:02.967Z",
    "size": 872
},
{
    "name": "admin_project_roles.csv",
    "createdAt": "2022-09-10T23:38:02.919Z",
    "size": 3837
},
{
    "name": "admin_project_user_companies.csv",
    "createdAt": "2022-09-10T23:38:02.911Z",
    "size": 354
},
{
    "name": "admin_projects.csv",
    "createdAt": "2022-09-10T23:38:04.811Z",
    "size": 452
},
{
    "name": "admin_roles.csv",
    "createdAt": "2022-09-10T23:38:04.811Z",
    "size": 3447
},
{
    "name": "admin_users.csv",
    "createdAt": "2022-09-10T23:38:06.311Z",
    "size": 1008
},
{
    "name": "autodesk_data_extract.zip",
    "createdAt": "2022-09-10T23:49:01.821Z",
    "size": 142025
}
]
Show Less
The files contain data about the project, including information about project members and companies.

Step 4: Download the Files from the Data Extract
To dowload project data call GET jobs/:jobId/data/:name specifying the relevant files:

admin_users.csv
admin_companies.csv
admin_project_user_companies.csv
Alternatively, you can download the ZIP file, which contains all the files.

Request
curl --location --request GET 'https://developer.api.autodesk.com/data-connector/v1/accounts/g5s4e3b5-vbta-6b02-d23a-5d55f36ba876/jobs/b0783d6e-791f-4430-ac6d-35864cf266db/data/autodesk_data_extract.zip' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
    "name": "autodesk_data_extract.zip",
    "size": 1152,
    "signedUrl": "https://bim360dc-s-ue1-extracts.s3.amazonaws.com/data/5c07c84c-bbd9-476e-8712-547f74c5b76b/b0783d6e-791f-4430-ac6d-35864cf266db/admin_users.csv?AWSAccessKeyId=ASIAX4NRGUIN3T674OXQ&Expires=1662913320&Signature=8WZ70JCtiP855ch0ySgeil2USAM%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEOH%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIQDoItRVB4RE%2BRFXFaTDuld3ht5wudsRnzG0mca22sAPNwIgMGHW9G3KEKgeTXLZrBlLLvOsew0Ccawr4GXtdz9bqMIqiwMIeRACGgw1NDIwNzQzODA4MjciDBksP21QdYraPE5WUCroAiobOr0EEPBEg2xGIXiAZzmItu15wdWT5pvC5ci7RH%2Bz6tMOSo6teD5jR9p380aPFmF6N0PgX%2BJwgab1Cnl3Wsu8L9Ay8kk4yI26DLG8yDGj5ZVOS%2BfJArcn%2FHWzhJnrg2yu2o8hcQbGbYHKIYR%2Fjb4WKgI%2Bnc0TnHq7BGD95gACce19uk3atblL5HhJKR%2FZ8Vd%2F%2FYGhkONezkFXoe0SAq1OEzuJA%2BbreJoLRkit72Iz%2BQZPVp2aS40m4XvI7LPDHQmeeEPz%2BIDRLtQ52c1pagCXONti44ceHkxvuM0oRSX%2BYoes0mefU5SzlVUpTnUKBI2lW8urvyVAvTNHem9agfm1W9%2FQdmpLp%2Blp6yCVIZkjitBauylqo0E5mMQQjUpmda8Wc6cD4AoxZiKca1KqEBmPhOB5flQd6qMYDDiwr%2Fb%2FmjlkjQSAVU%2BpQM5VqsjOyVfu7anR0RNt8sQFQIfyckpr5H5V4Yn9yTDWlfiYBjqdAY%2BHuvnfG0jgHbeHPhcVuYoMkmnmsLt%2B4RxWOO0Ihqvpj6O3g%2B4R6nkEmyut0qchu5iMkcVD6HJYmWKJ2%2FN73Nb%2BNER9a9Ab%2F8aHnJpLfVV1x0W0MsAiRUwRN7onrHfOiPrieifpihA59RXupDmL7CxobofuE6ARk0s7OadEcnWqyN3dXQn9G7rRRcuieh396vbOQ%2BNSdGWfiLNPY6s%3D"
}
To download the file from the signed URL, use a GET method and the signedUrl attribute as the URI. Note that you should not use a bearer token with this call.

Step 5: Examine the Data
To get a list of all the members of the project, use the admin_users.csv file.

To verify the company that is assigned to each user within the project, you need to examine 3 CSV files:

admin_users.csv
admin_companies.csv
admin_project_user_companies.csv
Use admin_users.csv to get the IDs of the users of the project. Note the data in the name (user name) column and the id (user ID) column.
Use admin_companies.csv to get the IDs of the companies. Note the data in the name (company name) column and the id (company ID) column.
Use admin_project_user_companies.csv to find the companies that are assigned to the users. The user IDs that you found in (a) is equivalent to the user_id column, and the company IDs that you found in (b) is equivalent to the company_oxygen_id column. Use this file to verify the company that is assigned to each user.

Documentation /Autodesk Construction Cloud APIs /How-to Guide
Configure a Locations Tree
This tutorial demonstrates how to configure a hierarchy (a tree) of building areas (locations), also known as a location breakdown structure (LBS). Each location is a node in the tree. The steps include retrieving the tree’s root node ID (representing the project); creating two second-tier nodes with the root as their parent; adding a third-tier node under one of the second-tier nodes; renaming a node; and deleting a node.

For more details about this API, see the Locations API Field Guide.

Before you begin
Register an app
Acquire a 3-legged OAuth token with data:read and data:write scope.
Verify that you have access to the relevant Autodesk Construction Cloud account and project.
Use the Data Management API to retrieve the relevant ACC account and project IDs.
This tutorial uses the example project ID e4ae9874-0ab6-4b33-ac91-ff70e806e013, but you should replace that with the project ID you have retrieved for your project.
In this tutorial, the LBS is used as follows:

The top-tier (root) node represents a hotel.
The second-tier nodes represent floors of the hotel.
The third-tier nodes represent rooms on each floor.
Note that the nodes in a given tier don’t all have to represent the same type of location. For example, a second-tier node could represent the hotel’s roof.

Step 1: Retrieve the root node ID
Use the GET nodes endpoint to retrieve the root node of your project’s LBS. This tutorial uses 24d53a28-cda0-43b0-9021-863736edebf8 as an example of the root node ID of the tree.

Note that when the project is new, only the root node is returned, so no pagination is necessary.

Request
curl --request GET 'https://developer.api.autodesk.com/construction/locations/v2/projects/e4ae9874-0ab6-4b33-ac91-ff70e806e013/trees/default/nodes' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT'
Response
200 Succeeded

{
    {
        "results": [
            {
                "id": "24d53a28-cda0-43b0-9021-863736edebf8",
                "parentId": null,
                "type": "Root",
                "name": "Project",
                "description": null,
                "barcode": null,
                "order": 0
            }
        ]
    }
}
Show Less
The response payload includes the root node ID (results.id) value of 24d53a28-cda0-43b0-9021-863736edebf8.

Step 2: Create the first and second floor nodes
Use the POST nodes endpoint to create the new nodes in the second tier of the LBS.

Note that the root node is automatically created with the project.

Step 2.1: Create the second floor node
Create a new node and name it Floor 2 (not Floor 1). Assign Floor 2’s parent by specifying the root node’s ID as the value of parentId. In this way you start to define the tree hierarchy.

Request
curl --request POST 'https://developer.api.autodesk.com/construction/locations/v2/projects/e4ae9874-0ab6-4b33-ac91-ff70e806e013/trees/default/nodes' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT' \
-d '{
        "parentId": "24d53a28-cda0-43b0-9021-863736edebf8",
        "type": "Area",
        "name": "Floor 2",
        "barcode": "barcodeFloor2"
    }'
Show Less
Response
201 Created

{
    {
        "id": "15e5bd3f-8334-4a98-9365-3489b83506f1",
        "parentId": "24d53a28-cda0-43b0-9021-863736edebf8",
        "type": "Area",
        "name": "Floor 2",
        "description": null,
        "barcode": "barcodeFloor2",
        "order": 0
    }
}
Show Less
Now your LBS should look as follows:

       Project
       (Hotel)
      /
     /
Floor 2
The response payload includes the Floor 2 ID (id) value of 15e5bd3f-8334-4a98-9365-3489b83506f1.

Step 2.2: Create the first floor node
Create a new node and name it Floor 1. Assign Floor 1’s parent by specifying the root node’s ID as the value of parentId.

Note that this request contains two query parameters: The targetNodeId value is the id of the Floor 2 node, and the insertOption value is Before, indicating that the Floor 1 node should come before the Floor 2 node in sequence order. For more details, see POST nodes .

Request
curl --request POST 'https://developer.api.autodesk.com/construction/locations/v2/projects/e4ae9874-0ab6-4b33-ac91-ff70e806e013/trees/default/nodes?targetNodeId=15e5bd3f-8334-4a98-9365-3489b83506f1&insertOption=Before' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT' \
-d '{
        "parentId": "24d53a28-cda0-43b0-9021-863736edebf8",
        "type": "Area",
        "name": "Floor 1",
        "barcode": "barcodeFloor1"
    }'
Show Less
Response
201 Created

{
    {
        "id": "94eb2ce9-8b3f-45e8-a178-894c8c49725b",
        "parentId": "24d53a28-cda0-43b0-9021-863736edebf8",
        "type": "Area",
        "name": "Floor 1",
        "description": null,
        "barcode": "barcodeFloor1",
        "order": 0
    }
}
Show Less
Now your LBS should look as follows:

      Project
      (Hotel)
     /       \
    /         \
Floor 1      Floor 2
The response payload includes the Floor 1 ID (id) value of 94eb2ce9-8b3f-45e8-a178-894c8c49725b, and the order value of 0, indicating that Floor 1 is before Floor 2 in sequence order (Floor 2’s order is now 1).

Step 3: Create a second floor suite node
Under the Floor 2 node, use the POST nodes endpoint to create a new node and name it Suite 205. Assign Suite 205’s parent by specifying the Floor 2 ID as the value of parentId.

Request
curl --request POST 'https://developer.api.autodesk.com/construction/locations/v2/projects/e4ae9874-0ab6-4b33-ac91-ff70e806e013/trees/default/nodes' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT' \
-d '{
        "parentId": "15e5bd3f-8334-4a98-9365-3489b83506f1",
        "type": "Area",
        "name": "Suite 205",
        "barcode": "barcodeSuite205"
    }'
Show Less
Response
201 Created

{
    {
        "id": "76e6814b-4a10-4347-80bd-d9b429453807",
        "parentId": "15e5bd3f-8334-4a98-9365-3489b83506f1",
        "type": "Area",
        "name": "Suite 205",
        "description": null,
        "barcode": "barcodeSuite205",
        "order": 0
    }
}
Show More
Your LBS should look as follows:

      Project
      (Hotel)
     /       \
    /         \
Floor 1      Floor 2
                \
                 \
               Suite 205
Show Less
The response payload includes the Suite 205 ID (id) value of 76e6814b-4a10-4347-80bd-d9b429453807.

Step 4: Update the suite node
Use the PATCH nodes/{nodeId} endpoint to update the node’s name, barcode, or both.

Note that you cannot send the request without at least one of these two fields.

Update node Suite 205’s name to be “Suite 211”, and its barcode to be “barcodeSuite211” (passing the node’s ID as a URI parameter).

Request
curl --request PATCH 'https://developer.api.autodesk.com/construction/locations/v2/projects/e4ae9874-0ab6-4b33-ac91-ff70e806e013/trees/default/nodes/76e6814b-4a10-4347-80bd-d9b429453807' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT' \
-d '{
        "name": "Suite 211",
        "barcode": "barcodeSuite211"
    }'
Response
200 Ok

{
    {
        "name": "Suite 211",
        "description": null,
        "barcode": "barcodeSuite211",
        "parentId": "15e5bd3f-8334-4a98-9365-3489b83506f1",
        "id": "76e6814b-4a10-4347-80bd-d9b429453807",
        "type": "Area",
        "order": 0
    }
}
Show Less
Your LBS should look as follows:

      Project
      (Hotel)
     /       \
    /         \
Floor 1      Floor 2
                \
                 \
               Suite 211
Show Less
The response payload includes the node’s updated name and barcode.

Step 5: Delete the suite node
Use the DELETE nodes/{nodeId} endpoint to delete the Suite 211 node by passing the node’s ID (76e6814b-4a10-4347-80bd-d9b429453807) as a URI parameter.

Request
curl --request DELETE 'https://developer.api.autodesk.com/construction/locations/v2/projects/e4ae9874-0ab6-4b33-ac91-ff70e806e013/trees/default/nodes/76e6814b-4a10-4347-80bd-d9b429453807' \
-H 'Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT'
Response
204 No Content
Finally, your LBS should look as follows:

      Project
      (Hotel)
     /       \
    /         \
Floor 1      Floor 2
Congratulations! You have created a location breakdown structure and modified it using the Locations API.

Documentation /Autodesk Construction Cloud APIs /How-to Guide
Model Sets and Versions
This tutorial demonstrates the various features of the Model Set Service. Model sets and model set versions are the unit of coordination used in BIM 360 Model Coordination. Model sets are equivalent to the coordination spaces configured via the Model Coordination Project Admin web UI. There is currently a limitation in the BIM 360 Model Coordination application resulting in the API not being accessible on new BIM 360 projects until the first coordination space has been defined by a project administrator. Essentially, the administrative process of creating the first collaboration space initializes the model set service container. If you are running these samples against a new BIM 360 project with no coordination spaces, you first need to manually create a coordination space via the Model Coordination Project Admin web UI.

Before You Begin
Make sure that you have registered an app. and successfully acquired an OAuth token with the data:read, data:write and data:create scopes.

Creating model sets
Once the model coordination container is initialized, you can programmatically create new model sets (coordination spaces) by posting a BIM 360 Docs Plans or Project Files folder URN on to POST modelsets endpoint. All of the endpoints in the model coordination API that change data are asynchronous. The initial POST, PATCH, PUT, or DELETE call starts a job. The various resource collections in the API each have corresponding job endpoints that you can use to track the success or failure of asynchronous operations.

Example Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f83cef12-deef-4771-9feb-4f85643e3c46/modelsets'
     -X POST
     -H 'Authorization: Bearer <token>'
     -H 'Content-Type: application/json'
     -d '{
       "name": "My Model Set",
       "description": "Space for coordinating all disciplines",
       "folders": [
         {
           "folderUrn": "urn:adsk.wipprod:fs.folder:co.WI8roO18TU2Cl3P9y64z4w"
         }
       ]
     }'
Show More
The initial response from the POST to the modelsets endpoint returns a job response body containing the jobId, status, and metadata associated with the job (in this case, the creation of a new model set). The job seed encapsulates the original input to the job, and provides a mechanism for correlating the job with the original POST, PATCH, PUT, or DELETE call that started the job. The initial response from the POST onto the modesets endpoint returns a status of Running, indicating that the job is executing. Also note that the system has allocated the new model set a GUID identity that is returned in the modelSetId property on the response object.

Example Response
{
    "jobId":"d41e37e7-921f-4e72-a33a-906085dc052b",
    "modelSetId":"a5fea9de-7487-45b8-a9f2-878cf7069053",
    "status":"Running",
    "job": {
        "operation":"CreateScope",
        "seed": {
            "createdBy":"DLLKP4DBC383",
            "name":"My Model Set",
            "description":"Space for coordinating all disciplines",
            "scopeId":"a5fea9de-7487-45b8-a9f2-878cf7069053",
            "containerId":"f83cef12-deef-4771-9feb-4f85643e3c46",
            "folders":[
                {
                    "folderUrn":"urn:adsk.wipprod:fs.folder:co.WI8roO18TU2Cl3P9y64z4w",
                    "documentFilters":null
                }
            ],
            "isDisabled":false
        }
    }
}
Show More
Taking the jobId from the response, you can call the container GET jobs/:jobId endpoint. Model sets belong to containers (that is, the process of adding a new model set to a container is a container-level operation, so you can use the container jobs endpoint to track the progress of the job).

Example Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f83cef12-deef-4771-9feb-4f85643e3c46/jobs/d41e37e7-921f-4e72-a33a-906085dc052b'
     -H 'Authorization: Bearer <token>'
Each call to a jobs endpoint yields a response similar to the initial response returned by the POST, PATCH, PUT, or DELETE operation that originally started the job. In the response below, the status is changed to Succeeded and you can interrogate the seed to get the data associated with the operation that originally started the job (in this case, a POST onto the modelsets endpoint).

Example Response
{
    "jobId":"d41e37e7-921f-4e72-a33a-906085dc052b",
    "modelSetId":"a5fea9de-7487-45b8-a9f2-878cf7069053",
    "status":"Succeeded",
    "job": {
        "operation":"CreateScope",
        "seed": {
            "createdBy":"DLLKP4DBC383",
            "name":"My Model Set",
            "description":"Space for coordinating all disciplines",
            "scopeId":"a5fea9de-7487-45b8-a9f2-878cf7069053",
            "containerId":"f83cef12-deef-4771-9feb-4f85643e3c46",
            "folders":[
                {
                    "folderUrn":"urn:adsk.wipprod:fs.folder:co.WI8roO18TU2Cl3P9y64z4w",
                    "documentFilters":null
                }
            ],
            "isDisabled":false
        }
    }
}
Show Less
Querying model sets
You can also use the GET modelsets endpoint on a container to list the currently defined model sets in the container. This endpoint is paged and returns all of the data necessary to interrogate an individual model set for its versions and the clash and index data associated with these versions.

Example Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f83cef12-deef-4771-9feb-4f85643e3c46/modelsets'
     -H 'Authorization: Bearer <token>'
In addition to returning display properties such as the name and description of the model set (as presented to the user in the BIM 360 Model Coordination web UI), you can also determine when the model set was created and obtain the ID of the user who created the model set. Model sets also have an isDeleted flag, indicating that the model set is no longer accessible via the web UI. Model sets and the data associated with them are only physically deleted when the model set container is deleted. The following sample response shows four model sets in this container.

Example Response
{
    "page": {},
    "modelSets": [
        {
            "modelSetId": "a5fea9de-7487-45b8-a9f2-878cf7069053",
            "containerId": "f83cef12-deef-4771-9feb-4f85643e3c46",
            "name": "My Model Set",
            "description": "Space for coordinating all disciplines",
            "createdBy": "DLLKP4DBC383",
            "createdTime": "2019-11-06T08:13:44.271173+00:00",
            "isDisabled": false,
            "isDeleted": false
        },
        {
            "modelSetId": "9338f1cb-3b63-465f-8c16-7719318fd2bb",
            "containerId": "f83cef12-deef-4771-9feb-4f85643e3c46",
            "name": "MC_20190909190333",
            "description": "This model set has been created to demonstrate the Model Coordination API and encapsulates MC_20190909190333",
            "createdBy": "7ERBMBR9EA4A",
            "createdTime": "2019-09-09T19:04:00.982144+00:00",
            "isDisabled": false,
            "isDeleted": false
        },
        {
            "modelSetId": "c85f934f-9945-4172-b905-5ec57dea09db",
            "containerId": "f83cef12-deef-4771-9feb-4f85643e3c46",
            "name": "MC_20190906122228",
            "description": "This model set has been created to demonstrate the Model Coordination API and encapsulates MC_20190906122228",
            "createdBy": "7ERBMBR9EA4A",
            "createdTime": "2019-09-06T12:23:25.33839+00:00",
            "isDisabled": false,
            "isDeleted": false
        },
        {
            "modelSetId": "e1e51b92-fccf-4672-9dd7-9bd66471cfa2",
            "containerId": "f83cef12-deef-4771-9feb-4f85643e3c46",
            "name": "MC_20190903092025",
            "description": "This model set has been created to demonstrate the Model Coordination API and encapsulates MC_20190903092025",
            "createdBy": "7ERBMBR9EA4A",
            "createdTime": "2019-09-03T09:21:08.256452+00:00",
            "isDisabled": false,
            "isDeleted": false
        }
    ]
}
Show Less
To obtain the full details of a given model set, you can call the GET modelsets/:modelSetId endpoint, supplying a modelSetId GUID identity returned in the above response.

Example Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f83cef12-deef-4771-9feb-4f85643e3c46/modelsets/a5fea9de-7487-45b8-a9f2-878cf7069053'
     -H 'Authorization: Bearer <token>'
The response is very similar to the paged summary response returned above; however, the detailed response also includes the folder URN associated with the model set, along with the current tipVersion of the model set. Model set versioning is the subject of the next section in this tutorial.

Example Response
{
    "modelSetId": "a5fea9de-7487-45b8-a9f2-878cf7069053",
    "modelSetType": "Plans",
    "containerId": "f83cef12-deef-4771-9feb-4f85643e3c46",
    "folders": [
        {
            "folderUrn": "urn:adsk.wipprod:fs.folder:co.WI8roO18TU2Cl3P9y64z4w"
        }
    ],
    "name": "My Model Set",
    "description": "Space for coordinating all disciplines",
    "createdBy": "DLLKP4DBC383",
    "createdTime": "2019-11-06T08:13:44.271173+00:00",
    "isDisabled": false,
    "tipVersion": 3
}
Show Less
Querying model set versions
Once a model set is defined, it is automatically “enabled” by the system. An enabled model set results in the system automatically creating model set versions as users interact with BIM 360 Docs. If a user changes the file content in a folder associated with a model set, the system automatically scans the tip versions of the 3D model content in the folder. If this scan yields a set of file versions different to any proceeding scan, a new model set version is created. Model set versions are sequential for a model set and have sequential version numbers. To page through the model set versions for a model set, you call its GET modelsets/:modelSetId/versions endpoint.

Example Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f83cef12-deef-4771-9feb-4f85643e3c46/modelsets/a5fea9de-7487-45b8-a9f2-878cf7069053/versions'
     -H 'Authorization: Bearer <token>'
The versions endpoint returns paged model set version summaries. These summaries include the status of each model set version, the date and time they were created, and the unique (within the context of a model set) version number.

Example Response
{
    "page": {},
    "modelSetVersions": [
        {
            "version": 3,
            "createTime": "2019-11-06T08:16:28.747403+00:00",
            "status": "Successful"
        },
        {
            "version": 2,
            "createTime": "2019-11-06T08:15:36.867067+00:00",
            "status": "Successful"
        },
        {
            "version": 1,
            "createTime": "2019-11-06T08:15:02.273917+00:00",
            "status": "Successful"
        }
    ]
}
Show Less
You can query a specific model set version by calling the GET modelsets/:modelSetId/versions/:version endpoint and passing the version number of the model set version.

Example Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f83cef12-deef-4771-9feb-4f85643e3c46/modelsets/61b5025d-59d0-43fd-add4-bdbd9b59119a/versions/3'
     -H 'Authorization: Bearer <token>'
This returns the immutable set of 3D model files that was found when the system queried the tip versions of the document lineages beneath the folder associated with the model set definition. You can use the model set version status and individual document version status properties to determine whether or not the system was able to successfully process all the files in the model set version. The ability of the system to track model content at the object/element level between successive versions of a file is dependent on an underlying object tracking capability of the model set service. Under certain conditions, object tracking is not possible for a file version. Under these conditions the document version is still visible via the BIM 360 model viewer, but the tracking IDs for objects in the model cannot be determined. Any downstream model set version workflow that is dependent on these IDs (for example, clash testing) uses these status values to determine if the model set version can be processed or partially processed.

Example Response
{
    "modelSetId": "a5fea9de-7487-45b8-a9f2-878cf7069053",
    "version": 3,
    "createTime": "2019-11-06T08:16:28.747403+00:00",
    "status": "Successful",
    "documentVersions": [
        {
            "documentLineage": {
                "lineageUrn": "urn:adsk.wipprod:dm.lineage:9IeFYnYxTB-OMsg3vwb3hQ",
                "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.-iqpHJcgSS6oVHYtZjoYnw",
                "isAligned": true,
                "tipVersionUrn": "urn:adsk.wipprod:fs.file:vf.9IeFYnYxTB-OMsg3vwb3hQ?version=1"
            },
            "documentStatus": "Succeeded",
            "forgeType": "versions:autodesk.bim360:Document",
            "versionUrn": "urn:adsk.wipprod:fs.file:vf.9IeFYnYxTB-OMsg3vwb3hQ?version=1",
            "displayName": "{3D}_Audubon_Structure.rvt",
            "viewableName": "{3D}",
            "createUserId": "ERZWLHJGT7NE",
            "createTime": "2019-11-06T08:14:55+00:00",
            "viewableGuid": "00cd2da3-fbfa-44a9-7a33-cad0bc4720cb",
            "viewableId": "0935d8b2-149b-4a0d-b816-863f0d595a20-000bcd64",
            "viewableMime": "application/autodesk-svf",
            "bubbleUrn": "urn:adsk.wipprod:fs.file:vf.NKGUU8CLQ8WP_dCM54KKKg?version=1",
            "originalSeedFileVersionUrn": "urn:adsk.wipprod:fs.file:vf.NKGUU8CLQ8WP_dCM54KKKg?version=1",
            "originalSeedFileVersionName": "Audubon_Structure.rvt"
        },
        {
            "documentLineage": {
                "lineageUrn": "urn:adsk.wipprod:dm.lineage:bAGrilc0SDyczBLIHEQFdA",
                "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.-iqpHJcgSS6oVHYtZjoYnw",
                "isAligned": true,
                "tipVersionUrn": "urn:adsk.wipprod:fs.file:vf.bAGrilc0SDyczBLIHEQFdA?version=1"
            },
            "documentStatus": "Skipped",
            "forgeType": "versions:autodesk.bim360:Document",
            "versionUrn": "urn:adsk.wipprod:fs.file:vf.bAGrilc0SDyczBLIHEQFdA?version=1",
            "displayName": "New Construction_Audubon_Mechanical.rvt",
            "viewableName": "New Construction",
            "createUserId": "ERZWLHJGT7NE",
            "createTime": "2019-11-06T08:16:21+00:00",
            "viewableGuid": "38c10754-d1f9-5bf6-2546-4bac2d3dab5b",
            "viewableId": "c884ae1b-61e7-4f9d-0001-719e20b22d0b-00121ed3",
            "viewableMime": "application/autodesk-svf",
            "bubbleUrn": "urn:adsk.wipprod:fs.file:vf.ajkTDG4eQeuDpBvbwX8Gfw?version=1",
            "originalSeedFileVersionUrn": "urn:adsk.wipprod:fs.file:vf.ajkTDG4eQeuDpBvbwX8Gfw?version=1",
            "originalSeedFileVersionName": "Audubon_Mechanical.rvt"
        },
        {
            "documentLineage": {
                "lineageUrn": "urn:adsk.wipprod:dm.lineage:eFcw-VElSrG-6SxjvnBHgA",
                "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.-iqpHJcgSS6oVHYtZjoYnw",
                "isAligned": true,
                "tipVersionUrn": "urn:adsk.wipprod:fs.file:vf.eFcw-VElSrG-6SxjvnBHgA?version=1"
            },
            "documentStatus": "Succeeded",
            "forgeType": "versions:autodesk.bim360:Document",
            "versionUrn": "urn:adsk.wipprod:fs.file:vf.eFcw-VElSrG-6SxjvnBHgA?version=1",
            "displayName": "{3D}_Audubon_Architecture.rvt",
            "viewableName": "{3D}",
            "createUserId": "ERZWLHJGT7NE",
            "createTime": "2019-11-06T08:15:30+00:00",
            "viewableGuid": "5d41dda7-eea1-eff5-77dd-ee1aa81fc3a8",
            "viewableId": "845097d1-c3be-4a6f-9dbe-51582fa6d465-002c2f04",
            "viewableMime": "application/autodesk-svf",
            "bubbleUrn": "urn:adsk.wipprod:fs.file:vf.kPYVVTK4SC2TcE2XJJdvuw?version=1",
            "originalSeedFileVersionUrn": "urn:adsk.wipprod:fs.file:vf.kPYVVTK4SC2TcE2XJJdvuw?version=1",
            "originalSeedFileVersionName": "Audubon_Architecture.rvt"
        },
        {
            "documentLineage": {
                "lineageUrn": "urn:adsk.wipprod:dm.lineage:EmoWniVZQlua5GTXFWwfTA",
                "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.-iqpHJcgSS6oVHYtZjoYnw",
                "isAligned": true,
                "tipVersionUrn": "urn:adsk.wipprod:fs.file:vf.EmoWniVZQlua5GTXFWwfTA?version=1"
            },
            "documentStatus": "Skipped",
            "forgeType": "versions:autodesk.bim360:Document",
            "versionUrn": "urn:adsk.wipprod:fs.file:vf.EmoWniVZQlua5GTXFWwfTA?version=1",
            "displayName": "New Construction_Audubon_Architecture.rvt",
            "viewableName": "New Construction",
            "createUserId": "ERZWLHJGT7NE",
            "createTime": "2019-11-06T08:15:30+00:00",
            "viewableGuid": "10c25a10-5469-3aef-b0a6-1c27c7b8e93b",
            "viewableId": "c884ae1b-61e7-4f9d-0001-719e20b22d0b-0032f400",
            "viewableMime": "application/autodesk-svf",
            "bubbleUrn": "urn:adsk.wipprod:fs.file:vf.kPYVVTK4SC2TcE2XJJdvuw?version=1",
            "originalSeedFileVersionUrn": "urn:adsk.wipprod:fs.file:vf.kPYVVTK4SC2TcE2XJJdvuw?version=1",
            "originalSeedFileVersionName": "Audubon_Architecture.rvt"
        },
        {
            "documentLineage": {
                "lineageUrn": "urn:adsk.wipprod:dm.lineage:r4Boku9qT9iQ6C1ofbYaCg",
                "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.-iqpHJcgSS6oVHYtZjoYnw",
                "isAligned": true,
                "tipVersionUrn": "urn:adsk.wipprod:fs.file:vf.r4Boku9qT9iQ6C1ofbYaCg?version=1"
            },
            "documentStatus": "Succeeded",
            "forgeType": "versions:autodesk.bim360:Document",
            "versionUrn": "urn:adsk.wipprod:fs.file:vf.r4Boku9qT9iQ6C1ofbYaCg?version=1",
            "displayName": "{3D}_Audubon_Mechanical.rvt",
            "viewableName": "{3D}",
            "createUserId": "ERZWLHJGT7NE",
            "createTime": "2019-11-06T08:16:21+00:00",
            "viewableGuid": "a3186f12-7750-fa47-f60a-610a779ba5ac",
            "viewableId": "24bb580c-5e74-4a65-bcae-e97c21424529-00027e16",
            "viewableMime": "application/autodesk-svf",
            "bubbleUrn": "urn:adsk.wipprod:fs.file:vf.ajkTDG4eQeuDpBvbwX8Gfw?version=1",
            "originalSeedFileVersionUrn": "urn:adsk.wipprod:fs.file:vf.ajkTDG4eQeuDpBvbwX8Gfw?version=1",
            "originalSeedFileVersionName": "Audubon_Mechanical.rvt"
        },
        {
            "documentLineage": {
                "lineageUrn": "urn:adsk.wipprod:dm.lineage:xMPsOKv5RIWG4pdPJ5IY5Q",
                "parentFolderUrn": "urn:adsk.wipprod:fs.folder:co.-iqpHJcgSS6oVHYtZjoYnw",
                "isAligned": true,
                "tipVersionUrn": "urn:adsk.wipprod:fs.file:vf.xMPsOKv5RIWG4pdPJ5IY5Q?version=1"
            },
            "documentStatus": "Skipped",
            "forgeType": "versions:autodesk.bim360:Document",
            "versionUrn": "urn:adsk.wipprod:fs.file:vf.xMPsOKv5RIWG4pdPJ5IY5Q?version=1",
            "displayName": "New Construction_Audubon_Structure.rvt",
            "viewableName": "New Construction",
            "createUserId": "ERZWLHJGT7NE",
            "createTime": "2019-11-06T08:14:55+00:00",
            "viewableGuid": "4a966c2a-ead6-65c3-4f98-273dd7543047",
            "viewableId": "c884ae1b-61e7-4f9d-0001-719e20b22d0b-00120bb2",
            "viewableMime": "application/autodesk-svf",
            "bubbleUrn": "urn:adsk.wipprod:fs.file:vf.NKGUU8CLQ8WP_dCM54KKKg?version=1",
            "originalSeedFileVersionUrn": "urn:adsk.wipprod:fs.file:vf.NKGUU8CLQ8WP_dCM54KKKg?version=1",
            "originalSeedFileVersionName": "Audubon_Structure.rvt"
        }
    ]
}
Show Less
The previous example described how to navigate from a model set to discover its versions, then how to select one of these versions to display the content associated with this version. The model set service provides a GET modelsets/:modelSetId/versions/latest short-cut API call that returns the details of the most recently available model set version.

Example Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f83cef12-deef-4771-9feb-4f85643e3c46/modelsets/a5fea9de-7487-45b8-a9f2-878cf7069053/versions/latest'
     -H 'Authorization: Bearer <token>'
Controlling automatic model set version creation
Up to this point, the examples work on the principle that model set versions should be created automatically as users interact with BIM 360 Docs (uploading, moving, and copying content). This has the potential to create redundant model set versions, representing intermediate states on the project that have no real value from a data analysis point of view. The model set service solves this potential issue by allowing API users to enable and disable automatic model set version creation. You can use the PATCH modelsets/:modelSetId/versions:disable endpoint to switch off automatic model set version creation.

Example Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f83cef12-deef-4771-9feb-4f85643e3c46/modelsets/a5fea9de-7487-45b8-a9f2-878cf7069053/versions:disable'
     -X PATCH
     -H 'Authorization: Bearer <token>'
The response from this endpoint is a model set job, the seed of which indicates that the isDisabled setting on a model set is toggled from false to true.

Example Response
{
    "jobId":"37ec9440-6ff8-4d7c-a817-78c527d4982e",
    "modelSetId":"a5fea9de-7487-45b8-a9f2-878cf7069053",
    "status":"Running",
    "job": {
        "seed": {
            "scopeId":"a5fea9de-7487-45b8-a9f2-878cf7069053",
            "isDisabled": {
                "original":false,
                "new":true
            }
        }
    }
}
Show Less
As before, you can track the status of this job using the GET modelsets/:modelSetId/jobs/:jobId endpoint.

Example Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f83cef12-deef-4771-9feb-4f85643e3c46/modelsets/a5fea9de-7487-45b8-a9f2-878cf7069053/jobs/37ec9440-6ff8-4d7c-a817-78c527d4982e'
     -H 'Authorization: Bearer <token>'
A status of Succeeded indicates that automatic model set version creation is disabled. At this point, all user interaction with BIM 360 Docs within the context of the disabled model set are ignored by the system and no further model set versions are created for the disable model set.

Example Response
{
    "jobId":"37ec9440-6ff8-4d7c-a817-78c527d4982e",
    "modelSetId":"a5fea9de-7487-45b8-a9f2-878cf7069053",
    "status":"Succeeded",
    "job": {
        "operation":"UpdateScope",
        "seed": {
            "scopeId":"a5fea9de-7487-45b8-a9f2-878cf7069053",
            "isDisabled": {
                "original":false,
                "new":true
            }
        }
    }
}
Show Less
You can enable a disabled model set version by calling the PATCH modelsets/:modelSetId/versions:enable endpoint, which starts a job to re-enable automatic model set versioning.

Example Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f83cef12-deef-4771-9feb-4f85643e3c46/modelsets/a5fea9de-7487-45b8-a9f2-878cf7069053/versions:enable'
     -X PATCH
     -H 'Authorization: Bearer <token>'
Once again, this endpoint returns a job that you can track using the GET modelsets/:modelSetId/jobs/:jobId endpoint.

Example Response
{
    "jobId":"ca8c7d00-fe59-4173-ba80-449cbe5a6ab2",
    "modelSetId":"a5fea9de-7487-45b8-a9f2-878cf7069053",
    "status":"Running",
    "job": {
        "seed": {
            "scopeId":"a5fea9de-7487-45b8-a9f2-878cf7069053",
            "isDisabled": {
                "original":true,
                "new":false
            }
        }
    }
}
Show Less
Example Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f83cef12-deef-4771-9feb-4f85643e3c46/modelsets/a5fea9de-7487-45b8-a9f2-878cf7069053/jobs/ca8c7d00-fe59-4173-ba80-449cbe5a6ab2'
     -H 'Authorization: Bearer <token>'
A status of Succeeded indicates that automatic model set version creation is enabled. At this point, all user interaction with BIM 360 Docs within the context of the enabled model set is processed by the system creating new model set versions for the newly enabled model set.

Example Response
{
    "jobId":"ca8c7d00-fe59-4173-ba80-449cbe5a6ab2",
    "modelSetId":"a5fea9de-7487-45b8-a9f2-878cf7069053",
    "status":"Succeeded",
    "job": {
        "operation":"UpdateScope",
        "seed": {
            "scopeId":"a5fea9de-7487-45b8-a9f2-878cf7069053",
            "isDisabled": {
                "original":true,
                "new":false
            }
        }
    }
}
Show Less
Manually creating a model set version
If you disable automatic model set version creation, it is still possible to get the system to create new model set versions by calling the POST modelsets/:modelSetId/versions endpoint. This has the net effect of invoking the same workflow that is run when automatic model set version creation is enabled. The logic is identical: if a new model set version can be calculated, then it is persisted. If, however, the tip versions of the models in the model set have not changed since the last time the model set version workflow was invoked, a new model set version is not persisted. As with all other data modifying workflows in the model coordination API, this call starts a job.

Example Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f83cef12-deef-4771-9feb-4f85643e3c46/modelsets/a5fea9de-7487-45b8-a9f2-878cf7069053/versions'
     -X POST
     -H 'Authorization: Bearer <token>'
The scopeId in the seed returned in response to the POST on the model set versions endpoint is the ID of the model set that is being targeted by the new model set version workflow.

Example Response
{
    "jobId": "98d1aab3-209b-489e-96e9-51cf7d3c4724",
    "modelSetId": "a5fea9de-7487-45b8-a9f2-878cf7069053",
    "status": "Running",
    "job": {
        "seed": {
            "scopeId": "a5fea9de-7487-45b8-a9f2-878cf7069053"
        }
    }
}
Show Less
As before, you can use a call to the GET modelsets/:modelSetId/jobs/:jobId endpoint to track the progress of the new model set version workflow.

Example Request
curl -v 'https://developer.api.autodesk.com/bim360/modelset/v3/containers/f83cef12-deef-4771-9feb-4f85643e3c46/modelsets/a5fea9de-7487-45b8-a9f2-878cf7069053/jobs/98d1aab3-209b-489e-96e9-51cf7d3c4724'
     -H 'Authorization: Bearer <token>'
A status of Succeeded indicates that the new model set version workflow has completed successfully.

Example Response
{
    "jobId": "98d1aab3-209b-489e-96e9-51cf7d3c4724",
    "modelSetId": "a5fea9de-7487-45b8-a9f2-878cf7069053",
    "status": "Succeeded",
    "job": {
        "operation": "CreateScopeVersion",
        "seed": {
            "scopeId": "a5fea9de-7487-45b8-a9f2-878cf7069053"
        }
    }
}

Documentation /Autodesk Construction Cloud APIs /How-to Guide
Querying Model Properties
The following step-by-step tutorial describes how to create a basic property index and run a simple query against this index.

Step 1: Specify the index
To create a basic index, call the batch status method, which allows you to check the status of one or more file version indexes. The batch status endpoint is lazy, meaning that if an indexing job for the file(s) specified in batch status check have not been executed, the service will automatically start the missing job(s). For the purposes of this tutorial, however, we will use the simple single file mode.

Example Request
In the request below a POST is made to the index batch status endpoint passing in a single model file. There are no query or columns properties set in the payload so no query results will be generated in response to this operation.

curl --request POST 'https://developer.api.autodesk.com/construction/index/v2/projects/f83cef12-deef-4771-9feb-4f85643e3c46/indexes:batch-status' \
     --header 'Authorization: Bearer ****' \
     --header 'Content-Type: application/json' \
     --data-raw '{
        "versions": [
             {
                 "versionUrn": "urn:adsk.wipprod:fs.file:vf.DyTWutcvTcOLUNUARxcTzQ?version=4"
             }
         ]
     }'
Show Less
Example Response
The response to a batch status request is an array of status objects, one per file being indexed. The indexId on the status object is the unique identifier for this index and can be used in subsequent calls to check the progress of the indexing job and to later download the resources associated with the index. Calling the batch status endpoint multiple times will not result in multiple, duplicate indexes as long as the input parameters of the request do not change. Provided the array of objects in the versions set, query, and optionally columns properties passed to the endpoints remain unchanged, the caller will always be returned the same indexId.

In addition to the indexId the the status response object contains the status of the indexing job. Indexes once calculated are cached for 30 days on a rolling event horizon that is incremented every time the index is accessed. If an index is not accessed for 30 days it will fall out of the cache and will need to be subsequently recalculated. A status of PROCESSING indicates that the service is building the index. This could include waiting for SVF2 translation to complete. When the service has successfully created an index the status will be set to FINISHED. This indicates that the index and all its resources are available for download. The contract returned by the index service in response to an index status request also includes a suggested retryAt timestamp, which can be used to regulate status polling frequency.

[
    {
        "projectId": "f83cef12-deef-4771-9feb-4f85643e3c46",
        "indexId": "qTmPiKJZ7siqxkTNpWGANw",
        "type": "INDEX",
        "state": "PROCESSING",
        "selfUrl": "https://developer.api.autodesk.com/construction/index/v2/projects/f83cef12-deef-4771-9feb-4f85643e3c46/indexes/qTmPiKJZ7siqxkTNpWGANw",
        "versionUrns": [
            "urn:adsk.wipprod:fs.file:vf.DyTWutcvTcOLUNUARxcTzQ?version=4"
        ],
        "updatedAt": "2021-08-19T08:21:13.8771187+00:00",
        "retryAt": "2021-08-27T14:28:28.8382067+00:00",
        "stats": null,
        "manifestUrl": null,
        "fieldsUrl": null,
        "propertiesUrl": null
    }
]
Show Less
The properties returned by this endpoint are as follows:

Property	Description
projectId	The project GUID
indexId	The unique ID for the index
type	The type of index INDEX (standard) or DIFF
state	The status of the indexing job (PROCESSING, FINISHED, FAILED)
selfUrl	The URL to this index job
versionUrns	The array of file version URNs passed to the indexing job
updatedAt	The date time the status of this job was last refreshed
retryAt	The suggested date time at which callers should poll for an updated status
stats	If the index state is FINISHED, the statistics for this index in terms of the number of objects
manifestUrl	If the index state is FINISHED, the URL to the manifest for this index, otherwise null
fieldsUrl	If the index state is FINISHED, the URL to the fields for this index, otherwise null
propertiesUrl	If the index state is FINISHED, the URL to the properties for this index, otherwise null
Step 2: Poll for progress
To track the progress of an indexing request, send a GET request to the index status endpoint using the indexId obtained in the batch status request. When the index has a status of FINISHED processing, the index is available for querying and download.

Example Request
curl --request GET 'https://developer.api.autodesk.com/construction/index/v2/projects/f83cef12-deef-4771-9feb-4f85643e3c46/indexes/qTmPiKJZ7siqxkTNpWGANw' \
     --header 'Authorization: Bearer ****'
Example Response
{
    "projectId": "f83cef12-deef-4771-9feb-4f85643e3c46",
    "indexId": "qTmPiKJZ7siqxkTNpWGANw",
    "type": "INDEX",
    "state": "FINISHED",
    "selfUrl": "https://developer.api.autodesk.com/construction/index/v2/projects/f83cef12-deef-4771-9feb-4f85643e3c46/indexes/qTmPiKJZ7siqxkTNpWGANw",
    "versionUrns": [
        "urn:adsk.wipprod:fs.file:vf.DyTWutcvTcOLUNUARxcTzQ?version=4"
    ],
    "updatedAt": "2021-08-19T08:21:13.8771187+00:00",
    "retryAt": "2021-08-27T14:31:55.1444684+00:00",
    "stats": {
        "objects": 33097
    },
    "manifestUrl": "https://developer.api.autodesk.com/construction/index/v2/projects/f83cef12-deef-4771-9feb-4f85643e3c46/indexes/qTmPiKJZ7siqxkTNpWGANw/manifest",
    "fieldsUrl": "https://developer.api.autodesk.com/construction/index/v2/projects/f83cef12-deef-4771-9feb-4f85643e3c46/indexes/qTmPiKJZ7siqxkTNpWGANw/fields",
    "propertiesUrl": "https://developer.api.autodesk.com/construction/index/v2/projects/f83cef12-deef-4771-9feb-4f85643e3c46/indexes/qTmPiKJZ7siqxkTNpWGANw/properties"
}
Show Less
When an index has been successfully created (state equals FINISHED), it contains three downloadable json.gz resources: a manifest describing the files and SVF2 database resources that were used to create the index, a list of fields (dimensions) in the index, and the index property data. Each of these resources has a URL that can be used to fetch the corresponding resource. The response JSON is identical to the response returned by the POST to the batch status endpoint (step 1 above).

Step 3: (Optional) Download the manifest
To retrieve the index manifest make a GET to the manifest endpoint as described in the field guide

Example Request
curl --request GET 'https://developer.api.autodesk.com/construction/index/v2/projects/f83cef12-deef-4771-9feb-4f85643e3c46/indexes/qTmPiKJZ7siqxkTNpWGANw/manifest' \
     --header 'Authorization: Bearer ****'
Example Response
{
    "schema": "2.0.0",
    "projectId": "f83cef12-deef-4771-9feb-4f85643e3c46",
    "status": "Succeeded",
    "createdAt": "2021-07-23T08:56:07.0868303+00:00",
    "seedFiles": [
        {
            "lineageId": "a19f7db",
            "lineageUrn": "urn:adsk.wipprod:dm.lineage:DyTWutcvTcOLUNUARxcTzQ",
            "versionUrn": "urn:adsk.wipprod:fs.file:vf.DyTWutcvTcOLUNUARxcTzQ?version=4",
            "databases": [
                {
                    "id": "3747dccf",
                    "offsets": "urn:adsk.viewing:fs.file:dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLkR5VFd1dGN2VGNPTFVOVUFSeGNUelE_dmVyc2lvbj00/output/Resource/objects_offs.json.gz",
                    "attributes": "urn:adsk.viewing:fs.file:dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLkR5VFd1dGN2VGNPTFVOVUFSeGNUelE_dmVyc2lvbj00/output/Resource/objects_attrs.json.gz",
                    "values": "urn:adsk.viewing:fs.file:dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLkR5VFd1dGN2VGNPTFVOVUFSeGNUelE_dmVyc2lvbj00/output/Resource/objects_vals.json.gz",
                    "mapping": "urn:adsk.viewing:fs.file:dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLkR5VFd1dGN2VGNPTFVOVUFSeGNUelE_dmVyc2lvbj00/output/Resource/objects_avs.json.gz",
                    "ids": "urn:adsk.viewing:fs.file:dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLkR5VFd1dGN2VGNPTFVOVUFSeGNUelE_dmVyc2lvbj00/output/Resource/objects_ids.json.gz"
                }
            ],
            "views": [
                {
                    "id": "e7fda9d5",
                    "urn": "urn:adsk.wipprod:fs.file:vf.DyTWutcvTcOLUNUARxcTzQ?version=4",
                    "is3d": true,
                    "viewableName": "{3D}",
                    "viewableId": "0935d8b2-149b-4a0d-b816-863f0d595a20-000bcd64",
                    "viewableGuid": "00cd2da3-fbfa-44a9-7a33-cad0bc4720cb"
                },
                {
                    "id": "12fcb372",
                    "urn": "urn:adsk.wipprod:fs.file:vf.DyTWutcvTcOLUNUARxcTzQ?version=4",
                    "is3d": true,
                    "viewableName": "New Construction",
                    "viewableId": "c884ae1b-61e7-4f9d-0001-719e20b22d0b-00120bb2",
                    "viewableGuid": "4a966c2a-ead6-65c3-4f98-273dd7543047"
                }
            ]
        }
    ],
    "errors": [],
    "stats": {
        "objects": 33097,
        "contentLength": 1881318
    }
}
Show Less
The structure of the manifest resource returned by this endpoint is described in the field guide page.

Step 4: (Optional) Download the fields
In order to query the index, download the fields resource, which describes the columns available in the index. The index fields are obtained by a call to the fieldsUrl returned either by a call to the batch status endpoint (Step 1) or by polling the state of a running indexing job (Step 2). If you already know the field keys you require for your query you can skip this step.

Example Request
curl --request GET 'https://developer.api.autodesk.com/construction/index/v2/projects/f83cef12-deef-4771-9feb-4f85643e3c46/indexes/qTmPiKJZ7siqxkTNpWGANw/fields' \
     --header 'Authorization: Bearer ****'
Example Response
{"key":"p153cb174","category":"__name__","type":"String","name":"name","uom":null}
{"key":"p74a9a490","category":"__document__","type":"String","name":"schema_name","uom":null}
{"key":"p137c14f2","category":"__document__","type":"String","name":"schema_version","uom":null}
{"key":"p1490bcea","category":"__document__","type":"Boolean","name":"is_doc_property","uom":null}
{"key":"p5eddc473","category":"__category__","type":"String","name":"Category","uom":null}
{"key":"p00723fa6","category":"Identity Data","type":"String","name":"Design Option","uom":null}
{"key":"pe8094f29","category":"Other","type":"String","name":"Project Issue Date","uom":null}
{"key":"p50756a0d","category":"Other","type":"String","name":"Client Name","uom":null}
{"key":"p32791eb0","category":"Other","type":"String","name":"Project Address","uom":null}
{"key":"pbf75ced9","category":"Other","type":"String","name":"Project Name","uom":null}
{"key":"p8213f1ad","category":"Other","type":"String","name":"Project Number","uom":null}
{"key":"pa7275c45","category":"__categoryId__","type":"Integer","name":"CategoryId","uom":null}
{"key":"p93e93af5","category":"__parent__","type":"DbKey","name":"parent","uom":null}
{"key":"pdf1348b1","category":"Constraints","type":"Double","name":"Elevation","uom":"ft"}
{"key":"p9513b772","category":"Constraints","type":"String","name":"Story Above","uom":null}
{"key":"p1d45bc4f","category":"Dimensions","type":"Double","name":"Computation Height","uom":"ft"}
{"key":"pe01bd7ef","category":"Extents","type":"String","name":"Scope Box","uom":null}
TRUNCATED
Show Less
The structure of the fields resource returned by this endpoint is described in the field guide page.

Step 5: (Optional) Download the raw index
While the indexing service is designed to run SQL-like queries targeting the fields contained within the indexes it hosts, it is possible to download raw indexes created by the service in their entirety. The raw index properties are obtained by a call to the propertiesUrl returned either by a call to the batch status endpoint (Step 1) or by polling the state of a running indexing job (Step 2).

Example Request
curl --request GET 'https://developer.api.autodesk.com/construction/index/v2/projects/f83cef12-deef-4771-9feb-4f85643e3c46/indexes/qTmPiKJZ7siqxkTNpWGANw/properties' \
     --header 'Authorization: Bearer ****'
Example Response
{"svf2Id":1,"lineageId":"a19f7db","externalId":"doc_4c0302d4-8355-4bba-aa3e-02ea475a867c","lmvId":1,"databaseId":"3747dccf","props":{"p00723fa6":"Main Model","p137c14f2":"1.0","p1490bcea":true,"p153cb174":"Model","p32791eb0":"Enter address here","p50756a0d":"AUDUBON OHIO","p5eddc473":"Revit Document","p74a9a490":"rvt","p8213f1ad":"1-06-444","pbf75ced9":"GRANGE INSURANCE AUDUBON CENTER","pe8094f29":"3-10-2008"},"propsHash":"16231084","views":[]}
{"svf2Id":2,"lineageId":"a19f7db","externalId":"b5c4b31f-321a-418d-a61a-0c8e326aa154-0003f50a","lmvId":2,"databaseId":"3747dccf","props":{"p00723fa6":"Main Model","p153cb174":"FOUNDATION PLAN","p1d45bc4f":0.0,"p5463fc28":false,"p5eddc473":"Revit Level","p5f2f196f":true,"p9513b772":"Default","pa7275c45":-2000240,"pdf1348b1":100.0,"pdf772b6f":"FOUNDATION PLAN","pe01bd7ef":"None"},"propsHash":"ca71d10d","propsIgnored":{"p93e93af5":1},"views":[]}
{"svf2Id":3,"lineageId":"a19f7db","externalId":"b5c4b31f-321a-418d-a61a-0c8e326aa154-0003f50b","lmvId":3,"databaseId":"3747dccf","props":{"p00723fa6":"Main Model","p153cb174":"BEARING","p1d45bc4f":0.0,"p5463fc28":false,"p5eddc473":"Revit Level","p5f2f196f":true,"p9513b772":"Default","pa7275c45":-2000240,"pdf1348b1":112.0,"pdf772b6f":"BEARING","pe01bd7ef":"None"},"propsHash":"4b5d70be","propsIgnored":{"p93e93af5":1},"views":[]}
{"svf2Id":4,"lineageId":"a19f7db","externalId":"b5c4b31f-321a-418d-a61a-0c8e326aa154-0003f50c","lmvId":4,"databaseId":"3747dccf","props":{"p00723fa6":"Main Model","p153cb174":"MEZZANINE","p1d45bc4f":0.0,"p5463fc28":false,"p5eddc473":"Revit Level","p5f2f196f":true,"p9513b772":"Default","pa7275c45":-2000240,"pdf1348b1":110.0,"pdf772b6f":"MEZZANINE","pe01bd7ef":"None"},"propsHash":"599fbb59","propsIgnored":{"p93e93af5":1},"views":[]}
{"svf2Id":5,"lineageId":"a19f7db","externalId":"0935d8b2-149b-4a0d-b816-863f0d595a20-000bcd64","lmvId":5,"databaseId":"3747dccf","props":{"p10c1a84a":false,"p114b1425":false,"p121ac73d":"Show Parts","p153cb174":"{3D}","p21b83ee9":1000.0,"p24044fbb":false,"p30015eee":"Medium","p31561b85":"None","p326e867f":99.66666666666666,"p345273d1":false,"p43766fd1":"96","p52413328":"By Discipline","p532f0ad6":"New Construction","p5eddc473":"Revit View","p79f5f88c":"Show All","p90dddb61":false,"p9ced1273":"{3D}","pa5fef29f":"all","pa7275c45":-2000279,"paea62326":"Adjusting","pb940b1a4":"Structural","pc2252206":"1/8\" = 1'-0\"","pd0d53a26":false,"pd45a2b8e":"Standard 3D Views","pe01bd7ef":"None","pe73257b1":"Independent","pf2c65ab9":271.2188634353403,"pfa32ecb1":"Orthographic","pfa463ea8":false},"propsHash":"64f41a52","propsIgnored":{"p93e93af5":1},"views":[]}
{"svf2Id":8,"lineageId":"a19f7db","externalId":"71cf8a75-c0d8-48db-b905-1eac3b6c8be7","lmvId":8,"databaseId":"3747dccf","props":{"p153cb174":"Phases","p20d8441e":"Phases","p5eddc473":"Revit Category"},"propsHash":"b9b0c2ee","propsIgnored":{"p93e93af5":1},"views":[]}
{"svf2Id":10,"lineageId":"a19f7db","externalId":"1513ee78-71c7-465f-9054-8ff932cfe1b9","lmvId":32,"databaseId":"3747dccf","props":{"p153cb174":"Materials","p20d8441e":"Materials","p5eddc473":"Revit Category"},"propsHash":"b1bec97b","propsIgnored":{"p93e93af5":1},"views":[]}
{"svf2Id":11,"lineageId":"a19f7db","externalId":"1d261fa6-2326-43bf-9ae8-b808ad2d3003","lmvId":320,"databaseId":"3747dccf","props":{"p153cb174":"Primary Contours","p20d8441e":"Primary Contours","p5eddc473":"Revit Category"},"propsHash":"6dbfc0eb","propsIgnored":{"p93e93af5":1},"views":[]}
{"svf2Id":12,"lineageId":"a19f7db","externalId":"31c7bc94-932d-411b-be66-433f5caf2c71","lmvId":529,"databaseId":"3747dccf","props":{"p153cb174":"Views","p20d8441e":"Views","p5eddc473":"Revit Category"},"propsHash":"d6fe53a3","propsIgnored":{"p93e93af5":1},"views":[]}
TRUNCATED
Show Less
Index rows are returned as compressed (gzip) line-delimited JSON. The following is an example viewable index row, formatted as a single JSON document to make reading the property description table below easier.

{
    "svf2Id": 68,
    "lineageId": "a19f7db",
    "externalId": "b5c4b31f-321a-418d-a61a-0c8e326aa154-0003f740",
    "lmvId": 2388,
    "databaseId": "3747dccf",
    "props": {
        "p00723fa6": "Main Model",
        "p09faf620": "HSS7X7X.250",
        "p0e507bbe": "None",
        "p13b6b3a0": "HSS7X7X.250",
        "p153cb174": "HSS-Hollow Structural Section-Column [259904]",
        "p188478f2": 0.485383241976329e0,
        "p20d8441e": "Structural Columns",
        "p2a0774a1": 0e0,
        "p30db51f9": "HSS-Hollow Structural Section-Column",
        "p34ed55db": "F-1.2",
        "p3c57b64e": "New Construction",
        "p54217060": "B10",
        "p5eddc473": "Revit Structural Columns",
        "p63ed81bb": "Superstructure",
        "p6637df3c": "Metal - Steel - ASTM A500 - Grade B - Rectangular and Square",
        "p69a0daab": 5833333333333334e-16,
        "p6aba1771": 0.01953125e0,
        "p751e1b21": true,
        "p773b5bd7": "Not Defined",
        "p801ffb64": 0.0390625e0,
        "p809920c7": "Square",
        "p953136d0": 0.04e0,
        "pa128dfb9": "Vertical",
        "pa57238c6": "Minimum Intersection",
        "pa7275c45": -2001330,
        "pa7456b2d": true,
        "pb5b8cef7": true,
        "pbadfe721": "BEARING",
        "pbb4f1bfe": "None",
        "pc2b858d6": 22.4e0,
        "pddd761c6": "FOUNDATION PLAN",
        "pe61a57c3": 0e0,
        "pee815a7f": "None",
        "pef87fde6": 0e0,
        "pf4ca60ab": 5833333333333334e-16,
        "pfa63d9d0": -9803431364364671e-16
    },
    "propsHash": "bcde34b3",
    "propsIgnored": {
        "p6a81eafd": 2386,
        "p93e93af5": 2387
    },
    "geomHash": "TCC2Cc9tvO4EVazM73O8BQ",
    "bboxMin": {
        "x": -1413565004170512e-13,
        "y": -5410244931321833e-14,
        "z": 10000000002097008e-14
    },
    "bboxMax": {
        "x": -14063352214982766e-14,
        "y": -53379471045994805e-15,
        "z": 11101965298365471e-14
    },
    "views": [
        "e7fda9d5",
        "12fcb372"
    ]
}
Show Less
The structure of the properties resource returned by this endpoint is described in the field guide page.

Step 6: Build and run a query
Once an index has been successfully created, it can be queried using the queries endpoint for the index via the indexId that can be obtained by a call to the index status tracking endpoints (Steps 1 or 2 above). Index queries are described using a custom JSON schema that is converted to a filter expression and applied line by line to the index. This documentation includes a comprehensive query language reference that describes how to form index and diff queries by example using this JSON schema.

Example Request
The query schema targets the structure of the JSON index rows. In the example POST to the queries endpoint below, only rows that have a views array with a count greater than 0 will be returned, i.e. only the rows in the index that are associated with a model element that can be viewed in the Viewer.

curl --request POST 'https://developer.api.autodesk.com/construction/index/v2/projects/f83cef12-deef-4771-9feb-4f85643e3c46/indexes/qTmPiKJZ7siqxkTNpWGANw/queries' \
     --header 'Authorization: Bearer ****' \
     --header 'Content-Type: application/json' \
     --data-raw '{
        "query": {
            "$gt": [{ "$count": "s.views" }, 0]
        }
     }'
Show More
Example Response
The response from the queries endpoint is very similar to the response from the index status endpoints. The only additional property returned by this endpoint is a queryId value. This queryId is a unique identifier for the query execution and can be used to poll the progress of the query job. As with index status operations, a query is successful when its state is set to FINISHED. Index queries also have the standard manifestUrl, fieldsUrl, and propertiesUrl values that point to the index resources used when performing the query. In addition the queries endpoint also returns a queryResultsUrl property that points to a gzip’d, line delimited JSON resource that contains the filtered index rows that match the query filter expression when the query reaches the FINISHED state.

{
    "projectId": "f83cef12-deef-4771-9feb-4f85643e3c46",
    "indexId": "qTmPiKJZ7siqxkTNpWGANw",
    "queryId": "1uqaSYj39pOIaAuQutmZpg",
    "type": "INDEX",
    "state": "RUNNING",
    "selfUrl": "https://developer.api.autodesk.com/construction/index/v2/projects/f83cef12-deef-4771-9feb-4f85643e3c46/indexes/qTmPiKJZ7siqxkTNpWGANw/queries/1uqaSYj39pOIaAuQutmZpg",
    "versionUrns": [
        "urn:adsk.wipprod:fs.file:vf.DyTWutcvTcOLUNUARxcTzQ?version=4"
    ],
    "updatedAt": "2021-08-23T08:42:38.6922628+00:00",
    "retryAt": "2021-08-27T14:45:12.6504394+00:00",
    "stats": null,
    "manifestUrl": null,
    "fieldsUrl": null,
    "propertiesUrl": null,
    "queryResultsUrl": null
}
Show More
Step 7: Poll for query progress
The index queries endpoint follows the same pattern as the status endpoint. The queryId obtained in the POST to the queries endpoint can be used to poll the progress of the query.

Example Request
In this example request the queryId and indexId from the previous Step (5) are used to poll the progress of the query.

curl --request GET 'https://developer.api.autodesk.com/construction/index/v2/projects/f83cef12-deef-4771-9feb-4f85643e3c46/indexes/qTmPiKJZ7siqxkTNpWGANw/queries/1uqaSYj39pOIaAuQutmZpg' \
     --header 'Authorization: Bearer ****'
Example Response
The response to this status GET is identical to the response returned by the POST to the queries endpoint. In the example below the query state is set to FINISHED and the queryResultsUrl is not null, indicating that the query has been completed successfully and the results are available for download.

{
    "projectId": "f83cef12-deef-4771-9feb-4f85643e3c46",
    "indexId": "qTmPiKJZ7siqxkTNpWGANw",
    "queryId": "1uqaSYj39pOIaAuQutmZpg",
    "type": "INDEX",
    "state": "FINISHED",
    "selfUrl": "https://developer.api.autodesk.com/construction/index/v2/projects/f83cef12-deef-4771-9feb-4f85643e3c46/indexes/qTmPiKJZ7siqxkTNpWGANw/queries/1uqaSYj39pOIaAuQutmZpg",
    "versionUrns": [
        "urn:adsk.wipprod:fs.file:vf.DyTWutcvTcOLUNUARxcTzQ?version=4"
    ],
    "updatedAt": "2021-08-23T08:42:38.6922628+00:00",
    "retryAt": "2021-08-27T14:47:59.2677745+00:00",
    "stats": {
        "objects": 6523
    },
    "manifestUrl": "https://developer.api.autodesk.com/construction/index/v2/projects/f83cef12-deef-4771-9feb-4f85643e3c46/indexes/qTmPiKJZ7siqxkTNpWGANw/manifest",
    "fieldsUrl": "https://developer.api.autodesk.com/construction/index/v2/projects/f83cef12-deef-4771-9feb-4f85643e3c46/indexes/qTmPiKJZ7siqxkTNpWGANw/fields",
    "propertiesUrl": "https://developer.api.autodesk.com/construction/index/v2/projects/f83cef12-deef-4771-9feb-4f85643e3c46/indexes/qTmPiKJZ7siqxkTNpWGANw/properties",
    "queryResultsUrl": "https://developer.api.autodesk.com/construction/index/v2/projects/f83cef12-deef-4771-9feb-4f85643e3c46/indexes/qTmPiKJZ7siqxkTNpWGANw/queries/1uqaSYj39pOIaAuQutmZpg/properties"
}
Show Less
Step 8: Download the query results
The final step in the process is to use the queryResultsUrl to download the index rows which match the submitted query expression. These line delimited JSON result rows are a sub-set of the property index rows and have exactly the same format.

Example Request
curl --request GET 'https://developer.api.autodesk.com/construction/index/v2/projects/f83cef12-deef-4771-9feb-4f85643e3c46/indexes/qTmPiKJZ7siqxkTNpWGANw/queries/1uqaSYj39pOIaAuQutmZpg/properties' \
     --header 'Authorization: Bearer ****'
Example Response
{"svf2Id":68,"lineageId":"a19f7db","externalId":"b5c4b31f-321a-418d-a61a-0c8e326aa154-0003f740","lmvId":2388,"databaseId":"3747dccf","props":{"p00723fa6":"Main Model","p09faf620":"HSS7X7X.250","p0e507bbe":"None","p13b6b3a0":"HSS7X7X.250","p153cb174":"HSS-Hollow Structural Section-Column [259904]","p188478f2":0.485383241976329e0,"p20d8441e":"Structural Columns","p2a0774a1":0e0,"p30db51f9":"HSS-Hollow Structural Section-Column","p34ed55db":"F-1.2","p3c57b64e":"New Construction","p54217060":"B10","p5eddc473":"Revit Structural Columns","p63ed81bb":"Superstructure","p6637df3c":"Metal - Steel - ASTM A500 - Grade B - Rectangular and Square","p69a0daab":5833333333333334e-16,"p6aba1771":0.01953125e0,"p751e1b21":true,"p773b5bd7":"Not Defined","p801ffb64":0.0390625e0,"p809920c7":"Square","p953136d0":0.04e0,"pa128dfb9":"Vertical","pa57238c6":"Minimum Intersection","pa7275c45":-2001330,"pa7456b2d":true,"pb5b8cef7":true,"pbadfe721":"BEARING","pbb4f1bfe":"None","pc2b858d6":22.4e0,"pddd761c6":"FOUNDATION PLAN","pe61a57c3":0e0,"pee815a7f":"None","pef87fde6":0e0,"pf4ca60ab":5833333333333334e-16,"pfa63d9d0":-9803431364364671e-16},"propsHash":"bcde34b3","propsIgnored":{"p6a81eafd":2386,"p93e93af5":2387},"geomHash":"TCC2Cc9tvO4EVazM73O8BQ","bbox":{"min":[-1413565004170512e-13,-5410244931321833e-14,10000000002097008e-14],"max":[-14063352214982766e-14,-53379471045994805e-15,11101965298365471e-14]},"views":["e7fda9d5","12fcb372"]}
{"svf2Id":69,"lineageId":"a19f7db","externalId":"b5c4b31f-321a-418d-a61a-0c8e326aa154-0003f742","lmvId":2389,"databaseId":"3747dccf","props":{"p00723fa6":"Main Model","p09faf620":"HSS7X7X.250","p0e507bbe":"None","p13b6b3a0":"HSS7X7X.250","p153cb174":"HSS-Hollow Structural Section-Column [259906]","p188478f2":5285644531249998e-16,"p20d8441e":"Structural Columns","p30db51f9":"HSS-Hollow Structural Section-Column","p34ed55db":"F-3","p3c57b64e":"New Construction","p54217060":"B10","p5eddc473":"Revit Structural Columns","p63ed81bb":"Superstructure","p6637df3c":"Metal - Steel - ASTM A500 - Grade B - Rectangular and Square","p69a0daab":5833333333333334e-16,"p6aba1771":0.01953125e0,"p773b5bd7":"Not Defined","p801ffb64":0.0390625e0,"p809920c7":"Square","p953136d0":0.04e0,"pa128dfb9":"Vertical","pa7275c45":-2001330,"pa7456b2d":true,"pb5b8cef7":true,"pbadfe721":"BEARING","pbb4f1bfe":"None","pc2b858d6":22.4e0,"pddd761c6":"FOUNDATION PLAN","pe61a57c3":0e0,"pee815a7f":"None","pef87fde6":0e0,"pf4ca60ab":5833333333333334e-16,"pfa63d9d0":0e0},"propsHash":"6f21f5ef","propsIgnored":{"p6a81eafd":2386,"p93e93af5":2387},"geomHash":"Yjh1a5R5k7OIuzFlup7U/A","bbox":{"min":[-11740090260815661e-14,-6244930357652374e-14,10000000002097008e-14],"max":[-11667791541749409e-14,-6172631768493561e-14,11199999966334221e-14]},"views":["e7fda9d5","12fcb372"]}
{"svf2Id":70,"lineageId":"a19f7db","externalId":"b5c4b31f-321a-418d-a61a-0c8e326aa154-0003f743","lmvId":2392,"databaseId":"3747dccf","props":{"p00723fa6":"Main Model","p09faf620":"HSS6X6X.1875","p0e507bbe":"None","p13b6b3a0":"HSS6X6X.1875","p153cb174":"HSS-Hollow Structural Section-Column [259907]","p188478f2":5622698018705423e-16,"p20d8441e":"Structural Columns","p30db51f9":"HSS-Hollow Structural Section-Column","p34ed55db":"A-7","p3c57b64e":"New Construction","p54217060":"B10","p5eddc473":"Revit Structural Columns","p63ed81bb":"Superstructure","p6637df3c":"Metal - Steel - ASTM A500 - Grade B - Rectangular and Square","p69a0daab":0.5e0,"p6aba1771":0.0146484375e0,"p773b5bd7":"Not Defined","p801ffb64":0.029296875e0,"p809920c7":"Square","p953136d0":0.03e0,"pa128dfb9":"Vertical","pa7275c45":-2001330,"pa7456b2d":true,"pb5b8cef7":true,"pbadfe721":"BEARING","pbb4f1bfe":"None","pc2b858d6":14.5e0,"pddd761c6":"FOUNDATION PLAN","pe61a57c3":0e0,"pee815a7f":"None","pef87fde6":0e0,"pf4ca60ab":0.5e0,"pfa63d9d0":7771382285923252e-15},"propsHash":"ca9845fe","propsIgnored":{"p6a81eafd":2390,"p93e93af5":2391},"geomHash":"KzBnTTzXjGBfEq4yR8VtzA","bbox":{"min":[-4067314124452854e-14,7.05652589540108e0,10000000002097008e-14],"max":[-40025658785271645e-15,7704008354657972e-15,1197713848562133e-13]},"views":["e7fda9d5","12fcb372"]}
{"svf2Id":71,"lineageId":"a19f7db","externalId":"b5c4b31f-321a-418d-a61a-0c8e326aa154-0003f744","lmvId":2393,"databaseId":"3747dccf","props":{"p00723fa6":"Main Model","p09faf620":"HSS6X6X.1875","p0e507bbe":"None","p13b6b3a0":"HSS6X6X.1875","p153cb174":"HSS-Hollow Structural Section-Column [259908]","p188478f2":5260619140289455e-16,"p20d8441e":"Structural Columns","p2a0774a1":0e0,"p30db51f9":"HSS-Hollow Structural Section-Column","p34ed55db":"A-8","p3c57b64e":"New Construction","p54217060":"B10","p5eddc473":"Revit Structural Columns","p63ed81bb":"Superstructure","p6637df3c":"Metal - Steel - ASTM A500 - Grade B - Rectangular and Square","p69a0daab":0.5e0,"p6aba1771":0.0146484375e0,"p751e1b21":true,"p773b5bd7":"Not Defined","p801ffb64":0.029296875e0,"p809920c7":"Square","p953136d0":0.03e0,"pa128dfb9":"Vertical","pa57238c6":"Minimum Intersection","pa7275c45":-2001330,"pa7456b2d":true,"pb5b8cef7":true,"pbadfe721":"BEARING","pbb4f1bfe":"None","pc2b858d6":14.5e0,"pddd761c6":"FOUNDATION PLAN","pe61a57c3":0e0,"pee815a7f":"None","pef87fde6":0e0,"pf4ca60ab":0.5e0,"pfa63d9d0":6498185699693238e-15},"propsHash":"d295b8c2","propsIgnored":{"p6a81eafd":2390,"p93e93af5":2391},"geomHash":"sKxntR3859ILOVn7pKKhIQ","bbox":{"min":[-23.9879046768966e0,12428865208033102e-16,10000000002097008e-14],"max":[-2334041855459337e-14,18903700449577627e-16,11849818386744377e-14]},"views":["e7fda9d5","12fcb372"]}
{"svf2Id":72,"lineageId":"a19f7db","externalId":"b5c4b31f-321a-418d-a61a-0c8e326aa154-0003f748","lmvId":2396,"databaseId":"3747dccf","props":{"p00723fa6":"Main Model","p09faf620":"HSS4X4X.1875","p0e507bbe":"None","p13b6b3a0":"HSS4X4X.1875","p153cb174":"HSS-Hollow Structural Section-Column [259912]","p188478f2":26921418830460175e-17,"p20d8441e":"Structural Columns","p30db51f9":"HSS-Hollow Structural Section-Column","p34ed55db":"F-13.8","p3c57b64e":"New Construction","p54217060":"B10","p5eddc473":"Revit Structural Columns","p63ed81bb":"Superstructure","p6637df3c":"Metal - Steel - ASTM A500 - Grade B - Rectangular and Square","p69a0daab":3333333333333333e-16,"p6aba1771":0.0146484375e0,"p773b5bd7":"Not Defined","p801ffb64":0.029296875e0,"p809920c7":"Square","p953136d0":0.02e0,"pa128dfb9":"Vertical","pa7275c45":-2001330,"pa7456b2d":true,"pb5b8cef7":true,"pbadfe721":"BEARING","pbb4f1bfe":"None","pc2b858d6":9.4e0,"pddd761c6":"FOUNDATION PLAN","pe61a57c3":0e0,"pee815a7f":"None","pef87fde6":0e0,"pf4ca60ab":3333333333333333e-16,"pfa63d9d0":2417340996715339e-15},"propsHash":"8b568853","propsIgnored":{"p6a81eafd":2394,"p93e93af5":2395},"geomHash":"cAWPEx2yBSeJGrInzF1/aw","bbox":{"min":[-5372055725666179e-15,-10128624040894114e-14,10000000002097008e-14],"max":[-4941667181569901e-15,-10085585121530767e-14,11441734280299065e-14]},"views":["e7fda9d5","12fcb372"]}
{"svf2Id":73,"lineageId":"a19f7db","externalId":"b5c4b31f-321a-418d-a61a-0c8e326aa154-0003f749","lmvId":2397,"databaseId":"3747dccf","props":{"p00723fa6":"Main Model","p09faf620":"HSS6X6X.1875","p0e507bbe":"None","p13b6b3a0":"HSS6X6X.1875","p153cb174":"HSS-Hollow Structural Section-Column [259913]","p188478f2":4100085339756494e-16,"p20d8441e":"Structural Columns","p30db51f9":"HSS-Hollow Structural Section-Column","p34ed55db":"F-12","p3c57b64e":"New Construction","p54217060":"B10","p5eddc473":"Revit Structural Columns","p63ed81bb":"Superstructure","p6637df3c":"Metal - Steel - ASTM A500 - Grade B - Rectangular and Square","p69a0daab":0.5e0,"p6aba1771":0.0146484375e0,"p773b5bd7":"Not Defined","p801ffb64":0.029296875e0,"p809920c7":"Square","p953136d0":0.03e0,"pa128dfb9":"Vertical","pa7275c45":-2001330,"pa7456b2d":true,"pb5b8cef7":true,"pbadfe721":"BEARING","pbb4f1bfe":"None","pc2b858d6":14.5e0,"pddd761c6":"FOUNDATION PLAN","pe61a57c3":0e0,"pee815a7f":"None","pef87fde6":0e0,"pf4ca60ab":0.5e0,"pfa63d9d0":24173409967153106e-16},"propsHash":"5c430fc7","propsIgnored":{"p6a81eafd":2390,"p93e93af5":2391},"geomHash":"Ef2OUDgFZDndJH9a648+6w","bbox":{"min":[-2751472931099257e-14,-9371743688325377e-14,10000000002097008e-14],"max":[-2686724540352532e-14,-9306995232624932e-14,11441734280299065e-14]},"views":["e7fda9d5","12fcb372"]}
{"svf2Id":74,"lineageId":"a19f7db","externalId":"b5c4b31f-321a-418d-a61a-0c8e326aa154-0003f74a","lmvId":2398,"databaseId":"3747dccf","props":{"p00723fa6":"Main Model","p09faf620":"HSS6X6X.1875","p0e507bbe":"None","p13b6b3a0":"HSS6X6X.1875","p153cb174":"HSS-Hollow Structural Section-Column [259914]","p188478f2":4135579583143538e-16,"p20d8441e":"Structural Columns","p30db51f9":"HSS-Hollow Structural Section-Column","p34ed55db":"E-3","p3c57b64e":"New Construction","p54217060":"B10","p5eddc473":"Revit Structural Columns","p63ed81bb":"Superstructure","p6637df3c":"Metal - Steel - ASTM A500 - Grade B - Rectangular and Square","p69a0daab":0.5e0,"p6aba1771":0.0146484375e0,"p773b5bd7":"Not Defined","p801ffb64":0.029296875e0,"p809920c7":"Square","p953136d0":0.03e0,"pa128dfb9":"Vertical","pa7275c45":-2001330,"pa7456b2d":true,"pb5b8cef7":true,"pbadfe721":"BEARING","pbb4f1bfe":"None","pc2b858d6":14.5e0,"pddd761c6":"FOUNDATION PLAN","pe61a57c3":0e0,"pee815a7f":"None","pef87fde6":0e0,"pf4ca60ab":0.5e0,"pfa63d9d0":25421512306314895e-16},"propsHash":"fcb8d37a","propsIgnored":{"p6a81eafd":2390,"p93e93af5":2391},"geomHash":"aUZjfH/wOI8ffqpcAzQcxw","bbox":{"min":[-11164540474581231e-14,-4277749229053744e-14,10000000002097008e-14],"max":[-11102570368482772e-14,-4215779122955284e-14,11454215206812736e-14]},"views":["e7fda9d5","12fcb372"]}
{"svf2Id":75,"lineageId":"a19f7db","externalId":"b5c4b31f-321a-418d-a61a-0c8e326aa154-0003f74b","lmvId":2399,"databaseId":"3747dccf","props":{"p00723fa6":"Main Model","p09faf620":"HSS6X6X.1875","p0e507bbe":"None","p13b6b3a0":"HSS6X6X.1875","p153cb174":"HSS-Hollow Structural Section-Column [259915]","p188478f2":41000853397562853e-17,"p20d8441e":"Structural Columns","p30db51f9":"HSS-Hollow Structural Section-Column","p34ed55db":"F-9","p3c57b64e":"New Construction","p54217060":"B10","p5eddc473":"Revit Structural Columns","p63ed81bb":"Superstructure","p6637df3c":"Metal - Steel - ASTM A500 - Grade B - Rectangular and Square","p69a0daab":0.5e0,"p6aba1771":0.0146484375e0,"p773b5bd7":"Not Defined","p801ffb64":0.029296875e0,"p809920c7":"Square","p953136d0":0.03e0,"pa128dfb9":"Vertical","pa7275c45":-2001330,"pa7456b2d":true,"pb5b8cef7":true,"pbadfe721":"BEARING","pbb4f1bfe":"None","pc2b858d6":14.5e0,"pddd761c6":"FOUNDATION PLAN","pe61a57c3":0e0,"pee815a7f":"None","pef87fde6":0e0,"pf4ca60ab":0.5e0,"pfa63d9d0":24173409967152963e-16},"propsHash":"81b2febb","propsIgnored":{"p6a81eafd":2390,"p93e93af5":2391},"geomHash":"5aq5RLee7AB70heqgw2t9g","bbox":{"min":[-5065056277327119e-14,-8565621912069254e-14,10000000002097008e-14],"max":[-50.0030803140143e0,-8500873666143565e-14,11441734280299065e-14]},"views":["e7fda9d5","12fcb372"]}
{"svf2Id":76,"lineageId":"a19f7db","externalId":"b5c4b31f-321a-418d-a61a-0c8e326aa154-0003f74c","lmvId":2400,"databaseId":"3747dccf","props":{"p00723fa6":"Main Model","p09faf620":"HSS6X6X.1875","p0e507bbe":"None","p13b6b3a0":"HSS6X6X.1875","p153cb174":"HSS-Hollow Structural Section-Column [259916]","p188478f2":0.410008533679623e0,"p20d8441e":"Structural Columns","p30db51f9":"HSS-Hollow Structural Section-Column","p34ed55db":"F-6","p3c57b64e":"New Construction","p54217060":"B10","p5eddc473":"Revit Structural Columns","p63ed81bb":"Superstructure","p6637df3c":"Metal - Steel - ASTM A500 - Grade B - Rectangular and Square","p69a0daab":0.5e0,"p6aba1771":0.0146484375e0,"p773b5bd7":"Not Defined","p801ffb64":0.029296875e0,"p809920c7":"Square","p953136d0":0.03e0,"pa128dfb9":"Vertical","pa7275c45":-2001330,"pa7456b2d":true,"pb5b8cef7":true,"pbadfe721":"BEARING","pbb4f1bfe":"None","pc2b858d6":14.5e0,"pddd761c6":"FOUNDATION PLAN","pe61a57c3":0e0,"pee815a7f":"None","pef87fde6":0e0,"pf4ca60ab":0.5e0,"pfa63d9d0":2417340986305419e-15},"propsHash":"2e8116ef","propsIgnored":{"p6a81eafd":2390,"p93e93af5":2391},"geomHash":"yR0kW3rbrpd8Lqpxsvx8Ng","bbox":{"min":[-7378639425489068e-14,-7759499822753376e-14,10000000002097008e-14],"max":[-7313891179563379e-14,-7694751576827687e-14,11441734280299065e-14]},"views":["e7fda9d5","12fcb372"]}
{"svf2Id":77,"lineageId":"a19f7db","externalId":"b5c4b31f-321a-418d-a61a-0c8e326aa154-0003f750","lmvId":2401,"databaseId":"3747dccf","props":{"p00723fa6":"Main Model","p09faf620":"HSS6X6X.1875","p0e507bbe":"None","p13b6b3a0":"HSS6X6X.1875","p153cb174":"HSS-Hollow Structural Section-Column [259920]","p188478f2":0.413755448370708e0,"p20d8441e":"Structural Columns","p30db51f9":"HSS-Hollow Structural Section-Column","p34ed55db":"E-1","p3c57b64e":"New Construction","p54217060":"B10","p5eddc473":"Revit Structural Columns","p63ed81bb":"Superstructure","p6637df3c":"Metal - Steel - ASTM A500 - Grade B - Rectangular and Square","p69a0daab":0.5e0,"p6aba1771":0.0146484375e0,"p773b5bd7":"Not Defined","p801ffb64":0.029296875e0,"p809920c7":"Square","p953136d0":0.03e0,"pa128dfb9":"Vertical","pa7275c45":-2001330,"pa7456b2d":true,"pb5b8cef7":true,"pbadfe721":"BEARING","pbb4f1bfe":"None","pc2b858d6":14.5e0,"pddd761c6":"FOUNDATION PLAN","pe61a57c3":0e0,"pee815a7f":"None","pef87fde6":0e0,"pf4ca60ab":0.5e0,"pfa63d9d0":25490956750758897e-16},"propsHash":"bc834fe3","propsIgnored":{"p6a81eafd":2390,"p93e93af5":2391},"geomHash":"m1uJ9gbzWIwZ0Y/RHTL3ww","bbox":{"min":[-13827222772628218e-14,-3503671150408979e-14,10000000002097008e-14],"max":[-1376525266652976e-13,-34417010443105184e-15,1145490948171508e-13]},"views":["e7fda9d5","12fcb372"]}
{"svf2Id":78,"lineageId":"a19f7db","externalId":"b5c4b31f-321a-418d-a61a-0c8e326aa154-0003f751","lmvId":2402,"databaseId":"3747dccf","props":{"p00723fa6":"Main Model","p09faf620":"HSS6X6X.1875","p0e507bbe":"None","p13b6b3a0":"HSS6X6X.1875","p153cb174":"HSS-Hollow Structural Section-Column [259921]","p188478f2":34126281738281244e-17,"p20d8441e":"Structural Columns","p30db51f9":"HSS-Hollow Structural Section-Column","p34ed55db":"B-10","p3c57b64e":"New Construction","p54217060":"B10","p5eddc473":"Revit Structural Columns","p63ed81bb":"Superstructure","p6637df3c":"Metal - Steel - ASTM A500 - Grade B - Rectangular and Square","p69a0daab":0.5e0,"p6aba1771":0.0146484375e0,"p773b5bd7":"Not Defined","p801ffb64":0.029296875e0,"p809920c7":"Square","p953136d0":0.03e0,"pa128dfb9":"Vertical","pa7275c45":-2001330,"pa7456b2d":true,"pb5b8cef7":true,"pbadfe721":"BEARING","pbb4f1bfe":"None","pc2b858d6":14.5e0,"pddd761c6":"FOUNDATION PLAN","pe61a57c3":0e0,"pee815a7f":"None","pef87fde6":0e0,"pf4ca60ab":0.5e0,"pfa63d9d0":0e0},"propsHash":"4d9b58db","propsIgnored":{"p6a81eafd":2390,"p93e93af5":2391},"geomHash":"N427c0D7TagBJXgRhaOOng","bbox":{"min":[-23171833458388303e-15,-2024642145398657e-14,10000000002097008e-14],"max":[-22.5521323974037e0,-19626720393001968e-15,11199999966334221e-14]},"views":["e7fda9d5","12fcb372"]}
TRUNCATED

Documentation /Autodesk Construction Cloud APIs /How-to Guide
Relationship Querying
The Relationship Service is used in BIM 360 to link entities across domains. The following document assumes the reader is familiar with the concept of domain entity linking. If you have not already done so refer to Relationship Service Field Guide which explains the concepts underpinning the relationship service.

Relationship Domain and Entity Types
It is important to note that the entity types returned from the relationship service may not yet be accessible via a public BIM 360 APIs. These identifiers can still be used to construct URL-based deep links back to the appropriate BIM 360 application module user experience. This is a useful feature for developers building bespoke 3LO web user experiences against the BIM 360 API.

Example Deep-Link Page URLs
Open the Assets module and display a specific Asset :-

https://assets.b360.autodesk.com/projects/<YOUR PROJECT GUID>/assets?preview=<RELATIONSHIP SERVICE ENTITY ID>
Open the Project Management module and display a specific Meeting :-

https://meetings.b360.autodesk.com/projects/<YOUR PROJECT GUID>/meetings/<RELATIONSHIP SERVICE ENTITY ID>
BIM 360 API Supported Relationship Service Entity Types
The following table lists Domains and Entity Types currently supported by the Relationship Service which are also available via a BIM 360 API.

Domain	Entity Type	BIM 360 Module
autodesk-bim360-asset	asset	Assets
autodesk-bim360-asset	category	Assets
autodesk-bim360-checklist	checklist	Field Management
autodesk-bim360-checklist	checklisttemplate	Field Management
autodesk-bim360-cost	budget	Cost Management
autodesk-bim360-cost	budgetpayment	Cost Management
autodesk-bim360-cost	contract	Cost Management
autodesk-bim360-cost	costpayment	Cost Management
autodesk-bim360-cost	maincontract	Cost Management
autodesk-bim360-cost	oco	Cost Management
autodesk-bim360-cost	pco	Cost Management
autodesk-bim360-cost	rco	Cost Management
autodesk-bim360-cost	rfq	Cost Management
autodesk-bim360-cost	sco	Cost Management
autodesk-bim360-documentmanagement	documentlineage	Document Management
autodesk-bim360-documentmanagement	documentversion	Document Management
autodesk-bim360-documentmanagement	filelineage	Document Management
autodesk-bim360-documentmanagement	fileversion	Document Management
autodesk-bim360-issue	collaboration	Various
autodesk-bim360-issue	coordination	Various
autodesk-bim360-issue	design	Various
autodesk-bim360-issue	issue	Various
autodesk-bim360-issue	quality	Various
autodesk-bim360-modelcoordination	clashgroup	Model Coordination
autodesk-bim360-modelcoordination	container	Model Coordination
autodesk-bim360-modelcoordination	documentlineage	Model Coordination
autodesk-bim360-modelcoordination	scope	Model Coordination
autodesk-bim360-rfi	rfi	Project Management
Additional Relationship Service Entity Types
The following table lists Domains and Entity Types currently supported by the Relationship Service which are not yet available via a BIM 360 API.

Domain	Entity Type	BIM 360 Module
autodesk-bim360-locations	location	Various
autodesk-bim360-markup	markup	Various
autodesk-bim360-meetingminutes	meeting	Project Management
autodesk-bim360-meetingminutes	meetingitem	Project Management
Get Relationships by ID
The get relationship by unique ID endpoint is used to retrieve a relationship given its GUID unique ID. This endpoint is only typically useful if you have previously cached the IDs of relationships from a search query (see below).

Example Request
curl -v 'https://developer.api.autodesk.com/bim360/relationship/v2/containers/04074497-ed5d-4ea3-861d-1f146418f5bb/relationships/b544a7eb-3c64-4a56-a7ff-392d0441015f'
     -H 'Authorization: Bearer <token>'
Example Response
{
    "id": "b544a7eb-3c64-4a56-a7ff-392d0441015f",
    "createdOn": "2015-10-21T16:32:22Z",
    "isReadOnly": true,
    "isService": false,
    "isDeleted": false,
    "entities": [
        {
            "createdOn": "2015-10-21T16:32:22Z",
            "domain": "autodesk-bim360-asset",
            "type": "asset",
            "id": "b1d1e7d4-f0ed-11e9-81b4-2a2ae2dbcce4"
        },
        {
            "createdOn": "2015-10-21T16:32:22Z",
            "domain": "autodesk-bim360-issue",
            "type": "issue",
            "id": "92d6bb28-9c5c-424a-8b29-6d847542fa7f"
        }
    ]
}
Show Less
In the case of this example the relationship ID b544a7eb-3c64-4a56-a7ff-392d0441015f corresponds to an association between an Asset and an Issue.

Get Relationship Batch
The relationship batch endpoint can be used to retrieve a set of relationships using their unique GUID IDs. This endpoint is only typically useful if you have previously cached the IDs of relationships from a search query (see below).

Example Request
curl -v 'https://developer.api.autodesk.com/bim360/relationship/v2/containers/04074497-ed5d-4ea3-861d-1f146418f5bb/relationships:batch' \
     -X POST \
     -H 'Authorization: Bearer <token>' \
     -H 'Content-Type: application/json' \
     -d '[
           "d98c1dd4-008f-04b2-e980-0998ecf8427e",
           "b544a7eb-3c64-4a56-a7ff-392d0441015f"
         ]'
Show Less
Example Response
[
    {
        "id": "d98c1dd4-008f-04b2-e980-0998ecf8427e",
        "createdOn": "2015-10-21T16:32:22Z",
        "isReadOnly": true,
        "isService": false,
        "isDeleted": false,
        "entities": [
            {
                "createdOn": "2015-10-21T16:32:22Z",
                "domain": "autodesk-bim360-asset ",
                "type": "asset",
                "id": "b43e4bb3-0223-430d-bc2c-2adfdf3c629f"
            },
            {
                "createdOn": "2015-10-21T16:32:22Z",
                "domain": "autodesk-bim360-issue",
                "type": "issue",
                "id": "b625c02e-52c8-4a64-9874-8a5195f1de6c"
            }
        ]
    },
    {
        "id": "b544a7eb-3c64-4a56-a7ff-392d0441015f",
        "createdOn": "2015-10-21T16:32:22Z",
        "isReadOnly": true,
        "isService": false,
        "isDeleted": false,
        "entities": [
            {
                "createdOn": "2015-10-21T16:32:22Z",
                "domain": "autodesk-bim360-asset",
                "type": "asset",
                "id": "b1d1e7d4-f0ed-11e9-81b4-2a2ae2dbcce4"
            },
            {
                "createdOn": "2015-10-21T16:32:22Z",
                "domain": "autodesk-bim360-issue",
                "type": "issue",
                "id": "92d6bb28-9c5c-424a-8b29-6d847542fa7f"
            }
        ]
    }
]
Show Less
Relationship Search vs. Intersect
Whilst superficially similar, the relationship search and intersect endpoints have been designed to serve two very different use cases. When choosing between search and intersect it is important to remember the relationship domain entity model is hierarchical whilst considering what you are trying to achieve. To recap, a domain can have many entity types and for any given domain entity type there can be one or more instances of this type in the domain, represented by the ID of the instance.

../../../_images/domain-relationships.png
Both the search and intersect endpoints contain an implicit assumption that users understand the existence of this hierarchy. If searching for relationships to a specific entity the assumption holds that the user will supply not only the entity’s ID but also it’s entity type and domain. Likewise when searching for relationships to specific entity types (omitting an ID) the assumption holds that the user will supply not only the entity type but also the domain. The domain is at the top of the hierarchy so no supplementary qualification is required when searching for relationships to domains.

The search endpoint is a GET method requiring users to supply search criteria which will be used to match either end of the relationships stored for the project. For example, it can be used to search for all the relationships between (with) the issues domain and asset entity types in the assets domain. By further qualifying the search we can retrieve relationships between coordination issues types in the issues domain and asset entity types in the assets domain. Finally we can specify a specific entity instance and intersect it with either a domain, entity type and domain or another fully qualified entity.

By contrast the intersect endpoint makes more specific starting assumptions about the nature of the search you are performing. Unlike the search endpoint the intersect endpoint requires users to POST a set of fully qualified domain entities (domain, entity type and id) along with a domain, domain and entity type or a second set of fully qualified domain entities. The intersect endpoint literally intersects these two sets with the relationships in the system. This endpoint has been specifically designed to support paged workflows where the requirement is to efficiently find entities related to a starting fixed set of known entities. For example suppose you have queried the BIM 360 issues service and are paging through the resulting issues returned by the service. You can use the intersect endpoint to pass in batches of issues and query the things (entities) these issues are related to. You may restrict this query to intersect specific domains, domain and entity types or a second set of specific entities. For example to determine if the issues returned from the issues service were associated with assets you would restrict the intersection to the asset entity type in the assets domain.

Search Relationships
The relationship search endpoint can be used to retrieve relationships using the domain, entity type and id hierarchy implicit in the relationship service’s data model. The search endpoint uses the domain, type, id, withDomain, withType and withId query parameters to control the search endpoint’s behaviour. Deleted relationships will only be returned if the includeDeleted query parameter is set to true. Remember the importance of supplying fully qualified search qualifiers domain+entityType+id, domain+entityType or domain on either side of the search.

Example Request
In this request we are searching for relationships which exists between the issue entity type in the issues domain and the asset entity type in the assets domain which were created between a specific date range, we have also optionally chosen to include deleted relationships in this search.

curl -v 'https://developer.api.autodesk.com/bim360/relationship/v2/containers/04074497-ed5d-4ea3-861d-1f146418f5bb/relationships:search?domain=autodesk-bim360-issue&type=issue&createdAfter=2015-10-21T16%3a32%3a21Z&createdBefore=2015-10-21T16%3a30%3a45Z&withDomain=autodesk-bim360-asset&withType=asset&includeDeleted=True&pageLimit=20' \
     -H 'Authorization: Bearer <token>'
Example Response
{
    "page": {
        "continuationToken": "10",
        "syncToken": "eyAibGFzdENoZWNrZWQiOiIyMDE5LTEwLTE4VDEyOjEwOjA3Ljc5NloiIH0="
    },
    "relationships": [
        {
            "id": "d98c1dd4-008f-04b2-e980-0998ecf8427e",
            "createdOn": "2015-10-21T16:32:22Z",
            "isReadOnly": true,
            "isService": false,
            "isDeleted": false,
            "entities": [
                {
                    "createdOn": "2015-10-21T16:32:22Z",
                    "domain": "autodesk-bim360-asset ",
                    "type": "asset",
                    "id": "b43e4bb3-0223-430d-bc2c-2adfdf3c629f"
                },
                {
                    "createdOn": "2015-10-21T16:32:22Z",
                    "domain": "autodesk-bim360-issue",
                    "type": "issue",
                    "id": "b625c02e-52c8-4a64-9874-8a5195f1de6c"
                }
            ]
        },
        {
            "id": "b544a7eb-3c64-4a56-a7ff-392d0441015f",
            "createdOn": "2015-10-21T16:32:22Z",
            "isReadOnly": true,
            "isService": false,
            "isDeleted": false,
            "entities": [
                {
                    "createdOn": "2015-10-21T16:32:22Z",
                    "domain": "autodesk-bim360-asset",
                    "type": "asset",
                    "id": "b1d1e7d4-f0ed-11e9-81b4-2a2ae2dbcce4"
                },
                {
                    "createdOn": "2015-10-21T16:32:22Z",
                    "domain": "autodesk-bim360-issue",
                    "type": "issue",
                    "id": "92d6bb28-9c5c-424a-8b29-6d847542fa7f"
                }
            ]
        }
    ]
}
Show Less
Intersect Relationships
The relationship intersection endpoint is similar to the relationship search endpoint in that it allows callers to control the domains and entity types which are being queried. The intersection endpoint however takes things one step further in that it requires users to pass a set of entities and then intersect these entities with other domains and entity types. Callers POST two collections of domain entities , entities which must be fully specified (Domain, Entity and Entity ID) and a second collection withEntities which can be fully or partially specified. In the following example four BIM 360 assets are passed in the entities collection and the withEntities collection is used to request relationships which contain these assets and links to any issues or photos associated with these assets.

Example Request
In this example we have a set of asset entities from the assets domain and we are intersecting this set of entities with the issues domain to find issues which are related to the assets passed in the entities collection.

curl -v 'https://developer.api.autodesk.com/bim360/relationship/v2/containers/04074497-ed5d-4ea3-861d-1f146418f5bb/relationships:intersect' \
     -X POST \
     -H 'Authorization: Bearer <token>' \
     -H 'Content-Type: application/json' \
     -d '{
           "entities": [
             {
               "domain": "autodesk-bim360-asset",
               "type": "asset",
               "id": "b1d1e7d4-f0ed-11e9-81b4-2a2ae2dbcce4"
             },
             {
               "domain": "autodesk-bim360-asset",
               "type": "asset",
               "id": "8d7b691a-6631-4ea0-af7b-df9e2e3922c5"
             },
             {
               "domain": "autodesk-bim360-asset",
               "type": "asset",
               "id": "fb86ee43-e920-476f-908e-33da70c66551"
             },
             {
               "domain": "autodesk-bim360-asset",
               "type": "asset",
               "id": "a2303c73-5460-42f8-9ec8-089d2aecc6b3"
             }
           ],
           "withEntities": [
             {
               "domain": "autodesk-bim360-issue",
               "type": "issue"
             }
           ]
         }'
Show Less
Example Response
{
    "page": {
        "continuationToken": null,
        "syncToken": "eyAibGFzdENoZWNrZWQiOiIyMDE5LTEwLTE4VDEyOjEwOjA3Ljc5NloiIH0="
    },
    "relationships": [
        {
            "id": "d98c1dd4-008f-04b2-e980-0998ecf8427e",
            "createdOn": "2015-10-21T16:32:22Z",
            "isReadOnly": true,
            "isService": false,
            "isDeleted": false,
            "entities": [
                {
                    "createdOn": "2015-10-21T16:32:22Z",
                    "domain": "autodesk-bim360-asset ",
                    "type": "asset",
                    "id": "b1d1e7d4-f0ed-11e9-81b4-2a2ae2dbcce4"
                },
                {
                    "createdOn": "2015-10-21T16:32:22Z",
                    "domain": "autodesk-bim360-issue",
                    "type": "issue",
                    "id": "b625c02e-52c8-4a64-9874-8a5195f1de6c"
                }
            ]
        },
        {
            "id": "b544a7eb-3c64-4a56-a7ff-392d0441015f",
            "createdOn": "2015-10-21T16:32:22Z",
            "isReadOnly": true,
            "isService": false,
            "isDeleted": false,
            "entities": [
                {
                    "createdOn": "2015-10-21T16:32:22Z",
                    "domain": "autodesk-bim360-asset",
                    "type": "asset",
                    "id": "a2303c73-5460-42f8-9ec8-089d2aecc6b3"
                },
                {
                    "createdOn": "2015-10-21T16:32:22Z",
                    "domain": "autodesk-bim360-issue",
                    "type": "issue",
                    "id": "92d6bb28-9c5c-424a-8b29-6d847542fa7f"
                }
            ]
        }
    ]
}
Show Less
In the response above only two assets in the request are returned. This indicates that only these two assets have a connection to an Issue or Photo, the other two assets did not have any relationships to Issues or Photos.

Relationship Sync
The relationship service supports full data synchronisation via the relationship sync endpoint. This endpoint allows callers to replicate ALL of the relationships stored in the relationship service to an external repository. After relationships have been initially replicated subsequent calls to the the sync endpoint can be used to discover changes which have occurred between the time the initial synchronisation ended and “now”.

Bootstrapping Sync with no syncToken
Calling the relationship sync endpoint with no initial syncToken will result in a full download of all the relationships currently in the system.

curl -v 'https://developer.api.autodesk.com/bim360/relationship/v2/containers/04074497-ed5d-4ea3-861d-1f146418f5bb/relationships:sync' \
     -X POST \
     -H 'Authorization: Bearer <token>' \
     -H 'Content-Type: application/json' \
     -d '{
        "syncToken": null,
        "filters": null
     }'
Show Less
Calling Sync with a syncToken
Calling the relationship sync endpoint with a syncToken will result in a full download of all the relationships which have changed (been added to the service or deleted) since the initial call which yielded the syncToken passed in the request. The relationship search endpoint and the relationship intersection endpoint both return syncTokens in the page header in their responses. These syncTokens can be passed to the relationship sync endpoint to limit the scope of the synchronisation. For example if a syncToken from a filtered search is used then the relationships downloaded will be restricted by the same search criteria used in the search request.

curl -v 'https://developer.api.autodesk.com/bim360/relationship/v2/containers/04074497-ed5d-4ea3-861d-1f146418f5bb/relationships:sync' \
     -X POST \
     -H 'Authorization: Bearer <token>' \
     -H 'Content-Type: application/json' \
     -d '{
        "syncToken": "eyAibGFzdENoZWNrZWQiOiIyMDE5LTEwLTE4VDEyOjEwOjA3Ljc5NloiIH0=",
        "filters": null
     }'
Show Less
Sync Token Response
{
    "current": {
        "data": [
            {
                "id": "d98c1dd4-008f-04b2-e980-0998ecf8427e",
                "createdOn": "2015-10-21T16:32:22Z",
                "isReadOnly": true,
                "isService": false,
                "isDeleted": false,
                "entities": [
                    {
                        "createdOn": "2015-10-21T16:32:22Z",
                        "domain": "autodesk-bim360-asset ",
                        "type": "asset",
                        "id": "b1d1e7d4-f0ed-11e9-81b4-2a2ae2dbcce4"
                    },
                    {
                        "createdOn": "2015-10-21T16:32:22Z",
                        "domain": "autodesk-bim360-issue",
                        "type": "issue",
                        "id": "b625c02e-52c8-4a64-9874-8a5195f1de6c"
                    }
                ]
            }
        ]
    },
    "deleted": {
        "data": [
            {
                "id": "74b70bb8-8802-a1fd-f201-890375a60c8f",
                "createdOn": "2015-10-21T16:32:22Z",
                "isReadOnly": true,
                "isService": false,
                "isDeleted": true,
                "entities": [
                    {
                        "createdOn": "2015-10-21T16:32:22Z",
                        "domain": "autodesk-bim360-asset",
                        "type": "asset",
                        "id": "a2303c73-5460-42f8-9ec8-089d2aecc6b3"
                    },
                    {
                        "createdOn": "2015-10-21T16:32:22Z",
                        "domain": "autodesk-bim360-issue",
                        "type": "issue",
                        "id": "92d6bb28-9c5c-424a-8b29-6d847542fa7f"
                    }
                ]
            }
        ]
    },
    "moreData": true,
    "overwrite": false,
    "nextSyncToken": "eyAibGFzdENoZWNrZWQiOiIyMDE5LTEwLTE4VDEyOjEwOjA3Ljc5NloiIH0="
}
Show Less
Relationship Sync Status
The relationship service sync status endpoint can be used to check if there is new data or changes available for a given syncToken. This endpoint accepts multiple syncTokens and returns a response for each syncToken passed. If moreData is set to true then a call to the relationship sync endpoint with the syncToken passed in the status check will yield updated relationships. The overwrite flag instructs callers “re-set” their copy of the relationship data if it is set to true.

curl -v 'https://developer.api.autodesk.com/bim360/relationship/v2/containers/04074497-ed5d-4ea3-861d-1f146418f5bb/relationships:syncStatus' \
     -X POST \
     -H 'Authorization: Bearer <token>' \
     -H 'Content-Type: application/json' \
     -d '[
           {
             "syncToken": "eyAibGFzdENoZWNrZWQiOiIyMDE5LTEwLTE4VDEyOjEwOjA3Ljc5NloiIH0="
           }
         ]'
Show Less
Sync Status Response - More Data
{
    "results": [
        {
            "moreData": true,
            "overwrite": false,
            "syncToken": "eyAibGFzdENoZWNrZWQiOiIyMDE5LTEwLTE4VDEyOjEwOjA3Ljc5NloiIH0="
        }
    ]
}
Show Less
Sync Status Response - No New Data
{
    "results": [
        {
            "moreData": false,
            "overwrite": false,
            "syncToken": "eyAibGFzdENoZWNrZWQiOiIyMDE5LTEwLTE4VDEyOjEwOjA3Ljc5NloiIH0="
        }
    ]
}

Documentation /Autodesk Construction Cloud APIs /How-to Guide
Inspect a Review
This tutorial demonstrates how to inspect the details of a review by retrieving the file versions included in the review, the workflow snapshot that was captured when the review was created, and the current progress of the review.

By the end, you will understand how to check both the configuration and the status of a review without making changes to it.

The workflow snapshot may differ from the current definition of the approval workflow if the workflow was edited after the review was created. Progress results are returned in reverse chronological order and include only the current round of the review.

Before You Begin
Register an app, and select Autodesk Construction Cloud APIs in the API Access dropdown.
Acquire a 3-legged or 2-legged OAuth token with data:read scopes for querying.
For a 3-legged token, ensure that the user has permission to access the review and the files.
For a 2-legged token, the x-user-id header is required. Retrieve the user’s Autodesk ID by calling GET projects/:projectId/users with your 2-legged OAuth token and the user’s email address. Ensure that the user is a project administrator or a candidate of the review.
Find the project ID for the project you want to work with by following the Retrieve an Account ID and Project ID tutorial. In this example, assume the project ID is 9ba6681e-1952-4d54-aac4-9de6d9858dd4.
Find the review ID by calling GET reviews. In this example, assume the review ID is 4e609369-e950-4097-b7d3-e6cf1c3c5415.
Verify that you have access to the relevant ACC account, project, folders, and files.
Step 1: Get File Versions Included in the Review
Use the project ID (9ba6681e-1952-4d54-aac4-9de6d9858dd4) and the review ID (4e609369-e950-4097-b7d3-e6cf1c3c5415), to call GET reviews/versions and retrieve the file versions that were included in the review.

Request
curl 'https://developer.api.autodesk.com/construction/reviews/v1/projects/9ba6681e-1952-4d54-aac4-9de6d9858dd4/reviews/4e609369-e950-4097-b7d3-e6cf1c3c5415/versions?limit=10&offset=0' \
  -X GET \
  -H 'x-user-id: U5XCJQ22TL8G' \
  -H 'Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT' \
  -H 'Content-Type: application/json'
Response
{
  "results": [
    {
      "name": "3rd Floor 3D Models.pdf",
      "urn": "urn:adsk.wipprod:fs.file:vf.Vl6kgO55TuWoHy9EbXAAaQ?version=1",
      "itemUrn": "urn:adsk.wipprod:dm.lineage:Vl6kgO55TuWoHy9EbXAAaQ",
      "approveStatus": null,
      "reviewContent": {
        "name": "3rd Floor 3D Models (shared).pdf",
        "customAttributes": [{
          "id": 10272,
          "type": "string",
          "name": "Reference Document Number",
          "value": "X-3910-3DWA"
        }]
      },
      "copiedFileVersionUrn": null
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "totalResults": 1,
    "nextUrl": ""
  }
}
Show Less
If the review files are approved or rejected, the approveStatus field is set in the response:

{
  "results": [
    {
      "name": "3rd Floor 3D Models.pdf",
      "urn": "urn:adsk.wipprod:fs.file:vf.Vl6kgO55TuWoHy9EbXAAaQ?version=1",
      "itemUrn": "urn:adsk.wipprod:dm.lineage:Vl6kgO55TuWoHy9EbXAAaQ",
      "approveStatus": {
        "id": "f44e623d-f04f-47fe-8195-efc43d1d985b",
        "label": "Approved",
        "value": "APPROVED"
      },
      "reviewContent": {
        "name": "3rd Floor 3D Models (shared).pdf",
        "customAttributes": [{
          "id": 10272,
          "type": "string",
          "name": "Reference Document Number",
          "value": "X-3910-3DWA"
        }]
      },
      "copiedFileVersionUrn": "urn:adsk.wipprod:fs.file:vf.JsWkC5LaR-6GGrx2GExVTg?version=1"
    },
    {
      "name": "4th Floor 3D Models.pdf",
      "urn": "urn:adsk.wipprod:fs.file:vf.oYonmqDTS8KXyZ2-tI38-g?version=1",
      "itemUrn": "urn:adsk.wipprod:dm.lineage:oYonmqDTS8KXyZ2-tI38-g",
      "approveStatus": {
        "id": "b2a3c3b7-4fef-40a4-868b-981b23e7182f",
        "label": "Rejected",
        "value": "REJECTED"
      },
      "reviewContent": {
        "name": "3rd Floor 3D Models (shared).pdf",
        "customAttributes": [{
          "id": 10272,
          "type": "string",
          "name": "Reference Document Number",
          "value": "X-4270-3DWB"
        }]
      },
      "copiedFileVersionUrn": null
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "totalResults": 2,
    "nextUrl": ""
  }
}
Show Less
In this example, the file 4th Floor 3D Models.pdf has been rejected, so copiedFileVersionUrn is null, which means it was not copied.

The response shows the files that were included in the review, along with their URNs and current approval status.

Step 2: Get Workflow Snapshot for the Review
Use the project ID (9ba6681e-1952-4d54-aac4-9de6d9858dd4) and the review ID (4e609369-e950-4097-b7d3-e6cf1c3c5415) to call GET reviews/workflow and retrieve the workflow snapshot that was captured when the review was created.

Request
curl 'https://developer.api.autodesk.com/construction/reviews/v1/projects/9ba6681e-1952-4d54-aac4-9de6d9858dd4/reviews/4e609369-e950-4097-b7d3-e6cf1c3c5415/workflow' \
  -X GET \
  -H 'x-user-id: U5XCJQ22TL8G' \
  -H 'Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT' \
  -H 'Content-Type: application/json'
Response
{
  "id": "3f8f0b2d-7b0b-4e4c-928a-87e42c1ff55a",
  "name": "Drawing Review Workflow",
  "steps": [
    {
      "id": "INITIATOR",
      "candidates": [
        {
          "autodeskId": "U5XCJQ22TL8G",
          "name": "Alex Johnson"
        }
      ]
    },
    {
      "id": "REVIEWER",
      "candidates": [
        {
          "autodeskId": "V6YCJR34AB2D",
          "name": "Maria Lee"
        }
      ]
    },
    {
      "id": "APPROVER",
      "candidates": [
        {
          "autodeskId": "W7ZDKE56CF3F",
          "name": "Chris Smith"
        }
      ]
    }
  ]
}
Show Less
The response shows the workflow steps and candidates that were defined at the time the review was created.

Note that the content of this workflow may differ from what you get using GET approval workflow, because the workflow may have been updated after the review was created. The snapshot returned by this endpoint reflects the state of the workflow at the time of review creation and does not change with subsequent workflow updates.

Step 3: Get Progress of the Review
Use the project ID (9ba6681e-1952-4d54-aac4-9de6d9858dd4) and the review ID (4e609369-e950-4097-b7d3-e6cf1c3c5415) to call GET reviews/progress and retrieve the current progress of the review.

Request
curl 'https://developer.api.autodesk.com/construction/reviews/v1/projects/9ba6681e-1952-4d54-aac4-9de6d9858dd4/reviews/4e609369-e950-4097-b7d3-e6cf1c3c5415/progress?limit=10&offset=0' \
  -X GET \
  -H 'x-user-id: U5XCJQ22TL8G' \
  -H 'Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT' \
  -H 'Content-Type: application/json'
Response
{
  "results": [
    {
      "stepId": "REVIEWER",
      "stepName": "Reviewer",
      "claimedBy": {
        "autodeskId": "V6YCJR34AB2D",
        "name": "Maria Lee"
      },
      "actionBy": {
        "autodeskId": "V6YCJR34AB2D",
        "name": "Maria Lee"
      },
      "status": "SUBMITTED",
      "endTime": "2025-09-10T12:30:45Z",
      "notes": "Reviewed and approved.",
      "candidates": {
        "users": [
          {
            "autodeskId": "V6YCJR34AB2D",
            "name": "Maria Lee"
          }
        ]
      }
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "totalResults": 1,
    "nextUrl": ""
  }
}
Show Less
The response shows the progress of each step in the review’s approval workflow, including who claimed or submitted the step, when it was completed, and any notes recorded. Results are returned in reverse chronological order, and only data for the current round of the review is included.

Documentation /Autodesk Construction Cloud APIs /How-to Guide
Export Sheets from ACC Build
This tutorial demonstrates how to export sheets from the Sheets tool in ACC Build into a new downloadable PDF file. The steps include finding the IDs of the sheets you want to export, exporting the sheets (you can optionally also export associated markups and hyperlinks), verifying the status of the export, getting a download link, and downloading the exported sheets.

Note the following limitations for exporting sheets:

You can export up to 1000 sheets at a time.
Currently, sheets can only be exported into PDF format.
For more information about exporting sheets, See the Help documentation.

Before You Begin
Register an app, and select the Autodesk Construction Cloud API.
Provision your app to acquire access to your ACC account.
Acquire a 2-legged or 3-legged OAuth token with data:write scope.
Find the project ID for the project that contains the sheets you want to export by following the Retrieve a Project ID tutorial. In this tutorial, assume that the project ID is b.139532ee-5cdb-4c9e-a293-652693991e65.
Verify that you have access to the relevant ACC project, and that you have the permissions to export sheets. Note that by default, users are allowed to export sheets.
Step 1: Find the IDs of the Sheets to Export
Find the IDs of the sheets you want to export using the project ID (b.139532ee-5cdb-4c9e-a293-652693991e65), by calling GET sheets.

If you want to export sheets associated with a specific version set, first call GET version sets to get the version set ID, and then call GET sheets using the version set filter (filter[versionSetId]).

In this example we are using a version set filter (7c2ecde0-2406-49f9-9199-50176848a0b7) to retrieve all the sheets associated with the specific version set.

Request
curl -v 'https://developer.api.autodesk.com/construction/sheets/v1/projects/b.139532ee-5cdb-4c9e-a293-652693991e65/sheets?currentOnly=true&filter[versionSetId]=7c2ecde0-2406-49f9-9199-50176848a0b7' \
     -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
Note that some lines in this payload example have been omitted for readability.

 {
  "results": [
    {
      "id": "0d7a5883-1694-3078-a06d-ad24413f8b06",
      "number": "A-01",
      "versionSet": {
        "id": "7c2ecde0-2406-49f9-9199-50176848a0b7",
        "name": "one set",
        "issuanceDate": "2021-07-01T00:00:00.000Z",
        "deleted": false
      },
      "createdAt": "2021-07-01T05:21:05.391Z",
      "createdBy": "45GPJ4KAX789",
      "createdByName": "John Smith",
      "updatedAt": "2021-07-01T05:21:05.391Z",
      "updatedBy": "45GPJ4KAX789",
      "updatedByName": "John Smith",
      "title": "Floor One",
      "uploadFileName": "example.pdf",
      "uploadId": "5cb5d9da-060e-421e-bca9-97dd8b5cd800",
      "tags": [
        "april",
        "floor"
      ],
      "paperSize": [
        1000,
        600
      ],
      "isCurrent": true,
      "deleted": false,
      "deletedAt": null,
      "deletedBy": null,
      "deletedByName": null,
      "viewable": {
        "urn": "urn:adsk.bimdocs:seed:207edb73-69c2-43d2-ba0e-e2ffe9fdcb56",
        "guid": "cc3eb847-737f-3408-bdbd-e2628a02b8de"
      }
    }
  ],
  "pagination": {
    "limit": 100,
    "offset": 0,
    "previousUrl": null,
    "nextUrl": null,
    "totalResults": 1
  }
}
Show Less
Note the IDs of the sheets (results[i].id) you want to export (0d7a5883-1694-3078-a06d-ad24413f8b06).

Step 2: Export the ACC Sheets
To export the sheet, use the project ID (b.139532ee-5cdb-4c9e-a293-652693991e65) and the sheet ID (0d7a5883-1694-3078-a06d-ad24413f8b06) to call POST exports.

By default, both standard and feature markups (issues and photos) are exported along with the sheets. However, hyperlinks are not included in the default export. You need to specifically indicate if you want to export them.

In this example, we are exporting all types of markups, which includes published (public), unpublished (private), standard, and feature markups (issues and photos). However, note that only the hyperlinks tied to standard markups will be exported. Currently, we do not support the export of hyperlinks associated with feature markups.

For more information about markups, see the Markups References Help Documentation.

Note that this endpoint is asynchronous and initiates a job that runs in the background rather than halting execution of your program. You can check whether the asynchronous job is complete by calling GET exports/:export_id.

Request
curl -v 'https://developer.api.autodesk.com/construction/sheets/v1/projects/b.139532ee-5cdb-4c9e-a293-652693991e65/exports' \
  -X 'POST' \
  -H 'authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a' \
  -H 'content-type: application/json' \
  -d '{
      "options": {
        "outputFileName": "MyOutputFile",
        "standardMarkups": {
          "includePublishedMarkups": true,
          "includeUnpublishedMarkups": true,
          "includeMarkupLinks": true
        },
        "issueMarkups": {
          "includePublishedMarkups": true,
          "includeUnpublishedMarkups": true
        },
        "photoMarkups": {
          "includePublishedMarkups": true,
          "includeUnpublishedMarkups": true
        }
      },
      "sheets": [
        "0d7a5883-1694-3078-a06d-ad24413f8b06"
      ]
    }'
Show Less
Response
{
  "id":"225eb2fb-d5b0-44c9-a50a-2c792d833f2e",
  "status":"processing"
}
Note the export ID (id - 225eb2fb-d5b0-44c9-a50a-2c792d833f2e). You use the export ID to verify the status of the export and to get a download link for the export.

Step 3: Verify the Status of the Export and Get a Download Link
To verify the status of the export job, and to get a download link for the exported sheets, use the project ID (b.139532ee-5cdb-4c9e-a293-652693991e65) and the export ID (225eb2fb-d5b0-44c9-a50a-2c792d833f2e) to call GET exports/:export_id.

When the status is successful the export is copmlete and a signed URL appears in the response, which you can use to download the sheets.

Request
curl -X GET 'https://developer.api.autodesk.com/construction/sheets/v1/projects/b.139532ee-5cdb-4c9e-a293-652693991e65/exports/225eb2fb-d5b0-44c9-a50a-2c792d833f2e' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "id": "225eb2fb-d5b0-44c9-a50a-2c792d833f2e",
  "status": "successful",
  "result": {
    "output": {
      "signedUrl": "https://accpes-p-ue1-storage.s3.amazonaws.com/{bucketId}/jobs/{jobId}/result.pdf?response-content-disposition={fileName}&AWSAccessKeyId={awsKey}&Signature={signature}&x-amz-security-token={token}&Expires={expire}"
    }
  }
}
Show Less
Note the signed URL (result.output.signedUrl) that you can use for downloading the exported file directly from S3. The link is available for one hour. If you need to download the result after one hour, you need to recall POST /projects/{projectId}/exports.

Step 4: Download the Exported File
To download the file from the signed URL, use a GET method and the URL attribute (result.output.signedUrl) as the URI.

Note that you should not use a bearer token with this call.

Request
curl -X 'GET' -v 'https://accpes-p-ue1-storage.s3.amazonaws.com/{bucketId}/jobs/{jobId}/result.pdf?response-content-disposition={fileName}&AWSAccessKeyId={awsKey}&Signature={signature}&x-amz-security-token={token}&Expires={expire}'
Response:
Status Code: 200 OK
Content-Type:application/pdf
Content-Length:90616

with chunked content body
Congratulations! You have exported sheets from ACC Build.

Documentation /Autodesk Construction Cloud APIs /How-to Guide
Download Submittal Attachments
This tutorial demonstrates how to download attachments that were added to submittal items in ACC Submittals. For more information about ACC Submittals, see the Submittals Help documentation. The steps include finding the ID of the submittal item that is associated with the attachment that you want to download, finding the storage object ID for the relevant attachment, retreiving a signed-URL for the attachment, and using the signed-URL to download the attachment.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with the data:read scope.
Verify that you have access to the relevant account and ACC project.
Find the relevant project ID for the project you want to download an attachment from. See the Retrieve a Project ID tutorial for more details. In this example, assume the project ID is f6a1e3b5-abaa-4b01-b33a-5d55f36ba047.
Step 1: Find the Submittal Item ID
Find the ID of the submittal item that is associated with the attachment that you want to download by calling GET items using the project ID (f6a1e3b5-abaa-4b01-b33a-5d55f36ba047).

Request
curl -v 'https://developer.api.autodesk.com/construction/submittals/v2/projects/f6a1e3b5-abaa-4b01-b33a-5d55f36ba047/items' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "results": [
    {
      "id": "b8cc9324-6759-4f07-8ce3-725d5afd4f11",
      "identifier": 1111,
      "typeId": "06fa0c1b-6462-459d-8a38-0aff11bfe868",
      "specId": "62d6f245-b470-4af4-802b-4cb94b5dead1",
      "specIdentifier": "09-5300",
      "specTitle": "Acoustical Ceilings",
      "subsection": "1.05-B",
      "title": "Shop Drawings",
      "description": "Detailed plans by subcontractor, showing project dimensions.",
      "priority": "Low",
      "revision": 0,
      "stateId": "rev",
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
      "responseComment": "",
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
          "id": "Item::retrieve",
          "fields": {},
          "mandatoryFields": [
            ""
          ],
          "transitions": [
            {
              "id": "rev::void",
              "name": "Send to void",
              "stateFrom": {
                "id": "rev",
                "name": "REV"
              },
              "stateTo": {
                "id": "rev",
                "name": "REV"
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
    "previousUrl": "https://developer.api.autodesk.com//construction/submittals/v2/projects/04605b7a-0c53-421e-8e11-c743e75ac10a",
    "nextUrl": null
  }
}
Show Less
Note the ID of the item that is associated with the attachment you want to download (results.id) (b8cc9324-6759-4f07-8ce3-725d5afd4f112).

Step 2: Find the Storage Object ID for the Attachment
Find the storage object ID for the attachment you want to download by calling GET attachments using the project ID (f6a1e3b5-abaa-4b01-b33a-5d55f36ba047) and the item ID (b8cc9324-6759-4f07-8ce3-725d5afd4f112).

Request
curl -v 'https://developer.api.autodesk.com/construction/submittals/v2/projects/f6a1e3b5-abaa-4b01-b33a-5d55f36ba047/items/attachments' \
  -H 'Authorization: Bearer AuIPTf4KYLTYGVnOHQ0cuolwCW2a'
Response
{
  "pagination": {
    "limit": 10,
    "offset": 100,
    "totalResults": 25,
    "previousUrl": "https://developer.api.autodesk.com//construction/submittals/v2/projects/04605b7a-0c53-421e-8e11-c743e75ac10a",
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
      "uploadUrn": "urn:adsk.objects:os.object:wip.dm.prod/72d5e7e4-89a7-4cb9-9da0-2e2bbc61ca8e.dwg",
      "urn": "urn:adsk.wipprod:fs.file:vf.TQW6YsrTTFGrJVJKAaK_ew?version=1",
      "urnVersion": 1,
      "revisionFolderUrn": "urn:adsk.wipprod:fs.folder:co.3is_lyUzTxu6nNXobG2P7Q\"",
      "revision": 0,
      "urnTypeId": "1",
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
          "id": "Item::retrieve",
          "fields": {},
          "mandatoryFields": [
            ""
          ],
          "transitions": [
            {
              "id": "rev::void",
              "name": "Send to void",
              "stateFrom": {
                "id": "rev",
                "name": "REV"
              },
              "stateTo": {
                "id": "rev",
                "name": "REV"
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
Show Less
Find the relevant attachment (results.name), and note the corresponding storage object ID (results.uploadUrn) - urn:adsk.objects:os.object:wip.dm.prod/72d5e7e4-89a7-4cb9-9da0-2e2bbc61ca8e.dwg.

The storage object ID includes the following sections: <urn:adsk.objects:os.object>:<bucket_key>/<object_key>

Note the bucket key - wip.dm.prod and the storage object key - 72d5e7e4-89a7-4cb9-9da0-2e2bbc61ca8e.dwg

Step 3: Generate a Signed S3 URL
Use the bucket key (wip.dm.prod) and the object key (72d5e7e4-89a7-4cb9-9da0-2e2bbc61ca8e.dwg) to call GET buckets/:bucketKey/objects/:objectKey/signeds3download to generate a signed URL for the storage object, which you can use to download the file directly from S3.

Request
curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT" "https://developer.api.autodesk.com/oss/v2/buckets/wip.dm.prod/objects/72d5e7e4-89a7-4cb9-9da0-2e2bbc61ca8e.dwg/signeds3download"
Response
{
  "status": "complete",
  "url": "https://cdn.us.oss.api.autodesk.com/com.autodesk.oss-persistent/us-east-1/3f/bf/5f/0137a7d9dc53af930bc1b527320d50fb5f/wip.dm.prod?response-content-type=application%2Foctet-stream&response-content-disposition=attachment%3B+filename%3D%977d69b1-43e7-40fa-8ece-6ec4602892f3.rvt%22&Expires=1643864703&Signature=00PZYS6gL~Nc6aRG2HAhOCKYl0xtqsuujMJ~VKSXm1vBa-OxS4lPQBSlTx5bswpLBe1W6Rz94eIZW2sPN-v6Mzz~JyXNZ-V9Z7zlBoE1VoQhspLioC225hxq6ZmDSU5QnZXuNDV4ih~p1n3xacYvUvQWX-ONAGVUgQvZ253Svw~qx-pO4j-Yh4kVRmzDZqQut1xOI5ZGH6JFGhXLSzkgbYcfYx6fvCxnvYUJrgAcqncIwGVewI3uC0I84Fzrj8nXE8ojuojqJP0pNlxkfBe~2LfjjzqKDKaNvfC2Grt12j9QgC~cN7nQCRcVUhExpoV1VVB5x3AkVTJ-q5NoedvsfO__&Key-Pair-Id=95HRZD7MMO1UK",
  "params": {
    "content-type": "application/octet-stream",
    "content-disposition": "attachment; filename=\"977d69b1-43e7-40fa-8ece-6ec4602892f3.rvt\""
  },
  "size": 472424,
  "sha1": "ffbf5f0137a7d9dc53af930bc1b527320d50fb53"
}
Show Less
Step 4: Download the File
To download the file from the signed URL, use a GET method and the url attribute as the URI.

Note that you can only use the signed URL once; after you have used it, it becomes invalid and cannot be used again.

Note that you should not use a bearer token with this call.

Request
curl -X GET "https://cdn.us.oss.api.autodesk.com/com.autodesk.oss-persistent/us-east-1/3f/bf/5f/0137a7d9dc53af930bc1b527320d50fb5f/wip.dm.prod?response-content-type=application%2Foctet-stream&response-content-disposition=attachment%3B+filename%3D%977d69b1-43e7-40fa-8ece-6ec4602892f3.dwg%22&Expires=1643864703&Signature=00PZYS6gL~Nc6aRG2HAhOCKYl0xtqsuujMJ~VKSXm1vBa-OxS4lPQBSlTx5bswpLBe1W6Rz94eIZW2sPN-v6Mzz~JyXNZ-V9Z7zlBoE1VoQhspLioC225hxq6ZmDSU5QnZXuNDV4ih~p1n3xacYvUvQWX-ONAGVUgQvZ253Svw~qx-pO4j-Yh4kVRmzDZqQut1xOI5ZGH6JFGhXLSzkgbYcfYx6fvCxnvYUJrgAcqncIwGVewI3uC0I84Fzrj8nXE8ojuojqJP0pNlxkfBe~2LfjjzqKDKaNvfC2Grt12j9QgC~cN7nQCRcVUhExpoV1VVB5x3AkVTJ-q5NoedvsfO__&Key-Pair-Id=95HRZD7MMO1UK" --output "My First File.dwg"
Congratulations! You have downloaded an attachment from ACC submittals.

