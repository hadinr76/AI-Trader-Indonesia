class FibonacciEngine:

    @staticmethod
    def calculate(
        current_price,
        swing_highs,
        swing_lows
    ):

        if current_price is None:
            raise ValueError("Harga sekarang tidak tersedia")

        if not swing_highs:
            raise ValueError("Swing high tidak tersedia")

        if not swing_lows:
            raise ValueError("Swing low tidak tersedia")

        current_price = float(current_price)

        # ==========================================
        # CARI SWING TERAKHIR YANG RELEVAN
        # ==========================================

        last_high = swing_highs[-1]
        last_low = swing_lows[-1]

        high_price = float(
            last_high["price"]
        )

        low_price = float(
            last_low["price"]
        )

        # ==========================================
        # TENTUKAN ARAH SWING
        # ==========================================

        if last_low["index"] < last_high["index"]:

            # Bullish swing:
            # dari swing low ke swing high

            trend = "BULLISH"

            swing_low = low_price
            swing_high = high_price

        else:

            # Bearish swing:
            # dari swing high ke swing low

            trend = "BEARISH"

            swing_low = low_price
            swing_high = high_price

        range_price = (
            swing_high - swing_low
        )

        if range_price <= 0:
            raise ValueError(
                "Range swing tidak valid"
            )

        # ==========================================
        # FIBONACCI BULLISH
        # ==========================================

        if trend == "BULLISH":

            fib_236 = (
                swing_high -
                range_price * 0.236
            )

            fib_382 = (
                swing_high -
                range_price * 0.382
            )

            fib_500 = (
                swing_high -
                range_price * 0.500
            )

            fib_618 = (
                swing_high -
                range_price * 0.618
            )

            fib_786 = (
                swing_high -
                range_price * 0.786
            )

        # ==========================================
        # FIBONACCI BEARISH
        # ==========================================

        else:

            fib_236 = (
                swing_low +
                range_price * 0.236
            )

            fib_382 = (
                swing_low +
                range_price * 0.382
            )

            fib_500 = (
                swing_low +
                range_price * 0.500
            )

            fib_618 = (
                swing_low +
                range_price * 0.618
            )

            fib_786 = (
                swing_low +
                range_price * 0.786
            )

        # ==========================================
        # HASIL
        # ==========================================

        return {
            "trend": trend,

            "swing_low": swing_low,
            "swing_high": swing_high,

            "fib_236": float(fib_236),
            "fib_382": float(fib_382),
            "fib_500": float(fib_500),
            "fib_618": float(fib_618),
            "fib_786": float(fib_786),

            "current_price": current_price
        }