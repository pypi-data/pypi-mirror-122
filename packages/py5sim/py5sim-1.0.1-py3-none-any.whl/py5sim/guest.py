from simtypes import GuestResponse
from simfuncs import reqBase

class Guest(reqBase):
    def __init__(self):
        super(self.__class__, self).__init__(GuestResponse)
        self._reqBase__session.headers.update({
            'Accept': 'application/json'
        })
        self.url = "https://5sim.net/v1/guest"
    
    # https://docs.5sim.net/#products-and-prices
    def products(self, country: str, operator: str) -> dict:
        return self.call(
            f"{self.url}/products/{country}/{operator}"
        )
    
    def prices(self, country: str = "", product: str = "") -> dict:
        return self.call(
            f"{self.url}/prices",
            country=country,
            product=product
        )
    