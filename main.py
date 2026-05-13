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


# print(df)
# print(df["close"])
# print(df["close"].iloc[-1])
# print(df.tail())
print(df[["timestamp", "close", "rsi", "bb_basse","ema200"]].tail())