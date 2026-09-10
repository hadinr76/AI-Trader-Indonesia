import csv
import os

from database.lq45 import LQ45
from database.idx30 import IDX30


class IndexMembershipUpdater:

    OUTPUT_FILE = "data/index_membership.csv"

    # =====================================================
    # BUILD MEMBERSHIP
    # =====================================================

    @classmethod
    def build_membership(cls):

        rows = []

        seen = set()

        # =================================================
        # LQ45
        # =================================================

        for code in LQ45:

            code = (
                str(code)
                .strip()
                .upper()
            )

            if not code:
                continue

            key = (
                code,
                "LQ45"
            )

            if key in seen:
                continue

            seen.add(
                key
            )

            rows.append(
                {
                    "code": code,
                    "index": "LQ45"
                }
            )

        # =================================================
        # IDX30
        # =================================================

        for code in IDX30:

            code = (
                str(code)
                .strip()
                .upper()
            )

            if not code:
                continue

            key = (
                code,
                "IDX30"
            )

            if key in seen:
                continue

            seen.add(
                key
            )

            rows.append(
                {
                    "code": code,
                    "index": "IDX30"
                }
            )

        # =================================================
        # SORT
        # =================================================

        rows.sort(
            key=lambda item: (
                item["code"],
                item["index"]
            )
        )

        return rows

    # =====================================================
    # SAVE
    # =====================================================

    @classmethod
    def save(cls):

        rows = cls.build_membership()

        folder = os.path.dirname(
            cls.OUTPUT_FILE
        )

        if folder:

            os.makedirs(
                folder,
                exist_ok=True
            )

        with open(
            cls.OUTPUT_FILE,
            "w",
            encoding="utf-8",
            newline=""
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "code",
                    "index"
                ]
            )

            writer.writeheader()

            writer.writerows(
                rows
            )

        return rows


if __name__ == "__main__":

    print("=" * 70)
    print("UPDATE INDEX MEMBERSHIP")
    print("=" * 70)

    rows = (
        IndexMembershipUpdater
        .save()
    )

    lq45_count = len(
        {
            row["code"]
            for row in rows
            if row["index"] == "LQ45"
        }
    )

    idx30_count = len(
        {
            row["code"]
            for row in rows
            if row["index"] == "IDX30"
        }
    )

    print()
    print(
        "LQ45 unik :",
        lq45_count
    )

    print(
        "IDX30 unik:",
        idx30_count
    )

    print(
        "Total row :",
        len(rows)
    )

    print()
    print(
        "File:",
        IndexMembershipUpdater.OUTPUT_FILE
    )

    print()
    print("=" * 70)
    print("UPDATE INDEX MEMBERSHIP SELESAI")
    print("=" * 70)