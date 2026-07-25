from src.analytics.cagr import *


def test_positive_cagr():

    value, flag = revenue_cagr(100, 200, 5)

    assert flag == "NORMAL"
    assert value > 0


def test_zero_start():

    value, flag = revenue_cagr(0, 200, 5)

    assert value is None
    assert flag == "ZERO_BASE"


def test_negative_start():

    value, flag = revenue_cagr(-100, 200, 5)

    assert value is None
    assert flag == "TURNAROUND"


def test_same_values():

    value, flag = revenue_cagr(100, 100, 5)

    assert value == 0.0
    assert flag == "NORMAL"


def test_pat_cagr():

    value, flag = pat_cagr(100, 200, 5)

    assert flag == "NORMAL"
    assert value > 0


def test_eps_cagr():

    value, flag = eps_cagr(10, 20, 5)

    assert flag == "NORMAL"
    assert value > 0