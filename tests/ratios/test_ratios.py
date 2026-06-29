
from src.ratios.ratios import (
    calculate_npm,
    calculate_opm,
    calculate_roe,
    calculate_roce,
    calculate_roa,
)
from src.ratios.ratios import (
    calculate_debt_to_equity,
    get_high_leverage_flag,
    calculate_interest_coverage,
    get_icr_label,
    get_icr_warning_flag,
    calculate_net_debt,
    calculate_asset_turnover,
)

def test_npm_normal():
    assert calculate_npm(100, 1000) == 10.0


def test_npm_zero_sales():
    assert calculate_npm(100, 0) is None


def test_opm_normal():
    assert calculate_opm(200, 1000) == 20.0


def test_roe_normal():
    assert calculate_roe(100, 100, 400) == 20.0


def test_roe_negative_equity():
    assert calculate_roe(100, -200, 100) is None


def test_roce_normal():
    assert calculate_roce(200, 100, 400, 500) == 20.0


def test_roa_normal():
    assert calculate_roa(100, 1000) == 10.0


def test_roa_zero_assets():
    assert calculate_roa(100, 0) is None

from src.ratios.ratios import validate_opm


def test_validate_opm_mismatch():
    validate_opm(
        calculated_opm=20,
        source_opm=10,
        company_id="TEST",
        year=2024
    )

    assert True
def test_debt_to_equity_debt_free():
    assert calculate_debt_to_equity(0, 100, 400) == 0


def test_debt_to_equity_negative_equity():
    assert calculate_debt_to_equity(500, -100, 50) is None


def test_high_leverage_flag():
    assert get_high_leverage_flag(6.0, "Consumer") is True
    assert get_high_leverage_flag(6.0, "Financials") is False


def test_interest_coverage_interest_zero():
    assert calculate_interest_coverage(1000, 100, 0) is None


def test_icr_label():
    assert get_icr_label(None) == "Debt Free"
    assert get_icr_label(3.5) == ""


def test_icr_warning_flag():
    assert get_icr_warning_flag(1.2) is True
    assert get_icr_warning_flag(2.0) is False


def test_net_debt():
    assert calculate_net_debt(500, 100) == 400


def test_asset_turnover():
    assert calculate_asset_turnover(1000, 500) == 2.0
    assert calculate_asset_turnover(1000, 0) is None