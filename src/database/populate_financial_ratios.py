import sqlite3
import pandas as pd

from src.ratios.ratios import *
from src.ratios.cagr import *

DB_PATH = "nifty100.db"


def load_tables():

    conn = sqlite3.connect(DB_PATH)

    pnl = pd.read_sql(
        "SELECT * FROM profitandloss",
        conn
    )

    bs = pd.read_sql(
        "SELECT * FROM balancesheet",
        conn
    )

    cf = pd.read_sql(
        "SELECT * FROM cashflow",
        conn
    )

    fr = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    return conn, pnl, bs, cf, fr
def merge_tables(pnl, bs, cf):

    merged = pnl.merge(
        bs,
        on=["company_id", "year"],
        how="left"
    )

    merged = merged.merge(
        cf,
        on=["company_id", "year"],
        how="left"
    )

    return merged

def calculate_basic_ratios(df):

    df["net_profit_margin_pct"] = df.apply(
        lambda row: calculate_npm(
            row["net_profit"],
            row["sales"]
        ),
        axis=1
    )

    df["operating_profit_margin_pct"] = df.apply(
        lambda row: calculate_opm(
            row["operating_profit"],
            row["sales"]
        ),
        axis=1
    )

    df["return_on_equity_pct"] = df.apply(
        lambda row: calculate_roe(
            row["net_profit"],
            row["equity_capital"],
            row["reserves"]
        ),
        axis=1
    )
    df["return_on_capital_employed_pct"] = df.apply(
    lambda row: calculate_roce(
        row["operating_profit"],
        row["equity_capital"],
        row["reserves"],
        row["borrowings"]
    ),
    axis=1
)

    return df

def calculate_remaining_ratios(df):

    df["debt_to_equity"] = df.apply(
        lambda row: calculate_debt_to_equity(
            row["borrowings"],
            row["equity_capital"],
            row["reserves"]
        ),
        axis=1
    )

    df["interest_coverage"] = df.apply(
        lambda row: calculate_interest_coverage(
            row["operating_profit"],
            row["other_income"],
            row["interest"]
        ),
        axis=1
    )

    df["asset_turnover"] = df.apply(
        lambda row: calculate_asset_turnover(
            row["sales"],
            row["total_assets"]
        ),
        axis=1
    )

    df["free_cash_flow_cr"] = df.apply(
        lambda row: calculate_free_cash_flow(
            row["operating_activity"],
            row["investing_activity"]
        ),
        axis=1
    )

    df["capex_cr"] = df["investing_activity"].abs()

    df["earnings_per_share"] = df["eps"]

    df["book_value_per_share"] = df.apply(
        lambda row: round(
            (row["equity_capital"] + row["reserves"]) / row["equity_capital"],
            2
        ) if row["equity_capital"] > 0 else None,
        axis=1
    )

    df["dividend_payout_ratio_pct"] = df["dividend_payout"]

    df["total_debt_cr"] = df["borrowings"]

    df["cash_from_operations_cr"] = df["operating_activity"]

    return df

def calculate_cagr_columns(df):

    df = df.sort_values(
        ["company_id", "year"]
    ).copy()

    df["revenue_cagr_5yr"] = None
    df["pat_cagr_5yr"] = None
    df["eps_cagr_5yr"] = None

    for company in df["company_id"].unique():

        company_df = df[
            df["company_id"] == company
        ]

        company_df = company_df.sort_values("year")

        indexes = company_df.index.tolist()

        for i in range(len(indexes)):

            if i < 5:
                continue

            current = indexes[i]
            previous = indexes[i - 5]

            revenue, _ = calculate_cagr(
                df.loc[previous, "sales"],
                df.loc[current, "sales"],
                5,
                5
            )

            pat, _ = calculate_cagr(
                df.loc[previous, "net_profit"],
                df.loc[current, "net_profit"],
                5,
                5
            )

            eps, _ = calculate_cagr(
                df.loc[previous, "eps"],
                df.loc[current, "eps"],
                5,
                5
            )

            df.loc[current, "revenue_cagr_5yr"] = revenue
            df.loc[current, "pat_cagr_5yr"] = pat
            df.loc[current, "eps_cagr_5yr"] = eps

    return df

