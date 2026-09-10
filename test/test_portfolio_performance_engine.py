from engine.portfolio_performance_engine import PortfolioPerformanceEngine


print("=" * 60)
print("PORTFOLIO PERFORMANCE ENGINE TEST")
print("=" * 60)


# ============================================================
# BUAT ENGINE
# ============================================================

portfolio = PortfolioPerformanceEngine(
    initial_capital=100_000_000
)


# ============================================================
# AMBIL SUMMARY
# ============================================================

summary = portfolio.summary()


# ============================================================
# PORTFOLIO
# ============================================================

print()
print("## PORTFOLIO")
print()

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
    "Equity            :",
    summary["equity"]
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
print("## PERFORMANCE")
print()

print(
    "Total Trade       :",
    summary["total_trade"]
)

print(
    "Winning Trade     :",
    summary["winning_trade"]
)

print(
    "Losing Trade      :",
    summary["losing_trade"]
)

print(
    "Win Rate          :",
    summary["win_rate"],
    "%"
)

print(
    "Average Win       :",
    summary["average_win"]
)

print(
    "Average Loss      :",
    summary["average_loss"]
)

print(
    "Profit Factor     :",
    summary["profit_factor"]
)


# ============================================================
# VALIDASI
# ============================================================

print()
print("## VALIDASI")
print()

if summary["total_trade"] > 0:
    print("Total Trade       : OK")
else:
    print("Total Trade       : GAGAL")


if summary["closed_position"] > 0:
    print("Closed Position   : OK")
else:
    print("Closed Position   : GAGAL")


if summary["total_profit"] != 0:
    print("Total Profit      : OK")
else:
    print("Total Profit      : GAGAL")


if summary["equity"] != summary["initial_capital"]:
    print("Equity             : OK")
else:
    print("Equity             : GAGAL")


if summary["profit_factor"] > 0:
    print("Profit Factor     : OK")
else:
    print("Profit Factor     : GAGAL")


print()
print("=" * 60)
print("PORTFOLIO PERFORMANCE ENGINE TEST SELESAI")
print("=" * 60)