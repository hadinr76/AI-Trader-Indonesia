import yfinance as yf


class FundamentalEngine:

    @staticmethod
    def analyze(kode):

        ticker = yf.Ticker(kode + ".JK")

        info = ticker.info

        return {

            "per": info.get("trailingPE", 0),

            "pbv": info.get("priceToBook", 0),

            "roe": info.get("returnOnEquity", 0),

            "roa": info.get("returnOnAssets", 0),

            "der": info.get("debtToEquity", 0),

            "eps": info.get("trailingEps", 0),

            "market_cap": info.get("marketCap", 0),

            "dividend_yield": info.get("dividendYield", 0),

            "sector": info.get("sector", "-"),

            "industry": info.get("industry", "-")
        }