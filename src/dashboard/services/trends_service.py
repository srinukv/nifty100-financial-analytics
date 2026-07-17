import streamlit as st

from src.dashboard.utils.db import execute_query

@st.cache_data(ttl=600)
def get_company_list():
    query = """
    SELECT
        id AS company_id,
        company_name
    FROM companies
    ORDER BY company_name;
    """

    df = execute_query(query)

    df["display_name"] = (
        df["company_id"] +
        " - " +
        df["company_name"]
    )

    return df
METRICS = {
    "Sales": ("profitandloss", "sales"),
    "Net Profit": ("profitandloss", "net_profit"),
    "Operating Profit": ("profitandloss", "operating_profit"),
    "EPS": ("profitandloss", "eps"),
    "ROE": ("financial_ratios", "return_on_equity_pct"),
    "ROCE": ("financial_ratios", "return_on_capital_employed_pct"),
    "Net Profit Margin": ("financial_ratios", "net_profit_margin_pct"),
    "Operating Profit Margin": ("financial_ratios", "operating_profit_margin_pct"),
    "Free Cash Flow": ("financial_ratios", "free_cash_flow_cr"),
    "Debt / Equity": ("financial_ratios", "debt_to_equity"),
}

@st.cache_data(ttl=600)
def get_metric_history(company_id, metric_name):

    table, column = METRICS[metric_name]

    query = f"""
SELECT
    year,
    {column} AS value
FROM {table}
WHERE company_id = ?
  AND year IS NOT NULL
ORDER BY year;
"""

    return execute_query(query, (company_id,))