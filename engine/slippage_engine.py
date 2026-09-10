class SlippageEngine:
    """
    Menghitung slippage transaksi BUY dan SELL.
    """

    DEFAULT_SLIPPAGE_RATE = 0.001

    # =====================================================
    # BUY PRICE
    # =====================================================

    @staticmethod
    def calculate_buy_price(
        buy_price,
        slippage_rate=DEFAULT_SLIPPAGE_RATE
    ):

        buy_price = float(buy_price)
        slippage_rate = float(slippage_rate)

        return (
            buy_price *
            (1 + slippage_rate)
        )

    # =====================================================
    # SELL PRICE
    # =====================================================

    @staticmethod
    def calculate_sell_price(
        sell_price,
        slippage_rate=DEFAULT_SLIPPAGE_RATE
    ):

        sell_price = float(sell_price)
        slippage_rate = float(slippage_rate)

        return (
            sell_price *
            (1 - slippage_rate)
        )

    # =====================================================
    # CALCULATE
    # =====================================================

    @classmethod
    def calculate(
        cls,
        buy_price,
        sell_price,
        slippage_rate=DEFAULT_SLIPPAGE_RATE
    ):

        buy_price = float(buy_price)

        sell_price = float(sell_price)

        slippage_rate = float(slippage_rate)

        # -------------------------------------------------
        # Actual BUY
        # -------------------------------------------------

        actual_buy = cls.calculate_buy_price(

            buy_price,

            slippage_rate

        )

        # -------------------------------------------------
        # Actual SELL
        # -------------------------------------------------

        actual_sell = cls.calculate_sell_price(

            sell_price,

            slippage_rate

        )

        # -------------------------------------------------
        # Slippage
        # -------------------------------------------------

        buy_slippage = (

            actual_buy -
            buy_price

        )

        sell_slippage = (

            sell_price -
            actual_sell

        )

        # -------------------------------------------------
        # Result
        # -------------------------------------------------

        return {

            "buy_price": buy_price,

            "sell_price": sell_price,

            "actual_buy": actual_buy,

            "actual_sell": actual_sell,

            "buy_slippage": buy_slippage,

            "sell_slippage": sell_slippage,

            "slippage_rate": slippage_rate

        }