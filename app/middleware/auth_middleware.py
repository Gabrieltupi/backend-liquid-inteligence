
from typing import Dict, Any
from app.services.auth_service import AuthService
from app.services.validation_service import ValidationService
from app.utils.exceptions import AuthenticationError

class AuthMiddleware:
    
    def __init__(self):
        self.auth_service = AuthService()
        self.validation_service = ValidationService()
    
    def validate_request(self, request_context: Dict[str, Any]) -> Dict[str, Any]:
        
        print("[AUTH_MIDDLEWARE] Iniciando validação de autenticação")
        print(f"[AUTH_MIDDLEWARE] Headers recebidos: {request_context.get('headers', {})}")
        
        token = self.validation_service.validate_auth_header(
            request_context.get('headers', {})
        )
        print(f"[AUTH_MIDDLEWARE] Token extraído: {token[:20]}..." if token else "[AUTH_MIDDLEWARE] Token: None")
        
        print("[AUTH_MIDDLEWARE] Validando token com AuthService")
        validation_result = self.auth_service.validate_token(token)
        print(f"[AUTH_MIDDLEWARE] Resultado da validação: {validation_result}")
        
        if not validation_result['valid']:
            print(f"[AUTH_MIDDLEWARE] Token inválido: {validation_result.get('error', 'Unknown error')}")
            raise AuthenticationError(validation_result['error'])
        
        print("[AUTH_MIDDLEWARE] Token válido! Retornando dados do usuário")
        return {
            'valid': True,
            'user': validation_result['user']
        }
