# src/validators/rules.py

import re


def check_company_id_not_null(df, table_name):

    failures = []

    if "company_id" not in df.columns:
        return failures

    invalid_rows = df[df["company_id"].isna()]

    for idx in invalid_rows.index:

        failures.append({
            "table": table_name,
            "row": idx,
            "field": "company_id",
            "issue": "NULL company_id",
            "severity": "CRITICAL"
        })

    return failures


def check_duplicate_company_year(df, table_name):

    failures = []

    valid_tables = [
        "profitandloss",
        "balancesheet",
        "cashflow",
        "financial_ratios",
        "market_cap"
    ]

    if table_name not in valid_tables:
        return failures

    if (
        "company_id" not in df.columns
        or
        "year" not in df.columns
    ):
        return failures

    duplicate_rows = df[
        df.duplicated(
            subset=["company_id", "year"],
            keep=False
        )
    ]

    if len(duplicate_rows) == 0:
        return failures

    grouped = (
        duplicate_rows
        .groupby(
            ["company_id", "year"]
        )
        .size()
        .reset_index(name="count")
    )

    for _, row in grouped.iterrows():

        failures.append({
            "table": table_name,
            "row": "-",
            "field": "company_id,year",
            "issue":
            f"Duplicate key {row['company_id']} {row['year']}",
            "severity": "CRITICAL"
        })

    return failures

def check_sales_positive(df, table_name):

    failures = []

    if "sales" not in df.columns:
        return failures

    invalid = df[df["sales"] <= 0]

    for idx in invalid.index:

        failures.append({
            "table": table_name,
            "row": idx,
            "field": "sales",
            "issue": "Sales <= 0",
            "severity": "CRITICAL"
        })

    return failures

def check_balance_sheet(df, table_name):

    failures = []

    if table_name != "balancesheet":
        return failures

    required = [
        "total_assets",
        "total_liabilities"
    ]

    if not all(c in df.columns for c in required):
        return failures

    invalid = df[
        abs(
            df["total_assets"]
            - df["total_liabilities"]
        ) > 1
    ]

    for idx in invalid.index:

        failures.append({
            "table": table_name,
            "row": idx,
            "field": "balance_sheet",
            "issue": "Assets != Liabilities",
            "severity": "CRITICAL"
        })

    return failures


def check_cashflow_totals(df, table_name):

    failures = []

    if table_name != "cashflow":
        return failures

    required = [
        "operating_activity",
        "investing_activity",
        "financing_activity",
        "net_cash_flow"
    ]

    if not all(c in df.columns for c in required):
        return failures

    calculated = (
        df["operating_activity"]
        + df["investing_activity"]
        + df["financing_activity"]
    )

    invalid = df[
        abs(
            calculated
            - df["net_cash_flow"]
        ) > 10
    ]

    for idx in invalid.index:

        failures.append({
            "table": table_name,
            "row": idx,
            "field": "net_cash_flow",
            "issue": "Cashflow mismatch",
            "severity": "CRITICAL"
        })

    return failures


def check_opm(df, table_name):

    failures = []

    if table_name != "profitandloss":
        return failures

    required = [
        "sales",
        "operating_profit",
        "opm_percentage"
    ]

    if not all(c in df.columns for c in required):
        return failures

    calculated = (
        df["operating_profit"]
        / df["sales"]
        * 100
    )

    invalid = df[
        abs(
            calculated
            - df["opm_percentage"]
        ) > 1
    ]

    for idx in invalid.index:

        failures.append({
            "table": table_name,
            "row": idx,
            "field": "opm_percentage",
            "issue": "OPM mismatch",
            "severity": "WARNING"
        })

    return failures


def check_year_format(df, table_name):

    failures = []

    if "year" not in df.columns:
        return failures

    invalid = []

    for idx, value in df["year"].items():

        value = str(value)

        if re.match(r"^\d{4}-\d{2}$", value):
            continue

        if re.match(r"^\d{4}$", value):
            continue

        invalid.append(idx)

    for idx in invalid:

        failures.append({
            "table": table_name,
            "row": idx,
            "field": "year",
            "issue": "Invalid year format",
            "severity": "WARNING"
        })

    return failures


def check_url_columns(df, table_name):

    failures = []

    url_columns = [
        "website",
        "annual_report"
    ]

    for col in url_columns:

        if col not in df.columns:
            continue

        invalid = df[
            (
                df[col].notna()
            )
            &
            (
                ~df[col]
                .astype(str)
                .str.startswith(
                    ("http://", "https://")
                )
            )
        ]

        for idx in invalid.index:

            failures.append({
                "table": table_name,
                "row": idx,
                "field": col,
                "issue": "Invalid URL",
                "severity": "WARNING"
            })

    return failures