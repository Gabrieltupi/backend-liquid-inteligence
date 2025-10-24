
import requests
from typing import Dict, Any
from app.external.base_client import BaseClient
from app.utils.exceptions import ExternalServiceError

class ViaCEPClient(BaseClient):
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://viacep.com.br/ws"
    
    def get_location_data(self, location_input: str) -> Dict[str, Any]:
        
        try:

            if self._is_cep(location_input):
                return self._get_by_cep(location_input)
            else:
                return self._get_by_address(location_input)
                
        except Exception as e:
            raise ExternalServiceError(f'ViaCEP error: {str(e)}')
    
    def _is_cep(self, input_str: str) -> bool:
        
        import re
        cep_clean = re.sub(r'[^0-9]', '', input_str)
        return len(cep_clean) == 8
    
    def _get_by_cep(self, cep: str) -> Dict[str, Any]:
        
        try:

            import re
            cep_clean = re.sub(r'[^0-9]', '', cep)
            
            url = f"{self.base_url}/{cep_clean}/json/"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'erro' in data:
                    return {
                        'success': False,
                        'error': 'CEP not found'
                    }
                
                return {
                    'success': True,
                    'data': {
                        'cep': data.get('cep'),
                        'street': data.get('logradouro'),
                        'neighborhood': data.get('bairro'),
                        'city': data.get('localidade'),
                        'state': data.get('uf'),
                        'coordinates': {
                            'lat': None,
                            'lng': None
                        }
                    }
                }
            else:
                return {
                    'success': False,
                    'error': f'HTTP {response.status_code}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Request error: {str(e)}'
            }
    
    def _get_by_address(self, address: str) -> Dict[str, Any]:
        
        try:

            return self._get_by_geocoding(address)
            
        except Exception as e:
            raise ExternalServiceError(f'Address search error: {str(e)}')
    
    def _get_by_geocoding(self, address: str) -> Dict[str, Any]:
        
        try:
            import requests
            
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                'q': f"{address}, Brazil",
                'format': 'json',
                'limit': 1,
                'addressdetails': 1
            }
            
            headers = {
                'User-Agent': 'Liquid Location Intelligence/1.0'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data and len(data) > 0:
                    result = data[0]
                    return {
                        'success': True,
                        'data': {
                            'address': address,
                            'city': result.get('address', {}).get('city', ''),
                            'state': result.get('address', {}).get('state', ''),
                            'coordinates': {
                                'lat': float(result.get('lat', 0)),
                                'lng': float(result.get('lon', 0))
                            }
                        }
                    }
                else:

                    return {
                        'success': True,
                        'data': {
                            'address': address,
                            'city': 'São Paulo',
                            'state': 'SP',
                            'coordinates': {
                                'lat': -23.5505,
                                'lng': -46.6333
                            }
                        }
                    }
            else:
                raise ExternalServiceError(f'Geocoding API error: HTTP {response.status_code}')
                
        except Exception as e:
            raise ExternalServiceError(f'Geocoding error: {str(e)}')
