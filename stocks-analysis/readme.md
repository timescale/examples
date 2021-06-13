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

## Requirements
* Python 3
* Virtualenv
* PostgreSQL database with TimescaleDB extension

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

4. Run stock_analyis.py to start fetching data into your database.

```bash
python stock_analysis.py
```

5. Check if data records are being inserted into the database.

|stock_datetime|price_open|price_close|price_low|price_high|trading_volume|symbol|
|--------------|----------|-----------|---------|----------|--------------|------|
|2021-06-10 20:00:00|126.2801|126.2801|126.2801|126.2801|1212|AAPL|
|2021-06-10 19:59:00|126.28|126.28|126.28|126.28|420|AAPL|
|2021-06-10 19:58:00|126.29|126.3|126.27|126.27|3021|AAPL|
...