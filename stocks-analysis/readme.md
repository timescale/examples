# Analyze historical intraday stock data

This project is an example on how to collect, store, and analyze intraday stock data with Python and 
TimescaleDB. To read the full tutorial, go to the TimescaleDB documentation!

## Prerequisites

* Python 3
* TimescaleDB (see [installation options](https://docs.timescale.com/timescaledb/latest/how-to-guides/install-timescaledb/))
* Alpha Vantage API key ([get one for free](https://www.alphavantage.co/support/#api-key))
* Virtualenv (`pip install virtualenv`)

## Installation and database setup

### Clone repository and open intraday-stocks-analysis

```bash
git clone https://github.com/timescale/examples.git
cd intraday-stocks-analysis/ 
```

### Create new virtual environment

```bash
virtualenv env
source env/bin/activate
```

### Install requirements

```bash
pip install -r requirements.txt
```

### Create table
Run `sql_script/create_table.sql`:

```sql
CREATE TABLE public.stocks_intraday (
    "time" timestamp(0) NOT NULL,
    symbol varchar NULL,
    price_open float8 NULL,
    price_close float8 NULL,
    price_low float8 NULL,
    price_high float8 NULL,
    trading_volume int4 NULL,
);
```

### Turn it into a hypertable
Run `sql_script/create_hypertable.sql`

```sql
/* Enable the TimscaleDB extension */
CREATE EXTENSION IF NOT EXISTS timescaledb;

/* 
Turn the 'stocks_intraday' table into a hypertable.
This is important to be able to make use of TimescaleDB features later on.
*/
SELECT create_hypertable('stocks_intraday', 'time');
```

### Edit configuration file
Edit `config.py` according to your database connection details.
```python
# Make sure to edit this configuration file with your database connection details
# and Alpha Vantage API key
DB_USER = 'user'
DB_PASS = 'passwd'
DB_HOST = 'host'
DB_PORT = '000'
DB_NAME = 'db'
APIKEY = 'alpha_vantage_apikey'
```
Also, `config.py` holds your Alpha Vantage API key, so make sure to edit that too.


## Usage

Run `explore.py` to run your first query against your database.

```bash
python explore.py
```
