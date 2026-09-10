class PerformanceReport:

    @staticmethod
    def generate(

        statistics,
        equity

    ):

        report = {

            # =====================================
            # Trade
            # =====================================

            "total_trade": statistics["total_trade"],

            "open_trade": statistics.get("open_trade", 0),

            "win": statistics["win"],

            "loss": statistics["loss"],

            "win_rate": statistics["win_rate"],

            # =====================================
            # Profit
            # =====================================

            "gross_profit": statistics["gross_profit"],

            "gross_loss": statistics["gross_loss"],

            "net_profit": statistics["net_profit"],

            "profit_factor": statistics["profit_factor"],

            "expectancy": statistics["expectancy"],

            # =====================================
            # Equity
            # =====================================

            "initial_capital": equity["initial_capital"],

            "final_capital": equity["final_capital"],

            "return": equity["return"],

            "max_drawdown": equity["max_drawdown"]

        }

        return report

    # =====================================================
    # PRINT REPORT
    # =====================================================

    @staticmethod
    def show(report):

        print()

        print("=" * 60)
        print("AI TRADER PERFORMANCE REPORT")
        print("=" * 60)

        print(f"Total Trade       : {report['total_trade']}")

        print(f"Open Trade        : {report['open_trade']}")

        print(f"Win               : {report['win']}")

        print(f"Loss              : {report['loss']}")

        print(f"Win Rate          : {report['win_rate']} %")

        print()

        print(f"Gross Profit      : {report['gross_profit']}")

        print(f"Gross Loss        : {report['gross_loss']}")

        print(f"Net Profit        : {report['net_profit']}")

        print(f"Profit Factor     : {report['profit_factor']}")

        print(f"Expectancy        : {report['expectancy']}")

        print()

        print(f"Initial Capital   : {report['initial_capital']:,.2f}")

        print(f"Final Capital     : {report['final_capital']:,.2f}")

        print(f"Return            : {report['return']} %")

        print(f"Max Drawdown      : {report['max_drawdown']} %")

        print("=" * 60)