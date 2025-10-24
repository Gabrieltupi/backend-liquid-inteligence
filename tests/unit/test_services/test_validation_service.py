import pytest
import json
from app.services.validation_service import ValidationService
from app.utils.exceptions import ValidationError


class TestValidationService:
    
    def setup_method(self):
        """Setup para cada teste"""
        self.validation_service = ValidationService()
    
    def test_validate_login_request_success(self):
        """Teste de validação de request de login com sucesso"""
        body = json.dumps({
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        result = self.validation_service.validate_login_request(body)
        
        assert result['email'] == 'test@example.com'
        assert result['password'] == 'password123'
    
    def test_validate_login_request_invalid_json(self):
        """Teste de validação com JSON inválido"""
        body = 'invalid json'
        
 & Assert
        with pytest.raises(ValidationError) as exc_info:
            self.validation_service.validate_login_request(body)
        
        assert "Invalid JSON in request body" in str(exc_info.value)
    
    def test_validate_login_request_missing_email(self):
        """Teste de validação com email ausente"""
        body = json.dumps({
            'password': 'password123'
        })
        
 & Assert
        with pytest.raises(ValidationError) as exc_info:
            self.validation_service.validate_login_request(body)
        
        assert "Email and password are required" in str(exc_info.value)
    
    def test_validate_login_request_missing_password(self):
        """Teste de validação com senha ausente"""
        body = json.dumps({
            'email': 'test@example.com'
        })
        
 & Assert
        with pytest.raises(ValidationError) as exc_info:
            self.validation_service.validate_login_request(body)
        
        assert "Email and password are required" in str(exc_info.value)
    
    def test_validate_login_request_invalid_email_format(self):
        """Teste de validação com formato de email inválido"""
        body = json.dumps({
            'email': 'invalid-email',
            'password': 'password123'
        })
        
 & Assert
        with pytest.raises(ValidationError) as exc_info:
            self.validation_service.validate_login_request(body)
        
        assert "Invalid email format" in str(exc_info.value)
    
    def test_validate_login_request_email_normalization(self):
        """Teste de normalização do email"""
        body = json.dumps({
            'email': '  TEST@EXAMPLE.COM  ',
            'password': 'password123'
        })
        
        result = self.validation_service.validate_login_request(body)
        
        assert result['email'] == 'test@example.com'
    
    def test_validate_register_request_success(self):
        """Teste de validação de request de registro com sucesso"""
        body = json.dumps({
            'email': 'test@example.com',
            'password': 'password123',
            'name': 'Test User'
        })
        
        result = self.validation_service.validate_register_request(body)
        
        assert result['email'] == 'test@example.com'
        assert result['password'] == 'password123'
        assert result['name'] == 'Test User'
    
    def test_validate_register_request_missing_fields(self):
        """Teste de validação com campos ausentes"""
        body = json.dumps({
            'email': 'test@example.com',
            'password': 'password123'
        })
        
 & Assert
        with pytest.raises(ValidationError) as exc_info:
            self.validation_service.validate_register_request(body)
        
        assert "Email, password and name are required" in str(exc_info.value)
    
    def test_validate_register_request_short_password(self):
        """Teste de validação com senha muito curta"""
        body = json.dumps({
            'email': 'test@example.com',
            'password': '123',
            'name': 'Test User'
        })
        
 & Assert
        with pytest.raises(ValidationError) as exc_info:
            self.validation_service.validate_register_request(body)
        
        assert "Password must be at least 8 characters" in str(exc_info.value)
    
    def test_validate_register_request_name_normalization(self):
        """Teste de normalização do nome"""
        body = json.dumps({
            'email': 'test@example.com',
            'password': 'password123',
            'name': '  Test User  '
        })
        
        result = self.validation_service.validate_register_request(body)
        
        assert result['name'] == 'Test User'
    
    def test_validate_location_request_success(self):
        """Teste de validação de request de localização com sucesso"""
        body = json.dumps({
            'location': '01310-100'
        })
        
        result = self.validation_service.validate_location_request(body)
        
        assert result['location'] == '01310-100'
    
    def test_validate_location_request_missing_location(self):
        """Teste de validação com localização ausente"""
        body = json.dumps({})
        
 & Assert
        with pytest.raises(ValidationError) as exc_info:
            self.validation_service.validate_location_request(body)
        
        assert "Location parameter is required" in str(exc_info.value)
    
    def test_validate_location_request_empty_location(self):
        """Teste de validação com localização vazia"""
        body = json.dumps({
            'location': ''
        })
        
 & Assert
        with pytest.raises(ValidationError) as exc_info:
            self.validation_service.validate_location_request(body)
        
        assert "Location parameter is required" in str(exc_info.value)
    
    def test_validate_location_request_invalid_format(self):
        """Teste de validação com formato inválido"""
        body = json.dumps({
            'location': '   '
        })
        
 & Assert
        with pytest.raises(ValidationError) as exc_info:
            self.validation_service.validate_location_request(body)
        
        assert "Invalid location format" in str(exc_info.value)
    
    def test_validate_location_request_normalization(self):
        """Teste de normalização da localização"""
        body = json.dumps({
            'location': '  01310-100  '
        })
        
        result = self.validation_service.validate_location_request(body)
        
        assert result['location'] == '01310-100'
    
    def test_validate_auth_header_success(self):
        """Teste de validação de header de autenticação com sucesso"""
        headers = {
            'Authorization': 'Bearer valid_token_here'
        }
        
        result = self.validation_service.validate_auth_header(headers)
        
        assert result == 'valid_token_here'
    
    def test_validate_auth_header_case_insensitive(self):
        """Teste de validação case insensitive"""
        headers = {
            'authorization': 'Bearer valid_token_here'
        }
        
        result = self.validation_service.validate_auth_header(headers)
        
        assert result == 'valid_token_here'
    
    def test_validate_auth_header_missing(self):
        """Teste de validação com header ausente"""
        headers = {}
        
 & Assert
        with pytest.raises(ValidationError) as exc_info:
            self.validation_service.validate_auth_header(headers)
        
        assert "Authorization header missing" in str(exc_info.value)
    
    def test_validate_auth_header_invalid_format(self):
        """Teste de validação com formato inválido"""
        headers = {
            'Authorization': 'InvalidFormat token'
        }
        
 & Assert
        with pytest.raises(ValidationError) as exc_info:
            self.validation_service.validate_auth_header(headers)
        
        assert "Invalid authorization format" in str(exc_info.value)
    
    def test_validate_auth_header_empty_token(self):
        """Teste de validação com token vazio"""
        headers = {
            'Authorization': 'Bearer '
        }
        
 & Assert
        with pytest.raises(ValidationError) as exc_info:
            self.validation_service.validate_auth_header(headers)
        
        assert "Token is empty" in str(exc_info.value)
    
    def test_validate_auth_header_no_bearer(self):
        """Teste de validação sem Bearer"""
        headers = {
            'Authorization': 'just_token'
        }
        
 & Assert
        with pytest.raises(ValidationError) as exc_info:
            self.validation_service.validate_auth_header(headers)
        
        assert "Invalid authorization format" in str(exc_info.value)
