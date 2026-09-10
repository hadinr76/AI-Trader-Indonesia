from decision.decision_engine_v4 import DecisionEngineV4
from engine.entry_engine import EntryEngine
from engine.risk_reward_engine import RiskRewardEngine


print("=" * 70)
print("FINAL DECISION + ENTRY TEST")
print("=" * 70)


# =====================================================
# DATA CONTOH IPAC
# =====================================================

price = 182
support = 147
resistance = 190
breakout = "Belum Breakout"


# =====================================================
# ENTRY PLAN
# =====================================================

entry = EntryEngine.calculate(

    price=price,
    support=support,
    resistance=resistance,
    breakout=breakout

)


# =====================================================
# RISK REWARD
# =====================================================

rr = RiskRewardEngine.calculate(

    entry["entry_low"],
    entry["entry_high"],
    entry["stop_loss"],
    entry["target1"],
    entry["target2"]

)


# =====================================================
# DECISION
# =====================================================

decision = DecisionEngineV4.decide(

    trend="Bullish",

    market_regime="BULL MARKET",

    mtf_status="Bullish",

    momentum="Strong Bullish",

    macd="Bullish Cross",

    volume="Very High",

    breakout=breakout,

    candlestick="Tidak ada pola",

    rsi=67.86,

    confidence=85,

    rr=rr["rr1"],

    fundamental_score=75,

    entry_recommendation=entry["recommendation"]

)


# =====================================================
# OUTPUT
# =====================================================

print()
print("=" * 70)
print("HASIL FINAL")
print("=" * 70)

print()

print(
    "Current Price        :",
    entry["price"]
)

print(
    "Support              :",
    entry["support"]
)

print(
    "Resistance           :",
    entry["resistance"]
)

print(
    "Entry Zone           :",
    entry["entry_low"],
    "-",
    entry["entry_high"]
)

print(
    "Stop Loss            :",
    entry["stop_loss"]
)

print(
    "Target 1             :",
    entry["target1"]
)

print(
    "Target 2             :",
    entry["target2"]
)

print(
    "R:R Target 1         :",
    rr["rr1"]
)

print(
    "R:R Target 2         :",
    rr["rr2"]
)

print()

print(
    "Score Recommendation :",
    decision["score_recommendation"]
)

print(
    "Entry Recommendation :",
    decision["entry_recommendation"]
)

print(
    "FINAL Recommendation :",
    decision["recommendation"]
)

print(
    "Decision Score       :",
    decision["score"]
)

print()
print("=" * 70)
print("FINAL DECISION + ENTRY TEST SELESAI")
print("=" * 70)