from decision.decision_engine_v4 import DecisionEngineV4


print("=" * 70)
print("DECISION ENGINE V4 INTEGRATION TEST")
print("=" * 70)


# =====================================================
# TEST 1
# KONDISI KUAT
# =====================================================

result_1 = DecisionEngineV4.decide(

    trend="Strong Bullish",

    market_regime="BULL MARKET",

    mtf_status="Bullish",

    momentum="Strong Bullish",

    macd="Bullish Cross",

    volume="Very High",

    breakout="Valid Breakout",

    candlestick="Bullish Engulfing",

    rsi=65,

    confidence=90,

    rr=3.5,

    fundamental_score=80

)


print()
print("TEST 1")
print("-" * 70)

print(
    "Recommendation :",
    result_1["recommendation"]
)

print(
    "Score          :",
    result_1["score"]
)


# =====================================================
# TEST 2
# KONDISI MENENGAH
# =====================================================

result_2 = DecisionEngineV4.decide(

    trend="Bullish",

    market_regime="SIDEWAYS",

    mtf_status="Mixed",

    momentum="Bullish",

    macd="Bullish",

    volume="Normal",

    breakout="Belum Breakout",

    candlestick="Tidak ada pola",

    rsi=60,

    confidence=70,

    rr=2.0,

    fundamental_score=70

)


print()
print("TEST 2")
print("-" * 70)

print(
    "Recommendation :",
    result_2["recommendation"]
)

print(
    "Score          :",
    result_2["score"]
)


# =====================================================
# TEST 3
# KONDISI LEMAH
# =====================================================

result_3 = DecisionEngineV4.decide(

    trend="Bearish",

    market_regime="BEAR MARKET",

    mtf_status="Mixed",

    momentum="Weak",

    macd="Bearish Cross",

    volume="Low",

    breakout="Belum Breakout",

    candlestick="Tidak ada pola",

    rsi=40,

    confidence=40,

    rr=1.0,

    fundamental_score=50

)


print()
print("TEST 3")
print("-" * 70)

print(
    "Recommendation :",
    result_3["recommendation"]
)

print(
    "Score          :",
    result_3["score"]
)


print()
print("=" * 70)
print("DECISION ENGINE V4 INTEGRATION TEST SELESAI")
print("=" * 70)