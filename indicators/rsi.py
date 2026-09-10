import numpy as np


class RSIIndicator:

    @staticmethod
    def calculate(data, period=14):

        close = data["Close"].dropna().astype(float)

        delta = close.diff()

        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)

        avg_gain = gain.rolling(period).mean()
        avg_loss = loss.rolling(period).mean()

        avg_loss = avg_loss.replace(0, np.nan)

        rs = avg_gain / avg_loss

        rsi = 100 - (100 / (1 + rs))

        return rsi.reindex(data.index).ffill().fillna(50)