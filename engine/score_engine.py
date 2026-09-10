from scoring.technical_score import TechnicalScore
from scoring.price_action_score import PriceActionScore
from scoring.volume_score import VolumeScore
from scoring.breakout_score import BreakoutScore
from scoring.candlestick_score import CandlestickScore


class ScoreEngine:

    @staticmethod
    def calculate(data, analysis):

        # =====================================================
        # RAW SCORE
        # =====================================================

        technical_score = TechnicalScore.calculate(
            data
        )

        price_action_score = PriceActionScore.calculate(
            analysis["price_action"]
        )

        volume_score = VolumeScore.calculate(
            analysis["volume"]
        )

        breakout_score = BreakoutScore.calculate(
            analysis["breakout"]
        )

        candlestick_score = CandlestickScore.calculate(
            analysis["candlestick"]
        )

        # =====================================================
        # WEIGHTED SCORE
        #
        # Technical     : 50%
        # Price Action  : 15%
        # Volume        : 15%
        # Breakout      : 10%
        # Candlestick   : 10%
        #
        # TOTAL         : 100
        # =====================================================

        technical_weighted = (
            technical_score
            * 0.50
        )

        # Price Action maksimum 20
        # 20 -> 15

        price_action_weighted = (
            price_action_score
            / 20
            * 15
        )

        # Volume maksimum 20
        # 20 -> 15

        volume_weighted = (
            volume_score
            / 20
            * 15
        )

        # Breakout maksimum 20
        # 20 -> 10

        breakout_weighted = (
            breakout_score
            / 20
            * 10
        )

        # Candlestick maksimum +12
        #
        # Three White Soldiers = 12 -> 10
        #
        # Bearish pattern tetap memberi
        # penalti negatif.

        candlestick_weighted = (
            candlestick_score
            / 12
            * 10
        )

        # =====================================================
        # TOTAL SCORE
        # =====================================================

        total_score = (

            technical_weighted
            + price_action_weighted
            + volume_weighted
            + breakout_weighted
            + candlestick_weighted

        )

        # =====================================================
        # BATAS 0 - 100
        # =====================================================

        total_score = max(
            0,
            min(
                total_score,
                100
            )
        )

        # =====================================================
        # RESULT
        # =====================================================

        return {

            "technical_score":
                technical_score,

            "price_action_score":
                price_action_score,

            "volume_score":
                volume_score,

            "breakout_score":
                breakout_score,

            "candlestick_score":
                candlestick_score,

            "technical_weighted":
                round(
                    technical_weighted,
                    2
                ),

            "price_action_weighted":
                round(
                    price_action_weighted,
                    2
                ),

            "volume_weighted":
                round(
                    volume_weighted,
                    2
                ),

            "breakout_weighted":
                round(
                    breakout_weighted,
                    2
                ),

            "candlestick_weighted":
                round(
                    candlestick_weighted,
                    2
                ),

            "score":
                round(
                    total_score,
                    2
                )

        }