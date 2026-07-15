from pathlib import Path
import sys

# ------------------------------------------------------------------
# Add project root to Python path
# ------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ------------------------------------------------------------------
# Streamlit App
# ------------------------------------------------------------------
import streamlit as st

st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Nifty 100 Financial Analytics")

st.markdown("""
Welcome to the **Nifty100 Financial Analytics Dashboard**.

Use the **sidebar** to navigate between the dashboard pages.
""")