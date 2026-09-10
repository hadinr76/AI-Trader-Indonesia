class TechnicalRankingEngine:

    """
    Technical Ranking Engine

    Mengubah hasil Technical Screener menjadi
    ranking akhir kandidat teknikal.

    Faktor utama:

    - Technical Score
    - Momentum Score
    - RSI Quality
    - Relative Volume
    - Distance to Resistance
    - Breakout Status

    Output akhir:
    - ranking_score 0 - 100
    - ranking_label
    - reasons
    """

    # =====================================================
    # RSI SCORE
    # =====================================================

    @staticmethod
    def _rsi_score(rsi):

        rsi = float(rsi)

        if 55 <= rsi <= 68:
            return 100

        if 50 <= rsi < 55:
            return 85

        if 68 < rsi <= 72:
            return 80

        if 45 <= rsi < 50:
            return 65

        if 72 < rsi <= 78:
            return 55

        if 40 <= rsi < 45:
            return 45

        if 78 < rsi <= 85:
            return 30

        if rsi > 85:
            return 10

        return 20

    # =====================================================
    # RVOL SCORE
    # =====================================================

    @staticmethod
    def _rvol_score(rvol):

        rvol = float(rvol)

        if rvol >= 2.0:
            return 100

        if rvol >= 1.5:
            return 90

        if rvol >= 1.2:
            return 80

        if rvol >= 1.0:
            return 70

        if rvol >= 0.75:
            return 55

        if rvol >= 0.50:
            return 40

        if rvol >= 0.25:
            return 25

        return 10

    # =====================================================
    # RESISTANCE SCORE
    # =====================================================

    @staticmethod
    def _resistance_score(
        price,
        resistance
    ):

        price = float(price)
        resistance = float(resistance or 0)

        if price <= 0:
            return 0

        if resistance <= 0:
            return 50

        distance_pct = (
            (
                resistance - price
            )
            /
            price
        ) * 100

        # Sudah breakout resistance
        if distance_pct < 0:
            return 85

        # Terlalu dekat resistance
        if distance_pct <= 1:
            return 40

        if distance_pct <= 3:
            return 60

        if distance_pct <= 5:
            return 75

        if distance_pct <= 10:
            return 90

        return 80

    # =====================================================
    # BREAKOUT SCORE
    # =====================================================

    @staticmethod
    def _breakout_score(status):

        if status == "Valid Breakout":
            return 100

        if status == "Weak Breakout":
            return 70

        if status == "Belum Breakout":
            return 60

        return 40

    # =====================================================
    # MOMENTUM NORMALIZATION
    # =====================================================

    @staticmethod
    def _momentum_score(score):

        score = float(score or 0)

        if score > 100:
            score = 100

        if score < 0:
            score = 0

        return score

    # =====================================================
    # CALCULATE
    # =====================================================

    @classmethod
    def calculate(
        cls,
        data
    ):

        technical_score = float(
            data.get(
                "technical_score",
                0
            )
        )

        momentum_score = (
            cls._momentum_score(
                data.get(
                    "momentum_score",
                    0
                )
            )
        )

        rsi = float(
            data.get(
                "rsi",
                0
            )
        )

        relative_volume = float(
            data.get(
                "relative_volume",
                0
            )
        )

        price = float(
            data.get(
                "price",
                0
            )
        )

        resistance = float(
            data.get(
                "resistance",
                0
            ) or 0
        )

        breakout = data.get(
            "breakout",
            ""
        )

        # =================================================
        # SUB SCORE
        # =================================================

        rsi_score = cls._rsi_score(
            rsi
        )

        rvol_score = cls._rvol_score(
            relative_volume
        )

        resistance_score = (
            cls._resistance_score(
                price,
                resistance
            )
        )

        breakout_score = (
            cls._breakout_score(
                breakout
            )
        )

        # =================================================
        # WEIGHT
        #
        # Technical   45%
        # Momentum    20%
        # RSI         15%
        # RVOL        10%
        # Resistance   5%
        # Breakout     5%
        # =================================================

        ranking_score = (

            technical_score * 0.45

            +

            momentum_score * 0.20

            +

            rsi_score * 0.15

            +

            rvol_score * 0.10

            +

            resistance_score * 0.05

            +

            breakout_score * 0.05

        )

        # =================================================
        # PENALTY
        # =================================================

        penalty = 0

        reasons = []

        # RSI terlalu tinggi
        if rsi > 85:

            penalty += 12

            reasons.append(
                "RSI sangat overbought"
            )

        elif rsi > 78:

            penalty += 7

            reasons.append(
                "RSI overbought"
            )

        elif rsi > 72:

            penalty += 3

            reasons.append(
                "RSI mulai tinggi"
            )

        # Volume sangat lemah
        if relative_volume < 0.25:

            penalty += 10

            reasons.append(
                "Relative volume sangat rendah"
            )

        elif relative_volume < 0.50:

            penalty += 5

            reasons.append(
                "Relative volume rendah"
            )

        # Harga sangat dekat resistance
        if (
            price > 0
            and
            resistance > 0
        ):

            distance_pct = (
                (
                    resistance - price
                )
                /
                price
            ) * 100

            if 0 <= distance_pct <= 1:

                penalty += 6

                reasons.append(
                    "Harga sangat dekat resistance"
                )

            elif 1 < distance_pct <= 3:

                penalty += 3

                reasons.append(
                    "Harga dekat resistance"
                )

        # Breakout lemah
        if breakout == "Weak Breakout":

            penalty += 2

            reasons.append(
                "Breakout lemah"
            )

        # =================================================
        # FINAL SCORE
        # =================================================

        ranking_score -= penalty

        ranking_score = max(
            0,
            min(
                ranking_score,
                100
            )
        )

        ranking_score = round(
            ranking_score,
            2
        )

        # =================================================
        # LABEL
        # =================================================

        if ranking_score >= 80:

            label = "STRONG CANDIDATE"

        elif ranking_score >= 70:

            label = "CANDIDATE"

        elif ranking_score >= 60:

            label = "WATCH"

        else:

            label = "LOW PRIORITY"

        # =================================================
        # POSITIVE REASONS
        # =================================================

        if technical_score >= 70:

            reasons.append(
                "Technical score kuat"
            )

        if momentum_score >= 90:

            reasons.append(
                "Momentum sangat kuat"
            )

        if 55 <= rsi <= 68:

            reasons.append(
                "RSI berada di zona ideal"
            )

        if relative_volume >= 2:

            reasons.append(
                "Volume jauh di atas rata-rata"
            )

        elif relative_volume >= 1.2:

            reasons.append(
                "Volume di atas rata-rata"
            )

        if breakout == "Valid Breakout":

            reasons.append(
                "Valid breakout"
            )

        # =================================================
        # RESULT
        # =================================================

        return {

            "ranking_score":
                ranking_score,

            "ranking_label":
                label,

            "penalty":
                penalty,

            "rsi_quality_score":
                rsi_score,

            "rvol_quality_score":
                rvol_score,

            "resistance_quality_score":
                resistance_score,

            "breakout_quality_score":
                breakout_score,

            "reasons":
                reasons

        }