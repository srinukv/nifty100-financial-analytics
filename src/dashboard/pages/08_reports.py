import streamlit as st

from src.dashboard.services.reports_service import (
    get_company_list,
    get_reports,
    is_report_available,
)

st.set_page_config(
    page_title="Annual Reports",
    layout="wide",
)

st.title("📄 Annual Reports")

companies = get_company_list()

selected = st.selectbox(
    "Select Company",
    companies["display_name"],
)

company_id = selected.split(" - ")[0]

reports = get_reports(company_id)

st.subheader(f"{company_id} Annual Reports")

if reports.empty:
    st.warning("No reports available.")
    st.stop()

for _, row in reports.iterrows():

    year = int(row["Year"])
    url = row["Annual_Report"]

    col1, col2 = st.columns([1, 5])

    with col1:
        st.markdown(f"### {year}")

    with col2:

        if is_report_available(url):

            st.link_button(
        "📄 Open Annual Report",
        url,
            use_container_width=True,
    )

        else:

            st.error("🔴 Annual report not available or link is no longer accessible.")