from engine.portfolio_execution_engine import PortfolioExecutionEngine


print("=" * 70)
print("PORTFOLIO EXECUTION ENGINE TEST")
print("=" * 70)


# ==========================================================
# MODAL
# ==========================================================

capital = 100_000_000

risk_percent = 1.0

entry_date = "2026-08-07"


# ==========================================================
# DATA HASIL ANALISIS AI
# ==========================================================

results = [

    {
        "code": "BBCA",
        "ranking_score": 90,
        "recommendation": "BUY",
        "price": 5000,
        "stop_loss": 4800,
        "target1": 5400,
        "target2": 5600
    },

    {
        "code": "BBRI",
        "ranking_score": 85,
        "recommendation": "BUY",
        "price": 4000,
        "stop_loss": 3800,
        "target1": 4400,
        "target2": 4600
    },

    {
        "code": "BMRI",
        "ranking_score": 80,
        "recommendation": "BUY ON WEAKNESS",
        "price": 5000,
        "stop_loss": 4800,
        "target1": 5400,
        "target2": 5600
    },

    {
        "code": "TLKM",
        "ranking_score": 75,
        "recommendation": "BUY",
        "price": 3000,
        "stop_loss": 2850,
        "target1": 3300,
        "target2": 3450
    },

    {
        "code": "ASII",
        "ranking_score": 70,
        "recommendation": "BUY ON WEAKNESS",
        "price": 5000,
        "stop_loss": 4800,
        "target1": 5400,
        "target2": 5600
    }

]


# ==========================================================
# PORTFOLIO AWAL
# ==========================================================

portfolio = []


# ==========================================================
# EXECUTE
# ==========================================================

print()
print("=" * 70)
print("INPUT RESULTS")
print("=" * 70)

for item in results:
    print(item)

positions = PortfolioExecutionEngine.execute(

    results=results,

    capital=capital,

    risk_percent=risk_percent,

    entry_date=entry_date,

    portfolio=portfolio

)


# ==========================================================
# HASIL
# ==========================================================

print()
print("INITIAL CAPITAL :", capital)

print()
print("-" * 70)
print("HASIL EXECUTION")
print("-" * 70)


for position in positions:

    data = position.to_dict()

    print()

    print("Code           :", data["code"])

    print(
        "Recommendation :",
        data["recommendation"]
    )

    print(
        "Entry Price    :",
        data["entry_price"]
    )

    print(
        "Stop Loss      :",
        data["stop_loss"]
    )

    print(
        "Target 1       :",
        data["target1"]
    )

    print(
        "Target 2       :",
        data["target2"]
    )

    print(
        "Shares         :",
        data["shares"]
    )

    print(
        "Lots           :",
        data["lots"]
    )

    print(
        "Investment     :",
        data["investment"]
    )

    print(
        "Status         :",
        data["status"]
    )


# ==========================================================
# VALIDASI
# ==========================================================

print()
print("=" * 70)

print(
    "Jumlah posisi :",
    len(positions)
)

print(
    "Portfolio     :",
    len(portfolio)
)


if len(positions) > 0:

    print("Execution     : OK")

else:

    print("Execution     : TIDAK ADA POSISI")


# ==========================================================
# VALIDASI LOT
# ==========================================================

lot_valid = True

for position in positions:

    if position.shares != position.lots * 100:

        lot_valid = False

        break


if lot_valid:

    print("Lot calculation: OK")

else:

    print("Lot calculation: ERROR")


# ==========================================================
# VALIDASI STATUS
# ==========================================================

status_valid = True

for position in positions:

    if position.status != "OPEN":

        status_valid = False

        break


if status_valid:

    print("Position status : OK")

else:

    print("Position status : ERROR")


print()
print("=" * 70)
print("PORTFOLIO EXECUTION ENGINE TEST SELESAI")
print("=" * 70)