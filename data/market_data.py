import time
import yfinance as yf
import pandas as pd


class MarketData:

    def __init__(self, debug=False):
        self.debug = debug

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
    # Universal Downloader
    # =====================================

    def get_data(
        self,
        kode,
        period="1y",
        interval="1d"
    ):

        ticker = self.format_symbol(kode)

        download_start = time.time()

        data = yf.download(
            ticker,
            period=period,
            interval=interval,
            progress=False,
            auto_adjust=False
        )

        download_elapsed = time.time() - download_start

        print()
        print(
            f"YFINANCE DOWNLOAD   : "
            f"{download_elapsed:.2f} DETIK"
        )

        if isinstance(data.columns, pd.MultiIndex):

            data.columns = (
                data.columns
                .get_level_values(0)
            )

        if data.empty:

            raise ValueError(
                f"Tidak ada data untuk {ticker}"
            )

        # =====================================
        # DEBUG
        # =====================================

        if self.debug:

            print(
                "\n=============================="
            )

            print(
                "Ticker :",
                ticker
            )

            print(
                data.tail()
            )

            print(
                "==============================\n"
            )

        return data

    # =====================================
    # BULK DAILY DATA
    # =====================================

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

            ticker = self.format_symbol(
                kode
            )

            ticker_map[ticker] = kode

        tickers = list(
            ticker_map.keys()
        )

        # =====================================
        # DOWNLOAD BULK PER BATCH
        # =====================================

        batch_size = 40
        data_batches = []

        for i in range(0, len(tickers), batch_size):

            batch = tickers[
                i:i + batch_size
            ]

            try:

                batch_data = yf.download(
                    batch,
                    period=period,
                    interval="1d",
                    progress=False,
                    auto_adjust=False,
                    group_by="ticker",
                    threads=4,
                    multi_level_index=True
                )

                if (
                    batch_data is not None
                    and not batch_data.empty
                ):

                    data_batches.append(
                        batch_data
                    )

                if self.debug:

                    print(
                        f"Batch "
                        f"{i // batch_size + 1} "
                        f"selesai "
                        f"({len(batch)} saham)"
                    )

            except Exception as e:

                print(
                    f"Gagal download batch "
                    f"{i // batch_size + 1}: {e}"
                )

        # Gabungkan seluruh batch
        if not data_batches:

            return {}

        data = pd.concat(
            data_batches,
            axis=1
        )

        # =====================================
        # VALIDASI
        # =====================================

        if data is None or data.empty:

            return {}

        results = {}

        # =====================================
        # MULTI TICKER DATA
        # =====================================

        if isinstance(
            data.columns,
            pd.MultiIndex
        ):

            available_tickers = (
                data.columns
                .get_level_values(0)
                .unique()
            )

            for ticker in available_tickers:

                if ticker not in ticker_map:

                    continue

                try:

                    stock_data = data[
                        ticker
                    ].copy()

                    if stock_data.empty:

                        continue

                    stock_data = (
                        stock_data
                        .dropna(
                            how="all"
                        )
                    )

                    if stock_data.empty:

                        continue

                    kode = ticker_map[
                        ticker
                    ]

                    results[kode] = (
                        stock_data
                    )

                except Exception as e:

                    if self.debug:

                        print(
                            f"Gagal membaca "
                            f"{ticker}: {e}"
                        )

        # =====================================
        # SINGLE TICKER FALLBACK
        # =====================================

        else:

            if len(tickers) == 1:

                ticker = tickers[0]

                kode = ticker_map[
                    ticker
                ]

                stock_data = data.copy()

                if not stock_data.empty:

                    results[kode] = (
                        stock_data
                    )

        # =====================================
        # DEBUG
        # =====================================

        if self.debug:

            print()
            print(
                "Bulk download selesai."
            )

            print(
                "Diminta :",
                len(kode_saham_list)
            )

            print(
                "Berhasil:",
                len(results)
            )

            print()

        return results