from database.database import Database
from database.watchlist_manager import WatchlistManager

from engine.scanner_engine import ScannerEngine
from engine.report_engine import ReportEngine
from report.excel_report import ExcelReport


# =====================================================
# PILIH MODE SCANNER
# =====================================================

SCAN_MODE = "WATCHLIST"

# pilihan:
# WATCHLIST
# IDX30
# LQ45
# SECTOR
# ALL

SECTOR_NAME = "BANK"


def main():

    print("=" * 80)
    print("AI TRADER STOCK SCANNER")
    print("=" * 80)

    Database.initialize()

    # ==========================================
    # Ambil daftar saham
    # ==========================================

    if SCAN_MODE == "SECTOR":
        stocks = WatchlistManager.get(
            mode="SECTOR",
            sector=SECTOR_NAME
        )
    else:
        stocks = WatchlistManager.get(
            mode=SCAN_MODE
        )

    results = []

    total = len(stocks)

    # ==========================================
    # Scan
    # ==========================================

    for i, code in enumerate(stocks, start=1):

        print(f"[{i}/{total}] Scanning {code} ...")

        try:

            result = ScannerEngine.scan(code)

            if result is None:
                continue

            Database.save_scan(result)

            results.append(result)

        except Exception as e:

            print(f"❌ {code} : {e}")

    # ==========================================
    # Report
    # ==========================================

    ReportEngine.show(results)

    ExcelReport.export(results)

    print("\n✓ Scanner selesai.")


if __name__ == "__main__":
    main()