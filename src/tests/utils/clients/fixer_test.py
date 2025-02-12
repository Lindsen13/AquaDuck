from src.utils.clients.fixer import Fixer
from unittest.mock import patch
import requests
import responses
from freezegun import freeze_time
from datetime import datetime
import pytest

def test_initiate_fixer() -> None:
    """Test initiate Fixer class"""
    fixer = Fixer()
    assert fixer.session is not None
    assert isinstance(fixer.session, requests.Session)


def test_authenticate() -> None:
    """Test authenticate method"""
    fixer = Fixer()
    with patch("src.utils.clients.fixer.os.getenv", return_value="123"):
        fixer.authenticate()
    assert fixer.api_key is not None

@responses.activate
@freeze_time("2025-05-01")
def test_get_exchange_rates() -> None:
    """Test get_exchange_rates method"""
    responses.add(
        responses.GET,
        "https://data.fixer.io/api/2025-05-01?access_key=123&base=EUR&symbols=USD",
        json={},
        status=200,
    )
    with (
        patch("src.utils.clients.fixer.os.getenv", return_value="123"),
        patch("src.utils.clients.fixer.SYMBOLS", ["USD"]),
        ):
        fixer = Fixer()
        fixer.authenticate()
        data = fixer.get_exchange_rates()
    assert data == {}
    assert len(responses.calls) == 1

@responses.activate
def test_get_exchange_rates_with_date() -> None:
    """Test get_exchange_rates method with a date"""
    date = datetime(2025, 5, 1)
    responses.add(
        responses.GET,
        f'https://data.fixer.io/api/{date.strftime("%Y-%m-%d")}?access_key=123&base=EUR&symbols=USD',
        json={},
        status=200,
    )
    with (
        patch("src.utils.clients.fixer.os.getenv", return_value="123"),
        patch("src.utils.clients.fixer.SYMBOLS", ["USD"]),
        ):
        fixer = Fixer()
        fixer.authenticate()
        data = fixer.get_exchange_rates(date=date)
    
    assert data == {}
    assert len(responses.calls) == 1

@responses.activate
@freeze_time("2025-05-01")
def test_get_exchange_rates_api_error() -> None:
    """Test get_exchange_rates method while receiving an API error"""
    responses.add(
        responses.GET,
        "https://data.fixer.io/api/2025-05-01?access_key=123&base=EUR&symbols=USD",
        json={},
        status=400,
    )
    with (
        patch("src.utils.clients.fixer.os.getenv", return_value="123"),
        patch("src.utils.clients.fixer.SYMBOLS", ["USD"]),
        ):
        fixer = Fixer()
        fixer.authenticate()
        with pytest.raises(requests.exceptions.HTTPError):
            fixer.get_exchange_rates()
