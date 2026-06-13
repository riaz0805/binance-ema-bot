import requests

url = "https://api.binance.com/api/v3/exchangeInfo"

response = requests.get(url, timeout=20)

print("STATUS:", response.status_code)
print("RAW RESPONSE:")
print(response.text)