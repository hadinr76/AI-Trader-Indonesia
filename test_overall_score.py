from scoring.overall_score import OverallScore

technical = 100
fundamental = 90

overall = OverallScore.calculate(
    technical,
    fundamental
)

print("=" * 50)
print("OVERALL SCORE TEST")
print("=" * 50)

print("Technical Score   :", technical)
print("Fundamental Score :", fundamental)
print("-" * 50)
print("Overall Score     :", overall)