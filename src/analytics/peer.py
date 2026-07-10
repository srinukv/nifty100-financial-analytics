"""
Peer Analytics Engine

This module computes peer percentile rankings
for financial metrics within each peer group.
"""

import pandas as pd

PEER_METRICS = {
    "return_on_equity_pct": False,
    "return_on_capital_employed_pct": False,
    "net_profit_margin_pct": False,
    "debt_to_equity": True,
    "free_cash_flow_cr": False,
    "pat_cagr_5yr": False,
    "revenue_cagr_5yr": False,
    "eps_cagr_5yr": False,
    "interest_coverage": False,
    "asset_turnover": False,
}

def load_peer_groups(file_path: str) -> pd.DataFrame:
    """
    Load peer group mapping from Excel.

    Parameters
    ----------
    file_path : str
        Path to peer_groups.xlsx

    Returns
    -------
    pd.DataFrame
        Peer group mapping.
    """
    df = pd.read_excel(file_path)

    required_columns = {
        "peer_group_name",
        "company_id",
        "is_benchmark",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    return df
def get_peer_group(company_id: str, peer_df: pd.DataFrame) -> str:
    """
    Return the peer group for a company.

    Parameters
    ----------
    company_id : str
        Company symbol (e.g. HDFCBANK)

    peer_df : pd.DataFrame
        Peer group mapping DataFrame

    Returns
    -------
    str
        Peer group name or "No peer group assigned"
    """
    match = peer_df.loc[peer_df["company_id"] == company_id]

    if match.empty:
        return "No peer group assigned"

    return match.iloc[0]["peer_group_name"]
def attach_peer_groups(
    analytics_df: pd.DataFrame,
    peer_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Attach peer group information to the analytics dataset.
    """

    merged_df = analytics_df.merge(
        peer_df[["company_id", "peer_group_name"]],
        on="company_id",
        how="left"
    )

    merged_df["peer_group_name"] = merged_df["peer_group_name"].fillna(
        "No peer group assigned"
    )

    return merged_df

def calculate_peer_percentiles():
    """
    Placeholder.
    Will be implemented in later steps.
    """
    pass
def calculate_metric_percentiles(
    merged_df: pd.DataFrame,
    metric: str,
    ascending: bool = False,
) -> pd.DataFrame:
    """
    Calculate percentile ranks for a single metric within each peer group.
    Companies without a peer group are excluded.
    """

    df = merged_df.copy()

    # Exclude companies that are not assigned to a peer group
    df = df[df["peer_group_name"] != "No peer group assigned"].copy()

    # Calculate percentile rank within each peer group
    df["percentile_rank"] = (
    df.groupby("peer_group_name")[metric]
    .rank(method="average", pct=True, ascending=ascending)
)

    if not ascending:
        df["percentile_rank"] = 1 - df["percentile_rank"] + (
        1 / df.groupby("peer_group_name")[metric].transform("count")
    )

    df["percentile_rank"] *= 100

    return df
def build_peer_percentiles(merged_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build peer percentile rankings for all configured metrics.
    """

    all_results = []

    for metric, ascending in PEER_METRICS.items():

        metric_df = calculate_metric_percentiles(
            merged_df,
            metric=metric,
            ascending=ascending,
        )

        metric_df = metric_df[
            [
                "company_id",
                "peer_group_name",
                "year",
                metric,
                "percentile_rank",
            ]
        ].copy()

        metric_df = metric_df.rename(
            columns={
                metric: "value",
            }
        )

        metric_df["metric"] = metric

        metric_df = metric_df[
            [
                "company_id",
                "peer_group_name",
                "metric",
                "value",
                "percentile_rank",
                "year",
            ]
        ]

        all_results.append(metric_df)

    return pd.concat(all_results, ignore_index=True)

import sqlite3


def save_peer_percentiles(
    peer_percentiles_df: pd.DataFrame,
    db_path: str = "nifty100.db",
) -> None:
    """
    Save peer percentile rankings into the SQLite database.

    Parameters
    ----------
    peer_percentiles_df : pd.DataFrame
        DataFrame containing peer percentile rankings.

    db_path : str
        SQLite database path.
    """

    conn = sqlite3.connect(db_path)

    peer_percentiles_df.to_sql(
        "peer_percentiles",
        conn,
        if_exists="replace",
        index=False,
    )

    conn.close()

    print("Peer percentile data saved successfully.")