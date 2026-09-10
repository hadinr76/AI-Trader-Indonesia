from engine.scanner_report_engine import ScannerReportEngine

print("=" * 60)
print("SCANNER REPORT ENGINE TEST")
print("=" * 60)

# =====================================================
# Data Dummy
# =====================================================

scan_result = [

    {
        "code": "BBCA",
        "smart_signal": "STRONG BUY",
        "confidence": 90,
        "rr2": 5.2
    },

    {
        "code": "BBRI",
        "smart_signal": "BUY",
        "confidence": 82,
        "rr2": 4.1
    },

    {
        "code": "TLKM",
        "smart_signal": "WATCH",
        "confidence": 68,
        "rr2": 3.2
    },

    {
        "code": "WIKA",
        "smart_signal": "AVOID",
        "confidence": 45,
        "rr2": 1.2
    }

]

# =====================================================
# Test Engine
# =====================================================

result = ScannerReportEngine.classify(scan_result)

print()

print("HIGH CONVICTION")
print("-" * 30)

for stock in result["high_conviction"]:
    print(stock["code"])

print()

print("WATCHLIST")
print("-" * 30)

for stock in result["watchlist"]:
    print(stock["code"])

print()

print("AVOID")
print("-" * 30)

for stock in result["avoid"]:
    print(stock["code"])