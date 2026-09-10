from engine.ai_engine import AIEngine

from engine.trade_manager_engine import TradeManagerEngine
from engine.performance_tracker_engine import PerformanceTrackerEngine
from engine.portfolio_manager_engine import PortfolioManagerEngine

print("=" * 70)
print("AI TRADER INDONESIA")
print("FULL SYSTEM TEST")
print("=" * 70)

# =====================================================
# ANALISA SAHAM
# =====================================================

kode = "BBCA"

print()
print("Analisa :", kode)
print("-" * 70)

result = AIEngine.analyze(kode)

print("Recommendation :", result["recommendation"])
print("Trend          :", result["trend"])
print("Overall Score  :", result["overall_score"])
print("Confidence     :", result["confidence"])
print("Ranking Score  :", result["ranking_score"])

print()

print("Entry Area     :", result["entry_low"], "-", result["entry_high"])
print("Stop Loss      :", result["stop_loss"])
print("Target 1       :", result["target1"])
print("Target 2       :", result["target2"])

# =====================================================
# SIMPAN TRADE
# =====================================================

manager = TradeManagerEngine()

if result["recommendation"] in [

    "BUY",

    "STRONG BUY",

    "BUY ON WEAKNESS"

]:

    trade = {

        "date": "",

        "code": result["code"],

        "recommendation": result["recommendation"],

        "price": result["price"],

        "entry": result["entry_low"],

        "stop_loss": result["stop_loss"],

        "target1": result["target1"],

        "target2": result["target2"],

        "confidence": result["confidence"],

        "overall_score": result["overall_score"],

        "ranking_score": result["ranking_score"]

    }

    saved = manager.save_trade(trade)

    print()

    if saved:

        print("Trade berhasil disimpan.")

    else:

        print("Trade sudah ada (OPEN).")

else:

    print()
    print("Trade tidak disimpan karena bukan sinyal BUY.")

# =====================================================
# UPDATE PERFORMANCE
# =====================================================

print()
print("-" * 70)
print("Updating Performance Tracker...")

PerformanceTrackerEngine.update()

print("Selesai.")

# =====================================================
# PORTFOLIO
# =====================================================

portfolio = PortfolioManagerEngine.calculate()

print()
print("=" * 70)
print("PORTFOLIO")
print("=" * 70)

for key, value in portfolio.items():

    print(f"{key:20}: {value}")

print()
print("=" * 70)
print("FULL SYSTEM TEST SELESAI")
print("=" * 70)