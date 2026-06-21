from pathlib import Path

from src.etl.loader import get_header_row


def test_companies_header():
    assert get_header_row("companies.xlsx") == 1


def test_profitandloss_header():
    assert get_header_row("profitandloss.xlsx") == 1


def test_balancesheet_header():
    assert get_header_row("balancesheet.xlsx") == 1


def test_market_cap_header():
    assert get_header_row("market_cap.xlsx") == 0


def test_stock_prices_header():
    assert get_header_row("stock_prices.xlsx") == 0