from engine.ai_engine import AIEngine


class ScannerEngine:

    @staticmethod
    def scan(kode):

        try:

            hasil = AIEngine.analyze(kode)

            return hasil

        except Exception as e:

            print(f"Error {kode}: {e}")

            return None