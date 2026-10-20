"""
╔══════════════════════════════════════════════════════════════╗
║       STOCK PORTFOLIO PERFORMANCE TRACKER — Task 2          ║
║       Datheon Python Programming Internship                  ║
╚══════════════════════════════════════════════════════════════╝

Description:
    An investment portfolio tracking utility that lets users enter
    stock ticker symbols, buy prices, and share quantities.
    It computes total portfolio value, percentage gain/loss per
    holding, and logs the transaction summary to portfolio_summary.csv.
    Word list is sourced from the full S&P 500 constituents.csv file.

Author  : Datheon Internship Submission
Language: Python 3
Modules : csv, os, sys, datetime, random (Standard Library only)
"""

import csv
import os
import sys
import random
from datetime import datetime


# ─────────────────────────────────────────────────────────────
#  SIMULATED MARKET PRICES
#  Realistic reference prices for popular S&P 500 tickers.
#  These act as "current market prices" when live data
#  (yfinance / requests) is not available.
# ─────────────────────────────────────────────────────────────
SIMULATED_PRICES = {
    "AAPL":  189.30,  "MSFT":  415.50,  "GOOGL": 175.80,
    "AMZN":  185.20,  "NVDA":  875.40,  "TSLA":  248.50,
    "META":  505.60,  "BRK.B": 395.20,  "JPM":   198.75,
    "V":     275.30,  "JNJ":   152.40,  "WMT":   68.90,
    "PG":    162.50,  "MA":    468.20,  "HD":    355.80,
    "CVX":   158.30,  "MRK":   127.60,  "ABBV":  172.40,
    "PEP":   171.20,  "KO":    60.45,   "AVGO":  1420.00,
    "COST":  875.30,  "MCD":   295.60,  "NFLX":  628.40,
    "ADBE":  485.20,  "CRM":   315.70,  "CSCO":  48.30,
    "ACN":   342.80,  "PFE":   28.15,   "LLY":   785.60,
    "TMO":   562.40,  "DHR":   248.90,  "ABT":   112.35,
    "NKE":   94.20,   "DIS":   112.80,  "INTC":  42.60,
    "AMD":   168.90,  "QCOM":  168.40,  "TXN":   178.50,
    "NEE":   72.30,   "UNH":   518.90,  "RTX":   103.50,
    "GE":    162.70,  "CAT":   348.20,  "BA":    215.40,
    "IBM":   192.30,  "ORCL":  125.60,  "PYPL":  68.40,
    "UBER":  77.30,   "SPOT":  318.90,  "SQ":    78.50,
}

CSV_FILENAME        = "portfolio_summary.csv"
CONSTITUENTS_FILE   = "constituents.csv"
SEPARATOR           = "=" * 70
THIN_SEPARATOR      = "-" * 70


