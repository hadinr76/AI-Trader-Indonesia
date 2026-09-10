class TechnicalAnalysis:

    @staticmethod
    def check_trend(data):

        close = float(data["Close"].dropna().iloc[-1])

        ema20 = float(data["EMA20"].dropna().iloc[-1])
        ema50 = float(data["EMA50"].dropna().iloc[-1])
        ema100 = float(data["EMA100"].dropna().iloc[-1])
        ema200 = float(data["EMA200"].dropna().iloc[-1])

        # ==========================================
        # STRONG BULLISH
        # EMA berurutan naik + harga di atas EMA20
        # ==========================================
        if (
            close > ema20
            and ema20 > ema50
            and ema50 > ema100
            and ema100 > ema200
        ):
            return "Strong Bullish"

        # ==========================================
        # BULLISH
        # Harga di atas EMA20 dan EMA20 di atas EMA50
        # ==========================================
        elif (
            close > ema20
            and ema20 > ema50
        ):
            return "Bullish"

        # ==========================================
        # RECOVERY
        # Harga mulai di atas EMA20 tetapi EMA20
        # masih di bawah EMA50
        # ==========================================
        elif (
            close > ema20
            and ema20 < ema50
        ):
            return "Recovery"

        # ==========================================
        # STRONG BEARISH
        # Semua EMA turun
        # ==========================================
        elif (
            close < ema20
            and ema20 < ema50
            and ema50 < ema100
            and ema100 < ema200
        ):
            return "Strong Bearish"

        # ==========================================
        # BEARISH
        # ==========================================
        elif close < ema20:
            return "Bearish"

        # ==========================================
        # SIDEWAYS
        # ==========================================
        else:
            return "Sideways"