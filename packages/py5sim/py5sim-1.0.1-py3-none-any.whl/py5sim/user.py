from simtypes import UserResponse
from simfuncs import reqBase, control_access_user
   
class User(reqBase):
    def __init__(self, api_key: str):
        self.api_key = api_key
        super(self.__class__, self).__init__(UserResponse)
        self._reqBase__session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Accept': 'application/json'
        })
        self.url = "https://5sim.net/v1/user"
        
        self.crypto = Crypto(api_key)
        self.vendor = Vendor(api_key)

    @control_access_user
    def profile(self):
        return self.call(f"{self.url}/profile")

    @control_access_user
    def orders(self, 
               category: str, 
               limit: str="", 
               offset: str="", 
               order: str="", 
               reverse: bool="") -> dict:
        
        return self.call(
            f"{self.url}/orders", 
            category=category,
            limit=limit,
            offset=offset,
            order=order,
            reverse=str(reverse).lower()
        )
    
    @control_access_user
    def payments(self, 
                 limit: str="", 
                 offset: str="", 
                 order: str="", 
                 reverse: bool="") -> dict:
        
        return self.call(
            f"{self.url}/payments",
            limit=limit,
            offset=offset,
            order=order,
            reverse=str(reverse).lower()
        )
    
    
    # SMS user api
    @control_access_user
    def buy_activation(self, 
            country: str, 
            operator: str, 
            product: str, 
            forwarding: str="", 
            number: str="",
            reuse: str="",
            voice: str="",
            ref: str="") -> dict:
         
        return self.call(
            f"{self.url}/buy/activation/{country}/{operator}/{product}",
            forwarding=forwarding,
            number=number,
            reuse=reuse,
            voice=voice,
            ref=ref
        )
        
    @control_access_user
    def buy_hosting(self, 
            country: str, 
            operator: str, 
            product: str) -> dict:
        
        return self.call(
            f"{self.url}/buy/hosting/{country}/{operator}/{product}",
        )
        
    @control_access_user
    def buy_reuse(self, 
            product: str, 
            number: int) -> dict:
        
        return self.call(
            f"{self.url}/buy/reuse/{product}/{number}",
        )
  
    @control_access_user
    def check(self, 
            id: int) -> dict:
        
        return self.call(
            f"{self.url}/check/{id}",
        )
    
    @control_access_user
    def finish(self, 
            id: int) -> dict:
        
        return self.call(
            f"{self.url}/finish/{id}",
        )
    
    @control_access_user
    def cancel(self, 
            id: int) -> dict:
        
        return self.call(
            f"{self.url}/cancel/{id}",
        )
        
    @control_access_user
    def inbox(self, 
            id: int) -> dict:
        
        return self.call(
            f"{self.url}/sms/inbox/{id}",
        )
    
    # Notifications
    @control_access_user
    def inbox(self, 
            lang: str='en') -> dict:
        
        return self.call(
            f"{self.url.replace('user', 'guest')}/flash/{lang}",
        )
        
    # Countries
    @control_access_user
    def countries(self) -> dict:
        return self.call(
            f"{self.url.replace('user', 'guest')}/countries",
        )
        
class Crypto(reqBase):
    def __init__(self, api_key: str):
        self.api_key = api_key
        super(self.__class__, self).__init__(UserResponse)
        self._reqBase__session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Accept': 'application/json'
        })
        self.url = "https://5sim.net/v1/user"
    
    @control_access_user
    def rates(self,
            currency: int) -> dict:
        
        return self.call(
            f"{self.url}/payment/crypto/rates", 
            currency=currency
        )
        
    @control_access_user
    def getaddress(self,
            currency: int) -> dict:
        
        return self.call(
            f"{self.url}/payment/crypto/getaddress", 
            currency=currency
        )

class Vendor(reqBase):
    def __init__(self, api_key: str):
        self.api_key = api_key
        super(self.__class__, self).__init__(UserResponse)
        self._reqBase__session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Accept': 'application/json'
        })
        self.url = "https://5sim.net/v1/user"
    
    @control_access_user
    def stats(self) -> dict:
        return self.call(
            f"{self.url}/vendor",
        )
    
    @control_access_user
    def wallets(self) -> dict:
        return self.call(
            f"{self.url}/wallets",
        )
    
    @control_access_user
    def orders(self,
               category: str,
               limit: int="",
               offset: int="",
               order: str="",
               reverse: bool="") -> dict:
        
        return self.call(
            f"{self.url}/orders", 
            category=category,
            limit=limit,
            offset=offset,
            order=order,
            reverse=str(reverse).lower()
        )
        
    @control_access_user
    def payments(self,
                 limit: int="",
                 offset: int="",
                 order: str="",
                 reverse: bool="") -> dict:
        
        return self.call(
            f"{self.url}/payments",
            limit=limit,
            offset=offset,
            order=order,
            reverse=str(reverse).lower()
        )

    @control_access_user
    def withdraw(self,
                 receiver: str,     # Получатель
                 method: str,       # Способ вывода visa/qiwi/yandex
                 amount: int,       # Сумма
                 fee: str) -> dict: # Платежная система fkwallet/payeer/unitpay
        
        return self.call(
            f"{self.url}/withdraw",
            use_data=True,
            custom_method='POST',
            receiver=receiver,
            method=method,
            amount=amount,
            fee=fee
        )
