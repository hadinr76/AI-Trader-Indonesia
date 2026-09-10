from backtest.equity_curve import EquityCurve

print("=" * 60)
print("EQUITY CURVE TEST")
print("=" * 60)

# =====================================================
# MODAL AWAL
# =====================================================

initial_capital = 100_000_000

# =====================================================
# HASIL TRADE
# =====================================================

trades = [

    {"profit": 400},

    {"profit": -200},

    {"profit": 600},

    {"profit": -100},

    {"profit": 300}

]

# =====================================================
# HITUNG EQUITY CURVE
# =====================================================

result = EquityCurve.calculate(

    initial_capital,

    trades

)

# =====================================================
# RINGKASAN
# =====================================================

print()

print("Initial Capital :", result["initial_capital"])

print("Final Capital   :", result["final_capital"])

print("Return (%)      :", result["return"])

print("Max Drawdown (%) :", result["max_drawdown"])

# =====================================================
# DETAIL EQUITY
# =====================================================

print()

print("-" * 60)

print("DETAIL EQUITY CURVE")

print("-" * 60)

for i, item in enumerate(result["curve"], start=1):

    print(

        f"Trade {i:2d}"

        f" | Equity : {item['equity']:,.2f}"

        f" | Peak : {item['peak']:,.2f}"

        f" | Drawdown : {item['drawdown']}%"

    )

print()

print("=" * 60)
print("EQUITY CURVE TEST SELESAI")
print("=" * 60)