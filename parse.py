import requests
from bs4 import BeautifulSoup


def fetch_crypto_prices(limit=10):
    """
    Fetches the current prices, volumes, and market caps of the top 10 cryptocurrencies from CoinMarketCap.

    The function sends a GET request to the CoinMarketCap homepage, parses the response HTML to extract
    cryptocurrency data, and returns a list of dictionaries containing the name, price, volume, and market cap
    of each cryptocurrency.

    Returns:
        list: A list of dictionaries, each containing the following keys:
            - 'name' (str): The name of the cryptocurrency.
            - 'price' (str): The current price of the cryptocurrency.
            - 'volume' (str): The 24-hour trading volume of the cryptocurrency.
            - 'market_cap' (str): The market capitalization of the cryptocurrency.
    :return:
    """
    url = 'https://coinmarketcap.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')  # use parse lxml

    # Parsing of cryptocurrency data (e.g. Bitcoin and Ethereum)
    crypto_data = []
    table = soup.find('table', class_='cmc-table')
    if not table:
        print("Table not found")
        return crypto_data

    rows = table.find_all('tr')[1:limit + 1]  # Skip the header and parse the first 10 cryptocurrencies

    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 7:
            continue  # Skip rows with insufficient number of columns

        name_tag = cols[2].find('p')
        price_tag = cols[3].find('div', class_='sc-a093f09c-0 gPTgRa')
        volume_tag = cols[8].find('p', class_="sc-71024e3e-0 bbHOdE font_weight_500")
        market_cap_tag = cols[7].find('span')

        name = name_tag.get_text(strip=True)
        price = price_tag.get_text(strip=True)
        volume = volume_tag.get_text(strip=True)
        market_cap = market_cap_tag.get_text(strip=True)

        crypto_data.append({
            'name': name,
            'price': price,
            'volume': volume,
            'market_cap': market_cap
        })

    return crypto_data


def fetch_crypto_by_name_first_ten(name):
    """
    Fetches the current price, volume, and market cap of a specific cryptocurrency by its name.

    Args:
        name (str): The name of the cryptocurrency to search for.

    Returns:
        dict: A dictionary containing the following keys:
            - 'name' (str): The name of the cryptocurrency.
            - 'price' (str): The current price of the cryptocurrency.
            - 'volume' (str): The 24-hour trading volume of the cryptocurrency.
            - 'market_cap' (str): The market capitalization of the cryptocurrency.
            If the cryptocurrency is not found, returns an empty dictionary.
    """
    all_data = fetch_crypto_prices(limit=10)  # Fetch a larger set of data to include more cryptocurrencies
    for crypto in all_data:
        if crypto['name'].lower() == name.lower():
            return crypto
    return {}


def fetch_crypto_by_name_11_to_100(name):
    """
    Fetches the current price of a specific cryptocurrency by its name from the 11th to the 100th position.

    Args:
        name (str): The name of the cryptocurrency to search for.

    Returns:
        dict: A dictionary containing the following keys:
            - 'name' (str): The name of the cryptocurrency.
            - 'price' (str): The current price of the cryptocurrency.
            If the cryptocurrency is not found, returns an empty dictionary.
    """
    url = 'https://coinmarketcap.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    table = soup.find('table', class_='cmc-table')
    # if not table:
    #     print("Table not found")
    #     return {}

    rows = table.find_all('tr')[12:101]  # Parse the 11th to 100th cryptocurrencies

    for row in rows:
        cols = row.find_all('td')

        # if len(cols) < 5:
        #     continue  # Skip rows with insufficient number of columns

        name_tag = cols[2].find('a', class_='cmc-link')
        price_tag = cols[3].text

        name_spans = name_tag.find_all('span')

        crypto_name = name_spans[1].text
        print(crypto_name)
        price = price_tag if price_tag else 'N/A'

        if crypto_name.lower() == name.lower():
            return {
                'name': crypto_name,
                'price': price
            }

    return {}


