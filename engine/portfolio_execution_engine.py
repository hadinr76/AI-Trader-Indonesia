from engine.portfolio_engine import PortfolioEngine
from engine.position_size_engine import PositionSizeEngine

from backtest.order_engine import OrderEngine
from backtest.position_engine import PositionEngine


class PortfolioExecutionEngine:
    """
    Menghubungkan:

    PortfolioEngine
        ↓
    PositionSizeEngine
        ↓
    OrderEngine
        ↓
    PositionEngine
    """

    @staticmethod
    def execute(
        results,
        capital=100_000_000,
        risk_percent=1.0,
        entry_date=None,
        portfolio=None
    ):

        # =================================================
        # VALIDASI
        # =================================================

        if not results:
            return []

        if portfolio is None:
            portfolio = []

        # =================================================
        # PORTFOLIO ALLOCATION
        # =================================================

        allocations = PortfolioEngine.allocate(
            results,
            capital=capital
        )

        positions = []

        # =================================================
        # PROSES SAHAM
        # =================================================

        for stock in allocations:

            code = stock["code"]

            price = float(stock["price"])

            recommendation = stock["recommendation"]

            stop_loss = float(
                stock.get("stop_loss", 0)
            )

            target1 = float(
                stock.get("target1", 0)
            )

            target2 = float(
                stock.get("target2", 0)
            )

            # =================================================
            # HANYA SINYAL BUY
            # =================================================

            if recommendation not in [
                "BUY",
                "BUY ON WEAKNESS",
                "STRONG BUY"
            ]:
                continue

            # =================================================
            # VALIDASI HARGA
            # =================================================

            if price <= 0:
                continue

            # =================================================
            # VALIDASI STOP LOSS
            # =================================================

            if stop_loss <= 0:
                continue

            if stop_loss >= price:
                continue

            # =================================================
            # CEK APAKAH SUDAH PUNYA POSISI
            # =================================================

            if not OrderEngine.can_buy(
                portfolio,
                code
            ):
                continue

            # =================================================
            # BATAS ALLOCATION
            # =================================================

            allocation = float(
                stock["allocation"]
            )

            allocation_shares = int(
                allocation // price
            )

            allocation_lots = (
                allocation_shares // 100
            )

            allocation_shares = (
                allocation_lots * 100
            )

            # =================================================
            # POSITION SIZE BERDASARKAN RISIKO
            # =================================================

            risk_result = PositionSizeEngine.calculate(
                capital=capital,
                risk_percent=risk_percent,
                entry=price,
                stop_loss=stop_loss
            )

            risk_shares = int(
                risk_result["shares"]
            )

            # =================================================
            # AMBIL BATAS TERKECIL
            # =================================================

            final_shares = min(
                allocation_shares,
                risk_shares
            )

            # =================================================
            # BULATKAN KE LOT
            # =================================================

            final_lots = (
                final_shares // 100
            )

            final_shares = (
                final_lots * 100
            )

            # =================================================
            # JIKA TIDAK ADA LOT
            # =================================================

            if final_lots <= 0:
                continue

            # =================================================
            # INVESTMENT
            # =================================================

            investment = (
                final_shares * price
            )

            # =================================================
            # BUAT POSITION
            # =================================================

            position = PositionEngine(
                code=code,
                entry_date=entry_date,
                entry_price=price,
                shares=final_shares,
                lots=final_lots,
                stop_loss=stop_loss,
                target1=target1,
                target2=target2,
                recommendation=recommendation
            )

            # =================================================
            # SIMPAN
            # =================================================

            portfolio.append(position)

            positions.append(position)

        return positions