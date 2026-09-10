class SlippageEngine:
    """
    Menghitung slippage transaksi.

    Default slippage:
    0.10%

    BUY  : harga menjadi lebih mahal
    SELL : harga menjadi lebih murah
    """

    DEFAULT_SLIPPAGE = 0.001

    @classmethod
    def buy_price(
        cls,
        price,
        slippage=None
    ):

        if slippage is None:
            slippage = cls.DEFAULT_SLIPPAGE

        actual_price = price * (1 + slippage)

        return round(actual_price, 2)

    @classmethod
    def sell_price(
        cls,
        price,
        slippage=None
    ):

        if slippage is None:
            slippage = cls.DEFAULT_SLIPPAGE

        actual_price = price * (1 - slippage)

        return round(actual_price, 2)

    @classmethod
    def calculate(
        cls,
        buy_price,
        sell_price,
        slippage=None
    ):

        actual_buy = cls.buy_price(
            buy_price,
            slippage
        )

        actual_sell = cls.sell_price(
            sell_price,
            slippage
        )

        return {

            "buy_price": buy_price,
            "sell_price": sell_price,

            "actual_buy": actual_buy,
            "actual_sell": actual_sell,

            "buy_slippage": round(
                actual_buy - buy_price,
                2
            ),

            "sell_slippage": round(
                sell_price - actual_sell,
                2
            ),

            "slippage_rate":

                cls.DEFAULT_SLIPPAGE
                if slippage is None
                else slippage

        }