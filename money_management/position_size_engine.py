class PositionSizeEngine:

    @staticmethod
    def calculate(

        capital,
        risk_percent,
        entry_price,
        stop_loss

    ):

        risk_money = capital * (risk_percent / 100)

        risk_per_share = entry_price - stop_loss

        if risk_per_share <= 0:

            return {

                "shares": 0,
                "lots": 0,
                "investment": 0,
                "risk_money": risk_money

            }

        shares = int(

            risk_money / risk_per_share

        )

        lots = shares // 100

        investment = lots * 100 * entry_price

        return {

            "shares": lots * 100,

            "lots": lots,

            "investment": investment,

            "risk_money": risk_money

        }