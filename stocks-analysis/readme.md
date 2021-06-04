# Historical stock data analysis tutorial

How to collect, store and analyze stock data with Python. This project will be built out in live Twitch streams.


1. Collect stock ticker symbols
   Top 10 stocks based on US market capitalization. 
   Extracted [from the web](https://companiesmarketcap.com/usa/largest-companies-in-the-usa-by-market-cap/)
2. Collect historical stock data using Alpha Vantage's free API.
   Use [Alpha Vantage's API](https://www.alphavantage.co/documentation/) to fetch historical stock data.
3. Store data in TimescaleDB.
4. Analyze the dataset
   Data visualization to answer specific questions regarding the dataset.

## Setup
* Python 3
* PostgreSQL database with TimescaleDB extension
* Virtualenv and `pip install -r requirements.txt`
