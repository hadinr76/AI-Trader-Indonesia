from engine.market_filter_engine import MarketFilterEngine

print("=" * 60)
print("MARKET FILTER ENGINE TEST")
print("=" * 60)

market = "BEAR MARKET"

hasil = MarketFilterEngine.adjust(

    regime=market,

    recommendation="BUY",

    ranking_score=86

)

print("Market        :", market)
print("Recommendation:", hasil["recommendation"])
print("Ranking Score :", hasil["ranking_score"])