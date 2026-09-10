class TechnicalScore:

    @staticmethod
    def calculate(data):

        score = 0

        close = float(data["Close"].iloc[-1])

        ema20 = float(data["EMA20"].iloc[-1])
        ema50 = float(data["EMA50"].iloc[-1])
        ema100 = float(data["EMA100"].iloc[-1])
        ema200 = float(data["EMA200"].iloc[-1])

        rsi = float(data["RSI"].iloc[-1])

        macd = float(data["MACD"].iloc[-1])
        signal = float(data["Signal"].iloc[-1])

        # ==========================
        # Harga di atas EMA20
        # ==========================

        if close > ema20:
            score += 20

        # ==========================
        # Struktur EMA
        # ==========================

        if ema20 > ema50:
            score += 15

        if ema50 > ema100:
            score += 15

        if ema100 > ema200:
            score += 15

        # ==========================
        # RSI
        # ==========================

        if 50 <= rsi <= 70:
            score += 20

        elif 30 <= rsi < 50:
            score += 10

        # ==========================
        # MACD
        # ==========================

        if macd > signal:
            score += 15

        return score