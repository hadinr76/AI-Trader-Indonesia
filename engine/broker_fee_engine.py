class BrokerFeeEngine:
    """
    Menghitung biaya broker untuk transaksi BUY dan SELL.

    BUY  : 0.15%
    SELL : 0.25%
    """

    BUY_FEE_RATE = 0.0015

    SELL_FEE_RATE = 0.0025

    # =====================================================
    # BUY FEE
    # =====================================================

    @classmethod
    def calculate_buy_fee(
        cls,
        buy_value
    ):

        return (
            float(buy_value) *
            cls.BUY_FEE_RATE
        )

    # =====================================================
    # SELL FEE
    # =====================================================

    @classmethod
    def calculate_sell_fee(
        cls,
        sell_value
    ):

        return (
            float(sell_value) *
            cls.SELL_FEE_RATE
        )

    # =====================================================
    # TOTAL FEE
    # =====================================================

    @classmethod
    def calculate_total_fee(
        cls,
        buy_value,
        sell_value
    ):

        buy_fee = cls.calculate_buy_fee(
            buy_value
        )

        sell_fee = cls.calculate_sell_fee(
            sell_value
        )

        return buy_fee + sell_fee

    # =====================================================
    # DETAIL
    # =====================================================

    @classmethod
    def calculate(
        cls,
        buy_value,
        sell_value
    ):

        buy_fee = cls.calculate_buy_fee(
            buy_value
        )

        sell_fee = cls.calculate_sell_fee(
            sell_value
        )

        total_fee = (
            buy_fee +
            sell_fee
        )

        return {

            "buy_value":
                float(buy_value),

            "sell_value":
                float(sell_value),

            "buy_fee":
                buy_fee,

            "sell_fee":
                sell_fee,

            "total_fee":
                total_fee

        }