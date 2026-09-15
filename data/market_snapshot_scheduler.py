import time

from data.market_snapshot_updater import MarketSnapshotUpdater


UPDATE_INTERVAL_SECONDS = 15 * 60


def run_scheduler():

    print("=" * 70)
    print("MARKET SNAPSHOT SCHEDULER")
    print("Update otomatis setiap 15 menit")
    print("=" * 70)

    updater = MarketSnapshotUpdater()

    while True:

        cycle_start = time.time()

        try:
            updater.update()

        except Exception as error:
            print()
            print(
                f"Snapshot update gagal: {error}"
            )

        print()
        print(
            "Menunggu 15 menit "
            "untuk update berikutnya..."
        )

        elapsed = time.time() - cycle_start

        wait_seconds = max(
            0,
            UPDATE_INTERVAL_SECONDS - elapsed
        )

        print(
            f"Update berikutnya dalam "
            f"{wait_seconds / 60:.1f} menit."
        )

        time.sleep(wait_seconds)


if __name__ == "__main__":
    run_scheduler()