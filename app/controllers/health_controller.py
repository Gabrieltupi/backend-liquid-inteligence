from typing import Dict, Any
from app.utils.formatters import ResponseFormatter

class HealthController:
    
    def __init__(self):
        self.response_formatter = ResponseFormatter()
    
    def health_check(self, request_context: Dict[str, Any]) -> Dict[str, Any]:
        health_data = {
            'status': 'healthy',
            'service': 'Liquid Location Intelligence',
            'version': '1.0.0',
            'timestamp': request_context.get('timestamp'),
            'uptime': 'N/A'
        }
        
        return self.response_formatter.success_response(
            data=health_data,
            message="Service is healthy"
        )
