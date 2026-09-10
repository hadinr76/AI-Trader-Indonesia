from engine.trade_manager_engine import TradeManagerEngine

print("=" * 60)
print("TRADE MANAGER TEST")
print("=" * 60)

manager = TradeManagerEngine()

trade = {

    "code": "BBCA",

    "entry_price": 6300,

    "stop_loss": 6100,

    "target1": 6600,

    "target2": 6900,

    "status": "OPEN"

}

print()

print("Saving Trade...")

saved = manager.save_trade(trade)

print("Saved :", saved)

print()

print("Checking OPEN...")

print(manager.is_trade_open("BBCA"))

print()

print("All Trades")

for item in manager.get_all_trades():

    print(dict(item))

print()

print("TEST SELESAI")