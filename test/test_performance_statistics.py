from engine.performance_tracker_engine import PerformanceTrackerEngine


print("=" * 60)
print("PERFORMANCE STATISTICS TEST")
print("=" * 60)


# ============================================================
# AMBIL STATISTICS
# ============================================================

stats = PerformanceTrackerEngine.statistics()


# ============================================================
# TAMPILKAN HASIL
# ============================================================

print()

print(
    "Total Trade       :",
    stats["total_trade"]
)

print(
    "Closed Trade      :",
    stats["closed_trade"]
)

print(
    "Open Trade        :",
    stats["open_trade"]
)

print(
    "Winning Trade     :",
    stats["winning_trade"]
)

print(
    "Losing Trade      :",
    stats["losing_trade"]
)

print(
    "Win Rate          :",
    stats["win_rate"],
    "%"
)

print(
    "Total Profit      :",
    stats["total_profit"]
)

print(
    "Average Profit    :",
    stats["average_profit"]
)

print(
    "Average Win       :",
    stats["average_win"]
)

print(
    "Average Loss      :",
    stats["average_loss"]
)

print(
    "Profit Factor     :",
    stats["profit_factor"]
)


print()
print("=" * 60)
print("PERFORMANCE STATISTICS TEST SELESAI")
print("=" * 60)