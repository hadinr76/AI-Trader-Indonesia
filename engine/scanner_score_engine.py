class ScannerScoreEngine:

    @staticmethod
    def calculate(data):

        """
        Scanner Score digunakan hanya untuk mengurutkan hasil scanner.

        Semua penilaian utama sudah dihitung pada:
        - Technical Engine
        - Fundamental Engine
        - Confidence Engine
        - Decision Engine
        - Ranking Engine

        Scanner Score hanya memberikan sedikit bonus
        berdasarkan Recommendation.
        """

        ranking = data["ranking_score"]

        recommendation = data["recommendation"]

        # ===============================
        # Bonus Recommendation
        # ===============================

        recommendation_bonus = {

            "STRONG BUY": 10,
            "BUY": 7,
            "BUY ON WEAKNESS": 5,
            "WATCH": 2,
            "WAIT": 0,
            "AVOID": -5

        }

        bonus = recommendation_bonus.get(
            recommendation,
            0
        )

        scanner_score = ranking + bonus

        if scanner_score > 100:
            scanner_score = 100

        if scanner_score < 0:
            scanner_score = 0

        return round(scanner_score, 2)