from data.market_data import MarketData
from analysis.swing_detector import SwingDetector
from analysis.sr_structure import SRStructure
from analysis.fibonacci_engine import FibonacciEngine
from analysis.confluence_engine import ConfluenceEngine


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

sr = SRStructure.calculate(
    current_price=current_price,
    swing_highs=swing["swing_highs"],
    swing_lows=swing["swing_lows"]
)

fib = FibonacciEngine.calculate(
    current_price=current_price,
    swing_highs=swing["swing_highs"],
    swing_lows=swing["swing_lows"]
)

hasil = ConfluenceEngine.calculate(
    current_price=current_price,
    sr_structure=sr,
    fibonacci=fib
)

print("=" * 60)
print("CONFLUENCE ENGINE TEST")
print("=" * 60)

print()
print("Saham       :", kode)
print("Harga       :", current_price)

print()
print("Area Low    :", hasil["area_low"])
print("Area High   :", hasil["area_high"])
print("Score       :", hasil["score"])

print()
print("Level yang bergabung:")

for level in hasil["levels"]:
    print(
        level["name"],
        ":",
        round(level["price"], 2)
    )