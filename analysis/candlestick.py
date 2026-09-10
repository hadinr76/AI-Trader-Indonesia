class Candlestick:

    @staticmethod
    def analyze(data):

        if len(data) < 2:
            return "Tidak diketahui"

        last = data.iloc[-1]
        prev = data.iloc[-2]

        open_price = float(last["Open"])
        close_price = float(last["Close"])
        high = float(last["High"])
        low = float(last["Low"])

        prev_open = float(prev["Open"])
        prev_close = float(prev["Close"])

        body = abs(close_price - open_price)
        candle_range = high - low

        upper_shadow = high - max(open_price, close_price)
        lower_shadow = min(open_price, close_price) - low

        # =====================
        # DOJI
        # =====================

        if candle_range > 0:

            if body / candle_range < 0.1:
                return "Doji"

        # =====================
        # HAMMER
        # =====================

        if (
            lower_shadow > body * 2
            and upper_shadow < body
        ):
            return "Hammer"

        # =====================
        # SHOOTING STAR
        # =====================

        if (
            upper_shadow > body * 2
            and lower_shadow < body
        ):
            return "Shooting Star"

        # =====================
        # BULLISH ENGULFING
        # =====================

        if (
            prev_close < prev_open
            and close_price > open_price
            and close_price > prev_open
            and open_price < prev_close
        ):
            return "Bullish Engulfing"

        # =====================
        # BEARISH ENGULFING
        # =====================

        if (
            prev_close > prev_open
            and close_price < open_price
            and open_price > prev_close
            and close_price < prev_open
        ):
            return "Bearish Engulfing"

        return "Tidak ada pola"