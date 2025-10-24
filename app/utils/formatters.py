
import json
from typing import Dict, Any, Optional
from datetime import datetime

class ResponseFormatter:
    
    def success_response(self, data: Any, message: str = "Success", status_code: int = 200) -> Dict[str, Any]:
        
        return {
            'statusCode': status_code,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
            },
            'body': json.dumps({
                'success': True,
                'message': message,
                'data': data,
                'timestamp': datetime.utcnow().isoformat()
            })
        }
    
    def error_response(self, error_code: str, message: str, status_code: int = 400, details: Optional[Dict] = None) -> Dict[str, Any]:
        
        error_data = {
            'success': False,
            'error_code': error_code,
            'message': message,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        if details:
            error_data['details'] = details
        
        return {
            'statusCode': status_code,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
            },
            'body': json.dumps(error_data)
        }
