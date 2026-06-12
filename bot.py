import requests
import pandas as pd
from binance.client import Client
import os

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

client = Client()

def send_msg(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

def get_symbols():
    info = client.get_exchange_info()
    return [
        s["symbol"] for s in info["symbols"]
        if s["quoteAsset"] == "USDT" and s["status"] == "TRADING"
    ]

def check(symbol, interval):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=100)

    df = pd.DataFrame(klines)
    df = df.iloc[:, 0:6]
    df.columns = ["t","o","h","l","c","v"]

    df["c"] = df["c"].astype(float)
    df["ema21"] = df["c"].ewm(span=21).mean()

    last = df.iloc[-1]
    prev = df.iloc[-2]

    price = last["c"]
    ema = last["ema21"]

    # Touch condition
    if abs(price - ema) / ema < 0.002:
        send_msg(f"⚡ {symbol} touching EMA21 ({interval})\nPrice: {price:.4f}")

    # Breakout condition
    if price > ema and prev["c"] < prev["ema21"]:
        send_msg(f"🚀 {symbol} BREAKOUT EMA21 ({interval})\nPrice: {price:.4f}")

symbols = get_symbols()

for s in symbols:
    try:
        check(s, Client.KLINE_INTERVAL_4HOUR)
        check(s, Client.KLINE_INTERVAL_1DAY)
    except:
        pass
