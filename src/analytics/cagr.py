import math


def calculate_cagr(
    start,
    end,
    years
):
    """
    Generic CAGR Calculator

    Returns:
        (value, flag)
    """

    if years <= 0:
        return None, "INVALID_YEARS"

    if start == 0:
        return None, "ZERO_BASE"

    if start < 0 and end < 0:
        return None, "BOTH_NEGATIVE"

    if start < 0 and end > 0:
        return None, "TURNAROUND"

    if start > 0 and end < 0:
        return None, "DECLINE_TO_LOSS"

    cagr = (
        (
            end / start
        ) ** (1 / years)
        - 1
    ) * 100

    return round(cagr, 2), "NORMAL"

def revenue_cagr(
    start_sales,
    end_sales,
    years
):

    return calculate_cagr(
        start_sales,
        end_sales,
        years
    )

def pat_cagr(
    start_profit,
    end_profit,
    years
):

    return calculate_cagr(
        start_profit,
        end_profit,
        years
    )

def eps_cagr(
    start_eps,
    end_eps,
    years
):

    return calculate_cagr(
        start_eps,
        end_eps,
        years
    )

def calculate_cagr_with_history(
    values,
    years
):

    if len(values) < years + 1:

        return None, "INSUFFICIENT"

    start = values[0]

    end = values[-1]

    return calculate_cagr(
        start,
        end,
        years
    )