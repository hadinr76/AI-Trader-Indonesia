class TaxEngine:
    """
    Menghitung pajak transaksi penjualan saham.

    Tax rate:
    0.10% dari nilai penjualan.
    """

    TAX_RATE = 0.001

    # =====================================================
    # HITUNG PAJAK
    # =====================================================

    @classmethod
    def calculate_tax(
        cls,
        sell_value
    ):

        return (
            float(sell_value) *
            cls.TAX_RATE
        )

    # =====================================================
    # DETAIL PAJAK
    # =====================================================

    @classmethod
    def calculate(
        cls,
        sell_value
    ):

        sell_tax = cls.calculate_tax(
            sell_value
        )

        return {

            "sell_value":
                float(sell_value),

            "tax_rate":
                cls.TAX_RATE,

            "tax":
                sell_tax

        }