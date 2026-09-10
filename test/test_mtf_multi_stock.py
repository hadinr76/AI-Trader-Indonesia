from engine.multi_timeframe_engine import MultiTimeFrameEngine


stocks = [
    "BBCA",
    "BBRI",
    "BMRI",
    "TLKM",
    "ANTM",
    "GOTO",
    "PGAS",
    "JPFA",
    "KLBF",
    "ASII"
]


print("=" * 95)
print("MULTI STOCK REAL DATA TEST - MTF SWING V2")
print("=" * 95)

print(
    f"{'CODE':<7}"
    f"{'MONTHLY':<18}"
    f"{'WEEKLY':<18}"
    f"{'DAILY':<18}"
    f"{'4H':<18}"
    f"{'1H':<18}"
    f"{'SCORE':<8}"
    f"{'STATUS'}"
)

print("-" * 130)


for code in stocks:

    try:

        result = MultiTimeFrameEngine.analyze(code)

        monthly = result.get(
            "Monthly",
            {}
        ).get("trend", "Unknown")

        weekly = result.get(
            "Weekly",
            {}
        ).get("trend", "Unknown")

        daily = result.get(
            "Daily",
            {}
        ).get("trend", "Unknown")

        h4 = result.get(
            "4H",
            {}
        ).get("trend", "Unknown")

        h1 = result.get(
            "1H",
            {}
        ).get("trend", "Unknown")

        summary = result.get(
            "summary",
            {}
        )

        score = summary.get(
            "average_score",
            0
        )

        status = summary.get(
            "status",
            "Unknown"
        )

        print(
            f"{code:<7}"
            f"{monthly:<18}"
            f"{weekly:<18}"
            f"{daily:<18}"
            f"{h4:<18}"
            f"{h1:<18}"
            f"{score:<8}"
            f"{status}"
        )

    except Exception as error:

        print(
            f"{code:<7} ERROR: {error}"
        )


print()
print("=" * 95)
print("MULTI STOCK TEST SELESAI")
print("=" * 95)