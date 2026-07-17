import streamlit as st

from src.dashboard.utils.db import execute_query

@st.cache_data(ttl=600)
def get_sector_list():

    query = """
    SELECT DISTINCT
        broad_sector
    FROM sectors
    ORDER BY broad_sector;
    """

    return execute_query(query)

@st.cache_data(ttl=600)
def get_sector_bubble_data(sector):

    query = """
    SELECT
        c.id AS company_id,
        c.company_name,

        s.broad_sector,
        s.sub_sector,

        p.sales AS revenue,

        fr.return_on_equity_pct AS roe,

        mc.market_cap_crore

    FROM companies c

    JOIN sectors s
        ON c.id = s.company_id

    JOIN profitandloss p
        ON c.id = p.company_id

    JOIN financial_ratios fr
        ON c.id = fr.company_id
        AND fr.year = p.year

    JOIN market_cap mc
        ON c.id = mc.company_id
        AND mc.year = p.year

    WHERE
        s.broad_sector = ?
        AND p.year = (
            SELECT MAX(year)
            FROM profitandloss
            WHERE company_id = c.id
        )

    ORDER BY revenue DESC;
    """

    return execute_query(query, (sector,))

@st.cache_data(ttl=600)
def get_sector_median_kpis(sector):

    query = """
    SELECT
        fr.return_on_equity_pct,
        fr.return_on_capital_employed_pct,
        fr.net_profit_margin_pct,
        fr.debt_to_equity,
        fr.interest_coverage

    FROM financial_ratios fr

    JOIN sectors s
        ON fr.company_id = s.company_id

    WHERE
        s.broad_sector = ?
        AND fr.year = (
            SELECT MAX(year)
            FROM financial_ratios
            WHERE company_id = fr.company_id
        );
    """

    df = execute_query(query, (sector,))

    return {
    "ROE": float(round(df["return_on_equity_pct"].median(), 2)),
    "ROCE": float(round(df["return_on_capital_employed_pct"].median(), 2)),
    "Net Profit Margin": float(round(df["net_profit_margin_pct"].median(), 2)),
    "Debt / Equity": float(round(df["debt_to_equity"].median(), 2)),
    "Interest Coverage": float(round(df["interest_coverage"].median(), 2)),
}