from scanner.stock_universe_source import (
    StockUniverseSource
)

from scanner.stock_universe_engine import (
    StockUniverseEngine
)


print("=" * 70)
print("FULL STOCK UNIVERSE TEST")
print("=" * 70)


# =====================================================
# SOURCE
# =====================================================

print()
print(
    "Source :",
    StockUniverseEngine.source()
)


# =====================================================
# FILE EXISTENCE
# =====================================================

print()
print(
    "CSV exists :",
    StockUniverseSource.exists()
)


# =====================================================
# LOAD STOCKS
# =====================================================

stocks = (
    StockUniverseEngine
    .get_all_stocks()
)


# =====================================================
# JUMLAH
# =====================================================

print()
print(
    "Jumlah saham :",
    len(stocks)
)


# =====================================================
# 20 SAHAM PERTAMA
# =====================================================

print()
print(
    "20 SAHAM PERTAMA"
)

print("-" * 70)


for index, code in enumerate(
    stocks[:20],
    start=1
):

    print(
        f"{index:3}. {code}"
    )


# =====================================================
# 20 SAHAM TERAKHIR
# =====================================================

print()
print(
    "20 SAHAM TERAKHIR"
)

print("-" * 70)


last_stocks = stocks[-20:]


start_number = (
    len(stocks)
    - len(last_stocks)
    + 1
)


for index, code in enumerate(
    last_stocks,
    start=start_number
):

    print(
        f"{index:3}. {code}"
    )


# =====================================================
# TEST CONTAINS
# =====================================================

print()
print(
    "TEST CONTAINS"
)

print("-" * 70)


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

    result = (
        StockUniverseEngine
        .contains(code)
    )

    print(
        f"{code:<6} : {result}"
    )


# =====================================================
# SUMMARY
# =====================================================

print()
print(
    "SUMMARY"
)

print("-" * 70)


summary = (
    StockUniverseEngine
    .summary()
)


print(
    "Source      :",
    summary["source"]
)

print(
    "Count       :",
    summary["count"]
)

print(
    "First ticker:",
    summary["first"]
)

print(
    "Last ticker :",
    summary["last"]
)


# =====================================================
# VALIDATION
# =====================================================

print()
print(
    "VALIDASI"
)

print("-" * 70)


csv_ok = (
    StockUniverseSource.exists()
)

count_ok = (
    len(stocks) > 0
)

duplicate_ok = (
    len(stocks)
    ==
    len(set(stocks))
)


print(
    "CSV source       :",
    "OK"
    if csv_ok
    else "GAGAL"
)

print(
    "Universe tidak kosong :",
    "OK"
    if count_ok
    else "GAGAL"
)

print(
    "Tidak ada duplikat :",
    "OK"
    if duplicate_ok
    else "GAGAL"
)


# =====================================================
# SELESAI
# =====================================================

print()
print("=" * 70)
print("FULL STOCK UNIVERSE TEST SELESAI")
print("=" * 70)