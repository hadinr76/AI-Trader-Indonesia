class MarketFilterEngine:

    @staticmethod
    def adjust(
        regime,
        recommendation,
        ranking_score
    ):

        recommendation = recommendation.upper()
        ranking_score = float(ranking_score)

        # ==========================================
        # BULL MARKET
        # ==========================================

        if regime == "BULL MARKET":

            multiplier = 1.00

        # ==========================================
        # RECOVERY
        # ==========================================

        elif regime == "RECOVERY":

            multiplier = 0.95

            if recommendation == "STRONG BUY":
                recommendation = "BUY"

        # ==========================================
        # SIDEWAYS
        # ==========================================

        elif regime == "SIDEWAYS":

            multiplier = 0.90

            if recommendation == "STRONG BUY":
                recommendation = "BUY"

            elif recommendation == "BUY":
                recommendation = "BUY ON WEAKNESS"

        # ==========================================
        # BEAR MARKET
        # ==========================================

        else:

            multiplier = 0.75

            if recommendation == "STRONG BUY":
                recommendation = "BUY"

            elif recommendation == "BUY":
                recommendation = "BUY ON WEAKNESS"

            elif recommendation == "BUY ON WEAKNESS":
                recommendation = "WATCH"

        # ==========================================
        # FINAL RANKING
        # ==========================================

        ranking_score *= multiplier

        ranking_score = max(0, min(100, ranking_score))

        ranking_score = round(ranking_score, 2)

        return {

            "recommendation": recommendation,

            "ranking_score": ranking_score

        }