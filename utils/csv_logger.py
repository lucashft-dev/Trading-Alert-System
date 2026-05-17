import csv
import os
from datetime import datetime


def log_signal(symbol, timeframe, setup_type, signal, score, price, rsi):

    file_path = "logs/signals.csv"
    file_exists = os.path.isfile(file_path)

    with open(file_path, mode="a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["timestamp", "symbol", "timeframe", "setup_type", "signal", "score", "price", "rsi"])

        writer.writerow([
            datetime.now(),
            symbol,
            timeframe,
            setup_type,
            signal,
            score,
            round(price, 2),
            round(rsi, 2)
        ])