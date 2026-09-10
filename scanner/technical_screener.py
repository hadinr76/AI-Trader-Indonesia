from data.market_data import MarketData
from engine.technical_engine import TechnicalEngine


class TechnicalScreener:

    """
    Technical Screener

    Fungsi:
    1. Menerima kandidat dari Fast Screener
    2. Mengambil data market kandidat
    3. Menjalankan TechnicalEngine
    4. Menggabungkan hasil Fast Screener + Technical Analysis
    5. Mengurutkan berdasarkan technical score
    """

    def __init__(
        self,
        candidates,
        period="1y"
    ):

        self.candidates = candidates
        self.period = period
        self.market = MarketData()

    # =====================================================
    # ANALYZE ONE STOCK
    # =====================================================

    @staticmethod
    def analyze_stock(
        code,
        data,
        fast_result
    ):

        try:

            if data is None:
                return None

            if data.empty:
                return None

            # TechnicalEngine membutuhkan data cukup panjang
            if len(data) < 200:
                return None

            technical = TechnicalEngine.analyze(
                data.copy()
            )

            return {

                # =========================================
                # BASIC
                # =========================================

                "code":
                    code,

                "price":
                    technical.get(
                        "price",
                        fast_result.get(
                            "price",
                            0
                        )
                    ),

                # =========================================
                # FAST SCREENER
                # =========================================

                "ma20":
                    fast_result.get(
                        "ma20",
                        0
                    ),

                "ma50":
                    fast_result.get(
                        "ma50",
                        0
                    ),

                "relative_volume":
                    fast_result.get(
                        "relative_volume",
                        0
                    ),

                "average_transaction_value_20":
                    fast_result.get(
                        "average_transaction_value_20",
                        0
                    ),

                "liquidity_status":
                    fast_result.get(
                        "liquidity_status",
                        "ILLIQUID"
                    ),    

                "passed_filters":
                    fast_result.get(
                        "passed_filters",
                        0
                    ),

                # =========================================
                # TECHNICAL ANALYSIS
                # =========================================

                "trend":
                    technical.get(
                        "trend",
                        "-"
                    ),

                "rsi":
                    round(
                        float(
                            technical.get(
                                "rsi",
                                0
                            )
                        ),
                        2
                    ),

                "macd":
                    technical.get(
                        "macd",
                        "-"
                    ),

                "price_action":
                    technical.get(
                        "price_action",
                        "-"
                    ),

                "volume":
                    technical.get(
                        "volume",
                        "-"
                    ),

                "breakout":
                    technical.get(
                        "breakout",
                        "-"
                    ),

                "candlestick":
                    technical.get(
                        "candlestick",
                        "-"
                    ),

                "support":
                    technical.get(
                        "support",
                        0
                    ),

                "resistance":
                    technical.get(
                        "resistance",
                        0
                    ),

                "momentum":
                    technical.get(
                        "momentum",
                        "-"
                    ),

                "momentum_score":
                    technical.get(
                        "momentum_score",
                        0
                    ),

                "technical_score":
                    technical.get(
                        "score",
                        0
                    )

            }

        except Exception as e:

            print(
                f"Gagal technical analysis "
                f"{code}: {e}"
            )

            return None

    # =====================================================
    # SCAN
    # =====================================================

    def scan(self):

        results = []

        if not self.candidates:

            return results

        codes = [

            item["code"]

            for item in self.candidates

        ]

        print()
        print("=" * 70)
        print("TECHNICAL SCREENER")
        print("=" * 70)

        print()
        print(
            "Jumlah kandidat :",
            len(codes)
        )

        print()
        print(
            "Mengambil market data..."
        )

        # =================================================
        # BULK DOWNLOAD
        # =================================================

        market_data = (
            self.market.get_bulk_daily(
                codes,
                period=self.period
            )
        )

        print()
        print(
            "Data berhasil :",
            len(market_data)
        )

        print()

        # =================================================
        # ANALYZE
        # =================================================

        for fast_result in self.candidates:

            code = fast_result[
                "code"
            ]

            data = market_data.get(
                code
            )

            result = (
                self.analyze_stock(
                    code,
                    data,
                    fast_result
                )
            )

            if result is None:

                continue

            results.append(
                result
            )

        # =================================================
        # SORT
        # =================================================

        results.sort(

            key=lambda x: (

                x["technical_score"],

                x["momentum_score"],

                x["relative_volume"]

            ),

            reverse=True

        )

        return results

    # =====================================================
    # TOP STOCKS
    # =====================================================

    @staticmethod
    def top_stocks(
        results,
        limit=20
    ):

        return results[
            :limit
        ]

    # =====================================================
    # PRINT RESULTS
    # =====================================================

    @staticmethod
    def print_results(
        results,
        limit=20
    ):

        print()
        print("=" * 70)
        print("TOP TECHNICAL CANDIDATES")
        print("=" * 70)

        if not results:

            print()
            print(
                "Tidak ada kandidat teknikal."
            )

            return

        top = results[
            :limit
        ]

        print()

        for index, result in enumerate(
            top,
            start=1
        ):

            print(
                f"{index:2}. "
                f"{result['code']:<6} "
                f"Price: {result['price']:<9} "
                f"RSI: {result['rsi']:<6} "
                f"Momentum: {result['momentum']:<15} "
                f"TechScore: {result['technical_score']:<6} "
                f"RVOL: {result['relative_volume']}"
            )