from scanner.index_classifier import IndexClassifier
from scanner.fast_screener import FastScreener
from scanner.technical_screener import TechnicalScreener

from engine.technical_ranking_engine import TechnicalRankingEngine
from engine.confidence_engine import ConfidenceEngine
from engine.entry_engine import EntryEngine
from engine.risk_reward_engine import RiskRewardEngine
from engine.watchlist_priority_engine import WatchlistPriorityEngine

from fundamental.fundamental_engine import FundamentalEngine
from scoring.fundamental_score import FundamentalScore
from valuation.valuation_engine import ValuationEngine

from decision.decision_engine_v4 import DecisionEngineV4


class DailyRecommendation:

    """
    DAILY RECOMMENDATION ENGINE

    Pipeline:

    981 saham
        ↓
    Fast Screener
        ↓
    Technical Screener
        ↓
    Technical Ranking
        ↓
    Top Kandidat
        ↓
    Fundamental
        ↓
    Confidence
        ↓
    Entry Plan
        ↓
    Risk Reward
        ↓
    Decision Engine V4
        ↓
    Final Recommendation
    """

    # =====================================================
    # INITIALIZE
    # =====================================================

    def __init__(
        self,
        period="1y",
        technical_limit=20
    ):

        self.period = period

        self.technical_limit = technical_limit

    # =====================================================
    # TECHNICAL PIPELINE
    # =====================================================

    def get_technical_candidates(self):

        print()
        print("=" * 70)
        print("STEP 1 - FAST SCREENER")
        print("=" * 70)

        fast_screener = FastScreener(
            period=self.period
        )

        fast_results = (
            fast_screener.scan()
        )

        candidates = (
            FastScreener.passed_stocks(
                fast_results
            )
        )

        print()
        print(
            "Fast Screener PASS :",
            len(candidates)
        )

        # =================================================
        # TECHNICAL SCREENER
        # =================================================

        print()
        print("=" * 70)
        print("STEP 2 - TECHNICAL SCREENER")
        print("=" * 70)

        technical_screener = (
            TechnicalScreener(
                candidates=candidates,
                period=self.period
            )
        )

        technical_results = (
            technical_screener.scan()
        )

        print()
        print(
            "Technical berhasil :",
            len(technical_results)
        )

        # =================================================
        # TECHNICAL RANKING
        # =================================================

        print()
        print("=" * 70)
        print("STEP 3 - TECHNICAL RANKING")
        print("=" * 70)

        ranked_results = []

        for stock in technical_results:

            try:

                ranking = (
                    TechnicalRankingEngine
                    .calculate(
                        stock
                    )
                )

                result = stock.copy()

                result.update(
                    ranking
                )

                ranked_results.append(
                    result
                )

            except Exception as e:

                print(
                    f"Gagal ranking "
                    f"{stock.get('code', '-')}: "
                    f"{e}"
                )

        ranked_results.sort(

            key=lambda x:
            x["ranking_score"],

            reverse=True

        )

        # =================================================
        # MULTI-ROUTE CANDIDATE SELECTION
        # =================================================

        # Kandidat tidak lagi hanya berasal
        # dari Top Technical Ranking.
        #
        # Kita mengambil kandidat dari:
        #
        # 1. Top Overall
        # 2. Top LQ45
        # 3. Top IDX30
        # 4. Saham yang sedang berada di ENTRY ZONE
        # 5. Saham yang sedang VALID BREAKOUT
        #
        # Setelah itu:
        # - digabungkan
        # - duplikat dihapus
        # - dibatasi agar deep analysis tidak terlalu berat
        # =================================================

        overall_candidates = (
            ranked_results[
                :self.technical_limit
            ]
        )

        # =================================================
        # LOAD INDEX MEMBERSHIP SEKALI
        # =================================================

        membership = (
            IndexClassifier
            .load_membership()
        )

        # =================================================
        # TOP LQ45
        # =================================================

        lq45_candidates = [

            stock

            for stock in ranked_results

            if "LQ45" in membership.get(
                stock["code"],
                []
            )

        ][:10]

        # =================================================
        # TOP IDX30
        # =================================================

        idx30_candidates = [

            stock

            for stock in ranked_results

            if "IDX30" in membership.get(
                stock["code"],
                []
            )

        ][:10]

        # =================================================
        # ENTRY ZONE CANDIDATES
        # =================================================

        entry_zone_candidates = []

        # =================================================
        # BREAKOUT CANDIDATES
        # =================================================

        breakout_candidates = []

        for stock in ranked_results:

            try:

                entry_plan = (
                    EntryEngine
                    .calculate(

                        price=stock["price"],

                        support=stock["support"],

                        resistance=stock[
                            "resistance"
                        ],

                        breakout=stock[
                            "breakout"
                        ]

                    )
                )

            except Exception:

                continue

            # =============================================
            # BUY NOW
            # =============================================

            if (
                entry_plan["recommendation"] == "BUY"

                and stock.get(
                    "liquidity_status",
                    "ILLIQUID"
                ) in [
                    "VERY LIQUID",
                    "LIQUID",
                    "MODERATE"
                ]

                and stock["trend"] in [
                    "Strong Bullish",
                    "Bullish",
                    "Recovery"
                ]

                and stock["momentum"] in [
                    "Strong Bullish",
                    "Bullish"
                ]

                and stock["macd"] in [
                    "Bullish Cross",
                    "Bullish"
                ]

                and stock["rsi"] >= 50
            ):

                entry_zone_candidates.append(
                    stock
                )

            # =============================================
            # BREAKOUT BUY
            # =============================================

            if (
                entry_plan[
                    "recommendation"
                ]
                == "BREAKOUT BUY"

                and stock.get(
                    "liquidity_status",
                    "ILLIQUID"
                ) in [
                    "VERY LIQUID",
                    "LIQUID",
                    "MODERATE"
                ]
            ):

                breakout_candidates.append(
                    stock
                )

        # =================================================
        # SORT ENTRY ZONE
        # =================================================

        entry_zone_candidates.sort(

            key=lambda x:
            x["ranking_score"],

            reverse=True

        )

        # =================================================
        # SORT BREAKOUT
        # =================================================

        breakout_candidates.sort(

            key=lambda x:
            x["ranking_score"],

            reverse=True

        )

        # Batasi agar deep analysis tidak terlalu berat

        entry_zone_candidates = (
            entry_zone_candidates[:20]
        )

        breakout_candidates = (
            breakout_candidates[:20]
        )

        # =================================================
        # COMBINE
        #
        # PRIORITAS:
        #
        # 1. BUY NOW
        # 2. BREAKOUT BUY
        # 3. LQ45
        # 4. IDX30
        # 5. TOP OVERALL
        # =================================================

        candidate_groups = [

            entry_zone_candidates,

            breakout_candidates,

            lq45_candidates,

            idx30_candidates,

            overall_candidates

        ]

        combined_candidates = []

        seen_codes = set()

        for group in candidate_groups:

            for stock in group:

                code = stock["code"]

                if code in seen_codes:

                    continue

                seen_codes.add(
                    code
                )

                combined_candidates.append(
                    stock
                )

        # =================================================
        # SAFETY LIMIT
        # =================================================

        max_deep_analysis = 50

        top_candidates = (
            combined_candidates[
                :max_deep_analysis
            ]
        )

        # =================================================
        # SUMMARY
        # =================================================

        print()
        print("=" * 70)
        print("DEEP ANALYSIS CANDIDATE SELECTION")
        print("=" * 70)

        print(
            "Top Overall        :",
            len(overall_candidates)
        )

        print(
            "Top LQ45           :",
            len(lq45_candidates)
        )

        print(
            "Top IDX30          :",
            len(idx30_candidates)
        )

        print(
            "BUY NOW Candidate  :",
            len(entry_zone_candidates)
        )

        print()
        print("DAFTAR BUY NOW CANDIDATE")

        for stock in entry_zone_candidates:

            print(
                stock["code"],
                "| Price:",
                stock["price"],
                "| Ranking:",
                stock["ranking_score"],
                "| RSI:",
                stock["rsi"],
                "| MACD:",
                stock["macd"],
                "| Volume:",
                stock["volume"],
                "| RVOL:",
                stock["relative_volume"]
            )

        print(
            "Breakout Candidate :",
            len(breakout_candidates)
        )

        print()
        print("DAFTAR BREAKOUT CANDIDATE")

        for stock in breakout_candidates:

            print(
                stock["code"],
                "| Price:",
                stock["price"],
                "| Ranking:",
                stock["ranking_score"],
                "| RSI:",
                stock["rsi"],
                "| MACD:",
                stock["macd"],
                "| Volume:",
                stock["volume"],
                "| RVOL:",
                stock["relative_volume"],
                "| Liquidity:",
                stock.get(
                    "liquidity_status",
                    "-"
                ),
                "| AvgValue20:",
                stock.get(
                    "average_transaction_value_20",
                    0
                )
            )

        print(
            "Unique Candidate   :",
            len(combined_candidates)
        )

        print(
            "Deep Analysis      :",
            len(top_candidates)
        )

        return top_candidates

    # =====================================================
    # ANALYZE ONE CANDIDATE
    # =====================================================

    @staticmethod
    def analyze_candidate(stock):

        code = stock["code"]

        print()
        print("-" * 70)
        print(
            "Deep Analysis :",
            code
        )
        print("-" * 70)

        # =================================================
        # FUNDAMENTAL
        # =================================================

        fundamental = None

        fundamental_score = 0

        try:

            fundamental = (
                FundamentalEngine
                .analyze(
                    code
                )
            )

            if fundamental:

                fundamental_score = (
                    FundamentalScore
                    .calculate(
                        fundamental
                    )
                )

        except Exception as e:

            print(
                f"Fundamental {code} gagal: "
                f"{e}"
            )

        # =================================================
        # VALUATION V3.2
        # =================================================

        valuation = {

            "fair_value": 0,
            "estimated_fair_value": 0,
            "price_to_fair_value": 0,
            "margin_of_safety": 0,

            "valuation_status": "UNKNOWN",
            "valuation_label": "TIDAK DIKETAHUI",

            "valuation_method": "NONE",
            "valuation_confidence": "LOW",
            "valuation_reliability": "LOW",

            "fair_value_capped": False,
            "warnings": []

        }

        if fundamental:

            try:

                valuation = (
                    ValuationEngine
                    .calculate(

                        price=stock["price"],

                        eps=fundamental.get(
                            "eps",
                            0
                        ),

                        pbv=fundamental.get(
                            "pbv",
                            0
                        ),

                        per=fundamental.get(
                            "per",
                            0
                        ),

                        roe=fundamental.get(
                            "roe",
                            0
                        ),

                        sector=fundamental.get(
                            "sector",
                            "-"
                        ),

                        industry=fundamental.get(
                            "industry",
                            "-"
                        )

                    )
                )

            except Exception as e:

                print(
                    f"Valuation {code} gagal: "
                    f"{e}"
                )

        # =================================================
        # CONFIDENCE
        # =================================================

        try:

            confidence_result = (
                ConfidenceEngine
                .calculate(
                    technical=stock,
                    fundamental_score=fundamental_score,
                    overall_score=stock[
                        "ranking_score"
                    ]
                )
            )

        except Exception as e:

            print(
                f"Confidence {code} gagal: "
                f"{e}"
            )

            confidence_result = {

                "confidence": 0,
                "level": "VERY LOW",
                "reasons": []

            }

        confidence = (
            confidence_result[
                "confidence"
            ]
        )

        # =================================================
        # ENTRY PLAN
        # =================================================

        try:

            entry = (
                EntryEngine
                .calculate(

                    price=stock["price"],

                    support=stock["support"],

                    resistance=stock[
                        "resistance"
                    ],

                    breakout=stock[
                        "breakout"
                    ]

                )
            )

        except Exception as e:

            print(
                f"Entry {code} gagal: "
                f"{e}"
            )

            return None

        # =================================================
        # RISK REWARD
        # =================================================

        rr = (
            RiskRewardEngine
            .calculate(

                entry["entry_low"],

                entry["entry_high"],

                entry["stop_loss"],

                entry["target1"],

                entry["target2"]

            )
        )

        # =================================================
        # MARKET REGIME
        #
        # Sementara dibuat neutral.
        # Nanti kita hubungkan ke MarketRegimeEngine.
        # =================================================

        market_regime = "SIDEWAYS"

        # =================================================
        # MULTI TIMEFRAME
        #
        # Sementara dibuat neutral.
        # Nanti kita hubungkan ke MultiTimeframeEngine.
        # =================================================

        mtf_status = "Mixed"

        # =================================================
        # FINAL DECISION
        # =================================================

        try:

            decision = (
                DecisionEngineV4
                .decide(

                    trend=stock["trend"],

                    market_regime=market_regime,

                    mtf_status=mtf_status,

                    momentum=stock[
                        "momentum"
                    ],

                    macd=stock[
                        "macd"
                    ],

                    volume=stock[
                        "volume"
                    ],

                    breakout=stock[
                        "breakout"
                    ],

                    candlestick=stock[
                        "candlestick"
                    ],

                    rsi=stock[
                        "rsi"
                    ],

                    confidence=confidence,

                    rr=rr["rr1"],

                    fundamental_score=(
                        fundamental_score
                    ),

                    entry_recommendation=(
                        entry[
                            "recommendation"
                        ]
                    )

                )
            )

        except Exception as e:

            print(
                f"Decision {code} gagal: "
                f"{e}"
            )

            return None

        # =================================================
        # INDEX CLASSIFICATION
        # =================================================

        index_info = IndexClassifier.classify(
            code
        )


        # =================================================
        # RESULT
        # =================================================

        return {

            "code":
                code,

            "price":
                stock["price"],

            # Technical

            "trend":
                stock["trend"],

            "momentum":
                stock["momentum"],

            "rsi":
                stock["rsi"],

            "macd":
                stock["macd"],

            "volume":
                stock["volume"],

            "relative_volume":
                stock[
                    "relative_volume"
                ],

            "average_transaction_value_20":
                stock.get(
                    "average_transaction_value_20",
                    0
                ),

            "liquidity_status":
                stock.get(
                    "liquidity_status",
                    "ILLIQUID"
                ),

            "breakout":
                stock["breakout"],

            "support":
                stock["support"],

            "resistance":
                stock[
                    "resistance"
                ],

            "technical_score":
                stock[
                    "technical_score"
                ],

            "ranking_score":
                stock[
                    "ranking_score"
                ],

            "ranking_label":
                stock[
                    "ranking_label"
                ],

            # Index

            "index_category":
                index_info[
                    "category"
                ],

            "indexes":
                index_info[
                    "indexes"
                ],

            "is_lq45":
                IndexClassifier.is_member(
                    code,
                    "LQ45"
                ),

            "is_idx30":
                IndexClassifier.is_member(
                    code,
                    "IDX30"
                ),

            # Fundamental

            "fundamental_score":
                fundamental_score,

            "fundamental":
                fundamental,

            # Valuation

            "fair_value":
                valuation.get(
                    "fair_value",
                    0
                ),

            "estimated_fair_value":
                valuation.get(
                    "estimated_fair_value",
                    0
                ),

            "price_to_fair_value":
                valuation.get(
                    "price_to_fair_value",
                    0
                ),

            "margin_of_safety":
                valuation.get(
                    "margin_of_safety",
                    0
                ),

            "valuation_status":
                valuation.get(
                    "valuation_status",
                    "UNKNOWN"
                ),

            "valuation_label":
                valuation.get(
                    "valuation_label",
                    "TIDAK DIKETAHUI"
                ),

            "valuation_method":
                valuation.get(
                    "valuation_method",
                    "NONE"
                ),

            "valuation_confidence":
                valuation.get(
                    "valuation_confidence",
                    "LOW"
                ),

            "valuation_reliability":
                valuation.get(
                    "valuation_reliability",
                    "LOW"
                ),

            "fair_value_capped":
                valuation.get(
                    "fair_value_capped",
                    False
                ),

            "valuation_warnings":
                valuation.get(
                    "warnings",
                    []
                ),


            # Confidence

            "confidence":
                confidence,

            "confidence_level":
                confidence_result[
                    "level"
                ],

            # Entry

            "entry_low":
                entry[
                    "entry_low"
                ],

            "entry_high":
                entry[
                    "entry_high"
                ],

            "stop_loss":
                entry[
                    "stop_loss"
                ],

            "target1":
                entry[
                    "target1"
                ],

            "target2":
                entry[
                    "target2"
                ],

            "entry_status":
                entry[
                    "position"
                ],

            "entry_recommendation":
                entry[
                    "recommendation"
                ],

            "entry_reason":
                entry[
                    "reason"
                ],

            "distance_from_entry_high":
                entry.get(
                    "distance_from_entry_high",
                    0
                ),

            # Risk Reward

            "average_entry":
                rr[
                    "entry"
                ],

            "rr1":
                rr[
                    "rr1"
                ],

            "rr2":
                rr[
                    "rr2"
                ],

            # Decision

            "decision_score":
                decision[
                    "score"
                ],

            "score_recommendation":
                decision[
                    "score_recommendation"
                ],

            "recommendation":
                decision[
                    "recommendation"
                ],

            "decision_reasons":
                decision[
                    "reasons"
                ]

        }

    # =====================================================
    # RUN
    # =====================================================

    def run(self):

        print()
        print("=" * 70)
        print("AI TRADER INDONESIA")
        print("DAILY STOCK RECOMMENDATION")
        print("=" * 70)

        candidates = (
            self.get_technical_candidates()
        )

        final_results = []

        # =================================================
        # DEEP ANALYSIS
        # =================================================

        for stock in candidates:

            result = (
                self.analyze_candidate(
                    stock
                )
            )

            if result is None:

                continue

            final_results.append(
                result
            )

        # =================================================
        # BUY NOW PRIORITY SCORE V2
        #
        # Decision           : 25%
        # Confidence         : 20%
        # Technical Ranking  : 15%
        # Fundamental        : 10%
        # Valuation          : 15%
        # Risk Reward        : 10%
        # RSI Timing         : 5%
        #
        # TOTAL              : 100%
        # =================================================

        for stock in final_results:

            if stock["recommendation"] not in [
                "BUY",
                "STRONG BUY"
            ]:

                stock["buy_now_priority_score"] = 0
                stock["buy_now_valuation_score"] = 0

                continue

            score = 0

            # Decision
            score += (
                stock.get(
                    "decision_score",
                    0
                )
                * 0.25
            )

            # Confidence
            score += (
                stock.get(
                    "confidence",
                    0
                )
                * 0.20
            )

            # Technical Ranking
            score += (
                stock.get(
                    "ranking_score",
                    0
                )
                * 0.15
            )

            # Fundamental
            score += (
                stock.get(
                    "fundamental_score",
                    0
                )
                * 0.10
            )

            # =================================================
            # VALUATION
            # =================================================

            valuation_label = stock.get(
                "valuation_label",
                "TIDAK DIKETAHUI"
            )

            valuation_reliability = stock.get(
                "valuation_reliability",
                "LOW"
            )

            if valuation_label == "SANGAT MURAH":
                valuation_score = 100

            elif valuation_label == "MURAH":
                valuation_score = 90

            elif valuation_label == "WAJAR":
                valuation_score = 70

            elif valuation_label == "MAHAL":
                valuation_score = 30

            elif valuation_label == "SANGAT MAHAL":
                valuation_score = 5

            else:
                valuation_score = 50

            if valuation_reliability == "HIGH":
                reliability_factor = 1.00

            elif valuation_reliability == "MEDIUM":
                reliability_factor = 0.70

            else:
                reliability_factor = 0.40

            valuation_score = (
                50
                +
                (
                    valuation_score - 50
                )
                * reliability_factor
            )

            valuation_score = max(
                0,
                min(
                    valuation_score,
                    100
                )
            )

            stock["buy_now_valuation_score"] = round(
                valuation_score,
                2
            )

            score += (
                valuation_score
                * 0.15
            )

            # =================================================
            # RISK REWARD
            # =================================================

            rr1 = stock.get(
                "rr1",
                0
            )

            if rr1 >= 4:
                rr_score = 100

            elif rr1 >= 3:
                rr_score = 90

            elif rr1 >= 2.5:
                rr_score = 80

            elif rr1 >= 2:
                rr_score = 70

            elif rr1 >= 1.5:
                rr_score = 40

            else:
                rr_score = 20

            score += (
                rr_score
                * 0.10
            )

            # =================================================
            # RSI TIMING
            # =================================================

            rsi = stock.get(
                "rsi",
                0
            )

            if 50 <= rsi <= 65:
                rsi_score = 100

            elif 65 < rsi <= 70:
                rsi_score = 80

            elif 45 <= rsi < 50:
                rsi_score = 70

            elif 70 < rsi <= 75:
                rsi_score = 50

            else:
                rsi_score = 20

            score += (
                rsi_score
                * 0.05
            )

            stock["buy_now_priority_score"] = round(
                score,
                2
            )

        # =================================================
        # FINAL BUY NOW QUALITY FILTER V2
        # =================================================

        for stock in final_results:

            if stock["recommendation"] not in [
                "BUY",
                "STRONG BUY"
            ]:
                continue

            buy_now_priority = stock.get(
                "buy_now_priority_score",
                0
            )

            rr1 = stock.get(
                "rr1",
                0
            )

            rsi = stock.get(
                "rsi",
                0
            )

            valuation_label = stock.get(
                "valuation_label",
                "TIDAK DIKETAHUI"
            )

            valuation_reliability = stock.get(
                "valuation_reliability",
                "LOW"
            )

            if not isinstance(
                stock.get("rejected_by"),
                list
            ):
                stock["rejected_by"] = []

            # =================================================
            # FILTER
            # =================================================

            if buy_now_priority < 75:

                stock["recommendation"] = "WATCH"

                stock["rejected_by"].append(
                    "BUY NOW Priority V2 < 75"
                )

                stock["decision_reasons"].append(
                    "BUY NOW Filter V2 : Priority < 75"
                )

            elif rr1 < 2:

                stock["recommendation"] = "WATCH"

                stock["rejected_by"].append(
                    "R:R TP1 < 2"
                )

                stock["decision_reasons"].append(
                    "BUY NOW Filter V2 : R:R TP1 < 2"
                )

            elif rsi > 75:

                stock["recommendation"] = "WATCH"

                stock["rejected_by"].append(
                    "RSI > 75"
                )

                stock["decision_reasons"].append(
                    "BUY NOW Filter V2 : RSI > 75"
                )

            elif (
                valuation_label == "SANGAT MAHAL"
                and
                valuation_reliability == "HIGH"
            ):

                stock["recommendation"] = "WATCH"

                stock["rejected_by"].append(
                    "Valuation sangat mahal (HIGH reliability)"
                )

                stock["decision_reasons"].append(
                    "BUY NOW Filter V2 : Valuation terlalu mahal"
                )

        # =================================================
        # BREAKOUT PRIORITY SCORE V2
        #
        # Decision           : 20%
        # Confidence         : 15%
        # Technical Ranking : 20%
        # Fundamental       : 10%
        # Valuation         : 10%
        # Risk Reward       : 10%
        # Relative Volume   : 10%
        # RSI Timing        : 5%
        #
        # TOTAL             : 100%
        # =================================================

        for stock in final_results:

            if stock["recommendation"] != "BREAKOUT BUY":

                stock["breakout_priority_score"] = 0
                stock["breakout_valuation_score"] = 0

                continue

            score = 0

            # =================================================
            # DECISION SCORE
            # =================================================

            score += (
                stock.get(
                    "decision_score",
                    0
                )
                * 0.20
            )

            # =================================================
            # CONFIDENCE
            # =================================================

            score += (
                stock.get(
                    "confidence",
                    0
                )
                * 0.15
            )

            # =================================================
            # TECHNICAL RANKING
            # =================================================

            score += (
                stock.get(
                    "ranking_score",
                    0
                )
                * 0.20
            )

            # =================================================
            # FUNDAMENTAL
            # =================================================

            score += (
                stock.get(
                    "fundamental_score",
                    0
                )
                * 0.10
            )

            # =================================================
            # VALUATION QUALITY
            # =================================================

            valuation_label = stock.get(
                "valuation_label",
                "TIDAK DIKETAHUI"
            )

            valuation_reliability = stock.get(
                "valuation_reliability",
                "LOW"
            )

            if valuation_label == "SANGAT MURAH":
                valuation_score = 100

            elif valuation_label == "MURAH":
                valuation_score = 90

            elif valuation_label == "WAJAR":
                valuation_score = 70

            elif valuation_label == "MAHAL":
                valuation_score = 35

            elif valuation_label == "SANGAT MAHAL":
                valuation_score = 10

            else:
                valuation_score = 50

            # Reliability factor

            if valuation_reliability == "HIGH":
                reliability_factor = 1.00

            elif valuation_reliability == "MEDIUM":
                reliability_factor = 0.70

            else:
                reliability_factor = 0.40

            # Tarik valuation score menuju netral 50
            # jika reliability rendah.

            valuation_score = (
                50
                +
                (
                    valuation_score - 50
                )
                * reliability_factor
            )

            valuation_score = max(
                0,
                min(
                    valuation_score,
                    100
                )
            )

            stock[
                "breakout_valuation_score"
            ] = round(
                valuation_score,
                2
            )

            score += (
                valuation_score
                * 0.10
            )

            # =================================================
            # RISK REWARD QUALITY
            # =================================================

            rr1 = stock.get(
                "rr1",
                0
            )

            if rr1 >= 4:
                rr_score = 100

            elif rr1 >= 3:
                rr_score = 90

            elif rr1 >= 2.5:
                rr_score = 80

            elif rr1 >= 2:
                rr_score = 70

            elif rr1 >= 1.5:
                rr_score = 40

            else:
                rr_score = 20

            score += (
                rr_score
                * 0.10
            )

            # =================================================
            # RELATIVE VOLUME
            # =================================================

            rvol = stock.get(
                "relative_volume",
                0
            )

            rvol_score = min(
                rvol * 20,
                100
            )

            score += (
                rvol_score
                * 0.10
            )

            # =================================================
            # RSI TIMING
            # =================================================

            rsi = stock.get(
                "rsi",
                0
            )

            if 55 <= rsi <= 70:
                rsi_score = 100

            elif 50 <= rsi < 55:
                rsi_score = 80

            elif 70 < rsi <= 75:
                rsi_score = 70

            elif 75 < rsi <= 80:
                rsi_score = 50

            else:
                rsi_score = 20

            score += (
                rsi_score
                * 0.05
            )

            # =================================================
            # FINAL BREAKOUT PRIORITY V2
            # =================================================

            stock[
                "breakout_priority_score"
            ] = round(
                score,
                2
            )

        # =================================================
        # FINAL BREAKOUT QUALITY FILTER V2
        # =================================================

        for stock in final_results:

            if stock["recommendation"] != "BREAKOUT BUY":
                continue

            breakout_priority = stock.get(
                "breakout_priority_score",
                0
            )

            rr1 = stock.get(
                "rr1",
                0
            )

            rsi = stock.get(
                "rsi",
                0
            )

            valuation_label = stock.get(
                "valuation_label",
                "TIDAK DIKETAHUI"
            )

            valuation_reliability = stock.get(
                "valuation_reliability",
                "LOW"
            )

            if not isinstance(
                stock.get("rejected_by"),
                list
            ):
                stock["rejected_by"] = []

            # =================================================
            # QUALITY FILTER
            # =================================================

            if breakout_priority < 70:

                stock["recommendation"] = "WATCH"

                stock["rejected_by"].append(
                    "Breakout Priority V2 < 70"
                )

                stock["decision_reasons"].append(
                    "Breakout Filter V2 : Priority < 70"
                )

            elif rr1 < 2:

                stock["recommendation"] = "WATCH"

                stock["rejected_by"].append(
                    "R:R TP1 < 2"
                )

                stock["decision_reasons"].append(
                    "Breakout Filter V2 : R:R TP1 < 2"
                )

            elif rsi > 80:

                stock["recommendation"] = "WATCH"

                stock["rejected_by"].append(
                    "RSI > 80"
                )

                stock["decision_reasons"].append(
                    "Breakout Filter V2 : RSI > 80"
                )

            # Sangat mahal hanya menjadi hard filter
            # jika valuation reliability HIGH.
            #
            # Jika reliability MEDIUM / LOW,
            # valuation hanya mempengaruhi priority score.

            elif (
                valuation_label == "SANGAT MAHAL"
                and
                valuation_reliability == "HIGH"
            ):

                stock["recommendation"] = "WATCH"

                stock["rejected_by"].append(
                    "Valuation sangat mahal (HIGH reliability)"
                )

                stock["decision_reasons"].append(
                    "Breakout Filter V2 : Valuation terlalu mahal"
                )

        # =================================================
        # BUY ON WEAKNESS PRIORITY SCORE V2
        #
        # Decision           : 20%
        # Confidence         : 15%
        # Technical Ranking  : 20%
        # Fundamental        : 10%
        # Valuation          : 15%
        # Risk Reward        : 10%
        # Relative Volume    : 5%
        # RSI Timing         : 5%
        #
        # TOTAL              : 100%
        # =================================================

        for stock in final_results:

            if stock["recommendation"] != "BUY ON WEAKNESS":

                stock["bow_priority_score"] = 0
                stock["valuation_priority_score"] = 0

                continue

            score = 0

            # =================================================
            # DECISION SCORE
            # =================================================

            score += (
                stock["decision_score"]
                * 0.20
            )

            # =================================================
            # CONFIDENCE
            # =================================================

            score += (
                stock["confidence"]
                * 0.15
            )

            # =================================================
            # TECHNICAL RANKING
            # =================================================

            score += (
                stock["ranking_score"]
                * 0.20
            )

            # =================================================
            # FUNDAMENTAL
            # =================================================

            score += (
                stock["fundamental_score"]
                * 0.10
            )

            # =================================================
            # VALUATION QUALITY
            # =================================================

            valuation_label = stock.get(
                "valuation_label",
                "TIDAK DIKETAHUI"
            )

            valuation_reliability = stock.get(
                "valuation_reliability",
                "LOW"
            )

            # Nilai dasar valuation

            if valuation_label == "SANGAT MURAH":
                valuation_score = 100

            elif valuation_label == "MURAH":
                valuation_score = 85

            elif valuation_label == "WAJAR":
                valuation_score = 65

            elif valuation_label == "MAHAL":
                valuation_score = 35

            elif valuation_label == "SANGAT MAHAL":
                valuation_score = 10

            else:
                valuation_score = 50

            # =================================================
            # RELIABILITY ADJUSTMENT
            #
            # Valuation yang kurang dapat dipercaya
            # ditarik mendekati nilai netral 50.
            # =================================================

            if valuation_reliability == "HIGH":

                reliability_factor = 1.00

            elif valuation_reliability == "MEDIUM":

                reliability_factor = 0.75

            else:

                reliability_factor = 0.50

            valuation_score = (
                50
                +
                (
                    valuation_score - 50
                )
                * reliability_factor
            )

            valuation_score = max(
                0,
                min(
                    valuation_score,
                    100
                )
            )

            stock["valuation_priority_score"] = round(
                valuation_score,
                2
            )

            score += (
                valuation_score
                * 0.15
            )

            # =================================================
            # RISK REWARD QUALITY
            # =================================================

            rr1 = stock.get(
                "rr1",
                0
            )

            if rr1 >= 4:
                rr_score = 100

            elif rr1 >= 3:
                rr_score = 90

            elif rr1 >= 2.5:
                rr_score = 80

            elif rr1 >= 2:
                rr_score = 70

            elif rr1 >= 1.5:
                rr_score = 40

            else:
                rr_score = 20

            score += (
                rr_score
                * 0.10
            )

            # =================================================
            # RELATIVE VOLUME
            # =================================================

            rvol_score = min(
                stock.get(
                    "relative_volume",
                    0
                ) * 20,
                100
            )

            score += (
                rvol_score
                * 0.05
            )

            # =================================================
            # RSI TIMING
            # =================================================

            rsi = stock.get(
                "rsi",
                0
            )

            if 55 <= rsi <= 70:
                rsi_score = 100

            elif 50 <= rsi < 55:
                rsi_score = 80

            elif 70 < rsi <= 75:
                rsi_score = 60

            elif 75 < rsi <= 80:
                rsi_score = 40

            else:
                rsi_score = 20

            score += (
                rsi_score
                * 0.05
            )

            # =================================================
            # FINAL BOW PRIORITY
            # =================================================

            stock["bow_priority_score"] = round(
                score,
                2
            )

        # =================================================
        # FINAL BUY ON WEAKNESS QUALITY FILTER
        # =================================================

        for stock in final_results:

            if stock["recommendation"] != "BUY ON WEAKNESS":
                continue

            bow_priority = stock.get(
                "bow_priority_score",
                0
            )

            rr1 = stock.get(
                "rr1",
                0
            )

            rsi = stock.get(
                "rsi",
                0
            )

            stock["rejected_by"] = []

            # =============================================
            # QUALITY FILTER
            # =============================================

            if bow_priority < 70:

                stock["recommendation"] = "WATCH"

                stock["rejected_by"].append(
                    "BOW Priority < 70"
                )

                stock["decision_reasons"].append(
                    "BOW Filter : Priority < 70"
                )

                
            elif rr1 < 2:

                stock["recommendation"] = "WATCH"

                stock["rejected_by"].append(
                    "R:R TP1 < 2"
                )

                stock["decision_reasons"].append(
                    "BOW Filter : R:R TP1 < 2"
                )

            elif rsi > 75:

                stock["recommendation"] = "WATCH"

                stock["rejected_by"].append(
                    "RSI > 75"
                )

                stock["decision_reasons"].append(
                    "BOW Filter : RSI > 75"
                )

        # =================================================
        # FINAL LIQUIDITY FILTER
        # =================================================

        allowed_liquidity = [
            "VERY LIQUID",
            "LIQUID",
            "MODERATE"
        ]

        for stock in final_results:

            # =================================================
            # CEK APAKAH SAHAM PERNAH MENJADI KANDIDAT BELI
            # =================================================

            is_buy_candidate = (

                stock["recommendation"] in [
                    "BUY",
                    "BREAKOUT BUY",
                    "BUY ON WEAKNESS"
                ]

                or bool(
                    stock.get(
                        "rejected_by",
                        []
                    )
                )
            )

            if not is_buy_candidate:
                continue

            liquidity_status = stock.get(
                "liquidity_status",
                "ILLIQUID"
            )

            if liquidity_status not in allowed_liquidity:

                stock["recommendation"] = "WATCH"

                if not isinstance(
                    stock.get("rejected_by"),
                    list
                ):

                    stock["rejected_by"] = []

                stock["rejected_by"].append(
                    f"Liquidity : {liquidity_status}"
                )

                stock["decision_reasons"].append(
                    f"Liquidity Filter : {liquidity_status}"
                )

        # =================================================
        # SORT FINAL
        #
        # Prioritas:
        # 1. Final recommendation
        # 2. Decision score
        # 3. Technical ranking
        # =================================================

        priority = {

            "STRONG BUY": 7,
            "BREAKOUT BUY": 6,
            "BUY": 5,
            "BUY ON WEAKNESS": 4,
            "WATCH": 3,
            "WAIT": 2,
            "AVOID": 1

        }

        # =================================================
        # WATCHLIST PRIORITY / NEAR BUY V1
        # =================================================

        for stock in final_results:

            watchlist_result = WatchlistPriorityEngine.calculate(

                decision_score=stock.get(
                    "decision_score",
                    0
                ),

                confidence=stock.get(
                    "confidence",
                    0
                ),

                technical_ranking=stock.get(
                    "ranking_score",
                    0
                ),

                fundamental_score=stock.get(
                    "fundamental_score",
                    0
                ),

                rsi=stock.get(
                    "rsi",
                    0
                ),

                relative_volume=stock.get(
                    "relative_volume",
                    0
                ),

                liquidity_status=stock.get(
                    "liquidity_status",
                    "ILLIQUID"
                ),

                entry_recommendation=stock.get(
                    "entry_recommendation",
                    "WAIT"
                ),

                distance_entry_high=stock.get(
                    "distance_from_entry_high",
                    999
                ),

                breakout_status=stock.get(
                    "breakout",
                    "Belum Breakout"
                )
            )

            stock["watchlist_priority_score"] = (
                watchlist_result["score"]
            )

            stock["watchlist_status"] = (
                watchlist_result["status"]
            )

            stock["watchlist_reasons"] = (
                watchlist_result["reasons"]
            )

        final_results.sort(

            key=lambda x: (

                priority.get(
                    x[
                        "recommendation"
                    ],
                    0
                ),

                x[
                    "decision_score"
                ],

                x[
                    "ranking_score"
                ]

            ),

            reverse=True

        )

        return final_results

    # =====================================================
    # PRINT REPORT
    # =====================================================

    @staticmethod
    def print_report(
        results,
        limit=10
    ):

        print()
        print("=" * 70)
        print("AI TRADER INDONESIA")
        print("REKOMENDASI SAHAM HARI INI")
        print("=" * 70)

        if not results:

            print()
            print("Tidak ada rekomendasi.")

            return

        # =================================================
        # KELOMPOKKAN REKOMENDASI
        # =================================================

        buy_now = []

        breakout_buy = []

        buy_on_weakness = []

        watch_wait = []


        for stock in results:

            final_recommendation = (
                stock.get(
                    "recommendation",
                    ""
                )
            )

            entry_recommendation = (
                stock.get(
                    "entry_recommendation",
                    ""
                )
            )

            # =============================================
            # BUY SEKARANG
            # =============================================

            if (
                entry_recommendation == "BUY"
                and
                final_recommendation in [
                    "BUY",
                    "STRONG BUY"
                ]
            ):

                buy_now.append(
                    stock
                )

            # =============================================
            # BREAKOUT BUY
            # =============================================

            elif (
                entry_recommendation == "BREAKOUT BUY"
                and
                final_recommendation == "BREAKOUT BUY"
            ):

                breakout_buy.append(
                    stock
                )

            # =============================================
            # BUY ON WEAKNESS
            # =============================================

            elif (
                final_recommendation
                == "BUY ON WEAKNESS"
            ):

                buy_on_weakness.append(
                    stock
                )

            # =============================================
            # WATCH / WAIT
            # =============================================

            else:

                watch_wait.append(
                    stock
                )

        # =================================================
        # FUNCTION PRINT STOCK
        # =================================================

        def print_stock(
            stock,
            index
        ):

            print()
            print("-" * 70)

            print(
                f"{index}. {stock['code']}"
            )

            print("-" * 70)

            print(
                "Final Recommendation :",
                stock["recommendation"]
            )

            print(
                "Decision Score       :",
                stock["decision_score"]
            )

            # =================================================
            # BUY NOW PRIORITY V2
            #
            # Tetap tampilkan score meskipun kandidat BUY
            # akhirnya berubah menjadi WATCH.
            # =================================================

            buy_now_priority = stock.get(
                "buy_now_priority_score",
                0
            )

            if buy_now_priority > 0:

                print(
                    "BUY NOW Priority V2 :",
                    buy_now_priority
                )

                print(
                    "Valuation Priority  :",
                    stock.get(
                        "buy_now_valuation_score",
                        0
                    )
                )

            # =================================================
            # BREAKOUT PRIORITY V2
            #
            # Tetap tampilkan score meskipun kandidat breakout
            # akhirnya berubah menjadi WATCH.
            # =================================================

            breakout_priority = stock.get(
                "breakout_priority_score",
                0
            )

            if breakout_priority > 0:

                print(
                    "Breakout Priority V2:",
                    breakout_priority
                )

                print(
                    "Valuation Priority  :",
                    stock.get(
                        "breakout_valuation_score",
                        0
                    )
                )

            if stock.get(
                "recommendation"
            ) == "BUY ON WEAKNESS":

                print(
                    "BOW Priority V2     :",
                    stock.get(
                        "bow_priority_score",
                        0
                    )
                )

                print(
                    "Valuation Priority  :",
                    stock.get(
                        "valuation_priority_score",
                        0
                    )
                )

            print(
                "Confidence           :",
                stock["confidence"],
                stock["confidence_level"]
            )

            print(
                "Technical Ranking    :",
                stock["ranking_score"]
            )

            print(
                "Fundamental Score    :",
                stock["fundamental_score"]
            )

            print()

            # =============================================
            # VALUATION V3.2
            # =============================================

            print(
                "Fair Value           :",
                stock.get(
                    "fair_value",
                    0
                )
            )

            print(
                "Estimated Fair Value :",
                stock.get(
                    "estimated_fair_value",
                    0
                )
            )

            print(
                "Price / Fair Value   :",
                stock.get(
                    "price_to_fair_value",
                    0
                ),
                "%"
            )

            print(
                "Margin of Safety     :",
                stock.get(
                    "margin_of_safety",
                    0
                ),
                "%"
            )

            print(
                "Valuation            :",
                stock.get(
                    "valuation_label",
                    "TIDAK DIKETAHUI"
                )
            )

            print(
                "Valuation Method     :",
                stock.get(
                    "valuation_method",
                    "NONE"
                )
            )

            print(
                "Valuation Confidence :",
                stock.get(
                    "valuation_confidence",
                    "LOW"
                )
            )

            print(
                "Valuation Reliability:",
                stock.get(
                    "valuation_reliability",
                    "LOW"
                )
            )

            if stock.get(
                "fair_value_capped",
                False
            ):

                print(
                    "Fair Value Capped    : YES"
                )

            warnings = stock.get(
                "valuation_warnings",
                []
            )

            if warnings:

                print(
                    "Valuation Warnings   :"
                )

                for warning in warnings:

                    print(
                        "  -",
                        warning
                    )

            print()

            print(
                "Current Price        :",
                stock["price"]
            )

            print(
                "Entry Zone           :",
                stock["entry_low"],
                "-",
                stock["entry_high"]
            )

            print(
                "Average Entry        :",
                stock["average_entry"]
            )

            print(
                "Stop Loss            :",
                stock["stop_loss"]
            )

            print(
                "Take Profit 1        :",
                stock["target1"]
            )

            print(
                "Take Profit 2        :",
                stock["target2"]
            )

            print(
                "R:R TP1              :",
                stock["rr1"]
            )

            print(
                "R:R TP2              :",
                stock["rr2"]
            )

            print()

            print(
                "Trend                :",
                stock["trend"]
            )

            print(
                "Momentum             :",
                stock["momentum"]
            )

            print(
                "RSI                  :",
                stock["rsi"]
            )

            print(
                "MACD                 :",
                stock["macd"]
            )

            print(
                "Volume               :",
                stock["volume"]
            )

            print(
                "Relative Volume      :",
                stock["relative_volume"]
            )

            print(
                "Breakout             :",
                stock["breakout"]
            )

            print()

            print(
                "Support              :",
                stock["support"]
            )

            print(
                "Resistance           :",
                stock["resistance"]
            )

            print(
                "Entry Status         :",
                stock["entry_status"]
            )

            print(
                "Entry Recommendation :",
                stock["entry_recommendation"]
            )

            print(
                "Entry Reason         :",
                stock["entry_reason"]
            )

            print(
                "Distance Entry High  :",
                stock.get(
                    "distance_from_entry_high",
                    0
                ),
                "%"
            )

            print()

            print(
                "Liquidity Status     :",
                stock.get(
                    "liquidity_status",
                    "-"
                )
            )

            avg_transaction = stock.get(
                "average_transaction_value_20",
                0
            )

            print(
                "Avg Transaction 20D  :",
                f"Rp {avg_transaction / 1_000_000_000:.2f} B"
            )

            rejected_by = stock.get(
                "rejected_by",
                []
            )

            if rejected_by:

                print(
                    "Rejected By          :"
                )

                for reason in rejected_by:

                    print(
                        "  -",
                        reason
                    )

        # =================================================
        # BUY NOW
        # =================================================

        print()
        print("=" * 70)
        print("BUY NOW")
        print("=" * 70)

        if buy_now:

            for index, stock in enumerate(
                buy_now[:limit],
                start=1
            ):

                print_stock(
                    stock,
                    index
                )

        else:

            print()
            print(
                "Tidak ada saham yang berada "
                "di zona BUY saat ini."
            )

        # =================================================
        # BREAKOUT BUY
        # =================================================

        print()
        print("=" * 70)
        print("BREAKOUT BUY")
        print("=" * 70)

        if breakout_buy:

        
            breakout_buy.sort(

                key=lambda x:
                x.get(
                    "breakout_priority_score",
                    0
                ),

                reverse=True

            )
            
            for index, stock in enumerate(
                breakout_buy[:limit],
                start=1
            ):

                print_stock(
                    stock,
                    index
                )

        else:

            print()
            print(
                "Tidak ada valid breakout "
                "untuk dibeli saat ini."
            )

        # =================================================
        # BUY ON WEAKNESS
        # =================================================

        print()
        print("=" * 70)
        print("BUY ON WEAKNESS")
        print("=" * 70)

        if buy_on_weakness:

            buy_on_weakness.sort(

                key=lambda x:
                x.get(
                    "bow_priority_score",
                    0
                ),

                reverse=True

            )

            for index, stock in enumerate(
                buy_on_weakness[:limit],
                start=1
            ):

                print_stock(
                    stock,
                    index
                )

        else:

            print()
            print(
                "Tidak ada kandidat "
                "BUY ON WEAKNESS."
            )

        # =================================================
        # WATCH / WAIT
        # =================================================

        print()
        print("=" * 70)
        print("WATCH / WAIT")
        print("=" * 70)

        if watch_wait:

            for index, stock in enumerate(
                watch_wait[:limit],
                start=1
            ):

                print_stock(
                    stock,
                    index
                )

        else:

            print()
            print(
                "Tidak ada kandidat "
                "WATCH / WAIT."
            )

        # =================================================
        # TOP LQ45
        # =================================================

        lq45_stocks = [

            stock

            for stock in results

            if stock.get(
                "is_lq45",
                False
            )

        ]

        lq45_stocks.sort(

            key=lambda x: (

                x["decision_score"],
                x["ranking_score"]

            ),

            reverse=True

        )

        print()
        print("=" * 70)
        print("TOP LQ45")
        print("=" * 70)

        if lq45_stocks:

            for index, stock in enumerate(
                lq45_stocks[:limit],
                start=1
            ):

                print_stock(
                    stock,
                    index
                )

        else:

            print()
            print(
                "Tidak ada saham LQ45 "
                "di kandidat deep analysis hari ini."
            )


        # =================================================
        # TOP IDX30
        # =================================================

        idx30_stocks = [

            stock

            for stock in results

            if stock.get(
                "is_idx30",
                False
            )

        ]

        idx30_stocks.sort(

            key=lambda x: (

                x["decision_score"],
                x["ranking_score"]

            ),

            reverse=True

        )

        print()
        print("=" * 70)
        print("TOP IDX30")
        print("=" * 70)

        if idx30_stocks:

            for index, stock in enumerate(
                idx30_stocks[:limit],
                start=1
            ):

                print_stock(
                    stock,
                    index
                )

        else:

            print()
            print(
                "Tidak ada saham IDX30 "
                "di kandidat deep analysis hari ini."
            )

        # =================================================
        # TOP NON INDEX
        # =================================================

        non_index_stocks = [

            stock

            for stock in results

            if not stock.get(
                "is_lq45",
                False
            )
            and
            not stock.get(
                "is_idx30",
                False
            )

        ]

        non_index_stocks.sort(

            key=lambda x: (

                x["decision_score"],
                x["ranking_score"]

            ),

            reverse=True

        )

        print()
        print("=" * 70)
        print("TOP NON INDEX")
        print("=" * 70)

        if non_index_stocks:

            for index, stock in enumerate(
                non_index_stocks[:limit],
                start=1
            ):

                print_stock(
                    stock,
                    index
                )

        else:

            print()
            print(
                "Tidak ada saham NON INDEX "
                "di kandidat hari ini."
            )


        # =================================================
        # SUMMARY
        # =================================================

        print()
        print("=" * 70)
        print("DAILY RECOMMENDATION SUMMARY")
        print("=" * 70)

        print(
            "BUY NOW        :",
            len(buy_now)
        )

        print(
            "BREAKOUT BUY   :",
            len(breakout_buy)
        )

        print(
            "BUY ON WEAKNESS:",
            len(buy_on_weakness)
        )

        print(
            "WATCH / WAIT   :",
            len(watch_wait)
        )

        print(
            "TOTAL ANALYSIS :",
            len(results)
        )

        print()
        print("=" * 70)
        print("DAILY RECOMMENDATION SELESAI")
        print("=" * 70)

    # =====================================================
    # FINAL DAILY SHORTLIST
    # =====================================================

    @staticmethod
    def print_shortlist(results):

        print()
        print("=" * 70)
        print("FINAL DAILY SHORTLIST")
        print("=" * 70)

        shortlist = [

            stock

            for stock in results

            if stock["recommendation"] in [
                "BUY",
                "BREAKOUT BUY",
                "BUY ON WEAKNESS"
            ]

        ]

        if not shortlist:

            print()
            print("Tidak ada kandidat utama hari ini.")
            return

        for index, stock in enumerate(
            shortlist,
            start=1
        ):

            print()
            print("-" * 70)
            print(
                f"{index}. {stock['code']}"
            )
            print("-" * 70)

            print(
                "Recommendation :",
                stock["recommendation"]
            )

            if stock["recommendation"] == "BREAKOUT BUY":

                print(
                    "Priority       :",
                    stock.get(
                        "breakout_priority_score",
                        0
                    )
                )

            elif stock["recommendation"] == "BUY ON WEAKNESS":

                print(
                    "Priority       :",
                    stock.get(
                        "bow_priority_score",
                        0
                    )
                )

            print(
                "Decision Score  :",
                stock["decision_score"]
            )

            print(
                "Confidence      :",
                stock["confidence"],
                stock["confidence_level"]
            )

            print(
                "Current Price   :",
                stock["price"]
            )

            print(
                "Entry Zone      :",
                stock["entry_low"],
                "-",
                stock["entry_high"]
            )

            print(
                "Stop Loss       :",
                stock["stop_loss"]
            )

            print(
                "Take Profit 1   :",
                stock["target1"]
            )

            print(
                "Take Profit 2   :",
                stock["target2"]
            )

            print(
                "R:R TP1         :",
                stock["rr1"]
            )

            print(
                "R:R TP2         :",
                stock["rr2"]
            )

            print(
                "RSI             :",
                stock["rsi"]
            )

            print(
                "Relative Volume :",
                stock["relative_volume"]
            )

            print(
                "Trend           :",
                stock["trend"]
            )

            print(
                "MACD            :",
                stock["macd"]
            )

            print(
                "Entry Reason    :",
                stock["entry_reason"]
            )

        print()
        print("=" * 70)
        print(
            "TOTAL SHORTLIST :",
            len(shortlist)
        )
        print("=" * 70)

    # =====================================================
    # TOP WATCHLIST PRIORITY / NEAR BUY
    # =====================================================

    @staticmethod
    def print_watchlist_priority(
        results,
        limit=5
    ):

        print()
        print("=" * 70)
        print("TOP WATCHLIST PRIORITY / NEAR BUY")
        print("=" * 70)

        candidates = [

            stock

            for stock in results

            if stock.get(
                "watchlist_status",
                "WATCH"
            ) in [
                "NEAR BUY",
                "WATCHLIST PRIORITY"
            ]

            and stock.get(
                "recommendation",
                ""
            ) not in [
                "BUY",
                "BREAKOUT BUY",
                "BUY ON WEAKNESS"
            ]

            and stock.get(
                "liquidity_status",
                "ILLIQUID"
            ) in [
                "VERY LIQUID",
                "LIQUID",
                "MODERATE"
            ]

        ]

        candidates.sort(

            key=lambda x:
            x.get(
                "watchlist_priority_score",
                0
            ),

            reverse=True

        )

        if not candidates:

            print()
            print(
                "Tidak ada kandidat NEAR BUY "
                "atau WATCHLIST PRIORITY."
            )
            return

        for index, stock in enumerate(
            candidates[:limit],
            start=1
        ):

            print()
            print("-" * 70)

            print(
                f"{index}. {stock['code']}"
            )

            print("-" * 70)

            print(
                "Status          :",
                stock.get(
                    "watchlist_status",
                    "-"
                )
            )

            print(
                "Priority Score  :",
                stock.get(
                    "watchlist_priority_score",
                    0
                )
            )

            print(
                "Decision Score  :",
                stock.get(
                    "decision_score",
                    0
                )
            )

            print(
                "Confidence      :",
                stock.get(
                    "confidence",
                    0
                ),
                stock.get(
                    "confidence_level",
                    "-"
                )
            )

            print(
                "Current Price   :",
                stock.get(
                    "price",
                    0
                )
            )

            print(
                "Entry Zone      :",
                stock.get(
                    "entry_low",
                    0
                ),
                "-",
                stock.get(
                    "entry_high",
                    0
                )
            )

            print(
                "Distance Entry  :",
                stock.get(
                    "distance_from_entry_high",
                    0
                ),
                "%"
            )

            print(
                "RSI             :",
                stock.get(
                    "rsi",
                    0
                )
            )

            print(
                "Relative Volume :",
                stock.get(
                    "relative_volume",
                    0
                )
            )

            print(
                "Liquidity       :",
                stock.get(
                    "liquidity_status",
                    "-"
                )
            )

            print(
                "Trend           :",
                stock.get(
                    "trend",
                    "-"
                )
            )

            print(
                "MACD            :",
                stock.get(
                    "macd",
                    "-"
                )
            )

            reasons = stock.get(
                "watchlist_reasons",
                []
            )

            if reasons:

                print(
                    "Reasons         :",
                    ", ".join(reasons)
                )

        print()
        print("=" * 70)
        print(
            "TOTAL WATCHLIST :",
            min(
                len(candidates),
                limit
            )
        )
        print("=" * 70)

# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    engine = DailyRecommendation(

        period="1y",

        technical_limit=20

    )

    results = (
        engine.run()
    )

    engine.print_report(

        results,

        limit=10

    )

    engine.print_shortlist(
        results
    )

    engine.print_watchlist_priority(
        results,
        limit=5
    )