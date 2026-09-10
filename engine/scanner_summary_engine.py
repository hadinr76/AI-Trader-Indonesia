class ScannerSummaryEngine:

    @staticmethod
    def summarize(scan_result, report):

        total = len(scan_result)

        bullish = 0
        bearish = 0

        total_score = 0
        total_confidence = 0

        best_stock = None

        best_score = -1

        for stock in scan_result:

            if stock["trend"] == "Bullish":
                bullish += 1
            else:
                bearish += 1

            total_score += stock["overall_score"]

            total_confidence += stock["confidence"]

            if stock["ranking_score"] > best_score:

                best_score = stock["ranking_score"]

                best_stock = stock

        average_score = (
            total_score / total
            if total > 0
            else 0
        )

        average_confidence = (
            total_confidence / total
            if total > 0
            else 0
        )

        return {

            "total": total,

            "high_conviction":
                len(report["high_conviction"]),

            "watchlist":
                len(report["watchlist"]),

            "avoid":
                len(report["avoid"]),

            "bullish": bullish,

            "bearish": bearish,

            "average_score":
                round(average_score, 2),

            "average_confidence":
                round(average_confidence, 2),

            "best_stock":
                best_stock

        }