import pandas as pd


class SupplyZone:

    @staticmethod
    def detect(
        data,
        lookback=120,
        impulse_threshold_pct=2.0,
        max_zones=5
    ):

        if data is None or data.empty:
            raise ValueError("Data kosong")

        required_columns = [
            "Open",
            "High",
            "Low",
            "Close"
        ]

        for column in required_columns:
            if column not in data.columns:
                raise ValueError(
                    f"Kolom {column} tidak ditemukan"
                )

        df = data.tail(lookback).copy()

        if len(df) < 10:
            raise ValueError(
                "Data tidak cukup untuk mendeteksi supply zone"
            )

        open_price = pd.to_numeric(
            df["Open"].squeeze(),
            errors="coerce"
        )

        high = pd.to_numeric(
            df["High"].squeeze(),
            errors="coerce"
        )

        low = pd.to_numeric(
            df["Low"].squeeze(),
            errors="coerce"
        )

        close = pd.to_numeric(
            df["Close"].squeeze(),
            errors="coerce"
        )

        zones = []

        for i in range(
            1,
            len(df) - 3
        ):

            base_open = float(
                open_price.iloc[i]
            )

            base_close = float(
                close.iloc[i]
            )

            base_high = float(
                high.iloc[i]
            )

            base_low = float(
                low.iloc[i]
            )

            future_low = float(
                low.iloc[
                    i + 1:i + 4
                ].min()
            )

            impulse_pct = (
                (
                    base_low -
                    future_low
                )
                / base_low
                * 100
            )

            if (
                base_close >= base_open
                and
                impulse_pct >= impulse_threshold_pct
            ):

                zone_low = min(
                    base_open,
                    base_close
                )

                zone_high = base_high

                # ==================================
                # CEK VALIDITAS ZONA
                # ==================================

                later_close = close.iloc[
                    i + 1:
                ]

                broken = (
                    later_close > zone_high
                )

                status = "ACTIVE"
                broken_at = None

                if broken.any():

                    status = "BROKEN"

                    broken_position = (
                        broken[broken].index[0]
                    )

                    broken_at = broken_position

                zones.append({
                    "index": df.index[i],
                    "zone_low": float(
                        zone_low
                    ),
                    "zone_high": float(
                        zone_high
                    ),
                    "impulse_pct": float(
                        impulse_pct
                    ),
                    "status": status,
                    "broken_at": broken_at
                })

        # ==========================================
        # PRIORITASKAN ZONA ACTIVE
        # ==========================================

        zones = sorted(
            zones,
            key=lambda x: (
                x["status"] != "ACTIVE",
                -x["index"].timestamp()
            )
        )

        return zones[:max_zones]