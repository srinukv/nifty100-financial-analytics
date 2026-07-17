import streamlit as st

from src.dashboard.utils.db import execute_query


@st.cache_data(ttl=600)
def get_screener_data():
    """
    Load latest screener dataset.
    """
    query = """
SELECT
    fr.company_id,
    c.company_name,
    s.broad_sector,
    fr.return_on_equity_pct,
    fr.debt_to_equity,
    fr.free_cash_flow_cr,
    fr.revenue_cagr_5yr,
    fr.pat_cagr_5yr,
    fr.operating_profit_margin_pct,
    fr.interest_coverage,
    fr.composite_quality_score

FROM financial_ratios fr

JOIN companies c
    ON fr.company_id = c.id

LEFT JOIN sectors s
    ON fr.company_id = s.company_id

WHERE fr.rowid IN (
    SELECT MIN(rowid)
    FROM financial_ratios
    WHERE year = (
        SELECT MAX(year)
        FROM financial_ratios
    )
    GROUP BY company_id
)

ORDER BY fr.composite_quality_score DESC;
    """

    return execute_query(query)

def apply_filters(
    df,
    roe_min,
    de_max,
    fcf_min,
    revenue_cagr_min,
    pat_cagr_min,
    opm_min,
    icr_min,
):
    """
    Apply screener filters.
    """

    filtered = df.copy()

    filtered = filtered[
        (filtered["return_on_equity_pct"] >= roe_min)
        & (filtered["debt_to_equity"] <= de_max)
        & (filtered["free_cash_flow_cr"] >= fcf_min)
        & (filtered["revenue_cagr_5yr"] >= revenue_cagr_min)
        & (filtered["pat_cagr_5yr"] >= pat_cagr_min)
        & (filtered["operating_profit_margin_pct"] >= opm_min)
        & (filtered["interest_coverage"] >= icr_min)
    ]

    return filtered

PRESETS = {

    "Quality": {
        "roe_min": 20,
        "de_max": 1,
        "fcf_min": 0,
        "revenue_cagr_min": 10,
        "pat_cagr_min": 10,
        "opm_min": 15,
        "icr_min": 3,
    },

    "Growth": {
        "roe_min": 15,
        "de_max": 2,
        "fcf_min": 0,
        "revenue_cagr_min": 20,
        "pat_cagr_min": 20,
        "opm_min": 10,
        "icr_min": 2,
    },

    "Dividend": {
        "roe_min": 15,
        "de_max": 2,
        "fcf_min": 0,
        "revenue_cagr_min": 5,
        "pat_cagr_min": 5,
        "opm_min": 10,
        "icr_min": 2,
    },

    "Debt-Free": {
        "roe_min": 15,
        "de_max": 0.20,
        "fcf_min": 0,
        "revenue_cagr_min": 5,
        "pat_cagr_min": 5,
        "opm_min": 10,
        "icr_min": 3,
    },

    "Turnaround": {
        "roe_min": 5,
        "de_max": 3,
        "fcf_min": -10000,
        "revenue_cagr_min": 5,
        "pat_cagr_min": 5,
        "opm_min": 5,
        "icr_min": 1,
    },

    "Value": {
        "roe_min": 15,
        "de_max": 1,
        "fcf_min": 0,
        "revenue_cagr_min": 5,
        "pat_cagr_min": 5,
        "opm_min": 10,
        "icr_min": 3,
    },
}