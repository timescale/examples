/* This file contains 5 different ways to explore the dataset */


/* 
Query1: How <ticker> price changed over time? 
Change the symbol and the time_bucket interval for further exploration about prices.
*/
SELECT
    time_bucket('7 days', stock_datetime) AS time_frame,
    last(price_close, stock_datetime) AS last_closing_price
FROM stocks_new
WHERE symbol = 'AAPL'
GROUP BY time_frame
ORDER BY time_frame

/*
Query2: How <ticker> trading volume changed over time?
Change the symbol and the time_bucket interval for further exploration about volumes.
*/
SELECT time_bucket('7 days', stock_datetime) AS time_frame, sum(trading_volume) AS volume
FROM stocks_new
WHERE symbol = 'AAPL'
GROUP BY time_frame
ORDER BY time_frame

/*
Query3: Which tickers had the most transaction volume in the past 14 days?
Change the time interval for further exploration about volumes.
*/
SELECT symbol, sum(trading_volume) AS volume
FROM stocks_new
WHERE (now() - date(stock_datetime)) < INTERVAL '14 day'
GROUP BY symbol
ORDER BY volume DESC
LIMIT 5

/*
Query4: FAANG prices over time
Change the time_bucket interval for further exploration about FAANG tickers.
*/
SELECT symbol, time_bucket('30 days', stock_datetime) AS time_frame, last(price_close, stock_datetime) AS last_closing_price
FROM stocks_new
WHERE symbol in ('AAPL', 'FB', 'AMZN', 'NFLX', 'GOOG')
GROUP BY time_frame, symbol
ORDER BY time_frame

/*
Query5: Which symbols had the biggest daily gain/loss?
Change the time_bucket interval and ORDER DESC/ASC for further exploration about price changes.
*/
SELECT symbol, time_frame, max((closing_price-opening_price)/closing_price*100) AS price_change_pct
FROM ( 
    SELECT 
    symbol, 
    time_bucket('1 day', stock_datetime) AS time_frame, 
    first(price_open, stock_datetime) AS opening_price, 
    last(price_close, stock_datetime) AS closing_price
    FROM stocks_new
    GROUP BY time_frame, symbol
) s
GROUP BY symbol, s.time_frame
ORDER BY price_change_pct DESC
LIMIT 5