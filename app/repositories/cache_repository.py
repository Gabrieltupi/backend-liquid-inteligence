
import time
from typing import Dict, Any, Optional
from app.repositories.base_repository import BaseRepository
from botocore.exceptions import ClientError

class CacheRepository(BaseRepository):
    
    def __init__(self):
        super().__init__()
        self.table_name = "liquid-cache"
        self.table = self._get_table()
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Busca item no cache DynamoDB"""
        try:
            
            if not self.table:
                return None
            
            response = self.table.get_item(
                Key={'key': key}
            )
            
            if 'Item' in response:
                item = response['Item']
                
                ttl = item.get('ttl', 0)
                if ttl > 0 and time.time() > ttl:
                    self.delete(key)
                    return None
                
                return item.get('value')
            else:
                return None
                
        except ClientError as e:
            return None
        except Exception as e:
            return None
    
    def set(self, key: str, value: Dict[str, Any], ttl: int = 3600) -> bool:
        """Salva item no cache DynamoDB"""
        try:
            
            if not self.table:
                return False
            
            ttl_timestamp = int(time.time()) + ttl
            
            self.table.put_item(
                Item={
                    'key': key,
                    'value': value,
                    'ttl': ttl_timestamp
                }
            )
            
            return True
            
        except ClientError as e:
            return False
        except Exception as e:
            return False
    
    def delete(self, key: str) -> bool:
        """Remove item do cache DynamoDB"""
        try:
            
            if not self.table:
                return False
            
            self.table.delete_item(
                Key={'key': key}
            )
            
            return True
            
        except ClientError as e:
            return False
        except Exception as e:
            return False
