class Statistics:

    @staticmethod
    def calculate(trades):

        open_trades = [
            t for t in trades
            if t.get("status") == "OPEN"
        ]

        closed_trades = [
            t for t in trades
            if t.get("status") != "OPEN"
        ]

        open_trade = len(open_trades)

        total_trade = len(closed_trades)

        if total_trade == 0:

            return {

                "total_trade": 0,

                "win": 0,

                "loss": 0,

                "win_rate": 0,

                "average_profit": 0,

                "average_loss": 0,

                "gross_profit": 0,

                "gross_loss": 0,

                "net_profit": 0,

                "profit_factor": 0,

                "expectancy": 0

            }

        # =====================================
        # Pisahkan Trade Profit & Loss
        # =====================================

        win_trades = [

            t for t in closed_trades

            if t["profit"] > 0

        ]       

        loss_trades = [

            t for t in closed_trades

            if t["profit"] <= 0

        ]

        win = len(win_trades)

        loss = len(loss_trades)

        # =====================================
        # Gross Profit
        # =====================================

        gross_profit = sum(

            t["profit"]

            for t in win_trades

        )

        # =====================================
        # Gross Loss
        # =====================================

        gross_loss = abs(sum(

            t["profit"]

            for t in loss_trades

        ))

        # =====================================
        # Average Profit
        # =====================================

        average_profit = (

            gross_profit / win

            if win > 0 else 0

        )

        # =====================================
        # Average Loss
        # =====================================

        average_loss = (

            gross_loss / loss

            if loss > 0 else 0

        )

        # =====================================
        # Net Profit
        # =====================================

        net_profit = (

            gross_profit -

            gross_loss

        )

        # =====================================
        # Win Rate
        # =====================================

        win_rate = (

            win / total_trade

        ) * 100

        # =====================================
        # Profit Factor
        # =====================================

        if gross_loss == 0:

            if gross_profit > 0:
                profit_factor = float("inf")
            else:
                profit_factor = 0

        else:

            profit_factor = (

                gross_profit /

                gross_loss

            )

        # =====================================
        # Expectancy
        # =====================================

        expectancy = (

            net_profit /

            total_trade

        )

        return {

            "total_trade": total_trade,

            "open_trade": open_trade,

            "win": win,

            "loss": loss,

            "win_rate": round(win_rate, 2),

            "average_profit": round(

                average_profit,

                2

            ),

            "average_loss": round(

                average_loss,

                2

            ),

            "gross_profit": round(

                gross_profit,

                2

            ),

            "gross_loss": round(

                gross_loss,

                2

            ),

            "net_profit": round(

                net_profit,

                2

            ),

            "profit_factor": round(

                profit_factor,

                2

            ),

            "expectancy": round(

                expectancy,

                2

            )

        }