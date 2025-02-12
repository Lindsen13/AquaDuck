from src.ingest.fixer.exchange_rate import process_fixer_exchange_rate
from freezegun import freeze_time
from unittest.mock import patch, MagicMock
from datetime import datetime

@freeze_time("2021-01-01")
def test_process_fixer_exchange_rate() -> None:
    """Test process_fixer_exchange_rate"""
    with (
        patch("src.ingest.fixer.exchange_rate.Fixer") as mock_fixer,
        patch("src.ingest.fixer.exchange_rate.store_object") as mock_store_object,
    ):
        fixer_mock = MagicMock()
        mock_fixer.return_value = fixer_mock

        fixer_mock.get_exchange_rates.return_value = {
            "base": "USD",
            "date": datetime.now(),
            "rates": {"USD": 1.0, "EUR": 0.8},
        }
        
        process_fixer_exchange_rate()
    
    fixer_mock.authenticate.assert_called_once()
    fixer_mock.get_exchange_rates.assert_called_once()
    fixer_mock.get_exchange_rates.assert_called_with(date=datetime.now())
    
    mock_store_object.assert_called_once()
    mock_store_object.assert_called_with(
        data=[
            {"base": "USD", "date": datetime.now(), "symbol": "USD", "rate": 1.0},
            {"base": "USD", "date": datetime.now(), "symbol": "EUR", "rate": 0.8},
        ],
        table_name="fixer_exchange_rate",
        date=datetime.now(),
    )

