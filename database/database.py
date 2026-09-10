import sqlite3
from datetime import datetime


class Database:

    DB_NAME = "ai_trader.db"

    @staticmethod
    def connect():
        return sqlite3.connect(Database.DB_NAME)

    @staticmethod
    def initialize():

        conn = Database.connect()
        cursor = conn.cursor()

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS scan_history(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            scan_date TEXT,

            code TEXT,

            price REAL,

            technical_score REAL,

            fundamental_score REAL,

            overall_score REAL,

            decision_score REAL,

            confidence REAL,

            ranking_score REAL,

            scanner_score REAL,

            market_regime TEXT,

            recommendation TEXT,

            rating TEXT

        )

        """)

        conn.commit()
        conn.close()

    @staticmethod
    def save_scan(result):

        conn = Database.connect()
        cursor = conn.cursor()

        cursor.execute("""

        INSERT INTO scan_history(

            scan_date,
            code,
            price,
            technical_score,
            fundamental_score,
            overall_score,
            decision_score,
            confidence,
            ranking_score,
            scanner_score,
            market_regime,
            recommendation,
            rating

        )

        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)

        """, (

            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            result["code"],
            result["price"],
            result["technical_score"],
            result["fundamental_score"],
            result["overall_score"],
            result["decision_score"],
            result["confidence"],
            result["ranking_score"],
            result["scanner_score"],
            result["market_regime"],
            result["recommendation"],
            result["rating"]

        ))

        conn.commit()
        conn.close()

    @staticmethod
    def get_history(code):

        conn = Database.connect()
        cursor = conn.cursor()

        cursor.execute("""

        SELECT *

        FROM scan_history

        WHERE code=?

        ORDER BY id DESC

        """,(code,))

        data = cursor.fetchall()

        conn.close()

        return data