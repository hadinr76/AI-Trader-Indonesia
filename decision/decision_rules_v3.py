class DecisionRulesV3:

    # ==========================================
    # TREND
    # ==========================================

    TREND = {

        "Strong Bullish": 20,
        "Bullish": 16,
        "Recovery": 10,
        "Sideways": 5,
        "Bearish": 0,
        "Strong Bearish": -10

    }

    # ==========================================
    # MARKET REGIME
    # ==========================================

    MARKET = {

        "BULL MARKET": 15,
        "RECOVERY": 10,
        "SIDEWAYS": 5,
        "BEAR MARKET": 0,
        "CRASH": -10

    }

    # ==========================================
    # MOMENTUM
    # ==========================================

    MOMENTUM = {

    "Strong Bullish": 15,

    "Bullish": 10,

    "Neutral": 5,

    "Weak": 2,

    "Bearish": -5

    }

    # ==========================================
    # MACD
    # ==========================================

    MACD = {

        "Bullish Cross": 10,
        "Bullish": 7,
        "Bearish Cross": -7,
        "Bearish": -10

    }

    # ==========================================
    # RSI
    # ==========================================

    @staticmethod
    def rsi_score(rsi):

        if 55 <= rsi <= 70:
            return 5

        elif 45 <= rsi < 55:
            return 3

        elif 70 < rsi <= 80:
            return 2

        return 0

    # ==========================================
    # CONFIDENCE
    # ==========================================

    @staticmethod
    def confidence_score(confidence):

        if confidence >= 80:
            return 5

        elif confidence >= 60:
            return 3

        elif confidence >= 40:
            return 2

        return 0

    # ==========================================
    # RISK REWARD
    # ==========================================

    @staticmethod
    def rr_score(rr):

        if rr >= 3:

            return 3

        elif rr >= 2:

            return 2

        elif rr >= 1.5:

            return 1

        return 0

    # ==========================================
    # FUNDAMENTAL
    # ==========================================

    @staticmethod
    def fundamental_score(score):

        if score >= 90:

            return 2

        elif score >= 80:

            return 1

        return 0