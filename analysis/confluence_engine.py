class ConfluenceEngine:

    @staticmethod
    def calculate(
        current_price,
        sr_structure,
        fibonacci,
        tolerance_pct=2.0
    ):

        current_price = float(current_price)

        # ==========================================
        # SUPPORT SEBAGAI ANCHOR BUY AREA
        # ==========================================

        support_levels = []

        major_support = sr_structure.get(
            "major_support"
        )

        minor_support = sr_structure.get(
            "minor_support"
        )

        if major_support is not None:
            support_levels.append({
                "type": "SR",
                "name": "major_support",
                "price": float(major_support)
            })

        if minor_support is not None:
            support_levels.append({
                "type": "SR",
                "name": "minor_support",
                "price": float(minor_support)
            })

        # ==========================================
        # FIBONACCI LEVEL
        # ==========================================

        fibonacci_levels = []

        fib_names = [
            "fib_382",
            "fib_500",
            "fib_618",
            "fib_786"
        ]

        for name in fib_names:

            price = fibonacci.get(name)

            if price is None:
                continue

            fibonacci_levels.append({
                "type": "FIB",
                "name": name,
                "price": float(price)
            })

        # ==========================================
        # BOBOT CONFLUENCE
        # ==========================================

        weights = {
            "major_support": 4,
            "minor_support": 2,

            "fib_382": 1,
            "fib_500": 2,
            "fib_618": 3,
            "fib_786": 2
        }

        # ==========================================
        # BUAT ZONA DARI SETIAP SUPPORT
        # ==========================================

        zones = []

        for anchor in support_levels:

            anchor_price = anchor["price"]

            zone_levels = [
                anchor
            ]

            # --------------------------------------
            # CARI SUPPORT LAIN YANG BERDEKATAN
            # --------------------------------------

            for support in support_levels:

                if support["name"] == anchor["name"]:
                    continue

                distance_pct = (
                    abs(
                        support["price"] -
                        anchor_price
                    )
                    /
                    anchor_price
                    * 100
                )

                if distance_pct <= tolerance_pct:
                    zone_levels.append(
                        support
                    )

            # --------------------------------------
            # CARI FIBONACCI YANG BERDEKATAN
            # --------------------------------------

            for fib in fibonacci_levels:

                distance_pct = (
                    abs(
                        fib["price"] -
                        anchor_price
                    )
                    /
                    anchor_price
                    * 100
                )

                if distance_pct <= tolerance_pct:
                    zone_levels.append(
                        fib
                    )

            # ======================================
            # HAPUS DUPLIKAT
            # ======================================

            unique_levels = {}

            for level in zone_levels:

                unique_levels[
                    level["name"]
                ] = level

            zone_levels = list(
                unique_levels.values()
            )

            # ======================================
            # HITUNG SCORE
            # ======================================

            score = sum(
                weights.get(
                    level["name"],
                    0
                )
                for level in zone_levels
            )

            prices = [
                level["price"]
                for level in zone_levels
            ]

            zones.append({
                "score": score,
                "area_low": min(prices),
                "area_high": max(prices),
                "levels": zone_levels
            })

        # ==========================================
        # JIKA TIDAK ADA SUPPORT
        # ==========================================

        if not zones:

            return {
                "score": 0,
                "area_low": None,
                "area_high": None,
                "levels": []
            }

        # ==========================================
        # PILIH ZONA TERBAIK
        # SCORE + PROXIMITY
        # ==========================================

        for zone in zones:

            area_mid = (
                zone["area_low"] +
                zone["area_high"]
            ) / 2

            distance_pct = abs(
                current_price -
                area_mid
            ) / current_price * 100

            # --------------------------------------
            # PROXIMITY SCORE
            # --------------------------------------

            proximity_score = 0

            if distance_pct <= 1:
                proximity_score = 4

            elif distance_pct <= 2:
                proximity_score = 3

            elif distance_pct <= 4:
                proximity_score = 2

            elif distance_pct <= 6:
                proximity_score = 1

            # --------------------------------------
            # TOTAL SCORE
            # --------------------------------------

            zone["distance_pct"] = distance_pct
            zone["proximity_score"] = proximity_score

            zone["total_score"] = (
                zone["score"] +
                proximity_score
            )

        best_zone = max(
            zones,
            key=lambda x: x["total_score"]
        )

        return best_zone