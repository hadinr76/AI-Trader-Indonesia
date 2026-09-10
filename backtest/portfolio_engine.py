from backtest.position_engine import PositionEngine
from backtest.order_engine import OrderEngine


class PortfolioEngine:
    """
    Mengelola modal, posisi terbuka, posisi tertutup,
    cash, investment, equity, dan profit portofolio.
    """

    def __init__(self, initial_capital):

        self.initial_capital = float(initial_capital)

        self.cash = float(initial_capital)

        self.positions = []

        self.closed_positions = []

    # =====================================================
    # BUY / OPEN POSITION
    # =====================================================

    def buy(

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

        # ---------------------------------------------
        # Cek apakah posisi sudah ada
        # ---------------------------------------------

        if not OrderEngine.can_buy(

            self.positions,

            code

        ):

            return {

                "approved": False,

                "reason": "POSITION ALREADY OPEN",

                "position": None

            }

        # ---------------------------------------------
        # Hitung investasi
        # ---------------------------------------------

        investment = (

            float(entry_price) *

            int(shares)

        )

        # ---------------------------------------------
        # Cek cash
        # ---------------------------------------------

        if investment > self.cash:

            return {

                "approved": False,

                "reason": "INSUFFICIENT CASH",

                "position": None

            }

        # ---------------------------------------------
        # Buat posisi
        # ---------------------------------------------

        position = PositionEngine(

            code=code,

            entry_date=entry_date,

            entry_price=entry_price,

            shares=shares,

            lots=lots,

            stop_loss=stop_loss,

            target1=target1,

            target2=target2,

            recommendation=recommendation

        )

        # ---------------------------------------------
        # Simpan posisi
        # ---------------------------------------------

        self.positions.append(position)

        # ---------------------------------------------
        # Kurangi cash
        # ---------------------------------------------

        self.cash -= investment

        return {

            "approved": True,

            "reason": "BUY APPROVED",

            "position": position

        }

    # =====================================================
    # SELL / CLOSE POSITION
    # =====================================================

    def sell(

        self,
        code,
        exit_price,
        exit_date,
        status="CLOSED"

    ):

        # ---------------------------------------------
        # Cari posisi
        # ---------------------------------------------

        position = OrderEngine.get_open_position(

            self.positions,

            code

        )

        # ---------------------------------------------
        # Tidak ditemukan
        # ---------------------------------------------

        if position is None:

            return {

                "approved": False,

                "reason": "NO OPEN POSITION",

                "position": None

            }

        # ---------------------------------------------
        # Tutup posisi
        # ---------------------------------------------

        position.close(

            exit_price=exit_price,

            exit_date=exit_date,

            status=status

        )

        # ---------------------------------------------
        # Kembalikan nilai penjualan ke cash
        # ---------------------------------------------

        sell_value = (

            float(exit_price) *

            position.shares

        )

        self.cash += sell_value

        # ---------------------------------------------
        # Pindahkan ke closed position
        # ---------------------------------------------

        self.closed_positions.append(position)

        return {

            "approved": True,

            "reason": "SELL EXECUTED",

            "position": position

        }

    # =====================================================
    # UPDATE SEMUA POSISI
    # =====================================================

    def update_prices(

        self,
        prices

    ):

        for position in self.positions:

            if position.status != "OPEN":

                continue

            code = position.code

            if code not in prices:

                continue

            position.update(

                float(prices[code])

            )

    # =====================================================
    # NEXT DAY
    # =====================================================

    def next_day(self):

        for position in self.positions:

            if position.status == "OPEN":

                position.next_day()

    # =====================================================
    # OPEN POSITIONS
    # =====================================================

    def get_open_positions(self):

        return [

            position

            for position in self.positions

            if position.status == "OPEN"

        ]

    # =====================================================
    # CLOSED POSITIONS
    # =====================================================

    def get_closed_positions(self):

        return self.closed_positions.copy()

    # =====================================================
    # JUMLAH POSISI
    # =====================================================

    def open_position_count(self):

        return len(

            self.get_open_positions()

        )

    def closed_position_count(self):

        return len(

            self.closed_positions

        )

    # =====================================================
    # TOTAL INVESTMENT
    # =====================================================

    def investment(self):

        total = 0

        for position in self.get_open_positions():

            total += position.investment

        return total

    # =====================================================
    # FLOATING PROFIT
    # =====================================================

    def floating_profit(self):

        total = 0

        for position in self.get_open_positions():

            total += position.profit

        return total

    # =====================================================
    # REALIZED PROFIT
    # =====================================================

    def realized_profit(self):

        total = 0

        for position in self.closed_positions:

            total += position.profit

        return total

    # =====================================================
    # EQUITY
    # =====================================================

    def equity(self):

        return (

            self.cash +

            self.investment() +

            self.floating_profit()

        )

    # =====================================================
    # TOTAL PROFIT
    # =====================================================

    def total_profit(self):

        return (

            self.realized_profit() +

            self.floating_profit()

        )

    # =====================================================
    # RETURN
    # =====================================================

    def return_pct(self):

        return (

            self.total_profit() /

            self.initial_capital

        ) * 100

    # =====================================================
    # EXPOSURE
    # =====================================================

    def exposure_pct(self):

        if self.initial_capital == 0:

            return 0

        return (

            self.investment() /

            self.initial_capital

        ) * 100

    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(self):

        return {

            "initial_capital":
                self.initial_capital,

            "cash":
                self.cash,

            "investment":
                self.investment(),

            "equity":
                self.equity(),

            "floating_profit":
                self.floating_profit(),

            "realized_profit":
                self.realized_profit(),

            "total_profit":
                self.total_profit(),

            "return":
                self.return_pct(),

            "exposure":
                self.exposure_pct(),

            "open_position":
                self.open_position_count(),

            "closed_position":
                self.closed_position_count()

        }