from decision.decision_rules_v4 import DecisionRulesV4


class DecisionEngineV4:

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
        fundamental_score,
        entry_recommendation=None
        

    ):

        score = 0
        reasons = []

        # Trend
        point = DecisionRulesV4.TREND.get(trend, 0)
        score += point
        reasons.append(f"Trend : {trend} ({point})")

        # Market
        point = DecisionRulesV4.MARKET.get(market_regime, 0)
        score += point
        reasons.append(f"Market : {market_regime} ({point})")

        # Momentum
        point = DecisionRulesV4.MOMENTUM.get(momentum, 0)
        score += point
        reasons.append(f"Momentum : {momentum} ({point})")

        # MACD
        point = DecisionRulesV4.MACD.get(macd, 0)
        score += point
        reasons.append(f"MACD : {macd} ({point})")

        # Volume
        point = DecisionRulesV4.VOLUME.get(volume, 0)
        score += point
        reasons.append(f"Volume : {volume} ({point})")

        # Breakout
        point = DecisionRulesV4.BREAKOUT.get(breakout, 0)
        score += point
        reasons.append(f"Breakout : {breakout} ({point})")

        # RSI
        point = DecisionRulesV4.rsi_score(rsi)
        score += point
        reasons.append(f"RSI : {point}")

        # Confidence
        point = DecisionRulesV4.confidence_score(confidence)
        score += point
        reasons.append(f"Confidence : {point}")

        # Fundamental
        point = DecisionRulesV4.fundamental_score(fundamental_score)
        score += point
        reasons.append(f"Fundamental : {point}")
        
        # Risk Reward
        point = DecisionRulesV4.rr_score(rr)
        score += point
        reasons.append(f"Risk Reward : {point}")

        # ==========================================
        # MULTI TIME FRAME - SWING V2
        # ==========================================

        if mtf_status == "VERY STRONG BULLISH":
            score += 10
            reasons.append(
                "MTF Very Strong Bullish (+10)"
            )

        elif mtf_status == "STRONG BULLISH":
            score += 8
            reasons.append(
                "MTF Strong Bullish (+8)"
            )

        elif mtf_status == "BULLISH":
            score += 6
            reasons.append(
                "MTF Bullish (+6)"
            )

        elif mtf_status == "MIXED":
            score += 3
            reasons.append(
                "MTF Mixed (+3)"
            )

        elif mtf_status == "BEARISH":
            score += 0
            reasons.append(
                "MTF Bearish (+0)"
            )

        elif mtf_status == "STRONG BEARISH":
            score -= 5
            reasons.append(
                "MTF Strong Bearish (-5)"
            )

        elif mtf_status == "VERY STRONG BEARISH":
            score -= 10
            reasons.append(
                "MTF Very Strong Bearish (-10)"
            )

        # ==========================================
        # CANDLESTICK
        # ==========================================

        bullish_candles = {
            "Bullish Engulfing": 5,
            "Morning Star": 5,
            "Three White Soldiers": 5,
            "Hammer": 4,
            "Piercing Line": 4
        }

        bearish_candles = {
            "Bearish Engulfing": -5,
            "Shooting Star": -5
        }

        neutral_candles = {
            "Doji": 0
        }


        if candlestick in bullish_candles:

            point = bullish_candles[candlestick]

            score += point

            reasons.append(
                f"{candlestick} (+{point})"
            )


        elif candlestick in bearish_candles:

            point = bearish_candles[candlestick]

            score += point

            reasons.append(
                f"{candlestick} ({point})"
            )


        elif candlestick in neutral_candles:

            reasons.append(
                f"{candlestick} (0)"
            )

        score = min(score, 100)

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

        # ==========================================
        # ENTRY FILTER
        # ==========================================

        score_recommendation = recommendation

        if entry_recommendation is not None:

            if recommendation == "AVOID":

                recommendation = "AVOID"

            elif entry_recommendation == "WAIT":

                recommendation = "WAIT"

                reasons.append(
                    "Entry Filter : WAIT"
                )

            elif entry_recommendation == "BUY ON WEAKNESS":

                if recommendation in [
                    "STRONG BUY",
                    "BUY",
                    "BUY ON WEAKNESS"
                ]:

                    recommendation = "BUY ON WEAKNESS"

                    reasons.append(
                        "Entry Filter : BUY ON WEAKNESS"
                    )

            elif entry_recommendation == "BREAKOUT BUY":

                if recommendation in [
                    "STRONG BUY",
                    "BUY",
                    "BUY ON WEAKNESS"
                ]:

                    recommendation = "BREAKOUT BUY"

                    reasons.append(
                        "Entry Filter : BREAKOUT BUY"
                    )

            elif entry_recommendation == "BUY":

                # ==========================================
                # ENTRY ZONE + QUALITY FILTER
                # ==========================================

                if score >= 80:

                    recommendation = "BUY"

                    reasons.append(
                        "Entry Filter : BUY - "
                        "zona entry dan score kuat"
                    )

                elif score >= 65:

                    recommendation = "BUY ON WEAKNESS"

                    reasons.append(
                        "Entry Filter : BUY ON WEAKNESS - "
                        "zona entry tetapi score belum cukup kuat"
                    )

                elif score >= 50:

                    recommendation = "WATCH"

                    reasons.append(
                        "Entry Filter : WATCH - "
                        "harga berada di zona entry "
                        "tetapi kualitas setup belum cukup"
                    )

                elif score >= 35:

                    recommendation = "WAIT"

                    reasons.append(
                        "Entry Filter : WAIT - "
                        "zona entry tetapi setup lemah"
                    )

                else:

                    recommendation = "AVOID"

                    reasons.append(
                        "Entry Filter : AVOID - "
                        "setup tidak layak"
                    )

        print()
        print("=" * 55)
        print("DECISION ENGINE V4")
        print("=" * 55)

        for item in reasons:
            print(item)

        print("-" * 55)
        print("TOTAL SCORE :", score)
        print("RECOMMENDATION :", recommendation)
        print("=" * 55)
        print()

        return {
            "score": score,
            "recommendation": recommendation,
            "reasons": reasons,
            "score_recommendation": score_recommendation,
            "entry_recommendation": entry_recommendation,
        }