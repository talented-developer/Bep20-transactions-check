import os
import requests
from dotenv import load_dotenv

def get_bep20_transactions(wallet_address, api_key):
    # Initialize variables
    transactions = []
    start_block = 0
    end_block = 99999999
    page = 1
    offset = 100  # Number of transactions per request

    while True:
        # Construct the API URL
        url = f'https://api.bscscan.com/api?module=account&action=tokentx&address={wallet_address}&startblock={start_block}&endblock={end_block}&page={page}&offset={offset}&sort=asc&apikey={api_key}'
        
        # Make the API request
        response = requests.get(url)
        data = response.json()

        # Check if the response is valid
        if data['status'] == '1':
            transactions.extend(data['result'])
            print(f"Fetched {len(data['result'])} transactions from page {page}.")
            # Check if there are more transactions to fetch
            if len(data['result']) < offset:
                break  # No more transactions to fetch
            page += 1  # Move to the next page
        else:
            print("Error fetching data:", data.get('message', 'Unknown error'))
            break

    return transactions

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Get wallet address and API key from environment variables
    wallet_address = os.getenv("WALLET_ADDRESS")
    api_key = os.getenv("API_KEY")

    if not wallet_address or not api_key:
        print("Please set WALLET_ADDRESS and API_KEY in the .env file.")
        return

    # Fetch BEP20 transactions
    transactions = get_bep20_transactions(wallet_address, api_key)

    # Display the results
    if transactions:
        print(f"\nTotal BEP20 Transactions for {wallet_address}: {len(transactions)}")
        for tx in transactions:
            print(f"Hash: {tx['hash']}, From: {tx['from']}, To: {tx['to']}, Value: {tx['value']} {tx['tokenSymbol']}, Date: {tx['timeStamp']}")
    else:
        print("No BEP20 transactions found.")

if __name__ == "__main__":
    main()