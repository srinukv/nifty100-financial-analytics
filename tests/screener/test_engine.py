import pandas as pd

from src.screener.engine import apply_single_filter
def test_financial_sector_not_filtered_by_debt_to_equity():
    """
    Financial sector companies should bypass
    Debt-to-Equity filtering.
    """

    df = pd.DataFrame(
        {
            "company_id": [
                "HDFCBANK",
                "TCS",
                "RELIANCE"
            ],
            "broad_sector": [
                "Financials",
                "Information Technology",
                "Energy"
            ],
            "debt_to_equity": [
                8.5,
                0.5,
                2.2
            ]
        }
    )

    result = apply_single_filter(
        df=df,
        column="debt_to_equity",
        operator="<=",
        value=1.0
    )

    assert "HDFCBANK" in result["company_id"].values

def test_non_financial_filtered_by_debt_to_equity():
    """
    Non-financial companies should be filtered
    using the Debt-to-Equity threshold.
    """

    df = pd.DataFrame(
        {
            "company_id": [
                "TCS",
                "RELIANCE"
            ],
            "broad_sector": [
                "Information Technology",
                "Energy"
            ],
            "debt_to_equity": [
                0.5,
                2.2
            ]
        }
    )

    result = apply_single_filter(
        df=df,
        column="debt_to_equity",
        operator="<=",
        value=1.0
    )

    assert "TCS" in result["company_id"].values
    assert "RELIANCE" not in result["company_id"].values