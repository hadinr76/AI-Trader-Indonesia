import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)
# import streamlit as st
import csv
import json
import time
import pandas as pd
from pathlib import Path
import yfinance as yf
from flask import Flask, render_template, redirect, url_for, request

from scanner.daily_recommendation import DailyRecommendation
from scanner.stock_universe_engine import StockUniverseEngine
from data.market_data import MarketData


app = Flask(__name__)

# =====================================================
# MARKET TICKER
# =====================================================

MARKET_TICKERS = {
    "IHSG": "^JKSE",
}

MOST_ACTIVE_CACHE = Path(
    "data/web_cache/latest_most_active.json"
)

def get_most_active_tickers():

    if not MOST_ACTIVE_CACHE.exists():
        return []

    try:

        with open(
            MOST_ACTIVE_CACHE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return data

    except Exception as error:

        print(
            f"Most Active cache error: {error}"
        )

        return []


def get_market_ticker():

    ticker_data = []

    for code, symbol in MARKET_TICKERS.items():

        try:

            data = yf.download(
                symbol,
                period="5d",
                interval="1d",
                auto_adjust=False,
                progress=False
            )

            if data.empty:
                continue

            close = data["Close"].squeeze().dropna()

            if len(close) < 2:
                continue

            current_price = float(close.iloc[-1])
            previous_price = float(close.iloc[-2])

            change = current_price - previous_price

            change_percent = (
                change / previous_price
            ) * 100

            ticker_data.append({
                "code": code,
                "price": current_price,
                "change": change,
                "change_percent": change_percent,
            })

        except Exception as error:

            print(
                f"Ticker error {code}: {error}"
            )

    return ticker_data

STOCK_NAME_FILE = Path(
    "data/idx_stocks.csv"
)

@app.template_filter("rupiah")
def rupiah(value):

    try:
        number = float(value)

        return (
            f"Rp{number:,.0f}"
            .replace(",", ".")
        )

    except (TypeError, ValueError):
        return "-"


def load_stock_names():

    stock_names = {}

    if not STOCK_NAME_FILE.exists():
        return stock_names

    with open(
        STOCK_NAME_FILE,
        "r",
        encoding="utf-8-sig"
    ) as file:

        reader = csv.reader(file)

        for row in reader:

            if len(row) < 2:
                continue

            code = row[0].strip().upper()
            company_name = row[1].strip()

            stock_names[code] = company_name

    return stock_names


STOCK_NAMES = load_stock_names()


# Menyimpan hasil screening terakhir

CACHE_FILE = Path(
    "data/web_cache/latest_screening.json"
)

if CACHE_FILE.exists():

    with open(
        CACHE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        scan_results = json.load(file)

else:

    scan_results = []


@app.route("/")
def dashboard():

    search_query = (
        request.args.get(
            "q",
            ""
        )
        .strip()
        .upper()
    )

    search_result = None
    search_found = False

    for stock in scan_results:

        stock["company_name"] = (
            STOCK_NAMES.get(
                stock.get("code", "").upper(),
                stock.get("code", "")
            )
        )

        if search_query:

            search_result = next(
                (
                    stock
                    for stock in scan_results
                    if stock.get(
                        "code",
                        ""
                    ).upper() == search_query
                ),
                None
            )

            search_found = (
                search_result is not None
            )

    top_opportunities = scan_results[:10]

    buy_now = [
        stock
        for stock in scan_results
        if stock.get("recommendation") == "BUY"
    ]

    breakout_buy = [
        stock
        for stock in scan_results
        if stock.get("recommendation") == "BREAKOUT BUY"
    ]

    buy_on_weakness = [
        stock
        for stock in scan_results
        if stock.get("recommendation") == "BUY ON WEAKNESS"
    ]

    near_buy = [
        stock
        for stock in scan_results
        if stock.get("watchlist_status") == "NEAR BUY"
    ]

    early_trend = [
        stock
        for stock in scan_results
        if stock.get("early_trend") is True
    ]

    market_ticker = get_market_ticker()

    ihsg = next(
        (
            item
            for item in market_ticker
            if item["code"] == "IHSG"
        ),
        None
    )

    stock_tickers = (
        get_most_active_tickers()
    )

    return render_template(
        "dashboard.html",
        stocks=top_opportunities,
        top_opportunities=top_opportunities,
        buy_now=buy_now,
        breakout_buy=breakout_buy,
        buy_on_weakness=buy_on_weakness,
        near_buy=near_buy,
        early_trend=early_trend,
        ihsg=ihsg,
        stock_tickers=stock_tickers,
        search_query=search_query,
        search_result=search_result,
        search_found=search_found,
    )

@app.route("/search")
def search_stock():

    code = (
        request.args.get(
            "q",
            ""
        )
        .strip()
        .upper()
    )

    if not code:
        return redirect(
            url_for("dashboard")
        )

    return redirect(
        url_for(
            "stock_detail",
            code=code
        )
    )

@app.route("/stock/<code>")
def stock_detail(code):

    code = code.strip().upper()

    # =============================================
    # VALIDASI KODE SAHAM BEI
    # =============================================

    stock_universe = (
        StockUniverseEngine
        .get_all_stocks()
    )

    if code not in stock_universe:

        return (
            f"Kode saham {code} "
            f"tidak terdaftar di universe BEI."
        ), 404

    # =============================================
    # 1. CARI DI CACHE SCREENING
    # =============================================

    stock = next(
        (
            item
            for item in scan_results
            if item.get(
                "code",
                ""
            ).upper() == code
        ),
        None
    )

    source = "SCREENING"

    # =============================================
    # 2. JIKA TIDAK ADA, ANALISIS SATU SAHAM
    # =============================================

    if (
        stock is None
        or "opportunity_score" not in stock
    ):

        print()
        print("=" * 70)
        print(
            "SINGLE STOCK ANALYSIS :",
            code
        )
        print("=" * 70)

        try:

            engine = DailyRecommendation()

            stock = (
                engine.analyze_single_stock(
                    code
                )
            )

            source = "SINGLE ANALYSIS"

        except Exception as error:

            print(
                f"Single analysis {code} gagal: "
                f"{error}"
            )

            stock = None

    # =============================================
    # 3. TIDAK DITEMUKAN / ANALISIS GAGAL
    # =============================================

    if stock is None:

        return (
            f"Saham {code} tidak ditemukan "
            f"atau data tidak cukup untuk dianalisis."
        )

    # =============================================
    # 4. COMPANY NAME
    # =============================================

    stock["company_name"] = (
        STOCK_NAMES.get(
            code,
            code
        )
    )

    # =============================================
    # 5. TRADING CHART DATA
    # =============================================

    chart_data = []

    try:

        market = MarketData()

        chart_df = market.get_daily(
            code,
            period="6mo"
        ).copy()

        # =============================================
        # MOVING AVERAGE
        # Hitung sebelum mengambil 60 candle terakhir
        # =============================================

        chart_df["MA20"] = (
            chart_df["Close"]
            .rolling(window=20)
            .mean()
        )

        chart_df["MA50"] = (
            chart_df["Close"]
            .rolling(window=50)
            .mean()
        )

        # =============================================
        # TAMPILKAN 60 CANDLE TERAKHIR
        # =============================================

        chart_df = chart_df.tail(60)

        for date, row in chart_df.iterrows():

            chart_data.append({

                "time":
                    date.strftime(
                        "%Y-%m-%d"
                    ),

                "open":
                    float(row["Open"]),

                "high":
                    float(row["High"]),

                "low":
                    float(row["Low"]),

                "close":
                    float(row["Close"]),

                "volume":
                    float(row["Volume"]),

                "ma20":
                    (
                        float(row["MA20"])
                        if pd.notna(
                            row["MA20"]
                        )
                        else None
                    ),

                "ma50":
                    (
                        float(row["MA50"])
                        if pd.notna(
                            row["MA50"]
                        )
                        else None
                    )
            })

    except Exception as error:

        print(
            f"Chart data {code} gagal: "
            f"{error}"
        )

        chart_data = []

    # =============================================
    # 6. TAMPILKAN DETAIL
    # =============================================

    return render_template(
        "stock_detail.html",
        stock=stock,
        source=source,
        chart_data=chart_data
    )
@app.route("/scan")
def scan():

    global scan_results

    start_time = time.time()

    print()
    print("=" * 70)
    print("WEB DASHBOARD - MENJALANKAN SCREENING")
    print("=" * 70)

    engine = DailyRecommendation(
        period="1y",
        technical_limit=20
    )

    results = engine.run()

    # Urutkan berdasarkan Opportunity Score
    scan_results = sorted(
        results,
        key=lambda x: x.get(
            "opportunity_score",
            0
        ),
        reverse=True
    )

    with open(
        CACHE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            scan_results,
            file,
            indent=4,
            ensure_ascii=False,
            default=str
        )

    elapsed = time.time() - start_time

    print()
    print(
        f"SCREENING SELESAI DALAM "
        f"{elapsed:.2f} DETIK"
    )

    return redirect(
        url_for("dashboard")
    )


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )