from engine.indicator_engine import IndicatorEngine
from engine.analysis_engine import AnalysisEngine
from engine.score_engine import ScoreEngine
from engine.momentum_engine import MomentumEngine


class TechnicalEngine:

    @staticmethod
    def analyze(data):

        # ==========================================
        # Indicator
        # ==========================================

        data = IndicatorEngine.calculate(data)

        # ==========================================
        # Analysis
        # ==========================================

        analysis = AnalysisEngine.analyze(data)

        trend = analysis["trend"]
        macd = analysis["macd"]
        price_action = analysis["price_action"]
        volume = analysis["volume"]
        support = analysis["support"]
        resistance = analysis["resistance"]
        breakout = analysis["breakout"]
        candlestick = analysis["candlestick"]

        # ==========================================
        # Score
        # ==========================================

        score_result = ScoreEngine.calculate(
            data,
            analysis
        )

        score = score_result["score"]
        candlestick_score = score_result["candlestick_score"]

        # ==========================================
        # Momentum
        # ==========================================

        momentum = MomentumEngine.analyze(data)

        # ==========================================
        # Price
        # ==========================================

        close = data["Close"].dropna()

        price = float(close.iloc[-1])

        # ==========================================
        # Return
        # ==========================================

        return {

            "trend": trend,

            "rsi": float(data["RSI"].iloc[-1]),

            "macd": macd,

            "price_action": price_action,

            "volume": volume,

            "breakout": breakout,

            "candlestick": candlestick,

            "candlestick_score": candlestick_score,

            "support": support,

            "resistance": resistance,

            "score": score,

            "price": price,

            "momentum": momentum["momentum"],

            "momentum_score": momentum["score"]

        }