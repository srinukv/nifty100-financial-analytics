from src.etl.normaliser import (
    normalize_year,
    normalize_company_id
)


def test_year_integer():
    assert normalize_year(2024) == 2024


def test_year_string():
    assert normalize_year("2024") == 2024


def test_year_fy():
    assert normalize_year("FY2024") == 2024


def test_year_none():
    assert normalize_year(None) is None


def test_company_upper():
    assert normalize_company_id("infy") == "INFY"


def test_company_trim():
    assert normalize_company_id("  tcs  ") == "TCS"


def test_company_none():
    assert normalize_company_id(None) is None

def test_year_with_spaces():
    assert normalize_year(" 2024 ") == 2024


def test_year_invalid():
    assert normalize_year("ABC") is None


def test_year_fy_format():
    assert normalize_year("FY 2025") == 2025


def test_year_long_text():
    assert normalize_year("Financial Year 2023") == 2023


def test_company_already_upper():
    assert normalize_company_id("INFY") == "INFY"


def test_company_mixed_case():
    assert normalize_company_id("InFy") == "INFY"


def test_company_numeric():
    assert normalize_company_id("123") == "123"


def test_company_empty_string():
    assert normalize_company_id("") == ""


def test_company_spaces_only():
    assert normalize_company_id("   ") == ""