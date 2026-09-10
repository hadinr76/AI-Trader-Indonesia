from engine.market_regime_engine import MarketRegimeEngine

print("=" * 60)
print("MARKET REGIME ENGINE TEST")
print("=" * 60)

hasil = MarketRegimeEngine.analyze()

print()

print("Market Regime :", hasil["market_regime"])
print("Trend         :", hasil["trend"])
print("MACD          :", hasil["macd"])
print("RSI           :", hasil["rsi"])