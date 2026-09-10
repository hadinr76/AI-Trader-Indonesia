from engine.mtf_score_engine import MTFScoreEngine


def run_test(
    name,
    data,
    expected_score,
    expected_status
):

    result = MTFScoreEngine.calculate(data)

    score = result["average_score"]
    status = result["status"]

    print("=" * 60)
    print(name)
    print("-" * 60)

    print("Score    :", score)
    print("Expected :", expected_score)

    print("Status   :", status)
    print("Expected :", expected_status)

    assert score == expected_score, (
        f"{name}: score salah. "
        f"{score} != {expected_score}"
    )

    assert status == expected_status, (
        f"{name}: status salah. "
        f"{status} != {expected_status}"
    )

    print("RESULT   : PASS")


# =====================================================
# TEST 1
# SEMUA TIMEFRAME STRONG BULLISH
# =====================================================

run_test(
    "TEST 1 - VERY STRONG BULLISH",
    {
        "Weekly": {
            "trend": "Strong Bullish",
            "score": 90
        },
        "Daily": {
            "trend": "Strong Bullish",
            "score": 90
        },
        "4H": {
            "trend": "Strong Bullish",
            "score": 90
        }
    },
    100,
    "VERY STRONG BULLISH"
)


# =====================================================
# TEST 2
# SWING BULLISH
# Weekly Recovery = 60 x 30%
# Daily Bullish   = 80 x 50%
# 4H Bullish      = 80 x 20%
# Score = 74
# =====================================================

run_test(
    "TEST 2 - STRONG BULLISH",
    {
        "Weekly": {
            "trend": "Recovery",
            "score": 30
        },
        "Daily": {
            "trend": "Bullish",
            "score": 30
        },
        "4H": {
            "trend": "Bullish",
            "score": 30
        }
    },
    74,
    "STRONG BULLISH"
)


# =====================================================
# TEST 3
# MIXED
# Weekly Bearish = 20 x 30%
# Daily Sideways = 50 x 50%
# 4H Bullish     = 80 x 20%
# Score = 47
# =====================================================

run_test(
    "TEST 3 - MIXED",
    {
        "Weekly": {
            "trend": "Bearish"
        },
        "Daily": {
            "trend": "Sideways"
        },
        "4H": {
            "trend": "Bullish"
        }
    },
    47,
    "MIXED"
)


# =====================================================
# TEST 4
# BEARISH
# Weekly Bearish        = 20 x 30%
# Daily Bearish         = 20 x 50%
# 4H Strong Bearish     = 0 x 20%
# Score = 16
# =====================================================

run_test(
    "TEST 4 - STRONG BEARISH",
    {
        "Weekly": {
            "trend": "Bearish"
        },
        "Daily": {
            "trend": "Bearish"
        },
        "4H": {
            "trend": "Strong Bearish"
        }
    },
    16,
    "STRONG BEARISH"
)


# =====================================================
# TEST 5
# SEMUA STRONG BEARISH
# =====================================================

run_test(
    "TEST 5 - VERY STRONG BEARISH",
    {
        "Weekly": {
            "trend": "Strong Bearish"
        },
        "Daily": {
            "trend": "Strong Bearish"
        },
        "4H": {
            "trend": "Strong Bearish"
        }
    },
    0,
    "VERY STRONG BEARISH"
)


# =====================================================
# TEST 6
# MONTHLY DAN 1H TIDAK BOLEH MENGUBAH SCORE
#
# Swing:
# Weekly Recovery = 60 x 30%
# Daily Bullish   = 80 x 50%
# 4H Bullish      = 80 x 20%
# Score = 74
#
# Monthly dibuat Strong Bearish
# 1H dibuat Strong Bearish
# Score HARUS tetap 74
# =====================================================

run_test(
    "TEST 6 - MONTHLY & 1H IGNORED",
    {
        "Monthly": {
            "trend": "Strong Bearish"
        },
        "Weekly": {
            "trend": "Recovery"
        },
        "Daily": {
            "trend": "Bullish"
        },
        "4H": {
            "trend": "Bullish"
        },
        "1H": {
            "trend": "Strong Bearish"
        }
    },
    74,
    "STRONG BULLISH"
)


print()
print("=" * 60)
print("SEMUA UNIT TEST MTF SCORE V2 BERHASIL")
print("=" * 60)