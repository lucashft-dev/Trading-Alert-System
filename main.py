import ccxt
import pandas as pd
import talib
import time
from datetime import datetime


# A améliorer plus tard avec d'autres indicateurs en fonction de la stratégie
def calcul_score(price, setup_type, in_entry_zone, rsi, liquidity_level, last_lows, last_highs, bb_basse, bb_haute, ema50, ema200):

    if not in_entry_zone:
         return 0

    score = 0
    # Forcément 'In_entry_zone' donc + 2 immédiatement
    score += 2

    if setup_type == "LONG":
        if rsi < 30:
            score += 2
        if ema50 > ema200:
            score += 1
        if price < bb_basse:
            score += 1
        # Regarde si on est sous liquidity_level
        current_low = last_lows.iloc[-1]
        if current_low <= liquidity_level:
            score += 2
    elif setup_type == "SHORT":
        if rsi > 70:
            score += 2
        if ema50 < ema200:
            score += 1
        if price > bb_haute:
            score += 1
        # Regarde si on est au dessus de liquidity_level
        current_high = last_highs.iloc[-1]
        if current_high >= liquidity_level:
            score += 2

    return score

def console_log(price, entry_zone, rsi, score):
    now = datetime.now().strftime("%H:%M:%S")

    print("=" * 40)
    print(f"{now}")
    print(f"Price: {price:.2f}")
    print(f"entry_Zone: {entry_zone}")
    print(f"RSI: {rsi:.2f}")
    print(f"Score: {score}")

    if score >= 6:
        print("This is a very strong setup, don't miss it.")
    elif score >= 4:
        print("This setup might be really interesting, take a look.")
    elif score >= 2:
        print("Price in entry_zone, waiting for more indicators ...")
    else:
        print("NO TRADE")
    print("=" * 40)

def get_signal(score, setup_type):
    if setup_type == "LONG":
        if score >= 7:
            return "VERY STRONG LONG SETUP"
        elif score == 6:
            return "STRONG SHORT SETUP"
        elif score == 4:
            return "POTENTIAL SETUP"
        elif score == 2:
            return "WATCH"
        else:
            return "NONE"
    if setup_type == "SHORT":
        if score >= 7:
            return "VERY STRONG SHORT SETUP"
        elif score == 6:
            return "STRONG SHORT SETUP"
        elif score == 4:
            return "POTENTIAL SETUP"
        elif score == 2:
            return "WATCH"
        else:
            return "NONE"


def run():
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv("ETH/USDC", timeframe="1m", limit=200)

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
    # print(df[["timestamp", "close", "rsi", "ema50","ema200"]].tail())


    price = df["close"].iloc[-1]
    volume = df["volume"].iloc[-1]

    rsi = df["rsi"].iloc[-1]
    bb_haute = df["bb_haute"].iloc[-1]
    bb_basse = df["bb_basse"].iloc[-1]
    last_lows = df["low"].tail(10)
    last_highs = df["high"].tail(10)
    ema200 = df["ema200"].iloc[-1]
    ema50 = df["ema50"].iloc[-1]


    setup_type = "SHORT"
    entry_zone = (2226, 2228)
    liquidity_level = 2226.4

    in_entry_zone = entry_zone[0] <= price <= entry_zone[1]

    score = calcul_score(price, setup_type, in_entry_zone, rsi, liquidity_level, last_lows, last_highs, bb_basse, bb_haute, ema50, ema200)

    console_log(price, entry_zone, rsi, score) # Si ici, affihage console a chaque nouvelle boucle (voir main())

    signal = get_signal(score, setup_type)
    return signal, price, entry_zone, rsi, score, last_lows, last_highs, setup_type


def main():
    last_signal = None
    while True:
        try:
            signal, price, entry_zone, rsi, score, last_lows, last_highs, setup_type = run()
            if signal != last_signal:
                print(f"SIGNAL : {signal}")
                # console_log(price, entry_zone, rsi, score) # Affichage console que si nouveau signal pour pas spam la console
                last_signal = signal
        except Exception as e:
            print("ERROR : ", e)

        time.sleep(60)



if __name__ == "__main__":
    main()