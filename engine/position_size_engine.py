class PositionSizeEngine:

    @staticmethod
    def calculate(

        capital,
        risk_percent,
        entry,
        stop_loss

    ):

        # =========================================
        # Risiko maksimal per transaksi
        # =========================================

        max_risk = capital * (risk_percent / 100)

        # =========================================
        # Risiko per lembar saham
        # =========================================

        risk_per_share = entry - stop_loss

        if risk_per_share <= 0:

            return {

                "capital": capital,

                "risk_percent": risk_percent,

                "max_risk": max_risk,

                "risk_per_share": 0,

                "shares": 0,

                "lots": 0,

                "investment": 0

            }

        # =========================================
        # Jumlah saham
        # =========================================

        shares = max_risk / risk_per_share

        # =========================================
        # Bulatkan menjadi lot
        # =========================================

        lots = int(shares // 100)

        shares = lots * 100

        investment = shares * entry

        return {

            "capital": capital,

            "risk_percent": risk_percent,

            "max_risk": round(max_risk,2),

            "risk_per_share": round(risk_per_share,2),

            "shares": shares,

            "lots": lots,

            "investment": round(investment,2)

        }