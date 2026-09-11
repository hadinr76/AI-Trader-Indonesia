from data.market_data import MarketData

from engine.technical_engine import TechnicalEngine
from engine.fundamental_engine import FundamentalEngine
from engine.entry_engine import EntryEngine
from engine.risk_reward_engine import RiskRewardEngine
from money_management.position_size_engine import PositionSizeEngine
from money_management.capital_manager import CapitalManager
from engine.confidence_engine import ConfidenceEngine
from engine.multi_timeframe_engine import MultiTimeFrameEngine
from engine.position_size_engine import PositionSizeEngine
from engine.explain_engine import ExplainEngine
from engine.investment_advisor_engine import InvestmentAdvisorEngine
from engine.market_regime_engine import MarketRegimeEngine
from engine.market_filter_engine import MarketFilterEngine
from engine.scanner_score_engine import ScannerScoreEngine

from signal.signal_engine import SignalEngine
from signal.smart_signal_engine import SmartSignalEngine

from ranking.ranking_engine import RankingEngine

from scoring.fundamental_score import FundamentalScore
from scoring.overall_score import OverallScore

from ai.rating import Rating
from ai.summary import AISummary

from decision.decision_engine_v4 import DecisionEngineV4

from analysis.swing_detector import SwingDetector
from analysis.sr_structure import SRStructure
from analysis.fibonacci_engine import FibonacciEngine
from analysis.confluence_engine import ConfluenceEngine
from analysis.trade_area_engine import TradeAreaEngine


