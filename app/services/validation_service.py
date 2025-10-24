
import json
from typing import Dict, Any, Optional, List
from app.utils.validators import validate_email, validate_password, validate_location_input
from app.utils.exceptions import ValidationError

class ValidationService:
    
    def validate_login_request(self, body: str) -> Dict[str, Any]:
        
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            raise ValidationError("Invalid JSON in request body")
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            raise ValidationError("Email and password are required")
        
        if not validate_email(email):
            raise ValidationError("Invalid email format")
        
        return {
            'email': email.strip().lower(),
            'password': password
        }
    
    def validate_register_request(self, body: str) -> Dict[str, Any]:
        
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            raise ValidationError("Invalid JSON in request body")
        
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        
        if not all([email, password, name]):
            raise ValidationError("Email, password and name are required")
        
        if not validate_email(email):
            raise ValidationError("Invalid email format")
        
        if not validate_password(password):
            raise ValidationError("Password must be at least 8 characters")
        
        return {
            'email': email.strip().lower(),
            'password': password,
            'name': name.strip()
        }
    
    def validate_location_request(self, body: str) -> Dict[str, Any]:
        
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            raise ValidationError("Invalid JSON in request body")
        
        location = data.get('location')
        
        if not location:
            raise ValidationError("Location parameter is required")
        
        if not validate_location_input(location):
            raise ValidationError("Invalid location format")
        
        return {
            'location': location.strip()
        }
    
    def validate_auth_header(self, headers: Dict[str, str]) -> str:
        
        auth_header = headers.get('Authorization') or headers.get('authorization')
        
        if not auth_header:
            raise ValidationError("Authorization header missing")
        
        if not auth_header.startswith('Bearer '):
            raise ValidationError("Invalid authorization format")
        
        token = auth_header[7:]
        
        if not token:
            raise ValidationError("Token is empty")
        
        return token
