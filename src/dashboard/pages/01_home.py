import streamlit as st

import plotly.express as px

from src.dashboard.services.home_service import (
    get_dashboard_summary,
    get_sector_breakdown,
    get_top_quality_companies
)

from src.dashboard.services.home_service import get_dashboard_summary
st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")

st.title("🏠 Nifty100 Financial Analytics Dashboard")

selected_year = st.sidebar.selectbox(
    "Select Financial Year",
    options=[2019, 2020, 2021, 2022, 2023, 2024],
    index=5
)

st.sidebar.markdown("---")
st.sidebar.write(f"Selected Year: **{selected_year}**")

st.header("Dashboard Overview")
summary = get_dashboard_summary(selected_year)
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

with col1:
    st.metric("Average ROE", f"{summary['average_roe']} %")

with col2:
    st.metric("Median P/E", summary["median_pe"])

with col3:
    st.metric("Median D/E", summary["median_de"])

with col4:
    st.metric("Total Companies", summary["total_companies"])

with col5:
    st.metric("Median Revenue CAGR", f"{summary['median_revenue_cagr']} %")

with col6:
    st.metric("Debt-Free Companies", summary["debt_free_companies"])

st.markdown("---")
st.subheader("Sector Breakdown")

sector_df = get_sector_breakdown()

fig = px.pie(
    sector_df,
    names="broad_sector",
    values="company_count",
    hole=0.5,
    title="Company Distribution by Sector"
)

fig.update_traces(textposition="inside", textinfo="percent+label")

st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

st.subheader("🏆 Top 5 Companies by Composite Quality Score")

top_companies = get_top_quality_companies(selected_year)

top_companies = top_companies.rename(
    columns={
        "ticker": "Ticker",
        "company_name": "Company",
        "composite_quality_score": "Quality Score"
    }
)

st.dataframe(
    top_companies,
    use_container_width=True,
    hide_index=True
)