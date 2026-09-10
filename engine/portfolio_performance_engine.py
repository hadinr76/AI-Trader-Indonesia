from storage.trade_history import TradeHistory
from engine.performance_tracker_engine import PerformanceTrackerEngine


class PortfolioPerformanceEngine:

    # ============================================================
    # INITIAL CAPITAL
    # ============================================================

    def __init__(self, initial_capital=100_000_000):

        self.initial_capital = float(
            initial_capital
        )

        self.history = TradeHistory()

    # ============================================================
    # GET TRADES
    # ============================================================

    def get_trades(self):

        return self.history.get_all_trades()

    # ============================================================
    # OPEN TRADES
    # ============================================================

    def get_open_trades(self):

        trades = self.get_trades()

        return [

            trade

            for trade in trades

            if trade["status"] != "CLOSED"

        ]

    # ============================================================
    # CLOSED TRADES
    # ============================================================

    def get_closed_trades(self):

        trades = self.get_trades()

        return [

            trade

            for trade in trades

            if trade["status"] == "CLOSED"

        ]

    # ============================================================
    # INVESTMENT
    # ============================================================

    def investment(self):

        open_trades = self.get_open_trades()

        total = 0

        for trade in open_trades:

            investment = float(
                trade["investment"] or 0
            )

            total += investment

        return total

    # ============================================================
    # REALIZED PROFIT
    # ============================================================

    def realized_profit(self):

        closed_trades = self.get_closed_trades()

        total = 0

        for trade in closed_trades:

            profit = float(
                trade["net_profit"] or 0
            )

            total += profit

        return total

    # ============================================================
    # UNREALIZED PROFIT
    # ============================================================

    def unrealized_profit(self):

        open_trades = self.get_open_trades()

        total = 0

        for trade in open_trades:

            profit = float(
                trade["net_profit"] or 0
            )

            total += profit

        return total

    # ============================================================
    # TOTAL PROFIT
    # ============================================================

    def total_profit(self):

        return (

            self.realized_profit()

            +

            self.unrealized_profit()

        )

    # ============================================================
    # CASH
    # ============================================================

    def cash(self):

        return (

            self.initial_capital

            -

            self.investment()

            +

            self.realized_profit()

        )

    # ============================================================
    # EQUITY
    # ============================================================

    def equity(self):

        return (

            self.cash()

            +

            self.investment()

            +

            self.unrealized_profit()

        )

    # ============================================================
    # RETURN
    # ============================================================

    def return_pct(self):

        if self.initial_capital <= 0:

            return 0

        return (

            (

                self.equity()

                -

                self.initial_capital

            )

            /

            self.initial_capital

        ) * 100

    # ============================================================
    # STATUS
    # ============================================================

    def status(self):

        equity = self.equity()

        if equity > self.initial_capital:

            return "PROFIT"

        if equity < self.initial_capital:

            return "LOSS"

        return "BREAKEVEN"

    # ============================================================
    # PERFORMANCE
    # ============================================================

    def performance(self):

        return PerformanceTrackerEngine.statistics()

    # ============================================================
    # SUMMARY
    # ============================================================

    def summary(self):

        performance = self.performance()

        return {

            "initial_capital":
                round(
                    self.initial_capital,
                    2
                ),

            "cash":
                round(
                    self.cash(),
                    2
                ),

            "investment":
                round(
                    self.investment(),
                    2
                ),

            "equity":
                round(
                    self.equity(),
                    2
                ),

            "realized_profit":
                round(
                    self.realized_profit(),
                    2
                ),

            "unrealized_profit":
                round(
                    self.unrealized_profit(),
                    2
                ),

            "total_profit":
                round(
                    self.total_profit(),
                    2
                ),

            "return_pct":
                round(
                    self.return_pct(),
                    2
                ),

            "open_position":
                len(
                    self.get_open_trades()
                ),

            "closed_position":
                len(
                    self.get_closed_trades()
                ),

            "status":
                self.status(),

            "total_trade":
                performance[
                    "total_trade"
                ],

            "winning_trade":
                performance[
                    "winning_trade"
                ],

            "losing_trade":
                performance[
                    "losing_trade"
                ],

            "win_rate":
                performance[
                    "win_rate"
                ],

            "average_win":
                performance[
                    "average_win"
                ],

            "average_loss":
                performance[
                    "average_loss"
                ],

            "profit_factor":
                performance[
                    "profit_factor"
                ]

        }