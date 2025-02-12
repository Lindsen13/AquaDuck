WITH FixerExchangeRate AS (
    SELECT 
        base,
        date,
        symbol,
        rate, 
        filename,
        ROW_NUMBER() OVER (PARTITION BY base, date, symbol ORDER BY base) as row_num
    FROM read_parquet({{ source('blob_storage', 'fixer_exchange_rate') }},filename = true)
),

ExchangeRate AS (
    SELECT 
        base,
        date,
        symbol,
        rate, 
        filename
    FROM FixerExchangeRate
    WHERE row_num = 1
)

SELECT * FROM ExchangeRate