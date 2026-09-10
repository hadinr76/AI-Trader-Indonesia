from storage.trade_history import TradeHistory
from engine.performance_tracker_engine import PerformanceTrackerEngine

print("=" * 60)
print("PERFORMANCE TRACKER UPDATE TEST")
print("=" * 60)

# ============================================================

# DATABASE

# ============================================================

history = TradeHistory()

# ============================================================

# DATA TEST

# ============================================================

test_trades = [

```
{
    "date": "2026-08-12",
    "code": "BBCA",
    "recommendation": "BUY",
    "price": 5000,
    "entry": 5000,
    "stop_loss": 4800,
    "target1": 5400,
    "target2": 5600,
    "confidence": 90,
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
},

{
    "date": "2026-08-12",
    "code": "BBRI",
    "recommendation": "BUY",
    "price": 4000,
    "entry": 4000,
    "stop_loss": 3800,
    "target1": 4400,
    "target2": 4600,
    "confidence": 85,
    "overall_score": 85,
    "ranking_score": 85,
    "status": "OPEN",
    "profit": 0,
    "shares": 5000,
    "lots": 50,
    "investment": 20000000,
    "exit_price": 0,
    "gross_profit": 0,
    "total_cost": 0,
    "net_profit": 0
},

{
    "date": "2026-08-12",
    "code": "BMRI",
    "recommendation": "BUY ON WEAKNESS",
    "price": 5000,
    "entry": 5000,
    "stop_loss": 4800,
    "target1": 5400,
    "target2": 5600,
    "confidence": 80,
    "overall_score": 80,
    "ranking_score": 80,
    "status": "OPEN",
    "profit": 0,
    "shares": 4000,
    "lots": 40,
    "investment": 20000000,
    "exit_price": 0,
    "gross_profit": 0,
    "total_cost": 0,
    "net_profit": 0
},

{
    "date": "2026-08-12",
    "code": "TLKM",
    "recommendation": "BUY",
    "price": 3000,
    "entry": 3000,
    "stop_loss": 2850,
    "target1": 3300,
    "target2": 3450,
    "confidence": 75,
    "overall_score": 75,
    "ranking_score": 75,
    "status": "OPEN",
    "profit": 0,
    "shares": 5000,
    "lots": 50,
    "investment": 15000000,
    "exit_price": 0,
    "gross_profit": 0,
    "total_cost": 0,
    "net_profit": 0
}
```

]

# ============================================================

# SIMPAN DATA TEST

# ============================================================

ids = []

for trade in test_trades:

```
history.save_trade(trade)

trades = history.get_all_trades()

trade_id = trades[0]["id"]

ids.append(trade_id)
```

print()
print("DATA TEST BERHASIL DISIMPAN")
print()

for trade_id in ids:

```
print("Trade ID :", trade_id)
```

# ============================================================

# TRANSAKSI OPEN

# ============================================================

print()
print("-" * 60)
print("TRANSAKSI OPEN")
print("-" * 60)

all_trades = history.get_all_trades()

for trade in all_trades:

```
if trade["id"] in ids:

    print(
        trade["id"],
        trade["code"],
        trade["status"]
    )
```

# ============================================================

# FAKE MARKET DATA

# ============================================================

class FakeMarketData:

```
prices = {

    "BBCA": 5400,

    "BBRI": 3700,

    "BMRI": 5000,

    "TLKM": 3500

}

def get_daily(self, code):

    import pandas as pd

    return pd.DataFrame({

        "Close": [

            self.prices[code]

        ]

    })
```

# ============================================================

# GANTI MARKET DATA DENGAN DATA TEST

# ============================================================

import engine.performance_tracker_engine as tracker_module

tracker_module.MarketData = FakeMarketData

# ============================================================

# JALANKAN PERFORMANCE TRACKER

# ============================================================

print()
print("=" * 60)
print("MENJALANKAN PERFORMANCE TRACKER")
print("=" * 60)

PerformanceTrackerEngine.update()

# ============================================================

# AMBIL DATA TERBARU

# ============================================================

updated_trades = history.get_all_trades()

results = {}

for trade in updated_trades:

```
if trade["id"] in ids:

    results[trade["code"]] = trade
```

# ============================================================

# HASIL UPDATE

# ============================================================

print()
print("=" * 60)
print("HASIL UPDATE")
print("=" * 60)

for code in [

```
"BBCA",
"BBRI",
"BMRI",
"TLKM"
```

]:

```
trade = results.get(code)

if trade is None:

    print()
    print(code, ": DATA TIDAK DITEMUKAN")

    continue

print()
print("Code   :", trade["code"])
print("Status :", trade["status"])
print("Entry  :", trade["entry"])
print("Profit :", trade["profit"])
```

# ============================================================

# VALIDASI

# ============================================================

print()
print("=" * 60)
print("VALIDASI")
print("=" * 60)

bbca = results.get("BBCA")
bbri = results.get("BBRI")
bmri = results.get("BMRI")
tlkm = results.get("TLKM")

# ============================================================

# BBCA

# Harga 5400 = TARGET 1

# ============================================================

if bbca and bbca["status"] == "TARGET1":

```
print("BBCA Target 1   : OK")
```

else:

```
print("BBCA Target 1   : GAGAL")
```

# ============================================================

# BBRI

# Harga 3700 <= STOP LOSS 3800

# ============================================================

if bbri and bbri["status"] == "CLOSED":

```
print("BBRI Stop Loss   : OK")
```

else:

```
print("BBRI Stop Loss   : GAGAL")
```

# ============================================================

# BMRI

# Harga 5000 masih di antara SL dan TARGET 1

# ============================================================

if bmri and bmri["status"] == "OPEN":

```
print("BMRI tetap OPEN  : OK")
```

else:

```
print("BMRI tetap OPEN  : GAGAL")
```

# ============================================================

# TLKM

# Harga 3500 >= TARGET 2 3450

# ============================================================

if tlkm and tlkm["status"] == "CLOSED":

```
print("TLKM Target 2    : OK")
```

else:

```
print("TLKM Target 2    : GAGAL")
```

# ============================================================

# PROFIT

# ============================================================

if bbca and float(bbca["profit"]) == 400:

```
print("BBCA Profit      : OK")
```

else:

```
print("BBCA Profit      : GAGAL")
```

if bbri and float(bbri["profit"]) == -300:

```
print("BBRI Loss        : OK")
```

else:

```
print("BBRI Loss        : GAGAL")
```

if bmri and float(bmri["profit"]) == 0:

```
print("BMRI Profit      : OK")
```

else:

```
print("BMRI Profit      : GAGAL")
```

if tlkm and float(tlkm["profit"]) == 500:

```
print("TLKM Profit      : OK")
```

else:

```
print("TLKM Profit      : GAGAL")
```

# ============================================================

# SELESAI

# ============================================================

print()
print("=" * 60)
print("PERFORMANCE TRACKER UPDATE TEST SELESAI")
print("=" * 60)
