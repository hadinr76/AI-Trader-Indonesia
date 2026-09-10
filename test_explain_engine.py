from engine.explain_engine import ExplainEngine

print("=" * 60)
print("EXPLAIN ENGINE TEST")
print("=" * 60)

data = {
    "trend": "Bullish",
    "mtf_status": "VERY STRONG BULLISH",
    "macd": "Bullish Cross",
    "volume": "High",
    "breakout": "Breakout",
    "rsi": 72.5,
    "rr2": 5.14,
    "confidence": 85,
    "fundamental_score": 90,
    "ranking_score": 92.1
}

hasil = ExplainEngine.generate(data)

print()

for i, item in enumerate(hasil, start=1):
    print(f"{i}. {item}")