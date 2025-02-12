WITH SpotPrice AS (
    SELECT 
        delivery_start,
        delivery_end,
        price_area,
        CASE price_area
            WHEN 'AT' THEN 'Austria'
            WHEN 'BE' THEN 'Belgium'
            WHEN 'DK1' THEN 'Denmark'
            WHEN 'DK2' THEN 'Denmark'
            WHEN 'EE' THEN 'Estonia'
            WHEN 'FI' THEN 'Finland'
            WHEN 'FR' THEN 'France'
            WHEN 'GER' THEN 'Germany'
            WHEN 'LT' THEN 'Lithuania'
            WHEN 'LV' THEN 'Latvia'
            WHEN 'NL' THEN 'Netherlands'
            WHEN 'NO1' THEN 'Norway'
            WHEN 'NO2' THEN 'Norway'
            WHEN 'NO3' THEN 'Norway'
            WHEN 'NO4' THEN 'Norway'
            WHEN 'NO5' THEN 'Norway'
            WHEN 'PL' THEN 'Poland'
            WHEN 'SE1' THEN 'Sweden'
            WHEN 'SE2' THEN 'Sweden'
            WHEN 'SE3' THEN 'Sweden'
            WHEN 'SE4' THEN 'Sweden'
            WHEN 'SYS' THEN 'Denmark'
            WHEN 'TEL' THEN 'Romania'
        END AS country,
        price
    FROM {{ ref('nordpool_spot_price') }}
)

SELECT * FROM SpotPrice


/*
            
*/