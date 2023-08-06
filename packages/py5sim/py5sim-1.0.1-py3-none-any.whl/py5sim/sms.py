from simtypes import SimResponse
from simfuncs import reqBase, response_decorator, control_access_sms

class SMS(reqBase):
    def __init__(self, api_key: str):
        self.api_key = api_key
        super(self.__class__, self).__init__(SimResponse)
        self._reqBase__session.params.update({
            'api_key': api_key
        })
        self.url = "http://api2.5sim.net/stubs/handler_api.php"
    
    @response_decorator
    @control_access_sms
    def getNumbers(self, country: str, service: str, count: int = 1) -> dict:
        r = self.call(
            self.url,
            return_text=True,
            action='getNumbers', 
            country=country, 
            service=service, 
            count=count
        )
        if 'ACCESS_NUMBER' in r:
            return {'id': r.split(':')[1], 'number': r.split(':')[2]}
        return r
    
    @response_decorator
    @control_access_sms
    def setStatus(self, id: int, status: int) -> str:
        return self.call(
            self.url,
            return_text=True,
            action='setStatus', 
            id=id, 
            status=status
        )
        
    @response_decorator
    @control_access_sms
    def getStatus(self, id: int) -> str:
        return self.call(
            self.url,
            return_text=True,
            action='getStatus', 
            id=id
        )
        
    @response_decorator
    @control_access_sms
    def getBalance(self) -> float:
        r = self.call(
            self.url,
            return_text=True,
            action='getBalance'
        )
        if 'ACCESS_BALANCE' in r:
            return float(r.split(':')[1])
        return r
    