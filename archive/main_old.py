from data.data_manager import DataManager
from engine.technical_engine import TechnicalEngine

from ai.summary import AISummary
from decision.decision_engine import DecisionEngine

from watchlist.watchlist import WATCHLIST


def main():

    print("=" * 70)
    print("AI TRADER INDONESIA")
    print("=" * 70)


    for kode in WATCHLIST:

        print("\n" + "=" * 70)
        print(f"SAHAM : {kode}")
        print("=" * 70)

        # ==========================
        # Ambil Data
        # ==========================
        data = DataManager.get_daily(kode)

        # ==========================
        # Analisis Technical Engine
        # ==========================
        hasil = TechnicalEngine.analyze(data)

        trend = hasil["trend"]
        rsi = hasil["rsi"]
        macd_status = hasil["macd"]

        price_action = hasil["price_action"]
        volume_status = hasil["volume"]
        breakout_status = hasil["breakout"]

        support = hasil["support"]
        resistance = hasil["resistance"]

        score = hasil["score"]
        harga = hasil["price"]

        # ==========================
        # AI Decision
        # ==========================
        keputusan = DecisionEngine.decide(
            trend,
            score,
            rsi
        )

        # ==========================
        # AI Summary
        # ==========================
        analisis = AISummary.generate(
            data,
            trend,
            score,
            keputusan
        )

        # ==========================
        # Trading Plan
        # ==========================
        entry_bawah = support
        entry_atas = support * 1.01

        stop_loss = support * 0.97

        target = resistance

        risk = entry_atas - stop_loss
        reward = target - entry_atas

        if risk > 0:
            rr = reward / risk
        else:
            rr = 0

        # ==========================
        # Tampilkan Hasil
        # ==========================
        print(f"Harga          : {harga:.0f}")
        print(f"Trend          : {trend}")
        print(f"RSI            : {rsi:.2f}")
        print(f"Technical Score: {score}")

        print(f"MACD           : {macd_status}")
        print(f"Price Action   : {price_action}")
        print(f"Volume         : {volume_status}")
        print(f"Breakout       : {breakout_status}")

        print(f"Support        : {support:.0f}")
        print(f"Resistance     : {resistance:.0f}")

        print(f"Entry Area     : {entry_bawah:.0f} - {entry_atas:.0f}")
        print(f"Stop Loss      : {stop_loss:.0f}")
        print(f"Target Profit  : {target:.0f}")
        print(f"Risk Reward    : 1 : {rr:.2f}")

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