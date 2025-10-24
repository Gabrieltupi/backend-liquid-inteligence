
import requests
from typing import Dict, Any
from datetime import datetime
from app.external.base_client import BaseClient
from app.utils.exceptions import ExternalServiceError

class WeatherClient(BaseClient):
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.openweathermap.org/data/2.5"

        self.api_key = "your_api_key_here"
    
    def get_weather_data(self, coordinates: Dict[str, float]) -> Dict[str, Any]:
        
        try:
            lat = coordinates.get('lat')
            lng = coordinates.get('lng')
            
            if not lat or not lng:
                raise ExternalServiceError("Invalid coordinates")
            
            current_url = f"{self.base_url}/weather"
            params = {
                'lat': lat,
                'lon': lng,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'pt_br'
            }
            
            response = requests.get(current_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                return {
                    'success': True,
                    'data': {
                        'temperature': data['main']['temp'],
                        'feels_like': data['main']['feels_like'],
                        'humidity': data['main']['humidity'],
                        'pressure': data['main']['pressure'],
                        'description': data['weather'][0]['description'],
                        'wind_speed': data['wind']['speed'],
                        'wind_direction': data['wind'].get('deg', 0),
                        'visibility': data.get('visibility', 0) / 1000,
                        'cloudiness': data['clouds']['all'],
                        'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).isoformat(),
                        'sunset': datetime.fromtimestamp(data['sys']['sunset']).isoformat(),
                        'city': data['name'],
                        'country': data['sys']['country'],
                        'last_updated': datetime.utcnow().isoformat(),
                        'source': 'OpenWeatherMap'
                    }
                }
            elif response.status_code == 401:
                raise ExternalServiceError("Invalid API key for OpenWeatherMap")
            elif response.status_code == 404:
                raise ExternalServiceError("Location not found")
            else:
                raise ExternalServiceError(f"OpenWeatherMap API error: HTTP {response.status_code}")
                
        except requests.exceptions.Timeout:
            raise ExternalServiceError("Weather API timeout")
        except requests.exceptions.ConnectionError:
            raise ExternalServiceError("Weather API connection error")
        except Exception as e:
            raise ExternalServiceError(f"Weather API error: {str(e)}")
    
    def get_air_quality(self, coordinates: Dict[str, float]) -> Dict[str, Any]:
        
        try:
            lat = coordinates.get('lat')
            lng = coordinates.get('lng')
            
            if not lat or not lng:
                raise ExternalServiceError("Invalid coordinates")
            
            air_quality_url = f"{self.base_url}/air_pollution"
            params = {
                'lat': lat,
                'lon': lng,
                'appid': self.api_key
            }
            
            response = requests.get(air_quality_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                aqi = data['list'][0]['main']['aqi']
                
                aqi_levels = {
                    1: "Boa",
                    2: "Moderada", 
                    3: "Insalubre para grupos sensíveis",
                    4: "Insalubre",
                    5: "Muito insalubre"
                }
                
                return {
                    'success': True,
                    'data': {
                        'aqi': aqi,
                        'aqi_description': aqi_levels.get(aqi, "Desconhecida"),
                        'last_updated': datetime.utcnow().isoformat(),
                        'source': 'OpenWeatherMap'
                    }
                }
            else:

                return {
                    'success': True,
                    'data': {
                        'aqi': 2,
                        'aqi_description': "Moderada",
                        'last_updated': datetime.utcnow().isoformat(),
                        'source': 'Estimated'
                    }
                }
                
        except Exception as e:

            return {
                'success': True,
                'data': {
                    'aqi': 2,
                    'aqi_description': "Moderada",
                    'last_updated': datetime.utcnow().isoformat(),
                    'source': 'Estimated'
                }
            }
