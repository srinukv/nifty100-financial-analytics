import sqlite3

import pandas as pd
import yaml
DB_PATH = "nifty100.db"

LATEST_YEAR_QUERY = """
SELECT MAX(year) AS latest_year
FROM financial_ratios
WHERE year IS NOT NULL;
"""
MASTER_SCREENER_QUERY = """
SELECT
    fr.company_id,
    c.company_name,
    s.broad_sector,
    s.sub_sector,

    fr.year,

    fr.return_on_equity_pct,
    fr.return_on_capital_employed_pct,
    fr.net_profit_margin_pct,
    fr.operating_profit_margin_pct,
    fr.debt_to_equity,
    fr.interest_coverage,
    fr.asset_turnover,
    fr.free_cash_flow_cr,
    fr.cash_from_operations_cr,
    fr.revenue_cagr_5yr,
    fr.pat_cagr_5yr,
    fr.eps_cagr_5yr,
    fr.composite_quality_score,

    mc.market_cap_crore,
    mc.pe_ratio,
    mc.pb_ratio,
    mc.dividend_yield_pct,

    pl.sales,
    pl.net_profit,
    pl.dividend_payout

FROM financial_ratios fr

LEFT JOIN companies c
    ON fr.company_id = c.id

LEFT JOIN sectors s
    ON fr.company_id = s.company_id

LEFT JOIN market_cap mc
    ON fr.company_id = mc.company_id
    AND fr.year = mc.year

LEFT JOIN profitandloss pl
    ON fr.company_id = pl.company_id
    AND fr.year = pl.year

WHERE fr.year = ?
"""
OPERATORS = {
    ">=": lambda series, value: series >= value,
    "<=": lambda series, value: series <= value,
    ">": lambda series, value: series > value,
    "<": lambda series, value: series < value,
    "==": lambda series, value: series == value,
}

def get_latest_year(conn: sqlite3.Connection) -> int:
    """
    Return the latest financial year available in the
    financial_ratios table.
    """
    cursor = conn.cursor()
    cursor.execute(LATEST_YEAR_QUERY)

    result = cursor.fetchone()

    if result is None or result[0] is None:
        raise ValueError("No financial year found in financial_ratios table.")

    return int(result[0])

def load_master_dataframe() -> pd.DataFrame:
    """
    Load the latest-year master screener dataset
    from the SQLite database.
    """

    conn = sqlite3.connect(DB_PATH)

    try:
        latest_year = get_latest_year(conn)

        df = pd.read_sql_query(
            MASTER_SCREENER_QUERY,
            conn,
            params=(latest_year,)
        )
        validate_master_dataframe(df)
        return df

    finally:
        conn.close()

def validate_master_dataframe(df: pd.DataFrame) -> None:
    """
    Validate the master screener dataset before
    applying any screening filters.
    """

    duplicates = df[df.duplicated(
        subset=["company_id", "year"],
        keep=False
    )]

    if not duplicates.empty:
        print(
            f"Warning: Found {duplicates['company_id'].nunique()} companies "
            f"with duplicate company-year records "
            f"({len(duplicates)} rows)."
        )

        print("\nDuplicate Companies:")

        print(
            duplicates[
                ["company_id", "company_name", "year"]
            ].drop_duplicates()
            .sort_values("company_id")
        )
def load_screener_config(config_path: str = "config/screener_config.yaml") -> dict:
    """
    Load screener configuration from a YAML file.
    """

    with open(config_path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

def apply_single_filter(
    df: pd.DataFrame,
    column: str,
    operator: str,
    value
) -> pd.DataFrame:
    """
    Apply a single filter to the DataFrame.
    """

    if column not in df.columns:
        raise KeyError(
            f"Column '{column}' not found in screener dataset."
        )

    if operator not in OPERATORS:
        raise ValueError(
            f"Unsupported operator: {operator}"
        )

    # Special business rule for Debt-to-Equity
    if column == "debt_to_equity":

        financial_df = df[
        df["broad_sector"] == "Financials"
    ]

        non_financial_df = df[
        df["broad_sector"] != "Financials"
    ]

        mask = OPERATORS[operator](
        non_financial_df[column],
        value
    )

        filtered_non_financial = non_financial_df[mask]

        return pd.concat(
        [financial_df, filtered_non_financial],
        ignore_index=True
    )

# Default filtering
    mask = OPERATORS[operator](
    df[column],
    value
)

    return df[mask]

def apply_filters(
    df: pd.DataFrame,
    config: dict
) -> pd.DataFrame:
    """
    Apply screening filters to the master screener DataFrame.
    """

    filtered_df = df.copy()
    filters = config["filters"]
    for column, rule in filters.items():

        operator = rule.get("operator")
        value = rule.get("value")

    # Skip filters that are disabled
        if value is None:
            continue

    # Validate column
        if column not in filtered_df.columns:
            raise KeyError(
            f"Column '{column}' not found in screener dataset."
        )

    # Validate operator
        if operator not in OPERATORS:
            raise ValueError(
            f"Unsupported operator: {operator}"
        )

    # Apply filter
        filtered_df = apply_single_filter(
    filtered_df,
    column,
    operator,
    value
)

    return (
    filtered_df
    .sort_values(
        by="composite_quality_score",
        ascending=False,
        na_position="last"
    )
    .reset_index(drop=True)
)

def prepare_analytics_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare the master dataset for analytics.
    Removes exact duplicate company-year records.
    """

    original_rows = len(df)

    cleaned_df = (
        df.drop_duplicates(
            subset=["company_id", "year"],
            keep="first"
        )
        .reset_index(drop=True)
    )

    removed_rows = original_rows - len(cleaned_df)

    print(
        f"Analytics Dataset Prepared: "
        f"{len(cleaned_df)} rows "
        f"({removed_rows} duplicate rows removed)"
    )

    return cleaned_df

from src.screener.presets import get_preset


def run_preset_screener(df, preset_name):
    """
    Execute a preset screener on an analytics DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        Analytics dataset.

    preset_name : str
        Name of the preset screener.

    Returns
    -------
    pandas.DataFrame
        Filtered and sorted DataFrame.
    """
    from src.screener.presets import get_preset


def run_preset_screener(df, preset_name):
    """
    Execute a preset screener using the existing filter engine.
    """

    preset_filters = get_preset(preset_name)

    config = {
        "filters": preset_filters
    }

    return apply_filters(df, config)