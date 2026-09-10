class BreakoutAnalysis:

    @staticmethod
    def analyze(data, resistance, volume_status):

        harga = float(data["Close"].iloc[-1])

        if harga > resistance:

            if volume_status in ["High", "Very High"]:
                return "Valid Breakout"

            return "Weak Breakout"

        return "Belum Breakout"