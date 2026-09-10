class CandlestickScore:

    @staticmethod
    def calculate(pattern):

        score = 0

        if pattern == "Bullish Engulfing":
            score = 10

        elif pattern == "Hammer":
            score = 8

        elif pattern == "Morning Star":
            score = 10

        elif pattern == "Three White Soldiers":
            score = 12

        elif pattern == "Doji":
            score = -3

        elif pattern == "Shooting Star":
            score = -8

        elif pattern == "Bearish Engulfing":
            score = -10

        else:
            score = 0

        return score