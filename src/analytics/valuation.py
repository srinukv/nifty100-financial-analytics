import sqlite3
from pathlib import Path

import pandas as pd
DB_PATH = Path("nifty100.db")
OUTPUT_DIR = Path("output")

OUTPUT_DIR.mkdir(exist_ok=True)
def get_connection():
    return sqlite3.connect(DB_PATH)

def load_latest_valuation_data():

    query = """
    SELECT

        mc.company_id,
        c.company_name,

        s.broad_sector,

        mc.year,

        mc.market_cap_crore,
        mc.pe_ratio,
        mc.pb_ratio,
        mc.ev_ebitda,

        fr.free_cash_flow_cr

    FROM market_cap mc

    JOIN companies c
        ON mc.company_id = c.id

    JOIN sectors s
        ON mc.company_id = s.company_id

    JOIN financial_ratios fr
        ON mc.company_id = fr.company_id
        AND mc.year = fr.year

    WHERE mc.rowid = (

        SELECT MIN(rowid)

        FROM market_cap x

        WHERE
            x.company_id = mc.company_id
            AND x.year = (

                SELECT MAX(year)

                FROM market_cap

                WHERE company_id = mc.company_id
            )
    )

    AND fr.rowid = (

        SELECT MIN(rowid)

        FROM financial_ratios y

        WHERE
            y.company_id = fr.company_id
            AND y.year = fr.year
    );
    """

    conn = get_connection()

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df

def calculate_fcf_yield(df):
    """
    Calculate Free Cash Flow Yield (%)
    """

    df = df.copy()

    df["fcf_yield_pct"] = (
        df["free_cash_flow_cr"]
        / df["market_cap_crore"]
    ) * 100

    df["fcf_yield_pct"] = df["fcf_yield_pct"].round(2)

    return df

def calculate_sector_median_pe(df):
    """
    Calculate median P/E for each broad sector.
    """

    sector_median = (
        df.groupby("broad_sector")["pe_ratio"]
        .median()
        .round(2)
        .rename("sector_median_pe")
    )

    df = df.merge(
        sector_median,
        on="broad_sector",
        how="left",
    )

    return df

def apply_valuation_flags(df):
    """
    Compare company P/E against its sector median and assign valuation flags.
    """

    df = df.copy()

    # Percentage difference from sector median
    df["pe_vs_sector_median_pct"] = (
        (df["pe_ratio"] - df["sector_median_pe"])
        / df["sector_median_pe"]
    ) * 100

    df["pe_vs_sector_median_pct"] = df[
        "pe_vs_sector_median_pct"
    ].round(2)

    # Default flag
    df["flag"] = "Fair"

    # Overvalued
    df.loc[
        df["pe_ratio"] > (df["sector_median_pe"] * 1.5),
        "flag"
    ] = "Caution"

    # Undervalued
    df.loc[
        df["pe_ratio"] < (df["sector_median_pe"] * 0.7),
        "flag"
    ] = "Discount"

    return df

def calculate_five_year_median_pe(df):
    """
    Calculate the median P/E ratio for each company over the latest 5 years.
    """

    conn = get_connection()

    query = """
    SELECT
        company_id,
        year,
        pe_ratio
    FROM market_cap
    WHERE year >= (
        SELECT MAX(year) - 4
        FROM market_cap
    )
    """

    pe_df = pd.read_sql_query(query, conn)
    conn.close()

    five_year_pe = (
        pe_df.groupby("company_id")["pe_ratio"]
        .median()
        .round(2)
        .rename("five_year_median_pe")
    )

    df = df.merge(
        five_year_pe,
        on="company_id",
        how="left"
    )

    return df

def export_valuation_reports(df):
    """
    Generate valuation_summary.xlsx and valuation_flags.csv.
    """

    summary = df[
        [
            "company_id",
            "company_name",
            "broad_sector",
            "pe_ratio",
            "pb_ratio",
            "ev_ebitda",
            "fcf_yield_pct",
            "five_year_median_pe",
            "pe_vs_sector_median_pct",
            "flag",
        ]
    ].copy()

    summary = summary.rename(
        columns={
            "broad_sector": "sector",
            "pe_ratio": "P/E",
            "pb_ratio": "P/B",
            "ev_ebitda": "EV/EBITDA",
            "fcf_yield_pct": "FCF_yield_pct",
            "five_year_median_pe": "5yr_median_PE",
            "pe_vs_sector_median_pct": "PE_vs_sector_median_pct",
        }
    )

    summary.to_excel(
        OUTPUT_DIR / "valuation_summary.xlsx",
        index=False,
    )

    flags = summary[
        summary["flag"].isin(["Caution", "Discount"])
    ]

    flags.to_csv(
        OUTPUT_DIR / "valuation_flags.csv",
        index=False,
    )

    print("✓ valuation_summary.xlsx created")
    print("✓ valuation_flags.csv created")