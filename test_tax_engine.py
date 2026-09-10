from risk.tax_engine import TaxEngine

print("=" * 60)
print("TAX ENGINE TEST")
print("=" * 60)

sell_value = 54_000_000

result = TaxEngine.summary(sell_value)

print()

print(f"Sell Value     : {result['sell_value']:,.0f}")
print(f"Tax Rate       : {result['tax_rate'] * 100:.2f}%")
print(f"Sell Tax       : {result['tax']:,.2f}")

print()
print("=" * 60)
print("TAX ENGINE TEST SELESAI")
print("=" * 60)