Introduction
The BIM 360 APIs allow developers to develop apps that integrate with the Autodesk BIM 360 platform to extend its capabilities in the construction ecosystem.

We currently offer the following BIM 360 APIs:

The BIM 360 Account Admin API automates setting up projects, assigning project admins, and managing member and partner company directories. You can also synchronize data with external systems.
The BIM 360 Assets API creates and manages assets in the BIM 360 Assets service. Use it to define the settings such as categories, custom attributes, and sets of statuses that are required to define assets, and then to create and modify assets within those settings. The API offers powerful search tools to retrieve specific sets of assets and other components, and it can modify both assets and the settings that define those assets.
The BIM 360 Checklists API tracks, sorts, and filters information about checklists, checklist templates, and checklist signatures.
The BIM 360 Cost Management API provides access to the data stored in the BIM 360 Cost Management module. It enables you to manage cost and budget changes to your projects, such as accessing budget, contract, and change order information. For example, you can extract budget data to export to external systems and import the data back to the BIM 360 Cost Management module.
The BIM 360 Data Connector API retrieves data from BIM 360 services such as Admin (both Project and Account), Issues, Locations, Submittals, Cost, and RFIs so the data can be used for local data analysis and other purposes. It works across multiple projects within an account or for a specific project, can set up data reporting on a regular schedule, and returns data in a format easily used by business intelligence tools.
The BIM 360 Document Management API accesses, uploads, and shares 2D plans, 3D BIM models, and any other project documents to maximize collaboration. Note that the BIM 360 Document Management API is part of the Data Management API.
The BIM 360 Issues API creates, tracks, and updates issues. An issue is an item that is created in BIM 360 for tracking, managing and communicating problems and other points of concern through to resolution. You can manage different types of issues, such as design, safety, and commissioning. We support both issues that are associated with a project and issues that are associated with a specific document (pushpin issues).
The BIM 360 Locations API allows you to manage and share the hierarchy of building areas in your project.
The BIM 360 Model Coordination API provides full access to the set of services used by the BIM 360 Model Coordination web application. It enables users to detect and manage the issues that arise when 3D models from different design disciplines are combined into a unified project coordination space.
The BIM 360 Relationships API creates, retrieves, and deletes links between entities across domains.
The BIM 360 RFIs API (beta) creates, tracks, and updates RFIs (requests for information). An RFI is a formal question asked by one project member of another, such as clarification of design intent from the architect. You can manage the RFI workflow by assigning members to the RFI, transitioning the RFI to different states, and adding comments and attachments. We support both RFIs that are associated with a project and RFIs that are associated with a specific document (pushpin RFIs). For more information about RFIs, see the help documentation.
You can use the Viewer SDK to display BIM 360 models in your application.
Currently Unavailable APIs
APIs for markups and submittals are not currently available. We plan to introduce additional BIM 360 APIs in the near future—stay tuned!

Getting Started
Take a look at our Step-by-Step Tutorials that explain how to get access to a BIM 360 account and how to provision access to BIM 360 documents. The tutorials also describe typical BIM 360 API workflows.

The API Basics, Field Guide, and Parameters sections will help you understand the high-level concepts, and the API Reference section will give you the information you need to refine and create your own custom flows.

API Basics
The BIM 360 APIs allow developers to develop apps that integrate with the Autodesk BIM 360 platform to extend its capabilities in the construction ecosystem.

Note that most of the BIM 360 API documentation is housed within the BIM 360 API documentation set. However, BIM 360 endpoints relating to BIM 360 document storage and document management are mostly housed within the Data Management API documentation.

BIM 360 Account Admin
BIM 360 Assets
BIM 360 Checklists
BIM 360 Cost Management
BIM 360 Data Connector
BIM 360 Document Management
BIM 360 Issues
BIM 360 Locations
BIM 360 Model Coordination
BIM 360 Relationships
BIM 360 RFIs (beta)
BIM 360 Account Admin
The BIM 360 Account Admin API allows you to manage your Autodesk BIM 360 account and its projects, members, and company data. It includes the following features:

Create, update, and retrieve information about BIM 360 projects.
Retrieve information about BIM 360 project users. Note that the project user endpoints support both two-legged and three-legged authentication.
Manage your business partner companies across services.
Create a master member directory to manage account users and project users across services.
Manage a business units structure that can be used to create regional offices or locations that you use for reporting purposes.
For more information about BIM 360 Account Admin features and workflows, see the BIM 360 Account Admin help documentation.

BIM 360 Assets
The Assets API provides programmatic access to the features of the BIM 360 Assets service. You can use it to define Assets settings and to manage assets within those settings. Assets API features allow you to:

Create and modify asset categories, setting up a hierarchical category tree that you can use to assign categories to assets.
Create and modify status sets containing statuses that you can assign to assets.
Create and modify custom attributes that you can assign with values to assets.
Associate status sets and custom attributes to categories so that assets in each category have a specific set of statuses and custom attributes that appropriately define the assets there.
Create, modify, and delete assets.
Search for and return sets of assets using powerful search filters.
Search for and return sets of settings components such as categories, status sets, and custom attributes.
Create and remove relationship links (maintained by the Relationships service) between assets and categories and outside entities such as issues and documents.
Retrieve the set of possible error codes that the Assets API may return.
The Assets API currently has some limitations:

It does not support 2-legged authentication.
It doesn’t yet provide endpoints that explicitly synchronize locally stored assets and Assets settings with service-stored assets and settings. However, it does provide a workaround through filtering on the updatedAt properties that can reveal changes since last checking the assets and Assets settings.
For more information about the Assets API, see the Assets API Field Guide.

BIM 360 Checklists
The BIM 360 Checklists API tracks information about a project’s checklists and checklist templates. This includes the following features:

Track and analyze the progress of a checklist.
Filter and sort checklists and checklist templates.
Retrieve detailed information about a checklist’s items, sections, and attachments.
Download checklist attachments.
Download checklist section signatures from S3 storage.
Constructing Checklists
Note that checklists are called instances in the Checklist API.

An instance payload can include data about the instance’s sections, items, and attachments:

../../../_images/checklistsRelations.png
You can reconstruct a checklist from the data by using the relationship objects in the response payload to arrange the sections, items, and attachments to reproduce the instance hierarchy. For more details, see the GET instances/:id endpoint.

For more information about BIM 360 Checklist features and workflows, see the BIM 360 Checklists help documentation.

Note that we do not currently support markups and submittals. In the near future we will be supporting more BIM 360 APIs - stay tuned!

BIM 360 Cost Management
Using the Cost Management API, you can:

Read budget code templates, and read, create, update and import budget code segments and values.
Read, create, update and import (i.e., bulk create) budget items.
Read, create, and update contract packages.
Read, create, update, and delete main contracts and main contract items.
Read, create, update, and delete Schedule of Values (SOV) items.
Read, create, and update change orders and cost items.
Read, create, update, and delete expenses.
Read, create, update, and delete expense items.
Read payments and payment items.
Read, create, update, and delete performance tracking items and performance tracking item instances.
Read, create, update, and delete timesheets.
Upload and download attachments to a budget, contract, change order, and cost item.
Download documents or file packages generated from change orders and contracts.
Subscribe to various types of Cost API-generated Webhook events that your app can monitor and respond to.
For more information about the Cost API, see the Cost Management API Field Guide

For information about the product features, see the BIM 360 Cost Management help documentation.

BIM 360 Data Connector
The BIM 360 Data Connector API exports data from BIM 360 service modules so that you can create your own custom analytics and reports, enrich that data with corresponding data of your own, and -— if you’d like -— archive that data in your own on-premise storage. The Data Connector service has access across all projects within an account so that you can get a full view of an account’s activity.

The Data Connector service delivers data files in CSV format, widely accepted by business intelligence tools such as Microsoft Power BI, Tableau, and Microsoft Excel. Returned data includes all objects within a service. Objects returned for the Admin service, for example, include users, projects, and companies. Objects returned for the Issues service include issues, root causes, and comments.

Using the Data Connector API, you can:

Request data from one or more BIM 360 services. These currently include Admin (both Project and Account), issues, locations, submittals, cost, and rfis, and will expand to include more services.
Retrieve that data immediately, or set up a recurring schedule when data is extracted and presented to you.
Get notification via URL callback or email when data extraction is ready to retrieve, or check on extraction at your convenience.
Set up and manage a set of data requests, editing them as desired to change what they extract, when they extract, and how they notify you.
For more information about the Data Connector API, see the Data Connector API Field Guide.

BIM 360 Document Management
Construction teams can use BIM 360 Document Management to manage blueprints, 2D plans, 3D BIM models, and any other project documents. BIM 360 Document Management is designed to streamline your document management processes, consolidate all your sheets and designs, and set up standard templates and workflows to maximize efficiency.

You access BIM 360 Document Management via the Data Management API, where you can manage your BIM 360 folders and files.

Some of the Document Management endpoints are part of a separate BIM 360 Document Management API. This includes the following features:

Export PDF files
Manage folder permissions
Retrieve custom attribute information and manage custom attribute values.
Retrieve file naming standard information for a project.
If you are using the Model Derivative API or the Viewer SDK to access BIM 360 data in EMEA data centers, see the blog on EMEA data centers for instructions on how to update your code.

For more information about BIM 360 Document Management, see the BIM 360 Document Management help documentation.

BIM 360 Issues
The BIM 360 Issues API creates, tracks, and updates issues. An issue is an item that is created in BIM 360 for tracking, managing and communicating problems and other points of concern through to resolution.

We support managing issues that are associated with a project, as well as managing issues that are associated with a specific document (pushpin issues).

The Issues API includes the following features:

Create, update, and track project-related BIM 360 issues.
Create, update, and track document-related BIM 360 issues.
Retrieve a project’s issue custom attributes and issue custom attribute mappings.
Add and update comments for issues.
Add and delete attachments for issues.
Issues Workflows and Transitions
You can use the Issues API to transition the issue through different status changes: draft, open, answered, and closed. You can also change various characteristics of the issue, for example, who it is assigned to and the due date.

BIM 360 Locations
The BIM 360 Locations API allows you to manage and share the hierarchy of building areas in your project using a location breakdown structure (LBS). An LBS is a tree structure that represents the layout of a construction project. Currently, the API allows you to retrieve locations (nodes) in the LBS.

BIM 360 Model Coordination
The BIM 360 Model Coordination API can be used to:

Create and view coordination space model sets and versions.
Create virtual model set views by combining user defined views extracted from design files uploaded to BIM 360 Document Management.
Run Navisworks-like clash tests against model set versions.
Group clashes and assign their resolution to project users via the BIM 360 Issues Service.
Permanently ignore clashes that are expected or are part of the design.
Run SQL-like breakdown queries against a unified coordination space BIM property index.
For more information on BIM 360 Model Coordination product features, see the BIM 360 Model Coordination help documentation.

BIM 360 Relationships
The BIM 360 Relationships API can be used to:

Create, retrieve and delete relationships between entities in different BIM 360 modules.
Perform advanced searches to retrieve specific links between entities where only some of the information about the links is known.
Synchronize relationships for a project, based on specific criteria (for example, for offline use).
BIM 360 RFIs (beta)
The BIM 360 RFIs API creates, tracks, and updates RFIs (requests for information). An RFI is a formal question asked by one project member of another, such as clarification of design intent from the architect.

We support managing RFIs that are associated with a project, as well as managing RFIs that are associated with a specific document (pushpin RFIs).

The RFIs API includes the following features:

Create, update, and track project-related BIM 360 RFIs. These RFIs correspond to the BIM 360 Project Management service. For more information, see the RFIs help documentation.
Create, update, and track document-related BIM 360 RFIs.
Add comments to an RFI and retrieve them. Note that we do not currently support adding multiple comments to RFIs.
Add, retrieve, and delete RFI attachments. Note that we do not currently support adding multiple attachments to RFIs.
The following table describes the Project Admin module names and the corresponding RFIs API names:

Project Admin Module Workflow Role Name	RFIs API Workflow Role Name
Creator	Subcontractor (projectSC)
Manager	General Contractor (projectGC)
Reviewer 1 (EMEA workflow)	Construction Manager (projectCM)
Reviewer (US workflow) / Reviewer 2 (EMEA workflow)	Architect (projectArch)
RFI Workflows
The RFIs endpoints contain references to workflows and permissions that are set in the Project Admin UI, such as the type of RFI workflow assigned to the project, and the workflow roles assigned to the project members. To check the workflow types for the RFI, see GET rfis/:id. To check the workflow roles assigned to the project members, see GET users/me.

Note that the RFIs API does not currently support setting up workflows and configuring worklow roles. For more information about RFI workflows, see the RFIs help documentation.

RFI Transitions
You can use the RFIs API to transition the RFI through different status changes: draft, submit, open, answered, closed, and void. You can also change various characteristics of the RFI, for example, who it is assigned to and the due date, etc.

For information on transitioning an RFI through a typical workflow, see the RFI Transitions tutorial.

Note that we do not currently support uploading local files to RFIs or linking RFIs to PCOs (potential change orders).

BIM 360 API Terminology
The following table defines important terms for the BIM 360 APIs:

Category	Description
Account	The host organization that owns BIM 360 projects.
Attachment	A document or image attached for reference to an issue.
Business Unit	Organize projects to correspond to different business units within an organization. For example, a construction firm may have different divisions for different project types (buildings, interiors, infrastructure). The information can then be used for reporting and analytics.
Checklist	A list of points or questions that need to be verified in order to assess the safety or quality of work completed by a trade in a given location or the correct installation of a piece of equipment.
Checklist template	Outlines the structure and content of a checklist.
Company	An organization that contributes to a project. Every project member is associated with a company.
Container	Each project is assigned a set of containers that stores all the issues and checklists for the project. This is relevant for the Issues API and the Checklist API. The container ID is used to call BIM 360 Issues and Checklists endpoints. You need to use the Data Management API (GET hubs/:hub_id/projects) to find the Container IDs.
Issue	An item that is created in BIM 360 for tracking, managing and communicating problems and other points of concern through to resolution.
Project	The primary organizing construct within which people work and content is managed in BIM 360.
Pushpin	A visual marker that denotes the location of an issue or RFI in a document.
RFI	An RFI (request for information) is a formal question asked by one project member of another, such as clarification of design intent from the architect.
User	Members participating in your BIM 360 account.
Getting Started
To use the BIM 360 APIs, you first need to register an app and successfully acquire an OAuth token. You also need to get access to a BIM 360 account and to provision access to BIM 360 documents.

Take a look at our Step-by-Step Tutorials to see typical BIM 360 API workflows.

Documentation /BIM 360 API /How-to Guide
Retrieve BIM 360 Account and Project ID
This tutorial demonstrates how to obtain your BIM 360 Account and Project ID. If you already have these, you can skip this tutorial.

Before You Begin
Register an app, and select the Data Management and BIM 360 APIs.
Acquire a 3-legged OAuth token with data:create data:read and data:write scopes.
Verify that you have access to the relevant BIM 360 account, project, and folder.
Step 1: Find the Hub ID for the BIM 360 Account
Find the hub ID for the BIM 360 account you are interested in, by calling GET hubs.

Note that the BIM 360 account ID corresponds to a Data Management hub ID. To convert an account ID into a hub ID you need to add a “b." prefix. For example, an account ID of d952a4eb-ad57-4d64-b9ab-d540b3b4522e translates to a hub ID of b.d952a4eb-ad57-4d64-b9ab-d540b3b4522e.

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
      "id": "b.d6cf8c84-c25e-4534-ae5c-62e08480e751",
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
Show More
In this example, assume that the Account that you are interested in is in a hub called My First Account.

Find the hub (data.name), and note the hub ID - b.d6cf8c84-c25e-4534-ae5c-62e08480e751.

Step 2: Find the Project ID
To get a list of all the projects in the hub (account), use the hub ID (b.d6cf8c84-c25e-4534-ae5c-62e08480e751) to call GET hubs/:hub_id/projects. Find the project ID of the project that you are interested in.

Note that the project ID in BIM 360 corresponds to the project ID in the Data Management API. To convert a project ID in BIM 360 to a project ID in the Data Management API, you need to add a “b." prefix. For example, a project ID of a4be0c34a-4ab7 translates to a project ID of b.a4be0c34a-4ab7.

Request
curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT" "https://developer.api.autodesk.com/project/v1/hubs/b.d6cf8c84-c25e-4534-ae5c-62e08480e751/projects"
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "https://developer.api.autodesk.com/project/v1/hubs/b.d6cf8c84-c25e-4534-ae5c-62e08480e751/projects"
    }
  },
  "data": [
    {
      "type": "projects",
      "id": "f6a1e3b5-abaa-4b01-b33a-5d55f36ba047",
      "attributes": {
        "name": "My First Project",
        "extension": {
          "type": "projects:autodesk.core:Project",
          "version": "1.0"
        }
      }
    }
  ]
}
Show Less
In this example, assume that My First Project is the project you are interested in.

Find the project (data.attributes.name), and note the project ID (data.id) - f6a1e3b5-abaa-4b01-b33a-5d55f36ba047.

Documentation /BIM 360 API /How-to Guide
Retrieve BIM 360 Assets Data
This tutorial demonstrates how to fetch your complete set of BIM 360 Asset data and project settings. This can be for the entirety of your Asset data, or filtered to a subset of Asset data.

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
For more details about BIM 360 Assets API, see the Assets Field Guide.

Before You Begin
Register an app, and select the Data Management and BIM 360 APIs.
Acquire a 3-legged OAuth token with data:read scope.
Verify that you have access to the relevant BIM 360 account, project, and folder.
Retrieve the relevant BIM 360 account and project ID. In this tutorial we will use the example project ID f6a1e3b5-abaa-4b01-b33a-5d55f36ba047, but you should replace that with the project ID you have retrieved for your project.
Step 1: Fetch Assets
To get the assets themselves, use the project ID (f6a1e3b5-abaa-4b01-b33a-5d55f36ba047) to call GET assets/v2/projects/:projectId/assets.

You will want to ensure you set the query parameter includeCustomAttributes=true if you wish to include Asset custom attribute data in your fetch. If you want to include deleted assets, you can set the query parameter includeDeleted=true as well.

If you want to fetch a more targeted set of assets, you can provide additional filters in your request. This could include filtering by category, status, a specific location or a location hierarchy, custom attribute value(s), or any combination thereof. A complete list of the filters available, and how they are used, can be found in the query parameter documentation for the asset pagination endpoint. Filters provided in the initial pagination request will automatically be added to the nextUrl field to continue the filtered pagination.

If you want to include only assets that have changed since previously retrieving assets, you can use the query parameter filter filter[updatedAt]={previousFetchTime}...

Request
curl 'https://developer.api.autodesk.com/bim360/assets/v2/projects/f6a1e3b5-abaa-4b01-b33a-5d55f36ba047/assets?includeCustomAttributes=true' \
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
    "nextUrl": "https://developer.api.autodesk.com/bim360/assets/v1/projects/f6a1e3b5-abaa-4b01-b33a-5d55f36ba047/assets?cursorState=eyJsaW1pdCI6MjUsIm9mZnNldCI6MjV9"
  }
}
Show Less
Step 2: Fetch Categories
To get the categories, use the project ID (f6a1e3b5-abaa-4b01-b33a-5d55f36ba047) to call GET assets/v1/projects/:projectId/categories.

If you want to include only active categories, you can set the query parameter filter[isActive]=true. Note that filtering to only active or inactive categories can result in the returned tree not being fully intact.

If you want to include only categories that have changed since previously retrieving categories, you can use the query parameter filter filter[updatedAt]={previousFetchTime}...

Request
curl 'https://developer.api.autodesk.com/bim360/assets/v1/projects/f6a1e3b5-abaa-4b01-b33a-5d55f36ba047/categories' \
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
curl 'https://developer.api.autodesk.com/bim360/assets/v1/projects/f6a1e3b5-abaa-4b01-b33a-5d55f36ba047/status-step-sets' \
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
curl 'https://developer.api.autodesk.com/bim360/assets/v1/projects/f6a1e3b5-abaa-4b01-b33a-5d55f36ba047/category-status-step-sets/status-step-sets:batch-get?includeInherited=true' \
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

Documentation /BIM 360 API /How-to Guide
Retrieve a Checklists Container ID
This tutorial demonstrates how to retrieve a container ID for a BIM 360 project. Each BIM 360 project is assigned a checklists container (checklistsContainerId) that stores all the checklists data for the project. The checklists container ID is used to call the BIM 360 checklists endpoints. To retrieve the ID, you need to call several Data Management endpoints.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with the data:read scope.
Verify that you have access to the relevant BIM 360 account and BIM 360 project. (To create a new BIM 360 project, see POST projects)
Step 1: Find the Hub ID
You first need to call GET hubs to find the hub ID for your BIM 360 account.

