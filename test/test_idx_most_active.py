import requests


URL = (
    "https://www.idx.co.id/id/data-pasar/"
    "laporan-statistik/digital-statistic/"
)


def test_idx_connection():

    print("=" * 70)
    print("TEST KONEKSI DATA BEI")
    print("=" * 70)

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    }

    try:

        response = requests.get(
            URL,
            headers=headers,
            timeout=20
        )

        print()
        print("Status Code :", response.status_code)
        print("Content Type:", response.headers.get("content-type"))
        print("Ukuran Data :", len(response.content), "bytes")

        if response.status_code == 200:

            print()
            print("KONEKSI BEI BERHASIL")

            text = response.text.lower()

            if "most active" in text:
                print("Most Active ditemukan di halaman.")
            else:
                print(
                    "Most Active belum ditemukan "
                    "langsung pada HTML."
                )

        else:

            print()
            print("KONEKSI BEI GAGAL")

    except Exception as error:

        print()
        print("ERROR:")
        print(error)


if __name__ == "__main__":
    test_idx_connection()