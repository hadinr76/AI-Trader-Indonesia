from scanner.stock_screener import StockScreener


print("=" * 70)
print("STOCK SCREENER TEST")
print("=" * 70)


# =====================================================
# BUAT SCREENER
# =====================================================

screener = StockScreener()


# =====================================================
# SCAN
# =====================================================

results = screener.scan()


# =====================================================
# TAMPILKAN HASIL
# =====================================================

screener.print_results(
    results
)


# =====================================================
# TOP 5
# =====================================================

top_stocks = results[:5]


print()
print("=" * 70)
print("TOP 5 STOCK")
print("=" * 70)

for index, stock in enumerate(
    top_stocks,
    start=1
):

    print()

    print(
        f"{index}. {stock.get('code')}"
    )

    print(
        f"   Price          : {stock.get('price')}"
    )

    print(
        f"   Trend          : {stock.get('trend')}"
    )

    print(
        f"   Recommendation : {stock.get('recommendation')}"
    )

    print(
        f"   Ranking Score  : {stock.get('ranking_score')}"
    )

    print(
        f"   Scanner Score  : {stock.get('scanner_score')}"
    )

    print(
        f"   Confidence     : {stock.get('confidence')}"
    )


print()
print("=" * 70)
print("STOCK SCREENER TEST SELESAI")
print("=" * 70)