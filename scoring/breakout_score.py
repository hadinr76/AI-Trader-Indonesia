class BreakoutScore:

    @staticmethod
    def calculate(status):

        if status == "Valid Breakout":
            return 20

        elif status == "Weak Breakout":
            return 10

        return 0