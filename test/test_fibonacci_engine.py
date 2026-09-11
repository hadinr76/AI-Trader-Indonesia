from data.market_data import MarketData
from analysis.swing_detector import SwingDetector
from analysis.fibonacci_engine import FibonacciEngine


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

hasil = FibonacciEngine.calculate(
    current_price=current_price,
    swing_highs=swing["swing_highs"],
    swing_lows=swing["swing_lows"]
)

print("=" * 60)
print("FIBONACCI ENGINE TEST")
print("=" * 60)

print()
print("Saham        :", kode)
print("Harga        :", current_price)
print("Trend Swing  :", hasil["trend"])

print()
print("Swing Low    :", hasil["swing_low"])
print("Swing High   :", hasil["swing_high"])

print()
print("Fib 23.6%    :", round(hasil["fib_236"], 2))
print("Fib 38.2%    :", round(hasil["fib_382"], 2))
print("Fib 50.0%    :", round(hasil["fib_500"], 2))
print("Fib 61.8%    :", round(hasil["fib_618"], 2))
print("Fib 78.6%    :", round(hasil["fib_786"], 2))