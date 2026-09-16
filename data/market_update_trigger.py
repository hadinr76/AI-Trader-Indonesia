import os
import requests


def trigger_market_update():

    url = os.environ.get("MARKET_UPDATE_URL")
    secret = os.environ.get("MARKET_UPDATE_SECRET")

    if not url:
        raise ValueError("MARKET_UPDATE_URL belum dikonfigurasi.")

    if not secret:
        raise ValueError("MARKET_UPDATE_SECRET belum dikonfigurasi.")

    response = requests.post(
        url,
        headers={
            "X-Update-Secret": secret
        },
        timeout=300
    )

    print("Status :", response.status_code)
    print("Response :", response.text)

    response.raise_for_status()


if __name__ == "__main__":
    trigger_market_update()