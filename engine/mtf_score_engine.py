class MTFScoreEngine:

    @staticmethod
    def calculate(result):

        # ==========================================
        # TIMEFRAME WEIGHT — SWING TRADING
        # ==========================================

        weights = {
            "Weekly": 0.30,
            "Daily": 0.50,
            "4H": 0.20
        }

        # ==========================================
        # TREND STRENGTH
        # ==========================================

        trend_strength = {
            "Strong Bullish": 100,
            "Bullish": 80,
            "Recovery": 60,
            "Sideways": 50,
            "Bearish": 20,
            "Strong Bearish": 0,
            "Unknown": 50
        }

        weighted_score = 0
        total_weight = 0

        bullish = 0
        bearish = 0

        # ==========================================
        # CALCULATE MTF
        # ==========================================

        for timeframe, weight in weights.items():

            tf = result.get(timeframe)

            if not tf:
                continue

            trend = tf.get(
                "trend",
                "Unknown"
            )

            strength = trend_strength.get(
                trend,
                50
            )

            weighted_score += (
                strength * weight
            )

            total_weight += weight

            if trend in (
                "Strong Bullish",
                "Bullish",
                "Recovery"
            ):
                bullish += 1

            elif trend in (
                "Strong Bearish",
                "Bearish"
            ):
                bearish += 1

        # ==========================================
        # FINAL SCORE
        # ==========================================

        if total_weight > 0:

            final_score = round(
                weighted_score
                / total_weight
            )

        else:

            final_score = 50

        # ==========================================
        # STATUS
        # ==========================================

        if final_score >= 85:

            status = "VERY STRONG BULLISH"

        elif final_score >= 70:

            status = "STRONG BULLISH"

        elif final_score >= 55:

            status = "BULLISH"

        elif final_score >= 45:

            status = "MIXED"

        elif final_score >= 30:

            status = "BEARISH"

        elif final_score >= 15:

            status = "STRONG BEARISH"

        else:

            status = "VERY STRONG BEARISH"

        return {

            "average_score": final_score,

            "bullish": bullish,

            "bearish": bearish,

            "status": status

        }