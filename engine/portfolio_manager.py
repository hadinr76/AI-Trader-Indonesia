from backtest.order_engine import OrderEngine
from backtest.position_engine import PositionEngine

from engine.broker_fee_engine import BrokerFeeEngine
from engine.tax_engine import TaxEngine
from engine.slippage_engine import SlippageEngine
from engine.trade_cost_engine import TradeCostEngine


class PortfolioManager:
    """
    Mengelola kondisi portfolio secara keseluruhan.

    Tanggung jawab:

    - capital awal
    - cash
    - posisi OPEN
    - posisi CLOSED
    - investment
    - profit / loss
    - equity
    - broker fee
    - tax
    - slippage
    """

    def __init__(self, capital=100_000_000):

        self.initial_capital = float(capital)

        self.cash = float(capital)

        self.positions = []

        self.closed_positions = []

    # =====================================================
    # TAMBAH POSISI / BUY
    # =====================================================

    def add_position(self, position):

        if position is None:
            return False

        # -------------------------------------------------
        # Cek apakah sudah memiliki posisi
        # -------------------------------------------------

        if not OrderEngine.can_buy(
            self.positions,
            position.code
        ):
            return False

        # -------------------------------------------------
        # Harga BUY
        # -------------------------------------------------

        entry_price = float(
            position.entry_price
        )

        shares = int(
            position.shares
        )

        # -------------------------------------------------
        # Slippage BUY
        # -------------------------------------------------

        actual_buy = SlippageEngine.calculate_buy_price(
            entry_price
        )

        # -------------------------------------------------
        # Nilai pembelian aktual
        # -------------------------------------------------

        buy_value = (
            actual_buy *
            shares
        )

        # -------------------------------------------------
        # Broker fee BUY
        # -------------------------------------------------

        buy_fee = BrokerFeeEngine.calculate_buy_fee(
            buy_value
        )

        # -------------------------------------------------
        # Total dana yang dibutuhkan
        # -------------------------------------------------

        total_buy_cost = (
            buy_value +
            buy_fee
        )

        # -------------------------------------------------
        # Cek cash
        # -------------------------------------------------

        if total_buy_cost > self.cash:
            return False

        # -------------------------------------------------
        # Kurangi cash
        # -------------------------------------------------

        self.cash -= total_buy_cost

        # -------------------------------------------------
        # Simpan informasi transaksi BUY
        #
        # Disimpan pada object position supaya dapat
        # digunakan ketika posisi ditutup.
        # -------------------------------------------------

        position.actual_entry_price = actual_buy

        position.buy_value = buy_value

        position.buy_fee = buy_fee

        position.total_buy_cost = total_buy_cost

        # -------------------------------------------------
        # Simpan posisi
        # -------------------------------------------------

        self.positions.append(
            position
        )

        return True

    # =====================================================
    # TUTUP POSISI / SELL
    # =====================================================

    def close_position(
        self,
        code,
        exit_price,
        exit_date=None,
        status="CLOSED"
    ):

        position = OrderEngine.get_open_position(
            self.positions,
            code
        )

        if position is None:
            return None

        # -------------------------------------------------
        # Data posisi
        # -------------------------------------------------

        entry_price = float(
            position.entry_price
        )

        shares = int(
            position.shares
        )

        exit_price = float(
            exit_price
        )

        # -------------------------------------------------
        # HITUNG SELURUH BIAYA TRANSAKSI
        # -------------------------------------------------

        trade_cost = TradeCostEngine.calculate(

            entry_price=entry_price,

            exit_price=exit_price,

            shares=shares

        )

        # -------------------------------------------------
        # Simpan informasi biaya transaksi
        # -------------------------------------------------

        position.actual_entry_price = (
            trade_cost["actual_buy"]
        )

        position.actual_exit_price = (
            trade_cost["actual_sell"]
        )

        position.buy_value = (
            trade_cost["buy_value"]
        )

        position.sell_value = (
            trade_cost["sell_value"]
        )

        position.buy_fee = (
            trade_cost["buy_fee"]
        )

        position.sell_fee = (
            trade_cost["sell_fee"]
        )

        position.tax = (
            trade_cost["tax"]
        )

        position.gross_profit = (
            trade_cost["gross_profit"]
        )

        position.total_cost = (
            trade_cost["total_cost"]
        )

        position.net_profit = (
            trade_cost["net_profit"]
        )

        position.net_return_pct = (
            trade_cost["return_pct"]
        )

        # -------------------------------------------------
        # Nilai bersih yang diterima ketika SELL
        #
        # Buy cost sudah dibayar ketika posisi dibuka.
        #
        # Sekarang cash hanya menerima:
        #
        # actual sell
        # - sell fee
        # - tax
        # -------------------------------------------------

        net_sell_cash = (

            trade_cost["sell_value"]

            - trade_cost["sell_fee"]

            - trade_cost["tax"]

        )

        # -------------------------------------------------
        # Tutup posisi
        # -------------------------------------------------

        position.close(
            exit_price=exit_price,
            exit_date=exit_date,
            status=status
        )

        # -------------------------------------------------
        # Profit posisi diganti menjadi NET PROFIT
        #
        # PositionEngine sebelumnya menghitung profit
        # berdasarkan selisih harga saja.
        #
        # Sekarang kita menggunakan profit setelah:
        #
        # slippage
        # broker fee
        # tax
        # -------------------------------------------------

        position.profit = (
            trade_cost["net_profit"]
        )

        position.return_pct = (
            trade_cost["return_pct"]
        )

        # -------------------------------------------------
        # Cash kembali
        # -------------------------------------------------

        self.cash += net_sell_cash

        # -------------------------------------------------
        # Pindahkan posisi
        # -------------------------------------------------

        if position in self.positions:

            self.positions.remove(
                position
            )

        self.closed_positions.append(
            position
        )

        return position

    # =====================================================
    # UPDATE POSISI
    # =====================================================

    def update_positions(self, prices):

        for position in self.positions:

            if position.status != "OPEN":
                continue

            code = position.code

            if code not in prices:
                continue

            close_price = float(
                prices[code]
            )

            position.update(
                close_price
            )

    # =====================================================
    # NEXT DAY
    # =====================================================

    def next_day(self):

        for position in self.positions:

            position.next_day()

    # =====================================================
    # OPEN POSITIONS
    # =====================================================

    @property
    def open_positions(self):

        return [

            position

            for position in self.positions

            if position.status == "OPEN"

        ]

    # =====================================================
    # JUMLAH OPEN POSITION
    # =====================================================

    @property
    def open_position_count(self):

        return len(
            self.open_positions
        )

    # =====================================================
    # JUMLAH CLOSED POSITION
    # =====================================================

    @property
    def closed_position_count(self):

        return len(
            self.closed_positions
        )

    # =====================================================
    # INVESTMENT
    # =====================================================

    @property
    def investment(self):

        total = 0

        for position in self.open_positions:

            total += float(
                position.investment
            )

        return total

    # =====================================================
    # REALIZED PROFIT
    # =====================================================

    @property
    def realized_profit(self):

        total = 0

        for position in self.closed_positions:

            total += float(
                position.profit
            )

        return total

    # =====================================================
    # UNREALIZED PROFIT
    # =====================================================

    @property
    def unrealized_profit(self):

        total = 0

        for position in self.open_positions:

            total += float(
                position.profit
            )

        return total

    # =====================================================
    # TOTAL PROFIT
    # =====================================================

    @property
    def total_profit(self):

        return (

            self.realized_profit +

            self.unrealized_profit

        )

    # =====================================================
    # EQUITY
    # =====================================================

    @property
    def equity(self):

        return (

            self.cash +

            self.investment +

            self.unrealized_profit

        )

    # =====================================================
    # RETURN
    # =====================================================

    @property
    def return_pct(self):

        if self.initial_capital <= 0:

            return 0

        return (

            (

                self.equity -

                self.initial_capital

            )

            /

            self.initial_capital

        ) * 100

    # =====================================================
    # STATUS
    # =====================================================

    @property
    def status(self):

        if self.equity > self.initial_capital:

            return "PROFIT"

        if self.equity < self.initial_capital:

            return "LOSS"

        return "BREAKEVEN"

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
                self.investment,

            "equity":
                self.equity,

            "realized_profit":
                self.realized_profit,

            "unrealized_profit":
                self.unrealized_profit,

            "total_profit":
                self.total_profit,

            "return_pct":
                round(
                    self.return_pct,
                    2
                ),

            "open_position":
                self.open_position_count,

            "closed_position":
                self.closed_position_count,

            "status":
                self.status

        }