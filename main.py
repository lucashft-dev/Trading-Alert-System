import ccxt
import pandas as pd
import talib
import time
from datetime import datetime


# A améliorer plus tard avec d'autres indicateurs en fonction de la stratégie
# Inutile dans la version actuelle du bot
def calcul_score(in_zone, rsi, price, bb_basse, liquidity, last_lows):

    if not in_zone:
         return 0
    
    score = 0
    # Forcément 'In_zone' donc + 1 immédiatement
    score += 1

    if rsi < 30:
        score += 1

    if price < bb_basse:
        score += 1

    # Regarde on est sous liquidity sweep
    currents_lows = last_lows.iloc[-1]
    if currents_lows <= liquidity:
        score += 1

    return score

def console_log(price, support_area, rsi, score):
    now = datetime.now().strftime("%H:%M:%S")

    print("=" * 40)
    print(f"{now}")
    print(f"Price: {price:.2f}")
    print(f"Zone: {support_area}")
    print(f"RSI: {rsi:.2f}")
    print(f"Score: {score}")

    if score >= 4:
        print("PRICE IN ZONE AND RSI OVERSOLD, STRONG SIGNAL")
    elif score >= 2:
        print("PRICE IN ZONE, WAITING FOR RSI")
    else:
        print("NO TRADE")
    print("=" * 40)

def get_signal(score):
    if score == 4:
        return "VERY STRONG SETUP"
    elif score == 3:
        return "STRONG SETUP"
    elif score == 2:
        return "POTENTIAL SETUP"
    elif score == 1:
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
    rsi = df["rsi"].iloc[-1]
    bb_haute = df["bb_haute"].iloc[-1]
    bb_basse = df["bb_basse"].iloc[-1]
    ema200 = df["ema200"].iloc[-1]
    ema50 = df["ema50"].iloc[-1]
    last_lows = df["low"].tail(10)


    support_area = (2291.65, 2296.08)
    liquidity = 2295.5

    in_zone = support_area[0] <= price <= support_area[1]

    score = calcul_score(in_zone, rsi, price, bb_basse, liquidity, last_lows)

    console_log(price, support_area, rsi, score) # Si ici, affihage console a chaque nouvelle boucle (voir main())

    signal = get_signal(score)
    return signal, price, support_area, rsi, score, last_lows


def main():
    last_signal = None
    while True:
        try:
            signal, price, support_area, rsi, score, last_lows = run()
            if signal != last_signal:
                print(f"SIGNAL : {signal}")
                # console_log(price, support_area, rsi, score) # Affichage console que si nouveau signal pour pas spam la console
                last_signal = signal
        except Exception as e:
            print("ERROR : ", e)

        time.sleep(60)



if __name__ == "__main__":
    main()