Note that the BIM 360 account ID corresponds to a Data Management hub ID. To convert an account ID into a hub ID you need to add a “b." prefix. For example, an account ID of c8b0c73d-3ae9 translates to a hub ID of b.c8b0c73d-3ae9.

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
Show More
In this example, assume that the project you want the container for is in My First Account hub.

Step 2: Find the Container ID for the Project
Use the BIM 360 hub ID that you retrieved in the previous step (b.cGVyc29uYWw6cGUyOWNjZjMy) to call GET hubs/:hub_id/projects, and retrieve a list of all the projects in the hub the user has access to. In this example, we have added a filter to only return details of a specific project (Demo Project).

Request
curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT" "https://developer.api.autodesk.com/project/v1/hubs/b.cGVyc29uYWw6cGUyOWNjZjMy/projects?filter%5Battributes.name%5D=Demo%20Project"
Response
The response payload includes the checklists container ID (data.relationships.checklists.id).

{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "https://developer.api.autodesk.com/project/v1/hubs/b.7fcde01c-738a-4f5e-8a1c-7a8da2381693/projects"
    }
  },
  "data": [
    {
      "type": "projects",
      "id": "b.1f50f9e7-df95-43f9-9366-2fd44cafa768",
      "attributes": {
        "name": "Demo Project",
        "extension": {
          "type": "projects:autodesk.bim360:Project",
          "version": "1.0",
          "schema": {
            "href": "https://developer.api.autodesk.com/schema/v1/versions/projects:autodesk.bim360:Project-1.0"
          },
          "data": {}
        }
      },
      "links": {
        "self": {
          "href": "https://developer.api.autodesk.com/project/v1/hubs/b.7fcde01c-738a-4f5e-8a1c-7a8da2381693/projects/b.1f50f9e7-df95-43f9-9366-2fd44cafa768"
        }
      },
      "relationships": {
        "hub": {
          "data": {
            "type": "hubs",
            "id": "b.7fcde01c-738a-4f5e-8a1c-7a8da2381693"
          },
          "links": {
            "related": {
              "href": "https://developer.api.autodesk.com/project/v1/hubs/b.7fcde01c-738a-4f5e-8a1c-7a8da2381693"
            }
          }
        },
        "rootFolder": {
          "data": {
            "type": "folders",
            "id": "urn:adsk.wipprod:fs.folder:co.xOuT2J3zSdqR4eD_pkd3WQ"
          },
          "meta": {
            "link": {
              "href": "https://developer.api.autodesk.com/data/v1/projects/b.1f50f9e7-df95-43f9-9366-2fd44cafa768/folders/urn:adsk.wipprod:fs.folder:co.xOuT2J3zSdqR4eD_pkd3WQ"
            }
          }
        },
        "topFolders": {
          "links": {
            "related": {
              "href": "https://developer.api.autodesk.com/project/v1/hubs/b.7fcde01c-738a-4f5e-8a1c-7a8da2381693/projects/b.1f50f9e7-df95-43f9-9366-2fd44cafa768/topFolders"
            }
          }
        },
        "checklists": {
          "data": {
            "type": "checklistsContainerId",
            "id": "e59adc9d-2677-4afc-a800-4bc42101f7d8"
          },
          "meta": {
            "link": {
             "href": "https://developer.api.autodesk.com/bim360/checklists/v1/containers/e59adc9d-2677-4afc-a800-4bc42101f7d8/instances"
            }
          }
        }
      }
    }
  ]
}

Documentation /BIM 360 API /How-to Guide
Retrieve a Checklists Section Signature
This tutorial demonstrate how to download a section item signature of a checklist. Each section of a checklist includes the sectionSignatures object, which contains an array of section signatures.

The BIM 360 checklist signatures are stored in S3 as images of actual signatures in Scalable Vector Graphics (SVG) format. Each signature object contains an object key that you can use to retrieve the associated SVG signature image.

Note that individual checklists are known as instances, so an instanceId is the ID of a checklist.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with the data:read scope.
Verify that you have access to the relevant BIM 360 account and BIM 360 project.
Have your project’s checklists containerId, or acquire it using the Retrieve a Checklists Container ID tutorial.
Have the appropriate instanceId of the checklist you want to retrieve the signature from, or acquire one using the GET instances endpoint.
Step 1: Find the object key of the section signature
Use the GET instances/:instanceId endpoint to retrieve the section signature using containerId and instanceId.

Request
curl -X GET "https://developer.api.autodesk.com/bim360/checklists/v1/containers/:containerId/instances/:instanceId?include=sections%2Csections.items%2Csections.items.attachments%2Csections.items.supplementalAttachments" \
-H "Authorization: Bearer cKLfhoInUNxFF0F0Eu7fZ187HUml"
Response
{
    "jsonapi": {
        "version": "1.0"
    },
    "meta": {},
    "links": {
        "...": "..."
    },
    "data": {
        "...": "..."
    },
    "included": [
        {
            "type": "instance_sections",
            "id": "12526088",
            "attributes": {
                "urn": "urn:adsk.checklists.cs.instance.section:edbd4b32-afef-452d-84a2-5e4269e36155/12526088",
                "templateSectionId": 4646162,
                "modifiedBy": "AUR8JHCWYTJG",
                "updatedAt": "2022-09-07T10:11:04.763Z",
                "status": "Completed",
                "instructions": null,
                "title": "SECTION 1",
                "index": 1,
                "number": 1,
                "itemsNumbering": {
                    "...": "..."
                },
                "sectionNumbering": {
                    "...": "..."
                },
                "assignees": [{
                    "...": "..."
                }],
                "permittedActions": [
                    "canEdit"
                ],
                "permittedAttributes": [
                    "...": "..."
                ],
                "sectionSignatures": [
                    {
                        "id": "6a2bc2e8-db7b-41a2-9a6d-d05b4bd4f299",
                        "urn": "urn:adsk.checklists.cs.item.signature:edbd4b32-afef-452d-84a2-5e4269e36155/6a2bc2e8-db7b-41a2-9a6d-d05b4bd4f299",
                        "ossUrn": "urn:adsk.objects:os.object:checklists.prod.us/6a2bc2e8-db7b-41a2-9a6d-d05b4bd4f299",
                        "instanceSectionId": 12526088,
                        "index": 2,
                        "requiredBy": "",
                        "isRequired": true,
                        "signedName": "Anuj ",
                        "signedCompany": "alentica",
                        "submittedBy": "AUR8JHCWYTJG",
                        "signedAt": "2022-09-07T15:40:52.936Z",
                        "createdAt": "2022-09-07T10:10:36.447Z",
                        "updatedAt": "2022-09-07T10:11:00.772Z",
                        "deletedAt": null,
                        "instructions": "",
                        "uploadStatus": "Completed",
                        "uuid": "002c1c04-380d-40ca-8f0c-01863d4ce31d"
                    }
                ],
                "uuid": "49000563-dcd2-4b2e-a57e-658b3b251bd9"
            },
            "links": {
                "...": "..."
            },
            "relationships": {
                "...": "..."
            }
        },
        {
            "type": "instance_items",
            "id": "78347147",
            "attributes": {
                "...": "..."
            },
            "links": {
                "self": "/containers/edbd4b32-afef-452d-84a2-5e4269e36155/instance_items/78347147"
            },
            "relationships": {
                "...": "..."
            }
        }
    ]
}
Show Less
In the response, you’ll find the relevant signature inside the included.sections.attributes.sectionSignatures array. The signature’s ossUrn attribute value of urn:adsk.objects:os.object:checklists.prod.us/6a2bc2e8-db7b-41a2-9a6d-d05b4bd4f299 parses into three substrings:

urn:adsk.objects:os.object (the Object Storage Service)
checklists.prod.us (the bucket key)
6a2bc2e8-db7b-41a2-9a6d-d05b4bd4f299 (the signature object key)
You’ll use these keys to access the storage service in the next step.

Step 2: Generate a signed S3 URL for the section signature
Use the Data Management API’s POST buckets/:bucketKey/objects/batchsigneds3download endpoint to generate a signed URL that you can use to download the signature SVG directly from S3. Include the bucket key (checklists.prod.us) in the endpoint URI, and the object key (6a2bc2e8-db7b-41a2-9a6d-d05b4bd4f299) in the payload.

Request
curl --request POST 'https://developer.api.autodesk.com/oss/v2/buckets/checklists.prod.us/objects/batchsigneds3download' \
     --header 'Authorization: Bearer 5CsDfQ83YgS49Jp9reGoTiFNwozS' \
     --header 'Content-Type: application/json' \
     --header 'Cookie: PF=mgLuMdDrunrpwPh51y1Zva' \
     --data-raw '{
                   "requests": [{
                     "objectKey": "6a2bc2e8-db7b-41a2-9a6d-d05b4bd4f299"
                   }]
                 }'
Show Less
Response
{
    "results": {
        "6a2bc2e8-db7b-41a2-9a6d-d05b4bd4f299": {
            "status": "complete",
            "url": "https://s3.amazonaws.com/com.autodesk.oss-persistent/52/fe/88/bcb1c05c58e97f0e2aed6b4554f97c6739/checklists.prod.us?response-content-disposition=attachment%3B%20filename%3D%226a2bc2e8-db7b-41a2-9a6d-d05b4bd4f299%22&response-content-type=application%2Foctet-stream&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEHoaCXVzLWVhc3QtMSJGMEQCIBMXw8rUAyCdRKFCF5dA0%2B84T5bAdI%2Bbk0QVrIyHprTdAiAR5MHrqc%2BFyXZ479pTLJXNC4L%2FBldZocv1JLGu90l34yrMBAgTEAAaDDYwNDczMzAwOTQwMyIMfXrMpUHMNFeZz0mPKqkE%2FOuIUOi3PxZp5ca7owgxWCiRPM4JCftDRAVTVAw7sm%2FpxsFcJ0fdIX0mmsr4P58B8vdiBHEzBlqW06nmYKbmbWpv%2BDKV%2FKtaOKdW7pfqpFsuuUFaNQnnF8ZqnFGtkpBBLtDCmCB6Rym18EIOnO4L1C5q607zNF5qM9fSebvgCJwGHjIOSkisJixcfzZLpLP2lrGvqtCCgN1l8vQqFRlkLo7Uq41dZAH7ZjCGnDIfC5z34sSFR14FglWNlgP9%2BF8w8kiW8LWGtjNVoLPasH1gbN01OXLDN5rdIVIohTcUVG4OGJVpuovWC3g2LlkeALDaoQp64gmwaculq19Nbtivk3j1aFfo0dn37licc6%2BxUn3SI71h128JmgAr102d1XBP7pLRL89Z4x9j7mGMTq4dKDt2bsaTZKfii%2FRkpZTzMPGNTVwsCzUFRPiG016mxD8GifKoo7KnQM26SiRtT7EAU6H%2FsiqOKt%2BRO2oal2OmO%2FWpOEwyaTlTdftsp2yI%2BzPDJ%2B28wq3m%2FkMPSvZ3Re8WsrL9Nj8%2FIWgJh0ArICa8IQZYeZgKQNKpcREGVLAWF0WhSvfFPp9U9csrP%2F89Ym%2F9fbnfT2%2BqFqNON%2BfSi4%2F6QI1H%2FYL5IdD8DhzL9Y2q740uI5ja%2Buvy%2BwxO80gbRPazHlSMTNzroieVJplHhIKTv0Xz2ZMVrVPGToa8%2B8drr%2FT7LOEcdZKBMnl2IYMbmEHTt%2BbB6uQK9qW0pDC90eGYBjqqAczuHMmVXVRC60ffCYjARQwFsryC3o1vk8M6V4cd%2BLNuTd5m5coSF130f1F%2B9ymt10TuNvuIBYV9Yg3hwW9dfLNLvRtQLzvceTwxUC5arJH5LoV4TYEeHQv6%2BXtw%2Bm%2FkhFGBN1gMCJ8Uarl8ROCCMVVk5hPBNKKd3hoU11RZuRt5PEEfVnmRojLtnBPzSmQn79NqeTDTq5ja%2BlJE34pdpywkH2aRTteit1E3&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220907T101906Z&X-Amz-SignedHeaders=host&X-Amz-Expires=119&X-Amz-Credential=ASIAYZTHFNX5XBYMIFNO%2F20220907%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=4c3a63fea6791e280cb3d28060f036b7dff60875208c9eae9eedf238a4872cb2",
            "params": {
                "content-type": "application/octet-stream",
                "content-disposition": "attachment; filename=\"6a2bc2e8-db7b-41a2-9a6d-d05b4bd4f299\""
            },
        },
        "size": 737,
        "sha1": "52fe88bcb1c05c58e97f0e2aed6b4554f97c6739"
    }
}
Show Less
The value of results.6a2bc2e8-db7b-41a2-9a6d-d05b4bd4f299.url is the signed S3 URL that you can use to retrieve the signature image.

Step 3: Fetch the section signature using the S3 URL
Make a GET request using the URL returned in the previous step to download the signature SVG.

Note that this call does not require an authorization token.

Request
curl --request GET 'https://s3.amazonaws.com/com.autodesk.oss-persistent/52/fe/88/bcb1c05c58e97f0e2aed6b4554f97c6739/checklists.prod.us?response-content-disposition=attachment%3B%20filename%3D%226a2bc2e8-db7b-41a2-9a6d-d05b4bd4f299%22&response-content-type=application%2Foctet-stream&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEHoaCXVzLWVhc3QtMSJHMEUCIQCeifG847tv1Yhwb%2B7g4rkrMU%2Fg8naa7c7tuRqs54dRNAIgTnClXB%2FO8JikYF3CSnZ%2BtlYW%2BcmRGelHM%2BV3a%2Bekex8qzAQIEhAAGgw2MDQ3MzMwMDk0MDMiDI3JVyn%2FKxZYOsLljyqpBIRPCdpFubLOk0Oc%2FPtN95YZbhZqE%2BOomsLQVo%2BN5JZFt9dwZ5z5%2FzQdOsqlaGkyLQxBdpTqYGVufXVz9NApnlk92gCmhZ3mlCT%2FaXVJNvsakp61ZH2ya%2BHMdlm9B7UatodX0TUdMcdNGP8BB3BQyWmNe9BM%2FffzE4ttP%2BnmQhjKI1jVMqQkjTa3kCzgFyTxUDqIB7fHQpRdmrAfQtr%2BTJZTm1kK6JOX6A1wOYdXG4MSrnXwU8cU%2Fz0wAH6dIAgVoL%2Br3TnGxBBb1GvTe4R9tMHNJoms%2FKfV2DbQJtBehs5nIkWG7Aa%2BWyblaitBzQMUClTPsVAelWYvdqHLNQfjDpSnBz0d1THe7IX%2BxiR0PxQxTNl8M2aN%2FKYjpQtrfV5FNddKD5QVArmFog2uvTN3jWOeypEvRQS4ai1bYx4sjGKGlGR5mEfg5IJZYcSgCtUxHpu%2BfJKJtQy9%2FXLvtYKsNScyynmAXMvcwOee9Umd6QMhMzjkQ9UtrKSNExlLQyKOaURvjYJTHFP8jEGqRgpPHfQ%2BX7ezzP7VJIYaVyjMzfTlG2tnVMLq%2BXJwraj8NQZ%2FrUx%2Ft4kOStfgrUcuUjOrfI%2Bf6FzLkqNmP%2FGNK4HmQwY9LXOKJlyAN1uSLaZXPJ8Eq%2FVve6R7KGC2GuEkd4ZcTOysq%2Fk%2FKCjGlYzvu32b8wA6gA3t1IiXRlwyqhNC8G%2Bo93f6%2FJtT5y2bO6DSBVJc7DFO5BUzD71Shg0w%2BcThmAY6qQH7oKGRABcV%2F2qnYVGJW6OfBWlf2GDjcoyuUfOLaQGSDWUB1VUi4OwbUCN5eSKvULc1PlIADiXT62LPv6%2Fw4BFjYJdY%2BI6j8spt%2Fy4%2F9ojg2XyNUml%2FYeFqhUY6Z785IumPSIj90i%2FviDOAckG26woNGADNyvZw%2BPMwiE3FL0GRGLQHONy2GJAxrDocxMHUs9%2FCy9DzM%2BO3lPuJZfvjCbwt8M3593y7AE5j&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220907T102227Z&X-Amz-SignedHeaders=host&X-Amz-Expires=119&X-Amz-Credential=ASIAYZTHFNX5ROZAZSGV%2F20220907%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=ab747902cf0125d7323b54d46e7ad522a0e2fcd2efc5cb57483f026280eeb4e9'
Response
<svg width=”566” height=”150” viewbox=”0 0 566 150” version=”1.2” xmlns=”http://www.w3.org/2000/svg”><g stroke=”black” fill=”none” stroke-linecap=”round” stroke-linejoin=”round” stroke-width=”5”><path d=”M 122 117.703125 L 122 114.703125 L 122 106.703125 L 122 95.703125 L 128 79.703125 L 139 59.703125 L 155 42.703125 L 167 36.703125 L 186 31.703125 L 198 31.703125 L 205 36.703125 L 210 47.703125 L 210 59.703125 L 206 68.703125 L 197 78.703125 L 182 85.703125 L 169 87.703125 L 157 82.703125 L 150 68.703125 L 149 54.703125 L 157 45.703125 L 177 38.703125 L 224 37.703125 L 242 39.703125 L 250 42.703125 L 255 45.703125 L 258 48.703125 L 259 51.703125 L 259 52.703125 L 259 52.703125 L 259 52.703125 L 260 52.703125”></path></g></svg>

Documentation /BIM 360 API /How-to Guide
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

Documentation /BIM 360 API /How-to Guide
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

Step 2: Change Your Request’s Active Status
To update your data request’s description, use the PATCH requests endpoint. It accepts a set of parameter settings that you want to change in the data request. You don’t need to specify all the parameters settings, just the one you want to change. In this example, it’s description. We’ll change it to “My Updated Weekly Extract”.

Request
curl -X PATCH 'https://developer.api.autodesk.com/data-connector/v1/accounts/<accountId>/requests/<requestId>' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <authToken>' \
-d '{
    "description": "My Updated Weekly Extract"
}'
Response
{
    "id": "55e410c5-4294-44ce-becf-68e1cfd6738c",
    "description": "My Updated Weekly Extract",
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
    "callbackUrl": null,
    "createdAt": "2020-11-19T16:32:13.545Z",
    "updatedAt": "2020-11-19T16:35:13.912Z",
    "deletedAt": null,
    "serviceGroups": [
        "admin",
        "issues",
        "locations",
        "submittals",
        "cost",
        "rfis"
    ]
}
Show Less
The response contains the updated parameter settings for your specified data request.

Documentation /BIM 360 API /How-to Guide
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

Documentation /BIM 360 API /How-to Guide
Download Files from BIM 360 Document Management (new)
This tutorial demonstrates how to download files from BIM 360 Document Management. The steps include finding the ID of the folder that contains the file, locating the storage object for the file, generating a signed S3 URL, and downloading the file from the signed S3 URL.

Note that you can only download files that are in the BIM 360 Project Files folder or in a folder nested under the Project Files folder.

For more details about BIM 360 file management, see the Data Management API.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with data:create data:read and data:write scopes.
Verify that you have access to the relevant BIM 360 account and BIM 360 project.
Note the name of the BIM 360 account, project, and folder that contains the file you want to download.
Step 1: Find the Hub ID for the BIM 360 Account
The first few steps of the tutorial demonstrate how to find the ID of the folder that contains the file you want to download, which invovles iterating through several Data Management endpoints.

Call GET hubs to find the hub ID for the BIM 360 account that contains the file you want to download.

Note that the BIM 360 account ID corresponds to a Data Management hub ID. To convert an account ID into a hub ID you need to add a “b." prefix. For example, an account ID of c8b0c73d-3ae9 translates to a hub ID of b.c8b0c73d-3ae9.

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
In this example, assume that the account (and the corresponding Data Management hub) that contains the file you want to download is called My First Account.

Find the hub (data.name), and note the hub ID - b.cGVyc29uYWw6cGUyOWNjZjMy.

Step 2: Find the Project ID
Use the hub ID (b.cGVyc29uYWw6cGUyOWNjZjMy) to call GET hubs/:hub_id/projects to get a list of all the projects in the hub. Find the project ID of the project that contains the folder you want to download the file from.

