from scanner.fast_screener import FastScreener
from scanner.technical_screener import TechnicalScreener
from engine.technical_ranking_engine import TechnicalRankingEngine


print("=" * 70)
print("TECHNICAL RANKING ENGINE TEST")
print("=" * 70)


# =====================================================
# FAST SCREENER
# =====================================================

fast_screener = FastScreener(
    period="1y"
)

fast_results = fast_screener.scan()


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


print()
print(
    "Technical berhasil :",
    len(technical_results)
)


# =====================================================
# TECHNICAL RANKING
# =====================================================

ranked_results = []


for stock in technical_results:

    ranking = (
        TechnicalRankingEngine
        .calculate(
            stock
        )
    )

    result = stock.copy()

    result.update(
        ranking
    )

    ranked_results.append(
        result
    )


# =====================================================
# SORT
# =====================================================

ranked_results.sort(

    key=lambda x:
    x["ranking_score"],

    reverse=True

)


# =====================================================
# TOP 20
# =====================================================

top20 = ranked_results[
    :20
]


print()
print("=" * 70)
print("TOP 20 FINAL TECHNICAL RANKING")
print("=" * 70)


for index, stock in enumerate(
    top20,
    start=1
):

    print()

    print(
        f"{index}. {stock['code']}"
    )

    print(
        "Price           :",
        stock["price"]
    )

    print(
        "Technical Score :",
        stock["technical_score"]
    )

    print(
        "Momentum Score  :",
        stock["momentum_score"]
    )

    print(
        "RSI             :",
        stock["rsi"]
    )

    print(
        "Relative Volume :",
        stock["relative_volume"]
    )

    print(
        "Resistance      :",
        stock["resistance"]
    )

    print(
        "Breakout        :",
        stock["breakout"]
    )

    print(
        "Penalty         :",
        stock["penalty"]
    )

    print(
        "Ranking Score   :",
        stock["ranking_score"]
    )

    print(
        "Ranking Label   :",
        stock["ranking_label"]
    )

    print(
        "Reasons         :",
        ", ".join(
            stock["reasons"]
        )
    )


# =====================================================
# DISTRIBUSI
# =====================================================

strong = [

    stock
    for stock in ranked_results
    if stock["ranking_label"]
    == "STRONG CANDIDATE"

]

candidate = [

    stock
    for stock in ranked_results
    if stock["ranking_label"]
    == "CANDIDATE"

]

watch = [

    stock
    for stock in ranked_results
    if stock["ranking_label"]
    == "WATCH"

]


print()
print("=" * 70)
print("RANKING SUMMARY")
print("=" * 70)

print(
    "Strong Candidate :",
    len(strong)
)

print(
    "Candidate        :",
    len(candidate)
)

print(
    "Watch            :",
    len(watch)
)

print(
    "Total Ranked     :",
    len(ranked_results)
)


print()
print("=" * 70)
print("TECHNICAL RANKING ENGINE TEST SELESAI")
print("=" * 70)