# ─────────────────────────────────────────────────────────────
#  LOAD S&P 500 CONSTITUENTS
#  Reads constituents.csv and returns a lookup dict.
# ─────────────────────────────────────────────────────────────
def load_sp500_constituents(filename: str = CONSTITUENTS_FILE) -> dict:
    """
    Load all S&P 500 tickers from constituents.csv.

    Expected CSV columns:
        Symbol, Security, GICS Sector, GICS Sub-Industry,
        Headquarters Location, Date added, CIK, Founded

    Returns:
        dict keyed by ticker symbol:
        {
            "AAPL": {
                "name":         "Apple Inc.",
                "sector":       "Information Technology",
                "sub_industry": "Technology Hardware ...",
            },
            ...
        }
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath   = os.path.join(script_dir, filename)
    constituents = {}

    try:
        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                symbol = row.get("Symbol", "").strip().upper()
                if symbol:
                    constituents[symbol] = {
                        "name":         row.get("Security", "N/A").strip(),
                        "sector":       row.get("GICS Sector", "N/A").strip(),
                        "sub_industry": row.get("GICS Sub-Industry", "N/A").strip(),
                        "hq":           row.get("Headquarters Location", "N/A").strip(),
                        "founded":      row.get("Founded", "N/A").strip(),
                    }
        print(f"  [OK]  Loaded {len(constituents)} S&P 500 tickers from '{filename}'.")
    except FileNotFoundError:
        print(f"  [!]   '{filename}' not found. Ticker lookup info will be unavailable.")
    except Exception as e:
        print(f"  [!]   Error reading '{filename}': {e}")

    return constituents


# Load S&P 500 data once at startup
SP500 = load_sp500_constituents()


# ─────────────────────────────────────────────────────────────
#  UTILITY — CLEAR SCREEN
# ─────────────────────────────────────────────────────────────
def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


# ─────────────────────────────────────────────────────────────
#  UTILITY — DISPLAY HEADER
# ─────────────────────────────────────────────────────────────
def display_header() -> None:
    clear_screen()
    print(SEPARATOR)
    print("   STOCK PORTFOLIO PERFORMANCE TRACKER")
    print("   Datheon Python Programming Internship — Task 2")
    print(f"   {datetime.now().strftime('%A, %d %B %Y  |  %I:%M %p')}")
    print(SEPARATOR)


# ─────────────────────────────────────────────────────────────
#  UTILITY — GET CURRENT PRICE
#  Tries yfinance first; falls back to simulated prices.
# ─────────────────────────────────────────────────────────────
def get_current_price(ticker: str) -> float | None:
    """
    Fetch the current market price for a ticker symbol.

    Strategy:
        1. Try yfinance (live price) if installed.
        2. Fallback: look up SIMULATED_PRICES dictionary.
        3. If still not found, return None.

    Args:
        ticker: Stock ticker symbol (e.g. 'AAPL').

    Returns:
        Current price as float, or None if unavailable.
    """
    ticker = ticker.upper()

    # --- Attempt live price via yfinance ---
    try:
        import yfinance as yf
        data = yf.Ticker(ticker)
        price = data.fast_info.get("last_price") or data.fast_info.get("regularMarketPrice")
        if price and price > 0:
            return round(float(price), 2)
    except Exception:
        pass  # yfinance not installed or network error — use simulation

    # --- Fallback: simulated price with small random drift ---
    if ticker in SIMULATED_PRICES:
        base  = SIMULATED_PRICES[ticker]
        drift = random.uniform(-0.02, 0.02)   # ±2 % daily fluctuation
        return round(base * (1 + drift), 2)

    return None


# ─────────────────────────────────────────────────────────────
#  UTILITY — INPUT HELPERS
# ─────────────────────────────────────────────────────────────
def input_float(prompt: str, min_val: float = 0.0) -> float:
    """Prompt until a valid positive float is entered."""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            if value <= min_val:
                print(f"   [!] Value must be greater than {min_val}. Try again.\n")
                continue
            return value
        except ValueError:
            print(f"   [!] '{raw}' is not a valid number. Try again.\n")


def input_int(prompt: str, min_val: int = 1) -> int:
    """Prompt until a valid positive integer is entered."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if value < min_val:
                print(f"   [!] Value must be at least {min_val}. Try again.\n")
                continue
            return value
        except ValueError:
            print(f"   [!] '{raw}' is not a valid integer. Try again.\n")


def input_ticker(prompt: str) -> str:
    """Prompt until a valid alphabetic ticker is entered."""
    while True:
        raw = input(prompt).strip().upper()
        if raw and all(c.isalpha() or c == "." for c in raw):
            return raw
        print(f"   [!] '{raw}' is not a valid ticker. Use letters only (e.g. AAPL).\n")


