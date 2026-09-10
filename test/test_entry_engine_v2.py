from engine.entry_engine import EntryEngine


print("=" * 70)
print("ENTRY ENGINE V2 - EXTENDED ENTRY ZONE TEST")
print("=" * 70)


support = 100
resistance = 200

# Dengan:
# support    = 100
# resistance = 200
#
# Entry Low  = 100
# Entry High = 120
#
# Extended Entry High = 120 * 1.05 = 126


tests = [

    (
        "DALAM ENTRY ZONE",
        115
    ),

    (
        "4% DI ATAS ENTRY HIGH",
        124.8
    ),

    (
        "TEPAT 5% DI ATAS ENTRY HIGH",
        126
    ),

    (
        "6% DI ATAS ENTRY HIGH",
        127.2
    ),

]


for name, price in tests:

    result = EntryEngine.calculate(
        price=price,
        support=support,
        resistance=resistance,
        breakout=None
    )

    print()
    print("-" * 70)
    print(name)
    print("-" * 70)

    print(
        "Price          :",
        price
    )

    print(
        "Entry Low      :",
        result["entry_low"]
    )

    print(
        "Entry High     :",
        result["entry_high"]
    )

    print(
        "Recommendation :",
        result["recommendation"]
    )

    print(
        "Reason         :",
        result["reason"]
    )


print()
print("=" * 70)
print("TEST SELESAI")
print("=" * 70)