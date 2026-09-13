class TradeSetupScore:

    @staticmethod
    def calculate(
        trade_status=None,
        trade_quality=None,
        demand_zone_low=None,
        supply_status=None,
        supply_warning=None,
        breakout_retest_status=None,
        volume_confirmation_status=None,
        volume_score=0,
        confluence_score=0
    ):

        score = 0
        reasons = []

        # ==========================================
        # TRADE AREA
        # ==========================================

        if trade_status == "IN BUY AREA":
            score += 20
            reasons.append("Harga berada di buy area")

        elif trade_status == "WAIT PULLBACK":
            score += 10
            reasons.append("Menunggu pullback ke buy area")

        # ==========================================
        # TRADE QUALITY
        # ==========================================

        if trade_quality == "SANGAT BAGUS":
            score += 20
            reasons.append("Kualitas trade sangat bagus")

        elif trade_quality == "BAGUS":
            score += 15
            reasons.append("Kualitas trade bagus")

        elif trade_quality == "CUKUP":
            score += 8
            reasons.append("Kualitas trade cukup")

        # ==========================================
        # DEMAND ZONE
        # ==========================================

        if demand_zone_low is not None:
            score += 10
            reasons.append("Didukung demand zone")

        # ==========================================
        # SUPPLY ZONE
        # ==========================================

        if supply_status == "BELOW SUPPLY":
            score += 10
            reasons.append("Harga masih di bawah supply")

        elif supply_status == "IN SUPPLY":
            score -= 15
            reasons.append("Harga berada di area supply")

        if supply_warning == "SUPPLY BEFORE TP1":
            score -= 10
            reasons.append("Supply berada sebelum target 1")

        elif supply_warning == "SUPPLY BEFORE TP2":
            score -= 5
            reasons.append("Supply berada sebelum target 2")

        # ==========================================
        # BREAKOUT RETEST
        # ==========================================

        if breakout_retest_status == "VALID RETEST":
            score += 15
            reasons.append("Breakout retest valid")

        elif breakout_retest_status == "FAILED RETEST":
            score -= 10
            reasons.append("Breakout retest gagal")

        # ==========================================
        # VOLUME CONFIRMATION
        # ==========================================

        if volume_confirmation_status == "VERY STRONG":
            score += 15
            reasons.append("Volume sangat kuat")

        elif volume_confirmation_status == "CONFIRMED":
            score += 12
            reasons.append("Volume terkonfirmasi")

        elif volume_confirmation_status == "MODERATE":
            score += 6
            reasons.append("Volume moderat")

        elif volume_confirmation_status == "WEAK":
            score -= 5
            reasons.append("Volume lemah")

        # ==========================================
        # VOLUME SCORE
        # ==========================================

        if volume_score >= 6:
            score += 5

        elif volume_score >= 4:
            score += 3

        # ==========================================
        # CONFLUENCE
        # ==========================================

        if confluence_score >= 10:
            score += 10
            reasons.append("Confluence sangat kuat")

        elif confluence_score >= 7:
            score += 7
            reasons.append("Confluence kuat")

        elif confluence_score >= 4:
            score += 4
            reasons.append("Confluence cukup")

        # ==========================================
        # BATASI SCORE
        # ==========================================

        score = max(
            0,
            min(score, 100)
        )

        # ==========================================
        # STATUS
        # ==========================================

        if score >= 80:
            status = "A+ SETUP"

        elif score >= 65:
            status = "A SETUP"

        elif score >= 50:
            status = "B SETUP"

        elif score >= 35:
            status = "C SETUP"

        else:
            status = "WEAK SETUP"

        return {
            "score": score,
            "status": status,
            "reasons": reasons
        }
