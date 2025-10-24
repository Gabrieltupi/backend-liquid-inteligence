from typing import Dict, Any
from app.services.auth_service import AuthService
from app.services.validation_service import ValidationService
from app.utils.formatters import ResponseFormatter
from app.utils.exceptions import ValidationError, AuthenticationError

class AuthController:
    
    def __init__(self):
        self.auth_service = AuthService()
        self.validation_service = ValidationService()
        self.response_formatter = ResponseFormatter()
    
    def login(self, request_context: Dict[str, Any]) -> Dict[str, Any]:
        validated_data = self.validation_service.validate_login_request(
            request_context.get('body', '{}')
        )
        
        auth_result = self.auth_service.authenticate_user(
            validated_data['email'], 
            validated_data['password']
        )
        
        if not auth_result['success']:
            raise AuthenticationError(auth_result['error'])
        
        return self.response_formatter.success_response(
            data={
                'token': auth_result['token'],
                'user': auth_result['user'],
                'expires_in': auth_result['expires_in']
            },
            message="Login successful"
        )
    
    def register(self, request_context: Dict[str, Any]) -> Dict[str, Any]:
        validated_data = self.validation_service.validate_register_request(
            request_context.get('body', '{}')
        )
        
        register_result = self.auth_service.register_user(
            validated_data['email'],
            validated_data['password'],
            validated_data['name']
        )
        
        if not register_result['success']:
            raise ValidationError(register_result['message'])
        
        return self.response_formatter.success_response(
            data={
                'user': register_result['user']
            },
            message="User registered successfully"
        )
