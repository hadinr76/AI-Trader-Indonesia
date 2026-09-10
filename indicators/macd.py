class MACDIndicator:

    @staticmethod
    def calculate(data):

        close = data["Close"].dropna()

        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()

        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()

        histogram = macd - signal

        return (
            macd.reindex(data.index).ffill(),
            signal.reindex(data.index).ffill(),
            histogram.reindex(data.index).ffill()
        )