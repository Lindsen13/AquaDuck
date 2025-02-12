from src.utils.clients.nordpool import NordPool
import requests
import responses
from freezegun import freeze_time
from datetime import datetime
import pytest

def test_initiate_nordpool() -> None:
    """Test initiate Nordpool class"""
    nordpool = NordPool()
    assert nordpool.session is not None
    assert isinstance(nordpool.session, requests.Session)


def test_authenticate() -> None:
    """Test authenticate method"""
    nordpool = NordPool()
    nordpool.authenticate()
    assert nordpool

@responses.activate
@freeze_time("2025-05-01")
def test_get_exchange_rates() -> None:
    """Test get_day_ahead_prices method"""
    delivery_area = "EE,LT,LV,AT,BE,FR,GER,NL,PL,DK1,DK2,FI,NO1,NO2,NO3,NO4,NO5,SE1,SE2,SE3,SE4,TEL,SYS"

    responses.add(
        responses.GET,
        f'https://dataportal-api.nordpoolgroup.com/api/DayAheadPrices?date=2025-05-01&market=DayAhead&deliveryArea={delivery_area}&currency=EUR',
        json={},
        status=200,
    )
    nordpool = NordPool()
    nordpool.authenticate()
    data = nordpool.get_day_ahead_prices()
    assert data == {}
    assert len(responses.calls) == 1

@responses.activate
def test_get_exchange_rates_with_date() -> None:
    """Test get_exchange_rates method with a date"""
    delivery_area = "EE,LT,LV,AT,BE,FR,GER,NL,PL,DK1,DK2,FI,NO1,NO2,NO3,NO4,NO5,SE1,SE2,SE3,SE4,TEL,SYS"

    date = datetime(2024, 5, 1)
    responses.add(
        responses.GET,
        f'https://dataportal-api.nordpoolgroup.com/api/DayAheadPrices?date={date.strftime("%Y-%m-%d")}&market=DayAhead&deliveryArea={delivery_area}&currency=EUR',
        json={},
        status=200,
    )
    nordpool = NordPool()
    nordpool.authenticate()
    data = nordpool.get_day_ahead_prices(date=date)
    assert data == {}
    assert len(responses.calls) == 1

@responses.activate
@freeze_time("2025-05-01")
def test_get_exchange_rates_api_error() -> None:
    """Test get_exchange_rates method while receiving an API error"""
    delivery_area = "EE,LT,LV,AT,BE,FR,GER,NL,PL,DK1,DK2,FI,NO1,NO2,NO3,NO4,NO5,SE1,SE2,SE3,SE4,TEL,SYS"

    responses.add(
        responses.GET,
        f'https://dataportal-api.nordpoolgroup.com/api/DayAheadPrices?date=2025-05-01&market=DayAhead&deliveryArea={delivery_area}&currency=EUR',
        json={},
        status=400,
    )
    nordpool = NordPool()
    nordpool.authenticate()
    with pytest.raises(requests.exceptions.HTTPError):
        nordpool.get_day_ahead_prices()