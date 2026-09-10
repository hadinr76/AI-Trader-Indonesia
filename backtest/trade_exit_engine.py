class TradeExitEngine:

    @staticmethod
    def check(

        high,
        low,
        close,

        stop_loss,
        target1,
        target2,

        holding_days,

        max_holding=20

    ):

        # ==========================================
        # STOP LOSS
        # ==========================================

        if low <= stop_loss:

            return {

                "status": "STOP LOSS",

                "exit_price": stop_loss

            }

        # ==========================================
        # TARGET 2
        # ==========================================

        if high >= target2:

            return {

                "status": "TARGET 2",

                "exit_price": target2

            }

        # ==========================================
        # TARGET 1
        # ==========================================

        if high >= target1:

            return {

                "status": "TARGET 1",

                "exit_price": target1

            }

        # ==========================================
        # MAX HOLDING
        # ==========================================

        if holding_days >= max_holding:

            return {

                "status": "TIME EXIT",

                "exit_price": close

            }

        return None