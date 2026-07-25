import streamlit as st
import plotly.express as px
import pandas as pd

from utils.db import (
    get_companies,
    get_trend_data
)

st.title("📈 Company Trend Analysis")

st.markdown("""
Analyze long-term financial performance
using interactive trend charts.
""")

st.divider()

companies = get_companies()
company_dict = dict(
    zip(
        companies["company_name"],
        companies["id"]
    )
)

company = st.selectbox(

    "Select Company",

    list(company_dict.keys())

)

ticker = company_dict[company]
trend = get_trend_data(ticker)


metrics = st.multiselect(
    "Select up to 3 Metrics",
    [
        "sales",
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "debt_to_equity",
        "free_cash_flow_cr",
        "interest_coverage",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr"
    ],
    default=["sales"],
    max_selections=3
)
trend = trend.copy()
for metric in metrics:

    trend[f"{metric}_yoy"] = (
        trend[metric]
        .pct_change()
        .mul(100)
        .round(2)
    )


import plotly.graph_objects as go

fig = go.Figure()

for metric in metrics:

    fig.add_trace(

        go.Scatter(

            x=trend["year"],

            y=trend[metric],

            mode="lines+markers+text",

            name=metric.replace("_", " ").title(),

            text=[
                ""
                if pd.isna(v)
                else f"{v:+.1f}%"
                for v in trend[f"{metric}_yoy"]
            ],

            textposition="top center"

        )

    )

fig.update_layout(

    title="10-Year Financial Trend",

    xaxis_title="Financial Year",

    yaxis_title="Value",

    hovermode="x unified"

)

st.plotly_chart(
    fig,
    use_container_width=True
)





