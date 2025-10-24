
import uuid
import json
import os
from typing import Dict, Any, Optional
from app.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository):
    
    def __init__(self):
        super().__init__()
        self.table_name = "liquid-users"

        self.storage_file = "/tmp/liquid_users.json"
        self._users = self._load_users()
    
    def _load_users(self) -> Dict[str, Dict[str, Any]]:
        
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading users: {e}")
            return {}
    
    def _save_users(self):
        
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(self._users, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving users: {e}")
    
    def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        
        try:

            print(f"Buscando usuário por email: {email}")
            print(f"Usuários armazenados: {list(self._users.keys())}")
            
            return self._users.get(email)
            
        except Exception as e:
            print(f"Error finding user by email: {e}")
            return None
    
    def find_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        
        try:

            print(f"Buscando usuário por ID: {user_id}")
            print(f"Usuários armazenados: {list(self._users.keys())}")
            
            for email, user_data in self._users.items():
                if user_data.get('id') == user_id:
                    return user_data
            
            return None
            
        except Exception as e:
            print(f"Error finding user by ID: {e}")
            return None
    
    def create(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        
        try:

            user_id = str(uuid.uuid4())
            
            user_data['id'] = user_id
            
            print(f"Criando usuário: {user_data['email']}")
            self._users[user_data['email']] = user_data
            self._save_users()
            print(f"Usuário salvo. Total de usuários: {len(self._users)}")

            return user_data
            
        except Exception as e:
            print(f"Error creating user: {e}")
            raise
