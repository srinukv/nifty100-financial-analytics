from src.ratios.cagr import (
    calculate_cagr,
    calculate_revenue_cagr,
    calculate_pat_cagr,
    calculate_eps_cagr,
)


def test_cagr_normal():
    value, flag = calculate_cagr(100, 200, 5, 5)
    assert value == 14.87
    assert flag is None


def test_decline_to_loss():
    value, flag = calculate_cagr(100, -50, 5, 5)
    assert value is None
    assert flag == "DECLINE_TO_LOSS"


def test_turnaround():
    value, flag = calculate_cagr(-100, 50, 5, 5)
    assert value is None
    assert flag == "TURNAROUND"


def test_both_negative():
    value, flag = calculate_cagr(-100, -50, 5, 5)
    assert value is None
    assert flag == "BOTH_NEGATIVE"


def test_zero_base():
    value, flag = calculate_cagr(0, 100, 5, 5)
    assert value is None
    assert flag == "ZERO_BASE"


def test_insufficient_data():
    value, flag = calculate_cagr(100, 200, 5, 3)
    assert value is None
    assert flag == "INSUFFICIENT"


def test_revenue_cagr():
    value, flag = calculate_revenue_cagr(100, 200, 5, 5)
    assert value == 14.87
    assert flag is None


def test_pat_cagr():
    value, flag = calculate_pat_cagr(100, 200, 3, 3)
    assert value == 25.99
    assert flag is None


def test_eps_cagr():
    value, flag = calculate_eps_cagr(10, 20, 10, 10)
    assert value == 7.18
    assert flag is None


def test_three_year_cagr():
    value, flag = calculate_cagr(100, 200, 3, 3)
    assert value == 25.99
    assert flag is None