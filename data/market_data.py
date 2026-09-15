import logging
import time
from pathlib import Path

import pandas as pd
import yfinance as yf

logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

# =====================================
# KONFIGURASI KEANDALAN DATA
# =====================================
# Bisa diubah lewat env var kalau perlu, tapi punya default yang aman.

MAX_RETRIES = 2          # jumlah percobaan ulang per ticker/batch
RETRY_BACKOFF_SECONDS = 3  # jeda dasar antar percobaan ulang (naik tiap retry)
BATCH_DELAY_SECONDS = 2    # jeda antar batch saat bulk download
CACHE_DIR = Path("data/cache/market_data")
CACHE_ENABLED = True
CACHE_TTL_SECONDS = 3600

FAILED_CACHE_FILE = CACHE_DIR / "failed_tickers.txt"


class MarketData:

    def __init__(
        self,
        debug=False,
        use_cache=True,
        force_refresh=False
    ):
        self.debug = debug
        self.use_cache = use_cache and CACHE_ENABLED
        self.force_refresh = force_refresh

        if self.use_cache:
            CACHE_DIR.mkdir(parents=True, exist_ok=True)

    # =====================================
    # Daily Data - SINGLE STOCK
    # =====================================

    def get_daily(self, kode_saham, period="1y"):

        return self.get_data(
            kode=kode_saham,
            period=period,
            interval="1d"
        )

    # =====================================
    # Format Symbol
    # =====================================

    @staticmethod
    def format_symbol(kode):

        kode = kode.upper()

        if kode.startswith("^"):
            return kode

        if "-" in kode or "=" in kode:
            return kode

        return kode + ".JK"

    # =====================================
    # CACHE HELPERS
    # =====================================
    # Cache per-hari: kalau data hari ini sudah pernah diambil, tidak perlu
    # download ulang lagi ke yfinance (mengurangi risiko kena rate-limit).

    def _cache_path(self, ticker, period, interval):

        today = time.strftime("%Y-%m-%d")
        safe_ticker = ticker.replace("^", "IDX_").replace("=", "_")

        filename = f"{safe_ticker}_{period}_{interval}_{today}.pkl"

        return CACHE_DIR / filename

    def _load_cache(self, ticker, period, interval):

        if not self.use_cache:
            return None

        if self.force_refresh:
            return None

        path = self._cache_path(ticker, period, interval)

        if not path.exists():
            return None

        cache_age = time.time() - path.stat().st_mtime

        if cache_age > CACHE_TTL_SECONDS:
            return None

        try:
            return pd.read_pickle(path)
        except Exception as e:
            if self.debug:
                logger.warning(
                    "Gagal membaca cache %s: %s", path, e
                )
            return None

    def _save_cache(self, ticker, period, interval, data):

        if not self.use_cache:
            return

        path = self._cache_path(ticker, period, interval)

        try:
            data.to_pickle(path)
        except Exception as e:
            if self.debug:
                logger.warning(
                    "Gagal menyimpan cache %s: %s", path, e
                )

    # =====================================
    # Universal Downloader (SINGLE TICKER)
    # =====================================

    def get_data(
        self,
        kode,
        period="1y",
        interval="1d"
    ):

        ticker = self.format_symbol(kode)

        cached = self._load_cache(ticker, period, interval)

        if cached is not None and not cached.empty:

            if self.debug:
                logger.info("Pakai cache untuk %s", ticker)

            return cached

        last_error = None

        for attempt in range(1, MAX_RETRIES + 1):

            try:
                download_start = time.time()

                data = yf.download(
                    ticker,
                    period=period,
                    interval=interval,
                    progress=False,
                    auto_adjust=False,
                )

                download_elapsed = time.time() - download_start

                if self.debug:
                    logger.info(
                        "YFINANCE DOWNLOAD %s: %.2f detik (percobaan %d)",
                        ticker, download_elapsed, attempt
                    )

                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.get_level_values(0)

                if data.empty:
                    raise ValueError(f"Tidak ada data untuk {ticker}")

                if self.debug:
                    logger.info(
                        "Ticker %s - data terbaru:\n%s",
                        ticker, data.tail()
                    )

                self._save_cache(ticker, period, interval, data)

                return data

            except Exception as e:

                last_error = e

                logger.warning(
                    "Gagal ambil data %s (percobaan %d/%d): %s",
                    ticker, attempt, MAX_RETRIES, e
                )

                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_BACKOFF_SECONDS * attempt)

        # Semua percobaan gagal - lempar error yang jelas ke pemanggil,
        # supaya pemanggil (mis. scanner) bisa skip saham ini dan lanjut,
        # bukan bikin seluruh proses screening berhenti.
        raise ValueError(
            f"Tidak ada data untuk {ticker} setelah {MAX_RETRIES} percobaan: {last_error}"
        )

    # =====================================
    # BULK DAILY DATA
    # =====================================
    
    def _load_failed_tickers(self):

        if not FAILED_CACHE_FILE.exists():
            return set()

        try:
            with open(FAILED_CACHE_FILE, "r", encoding="utf-8") as f:
                return {
                    line.strip()
                    for line in f
                    if line.strip()
                }
        except Exception:
            return set()


    def _save_failed_tickers(self, tickers):

        CACHE_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        try:
            with open(FAILED_CACHE_FILE, "w", encoding="utf-8") as f:
                for ticker in sorted(tickers):
                    f.write(ticker + "\n")
        except Exception as e:
            logger.warning(
                "Gagal menyimpan failed ticker cache: %s",
                e
            )
    
    def get_bulk_daily(
        self,
        kode_saham_list,
        period="1y"
    ):

        if not kode_saham_list:
            return {}

        # =====================================
        # FORMAT TICKER
        # =====================================

        ticker_map = {}

        for kode in kode_saham_list:
            ticker = self.format_symbol(kode)
            ticker_map[ticker] = kode

        tickers = list(ticker_map.keys())

        results = {}

        failed_tickers = self._load_failed_tickers()

        # =====================================
        # CEK CACHE DULU - kurangi jumlah yang perlu didownload
        # =====================================

        tickers_to_download = []

        for ticker in tickers:

            if ticker in failed_tickers:
                continue

            cached = self._load_cache(ticker, period, "1d")

            if cached is not None and not cached.empty:
                results[ticker_map[ticker]] = cached
            else:
                tickers_to_download.append(ticker)

        if self.debug and results:
            logger.info(
                "Bulk: %d/%d saham diambil dari cache",
                len(results), len(tickers)
            )

        if not tickers_to_download:
            return results

        # =====================================
        # DOWNLOAD BULK PER BATCH, DENGAN RETRY + JEDA ANTAR BATCH
        # =====================================

        batch_size = 100
        data_batches = []

        total_batches = (
            (len(tickers_to_download) - 1) // batch_size + 1
        )

        for i in range(0, len(tickers_to_download), batch_size):

            batch = tickers_to_download[i:i + batch_size]
            batch_number = i // batch_size + 1

            batch_data = None

            for attempt in range(1, MAX_RETRIES + 1):

                try:
                    batch_data = yf.download(
                        batch,
                        period=period,
                        interval="1d",
                        progress=False,
                        auto_adjust=False,
                        group_by="ticker",
                        threads=8,
                        multi_level_index=True
                    )

                    if batch_data is not None and not batch_data.empty:
                        break

                    raise ValueError("Batch kosong")

                except Exception as e:

                    logger.warning(
                        "Gagal download batch %d/%d (percobaan %d/%d, %d saham): %s",
                        batch_number, total_batches, attempt, MAX_RETRIES,
                        len(batch), e
                    )

                    if attempt < MAX_RETRIES:
                        time.sleep(RETRY_BACKOFF_SECONDS * attempt)
                    else:
                        batch_data = None

            if batch_data is not None and not batch_data.empty:

                data_batches.append(batch_data)

                if self.debug:
                    logger.info(
                        "Batch %d/%d selesai (%d saham)",
                        batch_number, total_batches, len(batch)
                    )
            else:
                logger.warning(
                    "Batch %d/%d dilewati setelah %d percobaan gagal - "
                    "%d saham di batch ini tidak dapat data",
                    batch_number, total_batches, MAX_RETRIES, len(batch)
                )

            # Jeda antar batch supaya tidak kena rate-limit yfinance,
            # kecuali ini batch terakhir.
            if i + batch_size < len(tickers_to_download):
                time.sleep(BATCH_DELAY_SECONDS)

        # Gabungkan seluruh batch yang berhasil
        if not data_batches:

            if not results:
                logger.warning(
                    "Semua batch gagal - tidak ada data baru yang didapat."
                )

            return results

        data = pd.concat(data_batches, axis=1)

        if data is None or data.empty:
            return results

        # =====================================
        # MULTI TICKER DATA
        # =====================================

        if isinstance(data.columns, pd.MultiIndex):

            available_tickers = (
                data.columns.get_level_values(0).unique()
            )

            for ticker in available_tickers:

                if ticker not in ticker_map:
                    continue

                try:
                    stock_data = data[ticker].copy()

                    if stock_data.empty:
                        continue

                    stock_data = stock_data.dropna(how="all")

                    if stock_data.empty:
                        continue

                    kode = ticker_map[ticker]
                    results[kode] = stock_data

                    self._save_cache(ticker, period, "1d", stock_data)

                except Exception as e:

                    if self.debug:
                        logger.warning(
                            "Gagal membaca %s: %s", ticker, e
                        )

        # =====================================
        # SINGLE TICKER FALLBACK
        # =====================================

        else:

            if len(tickers_to_download) == 1:

                ticker = tickers_to_download[0]
                kode = ticker_map[ticker]

                stock_data = data.copy()

                if not stock_data.empty:
                    results[kode] = stock_data
                    self._save_cache(ticker, period, "1d", stock_data)

        # =====================================
        # SIMPAN TICKER YANG GAGAL
        # =====================================

        successful_tickers = {
            self.format_symbol(kode)
            for kode in results.keys()
        }

        newly_failed = (
            set(tickers_to_download)
            - successful_tickers
        )

        if newly_failed:
            failed_tickers.update(newly_failed)
            self._save_failed_tickers(failed_tickers)

        # =====================================
        # DEBUG
        # =====================================

        if self.debug:
            logger.info(
                "Bulk download selesai. Diminta: %d, Berhasil: %d",
                len(kode_saham_list), len(results)
            )

        return results
