class ExplainEngine:

    @staticmethod
    def generate(ai):

        explanation = []

        # ==========================================
        # Trend
        # ==========================================

        if ai["trend"] == "Bullish":
            explanation.append(
                "Trend masih Bullish sehingga momentum naik masih terjaga."
            )
        else:
            explanation.append(
                "Trend belum Bullish sehingga perlu lebih berhati-hati."
            )

        # ==========================================
        # Multi Time Frame
        # ==========================================

        if ai["mtf_status"] == "VERY STRONG BULLISH":
            explanation.append(
                "Semua time frame mendukung kenaikan harga."
            )

        elif ai["mtf_status"] == "STRONG BULLISH":
            explanation.append(
                "Mayoritas time frame masih Bullish."
            )

        # ==========================================
        # MACD
        # ==========================================

        if ai["macd"] == "Bullish Cross":
            explanation.append(
                "MACD Bullish Cross mengindikasikan momentum beli."
            )

        # ==========================================
        # Volume
        # ==========================================

        if ai["volume"] == "High":
            explanation.append(
                "Volume transaksi tinggi sehingga sinyal lebih valid."
            )

        # ==========================================
        # Breakout
        # ==========================================

        if ai["breakout"] == "Breakout":
            explanation.append(
                "Harga telah breakout dari area resistance."
            )

        # ==========================================
        # RSI
        # ==========================================

        if ai["rsi"] > 70:
            explanation.append(
                "RSI berada di area overbought sehingga disarankan menunggu pullback."
            )

        elif ai["rsi"] < 30:
            explanation.append(
                "RSI berada di area oversold sehingga berpotensi rebound."
            )

        # ==========================================
        # Risk Reward
        # ==========================================

        if ai["rr2"] >= 4:
            explanation.append(
                f"Risk Reward sangat baik (1 : {ai['rr2']:.2f})."
            )

        elif ai["rr2"] >= 3:
            explanation.append(
                f"Risk Reward baik (1 : {ai['rr2']:.2f})."
            )

        # ==========================================
        # Confidence
        # ==========================================

        explanation.append(
            f"Confidence AI sebesar {ai['confidence']}%."
        )

        # ==========================================
        # Fundamental
        # ==========================================

        if ai["fundamental_score"] >= 80:
            explanation.append(
                "Fundamental perusahaan sangat baik."
            )

        elif ai["fundamental_score"] >= 60:
            explanation.append(
                "Fundamental perusahaan cukup baik."
            )

        # ==========================================
        # Ranking
        # ==========================================

        explanation.append(
            f"Ranking Score sebesar {ai['ranking_score']:.1f}."
        )

        return explanation