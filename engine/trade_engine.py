class TradeEngine:

    @staticmethod
    def simulate(data):

        trades = []

        position = None

        for i in range(1, len(data)):

            close = float(data["Close"].iloc[i])

            ema20 = float(data["EMA20"].iloc[i])

            ema50 = float(data["EMA50"].iloc[i])

            # BUY
            if position is None:

                if close > ema20 and ema20 > ema50:

                    position = {
                        "entry": close,
                        "entry_index": i
                    }

            # SELL
            else:

                if close < ema20:

                    exit_price = close

                    profit = (
                        exit_price - position["entry"]
                    ) / position["entry"] * 100

                    trades.append({

                        "entry": position["entry"],

                        "exit": exit_price,

                        "profit": profit,

                        "holding": i - position["entry_index"]

                    })

                    position = None

        return trades