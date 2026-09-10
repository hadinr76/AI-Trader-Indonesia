import csv
import os


class IndexClassifier:

    DEFAULT_FILE = "data/index_membership.csv"

    # =====================================================
    # LOAD MEMBERSHIP
    # =====================================================

    @classmethod
    def load_membership(
        cls,
        file_path=None
    ):

        if file_path is None:
            file_path = cls.DEFAULT_FILE

        if not os.path.exists(file_path):

            raise FileNotFoundError(
                f"File tidak ditemukan: {file_path}"
            )

        membership = {}

        with open(
            file_path,
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            reader = csv.DictReader(
                file
            )

            for row in reader:

                code = (
                    str(
                        row.get(
                            "code",
                            ""
                        )
                    )
                    .strip()
                    .upper()
                )

                index_name = (
                    str(
                        row.get(
                            "index",
                            ""
                        )
                    )
                    .strip()
                    .upper()
                )

                if not code:
                    continue

                if not index_name:
                    continue

                if code not in membership:

                    membership[code] = []

                if index_name not in membership[code]:

                    membership[code].append(
                        index_name
                    )

        return membership

    # =====================================================
    # GET INDEXES
    # =====================================================

    @classmethod
    def get_indexes(
        cls,
        code,
        file_path=None
    ):

        code = (
            str(code)
            .strip()
            .upper()
        )

        membership = (
            cls.load_membership(
                file_path
            )
        )

        return membership.get(
            code,
            []
        )

    # =====================================================
    # CHECK INDEX
    # =====================================================

    @classmethod
    def is_member(
        cls,
        code,
        index_name,
        file_path=None
    ):

        indexes = cls.get_indexes(
            code,
            file_path
        )

        index_name = (
            str(index_name)
            .strip()
            .upper()
        )

        return index_name in indexes

    # =====================================================
    # CLASSIFY
    # =====================================================

    @classmethod
    def classify(
        cls,
        code,
        file_path=None
    ):

        indexes = cls.get_indexes(
            code,
            file_path
        )

        if "LQ45" in indexes:

            category = "LQ45"

        elif "IDX30" in indexes:

            category = "IDX30"

        elif "IDX80" in indexes:

            category = "IDX80"

        else:

            category = "NON INDEX"

        return {

            "code":
                code.upper(),

            "indexes":
                indexes,

            "category":
                category

        }