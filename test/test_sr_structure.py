from data.market_data import MarketData
from analysis.swing_detector import SwingDetector
from analysis.sr_structure import SRStructure


kode = "BBCA"

market = MarketData()

data = market.get_daily(
    kode,
    period="1y"
)

current_price = float(
    data["Close"].squeeze().iloc[-1]
)

swing = SwingDetector.detect(
    data,
    window=3,
    lookback=120
)

hasil = SRStructure.calculate(
    current_price=current_price,
    swing_highs=swing["swing_highs"],
    swing_lows=swing["swing_lows"]
)

print("=" * 60)
print("SUPPORT RESISTANCE STRUCTURE TEST")
print("=" * 60)

print()
print("Saham              :", kode)
print("Harga Sekarang      :", current_price)

print()
print("Major Support       :", hasil["major_support"])
print("Minor Support       :", hasil["minor_support"])

print()
print("Minor Resistance    :", hasil["minor_resistance"])
print("Major Resistance    :", hasil["major_resistance"])