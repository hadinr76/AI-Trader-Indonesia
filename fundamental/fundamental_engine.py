import yfinance as yf


class FundamentalEngine:

    @staticmethod
    def analyze(kode):

        ticker = yf.Ticker(kode + ".JK")

        try:
            info = ticker.info
        except Exception:
            return None

        hasil = {
            "per": info.get("trailingPE", 0) or 0,
            "pbv": info.get("priceToBook", 0) or 0,
            "roe": info.get("returnOnEquity", 0) or 0,
            "roa": info.get("returnOnAssets", 0) or 0,
            "der": info.get("debtToEquity", 0) or 0,
            "eps": info.get("trailingEps", 0) or 0,
            "market_cap": info.get("marketCap", 0) or 0,
            "dividend_yield": info.get("dividendYield", 0) or 0,
            "sector": info.get("sector", "-"),
            "industry": info.get("industry", "-")
        }

        return hasil