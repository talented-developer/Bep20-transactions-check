import requests
import json

def save_tokens_to_file(filename):
    url = 'https://api.coingecko.com/api/v3/coins/list'
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the JSON response
        coins = response.json()
        
        # Save the tokens to a JSON file
        with open(filename, 'w') as file:
            json.dump(coins, file, indent=4)
        
        print(f"Successfully saved {len(coins)} tokens to {filename}.")
    else:
        print('Error fetching data:', response.status_code)

# Specify the filename
filename = 'all_token_symbols.json'

# Fetch and save tokens to file
save_tokens_to_file(filename)