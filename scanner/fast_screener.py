import pandas as pd

from data.market_data import MarketData
from scanner.stock_universe_engine import StockUniverseEngine


class FastScreener:

    """
    FAST SCREENER V2

    Fungsi:

    1. Mengambil universe saham BEI
    2. Mengambil data market secara BULK
    3. Menghitung MA20
    4. Menghitung MA50
    5. Menghitung Average Volume 20
    6. Menghitung Relative Volume
    7. Membandingkan harga dengan MA20
    8. Membandingkan harga dengan MA50
    9. Membandingkan MA20 dengan MA50
    10. Membandingkan volume dengan average volume
    11. Menentukan PASS / FAIL

    Fast Screener TIDAK melakukan:

    - RSI
    - MACD
    - AI analysis
    - fundamental analysis
    - broker summary
    - breakout analysis
    - support / resistance
    - entry
    - stop loss
    - take profit

    Tujuannya hanya:

    981 saham
        ↓
    Fast Filter
        ↓
    kandidat teknikal
    """

    # =====================================================
    # INITIALIZE
    # =====================================================

    def __init__(
        self,
        stocks=None,
        period="1y"
    ):

        self.market = MarketData()

        self.period = period

        if stocks is None:

            self.stocks = (
                StockUniverseEngine
                .get_all_stocks()
            )

        else:

            self.stocks = stocks

    # =====================================================
    # ANALYZE ONE STOCK
    # =====================================================

    @staticmethod
    def analyze_stock(
        code,
        data
    ):

        try:

            # =============================================
            # VALIDASI DATA
            # =============================================

            if data is None:

                return None

            if data.empty:

                return None

            # =============================================
            # DATA MINIMUM
            # =============================================

            if len(data) < 50:

                return None

            # =============================================
            # NORMALISASI
            # =============================================

            close = (
                data["Close"]
                .astype(float)
            )

            volume = (
                data["Volume"]
                .astype(float)
            )

            # =============================================
            # VALIDASI NILAI
            # =============================================

            if close.dropna().empty:

                return None

            if volume.dropna().empty:

                return None

            # =============================================
            # MOVING AVERAGE
            # =============================================

            ma20 = (
                close
                .rolling(
                    window=20
                )
                .mean()
            )

            ma50 = (
                close
                .rolling(
                    window=50
                )
                .mean()
            )

            # =============================================
            # AVERAGE VOLUME
            # =============================================

            average_volume_20 = (
                volume
                .rolling(
                    window=20
                )
                .mean()
            )

            # =============================================
            # AVERAGE TRANSACTION VALUE 20D
            # =============================================

            transaction_value = (
                close * volume
            )

            average_transaction_value_20 = (
                transaction_value
                .rolling(
                    window=20
                )
                .mean()
            )

            # =============================================
            # NILAI TERAKHIR
            # =============================================

            price = float(
                close.iloc[-1]
            )

            previous_price = float(
                close.iloc[-2]
            )

            change_percent = (
                (price - previous_price)
                / previous_price
            ) * 100

            current_ma20 = float(
                ma20.iloc[-1]
            )

            current_ma50 = float(
                ma50.iloc[-1]
            )

            current_volume = float(
                volume.iloc[-1]
            )

            current_average_volume = float(
                average_volume_20.iloc[-1]
            )

            current_average_transaction_value = float(
                average_transaction_value_20.iloc[-1]
            )

            # =============================================
            # LIQUIDITY CLASSIFICATION
            # Berdasarkan rata-rata nilai transaksi 20 hari
            # =============================================

            if current_average_transaction_value >= 100_000_000_000:

                liquidity_status = "VERY LIQUID"

            elif current_average_transaction_value >= 20_000_000_000:

                liquidity_status = "LIQUID"

            elif current_average_transaction_value >= 5_000_000_000:

                liquidity_status = "MODERATE"

            elif current_average_transaction_value >= 1_000_000_000:

                liquidity_status = "LOW LIQUIDITY"

            else:

                liquidity_status = "ILLIQUID"

            # =============================================
            # VALIDASI NaN
            # =============================================

            values = [

                price,

                current_ma20,

                current_ma50,

                current_volume,

                current_average_volume,

                current_average_transaction_value

            ]

            if any(
                pd.isna(value)
                for value in values
            ):

                return None

            # =============================================
            # RELATIVE VOLUME
            # =============================================

            if current_average_volume <= 0:

                relative_volume = 0.0

            else:

                relative_volume = (
                    current_volume /
                    current_average_volume
                )

            # =============================================
            # FILTER
            # =============================================

            price_above_ma20 = (

                price >
                current_ma20

            )

            price_above_ma50 = (

                price >
                current_ma50

            )

            ma20_above_ma50 = (

                current_ma20 >
                current_ma50

            )

            # =============================================
            # EARLY TREND / NEAR GOLDEN CROSS
            # =============================================

            distance_price_ma20 = (
                ((price - current_ma20) / current_ma20)
                * 100
            )

            distance_ma20_ma50 = (
                ((current_ma20 - current_ma50) / current_ma50)
                * 100
            )

            golden_cross_age = None

            lookback_days = min(
                20,
                len(ma20)
            )

            for i in range(1, lookback_days + 1):

                current_index = -i
                previous_index = -(i + 1)

                if abs(previous_index) > len(ma20):
                    break

                ma20_now = ma20.iloc[current_index]
                ma50_now = ma50.iloc[current_index]

                ma20_prev = ma20.iloc[previous_index]
                ma50_prev = ma50.iloc[previous_index]

                if (
                    pd.notna(ma20_now)
                    and pd.notna(ma50_now)
                    and pd.notna(ma20_prev)
                    and pd.notna(ma50_prev)
                ):

                    if (
                        ma20_now > ma50_now
                        and ma20_prev <= ma50_prev
                    ):

                        golden_cross_age = i - 1
                        break

            near_golden_cross = (
                abs(distance_ma20_ma50) <= 3
            )

            fresh_golden_cross = (
                golden_cross_age is not None
                and golden_cross_age <= 10
            )

            price_near_ma20 = (
                0 <= distance_price_ma20 <= 5
            )

            early_trend = (
                price_near_ma20
                and (
                    near_golden_cross
                    or fresh_golden_cross
                )
            )

            volume_above_average = (

                current_volume >
                current_average_volume

            )

            # =============================================
            # JUMLAH FILTER
            # =============================================

            passed_filters = 0

            if price_above_ma20:

                passed_filters += 1

            if price_above_ma50:

                passed_filters += 1

            if ma20_above_ma50:

                passed_filters += 1

            if volume_above_average:

                passed_filters += 1

            # =============================================
            # STATUS
            # =============================================

            if passed_filters >= 3:

                status = "PASS"

            else:

                status = "FAIL"

            # =============================================
            # RETURN
            # =============================================

            return {

                "code":
                    code,

                "price":
                    round(
                        price,
                        2
                    ),

                "change_percent":
                    round(
                        change_percent,
                        2
                    ),

                "ma20":
                    round(
                        current_ma20,
                        2
                    ),

                "ma50":
                    round(
                        current_ma50,
                        2
                    ),

                "volume":
                    int(
                        current_volume
                    ),

                "current_transaction_value":
                    round(
                        price * current_volume,
                        2
                    ),

                "average_volume_20":
                    int(
                        current_average_volume
                    ),

                "average_transaction_value_20":
                    round(
                        current_average_transaction_value,
                        2
                    ),

                "liquidity_status":
                    liquidity_status,

                "relative_volume":
                    round(
                        relative_volume,
                        2
                    ),

                "price_above_ma20":
                    price_above_ma20,

                "price_above_ma50":
                    price_above_ma50,

                "ma20_above_ma50":
                    ma20_above_ma50,

                "distance_price_ma20":
                    round(
                        distance_price_ma20,
                        2
                    ),

                "distance_ma20_ma50":
                    round(
                        distance_ma20_ma50,
                        2
                    ),

                "golden_cross_age":
                    golden_cross_age,

                "near_golden_cross":
                    near_golden_cross,

                "fresh_golden_cross":
                    fresh_golden_cross,

                "early_trend":
                    early_trend,

                "volume_above_average":
                    volume_above_average,

                "passed_filters":
                    passed_filters,

                "status":
                    status

            }

        except Exception as e:

            print(
                f"Gagal screening "
                f"{code}: {e}"
            )

            return None

    # =====================================================
    # SCAN ALL STOCKS
    # =====================================================

    def scan(self):

        results = []

        print()
        print("=" * 70)
        print("FAST STOCK SCREENER V2")
        print("=" * 70)

        print()

        print(
            "Jumlah universe :",
            len(self.stocks)
        )

        print()

        # =============================================
        # BULK DOWNLOAD
        # =============================================

        print(
            "Mengambil market data..."
        )

        market_data = (
            self.market.get_bulk_daily(
                self.stocks,
                period=self.period
            )
        )

        print()

        print(
            "Data berhasil :",
            len(market_data)
        )

        print()

        # =============================================
        # SCREENING
        # =============================================

        for code in self.stocks:

            data = market_data.get(
                code
            )

            result = (
                self.analyze_stock(
                    code,
                    data
                )
            )

            if result is None:

                continue

            results.append(
                result
            )

        # =============================================
        # SORTING
        # =============================================

        results.sort(

            key=lambda x: (

                x["passed_filters"],

                x["relative_volume"],

                x["price_above_ma20"],

                x["price_above_ma50"],

                x["ma20_above_ma50"],

                x["volume_above_average"]

            ),

            reverse=True

        )

        return results

    # =====================================================
    # ONLY PASS
    # =====================================================

    @staticmethod
    def passed_stocks(
        results
    ):

        return [

            result

            for result in results

            if result["status"] == "PASS"

        ]

    # =====================================================
    # PRINT RESULTS
    # =====================================================

    @staticmethod
    def print_results(
        results
    ):

        print()
        print("=" * 70)
        print("FAST SCREENER RESULT")
        print("=" * 70)

        if not results:

            print()

            print(
                "Tidak ada data "
                "yang berhasil dianalisis."
            )

            return

        print()

        for index, result in enumerate(

            results,

            start=1

        ):

            print(

                f"{index:3}. "

                f"{result['code']:<6} "

                f"Price: "
                f"{result['price']:<9} "

                f"MA20: "
                f"{result['ma20']:<9} "

                f"MA50: "
                f"{result['ma50']:<9} "

                f"RVOL: "
                f"{result['relative_volume']:<5} "

                f"Pass: "
                f"{result['passed_filters']}/4 "

                f"{result['status']}"

            )

    # =====================================================
    # PRINT PASS ONLY
    # =====================================================

    @staticmethod
    def print_passed(
        results
    ):

        passed = (
            FastScreener
            .passed_stocks(
                results
            )
        )

        print()
        print("=" * 70)
        print("SAHAM LOLOS FAST SCREENING")
        print("=" * 70)

        if not passed:

            print()

            print(
                "Tidak ada saham "
                "yang memenuhi "
                "minimal 3 dari 4 filter."
            )

            return

        print()

        for index, result in enumerate(

            passed,

            start=1

        ):

            print(

                f"{index:3}. "

                f"{result['code']:<6} "

                f"Price: "
                f"{result['price']:<9} "

                f"MA20: "
                f"{result['ma20']:<9} "

                f"MA50: "
                f"{result['ma50']:<9} "

                f"RVOL: "
                f"{result['relative_volume']:<5} "

                f"Pass: "
                f"{result['passed_filters']}/4"

            )

        print()

        print(
            "Total PASS :",
            len(passed)
        )