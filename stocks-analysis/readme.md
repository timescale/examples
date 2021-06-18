# Historical stock data analysis

How to collect, store and analyze stock data with Python. This project will be built out in live Twitch streams on the 
[TimescaleDB Twitch channel](https://www.twitch.tv/timescaledb).


1. Collect stock ticker symbols

   Top 10 stocks based on US market capitalization. 
   Extracted [from the web](https://companiesmarketcap.com/usa/largest-companies-in-the-usa-by-market-cap/).
2. Collect historical stock data using Alpha Vantage's free API.

   Use [Alpha Vantage's API](https://www.alphavantage.co/documentation/) to fetch historical stock data.
3. Store data in TimescaleDB.
4. Analyze the dataset

   Data visualization to answer specific questions regarding the dataset.

## Prerequisites
* Python 3
* Virtualenv
* PostgreSQL database with TimescaleDB extension
* Alpha Vantage API key ([get one here](https://www.alphavantage.co/support/#api-key))

## Usage

1. Create a new virtual environment in root directory and activate it.
   
   ```bash
   virtualenv env
   source env/bin/activate
   ```

2. Install requirements.

   `pip install requirements.txt`

3. Create table in your PostgreSQL database.
   - with psql:

   `psql -f create_table.sql`
   
   - or with this SQL script:

      ```sql
      CREATE TABLE public.stocks2 (
         stock_datetime timestamp(0) NOT NULL,
         price_open float8 NULL,
         price_close float8 NULL,
         price_low float8 NULL,
         price_high float8 NULL,
         trading_volume int4 NULL,
         symbol varchar NULL
      );
      ```

4. Create a hypertable so we can use TimescaleDB features later on.
   - with psql: 

      `psql -f create_hypertable.sql`
   - or with this SQL script:
      ```sql
      CREATE EXTENSION IF NOT EXISTS timescaledb;
      SELECT create_hypertable('stocks2', 'stock_datetime');
      ```
5. Modify `config.py` according to your database connection details.
   ```python
   class StocksConfig(object):
      DB_USER = 'user'
      DB_PASS = 'passwd'
      DB_HOST = 'host'
      DB_PORT = 'port'
      DB_NAME = 'name'
      APIKEY = 'apikey'
   ```
   Also, `config.py` holds your Alpha Vantage API key, so make sure to edit that too.

6. Run stock_analyis.py to start fetching data into your database.

   ```bash
   python stock_analysis.py
   ```

7. Check if data records are being inserted into the database.

| stock_datetime      | price_open | price_close | price_low | price_high | trading_volume | symbol |
| ------------------- | ---------- | ----------- | --------- | ---------- | -------------- | ------ |
| 2021-06-10 20:00:00 | 126.2801   | 126.2801    | 126.2801  | 126.2801   | 1212           | AAPL   |
| 2021-06-10 19:59:00 | 126.28     | 126.28      | 126.28    | 126.28     | 420            | AAPL   |
| 2021-06-10 19:58:00 | 126.29     | 126.3       | 126.27    | 126.27     | 3021           | AAPL   |
...

## Time-series stock price analysis

1. Query1: How <insert symbol> stock price changed over time? (line chart)
2. Query2: How <insert symbol> trading volume changed over time? (line chart)
3. Query3: Which symbols had the most transaction volumes in the past <insert time frame>? (bar chart)
4. Query4: Prices of FAANG over time? (line chart)
5. Query5: Which symbols had the most daily/weekly/monthly gains/losses?

You can try these queries by:

* running `explore.py` and uncommenting the lines in the main function.
* opening `sql_script/explore.sql` which includes each query in one file.
* using the jupyther notebook to modify the queries and explore other ideas.
