import pandas as pd
import ccxt
from config.config import SYMBOLE, TIMEFRAME, SETUP_TYPE, ENTRY_ZONE, LIQUIDITY_LEVEL
import talib



def fetch_market_data():
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(SYMBOLE, timeframe=TIMEFRAME, limit=200)

    df = pd.DataFrame(
        ohlcv,
        columns=["timestamp", "open", "high", "low", "close", "volume"]
    )
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

    # Manipulation utile a retenir :
    # print(df)
    # print(df["close"])
    # print(df["close"].iloc[-1])
    # print(df.tail())
    # print(df[["timestamp", "close", "rsi", "ema50","ema200"]].tail())


def calculate_indicators(df):
    df["rsi"] = talib.RSI(df["close"], timeperiod=14)
    df["bb_haute"], df["bb_mid"], df["bb_basse"] = talib.BBANDS(df["close"], timeperiod=20)
    df["ema50"] = talib.EMA(df["close"], timeperiod=50)
    df["ema200"] = talib.EMA(df["close"], timeperiod=200)

    price = df["close"].iloc[-1]

    rsi = df["rsi"].iloc[-1]

    bb_haute = df["bb_haute"].iloc[-1]
    bb_basse = df["bb_basse"].iloc[-1]

    last_open = df["open"].iloc[-1]
    last_close = df["close"].iloc[-1]
    last_low = df["low"].iloc[-1]
    last_high = df["high"].iloc[-1]

    ema200 = df["ema200"].iloc[-1]
    ema50 = df["ema50"].iloc[-1]

    return price, rsi, bb_haute, bb_basse, ema200, ema50, last_open, last_close, last_low, last_high