import requests

url = "https://api.binance.com/api/v3/exchangeInfo"

response = requests.get(url, timeout=20)

print("STATUS CODE:", response.status_code)
print("RESPONSE:")
print(response.text[:500])