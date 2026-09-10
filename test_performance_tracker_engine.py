from storage.trade_history import TradeHistory
from data.market_data import MarketData
from engine.trade_cost_engine import TradeCostEngine


class PerformanceTrackerEngine:

    # =====================================================
    # PERFORMANCE STATISTICS
    # =====================================================

    @staticmethod
    def statistics():

        history = TradeHistory()

        trades = history.get_all_trades()

        # =================================================
        # Jika belum ada transaksi
        # =================================================

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

        # =================================================
        # Pisahkan OPEN dan CLOSED
        # =================================================

        closed_trades = []

        open_trades = []

        for trade in trades:

            status = trade["status"]

            if status == "OPEN":

                open_trades.append(trade)

            else:

                closed_trades.append(trade)

        # =================================================
        # Profit
        # =================================================

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

        # =================================================
        # TOTAL
        # =================================================

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

        # =================================================
        # WIN RATE
        # =================================================

        if closed_trade > 0:

            win_rate = (

                winning_trade /
                closed_trade

            ) * 100

        else:

            win_rate = 0

        # =================================================
        # TOTAL PROFIT
        # =================================================

        total_profit = sum(
            profits
        )

        # =================================================
        # AVERAGE PROFIT
        # =================================================

        if closed_trade > 0:

            average_profit = (

                total_profit /
                closed_trade

            )

        else:

            average_profit = 0

        # =================================================
        # AVERAGE WIN
        # =================================================

        if winning_trade > 0:

            average_win = (

                sum(winning) /
                winning_trade

            )

        else:

            average_win = 0

        # =================================================
        # AVERAGE LOSS
        # =================================================

        if losing_trade > 0:

            average_loss = (

                sum(losing) /
                losing_trade

            )

        else:

            average_loss = 0

        # =================================================
        # PROFIT FACTOR
        # =================================================

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

        # =================================================
        # RESULT
        # =================================================

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

    # =====================================================
    # UPDATE TRADE
    #
    # Memeriksa posisi OPEN:
    #
    # STOP LOSS
    # TARGET 1
    # TARGET 2
    #
    # Kemudian menghitung NET PROFIT
    # menggunakan TradeCostEngine.
    # =====================================================

    @staticmethod
    def update():

        history = TradeHistory()

        market = MarketData()

        trades = history.get_all_trades()

        results = []

        # =================================================
        # LOOP SEMUA TRADE
        # =================================================

        for trade in trades:

            # -------------------------------------------------
            # Hanya proses posisi OPEN
            # -------------------------------------------------

            if trade["status"] != "OPEN":

                continue

            # -------------------------------------------------
            # Ambil data trade
            # -------------------------------------------------

            trade_id = trade["id"]

            code = trade["code"]

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

            # -------------------------------------------------
            # Jumlah saham
            #
            # TradeHistory lama belum memiliki kolom shares.
            #
            # Karena itu kita cari dari:
            #
            # investment / entry
            #
            # Jika investment tidak tersedia,
            # gunakan 0 agar tidak menyebabkan error.
            # -------------------------------------------------

            investment = float(
                trade["price"] or 0
            )

            # -------------------------------------------------
            # Ambil harga pasar terbaru
            # -------------------------------------------------

            try:

                data = market.get_daily(
                    code
                )

            except Exception:

                continue

            # -------------------------------------------------
            # Pastikan data tersedia
            # -------------------------------------------------

            if data is None:

                continue

            if "Close" not in data.columns:

                continue

            close_series = (
                data["Close"]
                .dropna()
            )

            if close_series.empty:

                continue

            close = float(
                close_series.iloc[-1]
            )

            # =================================================
            # TENTUKAN STATUS
            # =================================================

            new_status = None

            # -------------------------------------------------
            # STOP LOSS
            # -------------------------------------------------

            if close <= stop_loss:

                new_status = "STOP LOSS"

            # -------------------------------------------------
            # TARGET 2
            # -------------------------------------------------

            elif close >= target2:

                new_status = "TARGET 2"

            # -------------------------------------------------
            # TARGET 1
            # -------------------------------------------------

            elif close >= target1:

                new_status = "TARGET1"

            # -------------------------------------------------
            # Belum mencapai target
            # -------------------------------------------------

            else:

                continue

            # =================================================
            # HITUNG SHARES
            # =================================================
            #
            # TradeHistory saat ini tidak memiliki field shares.
            #
            # Kita menggunakan:
            #
            # investment = price
            #
            # sehingga untuk sementara kita perlu menentukan
            # jumlah saham dari nilai transaksi yang tersedia.
            #
            # Jika tidak dapat dihitung, profit akan dihitung
            # berdasarkan pergerakan harga.
            # =================================================

            shares = 0

            if investment > 0 and entry > 0:

                shares = int(
                    investment / entry
                )

            # =================================================
            # Jika shares tidak tersedia
            # =================================================

            if shares <= 0:

                shares = 1

            # =================================================
            # HITUNG TRADE COST
            # =================================================

            try:

                cost = TradeCostEngine.calculate(

                    entry_price=entry,

                    exit_price=close,

                    shares=shares

                )

            except Exception:

                continue

            # =================================================
            # NET PROFIT
            # =================================================

            net_profit = float(
                cost.get(
                    "net_profit",
                    0
                )
            )

            # =================================================
            # UPDATE DATABASE
            # =================================================

            history.update_trade(

                trade_id,

                {

                    "status": new_status,

                    "profit": net_profit

                }

            )

            # =================================================
            # SIMPAN HASIL
            # =================================================

            results.append({

                "id": trade_id,

                "code": code,

                "entry": entry,

                "close": close,

                "shares": shares,

                "status": new_status,

                "gross_profit":
                    cost.get(
                        "gross_profit",
                        0
                    ),

                "total_cost":
                    cost.get(
                        "total_cost",
                        0
                    ),

                "net_profit":
                    net_profit

            })

        return results