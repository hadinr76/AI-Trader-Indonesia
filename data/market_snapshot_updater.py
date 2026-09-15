import time
import json
from pathlib import Path

from data.market_data import MarketData
from scanner.stock_universe_engine import StockUniverseEngine


class MarketSnapshotUpdater:

    def __init__(self, period="1y"):
        self.period = period

    def update(self):

        lock_file = "data/cache/market_data/snapshot_update.lock"
        lock_path = Path(lock_file)

        if lock_path.exists():
            print("Market snapshot update sedang berjalan.")
            return None

        lock_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        lock_path.touch()

        try:

            print()
            print("=" * 70)
            print("MARKET SNAPSHOT UPDATE")
            print("=" * 70)

            start = time.time()

            stocks = StockUniverseEngine.get_all_stocks()

            print("Universe saham :", len(stocks))
            print("Mengambil snapshot pasar terbaru...")

            market = MarketData(
                force_refresh=True
            )

            results = market.get_bulk_daily(
                stocks,
                period=self.period
            )

            elapsed = time.time() - start

            status_file = Path(
                "data/cache/market_data/snapshot_status.json"
            )

            status = {
                "last_successful_update": time.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "stock_count": len(results),
                "elapsed_seconds": round(elapsed, 2)
            }

            with open(
                status_file,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    status,
                    file,
                    indent=4
                )

            print()
            print(
                "Snapshot berhasil :",
                len(results)
            )
            print(
                f"Waktu update       : "
                f"{elapsed:.2f} detik"
            )

            return results

        finally:

            if lock_path.exists():
                lock_path.unlink()


if __name__ == "__main__":
    updater = MarketSnapshotUpdater()
    updater.update()
