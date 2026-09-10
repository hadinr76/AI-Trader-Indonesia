class RankingEngine:

    @staticmethod
    def calculate(

        overall_score,
        confidence,
        rr,
        smart_signal,
        mtf_score

    ):

        score = 0

        # ====================================
        # Overall Score (40%)
        # ====================================

        score += overall_score * 0.40

        # ====================================
        # Confidence (20%)
        # ====================================

        score += confidence * 0.20

        # ====================================
        # Risk Reward (15%)
        # ====================================

        if rr >= 5:
            score += 15

        elif rr >= 4:
            score += 13

        elif rr >= 3:
            score += 10

        elif rr >= 2:
            score += 7

        else:
            score += 3

        # ====================================
        # Smart Signal (15%)
        # ====================================

        if smart_signal == "STRONG BUY":
            score += 15

        elif smart_signal == "BUY":
            score += 12

        elif smart_signal == "BUY ON WEAKNESS":
            score += 8

        elif smart_signal == "WATCH":
            score += 5

        else:
            score += 0

        # ====================================
        # Multi Time Frame (10%)
        # ====================================

        score += mtf_score * 0.10

        score = round(score, 2)

        if score > 100:
            score = 100

        return score