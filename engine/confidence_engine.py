class ConfidenceEngine:

    @staticmethod
    def calculate(technical, fundamental_score, overall_score):

        confidence = 0
        reasons = []

        # =========================================
        # TREND (20)
        # =========================================

        trend = technical["trend"]

        trend_score = {
            "Strong Bullish": (20, "Strong Bullish"),
            "Bullish": (18, "Bullish"),
            "Recovery": (12, "Recovery"),
            "Sideways": (6, "Sideways"),
            "Bearish": (0, "Bearish"),
            "Strong Bearish": (0, "Strong Bearish")
        }

        point, text = trend_score.get(trend, (0, trend))
        confidence += point
        reasons.append(f"{text} (+{point})")

        # =========================================
        # MACD (15)
        # =========================================

        if technical["macd"] == "Bullish Cross":
            confidence += 15
            reasons.append("MACD Bullish Cross (+15)")

        elif technical["macd"] == "Bullish":
            confidence += 10
            reasons.append("MACD Bullish (+10)")

        else:
            reasons.append("MACD Bearish (+0)")

        # =========================================
        # PRICE ACTION (15)
        # =========================================

        pa = technical["price_action"]

        if pa == "Higher High - Higher Low":
            confidence += 15
            reasons.append("Higher High Higher Low (+15)")

        elif pa == "Higher Low":
            confidence += 10
            reasons.append("Higher Low (+10)")

        elif pa == "Sideways":
            confidence += 5
            reasons.append("Sideways (+5)")

        else:
            reasons.append("Price Action Lemah (+0)")

        # =========================================
        # VOLUME (10)
        # =========================================

        volume = technical["volume"]

        if volume == "Very High":
            confidence += 10
            reasons.append("Volume Sangat Tinggi (+10)")

        elif volume == "High":
            confidence += 8
            reasons.append("Volume Tinggi (+8)")

        elif volume == "Normal":
            confidence += 5
            reasons.append("Volume Normal (+5)")

        else:
            reasons.append("Volume Rendah (+0)")

        # =========================================
        # BREAKOUT (10)
        # =========================================

        breakout = technical["breakout"]

        if breakout == "Valid Breakout":
            confidence += 10
            reasons.append("Valid Breakout (+10)")

        elif breakout == "Weak Breakout":
            confidence += 5
            reasons.append("Weak Breakout (+5)")

        else:
            reasons.append("Belum Breakout (+0)")
        # =========================================
        # CANDLESTICK (5)
        # =========================================

        candle = technical.get("candlestick", "")

        strong = [
            "Bullish Engulfing",
            "Morning Star",
            "Three White Soldiers"
        ]

        medium = [
            "Hammer",
            "Piercing Line"
        ]

        if candle in strong:
            confidence += 5
            reasons.append(f"{candle} (+5)")

        elif candle in medium:
            confidence += 4
            reasons.append(f"{candle} (+4)")

        elif candle == "Doji":
            confidence += 2
            reasons.append("Doji (+2)")

        else:
            reasons.append("Tidak ada pola (+0)")

        # =========================================
        # RSI (10)
        # =========================================

        rsi = technical["rsi"]

        if 55 <= rsi <= 70:
            confidence += 10
            reasons.append("RSI Ideal (+10)")

        elif 45 <= rsi < 55:
            confidence += 7
            reasons.append("RSI Netral (+7)")

        elif 70 < rsi <= 80:
            confidence += 5
            reasons.append("RSI Tinggi (+5)")

        else:
            reasons.append("RSI Kurang Ideal (+0)")

        # =========================================
        # MOMENTUM (10)
        # =========================================

        momentum = technical["momentum"]

        if momentum == "Strong Bullish":
            confidence += 10
            reasons.append("Momentum Strong Bullish (+10)")

        elif momentum == "Bullish":
            confidence += 8
            reasons.append("Momentum Bullish (+8)")

        elif momentum == "Neutral":
            confidence += 5
            reasons.append("Momentum Neutral (+5)")

        elif momentum == "Weak":
            confidence += 2
            reasons.append("Momentum Weak (+2)")

        else:
            reasons.append("Momentum Bearish (+0)")

        # =========================================
        # FUNDAMENTAL (10)
        # =========================================

        if fundamental_score >= 90:
            confidence += 10
            reasons.append("Fundamental Sangat Baik (+10)")

        elif fundamental_score >= 80:
            confidence += 8
            reasons.append("Fundamental Baik (+8)")

        elif fundamental_score >= 70:
            confidence += 5
            reasons.append("Fundamental Cukup (+5)")

        # =========================================
        # OVERALL SCORE (5)
        # =========================================

        if overall_score >= 90:
            confidence += 5
            reasons.append("Overall Sangat Tinggi (+5)")

        elif overall_score >= 80:
            confidence += 4
            reasons.append("Overall Tinggi (+4)")

        elif overall_score >= 70:
            confidence += 2
            reasons.append("Overall Cukup (+2)")

        # =========================================
        # FINAL
        # =========================================

        confidence = min(round(confidence), 100)

        if confidence >= 90:
            level = "HIGH CONVICTION"

        elif confidence >= 80:
            level = "VERY HIGH"

        elif confidence >= 70:
            level = "HIGH"

        elif confidence >= 55:
            level = "MEDIUM"

        elif confidence >= 40:
            level = "LOW"

        else:
            level = "VERY LOW"

        return {
            "confidence": confidence,
            "level": level,
            "reasons": reasons
        }