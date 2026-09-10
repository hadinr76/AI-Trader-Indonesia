from scanner.daily_recommendation import DailyRecommendation


print("=" * 70)
print("BREAKOUT PRIORITY V2 TEST")
print("=" * 70)


# =====================================================
# HELPER
# =====================================================

def test_case(
    name,
    decision_score,
    confidence,
    ranking_score,
    fundamental_score,
    valuation_label,
    valuation_reliability,
    rr1,
    relative_volume,
    rsi
):

    score = 0

    # Decision 20%
    score += decision_score * 0.20

    # Confidence 15%
    score += confidence * 0.15

    # Technical Ranking 20%
    score += ranking_score * 0.20

    # Fundamental 10%
    score += fundamental_score * 0.10

    # =================================================
    # VALUATION 10%
    # =================================================

    if valuation_label == "SANGAT MURAH":
        valuation_score = 100

    elif valuation_label == "MURAH":
        valuation_score = 90

    elif valuation_label == "WAJAR":
        valuation_score = 70

    elif valuation_label == "MAHAL":
        valuation_score = 35

    elif valuation_label == "SANGAT MAHAL":
        valuation_score = 10

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

    score += valuation_score * 0.10

    # =================================================
    # RISK REWARD 10%
    # =================================================

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

    # =================================================
    # RELATIVE VOLUME 10%
    # =================================================

    rvol_score = min(
        relative_volume * 20,
        100
    )

    score += rvol_score * 0.10

    # =================================================
    # RSI 5%
    # =================================================

    if 55 <= rsi <= 70:
        rsi_score = 100

    elif 50 <= rsi < 55:
        rsi_score = 80

    elif 70 < rsi <= 75:
        rsi_score = 70

    elif 75 < rsi <= 80:
        rsi_score = 50

    else:
        rsi_score = 20

    score += rsi_score * 0.05

    breakout_priority = round(
        score,
        2
    )

    # =================================================
    # FINAL FILTER
    # =================================================

    recommendation = "BREAKOUT BUY"
    rejected_by = []

    if breakout_priority < 70:

        recommendation = "WATCH"

        rejected_by.append(
            "Breakout Priority V2 < 70"
        )

    elif rr1 < 2:

        recommendation = "WATCH"

        rejected_by.append(
            "R:R TP1 < 2"
        )

    elif rsi > 80:

        recommendation = "WATCH"

        rejected_by.append(
            "RSI > 80"
        )

    elif (
        valuation_label == "SANGAT MAHAL"
        and
        valuation_reliability == "HIGH"
    ):

        recommendation = "WATCH"

        rejected_by.append(
            "Valuation sangat mahal (HIGH reliability)"
        )

    # =================================================
    # OUTPUT
    # =================================================

    print()
    print("-" * 70)
    print(name)
    print("-" * 70)

    print(
        "Breakout Priority :",
        breakout_priority
    )

    print(
        "Valuation Score   :",
        round(valuation_score, 2)
    )

    print(
        "Valuation         :",
        valuation_label
    )

    print(
        "Reliability       :",
        valuation_reliability
    )

    print(
        "R:R               :",
        rr1
    )

    print(
        "Relative Volume   :",
        relative_volume
    )

    print(
        "RSI               :",
        rsi
    )

    print(
        "Recommendation    :",
        recommendation
    )

    print(
        "Rejected By       :",
        rejected_by
    )


# =====================================================
# TEST 1
# BREAKOUT BAGUS + VALUASI MURAH
# =====================================================

test_case(
    name="TEST 1 - GOOD BREAKOUT + MURAH",
    decision_score=82,
    confidence=85,
    ranking_score=82,
    fundamental_score=80,
    valuation_label="MURAH",
    valuation_reliability="HIGH",
    rr1=3.0,
    relative_volume=2.5,
    rsi=65
)


# =====================================================
# TEST 2
# BREAKOUT BAGUS + VALUASI WAJAR
# =====================================================

test_case(
    name="TEST 2 - GOOD BREAKOUT + WAJAR",
    decision_score=82,
    confidence=85,
    ranking_score=82,
    fundamental_score=80,
    valuation_label="WAJAR",
    valuation_reliability="HIGH",
    rr1=3.0,
    relative_volume=2.5,
    rsi=65
)


# =====================================================
# TEST 3
# BREAKOUT BAGUS TAPI SANGAT MAHAL
# HIGH RELIABILITY
# =====================================================

test_case(
    name="TEST 3 - SANGAT MAHAL HIGH RELIABILITY",
    decision_score=85,
    confidence=88,
    ranking_score=85,
    fundamental_score=80,
    valuation_label="SANGAT MAHAL",
    valuation_reliability="HIGH",
    rr1=3.0,
    relative_volume=3.0,
    rsi=65
)


# =====================================================
# TEST 4
# SANGAT MAHAL TAPI RELIABILITY LOW
# =====================================================

test_case(
    name="TEST 4 - SANGAT MAHAL LOW RELIABILITY",
    decision_score=85,
    confidence=88,
    ranking_score=85,
    fundamental_score=80,
    valuation_label="SANGAT MAHAL",
    valuation_reliability="LOW",
    rr1=3.0,
    relative_volume=3.0,
    rsi=65
)


# =====================================================
# TEST 5
# RISK REWARD BURUK
# =====================================================

test_case(
    name="TEST 5 - R:R BURUK",
    decision_score=90,
    confidence=90,
    ranking_score=90,
    fundamental_score=90,
    valuation_label="MURAH",
    valuation_reliability="HIGH",
    rr1=1.5,
    relative_volume=3.0,
    rsi=65
)


# =====================================================
# TEST 6
# RSI TERLALU TINGGI
# =====================================================

test_case(
    name="TEST 6 - RSI TERLALU TINGGI",
    decision_score=90,
    confidence=90,
    ranking_score=90,
    fundamental_score=90,
    valuation_label="MURAH",
    valuation_reliability="HIGH",
    rr1=3.0,
    relative_volume=3.0,
    rsi=84
)


print()
print("=" * 70)
print("TEST SELESAI")
print("=" * 70)