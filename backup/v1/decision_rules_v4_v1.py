class DecisionRulesV4:

    # ==========================================
    # TREND
    # ==========================================

    TREND = {

        "Strong Bullish": 20,
        "Bullish": 16,
        "Recovery": 10,
        "Sideways": 5,
        "Bearish": -5,
        "Strong Bearish": -10

    }

    # ==========================================
    # MARKET REGIME
    # ==========================================

    MARKET = {

        "BULL MARKET": 10,
        "RECOVERY": 8,
        "SIDEWAYS": 3,
        "BEAR MARKET": -5,
        "CRASH": -10

    }

    # ==========================================
    # MOMENTUM
    # ==========================================

    MOMENTUM = {

        "Strong Bullish": 10,
        "Bullish": 8,
        "Neutral": 4,
        "Weak": 0,
        "Bearish": -5

    }

    # ==========================================
    # MACD
    # ==========================================

    MACD = {

        "Bullish Cross": 8,
        "Bullish": 5,
        "Bearish Cross": -5,
        "Bearish": -8

    }

    # ==========================================
    # VOLUME
    # ==========================================

    VOLUME = {

        "Very High": 7,
        "High": 5,
        "Normal": 3,
        "Low": 0

    }

    # ==========================================
    # BREAKOUT
    # ==========================================

    BREAKOUT = {

        "Valid Breakout": 5,
        "Weak Breakout": 3,
        "Belum Breakout": 0

    }
    # ==========================================
    # RSI
    # ==========================================

    @staticmethod
    def rsi_score(rsi):

        if 55 <= rsi <= 70:
            return 8

        elif 45 <= rsi < 55:
            return 5

        elif 70 < rsi <= 80:
            return 4

        return 0

    # ==========================================
    # CONFIDENCE
    # ==========================================

    @staticmethod
    def confidence_score(score):

        if score >= 90:
            return 15

        elif score >= 80:
            return 12

        elif score >= 70:
            return 10

        elif score >= 60:
            return 8

        elif score >= 50:
            return 5

        return 0

    # ==========================================
    # FUNDAMENTAL
    # ==========================================

    @staticmethod
    def fundamental_score(score):

        if score >= 90:
            return 10

        elif score >= 80:
            return 8

        elif score >= 70:
            return 6

        elif score >= 60:
            return 4

        return 0

    # ==========================================
    # OVERALL
    # ==========================================

    @staticmethod
    def overall_score(score):

        if score >= 90:
            return 15

        elif score >= 80:
            return 12

        elif score >= 70:
            return 8

        elif score >= 60:
            return 5

        return 0

    # ==========================================
    # RANKING
    # ==========================================

    @staticmethod
    def ranking_score(score):

        if score >= 90:
            return 10

        elif score >= 80:
            return 8

        elif score >= 70:
            return 6

        elif score >= 60:
            return 4

        return 0

    # ==========================================
    # RISK REWARD
    # ==========================================

    @staticmethod
    def rr_score(rr):

        if rr >= 4:
            return 10

        elif rr >= 3:
            return 8

        elif rr >= 2:
            return 5

        elif rr >= 1.5:
            return 2

        return 0