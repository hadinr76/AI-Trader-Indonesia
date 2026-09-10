from risk.broker_fee_engine import BrokerFeeEngine

print("=" * 60)
print("BROKER FEE ENGINE TEST")
print("=" * 60)

buy_value = 50_000_000
sell_value = 54_000_000

result = BrokerFeeEngine.calculate_total_fee(
    buy_value,
    sell_value
)

print()

print(f"Buy Value     : {buy_value:,.0f}")
print(f"Sell Value    : {sell_value:,.0f}")

print()

print(f"Buy Fee       : {result['buy_fee']:,.2f}")
print(f"Sell Fee      : {result['sell_fee']:,.2f}")
print(f"Total Fee     : {result['total_fee']:,.2f}")

print()
print("=" * 60)