# ─────────────────────────────────────────────────────────────
#  CORE — ADD STOCK HOLDING
# ─────────────────────────────────────────────────────────────
def add_holding(portfolio: dict) -> None:
    """
    Prompt user for a stock holding and add it to the portfolio.

    Portfolio structure:
        {
            "AAPL": {
                "ticker":     "AAPL",
                "name":       "Apple Inc.",
                "shares":     10,
                "buy_price":  150.00,
                "current_price": 189.30,
            },
            ...
        }
    """
    print(f"\n{THIN_SEPARATOR}")
    print("  ADD NEW STOCK HOLDING")
    print(THIN_SEPARATOR)

    ticker = input_ticker("  Ticker Symbol (e.g. AAPL, MSFT): ")

    # Show company info from S&P 500 list if available
    if ticker in SP500:
        info = SP500[ticker]
        print(f"\n  Company      : {info['name']}")
        print(f"  Sector       : {info['sector']}")
        print(f"  Sub-Industry : {info['sub_industry']}")
        print(f"  HQ           : {info['hq']}")
    else:
        print(f"\n  [i] '{ticker}' is not in the S&P 500 list — you can still add it manually.")

    if ticker in portfolio:
        print(f"\n  [!] {ticker} is already in your portfolio.")
        update = input("  Update existing holding? (y/n): ").strip().lower()
        if update != "y":
            return

    buy_price = input_float(f"  Buy Price per share for {ticker} ($): ")
    shares    = input_int(f"  Number of shares purchased: ")

    print(f"\n  Fetching current market price for {ticker}...")
    current_price = get_current_price(ticker)

    if current_price is None:
        print(f"  [!] Could not fetch price for '{ticker}'. Enter manually.")
        current_price = input_float(f"  Current Market Price for {ticker} ($): ")
    else:
        print(f"  Current Price: ${current_price:,.2f}")

    company_name = SP500[ticker]["name"] if ticker in SP500 else ticker
    portfolio[ticker] = {
        "ticker":        ticker,
        "name":          company_name,
        "shares":        shares,
        "buy_price":     buy_price,
        "current_price": current_price,
    }

    print(f"\n  [OK] {ticker} added to portfolio successfully!")


# ─────────────────────────────────────────────────────────────
#  CORE — REMOVE STOCK HOLDING
# ─────────────────────────────────────────────────────────────
def remove_holding(portfolio: dict) -> None:
    """Remove a stock from the portfolio by ticker symbol."""
    if not portfolio:
        print("\n  [!] Portfolio is empty. Nothing to remove.")
        return

    print(f"\n{THIN_SEPARATOR}")
    ticker = input("  Enter ticker to remove: ").strip().upper()

    if ticker in portfolio:
        del portfolio[ticker]
        print(f"  [OK] {ticker} removed from portfolio.")
    else:
        print(f"  [!] {ticker} not found in portfolio.")


# ─────────────────────────────────────────────────────────────
#  CORE — REFRESH PRICES
# ─────────────────────────────────────────────────────────────
def refresh_prices(portfolio: dict) -> None:
    """Refresh current market prices for all holdings."""
    if not portfolio:
        print("\n  [!] Portfolio is empty.")
        return

    print(f"\n  Refreshing prices for {len(portfolio)} holding(s)...")
    for ticker, data in portfolio.items():
        new_price = get_current_price(ticker)
        if new_price:
            data["current_price"] = new_price
    print("  [OK] Prices refreshed!")


# ─────────────────────────────────────────────────────────────
#  CORE — CALCULATE METRICS
# ─────────────────────────────────────────────────────────────
def calculate_metrics(holding: dict) -> dict:
    """
    Compute performance metrics for a single holding.

    Returns a dict with:
        invested      — total amount paid (shares × buy_price)
        current_value — current worth (shares × current_price)
        gain_loss     — profit or loss in dollars
        gain_loss_pct — profit or loss as a percentage
    """
    shares        = holding["shares"]
    buy_price     = holding["buy_price"]
    current_price = holding["current_price"]

    invested      = shares * buy_price
    current_value = shares * current_price
    gain_loss     = current_value - invested
    gain_loss_pct = (gain_loss / invested * 100) if invested else 0.0

    return {
        "invested":      round(invested,      2),
        "current_value": round(current_value, 2),
        "gain_loss":     round(gain_loss,     2),
        "gain_loss_pct": round(gain_loss_pct, 2),
    }


