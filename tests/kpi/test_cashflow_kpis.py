from src.analytics.cashflow_kpis import *


def test_free_cash_flow():
    assert free_cash_flow(100, -40) == 60


def test_capex_intensity():
    assert capex_intensity(-40, 200) == 20.0


def test_cfo_quality_score():
    # Your function returns 1.5
    assert cfo_quality_score(150, 100) == 1.5


def test_fcf_conversion_rate():
    # Your function returns percentage
    assert fcf_conversion_rate(80, 100) == 80.0


def test_zero_sales():
    assert capex_intensity(-50, 0) is None


def test_zero_operating_profit():
    assert fcf_conversion_rate(50, 0) is None


def test_negative_capex():
    assert free_cash_flow(300, -100) == 200