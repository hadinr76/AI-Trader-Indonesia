from openpyxl import Workbook
from openpyxl.styles import Font
from datetime import datetime
import os


class ExcelReport:

    @staticmethod
    def export(results):

        # ==========================================
        # OUTPUT FOLDER
        # ==========================================

        os.makedirs("output", exist_ok=True)

        filename = datetime.now().strftime(
            "output/AI_SCAN_%Y%m%d_%H%M%S.xlsx"
        )

        wb = Workbook()
        ws = wb.active

        ws.title = "AI Trader Scanner"

        # ==========================================
        # HEADER
        # ==========================================

        headers = [

            "Rank",
            "Code",
            "Price",
            "Trend",
            "Technical",
            "Fundamental",
            "Overall",
            "Decision",
            "Confidence",
            "Ranking",
            "Scanner",
            "Recommendation",
            "Smart Signal",
            "Market",
            "RR2"

        ]

        ws.append(headers)

        # Bold Header
        for cell in ws[1]:
            cell.font = Font(bold=True)

        # ==========================================
        # SORTING
        # ==========================================

        results = sorted(

            results,

            key=lambda x: x["ranking_score"],

            reverse=True

        )

        # ==========================================
        # DATA
        # ==========================================

        for rank, item in enumerate(results, start=1):

            ws.append([

                rank,

                item["code"],

                item["price"],

                item["trend"],

                item["technical_score"],

                item["fundamental_score"],

                item["overall_score"],

                item["decision_score"],

                item["confidence"],

                item["ranking_score"],

                item["scanner_score"],

                item["recommendation"],

                item["smart_signal"],

                item["market_regime"],

                item["rr2"]

            ])

        # ==========================================
        # AUTO WIDTH
        # ==========================================

        for column in ws.columns:

            length = max(

                len(str(cell.value))

                if cell.value is not None

                else 0

                for cell in column

            )

            ws.column_dimensions[
                column[0].column_letter
            ].width = length + 3

        wb.save(filename)

        print()
        print("=" * 70)
        print("EXCEL REPORT CREATED")
        print("=" * 70)
        print(filename)