
from typing import Dict, Any
from app.services.auth_service import AuthService
from app.services.validation_service import ValidationService
from app.utils.exceptions import AuthenticationError

class AuthMiddleware:
    
    def __init__(self):
        self.auth_service = AuthService()
        self.validation_service = ValidationService()
    
    def validate_request(self, request_context: Dict[str, Any]) -> Dict[str, Any]:
        
        
        token = self.validation_service.validate_auth_header(
            request_context.get('headers', {})
        )
        
        validation_result = self.auth_service.validate_token(token)
        
        if not validation_result['valid']:
            raise AuthenticationError(validation_result['error'])
        
        return {
            'valid': True,
            'user': validation_result['user']
        }