Note that the project ID in BIM 360 corresponds to the project ID in the Data Management API. To convert a project ID in BIM 360 to a project ID in the Data Management API, you need to add a “b." prefix. For example, a project ID of a4be0c34a-4ab7 translates to a project ID of b.a4be0c34a-4ab7.

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

Step 3: Find the Project Files Folder ID
Note that you can only download files from the BIM 360 Project Files folder or to a folder nested under the Project Files folder.

Use the hub ID (b.cGVyc29uYWw6cGUyOWNjZjMy) and the project ID (b.cGVyc29uYWw6d2l) to call GET hubs/:hub_id/projects/:project_id/topFolders to get the Project Files folder ID.

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
      }]
}
Show Less
Find the Project Files folder (data.attributes.name), and note the folder ID (data.id) - urn:adsk.wipprod:fs.folder:co.BJU3PTc4Sd2CmXM492XUiA

If you want to download a file from a folder nested under the Project Files folder, you need to call GET projects/:project_id/folders/:folder_id/contents repeatedly through the hierarchy of folders until you find the Folder ID of the folder you want to upload the file to. For the first iteration, use the Project Files ID (urn:adsk.wipprod:fs.folder:co.BJU3PTc4Sd2CmXM492XUiA).

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
                              "type": "versions:autodesk.bim360:File",
                              "version": "1.0",
                              "schema": {
                                      "href": "https://developer.api.autodesk.com/schema/v1/versions/versions:autodesk.bim360:File-1.0"
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
Congratulations! You have downloaded a file from BIM 360 Document Management.

ocumentation /BIM 360 API /How-to Guide
Export PDF Files from BIM 360 Document Management (new)
This tutorial demonstrates how to export a single-page (sheet) PDF file that was uploaded to BIM 360 Document Management into a new PDF file. The steps include finding the ID of the PDF page you want to export, exporting the page (you can optionally also export markups and hyperlinks), verifying that the asynchronous job is complete, retrieving data you need to download the exported file, and downloading the exported page.

Note that you can only export a page from a PDF file that was uploaded to the Plans folder or to a folder nested under the Plans folder. BIM 360 Document Management splits these files into separate pages (sheets) when they are uploaded, and assigns a separate ID to each page. You can identify exportable PDF files by searching for files with the following combination of properties:

attributes.extension.type: items:autodesk.bim360.Document (identifies all files that are split into separate pages)
attributes.extension.data.sourceFileName: <filename>.pdf (identifies all PDF files)
For more information about the Plans folder, see the Help documentation.

Before You Begin
Register an app.
Provision your app to acquire access to your BIM 360 account.
Acquire a 3-legged OAuth token or a 2-legged OAuth token with data:create data:read and data:write scopes.
Find the account ID and project ID for the PDF page you want to export, by following the first 2 steps of the Download Document tutorial.
Step 1: Find the Folder ID
Find the folder ID by calling GET hubs/:hub_id/projects/:project_id/topFolders using the hub ID (b.cGVyc29uYWw6cGUyOWNjZjMy) and the project ID (b.cGVyc29uYWw6d2l).

Request
curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT"
            "https://developer.api.autodesk.com/project/v1/hubs/b.cGVyc29uYWw6cGUyOWNjZjMy/projects/b.cGVyc29uYWw6d2l/topFolders"
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
              "CONVERT"
              "SPLIT",
              "OCR"
            ],
            "allowedTypes": [
              "items:autodesk.bim360:File",
              "folders:autodesk.bim360:Folder"
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
Find the Plans folder and note the folder ID (data.id) - urn:adsk.wipprod:fs.folder:co.BJU3PTc4Sd2CmXM492XUiA. Note that the Plans folder (and folders nested under the Plans folder) have the following property:attributes.extension.data.actions: SPLIT.

If you want to export a PDF file from a folder nested under the Plans folder, you need to call GET projects/:project_id/folders/:folder_id/contents repeatedly through the hierarchy of folders until you find the folder ID of the folder that contains the PDF file you want to export. To get contents of first level of the Plans folder, use the Plans folder ID (urn:adsk.wipprod:fs.folder:co.BJU3PTc4Sd2CmXM492XUiA).

Step 2: Find the Version ID of the File to Export
Find the latest version ID of the PDF page you want to export using the hub ID (b.cGVyc29uYWw6cGUyOWNjZjMy), the project ID (b.cGVyc29uYWw6d2l), and the URL-encoded folder ID (urn%3Aadsk.wipprod%3Afs.folder%3Aco.BJU3PTc4Sd2CmXM492XUiA) to call GET projects/:project_id/folders/:folder_id/contents.

(If you want to export a different version of the page, use GET projects/:project_id/items/:item_id/versions.)

Request
curl -X GET https://developer.api.autodesk.com/data/v1/projects/b.cGVyc29uYWw6d2l/folders/urn%3Aadsk.wipprod%3Afs.folder%3Aco.BJU3PTc4Sd2CmXM492XUiA/contents
     -H 'authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT'
Response
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
        "displayName": "A-101 FLOOR PLANS",
        "lastModifiedTime": "2017-09-24T07:46:08.0000000Z",
        "lastModifiedUserId": "X9WYLGPNCHSL",
        "lastModifiedUserName": "John Smith",
        "lastModifiedTime": "2017-08-25T08:59:04.0000000Z",
        "lastModifiedUserId": "200906020304322",
        "lastModifiedUserName": "John Smith",
        "hidden": false,
        "extension": {
          "type": "items:autodesk.bim360:Document",
          "version": "1.0",
          "schema": {
            "href": "https://developer.api.autodesk.com/schema/v1/versions/items:autodesk.bim360:Document-1.0"
          },
          "data": {
            "sourceFileName": "floors.pdf"
          }
        }
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
        "displayName": "A-102 FLOOR PLANS",
        "createTime": "2017-08-25T08:58:57.0000000Z",
        "createUserId": "200906020304322",
        "createUserName": "John Smith",
        "lastModifiedTime": "2017-08-25T08:59:04.0000000Z",
        "lastModifiedUserId": "200906020304322",
        "lastModifiedUserName": "John Smith",
        "hidden": false,
        "extension": {
          "type": "items:autodesk.bim360:Document",
          "version": "1.0",
          "schema": {
            "href": "https://developer.api.autodesk.com/schema/v1/versions/items:autodesk.bim360:Document-1.0"
          },
          "data": {
            "sourceFileName": "floors.pdf"
          }
        }
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
            "processState": "PROCESSING_COMPLETE",
            "viewableId": "1",
            "viewableGuid": "d45af981-3086-4145-a952-cbee9a7e7e78",
            "viewableName": "1",
            "viewableOrder": 1,
            "sourceFileName": "floors.pdf"
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
            "processState": "PROCESSING_COMPLETE",
            "viewableId": "2",
            "viewableGuid": "faf6ab96-6cf0-4b3b-9da5-fd5bb3bde9e3",
            "viewableName": "2",
            "viewableOrder": 2,
            "sourceFileName": "floors.pdf"
          }
        }
      }
    }
  ]
}
Show Less
Find the name of page you want to export i.e., included[i].type.attributes.displayName, which is the name that appears in the Document Management UI. For example, A-101 FLOOR PLANS. Note that included[i].type.attributes.name refers to the name BIM 360 assigns to the file. This is sometimes different from the name of the file in the UI. For example, if the filename contains reserved characters. Note the version ID (data.relationships.tip.data.id) - urn:adsk.wipprod:fs.file:vf.15Rg8B38Qp-SEu6HzXlTNg?version=1.

Step 3: Export the BIM 360 PDF File
To export the BIM 360 PDF file into a new PDF file, call POST projects/:project_id/versions/:version_id/exports using the version ID (urn:adsk.wipprod:fs.file:vf.15Rg8B38Qp-SEu6HzXlTNg?version=1) you retrieved in step 2.

Note that the project ID in the BIM 360 API corresponds to the project ID in the Data Management API. To convert a project ID in the Data Management API into a project ID in the BIM 360 API you need to remove the “b." prefix. For example, a project ID of b.a4be0c34a-4ab7 translates to a project ID of a4be0c34a-4ab7.

Note that this endpoint is asynchronous and initiates a job that runs in the background rather than halting execution of your program. You still need to check whether the asynchronous job is complete by calling GET projects/:project_id/versions/:version_id/exports/:export_id.

When exporting the PDF page, you can also export the page’s markups and hyperlinks. You can export hyperlinks that point to external pages, as well as hyperlinks that point to pages within BIM 360 Document Management.

This tutorial explains the following typical workflows:

3.1: Export files without markups or hyperlinks
3.2: Export files with markups
3.3: Export files with hyperlinks
3.1: Export files without markups or hyperlinks
You can export files without any markups or hyperlinks.

Request
curl -X POST \
  https://developer.api.autodesk.com/bim360/docs/v1/projects/c0337487-5b66-422b-a284-c273b424af54/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.15Rg8B38Qp-SEu6HzXlTNg%3Fversion%3D1/exports \
  -H 'authorization: Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6Imp3dF9zeW1tZXRyaWNfa2V5In0' \
  -H 'content-type: application/json'
Response
{
  "id":"225eb2fb-d5b0-44c9-a50a-2c792d833f2e",
  "status":"committed"
}
3.2: Export files with markups
You can export files with markups.

Request
curl -X POST \
  https://developer.api.autodesk.com/bim360/docs/v1/projects/c0337487-5b66-422b-a284-c273b424af54/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.15Rg8B38Qp-SEu6HzXlTNg%3Fversion%3D1/exports \
  -H 'authorization: Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6Imp3dF9zeW1tZXRyaWNfa2V5In0' \
  -H 'content-type: application/json'
  -d '{"includeMarkups": true}'
Response
{
  "id":"345eb2fb-d5b0-44c9-a50a-2c792d833f3f",
  "status":"committed"
}
3.3: Export files with hyperlinks
You can export files with hyperlinks.

Request
curl -X POST \
  https://developer.api.autodesk.com/bim360/docs/v1/projects/c0337487-5b66-422b-a284-c273b424af54/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.15Rg8B38Qp-SEu6HzXlTNg%3Fversion%3D1/exports \
  -H 'authorization: Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6Imp3dF9zeW1tZXRyaWNfa2V5In0' \
  -H 'content-type: application/json' \
  -d '{"includeHyperlinks": true}'
Response
{
  "id":"455eb2fb-d5b0-44c9-a50a-2c792d833f4g",
  "status":"committed"
}
Step 4: Verify the Job is Complete
To verify the status of the export job, and to retrieve the data you need to download the exported file when the export is complete, call GET projects/:project_id/versions/:version_id/exports/:export_id and check the status of the job. When the status is completed, the download data appears in the response.

Request
curl -X GET \
  https://developer.api.autodesk.com/bim360/docs/v1/projects/c0337487-5b66-422b-a284-c273b424af54/versions/urn%3Aadsk.wipprod%3Afs.file%3Avf.15Rg8B38Qp-SEu6HzXlTNg%3Fversion%3D1/exports/225eb2fb-d5b0-44c9-a50a-2c792d833f2e \
  -H 'authorization: Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6Imp3dF9zeW1tZXRyaWNfa2V5In0' \
  -H 'content-type: application/json'
Response
{
  "id":"433d07ec-32a2-44eb-a5eb-b41090bfe932",
  "status":"completed",
  "data":{
    "versionUrn":"dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLnBmM2ZyVTBnVFphT290S1hnMmgxRnc_dmVyc2lvbj0x",
    "resourceId":"urn:adsk.viewing:fs.file:dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLnBmM2ZyVTBnVFphT290S1hnMmgxRnc_dmVyc2lvbj0x/output/qXP_ZA5_3EqJoq5zqvnLHA/h8YAl4KMcEe9-L5SaEXY6A.pdf",
    "signedUrl":"https://autodesk-360-translation-storage.s3.amazonaws.com/dXJuOmFkc2sud2lwcWE6ZnMuZmlsZTp2Zi5wZjNmclUwZ1RaYU9vdEtYZzJoMUZ3P3ZlcnNpb249MQ/output/qXP_ZA5_3EqJoq5zqvnLHA/h8YAl4KMcEe9-L5SaEXY6A.pdf?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEFkaCXVzLWVhc3QtMSJIMEYCIQDNNbuZoazvwW76c8hUdKythQhpfmixh2AviJuykqwbxAIhAIM1ciB8MQj5FXAQMEnP2lVdraat6%2BU5XcH3rBAdLqUhKtsECLL%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMMjM3ODgyMTcyOTEyIgwzc1S4pCpcQPPqfQkqrwQOC9D39XsK8QpayEEZz5jLC69LO6qdMbs7mUJru5F%2Bx0VV0TXxy1vYjqdfH1SHCwW05FA8czaT40oYKmDcVDRV9iVBrxDNbYxuqS0rBK5CeOfzUQAlsl%2FHgFS%2BQ6p4ca5r2dOgG7fOics1ZLz5goqB7eRP7h27KGnGgcFmsZ4mcHlCBSrDz56hppqJfe%2BLoobZbcxkNvlTvMHH2XeXe5TsyMQWkpIT1qwEJnyMV2IlhBy6Inr%2FXCic5ID3H5NJKw9sI9W3ZhLL2nC9w791jjmxNnQAF624G38jC7pE9fN4vdHeytG27ajW291g9Z28ph%2BwK711ZAxXXM5jyApN6IcRI7ZT%2FmeqNwK3tf0JYjaWMY9flsi%2BgOc9Age7U%2FYl9gpPWokv94A4RTpZgaIoDcnPZRjOFhaKlqc%2FPRhfhU82fIchm2ajDUpJxU2R2NLpMcYQrdQwIpvdKskwr%2Bdv0ueQVOCCYy4OSmUSUN1uLvo9xuaevrakvtEw93jHAsrxBeBsiBFIrWYRSYRRxbp%2FWu%2FykQun1%2B35ny5m0aaDjMxSf3MFekcZlycFRTQ10rlsuWM1s9%2BhLpXylNngzG3vHdGkW2bz9OP517BlnXWhY2P34BY%2BoAYR1osK8FBKK4odoSzaysmsi8akSHooHCTHCE2cW%2BBOVpP%2BO2INmJeS9tVkBqVweYfABSDq0SPcS19wIOoErm2S05pJEFWxJsyh%2B4m2YcmKgrq4883NBU4R6eNKMOfYsZcGOqgBZ59tHFFtRgH8HKVbbDAqkt8RxlyxhjhY6d1rixsLsUtJcPcZP%2FZZmV51SH3rGTfg0cMCEHUH1UMQOQCwXPhJq8VQcI6Wyz7ywNuiWwUiC7%2B2ekEAnKrUwfVyLtI0u1ntG4inL9eYVmM%2BO6w7Es2XjCz%2FHms3q1HEHK26rWukyk18TO118virTD7%2BAwU4otL8D5tlV0OLH8t6D%2B%2FwZN3q0Baxj1zbsFlo&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220805T023429Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIATOYXB4XYG76TKVPE%2F20220805%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=b7cdd11b4ad70051d652bf9f0fa7e49e24b08c800f71211c495d53db2c0509d8"
  }
}
Show Less
Note the signedUrl (data.signedUrl) that you can use for downloading the exported file.

Step 5: Download the PDF File
Download the exported file using the data.signedUrl attribute you retrieved from the the previous step. You can request the signedUrl directly without adding any headers.

Request
curl -X 'GET' -v 'https://autodesk-360-translation-storage.s3.amazonaws.com/dXJuOmFkc2sud2lwcWE6ZnMuZmlsZTp2Zi5wZjNmclUwZ1RaYU9vdEtYZzJoMUZ3P3ZlcnNpb249MQ/output/qXP_ZA5_3EqJoq5zqvnLHA/h8YAl4KMcEe9-L5SaEXY6A.pdf?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEFkaCXVzLWVhc3QtMSJIMEYCIQDNNbuZoazvwW76c8hUdKythQhpfmixh2AviJuykqwbxAIhAIM1ciB8MQj5FXAQMEnP2lVdraat6%2BU5XcH3rBAdLqUhKtsECLL%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMMjM3ODgyMTcyOTEyIgwzc1S4pCpcQPPqfQkqrwQOC9D39XsK8QpayEEZz5jLC69LO6qdMbs7mUJru5F%2Bx0VV0TXxy1vYjqdfH1SHCwW05FA8czaT40oYKmDcVDRV9iVBrxDNbYxuqS0rBK5CeOfzUQAlsl%2FHgFS%2BQ6p4ca5r2dOgG7fOics1ZLz5goqB7eRP7h27KGnGgcFmsZ4mcHlCBSrDz56hppqJfe%2BLoobZbcxkNvlTvMHH2XeXe5TsyMQWkpIT1qwEJnyMV2IlhBy6Inr%2FXCic5ID3H5NJKw9sI9W3ZhLL2nC9w791jjmxNnQAF624G38jC7pE9fN4vdHeytG27ajW291g9Z28ph%2BwK711ZAxXXM5jyApN6IcRI7ZT%2FmeqNwK3tf0JYjaWMY9flsi%2BgOc9Age7U%2FYl9gpPWokv94A4RTpZgaIoDcnPZRjOFhaKlqc%2FPRhfhU82fIchm2ajDUpJxU2R2NLpMcYQrdQwIpvdKskwr%2Bdv0ueQVOCCYy4OSmUSUN1uLvo9xuaevrakvtEw93jHAsrxBeBsiBFIrWYRSYRRxbp%2FWu%2FykQun1%2B35ny5m0aaDjMxSf3MFekcZlycFRTQ10rlsuWM1s9%2BhLpXylNngzG3vHdGkW2bz9OP517BlnXWhY2P34BY%2BoAYR1osK8FBKK4odoSzaysmsi8akSHooHCTHCE2cW%2BBOVpP%2BO2INmJeS9tVkBqVweYfABSDq0SPcS19wIOoErm2S05pJEFWxJsyh%2B4m2YcmKgrq4883NBU4R6eNKMOfYsZcGOqgBZ59tHFFtRgH8HKVbbDAqkt8RxlyxhjhY6d1rixsLsUtJcPcZP%2FZZmV51SH3rGTfg0cMCEHUH1UMQOQCwXPhJq8VQcI6Wyz7ywNuiWwUiC7%2B2ekEAnKrUwfVyLtI0u1ntG4inL9eYVmM%2BO6w7Es2XjCz%2FHms3q1HEHK26rWukyk18TO118virTD7%2BAwU4otL8D5tlV0OLH8t6D%2B%2FwZN3q0Baxj1zbsFlo&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20220805T023429Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIATOYXB4XYG76TKVPE%2F20220805%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=b7cdd11b4ad70051d652bf9f0fa7e49e24b08c800f71211c495d53db2c0509d8'
Response:
Status Code: 200 OK
Content-Type:application/pdf
Content-Length:90616
Etag:8370fe54955cb4d7ab9967c7933c8210

with chunked content body


Documentation /BIM 360 API /How-to Guide
Retrieve a User’s Folder Permissions
This tutorial demonstrates how to retrieve a user’s permissions for a folder in BIM 360 Document Management.

The complete list of the user’s permissions for the folder is the aggregate of the user’s individual permissions combined with the permissions of the company that was assigned to the user (if that company was also assigned to the folder), and the permissions of any roles that were assigned to the user (if those roles were also assigned to the folder).

The tutorial steps include retrieving the user’s permissions for the folder, retrieving the roles and companies that were assigned to the folder, and retrieving the company and roles that were assigned to the user.

For more infomation about folder permissions, see the Help documentation.

Before You Begin
Register an app.
Provision your app to acquire access to your BIM 360 account to both BIM 360 Account Administration and Document Management.
Acquire a 3-legged OAuth token or a 2-legged OAuth token with account:read and data:create scopes.
Find the project ID and folder ID of the folder that you want to find the user’s permissions for, by following the initial steps of the Upload Files tutorial.
Step 1: Retrieve Folder Permissions
Call Get permissions using the project ID and folder ID to get all permissions for the folder, including the user’s individual permissions, and the permissions of the comapanies and roles that were assigned to the folder.

curl -X GET \
  https://developer.api.autodesk.com/bim360/docs/v1/projects/5a9ac886-0441-44da-a64a-bbea5b1e2ba3/folders/urn%3Aadsk.wipprod%3Afs.folder%3Aco.hGZHbcx2QHufgVMs_IDFlg/permissions \
  -H 'Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT' \
