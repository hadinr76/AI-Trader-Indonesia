class MACDAnalysis:

    @staticmethod
    def analyze(data):

        macd = float(data["MACD"].iloc[-1])
        signal = float(data["Signal"].iloc[-1])

        if macd > signal:
            return "Bullish Cross"

        elif macd < signal:
            return "Bearish Cross"

        return "Netral"