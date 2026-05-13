import ccxt
import pandas as pd
import talib


exchange = ccxt.binance()
ohlcv = exchange.fetch_ohlcv("ETH/USDT", timeframe="1m", limit=250)


df = pd.DataFrame(
    ohlcv,
    columns=["timestamp", "open", "high", "low", "close", "volume"]
)
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")


df["rsi"] = talib.RSI(df["close"], timeperiod=14)
df["bb_haute"], df["bb_mid"], df["bb_basse"] = talib.BBANDS(df["close"], timeperiod=20)
df["ema50"] = talib.EMA(df["close"], timeperiod=50)
df["ema200"] = talib.EMA(df["close"], timeperiod=200)


price = df["close"].iloc[-1]
rsi = df["rsi"].iloc[-1]
bb_haute = df["bb_haute"].iloc[-1]
bb_mid = df["bb_mid"].iloc[-1]
bb_basse = df["bb_basse"].iloc[-1]
ema200 = df["ema200"].iloc[-1]
ema50 = df["ema50"].iloc[-1]


support_area = (2298.4, 2300.15)
in_zone = support_area[0] <= price <= support_area[1]


def calcul_score(in_zone, rsi, ema50, ema200):

    if not in_zone:
         return 0
    
    score = 0
    # Forcément 'In_zone' donc + 2 immédiatement
    score += 2

    if rsi < 30:
        score += 2

    if ema50 > ema200:
        score += 1

    return score

# print(df)
# print(df["close"])
# print(df["close"].iloc[-1])
# print(df.tail())
# print(df[["timestamp", "close", "rsi", "bb_basse","ema200"]].tail())