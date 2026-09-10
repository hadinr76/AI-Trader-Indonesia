from engine.ai_engine import AIEngine

print("=" * 70)
print("AI ENGINE TEST")
print("=" * 70)

hasil = AIEngine.analyze("BBCA")

# ==========================================================
# Informasi Saham
# ==========================================================

print(f"Kode               : {hasil['code']}")
print(f"Harga              : {hasil['price']:.0f}")

print("-" * 70)

# ==========================================================
# Technical Analysis
# ==========================================================

print(f"Trend              : {hasil['trend']}")
print(f"RSI                : {hasil['rsi']:.2f}")
print(f"MACD               : {hasil['macd']}")
print(f"Price Action       : {hasil['price_action']}")
print(f"Volume             : {hasil['volume']}")
print(f"Breakout           : {hasil['breakout']}")

print("-" * 70)

# ==========================================================
# Score
# ==========================================================

print(f"Technical Score    : {hasil['technical_score']}")
print(f"Fundamental Score  : {hasil['fundamental_score']}")
print(f"Overall Score      : {hasil['overall_score']}")

print("-" * 70)

# ==========================================================
# AI Rating
# ==========================================================

print(f"AI Rating          : {hasil['rating']}")
print(f"Kategori           : {hasil['category']}")
print(f"Rekomendasi        : {hasil['recommendation']}")

print("-" * 70)

# ==========================================================
# Decision
# ==========================================================

print(f"Decision Score     : {hasil['decision_score']}")

print()

print("Decision Reason:")

for r in hasil["decision_reason"]:
    print("✓", r)

# ==========================================================
# Support Resistance
# ==========================================================

print(f"Support            : {hasil['support']:.0f}")
print(f"Resistance         : {hasil['resistance']:.0f}")

print("-" * 70)

# ==========================================================
# Entry Plan
# ==========================================================

print(f"Entry Area         : {hasil['entry_low']:.0f} - {hasil['entry_high']:.0f}")
print(f"Stop Loss          : {hasil['stop_loss']:.0f}")
print(f"Target 1           : {hasil['target1']:.0f}")
print(f"Target 2           : {hasil['target2']:.0f}")

print("-" * 70)

# ==========================================================
# Risk Reward
# ==========================================================

print(f"Risk               : {hasil['risk']:.0f}")
print(f"Reward TP1         : {hasil['reward1']:.0f}")
print(f"Reward TP2         : {hasil['reward2']:.0f}")

print(f"Risk Reward TP1    : 1 : {hasil['rr1']}")
print(f"Risk Reward TP2    : 1 : {hasil['rr2']}")

print("-" * 70)

# ==========================================================
# Position Sizing
# ==========================================================

print("POSITION SIZING")

print(f"Modal              : {hasil['capital']:,.0f}")

print(f"Risk (%)           : {hasil['risk_percent']}%")

print(f"Max Risk           : {hasil['max_risk']:,.0f}")

print(f"Risk / Share       : {hasil['risk_per_share']:,.0f}")

print(f"Recommended Lots   : {hasil['lots']}")

print(f"Investment         : {hasil['investment']:,.0f}")

cash_remaining = hasil["capital"] - hasil["investment"]

print(f"Remaining Cash     : {cash_remaining:,.0f}")

print("-" * 70)

# ==========================================================
# Confidence
# ==========================================================

print(f"Confidence         : {hasil['confidence']}%")

print()

print("Reason:")

for alasan in hasil["confidence_reason"]:
    print("✓", alasan)

print("-" * 70)

# ==========================================================
# AI Summary
# ==========================================================

print("ANALISIS AI")

for teks in hasil["summary"]:
    print("•", teks)

print("=" * 70)

print("-" * 70)
print("AI EXPLANATION")

print("-" * 70)
print("INVESTMENT ADVISOR")

for item in hasil["investment_advisor"]:
    print("•", item)

for item in hasil["explanation"]:
    print("•", item)


print("-" * 70)
print("MARKET CONDITION")
print(f"Market Regime     : {hasil['market_regime']}")
print(f"Market Trend      : {hasil['market_trend']}")
print(f"Market RSI        : {hasil['market_rsi']:.2f}")
print(f"Market MACD       : {hasil['market_macd']}")

print("-" * 70)

print("SMART SIGNAL")
print("Signal             :", hasil["smart_signal"])
print("Score              :", hasil["smart_score"])
print("MTF Status         :", hasil["mtf_status"])
print("MTF Avg Score      :", hasil["mtf_average_score"])

print("-" * 70)

print("AI RANKING")
print(f"Ranking Score      : {hasil['ranking_score']}")

print("\nSmart Reason:")

for item in hasil["smart_reason"]:
    print("✓", item)