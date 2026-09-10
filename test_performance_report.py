from backtest.statistics import Statistics
from backtest.equity_curve import EquityCurve
from backtest.performance_report import PerformanceReport

print("=" * 60)
print("PERFORMANCE REPORT TEST")
print("=" * 60)

# =====================================================
# MODAL AWAL
# =====================================================

initial_capital = 100_000_000

# =====================================================
# HASIL TRADE
# =====================================================

trades = [

    {
        "profit": 400
    },

    {
        "profit": -200
    },

    {
        "profit": 600
    },

    {
        "profit": -100
    },

    {
        "profit": 300
    }

]

# =====================================================
# HITUNG STATISTICS
# =====================================================

statistics = Statistics.calculate(trades)

# =====================================================
# HITUNG EQUITY
# =====================================================

equity = EquityCurve.calculate(

    initial_capital,

    trades

)

# =====================================================
# BUAT REPORT
# =====================================================

report = PerformanceReport.generate(

    statistics,

    equity

)

# =====================================================
# TAMPILKAN REPORT
# =====================================================

PerformanceReport.show(report)

print()

print("=" * 60)
print("PERFORMANCE REPORT TEST SELESAI")
print("=" * 60)