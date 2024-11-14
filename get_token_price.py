import requests

# Replace 'your_token_symbol' with the desired cryptocurrency symbol (e.g., 'bitcoin', 'ethereum')
token_symbol = 'binance-bridged-usdt-bnb-smart-chain'  
url = f'https://api.coingecko.com/api/v3/simple/price?ids={token_symbol}&vs_currencies=usd'

# Make a GET request to the API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    
    print(f'The current price data of {token_symbol} is ${data}')
    # Access the price
    # price = data[token_symbol]['usd']
    # print(f'The current price of {token_symbol} is ${price}')
else:
    print('Error fetching data:', response.status_code)