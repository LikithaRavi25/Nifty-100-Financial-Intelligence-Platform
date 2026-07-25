import streamlit as st
import plotly.express as px
import pandas as pd

from utils.db import get_sector_data
st.title("🏭 Sector Analysis")

st.markdown("""
Compare companies within each sector
using interactive visualizations.
""")

st.divider()
df = get_sector_data()
print(df.columns.tolist())
sector = st.selectbox(

    "Select Sector",

    sorted(df["broad_sector"].unique())

)
sector_df = df[
    df["broad_sector"] == sector
]
fig = px.scatter(

    sector_df,

    x="sales",

    y="return_on_equity_pct",

    size="market_cap_crore",
    color="sub_sector",

    hover_name="company_name",

    title=f"{sector} Companies"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader("📊 Sector Median KPIs")


sector_kpi = sector_df[
    [
        "return_on_equity_pct",
        "sales",
        "market_cap_crore"
    ]
].median()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Median Market Cap",
        f"₹ {sector_kpi['market_cap_crore']:,.0f} Cr"
    )

with col2:
    st.metric(
        "Median Sales",
        f"₹ {sector_kpi['sales']:,.0f} Cr"
    )

with col3:
    st.metric(
        "Median ROE",
        f"{sector_kpi['return_on_equity_pct']:.2f}%"
    )



kpi_df = sector_kpi.reset_index()

kpi_df.columns = [
    "Metric",
    "Median"
]

import plotly.express as px

fig = px.bar(

    kpi_df,

    x="Metric",

    y="Median",

    text="Median",

    title=f"{sector} Sector Median KPIs"

)

st.plotly_chart(
    fig,
    use_container_width=True
)