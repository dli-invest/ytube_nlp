# Assume this script is run from root during github actions
import requests 
stock_api = 'https://fstocks-fs25ivfruq-uw.a.run.app'
r = requests.get(f"{stock_api}/api/tickers")
resp = r.json()
stocks = resp.get('data')
meaningful_stocks = [stock.lower() for stock in stocks if len(stock) > 1]
# Make all 
with open("lib/nlp/curr_tickers.py", "a") as file_object:
    # Append 'hello' at the end of file
    formatted_stocks = f"\nstocks={meaningful_stocks} \n"
    file_object.write(formatted_stocks)