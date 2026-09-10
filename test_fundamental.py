from fundamental.fundamental_engine import FundamentalEngine

hasil = FundamentalEngine.analyze("BBCA")

print("=" * 60)
print("FUNDAMENTAL BBCA")
print("=" * 60)

for k, v in hasil.items():
    print(f"{k:20} : {v}")