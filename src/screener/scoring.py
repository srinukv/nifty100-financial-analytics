SCORING_MODEL = {
    "profitability": {
        "weight": 35,
        "metrics": {
            "return_on_equity_pct": 15,
            "return_on_capital_employed_pct": 10,
            "net_profit_margin_pct": 10,
        },
    },
    "cash_quality": {
        "weight": 30,
        "metrics": {
            "free_cash_flow_cr": 15,
            "cfo_pat_ratio": 10,
            "fcf_positive": 5,
        },
    },
    "growth": {
        "weight": 20,
        "metrics": {
            "revenue_cagr_5yr": 10,
            "pat_cagr_5yr": 10,
        },
    },
    "leverage": {
        "weight": 15,
        "metrics": {
            "debt_to_equity": 10,
            "interest_coverage": 5,
        },
    },
}
import numpy as np
import pandas as pd


def prepare_scoring_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare all metrics required by the composite scoring engine.

    This function creates derived metrics without modifying
    the original analytics DataFrame.
    """

    scoring_df = df.copy()

    # --------------------------------------------------
    # CFO / PAT Ratio
    # --------------------------------------------------

    scoring_df["cfo_pat_ratio"] = np.where(
        scoring_df["net_profit"] > 0,
        scoring_df["cash_from_operations_cr"] / scoring_df["net_profit"],
        np.nan,
    )

    # --------------------------------------------------
    # FCF Positive Flag
    # --------------------------------------------------

    scoring_df["fcf_positive"] = (
        scoring_df["free_cash_flow_cr"] > 0
    ).astype(int)

    return scoring_df

def winsorize_series(series: pd.Series) -> pd.Series:
    """
    Winsorize a numeric series using the
    10th and 90th percentiles.
    """

    p10 = series.quantile(0.10)
    p90 = series.quantile(0.90)

    return series.clip(lower=p10, upper=p90)

def normalize_series(
    series: pd.Series,
    higher_is_better: bool = True
) -> pd.Series:
    """
    Normalize a winsorized series to a 0–100 scale.

    Parameters
    ----------
    series : pd.Series
        Winsorized metric.

    higher_is_better : bool
        True  -> higher values get higher scores.
        False -> lower values get higher scores.
    """

    min_value = series.min()
    max_value = series.max()

    if pd.isna(min_value) or pd.isna(max_value):
        return pd.Series(0.0, index=series.index)

    if max_value == min_value:
        return pd.Series(50.0, index=series.index)

    normalized = (
        (series - min_value)
        / (max_value - min_value)
    ) * 100

    if not higher_is_better:
        normalized = 100 - normalized

    return normalized
def calculate_weighted_score(
    df: pd.DataFrame,
    metrics: dict,
    higher_is_better: dict,
) -> pd.Series:
    """
    Calculate a weighted score for a group of metrics.
    """

    weighted_score = pd.Series(0.0, index=df.index)

    for metric, weight in metrics.items():

        series = winsorize_series(df[metric])

        series = normalize_series(
            series,
            higher_is_better=higher_is_better.get(metric, True)
        )

        series = series.fillna(0)

        weighted_score += (series * weight) / 100

    return weighted_score
def calculate_profitability_score(df: pd.DataFrame) -> pd.Series:
    """
    Calculate the profitability component of the composite score.
    Weight = 35%
    """

    return calculate_weighted_score(
        df=df,
        metrics={
            "return_on_equity_pct": 15,
            "return_on_capital_employed_pct": 10,
            "net_profit_margin_pct": 10,
        },
        higher_is_better={
            "return_on_equity_pct": True,
            "return_on_capital_employed_pct": True,
            "net_profit_margin_pct": True,
        },
    )
def calculate_cash_quality_score(df: pd.DataFrame) -> pd.Series:
    """
    Calculate the cash quality component of the composite score.
    Weight = 30%
    """

    return calculate_weighted_score(
        df=df,
        metrics={
            "free_cash_flow_cr": 15,
            "cfo_pat_ratio": 10,
            "fcf_positive": 5,
        },
        higher_is_better={
            "free_cash_flow_cr": True,
            "cfo_pat_ratio": True,
            "fcf_positive": True,
        },
    )
def calculate_growth_score(df: pd.DataFrame) -> pd.Series:
    """
    Calculate the growth component of the composite score.
    Weight = 20%
    """

    return calculate_weighted_score(
        df=df,
        metrics={
            "revenue_cagr_5yr": 10,
            "pat_cagr_5yr": 10,
        },
        higher_is_better={
            "revenue_cagr_5yr": True,
            "pat_cagr_5yr": True,
        },
    )
def calculate_leverage_score(df: pd.DataFrame) -> pd.Series:
    """
    Calculate the leverage component of the composite score.
    Weight = 15%
    """

    return calculate_weighted_score(
        df=df,
        metrics={
            "debt_to_equity": 10,
            "interest_coverage": 5,
        },
        higher_is_better={
            "debt_to_equity": False,
            "interest_coverage": True,
        },
    )
def calculate_composite_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the final composite quality score (0–100).
    """

    result = df.copy()

    result["profitability_score"] = calculate_profitability_score(result)
    result["cash_quality_score"] = calculate_cash_quality_score(result)
    result["growth_score"] = calculate_growth_score(result)
    result["leverage_score"] = calculate_leverage_score(result)

    result["composite_quality_score"] = (
        result["profitability_score"]
        + result["cash_quality_score"]
        + result["growth_score"]
        + result["leverage_score"]
    )

    return result
def calculate_sector_relative_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate sector-relative composite scores.

    Each company's composite score is normalized
    within its own broad sector.
    """

    result = df.copy()

    result["sector_relative_score"] = (
        result
        .groupby("broad_sector")["composite_quality_score"]
        .transform(
            lambda x: normalize_series(
                winsorize_series(x)
            )
        )
    )

    return result