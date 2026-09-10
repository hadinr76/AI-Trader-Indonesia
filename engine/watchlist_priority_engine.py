class WatchlistPriorityEngine:

    @staticmethod
    def calculate(
        decision_score,
        confidence,
        technical_ranking,
        fundamental_score,
        rsi,
        relative_volume,
        liquidity_status,
        entry_recommendation,
        distance_entry_high,
        breakout_status
    ):

        score = 0
        reasons = []

        # Decision Score
        score += decision_score * 0.25

        # Confidence
        score += confidence * 0.20

        # Technical Ranking
        score += technical_ranking * 0.20

        # Fundamental
        score += fundamental_score * 0.10

        # RSI Timing
        if 50 <= rsi <= 70:
            score += 10
            reasons.append("RSI ideal")
        elif 45 <= rsi < 50:
            score += 6
            reasons.append("RSI mendekati bullish")
        elif 70 < rsi <= 75:
            score += 5
            reasons.append("RSI mulai tinggi")

        # Relative Volume
        if relative_volume >= 2:
            score += 8
            reasons.append("Volume sangat kuat")
        elif relative_volume >= 1:
            score += 5
            reasons.append("Volume mendukung")

        # Liquidity
        liquidity_score = {
            "VERY LIQUID": 10,
            "LIQUID": 8,
            "MODERATE": 5,
            "LOW LIQUIDITY": 0,
            "ILLIQUID": 0
        }

        score += liquidity_score.get(
            liquidity_status,
            0
        )

        # Entry Proximity
        # Mengukur jarak harga terhadap batas atas entry zone

        if distance_entry_high <= 0:
            score += 10
            reasons.append("Harga berada di zona entry")

        elif distance_entry_high <= 3:
            score += 9
            reasons.append("Sangat dekat zona entry")

        elif distance_entry_high <= 5:
            score += 8
            reasons.append("Dekat zona entry")

        elif distance_entry_high <= 10:
            score += 5
            reasons.append("Masih dekat zona entry")

        elif distance_entry_high <= 15:
            score += 2
            reasons.append("Mulai jauh dari zona entry")

        # Near breakout
        if breakout_status == "Belum Breakout":
            score += 2

        score = round(score, 2)

        # Classification
        if score >= 75:
            status = "NEAR BUY"
        elif score >= 65:
            status = "WATCHLIST PRIORITY"
        else:
            status = "WATCH"

        return {
            "score": score,
            "status": status,
            "reasons": reasons
        }