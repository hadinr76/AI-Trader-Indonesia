from backtest.trade_exit_engine import TradeExitEngine


class TradeSimulator:

    @staticmethod
    def simulate(

        data,
        entry_price,
        stop_loss,
        target1,
        target2,
        shares,
        lots

    ):

        result = {

            "status": "OPEN",

            "entry_filled": False,

            "entry_wait_days": 0,

            "exit_price": None,

            "profit": 0,

            "return": 0,

            "holding_days": 0,

            "shares": shares,

            "lots": lots

        }

        # ==========================================
        # Simulasi Pergerakan Harga
        # ==========================================

        for i in range(len(data)):

            high = float(data["High"].iloc[i])

            low = float(data["Low"].iloc[i])

            close = float(data["Close"].iloc[i])

            # ==========================================
            # VALIDASI ENTRY
            # ==========================================

            if not result["entry_filled"]:

                if not (low <= entry_price <= high):

                    result["entry_wait_days"] += 1

                    # Maksimal menunggu entry 5 hari perdagangan
                    if result["entry_wait_days"] >= 5:
                        break

                    continue

                result["entry_filled"] = True

            # ==========================================
            # HITUNG HOLDING DAY
            # ==========================================

            result["holding_days"] += 1

            # ==========================================
            # Cek Exit
            # ==========================================

            exit_result = TradeExitEngine.check(

                high=high,

                low=low,

                close=close,

                stop_loss=stop_loss,

                target1=target1,

                target2=target2,

                holding_days=result["holding_days"]

            )

            if exit_result is not None:

                result["status"] = exit_result["status"]

                result["exit_price"] = exit_result["exit_price"]

                break

        # ==========================================
        # ENTRY TIDAK PERNAH TERSENTUH
        # ==========================================

        if not result["entry_filled"]:

            result["status"] = "NOT FILLED"
            result["exit_price"] = entry_price
            result["profit"] = 0
            result["investment"] = 0
            result["return"] = 0

            return result

        # ==========================================
        # Jika belum Exit
        # ==========================================

        if result["exit_price"] is None:

            result["status"] = "OPEN"

            result["exit_price"] = float(data["Close"].iloc[-1])

        # ==========================================
        # Hitung Profit
        # ==========================================

        price_difference = (

            result["exit_price"] - entry_price

        )

        result["profit_per_share"] = price_difference

        result["profit"] = (

            price_difference * shares

        )

        result["investment"] = (

            entry_price * shares

        )

        result["return"] = (

            result["profit"] /

            result["investment"]

        ) * 100

        return result