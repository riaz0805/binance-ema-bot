import requests

url = "https://api.binance.com/api/v3/exchangeInfo"

data = requests.get(url).json()

symbols = []

for s in data["symbols"]:
    if s["quoteAsset"] == "USDT" and s["status"] == "TRADING":
        symbols.append(s["symbol"])

print("TOTAL SYMBOLS:", len(symbols))
print(symbols[:20])