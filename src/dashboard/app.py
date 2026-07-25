import streamlit as st

st.set_page_config(
    page_title="NIFTY 100 Financial Intelligence Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📈 NIFTY 100 Financial Intelligence Platform")

st.markdown("""
## Welcome

This dashboard provides analytics for NIFTY 100 companies.

Use the **sidebar** to navigate between the different modules.
""")

st.info("Select a page from the sidebar.")