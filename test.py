import requests
def btc():
    response = requests.get('https://api.blockchain.com/v3/exchange/tickers/BTC-USD')
    if response.status_code == 200:
        return response.json()['last_trade_price']


print(btc())
