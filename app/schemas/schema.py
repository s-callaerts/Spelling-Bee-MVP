class RegistrationSchema:  
    REQUIRED_FIELDS = {'name', 'email', 'password', 'grade'}

    @classmethod
    def validate(cls, payload: dict) -> dict:

        if not isinstance(payload, dict):
            raise ValueError('Invalid JSON load')
        
        missing = cls.REQUIRED_FIELDS - payload.keys()

        if missing:
            raise ValueError(f'Missing fields: {', '.join(missing)}')
            
        return {
            'name': payload['name'],
            'email': payload['email'],
            'password': payload['password'],
            'grade': payload['grade']
            }

class LoginSchema:
    REQUIRED_FIELDS = {'username', 'password'}

class SecurityError(Exception):
    pass