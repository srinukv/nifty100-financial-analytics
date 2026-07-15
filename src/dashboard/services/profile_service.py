import pandas as pd
import streamlit as st

from src.dashboard.utils.db import execute_query


def get_company_list():
    """
    Return all companies for the profile search dropdown.
    """

    query = """
    SELECT
        id AS ticker,
        company_name
    FROM companies
    ORDER BY company_name;
    """

    return execute_query(query)

def get_company_profile(ticker: str):
    """
    Return profile information for a company.
    """

    query = """
    SELECT
        c.id AS ticker,
        c.company_name,
        c.about_company,
        s.broad_sector,
        s.sub_sector
    FROM companies c
    LEFT JOIN sectors s
        ON c.id = s.company_id
    WHERE c.id = ?;
    """

    df = execute_query(query, (ticker,))

    if df.empty:
        return None

    return df.iloc[0]
def get_company_kpis(ticker: str):
    """
    Return latest KPI values for a company.
    """

    query = """
    SELECT
        return_on_equity_pct,
        return_on_capital_employed_pct,
        net_profit_margin_pct,
        debt_to_equity,
        revenue_cagr_5yr,
        free_cash_flow_cr
    FROM financial_ratios
    WHERE company_id = ?
    ORDER BY year DESC
    LIMIT 1;
    """

    df = execute_query(query, (ticker,))

    if df.empty:
        return None

    return df.iloc[0]

def get_revenue_profit_history(ticker: str):
    """
    Return Revenue and Net Profit history for a company.
    """

    query = """
    SELECT
    year,
    sales,
    net_profit
FROM profitandloss
WHERE company_id = ?
  AND year IS NOT NULL
ORDER BY year;
    """

    return execute_query(query, (ticker,))

@st.cache_data(ttl=600)
def get_profitability_history(ticker: str):
    """
    Return historical profitability metrics.
    """

    query = """
    SELECT
        year,
        return_on_equity_pct,
        return_on_capital_employed_pct,
        net_profit_margin_pct
    FROM financial_ratios
    WHERE company_id = ?
    ORDER BY year;
    """

    return execute_query(query, (ticker,))

@st.cache_data(ttl=600)
def get_balance_sheet_highlights(ticker: str):
    """
    Return latest balance sheet highlights.
    """

    query = """
    SELECT
        total_assets,
        total_liabilities,
        equity_capital,
        reserves,
        borrowings,
        investments
    FROM balancesheet
    WHERE company_id = ?
    ORDER BY year DESC
    LIMIT 1;
    """

    df = execute_query(query, (ticker,))

    if df.empty:
        return None

    return df.iloc[0]

@st.cache_data(ttl=600)
def get_cashflow_highlights(ticker: str):
    """
    Returns latest cash flow highlights for a company.
    """

    query = """
    SELECT
        operating_activity,
        investing_activity,
        financing_activity,
        net_cash_flow
    FROM cashflow
    WHERE company_id = ?
    ORDER BY year DESC
    LIMIT 1;
    """

    df = execute_query(query, (ticker,))

    if df.empty:
        return None

    return df.iloc[0]