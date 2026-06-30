from src.ratios.ratios import (
    calculate_free_cash_flow,
    calculate_cfo_quality_score,
    get_cfo_quality_label,
    calculate_capex_intensity,
    get_capex_intensity_label,
    calculate_fcf_conversion_rate,
    classify_capital_allocation,
)


def test_free_cash_flow():
    assert calculate_free_cash_flow(1000, -300) == 700


def test_negative_free_cash_flow():
    assert calculate_free_cash_flow(500, -700) == -200


def test_cfo_quality_score():
    assert calculate_cfo_quality_score(120, 100) == 1.2


def test_cfo_quality_none():
    assert calculate_cfo_quality_score(100, 0) is None


def test_cfo_quality_label():
    assert get_cfo_quality_label(1.2) == "High Quality"
    assert get_cfo_quality_label(0.7) == "Moderate"
    assert get_cfo_quality_label(0.3) == "Accrual Risk"


def test_capex_intensity():
    assert calculate_capex_intensity(-50, 1000) == 5.0


def test_capex_label():
    assert get_capex_intensity_label(2.0) == "Asset Light"
    assert get_capex_intensity_label(5.0) == "Moderate"
    assert get_capex_intensity_label(10.0) == "Capital Intensive"


def test_fcf_conversion():
    assert calculate_fcf_conversion_rate(700, 1000) == 70.0


def test_fcf_conversion_none():
    assert calculate_fcf_conversion_rate(700, 0) is None


def test_capital_allocation_classifier():
    assert (
        classify_capital_allocation(
            100,
            -50,
            -20,
            "High Quality",
        )
        == "Shareholder Returns"
    )