###################################################################
# crypto_data_extraction.py
# Script to construct a CSV data set of historical crypto prices
# using data from cryptocompare.com
# Author: Avthar Sewrathan
# Timescale Inc
# 20 August 2019
###################################################################
# The author apologizes in advance for any bad style practices.
# Extraneous statements have been added to help users of this script
# vizualize the progress constructing the CSV
###################################################################
import urllib.request
import json
import csv
from datetime import datetime
import argparse

# accepting api key as a command line argument
# run this script with an argument:
# python crypto_data_extraction.py -a my_api_key
# or
# python crypto_data_extraction.py --apikey my_api_key
parser = argparse.ArgumentParser(description='Api key',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-a', '--apikey', help='valid api key')
args = parser.parse_args()
config = vars(args)
apikey = 'apikey' if config['apikey'] is None else config["apikey"]

# If you don't provide an `apikey` argument when running the script,
# replace and uncomment this string below with your cryptocompare API Key or
# store it as an environment variable
# Note: the script will not run properly if you do not use your own valid API key
# apikey = 'YOUR_CRYPTO_COMPARE_API_KEY'

#attach to end of URLstring
url_api_part = '&api_key=' + apikey

#####################################################################
#1. Populate list of all coin names
#####################################################################
#URL to get a list of coins from cryptocompare API
URLcoinslist = 'https://min-api.cryptocompare.com/data/all/coinlist'

#Get list of cryptos with their symbols
with urllib.request.urlopen(URLcoinslist) as response:
    res1 = response.read()
res1_json = json.loads(res1.decode('utf-8'))
data1 = res1_json['Data']
symbol_array = []
cryptoDict = dict(data1)

#write to CSV
with open('coin_names.csv', mode = 'w') as test_file:
    test_file_writer = csv.writer(test_file, delimiter = ',', quotechar = '"', quoting=csv.QUOTE_MINIMAL)
    for coin in cryptoDict.values():
        name = coin['Name']
        symbol = coin['Symbol']
        symbol_array.append(symbol)
        coin_name = coin['CoinName']
        full_name = coin['FullName']
        entry = [symbol, coin_name]
        test_file_writer.writerow(entry)
print('Done getting crypto names and symbols. See coin_names.csv for result')

#####################################################################
#2. Populate historical price for each crypto in BTC
#####################################################################
#Note: this part might take a while to run since we're populating data for 4k+ coins
#counter variable for progress made
progress = 0
num_cryptos = str(len(symbol_array))
for symbol in symbol_array:
    # get data for that currency
    URL = 'https://min-api.cryptocompare.com/data/histoday?fsym='+ symbol +'&tsym=BTC&allData=true' + url_api_part
    with urllib.request.urlopen(URL) as response:
        res = response.read()
    res_json = json.loads(res.decode('utf-8'))
    data = res_json['Data']
    # write required fields into csv
    with open('crypto_prices.csv', mode = 'a') as test_file:
        test_file_writer = csv.writer(test_file, delimiter = ',', quotechar = '"', quoting=csv.QUOTE_MINIMAL)
        for day in data:
            rawts = day['time']
            ts = datetime.utcfromtimestamp(rawts).strftime('%Y-%m-%d %H:%M:%S')
            o = day['open']
            h = day['high']
            l = day['low']
            c = day['close']
            vfrom = day['volumefrom']
            vto = day['volumeto']
            entry = [ts, o, h, l, c, vfrom, vto, symbol]
            test_file_writer.writerow(entry)
    progress = progress + 1
    print('Processed ' + str(symbol))
    print(str(progress) + ' currencies out of ' +  num_cryptos + ' written to csv')
print('Done getting price data for all coins. See crypto_prices.csv for result')

#####################################################################
#3. Populate BTC prices in different fiat currencies
#####################################################################
# List of fiat currencies we want to query
# You can expand this list, but CryptoCompare does not have
# a comprehensive fiat lsit on their site
fiatList = ['AUD', 'CAD', 'CNY', 'EUR', 'GBP', 'GOLD', 'HKD',
'ILS', 'INR', 'JPY', 'KRW', 'PLN', 'RUB', 'SGD', 'UAH', 'USD', 'ZAR']

#counter variable for progress made
progress2 = 0
for fiat in fiatList:
    # get data for bitcoin price in that fiat
    URL = 'https://min-api.cryptocompare.com/data/histoday?fsym=BTC&tsym='+fiat+'&allData=true' + url_api_part
    with urllib.request.urlopen(URL) as response:
        res = response.read()
    res_json = json.loads(res.decode('utf-8'))
    data = res_json['Data']
    # write required fields into csv
    with open('btc_prices.csv', mode = 'a') as test_file:
        test_file_writer = csv.writer(test_file, delimiter = ',', quotechar = '"', quoting=csv.QUOTE_MINIMAL)
        for day in data:
            rawts = day['time']
            ts = datetime.utcfromtimestamp(rawts).strftime('%Y-%m-%d %H:%M:%S')
            o = day['open']
            h = day['high']
            l = day['low']
            c = day['close']
            vfrom = day['volumefrom']
            vto = day['volumeto']
            entry = [ts, o, h, l, c, vfrom, vto, fiat]
            test_file_writer.writerow(entry)
    progress2 = progress2 + 1
    print('processed ' + str(fiat))
    print(str(progress2) + ' currencies out of  17 written')
print('Done getting price data for btc. See btc_prices.csv for result')

#####################################################################
#4. Populate ETH prices in different fiat currencies
#####################################################################
#counter variable for progress made
progress3 = 0
for fiat in fiatList:
    # get data for bitcoin price in that fiat
    URL = 'https://min-api.cryptocompare.com/data/histoday?fsym=ETH&tsym='+fiat+'&allData=true' + url_api_part
    with urllib.request.urlopen(URL) as response:
        res = response.read()
    res_json = json.loads(res.decode('utf-8'))
    data = res_json['Data']
    # write required fields into csv
    with open('eth_prices.csv', mode = 'a') as test_file:
        test_file_writer = csv.writer(test_file, delimiter = ',', quotechar = '"', quoting=csv.QUOTE_MINIMAL)
        for day in data:
            rawts = day['time']
            ts = datetime.utcfromtimestamp(rawts).strftime('%Y-%m-%d %H:%M:%S')
            o = day['open']
            h = day['high']
            l = day['low']
            c = day['close']
            vfrom = day['volumefrom']
            vto = day['volumeto']
            entry = [ts, o, h, l, c, vfrom, vto, fiat]
            test_file_writer.writerow(entry)
    progress3 = progress3 + 1
    print('processed ' + str(fiat))
    print(str(progress3) + ' currencies out of  17 written')
print('Done getting price data for eth. See eth_prices.csv for result')
