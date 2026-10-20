# 📈 Task 2 — Stock Portfolio Performance Tracker

> **Datheon Python Programming Internship** | Task 2 of 4

---

## 📋 Overview

A terminal-based **investment portfolio tracking utility** written in pure Python 3.  
Users enter stock ticker symbols, buy prices, and share quantities.  
The program computes **total portfolio value**, **percentage gain/loss per holding**,  
and automatically logs the transaction summary to **`portfolio_summary.csv`**.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📥 Add Holdings | Enter ticker, buy price, and shares — simple guided prompts |
| 💰 Live Price Fetch | Tries `yfinance` (if installed), else uses realistic simulated prices |
| 📊 Performance Table | Formatted table: Invested, Current Value, Gain/Loss, % per holding |
| 📂 CSV Export | Appends snapshot to `portfolio_summary.csv` with timestamp |
| 🕰️ Historical Log | Every save session is appended — builds a performance history |
| 🔄 Price Refresh | Re-fetch current market prices for all holdings |
| ❌ Remove Holding | Delete any stock from the portfolio |
| 🗂️ View CSV Log | View saved CSV log directly from the app |
| 📋 Ticker Reference | Built-in list of 50+ S&P 500 tickers with simulated prices |
| 🛡️ Input Validation | All inputs validated — no crashes on bad data |

---

## 🚀 How to Run

```bash
# Navigate to the project folder
cd "task 2"

# Run the tracker
python portfolio.py
```

> **Requirements**: Python 3.10+  
> **Optional**: `pip install yfinance` for live stock prices  
> **Standard Library Only**: Works without yfinance using simulated prices

---

## 🎮 Usage Walkthrough

```
MAIN MENU
──────────────────────────────────────────────────────────────────────
[1]  Add / Update Stock Holding
[2]  View Portfolio Performance Table
[3]  Refresh Market Prices
[4]  Save Portfolio to CSV (portfolio_summary.csv)
[5]  View Saved CSV Log
[6]  Remove a Holding
[7]  Show Supported Tickers
[8]  Exit
```

### Example Session
```
  Ticker Symbol: AAPL
  Buy Price per share: 150.00
  Number of shares: 10

  Fetching current market price for AAPL...
  Current Price: $189.30

  [OK] AAPL added to portfolio!
```

### Portfolio Table Output
```
  TICKER   SHARES    BUY($)   CURR($)     INVESTED  CURR VALUE    GAIN/LOSS       %
  ──────────────────────────────────────────────────────────────────────────────────
  AAPL          10    150.00    189.30     1,500.00    1,893.00      +393.00  +26.20%  [UP]
  MSFT           5    380.00    415.50     1,900.00    2,077.50      +177.50   +9.34%  [UP]
  TSLA          20    210.00    248.50     4,200.00    4,970.00      +770.00  +18.33%  [UP]
```

---

## 📁 Project Structure

```
task 2/
│
├── portfolio.py          ← Main portfolio tracker script
├── sp500_tickers.csv     ← S&P 500 reference ticker dataset (51 stocks)
├── portfolio_summary.csv ← Auto-generated on first save (log file)
└── README.md             ← This file
```

---

## 🔧 Technical Implementation

| Aspect | Implementation |
|---|---|
| Data Structure | Python `dict` — `{ticker: {shares, buy_price, current_price}}` |
| Price Fetching | `yfinance` (live) → simulated dict (fallback) → manual entry |
| Gain/Loss Calc | `(current_value - invested) / invested * 100` |
| CSV Writing | Python `csv.DictWriter` — appends with timestamp headers |
| Input Safety | `isalpha()`, `float()`, `int()` with re-prompt loops |
| File I/O | `os.path` for cross-platform file resolution |

---

## 📊 CSV Output Format (`portfolio_summary.csv`)

```csv
Timestamp,Ticker,Shares,Buy_Price,Current_Price,Invested,Current_Value,Gain_Loss,Gain_Loss_Pct(%)
2026-10-20 14:30:00,AAPL,10,150.00,189.30,1500.00,1893.00,393.00,26.20
2026-10-20 14:30:00,MSFT,5,380.00,415.50,1900.00,2077.50,177.50,9.34
```

---

## 📌 Notes

- All core logic uses only the **Python Standard Library** (`csv`, `os`, `sys`, `datetime`, `random`).
- `yfinance` is **optional** — install with `pip install yfinance` for real-time prices.
- Without `yfinance`, realistic simulated prices with ±2% random drift are used.
- The `sp500_tickers.csv` file serves as a reference for available tickers.

---

*Submitted as part of the Datheon Python Programming Internship.*
