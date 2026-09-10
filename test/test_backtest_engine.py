from backtest.backtest_engine import BacktestEngine


print("=" * 70)
print("BACKTEST ENGINE TEST")
print("=" * 70)

result = BacktestEngine.run(
    code="BBCA",
    period="3y",
    initial_capital=10_000_000
)

print()
print("=" * 70)
print("HASIL TEST")
print("=" * 70)

print(result)