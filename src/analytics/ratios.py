import pandas as pd


def is_missing(value):
    return value is None or pd.isna(value)


# ------------------------------
# Day 08 Ratios
# ------------------------------

def net_profit_margin(net_profit, sales):

    if is_missing(net_profit) or is_missing(sales) or sales == 0:
        return None

    return round((net_profit / sales) * 100, 2)

def operating_profit_margin(
    operating_profit,
    sales,
    opm_percentage=None
):

    if is_missing(operating_profit) or is_missing(sales) or sales == 0:
        return None

    calculated = round((operating_profit / sales) * 100, 2)

    if opm_percentage is not None and not pd.isna(opm_percentage):

        source = float(opm_percentage)

        if source <= 1:
            source *= 100

        # Skip unrealistic values
        if source > 100:
            return calculated

        difference = abs(calculated - source)

        if difference > 1:
            print(
                f"WARNING | Calculated={calculated:.2f}% | "
                f"Excel={source:.2f}% | "
                f"Difference={difference:.2f}%"
            )

    return calculated



def return_on_equity(net_profit, equity_capital, reserves):

    if (
        is_missing(net_profit)
        or is_missing(equity_capital)
        or is_missing(reserves)
    ):
        return None

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round((net_profit / equity) * 100, 2)


def return_on_capital_employed(
    ebit,
    equity_capital,
    reserves,
    borrowings,
):

    if (
        is_missing(ebit)
        or is_missing(equity_capital)
        or is_missing(reserves)
        or is_missing(borrowings)
    ):
        return None

    capital = equity_capital + reserves + borrowings

    if capital <= 0:
        return None

    return round((ebit / capital) * 100, 2)


def return_on_assets(net_profit, total_assets):

    if (
        is_missing(net_profit)
        or is_missing(total_assets)
        or total_assets == 0
    ):
        return None

    return round((net_profit / total_assets) * 100, 2)


# ------------------------------
# Day 09 Ratios
# ------------------------------

def debt_to_equity(borrowings, equity_capital, reserves):

    if (
        is_missing(borrowings)
        or is_missing(equity_capital)
        or is_missing(reserves)
    ):
        return None

    if borrowings == 0:
        return 0

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round(borrowings / equity, 2)


def high_leverage_flag(de_ratio, company_id):

    if de_ratio is None or pd.isna(de_ratio):
        return False

    financial_companies = {
        "HDFCBANK",
        "ICICIBANK",
        "SBIN",
        "AXISBANK",
        "KOTAKBANK",
        "INDUSINDBK",
        "BANKBARODA",
        "PNB",
        "CANBK",
        "UNIONBANK",
        "IDBI",
        "BAJFINANCE",
        "BAJAJFINSV",
        "SBILIFE",
        "HDFCLIFE",
        "ICICIPRULI",
        "LICI",
        "PFC",
        "RECLTD"
    }

    if company_id in financial_companies:
        return False

    return de_ratio > 5


def interest_coverage_ratio(
    operating_profit,
    other_income,
    interest,
):

    if (
        is_missing(operating_profit)
        or is_missing(other_income)
        or is_missing(interest)
        or interest == 0
    ):
        return None

    return round(
        (operating_profit + other_income) / interest,
        2,
    )


def icr_label(icr):

    if icr is None or pd.isna(icr):
        return "Debt Free"

    return "Borrowing Company"


def icr_warning(icr):

    if icr is None or pd.isna(icr):
        return False

    return icr < 1.5


def net_debt(borrowings, investments):

    if is_missing(borrowings) or is_missing(investments):
        return None

    return round(borrowings - investments, 2)


def asset_turnover(sales, total_assets):

    if (
        is_missing(sales)
        or is_missing(total_assets)
        or total_assets == 0
    ):
        return None

    return round(sales / total_assets, 2)