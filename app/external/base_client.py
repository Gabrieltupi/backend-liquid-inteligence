
import requests
import time
from typing import Dict, Any

class BaseClient:
    
    def __init__(self):
        self.session = requests.Session()
        self.max_retries = 3
        self.retry_delay = 1
    
    def make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.request(method, url, **kwargs)
                return response
            except requests.exceptions.RequestException as e:
                if attempt == self.max_retries - 1:
                    raise e
                time.sleep(self.retry_delay * (2 ** attempt))
        
        raise Exception("Max retries exceeded")
    
    def handle_response(self, response: requests.Response) -> Dict[str, Any]:
        
        try:
            if response.status_code == 200:
                return {
                    'success': True,
                    'data': response.json()
                }
            else:
                return {
                    'success': False,
                    'error': f'HTTP {response.status_code}'
                }
        except Exception as e:
            return {
                'success': False,
                'error': f'Response error: {str(e)}'
            }
