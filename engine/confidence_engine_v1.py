class ConfidenceEngine:

    @staticmethod
    def calculate(technical, fundamental_score, overall_score):

        confidence = 0
        reasons = []

        # =========================================
        # TREND CONFIRMATION (40)
        # =========================================

        if technical["trend"] == "Bullish":
            confidence += 15
            reasons.append("✓ Trend Bullish (+15)")
        else:
            reasons.append("• Trend belum Bullish (+0)")

        if technical["macd"] == "Bullish Cross":
            confidence += 10
            reasons.append("✓ MACD Bullish Cross (+10)")
        else:
            reasons.append("• MACD belum Bullish (+0)")

        if technical["price_action"] == "Higher High - Higher Low":
            confidence += 10
            reasons.append("✓ Higher High Higher Low (+10)")
        else:
            reasons.append("• Price Action belum kuat (+0)")

        if technical["breakout"] == "Breakout":
            confidence += 5
            reasons.append("✓ Breakout (+5)")
        else:
            reasons.append("• Belum Breakout (+0)")

        # =========================================
        # MOMENTUM (30)
        # =========================================

        if technical["volume"] == "High":
            confidence += 10
            reasons.append("✓ Volume Tinggi (+10)")
        else:
            reasons.append("• Volume rendah (+0)")

        candle = technical.get("candlestick", "Tidak Ada")

        strong_pattern = [
            "Bullish Engulfing",
            "Morning Star",
            "Hammer",
            "Piercing Line"
        ]

        if candle in strong_pattern:
            confidence += 10
            reasons.append(f"✓ {candle} (+10)")
        elif candle != "Tidak Ada":
            confidence += 5
            reasons.append(f"✓ {candle} (+5)")
        else:
            reasons.append("• Tidak ada pola candlestick (+0)")

        rsi = technical["rsi"]

        if 40 <= rsi <= 70:
            confidence += 10
            reasons.append("✓ RSI Ideal (+10)")
        elif 30 <= rsi < 40 or 70 < rsi <= 80:
            confidence += 5
            reasons.append("✓ RSI Cukup Baik (+5)")
        else:
            reasons.append("• RSI terlalu tinggi/rendah (+0)")

        # =========================================
        # QUALITY (30)
        # =========================================

        if fundamental_score >= 80:
            confidence += 15
            reasons.append("✓ Fundamental Sangat Baik (+15)")
        elif fundamental_score >= 60:
            confidence += 10
            reasons.append("✓ Fundamental Baik (+10)")
        else:
            reasons.append("• Fundamental lemah (+0)")

        if overall_score >= 90:
            confidence += 15
            reasons.append("✓ Overall Sangat Tinggi (+15)")
        elif overall_score >= 80:
            confidence += 10
            reasons.append("✓ Overall Tinggi (+10)")
        elif overall_score >= 70:
            confidence += 5
            reasons.append("✓ Overall Cukup (+5)")
        else:
            reasons.append("• Overall masih rendah (+0)")

        confidence = min(confidence, 100)

        # =========================================
        # Confidence Level
        # =========================================

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