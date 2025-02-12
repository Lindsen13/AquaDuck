import requests
from datetime import datetime

class NordPool:
    """Class to interact with the NordPool API"""

    def __init__(self):
        self.base_url = "https://dataportal-api.nordpoolgroup.com/api"
        self.session = requests.Session()
    
    def authenticate(self)-> None:
        """Authenticate - Not needed for NordPool"""
        pass

    def get_day_ahead_prices(self, date:datetime | None = None)-> dict:
        """Get day ahead prices from NordPool API"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        else:
            date = date.strftime("%Y-%m-%d")
        delivery_area = "EE,LT,LV,AT,BE,FR,GER,NL,PL,DK1,DK2,FI,NO1,NO2,NO3,NO4,NO5,SE1,SE2,SE3,SE4,TEL,SYS"
        url = f"{self.base_url}/DayAheadPrices?date={date}&market=DayAhead&deliveryArea={delivery_area}&currency=EUR"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
if __name__ == "__main__":
    nordpool = NordPool()
    nordpool.authenticate()
    data = nordpool.get_day_ahead_prices()
    print(data)