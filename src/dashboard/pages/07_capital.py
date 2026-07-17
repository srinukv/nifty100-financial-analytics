import streamlit as st
import plotly.express as px

from src.dashboard.services.capital_service import (
    get_capital_allocation_data,
)

st.set_page_config(
    page_title="Capital Allocation Map",
    layout="wide"
)

st.title("💰 Capital Allocation Map")

# --------------------------------------------------
# Load Data
# --------------------------------------------------

df = get_capital_allocation_data()

# Treemap requires positive values
df["treemap_size"] = (
    df["free_cash_flow_cr"]
    .fillna(0)
    .abs()
    + 1
)

# --------------------------------------------------
# Treemap
# --------------------------------------------------

fig = px.treemap(
    df,
    path=["pattern", "company_name"],
    values="treemap_size",
    color="pattern",
    hover_name="company_name",
    hover_data={
        "id": True,
        "return_on_equity_pct": ":.2f",
        "debt_to_equity": ":.2f",
        "revenue_cagr_5yr": ":.2f",
        "free_cash_flow_cr": ":,.0f",
    },
)

fig.update_layout(
    height=750,
    margin=dict(t=40, l=10, r=10, b=10),
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Pattern Selection
# --------------------------------------------------

st.divider()

selected_pattern = st.selectbox(
    "Select Capital Allocation Pattern",
    sorted(df["pattern"].unique())
)

filtered = (
    df[df["pattern"] == selected_pattern]
    .sort_values("company_name")
    .copy()
)

# Round numeric columns
numeric_cols = [
    "return_on_equity_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
]

for col in numeric_cols:
    filtered[col] = filtered[col].round(2)

st.subheader(f"{selected_pattern} Companies")

st.dataframe(
    filtered[
        [
            "id",
            "company_name",
            "return_on_equity_pct",
            "debt_to_equity",
            "free_cash_flow_cr",
            "revenue_cagr_5yr",
        ]
    ],
    hide_index=True,
    use_container_width=True,
)