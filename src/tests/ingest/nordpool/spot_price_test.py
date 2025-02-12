from src.ingest.nordpool.spot_price import process_nordpool_spot_price
from freezegun import freeze_time
from unittest.mock import patch, MagicMock
from datetime import datetime

@freeze_time("2021-01-01")
def test_process_nordpool_spot_price() -> None:
    """Test test_process_nordpool_spot_price"""
    with (
        patch("src.ingest.nordpool.spot_price.NordPool") as mock_nordpool,
        patch("src.ingest.nordpool.spot_price.store_object") as mock_store_object,
    ):
        nordpool_mock = MagicMock()
        mock_nordpool.return_value = nordpool_mock

        nordpool_mock.get_day_ahead_prices.return_value = {
            "multiAreaEntries": [
                {
                    "deliveryStart": datetime.now(),
                    "deliveryEnd": datetime.now(),
                    "entryPerArea": {"SE1": 10.0, "SE2": 20.0},
                }
            ]
        }
        
        process_nordpool_spot_price()
    
    nordpool_mock.authenticate.assert_called_once()
    nordpool_mock.get_day_ahead_prices.assert_called_once()
    nordpool_mock.get_day_ahead_prices.assert_called_with(date=datetime.now())
    
    mock_store_object.assert_called_once()
    mock_store_object.assert_called_with(
        data=[
            {"delivery_start": datetime.now(), "delivery_end": datetime.now(), "price_area": "SE1", "price": 10.0},
            {"delivery_start": datetime.now(), "delivery_end": datetime.now(), "price_area": "SE2", "price": 20.0},
        ],
        table_name="nordpool_spot_price",
        date=datetime.now(),
    )

