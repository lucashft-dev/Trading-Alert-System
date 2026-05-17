import time
from datetime import datetime


def wait_for_next_candle(timeframe):

    timeframe_seconds = {
        "1m": 60,
        "5m": 300,
        "15m": 900,
        "1h": 3600
    }

    candle_time = timeframe_seconds[timeframe]

    now = time.time()

    sleep_time = candle_time - (now % candle_time)

    print(f"Sleeping {sleep_time:.0f}s until next candle close...")
    time.sleep(sleep_time + 1)