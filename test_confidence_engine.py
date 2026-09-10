from engine.confidence_engine import ConfidenceEngine

technical = {

    "trend": "Bullish",

    "macd": "Bullish Cross",

    "price_action": "Higher High - Higher Low",

    "volume": "High",

    "breakout": "Belum Breakout",

    "candlestick": "Bullish Engulfing"

}

hasil = ConfidenceEngine.calculate(

    technical,

    90,

    87

)

print("=" * 60)
print("CONFIDENCE ENGINE TEST")
print("=" * 60)

print("Confidence :", hasil["confidence"], "%")

print()

print("Reasons:")

for alasan in hasil["reasons"]:
    print("✓", alasan)