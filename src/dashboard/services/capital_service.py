import streamlit as st
import pandas as pd

from src.dashboard.utils.db import execute_query
@st.cache_data(ttl=600)
def get_capital_allocation_data():

    query = """
    SELECT

        c.id,
        c.company_name,

        fr.return_on_equity_pct,
        fr.return_on_capital_employed_pct,
        fr.debt_to_equity,
        fr.free_cash_flow_cr,
        fr.capex_cr,
        fr.dividend_payout_ratio_pct,
        fr.revenue_cagr_5yr

    FROM companies c

    JOIN financial_ratios fr
        ON c.id = fr.company_id

    WHERE fr.rowid = (
    SELECT MIN(rowid)
    FROM financial_ratios f2
    WHERE
        f2.company_id = fr.company_id
        AND f2.year = (
            SELECT MAX(year)
            FROM financial_ratios
            WHERE company_id = fr.company_id
        )
)
    """

    df = execute_query(query)
    df = df.drop_duplicates(subset=["id"])

    return classify_patterns(df)

def classify_patterns(df):

    pattern = []

    for _, row in df.iterrows():

        if row["free_cash_flow_cr"] > 1000 and row["debt_to_equity"] < 0.5:
            pattern.append("Cash Generator")

        elif row["revenue_cagr_5yr"] > 15:
            pattern.append("Growth Leader")

        elif (
            row["return_on_equity_pct"] > 20
            and row["return_on_capital_employed_pct"] > 20
        ):
            pattern.append("Profit Compounder")

        elif row["dividend_payout_ratio_pct"] > 40:
            pattern.append("Income Distributor")

        elif row["debt_to_equity"] > 2:
            pattern.append("Debt Heavy")

        elif row["capex_cr"] > 5000:
            pattern.append("Capital Intensive")

        elif (
            row["return_on_equity_pct"] < 10
            and row["free_cash_flow_cr"] > 0
        ):
            pattern.append("Turnaround Candidate")

        else:
            pattern.append("Balanced Performer")

    df["pattern"] = pattern

    return df