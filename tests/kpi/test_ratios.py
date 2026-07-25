import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.analytics.ratios import *

def test_net_profit_margin():
    assert net_profit_margin(100, 1000) == 10.0


def test_operating_profit_margin():
    assert operating_profit_margin(200, 1000) == 20.0


def test_roe():
    assert return_on_equity(100, 200, 300) == 20.0


def test_roce():
    assert return_on_capital_employed(
        150,
        200,
        300,
        100
    ) == 25.0


def test_roa():
    assert return_on_assets(
        100,
        1000
    ) == 10.0


def test_debt_equity():
    assert debt_to_equity(
        100,
        200,
        300
    ) == 0.2


def test_interest_coverage():
    assert interest_coverage_ratio(
        100,
        20,
        10
    ) == 12.0


def test_net_debt():
    assert net_debt(
        200,
        50
    ) == 150


def test_asset_turnover():
    assert asset_turnover(
        1000,
        500
    ) == 2.0

def test_npm_none():

    assert net_profit_margin(
        None,
        1000
    ) is None


def test_npm_zero_sales():

    assert net_profit_margin(
        100,
        0
    ) is None

def test_opm_zero_sales():

    assert operating_profit_margin(
        100,
        0
    ) is None


def test_opm_excel_percentage():

    assert operating_profit_margin(
        200,
        1000,
        20
    ) == 20.0

def test_roe_negative_equity():

    assert return_on_equity(
        100,
        -200,
        100
    ) is None


def test_roe_missing():

    assert return_on_equity(
        None,
        100,
        200
    ) is None

def test_roce_zero_capital():

    assert return_on_capital_employed(
        100,
        0,
        0,
        0
    ) is None

def test_debt_free():

    assert debt_to_equity(
        0,
        100,
        100
    ) == 0

def test_high_leverage():

    assert high_leverage_flag(
        6,
        "TCS"
    ) is True


def test_bank_not_high_leverage():

    assert high_leverage_flag(
        12,
        "HDFCBANK"
    ) is False

def test_interest_zero():

    assert interest_coverage_ratio(
        100,
        10,
        0
    ) is None


def test_icr_warning():

    assert icr_warning(
        1.2
    ) is True


def test_icr_no_warning():

    assert icr_warning(
        4
    ) is False

def test_net_debt_none():

    assert net_debt(
        None,
        100
    ) is None

def test_asset_turnover_zero():

    assert asset_turnover(
        100,
        0
    ) is None