# tests/test_normalizer.py
import pytest

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

def test_company_id_mixed_case():

    assert normalize_company_id("TcS") == "TCS"


def test_company_id_spaces():

    assert normalize_company_id("   RELIANCE   ") == "RELIANCE"


def test_company_id_numbers():

    assert normalize_company_id("m&m") == "M&M"


def test_company_id_empty():

    assert normalize_company_id("") == ""

def test_year_jan():

    assert normalize_year("Jan-24") == "2024-01"


def test_year_feb():

    assert normalize_year("Feb-24") == "2024-02"


def test_year_apr():

    assert normalize_year("Apr-24") == "2024-04"


def test_year_may():

    assert normalize_year("May-24") == "2024-05"


def test_year_jun():

    assert normalize_year("Jun-24") == "2024-06"


def test_year_jul():

    assert normalize_year("Jul-24") == "2024-07"


def test_year_aug():

    assert normalize_year("Aug-24") == "2024-08"


def test_year_sep():

    assert normalize_year("Sep-24") == "2024-09"


def test_year_oct():

    assert normalize_year("Oct-24") == "2024-10"


def test_year_nov():

    assert normalize_year("Nov-24") == "2024-11"

def test_year_old():

    assert normalize_year("Mar-19") == "2019-03"


def test_year_2025():

    assert normalize_year("Dec-25") == "2025-12"

def test_invalid_month():

    assert normalize_year("ABC-23") is None


def test_invalid_string():

    assert normalize_year("Hello") == "Hello"

def test_empty_year():

    assert normalize_year("") == ""


def test_invalid_month():

    assert normalize_year("ABC-23") == "ABC-23"

def test_none_year():

    assert normalize_year(None) is None

def test_ttm():

    assert normalize_year("TTM") == "TTM"

def test_ttm_lower():

    assert normalize_year("ttm") == "TTM"

def test_mar_space():

    assert normalize_year("Mar 23") == "2023-03"

def test_mar_four_digit():

    assert normalize_year("Mar 2023") == "2023-03"

def test_year_strip():

    assert normalize_year("  Mar-23  ") == "2023-03"