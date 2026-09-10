from engine.portfolio_engine import PortfolioEngine


print("=" * 60)
print("PORTFOLIO ENGINE TEST")
print("=" * 60)


# =====================================================
# DATA HASIL ANALISIS AI
# =====================================================

results = [

    {
        "code": "BBCA",
        "ranking_score": 90,
        "recommendation": "BUY",
        "price": 5000
    },

    {
        "code": "BBRI",
        "ranking_score": 85,
        "recommendation": "BUY",
        "price": 4000
    },

    {
        "code": "BMRI",
        "ranking_score": 80,
        "recommendation": "BUY ON WEAKNESS",
        "price": 5000
    },

    {
        "code": "TLKM",
        "ranking_score": 75,
        "recommendation": "BUY",
        "price": 3000
    },

    {
        "code": "ASII",
        "ranking_score": 70,
        "recommendation": "BUY ON WEAKNESS",
        "price": 5000
    },

    {
        "code": "UNTR",
        "ranking_score": 60,
        "recommendation": "WATCH",
        "price": 25000
    }
]


# =====================================================
# CAPITAL
# =====================================================

capital = 100_000_000


# =====================================================
# ALLOCATION
# =====================================================

portfolio = PortfolioEngine.allocate(

    results,

    capital=capital

)


# =====================================================
# OUTPUT
# =====================================================

print()

print("INITIAL CAPITAL :", capital)

print()

print("-" * 60)

for stock in portfolio:

    print()

    print("Code          :", stock["code"])

    print("Ranking Score :", stock["ranking_score"])

    print("Recommendation:", stock["recommendation"])

    print("Weight        :", stock["weight"], "%")

    print("Allocation    :", stock["allocation"])

    print("Price         :", stock["price"])

    print("Shares        :", stock["shares"])

    print("Lots          :", stock["lots"])

    print("Investment    :", stock["investment"])

    print("Remaining     :", stock["remaining"])


# =====================================================
# VALIDASI
# =====================================================

print()

print("=" * 60)

print("VALIDATION")

print("=" * 60)


# Harus maksimal 5 saham

assert len(portfolio) <= 5

print("Top 5 saham     : OK")


# Ranking harus descending

scores = [

    stock["ranking_score"]

    for stock in portfolio

]

assert scores == sorted(

    scores,

    reverse=True

)

print("Ranking order   : OK")


# Bobot

weights = [

    stock["weight"]

    for stock in portfolio

]

assert weights == [

    30,

    25,

    20,

    15,

    10

]

print("Portfolio weight: OK")


# Semua saham harus dalam kelipatan 100

for stock in portfolio:

    assert stock["shares"] % 100 == 0

print("Lot calculation : OK")


# Investment tidak boleh melebihi allocation

for stock in portfolio:

    assert stock["investment"] <= stock["allocation"]

print("Allocation      : OK")


print()

print("=" * 60)

print("PORTFOLIO ENGINE TEST SELESAI")

print("=" * 60)