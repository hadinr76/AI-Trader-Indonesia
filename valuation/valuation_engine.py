class ValuationEngine:

    # =====================================================
    # SECTOR MULTIPLES
    # =====================================================

    @staticmethod
    def get_sector_profile(
        sector,
        industry="-"
    ):

        sector = str(
            sector or ""
        ).lower()

        industry = str(
            industry or ""
        ).lower()

        profile = {
            "base_per": 12,
            "base_pbv": 1.5,
            "per_weight": 0.60,
            "pbv_weight": 0.40
        }

        # =================================================
        # FINANCIAL / BANK
        # =================================================

        if (
            "financial" in sector
            or "bank" in industry
        ):

            profile = {
                "base_per": 13,
                "base_pbv": 1.8,
                "per_weight": 0.30,
                "pbv_weight": 0.70
            }

        # =================================================
        # ENERGY / COAL
        # =================================================

        elif (
            "energy" in sector
            or "coal" in industry
        ):

            profile = {
                "base_per": 8,
                "base_pbv": 1.3,
                "per_weight": 0.80,
                "pbv_weight": 0.20
            }

        # =================================================
        # CONSUMER DEFENSIVE
        # =================================================

        elif "consumer defensive" in sector:

            profile = {
                "base_per": 16,
                "base_pbv": 2.5,
                "per_weight": 0.70,
                "pbv_weight": 0.30
            }

        # =================================================
        # CONSUMER CYCLICAL
        # =================================================

        elif "consumer cyclical" in sector:

            profile = {
                "base_per": 14,
                "base_pbv": 2.0,
                "per_weight": 0.70,
                "pbv_weight": 0.30
            }

        # =================================================
        # COMMUNICATION
        # =================================================

        elif "communication" in sector:

            profile = {
                "base_per": 14,
                "base_pbv": 2.0,
                "per_weight": 0.60,
                "pbv_weight": 0.40
            }

        # =================================================
        # TECHNOLOGY
        # =================================================

        elif "technology" in sector:

            profile = {
                "base_per": 18,
                "base_pbv": 2.5,
                "per_weight": 0.70,
                "pbv_weight": 0.30
            }

        # =================================================
        # HEALTHCARE
        # =================================================

        elif "healthcare" in sector:

            profile = {
                "base_per": 17,
                "base_pbv": 2.5,
                "per_weight": 0.70,
                "pbv_weight": 0.30
            }

        # =================================================
        # INDUSTRIALS
        # =================================================

        elif "industrials" in sector:

            profile = {
                "base_per": 13,
                "base_pbv": 1.8,
                "per_weight": 0.70,
                "pbv_weight": 0.30
            }

        # =================================================
        # BASIC MATERIALS
        # =================================================

        elif "basic materials" in sector:

            profile = {
                "base_per": 10,
                "base_pbv": 1.5,
                "per_weight": 0.60,
                "pbv_weight": 0.40
            }

        # =================================================
        # REAL ESTATE
        # =================================================

        elif "real estate" in sector:

            profile = {
                "base_per": 12,
                "base_pbv": 1.2,
                "per_weight": 0.30,
                "pbv_weight": 0.70
            }

        # =================================================
        # UTILITIES
        # =================================================

        elif "utilities" in sector:

            profile = {
                "base_per": 13,
                "base_pbv": 1.5,
                "per_weight": 0.60,
                "pbv_weight": 0.40
            }

        return profile

    # =====================================================
    # ROE FACTOR
    # =====================================================

    @staticmethod
    def get_roe_factor(
        roe
    ):

        roe = float(
            roe or 0
        )

        if roe >= 0.25:
            return 1.20

        if roe >= 0.20:
            return 1.15

        if roe >= 0.15:
            return 1.10

        if roe >= 0.10:
            return 1.00

        if roe >= 0.05:
            return 0.90

        if roe > 0:
            return 0.80

        return 0.70

    # =====================================================
    # VALUATION LABEL
    # =====================================================

    @staticmethod
    def get_valuation_label(
        price_to_fair_value
    ):

        if price_to_fair_value <= 0:

            return (
                "UNKNOWN",
                "TIDAK DIKETAHUI"
            )

        if price_to_fair_value <= 70:

            return (
                "VERY UNDERVALUED",
                "SANGAT MURAH"
            )

        if price_to_fair_value <= 85:

            return (
                "UNDERVALUED",
                "MURAH"
            )

        if price_to_fair_value <= 110:

            return (
                "FAIRLY VALUED",
                "WAJAR"
            )

        if price_to_fair_value <= 130:

            return (
                "OVERVALUED",
                "MAHAL"
            )

        return (
            "VERY OVERVALUED",
            "SANGAT MAHAL"
        )

    # =====================================================
    # CALCULATE
    # =====================================================

    @staticmethod
    def calculate(
        price,
        eps,
        pbv,
        per,
        roe=0,
        sector="-",
        industry="-"
    ):

        # =================================================
        # NORMALIZATION
        # =================================================

        price = float(
            price or 0
        )

        eps = float(
            eps or 0
        )

        pbv = float(
            pbv or 0
        )

        per = float(
            per or 0
        )

        roe = float(
            roe or 0
        )

        warnings = []

        # =================================================
        # BASIC VALIDATION
        # =================================================

        if price <= 0:

            return {

                "fair_per": 0,
                "fair_pbv": 0,

                "fair_value_per": 0,
                "fair_value_pbv": 0,

                "fair_value": 0,

                "price_to_fair_value": 0,
                "margin_of_safety": 0,

                "valuation_status":
                    "UNKNOWN",

                "valuation_label":
                    "TIDAK DIKETAHUI",

                "valuation_method":
                    "NONE",

                "valuation_confidence":
                    "LOW",

                "warnings": [
                    "Invalid market price"
                ],

                "sector":
                    sector,

                "industry":
                    industry

            }

        # =================================================
        # SECTOR PROFILE
        # =================================================

        profile = (
            ValuationEngine
            .get_sector_profile(
                sector,
                industry
            )
        )

        roe_factor = (
            ValuationEngine
            .get_roe_factor(
                roe
            )
        )

        fair_per = (
            profile["base_per"]
            * roe_factor
        )

        fair_pbv = (
            profile["base_pbv"]
            * roe_factor
        )

        # =================================================
        # METHOD VALIDATION
        # =================================================

        per_valid = True
        pbv_valid = True

        # PER validation
        if eps <= 0:

            per_valid = False

            warnings.append(
                "EPS negatif atau nol"
            )

        if per <= 0:

            per_valid = False

            warnings.append(
                "PER tidak tersedia"
            )

        if per > 100:

            warnings.append(
                "PER sangat tinggi"
            )

        # PBV validation
        if pbv <= 0:

            pbv_valid = False

            warnings.append(
                "PBV tidak tersedia"
            )

        elif pbv > 20:

            pbv_valid = False

            warnings.append(
                "PBV data suspicious"
            )

        if roe <= 0:

            warnings.append(
                "ROE negatif atau nol"
            )

        # =================================================
        # PER FAIR VALUE
        # =================================================

        if per_valid:

            fair_value_per = (
                eps
                * fair_per
            )

        else:

            fair_value_per = 0

        # =================================================
        # PBV FAIR VALUE
        # =================================================

        if pbv_valid:

            bvps = (
                price
                /
                pbv
            )

            fair_value_pbv = (
                bvps
                * fair_pbv
            )

        else:

            bvps = 0
            fair_value_pbv = 0

        # =================================================
        # WEIGHTS
        # =================================================

        per_weight = (
            profile["per_weight"]
        )

        pbv_weight = (
            profile["pbv_weight"]
        )

        # Jika hanya PER valid
        if (
            per_valid
            and not pbv_valid
        ):

            per_weight = 1.0
            pbv_weight = 0.0

            valuation_method = (
                "PER ONLY"
            )

        # Jika hanya PBV valid
        elif (
            pbv_valid
            and not per_valid
        ):

            per_weight = 0.0
            pbv_weight = 1.0

            valuation_method = (
                "PBV ONLY"
            )

        # Jika keduanya valid
        elif (
            per_valid
            and pbv_valid
        ):

            valuation_method = (
                "PER + PBV"
            )

        else:

            valuation_method = (
                "NONE"
            )

        # =================================================
        # FAIR VALUE
        # =================================================

        if valuation_method == "NONE":

            fair_value = 0

        else:

            fair_value = (

                (
                    fair_value_per
                    * per_weight
                )

                +

                (
                    fair_value_pbv
                    * pbv_weight
                )

            )

        # =================================================
        # PRICE TO FAIR VALUE
        # =================================================

        if fair_value > 0:

            price_to_fair_value = (

                price
                /
                fair_value

            ) * 100

        else:

            price_to_fair_value = 0

        # =================================================
        # MARGIN OF SAFETY
        # =================================================

        if fair_value > 0:

            margin_of_safety = (

                (
                    fair_value
                    - price
                )
                /
                fair_value

            ) * 100

        else:

            margin_of_safety = 0

        # =================================================
        # VALUATION STATUS
        # =================================================

        (
            valuation_status,
            valuation_label
        ) = (
            ValuationEngine
            .get_valuation_label(
                price_to_fair_value
            )
        )

        # =================================================
        # CONFIDENCE
        # =================================================

        if (
            per_valid
            and pbv_valid
            and roe > 0
        ):

            valuation_confidence = (
                "HIGH"
            )

        elif (
            per_valid
            or pbv_valid
        ):

            valuation_confidence = (
                "MEDIUM"
            )

        else:

            valuation_confidence = (
                "LOW"
            )

        # Turunkan confidence jika warning berat
        if (
            "PBV data suspicious"
            in warnings
        ):

            if valuation_confidence == "HIGH":

                valuation_confidence = (
                    "MEDIUM"
                )

        if roe <= 0:

            valuation_confidence = (
                "LOW"
            )

        # =================================================
        # PROFITABILITY CONFIDENCE ADJUSTMENT
        # =================================================

        if 0 < roe < 0.05:

            warnings.append(
                "ROE sangat rendah"
            )

            if valuation_confidence == "HIGH":
                valuation_confidence = "MEDIUM"

        elif roe <= 0:

            valuation_confidence = "LOW"

        # =================================================
        # FAIR VALUE SANITY CAP
        # =================================================

        original_fair_value = fair_value
        fair_value_capped = False

        if fair_value > 0:

            if valuation_confidence == "HIGH":
                max_fair_value = price * 2.00

            elif valuation_confidence == "MEDIUM":
                max_fair_value = price * 1.60

            else:
                max_fair_value = price * 1.30

            if fair_value > max_fair_value:

                fair_value = max_fair_value
                fair_value_capped = True

                warnings.append(
                    "Fair value capped for sanity check"
                )

        # =================================================
        # RECALCULATE AFTER SANITY CAP
        # =================================================

        if fair_value > 0:

            price_to_fair_value = (
                price / fair_value
            ) * 100

            margin_of_safety = (
                (fair_value - price)
                / fair_value
            ) * 100

        else:

            price_to_fair_value = 0
            margin_of_safety = 0

        (
            valuation_status,
            valuation_label
        ) = ValuationEngine.get_valuation_label(
            price_to_fair_value
        )

        # =================================================
        # VALUATION RELIABILITY V3.2
        # =================================================

        valuation_reliability = valuation_confidence

        # Jika estimasi asli terlalu jauh dari harga pasar,
        # reliability harus diturunkan.

        if fair_value_capped:

            warnings.append(
                "Fair value estimate unusually far from market price"
            )

            if valuation_reliability == "HIGH":
                valuation_reliability = "MEDIUM"

            elif valuation_reliability == "MEDIUM":
                valuation_reliability = "LOW"


        # Profitabilitas sangat rendah
        if 0 < roe < 0.05:

            valuation_reliability = "LOW"


        # Perusahaan belum profitable
        if roe <= 0 or eps <= 0:

            valuation_reliability = "LOW"


        # Hanya satu metode valuasi yang valid
        if valuation_method in [
            "PER ONLY",
            "PBV ONLY"
        ]:

            if valuation_reliability == "HIGH":
                valuation_reliability = "MEDIUM"

        # =================================================
        # RETURN
        # =================================================

        return {

            "fair_per":
                round(
                    fair_per,
                    2
                ),

            "fair_pbv":
                round(
                    fair_pbv,
                    2
                ),

            "fair_value_per":
                round(
                    fair_value_per,
                    2
                ),

            "fair_value_pbv":
                round(
                    fair_value_pbv,
                    2
                ),

            "fair_value":
                round(
                    fair_value,
                    2
                ),

            "estimated_fair_value":
                round(
                    original_fair_value,
                    2
                ),

            "valuation_reliability":
                valuation_reliability,

            "price_to_fair_value":
                round(
                    price_to_fair_value,
                    2
                ),

            "margin_of_safety":
                round(
                    margin_of_safety,
                    2
                ),

            "valuation_status":
                valuation_status,

            "valuation_label":
                valuation_label,

            "valuation_method":
                valuation_method,

            "valuation_confidence":
                valuation_confidence,

            "per_valid":
                per_valid,

            "pbv_valid":
                pbv_valid,

            "per_weight":
                round(
                    per_weight,
                    2
                ),

            "pbv_weight":
                round(
                    pbv_weight,
                    2
                ),

            "warnings":
                warnings,

            "sector":
                sector,

            "industry":
                industry,

            "original_fair_value":
                round(
                    original_fair_value,
                    2
                ),

            "fair_value_capped":
                fair_value_capped,

            "max_fair_value":
                round(
                    max_fair_value
                    if fair_value > 0
                    else 0,
                    2
                ),

        }