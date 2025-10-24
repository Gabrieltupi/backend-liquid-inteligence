
import boto3
from typing import Optional
from app.config.settings import Settings

class DatabaseConfig:
    
    def __init__(self):
        self.settings = Settings()
        self.dynamodb = None
        self._init_dynamodb()
    
    def _init_dynamodb(self):
        
        try:
            if self.settings.use_dynamodb:
                self.dynamodb = boto3.resource(
                    'dynamodb',
                    region_name=self.settings.aws_region,
                    aws_access_key_id=self.settings.aws_access_key,
                    aws_secret_access_key=self.settings.aws_secret_key,
                    endpoint_url=self.settings.dynamodb_endpoint
                )
        except Exception as e:
            print(f"Error initializing DynamoDB: {e}")
            self.dynamodb = None
    
    def get_table(self, table_name: str):
        
        if not self.dynamodb:
            return None
        
        try:
            return self.dynamodb.Table(table_name)
        except Exception as e:
            print(f"Error getting table {table_name}: {e}")
            return None
