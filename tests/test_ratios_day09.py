import pytest

from src.analytics.ratios import (
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    icr_label,
    icr_warning,
    net_debt,
    asset_turnover
)


# -----------------------------
# Test 1 - Debt to Equity
# -----------------------------
def test_debt_to_equity_normal():

    assert debt_to_equity(
        100,
        200,
        300
    ) == 0.2


# -----------------------------
# Test 2 - Debt Free Company
# -----------------------------
def test_debt_to_equity_zero_borrowings():

    assert debt_to_equity(
        0,
        200,
        300
    ) == 0


# -----------------------------
# Test 3 - Negative Equity
# -----------------------------
def test_debt_to_equity_negative_equity():

    assert debt_to_equity(
        100,
        -200,
        100
    ) is None


# -----------------------------
# Test 4 - High Leverage Flag
# -----------------------------
def test_high_leverage_flag():

    assert high_leverage_flag(
        6,
        "Energy"
    ) is True


# -----------------------------
# Test 5 - Interest Coverage
# -----------------------------
def test_interest_coverage_zero_interest():

    assert interest_coverage_ratio(
        1000,
        100,
        0
    ) is None


# -----------------------------
# Test 6 - ICR Label
# -----------------------------
def test_icr_label():

    assert icr_label(
        None
    ) == "Debt Free"


# -----------------------------
# Test 7 - ICR Warning
# -----------------------------
def test_icr_warning():

    assert icr_warning(
        1.2
    ) is True


# -----------------------------
# Test 8 - Asset Turnover
# -----------------------------
def test_asset_turnover_zero_assets():

    assert asset_turnover(
        1000,
        0
    ) is None