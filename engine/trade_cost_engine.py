from engine.broker_fee_engine import BrokerFeeEngine
from engine.tax_engine import TaxEngine
from engine.slippage_engine import SlippageEngine


class TradeCostEngine:

    @staticmethod
    def calculate(
        entry_price,
        exit_price,
        shares,
        slippage_rate=0.001
    ):
        """
        Menghitung seluruh biaya transaksi:

        1. Slippage BUY
        2. Slippage SELL
        3. Broker Fee BUY
        4. Broker Fee SELL
        5. Tax SELL
        6. Gross Profit
        7. Total Cost
        8. Net Profit
        """

        entry_price = float(entry_price)
        exit_price = float(exit_price)
        shares = int(shares)

        # =====================================================
        # SLIPPAGE
        # =====================================================

        slippage = SlippageEngine.calculate(
            buy_price=entry_price,
            sell_price=exit_price,
            slippage_rate=slippage_rate
        )

        actual_buy = slippage["actual_buy"]

        actual_sell = slippage["actual_sell"]

        # =====================================================
        # BUY VALUE
        # =====================================================

        buy_value = actual_buy * shares

        # =====================================================
        # SELL VALUE
        # =====================================================

        sell_value = actual_sell * shares

        # =====================================================
        # BROKER FEE
        # =====================================================

        buy_fee = BrokerFeeEngine.calculate_buy_fee(
            buy_value
        )

        sell_fee = BrokerFeeEngine.calculate_sell_fee(
            sell_value
        )

        # =====================================================
        # TAX
        # =====================================================

        tax_result = TaxEngine.calculate(
            sell_value
        )

        tax = tax_result["tax"]

        # =====================================================
        # GROSS PROFIT
        # =====================================================

        gross_profit = (

            sell_value
            - buy_value

        )

        # =====================================================
        # TOTAL COST
        # =====================================================

        total_cost = (

            buy_fee
            + sell_fee
            + tax

        )

        # =====================================================
        # NET PROFIT
        # =====================================================

        net_profit = (

            gross_profit
            - total_cost

        )

        # =====================================================
        # RETURN
        # =====================================================

        if buy_value > 0:

            return_pct = (

                net_profit
                / buy_value

            ) * 100

        else:

            return_pct = 0

        # =====================================================
        # RESULT
        # =====================================================

        return {

            "entry_price": entry_price,

            "exit_price": exit_price,

            "actual_buy": actual_buy,

            "actual_sell": actual_sell,

            "shares": shares,

            "buy_value": buy_value,

            "sell_value": sell_value,

            "buy_fee": buy_fee,

            "sell_fee": sell_fee,

            "tax": tax,

            "gross_profit": gross_profit,

            "total_cost": total_cost,

            "net_profit": net_profit,

            "return_pct": return_pct

        }