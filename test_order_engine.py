from backtest.position_engine import PositionEngine
from backtest.order_engine import OrderEngine

print("=" * 60)
print("ORDER ENGINE TEST")
print("=" * 60)

portfolio = []

# =======================================
# Tambah posisi BBCA
# =======================================

portfolio.append(

    PositionEngine(

        code="BBCA",

        entry_date="2026-08-06",

        entry_price=5000,

        shares=10000,

        lots=100,

        stop_loss=4800,

        target1=5400,

        target2=5600

    )

)

print()

print("Can Buy BBCA :", OrderEngine.can_buy(

    portfolio,

    "BBCA"

))

print()

print("Can Buy BBRI :", OrderEngine.can_buy(

    portfolio,

    "BBRI"

))

print()

print("Can Sell BBCA :", OrderEngine.can_sell(

    portfolio,

    "BBCA"

))

print()

print("Open Position :", OrderEngine.count_open_position(

    portfolio

))

print()

print("=" * 60)
print("ORDER ENGINE TEST SELESAI")