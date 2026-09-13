class SignalExplanation:

    @staticmethod
    def generate(
        trade_setup_status=None,
        trade_setup_score=None,
        trade_status=None,
        demand_zone_low=None,
        supply_status=None,
        supply_warning=None,
        breakout_retest_status=None,
        volume_confirmation_status=None,
        final_decision=None
    ):

        parts = []

        if (
            trade_setup_status
            and trade_setup_score is not None
        ):
            parts.append(
                f"{trade_setup_status} "
                f"({trade_setup_score}/100)"
            )

        if trade_status == "IN BUY AREA":
            parts.append(
                "Harga berada di Buy Area"
            )

        elif trade_status == "WAIT PULLBACK":
            parts.append(
                "Harga masih menunggu pullback ke Buy Area"
            )

        if demand_zone_low is not None:
            parts.append(
                "Setup didukung Demand Zone"
            )

        if breakout_retest_status == "VALID RETEST":
            parts.append(
                "Breakout Retest terkonfirmasi valid"
            )

        elif breakout_retest_status == "FAILED RETEST":
            parts.append(
                "Breakout Retest gagal bertahan"
            )

        if volume_confirmation_status == "VERY STRONG":
            parts.append(
                "Volume memberikan konfirmasi sangat kuat"
            )

        elif volume_confirmation_status == "CONFIRMED":
            parts.append(
                "Volume memberikan konfirmasi"
            )

        elif volume_confirmation_status == "WEAK":
            parts.append(
                "Volume masih lemah"
            )

        if supply_status == "IN SUPPLY":
            parts.append(
                "Harga sedang berada di area Supply"
            )

        elif supply_status == "BELOW SUPPLY":
            parts.append(
                "Harga masih berada di bawah Supply"
            )

        if supply_warning == "SUPPLY BEFORE TP1":
            parts.append(
                "Supply berada sebelum Target 1"
            )

        elif supply_warning == "SUPPLY BEFORE TP2":
            parts.append(
                "Supply berada sebelum Target 2"
            )

        if final_decision:
            parts.append(
                f"Final Decision saat ini {final_decision}"
            )

        if not parts:
            return "Belum ada sinyal yang cukup untuk dijelaskan."

        return ". ".join(parts) + "."
