from fundamental.fundamental_engine import FundamentalEngine
from scoring.fundamental_score import FundamentalScore

fundamental = FundamentalEngine.analyze("BBCA")

score = FundamentalScore.calculate(fundamental)

print("=" * 60)
print("FUNDAMENTAL TEST")
print("=" * 60)

print(f"PER              : {fundamental['per']}")
print(f"PBV              : {fundamental['pbv']}")
print(f"ROE              : {fundamental['roe']:.2%}")
print(f"ROA              : {fundamental['roa']:.2%}")
print(f"EPS              : {fundamental['eps']}")
print(f"Dividend Yield   : {fundamental['dividend_yield']}")
print("-" * 60)
print(f"Fundamental Score : {score}")