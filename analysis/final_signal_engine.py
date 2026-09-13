class FinalSignalEngine:

    @staticmethod
    def decide(
        decision_recommendation=None,
        entry_signal=None,
        trade_setup_status=None,
        trade_setup_score=0,
        trade_status=None,
        volume_confirmation=None,
        breakout_retest_status=None,
        supply_status=None,
        supply_warning=None
    ):

        reasons = []

        decision = (
            decision_recommendation
            or "WAIT"
        )

        entry = (
            entry_signal
            or "WAIT"
        )

        setup = (
            trade_setup_status
            or "WEAK SETUP"
        )

        score = float(
            trade_setup_score
            or 0
        )

        volume_confirmed = (
            volume_confirmation
            in [
                "CONFIRMED",
                "VERY STRONG"
            ]
        )

        valid_retest = (
            breakout_retest_status
            == "VALID RETEST"
        )

        # ==========================================
        # AVOID FILTER
        # ==========================================

        if decision == "AVOID":

            return {
                "signal": "AVOID",
                "reasons": [
                    "Decision Engine menunjukkan risiko terlalu tinggi"
                ]
            }

        # ==========================================
        # HARD RISK FILTER
        # ==========================================

        if supply_status == "IN SUPPLY":

            return {
                "signal": "WAIT",
                "reasons": [
                    "Harga berada di area supply"
                ]
            }

        if supply_warning == "SUPPLY BEFORE TP1":

            return {
                "signal": "WAIT",
                "reasons": [
                    "Supply terlalu dekat sebelum Target 1"
                ]
            }

        # ==========================================
        # WAIT PULLBACK
        # ==========================================

        if trade_status == "WAIT PULLBACK":

            return {
                "signal": "WAIT PULLBACK",
                "reasons": [
                    "Setup belum berada di Buy Area"
                ]
            }

        # ==========================================
        # BUY
        # ==========================================

        if (
            decision in [
                "BUY",
                "STRONG BUY"
            ]
            and
            entry == "BUY"
            and
            setup in [
                "A SETUP",
                "A+ SETUP"
            ]
            and
            score >= 65
            and
            volume_confirmed
        ):

            reasons.append(
                "Decision Engine mendukung BUY"
            )

            reasons.append(
                "Harga berada di area entry"
            )

            reasons.append(
                "Trade Setup kuat"
            )

            reasons.append(
                "Volume terkonfirmasi"
            )

            return {
                "signal": "BUY",
                "reasons": reasons
            }

        # ==========================================
        # BUY ON WEAKNESS
        # ==========================================

        if (
            decision in [
                "WATCH",
                "BUY ON WEAKNESS",
                "BUY"
            ]
            and
            entry == "BUY"
            and
            setup in [
                "A SETUP",
                "A+ SETUP"
            ]
            and
            score >= 65
            and
            volume_confirmed
            and
            valid_retest
        ):

            reasons.append(
                "Harga berada di Buy Area"
            )

            reasons.append(
                "Trade Setup kuat"
            )

            reasons.append(
                "Breakout Retest valid"
            )

            reasons.append(
                "Volume terkonfirmasi"
            )

            if supply_warning == "SUPPLY BEFORE TP2":
                reasons.append(
                    "Supply berada sebelum Target 2"
                )

            return {
                "signal": "BUY ON WEAKNESS",
                "reasons": reasons
            }

        # ==========================================
        # WATCH / WAIT
        # ==========================================

        if (
            setup in [
                "A SETUP",
                "A+ SETUP"
            ]
            and
            score >= 65
        ):

            return {
                "signal": "WATCH",
                "reasons": [
                    "Setup kuat tetapi konfirmasi entry belum lengkap"
                ]
            }

        return {
            "signal": "WAIT",
            "reasons": [
                "Syarat final entry belum terpenuhi"
            ]
        }
