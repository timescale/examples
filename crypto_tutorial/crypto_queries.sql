-- crypto_queries.sql
-- A set of questions and queries to run on a cryptocurrency market dataset
-- Author: Avthar Sewrathan
-- Timescale Inc
-- 16 September 2019

--Query 1
-- How did Bitcoin price in USD vary over time?
-- BTC 7 day prices
SELECT time_bucket('7 days', time) as period,
       last(closing_price, time) AS last_closing_price
FROM btc_prices
WHERE currency_code = 'USD'
GROUP BY period
ORDER BY period

--Query 2
-- How did BTC daily returns vary over time?
-- Which days had the worst and best returns?
-- BTC daily return
SELECT time,
       closing_price / lead(closing_price) over prices AS daily_factor
FROM (
   SELECT time,
          closing_price
   FROM btc_prices
   WHERE currency_code = 'USD'
   GROUP BY 1,2
) sub window prices AS (ORDER BY time DESC)

--Query 3
-- How did the trading volume of Bitcoin vary over time in different fiat currencies?
-- BTC volume in different fiat in 7 day intervals
SELECT time_bucket('7 days', time) as period,
       currency_code,
       sum(volume_btc)
FROM btc_prices
GROUP BY currency_code, period
ORDER BY period

-- Q4
-- How did Ethereum (ETH) price in BTC vary over time?
-- ETH prices in BTC in 7 day intervals
SELECT 
    time_bucket('7 days', time) AS time_period, 
    last(closing_price, time) AS closing_price_btc
FROM crypto_prices
WHERE currency_code='ETH' 
GROUP BY time_period
ORDER BY time_period

--Q5
-- How did ETH prices, in different fiat currencies, vary over time?
-- (using the BTC/Fiat exchange rate at the time)
-- ETH prices in fiat
SELECT time_bucket('7 days', c.time) AS time_period,
       last(c.closing_price, c.time) AS last_closing_price_in_btc,
       last(c.closing_price, c.time) * last(b.closing_price, c.time) FILTER (WHERE b.currency_code = 'USD') AS last_closing_price_in_usd,
       last(c.closing_price, c.time) * last(b.closing_price, c.time) FILTER (WHERE b.currency_code = 'EUR') AS last_closing_price_in_eur,
       last(c.closing_price, c.time) * last(b.closing_price, c.time) FILTER (WHERE b.currency_code = 'CNY') AS last_closing_price_in_cny,
       last(c.closing_price, c.time) * last(b.closing_price, c.time) FILTER (WHERE b.currency_code = 'JPY') AS last_closing_price_in_jpy,
       last(c.closing_price, c.time) * last(b.closing_price, c.time) FILTER (WHERE b.currency_code = 'KRW') AS last_closing_price_in_krw
FROM crypto_prices c 
JOIN btc_prices b 
    ON time_bucket('1 day', c.time) = time_bucket('1 day', b.time)
WHERE c.currency_code = 'ETH'
GROUP BY time_period
ORDER BY time_period

--Q6
-- Which are the newest cryptocurrencies?
-- Crypto by date of first data
SELECT ci.currency_code, min(c.time)
FROM currency_info ci JOIN crypto_prices c ON ci.currency_code = c.currency_code
AND c.closing_price > 0
GROUP BY ci.currency_code
ORDER BY min(c.time) DESC

--Q7
-- Number of new cryptocurrencies by day
-- Which days had the most new cryptocurrencies added?
SELECT day, COUNT(code)
FROM (
   SELECT min(c.time) AS day, ci.currency_code AS code
   FROM currency_info ci JOIN crypto_prices c ON ci.currency_code = c.currency_code
   AND c.closing_price > 0
   GROUP BY ci.currency_code
   ORDER BY min(c.time)
)a
GROUP BY day 
ORDER BY day DESC


--Q8
-- Which cryptocurrencies had the most transaction volume in the past 14 days?
-- Crypto transaction volume during a certain time period
SELECT 'BTC' as currency_code,
       sum(b.volume_currency) as total_volume_in_usd
FROM btc_prices b
WHERE b.currency_code = 'USD'
AND now() - date(b.time) < INTERVAL '14 day'
GROUP BY b.currency_code
UNION
SELECT c.currency_code as currency_code,
       sum(c.volume_btc) * avg(b.closing_price) as total_volume_in_usd
FROM crypto_prices c JOIN btc_prices b ON date(c.time) = date(b.time)
WHERE c.volume_btc > 0
AND b.currency_code = 'USD'
AND now() - date(b.time) < INTERVAL '14 day'
AND now() - date(c.time) < INTERVAL '14 day'
GROUP BY c.currency_code
ORDER BY total_volume_in_usd DESC

--Q9
-- Which cryptocurrencies had the top daily return?
-- Top crypto by daily return
WITH 
    prev_day_closing AS (
SELECT
    currency_code,
    time,
    closing_price,
    LEAD(closing_price) OVER (PARTITION BY currency_code ORDER BY TIME DESC) AS prev_day_closing_price
FROM
     crypto_prices   
)
,    daily_factor AS (
SELECT
    currency_code,
    time,
    CASE WHEN prev_day_closing_price = 0 THEN 0 ELSE closing_price/prev_day_closing_price END AS daily_factor
FROM
    prev_day_closing
)
SELECT
    time, 
    LAST(currency_code, daily_factor) as currency_code,
    MAX(daily_factor) as max_daily_factor
FROM
    daily_factor
GROUP BY
    TIME