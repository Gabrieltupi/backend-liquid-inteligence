
import boto3
from typing import Dict, Any, Optional
from app.config.settings import Settings

class BaseRepository:
    
    def __init__(self):
        self.settings = Settings()
        self.dynamodb = None
        self.table_name = None
        
        if self.settings.use_dynamodb:
            self._init_dynamodb()
    
    def _init_dynamodb(self):
        
        try:
            self.dynamodb = boto3.resource(
                'dynamodb',
                region_name=self.settings.aws_region,
                aws_access_key_id=self.settings.aws_access_key,
                aws_secret_access_key=self.settings.aws_secret_key
            )
        except Exception as e:
            print(f"Error initializing DynamoDB: {e}")
            self.dynamodb = None
    
    def _get_table(self):
        
        if not self.dynamodb or not self.table_name:
            return None
        
        try:
            return self.dynamodb.Table(self.table_name)
        except Exception as e:
            print(f"Error getting table {self.table_name}: {e}")
            return None
