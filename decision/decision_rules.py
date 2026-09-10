class DecisionRules:

    @staticmethod
    def evaluate(score):

        if score >= 95:
            return "STRONG BUY"

        elif score >= 80:
            return "BUY"

        elif score >= 60:
            return "BUY ON WEAKNESS"

        elif score >= 45:
            return "WATCH"

        elif score >= 25:
            return "WAIT"

        return "AVOID"