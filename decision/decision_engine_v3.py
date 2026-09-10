from decision.decision_rules_v3 import DecisionRulesV3


class DecisionEngineV3:

    @staticmethod
    def decide(

        trend,
        market_regime,
        mtf_status,
        momentum,
        macd,
        volume,
        breakout,
        candlestick,
        rsi,
        confidence,
        rr,
        fundamental_score

    ):

        score = 0
        reasons = []

        # ==========================================
        # TREND
        # ==========================================

        point = DecisionRulesV3.TREND.get(trend, 0)

        score += point

        reasons.append(f"Trend : {trend} ({point})")

        # ==========================================
        # MARKET REGIME
        # ==========================================

        point = DecisionRulesV3.MARKET.get(
            market_regime,
            0
        )

        score += point

        reasons.append(
            f"Market : {market_regime} ({point})"
        )

        # ==========================================
        # MOMENTUM
        # ==========================================

        point = DecisionRulesV3.MOMENTUM.get(
            momentum,
            0
        )

        score += point

        reasons.append(
            f"Momentum : {momentum} ({point})"
        )

        # ==========================================
        # MACD
        # ==========================================

        point = DecisionRulesV3.MACD.get(
            macd,
            0
        )

        score += point

        reasons.append(
            f"MACD : {macd} ({point})"
        )

        # ==========================================
        # RSI
        # ==========================================

        point = DecisionRulesV3.rsi_score(rsi)

        score += point

        reasons.append(
            f"RSI : {point}"
        )

        # ==========================================
        # CONFIDENCE
        # ==========================================

        point = DecisionRulesV3.confidence_score(
            confidence
        )

        score += point

        reasons.append(
            f"Confidence : {point}"
        )

        # ==========================================
        # RISK REWARD
        # ==========================================

        point = DecisionRulesV3.rr_score(rr)

        score += point

        reasons.append(
            f"Risk Reward : {point}"
        )

        # ==========================================
        # FUNDAMENTAL
        # ==========================================

        point = DecisionRulesV3.fundamental_score(
            fundamental_score
        )

        score += point

        reasons.append(
            f"Fundamental : {point}"
        )

        # ==========================================
        # MULTI TIME FRAME
        # ==========================================

        if mtf_status == "Bullish":

            score += 10

            reasons.append(
                "MTF Bullish (+10)"
            )

        elif mtf_status == "Mixed":

            score += 5

            reasons.append(
                "MTF Mixed (+5)"
            )

        # ==========================================
        # VOLUME
        # ==========================================

        if volume == "High":

            score += 5

            reasons.append(
                "High Volume (+5)"
            )

        elif volume == "Normal":

            score += 3

            reasons.append(
                "Normal Volume (+3)"
            )

        # ==========================================
        # BREAKOUT
        # ==========================================

        if breakout == "Breakout":

            score += 5

            reasons.append(
                "Breakout (+5)"
            )

        # ==========================================
        # CANDLESTICK
        # ==========================================

        if candlestick not in [

            "None",

            "Tidak ada pola",

             "",

            None

        ]:

            score += 5

            reasons.append(
                f"{candlestick} (+5)"
            )

        # ==========================================
        # FINAL SCORE
        # ==========================================

        score = max(0, min(score, 100))

        # ==========================================
        # RECOMMENDATION
        # ==========================================

        if score >= 90:

            recommendation = "STRONG BUY"

        elif score >= 80:

            recommendation = "BUY"

        elif score >= 65:

            recommendation = "BUY ON WEAKNESS"

        elif score >= 50:

            recommendation = "WATCH"

        elif score >= 35:

            recommendation = "WAIT"

        else:

            recommendation = "AVOID"

        print()
        print("=" * 50)
        print("DECISION ENGINE DEBUG")
        print("=" * 50)

        for reason in reasons:
            print(reason)

        print("-" * 50)
        print("TOTAL SCORE :", score)
        print("RECOMMENDATION :", recommendation)
        print("=" * 50)
        print()

        return {

            "score": score,

            "recommendation": recommendation,

            "reasons": reasons

        }