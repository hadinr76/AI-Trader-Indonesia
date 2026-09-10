from scoring.candlestick_score import CandlestickScore

print("=" * 60)
print("CANDLESTICK SCORE TEST")
print("=" * 60)

patterns = [
    "Bullish Engulfing",
    "Hammer",
    "Morning Star",
    "Three White Soldiers",
    "Doji",
    "Shooting Star",
    "Bearish Engulfing",
    "Tidak Ada"
]

for p in patterns:

    score = CandlestickScore.calculate(p)

    print(f"{p:25} : {score}")