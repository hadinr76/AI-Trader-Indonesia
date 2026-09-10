from data.data_manager import DataManager
from engine.technical_engine import TechnicalEngine


class MarketRegimeEngine:

    @staticmethod
    def analyze():

        try:

            data = DataManager.get_daily("^JKSE")

            technical = TechnicalEngine.analyze(data)

            DEBUG = False

            if DEBUG:
                print("=" * 40)
                print("DEBUG MARKET REGIME")
                print(data.tail())
                print()

                print("Trend :", technical["trend"])
                print("RSI   :", technical["rsi"])
                print("MACD  :", technical["macd"])
                print("=" * 40)

            trend = technical["trend"]
            rsi = technical["rsi"]
            macd = technical["macd"]

            # =====================================
            # MARKET REGIME
            # =====================================

            if (
                trend == "Strong Bullish"
                and macd == "Bullish Cross"
                and rsi >= 60
            ):

                market_regime = "BULL MARKET"

            elif trend == "Bullish":

                market_regime = "BULL MARKET"

            elif trend == "Recovery":

                market_regime = "RECOVERY"

            elif trend == "Bearish":

                market_regime = "BEAR MARKET"

            elif trend == "Strong Bearish":

                market_regime = "CRASH"

            else:

                market_regime = "SIDEWAYS"

            return {

                "market_regime": market_regime,
                "trend": trend,
                "macd": macd,
                "rsi": round(rsi, 2)

            }

        except Exception:

            return {

                "market_regime": "UNKNOWN",
                "trend": "-",
                "macd": "-",
                "rsi": 0

            }