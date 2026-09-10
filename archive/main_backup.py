from data.market_data import MarketData
from indicators.ema import EMAIndicator
from indicators.rsi import RSIIndicator
from analysis.technical_analysis import TechnicalAnalysis
from watchlist.watchlist import WATCHLIST
from scoring.technical_score import TechnicalScore
from ai.summary import AISummary
from decision.decision_engine import DecisionEngine


def main():

    print("=" * 70)
    print("AI TRADER INDONESIA")
    print("=" * 70)

    market = MarketData()

    for kode in WATCHLIST:

        print("\n" + "=" * 70)
        print(f"SAHAM : {kode}")
        print("=" * 70)

        # Ambil data
        data = market.get_daily(kode)

        # Hitung indikator
        data["EMA20"] = EMAIndicator.calculate(data, 20)
        data["EMA50"] = EMAIndicator.calculate(data, 50)
        data["EMA100"] = EMAIndicator.calculate(data, 100)
        data["EMA200"] = EMAIndicator.calculate(data, 200)
        data["RSI"] = RSIIndicator.calculate(data)

        # Analisis
        trend = TechnicalAnalysis.check_trend(data)
        score = TechnicalScore.calculate(data)
        rsi = float(data["RSI"].iloc[-1])

        # Keputusan AI
        keputusan = DecisionEngine.decide(trend, score, rsi)

        # Ringkasan AI
        analisis = AISummary.generate(data, trend, score, keputusan)

        harga = float(data["Close"].iloc[-1])

        print(f"Harga          : {harga:.0f}")
        print(f"Trend          : {trend}")
        print(f"RSI            : {rsi:.2f}")
        print(f"Technical Score: {score}")

        print("\nAnalisis AI")
        print("-" * 30)

        for teks in analisis:
            print("•", teks)

        print(f"\nRekomendasi : {keputusan}")

    print("\n" + "=" * 70)
    print("SELESAI")
    print("=" * 70)


if __name__ == "__main__":
    main()