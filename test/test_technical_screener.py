from scanner.fast_screener import FastScreener
from scanner.technical_screener import TechnicalScreener


print("=" * 70)
print("TECHNICAL SCREENER TEST")
print("=" * 70)


# =====================================================
# FAST SCREENER
# =====================================================

fast_screener = FastScreener(
    period="1y"
)

fast_results = fast_screener.scan()


# =====================================================
# AMBIL YANG PASS
# =====================================================

candidates = (
    FastScreener
    .passed_stocks(
        fast_results
    )
)


print()
print(
    "Fast Screener PASS :",
    len(candidates)
)


# =====================================================
# TECHNICAL SCREENER
# =====================================================

technical_screener = (
    TechnicalScreener(
        candidates=candidates,
        period="1y"
    )
)


technical_results = (
    technical_screener.scan()
)


# =====================================================
# HASIL
# =====================================================

print()
print(
    "Technical berhasil :",
    len(technical_results)
)


# =====================================================
# TOP 20
# =====================================================

technical_screener.print_results(
    technical_results,
    limit=20
)


# =====================================================
# DETAIL TOP 10
# =====================================================

top10 = (
    TechnicalScreener
    .top_stocks(
        technical_results,
        limit=10
    )
)


print()
print("=" * 70)
print("DETAIL TOP 10")
print("=" * 70)


for index, stock in enumerate(
    top10,
    start=1
):

    print()

    print(
        f"{index}. {stock['code']}"
    )

    print(
        "Price          :",
        stock["price"]
    )

    print(
        "Trend          :",
        stock["trend"]
    )

    print(
        "RSI            :",
        stock["rsi"]
    )

    print(
        "MACD           :",
        stock["macd"]
    )

    print(
        "Momentum       :",
        stock["momentum"]
    )

    print(
        "Momentum Score :",
        stock["momentum_score"]
    )

    print(
        "Volume         :",
        stock["volume"]
    )

    print(
        "Relative Volume:",
        stock["relative_volume"]
    )

    print(
        "Breakout       :",
        stock["breakout"]
    )

    print(
        "Price Action   :",
        stock["price_action"]
    )

    print(
        "Candlestick    :",
        stock["candlestick"]
    )

    print(
        "Support        :",
        stock["support"]
    )

    print(
        "Resistance     :",
        stock["resistance"]
    )

    print(
        "Technical Score:",
        stock["technical_score"]
    )


print()
print("=" * 70)
print("TECHNICAL SCREENER TEST SELESAI")
print("=" * 70)