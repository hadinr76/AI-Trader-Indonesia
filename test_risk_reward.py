from engine.risk_reward_engine import RiskRewardEngine

print("=" * 60)
print("RISK REWARD TEST")
print("=" * 60)

hasil = RiskRewardEngine.calculate(

    entry_low=5550,
    entry_high=5750,
    stop_loss=5383,
    target1=6625,
    target2=7125

)

print(f"Entry       : {hasil['entry']}")
print(f"Risk        : {hasil['risk']}")
print(f"Reward TP1  : {hasil['reward1']}")
print(f"Reward TP2  : {hasil['reward2']}")
print(f"RR TP1      : 1 : {hasil['rr1']}")
print(f"RR TP2      : 1 : {hasil['rr2']}")