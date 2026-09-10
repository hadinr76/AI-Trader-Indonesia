from data.market_data import MarketData

from scanner.fast_screener import FastScreener
from scanner.technical_screener import TechnicalScreener
from scanner.daily_recommendation import DailyRecommendation

from engine.technical_ranking_engine import TechnicalRankingEngine


CODE = "WIFI"


print("=" * 70)
print("DAILY RECOMMENDATION VALUATION TEST")
print("=" * 70)

# =====================================================
# MARKET DATA
# =====================================================

market = MarketData()

data = market.get_daily(
    CODE,
    period="1y"
)

if data is None or data.empty:

    raise ValueError(
        f"Data {CODE} tidak tersedia"
    )

# =====================================================
# FAST SCREENER
# =====================================================

fast_result = (
    FastScreener
    .analyze_stock(
        CODE,
        data
    )
)

if fast_result is None:

    raise ValueError(
        f"Fast Screener {CODE} gagal"
    )

# =====================================================
# TECHNICAL SCREENER
# =====================================================

technical_result = (
    TechnicalScreener
    .analyze_stock(
        CODE,
        data,
        fast_result
    )
)

if technical_result is None:

    raise ValueError(
        f"Technical Screener {CODE} gagal"
    )

# =====================================================
# TECHNICAL RANKING
# =====================================================

ranking = (
    TechnicalRankingEngine
    .calculate(
        technical_result
    )
)

stock = technical_result.copy()

stock.update(
    ranking
)

# =====================================================
# DEEP ANALYSIS
# =====================================================

result = (
    DailyRecommendation
    .analyze_candidate(
        stock
    )
)

if result is None:

    raise ValueError(
        f"Deep Analysis {CODE} gagal"
    )

# =====================================================
# RESULT
# =====================================================

print()
print("=" * 70)
print("VALUATION RESULT")
print("=" * 70)

print()
print(
    "Code                  :",
    result["code"]
)

print(
    "Current Price         :",
    result["price"]
)

print(
    "Fundamental Score     :",
    result["fundamental_score"]
)

print()

print(
    "Fair Value            :",
    result.get(
        "fair_value",
        0
    )
)

print(
    "Estimated Fair Value  :",
    result.get(
        "estimated_fair_value",
        0
    )
)

print(
    "Price / Fair Value    :",
    result.get(
        "price_to_fair_value",
        0
    ),
    "%"
)

print(
    "Margin of Safety      :",
    result.get(
        "margin_of_safety",
        0
    ),
    "%"
)

print(
    "Valuation             :",
    result.get(
        "valuation_label",
        "-"
    )
)

print(
    "Valuation Status      :",
    result.get(
        "valuation_status",
        "-"
    )
)

print(
    "Valuation Method      :",
    result.get(
        "valuation_method",
        "-"
    )
)

print(
    "Valuation Confidence  :",
    result.get(
        "valuation_confidence",
        "-"
    )
)

print(
    "Valuation Reliability :",
    result.get(
        "valuation_reliability",
        "-"
    )
)

print(
    "Fair Value Capped     :",
    result.get(
        "fair_value_capped",
        False
    )
)

warnings = result.get(
    "valuation_warnings",
    []
)

if warnings:

    print()
    print("Valuation Warnings:")

    for warning in warnings:

        print(
            "  -",
            warning
        )

print()
print("=" * 70)
print("TEST SELESAI")
print("=" * 70)