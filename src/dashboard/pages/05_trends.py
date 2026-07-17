import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from src.dashboard.services.trends_service import (
    get_company_list,
    get_metric_history,
    METRICS,
)

st.set_page_config(page_title="Trend Analysis", layout="wide")

st.title("📈 Trend Analysis")

# -----------------------------
# Company Selection
# -----------------------------

companies = get_company_list()

selected_company = st.selectbox(
    "Select Company",
    companies["display_name"]
)

company_id = selected_company.split(" - ")[0]

# -----------------------------
# Metric Selection
# -----------------------------

selected_metrics = st.multiselect(
    "Select up to 3 metrics",
    list(METRICS.keys()),
    default=["Sales"],
    max_selections=3,
)

if not selected_metrics:
    st.warning("Please select at least one metric.")
    st.stop()
fig = go.Figure()

for metric in selected_metrics:

    df = get_metric_history(company_id, metric)

    # Calculate YoY %
    df["yoy"] = df["value"].pct_change() * 100

    # Annotation text
    text = []
    for val in df["yoy"]:
        if pd.isna(val):
            text.append("")
        else:
            text.append(f"{val:.1f}%")

    fig.add_trace(
        go.Scatter(
            x=df["year"],
            y=df["value"],
            mode="lines+markers+text",
            name=metric,
            text=text,
            textposition="top center",
        )
    )

fig.update_layout(
    title=f"{company_id} - Historical Trend",
    xaxis_title="Year",
    yaxis_title="Value",
    hovermode="x unified",
)

st.plotly_chart(fig, use_container_width=True)