class RiskRewardEngine:

    @staticmethod
    def calculate(entry_low, entry_high, stop_loss, target1, target2):

        # Entry rata-rata
        entry = (entry_low + entry_high) / 2

        # Risk
        risk = entry - stop_loss

        # Reward
        reward1 = target1 - entry
        reward2 = target2 - entry

        # Hindari pembagian dengan nol
        if risk <= 0:
            rr1 = 0
            rr2 = 0
        else:
            rr1 = reward1 / risk
            rr2 = reward2 / risk

        return {

            "entry": round(entry, 2),

            "risk": round(risk, 2),

            "reward1": round(reward1, 2),

            "reward2": round(reward2, 2),

            "rr1": round(rr1, 2),

            "rr2": round(rr2, 2)

        }