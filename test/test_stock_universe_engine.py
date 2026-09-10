from scanner.stock_universe_engine import StockUniverseEngine


print("=" * 60)
print("STOCK UNIVERSE ENGINE TEST")
print("=" * 60)


# =====================================================
# GET ALL STOCKS
# =====================================================

stocks = StockUniverseEngine.get_all_stocks()


# =====================================================
# JUMLAH SAHAM
# =====================================================

print()
print(
    "Total saham :",
    len(stocks)
)


# =====================================================
# TAMPILKAN SAHAM
# =====================================================

print()
print("DAFTAR SAHAM")
print("-" * 60)


for index, code in enumerate(
    stocks,
    start=1
):

    print(
        f"{index:3}. {code}"
    )


# =====================================================
# TEST COUNT
# =====================================================

print()
print("Jumlah dari Engine :",
      StockUniverseEngine.count())


# =====================================================
# TEST CONTAINS
# =====================================================

print()
print("TEST CONTAINS")
print("-" * 60)


test_codes = [

    "BBCA",
    "BBRI",
    "BMRI",
    "ANTM",
    "TLKM",
    "GOTO",
    "XYZ"

]


for code in test_codes:

    result = StockUniverseEngine.contains(
        code
    )

    print(
        f"{code:<6} : {result}"
    )


# =====================================================
# SELESAI
# =====================================================

print()
print("=" * 60)
print("STOCK UNIVERSE ENGINE TEST SELESAI")
print("=" * 60)