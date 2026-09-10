class OverallScore:

    @staticmethod
    def calculate(technical_score, fundamental_score):

        # Bobot penilaian
        technical_weight = 0.6
        fundamental_weight = 0.4

        overall = (
            technical_score * technical_weight +
            fundamental_score * fundamental_weight
        )

        return round(overall)