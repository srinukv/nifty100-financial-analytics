from math import pow


def calculate_cagr(
    start_value,
    end_value,
    years,
    available_years,
):
    """
    Generic CAGR calculation.
    Returns:
        (cagr_value, flag)
    """

    if available_years < years:
        return None, "INSUFFICIENT"

    if start_value == 0:
        return None, "ZERO_BASE"

    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    cagr = (
        (pow(end_value / start_value, 1 / years) - 1)
        * 100
    )

    return round(cagr, 2), None

def calculate_revenue_cagr(
    start_sales,
    end_sales,
    years,
    available_years,
):
    """
    Revenue CAGR
    """
    return calculate_cagr(
        start_sales,
        end_sales,
        years,
        available_years,
    )


def calculate_pat_cagr(
    start_profit,
    end_profit,
    years,
    available_years,
):
    """
    PAT CAGR
    """
    return calculate_cagr(
        start_profit,
        end_profit,
        years,
        available_years,
    )


def calculate_eps_cagr(
    start_eps,
    end_eps,
    years,
    available_years,
):
    """
    EPS CAGR
    """
    return calculate_cagr(
        start_eps,
        end_eps,
        years,
        available_years,
    )