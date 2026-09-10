class PriceActionScore:

    @staticmethod
    def calculate(status):

        if status == "Higher High - Higher Low":
            return 20

        elif status == "Higher High":
            return 15

        elif status == "Higher Low":
            return 15

        elif status == "Sideways":
            return 10

        else:
            return 0