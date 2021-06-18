import plotly.express as px
import pandas as pd
import psycopg2
from config import StocksConfig as config

conn = psycopg2.connect(database=config.DB_NAME,
                        host=config.DB_HOST,
                        user=config.DB_USER,
                        password=config.DB_PASS,
                        port=config.DB_PORT)


#  How <ticker> price changed over time?
def query1():
    query = """
        SELECT time_bucket('7 days', stock_datetime) AS time_frame,
        last(price_close, stock_datetime) AS last_closing_price
        FROM stocks_new
        WHERE symbol = 'AAPL'
        GROUP BY time_frame
        ORDER BY time_frame
    """
    df = pd.read_sql(query, conn)

    fig = px.line(df, x='time_frame', y='last_closing_price')
    fig.show()

# How <ticker> trading volume changed over time?
def query2():
    query = """
        SELECT time_bucket('7 days', stock_datetime) AS time_frame, sum(trading_volume) AS volume
        FROM stocks_new
        WHERE symbol = 'AAPL'
        GROUP BY time_frame
        ORDER BY time_frame
    """
    df = pd.read_sql(query, conn)

    fig = px.line(df, x='time_frame', y='volume')
    fig.show()

# Which tickers had the most transaction volume in the past 14 days?
def query3():
    query = """
        SELECT symbol, sum(trading_volume) AS volume
        FROM stocks_new
        WHERE (now() - date(stock_datetime)) < INTERVAL '14 day'
        GROUP BY symbol
        ORDER BY volume DESC
        LIMIT 5
    """
    df = pd.read_sql(query, conn)

    fig = px.bar(df, x='symbol', y='volume')
    fig.show()

# FAANG prices over time
def query4():
    query = """
    SELECT symbol, time_bucket('30 days', stock_datetime) AS time_frame, last(price_close, stock_datetime) AS last_closing_price
    FROM stocks_new
    WHERE symbol in ('AAPL', 'FB', 'AMZN', 'NFLX', 'GOOG')
    GROUP BY time_frame, symbol
    ORDER BY time_frame
    """
    df = pd.read_sql(query, conn)

    fig = px.line(df, x='time_frame', y='last_closing_price', color='symbol')
    fig.show()

# Which symbols had the biggest daily gain/loss?
def query5():
    query = """
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
    """
    df = pd.read_sql(query, conn)
    print(df)


def main():
    query1()
    #query2()
    #query3()
    #query4()
    #query5()
    
if __name__=='__main__':
    main()