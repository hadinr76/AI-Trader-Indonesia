print("=" * 70)
print("BUY NOW PRIORITY V2 TEST")
print("=" * 70)


def calculate_buy_now_priority(stock):

    score = 0

    # =====================================================
    # DECISION - 25%
    # =====================================================

    score += stock["decision_score"] * 0.25

    # =====================================================
    # CONFIDENCE - 20%
    # =====================================================

    score += stock["confidence"] * 0.20

    # =====================================================
    # TECHNICAL RANKING - 15%
    # =====================================================

    score += stock["ranking_score"] * 0.15

    # =====================================================
    # FUNDAMENTAL - 10%
    # =====================================================

    score += stock["fundamental_score"] * 0.10

    # =====================================================
    # VALUATION - 15%
    # =====================================================

    valuation_label = stock["valuation_label"]

    valuation_reliability = stock[
        "valuation_reliability"
    ]

    if valuation_label == "SANGAT MURAH":
        valuation_score = 100

    elif valuation_label == "MURAH":
        valuation_score = 90

    elif valuation_label == "WAJAR":
        valuation_score = 70

    elif valuation_label == "MAHAL":
        valuation_score = 30

    elif valuation_label == "SANGAT MAHAL":
        valuation_score = 5

    else:
        valuation_score = 50

    if valuation_reliability == "HIGH":
        reliability_factor = 1.00

    elif valuation_reliability == "MEDIUM":
        reliability_factor = 0.70

    else:
        reliability_factor = 0.40

    valuation_score = (
        50
        +
        (valuation_score - 50)
        * reliability_factor
    )

    valuation_score = max(
        0,
        min(valuation_score, 100)
    )

    score += valuation_score * 0.15

    # =====================================================
    # RISK REWARD - 10%
    # =====================================================

    rr1 = stock["rr1"]

    if rr1 >= 4:
        rr_score = 100

    elif rr1 >= 3:
        rr_score = 90

    elif rr1 >= 2.5:
        rr_score = 80

    elif rr1 >= 2:
        rr_score = 70

    elif rr1 >= 1.5:
        rr_score = 40

    else:
        rr_score = 20

    score += rr_score * 0.10

    # =====================================================
    # RSI TIMING - 5%
    # =====================================================

    rsi = stock["rsi"]

    if 50 <= rsi <= 65:
        rsi_score = 100

    elif 65 < rsi <= 70:
        rsi_score = 80

    elif 45 <= rsi < 50:
        rsi_score = 70

    elif 70 < rsi <= 75:
        rsi_score = 50

    else:
        rsi_score = 20

    score += rsi_score * 0.05

    return (
        round(score, 2),
        round(valuation_score, 2)
    )


def apply_filter(stock):

    priority, valuation_score = (
        calculate_buy_now_priority(stock)
    )

    recommendation = "BUY"

    rejected_by = []

    if priority < 75:

        recommendation = "WATCH"

        rejected_by.append(
            "BUY NOW Priority V2 < 75"
        )

    elif stock["rr1"] < 2:

        recommendation = "WATCH"

        rejected_by.append(
            "R:R TP1 < 2"
        )

    elif stock["rsi"] > 75:

        recommendation = "WATCH"

        rejected_by.append(
            "RSI > 75"
        )

    elif (
        stock["valuation_label"]
        == "SANGAT MAHAL"
        and
        stock["valuation_reliability"]
        == "HIGH"
    ):

        recommendation = "WATCH"

        rejected_by.append(
            "Valuation sangat mahal (HIGH reliability)"
        )

    return {
        "priority": priority,
        "valuation_score": valuation_score,
        "recommendation": recommendation,
        "rejected_by": rejected_by
    }


# =========================================================
# TEST CASES
# =========================================================

tests = [

    (
        "TEST 1 - STRONG BUY + MURAH",
        {
            "decision_score": 90,
            "confidence": 90,
            "ranking_score": 88,
            "fundamental_score": 90,
            "valuation_label": "MURAH",
            "valuation_reliability": "HIGH",
            "rr1": 3.0,
            "rsi": 60
        }
    ),

    (
        "TEST 2 - GOOD BUY + WAJAR",
        {
            "decision_score": 85,
            "confidence": 82,
            "ranking_score": 80,
            "fundamental_score": 80,
            "valuation_label": "WAJAR",
            "valuation_reliability": "HIGH",
            "rr1": 2.5,
            "rsi": 62
        }
    ),

    (
        "TEST 3 - SANGAT MAHAL HIGH RELIABILITY",
        {
            "decision_score": 90,
            "confidence": 90,
            "ranking_score": 90,
            "fundamental_score": 90,
            "valuation_label": "SANGAT MAHAL",
            "valuation_reliability": "HIGH",
            "rr1": 3.0,
            "rsi": 60
        }
    ),

    (
        "TEST 4 - SANGAT MAHAL LOW RELIABILITY",
        {
            "decision_score": 90,
            "confidence": 90,
            "ranking_score": 90,
            "fundamental_score": 90,
            "valuation_label": "SANGAT MAHAL",
            "valuation_reliability": "LOW",
            "rr1": 3.0,
            "rsi": 60
        }
    ),

    (
        "TEST 5 - R:R BURUK",
        {
            "decision_score": 90,
            "confidence": 90,
            "ranking_score": 90,
            "fundamental_score": 90,
            "valuation_label": "MURAH",
            "valuation_reliability": "HIGH",
            "rr1": 1.5,
            "rsi": 60
        }
    ),

    (
        "TEST 6 - RSI TERLALU TINGGI",
        {
            "decision_score": 90,
            "confidence": 90,
            "ranking_score": 90,
            "fundamental_score": 90,
            "valuation_label": "MURAH",
            "valuation_reliability": "HIGH",
            "rr1": 3.0,
            "rsi": 80
        }
    ),

    (
        "TEST 7 - PRIORITY RENDAH",
        {
            "decision_score": 80,
            "confidence": 65,
            "ranking_score": 60,
            "fundamental_score": 40,
            "valuation_label": "WAJAR",
            "valuation_reliability": "MEDIUM",
            "rr1": 2.0,
            "rsi": 55
        }
    )
]


# =========================================================
# RUN TEST
# =========================================================

for name, stock in tests:

    result = apply_filter(stock)

    print()
    print("-" * 70)
    print(name)
    print("-" * 70)

    print(
        "BUY NOW Priority :",
        result["priority"]
    )

    print(
        "Valuation Score  :",
        result["valuation_score"]
    )

    print(
        "Valuation        :",
        stock["valuation_label"]
    )

    print(
        "Reliability      :",
        stock["valuation_reliability"]
    )

    print(
        "R:R              :",
        stock["rr1"]
    )

    print(
        "RSI              :",
        stock["rsi"]
    )

    print(
        "Recommendation   :",
        result["recommendation"]
    )

    print(
        "Rejected By      :",
        result["rejected_by"]
    )


print()
print("=" * 70)
print("TEST SELESAI")
print("=" * 70)