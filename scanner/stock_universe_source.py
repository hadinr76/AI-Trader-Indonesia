import csv
import os


class StockUniverseSource:

    """
    Membaca daftar saham Indonesia dari file CSV.

    File default:

        data/idx_stocks.csv

    Format CSV:

        code,name

    Contoh:

        BBCA,Bank Central Asia
        BBRI,Bank Rakyat Indonesia
        BMRI,Bank Mandiri

    Source ini sengaja dipisahkan dari
    StockUniverseEngine agar daftar saham
    dapat diperbarui tanpa mengubah kode engine.
    """

    DEFAULT_FILE = "data/idx_stocks.csv"

    # =====================================================
    # LOAD CSV
    # =====================================================

    @classmethod
    def load_from_csv(
        cls,
        file_path=None
    ):

        if file_path is None:

            file_path = cls.DEFAULT_FILE

        # -------------------------------------------------
        # CEK FILE
        # -------------------------------------------------

        if not os.path.exists(file_path):

            raise FileNotFoundError(
                f"File universe tidak ditemukan: {file_path}"
            )

        stocks = []

        # -------------------------------------------------
        # BACA CSV
        # -------------------------------------------------

        with open(
            file_path,
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            reader = csv.DictReader(
                file
            )

            # ---------------------------------------------
            # CEK HEADER
            # ---------------------------------------------

            if reader.fieldnames is None:

                raise ValueError(
                    "File CSV tidak memiliki header."
                )

            # ---------------------------------------------
            # CARI KOLOM CODE
            # ---------------------------------------------

            code_column = None

            for column in reader.fieldnames:

                if column is None:

                    continue

                normalized = (
                    column
                    .strip()
                    .lower()
                )

                if normalized in (
                    "code",
                    "kode",
                    "ticker",
                    "symbol"
                ):

                    code_column = column

                    break

            if code_column is None:

                raise ValueError(
                    "Kolom kode saham tidak ditemukan. "
                    "Gunakan header: code,name"
                )

            # ---------------------------------------------
            # BACA DATA
            # ---------------------------------------------

            for row in reader:

                raw_code = row.get(
                    code_column,
                    ""
                )

                if raw_code is None:

                    continue

                code = (
                    str(raw_code)
                    .strip()
                    .upper()
                )

                # -----------------------------------------
                # VALIDASI DASAR
                # -----------------------------------------

                if not code:

                    continue

                # -----------------------------------------
                # HILANGKAN SUFFIX .JK
                # -----------------------------------------

                if code.endswith(".JK"):

                    code = code[:-3]

                # -----------------------------------------
                # TICKER SAHAM INDONESIA
                # -----------------------------------------

                if not code.isalnum():

                    continue

                if len(code) < 2:

                    continue

                if len(code) > 6:

                    continue

                stocks.append(
                    code
                )

        # =================================================
        # REMOVE DUPLICATES
        # =================================================

        stocks = list(
            dict.fromkeys(
                stocks
            )
        )

        # =================================================
        # SORT
        # =================================================

        stocks.sort()

        # =================================================
        # VALIDASI HASIL
        # =================================================

        if not stocks:

            raise ValueError(
                "Tidak ada ticker valid "
                "di dalam file universe."
            )

        return stocks

    # =====================================================
    # CHECK SOURCE
    # =====================================================

    @classmethod
    def exists(
        cls,
        file_path=None
    ):

        if file_path is None:

            file_path = cls.DEFAULT_FILE

        return os.path.exists(
            file_path
        )

    # =====================================================
    # COUNT
    # =====================================================

    @classmethod
    def count(
        cls,
        file_path=None
    ):

        stocks = cls.load_from_csv(
            file_path
        )

        return len(
            stocks
        )