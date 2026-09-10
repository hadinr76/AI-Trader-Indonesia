from engine.ai_engine import AIEngine


class ScannerEngine:

    @staticmethod
    def scan(watchlist):

        results = []

        for code in watchlist:

            try:

                result = AIEngine.analyze(code)

                results.append(result)

                print(f"✓ {code}")

            except Exception as e:

                print(f"✗ {code} : {e}")

        return results