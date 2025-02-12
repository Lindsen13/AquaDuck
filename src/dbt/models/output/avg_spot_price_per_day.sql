WITH SpotPrice AS (
    SELECT 
        delivery_start,
        delivery_end,
        country,
        price
    FROM {{ ref('spot_price') }}
),

ExchangeRate AS (
    SELECT 
        base,
        date,
        symbol,
        rate
    FROM {{ ref('exchange_rate') }}
    WHERE symbol = 'USD'
),

AvgSpotPricePerDay AS (
    SELECT 
        delivery_start::date AS delivery_date,
        country,
        AVG(price) AS avg_price,
        RANK() OVER (PARTITION BY delivery_start::date ORDER BY AVG(price) DESC) AS rank
    FROM SpotPrice
    GROUP BY delivery_start::date, country
),

Final AS (
    SELECT 
        sp.delivery_date AS date,
        sp.country,
        sp.avg_price AS avg_price_eur,
        sp.avg_price * er.rate AS avg_price_usd,
        sp.rank
    FROM AvgSpotPricePerDay sp
    JOIN ExchangeRate er
    ON sp.delivery_date = er.date
)

SELECT * FROM Final