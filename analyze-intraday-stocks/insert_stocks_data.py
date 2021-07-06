import csv
import pandas as pd
import config
import psycopg2
from pgcopy import CopyManager

conn = psycopg2.connect(database=config.DB_NAME, 
                            host=config.DB_HOST, 
                            user=config.DB_USER, 
                            password=config.DB_PASS, 
                            port=config.DB_PORT)
columns = ('stock_datetime', 'price_open', 'price_close', 
           'price_low', 'price_high', 'trading_volume', 'symbol')

def get_symbols():
    """Read symbols from a csv file.

    Returns:
        [list of strings]: symbols
    """
    with open('symbols.csv') as f:
        reader = csv.reader(f)
        return [row[0] for row in reader]

def fetch_stock_data(symbol, month):
    """Fetches historical intraday data for one ticker symbol (1-min interval)

    Args:
        symbol (string): ticker symbol
        month (int): month value as an integer 1-24 (for example month=4 will fetch data from the last 4 months)

    Returns:
        list of tuples: intraday (candlestick) stock data
    """
    interval = '1min'
    slice = 'year1month' + str(month) if month <= 12 else 'year2month1' + str(month)
    apikey = config.APIKEY
    CSV_URL = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&' \
              'symbol={symbol}&interval={interval}&slice={slice}&apikey={apikey}' \
              .format(symbol=symbol, slice=slice, interval=interval,apikey=apikey)
    df = pd.read_csv(CSV_URL)
    df['symbol'] = symbol

    df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')
    df = df.rename(columns={'time': 'time', 
                            'open': 'price_open', 
                            'close': 'price_close', 
                            'high': 'price_high',
                            'low': 'price_low',
                            'volume': 'trading_volume'}
                            )
    return [row for row in df.itertuples(index=False, name=None)] 

def main():
    symbols = get_symbols()
    for symbol in symbols:
        print("Fetching data for: ", symbol)
        for month in range(1, 3): # last 2 months, you can go up to 24 month if you want to
            stock_data = fetch_stock_data(symbol, month)
            print('Inserting data...')
            mgr = CopyManager(conn, 'stocks_intraday', columns)
            mgr.copy(stock_data)
            conn.commit()


if __name__ == '__main__':
    main()
