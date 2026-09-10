class VolumeAnalysis:

    @staticmethod
    def analyze(data):

        volume = float(data["Volume"].iloc[-1])

        avg_volume = float(data["Volume"].tail(20).mean())

        if volume >= avg_volume * 2:
            return "Very High"

        elif volume >= avg_volume * 1.5:
            return "High"

        elif volume >= avg_volume:
            return "Normal"

        else:
            return "Low"