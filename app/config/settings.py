
import os
from typing import Optional

class Settings:
    
    def __init__(self):

        self.aws_region = os.getenv('AWS_REGION', 'us-east-1')
        self.aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        
        self.use_dynamodb = os.getenv('USE_DYNAMODB', 'false').lower() == 'true'
        self.dynamodb_endpoint = os.getenv('DYNAMODB_ENDPOINT')
        
        self.jwt_secret = os.getenv('JWT_SECRET', 'liquid-secret-key')
        self.jwt_expiry = int(os.getenv('JWT_EXPIRY', '3600'))
        
        self.viacep_enabled = os.getenv('VIACEP_ENABLED', 'true').lower() == 'true'
        self.banco_central_enabled = os.getenv('BANCO_CENTRAL_ENABLED', 'true').lower() == 'true'
        self.weather_enabled = os.getenv('WEATHER_ENABLED', 'true').lower() == 'true'
        self.weather_api_key = os.getenv('WEATHER_API_KEY')
        
        self.cache_ttl = int(os.getenv('CACHE_TTL', '3600'))
        
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
