from scanner.index_classifier import IndexClassifier


print("=" * 70)
print("INDEX CLASSIFIER TEST")
print("=" * 70)


test_codes = [

    "BBCA",
    "BBRI",
    "BMRI",
    "ANTM",
    "TLKM",
    "TIFA"

]


for code in test_codes:

    result = (
        IndexClassifier
        .classify(
            code
        )
    )

    print()

    print(
        "Code     :",
        result["code"]
    )

    print(
        "Indexes  :",
        result["indexes"]
    )

    print(
        "Category :",
        result["category"]
    )


print()
print("=" * 70)

print(
    "BBCA LQ45 :",
    IndexClassifier.is_member(
        "BBCA",
        "LQ45"
    )
)

print(
    "TIFA LQ45 :",
    IndexClassifier.is_member(
        "TIFA",
        "LQ45"
    )
)

print()
print("=" * 70)
print("INDEX CLASSIFIER TEST SELESAI")
print("=" * 70)