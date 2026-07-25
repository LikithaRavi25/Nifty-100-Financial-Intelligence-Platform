import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import get_home_metrics
from components.cards import metric_card
from utils.db import (
    get_home_metrics,
    get_sector_distribution,
    get_top_companies
)

st.title("🏠 Home Dashboard")

year = st.sidebar.selectbox(
    "Financial Year",
    [
        "2019-03",
        "2020-03",
        "2021-03",
        "2022-03",
        "2023-03",
        "2024-03"
    ],
    index=5
)

data = get_home_metrics(year)
sector_data = get_sector_distribution()
top_companies = get_top_companies(year)

avg_roe = round(
    data["return_on_equity_pct"].mean(),
    2
)

median_de = round(
    data["debt_to_equity"].median(),
    2
)

median_rev = round(
    data["revenue_cagr_5yr"].median(),
    2
)

companies = data["company_id"].nunique()

debt_free = (
    data["debt_to_equity"] == 0
).sum()

# Placeholder until valuation module
median_pe = "Coming Soon"

row1 = st.columns(3)

with row1[0]:
    metric_card(
        "Average ROE",
        f"{avg_roe}%"
    )

with row1[1]:
    metric_card(
        "Median P/E",
        median_pe
    )

with row1[2]:
    metric_card(
        "Median D/E",
        median_de
    )

row2 = st.columns(3)

with row2[0]:
    metric_card(
        "Companies",
        companies
    )

with row2[1]:
    metric_card(
        "Median Revenue CAGR",
        f"{median_rev}%"
    )

with row2[2]:
    metric_card(
        "Debt-Free Companies",
        debt_free
    )

st.divider()

st.subheader("🏭 Sector Breakdown")

fig = px.pie(
    sector_data,
    names="peer_group_name",
    values="companies",
    hole=0.55,
    title="Company Distribution by Peer Group"
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

fig.update_layout(
    height=550,
    legend_title="Peer Groups"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.divider()

st.subheader("🏆 Top 5 Companies by Composite Quality Score")

st.dataframe(
    top_companies,
    use_container_width=True,
    hide_index=True
)