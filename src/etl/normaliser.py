import re
import pandas as pd


def normalize_year(value):
    """
    Convert year values to integer.
    Examples:
    2024 -> 2024
    '2024' -> 2024
    'FY2024' -> 2024
    """

    if pd.isna(value):
        return None

    value = str(value).strip()

    match = re.search(r"(20\d{2})", value)

    if match:
        return int(match.group(1))

    return None


def normalize_company_id(value):
    """
    Standardise company_id.

    Example:
    infy -> INFY
    Tcs -> TCS
    """

    if pd.isna(value):
        return None

    return str(value).strip().upper()