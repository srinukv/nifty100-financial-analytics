import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Existing SQLite database
DB_PATH = PROJECT_ROOT / "nifty100.db"


def execute_query(query: str, params: tuple = ()) -> pd.DataFrame:
    """
    Execute a SQL query and return the result as a Pandas DataFrame.
    """
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(query, conn, params=params)
@st.cache_data(ttl=600)
@st.cache_data(ttl=600)
def get_companies() -> pd.DataFrame:
    """
    Return all companies ordered by ticker.
    """
    query = """
    SELECT *
    FROM companies
    ORDER BY id;
    """
    return execute_query(query)

@st.cache_data(ttl=600)
def get_ratios(ticker: str, year: int | None = None) -> pd.DataFrame:
    """
    Return financial ratios for a company.

    If year is None, return all available years (latest first).
    Otherwise, return data for the specified year.
    """
    if year is None:
        query = """
        SELECT *
        FROM financial_ratios
        WHERE company_id = ?
        ORDER BY year DESC;
        """
        return execute_query(query, (ticker,))

    query = """
    SELECT *
    FROM financial_ratios
    WHERE company_id = ?
      AND year = ?;
    """

    return execute_query(query, (ticker, year))

def get_latest_year(table: str, ticker: str) -> int | None:
    """
    Return the latest available year for a company in the given table.
    """
    query = f"""
    SELECT MAX(year) AS latest_year
    FROM {table}
    WHERE company_id = ?;
    """

    df = execute_query(query, (ticker,))

    if df.empty or df.loc[0, "latest_year"] is None:
        return None

    return int(df.loc[0, "latest_year"])

@st.cache_data(ttl=600)
def get_pl(ticker: str, year: int | None = None) -> pd.DataFrame:
    """
    Return Profit & Loss data for a company.
    If year is None, return the latest available year.
    """
    if year is None:
        year = get_latest_year("profitandloss", ticker)

    query = """
    SELECT *
    FROM profitandloss
    WHERE company_id = ?
      AND year = ?;
    """

    return execute_query(query, (ticker, year))

@st.cache_data(ttl=600)
def get_bs(ticker: str, year: int | None = None) -> pd.DataFrame:
    """
    Return Balance Sheet data for a company.
    If year is None, return the latest available year.
    """
    if year is None:
        year = get_latest_year("balancesheet", ticker)

    query = """
    SELECT *
    FROM balancesheet
    WHERE company_id = ?
      AND year = ?;
    """

    return execute_query(query, (ticker, year))

@st.cache_data(ttl=600)
def get_cf(ticker: str, year: int | None = None) -> pd.DataFrame:
    """
    Return Cash Flow data for a company.
    If year is None, return the latest available year.
    """
    if year is None:
        year = get_latest_year("cashflow", ticker)

    query = """
    SELECT *
    FROM cashflow
    WHERE company_id = ?
      AND year = ?;
    """

    return execute_query(query, (ticker, year))

@st.cache_data(ttl=600)
def get_sectors() -> pd.DataFrame:
    """
    Return sector mapping for all companies.
    """
    query = """
    SELECT *
    FROM sectors
    ORDER BY broad_sector, company_id;
    """

    return execute_query(query)
@st.cache_data(ttl=600)
def get_peers(group_name: str) -> pd.DataFrame:
    """
    Return all companies belonging to a peer group.
    """
    query = """
    SELECT
        pg.peer_group_name,
        pg.company_id,
        pg.is_benchmark,
        c.company_name
    FROM peer_groups pg
    JOIN companies c
        ON pg.company_id = c.id
    WHERE pg.peer_group_name = ?
    ORDER BY
        pg.is_benchmark DESC,
        pg.company_id;
    """

    return execute_query(query, (group_name,))

@st.cache_data(ttl=600)
def get_valuation(ticker: str) -> pd.DataFrame:
    """
    Placeholder for the Sprint 4 valuation engine.

    This function will be implemented after the valuation
    module is completed (Days 23–28).
    """
    return pd.DataFrame()