import os
import requests
from dotenv import load_dotenv

load_dotenv("config/.env")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_message(message: str):

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }

    requests.post(url, data=data)



def format_telegram_message(SYMBOLE, price, rsi, score, entry_zone, setup_type, timeframe, liquidity_level, ema50, ema200):

    zone_low = entry_zone[0]
    zone_high = entry_zone[1]

    message = f"""
🚨 TRADING OPPORTUNITY DETECTED ({setup_type})

🔥 {f"{SYMBOLE}"}
⏱ Timeframe: {timeframe}

💰 Price : {price:.2f}
📍 Entry Zone : {zone_low:.2f} → {zone_high:.2f}
📊 RSI : {rsi:.2f}

⭐ Score : {score}

━━━━━━━━━━━━━━
📈 Context :
- Looking for a {setup_type} setup.
- Market in Zone : {"YES" if zone_low <= price <= zone_high else "NO"}
- RSI condition : {"OVERSOLD" if rsi < 30 else "OVERBOUGHT" if rsi > 70 else "NEUTRAL"}
- Liquidity level : {"TAKEN" if (price <= liquidity_level and setup_type == "LONG") or (price >= liquidity_level and setup_type == "SHORT") else "NOT TAKEN"}
- EMA50 vs EMA200 : {"BULLISH" if ema50 > ema200 else "BEARISH"}
━━━━━━━━━━━━━━

📡 Crypto Trading Alert System Bot
"""

    return message