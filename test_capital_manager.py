from money_management.capital_manager import CapitalManager

print("=" * 60)
print("CAPITAL MANAGER TEST")
print("=" * 60)

capital = 100_000_000

investment = 50_000_000

print()
print("TEST 1")
print("-" * 60)

result = CapitalManager.allocate(

    capital=capital,

    investment=investment

)

for k, v in result.items():

    print(f"{k:15} : {v}")

print()

print("TEST 2")
print("-" * 60)

result = CapitalManager.allocate(

    capital=100_000_000,

    investment=150_000_000

)

for k, v in result.items():

    print(f"{k:15} : {v}")

print()

print("TEST 3")
print("-" * 60)

result = CapitalManager.adjust_lot(

    capital=100_000_000,

    entry_price=7_250

)

for k, v in result.items():

    print(f"{k:15} : {v}")

print("=" * 60)