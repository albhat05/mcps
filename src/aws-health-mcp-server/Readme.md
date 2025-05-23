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

git clone <repository-url>
cd aws-health-mcp



##  Install required dependencies:

pip install boto3 fastapi uvicorn



## Configure AWS credentials:
```bash

export AWS_ACCESS_KEY_ID="your_access_key"
export AWS_SECRET_ACCESS_KEY="your_secret_key"
export AWS_REGION="your_region"



# Starting the Server
# Run the FastAPI server using uvicorn:

uvicorn main:app --reload


# The server will start on http://localhost:8000

# API Endpoints
POST /aws-health-mcp


# Describe Health Events:

{
    "command": "describe_events",
    "parameters": {
        "categories": ["issue", "scheduledChange"],
        "regions": ["us-east-1"],
        "services": ["EC2"]
    }
}



#  Describe Affected Entities:

{
    "command": "describe_affected_entities",
    "parameters": {
        "eventArn": "arn:aws:health:region:event-arn"
    }
}



# Describe Event Details:

{
    "command": "describe_event_details",
    "parameters": {
        "eventArn": "arn:aws:health:region:event-arn"
    }
}



# Response Format
# # Successful response:

{
    "status": "success",
    "events/entities/eventDetails": [...]
}



# Error response:

{
    "status": "error",
    "message": "Error description"
}

```

The server implements comprehensive error handling:

Invalid commands return a 500 error with details

AWS API errors are caught and returned with appropriate error messages

Request validation errors return appropriate HTTP status codes

Security Considerations
Always use environment variables for AWS credentials

Implement appropriate authentication for the FastAPI endpoint in production

Use HTTPS in production environments

Follow AWS IAM best practices for minimum required permissions
 ```bash
# IAM Permissions
# The AWS IAM user/role needs the following permissions:

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



# Testing
#  To run tests (once implemented):

pytest -v



## License

Acknowledgments
AWS Health API Documentation

FastAPI Documentation

Boto3 Documentation

