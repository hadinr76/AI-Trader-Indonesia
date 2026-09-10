class Rating:

    @staticmethod
    def calculate(overall_score):

        if overall_score >= 95:
            return {
                "stars": "★★★★★",
                "category": "STRONG BUY"
            }

        elif overall_score >= 80:
            return {
                "stars": "★★★★☆",
                "category": "BUY"
            }

        elif overall_score >= 65:
            return {
                "stars": "★★★☆☆",
                "category": "BUY ON WEAKNESS"
            }

        elif overall_score >= 50:
            return {
                "stars": "★★☆☆☆",
                "category": "WATCH"
            }

        else:
            return {
                "stars": "★☆☆☆☆",
                "category": "AVOID"
            }