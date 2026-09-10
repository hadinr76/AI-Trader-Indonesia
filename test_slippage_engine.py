from risk.slippage_engine import SlippageEngine

print("=" * 60)
print("SLIPPAGE ENGINE TEST")
print("=" * 60)

buy_price = 5000
sell_price = 5500

result = SlippageEngine.calculate(

    buy_price=buy_price,

    sell_price=sell_price

)

print()

for key, value in result.items():

    print(f"{key:<18}: {value}")

print()

print("=" * 60)
print("SLIPPAGE ENGINE TEST SELESAI")