def calculate_composite_quality_score(df):

    df["composite_quality_score"] = (
        df[
            [
                "return_on_equity_pct",
                "net_profit_margin_pct",
                "operating_profit_margin_pct",
                "revenue_cagr_5yr",
                "pat_cagr_5yr",
            ]
        ]
        .mean(axis=1)
        .round(2)
    )

    return df

def main():

    conn, pnl, bs, cf, fr = load_tables()

    print("Profit & Loss :", len(pnl))
    print("Balance Sheet :", len(bs))
    print("Cash Flow     :", len(cf))
    print("Financial Ratios :", len(fr))

    merged = merge_tables(
    pnl,
    bs,
    cf
    )
    valid_years = merged[
    merged["year"].notna()
    ].copy()
    valid_years["year"] = valid_years["year"].astype(int)

    valid_years = calculate_basic_ratios(valid_years)
    valid_years = calculate_remaining_ratios(valid_years)
    valid_years = calculate_cagr_columns(valid_years)
    valid_years = calculate_composite_quality_score(valid_years)
    cursor = conn.cursor()

    for _, row in valid_years.iterrows():

        cursor.execute(
        """
        UPDATE financial_ratios
        SET
            net_profit_margin_pct=?,
            operating_profit_margin_pct=?,
            return_on_equity_pct=?,
            return_on_capital_employed_pct=?,
            debt_to_equity=?,
            interest_coverage=?,
            asset_turnover=?,
            free_cash_flow_cr=?,
            capex_cr=?,
            earnings_per_share=?,
            book_value_per_share=?,
            dividend_payout_ratio_pct=?,
            total_debt_cr=?,
            cash_from_operations_cr=?,
            revenue_cagr_5yr=?,
            pat_cagr_5yr=?,
            eps_cagr_5yr=?,
            composite_quality_score=?
        WHERE
            company_id=?
            AND year=?
        """,
        (
            row["net_profit_margin_pct"],
            row["operating_profit_margin_pct"],
            row["return_on_equity_pct"],
            row["return_on_capital_employed_pct"],
            row["debt_to_equity"],
            row["interest_coverage"],
            row["asset_turnover"],
            row["free_cash_flow_cr"],
            row["capex_cr"],
            row["earnings_per_share"],
            row["book_value_per_share"],
            row["dividend_payout_ratio_pct"],
            row["total_debt_cr"],
            row["cash_from_operations_cr"],
            row["revenue_cagr_5yr"],
            row["pat_cagr_5yr"],
            row["eps_cagr_5yr"],
            row["composite_quality_score"],
            row["company_id"],
            row["year"],
        ),
    )

    conn.commit()

    print("\nFinancial ratios table updated successfully.")
    print("\nCAGR Sample:\n")

    print(
     valid_years[
            [
            "company_id",
            "year",
            "revenue_cagr_5yr",
            "pat_cagr_5yr",
            "eps_cagr_5yr"
            ]
        ].head(15)
    )
    print(
    valid_years[
        [
            "company_id",
            "year",
            "debt_to_equity",
            "interest_coverage",
            "asset_turnover",
            "free_cash_flow_cr",
            "book_value_per_share"
        ]
    ].head(10)
)
    print("\nCalculated Sample:\n")

    print(
    valid_years[
            [
            "company_id",
            "year",
            "net_profit_margin_pct",
            "operating_profit_margin_pct",
            "return_on_equity_pct",
            "return_on_capital_employed_pct"
            ]
        ].head(10)
    )
    print("\nMerged Rows :", len(merged))
    print("Valid Year Rows :", len(valid_years))
    print("\nMerged Columns:\n")

    print(valid_years.columns.tolist())

    conn.close()


if __name__ == "__main__":
    main()