import streamlit as st

from src.dashboard.services.screener_service import (
    get_screener_data,
    apply_filters,
    PRESETS,
)

st.set_page_config(
    page_title="Stock Screener",
    page_icon="🔍",
    layout="wide",
)

st.title("🔍 Nifty100 Stock Screener")

# ----------------------------
# Initialize Session State
# ----------------------------
if "filters" not in st.session_state:
    st.session_state.filters = PRESETS["Quality"].copy()

# ----------------------------
# Preset Buttons
# ----------------------------
st.sidebar.header("📌 Preset Screeners")

col1, col2 = st.sidebar.columns(2)
col3, col4 = st.sidebar.columns(2)
col5, col6 = st.sidebar.columns(2)

with col1:
    if st.button("Quality"):
        st.session_state.filters = PRESETS["Quality"].copy()
        st.rerun()

with col2:
    if st.button("Value"):
        st.session_state.filters = PRESETS["Value"].copy()
        st.rerun()

with col3:
    if st.button("Growth"):
        st.session_state.filters = PRESETS["Growth"].copy()
        st.rerun()

with col4:
    if st.button("Dividend"):
        st.session_state.filters = PRESETS["Dividend"].copy()
        st.rerun()

with col5:
    if st.button("Debt-Free"):
        st.session_state.filters = PRESETS["Debt-Free"].copy()
        st.rerun()

with col6:
    if st.button("Turnaround"):
        st.session_state.filters = PRESETS["Turnaround"].copy()
        st.rerun()

st.sidebar.divider()

# ----------------------------
# Filter Controls
# ----------------------------
st.sidebar.header("🎯 Screening Filters")

roe_min = st.sidebar.slider(
    "Minimum ROE (%)",
    min_value=0.0,
    max_value=60.0,
    value=float(st.session_state.filters["roe_min"]),
    step=1.0,
)

de_max = st.sidebar.slider(
    "Maximum Debt / Equity",
    min_value=0.0,
    max_value=5.0,
    value=float(st.session_state.filters["de_max"]),
    step=0.1,
)

fcf_min = st.sidebar.number_input(
    "Minimum Free Cash Flow (₹ Cr)",
    value=float(st.session_state.filters["fcf_min"]),
)

revenue_cagr_min = st.sidebar.slider(
    "Minimum Revenue CAGR (%)",
    min_value=0.0,
    max_value=50.0,
    value=float(st.session_state.filters["revenue_cagr_min"]),
    step=1.0,
)

pat_cagr_min = st.sidebar.slider(
    "Minimum PAT CAGR (%)",
    min_value=0.0,
    max_value=50.0,
    value=float(st.session_state.filters["pat_cagr_min"]),
    step=1.0,
)

opm_min = st.sidebar.slider(
    "Minimum Operating Profit Margin (%)",
    min_value=0.0,
    max_value=60.0,
    value=float(st.session_state.filters["opm_min"]),
    step=1.0,
)

icr_min = st.sidebar.slider(
    "Minimum Interest Coverage",
    min_value=0.0,
    max_value=500.0,
    value=float(st.session_state.filters["icr_min"]),
    step=1.0,
)

# ----------------------------
# Apply Filters
# ----------------------------
df = get_screener_data()

filtered_df = apply_filters(
    df,
    roe_min,
    de_max,
    fcf_min,
    revenue_cagr_min,
    pat_cagr_min,
    opm_min,
    icr_min,
)

# ----------------------------
# Results
# ----------------------------
st.subheader(f"📊 Companies Matching Filters: {len(filtered_df)}")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Results as CSV",
    data=csv,
    file_name="nifty100_screener.csv",
    mime="text/csv",
)

display_df = filtered_df[
    [
        "company_id",
        "company_name",
        "broad_sector",
        "composite_quality_score",
        "return_on_equity_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "operating_profit_margin_pct",
        "interest_coverage",
    ]
]

st.dataframe(
    display_df,
    width="stretch",
)