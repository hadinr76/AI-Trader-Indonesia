class VolumeConfirmation:

    @staticmethod
    def analyze(
        data,
        breakout_status=None,
        retest_status=None
    ):

        if data is None or data.empty:
            raise ValueError("Data kosong")

        if "Volume" not in data.columns:
            raise ValueError(
                "Kolom Volume tidak ditemukan"
            )

        volume = data["Volume"].squeeze()

        if len(volume) < 20:
            return {
                "status": "INSUFFICIENT DATA",
                "relative_volume": None,
                "volume_trend": None,
                "confirmation": False,
                "score": 0
            }

        current_volume = float(
            volume.iloc[-1]
        )

        previous_volume = float(
            volume.iloc[-2]
        )

        avg_volume_20 = float(
            volume.tail(20).mean()
        )

        relative_volume = (
            current_volume /
            avg_volume_20
            if avg_volume_20 > 0
            else 0
        )

        if current_volume > previous_volume:
            volume_trend = "RISING"

        elif current_volume < previous_volume:
            volume_trend = "FALLING"

        else:
            volume_trend = "FLAT"

        score = 0
        reasons = []

        if relative_volume >= 2.0:
            score += 3
            reasons.append(
                "Relative volume sangat kuat"
            )

        elif relative_volume >= 1.5:
            score += 2
            reasons.append(
                "Relative volume kuat"
            )

        elif relative_volume >= 1.0:
            score += 1
            reasons.append(
                "Relative volume normal"
            )

        else:
            reasons.append(
                "Relative volume lemah"
            )

        if volume_trend == "RISING":
            score += 1
            reasons.append(
                "Volume meningkat"
            )

        if breakout_status == "Valid Breakout":
            score += 2
            reasons.append(
                "Volume mendukung valid breakout"
            )

        if retest_status == "VALID RETEST":
            score += 2
            reasons.append(
                "Volume mendukung valid retest"
            )

        confirmation = (
            score >= 4
        )

        if score >= 6:
            status = "VERY STRONG"

        elif score >= 4:
            status = "CONFIRMED"

        elif score >= 2:
            status = "MODERATE"

        else:
            status = "WEAK"

        return {
            "status": status,
            "relative_volume": round(
                relative_volume,
                2
            ),
            "volume_trend": volume_trend,
            "confirmation": confirmation,
            "score": score,
            "reasons": reasons
        }
