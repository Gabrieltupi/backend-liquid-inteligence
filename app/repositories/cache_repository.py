
from typing import Dict, Any, Optional
from app.repositories.base_repository import BaseRepository

class CacheRepository(BaseRepository):
    
    def __init__(self):
        super().__init__()
        self.table_name = "liquid-cache"
        self.cache = {}
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        
        try:

            return self.cache.get(key)
            
        except Exception as e:
            print(f"Error getting cache: {e}")
            return None
    
    def set(self, key: str, value: Dict[str, Any], ttl: int = 3600) -> bool:
        
        try:

            self.cache[key] = value
            return True
            
        except Exception as e:
            print(f"Error setting cache: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        
        try:

            if key in self.cache:
                del self.cache[key]
            return True
            
        except Exception as e:
            print(f"Error deleting cache: {e}")
            return False
