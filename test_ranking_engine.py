from ranking.ranking_engine import RankingEngine

print("=" * 60)
print("AI RANKING ENGINE TEST")
print("=" * 60)

ranking = RankingEngine.calculate(

    overall_score=87,

    confidence=92,

    rr=5.2,

    smart_signal="STRONG BUY",

    mtf_score=85

)

print("Ranking Score :", ranking)