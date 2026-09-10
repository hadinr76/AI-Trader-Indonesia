from scanner.fast_screener import FastScreener


print("=" * 70)
print("FAST SCREENER - 981 STOCK TEST")
print("=" * 70)


screener = FastScreener(
    period="1y"
)


print()
print(
    "Universe :",
    len(screener.stocks)
)


results = screener.scan()


print()
print("=" * 70)
print("HASIL FAST SCREENING")
print("=" * 70)


print()
print(
    "Jumlah saham berhasil dianalisis :",
    len(results)
)


passed = FastScreener.passed_stocks(
    results
)


print(
    "Jumlah saham PASS               :",
    len(passed)
)


FastScreener.print_passed(
    results
)


print()
print("=" * 70)
print("FAST SCREENER TEST SELESAI")
print("=" * 70)