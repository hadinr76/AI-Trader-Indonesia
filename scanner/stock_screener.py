from engine.ai_engine import AIEngine
from engine.scanner_score_engine import ScannerScoreEngine


class StockScreener:

    """
    Stock Screener V1

    Fungsi:
    1. Menganalisis beberapa saham menggunakan AIEngine
    2. Menghitung Scanner Score
    3. Mengurutkan saham berdasarkan Scanner Score
    4. Mengambil saham terbaik
    """

    # =====================================================
    # DEFAULT WATCHLIST
    # =====================================================

    DEFAULT_STOCKS = [

        "BBCA",
        "BBRI",
        "BMRI",
        "BBNI",
        "TLKM",
        "ASII",
        "ANTM",
        "MDKA",
        "ICBP",
        "INDF"

    ]

    # =====================================================
    # INITIALIZE
    # =====================================================

    def __init__(self, stocks=None):

        if stocks is None:

            self.stocks = self.DEFAULT_STOCKS.copy()

        else:

            self.stocks = stocks

    # =====================================================
    # ANALYZE ONE STOCK
    # =====================================================

    @staticmethod
    def analyze_stock(code):

        try:

            result = AIEngine.analyze(
                code
            )

            if result is None:

                return None

            # =============================================
            # SCANNER SCORE
            # =============================================

            scanner_score = ScannerScoreEngine.calculate(
                result
            )

            # =============================================
            # SIMPAN SCANNER SCORE
            # =============================================

            result["scanner_score"] = scanner_score

            # =============================================
            # SIMPAN CODE
            # =============================================

            result["code"] = code

            return result

        except Exception as e:

            print(
                f"Gagal menganalisis {code}: {e}"
            )

            return None

    # =====================================================
    # SCAN
    # =====================================================

    def scan(self):

        results = []

        print()
        print("=" * 70)
        print("AI STOCK SCREENER")
        print("=" * 70)

        print()
        print(
            f"Jumlah saham : {len(self.stocks)}"
        )

        print()

        # =============================================
        # ANALISIS SEMUA SAHAM
        # =============================================

        for code in self.stocks:

            print(
                f"Menganalisis : {code}"
            )

            result = self.analyze_stock(
                code
            )

            if result is None:

                continue

            results.append(
                result
            )

        # =============================================
        # SORTING
        # =============================================

        results.sort(

            key=lambda x: x.get(
                "scanner_score",
                0
            ),

            reverse=True

        )

        return results

    # =====================================================
    # TOP STOCK
    # =====================================================

    def top_stocks(
        self,
        limit=5
    ):

        results = self.scan()

        return results[:limit]

    # =====================================================
    # PRINT RESULT
    # =====================================================

    @staticmethod
    def print_results(
        results
    ):

        print()
        print("=" * 70)
        print("HASIL STOCK SCREENER")
        print("=" * 70)

        if not results:

            print()
            print(
                "Tidak ada saham yang berhasil dianalisis."
            )

            return

        print()

        for index, result in enumerate(
            results,
            start=1
        ):

            code = result.get(
                "code",
                "-"
            )

            price = result.get(
                "price",
                0
            )

            recommendation = result.get(
                "recommendation",
                "-"
            )

            ranking_score = result.get(
                "ranking_score",
                0
            )

            scanner_score = result.get(
                "scanner_score",
                0
            )

            confidence = result.get(
                "confidence",
                0
            )

            trend = result.get(
                "trend",
                "-"
            )

            print(
                f"{index}. {code:<6}"
                f" Price: {price:<8}"
                f" Trend: {trend:<10}"
                f" Recommendation: {recommendation:<18}"
                f" Ranking: {ranking_score:<6}"
                f" Scanner: {scanner_score:<6}"
                f" Confidence: {confidence}"
            )

    # =====================================================
    # GET BUY CANDIDATES
    # =====================================================

    @staticmethod
    def get_buy_candidates(
        results
    ):

        buy_recommendations = [

            "STRONG BUY",

            "BUY",

            "BUY ON WEAKNESS"

        ]

        candidates = []

        for result in results:

            recommendation = result.get(
                "recommendation",
                ""
            )

            if recommendation in buy_recommendations:

                candidates.append(
                    result
                )

        return candidates