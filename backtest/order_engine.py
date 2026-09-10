class OrderEngine:
    """
    Mengatur validasi order BUY dan SELL.
    """

    @staticmethod
    def has_open_position(portfolio, code):
        """
        Mengecek apakah masih ada posisi OPEN
        pada kode saham tertentu.
        """

        for position in portfolio:

            if (
                position.code == code
                and position.status == "OPEN"
            ):

                return True

        return False

    # =====================================================
    # BUY
    # =====================================================

    @classmethod
    def can_buy(cls, portfolio, code):

        return not cls.has_open_position(

            portfolio,

            code

        )

    # =====================================================
    # SELL
    # =====================================================

    @classmethod
    def can_sell(cls, portfolio, code):

        return cls.has_open_position(

            portfolio,

            code

        )

    # =====================================================
    # Ambil posisi yang masih OPEN
    # =====================================================

    @staticmethod
    def get_open_position(portfolio, code):

        for position in portfolio:

            if (

                position.code == code

                and

                position.status == "OPEN"

            ):

                return position

        return None

    # =====================================================
    # Jumlah posisi OPEN
    # =====================================================

    @staticmethod
    def count_open_position(portfolio):

        total = 0

        for position in portfolio:

            if position.status == "OPEN":

                total += 1

        return total

    # =====================================================
    # Semua posisi OPEN
    # =====================================================

    @staticmethod
    def get_all_open_position(portfolio):

        result = []

        for position in portfolio:

            if position.status == "OPEN":

                result.append(position)

        return result