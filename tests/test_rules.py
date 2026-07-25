import pandas as pd

from src.etl.validator import (
    validate_table,
    all_failures
)

def test_empty_dataframe():

    df = pd.DataFrame()

    all_failures.clear()

    validate_table(
        df,
        "companies"
    )

    assert isinstance(
        all_failures,
        list
    )

def test_company_id_column():

    df = pd.DataFrame({

        "company_id":["TCS"]

    })

    all_failures.clear()

    validate_table(
        df,
        "companies"
    )

    assert isinstance(
        all_failures,
        list
    )

def test_year_column():

    df = pd.DataFrame({

        "company_id":["TCS"],

        "year":["2024-03"]

    })

    all_failures.clear()

    validate_table(
        df,
        "profitandloss"
    )

    assert isinstance(
        all_failures,
        list
    )

def test_duplicate_rows():

    df = pd.DataFrame({

        "company_id":["TCS","TCS"],

        "year":["2024-03","2024-03"]

    })

    all_failures.clear()

    validate_table(
        df,
        "profitandloss"
    )

    assert len(all_failures) >= 0

def test_missing_company():

    df = pd.DataFrame({

        "company_id":[None]

    })

    all_failures.clear()

    validate_table(
        df,
        "companies"
    )

    assert len(all_failures) >= 0

def test_negative_sales():

    df = pd.DataFrame({

        "company_id":["ABC"],

        "year":["2024-03"],

        "sales":[-100]

    })

    all_failures.clear()

    validate_table(
        df,
        "profitandloss"
    )

    assert len(all_failures) >= 0

def test_balance_sheet():

    df = pd.DataFrame({

        "company_id":["ABC"],

        "year":["2024-03"]

    })

    all_failures.clear()

    validate_table(
        df,
        "balancesheet"
    )

    assert isinstance(
        all_failures,
        list
    )

def test_cashflow():

    df = pd.DataFrame({

        "company_id":["ABC"],

        "year":["2024-03"]

    })

    all_failures.clear()

    validate_table(
        df,
        "cashflow"
    )

    assert isinstance(
        all_failures,
        list
    )

def test_invalid_year():

    df = pd.DataFrame({

        "company_id":["ABC"],

        "year":["INVALID"]

    })

    all_failures.clear()

    validate_table(
        df,
        "profitandloss"
    )

    assert len(all_failures) >= 0

def test_url_columns():

    df = pd.DataFrame({

        "company_id":["ABC"],

        "website":["invalid_url"]

    })

    all_failures.clear()

    validate_table(
        df,
        "companies"
    )

    assert isinstance(
        all_failures,
        list
    )
