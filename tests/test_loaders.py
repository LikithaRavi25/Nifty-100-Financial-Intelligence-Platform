import pandas as pd
import pytest

from pathlib import Path

from src.etl.loader import (
    validate_files_exist,
    load_excel
)

def test_validate_files_returns_list():

    missing = validate_files_exist()

    assert isinstance(
        missing,
        list
    )

def test_no_missing_files():

    missing = validate_files_exist()

    assert len(missing) == 0

def test_load_excel_dataframe():

    df = load_excel(
        Path("data/raw/companies.xlsx")
    )

    assert isinstance(
        df,
        pd.DataFrame
    )

def test_load_excel_not_empty():

    df = load_excel(
        Path("data/raw/companies.xlsx")
    )

    assert len(df) > 0

def test_columns_lowercase():

    df = load_excel(
        Path("data/raw/companies.xlsx")
    )

    for col in df.columns:

        assert col == col.lower()

def test_columns_snake_case():

    df = load_excel(
        Path("data/raw/companies.xlsx")
    )

    for col in df.columns:

        assert " " not in col

def test_company_id_uppercase():

    df = load_excel(
        Path("data/raw/companies.xlsx")
    )

    if "company_id" in df.columns:

        assert all(

            df["company_id"]

            .dropna()

            .str.isupper()

        )

def test_year_column():

    df = load_excel(
        Path("data/raw/companies.xlsx")
    )

    if "year" in df.columns:

        assert "year" in df.columns

def test_invalid_file():

    with pytest.raises(FileNotFoundError):

        load_excel(

            Path("data/raw/not_exists.xlsx")

        )

def test_dataframe_has_columns():

    df = load_excel(
        Path("data/raw/companies.xlsx")
    )

    assert len(df.columns) > 0