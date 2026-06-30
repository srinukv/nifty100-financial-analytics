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

def calculate_free_cash_flow(
    operating_activity,
    investing_activity
):
    """
    Free Cash Flow (FCF)
    """

    return round(
        operating_activity + investing_activity,
        2
    )

def calculate_cfo_quality_score(
    average_cfo,
    average_pat
):
    """
    CFO Quality Score
    """

    if average_pat == 0:
        return None

    return round(
        average_cfo / average_pat,
        2
    )

def get_cfo_quality_label(score):
    """
    CFO Quality Classification
    """

    if score is None:
        return None

    if score > 1.0:
        return "High Quality"

    if score >= 0.5:
        return "Moderate"

    return "Accrual Risk"

def calculate_capex_intensity(
    investing_activity,
    sales
):
    """
    CapEx Intensity (%)
    """

    if sales == 0:
        return None

    return round(
        (abs(investing_activity) / sales) * 100,
        2
    )

def get_capex_intensity_label(intensity):
    """
    CapEx Intensity Classification
    """

    if intensity is None:
        return None

    if intensity < 3:
        return "Asset Light"

    if intensity <= 8:
        return "Moderate"

    return "Capital Intensive"

def calculate_fcf_conversion_rate(
    free_cash_flow,
    operating_profit
):
    """
    Free Cash Flow Conversion Rate (%)
    """

    if operating_profit == 0:
        return None

    return round(
        (free_cash_flow / operating_profit) * 100,
        2
    )
def classify_capital_allocation(
    operating_activity,
    investing_activity,
    financing_activity,
    cfo_quality_label=None,
):
    """
    Capital Allocation Pattern Classification
    """

    cfo = "+" if operating_activity >= 0 else "-"
    cfi = "+" if investing_activity >= 0 else "-"
    cff = "+" if financing_activity >= 0 else "-"

    pattern = (cfo, cfi, cff)

    if pattern == ("+", "-", "-"):
        if cfo_quality_label == "High Quality":
            return "Shareholder Returns"
        return "Reinvestor"

    if pattern == ("+", "+", "-"):
        return "Liquidating Assets"

    if pattern == ("-", "+", "+"):
        return "Distress Signal"

    if pattern == ("-", "-", "+"):
        return "Growth Funded by Debt"

    if pattern == ("+", "+", "+"):
        return "Cash Accumulator"

    if pattern == ("-", "-", "-"):
        return "Pre-Revenue"

    if pattern == ("+", "-", "+"):
        return "Mixed"

    return "Other"