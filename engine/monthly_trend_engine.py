class MonthlyTrendEngine:

    @staticmethod
    def analyze(data):

        # ==========================================
        # VALIDATION
        # ==========================================

        close = data["Close"].dropna()

        if len(close) < 20:

            return {
                "trend": "Unknown",
                "price": 0,
                "ema10": 0,
                "ema20": 0
            }

        # ==========================================
        # MONTHLY EMA
        # ==========================================

        ema10 = close.ewm(
            span=10,
            adjust=False
        ).mean()

        ema20 = close.ewm(
            span=20,
            adjust=False
        ).mean()

        price = float(close.iloc[-1])
        current_ema10 = float(ema10.iloc[-1])
        current_ema20 = float(ema20.iloc[-1])

        # ==========================================
        # MAJOR TREND
        # ==========================================

        if (
            price > current_ema10
            and current_ema10 > current_ema20
        ):

            trend = "Bullish"

        elif (
            price > current_ema10
            and current_ema10 <= current_ema20
        ):

            trend = "Recovery"

        elif (
            price < current_ema10
            and current_ema10 < current_ema20
        ):

            trend = "Bearish"

        else:

            trend = "Sideways"

        # ==========================================
        # RETURN
        # ==========================================

        return {
            "trend": trend,
            "price": round(price, 2),
            "ema10": round(current_ema10, 2),
            "ema20": round(current_ema20, 2)
        }