import pytest
import jwt
from unittest.mock import Mock, patch
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
from app.utils.exceptions import ValidationError


class TestAuthService:
    
    def setup_method(self):
        """Setup para cada teste"""
        self.auth_service = AuthService()
        self.user_repo = Mock(spec=UserRepository)
        self.auth_service.user_repository = self.user_repo
    
    def test_register_user_success(self):
        """Teste de registro de usuário com sucesso"""
        user_data = {
            'email': 'test@example.com',
            'password': 'password123',
            'name': 'Test User'
        }
        
        self.user_repo.find_by_email.return_value = None
        self.user_repo.create.return_value = {
            'id': 'user123',
            'email': 'test@example.com',
            'name': 'Test User'
        }
        
        result = self.auth_service.register_user(
            user_data['email'], 
            user_data['password'], 
            user_data['name']
        )
        
        assert result['success'] is True
        assert result['user']['email'] == 'test@example.com'
        assert result['user']['name'] == 'Test User'
        assert 'password_hash' not in result['user']
        self.user_repo.find_by_email.assert_called_once_with('test@example.com')
        self.user_repo.create.assert_called_once()
    
    def test_register_user_email_already_exists(self):
        """Teste de registro com email já existente"""
        user_data = {
            'email': 'existing@example.com',
            'password': 'password123',
            'name': 'Test User'
        }
        
        self.user_repo.find_by_email.return_value = {
            'id': 'existing123',
            'email': 'existing@example.com'
        }
        
        result = self.auth_service.register_user(
            user_data['email'], 
            user_data['password'], 
            user_data['name']
        )
        
        assert result['success'] is False
        assert result['message'] == 'User already exists'
    
    def test_login_user_success(self):
        """Teste de login com sucesso"""
        email = 'test@example.com'
        password = 'password123'
        
        user_data = {
            'id': 'user123',
            'email': 'test@example.com',
            'name': 'Test User',
            'password_hash': '$2b$12$hashedpassword'
        }
        
        self.user_repo.find_by_email.return_value = user_data
        
        with patch.object(self.auth_service, '_verify_password', return_value=True):
            with patch.object(self.auth_service, '_generate_token', return_value='mock_token'):
                
                result = self.auth_service.authenticate_user(email, password)
                
                assert result['success'] is True
                assert result['token'] == 'mock_token'
                assert result['user']['email'] == 'test@example.com'
                assert 'password_hash' not in result['user']
                self.user_repo.find_by_email.assert_called_once_with(email)
    
    def test_login_user_invalid_credentials(self):
        """Teste de login com credenciais inválidas"""
        email = 'test@example.com'
        password = 'wrongpassword'
        
        user_data = {
            'id': 'user123',
            'email': 'test@example.com',
            'name': 'Test User',
            'password_hash': '$2b$12$hashedpassword'
        }
        
        self.user_repo.find_by_email.return_value = user_data
        
        with patch.object(self.auth_service, '_verify_password', return_value=False):
            result = self.auth_service.authenticate_user(email, password)
            
            assert result['success'] is False
            assert 'Invalid password' in result['error']
    
    def test_login_user_not_found(self):
        """Teste de login com usuário não encontrado"""
        email = 'nonexistent@example.com'
        password = 'password123'
        
        self.user_repo.find_by_email.return_value = None
        
        result = self.auth_service.authenticate_user(email, password)
        
        assert result['success'] is False
        assert 'User not found' in result['error']
    
    def test_validate_token_success(self):
        """Teste de validação de token com sucesso"""
        token = 'valid_token'
        payload = {
            'user_id': 'user123',
            'email': 'test@example.com',
            'exp': 9999999999
        }
        
        user_data = {
            'id': 'user123',
            'email': 'test@example.com',
            'name': 'Test User'
        }
        
        with patch('app.services.auth_service.jwt.decode', return_value=payload):
            self.user_repo.find_by_id.return_value = user_data
            
            result = self.auth_service.validate_token(token)
            
            assert result['valid'] is True
            assert result['user']['id'] == 'user123'
            assert result['user']['email'] == 'test@example.com'
            self.user_repo.find_by_id.assert_called_once_with('user123')
    
    def test_validate_token_expired(self):
        """Teste de validação de token expirado"""
        token = 'expired_token'
        payload = {
            'user_id': 'user123',
            'email': 'test@example.com',
            'exp': 1000000000
        }
        
        with patch('app.services.auth_service.jwt.decode', return_value=payload):
            with patch('app.services.auth_service.datetime') as mock_datetime:
                mock_datetime.utcnow.return_value.timestamp.return_value = 9999999999
                result = self.auth_service.validate_token(token)
                
                assert result['valid'] is False
                assert "Token expired" in result['error']
                self.user_repo.find_by_id.assert_not_called()
    
    def test_validate_token_invalid(self):
        """Teste de validação de token inválido"""
        token = 'invalid_token'
        
        with patch('app.services.auth_service.jwt.decode', side_effect=jwt.InvalidTokenError):
            result = self.auth_service.validate_token(token)
            
            assert result['valid'] is False
            assert "Invalid token" in result['error']
            self.user_repo.find_by_id.assert_not_called()
    
    def test_validate_token_user_not_found(self):
        """Teste de validação de token com usuário não encontrado"""
        token = 'valid_token'
        payload = {
            'user_id': 'nonexistent123',
            'email': 'test@example.com',
            'exp': 9999999999
        }
        
        with patch('app.services.auth_service.jwt.decode', return_value=payload):
            self.user_repo.find_by_id.return_value = None
            
            result = self.auth_service.validate_token(token)
            
            assert result['valid'] is False
            assert "User not found" in result['error']
            self.user_repo.find_by_id.assert_called_once_with('nonexistent123')
