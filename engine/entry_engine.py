class EntryEngine:

    @staticmethod
    def calculate(
        price,
        support,
        resistance,
        breakout=None
    ):

        # =====================================================
        # VALIDASI
        # =====================================================

        price = float(price)
        support = float(support)
        resistance = float(resistance)

        if price <= 0:
            raise ValueError(
                "Price harus lebih besar dari 0"
            )

        if support <= 0:
            raise ValueError(
                "Support harus lebih besar dari 0"
            )

        if resistance <= support:
            raise ValueError(
                "Resistance harus lebih besar dari support"
            )

        # =====================================================
        # RANGE
        # =====================================================

        price_range = (
            resistance - support
        )

        # =====================================================
        # ZONA ENTRY PULLBACK
        # =====================================================

        entry_low = support

        entry_high = (
            support
            + (
                price_range
                * 0.20
            )
        )

        # =====================================================
        # DISTANCE FROM ENTRY HIGH
        # Diagnostic untuk Entry Engine V2
        # =====================================================

        distance_from_entry_high = (
            (
                price - entry_high
            )
            /
            entry_high
        ) * 100

        # =====================================================
        # STOP LOSS
        # 3% di bawah support
        # =====================================================

        stop_loss = (
            support
            * 0.97
        )

        # =====================================================
        # TARGET
        # =====================================================

        target1 = resistance

        target2 = (
            resistance
            + (
                price_range
                * 0.50
            )
        )

        # =====================================================
        # DISTANCE TO RESISTANCE
        # =====================================================

        distance_to_resistance = (

            (
                resistance - price
            )
            /
            price

        ) * 100

        # =====================================================
        # POSITION
        # =====================================================

        if price < entry_low:

            position = (
                "BELOW ENTRY"
            )

        elif (
            entry_low
            <= price
            <= entry_high
        ):

            position = (
                "ENTRY ZONE"
            )

        elif (
            entry_high
            < price
            < resistance
        ):

            position = (
                "ABOVE ENTRY"
            )

        else:

            position = (
                "BREAKOUT AREA"
            )

        # =====================================================
        # RECOMMENDATION
        # =====================================================

        recommendation = "WAIT"

        reason = (
            "Belum ada kondisi entry ideal"
        )

        # -----------------------------------------------------
        # HARGA DI BAWAH SUPPORT / ENTRY
        # -----------------------------------------------------

        if price < support:

            recommendation = "WAIT"

            reason = (
                "Harga masih berada "
                "di bawah support"
            )

        # -----------------------------------------------------
        # HARGA BERADA DI ZONA ENTRY
        # -----------------------------------------------------

        elif (
            entry_low
            <= price
            <= entry_high
        ):

            recommendation = "BUY"

            reason = (
                "Harga berada "
                "di zona entry"
            )

        # -----------------------------------------------------
        # HARGA DI ATAS ENTRY
        # TETAPI BELUM RESISTANCE
        # -----------------------------------------------------

        elif (
            entry_high
            < price
            < resistance
        ):

            # =================================================
            # EXTENDED ENTRY ZONE
            #
            # Maksimum 5% di atas entry_high.
            # BUY NOW Priority V2 akan menjadi filter
            # kualitas akhir.
            # =================================================

            extended_entry_high = (
                entry_high * 1.05
            )

            if (
                price <= extended_entry_high
                and distance_to_resistance >= 5
            ):

                recommendation = "BUY"

                reason = (
                    "Harga sedikit di atas zona entry "
                    "dan masih dalam Extended Entry Zone"
                )

            # =================================================
            # ABOVE ENTRY
            # =================================================

            elif distance_to_resistance >= 5:

                recommendation = (
                    "BUY ON WEAKNESS"
                )

                reason = (
                    "Harga sudah di atas "
                    "zona entry. Tunggu pullback."
                )

            else:

                recommendation = "WAIT"

                reason = (
                    "Harga terlalu dekat "
                    "dengan resistance"
                )

        # -----------------------------------------------------
        # BREAKOUT
        # -----------------------------------------------------

        elif price >= resistance:

            breakout_distance = (
                (
                    price - resistance
                )
                /
                resistance
            ) * 100

            if breakout == "Valid Breakout":

                # ==========================================
                # FRESH BREAKOUT
                # Maksimum 2% di atas resistance
                # ==========================================

                if breakout_distance <= 2:

                    recommendation = (
                        "BREAKOUT BUY"
                    )

                    reason = (
                        "Valid breakout dan harga "
                        "masih dekat resistance"
                    )

                # ==========================================
                # BREAKOUT SUDAH TERLALU JAUH
                # ==========================================

                else:

                    recommendation = "WAIT"

                    reason = (
                        "Valid breakout tetapi harga "
                        "sudah terlalu jauh dari resistance"
                    )

        else:

            recommendation = "WAIT"

            reason = (
                "Harga berada di area breakout "
                "tetapi belum terkonfirmasi"
            )

        # =====================================================
        # BREAKOUT ENTRY
        # =====================================================

        breakout_entry_low = resistance

        breakout_entry_high = (
            resistance
            * 1.02
        )

        # =====================================================
        # BREAKOUT STOP LOSS
        # =====================================================

        breakout_stop_loss = (
            resistance
            * 0.97
        )

        # =====================================================
        # BREAKOUT TARGET
        # =====================================================

        breakout_target1 = (
            resistance
            + (
                price_range
                * 0.50
            )
        )

        breakout_target2 = (
            resistance
            + price_range
        )

        # =====================================================
        # PILIH TRADE PLAN
        # =====================================================

        if recommendation == "BREAKOUT BUY":

            final_entry_low = (
                breakout_entry_low
            )

            final_entry_high = (
                breakout_entry_high
            )

            final_stop_loss = (
                breakout_stop_loss
            )

            final_target1 = (
                breakout_target1
            )

            final_target2 = (
                breakout_target2
            )

        else:

            final_entry_low = (
                entry_low
            )

            final_entry_high = (
                entry_high
            )

            final_stop_loss = (
                stop_loss
            )

            final_target1 = (
                target1
            )

            final_target2 = (
                target2
            )

        # =====================================================
        # FINAL DISTANCE FROM ENTRY HIGH
        # Menggunakan entry_high dari trade plan final
        # =====================================================

        distance_from_entry_high = (
            (
                price - final_entry_high
            )
            /
            final_entry_high
        ) * 100

        # =====================================================
        # RETURN
        # =====================================================

        return {

            "price":
                round(
                    price,
                    2
                ),

            "support":
                round(
                    support,
                    2
                ),

            "resistance":
                round(
                    resistance,
                    2
                ),

            "entry_low":
                round(
                    final_entry_low,
                    2
                ),

            "entry_high":
                round(
                    final_entry_high,
                    2
                ),

            "stop_loss":
                round(
                    final_stop_loss,
                    2
                ),

            "target1":
                round(
                    final_target1,
                    2
                ),

            "target2":
                round(
                    final_target2,
                    2
                ),

            "position":
                position,

            "recommendation":
                recommendation,

            "reason":
                reason,

            "distance_to_resistance":
                round(
                    distance_to_resistance,
                    2
                ),

            "distance_from_entry_high":
                round(
                    distance_from_entry_high,
                    2
                ),

            "breakout_distance":
                round(
                    (
                        (
                            price - resistance
                        )
                        /
                        resistance
                    ) * 100
                    if resistance > 0
                    else 0,
                    2
                )
        }