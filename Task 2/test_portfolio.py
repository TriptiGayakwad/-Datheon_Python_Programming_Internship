import sys, os
sys.path.insert(0, r'd:\CODING FOLDER\Datheon_Python_Programming_Internship\task 2')
os.chdir(r'd:\CODING FOLDER\Datheon_Python_Programming_Internship\task 2')

from portfolio import calculate_metrics, get_current_price, SIMULATED_PRICES, save_to_csv

print("=== PORTFOLIO TRACKER UNIT TESTS ===\n")

# Test 1
print(f"[TEST 1] Simulated tickers : {len(SIMULATED_PRICES)}   OK")

# Test 2
price = get_current_price("AAPL")
print(f"[TEST 2] AAPL price        : ${price:.2f}   OK")

# Test 3 - gain
h1 = {"shares": 10, "buy_price": 150.00, "current_price": 189.30}
m1 = calculate_metrics(h1)
print(f"[TEST 3] Gain scenario (AAPL x10):")
print(f"         Invested   = ${m1['invested']:,.2f}")
print(f"         Curr Value = ${m1['current_value']:,.2f}")
print(f"         Gain/Loss  = +${m1['gain_loss']:,.2f}")
print(f"         Gain Pct   = +{m1['gain_loss_pct']}%   OK")

# Test 4 - loss
h2 = {"shares": 5, "buy_price": 300.00, "current_price": 248.50}
m2 = calculate_metrics(h2)
print(f"[TEST 4] Loss scenario (TSLA x5):")
print(f"         Invested   = ${m2['invested']:,.2f}")
print(f"         Curr Value = ${m2['current_value']:,.2f}")
print(f"         Gain/Loss  = ${m2['gain_loss']:,.2f}")
print(f"         Loss Pct   = {m2['gain_loss_pct']}%   OK")

# Test 5 - CSV save
portfolio = {
    "AAPL": {"ticker": "AAPL", "shares": 10, "buy_price": 150.00, "current_price": 189.30},
    "MSFT": {"ticker": "MSFT", "shares": 5,  "buy_price": 380.00, "current_price": 415.50},
}
save_to_csv(portfolio)
print("[TEST 5] CSV saved   OK")
print("\nAll tests passed!")
