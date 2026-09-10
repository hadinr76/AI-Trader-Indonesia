from risk.trade_cost_engine import TradeCostEngine

print("=" * 60)
print("TRADE COST ENGINE TEST")
print("=" * 60)

result = TradeCostEngine.calculate(

    entry_price=5000,

    exit_price=5500,

    shares=10000

)

print()

for k, v in result.items():

    print(f"{k:<18}: {v}")

print()

print("=" * 60)
print("TRADE COST ENGINE TEST SELESAI")