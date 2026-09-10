class ReportEngine:

    @staticmethod
    def show(scan_result):

        if not scan_result:

            print("Tidak ada data scanner.")
            return

        # ==========================================
        # SORT BY RANKING SCORE
        # ==========================================

        scan_result = sorted(

            scan_result,

            key=lambda x: x["ranking_score"],

            reverse=True

        )

        print()
        print("=" * 110)
        print("TOP 10 AI TRADER STOCK SCANNER")
        print("=" * 110)

        print(

            f"{'No':<4}"
            f"{'Code':<8}"
            f"{'Price':>8}"
            f"{'Overall':>10}"
            f"{'Decision':>10}"
            f"{'Conf':>8}"
            f"{'Rank':>10}"
            f"{'Rec':>22}"

        )

        print("-" * 110)

        for i, item in enumerate(scan_result[:10], start=1):

            print(

                f"{i:<4}"
                f"{item['code']:<8}"
                f"{item['price']:>8,.0f}"
                f"{item['overall_score']:>10}"
                f"{item['decision_score']:>10}"
                f"{item['confidence']:>8}%"
                f"{item['ranking_score']:>10.2f}"
                f"{item['recommendation']:>22}"

            )

        print()
        print("=" * 110)
        print("SUMMARY")
        print("=" * 110)

        summary = {

            "STRONG BUY":0,
            "BUY":0,
            "BUY ON WEAKNESS":0,
            "WATCH":0,
            "WAIT":0,
            "AVOID":0

        }

        for item in scan_result:

            rec = item["recommendation"]

            if rec in summary:

                summary[rec] += 1

        for key, value in summary.items():

            print(f"{key:<20}: {value}")

        print("=" * 110)