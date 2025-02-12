from src.utils.clients.fixer import Fixer
from datetime import datetime
from src.utils.storage import store_object

def process_fixer_exchange_rate(date: datetime | None = None)-> None:
    """Process Fixer Exchange Rates data"""
    if not date:
        date = datetime.now()

    fixer = Fixer()
    fixer.authenticate()
    data = fixer.get_exchange_rates(date=date)
    output = []
    for symbol, rate in data["rates"].items():
        output.append(
            {
                "base": data["base"],
                "date": data["date"],
                "symbol": symbol,
                "rate": rate,
            }
        )
    store_object(data=output, table_name="fixer_exchange_rate", date=date)

if __name__ == "__main__":
    start = datetime.now()
    process_fixer_exchange_rate()
    print(f"Fixer Exchange Rate: {datetime.now() - start}")