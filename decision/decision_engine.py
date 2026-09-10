from engine.decision_score_engine import DecisionScoreEngine
from decision.decision_rules import DecisionRules


class DecisionEngine:

    @staticmethod
    def decide(

        trend,
        mtf_status,
        macd,
        volume,
        breakout,
        candlestick,
        rsi,
        confidence,
        rr,
        overall

    ):

        decision_score = DecisionScoreEngine.calculate(

            trend,
            mtf_status,
            macd,
            volume,
            breakout,
            candlestick,
            rsi,
            confidence,
            rr,
            overall

        )

        recommendation = DecisionRules.evaluate(

            decision_score["score"]

        )

        return {

            "recommendation": recommendation,

            "score": decision_score["score"],

            "reasons": decision_score["reasons"]

        }