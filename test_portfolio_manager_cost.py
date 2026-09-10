import math

from engine.portfolio_manager import PortfolioManager
from engine.trade_cost_engine import TradeCostEngine


print("=" * 60)
print("PORTFOLIO MANAGER COST TEST")
print("=" * 60)


# ==========================================================
# INITIAL CAPITAL
# ==========================================================

initial_capital = 100_000_000

print()
print("INITIAL CAPITAL :", initial_capital)


# ==========================================================
# DATA TRANSAKSI
# ==========================================================

entry_price = 5000
exit_price = 5500

shares = 5000
lots = shares // 100


# ==========================================================
# TRADE COST
# ==========================================================

cost = TradeCostEngine.calculate(

    entry_price=entry_price,

    exit_price=exit_price,

    shares=shares

)


# ==========================================================
# HASIL TRADE COST
# ==========================================================

print()
print("=" * 60)
print("TRADE COST")
print("=" * 60)

print(
    "Entry Price       :",
    cost["entry_price"]
)

print(
    "Exit Price        :",
    cost["exit_price"]
)

print(
    "Actual Buy        :",
    cost["actual_buy"]
)

print(
    "Actual Sell       :",
    cost["actual_sell"]
)

print(
    "Shares            :",
    cost["shares"]
)

print(
    "Lots              :",
    lots
)

print(
    "Buy Value         :",
    cost["buy_value"]
)

print(
    "Sell Value        :",
    cost["sell_value"]
)

print(
    "Buy Fee           :",
    cost["buy_fee"]
)

print(
    "Sell Fee          :",
    cost["sell_fee"]
)

print(
    "Tax               :",
    cost["tax"]
)

print(
    "Gross Profit      :",
    cost["gross_profit"]
)

print(
    "Total Cost        :",
    cost["total_cost"]
)

print(
    "Net Profit        :",
    cost["net_profit"]
)

print(
    "Return            :",
    cost["return_pct"]
)


# ==========================================================
# VALIDATION
# ==========================================================

print()
print("=" * 60)
print("VALIDATION")
print("=" * 60)

assert cost["shares"] == 5000

assert lots == 50

assert math.isclose(
    cost["actual_buy"],
    5005.0,
    rel_tol=1e-9
)

assert math.isclose(
    cost["actual_sell"],
    5494.5,
    rel_tol=1e-9
)

assert math.isclose(
    cost["buy_value"],
    25_025_000,
    rel_tol=1e-9
)

assert math.isclose(
    cost["sell_value"],
    27_472_500,
    rel_tol=1e-9
)

assert math.isclose(
    cost["buy_fee"],
    37_537.5,
    rel_tol=1e-9
)

assert math.isclose(
    cost["sell_fee"],
    68_681.25,
    rel_tol=1e-9
)

assert math.isclose(
    cost["tax"],
    27_472.5,
    rel_tol=1e-9
)

assert math.isclose(
    cost["gross_profit"],
    2_447_500,
    rel_tol=1e-9
)

assert math.isclose(
    cost["total_cost"],
    133_691.25,
    rel_tol=1e-9
)

assert math.isclose(
    cost["net_profit"],
    2_313_808.75,
    rel_tol=1e-9
)


print("Shares          : OK")
print("Lots            : OK")
print("Slippage BUY    : OK")
print("Slippage SELL   : OK")
print("Broker Fee BUY  : OK")
print("Broker Fee SELL : OK")
print("Tax             : OK")
print("Gross Profit    : OK")
print("Total Cost      : OK")
print("Net Profit      : OK")