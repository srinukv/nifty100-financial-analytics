"""
NLP Analysis Text Parser

Parses analysis.xlsx using regex and
converts text metrics into structured data.
"""

import re
import sqlite3
from pathlib import Path

import pandas as pd

INPUT_FILE = Path("data/raw/analysis.xlsx")
OUTPUT_DIR = Path("output")

OUTPUT_DIR.mkdir(exist_ok=True)


def load_analysis_data():
    """Load and clean analysis.xlsx"""

    df = pd.read_excel(INPUT_FILE, header=None)

    # Second row contains actual column names
    df.columns = df.iloc[1]

    # Remove title + header rows
    df = df.iloc[2:].reset_index(drop=True)

    return df

PATTERN = re.compile(
    r"(\d+)\s*Years?:?\s*(-?[\d.]+)%"
)

def parse_metric(text):
    """
    Parse text like:
    10 Years: 21%

    Returns:
        (10,21.0)
    """

    if pd.isna(text):
        return None

    match = PATTERN.search(str(text))

    if not match:
        return None

    return (
        int(match.group(1)),
        float(match.group(2)),
    )

TARGET_COLUMNS = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe",
]


def build_parsed_dataframe(df):

    parsed_rows = []
    failed_rows = []

    for _, row in df.iterrows():

        company = row["company_id"]

        for metric in TARGET_COLUMNS:

            result = parse_metric(row[metric])

            if result is None:

                failed_rows.append({
                    "company_id": company,
                    "metric_type": metric,
                    "original_text": row[metric],
                })

                continue

            years, value = result

            parsed_rows.append({
                "company_id": company,
                "metric_type": metric,
                "period_years": years,
                "value_pct": value,
            })

    parsed_df = pd.DataFrame(parsed_rows)
    failed_df = pd.DataFrame(failed_rows)

    return parsed_df, failed_df

def save_outputs(parsed_df, failed_df):

    parsed_df.to_csv(
        OUTPUT_DIR / "analysis_parsed.csv",
        index=False,
    )

    failed_df.to_csv(
        OUTPUT_DIR / "parse_failures.csv",
        index=False,
    )

    print("analysis_parsed.csv generated")

    print("parse_failures.csv generated")

def cross_validate(parsed_df):
    """
    Compare parsed values with Ratio Engine values.
    Flag differences greater than 5%.
    """

    conn = sqlite3.connect("nifty100.db")

    ratios = pd.read_sql_query("""
        SELECT
            company_id,
            year,
            revenue_cagr_5yr,
            pat_cagr_5yr,
            return_on_equity_pct
        FROM financial_ratios
        WHERE year = (
            SELECT MAX(year)
            FROM financial_ratios f2
            WHERE f2.company_id = financial_ratios.company_id
        )
    """, conn)

    conn.close()

    metric_map = {
        "compounded_sales_growth": "revenue_cagr_5yr",
        "compounded_profit_growth": "pat_cagr_5yr",
        "roe": "return_on_equity_pct",
    }

    review_rows = []

    for _, row in parsed_df.iterrows():

        metric = row["metric_type"]

        if metric not in metric_map:
            continue

        db_col = metric_map[metric]

        company = row["company_id"]

        match = ratios[
            ratios["company_id"] == company
        ]

        if match.empty:
            continue

        db_value = match.iloc[0][db_col]

        if pd.isna(db_value):
            continue

        parsed_value = row["value_pct"]

        difference = abs(parsed_value - db_value)

        if difference > 5:

            review_rows.append({
                "company_id": company,
                "metric_type": metric,
                "parsed_value": parsed_value,
                "ratio_engine_value": db_value,
                "difference": round(difference, 2),
            })

    review_df = pd.DataFrame(review_rows)

    review_df.to_csv(
        OUTPUT_DIR / "manual_review.csv",
        index=False,
    )

    print("manual_review.csv generated")

def main():

    df = load_analysis_data()

    parsed_df, failed_df = build_parsed_dataframe(df)

    save_outputs(parsed_df, failed_df)

    cross_validate(parsed_df)


if __name__ == "__main__":
    main()