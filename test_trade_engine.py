from data.data_manager import DataManager
from indicators.ema import EMAIndicator
from engine.trade_engine import TradeEngine

print("=" * 60)
print("TRADE ENGINE TEST")
print("=" * 60)

data = DataManager.get_daily("BBCA")

data["EMA20"] = EMAIndicator.calculate(data, 20)
data["EMA50"] = EMAIndicator.calculate(data, 50)

trades = TradeEngine.simulate(data)

print(f"Total Trade : {len(trades)}")
print()

for trade in trades[:10]:
    print(trade)