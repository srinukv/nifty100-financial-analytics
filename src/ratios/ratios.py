"""
Sprint 2 - Day 08
Profitability Ratio Engine
"""
from src.ratios.logger import ratio_logger

def calculate_npm(net_profit, sales):
    """
    Net Profit Margin
    """
    if sales == 0:
        return None

    return round((net_profit / sales) * 100, 2)


def calculate_opm(operating_profit, sales):
    """
    Operating Profit Margin
    """
    if sales == 0:
        return None

    return round((operating_profit / sales) * 100, 2)


def calculate_roe(net_profit, equity_capital, reserves):
    """
    Return on Equity
    """
    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round((net_profit / equity) * 100, 2)


def calculate_roce(
    operating_profit,
    equity_capital,
    reserves,
    borrowings
):
    """
    Return on Capital Employed
    """
    capital_employed = (
        equity_capital
        + reserves
        + borrowings
    )

    if capital_employed <= 0:
        return None

    return round(
        (operating_profit / capital_employed) * 100,
        2
    )


def calculate_roa(
    net_profit,
    total_assets
):
    """
    Return on Assets
    """
    if total_assets == 0:
        return None

    return round(
        (net_profit / total_assets) * 100,
        2
    )
def validate_opm(
    calculated_opm,
    source_opm,
    company_id=None,
    year=None
):
    """
    Compare calculated OPM with source OPM.
    Log warning if difference > 1%.
    """

    if calculated_opm is None or source_opm is None:
        return

    difference = abs(
        calculated_opm - source_opm
    )

    if difference > 1:
        ratio_logger.warning(
            f"OPM_MISMATCH | "
            f"Company={company_id} | "
            f"Year={year} | "
            f"Calculated={calculated_opm} | "
            f"Source={source_opm}"
        )