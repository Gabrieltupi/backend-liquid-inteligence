import pytest
from unittest.mock import Mock, patch
from app.services.location_service import LocationService
from app.external.viacep_client import ViaCEPClient
from app.external.banco_central_client import BancoCentralClient
from app.external.weather_client import WeatherClient
from app.repositories.cache_repository import CacheRepository
from app.utils.exceptions import ExternalServiceError


class TestLocationService:
    
    def setup_method(self):
        """Setup para cada teste"""
        self.location_service = LocationService()
        
        self.viacep_client = Mock(spec=ViaCEPClient)
        self.banco_central_client = Mock(spec=BancoCentralClient)
        self.weather_client = Mock(spec=WeatherClient)
        self.cache_repo = Mock(spec=CacheRepository)
        
        self.location_service.viacep_client = self.viacep_client
        self.location_service.banco_central_client = self.banco_central_client
        self.location_service.weather_client = self.weather_client
        self.location_service.cache_repository = self.cache_repo
    
    def test_analyze_location_success(self):
        """Teste de análise de localização com sucesso"""
        location_input = "93230-600"
        
        self.cache_repo.get.return_value = None
        
        self.viacep_client.get_location_data.return_value = {
            'success': True,
                'data': {
                    'cep': '93230-600',
                    'street': 'Avenida Juventino Machado',
                    'neighborhood': 'Centro',
                    'city': 'Sapucaia do Sul',
                    'state': 'RS',
                    'coordinates': {'lat': -29.8275, 'lng': -51.1464}
                }
        }
        
        self.banco_central_client.get_economic_data.return_value = {
            'success': True,
            'data': {
                'interest_rate': 8.5,
                'inflation': 4.2,
                'currency': 'BRL',
                'last_updated': '2025-01-01T00:00:00Z'
            }
        }
        
        self.weather_client.get_weather_data.return_value = {
            'success': True,
            'data': {
                'temperature': 22,
                'feels_like': 24,
                'description': 'Ensolarado',
                'humidity': 65,
                'pressure': 1013,
                'wind_speed': 3.5,
                'last_updated': '2025-01-01T00:00:00Z'
            }
        }
        
        self.cache_repo.set.return_value = True
        
        result = self.location_service.analyze_location(location_input)
        
        assert result['location'] == '93230-600'
        assert 'geographic' in result
        assert 'economic' in result
        assert 'climate' in result
        
        self.cache_repo.get.assert_called_once_with(f'location:{location_input}')
        self.cache_repo.set.assert_called_once()
        
        self.viacep_client.get_location_data.assert_called_once_with(location_input)
        self.banco_central_client.get_economic_data.assert_called_once()
        self.weather_client.get_weather_data.assert_called_once()
    
    def test_analyze_location_from_cache(self):
        """Teste de análise de localização usando cache"""
        location_input = "93230-600"
        
        cached_data = {
            'success': True,
            'location': '93230-600',
            'geographic': {'city': 'Sapucaia do Sul'},
            'economic': {'interest_rate': 8.5},
            'climate': {'temperature': 22}
        }
        
        self.cache_repo.get.return_value = cached_data
        
        result = self.location_service.analyze_location(location_input)
        
        assert result == cached_data
        self.cache_repo.get.assert_called_once_with(f'location:{location_input}')
        
        self.viacep_client.get_location_data.assert_not_called()
        self.banco_central_client.get_economic_data.assert_not_called()
        self.weather_client.get_weather_data.assert_not_called()
    
    def test_analyze_location_viacep_error(self):
        """Teste de análise com erro na API ViaCEP"""
        location_input = "cep-invalido"
        
        self.cache_repo.get.return_value = None
        self.viacep_client.get_location_data.side_effect = ExternalServiceError("ViaCEP error")
        
 & Assert
        with pytest.raises(ExternalServiceError) as exc_info:
            self.location_service.analyze_location(location_input)
        
        assert "ViaCEP error" in str(exc_info.value)
        self.viacep_client.get_location_data.assert_called_once_with(location_input)
    
    def test_analyze_location_banco_central_error(self):
        """Teste de análise com erro na API Banco Central"""
        location_input = "93230-600"
        
        self.cache_repo.get.return_value = None
        
        self.viacep_client.get_location_data.return_value = {
            'success': True,
            'data': {'city': 'Sapucaia do Sul'}
        }
        
        self.banco_central_client.get_economic_data.side_effect = ExternalServiceError("Banco Central error")
        
 & Assert
        with pytest.raises(ExternalServiceError) as exc_info:
            self.location_service.analyze_location(location_input)
        
        assert "Banco Central error" in str(exc_info.value)
        self.banco_central_client.get_economic_data.assert_called_once()
    
    def test_analyze_location_weather_error(self):
        """Teste de análise com erro na API Weather"""
        location_input = "93230-600"
        
        self.cache_repo.get.return_value = None
        
        self.viacep_client.get_location_data.return_value = {
            'success': True,
            'data': {
                'city': 'Sapucaia do Sul',
                'coordinates': {'lat': -29.8275, 'lng': -51.1464}
            }
        }
        
        self.banco_central_client.get_economic_data.return_value = {
            'success': True,
            'data': {'interest_rate': 8.5}
        }
        
        self.weather_client.get_weather_data.side_effect = ExternalServiceError("Weather error")
        
        result = self.location_service.analyze_location(location_input)
        
 - O serviço continua mesmo com erro no weather
        assert result['location'] == '93230-600'
        assert 'geographic' in result
        assert 'economic' in result
        self.weather_client.get_weather_data.assert_called_once()
    
    def test_analyze_location_partial_data_success(self):
        """Teste de análise com dados parciais (algumas APIs falham mas outras funcionam)"""
        location_input = "93230-600"
        
        self.cache_repo.get.return_value = None
        
        self.viacep_client.get_location_data.return_value = {
            'success': True,
            'data': {
                'cep': '93230-600',
                'city': 'Sapucaia do Sul',
                'state': 'RS'
            }
        }
        
        self.banco_central_client.get_economic_data.side_effect = ExternalServiceError("Banco Central error")
        
        self.weather_client.get_weather_data.return_value = {
            'success': True,
            'data': {
                'temperature': 22,
                'description': 'Ensolarado'
            }
        }
        
 & Assert
        with pytest.raises(ExternalServiceError) as exc_info:
            self.location_service.analyze_location(location_input)
        
        assert "Banco Central error" in str(exc_info.value)
    
    def test_analyze_location_empty_input(self):
        """Teste de análise com entrada vazia"""
        location_input = ""
        
 & Assert
        with pytest.raises(ValueError) as exc_info:
            self.location_service.analyze_location(location_input)
        
        assert "Location input cannot be empty" in str(exc_info.value)
    
    def test_analyze_location_none_input(self):
        """Teste de análise com entrada None"""
        location_input = None
        
 & Assert
        with pytest.raises(ValueError) as exc_info:
            self.location_service.analyze_location(location_input)
        
        assert "Location input cannot be empty" in str(exc_info.value)