[
    {
        "subjectId": "12ea2c20-1fde-43ad-b4ec-6d4c4ca84994",
        "autodeskId": "WDF5NJDPVJUV",
        "name": "Tom",
        "email": "tom@autodesk.com",
        "userType": "PROJECT_MEMBER",
        "subjectStatus": "ACTIVE",
        "subjectType": "USER",
        "actions": [
            "VIEW",
            "DOWNLOAD",
            "COLLABORATE"
        ],
        "inheritActions": [
            "VIEW",
            "COLLABORATE"
        ]
    },
    {
        "subjectId": "7cd13d3a-1b53-4747-b332-2252d2d19808",
        "autodeskId": "28658742",
        "name": "Architect",
        "subjectStatus": "ACTIVE",
        "subjectType": "ROLE",
        "actions": [],
        "inheritActions": [
            "PUBLISH"
        ]
    }
]
Show Less
Find the relevant user, and note the user’s individual permissions (actions and inheritActions). See the documentation for information about how to convert the actions into BIM 360 permission levels. Also note the user’s subjectId (12ea2c20-1fde-43ad-b4ec-6d4c4ca84994) for the next step.

The complete list of the user’s permissions is the aggregate of the user’s individual permissions combined with the permissions of the company (subjectType) that was assigned to the user (if that company was also assigned to the folder), and the permissions of any roles (subjectType) that were assigned to the user (if those roles were also assigned to the folder).

Note also the subjectId that corresponds to each role and company (subjectType). In the next step, you need to check whether any of the companies or roles (subjectId) were also assigned to the user.

Step 2: Retrieve the Company and Roles Assigned to the User
Call GET projects/users/:id using the user’s ID that you retrieved from the previous step ("subjectId": "12ea2c20-1fde-43ad-b4ec-6d4c4ca84994"), and the project ID to get information about the company and roles that were assigned to the user.

curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT" "https://developer.api.autodesk.com/bim360/admin/v1/projects/5a9ac886-0441-44da-a64a-bbea5b1e2ba3/users/12ea2c20-1fde-43ad-b4ec-6d4c4ca84994"
{
    "id": "12ea2c20-1fde-43ad-b4ec-6d4c4ca84994",
    "email": "tom@autodesk.com",
    "name": "Tom",
    "autodeskId": "WDF5NJDPVJUV",
    "companyId": "572c7a25-bf4b-4f21-bbe5-ff4a806be56e",
    "roleIds": [
        "7cd13d3a-1b53-4747-b332-2252d2d19808"
    ],
    "services": [
        {
            "serviceName": "documentManagement",
            "access": "member"
        }
    ],
    "accessLevels": {
        "accountAdmin": true,
        "projectAdmin": true,
        "executive": false
    }
}
Show Less
In this step you need to do the following:

Note whether a company (results.companyId) is assigned to the user.
Check whether any subjectTypes in the previous step are companies (COMPANY), and whether the subjectId of any of the companies match results.companyId.
Note whether any roles (results.roleIds) are assigned to the user.
Check whether any subjectTypes in the previous step are roles (ROLE), and whether the subjectId of any of the roles match results.roleId.
In this example, the user was assigned a company, however, in the previous step there is no subjectType with a value of COMPANY, which means that no company has been assigned to the folder. The user was assigned a role ("roleIds": ["7cd13d3a-1b53-4747-b332-2252d2d19808"]), and in the previous step there is a subjectType with a value of ROLE. The subjectId of the role matches the roleIds, which means that the role (Architect) has been assigned to both the user and the folder. We can therefore conclude that the user had been assigned permissions associated with that role - PUBLISH.

The complete list of the user’s permissions for the folder is, VIEW, DOWNLOAD, COLLABORATE, PUBLISH.

Documentation /BIM 360 API /How-to Guide
Retrieve an Issues Container ID
This tutorial demonstrates how to retrieve an issues container ID for a BIM 360 project. Each BIM 360 project is assigned an issues container (issueContainerId) that stores all the issues data for the project. The issues container ID is used to call the issues endpoints. To retrieve the ID, you need to call several Data Management endpoints.

Note that this tutorial is the same for BIM 360 Issues v1 and BIM 360 Issues v2.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with the data:read scope.
Verify that you have access to the relevant BIM 360 account and BIM 360 project. (To create a new BIM 360 project, see POST projects)
Step 1: Find the Hub ID
You first need to call GET hubs to find the hub ID for your BIM 360 account.

Note that the BIM 360 account ID corresponds to a Data Management hub ID. To convert an account ID into a hub ID you need to add a “b." prefix. For example, an account ID of c8b0c73d-3ae9 translates to a hub ID of b.c8b0c73d-3ae9.

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
Show More
In this example, assume that the project you want the container for is in My First Account hub.

Step 2: Find the Issues Container ID for the Project
Use the BIM 360 hub ID that you retrieved in the previous step (b.cGVyc29uYWw6cGUyOWNjZjMy) to call GET hubs/:hub_id/projects, and retrieve a list of all the projects in the hub the user has access to. In this example, we have added a filter to only return details of a specific project (Demo Project).

Request
curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT" "https://developer.api.autodesk.com/project/v1/hubs/b.cGVyc29uYWw6cGUyOWNjZjMy/projects?filter%5Battributes.name%5D=Demo%20Project"
Response
The response payload includes the issues container ID (data.relationships.issues.data.id).

{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "https://developer.api.autodesk.com/project/v1/hubs/b.cGVyc29uYWw6cGUyOWNjZjMy/projects"
    }
  },
  "data": [
    {
      "type": "projects",
      "id": "b.cGVyc29uYWw6cGUyOWNjZjMyI0QyMDE2MDUyNDEyOTI5NzY",
      "attributes": {
        "name": "My First Project",
        "extension": {
          "type": "projects:autodesk.bim360:Project",
          "version": "1.0",
          "schema": {
            "href": "https://developer.api.autodesk.com/schema/v1/versions/projects%3Aautodesk.bim360%3AProject-1.0"
          },
          "data": {}
        }
      },
      "links": {
        "self": {
          "href": "https://developer.api.autodesk.com/project/v1/hubs/b.cGVyc29uYWw6cGUyOWNjZjMy/projects/b.57be304852e74856a61bf25acebc200f"
        }
      },
      "relationships": {
        "hub": {
          "data": {
            "type": "hubs",
            "id": "b.cGVyc29uYWw6cGUyOWNjZjMy"
          },
          "links": {
            "related": {
              "href": "https://developer.api.autodesk.com/project/v1/hubs/b.cGVyc29uYWw6cGUyOWNjZjMy"
            }
          }
        },
        "rootFolder": {
          "data": {
            "type": "folders",
            "id": "urn:adsk.wipprod:fs.folder:co.uvDiLQ5DRYidDQ_EFW1OOg"
          },
          "meta": {
            "link": {
              "href": "https://developer.api.autodesk.com/data/v1/projects/b.57be304852e74856a61bf25acebc200f/folders/urn%3Aadsk.wipprod%3Afs.folder%3Aco.uvDiLQ5DRYidDQ_EFW1OOg"
            }
          }
        },
        "topFolders": {
          "links": {
            "related": {
              "href": "https://developer.api.autodesk.com/project/v1/hubs/b.cGVyc29uYWw6cGUyOWNjZjMy/projects/b.57be304852e74856a61bf25acebc200f/topFolders"
            }
          }
        },
        "issues": {
          "data": {
            "type": "issueContainerId",
            "id": "be00f32e-c03c-4c7b-9ec4-d2614bf1980c"
          }
        }
      }
    }
  ]
}

Documentation /BIM 360 API /How-to Guide
Retrieve Issues (new)
This tutorial demonstrates how to retrieve a project’s issue IDs. The steps include retrieving the container ID for the project and retrieving a list of the issue IDs. Each project is assigned a container that stores all the issues for the project. You need to use the Data Management API to retrieve the container ID for the project.

There are two types of issues:

Issues that are associated with a project but not associated with a specific document.
Issues associated with a specific document (pushpin issues).
Note that we support managing issues that are associated with a project. However, regarding issues associated with a specific document, we only currently support tracking these issues, but not creating, updating or locating the issues within the document.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with the data:read scope.
Verify that you have access to the relevant BIM 360 account and BIM 360 project. (To create a new BIM 360 project, see POST projects)
Step 1: Find the Hub ID
You first need to call GET hubs to find the hub ID for your BIM 360 account.

Note that the BIM 360 account ID corresponds to a Data Management hub ID. To convert an account ID into a hub ID you need to add a “b." prefix. For example, an account ID of c8b0c73d-3ae9 translates to a hub ID of b.c8b0c73d-3ae9.

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
In this example, assume that the project you want the container for is in My First Account hub.

Step 2: Find the Issues Container ID for the Project
Use the BIM 360 hub ID that you retrieved in the previous step (b.cGVyc29uYWw6cGUyOWNjZjMy) to call GET hubs/:hub_id/projects, and retrieve a list of all the projects in the hub the user has access to. In this example, we have added a filter to only return details of a specific project (My First Project).

Request
curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT" "https://developer.api.autodesk.com/project/v1/hubs/b.cGVyc29uYWw6cGUyOWNjZjMy/projects?filter%5Battributes.name%5D=My%20First%20Project"
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
  "data": [
    {
      "type": "projects",
      "id": "b.cGVyc29uYWw6cGUyOWNjZjMyI0QyMDE2MDUyNDEyOTI5NzY",
      "attributes": {
        "name": "My First Project",
        "extension": {
          "type": "projects:autodesk.bim360:Project",
          "version": "1.0",
          "schema": {
            "href": "https://developer.api.autodesk.com/schema/v1/versions/projects%3Aautodesk.core%3AProject-1.0"
          },
          "data": {}
        }
      },
      "links": {
        "self": {
          "href": "https://developer.api.autodesk.com/project/v1/hubs/b.cGVyc29uYWw6cGUyOWNjZjMy/projects/b.57be304852e74856a61bf25acebc200f"
        }
      },
      "relationships": {
        "hub": {
          "data": {
            "type": "hubs",
            "id": "b.cGVyc29uYWw6cGUyOWNjZjMy"
          },
          "links": {
            "related": {
              "href": "https://developer.api.autodesk.com/project/v1/hubs/b.cGVyc29uYWw6cGUyOWNjZjMy"
            }
          }
        },
        "rootFolder": {
          "data": {
            "type": "folders",
            "id": "urn:adsk.wipprod:fs.folder:co.uvDiLQ5DRYidDQ_EFW1OOg"
          },
          "meta": {
            "link": {
              "href": "https://developer.api.autodesk.com/data/v1/projects/b.57be304852e74856a61bf25acebc200f/folders/urn%3Aadsk.wipprod%3Afs.folder%3Aco.uvDiLQ5DRYidDQ_EFW1OOg"
            }
          }
        },
        "topFolders": {
          "links": {
            "related": {
              "href": "https://developer.api.autodesk.com/project/v1/hubs/b.cGVyc29uYWw6cGUyOWNjZjMy/projects/b.57be304852e74856a61bf25acebc200f/topFolders"
            }
          }
        },
        "issues": {
          "data": {
            "type": "issueContainerId",
            "id": "be00f32e-c03c-4c7b-9ec4-d2614bf1980c"
          }
        }
      }
    }
  ]
}
Show Less
The response payload includes the container ID (data.relationships.issues.data.id).

Step 3: Find the Issue IDs
Use the container ID (be00f32e-c03c-4c7b-9ec4-d2614bf1980cfor) to retrieve the project’s issues, by calling GET issues

request
curl "https://developer.api.autodesk.com/issues/v2/containers/6c8e8341-a4da-4959-a90d-e3b16c60ffd4/issues" -X GET \
  -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT"
response
{
  "pagination": {
      "limit": 100,
      "offset": 0,
      "totalResults": 2
  },
  "results": [
      {
          "id": "788bc959-233f-4307-b828-26794682ec4d",
          "containerId": "6c8e8341-a4da-4959-a90d-e3b16c60ffd4",
          "displayId": 1,
          "rootCauseId": null,
          "title": "test 1",
          "description": null,
          "issueTypeId": "a2b12543-e488-4578-bd4d-41212383ff5e",
          "issueSubtypeId": "a0a1b5a4-2c72-4bca-8de2-f2d0e2aa0e86",
          "status": "open",
          "assignedTo": null,
          "assignedToType": null,
          "dueDate": null,
          "locationId": null,
          "locationDetails": null,
          "snapshotUrn": null,
          "linkedDocuments": [],
          "links": [],
          "ownerId": "U6H9J8Z78B8N",
          "officialResponse": {
              "response": null,
              "respondedAt": null,
              "respondedBy": null
          },
          "permittedAttributes": [
              "title",
              "description",
              "issueTypeId",
              "issueSubtypeId",
              "status",
              "assignedTo",
              "assignedToType",
              "dueDate",
              "locationId",
              "locationDetails",
              "linkedDocuments",
              "links",
              "ownerId",
              "rootCauseId",
              "officialResponse",
              "customAttributes",
              "clientUpdatedAt",
              "snapshotUrn"
          ],
          "permittedActions": [
              "add_comment",
              "add_attachment",
              "assign_all",
              "clear_assignee"
          ],
          "commentCount": 0,
          "attachmentCount": 0,
          "openedBy": "U6H9J8Z78B8N",
          "openedAt": "2021-06-22T06:59:57.556Z",
          "closedBy": null,
          "closedAt": null,
          "createdBy": "U6H9J8Z78B8N",
          "createdAt": "2021-06-22T06:59:57.568Z",
          "updatedBy": "U6H9J8Z78B8N",
          "updatedAt": "2022-09-12T08:06:42.539Z",
          "issueTemplateId": null,
          "customAttributes": [],
          "permittedStatuses": [
              "open",
              "answered",
              "closed",
              "void"
          ]
      },
      {
          "id": "59c74845-ab31-44d1-8598-04b8a5a560b0",
          "containerId": "b22aafc0-f586-416d-bdd9-17667dc2e117",
          "displayId": 31,
          "rootCauseId": null,
          "title": "New Item",
          "description": null,
          "issueTypeId": "3456d343-614d-4ea6-85c8-14bd333ae6b6",
          "issueSubtypeId": "478be241-e9c8-4447-9577-05d1a3faaa0b",
          "status": "open",
          "assignedTo": null,
          "assignedToType": null,
          "dueDate": null,
          "locationId": null,
          "locationDetails": null,
          "snapshotUrn": "urn:adsk.objects:os.object:ng-issues-prod-b22aafc0-f586-416d-bdd9-17667dc2e117/e74861ce-f490-4dc1-a17f-5e70e2d810a3",
          "linkedDocuments": [
              {
                  "type": "TwoDVectorPushpin",
                  "urn": "urn:adsk.wipprod:dm.lineage:vnjsJaDmQh6OOBnYgzwUXQ",
                  "createdBy": "...",
                  "createdAt": "2022-11-28T12:48:37.188Z",
                  "createdAtVersion": 1,
                  "closedBy": null,
                  "closedAt": null,
                  "closedAtVersion": null,
                  "details": {
                      "viewable": {
                          "id": "05babd63-a4ad-5c53-b02b-9a8574bcefb7",
                          "guid": "05babd63-a4ad-5c53-b02b-9a8574bcefb7",
                          "name": "03 Floor Plan.ifc",
                          "is3D": true,
                          "viewableId": "03 Floor Plan.ifc"
                      },
                      "position": {
                          "x": -106.77637888241387,
                          "y": -60.76041506179583,
                          "z": 6.664661474679461
                      },
                      "objectId": 309,
                      "externalId": "2G_tjpeeOI4000000009_c",
                      "viewerState": {
                          "seedURN": "dXJuOmFkc2sud2lwcHJvZDpmcy",
                          "viewport": {
                              "up": [
                                  0,
                                  0,
                                  1
                              ],
                              "eye": [
                                  "103.94791412353516",
                                  "-277.0862121582031",
                                  "1.7852157354354858"
                              ],
                              "name": "",
                              "target": [
                                  "103.94791412353516",
                                  "68.5",
                                  "1.7852157354354858"
                              ],
                              "pivotPoint": [
                                  "103.94791412353516",
                                  "68.5",
                                  "1.7852157354354858"
                              ],
                              "projection": "perspective",
                              "aspectRatio": 1.7908653846153846,
                              "fieldOfView": 44.99999100695533,
                              "worldUpVector": [
                                  0,
                                  0,
                                  1
                              ],
                              "isOrthographic": false,
                              "distanceToOrbit": 345.5862121582031
                          },
                          "cutplanes": [],
                          "objectSet": [
                              {
                                  "id": [],
                                  "hidden": [],
                                  "idType": "lmv",
                                  "isolated": [],
                                  "explodeScale": 0
                              }
                          ],
                          "globalOffset": {
                              "x": 103.9479166815678,
                              "y": 68.49999999999999,
                              "z": 1.7852156956990575
                          },
                          "renderOptions": {
                              "toneMap": {
                                  "method": 1,
                                  "exposure": -7,
                                  "lightMultiplier": -1e-20
                              },
                              "appearance": {
                                  "ghostHidden": true,
                                  "antiAliasing": true,
                                  "displayLines": true,
                                  "ambientShadow": false,
                                  "displayPoints": true,
                                  "swapBlackAndWhite": false,
                                  "progressiveDisplay": true
                              },
                              "environment": "Boardwalk",
                              "ambientOcclusion": {
                                  "radius": 13.123359580052492,
                                  "enabled": false,
                                  "intensity": 1
                              }
                          },
                          "attributesVersion": 2
                      }
                  }
              }
          ],
          "links": [
              {
                  "type": "checklist",
                  "data": {
                      "urn1": "urn:adsk.checklists.cs.instance.item:b22aafc0-f586-416d-bdd9-17667dc2e117/87252924",
                      "urn2": "urn:adsk.checklists.cs.instance.section:b22aafc0-f586-416d-bdd9-17667dc2e117/14060247",
                      "urn3": "urn:adsk.checklists.cs.instance:b22aafc0-f586-416d-bdd9-17667dc2e117/2695283"
                  }
              }
          ],
          "ownerId": "...",
          "officialResponse": {
              "response": null,
              "respondedAt": null,
              "respondedBy": null
          },
          "permittedAttributes": [
              "title",
              "description",
              "issueTypeId",
              "issueSubtypeId",
              "status",
              "assignedTo",
              "assignedToType",
              "dueDate",
              "locationId",
              "locationDetails",
              "linkedDocuments",
              "links",
              "ownerId",
              "rootCauseId",
              "officialResponse",
              "customAttributes",
              "clientUpdatedAt",
              "snapshotUrn"
          ],
          "permittedActions": [
              "add_comment",
              "add_attachment",
              "assign_all",
              "clear_assignee"
          ],
          "commentCount": 0,
          "attachmentCount": 0,
          "openedBy": "...",
          "openedAt": "2022-11-28T12:31:27.134Z",
          "closedBy": null,
          "closedAt": null,
          "createdBy": "...",
          "createdAt": "2022-11-28T12:31:27.339Z",
          "clientCreatedAt": "2022-11-28T12:31:27.134Z",
          "updatedBy": "...",
          "updatedAt": "2022-11-28T12:48:44.335Z",
          "clientUpdatedAt": "2022-11-28T12:48:37.187Z",
          "issueTemplateId": null,
          "customAttributes": [],
          "permittedStatuses": [
              "open",
              "work_completed",
              "ready_to_inspect",
              "in_dispute",
              "not_approved",
              "closed",
              "void"
          ]
      }
  ]
}
Show Less
The response payload includes the issues IDs (results.id).

Documentation /BIM 360 API /How-to Guide
Retrieve Issue Custom Attributes Mapped to an Issue Type (new)
This tutorial demonstrates how to retrieve issue custom attributes mapped to a specific issue type or sub-type.

In BIM 360 Project Admin you can create issue custom attributes and add them to issue types and issue sub-types in three different ways:

Add custom attributes to all issue types (container) in the project; all types and sub-types inherit the mapping.
Add custom attributes to a specific type; the type’s sub-types inherit the mapping.
Add custom attributes to a specific sub-type.
../../../_images/custom-issue-attributes.jpg
For more information see the help documentation.

You can retrieve custom attributes that were added to a type or sub-type by calling GET issue-attribute-mappings, however, it only returns custom attributes that were directly added to the types and sub-types; it does not retrieve custom attributes that were inherited by the types or subtypes. This tutorial explains how to retrieve both custom attributes that were directly added to a type or sub-type and custom attributes that they inherited. The steps include retrieving the ID of the type or sub-type, finding the ID of the sub-type’s type (only relevant if you want to find the mapping for a sub-type), and retrieving all the custom attributes that were added to the type or sub-type.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with the data:read scope.
Verify that you have access to the relevant BIM 360 account and BIM 360 project. (To create a new BIM 360 project, see POST projects).
Find the Issues container ID for the project. In this example, assume the container ID is e59adc9d-2677-4afc-a800-4bc42101f7d8.
Step 1: Find the Type ID
You first need to call GET issue-types to find the ID of the issue type or sub-type you want to find the custom attribute mappings for. Note that to include sub-type IDs in the response payload, you need to add the include=subtypes parameter to the request.

