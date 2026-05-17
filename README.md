# 📊 Trading Setup Analysis System (Python + CCXT + Price Action)

## 🧠 Overview

This project is a modular trading signal engine built in Python.  
It combines technical indicators, liquidity concepts, and price action patterns to generate structured trading setups and alerts.

The goal is not to execute trades automatically, but to build a **research and signal generation system** that can later be evaluated and optimized for my personal trading.

---

## ⚙️ Features

- 📡 Live market data via CCXT (Binance)
- 📊 Technical indicators (TA-Lib):
- RSI
- Bollinger Bands
- EMA 50 / EMA 200
- 📍 Zone-based setup detection (support / resistance)
- 💧 Liquidity concept (sweep detection)
- 🕯️ Price action patterns:
- Hammer (bullish rejection candle)
- Shooting star (bearish rejection candle)
- Rejection logic (sweep + reclaim)
- 🧮 Custom scoring system for trade setups
- 📲 Telegram notifications for high-quality setups
- 📁 CSV logging for post-analysis
- 📊 Analytics module for strategy evaluation

---

## 🏗️ Project Structure

- `/indicators` → market data + indicators calculation  
- `/strategy` → scoring system + signal logic  
- `/utils` → logging utilities and time sync
- `/notif` → Telegram integration  
- `/config` → configuration (pairs, zones, settings)  
- `analytics/` → strategy analysis scripts  
- `main.py` → main execution loop  


---

## 🧮 Strategy Logic

The system evaluates potential trade setups using a scoring model based on:

### LONG conditions:
- Price inside defined support zone
- RSI oversold
- Liquidity sweep below support
- Bullish rejection or hammer candle
- EMA / Bollinger Band confluence

### SHORT conditions:
- Price inside resistance zone
- RSI overbought
- Liquidity sweep above resistance
- Bearish rejection or shooting star candle
- EMA / Bollinger Band confluence

Each condition adds to a **global score**, which determines signal strength.

---

## 📈 Signal Types

- `NONE` → no setup
- `POTENTIAL SETUP` → moderate setup, waiting for more indicators
- `STRONG SETUP` → high probability and confluence setup

---

## 📊 Analytics

The project includes a basic analytics module that allows:

- Setup frequency analysis
- Score distribution
- RSI statistics
- Long vs Short ratio
- Historical signal tracking (CSV logs)

Future improvements include:
- Win/Loss tracking
- Backtesting engine
- Strategy optimization

---

## 📦 Tech Stack

- Python
- CCXT (exchange data)
- Pandas
- TA-Lib
- Telegram Bot API

---

## 🚀 Future Improvements

- Trade outcome tracking (WIN / LOSS)
- Backtesting module
- Multi-timeframe analysis
- Multi-asset scanning
- Strategy optimization based on historical data
- Advanced price action detection (engulfing, structure breaks)

---

## ⚠️ Disclaimer

This project is for educational and research purposes only.  
It does not constitute financial advice and does not guarantee profitability.

---

## 👨‍💻 Author

Built as a tool i will use for my trading on Hyperliquid. Learning project focused on trading systems and data analysis.