import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from watchlist.watchlist import WATCHLIST
from engine.ai_engine import AIEngine
from engine.trade_manager_engine import TradeManagerEngine


print("=" * 60)
print("AI TRADER INDONESIA")
print("DAILY SCANNER")
print("=" * 60)

manager = TradeManagerEngine()

for code in WATCHLIST:

    print()
    print("-" * 60)

    print("Scanning :", code)

    try:

        result = AIEngine.analyze(code)

        print("Recommendation :", result["recommendation"])

        print("Ranking Score  :", result["ranking_score"])

        print("Confidence     :", result["confidence"])

        print("Overall Score  :", result["overall_score"])

        # ==========================================
        # Simpan hanya BUY
        # ==========================================

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

            if saved:

                print("Trade Saved")

            else:

                print("Trade Already Open")

        else:

            print("Skip")

    except Exception as e:

        print("ERROR :", e)

print()
print("=" * 60)
print("SCAN FINISHED")
print("=" * 60)