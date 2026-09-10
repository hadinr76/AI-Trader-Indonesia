from backtest.position_engine import PositionEngine

print("=" * 60)
print("POSITION ENGINE TEST")
print("=" * 60)

position = PositionEngine(

    code="BBCA",

    entry_date="2026-08-06",

    entry_price=5000,

    shares=10000,

    lots=100,

    stop_loss=4800,

    target1=5400,

    target2=5600,

    recommendation="BUY"

)

print("\nPOSISI AWAL")
print(position.to_dict())

position.next_day()
position.next_day()

position.update(5200)

print("\nSETELAH UPDATE")
print(position.to_dict())

position.close(

    exit_price=5400,

    exit_date="2026-08-09",

    status="TARGET 1"

)

print("\nSETELAH CLOSE")
print(position.to_dict())

print()
print(position)

print()
print("=" * 60)
print("POSITION ENGINE TEST SELESAI")
print("=" * 60)