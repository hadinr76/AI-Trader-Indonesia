from signal.buy_signal import BuySignal
from signal.sell_signal import SellSignal
from signal.pullback_signal import PullbackSignal
from signal.breakout_signal import BreakoutSignal


class SignalEngine:

    @staticmethod
    def analyze(data):

        # Prioritas sinyal
        signals = [

            BreakoutSignal.check(data),

            BuySignal.check(data),

            PullbackSignal.check(data),

            SellSignal.check(data)

        ]

        for signal in signals:

            if signal is not None:
                return signal

        return {
            "signal": "WATCH",
            "confidence": 50,
            "reason": "Belum ada sinyal yang memenuhi syarat."
        }