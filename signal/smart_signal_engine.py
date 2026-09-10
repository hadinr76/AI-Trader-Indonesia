class SmartSignalEngine:

    @staticmethod
    def analyze(

        recommendation,
        confidence,
        overall_score,
        rr,
        mtf_status

    ):

        reason = []
        score = 0

        # =====================================
        # Confidence
        # =====================================

        if confidence >= 90:
            score += 30
            reason.append("Confidence Sangat Tinggi")

        elif confidence >= 80:
            score += 25
            reason.append("Confidence Tinggi")

        elif confidence >= 70:
            score += 20
            reason.append("Confidence Baik")

        elif confidence >= 60:
            score += 10
            reason.append("Confidence Sedang")

        # =====================================
        # Overall Score
        # =====================================

        if overall_score >= 90:
            score += 25
            reason.append("Overall Sangat Tinggi")

        elif overall_score >= 80:
            score += 20
            reason.append("Overall Tinggi")

        elif overall_score >= 70:
            score += 10
            reason.append("Overall Cukup")

        # =====================================
        # Risk Reward
        # =====================================

        if rr >= 4:
            score += 25
            reason.append("Risk Reward Sangat Baik")

        elif rr >= 3:
            score += 20
            reason.append("Risk Reward Baik")

        elif rr >= 2:
            score += 10
            reason.append("Risk Reward Cukup")

        # =====================================
        # Multi Time Frame
        # =====================================

        if mtf_status == "VERY STRONG BULLISH":
            score += 20
            reason.append(
                "MTF Very Strong Bullish"
            )

        elif mtf_status == "STRONG BULLISH":
            score += 10
            reason.append(
                "MTF Strong Bullish"
            )

        elif mtf_status == "BULLISH":
            score += 5
            reason.append(
                "MTF Bullish"
            )

        # =====================================
        # FINAL SIGNAL
        # =====================================

        signal = recommendation

        if recommendation == "BUY":

            if score >= 90:
                signal = "STRONG BUY"

            elif score < 60:
                signal = "BUY ON WEAKNESS"

        elif recommendation == "BUY ON WEAKNESS":

            if score >= 90:
                signal = "BUY"

        return {

            "signal": signal,

            "score": score,

            "reason": reason

        }