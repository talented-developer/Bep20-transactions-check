import os
import requests
from dotenv import load_dotenv
from datetime import datetime

def get_bep20_transactions(wallet_address, api_key):
    """Fetch all BEP20 transactions for a given wallet address."""
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

def classify_transactions(transactions):
    """Classify transactions into valid and invalid based on specific criteria."""
    valid_transactions = []
    invalid_transactions = []

    for tx in transactions:
        tx_hash = tx['hash']
        from_address = tx['from']
        to_address = tx['to']
        value = int(tx['value']) / (10 ** int(tx['tokenDecimal']))  # Convert value to human-readable format
        confirmations = int(tx['confirmations'])
        token_symbol = tx['tokenSymbol']

        # Check validity criteria including token symbol
        if (tx_hash and from_address and to_address and value > 0 
                and confirmations > 0 and token_symbol == 'BSC-USD'):
            valid_transactions.append(tx)
        else:
            invalid_transactions.append(tx)

    return valid_transactions, invalid_transactions

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

    # Classify transactions into valid and invalid
    valid_transactions, invalid_transactions = classify_transactions(transactions)

    # Display results
    total_transactions = len(transactions)
    
    print(f"\nTotal BEP20 Transactions for {wallet_address}: {total_transactions}")
    
    print(f"\nValid Transactions: {len(valid_transactions)}")
    for tx in valid_transactions:
        transaction_date = datetime.utcfromtimestamp(int(tx['timeStamp'])).strftime('%Y-%m-%d %H:%M:%S')
        print(f"Hash: {tx['hash']}, From: {tx['from']}, To: {tx['to']}, Value: {int(tx['value']) / (10 ** int(tx['tokenDecimal'])):.6f} {tx['tokenSymbol']}, Date: {transaction_date}")

    print(f"\nInvalid Transactions: {len(invalid_transactions)}")
    for tx in invalid_transactions:
        transaction_date = datetime.utcfromtimestamp(int(tx['timeStamp'])).strftime('%Y-%m-%d %H:%M:%S')
        print(f"Hash: {tx.get('hash', 'N/A')}, From: {tx.get('from', 'N/A')}, To: {tx.get('to', 'N/A')}, Value: {int(tx['value']) / (10 ** int(tx['tokenDecimal'])):.6f} {tx.get('tokenSymbol', 'N/A')}, Date: {transaction_date}")

if __name__ == "__main__":
    main()