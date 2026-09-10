class ScannerReportEngine:

    @staticmethod
    def classify(scan_result):

        high_conviction = []

        watchlist = []

        avoid = []

        for stock in scan_result:

            signal = stock["smart_signal"]

            confidence = stock["confidence"]

            rr = stock["rr2"]

            if (

                signal == "STRONG BUY"

                and confidence >= 80

                and rr >= 3

            ):

                high_conviction.append(stock)

            elif signal in [

                "BUY",

                "BUY ON WEAKNESS",

                "WATCH"

            ]:

                watchlist.append(stock)

            else:

                avoid.append(stock)

        return {

            "high_conviction": high_conviction,

            "watchlist": watchlist,

            "avoid": avoid

        }