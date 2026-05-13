import ccxt
import pandas as pd

exchange = ccxt.binance()
ohlcv = exchange.fetch_ohlcv("ETH/USDT", timeframe="1m", limit=100)

df = pd.DataFrame(
    ohlcv,
    columns=["timestamp", "open", "high", "low", "close", "volume"]
)

df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

# print(df)
# print(df["close"])
# print(df["close"].iloc[-1])
# print(df.tail())