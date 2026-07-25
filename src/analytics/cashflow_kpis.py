def free_cash_flow(
    operating_activity,
    investing_activity
):
    """
    Free Cash Flow

    Negative FCF is allowed.
    """

    return round(
        operating_activity +
        investing_activity,
        2
    )

def cfo_quality_score(
    operating_activity,
    net_profit
):

    if net_profit == 0:
        return None

    return round(
        operating_activity /
        net_profit,
        2
    )

def cfo_quality_label(score):

    if score is None:
        return "Not Available"

    if score > 1:
        return "High Quality"

    if score >= 0.5:
        return "Moderate"

    return "Accrual Risk"

def capex_intensity(
    investing_activity,
    sales
):

    if sales == 0:
        return None

    return round(
        (
            abs(investing_activity)
            /
            sales
        ) * 100,
        2
    )

def capex_label(value):

    if value is None:
        return "Not Available"

    if value < 3:
        return "Asset Light"

    if value <= 8:
        return "Moderate"

    return "Capital Intensive"

def fcf_conversion_rate(
    free_cash_flow,
    operating_profit
):

    if operating_profit == 0:
        return None

    return round(
        (
            free_cash_flow /
            operating_profit
        ) * 100,
        2
    )

def sign(value):

    if value >= 0:
        return "+"

    return "-"

def capital_allocation_pattern(
    cfo,
    cfi,
    cff,
    cfo_quality=None
):

    pattern = (
        sign(cfo),
        sign(cfi),
        sign(cff)
    )

    if pattern == ("+", "-", "-"):

        if (
            cfo_quality is not None
            and
            cfo_quality > 1
        ):

            return "Shareholder Returns"

        return "Reinvestor"

    if pattern == ("+", "+", "-"):
        return "Liquidating Assets"

    if pattern == ("-", "+", "+"):
        return "Distress Signal"

    if pattern == ("-", "-", "+"):
        return "Growth Funded by Debt"

    if pattern == ("+", "+", "+"):
        return "Cash Accumulator"

    if pattern == ("-", "-", "-"):
        return "Pre-Revenue"

    return "Mixed"

def distress_signal(cfo, cff):

    if cfo is None or cff is None:
        return False

    return cfo < 0 and cff > 0


def deleveraging_flag(cff_current, cff_previous):

    if cff_current is None or cff_previous is None:
        return False

    return (
        cff_current < 0 and
        cff_current < cff_previous
    )