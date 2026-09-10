class SignalResult:

    @staticmethod
    def create(signal, confidence, reason):

        return {
            "signal": signal,
            "confidence": confidence,
            "reason": reason
        }