from storage.trade_history import TradeHistory


class TradeManagerEngine:

    def __init__(self):

        self.history = TradeHistory()

    # =====================================
    # Cek apakah trade masih OPEN
    # =====================================

    def is_trade_open(self, code):

        trades = self.history.get_all_trades()

        for trade in trades:

            if (
                trade["code"] == code
                and trade["status"] == "OPEN"
            ):

                return True

        return False

    # =====================================
    # Simpan Trade Baru
    # =====================================

    def save_trade(self, trade_data):

        code = trade_data["code"]

        if self.is_trade_open(code):

            return False

        self.history.save_trade(trade_data)

        return True

    # =====================================
    # Update Trade
    # =====================================

    def update_trade(self, trade_id, data):

        conn = sqlite3.connect(
            self.db_name
        )

        cursor = conn.cursor()

        cursor.execute(

        """
        UPDATE trade_history

        SET

            status = ?,

            profit = ?,

            exit_price = ?,

            gross_profit = ?,

            total_cost = ?,

            net_profit = ?

        WHERE id = ?

        """,

        (

            data.get(
                "status",
                "OPEN"
            ),

            data.get(
                "profit",
                0
            ),

            data.get(
                "exit_price",
                0
            ),

            data.get(
                "gross_profit",
                0
            ),

            data.get(
                "total_cost",
                0
            ),

            data.get(
                "net_profit",
                0
            ),

            trade_id

        )

    )

    conn.commit()

    conn.close()

    # =====================================
    # Tutup Trade
    # =====================================

    def close_trade(self, trade_id):

        self.history.update_trade(
            trade_id,
            {
                "status": "CLOSED"
            }
        )

    # =====================================
    # Ambil Semua Trade
    # =====================================

    def get_all_trades(self):

        return self.history.get_all_trades()