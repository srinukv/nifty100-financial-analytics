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
def calculate_debt_to_equity(
    borrowings,
    equity_capital,
    reserves
):
    """
    Debt-to-Equity Ratio
    """

    if borrowings == 0:
        return 0

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round(
        borrowings / equity,
        2
    )

def get_high_leverage_flag(
    debt_to_equity,
    broad_sector
):
    """
    Returns True if a non-financial company has
    Debt-to-Equity greater than 5.
    """

    if debt_to_equity is None:
        return False

    if (
        debt_to_equity > 5 and
        broad_sector.lower() != "financials"
    ):
        return True

    return False

def calculate_interest_coverage(
    operating_profit,
    other_income,
    interest
):
    """
    Interest Coverage Ratio (ICR)
    """

    if interest == 0:
        return None

    ebit = operating_profit + other_income

    return round(
        ebit / interest,
        2
    )

def get_icr_label(icr):
    """
    Returns display label for Interest Coverage Ratio.
    """

    if icr is None:
        return "Debt Free"

    return ""

def get_icr_warning_flag(icr):
    """
    Returns True if Interest Coverage Ratio
    indicates financial risk.
    """

    if icr is None:
        return False

    return icr < 1.5

def calculate_net_debt(
    borrowings,
    investments
):
    """
    Net Debt
    """

    return round(
        borrowings - investments,
        2
    )
def calculate_asset_turnover(
    sales,
    total_assets
):
    """
    Asset Turnover Ratio
    """

    if total_assets == 0:
        return None

    return round(
        sales / total_assets,
        2
    )