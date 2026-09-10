from backtest.statistics import Statistics


print("=" * 60)
print("STATISTICS TEST")
print("=" * 60)

# =====================================================
# DATA DUMMY HASIL BACKTEST
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
# HITUNG STATISTIK
# =====================================================

result = Statistics.calculate(trades)

# =====================================================
# TAMPILKAN HASIL
# =====================================================

print()

for key, value in result.items():

    print(f"{key:20}: {value}")

print()

print("=" * 60)
print("STATISTICS TEST SELESAI")
print("=" * 60)