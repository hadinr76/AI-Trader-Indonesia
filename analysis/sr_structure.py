class SRStructure:

    @staticmethod
    def calculate(
        current_price,
        swing_highs,
        swing_lows
    ):

        # ==========================================
        # VALIDASI
        # ==========================================

        if current_price is None:
            raise ValueError("Harga sekarang tidak tersedia")

        if not swing_highs:
            raise ValueError("Swing high tidak tersedia")

        if not swing_lows:
            raise ValueError("Swing low tidak tersedia")

        current_price = float(current_price)

        # ==========================================
        # AMBIL HARGA SWING
        # ==========================================

        high_prices = sorted([
            float(item["price"])
            for item in swing_highs
        ])

        low_prices = sorted([
            float(item["price"])
            for item in swing_lows
        ])

        # ==========================================
        # SUPPORT
        # ==========================================

        supports = [
            price
            for price in low_prices
            if price < current_price
        ]

        # ==========================================
        # RESISTANCE
        # ==========================================

        resistances = [
            price
            for price in high_prices
            if price > current_price
        ]

        # ==========================================
        # MINOR SUPPORT
        # Support terdekat di bawah harga
        # ==========================================

        minor_support = None

        if supports:
            minor_support = max(supports)

        # ==========================================
        # MAJOR SUPPORT
        # Support berikutnya yang lebih dalam
        # ==========================================

        major_support = None

        if len(supports) >= 2:
            major_support = sorted(
                supports,
                reverse=True
            )[1]

        elif len(supports) == 1:
            major_support = supports[0]

        # ==========================================
        # MINOR RESISTANCE
        # Resistance terdekat di atas harga
        # ==========================================

        minor_resistance = None

        if resistances:
            minor_resistance = min(resistances)

        # ==========================================
        # MAJOR RESISTANCE
        # Resistance berikutnya yang lebih tinggi
        # ==========================================

        major_resistance = None

        if len(resistances) >= 2:
            major_resistance = sorted(
                resistances
            )[1]

        elif len(resistances) == 1:
            major_resistance = resistances[0]

        # ==========================================
        # HASIL
        # ==========================================

        return {
            "major_support": major_support,
            "minor_support": minor_support,
            "minor_resistance": minor_resistance,
            "major_resistance": major_resistance
        }