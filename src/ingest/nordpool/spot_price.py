from datetime import datetime

from src.utils.clients.nordpool import NordPool
from src.utils.storage import store_object


def process_nordpool_spot_price(date: datetime | None = None) -> None:
    """Process NordPool spot price data"""
    if not date:
        date = datetime.now()

    nordpool = NordPool()
    nordpool.authenticate()
    data = nordpool.get_day_ahead_prices(date=date)
    output = []
    for entry in data["multiAreaEntries"]:
        for price_area, price in entry["entryPerArea"].items():
            output.append(
                {
                    "delivery_start": entry["deliveryStart"],
                    "delivery_end": entry["deliveryEnd"],
                    "price_area": price_area,
                    "price": price,
                }
            )
    store_object(data=output, table_name="nordpool_spot_price", date=date)


if __name__ == "__main__":
    start = datetime.now()
    process_nordpool_spot_price()
    print(f"Nordpool Spot Prices: {datetime.now() - start}")
