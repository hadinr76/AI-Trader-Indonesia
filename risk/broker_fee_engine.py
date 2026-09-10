class BrokerFeeEngine:
    """
    Menghitung biaya transaksi broker.

    Default menggunakan fee broker Indonesia.

    Buy  : 0.15%
    Sell : 0.25%
    """

    BUY_FEE = 0.0015
    SELL_FEE = 0.0025

    @classmethod
    def calculate_buy_fee(cls, investment):
        """
        Menghitung fee pembelian.
        """

        fee = investment * cls.BUY_FEE

        return round(fee, 2)

    @classmethod
    def calculate_sell_fee(cls, investment):
        """
        Menghitung fee penjualan.
        """

        fee = investment * cls.SELL_FEE

        return round(fee, 2)

    @classmethod
    def calculate_total_fee(cls, buy_value, sell_value):
        """
        Total fee beli + fee jual.
        """

        buy_fee = cls.calculate_buy_fee(buy_value)

        sell_fee = cls.calculate_sell_fee(sell_value)

        return {
            "buy_fee": buy_fee,
            "sell_fee": sell_fee,
            "total_fee": round(buy_fee + sell_fee, 2)
        }