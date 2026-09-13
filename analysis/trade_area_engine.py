class TradeAreaEngine:

    @staticmethod
    def calculate(
        current_price,
        confluence,
        sr_structure,
         supply_zone=None,
        stop_buffer_pct=1.0
    ):

        current_price = float(current_price)

        area_low = confluence.get("area_low")
        area_high = confluence.get("area_high")
        score = confluence.get("score", 0)

        minor_resistance = sr_structure.get(
            "minor_resistance"
        )

        major_resistance = sr_structure.get(
            "major_resistance"
        )

        major_support = sr_structure.get(
            "major_support"
        )

        # ==========================================
        # SUPPLY ZONE V2
        # ==========================================

        supply_zone_low = None
        supply_zone_high = None

        if supply_zone:

            supply_zone_low = supply_zone.get(
                "zone_low"
            )

            supply_zone_high = supply_zone.get(
                "zone_high"
            )

            if supply_zone_low is not None:
                supply_zone_low = float(
                    supply_zone_low
                )

            if supply_zone_high is not None:
                supply_zone_high = float(
                    supply_zone_high
                )

        # ==========================================
        # VALIDASI BUY AREA
        # ==========================================

        if (
            area_low is None
            or area_high is None
        ):

            return {
                "buy_area_low": None,
                "buy_area_high": None,
                "ideal_entry": None,
                "stop_loss": None,
                "tp1": minor_resistance,
                "tp2": major_resistance,
                "confluence_score": score
            }

        area_low = float(area_low)
        area_high = float(area_high)

        # ==========================================
        # BUY AREA
        # ==========================================

        buy_area_low = min(
            area_low,
            area_high
        )

        buy_area_high = max(
            area_low,
            area_high
        )

        ideal_entry = (
            buy_area_low +
            buy_area_high
        ) / 2

        # ==========================================
        # STOP LOSS
        # ==========================================
        # SL mengikuti support pada zona terpilih,
        # bukan selalu major support global
        # ==========================================

        stop_reference = buy_area_low

        selected_levels = confluence.get(
            "levels",
            []
        )

        selected_supports = [
            float(level["price"])
            for level in selected_levels
            if level.get("name") in [
                "major_support",
                "minor_support"
            ]
        ]

        if selected_supports:

            stop_reference = min(
                [buy_area_low] +
                selected_supports
            )

        stop_loss = (
            stop_reference *
            (1 - stop_buffer_pct / 100)
        )

        # ==========================================
        # TARGET
        # ==========================================

        tp1 = None
        tp2 = None

        if minor_resistance is not None:
            tp1 = float(
                minor_resistance
            )

        if major_resistance is not None:
            tp2 = float(
                major_resistance
            )

        # ==========================================
        # SUPPLY STATUS
        # ==========================================

        supply_status = None
        distance_to_supply_pct = None

        if (
            supply_zone_low is not None
            and supply_zone_high is not None
        ):

            if current_price < supply_zone_low:

                supply_status = "BELOW SUPPLY"

                distance_to_supply_pct = (
                    (
                        supply_zone_low -
                        current_price
                    )
                    / current_price
                    * 100
                )

            elif (
                current_price >= supply_zone_low
                and current_price <= supply_zone_high
            ):

                supply_status = "IN SUPPLY"

                distance_to_supply_pct = 0.0

            else:

                supply_status = "ABOVE SUPPLY"

        # ==========================================
        # SUPPLY TARGET WARNING
        # ==========================================

        supply_warning = None

        if supply_zone_low is not None:

            if (
                tp1 is not None
                and supply_zone_low <= tp1
            ):
                supply_warning = "SUPPLY BEFORE TP1"

            elif (
                tp2 is not None
                and supply_zone_low <= tp2
            ):
                supply_warning = "SUPPLY BEFORE TP2"

            else:
                supply_warning = "SUPPLY ABOVE TARGET"

        # ==========================================
        # RISK / REWARD
        # ==========================================

        risk = (
            ideal_entry -
            stop_loss
        )

        rr_tp1 = None
        rr_tp2 = None

        if risk > 0:

            if (
                tp1 is not None
                and tp1 > ideal_entry
            ):

                rr_tp1 = (
                    tp1 -
                    ideal_entry
                ) / risk

            if (
                tp2 is not None
                and tp2 > ideal_entry
            ):

                rr_tp2 = (
                    tp2 -
                    ideal_entry
                ) / risk

        # ==========================================
        # STATUS HARGA
        # ==========================================

        if (
            current_price >= buy_area_low
            and current_price <= buy_area_high
        ):

            status = "IN BUY AREA"

        elif current_price > buy_area_high:

            status = "WAIT PULLBACK"

        else:

            status = "BELOW BUY AREA"

        # ==========================================
        # TRADE QUALITY
        # ==========================================

        trade_quality = "WAIT"
        trade_reason = "Harga belum berada di buy area"

        best_rr = None

        rr_values = [
            rr
            for rr in [rr_tp1, rr_tp2]
            if rr is not None
        ]

        if rr_values:
            best_rr = max(rr_values)

        # Hanya nilai kualitas entry
        # jika harga sudah berada di buy area

        if status == "IN BUY AREA":

            if best_rr is None:

                trade_quality = "SKIP"
                trade_reason = (
                    "Risk Reward tidak tersedia"
                )

            elif best_rr >= 2.0:

                trade_quality = "BAGUS"
                trade_reason = (
                    "Harga di buy area dan "
                    "Risk Reward sangat baik"
                )

            elif best_rr >= 1.5:

                trade_quality = "CUKUP"
                trade_reason = (
                    "Harga di buy area dan "
                    "Risk Reward masih layak"
                )

            else:

                trade_quality = "SKIP"
                trade_reason = (
                    "Harga di buy area tetapi "
                    "Risk Reward terlalu rendah"
                )

        elif status == "WAIT PULLBACK":

            trade_quality = "WAIT"
            trade_reason = (
                "Tunggu harga masuk buy area"
            )

        elif status == "BELOW BUY AREA":

            trade_quality = "SKIP"
            trade_reason = (
                "Harga sudah turun di bawah buy area"
            )

        # ==========================================
        # TRADE ACTION
        # ==========================================

        trade_action = "WAIT"

        if status == "IN BUY AREA":

            if trade_quality == "BAGUS":
                trade_action = "BUY"

            elif trade_quality == "CUKUP":
                trade_action = "BUY ON WEAKNESS"

            else:
                trade_action = "WAIT"

        elif status == "WAIT PULLBACK":
            trade_action = "WAIT"

        elif status == "BELOW BUY AREA":
            trade_action = "WAIT"

        # ==========================================
        # HASIL
        # ==========================================

        return {
            "buy_area_low": buy_area_low,
            "buy_area_high": buy_area_high,

            "ideal_entry": ideal_entry,

            "stop_loss": float(
                stop_loss
            ),

            "tp1": tp1,
            "tp2": tp2,

            "rr_tp1": rr_tp1,
            "rr_tp2": rr_tp2,

            "status": status,

            "confluence_score": score,

            "trade_quality": trade_quality,
            "trade_action": trade_action,
            "trade_reason": trade_reason,
            "best_rr": best_rr,
            "supply_zone_low": supply_zone_low,
            "supply_zone_high": supply_zone_high,
            "supply_status": supply_status,
            "distance_to_supply_pct": distance_to_supply_pct,
            "supply_warning": supply_warning,
        }