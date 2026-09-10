from signal.signal_result import SignalResult


class PullbackSignal:

    @staticmethod
    def check(data):

        trend = data["trend"]
        rsi = data["rsi"]

        if trend == "Bullish" and rsi > 70:

            return SignalResult.create(
                "WAIT PULLBACK",
                90,
                "RSI sudah tinggi, tunggu harga pullback."
            )

        return None