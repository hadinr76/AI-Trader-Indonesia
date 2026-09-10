from datetime import datetime


class PositionEngine:
    """
    Menyimpan dan mengelola satu posisi trading.
    """

    def __init__(

        self,

        code,
        entry_date,
        entry_price,
        shares,
        lots,
        stop_loss,
        target1,
        target2,
        recommendation="BUY"

    ):

        self.code = code

        self.entry_date = entry_date

        self.entry_price = float(entry_price)

        self.shares = int(shares)

        self.lots = int(lots)

        self.stop_loss = float(stop_loss)

        self.target1 = float(target1)

        self.target2 = float(target2)

        self.recommendation = recommendation

        self.status = "OPEN"

        self.exit_date = None

        self.exit_price = None

        self.profit = 0

        self.return_pct = 0

        self.holding_days = 0

    # ===================================================
    # Update harga harian
    # ===================================================

    def update(

        self,

        close_price

    ):

        if self.status != "OPEN":

            return

        self.profit = (

            close_price -

            self.entry_price

        ) * self.shares

        self.return_pct = (

            (close_price - self.entry_price)

            / self.entry_price

        ) * 100

    # ===================================================
    # Tambah holding day
    # ===================================================

    def next_day(self):

        if self.status == "OPEN":

            self.holding_days += 1

    # ===================================================
    # Tutup posisi
    # ===================================================

    def close(

        self,

        exit_price,
        exit_date=None,
        status="CLOSED"

    ):

        self.exit_price = float(exit_price)

        self.exit_date = exit_date

        self.status = status

        self.profit = (

            self.exit_price -

            self.entry_price

        ) * self.shares

        self.return_pct = (

            (self.exit_price - self.entry_price)

            / self.entry_price

        ) * 100

    # ===================================================
    # Nilai investasi
    # ===================================================

    @property
    def investment(self):

        return self.entry_price * self.shares

    # ===================================================
    # Export ke dictionary
    # ===================================================

    def to_dict(self):

        return {

            "code": self.code,

            "entry_date": self.entry_date,

            "entry_price": self.entry_price,

            "shares": self.shares,

            "lots": self.lots,

            "investment": self.investment,

            "stop_loss": self.stop_loss,

            "target1": self.target1,

            "target2": self.target2,

            "recommendation": self.recommendation,

            "status": self.status,

            "exit_date": self.exit_date,

            "exit_price": self.exit_price,

            "profit": self.profit,

            "return_pct": round(self.return_pct, 2),

            "holding_days": self.holding_days

        }

    # ===================================================
    # Print object
    # ===================================================

    def __str__(self):

        return (

            f"{self.code} | "

            f"{self.status} | "

            f"Entry {self.entry_price} | "

            f"Profit {self.profit:,.0f}"

        )