# server.py
import boto3
from typing import Dict, Any
from fastapi import FastAPI
from pydantic import BaseModel

class MCPRequest(BaseModel):
    command: str
    parameters: Dict[str, Any]

class AWSHealthMCPServer:
    def __init__(self):
        self.health_client = boto3.client('health')
        
    async def handle_request(self, request: MCPRequest) -> Dict[str, Any]:
        try:
            command = request.command
            params = request.parameters
            
            if command == 'describe_events':
                return await self.describe_health_events(params)
            elif command == 'describe_affected_entities':
                return await self.describe_affected_entities(params)
            elif command == 'describe_event_details':
                return await self.describe_event_details(params)
            else:
                return {
                    'status': 'error',
                    'message': f"Unknown command: {command}"
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    async def describe_health_events(self, params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            response = self.health_client.describe_events(
                filter={
                    'eventTypeCategories': params.get('categories', ['issue']),
                    'regions': params.get('regions', ['us-east-1']),
                    'services': params.get('services', ['EC2'])
                }
            )
            return {
                'status': 'success',
                'events': response['events']
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    async def describe_affected_entities(self, params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if 'eventArn' not in params:
                return {
                    'status': 'error',
                    'message': 'eventArn is required'
                }
            
            response = self.health_client.describe_affected_entities(
                filter={
                    'eventArns': [params['eventArn']]
                }
            )
            return {
                'status': 'success',
                'entities': response['entities']
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    async def describe_event_details(self, params: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if 'eventArn' not in params:
                return {
                    'status': 'error',
                    'message': 'eventArn is required'
                }
            
            response = self.health_client.describe_event_details(
                eventArns=[params['eventArn']]
            )
            return {
                'status': 'success',
                'eventDetails': response['successfulSet']
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

app = FastAPI()
health_mcp = AWSHealthMCPServer()

@app.post("/aws-health-mcp")
async def process_mcp_request(request: MCPRequest):
    return await health_mcp.handle_request(request)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
