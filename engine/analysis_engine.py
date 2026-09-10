from analysis.technical_analysis import TechnicalAnalysis
from analysis.macd_analysis import MACDAnalysis
from analysis.price_action import PriceAction
from analysis.volume_analysis import VolumeAnalysis
from analysis.breakout_analysis import BreakoutAnalysis
from analysis.support_resistance import SupportResistance
from analysis.candlestick import Candlestick


class AnalysisEngine:

    @staticmethod
    def analyze(data):

        trend = TechnicalAnalysis.check_trend(data)

        macd = MACDAnalysis.analyze(data)

        price_action = PriceAction.analyze(data)

        volume = VolumeAnalysis.analyze(data)

        support, resistance = SupportResistance.calculate(data)

        breakout = BreakoutAnalysis.analyze(
            data,
            resistance,
            volume
        )

        candlestick = Candlestick.analyze(data)

        return {
            "trend": trend,
            "macd": macd,
            "price_action": price_action,
            "volume": volume,
            "support": support,
            "resistance": resistance,
            "breakout": breakout,
            "candlestick": candlestick
        }