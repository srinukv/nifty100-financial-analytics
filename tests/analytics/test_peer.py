import pandas as pd

from src.analytics.peer import load_peer_groups
from src.screener.engine import (
    load_master_dataframe,
    prepare_analytics_dataframe,
)
from src.analytics.peer import calculate_metric_percentiles

from src.analytics.peer import attach_peer_groups
from src.analytics.peer import build_peer_percentiles

def test_load_peer_groups():
    """
    Test that peer_groups.xlsx loads successfully.
    """

    peer_df = load_peer_groups("data/raw/peer_groups.xlsx")

    assert isinstance(peer_df, pd.DataFrame)

    assert not peer_df.empty

    required_columns = {
        "peer_group_name",
        "company_id",
        "is_benchmark",
    }

    assert required_columns.issubset(peer_df.columns)

from src.analytics.peer import get_peer_group


def test_get_peer_group_existing_company():
    """
    Test that an existing company returns the correct peer group.
    """

    peer_df = load_peer_groups("data/raw/peer_groups.xlsx")

    assert get_peer_group("HDFCBANK", peer_df) == "Private Banks"


def test_get_peer_group_unknown_company():
    """
    Test that an unknown company returns the expected message.
    """

    peer_df = load_peer_groups("data/raw/peer_groups.xlsx")

    assert (
        get_peer_group("UNKNOWN_COMPANY", peer_df)
        == "No peer group assigned"
    )

def test_attach_peer_groups():
    """
    Test that peer groups are attached to the analytics dataset.
    """

    master_df = load_master_dataframe()
    analytics_df = prepare_analytics_dataframe(master_df)

    peer_df = load_peer_groups("data/raw/peer_groups.xlsx")

    merged_df = attach_peer_groups(analytics_df, peer_df)

    # Verify new column exists
    assert "peer_group_name" in merged_df.columns

    # Verify no missing values remain
    assert merged_df["peer_group_name"].isna().sum() == 0

    # Verify at least one mapped company exists
    assert (
        merged_df["peer_group_name"] != "No peer group assigned"
    ).any()

    # Verify at least one unmapped company exists
    assert (
        merged_df["peer_group_name"] == "No peer group assigned"
    ).any()

def test_calculate_metric_percentiles():
    """
    Test percentile calculation for a single metric.
    """

    master_df = load_master_dataframe()
    analytics_df = prepare_analytics_dataframe(master_df)

    peer_df = load_peer_groups("data/raw/peer_groups.xlsx")

    merged_df = attach_peer_groups(analytics_df, peer_df)

    result = calculate_metric_percentiles(
        merged_df,
        metric="return_on_equity_pct"
    )

    # Verify percentile column exists
    assert "percentile_rank" in result.columns

    # Verify values are between 0 and 100
    assert result["percentile_rank"].between(0, 100).all()

    # Verify companies without peer groups are excluded
    assert (
        result["peer_group_name"] == "No peer group assigned"
    ).sum() == 0

def test_build_peer_percentiles():
    """
    Test building peer percentile rankings for all configured metrics.
    """

    master_df = load_master_dataframe()
    analytics_df = prepare_analytics_dataframe(master_df)

    peer_df = load_peer_groups("data/raw/peer_groups.xlsx")

    merged_df = attach_peer_groups(analytics_df, peer_df)

    result = build_peer_percentiles(merged_df)

    # Verify DataFrame is not empty
    assert not result.empty

    # Verify required columns exist
    required_columns = {
        "company_id",
        "peer_group_name",
        "metric",
        "value",
        "percentile_rank",
        "year",
    }

    assert required_columns.issubset(result.columns)

    # Verify all configured metrics are present
    assert result["metric"].nunique() == 10