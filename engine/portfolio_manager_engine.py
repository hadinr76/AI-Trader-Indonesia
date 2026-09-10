from storage.trade_history import TradeHistory


class PortfolioManagerEngine:

    @staticmethod
    def calculate(initial_capital=100_000_000):

        history = TradeHistory()

        trades = history.get_all_trades()

        open_position = 0
        closed_position = 0

        total_profit = 0

        invested = 0

        win = 0
        loss = 0

        for trade in trades:

            profit = trade["profit"] or 0

            total_profit += profit

            if trade["status"] == "OPEN":

                open_position += 1
                invested += trade["entry"]

            else:

                closed_position += 1

                if profit > 0:
                    win += 1

                elif profit < 0:
                    loss += 1

        cash = initial_capital - invested

        equity = cash + invested + total_profit

        total_trade = win + loss

        if total_trade > 0:

            win_rate = (win / total_trade) * 100

        else:

            win_rate = 0

        if total_profit > 0:

            status = "PROFIT"

        elif total_profit < 0:

            status = "LOSS"

        else:

            status = "BREAKEVEN"

        return {

            "capital": initial_capital,

            "cash": cash,

            "investment": invested,

            "equity": equity,

            "profit": total_profit,

            "return": round(
                (total_profit / initial_capital) * 100,
                2
            ),

            "open_position": open_position,

            "closed_position": closed_position,

            "win": win,

            "loss": loss,

            "win_rate": round(win_rate, 2),

            "status": status

        }