Request
curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT" "https://developer.api.autodesk.com/issues/v2/containers/2b26ddea-34a8-4f11-b352-2a1406ec454e/issue-types?include=subtypes"
Response
{
"pagination": {
    "limit": 200,
    "offset": 0,
    "totalResults": 1
},
"results": [
    {
        "id": "72b4d9a9-52c5-41a2-8e09-c119f590b183",
        "containerId": "e59adc9d-2677-4afc-a800-4bc42101f7d8",
        "title": "Coordination",
        "createdBy": "System",
        "updatedBy": "System",
        "deletedBy": null,
        "statusSet": "basic",
        "createdAt": "2019-01-08T23:31:30.163Z",
        "updatedAt": "2019-01-08T23:31:30.163Z",
        "deletedAt": null,
        "subtypes": [
            {
                "id": "65d1d70f-c996-4c4d-8968-afb3447a3a50",
                "issueTypeId": "72b4d9a9-52c5-41a2-8e09-c119f590b183",
                "title": "Coordination",
                "createdBy": "System",
                "updatedBy": "System",
                "deletedBy": null,
                "createdAt": "2019-01-08T23:31:30.170Z",
                "updatedAt": "2019-01-08T23:31:30.170Z",
                "deletedAt": null,
                "isActive": true,
                "orderIndex": 0,
                "isReadOnly": true,
                "permittedActions": [
                    "change_order"
                ],
                "permittedAttributes": []
            },
            {
                "id": "0d54731e-6bbc-4d77-949b-1ced6b0292da",
                "issueTypeId": "72b4d9a9-52c5-41a2-8e09-c119f590b183",
                "title": "Clash",
                "createdBy": "System",
                "updatedBy": "System",
                "deletedBy": null,
                "createdAt": "2019-01-08T23:31:30.170Z",
                "updatedAt": "2019-01-08T23:31:30.170Z",
                "deletedAt": null,
                "isActive": true,
                "orderIndex": 1,
                "isReadOnly": true,
                "permittedActions": [
                    "change_order",
                    "edit"
                ],
                "permittedAttributes": [
                    "isActive"
                ]
            }
        ],
        "isActive": true,
        "orderIndex": 1,
        "permittedActions": [
            "change_order",
            "edit"
        ],
        "permittedAttributes": [
            "isActive"
        ]
    }
]
}
Show More
If you want to find the custom attributes that were added to a type, for example Coordination, note the type ID (results.id) - 72b4d9a9-52c5-41a2-8e09-c119f590b183. You will also need the container ID (e59adc9d-2677-4afc-a800-4bc42101f7d8) so that you can check if any custom attributes were added directly to the container and were inherited by the type.

If you want to find the custom attributes that were added to a sub-type, for example, Clash, you need to do the following:

Note the sub-type ID (results.subtypes.id) - 0d54731e-6bbc-4d77-949b-1ced6b0292da.
Note the type ID of the sub-type to check if any custom attributes were added directly to the type and inherited by the sub-type. To find the type ID, check the sub-type’s issueTypeId (results-subtypes.issueTypeId) - 72b4d9a9-52c5-41a2-8e09-c119f590b183.
You will also need the container ID (e59adc9d-2677-4afc-a800-4bc42101f7d8) so that you can check if any custom attributes were added directly to the container and were inherited by the sub-type.
Step 2: Find the Mapped Custom Attributes
Call GET issue-attribute-mappings to find the custom attributes that were added to the type or sub-type.

In this example, assume you want to find the custom attributes that were added to a sub-type (Clash - 0d54731e-6bbc-4d77-949b-1ced6b0292da). You will need to search the results for:

Custom attributes that were directly added to the sub-type (Clash - 0d54731e-6bbc-4d77-949b-1ced6b0292da).
Custom attributes that were added to the sub-type’s type (Coordination - 72b4d9a9-52c5-41a2-8e09-c119f590b183), and were inherited by the sub-type.
Custom attributes were added to the container (e59adc9d-2677-4afc-a800-4bc42101f7d8) and were inherited by the sub-type.
If you only need to find the custom attributes for one sub-type, you can use the filter[mappedItemId] filter to filter out custom attributes that are not associated with the sub-type.

Request
curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT" "https://developer.api.autodesk.com/issues/v2/containers/e59adc9d-2677-4afc-a800-4bc42101f7d8/issue-attribute-mappings?filter[mappedItemId]=0d54731e-6bbc-4d77-949b-1ced6b0292da,72b4d9a9-52c5-41a2-8e09-c119f590b183,e59adc9d-2677-4afc-a800-4bc42101f7d8"
Response
{
 "pagination": {
     "limit": 200,
     "offset": 0,
     "totalResults": 3
 },
 "results": [
             {
         "id": "86afb15e-09cb-46aa-8b73-c01e2f43bfe5",
         "containerId": "e59adc9d-2677-4afc-a800-4bc42101f7d8",
         "attributeDefinitionId": "c41750ab-9189-4d0e-9b80-c9ac0f9a1a62",
         "mappedItemId": "e59adc9d-2677-4afc-a800-4bc42101f7d8",
         "mappedItemType": "container",
         "order": 0,
         "isRequired": false,
         "createdBy": "System",
         "updatedBy": "System",
         "deletedBy": null,
         "createdAt": "2019-01-31T16:44:31.190Z",
         "updatedAt": "2019-01-31T16:44:31.190Z",
         "deletedAt": null,
         "permittedActions": [
             "change_order",
             "edit",
             "delete"
         ],
         "permittedAttributes": [
             "isRequired"
         ]
     },
     {
         "id": "c9088c83-70e4-4630-af07-c5e96d084bb8",
         "containerId": "e59adc9d-2677-4afc-a800-4bc42101f7d8",
         "attributeDefinitionId": "7f7e94fb-e00d-4fb6-9cf7-c18bb8e5e891",
         "mappedItemId": "72b4d9a9-52c5-41a2-8e09-c119f590b183",
         "mappedItemType": "issueType",
         "order": 0,
         "isRequired": false,
         "createdBy": "System",
         "updatedBy": "System",
         "deletedBy": null,
         "createdAt": "2019-01-13T09:48:30.425Z",
         "updatedAt": "2019-01-13T09:48:30.425Z",
         "deletedAt": null,
         "permittedActions": [
             "change_order",
             "edit",
             "delete"
         ],
         "permittedAttributes": [
             "isRequired"
         ]
     },
     {
         "id": "75919b67-3716-48e6-b25a-5cda566b8119",
         "containerId": "e59adc9d-2677-4afc-a800-4bc42101f7d8",
         "attributeDefinitionId": "8g3k94fb-e00d-4fb6-9cf7-c18bb8e5c325",
         "mappedItemId": "0d54731e-6bbc-4d77-949b-1ced6b0292da",
         "mappedItemType": "issueSubtype",
         "order": 0,
         "isRequired": false,
         "createdBy": "System",
         "updatedBy": "System",
         "deletedBy": null,
         "createdAt": "2019-01-21T09:58:42.300Z",
         "updatedAt": "2019-01-21T09:58:42.300Z",
         "deletedAt": null,
         "permittedActions": [
             "change_order",
             "edit",
             "delete"
         ],
         "permittedAttributes": [
             "isRequired"
         ]
     }

 ]
}
Show Less
If you need to find the custom attributes (results.attributeDefinitionId) for more than one sub-type, you need to search the results (results.mappedItemId and results.mappedItemType). For example, for the Clash sub-type, you need to search for the following:

Sub-type ID (Clash - 8g3k94fb-e00d-4fb6-9cf7-c18bb8e5c325) - custom attributes that were added directly to the sub-type.
Type ID (Coordination - 7f7e94fb-e00d-4fb6-9cf7-c18bb8e5e891) - custom attributes that were added to the sub-type’s type and inherited by the sub-type.
Container ID (c41750ab-9189-4d0e-9b80-c9ac0f9a1a62) - customer attributes that were added to the container and inherited by the sub-type.
To find more details about the custom attributes (results.attributeDefinitionId) such as the titles and descriptions, call GET issue-attribute-definitions. The value for results.id in GET issue-attribute-definitions corresponds to the value for results.attributeDefinitionId in GET issue-attribute mappings.

Documentation /BIM 360 API /How-to Guide
Retrieve a Locations Container ID
This tutorial demonstrates how to retrieve a container ID for a BIM 360 project. Each BIM 360 project is assigned a locations container (locationsContainerId) that stores all the locations data for the project. The locations container ID is used to call the BIM 360 locations endpoints. To retrieve the ID, you need to call several Data Management endpoints.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with the data:read scope.
Verify that you have access to the relevant BIM 360 account and BIM 360 project. (To create a new BIM 360 project, see POST projects)
Step 1: Find the Hub ID
You first need to call GET hubs to find the hub ID for your BIM 360 account.

Note that the BIM 360 account ID corresponds to a Data Management hub ID. To convert an account ID into a hub ID you need to add a “b." prefix. For example, an account ID of c8b0c73d-3ae9 translates to a hub ID of b.c8b0c73d-3ae9.

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
In this example, assume that the project you want the container for is in My First Account hub.

Step 2: Find the Container ID for the Project
Use the BIM 360 hub ID that you retrieved in the previous step (b.cGVyc29uYWw6cGUyOWNjZjMy) to call GET hubs/:hub_id/projects, and retrieve a list of all the projects in the hub the user has access to. In this example, we have added a filter to only return details of a specific project (Demo Project).

The response payload includes the Locations container ID (data.relationships.locations.id).

Request
curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT" "https://developer.api.autodesk.com/project/v1/hubs/b.cGVyc29uYWw6cGUyOWNjZjMy/projects?filter%5Battributes.name%5D=Demo%20Project"
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "https://developer.api.autodesk.com/project/v1/hubs/b.7fcde01c-738a-4f5e-8a1c-7a8da2381693/projects"
    }
  },
  "data": [
    {
      "type": "projects",
      "id": "b.1f50f9e7-df95-43f9-9366-2fd44cafa768",
      "attributes": {
        "name": "Demo Project",
        "extension": {
          "type": "projects:autodesk.bim360:Project",
          "version": "1.0",
          "schema": {
            "href": "https://developer.api.autodesk.com/schema/v1/versions/projects:autodesk.bim360:Project-1.0"
          },
          "data": {}
        }
      },
      "links": {
        "self": {
          "href": "https://developer.api.autodesk.com/project/v1/hubs/b.7fcde01c-738a-4f5e-8a1c-7a8da2381693/projects/b.1f50f9e7-df95-43f9-9366-2fd44cafa768"
        }
      },
      "relationships": {
        "hub": {
          "data": {
            "type": "hubs",
            "id": "b.7fcde01c-738a-4f5e-8a1c-7a8da2381693"
          },
          "links": {
            "related": {
              "href": "https://developer.api.autodesk.com/project/v1/hubs/b.7fcde01c-738a-4f5e-8a1c-7a8da2381693"
            }
          }
        },
        "rootFolder": {
          "data": {
            "type": "folders",
            "id": "urn:adsk.wipprod:fs.folder:co.xOuT2J3zSdqR4eD_pkd3WQ"
          },
          "meta": {
            "link": {
              "href": "https://developer.api.autodesk.com/data/v1/projects/b.1f50f9e7-df95-43f9-9366-2fd44cafa768/folders/urn:adsk.wipprod:fs.folder:co.xOuT2J3zSdqR4eD_pkd3WQ"
            }
          }
        },
        "topFolders": {
          "links": {
            "related": {
              "href": "https://developer.api.autodesk.com/project/v1/hubs/b.7fcde01c-738a-4f5e-8a1c-7a8da2381693/projects/b.1f50f9e7-df95-43f9-9366-2fd44cafa768/topFolders"
            }
          }
        },
        "locations": {
          "data": {
            "type": "locationsContainerId",
            "id": "cfb0fafd-a3c9-4155-b931-bcd640510ead"
          },
          "meta": {
            "link": {
              "href": "https://developer.api.autodesk.com/bim360/locations/v2/containers/cfb0fafd-a3c9-4155-b931-bcd640510ead/trees/default/nodes"
            }
          }
        }
      }
    }
  ]
}

Documentation /BIM 360 API /How-to Guide
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
Show Less
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
Show Less
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


Documentation /BIM 360 API /How-to Guide
Render Document-related (Pushpin) Issues and RFIs in Your App
This tutorial demonstrates how to use the Viewer SDK to render pushpin issues and RFIs in your app. Pushpins are visual markers that denote the location of a BIM 360 issue or RFI in a document. The Viewer SDK includes an extension that creates and renders pushpin issues and RFIs. This tutorial demonstrates how to use the Viewer SDK to load BIM 360 documents and render pushpins. The steps include finding the version ID of the document the pushpins were added to, initializing the Viewer, loading the document, retrieving the pushpin issue and RFI IDs associated with the document, and rendering the pushpins in the Viewer.

To see a fully working sample, see this Pushpin app.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with viewables:read data:create data:read and data:write scopes.
Upload the file to BIM 360 Document Management.
Add pushpins issues or RFIs to a document in BIM 360, either by creating them in the UI or by using the Create Pushpin Issues in Your App tutorial.
Find the project ID of the document that the issues or RFIs were added to. See the initial steps of the Attachments tutorial for more details.
Verify the ID of the project’s container. For more details see the Retrieve a Container ID tutorial.
Verify that you have access to the relevant BIM 360 account and BIM 360 project.
Read through the Basic Viewer documentation.
Step 1: Find the Item ID and Version ID
Find the item ID and version ID of the document the pushpins were added to by calling GET projects/:project_id/folders/:folder_id/contents with a 3-legged token, using the project ID (b.cGVyc29uYWw6d2l) and the folder ID of the folder that contains the document that the pushpins were added to (urn:adsk.wipprod:fs.folder:co.O7Zwai).

The version ID is used to render the document in the Viewer (step 2).

The item ID is used to filter the pushpins (step 3).

Request
curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT"
    "https://developer.api.autodesk.com/project/v1/projects/b.cGVyc29uYWw6d2l/folders/urn:adsk.wipprod:fs.folder:co.BJU3PTc4Sd2CmXM492XUiA/contents"
