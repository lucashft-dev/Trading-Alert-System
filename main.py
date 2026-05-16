import time
from indicators.indicators import fetch_market_data, calculate_indicators
from strategy.strategy import calculate_score, get_signal
from utils.logger import console_log
from config.config import SYMBOLE, TIMEFRAME, SETUP_TYPE, ENTRY_ZONE, LIQUIDITY_LEVEL



def main():
    last_signal = None
    while True:
        try:
            df = fetch_market_data()
            price, rsi, bb_haute, bb_basse, last_lows, last_highs, ema200, ema50 = calculate_indicators(df)
            score = calculate_score(price, SETUP_TYPE, ENTRY_ZONE, rsi, LIQUIDITY_LEVEL, last_lows, last_highs, bb_basse, bb_haute, ema50, ema200)
            signal = get_signal(score)
            # Pour afficher dans la console seulement si nouveau signal détecté :
            # if signal != last_signal:
            #     last_signal = signal
            #     console_log(price, ENTRY_ZONE, rsi, score, signal)
            # Ici j'affiche toutes les 60 secondes car pratique pour debug
            console_log(price, ENTRY_ZONE, rsi, score, signal)
        except Exception as e:
            print("ERROR : ", e)

        time.sleep(60)



if __name__ == "__main__":
    main()