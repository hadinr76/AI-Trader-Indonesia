from signal.signal_result import SignalResult


class SellSignal:

    @staticmethod
    def check(data):

        trend = data["trend"]
        rsi = data["rsi"]

        if trend == "Bearish" and rsi < 45:

            return SignalResult.create(
                "SELL",
                90,
                "Trend bearish dan momentum melemah."
            )

        return None