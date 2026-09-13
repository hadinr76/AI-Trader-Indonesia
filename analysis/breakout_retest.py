class BreakoutRetest:

    @staticmethod
    def analyze(
        data,
        resistance,
        tolerance_pct=1.0,
        lookback=10
    ):

        if data is None or data.empty:
            raise ValueError("Data kosong")

        resistance = float(resistance)

        if resistance <= 0:
            raise ValueError(
                "Resistance harus lebih besar dari 0"
            )

        df = data.tail(lookback).copy()

        if len(df) < 3:
            return {
                "status": "NO RETEST",
                "breakout_found": False,
                "retest_found": False,
                "retest_holding": False
            }

        tolerance = (
            resistance *
            tolerance_pct / 100
        )

        breakout_found = False
        breakout_index = None

        for i in range(1, len(df)):

            previous_close = float(
                df["Close"].iloc[i - 1]
            )

            current_close = float(
                df["Close"].iloc[i]
            )

            if (
                previous_close <= resistance
                and current_close > resistance
            ):
                breakout_found = True
                breakout_index = i

        if not breakout_found:

            return {
                "status": "NO BREAKOUT",
                "breakout_found": False,
                "retest_found": False,
                "retest_holding": False
            }

        retest_found = False
        retest_holding = False

        for i in range(
            breakout_index + 1,
            len(df)
        ):

            candle_low = float(
                df["Low"].iloc[i]
            )

            candle_close = float(
                df["Close"].iloc[i]
            )

            near_resistance = (
                candle_low
                <= resistance + tolerance
            )

            holding = (
                candle_close
                >= resistance - tolerance
            )

            if near_resistance:

                retest_found = True

                if holding:
                    retest_holding = True

        if (
            retest_found
            and retest_holding
        ):
            status = "VALID RETEST"

        elif retest_found:
            status = "FAILED RETEST"

        else:
            status = "WAIT RETEST"

        return {
            "status": status,
            "breakout_found": breakout_found,
            "retest_found": retest_found,
            "retest_holding": retest_holding,
            "resistance": resistance,
            "tolerance_pct": tolerance_pct
        }
