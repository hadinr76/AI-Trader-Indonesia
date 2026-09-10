from engine.portfolio_manager import PortfolioManager
from backtest.position_engine import PositionEngine


print("=" * 60)
print("PORTFOLIO MANAGER TEST")
print("=" * 60)


# ==========================================================
# INITIAL CAPITAL
# ==========================================================

capital = 100_000_000

portfolio = PortfolioManager(
    capital=capital
)

print()
print("INITIAL CAPITAL :", capital)


# ==========================================================
# BUAT POSISI BBCA
# ==========================================================

bbca = PositionEngine(

    code="BBCA",

    entry_date="2026-08-10",

    entry_price=5000,

    shares=5000,

    lots=50,

    stop_loss=4800,

    target1=5400,

    target2=5600,

    recommendation="BUY"

)


# ==========================================================
# TEST BUY
# ==========================================================

print()
print("=" * 60)
print("TEST BUY")
print("=" * 60)

result = portfolio.add_position(
    bbca
)

print("BUY BBCA       :", result)

print(
    "Cash           :",
    portfolio.cash
)

print(
    "Investment     :",
    portfolio.investment
)

print(
    "Open Position  :",
    portfolio.open_position_count
)


# ==========================================================
# TEST UPDATE HARGA
# ==========================================================

print()
print("=" * 60)
print("TEST UPDATE PRICE")
print("=" * 60)

portfolio.update_positions({

    "BBCA": 5200

})

print(
    "BBCA Profit    :",
    bbca.profit
)

print(
    "BBCA Return    :",
    bbca.return_pct
)


# ==========================================================
# TEST NEXT DAY
# ==========================================================

portfolio.next_day()

print(
    "Holding Days   :",
    bbca.holding_days
)


# ==========================================================
# TEST CLOSE
# ==========================================================

print()
print("=" * 60)
print("TEST CLOSE")
print("=" * 60)

closed = portfolio.close_position(

    code="BBCA",

    exit_price=5400,

    exit_date="2026-08-13",

    status="TARGET 1"

)

print(
    "Status         :",
    closed.status
)

print(
    "Exit Price     :",
    closed.exit_price
)

print(
    "Profit         :",
    closed.profit
)

print(
    "Return         :",
    closed.return_pct
)

print(
    "Cash           :",
    portfolio.cash
)

print(
    "Open Position  :",
    portfolio.open_position_count
)

print(
    "Closed Position:",
    portfolio.closed_position_count
)


# ==========================================================
# SUMMARY
# ==========================================================

print()
print("=" * 60)
print("PORTFOLIO SUMMARY")
print("=" * 60)

summary = portfolio.summary()

for key, value in summary.items():

    print(
        f"{key:<20}: {value}"
    )


print()
print("=" * 60)
print("PORTFOLIO MANAGER TEST SELESAI")
print("=" * 60)