from data.market_data import MarketData
from analysis.swing_detector import SwingDetector
from analysis.sr_structure import SRStructure
from analysis.fibonacci_engine import FibonacciEngine
from analysis.confluence_engine import ConfluenceEngine
from analysis.trade_area_engine import TradeAreaEngine


stocks = [
    "BBCA",
    "BBRI",
    "BMRI",
    "ANTM",
    "TLKM"
]

market = MarketData()


for kode in stocks:

    print()
    print("=" * 70)
    print("SAHAM :", kode)
    print("=" * 70)

    try:

        data = market.get_daily(
            kode,
            period="1y"
        )

        current_price = float(
            data["Close"].squeeze().iloc[-1]
        )

        swing = SwingDetector.detect(
            data,
            window=3,
            lookback=120
        )

        sr = SRStructure.calculate(
            current_price=current_price,
            swing_highs=swing["swing_highs"],
            swing_lows=swing["swing_lows"]
        )

        fib = FibonacciEngine.calculate(
            current_price=current_price,
            swing_highs=swing["swing_highs"],
            swing_lows=swing["swing_lows"]
        )

        confluence = ConfluenceEngine.calculate(
            current_price=current_price,
            sr_structure=sr,
            fibonacci=fib
        )

        hasil = TradeAreaEngine.calculate(
            current_price=current_price,
            confluence=confluence,
            sr_structure=sr
        )

        print("Harga            :", current_price)

        print()
        print("Major Support    :", sr["major_support"])
        print("Minor Support    :", sr["minor_support"])
        print("Minor Resistance :", sr["minor_resistance"])
        print("Major Resistance :", sr["major_resistance"])

        print()
        print("Fib 38.2%        :", round(fib["fib_382"], 2))
        print("Fib 50.0%        :", round(fib["fib_500"], 2))
        print("Fib 61.8%        :", round(fib["fib_618"], 2))
        print("Fib 78.6%        :", round(fib["fib_786"], 2))

        print()
        print(
            "Buy Area         :",
            hasil["buy_area_low"],
            "-",
            hasil["buy_area_high"]
        )

        print("Ideal Entry      :", hasil["ideal_entry"])
        print("Stop Loss        :", hasil["stop_loss"])
        print("TP1              :", hasil["tp1"])
        print("TP2              :", hasil["tp2"])

        print()
        print("R:R TP1          :", hasil["rr_tp1"])
        print("R:R TP2          :", hasil["rr_tp2"])

        print()
        print("Status           :", hasil["status"])
        print("Trade Quality    :", hasil["trade_quality"])
        print("Best R:R         :", hasil["best_rr"])
        print("Confluence Score :", hasil["confluence_score"])
        print("Reason           :", hasil["trade_reason"])

    except Exception as e:

        print(
            "ERROR :",
            str(e)
        )