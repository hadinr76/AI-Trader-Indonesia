from storage.trade_history import TradeHistory
from data.market_data import MarketData
from engine.trade_cost_engine import TradeCostEngine


class PerformanceTrackerEngine:

    # ============================================================
    # UPDATE OPEN TRADE
    # ============================================================

    @staticmethod
    def update():

        history = TradeHistory()
        market = MarketData()

        trades = history.get_all_trades()

        for trade in trades:

            # ----------------------------------------------------
            # HANYA PROSES POSISI OPEN
            # ----------------------------------------------------

            if trade["status"] != "OPEN":
                continue

            code = trade["code"]

            try:

                data = market.get_daily(code)

            except Exception:

                continue

            # ----------------------------------------------------
            # AMBIL HARGA TERAKHIR
            # ----------------------------------------------------

            try:

                close = float(
                    data["Close"].dropna().iloc[-1]
                )

            except Exception:

                continue

            # ----------------------------------------------------
            # DATA TRANSAKSI
            # ----------------------------------------------------

            entry = float(
                trade["entry"] or 0
            )

            stop_loss = float(
                trade["stop_loss"] or 0
            )

            target1 = float(
                trade["target1"] or 0
            )

            target2 = float(
                trade["target2"] or 0
            )

            shares = int(
                trade["shares"] or 0
            )

            # ----------------------------------------------------
            # VALIDASI SHARES
            # ----------------------------------------------------

            if shares <= 0:

                continue

            # ====================================================
            # TENTUKAN STATUS
            # ====================================================

            new_status = "OPEN"

            if close <= stop_loss:

                new_status = "CLOSED"

            elif close >= target2:

                new_status = "CLOSED"

            elif close >= target1:

                new_status = "TARGET1"

            # ====================================================
            # HITUNG BIAYA DAN PROFIT
            # ====================================================

            cost = TradeCostEngine.calculate(

                entry_price=entry,

                exit_price=close,

                shares=shares

            )

            # ====================================================
            # SIMPAN HASIL
            # ====================================================

            update_data = {

                "status": new_status,

                "profit": cost["net_profit"],

                "exit_price": close,

                "gross_profit": cost["gross_profit"],

                "total_cost": cost["total_cost"],

                "net_profit": cost["net_profit"]

            }

            # ----------------------------------------------------
            # UPDATE DATABASE
            # ----------------------------------------------------

            history.update_trade(

                trade["id"],

                update_data

            )


    # ============================================================
    # PERFORMANCE STATISTICS
    # ============================================================

    @staticmethod
    def statistics():

        history = TradeHistory()

        trades = history.get_all_trades()

        # --------------------------------------------------------
        # BELUM ADA TRANSAKSI
        # --------------------------------------------------------

        if not trades:

            return {

                "total_trade": 0,

                "closed_trade": 0,

                "open_trade": 0,

                "winning_trade": 0,

                "losing_trade": 0,

                "win_rate": 0,

                "total_profit": 0,

                "average_profit": 0,

                "average_win": 0,

                "average_loss": 0,

                "profit_factor": 0

            }

        # --------------------------------------------------------
        # PISAHKAN OPEN DAN CLOSED
        # --------------------------------------------------------

        closed_trades = []

        open_trades = []

        for trade in trades:

            status = trade["status"]

            if status == "CLOSED":

                closed_trades.append(trade)

            else:

                open_trades.append(trade)
                

        # --------------------------------------------------------
        # PROFIT
        # --------------------------------------------------------

        profits = []

        winning = []

        losing = []

        for trade in closed_trades:

            profit = float(
                trade["profit"] or 0
            )

            profits.append(profit)

            if profit > 0:

                winning.append(profit)

            elif profit < 0:

                losing.append(profit)

        # --------------------------------------------------------
        # JUMLAH TRANSAKSI
        # --------------------------------------------------------

        total_trade = len(trades)

        closed_trade = len(
            closed_trades
        )

        open_trade = len(
            open_trades
        )

        winning_trade = len(
            winning
        )

        losing_trade = len(
            losing
        )

        # --------------------------------------------------------
        # WIN RATE
        # --------------------------------------------------------

        if closed_trade > 0:

            win_rate = (

                winning_trade /
                closed_trade

            ) * 100

        else:

            win_rate = 0

        # --------------------------------------------------------
        # TOTAL PROFIT
        # --------------------------------------------------------

        total_profit = sum(
            profits
        )

        # --------------------------------------------------------
        # AVERAGE PROFIT
        # --------------------------------------------------------

        if closed_trade > 0:

            average_profit = (

                total_profit /
                closed_trade

            )

        else:

            average_profit = 0

        # --------------------------------------------------------
        # AVERAGE WIN
        # --------------------------------------------------------

        if winning_trade > 0:

            average_win = (

                sum(winning) /
                winning_trade

            )

        else:

            average_win = 0

        # --------------------------------------------------------
        # AVERAGE LOSS
        # --------------------------------------------------------

        if losing_trade > 0:

            average_loss = (

                sum(losing) /
                losing_trade

            )

        else:

            average_loss = 0

        # --------------------------------------------------------
        # PROFIT FACTOR
        # --------------------------------------------------------

        gross_profit = sum(
            winning
        )

        gross_loss = abs(
            sum(losing)
        )

        if gross_loss > 0:

            profit_factor = (

                gross_profit /
                gross_loss

            )

        else:

            profit_factor = 0

        # --------------------------------------------------------
        # RESULT
        # --------------------------------------------------------

        return {

            "total_trade":
                total_trade,

            "closed_trade":
                closed_trade,

            "open_trade":
                open_trade,

            "winning_trade":
                winning_trade,

            "losing_trade":
                losing_trade,

            "win_rate":
                round(
                    win_rate,
                    2
                ),

            "total_profit":
                round(
                    total_profit,
                    2
                ),

            "average_profit":
                round(
                    average_profit,
                    2
                ),

            "average_win":
                round(
                    average_win,
                    2
                ),

            "average_loss":
                round(
                    average_loss,
                    2
                ),

            "profit_factor":
                round(
                    profit_factor,
                    2
                )

        }