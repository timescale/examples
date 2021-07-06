import requests, csv
from bs4 import BeautifulSoup

def scrape_symbols():
    """Scrapes ticker symbols of top 100 US companies (based on market cap)

    Returns:
        list of strings: 100 ticker symbols
    """
    
    url = 'https://companiesmarketcap.com/usa/largest-companies-in-the-usa-by-market-cap/'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    return [e.text for e in soup.select('div.company-code')]

def create_symbols_csv():
    with open("symbols.csv", "w", newline='') as f:
        writer = csv.writer(f)
        for symbol in scrape_symbols():
            writer.writerow([symbol])

def read_symbols_csv():
    with open('symbols.csv') as f:
        reader = csv.reader(f)
        return [row[0] for row in reader]

create_symbols_csv()
symbols = read_symbols_csv()
print(symbols)