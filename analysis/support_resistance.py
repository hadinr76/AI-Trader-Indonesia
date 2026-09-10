class SupportResistance:

    @staticmethod
    def calculate(data):

        # ==========================================
        # Gunakan 20 candle SEBELUM candle terakhir
        # ==========================================

        previous_data = data.iloc[:-1].tail(20)

        if previous_data.empty:
            raise ValueError(
                "Data tidak cukup untuk menghitung support/resistance"
            )

        support = previous_data["Low"].min()

        resistance = previous_data["High"].max()

        return float(support), float(resistance)