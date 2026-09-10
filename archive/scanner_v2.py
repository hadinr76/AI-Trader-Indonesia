from database.stocks import STOCKS

from engine.scanner_engine import ScannerEngine
from engine.portfolio_engine import PortfolioEngine


def main():

    print("=" * 70)
    print("AI STOCK SCANNER V2")
    print("=" * 70)

    print()

    # ==================================================
    # Scan Semua Saham
    # ==================================================

    result = ScannerEngine.scan(STOCKS)

    results = result["results"]

    # ==================================================
    # Portfolio Allocation
    # ==================================================

    portfolio = PortfolioEngine.allocate(
        results,
        capital=100_000_000
    )

    print()

    # ==================================================
    # TOP AI PICKS
    # ==================================================

    print("=" * 70)
    print("TOP AI PICKS")
    print("=" * 70)

    print(
        f"{'Rank':<5}"
        f"{'Kode':<8}"
        f"{'Scanner':<12}"
        f"{'Signal':<18}"
        f"{'Conf':<8}"
        f"{'RR':<8}"
        f"{'Trend'}"
    )

    print("-" * 70)

    for i, saham in enumerate(results[:10], start=1):

        print(
            f"{i:<5}"
            f"{saham['code']:<8}"
            f"{saham['scanner_score']:<12.1f}"
            f"{saham['smart_signal']:<18}"
            f"{str(saham['confidence']) + '%':<8}"
            f"{saham['rr2']:<8.2f}"
            f"{saham['trend']}"
        )

    # ==================================================
    # PORTFOLIO ALLOCATION
    # ==================================================

    print()
    print("=" * 70)
    print("PORTFOLIO ALLOCATION")
    print("=" * 70)

    for item in portfolio:

        print("-" * 70)

        print(f"Kode            : {item['code']}")
        print(f"Recommendation  : {item['recommendation']}")
        print(f"Weight          : {item['weight']}%")
        print(f"Allocation      : Rp{item['allocation']:,.0f}")
        print(f"Harga           : Rp{item['price']:,.0f}")
        print(f"Recommended Lot : {item['lots']}")
        print(f"Investment      : Rp{item['investment']:,.0f}")
        print(f"Remaining Cash  : Rp{item['remaining']:,.0f}")

    print()
    print("=" * 70)
    print("SCAN SELESAI")
    print("=" * 70)


if __name__ == "__main__":
    main()