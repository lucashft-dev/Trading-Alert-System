from datetime import datetime



def console_log(price, entry_zone, rsi, score, signal):
    now = datetime.now().strftime("%H:%M:%S")

    print("=" * 40)
    print(f"{now}")
    print(f"Price: {price:.2f}")
    print(f"Entry Zone: {entry_zone}")
    print(f"RSI: {rsi:.2f}")
    print(f"Score: {score}")
    print(f"Signal: {signal}")
    print("=" * 40)