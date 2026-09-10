from risk.broker_fee_engine import BrokerFeeEngine
from risk.tax_engine import TaxEngine
from risk.slippage_engine import SlippageEngine


class TradeCostEngine:

    @staticmethod
    def calculate(

        entry_price,
        exit_price,
        shares

    ):

        # ==========================================
        # Slippage
        # ==========================================

        actual_buy = SlippageEngine.buy_price(

            entry_price

        )

        actual_sell = SlippageEngine.sell_price(

            exit_price

        )

        # ==========================================
        # Nilai transaksi
        # ==========================================

        buy_value = actual_buy * shares

        sell_value = actual_sell * shares

        # ==========================================
        # Broker Fee
        # ==========================================

        buy_fee = BrokerFeeEngine.calculate_buy_fee(

            buy_value

        )

        sell_fee = BrokerFeeEngine.calculate_sell_fee(

            sell_value

        )

        # ==========================================
        # Pajak
        # ==========================================

        tax = TaxEngine.calculate_sell_tax(

            sell_value

        )

        # ==========================================
        # Profit
        # ==========================================

        gross_profit = sell_value - buy_value

        total_cost = (

            buy_fee +

            sell_fee +

            tax

        )

        net_profit = (

            gross_profit -

            total_cost

        )

        return {

            "entry_price": entry_price,

            "exit_price": exit_price,

            "actual_buy": actual_buy,

            "actual_sell": actual_sell,

            "buy_value": round(buy_value, 2),

            "sell_value": round(sell_value, 2),

            "buy_fee": buy_fee,

            "sell_fee": sell_fee,

            "tax": tax,

            "gross_profit": round(gross_profit, 2),

            "total_cost": round(total_cost, 2),

            "net_profit": round(net_profit, 2)

        }