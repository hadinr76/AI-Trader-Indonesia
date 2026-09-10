from signal.signal_result import SignalResult


class BuySignal:

    @staticmethod
    def check(data):

        trend = data["trend"]
        rsi = data["rsi"]
        macd = data["macd"]
        volume = data["volume"]

        if (
            trend == "Bullish"
            and macd == "Bullish Cross"
            and volume == "High"
            and 55 <= rsi <= 70
        ):

            return SignalResult.create(
                "BUY",
                95,
                "Trend bullish dengan volume kuat dan MACD Bullish Cross."
            )

        return None