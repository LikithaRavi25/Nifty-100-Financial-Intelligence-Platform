import streamlit as st
import pandas as pd

from utils.db import get_annual_reports

st.title("📄 Annual Reports")

st.markdown(
"""
Browse company annual reports directly from BSE.
"""
)

st.divider()

df = get_annual_reports()

company = st.selectbox(

    "Select Company",

    sorted(
        df["company_name"].unique()
    )

)

company_df = df[
    df["company_name"] == company
]

st.subheader(f"📑 {company} Annual Reports")

for _, row in company_df.iterrows():

    with st.expander(
        f"📅 Annual Report {row['year']}"
    ):

        if (
            pd.isna(row["annual_report"])
            or row["annual_report"] == ""
        ):

            st.error("🔴 Report Unavailable")

        else:

            st.link_button(
                "📥 Open BSE Annual Report",
                row["annual_report"]
            )
    st.divider()

    