class OpportunityRankingEngine:

    @staticmethod
    def calculate(
        recommendation,
        decision_score,
        confidence,
        technical_ranking,
        fundamental_score,
        watchlist_priority_score,
        rr1,
        rsi,
        relative_volume,
        liquidity_status,
        distance_entry_high
    ):

        score = 0
        reasons = []

        # =================================================
        # RECOMMENDATION WEIGHT
        # =================================================

        recommendation_score = {
            "STRONG BUY": 100,
            "BUY": 95,
            "BREAKOUT BUY": 90,
            "BUY ON WEAKNESS": 85,
            "WATCH": 60,
            "WAIT": 40,
            "AVOID": 0
        }

        score += (
            recommendation_score.get(
                recommendation,
                0
            )
            * 0.20
        )

        # =================================================
        # DECISION SCORE
        # =================================================

        score += decision_score * 0.20

        # =================================================
        # CONFIDENCE
        # =================================================

        score += confidence * 0.15

        # =================================================
        # TECHNICAL RANKING
        # =================================================

        score += technical_ranking * 0.15

        # =================================================
        # FUNDAMENTAL
        # =================================================

        score += fundamental_score * 0.10

        # =================================================
        # WATCHLIST PRIORITY
        # =================================================

        score += watchlist_priority_score * 0.10

        # =================================================
        # RISK REWARD
        # =================================================

        if rr1 >= 3:
            score += 5
            reasons.append("Risk reward sangat baik")

        elif rr1 >= 2:
            score += 3
            reasons.append("Risk reward baik")

        # =================================================
        # RSI TIMING
        # =================================================

        if 50 <= rsi <= 70:
            score += 3
            reasons.append("RSI ideal")

        elif 70 < rsi <= 75:
            score += 1
            reasons.append("RSI mulai tinggi")

        # =================================================
        # RELATIVE VOLUME
        # =================================================

        if relative_volume >= 2:
            score += 5
            reasons.append("Volume sangat kuat")

        elif relative_volume >= 1:
            score += 3
            reasons.append("Volume mendukung")

        # =================================================
        # LIQUIDITY
        # =================================================

        liquidity_score = {
            "VERY LIQUID": 5,
            "LIQUID": 4,
            "MODERATE": 2,
            "LOW LIQUIDITY": 0,
            "ILLIQUID": 0
        }

        score += liquidity_score.get(
            liquidity_status,
            0
        )

        # =================================================
        # ENTRY DISTANCE PENALTY
        # =================================================

        if distance_entry_high > 25:
            score -= 15
            reasons.append("Harga sangat jauh dari zona entry")

        elif distance_entry_high > 15:
            score -= 10
            reasons.append("Harga jauh dari zona entry")

        elif distance_entry_high > 10:
            score -= 5
            reasons.append("Harga mulai jauh dari zona entry")

        elif 0 <= distance_entry_high <= 5:
            score += 3
            reasons.append("Harga dekat zona entry")

        # =================================================
        # FINAL SCORE
        # =================================================

        score = round(
            max(0, min(score, 100)),
            2
        )

        return {
            "score": score,
            "reasons": reasons
        }