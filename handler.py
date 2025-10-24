import json
import logging
from datetime import datetime
from typing import Dict, Any
from app.main import create_app

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = create_app()

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        
        logger.info(f"Received event: {json.dumps(event)}")
        
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        headers = event.get('headers', {})
        body = event.get('body', '{}')
        query_params = event.get('queryStringParameters', {}) or {}
        
        
        request_context = {
            'method': http_method,
            'path': path,
            'headers': headers,
            'body': body,
            'query_params': query_params,
            'event': event,
            'context': context
        }
        
        response = app.process_request(request_context)
        
        logger.info(f"Response: {json.dumps(response)}")
        
        return response
        
    except Exception as e:
        
        logger.error(f"Error processing request: {str(e)}")
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
            },
            'body': json.dumps({
                'success': False,
                'error_code': 'INTERNAL_ERROR',
                'message': 'An unexpected error occurred',
                'timestamp': str(datetime.now())
            })
        }

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    return handler(event, context)
