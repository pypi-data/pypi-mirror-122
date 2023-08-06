from requests import Session
from simplejson.errors import JSONDecodeError
from simtypes import SimResponse, ApiKeyError, AuthorizationError

def response_decorator(func):
    def wrapper(*args, **kwargs):
        r = func(*args, **kwargs)
        if type(r) == dict:
            return SimResponse(r)
        return r
    return wrapper

def control_access_sms(func):
    def controller(*args, **kwargs):
        if args[0]._reqBase__session.params['api_key']:
            r = func(*args, **kwargs)
            if type(r) == dict:
                return SimResponse(r)
            return r
        else:
            raise ApiKeyError('Call method with sms api key (https://5sim.net/settings/security API key API 1 protocol)')
    return controller

def control_access_user(func):
    def controller(*args, **kwargs):
        if args[0]._reqBase__session.headers['Authorization'] != 'Bearer ':
            r = func(*args, **kwargs)
            if type(r) == dict:
                return SimResponse(r)
            return r
        else:
            raise ApiKeyError('Call method with user api key (https://5sim.net/settings/security API key 5sim protocol)')
    return controller


class reqBase:
    def __init__(self, respClass):
        self.__session = Session()
        self.respClass = respClass
    
    def call(self, 
             url: str, 
             return_text: str=None, 
             use_data=False, 
             custom_method='GET',
             **kwargs) -> dict:
        
        
        
        if use_data: 
            data = kwargs
            params = None
        else:
            data = None
            params = kwargs
            
        r = self.__session.request(custom_method.upper(), url=url, data=data, params=params)
        
        if self.__class__.__name__ == 'User':
            if r.status_code == 401:
                raise AuthorizationError('user_api_key is invalid')
        
        if return_text == True:
            return r.text
        return self.respClass(r.json())
