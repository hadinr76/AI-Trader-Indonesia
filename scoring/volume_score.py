class VolumeScore:

    @staticmethod
    def calculate(status):

        if status == "Very High":
            return 20

        elif status == "High":
            return 15

        elif status == "Normal":
            return 10

        return 0