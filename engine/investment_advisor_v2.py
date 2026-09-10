class InvestmentAdvisorV2:

    @staticmethod
    def generate(data):

        kode = data["code"]

        trend = data["trend"]
        mtf = data["mtf_status"]
        macd = data["macd"]
        rsi = data["rsi"]
        rr = data["rr2"]
        confidence = data["confidence"]
        recommendation = data["recommendation"]
        ranking = data["ranking_score"]

               
        report = []

        # ==========================================
        # Pembuka
        # ==========================================

        if trend == "Bullish":

            pembuka = f"{kode} masih berada dalam tren bullish"

            if mtf == "VERY STRONG BULLISH":
                pembuka += " yang didukung oleh seluruh time frame."

            elif mtf == "STRONG BULLISH":
                pembuka += " dengan mayoritas time frame masih menunjukkan arah naik."

            else:
                pembuka += " walaupun belum didukung seluruh time frame."

        else:

            pembuka = (
                f"{kode} masih berada dalam tren yang relatif lemah sehingga "
                "perlu kehati-hatian."
            )

        report.append(pembuka)

        # ==========================================
        # Momentum
        # ==========================================

        momentum = []

        if macd == "Bullish Cross":
            momentum.append("MACD Bullish Cross")

        if rsi > 70:
            momentum.append("RSI berada pada area overbought")

        elif rsi < 30:
            momentum.append("RSI berada pada area oversold")

        if momentum:

            report.append(
                "Momentum saat ini didukung oleh "
                + " dan ".join(momentum)
                + "."
            )
        # ==========================================
        # Risk Reward & Confidence
        # ==========================================

        analisis = []

        if rr >= 5:
            analisis.append(
                f"Risk Reward sebesar 1:{rr:.2f} tergolong sangat menarik."
            )
        elif rr >= 3:
            analisis.append(
                f"Risk Reward sebesar 1:{rr:.2f} masih cukup baik."
            )
        else:
            analisis.append(
                f"Risk Reward sebesar 1:{rr:.2f} relatif terbatas."
            )

        if confidence >= 80:
            analisis.append(
                f"Tingkat keyakinan AI mencapai {confidence}% sehingga sinyal tergolong kuat."
            )
        elif confidence >= 60:
            analisis.append(
                f"Tingkat keyakinan AI berada di {confidence}% sehingga masih memerlukan konfirmasi tambahan."
            )
        else:
            analisis.append(
                f"Tingkat keyakinan AI baru {confidence}% sehingga sebaiknya lebih berhati-hati."
            )

        report.append(" ".join(analisis))

        # ==========================================
        # Kesimpulan
        # ==========================================

        if recommendation == "STRONG BUY":
            kesimpulan = (
                "Kesimpulannya, saham ini layak dipertimbangkan untuk pembelian segera "
                "karena mayoritas indikator menunjukkan sinyal yang sangat kuat."
            )

        elif recommendation == "BUY":
            kesimpulan = (
                "Kesimpulannya, saham ini layak dipertimbangkan untuk dibeli sesuai "
                "rencana manajemen risiko."
            )

        elif recommendation == "BUY ON WEAKNESS":
            kesimpulan = (
                "Kesimpulannya, strategi terbaik adalah melakukan pembelian secara "
                "bertahap ketika terjadi pelemahan harga."
            )

        elif recommendation == "WAIT PULLBACK":
            kesimpulan = (
                "Kesimpulannya, lebih bijak menunggu pullback menuju area entry "
                "sebelum membuka posisi baru."
            )

        else:
            kesimpulan = (
                "Kesimpulannya, kondisi saat ini belum cukup menarik sehingga "
                "lebih baik menghindari pembelian."
            )

        report.append(kesimpulan)    

        return "\n\n".join(report)

        return report