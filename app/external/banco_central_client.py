
import requests
from typing import Dict, Any
from app.external.base_client import BaseClient

class BancoCentralClient(BaseClient):
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/1"
    
    def get_economic_data(self) -> Dict[str, Any]:
        
        try:

            selic_url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/1"
            selic_response = requests.get(selic_url, timeout=10)
            
            ipca_url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1"
            ipca_response = requests.get(ipca_url, timeout=10)
            
            interest_rate = 8.5
            if selic_response.status_code == 200:
                selic_data = selic_response.json()
                if selic_data and len(selic_data) > 0:
                    interest_rate = float(selic_data[0].get('valor', 8.5))
            
            inflation = 4.2
            if ipca_response.status_code == 200:
                ipca_data = ipca_response.json()
                if ipca_data and len(ipca_data) > 0:
                    inflation = float(ipca_data[0].get('valor', 4.2))
            
            return {
                'success': True,
                'data': {
                    'interest_rate': interest_rate,
                    'inflation': inflation,

                    'currency': 'BRL',
                    'last_updated': datetime.utcnow().isoformat(),
                    'source': 'Banco Central do Brasil'
                }
            }
            
        except Exception as e:
            raise ExternalServiceError(f'Banco Central error: {str(e)}')
