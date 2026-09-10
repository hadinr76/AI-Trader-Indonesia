from data.market_data import MarketData


class DataManager:

    _cache = {}

    # =====================================
    # Daily
    # =====================================

    @classmethod
    def get_daily(cls, code):

        key = f"{code}_1d"

        if key not in cls._cache:

            market = MarketData()
            cls._cache[key] = market.get_data(
                kode=code,
                period="1y",
                interval="1d"
            )

        return cls._cache[key]

    # =====================================
    # Monthly
    # =====================================

    @classmethod
    def get_monthly(cls, code):

        key = f"{code}_1mo"

        if key not in cls._cache:

            market = MarketData()
            cls._cache[key] = market.get_data(
                kode=code,
                period="10y",
                interval="1mo"
            )

        return cls._cache[key]


    # =====================================
    # Weekly
    # =====================================

    @classmethod
    def get_weekly(cls, code):

        key = f"{code}_1wk"

        if key not in cls._cache:

            market = MarketData()
            cls._cache[key] = market.get_data(
                kode=code,
                period="1y",
                interval="1wk"
            )

        return cls._cache[key]

    # =====================================
    # 4 Hour
    # =====================================

    @classmethod
    def get_4h(cls, code):

        key = f"{code}_4h"

        if key not in cls._cache:

            market = MarketData()
            cls._cache[key] = market.get_data(
                kode=code,
                period="1y",
                interval="4h"
            )

        return cls._cache[key]

    # =====================================
    # 1 Hour
    # =====================================

    @classmethod
    def get_1h(cls, code):

        key = f"{code}_1h"

        if key not in cls._cache:

            market = MarketData()
            cls._cache[key] = market.get_data(
                kode=code,
                period="1y",
                interval="1h"
            )

        return cls._cache[key]

    # =====================================
    # Clear Cache
    # =====================================

    @classmethod
    def clear_cache(cls):

        cls._cache.clear()