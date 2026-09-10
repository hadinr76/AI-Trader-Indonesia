class AISummary:

    @staticmethod
    def generate(data, trend, score, keputusan):

        close = float(data["Close"].iloc[-1])
        ema20 = float(data["EMA20"].iloc[-1])
        rsi = float(data["RSI"].iloc[-1])

        hasil = []

        hasil.append(f"Harga saat ini {close:.0f}")

        if close > ema20:
            hasil.append("Harga berada di atas EMA20 sehingga tren jangka pendek masih naik.")
        else:
            hasil.append("Harga berada di bawah EMA20 sehingga tren jangka pendek masih lemah.")

        if rsi >= 70:
            hasil.append("RSI menunjukkan kondisi overbought.")
        elif rsi >= 50:
            hasil.append("RSI masih menunjukkan momentum bullish yang sehat.")
        elif rsi >= 30:
            hasil.append("Momentum masih lemah.")
        else:
            hasil.append("RSI berada pada area oversold.")

        if score >= 80:
            hasil.append("Kondisi teknikal sangat kuat.")
        elif score >= 60:
            hasil.append("Kondisi teknikal cukup baik.")
        elif score >= 40:
            hasil.append("Perlu menunggu konfirmasi.")
        else:
            hasil.append("Kondisi teknikal masih lemah.")

        return hasil