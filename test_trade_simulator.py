from backtest.trade_simulator import TradeSimulator
import pandas as pd

print("=" * 60)
print("TRADE SIMULATOR TEST")
print("=" * 60)

# =====================================================
# TEST 1 : TARGET 1
# =====================================================

print()
print("TEST 1 : TARGET 1")

data = pd.DataFrame({

    "High": [5100, 5300, 5450, 5500],
    "Low": [4950, 5050, 5200, 5300],
    "Close": [5050, 5250, 5400, 5450]

})

result = TradeSimulator.simulate(

    data=data,

    entry_price=5000,

    stop_loss=4800,

    target1=5400,

    target2=5700,

    shares=10000,

    lots=100

)

for k, v in result.items():
    print(f"{k:15} : {v}")

# =====================================================
# TEST 2 : STOP LOSS
# =====================================================

print()
print("=" * 60)
print("TEST 2 : STOP LOSS")

data = pd.DataFrame({

    "High": [5050, 5020, 5000],
    "Low": [4950, 4850, 4750],
    "Close": [5000, 4900, 4800]

})

result = TradeSimulator.simulate(

    data=data,

    entry_price=5000,

    stop_loss=4800,

    target1=5400,

    target2=5700,

    shares=10000,

    lots=100

)

for k, v in result.items():
    print(f"{k:15} : {v}")

# =====================================================
# TEST 3 : OPEN
# =====================================================

print()
print("=" * 60)
print("TEST 3 : OPEN")

data = pd.DataFrame({

    "High": [5050, 5080, 5100],
    "Low": [4950, 5000, 5020],
    "Close": [5030, 5060, 5090]

})

result = TradeSimulator.simulate(

    data=data,

    entry_price=5000,

    stop_loss=4800,

    target1=5400,

    target2=5700,

    shares=10000,

    lots=100

)

for k, v in result.items():
    print(f"{k:15} : {v}")

print()
print("=" * 60)
print("TRADE SIMULATOR TEST SELESAI")
print("=" * 60)