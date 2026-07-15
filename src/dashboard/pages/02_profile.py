import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from src.dashboard.services.profile_service import (
    get_company_list,
    get_company_profile,
    get_company_kpis,
    get_revenue_profit_history,
    get_profitability_history,
    get_balance_sheet_highlights,
    get_cashflow_highlights,
)
st.set_page_config(
    page_title="Company Profile",
    page_icon="🏢",
    layout="wide",
)

st.title("🏢 Company Profile")

# ---------------------------------------------------
# Company Selection
# ---------------------------------------------------

companies = get_company_list()

companies["display_name"] = (
    companies["ticker"] + " - " + companies["company_name"]
)

selected_company = st.selectbox(
    "Search Company (Ticker or Name)",
    companies["display_name"],
)

ticker = selected_company.split(" - ")[0]

profile = get_company_profile(ticker)

if profile is None:
    st.error("Ticker not found — please try another.")
    st.stop()

kpis = get_company_kpis(ticker)

# ---------------------------------------------------
# Helper Functions
# ---------------------------------------------------

def format_percentage(value):
    if value is None:
        return "N/A"
    return f"{float(value):.2f}%"


def format_number(value):
    if value is None:
        return "N/A"
    return f"{float(value):.2f}"


def format_currency(value):
    if value is None:
        return "N/A"
    return f"₹{float(value):,.0f} Cr"


# ---------------------------------------------------
# Company Information
# ---------------------------------------------------

st.markdown("## Company Information")

col1, col2 = st.columns(2)

with col1:
    st.write(f"**Company Name:** {profile['company_name']}")
    st.write(f"**Ticker:** {profile['ticker']}")
    st.write(f"**Sector:** {profile['broad_sector']}")

with col2:
    st.write(f"**Sub-Sector:** {profile['sub_sector']}")

# ---------------------------------------------------
# KPI Cards
# ---------------------------------------------------

st.divider()

st.subheader("📊 Financial Highlights")

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

with col1:
    st.metric(
        "ROE",
        format_percentage(kpis["return_on_equity_pct"]),
    )

with col2:
    st.metric(
        "ROCE",
        format_percentage(
            kpis["return_on_capital_employed_pct"]
        ),
    )

with col3:
    st.metric(
        "Net Profit Margin",
        format_percentage(
            kpis["net_profit_margin_pct"]
        ),
    )

with col4:
    st.metric(
        "Debt / Equity",
        format_number(
            kpis["debt_to_equity"]
        ),
    )

with col5:
    st.metric(
        "Revenue CAGR (5Y)",
        format_percentage(
            kpis["revenue_cagr_5yr"]
        ),
    )

with col6:
    st.metric(
        "Free Cash Flow",
        format_currency(
            kpis["free_cash_flow_cr"]
        ),
    )

# ---------------------------------------------------
# Revenue vs Net Profit
# ---------------------------------------------------

history_df = get_revenue_profit_history(ticker)

st.divider()

years = len(history_df)

st.subheader(
    f"📊 Revenue vs Net Profit ({years}-Year History)"
)

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=history_df["year"],
        y=history_df["sales"],
        name="Revenue",
    )
)

fig.add_trace(
    go.Bar(
        x=history_df["year"],
        y=history_df["net_profit"],
        name="Net Profit",
    )
)

fig.update_layout(
    barmode="group",
    xaxis_title="Financial Year",
    yaxis_title="₹ Crore",
    height=500,
)

st.plotly_chart(fig, width="stretch")

# ---------------------------------------------------
# Profitability Trend
# ---------------------------------------------------

profit_df = get_profitability_history(ticker)

st.divider()

st.subheader("📈 Profitability Trend")

profit_df = profit_df.rename(
    columns={
        "return_on_equity_pct": "ROE",
        "return_on_capital_employed_pct": "ROCE",
        "net_profit_margin_pct": "Net Profit Margin",
    }
)

fig = px.line(
    profit_df,
    x="year",
    y=["ROE", "ROCE", "Net Profit Margin"],
    markers=True,
    title="ROE vs ROCE vs Net Profit Margin",
)

fig.update_layout(
    height=500,
    legend_title="Financial Ratios",
)

st.plotly_chart(fig, width="stretch")

# ---------------------------------------------------
# Balance Sheet Highlights
# ---------------------------------------------------

bs = get_balance_sheet_highlights(ticker)
cashflow = get_cashflow_highlights(ticker)
if bs is not None:

    st.divider()

    st.subheader("🏦 Balance Sheet Highlights")

    c1, c2, c3 = st.columns(3)
    c4, c5, c6 = st.columns(3)

    with c1:
        st.metric(
            "Total Assets",
            f"₹{bs['total_assets']:,.0f} Cr"
        )

    with c2:
        st.metric(
            "Total Liabilities",
            f"₹{bs['total_liabilities']:,.0f} Cr"
        )

    with c3:
        st.metric(
            "Equity Capital",
            f"₹{bs['equity_capital']:,.0f} Cr"
        )

    with c4:
        st.metric(
            "Reserves",
            f"₹{bs['reserves']:,.0f} Cr"
        )

    with c5:
        st.metric(
            "Borrowings",
            f"₹{bs['borrowings']:,.0f} Cr"
        )

    with c6:
        st.metric(
            "Investments",
            f"₹{bs['investments']:,.0f} Cr"
        )
st.divider()

st.subheader("💵 Cash Flow Highlights")

c1, c2 = st.columns(2)
c3, c4 = st.columns(2)

with c1:
    st.metric(
        "Operating Cash Flow",
        format_currency(cashflow["operating_activity"])
    )

with c2:
    st.metric(
        "Investing Cash Flow",
        format_currency(cashflow["investing_activity"])
    )

with c3:
    st.metric(
        "Financing Cash Flow",
        format_currency(cashflow["financing_activity"])
    )

with c4:
    st.metric(
        "Net Cash Flow",
        format_currency(cashflow["net_cash_flow"])
    )
# ---------------------------------------------------
# About Company
# ---------------------------------------------------

st.divider()

st.subheader("ℹ️ About Company")

st.info(profile["about_company"])