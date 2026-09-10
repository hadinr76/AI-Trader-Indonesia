from money_management.position_size_engine import PositionSizeEngine

print("=" * 60)
print("POSITION SIZE ENGINE TEST")
print("=" * 60)

result = PositionSizeEngine.calculate(

    capital=100_000_000,

    risk_percent=1,

    entry_price=5000,

    stop_loss=4900

)

for k, v in result.items():

    print(f"{k:15} : {v}")

print("=" * 60)