Response
{
  "jsonapi": {
      "version": "1.0"
   },
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
                  }
             },
       {
          "type": "items",
          "id": "urn:adsk.wip:dm.lineage:7_5NcbL1Q1GSjRLJe9ffvw",
          "attributes": {
              "displayName": "My First Document",
              "createTime": "2017-10-02T11:25:57.0000000Z",
              "createUserId": "X9WYLGPNCHVK",
              "createUserName": "John Smith",
              "lastModifiedTime": "2017-10-02T11:27:22.0000000Z",
              "lastModifiedUserId": "X9WYLGPNCHVK",
              "lastModifiedUserName": "John Smith",
              "hidden": false,
              "extension": {
                  "type": "items:autodesk.bim360:File",
                  "version": "1.0",
                  "schema": {
                      "href": "https://developer.api.autodesk.com/schema/v1/versions/items:autodesk.bim360:File-1.0"
                  },
                  "data": {}
              }
            ]
         }
 "included": [
      {
          "type": "versions",
          "id": "urn:adsk.wipprod:fs.file:vf.7_5NcbL1Q1GSjRLJe9ffvw?version=1",
          "attributes": {
              "name": "My First Document",
              "displayName": "My First Document",
             "createTime": "2017-10-02T11:25:57.0000000Z",
             "createUserId": "X9WYLGPNCHVK",
             "createUserName": "John Smith",
             "lastModifiedTime": "2017-10-02T11:27:22.0000000Z",
             "lastModifiedUserId": "X9WYLGPNCHVK",
             "lastModifiedUserName": "John Smith",
             "hidden": false,
             "versionNumber": 1,
             "fileType": "ifc",
             "extension": {
                  "type": "versions:autodesk.bim360:File",
                  "version": "1.0",
                  "schema": {
                      "href": "https://developer.api.autodesk.com/schema/v1/versions/versions:autodesk.bim360:File-1.0"
                  },
                  "data": {
                      "processState": "PROCESSING_COMPLETE",
                      "extractionState": "SUCCESS",
                      "splittingState": "NOT_SPLIT",
                      "reviewState": "NOT_IN_REVIEW",
                      "revisionDisplayLabel": "1",
                  }
              }
Show Less
Find the name of the item (data.attributes.displayName), and note the following:

The version ID (included[i].id) - urn:adsk.wipprod:fs.file:7_5NcbL1Q1GSjRLJe9ffvw?version=1, which is used to render the document in the Viewer (step 2). Note that you do not need to encode the version ID to Base64 format since it is already encoded when the document was uploaded to BIM 360 Document Management.

The item ID (data.id) - urn:adsk.wipprod:dm.lineage:7_5NcbL1Q1GSjRLJe9ffvw, which is used to filter the pushpins (step 3).

Step 2: Initialize the Viewer
Initialize the Viewer and load the document and the Pushpin extension using the Viewer SDK.

// Set up the following handles:
var viewerApp;
var PushPinExtensionHandle;

// Initialize the Viewer and load the document (model)
function launchViewer(urn) {
  var options = {
    env: 'AutodeskProduction',
    // Replace <YOUR_ACCESS_TOKEN> with a 3-legged access token.
    getAccessToken: <YOUR_ACCESS_TOKEN>
  };
  // Replace <YOUR_VERSION_ID> with a the version ID of the document.
  var documentId = 'urn:' + <YOUR_VERSION_ID>;

  var config3d = {
    extensions: []
  };
  Autodesk.Viewing.Initializer(options, function onInitialized() {
    viewerApp = new Autodesk.Viewing.ViewingApplication('forgeViewer'); // setting viewerApp handle
    viewerApp.registerViewer(viewerApp.k3D, Autodesk.Viewing.Private.GuiViewer3D, config3d);
    viewerApp.loadDocument(documentId, onDocumentLoadSuccess, onDocumentLoadFailure); // loading document
  });
}

// Select a sheet of the model to display in the Viewer.
function onDocumentLoadSuccess(doc) {

  // The `bubble` object contains metadata about the viewer and its displayed content.
  // Use `bubble.search` to filter for data within the object.
  // The "geometry" type retrieves all of the document's 2D and 3D sheets.
  var viewables = viewerApp.bubble.search({ 'type': 'geometry' });
  if (!viewables.length) {
    return console.error('Document contains no viewables.');
  }

  // In this example, we are using the `viewerApp` handle to select and load the first sheet (view).
  // Alternatively load a different sheet.
  viewerApp.selectItem(viewables[0], onItemLoadSuccess, onItemLoadFail);
}

// Load the Pushpin extension
function onItemLoadSuccess(viewer, item) {
  ...

  // Select pushpin buttons for the Viewer toolbar.
  // By default, the buttons will not appear in the toolbar.
  var extensionOptions = {
     hideIssuesButton: false,
     hideRfisButton: true,
     hideFieldIssuesButton: true,
   };

   // Use the `viewer` reference to call `loadExtension` with the extension name and the extension options:

   viewer.loadExtension('Autodesk.BIM360.Extension.PushPin', extensionOptions)
     .then(function (extension) {
       PushPinExtensionHandle = extension;

       // After the extension loads, call `getIssues`. This is a simple AJAX function that should call
       // your server. The actual `get issues` call should be implemented there using your 3-legged token.
       //
       // Note that in this example we called `getIssues` after the model is rendered in case the Viewer, document or extension fails to load. However, you can call `getIssues` before loading the extension to spare the time it takes to render the model.

       getIssues() // Implement the call; see step 3.
         .then(function(issues) {
            registerOnSelectEvent(issues); // See step 4
            renderIssues(issues); // See step 5
          })
     });
 }
Show Less
Step 3: Retrieve the Issues or RFIs
This tutorial will retrieve pushpin issues.

Within our server, we will implement the GET issues call.

We recommend using the target_urn filter when calling these endpoints so that you only retrieve pushpins associated with the specific document and version. You need to specify the document (the item ID you retrieved in step 1), and the version number (the number at the end of the version ID string you retrieved in step 1), in the followng format: item_id@version_number. For example, urn:adsk.wipprod:dm.lineage:7_5NcbL1Q1GSjRLJe9ffvw@1.

Step 4: Set an Event Listener (optional)
The Pushpin extension offers a number of events. In this example, we are going to listen for the pushpin.selected event, which is fired when the user selects a pushpin. You can set up your app to display pushpin-related information when the pushpin is selected.

registerOnSelectEvent(issues) {
  PushPinExtensionHandle.pushPinManager.addEventListener('pushpin.selected', function (e) {
    if (e.value) {
      // Use the pushpin data (that you retrieved in step 3) to search for the selected pushpin metadata that you can display in the UI.
      var issue = findIssueByLabel(issues, e.value.itemData.label);
      // Implement the function ``findIssueByLabel``, which searches for the pushpin by comparing the pushin data to the event data: `issue.attributes.identifier` === `e.value.itemData.label`.
      // You can choose which data to display and how to display it.
    }
};
Show Less
Step 5: Render Pushpin Data
In order to render the pushpins data you need to traverse all the retrieved issues or RFIs and apply the createItem Pushpins extension function to them.

To rerender all the pushpins on the sheet you first need to remove the current pushpins by using PushPinExtensionHandle.removeAllItems();, and then use the following function:

renderIssues(issues) {
  issues.forEach(function (issue) {
    var issueAttributes = issue.attributes;
    var pushpinAttributes = issue.attributes.pushpin_attributes;
    // Notice the last rendering condition, which will enforce rendering the pushpin on the current sheet.
    // We simply compare the issue sheet metadata against the current sheet.
    if (pushpinAttributes && issueAttributes.sheet_metadata &&
          issueAttributes.sheet_metadata.sheetGuid === viewerApp.selectedItem.guid()) {
      PushPinExtensionHandle.createItem({
        id: issue.id, // The issue ID.
        label: issueAttributes.identifier, // The value displayed when you select the pushpin.
        // The shape and color of the pushpin, in the following format: ``type-status`` (e.g., ``issues-open``).
        status: issue.type && issueAttributes.status.indexOf(issue.type) === -1 ?
                  `${issue.type}-${issueAttributes.status}` : issueAttributes.status,
        position: pushpinAttributes.location, // The x, y, z coordinates of the pushpin.
        type: issue.type, // The issue type.
        objectId: pushpinAttributes.object_id, // (Only for 3D models) The object the pushpin is situated on.
        viewerState: pushpinAttributes.viewer_state // The current viewer state. For example, angle, camera, zoom.
      });
    } // if
  } // forEach
};
Show Less
Step 6: Extra Functionality
Issues and RFIs are associated with a specific sheet, which is why we filtered the pushpins for a specific sheet in the last step. You can allow your users to switch between sheets or display a pushpin on a specific sheet, by using a combination of the above steps. We will, however, go over a few minor details in order make sure everything is perfectly clear.

Note that these extra optional steps are only applicable to Project Files folder files.

Use an External View of Pushpin Data to Display a Pushpin in the Viewer
In order to display a list of pushpin data you can simply use the data from the retrieved issues and RFIs. If you click on the pushpin name in the list of pushpin data, you can configure your app to load the sheet by its GUID and load the pushpin in the sheet:

// If the pushpin is not in the current sheet, switch to the correct sheet to view it.
// Note that this code is similar to step 2, where we described how to load the initial sheet (`onDocumentLoadSuccess`).
if (issue.sheetGuid !== viewerApp.selectedItem.guid()) {
  var viewable = viewerApp.bubble.search({ 'guid': issue.sheetGuid }); // get sheet by guid
  if (!viewable.length) {
    return console.error('Sheet could not be found.');
  }
  // Select sheet to display (callbacks are the same as in `onDocumentLoadSuccess`)
  viewerApp.selectItem(viewable[0], onItemLoadSuccess, onItemLoadFail);
  // To highlight this pushpin in the sheet, use this function `PushPinExtensionHandle.selectOne(issue_id);` within the `onItemLoadSuccess` function.
} else {
  // If the pushpin is in the current sheet, select the pushpin
  PushPinExtensionHandle.selectOne(issue.id);
}
Show Less
Use an External View of Document Sheets to Select Different Sheets
Displaying and interacting with the list of sheets is very similar to displaying the pushpin as described above:

var viewables = viewerApp.bubble.search({ 'type': 'geometry' }); // get all sheets / views
if (!viewables.length) {
  return console.error('Document contains no viewables.');
}
// Select the sheet you want to load.

Documentation /BIM 360 API /How-to Guide
Render Document-related (Pushpin) Issues (V2) and RFIs in Your App
This tutorial demonstrates how to use the Viewer SDK to render pushpin issues and RFIs in your app. Pushpins are visual markers that denote the location of a BIM 360 issue or RFI in a document. The Viewer SDK includes an extension that creates and renders pushpin issues and RFIs. This tutorial demonstrates how to use the Viewer SDK to load BIM 360 documents and render pushpins. The steps include finding the version ID of the document the pushpins were added to, initializing the Viewer, loading the document, retrieving the pushpin issue and RFI IDs associated with the document, and rendering the pushpins in the Viewer.

To see a fully working sample, see this Pushpin app.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with viewables:read data:create data:read and data:write scopes.
Upload the file to BIM 360 Document Management.
Add pushpins issues or RFIs to a document in BIM 360, either by creating them in the UI or by using the Create Pushpin Issues in Your App tutorial.
Find the project ID of the document that the issues or RFIs were added to. See the initial steps of the Attachments tutorial for more details.
Verify the ID of the project’s container. For more details see the Retrieve a Container ID tutorial.
Verify that you have access to the relevant BIM 360 account and BIM 360 project.
Read through the Basic Viewer documentation.
Step 1: Find the Item ID and Version ID
Find the item ID and version ID of the document the pushpins were added to by calling GET projects/:project_id/folders/:folder_id/contents with a 3-legged token, using the project ID (b.cGVyc29uYWw6d2l) and the folder ID of the folder that contains the document that the pushpins were added to (urn:adsk.wipprod:fs.folder:co.O7Zwai).

The version ID is used to render the document in the Viewer (step 2).

The item ID is used to filter the pushpins (step 3).

Request
curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT"
    "https://developer.api.autodesk.com/project/v1/projects/b.cGVyc29uYWw6d2l/folders/urn:adsk.wipprod:fs.folder:co.BJU3PTc4Sd2CmXM492XUiA/contents"
Response
{
  "jsonapi": {
      "version": "1.0"
   },
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
                  }
             },
       {
          "type": "items",
          "id": "urn:adsk.wip:dm.lineage:7_5NcbL1Q1GSjRLJe9ffvw",
          "attributes": {
              "displayName": "My First Document",
              "createTime": "2017-10-02T11:25:57.0000000Z",
              "createUserId": "X9WYLGPNCHVK",
              "createUserName": "John Smith",
              "lastModifiedTime": "2017-10-02T11:27:22.0000000Z",
              "lastModifiedUserId": "X9WYLGPNCHVK",
              "lastModifiedUserName": "John Smith",
              "hidden": false,
              "extension": {
                  "type": "items:autodesk.bim360:File",
                  "version": "1.0",
                  "schema": {
                      "href": "https://developer.api.autodesk.com/schema/v1/versions/items:autodesk.bim360:File-1.0"
                  },
                  "data": {}
              }
            ]
         }
 "included": [
      {
          "type": "versions",
          "id": "urn:adsk.wipprod:fs.file:vf.7_5NcbL1Q1GSjRLJe9ffvw?version=1",
          "attributes": {
              "name": "My First Document",
              "displayName": "My First Document",
             "createTime": "2017-10-02T11:25:57.0000000Z",
             "createUserId": "X9WYLGPNCHVK",
             "createUserName": "John Smith",
             "lastModifiedTime": "2017-10-02T11:27:22.0000000Z",
             "lastModifiedUserId": "X9WYLGPNCHVK",
             "lastModifiedUserName": "John Smith",
             "hidden": false,
             "versionNumber": 1,
             "fileType": "ifc",
             "extension": {
                  "type": "versions:autodesk.bim360:File",
                  "version": "1.0",
                  "schema": {
                      "href": "https://developer.api.autodesk.com/schema/v1/versions/versions:autodesk.bim360:File-1.0"
                  },
                  "data": {
                      "processState": "PROCESSING_COMPLETE",
                      "extractionState": "SUCCESS",
                      "splittingState": "NOT_SPLIT",
                      "reviewState": "NOT_IN_REVIEW",
                      "revisionDisplayLabel": "1",
                  }
              }
Show Less
Find the name of the item (data.attributes.displayName), and note the following:

The version ID (included[i].id) - urn:adsk.wipprod:fs.file:7_5NcbL1Q1GSjRLJe9ffvw?version=1, which is used to render the document in the Viewer (step 2). Note that you do not need to encode the version ID to Base64 format since it is already encoded when the document was uploaded to BIM 360 Document Management.

The item ID (data.id) - urn:adsk.wipprod:dm.lineage:7_5NcbL1Q1GSjRLJe9ffvw, which is used to filter the pushpins (step 3).

Step 2: Initialize the Viewer
Initialize the Viewer and load the document and the Pushpin extension using the Viewer SDK.

// Set up the following handles:
var viewer;
var PushPinExtensionHandle;

// Initialize the Viewer and load the document (model)
function launchViewer(urn) {
  var options = {
    env: 'AutodeskProduction',
    // Replace <YOUR_ACCESS_TOKEN> with a 3-legged access token.
    getAccessToken: <YOUR_ACCESS_TOKEN>
  };
  // Replace <YOUR_VERSION_ID> with a the version ID of the document.
  var documentId = 'urn:' + <YOUR_VERSION_ID>;

  Autodesk.Viewing.Initializer(options, function onInitialized() {
    viewer = new Autodesk.Viewing.GuiViewer3D(document.getElementById('forgeViewer')); // setting viewer handle
    viewer.start();
    Autodesk.Viewing.Document.load(documentId, onDocumentLoadSuccess, onDocumentLoadFailure); // loading document
  });
}

// Select a sheet of the model to display in the Viewer.
function onDocumentLoadSuccess(viewerDocument) {
  // viewerDocument is an instance of Autodesk.Viewing.Document

  // The "geometry" type retrieves all of the document's 2D and 3D sheets.
  var viewables = viewerDocument.getRoot().search({'type':'geometry'});
  if (!viewables.length) {
    return console.error('Document contains no viewables.');
  }
  // In this example, we are using the `viewer` handle to select and load the first sheet (view).
  // Alternatively load a different sheet.
  viewer.loadDocumentNode(viewerDocument, viewables[0]);

  // Load the Pushpin extension
  // Select pushpin buttons for the Viewer toolbar.
  // By default, the buttons will not appear in the toolbar.
  var extensionOptions = {
     hideIssuesButton: false,
     hideRfisButton: true,
     hideFieldIssuesButton: true,
   };

  // Use the `viewer` reference to call `loadExtension` with the extension name and the extension options:

  viewer.loadExtension('Autodesk.BIM360.Extension.PushPin', extensionOptions)
    .then(function (extension) {
      PushPinExtensionHandle = extension;

      // After the extension loads, call `getIssues`. This is a simple AJAX function that should call
      // your server. The actual `get issues` call should be implemented there using your 3-legged token.
      //
      // Note that in this example we called `getIssues` after the model is rendered in case the Viewer, document or extension fails to load. However, you can call `getIssues` before loading the extension to spare the time it takes to render the model.

      getIssues() // Implement the call; see step 3.
        .then(function(issues) {
          registerOnSelectEvent(issues); // See step 4
          renderIssues(issues); // See step 5
        })
    });

}
Show Less
Step 3: Retrieve the Issues or RFIs
This tutorial will retrieve pushpin issues. In order to retrieve rfis, see GET rfis call.

Within our server, we will implement the GET issues call.

We recommend using the linkedDocumentUrn filter when calling these endpoints so that you only retrieve pushpins associated with the specific document and version. You need to specify the document (the item ID you retrieved in step 1), and the version number (the number at the end of the version ID string you retrieved in step 1), in the followng format: item_id@version_number. For example, urn:adsk.wipprod:dm.lineage:7_5NcbL1Q1GSjRLJe9ffvw@1.

Step 4: Set an Event Listener (optional)
The Pushpin extension offers a number of events. In this example, we are going to listen for the pushpin.selected event, which is fired when the user selects a pushpin. You can set up your app to display pushpin-related information when the pushpin is selected.

registerOnSelectEvent(issues) {
  PushPinExtensionHandle.pushPinManager.addEventListener('pushpin.selected', function (e) {
    if (e.value) {
      // Use the pushpin data (that you retrieved in step 3) to search for the selected pushpin metadata that you can display in the UI.
      var issue = findIssueByLabel(issues, e.value.itemData.label);
      // Implement the function ``findIssueByLabel``, which searches for the pushpin by comparing the pushin data to the event data: `issue.attributes.identifier` === `e.value.itemData.label`.
      // You can choose which data to display and how to display it.
    }
};
Show Less
Step 5: Render Pushpin Data
In order to render the pushpins data you need to traverse all the retrieved issues or RFIs and apply the createItem Pushpins extension function to them.

To rerender all the pushpins on the sheet you first need to remove the current pushpins by using PushPinExtensionHandle.removeAllItems();, and then use the following function:

renderIssues(issues) {
  var viewerNode = viewer.model.getDocumentNode();
  issues.forEach(function (issue) {

    // Notice the last rendering condition, which will enforce rendering the pushpin on the current viewable.
    // We simply compare the issue vieawble metadata against the current viewable.
    if (issue.linkedDocuments[0] &&
          issue.linkedDocuments[0].details.viewable.guid === viewerNode.guid()) {
      PushPinExtensionHandle.createItem({
        id: issue.id, // The issue ID.
        label: issue.displayId, // The value displayed when you select the pushpin.
        // The shape and color of the pushpin, in the following format: ``type-status`` (e.g., ``issues-open``).
        status: issue.type && issue.status.indexOf(issue.type) === -1 ?
                  `${issue.type}-${issue.status}` : issue.status,
        position: issue.linkedDocuments[0].details.position, // The x, y, z coordinates of the pushpin.
        type: issue.type, // The issue type.
        objectId: issue.linkedDocuments[0].details.objectId, // (Only for 3D models) The object the pushpin is situated on.
        viewerState: issue.linkedDocuments[0].details.viewerState // The current viewer state. For example, angle, camera, zoom.
      });
    } // if
  } // forEach
};
Show Less
Step 6: Extra Functionality
Issues and RFIs are associated with a specific sheet, which is why we filtered the pushpins for a specific sheet in the last step. You can allow your users to switch between sheets or display a pushpin on a specific sheet, by using a combination of the above steps. We will, however, go over a few minor details in order make sure everything is perfectly clear.

Note that these extra optional steps are only applicable to Project Files folder files.

Use an External View of Pushpin Data to Display a Pushpin in the Viewer
In order to display a list of pushpin data you can simply use the data from the retrieved issues and RFIs. If you click on the pushpin name in the list of pushpin data, you can configure your app to load the sheet by its GUID and load the pushpin in the sheet:

// If the pushpin is not in the current sheet, switch to the correct sheet to view it.
// Note that this code is similar to step 2, where we described how to load the initial sheet (`onDocumentLoadSuccess`).
var issueViewableGuid = issue.linkedDocuments[0].details.viewable.guid;
var viewerNode = viewer.model.getDocumentNode();
if (objectId: issueViewableGuid !== viewerNode.guid()) {
  var viewable = viewerNode.search({ 'guid': issueViewableGuid }); // get sheet by guid
  if (!viewable.length) {
    return console.error('Sheet could not be found.');
  }
  // Select sheet to display (callbacks are the same as in `onDocumentLoadSuccess`)
  viewer.loadModel(viewable[0], {} , onItemLoadSuccess, onItemLoadFail);
  // To highlight this pushpin in the sheet, use this function `PushPinExtensionHandle.selectOne(issue_id);` within the `onItemLoadSuccess` function.
} else {
  // If the pushpin is in the current sheet, select the pushpin
  PushPinExtensionHandle.selectOne(issue.id);
}
Show Less
Use an External View of Document Sheets to Select Different Sheets
Displaying and interacting with the list of sheets is very similar to displaying the pushpin as described above:

var viewables = viewer.model.getDocumentNode().search({ 'type': 'geometry' }); // get all sheets / views
if (!viewables.length) {
  return console.error('Document contains no viewables.');
}
// Select the sheet you want to load.

Documentation /BIM 360 API /How-to Guide
Create Document-related (Pushpin) Issues and RFIs in Your App
This tutorial demonstrates how to use the Viewer SDK to create pushpin issues and RFIs in your app. Pushpins are visual markers that denote the location of a BIM 360 issue or RFI in a document. The Viewer SDK includes an extension that renders pushpin issues and RFIs, or collects payload data for creating issues or RFIs. This tutorial demonstrates how to use the Viewer SDK to load BIM 360 documents and create issue or RFI pushpins from data specified by the end user. The steps include finding the ID of the document you want to add the pushpins to, initializing the Viewer, loading the document, enabling the end user to select a postion and object and creating the pushpin issues and RFIs (on the server side).

Note that you can add pushpins to documents in any BIM 360 Document Management folder. This tutorial demonstrates how to add a pusphin to a document in the Project Files folder, which is a simpler workflow than adding pushpins to documents in the Plans folder.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with viewables:read data:create data:read and data:write scopes.
Upload the file to BIM 360 Document Management.
Verify the name of the document you want to add the issue pushpins to. If you want to upload a new document, see the Upload a Document to BIM 360 Docs tutorial.
Find the project ID of the document that the issues or RFIs were added to. See the initial steps of the Attachments tutorial for more details.
Verify the ID of the project’s container. For more details see the Retrieve a Container ID tutorial.
Verify that you have access to the relevant BIM 360 account and BIM 360 project.
We recommend reading the Basic Application tutorial, if you are not familiar with the Viewer SDK.
This tutorial applies to both issue pushpins and RFI pushpins. The Viewer extension uses quality-issue for issue pushpins, rfi for RFI pushpins. This tutorial describes an example of creating issue pushpins.

Note that the Viewer demo code (initialization, pushpin workflow) in this tutorial is not relevant for versions 7.0 and above. If you are using Viewer 7.0 or above, check the source demo project (Demo project) which has been migrated with latest version of Viewer.

Step 1: Find the Item ID and Version ID
Use the project ID (b.cGVyc29uYWw6d2l) and the folder ID of the folder that contains the document that the issues were added to (urn:adsk.wipprod:fs.folder:co.O7Zwai) to call GET projects/:project_id/folders/:folder_id/contents with a 3-legged token. This provides the following:

The item ID that is used when creating the pushpin in the document (step 5).
The version ID that is used to render the document in the Viewer (step 3).
Request
curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT"
    "https://developer.api.autodesk.com/project/v1/projects/b.cGVyc29uYWw6d2l/folders/urn:adsk.wipprod:fs.folder:co.BJU3PTc4Sd2CmXM492XUiA/contents"
Response
{
  "jsonapi": {
      "version": "1.0"
   },
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
                  }
             },
       {
          "type": "items",
          "id": "urn:adsk.wip:dm.lineage:7_5NcbL1Q1GSjRLJe9ffvw",
          "attributes": {
              "displayName": "My First Document",
              "createTime": "2017-10-02T11:25:57.0000000Z",
              "createUserId": "X9WYLGPNCHVK",
              "createUserName": "John Smith",
              "lastModifiedTime": "2017-10-02T11:27:22.0000000Z",
              "lastModifiedUserId": "X9WYLGPNCHVK",
              "lastModifiedUserName": "John Smith",
              "hidden": false,
              "extension": {
                  "type": "items:autodesk.bim360:File",
                  "version": "1.0",
                  "schema": {
                      "href": "https://developer.api.autodesk.com/schema/v1/versions/items:autodesk.bim360:File-1.0"
                  },
                  "data": {}
              }
            ]
         }
 "included": [
      {
          "type": "versions",
          "id": "urn:adsk.wipprod:fs.file:vf.7_5NcbL1Q1GSjRLJe9ffvw?version=1",
          "attributes": {
              "name": "My First Document",
              "displayName": "My First Document",
             "createTime": "2017-10-02T11:25:57.0000000Z",
             "createUserId": "X9WYLGPNCHVK",
             "createUserName": "John Smith",
             "lastModifiedTime": "2017-10-02T11:27:22.0000000Z",
             "lastModifiedUserId": "X9WYLGPNCHVK",
             "lastModifiedUserName": "John Smith",
             "hidden": false,
             "versionNumber": 1,
             "fileType": "ifc",
             "extension": {
                  "type": "versions:autodesk.bim360:File",
                  "version": "1.0",
                  "schema": {
                      "href": "https://developer.api.autodesk.com/schema/v1/versions/versions:autodesk.bim360:File-1.0"
                  },
                  "data": {
                      "processState": "PROCESSING_COMPLETE",
                      "extractionState": "SUCCESS",
                      "splittingState": "NOT_SPLIT",
                      "reviewState": "NOT_IN_REVIEW",
                      "revisionDisplayLabel": "1",
                  }
              }
Show Less
Assume that the document is called My First Document, and note the following:

The item ID (data.id) - urn:adsk.wipprod:dm.lineage:7_5NcbL1Q1GSjRLJe9ffvw, which is used when creating the pusphin. (step 5).
The version ID (included[i].id) - urn:adsk.wipprod:fs.file:7_5NcbL1Q1GSjRLJe9ffvw?version=1, which is used to render the document in the Viewer. Note that you do not need to encode the version ID to Base64 format, since it is already encoded when the document was uploaded to BIM 360 Document Management.
Step 2: Initialize the Viewer
Initialize the Viewer and load the document and the Pushpin extension using the Viewer SDK (for versions of the Viewer lower than 7.0). If you want to migrate the initialization process to Viewer 7.0, see the Migration Guide.

// Set up the following handles:
var viewerApp;
var PushPinExtensionHandle;

// Initialize the Viewer and load the document (model)
function launchViewer(urn) {
  var options = {
    env: 'AutodeskProduction',
    // Replace <YOUR_ACCESS_TOKEN> with a 3-legged access token.
    getAccessToken: <YOUR_ACCESS_TOKEN>
  };
  // Replace <YOUR_VERSION_ID> with a the version ID of the document.
  var documentId = 'urn:' + <YOUR_VERSION_ID>;

  var config3d = {
    extensions: []
  };
  Autodesk.Viewing.Initializer(options, function onInitialized() {
    viewerApp = new Autodesk.Viewing.ViewingApplication('forgeViewer'); // setting viewerApp handle
    viewerApp.registerViewer(viewerApp.k3D, Autodesk.Viewing.Private.GuiViewer3D, config3d);
    viewerApp.loadDocument(documentId, onDocumentLoadSuccess, onDocumentLoadFailure); // loading document
  });
}

// Select a sheet of the model to display in the Viewer.
function onDocumentLoadSuccess(doc) {

  // The `bubble` object contains metadata about the viewer and its displayed content.
  // Use `bubble.search` to filter for data within the object.
  // The "geometry" type retrieves all of the document's 2D and 3D sheets.
  var viewables = viewerApp.bubble.search({ 'type': 'geometry' });
  if (!viewables.length) {
    return console.error('Document contains no viewables.');
  }

  // In this example, we are using the `viewerApp` handle to select and load the first sheet (view).
  // Alternatively load a different sheet.
  viewerApp.selectItem(viewables[0], onItemLoadSuccess, onItemLoadFail);
}

// Load the Pushpin extension
function onItemLoadSuccess(viewer, item) {
  ...

  // Select pushpin buttons for the Viewer toolbar.
  // By default, the buttons will not appear in the toolbar.
  var extensionOptions = {
     hideIssuesButton: false,
     hideFieldIssuesButton: true,
   };

   // Use the `viewer` reference to call `loadExtension` with the extension name and the extension options:

   viewer.loadExtension('Autodesk.BIM360.Extension.PushPin', extensionOptions)
     .then(function (extension) {
       PushPinExtensionHandle = extension;
     });
 }
Show Less
Step 3: Create the Pushpin
We recommend adding a Create Pushpin button to start the pushpin creation process. Use the button to invoke the following function:

// Define the following properties:
// `label` - An initial dummy identifier until it is saved; `status` - The color of the pushpin; `type` - the shape of the pushpin
PushPinExtensionHandle.startCreateItem({label: 'New', status: 'open', type: 'issues'});
We recommend creating a form for displaying the pushpin data. Note that it is obligatory to include a title field. This is used when creating the pushpin in step 5. We will store the data in an object called userForm.

After calling the startCreateItem function, you need to set up an event listener for the pushpin.created event. This completes the pinning process.

You could decide to set the event listener before calling startCreateItem, however, you will need to make sure nothing else triggers the pushpin.created event before completing the pinning process.

PushPinExtensionHandle.pushPinManager.addEventListener('pushpin.created', function (e) {
  PushPinExtensionHandle.endCreateItem();
  ...
});
To sum things up - startCreateItem allows us to place the pushpin in the document. Pinning the pushpin fires the pushpin.created event. To complete the pinning process, you need to call endCreateItem.

This tutorial will create a pushpin issue.

Step 4: Adjusting the Pushpin (optional)
The user can optionally adjust the coordinates and edit the form data before creating the actual pushpin issue. The following code should follow after the endCreateItem function:

PushPinExtensionHandle.setDraggableById('0', true);
Our newly created Pushpin will have a default id of 0, which is how we grab hold of it. Setting setDraggableById to true allows us to move it around.

Note that you can listen to “dropping” events (after adjusting the pushpin) using the pushpin.modified event.

Step 5: Prepare the Payload for Creating Issue and RFI Pushpins
Before creating the issue or RFI pushpins, you need to prepare the data. This tutorial demonstrates how to prepare the payload for creating issue pushpins. For information about preparing the payload for RFI pushpins, see POST rfis.

// Once the user clicks the ``Create Pushpin`` button (see step 3), you need to grab the current position of the newly created pushpin and the pushpin data using its ID, which is automatically set to ``0``.
var issue = PushPinExtensionHandle.getItemById('0');
// This is how the API expects to receive the data:
var data = {
  type: issue.type,
  attributes: {
    title: userForm.title, // In our example, this is the ``title`` the user sets in the form data (see step 3).
    // The extension retrieved the ``type`` and ``status`` properties in step 3, concatenated them, added a dash, and
    // assigned the new string to the ``status`` property of the newly created pushpin object. For example, ``issues-
    // open``.
    // You now need to extract the ``status`` (``open``) from the pushpin object.
    status: issue.status.split('-')[1] || issue.status,
    // The ``target_urn`` is the ID of the document (``item``) associated with an issue; see step 1.
    target_urn: <YOUR_ITEM_ID>,
    starting_version: <YOUR_VERSION_ID>, // See step 1 for the version ID.
    // The issue type ID and issue subtype ID. See GET ng-issue-types for more details.
    ng_issue_type_id: <ISSUE_TYPE_ID>
    ng_issue_subtype_id: <ISSUE_SUBTYPE_ID>
    // ``sheet_metadata`` is the sheet in the document associated with the pushpin.
    sheet_metadata: { // `viewerApp.selectedItem` references the current sheet
      is3D: viewerApp.selectedItem.is3D(),
      sheetGuid: viewerApp.selectedItem.guid(),
      sheetName: viewerApp.selectedItem.name()
    },
    pushpin_attributes: { // Data about the pushpin
      type: 'TwoDVectorPushpin', // This is the only type currently available
      object_id: issue.objectId, // (Only for 3D models) The object the pushpin is situated on.
      location: issue.position, // The x, y, z coordinates of the pushpin.
      viewer_state: issue.viewerState // The current viewer state. For example, angle, camera, zoom.
    },
  }
};
// See step 6 for details about how to implement the call in your server
createIssue(data);
Show Less
Step 6: Create the Issue or RFI Pushpins
Within our server we will implement the POST issues call. If you are creating RFI pushpins, you need to implement POST rfis.

Note that if a document has multiple pages and is a Project Files folder file, you need to specify the page number in the sheet_metadata.sheetName parameter.

Step 7: Final Formatting
After calling POST issues, you can follow the Render Pushpin Issues and RFIs in Your App tutorial to rerender all the pushpins in the document. This will format the newly created pushpin in the following ways:

Permanently pin the pushpin in the document (this is only necessary if you invoked the setDraggableById function in step 4)
Unselect the selected pushpin.
Update the pushpin data with the data generated in the server.

Documentation /BIM 360 API /How-to Guide
Create Document-related (Pushpin) Issues and RFIs in Your App
This tutorial demonstrates how to use the Viewer SDK to create pushpin issues and RFIs in your app. Pushpins are visual markers that denote the location of a BIM 360 issue or RFI in a document. The Viewer SDK includes an extension that renders pushpin issues and RFIs, or collects payload data for creating issues or RFIs. This tutorial demonstrates how to use the Viewer SDK to load BIM 360 documents and create issue or RFI pushpins from data specified by the end user. The steps include finding the ID of the document you want to add the pushpins to, initializing the Viewer, loading the document, enabling the end user to select a postion and object and creating the pushpin issues and RFIs (on the server side).

Note that you can add pushpins to documents in any BIM 360 Document Management folder. This tutorial demonstrates how to add a pusphin to a document in the Project Files folder, which is a simpler workflow than adding pushpins to documents in the Plans folder.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with viewables:read data:create data:read and data:write scopes.
Upload the file to BIM 360 Document Management.
Verify the name of the document you want to add the issue pushpins to. If you want to upload a new document, see the Upload a Document to BIM 360 Docs tutorial.
Find the project ID of the document that the issues or RFIs were added to. See the initial steps of the Attachments tutorial for more details.
Verify the ID of the project’s container. For more details see the Retrieve a Container ID tutorial.
Verify that you have access to the relevant BIM 360 account and BIM 360 project.
We recommend reading the Basic Application tutorial, if you are not familiar with the Viewer SDK.
This tutorial applies to both issue pushpins and RFI pushpins. The Viewer extension uses issue for issue pushpins, rfi for RFI pushpins. This tutorial describes an example of creating issue pushpins.

To see a working sample, see this viewer demo project (Demo project).

Step 1: Find the Item ID and Version ID
Use the project ID (b.cGVyc29uYWw6d2l) and the folder ID of the folder that contains the document that the issues were added to (urn:adsk.wipprod:fs.folder:co.O7Zwai) to call GET projects/:project_id/folders/:folder_id/contents with a 3-legged token. This provides the following:

The item ID that is used when creating the pushpin in the document (step 5).
The version ID that is used to render the document in the Viewer (step 3).
Request
curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT"
    "https://developer.api.autodesk.com/project/v1/projects/b.cGVyc29uYWw6d2l/folders/urn:adsk.wipprod:fs.folder:co.BJU3PTc4Sd2CmXM492XUiA/contents"
Response
{
  "jsonapi": {
      "version": "1.0"
   },
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
                  }
             },
       {
          "type": "items",
          "id": "urn:adsk.wip:dm.lineage:7_5NcbL1Q1GSjRLJe9ffvw",
          "attributes": {
              "displayName": "My First Document",
              "createTime": "2017-10-02T11:25:57.0000000Z",
              "createUserId": "X9WYLGPNCHVK",
              "createUserName": "John Smith",
              "lastModifiedTime": "2017-10-02T11:27:22.0000000Z",
              "lastModifiedUserId": "X9WYLGPNCHVK",
              "lastModifiedUserName": "John Smith",
              "hidden": false,
              "extension": {
                  "type": "items:autodesk.bim360:File",
                  "version": "1.0",
                  "schema": {
                      "href": "https://developer.api.autodesk.com/schema/v1/versions/items:autodesk.bim360:File-1.0"
                  },
                  "data": {}
              }
            ]
         }
 "included": [
      {
          "type": "versions",
          "id": "urn:adsk.wipprod:fs.file:vf.7_5NcbL1Q1GSjRLJe9ffvw?version=1",
          "attributes": {
              "name": "My First Document",
              "displayName": "My First Document",
             "createTime": "2017-10-02T11:25:57.0000000Z",
             "createUserId": "X9WYLGPNCHVK",
             "createUserName": "John Smith",
             "lastModifiedTime": "2017-10-02T11:27:22.0000000Z",
             "lastModifiedUserId": "X9WYLGPNCHVK",
             "lastModifiedUserName": "John Smith",
             "hidden": false,
             "versionNumber": 1,
             "fileType": "ifc",
             "extension": {
                  "type": "versions:autodesk.bim360:File",
                  "version": "1.0",
                  "schema": {
                      "href": "https://developer.api.autodesk.com/schema/v1/versions/versions:autodesk.bim360:File-1.0"
                  },
                  "data": {
                      "processState": "PROCESSING_COMPLETE",
                      "extractionState": "SUCCESS",
                      "splittingState": "NOT_SPLIT",
                      "reviewState": "NOT_IN_REVIEW",
                      "revisionDisplayLabel": "1",
                  }
              }
Show Less
Assume that the document is called My First Document, and note the following:

The item ID (data.id) - urn:adsk.wipprod:dm.lineage:7_5NcbL1Q1GSjRLJe9ffvw, which is used when creating the pusphin. (step 5).
The version ID (included[i].id) - urn:adsk.wipprod:fs.file:7_5NcbL1Q1GSjRLJe9ffvw?version=1, which is used to render the document in the Viewer. Note that you do not need to encode the version ID to Base64 format, since it is already encoded when the document was uploaded to BIM 360 Document Management.
Step 2: Initialize the Viewer
Initialize the Viewer and load the document and the Pushpin extension using the Viewer SDK.

// Set up the following handles:
var viewer;
var PushPinExtensionHandle;
// Initialize the Viewer and load the document (model)
function launchViewer(urn) {
  var options = {
    env: 'AutodeskProduction',
    // Replace <YOUR_ACCESS_TOKEN> with a 3-legged access token.
    getAccessToken: <YOUR_ACCESS_TOKEN>
  };
  // Replace <YOUR_VERSION_ID> with a the version ID of the document.
  var documentId = 'urn:' + <YOUR_VERSION_ID>;
  Autodesk.Viewing.Initializer(options, function onInitialized() {
    viewer = new Autodesk.Viewing.GuiViewer3D(document.getElementById('forgeViewer')); // setting viewer handle
    viewer.start();
    Autodesk.Viewing.Document.load(documentId, onDocumentLoadSuccess, onDocumentLoadFailure); // loading document
  });
}
// Select a sheet of the model to display in the Viewer.
function onDocumentLoadSuccess(viewerDocument) {
  // viewerDocument is an instance of Autodesk.Viewing.Document
  // The "geometry" type retrieves all of the document's 2D and 3D sheets.
  var viewables = viewerDocument.getRoot().search({'type':'geometry'});
  if (!viewables.length) {
    return console.error('Document contains no viewables.');
  }
  // In this example, we are using the `viewer` handle to select and load the first sheet (view).
  // Alternatively load a different sheet.
  viewer.loadDocumentNode(viewerDocument, viewables[0]);
  // Load the Pushpin extension
  // Select pushpin buttons for the Viewer toolbar.
  // By default, the buttons will not appear in the toolbar.
  var extensionOptions = {
     hideIssuesButton: false,
     hideRfisButton: true,
     hideFieldIssuesButton: true,
   };
  // Use the `viewer` reference to call `loadExtension` with the extension name and the extension options:
  viewer.loadExtension('Autodesk.BIM360.Extension.PushPin', extensionOptions)
    .then(function (extension) {
      PushPinExtensionHandle = extension;
    });
}
Show Less
Step 3: Create the Pushpin
We recommend adding a Create Pushpin button to start the pushpin creation process. Use the button to invoke the following function:

// Define the following properties:
// `label` - An initial dummy identifier until it is saved; `status` - The color of the pushpin; `type` - the shape of the pushpin
PushPinExtensionHandle.startCreateItem({label: 'New', status: 'open', type: 'issues'});
We recommend creating a form for displaying the pushpin data. Note that it is obligatory to include a title field. This is used when creating the pushpin in step 5. We will store the data in an object called userForm.

After calling the startCreateItem function, you need to set up an event listener for the pushpin.created event. This completes the pinning process.

You could decide to set the event listener before calling startCreateItem, however, you will need to make sure nothing else triggers the pushpin.created event before completing the pinning process.

PushPinExtensionHandle.pushPinManager.addEventListener('pushpin.created', function (e) {
  PushPinExtensionHandle.endCreateItem();
  ...
});
To sum things up - startCreateItem allows us to place the pushpin in the document. Pinning the pushpin fires the pushpin.created event. To complete the pinning process, you need to call endCreateItem.

This tutorial will create a pushpin issue.

Step 4: Adjusting the Pushpin (optional)
The user can optionally adjust the coordinates and edit the form data before creating the actual pushpin issue. The following code should follow after the endCreateItem function:

PushPinExtensionHandle.setDraggableById('0', true);
Our newly created Pushpin will have a default id of 0, which is how we grab hold of it. Setting setDraggableById to true allows us to move it around.

Note that you can listen to “dropping” events (after adjusting the pushpin) using the pushpin.modified event.

Step 5: Prepare the Payload for Creating Issue and RFI Pushpins
Before creating the issue or RFI pushpins, you need to prepare the data. This tutorial demonstrates how to prepare the payload for creating issue pushpins. For information about preparing the payload for RFI pushpins, see POST rfis.

// Once the user clicks the ``Create Pushpin`` button (see step 3), you need to grab the current position of the newly created pushpin and the pushpin data using its ID, which is automatically set to ``0``.
var issue = PushPinExtensionHandle.getItemById('0');
// This is how the API expects to receive the data:
var payload = {
    title: userForm.title, // In our example, this is the ``title`` the user sets in the form data (see step 3).
    // The extension retrieved the ``type`` and ``status`` properties in step 3, concatenated them, added a dash, and
    // assigned the new string to the ``status`` property of the newly created pushpin object. For example, ``issues-
    // open``.
    // You now need to extract the ``status`` (``open``) from the pushpin object.
    status: issue.status.split('-')[1] || issue.status,
    createdAtVersion: <YOUR_VERSION_ID>, // See step 1 for the version ID.
    // The issue subtype ID. See GET issue-types for more details.
    issueSubtypeId: <ISSUE_SUBTYPE_ID>
   "linkedDocuments": [
        {
          type: "TwoDVectorPushpin",
          // The ``urn`` is the ID of the document (``item``) associated with an issue; see step 1.
          urn: <YOUR_ITEM_ID>,
          createdAtVersion: <YOUR_VERSION_ID>, // See step 1 for the version ID.
          details: {
            viewable: {
              id: viewer.model.getDocumentNode().data.guid,
              name: viewer.model.getDocumentNode().data.name,
              is3D: viewer.model.is3D
            },
            position: issue.position,// The x, y, z coordinates of the pushpin.
            objectId: issue.objectId, // (Only for 3D models) The object the pushpin is situated on.
            viewerState: issue.viewerState // The current viewer state. For example, angle, camera, zoom.
          }
        }
    ],
  };
// See step 6 for details about how to implement the call in your server
createIssue(data);
Show Less
Step 6: Create the Issue or RFI Pushpins
Within our server we will implement the POST issues call. If you are creating RFI pushpins, you need to implement POST rfis.

Step 7: Final Formatting
After calling POST issues, you can follow the Render Pushpin Issues and RFIs in Your App tutorial to rerender all the pushpins in the document. This will format the newly created pushpin in the following ways:

Permanently pin the pushpin in the document (this is only necessary if you invoked the setDraggableById function in step 4)
Unselect the selected pushpin.
Update the pushpin data with the data generated in the server.

Documentation /BIM 360 API /How-to Guide
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

Documentation /BIM 360 API /How-to Guide
Retrieve an RFIs Container ID
This tutorial demonstrates how to retrieve a container ID for a BIM 360 project. Each BIM 360 project is assigned an RFIs container (rfisContainerId) that stores all the RFIs data for the project. The RFIs container ID is used to call the BIM 360 RFIs endpoints. To retrieve the ID, you need to call several Data Management endpoints.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with the data:read scope.
Verify that you have access to the relevant BIM 360 account and BIM 360 project. (To create a new BIM 360 project, see POST projects)
Step 1: Find the Hub ID
You first need to call GET hubs to find the hub ID for your BIM 360 account.

Note that the BIM 360 account ID corresponds to a Data Management hub ID. To convert an account ID into a hub ID you need to add a “b." prefix. For example, an account ID of c8b0c73d-3ae9 translates to a hub ID of b.c8b0c73d-3ae9.

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
In this example, assume that the project you want the container for is in My First Account hub.

Step 2: Find the Container ID for the Project
Use the BIM 360 hub ID that you retrieved in the previous step (b.cGVyc29uYWw6cGUyOWNjZjMy) to call GET hubs/:hub_id/projects, and retrieve a list of all the projects in the hub the user has access to. In this example, we have added a filter to only return details of a specific project (Demo Project).

The response payload includes the RFIs container ID (data.relationships.rfis.data.id).

Request
curl -X GET -H "Authorization: Bearer nFRJxzCD8OOUr7hzBwbr06D76zAT" "https://developer.api.autodesk.com/project/v1/hubs/b.cGVyc29uYWw6cGUyOWNjZjMy/projects?filter%5Battributes.name%5D=Demo%20Project"
Response
{
  "jsonapi": {
    "version": "1.0"
  },
  "links": {
    "self": {
      "href": "https://developer.api.autodesk.com/project/v1/hubs/b.7fcde01c-738a-4f5e-8a1c-7a8da2381693/projects"
    }
  },
  "data": [
    {
      "type": "projects",
      "id": "b.1f50f9e7-df95-43f9-9366-2fd44cafa768",
      "attributes": {
        "name": "Demo Project",
        "extension": {
          "type": "projects:autodesk.bim360:Project",
          "version": "1.0",
          "schema": {
            "href": "https://developer.api.autodesk.com/schema/v1/versions/projects:autodesk.bim360:Project-1.0"
          },
          "data": {}
        }
      },
      "links": {
        "self": {
          "href": "https://developer.api.autodesk.com/project/v1/hubs/b.7fcde01c-738a-4f5e-8a1c-7a8da2381693/projects/b.1f50f9e7-df95-43f9-9366-2fd44cafa768"
        }
      },
      "relationships": {
        "hub": {
          "data": {
            "type": "hubs",
            "id": "b.7fcde01c-738a-4f5e-8a1c-7a8da2381693"
          },
          "links": {
            "related": {
              "href": "https://developer.api.autodesk.com/project/v1/hubs/b.7fcde01c-738a-4f5e-8a1c-7a8da2381693"
            }
          }
        },
        "rootFolder": {
          "data": {
            "type": "folders",
            "id": "urn:adsk.wipprod:fs.folder:co.xOuT2J3zSdqR4eD_pkd3WQ"
          },
          "meta": {
            "link": {
              "href": "https://developer.api.autodesk.com/data/v1/projects/b.1f50f9e7-df95-43f9-9366-2fd44cafa768/folders/urn:adsk.wipprod:fs.folder:co.xOuT2J3zSdqR4eD_pkd3WQ"
            }
          }
        },
        "topFolders": {
          "links": {
            "related": {
              "href": "https://developer.api.autodesk.com/project/v1/hubs/b.7fcde01c-738a-4f5e-8a1c-7a8da2381693/projects/b.1f50f9e7-df95-43f9-9366-2fd44cafa768/topFolders"
            }
          }
        },
        "rfis": {
          "data": {
            "type": "rfisContainerId",
            "id": "e59adc9d-2677-4afc-a800-4bc42101f7d8"
          },
          "meta": {
            "link": {
              "href": "https://developer.api.autodesk.com/bim360/rfis/v1/containers/e59adc9d-2677-4afc-a800-4bc42101f7d8/rfis"
            }
          }
        }
      }
    }
  ]
}

Documentation /BIM 360 API /How-to Guide
RFI Transitions
This tutorial demonstrates a typical RFI workflow. The steps include:

Verifying whether a user has permissions to create an RFI (creator or manager workflow role).
Creating an RFI with draft status.
Verifying whether a user has permissions to transition an RFI from draft status to submitted status (creator workflow role), and verifying which users can be assigned to the RFI when it is transitioned to submitted status (manager workflow role).
Transitioning the RFI to submitted status and assigning the RFI to a user.
Verifying whether a user has permissions to transition an RFI from submitted status to open status (manager workflow role), and verifying which users can be assigned to the RFI when it is transitioned to open status (reviewer workflow role).
Transitioning the RFI to open status and assigning the RFI to a user.
Repeating the process for transitioning from open status to answered status and for transitioning from answered status to closed status.
Note that the RFIs API does not use the same names for workflow roles as the Project Admin module. The following table describes the Project Admin module names and the corresponding RFIs API names:

Project Admin Module Workflow Role Name	RFIs API Workflow Role Name
Creator	Subcontractor (projectSC)
Manager	General Contractor (projectGC)
Reviewer 1 (EMEA workflow)	Construction Manager (projectCM)
Reviewer (US workflow) / Reviewer 2 (EMEA workflow)	Architect (projectArch)
To assign users to workflow roles, open the BIM 360 Project Admin module, select the Services tab, and select the Project Management section.

At each stage in the workflow you can assign an RFI to a user. In order to assign an RFI to a user at specific stages in the workflow, the user needs to have been assigned specific workflow roles. For more details, see the RFIs help documentation.

There are two RFI workflow options you can assign to a project:

The default RFI workflow which has a single reviewer. The RFIs API uses the term US for this workflow.
A workflow with an additional reviewer. The RFIs API uses the term - EMEA for this workflow.
This tutorial is using the default RFI workflow with a single reviewer. For information about selecting an RFI workflow for a project, see the RFIs help documentation. Note that currently you cannot use the RFIs API to select an RFI workflow.

Before You Begin
Register an app
Acquire a 3-legged OAuth token with data:create data:read and data:write scopes.
Verify the container ID for the RFI. In this example, assume the container ID is e59adc9d-2677-4afc-a800-4bc42101f7d8.
Step 1: Verify the User’s Permissions
Before the user creates an RFI you need to verify that the user has permissions to create it. Users who have been assigned either creator (projectSC) or manager (projectGC) workflow roles can create RFIs. All users in the project are automatically assigned the creator workflow role. To assign creator or manager workflow roles to project members, open the BIM 360 Project Admin module, select the Services tab, and select the Project Management section.

Use the container ID (e59adc9d-2677-4afc-a800-4bc42101f7d8) to call GET users/me to verify the user’s permissions for creating RFIs.

Note that only users who are members of a project can potentially create and edit RFIs for the project. To check which users are members of a project, call GET projects/users.

Note that if a user is not a project member, the endpoint will return an error.

Request
curl -X GET \
  https://developer.api.autodesk.com/bim360/rfis/v2/containers/e59adc9d-2677-4afc-a800-4bc42101f7d8/users/me \
  -H 'Authorization: Bearer XZvCJNhdxESsBRIH28MfLf2hKL5O' \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json'
Response
{
  "user": {
    "id": "PER8KQPK2JRT",
    "name": "John Smith",
    "role": "project_user"
  },
  "permittedActions": {
    "createRfi": {
      "permittedStatuses": [
        {
          "status": "draft",
          "requiredAttributes": [
            {
              "name": "title"
            }
          ]
        },
        {
          "status": "submitted",
          "requiredAttributes": [
            {
              "name": "title"
            },
            {
              "name": "assignedTo",
              "values": [
                {
                  "value": "SN8TPJUCUASA",
                  "type": "user"
                },
                {
                  "value": "BXQXL7646C2R",
                  "type": "user"
                }
              ]
            }
          ]
        },
        {
          "status": "open",
          "requiredAttributes": [
            {
              "name": "title"
            },
            {
              "name": "assignedTo",
              "values": [
                {
                  "value": "8QVAQV5PW36V",
                  "type": "user"
                },
                {
                  "value": "LXD6JZWKDFKA",
                  "type": "user"
                },
                {
                  "value": "R7ZNPU3EZRMM",
                  "type": "user"
                },
                {
                  "value": "53SAKU73TL5R",
                  "type": "user"
                }
              ]
            }
          ]
        }
      ]
    }
  },
  "workflow": {
    "roles": [
      "projectSC",
      "projectGC"
    ],
    "type": "US"
  }
}
Show Less
Find the workflow.roles list. If it includes either projectSC, or projectGC it indicates that the user can create RFIs.

The permittedActions.createRfi.permittedStatuses section informs you which types of statuses the user can create the RFI with; in this example draft, submitted, and open. It also lists the attributes that are required for each status.

In our example, the user will create the RFI in draft status, and will include the title attribute in the request body.

Step 2: Create the RFI
Use the container ID (e59adc9d-2677-4afc-a800-4bc42101f7d8) to call POST rfis.

Request
curl "https://developer.api.autodesk.com/bim360/rfis/v1/containers/e59adc9d-2677-4afc-a800-4bc42101f7d8/rfis" -d '{
    "title": "Pipe Size",
    "status": "draft",
    "question": "Is the pipe in room 3 the correct size?",
    "suggestedAnswer": "No",
    "location": {
        "description": "Room 3"
    },
    "dueDate": "2020-07-31T09:35:54.000Z"
  }' -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer XZvCJNhdxESsBRIH28MfLf2hKL5O"
Show Less
Response
{
  "createdAt": "2020-05-10T09:35:57.871Z",
  "updatedAt": "2020-05-10T09:35:57.871Z",
  "id": "5a8e2519-7e91-4c4c-ba5c-685fdbbf021e",
  "assignedToType": "user",
  "coReviewers": [

  ],
  "distributionList": [

  ],
  "mentionees": [

  ],
  "discipline": [

  ],
  "category": [

  ],
  "containerId": "e59adc9d-2677-4afc-a800-4bc42101f7d8",
  "title": "Pipe Size",
  "status": "draft",
  "question": "",
  "dueDate": "2020-05-11T09:35:54.000Z",
  "workflowType": "US",
  "createdBy": "PER8KQPK2JRT",
  "assignedTo": "PER8KQPK2JRT",
  "workflowStateId": "57780388-37f8-4505-9758-808adcb9b124",
  "pushpinAttributes": null,
  "permittedActions": {
    "updateRfi": {
      "permittedAttributes": [
        {
          "name": "category"
        },
        {
          "name": "costImpact"
        },
        {
          "name": "discipline"
        },
        {
          "name": "distributionList"
        },
        {
          "name": "dueDate"
        },
        {
          "name": "linkedDocument"
        },
        {
          "name": "linkedDocumentVersion"
        },
        {
          "name": "location"
        },
        {
          "name": "priority"
        },
        {
          "name": "question"
        },
        {
          "name": "reference"
        },
        {
          "name": "scheduleImpact"
        },
        {
          "name": "suggestedAnswer"
        },
        {
          "name": "title"
        },
        {
          "name": "status",
          "values": [
            {
              "value": "submitted"
            },
            {
              "value": "open"
            },
            {
              "value": "void"
            }
          ]
        }
      ],
      "permittedStatuses": [
        {
          "status": "submitted",
          "requiredAttributes": [
            {
              "name": "assignedTo",
              "values": [
                {
                  "value": "8QVAQV5PW36V",
                  "type": "user"
                },
                {
                  "value": "BXQXL7646C2R",
                  "type": "user"
                }
              ]
            }
          ]
        },
        {
          "status": "open",
          "requiredAttributes": [
            {
              "name": "assignedTo",
              "values": [
                {
                  "value": "8QVAQV5PW36V",
                  "type": "user"
                },
                {
                  "value": "LXD6JZWKDFKA",
                  "type": "user"
                },
                {
                  "value": "R7ZNPU3EZRMM",
                  "type": "user"
                },
                {
                  "value": "53SAKU73TL5R",
                  "type": "user"
                }
              ]
            }
          ]
        },
        {
          "status": "void",
          "requiredAttributes": [

          ]
        }
      ]
    },
    "createComment": true,
    "createAttachment": true,
    "togglePushpinVisibility": false
  }
}
Show More
Find the RFI ID (id) and note the ID (5a8e2519-7e91-4c4c-ba5c-685fdbbf021e).

The permittedActions.updateRfi.permittedStatuses section informs you which types of statuses the user can transition the RFI into; in this example submitted, open, or void. It also lists which users you can assign to the RFI when you transition to the new status.

In this example, we will transition the RFI to submitted status. When you transition the RFI to submitted status, you need to assign the RFI to a user. Locate the list of users that can potentially be assigned to the RFI when you transition it to submitted status by finding the submitted status in permittedActions.updateRfi.permittedStatuses, and checking the list of users (requiredAttributes.values).

Note that only assignees with a manager (projectGC) workflow role will be listed as potential assignees. See the help documentation for more details.

Note the user’s BIM 360 ID. In this example 8QVAQV5PW36V.

To verify the actual name of the user, call GET projects/:projectId/users/:userId.

Step 3: Transition the RFI to Submitted Status
Use the container ID (e59adc9d-2677-4afc-a800-4bc42101f7d8), the RFI ID (5a8e2519-7e91-4c4c-ba5c-685fdbbf021e) and the BIM 360 ID of the assignee (8QVAQV5PW36V) to call PATCH rfis/:id to transition the RFI from draft status to submitted status.

In this example, the user who created the RFI will also transition the RFI to submitted status.

Request
curl "https://developer.api.autodesk.com/bim360/rfis/v2/containers/e59adc9d-2677-4afc-a800-4bc42101f7d8/rfis/5a8e2519-7e91-4c4c-ba5c-685fdbbf021e" -d '{
      "status": "submitted",
      "assignedTo": "8QVAQV5PW36V"
  }' -X PATCH \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer XZvCJNhdxESsBRIH28MfLf2hKL5O"
Response
200 Success
Content-Type: application/json; charset=utf-8

{
  "id": "5a8e2519-7e91-4c4c-ba5c-685fdbbf021e",
  "title": "Pipe Size",
  "question": "Is the pipe in room 3 the correct size?",
  "status": "submitted",
  "assignedTo": "8QVAQV5PW36V",
  "assignedToType": "user",
  "dueDate": "2020-05-11T09:35:54.000Z",
  "createdBy": "PER8KQPK2JRT",
  "containerId": "e59adc9d-2677-4afc-a800-4bc42101f7d8",
  "workflowStateId": "57780388-37f8-4505-9758-808adcb9b124",
  "workflowType": "US",
  "coReviewers": [

  ],
  "distributionList": [

  ],
  "mentionees": [

  ],
  "discipline": [

  ],
  "category": [

  ],
  "createdAt": "2020-05-10T09:35:57.871Z",
  "updatedAt": "2020-05-10T09:35:57.872Z",
  "comments": [

  ],
  "attachments": [

  ],
  "managerId": "8QVAQV5PW36V",
  "updatedBy": "PER8KQPK2JRT",
  "permittedActions": {
    "updateRfi": {
      "permittedAttributes": [
        {
          "name": "assignedTo",
          "values": [
            {
              "value": "SN8TPJUCUASA",
              "type": "user"
            },
            {
              "value": "BXQXL7646C2R",
              "type": "user"
            }
          ]
        },
        {
          "name": "category"
        },
        {
          "name": "coReviewers"
        },
        {
          "name": "costImpact"
        },
        {
          "name": "discipline"
        },
        {
          "name": "distributionList"
        },
        {
          "name": "dueDate"
        },
        {
          "name": "linkedDocument"
        },
        {
          "name": "linkedDocumentVersion"
        },
        {
          "name": "location"
        },
        {
          "name": "priority"
        },
        {
          "name": "question"
        },
        {
          "name": "reference"
        },
        {
          "name": "scheduleImpact"
        },
        {
          "name": "suggestedAnswer"
        },
        {
          "name": "title"
        },
        {
          "name": "status",
          "values": [
            {
              "value": "open"
            },
            {
              "value": "closed"
            },
            {
              "value": "void"
            }
          ]
        }
      ],
      "permittedStatuses": [
        {
          "status": "open",
          "requiredAttributes": [
            {
              "name": "assignedTo",
              "values": [
                {
                  "value": "JZ7WLLQUKRAD",
                  "type": "user"
                },
                {
                  "value": "LXD6JZWKDFKA",
                  "type": "user"
                },
                {
                  "value": "R7ZNPU3EZRMM",
                  "type": "user"
                },
                {
                  "value": "53SAKU73TL5R",
                  "type": "user"
                }
              ]
            }
          ]
        },
        {
          "status": "closed",
          "requiredAttributes": [
            {
              "name": "officialResponse"
            }
          ]
        },
        {
          "status": "void",
          "requiredAttributes": [

          ]
        }
      ]
    },
    "createComment": true,
    "createAttachment": true,
    "togglePushpinVisibility": false
  }
}
Show Less
In this example, the permittedActions.updateRfi.permittedStatuses section informs you that you can potentially transition the RFI into open, closed, or void statuses. We will transition the RFI into open status, and assign it to JZ7WLLQUKRAD.

Step 4: Change the User
The user who was assigned to the RFI (8QVAQV5PW36V) in the previous step when the RFI was transitioned to submitted status needs to transition the RFI to open status. You need to acquire a 3-legged OAuth token for the assignee with data:create data:read and data:write scopes to use in the next few steps.

Step 5: Transition the RFI to Open Status
Use the container ID (e59adc9d-2677-4afc-a800-4bc42101f7d8), the RFI ID (5a8e2519-7e91-4c4c-ba5c-685fdbbf021e), and the BIM 360 ID of the assignee (JZ7WLLQUKRAD) to call PATCH rfis/:id to transition the RFI from submitted status to open status.

Request
curl "https://developer.api.autodesk.com/bim360/rfis/v2/containers/e59adc9d-2677-4afc-a800-4bc42101f7d8/rfis/5a8e2519-7e91-4c4c-ba5c-685fdbbf021e" -d '{
      "status": "open",
      "assignedTo": "JZ7WLLQUKRAD"
  }' -X PATCH \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer l0ZSIsImRhdGE6cmVhZCIsImRhdGE6Y3JlYXRlIiwiZGF0YTpzZWFyY2gi"
Response
200 Success
Content-Type: application/json; charset=utf-8

{
  "id": "5a8e2519-7e91-4c4c-ba5c-685fdbbf021e",
  "title": "Pipe Size",
  "question": "Is the pipe in room 3 the correct size?",
  "status": "open",
  "assignedTo": "JZ7WLLQUKRAD",
  "assignedToType": "user",
  "dueDate": "2020-05-11T09:35:54.000Z",
  "createdBy": "PER8KQPK2JRT",
  "updatedBy": "8QVAQV5PW36V",
  "containerId": "80d025dc-6c45-4178-95a8-d4066a28da09",
  "workflowStateId": "bf6f2833-6ab1-403d-83f6-2c716fbf8e06",
  "workflowType": "US",
  "coReviewers": [

  ],
  "distributionList": [

  ],
  "managerId": "8QVAQV5PW36V",
  "mentionees": [

  ],
  "discipline": [

  ],
  "category": [

  ],
  "createdAt": "2020-05-10T09:35:57.871Z",
  "updatedAt": "2020-05-10T13:13:35.297Z",
  "comments": [

  ],
  "attachments": [

  ],
  "customIdentifier": "1",
  "openedBy": "8QVAQV5PW36V",
  "openedAt": "2020-05-10T14:04:03.328Z",
  "reviewerId": "JZ7WLLQUKRAD",
  "architectId": "JZ7WLLQUKRAD",
  "permittedActions": {
    "updateRfi": {
      "permittedAttributes": [
        {
          "name": "assignedTo",
          "values": [
            {
              "value": "8QVAQV5PW36V",
              "type": "user"
            },
            {
              "value": "LXD6JZWKDFKA",
              "type": "user"
            },
            {
              "value": "R7ZNPU3EZRMM",
              "type": "user"
            },
            {
              "value": "53SAKU73TL5R",
              "type": "user"
            }
          ]
        },
        {
          "name": "category"
        },
        {
          "name": "coReviewers"
        },
        {
          "name": "costImpact"
        },
        {
          "name": "customIdentifier"
        },
        {
          "name": "discipline"
        },
        {
          "name": "distributionList"
        },
        {
          "name": "dueDate"
        },
        {
          "name": "linkedDocument"
        },
        {
          "name": "linkedDocumentVersion"
        },
        {
          "name": "location"
        },
        {
          "name": "officialResponse"
        },
        {
          "name": "priority"
        },
        {
          "name": "question"
        },
        {
          "name": "reference"
        },
        {
          "name": "scheduleImpact"
        },
        {
          "name": "suggestedAnswer"
        },
        {
          "name": "title"
        },
        {
          "name": "status",
          "values": [
            {
              "value": "answered"
            },
            {
              "value": "rejected"
            },
            {
              "value": "void"
            }
          ]
        }
      ],
      "permittedStatuses": [
        {
          "status": "answered",
          "requiredAttributes": [
            {
              "name": "officialResponse"
            }
          ]
        },
        {
          "status": "rejected",
          "requiredAttributes": [
            {
              "name": "officialResponse"
            }
          ]
        },
        {
          "status": "void",
          "requiredAttributes": [

          ]
        }
      ]
    },
    "createComment": true,
    "createAttachment": true,
    "togglePushpinVisibility": false
  }
}
Show Less
Step 6: Transition to Answered Status
Check the response of the previous step to get information about how to transition the RFI to answered status. The user needs to have been assigned either a reviewer (projectArch) or manager (projectGC) workflow role.

Step 7: Transition to Closed Status
Check the response of the previous step to get information about how to transition the RFI to closed status. The user needs to have been assigned a manager workflow role (projectGC).