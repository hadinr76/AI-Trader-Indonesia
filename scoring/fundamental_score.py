class FundamentalScore:

    @staticmethod
    def calculate(fundamental):

        score = 0

        per = fundamental["per"]
        pbv = fundamental["pbv"]
        roe = fundamental["roe"]
        roa = fundamental["roa"]
        eps = fundamental["eps"]
        dividend = fundamental["dividend_yield"]

        # =====================
        # PER
        # =====================
        if per > 0:

            if per <= 15:
                score += 20

            elif per <= 25:
                score += 10

        # =====================
        # PBV
        # =====================
        if pbv > 0:

            if pbv <= 3:
                score += 20

            elif pbv <= 5:
                score += 10

        # =====================
        # ROE
        # =====================
        if roe >= 0.20:
            score += 25

        elif roe >= 0.15:
            score += 15

        elif roe >= 0.10:
            score += 10

        # =====================
        # ROA
        # =====================
        if roa >= 0.03:
            score += 15

        elif roa >= 0.02:
            score += 10

        # =====================
        # EPS
        # =====================
        if eps > 0:
            score += 10

        # =====================
        # DIVIDEND YIELD
        # =====================

        # Normalisasi:
        # 0.0565  -> 5.65%
        # 5.65    -> 5.65%

        if 0 < dividend < 1:
            dividend_pct = dividend * 100
        else:
            dividend_pct = dividend


        if dividend_pct >= 5:
            score += 10

        elif dividend_pct >= 2:
            score += 5

        return score