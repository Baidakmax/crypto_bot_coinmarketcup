import requests
from bs4 import BeautifulSoup

def fetch_crypto_prices():
    url = "https://coinmarketcap.com/"
    responce = requests.get(url)
    soup = BeautifulSoup(responce.text, 'lxml')  # use parse lxml

    # Parsing of cryptocurrency data (e.g. Bitcoin and Ethereum)
    crypto_data = []
    rows = soup.find_all("tr", class_="cmc-table-row")
    for row in rows[:10]:  # parse first 10 cryptoсurrencies
        name = row.find("p", class_="sc-1eb5slv-0 iJjGCS").get_text(strip=True)
        price = row.find("span", class_="sc-131di3y-0 cLgOOr").get_text(strip=True)
        volume = row.find_all('td', class_='cmc-table__cell')[2].get_text(strip=True)
        market_cap = row.find_all("td", class_='cmc-table__cell')[3].get_text(strip=True)
        crypto_data.append({
            "name": name,
            "price": price,
            "volume": volume,
            "market_cap" : market_cap
        })
    return crypto_data

print(fetch_crypto_prices())