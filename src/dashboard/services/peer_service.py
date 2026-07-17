import streamlit as st

from src.dashboard.utils.db import execute_query


@st.cache_data(ttl=600)
def get_peer_groups():
    """
    Returns all peer groups.
    """

    query = """
    SELECT DISTINCT peer_group_name
    FROM peer_percentiles
    ORDER BY peer_group_name;
    """

    df = execute_query(query)

    return df["peer_group_name"].tolist()

@st.cache_data(ttl=600)
def get_companies_in_peer_group(peer_group):
    """
    Return all companies belonging to a peer group.
    """

    query = """
    SELECT DISTINCT
        p.company_id,
        c.company_name
    FROM peer_percentiles p
    JOIN companies c
        ON p.company_id = c.id
    WHERE p.peer_group_name = ?
    ORDER BY c.company_name;
    """

    df = execute_query(query, (peer_group,))

    df["display_name"] = (
        df["company_id"] + " - " + df["company_name"]
    )

    return df

@st.cache_data(ttl=600)
def get_peer_comparison_data(company_id: str):
    """
    Return the selected company's metrics and the peer group average.
    """

    query = """
    SELECT
        company_id,
        metric,
        value
    FROM peer_percentiles
    WHERE company_id = ?
      AND year = (
            SELECT MAX(year)
            FROM peer_percentiles
      );
    """

    company_df = execute_query(query, (company_id,))

    if company_df.empty:
        return company_df, company_df

    peer_group = execute_query(
        """
        SELECT DISTINCT peer_group_name
        FROM peer_percentiles
        WHERE company_id = ?
        LIMIT 1;
        """,
        (company_id,),
    ).iloc[0, 0]

    peer_avg_query = """
    SELECT
        metric,
        AVG(value) AS value
    FROM peer_percentiles
    WHERE peer_group_name = ?
      AND year = (
            SELECT MAX(year)
            FROM peer_percentiles
      )
    GROUP BY metric;
    """

    peer_avg_df = execute_query(peer_avg_query, (peer_group,))

    return company_df, peer_avg_df

@st.cache_data(ttl=600)
def get_peer_table(peer_group):
    query = """
    SELECT DISTINCT
        p.company_id,
        c.company_name,
        fr.return_on_equity_pct,
        fr.return_on_capital_employed_pct,
        fr.net_profit_margin_pct,
        fr.debt_to_equity,
        fr.revenue_cagr_5yr,
        fr.pat_cagr_5yr,
        fr.free_cash_flow_cr,
        fr.composite_quality_score
    FROM peer_groups p
    JOIN companies c
        ON p.company_id = c.id
    JOIN financial_ratios fr
        ON p.company_id = fr.company_id
    WHERE
        p.peer_group_name = ?
        AND fr.year = (
            SELECT MAX(year)
            FROM financial_ratios
            WHERE company_id = fr.company_id
        )
    ORDER BY
        fr.composite_quality_score DESC;
    """

    df = execute_query(query, (peer_group,))

    # Remove duplicate companies
    df = df.drop_duplicates(
        subset=["company_id"],
        keep="first"
    )

    return df