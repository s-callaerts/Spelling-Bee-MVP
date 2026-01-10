class BaseSchema:  
    REQUIRED_FIELDS = set()

    @classmethod
    def validate(cls, payload: dict) -> dict:

        if not isinstance(payload, dict):
            raise ValueError('Invalid JSON load')
        
        missing = cls.REQUIRED_FIELDS - payload.keys()

        if missing:
            raise ValueError(f'Missing fields: {', '.join(missing)}')
            
        return {field: payload[field] for field in cls.REQUIRED_FIELDS}
    
class RegistrationSchema(BaseSchema):
    REQUIRED_FIELDS = {'name', 'email', 'password', 'grade'}

class LoginSchema(BaseSchema):
    REQUIRED_FIELDS = {'name', 'password'}

class SecurityError(Exception):
    pass