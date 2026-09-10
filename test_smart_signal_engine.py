from signal.smart_signal_engine import SmartSignalEngine

print("=" * 60)
print("SMART SIGNAL ENGINE TEST")
print("=" * 60)

hasil = SmartSignalEngine.analyze(

    recommendation="BUY",

    confidence=92,

    overall_score=88,

    rr=4.5,

    mtf_status="VERY STRONG BULLISH"

)

print("Recommendation :", "BUY")
print("Final Signal   :", hasil["signal"])
print("Score          :", hasil["score"])

print("\nReason:")

for item in hasil["reason"]:
    print("✓", item)