# test_server.py
import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from server import app, AWSHealthMCPServer
from botocore.exceptions import ClientError

client = TestClient(app)

# Mock AWS Health API responses
mock_health_events = {
    'events': [
        {
            'arn': 'arn:aws:health:us-east-1:123456789012:event/ABC123',
            'service': 'EC2',
            'eventTypeCode': 'AWS_EC2_INSTANCE_ISSUE',
            'statusCode': 'open',
            'region': 'us-east-1'
        }
    ]
}

mock_affected_entities = {
    'entities': [
        {
            'entityArn': 'arn:aws:ec2:us-east-1:123456789012:instance/i-1234567890abcdef0',
            'eventArn': 'arn:aws:health:us-east-1:123456789012:event/ABC123',
            'entityValue': 'i-1234567890abcdef0',
            'statusCode': 'IMPAIRED'
        }
    ]
}

mock_event_details = {
    'successfulSet': [
        {
            'event': {
                'arn': 'arn:aws:health:us-east-1:123456789012:event/ABC123',
                'service': 'EC2',
                'eventDescription': [
                    {
                        'language': 'en_US',
                        'latestDescription': 'EC2 instance is experiencing connectivity issues'
                    }
                ]
            }
        }
    ]
}

class TestAWSHealthMCPServer:
    
    def setup_method(self):
        """Setup method that runs before each test"""
        self.mock_client_patcher = patch('boto3.client')
        self.mock_client = self.mock_client_patcher.start()
        
        # Create a mock instance with all the necessary methods
        self.mock_health = Mock()
        self.mock_health.describe_events.return_value = mock_health_events
        self.mock_health.describe_affected_entities.return_value = mock_affected_entities
        self.mock_health.describe_event_details.return_value = mock_event_details
        
        # Make the client return our mock health instance
        self.mock_client.return_value = self.mock_health

    def teardown_method(self):
        """Teardown method that runs after each test"""
        self.mock_client_patcher.stop()

    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_describe_health_events_success(self):
        # Arrange
        self.mock_health.describe_events.return_value = mock_health_events

        # Act
        request_data = {
            "command": "describe_events",
            "parameters": {
                "categories": ["issue"],
                "regions": ["us-east-1"],
                "services": ["EC2"]
            }
        }
        response = client.post("/aws-health-mcp", json=request_data)
        
        # Assert
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert len(response.json()["events"]) == 1
        assert response.json()["events"][0]["service"] == "EC2"

    def test_describe_affected_entities_success(self):
        # Arrange
        self.mock_health.describe_affected_entities.return_value = mock_affected_entities

        # Act
        request_data = {
            "command": "describe_affected_entities",
            "parameters": {
                "eventArn": "arn:aws:health:us-east-1:123456789012:event/ABC123"
            }
        }
        response = client.post("/aws-health-mcp", json=request_data)
        
        # Assert
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert len(response.json()["entities"]) == 1

    def test_describe_event_details_success(self):
        # Arrange
        self.mock_health.describe_event_details.return_value = mock_event_details

        # Act
        request_data = {
            "command": "describe_event_details",
            "parameters": {
                "eventArn": "arn:aws:health:us-east-1:123456789012:event/ABC123"
            }
        }
        response = client.post("/aws-health-mcp", json=request_data)
        
        # Assert
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert len(response.json()["eventDetails"]) == 1

    def test_invalid_command(self):
        request_data = {
            "command": "invalid_command",
            "parameters": {}
        }
        response = client.post("/aws-health-mcp", json=request_data)
        assert response.status_code == 200
        assert response.json()["status"] == "error"
        assert "Unknown command" in response.json()["message"]

    def test_missing_event_arn(self):
        request_data = {
            "command": "describe_affected_entities",
            "parameters": {}
        }
        response = client.post("/aws-health-mcp", json=request_data)
        assert response.status_code == 200
        assert response.json()["status"] == "error"
        assert "eventArn is required" in response.json()["message"]

    def test_aws_api_error(self):
        # Arrange
        error_response = {
            'Error': {
                'Code': 'AWS API Error',
                'Message': 'AWS API Error'
            }
        }
        self.mock_health.describe_events.side_effect = ClientError(
            error_response, 'DescribeEvents')

        # Act
        request_data = {
            "command": "describe_events",
            "parameters": {
                "categories": ["issue"]
            }
        }
        response = client.post("/aws-health-mcp", json=request_data)
        
        # Assert
        assert response.status_code == 200
        assert response.json()["status"] == "error"
        assert "AWS API Error" in response.json()["message"]

if __name__ == "__main__":
    pytest.main(["-v", "test_server.py"])
