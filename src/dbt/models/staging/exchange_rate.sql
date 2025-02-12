WITH ExchangeRate AS (
    SELECT 
        base,
        date,
        symbol,
        rate
    FROM {{ ref('fixer_exchange_rate') }}
)

SELECT * FROM ExchangeRate