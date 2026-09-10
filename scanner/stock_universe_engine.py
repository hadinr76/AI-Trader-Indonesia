from scanner.stock_universe_source import (
    StockUniverseSource
)


class StockUniverseEngine:

    """
    Stock Universe Engine.

    Tugas:

    1. Membaca seluruh universe saham
       dari StockUniverseSource.

    2. Menyediakan daftar ticker kepada
       Fast Screener.

    3. Menjaga fallback universe apabila
       file CSV belum tersedia.

    Untuk produksi, gunakan:

        data/idx_stocks.csv

    sehingga jumlah saham tidak lagi
    dibatasi oleh daftar hard-coded.
    """

    # =====================================================
    # FALLBACK UNIVERSE
    # =====================================================

    FALLBACK_STOCKS = [

        "BBCA",
        "BBRI",
        "BMRI",
        "BBNI",
        "BRIS",
        "BBTN",
        "BNGA",
        "BDMN",
        "NISP",
        "BSIM",

        "TLKM",
        "ISAT",
        "EXCL",
        "MTEL",

        "ICBP",
        "INDF",
        "MYOR",
        "UNVR",
        "HMSP",
        "GGRM",
        "KLBF",
        "SIDO",

        "ASII",
        "AUTO",
        "UNTR",
        "SMGR",
        "INTP",
        "WTON",
        "ADHI",
        "PTPP",

        "ADRO",
        "ITMG",
        "PTBA",
        "ANTM",
        "MDKA",
        "INCO",
        "TINS",
        "HRUM",
        "MEDC",
        "PGAS",

        "JSMR",
        "WIKA",
        "WEGE",

        "BSDE",
        "CTRA",
        "PWON",
        "SMRA",
        "DMAS",

        "GOTO",
        "BUKA",
        "EMTK",

        "ACES",
        "ERAA",
        "MAPI",

        "AALI",
        "LSIP",
        "SIMP",

        "TOWR",
        "TBIG",
        "MIKA",
        "HEAL",
        "INKP",
        "TKIM"

    ]

    # =====================================================
    # GET ALL STOCKS
    # =====================================================

    @classmethod
    def get_all_stocks(
        cls,
        file_path=None,
        use_fallback=True
    ):

        # -------------------------------------------------
        # COBA LOAD DARI CSV
        # -------------------------------------------------

        try:

            stocks = (
                StockUniverseSource
                .load_from_csv(
                    file_path
                )
            )

            return stocks

        except (
            FileNotFoundError,
            ValueError
        ) as error:

            # ---------------------------------------------
            # FALLBACK
            # ---------------------------------------------

            if not use_fallback:

                raise error

            return cls.FALLBACK_STOCKS.copy()

    # =====================================================
    # COUNT
    # =====================================================

    @classmethod
    def count(
        cls,
        file_path=None,
        use_fallback=True
    ):

        stocks = cls.get_all_stocks(
            file_path=file_path,
            use_fallback=use_fallback
        )

        return len(
            stocks
        )

    # =====================================================
    # CHECK STOCK
    # =====================================================

    @classmethod
    def contains(
        cls,
        code,
        file_path=None,
        use_fallback=True
    ):

        code = (
            str(code)
            .strip()
            .upper()
        )

        if code.endswith(".JK"):

            code = code[:-3]

        stocks = cls.get_all_stocks(
            file_path=file_path,
            use_fallback=use_fallback
        )

        return code in stocks

    # =====================================================
    # GET SOURCE
    # =====================================================

    @classmethod
    def source(
        cls,
        file_path=None
    ):

        if StockUniverseSource.exists(
            file_path
        ):

            return "CSV"

        return "FALLBACK"

    # =====================================================
    # SUMMARY
    # =====================================================

    @classmethod
    def summary(
        cls,
        file_path=None
    ):

        stocks = cls.get_all_stocks(
            file_path=file_path
        )

        return {

            "source":
                cls.source(
                    file_path
                ),

            "count":
                len(stocks),

            "first":
                stocks[0]
                if stocks
                else None,

            "last":
                stocks[-1]
                if stocks
                else None

        }