from data.data_manager import DataManager
from engine.indicator_engine import IndicatorEngine
from engine.trade_engine import TradeEngine


class BacktestEngine:

    @staticmethod
    def run(kode):

        # ==========================
        # Ambil Data
        # ==========================

        data = DataManager.get_daily(kode)

        # ==========================
        # Indicator
        # ==========================

        data = IndicatorEngine.calculate(data)

        # ==========================
        # Simulasi Trading
        # ==========================

        trades = TradeEngine.simulate(data)

        return trades