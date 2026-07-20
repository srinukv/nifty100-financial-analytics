import streamlit as st
import plotly.graph_objects as go

from src.dashboard.services.peer_service import (
    get_peer_groups,
    get_companies_in_peer_group,
    get_peer_comparison_data,
    get_peer_table,
)

st.set_page_config(
    page_title="Peer Comparison",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Peer Comparison")

# --------------------------------------------------
# Peer Group Selection
# --------------------------------------------------

peer_groups = get_peer_groups()

selected_group = st.selectbox(
    "Select Peer Group",
    peer_groups,
)

# --------------------------------------------------
# Company Selection
# --------------------------------------------------

companies = get_companies_in_peer_group(selected_group)

selected_company = st.selectbox(
    "Select Company",
    companies["display_name"],
)

company_id = selected_company.split(" - ")[0]

st.success(f"Selected Peer Group : {selected_group}")
st.success(f"Selected Company : {company_id}")

# --------------------------------------------------
# Radar Chart
# --------------------------------------------------

company_df, peer_df = get_peer_comparison_data(company_id)

if company_df.empty:
    st.info(
        "Peer comparison data is not available for this company because sufficient historical data is not available."
    )
    st.stop()
company_metrics = company_df.set_index("metric")["value"]
peer_metrics = peer_df.set_index("metric")["value"]

metrics = sorted(
    list(set(company_metrics.index) & set(peer_metrics.index))
)

company_values = [company_metrics[m] for m in metrics]
peer_values = [peer_metrics[m] for m in metrics]

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=company_values,
        theta=metrics,
        fill="toself",
        name=company_id,
    )
)

fig.add_trace(
    go.Scatterpolar(
        r=peer_values,
        theta=metrics,
        fill="toself",
        name="Peer Average",
    )
)

fig.update_layout(
    title="Company vs Peer Group Average",
    polar=dict(
        radialaxis=dict(
            visible=True,
        )
    ),
    showlegend=True,
    height=650,
)

st.plotly_chart(fig, width="stretch")

# --------------------------------------------------
# Peer Comparison Table
# --------------------------------------------------

st.divider()

st.subheader("📋 Peer Comparison Table")

peer_table = get_peer_table(selected_group)

# Highlight selected company with a star
peer_table["Benchmark"] = peer_table["company_id"].apply(
    lambda x: "⭐" if x == company_id else ""
)

peer_table = peer_table[
    [
        "Benchmark",
        "company_id",
        "company_name",
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "free_cash_flow_cr",
        "composite_quality_score",
    ]
]

peer_table.columns = [
    "Benchmark",
    "Company ID",
    "Company Name",
    "ROE (%)",
    "ROCE (%)",
    "Net Profit Margin (%)",
    "Debt / Equity",
    "Revenue CAGR (5Y)",
    "PAT CAGR (5Y)",
    "Free Cash Flow (₹ Cr)",
    "Composite Score",
]
peer_table = peer_table.fillna("N/A")
numeric_columns = [
    "ROE (%)",
    "ROCE (%)",
    "Net Profit Margin (%)",
    "Debt / Equity",
    "Revenue CAGR (5Y)",
    "PAT CAGR (5Y)",
    "Free Cash Flow (₹ Cr)",
    "Composite Score",
]

peer_table[numeric_columns] = peer_table[numeric_columns].round(2)
st.dataframe(
    peer_table,
    width="stretch",
    hide_index=True,
)