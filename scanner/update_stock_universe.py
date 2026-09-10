import csv
import os
import re
import requests
from bs4 import BeautifulSoup


class StockUniverseUpdater:

    """
    Mengambil universe saham dari halaman KSEI
    dan menyimpannya ke:

        data/idx_stocks.csv

    Format:

        code,name
    """

    KSEI_URL = (
        "https://web.ksei.co.id/services/"
        "registered-securities/shares"
        "?setLocale=id-ID"
    )

    OUTPUT_FILE = "data/idx_stocks.csv"

    # =====================================================
    # REQUEST
    # =====================================================

    @classmethod
    def download_page(cls):

        headers = {

            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/151.0 Safari/537.36"
            ),

            "Accept": (
                "text/html,"
                "application/xhtml+xml,"
                "application/xml;q=0.9,"
                "*/*;q=0.8"
            ),

            "Accept-Language": (
                "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
            ),

        }

        response = requests.get(
            cls.KSEI_URL,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        return response.text

    # =====================================================
    # EXTRACT USING TABLE
    # =====================================================

    @classmethod
    def extract_from_table(
        cls,
        soup
    ):

        stocks = []

        # -------------------------------------------------
        # SEMUA TABLE
        # -------------------------------------------------

        tables = soup.find_all(
            "table"
        )

        for table in tables:

            rows = table.find_all(
                "tr"
            )

            for row in rows:

                cells = row.find_all(
                    ["td", "th"]
                )

                if len(cells) < 2:

                    continue

                values = []

                for cell in cells:

                    text = cell.get_text(
                        " ",
                        strip=True
                    )

                    values.append(
                        text
                    )

                code = (
                    values[0]
                    .strip()
                    .upper()
                )

                name = (
                    values[1]
                    .strip()
                )

                # -------------------------------------------------
                # VALIDASI KODE
                # -------------------------------------------------

                if not re.fullmatch(
                    r"[A-Z]{2,5}",
                    code
                ):

                    continue

                if code in (
                    "KODE",
                    "CODE"
                ):

                    continue

                if not name:

                    continue

                stocks.append(
                    {
                        "code": code,
                        "name": name
                    }
                )

        return stocks

    # =====================================================
    # EXTRACT FROM PAGE TEXT
    # =====================================================

    @classmethod
    def extract_from_text(
        cls,
        soup
    ):

        stocks = []

        text = soup.get_text(
            "\n",
            strip=True
        )

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        # -------------------------------------------------
        # POLA:
        #
        # AADI
        # ADARO ANDALAN INDONESIA Tbk
        #
        # atau:
        #
        # 1
        # AADI
        # ADARO ANDALAN INDONESIA Tbk
        #
        # -------------------------------------------------

        for index, line in enumerate(
            lines
        ):

            code_match = re.fullmatch(
                r"[A-Z]{2,5}",
                line
            )

            if not code_match:

                continue

            code = line.upper()

            # -------------------------------------------------
            # HEADER
            # -------------------------------------------------

            if code in (
                "KODE",
                "CODE"
            ):

                continue

            # -------------------------------------------------
            # CARI NAMA SETELAH KODE
            # -------------------------------------------------

            name = None

            for offset in range(
                1,
                5
            ):

                position = (
                    index + offset
                )

                if position >= len(
                    lines
                ):

                    break

                candidate = (
                    lines[position]
                    .strip()
                )

                if not candidate:

                    continue

                # -------------------------------------------------
                # JANGAN AMBIL KODE BERIKUTNYA
                # -------------------------------------------------

                if re.fullmatch(
                    r"[A-Z]{2,5}",
                    candidate
                ):

                    continue

                # -------------------------------------------------
                # JANGAN AMBIL NOMOR
                # -------------------------------------------------

                if re.fullmatch(
                    r"\d+",
                    candidate
                ):

                    continue

                # -------------------------------------------------
                # NAMA EMITEN UMUMNYA
                # MENGANDUNG Tbk
                # -------------------------------------------------

                if (
                    "Tbk" in candidate
                    or
                    "TBK" in candidate
                ):

                    name = candidate

                    break

            if name is None:

                continue

            stocks.append(
                {
                    "code": code,
                    "name": name
                }
            )

        return stocks

    # =====================================================
    # EXTRACT
    # =====================================================

    @classmethod
    def extract_stocks(
        cls,
        html
    ):

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        # -------------------------------------------------
        # METHOD 1
        # TABLE
        # -------------------------------------------------

        stocks = cls.extract_from_table(
            soup
        )

        print(
            "Ticker dari table :",
            len(stocks)
        )

        # -------------------------------------------------
        # METHOD 2
        # TEXT FALLBACK
        # -------------------------------------------------

        if len(stocks) < 500:

            text_stocks = (
                cls.extract_from_text(
                    soup
                )
            )

            print(
                "Ticker dari text  :",
                len(text_stocks)
            )

            if len(text_stocks) > len(
                stocks
            ):

                stocks = text_stocks

        # -------------------------------------------------
        # REMOVE DUPLICATES
        # -------------------------------------------------

        unique = {}

        for stock in stocks:

            code = (
                stock["code"]
                .strip()
                .upper()
            )

            name = (
                stock["name"]
                .strip()
            )

            if code not in unique:

                unique[code] = {
                    "code": code,
                    "name": name
                }

        stocks = list(
            unique.values()
        )

        # -------------------------------------------------
        # SORT
        # -------------------------------------------------

        stocks.sort(
            key=lambda item:
            item["code"]
        )

        return stocks

    # =====================================================
    # SAVE CSV
    # =====================================================

    @classmethod
    def save_csv(
        cls,
        stocks,
        output_file=None
    ):

        if output_file is None:

            output_file = (
                cls.OUTPUT_FILE
            )

        folder = os.path.dirname(
            output_file
        )

        if folder:

            os.makedirs(
                folder,
                exist_ok=True
            )

        with open(
            output_file,
            "w",
            encoding="utf-8",
            newline=""
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "code",
                    "name"
                ]
            )

            writer.writeheader()

            writer.writerows(
                stocks
            )

        return output_file

    # =====================================================
    # UPDATE
    # =====================================================

    @classmethod
    def update(cls):

        print("=" * 70)
        print(
            "UPDATE IDX STOCK UNIVERSE"
        )
        print("=" * 70)

        print()
        print(
            "Mengambil data saham dari KSEI..."
        )

        html = cls.download_page()

        print(
            "Download berhasil."
        )

        print()
        print(
            "Ukuran HTML :",
            len(html),
            "bytes"
        )

        print()
        print(
            "Membaca daftar saham..."
        )

        stocks = cls.extract_stocks(
            html
        )

        print()
        print(
            "Jumlah ticker ditemukan:",
            len(stocks)
        )

        # -------------------------------------------------
        # SAFETY CHECK
        # -------------------------------------------------

        if len(stocks) < 500:

            raise RuntimeError(
                "Jumlah ticker terlalu sedikit "
                f"({len(stocks)}). "
                "File CSV TIDAK ditimpa."
            )

        # -------------------------------------------------
        # SAVE
        # -------------------------------------------------

        output = cls.save_csv(
            stocks
        )

        print()
        print(
            "Universe berhasil disimpan:"
        )

        print(
            output
        )

        # -------------------------------------------------
        # SAMPLE
        # -------------------------------------------------

        print()
        print(
            "20 TICKER PERTAMA"
        )

        print("-" * 70)

        for index, stock in enumerate(
            stocks[:20],
            start=1
        ):

            print(
                f"{index:3}. "
                f"{stock['code']:<6} "
                f"{stock['name']}"
            )

        print()
        print(
            "20 TICKER TERAKHIR"
        )

        print("-" * 70)

        start = max(
            1,
            len(stocks) - 19
        )

        for index, stock in enumerate(
            stocks[-20:],
            start=start
        ):

            print(
                f"{index:3}. "
                f"{stock['code']:<6} "
                f"{stock['name']}"
            )

        print()
        print("=" * 70)
        print(
            "UPDATE UNIVERSE SELESAI"
        )
        print("=" * 70)


if __name__ == "__main__":

    StockUniverseUpdater.update()