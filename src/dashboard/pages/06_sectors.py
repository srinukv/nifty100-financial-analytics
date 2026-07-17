import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from src.dashboard.services.sector_service import (
    get_sector_list,
    get_sector_bubble_data,
    get_sector_median_kpis,
)

st.set_page_config(page_title="Sector Analysis", layout="wide")

st.title("🏭 Sector Analysis")

# -----------------------------
# Sector Dropdown
# -----------------------------

sector_df = get_sector_list()

selected_sector = st.selectbox(
    "Select Sector",
    sector_df["broad_sector"]
)

# -----------------------------
# Bubble Chart
# -----------------------------

bubble_df = get_sector_bubble_data(selected_sector)

fig = px.scatter(
    bubble_df,
    x="revenue",
    y="roe",
    size="market_cap_crore",
    color="sub_sector",
    hover_name="company_name",
    hover_data={
        "company_id": True,
        "revenue": ":,.0f",
        "roe": ":.2f",
        "market_cap_crore": ":,.0f",
    },
    title=f"{selected_sector} Sector Comparison",
)

fig.update_layout(height=650)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Sector Median KPI Chart
# -----------------------------

st.subheader("Sector Median KPIs")

kpis = get_sector_median_kpis(selected_sector)

bar = go.Figure(
    go.Bar(
        x=list(kpis.keys()),
        y=list(kpis.values()),
        text=[f"{v:.2f}" for v in kpis.values()],
        textposition="outside",
    )
)

bar.update_layout(
    height=450,
    yaxis_title="Median Value",
)

st.plotly_chart(bar, use_container_width=True)