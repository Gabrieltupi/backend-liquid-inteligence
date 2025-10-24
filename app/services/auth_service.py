
import jwt
import hashlib
import os
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from app.repositories.user_repository import UserRepository
from app.utils.exceptions import AuthenticationError, ValidationError

class AuthService:
    
    def __init__(self):
        self.user_repository = UserRepository()

        self.secret_key = os.getenv('JWT_SECRET')
        if not self.secret_key:
            raise ValueError("JWT_SECRET environment variable is required")
        
        self.token_expiry = int(os.getenv('JWT_EXPIRY', '3600'))
    
    def authenticate_user(self, email: str, password: str) -> Dict[str, Any]:
        
        try:

            user_data = self.user_repository.find_by_email(email)
            
            if not user_data:
                return {
                    'success': False,
                    'error': 'User not found'
                }
            
            if not self._verify_password(password, user_data['password_hash']):
                return {
                    'success': False,
                    'error': 'Invalid password'
                }
            
            token = self._generate_token(user_data)
            
            return {
                'success': True,
                'token': token,
                'user': {
                    'id': user_data['id'],
                    'email': user_data['email'],
                    'name': user_data['name']
                },
                'expires_in': self.token_expiry
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Authentication failed: {str(e)}'
            }
    
    def register_user(self, email: str, password: str, name: str) -> Dict[str, Any]:
        
        try:

            existing_user = self.user_repository.find_by_email(email)
            if existing_user:
                return {
                    'success': False,
                    'message': 'User already exists'
                }
            
            password_hash = self._hash_password(password)
            
            user_data = {
                'email': email,
                'password_hash': password_hash,
                'name': name,
                'created_at': datetime.utcnow().isoformat()
            }
            
            user = self.user_repository.create(user_data)
            
            return {
                'success': True,
                'user': {
                    'id': user['id'],
                    'email': user['email'],
                    'name': user['name']
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Registration failed: {str(e)}'
            }
    
    def validate_token(self, token: str) -> Dict[str, Any]:
        
        try:
            
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            
            exp = payload.get('exp')
            current_time = datetime.utcnow().timestamp()
            
            if exp and current_time > exp:
                return {
                    'valid': False,
                    'error': 'Token expired'
                }
            
            user_id = payload.get('user_id')
            user_data = self.user_repository.find_by_id(user_id)
            
            if not user_data:
                return {
                    'valid': False,
                    'error': 'User not found'
                }
            
            return {
                'valid': True,
                'user': {
                    'id': user_data['id'],
                    'email': user_data['email'],
                    'name': user_data['name']
                }
            }
            
        except jwt.ExpiredSignatureError:
            return {
                'valid': False,
                'error': 'Token expired'
            }
        except jwt.InvalidTokenError:
            return {
                'valid': False,
                'error': 'Invalid token'
            }
        except Exception as e:
            return {
                'valid': False,
                'error': f'Token validation failed: {str(e)}'
            }
    
    def _hash_password(self, password: str) -> str:
        
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        
        return self._hash_password(password) == password_hash
    
    def _generate_token(self, user: Dict[str, Any]) -> str:
        
        payload = {
            'user_id': user['id'],
            'email': user['email'],
            'exp': int(datetime.utcnow().timestamp()) + self.token_expiry
        }
        
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
