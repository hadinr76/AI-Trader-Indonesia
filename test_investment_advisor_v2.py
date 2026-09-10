from engine.investment_advisor_v2 import InvestmentAdvisorV2

print("=" * 60)
print("INVESTMENT ADVISOR V2 TEST")
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

hasil = InvestmentAdvisorV2.generate(data)

print()
print(hasil)