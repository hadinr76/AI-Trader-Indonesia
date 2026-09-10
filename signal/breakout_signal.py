from signal.signal_result import SignalResult


class BreakoutSignal:

    @staticmethod
    def check(data):

        breakout = data["breakout"]
        volume = data["volume"]

        if breakout == "Breakout" and volume == "High":

            return SignalResult.create(
                "BUY BREAKOUT",
                98,
                "Breakout dengan volume tinggi."
            )

        return None