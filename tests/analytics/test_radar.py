import pandas as pd

from src.analytics.radar import prepare_radar_dataset
from src.analytics.radar import get_peer_group_average

def test_prepare_radar_dataset():
    """
    Test that prepare_radar_dataset returns
    the required radar chart columns.
    """
    df = pd.DataFrame({
        "company_id": ["ABC"],
        "company_name": ["ABC Ltd"],
        "peer_group_name": ["IT"],
        "year": [2024],
        "return_on_equity_pct": [20],
        "return_on_capital_employed_pct": [18],
        "net_profit_margin_pct": [15],
        "debt_to_equity": [0.5],
        "free_cash_flow_cr": [120],
        "pat_cagr_5yr": [14],
        "revenue_cagr_5yr": [12],
        "composite_quality_score": [85],
    })

    radar_df = prepare_radar_dataset(df)

    assert radar_df.shape[0] == 1

    expected_columns = [
        "company_id",
        "company_name",
        "peer_group_name",
        "year",
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "pat_cagr_5yr",
        "revenue_cagr_5yr",
        "composite_quality_score",
    ]

    assert list(radar_df.columns) == expected_columns

from src.analytics.radar import calculate_peer_group_averages


def test_calculate_peer_group_averages():
    """
    Test peer group average calculation.
    """
    df = pd.DataFrame({
        "company_id": ["A", "B"],
        "company_name": ["A Ltd", "B Ltd"],
        "peer_group_name": ["IT", "IT"],
        "year": [2024, 2024],
        "return_on_equity_pct": [20, 30],
        "return_on_capital_employed_pct": [15, 25],
        "net_profit_margin_pct": [10, 20],
        "debt_to_equity": [0.5, 1.5],
        "free_cash_flow_cr": [100, 200],
        "pat_cagr_5yr": [12, 18],
        "revenue_cagr_5yr": [10, 20],
        "composite_quality_score": [80, 90],
    })

    peer_avg = calculate_peer_group_averages(df)

    assert peer_avg.shape[0] == 1
    assert peer_avg.iloc[0]["peer_group_name"] == "IT"
    assert peer_avg.iloc[0]["return_on_equity_pct"] == 25

from src.analytics.radar import get_company_radar_data


def test_get_company_radar_data():
    """
    Test retrieving radar data for a single company.
    """
    df = pd.DataFrame({
        "company_id": ["ABC", "XYZ"],
        "company_name": ["ABC Ltd", "XYZ Ltd"],
        "peer_group_name": ["IT", "Banking"],
        "year": [2024, 2024],
        "return_on_equity_pct": [20, 25],
        "return_on_capital_employed_pct": [18, 22],
        "net_profit_margin_pct": [15, 18],
        "debt_to_equity": [0.5, 0.8],
        "free_cash_flow_cr": [100, 120],
        "pat_cagr_5yr": [12, 14],
        "revenue_cagr_5yr": [10, 16],
        "composite_quality_score": [82, 88],
    })

    company = get_company_radar_data(df, "ABC")

    assert company["company_name"] == "ABC Ltd"
    assert company["peer_group_name"] == "IT"

def test_get_peer_group_average():
    """
    Test retrieving average metrics for a peer group.
    """
    peer_avg_df = pd.DataFrame({
        "peer_group_name": ["IT", "Banking"],
        "return_on_equity_pct": [25, 18],
        "return_on_capital_employed_pct": [22, 15],
        "net_profit_margin_pct": [18, 12],
        "debt_to_equity": [0.6, 1.2],
        "free_cash_flow_cr": [150, 200],
        "pat_cagr_5yr": [15, 10],
        "revenue_cagr_5yr": [14, 8],
        "composite_quality_score": [86, 74],
    })

    peer = get_peer_group_average(peer_avg_df, "IT")

    assert peer["peer_group_name"] == "IT"
    assert peer["return_on_equity_pct"] == 25