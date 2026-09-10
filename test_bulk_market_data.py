from data.market_data import MarketData


def main():

    market = MarketData(
        debug=True
    )

    stocks = [
        "BBCA",
        "BBRI",
        "BMRI",
        "TLKM",
        "ANTM"
    ]

    print()
    print("=" * 70)
    print("TEST BULK MARKET DATA")
    print("=" * 70)

    data = market.get_bulk_daily(
        stocks,
        period="1y"
    )

    print()
    print(
        "Jumlah saham berhasil :",
        len(data)
    )

    print()

    for code, df in data.items():

        print(
            f"{code:<6} "
            f"Rows: {len(df):<5} "
            f"Last Close: "
            f"{df['Close'].iloc[-1]}"
        )


if __name__ == "__main__":

    main()