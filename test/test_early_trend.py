from scanner.fast_screener import FastScreener


print("=" * 90)
print("EARLY TREND / NEAR GOLDEN CROSS TEST")
print("=" * 90)

screener = FastScreener()

results = screener.scan()

early_candidates = [
    stock
    for stock in results
    if stock.get("early_trend") is True
]

quality_candidates = [
    stock
    for stock in early_candidates
    if (
        stock.get("liquidity_status")
        in [
            "VERY LIQUID",
            "LIQUID",
            "MODERATE"
        ]
        and stock.get("relative_volume", 0) >= 0.50
    )
]

early_candidates.sort(
    key=lambda x: (
        x.get("golden_cross_age")
        if x.get("golden_cross_age") is not None
        else 999,
        abs(x.get("distance_ma20_ma50", 999)),
        abs(x.get("distance_price_ma20", 999))
    )
)

print()
print("Jumlah Early Trend :", len(early_candidates))
print(
    "Lolos Quality Filter :",
    len(quality_candidates)
)
print()

print(
    f"{'CODE':<7}"
    f"{'PRICE':>10}"
    f"{'MA20':>10}"
    f"{'MA50':>10}"
    f"{'P-MA20':>10}"
    f"{'MA20-50':>11}"
    f"{'CROSS':>8}"
    f"{'RVOL':>8}"
    f"{'LIQUIDITY':>16}"
)

print("-" * 115)

for stock in early_candidates[:20]:

    cross_age = stock.get("golden_cross_age")

    if cross_age is None:
        cross_text = "-"
    else:
        cross_text = str(cross_age)

    rvol = stock.get(
        "relative_volume",
        0
    )

    liquidity = stock.get(
        "liquidity_status",
        "-"
    )

    print(
        f"{stock['code']:<7}"
        f"{stock['price']:>10.2f}"
        f"{stock['ma20']:>10.2f}"
        f"{stock['ma50']:>10.2f}"
        f"{stock['distance_price_ma20']:>9.2f}%"
        f"{stock['distance_ma20_ma50']:>10.2f}%"
        f"{cross_text:>8}"
        f"{rvol:>8.2f}"
        f"{liquidity:>16}"
    )

print("-" * 90)

for stock in early_candidates[:20]:

    cross_age = stock.get("golden_cross_age")

    if cross_age is None:
        cross_text = "-"
    else:
        cross_text = str(cross_age)

    print(
        f"{stock['code']:<7}"
        f"{stock['price']:>10.2f}"
        f"{stock['ma20']:>10.2f}"
        f"{stock['ma50']:>10.2f}"
        f"{stock['distance_price_ma20']:>9.2f}%"
        f"{stock['distance_ma20_ma50']:>10.2f}%"
        f"{cross_text:>8}"
    )