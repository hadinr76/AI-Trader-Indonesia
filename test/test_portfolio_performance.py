from engine.portfolio_manager import PortfolioManager
from engine.performance_tracker_engine import PerformanceTrackerEngine


print("=" * 60)
print("PORTFOLIO PERFORMANCE TEST")
print("=" * 60)


# ============================================================
# PORTFOLIO
# ============================================================

portfolio = PortfolioManager(
    capital=100_000_000
)


# ============================================================
# PERFORMANCE
# ============================================================

performance = PerformanceTrackerEngine.statistics()


# ============================================================
# PORTFOLIO SUMMARY
# ============================================================

summary = portfolio.summary()


print()
print("PORTFOLIO")
print("-" * 60)

print(
    "Initial Capital   :",
    summary["initial_capital"]
)

print(
    "Cash              :",
    summary["cash"]
)

print(
    "Investment        :",
    summary["investment"]
)

print(
    "Equity            :",
    summary["equity"]
)

print(
    "Realized Profit   :",
    summary["realized_profit"]
)

print(
    "Unrealized Profit :",
    summary["unrealized_profit"]
)

print(
    "Total Profit      :",
    summary["total_profit"]
)

print(
    "Return            :",
    summary["return_pct"],
    "%"
)

print(
    "Open Position     :",
    summary["open_position"]
)

print(
    "Closed Position   :",
    summary["closed_position"]
)

print(
    "Status            :",
    summary["status"]
)


# ============================================================
# PERFORMANCE
# ============================================================

print()
print("PERFORMANCE")
print("-" * 60)

print(
    "Total Trade       :",
    performance["total_trade"]
)

print(
    "Closed Trade      :",
    performance["closed_trade"]
)

print(
    "Open Trade        :",
    performance["open_trade"]
)

print(
    "Winning Trade     :",
    performance["winning_trade"]
)

print(
    "Losing Trade      :",
    performance["losing_trade"]
)

print(
    "Win Rate          :",
    performance["win_rate"],
    "%"
)

print(
    "Total Profit      :",
    performance["total_profit"]
)

print(
    "Average Profit    :",
    performance["average_profit"]
)

print(
    "Average Win       :",
    performance["average_win"]
)

print(
    "Average Loss      :",
    performance["average_loss"]
)

print(
    "Profit Factor     :",
    performance["profit_factor"]
)


# ============================================================
# SELESAI
# ============================================================

print()
print("=" * 60)
print("PORTFOLIO PERFORMANCE TEST SELESAI")
print("=" * 60)