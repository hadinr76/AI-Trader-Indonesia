from engine.scanner_report_engine import ScannerReportEngine
from engine.scanner_summary_engine import ScannerSummaryEngine

print("=" * 60)
print("SCANNER SUMMARY ENGINE TEST")
print("=" * 60)

# =====================================================
# Data Dummy
# =====================================================

scan_result = [

    {
        "code": "BBCA",
        "trend": "Bullish",
        "overall_score": 92,
        "confidence": 90,
        "ranking_score": 95,
        "smart_signal": "STRONG BUY",
        "rr2": 5.2
    },

    {
        "code": "BBRI",
        "trend": "Bullish",
        "overall_score": 85,
        "confidence": 82,
        "ranking_score": 88,
        "smart_signal": "BUY",
        "rr2": 4.1
    },

    {
        "code": "TLKM",
        "trend": "Bullish",
        "overall_score": 76,
        "confidence": 68,
        "ranking_score": 75,
        "smart_signal": "WATCH",
        "rr2": 3.2
    },

    {
        "code": "WIKA",
        "trend": "Bearish",
        "overall_score": 45,
        "confidence": 40,
        "ranking_score": 38,
        "smart_signal": "AVOID",
        "rr2": 1.2
    }

]

# =====================================================
# Report
# =====================================================

report = ScannerReportEngine.classify(scan_result)

# =====================================================
# Summary
# =====================================================

summary = ScannerSummaryEngine.summarize(
    scan_result,
    report
)

print()
print("TOTAL SAHAM           :", summary["total"])
print("HIGH CONVICTION       :", summary["high_conviction"])
print("WATCHLIST             :", summary["watchlist"])
print("AVOID                 :", summary["avoid"])
print()

print("BULLISH               :", summary["bullish"])
print("BEARISH               :", summary["bearish"])
print()

print("AVERAGE SCORE         :", summary["average_score"])
print("AVERAGE CONFIDENCE    :", summary["average_confidence"])
print()

print("BEST STOCK            :", summary["best_stock"]["code"])