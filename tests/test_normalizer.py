# tests/test_normalizer.py

from src.etl.normalizer import (
    normalize_company_id,
    normalize_year
)


def test_company_id_upper():

    assert (
        normalize_company_id("tcs")
        == "TCS"
    )


def test_company_id_strip():

    assert (
        normalize_company_id("  infy ")
        == "INFY"
    )


def test_year_mar():

    assert (
        normalize_year("Mar-23")
        == "2023-03"
    )


def test_year_dec():

    assert (
        normalize_year("Dec-24")
        == "2024-12"
    )