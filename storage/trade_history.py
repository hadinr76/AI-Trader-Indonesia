import sqlite3


class TradeHistory:
    """
    Mengelola penyimpanan dan pembaruan
    riwayat transaksi menggunakan SQLite.
    """

    def __init__(self):

        self.db_name = "storage/ai_trader.db"

        self.create_table()

    # =====================================================
    # CREATE TABLE
    # =====================================================

    def create_table(self):

        conn = sqlite3.connect(self.db_name)

        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS trade_history(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                date TEXT,

                code TEXT,

                recommendation TEXT,

                price REAL,

                entry REAL,

                stop_loss REAL,

                target1 REAL,

                target2 REAL,

                confidence REAL,

                overall_score REAL,

                ranking_score REAL,

                status TEXT,

                profit REAL,

                shares INTEGER,

                lots INTEGER,

                investment REAL,

                exit_price REAL,

                gross_profit REAL,

                total_cost REAL,

                net_profit REAL

            )
            """
        )

        conn.commit()

        conn.close()

    # =====================================================
    # SAVE TRADE
    # =====================================================

    def save_trade(self, trade):

        conn = sqlite3.connect(self.db_name)

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO trade_history(

                date,
                code,
                recommendation,
                price,
                entry,
                stop_loss,
                target1,
                target2,
                confidence,
                overall_score,
                ranking_score,
                status,
                profit,
                shares,
                lots,
                investment,
                exit_price,
                gross_profit,
                total_cost,
                net_profit

            )

            VALUES(

                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?

            )
            """,
            (
                trade.get("date", ""),

                trade.get("code", ""),

                trade.get(
                    "recommendation",
                    ""
                ),

                trade.get(
                    "price",
                    0
                ),

                trade.get(
                    "entry",
                    0
                ),

                trade.get(
                    "stop_loss",
                    0
                ),

                trade.get(
                    "target1",
                    0
                ),

                trade.get(
                    "target2",
                    0
                ),

                trade.get(
                    "confidence",
                    0
                ),

                trade.get(
                    "overall_score",
                    0
                ),

                trade.get(
                    "ranking_score",
                    0
                ),

                trade.get(
                    "status",
                    "OPEN"
                ),

                trade.get(
                    "profit",
                    0
                ),

                trade.get(
                    "shares",
                    0
                ),

                trade.get(
                    "lots",
                    0
                ),

                trade.get(
                    "investment",
                    0
                ),

                trade.get(
                    "exit_price",
                    0
                ),

                trade.get(
                    "gross_profit",
                    0
                ),

                trade.get(
                    "total_cost",
                    0
                ),

                trade.get(
                    "net_profit",
                    0
                )
            )
        )

        conn.commit()

        conn.close()

    # =====================================================
    # GET ALL TRADES
    # =====================================================

    def get_all_trades(self):

        conn = sqlite3.connect(self.db_name)

        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *

            FROM trade_history

            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()

        conn.close()

        return rows

    # =====================================================
    # GET TRADE BY ID
    # =====================================================

    def get_trade(self, trade_id):

        conn = sqlite3.connect(self.db_name)

        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *

            FROM trade_history

            WHERE id = ?
            """,
            (trade_id,)
        )

        row = cursor.fetchone()

        conn.close()

        return row

    # =====================================================
    # UPDATE TRADE
    # =====================================================

    def update_trade(
        self,
        trade_id,
        data
    ):

        conn = sqlite3.connect(self.db_name)

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

    # =====================================================
    # UPDATE FULL TRADE
    # =====================================================

    def update_full_trade(
        self,
        trade_id,
        data
    ):

        conn = sqlite3.connect(self.db_name)

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE trade_history

            SET

                date = ?,

                code = ?,

                recommendation = ?,

                price = ?,

                entry = ?,

                stop_loss = ?,

                target1 = ?,

                target2 = ?,

                confidence = ?,

                overall_score = ?,

                ranking_score = ?,

                status = ?,

                profit = ?,

                shares = ?,

                lots = ?,

                investment = ?,

                exit_price = ?,

                gross_profit = ?,

                total_cost = ?,

                net_profit = ?

            WHERE id = ?
            """,
            (
                data.get(
                    "date",
                    ""
                ),

                data.get(
                    "code",
                    ""
                ),

                data.get(
                    "recommendation",
                    ""
                ),

                data.get(
                    "price",
                    0
                ),

                data.get(
                    "entry",
                    0
                ),

                data.get(
                    "stop_loss",
                    0
                ),

                data.get(
                    "target1",
                    0
                ),

                data.get(
                    "target2",
                    0
                ),

                data.get(
                    "confidence",
                    0
                ),

                data.get(
                    "overall_score",
                    0
                ),

                data.get(
                    "ranking_score",
                    0
                ),

                data.get(
                    "status",
                    "OPEN"
                ),

                data.get(
                    "profit",
                    0
                ),

                data.get(
                    "shares",
                    0
                ),

                data.get(
                    "lots",
                    0
                ),

                data.get(
                    "investment",
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

    # =====================================================
    # DELETE TRADE
    # =====================================================

    def delete_trade(self, trade_id):

        conn = sqlite3.connect(self.db_name)

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM trade_history

            WHERE id = ?
            """,
            (trade_id,)
        )

        conn.commit()

        conn.close()

    # =====================================================
    # COUNT TRADES
    # =====================================================

    def count_trades(self):

        conn = sqlite3.connect(self.db_name)

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)

            FROM trade_history
            """
        )

        result = cursor.fetchone()

        conn.close()

        return result[0]

    # =====================================================
    # CLEAR HISTORY
    # =====================================================

    def clear_history(self):

        conn = sqlite3.connect(self.db_name)

        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM trade_history
            """
        )

        conn.commit()

        conn.close()