class AIEngine:

    @staticmethod
    def analyze(
        kode,
        data=None,
        backtest_mode=False
    ):

        # =====================================================
        # MARKET DATA
        # =====================================================

        from data.data_manager import DataManager
        
        if data is None:
            data = DataManager.get_daily(kode)

        # =====================================================
        # TECHNICAL ANALYSIS
        # =====================================================

        technical = TechnicalEngine.analyze(data)

        technical_score = technical["score"]
        trend = technical["trend"]
        rsi = technical["rsi"]

        # =====================================================
        # MARKET STRUCTURE ANALYSIS
        # =====================================================

        current_price = float(
            technical["price"]
        )

        swing = SwingDetector.detect(
            data,
            window=3,
            lookback=120
        )

        sr_structure = SRStructure.calculate(
            current_price=current_price,
            swing_highs=swing["swing_highs"],
            swing_lows=swing["swing_lows"]
        )

        fibonacci = FibonacciEngine.calculate(
            current_price=current_price,
            swing_highs=swing["swing_highs"],
            swing_lows=swing["swing_lows"]
        )

        confluence = ConfluenceEngine.calculate(
            current_price=current_price,
            sr_structure=sr_structure,
            fibonacci=fibonacci
        )

        trade_area = TradeAreaEngine.calculate(
            current_price=current_price,
            confluence=confluence,
            sr_structure=sr_structure
        )

        # =====================================================
        # SIGNAL ENGINE
        # =====================================================

        signal = SignalEngine.analyze(technical)

        # =====================================================
        # FUNDAMENTAL ANALYSIS
        # =====================================================

        if backtest_mode:

            fundamental = {
                "per": 0,
                "pbv": 0,
                "roe": 0,
                "roa": 0,
                "der": 0,
                "eps": 0,
                "market_cap": 0,
                "dividend_yield": 0,
                "sector": "-",
                "industry": "-"
            }

            fundamental_score = 0

        else:

            fundamental = FundamentalEngine.analyze(kode)

            fundamental_score = FundamentalScore.calculate(
                fundamental
            )

        # =====================================================
        # OVERALL SCORE
        # =====================================================

        overall_score = OverallScore.calculate(
            technical_score,
            fundamental_score
        )

        # =====================================================
        # ENTRY ENGINE
        # =====================================================

        entry = EntryEngine.calculate(
            technical["price"],
            technical["support"],
            technical["resistance"],
            breakout=technical["breakout"]
        )

        # =====================================================
        # RISK REWARD
        # =====================================================

        risk_reward = RiskRewardEngine.calculate(
            entry["entry_low"],
            entry["entry_high"],
            entry["stop_loss"],
            entry["target1"],
            entry["target2"]
        )

        # =====================================================
        # Position Sizing
        # =====================================================

        position = PositionSizeEngine.calculate(
            capital=100_000_000,
            risk_percent=1,
            entry=risk_reward["entry"],
            stop_loss=entry["stop_loss"]
        )

        # ==========================================
        # CAPITAL CHECK
        # ==========================================

        capital = CapitalManager.allocate(

            capital=100_000_000,

            investment=position["investment"]

        )

        # =====================================================
        # MULTI TIME FRAME
        # =====================================================

        if backtest_mode:

            mtf = {
                "summary": {
                    "status": "Neutral",
                    "average_score": 0
                }
            }

        else:

            mtf = MultiTimeFrameEngine.analyze(kode)

        # =====================================================
        # MARKET REGIME
        # =====================================================
        
        if backtest_mode:

            market_regime = {
                "market_regime": "SIDEWAYS",
                "trend": "-",
                "macd": "-",
                "rsi": 0
            }

        else:

            market_regime = MarketRegimeEngine.analyze()

        
        # =====================================================
        # CONFIDENCE
        # =====================================================

        confidence = ConfidenceEngine.calculate(
            technical,
            fundamental_score,
            overall_score
        )

        # =====================================================
        # RATING
        # =====================================================

        rating = Rating.calculate(
            overall_score
        )

       
        # =====================================================
        # DECISION ENGINE V4
        # =====================================================

        decision = DecisionEngineV4.decide(

            trend=trend,

            market_regime=market_regime["market_regime"],

            mtf_status=mtf["summary"]["status"],

            momentum=technical["momentum"],

            macd=technical["macd"],

            volume=technical["volume"],

            breakout=technical["breakout"],

            candlestick=technical["candlestick"],

            rsi=rsi,

            confidence=confidence["confidence"],

            rr=risk_reward["rr2"],

            fundamental_score=fundamental_score

        )

        recommendation = decision["recommendation"]
        
        # =====================================================
        # SMART SIGNAL
        # =====================================================

        smart_signal = SmartSignalEngine.analyze(

            recommendation=recommendation,

            confidence=confidence["confidence"],

            overall_score=overall_score,

            rr=risk_reward["rr2"],

            mtf_status=mtf["summary"]["status"]

        )

        

        # =====================================================
        # RANKING
        # =====================================================

        ranking_score = RankingEngine.calculate(

            overall_score=overall_score,

            confidence=confidence["confidence"],

            rr=risk_reward["rr2"],

            smart_signal=smart_signal["signal"],

            mtf_score=mtf["summary"]["average_score"]

        )

        

        # =====================================================
        # Scaner Score
        # =====================================================

        scanner_score = ScannerScoreEngine.calculate({

            "recommendation": recommendation,

            "ranking_score": ranking_score,

            "confidence": confidence["confidence"],

            "overall_score": overall_score

        })

        # =====================================================
        # Market Filter
        # =====================================================
        
        market_filter = MarketFilterEngine.adjust(
            regime=market_regime["market_regime"],
            recommendation=recommendation,
             ranking_score=ranking_score
        
        )
        
        recommendation = market_filter["recommendation"]
        ranking_score = market_filter["ranking_score"]
        

        # =====================================================
        # AI SUMMARY
        # =====================================================

        summary = AISummary.generate(

            data,

            trend,

            overall_score,

            recommendation

        )

              

        # =====================================================
        # Explain Engine
        # =====================================================

        explanation = ExplainEngine.generate({
            "trend":trend,

            "mtf_status": mtf["summary"]["status"],

            "macd": technical["macd"],
            
            "volume": technical["volume"],

            "breakout": technical["breakout"],

            "rsi": rsi,

            "rr2": risk_reward["rr2"],

            "confidence": confidence["confidence"],

            "fundamental_score": fundamental_score,

            "ranking_score": ranking_score

        })
        
        # ==========================
        # Investment Advisor
        # ==========================

        investment_advisor = InvestmentAdvisorEngine.generate({

            "code": kode,

            "trend": trend,

            "mtf_status": mtf["summary"]["status"],

            "macd": technical["macd"],

            "rsi": rsi,

            "rr2": risk_reward["rr2"],

            "confidence": confidence["confidence"],

            "recommendation": recommendation,

            "ranking_score": ranking_score

        })

        # =====================================================
        # RETURN
        # =====================================================

        return {

            "code": kode,

            "price": technical["price"],

            "trend": trend,

            "rsi": rsi,

            "macd": technical["macd"],

            "price_action": technical["price_action"],

            "volume": technical["volume"],

            "breakout": technical["breakout"],

            "support": technical["support"],

            "resistance": technical["resistance"],

                        # Market Structure V2
            "major_support": sr_structure["major_support"],

            "minor_support": sr_structure["minor_support"],

            "minor_resistance": sr_structure["minor_resistance"],

            "major_resistance": sr_structure["major_resistance"],

            # Fibonacci
            "fib_382": fibonacci["fib_382"],

            "fib_500": fibonacci["fib_500"],

            "fib_618": fibonacci["fib_618"],

            "fib_786": fibonacci["fib_786"],

            # Trade Area V2
            "buy_area_low": trade_area["buy_area_low"],

            "buy_area_high": trade_area["buy_area_high"],

            "ideal_entry_v2": trade_area["ideal_entry"],

            "stop_loss_v2": trade_area["stop_loss"],

            "target1_v2": trade_area["tp1"],

            "target2_v2": trade_area["tp2"],

            "rr1_v2": trade_area["rr_tp1"],

            "rr2_v2": trade_area["rr_tp2"],

            "trade_status": trade_area["status"],

            "trade_quality": trade_area["trade_quality"],

            "trade_reason": trade_area["trade_reason"],

            "confluence_score": trade_area["confluence_score"],

            "technical_score": technical_score,

            "fundamental_score": fundamental_score,

            "overall_score": overall_score,

            "rating": rating["stars"],

            "category": rating["category"],

            "decision_score": decision["score"],
            
            "decision_reason": decision["reasons"],

            "recommendation": recommendation,

            # Signal Engine
            "signal": signal["signal"],

            "signal_confidence": signal["confidence"],

            "signal_reason": signal["reason"],

            # Entry
            "entry_low": entry["entry_low"],

            "entry_high": entry["entry_high"],

            "stop_loss": entry["stop_loss"],

            "target1": entry["target1"],

            "target2": entry["target2"],

            # Risk Reward
            "risk": risk_reward["risk"],

            "reward1": risk_reward["reward1"],

            "reward2": risk_reward["reward2"],

            "rr1": risk_reward["rr1"],

            "rr2": risk_reward["rr2"],

            "capital": position["capital"],

            "risk_percent": position["risk_percent"],

            "max_risk": position["max_risk"],

            "risk_per_share": position["risk_per_share"],

            "shares": position["shares"],

            "lots": position["lots"],

            "investment": position["investment"],

            "capital_remaining": capital["remaining"],

            "capital_approved": capital["approved"],


            # Confidence
            "confidence": confidence["confidence"],

            "confidence_reason": confidence["reasons"],

            # Smart Signal
            "smart_signal": smart_signal["signal"],

            "smart_score": smart_signal["score"],

            "smart_reason": smart_signal["reason"],

            # Multi Time Frame
            "mtf_status": mtf["summary"]["status"],

            "mtf_average_score": mtf["summary"]["average_score"],

                        "monthly_trend": mtf.get(
                "Monthly",
                {}
            ).get(
                "trend",
                "Unknown"
            ),

            "weekly_trend": mtf.get(
                "Weekly",
                {}
            ).get(
                "trend",
                "Unknown"
            ),

            "daily_trend": mtf.get(
                "Daily",
                {}
            ).get(
                "trend",
                "Unknown"
            ),

            "h4_trend": mtf.get(
                "4H",
                {}
            ).get(
                "trend",
                "Unknown"
            ),

            "h1_trend": mtf.get(
                "1H",
                {}
            ).get(
                "trend",
                "Unknown"
            ),

            # Ranking
            "ranking_score": ranking_score,

            # Scanner Score

            "scanner_score": scanner_score,

            # Market Regime
            "market_regime": market_regime["market_regime"],

            "market_trend": market_regime["trend"],

            "market_rsi": market_regime["rsi"],

            "market_macd": market_regime["macd"],

            # Summary
            "summary": summary,

            "explanation": explanation,

            "investment_advisor": investment_advisor,

            "fundamental": fundamental

            
        }