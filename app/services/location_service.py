
from typing import Dict, Any
from app.external.viacep_client import ViaCEPClient
from app.external.banco_central_client import BancoCentralClient
from app.external.weather_client import WeatherClient
from app.repositories.cache_repository import CacheRepository
from app.utils.exceptions import ExternalServiceError

class LocationService:
    
    def __init__(self):
        self.viacep_client = ViaCEPClient()
        self.banco_central_client = BancoCentralClient()
        self.weather_client = WeatherClient()
        self.cache_repository = CacheRepository()
    
    def analyze_location(self, location_input: str) -> Dict[str, Any]:
        
        try:

            cache_key = f"location:{location_input.lower()}"
            cached_data = self.cache_repository.get(cache_key)
            
            if cached_data:
                return cached_data
            
            analysis_data = {
                'location': location_input,
                'geographic': {},
                'economic': {},
                'climate': {},
                'demographic': {}
            }
            
            geographic_data = self.viacep_client.get_location_data(location_input)
            if geographic_data['success']:
                analysis_data['geographic'] = geographic_data['data']
            
            economic_data = self.banco_central_client.get_economic_data()
            if economic_data['success']:
                analysis_data['economic'] = economic_data['data']
            
            if geographic_data['success'] and 'coordinates' in geographic_data['data']:
                coordinates = geographic_data['data']['coordinates']
                try:
                    climate_data = self.weather_client.get_weather_data(coordinates)
                    analysis_data['climate'] = climate_data['data']
                    
                    air_quality_data = self.weather_client.get_air_quality(coordinates)
                    analysis_data['climate']['air_quality'] = air_quality_data['data']
                except Exception as e:

                    analysis_data['climate'] = {
                        'temperature': 22,
                        'humidity': 60,
                        'description': 'Dados indisponíveis',
                        'air_quality': {'aqi_description': 'Moderada'}
                    }
            
            self.cache_repository.set(cache_key, analysis_data, ttl=3600)
            
            return analysis_data
            
        except Exception as e:
            raise ExternalServiceError(f'Location analysis failed: {str(e)}')
