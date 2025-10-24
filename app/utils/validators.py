
import re
from typing import Any

def validate_email(email: str) -> bool:
    
    if not email or not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> bool:
    
    if not password or not isinstance(password, str):
        return False
    
    return len(password) >= 8

def validate_location_input(location: str) -> bool:
    
    if not location or not isinstance(location, str):
        return False
    
    location = location.strip()
    
    if not location:
        return False
    
    if len(location) < 2 or len(location) > 200:
        return False
    
    return True

def validate_cep(cep: str) -> bool:
    
    if not cep or not isinstance(cep, str):
        return False
    
    cep_clean = re.sub(r'[^0-9]', '', cep)
    
    return len(cep_clean) == 8

def sanitize_input(input_value: Any) -> str:
    
    if not input_value:
        return ""
    
    sanitized = str(input_value)
    
    sanitized = re.sub(r'[<>"\']', '', sanitized)
    
    return sanitized[:200]
