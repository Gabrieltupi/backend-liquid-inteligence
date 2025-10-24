
import uuid
import boto3
from typing import Dict, Any, Optional
from app.repositories.base_repository import BaseRepository
from botocore.exceptions import ClientError

class UserRepository(BaseRepository):
    
    def __init__(self):
        super().__init__()
        self.table_name = "liquid-users"
        self.table = self._get_table()
    
    def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Busca usuário por email usando DynamoDB"""
        try:
            
            if not self.table:
                return None
            
            response = self.table.scan(
                FilterExpression='email = :email',
                ExpressionAttributeValues={':email': email}
            )
            
            if response['Items']:
                user = response['Items'][0]
                return user
            else:
                return None
                
        except ClientError as e:
            return None
        except Exception as e:
            return None
    
    def find_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Busca usuário por ID usando DynamoDB"""
        try:
            
            if not self.table:
                return None
            
            response = self.table.get_item(
                Key={'id': user_id}
            )
            
            if 'Item' in response:
                user = response['Item']
                return user
            else:
                return None
                
        except ClientError as e:
            return None
        except Exception as e:
            return None
    
    def create(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria usuário no DynamoDB"""
        try:
            user_id = str(uuid.uuid4())
            user_data['id'] = user_id
            
            
            if not self.table:
                raise Exception("DynamoDB table not available")
            
            self.table.put_item(Item=user_data)
            
            return user_data
            
        except ClientError as e:
            raise
        except Exception as e:
            raise
