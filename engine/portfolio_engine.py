class PortfolioEngine:

    @staticmethod
    def allocate(
        results,
        capital=100_000_000
    ):

        # ==================================================
        # VALIDASI
        # ==================================================

        if not results:

            return []

        # ==================================================
        # URUTKAN BERDASARKAN RANKING SCORE
        # ==================================================

        results = sorted(
            results,
            key=lambda x: x["ranking_score"],
            reverse=True
        )

        # ==================================================
        # AMBIL 5 SAHAM TERBAIK
        # ==================================================

        top = results[:5]

        # ==================================================
        # BOBOT PORTFOLIO
        # ==================================================

        weights = [
            30,
            25,
            20,
            15,
            10
        ]

        portfolio = []

        # ==================================================
        # ALLOCATION
        # ==================================================

        for stock, weight in zip(
            top,
            weights
        ):

            allocation = (
                capital *
                weight /
                100
            )

            price = float(
                stock["price"]
            )

            # ==================================================
            # VALIDASI HARGA
            # ==================================================

            if price <= 0:

                continue

            # ==================================================
            # JUMLAH SAHAM
            # ==================================================

            shares = int(
                allocation //
                price
            )

            # ==================================================
            # BULATKAN KE LOT
            # ==================================================

            lots = (
                shares //
                100
            )

            shares = (
                lots *
                100
            )

            # ==================================================
            # INVESTMENT
            # ==================================================

            investment = (
                shares *
                price
            )

            # ==================================================
            # DANA TERSISA
            # ==================================================

            remaining = (
                allocation -
                investment
            )

            # ==================================================
            # SIMPAN HASIL
            # ==================================================

            portfolio.append({

                # ------------------------------------------
                # IDENTITAS
                # ------------------------------------------

                "code":
                    stock["code"],

                "ranking_score":
                    stock["ranking_score"],

                "recommendation":
                    stock["recommendation"],

                # ------------------------------------------
                # HARGA
                # ------------------------------------------

                "price":
                    price,

                # ------------------------------------------
                # RISK MANAGEMENT
                # ------------------------------------------

                "stop_loss":
                    stock.get(
                        "stop_loss",
                        0
                    ),

                "target1":
                    stock.get(
                        "target1",
                        0
                    ),

                "target2":
                    stock.get(
                        "target2",
                        0
                    ),

                # ------------------------------------------
                # PORTFOLIO
                # ------------------------------------------

                "weight":
                    weight,

                "allocation":
                    allocation,

                "shares":
                    shares,

                "lots":
                    lots,

                "investment":
                    investment,

                "remaining":
                    remaining

            })

        return portfolio