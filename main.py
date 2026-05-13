import ccxt
import pandas as pd
import talib
import time



# A améliorer plus tard avec d'autres indicateurs en fonction de la stratégie
# Inutile dans la version actuelle du bot
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


def run():
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv("BTC/USDC", timeframe="1m", limit=200)

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
    # bb_haute = df["bb_haute"].iloc[-1]
    # bb_basse = df["bb_basse"].iloc[-1]
    ema200 = df["ema200"].iloc[-1]
    ema50 = df["ema50"].iloc[-1]


    support_area = (80832.78, 80970.30)
    # resistance_area = (X, X)
    in_zone = support_area[0] <= price <= support_area[1]
    # in_zone = resistance_area[0] <= price <= resistance_area[1]

    score = calcul_score(in_zone, rsi, ema50, ema200)


    print(f"Price : {price}")
    print(f"Key Level : {support_area}")
    print(f"RSI : {rsi}")
    print(f"Score : {score}")

    if score >= 4:
        print("PRICE IN ZONE AND RSI OVERSOLD, STRONG SIGNAL")
    elif score >= 2:
        print("PRICE IN ZONE, WAITING FOR RSI")
    else:
        print("NO TRADE")

def main():
    while True:
        try:
            run()
        except Exception as e:
            print("ERROR : ", e)

        time.sleep(60)



if __name__ == "__main__":
    main()