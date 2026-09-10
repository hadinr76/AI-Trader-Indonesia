class DecisionScoreEngine:

    @staticmethod
    def calculate(

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

        score = 0
        reasons = []

        # ==========================================
        # TREND
        # ==========================================

        trend_score = {

            "Strong Bullish": 35,
            "Bullish": 28,
            "Recovery": 18,
            "Sideways": 8,
            "Bearish": -20,
            "Strong Bearish": -35

        }

        s = trend_score.get(trend, 0)
        score += s
        reasons.append(f"Trend : {trend} ({s:+})")

        # ==========================================
        # MULTI TIMEFRAME
        # ==========================================

        mtf_score = {

            "VERY STRONG BULLISH": 18,
            "STRONG BULLISH": 14,
            "BULLISH": 10,
            "MIXED": 5,
            "BEARISH": -10

        }

        s = mtf_score.get(mtf_status, 0)
        score += s
        reasons.append(f"MTF : {mtf_status} ({s:+})")

        # ==========================================
        # MACD
        # ==========================================

        if macd == "Bullish Cross":

            score += 12
            reasons.append("MACD Bullish (+12)")

        else:

            score -= 8
            reasons.append("MACD Bearish (-8)")

        # ==========================================
        # VOLUME
        # ==========================================

        if volume == "High":

            score += 10
            reasons.append("Volume High (+10)")

        elif volume == "Normal":

            score += 5
            reasons.append("Volume Normal (+5)")

        else:

            score -= 2
            reasons.append("Volume Low (-2)")

        # ==========================================
        # BREAKOUT
        # ==========================================

        if breakout == "Breakout":

            score += 12
            reasons.append("Breakout (+12)")

        # ==========================================
        # CANDLESTICK
        # ==========================================

        bullish_pattern = [

            "Hammer",
            "Bullish Engulfing",
            "Morning Star",
            "Piercing Line",
            "Three White Soldiers"

        ]

        if candlestick in bullish_pattern:

            score += 8
            reasons.append(f"{candlestick} (+8)")

        elif candlestick == "Doji":

            score += 3
            reasons.append("Doji (+3)")

        # ==========================================
        # RSI
        # ==========================================

        if 55 <= rsi <= 70:

            score += 10
            reasons.append("RSI Ideal (+10)")

        elif 45 <= rsi < 55:

            score += 6
            reasons.append("RSI Netral (+6)")

        elif 70 < rsi <= 80:

            score += 3
            reasons.append("RSI Tinggi (+3)")

        elif rsi > 80:

            score -= 5
            reasons.append("RSI Overbought (-5)")

        # ==========================================
        # CONFIDENCE
        # ==========================================

        score += confidence * 0.15

        reasons.append(f"Confidence ({confidence})")

        # ==========================================
        # RISK REWARD
        # ==========================================

        if rr >= 5:

            score += 15

        elif rr >= 3:

            score += 10

        elif rr >= 2:

            score += 5

        # ==========================================
        # OVERALL
        # ==========================================

        score += overall * 0.15

        reasons.append(f"Overall ({overall})")

        return {

            "score": round(score,1),

            "reasons": reasons

        }