import logging
from typing import Dict, Any
from app.controllers.auth_controller import AuthController
from app.controllers.location_controller import LocationController
from app.controllers.health_controller import HealthController
from app.middleware.auth_middleware import AuthMiddleware
from app.middleware.error_middleware import ErrorMiddleware
from app.middleware.logging_middleware import LoggingMiddleware
from app.utils.formatters import ResponseFormatter
from app.utils.exceptions import ValidationError, ExternalServiceError

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LiquidApp:
    
    def __init__(self):
        self.logger = logger
        
        self.auth_middleware = AuthMiddleware()
        self.error_middleware = ErrorMiddleware()
        self.logging_middleware = LoggingMiddleware()
        
        self.auth_controller = AuthController()
        self.location_controller = LocationController()
        self.health_controller = HealthController()
        
        self.response_formatter = ResponseFormatter()
        
        self.logger.info("Liquid Location Intelligence app initialized")
    
    def process_request(self, request_context: Dict[str, Any]) -> Dict[str, Any]:
        try:
            request_context = self.logging_middleware.process_request(request_context)
            
            method = request_context['method']
            path = request_context['path']
            
            if path == '/health':
                return self.health_controller.health_check(request_context)
            
            elif path.startswith('/api/auth'):
                return self._route_auth(method, path, request_context)
            
            elif path.startswith('/api/location'):
                return self._route_location(method, path, request_context)
            
            else:
                return self.response_formatter.error_response(
                    error_code="NOT_FOUND",
                    message="Endpoint not found",
                    status_code=404
                )
                
        except Exception as e:
            return self.error_middleware.handle_error(e, request_context)
    
    def _route_auth(self, method: str, path: str, request_context: Dict[str, Any]) -> Dict[str, Any]:
        if path == '/api/auth/login' and method == 'POST':
            return self.auth_controller.login(request_context)
        elif path == '/api/auth/register' and method == 'POST':
            return self.auth_controller.register(request_context)
        else:
            return self.response_formatter.error_response(
                error_code="METHOD_NOT_ALLOWED",
                message="Method not allowed for this endpoint",
                status_code=405
            )
    
    def _route_location(self, method: str, path: str, request_context: Dict[str, Any]) -> Dict[str, Any]:
        
        if path == '/api/location/analyze' and method == 'POST':
            auth_result = self.auth_middleware.validate_request(request_context)
            request_context['user'] = auth_result['user']
            return self.location_controller.analyze_location(request_context)
        else:
            return self.response_formatter.error_response(
                error_code="METHOD_NOT_ALLOWED",
                message="Method not allowed for this endpoint",
                status_code=405
            )

def create_app() -> LiquidApp:
    return LiquidApp()
