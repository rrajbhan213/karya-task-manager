# TODO API

## Overview

This project is a serverless TODO API built using AWS Serverless Architecture. The API allows users to manage tasks (CRUD operations), attach files to tasks, and receive reminders via email for upcoming due dates. It utilizes AWS services like **Lambda**, **API Gateway**, **DynamoDB**, **S3**, **SNS**, **SQS**, and **Cognito** for authentication and authorization.

---

## Features

- **User Authentication**:
  - Uses **AWS Cognito** for secure user management.
  - Supports **OAuth 2.0 Code Flow** for user login.
  - Supports **Client Credentials Flow** for machine-to-machine communication.
  
- **CRUD Operations**:
  - Create, Read, Update, and Delete tasks using API Gateway and Lambda functions.

- **File Attachments**:
  - Upload files to an **S3 bucket** and associate them with tasks.

- **Reminders**:
  - Utilize **SQS** and **SNS** to send email reminders for tasks with upcoming due dates.

- **Serverless Deployment**:
  - Powered by AWS SAM (Serverless Application Model).

---

## Architecture

![Architecture Diagram](https://via.placeholder.com/800x400.png?text=Architecture+Diagram)

---

## Prerequisites

1. **AWS CLI**: Install the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) and configure it with appropriate credentials.
2. **AWS SAM CLI**: Install the [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html).
3. **Node.js**: Install [Node.js](https://nodejs.org/) for testing purposes if needed.
4. **Postman**: For testing API endpoints.

---

## Deployment

### Steps to Deploy the Project

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. **Build the Project**:
    ```bash
    sam build
    ```

3. **Deploy the project**:
    ```bash
    sam deploy --guided
    ```

During the deployment, provide:

- Stack name: TODOApiStack
- Project name: Example: todo
- Environment: Example: dev
- Region: Example: us-east-1

4. **Retrieve Outputs**: After deployment, note the following outputs:

- **API Endpoint**: For accessing the API Gateway.
- **Cognito User Pool ID** and **Client IDs** for authentication.

## API Endpoints

| API Endpoints | HTTP Method | Endpoint | Description |
|---|---|---|---|
| Create Task | POST | /api/tasks | Create a new task. |
| Fetch Tasks | GET | /api/tasks | Fetch all tasks. |
| Update Task | PUT | /api/tasks/{taskId} | Update an existing task. |
| Delete Task | DELETE | /api/tasks/{taskId} | Delete a task. |
| Attach File | POST | /api/tasks/{taskId}/attachments | Attach a file to a task. |

## AWS Services Used

- **AWS Lambda**: Compute layer for business logic.
- **Amazon API Gateway**: Exposes RESTful endpoints.
- **Amazon DynamoDB**: Stores tasks and metadata.
- **Amazon S3**: Stores file attachments.
- **Amazon SQS**: Queues for reminders.
- **Amazon SNS**: Sends email reminders.
- **Amazon Cognito**: Authentication and authorization.

## Folder Structure

```bash
project-root/
│
├── src/
│   ├── lambdas/
│   │   ├── create_task/
│   │   │   └── main.py
│   │   ├── get_tasks/
│   │   │   └── main.py
│   │   ├── update_task/
│   │   │   └── main.py
│   │   ├── delete_task/
│   │   │   └── main.py
│   │   ├── attach_file/
│   │   │   └── main.py
│   │   └── send_reminder/
│   │       └── main.py
│   └── shared/
│       └── utils.py
│
├── template.yaml
└── README.md
```