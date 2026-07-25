# src/etl/normalizer.py

import re

MONTH_MAP = {
    "JAN": "01",
    "FEB": "02",
    "MAR": "03",
    "APR": "04",
    "MAY": "05",
    "JUN": "06",
    "JUL": "07",
    "AUG": "08",
    "SEP": "09",
    "OCT": "10",
    "NOV": "11",
    "DEC": "12"
}


def clean_column_name(col):
    """
    Convert column names into snake_case.
    """

    if col is None:
        return None

    col = str(col).strip().lower()

    col = re.sub(
        r"[^a-z0-9]+",
        "_",
        col
    )

    return col.strip("_")


def normalize_company_id(value):
    """
    Standardize company ticker.
    """

    if value is None:
        return None

    return str(value).strip().upper()


def normalize_year(value):
    """
    Convert different year formats into YYYY-MM.

    Examples:
        Mar-23   -> 2023-03
        Mar 23   -> 2023-03
        Mar 2023 -> 2023-03
        Dec 2012 -> 2012-12
        TTM      -> TTM
    """

    if value is None:
        return None

    value = str(value).strip()

    if value.upper() == "TTM":
        return "TTM"

    match = re.match(
        r"([A-Za-z]{3})[- ]?(\d{2,4})",
        value
    )

    if match:

        month = MONTH_MAP.get(
            match.group(1).upper()
        )

        if month is None:
            return value

        year = int(match.group(2))

        if year < 100:
            year += 2000

        return f"{year}-{month}"

    return value


def normalize_dataframe(df):
    """
    Normalize dataframe columns.
    """

    # Clean column names
    df.columns = [
        clean_column_name(col)
        for col in df.columns
    ]

    # Normalize company id
    if "company_id" in df.columns:

        df["company_id"] = (
            df["company_id"]
            .apply(normalize_company_id)
        )

    # Normalize year
    if "year" in df.columns:

        df["year"] = (
            df["year"]
            .apply(normalize_year)
        )

    return df