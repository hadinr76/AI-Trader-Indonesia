from engine.ai_engine import AIEngine


stocks = [
    "BBCA",
    "TLKM",
    "ANTM",
    "JPFA"
]


print("=" * 100)
print("MTF SWING V2 - PIPELINE TEST")
print("=" * 100)


for code in stocks:

    print()
    print("=" * 100)
    print("STOCK :", code)
    print("=" * 100)

    try:

        result = AIEngine.analyze(code)

        print(
            "Monthly       :",
            result.get(
                "monthly_trend",
                "Unknown"
            )
        )

        print(
            "Weekly        :",
            result.get(
                "weekly_trend",
                "Unknown"
            )
        )

        print(
            "Daily         :",
            result.get(
                "daily_trend",
                "Unknown"
            )
        )

        print(
            "4H            :",
            result.get(
                "h4_trend",
                "Unknown"
            )
        )

        print(
            "1H            :",
            result.get(
                "h1_trend",
                "Unknown"
            )
        )

        print(
            "MTF Score     :",
            result.get(
                "mtf_average_score"
            )
        )

        print(
            "MTF Status    :",
            result.get(
                "mtf_status"
            )
        )

        print(
            "Decision Score:",
            result.get(
                "decision_score"
            )
        )

        print(
            "Recommendation:",
            result.get(
                "recommendation"
            )
        )

        print(
            "Smart Signal  :",
            result.get(
                "smart_signal"
            )
        )

        print(
            "Smart Score   :",
            result.get(
                "smart_score"
            )
        )

        print(
            "Ranking Score :",
            result.get(
                "ranking_score"
            )
        )

        print("Decision MTF  :")

        mtf_reasons = [
            reason
            for reason
            in result.get(
                "decision_reason",
                []
            )
            if "MTF" in reason
        ]

        if mtf_reasons:

            for reason in mtf_reasons:
                print("  -", reason)

        else:
            print("  - Tidak ada MTF reason")

    except Exception as error:

        print(
            "ERROR:",
            type(error).__name__,
            error
        )


print()
print("=" * 100)
print("PIPELINE TEST SELESAI")
print("=" * 100)