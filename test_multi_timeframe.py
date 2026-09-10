from engine.multi_timeframe_engine import MultiTimeFrameEngine

print("=" * 60)
print("MULTI TIME FRAME TEST")
print("=" * 60)

hasil = MultiTimeFrameEngine.analyze("BBCA")

for tf in ["Weekly", "Daily", "4H", "1H"]:

    print(
        tf,
        "|",
        hasil[tf]["trend"],
        "|",
        hasil[tf]["score"]
    )

print()

print("Average Score :", hasil["summary"]["average_score"])
print("Bullish       :", hasil["summary"]["bullish"])
print("Bearish       :", hasil["summary"]["bearish"])
print("Status        :", hasil["summary"]["status"])