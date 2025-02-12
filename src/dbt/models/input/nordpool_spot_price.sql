WITH NordPoolSpotPrice AS (
    SELECT 
        delivery_start,
        delivery_end,
        price_area,
        price, 
        filename,
        ROW_NUMBER() OVER (PARTITION BY delivery_start, price_area ORDER BY delivery_start) as row_num
    FROM read_parquet({{ source('blob_storage', 'nordpool_spot_price') }},filename = true)
),

SpotPrice AS (
    SELECT 
        delivery_start,
        delivery_end,
        price_area,
        price, 
        filename
    FROM NordPoolSpotPrice
    WHERE row_num = 1
)

SELECT * FROM SpotPrice