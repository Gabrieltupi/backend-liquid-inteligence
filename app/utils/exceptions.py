
class LiquidException(Exception):
    
    pass

class ValidationError(LiquidException):
    
    pass

class AuthenticationError(LiquidException):
    
    pass

class AuthorizationError(LiquidException):
    
    pass

class ExternalServiceError(LiquidException):
    
    pass

class DatabaseError(LiquidException):
    
    pass

class CacheError(LiquidException):
    
    pass
