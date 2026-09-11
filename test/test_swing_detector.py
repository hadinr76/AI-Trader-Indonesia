from data.market_data import MarketData
from analysis.swing_detector import SwingDetector


kode = "BBCA"

market = MarketData()

data = market.get_daily(
    kode,
    period="1y"
)

hasil = SwingDetector.detect(
    data,
    window=3,
    lookback=120
)

print("=" * 60)
print("SWING DETECTOR TEST")
print("=" * 60)

print()
print("Saham :", kode)

print()
print("Jumlah Swing High :", len(hasil["swing_highs"]))
print("Jumlah Swing Low  :", len(hasil["swing_lows"]))

print()
print("5 Swing High Terakhir:")
for swing in hasil["swing_highs"][-5:]:
    print(
        swing["index"],
        "-",
        swing["price"]
    )

print()
print("5 Swing Low Terakhir:")
for swing in hasil["swing_lows"][-5:]:
    print(
        swing["index"],
        "-",
        swing["price"]
    )