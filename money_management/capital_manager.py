class CapitalManager:

    @staticmethod
    def allocate(

        capital,
        investment

    ):

        # ==========================================
        # Modal tidak boleh negatif
        # ==========================================

        if capital <= 0:

            return {

                "approved": False,

                "investment": 0,

                "remaining": 0

            }

        # ==========================================
        # Investment lebih kecil dari modal
        # ==========================================

        if investment <= capital:

            return {

                "approved": True,

                "investment": investment,

                "remaining": capital - investment

            }

        # ==========================================
        # Jika investment melebihi modal
        # ==========================================

        return {

            "approved": False,

            "investment": capital,

            "remaining": 0

        }

    # ==========================================
    # Hitung lot maksimum sesuai modal
    # ==========================================

    @staticmethod
    def adjust_lot(

        capital,
        entry_price

    ):

        if entry_price <= 0:

            return {

                "lots": 0,

                "investment": 0

            }

        max_shares = int(capital / entry_price)

        lots = max_shares // 100

        investment = lots * 100 * entry_price

        return {

            "lots": lots,

            "investment": investment

        }