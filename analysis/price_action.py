class PriceAction:

    @staticmethod
    def analyze(data):

        high = data["High"]
        low = data["Low"]

        last_high = float(high.iloc[-1])
        prev_high = float(high.iloc[-2])

        last_low = float(low.iloc[-1])
        prev_low = float(low.iloc[-2])

        if last_high > prev_high and last_low > prev_low:
            return "Higher High - Higher Low"

        elif last_high < prev_high and last_low < prev_low:
            return "Lower High - Lower Low"

        elif last_high > prev_high:
            return "Higher High"

        elif last_low > prev_low:
            return "Higher Low"

        elif last_high < prev_high:
            return "Lower High"

        elif last_low < prev_low:
            return "Lower Low"

        return "Sideways"