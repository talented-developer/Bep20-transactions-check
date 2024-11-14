import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

def get_bscscan_data():
    """Fetch and parse data from BscScan."""
    # URL for BscScan main page
    url = 'https://bscscan.com/'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve data from BscScan: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Scrape BNB price and market cap
    bnb_price = soup.find('div', {'class': 'price'}).text.strip()
    market_cap = soup.find('div', {'class': 'market-cap'}).text.strip()

    # Scrape latest blocks
    latest_blocks = []
    blocks_table = soup.find('table', {'id': 'blocks'})
    for row in blocks_table.find_all('tr')[1:]:  # Skip header row
        cols = row.find_all('td')
        latest_blocks.append({
            'block_number': cols[0].text.strip(),
            'time': cols[1].text.strip(),
            'transactions': cols[2].text.strip(),
            'miner': cols[3].text.strip()
        })

    # Scrape latest transactions
    latest_transactions = []
    transactions_table = soup.find('table', {'id': 'tokentx'})
    for row in transactions_table.find_all('tr')[1:]:  # Skip header row
        cols = row.find_all('td')
        latest_transactions.append({
            'hash': cols[0].text.strip(),
            'from': cols[1].text.strip(),
            'to': cols[2].text.strip(),
            'value': cols[3].text.strip(),
            'token': cols[4].text.strip(),
            'date': cols[5].text.strip()
        })

    return {
        'bnb_price': bnb_price,
        'market_cap': market_cap,
        'latest_blocks': latest_blocks,
        'latest_transactions': latest_transactions,
    }

def main():
    # Load environment variables from .env file (if needed)
    load_dotenv()

    # Fetch data from BscScan
    data = get_bscscan_data()

    if data:
        print(f"BNB Price: {data['bnb_price']}")
        print(f"Market Cap: {data['market_cap']}")
        
        print("\nLatest Blocks:")
        for block in data['latest_blocks']:
            print(f"Block Number: {block['block_number']}, Time: {block['time']}, Transactions: {block['transactions']}, Miner: {block['miner']}")

        print("\nLatest Transactions:")
        for tx in data['latest_transactions']:
            print(f"Hash: {tx['hash']}, From: {tx['from']}, To: {tx['to']}, Value: {tx['value']} {tx['token']}, Date: {tx['date']}")

if __name__ == "__main__":
    main()
