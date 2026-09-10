from ai.rating import Rating

nilai = [98, 90, 75, 58, 35]

print("=" * 60)
print("AI RATING TEST")
print("=" * 60)

for score in nilai:

    rating = Rating.calculate(score)

    print(
        f"Overall Score : {score}"
    )

    print(
        f"Rating        : {rating['stars']}"
    )

    print(
        f"Kategori      : {rating['category']}"
    )

    print("-" * 40)