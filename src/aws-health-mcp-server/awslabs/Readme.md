# AWS Health MCP Server

A Model Context Protocol (MCP) server implementation for AWS Health API that enables programmatic access to AWS Health events, affected entities, and event details.

## Features

- Asynchronous request handling
- Support for multiple AWS Health API operations:
  - Describe health events
  - Get affected entities
  - Retrieve detailed event information
- FastAPI integration for HTTP endpoints
- Comprehensive error handling
- Type-safe implementation

## Prerequisites

- Python 3.7+
- AWS Account with appropriate IAM permissions
- AWS credentials configured

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd aws-health-mcp


Copy

Insert at cursor
markdown
Install required dependencies:

pip install boto3 fastapi uvicorn


Copy

Insert at cursor
bash
Configure AWS credentials:

export AWS_ACCESS_KEY_ID="your_access_key"
export AWS_SECRET_ACCESS_KEY="your_secret_key"
export AWS_REGION="your_region"


Copy

Insert at cursor
bash
Usage
Starting the Server
Run the FastAPI server using uvicorn:

uvicorn main:app --reload


Copy

Insert at cursor
bash
The server will start on http://localhost:8000

API Endpoints
POST /aws-health-mcp
Accepts MCP requests for AWS Health operations.

Example requests:

Describe Health Events:

{
    "command": "describe_events",
    "parameters": {
        "categories": ["issue", "scheduledChange"],
        "regions": ["us-east-1"],
        "services": ["EC2"]
    }
}


Copy

Insert at cursor
json
Describe Affected Entities:

{
    "command": "describe_affected_entities",
    "parameters": {
        "eventArn": "arn:aws:health:region:event-arn"
    }
}


Copy

Insert at cursor
json
Describe Event Details:

{
    "command": "describe_event_details",
    "parameters": {
        "eventArn": "arn:aws:health:region:event-arn"
    }
}


Copy

Insert at cursor
json
Response Format
Successful response:

{
    "status": "success",
    "events/entities/eventDetails": [...]
}


Copy

Insert at cursor
json
Error response:

{
    "status": "error",
    "message": "Error description"
}


Copy

Insert at cursor
json
Error Handling
The server implements comprehensive error handling:

Invalid commands return a 500 error with details

AWS API errors are caught and returned with appropriate error messages

Request validation errors return appropriate HTTP status codes

Security Considerations
Always use environment variables for AWS credentials

Implement appropriate authentication for the FastAPI endpoint in production

Use HTTPS in production environments

Follow AWS IAM best practices for minimum required permissions

IAM Permissions
The AWS IAM user/role needs the following permissions:

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "health:DescribeEvents",
                "health:DescribeEventDetails",
                "health:DescribeAffectedEntities"
            ],
            "Resource": "*"
        }
    ]
}


Copy

Insert at cursor
json
Development
Project Structure
aws-health-mcp/
├── main.py
├── requirements.txt
└── README.md


Copy

Insert at cursor
Contributing
Fork the repository

Create a feature branch

Commit your changes

Push to the branch

Create a Pull Request

Testing
To run tests (once implemented):

pytest


Copy

Insert at cursor
bash
License
Add your chosen license here

Support
For support, please create an issue in the repository.

Acknowledgments
AWS Health API Documentation

FastAPI Documentation

Boto3 Documentation


This README.md provides:
- Clear installation and setup instructions
- Detailed usage examples
- Security considerations
- API documentation
- Development guidelines
- Required permissions
- Project structure

You may want to customize:
- Repository URLs
- License information
- Support channels
- Any specific deployment instructions for your environment
- Additional features or limitations specific to your implementation

Remember to keep the README updated as you make changes to the implementation.