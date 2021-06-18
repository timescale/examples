from bs4 import BeautifulSoup
import requests
import pandas as pd
from config import StocksConfig as config
import psycopg2
from pgcopy import CopyManager

def get_symbols():
    """Scrapes ticker symbols of top 100 US companies (based on market cap)

    Returns:
        list of strings: 100 ticker symbols
    """
    
    url = 'https://companiesmarketcap.com/usa/largest-companies-in-the-usa-by-market-cap/'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    symbols = [e.text for e in soup.select('div.company-code')]
    return symbols

def fetch_stock_data(symbol):
    """Fetches historical intraday data for one ticker symbol (1-min interval)

    Args:
        symbol (string): ticker symbol

    Returns:
        dataframe
    """
    interval = '1min'
    slice = 'year1month1'
    apikey = config.APIKEY
    CSV_URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&' \
              'symbol={symbol}&interval={interval}&slice={slice}&apikey={apikey}' \
              .format(symbol=symbol, slice=slice, interval=interval,apikey=apikey)
    df = pd.read_csv(CSV_URL)
    df['symbol'] = symbol

    df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')
    df = df.rename(columns={'time': 'stock_datetime', 
                            'open': 'price_open', 
                            'close': 'price_close', 
                            'high': 'price_high',
                            'low': 'price_low',
                            'volume': 'trading_volume'}
                            )

    return [row for row in df.itertuples(index=False, name=None)] 


def insert_to_db(records):
    """Batch inserts records into db

    Args:
        records (list of tuples)
    """
    conn = psycopg2.connect(database=config.DB_NAME, host=config.DB_HOST, user=config.DB_USER, password=config.DB_PASS, port=config.DB_PORT)
    columns = ('stock_datetime', 'price_open', 'price_close', 'price_low', 'price_high', 'trading_volume', 'symbol')
    mgr = CopyManager(conn, 'stocks2', columns)
    mgr.copy(records)
    conn.commit()

def main():
    symbols = get_symbols()[:10] # for testing purposes, limiting this to 10
    for symbol in symbols:
        print("Fetching data for: ", symbol)
        stock_data = fetch_stock_data(symbol)
        print('Inserting data...')
        insert_to_db(stock_data)


if __name__ == '__main__':
    main()
