class MomentumEngine:

    @staticmethod
    def analyze(data):

        close = float(data["Close"].iloc[-1])

        ema20 = float(data["EMA20"].iloc[-1])
        ema50 = float(data["EMA50"].iloc[-1])

        rsi = float(data["RSI"].iloc[-1])

        macd = float(data["MACD"].iloc[-1])
        signal = float(data["Signal"].iloc[-1])

        score = 0

        # ==========================================
        # EMA
        # ==========================================

        if close > ema20:
            score += 20

        if ema20 > ema50:
            score += 20

        # ==========================================
        # RSI
        # ==========================================

        if 55 <= rsi <= 70:
            score += 20

        elif 45 <= rsi < 55:
            score += 10

        elif rsi > 70:
            score += 10

        # ==========================================
        # MACD
        # ==========================================

        if macd > signal:
            score += 20

        if macd > 0:
            score += 20

        # ==========================================
        # Momentum Classification
        # ==========================================

        if score >= 90:

            momentum = "Strong Bullish"

        elif score >= 70:

            momentum = "Bullish"

        elif score >= 50:

            momentum = "Neutral"

        elif score >= 30:

            momentum = "Weak"

        else:

            momentum = "Bearish"

        return {

            "momentum": momentum,

            "score": score

        }