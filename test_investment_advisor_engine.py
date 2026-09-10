from engine.investment_advisor_engine import InvestmentAdvisorEngine

print("=" * 60)
print("INVESTMENT ADVISOR ENGINE TEST")
print("=" * 60)

data = {

    "code": "BBCA",

    "trend": "Bullish",

    "mtf_status": "VERY STRONG BULLISH",

    "macd": "Bullish Cross",

    "rsi": 82.46,

    "rr2": 5.49,

    "confidence": 60,

    "recommendation": "WAIT PULLBACK",

    "ranking_score": 63.1

}

hasil = InvestmentAdvisorEngine.generate(data)

print()

for i, item in enumerate(hasil, start=1):

    print(f"{i}. {item}")