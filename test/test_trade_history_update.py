from storage.trade_history import TradeHistory


print("=" * 60)
print("TRADE HISTORY UPDATE TEST")
print("=" * 60)


# =====================================================
# INIT
# =====================================================

history = TradeHistory()


# =====================================================
# BUAT DATA TEST
# =====================================================

trade = {

    "date": "2026-08-10",

    "code": "BBCA",

    "recommendation": "BUY",

    "price": 5000,

    "entry": 5000,

    "stop_loss": 4800,

    "target1": 5400,

    "target2": 5600,

    "confidence": 85,

    "overall_score": 90,

    "ranking_score": 90,

    "status": "OPEN",

    "profit": 0,

    "shares": 5000,

    "lots": 50,

    "investment": 25000000,

    "exit_price": 0,

    "gross_profit": 0,

    "total_cost": 0,

    "net_profit": 0

}


# =====================================================
# SIMPAN TRADE
# =====================================================

history.save_trade(trade)


# =====================================================
# AMBIL TRADE TERBARU
# =====================================================

trades = history.get_all_trades()

trade_id = trades[0]["id"]


print()
print("TRADE BERHASIL DISIMPAN")
print("Trade ID :", trade_id)


# =====================================================
# UPDATE TRADE
# =====================================================

history.update_trade(

    trade_id,

    {

        "status": "CLOSED",

        "profit": 2313808.75,

        "exit_price": 5500,

        "gross_profit": 2447500,

        "total_cost": 133691.25,

        "net_profit": 2313808.75

    }

)


# =====================================================
# BACA ULANG DATA
# =====================================================

updated = history.get_trade(
    trade_id
)


print()
print("HASIL UPDATE")
print("-" * 60)

print(
    "Code          :",
    updated["code"]
)

print(
    "Status        :",
    updated["status"]
)

print(
    "Entry Price   :",
    updated["entry"]
)

print(
    "Exit Price    :",
    updated["exit_price"]
)

print(
    "Shares        :",
    updated["shares"]
)

print(
    "Lots          :",
    updated["lots"]
)

print(
    "Gross Profit  :",
    updated["gross_profit"]
)

print(
    "Total Cost    :",
    updated["total_cost"]
)

print(
    "Net Profit    :",
    updated["net_profit"]
)


# =====================================================
# VALIDASI
# =====================================================

assert updated["status"] == "CLOSED"

assert updated["exit_price"] == 5500

assert updated["shares"] == 5000

assert updated["lots"] == 50

assert updated["gross_profit"] == 2447500

assert updated["total_cost"] == 133691.25

assert updated["net_profit"] == 2313808.75


print()
print("Status        : OK")
print("Exit Price    : OK")
print("Shares        : OK")
print("Lots          : OK")
print("Gross Profit  : OK")
print("Total Cost    : OK")
print("Net Profit    : OK")

print()
print("=" * 60)
print("TRADE HISTORY UPDATE TEST SELESAI")
print("=" * 60)
