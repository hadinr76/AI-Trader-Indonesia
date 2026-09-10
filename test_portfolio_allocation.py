from engine.portfolio_engine import PortfolioEngine

print("=" * 60)
print("PORTFOLIO ENGINE TEST")
print("=" * 60)

scanner_result = [

    {
        "code":"TINS",
        "ranking_score":92,
        "price":1400,
        "recommendation":"STRONG BUY"
    },

    {
        "code":"ADRO",
        "ranking_score":86,
        "price":2300,
        "recommendation":"BUY"
    },

    {
        "code":"ISAT",
        "ranking_score":82,
        "price":2500,
        "recommendation":"BUY"
    },

    {
        "code":"LSIP",
        "ranking_score":80,
        "price":1150,
        "recommendation":"BUY"
    },

    {
        "code":"INDF",
        "ranking_score":78,
        "price":7600,
        "recommendation":"BUY"
    }

]

portfolio = PortfolioEngine.allocate(scanner_result)

for item in portfolio:

    print("-" * 60)

    print("Kode          :", item["code"])

    print("Ranking       :", item["ranking_score"])

    print("Recommendation:", item["recommendation"])

    print("Weight        :", str(item["weight"]) + "%")

    print("Allocation    : Rp{:,.0f}".format(item["allocation"]))

    print("Price         : Rp{:,.0f}".format(item["price"]))

    print("Shares        :", item["shares"])

    print("Lots          :", item["lots"])

    print("Investment    : Rp{:,.0f}".format(item["investment"]))

    print("Remaining     : Rp{:,.0f}".format(item["remaining"]))