# ─────────────────────────────────────────────────────────────
#  CORE — DISPLAY PORTFOLIO TABLE
# ─────────────────────────────────────────────────────────────
def display_portfolio(portfolio: dict) -> None:
    """Print a formatted, colour-coded portfolio performance table."""
    display_header()

    if not portfolio:
        print("\n  Portfolio is empty. Add some stocks first!\n")
        return

    # ── Table Header ─────────────────────────────────────────
    print(f"\n  {'TICKER':<8} {'COMPANY':<22} {'SHARES':>6} {'BUY($)':>10} "
          f"{'CURR($)':>10} {'INVESTED':>12} {'CURR VALUE':>12} "
          f"{'GAIN/LOSS':>12} {'%':>8}")
    print("  " + THIN_SEPARATOR)

    total_invested = 0.0
    total_value    = 0.0
    total_gain     = 0.0

    rows = []

    for ticker, holding in portfolio.items():
        m = calculate_metrics(holding)

        total_invested += m["invested"]
        total_value    += m["current_value"]
        total_gain     += m["gain_loss"]

        # Sign indicators
        sign  = "+" if m["gain_loss"] >= 0 else ""
        arrow = "[UP]  " if m["gain_loss"] >= 0 else "[DOWN]"
        name  = holding.get("name", ticker)[:20]   # truncate long names

        row = (
            f"  {ticker:<8} "
            f"{name:<22} "
            f"{holding['shares']:>6} "
            f"{holding['buy_price']:>10.2f} "
            f"{holding['current_price']:>10.2f} "
            f"{m['invested']:>12,.2f} "
            f"{m['current_value']:>12,.2f} "
            f"{sign}{m['gain_loss']:>11,.2f} "
            f"{sign}{m['gain_loss_pct']:>7.2f}%  {arrow}"
        )
        rows.append(row)

    for row in rows:
        print(row)

    # ── Totals Footer ─────────────────────────────────────────
    total_pct  = (total_gain / total_invested * 100) if total_invested else 0.0
    sign_total = "+" if total_gain >= 0 else ""
    status     = "[PROFIT]" if total_gain >= 0 else "[LOSS]  "

    print("  " + THIN_SEPARATOR)
    print(f"\n  PORTFOLIO SUMMARY")
    print(THIN_SEPARATOR)
    print(f"  Total Invested        : ${total_invested:>12,.2f}")
    print(f"  Total Current Value   : ${total_value:>12,.2f}")
    print(f"  Total Gain / Loss     : {sign_total}${abs(total_gain):>11,.2f}  "
          f"({sign_total}{total_pct:.2f}%)  {status}")
    print(f"  Holdings Count        : {len(portfolio)}")
    print(f"  Snapshot Time         : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(SEPARATOR + "\n")


# ─────────────────────────────────────────────────────────────
#  CORE — SAVE TO CSV
# ─────────────────────────────────────────────────────────────
def save_to_csv(portfolio: dict, filename: str = CSV_FILENAME) -> None:
    """
    Write the full portfolio summary to a CSV file.

    CSV columns:
        Timestamp, Ticker, Shares, Buy_Price, Current_Price,
        Invested, Current_Value, Gain_Loss, Gain_Loss_Pct

    Each save APPENDS a new snapshot block (with timestamp) so the
    file builds a historical performance log over time.
    """
    if not portfolio:
        print("\n  [!] Portfolio is empty. Nothing to save.")
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath   = os.path.join(script_dir, filename)

    file_exists = os.path.isfile(filepath)

    fieldnames = [
        "Timestamp", "Ticker", "Company", "Shares",
        "Buy_Price", "Current_Price",
        "Invested", "Current_Value",
        "Gain_Loss", "Gain_Loss_Pct(%)"
    ]

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(filepath, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header only on first creation
        if not file_exists:
            writer.writeheader()

        # Write a blank separator line between sessions
        if file_exists:
            csvfile.write("\n")

        for ticker, holding in portfolio.items():
            m = calculate_metrics(holding)
            writer.writerow({
                "Timestamp":        timestamp,
                "Ticker":           ticker,
                "Company":          holding.get("name", ticker),
                "Shares":           holding["shares"],
                "Buy_Price":        f"{holding['buy_price']:.2f}",
                "Current_Price":    f"{holding['current_price']:.2f}",
                "Invested":         f"{m['invested']:.2f}",
                "Current_Value":    f"{m['current_value']:.2f}",
                "Gain_Loss":        f"{m['gain_loss']:.2f}",
                "Gain_Loss_Pct(%)": f"{m['gain_loss_pct']:.2f}",
            })

    print(f"\n  [OK] Portfolio saved to '{filename}'")
    print(f"       Path: {filepath}\n")


# ─────────────────────────────────────────────────────────────
#  CORE — VIEW CSV LOG
# ─────────────────────────────────────────────────────────────
def view_csv_log(filename: str = CSV_FILENAME) -> None:
    """Display the contents of the saved CSV log file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath   = os.path.join(script_dir, filename)

    if not os.path.isfile(filepath):
        print(f"\n  [!] No log file found. Save your portfolio first.\n")
        return

    print(f"\n  === CONTENTS OF {filename} ===\n")
    with open(filepath, "r", encoding="utf-8") as f:
        print(f.read())


# ─────────────────────────────────────────────────────────────
#  CORE — SHOW SUPPORTED TICKERS
# ─────────────────────────────────────────────────────────────
def show_supported_tickers() -> None:
    """Print all S&P 500 tickers from constituents.csv grouped by sector."""
    print(f"\n{THIN_SEPARATOR}")
    print("  S&P 500 TICKER LIST  (source: constituents.csv)")
    print(THIN_SEPARATOR)

    if SP500:
        # Group by sector
        sectors: dict = {}
        for symbol, info in SP500.items():
            sec = info["sector"]
            sectors.setdefault(sec, []).append(symbol)

        for sector, symbols in sorted(sectors.items()):
            print(f"\n  [{sector}] — {len(symbols)} stocks")
            for i in range(0, len(symbols), 10):
                row = "  ".join(f"{s:<6}" for s in sorted(symbols)[i:i+10])
                print(f"    {row}")

        print(f"\n  Total S&P 500 tickers loaded : {len(SP500)}")
    else:
        # Fallback to simulated prices list
        print("  [!] constituents.csv not loaded. Showing built-in tickers:")
        tickers = list(SIMULATED_PRICES.keys())
        for i in range(0, len(tickers), 8):
            row = "  ".join(f"{t:<6}" for t in tickers[i:i+8])
            print(f"  {row}")
        print(f"\n  Total: {len(tickers)} tickers")

    print(f"\n  Note: Prices fetched via yfinance (live) or simulated (fallback).\n")


# ─────────────────────────────────────────────────────────────
#  CORE — MAIN MENU
# ─────────────────────────────────────────────────────────────
def main_menu(portfolio: dict) -> None:
    """Display the main menu."""
    display_header()
    holdings_count = len(portfolio)
    print(f"\n  Holdings in portfolio: {holdings_count}\n")
    print("  MAIN MENU")
    print(THIN_SEPARATOR)
    print("  [1]  Add / Update Stock Holding")
    print("  [2]  View Portfolio Performance Table")
    print("  [3]  Refresh Market Prices")
    print("  [4]  Save Portfolio to CSV (portfolio_summary.csv)")
    print("  [5]  View Saved CSV Log")
    print("  [6]  Remove a Holding")
    print("  [7]  Show Supported Tickers")
    print("  [8]  Exit")
    print()


# ─────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────
def main() -> None:
    """Program entry point — orchestrates the portfolio tracker loop."""
    portfolio: dict = {}

    while True:
        main_menu(portfolio)

        try:
            choice = input("  Select an option (1-8): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  Goodbye!\n")
            sys.exit(0)

        if choice == "1":
            add_holding(portfolio)
            input("\n  Press ENTER to return to menu...")

        elif choice == "2":
            display_portfolio(portfolio)
            input("  Press ENTER to return to menu...")

        elif choice == "3":
            refresh_prices(portfolio)
            input("\n  Press ENTER to return to menu...")

        elif choice == "4":
            save_to_csv(portfolio)
            input("  Press ENTER to return to menu...")

        elif choice == "5":
            view_csv_log()
            input("  Press ENTER to return to menu...")

        elif choice == "6":
            remove_holding(portfolio)
            input("\n  Press ENTER to return to menu...")

        elif choice == "7":
            show_supported_tickers()
            input("  Press ENTER to return to menu...")

        elif choice == "8":
            if portfolio:
                save = input("\n  Save portfolio before exiting? (y/n): ").strip().lower()
                if save == "y":
                    save_to_csv(portfolio)
            print("\n  Thank you for using the Portfolio Tracker! Goodbye!\n")
            sys.exit(0)

        else:
            print("\n  [!] Invalid option. Please enter a number between 1 and 8.\n")
            input("  Press ENTER to continue...")


if __name__ == "__main__":
    main()
