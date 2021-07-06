import plotly.express as px
import pandas as pd
import psycopg2
import config

conn = psycopg2.connect(database=config.DB_NAME,
                        host=config.DB_HOST,
                        user=config.DB_USER,
                        password=config.DB_PASS,
                        port=config.DB_PORT)


#  Which symbols have the highest transaction volumes?
def query1():
    query = """
        SELECT symbol, sum(trading_volume) AS volume
        FROM stocks_intraday
        WHERE time < now() - INTERVAL '{bucket}'
        GROUP BY symbol
        ORDER BY volume DESC
        LIMIT 5
    """.format(bucket="14 day")
    df = pd.read_sql(query, conn)
    fig = px.bar(df, x='symbol', y='volume', title="Most traded symbols in the last 14 days")
    fig.show()

# How did Apple's trading volume change over time?
def query2():
    query = """
        SELECT time_bucket('{bucket}', time) AS bucket, sum(trading_volume) AS volume
        FROM stocks_intraday
        WHERE symbol = '{symbol}'
        GROUP BY bucket
        ORDER BY bucket
    """.format(bucket="1 day", symbol="AAPL")
    df = pd.read_sql(query, conn)
    fig = px.line(df, x='bucket', y='volume', title="Apple's daily trading volume over time")
    fig.show()

# How did Apple's stock price change over time? 
def query3():
    query = """
        SELECT time_bucket('{bucket}', time) AS bucket,
        last(price_close, time) AS last_closing_price
        FROM stocks_intraday
        WHERE symbol = '{symbol}'
        GROUP BY bucket
        ORDER BY bucket
    """.format(bucket="7 days", symbol="AAPL")
    df = pd.read_sql(query, conn)
    fig = px.line(df, x='bucket', y='last_closing_price')
    fig.show()

# Which symbols had the highest weekly gains?
def query4():
    query = """
        SELECT symbol, bucket, max((closing_price-opening_price)/closing_price*100) AS price_change_pct
        FROM ( 
            SELECT 
            symbol, 
            time_bucket('{bucket}', time) AS bucket, 
            first(price_open, time) AS opening_price, 
            last(price_close, time) AS closing_price
            FROM stocks_intraday
            GROUP BY bucket, symbol
        ) s
        GROUP BY symbol, s.bucket
        ORDER BY price_change_pct {orderby}
        LIMIT 5
    """.format(bucket="7 days", orderby="DESC")
    df = pd.read_sql(query, conn)
    print(df)

# Weekly FAANG prices over time?
def query5():
    query = """
        SELECT symbol, time_bucket('{bucket}', time) AS bucket, 
        last(price_close, time) AS last_closing_price
        FROM stocks_intraday
        WHERE symbol in {symbols}
        GROUP BY bucket, symbol
        ORDER BY bucket
    """.format(bucket="7 days", symbols="('AAPL', 'FB', 'AMZN', 'NFLX', 'GOOG')")
    df = pd.read_sql(query, conn)
    fig = px.line(df, x='bucket', y='last_closing_price', color='symbol', title="FAANG prices over time")
    fig.show()
    
# Weekly price changes of Apple, Facebook, Google?
def query6():
    query = """
    SELECT symbol, bucket, max((closing_price-opening_price)/closing_price) AS price_change_pct
        FROM ( 
            SELECT 
            symbol, 
            time_bucket('{bucket}}', time) AS bucket, 
            first(price_open, time) AS opening_price, 
            last(price_close, time) AS closing_price
            FROM stocks_intraday
            WHERE symbol IN {symbols}
            GROUP BY bucket, symbol
        ) s
        GROUP BY symbol, s.bucket
        ORDER BY bucket
    """.format(bucket="7 days", symbols="('AAPL', 'FB', 'GOOG')")
    df = pd.read_sql(query, conn)
    figure = px.line(df, x="bucket", y="price_change_pct", color="symbol", title="Apple, Facebook, Google weekly price changes")
    figure = figure.update_layout(yaxis={'tickformat': '.2%'})
    figure.show()

# Distribution of daily price changes of Amazon and Zoom
def query7():
    query = """
    SELECT symbol, bucket, max((closing_price-opening_price)/closing_price) AS price_change_pct
        FROM ( 
            SELECT 
            symbol, 
            time_bucket('{bucket}', time) AS bucket, 
            first(price_open, time) AS opening_price, 
            last(price_close, time) AS closing_price
            FROM stocks_intraday
            WHERE symbol IN {symbols}
            GROUP BY bucket, symbol
        ) s
        GROUP BY symbol, s.bucket
        ORDER BY bucket
    """.format(bucket="1 day", symbols="('ZM', 'AMZN')")
    df = pd.read_sql(query, conn)
    figure = px.scatter(df, x="price_change_pct", color="symbol", title="Distribution of daily price changes (Amazon, Zoom)")
    figure = figure.update_layout(xaxis={'tickformat': '.2%'})
    figure.show()
    
# Apple 15-min candlestick chart
def query8():
    import plotly.graph_objects as go
    query = """
        SELECT time_bucket('{bucket}', time) AS bucket, 
        FIRST(price_open, time) AS price_open, 
        LAST(price_close, time) AS price_close,
        MAX(price_high) AS price_high,
        MIN(price_low) AS price_low
        FROM stocks_intraday
        WHERE symbol = '{symbol}' AND date(time) = date('{date}') 
        GROUP BY bucket
    """.format(bucket="15 min", symbol="AAPL", date="2021-06-09")
    df = pd.read_sql(query, conn)
    figure = go.Figure(data=[go.Candlestick(x=df['bucket'],
                    open=df['price_open'],
                    high=df['price_high'],
                    low=df['price_low'],
                    close=df['price_close'],)])
    figure.update_layout(title="15-min candlestick chart of Apple, 2021-06-09")
    figure.show()   
    

def main():
    query1()
    #query2()
    #query3()
    #query4()
    #query5()
    #query6()
    #query7()
    #query8()
    
if __name__=='__main__':
    main()