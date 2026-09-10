from indicators.ema import EMAIndicator
from indicators.rsi import RSIIndicator
from indicators.macd import MACDIndicator


class IndicatorEngine:

    @staticmethod
    def calculate(data):

        data["EMA20"] = EMAIndicator.calculate(data, 20)
        data["EMA50"] = EMAIndicator.calculate(data, 50)
        data["EMA100"] = EMAIndicator.calculate(data, 100)
        data["EMA200"] = EMAIndicator.calculate(data, 200)

        data["RSI"] = RSIIndicator.calculate(data)

        (
            data["MACD"],
            data["Signal"],
            data["Histogram"]
        ) = MACDIndicator.calculate(data)
        
        return data