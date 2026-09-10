class EquityCurve:

    @staticmethod
    def calculate(

        initial_capital,
        trades

    ):

        equity = initial_capital

        peak = initial_capital

        max_drawdown = 0

        curve = []

        # =====================================
        # Hitung Equity
        # =====================================

        for trade in trades:

            # Posisi yang masih OPEN belum menjadi realized profit/loss
            if trade.get("status") == "OPEN":
                continue

            equity += trade["profit"]

            # Peak Equity

            if equity > peak:

                peak = equity

            # Drawdown

            drawdown = (

                peak - equity

            ) / peak * 100

            if drawdown > max_drawdown:

                max_drawdown = drawdown

            curve.append({

                "equity": round(equity, 2),

                "peak": round(peak, 2),

                "drawdown": round(drawdown, 2)

            })

        # =====================================
        # Return
        # =====================================

        total_return = (

            equity - initial_capital

        ) / initial_capital * 100

        return {

            "initial_capital": round(initial_capital, 2),

            "final_capital": round(equity, 2),

            "return": round(total_return, 2),

            "max_drawdown": round(max_drawdown, 2),

            "curve": curve

        }