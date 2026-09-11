import pandas as pd


class SwingDetector:

    @staticmethod
    def detect(
        data,
        window=3,
        lookback=120
    ):

        # ==========================================
        # VALIDASI DATA
        # ==========================================

        if data is None or data.empty:
            raise ValueError("Data kosong")

        if "High" not in data.columns:
            raise ValueError("Kolom High tidak ditemukan")

        if "Low" not in data.columns:
            raise ValueError("Kolom Low tidak ditemukan")

        # Gunakan data terakhir sesuai lookback
        df = data.tail(lookback).copy()

        if len(df) < (window * 2) + 1:
            raise ValueError(
                "Data tidak cukup untuk mendeteksi swing"
            )

        high = pd.to_numeric(
            df["High"].squeeze(),
            errors="coerce"
        )

        low = pd.to_numeric(
            df["Low"].squeeze(),
            errors="coerce"
        )

        swing_highs = []
        swing_lows = []

        # ==========================================
        # DETEKSI SWING
        # ==========================================

        for i in range(
            window,
            len(df) - window
        ):

            current_high = float(
                high.iloc[i]
            )

            current_low = float(
                low.iloc[i]
            )

            # --------------------------------------
            # SWING HIGH
            # --------------------------------------

            high_before = high.iloc[
                i - window:i
            ]

            high_after = high.iloc[
                i + 1:i + window + 1
            ]

            if (
                current_high >
                high_before.max()
                and
                current_high >
                high_after.max()
            ):

                swing_highs.append({
                    "index": df.index[i],
                    "position": i,
                    "price": current_high
                })

            # --------------------------------------
            # SWING LOW
            # --------------------------------------

            low_before = low.iloc[
                i - window:i
            ]

            low_after = low.iloc[
                i + 1:i + window + 1
            ]

            if (
                current_low <
                low_before.min()
                and
                current_low <
                low_after.min()
            ):

                swing_lows.append({
                    "index": df.index[i],
                    "position": i,
                    "price": current_low
                })

        # ==========================================
        # HASIL
        # ==========================================

        return {
            "swing_highs": swing_highs,
            "swing_lows": swing_lows
        }