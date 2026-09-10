class TaxEngine:
    """
    Menghitung pajak transaksi saham.

    Default:
    Pajak Penjualan Saham Indonesia = 0.10%
    """

    SELL_TAX = 0.001

    @classmethod
    def calculate_sell_tax(cls, sell_value):
        """
        Menghitung pajak penjualan.

        Parameters
        ----------
        sell_value : float
            Nilai bruto penjualan saham.

        Returns
        -------
        float
            Pajak penjualan.
        """

        tax = sell_value * cls.SELL_TAX

        return round(tax, 2)

    @classmethod
    def get_tax_rate(cls):
        """
        Mengembalikan tarif pajak.
        """

        return cls.SELL_TAX

    @classmethod
    def summary(cls, sell_value):
        """
        Ringkasan perhitungan pajak.
        """

        tax = cls.calculate_sell_tax(sell_value)

        return {
            "sell_value": sell_value,
            "tax_rate": cls.SELL_TAX,
            "tax": tax
        }