from data.market_data import MarketData
from analysis.swing_detector import SwingDetector
from analysis.sr_structure import SRStructure
from analysis.fibonacci_engine import FibonacciEngine
from analysis.confluence_engine import ConfluenceEngine
from analysis.trade_area_engine import TradeAreaEngine


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

confluence = ConfluenceEngine.calculate(
    current_price=current_price,
    sr_structure=sr,
    fibonacci=fib
)

hasil = TradeAreaEngine.calculate(
    current_price=current_price,
    confluence=confluence,
    sr_structure=sr
)

print("=" * 60)
print("TRADE AREA ENGINE TEST")
print("=" * 60)

print()
print("Saham        :", kode)
print("Harga        :", current_price)

print()
print("Buy Area Low :", hasil["buy_area_low"])
print("Buy Area High:", hasil["buy_area_high"])
print("Ideal Entry  :", hasil["ideal_entry"])

print()
print("Stop Loss    :", round(hasil["stop_loss"], 2))
print("TP1          :", hasil["tp1"])
print("TP2          :", hasil["tp2"])

print()
print("R:R TP1      :", hasil["rr_tp1"])
print("R:R TP2      :", hasil["rr_tp2"])

print()
print("Status       :", hasil["status"])
print("Score        :", hasil["confluence_score"])

print()
print("Trade Quality:", hasil["trade_quality"])
print("Best R:R     :", hasil["best_rr"])
print("Reason       :", hasil["trade_reason"])