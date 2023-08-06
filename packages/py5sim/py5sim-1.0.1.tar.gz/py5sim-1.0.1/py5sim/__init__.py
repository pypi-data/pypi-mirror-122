from user import User
from sms import SMS
from guest import Guest

class py5sim:
    def __init__(self, sms_key: str="", user_key: str=""):
        self.sms = SMS(sms_key)
        self.user = User(user_key)
        self.guest = Guest()
 
if __name__ == '__main__':
    sms = "Your API key API1 protocol (Deprecated API) from https://5sim.net/settings/security"
    user = "Your API key 5sim protocol from https://5sim.net/settings/security"
    sim_api = py5sim(sms_key=sms, user_key=user)
    sim_api.user.profile()
    sim_api.user.crypto.rates('RUB')
    sim_api.user.vendor.stats()
    
    sim_api.sms.getBalance()
    sim_api.guest.prices()

    
    