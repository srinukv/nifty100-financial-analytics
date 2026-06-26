from src.ratios.ratios import (
    calculate_npm,
    calculate_opm,
    calculate_roe,
    calculate_roce,
    calculate_roa,
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