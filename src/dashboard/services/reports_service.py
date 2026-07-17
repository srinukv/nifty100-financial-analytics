import streamlit as st
import requests

from src.dashboard.utils.db import execute_query


# -------------------------------------------------------
# Company List
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_company_list():
    """
    Returns all companies for the dropdown.
    """

    query = """
    SELECT
        id,
        company_name
    FROM companies
    ORDER BY company_name;
    """

    df = execute_query(query)

    df["display_name"] = (
        df["id"] +
        " - " +
        df["company_name"]
    )

    return df


# -------------------------------------------------------
# Annual Reports
# -------------------------------------------------------

@st.cache_data(ttl=600)
def get_reports(company_id):
    """
    Returns all annual reports for a company.
    """

    query = """
    SELECT
        Year,
        Annual_Report
    FROM documents
    WHERE company_id = ?
    ORDER BY Year DESC;
    """

    return execute_query(query, (company_id,))


# -------------------------------------------------------
# Validate Report URL
# -------------------------------------------------------

@st.cache_data(ttl=3600)
def is_report_available(url):
    if not url or str(url).strip() == "":
        return False

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            allow_redirects=True,
            timeout=10,
            stream=True,
        )

        if response.status_code != 200:
            return False

        content_type = response.headers.get("Content-Type", "").lower()

        if "pdf" in content_type:
            return True

        if "page not found" in response.text.lower():
            return False

        return False

    except requests.RequestException:
        return False