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

    col = str(col).strip().lower()

    col = re.sub(r"[^a-z0-9]+", "_", col)

    return col.strip("_")


def normalize_company_id(value):
    """
    Convert company ticker to standard format.
    """

    if value is None:
        return None

    return str(value).strip().upper()


def normalize_year(value):
    """
    Convert:
    Mar-23 -> 2023-03
    Dec-24 -> 2024-12
    """

    if value is None:
        return None

    value = str(value).strip()

    match = re.match(
        r"([A-Za-z]{3})[- ]?(\d{2})",
        value
    )

    if match:

        month = MONTH_MAP[
            match.group(1).upper()
        ]

        year = int(match.group(2))

        year += 2000

        return f"{year}-{month}"

    return value


def normalize_dataframe(df):

    if "company_id" in df.columns:
        df["company_id"] = (
            df["company_id"]
            .apply(normalize_company_id)
        )

    if "year" in df.columns:
        df["year"] = (
            df["year"]
            .apply(normalize_year)
        )

    return df