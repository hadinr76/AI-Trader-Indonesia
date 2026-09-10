from data.data_manager import DataManager
from engine.technical_engine import TechnicalEngine
from engine.mtf_score_engine import MTFScoreEngine
from engine.monthly_trend_engine import MonthlyTrendEngine


class MultiTimeFrameEngine:

    @staticmethod
    def analyze(kode):

        result = {}

        try:
            monthly = DataManager.get_monthly(kode)

            monthly_analysis = (
                MonthlyTrendEngine.analyze(
                    monthly
                )
            )

            result["Monthly"] = {
                "trend": monthly_analysis["trend"],
                "price": monthly_analysis["price"],
                "ema10": monthly_analysis["ema10"],
                "ema20": monthly_analysis["ema20"]
            }

        except Exception:

            result["Monthly"] = {
                "trend": "Unknown",
                "price": 0,
                "ema10": 0,
                "ema20": 0
            }

        try:
            weekly = DataManager.get_weekly(kode)

            technical = TechnicalEngine.analyze(weekly)

            result["Weekly"] = {
                "trend": technical["trend"],
                "score": technical["score"]
            }

        except Exception:

            result["Weekly"] = {
                "trend": "Unknown",
                "score": 0
            }

        try:
            daily = DataManager.get_daily(kode)

            technical = TechnicalEngine.analyze(daily)

            result["Daily"] = {
                "trend": technical["trend"],
                "score": technical["score"]
            }

        except Exception:

            result["Daily"] = {
                "trend": "Unknown",
                "score": 0
            }

        try:
            h4 = DataManager.get_4h(kode)

            technical = TechnicalEngine.analyze(h4)

            result["4H"] = {
                "trend": technical["trend"],
                "score": technical["score"]
            }

        except Exception:

            result["4H"] = {
                "trend": "Unknown",
                "score": 0
            }

        try:
            h1 = DataManager.get_1h(kode)

            technical = TechnicalEngine.analyze(h1)

            result["1H"] = {
                "trend": technical["trend"],
                "score": technical["score"]
            }

        except Exception:

            result["1H"] = {
                "trend": "Unknown",
                "score": 0
            }

        summary = MTFScoreEngine.calculate(result)

        result["summary"] = summary

        return result