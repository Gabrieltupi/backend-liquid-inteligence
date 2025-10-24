
import logging
from typing import Dict, Any
from app.utils.formatters import ResponseFormatter
from app.utils.exceptions import ValidationError, ExternalServiceError, AuthenticationError, AuthorizationError

logger = logging.getLogger(__name__)

class ErrorMiddleware:
    
    def __init__(self):
        self.response_formatter = ResponseFormatter()
    
    def handle_error(self, error: Exception, request_context: Dict[str, Any] = None) -> Dict[str, Any]:
        
        self._log_error(error, request_context)
        
        if isinstance(error, ValidationError):
            return self._handle_validation_error(error)
        elif isinstance(error, AuthenticationError):
            return self._handle_authentication_error(error)
        elif isinstance(error, AuthorizationError):
            return self._handle_authorization_error(error)
        elif isinstance(error, ExternalServiceError):
            return self._handle_external_service_error(error)
        else:
            return self._handle_generic_error(error)
    
    def _log_error(self, error: Exception, request_context: Dict[str, Any] = None):
        
        error_info = {
            'error_type': type(error).__name__,
            'error_message': str(error),
            'request_path': request_context.get('path') if request_context else None,
            'request_method': request_context.get('method') if request_context else None
        }
        
        logger.error(f"Error occurred: {error_info}")
    
    def _handle_validation_error(self, error: ValidationError) -> Dict[str, Any]:
        
        return self.response_formatter.error_response(
            error_code="VALIDATION_ERROR",
            message=str(error),
            status_code=400
        )
    
    def _handle_authentication_error(self, error: AuthenticationError) -> Dict[str, Any]:
        
        return self.response_formatter.error_response(
            error_code="AUTHENTICATION_ERROR",
            message=str(error),
            status_code=401
        )
    
    def _handle_authorization_error(self, error: AuthorizationError) -> Dict[str, Any]:
        
        return self.response_formatter.error_response(
            error_code="AUTHORIZATION_ERROR",
            message=str(error),
            status_code=403
        )
    
    def _handle_external_service_error(self, error: ExternalServiceError) -> Dict[str, Any]:
        
        return self.response_formatter.error_response(
            error_code="EXTERNAL_SERVICE_ERROR",
            message=str(error),
            status_code=502
        )
    
    def _handle_generic_error(self, error: Exception) -> Dict[str, Any]:
        
        return self.response_formatter.error_response(
            error_code="INTERNAL_ERROR",
            message="An unexpected error occurred",
            status_code=500
        )
