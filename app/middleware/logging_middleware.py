
import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class LoggingMiddleware:
    
    def process_request(self, request_context: Dict[str, Any]) -> Dict[str, Any]:
        
        request_context['timestamp'] = datetime.utcnow().isoformat()
        
        method = request_context.get('method', 'UNKNOWN')
        path = request_context.get('path', 'UNKNOWN')
        
        logger.info(f"Processing {method} {path}")
        
        return request_context
