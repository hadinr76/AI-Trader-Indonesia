from database.watchlist import WATCHLIST
from database.idx30 import IDX30
from database.lq45 import LQ45
from database.sectors import SECTORS
from database.stocks import STOCKS


class WatchlistManager:

    @staticmethod
    def get(mode="WATCHLIST", sector=None):

        mode = mode.upper()

        # ===============================
        # Watchlist Pribadi
        # ===============================

        if mode == "WATCHLIST":
            return WATCHLIST

        # ===============================
        # IDX30
        # ===============================

        elif mode == "IDX30":
            return IDX30

        # ===============================
        # LQ45
        # ===============================

        elif mode == "LQ45":
            return LQ45

        # ===============================
        # Seluruh IDX
        # ===============================

        elif mode == "ALL":
            return STOCKS

        # ===============================
        # Berdasarkan sektor
        # ===============================

        elif mode == "SECTOR":

            if sector is None:
                raise ValueError("Nama sektor harus diisi.")

            sector = sector.upper()

            if sector not in SECTORS:
                raise ValueError(f"Sektor '{sector}' tidak ditemukan.")

            return SECTORS[sector]

        # ===============================
        # Default
        # ===============================

        return WATCHLIST