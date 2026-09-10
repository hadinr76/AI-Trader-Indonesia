class InvestmentAdvisorEngine:

    @staticmethod
    def generate(data):

        advisor = []

        kode = data["code"]

        trend = data["trend"]
        mtf = data["mtf_status"]
        macd = data["macd"]
        rsi = data["rsi"]
        rr = data["rr2"]
        confidence = data["confidence"]
        recommendation = data["recommendation"]
        ranking = data["ranking_score"]

        # ======================================
        # Trend
        # ======================================

        if trend == "Bullish":
            advisor.append(
                f"{kode} masih berada dalam tren naik sehingga peluang kenaikan masih terbuka."
            )
        else:
            advisor.append(
                "Tren saham masih lemah sehingga perlu berhati-hati."
            )

        # ======================================
        # Multi Time Frame
        # ======================================

        if mtf == "VERY STRONG BULLISH":
            advisor.append(
                "Seluruh time frame mendukung kenaikan harga sehingga sinyal bullish semakin kuat."
            )

        elif mtf == "STRONG BULLISH":
            advisor.append(
                "Mayoritas time frame masih berada dalam kondisi bullish."
            )

        # ======================================
        # MACD
        # ======================================

        if macd == "Bullish Cross":
            advisor.append(
                "MACD Bullish Cross menunjukkan momentum beli masih berlangsung."
            )

        # ======================================
        # RSI
        # ======================================

        if rsi > 70:
            advisor.append(
                "RSI berada pada area overbought sehingga pembelian sebaiknya menunggu pullback."
            )

        elif rsi < 30:
            advisor.append(
                "RSI oversold sehingga berpotensi terjadi rebound."
            )

        # ======================================
        # Risk Reward
        # ======================================

        if rr >= 4:
            advisor.append(
                f"Risk Reward sebesar 1:{rr:.2f} tergolong sangat menarik."
            )

        elif rr >= 3:
            advisor.append(
                f"Risk Reward sebesar 1:{rr:.2f} masih layak dipertimbangkan."
            )

        # ======================================
        # Confidence
        # ======================================

        if confidence >= 80:
            advisor.append(
                "Confidence AI sangat tinggi sehingga kualitas sinyal cukup meyakinkan."
            )

        elif confidence >= 60:
            advisor.append(
                "Confidence AI berada pada level menengah sehingga tetap perlu konfirmasi tambahan."
            )

        # ======================================
        # Ranking
        # ======================================

        if ranking >= 85:
            advisor.append(
                "Saham ini termasuk kandidat terbaik berdasarkan hasil AI Scanner."
            )

        elif ranking >= 70:
            advisor.append(
                "Saham ini masih berada dalam kelompok saham yang menarik."
            )

        # ======================================
        # Final Recommendation
        # ======================================

        if recommendation == "STRONG BUY":

            advisor.append(
                "Kesimpulan: saham layak diprioritaskan untuk akumulasi."
            )

        elif recommendation == "BUY":

            advisor.append(
                "Kesimpulan: saham layak dibeli sesuai money management."
            )

        elif recommendation == "BUY ON WEAKNESS":

            advisor.append(
                "Kesimpulan: lakukan pembelian bertahap saat harga melemah."
            )

        elif recommendation == "WAIT PULLBACK":

            advisor.append(
                "Kesimpulan: sebaiknya menunggu pullback sebelum melakukan entry."
            )

        else:

            advisor.append(
                "Kesimpulan: belum layak untuk dibeli."
            )

        return advisor