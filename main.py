import time
from indicators.indicators import fetch_market_data, calculate_indicators
from strategy.strategy import calculate_score, get_signal
from utils.console_logger import console_log
from config.config import SYMBOLE, TIMEFRAME, SETUP_TYPE, ENTRY_ZONE, LIQUIDITY_LEVEL
from notif.telegram import send_telegram_message, format_telegram_message
from utils.csv_logger import log_signal
from utils.time_sync import wait_for_next_candle



def main():
    last_signal = None
    last_logged_signal = None
    while True:
        try:
            df = fetch_market_data()
            price, rsi, bb_haute, bb_basse, last_low, last_high, last_close, ema200, ema50 = calculate_indicators(df)
            score = calculate_score(price, SETUP_TYPE, ENTRY_ZONE, rsi, LIQUIDITY_LEVEL, last_low, last_high, last_close, bb_basse, bb_haute, ema50, ema200)
            signal = get_signal(score)
            # Pour afficher dans la console seulement si nouveau signal détecté :
            # if signal != last_signal:
            #     last_signal = signal
            #     console_log(price, ENTRY_ZONE, rsi, score, signal)
            # Ici j'affiche toutes les 60 secondes car pratique pour debug (facultatif)
            console_log(price, ENTRY_ZONE, rsi, score, signal)
            if signal == "STRONG SETUP":
                message = format_telegram_message(SYMBOLE=SYMBOLE,
                                                  price=price,
                                                  rsi=rsi,
                                                  score=score, 
                                                  entry_zone=ENTRY_ZONE,
                                                  setup_type=SETUP_TYPE,
                                                  timeframe=TIMEFRAME,
                                                  liquidity_level=LIQUIDITY_LEVEL,
                                                  ema50=ema50, 
                                                  ema200=ema200)
                send_telegram_message(message)

            # Log seulement si on a un setup fort (à modifier en fonction des préférences, ici 8)
            # A moyen / long terme, on pourra analyser et améliorer
            if signal != last_logged_signal and score >= 8:
                log_signal(symbol=SYMBOLE, timeframe=TIMEFRAME, setup_type=SETUP_TYPE, signal=signal, score=score, price=price, rsi=rsi)
                last_logged_signal = signal
        except Exception as e:
            print("ERROR : ", e)

        wait_for_next_candle(TIMEFRAME)



if __name__ == "__main__":
    main()