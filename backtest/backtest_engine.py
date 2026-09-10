from data.market_data import MarketData

from engine.ai_engine import AIEngine

from backtest.trade_simulator import TradeSimulator
from backtest.statistics import Statistics
from backtest.equity_curve import EquityCurve
from backtest.performance_report import PerformanceReport



class BacktestEngine:

    @staticmethod
    def run(

        code,
        period="3y",
        initial_capital=100_000_000

    ):

        print("=" * 70)
        print("BACKTEST ENGINE")
        print("=" * 70)

        print()

        print("Downloading data...")

        market = MarketData()

        data = market.get_daily(

            code,

            period=period

        )

        if data is None:

            print("Data tidak tersedia.")

            return None

        print("Jumlah Candle :", len(data))

        print()

        trades = []

        # ==========================================
        # LOOP CANDLE
        # ==========================================

        i = 200

        while i < len(data):

            history = data.iloc[: i + 1].copy()

            print(

                f"Backtest {i+1}/{len(data)}",

                end="\r"

            )

            # =====================================================
            # AI ANALYZE
            # =====================================================

            result = AIEngine.analyze(
                code,
                data=history,
                backtest_mode=True
            )

            if result is None:

                i += 1

                continue

            # =====================================================
            # HANYA BUY
            # =====================================================

            if result["recommendation"] not in [

                "BUY",

                "BUY ON WEAKNESS",

                "STRONG BUY"

            ]:

                i += 1

                continue

            # =====================================================
            # FIXED POSITION - BACKTEST V1
            # =====================================================

            position = {
                "shares": 100,
                "lots": 1,
                "investment": result["entry_low"] * 100
            }

            # =====================================================
            # SIMULASI TRADE
            # =====================================================

            trade = TradeSimulator.simulate(

                data=data.iloc[i+1:].copy(),

                entry_price=result["entry_low"],

                stop_loss=result["stop_loss"],

                target1=result["target1"],

                target2=result["target2"],

                shares=position["shares"],

                lots=position["lots"]

            )

            # =====================================================
            # ENTRY TIDAK TEREKSEKUSI
            # =====================================================

            if trade["status"] == "NOT FILLED":

                i += 1

                continue

            # =====================================================
            # SIMPAN INFORMASI
            # =====================================================

            trade["date"] = history.index[-1]

            trade["code"] = code

            trade["recommendation"] = result["recommendation"]

            trade["overall_score"] = result["overall_score"]

            trade["confidence"] = result["confidence"]

            trade["ranking_score"] = result["ranking_score"]

            trade["shares"] = position["shares"]

            trade["lots"] = position["lots"]

            trade["investment"] = position["investment"]

            trades.append(trade)

            print()
            print("=" * 60)
            print(f"TRADE {len(trades)}")
            print("=" * 60)
            print("Signal Date      :", trade["date"])
            print("Recommendation   :", trade["recommendation"])
            print("Entry            :", result["entry_low"])
            print("Stop Loss        :", result["stop_loss"])
            print("Target 1         :", result["target1"])
            print("Target 2         :", result["target2"])
            print("Entry Wait Days  :", trade["entry_wait_days"])
            print("Holding Days     :", trade["holding_days"])
            print("Exit Status      :", trade["status"])
            print("Exit Price       :", trade["exit_price"])
            print("Decision Score   :", result["decision_score"])
            print("Technical Score  :", result["technical_score"])
            print("Confidence       :", result["confidence"])
            print("Profit           :", trade["profit"])
            print("=" * 60)

            i += trade["entry_wait_days"] + trade["holding_days"] + 1
       
        print()

        print("=" * 70)

        print("BACKTEST FINISHED")

        print("=" * 70)

        print()

        print("Total Trade :", len(trades))

        print()

        # =====================================================
        # STATISTICS
        # =====================================================

        statistics = Statistics.calculate(

            trades

        )

        # =====================================================
        # EQUITY CURVE
        # =====================================================

        equity = EquityCurve.calculate(

            initial_capital,

            trades

        )

        # =====================================================
        # PERFORMANCE REPORT
        # =====================================================

        report = PerformanceReport.generate(

            statistics,

            equity

        )

        PerformanceReport.show(

            report

        )

        return report